#!/usr/bin/env python3
"""Baseline-free verification of the formal Bars plethystic identity in SO(9).

Using independently derived HFT characters, verify

    R(q) = r(q)/(1-q),
    PL[R(q)] = PL[r(q)] + 1*q.

This formal identity does not prove an SO(10) lift or positivity. Signed
plethystic coefficients are not assigned a geometric interpretation.
"""

import argparse
import sys

import hft_so9
from plethystic_series import plethystic_log


B4 = hft_so9.B4


def run_verification(max_level=10):
    if max_level < 2:
        raise ValueError("max_level must be at least 2")

    _numerator, single_levels = hft_so9.derive_hft_spectrum(max_level)
    max_degree = max_level - 1
    singlet = B4(0, 0, 0, 0)

    r_series = {
        degree: single_levels[degree + 1]
        for degree in range(max_degree + 1)
    }
    cumulative_series = {}
    running = B4(0)
    for degree in range(max_degree + 1):
        running += r_series[degree]
        cumulative_series[degree] = running

    pl_r = plethystic_log(r_series, max_degree)
    pl_cumulative = plethystic_log(cumulative_series, max_degree)

    print("=" * 86)
    print("BASELINE-FREE PLETHYSTIC IDENTITY IN SO(9)")
    print("=" * 86)
    all_pass = True
    for degree in range(1, max_degree + 1):
        expected = singlet if degree == 1 else B4(0)
        difference = pl_cumulative[degree] - pl_r[degree]
        match = difference == expected
        all_pass = all_pass and match
        displayed = "singlet" if difference == singlet else str(difference)
        print(f"q^{degree:<2}  PL[R]-PL[r] = {displayed:<20} {'PASS' if match else 'FAIL'}")

    print("-" * 86)
    print("Protected SO(10) baseline imported: NO")
    print("Interpretation: formal series identity only; no SO(10) positivity conclusion.")
    print(f"Result: {'[PASSED]' if all_pass else '[FAILED]'}")
    return all_pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Verify PL[R]=PL[r]+q using baseline-free HFT SO(9) data"
    )
    parser.add_argument("--max-level", type=int, default=10)
    args = parser.parse_args()
    sys.exit(0 if run_verification(args.max_level) else 1)
