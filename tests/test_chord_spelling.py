"""Every shape must spell the chord it is named for.

The sounding notes come from OPEN_MIDI + fret, the same arithmetic
app.js's stringMidi() does.  Capo is ignored: it shifts every string
equally, and songs.js names shapes, not sounding chords ("Hold Bm, hear
Cm").
"""

import unittest

import chordnames
import jsdata
from jsdata import SONGS

#: Shapes that deliberately sound a note their name does not call for.
#: Each entry must stay documented in the song's own notes -- see
#: test_documented_deviations_are_still_documented below.
DOCUMENTED_EXTRA_NOTES = {
    # "About the names" in Just Like a Woman: with the open B and high e
    # ringing, x33010 keeps the major third, so it is strictly Cadd4.  The
    # dylanchords label is kept on purpose.
    ("justlikeawoman", "Csus4"): {4},   # E, the major third
}


class ChordSpellingTests(unittest.TestCase):

    def test_every_chord_name_is_one_we_can_read(self):
        for song_id, song in SONGS.items():
            for name in song["shapes"]:
                with self.subTest(song=song_id, chord=name):
                    chordnames.expected_pitch_classes(name)   # raises if unknown

    def test_shape_sounds_every_note_its_name_calls_for(self):
        for song_id, song in SONGS.items():
            for name, shape in song["shapes"].items():
                expected = chordnames.expected_pitch_classes(name)
                actual = jsdata.pitch_classes(shape)
                with self.subTest(song=song_id, chord=name):
                    missing = expected - actual
                    self.assertFalse(
                        missing,
                        "%s (%s) is missing %s; it sounds %s"
                        % (name, _frets(shape), chordnames.spell(missing),
                           chordnames.spell(actual)))

    def test_shape_sounds_no_note_outside_its_name(self):
        for song_id, song in SONGS.items():
            for name, shape in song["shapes"].items():
                expected = chordnames.expected_pitch_classes(name)
                allowed = expected | DOCUMENTED_EXTRA_NOTES.get((song_id, name), set())
                actual = jsdata.pitch_classes(shape)
                with self.subTest(song=song_id, chord=name):
                    extra = actual - allowed
                    self.assertFalse(
                        extra,
                        "%s (%s) also sounds %s"
                        % (name, _frets(shape), chordnames.spell(extra)))

    def test_documented_deviations_really_do_deviate(self):
        # If a shape is corrected, its entry here should go too, rather than
        # sitting around excusing a chord that no longer needs it.
        for (song_id, name), extra in DOCUMENTED_EXTRA_NOTES.items():
            shape = SONGS[song_id]["shapes"][name]
            actual = jsdata.pitch_classes(shape)
            expected = chordnames.expected_pitch_classes(name)
            with self.subTest(song=song_id, chord=name):
                self.assertEqual(actual - expected, extra)

    def test_documented_deviations_are_still_documented(self):
        # The Csus4/Cadd4 naming is only acceptable because the song's notes
        # explain it.  Lose the explanation and this fails.
        notes = jsdata.note_text(SONGS["justlikeawoman"])
        self.assertIn("Cadd4", notes)
        self.assertIn("x33010", notes)

    def test_bass_string_sounds_a_chord_tone(self):
        # The thumb is the loudest note in every pattern; it should not land
        # on a note outside the chord.
        for song_id, song in SONGS.items():
            for name, shape in song["shapes"].items():
                allowed = (chordnames.expected_pitch_classes(name)
                           | DOCUMENTED_EXTRA_NOTES.get((song_id, name), set()))
                for key in ("bass", "alt"):
                    if key not in shape:
                        continue
                    midi = jsdata.sounding_midi(shape, shape[key])
                    with self.subTest(song=song_id, chord=name, thumb=key):
                        self.assertIsNotNone(midi)
                        self.assertIn(midi % 12, allowed,
                                      "%s bass sounds %s" % (name, chordnames.spell({midi % 12})))

    def test_bass_string_is_the_lowest_sounding_string(self):
        # shape.bass is the root bass note the thumb takes on beat 1; nothing
        # below it should be left ringing.
        for song_id, song in SONGS.items():
            for name, shape in song["shapes"].items():
                if "bass" not in shape:
                    continue
                lowest = min(i for i, f in enumerate(shape["frets"]) if f >= 0)
                with self.subTest(song=song_id, chord=name):
                    self.assertEqual(shape["bass"], lowest)

    def test_known_chords_spell_what_music_theory_says(self):
        # A guard on the checker itself, so a broken interval table cannot
        # make the tests above pass vacuously.
        self.assertEqual(chordnames.spell(chordnames.expected_pitch_classes("C")),
                         ["C", "E", "G"])
        self.assertEqual(chordnames.spell(chordnames.expected_pitch_classes("Am")),
                         ["C", "E", "A"])
        self.assertEqual(chordnames.spell(chordnames.expected_pitch_classes("G7")),
                         ["D", "F", "G", "B"])
        self.assertEqual(chordnames.spell(chordnames.expected_pitch_classes("F#5")),
                         ["C#", "F#"])
        self.assertEqual(chordnames.spell(chordnames.expected_pitch_classes("Cmaj7")),
                         ["C", "E", "G", "B"])

    def test_unknown_quality_is_rejected(self):
        with self.assertRaises(chordnames.UnknownChordName):
            chordnames.expected_pitch_classes("Cwhatever")
        with self.assertRaises(chordnames.UnknownChordName):
            chordnames.expected_pitch_classes("H")


def _frets(shape):
    return "".join("x" if f < 0 else str(f) for f in shape["frets"])


if __name__ == "__main__":
    unittest.main()
