"""TK1: baseline-free extraction and analysis of HFT B4 Regge columns.

For a B4 irrep ``[ell,m,r,s]`` at mass level ``n``, a Regge shift sends

    (n, ell, m, r, s) -> (n+1, ell+1, m, r, s).

Equivalently, it fixes the column ``(m,r,s)`` and the HFT-reduced depth
``delta=n-ell-3m``. This module derives the HFT SO(9) characters without
protected SO(10) data, extracts all irreducible multiplicities, and tests that
shift including zero entries and new boundary states.
"""

import argparse
import sys
import time
from collections import Counter, defaultdict
from dataclasses import dataclass

from sage.all import ZZ

import hft_so9


@dataclass(frozen=True, order=True)
class ReggeColumn:
    """Fixed subleading labels ``(m,r,s)`` of a B4 weight ``[ell,m,r,s]``."""

    m: int
    r: int
    s: int

    def __post_init__(self):
        if min(self.m, self.r, self.s) < 0:
            raise ValueError(f"Regge-column labels must be nonnegative: {self}")


@dataclass(frozen=True, order=True)
class ReggeOrbit:
    """A shift orbit, fixed by reduced depth ``n-ell-3m`` and a column."""

    depth: int
    column: ReggeColumn

    def __post_init__(self):
        if self.depth < 0:
            raise ValueError(f"Regge depth must be nonnegative: {self.depth}")


@dataclass(frozen=True)
class ShiftComparison:
    """One adjacent comparison under ``(n,ell)->(n+1,ell+1)``."""

    level: int
    label: tuple
    multiplicity: int
    shifted_multiplicity: int

    @property
    def shifted_label(self):
        return regge_shift(self.label)

    @property
    def matches(self):
        return self.multiplicity == self.shifted_multiplicity


@dataclass(frozen=True)
class OrbitAnalysis:
    """Finite-window multiplicity sequence along one Regge-shift orbit."""

    orbit: ReggeOrbit
    sequence: tuple
    first_nonzero_level: int
    stable_start_level: int | None
    stable_value: int | None
    stable_run_length: int

    @property
    def stable_from_first_nonzero(self):
        return self.stable_start_level == self.first_nonzero_level


def split_b4_label(label):
    """Return ``(ell, ReggeColumn(m,r,s))`` for a B4 Dynkin-label tuple."""
    if len(label) != 4:
        raise ValueError(f"Expected four B4 Dynkin labels, received {label}")
    ell, m, r, s = (int(value) for value in label)
    if min(ell, m, r, s) < 0:
        raise ValueError(f"B4 Dynkin labels must be nonnegative: {label}")
    return ell, ReggeColumn(m, r, s)


def join_b4_label(ell, column):
    """Reconstruct ``[ell,m,r,s]`` from a leading label and column key."""
    if ell < 0:
        raise ValueError(f"Leading Regge label must be nonnegative: {ell}")
    return (int(ell), column.m, column.r, column.s)


def regge_shift(label, steps=1):
    """Apply ``ell -> ell + steps`` while keeping ``(m,r,s)`` fixed."""
    ell, column = split_b4_label(label)
    shifted_ell = ell + int(steps)
    return join_b4_label(shifted_ell, column)


def _exact_integer(value, description):
    """Convert an exact Sage integer, rejecting fractional multiplicities."""
    if value not in ZZ:
        raise ValueError(f"Non-integral {description}: {value}")
    return int(value)


def b4_weight_to_dynkin(weight):
    """Convert a B4 ambient highest weight to Dynkin labels ``[ell,m,r,s]``."""
    x1, x2, x3, x4 = weight.to_vector()
    return (
        _exact_integer(x1 - x2, "B4 label ell"),
        _exact_integer(x2 - x3, "B4 label m"),
        _exact_integer(x3 - x4, "B4 label r"),
        _exact_integer(2 * x4, "B4 label s"),
    )


def extract_level_multiplicities(character):
    """Return a sparse ``label -> nonnegative integer`` decomposition."""
    result = {}
    for weight, coefficient in character.monomial_coefficients().items():
        value = _exact_integer(coefficient, "B4 multiplicity")
        if value < 0:
            raise ValueError(f"HFT spectrum contains negative multiplicity {value}")
        if value:
            result[b4_weight_to_dynkin(weight)] = value
    return result


def derive_multiplicity_table(max_level):
    """Derive all ``r_n^9`` multiplicities through ``max_level`` from HFT."""
    _numerator, characters = hft_so9.derive_hft_spectrum(max_level)
    return {
        level: extract_level_multiplicities(characters[level])
        for level in range(1, max_level + 1)
    }


