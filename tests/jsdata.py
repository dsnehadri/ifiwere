"""Read the repo's JavaScript data files from Python.

There is no Node on this machine, so the tests cannot execute songs.js or
app.js.  Instead this module parses the small subset of JavaScript those
files use for data -- object and array literals of strings, numbers,
null/true/false, with bare or quoted keys and /* */ or // comments.

Nothing here modifies the sources; it only reads them.
"""

import os
import re

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SONGS_JS = os.path.join(REPO_ROOT, "songs.js")
APP_JS = os.path.join(REPO_ROOT, "app.js")
LYRICS_DIR = os.path.join(REPO_ROOT, "lyrics")


class JsParseError(Exception):
    """Raised when songs.js does not look the way this reader expects."""


_SKIP = re.compile(r"(?:\s+|/\*.*?\*/|//[^\n]*)*", re.S)
_NUMBER = re.compile(r"-?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][+-]?\d+)?")
_IDENT = re.compile(r"[A-Za-z_$][A-Za-z0-9_$]*")
_ESCAPES = {"n": "\n", "t": "\t", "r": "\r", "b": "\b", "f": "\f", "v": "\v", "0": "\0"}


def _skip(src, i):
    return _SKIP.match(src, i).end()


def _parse_string(src, i):
    quote = src[i]
    i += 1
    out = []
    while True:
        if i >= len(src):
            raise JsParseError("unterminated string literal")
        c = src[i]
        if c == "\\":
            nxt = src[i + 1]
            if nxt == "u":
                out.append(chr(int(src[i + 2:i + 6], 16)))
                i += 6
            elif nxt == "x":
                out.append(chr(int(src[i + 2:i + 4], 16)))
                i += 4
            else:
                out.append(_ESCAPES.get(nxt, nxt))
                i += 2
        elif c == quote:
            return "".join(out), i + 1
        else:
            out.append(c)
            i += 1


def _parse_array(src, i):
    i = _skip(src, i + 1)
    out = []
    while src[i] != "]":
        value, i = _parse_value(src, i)
        out.append(value)
        i = _skip(src, i)
        if src[i] == ",":
            i = _skip(src, i + 1)
    return out, i + 1


def _parse_object(src, i):
    i = _skip(src, i + 1)
    out = {}
    while src[i] != "}":
        if src[i] in "\"'":
            key, i = _parse_string(src, i)
        else:
            m = _IDENT.match(src, i)
            if not m:
                raise JsParseError("expected a property name at offset %d" % i)
            key, i = m.group(0), m.end()
        i = _skip(src, i)
        if src[i] != ":":
            raise JsParseError("expected ':' after %r at offset %d" % (key, i))
        value, i = _parse_value(src, _skip(src, i + 1))
        out[key] = value
        i = _skip(src, i)
        if src[i] == ",":
            i = _skip(src, i + 1)
    return out, i + 1


def _parse_value(src, i):
    i = _skip(src, i)
    c = src[i]
    if c == "{":
        return _parse_object(src, i)
    if c == "[":
        return _parse_array(src, i)
    if c in "\"'":
        return _parse_string(src, i)
    for word, value in (("true", True), ("false", False), ("null", None), ("undefined", None)):
        if src.startswith(word, i):
            return value, i + len(word)
    m = _NUMBER.match(src, i)
    if not m:
        raise JsParseError("cannot parse a value at offset %d: %r" % (i, src[i:i + 20]))
    text = m.group(0)
    number = float(text) if ("." in text or "e" in text or "E" in text) else int(text)
    return number, m.end()


def read_js_const(src, name):
    """Return the literal assigned to `const <name> = ...` in `src`."""
    m = re.search(r"\bconst\s+" + re.escape(name) + r"\s*=", src)
    if not m:
        raise JsParseError("no `const %s =` in the source" % name)
    value, _ = _parse_value(src, m.end())
    return value


def _read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def songs_js_source():
    return _read(SONGS_JS)


def app_js_source():
    return _read(APP_JS)


def load_songs():
    """(OPEN_MIDI, SONGS) exactly as songs.js declares them."""
    src = songs_js_source()
    return read_js_const(src, "OPEN_MIDI"), read_js_const(src, "SONGS")


OPEN_MIDI, SONGS = load_songs()

#: gridStrings pairs are [string index, label]; the engine indexes strings
#: 0..5 = low E .. high e, exactly as songs.js documents.
STRING_NAMES = ["E", "A", "D", "G", "B", "e"]


def bars(song):
    """The flat bar list loadSong() builds: one chord name per bar."""
    out = []
    for section in song["sections"]:
        out.extend(section_chords(section))
    return out


def section_chords(section):
    """A section's chords as a list, the way loadSong() splits the string."""
    chords = section["chords"]
    if isinstance(chords, str):
        return chords.strip().split()
    return list(chords)


def section_bounds(song):
    """{section name: (start, end)} in flat bar indices, as loadSong() sets them."""
    out = {}
    start = 0
    for section in song["sections"]:
        end = start + len(section_chords(section))
        out[section["name"]] = (start, end)
        start = end
    return out


def line_bars(song):
    """LINE_BARS: flat 0-based bar index of every sung line, in order."""
    out = []
    start = 0
    for section in song["sections"]:
        chords = section_chords(section)
        for offset in section.get("lines", []):
            out.append(start + offset)
        start += len(chords)
    return out


def runtime_seconds(song):
    """bars x beatsPerBar x 60 / bpm -- the model the notes quote."""
    return len(bars(song)) * song["beatsPerBar"] * 60.0 / song["bpm"]


def mmss(seconds):
    """Seconds as m:ss, truncated -- the rounding the notes' figures use."""
    total = int(seconds)
    return "%d:%02d" % (total // 60, total % 60)


def note_text(song):
    """Every note heading and body of a song, joined, for claim checks."""
    return "\n".join(n.get("h", "") + "\n" + n.get("body", "") for n in song["notes"])


def sounding_midi(shape, string, capo=0):
    """MIDI note a string sounds in this shape, or None when muted."""
    fret = shape["frets"][string]
    if fret < 0:
        return None
    return OPEN_MIDI[string] + fret + capo


def pitch_classes(shape):
    """The set of pitch classes (0..11) a shape sounds.

    Capo is left out on purpose: a capo transposes every string equally, so
    it cannot change whether a shape spells the chord it is named for.
    """
    out = set()
    for string in range(len(shape["frets"])):
        midi = sounding_midi(shape, string)
        if midi is not None:
            out.add(midi % 12)
    return out
