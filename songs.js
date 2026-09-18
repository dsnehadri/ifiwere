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
      desc:"<b>p&ndash;i&ndash;m&ndash;a&ndash;m&ndash;i</b> &mdash; counted <b>1 2 3 4 3 2</b>, climbing the four strings and coming back down. This is the pattern taught in the video lesson this arrangement comes from, where it runs unchanged through the whole song." },
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
      body:"<p>In the video lesson this arrangement comes from, every chord is played on the <b>top four strings only</b> &mdash; D, G, B and high E. The bottom two are never sounded.</p><p>That's what lets the right hand stay completely still: your <b>thumb owns the D string</b> on every chord, and <b>i&ndash;m&ndash;a</b> sit on G, B and E permanently. One finger per string, never moving. The picking is identical from the first bar to the last &mdash; all the work is in the left hand.</p>" },
    { h:"The picking pattern",
      body:"<p>Six notes per bar, up and back down: <b>p&ndash;i&ndash;m&ndash;a&ndash;m&ndash;i</b>. Counted as <b>1 2 3 4 3 2</b>, where the numbers are strings, not beats.</p><ul><li>Anchor your <b>pinky on the body</b> below the strings. It stabilises the hand so the three fingers move independently.</li><li>The thumb note is the loudest. Everything else is lighter.</li><li>Keep it perfectly even before speeding up &mdash; an uneven roll is far more noticeable than a slow one.</li></ul>" },
    { h:"Left hand",
      body:"<ul><li><b>F</b> <code>xx3211</code> and <b>G</b> <code>xx5433</code> are the <i>same shape</i> two frets apart. Learn one, slide it.</li><li><b>Am</b> <code>xx7555</code> is the only barre: index flat across G, B and E at the 5th fret, ring finger on D at the 7th.</li><li><b>Em</b> <code>xx2000</code> is one finger &mdash; index on the D string, 2nd fret.</li><li>The <b>C</b> here, <code>xx2010</code>, has E as its lowest note, so strictly it's <b>C/E</b>. That's how the lesson plays it: the thumb on the D string sounds the E, which keeps the bass line moving smoothly between chords.</li><li>Press with the <b>tips</b> of your fingers so each touches only its own string.</li></ul>" },
    { cls:"warn", h:"Where this came from",
      body:"<p>The <b>voicings and picking pattern</b> are transcribed from a video guitar lesson for this song (its transcript was supplied directly, so there's no public link), so they reflect how that teacher plays it. No other source documents the right hand; the one published chart that mentions it suggests strumming instead. The record itself also has harp and Fender Rhodes on it, so not all of the rippling texture you hear is guitar.</p><p>The <b>chord order</b> comes from a separate published transcription. It uses exactly the six chords the lesson teaches, which is good corroboration, but the two sources are independent.</p><p>The <b>3/4 timing</b> is inferred: six picked notes per chord, and 76 chords at 97 BPM comes to about <b>2:21</b> against the track's 2:15 &mdash; close, but about 6 seconds long.</p>" }
  ]
},

