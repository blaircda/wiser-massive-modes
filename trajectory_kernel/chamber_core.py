"""TK5b: decompose the HFT spectrum into GMSZ transport and residual core.

The empirical shifts of arXiv:2609.04107 are applied in their stated order
``ell``, ``m``, ``r`` and with the largest admissible step in the first
applicable family.  This gives a deterministic partition of every observed
B4 irrep at levels n > 6 into transported data or a residual core.

The decomposition is then compared with the exact finite D5 -> B4 kernel
lattice.  Finally, a candidate source rule is tested: kernel-coordinate
sources may occur only when the corresponding B4 top weight belongs to the
residual core (with pre-chamber levels kept explicit).  No protected SO(10)
completion is imported.
"""

import argparse
import time
from collections import Counter, defaultdict
from dataclasses import dataclass

from sage.all import MixedIntegerLinearProgram
from sage.numerical.mip import MIPSolverException

from trajectory_kernel import chamber_audit
from trajectory_kernel import correction_ansatz
from trajectory_kernel import kernel_lattice
from trajectory_kernel import regge_columns
from trajectory_kernel import trajectory_selection


TRANSPORT_PRIORITY = ("ell", "m", "r")


@dataclass(frozen=True)
class TransportRecord:
    """Deterministic GMSZ provenance assigned to one nonzero B4 irrep."""

    level: int
    label: tuple
    multiplicity: int
    region: str
    steps: int | None = None
    source_level: int | None = None
    source_label: tuple | None = None
    source_multiplicity: int | None = None

    @property
    def transported(self):
        return self.region in TRANSPORT_PRIORITY

    @property
    def matches_source(self):
        return (
            not self.transported
            or self.multiplicity == self.source_multiplicity
        )


def classify_irrep(level, label, multiplicities):
    """Apply the published priority and largest-step convention literally."""
    multiplicity = multiplicities[level][label]
    if level < chamber_audit.GMSZ_FIRST_LEVEL:
        return TransportRecord(level, label, multiplicity, "pre-chamber")

    ell, m, r, s = label
    maximum = chamber_audit.ell_max(level, m, r, s)
    limits = {"ell": ell, "m": m, "r": r}
    for family in TRANSPORT_PRIORITY:
        for steps in range(limits[family], 0, -1):
            source_level, source_label = chamber_audit._source(
                family, level, label, steps
            )
            if source_level < 1:
                continue
            source_multiplicity = multiplicities[source_level].get(source_label)
            if source_multiplicity is None:
                continue
            if not chamber_audit._eligible(family, label, steps, maximum):
                continue
            return TransportRecord(
                level=level,
                label=label,
                multiplicity=multiplicity,
                region=family,
                steps=steps,
                source_level=source_level,
                source_label=source_label,
                source_multiplicity=source_multiplicity,
            )
    return TransportRecord(level, label, multiplicity, "core")


def decompose_spectrum(multiplicities, max_level):
    """Return the deterministic transport/core record for every nonzero irrep."""
    return {
        level: tuple(
            classify_irrep(level, label, multiplicities)
            for label in sorted(multiplicities[level])
        )
        for level in range(1, max_level + 1)
    }


def decomposition_statistics(records):
    """Count irreps and total multiplicities in each provenance region."""
    result = {}
    for level, level_records in records.items():
        irrep_counts = Counter(item.region for item in level_records)
        multiplicities = Counter()
        for item in level_records:
            multiplicities[item.region] += item.multiplicity
        result[level] = {
            "irrep_counts": irrep_counts,
            "multiplicities": multiplicities,
            "all_transport_matches": all(
                item.matches_source for item in level_records
            ),
        }
    return result


def _generator_family(generator):
    _ell, m, r, s = generator.top_weight
    return {
        (0, 0, 2): "A",
        (1, 0, 2): "B",
        (0, 0, 3): "C",
    }.get((m, r, s), f"({m},{r},{s})")


def shift_d5_axis(table, family, steps):
    """Shift the D5 Dynkin coordinate corresponding to a GMSZ family."""
    axis = {"ell": 0, "m": 1, "r": 2}.get(family)
    if axis is None:
        raise ValueError(f"No D5 coordinate shift for family {family}")
    result = {}
    for label, coefficient in table.items():
        shifted = list(label)
        shifted[axis] += int(steps)
        result[tuple(shifted)] = coefficient
    return kernel_lattice.clean_sparse(result)


