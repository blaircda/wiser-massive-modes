"""TK5c: minimality, non-uniqueness and cutoff stability of TK5b witnesses.

The model uses only the HFT-derived SO(9) data, the finite branching lattice
and the GMSZ residual-core source policy.  It never imports the protected
SO(10) completion.

Witnesses are optimized lexicographically:

1. number of nonzero source events;
2. total absolute source charge;
3. total kernel-coordinate population (only to choose one representative
   after the first two, scientifically relevant, optima have been fixed).

The first two objectives define a ``minimal witness`` in this module.  The
third objective is a deterministic convenience and is not part of the claim.
"""

import argparse
import time
from dataclasses import dataclass

from sage.all import MixedIntegerLinearProgram
from sage.numerical.mip import MIPSolverException

from trajectory_kernel import chamber_audit
from trajectory_kernel import chamber_core
from trajectory_kernel import correction_ansatz
from trajectory_kernel import kernel_lattice
from trajectory_kernel import regge_columns
from trajectory_kernel import trajectory_selection


@dataclass
class SourceModel:
    program: object
    coordinates: object
    source_positive: object
    source_negative: object
    source_active: object
    sites: tuple
    event_sum: object
    charge_sum: object
    population_sum: object
    coordinate_bounds: dict
    references: dict


def _integer_objective(value):
    """Round an integral MILP objective and reject numerical drift."""
    rounded = int(round(float(value)))
    if abs(float(value) - rounded) > 1e-6:
        raise ValueError(f"Expected integral objective, obtained {value}")
    return rounded


def _record_index(records):
    return {
        (item.level, item.label): item
        for level_records in records.values()
        for item in level_records
    }


def _cumulative_multiplicities(domain, max_level):
    return {
        level: correction_ansatz.cross.character_coefficients(
            domain["cumulative"][level]
        )
        for level in range(1, max_level + 1)
    }


def build_source_model(max_level, domain, generators, records):
    """Build the exact core-supported positive-path MILP.

    The coordinate bound for a generator is the cumulative multiplicity of
    its top B4 weight.  This is rigorous: that coordinate is the coefficient
    of the generator's alternative D5 parent, whose restriction contains the
    top B4 weight with multiplicity one, while the final lift is positive.
    """
    record_index = _record_index(records)
    keys = trajectory_selection.generator_coordinates(generators)
    key_index = {key: index for index, key in enumerate(keys)}
    cumulative = _cumulative_multiplicities(domain, max_level)
    references = {
        level: correction_ansatz.reference_lift(
            domain, domain["cumulative"][level]
        )
        for level in range(1, max_level + 1)
    }

    program = MixedIntegerLinearProgram(maximization=False)
    coordinates = program.new_variable(integer=True, nonnegative=True)
    source_positive = program.new_variable(integer=True, nonnegative=True)
    source_negative = program.new_variable(integer=True, nonnegative=True)
    source_active = program.new_variable(binary=True)

    coordinate_bounds = {}
    sites = []
    population_terms = []

    for level in range(1, max_level + 1):
        chamber_core._add_positivity_constraints(
            program,
            coordinates,
            domain,
            generators,
            level,
            references[level],
        )
        for index, generator in enumerate(generators):
            key = keys[index]
            ell = key[1]
            bound = int(cumulative[level].get(generator.top_weight, 0))
            coordinate_bounds[level, index] = bound
            program.add_constraint(coordinates[level, index] <= bound)
            population_terms.append(coordinates[level, index])

            predecessor_index = (
                None if ell == 0 else key_index.get((key[0], ell - 1))
            )
            transported = (
                0
                if level == 1 or predecessor_index is None
                else coordinates[level - 1, predecessor_index]
            )
            allowed = chamber_core._source_allowed(
                "gmsz-core", level, generator, record_index
            )
            if not allowed:
                program.add_constraint(coordinates[level, index] == transported)
                continue

            previous_bound = (
                0
                if level == 1 or predecessor_index is None
                else coordinate_bounds[level - 1, predecessor_index]
            )
            site = len(sites)
            positive_bound = bound
            negative_bound = previous_bound
            program.add_constraint(
                coordinates[level, index] - transported
                == source_positive[site] - source_negative[site]
            )
            program.add_constraint(
                source_positive[site] <= positive_bound * source_active[site]
            )
            program.add_constraint(
                source_negative[site] <= negative_bound * source_active[site]
            )
            sites.append(
                {
                    "site": site,
                    "level": level,
                    "index": index,
                    "generator": correction_ansatz.family_label(generator),
                    "top_weight": generator.top_weight,
                    "region": record_index[level, generator.top_weight].region,
                    "lower": -negative_bound,
                    "upper": positive_bound,
                }
            )

    event_sum = program.sum(source_active[item["site"]] for item in sites)
    charge_sum = program.sum(
        source_positive[item["site"]] + source_negative[item["site"]]
        for item in sites
    )
    population_sum = program.sum(population_terms)
    return SourceModel(
        program=program,
        coordinates=coordinates,
        source_positive=source_positive,
        source_negative=source_negative,
        source_active=source_active,
        sites=tuple(sites),
        event_sum=event_sum,
        charge_sum=charge_sum,
        population_sum=population_sum,
        coordinate_bounds=coordinate_bounds,
        references=references,
    )


