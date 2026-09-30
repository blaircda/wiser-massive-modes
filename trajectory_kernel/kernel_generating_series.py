"""TK4b: kernel-valued source series and HFT numerator compatibility.

For trajectory coordinates ``z_F(n,ell)``, define the source transform

    s_F(n,0)   = z_F(n,0),
    s_F(n,ell) = z_F(n,ell) - z_F(n-1,ell-1).

Thus ``S_F(q,t) = (1-q*t) C_F(q,t)``, where ``C_F`` is the coordinate
series.  Boundary-only generation means that ``S_F`` has no positive power of
``t``.  This notation avoids collision with the HFT fermionic partition
function convention ``Z_F``.

The module also tests the stronger baseline-free equation

    N_n^10 = Z_Q^10 * (L_n - L_{n-1})

with every cumulative ``L_n`` constrained to be a positive integral lift in
the complete finite parent domain.  No protected SO(10) data is imported.
"""

import argparse
import sys
import time
from collections import defaultdict

from sage.all import MixedIntegerLinearProgram
from sage.numerical.mip import MIPSolverException

import hft_so10_uplift
from trajectory_kernel import correction_ansatz as fibers_module
from trajectory_kernel import milp_certification
from trajectory_kernel import trajectory_selection as selection


def family_name(generator):
    """Return the fixed-tail family name used in TK2--TK4."""
    _ell, m, r, s = generator.top_weight
    return {
        (0, 0, 2): "A",
        (1, 0, 2): "B",
        (0, 0, 3): "C",
    }.get((m, r, s), f"F({m},{r},{s})")


def source_transform(solutions, generators):
    """Convert a coordinate path to its exact boundary-and-interior sources."""
    keys = selection.generator_coordinates(generators)
    index = {key: position for position, key in enumerate(keys)}
    previous = tuple(0 for _generator in generators)
    terms = []

    for level, current in enumerate(solutions, start=1):
        for position, ((family, ell), value) in enumerate(zip(keys, current)):
            if ell == 0:
                source = value
            else:
                predecessor = index.get((family, ell - 1))
                transported = 0 if predecessor is None else previous[predecessor]
                source = value - transported
            if source:
                terms.append(
                    {
                        "level": level,
                        "family": family_name(generators[position]),
                        "ell": ell,
                        "value": source,
                    }
                )
        previous = current
    return tuple(terms)


def reconstruct_from_sources(source_terms, generators, max_level):
    """Invert the source transform exactly."""
    keys = selection.generator_coordinates(generators)
    index = {key: position for position, key in enumerate(keys)}
    names = {
        (family_name(generator), generator.top_weight[0]): position
        for position, generator in enumerate(generators)
    }
    sources = {
        (term["level"], names[(term["family"], term["ell"])]): term["value"]
        for term in source_terms
    }
    previous = [0] * len(generators)
    solutions = []
    for level in range(1, max_level + 1):
        current = [0] * len(generators)
        for position, (family, ell) in enumerate(keys):
            if ell == 0:
                transported = 0
            else:
                predecessor = index.get((family, ell - 1))
                transported = 0 if predecessor is None else previous[predecessor]
            current[position] = transported + sources.get((level, position), 0)
        solutions.append(tuple(current))
        previous = current
    return tuple(solutions)


def source_statistics(terms):
    boundary = tuple(term for term in terms if term["ell"] == 0)
    interior = tuple(term for term in terms if term["ell"] > 0)
    return {
        "terms": len(terms),
        "charge": sum(abs(term["value"]) for term in terms),
        "boundary_terms": len(boundary),
        "boundary_charge": sum(abs(term["value"]) for term in boundary),
        "interior_terms": len(interior),
        "interior_charge": sum(abs(term["value"]) for term in interior),
    }


def d5_character(coefficients):
    """Convert sparse D5 Dynkin coefficients to a Weyl character."""
    character = fibers_module.cross.D5(0)
    for parent, coefficient in coefficients.items():
        character += coefficient * fibers_module.cross.D5(*parent)
    return character


def character_table(character):
    """Return an irreducible coefficient table keyed by ambient weights."""
    return {
        weight: coefficient
        for weight, coefficient in character.monomial_coefficients().items()
        if coefficient
    }


def d5_weight_to_dynkin(weight):
    """Convert a D5 ambient highest weight to exact Dynkin labels."""
    x1, x2, x3, x4, x5 = weight.to_vector()
    return (
        int(x1 - x2),
        int(x2 - x3),
        int(x3 - x4),
        int(x4 - x5),
        int(x4 + x5),
    )


def add_positivity_constraints(program, coordinates, domain, generators, level, reference):
    """Constrain one cumulative lift to have nonnegative D5 coefficients."""
    for parent in domain["parents"]:
        expression = reference.get(parent, 0) + program.sum(
            generator.as_dict().get(parent, 0) * coordinates[level, index]
            for index, generator in enumerate(generators)
            if generator.as_dict().get(parent, 0)
        )
        program.add_constraint(expression >= 0)


