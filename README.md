# Guitar Karaoke

A single self-contained page that walks you through a song in time: the current chord in
large type, its diagram, the next two chords, and an animated right-hand pattern showing
exactly which string each finger plucks on each beat.

**Live: https://dsnehadri.github.io/ifiwere/**

Two songs so far, picked from the selector at the top:

| Song | Artist | Key | Metre | Tempo |
|---|---|---|---|---|
| If I Were | Vashti Bunyan | C major | 3/4 | 97 BPM |
| Just Like a Woman | Bob Dylan | E major (capo 4, C shapes) | 4/4 | 115 BPM |

## Features

- **Timed chord scroller** — the full chart scrolls and highlights in time.
- **Audio play-along** — a synthesised plucked guitar plays the pattern, with an optional
  metronome click. No audio files, no external requests; everything is Web Audio.
- **Chord diagrams** — SVG, with finger numbers, barre rendering and position markers.
- **Animated picking grid** — string rows against the beats of the bar, showing which finger
  plucks what. The thumb's string is re-marked per chord, so alternating-bass patterns show
  the correct bass note for the chord you're actually on.
- **Multiple right-hand patterns per song**, including strummed options where the record is
  strummed, and a sparse "learning" pattern for locking changes in before adding the roll.
- **Editable cues with built-in alignment** — see below.
- **Tempo 40–120%**, **capo 0–7**, and **per-section looping**.

Keyboard: <kbd>Space</kbd> play/pause, <kbd>R</kbd> restart, <kbd>←</kbd>/<kbd>→</kbd> step a
chord, <kbd>↑</kbd>/<kbd>↓</kbd> tempo.

## Cues, and the note on lyrics

**No lyrics are reproduced here, and none are committed to this repo.**

What *is* committed is the **alignment map** — per song, a list of which bars carry a sung
line. That's timing information derived from song structure, and it's what lets the page
place your text correctly without ever containing it.

Press `✎ Cues`, paste the sung lines one per line, press **Align lines**, and they drop onto
those bars. Each cue holds on screen until the next begins. `Apply numbered` (`bar: text`)
gives per-bar control, `Load current` round-trips for backup, `Clear all` wipes. Everything
lives in your browser's local storage, keyed per song — nothing is uploaded, and clearing
browser data clears it.

Chord progressions, voicings and structure are factual musical information presented for
study and practice. Please support these artists by buying their records.

## Accuracy

Different parts of this rest on very different evidence. Per song:

**If I Were** — the voicings and picking pattern are transcribed from a guitar lesson, so
they reflect how it's actually played. All chords sit on the top four strings, thumb fixed on
the D string, `p–i–m–a–m–i` throughout. The chord order comes from a separate published
transcription. The 3/4 reading is inferred, and checks out: 76 bars at 97 BPM ≈ 2:21 against
the track's 2:15.

**Just Like a Woman** — the chords and capo are well documented and agree across sources.
**The bar counts are my model, not a transcription** — sources give chord order but not
bar-exact timing. Four bars per line and sixteen per section puts it at 4:43 against the
track's 4:52. **The picking patterns are idiomatic, not transcribed**; the record is a band
arrangement with strummed guitar, so the "Strum" pattern is closest to what you hear.

Treat both as practice scaffolds rather than authoritative transcriptions.

## Layout

| File | What's in it |
|---|---|
| `index.html` | Page shell and stylesheet |
| `songs.js` | All song data — shapes, sections, patterns, notes, alignment maps |
| `app.js` | The engine; knows nothing about any particular song |

Adding a song means adding one entry to `SONGS` in `songs.js`. Nothing else needs touching.

## Running it

No dependencies, no build step.

```sh
python3 -m http.server 8000   # then open http://localhost:8000
```

Browsers need a user gesture before audio starts, so press **Play** rather than expecting
sound on load.
