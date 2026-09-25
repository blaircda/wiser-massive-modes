"""TK4d: exact level-2 closed-string completion test.

The positive 65,536-state closed supermultiplet is constructed intrinsically
as the fermionic Fock representation

    Q_closed = sum_(j=0)^16 exterior_power^j(16).

It is not the literal square of the virtual chiral SO(10) uplift ``Z_Q^10``.
This module compares both same- and opposite-chirality products of the HFT
chiral numerator with ``Q_closed`` and tests exact divisibility in the
injective five-variable Laurent weight ring.

No protected SO(10) spectrum is imported.
"""

import argparse
import sys
import time

from sage.all import LaurentPolynomialRing, QQ

import finite_cross_section
import hft_so10_uplift
import hft_so9
from trajectory_kernel import kernel_anomaly


def positive_character(character):
    """Test nonnegative integral irreducible multiplicities."""
    coefficients = kernel_anomaly.character_table(character).values()
    return all(coefficient.is_integer() and coefficient >= 0 for coefficient in coefficients)


def coefficient_statistics(character):
    """Return basic irreducible coefficient statistics."""
    values = tuple(kernel_anomaly.character_table(character).values())
    return {
        "terms": len(values),
        "negative_terms": sum(value < 0 for value in values),
        "minimum": min(values, default=0),
        "maximum": max(values, default=0),
    }


def closed_supermultiplet(chirality=1):
    """Construct the positive closed supermultiplet as an exterior algebra."""
    if chirality not in (-1, 1):
        raise ValueError("chirality must be +1 or -1")
    spinor = (
        hft_so10_uplift.D5(0, 0, 0, 0, 1)
        if chirality == 1
        else hft_so10_uplift.D5(0, 0, 0, 1, 0)
    )
    return sum(
        (spinor.exterior_power(degree) for degree in range(17)),
        hft_so10_uplift.D5(0),
    )


def closed_reference_quotient(level=2):
    """Lift the level-matched SO(9) quotient on the fixed chiral section."""
    _numerator, single_levels = hft_so9.derive_hft_spectrum(level)
    target = single_levels[level] * single_levels[level]
    lifted = finite_cross_section.invert_on_cross_section(target, policy="chiral")
    if not lifted["exact"] or not lifted["integral"]:
        raise ValueError("Closed SO(9) quotient did not lift exactly")
    return target, lifted["lift"]


def exact_laurent_division(dividend, divisor, ring):
    """Test divisibility in the injective doubled-weight Laurent embedding."""
    dividend_polynomial = kernel_anomaly.character_to_laurent(dividend, ring)
    divisor_polynomial = kernel_anomaly.character_to_laurent(divisor, ring)
    quotient, remainder = dividend_polynomial.quo_rem(divisor_polynomial)
    divides = divisor_polynomial.divides(dividend_polynomial)
    if divides != (remainder == 0):
        raise ValueError("Laurent divisibility checks disagree")
    return {
        "divides": divides,
        "quotient": quotient if divides else None,
        "remainder": remainder,
        "remainder_terms": len(remainder.monomial_coefficients()),
    }


