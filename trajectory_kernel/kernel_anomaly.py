"""TK4c: the restriction-kernel anomaly of the SO(10) HFT quotient.

For a cumulative lift ``L_n`` define

    kappa_n = N_n^10 - Z_Q^10 * (L_n - L_(n-1)).

Every ``kappa_n`` restricts to zero.  Replacing ``L_n`` by ``L_n + H_n``,
with ``H_n`` in the restriction kernel, changes the anomaly by

    kappa_n -> kappa_n - Z_Q^10 * (H_n - H_(n-1)).

This module therefore keeps two objects separate:

1. an anomaly representative, obtained from the fixed all-chiral section;
2. its lift-independent class modulo ``Z_Q^10 * ker(Res)``.

The computation is baseline-free.  It uses only the independently constructed
HFT numerator and exact D5 -> B4 branching data.
"""

import argparse
import sys
import time
from functools import lru_cache
from itertools import permutations, product

from sage.all import LaurentPolynomialRing, QQ, matrix, prod, vector

import hft_so10_uplift
from trajectory_kernel import correction_ansatz as fibers_module
from trajectory_kernel import kernel_generating_series as series_module


REGULAR_LAURENT_RING = LaurentPolynomialRing(QQ, "u")
REGULAR_TORUS_VECTOR = (17, 11, 7, 3, 1)


def character_from_table(table):
    """Convert a sparse D5 irreducible table to a Weyl character."""
    return series_module.d5_character(table)


def character_table(character):
    """Return a sparse D5 table keyed by Dynkin labels."""
    return fibers_module.lattice.clean_sparse(
        {
            series_module.d5_weight_to_dynkin(weight): coefficient
            for weight, coefficient in character.monomial_coefficients().items()
            if coefficient
        }
    )


def outer_conjugate(character):
    """Apply the D5 outer automorphism interchanging the two spinor nodes."""
    return character_from_table(
        {
            (a1, a2, a3, a5, a4): coefficient
            for (a1, a2, a3, a4, a5), coefficient in character_table(character).items()
        }
    )


def outer_parity_diagnostics(character):
    """Report whether a virtual character is outer-even or outer-odd."""
    conjugate = outer_conjugate(character)
    return {
        "even": conjugate == character,
        "odd": conjugate == -character,
        "odd_defect_terms": len(character_table(character - conjugate)),
    }


def is_chiral_reference_parent(parent):
    """Test whether ``parent`` belongs to the fixed all-chiral section."""
    top = fibers_module.cross.top_b4_weight(parent)
    return parent == fibers_module.cross.select_parent(top, policy="chiral")


@lru_cache(maxsize=None)
def natural_kernel_relation(parent):
    """Return ``parent - s_ch(Res(parent))`` as an exact sparse relation."""
    parent = tuple(parent)
    if is_chiral_reference_parent(parent):
        return {}
    target = fibers_module.cross.branch_parent(parent)
    lifted = fibers_module.cross.invert_on_cross_section(target, policy="chiral")
    if not lifted["exact"] or not lifted["integral"]:
        raise ValueError(f"Failed to lift the restriction of {parent}")
    relation = {parent: 1}
    relation = fibers_module.lattice.add_sparse(
        relation,
        fibers_module.lattice.clean_sparse(lifted["coefficients"]),
        scale=-1,
    )
    if fibers_module.lattice.branch_virtual(relation):
        raise ValueError(f"Natural relation for {parent} is not in the kernel")
    return relation


def decompose_kernel_character(character):
    """Decompose a finite kernel character in the global chiral-section basis.

    The coefficient of a non-reference parent is its coordinate because its
    natural relation has that parent as a unique pivot.  Exact reconstruction
    checks that no reference-section remainder has been discarded.
    """
    if character.branch(fibers_module.cross.B4, rule="default") != fibers_module.cross.B4(0):
        raise ValueError("Character does not restrict to zero")
    table = character_table(character)
    coordinates = {
        parent: coefficient
        for parent, coefficient in table.items()
        if not is_chiral_reference_parent(parent)
    }
    reconstruction = fibers_module.cross.D5(0)
    for parent, coefficient in coordinates.items():
        reconstruction += coefficient * character_from_table(
            natural_kernel_relation(parent)
        )
    if reconstruction != character:
        residual = character_table(character - reconstruction)
        raise ValueError(
            "Global natural-kernel decomposition left a reference remainder: "
            f"{residual}"
        )
    return dict(sorted(coordinates.items()))


