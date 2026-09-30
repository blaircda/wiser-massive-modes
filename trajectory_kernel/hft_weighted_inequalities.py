"""TK6B.5: pull weighted circuit facets back to local HFT inequalities.

The all-chiral D5 -> B4 section has a closed inverse.  If ``M`` is a
finite B4 multiplicity table, the coefficient of the selected parent

    [ell, m, r, 0, s]

is the three-fold forward difference of ``M`` in orthogonal highest-weight
coordinates.  This module implements that formula, verifies it independently
against the exact triangular packet solve, and pulls arbitrary weighted
circuit functionals back to sparse B4 multiplicity functionals.

No protected SO(10) completion is imported.
"""

import argparse
import itertools
import sys
import time
from collections import defaultdict

from sage.all import ZZ, vector

import finite_cross_section as cross
from trajectory_kernel import kernel_lattice
from trajectory_kernel import restriction_semigroup


def orthogonal_forward_shift(label, epsilon):
    """Shift the first three orthogonal coordinates of a B4 highest weight.

    ``epsilon=(e1,e2,e3)`` adds ``ei`` to the corresponding orthogonal
    coordinate while leaving the fourth coordinate fixed.  ``None`` denotes
    a point outside the dominant chamber.
    """
    ell, m, r, s = map(int, label)
    e1, e2, e3 = map(int, epsilon)
    if any(value not in (0, 1) for value in (e1, e2, e3)):
        raise ValueError("Forward-shift entries must be zero or one")
    shifted = (
        ell + e1 - e2,
        m + e2 - e3,
        r + e3,
        s,
    )
    return None if min(shifted) < 0 else shifted


def mobius_coordinate(multiplicities, label):
    """Return one all-chiral section coefficient by local Möbius inversion."""
    total = 0
    for epsilon in itertools.product((0, 1), repeat=3):
        shifted = orthogonal_forward_shift(label, epsilon)
        if shifted is None:
            continue
        sign = -1 if sum(epsilon) % 2 else 1
        total += sign * multiplicities.get(shifted, 0)
    if total not in ZZ:
        raise ValueError(f"Non-integral Möbius coordinate at {label}: {total}")
    return int(total)


def mobius_section_coordinates(multiplicities, labels):
    """Evaluate the closed all-chiral inverse on an ordered label family."""
    return tuple(
        mobius_coordinate(multiplicities, tuple(label)) for label in labels
    )


def triangular_section_coordinates(domain, level):
    """Compute the same coordinates by an independent exact matrix solve."""
    _parents, reference = restriction_semigroup.reference_matrix(domain)
    if abs(int(reference.det())) != 1:
        raise ValueError("All-chiral reference matrix is not unimodular")
    target = restriction_semigroup.target_vector(domain, level)
    solved = reference.solve_right(vector(ZZ, target))
    if any(value not in ZZ for value in solved):
        raise ValueError("Triangular section coordinates are not integral")
    return tuple(int(value) for value in solved)


def verify_mobius_formula(domain, levels=None):
    """Compare the local formula with exact packet-matrix inversion."""
    if levels is None:
        levels = tuple(sorted(domain["cumulative"]))
    checks = {}
    for level in levels:
        table = cross.character_coefficients(domain["cumulative"][level])
        local = mobius_section_coordinates(table, domain["weights"])
        matrix_coordinates = triangular_section_coordinates(domain, level)
        checks[int(level)] = local == matrix_coordinates
        if not checks[int(level)]:
            mismatch = next(
                (
                    (weight, left, right)
                    for weight, left, right in zip(
                        domain["weights"], local, matrix_coordinates
                    )
                    if left != right
                ),
                None,
            )
            raise ValueError(f"Möbius formula mismatch at level {level}: {mismatch}")
    return checks