justlikeawoman: {
  title: "Just Like a Woman",
  artist: "Bob Dylan",
  album: "Blonde on Blonde (1966)",
  bpm: 115,
  capo: 4,
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
    Em:     { frets:[0,2,2,0,0,0], fingers:[0,2,3,0,0,0], bass:0, alt:1, sub:"" },
    Dm:     { frets:[-1,-1,0,2,3,1], fingers:[0,0,0,2,3,1], bass:2, alt:3, sub:"" },
    Am:     { frets:[-1,0,2,2,1,0], fingers:[0,0,2,3,1,0], bass:1, alt:2, sub:"" },
    E:      { frets:[0,2,2,1,0,0], fingers:[0,2,3,1,0,0], bass:0, alt:1, sub:"bridge only" }
  },
  sections: [
    { name:"Intro",    chords:"C F G C C F G C" },
    { name:"Verse 1",  chords:"C F G C C F G C F G F G F Em Dm C G7 Am C F G7", lines:[0,4,8,10,12,17] },
    { name:"Chorus 1", chords:"C Em Dm F C Em Dm F C Em Dm F G7 C", lines:[0,4,8,12] },
    { name:"Fill 1",   chords:"F C" },
    { name:"Verse 2",  chords:"C F G C C F G C F G F G F Em Dm C G7 Am C F G7", lines:[0,4,8,10,12,17] },
    { name:"Chorus 2", chords:"C Em Dm F C Em Dm F C Em Dm F G7 C", lines:[0,4,8,12] },
    { name:"Fill 2",   chords:"F C" },
    { name:"Bridge",   chords:"E E C Csus4 C E E F G7 G7", lines:[0,1,2,5,6,7,8,9] },
    { name:"Verse 3",  chords:"C F G C C F G C F G F G F Em Dm C G7 Am C F G7", lines:[0,4,8,10,12,17] },
    { name:"Chorus 3", chords:"C Em Dm F C Em Dm F C Em Dm F G7 C", lines:[0,4,8,12] },
    { name:"Fill 3",   chords:"F C" },
    { name:"Outro",    chords:"C F G C C F G C F G C" }
  ],
  patterns: [
    { name:"Pendulum (second guitar)",
      steps:[{s:2,f:"p"},{s:3,f:"i"},{s:4,f:"m"},{s:5,f:"a"},{s:4,f:"m"},{s:3,f:"i"},{s:2,f:"p"},{s:3,f:"i"}],
      desc:"An arpeggio that climbs <b>D&ndash;G&ndash;B&ndash;E</b> and falls back, on the <b>top four strings only</b>. This is the part dylanchords tabs for the record's <b>second guitarist</b>, who plays it in E with no capo; here it's moved onto the capo-4 C shapes. Dylan's own part isn't tabbed there. The thumb stays on the D string and never hunts for a bass note." },
    { name:"Alternating bass",
      steps:[{b:1,f:"p"},{s:3,f:"i"},{s:4,f:"m"},{s:5,f:"a"},{b:2,f:"p"},{s:3,f:"i"},{s:4,f:"m"},{s:5,f:"a"}],
      desc:"Fuller, for playing it on your own. The thumb takes the chord's <b>root on beat 1</b> and a <b>different bass note on beat 3</b>, so the low end moves while the fingers hold the arpeggio above it. Watch the grid &mdash; the thumb's string changes with every chord." },
    { name:"Sparse (learning)",
      steps:[{s:2,f:"p"},null,{s:4,f:"m"},null,{s:2,f:"p"},null,{s:5,f:"a"},null],
      desc:"Four notes a bar, on the beats. The turnaround at the end of each verse and chorus moves fast &mdash; <b>G7sus4&ndash;G7&ndash;G7sus2&ndash;G7</b> is four changes inside one bar &mdash; so lock the changes with this before adding the full pattern." },
    { name:"Strum",
      steps:[{strum:"d"},null,{strum:"d"},{strum:"u"},null,{strum:"u"},{strum:"d"},{strum:"u"}],
      desc:"<b>D &middot; D U &middot; U D U</b>. Not what the guitar does on the record &mdash; that part is picked &mdash; but the easiest way to get through the song while you're still learning the words." }
  ],
  notes: [
    { cls:"good", h:"Capo 4 is the whole trick",
      body:"<p>The record sounds in <b>E major</b>, which is miserable in open position. With a <b>capo at the 4th fret</b> you play ordinary <b>C shapes</b> and it comes out in E.</p><p>Every chord name here is the <i>shape you hold</i>, not the note that sounds. Hold C, hear E. Hold F, hear A. There is a second guitar on the record playing E, A and B7 shapes with no capo &mdash; that's the same harmony from the other direction.</p>" },
    { h:"Six-line verse, four-line chorus",
      body:"<p>The verse doesn't repeat as squarely as it first sounds. Lines 1 and 2 run <code>C F G C</code>, lines 3 and 4 are just <code>F G</code>, then line 5 walks down <code>F Em Dm C G7</code> and line 6 turns it around through <code>Am C F</code> into a bar of <code>G7</code>.</p><p>The chorus is <b>four</b> lines: three of <code>C Em Dm F</code>, then a fourth that lands on the same <code>G7</code> bar and resolves to <code>C</code>. After every chorus comes a <b>two-bar fill</b> before the next section.</p>" },
    { h:"Bars with a chord on every beat",
      body:"<p>Two bars in this song change chord on every beat, and the chart shows each by its first chord.</p><p><b>The G7 turnaround</b> at the end of each verse and chorus is one bar: <code>G7sus4 &rarr; G7 &rarr; G7sus2 &rarr; G7</code>, one per beat. It's a single shape &mdash; keep the low E at the 3rd fret and the high e at the 1st, and move one finger on the <b>A string</b>: 3, 2, 0, 2.</p><p><b>The fill</b> after each chorus is <code>F C F G</code>, one per beat, then a bar of <code>C</code>. The chart shows it as <code>F C</code>.</p><p>The bridge has the same trick at a slower pace: <code>C &rarr; Csus4 &rarr; C</code> is the C shape with one finger added and lifted on the D string.</p><p><b>About the names:</b> these are the labels dylanchords uses. With the open B and high e ringing, the voicings still contain the major third, so strictly the Csus4 here (<code>x33010</code>) is Cadd4, and the two G7 variants are G11 and G9. They sound right in the song; the names are kept to match the source.</p>" },
    { cls:"warn", h:"Where this came from",
      body:"<p>The <b>chords, capo, verse, chorus, bridge and fill</b> are from Eyolf &Oslash;strem's dylanchords transcription of the Blonde on Blonde version &mdash; the most careful source for Dylan there is. The <b>intro and outro are not</b>: that transcription gives neither, so they're a model built on the verse loop.</p><p>The <b>default picking</b> is the arpeggio dylanchords tabs for the record's <b>second guitarist</b>, moved onto capo-4 shapes. Dylan's own part isn't tabbed there.</p><p>The <b>bar counts are a model</b> &mdash; one chord per bar, with each turnaround and each fill's first bar counted as one bar. That comes to 140 bars, about 4:52 against the track's 4:53, but the outro was set to 11 bars to make that fit, so the match is by construction rather than evidence.</p>" }
  ]
}
,

