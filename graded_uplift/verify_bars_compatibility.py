"""GU2 comparison: can the protected Bars lift obey Delta-J=nu?

This is explicitly a protected comparison layer.  Candidate domains and the
integer solver are implemented baseline-free in ``graded_kernel.py``.
"""

import argparse
from collections import defaultdict

from massive_SO10 import get_so10_character

from graded_uplift import graded_kernel
from graded_uplift import paper_levels
from graded_uplift import refined_spectrum
from graded_uplift import verify_against_baseline
from graded_uplift import verify_paper_grading


def paper_ungraded_level(level):
    result = defaultdict(int)
    for _twice_delta, coefficient, label in paper_levels.expanded_terms(level):
        result[label] += coefficient
    return {label: value for label, value in sorted(result.items()) if value}


def bars_ungraded_level(level):
    current = verify_against_baseline.coefficient_table(get_so10_character(level))
    previous = (
        {}
        if level == 1
        else verify_against_baseline.coefficient_table(get_so10_character(level - 1))
    )
    keys = set(current) | set(previous)
    return {
        label: current.get(label, 0) - previous.get(label, 0)
        for label in sorted(keys)
        if current.get(label, 0) != previous.get(label, 0)
    }


def run_comparison(max_level=7, verbose=False, min_level=1):
    if max_level > max(paper_levels.PAPER_LEVELS):
        raise ValueError("GU2 literature transcription currently covers levels 1--7")
    if min_level < 1 or min_level > max_level:
        raise ValueError("min_level must lie between 1 and max_level")
    refined = refined_spectrum.derive_refined_primaries(max_level)
    results = {}

    print("=" * 116)
    print("GU2 — GRADED COMPATIBILITY OF THE PAPER AND BARS LIFTS")
    print("=" * 116)
    print("  level | paper/paper-bound | Bars/paper-bound | Bars/outer-closed | candidate terms paper/outer")
    for level in range(min_level, max_level + 1):
        target = verify_paper_grading.target_level_image(refined, level)
        paper = graded_kernel.solve_graded_lift(
            level, target, paper_ungraded_level(level), "paper-bound"
        )
        bars_paper = graded_kernel.solve_graded_lift(
            level, target, bars_ungraded_level(level), "paper-bound"
        )
        bars_outer = graded_kernel.solve_graded_lift(
            level, target, bars_ungraded_level(level), "outer-closed"
        )
        results[level] = {
            "paper": paper,
            "bars_paper_bound": bars_paper,
            "bars_outer_closed": bars_outer,
        }
        print(
            f"  {level:5d} | {str(paper['feasible'] and paper['exact']):>17s} | "
            f"{str(bars_paper['feasible'] and bars_paper['exact']):>16s} | "
            f"{str(bars_outer['feasible'] and bars_outer['exact']):>17s} | "
            f"{paper['term_count']:7d}/{bars_outer['term_count']}"
        )
        if verbose:
            for name, result in results[level].items():
                print(
                    f"    {name}: feasible={result['feasible']}, "
                    f"exact={result['exact']}, charge={result['minimum_charge']}, "
                    f"missing={result['missing_labels']}"
                )
                if result["feasible"]:
                    print(f"      solution={result['solution']}")

    controls_pass = all(
        result["paper"]["feasible"] and result["paper"]["exact"]
        for result in results.values()
    )
    first_paper_bound_failure = next(
        (
            level
            for level, result in results.items()
            if not (
                result["bars_paper_bound"]["feasible"]
                and result["bars_paper_bound"]["exact"]
            )
        ),
        None,
    )
    first_outer_failure = next(
        (
            level
            for level, result in results.items()
            if not (
                result["bars_outer_closed"]["feasible"]
                and result["bars_outer_closed"]["exact"]
            )
        ),
        None,
    )
    print("-" * 116)
    print(f"Paper-table controls pass: {controls_pass}")
    print(f"First Bars failure in paper-bound domain: {first_paper_bound_failure}")
    print(f"First Bars failure in outer-closed domain: {first_outer_failure}")
    print("Protected Bars completion imported: YES, comparison only")
    return {
        "results": results,
        "controls_pass": controls_pass,
        "first_paper_bound_failure": first_paper_bound_failure,
        "first_outer_failure": first_outer_failure,
    }


def run_self_test():
    level = 2
    terms = graded_kernel.candidate_terms(level, "paper-bound")
    expected = ((0, 0, 0, 0, 0), 6) in terms and (
        (1, 0, 0, 0, 0), 4
    ) in terms
    print("GU2 GRADED-DOMAIN SELF-TEST")
    print(f"Level-2 starred pair included: {'PASS' if expected else 'FAIL'}")
    print("Protected SO(10) baseline imported: YES, comparison module")
    return expected


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Test graded compatibility of the protected Bars lift"
    )
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--max-level", type=int, default=7)
    parser.add_argument("--min-level", type=int, default=1)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        raise SystemExit(0 if run_self_test() else 1)
    result = run_comparison(args.max_level, args.verbose, args.min_level)
    raise SystemExit(0 if result["controls_pass"] else 1)
