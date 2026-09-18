"""stepStrings() from app.js: which strings a pattern step plucks.

This is the one engine function that reads both the pattern and the chord
shape, and the only place a muted target string is recovered from.  It
cannot be executed here (no JavaScript runtime), so tests/engine.py
restates it in Python and the behaviour tests run against that port.
SourceAgreementTests asserts each rule is still written that way in
app.js, so the port cannot drift.
"""

import re
import unittest

import jsdata
from engine import diagram_base_fret, esc, sounding_strings, step_strings
from jsdata import SONGS

#: Stand-in shapes, each copied from a real one so the numbers stay honest.
E_SHAPE = {"frets": [0, 2, 2, 1, 0, 0], "fingers": [0, 2, 3, 1, 0, 0],
           "bass": 0, "alt": 1}                       # all six strings sound
DM_SHAPE = {"frets": [-1, -1, 0, 2, 3, 1], "fingers": [0, 0, 0, 2, 3, 1],
            "bass": 2}                                # top four only, no alt
POWER_SHAPE = {"frets": [2, 4, 4, -1, -1, -1], "fingers": [1, 3, 4, 0, 0, 0],
               "bass": 0, "alt": 1}                   # F#5: bottom three only
SILENT_SHAPE = {"frets": [-1, -1, -1, -1, -1, -1], "fingers": [0] * 6,
                "bass": 0}                            # nothing sounds at all
HIGH_SHAPE = {"frets": [-1, -1, 7, 5, 5, 5], "fingers": [0, 0, 3, 1, 1, 1],
              "bass": 2}                              # Am at xx7555, up the neck


class FixedStringTests(unittest.TestCase):
    """step["s"] names a string outright."""

    def test_a_sounding_string_is_plucked_as_asked(self):
        self.assertEqual(step_strings(E_SHAPE, {"s": 3, "f": "i"}), [3])

    def test_every_string_of_a_six_string_shape_can_be_asked_for(self):
        for string in range(6):
            with self.subTest(string=string):
                self.assertEqual(step_strings(E_SHAPE, {"s": string}), [string])

    def test_a_null_step_plucks_nothing(self):
        # The sparse patterns are half nulls; they must be silent, not noisy.
        self.assertEqual(step_strings(E_SHAPE, None), [])

    def test_a_step_with_no_target_string_is_rejected_by_the_port(self):
        # app.js computes NaN here and plucks a NaN frequency.  No pattern in
        # songs.js contains such a step -- test_song_data.py enforces that --
        # so the port refuses rather than imitating the NaN.
        with self.assertRaises(ValueError):
            step_strings(E_SHAPE, {"f": "p"})


class BassStringTests(unittest.TestCase):
    """step["b"] picks the chord's own thumb string."""

    def test_b1_takes_the_root_bass(self):
        self.assertEqual(step_strings(E_SHAPE, {"b": 1, "f": "p"}), [0])

    def test_b2_takes_the_alternate_bass(self):
        self.assertEqual(step_strings(E_SHAPE, {"b": 2, "f": "p"}), [1])

    def test_b2_falls_back_to_the_root_when_a_shape_has_no_alt(self):
        self.assertEqual(step_strings(DM_SHAPE, {"b": 2, "f": "p"}), [2])

    def test_an_alt_of_string_zero_is_used_not_treated_as_missing(self):
        # The low E is string 0.  A falsiness test instead of a null test
        # would silently send this thumb to the root bass.
        shape = dict(E_SHAPE, bass=1, alt=0)
        self.assertEqual(step_strings(shape, {"b": 2, "f": "p"}), [0])

    def test_a_bass_of_string_zero_is_used_not_treated_as_missing(self):
        self.assertEqual(step_strings(E_SHAPE, {"b": 1, "f": "p"}), [0])

    def test_any_other_b_value_is_not_a_bass_request(self):
        # Only 1 and 2 are bass requests; b:3 falls through to step["s"].
        self.assertEqual(step_strings(E_SHAPE, {"b": 3, "s": 4}), [4])


