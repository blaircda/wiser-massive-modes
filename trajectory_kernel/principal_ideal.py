"""TK6a: the global principal ideal of the D5 -> B4 restriction kernel.

For simply connected compact groups the representation rings are polynomial
rings in the fundamental characters.  Under Spin(10) -> Spin(9), the first
three D5 fundamental characters restrict triangularly and the two half-spinor
fundamentals have the same restriction.  Consequently

    ker( R(Spin(10)) -> R(Spin(9)) ) = (16_+ - 16_-).

This module makes that presentation exact and computational.  It converts D5
irreducible characters to polynomials in the five fundamental characters,
divides finite restriction-kernel relations by the half-spinor difference,
and verifies the quotient back in the Weyl character ring.

The calculation is baseline-free.  It imports no protected SO(10) completion.
"""

import argparse
import sys
import time

from sage.all import PolynomialRing, QQ, ZZ

import finite_cross_section as cross
from trajectory_kernel import kernel_lattice


D5 = cross.D5
B4 = cross.B4

D5_POLYNOMIAL_RING = PolynomialRing(
    QQ,
    names=("f1", "f2", "f3", "f4", "f5"),
)
B4_POLYNOMIAL_RING = PolynomialRing(
    QQ,
    names=("b1", "b2", "b3", "b4"),
)

F1, F2, F3, F4, F5 = D5_POLYNOMIAL_RING.gens()
B1, B2, B3, B4_VAR = B4_POLYNOMIAL_RING.gens()

D5_FUNDAMENTALS = tuple(
    D5(*(1 if index == position else 0 for index in range(5)))
    for position in range(5)
)
B4_FUNDAMENTALS = tuple(
    B4(*(1 if index == position else 0 for index in range(4)))
    for position in range(4)
)

D5_ONE = D5(0, 0, 0, 0, 0)
B4_ONE = B4(0, 0, 0, 0)

SPIN_PLUS = D5(0, 0, 0, 1, 0)
SPIN_MINUS = D5(0, 0, 0, 0, 1)
J_CHARACTER = SPIN_PLUS - SPIN_MINUS
J_POLYNOMIAL = F4 - F5

# Exact polynomial restriction and a right inverse on fundamental generators.
D5_TO_B4_SUBSTITUTIONS = (
    1 + B1,
    B1 + B2,
    B2 + B3,
    B4_VAR,
    B4_VAR,
)
B4_TO_D5_SECTION = (
    F1 - 1,
    F2 - F1 + 1,
    F3 - F2 + F1 - 1,
    F5,
)

_D5_IRREP_POLYNOMIAL_CACHE = {(0, 0, 0, 0, 0): D5_POLYNOMIAL_RING.one()}
_D5_ACTIVE_LABELS = set()


def _integer(value, description):
    """Return an exact Python integer, rejecting nonintegral labels."""
    if value not in ZZ:
        raise ValueError(f"Nonintegral {description}: {value}")
    return int(value)


def d5_weight_to_dynkin(weight):
    """Convert a D5 ambient highest weight to Dynkin labels."""
    x1, x2, x3, x4, x5 = weight.to_vector()
    return (
        _integer(x1 - x2, "D5 label a1"),
        _integer(x2 - x3, "D5 label a2"),
        _integer(x3 - x4, "D5 label a3"),
        _integer(x4 - x5, "D5 label a4"),
        _integer(x4 + x5, "D5 label a5"),
    )


def character_table(character):
    """Return irreducible D5 coefficients keyed by Dynkin labels."""
    return {
        d5_weight_to_dynkin(weight): coefficient
        for weight, coefficient in character.monomial_coefficients().items()
        if coefficient
    }


def character_from_table(table):
    """Convert a sparse D5 irreducible table to a Weyl character."""
    result = D5(0)
    for label, coefficient in table.items():
        if coefficient:
            result += coefficient * D5(*label)
    return result


def evaluate_polynomial(polynomial, values, zero, one):
    """Evaluate a multivariate polynomial in any commutative target ring."""
    result = zero
    for exponents, coefficient in polynomial.dict().items():
        term = one
        for value, exponent in zip(values, exponents):
            if exponent:
                term *= value ** exponent
        result += coefficient * term
    return result


