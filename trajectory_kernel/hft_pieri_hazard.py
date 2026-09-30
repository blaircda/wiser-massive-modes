"""TK6B.5e: coupling-aware support bounds for the HFT remainder.

The four linear forms whose maximum gives the GMSZ exterior cost are useful
support functionals, but they are not multiplicative filtrations of the B4
representation ring.  This module replaces that failed shortcut by a finite
source invariant tailored to the already-proved stable Pieri theorem.

For a dominant B4 label ``mu``, define its Pieri hazard by

    H(mu) = max(E(lambda) - k),

where ``lambda`` ranges over unstable constituents of ``mu * H_k`` and
``H_k = [k,0,0,0]`` is the harmonic one-row representation.  Only
``k < 2 mu_1`` can contribute: if ``H_k`` occurs in ``mu * lambda``, the
weight-polytope coordinate bound gives ``k <= mu_1 + lambda_1``.  Hence an
unstable constituent with ``lambda_1 < mu_1`` forces ``k < 2 mu_1``.

Since ``Sym^R(V)`` is the sum of ``H_{R-2j}``, the exact source-degree bound

    d >= H(mu)

implies ``E(lambda) <= d + R`` for every unstable constituent of
``mu * Sym^R(V)``.  Combining this with ``d >= E(mu)-1`` also excludes the
unpaired top-degree remainder term from the exterior GMSZ chamber.

The implementation derives the HFT spectrum without importing a protected
SO(10) completion.  Finite computations are theorem diagnostics, not a proof
of the remaining all-degree HFT support bound.
"""

import argparse
import sys
import time
from functools import lru_cache
from itertools import product

from sage.all import CartanType, QQ, ZZ

import hft_so9
from trajectory_kernel import chamber_audit
from trajectory_kernel import regge_factorization
from trajectory_kernel import stable_pieri


B4 = hft_so9.B4
RHO_ORTHOGONAL = (QQ(7) / 2, QQ(5) / 2, QQ(3) / 2, QQ(1) / 2)

# E(label) = max(L_i(label) - shift_i).
LINEAR_FORMS = (
    (2, 3, 6, 5),
    (2, 3, 6, 4),
    (2, 3, 6, 3),
    (2, 3, 0, 2),
)
EXTERIOR_SHIFTS = (6, 2, 1, -1)

# Additional affine pieces in the exact Pieri hazard away from the dominance
# wall ell=0.  Each pair represents L(label) - shift.
WALL_HAZARD_FORMS = (
    ((2, 5, 6, 3), 4),
    ((2, 5, 7, 4), 5),
    ((2, 5, 9, 5), 9),
)

# Maximizing the four exterior-cost pieces on the odd-orthogonal horizontal-
# strip polytope gives these affine expressions in orthogonal coordinates
# (a,b,c,d).  The fourth is dominated by the original E(mu)-1 threshold.
ORTHOGONAL_HAZARD_FORMS = (
    ((2, 3, 4, 1), 9),
    ((2, 3, 2, 1), 5),
    ((2, 3, 1, 0), 4),
    ((2, 1, 0, 1), 2),
)


def linear_form(label, coefficients):
    """Evaluate one integral linear form on a B4 Dynkin label."""
    if len(label) != 4 or min(label) < 0:
        raise ValueError(f"Expected a dominant B4 Dynkin label: {label}")
    return sum(int(a) * int(b) for a, b in zip(coefficients, label))


def exterior_cost_from_forms(label):
    """Evaluate the exterior cost from its four affine support forms."""
    return max(
        linear_form(label, coefficients) - shift
        for coefficients, shift in zip(LINEAR_FORMS, EXTERIOR_SHIFTS)
    )


def twice_first_orthogonal_coordinate(label):
    """Return twice the first orthogonal coordinate of a B4 highest weight."""
    ell, m, r, s = label
    return 2 * ell + 2 * m + 2 * r + s


def orthogonal_coordinates(label):
    """Return the dominant orthogonal coordinates of a B4 Dynkin label."""
    ell, m, r, s = map(int, label)
    return (
        QQ(ell + m + r) + QQ(s) / 2,
        QQ(m + r) + QQ(s) / 2,
        QQ(r) + QQ(s) / 2,
        QQ(s) / 2,
    )


