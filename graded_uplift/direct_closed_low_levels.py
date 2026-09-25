"""GU4: direct low-level closed ``SO(9) -> SO(10)`` lift.

This module deliberately starts from the closed primary target

    T_n = R_n^9 tensor R_n^9,

where ``R_n^9=sum_(ell=1)^n r_ell^9`` is derived from the HFT formula.  It
does not form a product of the virtual chiral HFT ``SO(10)`` numerators.

The finite search includes every ``D5`` top parent of every ``B4`` weight in
the branching closure.  It enumerates all nonnegative integral lifts that are
invariant under the ``D5`` outer automorphism.  No protected ``SO(10)``
baseline is imported.

The calculation also keeps the Bars source labels
``ell_prime=n-ell`` long enough to test the stronger (and, as the result
shows, inappropriate) requirement that restriction preserve each source
block separately.
"""

import argparse
from functools import lru_cache

from sage.all import ZZ

import finite_cross_section as cross
from trajectory_kernel import closed_level2
from trajectory_kernel import kernel_lattice


def outer_conjugate_label(parent):
    """Exchange the two spinor nodes of a ``D5`` Dynkin label."""
    a1, a2, a3, a4, a5 = parent
    return (a1, a2, a3, a5, a4)


def full_parent_family(weight):
    """All ``D5`` parents whose top ``B4`` component is ``weight``."""
    ell, m, r, s = weight
    if min(weight) < 0:
        raise ValueError(f"Negative B4 Dynkin label: {weight}")
    return tuple((ell, m, r, k, s - k) for k in range(s + 1))


def outer_parent_orbits(weight):
    """Outer-automorphism orbits in the full top-parent family."""
    family = set(full_parent_family(weight))
    orbits = []
    while family:
        parent = min(family)
        conjugate = outer_conjugate_label(parent)
        members = tuple(sorted({parent, conjugate}))
        family.difference_update(members)
        orbits.append(members)
    return tuple(orbits)


@lru_cache(maxsize=None)
def orbit_branch_table(orbit):
    """Restriction column of the sum of all parents in one outer orbit."""
    result = {}
    for parent in orbit:
        result = kernel_lattice.add_sparse(
            result,
            cross.character_coefficients(cross.branch_parent(parent)),
        )
    return result


def full_outer_closure(targets):
    """Close target supports under every full-family parent branching."""
    support = set()
    for target in targets:
        support.update(cross.character_coefficients(target))
    pending = list(support)
    while pending:
        weight = pending.pop()
        for orbit in outer_parent_orbits(weight):
            for child in orbit_branch_table(orbit):
                if child not in support:
                    support.add(child)
                    pending.append(child)
    return tuple(
        sorted(support, key=cross.b4_dynkin_to_ambient, reverse=True)
    )