def corrected_kernel_shift(generator, family, steps):
    """Apply a raw D5 Dynkin shift and remove its exact branching anomaly."""
    raw = shift_d5_axis(generator.as_dict(), family, steps)
    anomaly = kernel_lattice.branch_virtual(raw)
    correction = (
        kernel_lattice.chiral_section_lift(anomaly) if anomaly else {}
    )
    return kernel_lattice.add_sparse(raw, correction, scale=-1)


def generator_lineage(domain, generators, records):
    """Relate finite kernel generators to transport/core first appearances."""
    record_index = {
        (item.level, item.label): item
        for level_records in records.values()
        for item in level_records
    }
    generator_index = {generator.top_weight: generator for generator in generators}
    lineages = []
    for generator in generators:
        first_level = generator.first_hft_level
        appearance = record_index.get((first_level, generator.top_weight))
        source_generator = None
        generated_from_source = False
        if appearance.transported:
            source_generator = generator_index.get(appearance.source_label)
            if source_generator is not None:
                generated_from_source = (
                    corrected_kernel_shift(
                        source_generator, appearance.region, appearance.steps
                    )
                    == generator.as_dict()
                )
        lineages.append(
            {
                "generator": generator,
                "family": _generator_family(generator),
                "first_appearance": appearance,
                "source_generator": source_generator,
                "generated_from_source": generated_from_source,
            }
        )

    families = defaultdict(list)
    for item in lineages:
        families[item["family"]].append(item)
    contiguous = all(
        [entry["generator"].top_weight[0] for entry in sorted(
            entries, key=lambda value: value["generator"].top_weight[0]
        )] == list(range(len(entries)))
        for entries in families.values()
    )
    transported_generated = all(
        not item["first_appearance"].transported
        or (
            item["source_generator"] is not None
            and item["generated_from_source"]
        )
        for item in lineages
    )
    nontransported_seeds = tuple(
        item
        for item in lineages
        if item["first_appearance"].region in ("core", "pre-chamber")
    )
    return {
        "records": tuple(lineages),
        "families": dict(families),
        "contiguous": contiguous,
        "transported_generated": transported_generated,
        "nontransported_seeds": nontransported_seeds,
        "full_kernel_core_seed_generated": (
            contiguous and transported_generated and bool(nontransported_seeds)
        ),
    }


def _coordinate_keys(generators):
    return trajectory_selection.generator_coordinates(generators)


def _source_allowed(policy, level, generator, record_index):
    ell = generator.top_weight[0]
    if policy == "boundary-only":
        return ell == 0
    if policy == "gmsz-core":
        record = record_index.get((level, generator.top_weight))
        return record is not None and record.region in ("core", "pre-chamber")
    raise ValueError(f"Unknown kernel-source policy: {policy}")


def _add_positivity_constraints(
    program, coordinates, domain, generators, level, reference
):
    for parent in domain["parents"]:
        expression = reference.get(parent, 0) + program.sum(
            generator.as_dict().get(parent, 0) * coordinates[level, index]
            for index, generator in enumerate(generators)
            if generator.as_dict().get(parent, 0)
        )
        program.add_constraint(expression >= 0)


