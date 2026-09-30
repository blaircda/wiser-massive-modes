"""TK6B.4: exact positive circuits of universal all-split shell systems.

TK6B.3 gives every natural D5 -> B4 restriction-kernel relation in closed
form.  This module builds finite collision hypergraphs directly from those
relations, transposes them to their Gale row configurations, and enumerates
the primitive positive circuits

    x >= 0,  G^T x = 0.

The construction is independent of protected SO(10) completions.  Synthetic
top-weight boxes test the branching structure without waiting for those
weights to occur in the HFT spectrum.  Actual HFT closures can be analyzed as
a separate comparison.
"""

import argparse
import math
import sys
import time
from collections import Counter, defaultdict

from sage.all import Polyhedron, QQ, ZZ, lcm, matrix, vector

from trajectory_kernel import boundary_shell
from trajectory_kernel import kernel_lattice
from trajectory_kernel import restriction_semigroup


def top_weight_box(max_ell=0, max_m=0, max_r=0, max_s=4, min_s=2):
    """Return a rectangular finite family of ambiguous B4 top weights."""
    bounds = (max_ell, max_m, max_r, max_s)
    if any(value not in ZZ for value in bounds) or min_s not in ZZ:
        raise ValueError("Synthetic box bounds must be integers")
    max_ell, max_m, max_r, max_s, min_s = map(
        int, (max_ell, max_m, max_r, max_s, min_s)
    )
    if min(max_ell, max_m, max_r) < 0:
        raise ValueError("Synthetic Dynkin-label bounds must be nonnegative")
    if min_s < 2 or max_s < min_s:
        raise ValueError("Require 2 <= min_s <= max_s")
    return tuple(
        (ell, m, r, s)
        for ell in range(max_ell + 1)
        for m in range(max_m + 1)
        for r in range(max_r + 1)
        for s in range(min_s, max_s + 1)
    )


