"""TK3: positive lift fibres in trajectory-adapted kernel coordinates.

Every lift in the finite positive-chirality parent domain is written as the
all-chiral reference lift plus an integral combination of the eight TK2 kernel
generators.  Positivity is then a finite system of exact integer inequalities.

The construction uses only HFT-derived SO(9) characters and baseline-free
branching data.  It never imports the protected SO(10) completion.
"""

import argparse
import sys
import time
from dataclasses import dataclass

from sage.all import ZZ

import finite_cross_section as cross
from trajectory_kernel import kernel_lattice as lattice


@dataclass(frozen=True)
class PositiveFiber:
    """All positive integral lifts of one cumulative HFT character."""

    level: int
    reference_coefficients: tuple
    coordinate_labels: tuple
    solutions: tuple

    @property
    def solution_count(self):
        return len(self.solutions)


def ordered_generators(generators):
    """Order generators from highest to lowest B4 top weight."""
    return tuple(
        sorted(
            generators,
            key=lambda generator: cross.b4_dynkin_to_ambient(
                generator.top_weight
            ),
            reverse=True,
        )
    )


def family_label(generator):
    """Return the TK2 trajectory-family label and leading coordinate."""
    ell, m, r, s = generator.top_weight
    known = {
        (0, 0, 2): "A",
        (1, 0, 2): "B",
        (0, 0, 3): "C",
    }
    family = known.get((m, r, s), f"({m},{r},{s})")
    return f"{family}{ell}"


def reference_lift(domain, target):
    """Invert one target on the fixed all-chiral section in the TK2 domain."""
    selection = {
        weight: cross.select_parent(weight, policy="chiral")
        for weight in domain["weights"]
    }
    exact, integral, _positive, coefficients, residual = (
        lattice.section_search.invert_sparse(
            cross.character_coefficients(target),
            domain["weights"],
            selection,
            domain["branch_tables"],
        )
    )
    if not exact or not integral or residual:
        raise ValueError("All-chiral reference inversion failed")
    return lattice.clean_sparse(coefficients)


def coefficients_from_coordinates(reference, generators, coordinates):
    """Evaluate ``reference + sum_i coordinates[i] K_i`` exactly."""
    if len(generators) != len(coordinates):
        raise ValueError("Generator and coordinate counts do not agree")
    coefficients = dict(reference)
    for generator, coordinate in zip(generators, coordinates):
        value = int(coordinate)
        if value:
            coefficients = lattice.add_sparse(
                coefficients, generator.as_dict(), scale=value
            )
    return coefficients


def verify_triangular_coordinate_order(generators):
    """Check the exact pivot property needed for finite enumeration."""
    for index, generator in enumerate(generators):
        relation = generator.as_dict()
        reference_parent = cross.select_parent(
            generator.top_weight, policy="chiral"
        )
        if relation.get(generator.alternative_parent) != 1:
            return False
        if relation.get(reference_parent) != -1:
            return False
        for later in generators[index + 1 :]:
            later_relation = later.as_dict()
            if later_relation.get(reference_parent, 0):
                return False
            if later_relation.get(generator.alternative_parent, 0):
                return False
    return True


def enumerate_positive_coordinates(reference, generators):
    """Enumerate all nonnegative lifts using triangular integer bounds.

    At generator ``i``, its non-reference parent has coefficient ``z_i`` and
    its reference top parent has current coefficient minus ``z_i``.  Later
    generators cannot change either pivot, so ``0 <= z_i <= current`` is an
    exact finite range rather than an imposed search cutoff.
    """
    if not verify_triangular_coordinate_order(generators):
        raise ValueError("Kernel generators are not in triangular pivot order")

    solutions = []
    coordinates = [0] * len(generators)

    def visit(index, current):
        if index == len(generators):
            if all(value >= 0 for value in current.values()):
                solutions.append(tuple(coordinates))
            return

        generator = generators[index]
        reference_parent = cross.select_parent(
            generator.top_weight, policy="chiral"
        )
        available = current.get(reference_parent, 0)
        if available not in ZZ:
            raise ValueError(f"Non-integral coordinate bound: {available}")
        available = int(available)
        if available < 0:
            return

        relation = generator.as_dict()
        for coordinate in range(available + 1):
            coordinates[index] = coordinate
            updated = (
                current
                if coordinate == 0
                else lattice.add_sparse(current, relation, scale=coordinate)
            )
            visit(index + 1, updated)
        coordinates[index] = 0

    visit(0, dict(reference))
    return tuple(solutions)