def numerator_compatibility(max_level, domain, generators):
    """Test exact HFT numerator division with positive cumulative lifts."""
    p10 = hft_so10_uplift.compute_hft_d5(max_level)
    zq10 = p10[1]
    references = {
        level: fibers_module.reference_lift(
            domain, domain["cumulative"][level]
        )
        for level in range(1, max_level + 1)
    }
    reference_characters = {
        0: fibers_module.cross.D5(0),
        **{
            level: d5_character(references[level])
            for level in range(1, max_level + 1)
        },
    }
    generator_products = tuple(
        character_table(zq10 * d5_character(generator.as_dict()))
        for generator in generators
    )

    program = MixedIntegerLinearProgram(maximization=False)
    coordinates = program.new_variable(integer=True, nonnegative=True)
    feasible_through = 0
    solutions = {}
    obstruction = None

    for level in range(1, max_level + 1):
        add_positivity_constraints(
            program,
            coordinates,
            domain,
            generators,
            level,
            references[level],
        )

        reference_increment = (
            reference_characters[level] - reference_characters[level - 1]
        )
        base_remainder_character = p10[level] - zq10 * reference_increment
        base_remainder = character_table(base_remainder_character)
        weights = set(base_remainder)
        for table in generator_products:
            weights.update(table)

        for weight in weights:
            expression = base_remainder.get(weight, 0) - program.sum(
                table.get(weight, 0) * coordinates[level, index]
                for index, table in enumerate(generator_products)
                if table.get(weight, 0)
            )
            if level > 1:
                expression += program.sum(
                    table.get(weight, 0) * coordinates[level - 1, index]
                    for index, table in enumerate(generator_products)
                    if table.get(weight, 0)
                )
            program.add_constraint(expression == 0)

        program.set_objective(0)
        try:
            program.solve()
        except MIPSolverException as error:
            a0_generator = next(
                (
                    generator
                    for generator in generators
                    if generator.top_weight == (0, 0, 0, 2)
                ),
                None,
            )
            level_two_kernel_decomposition = None
            if level == 2 and a0_generator is not None:
                chirality_difference = (
                    fibers_module.cross.D5(0, 0, 0, 2, 0)
                    - fibers_module.cross.D5(0, 0, 0, 0, 2)
                )
                level_two_kernel_decomposition = (
                    base_remainder_character
                    == -2 * d5_character(a0_generator.as_dict())
                    + chirality_difference
                )
            obstruction = {
                "level": level,
                "message": str(error),
                "reference_remainder_terms": len(base_remainder),
                "reference_remainder": tuple(
                    sorted(
                        (
                            d5_weight_to_dynkin(weight),
                            int(coefficient),
                        )
                        for weight, coefficient in base_remainder.items()
                    )
                ),
                "reference_remainder_dimension": int(
                    base_remainder_character.degree()
                ),
                "reference_remainder_restricts_zero": (
                    base_remainder_character.branch(
                        fibers_module.cross.B4, rule="default"
                    )
                    == fibers_module.cross.B4(0)
                ),
                "equals_minus_two_a0_plus_chirality_difference": (
                    level_two_kernel_decomposition
                ),
            }
            break

        feasible_through = level
        values = program.get_values(coordinates)
        prefix_coordinates = {
            horizon: tuple(
                milp_certification.checked_value(
                    values,
                    (horizon, index),
                    "numerator-compatibility coordinate",
                )
                for index in range(len(generators))
            )
            for horizon in range(1, level + 1)
        }
        previous_lift = fibers_module.cross.D5(0)
        for horizon in range(1, level + 1):
            coefficients = fibers_module.coefficients_from_coordinates(
                references[horizon],
                generators,
                prefix_coordinates[horizon],
            )
            if any(value < 0 for value in coefficients.values()):
                raise ValueError(
                    "MILP numerator-compatibility witness has a negative "
                    f"lift coefficient at level {horizon}"
                )
            lift = d5_character(coefficients)
            if zq10 * (lift - previous_lift) != p10[horizon]:
                raise ValueError(
                    "MILP numerator-compatibility witness fails exact "
                    f"character verification at level {horizon}"
                )
            previous_lift = lift
        solutions[level] = prefix_coordinates[level]

    return {
        "feasible_through": feasible_through,
        "obstruction": obstruction,
        "solutions": solutions,
        "p10": p10,
        "zq10": zq10,
    }


