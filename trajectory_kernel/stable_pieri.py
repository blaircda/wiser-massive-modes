"""TK6B.5d: stable ``B_n`` Pieri translation for the HFT Regge tower.

Let ``V_mu`` and ``V_lambda`` be arbitrary (tensorial or spinorial) type-B
irreducibles and let ``H_k = V_(k,0,...,0)`` be the harmonic one-row
representation.  Racah--Speiser gives the cutoff-independent identity

    [V_lambda : V_mu H_k]
      = [V_(lambda+omega_1) : V_mu H_(k+1)]

whenever the first orthogonal coordinate of ``lambda`` is at least that of
``mu``.  Summing the harmonic decomposition of ``Sym^R(V)`` gives the same
identity for consecutive symmetric powers.  The proof works on both weight
cosets and therefore does not require a chirality convention.

This module checks the identity independently in small exact character-ring
samples and audits its hypothesis irrep by irrep in the virtual HFT remainder.
It imports no protected SO(10) completion.
"""

import argparse
import sys
import time
from collections import Counter
from itertools import product

from sage.all import QQ

import hft_so9
from trajectory_kernel import chamber_audit
from trajectory_kernel import regge_columns
from trajectory_kernel import regge_factorization


B4 = hft_so9.B4


def first_orthogonal_coordinate(label):
    """Return the first orthogonal coordinate of a B4 Dynkin label."""
    if len(label) != 4 or min(label) < 0:
        raise ValueError(f"Expected a dominant B4 Dynkin label: {label}")
    ell, m, r, s = label
    return QQ(ell + m + r) + QQ(s) / 2


def ell_shift(label, steps=1):
    """Translate a B4 label by ``steps * omega_1``."""
    steps = int(steps)
    if steps < 0:
        raise ValueError("The stable Pieri translation uses nonnegative steps")
    ell, m, r, s = label
    return (ell + steps, m, r, s)


def stable_pieri_hypothesis(target_before_shift, remainder_label):
    """Test the exact Racah--Speiser stable-range inequality."""
    return (
        first_orthogonal_coordinate(target_before_shift)
        >= first_orthogonal_coordinate(remainder_label)
    )


def exterior_cost(label):
    """Return the GMSZ exterior-chamber cost attached to a B4 label."""
    ell, m, r, s = label
    return 2 * ell + 3 * m + chamber_audit.support_cost(r, s)


def _small_labels(maximum_sum):
    maximum_sum = int(maximum_sum)
    if maximum_sum < 0:
        raise ValueError("maximum_sum must be nonnegative")
    return tuple(
        label
        for label in product(range(maximum_sum + 1), repeat=4)
        if sum(label) <= maximum_sum
    )


def direct_stable_pieri_audit(maximum_sum=2, maximum_degree=4):
    """Check the theorem in a finite exact B4 character-ring sample.

    This is a regression test, not the proof.  The analytic proof is the
    Racah--Speiser stabilizer argument recorded in the accompanying report.
    """
    tested = 0
    failures = []
    parity_counts = Counter()
    for mu in _small_labels(maximum_sum):
        mu_character = B4(*mu)
        for degree in range(int(maximum_degree) + 1):
            before = regge_factorization.character_table(
                mu_character
                * regge_factorization.symmetric_vector_coefficient(degree)
            )
            after = regge_factorization.character_table(
                mu_character
                * regge_factorization.symmetric_vector_coefficient(degree + 1)
            )
            candidate_labels = set(before)
            candidate_labels.update(
                (label[0] - 1, label[1], label[2], label[3])
                for label in after
                if label[0] >= 1
            )
            for label in candidate_labels:
                if not stable_pieri_hypothesis(label, mu):
                    continue
                shifted = ell_shift(label)
                source_value = before.get(label, 0)
                target_value = after.get(shifted, 0)
                tested += 1
                parity_counts["spinorial" if mu[3] % 2 else "tensorial"] += 1
                if source_value != target_value:
                    failures.append(
                        {
                            "remainder_label": mu,
                            "symmetric_degree": degree,
                            "source_label": label,
                            "target_label": shifted,
                            "source_multiplicity": source_value,
                            "target_multiplicity": target_value,
                        }
                    )
    return {
        "tested": tested,
        "failures": tuple(failures),
        "parity_counts": dict(parity_counts),
        "all_match": not failures,
    }