def build_positive_fibers(max_level=10):
    """Construct every finite-domain positive fibre through ``max_level``."""
    domain = lattice.build_finite_domain(max_level)
    generators = ordered_generators(lattice.natural_kernel_generators(domain))
    labels = tuple(family_label(generator) for generator in generators)
    fibers = {}

    for level in range(1, max_level + 1):
        reference = reference_lift(domain, domain["cumulative"][level])
        solutions = enumerate_positive_coordinates(reference, generators)
        fibers[level] = PositiveFiber(
            level=level,
            reference_coefficients=tuple(reference.items()),
            coordinate_labels=labels,
            solutions=solutions,
        )
    return domain, generators, fibers


def solution_coefficients(fiber, generators, solution):
    return coefficients_from_coordinates(
        dict(fiber.reference_coefficients), generators, solution
    )


def coefficientwise_leq(left, right, parents):
    """Test whether ``right-left`` is a nonnegative D5 character."""
    return all(right.get(parent, 0) >= left.get(parent, 0) for parent in parents)


def nonnegative_increment_diagnostics(domain, generators, fibers):
    """Test the optional stronger condition of nonnegative D5 increments.

    This condition is not required for positive cumulative lifts: restriction
    and the choice of positive SO(10) lift need not commute with taking the
    difference between consecutive cumulative SO(9) characters.
    """
    parents = domain["parents"]
    coefficient_tables = {
        level: tuple(
            solution_coefficients(fiber, generators, solution)
            for solution in fiber.solutions
        )
        for level, fiber in fibers.items()
    }

    reachable = {0: {0: 1}}
    predecessors = {}
    adjacent_pair_counts = {}
    # The artificial level zero has one zero lift.
    previous_tables = ({},)
    previous_counts = (1,)

    for level in sorted(fibers):
        current_tables = coefficient_tables[level]
        current_counts = [0] * len(current_tables)
        level_predecessors = {}
        adjacent_pairs = 0
        for current_index, current in enumerate(current_tables):
            for previous_index, previous in enumerate(previous_tables):
                if coefficientwise_leq(previous, current, parents):
                    adjacent_pairs += 1
                    if previous_counts[previous_index]:
                        current_counts[current_index] += previous_counts[previous_index]
                        level_predecessors.setdefault(current_index, previous_index)
        reachable[level] = {
            index: count
            for index, count in enumerate(current_counts)
            if count
        }
        predecessors[level] = level_predecessors
        adjacent_pair_counts[level] = adjacent_pairs
        previous_tables = current_tables
        previous_counts = tuple(current_counts)

    final_level = max(fibers)
    total_chains = sum(reachable[final_level].values())
    example_indices = None
    if total_chains:
        final_index = next(iter(reachable[final_level]))
        chain = {}
        current_index = final_index
        for level in range(final_level, 0, -1):
            chain[level] = current_index
            current_index = predecessors[level][current_index]
        example_indices = tuple(chain[level] for level in range(1, final_level + 1))

    first_adjacent_failure = next(
        (level for level, count in adjacent_pair_counts.items() if count == 0),
        None,
    )
    obstruction = None
    if first_adjacent_failure is not None:
        current_tables = coefficient_tables[first_adjacent_failure]
        previous_tables = (
            ({},)
            if first_adjacent_failure == 1
            else coefficient_tables[first_adjacent_failure - 1]
        )
        candidates = []
        for previous_index, previous in enumerate(previous_tables):
            for current_index, current in enumerate(current_tables):
                negative = tuple(
                    (parent, current.get(parent, 0) - previous.get(parent, 0))
                    for parent in parents
                    if current.get(parent, 0) - previous.get(parent, 0) < 0
                )
                score = (len(negative), -sum(value for _parent, value in negative))
                candidates.append(
                    (score, previous_index, current_index, negative)
                )
        _score, previous_index, current_index, negative = min(candidates)
        obstruction = {
            "transition": (first_adjacent_failure - 1, first_adjacent_failure),
            "previous_index": previous_index,
            "current_index": current_index,
            "negative_increment": negative,
        }

    return {
        "coefficient_tables": coefficient_tables,
        "reachable": reachable,
        "adjacent_pair_counts": adjacent_pair_counts,
        "total_chains": total_chains,
        "example_indices": example_indices,
        "first_adjacent_failure": first_adjacent_failure,
        "obstruction": obstruction,
    }


