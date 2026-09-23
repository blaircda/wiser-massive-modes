#!/usr/bin/env python3
"""Exhaustive baseline-free search for finite D5 -> B4 cross-sections.

For the cumulative HFT SO(9) spectra through a requested level, this script:

1. closes the finite B4 support under *every* positive-chirality top parent;
2. lists every parent ambiguity ``[l,m,r,k,s-k]``;
3. enumerates one global parent choice for each ambiguous B4 top weight; and
4. tests exactness, integrality, and nonnegative D5 coefficients at every level.

The search uses the SO(9) data being lifted, so a successful section is finite
evidence, not an all-orders rule or a proof of physical uniqueness.  No
protected SO(10) baseline is imported.
"""

import argparse
import itertools
import sys
import time

from sage.all import ZZ

import finite_cross_section as cross


def full_family_closure(targets):
    """Close target supports under every allowed positive-chirality parent."""
    support = set()
    for target in targets.values():
        support.update(cross.character_coefficients(target))
    pending = list(support)

    while pending:
        mu = pending.pop()
        for parent in cross.positive_chirality_parent_family(mu):
            branch = cross.branch_parent(parent)
            for child in cross.character_coefficients(branch):
                if child not in support:
                    support.add(child)
                    pending.append(child)

    return tuple(
        sorted(support, key=cross.b4_dynkin_to_ambient, reverse=True)
    )


def prepare_branch_tables(weights):
    """Precompute sparse integer branching columns for every candidate parent."""
    tables = {}
    for mu in weights:
        for parent in cross.positive_chirality_parent_family(mu):
            tables[parent] = cross.character_coefficients(
                cross.branch_parent(parent)
            )
    return tables


def invert_sparse(target_table, weights, selection, branch_tables):
    """Perform exact triangular inversion using sparse coefficient dictionaries."""
    residual = dict(target_table)
    lift_coefficients = {}

    for mu in weights:
        multiplicity = residual.get(mu, 0)
        parent = selection[mu]
        lift_coefficients[parent] = multiplicity
        if multiplicity:
            for child, branch_multiplicity in branch_tables[parent].items():
                updated = residual.get(child, 0) - multiplicity * branch_multiplicity
                if updated:
                    residual[child] = updated
                else:
                    residual.pop(child, None)

    exact = not residual
    integral = all(value in ZZ for value in lift_coefficients.values())
    positive = integral and all(value >= 0 for value in lift_coefficients.values())
    return exact, integral, positive, lift_coefficients, residual


def search_sections(max_level=10, max_solutions=None):
    """Return every global finite selection positive at levels 1..max_level."""
    _single, cumulative = cross.derive_cumulative_so9(max_level)
    weights = full_family_closure(cumulative)
    branch_tables = prepare_branch_tables(weights)
    target_tables = {
        level: cross.character_coefficients(cumulative[level])
        for level in range(1, max_level + 1)
    }

    fixed = {}
    ambiguous = []
    for mu in weights:
        family = cross.positive_chirality_parent_family(mu)
        if len(family) == 1:
            fixed[mu] = family[0]
        else:
            ambiguous.append((mu, family))

    candidate_count = 1
    for _mu, family in ambiguous:
        candidate_count *= len(family)

    solutions = []
    failures_by_first_level = {level: 0 for level in range(1, max_level + 1)}
    individual_positive_counts = {level: 0 for level in range(1, max_level + 1)}
    failure_records = []
    structural_failures = 0

    for parent_choices in itertools.product(*(family for _mu, family in ambiguous)):
        selection = dict(fixed)
        selection.update(
            (ambiguous[index][0], parent)
            for index, parent in enumerate(parent_choices)
        )

        valid = True
        first_positivity_failure = None
        level_coefficients = {}
        for level in range(1, max_level + 1):
            exact, integral, positive, coefficients, _residual = invert_sparse(
                target_tables[level], weights, selection, branch_tables
            )
            if not exact or not integral:
                structural_failures += 1
                valid = False
                break
            if positive:
                individual_positive_counts[level] += 1
                level_coefficients[level] = coefficients
            elif first_positivity_failure is None:
                first_positivity_failure = level
                failures_by_first_level[level] += 1
                failure_records.append(
                    {
                        "level": level,
                        "selection": selection,
                        "negative_parents": tuple(
                            (parent, int(value))
                            for parent, value in coefficients.items()
                            if value < 0
                        ),
                    }
                )
                valid = False

        if valid and first_positivity_failure is None:
            solutions.append(
                {
                    "selection": selection,
                    "level_coefficients": level_coefficients,
                }
            )
            if max_solutions is not None and len(solutions) >= max_solutions:
                break

    return {
        "weights": weights,
        "ambiguous": tuple(ambiguous),
        "candidate_count": candidate_count,
        "solutions": solutions,
        "failures_by_first_level": failures_by_first_level,
        "individual_positive_counts": individual_positive_counts,
        "failure_records": failure_records,
        "structural_failures": structural_failures,
    }


