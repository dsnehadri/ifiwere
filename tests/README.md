# Tests

Standard-library Python, no dependencies, no network:

```
python3 -m unittest discover -s tests -v
```

Run it from the repository root. GitHub Actions runs the same command on
every push and pull request (`.github/workflows/tests.yml`).

There is no JavaScript runtime in this project's toolchain, so the tests
read `songs.js` and `app.js` as text:

| File | What it is |
|---|---|
| `jsdata.py` | Parses the JS object literals in `songs.js` (`OPEN_MIDI`, `SONGS`) and derives bar lists, sung-line bars and runtimes the way `loadSong()` does. |
| `chordnames.py` | Turns a chord name into the pitch classes it calls for. |
| `lyricfile.py` | A Python port of `parseLyricFile()` from `app.js`. |
| `engine.py` | Python ports of `stepStrings()`, `esc()` and `diagram()`'s base-fret rule. |
| `test_song_data.py` | Shapes, sections, patterns and header facts in `songs.js`. |
| `test_chord_spelling.py` | Every shape spells the chord it is named for. |
| `test_runtimes.py` | `bars x beatsPerBar x 60 / bpm` against the runtimes the notes state. |
| `test_parse_lyric_file.py` | The lyric-cue parsing rules, plus a check that the port still matches `app.js`. |
| `test_lyric_templates.py` | `lyrics/*.template.txt` hold comments and blanks only, and their headers match `songs.js`. |
| `test_step_strings.py` | Which strings each pattern step plucks, the muted-string fallback, strums, pinches, and `esc()`. |
| `test_dom_contract.py` | Every id and class `app.js` reaches for exists in `index.html`, and script order. |
| `test_ci_workflow.py` | The workflow still runs this suite, read-only, with no secrets or deploy steps. |

The filled-in `lyrics/<song id>.txt` files are deliberately never read:
only the `.template.txt` files are.

If a test fails after a deliberate change to a song, the fix is usually in
`songs.js` or in the template header it disagrees with -- the tests assert
that the two tell the same story.
