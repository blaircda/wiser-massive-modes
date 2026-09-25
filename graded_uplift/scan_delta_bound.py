"""GU2 finite-bound scan for the protected Bars representative.

This is a protected comparison layer: it imports the established Bars
completion only to specify the ungraded D5 target.  The refined oscillator
target and finite-domain solver remain baseline-free.
"""

import argparse

from graded_uplift import graded_kernel
from graded_uplift import refined_spectrum
from graded_uplift import verify_bars_compatibility
from graded_uplift import verify_paper_grading


def scan(level=6, max_slack=3, policy="outer-closed", exact_rank=False):
    refined = refined_spectrum.derive_refined_primaries(level)
    target = verify_paper_grading.target_level_image(refined, level)
    bars = verify_bars_compatibility.bars_ungraded_level(level)
    rows = []
    print("GU2 — FINITE DELTA-BOUND SCAN")
    print(f"level={level}, policy={policy}")
    print(" slack | Delta maximum | candidate terms | feasible | exact | minimum charge")
    for slack in range(max_slack + 1):
        result = graded_kernel.solve_graded_lift(
            level,
            target,
            bars,
            policy,
            delta_slack=slack,
        )
        rows.append(result)
        print(
            f" {slack:5d} | {level + 1 + slack:13d} | "
            f"{result['term_count']:15d} | {str(result['feasible']):8s} | "
            f"{str(result['exact']):5s} | {result['minimum_charge']}"
        )
        if result["feasible"]:
            print(f" solution={result['solution']}")
        if exact_rank:
            rational = graded_kernel.rational_feasibility(
                level,
                target,
                bars,
                policy,
                delta_slack=slack,
            )
            print(
                "         exact QQ check: "
                f"feasible={rational['feasible_over_QQ']}, "
                f"rank={rational['rank']}, "
                f"augmented_rank={rational['augmented_rank']}, "
                f"matrix={rational['row_count']}x{rational['column_count']}"
            )
    print("Protected Bars completion imported: YES, comparison only")
    return rows


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scan the finite GU2 Delta cutoff")
    parser.add_argument("--level", type=int, default=6)
    parser.add_argument("--max-slack", type=int, default=3)
    parser.add_argument("--policy", choices=graded_kernel.DOMAIN_POLICIES, default="outer-closed")
    parser.add_argument("--exact-rank", action="store_true")
    arguments = parser.parse_args()
    scan(arguments.level, arguments.max_slack, arguments.policy, arguments.exact_rank)