def shifted_spin_partition(label):
    """Remove the universal half-spin shift from a spinorial B4 weight."""
    if int(label[3]) % 2 != 1:
        raise ValueError(f"Expected a spinorial B4 label: {label}")
    shifted = tuple(value - QQ(1) / 2 for value in orthogonal_coordinates(label))
    if any(value not in ZZ or value < 0 for value in shifted):
        raise ValueError(f"Invalid shifted spin partition: {label} -> {shifted}")
    return tuple(int(value) for value in shifted)


def shifted_spin_partition_to_label(partition):
    """Convert an integral shifted spin partition back to a B4 label."""
    first, second, third, fourth = map(int, partition)
    if not first >= second >= third >= fourth >= 0:
        raise ValueError(f"Expected a four-row partition: {partition}")
    return (
        first - second,
        second - third,
        third - fourth,
        2 * fourth + 1,
    )


def _intermediate_partitions(left, right):
    """Enumerate partitions interlacing two four-row partitions."""
    ranges = []
    for index in range(4):
        lower = max(
            left[index + 1] if index < 3 else 0,
            right[index + 1] if index < 3 else 0,
        )
        upper = min(left[index], right[index])
        if lower > upper:
            return ()
        ranges.append(range(lower, upper + 1))
    return product(*ranges)


def spin_pieri_formula_multiplicity(source, target, degree):
    """Evaluate the shifted-partition Pieri formula in the spinorial coset.

    The Weyl character formula gives

        ch_B(alpha + omega_4) = ch_B(omega_4) ch_C(alpha),

    while restriction to the common torus gives

        ch_B(H_k) = ch_C(H_k) + ch_C(H_{k-1}).

    Symplectic Pieri therefore counts interlacing partitions whose two
    horizontal-strip sizes sum to either ``k`` or ``k-1``.
    """
    degree = int(degree)
    if degree < 0:
        return 0
    left = shifted_spin_partition(tuple(source))
    right = shifted_spin_partition(tuple(target))
    multiplicity = 0
    for intermediate in _intermediate_partitions(left, right):
        gap = sum(left) + sum(right) - 2 * sum(intermediate)
        if gap in (degree, degree - 1):
            multiplicity += 1
    return multiplicity


def _bounded_four_row_partitions(maximum_part):
    """Enumerate four-row partitions with first part at most the bound."""
    for first in range(int(maximum_part) + 1):
        for second in range(first + 1):
            for third in range(second + 1):
                for fourth in range(third + 1):
                    yield (first, second, third, fourth)


def spin_pieri_formula_audit(maximum_label_sum=3, extra_degrees=1):
    """Compare the shifted spin-Pieri formula with exact B4 products."""
    maximum_label_sum = int(maximum_label_sum)
    sources = tuple(
        label
        for label in product(range(maximum_label_sum + 1), repeat=4)
        if sum(label) <= maximum_label_sum and label[3] % 2 == 1
    )
    failures = []
    tested = 0
    for source in sources:
        shifted_source = shifted_spin_partition(source)
        maximum_degree = (
            twice_first_orthogonal_coordinate(source) + int(extra_degrees)
        )
        for degree in range(maximum_degree + 1):
            exact = harmonic_product_table(source, degree)
            predicted = {}
            for partition in _bounded_four_row_partitions(
                shifted_source[0] + degree
            ):
                target = shifted_spin_partition_to_label(partition)
                multiplicity = spin_pieri_formula_multiplicity(
                    source, target, degree
                )
                if multiplicity:
                    predicted[target] = multiplicity
            for target in set(exact) | set(predicted):
                tested += 1
                if exact.get(target, 0) != predicted.get(target, 0):
                    failures.append(
                        {
                            "source": source,
                            "harmonic_degree": degree,
                            "target": target,
                            "exact": exact.get(target, 0),
                            "formula": predicted.get(target, 0),
                        }
                    )
    return {
        "sources": len(sources),
        "tested_constituents": tested,
        "failures": tuple(failures),
        "all_match": not failures,
    }


@lru_cache(maxsize=None)
def harmonic_product_table(label, degree):
    """Return the exact irreducible table of ``V_label tensor H_degree``."""
    degree = int(degree)
    if degree < 0:
        raise ValueError("Harmonic degree must be nonnegative")
    return regge_factorization.character_table(
        B4(*label) * B4(degree, 0, 0, 0)
    )


