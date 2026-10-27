"""Explicit cumulative ``D5`` lift from the HFT Regge factorization.

Write the massive-primary ``B4`` series in the exact HFT form

    Z_m(q) = PE(q V_9) F(q).

The Bars III.B cumulative series is ``Z_m(q)/(1-q)``.  Since the defining
``D5`` vector restricts as ``V_10 -> 1 + V_9``, one has the formal identity

    Z_m(q)/(1-q) = Res(PE(q V_10)) F(q).

Thus every coefficientwise virtual lift ``F_tilde`` of ``F`` gives an exact
virtual cumulative lift

    X(q) = PE(q V_10) F_tilde(q).

This module tests whether natural, cutoff-independent triangular sections of
``D5 -> B4`` make the coefficients of ``X`` positive.  It imports no
protected ``SO(10)`` completion.  Failure is reported as an obstruction; no
ground-truth correction is inserted.
"""

import argparse
import sys
import time
from itertools import product

from sage.all import QQ, ZZ

import finite_cross_section as cross
import hft_so9
from trajectory_kernel import regge_factorization


D5 = cross.D5
B4 = hft_so9.B4

J_CHARACTER = D5(0, 0, 0, 1, 0) - D5(0, 0, 0, 0, 1)
CHIRALITY_REPAIR = -J_CHARACTER
A0_CHARACTER = (
    D5(0, 0, 0, 1, 1)
    - D5(0, 0, 0, 0, 2)
    - D5(0, 0, 1, 0, 0)
    + D5(0, 1, 0, 0, 0)
    - D5(1, 0, 0, 0, 0)
    + D5(0, 0, 0, 0, 0)
)


def d5_weight_to_dynkin(weight):
    """Convert one ambient ``D5`` highest weight to integral Dynkin labels."""
    x1, x2, x3, x4, x5 = weight.to_vector()
    labels = (x1 - x2, x2 - x3, x3 - x4, x4 - x5, x4 + x5)
    if any(value not in ZZ for value in labels):
        raise ValueError(f"Nonintegral D5 Dynkin label from {weight}")
    return tuple(int(value) for value in labels)


def d5_character_table(character):
    """Return the signed irreducible table of a ``D5`` character."""
    return {
        d5_weight_to_dynkin(weight): int(coefficient)
        for weight, coefficient in character.monomial_coefficients().items()
        if coefficient
    }


