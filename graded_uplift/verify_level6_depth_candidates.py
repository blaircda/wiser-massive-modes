"""Protected GU5 comparison of level-6 candidates with interlacing depth.

The baseline-free feasibility result lives in ``interlacing_depth_audit.py``.
This module separately checks the protected Bars character and the transcribed
paper candidate.  Neither is ever fed back into the derivation.
"""

import argparse

import finite_cross_section as cross
from graded_uplift import direct_closed_low_levels as direct
from graded_uplift import iia_closed_refinement as iia
from graded_uplift import verify_iia_closed_against_baseline as protected
from graded_uplift import verify_paper_grading


def refined_difference(character, target):
    image = direct.depth_graded_restriction(character)
    depths = sorted(set(image) | set(target))
    return {
        depth: cross.character_coefficients(
            image.get(depth, cross.B4(0)) - target.get(depth, cross.B4(0))
        )
        for depth in depths
        if image.get(depth, cross.B4(0)) != target.get(depth, cross.B4(0))
    }


def run_comparison(max_level=6, verbose=False):
    if max_level < 1 or max_level > 6:
        raise ValueError("Protected GU5 comparison is scoped to levels 1--6")
    single_levels, cumulative_so9 = cross.derive_cumulative_so9(max_level)
    paper_tables = verify_paper_grading.cumulative_ungraded_coefficients(
        max_level
    )
    results = {}

    print("=" * 108)
    print("GU5 — PROTECTED LEVEL-6 INTERLACING-DEPTH COMPARISON")
    print("=" * 108)
    print(" level | paper depth exact | Bars depth exact | refined images equal | chiral characters equal")
    for level in range(1, max_level + 1):
        target = {
            level - oscillator_level: single_levels[oscillator_level]
            for oscillator_level in range(1, level + 1)
        }
        paper = iia.d5_character(paper_tables[level])
        bars = protected.bars_character(level)
        paper_difference = refined_difference(paper, target)
        bars_difference = refined_difference(bars, target)
        paper_image = direct.depth_graded_restriction(paper)
        bars_image = direct.depth_graded_restriction(bars)
        result = {
            "paper": paper,
            "bars": bars,
            "paper_difference": paper_difference,
            "bars_difference": bars_difference,
            "paper_exact": not paper_difference,
            "bars_exact": not bars_difference,
            "images_equal": paper_image == bars_image,
            "characters_equal": paper == bars,
            "paper_restriction_exact": (
                paper.branch(cross.B4, rule="default") == cumulative_so9[level]
            ),
            "bars_restriction_exact": (
                bars.branch(cross.B4, rule="default") == cumulative_so9[level]
            ),
        }
        results[level] = result
        print(
            f" {level:5d} | {str(result['paper_exact']):>17s} | "
            f"{str(result['bars_exact']):>16s} | "
            f"{str(result['images_equal']):>20s} | "
            f"{str(result['characters_equal']):>22s}"
        )
        if verbose and paper_difference:
            print(f"         common refined residual: {paper_difference}")

    first_failure = next(
        (level for level, result in results.items() if not result["bars_exact"]),
        None,
    )
    checks = (
        first_failure == 5
        and all(result["images_equal"] for result in results.values())
        and all(
            result["paper_restriction_exact"]
            and result["bars_restriction_exact"]
            for result in results.values()
        )
        and not results[6]["characters_equal"]
        and results[6]["paper_difference"] == results[6]["bars_difference"]
    )
    print("-" * 108)
    print(f"First depth mismatch for both candidates: {first_failure}")
    print("The level-6 Bars/paper chirality difference is invisible to interlacing depth.")
    print("Protected Bars completion imported: YES, comparison only")
    print(f"GU5 protected checks: {'PASS' if checks else 'FAIL'}")
    return {
        "results": results,
        "first_failure": first_failure,
        "all_checks": checks,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compare level-6 candidates with interlacing depth"
    )
    parser.add_argument("--max-level", type=int, default=6)
    parser.add_argument("--verbose", action="store_true")
    arguments = parser.parse_args()
    comparison = run_comparison(arguments.max_level, arguments.verbose)
    raise SystemExit(0 if comparison["all_checks"] else 1)