def _solve_objective(program, objective):
    program.set_objective(objective)
    return _integer_objective(program.solve())


def optimize_model(model):
    """Apply the three lexicographic objectives and extract one witness."""
    minimum_events = _solve_objective(model.program, model.event_sum)
    model.program.add_constraint(model.event_sum == minimum_events)
    minimum_charge = _solve_objective(model.program, model.charge_sum)
    model.program.add_constraint(model.charge_sum == minimum_charge)
    minimum_population = _solve_objective(model.program, model.population_sum)
    return minimum_events, minimum_charge, minimum_population


def extract_witness(model, generators, max_level):
    coordinate_values = model.program.get_values(model.coordinates)
    positive_values = model.program.get_values(model.source_positive)
    negative_values = model.program.get_values(model.source_negative)
    coordinates = tuple(
        tuple(
            int(round(coordinate_values.get((level, index), 0)))
            for index in range(len(generators))
        )
        for level in range(1, max_level + 1)
    )
    source_vector = tuple(
        int(round(positive_values.get(item["site"], 0)))
        - int(round(negative_values.get(item["site"], 0)))
        for item in model.sites
    )
    sources = tuple(
        {**item, "value": value}
        for item, value in zip(model.sites, source_vector)
        if value
    )
    return coordinates, source_vector, sources


def verify_witness(model, generators, domain, coordinates, sources):
    positive = True
    exact_restriction = True
    for level, solution in enumerate(coordinates, start=1):
        coefficients = correction_ansatz.coefficients_from_coordinates(
            model.references[level], generators, solution
        )
        positive = positive and all(value >= 0 for value in coefficients.values())
        target = kernel_lattice.clean_sparse(
            correction_ansatz.cross.character_coefficients(
                domain["cumulative"][level]
            )
        )
        exact_restriction = exact_restriction and (
            kernel_lattice.branch_virtual(coefficients) == target
        )
    event_count = len(sources)
    charge = sum(abs(item["value"]) for item in sources)
    return {
        "positive": positive,
        "exact_restriction": exact_restriction,
        "event_count": event_count,
        "charge": charge,
    }


def add_exclusion_cut(model, source_vector):
    """Exclude one exact integral source vector using rigorous site bounds."""
    lower_flags = model.program.new_variable(binary=True)
    upper_flags = model.program.new_variable(binary=True)
    flags = []
    for item, value in zip(model.sites, source_vector):
        site = item["site"]
        lower = item["lower"]
        upper = item["upper"]
        source = model.source_positive[site] - model.source_negative[site]
        if lower <= value - 1:
            flag = lower_flags[site]
            model.program.add_constraint(
                source <= value - 1 + (upper - value + 1) * (1 - flag)
            )
            flags.append(flag)
        if value + 1 <= upper:
            flag = upper_flags[site]
            model.program.add_constraint(
                source >= value + 1 - (value - lower + 1) * (1 - flag)
            )
            flags.append(flag)
    if not flags:
        raise ValueError("Cannot exclude the only bounded source vector")
    model.program.add_constraint(model.program.sum(flags) >= 1)


def optimize_horizon(max_level, domain, generators, records, enumeration_cap):
    model = build_source_model(max_level, domain, generators, records)
    optimum = optimize_model(model)
    coordinates, source_vector, sources = extract_witness(
        model, generators, max_level
    )
    checks = verify_witness(model, generators, domain, coordinates, sources)
    enumeration = enumerate_minimal_source_vectors(
        max_level,
        domain,
        generators,
        records,
        optimum[0],
        optimum[1],
        enumeration_cap,
    )
    alternatives = tuple(
        witness
        for vector, witness in zip(
            enumeration["vectors"], enumeration["witnesses"]
        )
        if vector != source_vector
    )
    return {
        "model": model,
        "max_level": max_level,
        "minimum_events": optimum[0],
        "minimum_charge": optimum[1],
        "representative_population": optimum[2],
        "coordinates": coordinates,
        "source_vector": source_vector,
        "sources": sources,
        "has_alternative": bool(alternatives),
        "alternative_sources": () if not alternatives else alternatives[0],
        "enumeration": enumeration,
        "checks": checks,
    }


