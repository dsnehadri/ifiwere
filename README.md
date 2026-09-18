# Guitar Karaoke

A single self-contained page that walks you through a song in time: the current chord in
large type, its diagram, the next two chords, and an animated right-hand pattern showing
exactly which string each finger plucks on each beat.

**Live: https://dsnehadri.github.io/ifiwere/**

Four songs so far, picked from the selector at the top:

| Song | Artist | Key | Metre | Tempo |
|---|---|---|---|---|
| If I Were | Vashti Bunyan | C major | 3/4 | 97 BPM |
| Just Like a Woman | Bob Dylan | E major (capo 4, C shapes) | 4/4 | 115 BPM |
| Go Away | Strawberry Switchblade | B minor | 4/4 | 127 BPM |
| My Favourite Game | The Cardigans | C minor (capo 1, Bm shapes) | 4/4 | 143 BPM |

## Features

- **Timed chord chart** — the whole song is shown at once and highlights in time.
- **Audio play-along** — a synthesised plucked guitar plays the pattern, with an optional
  metronome click. No audio files; everything is Web Audio. The page's only external request
  is the Comic Neue font from Google Fonts.
- **Chord diagrams** — SVG, with finger numbers, barre rendering and position markers.
- **Animated picking grid** — string rows against the beats of the bar, showing which finger
  plucks what. The thumb's string is re-marked per chord, so alternating-bass patterns show
  the correct bass note for the chord you're actually on.
- **Multiple right-hand patterns per song**, plus a sparse "learning" pattern for locking
  the changes in before adding the full roll.
- **Editable cues with built-in alignment** — see below.
- **Tempo 0–120%** (0 freezes on the current bar), **capo 0–7**, and **per-section looping**.

Keyboard: <kbd>Space</kbd> play/pause, <kbd>R</kbd> restart, <kbd>←</kbd>/<kbd>→</kbd> step a
chord, <kbd>↑</kbd>/<kbd>↓</kbd> tempo.

## Cues, and the note on lyrics

**The page's code and song data contain no lyrics.** Lyric files the site's owner adds under
`lyrics/` are a separate matter: they are committed and published with the site, by
deliberate choice (see `.gitignore`).

What *is* committed is the **alignment map** — per song, a list of which bars carry a sung
line. That's timing information derived from song structure, and it's what lets the page
place your text correctly without ever containing it.

Press `✎ Cues`, paste the sung lines one per line, press **Align lines**, and they drop onto
those bars. Each cue holds on screen until the next begins. `Apply numbered` (`bar: text`)
gives per-bar control, `Load current` round-trips for backup, `Clear all` wipes. Everything
lives in your browser's local storage, keyed per song — nothing is uploaded, and clearing
browser data clears it.

### Pasting them from a file instead

Each song has a template in [`lyrics/`](lyrics/). Copy `lyrics/<song>.template.txt` to
`lyrics/<song>.txt`, paste the sung lines in one per line, save, reload. The page picks the
file up automatically and it overrides anything stored in the browser.

The template lists which bars each line lands on, and you can pin a line to an exact bar with
`37: some line` if the sequential fill puts one in the wrong place.

Two things to know:

- **`lyrics/*.txt` files are tracked and published.** Anything you save there and commit goes
  to the public Pages site. To keep a song's lyrics on your machine only, add that file to
  `.gitignore` before committing.
- **It needs a local web server.** Browsers block `fetch()` on `file://` URLs, so open it via
  `python3 -m http.server 8000`, not by double-clicking `index.html`.

Chord progressions, voicings and structure are factual musical information presented for
study and practice. Please support these artists by buying their records.

## Accuracy

Different parts of this rest on very different evidence. Per song:

**If I Were** — the voicings and picking pattern are transcribed from a video guitar lesson
whose transcript was supplied directly, so there's no public link. All chords sit on the top
four strings, thumb fixed on the D string, `p–i–m–a–m–i` throughout. No other source documents
the right hand; the one published chart that mentions it suggests strumming. The chord order
comes from a single published transcription (a second site that seemed to agree is a copy of
it). The 3/4 reading is inferred: 76 bars at 97 BPM is 2:21 against the track's 2:15, about
6 seconds long. One open question: two charts give the second chord of each verse line as `Am`,
while an automatic chord detector hears `Em`; this page keeps `Am`.

