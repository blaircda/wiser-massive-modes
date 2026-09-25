"""TK2: baseline-free D5 -> B4 branching shifts and finite kernel lattice.

The finite domain is the full positive-chirality parent closure of the
HFT-derived cumulative SO(9) spectra through a requested level. No protected
SO(10) completion is imported.

Two distinct shift questions are kept separate:

1. A D5 branching column shifted in its first Dynkin label equals the shifted
   B4 column plus an explicit lower-boundary anomaly.
2. A restriction-kernel relation may or may not remain in the kernel under
   the raw D5 shift. When it does not, the chosen chiral section gives an
   explicit boundary correction, whose provenance is reported.
"""

import argparse
import sys
import time
from collections import defaultdict
from dataclasses import dataclass

from sage.all import QQ, ZZ, matrix

import finite_cross_section as cross
import search_finite_cross_sections as section_search


@dataclass(frozen=True)
class KernelGenerator:
    """One natural integral kernel generator relative to the chiral section."""

    top_weight: tuple
    alternative_parent: tuple
    relation: tuple
    first_hft_level: int | None
    reduced_depth: int | None

    def as_dict(self):
        return dict(self.relation)


def _integer(value, description):
    if value not in ZZ:
        raise ValueError(f"Non-integral {description}: {value}")
    return int(value)


def clean_sparse(table):
    """Return a deterministically ordered sparse integer dictionary."""
    cleaned = {}
    for label, coefficient in table.items():
        value = _integer(coefficient, "sparse coefficient")
        if value:
            cleaned[tuple(label)] = value
    return dict(sorted(cleaned.items()))


def add_sparse(left, right, scale=1):
    """Return ``left + scale*right`` for sparse character dictionaries."""
    result = dict(left)
    for label, coefficient in right.items():
        value = result.get(label, 0) + scale * coefficient
        if value:
            result[label] = value
        else:
            result.pop(label, None)
    return clean_sparse(result)


def shift_b4_label(label, steps=1):
    """Apply the leading-label shift to a B4 Dynkin label."""
    ell, m, r, s = label
    shifted = ell + int(steps)
    if shifted < 0:
        raise ValueError(f"Negative shifted B4 leading label: {label}")
    return (shifted, m, r, s)


def shift_d5_label(label, steps=1):
    """Apply the corresponding first-label shift to a D5 Dynkin label."""
    a1, a2, a3, a4, a5 = label
    shifted = a1 + int(steps)
    if shifted < 0:
        raise ValueError(f"Negative shifted D5 first label: {label}")
    return (shifted, a2, a3, a4, a5)


def shift_b4_table(table, steps=1):
    return clean_sparse(
        {shift_b4_label(label, steps): value for label, value in table.items()}
    )


def shift_d5_virtual(table, steps=1):
    return clean_sparse(
        {shift_d5_label(label, steps): value for label, value in table.items()}
    )


def branch_table(parent):
    """Return the sparse integral B4 restriction of one D5 irrep."""
    return clean_sparse(
        cross.character_coefficients(cross.branch_parent(tuple(parent)))
    )


def branch_virtual(table):
    """Restrict a sparse virtual D5 character."""
    result = {}
    for parent, coefficient in table.items():
        result = add_sparse(result, branch_table(parent), coefficient)
    return result


def branching_shift_anomaly(parent):
    """Compute ``Res(S parent) - S(Res parent)`` exactly."""
    shifted_branch = branch_table(shift_d5_label(parent))
    transported_branch = shift_b4_table(branch_table(parent))
    return add_sparse(shifted_branch, transported_branch, scale=-1)


def twice_d5_lambda2(parent):
    """Return twice the second orthogonal coordinate of a D5 highest weight."""
    _a1, a2, a3, a4, a5 = parent
    return 2 * (a2 + a3) + a4 + a5


def is_lower_interlacing_boundary(parent, b4_label):
    """Test whether a B4 weight lies on ``mu_1=lambda_2`` for ``parent``."""
    twice_mu1 = cross.b4_dynkin_to_ambient(b4_label)[0]
    return twice_mu1 == twice_d5_lambda2(parent)


def sparse_b4_character(table):
    """Convert a sparse B4 irreducible table to a Weyl character."""
    character = cross.B4(0)
    for label, coefficient in table.items():
        character += coefficient * cross.B4(*label)
    return character


def chiral_section_lift(table):
    """Lift a possibly virtual B4 table on the fixed all-chiral section."""
    result = cross.invert_on_cross_section(
        sparse_b4_character(table), policy="chiral"
    )
    if not result["exact"] or not result["integral"]:
        raise ValueError("Chiral section failed to lift a branching anomaly")
    return clean_sparse(result["coefficients"])