def summarize_tk4b(max_level=11, verbose=False):
    """Run source-series and exact-numerator compatibility diagnostics."""
    started = time.time()
    domain = fibers_module.lattice.build_finite_domain(max_level)
    generators = fibers_module.ordered_generators(
        fibers_module.lattice.natural_kernel_generators(domain)
    )
    rules = ("transport-first", "boundary-first", "total-deviation")
    paths = {
        rule: selection.milp_optimal_path(domain, generators, max_level, rule)
        for rule in rules
    }

    source_data = {}
    for rule, result in paths.items():
        terms = source_transform(result["solutions"], generators)
        if reconstruct_from_sources(terms, generators, max_level) != result["solutions"]:
            raise ValueError(f"Source transform failed to reconstruct {rule} path")
        source_data[rule] = {
            "terms": terms,
            "statistics": source_statistics(terms),
        }

    interior_minima = {}
    for horizon in range(1, max_level + 1):
        result = selection.milp_optimal_path(
            domain, generators, horizon, "transport-first"
        )
        interior_minima[horizon] = result["optimum"][0]

    numerator = numerator_compatibility(max_level, domain, generators)

    print("=" * 118)
    print("TK4b — KERNEL-VALUED SOURCE SERIES AND HFT NUMERATOR TEST (BASELINE-FREE)")
    print("=" * 118)
    print(f"Levels: 1 through {max_level}")
    print(f"Finite domain: {len(domain['weights'])} B4 rows, {len(domain['parents'])} D5 columns")
    print(f"Kernel generators: {len(generators)}")
    print("Protected SO(10) baseline imported: NO")
    print("\nSource identity: S_F(q,t) = (1-q*t) C_F(q,t)")

    print("\nMinimum total interior-source charge by horizon:")
    print(
        "  "
        + ", ".join(
            f"n={level}: {value}"
            for level, value in interior_minima.items()
        )
    )
    first_bulk = next(
        (level for level, value in interior_minima.items() if value), None
    )
    print(f"  First horizon requiring an interior source: {first_bulk}")

    print("\nSource complexity of representative optimized paths:")
    for rule, data in source_data.items():
        stats = data["statistics"]
        print(
            f"  {rule}: terms={stats['terms']}, charge={stats['charge']}, "
            f"boundary={stats['boundary_terms']}/{stats['boundary_charge']}, "
            f"interior={stats['interior_terms']}/{stats['interior_charge']}"
        )
        if verbose:
            print(f"    terms: {data['terms']}")

    print("\nExact HFT numerator compatibility:")
    print(
        "  Equation tested: N_n^10 = Z_Q^10 * (L_n - L_(n-1)), "
        "with every L_n positive."
    )
    print(f"  Feasible through level: {numerator['feasible_through']}")
    if numerator["obstruction"]:
        print(
            "  First infeasible level in the finite positive domain: "
            f"{numerator['obstruction']['level']}"
        )
        print(
            "  All-chiral reference remainder terms there: "
            f"{numerator['obstruction']['reference_remainder_terms']}"
        )
        print(
            "  Remainder dimension / restriction zero: "
            f"{numerator['obstruction']['reference_remainder_dimension']} / "
            f"{numerator['obstruction']['reference_remainder_restricts_zero']}"
        )
        if verbose:
            print(
                "  Remainder coefficients: "
                f"{numerator['obstruction']['reference_remainder']}"
            )
        decomposition = numerator["obstruction"].get(
            "equals_minus_two_a0_plus_chirality_difference"
        )
        if decomposition is not None:
            print(
                "  Remainder equals -2*A0 + (126_conjugate-126_chiral): "
                f"{decomposition}"
            )
    else:
        print("  Exact positive numerator-compatible path found through the full window.")

    print("-" * 118)
    print("Finite source support is descriptive unless it is stable under further HFT extension.")
    print(f"Elapsed: {time.time() - started:.3f}s")
    return {
        "domain": domain,
        "generators": generators,
        "paths": paths,
        "sources": source_data,
        "interior_minima": interior_minima,
        "numerator": numerator,
    }


def run_self_test():
    """Check that the source transform and reconstruction are inverse."""
    generator_type = fibers_module.lattice.KernelGenerator
    generators = (
        generator_type((1, 0, 0, 2), (1, 0, 0, 1, 1), (), 7, 6),
        generator_type((0, 0, 0, 2), (0, 0, 0, 1, 1), (), 6, 6),
    )
    solutions = ((0, 1), (1, 2), (2, 0))
    terms = source_transform(solutions, generators)
    reconstructed = reconstruct_from_sources(terms, generators, len(solutions))
    passed = reconstructed == solutions
    print("TRAJECTORY-KERNEL TK4b SELF-TEST")
    print(f"Source transform inversion: {'PASS' if passed else 'FAIL'}")
    print("Protected SO(10) baseline imported: NO")
    return passed


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Kernel-valued source series and HFT numerator compatibility"
    )
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--max-level", type=int, default=11)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        sys.exit(0 if run_self_test() else 1)
    summarize_tk4b(args.max_level, args.verbose)
    sys.exit(0)
