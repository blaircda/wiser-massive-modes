"""GU5: baseline-free nonuniqueness witness for the direct closed lift at level 6.

Two positive chiral lifts of the same HFT-derived cumulative ``SO(9)`` target
are constructed without protected data.  They differ by orienting one
outer-conjugate ``D5`` parent differently.  Tensoring each lift with its outer
conjugate gives two distinct positive, outer-invariant closed characters with
the same exact ``SO(9)`` restriction.
"""

import argparse

import finite_cross_section as cross
from graded_uplift import direct_closed_low_levels as direct
from graded_uplift import iia_closed_refinement as iia


def positive_coefficients(coefficients):
    return all(value >= 0 for value in coefficients.values())


def flip_one_parent(coefficients):
    """Reverse one non-self-conjugate parent while preserving positivity."""
    candidates = sorted(
        (
            parent
            for parent, coefficient in coefficients.items()
            if coefficient > 0
            and parent != direct.outer_conjugate_label(parent)
        ),
        reverse=True,
    )
    if not candidates:
        raise ValueError("No non-self-conjugate positive parent is available")
    parent = candidates[0]
    conjugate = direct.outer_conjugate_label(parent)
    result = dict(coefficients)
    result[parent] -= 1
    if not result[parent]:
        result.pop(parent)
    result[conjugate] = result.get(conjugate, 0) + 1
    return parent, conjugate, dict(sorted(result.items()))


def run_level6(verbose=False):
    level = 6
    _single_levels, cumulative = cross.derive_cumulative_so9(level)
    target = cumulative[level]
    reference_result = cross.invert_on_cross_section(target, policy="chiral")
    reference_coefficients = {
        parent: int(coefficient)
        for parent, coefficient in reference_result["coefficients"].items()
        if coefficient
    }
    parent, conjugate, alternative_coefficients = flip_one_parent(
        reference_coefficients
    )

    reference = direct.d5_character(reference_coefficients)
    alternative = direct.d5_character(alternative_coefficients)
    kernel_difference = alternative - reference
    reference_closed = reference * iia.d5_outer_conjugate(reference)
    alternative_closed = alternative * iia.d5_outer_conjugate(alternative)
    closed_difference = alternative_closed - reference_closed
    closed_difference_table = iia.d5_coefficients(closed_difference)

    checks = {
        "reference_positive": positive_coefficients(reference_coefficients),
        "alternative_positive": positive_coefficients(alternative_coefficients),
        "reference_exact": (
            reference.branch(cross.B4, rule="default") == target
        ),
        "alternative_exact": (
            alternative.branch(cross.B4, rule="default") == target
        ),
        "kernel_restricts_zero": (
            kernel_difference.branch(cross.B4, rule="default") == cross.B4(0)
        ),
        "closed_distinct": bool(closed_difference_table),
        "closed_difference_restricts_zero": (
            closed_difference.branch(cross.B4, rule="default") == cross.B4(0)
        ),
        "closed_difference_outer_even": (
            iia.d5_outer_conjugate(closed_difference) == closed_difference
        ),
        "closed_dimensions_match": (
            reference_closed.degree() == alternative_closed.degree()
        ),
    }
    all_checks = all(checks.values())

    print("=" * 110)
    print("GU5 — DIRECT CLOSED LEVEL-6 NONUNIQUENESS WITNESS (BASELINE-FREE)")
    print("=" * 110)
    print("Protected SO(10) baseline imported: NO")
    print(f"Reference chiral lift positive/exact: {checks['reference_positive']} / {checks['reference_exact']}")
    print(f"Flipped parent: {parent} -> {conjugate}")
    print(f"Alternative chiral lift positive/exact: {checks['alternative_positive']} / {checks['alternative_exact']}")
    print(f"Chiral difference restricts to zero: {checks['kernel_restricts_zero']}")
    print()
    print("Closed candidates X=A*tau(A):")
    print(f"  distinct: {checks['closed_distinct']}")
    print(
        "  difference restricts to zero / is outer-even: "
        f"{checks['closed_difference_restricts_zero']} / "
        f"{checks['closed_difference_outer_even']}"
    )
    print(
        "  difference irreducible terms / dimension: "
        f"{len(closed_difference_table)} / {int(closed_difference.degree())}"
    )
    print(
        "Conclusion: positivity, exact restriction and closed outer invariance "
        "do not select a unique level-6 lift."
    )
    if verbose:
        print(f"Chiral kernel difference: {kernel_difference}")
        values = tuple(closed_difference_table.values())
        print(
            "Closed difference coefficient range: "
            f"[{min(values)},{max(values)}]"
        )
    print(f"GU5 direct closed checks: {'PASS' if all_checks else 'FAIL'}")
    return {
        "target": target,
        "reference": reference,
        "alternative": alternative,
        "kernel_difference": kernel_difference,
        "reference_closed": reference_closed,
        "alternative_closed": alternative_closed,
        "closed_difference": closed_difference,
        "closed_difference_table": closed_difference_table,
        "flipped_parent": (parent, conjugate),
        "checks": checks,
        "all_checks": all_checks,
    }


def run_self_test():
    coefficients = {(1, 0, 0, 0, 1): 1, (0, 0, 0, 0, 0): 2}
    parent, conjugate, flipped = flip_one_parent(coefficients)
    checks = (
        parent == (1, 0, 0, 0, 1),
        conjugate == (1, 0, 0, 1, 0),
        flipped.get(parent, 0) == 0,
        flipped.get(conjugate, 0) == 1,
        positive_coefficients(flipped),
    )
    passed = all(checks)
    print("GU5 DIRECT CLOSED LEVEL-6 SELF-TEST")
    print(f"Parent-flip checks: {'PASS' if passed else 'FAIL'}")
    print("Protected SO(10) baseline imported: NO")
    return passed


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Construct two distinct direct closed level-6 lifts"
    )
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    arguments = parser.parse_args()
    if arguments.self_test:
        raise SystemExit(0 if run_self_test() else 1)
    result = run_level6(arguments.verbose)
    raise SystemExit(0 if result["all_checks"] else 1)
