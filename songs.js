/* ============================================================
   Song data.  Strings are indexed 0..5 = low E, A, D, G, B, high E.
   fret -1 = muted, 0 = open.  bass/alt are string indices for the
   thumb.  A section with a `lines` array carries sung lines starting
   at those bar offsets -- that is timing only, never lyric text.
   ============================================================ */
const OPEN_MIDI = [40, 45, 50, 55, 59, 64];

const SONGS = {

ifiwere: {
  title: "If I Were",
  artist: "Vashti Bunyan",
  album: "Lookaftering (2005)",
  bpm: 97,
  stepsPerBar: 6,
  beatsPerBar: 3,
  cueKey: "ifiwere-cues-v1",
  gridStrings: [[5,"e"],[4,"B"],[3,"G"],[2,"D"]],
  facts: [
    ["Key","C major / D minor feel"],
    ["Metre","3/4 &mdash; one chord per bar"],
    ["Tempo","97 BPM"],
    ["Strings","top four only &mdash; D G B E"],
    ["Pattern","p&ndash;i&ndash;m&ndash;a&ndash;m&ndash;i"],
    ["Tuning","Standard"]
  ],
  shapes: {
    Dm: { frets:[-1,-1,0,2,3,1], fingers:[0,0,0,2,3,1], bass:2, sub:"open" },
    Em: { frets:[-1,-1,2,0,0,0], fingers:[0,0,1,0,0,0], bass:2, sub:"one finger" },
    C:  { frets:[-1,-1,2,0,1,0], fingers:[0,0,2,0,1,0], bass:2, sub:"" },
    F:  { frets:[-1,-1,3,2,1,1], fingers:[0,0,3,2,1,1], bass:2, barre:{fret:1,from:4,to:5}, sub:"movable" },
    G:  { frets:[-1,-1,5,4,3,3], fingers:[0,0,3,2,1,1], bass:2, barre:{fret:3,from:4,to:5}, sub:"F, up 2" },
    Am: { frets:[-1,-1,7,5,5,5], fingers:[0,0,3,1,1,1], bass:2, barre:{fret:5,from:3,to:5}, sub:"barre" }
  },
  sections: [
    { name:"Intro",   chords:"Dm C Dm C Dm Em Dm Em F G F G Dm Em Dm Em F G F C" },
    { name:"Verse 1", chords:"Dm Am Dm C F G F G Dm Am Dm C F G Am C", lines:[0,2,6,8,10,12,14] },
    { name:"Verse 2", chords:"Dm Am Dm C F G F G Dm Am Dm C F G Am C", lines:[0,2,6,8,10,12,14] },
    { name:"Outro",   chords:"Dm Em Dm C F G F G Dm Em Dm C F G Am G Dm Em Dm C F G F G" }
  ],
  patterns: [
    { name:"Lesson pattern",
      steps:[{s:2,f:"p"},{s:3,f:"i"},{s:4,f:"m"},{s:5,f:"a"},{s:4,f:"m"},{s:3,f:"i"}],
      desc:"<b>p&ndash;i&ndash;m&ndash;a&ndash;m&ndash;i</b> &mdash; counted <b>1 2 3 4 3 2</b>, climbing the four strings and coming back down. This is the pattern the song is played with, and it never changes for the whole piece." },
    { name:"Reverse roll",
      steps:[{s:2,f:"p"},{s:5,f:"a"},{s:4,f:"m"},{s:3,f:"i"},{s:4,f:"m"},{s:5,f:"a"}],
      desc:"<b>p&ndash;a&ndash;m&ndash;i&ndash;m&ndash;a</b>. The top note arrives immediately after the bass instead of in the middle of the bar. A variation &mdash; useful for contrast on a repeat, but the lesson pattern is the one to learn first." },
    { name:"Sparse (learning)",
      steps:[{s:2,f:"p"},null,{s:4,f:"m"},null,{s:5,f:"a"},null],
      desc:"Three notes instead of six, on the beats of the bar. Use this to lock the left-hand changes in time before adding the full roll back. Not how the record sounds &mdash; a scaffold only." },
    { name:"Pinched downbeat",
      steps:[{s:2,f:"p",pinch:5},{s:3,f:"i"},{s:4,f:"m"},{s:5,f:"a"},{s:4,f:"m"},{s:3,f:"i"}],
      desc:"The lesson pattern with thumb and <b>a</b> striking <b>together</b> on beat one. Marks each chord change more clearly &mdash; handy when practising changes, or playing without accompaniment." }
  ],
  notes: [
    { cls:"good", h:"The one thing that makes this song click",
      body:"<p>Every chord is played on the <b>top four strings only</b> &mdash; D, G, B and high E. The bottom two are never sounded.</p><p>That's what lets the right hand stay completely still: your <b>thumb owns the D string</b> on every chord, and <b>i&ndash;m&ndash;a</b> sit on G, B and E permanently. One finger per string, never moving. The picking is identical from the first bar to the last &mdash; all the work is in the left hand.</p>" },
    { h:"The picking pattern",
      body:"<p>Six notes per bar, up and back down: <b>p&ndash;i&ndash;m&ndash;a&ndash;m&ndash;i</b>. Counted as <b>1 2 3 4 3 2</b>, where the numbers are strings, not beats.</p><ul><li>Anchor your <b>pinky on the body</b> below the strings. It stabilises the hand so the three fingers move independently.</li><li>The thumb note is the loudest. Everything else is lighter.</li><li>Keep it perfectly even before speeding up &mdash; an uneven roll is far more noticeable than a slow one.</li></ul>" },
    { h:"Left hand",
      body:"<ul><li><b>F</b> <code>xx3211</code> and <b>G</b> <code>xx5433</code> are the <i>same shape</i> two frets apart. Learn one, slide it.</li><li><b>Am</b> <code>xx7555</code> is the only barre: index flat across G, B and E at the 5th fret, ring finger on D at the 7th.</li><li><b>Em</b> <code>xx2000</code> is one finger &mdash; index on the D string, 2nd fret.</li><li>Press with the <b>tips</b> of your fingers so each touches only its own string.</li></ul>" },
    { cls:"warn", h:"Where this came from",
      body:"<p>The <b>voicings and picking pattern</b> are transcribed from a guitar lesson for this song, so the right hand and the four-string shapes reflect how it's actually played.</p><p>The <b>chord order</b> comes from a separate published transcription. It uses exactly the six chords the lesson teaches, which is good corroboration, but the two sources are independent.</p><p>The <b>3/4 timing</b> is inferred: six picked notes per chord, and 76 chords at 97 BPM lands within a few seconds of the track's 2:15.</p>" }
  ]
},

justlikeawoman: {
  title: "Just Like a Woman",
  artist: "Bob Dylan",
  album: "Blonde on Blonde (1966)",
  bpm: 115,
  stepsPerBar: 8,
  beatsPerBar: 4,
  cueKey: "justlikeawoman-cues-v1",
  gridStrings: [[5,"e"],[4,"B"],[3,"G"],[2,"D"],[1,"A"],[0,"E"]],
  facts: [
    ["Sounding key","E major"],
    ["Capo","4th fret &mdash; C shapes"],
    ["Metre","4/4 &mdash; one chord per bar"],
    ["Tempo","115 BPM"],
    ["Pattern","pendulum arpeggio"],
    ["Tuning","Standard"]
  ],
  shapes: {
    C:      { frets:[-1,3,2,0,1,0], fingers:[0,3,2,0,1,0], bass:1, alt:2, sub:"" },
    Csus4:  { frets:[-1,3,3,0,1,0], fingers:[0,3,4,0,1,0], bass:1, alt:2, sub:"add a finger" },
    F:      { frets:[1,3,3,2,1,1], fingers:[1,3,4,2,1,1], bass:0, alt:1, barre:{fret:1,from:0,to:5}, sub:"barre" },
    G:      { frets:[3,2,0,0,0,3], fingers:[2,1,0,0,0,3], bass:0, alt:2, sub:"" },
    G7:     { frets:[3,2,0,0,0,1], fingers:[3,2,0,0,0,1], bass:0, alt:2, sub:"turnaround" },
    G7sus4: { frets:[3,3,0,0,0,1], fingers:[2,3,0,0,0,1], bass:0, alt:2, sub:"A string 3" },
    G7sus2: { frets:[3,0,0,0,0,1], fingers:[2,0,0,0,0,1], bass:0, alt:2, sub:"A string open" },
    Em:     { frets:[0,2,2,0,0,0], fingers:[0,2,3,0,0,0], bass:0, alt:1, sub:"" },
    Dm:     { frets:[-1,-1,0,2,3,1], fingers:[0,0,0,2,3,1], bass:2, alt:3, sub:"" },
    Am:     { frets:[-1,0,2,2,1,0], fingers:[0,0,2,3,1,0], bass:1, alt:2, sub:"" },
    E:      { frets:[0,2,2,1,0,0], fingers:[0,2,3,1,0,0], bass:0, alt:1, sub:"bridge only" }
  },
  sections: [
    { name:"Intro",    chords:"C F G C C F G C" },
    { name:"Verse 1",  chords:"C F G C C F G C F G F G F Em Dm C G7 Am C F G7sus4 G7 G7sus2 G7", lines:[0,4,8,10,12,17] },
    { name:"Chorus 1", chords:"C Em Dm F C Em Dm F C Em Dm F", lines:[0,4,8] },
    { name:"Verse 2",  chords:"C F G C C F G C F G F G F Em Dm C G7 Am C F G7sus4 G7 G7sus2 G7", lines:[0,4,8,10,12,17] },
    { name:"Chorus 2", chords:"C Em Dm F C Em Dm F C Em Dm F", lines:[0,4,8] },
    { name:"Bridge",   chords:"E C Csus4 C E F G7sus4 G7 G7sus2 G7 G7sus4 G7 G7sus2 G7", lines:[0,1,4,5,6,10] },
    { name:"Verse 3",  chords:"C F G C C F G C F G F G F Em Dm C G7 Am C F G7sus4 G7 G7sus2 G7", lines:[0,4,8,10,12,17] },
    { name:"Chorus 3", chords:"C Em Dm F C Em Dm F C Em Dm F", lines:[0,4,8] },
    { name:"Outro",    chords:"C F G C C F G C" }
  ],
  patterns: [
    { name:"Pendulum (as recorded)",
      steps:[{s:2,f:"p"},{s:3,f:"i"},{s:4,f:"m"},{s:5,f:"a"},{s:4,f:"m"},{s:3,f:"i"},{s:2,f:"p"},{s:3,f:"i"}],
      desc:"The pattern in the tabbed part of the record: an arpeggio that climbs <b>D&ndash;G&ndash;B&ndash;E</b> and falls back, on the <b>top four strings only</b>. Same pendulum shape as a lot of Dylan's picking &mdash; the thumb stays on the D string and never hunts for a bass note." },
    { name:"Alternating bass",
      steps:[{b:1,f:"p"},{s:3,f:"i"},{s:4,f:"m"},{s:5,f:"a"},{b:2,f:"p"},{s:3,f:"i"},{s:4,f:"m"},{s:5,f:"a"}],
      desc:"Fuller, for playing it on your own. The thumb takes the chord's <b>root on beat 1</b> and a <b>different bass note on beat 3</b>, so the low end moves while the fingers hold the arpeggio above it. Watch the grid &mdash; the thumb's string changes with every chord." },
    { name:"Sparse (learning)",
      steps:[{s:2,f:"p"},null,{s:4,f:"m"},null,{s:2,f:"p"},null,{s:5,f:"a"},null],
      desc:"Four notes a bar, on the beats. The verse turnaround moves fast &mdash; <b>G7sus4&ndash;G7&ndash;G7sus2&ndash;G7</b> is four chords in four bars &mdash; so lock the changes with this before adding the full pattern." },
    { name:"Strum",
      steps:[{strum:"d"},null,{strum:"d"},{strum:"u"},null,{strum:"u"},{strum:"d"},{strum:"u"}],
      desc:"<b>D &middot; D U &middot; U D U</b>. Not what the guitar does on the record &mdash; that part is picked &mdash; but the easiest way to get through the song while you're still learning the words." }
  ],
  notes: [
    { cls:"good", h:"Capo 4 is the whole trick",
      body:"<p>The record sounds in <b>E major</b>, which is miserable in open position. With a <b>capo at the 4th fret</b> you play ordinary <b>C shapes</b> and it comes out in E.</p><p>Every chord name here is the <i>shape you hold</i>, not the note that sounds. Hold C, hear E. Hold F, hear A. There is a second guitar on the record playing E, A and B7 shapes with no capo &mdash; that's the same harmony from the other direction.</p>" },
    { h:"The verse is six lines, not four",
      body:"<p>It doesn't repeat as squarely as it first sounds. Lines 1 and 2 run <code>C F G C</code>, lines 3 and 4 are just <code>F G</code>, then line 5 walks down <code>F Em Dm C G7</code> and line 6 turns it around through <code>Am C F</code>.</p><p>The chorus is only <b>three</b> lines of <code>C Em Dm F</code>. The <code>G7</code> turnaround people expect at the end of the chorus is actually the end of the <i>verse</i>.</p>" },
    { h:"The G7 turnaround",
      body:"<p><code>G7sus4 &rarr; G7 &rarr; G7sus2 &rarr; G7</code> looks like four chord changes. It's one shape: keep the low E at the 3rd fret and the high E at the 1st, and move a single finger on the <b>A string</b> &mdash; 3, 2, 0, 2.</p><p>Same idea in the bridge with <code>C &rarr; Csus4 &rarr; C</code>: hold the C and add or lift one finger on the D string.</p>" },
    { cls:"warn", h:"Where this came from",
      body:"<p>The <b>chords, capo and section order</b> are from Eyolf &Oslash;strem's dylanchords transcription of the Blonde on Blonde version &mdash; the most careful source for Dylan there is. The <b>picking</b> follows the arpeggio tabbed there for the record.</p><p>The <b>bar counts are still my model.</b> The transcription gives chord order and line breaks but not bar-exact durations; this page puts one chord in each bar. That comes to 138 bars, about 4:48 against the track's 4:52 &mdash; a good fit, but not proof.</p>" }
  ]
}

};