def kernel_coordinate_table(character):
    """Return global natural-kernel coordinates using triangular pivots.

    For a character already verified to restrict to zero, the coefficients of
    its non-reference irreducibles are its unique coordinates in the natural
    chiral-section basis.  ``decompose_kernel_character`` performs the more
    expensive explicit reconstruction and is retained for self-tests.
    """
    return {
        parent: coefficient
        for parent, coefficient in character_table(character).items()
        if not is_chiral_reference_parent(parent)
    }


def corrected_kernel_shift(character):
    """Apply the exact chiral-section boundary-corrected Regge shift."""
    relation = character_table(character)
    raw = fibers_module.lattice.shift_d5_virtual(relation)
    raw_boundary = fibers_module.lattice.branch_virtual(raw)
    correction = (
        fibers_module.lattice.chiral_section_lift(raw_boundary)
        if raw_boundary
        else {}
    )
    shifted = fibers_module.lattice.add_sparse(raw, correction, scale=-1)
    result = character_from_table(shifted)
    if result.branch(fibers_module.cross.B4, rule="default") != fibers_module.cross.B4(0):
        raise ValueError("Corrected shift did not preserve the restriction kernel")
    return result


def reference_data(max_level):
    """Construct all-chiral cumulative lifts and their exact anomalies."""
    domain = fibers_module.lattice.build_finite_domain(max_level)
    generators = fibers_module.ordered_generators(
        fibers_module.lattice.natural_kernel_generators(domain)
    )
    numerator = hft_so10_uplift.compute_hft_d5(max_level)
    zq = numerator[1]
    references = {
        0: fibers_module.cross.D5(0),
        **{
            level: character_from_table(
                fibers_module.reference_lift(
                    domain, domain["cumulative"][level]
                )
            )
            for level in range(1, max_level + 1)
        },
    }
    anomalies = {}
    decompositions = {}
    for level in range(1, max_level + 1):
        anomaly = numerator[level] - zq * (
            references[level] - references[level - 1]
        )
        if anomaly.branch(fibers_module.cross.B4, rule="default") != fibers_module.cross.B4(0):
            raise ValueError(f"Reference anomaly does not restrict to zero at level {level}")
        anomalies[level] = anomaly
        decompositions[level] = kernel_coordinate_table(anomaly)
    return {
        "domain": domain,
        "generators": generators,
        "numerator": numerator,
        "zq": zq,
        "references": references,
        "anomalies": anomalies,
        "decompositions": decompositions,
    }


def rational_span_membership(target, columns):
    """Test exact rational span membership of sparse D5 characters."""
    target_table = character_table(target)
    column_tables = tuple(character_table(column) for column in columns)
    labels = tuple(
        sorted(
            set(target_table).union(
                *(set(table) for table in column_tables)
            )
        )
    )
    if not columns:
        return {"in_span": not target_table, "coefficients": (), "rank": 0}
    coefficient_matrix = matrix(
        QQ,
        len(labels),
        len(columns),
        lambda row, column: column_tables[column].get(labels[row], 0),
    )
    target_vector = vector(QQ, [target_table.get(label, 0) for label in labels])
    rank = coefficient_matrix.rank()
    augmented_rank = coefficient_matrix.augment(target_vector).rank()
    if augmented_rank != rank:
        return {"in_span": False, "coefficients": None, "rank": rank}
    solution = coefficient_matrix.solve_right(target_vector)
    return {
        "in_span": True,
        "coefficients": tuple(solution),
        "integral": all(value.denominator() == 1 for value in solution),
        "rank": rank,
    }


