"""TK6B.6b: obstruction to a multiplicative ``D4 -> D5`` core lift.

The equal-rank Dirac fold used in TK6B.5f is a ring homomorphism from the
``D4`` representation ring to virtual ``B4`` characters.  On fundamental
characters its all-chiral ``D5`` lift is

    8_v  -> 10 - 2,
    28   -> 45 - 2*10 + 3,
    8_s  -> 0,
    8_c  -> 16_-,

with the displayed spinor convention.  One can extend these assignments as
a polynomial-ring homomorphism, but this does *not* give a lift of general
Green--Schwarz coefficients: equal-rank Dirac induction is additive, not
multiplicative.

This module records the obstruction.  Agreement holds through degree four
(the degree-four difference is the restriction-kernel chirality class
``J``), while at degree five the restrictions themselves differ.  Thus this
natural shortcut cannot be used in an all-orders proof.  No protected
``SO(10)`` completion is imported.
"""

import argparse
import sys
import time

from sage.all import PolynomialRing, QQ, ZZ

import finite_cross_section as cross
import hft_so9
from trajectory_kernel import cumulative_regge_uplift
from trajectory_kernel import hft_analytic_support


D4 = hft_analytic_support.D4
D5 = cross.D5
B4 = hft_so9.B4

D4_POLYNOMIAL_RING = PolynomialRing(QQ, names=("g1", "g2", "g3", "g4"))
G1, G2, G3, G4 = D4_POLYNOMIAL_RING.gens()
D4_FUNDAMENTALS = tuple(
    D4(*(1 if index == position else 0 for index in range(4)))
    for position in range(4)
)

D5_ONE = D5(0, 0, 0, 0, 0)
D5_VECTOR = D5(1, 0, 0, 0, 0)
D5_ADJOINT = D5(0, 1, 0, 0, 0)
D5_SPIN_MINUS = D5(0, 0, 0, 0, 1)
D5_IMAGES = (
    D5_VECTOR - 2 * D5_ONE,
    D5_ADJOINT - 2 * D5_VECTOR + 3 * D5_ONE,
    D5(0),
    D5_SPIN_MINUS,
)

_IRREP_POLYNOMIAL_CACHE = {
    (0, 0, 0, 0): D4_POLYNOMIAL_RING.one()
}
_ACTIVE_LABELS = set()


def d4_weight_to_dynkin(weight):
    """Convert one ambient ``D4`` highest weight to Dynkin labels."""
    twice = tuple(int(2 * value) for value in weight.to_vector())
    return hft_analytic_support.d4_dynkin_from_twice_orthogonal(twice)


def d4_character_table(character):
    """Return a signed ``D4`` irreducible table keyed by Dynkin labels."""
    return {
        d4_weight_to_dynkin(weight): int(coefficient)
        for weight, coefficient in character.monomial_coefficients().items()
        if coefficient
    }


def evaluate_polynomial(polynomial, values, zero, one):
    """Evaluate a four-variable polynomial in a commutative target ring."""
    result = zero
    for exponents, coefficient in polynomial.dict().items():
        term = one
        for value, exponent in zip(values, exponents):
            if exponent:
                term *= value ** exponent
        result += coefficient * term
    return result


def evaluate_d4_polynomial(polynomial):
    """Evaluate in the ``D4`` Weyl character ring."""
    return evaluate_polynomial(
        D4_POLYNOMIAL_RING(polynomial),
        D4_FUNDAMENTALS,
        D4(0),
        D4(0, 0, 0, 0),
    )


def evaluate_d5_section(polynomial):
    """Evaluate the fixed multiplicative ``D4 -> D5`` section."""
    return evaluate_polynomial(
        D4_POLYNOMIAL_RING(polynomial),
        D5_IMAGES,
        D5(0),
        D5_ONE,
    )


def fundamental_monomial(label):
    """Return the Cartan-product monomial for one ``D4`` label."""
    result = D4_POLYNOMIAL_RING.one()
    for generator, exponent in zip(D4_POLYNOMIAL_RING.gens(), label):
        if exponent:
            result *= generator ** exponent
    return result