def hft_contribution_stable_range_audit(single_levels, factorization, max_level):
    """Audit stable Pieri separately for every active HFT remainder irrep."""
    max_level = int(max_level)
    multiplicities = {
        level: regge_columns.extract_level_multiplicities(single_levels[level])
        for level in range(1, max_level + 1)
    }
    shifts = tuple(
        item
        for item in chamber_audit.audit_shifts(multiplicities, max_level)
        if item.family == "ell" and item.steps == 1
    )
    remainder_tables = {
        degree: regge_factorization.character_table(character)
        for degree, character in factorization["remainder"].items()
    }
    product_cache = {}

    def product_table(mu, degree):
        key = (mu, degree)
        if key not in product_cache:
            product_cache[key] = regge_factorization.character_table(
                B4(*mu)
                * regge_factorization.symmetric_vector_coefficient(degree)
            )
        return product_cache[key]

    active_records = []
    inactive_hypothesis_failures = 0
    for shift in shifts:
        target_degree = shift.target_level - 1
        source_degree = shift.source_level - 1
        if target_degree != source_degree + 1:
            raise ValueError("Expected an adjacent physical-level ell shift")
        for remainder_degree in range(target_degree + 1):
            for mu, coefficient in remainder_tables[remainder_degree].items():
                if remainder_degree == target_degree:
                    source_value = 0
                    target_value = int(mu == shift.target_label)
                    stable = False
                    top_boundary = True
                else:
                    symmetric_degree = source_degree - remainder_degree
                    source_value = product_table(mu, symmetric_degree).get(
                        shift.source_label, 0
                    )
                    target_value = product_table(mu, symmetric_degree + 1).get(
                        shift.target_label, 0
                    )
                    stable = stable_pieri_hypothesis(shift.source_label, mu)
                    top_boundary = False
                    if not stable and not (source_value or target_value):
                        inactive_hypothesis_failures += 1
                if not (source_value or target_value):
                    continue
                active_records.append(
                    {
                        "shift": shift,
                        "remainder_degree": remainder_degree,
                        "remainder_label": mu,
                        "remainder_coefficient": coefficient,
                        "source_multiplicity": source_value,
                        "target_multiplicity": target_value,
                        "stable_hypothesis": stable,
                        "top_boundary": top_boundary,
                        "matches": source_value == target_value,
                    }
                )

    uncovered = tuple(
        record
        for record in active_records
        if not record["stable_hypothesis"] and not record["top_boundary"]
    )
    top_boundary = tuple(
        record for record in active_records if record["top_boundary"]
    )
    failures = tuple(
        record for record in active_records if not record["matches"]
    )
    parity_counts = Counter(
        "spinorial" if record["remainder_label"][3] % 2 else "tensorial"
        for record in active_records
        if not record["top_boundary"]
    )
    signed_counts = Counter(
        "negative" if record["remainder_coefficient"] < 0 else "positive"
        for record in active_records
        if not record["top_boundary"]
    )
    return {
        "eligible_shifts": len(shifts),
        "active_records": tuple(active_records),
        "active_pairs": len(active_records),
        "stable_pairs": sum(
            record["stable_hypothesis"] for record in active_records
        ),
        "uncovered": uncovered,
        "top_boundary": top_boundary,
        "failures": failures,
        "inactive_hypothesis_failures": inactive_hypothesis_failures,
        "parity_counts": dict(parity_counts),
        "signed_counts": dict(signed_counts),
        "all_active_certified": not uncovered and not top_boundary and not failures,
    }