class MutedTargetTests(unittest.TestCase):
    """A muted target string is recovered by rank from the top."""

    def test_the_high_e_job_goes_to_the_highest_sounding_string(self):
        self.assertEqual(step_strings(POWER_SHAPE, {"s": 5, "f": "a"}), [2])

    def test_the_b_string_job_goes_to_the_next_one_down(self):
        self.assertEqual(step_strings(POWER_SHAPE, {"s": 4, "f": "m"}), [1])

    def test_the_g_string_job_goes_to_the_one_below_that(self):
        self.assertEqual(step_strings(POWER_SHAPE, {"s": 3, "f": "i"}), [0])

    def test_three_fingers_on_a_three_string_shape_land_on_three_strings(self):
        # The regression the comment in app.js records: taking the nearest
        # sounding string instead sent every finger to the same note.
        picked = [step_strings(POWER_SHAPE, {"s": s})[0] for s in (3, 4, 5)]
        self.assertEqual(sorted(picked), [0, 1, 2])
        self.assertEqual(len(set(picked)), 3)

    def test_the_rank_is_clamped_at_the_lowest_sounding_string(self):
        # A muted low E on a shape with five sounding strings ranks off the
        # bottom of the list; Math.max(0, ...) pins it to the lowest.
        shape = dict(DM_SHAPE, frets=[-1, 0, 2, 2, 1, 0], bass=1)
        self.assertEqual(step_strings(shape, {"s": 0}), [1])

    def test_a_shape_that_sounds_nothing_plucks_nothing(self):
        self.assertEqual(step_strings(SILENT_SHAPE, {"s": 5}), [])
        self.assertEqual(step_strings(SILENT_SHAPE, {"b": 1, "f": "p"}), [])

    def test_a_sounding_target_never_goes_through_the_fallback(self):
        self.assertEqual(step_strings(POWER_SHAPE, {"s": 2}), [2])


class StrumTests(unittest.TestCase):
    """step["strum"] sweeps every sounding string."""

    def test_a_downstroke_runs_low_to_high(self):
        self.assertEqual(step_strings(E_SHAPE, {"strum": "d"}), [0, 1, 2, 3, 4, 5])

    def test_an_upstroke_runs_high_to_low(self):
        self.assertEqual(step_strings(E_SHAPE, {"strum": "u"}), [5, 4, 3, 2, 1, 0])

    def test_muted_strings_are_left_out_of_a_strum(self):
        self.assertEqual(step_strings(DM_SHAPE, {"strum": "d"}), [2, 3, 4, 5])
        self.assertEqual(step_strings(DM_SHAPE, {"strum": "u"}), [5, 4, 3, 2])

    def test_a_strum_on_a_power_chord_is_three_strings(self):
        self.assertEqual(step_strings(POWER_SHAPE, {"strum": "d"}), [0, 1, 2])

    def test_a_strum_on_a_silent_shape_is_empty(self):
        self.assertEqual(step_strings(SILENT_SHAPE, {"strum": "d"}), [])
        self.assertEqual(step_strings(SILENT_SHAPE, {"strum": "u"}), [])

    def test_a_strum_ignores_any_string_or_bass_field_on_the_same_step(self):
        # The strum branch returns before either is read.
        self.assertEqual(step_strings(DM_SHAPE, {"strum": "d", "s": 0, "b": 1}),
                         [2, 3, 4, 5])

    def test_an_upstroke_does_not_disturb_the_next_downstroke(self):
        # all.reverse() reverses in place, so a shared array would corrupt it.
        step_strings(E_SHAPE, {"strum": "u"})
        self.assertEqual(step_strings(E_SHAPE, {"strum": "d"}), [0, 1, 2, 3, 4, 5])


class PinchTests(unittest.TestCase):
    """step["pinch"] adds a second string struck together with the first."""

    def test_a_pinch_adds_its_string_after_the_primary(self):
        self.assertEqual(step_strings(DM_SHAPE, {"s": 2, "f": "p", "pinch": 5}), [2, 5])

    def test_a_pinch_on_a_muted_string_is_dropped_not_recovered(self):
        # Unlike the primary, a muted pinch gets no rank fallback.
        self.assertEqual(step_strings(DM_SHAPE, {"s": 2, "f": "p", "pinch": 0}), [2])

    def test_a_pinch_of_string_zero_is_honoured_when_it_sounds(self):
        self.assertEqual(step_strings(E_SHAPE, {"s": 3, "f": "p", "pinch": 0}), [3, 0])

    def test_a_pinch_on_the_primary_string_names_it_twice(self):
        # A quirk rather than a rule: no pattern in songs.js does this, and
        # the engine would pluck the same string twice a few ms apart.
        self.assertEqual(step_strings(E_SHAPE, {"s": 3, "pinch": 3}), [3, 3])

    def test_a_pinch_survives_the_primary_falling_back(self):
        self.assertEqual(step_strings(POWER_SHAPE, {"s": 5, "pinch": 0}), [2, 0])


