# If I Were — Guitar Karaoke

A single-page, play-along chord and fingerpicking trainer for **"If I Were"** by Vashti Bunyan
(*Lookaftering*, 2005).

Open the page, hit play, and it walks through the song in time: the current chord in large
type, the chord diagram, the next two chords, and an animated right-hand pattern showing
exactly which string each finger plucks on each beat.

## Features

- **Timed chord scroller** — the full chart scrolls and highlights in time, at 97 BPM.
- **Audio play-along** — a synthesised plucked guitar plays the pattern, with an optional
  metronome click. No audio files, no external requests; everything is Web Audio.
- **Chord diagrams** — rendered as SVG with finger numbers, drawn from a shape table.
- **Four right-hand patterns** — from a plain `p-i-m-a` arpeggio to a sparse half-time
  version, each with the thumb's bass string tracked per chord.
- **Tempo control** — 40–120% of the original tempo.
- **Section looping** — loop the intro, either verse, or the outro while you drill it.
- **Capo 0–7** — shapes stay the same, sounding pitch moves, so you can find your own
  vocal range.
- **Easy `F`** — click the `Fmaj7` card to swap the barre chord out everywhere.

Keyboard: <kbd>Space</kbd> play/pause, <kbd>R</kbd> restart, <kbd>←</kbd>/<kbd>→</kbd> step a
chord, <kbd>↑</kbd>/<kbd>↓</kbd> tempo.

## The song

| | |
|---|---|
| Key | C major (D minor feel) |
| Tempo | 97 BPM |
| Metre | 4/4 |
| Tuning | Standard, EADGBE |
| Chords | Dm, C, Em, F, G, Am |
| Length | 2:15 |

Every chord in the song is diatonic to C major, which is what makes it so approachable —
six open shapes and no key changes.

## Accuracy

Worth being straight about which parts are sourced and which are reconstructed:

- **The chord progression** comes from a published transcription, and is corroborated by the
  song's reported key — all six chords are diatonic to C major, consistent across sources.
- **The fingerpicking patterns are suggestions**, not a transcription. No source found
  notates the right hand for this song; the patterns here are idiomatic ones built to fit the
  harmony and the feel of the record.
- **The timing assumes two beats per chord.** That fits the paired chord movement in the
  transcription, but play along with the record and switch to the `4 beats` setting if a
  section drifts.

Treat it as a practice scaffold rather than an authoritative transcription.

## Running it

It's one self-contained `index.html` with no dependencies or build step.

```sh
python3 -m http.server 8000   # then open http://localhost:8000
```

Or just open `index.html` in a browser. Browsers require a user gesture before audio starts,
so press **Play** rather than expecting sound on load.

## Note on lyrics

No lyrics are reproduced here. "If I Were" was written and recorded by Vashti Bunyan; chord
progressions and song structure are factual musical information, presented for study and
practice. Please support the artist by buying *Lookaftering*.
