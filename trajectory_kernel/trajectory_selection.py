"""TK4: baseline-free selection tests on the positive trajectory fibres.

This module does not compare with the protected SO(10) completion.  It tests
whether intrinsic costs derived from the exact TK2 corrected shift select a
distinguished path through the TK3 positive fibres.
"""

import argparse
import sys
import time
from dataclasses import dataclass

from sage.all import MixedIntegerLinearProgram

from trajectory_kernel import correction_ansatz as fibers_module


@dataclass(frozen=True)
class PathState:
    cost: tuple
    path_count: int
    predecessor: int | None


def generator_coordinates(generators):
    """Return ``((family_key, ell), ...)`` in the fibre coordinate order."""
    result = []
    for generator in generators:
        ell, m, r, s = generator.top_weight
        result.append(((m, r, s), ell))
    return tuple(result)


def transport_coordinates(previous, generators):
    """Transport coordinates by ``K_(ell-1) -> K_ell``.

    Coordinates at ``ell=0`` have no predecessor and are set to zero; they are
    the new boundary data at the next level.
    """
    keys = generator_coordinates(generators)
    index = {key: position for position, key in enumerate(keys)}
    transported = []
    for family, ell in keys:
        predecessor = index.get((family, ell - 1)) if ell > 0 else None
        transported.append(0 if predecessor is None else previous[predecessor])
    return tuple(transported)


def transition_statistics(previous, current, generators):
    """Measure corrected-shift defects and new boundary population."""
    expected = transport_coordinates(previous, generators)
    keys = generator_coordinates(generators)
    interior_defect = sum(
        abs(value - predicted)
        for value, predicted, (_family, ell) in zip(current, expected, keys)
        if ell > 0
    )
    boundary_injection = sum(
        value
        for value, (_family, ell) in zip(current, keys)
        if ell == 0
    )
    total_population = sum(current)
    support = sum(value != 0 for value in current)
    return {
        "expected": expected,
        "interior_defect": interior_defect,
        "boundary_injection": boundary_injection,
        "total_population": total_population,
        "support": support,
    }


def transition_cost(previous, current, generators, rule):
    stats = transition_statistics(previous, current, generators)
    interior = stats["interior_defect"]
    boundary = stats["boundary_injection"]
    population = stats["total_population"]
    support = stats["support"]
    if rule == "transport-first":
        return (interior, boundary, population, support)
    if rule == "boundary-first":
        return (boundary, interior, population, support)
    if rule == "total-deviation":
        return (interior + boundary, population, support, interior)
    raise ValueError(f"Unknown selection rule: {rule}")


def add_cost(left, right):
    return tuple(a + b for a, b in zip(left, right))


def dynamic_optimal_paths(fibers, generators, rule):
    """Find globally optimal paths and retain exact tie counts."""
    levels = tuple(sorted(fibers))
    zero = tuple(0 for _generator in generators)
    previous_solutions = (zero,)
    previous_states = (PathState((0, 0, 0, 0), 1, None),)
    states_by_level = {}
    horizon_minima = {}

    for level in levels:
        current_solutions = fibers[level].solutions
        current_states = []
        for current in current_solutions:
            best_cost = None
            best_count = 0
            best_predecessor = None
            for previous_index, (previous, state) in enumerate(
                zip(previous_solutions, previous_states)
            ):
                candidate = add_cost(
                    state.cost,
                    transition_cost(previous, current, generators, rule),
                )
                if best_cost is None or candidate < best_cost:
                    best_cost = candidate
                    best_count = state.path_count
                    best_predecessor = previous_index
                elif candidate == best_cost:
                    best_count += state.path_count
            current_states.append(
                PathState(best_cost, best_count, best_predecessor)
            )
        states_by_level[level] = tuple(current_states)
        horizon_minima[level] = min(state.cost for state in current_states)
        previous_solutions = current_solutions
        previous_states = tuple(current_states)

    final_level = levels[-1]
    final_states = states_by_level[final_level]
    optimal_cost = horizon_minima[final_level]
    optimal_final_indices = tuple(
        index
        for index, state in enumerate(final_states)
        if state.cost == optimal_cost
    )
    optimal_path_count = sum(
        final_states[index].path_count for index in optimal_final_indices
    )

    chosen_indices = {}
    current_index = optimal_final_indices[0]
    for level in reversed(levels):
        chosen_indices[level] = current_index
        current_index = states_by_level[level][current_index].predecessor
    chosen_path = tuple(
        fibers[level].solutions[chosen_indices[level]] for level in levels
    )

    prefix_optimality = []
    for level in levels:
        state = states_by_level[level][chosen_indices[level]]
        prefix_optimality.append(state.cost == horizon_minima[level])

    return {
        "rule": rule,
        "levels": levels,
        "states_by_level": states_by_level,
        "horizon_minima": horizon_minima,
        "optimal_cost": optimal_cost,
        "optimal_final_indices": optimal_final_indices,
        "optimal_path_count": optimal_path_count,
        "chosen_indices": chosen_indices,
        "chosen_path": chosen_path,
        "prefix_optimality": tuple(prefix_optimality),
        "cutoff_stable": all(prefix_optimality),
    }


