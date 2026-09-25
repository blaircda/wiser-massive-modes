"""GU5: baseline-free audit of the naive interlacing-depth proposal.

The proposed refinement identifies the Bars source label with the standard
``D5 -> B4`` interlacing depth

    ell_prime = lambda_1 - mu_1.

For every mass level this module exhaustively enumerates positive lifts of the
depth-refined HFT target.  Outer-conjugate parents have identical refined
columns, so the search first enumerates their total multiplicities and then
counts all chirality orientations exactly.

No protected ``SO(10)`` completion or literature candidate is imported.
"""

import argparse
from functools import lru_cache

from sage.all import ZZ

import finite_cross_section as cross
from graded_uplift import direct_closed_low_levels as direct
from trajectory_kernel import kernel_lattice


@lru_cache(maxsize=None)
def parent_depth_column(parent):
    """Sparse refined restriction of one ``D5`` parent."""
    twice_lambda_one = (
        2 * (parent[0] + parent[1] + parent[2]) + parent[3] + parent[4]
    )
    result = {}
    for child, coefficient in cross.character_coefficients(
        cross.branch_parent(parent)
    ).items():
        twice_mu_one = 2 * (child[0] + child[1] + child[2]) + child[3]
        difference = twice_lambda_one - twice_mu_one
        if difference < 0 or difference % 2:
            raise ValueError(f"Invalid interlacing depth: {parent} -> {child}")
        depth = difference // 2
        result[depth, child] = int(coefficient)
    return kernel_lattice.clean_sparse(result)


def target_depth_table(level, single_levels):
    """The proposed refined target ``sum t^(n-ell) r_ell``."""
    result = {}
    for oscillator_level in range(1, level + 1):
        depth = level - oscillator_level
        for child, coefficient in cross.character_coefficients(
            single_levels[oscillator_level]
        ).items():
            result[depth, child] = int(coefficient)
    return kernel_lattice.clean_sparse(result)


def orbit_column(orbit):
    """The common column of the parents in an outer orbit."""
    columns = tuple(parent_depth_column(parent) for parent in orbit)
    if any(column != columns[0] for column in columns[1:]):
        raise ValueError(f"Outer-conjugate refined columns differ: {orbit}")
    return columns[0]


def enumerate_unoriented_fibre(level, single_levels, weights):
    """Enumerate positive solutions modulo independent chirality orientation."""
    target = target_depth_table(level, single_levels)
    solutions = []
    dead_ends = []

    def visit(index, residual, orbit_totals):
        if index == len(weights):
            if not residual:
                solutions.append(dict(orbit_totals))
            else:
                dead_ends.append((index, dict(residual)))
            return

        weight = weights[index]
        multiplicity = residual.get((0, weight), 0)
        if multiplicity not in ZZ or multiplicity < 0:
            dead_ends.append((index, dict(residual)))
            return

        orbits = direct.outer_parent_orbits(weight)
        for values in direct.weighted_compositions(
            int(multiplicity), (1,) * len(orbits)
        ):
            updated_residual = dict(residual)
            updated_totals = dict(orbit_totals)
            for orbit, coefficient in zip(orbits, values):
                if not coefficient:
                    continue
                updated_residual = kernel_lattice.add_sparse(
                    updated_residual, orbit_column(orbit), scale=-coefficient
                )
                updated_totals[orbit] = coefficient
            visit(index + 1, updated_residual, updated_totals)

    visit(0, target, {})
    return {
        "target": target,
        "solutions": tuple(solutions),
        "dead_ends": tuple(dead_ends),
    }


def oriented_count(solution):
    """Count actual positive characters represented by orbit totals."""
    count = 1
    for orbit, total in solution.items():
        if len(orbit) == 2:
            count *= total + 1
    return count


def outer_even_count(solution):
    """Count outer-invariant chiral lifts represented by one solution."""
    return int(
        all(len(orbit) == 1 or total % 2 == 0 for orbit, total in solution.items())
    )


def expand_orientations(solution):
    """Generate every oriented positive character in one compressed solution."""
    items = tuple(solution.items())
    coefficients = {}

    def visit(index):
        if index == len(items):
            yield kernel_lattice.clean_sparse(coefficients)
            return
        orbit, total = items[index]
        if len(orbit) == 1:
            coefficients[orbit[0]] = total
            yield from visit(index + 1)
            coefficients.pop(orbit[0], None)
            return
        left, right = orbit
        for left_value in range(total + 1):
            right_value = total - left_value
            if left_value:
                coefficients[left] = left_value
            else:
                coefficients.pop(left, None)
            if right_value:
                coefficients[right] = right_value
            else:
                coefficients.pop(right, None)
            yield from visit(index + 1)
        coefficients.pop(left, None)
        coefficients.pop(right, None)

    yield from visit(0)