def evaluate_d5_polynomial(polynomial):
    """Evaluate a fundamental-character polynomial in R(Spin(10))."""
    return evaluate_polynomial(
        D5_POLYNOMIAL_RING(polynomial),
        D5_FUNDAMENTALS,
        D5(0),
        D5_ONE,
    )


def restrict_polynomial(polynomial):
    """Apply the exact polynomial restriction map to a D5 polynomial."""
    return evaluate_polynomial(
        D5_POLYNOMIAL_RING(polynomial),
        D5_TO_B4_SUBSTITUTIONS,
        B4_POLYNOMIAL_RING.zero(),
        B4_POLYNOMIAL_RING.one(),
    )


def section_polynomial(polynomial):
    """Apply the fixed polynomial right inverse to a B4 polynomial."""
    return evaluate_polynomial(
        B4_POLYNOMIAL_RING(polynomial),
        B4_TO_D5_SECTION,
        D5_POLYNOMIAL_RING.zero(),
        D5_POLYNOMIAL_RING.one(),
    )


def principal_polynomial_decomposition(polynomial):
    """Decompose a D5 polynomial into its fixed section plus a multiple of J."""
    polynomial = D5_POLYNOMIAL_RING(polynomial)
    restricted = restrict_polynomial(polynomial)
    lifted = section_polynomial(restricted)
    kernel_part = polynomial - lifted
    quotient, remainder = kernel_part.quo_rem(J_POLYNOMIAL)
    return {
        "restricted": restricted,
        "lifted": lifted,
        "kernel_part": kernel_part,
        "quotient": quotient,
        "remainder": remainder,
        "exact": lifted + J_POLYNOMIAL * quotient == polynomial and not remainder,
    }


def _fundamental_monomial(label):
    """Return the Cartan-product monomial for one D5 highest weight."""
    result = D5_POLYNOMIAL_RING.one()
    for generator, exponent in zip(D5_POLYNOMIAL_RING.gens(), label):
        if exponent:
            result *= generator ** exponent
    return result


def irrep_to_fundamental_polynomial(label):
    """Express one D5 irreducible exactly in fundamental-character variables.

    The product of fundamental representations selected by the Dynkin labels
    contains the requested Cartan component with multiplicity one.  All other
    components are lower in dominance order, so recursive triangular
    subtraction terminates.
    """
    label = tuple(_integer(value, "D5 Dynkin label") for value in label)
    if min(label) < 0:
        raise ValueError(f"D5 Dynkin labels must be nonnegative: {label}")
    cached = _D5_IRREP_POLYNOMIAL_CACHE.get(label)
    if cached is not None:
        return cached
    if label in _D5_ACTIVE_LABELS:
        raise ValueError(f"Triangular fundamental conversion cycled at {label}")

    _D5_ACTIVE_LABELS.add(label)
    try:
        monomial = _fundamental_monomial(label)
        product_character = evaluate_d5_polynomial(monomial)
        components = character_table(product_character)
        leading_coefficient = components.pop(label, 0)
        if leading_coefficient != 1:
            raise ValueError(
                "Cartan component does not have multiplicity one for "
                f"{label}: {leading_coefficient}"
            )

        result = monomial
        for lower_label, coefficient in components.items():
            result -= coefficient * irrep_to_fundamental_polynomial(lower_label)

        if evaluate_d5_polynomial(result) != D5(*label):
            raise ValueError(f"Fundamental conversion failed for {label}")
        _D5_IRREP_POLYNOMIAL_CACHE[label] = result
        return result
    finally:
        _D5_ACTIVE_LABELS.remove(label)


def character_to_fundamental_polynomial(character):
    """Express a finite virtual D5 character in fundamental variables."""
    result = D5_POLYNOMIAL_RING.zero()
    for label, coefficient in character_table(character).items():
        result += coefficient * irrep_to_fundamental_polynomial(label)
    if evaluate_d5_polynomial(result) != character:
        raise ValueError("Character-to-polynomial round trip failed")
    return result