def level_extrema(fiber, generators):
    """Count minimizers of simple level-local intrinsic statistics."""
    keys = generator_coordinates(generators)

    def boundary(solution):
        return sum(
            value
            for value, (_family, ell) in zip(solution, keys)
            if ell == 0
        )

    metrics = {
        "population": lambda solution: sum(solution),
        "support": lambda solution: sum(value != 0 for value in solution),
        "boundary": boundary,
    }
    result = {}
    for name, metric in metrics.items():
        values = tuple(metric(solution) for solution in fiber.solutions)
        minimum = min(values)
        result[name] = {
            "minimum": minimum,
            "count": sum(value == minimum for value in values),
            "first": fiber.solutions[values.index(minimum)],
        }
    return result


def decoded_coordinates(solution, generators):
    """Return only nonzero coordinates with human-readable family labels."""
    return {
        fibers_module.family_label(generator): value
        for generator, value in zip(generators, solution)
        if value
    }


def path_cost(solutions, generators, rule):
    """Evaluate one complete coordinate path under a stated rule."""
    previous = tuple(0 for _generator in generators)
    total = (0, 0, 0, 0)
    for current in solutions:
        total = add_cost(
            total, transition_cost(previous, current, generators, rule)
        )
        previous = current
    return total


def primary_cost(full_cost, rule):
    """Discard the optional support tie-break used only in fibre enumeration."""
    if rule in ("transport-first", "boundary-first"):
        return full_cost[:3]
    if rule == "total-deviation":
        return (full_cost[0], full_cost[1], full_cost[3])
    raise ValueError(f"Unknown selection rule: {rule}")


def milp_optimal_path(domain, generators, max_level, rule):
    """Solve the full positive path problem without materializing its fibres."""
    program = MixedIntegerLinearProgram(maximization=False)
    coordinates = program.new_variable(integer=True, nonnegative=True)
    defects = program.new_variable(integer=True, nonnegative=True)
    keys = generator_coordinates(generators)
    key_index = {key: index for index, key in enumerate(keys)}
    references = {
        level: fibers_module.reference_lift(
            domain, domain["cumulative"][level]
        )
        for level in range(1, max_level + 1)
    }

    interior_terms = []
    boundary_terms = []
    population_terms = []

    for level in range(1, max_level + 1):
        reference = references[level]
        for parent in domain["parents"]:
            expression = reference.get(parent, 0) + program.sum(
                generator.as_dict().get(parent, 0)
                * coordinates[level, index]
                for index, generator in enumerate(generators)
                if generator.as_dict().get(parent, 0)
            )
            program.add_constraint(expression >= 0)

        for index, (_family, ell) in enumerate(keys):
            variable = coordinates[level, index]
            population_terms.append(variable)
            if ell == 0:
                boundary_terms.append(variable)
                continue

            predecessor_index = key_index.get((_family, ell - 1))
            expected = (
                0
                if level == 1 or predecessor_index is None
                else coordinates[level - 1, predecessor_index]
            )
            defect = defects[level, index]
            program.add_constraint(defect >= variable - expected)
            program.add_constraint(defect >= expected - variable)
            interior_terms.append(defect)

    interior = program.sum(interior_terms)
    boundary = program.sum(boundary_terms)
    population = program.sum(population_terms)
    if rule == "transport-first":
        objectives = (interior, boundary, population)
    elif rule == "boundary-first":
        objectives = (boundary, interior, population)
    elif rule == "total-deviation":
        objectives = (interior + boundary, population, interior)
    else:
        raise ValueError(f"Unknown selection rule: {rule}")

    optimum = []
    for objective in objectives:
        program.set_objective(objective)
        value = int(round(program.solve()))
        optimum.append(value)
        program.add_constraint(objective == value)

    values = program.get_values(coordinates)
    solutions = tuple(
        tuple(
            int(round(values.get((level, index), 0)))
            for index in range(len(generators))
        )
        for level in range(1, max_level + 1)
    )
    actual_cost = primary_cost(path_cost(solutions, generators, rule), rule)
    if actual_cost != tuple(optimum):
        raise ValueError(
            "MILP path cost does not match the optimized objective: "
            f"actual={actual_cost}, optimized={tuple(optimum)}, "
            f"solutions={solutions}"
        )

    for level, solution in enumerate(solutions, start=1):
        coefficients = fibers_module.coefficients_from_coordinates(
            references[level], generators, solution
        )
        if any(value < 0 for value in coefficients.values()):
            raise ValueError(f"MILP returned a negative lift at level {level}")
        target = fibers_module.lattice.clean_sparse(
            fibers_module.cross.character_coefficients(
                domain["cumulative"][level]
            )
        )
        if fibers_module.lattice.branch_virtual(coefficients) != target:
            raise ValueError(
                f"MILP lift does not restrict to the HFT target at level {level}"
            )

    final_ranges = []
    for index in range(len(generators)):
        variable = coordinates[max_level, index]
        program.set_objective(variable)
        lower = int(round(program.solve()))
        program.set_objective(-variable)
        upper = -int(round(program.solve()))
        final_ranges.append((lower, upper))

    return {
        "rule": rule,
        "optimum": tuple(optimum),
        "solutions": solutions,
        "final_ranges": tuple(final_ranges),
        "unique_final": all(lower == upper for lower, upper in final_ranges),
    }


