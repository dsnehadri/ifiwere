"""The contract between app.js and index.html.

app.js reaches into the page by id and by class and never checks that
what it asked for came back: `$("play").innerHTML = ...` on a missing
element throws, and `querySelectorAll` on a class the stylesheet forgot
fails silently and leaves the marker invisible.  Nothing else in the
suite would notice either, so these tests hold the two files together.
"""

import re
import unittest

import jsdata

APP = jsdata.app_js_source()

with open(jsdata.os.path.join(jsdata.REPO_ROOT, "index.html"), encoding="utf-8") as _fh:
    HTML = _fh.read()

#: Every `$("...")` lookup app.js performs.
LOOKED_UP = sorted(set(re.findall(r'\$\("([^"]+)"\)', APP)))

#: Every id written into the static page.
IN_PAGE = sorted(set(re.findall(r'\bid="([^"]+)"', HTML)))

#: Every id app.js builds at runtime, in the cue-editing panel.
BUILT_BY_APP = sorted(set(re.findall(r'\bid="([^"]+)"', APP)))

_STYLE = re.search(r"<style>(.*?)</style>", HTML, re.S)
CSS = _STYLE.group(1) if _STYLE else ""


class LookupTests(unittest.TestCase):
    """Every id app.js asks for exists somewhere."""

    def test_app_js_looks_elements_up_at_all(self):
        self.assertTrue(LOOKED_UP, "no $(\"...\") lookups found -- has app.js changed shape?")

    def test_every_id_app_js_asks_for_exists(self):
        known = set(IN_PAGE) | set(BUILT_BY_APP)
        for name in LOOKED_UP:
            with self.subTest(id=name):
                self.assertIn(name, known,
                              "$(\"%s\") has nothing to find" % name)

    def test_every_id_in_the_page_is_actually_used(self):
        # Dead markup: an element with an id nothing reaches for.
        for name in IN_PAGE:
            with self.subTest(id=name):
                self.assertIn(name, LOOKED_UP,
                              'id="%s" is in index.html but nothing uses it' % name)

    def test_the_cue_editor_ids_come_from_app_js_not_the_page(self):
        # They only exist while the editor is open, which is why bindTimeline()
        # bails out with `if (!bt) return;` when it cannot find the textarea.
        for name in ("bulkText", "bulkMsg", "bulkAlign", "bulkApply",
                     "bulkLoad", "bulkClear"):
            with self.subTest(id=name):
                self.assertIn(name, BUILT_BY_APP)
                self.assertNotIn(name, IN_PAGE)

    def test_bind_timeline_guards_against_the_editor_being_closed(self):
        self.assertIn('const bt = $("bulkText");', APP)
        self.assertIn("if (!bt) return;", APP)

    def test_no_id_is_declared_twice_in_the_page(self):
        declared = re.findall(r'\bid="([^"]+)"', HTML)
        self.assertEqual(len(declared), len(set(declared)),
                         "duplicate id in index.html")


class ScriptOrderTests(unittest.TestCase):
    """app.js reads SONGS while it loads, so songs.js must come first."""

    def test_both_scripts_are_included(self):
        self.assertIn('<script src="songs.js"></script>', HTML)
        self.assertIn('<script src="app.js"></script>', HTML)

    def test_songs_js_is_loaded_before_app_js(self):
        self.assertLess(HTML.index('src="songs.js"'), HTML.index('src="app.js"'))

    def test_app_js_uses_songs_at_load_time(self):
        # This is what makes the order matter rather than being a preference.
        self.assertIn("loadSong(Object.keys(SONGS)[0]);", APP)

    def test_neither_script_is_deferred_out_of_order(self):
        # `defer` on one but not the other would reverse the order above.
        for tag in re.findall(r"<script[^>]*>", HTML):
            with self.subTest(tag=tag):
                self.assertNotIn("defer", tag)
                self.assertNotIn("async", tag)