def group_by_column(multiplicities):
    """Group sparse entries by fixed ``(m,r,s)`` Regge column."""
    grouped = defaultdict(list)
    for level, level_data in multiplicities.items():
        for label, value in level_data.items():
            ell, column = split_b4_label(label)
            grouped[column].append((level, ell, value))
    return {
        column: tuple(sorted(entries))
        for column, entries in grouped.items()
    }


def compare_adjacent_shifts(multiplicities, max_level):
    """Compare all adjacent shift pairs, including implicit zero coefficients.

    New nonzero states at ``ell=0`` have no predecessor under a nonnegative
    Regge shift and are returned separately as boundary seeds.
    """
    comparisons = []
    boundary_seeds = []

    for level in range(1, max_level):
        current = multiplicities[level]
        following = multiplicities[level + 1]
        candidates = set(current)

        for shifted_label, value in following.items():
            ell, column = split_b4_label(shifted_label)
            if ell == 0:
                boundary_seeds.append((level + 1, shifted_label, value))
            else:
                candidates.add(join_b4_label(ell - 1, column))

        for label in sorted(candidates):
            comparisons.append(
                ShiftComparison(
                    level=level,
                    label=label,
                    multiplicity=current.get(label, 0),
                    shifted_multiplicity=following.get(regge_shift(label), 0),
                )
            )

    return tuple(comparisons), tuple(boundary_seeds)


def analyze_orbits(multiplicities, max_level, minimum_stable_run=2):
    """Analyze finite multiplicity sequences at fixed ``(depth,m,r,s)``.

    ``stable_start_level`` is the earliest nonzero point from which the observed
    suffix is constant, provided at least ``minimum_stable_run`` points are
    available. A finite constant suffix is evidence, not an all-orders proof.
    """
    observed_orbits = set()
    for level, level_data in multiplicities.items():
        for label in level_data:
            ell, column = split_b4_label(label)
            observed_orbits.add(ReggeOrbit(level - ell - 3 * column.m, column))

    analyses = []
    for orbit in sorted(observed_orbits):
        first_allowed_level = max(
            1, orbit.depth + 3 * orbit.column.m
        )
        sequence = []
        for level in range(first_allowed_level, max_level + 1):
            ell = level - orbit.depth - 3 * orbit.column.m
            label = join_b4_label(ell, orbit.column)
            sequence.append((level, ell, multiplicities[level].get(label, 0)))

        nonzero_levels = [level for level, _ell, value in sequence if value > 0]
        if not nonzero_levels:
            continue
        first_nonzero = nonzero_levels[0]

        stable_start = None
        stable_value = None
        stable_run_length = 0
        for index, (level, _ell, value) in enumerate(sequence):
            suffix = sequence[index:]
            if (
                value > 0
                and len(suffix) >= minimum_stable_run
                and all(item[2] == value for item in suffix)
            ):
                stable_start = level
                stable_value = value
                stable_run_length = len(suffix)
                break

        analyses.append(
            OrbitAnalysis(
                orbit=orbit,
                sequence=tuple(sequence),
                first_nonzero_level=first_nonzero,
                stable_start_level=stable_start,
                stable_value=stable_value,
                stable_run_length=stable_run_length,
            )
        )
    return tuple(analyses)