@lru_cache(maxsize=None)
def pieri_hazard_data(label):
    """Return the exact finite unstable harmonic hazard of ``label``.

    The cutoff ``k < 2 mu_1`` follows from the weight-polytope coordinate
    bound explained in the module docstring, not from an empirical level
    cutoff.
    """
    label = tuple(int(value) for value in label)
    maximum_harmonic_degree = twice_first_orthogonal_coordinate(label) - 1
    records = []
    for degree in range(maximum_harmonic_degree + 1):
        for target, multiplicity in harmonic_product_table(label, degree).items():
            if stable_pieri.stable_pieri_hypothesis(target, label):
                continue
            records.append(
                {
                    "harmonic_degree": degree,
                    "target": target,
                    "multiplicity": multiplicity,
                    "target_cost": stable_pieri.exterior_cost(target),
                    "hazard": stable_pieri.exterior_cost(target) - degree,
                }
            )
    maximum = max((record["hazard"] for record in records), default=None)
    maximizers = tuple(
        record for record in records if record["hazard"] == maximum
    )
    return {
        "label": label,
        "maximum_harmonic_degree": maximum_harmonic_degree,
        "records": tuple(records),
        "hazard": maximum,
        "maximizers": maximizers,
    }


def _orthogonal_to_dynkin(vector):
    """Convert a dominant B4 orthogonal-coordinate vector to Dynkin labels."""
    values = tuple(QQ(value) for value in vector)
    dynkin = (
        values[0] - values[1],
        values[1] - values[2],
        values[2] - values[3],
        2 * values[3],
    )
    if any(value not in ZZ or value < 0 for value in dynkin):
        return None
    return tuple(int(value) for value in dynkin)


@lru_cache(maxsize=None)
def racah_candidate_hazard_data(label):
    """Bound the hazard using the uncancelled Racah--Speiser terms.

    For each weight ``nu`` of ``V_mu`` and each analytically allowed harmonic
    degree, dominantize ``nu + k e_1 + rho``.  Subtracting ``rho`` gives every
    target which can occur in a nonzero Racah--Speiser summand.  Alternating
    Weyl cancellations are deliberately ignored, so this is an exact upper
    support bound rather than a tensor-product decomposition.
    """
    label = tuple(int(value) for value in label)
    maximum_harmonic_degree = twice_first_orthogonal_coordinate(label) - 1
    weights = B4(*label).weight_multiplicities()
    candidates = {}
    for degree in range(maximum_harmonic_degree + 1):
        for weight in weights:
            shifted = list(weight.to_vector())
            shifted[0] += degree
            shifted = tuple(
                QQ(shifted[index]) + RHO_ORTHOGONAL[index]
                for index in range(4)
            )
            absolute = tuple(abs(value) for value in shifted)
            if 0 in absolute or len(set(absolute)) < 4:
                continue
            dominant_shifted = tuple(sorted(absolute, reverse=True))
            target_orthogonal = tuple(
                dominant_shifted[index] - RHO_ORTHOGONAL[index]
                for index in range(4)
            )
            target = _orthogonal_to_dynkin(target_orthogonal)
            if target is None:
                continue
            if stable_pieri.stable_pieri_hypothesis(target, label):
                continue
            value = stable_pieri.exterior_cost(target) - degree
            candidates[degree, target] = max(
                candidates.get((degree, target), value), value
            )
    maximum = max(candidates.values(), default=None)
    maximizers = tuple(
        {
            "harmonic_degree": degree,
            "target": target,
            "hazard": value,
        }
        for (degree, target), value in sorted(candidates.items())
        if value == maximum
    )
    return {
        "label": label,
        "hazard": maximum,
        "maximizers": maximizers,
        "candidate_terms": len(candidates),
    }


def racah_hazard_audit(maximum_label_sum=2):
    """Compare exact, uncancelled-Racah and wall-formula hazards."""
    labels = tuple(
        label
        for label in product(range(int(maximum_label_sum) + 1), repeat=4)
        if sum(label) <= int(maximum_label_sum)
    )
    records = []
    for label in labels:
        exact = pieri_hazard_data(label)["hazard"]
        racah = racah_candidate_hazard_data(label)["hazard"]
        records.append(
            {
                "label": label,
                "exact_hazard": exact,
                "racah_hazard": racah,
                "required_degree": required_remainder_degree(label),
                "wall_formula": wall_hazard_formula(label),
            }
        )
    underestimates = tuple(
        record
        for record in records
        if record["exact_hazard"] is not None
        and (
            record["racah_hazard"] is None
            or record["racah_hazard"] < record["exact_hazard"]
        )
    )
    cancellation_gaps = tuple(
        record
        for record in records
        if record["racah_hazard"] is not None
        and (
            record["exact_hazard"] is None
            or record["racah_hazard"] > record["exact_hazard"]
        )
    )
    formula_failures = tuple(
        record
        for record in records
        if record["required_degree"] != record["wall_formula"]
    )
    return {
        "tested": len(records),
        "records": tuple(records),
        "underestimates": underestimates,
        "cancellation_gaps": cancellation_gaps,
        "formula_failures": formula_failures,
        "is_upper_bound": not underestimates,
        "is_exact": not underestimates and not cancellation_gaps,
    }