goaway: {
  title: "Go Away",
  artist: "Strawberry Switchblade",
  album: "b-side of Trees and Flowers (1983); LP Strawberry Switchblade (1985)",
  bpm: 127,
  stepsPerBar: 8,
  beatsPerBar: 4,
  cueKey: "goaway-cues-v1",
  gridStrings: [[5,"e"],[4,"B"],[3,"G"],[2,"D"],[1,"A"],[0,"E"]],
  facts: [
    ["Key","B minor"],
    ["Capo","none &mdash; it's a barre workout"],
    ["Metre","4/4 &mdash; one chord per bar"],
    ["Tempo","127 BPM"],
    ["Feel","jangly eighth notes"],
    ["Tuning","Standard"]
  ],
  shapes: {
    G:     { frets:[3,2,0,0,0,3], fingers:[2,1,0,0,0,3], bass:0, alt:2, sub:"" },
    "F#":  { frets:[2,4,4,3,2,2], fingers:[1,3,4,2,1,1], bass:0, alt:1, barre:{fret:2,from:0,to:5}, sub:"barre" },
    Bm:    { frets:[-1,2,4,4,3,2], fingers:[0,1,3,4,2,1], bass:1, alt:2, barre:{fret:2,from:1,to:5}, sub:"barre" },
    E:     { frets:[0,2,2,1,0,0], fingers:[0,2,3,1,0,0], bass:0, alt:1, sub:"" },
    "F#m": { frets:[2,4,4,2,2,2], fingers:[1,3,4,1,1,1], bass:0, alt:1, barre:{fret:2,from:0,to:5}, sub:"barre" },
    B:     { frets:[-1,2,4,4,4,2], fingers:[0,1,2,3,4,1], bass:1, alt:2, barre:{fret:2,from:1,to:5}, sub:"barre" },
    A:     { frets:[-1,0,2,2,2,0], fingers:[0,0,1,2,3,0], bass:1, alt:2, sub:"" },
    "C#m": { frets:[-1,4,6,6,5,4], fingers:[0,1,3,4,2,1], bass:1, alt:2, barre:{fret:4,from:1,to:5}, sub:"Bm, up 2" }
  },
  sections: [
    { name:"Intro",        chords:"G F# Bm E G F# Bm E" },
    { name:"Verse 1",      chords:"G F# Bm E G F# Bm E F#m", lines:[0,2,4,6,8] },
    { name:"Pre-chorus 1", chords:"B A E F#m B A E", lines:[0,1,3,5] },
    { name:"Verse 2",      chords:"G F# Bm E G F# Bm E F#m", lines:[0,1,2,3,4,6,8] },
    { name:"Pre-chorus 2", chords:"B A E F#m B A C#m", lines:[0,1,3,5] },
    { name:"Chorus 1",     chords:"E Bm E Bm E Bm E", lines:[0,1,3,5] },
    { name:"Bridge",       chords:"G F# Bm E G F# Bm E" },
    { name:"Verse 3",      chords:"G F# Bm E G F# Bm E F#m", lines:[0,2,4,6,8] },
    { name:"Pre-chorus 3", chords:"B A E F#m B A C#m", lines:[0,1,3,5] },
    { name:"Chorus (out)", chords:"E Bm E Bm E Bm E Bm E Bm E Bm E Bm E", lines:[0,1,3,5,7,9,11,13] },
    { name:"Outro",        chords:"G F# Bm E G F# Bm E G" }
  ],
  patterns: [
    { name:"Jangle strum",
      steps:[{strum:"d"},{strum:"u"},{strum:"d"},{strum:"u"},{strum:"d"},{strum:"u"},{strum:"d"},{strum:"u"}],
      desc:"Straight eighth notes, <b>down-up all the way</b>, light and even. This is the janglepop engine &mdash; the 1983 recording is driven by strummed jangle, not picking. Keep the wrist loose; the shimmer comes from never digging in." },
    { name:"Jangle arpeggio",
      steps:[{b:1,f:"p"},{s:3,f:"i"},{s:4,f:"m"},{s:5,f:"a"},{s:4,f:"m"},{s:5,f:"a"},{s:4,f:"m"},{s:3,f:"i"}],
      desc:"A broken-chord shimmer: bass note, then the fingers circle the top three strings. Not from the record &mdash; an idiomatic way to play it quietly while keeping the eighth-note motion of the strummed original." },
    { name:"Alternating bass",
      steps:[{b:1,f:"p"},{s:3,f:"i"},{s:4,f:"m"},{s:5,f:"a"},{b:2,f:"p"},{s:3,f:"i"},{s:4,f:"m"},{s:5,f:"a"}],
      desc:"Root on beat 1, alternate bass on beat 3, fingers filling above. Watch the grid &mdash; the thumb's strings change with every chord, and on the barre chords both bass notes sit under the same finger." },
    { name:"Sparse (learning)",
      steps:[{b:1,f:"p"},null,{s:4,f:"m"},null,{b:2,f:"p"},null,{s:5,f:"a"},null],
      desc:"Four notes a bar on the beats. This song changes chords every bar and most of them are barres &mdash; drill the changes with this before adding speed. The G&rarr;F#&rarr;Bm run is the one to get smooth." }
  ],
  notes: [
    { cls:"good", h:"One shape, moved around",
      body:"<p>Five of the eight chords &mdash; <b>F#</b>, <b>F#m</b>, <b>Bm</b>, <b>B</b> and <b>C#m</b> &mdash; are barres from the same family, and <b>C#m</b> is literally the Bm shape slid up two frets.</p><p>The verse is a loop of <code>G F# Bm E</code>: open, barre, barre, open. That descent from G through F# to Bm is the hook of the harmony &mdash; practise those three changes until the barre lands without a gap.</p>" },
    { h:"Most lines start a bar early",
      body:"<p>In the chart this page follows, nearly every verse line after the first begins with a <b>pickup</b>: the words start in the bar before the chord printed over them. The cues here appear at the start of the words, so most of them come up a bar before the chord change.</p><p>Verses 1 and 3 have <b>five</b> lines, including a short one over the <code>F#m</code> at the end. Verse 2 has <b>seven</b> shorter ones. There's only one chorus before the bridge: the song goes verse, pre-chorus, verse, pre-chorus, chorus.</p><p>Also worth noticing: pre-chorus 1 ends <code>A&nbsp;E</code>, but pre-choruses 2 and 3 end <code>A&nbsp;C#m</code>. Same music, different exit.</p>" },
    { h:"Several records",
      body:"<p>The song exists as the <b>1983 b-side</b> of Trees and Flowers &mdash; jangly and guitar-driven, the one worth playing along with &mdash; and as later synthpop versions, which run 2:49, 2:59 and 3:09. Every chord chart found is of the <b>1985 studio version</b>; none covers the 1983 recording, so treat \"same chords\" as likely rather than checked.</p><p>Timing here is modelled on the album cut (127 BPM, 3:09).</p>" },
    { cls:"warn", h:"Where this came from",
      body:"<p>The <b>chords, section order and line positions</b> follow a published chord chart of the 1985 studio version (Ultimate Guitar #3694163), and the core <code>G F# Bm E</code> loop is corroborated by independent audio chord-detection. A second chart that looked like extra corroboration turned out to be a copy of the first, so that's two independent sources, not three.</p><p>The cue positions are <b>adjusted for pickups</b>, which depends on how the chart lines chords up over the words. That alignment is loose, so treat individual cues as approximate.</p><p>The <b>bar counts are a model</b> &mdash; one chord per bar, with the intro and the bridge each played twice where the chart writes them once, as the audio chord-detection shows. That's 95 bars, about 2:59 against the album's 3:09, so something is probably still missing, most likely a repeat.</p><p><b>No reliable source documents the right hand.</b> The only rhythm-notated tab is an unvetted user upload. The 1983 record is strummed jangle; the strum pattern is closest to it, and the picking patterns are idiomatic alternatives, not transcriptions.</p>" }
  ]
}