def summarize_next_level_probe(max_level=11):
    """Probe one level beyond TK3 using full-horizon integer optimization."""
    started = time.time()
    domain = fibers_module.lattice.build_finite_domain(max_level)
    generators = fibers_module.ordered_generators(
        fibers_module.lattice.natural_kernel_generators(domain)
    )
    rules = ("transport-first", "boundary-first", "total-deviation")
    full_results = {
        rule: milp_optimal_path(domain, generators, max_level, rule)
        for rule in rules
    }
    short_results = {
        rule: milp_optimal_path(domain, generators, max_level - 1, rule)
        for rule in rules
    }

    print("=" * 118)
    print("TK4 — NEXT-LEVEL FULL-HORIZON MILP PROBE (BASELINE-FREE)")
    print("=" * 118)
    print(f"Horizon: 1 through {max_level}")
    print(f"Finite domain: {len(domain['weights'])} B4 rows, {len(domain['parents'])} D5 columns")
    print(f"Integral kernel generators: {len(generators)}")
    print("Coordinates: " + ", ".join(fibers_module.family_label(item) for item in generators))
    print("Protected SO(10) baseline imported: NO")

    for rule in rules:
        full = full_results[rule]
        short = short_results[rule]
        prefix_cost = primary_cost(
            path_cost(full["solutions"][:-1], generators, rule), rule
        )
        print(f"\n{rule}:")
        print(f"  level-{max_level - 1} optimum: {short['optimum']}")
        print(f"  level-{max_level} optimum: {full['optimum']}")
        print(f"  chosen prefix remains horizon-optimal: {prefix_cost == short['optimum']}")
        print(
            f"  final coordinates: {decoded_coordinates(full['solutions'][-1], generators)}"
        )
        varying = {
            fibers_module.family_label(generator): bounds
            for generator, bounds in zip(generators, full["final_ranges"])
            if bounds[0] != bounds[1]
        }
        print(f"  final point unique under optimized costs: {full['unique_final']}")
        if varying:
            print(f"  residual optimal ranges: {varying}")

    same_final = len(
        {result["solutions"][-1] for result in full_results.values()}
    ) == 1
    print("\nCross-rule result:")
    print(f"  All rules choose the same level-{max_level} point: {same_final}")
    print(f"Elapsed: {time.time() - started:.3f}s")
    return {
        "domain": domain,
        "generators": generators,
        "full": full_results,
        "short": short_results,
        "same_final": same_final,
    }