def required_remainder_degree(label):
    """Return the source degree sufficient for both TK6B.5d obligations."""
    top_boundary_threshold = stable_pieri.exterior_cost(label) - 1
    hazard = pieri_hazard_data(tuple(label))["hazard"]
    if hazard is None:
        return top_boundary_threshold
    return max(top_boundary_threshold, hazard)


def wall_hazard_formula(label):
    """Return the closed Pieri-wall formula for the required source degree.

    If ``ell=0``, then ``mu_1=mu_2`` and horizontal-strip interlacing makes an
    unstable target ``lambda_1 < mu_1`` impossible.  If ``ell>=1``, maximizing
    the four pieces of ``E(lambda)-k`` on the Pieri polytope gives the three
    displayed wall forms and one redundant fourth form.  The same optimization
    applies to the shifted spin partitions because the extra ``k-1`` branch
    only lowers the hazard.
    """
    label = tuple(int(value) for value in label)
    result = stable_pieri.exterior_cost(label) - 1
    if label[0] >= 1:
        result = max(
            result,
            *(
                linear_form(label, coefficients) - shift
                for coefficients, shift in WALL_HAZARD_FORMS
            ),
        )
    return result


def _orthogonal_affine_to_dynkin(coefficients, shift):
    """Convert one affine form in (a,b,c,d) to B4 Dynkin coordinates."""
    first, second, third, fourth = map(int, coefficients)
    spin_coefficient = QQ(first + second + third + fourth) / 2
    dynkin = (
        first,
        first + second,
        first + second + third,
        spin_coefficient,
    )
    if any(value not in ZZ for value in dynkin):
        raise ValueError(f"Non-integral Dynkin affine form: {coefficients}")
    return tuple(int(value) for value in dynkin), int(shift)


def wall_hazard_derivation_audit():
    """Verify the affine conversions used in the Pieri-polytope derivation."""
    converted = tuple(
        _orthogonal_affine_to_dynkin(coefficients, shift)
        for coefficients, shift in ORTHOGONAL_HAZARD_FORMS
    )
    nonredundant = tuple(sorted(converted[:3]))
    expected = tuple(sorted(WALL_HAZARD_FORMS))
    redundant_coefficients, redundant_shift = converted[3]

    # The L3 component of E(mu)-1 is
    # (2,3,6,3).mu - 2.  It exceeds the fourth Pieri maximum by 3r+s.
    dominating_coefficients = LINEAR_FORMS[2]
    dominating_shift = EXTERIOR_SHIFTS[2] + 1
    dominance_difference = tuple(
        left - right
        for left, right in zip(dominating_coefficients, redundant_coefficients)
    )
    return {
        "converted_forms": converted,
        "nonredundant_match": nonredundant == expected,
        "redundant_form": (redundant_coefficients, redundant_shift),
        "dominating_form": (dominating_coefficients, dominating_shift),
        "dominance_difference": dominance_difference,
        "redundant_is_dominated": (
            dominance_difference == (0, 0, 3, 1)
            and dominating_shift == redundant_shift
        ),
    }


def wall_hazard_formula_audit(maximum_label_sum=5):
    """Regress the proved wall formula against exact finite Pieri products."""
    maximum_label_sum = int(maximum_label_sum)
    labels = tuple(
        label
        for label in product(range(maximum_label_sum + 1), repeat=4)
        if sum(label) <= maximum_label_sum
    )
    records = tuple(
        {
            "label": label,
            "exact": required_remainder_degree(label),
            "formula": wall_hazard_formula(label),
        }
        for label in labels
    )
    failures = tuple(
        record for record in records if record["exact"] != record["formula"]
    )
    return {
        "maximum_label_sum": maximum_label_sum,
        "tested": len(records),
        "tensorial_tested": sum(record["label"][3] % 2 == 0 for record in records),
        "spinorial_tested": sum(record["label"][3] % 2 == 1 for record in records),
        "failures": failures,
        "all_match": not failures,
    }