def character_to_laurent(character, ring):
    """Embed a D5 character in the doubled-weight Laurent polynomial ring.

    D5 weights can be half-integral in orthogonal coordinates.  Doubling all
    five exponents gives an injective integral-exponent encoding.  Character
    multiplication is preserved exactly.
    """
    variables = ring.gens()
    return ring(
        sum(
            coefficient
            * prod(
                variables[index] ** int(2 * coordinate)
                for index, coordinate in enumerate(weight.to_vector())
            )
            for weight, coefficient in character.lift().monomial_coefficients().items()
        )
    )


def laurent_remainder(character, divisor, ring):
    """Return the exact remainder after division in the Laurent weight ring."""
    dividend_polynomial = character_to_laurent(character, ring)
    divisor_polynomial = character_to_laurent(divisor, ring)
    _quotient, remainder = dividend_polynomial.quo_rem(divisor_polynomial)
    return remainder


def laurent_span_membership(target, columns):
    """Test rational span membership for Laurent polynomials."""
    target_table = target.monomial_coefficients()
    column_tables = tuple(column.monomial_coefficients() for column in columns)
    labels = tuple(
        sorted(
            set(target_table).union(
                *(set(table) for table in column_tables)
            )
        )
    )
    if not columns:
        return {"in_span": not target_table, "rank": 0}
    coefficient_matrix = matrix(
        QQ,
        len(labels),
        len(columns),
        lambda row, column: column_tables[column].get(labels[row], 0),
    )
    target_vector = vector(QQ, [target_table.get(label, 0) for label in labels])
    rank = coefficient_matrix.rank()
    augmented_rank = coefficient_matrix.augment(target_vector).rank()
    if augmented_rank != rank:
        return {"in_span": False, "rank": rank}
    solution = coefficient_matrix.solve_right(target_vector)
    return {
        "in_span": True,
        "rank": rank,
        "coefficients": tuple(solution),
        "integral": all(value.denominator() == 1 for value in solution),
    }


def twice_orthogonal_highest_weight(parent):
    """Return twice the five orthogonal coordinates of a D5 highest weight."""
    a1, a2, a3, a4, a5 = parent
    return (
        2 * (a1 + a2 + a3) + a4 + a5,
        2 * (a2 + a3) + a4 + a5,
        2 * a3 + a4 + a5,
        a4 + a5,
        -a4 + a5,
    )


def permutation_parity(permutation):
    """Return the sign of a finite permutation."""
    inversions = sum(
        permutation[left] > permutation[right]
        for left in range(len(permutation))
        for right in range(left + 1, len(permutation))
    )
    return -1 if inversions % 2 else 1


@lru_cache(maxsize=None)
def weyl_alternant(twice_weight):
    """Specialize a D5 Weyl alternant at a fixed generic regular torus."""
    u = REGULAR_LAURENT_RING.gen()
    coefficients = {}
    even_signs = tuple(
        signs for signs in product((-1, 1), repeat=5) if prod(signs) == 1
    )
    for permutation in permutations(range(5)):
        parity = permutation_parity(permutation)
        permuted = tuple(twice_weight[index] for index in permutation)
        for signs in even_signs:
            exponent = sum(
                signs[index]
                * permuted[index]
                * REGULAR_TORUS_VECTOR[index]
                for index in range(5)
            )
            coefficients[exponent] = coefficients.get(exponent, 0) + parity
    return REGULAR_LAURENT_RING(
        sum(
            coefficient * u ** exponent
            for exponent, coefficient in coefficients.items()
            if coefficient
        )
    )


@lru_cache(maxsize=None)
def regular_irrep(parent):
    """Generic one-variable specialization of one D5 Weyl character."""
    twice_rho = (8, 6, 4, 2, 0)
    twice_lambda = twice_orthogonal_highest_weight(tuple(parent))
    numerator_weight = tuple(
        left + right for left, right in zip(twice_lambda, twice_rho)
    )
    numerator = weyl_alternant(numerator_weight)
    denominator = weyl_alternant(twice_rho)
    quotient, remainder = numerator.quo_rem(denominator)
    if remainder:
        raise ValueError(f"Regular Weyl quotient was not Laurent polynomial for {parent}")
    return quotient


