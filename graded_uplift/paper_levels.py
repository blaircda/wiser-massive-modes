"""Structured transcription of hep-th/0310292 Appendix B, levels 1--7.

This is external literature input, not a derived result.  Each entry is
``(2 Delta, multiplicity, D5 Dynkin label, starred)``.  The paper defines the
ungraded virtual character

    [k,l,m,p,q]* = [k,l,m,p,q] - [k-1,l,m,p,q].

In the graded table the predecessor saturates a bound one unit higher, so an
entry displayed at Delta expands as

    [k,...]_Delta - [k-1,...]_(Delta+1).

Only levels 1--7 are transcribed for the first graded-uplift audit.  Extending
the transcription must remain a verification layer; derivation code must not
look up this table.
"""


PAPER_LEVELS = {
    1: ((2, 1, (0, 0, 0, 0, 0), False),),
    2: ((4, 1, (1, 0, 0, 0, 0), True),),
    3: (
        (6, 1, (2, 0, 0, 0, 0), True),
        (5, 1, (0, 0, 0, 0, 1), False),
    ),
    4: (
        (8, 1, (3, 0, 0, 0, 0), True),
        (7, 1, (1, 0, 0, 0, 1), True),
        (6, 1, (0, 1, 0, 0, 0), False),
    ),
    5: (
        (10, 1, (4, 0, 0, 0, 0), True),
        (9, 1, (2, 0, 0, 0, 1), True),
        (8, 1, (0, 0, 1, 0, 0), False),
        (8, 1, (1, 1, 0, 0, 0), True),
        (7, 1, (1, 0, 0, 0, 1), False),
        (6, 1, (0, 0, 0, 0, 0), False),
    ),
    6: (
        (12, 1, (5, 0, 0, 0, 0), True),
        (11, 1, (3, 0, 0, 0, 1), True),
        (10, 1, (1, 0, 1, 0, 0), True),
        (10, 1, (2, 1, 0, 0, 0), True),
        (9, 1, (0, 1, 0, 0, 1), False),
        (9, 1, (1, 0, 0, 1, 0), False),
        (9, 1, (2, 0, 0, 0, 1), True),
        (8, 1, (0, 0, 0, 0, 2), False),
        (8, 1, (1, 0, 0, 0, 0), True),
        (8, 1, (1, 1, 0, 0, 0), False),
        (7, 1, (0, 0, 0, 1, 0), False),
    ),
    7: (
        (14, 1, (6, 0, 0, 0, 0), True),
        (13, 1, (4, 0, 0, 0, 1), True),
        (12, 1, (2, 0, 1, 0, 0), True),
        (12, 1, (3, 1, 0, 0, 0), True),
        (11, 1, (0, 1, 0, 1, 0), False),
        (11, 1, (1, 1, 0, 0, 1), True),
        (11, 1, (2, 0, 0, 1, 0), True),
        (11, 1, (3, 0, 0, 0, 1), True),
        (10, 1, (0, 0, 0, 1, 1), False),
        (10, 1, (0, 2, 0, 0, 0), False),
        (10, 1, (1, 0, 0, 0, 2), True),
        (10, 1, (1, 0, 1, 0, 0), False),
        (10, 1, (2, 0, 0, 0, 0), False),
        (10, 1, (2, 0, 0, 0, 0), True),
        (10, 1, (2, 1, 0, 0, 0), True),
        (9, 1, (0, 0, 0, 0, 1), False),
        (9, 1, (0, 1, 0, 0, 1), False),
        (9, 1, (1, 0, 0, 1, 0), True),
        (9, 1, (2, 0, 0, 0, 1), False),
        (8, 1, (0, 0, 1, 0, 0), False),
        (8, 1, (1, 0, 0, 0, 0), False),
    ),
}


def expanded_terms(level):
    result = []
    for twice_delta, multiplicity, label, starred in PAPER_LEVELS[level]:
        result.append((twice_delta, multiplicity, label))
        if starred:
            if label[0] <= 0:
                raise ValueError(f"Invalid starred label: {label}")
            predecessor = (label[0] - 1,) + label[1:]
            result.append((twice_delta + 2, -multiplicity, predecessor))
    return tuple(result)