def first_occurrence_levels(cumulative):
    """Return the first cumulative HFT level containing each B4 irrep."""
    first = {}
    for level in sorted(cumulative):
        for label, coefficient in cross.character_coefficients(
            cumulative[level]
        ).items():
            if coefficient and label not in first:
                first[label] = level
    return first


def build_finite_domain(max_level=10):
    """Construct the exact finite branching matrix domain for TK2."""
    single_levels, cumulative = cross.derive_cumulative_so9(max_level)
    weights = section_search.full_family_closure(cumulative)
    branch_tables = section_search.prepare_branch_tables(weights)
    parents = tuple(sorted(branch_tables))
    ambiguous = tuple(
        (weight, cross.positive_chirality_parent_family(weight))
        for weight in weights
        if len(cross.positive_chirality_parent_family(weight)) > 1
    )
    return {
        "single_levels": single_levels,
        "cumulative": cumulative,
        "weights": weights,
        "branch_tables": branch_tables,
        "parents": parents,
        "ambiguous": ambiguous,
        "first_occurrence": first_occurrence_levels(cumulative),
    }


def natural_kernel_generators(domain):
    """Build the integral kernel basis induced by the all-chiral section.

    Each non-reference parent is compared with the exact chiral-section lift
    of its own restriction. The resulting virtual D5 character restricts to
    zero and has coefficient one on a unique non-reference column.
    """
    weights = domain["weights"]
    branch_tables = domain["branch_tables"]
    selection = {
        weight: cross.select_parent(weight, policy="chiral")
        for weight in weights
    }
    first_occurrence = domain["first_occurrence"]
    generators = []

    for top_weight, family in domain["ambiguous"]:
        for alternative in family[1:]:
            exact, integral, _positive, coefficients, residual = (
                section_search.invert_sparse(
                    branch_tables[alternative],
                    weights,
                    selection,
                    branch_tables,
                )
            )
            if not exact or not integral or residual:
                raise ValueError(
                    f"Failed to invert restriction of alternative {alternative}"
                )

            relation = {alternative: 1}
            relation = add_sparse(relation, coefficients, scale=-1)
            if branch_virtual(relation):
                raise ValueError(
                    f"Constructed relation does not restrict to zero: {alternative}"
                )

            level = first_occurrence.get(top_weight)
            ell, m, _r, _s = top_weight
            depth = None if level is None else level - ell - 3 * m
            generators.append(
                KernelGenerator(
                    top_weight=top_weight,
                    alternative_parent=alternative,
                    relation=tuple(relation.items()),
                    first_hft_level=level,
                    reduced_depth=depth,
                )
            )
    return tuple(generators)


def matrix_diagnostics(domain, generators):
    """Check rank, nullity, and integral-basis structure of the finite map."""
    weights = domain["weights"]
    parents = domain["parents"]
    tables = domain["branch_tables"]
    parent_index = {parent: index for index, parent in enumerate(parents)}

    restriction = matrix(
        QQ,
        len(weights),
        len(parents),
        lambda row, column: tables[parents[column]].get(weights[row], 0),
    )
    relation_vectors = []
    for generator in generators:
        vector = [0] * len(parents)
        for parent, coefficient in generator.relation:
            vector[parent_index[parent]] = coefficient
        relation_vectors.append(vector)
    relation_matrix = matrix(QQ, relation_vectors)
    reference_parents = tuple(
        cross.select_parent(weight, policy="chiral") for weight in weights
    )
    reference_matrix = matrix(
        QQ,
        len(weights),
        len(reference_parents),
        lambda row, column: tables[reference_parents[column]].get(
            weights[row], 0
        ),
    )
    reference_determinant = reference_matrix.det()

    unique_alternatives = len(
        {generator.alternative_parent for generator in generators}
    ) == len(generators)
    unit_alternatives = all(
        generator.as_dict().get(generator.alternative_parent) == 1
        for generator in generators
    )
    only_own_alternative = all(
        all(
            other.alternative_parent == generator.alternative_parent
            or generator.as_dict().get(other.alternative_parent, 0) == 0
            for other in generators
        )
        for generator in generators
    )

    return {
        "matrix": restriction,
        "rank": restriction.rank(),
        "nullity": len(parents) - restriction.rank(),
        "relation_rank": relation_matrix.rank(),
        "reference_determinant": reference_determinant,
        "reference_unimodular": abs(reference_determinant) == 1,
        "all_relations_null": all(
            not branch_virtual(generator.as_dict()) for generator in generators
        ),
        "integral_triangular_basis": (
            unique_alternatives and unit_alternatives and only_own_alternative
        ),
    }


