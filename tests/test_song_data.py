"""Structural checks on the song data in songs.js.

Everything the engine in app.js assumes about a song is asserted here:
chords resolve to shapes, thumb strings sound and are visible on the
pattern grid, sung-line offsets land inside their section, and every
pattern fills exactly one bar.
"""

import unittest

import jsdata
from jsdata import SONGS


class SongShapeTests(unittest.TestCase):
    """Per-song invariants that hold for every song in the file."""

    def test_at_least_one_song(self):
        self.assertTrue(SONGS, "songs.js defines no songs")

    def test_required_top_level_fields(self):
        required = ["title", "artist", "album", "bpm", "stepsPerBar", "beatsPerBar",
                    "cueKey", "gridStrings", "facts", "shapes", "sections", "patterns", "notes"]
        for song_id, song in SONGS.items():
            for field in required:
                with self.subTest(song=song_id, field=field):
                    self.assertIn(field, song)

    def test_cue_key_is_derived_from_the_song_id(self):
        for song_id, song in SONGS.items():
            with self.subTest(song=song_id):
                self.assertEqual(song["cueKey"], song_id + "-cues-v1")

    def test_cue_keys_are_unique(self):
        keys = [song["cueKey"] for song in SONGS.values()]
        self.assertEqual(len(keys), len(set(keys)), "two songs share a localStorage cue key")

    def test_steps_per_bar_divides_into_beats(self):
        # stepsPerBeat() must be a whole number: the click and the beat dots
        # are placed with `i % stepsPerBeat() === 0`.
        for song_id, song in SONGS.items():
            with self.subTest(song=song_id):
                self.assertEqual(song["stepsPerBar"] % song["beatsPerBar"], 0)

    def test_grid_strings_are_valid_string_indices(self):
        for song_id, song in SONGS.items():
            for index, label in song["gridStrings"]:
                with self.subTest(song=song_id, label=label):
                    self.assertIn(index, range(6))
                    self.assertEqual(label, jsdata.STRING_NAMES[index])


class ShapeTests(unittest.TestCase):
    """Chord shapes: six strings, sane fingers, well-formed barres."""

    def test_frets_are_six_strings_in_range(self):
        for song_id, song in SONGS.items():
            for name, shape in song["shapes"].items():
                with self.subTest(song=song_id, chord=name):
                    self.assertEqual(len(shape["frets"]), 6)
                    for fret in shape["frets"]:
                        self.assertGreaterEqual(fret, -1)
                        self.assertLessEqual(fret, 24)

    def test_a_shape_sounds_at_least_two_strings(self):
        for song_id, song in SONGS.items():
            for name, shape in song["shapes"].items():
                with self.subTest(song=song_id, chord=name):
                    sounding = [f for f in shape["frets"] if f >= 0]
                    self.assertGreaterEqual(len(sounding), 2)

    def test_a_finger_is_given_exactly_where_a_string_is_fretted(self):
        for song_id, song in SONGS.items():
            for name, shape in song["shapes"].items():
                self.assertEqual(len(shape["fingers"]), 6, "%s %s" % (song_id, name))
                for string, (fret, finger) in enumerate(zip(shape["frets"], shape["fingers"])):
                    with self.subTest(song=song_id, chord=name, string=string):
                        if fret > 0:
                            self.assertIn(finger, (1, 2, 3, 4),
                                          "fretted string with no finger number")
                        else:
                            self.assertEqual(finger, 0,
                                             "open or muted string carries a finger number")

    def test_barre_spans_strings_fretted_at_or_above_the_barre(self):
        for song_id, song in SONGS.items():
            for name, shape in song["shapes"].items():
                barre = shape.get("barre")
                if not barre:
                    continue
                with self.subTest(song=song_id, chord=name):
                    self.assertLess(barre["from"], barre["to"])
                    self.assertEqual(shape["frets"][barre["from"]], barre["fret"],
                                     "the barre's lowest string is not at the barre fret")
                    self.assertEqual(shape["frets"][barre["to"]], barre["fret"],
                                     "the barre's highest string is not at the barre fret")
                    for string in range(barre["from"], barre["to"] + 1):
                        self.assertGreaterEqual(
                            shape["frets"][string], barre["fret"],
                            "string %d sits below the barre" % string)

    def test_shape_fits_the_four_fret_diagram(self):
        # diagram() draws NF = 4 fret spaces and picks base = 1 when the
        # highest fret is within them, else the lowest fretted fret.  A shape
        # wider than four frets would draw its dots off the bottom of the grid.
        NF = 4
        for song_id, song in SONGS.items():
            for name, shape in song["shapes"].items():
                fretted = [f for f in shape["frets"] if f > 0]
                if not fretted:
                    continue
                base = 1 if max(fretted) <= NF else min(fretted)
                with self.subTest(song=song_id, chord=name):
                    self.assertLessEqual(max(fretted) - base, NF - 1,
                                         "%s spans more than %d frets" % (name, NF))

    def test_bass_and_alt_strings_sound_and_are_on_the_grid(self):
        # The thumb plays shape.bass / shape.alt.  A muted string there would
        # send the thumb through stepStrings()' fallback, and a string missing
        # from gridStrings would leave the "p" marker with nowhere to draw.
        for song_id, song in SONGS.items():
            grid = {index for index, _ in song["gridStrings"]}
            for name, shape in song["shapes"].items():
                for key in ("bass", "alt"):
                    if key not in shape or shape[key] is None:
                        continue
                    string = shape[key]
                    with self.subTest(song=song_id, chord=name, thumb=key):
                        self.assertIn(string, range(6))
                        self.assertGreaterEqual(
                            shape["frets"][string], 0,
                            "%s is muted in %s" % (jsdata.STRING_NAMES[string], name))
                        self.assertIn(string, grid,
                                      "%s is not in gridStrings" % jsdata.STRING_NAMES[string])

    def test_alt_bass_differs_from_the_root_bass(self):
        for song_id, song in SONGS.items():
            for name, shape in song["shapes"].items():
                if "alt" not in shape:
                    continue
                with self.subTest(song=song_id, chord=name):
                    self.assertNotEqual(shape["alt"], shape["bass"],
                                        "the alternating bass would not alternate")