def unstable_coupling_energy_audit(factorization):
    """Test the candidate energy bound which excludes unstable chamber pairs.

    If ``lambda`` occurs in ``mu * Sym^R(V)`` but ``lambda_1 < mu_1``, the
    candidate bound is

        d + R >= 2 ell(lambda) + 3 m(lambda) + support_cost(r, s),

    where ``d`` is the virtual-remainder degree.  At the next series degree
    this puts ``lambda + omega_1`` outside the eligible GMSZ ell chamber.
    """
    remainder_tables = {
        degree: regge_factorization.character_table(character)
        for degree, character in factorization["remainder"].items()
    }
    maximum_degree = max(remainder_tables)
    product_cache = {}

    def product_table(mu, degree):
        key = (mu, degree)
        if key not in product_cache:
            product_cache[key] = regge_factorization.character_table(
                B4(*mu)
                * regge_factorization.symmetric_vector_coefficient(degree)
            )
        return product_cache[key]

    tested = 0
    unstable = 0
    failures = []
    minimum_margin = None
    for total_degree in range(maximum_degree + 1):
        for remainder_degree in range(total_degree + 1):
            symmetric_degree = total_degree - remainder_degree
            for mu in remainder_tables[remainder_degree]:
                for label, multiplicity in product_table(
                    mu, symmetric_degree
                ).items():
                    tested += 1
                    if stable_pieri_hypothesis(label, mu):
                        continue
                    unstable += 1
                    required = exterior_cost(label)
                    margin = total_degree - required
                    if minimum_margin is None or margin < minimum_margin:
                        minimum_margin = margin
                    if margin < 0:
                        failures.append(
                            {
                                "total_degree": total_degree,
                                "remainder_degree": remainder_degree,
                                "symmetric_degree": symmetric_degree,
                                "remainder_label": mu,
                                "target_before_shift": label,
                                "tensor_multiplicity": multiplicity,
                                "required_degree": required,
                                "margin": margin,
                            }
                        )
    return {
        "tested_product_terms": tested,
        "unstable_product_terms": unstable,
        "minimum_margin": minimum_margin,
        "failures": tuple(failures),
        "all_satisfy": not failures,
    }


def remainder_exterior_cost_audit(remainder):
    """Test the sharper observed HFT support bound ``E(mu) <= d + 1``."""
    records = []
    for degree, character in remainder.items():
        for label, coefficient in regge_factorization.character_table(
            character
        ).items():
            cost = exterior_cost(label)
            records.append(
                {
                    "degree": degree,
                    "label": label,
                    "coefficient": coefficient,
                    "cost": cost,
                    "margin": degree + 1 - cost,
                }
            )
    failures = tuple(record for record in records if record["margin"] < 0)
    return {
        "records": tuple(records),
        "tested": len(records),
        "minimum_margin": min(
            (record["margin"] for record in records), default=None
        ),
        "tight": sum(record["margin"] == 0 for record in records),
        "failures": failures,
        "all_satisfy": not failures,
    }


def generic_cost_counterexample():
    """Return an exact counterexample to a tempting generic cost inequality."""
    mu = (1, 0, 2, 1)
    degree = 3
    label = (0, 0, 0, 5)
    multiplicity = regge_factorization.character_table(
        B4(*mu) * regge_factorization.symmetric_vector_coefficient(degree)
    ).get(label, 0)
    return {
        "remainder_label": mu,
        "symmetric_degree": degree,
        "unstable_target": label,
        "multiplicity": multiplicity,
        "stable_hypothesis": stable_pieri_hypothesis(label, mu),
        "source_cost": exterior_cost(mu),
        "target_cost": exterior_cost(label),
        "generic_bound_rhs": exterior_cost(mu) + degree - 1,
        "is_counterexample": (
            multiplicity > 0
            and not stable_pieri_hypothesis(label, mu)
            and exterior_cost(label) > exterior_cost(mu) + degree - 1
        ),
    }


def remainder_plethystic_cost_audit(remainder, maximum_degree=8):
    """Test whether the exterior-cost bound holds on ``PL[Z'_m]`` itself."""
    from plethystic_series import plethystic_log

    maximum_degree = min(int(maximum_degree), max(remainder))
    truncated = {
        degree: remainder[degree]
        for degree in range(maximum_degree + 1)
    }
    plethystic = plethystic_log(truncated, maximum_degree)
    records = []
    for degree, character in plethystic.items():
        for label, coefficient in regge_factorization.character_table(
            character
        ).items():
            records.append(
                {
                    "degree": degree,
                    "label": label,
                    "coefficient": coefficient,
                    "cost": exterior_cost(label),
                    "margin": degree + 1 - exterior_cost(label),
                }
            )
    failures = tuple(record for record in records if record["margin"] < 0)
    return {
        "maximum_degree": maximum_degree,
        "tested": len(records),
        "minimum_margin": min(
            (record["margin"] for record in records), default=None
        ),
        "failures": failures,
        "all_satisfy": not failures,
    }