def branching_shift_diagnostics(domain):
    """Test the exact one-step branching shift on every finite-domain parent."""
    records = []
    anomalies_by_tail = defaultdict(list)
    for parent in domain["parents"]:
        anomaly = branching_shift_anomaly(parent)
        records.append(
            {
                "parent": parent,
                "anomaly": anomaly,
                "nonnegative": all(value >= 0 for value in anomaly.values()),
                "multiplicity_free": all(value == 1 for value in anomaly.values()),
                "on_lower_boundary": all(
                    is_lower_interlacing_boundary(parent, label)
                    for label in anomaly
                ),
            }
        )
        anomalies_by_tail[parent[1:]].append((parent[0], anomaly))

    repeated_tail_groups = {
        tail: entries
        for tail, entries in anomalies_by_tail.items()
        if len(entries) > 1
    }
    tail_independent = all(
        all(anomaly == entries[0][1] for _a1, anomaly in entries[1:])
        for entries in repeated_tail_groups.values()
    )
    return {
        "records": tuple(records),
        "all_nonnegative": all(record["nonnegative"] for record in records),
        "all_multiplicity_free": all(
            record["multiplicity_free"] for record in records
        ),
        "all_on_lower_boundary": all(
            record["on_lower_boundary"] for record in records
        ),
        "tail_groups": len(anomalies_by_tail),
        "repeated_tail_groups": len(repeated_tail_groups),
        "tail_independent": tail_independent,
    }


def kernel_shift_diagnostics(generators):
    """Test raw and chiral-section-corrected shifts of kernel generators."""
    records = []
    for generator in generators:
        relation = generator.as_dict()
        raw_shift = shift_d5_virtual(relation)
        raw_anomaly = branch_virtual(raw_shift)
        correction = chiral_section_lift(raw_anomaly) if raw_anomaly else {}
        corrected_shift = add_sparse(raw_shift, correction, scale=-1)

        shifted_top = shift_b4_label(generator.top_weight)
        shifted_alternative = shift_d5_label(generator.alternative_parent)
        target_result = cross.invert_on_cross_section(
            cross.branch_parent(shifted_alternative), policy="chiral"
        )
        if not target_result["exact"] or not target_result["integral"]:
            raise ValueError(
                "Failed to construct the shifted natural kernel generator"
            )
        target_relation = add_sparse(
            {shifted_alternative: 1},
            clean_sparse(target_result["coefficients"]),
            scale=-1,
        )

        records.append(
            {
                "top_weight": generator.top_weight,
                "shifted_top": shifted_top,
                "raw_anomaly": raw_anomaly,
                "raw_is_kernel": not raw_anomaly,
                "correction": correction,
                "corrected_shift": corrected_shift,
                "corrected_is_kernel": not branch_virtual(corrected_shift),
                "target_relation": target_relation,
                "matches_next_natural_generator": corrected_shift
                == target_relation,
            }
        )
    return tuple(records)