,

myfavouritegame: {
  title: "My Favourite Game",
  artist: "The Cardigans",
  album: "Gran Turismo (1998)",
  bpm: 143,
  stepsPerBar: 8,
  beatsPerBar: 4,
  capo: 1,
  cueKey: "myfavouritegame-cues-v1",
  gridStrings: [[5,"e"],[4,"B"],[3,"G"],[2,"D"],[1,"A"],[0,"E"]],
  facts: [
    ["Sounding key","C minor"],
    ["Capo","1st fret &mdash; Bm shapes"],
    ["Metre","4/4 &mdash; one chord per bar"],
    ["Tempo","143 BPM"],
    ["Feel","driving eighth notes"],
    ["Tuning","Standard"]
  ],
  shapes: {
    Bm:    { frets:[-1,2,4,4,3,2], fingers:[0,1,3,4,2,1], bass:1, alt:2, barre:{fret:2,from:1,to:5}, sub:"barre" },
    A:     { frets:[-1,0,2,2,2,0], fingers:[0,0,1,2,3,0], bass:1, alt:2, sub:"" },
    E:     { frets:[0,2,2,1,0,0], fingers:[0,2,3,1,0,0], bass:0, alt:1, sub:"" },
    G:     { frets:[3,2,0,0,0,3], fingers:[2,1,0,0,0,3], bass:0, alt:2, sub:"" },
    "F#":  { frets:[2,4,4,3,2,2], fingers:[1,3,4,2,1,1], bass:0, alt:1, barre:{fret:2,from:0,to:5}, sub:"barre" },
    "F#5": { frets:[2,4,4,-1,-1,-1], fingers:[1,3,4,0,0,0], bass:0, alt:1, sub:"power chord" },
    "F#7": { frets:[2,4,2,3,2,2], fingers:[1,3,1,2,1,1], bass:0, alt:1, barre:{fret:2,from:0,to:5}, sub:"barre" },
    Cmaj7: { frets:[-1,3,2,0,0,0], fingers:[0,3,2,0,0,0], bass:1, alt:2, sub:"open" }
  },
  sections: [
    { name:"Intro",     chords:"Bm G E A F#7 Bm A E G Bm A E G" },
    { name:"Verse 1",   chords:"Bm A E G Bm A E G Bm A E G", lines:[0,2,4,6] },
    { name:"Verse 2",   chords:"Bm A E G Bm A E G", lines:[0,2,4,6] },
    { name:"Chorus 1",  chords:"Bm G A F#5 Bm G A F#5 Bm G E A F#", lines:[0,4,8,10] },
    { name:"Interlude", chords:"Bm A E G Bm A E G" },
    { name:"Verse 3",   chords:"Bm A E G Bm A E G Bm A E G", lines:[0,2,4,6] },
    { name:"Verse 4",   chords:"Bm A E G Bm A E G", lines:[0,2,4,6] },
    { name:"Chorus 2",  chords:"Bm G A F#5 Bm G A F#5 Bm G A F#5 Bm G A F#5 Bm G E A F# F#", lines:[0,4,8,12,16,18] },
    { name:"Link",      chords:"Bm A E G" },
    { name:"Bridge",    chords:"Bm Cmaj7 Bm Cmaj7 Bm Cmaj7 Bm Cmaj7 Bm Cmaj7 Bm Cmaj7 Bm G E A F#", lines:[0,4,8,12,14] },
    { name:"Outro",     chords:"Bm A E G Bm A E G E G E G" }
  ],
  patterns: [
    { name:"Eighth-note drive (per Songsterr)",
      steps:[{strum:"d"},{strum:"u"},{strum:"d"},{strum:"u"},{strum:"d"},{strum:"u"},{strum:"d"},{strum:"u"}],
      desc:"<b>Down-up on every eighth, all bar long.</b> This is how the Songsterr transcription notates the rhythm guitar: it never breaks the eighth-note grid from the first bar to the last. That is one transcriber's reading &mdash; two other charts show some intro and chorus chords simply left to ring. In that transcription a shifting handful of the <i>upstrokes</i> are <b>ghosted</b>: the fretting hand relaxes just enough to deaden them, so they land as a click rather than a chord. Which ones changes bar to bar, so don't drill a fixed map &mdash; keep the arm swinging evenly and let the left hand decide how much rings." },
    { name:"Bridge quarters (per Songsterr)",
      steps:[{strum:"d"},null,{strum:"d"},null,{strum:"d"},null,{strum:"d"},null],
      desc:"<b>Four downstrokes, one per beat.</b> From the same transcription, and not confirmed by any other source: the bridge drops out of eighths into plain quarter-note chords, which is what makes it feel like the song has pulled over. Doubles as the learning pattern &mdash; the changes here come every bar at 143 BPM, so lock them with this before putting the eighths back." },
    { name:"Alternating bass (idiomatic)",
      steps:[{b:1,f:"p"},{s:3,f:"i"},{s:4,f:"m"},{s:5,f:"a"},{b:2,f:"p"},{s:3,f:"i"},{s:4,f:"m"},{s:5,f:"a"}],
      desc:"Root on beat 1, fifth on beat 3, fingers filling above. <b>Not on the record</b> &mdash; this is an electric rock track and nobody fingerpicks it. It's here for playing the song unplugged on your own. Watch the grid: the thumb's string moves between the low E and the A depending on the chord." },
    { name:"Arpeggio (idiomatic)",
      steps:[{b:1,f:"p"},{s:3,f:"i"},{s:4,f:"m"},{s:5,f:"a"},{s:4,f:"m"},{s:5,f:"a"},{s:4,f:"m"},{s:3,f:"i"}],
      desc:"Bass note, then the fingers circle the top three strings, keeping the eighth-note motion of the strummed original. <b>Also not on the record</b> &mdash; an idiomatic way to practise the changes quietly. On <b>F#5</b> there is no top end to circle, so it folds down onto the three strings that shape actually has." }
  ],
  notes: [
    { cls:"good", h:"Two loops, and that's nearly the whole song",
      body:"<p>Almost everything here is built from two four-bar loops. The verse is <code>Bm A E G</code>. The chorus is <code>Bm G A F#5</code> &mdash; the same chords in a different order, with the F# as a power chord.</p><p>The <b>bridge</b> is where it leaves home: it rocks between <code>Bm</code> and <code>Cmaj7</code> a bar at a time, then a last <code>Bm G</code> and the <code>E A F#</code> lead-back. Cmaj7 is the one chord in the song that isn't in the key, and it's what makes the bridge feel suspended.</p><p>Only three shapes are full barres: Bm, F# and F#7 (the intro's version of F#). A, E, G and Cmaj7 are open chords. Get the <code>Bm&rarr;A</code> change clean and the rest follows.</p>" },
    { h:"Capo 1: what you hold isn't what you hear",
      body:"<p>The record sounds in <b>C minor</b>. Played open that means Cm, Bb, F, Ab and G &mdash; barres all the way down. Put a <b>capo at the 1st fret</b> and the same music comes out of ordinary shapes.</p><p>Every chord name on this page is the <b>shape you hold</b>, not the note that sounds:</p><ul><li>Hold <b>Bm</b>, hear <b>Cm</b> &mdash; the home chord</li><li>Hold <b>A</b>, hear <b>Bb</b></li><li>Hold <b>E</b>, hear <b>F</b></li><li>Hold <b>G</b>, hear <b>Ab</b></li><li>Hold <b>F#</b>, hear <b>G</b> &mdash; the dominant</li><li>Hold <b>Cmaj7</b>, hear <b>Dbmaj7</b> &mdash; the bridge's outside chord</li></ul><p>The <b>E</b> shape is the interesting one in the loops: a major IV chord in a minor key, which is where a lot of the song's lift comes from.</p>" },
    { h:"The push, and what the grid can't show",
      body:"<p>A few things the one-chord-per-bar grid flattens out.</p><p><b>Almost every chord arrives early.</b> On the record the next chord is struck on the <i>and of beat 4</i>, an eighth note before its bar. That anticipation is most of what makes the track drive. The grid changes chord on the downbeat; you should change a hair before it.</p><p><b>The fourth bar of each loop has two chords.</b> In the verse, the <code>G</code> holds for about half the bar and then moves to <code>A</code> &mdash; sounding Ab walking up through Bb back to Cm. In the chorus, the <code>F#5</code> holds two beats and then moves to <code>A</code> on beat 3. This page names each bar by its downbeat chord, which is what the published chord charts do too, but if you want it to sound right, make that second change halfway through.</p><p><b>Some chorus bars sit over a held bass note.</b> Under several of the <code>G</code> and <code>A</code> bars the bass stays on its low note, so on the record they sound as A&flat;/C and B&flat;/C rather than plain chords. The shapes you hold don't change.</p><p>One more: the <b>last four bars of Verse 1 and Verse 3 are the instrumental riff</b>, not sung. That's why the cue slots stop before those sections end.</p>" },
    { cls:"warn", h:"Where this came from",
      body:"<p>The <b>chords, capo, section order and bar count</b> are read off the Songsterr transcription of the album version, one bar at a time from the Rhythm part (electric guitar, clean, capo 1) &mdash; only which chord sounds in each bar, not the tab. The main shapes (<b>Bm A E G F#</b> at capo 1) match an independent published chord chart.</p><p>Two places were corrected using the bass and organ parts of the same transcription, and each is backed by a published chart: the bridge's <code>Cmaj7</code> bars, where the bass moves to Db, and the last four outro bars, which cycle <code>E G</code>. The intro's F# is <code>F#7</code> in the organ and in one chart. The other F# bars carry the same 7th in the organ, but the guitar plays a plain F#, so they're left as F#.</p><p>The <b>tempo is 143 BPM</b>: four sources say 143, and only the transcription's own tempo marking says 144. At 143, the 129 bars come to 3:36, against the track's 3:37&ndash;3:38.</p><p>The <b>cue slots</b> follow two published chord charts that print the vocal lines against the chords: a line every two bars in the verses, one per four-bar loop in the choruses and bridge, 31 in all. The charts disagree only at the end of the second chorus, where one splits a line in two; this page follows the split.</p><p>The <b>strumming</b> comes from the Songsterr transcription alone: unbroken eighth notes with some upstrokes muted, and quarter notes in the bridge. No other source confirms that detail, and two charts show some intro and chorus chords simply left to ring. There's no fingerpicking on this record; the alternating-bass and arpeggio patterns are idiomatic alternatives for practising.</p>" }
  ]
}

};
