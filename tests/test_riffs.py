"""Riffs: exact-note lead parts, and the split bars that go with them.

A song may carry `riffs` (name -> one bar of step tokens) and give each
section a `riff` list naming the bar to play under each of its bars.
app.js parses the tokens in parseRiffBar(); the grammar is restated here
and checked against that function, so the two cannot drift apart.
"""

import re
import unittest

import jsdata
from jsdata import SONGS

#: The token grammar parseRiffBar() accepts: "." and "r", or notes joined
#: by "+", each a string letter, a fret and an optional x (dead) or ~ (ring).
NOTE = re.compile(r"^([EADGBe])(\d+)([x~]?)$")
STRING_LETTERS = "EADGBe"

RIFF_SONGS = {song_id: song for song_id, song in SONGS.items() if song.get("riffs")}


def parse_riff_bar(text):
    """Python port of parseRiffBar(): None, "r", or a list of note dicts."""
    out = []
    for tok in text.split():
        if tok == ".":
            out.append(None)
        elif tok == "r":
            out.append("r")
        else:
            notes = []
            for part in tok.split("+"):
                m = NOTE.match(part)
                if not m:
                    raise ValueError("bad riff note %r in %r" % (part, tok))
                notes.append({"str": STRING_LETTERS.index(m.group(1)), "fret": int(m.group(2)),
                              "dead": m.group(3) == "x", "ring": m.group(3) == "~"})
            out.append(notes)
    return out


def section_riff(section):
    return section.get("riff", "").split()


class RiffGrammarTests(unittest.TestCase):

    def test_the_port_still_matches_app_js(self):
        source = jsdata.app_js_source()
        self.assertIn('const RIFF_STRINGS = "EADGBe";', source)
        self.assertIn(r"/^([EADGBe])(\d+)([x~]?)$/", source)
        self.assertIn('if (tok === ".") return null;', source)
        self.assertIn('if (tok === "r") return "r";', source)

    def test_the_port_reads_each_kind_of_token(self):
        bar = parse_riff_bar(". r G12+B12 D12x e0~")
        self.assertEqual(bar[0], None)
        self.assertEqual(bar[1], "r")
        self.assertEqual([(n["str"], n["fret"]) for n in bar[2]], [(3, 12), (4, 12)])
        self.assertTrue(bar[3][0]["dead"])
        self.assertTrue(bar[4][0]["ring"])
        self.assertEqual(bar[4][0]["str"], 5)

    def test_a_malformed_note_is_rejected(self):
        for bad in ("H3", "G", "g3", "G3y", "G-1"):
            with self.subTest(token=bad), self.assertRaises(ValueError):
                parse_riff_bar(bad)


class RiffDataTests(unittest.TestCase):

    def test_some_song_has_riffs(self):
        # Otherwise everything below passes vacuously.
        self.assertTrue(RIFF_SONGS)

    def test_every_riff_bar_parses_and_fills_one_bar(self):
        for song_id, song in RIFF_SONGS.items():
            for name, text in song["riffs"].items():
                with self.subTest(song=song_id, riff=name):
                    self.assertEqual(len(parse_riff_bar(text)), song["stepsPerBar"])

    def test_riff_notes_are_on_the_grid_and_on_the_neck(self):
        for song_id, song in RIFF_SONGS.items():
            grid = {index for index, _ in song["gridStrings"]}
            for name, text in song["riffs"].items():
                for step, tok in enumerate(parse_riff_bar(text)):
                    if not isinstance(tok, list):
                        continue
                    for note in tok:
                        with self.subTest(song=song_id, riff=name, step=step):
                            self.assertIn(note["str"], grid)
                            self.assertLessEqual(note["fret"], 24)

    def test_no_step_strikes_one_string_twice(self):
        for song_id, song in RIFF_SONGS.items():
            for name, text in song["riffs"].items():
                for step, tok in enumerate(parse_riff_bar(text)):
                    if isinstance(tok, list):
                        strings = [n["str"] for n in tok]
                        with self.subTest(song=song_id, riff=name, step=step):
                            self.assertEqual(len(strings), len(set(strings)))

    def test_every_section_names_one_riff_bar_per_bar(self):
        for song_id, song in RIFF_SONGS.items():
            for section in song["sections"]:
                with self.subTest(song=song_id, section=section["name"]):
                    self.assertEqual(len(section_riff(section)),
                                     len(jsdata.section_chords(section)))
                    for name in section_riff(section):
                        self.assertIn(name, song["riffs"])

    def test_every_riff_bar_is_played_somewhere(self):
        for song_id, song in RIFF_SONGS.items():
            used = {name for section in song["sections"] for name in section_riff(section)}
            with self.subTest(song=song_id):
                self.assertEqual(used, set(song["riffs"]))

    def test_a_riff_pattern_exists_exactly_where_riffs_do(self):
        for song_id, song in SONGS.items():
            has_pattern = any(p.get("riff") for p in song["patterns"])
            with self.subTest(song=song_id):
                self.assertEqual(has_pattern, bool(song.get("riffs")))

    def test_sections_without_riffs_do_not_name_any(self):
        for song_id, song in SONGS.items():
            if song.get("riffs"):
                continue
            for section in song["sections"]:
                with self.subTest(song=song_id, section=section["name"]):
                    self.assertNotIn("riff", section)


class SplitBarTests(unittest.TestCase):
    """A bar token "Cadd9,Bm/D" is two chords, one per half."""

    def test_a_split_bar_holds_exactly_two_chords(self):
        for song_id, song in SONGS.items():
            for bar in jsdata.bars(song):
                with self.subTest(song=song_id, bar=bar):
                    halves = jsdata.bar_chords(bar)
                    self.assertIn(len(halves), (1, 2))
                    self.assertTrue(all(halves), "empty half in %r" % bar)

    def test_split_bars_divide_evenly(self):
        # chordAt() switches at stepsPerBar / 2.
        for song_id, song in SONGS.items():
            if any("," in bar for bar in jsdata.bars(song)):
                with self.subTest(song=song_id):
                    self.assertEqual(song["stepsPerBar"] % 2, 0)

    def test_the_engine_still_splits_at_the_half_bar(self):
        source = jsdata.app_js_source()
        self.assertIn('const two = c.split(",");', source)
        self.assertIn("step >= SONG.stepsPerBar / 2", source)


class ThisCharmingManTests(unittest.TestCase):
    """Claims the song's notes make about its own data."""

    SONG = SONGS["thischarmingman"]

    def test_the_riff_opens_on_the_g_and_b_strings_at_the_12th_fret(self):
        # "The riff opens on the G and B strings, both at the 12th fret"
        first = self.SONG["sections"][0]
        steps = parse_riff_bar(self.SONG["riffs"][section_riff(first)[0]])
        opening = next(tok for tok in steps if isinstance(tok, list))
        self.assertEqual(sorted((n["str"], n["fret"]) for n in opening), [(3, 12), (4, 12)])
        self.assertIn("G and B strings, both at the 12th fret", jsdata.note_text(self.SONG))

    def test_the_chorus_changes_chord_every_half_bar(self):
        chorus = [s for s in self.SONG["sections"] if s["name"] == "Chorus 1"][0]
        bars = jsdata.section_chords(chorus)
        self.assertEqual(bars[:4], ["Cadd9,Bm/D", "Em,A", "Cadd9,A7", "Em"])

    def test_the_cue_slot_count(self):
        self.assertEqual(len(jsdata.line_bars(self.SONG)), 32)


if __name__ == "__main__":
    unittest.main()
