"use strict";

/* ============================================================
   Engine.  All song-specific data lives in songs.js; this file
   knows nothing about any particular song.
   ============================================================ */

const $ = id => document.getElementById(id);
const esc = t => String(t).replace(/[&<>"]/g, c =>
  ({ "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;" }[c]));

/* ---- per-song state, all rebuilt by loadSong() ---- */
let SONG, SONG_ID, EVENTS = [], TOTAL = 0, LINE_BARS = [];
let pattern, cues = {}, editingCues = false;
let lyricStatus = "";   // set when cues came from lyrics/<id>.txt

/* ---- transport state ---- */
let bpm = 100, capo = 0, soundMode = "both";
let playing = false, cursor = 0, loopSection = null;
let ctx = null, master = null, nextStepTime = 0, stepIndex = 0, schedTimer = null;
const drawQueue = [];

const stepsPerBeat = () => SONG.stepsPerBar / SONG.beatsPerBar;
const stepDur      = () => (60 / bpm) / stepsPerBeat();
const fretStr      = n => SONG.shapes[n].frets.map(f => f < 0 ? "x" : f).join(" ");

/* ============================================================
   Audio
   ============================================================ */
function initAudio(){
  if (ctx) return;
  ctx = new (window.AudioContext || window.webkitAudioContext)();
  master = ctx.createGain();
  master.gain.value = 0.85;
  master.connect(ctx.destination);
}

function pluck(midi, when, vel){
  if (soundMode === "off" || soundMode === "click") return;
  const f = 440 * Math.pow(2, (midi - 69) / 12);
  const out = ctx.createGain();
  out.gain.setValueAtTime(0.16, when);
  out.connect(master);
  [[1,1.0,2.6],[2,0.42,1.5],[3,0.20,0.9],[4,0.10,0.6],[5,0.05,0.4]].forEach(([mult,amp,dec]) => {
    const o = ctx.createOscillator(), g = ctx.createGain();
    o.type = "triangle";
    o.frequency.value = f * mult;
    g.gain.setValueAtTime(0, when);
    g.gain.linearRampToValueAtTime(amp * vel, when + 0.004);
    g.gain.exponentialRampToValueAtTime(0.0001, when + dec);
    o.connect(g); g.connect(out);
    o.start(when); o.stop(when + dec + 0.05);
  });
}

function click(when, accent){
  if (soundMode === "off" || soundMode === "guitar") return;
  const o = ctx.createOscillator(), g = ctx.createGain();
  o.type = "square";
  o.frequency.value = accent ? 1500 : 950;
  g.gain.setValueAtTime(0.09, when);
  g.gain.exponentialRampToValueAtTime(0.0001, when + 0.035);
  o.connect(g); g.connect(master);
  o.start(when); o.stop(when + 0.05);
}

const stringMidi = (shape, str) =>
  shape.frets[str] < 0 ? null : OPEN_MIDI[str] + shape.frets[str] + capo;

/* Which strings a pattern step plucks, for a given chord shape.
   step.b === 1 -> the chord's root bass, 2 -> its alternate bass,
   step.s -> a fixed string index, step.strum -> the whole chord. */
function stepStrings(shape, st){
  if (!st) return [];
  if (st.strum){
    const all = [];
    shape.frets.forEach((f, i) => { if (f >= 0) all.push(i); });
    return st.strum === "u" ? all.reverse() : all;
  }
  const out = [];
  let primary = st.b === 2 ? (shape.alt != null ? shape.alt : shape.bass)
              : st.b === 1 ? shape.bass
              : st.s;
  if (shape.frets[primary] >= 0) out.push(primary);
  else for (let d = 1; d < 6; d++){                 // nearest sounding string
    if (shape.frets[primary + d] >= 0){ out.push(primary + d); break; }
    if (shape.frets[primary - d] >= 0){ out.push(primary - d); break; }
  }
  if (st.pinch != null && shape.frets[st.pinch] >= 0) out.push(st.pinch);
  return out;
}

/* ============================================================
   Scheduler
   ============================================================ */
function scheduleStep(idx, step, when){
  const shape = SONG.shapes[EVENTS[idx].chord];
  const st = pattern.steps[step];
  if (step % stepsPerBeat() === 0) click(when, step === 0);
  const spread = st && st.strum ? 0.014 : 0.006;
  stepStrings(shape, st).forEach((s, i) => {
    const m = stringMidi(shape, s);
    if (m != null) pluck(m, when + i * spread, st.f === "p" && i === 0 ? 1.0 : 0.7);
  });
  drawQueue.push({ idx, step, when });
}

function advance(){
  if (++stepIndex >= SONG.stepsPerBar){
    stepIndex = 0;
    cursor++;
    if (loopSection != null){
      const s = SONG.sections[loopSection];
      if (cursor >= s.end) cursor = s.start;
    } else if (cursor >= TOTAL) cursor = 0;
  }
  nextStepTime += stepDur();
}

function scheduler(){
  /* 0% tempo: hold position and keep the clock fresh, so raising the
     slider again resumes smoothly instead of firing a burst of catch-up. */
  if (bpm <= 0){ nextStepTime = ctx.currentTime + 0.05; return; }
  while (nextStepTime < ctx.currentTime + 0.12){
    scheduleStep(cursor, stepIndex, nextStepTime);
    advance();
  }
}

function start(){
  initAudio();
  if (ctx.state === "suspended") ctx.resume();
  playing = true;
  stepIndex = 0;
  nextStepTime = ctx.currentTime + 0.08;
  schedTimer = setInterval(scheduler, 25);
  $("play").innerHTML = "&#10074;&#10074; Pause";
  $("nowLabel").textContent = "Now playing";
}

function stop(){
  playing = false;
  clearInterval(schedTimer);
  schedTimer = null;
  drawQueue.length = 0;
  $("play").innerHTML = "&#9654; Play";
  $("nowLabel").textContent = "Paused";
  document.querySelectorAll(".dot").forEach(d => d.classList.remove("on","down"));
  document.querySelectorAll(".pg-cell.active").forEach(c => c.classList.remove("active"));
}

const toggle = () => playing ? stop() : start();

/* ============================================================
   Chord diagrams
   ============================================================ */
function diagram(name, size){
  const shape = SONG.shapes[name];
  if (!shape) return "";
  const W = size, H = size * 1.18;
  const padX = W * 0.17, padTop = H * 0.20, padBot = H * 0.08;
  const gw = W - padX * 2, gh = H - padTop - padBot;
  const NF = 4, sx = gw / 5, fy = gh / NF;

  const fretted = shape.frets.filter(f => f > 0);
  const minF = fretted.length ? Math.min.apply(null, fretted) : 1;
  const maxF = fretted.length ? Math.max.apply(null, fretted) : 1;
  const base = maxF <= NF ? 1 : minF;

  let s = '<svg viewBox="0 0 ' + W + ' ' + H + '" width="' + W + '" height="' + H +
          '" role="img" aria-label="' + name + ' chord diagram, frets ' + fretStr(name) + '">';

  if (base === 1)
    s += '<rect x="' + (padX-1) + '" y="' + (padTop-3) + '" width="' + (gw+2) + '" height="4" fill="#fff" rx="1"/>';
  else
    s += '<text x="' + (padX-9) + '" y="' + (padTop + fy*0.66) + '" font-size="' + (W*0.115) +
         '" fill="#ff0" text-anchor="end" font-family="monospace" font-weight="700">' + base + '</text>';

  for (let f = 1; f <= NF; f++)
    s += '<line x1="' + padX + '" y1="' + (padTop+f*fy) + '" x2="' + (padX+gw) + '" y2="' + (padTop+f*fy) + '" stroke="#0ff" stroke-width="1"/>';
  for (let i = 0; i < 6; i++)
    s += '<line x1="' + (padX+i*sx) + '" y1="' + padTop + '" x2="' + (padX+i*sx) + '" y2="' + (padTop+gh) + '" stroke="#888" stroke-width="1"/>';

  const b = shape.barre;
  if (b){
    const y = padTop + (b.fret - base) * fy + fy/2;
    s += '<rect x="' + (padX + b.from*sx - sx*0.3) + '" y="' + (y - fy*0.28) + '" width="' +
         ((b.to-b.from)*sx + sx*0.6) + '" height="' + (fy*0.56) + '" rx="' + (fy*0.28) + '" fill="#ff0"/>';
    const fg = shape.fingers[b.to];
    if (fg) s += '<text x="' + (padX + (b.from + (b.to-b.from)/2)*sx) + '" y="' + (y + W*0.04) +
                 '" font-size="' + (W*0.11) + '" fill="#000" text-anchor="middle" font-weight="700" font-family="monospace">' + fg + '</text>';
  }

  shape.frets.forEach((fr, i) => {
    const x = padX + i*sx;
    if (fr < 0){
      const r = W * 0.030;
      s += '<g stroke="#f00" stroke-width="1.6" stroke-linecap="round">' +
           '<line x1="' + (x-r) + '" y1="' + (padTop-r-7) + '" x2="' + (x+r) + '" y2="' + (padTop+r-7) + '"/>' +
           '<line x1="' + (x+r) + '" y1="' + (padTop-r-7) + '" x2="' + (x-r) + '" y2="' + (padTop+r-7) + '"/></g>';
    } else if (fr === 0){
      s += '<circle cx="' + x + '" cy="' + (padTop-7) + '" r="' + (W*0.032) + '" fill="none" stroke="#0f0" stroke-width="1.6"/>';
    } else {
      if (b && fr === b.fret && i >= b.from && i <= b.to) return;   // under the barre
      const cy = padTop + (fr - base)*fy + fy/2;
      s += '<circle cx="' + x + '" cy="' + cy + '" r="' + (sx*0.34) + '" fill="#ff0"/>';
      const fg = shape.fingers[i];
      if (fg) s += '<text x="' + x + '" y="' + (cy + W*0.04) + '" font-size="' + (W*0.11) +
                   '" fill="#000" text-anchor="middle" font-weight="700" font-family="monospace">' + fg + '</text>';
    }
  });
  return s + "</svg>";
}

/* ============================================================
   Cues -- typed by the user, stored in this browser only.
   Only bar positions ship with the page; never any lyric text.
   ============================================================ */
const saveCues = () => {
  try { localStorage.setItem(SONG.cueKey, JSON.stringify(cues)); } catch(_){}
};

function cueFor(idx){
  for (let i = idx; i >= 0; i--) if (cues[i]) return cues[i];
  return "";
}

/* ------------------------------------------------------------
   Optional local lyric file: lyrics/<song id>.txt

   Never committed (see .gitignore) and never shipped -- this only
   reads whatever the user has put on their own machine.  Plain lines
   fill the sung-line slots in order; a "12: text" line pins that bar
   and wins over the sequential fill.
   ------------------------------------------------------------ */
function parseLyricFile(text){
  const out = {}, plain = [];
  text.split(/\r?\n/).forEach(raw => {
    const line = raw.trim();
    if (!line || line.charAt(0) === "#") return;
    const m = line.match(/^(\d+)\s*[:|]\s*(.*)$/);
    if (m){
      const n = +m[1] - 1, t = m[2].trim();
      if (n >= 0 && n < TOTAL && t) out[n] = t;
    } else {
      plain.push(line);
    }
  });
  plain.slice(0, LINE_BARS.length).forEach((t, i) => {
    if (out[LINE_BARS[i]] === undefined) out[LINE_BARS[i]] = t;
  });
  return out;
}

function loadLyricFile(id){
  fetch("lyrics/" + id + ".txt", { cache:"no-store" })
    .then(r => r.ok ? r.text() : null)
    .then(text => {
      if (text == null || SONG_ID !== id) return;      // song switched while fetching
      const parsed = parseLyricFile(text);
      const n = Object.keys(parsed).length;
      if (!n) return;
      cues = parsed;
      lyricStatus = '<span style="color:#0f0">&mdash; ' + n +
        ' cue' + (n === 1 ? "" : "s") + ' loaded from <b>lyrics/' + id +
        '.txt</b>; edits here won\'t change that file</span>';
      buildTimeline(); bindTimeline();
      lastDrawn = -1;
      paint(cursor, lastStep < 0 ? 0 : lastStep);
    })
    .catch(() => {});                                   // no file, or opened over file://
}

/* ============================================================
   Rendering
   ============================================================ */
function buildTimeline(){
  $("tl").innerHTML = SONG.sections.map((s, si) => {
    const kind = /chorus/i.test(s.name) ? " chorus" : /bridge/i.test(s.name) ? " bridge" : "";
    const cells = s.chords.map((c, i) => {
      const gi = s.start + i;
      const chip = '<button class="chip" data-i="' + gi + '">' + c + '</button>';
      return editingCues
        ? '<div class="cue-cell">' + chip + '<input data-cue="' + gi + '" value="' +
          esc(cues[gi] || "") + '" placeholder="' + (gi+1) + '…" aria-label="Cue for bar ' + (gi+1) + '"></div>'
        : chip;
    }).join("");
    return '<div class="tl-sec' + kind + '">' +
      '<div class="tl-head"><span class="tl-name">' + s.name + '</span>' +
      '<span class="tl-bars">' + s.chords.length + ' bars</span>' +
      '<button class="tl-loop" data-loop="' + si + '">Loop</button></div>' +
      '<div class="tl-chords' + (editingCues ? " editing" : "") + '">' + cells + '</div></div>';
  }).join("");

  if (editingCues) $("tl").insertAdjacentHTML("afterbegin",
    '<div class="bulk">' +
      '<p><b>Align lines</b> &mdash; paste the ' + LINE_BARS.length + ' sung lines of this song, one per line, ' +
      'in order. Blank lines are ignored, so pasting whole verses with gaps between them is fine. ' +
      'They drop onto the ' + LINE_BARS.length + ' bars where the singing starts.</p>' +
      '<p><b>Apply numbered</b> &mdash; for full control, use <b>bar number : text</b> per line. ' +
      'Bars run <b>1&ndash;' + TOTAL + '</b> straight through and every box below shows its own number. ' +
      'A cue holds on screen until the next one starts.</p>' +
      '<textarea id="bulkText" placeholder="paste the sung lines here, one per line…" spellcheck="false"></textarea>' +
      '<div class="bulk-row">' +
        '<button class="btn primary" id="bulkAlign">Align lines</button>' +
        '<button class="btn" id="bulkApply">Apply numbered</button>' +
        '<button class="btn" id="bulkLoad">Load current</button>' +
        '<button class="btn" id="bulkClear">Clear all</button>' +
        '<span class="bulk-msg" id="bulkMsg"></span>' +
      '</div></div>');

  $("cueHint").innerHTML = editingCues
    ? '<span style="color:#0f0">&mdash; each cue stays on screen until the next</span>'
    : lyricStatus;
}

function buildLib(){
  $("lib").innerHTML = Object.keys(SONG.shapes).map(n =>
    '<div class="cc" data-chord="' + n + '"><div class="cc-name">' + n + '</div>' +
    '<div class="cc-sub">' + fretStr(n).replace(/ /g, "") + '</div>' + diagram(n, 108) + '</div>'
  ).join("");
}

function buildPatGrid(){
  const N = SONG.stepsPerBar, spb = stepsPerBeat();
  let html = '<div class="pg-cell pg-head"></div>';
  for (let i = 0; i < N; i++)
    html += '<div class="pg-cell pg-head' + (i % spb === 0 ? " beat" : "") + '">' + (i+1) + '</div>';
  SONG.gridStrings.forEach(pair => {
    html += '<div class="pg-cell pg-str">' + pair[1] + '</div>';
    for (let s = 0; s < N; s++)
      html += '<div class="pg-cell" data-step="' + s + '" data-str="' + pair[0] + '"></div>';
  });
  $("patGrid").innerHTML = html;
  $("patGrid").style.gridTemplateColumns = "28px repeat(" + N + ", 1fr)";
  $("patName").innerHTML = pattern.name;
  $("patDesc").innerHTML = pattern.desc;
}

/* The thumb's string depends on the chord, so the grid is re-marked
   on every chord change rather than once per pattern. */
function markPattern(chordName){
  const shape = SONG.shapes[chordName];
  document.querySelectorAll(".pg-cell[data-step]").forEach(c => {
    c.className = "pg-cell";
    c.textContent = "";
  });
  pattern.steps.forEach((st, si) => {
    if (!st) return;
    const strs = stepStrings(shape, st);
    strs.forEach((str, i) => {
      const cell = document.querySelector('.pg-cell[data-step="' + si + '"][data-str="' + str + '"]');
      if (!cell) return;
      cell.classList.add("hit");
      if (st.strum){
        cell.textContent = st.strum === "u" ? "↑" : "↓";
      } else if (st.f === "p" && i === 0){
        cell.classList.add("thumb");
        cell.textContent = "p";
      } else {
        cell.textContent = st.pinch === str && i > 0 ? "a" : st.f;
      }
    });
  });
}

/* ============================================================
   Display
   ============================================================ */
let lastDrawn = -1, lastStep = -1, lastChordShown = null;

function paint(idx, step){
  const ev = EVENTS[idx];

  if (idx !== lastDrawn){
    $("nowChord").textContent = ev.chord;
    $("nowFrets").textContent = fretStr(ev.chord);
    $("nextChord").textContent = EVENTS[(idx+1) % TOTAL].chord;
    $("thenChord").textContent = EVENTS[(idx+2) % TOTAL].chord;

    const sec = SONG.sections[ev.sectionIdx], pos = idx - sec.start;
    $("barNum").textContent = pos + 1;
    $("nowSec").textContent = sec.name + " · bar " + (pos+1) + " of " + sec.chords.length;
    $("nowCue").textContent = cueFor(idx);

    if (ev.chord !== lastChordShown){
      $("nowDiagram").innerHTML = diagram(ev.chord, 152);
      lastChordShown = ev.chord;
      document.querySelectorAll(".cc").forEach(c =>
        c.classList.toggle("cur", c.dataset.chord === ev.chord));
      markPattern(ev.chord);
      lastStep = -1;
    }

    document.querySelectorAll(".chip").forEach(c => {
      const i = +c.dataset.i;
      c.classList.toggle("cur", i === idx);
      c.classList.toggle("done", i < idx);
    });
    const cur = document.querySelector(".chip.cur");
    const box = $("tl");
    if (cur && box.scrollHeight > box.clientHeight + 2){
      const top = cur.offsetTop - box.offsetTop;
      if (top < box.scrollTop || top > box.scrollTop + box.clientHeight - 60)
        box.scrollTo({ top: top - box.clientHeight/2, behavior:"smooth" });
    }
    lastDrawn = idx;
  }

  if (step !== lastStep){
    document.querySelectorAll(".pg-cell.active").forEach(c => c.classList.remove("active"));
    document.querySelectorAll('.pg-cell[data-step="' + step + '"].hit').forEach(c => c.classList.add("active"));
    document.querySelectorAll(".dot").forEach((d, i) => {
      d.classList.toggle("on", i === step);
      d.classList.toggle("down", i === step && step === 0);
    });
    lastStep = step;
  }
}

function frame(){
  if (playing && ctx){
    const now = ctx.currentTime;
    let ev = null;
    while (drawQueue.length && drawQueue[0].when <= now) ev = drawQueue.shift();
    if (ev) paint(ev.idx, ev.step);
  }
  requestAnimationFrame(frame);
}

/* ============================================================
   Song loading
   ============================================================ */
function loadSong(id){
  if (playing) stop();
  SONG_ID = id;
  SONG = SONGS[id];

  /* sections -> flat bar list, and the sung-line bar map */
  EVENTS = [];
  SONG.sections.forEach((s, si) => {
    if (typeof s.chords === "string") s.chords = s.chords.trim().split(/\s+/);
    s.start = EVENTS.length;
    s.chords.forEach(c => EVENTS.push({ chord:c, sectionIdx:si }));
    s.end = EVENTS.length;
  });
  TOTAL = EVENTS.length;
  LINE_BARS = SONG.sections.reduce((acc, s) =>
    acc.concat((s.lines || []).map(o => s.start + o)), []);

  bpm = SONG.bpm;
  capo = 0;
  cursor = 0; stepIndex = 0; loopSection = null;
  lastDrawn = -1; lastStep = -1; lastChordShown = null;
  pattern = SONG.patterns[0];
  editingCues = false;

  lyricStatus = "";
  try { cues = JSON.parse(localStorage.getItem(SONG.cueKey) || "{}"); } catch(_){ cues = {}; }

  /* header */
  $("hTitle").textContent = SONG.title;
  $("hByline").innerHTML = SONG.artist + " &middot; <i>" + SONG.album + "</i>";
  $("hFacts").innerHTML = SONG.facts.map(f =>
    '<span class="fact"><b>' + f[0] + '</b> ' + f[1] + '</span>').join("");
  document.title = SONG.title + " — Guitar Karaoke";

  /* controls */
  $("tempo").value = 100;
  $("tempoOut").textContent = SONG.bpm + " BPM · 100%";
  $("capo").innerHTML = Array.from({length:8}, (_, i) =>
    '<option value="' + i + '">' + (i === 0 ? "None" : i) + "</option>").join("");
  $("pattern").innerHTML = SONG.patterns.map((p, i) =>
    '<option value="' + i + '">' + p.name + "</option>").join("");
  $("cueEdit").classList.remove("on");
  $("cueEdit").innerHTML = "&#9998; Cues";
  $("dots").innerHTML = Array.from({length:SONG.stepsPerBar}, (_, i) =>
    '<span class="dot' + (i % stepsPerBeat() === 0 ? " beat" : "") + '"></span>').join("");

  /* panels */
  $("notes").innerHTML = SONG.notes.map(n =>
    '<div class="panel note ' + (n.cls || "") + '"><h3>' + n.h + "</h3>" + n.body + "</div>").join("");

  buildLib(); buildPatGrid(); buildTimeline(); bindTimeline();
  markPattern(EVENTS[0].chord);
  paint(0, 0);
  loadLyricFile(id);      // overrides the stored cues if the file exists
}

/* ============================================================
   Events
   ============================================================ */
function reseek(){
  stepIndex = 0; lastDrawn = -1;
  if (playing){ drawQueue.length = 0; nextStepTime = ctx.currentTime + 0.05; }
  else paint(cursor, 0);
}

function bindTimeline(){
  document.querySelectorAll(".chip").forEach(c =>
    c.onclick = () => { cursor = +c.dataset.i; reseek(); });

  document.querySelectorAll(".tl-loop").forEach(b =>
    b.onclick = () => {
      const si = +b.dataset.loop;
      loopSection = loopSection === si ? null : si;
      document.querySelectorAll(".tl-loop").forEach(x =>
        x.classList.toggle("on", +x.dataset.loop === loopSection));
      const s = SONG.sections[si];
      if (loopSection != null && (cursor < s.start || cursor >= s.end)){
        cursor = s.start; reseek();
      }
    });

  document.querySelectorAll("input[data-cue]").forEach(inp => {
    inp.oninput = () => {
      const i = +inp.dataset.cue, v = inp.value.trim();
      if (v) cues[i] = v; else delete cues[i];
      saveCues();
      $("nowCue").textContent = cueFor(cursor);
    };
    inp.onkeydown = e => e.stopPropagation();
  });

  const bt = $("bulkText");
  if (!bt) return;
  bt.onkeydown = e => e.stopPropagation();

  const refresh = msg => {
    saveCues();
    buildTimeline(); bindTimeline();
    lastDrawn = -1; paint(cursor, lastStep < 0 ? 0 : lastStep);
    if (msg) $("bulkMsg").textContent = msg;
  };

  $("bulkAlign").onclick = () => {
    const lines = bt.value.split(/\r?\n/).map(l => l.trim()).filter(Boolean);
    if (!lines.length){ $("bulkMsg").textContent = "nothing to align — paste the lines first"; return; }
    LINE_BARS.forEach(b => delete cues[b]);
    const n = Math.min(lines.length, LINE_BARS.length);
    for (let i = 0; i < n; i++) cues[LINE_BARS[i]] = lines[i];
    const extra = lines.length - n, short = LINE_BARS.length - n;
    refresh(n + " line" + (n === 1 ? "" : "s") + " aligned" +
      (extra ? " · " + extra + " left over (only " + LINE_BARS.length + " slots)" : "") +
      (short ? " · " + short + " slot" + (short === 1 ? "" : "s") + " still empty" : ""));
  };

  $("bulkApply").onclick = () => {
    let applied = 0, skipped = 0;
    bt.value.split(/\r?\n/).forEach(line => {
      if (!line.trim()) return;
      const m = line.match(/^\s*(\d+)\s*[:|\t]\s*(.*)$/);
      if (!m){ skipped++; return; }
      const n = +m[1] - 1, text = m[2].trim();
      if (n < 0 || n >= TOTAL){ skipped++; return; }
      if (text) cues[n] = text; else delete cues[n];
      applied++;
    });
    refresh(applied + " cue" + (applied === 1 ? "" : "s") + " set" +
      (skipped ? " · " + skipped + " line" + (skipped === 1 ? "" : "s") + " skipped (no bar number)" : ""));
  };

  $("bulkLoad").onclick = () => {
    bt.value = Object.keys(cues).map(Number).sort((a,b) => a-b)
      .map(n => (n+1) + ": " + cues[n]).join("\n");
    $("bulkMsg").textContent = "loaded — edit and Apply, or copy to keep a backup";
  };

  $("bulkClear").onclick = () => {
    if (!confirm("Delete every cue you've typed for this song? This can't be undone.")) return;
    cues = {};
    refresh("all cues cleared");
  };
}

$("song").onchange = e => loadSong(e.target.value);
$("play").onclick = toggle;
$("restart").onclick = () => {
  cursor = loopSection != null ? SONG.sections[loopSection].start : 0;
  reseek();
};
$("cueEdit").onclick = () => {
  editingCues = !editingCues;
  $("cueEdit").classList.toggle("on", editingCues);
  $("cueEdit").innerHTML = editingCues ? "&#10003; Done" : "&#9998; Cues";
  buildTimeline(); bindTimeline();
  lastDrawn = -1; paint(cursor, lastStep < 0 ? 0 : lastStep);
};
$("tempo").oninput = e => {
  const pct = +e.target.value;
  bpm = Math.round(SONG.bpm * pct / 100);
  $("tempoOut").textContent = bpm <= 0 ? "frozen · 0%" : bpm + " BPM · " + pct + "%";
};
$("capo").onchange = e => { capo = +e.target.value; };
$("sound").onchange = e => { soundMode = e.target.value; };
$("pattern").onchange = e => {
  pattern = SONG.patterns[+e.target.value];
  buildPatGrid();
  markPattern(EVENTS[cursor].chord);
  lastStep = -1;
};

document.addEventListener("keydown", e => {
  if (e.target.tagName === "SELECT" || e.target.tagName === "INPUT" || e.target.tagName === "TEXTAREA") return;
  if (e.code === "Space"){ e.preventDefault(); toggle(); }
  else if (e.key === "r" || e.key === "R"){
    cursor = loopSection != null ? SONG.sections[loopSection].start : 0; reseek();
  }
  else if (e.key === "ArrowRight"){ e.preventDefault(); cursor = (cursor+1) % TOTAL; reseek(); }
  else if (e.key === "ArrowLeft"){ e.preventDefault(); cursor = (cursor-1+TOTAL) % TOTAL; reseek(); }
  else if (e.key === "ArrowUp" || e.key === "ArrowDown"){
    e.preventDefault();
    const t = $("tempo");
    t.value = Math.min(120, Math.max(0, +t.value + (e.key === "ArrowUp" ? 5 : -5)));
    t.oninput({ target:t });
  }
});

/* ---- boot ---- */
$("song").innerHTML = Object.keys(SONGS).map(id =>
  '<option value="' + id + '">' + SONGS[id].title + " — " + SONGS[id].artist + "</option>").join("");
loadSong(Object.keys(SONGS)[0]);
requestAnimationFrame(frame);