def best_obstruction(audit, weights):
    """Return a compact terminal residual from a failed exhaustive search."""
    if audit["solutions"] or not audit["dead_ends"]:
        return None
    scored = []
    for index, residual in audit["dead_ends"]:
        negative = tuple(
            sorted((key, value) for key, value in residual.items() if value < 0)
        )
        score = (
            len(negative),
            -sum(value for _key, value in negative),
            len(residual),
            -index,
        )
        scored.append((score, index, negative, residual))
    _score, index, negative, residual = min(scored)
    negative_sets = [
        {
            (key, value)
            for key, value in dead_residual.items()
            if value < 0
        }
        for _dead_index, dead_residual in audit["dead_ends"]
    ]
    common_negative = tuple(sorted(set.intersection(*negative_sets)))
    return {
        "next_weight": None if index == len(weights) else weights[index],
        "representative_negative": negative,
        "common_negative": common_negative,
        "residual": residual,
    }


def run_audit(max_level=6, verbose=False):
    if max_level < 1 or max_level > 6:
        raise ValueError("GU5 is currently scoped to levels 1--6")
    single_levels, _cumulative = cross.derive_cumulative_so9(max_level)
    weights = direct.full_outer_closure(
        tuple(single_levels[level] for level in range(1, max_level + 1))
    )

    results = {}
    print("=" * 108)
    print("GU5 — INTERLACING-DEPTH AUDIT (BASELINE-FREE)")
    print("=" * 108)
    print("Proposed rule: ell_prime = lambda_1 - mu_1")
    print("Domain: complete full-parent branching closure; no coefficient cutoff")
    print("Protected SO(10) baseline imported: NO")
    print()
    print(" level | refined rows | unoriented fibres | positive lifts | outer-even chiral lifts")
    for level in range(1, max_level + 1):
        audit = enumerate_unoriented_fibre(level, single_levels, weights)
        solutions = audit["solutions"]
        positive_count = sum(oriented_count(item) for item in solutions)
        invariant_count = sum(outer_even_count(item) for item in solutions)
        obstruction = best_obstruction(audit, weights)
        results[level] = {
            **audit,
            "positive_count": positive_count,
            "outer_even_count": invariant_count,
            "obstruction": obstruction,
        }
        print(
            f" {level:5d} | {len(audit['target']):12d} | "
            f"{len(solutions):17d} | {positive_count:14d} | {invariant_count:23d}"
        )
        if verbose and obstruction is not None:
            print(f"         next top weight: {obstruction['next_weight']}")
            print(
                "         negative residual common to every search branch: "
                f"{obstruction['common_negative']}"
            )

    first_failure = next(
        (level for level, result in results.items() if not result["solutions"]),
        None,
    )
    checks = (
        all(results[level]["positive_count"] > 0 for level in range(1, 5))
        and first_failure == 5
        and not results[6]["solutions"]
    )
    print("-" * 108)
    print(f"First level with no positive depth-compatible lift: {first_failure}")
    print(
        "Conclusion: the unmodified interlacing-depth rule is obstructed "
        "before the level-6 selection problem."
    )
    print(f"GU5 exact checks: {'PASS' if checks else 'FAIL'}")
    return {
        "single_levels": single_levels,
        "weights": weights,
        "results": results,
        "first_failure": first_failure,
        "all_checks": checks,
    }


def run_self_test():
    vector = (1, 0, 0, 0, 0)
    conjugate_spinors = ((0, 0, 0, 0, 1), (0, 0, 0, 1, 0))
    checks = (
        set(parent_depth_column(vector))
        == {(0, (1, 0, 0, 0)), (1, (0, 0, 0, 0))},
        parent_depth_column(conjugate_spinors[0])
        == parent_depth_column(conjugate_spinors[1]),
        oriented_count({conjugate_spinors: 3}) == 4,
        outer_even_count({conjugate_spinors: 3}) == 0,
        outer_even_count({conjugate_spinors: 4}) == 1,
    )
    passed = all(checks)
    print("GU5 INTERLACING-DEPTH SELF-TEST")
    print(f"Refined-column and orbit-count checks: {'PASS' if passed else 'FAIL'}")
    print("Protected SO(10) baseline imported: NO")
    return passed


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Audit ell_prime as D5/B4 interlacing depth"
    )
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--max-level", type=int, default=6)
    parser.add_argument("--verbose", action="store_true")
    arguments = parser.parse_args()
    if arguments.self_test:
        raise SystemExit(0 if run_self_test() else 1)
    result = run_audit(arguments.max_level, arguments.verbose)
    raise SystemExit(0 if result["all_checks"] else 1)