def irrep_to_fundamental_polynomial(label):
    """Express one ``D4`` irrep in its fundamental-character polynomial ring."""
    label = tuple(map(int, label))
    if len(label) != 4 or min(label) < 0:
        raise ValueError(f"Invalid D4 Dynkin label: {label}")
    cached = _IRREP_POLYNOMIAL_CACHE.get(label)
    if cached is not None:
        return cached
    if label in _ACTIVE_LABELS:
        raise ValueError(f"D4 fundamental conversion cycled at {label}")
    _ACTIVE_LABELS.add(label)
    try:
        monomial = fundamental_monomial(label)
        product_character = evaluate_d4_polynomial(monomial)
        components = d4_character_table(product_character)
        leading = components.pop(label, 0)
        if leading != 1:
            raise ValueError(
                f"D4 Cartan component is not unit for {label}: {leading}"
            )
        result = monomial
        for lower, coefficient in components.items():
            result -= coefficient * irrep_to_fundamental_polynomial(lower)
        if evaluate_d4_polynomial(result) != D4(*label):
            raise ValueError(f"D4 polynomial round trip failed for {label}")
        _IRREP_POLYNOMIAL_CACHE[label] = result
        return result
    finally:
        _ACTIVE_LABELS.remove(label)


def character_to_fundamental_polynomial(character):
    """Convert a finite virtual ``D4`` character to a polynomial."""
    result = D4_POLYNOMIAL_RING.zero()
    for label, coefficient in d4_character_table(character).items():
        result += coefficient * irrep_to_fundamental_polynomial(label)
    if evaluate_d4_polynomial(result) != character:
        raise ValueError("D4 character polynomial round trip failed")
    return result


def multiplicative_d5_lift(character):
    """Apply the exact polynomial ``D4 -> D5`` section."""
    return evaluate_d5_section(character_to_fundamental_polynomial(character))


def b4_character_from_table(table):
    """Build one virtual ``B4`` character from a sparse label table."""
    return sum(
        (coefficient * B4(*label) for label, coefficient in table.items()),
        B4(0),
    )


def fundamental_section_audit():
    """Verify that the four images lift the Dirac-folded fundamentals."""
    records = []
    for position, fundamental in enumerate(D4_FUNDAMENTALS):
        folded = b4_character_from_table(
            hft_analytic_support.d4_dirac_dominant_table(fundamental)
        )
        restricted = D5_IMAGES[position].branch(B4, rule="default")
        records.append(
            {
                "position": position + 1,
                "folded": folded,
                "restricted": restricted,
                "exact": folded == restricted,
            }
        )
    return {
        "records": tuple(records),
        "all_exact": all(record["exact"] for record in records),
    }


def total_telescoping_coefficients(maximum_degree):
    """Sum the exact ``D4`` Green--Schwarz pivot series by degree."""
    maximum_degree = int(maximum_degree)
    terms = hft_analytic_support.d4_telescoping_terms(maximum_degree)
    total = {degree: D4(0) for degree in range(maximum_degree + 1)}
    for series in terms.values():
        for degree, character in series.items():
            total[degree] += character
    return total


