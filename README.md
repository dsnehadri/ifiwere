# If I Were — Guitar Karaoke

A single-page, play-along chord and fingerpicking trainer for **"If I Were"** by Vashti Bunyan
(*Lookaftering*, 2005).

Open the page, hit play, and it walks through the song in time: the current chord in large
type, the chord diagram, the next two chords, and an animated right-hand pattern showing
exactly which string each finger plucks on each beat.

## The trick to this song

Every chord is played on the **top four strings only** — D, G, B and high E. The bottom two
are never sounded.

That's what makes it approachable: the right hand never moves. The **thumb owns the D string**
on every chord, and **i–m–a** sit permanently on G, B and E. The picking pattern is identical
from the first bar to the last, so all the work is in the left hand.

The pattern is **`p–i–m–a–m–i`** — counted *1 2 3 4 3 2*, climbing the four strings and coming
back down. Six notes per bar, in 3/4.

| Chord | Shape | Note |
|---|---|---|
| `Dm` | `xx0231` | standard open Dm |
| `Em` | `xx2000` | one finger — index on D string, 2nd fret |
| `C`  | `xx2010` | |
| `F`  | `xx3211` | movable shape |
| `G`  | `xx5433` | the F shape, up two frets |
| `Am` | `xx7555` | index barred across G/B/E at the 5th |

## Features

- **Timed chord scroller** — the full chart scrolls and highlights in time, at 97 BPM.
- **Audio play-along** — a synthesised plucked guitar plays the pattern, with an optional
  metronome click. No audio files, no external requests; everything is Web Audio.
- **Chord diagrams** — SVG, with finger numbers and barre rendering, drawn from a shape table.
- **Animated picking grid** — four string rows, six columns, showing which finger plucks
  which string on each note of the bar.
- **Four right-hand patterns** — the lesson pattern plus a reverse roll, a sparse practice
  version, and a pinched-downbeat variant.
- **Editable cues with built-in alignment** — hit `✎ Cues`, paste the two verses one line
  per line, and press **Align lines**. The 14 sung lines drop onto the 14 bars where the
  singing starts. Each holds on screen until the next begins. Saved to your browser's local
  storage only; nothing is uploaded or committed.
- **Tempo control** — 40–120% of the original tempo.
- **Section looping** — loop the intro, either verse, or the outro while you drill it.
- **Capo 0–7** — shapes stay the same, sounding pitch moves, so you can find your own
  vocal range.

Keyboard: <kbd>Space</kbd> play/pause, <kbd>R</kbd> restart, <kbd>←</kbd>/<kbd>→</kbd> step a
chord, <kbd>↑</kbd>/<kbd>↓</kbd> tempo.

## The song

| | |
|---|---|
| Key | C major (D minor feel) |
| Tempo | 97 BPM |
| Metre | 3/4, one chord per bar |
| Tuning | Standard, EADGBE |
| Chords | Dm, C, Em, F, G, Am |
| Length | 2:15 |

Every chord is diatonic to C major — no key changes, and only six shapes in the whole song.

## Accuracy

Which parts are sourced and which are inferred:

- **The voicings and the picking pattern** are transcribed from a guitar lesson for this song,
  so they reflect how someone actually plays it rather than a reconstruction. All six voicings
  were checked to spell the chord they're named after.
- **The chord order** comes from a separate published transcription. It uses exactly the six
  chords the lesson teaches, which is decent corroboration, but the two sources are
  independent and the order is the least verified part here.
- **The 3/4 metre is inferred**, not stated by either source: six picked notes per chord, and
  76 chords at 97 BPM comes to ~141s against the track's 2:15. Close enough to be convincing,
  not close enough to be proof. Use `Bars/chord` if a section drifts against the record.

Treat it as a practice scaffold rather than an authoritative transcription.

## Running it

It's one self-contained `index.html` with no dependencies or build step.

```sh
python3 -m http.server 8000   # then open http://localhost:8000
```

Or just open `index.html` in a browser. Browsers require a user gesture before audio starts,
so press **Play** rather than expecting sound on load.

## Note on lyrics

No lyrics are reproduced here, and none are committed to this repo.

What *is* committed is the **alignment map** — a 14-entry list of which bars carry a sung
line, derived from the song's structure. That's timing information, and it's what lets
`Align lines` place pasted text correctly without the page ever knowing what the text says.
Paste your own words and they live in your browser's local storage and go no further.

"If I Were" was written and recorded by Vashti Bunyan; chord progressions, voicings and song
structure are factual musical information, presented for study and practice. Please support
the artist by buying *Lookaftering*.
