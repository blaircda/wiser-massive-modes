"""
Compare the baseline-free HFT numerator uplift with the preserved SO(10) data.

This verification script is intentionally separate from hft_so10_uplift.py.
It checks restriction consistency and measures the kernel remainder obtained when
the known baseline single-level lift is substituted into the proposed quotient.
It does not claim to derive the baseline spectrum or to pass Milestone M4.
"""

import argparse
import sys
import time

import hft_so9
import hft_so10_uplift
from massive_SO10 import SO10_SUPERMULTIPLETS_DYNKIN


D5 = hft_so10_uplift.D5
B4 = hft_so10_uplift.B4


def get_baseline_cumulative(max_level):
    """Load the preserved cumulative R_n characters for comparison only."""
    result = {}
    for level in range(1, max_level + 1):
        char = D5(0)
        for mult, _dim, dynkin in SO10_SUPERMULTIPLETS_DYNKIN[level]["bosons"]:
            char += mult * D5(*dynkin)
        for mult, _dim, dynkin in SO10_SUPERMULTIPLETS_DYNKIN[level]["fermions"]:
            char += mult * D5(*dynkin)
        result[level] = char
    return result


def run_verification(max_level=10, verbose=False):
    print("=" * 104)
    print("VERIFYING HFT NUMERATOR RESTRICTION AND BASELINE KERNEL REMAINDERS")
    print("=" * 104)

    started = time.time()
    p10 = hft_so10_uplift.compute_hft_d5(max_level)
    p9, derived_r9 = hft_so9.derive_hft_spectrum(max_level)
    zq10 = p10[1]
    baseline_R = get_baseline_cumulative(max_level)
    baseline_r = {
        1: baseline_R[1],
        **{
            level: baseline_R[level] - baseline_R[level - 1]
            for level in range(2, max_level + 1)
        },
    }

    running_r9 = B4(0)
    print(
        f"{'Level':<7}{'Numerator Res':<16}{'Baseline R Res':<18}"
        f"{'Remainder Zero':<17}{'Rem Res=0':<13}{'Rem dim=0':<12}{'Status'}"
    )
    print("-" * 104)

    all_consistent = True
    nonzero_remainders = []
    for level in range(1, max_level + 1):
        numerator_restricts = p10[level].branch(B4) == p9[level]
        running_r9 += derived_r9[level]
        baseline_restricts = baseline_R[level].branch(B4) == running_r9

        remainder = p10[level] - zq10 * baseline_r[level]
        remainder_zero = remainder == D5(0)
        remainder_branch_zero = remainder.branch(B4) == B4(0)
        remainder_dimension_zero = remainder.degree() == 0
        if not remainder_zero:
            nonzero_remainders.append(level)

        level_consistent = (
            numerator_restricts
            and baseline_restricts
            and remainder_branch_zero
            and remainder_dimension_zero
        )
        all_consistent = all_consistent and level_consistent
        print(
            f"{level:<7}{str(numerator_restricts):<16}{str(baseline_restricts):<18}"
            f"{str(remainder_zero):<17}{str(remainder_branch_zero):<13}"
            f"{str(remainder_dimension_zero):<12}"
            f"{'CONSISTENT' if level_consistent else 'FAIL'}"
        )
        if verbose and not remainder_zero:
            print(f"      kernel remainder = {remainder}")

    print("-" * 104)
    print(f"Nonzero kernel remainders occur at levels: {nonzero_remainders}")
    print("These checks establish consistency after restriction, not a direct SO(10) quotient.")
    print(f"Elapsed: {time.time() - started:.3f}s")
    print(f"Result: {'[CONSISTENT]' if all_consistent else '[FAILED]'}")
    return all_consistent


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compare the HFT SO(10) numerator with the preserved baseline"
    )
    parser.add_argument("--max-level", type=int, default=10)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    sys.exit(0 if run_verification(args.max_level, args.verbose) else 1)