def divide_kernel_character(character):
    """Divide a restriction-kernel character exactly by 16_+ - 16_-.

    Returns the quotient both as a fundamental-character polynomial and as a
    virtual D5 Weyl character.  Any nonzero polynomial remainder is reported as
    a mathematical obstruction.
    """
    if character.branch(B4, rule="default") != B4(0):
        raise ValueError("Character is not in the D5 -> B4 restriction kernel")
    polynomial = character_to_fundamental_polynomial(character)
    quotient, remainder = polynomial.quo_rem(J_POLYNOMIAL)
    if remainder:
        raise ValueError(
            "Kernel polynomial was not divisible by the half-spinor "
            f"difference: remainder={remainder}"
        )
    quotient_character = evaluate_d5_polynomial(quotient)
    if J_CHARACTER * quotient_character != character:
        raise ValueError("Half-spinor quotient failed exact character verification")
    return {
        "polynomial": polynomial,
        "quotient_polynomial": quotient,
        "quotient_character": quotient_character,
    }


def relation_character(generator):
    """Return the Weyl character of one natural finite kernel generator."""
    return character_from_table(generator.as_dict())


def family_name(top_weight):
    """Return the TK family name for a finite natural generator."""
    ell, m, r, s = top_weight
    prefix = {
        (0, 0, 2): "A",
        (1, 0, 2): "B",
        (0, 0, 3): "C",
    }.get((m, r, s), f"F({m},{r},{s})")
    return f"{prefix}_{ell}"


def expected_family_quotient(top_weight):
    """Return the observed closed quotient pattern for the A, B and C families.

    This is used as an exact finite-window diagnostic.  Agreement at finitely
    many values of ``ell`` is not by itself promoted to an all-orders proof.
    """
    ell, m, r, s = top_weight
    if (m, r, s) == (0, 0, 2):
        return sum(
            (D5(index, 0, 0, 0, 1) for index in range(ell + 1)),
            D5(0),
        )
    if (m, r, s) == (1, 0, 2):
        return sum(
            (
                D5(index + 1, 0, 0, 0, 1)
                + D5(index, 1, 0, 0, 1)
                for index in range(ell + 1)
            ),
            D5(0),
        )
    if (m, r, s) == (0, 0, 3):
        return sum(
            (D5(index, 0, 0, 0, 2) for index in range(ell + 1)),
            D5(0),
        )
    return None


def quotient_diagnostics(generator):
    """Factor one finite kernel generator and classify its quotient."""
    character = relation_character(generator)
    division = divide_kernel_character(character)
    quotient = division["quotient_character"]
    table = character_table(quotient)
    coefficients = tuple(table.values())
    integral = all(coefficient in ZZ for coefficient in coefficients)
    positive = integral and all(coefficient >= 0 for coefficient in coefficients)
    expected = expected_family_quotient(generator.top_weight)
    return {
        "name": family_name(generator.top_weight),
        "top_weight": generator.top_weight,
        "first_hft_level": generator.first_hft_level,
        "reduced_depth": generator.reduced_depth,
        "relation": character,
        "relation_terms": len(character_table(character)),
        "quotient": quotient,
        "quotient_table": table,
        "quotient_terms": len(table),
        "minimum_coefficient": min(coefficients, default=0),
        "maximum_coefficient": max(coefficients, default=0),
        "integral": integral,
        "positive": positive,
        "irreducible": positive and len(table) == 1 and coefficients == (1,),
        "exact": J_CHARACTER * quotient == character,
        "expected_family_quotient": expected,
        "family_pattern_matches": expected is not None and quotient == expected,
        "polynomial": division["polynomial"],
        "quotient_polynomial": division["quotient_polynomial"],
    }