class RealSongTests(unittest.TestCase):
    """Every step of every pattern, against every chord it can meet."""

    def _cases(self):
        for song_id, song in SONGS.items():
            chords = sorted(set(jsdata.bars(song)))
            for pattern in song["patterns"]:
                for index, step in enumerate(pattern["steps"]):
                    for chord in chords:
                        yield song_id, pattern["name"], index, step, chord, song["shapes"][chord]

    def test_no_step_ever_plucks_a_muted_string(self):
        for song_id, pat, index, step, chord, shape in self._cases():
            for string in step_strings(shape, step):
                with self.subTest(song=song_id, pattern=pat, step=index, chord=chord):
                    self.assertGreaterEqual(
                        shape["frets"][string], 0,
                        "%s step %d plucks the muted %s string of %s"
                        % (pat, index, jsdata.STRING_NAMES[string], chord))

    def test_every_plucked_string_is_a_real_string_index(self):
        for song_id, pat, index, step, chord, shape in self._cases():
            for string in step_strings(shape, step):
                with self.subTest(song=song_id, pattern=pat, step=index, chord=chord):
                    self.assertIn(string, range(6))

    def test_every_plucked_string_has_a_row_on_the_pattern_grid(self):
        # markPattern() looks up .pg-cell[data-str="N"] and silently skips a
        # miss, so an off-grid string would be heard but never drawn.
        for song_id, song in SONGS.items():
            grid = {index for index, _ in song["gridStrings"]}
            chords = sorted(set(jsdata.bars(song)))
            for pattern in song["patterns"]:
                for index, step in enumerate(pattern["steps"]):
                    for chord in chords:
                        for string in step_strings(song["shapes"][chord], step):
                            with self.subTest(song=song_id, pattern=pattern["name"],
                                              step=index, chord=chord):
                                self.assertIn(
                                    string, grid,
                                    "%s is plucked but is not in gridStrings" %
                                    jsdata.STRING_NAMES[string])

    def test_no_step_of_any_pattern_is_silent_on_a_chord_it_meets(self):
        # A non-null step that returned [] would be a hole in the bar.
        for song_id, pat, index, step, chord, shape in self._cases():
            if step is None:
                continue
            with self.subTest(song=song_id, pattern=pat, step=index, chord=chord):
                self.assertTrue(step_strings(shape, step))

    def test_a_strum_sounds_exactly_the_strings_the_shape_sounds(self):
        for song_id, pat, index, step, chord, shape in self._cases():
            if step is None or not step.get("strum"):
                continue
            plucked = step_strings(shape, step)
            with self.subTest(song=song_id, pattern=pat, step=index, chord=chord):
                self.assertEqual(sorted(plucked), sounding_strings(shape))
                self.assertEqual(len(plucked), len(set(plucked)), "a string is struck twice")

    def test_the_power_chord_folds_the_arpeggio_onto_its_three_strings(self):
        # The one shape in the repo that forces the fallback, named outright
        # so the case does not quietly disappear if the song data changes.
        shape = SONGS["myfavouritegame"]["shapes"]["F#5"]
        self.assertEqual(sounding_strings(shape), [0, 1, 2])
        fingers = [step_strings(shape, {"s": s})[0] for s in (3, 4, 5)]
        self.assertEqual(len(set(fingers)), 3)

    def test_finger_steps_of_one_bar_stay_in_pattern_order(self):
        # i below m below a, whatever the shape mutes: the fallback ranks
        # from the top, so the contour can flatten but must never invert.
        order = {"i": 0, "m": 1, "a": 2}
        for song_id, song in SONGS.items():
            for chord, shape in song["shapes"].items():
                for pattern in song["patterns"]:
                    heights = {}
                    for step in pattern["steps"]:
                        if step is None or step.get("f") not in order:
                            continue
                        if step.get("b") or step.get("s") is None:
                            continue
                        heights.setdefault(step["f"], set()).add(
                            step_strings(shape, step)[0])
                    picked = [(order[f], min(v), max(v)) for f, v in heights.items()]
                    picked.sort()
                    for (_, _, lo_max), (_, hi_min, _) in zip(picked, picked[1:]):
                        with self.subTest(song=song_id, chord=chord,
                                          pattern=pattern["name"]):
                            self.assertLessEqual(lo_max, hi_min)