**Just Like a Woman** — the chords, capo, verse, chorus, bridge and the fill after each chorus
come from Eyolf Østrem's
[dylanchords](https://www.dylanchords.com/07_bob/just_like_a_woman) transcription of the
Blonde on Blonde version. The intro and outro are **not** from it — it gives neither — so
they're modelled on the verse loop. The default picking is the arpeggio dylanchords tabs for
the record's **second guitarist**, moved onto capo-4 shapes. The verse is six lines and the
chorus four; both end on a single bar of `G7` in which the chord changes on every beat
(`G7sus4 G7 G7sus2 G7`), and the chart shows that bar as one `G7`. Bar counts are
one-chord-per-bar: 140 bars ≈ 4:52 against the track's 4:53, but the outro was set to 11
bars to reach that, so the fit is by construction.

An earlier version of this entry got the chorus wrong (three lines, with the turnaround
counted as four bars); the two errors cancelled and hid each other in the runtime check.

**Go Away** — the chords, section order and line positions follow a published chord chart of
the 1985 studio version (Ultimate Guitar #3694163); the core `G F# Bm E` loop is corroborated by
independent audio chord-detection. A third chart turned out to be a copy of the first, so that's
two independent sources. There is one chorus before the bridge, not two, and the verses have
five, seven and five lines. Cues are placed at the start of the words, which in this song is
usually a bar before the chord (a pickup); that depends on loose chord-over-word alignment in
the chart, so treat single cues as approximate. The bars are one-chord-per-bar with the intro
and bridge each played twice, as the audio shows: 95 bars ≈ 2:59 against the album's 3:09, so
a repeat is probably still missing. **No reliable source documents the right hand** — the
1983 b-side is strummed jangle, so the strum pattern is closest to the record and the picking
patterns are idiomatic alternatives. Note the C#m: pre-choruses 2 and 3 end `A C#m` where
pre-chorus 1 ends `A E`.

**My Favourite Game** — the chords, capo, section order and bar count were read bar by bar
off the Songsterr transcription of the album version, from the Rhythm part (electric guitar,
clean, capo 1); the main shapes — `Bm A E G F#` at capo 1 — match an independent published
chart. The bridge's `Cmaj7` bars and the outro's closing `E G E G` were corrected from the
transcription's bass and organ parts, and both are backed by published charts. Tempo is
**143 BPM** (four sources; the transcription's marking says 144): 129 bars ≈ 3:36 against
the track's 3:37–3:38. The 31 cue slots follow two published charts that print the vocal
against the chords. The strumming — unbroken eighths with some upstrokes muted, quarter notes
in the bridge — comes from that one transcription only, and two charts show some chords left
to ring instead. There is no fingerpicking on this record, so the arpeggio and alternating-bass
patterns are idiomatic alternatives. The one-chord-per-bar grid names each bar by its
**downbeat** chord: the fourth bar of each loop really has two chords, several chorus bars sit
over a held bass note, and nearly every chord is pushed an eighth early.

Treat all of these as practice scaffolds rather than authoritative transcriptions.

## Layout

| File | What's in it |
|---|---|
| `index.html` | Page shell and stylesheet |
| `songs.js` | All song data — shapes, sections, patterns, notes, alignment maps |
| `app.js` | The engine; knows nothing about any particular song |
| `lyrics/` | Per-song cue templates, plus any filled-in `<song>.txt` files (tracked and published) |

Adding a song means adding one entry to `SONGS` in `songs.js`. Nothing else needs touching.

## Running it

No dependencies, no build step.

```sh
python3 -m http.server 8000   # then open http://localhost:8000
```

Browsers need a user gesture before audio starts, so press **Play** rather than expecting
sound on load.