def candidate_filtration_audit(maximum_label_sum=2):
    """Find exact tensor counterexamples to multiplicativity of every L_i."""
    maximum_label_sum = int(maximum_label_sum)
    if maximum_label_sum < 1:
        raise ValueError("maximum_label_sum must be at least one")
    labels = tuple(
        label
        for label in product(range(maximum_label_sum + 1), repeat=4)
        if sum(label) <= maximum_label_sum
    )
    witnesses = [None] * len(LINEAR_FORMS)
    tested_products = 0
    for left in labels:
        for right in labels:
            table = regge_factorization.character_table(B4(*left) * B4(*right))
            tested_products += 1
            for target, multiplicity in table.items():
                for index, coefficients in enumerate(LINEAR_FORMS):
                    if witnesses[index] is not None:
                        continue
                    source_value = linear_form(left, coefficients) + linear_form(
                        right, coefficients
                    )
                    target_value = linear_form(target, coefficients)
                    if target_value > source_value:
                        witnesses[index] = {
                            "form": index + 1,
                            "left": left,
                            "right": right,
                            "target": target,
                            "multiplicity": multiplicity,
                            "source_value": source_value,
                            "target_value": target_value,
                            "excess": target_value - source_value,
                        }
            if all(witnesses):
                break
        if all(witnesses):
            break

    cartan = CartanType(["B", 4]).cartan_matrix()
    simple_root_changes = tuple(
        tuple(
            sum(cartan[root, column] * coefficients[column] for column in range(4))
            for root in range(4)
        )
        for coefficients in LINEAR_FORMS
    )
    return {
        "labels": len(labels),
        "tested_products": tested_products,
        "simple_root_changes": simple_root_changes,
        "witnesses": tuple(witnesses),
        "all_nonmultiplicative": all(witnesses),
    }


def harmonic_cutoff_audit(maximum_label_sum=2, extra_degrees=3):
    """Check the analytic unstable-harmonic cutoff in a small exact sample."""
    labels = tuple(
        label
        for label in product(range(int(maximum_label_sum) + 1), repeat=4)
        if sum(label) <= int(maximum_label_sum)
    )
    failures = []
    tested = 0
    for label in labels:
        cutoff = twice_first_orthogonal_coordinate(label)
        for degree in range(cutoff, cutoff + int(extra_degrees) + 1):
            for target, multiplicity in harmonic_product_table(label, degree).items():
                tested += 1
                if not stable_pieri.stable_pieri_hypothesis(target, label):
                    failures.append(
                        {
                            "source": label,
                            "harmonic_degree": degree,
                            "target": target,
                            "multiplicity": multiplicity,
                        }
                    )
    return {
        "tested_constituents": tested,
        "failures": tuple(failures),
        "all_stable_beyond_cutoff": not failures,
    }


def symmetric_hazard_audit(maximum_label_sum=2, extra_degrees=3):
    """Check that the harmonic hazard controls direct symmetric powers."""
    labels = tuple(
        label
        for label in product(range(int(maximum_label_sum) + 1), repeat=4)
        if sum(label) <= int(maximum_label_sum)
    )
    failures = []
    tested_unstable = 0
    for label in labels:
        data = pieri_hazard_data(label)
        hazard = data["hazard"]
        maximum_degree = max(0, data["maximum_harmonic_degree"]) + int(
            extra_degrees
        )
        for degree in range(maximum_degree + 1):
            table = regge_factorization.character_table(
                B4(*label)
                * regge_factorization.symmetric_vector_coefficient(degree)
            )
            for target, multiplicity in table.items():
                if stable_pieri.stable_pieri_hypothesis(target, label):
                    continue
                tested_unstable += 1
                value = stable_pieri.exterior_cost(target) - degree
                if hazard is None or value > hazard:
                    failures.append(
                        {
                            "source": label,
                            "symmetric_degree": degree,
                            "target": target,
                            "multiplicity": multiplicity,
                            "value": value,
                            "hazard": hazard,
                        }
                    )
    return {
        "tested_unstable_constituents": tested_unstable,
        "failures": tuple(failures),
        "all_controlled": not failures,
    }