def symmetric_d5_vector_coefficient(degree):
    """Return ``Sym^degree(V_10)`` as a sum of traceless harmonics."""
    degree = int(degree)
    if degree < 0:
        return D5(0)
    return sum(
        (
            D5(degree - 2 * trace, 0, 0, 0, 0)
            for trace in range(degree // 2 + 1)
        ),
        D5(0),
    )


def symmetric_tower_restriction_audit(maximum_degree):
    """Check ``Res Sym^N(V10)=sum_{j<=N} Sym^j(V9)`` exactly."""
    records = []
    running_b4 = B4(0)
    for degree in range(int(maximum_degree) + 1):
        running_b4 += regge_factorization.symmetric_vector_coefficient(degree)
        restricted = symmetric_d5_vector_coefficient(degree).branch(
            B4, rule="default"
        )
        records.append(
            {
                "degree": degree,
                "exact": restricted == running_b4,
            }
        )
    return {
        "records": tuple(records),
        "all_exact": all(record["exact"] for record in records),
    }


def first_d5_orthogonal_coordinate(label):
    """Return the first orthogonal coordinate of a dominant ``D5`` label."""
    first, second, third, spin_minus, spin_plus = map(int, label)
    return QQ(first + second + third) + QQ(spin_minus + spin_plus) / 2


def d5_stable_pieri_audit(maximum_label_sum=1, maximum_degree=3):
    """Check a small exact sample of the analytic ``D_n`` translation theorem."""
    records = []
    failures = []
    labels = tuple(
        label
        for label in product(range(int(maximum_label_sum) + 1), repeat=5)
        if sum(label) <= int(maximum_label_sum)
    )
    for source in labels:
        source_first = first_d5_orthogonal_coordinate(source)
        source_character = D5(*source)
        for degree in range(int(maximum_degree) + 1):
            before = d5_character_table(
                source_character * D5(degree, 0, 0, 0, 0)
            )
            after = d5_character_table(
                source_character * D5(degree + 1, 0, 0, 0, 0)
            )
            for target, multiplicity in before.items():
                if first_d5_orthogonal_coordinate(target) < source_first:
                    continue
                shifted = (target[0] + 1,) + target[1:]
                record = {
                    "source": source,
                    "degree": degree,
                    "target": target,
                    "multiplicity": multiplicity,
                    "shifted_multiplicity": after.get(shifted, 0),
                }
                records.append(record)
                if multiplicity != record["shifted_multiplicity"]:
                    failures.append(record)
    return {
        "records": tuple(records),
        "tested": len(records),
        "failures": tuple(failures),
        "all_exact": not failures,
    }


def a0_scalar_response_audit(maximum_degree):
    """Check ``[1](Sym^k(V10) A0)=(-1)^k`` exactly."""
    records = []
    for degree in range(int(maximum_degree) + 1):
        scalar = d5_character_table(
            symmetric_d5_vector_coefficient(degree) * A0_CHARACTER
        ).get((0, 0, 0, 0, 0), 0)
        records.append(
            {
                "degree": degree,
                "scalar": scalar,
                "expected": (-1) ** degree,
            }
        )
    return {
        "records": tuple(records),
        "all_exact": all(
            record["scalar"] == record["expected"] for record in records
        ),
    }


def lift_remainder_coefficients(remainder, policy):
    """Lift every virtual remainder coefficient on one fixed triangular section."""
    records = {}
    for degree, character in sorted(remainder.items()):
        inversion = cross.invert_on_cross_section(character, policy=policy)
        if not inversion["exact"] or not inversion["integral"]:
            raise ValueError(
                f"Remainder section failed at degree {degree} under {policy}"
            )
        records[degree] = {
            "lift": inversion["lift"],
            "coefficients": {
                parent: int(value)
                for parent, value in inversion["coefficients"].items()
                if value
            },
            "positive": inversion["positive"],
        }
    return records


def convolve_cumulative_lift(remainder_lifts, maximum_degree):
    """Form ``PE(q V10) F_tilde(q)`` through one finite degree."""
    symmetric = {
        degree: symmetric_d5_vector_coefficient(degree)
        for degree in range(int(maximum_degree) + 1)
    }
    coefficients = {}
    for degree in range(int(maximum_degree) + 1):
        coefficients[degree] = sum(
            (
                symmetric[degree - remainder_degree]
                * remainder_lifts[remainder_degree]["lift"]
                for remainder_degree in range(degree + 1)
            ),
            D5(0),
        )
    return coefficients


def cumulative_coefficient(remainder_lifts, degree, symmetric=None):
    """Return one coefficient of ``PE(q V10) F_tilde`` exactly."""
    degree = int(degree)
    if symmetric is None:
        symmetric = {
            index: symmetric_d5_vector_coefficient(index)
            for index in range(degree + 1)
        }
    return sum(
        (
            symmetric[degree - remainder_degree]
            * remainder_lifts[remainder_degree]["lift"]
            for remainder_degree in range(degree + 1)
        ),
        D5(0),
    )


def nonnegative_seed_interval(character, seed):
    """Return all nonnegative integers ``t`` for which ``character+t*seed>=0``.

    The result is a closed integer interval, possibly with no finite upper
    endpoint.  A negative coefficient in a coordinate untouched by ``seed``
    is returned as an exact obstruction.
    """
    table = d5_character_table(character)
    seed_table = d5_character_table(seed)
    lower = 0
    upper = None
    untouched_negative = {}
    for label in set(table) | set(seed_table):
        value = int(table.get(label, 0))
        slope = int(seed_table.get(label, 0))
        if slope > 0:
            lower = max(lower, (-value + slope - 1) // slope)
        elif slope < 0:
            bound = value // (-slope)
            upper = bound if upper is None else min(upper, bound)
        elif value < 0:
            untouched_negative[label] = value
    feasible = not untouched_negative and (upper is None or lower <= upper)
    return {
        "lower": lower,
        "upper": upper,
        "untouched_negative": untouched_negative,
        "feasible": feasible,
    }


def diagonal_section_series(remainder_lifts, maximum_degree):
    """Return ``C_N=sum_{d+ell=N} [ell,0,0,0,0] S(F_d)``.

    Only one-row ``D5`` irreps can pair with a constituent of a symmetric
    vector power to produce a scalar.  This diagonal series therefore
    controls the scalar coefficient of the full Regge convolution.
    """
    maximum_degree = int(maximum_degree)
    coefficients = [0] * (maximum_degree + 1)
    for degree, record in remainder_lifts.items():
        for parent, value in record["coefficients"].items():
            ell, middle, rank_three, spin_minus, spin_plus = parent
            if (middle, rank_three, spin_minus, spin_plus) != (0, 0, 0, 0):
                continue
            total_degree = int(degree) + int(ell)
            if total_degree <= maximum_degree:
                coefficients[total_degree] += int(value)
    return tuple(coefficients)


def one_row_chiral_coordinate(multiplicities, ell):
    """Evaluate the six surviving Möbius terms at ``(ell,0,0,0)``."""
    ell = int(ell)
    if ell < 0:
        return 0
    value = int(multiplicities.get((ell, 0, 0, 0), 0))
    value -= int(multiplicities.get((ell + 1, 0, 0, 0), 0))
    value += int(multiplicities.get((ell, 1, 0, 0), 0))
    value -= int(multiplicities.get((ell, 0, 1, 0), 0))
    if ell >= 1:
        value -= int(multiplicities.get((ell - 1, 1, 0, 0), 0))
        value += int(multiplicities.get((ell - 1, 0, 1, 0), 0))
    return value


def diagonal_hft_mobius_series(remainder, maximum_degree):
    """Compute the one-row diagonal directly from six HFT multiplicity rays."""
    maximum_degree = int(maximum_degree)
    coefficients = [0] * (maximum_degree + 1)
    for degree, character in remainder.items():
        table = regge_factorization.character_table(character)
        maximum_ell = maximum_degree - int(degree)
        for ell in range(maximum_ell + 1):
            coefficients[int(degree) + ell] += one_row_chiral_coordinate(
                table, ell
            )
    return tuple(coefficients)


def scalar_regge_series_from_diagonal(diagonal):
    """Apply ``1/(1-q^2)`` to the one-row diagonal series."""
    diagonal = tuple(map(int, diagonal))
    return tuple(
        sum(diagonal[degree - 2 * trace] for trace in range(degree // 2 + 1))
        for degree in range(len(diagonal))
    )


def scalar_series_diagnostics(remainder, remainder_lifts, uplift, corrections):
    """Verify the exact scalar reduction and the inferred ``A0`` source tail."""
    maximum_degree = max(uplift)
    diagonal = diagonal_section_series(remainder_lifts, maximum_degree)
    mobius_diagonal = diagonal_hft_mobius_series(
        remainder, maximum_degree
    )
    predicted = scalar_regge_series_from_diagonal(diagonal)
    observed = tuple(
        d5_character_table(uplift[degree]).get((0, 0, 0, 0, 0), 0)
        for degree in range(maximum_degree + 1)
    )
    a0_corrections = {
        degree: coefficient
        for degree, (name, coefficient) in corrections.items()
        if name == "A0"
    }
    inferred = {}
    if a0_corrections:
        first = min(a0_corrections)
        for degree in range(first, maximum_degree + 1):
            inferred[degree] = -(
                predicted[degree]
                + (predicted[degree - 1] if degree > first else 0)
            )
    return {
        "diagonal": diagonal,
        "mobius_diagonal": mobius_diagonal,
        "mobius_diagonal_identity": diagonal == mobius_diagonal,
        "predicted_scalar": predicted,
        "observed_scalar": observed,
        "scalar_identity": predicted == observed,
        "a0_corrections": a0_corrections,
        "inferred_a0_corrections": inferred,
        "a0_from_scalar_tail": a0_corrections == inferred,
    }


def two_seed_recursive_correction(remainder_lifts, maximum_degree):
    """Try the smallest observed kernel recursion: one ``J`` seed, then ``A0``.

    At degree three the unique nonnegative multiple of ``J`` repairing the
    first chirality defect is selected.  At every later degree the smallest
    nonnegative multiple of the fixed six-term shell ``A0`` is selected that
    makes the current cumulative coefficient positive.  Earlier choices are
    never revised.  Failure returns the exact incompatible coefficient or
    interval rather than adding another seed family silently.
    """
    maximum_degree = int(maximum_degree)
    lifted = {
        degree: dict(record)
        for degree, record in remainder_lifts.items()
    }
    symmetric = {
        degree: symmetric_d5_vector_coefficient(degree)
        for degree in range(maximum_degree + 1)
    }
    corrections = {}
    records = []
    failure = None
    for degree in range(maximum_degree + 1):
        before = cumulative_coefficient(lifted, degree, symmetric=symmetric)
        seed_name = "-J" if degree == 3 else "A0"
        seed = CHIRALITY_REPAIR if degree == 3 else A0_CHARACTER
        interval = nonnegative_seed_interval(before, seed)
        if not interval["feasible"]:
            failure = {
                "degree": degree,
                "level": degree + 1,
                "seed": seed_name,
                "interval": interval,
                "negative_before": {
                    label: value
                    for label, value in d5_character_table(before).items()
                    if value < 0
                },
            }
            break
        coefficient = int(interval["lower"])
        if coefficient:
            lifted[degree]["lift"] += coefficient * seed
            corrections[degree] = (seed_name, coefficient)
        after = before + coefficient * seed
        table = d5_character_table(after)
        records.append(
            {
                "degree": degree,
                "level": degree + 1,
                "seed": seed_name,
                "coefficient": coefficient,
                "interval": interval,
                "minimum": min(table.values(), default=0),
                "positive": all(value >= 0 for value in table.values()),
            }
        )
    return {
        "remainder_lifts": lifted,
        "corrections": corrections,
        "records": tuple(records),
        "failure": failure,
        "completed": failure is None and len(records) == maximum_degree + 1,
        "all_positive": failure is None
        and all(record["positive"] for record in records),
    }


def cumulative_targets(single_levels, max_level):
    """Return Bars' cumulative ``B4`` targets through ``max_level``."""
    targets = {}
    running = B4(0)
    for level in range(1, int(max_level) + 1):
        running += single_levels[level]
        targets[level] = running
    return targets


def policy_diagnostics(single_levels, factorization, max_level, policy):
    """Construct and test one explicit cumulative uplift policy."""
    maximum_degree = int(max_level) - 1
    remainder_lifts = lift_remainder_coefficients(
        factorization["remainder"], policy
    )
    uplift = convolve_cumulative_lift(remainder_lifts, maximum_degree)
    targets = cumulative_targets(single_levels, max_level)
    records = []
    for degree in range(maximum_degree + 1):
        level = degree + 1
        table = d5_character_table(uplift[degree])
        negative = {
            label: value for label, value in table.items() if value < 0
        }
        branch_exact = (
            uplift[degree].branch(B4, rule="default") == targets[level]
        )
        records.append(
            {
                "level": level,
                "degree": degree,
                "terms": len(table),
                "minimum": min(table.values(), default=0),
                "negative_terms": negative,
                "positive": not negative,
                "branch_exact": branch_exact,
            }
        )
    recursive = two_seed_recursive_correction(
        remainder_lifts, maximum_degree
    )
    scalar = scalar_series_diagnostics(
        factorization["remainder"],
        remainder_lifts,
        uplift,
        recursive["corrections"],
    )
    corrected_branch_exact = False
    if recursive["completed"]:
        corrected_branch_exact = all(
            cumulative_coefficient(
                recursive["remainder_lifts"], degree
            ).branch(B4, rule="default") == targets[degree + 1]
            for degree in range(maximum_degree + 1)
        )
    return {
        "policy": policy,
        "remainder_lifts": remainder_lifts,
        "uplift": uplift,
        "records": tuple(records),
        "all_branch_exact": all(record["branch_exact"] for record in records),
        "all_positive": all(record["positive"] for record in records),
        "first_failure": next(
            (record for record in records if not record["positive"]), None
        ),
        "recursive_correction": recursive,
        "corrected_branch_exact": corrected_branch_exact,
        "scalar_diagnostics": scalar,
        "mobius_diagonal_applicable": policy == "chiral",
    }


def run_analysis(max_level=13, policies=cross.POLICIES):
    """Run the exact cumulative-Regge construction for the requested sections."""
    max_level = int(max_level)
    if max_level < 1:
        raise ValueError("max_level must be positive")
    policies = tuple(policies)
    if not policies:
        raise ValueError("At least one triangular policy is required")
    if any(policy not in cross.POLICIES for policy in policies):
        raise ValueError(f"Unknown policy list: {policies}")

    started = time.time()
    _numerator, single_levels = hft_so9.derive_hft_spectrum(max_level)
    factorization = regge_factorization.factor_symmetric_vector_tower(
        single_levels, max_level
    )
    tower = symmetric_tower_restriction_audit(max_level - 1)
    stable_pieri = d5_stable_pieri_audit()
    scalar_response = a0_scalar_response_audit(max_level - 1)
    diagnostics = tuple(
        policy_diagnostics(
            single_levels, factorization, max_level, policy
        )
        for policy in policies
    )

    print("=" * 104)
    print("TK6B.6 — CUMULATIVE REGGE-TOWER UPLIFT")
    print("=" * 104)
    print(f"Physical HFT levels: 1 through {max_level}")
    print(
        "Res Sym^N(V10) = sum_{j=0}^N Sym^j(V9): "
        f"{tower['all_exact']}"
    )
    print(
        f"Stable D5 Pieri sample ({stable_pieri['tested']} terms): "
        f"{stable_pieri['all_exact']}"
    )
    print(
        "A0 scalar response is 1/(1+q): "
        f"{scalar_response['all_exact']}"
    )
    for item in diagnostics:
        print(f"Policy: {item['policy']}")
        print(f"  exact cumulative restrictions: {item['all_branch_exact']}")
        print(f"  positive D5 coefficients: {item['all_positive']}")
        if item["first_failure"] is not None:
            failure = item["first_failure"]
            print(
                f"  first negative level: {failure['level']} "
                f"({len(failure['negative_terms'])} negative irreps, "
                f"minimum {failure['minimum']})"
            )
        recursive = item["recursive_correction"]
        print(
            "  greedy J/A0 correction positive: "
            f"{recursive['all_positive']}"
        )
        print(f"  correction series: {recursive['corrections']}")
        print(
            "  A0 tail determined by the scalar diagonal: "
            f"{item['scalar_diagnostics']['a0_from_scalar_tail']}"
        )
        print(
            "  all-chiral scalar diagonal equals the six-ray HFT Möbius "
            "functional: "
            f"{item['scalar_diagnostics']['mobius_diagonal_identity']}"
            if item["mobius_diagonal_applicable"]
            else "  six-ray all-chiral Möbius functional: not applicable"
        )
        if recursive["failure"] is not None:
            print(f"  correction obstruction: {recursive['failure']}")
    print("Protected SO(10) baseline imported: NO")
    print(f"Runtime: {time.time() - started:.3f}s")

    all_structural = (
        tower["all_exact"]
        and stable_pieri["all_exact"]
        and scalar_response["all_exact"]
        and all(
        item["all_branch_exact"]
        and item["scalar_diagnostics"]["scalar_identity"]
        and (
            not item["mobius_diagonal_applicable"]
            or item["scalar_diagnostics"]["mobius_diagonal_identity"]
        )
        and (
            not item["recursive_correction"]["completed"]
            or item["corrected_branch_exact"]
        )
        for item in diagnostics
        )
    )
    return {
        "max_level": max_level,
        "single_levels": single_levels,
        "factorization": factorization,
        "tower": tower,
        "stable_pieri": stable_pieri,
        "scalar_response": scalar_response,
        "policies": diagnostics,
        "all_structural": all_structural,
    }


def run_self_test():
    """Exercise the formal identity and both fixed section policies."""
    if D5(0, 0, 0, 0, 1) * J_CHARACTER != A0_CHARACTER:
        raise AssertionError("The A0 = 16_- J seed identity failed")
    if J_CHARACTER.branch(B4, rule="default") != B4(0):
        raise AssertionError("The half-spinor difference does not restrict to zero")
    result = run_analysis(max_level=7)
    if not result["all_structural"]:
        raise AssertionError("The cumulative Regge uplift failed structurally")
    chiral = next(
        item for item in result["policies"] if item["policy"] == "chiral"
    )
    if not (
        chiral["recursive_correction"]["all_positive"]
        and chiral["corrected_branch_exact"]
    ):
        raise AssertionError("The chiral J/A0 construction failed")
    return True


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Test explicit cumulative D5 lifts of the HFT Regge factorization"
    )
    parser.add_argument("--max-level", type=int, default=13)
    parser.add_argument(
        "--policy",
        action="append",
        choices=cross.POLICIES,
        help="Triangular section to test; repeat for more than one",
    )
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.self_test:
            return 0 if run_self_test() else 1
        result = run_analysis(
            max_level=args.max_level,
            policies=tuple(args.policy) if args.policy else cross.POLICIES,
        )
    except Exception as error:
        print(f"TK6B.6 FAILED: {error}", file=sys.stderr)
        return 1
    chiral = next(
        (
            item
            for item in result["policies"]
            if item["policy"] == "chiral"
        ),
        None,
    )
    chiral_success = chiral is None or (
        chiral["recursive_correction"]["all_positive"]
        and chiral["corrected_branch_exact"]
    )
    return 0 if result["all_structural"] and chiral_success else 1


if __name__ == "__main__":
    raise SystemExit(main())