def fundamental_restriction_diagnostics():
    """Verify the fundamental restrictions and polynomial right inverse."""
    expected = (
        B4_ONE + B4_FUNDAMENTALS[0],
        B4_FUNDAMENTALS[0] + B4_FUNDAMENTALS[1],
        B4_FUNDAMENTALS[1] + B4_FUNDAMENTALS[2],
        B4_FUNDAMENTALS[3],
        B4_FUNDAMENTALS[3],
    )
    actual = tuple(
        fundamental.branch(B4, rule="default")
        for fundamental in D5_FUNDAMENTALS
    )
    section_checks = tuple(
        restrict_polynomial(section) == generator
        for section, generator in zip(B4_TO_D5_SECTION, B4_POLYNOMIAL_RING.gens())
    )
    return {
        "actual": actual,
        "expected": expected,
        "restrictions_exact": actual == expected,
        "spinors_identified": actual[3] == actual[4],
        "j_restricts_to_zero": J_CHARACTER.branch(B4, rule="default") == B4(0),
        "section_checks": section_checks,
        "section_is_right_inverse": all(section_checks),
        "j_polynomial_restricts_to_zero": restrict_polynomial(J_POLYNOMIAL) == 0,
    }


def seed_diagnostics(records):
    """Verify the two simple nontransported seed factorizations."""
    by_top = {record["top_weight"]: record for record in records}
    a0 = by_top.get((0, 0, 0, 2))
    c0 = by_top.get((0, 0, 0, 3))
    return {
        "a0_present": a0 is not None,
        "c0_present": c0 is not None,
        "a0_is_spin_minus_times_j": (
            a0 is not None and a0["quotient"] == SPIN_MINUS
        ),
        "c0_is_126_minus_times_j": (
            c0 is not None and c0["quotient"] == D5(0, 0, 0, 0, 2)
        ),
    }


def analyze_principal_ideal(max_level=11):
    """Run the complete baseline-free TK6a finite-window analysis."""
    fundamentals = fundamental_restriction_diagnostics()
    domain = kernel_lattice.build_finite_domain(max_level)
    generators = kernel_lattice.natural_kernel_generators(domain)
    records = tuple(
        sorted(
            (quotient_diagnostics(generator) for generator in generators),
            key=lambda record: (record["name"][0], record["top_weight"][0]),
        )
    )
    seeds = seed_diagnostics(records)
    return {
        "max_level": max_level,
        "fundamentals": fundamentals,
        "domain": domain,
        "generators": generators,
        "records": records,
        "seeds": seeds,
        "all_factor_exactly": all(record["exact"] for record in records),
        "all_quotients_integral": all(record["integral"] for record in records),
        "positive_quotients": sum(record["positive"] for record in records),
        "irreducible_quotients": sum(record["irreducible"] for record in records),
        "all_family_patterns_match": all(
            record["family_pattern_matches"] for record in records
        ),
    }


def run_analysis(max_level=11, verbose=False):
    """Print the reproducible TK6a analysis."""
    print("=" * 80)
    print("TK6a — PRINCIPAL D5 -> B4 RESTRICTION-KERNEL IDEAL")
    print("=" * 80)
    started = time.time()
    result = analyze_principal_ideal(max_level=max_level)
    fundamentals = result["fundamentals"]

    print("\nFundamental restriction presentation:")
    for index, (actual, expected) in enumerate(
        zip(fundamentals["actual"], fundamentals["expected"]),
        start=1,
    ):
        print(f"  f{index}: {actual}  expected={expected}  exact={actual == expected}")
    print(f"  Polynomial section is a right inverse: {fundamentals['section_is_right_inverse']}")
    print(f"  J = 16_+ - 16_- restricts to zero: {fundamentals['j_restricts_to_zero']}")

    print(f"\nFinite level-{max_level} kernel quotient analysis:")
    print("  name   top weight       first  q-terms  min/max   positive  pattern  exact")
    for record in result["records"]:
        first = "-" if record["first_hft_level"] is None else record["first_hft_level"]
        bounds = f"{record['minimum_coefficient']}/{record['maximum_coefficient']}"
        print(
            f"  {record['name']:<6} {str(record['top_weight']):<16} "
            f"{str(first):<6} {record['quotient_terms']:<8} {bounds:<9} "
            f"{str(record['positive']):<9} "
            f"{str(record['family_pattern_matches']):<8} "
            f"{record['exact']}"
        )
        if verbose:
            print(f"         K/J = {record['quotient']}")

    print("\nSeed identities:")
    print(f"  A_0 = 16_- J: {result['seeds']['a0_is_spin_minus_times_j']}")
    print(f"  C_0 = 126_- J: {result['seeds']['c0_is_126_minus_times_j']}")
    print("\nSummary:")
    print(f"  Natural finite generators: {len(result['records'])}")
    print(f"  Exact J-factorizations: {result['all_factor_exactly']}")
    print(f"  Integral quotients: {result['all_quotients_integral']}")
    print(
        "  Positive / irreducible quotients: "
        f"{result['positive_quotients']} / {result['irreducible_quotients']}"
    )
    print(f"  A/B/C partial-sum patterns all match: {result['all_family_patterns_match']}")
    print(f"  Runtime: {time.time() - started:.3f}s")
    print("\nProtected SO(10) baseline imported: NO")
    return result


