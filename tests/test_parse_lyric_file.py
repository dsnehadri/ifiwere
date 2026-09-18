"""The lyric-cue file parsing rules from app.js.

parseLyricFile() cannot be executed here (no JavaScript runtime), so
tests/lyricfile.py restates its rules in Python and the behaviour tests
run against that port.  SourceAgreementTests pulls the real function out
of app.js and asserts each rule is still written there, so the port
cannot drift away from the code it stands in for.
"""

import re
import unittest

import jsdata
from lyricfile import NUMBERED_RE, cue_for, js_trim, parse_lyric_file

#: A stand-in song: 20 bars, sung lines starting at bars 3, 7 and 11
#: (0-based), i.e. bars 4, 8 and 12 as a lyric file numbers them.
TOTAL = 20
LINE_BARS = [3, 7, 11]


def parse(text, total=TOTAL, line_bars=None):
    return parse_lyric_file(text, total, LINE_BARS if line_bars is None else line_bars)


class PlainLineTests(unittest.TestCase):
    """Plain lines fill the sung-line slots in order."""

    def test_lines_drop_onto_the_sung_line_bars_in_order(self):
        self.assertEqual(parse("first\nsecond\nthird"),
                         {3: "first", 7: "second", 11: "third"})

    def test_blank_lines_are_ignored_so_verses_can_be_spaced_out(self):
        text = "first\n\n\nsecond\n   \n\t\nthird\n"
        self.assertEqual(parse(text), {3: "first", 7: "second", 11: "third"})

    def test_comment_lines_are_ignored(self):
        text = "# --- Verse 1 ---\nfirst\n#second is a comment\nthird"
        self.assertEqual(parse(text), {3: "first", 7: "third"})

    def test_a_comment_marker_must_be_the_first_character_after_trimming(self):
        self.assertEqual(parse("   # indented comment\nsung"), {3: "sung"})
        self.assertEqual(parse("not a # comment"), {3: "not a # comment"})

    def test_leading_and_trailing_whitespace_is_stripped(self):
        self.assertEqual(parse("   padded line   "), {3: "padded line"})

    def test_carriage_returns_are_handled(self):
        self.assertEqual(parse("first\r\nsecond\r\n"), {3: "first", 7: "second"})

    def test_lines_past_the_last_slot_are_dropped(self):
        self.assertEqual(parse("a\nb\nc\nd\ne"), {3: "a", 7: "b", 11: "c"})

    def test_fewer_lines_than_slots_leaves_the_rest_empty(self):
        self.assertEqual(parse("only one"), {3: "only one"})

    def test_a_song_with_no_sung_line_slots_takes_no_plain_lines(self):
        self.assertEqual(parse("a\nb", line_bars=[]), {})

    def test_empty_and_comment_only_input_yields_nothing(self):
        self.assertEqual(parse(""), {})
        self.assertEqual(parse("\n\n   \n"), {})
        self.assertEqual(parse("# just a header\n#\n# more\n"), {})

    def test_a_byte_order_mark_does_not_swallow_the_first_line(self):
        # JavaScript's trim() strips U+FEFF, so a BOM-prefixed first line is
        # still an ordinary lyric line.
        self.assertEqual(parse("﻿first\nsecond"), {3: "first", 7: "second"})