def coordinate_ranges(fiber):
    """Return minimum and maximum of each coordinate on a nonempty fibre."""
    if not fiber.solutions:
        return ()
    return tuple(
        (
            min(solution[index] for solution in fiber.solutions),
            max(solution[index] for solution in fiber.solutions),
        )
        for index in range(len(fiber.coordinate_labels))
    )


def reference_statistics(fiber):
    values = [0] + [value for _parent, value in fiber.reference_coefficients]
    return {
        "negative_terms": sum(value < 0 for value in values),
        "minimum": min(values, default=0),
    }


def affine_positivity_constraints(reference, generators, parents):
    """Return nonconstant coefficient inequalities for one positive fibre."""
    constraints = []
    for parent in parents:
        vector = tuple(
            generator.as_dict().get(parent, 0) for generator in generators
        )
        constant = reference.get(parent, 0)
        if any(vector):
            constraints.append((parent, constant, vector))
    return tuple(constraints)


def validate_positive_fibers(domain, generators, fibers):
    """Verify enumerated coefficients and representative restrictions exactly."""
    for level, fiber in fibers.items():
        if len(set(fiber.solutions)) != fiber.solution_count:
            return False
        for solution in fiber.solutions:
            coefficients = solution_coefficients(fiber, generators, solution)
            if any(value < 0 for value in coefficients.values()):
                return False

        sample_solutions = fiber.solutions[:1] + fiber.solutions[-1:]
        target = lattice.clean_sparse(
            cross.character_coefficients(domain["cumulative"][level])
        )
        for solution in sample_solutions:
            coefficients = solution_coefficients(fiber, generators, solution)
            if lattice.branch_virtual(coefficients) != target:
                return False
    return True


def format_affine_constraint(parent, constant, vector, labels):
    terms = [str(constant)] if constant else []
    for coefficient, label in zip(vector, labels):
        if not coefficient:
            continue
        sign = "+" if coefficient > 0 else "-"
        magnitude = abs(coefficient)
        term = label if magnitude == 1 else f"{magnitude}*{label}"
        if not terms:
            terms.append(term if coefficient > 0 else f"-{term}")
        else:
            terms.append(f"{sign} {term}")
    return f"D5 {parent}: {' '.join(terms) if terms else '0'} >= 0"


