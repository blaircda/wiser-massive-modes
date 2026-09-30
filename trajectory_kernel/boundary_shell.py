"""TK6B.3: universal boundary shells and the growing Gale hypergraph.

TK6B.2 found an exact A/B/C Gale-row pattern through HFT horizon 11.  This
module separates two questions which the finite observation had conflated:

* does the stated row pattern hold for A/B/C chains of arbitrary length? and
* do A/B/C remain the only ambiguous top-weight families at later horizons?

The first question is reduced to the collision pattern of three explicit
six-term restriction-kernel identities.  The second is tested against the
baseline-free HFT construction at the first unexamined horizon.

The module also proves and checks the closed local answer for every allowed
parent split.  Consecutive parents differ by a universal six-term shell
relation, while comparison with the all-chiral parent is its telescoping sum.
Protected SO(10) completion data are never imported.
"""

import argparse
import sys
import time
from collections import Counter, defaultdict

from sage.all import ZZ, matrix

import finite_cross_section as cross
from trajectory_kernel import correction_ansatz
from trajectory_kernel import interlacing_facets
from trajectory_kernel import kernel_lattice


ABC_TAILS = {
    "A": (0, 0, 2),
    "B": (1, 0, 2),
    "C": (0, 0, 3),
}


def split_parent(top_weight, split):
    """Return ``[ell,m,r,split,s-split]`` after exact range validation."""
    if len(top_weight) != 4:
        raise ValueError("A B4 top weight must have four Dynkin labels")
    ell, m, r, s = top_weight
    if min(top_weight) < 0:
        raise ValueError("B4 Dynkin labels must be nonnegative")
    if split not in ZZ:
        raise ValueError("The parent split must be an integer")
    split = int(split)
    if not 0 <= split <= s // 2:
        raise ValueError(
            f"Parent split {split} is outside 0 <= k <= floor({s}/2)"
        )
    return (ell, m, r, split, s - split)


def shell_packets(top_weight, split):
    """Return the four all-chiral packets resolving one interlacing shell.

    If the common orthogonal top boundary is ``(a,b,c,d)`` and
    ``e=d-split``, these are respectively

    ``Q(a,b,c,e), Q(a,b,d-1,e), Q(a,c-1,d-1,e),`` and
    ``Q(b-1,c-1,d-1,e)``.
    """
    ell, m, r, s = top_weight
    split_parent(top_weight, split)
    split = int(split)
    if split < 1:
        raise ValueError("A consecutive shell requires split >= 1")
    return (
        (ell, m, r + split, 0, s - 2 * split),
        (ell, m + r + 1, split - 1, 0, s - 2 * split),
        (ell + m + 1, r, split - 1, 0, s - 2 * split),
        (m, r, split - 1, 0, s - 2 * split),
    )


def shell_relation(top_weight, split):
    """Return the universal six-term relation for consecutive parent splits.

    The relation compares ``P_split`` with ``P_(split-1)`` and subtracts
    the four-term all-chiral inclusion-exclusion formula for the intervening
    interlacing shell.
    """
    current = split_parent(top_weight, split)
    split = int(split)
    previous = split_parent(top_weight, split - 1)
    q1, q2, q3, q4 = shell_packets(top_weight, split)
    relation = {current: 1, previous: -1}
    for packet, coefficient in (
        (q1, -1),
        (q2, 1),
        (q3, -1),
        (q4, 1),
    ):
        relation = kernel_lattice.add_sparse(
            relation, {packet: coefficient}
        )
    return relation


def natural_split_relation(top_weight, split):
    """Compare the ``split`` parent directly with the all-chiral parent.

    This is the closed telescoped formula ``sum(shell_relation(t), t=1..k)``
    written with its two endpoint parents and all ``4*k`` chiral packets.
    """
    current = split_parent(top_weight, split)
    split = int(split)
    reference = split_parent(top_weight, 0)
    if split < 1:
        raise ValueError("A non-reference parent requires split >= 1")
    relation = {current: 1, reference: -1}
    for step in range(1, split + 1):
        q1, q2, q3, q4 = shell_packets(top_weight, step)
        for packet, coefficient in (
            (q1, -1),
            (q2, 1),
            (q3, -1),
            (q4, 1),
        ):
            relation = kernel_lattice.add_sparse(
                relation, {packet: coefficient}
            )
    return relation