class NumberedLineTests(unittest.TestCase):
    """"12: text" pins a bar; the number is 1-based."""

    def test_a_numbered_line_pins_that_bar(self):
        self.assertEqual(parse("12: pinned"), {11: "pinned"})

    def test_bar_numbers_are_one_based(self):
        self.assertEqual(parse("1: first bar"), {0: "first bar"})

    def test_a_pipe_also_separates_the_number_from_the_text(self):
        self.assertEqual(parse("12 | pinned"), {11: "pinned"})

    def test_space_around_the_separator_is_optional(self):
        self.assertEqual(parse("12:pinned"), {11: "pinned"})
        self.assertEqual(parse("12   :   pinned"), {11: "pinned"})

    def test_text_after_the_separator_is_trimmed(self):
        self.assertEqual(parse("12:   pinned   "), {11: "pinned"})

    def test_a_pinned_line_does_not_consume_a_sequential_slot(self):
        self.assertEqual(parse("12: pinned\nfirst\nsecond"),
                         {11: "pinned", 3: "first", 7: "second"})

    def test_a_pinned_bar_wins_over_the_sequential_fill(self):
        self.assertEqual(parse("8: pinned\nfirst\nsecond\nthird"),
                         {3: "first", 7: "pinned", 11: "third"})

    def test_a_plain_line_whose_slot_is_pinned_is_dropped_not_shifted(self):
        # "second" would have gone to bar 7; bar 7 is pinned, so it is lost
        # and "third" still lands on its own slot.
        result = parse("8: pinned\nfirst\nsecond\nthird")
        self.assertNotIn("second", result.values())
        self.assertEqual(result[11], "third")

    def test_bar_numbers_outside_the_song_are_ignored(self):
        self.assertEqual(parse("0: before the start"), {})
        self.assertEqual(parse("21: past the end"), {})
        self.assertEqual(parse("20: last bar"), {19: "last bar"})

    def test_an_out_of_range_numbered_line_is_not_reused_as_a_plain_line(self):
        # It matched the numbered pattern, so it never reaches the plain list.
        self.assertEqual(parse("99: nowhere\nfirst"), {3: "first"})

    def test_a_numbered_line_with_no_text_sets_nothing(self):
        self.assertEqual(parse("12:"), {})
        self.assertEqual(parse("12:    "), {})

    def test_an_empty_numbered_line_still_leaves_the_slot_open(self):
        # It sets nothing, so the sequential fill can still use bar 11.
        self.assertEqual(parse("12:\na\nb\nc"), {3: "a", 7: "b", 11: "c"})

    def test_later_pins_on_the_same_bar_win(self):
        self.assertEqual(parse("12: first\n12: second"), {11: "second"})

    def test_leading_zeros_are_read_as_decimal(self):
        self.assertEqual(parse("012: pinned"), {11: "pinned"})

    def test_a_line_starting_with_a_number_but_no_separator_is_plain(self):
        self.assertEqual(parse("1999 was a good year"), {3: "1999 was a good year"})

    def test_a_tab_is_not_a_separator_in_a_lyric_file(self):
        # The browser's "Apply numbered" box accepts [:|\t]; the file parser
        # accepts [:|] only, so this is an ordinary lyric line.
        self.assertEqual(parse("12\tnot pinned"), {3: "12\tnot pinned"})

    def test_a_negative_number_is_not_a_bar_pin(self):
        self.assertEqual(parse("-3: text"), {3: "-3: text"})

    def test_a_lyric_that_looks_like_a_bar_pin_is_taken_as_one(self):
        # Documented consequence of the format: a sung line that begins with
        # digits and a colon pins a bar instead of filling the next slot.
        self.assertEqual(parse("5: 15 miles from home"), {4: "15 miles from home"})

    def test_text_may_contain_further_colons(self):
        self.assertEqual(parse("12: a line: with a colon"), {11: "a line: with a colon"})


class MixedFileTests(unittest.TestCase):
    """A realistic file: header comments, spaced verses, one pinned line."""

    def test_a_whole_file_parses_as_expected(self):
        text = (
            "# Test Song - Nobody\n"
            "#\n"
            "# Paste the sung lines below, ONE PER LINE.\n"
            "\n"
            "# --- Verse 1 ---\n"
            "the first line\n"
            "the second line\n"
            "\n"
            "# --- Verse 2 ---\n"
            "15: pinned late\n"
            "the third line\n"
        )
        self.assertEqual(parse(text),
                         {3: "the first line", 7: "the second line",
                          11: "the third line", 14: "pinned late"})

    def test_cue_for_holds_the_last_cue_until_the_next(self):
        cues = parse("first\nsecond\nthird")
        self.assertEqual(cue_for(cues, 0), "")
        self.assertEqual(cue_for(cues, 3), "first")
        self.assertEqual(cue_for(cues, 6), "first")
        self.assertEqual(cue_for(cues, 7), "second")
        self.assertEqual(cue_for(cues, 19), "third")

    def test_result_keys_are_bar_indices_inside_the_song(self):
        cues = parse("a\nb\nc\n20: last")
        for bar in cues:
            self.assertIn(bar, range(TOTAL))