class SectionTests(unittest.TestCase):
    """Sections, their chords and their sung-line offsets."""

    def test_every_chord_used_has_a_shape(self):
        for song_id, song in SONGS.items():
            for section in song["sections"]:
                for chord in jsdata.section_chords(section):
                    with self.subTest(song=song_id, section=section["name"], chord=chord):
                        self.assertIn(chord, song["shapes"])

    def test_every_shape_is_used_by_some_section(self):
        for song_id, song in SONGS.items():
            used = set(jsdata.bars(song))
            for name in song["shapes"]:
                with self.subTest(song=song_id, chord=name):
                    self.assertIn(name, used, "shape is defined but never played")

    def test_sections_are_named_and_non_empty(self):
        for song_id, song in SONGS.items():
            names = []
            for section in song["sections"]:
                with self.subTest(song=song_id, section=section.get("name")):
                    self.assertTrue(section.get("name"))
                    self.assertGreater(len(jsdata.section_chords(section)), 0)
                names.append(section["name"])
            self.assertEqual(len(names), len(set(names)),
                             "%s repeats a section name" % song_id)

    def test_line_offsets_fall_inside_their_section(self):
        for song_id, song in SONGS.items():
            for section in song["sections"]:
                length = len(jsdata.section_chords(section))
                for offset in section.get("lines", []):
                    with self.subTest(song=song_id, section=section["name"], offset=offset):
                        self.assertGreaterEqual(offset, 0)
                        self.assertLess(offset, length,
                                        "cue starts past the end of a %d-bar section" % length)

    def test_line_offsets_are_sorted_and_distinct(self):
        for song_id, song in SONGS.items():
            for section in song["sections"]:
                lines = section.get("lines", [])
                with self.subTest(song=song_id, section=section["name"]):
                    self.assertEqual(lines, sorted(set(lines)),
                                     "sung lines are out of order or repeat a bar")

    def test_line_bars_are_within_the_song_and_ascending(self):
        for song_id, song in SONGS.items():
            line_bars = jsdata.line_bars(song)
            total = len(jsdata.bars(song))
            with self.subTest(song=song_id):
                self.assertEqual(line_bars, sorted(set(line_bars)))
                if line_bars:
                    self.assertGreaterEqual(line_bars[0], 0)
                    self.assertLess(line_bars[-1], total)


