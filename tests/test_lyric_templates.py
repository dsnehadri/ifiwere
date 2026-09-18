"""lyrics/*.template.txt must hold comments and blank lines only.

The templates ship with the site and are meant to be copied to
lyrics/<song id>.txt and filled in.  They must therefore contain no lyric
text of their own -- parsing one has to yield zero cues -- and their
header has to describe the song the way songs.js actually defines it.

Only the .template.txt files are read here.  The filled-in lyrics/*.txt
files are never opened.
"""

import glob
import os
import re
import unittest

import jsdata
from lyricfile import parse_lyric_file

TEMPLATES = sorted(glob.glob(os.path.join(jsdata.LYRICS_DIR, "*.template.txt")))

#: "#   Verse 1      bars 9, 11, 13, 15, 17"
_BAR_LIST = re.compile(r"^#\s+(\S.*?)\s+bars\s+([\d,\s]+)$")
_LINE_COUNT = re.compile(r"^#\s*This song has (\d+) sung lines\.")
_SAVE_AS = re.compile(r"^#\s*IMPORTANT: save this as (\S+?)\.txt")


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def song_id_of(path):
    return os.path.basename(path)[:-len(".template.txt")]


class TemplateInventoryTests(unittest.TestCase):

    def test_templates_were_found(self):
        self.assertTrue(TEMPLATES, "no lyrics/*.template.txt files")

    def test_every_song_has_a_template(self):
        have = {song_id_of(p) for p in TEMPLATES}
        self.assertEqual(have, set(jsdata.SONGS))

    def test_no_template_is_itself_a_lyric_file(self):
        # A template must never be named <id>.txt: that is the file the page
        # fetches, and it would publish an empty cue set.
        for path in TEMPLATES:
            self.assertTrue(path.endswith(".template.txt"), path)


class TemplateContentTests(unittest.TestCase):
    """Comments and blanks only -- no lyrics in a tracked template."""

    def test_every_line_is_blank_or_a_comment(self):
        for path in TEMPLATES:
            for number, raw in enumerate(read(path).split("\n"), start=1):
                line = raw.strip()
                with self.subTest(template=os.path.basename(path), line=number):
                    self.assertTrue(line == "" or line.startswith("#"),
                                    "template holds lyric text: %r" % raw)

    def test_parsing_a_template_yields_no_cues(self):
        for path in TEMPLATES:
            song = jsdata.SONGS[song_id_of(path)]
            cues = parse_lyric_file(read(path), len(jsdata.bars(song)),
                                    jsdata.line_bars(song))
            with self.subTest(template=os.path.basename(path)):
                self.assertEqual(cues, {}, "template would load cues of its own")

    def test_templates_are_plain_ascii_text(self):
        for path in TEMPLATES:
            with self.subTest(template=os.path.basename(path)):
                text = read(path)
                self.assertFalse(text.startswith("﻿"), "template starts with a BOM")
                self.assertNotIn("\r", text, "template has CRLF line endings")

    def test_template_has_a_blank_slot_for_every_sung_line(self):
        # The blank lines after the header are where the lines get pasted.
        for path in TEMPLATES:
            song = jsdata.SONGS[song_id_of(path)]
            lines = read(path).split("\n")
            body_start = max(i for i, l in enumerate(lines)
                             if l.startswith("#     python3 -m http.server"))
            blanks = sum(1 for l in lines[body_start:] if l.strip() == "")
            with self.subTest(template=os.path.basename(path)):
                self.assertGreaterEqual(blanks, len(jsdata.line_bars(song)),
                                        "fewer blank slots than the song has sung lines")


class TemplateHeaderTests(unittest.TestCase):
    """The header's promises must match songs.js."""

    def test_header_names_the_song_and_artist(self):
        for path in TEMPLATES:
            song = jsdata.SONGS[song_id_of(path)]
            first = read(path).split("\n")[0]
            with self.subTest(template=os.path.basename(path)):
                self.assertIn(song["title"], first)
                self.assertIn(song["artist"], first)

    def test_header_tells_the_reader_the_right_filename(self):
        for path in TEMPLATES:
            song_id = song_id_of(path)
            m = _find(read(path), _SAVE_AS)
            with self.subTest(template=os.path.basename(path)):
                self.assertIsNotNone(m, "no 'save this as ...' line")
                self.assertEqual(m.group(1), song_id)

    def test_sung_line_count_matches_the_song(self):
        for path in TEMPLATES:
            song = jsdata.SONGS[song_id_of(path)]
            m = _find(read(path), _LINE_COUNT)
            with self.subTest(template=os.path.basename(path)):
                self.assertIsNotNone(m, "no 'This song has N sung lines' line")
                self.assertEqual(int(m.group(1)), len(jsdata.line_bars(song)))

    def test_bar_lists_match_the_sections_they_name(self):
        for path in TEMPLATES:
            song = jsdata.SONGS[song_id_of(path)]
            bounds = jsdata.section_bounds(song)
            listed = _bar_lists(read(path))
            self.assertTrue(listed, "%s lists no bars" % os.path.basename(path))
            for name, bars in listed:
                with self.subTest(template=os.path.basename(path), section=name):
                    self.assertIn(name, bounds, "no such section in songs.js")
                    section = [s for s in song["sections"] if s["name"] == name][0]
                    start = bounds[name][0]
                    expected = [start + offset + 1 for offset in section.get("lines", [])]
                    self.assertEqual(bars, expected,
                                     "template bar numbers disagree with songs.js")

    def test_bar_lists_cover_every_section_that_has_sung_lines(self):
        for path in TEMPLATES:
            song = jsdata.SONGS[song_id_of(path)]
            with_lines = [s["name"] for s in song["sections"] if s.get("lines")]
            listed = [name for name, _ in _bar_lists(read(path))]
            with self.subTest(template=os.path.basename(path)):
                self.assertEqual(listed, with_lines,
                                 "the header's sections are missing, extra or out of order")

    def test_listed_bars_add_up_to_the_stated_line_count(self):
        for path in TEMPLATES:
            text = read(path)
            stated = int(_find(text, _LINE_COUNT).group(1))
            listed = sum(len(bars) for _, bars in _bar_lists(text))
            with self.subTest(template=os.path.basename(path)):
                self.assertEqual(listed, stated)

    def test_the_pin_example_points_at_a_real_bar(self):
        for path in TEMPLATES:
            song = jsdata.SONGS[song_id_of(path)]
            total = len(jsdata.bars(song))
            m = re.search(r"prefix it with the bar number:\s+(\d+):", read(path))
            with self.subTest(template=os.path.basename(path)):
                self.assertIsNotNone(m, "no 'prefix it with the bar number' example")
                self.assertIn(int(m.group(1)), range(1, total + 1))


def _find(text, pattern):
    for line in text.split("\n"):
        m = pattern.match(line)
        if m:
            return m
    return None


def _bar_lists(text):
    """[(section name, [1-based bar numbers]), ...] from the header."""
    out = []
    for line in text.split("\n"):
        m = _BAR_LIST.match(line)
        if m:
            bars = [int(n) for n in m.group(2).replace(" ", "").split(",") if n]
            out.append((m.group(1).strip(), bars))
    return out


if __name__ == "__main__":
    unittest.main()
