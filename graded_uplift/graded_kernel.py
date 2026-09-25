"""Finite exact feasibility for oscillator-graded SO(10) lifts.

This baseline-free module exposes two candidate domains.  The ``paper-bound``
domain implements the SO(10) bound of hep-th/0310292, Eq. (2.15), together
with the finite upper cutoff Delta <= ell+1 needed by starred predecessors.
The ``outer-closed`` domain adds the D5 outer conjugate of every tagged term at
the same Delta.  It thereby isolates the effect of the paper's chirality-
asymmetric bound.

The solver accepts arbitrary graded SO(8) and ungraded virtual SO(10) targets.
It imports no protected completion.
"""

from collections import defaultdict

from sage.all import MixedIntegerLinearProgram, QQ, matrix, vector
from sage.numerical.mip import MIPSolverException

from graded_uplift import refined_branching
from graded_uplift import refined_spectrum


DOMAIN_POLICIES = ("paper-bound", "outer-closed")


def twice_delta_bound(label):
    """Return twice the hep-th/0310292 bound in Eq. (2.15)."""
    a1, a2, a3, a4, a5 = label
    return 2 + 2 * a1 + 4 * a2 + 6 * a3 + 5 * a4 + 3 * a5


def outer_conjugate(label):
    a1, a2, a3, a4, a5 = label
    return (a1, a2, a3, a5, a4)