def regular_specialization(character):
    """Evaluate a virtual D5 character at a fixed generic regular torus."""
    return REGULAR_LAURENT_RING(
        sum(
            coefficient * regular_irrep(parent)
            for parent, coefficient in character_table(character).items()
        )
    )


def regular_remainder(character, divisor):
    """Return the exact regular-specialization remainder modulo ``divisor``."""
    dividend = regular_specialization(character)
    divisor_polynomial = regular_specialization(divisor)
    _quotient, remainder = dividend.quo_rem(divisor_polynomial)
    return remainder


def anomaly_for_coordinate_path(data, solutions):
    """Evaluate anomalies for one path and verify the affine variation law."""
    generators = data["generators"]
    corrections = {0: fibers_module.cross.D5(0)}
    anomalies = {}
    for level, coordinates in enumerate(solutions, start=1):
        correction_table = fibers_module.coefficients_from_coordinates(
            {}, generators, coordinates
        )
        corrections[level] = character_from_table(correction_table)
        direct = data["numerator"][level] - data["zq"] * (
            data["references"][level]
            + corrections[level]
            - data["references"][level - 1]
            - corrections[level - 1]
        )
        predicted = data["anomalies"][level] - data["zq"] * (
            corrections[level] - corrections[level - 1]
        )
        if direct != predicted:
            raise ValueError(f"Anomaly variation law failed at level {level}")
        anomalies[level] = direct
    return anomalies


def seed_shift_diagnostics(data, max_level, certificate_level=6):
    """Test whether the fixed level-2 seed propagates under corrected shift."""
    certificate_level = min(max_level, int(certificate_level))
    if certificate_level < 2:
        raise ValueError("certificate_level must be at least 2")
    seed = data["anomalies"][2]
    orbit = {2: seed}
    for level in range(3, max_level + 1):
        orbit[level] = corrected_kernel_shift(orbit[level - 1])

    anomaly_residues = {
        level: regular_remainder(data["anomalies"][level], data["zq"])
        for level in range(2, certificate_level + 1)
    }
    orbit_residues = {
        level: regular_remainder(orbit[level], data["zq"])
        for level in range(2, certificate_level + 1)
    }
    records = {}
    for level in range(2, max_level + 1):
        residual = data["anomalies"][level] - orbit[level]
        if level <= certificate_level:
            residual_mod_zq = regular_remainder(residual, data["zq"])
            seed_span = laurent_span_membership(
                anomaly_residues[level],
                tuple(orbit_residues[index] for index in range(2, level + 1)),
            )
            nondivisibility = bool(anomaly_residues[level])
            inequivalence = bool(residual_mod_zq)
            outside_span = not seed_span["in_span"]
            integral_span = seed_span.get("integral", False)
            residue_rank = seed_span["rank"]
        else:
            nondivisibility = None
            inequivalence = None
            outside_span = None
            integral_span = None
            residue_rank = None
        records[level] = {
            "exact_seed_shift": residual == fibers_module.cross.D5(0),
            "regular_nondivisibility_certificate": nondivisibility,
            "regular_inequivalence_to_shift": inequivalence,
            "regular_outside_seed_orbit_span": outside_span,
            "integral_seed_orbit_span": integral_span,
            "residual_terms": len(character_table(residual)),
            "seed_orbit_residue_rank": residue_rank,
        }
    anomaly_residue_ranks = {}
    for horizon in range(2, certificate_level + 1):
        tables = tuple(
            anomaly_residues[level].monomial_coefficients()
            for level in range(2, horizon + 1)
        )
        labels = tuple(sorted(set().union(*(set(table) for table in tables))))
        residue_matrix = matrix(
            QQ,
            len(labels),
            len(tables),
            lambda row, column: tables[column].get(labels[row], 0),
        )
        anomaly_residue_ranks[horizon] = residue_matrix.rank()
    return {
        "seed": seed,
        "orbit": orbit,
        "records": records,
        "anomaly_residue_ranks": anomaly_residue_ranks,
        "certificate_level": certificate_level,
    }