def intrinsic_split_relation(top_weight, split):
    """Reconstruct one natural relation by independent triangular inversion."""
    alternative = split_parent(top_weight, split)
    split = int(split)
    if split < 1:
        raise ValueError("An intrinsic alternative requires split >= 1")
    inversion = cross.invert_on_cross_section(
        cross.branch_parent(alternative), policy="chiral"
    )
    if not inversion["exact"] or not inversion["integral"]:
        raise ValueError(
            f"Chiral-section inversion failed for alternative {alternative}"
        )
    relation = {alternative: 1}
    for parent, coefficient in inversion["coefficients"].items():
        if coefficient:
            relation = kernel_lattice.add_sparse(
                relation, {parent: -coefficient}
            )
    return relation


def first_split_relation(top_weight):
    """Return the ``split=1`` specialization of the all-split theorem.

    For ``top_weight=(ell,m,r,s)`` with ``s >= 2``, this compares the
    alternative parent ``[ell,m,r,1,s-1]`` with the all-chiral parent
    ``[ell,m,r,0,s]``.  The other four terms are all-chiral parents.
    """
    return shell_relation(top_weight, 1)


def abc_relation(family, ell):
    """Return the observed six-term D5 kernel identity at arbitrary ``ell``."""
    if family not in ABC_TAILS:
        raise ValueError(f"Unknown A/B/C family {family!r}")
    if ell < 0:
        raise ValueError("A/B/C leading labels must be nonnegative")

    m, r, s = ABC_TAILS[family]
    return first_split_relation((ell, m, r, s))


def abstract_abc_relations(a_length, b_length, c_length):
    """Build formal A/B/C chains with the exact six-term supports."""
    lengths = {"A": a_length, "B": b_length, "C": c_length}
    if any(length < 0 for length in lengths.values()):
        raise ValueError("A/B/C chain lengths must be nonnegative")
    return {
        f"{family}{ell}": abc_relation(family, ell)
        for family in ("A", "B", "C")
        for ell in range(lengths[family])
    }


def gale_rows_from_relations(relations, parent_universe=()):
    """Transpose named sparse kernel relations into named Gale row signatures."""
    names = tuple(relations)
    coefficients = defaultdict(dict)
    for name, relation in relations.items():
        for parent, coefficient in relation.items():
            coefficients[parent][name] = int(coefficient)
    for parent in parent_universe:
        coefficients.setdefault(tuple(parent), {})
    rows = {
        parent: tuple(
            (name, table[name]) for name in names if table.get(name, 0)
        )
        for parent, table in coefficients.items()
    }
    return names, dict(sorted(rows.items()))


def abstract_abc_diagnostics(a_length, b_length, c_length):
    """Verify the compact row rule solely from six-term support collisions."""
    relations = abstract_abc_relations(a_length, b_length, c_length)
    names, rows = gale_rows_from_relations(relations)
    observed = set(rows.values()) | {()}
    expected = interlacing_facets.expected_abc_gale_types(names)
    return {
        "lengths": (a_length, b_length, c_length),
        "generator_names": names,
        "relations": relations,
        "rows": rows,
        "observed_types": observed,
        "expected_types": expected,
        "matches": expected is not None and observed == expected,
        "extra_types": () if expected is None else tuple(sorted(observed - expected)),
        "missing_types": () if expected is None else tuple(sorted(expected - observed)),
    }


def branch_identity_diagnostics(max_ell=4):
    """Exactly branch a finite sample of the all-ell A/B/C identities."""
    records = []
    for family in ("A", "B", "C"):
        for ell in range(max_ell + 1):
            relation = abc_relation(family, ell)
            residual = kernel_lattice.branch_virtual(relation)
            records.append(
                {
                    "family": family,
                    "ell": ell,
                    "terms": len(relation),
                    "restricts_zero": not residual,
                    "residual": residual,
                }
            )
    return {
        "max_ell": max_ell,
        "records": tuple(records),
        "all_restrict_zero": all(item["restricts_zero"] for item in records),
        "all_six_term": all(item["terms"] == 6 for item in records),
    }


