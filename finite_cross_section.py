#!/usr/bin/env python3
"""Baseline-free finite cross-sections for D5 -> B4 branching.

The restriction of a D5 highest weight ``[a1,a2,a3,a4,a5]`` has top B4
component ``[a1,a2,a3,a4+a5]``.  Hence a B4 top weight
``mu=[l,m,r,s]`` has the finite positive-chirality parent family

    [l,m,r,k,s-k],  0 <= k <= floor(s/2).

Choosing one value of ``k`` for every ``mu`` defines a cross-section on highest
weights.  This module makes that choice explicit and inverts the resulting
finite, unipotent branching system on each cumulative HFT SO(9) spectrum.

It deliberately imports no protected SO(10) baseline.  Comparisons with the
known level-1--10 completion live in
``verify_finite_cross_section_against_baseline.py``.

The default ``chiral`` policy is level-independent and selects ``k=0`` for all
weights.  The alternative ``fermion-chiral-tensor-balanced`` policy implements
the other global convention discussed in the earlier reports: odd-s weights
select ``k=0``, while even-s weights select ``k=s/2``.  Neither policy is
asserted to be physically preferred merely because it is a valid section.
"""

import argparse
import sys
import time
from functools import lru_cache

from sage.all import QQ, ZZ, WeylCharacterRing

import hft_so9


D5 = WeylCharacterRing("D5", base_ring=QQ, style="coroots")
B4 = hft_so9.B4

POLICIES = (
    "chiral",
    "fermion-chiral-tensor-balanced",
)


def _integer(value, description):
    """Return an exact Python integer, rejecting non-integral coordinates."""
    if value not in ZZ:
        raise ValueError(f"Non-integral {description}: {value}")
    return int(value)


def b4_weight_to_dynkin(weight):
    """Convert a B4 ambient highest weight to coroot/Dynkin labels."""
    x1, x2, x3, x4 = weight.to_vector()
    return (
        _integer(x1 - x2, "B4 label l"),
        _integer(x2 - x3, "B4 label m"),
        _integer(x3 - x4, "B4 label r"),
        _integer(2 * x4, "B4 label s"),
    )


def b4_dynkin_to_ambient(mu):
    """Return twice the B4 orthogonal coordinates, for exact ordering."""
    ell, m, r, s = mu
    return (
        2 * (ell + m + r) + s,
        2 * (m + r) + s,
        2 * r + s,
        s,
    )


def character_coefficients(character):
    """Return irreducible B4 coefficients keyed by Dynkin-label tuples."""
    return {
        b4_weight_to_dynkin(weight): coeff
        for weight, coeff in character.monomial_coefficients().items()
        if coeff != 0
    }


