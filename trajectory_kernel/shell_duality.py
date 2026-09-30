"""TK6B.5b: eliminate pivot rows from the universal shell circuit cone.

For every natural all-split kernel coordinate there is one unique
non-all-chiral parent whose Gale row is the corresponding positive unit
vector.  Eliminating these pivot variables identifies the positive Gale
circuit cone with a cone of nonnegative functions on all-chiral parents
subject to explicit prefix-shell inequalities.

This is a structural D5 -> B4 branching calculation.  It imports no
protected SO(10) completion.
"""

import argparse
import itertools
import math
import sys
import time
from collections import Counter

from sage.all import Polyhedron, QQ, ZZ, lcm, matrix, vector

import finite_cross_section as cross
from trajectory_kernel import all_split_circuits
from trajectory_kernel import boundary_shell
from trajectory_kernel import hft_weighted_inequalities


def _primitive_integral_ray(ray):
    """Convert an exact rational ray to a primitive integral tuple."""
    denominators = [QQ(value).denominator() for value in ray]
    common = int(lcm(denominators)) if denominators else 1
    integral = [int(QQ(value) * common) for value in ray]
    content = 0
    for value in integral:
        content = math.gcd(content, abs(value))
    if not content:
        raise ValueError("An extreme ray cannot vanish")
    primitive = tuple(value // content for value in integral)
    if any(value < 0 for value in primitive):
        raise ValueError("The prefix-shell cone returned a negative ray entry")
    return primitive


def eliminated_shell_system(relations):
    """Build the exact pivot-eliminated prefix-shell operator.

    If ``K`` is the sparse natural-relation matrix, its rows split into
    unique alternative pivots ``+e_g`` and all-chiral rows ``V``.  The
    positive equation

        x + V^T y = 0

    is equivalent to ``x=L*y >= 0`` with ``L=-V^T``.
    """
    names = tuple(relations)
    alternatives = {}
    all_chiral = set()
    parents = set()
    for name, relation in relations.items():
        parents.update(relation)
        non_chiral = tuple(
            (parent, int(coefficient))
            for parent, coefficient in relation.items()
            if parent[3] != 0
        )
        if len(non_chiral) != 1 or non_chiral[0][1] != 1:
            raise ValueError(
                f"Relation {name} lacks one unique positive pivot: {non_chiral}"
            )
        alternatives[name] = non_chiral[0][0]
        all_chiral.update(parent for parent in relation if parent[3] == 0)

    if len(set(alternatives.values())) != len(names):
        raise ValueError("Two shell coordinates share a non-chiral pivot")
    if set(alternatives.values()) & all_chiral:
        raise ValueError("A shell pivot was also classified as all-chiral")
    if parents != set(alternatives.values()) | all_chiral:
        raise ValueError("The shell parent partition is incomplete")

    chiral_parents = tuple(sorted(all_chiral))
    parent_index = {parent: index for index, parent in enumerate(chiral_parents)}
    operator = matrix(
        ZZ,
        len(names),
        len(chiral_parents),
        lambda row, column: -int(
            relations[names[row]].get(chiral_parents[column], 0)
        ),
    )
    return {
        "names": names,
        "relations": relations,
        "alternatives": alternatives,
        "chiral_parents": chiral_parents,
        "chiral_top_weights": tuple(
            cross.top_b4_weight(parent) for parent in chiral_parents
        ),
        "parent_index": parent_index,
        "operator": operator,
        "parents": tuple(sorted(parents)),
    }


def prefix_shell_value(top_weight, split, values):
    """Evaluate the closed prefix-shell inequality on top-weight values."""
    total = int(values.get(tuple(top_weight), 0))
    for step in range(1, int(split) + 1):
        q1, q2, q3, q4 = boundary_shell.shell_packets(top_weight, step)
        q1, q2, q3, q4 = (
            cross.top_b4_weight(parent) for parent in (q1, q2, q3, q4)
        )
        total += int(values.get(q1, 0))
        total -= int(values.get(q2, 0))
        total += int(values.get(q3, 0))
        total -= int(values.get(q4, 0))
    return total


def infinite_tail_violation(values):
    """Exhibit the inevitable violated shell for finite nonzero ``y>=0``.

    The fourth shell packet forgets the leading label of its source.  Hence a
    fixed positive value at ``(L,M,R,S)`` contributes negatively to shell
    coordinates with arbitrarily large leading label.  Past the finite
    support, every positive term vanishes while a nonempty negative tail
    remains.
    """
    cleaned = {
        tuple(map(int, label)): int(value)
        for label, value in values.items()
        if value
    }
    if not cleaned:
        return None
    if any(min(label) < 0 for label in cleaned):
        raise ValueError("Prefix-shell labels must be dominant")
    if any(value < 0 for value in cleaned.values()):
        raise ValueError("The infinite-cone obstruction assumes y >= 0")

    label = min(cleaned)
    leading_bound = max(item[0] for item in cleaned)
    leading = leading_bound + 1
    left, middle, third, spin = label
    split = third + 1
    top_weight = (
        leading,
        left,
        middle,
        spin + 2 * third + 2,
    )
    value = prefix_shell_value(top_weight, split, cleaned)
    negative_tail = sum(
        cleaned.get(
            (
                left,
                middle,
                step - 1,
                spin + 2 * (split - step),
            ),
            0,
        )
        for step in range(1, split + 1)
    )
    if negative_tail < cleaned[label] or value != -negative_tail or value >= 0:
        raise ValueError("The predicted infinite leading-tail violation failed")
    return {
        "seed_label": label,
        "top_weight": top_weight,
        "split": split,
        "value": value,
        "negative_tail": negative_tail,
    }


def chain_tail(middle, third, spin, split, max_ell):
    """Return one universal leading-label tail for a fixed shell family."""
    middle, third, spin, split, max_ell = map(
        int, (middle, third, spin, split, max_ell)
    )
    max_ell = int(max_ell)
    if min(middle, third, spin, max_ell) < 0:
        raise ValueError("Chain-tail labels and horizon must be nonnegative")
    if not 1 <= split <= spin // 2:
        raise ValueError("Chain-tail split is outside its allowed range")
    return {
        (leading, third, split - 1, spin - 2 * split): 1
        for leading in range(middle, middle + max_ell + 2)
    }


def interval_endpoint_functional(first, last, middle, third, spin):
    """Pull a leading-label interval through the three-fold Möbius operator."""
    first, last, middle, third, spin = map(
        int, (first, last, middle, third, spin)
    )
    if first < 0 or last < first or min(middle, third, spin) < 0:
        raise ValueError("Invalid leading-label interval")
    result = {}
    for e2, e3 in itertools.product((0, 1), repeat=2):
        sign = -1 if (e2 + e3) % 2 else 1
        for leading, endpoint_sign in ((first - e2, 1), (last + 1 - e2, -1)):
            label = (
                leading,
                middle + e2 - e3,
                third + e3,
                spin,
            )
            if min(label) < 0:
                continue
            value = result.get(label, 0) + sign * endpoint_sign
            if value:
                result[label] = value
            else:
                result.pop(label, None)
    return dict(sorted(result.items()))


def a_chain_tail(max_ell):
    """Return the ``m=r=0,s=2,k=1`` chain tail."""
    return chain_tail(0, 0, 2, 1, max_ell)


def a_chain_endpoint_functional(max_ell):
    """Return the four-term HFT pullback of the growing A-chain circuit."""
    return interval_endpoint_functional(0, int(max_ell) + 1, 0, 0, 0)


def a_chain_tail_diagnostics(max_ell):
    """Verify the first parametric boundary circuit and its telescoping pullback."""
    top_weights = tuple((ell, 0, 0, 2) for ell in range(int(max_ell) + 1))
    relations = all_split_circuits.all_split_relations(top_weights)
    system = eliminated_shell_system(relations)
    values = a_chain_tail(max_ell)
    ray = tuple(
        values.get(label, 0) for label in system["chiral_top_weights"]
    )
    slacks = tuple(int(value) for value in system["operator"] * vector(ZZ, ray))
    reduced = reduced_positive_rays(system)
    pulled = hft_weighted_inequalities.pullback_coordinate_functional(values)
    expected = a_chain_endpoint_functional(max_ell)
    return {
        "max_ell": int(max_ell),
        "top_weights": top_weights,
        "values": values,
        "slacks": slacks,
        "all_shell_slacks_zero": all(value == 0 for value in slacks),
        "primitive_extreme_ray": ray in reduced["rays"],
        "pulled_functional": pulled,
        "expected_functional": expected,
        "four_term_endpoint_identity": pulled == expected,
    }


def general_chain_tail_diagnostics(middle, third, spin, split, max_ell):
    """Verify a general split tail and its bounded endpoint pullback."""
    top_weights = tuple(
        (ell, int(middle), int(third), int(spin))
        for ell in range(int(max_ell) + 1)
    )
    relations = all_split_circuits.all_split_relations(top_weights)
    system = eliminated_shell_system(relations)
    values = chain_tail(middle, third, spin, split, max_ell)
    ray = tuple(values.get(label, 0) for label in system["chiral_top_weights"])
    slacks = tuple(int(value) for value in system["operator"] * vector(ZZ, ray))
    reduced = reduced_positive_rays(system)
    pulled = hft_weighted_inequalities.pullback_coordinate_functional(values)
    first = int(middle)
    last = first + int(max_ell) + 1
    expected = interval_endpoint_functional(
        first,
        last,
        int(third),
        int(split) - 1,
        int(spin) - 2 * int(split),
    )
    return {
        "parameters": (
            int(middle),
            int(third),
            int(spin),
            int(split),
            int(max_ell),
        ),
        "all_shell_slacks_zero": all(value == 0 for value in slacks),
        "primitive_extreme_ray": ray in reduced["rays"],
        "pulled_functional": pulled,
        "expected_functional": expected,
        "bounded_endpoint_identity": pulled == expected and len(pulled) <= 8,
    }


def verify_closed_prefix_operator(system):
    """Compare every matrix row with the label-uniform closed formula."""
    basis_checks = []
    names = system["names"]
    tops = system["chiral_top_weights"]
    operator = system["operator"]
    for row, name in enumerate(names):
        top_weight, split = name
        for column, label in enumerate(tops):
            values = {label: 1}
            basis_checks.append(
                int(operator[row, column])
                == prefix_shell_value(top_weight, split, values)
            )
    return all(basis_checks)


def reduced_positive_rays(system):
    """Enumerate extreme rays of ``y>=0`` and ``L*y>=0`` exactly."""
    operator = system["operator"]
    count = operator.ncols()
    inequalities = []
    for position in range(count):
        inequalities.append(
            tuple([0] + [1 if index == position else 0 for index in range(count)])
        )
    for row in operator.rows():
        inequalities.append(tuple([0] + [int(value) for value in row]))
    cone = Polyhedron(ieqs=tuple(inequalities), base_ring=QQ, backend="ppl")
    if cone.lines_list():
        raise ValueError("The nonnegative prefix-shell cone contains a line")
    rays = tuple(sorted(_primitive_integral_ray(ray) for ray in cone.rays_list()))
    return {"cone": cone, "rays": rays}


def pullback_complexity_diagnostics(system, rays):
    """Measure cancellations after pulling reduced rays to HFT multiplicities."""
    support_sizes = Counter()
    maximum_coefficients = Counter()
    examples = {}
    for ray in rays:
        coordinate_functional = {
            label: int(value)
            for label, value in zip(system["chiral_top_weights"], ray)
            if value
        }
        pulled = hft_weighted_inequalities.pullback_coordinate_functional(
            coordinate_functional
        )
        support = len(pulled)
        maximum = max((abs(value) for value in pulled.values()), default=0)
        support_sizes[support] += 1
        maximum_coefficients[maximum] += 1
        examples.setdefault(
            support,
            {
                "coordinate_functional": coordinate_functional,
                "pulled_functional": pulled,
            },
        )
    largest_support = max(support_sizes, default=0)
    return {
        "support_size_histogram": dict(sorted(support_sizes.items())),
        "maximum_coefficient_histogram": dict(
            sorted(maximum_coefficients.items())
        ),
        "largest_support": largest_support,
        "largest_support_example": examples.get(largest_support),
    }


def lift_reduced_ray(system, ray):
    """Restore the unique alternative-pivot entries of one reduced ray."""
    if len(ray) != len(system["chiral_parents"]):
        raise ValueError("Reduced ray has the wrong number of chiral entries")
    slacks = system["operator"] * vector(ZZ, ray)
    if any(value < 0 for value in slacks):
        raise ValueError("A reduced ray violates a prefix-shell inequality")
    by_parent = {
        parent: int(value)
        for parent, value in zip(system["chiral_parents"], ray)
        if value
    }
    for name, value in zip(system["names"], slacks):
        if value:
            by_parent[system["alternatives"][name]] = int(value)
    return tuple(int(by_parent.get(parent, 0)) for parent in system["parents"])


def section_decomposition(system, coordinates, shell_counts):
    """Apply nonnegative shell counts to all-chiral section coordinates.

    With ``L`` the prefix-shell operator, the final all-chiral coefficients
    are ``u=c-L^T*z`` and the alternative-parent coefficients are ``z``.
    """
    operator = system["operator"]
    c = vector(ZZ, tuple(map(int, coordinates)))
    z = vector(ZZ, tuple(map(int, shell_counts)))
    if len(c) != operator.ncols() or len(z) != operator.nrows():
        raise ValueError("Section decomposition has incompatible dimensions")
    u = c - operator.transpose() * z
    return {
        "all_chiral": tuple(int(value) for value in u),
        "alternatives": tuple(int(value) for value in z),
        "positive": all(value >= 0 for value in u)
        and all(value >= 0 for value in z),
    }


def dual_pairing_identity(system, all_chiral, shell_counts, test_function):
    """Verify ``<y,c>=<y,u>+<L*y,z>`` with ``c=u+L^T*z``."""
    operator = system["operator"]
    u = vector(ZZ, tuple(map(int, all_chiral)))
    z = vector(ZZ, tuple(map(int, shell_counts)))
    y = vector(ZZ, tuple(map(int, test_function)))
    if len(u) != operator.ncols() or len(y) != operator.ncols():
        raise ValueError("Dual pairing has the wrong chiral dimension")
    if len(z) != operator.nrows():
        raise ValueError("Dual pairing has the wrong shell dimension")
    c = u + operator.transpose() * z
    left = y * c
    shell_slacks = operator * y
    right = y * u + shell_slacks * z
    return {
        "coordinates": tuple(int(value) for value in c),
        "shell_slacks": tuple(int(value) for value in shell_slacks),
        "left": int(left),
        "right": int(right),
        "exact": left == right,
    }


def full_positive_circuits(system):
    """Enumerate the original parent-row circuits without elimination."""
    rows = tuple(
        tuple(
            int(system["relations"][name].get(parent, 0))
            for name in system["names"]
        )
        for parent in system["parents"]
    )
    return all_split_circuits.positive_circuits(rows)["circuits"]


def elimination_diagnostics(top_weights):
    """Verify exact ray-by-ray equivalence on one finite shell family."""
    relations = all_split_circuits.all_split_relations(top_weights)
    system = eliminated_shell_system(relations)
    reduced = reduced_positive_rays(system)
    lifted = tuple(sorted(lift_reduced_ray(system, ray) for ray in reduced["rays"]))
    full = full_positive_circuits(system)
    return {
        "top_weights": tuple(sorted(set(tuple(weight) for weight in top_weights))),
        "system": system,
        "reduced": reduced,
        "full_circuits": full,
        "lifted_circuits": lifted,
        "closed_operator_exact": verify_closed_prefix_operator(system),
        "ray_bijection": lifted == full,
        "circuit_count": len(full),
        "maximum_coefficient": max(
            (max(circuit) for circuit in full), default=0
        ),
    }


def run_analysis(max_ell=0, max_m=0, max_r=0, max_s=4, min_s=2):
    """Run a reproducible finite audit of the all-label elimination theorem."""
    started = time.time()
    top_weights = all_split_circuits.top_weight_box(
        max_ell=max_ell,
        max_m=max_m,
        max_r=max_r,
        max_s=max_s,
        min_s=min_s,
    )
    result = elimination_diagnostics(top_weights)
    system = result["system"]
    pullback_complexity = pullback_complexity_diagnostics(
        system, result["reduced"]["rays"]
    )
    result["pullback_complexity"] = pullback_complexity
    sample_values = {
        label: index + 1
        for index, label in enumerate(system["chiral_top_weights"][:4])
    }
    tail_violation = infinite_tail_violation(sample_values)
    a_tail = a_chain_tail_diagnostics(max_ell=max(0, int(max_ell)))
    general_tail = general_chain_tail_diagnostics(
        middle=1,
        third=1,
        spin=max(4, int(max_s)),
        split=2,
        max_ell=max(0, int(max_ell)),
    )
    result["tail_violation"] = tail_violation
    result["a_chain_tail"] = a_tail
    result["general_chain_tail"] = general_tail
    u = tuple((index % 3) + 1 for index in range(len(system["chiral_parents"])))
    z = tuple((index % 2) for index in range(len(system["names"])))
    y = tuple((index % 4) + 1 for index in range(len(system["chiral_parents"])))
    pairing = dual_pairing_identity(system, u, z, y)
    result["dual_pairing"] = pairing
    print("=" * 100)
    print("TK6B.5b — PIVOT-ELIMINATED PREFIX-SHELL CONE")
    print("=" * 100)
    print(f"Top weights: {len(result['top_weights'])}")
    print(f"Natural shell coordinates: {len(system['names'])}")
    print(f"All-chiral parent variables: {len(system['chiral_parents'])}")
    print(f"Primitive positive circuits: {result['circuit_count']}")
    print(f"Maximum primitive coefficient: {result['maximum_coefficient']}")
    print(
        "Largest pulled HFT-functional support: "
        f"{pullback_complexity['largest_support']}"
    )
    print(f"Closed prefix-shell formula exact: {result['closed_operator_exact']}")
    print(f"Reduced rays lift bijectively to full circuits: {result['ray_bijection']}")
    print(
        "Nonzero finite support fails in the infinite shell cone: "
        f"{tail_violation is not None and tail_violation['value'] < 0}"
    )
    print(
        "Growing A-chain circuit has a four-term endpoint pullback: "
        f"{a_tail['primitive_extreme_ray'] and a_tail['four_term_endpoint_identity']}"
    )
    print(
        "General split-chain tail has at most eight endpoint terms: "
        f"{general_tail['primitive_extreme_ray'] and general_tail['bounded_endpoint_identity']}"
    )
    print(f"Exact shell/Farkas pairing identity: {pairing['exact']}")
    print("Protected SO(10) baseline imported: NO")
    print(f"Runtime: {time.time() - started:.3f}s")
    result["all_checks"] = (
        result["closed_operator_exact"]
        and result["ray_bijection"]
        and tail_violation is not None
        and tail_violation["value"] < 0
        and a_tail["all_shell_slacks_zero"]
        and a_tail["primitive_extreme_ray"]
        and a_tail["four_term_endpoint_identity"]
        and general_tail["all_shell_slacks_zero"]
        and general_tail["primitive_extreme_ray"]
        and general_tail["bounded_endpoint_identity"]
        and pairing["exact"]
    )
    return result


def run_self_test():
    """Check one unit and one coefficient-two finite shell system."""
    unit = run_analysis(max_s=4)
    mixed_base = run_analysis(max_m=1, max_s=4)
    weighted = run_analysis(max_ell=1, max_m=1, max_s=4)
    if not unit["all_checks"] or unit["maximum_coefficient"] != 1:
        raise AssertionError("The one-column prefix-shell control failed")
    if not weighted["all_checks"] or weighted["maximum_coefficient"] != 2:
        raise AssertionError("The coefficient-two prefix-shell audit failed")
    if not (
        mixed_base["pullback_complexity"]["largest_support"]
        < weighted["pullback_complexity"]["largest_support"]
    ):
        raise AssertionError("The mixed-circuit pullback-growth obstruction changed")
    return True


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Eliminate pivot rows from finite all-split shell cones"
    )
    parser.add_argument("--max-ell", type=int, default=0)
    parser.add_argument("--max-m", type=int, default=0)
    parser.add_argument("--max-r", type=int, default=0)
    parser.add_argument("--min-s", type=int, default=2)
    parser.add_argument("--max-s", type=int, default=4)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.self_test:
            return 0 if run_self_test() else 1
        result = run_analysis(
            max_ell=args.max_ell,
            max_m=args.max_m,
            max_r=args.max_r,
            min_s=args.min_s,
            max_s=args.max_s,
        )
    except Exception as error:
        print(f"TK6B.5b FAILED: {error}", file=sys.stderr)
        return 1
    return 0 if result["all_checks"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