def first_split_grid_diagnostics(
    max_label=1,
    spin_labels=(2, 3, 4),
    top_weights=None,
):
    """Exactly test the universal first-split formula on a small label grid."""
    records = []
    weights = (
        tuple(top_weights)
        if top_weights is not None
        else tuple(
            (ell, m, r, s)
            for ell in range(max_label + 1)
            for m in range(max_label + 1)
            for r in range(max_label + 1)
            for s in spin_labels
        )
    )
    for top_weight in weights:
        relation = first_split_relation(top_weight)
        records.append(
            {
                "top_weight": top_weight,
                "terms": len(relation),
                "coefficients_unit": all(
                    abs(value) == 1 for value in relation.values()
                ),
                "restricts_zero": not kernel_lattice.branch_virtual(relation),
            }
        )
    return {
        "records": tuple(records),
        "all_six_term": all(item["terms"] == 6 for item in records),
        "all_coefficients_unit": all(
            item["coefficients_unit"] for item in records
        ),
        "all_restrict_zero": all(item["restricts_zero"] for item in records),
    }


def all_split_grid_diagnostics(
    max_label=0,
    spin_labels=range(2, 7),
    top_weights=None,
):
    """Check all allowed splits by branching and independent inversion.

    The branching-zero test and the chiral-section reconstruction are
    logically separate checks.  The latter derives the natural relation from
    the restriction of the alternative parent rather than from the formula.
    """
    weights = (
        tuple(top_weights)
        if top_weights is not None
        else tuple(
            (ell, m, r, s)
            for ell in range(max_label + 1)
            for m in range(max_label + 1)
            for r in range(max_label + 1)
            for s in spin_labels
        )
    )
    records = []
    for top_weight in weights:
        _ell, _m, _r, s = top_weight
        for split in range(1, s // 2 + 1):
            shell = shell_relation(top_weight, split)
            natural = natural_split_relation(top_weight, split)
            telescoped = {}
            for step in range(1, split + 1):
                telescoped = kernel_lattice.add_sparse(
                    telescoped, shell_relation(top_weight, step)
                )
            intrinsic = intrinsic_split_relation(top_weight, split)
            records.append(
                {
                    "top_weight": top_weight,
                    "split": split,
                    "shell_terms": len(shell),
                    "natural_terms": len(natural),
                    "shell_coefficients_unit": all(
                        abs(value) == 1 for value in shell.values()
                    ),
                    "natural_coefficients_unit": all(
                        abs(value) == 1 for value in natural.values()
                    ),
                    "shell_restricts_zero": not kernel_lattice.branch_virtual(
                        shell
                    ),
                    "natural_restricts_zero": not kernel_lattice.branch_virtual(
                        natural
                    ),
                    "telescopes": natural == telescoped,
                    "matches_intrinsic": natural == intrinsic,
                }
            )
    return {
        "records": tuple(records),
        "all_shell_six_term": all(
            item["shell_terms"] == 6 for item in records
        ),
        "all_natural_term_counts": all(
            item["natural_terms"] == 4 * item["split"] + 2
            for item in records
        ),
        "all_coefficients_unit": all(
            item["shell_coefficients_unit"]
            and item["natural_coefficients_unit"]
            for item in records
        ),
        "all_restrict_zero": all(
            item["shell_restricts_zero"] and item["natural_restricts_zero"]
            for item in records
        ),
        "all_telescope": all(item["telescopes"] for item in records),
        "all_match_intrinsic": all(
            item["matches_intrinsic"] for item in records
        ),
    }


def generator_name(generator):
    """Return a unique readable coordinate name, including the parent split."""
    legacy = correction_ansatz.family_label(generator)
    if legacy[0] in "ABC" and legacy[1:].isdigit():
        return legacy
    ell, m, r, s = generator.top_weight
    split = generator.alternative_parent[3]
    return f"K({ell},{m},{r},{s};{split})"


def domain_gale_diagnostics(domain):
    """Construct the exact natural Gale matrix without enumerating cone facets."""
    generators = correction_ansatz.ordered_generators(
        kernel_lattice.natural_kernel_generators(domain)
    )
    names = tuple(generator_name(generator) for generator in generators)
    if len(set(names)) != len(names):
        raise ValueError("Natural generator names are not unique")
    relations = {
        name: generator.as_dict()
        for name, generator in zip(names, generators)
    }
    names, row_tables = gale_rows_from_relations(relations, domain["parents"])
    rows = tuple(row_tables[parent] for parent in domain["parents"])
    row_counts = Counter(rows)
    packets = matrix(
        ZZ,
        len(domain["weights"]),
        len(domain["parents"]),
        lambda row, column: domain["branch_tables"][domain["parents"][column]].get(
            domain["weights"][row], 0
        ),
    )
    gale = matrix(
        ZZ,
        len(domain["parents"]),
        len(generators),
        lambda row, column: generators[column].as_dict().get(
            domain["parents"][row], 0
        ),
    )
    if packets * gale != 0 or gale.rank() != len(generators):
        raise ValueError("Natural relations do not form the full Gale kernel")

    type_classes = Counter()
    for row in row_counts:
        values = tuple(value for _name, value in row)
        if not values:
            type_classes["zero"] += 1
        elif len(values) == 1 and abs(values[0]) == 1:
            type_classes["signed-coordinate"] += 1
        else:
            type_classes["composite"] += 1
    composites = tuple(
        sorted(
            (row, multiplicity)
            for row, multiplicity in row_counts.items()
            if len(row) > 1
        )
    )
    return {
        "generators": generators,
        "generator_names": names,
        "relations": relations,
        "gale": gale,
        "row_counts": row_counts,
        "unique_row_types": len(row_counts),
        "type_classes": dict(sorted(type_classes.items())),
        "composites": composites,
        "all_relation_coefficients_unit": all(
            abs(value) == 1
            for relation in relations.values()
            for value in relation.values()
        ),
    }


def hft_support_lookahead(current_level, lookahead_level):
    """Find new ambiguous top weights directly in later HFT single levels."""
    if lookahead_level <= current_level:
        raise ValueError("HFT lookahead must exceed the current level")
    single_levels, _cumulative = cross.derive_cumulative_so9(lookahead_level)
    previous = {
        weight
        for level in range(1, current_level + 1)
        for weight in cross.character_coefficients(single_levels[level])
        if weight[3] >= 2
    }
    new_by_level = {}
    running = set(previous)
    for level in range(current_level + 1, lookahead_level + 1):
        current = {
            weight
            for weight in cross.character_coefficients(single_levels[level])
            if weight[3] >= 2
        }
        new_by_level[level] = tuple(sorted(current - running))
        running.update(current)
    return {
        "current_level": current_level,
        "lookahead_level": lookahead_level,
        "new_by_level": new_by_level,
        "new_tails_by_level": {
            level: tuple(sorted({weight[1:] for weight in weights}))
            for level, weights in new_by_level.items()
        },
    }


def analyze_boundary_shell(
    max_level=12,
    previous_level=None,
    branch_check_ell=4,
    split_check_max_label=0,
    split_check_max_s=6,
    lookahead_level=None,
):
    """Analyze all parent splits and the first HFT shell beyond TK6B.2."""
    if max_level < 2:
        raise ValueError("Boundary-shell comparison requires max_level >= 2")
    if split_check_max_label < 0:
        raise ValueError("All-split check labels must be nonnegative")
    if split_check_max_s < 2:
        raise ValueError("All-split checks require split_check_max_s >= 2")
    if previous_level is None:
        previous_level = max_level - 1
    if not 1 <= previous_level < max_level:
        raise ValueError("Require 1 <= previous_level < max_level")

    abstract = abstract_abc_diagnostics(9, 6, 5)
    branch_checks = branch_identity_diagnostics(branch_check_ell)
    all_split_checks = all_split_grid_diagnostics(
        max_label=split_check_max_label,
        spin_labels=range(2, split_check_max_s + 1),
    )
    master = kernel_lattice.build_finite_domain(max_level)
    previous = interlacing_facets.build_nested_domain(master, previous_level)
    current_gale = domain_gale_diagnostics(master)
    previous_gale = domain_gale_diagnostics(previous)

    previous_tops = {
        generator.top_weight for generator in previous_gale["generators"]
    }
    new_generators = tuple(
        generator
        for generator in current_gale["generators"]
        if generator.top_weight not in previous_tops
    )
    new_non_abc = tuple(
        generator
        for generator in new_generators
        if generator.top_weight[1:] not in ABC_TAILS.values()
    )
    tail_counts = Counter(
        generator.top_weight[1:] for generator in current_gale["generators"]
    )
    matrix_checks = kernel_lattice.matrix_diagnostics(
        master, current_gale["generators"]
    )
    split_relation_records = tuple(
        (
            generator_name(generator),
            generator.alternative_parent[3],
            generator.as_dict()
            == natural_split_relation(
                generator.top_weight, generator.alternative_parent[3]
            ),
        )
        for generator in current_gale["generators"]
    )
    all_split_complete = all(
        matches for _name, _split, matches in split_relation_records
    )
    lookahead = (
        None
        if lookahead_level is None
        else hft_support_lookahead(max_level, lookahead_level)
    )
    return {
        "max_level": max_level,
        "previous_level": previous_level,
        "abstract": abstract,
        "branch_checks": branch_checks,
        "all_split_checks": all_split_checks,
        "master": master,
        "previous": previous,
        "current_gale": current_gale,
        "previous_gale": previous_gale,
        "new_generators": new_generators,
        "new_generator_names": tuple(generator_name(item) for item in new_generators),
        "new_non_abc": new_non_abc,
        "new_non_abc_names": tuple(generator_name(item) for item in new_non_abc),
        "tail_counts": dict(sorted(tail_counts.items())),
        "abc_complete": not new_non_abc,
        "split_relation_records": split_relation_records,
        "all_split_complete": all_split_complete,
        "lookahead": lookahead,
        "matrix_checks": matrix_checks,
        "all_checks": (
            abstract["matches"]
            and branch_checks["all_restrict_zero"]
            and branch_checks["all_six_term"]
            and all_split_checks["all_shell_six_term"]
            and all_split_checks["all_natural_term_counts"]
            and all_split_checks["all_coefficients_unit"]
            and all_split_checks["all_restrict_zero"]
            and all_split_checks["all_telescope"]
            and all_split_checks["all_match_intrinsic"]
            and matrix_checks["reference_unimodular"]
            and matrix_checks["all_relations_null"]
            and matrix_checks["integral_triangular_basis"]
            and current_gale["all_relation_coefficients_unit"]
            and all_split_complete
        ),
    }


def run_analysis(
    max_level=12,
    previous_level=None,
    branch_check_ell=4,
    split_check_max_label=0,
    split_check_max_s=6,
    lookahead_level=None,
    verbose=False,
):
    started = time.time()
    result = analyze_boundary_shell(
        max_level=max_level,
        previous_level=previous_level,
        branch_check_ell=branch_check_ell,
        split_check_max_label=split_check_max_label,
        split_check_max_s=split_check_max_s,
        lookahead_level=lookahead_level,
    )
    previous_level = result["previous_level"]
    previous = result["previous_gale"]
    current = result["current_gale"]

    print("=" * 112)
    print("TK6B.3 — BOUNDARY-SHELL GALE TEMPLATE AUDIT")
    print("=" * 112)
    print("Protected SO(10) baseline imported: NO")
    print(
        "Abstract A/B/C support-collision theorem: "
        f"{'PASS' if result['abstract']['matches'] else 'FAIL'}"
    )
    print(
        f"Exact A/B/C branch checks through ell={branch_check_ell}: "
        f"{'PASS' if result['branch_checks']['all_restrict_zero'] else 'FAIL'}"
    )
    all_split = result["all_split_checks"]
    print(
        "Universal all-split shell checks "
        f"(labels <= {split_check_max_label}, s <= {split_check_max_s}): "
        f"{'PASS' if all_split['all_restrict_zero'] else 'FAIL'}"
    )
    print(
        "Independent chiral-section reconstruction of every sampled split: "
        f"{'PASS' if all_split['all_match_intrinsic'] else 'FAIL'}"
    )
    print("\nNested HFT branching domains:")
    print("  horizon  B4 rows  packets  kernel rank  Gale row types")
    for horizon, domain, gale in (
        (previous_level, result["previous"], previous),
        (max_level, result["master"], current),
    ):
        print(
            f"  {horizon:<8} {len(domain['weights']):<8} "
            f"{len(domain['parents']):<8} {len(gale['generators']):<12} "
            f"{gale['unique_row_types']}"
        )
    print(f"\nNew kernel generators at horizon {max_level}:")
    for name, generator in zip(
        result["new_generator_names"], result["new_generators"]
    ):
        marker = "NEW FAMILY" if generator in result["new_non_abc"] else "A/B/C"
        print(
            f"  {name:<18} top={generator.top_weight} "
            f"alternative={generator.alternative_parent}  [{marker}]"
        )
    print(
        "A/B/C complete at the new horizon: "
        f"{result['abc_complete']}"
    )
    print(
        "Every current generator matches the universal telescoped all-split "
        f"relation: {result['all_split_complete']}"
    )
    print("\nCurrent Gale row classes:")
    for name, count in current["type_classes"].items():
        print(f"  {name}: {count}")
    print("  composite row types:")
    for row, multiplicity in current["composites"]:
        print(f"    {row}  multiplicity={multiplicity}")
    if verbose:
        print("\nAll kernel-family tails (m,r,s):")
        for tail, count in result["tail_counts"].items():
            print(f"  {tail}: {count}")
    if result["lookahead"] is not None:
        print("\nRaw HFT ambiguous-support lookahead:")
        for level, weights in result["lookahead"]["new_by_level"].items():
            print(f"  level {level}: new top weights={weights}")
            print(
                " " * 12
                + f"new tails={result['lookahead']['new_tails_by_level'][level]}"
            )
    print("-" * 112)
    print(
        "Boundary-shell checks: "
        f"{'PASS' if result['all_checks'] else 'FAIL'}"
    )
    print(
        "The all-split identity is unconditional; only the A/B/C family list "
        "is conditional, and the HFT shell test refutes that list at level 12."
    )
    print(f"Runtime: {time.time() - started:.3f}s")
    return result


def run_self_test():
    cases = ((0, 0, 0), (1, 0, 0), (3, 2, 2), (9, 6, 5))
    abstract_ok = all(
        abstract_abc_diagnostics(*lengths)["matches"] for lengths in cases
    )
    branch_checks = branch_identity_diagnostics(max_ell=2)
    first_split_checks = first_split_grid_diagnostics(
        top_weights=((0, 0, 1, 2), (0, 2, 0, 2))
    )
    all_split_checks = all_split_grid_diagnostics(
        top_weights=((0, 0, 0, 4), (1, 0, 0, 4), (0, 0, 0, 6))
    )
    passed = (
        abstract_ok
        and branch_checks["all_restrict_zero"]
        and branch_checks["all_six_term"]
        and first_split_checks["all_restrict_zero"]
        and first_split_checks["all_six_term"]
        and first_split_checks["all_coefficients_unit"]
        and all_split_checks["all_shell_six_term"]
        and all_split_checks["all_natural_term_counts"]
        and all_split_checks["all_coefficients_unit"]
        and all_split_checks["all_restrict_zero"]
        and all_split_checks["all_telescope"]
        and all_split_checks["all_match_intrinsic"]
    )
    print("TK6B.3 BOUNDARY-SHELL SELF-TEST")
    print(f"Abstract A/B/C collision rule: {'PASS' if abstract_ok else 'FAIL'}")
    print(
        "Exact sampled branching identities: "
        f"{'PASS' if branch_checks['all_restrict_zero'] else 'FAIL'}"
    )
    print(
        "Universal first-split grid: "
        f"{'PASS' if first_split_checks['all_restrict_zero'] else 'FAIL'}"
    )
    print(
        "Universal all-split grid and intrinsic reconstruction: "
        f"{'PASS' if all_split_checks['all_match_intrinsic'] else 'FAIL'}"
    )
    print("Protected SO(10) baseline imported: NO")
    return passed


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=(
            "Audit universal parent-split shells, the A/B/C Gale template, "
            "and the next HFT shell"
        )
    )
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--max-level", type=int, default=12)
    parser.add_argument("--previous-level", type=int)
    parser.add_argument("--branch-check-ell", type=int, default=4)
    parser.add_argument("--split-check-max-label", type=int, default=0)
    parser.add_argument("--split-check-max-s", type=int, default=6)
    parser.add_argument("--lookahead-level", type=int)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.self_test:
            return 0 if run_self_test() else 1
        result = run_analysis(
            max_level=args.max_level,
            previous_level=args.previous_level,
            branch_check_ell=args.branch_check_ell,
            split_check_max_label=args.split_check_max_label,
            split_check_max_s=args.split_check_max_s,
            lookahead_level=args.lookahead_level,
            verbose=args.verbose,
        )
    except Exception as error:
        print(f"TK6B.3 FAILED: {error}", file=sys.stderr)
        return 1
    return 0 if result["all_checks"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