def validate_regular_specialization(data, through_level=3):
    """Cross-check regular specialization and low-level full Laurent results."""
    full_ring = LaurentPolynomialRing(QQ, 5, "x")
    full_zq = character_to_laurent(data["zq"], full_ring)
    checks = {}
    for level in range(1, min(through_level, max(data["anomalies"])) + 1):
        anomaly = data["anomalies"][level]
        if anomaly == fibers_module.cross.D5(0):
            checks[level] = {
                "full_nondivisible": False,
                "regular_nondivisible": False,
            }
            continue
        full_anomaly = character_to_laurent(anomaly, full_ring)
        _quotient, full_remainder = full_anomaly.quo_rem(full_zq)
        full_divides = full_zq.divides(full_anomaly)
        if full_divides == bool(full_remainder):
            raise ValueError("Full Laurent divisibility checks disagree")
        regular_remainder_value = regular_remainder(anomaly, data["zq"])
        checks[level] = {
            "full_nondivisible": bool(full_remainder),
            "full_divides": full_divides,
            "regular_nondivisible": bool(regular_remainder_value),
        }
        if bool(regular_remainder_value) and not bool(full_remainder):
            raise ValueError("Regular specialization contradicted full divisibility")
    return checks


def summarize_tk4c(max_level=11, certificate_level=6, verbose=False):
    """Run the baseline-free structured-kernel-anomaly experiment."""
    if max_level < 2:
        raise ValueError("TK4c requires max_level >= 2")
    started = time.time()
    data = reference_data(max_level)
    rules = ("transport-first", "boundary-first", "total-deviation")
    paths = {
        rule: series_module.selection.milp_optimal_path(
            data["domain"], data["generators"], max_level, rule
        )
        for rule in rules
    }
    representative_anomalies = {
        rule: anomaly_for_coordinate_path(data, result["solutions"])
        for rule, result in paths.items()
    }
    seed_test = seed_shift_diagnostics(data, max_level, certificate_level)
    specialization_checks = validate_regular_specialization(data)

    print("=" * 118)
    print("TK4c — STRUCTURED RESTRICTION-KERNEL ANOMALY (BASELINE-FREE)")
    print("=" * 118)
    print(f"Levels: 1 through {max_level}")
    print(f"Finite positive-lift kernel generators: {len(data['generators'])}")
    print("Protected SO(10) baseline imported: NO")
    print("\nAll-chiral reference anomaly:")
    print(
        "  n   D5 terms   natural-kernel coordinates   dimension   "
        "restricts zero   outer-even"
    )
    for level in range(1, max_level + 1):
        anomaly = data["anomalies"][level]
        parity = outer_parity_diagnostics(anomaly)
        print(
            f"  {level:<3} {len(character_table(anomaly)):<10} "
            f"{len(data['decompositions'][level]):<28} "
            f"{int(anomaly.degree()):<11} "
            f"{str(anomaly.branch(fibers_module.cross.B4, rule='default') == fibers_module.cross.B4(0)):<16} "
            f"{parity['even']}"
        )

    print("\nLevel-2 seed under the corrected kernel shift:")
    print(
        "  Exact regular-torus quotient certificates computed through level "
        f"{seed_test['certificate_level']}."
    )
    for level, record in seed_test["records"].items():
        certificate = record["regular_nondivisibility_certificate"]
        inequivalence = record["regular_inequivalence_to_shift"]
        outside_span = record["regular_outside_seed_orbit_span"]
        print(
            f"  n={level}: exact={record['exact_seed_shift']}, "
            "nondivisibility certificate="
            f"{'not computed' if certificate is None else certificate}, "
            "inequivalent to transported seed certificate="
            f"{'not computed' if inequivalence is None else inequivalence}, "
            "outside seed-orbit span certificate="
            f"{'not computed' if outside_span is None else outside_span}, "
            f"residual terms={record['residual_terms']}"
        )
    print(
        "  Regular-torus residue rank (certifies class independence): "
        + ", ".join(
            f"n={level}: {rank}"
            for level, rank in seed_test["anomaly_residue_ranks"].items()
        )
    )

    print("\nRepresentative positive paths:")
    for rule in rules:
        nonzero = sum(
            anomaly != fibers_module.cross.D5(0)
            for anomaly in representative_anomalies[rule].values()
        )
        print(
            f"  {rule}: nonzero anomalies at {nonzero}/{max_level} levels; "
            "affine variation identity checked exactly"
        )
        if verbose:
            counts = {
                level: len(character_table(anomaly))
                for level, anomaly in representative_anomalies[rule].items()
            }
            print(f"    irreducible term counts: {counts}")

    level_two = data["anomalies"][2]
    a0 = next(
        generator
        for generator in data["generators"]
        if generator.top_weight == (0, 0, 0, 2)
    )
    chirality_difference = (
        fibers_module.cross.D5(0, 0, 0, 2, 0)
        - fibers_module.cross.D5(0, 0, 0, 0, 2)
    )
    seed_identity = (
        level_two
        == -2 * character_from_table(a0.as_dict()) + chirality_difference
    )
    print("\nCanonical low-level check:")
    print(f"  kappa_1 = 0: {data['anomalies'][1] == fibers_module.cross.D5(0)}")
    print(f"  kappa_2 = -2*A0 + J126: {seed_identity}")
    print(f"  kappa_2 is outer-chirality even: {outer_parity_diagnostics(level_two)['even']}")
    print(
        "  Full five-variable / regular-torus nondivisibility cross-check: "
        f"{specialization_checks}"
    )
    print("-" * 118)
    print(f"Elapsed: {time.time() - started:.3f}s")
    return {
        "data": data,
        "paths": paths,
        "representative_anomalies": representative_anomalies,
        "seed_test": seed_test,
        "seed_identity": seed_identity,
        "specialization_checks": specialization_checks,
    }


