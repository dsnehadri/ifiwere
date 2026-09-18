"""A Python port of parseLyricFile() from app.js.

There is no JavaScript runtime here, so the parsing rules are re-stated in
Python and exercised directly.  test_parse_lyric_file.py keeps the port
honest: it pulls the real function out of app.js and asserts that every
rule below still appears there verbatim, so the port cannot quietly drift
away from the code it stands in for.

The rules, from app.js:

  * the file is split on /\\r?\\n/;
  * each line is trimmed; empty lines and lines starting with "#" are dropped;
  * a line matching /^(\\d+)\\s*[:|]\\s*(.*)$/ pins bar N (1-based) to the
    trimmed text, but only when 0 <= N-1 < TOTAL and the text is non-empty;
  * every other line is "plain" and fills the sung-line slots (LINE_BARS)
    in order, at most one per slot;
  * a pinned bar wins: a plain line whose slot is already pinned is dropped,
    and the remaining plain lines keep their own slots.
"""

import re

#: The separator class app.js uses.  Note it is [:|] -- a colon or a pipe,
#: not a tab (the bulk-paste box in the browser also accepts a tab).
NUMBERED_RE = re.compile(r"^(\d+)\s*[:|]\s*(.*)$")

#: What JavaScript's String.prototype.trim() strips: WhiteSpace plus
#: LineTerminator plus U+FEFF.  Python's str.strip() leaves U+FEFF alone,
#: so a byte-order mark would be handled differently if we used it.
JS_WHITESPACE = (
    "\t\n\v\f\r           "
    "       　﻿"
)


def js_trim(text):
    return text.strip(JS_WHITESPACE)


def parse_lyric_file(text, total, line_bars):
    """parseLyricFile(text) with TOTAL and LINE_BARS passed in explicitly.

    Returns {0-based bar index: cue text}, the same shape as `cues`.
    """
    out = {}
    plain = []
    for raw in re.split(r"\r?\n", text):
        line = js_trim(raw)
        if not line or line[0] == "#":
            continue
        m = NUMBERED_RE.match(line)
        if m:
            n = int(m.group(1)) - 1
            t = js_trim(m.group(2))
            if 0 <= n < total and t:
                out[n] = t
        else:
            plain.append(line)
    for i, t in enumerate(plain[:len(line_bars)]):
        if line_bars[i] not in out:
            out[line_bars[i]] = t
    return out


def cue_for(cues, idx):
    """cueFor(idx): the most recent cue at or before this bar."""
    for i in range(idx, -1, -1):
        if cues.get(i):
            return cues[i]
    return ""
