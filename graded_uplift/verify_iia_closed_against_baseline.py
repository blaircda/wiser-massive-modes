"""GU3 protected comparison of the IIA closed candidate with Bars.

The construction is performed in ``iia_closed_refinement.py`` without access
to the protected completion.  This module imports ``massive_SO10.py`` only to
compare the resulting cumulative closed character with the Bars target.
"""

import argparse

import hft_so9
from massive_SO10 import get_so10_character

from graded_uplift import iia_closed_refinement
from graded_uplift import verify_against_baseline
from graded_uplift import verify_paper_grading


def bars_character(level):
    return iia_closed_refinement.d5_character(
        verify_against_baseline.coefficient_table(
            get_so10_character(level)
        )
    )


def positive_character(character):
    return all(
        coefficient >= 0
        for coefficient in iia_closed_refinement.d5_coefficients(character).values()
    )


def run_comparison(max_level=7, verbose=False):
    if max_level < 1 or max_level > 7:
        raise ValueError("GU3 comparison currently covers levels 1--7")
    cumulative = verify_paper_grading.cumulative_ungraded_coefficients(max_level)
    results = {}

    print("=" * 116)
    print("GU3 — PROTECTED COMPARISON OF TYPE-IIA CLOSED CANDIDATES")
    print("=" * 116)
    print(
        " level | chiral paper=Bars | IIA closed paper=Bars | "
        "difference restricts zero | outer invariant | difference terms"
    )
    for level in range(1, max_level + 1):
        paper = iia_closed_refinement.d5_character(cumulative[level])
        bars = bars_character(level)
        chiral_equal = paper == bars
        kernel_difference = paper - bars
        kernel_restricts_zero = (
            kernel_difference.branch(hft_so9.B4, rule="default")
            == hft_so9.B4(0)
        )
        kernel_outer_odd = (
            iia_closed_refinement.d5_outer_conjugate(kernel_difference)
            == -kernel_difference
        )

        paper_closed = paper * iia_closed_refinement.d5_outer_conjugate(paper)
        bars_closed = bars * iia_closed_refinement.d5_outer_conjugate(bars)
        closed_difference = paper_closed - bars_closed
        difference_table = iia_closed_refinement.d5_coefficients(closed_difference)
        closed_equal = not difference_table
        restriction_exact = (
            closed_difference.branch(hft_so9.B4, rule="default")
            == hft_so9.B4(0)
        )
        outer_invariant = (
            iia_closed_refinement.d5_outer_conjugate(closed_difference)
            == closed_difference
        )
        factor_identity = (
            closed_difference
            == kernel_difference
            * (iia_closed_refinement.d5_outer_conjugate(paper) - bars)
        )
        results[level] = {
            "paper": paper,
            "bars": bars,
            "chiral_equal": chiral_equal,
            "kernel_restricts_zero": kernel_restricts_zero,
            "kernel_outer_odd": kernel_outer_odd,
            "paper_positive": positive_character(paper),
            "bars_positive": positive_character(bars),
            "paper_closed": paper_closed,
            "bars_closed": bars_closed,
            "closed_equal": closed_equal,
            "closed_difference": closed_difference,
            "difference_table": difference_table,
            "restriction_exact": restriction_exact,
            "outer_invariant": outer_invariant,
            "factor_identity": factor_identity,
        }
        print(
            f" {level:5d} | {str(chiral_equal):>17s} | "
            f"{str(closed_equal):>22s} | {str(restriction_exact):>25s} | "
            f"{str(outer_invariant):>15s} | {len(difference_table):>16d}"
        )
        if verbose and difference_table:
            values = tuple(difference_table.values())
            print(
                "         difference coefficient range / dimension: "
                f"[{min(values)},{max(values)}] / {int(closed_difference.degree())}"
            )
            print(
                "         chiral kernel outer-odd / closed factor identity: "
                f"{kernel_outer_odd} / {factor_identity}"
            )

    first_closed_mismatch = next(
        (
            level
            for level, result in results.items()
            if not result["closed_equal"]
        ),
        None,
    )
    all_checks = all(
        result["paper_positive"]
        and result["bars_positive"]
        and result["kernel_restricts_zero"]
        and result["restriction_exact"]
        and result["outer_invariant"]
        and result["factor_identity"]
        for result in results.values()
    )
    print("-" * 116)
    print(f"First IIA closed mismatch: {first_closed_mismatch}")
    print("Both candidates are positive and have the same closed SO(9) restriction")
    print("Protected Bars completion imported: YES, comparison only")
    print(f"GU3 protected consistency checks: {'PASS' if all_checks else 'FAIL'}")
    return {
        "results": results,
        "first_closed_mismatch": first_closed_mismatch,
        "all_checks": all_checks,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compare the IIA closed paper and Bars completions"
    )
    parser.add_argument("--max-level", type=int, default=7)
    parser.add_argument("--verbose", action="store_true")
    arguments = parser.parse_args()
    comparison = run_comparison(arguments.max_level, arguments.verbose)
    raise SystemExit(0 if comparison["all_checks"] else 1)
