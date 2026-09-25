"""TK5a: audit the GMSZ support chambers and multiplicity shifts.

Georgoudis--Minahan--Strom--Zoumis (arXiv:2609.04107) propose an
empirical description of the support of the massive B4 character and three
families of multiplicity shifts.  This module encodes their equations
(3.6) and (3.32)--(3.35) literally and compares them with the spectrum
derived independently from ``hft_so9.py``.

The published support rule is stated only for levels n > 6.  Results at
levels 1--6 are therefore reported as out-of-domain diagnostics, never as
counterexamples.  No protected SO(10) completion is imported.
"""

import argparse
import time
from collections import Counter
from dataclasses import dataclass

from trajectory_kernel import regge_columns


GMSZ_FIRST_LEVEL = 7


@dataclass(frozen=True)
class SupportAudit:
    """Comparison of predicted and observed nonzero B4 support at one level."""

    level: int
    predicted: frozenset
    observed: frozenset

    @property
    def missing(self):
        return self.predicted - self.observed

    @property
    def unexpected(self):
        return self.observed - self.predicted

    @property
    def exact(self):
        return not self.missing and not self.unexpected


@dataclass(frozen=True)
class ShiftAudit:
    """One admissible GMSZ multiplicity-shift comparison."""

    family: str
    target_level: int
    target_label: tuple
    source_level: int
    source_label: tuple
    steps: int
    ell_max: int
    target_multiplicity: int
    source_multiplicity: int

    @property
    def matches(self):
        return self.target_multiplicity == self.source_multiplicity


def support_cost(r, s):
    """Minimum reduced level from the four inequalities in GMSZ (3.6)."""
    r = int(r)
    s = int(s)
    if r < 0 or s < 0:
        raise ValueError("GMSZ support labels must be nonnegative")
    return max(
        6 * r + 5 * s - 6,
        6 * r + 4 * s - 2,
        6 * r + 3 * s - 1,
        2 * s + 1,
    )


def ell_max(level, m, r, s):
    """Largest leading label allowed by GMSZ (3.6), before the one gap."""
    values = (level, m, r, s)
    if min(values) < 0:
        raise ValueError(f"Level and Dynkin labels must be nonnegative: {values}")
    return int(level) - 3 * int(m) - support_cost(r, s)


def exceptional_gap(level):
    """The isolated representation excluded from the support polytope."""
    return (int(level) - 2, 0, 0, 0)


