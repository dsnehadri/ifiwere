"""What a chord name means, in pitch classes.

Used to check that every shape in songs.js spells the chord it is named
for.  Unknown roots or qualities raise, so adding a chord name the tests
have never seen is a test failure rather than a silent pass.
"""

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

_ROOTS = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}

#: Intervals above the root, in semitones.
QUALITIES = {
    "": (0, 4, 7),            # major triad
    "m": (0, 3, 7),           # minor triad
    "5": (0, 7),              # power chord: root and fifth, no third
    "6": (0, 4, 7, 9),
    "7": (0, 4, 7, 10),       # dominant seventh
    "m7": (0, 3, 7, 10),
    "maj7": (0, 4, 7, 11),
    "dim": (0, 3, 6),
    "aug": (0, 4, 8),
    "sus2": (0, 2, 7),
    "sus4": (0, 5, 7),        # no third at all
    "add4": (0, 4, 5, 7),
    "add9": (0, 2, 4, 7),
}


class UnknownChordName(Exception):
    pass


def split_name(name):
    """('F#m') -> ('F#', 'm'). Slash chords keep only the part before '/'."""
    head = name.split("/")[0]
    if not head or head[0] not in _ROOTS:
        raise UnknownChordName("no note name at the start of %r" % name)
    root = head[0]
    rest = head[1:]
    if rest[:1] in ("#", "b"):
        root += rest[0]
        rest = rest[1:]
    return root, rest


def root_pitch_class(root):
    pc = _ROOTS[root[0]]
    if root[1:] == "#":
        pc += 1
    elif root[1:] == "b":
        pc -= 1
    return pc % 12


def expected_pitch_classes(name):
    """The pitch classes a chord name calls for."""
    root, quality = split_name(name)
    if quality not in QUALITIES:
        raise UnknownChordName(
            "chord quality %r in %r is not in QUALITIES -- add it to "
            "tests/chordnames.py once you know what it should spell" % (quality, name))
    base = root_pitch_class(root)
    return {(base + step) % 12 for step in QUALITIES[quality]}


def spell(pitch_classes):
    """A sorted, readable note-name list for assertion messages."""
    return [NOTE_NAMES[pc] for pc in sorted(pitch_classes)]