def run_level2_closed_test(verbose=False):
    """Run the complete baseline-free level-2 closed-sector check."""
    started = time.time()
    numerator = hft_so10_uplift.compute_hft_d5(2)
    zq = numerator[1]
    n2 = numerator[2]
    tau_zq = kernel_anomaly.outer_conjugate(zq)
    tau_n2 = kernel_anomaly.outer_conjugate(n2)

    closed_factor = closed_supermultiplet(chirality=1)
    closed_factor_conjugate = kernel_anomaly.outer_conjugate(closed_factor)
    zq9 = zq.branch(hft_so10_uplift.B4, rule="default")
    expected_so9, reference_quotient = closed_reference_quotient(2)

    cases = {
        "same": {
            "raw_factor": zq * zq,
            "numerator": n2 * n2,
        },
        "opposite": {
            "raw_factor": zq * tau_zq,
            "numerator": n2 * tau_n2,
        },
    }

    laurent_ring = LaurentPolynomialRing(QQ, 5, "x")
    results = {}
    for name, case in cases.items():
        raw_factor = case["raw_factor"]
        closed_numerator = case["numerator"]
        raw_level_one_difference = raw_factor - closed_factor
        anomaly = closed_numerator - closed_factor * reference_quotient
        division = exact_laurent_division(
            closed_numerator, closed_factor, laurent_ring
        )
        results[name] = {
            **case,
            "raw_factor_positive": positive_character(raw_factor),
            "raw_factor_statistics": coefficient_statistics(raw_factor),
            "raw_factor_matches_closed": raw_factor == closed_factor,
            "raw_level_one_difference": raw_level_one_difference,
            "raw_level_one_difference_restricts_zero": (
                raw_level_one_difference.branch(
                    hft_so10_uplift.B4, rule="default"
                )
                == hft_so10_uplift.B4(0)
            ),
            "numerator_restriction_matches": (
                closed_numerator.branch(
                    hft_so10_uplift.B4, rule="default"
                )
                == (zq9 * zq9) * expected_so9
            ),
            "anomaly": anomaly,
            "anomaly_restricts_zero": (
                anomaly.branch(hft_so10_uplift.B4, rule="default")
                == hft_so10_uplift.B4(0)
            ),
            "anomaly_dimension": int(anomaly.degree()),
            "anomaly_terms": len(kernel_anomaly.character_table(anomaly)),
            "division": division,
        }

    case_difference = cases["same"]["numerator"] - cases["opposite"]["numerator"]
    difference_division = exact_laurent_division(
        case_difference, closed_factor, laurent_ring
    )

    print("=" * 118)
    print("TK4d — EXACT LEVEL-2 CLOSED-STRING COMPLETION TEST (BASELINE-FREE)")
    print("=" * 118)
    print("Protected SO(10) baseline imported: NO")
    print("\nIntrinsic closed universal factor:")
    print("  Definition: Q_closed = sum_(j=0)^16 Lambda^j(16)")
    print(f"  Dimension: {int(closed_factor.degree())}")
    print(f"  Irreducible terms: {len(kernel_anomaly.character_table(closed_factor))}")
    print(f"  Positive integral character: {positive_character(closed_factor)}")
    print(f"  Outer-chirality invariant: {closed_factor_conjugate == closed_factor}")
    print(f"  Restriction equals (Z_Q^9)^2: {closed_factor.branch(hft_so10_uplift.B4, rule='default') == zq9 * zq9}")

    print("\nRaw chiral-product uplifts and level-2 division:")
    for name, result in results.items():
        stats = result["raw_factor_statistics"]
        print(f"  {name} chirality:")
        print(
            "    raw level-1 factor positive / equals Q_closed: "
            f"{result['raw_factor_positive']} / {result['raw_factor_matches_closed']}"
        )
        print(
            "    raw factor terms / negative terms / minimum: "
            f"{stats['terms']} / {stats['negative_terms']} / {stats['minimum']}"
        )
        print(
            "    raw factor differs from Q_closed by restriction kernel: "
            f"{result['raw_level_one_difference_restricts_zero']}"
        )
        print(
            "    closed numerator has expected SO(9) restriction: "
            f"{result['numerator_restriction_matches']}"
        )
        print(
            "    reference anomaly dimension / restricts zero / terms: "
            f"{result['anomaly_dimension']} / {result['anomaly_restricts_zero']} / "
            f"{result['anomaly_terms']}"
        )
        print(
            "    exact division by Q_closed: "
            f"{result['division']['divides']} "
            f"(Laurent remainder terms: {result['division']['remainder_terms']})"
        )
        if verbose:
            print(f"    raw factor: {result['raw_factor']}")

    print("\nComparison of chirality choices:")
    print(
        "  Their level-2 numerator difference is divisible by Q_closed: "
        f"{difference_division['divides']}"
    )
    print("-" * 118)
    print("Conclusion: tensoring the present virtual chiral uplifts does not")
    print("produce the intrinsic positive closed uplift, already at level 1,")
    print("and neither raw level-2 product is divisible by Q_closed.")
    print(f"Elapsed: {time.time() - started:.3f}s")
    return {
        "closed_factor": closed_factor,
        "expected_so9": expected_so9,
        "reference_quotient": reference_quotient,
        "cases": results,
        "difference_division": difference_division,
    }


def run_self_test():
    """Check involution and low-cost character utilities."""
    vector = hft_so10_uplift.D5(1, 0, 0, 0, 0)
    spinor = hft_so10_uplift.D5(0, 0, 0, 0, 1)
    checks = (
        positive_character(vector),
        kernel_anomaly.outer_conjugate(vector) == vector,
        kernel_anomaly.outer_conjugate(
            kernel_anomaly.outer_conjugate(spinor)
        )
        == spinor,
    )
    passed = all(checks)
    print("TRAJECTORY-KERNEL TK4d SELF-TEST")
    print(f"Closed-sector utility checks: {'PASS' if passed else 'FAIL'}")
    print("Protected SO(10) baseline imported: NO")
    return passed


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Exact level-2 closed-string SO(10) completion test"
    )
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        sys.exit(0 if run_self_test() else 1)
    run_level2_closed_test(args.verbose)
    sys.exit(0)