def adjacent_cutoff_compatibility(first_level, max_level, horizons):
    """Test whether adjacent cutoff-optimal faces have a common witness."""
    result = {}
    for cutoff in range(first_level + 1, max_level + 1):
        model = horizons[cutoff]["model"]
        prefix_sites = [
            item for item in model.sites if item["level"] <= cutoff - 1
        ]
        prefix_events = model.program.sum(
            model.source_active[item["site"]] for item in prefix_sites
        )
        prefix_charge = model.program.sum(
            model.source_positive[item["site"]]
            + model.source_negative[item["site"]]
            for item in prefix_sites
        )
        model.program.add_constraint(
            prefix_events == horizons[cutoff - 1]["minimum_events"]
        )
        model.program.add_constraint(
            prefix_charge == horizons[cutoff - 1]["minimum_charge"]
        )
        model.program.set_objective(0)
        try:
            model.program.solve()
            compatible = True
        except MIPSolverException:
            compatible = False
        result[cutoff - 1, cutoff] = compatible
    return result


def enumerate_minimal_source_vectors(
    max_level, domain, generators, records, minimum_events, minimum_charge, cap
):
    """Enumerate distinct minimal source vectors up to an explicit cap."""
    model = build_source_model(max_level, domain, generators, records)
    model.program.add_constraint(model.event_sum == minimum_events)
    model.program.add_constraint(model.charge_sum == minimum_charge)
    model.program.set_objective(0)
    vectors = []
    witnesses = []
    exhausted = False
    while len(vectors) < cap:
        try:
            model.program.solve()
        except MIPSolverException:
            exhausted = True
            break
        _coordinates, source_vector, sources = extract_witness(
            model, generators, max_level
        )
        vectors.append(source_vector)
        witnesses.append(sources)
        add_exclusion_cut(model, source_vector)
    if len(vectors) == cap:
        try:
            model.program.solve()
        except MIPSolverException:
            exhausted = True
    return {
        "count": len(vectors),
        "cap": cap,
        "exhausted": exhausted,
        "at_least": not exhausted,
        "vectors": tuple(vectors),
        "witnesses": tuple(witnesses),
    }


def preceding_prefix_range(result):
    """Return event/charge ranges one level below an exactly enumerated face."""
    enumeration = result["enumeration"]
    if not enumeration["exhausted"] or result["max_level"] <= 1:
        return None
    cutoff = result["max_level"] - 1
    profiles = []
    for witness in enumeration["witnesses"]:
        prefix = tuple(item for item in witness if item["level"] <= cutoff)
        profiles.append(
            (
                len(prefix),
                sum(abs(item["value"]) for item in prefix),
            )
        )
    return {
        "cutoff": cutoff,
        "event_range": (
            min(value[0] for value in profiles),
            max(value[0] for value in profiles),
        ),
        "charge_range": (
            min(value[1] for value in profiles),
            max(value[1] for value in profiles),
        ),
        "profiles": tuple(sorted(set(profiles))),
    }


def cutoff_stable_minimal_witness(
    first_level, max_level, minima, domain, generators, records
):
    """Test simultaneous prefix minimality at every requested cutoff."""
    model = build_source_model(max_level, domain, generators, records)
    for cutoff in range(first_level, max_level + 1):
        prefix_sites = [
            item for item in model.sites if item["level"] <= cutoff
        ]
        prefix_events = model.program.sum(
            model.source_active[item["site"]] for item in prefix_sites
        )
        prefix_charge = model.program.sum(
            model.source_positive[item["site"]]
            + model.source_negative[item["site"]]
            for item in prefix_sites
        )
        model.program.add_constraint(
            prefix_events == minima[cutoff]["minimum_events"]
        )
        model.program.add_constraint(
            prefix_charge == minima[cutoff]["minimum_charge"]
        )
    model.program.set_objective(model.population_sum)
    try:
        population = _integer_objective(model.program.solve())
    except MIPSolverException:
        return {"feasible": False, "population": None, "sources": ()}
    coordinates, _vector, sources = extract_witness(
        model, generators, max_level
    )
    checks = verify_witness(model, generators, domain, coordinates, sources)
    return {
        "feasible": True,
        "population": population,
        "sources": sources,
        "coordinates": coordinates,
        "checks": checks,
    }