def pullback_coordinate_functional(coordinate_coefficients):
    """Pull a section-coordinate functional back to B4 multiplicities.

    The input is a sparse table ``alpha[mu]`` representing

        sum_mu alpha[mu] c_mu.

    The output is the unique sparse table ``beta`` such that this equals

        sum_lambda beta[lambda] M(lambda)

    under the local Möbius formula.
    """
    pulled = defaultdict(int)
    for label, coefficient in coordinate_coefficients.items():
        coefficient = int(coefficient)
        if not coefficient:
            continue
        for epsilon in itertools.product((0, 1), repeat=3):
            shifted = orthogonal_forward_shift(label, epsilon)
            if shifted is None:
                continue
            sign = -1 if sum(epsilon) % 2 else 1
            pulled[shifted] += sign * coefficient
    return dict(sorted((label, value) for label, value in pulled.items() if value))


def evaluate_functional(functional, multiplicities):
    """Evaluate one sparse integral multiplicity functional exactly."""
    value = sum(
        int(coefficient) * multiplicities.get(tuple(label), 0)
        for label, coefficient in functional.items()
    )
    if value not in ZZ:
        raise ValueError(f"Non-integral functional value: {value}")
    return int(value)


def translate_label(label, delta):
    """Translate a Dynkin label, returning ``None`` outside the chamber."""
    if len(label) != 4 or len(delta) != 4:
        raise ValueError("B4 labels and translations must have four entries")
    shifted = tuple(int(value) + int(step) for value, step in zip(label, delta))
    return None if min(shifted) < 0 else shifted


def translate_table(multiplicities, delta):
    """Translate a finite multiplicity table in the B4 Dynkin lattice."""
    result = defaultdict(int)
    for label, multiplicity in multiplicities.items():
        shifted = translate_label(label, delta)
        if shifted is None:
            raise ValueError(
                f"Translation {delta} moves {label} outside the dominant chamber"
            )
        result[shifted] += multiplicity
    return dict(sorted((label, value) for label, value in result.items() if value))


def translation_equivariance_check(multiplicities, labels, delta):
    """Check that the local section inverse commutes with one translation."""
    translated = translate_table(multiplicities, delta)
    comparisons = []
    for label in labels:
        shifted = translate_label(label, delta)
        if shifted is None:
            raise ValueError("Requested comparison leaves the dominant chamber")
        comparisons.append(
            mobius_coordinate(translated, shifted)
            == mobius_coordinate(multiplicities, label)
        )
    return all(comparisons)


def verify_pullback_identity(multiplicities, coordinate_coefficients):
    """Check the coordinate and multiplicity evaluations agree exactly."""
    left = sum(
        int(coefficient) * mobius_coordinate(multiplicities, tuple(label))
        for label, coefficient in coordinate_coefficients.items()
    )
    pulled = pullback_coordinate_functional(coordinate_coefficients)
    right = evaluate_functional(pulled, multiplicities)
    return {
        "coordinate_value": int(left),
        "multiplicity_value": right,
        "pulled_functional": pulled,
        "exact": left == right,
    }


def cumulative_commutation_checks(domain):
    """Check that Möbius inversion commutes with cumulative level sums."""
    running = {weight: 0 for weight in domain["weights"]}
    coordinate_running = [0] * len(domain["weights"])
    checks = {}
    for level in sorted(domain["single_levels"]):
        single_table = cross.character_coefficients(domain["single_levels"][level])
        for weight, value in single_table.items():
            running[weight] = running.get(weight, 0) + value
        single_coordinates = mobius_section_coordinates(
            single_table, domain["weights"]
        )
        coordinate_running = [
            old + new
            for old, new in zip(coordinate_running, single_coordinates)
        ]
        cumulative_table = cross.character_coefficients(domain["cumulative"][level])
        direct = mobius_section_coordinates(cumulative_table, domain["weights"])
        checks[level] = (
            all(running.get(weight, 0) == cumulative_table.get(weight, 0)
                for weight in set(running) | set(cumulative_table))
            and tuple(coordinate_running) == direct
        )
        if not checks[level]:
            raise ValueError(f"Cumulative commutation failed at level {level}")
    return checks