def summarize_tk4(max_level=10, verbose=False):
    """Run the first baseline-free analytic-selection experiment."""
    started = time.time()
    domain, generators, fibers = fibers_module.build_positive_fibers(max_level)
    if not fibers_module.validate_positive_fibers(domain, generators, fibers):
        raise ValueError("TK3 positive fibres failed validation")

    rules = ("transport-first", "boundary-first", "total-deviation")
    paths = {
        rule: dynamic_optimal_paths(fibers, generators, rule) for rule in rules
    }
    final_extrema = level_extrema(fibers[max_level], generators)

    print("=" * 118)
    print("TK4 — FIRST ANALYTIC TRAJECTORY-SELECTION EXPERIMENT (BASELINE-FREE)")
    print("=" * 118)
    print(f"Levels: 1 through {max_level}")
    print(f"Positive lifts at final level: {fibers[max_level].solution_count}")
    print("Coordinate order: " + ", ".join(fibers[max_level].coordinate_labels))
    print("Protected SO(10) baseline imported: NO")

    print("\nSimple level-local extrema at the final level:")
    for name, result in final_extrema.items():
        print(
            f"  minimum {name}: {result['minimum']}; "
            f"minimizers: {result['count']}; "
            f"first: {decoded_coordinates(result['first'], generators)}"
        )

    print("\nGlobal trajectory-compatible path rules:")
    for rule, result in paths.items():
        print(f"  {rule}:")
        print(f"    optimum cost: {result['optimal_cost']}")
        print(f"    optimal final states: {len(result['optimal_final_indices'])}")
        print(f"    optimal paths including ties: {result['optimal_path_count']}")
        print(f"    cutoff-stable chosen prefix: {result['cutoff_stable']}")
        print(
            "    final coordinates: "
            f"{decoded_coordinates(result['chosen_path'][-1], generators)}"
        )

    all_same_final = len(
        {result["chosen_path"][-1] for result in paths.values()}
    ) == 1
    all_unique = all(result["optimal_path_count"] == 1 for result in paths.values())
    all_cutoff_stable = all(result["cutoff_stable"] for result in paths.values())

    print("\nCross-rule diagnostics:")
    print(f"  All three rules choose the same final point: {all_same_final}")
    print(f"  Every rule has a unique optimal path: {all_unique}")
    print(f"  Every chosen path is cutoff-stable: {all_cutoff_stable}")

    if verbose:
        print("\nChosen coordinate paths:")
        for rule, result in paths.items():
            print(f"  {rule}:")
            for level, solution, stable in zip(
                result["levels"],
                result["chosen_path"],
                result["prefix_optimality"],
            ):
                print(
                    f"    n={level}: {decoded_coordinates(solution, generators)} "
                    f"[horizon-optimal={stable}]"
                )

    print("-" * 118)
    print("This experiment tests intrinsic candidates; it does not yet declare a canonical lift.")
    print(f"Elapsed: {time.time() - started:.3f}s")
    return {
        "domain": domain,
        "generators": generators,
        "fibers": fibers,
        "paths": paths,
        "final_extrema": final_extrema,
        "all_same_final": all_same_final,
        "all_unique": all_unique,
        "all_cutoff_stable": all_cutoff_stable,
    }


def run_self_test():
    """Check the corrected-shift coordinate transport convention."""
    generator_type = fibers_module.lattice.KernelGenerator
    generators = (
        generator_type((1, 0, 0, 2), (1, 0, 0, 1, 1), (), 7, 6),
        generator_type((0, 0, 0, 2), (0, 0, 0, 1, 1), (), 6, 6),
    )
    previous = (0, 3)
    current = (3, 2)
    stats = transition_statistics(previous, current, generators)
    checks = (
        transport_coordinates(previous, generators) == (3, 0),
        stats["interior_defect"] == 0,
        stats["boundary_injection"] == 2,
    )
    passed = all(checks)
    print("TRAJECTORY-KERNEL TK4 SELF-TEST")
    print(f"Corrected-shift coordinate transport: {'PASS' if passed else 'FAIL'}")
    print("Protected SO(10) baseline imported: NO")
    return passed


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Test intrinsic trajectory-compatible selection principles"
    )
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--max-level", type=int, default=10)
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument(
        "--probe-next-level",
        action="store_true",
        help="Use full-horizon MILP optimization instead of fibre enumeration",
    )
    args = parser.parse_args()
    if args.self_test:
        sys.exit(0 if run_self_test() else 1)
    if args.probe_next_level:
        summarize_next_level_probe(args.max_level)
        sys.exit(0)
    summarize_tk4(args.max_level, args.verbose)
    sys.exit(0)