def summarize_tk1(max_level=10, verbose=False):
    """Run the complete baseline-free TK1 extraction and shift diagnostics."""
    started = time.time()
    multiplicities = derive_multiplicity_table(max_level)
    columns = group_by_column(multiplicities)
    comparisons, boundary_seeds = compare_adjacent_shifts(
        multiplicities, max_level
    )
    orbits = analyze_orbits(multiplicities, max_level)

    mismatches = tuple(item for item in comparisons if not item.matches)
    stable_from_first = tuple(item for item in orbits if item.stable_from_first_nonzero)
    delayed_stable = tuple(
        item
        for item in orbits
        if item.stable_start_level is not None and not item.stable_from_first_nonzero
    )
    unresolved = tuple(item for item in orbits if item.stable_start_level is None)
    stable = stable_from_first + delayed_stable
    delayed_activation = tuple(
        item
        for item in orbits
        if item.first_nonzero_level > item.sequence[0][0]
    )
    stable_run_at_least_three = tuple(
        item for item in stable if item.stable_run_length >= 3
    )
    unresolved_single_point = tuple(
        item for item in unresolved if len(item.sequence) == 1
    )
    mismatch_transitions = Counter(item.level for item in mismatches)
    seed_levels = Counter(level for level, _label, _value in boundary_seeds)

    print("=" * 104)
    print("TK1 — BASELINE-FREE HFT REGGE-COLUMN EXTRACTION")
    print("=" * 104)
    print(f"Levels derived: 1 through {max_level}")
    print(f"Nonzero spectrum entries: {sum(len(data) for data in multiplicities.values())}")
    print(f"Distinct fixed-(m,r,s) columns: {len(columns)}")
    print(f"Observed fixed-(depth,m,r,s) orbits: {len(orbits)}")
    print(f"Adjacent shift comparisons (including zeros): {len(comparisons)}")
    print(f"Exact adjacent matches: {len(comparisons) - len(mismatches)}")
    print(f"Adjacent mismatches: {len(mismatches)}")
    print(f"New ell=0 boundary seeds: {len(boundary_seeds)}")
    print(f"Orbits stable from first nonzero observation: {len(stable_from_first)}")
    print(f"Orbits with delayed observed stabilization: {len(delayed_stable)}")
    print(f"All orbits with an observed constant suffix: {len(stable)}")
    print(f"  of which have at least three observed terms: {len(stable_run_at_least_three)}")
    print(f"Orbits with delayed activation after their kinematic start: {len(delayed_activation)}")
    print(f"Orbits unresolved by the finite window: {len(unresolved)}")
    print(f"  of which have only one available point: {len(unresolved_single_point)}")

    if mismatches:
        print("\nAdjacent mismatch counts by transition n -> n+1:")
        print("  " + ", ".join(
            f"{level}->{level + 1}: {count}"
            for level, count in sorted(mismatch_transitions.items())
        ))

    if boundary_seeds:
        print("\nNew ell=0 boundary-seed counts by level:")
        print("  " + ", ".join(
            f"n={level}: {count}"
            for level, count in sorted(seed_levels.items())
        ))

    if verbose:
        if mismatches:
            print("\nAdjacent shift mismatches:")
            for item in mismatches:
                print(
                    f"  n={item.level}, {item.label} mult={item.multiplicity} -> "
                    f"n={item.level + 1}, {item.shifted_label} "
                    f"mult={item.shifted_multiplicity}"
                )

        if boundary_seeds:
            print("\nNew ell=0 boundary seeds:")
            for level, label, value in boundary_seeds:
                print(f"  n={level}, {label}, multiplicity={value}")

        print("\nOrbit sequences:")
        for item in orbits:
            status = (
                f"stable from n={item.stable_start_level} at {item.stable_value}"
                if item.stable_start_level is not None
                else "unresolved"
            )
            print(
                f"  depth={item.orbit.depth}, column={item.orbit.column}: "
                f"{item.sequence} [{status}]"
            )

    print("-" * 104)
    print("Protected SO(10) baseline imported: NO")
    print("Finite-window stability is reported as evidence, not an all-orders theorem.")
    print(f"Elapsed: {time.time() - started:.3f}s")
    return {
        "multiplicities": multiplicities,
        "columns": columns,
        "comparisons": comparisons,
        "boundary_seeds": boundary_seeds,
        "orbits": orbits,
        "mismatches": mismatches,
        "stable_from_first": stable_from_first,
        "delayed_stable": delayed_stable,
        "stable": stable,
        "stable_run_at_least_three": stable_run_at_least_three,
        "delayed_activation": delayed_activation,
        "unresolved": unresolved,
        "unresolved_single_point": unresolved_single_point,
    }


def run_self_test():
    """Check the package's Regge-column conventions."""
    label = (3, 2, 1, 4)
    ell, column = split_b4_label(label)
    checks = (
        ell == 3,
        column == ReggeColumn(2, 1, 4),
        join_b4_label(ell, column) == label,
        regge_shift(label) == (4, 2, 1, 4),
        regge_shift(label, 3) == (6, 2, 1, 4),
        ReggeOrbit(4, column).depth == 4,
    )
    passed = all(checks)
    print("TRAJECTORY-KERNEL TK0 SELF-TEST")
    print(f"Regge-column label and shift primitives: {'PASS' if passed else 'FAIL'}")
    print("Protected SO(10) baseline imported: NO")
    return passed


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Regge-column extraction utilities")
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run the TK0 label-convention check",
    )
    parser.add_argument("--max-level", type=int, default=10)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        raise SystemExit(0 if run_self_test() else 1)
    summarize_tk1(args.max_level, args.verbose)
    raise SystemExit(0)