def summarize_search(result, max_level):
    print("=" * 96)
    print("EXHAUSTIVE FINITE CROSS-SECTION SEARCH (BASELINE-FREE)")
    print("=" * 96)
    print(f"Levels required positive: 1 through {max_level}")
    print(f"Finite closed B4 basis size: {len(result['weights'])}")
    print(f"Ambiguous top weights: {len(result['ambiguous'])}")
    print(f"Global selections tested: {result['candidate_count']}")
    print("Protected SO(10) baseline imported: NO")
    print("\nAllowed parent families:")
    for mu, family in result["ambiguous"]:
        print(f"  B4 {mu}: {family}")

    print("\nFirst failed positivity level among rejected selections:")
    for level, count in result["failures_by_first_level"].items():
        if count:
            print(f"  level {level}: {count}")
    if result["structural_failures"]:
        print(f"  structural inversion failures: {result['structural_failures']}")

    print("\nSelections positive when each cumulative level is tested separately:")
    for level, count in result["individual_positive_counts"].items():
        print(f"  level {level}: {count} / {result['candidate_count']}")

    print("\nChoice-by-choice obstruction certificates:")
    outcomes = result["failure_records"] + [
        {"level": "PASS", "selection": solution["selection"]}
        for solution in result["solutions"]
    ]
    found_certificate = False
    for mu, family in result["ambiguous"]:
        for parent in family:
            parent_outcomes = {
                outcome["level"]
                for outcome in outcomes
                if outcome["selection"][mu] == parent
            }
            if len(parent_outcomes) == 1:
                found_certificate = True
                only_outcome = next(iter(parent_outcomes))
                print(f"  B4 {mu} -> D5 {parent}: always first fails at level {only_outcome}")
                matching_failures = [
                    outcome
                    for outcome in result["failure_records"]
                    if outcome["selection"][mu] == parent
                ]
                if matching_failures:
                    common_negative = set(matching_failures[0]["negative_parents"])
                    for failure in matching_failures[1:]:
                        common_negative.intersection_update(failure["negative_parents"])
                    if common_negative:
                        print(f"    unavoidable negative coefficient(s): {sorted(common_negative)}")
    if not found_certificate:
        print("  No single parent choice determines the first failure level by itself.")

    solutions = result["solutions"]
    print(f"\nSelections positive at every tested level: {len(solutions)}")
    if not solutions:
        print("Result: [NO POSITIVE GLOBAL CROSS-SECTION IN THE TESTED FAMILY]")
        return

    for solution_index, solution in enumerate(solutions, start=1):
        print(f"\nSolution {solution_index} ambiguous choices:")
        for mu, _family in result["ambiguous"]:
            print(f"  B4 {mu} -> D5 {solution['selection'][mu]}")
    print("Result: [FINITE POSITIVE CROSS-SECTION(S) FOUND]")
    print("This is finite fitted evidence, not an all-orders selection theorem.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Exhaustively search global positive-chirality cross-sections"
    )
    parser.add_argument("--max-level", type=int, default=10)
    parser.add_argument(
        "--max-solutions",
        type=int,
        default=None,
        help="Stop after this many solutions (default: enumerate all)",
    )
    args = parser.parse_args()

    started = time.time()
    search_result = search_sections(args.max_level, args.max_solutions)
    summarize_search(search_result, args.max_level)
    print(f"Elapsed: {time.time() - started:.3f}s")
    sys.exit(0)