def all_split_relations(top_weights):
    """Return every natural all-chiral-section relation over ``top_weights``."""
    relations = {}
    for top_weight in sorted(set(tuple(weight) for weight in top_weights)):
        _ell, _m, _r, s = top_weight
        if min(top_weight) < 0 or s < 2:
            raise ValueError(f"Not an ambiguous dominant B4 weight: {top_weight}")
        for split in range(1, s // 2 + 1):
            name = (top_weight, split)
            relations[name] = boundary_shell.natural_split_relation(
                top_weight, split
            )
    return relations


def gale_configuration(relations, parent_universe=()):
    """Transpose sparse kernel relations and group identical Gale rows."""
    names = tuple(relations)
    coefficients = defaultdict(dict)
    for name, relation in relations.items():
        for parent, coefficient in relation.items():
            coefficients[tuple(parent)][name] = int(coefficient)
    for parent in parent_universe:
        coefficients.setdefault(tuple(parent), {})

    parent_rows = {}
    row_parents = defaultdict(list)
    for parent in sorted(coefficients):
        table = coefficients[parent]
        row = tuple(int(table.get(name, 0)) for name in names)
        parent_rows[parent] = row
        row_parents[row].append(parent)

    unique_rows = tuple(sorted(row_parents))
    return {
        "names": names,
        "parent_rows": parent_rows,
        "row_parents": {
            row: tuple(parents) for row, parents in row_parents.items()
        },
        "unique_rows": unique_rows,
        "row_type_counts": Counter(parent_rows.values()),
    }


def _primitive_nonnegative_ray(ray):
    """Convert one exact rational cone ray to a primitive integer tuple."""
    denominators = [QQ(value).denominator() for value in ray]
    common = int(lcm(denominators)) if denominators else 1
    integral = [int(QQ(value) * common) for value in ray]
    content = 0
    for value in integral:
        content = math.gcd(content, abs(value))
    if content == 0:
        raise ValueError("A positive-circuit ray cannot vanish")
    primitive = tuple(value // content for value in integral)
    if any(value < 0 for value in primitive):
        raise ValueError("Positive-circuit cone returned a negative coordinate")
    return primitive


def positive_circuits(unique_rows):
    """Enumerate primitive extreme rays of ``x>=0, G^T x=0`` exactly."""
    rows = tuple(tuple(int(value) for value in row) for row in unique_rows)
    if not rows:
        return {
            "matrix": matrix(ZZ, 0, 0),
            "cone": None,
            "circuits": (),
        }
    rank = len(rows[0])
    if any(len(row) != rank for row in rows):
        raise ValueError("Gale row vectors must have a common rank")
    gale = matrix(ZZ, rows)
    count = len(rows)
    inequalities = tuple(
        tuple([0] + [1 if index == position else 0 for index in range(count)])
        for position in range(count)
    )
    equations = tuple(
        tuple([0] + [rows[index][coordinate] for index in range(count)])
        for coordinate in range(rank)
    )
    cone = Polyhedron(
        ieqs=inequalities,
        eqns=equations,
        base_ring=QQ,
        backend="ppl",
    )
    if cone.lines_list():
        raise ValueError("A nonnegative circuit cone cannot contain a line")
    circuits = tuple(
        sorted(_primitive_nonnegative_ray(ray) for ray in cone.rays_list())
    )
    for circuit in circuits:
        column = matrix(ZZ, len(circuit), 1, circuit)
        if gale.transpose() * column != 0:
            raise ValueError("Enumerated positive circuit is not a Gale relation")
    return {
        "matrix": gale,
        "cone": cone,
        "circuits": circuits,
    }


def circuit_diagnostics(configuration):
    """Summarize exact circuit supports and primitive coefficient sizes."""
    rows = configuration["unique_rows"]
    enumeration = positive_circuits(rows)
    circuits = enumeration["circuits"]
    support_histogram = Counter()
    maximum_coefficient_histogram = Counter()
    coefficient_pattern_histogram = Counter()
    nonunit = []
    all_support_minimal = True
    for circuit in circuits:
        support = tuple(index for index, value in enumerate(circuit) if value)
        coefficients = tuple(circuit[index] for index in support)
        supported_rows = matrix(ZZ, [rows[index] for index in support])
        all_support_minimal = all_support_minimal and (
            supported_rows.rank() == len(support) - 1
        )
        support_histogram[len(support)] += 1
        maximum_coefficient_histogram[max(coefficients)] += 1
        coefficient_pattern_histogram[tuple(sorted(coefficients))] += 1
        if max(coefficients) > 1:
            nonunit.append(
                {
                    "circuit": circuit,
                    "terms": tuple(
                        (rows[index], circuit[index]) for index in support
                    ),
                    "parents": tuple(
                        configuration["row_parents"][rows[index]]
                        for index in support
                    ),
                }
            )
    return {
        "enumeration": enumeration,
        "circuit_count": len(circuits),
        "support_histogram": dict(sorted(support_histogram.items())),
        "maximum_coefficient_histogram": dict(
            sorted(maximum_coefficient_histogram.items())
        ),
        "coefficient_pattern_histogram": dict(
            sorted(coefficient_pattern_histogram.items())
        ),
        "all_coefficients_unit": not nonunit,
        "all_supports_minimal": all_support_minimal,
        "nonunit_circuits": tuple(nonunit),
    }


def analyze_top_weights(top_weights, parent_universe=()):
    """Classify the all-split collision system over an explicit top set."""
    top_weights = tuple(sorted(set(tuple(weight) for weight in top_weights)))
    relations = all_split_relations(top_weights)
    configuration = gale_configuration(
        relations, parent_universe=parent_universe
    )
    circuits = circuit_diagnostics(configuration)
    relation_checks = tuple(
        not kernel_lattice.branch_virtual(relation)
        for relation in relations.values()
    )
    return {
        "top_weights": top_weights,
        "relations": relations,
        "configuration": configuration,
        "circuits": circuits,
        "all_relations_null": all(relation_checks),
    }


def analyze_synthetic_box(
    max_ell=0,
    max_m=0,
    max_r=0,
    max_s=4,
    min_s=2,
):
    """Build and classify one exact synthetic all-split collision system."""
    top_weights = top_weight_box(
        max_ell=max_ell,
        max_m=max_m,
        max_r=max_r,
        max_s=max_s,
        min_s=min_s,
    )
    result = analyze_top_weights(top_weights)
    result["bounds"] = (max_ell, max_m, max_r, min_s, max_s)
    return result


def sparse_gale_row(row, names):
    """Return one Gale row as named nonzero kernel coordinates."""
    return tuple(
        (name, int(value))
        for name, value in zip(names, row)
        if value
    )


def compact_circuit_certificate(item, configuration):
    """Return a readable exact non-unit positive-circuit certificate."""
    names = configuration["names"]
    terms = []
    for (row, coefficient), parents in zip(item["terms"], item["parents"]):
        terms.append(
            {
                "coefficient": coefficient,
                "gale_row": sparse_gale_row(row, names),
                "representative_parent": parents[0],
                "row_multiplicity": len(parents),
            }
        )
    return {
        "support": len(terms),
        "coefficient_mass": sum(term["coefficient"] for term in terms),
        "maximum_coefficient": max(term["coefficient"] for term in terms),
        "terms": tuple(terms),
    }


def minimal_nonunit_certificate(result):
    """Return the smallest non-unit circuit in one analysis, if present."""
    nonunit = result["circuits"]["nonunit_circuits"]
    if not nonunit:
        return None
    item = min(
        nonunit,
        key=lambda entry: (
            sum(value != 0 for value in entry["circuit"]),
            sum(entry["circuit"]),
            entry["circuit"],
        ),
    )
    return compact_circuit_certificate(item, result["configuration"])


def circuit_target_diagnostics(domain, packets, configuration, circuits, level):
    """Test every expanded weighted-circuit inequality on one HFT target.

    A circuit of distinct Gale row types lifts by choosing one actual parent
    realizing each supported type.  Its facet value is the weighted sum of
    the triangular all-chiral coordinates on the chosen reference parents.
    The choices are independent, so minimizing type by type tests every
    expanded facet without explicitly listing them.
    """
    reference_parents, reference = restriction_semigroup.reference_matrix(domain)
    determinant = int(reference.det())
    if abs(determinant) != 1:
        raise ValueError("All-chiral reference matrix is not unimodular")
    target = restriction_semigroup.target_vector(domain, level)
    coordinates_raw = reference.solve_right(vector(ZZ, target))
    if any(value not in ZZ for value in coordinates_raw):
        raise ValueError("Triangular section coordinates are not integral")
    coordinates = tuple(int(value) for value in coordinates_raw)
    coordinate_by_parent = dict(zip(reference_parents, coordinates))

    rows = configuration["unique_rows"]
    row_parents = configuration["row_parents"]
    minimum_slacks = []
    worst_choices = []
    expanded_count = 0
    for circuit in circuits:
        slack = 0
        choice = []
        multiplicity = 1
        for index, coefficient in enumerate(circuit):
            if not coefficient:
                continue
            parents = row_parents[rows[index]]
            multiplicity *= len(parents)
            candidates = tuple(
                (
                    coefficient * coordinate_by_parent.get(parent, 0),
                    parent,
                    parent in coordinate_by_parent,
                )
                for parent in parents
            )
            selected = min(candidates)
            slack += selected[0]
            choice.append(
                {
                    "coefficient": coefficient,
                    "row": rows[index],
                    "parent": selected[1],
                    "is_reference": selected[2],
                    "contribution": selected[0],
                }
            )
        expanded_count += multiplicity
        minimum_slacks.append(slack)
        worst_choices.append(tuple(choice))

    minimum = min(minimum_slacks, default=0)
    worst_index = (
        None if not minimum_slacks else minimum_slacks.index(minimum)
    )
    return {
        "level": level,
        "target": target,
        "reference_determinant": determinant,
        "coordinates": coordinates,
        "negative_coordinates": sum(value < 0 for value in coordinates),
        "minimum_coordinate": min(coordinates, default=0),
        "expanded_circuit_count": expanded_count,
        "minimum_slacks": tuple(minimum_slacks),
        "minimum_slack": minimum,
        "violated_circuit_types": sum(value < 0 for value in minimum_slacks),
        "all_circuit_inequalities": all(value >= 0 for value in minimum_slacks),
        "worst_choice": () if worst_index is None else worst_choices[worst_index],
    }


def analyze_hft_closure(max_level=12):
    """Classify circuits in one complete baseline-free HFT branching closure."""
    if max_level < 1:
        raise ValueError("HFT circuit analysis requires max_level >= 1")
    domain = kernel_lattice.build_finite_domain(max_level)
    top_weights = tuple(weight for weight, _family in domain["ambiguous"])
    result = analyze_top_weights(
        top_weights, parent_universe=domain["parents"]
    )
    configuration = result["configuration"]
    gale = matrix(
        ZZ,
        [configuration["parent_rows"][parent] for parent in domain["parents"]],
    )
    packets = matrix(
        ZZ,
        len(domain["weights"]),
        len(domain["parents"]),
        lambda row, column: domain["branch_tables"][
            domain["parents"][column]
        ].get(domain["weights"][row], 0),
    )
    expected_nullity = len(domain["parents"]) - packets.rank()
    full_kernel_basis = (
        packets * gale == 0
        and gale.rank() == expected_nullity
        and gale.ncols() == expected_nullity
    )
    target_checks = circuit_target_diagnostics(
        domain,
        packets,
        configuration,
        result["circuits"]["enumeration"]["circuits"],
        max_level,
    )
    packet_witness = restriction_semigroup.integral_packet_witness(
        packets, target_checks["target"]
    )
    result.update(
        {
            "max_level": max_level,
            "domain": domain,
            "packets": packets,
            "gale": gale,
            "full_kernel_basis": full_kernel_basis,
            "target_checks": target_checks,
            "packet_witness": packet_witness,
        }
    )
    return result


def run_analysis(
    max_ell=0,
    max_m=0,
    max_r=0,
    max_s=4,
    min_s=2,
    verbose=False,
):
    """Print one reproducible synthetic TK6B.4 circuit audit."""
    started = time.time()
    result = analyze_synthetic_box(
        max_ell=max_ell,
        max_m=max_m,
        max_r=max_r,
        max_s=max_s,
        min_s=min_s,
    )
    configuration = result["configuration"]
    circuits = result["circuits"]
    print("=" * 104)
    print("TK6B.4 — UNIVERSAL ALL-SPLIT POSITIVE-CIRCUIT AUDIT")
    print("=" * 104)
    print(f"Synthetic top-weight bounds: {result['bounds']}")
    print(f"Top weights: {len(result['top_weights'])}")
    print(f"Natural kernel coordinates: {len(result['relations'])}")
    print(f"Parent rows: {len(configuration['parent_rows'])}")
    print(f"Distinct Gale row types: {len(configuration['unique_rows'])}")
    print(f"Primitive positive circuits: {circuits['circuit_count']}")
    print(f"Circuit support histogram: {circuits['support_histogram']}")
    print(
        "Maximum circuit-coefficient histogram: "
        f"{circuits['maximum_coefficient_histogram']}"
    )
    print(f"All circuit coefficients unit: {circuits['all_coefficients_unit']}")
    print(f"Every circuit support minimal: {circuits['all_supports_minimal']}")
    certificate = minimal_nonunit_certificate(result)
    if certificate is not None:
        print(
            "Smallest non-unit certificate: "
            f"support={certificate['support']}, "
            f"mass={certificate['coefficient_mass']}, "
            f"maximum={certificate['maximum_coefficient']}"
        )
        if verbose:
            for term in certificate["terms"]:
                print(
                    f"  {term['coefficient']} * {term['gale_row']} "
                    f"at parent {term['representative_parent']} "
                    f"(row multiplicity {term['row_multiplicity']})"
                )
    print(f"All shell relations branch to zero: {result['all_relations_null']}")
    print("Protected SO(10) baseline imported: NO")
    print(f"Runtime: {time.time() - started:.3f}s")
    result["all_checks"] = (
        result["all_relations_null"] and circuits["all_supports_minimal"]
    )
    return result


def run_hft_analysis(max_level=12, verbose=False):
    """Print a circuit audit for one actual baseline-free HFT closure."""
    started = time.time()
    result = analyze_hft_closure(max_level=max_level)
    domain = result["domain"]
    configuration = result["configuration"]
    circuits = result["circuits"]
    print("=" * 104)
    print("TK6B.4 — HFT-CLOSURE ALL-SPLIT POSITIVE-CIRCUIT AUDIT")
    print("=" * 104)
    print(f"HFT horizon: {max_level}")
    print(f"B4 rows: {len(domain['weights'])}")
    print(f"Parent packets: {len(domain['parents'])}")
    print(f"Natural kernel coordinates: {len(result['relations'])}")
    print(f"Distinct Gale row types: {len(configuration['unique_rows'])}")
    print(f"Primitive positive-circuit types: {circuits['circuit_count']}")
    print(f"Circuit support histogram: {circuits['support_histogram']}")
    print(
        "Maximum circuit-coefficient histogram: "
        f"{circuits['maximum_coefficient_histogram']}"
    )
    print(f"All circuit coefficients unit: {circuits['all_coefficients_unit']}")
    print(f"Every circuit support minimal: {circuits['all_supports_minimal']}")
    print(f"Closed formulas give the full kernel basis: {result['full_kernel_basis']}")
    target = result["target_checks"]
    witness = result["packet_witness"]
    print(f"Expanded actual circuits/facets: {target['expanded_circuit_count']}")
    print(
        "Triangular coordinates: "
        f"negative={target['negative_coordinates']}, "
        f"minimum={target['minimum_coordinate']}"
    )
    print(
        "Weighted circuit inequalities on the cumulative target: "
        f"minimum={target['minimum_slack']}, "
        f"violated types={target['violated_circuit_types']}"
    )
    print(
        "Exact nonnegative integral packet witness found: "
        f"{witness['feasible'] and witness['exact']}"
    )
    certificate = minimal_nonunit_certificate(result)
    if certificate is not None:
        print(
            "Smallest non-unit certificate: "
            f"support={certificate['support']}, "
            f"mass={certificate['coefficient_mass']}, "
            f"maximum={certificate['maximum_coefficient']}"
        )
        if verbose:
            for term in certificate["terms"]:
                print(
                    f"  {term['coefficient']} * {term['gale_row']} "
                    f"at parent {term['representative_parent']} "
                    f"(row multiplicity {term['row_multiplicity']})"
                )
    print("Protected SO(10) baseline imported: NO")
    print(f"Runtime: {time.time() - started:.3f}s")
    result["all_checks"] = (
        result["all_relations_null"]
        and result["full_kernel_basis"]
        and circuits["all_supports_minimal"]
        and target["all_circuit_inequalities"]
        and witness["feasible"]
        and witness["exact"]
    )
    return result


def run_self_test():
    """Check circuit enumeration on a known coefficient-two configuration."""
    rows = ((1, 1), (-1, 1), (0, -1))
    result = positive_circuits(rows)
    expected = ((1, 1, 2),)
    if result["circuits"] != expected:
        raise AssertionError(
            f"Synthetic non-unit circuit mismatch: {result['circuits']}"
        )
    shell = analyze_synthetic_box(max_s=4)
    if not shell["all_relations_null"]:
        raise AssertionError("Universal shell relation failed exact branching")
    first_split_box = analyze_synthetic_box(
        max_ell=1, max_m=1, max_s=3
    )
    if not first_split_box["circuits"]["all_coefficients_unit"]:
        raise AssertionError("The s <= 3 control box unexpectedly became non-unit")
    obstruction = analyze_synthetic_box(
        max_ell=1, max_m=1, max_s=4
    )
    if obstruction["circuits"]["maximum_coefficient_histogram"] != {
        1: 398,
        2: 41,
    }:
        raise AssertionError("The all-split coefficient-two obstruction changed")
    certificate = minimal_nonunit_certificate(obstruction)
    if certificate is None or certificate["support"] != 9:
        raise AssertionError("The minimal all-split obstruction was not recovered")
    print("TK6B.4 ALL-SPLIT CIRCUIT SELF-TEST")
    print("  Primitive coefficient-two circuit: PASS")
    print("  Synthetic all-split shell system: PASS")
    print("  Unit s <= 3 control box: PASS")
    print("  Coefficient-two s <= 4 obstruction: PASS")
    print("  Protected SO(10) baseline imported: NO")
    return True


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Enumerate exact circuits of synthetic all-split Gale rows"
    )
    parser.add_argument("--max-ell", type=int, default=0)
    parser.add_argument("--max-m", type=int, default=0)
    parser.add_argument("--max-r", type=int, default=0)
    parser.add_argument("--min-s", type=int, default=2)
    parser.add_argument("--max-s", type=int, default=4)
    parser.add_argument("--hft-level", type=int)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.self_test:
            return 0 if run_self_test() else 1
        if args.hft_level is None:
            result = run_analysis(
                max_ell=args.max_ell,
                max_m=args.max_m,
                max_r=args.max_r,
                min_s=args.min_s,
                max_s=args.max_s,
                verbose=args.verbose,
            )
        else:
            result = run_hft_analysis(
                max_level=args.hft_level, verbose=args.verbose
            )
    except Exception as error:
        print(f"TK6B.4 FAILED: {error}", file=sys.stderr)
        return 1
    return 0 if result["all_checks"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