class DiagramBaseFretTests(unittest.TestCase):
    """diagram()'s `base = maxF <= NF ? 1 : minF`."""

    def test_an_open_position_shape_starts_at_the_nut(self):
        self.assertEqual(diagram_base_fret(E_SHAPE), 1)

    def test_a_shape_reaching_past_the_fourth_fret_starts_at_its_lowest(self):
        self.assertEqual(diagram_base_fret(HIGH_SHAPE), 5)

    def test_a_shape_exactly_at_the_fourth_fret_still_starts_at_the_nut(self):
        self.assertEqual(diagram_base_fret({"frets": [-1, -1, 4, 4, 4, -1]}), 1)

    def test_a_low_barre_within_four_frets_still_starts_at_the_nut(self):
        # F#5 sits at frets 2 and 4, which the nut window already covers.
        self.assertEqual(diagram_base_fret(POWER_SHAPE), 1)

    def test_an_all_open_shape_falls_back_to_the_nut(self):
        self.assertEqual(diagram_base_fret({"frets": [0, 0, 0, 0, 0, 0]}), 1)

    def test_an_all_muted_shape_falls_back_to_the_nut(self):
        self.assertEqual(diagram_base_fret(SILENT_SHAPE), 1)

    def test_open_strings_do_not_drag_the_base_down(self):
        # Am at xx7555 has open strings nowhere, but a shape that mixed them
        # must still window on its fretted notes only.
        self.assertEqual(diagram_base_fret({"frets": [-1, 0, 7, 5, 5, 5]}), 5)


class EscapeTests(unittest.TestCase):
    """esc(), which guards cue text on its way into a value="" attribute."""

    def test_the_four_characters_are_replaced(self):
        self.assertEqual(esc('&<>"'), "&amp;&lt;&gt;&quot;")

    def test_an_ampersand_is_escaped_before_the_rest(self):
        self.assertEqual(esc("<b>"), "&lt;b&gt;")
        self.assertEqual(esc("&lt;"), "&amp;lt;")

    def test_an_apostrophe_is_left_alone(self):
        # Deliberate: every attribute app.js builds is double-quoted.
        self.assertEqual(esc("it's"), "it's")

    def test_a_quote_cannot_close_the_attribute_it_sits_in(self):
        self.assertNotIn('"', esc('" onfocus="alert(1)'))

    def test_ordinary_lyric_text_passes_through_unchanged(self):
        self.assertEqual(esc("she takes just like a woman"),
                         "she takes just like a woman")

    def test_an_empty_string_stays_empty(self):
        self.assertEqual(esc(""), "")

    def test_non_strings_are_stringified_first(self):
        self.assertEqual(esc(12), "12")


class SourceAgreementTests(unittest.TestCase):
    """The ports above must still match the functions in app.js."""

    @classmethod
    def setUpClass(cls):
        cls.source = jsdata.app_js_source()
        m = re.search(r"function stepStrings\(shape, st\)\{(.*?)\n\}", cls.source, re.S)
        if not m:
            raise AssertionError("stepStrings() is no longer in app.js")
        cls.body = m.group(1)

    def test_a_null_step_still_returns_nothing(self):
        self.assertIn("if (!st) return [];", self.body)

    def test_the_strum_branch_still_collects_every_sounding_string(self):
        self.assertIn("shape.frets.forEach((f, i) => { if (f >= 0) all.push(i); });",
                      self.body)
        self.assertIn('return st.strum === "u" ? all.reverse() : all;', self.body)

    def test_the_primary_string_is_still_chosen_the_same_way(self):
        self.assertIn("st.b === 2 ? (shape.alt != null ? shape.alt : shape.bass)",
                      self.body)
        self.assertIn(": st.b === 1 ? shape.bass", self.body)
        self.assertIn(": st.s;", self.body)

    def test_the_alt_bass_is_still_tested_against_null_not_falsiness(self):
        # Guards test_an_alt_of_string_zero_is_used_not_treated_as_missing.
        self.assertIn("shape.alt != null", self.body)
        self.assertNotIn("shape.alt ||", self.body)

    def test_a_sounding_primary_is_still_taken_directly(self):
        self.assertIn("if (shape.frets[primary] >= 0) out.push(primary);", self.body)

    def test_the_fallback_still_ranks_from_the_top_and_clamps(self):
        self.assertIn("const fromTop = 5 - primary;", self.body)
        self.assertIn(
            "if (sounding.length) out.push(sounding[Math.max(0, sounding.length - 1 - fromTop)]);",
            self.body)

    def test_the_pinch_is_still_added_only_when_it_sounds(self):
        self.assertIn(
            "if (st.pinch != null && shape.frets[st.pinch] >= 0) out.push(st.pinch);",
            self.body)

    def test_esc_still_replaces_the_four_characters_we_ported(self):
        self.assertIn(r'String(t).replace(/[&<>"]/g', self.source)
        for char, entity in (("&", "&amp;"), ("<", "&lt;"),
                             (">", "&gt;"), ('"', "&quot;")):
            with self.subTest(char=char):
                self.assertIn('"%s":"%s"' % (char, entity),
                              self.source.replace(" ", "").replace("'", '"'))

    def test_the_diagram_base_fret_rule_is_the_one_we_ported(self):
        self.assertIn("const base = maxF <= NF ? 1 : minF;", self.source)
        self.assertIn("NF = 4", self.source)


if __name__ == "__main__":
    unittest.main()