def positive_chirality_parent_family(mu):
    """List all D5 top parents with a5 >= a4, omitting outer conjugates."""
    ell, m, r, s = mu
    if min(mu) < 0:
        raise ValueError(f"B4 Dynkin labels must be nonnegative: {mu}")
    return tuple((ell, m, r, k, s - k) for k in range(s // 2 + 1))


def select_parent(mu, policy="chiral"):
    """Select one parent from the finite family using an explicit global rule."""
    if policy not in POLICIES:
        raise ValueError(f"Unknown policy {policy!r}; choose one of {POLICIES}")

    ell, m, r, s = mu
    if policy == "chiral":
        k = 0
    else:
        # Fixed-chirality fermions, lambda_5=0 tensors.
        k = 0 if s % 2 else s // 2
    return (ell, m, r, k, s - k)


def top_b4_weight(parent):
    """Return the top B4 Dynkin label in the restriction of a D5 parent."""
    a1, a2, a3, a4, a5 = parent
    return (a1, a2, a3, a4 + a5)


@lru_cache(maxsize=None)
def branch_parent(parent):
    """Branch one D5 parent, cached by its Dynkin-label tuple."""
    return D5(*parent).branch(B4, rule="default")


@lru_cache(maxsize=None)
def branch_selected_parent(mu, policy="chiral"):
    """Branch the selected D5 parent and return its B4 character."""
    return branch_parent(select_parent(mu, policy))


def finite_branching_closure(target, policy="chiral"):
    """Close target support under branchings of all selected top parents."""
    support = set(character_coefficients(target))
    pending = list(support)

    while pending:
        mu = pending.pop()
        for child in character_coefficients(branch_selected_parent(mu, policy)):
            if child not in support:
                support.add(child)
                pending.append(child)

    return tuple(sorted(support, key=b4_dynkin_to_ambient, reverse=True))


def invert_on_cross_section(target, policy="chiral"):
    """Invert restriction on the finite unipotent section containing target.

    Returns a dictionary containing the finite closed B4 basis, selected D5
    parents and signed coefficients, the lifted D5 character, and exact checks.
    """
    ordered_weights = finite_branching_closure(target, policy)
    residual = target
    coefficients = {}
    lift = D5(0)
    section_ok = True
    diagonal_ok = True
    triangular_ok = True

    for mu in ordered_weights:
        parent = select_parent(mu, policy)
        section_ok = section_ok and top_b4_weight(parent) == mu
        branch = branch_selected_parent(mu, policy)
        branch_coeffs = character_coefficients(branch)
        diagonal_ok = diagonal_ok and branch_coeffs.get(mu, 0) == 1
        triangular_ok = triangular_ok and all(
            b4_dynkin_to_ambient(child) <= b4_dynkin_to_ambient(mu)
            for child in branch_coeffs
        )

        residual_coeffs = character_coefficients(residual)
        multiplicity = residual_coeffs.get(mu, 0)
        coefficients[parent] = multiplicity
        if multiplicity:
            lift += multiplicity * D5(*parent)
            residual -= multiplicity * branch

    exact = residual == B4(0) and lift.branch(B4, rule="default") == target
    integral = all(value in ZZ for value in coefficients.values())
    positive = integral and all(value >= 0 for value in coefficients.values())

    return {
        "policy": policy,
        "weights": ordered_weights,
        "coefficients": coefficients,
        "lift": lift,
        "residual": residual,
        "section_ok": section_ok,
        "diagonal_ok": diagonal_ok,
        "triangular_ok": triangular_ok,
        "exact": exact,
        "integral": integral,
        "positive": positive,
    }


def derive_cumulative_so9(max_level):
    """Derive cumulative SO(9) spectra from the baseline-free HFT formula."""
    _numerator, single_levels = hft_so9.derive_hft_spectrum(max_level)
    cumulative = {}
    running = B4(0)
    for level in range(1, max_level + 1):
        running += single_levels[level]
        cumulative[level] = running
    return single_levels, cumulative


def coefficient_statistics(result):
    """Summarize nonzero positive and negative coefficients."""
    values = [value for value in result["coefficients"].values() if value]
    return {
        "positive_terms": sum(1 for value in values if value > 0),
        "negative_terms": sum(1 for value in values if value < 0),
        "minimum": min(values, default=0),
        "maximum": max(values, default=0),
    }


def run_pipeline(max_level=10, policy="chiral", verbose=False):
    print("=" * 112)
    print("FINITE D5 -> B4 CROSS-SECTION INVERSION (BASELINE-FREE)")
    print(f"Levels 1 through {max_level}; policy: {policy}")
    print("=" * 112)
    print("Assumptions:")
    print("  1. Only positive-chirality parents a5 >= a4 are considered.")
    print("  2. Exactly one parent is selected for each B4 top weight.")
    if policy == "chiral":
        print("  3. Global selection rule: [l,m,r,s] -> [l,m,r,0,s].")
    else:
        print("  3. Global selection rule: odd s -> [l,m,r,0,s];")
        print("     even s -> [l,m,r,s/2,s/2].")
    print("  4. The finite basis is the branching closure of the actual cumulative SO(9) support.")
    print("  5. No claim of physical uniqueness is made; this is a chosen additive section.")
    print("  6. Protected SO(10) baseline imported: NO.")

    started = time.time()
    _single_levels, cumulative = derive_cumulative_so9(max_level)

    print("-" * 112)
    print(
        f"{'Level':<7}{'Basis':<9}{'Section':<10}{'Unipotent':<12}"
        f"{'Exact':<9}{'Integral':<11}{'Positive':<11}{'+ terms':<10}{'- terms':<10}{'Min coeff'}"
    )
    print("-" * 112)

    results = {}
    all_structural = True
    all_positive = True
    for level in range(1, max_level + 1):
        result = invert_on_cross_section(cumulative[level], policy)
        results[level] = result
        stats = coefficient_statistics(result)
        structural = (
            result["section_ok"]
            and result["diagonal_ok"]
            and result["triangular_ok"]
            and result["exact"]
            and result["integral"]
        )
        all_structural = all_structural and structural
        all_positive = all_positive and result["positive"]
        print(
            f"{level:<7}{len(result['weights']):<9}{str(result['section_ok']):<10}"
            f"{str(result['diagonal_ok'] and result['triangular_ok']):<12}"
            f"{str(result['exact']):<9}{str(result['integral']):<11}"
            f"{str(result['positive']):<11}{stats['positive_terms']:<10}"
            f"{stats['negative_terms']:<10}{stats['minimum']}"
        )
        if verbose:
            nonzero = {
                parent: coeff
                for parent, coeff in result["coefficients"].items()
                if coeff
            }
            print(f"      lift coefficients: {nonzero}")

    print("-" * 112)
    print(f"Finite-section structure and exact inversion: {'[PASSED]' if all_structural else '[FAILED]'}")
    print(f"Cumulative positivity for this chosen section: {'[PASSED]' if all_positive else '[FAILED]'}")
    print(f"Elapsed: {time.time() - started:.3f}s")
    print("=" * 112)
    return all_structural, all_positive, results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Invert cumulative HFT SO(9) spectra on an explicit finite D5 cross-section"
    )
    parser.add_argument("--max-level", type=int, default=10)
    parser.add_argument("--policy", choices=POLICIES, default="chiral")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    structural_ok, _positive, _results = run_pipeline(
        max_level=args.max_level,
        policy=args.policy,
        verbose=args.verbose,
    )
    sys.exit(0 if structural_ok else 1)