def source_constrained_positive_path(
    policy, max_level, domain, generators, records
):
    """Test positive cumulative lifts with sources restricted by ``policy``."""
    record_index = {
        (item.level, item.label): item
        for level_records in records.values()
        for item in level_records
    }
    keys = _coordinate_keys(generators)
    key_index = {key: index for index, key in enumerate(keys)}
    references = {
        level: correction_ansatz.reference_lift(
            domain, domain["cumulative"][level]
        )
        for level in range(1, max_level + 1)
    }

    program = MixedIntegerLinearProgram(maximization=False)
    coordinates = program.new_variable(integer=True, nonnegative=True)
    feasible_through = 0

    for level in range(1, max_level + 1):
        _add_positivity_constraints(
            program,
            coordinates,
            domain,
            generators,
            level,
            references[level],
        )
        for index, generator in enumerate(generators):
            if _source_allowed(policy, level, generator, record_index):
                continue
            ell, m, r, s = generator.top_weight
            if ell == 0 or level == 1:
                transported = 0
            else:
                predecessor = key_index.get(((m, r, s), ell - 1))
                transported = (
                    0
                    if predecessor is None
                    else coordinates[level - 1, predecessor]
                )
            program.add_constraint(coordinates[level, index] == transported)

        program.set_objective(0)
        try:
            program.solve()
        except MIPSolverException as error:
            return {
                "policy": policy,
                "feasible_through": feasible_through,
                "obstruction_level": level,
                "message": str(error),
                "solutions": (),
                "sources": (),
                "sources_valid": True,
                "positive": True,
            }
        feasible_through = level

    values = program.get_values(coordinates)
    solutions = tuple(
        tuple(
            int(round(values.get((level, index), 0)))
            for index in range(len(generators))
        )
        for level in range(1, max_level + 1)
    )
    sources = []
    previous = tuple(0 for _generator in generators)
    for level, current in enumerate(solutions, start=1):
        for index, (generator, key) in enumerate(zip(generators, keys)):
            _tail, ell = key
            if ell == 0:
                transported = 0
            else:
                predecessor = key_index.get((key[0], ell - 1))
                transported = 0 if predecessor is None else previous[predecessor]
            source = current[index] - transported
            if source:
                record = record_index.get((level, generator.top_weight))
                sources.append(
                    {
                        "level": level,
                        "generator": correction_ansatz.family_label(generator),
                        "top_weight": generator.top_weight,
                        "value": source,
                        "support_region": None if record is None else record.region,
                        "allowed": _source_allowed(
                            policy, level, generator, record_index
                        ),
                    }
                )
        previous = current

    positive = True
    exact_restriction = True
    for level, solution in enumerate(solutions, start=1):
        coefficients = correction_ansatz.coefficients_from_coordinates(
            references[level], generators, solution
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
    return {
        "policy": policy,
        "feasible_through": feasible_through,
        "obstruction_level": None,
        "message": None,
        "solutions": solutions,
        "sources": tuple(sources),
        "sources_valid": all(item["allowed"] for item in sources),
        "positive": positive,
        "exact_restriction": exact_restriction,
    }


def summarize_tk5b(max_level=11, verbose=False):
    """Run the complete baseline-free chamber/core and kernel-source audit."""
    if max_level < chamber_audit.GMSZ_FIRST_LEVEL:
        raise ValueError("TK5b needs max_level >= 7")
    started = time.time()
    multiplicities = regge_columns.derive_multiplicity_table(max_level)
    records = decompose_spectrum(multiplicities, max_level)
    statistics = decomposition_statistics(records)

    domain = kernel_lattice.build_finite_domain(max_level)
    generators = correction_ansatz.ordered_generators(
        kernel_lattice.natural_kernel_generators(domain)
    )
    lineage = generator_lineage(domain, generators, records)
    paths = {
        policy: source_constrained_positive_path(
            policy, max_level, domain, generators, records
        )
        for policy in ("boundary-only", "gmsz-core")
    }

    print("=" * 112)
    print("TK5b — GMSZ TRANSPORTED CHAMBERS, RESIDUAL CORE, AND KERNEL SOURCES")
    print("=" * 112)
    print(f"HFT levels derived: 1 through {max_level}")
    print("Transport priority: ell, then m, then r; largest admissible k first")
    print("\nSingle-level decomposition in the GMSZ domain:")
    print("  level | ell | m | r | core | total || multiplicity mass: ell/m/r/core")
    for level in range(chamber_audit.GMSZ_FIRST_LEVEL, max_level + 1):
        info = statistics[level]
        counts = info["irrep_counts"]
        mass = info["multiplicities"]
        print(
            f"  {level:5d} | {counts['ell']:3d} | {counts['m']:1d} | "
            f"{counts['r']:1d} | {counts['core']:4d} | "
            f"{sum(counts.values()):5d} || "
            f"{mass['ell']}/{mass['m']}/{mass['r']}/{mass['core']}"
        )
    all_transport_matches = all(
        statistics[level]["all_transport_matches"]
        for level in range(chamber_audit.GMSZ_FIRST_LEVEL, max_level + 1)
    )
    print(f"All selected transport identities exact: {all_transport_matches}")

    print("\nFinite restriction-kernel lineage:")
    region_counts = Counter(
        item["first_appearance"].region for item in lineage["records"]
    )
    print(f"  Kernel generators: {len(generators)}")
    print(
        "  First-appearance regions: "
        + ", ".join(f"{name}={count}" for name, count in sorted(region_counts.items()))
    )
    for family, entries in sorted(lineage["families"].items()):
        ordered = sorted(entries, key=lambda item: item["generator"].top_weight[0])
        seed = ordered[0]
        print(
            f"  Family {family}: ell=0..{ordered[-1]['generator'].top_weight[0]}, "
            f"seed first n={seed['generator'].first_hft_level} "
            f"({seed['first_appearance'].region})"
        )
    print(
        "  Every transported generator is the exact corrected GMSZ shift of its source: "
        f"{lineage['transported_generated']}"
    )
    print(
        "  Nontransported kernel seeds: "
        + ", ".join(
            correction_ansatz.family_label(item["generator"])
            for item in lineage["nontransported_seeds"]
        )
    )
    print(
        "  Full finite kernel generated from nontransported seeds: "
        f"{lineage['full_kernel_core_seed_generated']}"
    )

    print("\nPositive cumulative lifts with constrained coordinate sources:")
    for policy, result in paths.items():
        print(
            f"  {policy}: feasible through n={result['feasible_through']}, "
            f"obstruction={result['obstruction_level']}"
        )
        if result["obstruction_level"] is None:
            charge = sum(abs(item["value"]) for item in result["sources"])
            print(
                f"    one non-minimized witness: nonzero sources={len(result['sources'])}, "
                f"absolute charge={charge}, sources valid={result['sources_valid']}, "
                f"lifts positive={result['positive']}, "
                f"restrictions exact={result['exact_restriction']}"
            )
            if verbose:
                for source in result["sources"]:
                    print(f"    {source}")

    all_checks = (
        all_transport_matches
        and lineage["full_kernel_core_seed_generated"]
        and paths["gmsz-core"]["feasible_through"] == max_level
        and paths["gmsz-core"]["sources_valid"]
        and paths["gmsz-core"]["positive"]
        and paths["gmsz-core"]["exact_restriction"]
    )
    print("-" * 112)
    print("Protected SO(10) baseline imported: NO")
    print("GMSZ transport remains empirical; the source rule is a tested candidate, not a theorem.")
    print(f"TK5b finite checks: {'PASS' if all_checks else 'FAIL'}")
    print(f"Elapsed: {time.time() - started:.3f}s")
    return {
        "multiplicities": multiplicities,
        "records": records,
        "statistics": statistics,
        "domain": domain,
        "generators": generators,
        "lineage": lineage,
        "paths": paths,
        "all_transport_matches": all_transport_matches,
        "all_checks": all_checks,
    }


def run_self_test():
    """Check priority classification on a small synthetic chamber."""
    multiplicities = {
        level: {} for level in range(1, 8)
    }
    multiplicities[6][(0, 0, 0, 2)] = 1
    multiplicities[7][(1, 0, 0, 2)] = 1
    multiplicities[7][(0, 0, 0, 2)] = 2
    shifted = classify_irrep(7, (1, 0, 0, 2), multiplicities)
    core = classify_irrep(7, (0, 0, 0, 2), multiplicities)
    checks = (
        shifted.region == "ell",
        shifted.steps == 1,
        shifted.source_level == 6,
        shifted.matches_source,
        core.region == "core",
    )
    passed = all(checks)
    print("TK5b CHAMBER/CORE SELF-TEST")
    print(f"Priority and residual-core conventions: {'PASS' if passed else 'FAIL'}")
    print("Protected SO(10) baseline imported: NO")
    return passed


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Decompose GMSZ transport chambers and test kernel sources"
    )
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--max-level", type=int, default=11)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        raise SystemExit(0 if run_self_test() else 1)
    result = summarize_tk5b(args.max_level, args.verbose)
    raise SystemExit(0 if result["all_checks"] else 1)