def kernel_difference_analysis(maximum_degree=5):
    """Compare multiplicative and triangular lifts of the telescope."""
    maximum_degree = int(maximum_degree)
    total = total_telescoping_coefficients(maximum_degree)
    records = []
    for degree in range(maximum_degree + 1):
        multiplicative = multiplicative_d5_lift(total[degree])
        folded_table = hft_analytic_support.d4_dirac_dominant_table(
            total[degree]
        )
        folded = b4_character_from_table(folded_table)
        triangular_data = cross.invert_on_cross_section(
            folded, policy="chiral"
        )
        if not triangular_data["exact"] or not triangular_data["integral"]:
            raise ValueError(f"Triangular core lift failed at degree {degree}")
        triangular = triangular_data["lift"]
        difference = multiplicative - triangular
        branch_zero = difference.branch(B4, rule="default") == B4(0)
        table = cumulative_regge_uplift.d5_character_table(difference)
        expected_multiple = None
        if difference == cumulative_regge_uplift.J_CHARACTER:
            expected_multiple = ("J", 1)
        elif difference == -cumulative_regge_uplift.J_CHARACTER:
            expected_multiple = ("-J", 1)
        elif difference:
            a0_table = cumulative_regge_uplift.d5_character_table(
                cumulative_regge_uplift.A0_CHARACTER
            )
            ratios = {
                QQ(table.get(label, 0)) / coefficient
                for label, coefficient in a0_table.items()
            }
            if len(ratios) == 1:
                ratio = ratios.pop()
                if ratio in ZZ and difference == int(ratio) * cumulative_regge_uplift.A0_CHARACTER:
                    expected_multiple = ("A0", int(ratio))
        records.append(
            {
                "degree": degree,
                "multiplicative": multiplicative,
                "triangular": triangular,
                "difference": difference,
                "difference_table": table,
                "branch_zero": branch_zero,
                "simple_multiple": expected_multiple,
            }
        )
    return {
        "maximum_degree": maximum_degree,
        "total_d4": total,
        "records": tuple(records),
        "all_kernel": all(record["branch_zero"] for record in records),
        "simple_correction_series": {
            record["degree"]: record["simple_multiple"]
            for record in records
            if record["difference"]
        },
        "degree_five_obstruction": (
            maximum_degree >= 5
            and not records[5]["branch_zero"]
        ),
    }


def run_analysis(maximum_degree=5):
    """Run the multiplicative-section comparison through one degree."""
    started = time.time()
    fundamentals = fundamental_section_audit()
    analysis = kernel_difference_analysis(maximum_degree)
    print("=" * 100)
    print("TK6B.6b — MULTIPLICATIVE D4 -> D5 CORE")
    print("=" * 100)
    print(f"Fundamental section identities exact: {fundamentals['all_exact']}")
    print(f"Degrees: 0 through {int(maximum_degree)}")
    print(f"Every difference restricts to zero: {analysis['all_kernel']}")
    if int(maximum_degree) >= 5:
        print(
            "Degree-five nonmultiplicativity obstruction found: "
            f"{analysis['degree_five_obstruction']}"
        )
    print(f"Simple correction series: {analysis['simple_correction_series']}")
    for record in analysis["records"]:
        if record["difference"] and record["simple_multiple"] is None:
            print(
                f"  degree {record['degree']} non-simple kernel difference: "
                f"{record['difference_table']}"
            )
    print("Protected SO(10) baseline imported: NO")
    print(f"Runtime: {time.time() - started:.3f}s")
    return {
        "fundamentals": fundamentals,
        "analysis": analysis,
        "all_checks": (
            fundamentals["all_exact"]
            and (
                analysis["degree_five_obstruction"]
                if int(maximum_degree) >= 5
                else analysis["all_kernel"]
            )
        ),
    }


def run_self_test():
    """Check the fundamental agreement and first multiplicativity failure."""
    result = run_analysis(maximum_degree=5)
    if not result["all_checks"]:
        raise AssertionError("The multiplicative obstruction audit failed")
    correction = result["analysis"]["simple_correction_series"]
    if correction.get(4) != ("J", 1):
        raise AssertionError(f"Unexpected degree-four kernel term: {correction}")
    if result["analysis"]["records"][5]["branch_zero"]:
        raise AssertionError("Expected the degree-five restriction obstruction")
    return True


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Compare multiplicative and triangular lifts of the HFT core"
    )
    parser.add_argument("--maximum-degree", type=int, default=5)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.self_test:
            return 0 if run_self_test() else 1
        result = run_analysis(maximum_degree=args.maximum_degree)
    except Exception as error:
        print(f"TK6B.6b FAILED: {error}", file=sys.stderr)
        return 1
    return 0 if result["all_checks"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