def run_self_test():
    """Check global kernel coordinates and corrected shifting on a toy relation."""
    parent = (0, 0, 0, 1, 1)
    relation = natural_kernel_relation(parent)
    character = character_from_table(relation)
    coordinates = decompose_kernel_character(character)
    shifted = corrected_kernel_shift(character)
    vector_character = fibers_module.cross.D5(1, 0, 0, 0, 0)
    spinor_character = fibers_module.cross.D5(0, 0, 0, 0, 1)
    direct_ring = LaurentPolynomialRing(QQ, 5, "x")

    def direct_regular_specialization(test_character):
        direct = character_to_laurent(test_character, direct_ring)
        return REGULAR_LAURENT_RING(
            sum(
                coefficient
                * REGULAR_LAURENT_RING.gen()
                ** sum(
                    exponent * torus_coordinate
                    for exponent, torus_coordinate in zip(
                        monomial, REGULAR_TORUS_VECTOR
                    )
                )
                for monomial, coefficient in direct.monomial_coefficients().items()
            )
        )
    checks = (
        coordinates == {parent: 1},
        shifted.branch(fibers_module.cross.B4, rule="default")
        == fibers_module.cross.B4(0),
        decompose_kernel_character(shifted) is not None,
        regular_specialization(vector_character)
        == direct_regular_specialization(vector_character),
        regular_specialization(spinor_character)
        == direct_regular_specialization(spinor_character),
        outer_conjugate(outer_conjugate(character)) == character,
    )
    passed = all(checks)
    print("TRAJECTORY-KERNEL TK4c SELF-TEST")
    print(f"Global natural-kernel decomposition and shift: {'PASS' if passed else 'FAIL'}")
    print("Protected SO(10) baseline imported: NO")
    return passed


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Structured restriction-kernel anomaly diagnostics"
    )
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--max-level", type=int, default=11)
    parser.add_argument("--certificate-level", type=int, default=6)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        sys.exit(0 if run_self_test() else 1)
    summarize_tk4c(args.max_level, args.certificate_level, args.verbose)
    sys.exit(0)