class ClassContractTests(unittest.TestCase):
    """Every class app.js toggles is one the stylesheet draws."""

    #: class -> a selector the stylesheet must contain for it to be visible.
    STYLED = {
        "on": [".dot.on", ".countin.on", ".btn.on"],
        "down": [".dot.on.down"],
        "active": [".pg-cell.active"],
        "cur": [".chip.cur", ".cc.cur"],
        "done": [".chip.done"],
        "hit": [".pg-cell.hit"],
        "thumb": [".pg-cell.hit.thumb"],
    }

    def test_the_stylesheet_was_found(self):
        self.assertTrue(CSS.strip(), "no <style> block in index.html")

    def test_every_toggled_class_has_a_rule(self):
        toggled = set(re.findall(r'classList\.(?:add|remove|toggle)\("([^"]+)"',
                                 APP))
        toggled |= set(re.findall(r'classList\.remove\("[^"]+","([^"]+)"', APP))
        self.assertTrue(toggled, "no classList calls found in app.js")
        for name in sorted(toggled):
            with self.subTest(cls=name):
                self.assertIn(name, self.STYLED,
                              "app.js toggles .%s but this test does not know it" % name)
                for selector in self.STYLED[name]:
                    self.assertIn(selector, CSS,
                                  "%s is not styled in index.html" % selector)

    def test_classes_queried_for_are_ones_app_js_or_the_page_creates(self):
        # app.js builds class lists by concatenation -- `class="dot' + ... ` --
        # so read only as far as the first quote of either kind.
        made = set()
        for value in re.findall(r'class="([^"\']*)', APP + HTML):
            made.update(value.split())
        for selector in re.findall(r'querySelectorAll?\("\.([a-z-]+)', APP):
            with self.subTest(selector=selector):
                self.assertIn(selector, made,
                              ".%s is queried but never created" % selector)

    def test_the_count_in_pip_classes_match_the_stylesheet(self):
        self.assertIn('class="pip', APP)
        self.assertIn(".countin .pip", CSS)
        self.assertIn(".countin .pip.lit", CSS)

    def test_the_section_kinds_the_timeline_tags_are_styled(self):
        self.assertIn('/chorus/i.test(s.name) ? " chorus"', APP)
        self.assertIn('/bridge/i.test(s.name) ? " bridge"', APP)
        self.assertIn(".tl-sec.chorus", CSS)
        self.assertIn(".tl-sec.bridge", CSS)


class DataAttributeTests(unittest.TestCase):
    """The data-* attributes app.js writes and then reads back."""

    def test_every_data_attribute_read_is_also_written(self):
        written = set(re.findall(r'data-([a-z]+)="', APP))
        for name in ("i", "loop", "chord", "step", "str", "cue"):
            with self.subTest(attribute=name):
                self.assertIn(name, written)

    def test_the_pattern_grid_rows_are_keyed_by_string_index(self):
        # markPattern() matches these against the numbers stepStrings() returns.
        self.assertIn('data-str="\' + pair[0] + \'"', APP)
        self.assertIn("SONG.gridStrings.forEach(pair =>", APP)

    def test_a_missing_grid_cell_is_skipped_rather_than_crashing(self):
        self.assertIn("if (!cell) return;", APP)


class EscapingTests(unittest.TestCase):
    """Cue text is the only untrusted string that reaches innerHTML."""

    def test_cue_text_is_escaped_on_its_way_into_an_attribute(self):
        self.assertIn('value="\' +\n          esc(cues[gi] || "")', APP)

    def test_every_html_line_that_interpolates_a_cue_escapes_it(self):
        for line in APP.splitlines():
            if "cues[" in line and "'<" in line:
                with self.subTest(line=line.strip()):
                    self.assertIn("esc(", line)

    def test_the_cue_shown_on_the_now_panel_is_set_as_text_not_html(self):
        self.assertIn('$("nowCue").textContent = cueFor(idx);', APP)
        self.assertNotIn('$("nowCue").innerHTML', APP)

    def test_the_bulk_message_is_set_as_text_not_html(self):
        self.assertNotIn('$("bulkMsg").innerHTML', APP)


if __name__ == "__main__":
    unittest.main()