def _bounded_labels(max_twice_delta):
    """Enumerate every dominant D5 label satisfying the paper bound."""
    result = []
    for a5 in range((max_twice_delta - 2) // 3 + 1):
        for a4 in range((max_twice_delta - 2 - 3 * a5) // 5 + 1):
            for a3 in range((max_twice_delta - 2 - 3 * a5 - 5 * a4) // 6 + 1):
                for a2 in range(
                    (max_twice_delta - 2 - 3 * a5 - 5 * a4 - 6 * a3) // 4 + 1
                ):
                    remainder = (
                        max_twice_delta
                        - 2
                        - 3 * a5
                        - 5 * a4
                        - 6 * a3
                        - 4 * a2
                    )
                    for a1 in range(remainder // 2 + 1):
                        result.append((a1, a2, a3, a4, a5))
    return tuple(sorted(result))


def candidate_terms(level, policy="paper-bound", delta_slack=0):
    """Return finite ``(D5 label, 2Delta)`` candidates at one string level."""
    if policy not in DOMAIN_POLICIES:
        raise ValueError(f"Unknown graded-domain policy: {policy}")
    if int(delta_slack) < 0:
        raise ValueError("delta_slack must be nonnegative")
    maximum = 2 * (int(level) + 1 + int(delta_slack))
    terms = set()
    for label in _bounded_labels(maximum):
        minimum = twice_delta_bound(label)
        for twice_delta in range(minimum, maximum + 1, 2):
            terms.add((label, twice_delta))
    if policy == "outer-closed":
        terms.update(
            (outer_conjugate(label), twice_delta)
            for label, twice_delta in tuple(terms)
        )
    return tuple(sorted(terms, key=lambda item: (item[1], item[0])))


def _graded_coefficients(table):
    return {
        (nu, label): coefficient
        for nu, character in table.items()
        for label, coefficient in refined_spectrum.d4_coefficients(character).items()
        if coefficient
    }


def tagged_term_image(label, twice_delta):
    sign = refined_branching.d5_parity(label)
    image = refined_branching.delta_nu_image(label, twice_delta)
    return {
        (nu, d4_label): sign * coefficient
        for nu, character in image.items()
        for d4_label, coefficient in refined_spectrum.d4_coefficients(character).items()
        if coefficient
    }


def _evaluate_solution(solution):
    graded = {}
    ungraded = defaultdict(int)
    for (label, twice_delta), coefficient in solution.items():
        if not coefficient:
            continue
        ungraded[label] += coefficient
        for key, value in tagged_term_image(label, twice_delta).items():
            graded[key] = graded.get(key, 0) + coefficient * value
            if not graded[key]:
                del graded[key]
    return dict(sorted(graded.items())), {
        label: coefficient
        for label, coefficient in sorted(ungraded.items())
        if coefficient
    }


def rational_feasibility(
    level,
    graded_target,
    ungraded_target,
    policy="paper-bound",
    delta_slack=0,
):
    """Test the same finite system over QQ by exact rank comparison.

    Rational infeasibility is a stronger and solver-independent obstruction to
    an integral tagged lift.  This routine intentionally does not optimize or
    construct a preferred solution.
    """
    terms = candidate_terms(level, policy, delta_slack)
    target_graded = _graded_coefficients(graded_target)
    target_ungraded = {
        tuple(label): int(coefficient)
        for label, coefficient in ungraded_target.items()
        if coefficient
    }
    images = {term: tagged_term_image(*term) for term in terms}
    candidate_labels = {label for label, _twice_delta in terms}
    missing_labels = tuple(sorted(set(target_ungraded) - candidate_labels))
    if missing_labels:
        return {
            "feasible_over_QQ": False,
            "rank": None,
            "augmented_rank": None,
            "row_count": None,
            "column_count": len(terms),
            "missing_labels": missing_labels,
        }

    graded_rows = set(target_graded)
    for image in images.values():
        graded_rows.update(image)
    row_keys = [("graded", row) for row in sorted(graded_rows)]
    row_keys.extend(("ungraded", label) for label in sorted(candidate_labels))
    row_index = {key: index for index, key in enumerate(row_keys)}
    entries = {}
    for column, term in enumerate(terms):
        label, _twice_delta = term
        for row, coefficient in images[term].items():
            entries[(row_index[("graded", row)], column)] = coefficient
        entries[(row_index[("ungraded", label)], column)] = 1
    right_hand_side = []
    for kind, row in row_keys:
        if kind == "graded":
            right_hand_side.append(target_graded.get(row, 0))
        else:
            right_hand_side.append(target_ungraded.get(row, 0))

    coefficient_matrix = matrix(
        QQ, len(row_keys), len(terms), entries, sparse=True
    )
    target_vector = vector(QQ, right_hand_side)
    rank = coefficient_matrix.rank()
    augmented_rank = coefficient_matrix.augment(target_vector.column()).rank()
    return {
        "feasible_over_QQ": rank == augmented_rank,
        "rank": rank,
        "augmented_rank": augmented_rank,
        "row_count": len(row_keys),
        "column_count": len(terms),
        "missing_labels": (),
    }


def solve_graded_lift(
    level,
    graded_target,
    ungraded_target,
    policy="paper-bound",
    delta_slack=0,
):
    """Find a minimum-charge integral tagged lift, or report infeasibility."""
    terms = candidate_terms(level, policy, delta_slack)
    target_graded = _graded_coefficients(graded_target)
    target_ungraded = {
        tuple(label): int(coefficient)
        for label, coefficient in ungraded_target.items()
        if coefficient
    }
    candidate_labels = {label for label, _twice_delta in terms}
    missing_labels = tuple(sorted(set(target_ungraded) - candidate_labels))
    if missing_labels:
        return {
            "feasible": False,
            "policy": policy,
            "level": level,
            "delta_slack": delta_slack,
            "term_count": len(terms),
            "missing_labels": missing_labels,
            "minimum_charge": None,
            "solution": {},
            "exact": False,
        }

    images = {
        term: tagged_term_image(*term)
        for term in terms
    }
    graded_rows = set(target_graded)
    for image in images.values():
        graded_rows.update(image)
    ungraded_rows = candidate_labels | set(target_ungraded)

    program = MixedIntegerLinearProgram(maximization=False)
    positive = program.new_variable(integer=True, nonnegative=True)
    negative = program.new_variable(integer=True, nonnegative=True)

    def variable(index):
        return positive[index] - negative[index]

    for row in sorted(graded_rows):
        expression = program.sum(
            images[term].get(row, 0) * variable(index)
            for index, term in enumerate(terms)
            if images[term].get(row, 0)
        )
        program.add_constraint(expression == target_graded.get(row, 0))

    terms_by_label = defaultdict(list)
    for index, (label, _twice_delta) in enumerate(terms):
        terms_by_label[label].append(index)
    for label in sorted(ungraded_rows):
        expression = program.sum(variable(index) for index in terms_by_label[label])
        program.add_constraint(expression == target_ungraded.get(label, 0))

    charge = program.sum(
        positive[index] + negative[index]
        for index in range(len(terms))
    )
    program.set_objective(charge)
    try:
        objective = int(round(float(program.solve())))
    except MIPSolverException as error:
        return {
            "feasible": False,
            "policy": policy,
            "level": level,
            "delta_slack": delta_slack,
            "term_count": len(terms),
            "missing_labels": (),
            "minimum_charge": None,
            "solution": {},
            "exact": False,
            "message": str(error),
        }

    positive_values = program.get_values(positive)
    negative_values = program.get_values(negative)
    solution = {}
    for index, term in enumerate(terms):
        coefficient = int(round(positive_values.get(index, 0))) - int(
            round(negative_values.get(index, 0))
        )
        if coefficient:
            solution[term] = coefficient
    evaluated_graded, evaluated_ungraded = _evaluate_solution(solution)
    exact = (
        evaluated_graded == dict(sorted(target_graded.items()))
        and evaluated_ungraded == dict(sorted(target_ungraded.items()))
        and sum(abs(value) for value in solution.values()) == objective
    )
    return {
        "feasible": True,
        "policy": policy,
        "level": level,
        "delta_slack": delta_slack,
        "term_count": len(terms),
        "missing_labels": (),
        "minimum_charge": objective,
        "solution": dict(sorted(solution.items())),
        "exact": exact,
    }