def _synthetic_packet_table(parent):
    return cross.character_coefficients(cross.branch_parent(tuple(parent)))


def synthetic_formula_checks():
    """Exercise the formula on packets, mixtures, and chamber boundaries."""
    parents = (
        (0, 0, 0, 0, 0),
        (2, 0, 0, 0, 0),
        (0, 2, 0, 0, 0),
        (0, 0, 2, 0, 0),
        (1, 1, 1, 0, 2),
    )
    coefficients = (3, -2, 4, 1, 2)
    target = defaultdict(int)
    expected = defaultdict(int)
    support = set()
    for parent, coefficient in zip(parents, coefficients):
        packet = _synthetic_packet_table(parent)
        for label, multiplicity in packet.items():
            target[label] += coefficient * multiplicity
            support.add(label)
        top = cross.top_b4_weight(parent)
        if parent == cross.select_parent(top, policy="chiral"):
            expected[top] += coefficient
        else:
            # This test only asserts selected-packet recovery term by term.
            # A non-reference packet is deliberately omitted below.
            for label, multiplicity in packet.items():
                target[label] -= coefficient * multiplicity
    recovered = {
        label: mobius_coordinate(target, label)
        for label in support
    }
    inversion_ok = all(
        recovered.get(label, 0) == value for label, value in expected.items()
    ) and all(
        value == expected.get(label, 0) for label, value in recovered.items()
    )
    translations_ok = all(
        translation_equivariance_check(target, support, delta)
        for delta in ((1, 0, 0, 0), (0, 2, 0, 0), (0, 0, 1, 0))
    )
    return inversion_ok and translations_ok


def run_analysis(max_level=10):
    """Run the baseline-free TK6B.5 Möbius and pullback audit."""
    started = time.time()
    domain = kernel_lattice.build_finite_domain(max_level)
    formula_checks = verify_mobius_formula(domain)
    cumulative_checks = cumulative_commutation_checks(domain)

    # A deliberately weighted functional tests the general pullback, including
    # labels on dominance walls.  It is not asserted to be a cone facet.
    labels = domain["weights"]
    coordinate_functional = {
        label: coefficient
        for label, coefficient in zip(labels[: min(5, len(labels))], (2, -1, 3, 1, -2))
    }
    final_table = cross.character_coefficients(domain["cumulative"][max_level])
    pullback = verify_pullback_identity(final_table, coordinate_functional)
    synthetic_ok = synthetic_formula_checks()

    print("=" * 96)
    print("TK6B.5 — LOCAL HFT WEIGHTED-INEQUALITY PULLBACK")
    print("=" * 96)
    print(f"HFT levels checked: 1 through {max_level}")
    print(f"B4 labels in complete closure: {len(domain['weights'])}")
    print(f"Local Möbius formula agrees with exact matrix inversion: {all(formula_checks.values())}")
    print(f"Möbius inversion commutes with cumulative sums: {all(cumulative_checks.values())}")
    print(f"Weighted functional pullback identity exact: {pullback['exact']}")
    print(f"Synthetic selected-packet and boundary checks: {synthetic_ok}")
    print(f"Protected SO(10) baseline imported: NO")
    print(f"Runtime: {time.time() - started:.3f}s")
    return {
        "domain": domain,
        "formula_checks": formula_checks,
        "cumulative_checks": cumulative_checks,
        "pullback": pullback,
        "synthetic_ok": synthetic_ok,
        "all_checks": (
            all(formula_checks.values())
            and all(cumulative_checks.values())
            and pullback["exact"]
            and synthetic_ok
        ),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Pull all-chiral section coordinates back to local HFT differences"
    )
    parser.add_argument("--max-level", type=int, default=10)
    args = parser.parse_args(argv)
    try:
        result = run_analysis(max_level=args.max_level)
    except Exception as error:
        print(f"TK6B.5 FAILED: {error}", file=sys.stderr)
        return 1
    return 0 if result["all_checks"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
