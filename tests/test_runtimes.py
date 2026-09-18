"""The arithmetic the notes state must follow from the data.

Each song's "Where this came from" note quotes a bar count and a runtime
for the one-chord-per-bar model.  Those are claims about the data in the
same file, so they can be checked:

    bars x beatsPerBar x 60 / bpm  ==  the runtime the note states

Every claim is written out with the wording it appears in, so rewording a
note without redoing the sum fails here rather than going unnoticed.
"""

import math
import unittest

import jsdata
from jsdata import SONGS

#: song id -> (bar count claimed, runtime claimed, snippet that must appear
#: verbatim in that song's notes)
RUNTIME_CLAIMS = {
    "ifiwere": (76, "2:21", "76 chords at 97 BPM comes to about <b>2:21</b>"),
    "justlikeawoman": (140, "4:52", "That comes to 140 bars, about 4:52"),
    "goaway": (95, "2:59", "That's 95 bars, about 2:59"),
    "myfavouritegame": (129, "3:36", "the 129 bars come to 3:36"),
}

#: Other countable claims the notes make in prose.
COUNT_CLAIMS = [
    # song id, what to count, expected, snippet that states it
    ("myfavouritegame", "sung lines", 31, "31 in all"),
    ("justlikeawoman", "outro bars", 11, "the outro was set to 11 bars"),
]


class RuntimeTests(unittest.TestCase):

    def test_every_song_has_a_runtime_claim_under_test(self):
        self.assertEqual(set(RUNTIME_CLAIMS), set(SONGS),
                         "a song was added or removed without updating RUNTIME_CLAIMS")

    def test_bar_count_matches_the_notes(self):
        for song_id, (claimed_bars, _, _) in RUNTIME_CLAIMS.items():
            with self.subTest(song=song_id):
                self.assertEqual(len(jsdata.bars(SONGS[song_id])), claimed_bars)

    def test_runtime_matches_the_notes(self):
        for song_id, (_, claimed_time, _) in RUNTIME_CLAIMS.items():
            with self.subTest(song=song_id):
                seconds = jsdata.runtime_seconds(SONGS[song_id])
                self.assertEqual(jsdata.mmss(seconds), claimed_time,
                                 "%d bars x %d beats at %d BPM is %.1f s"
                                 % (len(jsdata.bars(SONGS[song_id])),
                                    SONGS[song_id]["beatsPerBar"],
                                    SONGS[song_id]["bpm"], seconds))

    def test_runtime_claim_is_within_a_second_of_the_arithmetic(self):
        # m:ss is truncated, so also pin the real figure: no claim may be more
        # than a second away from bars x beats x 60 / bpm.
        for song_id, (_, claimed_time, _) in RUNTIME_CLAIMS.items():
            minutes, seconds = claimed_time.split(":")
            claimed = int(minutes) * 60 + int(seconds)
            actual = jsdata.runtime_seconds(SONGS[song_id])
            with self.subTest(song=song_id):
                self.assertLess(abs(actual - claimed), 1.0,
                                "note claims %s, arithmetic gives %.2f s"
                                % (claimed_time, actual))

    def test_the_claims_are_still_worded_that_way_in_the_notes(self):
        for song_id, (_, _, snippet) in RUNTIME_CLAIMS.items():
            with self.subTest(song=song_id):
                self.assertIn(snippet, jsdata.note_text(SONGS[song_id]),
                              "the note no longer says this; recheck the sum")

    def test_mmss_truncates(self):
        self.assertEqual(jsdata.mmss(179.99), "2:59")
        self.assertEqual(jsdata.mmss(180.0), "3:00")
        self.assertEqual(jsdata.mmss(0), "0:00")

    def test_runtime_is_seconds_per_bar_times_bars(self):
        # A second route to the same number, so a bug in runtime_seconds()
        # cannot make every claim agree with itself.
        for song_id, song in SONGS.items():
            seconds_per_bar = song["beatsPerBar"] * 60.0 / song["bpm"]
            with self.subTest(song=song_id):
                self.assertTrue(math.isclose(
                    jsdata.runtime_seconds(song),
                    seconds_per_bar * len(jsdata.bars(song))))


class CountClaimTests(unittest.TestCase):

    def test_sung_line_count_claim(self):
        song = SONGS["myfavouritegame"]
        self.assertEqual(len(jsdata.line_bars(song)), 31)
        self.assertIn("31 in all", jsdata.note_text(song))

    def test_outro_bar_count_claim(self):
        song = SONGS["justlikeawoman"]
        outro = [s for s in song["sections"] if s["name"] == "Outro"][0]
        self.assertEqual(len(jsdata.section_chords(outro)), 11)
        self.assertIn("the outro was set to 11 bars", jsdata.note_text(song))

    def test_verse_and_chorus_line_counts_claimed_for_just_like_a_woman(self):
        # "Six-line verse, four-line chorus"
        song = SONGS["justlikeawoman"]
        self.assertIn("Six-line verse, four-line chorus",
                      "\n".join(n.get("h", "") for n in song["notes"]))
        for section in song["sections"]:
            if section["name"].startswith("Verse"):
                self.assertEqual(len(section["lines"]), 6, section["name"])
            elif section["name"].startswith("Chorus"):
                self.assertEqual(len(section["lines"]), 4, section["name"])

    def test_go_away_verse_line_counts_claimed_in_the_notes(self):
        # "Verses 1 and 3 have five lines ... Verse 2 has seven shorter ones."
        song = SONGS["goaway"]
        lines = {s["name"]: len(s.get("lines", [])) for s in song["sections"]}
        self.assertEqual(lines["Verse 1"], 5)
        self.assertEqual(lines["Verse 3"], 5)
        self.assertEqual(lines["Verse 2"], 7)
        self.assertIn("<b>five</b>", jsdata.note_text(song))
        self.assertIn("<b>seven</b>", jsdata.note_text(song))

    def test_my_favourite_game_verses_stop_before_the_instrumental_riff(self):
        # "the last four bars of Verse 1 and Verse 3 are the instrumental
        # riff, not sung. That's why the cue slots stop before those sections
        # end."
        song = SONGS["myfavouritegame"]
        for name in ("Verse 1", "Verse 3"):
            section = [s for s in song["sections"] if s["name"] == name][0]
            length = len(jsdata.section_chords(section))
            with self.subTest(section=name):
                self.assertLess(max(section["lines"]), length - 4,
                                "a cue starts inside the instrumental riff")


if __name__ == "__main__":
    unittest.main()