def run_analysis(max_level=10, plethystic_audit=False):
    """Run exact sample and HFT contribution-wise stable-range audits."""
    if max_level < chamber_audit.GMSZ_FIRST_LEVEL:
        raise ValueError("Use max_level >= 7 to enter the shift chamber")
    started = time.time()
    sample = direct_stable_pieri_audit()
    _numerator, single_levels = hft_so9.derive_hft_spectrum(max_level)
    factorization = regge_factorization.factor_symmetric_vector_tower(
        single_levels, max_level
    )
    hft_audit = hft_contribution_stable_range_audit(
        single_levels, factorization, max_level
    )
    energy = unstable_coupling_energy_audit(factorization)
    remainder_cost = remainder_exterior_cost_audit(factorization["remainder"])
    generic_counterexample = generic_cost_counterexample()
    plethystic = (
        remainder_plethystic_cost_audit(factorization["remainder"])
        if plethystic_audit
        else None
    )

    print("=" * 100)
    print("TK6B.5d — STABLE B4 PIERI TRANSLATION")
    print("=" * 100)
    print(f"Small exact theorem-regression cases: {sample['tested']}")
    print(f"Small-sample failures: {len(sample['failures'])}")
    print(f"Eligible adjacent HFT ell shifts: {hft_audit['eligible_shifts']}")
    print(f"Active irrep-by-irrep remainder pairs: {hft_audit['active_pairs']}")
    print(f"Stable-range active pairs: {hft_audit['stable_pairs']}")
    print(f"Active pairs outside theorem range: {len(hft_audit['uncovered'])}")
    print(f"Unpaired top-remainder contributions: {len(hft_audit['top_boundary'])}")
    print(f"Direct multiplicity failures: {len(hft_audit['failures'])}")
    print(f"Active parity sectors: {hft_audit['parity_counts']}")
    print(f"Active virtual signs: {hft_audit['signed_counts']}")
    print(f"Unstable product terms in energy audit: {energy['unstable_product_terms']}")
    print(f"Minimum unstable-coupling energy margin: {energy['minimum_margin']}")
    print(f"Unstable-coupling energy failures: {len(energy['failures'])}")
    print(
        "Remainder exterior-cost support failures: "
        f"{len(remainder_cost['failures'])}"
    )
    print(
        "Remainder exterior-cost minimum margin/tight terms: "
        f"{remainder_cost['minimum_margin']}/{remainder_cost['tight']}"
    )
    print(
        "Generic Pieri-cost shortcut has exact counterexample: "
        f"{generic_counterexample['is_counterexample']}"
    )
    if plethystic is not None:
        print(
            "Plethystic-log exterior-cost failures/minimum margin: "
            f"{len(plethystic['failures'])}/{plethystic['minimum_margin']}"
        )
    print("Protected SO(10) baseline imported: NO")
    print(f"Runtime: {time.time() - started:.3f}s")
    return {
        "sample": sample,
        "hft_audit": hft_audit,
        "energy_audit": energy,
        "remainder_cost_audit": remainder_cost,
        "generic_cost_counterexample": generic_counterexample,
        "plethystic_cost_audit": plethystic,
        "all_checks": (
            sample["all_match"]
            and hft_audit["all_active_certified"]
            and energy["all_satisfy"]
            and remainder_cost["all_satisfy"]
            and generic_counterexample["is_counterexample"]
            and (plethystic is None or not plethystic["all_satisfy"])
        ),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Audit the stable B4 Pieri translation in the HFT factorization"
    )
    parser.add_argument("--max-level", type=int, default=10)
    parser.add_argument(
        "--plethystic-audit",
        action="store_true",
        help="also test the exterior-cost bound on PL[Z'_m] through degree 8",
    )
    args = parser.parse_args(argv)
    try:
        result = run_analysis(
            max_level=args.max_level,
            plethystic_audit=args.plethystic_audit,
        )
    except Exception as error:
        print(f"TK6B.5d FAILED: {error}", file=sys.stderr)
        return 1
    return 0 if result["all_checks"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
