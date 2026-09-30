"""TK6B.5c: exact symmetric-vector factorization of the HFT primary series.

Hanany--Forcella--Troost factor the level-one symmetric-vector tower from the
massive primary series,

    Z_m(q) = PE([1,0,0,0] q) Z'_m(q).

This module performs that factorization exactly in the B4 representation ring
and tests whether the observed leading-label Regge shift holds separately at
each coefficient of the virtual remainder.  It imports no protected SO(10)
completion.
"""

import argparse
import sys
import time
from collections import Counter

from sage.all import ZZ

import finite_cross_section as cross
import hft_so9
from trajectory_kernel import chamber_audit
from trajectory_kernel import regge_columns


B4 = hft_so9.B4
VECTOR = B4(1, 0, 0, 0)


def symmetric_vector_coefficient(degree):
    """Return ``Sym^degree([1,0,0,0])`` as an exact B4 character."""
    degree = int(degree)
    if degree < 0:
        return B4(0)
    return sum(
        (B4(degree - 2 * trace, 0, 0, 0)
         for trace in range(degree // 2 + 1)),
        B4(0),
    )


def factor_symmetric_vector_tower(single_levels, max_level):
    """Solve exactly for the virtual HFT remainder coefficients.

    ``single_levels[n]`` uses the project convention in which physical level
    one is the constant term of the HFT massive-primary series.  The returned
    dictionaries use the series degree ``N=n-1``.
    """
    maximum_degree = int(max_level) - 1
    if maximum_degree < 0:
        raise ValueError("The HFT factorization requires max_level >= 1")
    primaries = {
        degree: single_levels[degree + 1]
        for degree in range(maximum_degree + 1)
    }
    symmetric = {
        degree: symmetric_vector_coefficient(degree)
        for degree in range(maximum_degree + 1)
    }
    remainder = {}
    for degree in range(maximum_degree + 1):
        value = primaries[degree]
        for symmetric_degree in range(1, degree + 1):
            value -= (
                symmetric[symmetric_degree]
                * remainder[degree - symmetric_degree]
            )
        remainder[degree] = value

    reconstructed = {
        degree: sum(
            (
                symmetric[symmetric_degree]
                * remainder[degree - symmetric_degree]
                for symmetric_degree in range(degree + 1)
            ),
            B4(0),
        )
        for degree in range(maximum_degree + 1)
    }
    if reconstructed != primaries:
        raise ValueError("The symmetric-vector convolution did not reconstruct HFT")
    return {
        "primaries": primaries,
        "symmetric": symmetric,
        "remainder": remainder,
        "reconstructed": reconstructed,
    }


def character_table(character):
    """Return an integral, possibly signed, Dynkin-label coefficient table."""
    table = cross.character_coefficients(character)
    if any(value not in ZZ for value in table.values()):
        raise ValueError("A factorized HFT coefficient is non-integral")
    return {label: int(value) for label, value in table.items() if value}


def remainder_contributions(factorization):
    """Decompose every primary coefficient by virtual remainder degree."""
    maximum_degree = max(factorization["primaries"])
    contributions = {}
    for degree in range(maximum_degree + 1):
        for remainder_degree in range(degree + 1):
            character = (
                factorization["symmetric"][degree - remainder_degree]
                * factorization["remainder"][remainder_degree]
            )
            contributions[degree, remainder_degree] = character_table(character)
    return contributions


def termwise_ell_shift_diagnostics(single_levels, factorization, max_level):
    """Test each empirical eligible ell shift before summing remainder degrees."""
    multiplicities = {
        level: regge_columns.extract_level_multiplicities(single_levels[level])
        for level in range(1, int(max_level) + 1)
    }
    shifts = tuple(
        item
        for item in chamber_audit.audit_shifts(multiplicities, max_level)
        if item.family == "ell" and item.steps == 1
    )
    contributions = remainder_contributions(factorization)
    records = []
    for item in shifts:
        source_degree = item.source_level - 1
        target_degree = item.target_level - 1
        comparisons = []
        for remainder_degree in range(target_degree + 1):
            source = contributions.get(
                (source_degree, remainder_degree), {}
            ).get(item.source_label, 0)
            target = contributions.get(
                (target_degree, remainder_degree), {}
            ).get(item.target_label, 0)
            comparisons.append((remainder_degree, source, target))
        records.append(
            {
                "shift": item,
                "comparisons": tuple(comparisons),
                "termwise": all(source == target for _degree, source, target in comparisons),
            }
        )
    failures = tuple(record for record in records if not record["termwise"])
    first_failure = failures[0] if failures else None
    return {
        "records": tuple(records),
        "tested": len(records),
        "termwise_matches": len(records) - len(failures),
        "failures": failures,
        "first_failure": first_failure,
        "all_termwise": not failures,
    }


def remainder_statistics(remainder):
    """Summarize signed irreducible content of the virtual remainder."""
    result = {}
    for degree, character in remainder.items():
        values = tuple(character_table(character).values())
        result[degree] = {
            "terms": len(values),
            "positive_terms": sum(value > 0 for value in values),
            "negative_terms": sum(value < 0 for value in values),
            "minimum": min(values, default=0),
            "maximum": max(values, default=0),
        }
    return result


def remainder_support_diagnostics(remainder):
    """Test the observed half-slope bound after removing the Regge tower."""
    records = {}
    for degree, character in remainder.items():
        table = character_table(character)
        heights = {
            label: 2 * label[0] + 2 * label[1] + 2 * label[2] + label[3]
            for label in table
        }
        maximum = max(heights.values(), default=None)
        bound = None if degree < 2 else degree - 1
        records[degree] = {
            "maximum_twice_first_orthogonal_coordinate": maximum,
            "candidate_bound": bound,
            "satisfies": bound is None or maximum is None or maximum <= bound,
        }
    return {
        "records": records,
        "all_satisfy": all(item["satisfies"] for item in records.values()),
    }


def a_tail_endpoint_diagnostics(single_levels, max_level):
    """Evaluate the first telescoped shell-tail inequality on HFT targets."""
    running = B4(0)
    cumulative = {}
    for level in range(1, int(max_level) + 1):
        running += single_levels[level]
        cumulative[level] = character_table(running)
    records = []
    for level in range(6, int(max_level) + 1):
        table = cumulative[level]
        endpoints = (
            table.get((level - 5, 0, 1, 0), 0),
            table.get((level - 5, 1, 0, 0), 0),
            table.get((level - 4, 0, 0, 0), 0),
        )
        scalar = table.get((0, 0, 0, 0), 0)
        slack = scalar - endpoints[0] + endpoints[1] - endpoints[2]
        records.append(
            {
                "level": level,
                "endpoints": endpoints,
                "scalar": scalar,
                "slack": slack,
                "equals_scalar_minus_one": endpoints == (1, 3, 3)
                and slack == scalar - 1,
            }
        )
    return {
        "records": tuple(records),
        "all_endpoints_1_3_3": all(
            item["endpoints"] == (1, 3, 3) for item in records
        ),
        "all_positive": all(item["slack"] >= 0 for item in records),
    }


def run_analysis(max_level=10):
    """Run the exact HFT factorization and termwise-shift audit."""
    if max_level < chamber_audit.GMSZ_FIRST_LEVEL:
        raise ValueError("Use max_level >= 7 to enter the tested shift chamber")
    started = time.time()
    _numerator, single_levels = hft_so9.derive_hft_spectrum(max_level)
    factorization = factor_symmetric_vector_tower(single_levels, max_level)
    statistics = remainder_statistics(factorization["remainder"])
    support = remainder_support_diagnostics(factorization["remainder"])
    shifts = termwise_ell_shift_diagnostics(
        single_levels, factorization, max_level
    )
    a_tail = a_tail_endpoint_diagnostics(single_levels, max_level)
    negative_degrees = tuple(
        degree
        for degree, item in statistics.items()
        if item["negative_terms"]
    )
    failure_pairs = Counter()
    for failure in shifts["failures"]:
        item = failure["shift"]
        failure_pairs[item.source_level, item.target_level] += 1

    print("=" * 100)
    print("TK6B.5c — HFT SYMMETRIC-VECTOR REGGE FACTORIZATION")
    print("=" * 100)
    print(f"Physical HFT levels: 1 through {max_level}")
    print("Exact PE([1,0,0,0] q) convolution reconstruction: True")
    print(f"Virtual remainder degrees containing negative irreps: {negative_degrees}")
    print(f"Remainder half-slope support bound through this order: {support['all_satisfy']}")
    print(f"Eligible adjacent ell shifts tested: {shifts['tested']}")
    print(f"Shifts matching separately at every remainder degree: {shifts['termwise_matches']}")
    print(f"Termwise failures by transition: {dict(sorted(failure_pairs.items()))}")
    print(
        "A-tail moving endpoint multiplicities are (1,3,3): "
        f"{a_tail['all_endpoints_1_3_3']}"
    )
    print("Protected SO(10) baseline imported: NO")
    print(f"Runtime: {time.time() - started:.3f}s")
    return {
        "single_levels": single_levels,
        "factorization": factorization,
        "remainder_statistics": statistics,
        "remainder_support": support,
        "shift_diagnostics": shifts,
        "a_tail_endpoints": a_tail,
        "all_checks": factorization["reconstructed"] == factorization["primaries"],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Factor the exact HFT symmetric-vector Regge tower"
    )
    parser.add_argument("--max-level", type=int, default=10)
    args = parser.parse_args(argv)
    try:
        result = run_analysis(max_level=args.max_level)
    except Exception as error:
        print(f"TK6B.5c FAILED: {error}", file=sys.stderr)
        return 1
    return 0 if result["all_checks"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
