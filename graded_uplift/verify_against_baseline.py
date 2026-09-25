"""Compare the independent Appendix-B graded lift with the protected baseline.

This is a comparison layer only.  It deliberately imports the protected
``massive_SO10.py`` data and must never be used by derivation modules.
"""

import argparse

from massive_SO10 import get_so10_character

from graded_uplift import verify_paper_grading


def coefficient_table(character):
    result = {}
    for weight, coefficient in character.monomial_coefficients().items():
        coordinates = weight.to_vector()
        x1, x2, x3, x4, x5 = coordinates
        label = (
            int(x1 - x2),
            int(x2 - x3),
            int(x3 - x4),
            int(x4 - x5),
            int(x4 + x5),
        )
        result[label] = int(coefficient)
    return dict(sorted(result.items()))


def sparse_difference(left, right):
    keys = set(left) | set(right)
    return {
        key: left.get(key, 0) - right.get(key, 0)
        for key in sorted(keys)
        if left.get(key, 0) != right.get(key, 0)
    }


def run_comparison(max_level=7, verbose=False):
    result = verify_paper_grading.run_audit(max_level=max_level, verbose=False)
    matches = {}
    differences = {}
    for level in range(1, max_level + 1):
        protected = coefficient_table(get_so10_character(level))
        candidate = result["cumulative"][level]
        differences[level] = sparse_difference(candidate, protected)
        matches[level] = not differences[level]
        print(
            f"n={level}: paper-graded cumulative lift equals protected Bars lift: "
            f"{matches[level]}"
        )
        if verbose and differences[level]:
            print(f"  candidate - protected: {differences[level]}")
    first_mismatch = next(
        (level for level in range(1, max_level + 1) if not matches[level]),
        None,
    )
    print(f"First mismatch: {first_mismatch}")
    print("Protected baseline imported: YES, comparison only")
    return {
        "candidate": result,
        "matches": matches,
        "differences": differences,
        "first_mismatch": first_mismatch,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compare the paper-graded lift with the protected Bars completion"
    )
    parser.add_argument("--max-level", type=int, default=7)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    run_comparison(args.max_level, args.verbose)