def summarize_tk2(max_level=10, verbose=False):
    """Run all baseline-free TK2 diagnostics."""
    started = time.time()
    domain = build_finite_domain(max_level)
    generators = natural_kernel_generators(domain)
    matrix_info = matrix_diagnostics(domain, generators)
    branch_shift = branching_shift_diagnostics(domain)
    kernel_shifts = kernel_shift_diagnostics(generators)

    raw_kernel_count = sum(record["raw_is_kernel"] for record in kernel_shifts)
    corrected_kernel_count = sum(
        record["corrected_is_kernel"] for record in kernel_shifts
    )
    corrected_match_count = sum(
        record["matches_next_natural_generator"] for record in kernel_shifts
    )

    print("=" * 108)
    print("TK2 — BASELINE-FREE D5 -> B4 BRANCHING SHIFTS AND FINITE KERNEL LATTICE")
    print("=" * 108)
    print(f"HFT levels defining finite closure: 1 through {max_level}")
    print(f"B4 row weights: {len(domain['weights'])}")
    print(f"D5 positive-chirality parent columns: {len(domain['parents'])}")
    print(f"Restriction-matrix rank: {matrix_info['rank']}")
    print(f"Restriction-kernel rank: {matrix_info['nullity']}")
    print(f"Natural integral generators: {len(generators)}")
    print(f"Natural-generator rank: {matrix_info['relation_rank']}")
    print(
        "Chiral reference-section determinant: "
        f"{matrix_info['reference_determinant']}"
    )
    print(f"All natural generators restrict to zero: {matrix_info['all_relations_null']}")
    print(
        "Natural generators form an integral triangular basis: "
        f"{matrix_info['integral_triangular_basis']}"
    )
    print("\nBranching-column shift:")
    print(f"  Parents tested: {len(branch_shift['records'])}")
    print(f"  Boundary anomalies all nonnegative: {branch_shift['all_nonnegative']}")
    print(
        "  Boundary anomalies multiplicity-free: "
        f"{branch_shift['all_multiplicity_free']}"
    )
    print(
        "  Every anomaly lies on mu1=lambda2: "
        f"{branch_shift['all_on_lower_boundary']}"
    )
    print(f"  Distinct fixed-tail groups: {branch_shift['tail_groups']}")
    print(
        "  Repeated-tail groups tested for a1 independence: "
        f"{branch_shift['repeated_tail_groups']}"
    )
    print(f"  All repeated-tail anomalies agree: {branch_shift['tail_independent']}")
    print("\nKernel-generator shift:")
    print(f"  Raw shifted generators still in kernel: {raw_kernel_count} / {len(generators)}")
    print(
        "  Boundary-corrected shifts in kernel: "
        f"{corrected_kernel_count} / {len(generators)}"
    )
    print(
        "  Corrected shifts equal next natural generator: "
        f"{corrected_match_count} / {len(generators)}"
    )

    print("\nKernel-generator trajectory coordinates:")
    for index, generator in enumerate(generators, start=1):
        print(
            f"  K{index}: top={generator.top_weight}, "
            f"first HFT n={generator.first_hft_level}, "
            f"delta={generator.reduced_depth}, "
            f"support={len(generator.relation)}"
        )

    if verbose:
        print("\nNatural kernel relations:")
        for index, generator in enumerate(generators, start=1):
            print(f"  K{index} = {generator.as_dict()}")

        print("\nKernel shift anomalies and corrections:")
        for index, record in enumerate(kernel_shifts, start=1):
            print(f"  K{index}: {record['top_weight']} -> {record['shifted_top']}")
            print(f"    raw anomaly: {record['raw_anomaly']}")
            print(f"    chiral-section correction: {record['correction']}")
            print(
                "    corrected equals next natural generator: "
                f"{record['matches_next_natural_generator']}"
            )

    all_checks = (
        matrix_info["rank"] == len(domain["weights"])
        and matrix_info["nullity"] == len(generators)
        and matrix_info["relation_rank"] == len(generators)
        and matrix_info["all_relations_null"]
        and matrix_info["reference_unimodular"]
        and matrix_info["integral_triangular_basis"]
        and branch_shift["all_nonnegative"]
        and branch_shift["all_multiplicity_free"]
        and branch_shift["all_on_lower_boundary"]
        and branch_shift["tail_independent"]
        and corrected_kernel_count == len(generators)
    )
    print("-" * 108)
    print("Protected SO(10) baseline imported: NO")
    print(f"TK2 structural checks: {'PASS' if all_checks else 'FAIL'}")
    print(f"Elapsed: {time.time() - started:.3f}s")
    return {
        "domain": domain,
        "generators": generators,
        "matrix": matrix_info,
        "branch_shift": branch_shift,
        "kernel_shifts": kernel_shifts,
        "all_checks": all_checks,
    }


def run_self_test():
    """Check sparse arithmetic and shift conventions without HFT derivation."""
    b4 = (2, 1, 0, 3)
    d5 = (2, 1, 0, 1, 2)
    checks = (
        shift_b4_label(b4) == (3, 1, 0, 3),
        shift_d5_label(d5) == (3, 1, 0, 1, 2),
        add_sparse({b4: 2}, {b4: 1}, scale=-2) == {},
        shift_b4_table({b4: 4}) == {(3, 1, 0, 3): 4},
        shift_d5_virtual({d5: -1}) == {(3, 1, 0, 1, 2): -1},
    )
    passed = all(checks)
    print("TRAJECTORY-KERNEL TK2 SELF-TEST")
    print(f"Sparse arithmetic and shift conventions: {'PASS' if passed else 'FAIL'}")
    print("Protected SO(10) baseline imported: NO")
    return passed


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Baseline-free D5 -> B4 branching and kernel-shift diagnostics"
    )
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--max-level", type=int, default=10)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        sys.exit(0 if run_self_test() else 1)
    result = summarize_tk2(args.max_level, args.verbose)
    sys.exit(0 if result["all_checks"] else 1)