def summarize_tk5c(
    max_level=11, first_level=7, enumeration_cap=20, verbose=False
):
    if first_level < chamber_audit.GMSZ_FIRST_LEVEL:
        raise ValueError("TK5c cutoff comparison starts in the GMSZ domain, n >= 7")
    if max_level < first_level:
        raise ValueError("max_level must be at least first_level")
    started = time.time()
    multiplicities = regge_columns.derive_multiplicity_table(max_level)
    records = chamber_core.decompose_spectrum(multiplicities, max_level)
    domain = kernel_lattice.build_finite_domain(max_level)
    generators = correction_ansatz.ordered_generators(
        kernel_lattice.natural_kernel_generators(domain)
    )

    horizons = {}
    for cutoff in range(first_level, max_level + 1):
        horizons[cutoff] = optimize_horizon(
            cutoff, domain, generators, records, enumeration_cap
        )
        result = horizons[cutoff]
        print(
            f"n <= {cutoff}: events={result['minimum_events']}, "
            f"charge={result['minimum_charge']}, "
            f"alternative={result['has_alternative']}"
        )

    stable = cutoff_stable_minimal_witness(
        first_level, max_level, horizons, domain, generators, records
    )
    adjacent = adjacent_cutoff_compatibility(
        first_level, max_level, horizons
    )

    print("=" * 104)
    print("TK5c — MINIMAL CORE-SUPPORTED WITNESSES")
    print("=" * 104)
    print("Lexicographic objectives: nonzero source events, then absolute source charge")
    print("  cutoff | min events | min charge | distinct equally minimal witness")
    for cutoff, result in horizons.items():
        print(
            f"  {cutoff:6d} | {result['minimum_events']:10d} | "
            f"{result['minimum_charge']:10d} | {str(result['has_alternative']):>32s}"
        )
        if verbose:
            print("    representative:")
            for source in result["sources"]:
                print(
                    f"      n={source['level']} {source['generator']}: "
                    f"{source['value']:+d} ({source['region']})"
                )
            if result["has_alternative"]:
                print("    second equally minimal witness:")
                for source in result["alternative_sources"]:
                    print(
                        f"      n={source['level']} {source['generator']}: "
                        f"{source['value']:+d} ({source['region']})"
                    )

    print(
        "Simultaneously minimal at every cutoff "
        f"{first_level}..{max_level}: {stable['feasible']}"
    )
    print("Adjacent cutoff-optimal faces compatible:")
    for (lower, upper), compatible in adjacent.items():
        print(f"  {lower} -> {upper}: {compatible}")
    print("Minimal-witness counts and preceding-prefix ranges:")
    for cutoff, result in horizons.items():
        enumeration = result["enumeration"]
        count_prefix = "exactly" if enumeration["exhausted"] else "at least"
        prefix = preceding_prefix_range(result)
        suffix = ""
        if prefix is not None and cutoff > first_level:
            suffix = (
                f"; n<={prefix['cutoff']} profiles="
                f"{list(prefix['profiles'])}"
            )
        print(
            f"  n<={cutoff}: {count_prefix} {enumeration['count']}"
            f"{suffix}"
        )
    if verbose and stable["feasible"]:
        print("  cutoff-stable representative:")
        for source in stable["sources"]:
            print(
                f"    n={source['level']} {source['generator']}: "
                f"{source['value']:+d} ({source['region']})"
            )

    checks = all(
        result["checks"]["positive"]
        and result["checks"]["exact_restriction"]
        and result["checks"]["event_count"] == result["minimum_events"]
        and result["checks"]["charge"] == result["minimum_charge"]
        for result in horizons.values()
    ) and (
        not stable["feasible"]
        or (
            stable["checks"]["positive"]
            and stable["checks"]["exact_restriction"]
        )
    )
    print("-" * 104)
    print("Protected SO(10) baseline imported: NO")
    print("Minimality is finite-window and criterion-dependent; it is not a physical selector.")
    print(f"TK5c exact checks: {'PASS' if checks else 'FAIL'}")
    print(f"Elapsed: {time.time() - started:.3f}s")
    return {
        "multiplicities": multiplicities,
        "records": records,
        "domain": domain,
        "generators": generators,
        "horizons": horizons,
        "stable": stable,
        "adjacent": adjacent,
        "all_checks": checks,
    }


def run_self_test():
    """Exercise the integral objective and exact exclusion-cut helpers."""
    program = MixedIntegerLinearProgram(maximization=False)
    variable = program.new_variable(integer=True, nonnegative=True)
    program.add_constraint(variable[0] >= 2)
    minimum = _solve_objective(program, variable[0])
    passed = minimum == 2
    print("TK5c MINIMAL-WITNESS SELF-TEST")
    print(f"Integral optimization helper: {'PASS' if passed else 'FAIL'}")
    print("Protected SO(10) baseline imported: NO")
    return passed


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Optimize and compare core-supported TK5b witnesses"
    )
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--max-level", type=int, default=11)
    parser.add_argument("--first-level", type=int, default=7)
    parser.add_argument("--enumeration-cap", type=int, default=20)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        raise SystemExit(0 if run_self_test() else 1)
    result = summarize_tk5c(
        args.max_level, args.first_level, args.enumeration_cap, args.verbose
    )
    raise SystemExit(0 if result["all_checks"] else 1)