def remainder_hazard_audit(remainder):
    """Test the coupling-aware source-degree bound on every HFT remainder term."""
    records = []
    for degree, character in remainder.items():
        for label, coefficient in regge_factorization.character_table(character).items():
            scalar_threshold = stable_pieri.exterior_cost(label) - 1
            hazard = pieri_hazard_data(tuple(label))["hazard"]
            required = required_remainder_degree(label)
            records.append(
                {
                    "degree": degree,
                    "label": label,
                    "coefficient": coefficient,
                    "scalar_threshold": scalar_threshold,
                    "hazard": hazard,
                    "required_degree": required,
                    "margin": degree - required,
                    "hazard_exceeds_scalar": (
                        hazard is not None and hazard > scalar_threshold
                    ),
                }
            )
    failures = tuple(record for record in records if record["margin"] < 0)
    sharpened = tuple(
        record for record in records if record["hazard_exceeds_scalar"]
    )
    return {
        "records": tuple(records),
        "tested": len(records),
        "unique_labels": len({record["label"] for record in records}),
        "minimum_margin": min(
            (record["margin"] for record in records), default=None
        ),
        "tight": sum(record["margin"] == 0 for record in records),
        "sharpened_records": sharpened,
        "failures": failures,
        "all_satisfy": not failures,
    }