def weighted_compositions(total, weights):
    """Enumerate nonnegative ``x`` satisfying ``sum weights[i]*x[i]=total``."""
    if total < 0:
        return
    values = [0] * len(weights)

    def visit(index, remaining):
        if index == len(weights):
            if remaining == 0:
                yield tuple(values)
            return
        weight = weights[index]
        for value in range(remaining // weight + 1):
            values[index] = value
            yield from visit(index + 1, remaining - weight * value)
        values[index] = 0

    yield from visit(0, int(total))


def enumerate_positive_lifts(target, weights=None, outer_invariant=True):
    """Enumerate the complete finite positive lift fibre.

    Triangularity makes every coefficient range exact: at a top weight
    ``mu``, the current residual coefficient must be partitioned among the
    allowed parent groups above ``mu``. Outer-invariant groups are full
    automorphism orbits; without that condition they are singletons. No
    artificial coefficient cutoff is used.
    """
    if weights is None:
        weights = full_outer_closure((target,))
    target_table = kernel_lattice.clean_sparse(
        cross.character_coefficients(target)
    )
    solutions = []

    def visit(index, residual, coefficients):
        if index == len(weights):
            if not residual:
                solutions.append(kernel_lattice.clean_sparse(coefficients))
            return

        weight = weights[index]
        multiplicity = residual.get(weight, 0)
        if multiplicity not in ZZ or multiplicity < 0:
            return
        orbits = (
            outer_parent_orbits(weight)
            if outer_invariant
            else tuple((parent,) for parent in full_parent_family(weight))
        )
        top_multiplicities = tuple(len(orbit) for orbit in orbits)
        for orbit_coefficients in weighted_compositions(
            int(multiplicity), top_multiplicities
        ):
            updated_residual = dict(residual)
            updated_coefficients = dict(coefficients)
            for orbit, coefficient in zip(orbits, orbit_coefficients):
                if not coefficient:
                    continue
                updated_residual = kernel_lattice.add_sparse(
                    updated_residual,
                    orbit_branch_table(orbit),
                    scale=-coefficient,
                )
                for parent in orbit:
                    updated_coefficients[parent] = (
                        updated_coefficients.get(parent, 0) + coefficient
                    )
            visit(index + 1, updated_residual, updated_coefficients)

    visit(0, target_table, {})
    return tuple(solutions)


def d5_character(coefficients):
    """Convert a sparse Dynkin-label table to a ``D5`` character."""
    return sum(
        (
            coefficient * cross.D5(*parent)
            for parent, coefficient in coefficients.items()
        ),
        cross.D5(0),
    )


def d5_coefficients(character):
    """Return irreducible coefficients keyed by ``D5`` Dynkin labels."""
    result = {}
    for weight, coefficient in character.monomial_coefficients().items():
        x1, x2, x3, x4, x5 = weight.to_vector()
        parent = (
            int(x1 - x2),
            int(x2 - x3),
            int(x3 - x4),
            int(x4 - x5),
            int(x4 + x5),
        )
        if coefficient:
            result[parent] = int(coefficient)
    return dict(sorted(result.items()))


def depth_graded_restriction(character):
    """Grade ``D5 -> B4`` components by interlacing depth.

    For highest orthogonal coordinates ``lambda`` and ``mu``, the depth is
    ``d=lambda_1-mu_1``.  It is a nonnegative integer under the standard
    interlacing branching rule.
    """
    result = {}
    for parent, parent_coefficient in d5_coefficients(character).items():
        twice_lambda_one = (
            2 * (parent[0] + parent[1] + parent[2])
            + parent[3]
            + parent[4]
        )
        for child, child_coefficient in cross.character_coefficients(
            cross.branch_parent(parent)
        ).items():
            twice_mu_one = 2 * (child[0] + child[1] + child[2]) + child[3]
            difference = twice_lambda_one - twice_mu_one
            if difference < 0 or difference % 2:
                raise ValueError(
                    f"Invalid D5/B4 interlacing depth for {parent} -> {child}"
                )
            depth = difference // 2
            result[depth] = (
                result.get(depth, cross.B4(0))
                + parent_coefficient * child_coefficient * cross.B4(*child)
            )
    return {depth: value for depth, value in sorted(result.items()) if value}


def tagged_primary_blocks(level, single_levels):
    """Closed source blocks keyed by ``(ell_prime_L,ell_prime_R)``."""
    return {
        (level - left, level - right): single_levels[left] * single_levels[right]
        for left in range(1, level + 1)
        for right in range(1, level + 1)
    }


def solution_checks(target, coefficients):
    character = d5_character(coefficients)
    conjugate_coefficients = {
        outer_conjugate_label(parent): coefficient
        for parent, coefficient in coefficients.items()
    }
    return {
        "character": character,
        "positive": all(value >= 0 for value in coefficients.values()),
        "outer_invariant": coefficients == conjugate_coefficients,
        "restriction_exact": (
            character.branch(cross.B4, rule="default") == target
        ),
    }


def expected_low_level_factors():
    """Intrinsic left/right factors, not protected baseline data."""
    vector = cross.D5(1, 0, 0, 0, 0)
    rank_two = cross.D5(2, 0, 0, 0, 0)
    spinor_plus = cross.D5(0, 0, 0, 0, 1)
    spinor_minus = cross.D5(0, 0, 0, 1, 0)
    return {
        1: (
            cross.D5(0, 0, 0, 0, 0),
            cross.D5(0, 0, 0, 0, 0),
        ),
        2: (vector, vector),
        3: (rank_two + spinor_plus, rank_two + spinor_minus),
    }


def run_direct_closed(max_level=3, verbose=False):
    """Run the exact direct closed search through level 2 or 3."""
    if max_level not in (2, 3):
        raise ValueError("The exhaustive GU4 calculation is scoped to levels 2 or 3")

    single_levels, cumulative = cross.derive_cumulative_so9(max_level)
    targets = {
        level: cumulative[level] * cumulative[level]
        for level in range(1, max_level + 1)
    }
    common_weights = full_outer_closure(tuple(targets.values()))
    expected_factors = expected_low_level_factors()
    closed_factor = closed_level2.closed_supermultiplet()
    closed_factor_positive = closed_level2.positive_character(closed_factor)
    factor_outer_even = (
        closed_level2.kernel_anomaly.outer_conjugate(closed_factor)
        == closed_factor
    )
    closed_factor_restriction = closed_factor.branch(
        cross.B4, rule="default"
    )

    results = {}
    print("=" * 118)
    print("GU4 — DIRECT CLOSED LOW-LEVEL LIFT (BASELINE-FREE)")
    print("=" * 118)
    print("Target: T_n = R_n^9 tensor R_n^9")
    print("Domain: complete finite D5 top-parent closure, both chiralities")
    print("Constraints: nonnegative integral coefficients and outer invariance")
    print("Protected SO(10) baseline imported: NO")
    print()
    print(" level | B4 terms | rows | positive lifts | outer-even lifts | expected form")
    for level in range(1, max_level + 1):
        solutions = enumerate_positive_lifts(
            targets[level], weights=common_weights
        )
        unrestricted_solutions = enumerate_positive_lifts(
            targets[level], weights=common_weights, outer_invariant=False
        )
        checks = tuple(solution_checks(targets[level], item) for item in solutions)
        left_factor, right_factor = expected_factors[level]
        expected_character = left_factor * right_factor
        expected_matches = tuple(
            check["character"] == expected_character for check in checks
        )
        expected_depth_image = {
            level - oscillator_level: single_levels[oscillator_level]
            for oscillator_level in range(1, level + 1)
        }
        left_depth_exact = (
            depth_graded_restriction(left_factor) == expected_depth_image
        )
        right_depth_exact = (
            depth_graded_restriction(right_factor) == expected_depth_image
        )
        if not all(
            check["positive"]
            and check["outer_invariant"]
            and check["restriction_exact"]
            for check in checks
        ):
            raise ValueError(f"Invalid enumerated solution at level {level}")

        full_checks = []
        for check in checks:
            full_checks.append(
                {
                    # Positivity and outer invariance are preserved by tensor
                    # products.  Avoid expanding the large 65,536-dimensional
                    # product merely to recheck these elementary implications.
                    "positive": closed_factor_positive and check["positive"],
                    "outer_invariant": factor_outer_even and check["outer_invariant"],
                    "restriction_exact": (
                        closed_factor_restriction
                        * check["character"].branch(cross.B4, rule="default")
                        == closed_factor_restriction * targets[level]
                    ),
                }
            )

        blocks = tagged_primary_blocks(level, single_levels)
        block_results = {}
        for tag, block in blocks.items():
            block_weights = full_outer_closure((block,))
            block_solutions = enumerate_positive_lifts(
                block, weights=block_weights
            )
            block_results[tag] = {
                "target": block,
                "solutions": block_solutions,
            }

        results[level] = {
            "target": targets[level],
            "solutions": solutions,
            "unrestricted_solutions": unrestricted_solutions,
            "checks": checks,
            "expected_matches": expected_matches,
            "left_factor": left_factor,
            "right_factor": right_factor,
            "left_depth_exact": left_depth_exact,
            "right_depth_exact": right_depth_exact,
            "full_checks": tuple(full_checks),
            "tagged_blocks": block_results,
        }
        print(
            f" {level:5d} | {len(cross.character_coefficients(targets[level])):8d} | "
            f"{len(common_weights):4d} | {len(unrestricted_solutions):14d} | "
            f"{len(solutions):16d} | "
            f"{sum(expected_matches)}/{len(solutions)}"
        )

    print()
    print("Level-2 ell-prime source blocks (tested as separately preserved grades):")
    for tag, block in sorted(results[2]["tagged_blocks"].items(), reverse=True):
        target_terms = cross.character_coefficients(block["target"])
        print(
            f"  {tag}: {target_terms}; positive outer-even lifts = "
            f"{len(block['solutions'])}"
        )

    total_level2 = results[2]
    q_checks = total_level2["full_checks"]
    print()
    print("Closed universal factor check:")
    print(f"  dim Q_closed = {int(closed_factor.degree())}")
    print(f"  Q_closed positive and outer-even: {closed_factor_positive and factor_outer_even}")
    print(
        "  Every enumerated Q_closed*T-lift is positive, outer-even, and has "
        "the exact SO(9) restriction: "
        f"{all(item['positive'] and item['outer_invariant'] and item['restriction_exact'] for item in q_checks)}"
    )
    print(
        "  This multiplication is automatic once the primary lift is positive; "
        "it does not further reduce the fibre."
    )

    print()
    print("Source-label reconstruction in the factorized representative:")
    for level, result in results.items():
        print(
            f"  level {level}: left/right interlacing-depth images equal "
            f"sum_(ell<=n) ell_prime^(n-ell) r_ell: "
            f"{result['left_depth_exact']} / {result['right_depth_exact']}"
        )
    print(
        "  Hence their factorized tensor product recovers every "
        "(ell_prime_L,ell_prime_R) source block exactly."
    )

    if verbose:
        for level, result in results.items():
            print(f"\nLevel {level} solutions:")
            for index, check in enumerate(result["checks"], start=1):
                print(f"  {index}: {check['character']}")

    all_checks = all(
        len(result["solutions"]) == 1
        and result["expected_matches"] == (True,)
        and result["left_depth_exact"]
        and result["right_depth_exact"]
        and all(
            item["positive"]
            and item["outer_invariant"]
            and item["restriction_exact"]
            for item in result["full_checks"]
        )
        for result in results.values()
    )
    print()
    print(f"GU4 low-level exact checks: {'PASS' if all_checks else 'FAIL'}")
    return {
        "single_levels": single_levels,
        "cumulative": cumulative,
        "weights": common_weights,
        "closed_factor": closed_factor,
        "results": results,
        "all_checks": all_checks,
    }


def run_self_test():
    vector_weight = (1, 0, 0, 0)
    family = full_parent_family((0, 0, 0, 2))
    orbits = outer_parent_orbits((0, 0, 0, 2))
    checks = (
        full_parent_family(vector_weight) == ((1, 0, 0, 0, 0),),
        len(family) == 3,
        tuple(map(len, orbits)) == (2, 1),
        tuple(weighted_compositions(3, (1, 2)))
        == ((1, 1), (3, 0)),
    )
    passed = all(checks)
    print("GU4 DIRECT CLOSED SELF-TEST")
    print(f"Outer-orbit and triangular-enumeration checks: {'PASS' if passed else 'FAIL'}")
    print("Protected SO(10) baseline imported: NO")
    return passed


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Direct low-level closed SO(9) to SO(10) lift"
    )
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--max-level", type=int, default=3)
    parser.add_argument("--verbose", action="store_true")
    arguments = parser.parse_args()
    if arguments.self_test:
        raise SystemExit(0 if run_self_test() else 1)
    audit = run_direct_closed(arguments.max_level, arguments.verbose)
    raise SystemExit(0 if audit["all_checks"] else 1)