def summarize_tk3(max_level=10, verbose=False):
    """Run the complete baseline-free TK3 positive-fibre analysis."""
    started = time.time()
    domain, generators, fibers = build_positive_fibers(max_level)
    increments = nonnegative_increment_diagnostics(domain, generators, fibers)
    fibers_verified = validate_positive_fibers(domain, generators, fibers)

    print("=" * 116)
    print("TK3 — POSITIVE LIFT FIBRES IN TRAJECTORY-KERNEL COORDINATES (BASELINE-FREE)")
    print("=" * 116)
    print(f"HFT levels: 1 through {max_level}")
    print(f"Finite parent domain: {len(domain['parents'])} D5 columns over {len(domain['weights'])} B4 rows")
    print(f"Integral kernel coordinates: {len(generators)}")
    print("Coordinate order: " + ", ".join(family_label(item) for item in generators))
    print("Protected SO(10) baseline imported: NO")
    print("-" * 116)
    print(
        f"{'Level':<7}{'Ref negative':<15}{'Ref minimum':<14}"
        f"{'Positive lifts':<18}{'Optional +increment pairs'}"
    )
    print("-" * 116)
    for level, fiber in fibers.items():
        stats = reference_statistics(fiber)
        print(
            f"{level:<7}{stats['negative_terms']:<15}{stats['minimum']:<14}"
            f"{fiber.solution_count:<18}{increments['adjacent_pair_counts'][level]}"
        )

    print("\nPositive coordinate ranges by level:")
    for level, fiber in fibers.items():
        ranges = coordinate_ranges(fiber)
        if not ranges:
            print(f"  n={level}: EMPTY")
            continue
        nonzero_ranges = [
            f"{label}={lower}" if lower == upper else f"{label}={lower}..{upper}"
            for label, (lower, upper) in zip(fiber.coordinate_labels, ranges)
            if lower or upper
        ]
        print(f"  n={level}: " + (", ".join(nonzero_ranges) or "all zero"))

    print("\nOptional stronger nonnegative-increment condition:")
    print(
        f"  Chains through level {max_level}: {increments['total_chains']}"
    )
    if increments["example_indices"] is not None:
        print("  Example coordinate sequence:")
        for level, solution_index in enumerate(
            increments["example_indices"], start=1
        ):
            solution = fibers[level].solutions[solution_index]
            print(f"    n={level}: {solution}")
    else:
        first_failed = increments["first_adjacent_failure"]
        if first_failed is not None:
            print(
                "  First transition with no admissible pair: "
                f"{first_failed - 1}->{first_failed}"
            )
            print(
                "  Least-negative increment certificate: "
                f"{increments['obstruction']['negative_increment']}"
            )
        else:
            print(
                "  Every adjacent transition has an admissible pair, but no "
                "single pairwise-compatible chain crosses the whole window."
            )
        print(
            "  This does not obstruct positive cumulative lifts; it only "
            "rules out positive SO(10) differences for one common choice."
        )

    if verbose:
        print("\nRepresentative positive coordinate tuples by level:")
        for level, fiber in fibers.items():
            examples = fiber.solutions[:10]
            suffix = "" if len(examples) == fiber.solution_count else " ..."
            print(f"  n={level}: {examples}{suffix}")

        print(f"\nNonconstant positivity inequalities at level {max_level}:")
        final_reference = dict(fibers[max_level].reference_coefficients)
        for constraint in affine_positivity_constraints(
            final_reference, generators, domain["parents"]
        ):
            print(
                "  "
                + format_affine_constraint(
                    *constraint, fibers[max_level].coordinate_labels
                )
            )

    all_fibers_nonempty = all(fiber.solutions for fiber in fibers.values())
    all_structural = (
        verify_triangular_coordinate_order(generators)
        and all_fibers_nonempty
        and fibers_verified
    )
    print("-" * 116)
    print(f"Every cumulative positive fibre nonempty: {all_fibers_nonempty}")
    print(f"Enumerated lift coefficients and sampled restrictions verified: {fibers_verified}")
    print(
        "Optional nonnegative-increment chain exists: "
        f"{increments['total_chains'] > 0}"
    )
    print(f"TK3 structural checks: {'PASS' if all_structural else 'FAIL'}")
    print(f"Elapsed: {time.time() - started:.3f}s")
    return {
        "domain": domain,
        "generators": generators,
        "fibers": fibers,
        "increments": increments,
        "fibers_verified": fibers_verified,
        "all_checks": all_structural,
    }


def run_self_test():
    """Test exact coordinate evaluation on one synthetic triangular pair."""
    generator = lattice.KernelGenerator(
        top_weight=(0, 0, 0, 2),
        alternative_parent=(0, 0, 0, 1, 1),
        relation=(
            ((0, 0, 0, 0, 2), -1),
            ((0, 0, 0, 1, 1), 1),
        ),
        first_hft_level=6,
        reduced_depth=6,
    )
    reference = {(0, 0, 0, 0, 2): 2}
    generators = (generator,)
    solutions = enumerate_positive_coordinates(reference, generators)
    checks = (
        solutions == ((0,), (1,), (2,)),
        coefficients_from_coordinates(reference, generators, (2,))
        == {(0, 0, 0, 1, 1): 2},
    )
    passed = all(checks)
    print("TRAJECTORY-KERNEL TK3 SELF-TEST")
    print(f"Triangular positive-fibre enumeration: {'PASS' if passed else 'FAIL'}")
    print("Protected SO(10) baseline imported: NO")
    return passed


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Baseline-free positive lifts in trajectory-kernel coordinates"
    )
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--max-level", type=int, default=10)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        sys.exit(0 if run_self_test() else 1)
    result = summarize_tk3(args.max_level, args.verbose)
    sys.exit(0 if result["all_checks"] else 1)
