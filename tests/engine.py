"""Pure engine helpers from app.js, restated in Python.

There is no JavaScript runtime in this project's toolchain, so the
functions in app.js cannot be executed here.  This module ports the pure
ones the tests need -- stepStrings() and esc() -- written to match the
JavaScript exactly, quirks included.  test_step_strings.py pulls the
originals out of app.js and asserts they are still written the same way,
so the ports cannot drift away from the code they stand in for.

Follows the same arrangement as lyricfile.py, which ports parseLyricFile().
"""

import re

#: diagram() draws this many fret spaces.
NF = 4

#: Strings are indexed 0..5 = low E .. high e.
LAST_STRING = 5

_ESC_MAP = {"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"}


def esc(text):
    """app.js's esc(): the four characters it replaces, and no others.

    Note that the apostrophe is deliberately not escaped -- every
    attribute app.js builds is double-quoted.
    """
    return re.sub(r'[&<>"]', lambda m: _ESC_MAP[m.group(0)], str(text))


def sounding_strings(shape):
    """The string indices a shape actually sounds, lowest first."""
    return [i for i, fret in enumerate(shape["frets"]) if fret >= 0]


def step_strings(shape, step):
    """Port of stepStrings(shape, st) from app.js.

    Which strings one pattern step plucks on a given chord shape:
    step["b"] == 1 -> the chord's root bass, 2 -> its alternate bass,
    step["s"] -> a fixed string index, step["strum"] -> the whole chord.

    A step carrying none of `b`, `s` or `strum` has no target string.  The
    JavaScript quietly computes NaN for it and plucks a NaN frequency; no
    pattern in songs.js contains such a step, and rather than reproduce
    that, this port raises so a test can state the rule out loud.
    """
    if step is None:
        return []

    if step.get("strum"):
        every = sounding_strings(shape)
        return list(reversed(every)) if step["strum"] == "u" else every

    out = []
    if step.get("b") == 2:
        # `shape.alt != null ? shape.alt : shape.bass` -- string 0 is a
        # legitimate alternate bass, so this test is against null, not
        # against falsiness.
        primary = shape["alt"] if shape.get("alt") is not None else shape["bass"]
    elif step.get("b") == 1:
        primary = shape["bass"]
    else:
        primary = step.get("s")

    if primary is None:
        raise ValueError("a pattern step needs one of 'b', 's' or 'strum'")

    if shape["frets"][primary] >= 0:
        out.append(primary)
    else:
        # The target string is muted in this shape.  Keep the pattern's
        # contour by rank rather than by nearest string.
        sounding = sounding_strings(shape)
        from_top = LAST_STRING - primary
        if sounding:
            out.append(sounding[max(0, len(sounding) - 1 - from_top)])

    pinch = step.get("pinch")
    if pinch is not None and shape["frets"][pinch] >= 0:
        out.append(pinch)
    return out


def diagram_base_fret(shape):
    """The fret diagram() puts at the top of the grid.

    `base = maxF <= NF ? 1 : minF`, with an all-open or all-muted shape
    falling back to 1.
    """
    fretted = [f for f in shape["frets"] if f > 0]
    if not fretted:
        return 1
    return 1 if max(fretted) <= NF else min(fretted)