class RealSongShapeTests(unittest.TestCase):
    """The parser against the real songs' bar counts and slot maps."""

    def test_sequential_fill_uses_every_slot_of_every_song(self):
        for song_id, song in jsdata.SONGS.items():
            line_bars = jsdata.line_bars(song)
            total = len(jsdata.bars(song))
            text = "\n".join("line %d" % (i + 1) for i in range(len(line_bars)))
            cues = parse_lyric_file(text, total, line_bars)
            with self.subTest(song=song_id):
                self.assertEqual(sorted(cues), sorted(line_bars))
                self.assertEqual(len(cues), len(line_bars))

    def test_every_bar_of_every_song_can_be_pinned(self):
        for song_id, song in jsdata.SONGS.items():
            total = len(jsdata.bars(song))
            text = "\n".join("%d: bar %d" % (n, n) for n in range(1, total + 1))
            cues = parse_lyric_file(text, total, jsdata.line_bars(song))
            with self.subTest(song=song_id):
                self.assertEqual(len(cues), total)
                self.assertEqual(cues[0], "bar 1")
                self.assertEqual(cues[total - 1], "bar %d" % total)


class SourceAgreementTests(unittest.TestCase):
    """The port above must still match parseLyricFile() in app.js."""

    @classmethod
    def setUpClass(cls):
        source = jsdata.app_js_source()
        m = re.search(r"function parseLyricFile\(text\)\{(.*?)\n\}", source, re.S)
        if not m:
            raise AssertionError("parseLyricFile() is no longer in app.js")
        cls.body = m.group(1)

    def test_the_numbered_line_regex_is_the_one_we_ported(self):
        m = re.search(r"line\.match\((/.*?/)\)", self.body)
        self.assertIsNotNone(m, "no line.match(...) in parseLyricFile")
        self.assertEqual(m.group(1), r"/^(\d+)\s*[:|]\s*(.*)$/")
        self.assertEqual(NUMBERED_RE.pattern, m.group(1).strip("/"))

    def test_lines_are_split_on_optional_carriage_returns(self):
        self.assertIn(r"text.split(/\r?\n/)", self.body)

    def test_blank_and_comment_lines_are_skipped(self):
        self.assertIn("const line = raw.trim();", self.body)
        self.assertIn('if (!line || line.charAt(0) === "#") return;', self.body)

    def test_the_bar_number_guard_is_one_based_and_bounded(self):
        self.assertIn("const n = +m[1] - 1, t = m[2].trim();", self.body)
        self.assertIn("if (n >= 0 && n < TOTAL && t) out[n] = t;", self.body)

    def test_the_sequential_fill_is_capped_and_yields_to_pins(self):
        self.assertIn("plain.slice(0, LINE_BARS.length)", self.body)
        self.assertIn("if (out[LINE_BARS[i]] === undefined) out[LINE_BARS[i]] = t;", self.body)

    def test_the_bulk_paste_box_is_the_only_place_a_tab_separates(self):
        # Guards the difference test_a_tab_is_not_a_separator_in_a_lyric_file
        # documents: the two parsers really do use different separator sets.
        source = jsdata.app_js_source()
        self.assertIn(r"/^\s*(\d+)\s*[:|\t]\s*(.*)$/", source)
        self.assertNotIn(r"[:|\t]", self.body)

    def test_js_trim_strips_what_javascript_strips(self):
        self.assertEqual(js_trim("﻿ \t text  \n"), "text")
        self.assertEqual(js_trim("   "), "")


if __name__ == "__main__":
    unittest.main()
