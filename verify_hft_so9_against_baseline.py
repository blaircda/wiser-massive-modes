"""
Independent benchmark of the baseline-free HFT SO(9) derivation.

This is intentionally the only HFT SO(9) script in this workflow that imports
massive_SO10.py.  The derivation lives in hft_so9.py and does not depend on the
baseline.  This script compares its output with the human-established level
1--10 SO(10) completion after restriction to SO(9).
"""

import argparse
import sys
import time

from sage.all import QQ, WeylCharacterRing

import hft_so9
from massive_SO10 import SO10_SUPERMULTIPLETS_DYNKIN


B4 = hft_so9.B4
D5 = WeylCharacterRing("D5", base_ring=QQ, style="coroots")


def get_baseline_r(max_level):
    """Restrict consecutive differences of the baseline R_n to SO(9)."""

    def get_so10_character(level):
        result = D5(0)
        for mult, _dim, dynkin in SO10_SUPERMULTIPLETS_DYNKIN[level]["bosons"]:
            result += mult * D5(*dynkin)
        for mult, _dim, dynkin in SO10_SUPERMULTIPLETS_DYNKIN[level]["fermions"]:
            result += mult * D5(*dynkin)
        return result

    cumulative = {
        level: get_so10_character(level).branch(B4, rule="default")
        for level in range(1, max_level + 1)
    }
    return {
        1: cumulative[1],
        **{
            level: cumulative[level] - cumulative[level - 1]
            for level in range(2, max_level + 1)
        },
    }


def run_verification(max_level=10, verbose=False):
    print("=" * 82)
    print("VERIFYING BASELINE-FREE HFT SO(9) DERIVATION AGAINST PRESERVED BASELINE")
    print("=" * 82)

    started = time.time()
    numerator, derived_r = hft_so9.derive_hft_spectrum(max_level)
    baseline_r = get_baseline_r(max_level)

    print(f"{'Level':<7}{'Dimension':<13}{'Internal N=Z_Q*r':<20}{'Baseline Match':<18}{'Status'}")
    print("-" * 82)
    all_pass = True
    for level in range(1, max_level + 1):
        internal_match = hft_so9.Z_Q * derived_r[level] == numerator[level]
        baseline_match = derived_r[level] == baseline_r[level]
        level_pass = internal_match and baseline_match
        all_pass = all_pass and level_pass
        print(
            f"{level:<7}{int(derived_r[level].degree()):<13}"
            f"{str(internal_match):<20}{str(baseline_match):<18}"
            f"{'PASS' if level_pass else 'FAIL'}"
        )
        if verbose and not baseline_match:
            print(f"  difference = {derived_r[level] - baseline_r[level]}")

    print("-" * 82)
    print(f"Elapsed: {time.time() - started:.3f}s")
    print(f"Result: {'[PASSED]' if all_pass else '[FAILED]'}")
    return all_pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compare the independent HFT SO(9) derivation with the baseline"
    )
    parser.add_argument("--max-level", type=int, default=10)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    sys.exit(0 if run_verification(args.max_level, args.verbose) else 1)