def predicted_support(level):
    """Return the finite support predicted by GMSZ (3.6) at one level.

    The formula can be evaluated at any positive level, but the paper claims
    it only for ``level > 6``.
    """
    level = int(level)
    if level < 1:
        raise ValueError("String level must be positive")

    result = set()
    # If 3m exceeds n+6 then even the weakest first inequality fails.
    for m in range((level + 6) // 3 + 1):
        # The first inequality bounds r and the fourth bounds s.
        for r in range((level + 12) // 6 + 1):
            for s in range((level + 7) // 2 + 1):
                maximum = ell_max(level, m, r, s)
                if maximum < 0:
                    continue
                for ell in range(maximum + 1):
                    label = (ell, m, r, s)
                    if label != exceptional_gap(level):
                        result.add(label)
    return frozenset(result)


def audit_support(multiplicities, max_level):
    """Compare the GMSZ support polytope with the HFT-derived support."""
    return tuple(
        SupportAudit(
            level=level,
            predicted=predicted_support(level),
            observed=frozenset(multiplicities[level]),
        )
        for level in range(1, max_level + 1)
    )


def epsilon(s):
    """The piecewise spinor-label correction in GMSZ equation (3.35)."""
    s = int(s)
    if s < 0:
        raise ValueError("Spinor Dynkin label must be nonnegative")
    if s == 0:
        return 2
    if s <= 3:
        return 1
    return 0


def _source(family, level, label, steps):
    """Return the lower-level label for one published shift family."""
    ell, m, r, s = label
    if family == "ell":
        return level - steps, (ell - steps, m, r, s)
    if family == "m":
        return level - 3 * steps, (ell, m - steps, r, s)
    if family == "r":
        return level - 6 * steps, (ell, m, r - steps, s)
    raise ValueError(f"Unknown GMSZ shift family: {family}")


def _eligible(family, label, steps, maximum):
    """Apply equations (3.32)--(3.35) to a target representation."""
    ell, m, r, s = label
    if family == "ell":
        return ell > maximum // 2 + steps // 2
    if family == "m":
        return ell > maximum - m + steps - 1
    if family == "r":
        return ell > maximum - r + (steps - 1) + epsilon(s)
    raise ValueError(f"Unknown GMSZ shift family: {family}")


def audit_shifts(multiplicities, max_level):
    """Test every admissible published shift relation in the finite window.

    A relation is admissible only when its target has nonzero HFT
    multiplicity, the target lies in the claimed ``n > 6`` range, and the
    shifted label is present at the indicated lower level, as required in the
    paper.  Every positive shift size satisfying these conditions is tested;
    the paper's optional largest-k evaluation shortcut is not imposed.
    """
    results = []
    for level in range(GMSZ_FIRST_LEVEL, max_level + 1):
        for label, target_multiplicity in sorted(multiplicities[level].items()):
            ell, m, r, s = label
            maximum = ell_max(level, m, r, s)
            step_limits = {"ell": ell, "m": m, "r": r}
            for family in ("ell", "m", "r"):
                for steps in range(1, step_limits[family] + 1):
                    source_level, source_label = _source(
                        family, level, label, steps
                    )
                    if source_level < 1:
                        continue
                    source_multiplicity = multiplicities[source_level].get(
                        source_label
                    )
                    if source_multiplicity is None:
                        continue
                    if not _eligible(family, label, steps, maximum):
                        continue
                    results.append(
                        ShiftAudit(
                            family=family,
                            target_level=level,
                            target_label=label,
                            source_level=source_level,
                            source_label=source_label,
                            steps=steps,
                            ell_max=maximum,
                            target_multiplicity=target_multiplicity,
                            source_multiplicity=source_multiplicity,
                        )
                    )
    return tuple(results)


def summarize_tk5a(max_level=11, verbose=False):
    """Run the complete baseline-free support and shift audit."""
    if max_level < GMSZ_FIRST_LEVEL:
        raise ValueError("TK5a needs max_level >= 7 to enter the claimed chamber")

    started = time.time()
    multiplicities = regge_columns.derive_multiplicity_table(max_level)
    support = audit_support(multiplicities, max_level)
    shifts = audit_shifts(multiplicities, max_level)

    claimed_support = tuple(
        item for item in support if item.level >= GMSZ_FIRST_LEVEL
    )
    early_support = tuple(
        item for item in support if item.level < GMSZ_FIRST_LEVEL
    )
    support_failures = tuple(item for item in claimed_support if not item.exact)
    shift_failures = tuple(item for item in shifts if not item.matches)
    shift_family_counts = Counter(item.family for item in shifts)
    shift_family_failures = Counter(item.family for item in shift_failures)
    shift_step_counts = Counter((item.family, item.steps) for item in shifts)
    shift_level_counts = Counter(item.target_level for item in shifts)
    shift_level_failures = Counter(item.target_level for item in shift_failures)

    # Relate the chambered ell shift directly to TK1's unrestricted adjacent
    # comparisons, including implicit zeros.
    adjacent, _boundary = regge_columns.compare_adjacent_shifts(
        multiplicities, max_level
    )
    claimed_adjacent = tuple(
        item for item in adjacent if item.level + 1 >= GMSZ_FIRST_LEVEL
    )
    unrestricted_failures = tuple(
        item for item in claimed_adjacent if not item.matches
    )
    eligible_ell_pairs = {
        (item.source_level, item.source_label, item.target_level, item.target_label)
        for item in shifts
        if item.family == "ell" and item.steps == 1
    }
    chambered_adjacent = tuple(
        item
        for item in claimed_adjacent
        if (
            item.level,
            item.label,
            item.level + 1,
            item.shifted_label,
        )
        in eligible_ell_pairs
    )
    chambered_adjacent_failures = tuple(
        item for item in chambered_adjacent if not item.matches
    )
    chambered_adjacent_keys = {
        (item.level, item.label, item.level + 1, item.shifted_label)
        for item in chambered_adjacent
    }
    outside_adjacent = tuple(
        item
        for item in claimed_adjacent
        if (item.level, item.label, item.level + 1, item.shifted_label)
        not in chambered_adjacent_keys
    )
    outside_adjacent_failures = tuple(
        item for item in outside_adjacent if not item.matches
    )

    print("=" * 104)
    print("TK5a — GMSZ CHAMBER SUPPORT AND SHIFT AUDIT (BASELINE-FREE)")
    print("=" * 104)
    print(f"HFT levels derived: 1 through {max_level}")
    print("Published support domain: n > 6")
    print("\nSupport comparison in the claimed domain:")
    print("  level | predicted | observed | missing | unexpected | exact")
    for item in claimed_support:
        print(
            f"  {item.level:5d} | {len(item.predicted):9d} | "
            f"{len(item.observed):8d} | {len(item.missing):7d} | "
            f"{len(item.unexpected):10d} | {item.exact}"
        )
    print(f"Claimed-domain support failures: {len(support_failures)}")

    print("\nOut-of-domain levels 1--6 (diagnostic only):")
    for item in early_support:
        print(
            f"  n={item.level}: predicted={len(item.predicted)}, "
            f"observed={len(item.observed)}, missing={len(item.missing)}, "
            f"unexpected={len(item.unexpected)}"
        )

    print("\nAdmissible multiplicity-shift relations:")
    for family in ("ell", "m", "r"):
        steps = ", ".join(
            f"k={step}: {count}"
            for (name, step), count in sorted(shift_step_counts.items())
            if name == family
        ) or "none"
        print(
            f"  {family:>3}: tested={shift_family_counts[family]}, "
            f"failures={shift_family_failures[family]} ({steps})"
        )
    print(f"  all: tested={len(shifts)}, failures={len(shift_failures)}")
    print("  by target level: " + ", ".join(
        f"n={level}: {shift_level_counts[level]} tested/"
        f"{shift_level_failures[level]} failed"
        for level in range(GMSZ_FIRST_LEVEL, max_level + 1)
    ))

    print("\nRelation to unrestricted TK1 adjacent Regge comparisons:")
    print(f"  Comparisons with target n >= 7: {len(claimed_adjacent)}")
    print(f"  Unrestricted mismatches: {len(unrestricted_failures)}")
    print(f"  Pairs satisfying the GMSZ ell chamber: {len(chambered_adjacent)}")
    print(f"  Mismatches inside that chamber: {len(chambered_adjacent_failures)}")
    print(
        f"  Pairs outside that chamber: {len(outside_adjacent)} "
        f"({len(outside_adjacent_failures)} mismatches)"
    )

    if verbose:
        if support_failures:
            print("\nSupport failures in the claimed domain:")
            for item in support_failures:
                print(f"  n={item.level}, missing={sorted(item.missing)}")
                print(f"       unexpected={sorted(item.unexpected)}")
        print("\nOut-of-domain missing labels (not claimed counterexamples):")
        for item in early_support:
            if item.missing or item.unexpected:
                print(
                    f"  n={item.level}, missing={sorted(item.missing)}, "
                    f"unexpected={sorted(item.unexpected)}"
                )
        if shift_failures:
            print("\nShift failures:")
            for item in shift_failures:
                print(
                    f"  {item.family}, k={item.steps}: "
                    f"n={item.source_level} {item.source_label} "
                    f"mult={item.source_multiplicity} -> "
                    f"n={item.target_level} {item.target_label} "
                    f"mult={item.target_multiplicity}, "
                    f"ell_max={item.ell_max}"
                )

    print("-" * 104)
    print("Protected SO(10) baseline imported: NO")
    print("The audited GMSZ statements remain empirical; finite agreement is not a proof.")
    print(f"Elapsed: {time.time() - started:.3f}s")
    return {
        "multiplicities": multiplicities,
        "support": support,
        "claimed_support": claimed_support,
        "early_support": early_support,
        "support_failures": support_failures,
        "shifts": shifts,
        "shift_failures": shift_failures,
        "shift_family_counts": shift_family_counts,
        "shift_family_failures": shift_family_failures,
        "shift_step_counts": shift_step_counts,
        "shift_level_counts": shift_level_counts,
        "shift_level_failures": shift_level_failures,
        "claimed_adjacent": claimed_adjacent,
        "unrestricted_failures": unrestricted_failures,
        "chambered_adjacent": chambered_adjacent,
        "chambered_adjacent_failures": chambered_adjacent_failures,
        "outside_adjacent": outside_adjacent,
        "outside_adjacent_failures": outside_adjacent_failures,
    }


def run_self_test():
    """Check the published inequalities and shift conventions without HFT."""
    support_7 = predicted_support(7)
    checks = (
        len(support_7) == 23,
        (6, 0, 0, 0) in support_7,
        exceptional_gap(7) not in support_7,
        (0, 0, 2, 0) not in predicted_support(10),
        (0, 0, 2, 0) in predicted_support(11),
        ell_max(11, 0, 2, 0) == 0,
        epsilon(0) == 2,
        epsilon(2) == 1,
        epsilon(4) == 0,
        _source("ell", 9, (5, 1, 0, 0), 2)
        == (7, (3, 1, 0, 0)),
        _source("m", 9, (1, 2, 0, 0), 2)
        == (3, (1, 0, 0, 0)),
        _source("r", 11, (0, 0, 2, 0), 1)
        == (5, (0, 0, 1, 0)),
    )
    passed = all(checks)
    print("TK5a GMSZ CHAMBER SELF-TEST")
    print(f"Support and shift conventions: {'PASS' if passed else 'FAIL'}")
    print("Protected SO(10) baseline imported: NO")
    return passed


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Audit the GMSZ support chambers and multiplicity shifts"
    )
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--max-level", type=int, default=11)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        raise SystemExit(0 if run_self_test() else 1)
    summarize_tk5a(args.max_level, args.verbose)
    raise SystemExit(0)