class PatternTests(unittest.TestCase):
    """Picking and strumming patterns fill exactly one bar."""

    def test_each_pattern_has_steps_per_bar_steps(self):
        for song_id, song in SONGS.items():
            for pattern in song["patterns"]:
                with self.subTest(song=song_id, pattern=pattern["name"]):
                    self.assertEqual(len(pattern["steps"]), song["stepsPerBar"])

    def test_patterns_are_named_and_described(self):
        for song_id, song in SONGS.items():
            names = [p["name"] for p in song["patterns"]]
            self.assertEqual(len(names), len(set(names)), "%s repeats a pattern name" % song_id)
            for pattern in song["patterns"]:
                with self.subTest(song=song_id, pattern=pattern["name"]):
                    self.assertTrue(pattern["name"].strip())
                    self.assertTrue(pattern["desc"].strip())

    def test_step_fields_are_ones_the_engine_understands(self):
        # stepStrings() reads exactly st.strum, st.b, st.s and st.pinch; st.f
        # is the finger label drawn on the grid.
        allowed = {"s", "b", "f", "strum", "pinch"}
        for song_id, song in SONGS.items():
            for pattern in song["patterns"]:
                for i, step in enumerate(pattern["steps"]):
                    if step is None:
                        continue
                    with self.subTest(song=song_id, pattern=pattern["name"], step=i):
                        self.assertLessEqual(set(step), allowed)
                        self.assertTrue(
                            "strum" in step or "b" in step or "s" in step,
                            "step plucks nothing: no strum, b or s")
                        if "strum" in step:
                            self.assertIn(step["strum"], ("d", "u"))
                        if "b" in step:
                            self.assertIn(step["b"], (1, 2))
                        if "f" in step:
                            self.assertIn(step["f"], ("p", "i", "m", "a"))

    def test_fixed_pattern_strings_are_on_the_grid(self):
        for song_id, song in SONGS.items():
            grid = {index for index, _ in song["gridStrings"]}
            for pattern in song["patterns"]:
                for i, step in enumerate(pattern["steps"]):
                    if not step:
                        continue
                    for key in ("s", "pinch"):
                        if key in step:
                            with self.subTest(song=song_id, pattern=pattern["name"], step=i):
                                self.assertIn(step[key], grid,
                                              "step %s targets a string the grid never shows" % key)

    def test_alternating_bass_patterns_have_an_alt_string_to_use(self):
        # stepStrings() falls back to shape.bass when b === 2 and the shape has
        # no alt, which would silently turn an alternating bass into a drone.
        for song_id, song in SONGS.items():
            uses_alt = any(step and step.get("b") == 2
                           for pattern in song["patterns"] for step in pattern["steps"])
            if not uses_alt:
                continue
            for name, shape in song["shapes"].items():
                with self.subTest(song=song_id, chord=name):
                    self.assertIn("alt", shape,
                                  "%s has no alt bass but the song has an alternating"
                                  " bass pattern" % name)


class FactTests(unittest.TestCase):
    """The facts strip in the header must agree with the data driving playback."""

    def _fact(self, song, label):
        for key, value in song["facts"]:
            if key == label:
                return value
        return None

    def test_tempo_fact_matches_bpm(self):
        for song_id, song in SONGS.items():
            with self.subTest(song=song_id):
                self.assertEqual(self._fact(song, "Tempo"), "%d BPM" % song["bpm"])

    def test_metre_fact_matches_beats_per_bar(self):
        for song_id, song in SONGS.items():
            metre = self._fact(song, "Metre")
            with self.subTest(song=song_id):
                self.assertIsNotNone(metre, "no Metre fact")
                self.assertTrue(metre.startswith("%d/" % song["beatsPerBar"]),
                                "Metre %r does not start with %d beats"
                                % (metre, song["beatsPerBar"]))

    def test_capo_fact_matches_the_capo_field(self):
        for song_id, song in SONGS.items():
            capo = song.get("capo", 0)
            fact = self._fact(song, "Capo")
            with self.subTest(song=song_id):
                if capo:
                    self.assertIsNotNone(fact, "song has a capo but no Capo fact")
                    self.assertTrue(fact.startswith("%dst fret" % capo)
                                    or fact.startswith("%dth fret" % capo)
                                    or fact.startswith("%dnd fret" % capo)
                                    or fact.startswith("%drd fret" % capo),
                                    "Capo fact %r does not name fret %d" % (fact, capo))
                elif fact is not None:
                    self.assertTrue(fact.startswith("none"),
                                    "no capo set but the Capo fact says %r" % fact)


if __name__ == "__main__":
    unittest.main()