def higher_vector_tower(maximum_degree):
    """Return ``PE(q^2/(1-q) V)`` through ``maximum_degree``."""
    maximum_degree = int(maximum_degree)
    factors = [
        {
            mode * multiplicity: regge_factorization.symmetric_vector_coefficient(
                multiplicity
            )
            for multiplicity in range(maximum_degree // mode + 1)
        }
        for mode in range(2, maximum_degree + 1)
    ]
    return hft_so9.multiply_formal_series(factors, maximum_degree)


def factor_higher_vector_tower(remainder):
    """Factor all vector oscillator modes of degree at least two from ``F``."""
    maximum_degree = max(remainder)
    tower = higher_vector_tower(maximum_degree)
    core = {}
    for degree in range(maximum_degree + 1):
        value = remainder[degree]
        for tower_degree in range(1, degree + 1):
            value -= tower[tower_degree] * core[degree - tower_degree]
        core[degree] = value
    reconstructed = {
        degree: sum(
            (
                tower[tower_degree] * core[degree - tower_degree]
                for tower_degree in range(degree + 1)
            ),
            B4(0),
        )
        for degree in range(maximum_degree + 1)
    }
    if reconstructed != remainder:
        raise ValueError("The higher-vector convolution did not reconstruct F")
    return {
        "tower": tower,
        "core": core,
        "reconstructed": reconstructed,
    }


def filtered_character_audit(series):
    """Audit ``degree >= required_remainder_degree(label)`` on a signed series."""
    records = []
    for degree, character in series.items():
        for label, coefficient in regge_factorization.character_table(character).items():
            required = required_remainder_degree(label)
            records.append(
                {
                    "degree": degree,
                    "label": label,
                    "coefficient": coefficient,
                    "required_degree": required,
                    "margin": degree - required,
                }
            )
    failures = tuple(record for record in records if record["margin"] < 0)
    return {
        "records": tuple(records),
        "tested": len(records),
        "negative_coefficients": sum(
            record["coefficient"] < 0 for record in records
        ),
        "minimum_margin": min(
            (record["margin"] for record in records), default=None
        ),
        "failures": failures,
        "all_satisfy": not failures,
    }


def vector_transition_audit(maximum_label_sum=3):
    """Test whether one defining vector raises the required degree by at most two."""
    labels = tuple(
        label
        for label in product(range(int(maximum_label_sum) + 1), repeat=4)
        if sum(label) <= int(maximum_label_sum)
    )
    records = []
    for label in labels:
        source_degree = required_remainder_degree(label)
        for target, multiplicity in harmonic_product_table(label, 1).items():
            increase = required_remainder_degree(target) - source_degree
            records.append(
                {
                    "source": label,
                    "target": target,
                    "multiplicity": multiplicity,
                    "increase": increase,
                }
            )
    failures = tuple(record for record in records if record["increase"] > 2)
    return {
        "tested": len(records),
        "maximum_increase": max(
            (record["increase"] for record in records), default=None
        ),
        "failures": failures,
        "preserves_mode_two_filtration": not failures,
    }


def higher_vector_cancellation_audit(factorization):
    """Locate filtered-support violations cancelled inside the exact convolution."""
    tower = factorization["tower"]
    core = factorization["core"]
    maximum_degree = max(core)
    records = []
    failures = []
    for total_degree in range(maximum_degree + 1):
        contributions = {}
        for tower_degree in range(total_degree + 1):
            table = regge_factorization.character_table(
                tower[tower_degree] * core[total_degree - tower_degree]
            )
            for label, coefficient in table.items():
                if required_remainder_degree(label) <= total_degree:
                    continue
                contributions.setdefault(label, {})[tower_degree] = coefficient
        for label, by_tower_degree in contributions.items():
            residual = sum(by_tower_degree.values())
            record = {
                "total_degree": total_degree,
                "label": label,
                "required_degree": required_remainder_degree(label),
                "contributions": tuple(sorted(by_tower_degree.items())),
                "residual": residual,
                "translation_signature": (
                    total_degree - 2 * label[0],
                    label[1],
                    label[2],
                    label[3],
                    tuple(sorted(by_tower_degree.items())),
                ),
            }
            records.append(record)
            if residual:
                failures.append(record)
    return {
        "records": tuple(records),
        "bad_contribution_labels": len(records),
        "translation_signatures": len(
            {record["translation_signature"] for record in records}
        ),
        "maximum_number_of_summands": max(
            (len(record["contributions"]) for record in records), default=0
        ),
        "failures": tuple(failures),
        "all_cancel": not failures,
    }


def generic_hazard_obstruction():
    """Evaluate the TK6B.5d generic counterexample with the exact hazard."""
    source = (1, 0, 2, 1)
    target = (0, 0, 0, 5)
    harmonic_degree = 3
    multiplicity = harmonic_product_table(source, harmonic_degree).get(target, 0)
    scalar_threshold = stable_pieri.exterior_cost(source) - 1
    hazard_data = pieri_hazard_data(source)
    return {
        "source": source,
        "target": target,
        "harmonic_degree": harmonic_degree,
        "multiplicity": multiplicity,
        "scalar_threshold": scalar_threshold,
        "hazard": hazard_data["hazard"],
        "witness_value": stable_pieri.exterior_cost(target) - harmonic_degree,
        "hazard_is_stronger": hazard_data["hazard"] > scalar_threshold,
    }


def run_analysis(max_level=13, maximum_label_sum=2, formula_label_sum=5):
    """Run the exact TK6B.5e obstruction and HFT hazard audits."""
    if max_level < chamber_audit.GMSZ_FIRST_LEVEL:
        raise ValueError("Use max_level >= 7 to enter the GMSZ chamber")
    started = time.time()
    filtration = candidate_filtration_audit(maximum_label_sum)
    harmonic_cutoff = harmonic_cutoff_audit(maximum_label_sum)
    symmetric_hazard = symmetric_hazard_audit(maximum_label_sum)
    spin_pieri = spin_pieri_formula_audit(maximum_label_sum + 1)
    vector_transition = vector_transition_audit(maximum_label_sum + 1)
    wall_derivation = wall_hazard_derivation_audit()
    wall_formula = wall_hazard_formula_audit(formula_label_sum)
    racah_hazard = racah_hazard_audit(maximum_label_sum)
    generic = generic_hazard_obstruction()

    _numerator, single_levels = hft_so9.derive_hft_spectrum(max_level)
    factorization = regge_factorization.factor_symmetric_vector_tower(
        single_levels, max_level
    )
    remainder = remainder_hazard_audit(factorization["remainder"])
    higher_vector_factorization = factor_higher_vector_tower(
        factorization["remainder"]
    )
    higher_vector_core = filtered_character_audit(
        higher_vector_factorization["core"]
    )
    higher_vector_cancellations = higher_vector_cancellation_audit(
        higher_vector_factorization
    )
    direct_energy = stable_pieri.unstable_coupling_energy_audit(factorization)

    print("=" * 100)
    print("TK6B.5e — COUPLING-AWARE HFT PIERI HAZARD")
    print("=" * 100)
    print(
        "Candidate linear forms with exact tensor counterexamples: "
        f"{sum(witness is not None for witness in filtration['witnesses'])}/4"
    )
    print(
        "Unstable constituents at or beyond the analytic harmonic cutoff: "
        f"{len(harmonic_cutoff['failures'])}"
    )
    print(
        "Direct symmetric-power hazard failures in the small sample: "
        f"{len(symmetric_hazard['failures'])}"
    )
    print(
        "Shifted spin-Pieri constituents/failures: "
        f"{spin_pieri['tested_constituents']}/{len(spin_pieri['failures'])}"
    )
    print(
        "Mode-two vector transitions exceeding filtered degree two: "
        f"{len(vector_transition['failures'])}"
    )
    print(
        "Wall-hazard formula tensor/spin cases/failures: "
        f"{wall_formula['tensorial_tested']}/"
        f"{wall_formula['spinorial_tested']}/"
        f"{len(wall_formula['failures'])}"
    )
    print(
        "Uncancelled Racah upper-bound failures/cancellation gaps: "
        f"{len(racah_hazard['underestimates'])}/"
        f"{len(racah_hazard['cancellation_gaps'])}"
    )
    print(
        "Generic scalar-cost shortcut requires a stronger hazard: "
        f"{generic['hazard_is_stronger']}"
    )
    print(
        "HFT remainder terms/unique labels audited: "
        f"{remainder['tested']}/{remainder['unique_labels']}"
    )
    print(
        "HFT source-degree hazard failures: "
        f"{len(remainder['failures'])}"
    )
    print(
        "HFT hazard minimum margin/tight terms: "
        f"{remainder['minimum_margin']}/{remainder['tight']}"
    )
    print(
        "Observed HFT terms where hazard strengthens E(mu)-1: "
        f"{len(remainder['sharpened_records'])}"
    )
    print(
        "Higher-vector-free core terms/filter failures: "
        f"{higher_vector_core['tested']}/{len(higher_vector_core['failures'])}"
    )
    print(
        "Individually bad higher-vector convolution labels/cancellation failures: "
        f"{higher_vector_cancellations['bad_contribution_labels']}/"
        f"{len(higher_vector_cancellations['failures'])}"
    )
    print(
        "Bad-convolution translation signatures/max summands: "
        f"{higher_vector_cancellations['translation_signatures']}/"
        f"{higher_vector_cancellations['maximum_number_of_summands']}"
    )
    print(
        "Direct unstable-coupling failures: "
        f"{len(direct_energy['failures'])}"
    )
    print("Protected SO(10) baseline imported: NO")
    print(f"Runtime: {time.time() - started:.3f}s")

    all_checks = (
        filtration["all_nonmultiplicative"]
        and harmonic_cutoff["all_stable_beyond_cutoff"]
        and symmetric_hazard["all_controlled"]
        and spin_pieri["all_match"]
        and not vector_transition["preserves_mode_two_filtration"]
        and wall_derivation["nonredundant_match"]
        and wall_derivation["redundant_is_dominated"]
        and wall_formula["all_match"]
        and racah_hazard["is_upper_bound"]
        and not racah_hazard["is_exact"]
        and generic["hazard_is_stronger"]
        and remainder["all_satisfy"]
        and higher_vector_core["all_satisfy"]
        and higher_vector_cancellations["all_cancel"]
        and direct_energy["all_satisfy"]
    )
    return {
        "filtration_audit": filtration,
        "harmonic_cutoff_audit": harmonic_cutoff,
        "symmetric_hazard_audit": symmetric_hazard,
        "spin_pieri_formula_audit": spin_pieri,
        "vector_transition_audit": vector_transition,
        "wall_hazard_derivation_audit": wall_derivation,
        "wall_hazard_formula_audit": wall_formula,
        "racah_hazard_audit": racah_hazard,
        "generic_hazard_obstruction": generic,
        "factorization": factorization,
        "remainder_hazard_audit": remainder,
        "higher_vector_factorization": higher_vector_factorization,
        "higher_vector_core_audit": higher_vector_core,
        "higher_vector_cancellation_audit": higher_vector_cancellations,
        "direct_energy_audit": direct_energy,
        "all_checks": all_checks,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Audit coupling-aware HFT stable-range support"
    )
    parser.add_argument("--max-level", type=int, default=13)
    parser.add_argument("--maximum-label-sum", type=int, default=2)
    parser.add_argument("--formula-label-sum", type=int, default=5)
    args = parser.parse_args(argv)
    try:
        result = run_analysis(
            max_level=args.max_level,
            maximum_label_sum=args.maximum_label_sum,
            formula_label_sum=args.formula_label_sum,
        )
    except Exception as error:
        print(f"TK6B.5e FAILED: {error}", file=sys.stderr)
        return 1
    return 0 if result["all_checks"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