def run_self_test():
    """Run fast exact structural and seed-factorization tests."""
    fundamentals = fundamental_restriction_diagnostics()
    if not fundamentals["restrictions_exact"]:
        raise AssertionError("Fundamental branching presentation failed")
    if not fundamentals["section_is_right_inverse"]:
        raise AssertionError("Polynomial restriction section is not a right inverse")
    if not fundamentals["j_restricts_to_zero"]:
        raise AssertionError("Half-spinor difference does not restrict to zero")
    if not fundamentals["j_polynomial_restricts_to_zero"]:
        raise AssertionError("Polynomial half-spinor difference does not vanish")

    sample_polynomial = (
        F1 ** 2 * F4
        - 3 * F2 * F5
        + F3
        + 2 * F4 * F5
        - 7
    )
    sample_decomposition = principal_polynomial_decomposition(sample_polynomial)
    if not sample_decomposition["exact"]:
        raise AssertionError("Principal polynomial decomposition failed")

    a0 = (
        D5(0, 0, 0, 1, 1)
        - D5(0, 0, 0, 0, 2)
        - D5(0, 0, 1, 0, 0)
        + D5(0, 1, 0, 0, 0)
        - D5(1, 0, 0, 0, 0)
        + D5_ONE
    )
    c0 = (
        D5(0, 0, 0, 1, 2)
        - D5(0, 0, 0, 0, 3)
        - D5(0, 0, 1, 0, 1)
        + D5(0, 1, 0, 0, 1)
        + D5(0, 0, 0, 0, 1)
        - D5(1, 0, 0, 0, 1)
    )
    a0_division = divide_kernel_character(a0)
    c0_division = divide_kernel_character(c0)
    if a0_division["quotient_character"] != SPIN_MINUS:
        raise AssertionError("A_0 / J is not the expected 16_-")
    if c0_division["quotient_character"] != D5(0, 0, 0, 0, 2):
        raise AssertionError("C_0 / J is not the expected 126_-")

    sample = D5(2, 1, 0, 1, 0) - D5(1, 0, 0, 0, 1)
    polynomial = character_to_fundamental_polynomial(sample)
    if evaluate_d5_polynomial(polynomial) != sample:
        raise AssertionError("General fundamental-polynomial round trip failed")

    print("TK6a PRINCIPAL-IDEAL SELF-TEST")
    print("  Fundamental restriction presentation: PASS")
    print("  Polynomial right inverse: PASS")
    print("  Principal polynomial decomposition: PASS")
    print("  Irreducible/fundamental round trip: PASS")
    print("  A_0 = 16_- J: PASS")
    print("  C_0 = 126_- J: PASS")
    print("  Protected SO(10) baseline imported: NO")
    return True


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Factor the finite D5 -> B4 kernel through 16_+ - 16_-"
    )
    parser.add_argument("--max-level", type=int, default=11)
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)

    try:
        if args.self_test:
            run_self_test()
        else:
            run_analysis(max_level=args.max_level, verbose=args.verbose)
    except Exception as error:
        print(f"TK6a FAILED: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
