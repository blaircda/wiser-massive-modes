#!/usr/bin/env python3
"""Compare baseline-free cross-section lifts with the protected SO(10) data.

The derivation remains in ``finite_cross_section.py``.  This separate script is
the only layer in the finite-cross-section workflow that imports the known
level-1--10 completion.  Exact equality is not assumed: two lifts of the same
SO(9) character may differ by a nonzero element of the restriction kernel.
"""

import argparse
import sys
import time

import finite_cross_section as cross
from massive_SO10 import SO10_SUPERMULTIPLETS_DYNKIN


D5 = cross.D5
B4 = cross.B4


def get_baseline_cumulative(max_level):
    """Load protected cumulative SO(10) characters for comparison only."""
    result = {}
    for level in range(1, max_level + 1):
        character = D5(0)
        data = SO10_SUPERMULTIPLETS_DYNKIN[level]
        for multiplicity, _dimension, dynkin in data["bosons"]:
            character += multiplicity * D5(*dynkin)
        for multiplicity, _dimension, dynkin in data["fermions"]:
            character += multiplicity * D5(*dynkin)
        result[level] = character
    return result


def run_verification(max_level=10, policies=cross.POLICIES, verbose=False):
    print("=" * 118)
    print("FINITE CROSS-SECTION COMPARISON WITH PROTECTED SO(10) BASELINE")
    print("=" * 118)
    started = time.time()

    _single, cumulative = cross.derive_cumulative_so9(max_level)
    baseline = get_baseline_cumulative(max_level)
    all_consistent = True

    for policy in policies:
        print(f"\nPolicy: {policy}")
        print("-" * 118)
        print(
            f"{'Level':<7}{'Canonical Res':<16}{'Baseline Res':<15}"
            f"{'Exact Match':<14}{'Difference Res=0':<19}"
            f"{'Difference dim=0':<19}{'Canonical Positive':<20}{'Status'}"
        )
        print("-" * 118)

        for level in range(1, max_level + 1):
            result = cross.invert_on_cross_section(cumulative[level], policy)
            canonical = result["lift"]
            known = baseline[level]
            difference = canonical - known

            canonical_restricts = canonical.branch(B4, rule="default") == cumulative[level]
            baseline_restricts = known.branch(B4, rule="default") == cumulative[level]
            exact_match = difference == D5(0)
            difference_restricts_zero = difference.branch(B4, rule="default") == B4(0)
            difference_dimension_zero = difference.degree() == 0
            consistent = (
                canonical_restricts
                and baseline_restricts
                and difference_restricts_zero
                and difference_dimension_zero
            )
            all_consistent = all_consistent and consistent

            print(
                f"{level:<7}{str(canonical_restricts):<16}{str(baseline_restricts):<15}"
                f"{str(exact_match):<14}{str(difference_restricts_zero):<19}"
                f"{str(difference_dimension_zero):<19}{str(result['positive']):<20}"
                f"{'CONSISTENT' if consistent else 'FAIL'}"
            )
            if verbose and not exact_match:
                print(f"      canonical - baseline = {difference}")

    print("-" * 118)
    print("Exact matches are informative but are not required: kernel differences are expected.")
    print(f"Overall restriction consistency: {'[PASSED]' if all_consistent else '[FAILED]'}")
    print(f"Elapsed: {time.time() - started:.3f}s")
    return all_consistent


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compare finite cross-section lifts with the protected baseline"
    )
    parser.add_argument("--max-level", type=int, default=10)
    parser.add_argument(
        "--policy",
        choices=("all",) + cross.POLICIES,
        default="all",
    )
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    selected_policies = cross.POLICIES if args.policy == "all" else (args.policy,)
    sys.exit(
        0
        if run_verification(args.max_level, selected_policies, args.verbose)
        else 1
    )
