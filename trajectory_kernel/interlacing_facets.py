"""TK6B.2: classify finite D5 -> B4 packet-cone facets.

TK6B.1 proves that the complete baseline-free level-11 packet semigroup is
saturated.  Positive integral liftability in that finite closure is therefore
equivalent to the rational facet inequalities.  This module asks whether those
facets organize into stable families under Dynkin-label translations and under
growth of the HFT horizon.

The calculation is baseline-free.  It imports no protected SO(10) completion.
Finite proliferation or failure of shift covariance is reported as an
obstruction rather than replaced by a fitted template.
"""

import argparse
import math
import sys
import time
from collections import Counter

from sage.all import ZZ, matrix

import finite_cross_section as cross
from trajectory_kernel import correction_ansatz
from trajectory_kernel import kernel_lattice
from trajectory_kernel import restriction_semigroup


AXIS_NAMES = ("ell", "m", "r", "s")


def build_nested_domain(master_domain, horizon):
    """Build the full branching closure through one nested HFT horizon."""
    cumulative = {
        level: master_domain["cumulative"][level]
        for level in range(1, horizon + 1)
    }
    weights = kernel_lattice.section_search.full_family_closure(cumulative)
    branch_tables = kernel_lattice.section_search.prepare_branch_tables(weights)
    parents = tuple(sorted(branch_tables))
    ambiguous = tuple(
        (weight, cross.positive_chirality_parent_family(weight))
        for weight in weights
        if len(cross.positive_chirality_parent_family(weight)) > 1
    )
    if not set(weights).issubset(master_domain["weights"]):
        raise ValueError("Nested B4 closure is not contained in master closure")
    if not set(parents).issubset(master_domain["parents"]):
        raise ValueError("Nested D5 packet family is not contained in master closure")
    return {
        "single_levels": {
            level: master_domain["single_levels"][level]
            for level in range(1, horizon + 1)
        },
        "cumulative": cumulative,
        "weights": weights,
        "branch_tables": branch_tables,
        "parents": parents,
        "ambiguous": ambiguous,
        "first_occurrence": kernel_lattice.first_occurrence_levels(cumulative),
    }


def _primitive_coefficients(coefficients):
    """Divide a nonzero integral facet normal by its positive content."""
    content = 0
    for coefficient in coefficients:
        content = math.gcd(content, abs(int(coefficient)))
    if content == 0:
        raise ValueError("Facet normal cannot vanish")
    return tuple(int(coefficient) // content for coefficient in coefficients)


def facet_table(weights, inequality):
    """Return one homogeneous facet as a canonical sparse label table."""
    if inequality[0] != 0:
        raise ValueError("Packet-cone facets must be homogeneous")
    coefficients = _primitive_coefficients(inequality[1:])
    return tuple(
        sorted(
            (tuple(weight), coefficient)
            for weight, coefficient in zip(weights, coefficients)
            if coefficient
        )
    )


def shift_facet_table(table, shift):
    """Translate every B4 label in a sparse facet by one vector."""
    if len(shift) != 4:
        raise ValueError("B4 facet shifts require four coordinates")
    shifted = []
    for label, coefficient in table:
        new_label = tuple(value + step for value, step in zip(label, shift))
        if min(new_label) < 0:
            return None
        shifted.append((new_label, coefficient))
    return tuple(sorted(shifted))


def translation_signature(table, axes=(0, 1, 2, 3)):
    """Canonicalize a facet modulo common translations in selected axes."""
    minima = {
        axis: min(label[axis] for label, _coefficient in table)
        for axis in axes
    }
    normalized = []
    for label, coefficient in table:
        relative = tuple(
            value - minima.get(axis, 0)
            for axis, value in enumerate(label)
        )
        normalized.append((relative, coefficient))
    return tuple(sorted(normalized))


def facet_morphology(facet_tables):
    """Summarize support, signs and coefficient sizes of exact facets."""
    support_histogram = Counter()
    maximum_coefficient_histogram = Counter()
    positive_terms_histogram = Counter()
    negative_terms_histogram = Counter()
    coefficient_sum_histogram = Counter()
    pure_nonnegative = 0
    mixed_sign = 0

    for table in facet_tables:
        coefficients = tuple(coefficient for _label, coefficient in table)
        support_histogram[len(table)] += 1
        maximum_coefficient_histogram[max(abs(value) for value in coefficients)] += 1
        positive_terms_histogram[sum(value > 0 for value in coefficients)] += 1
        negative_terms_histogram[sum(value < 0 for value in coefficients)] += 1
        coefficient_sum_histogram[sum(coefficients)] += 1
        if all(value >= 0 for value in coefficients):
            pure_nonnegative += 1
        else:
            mixed_sign += 1

    return {
        "support_histogram": dict(sorted(support_histogram.items())),
        "maximum_coefficient_histogram": dict(
            sorted(maximum_coefficient_histogram.items())
        ),
        "positive_terms_histogram": dict(sorted(positive_terms_histogram.items())),
        "negative_terms_histogram": dict(sorted(negative_terms_histogram.items())),
        "coefficient_sum_histogram": dict(sorted(coefficient_sum_histogram.items())),
        "pure_nonnegative": pure_nonnegative,
        "mixed_sign": mixed_sign,
        "zero_sum": coefficient_sum_histogram.get(0, 0),
    }


def shift_orbit_diagnostics(facet_tables, weights, axis):
    """Classify exact one-step translation edges along one Dynkin axis."""
    facet_set = set(facet_tables)
    weight_set = set(weights)
    forward_shift = tuple(1 if index == axis else 0 for index in range(4))
    backward_shift = tuple(-value for value in forward_shift)
    successor = {}
    predecessor = {}
    forward_eligible = 0
    backward_eligible = 0

    for table in facet_tables:
        forward = shift_facet_table(table, forward_shift)
        if forward is not None and all(label in weight_set for label, _ in forward):
            forward_eligible += 1
            if forward in facet_set:
                successor[table] = forward
        backward = shift_facet_table(table, backward_shift)
        if backward is not None and all(label in weight_set for label, _ in backward):
            backward_eligible += 1
            if backward in facet_set:
                predecessor[table] = backward

    if any(predecessor.get(target) != source for source, target in successor.items()):
        raise ValueError("Facet shift predecessor/successor maps disagree")

    seeds = tuple(table for table in facet_tables if table not in predecessor)
    orbit_lengths = []
    covered = set()
    for seed in seeds:
        current = seed
        length = 0
        while current is not None and current not in covered:
            covered.add(current)
            length += 1
            current = successor.get(current)
        orbit_lengths.append(length)

    return {
        "axis": AXIS_NAMES[axis],
        "forward_eligible": forward_eligible,
        "forward_matches": len(successor),
        "backward_eligible": backward_eligible,
        "backward_matches": len(predecessor),
        "eligible_match_fraction": (
            None if not forward_eligible else len(successor) / forward_eligible
        ),
        "seeds": len(seeds),
        "nontrivial_orbits": sum(length > 1 for length in orbit_lengths),
        "maximum_orbit_length": max(orbit_lengths, default=0),
        "orbit_length_histogram": dict(sorted(Counter(orbit_lengths).items())),
        "all_facets_covered": len(covered) == len(facet_tables),
    }


def packet_slack_diagnostics(facet_tables, weights, domain):
    """Count packet rays on and off each facet wall."""
    parent_tables = domain["branch_tables"]
    positive_ray_histogram = Counter()
    maximum_slack_histogram = Counter()
    minimum_tight_rays = None
    maximum_tight_rays = None
    for table in facet_tables:
        functional = dict(table)
        slacks = tuple(
            sum(
                functional.get(weight, 0) * multiplicity
                for weight, multiplicity in parent_tables[parent].items()
            )
            for parent in domain["parents"]
        )
        if any(value < 0 for value in slacks):
            raise ValueError("Facet functional is negative on a packet ray")
        positive = sum(value > 0 for value in slacks)
        tight = len(slacks) - positive
        positive_ray_histogram[positive] += 1
        maximum_slack_histogram[max(slacks, default=0)] += 1
        minimum_tight_rays = tight if minimum_tight_rays is None else min(
            minimum_tight_rays, tight
        )
        maximum_tight_rays = tight if maximum_tight_rays is None else max(
            maximum_tight_rays, tight
        )
    return {
        "positive_ray_histogram": dict(sorted(positive_ray_histogram.items())),
        "maximum_slack_histogram": dict(sorted(maximum_slack_histogram.items())),
        "minimum_tight_rays": minimum_tight_rays,
        "maximum_tight_rays": maximum_tight_rays,
    }


def expected_abc_gale_types(generator_names):
    """Return the compact A/B/C Gale-row template set.

    TK6B.3 proves this template for arbitrary lengths of the three named
    chains, but also shows that the actual HFT closure acquires additional
    kernel families at level 12.  This helper therefore describes the
    A/B/C-only subsystem, not an all-orders completeness conjecture.
    """
    parsed = {}
    for position, name in enumerate(generator_names):
        if not name or name[0] not in "ABC" or not name[1:].isdigit():
            return None
        parsed[name] = position

    rank = len(generator_names)

    def sparse(entries):
        vector = [0] * rank
        for name, coefficient in entries.items():
            if name not in parsed:
                return None
            vector[parsed[name]] = coefficient
        return tuple(
            (generator_names[index], value)
            for index, value in enumerate(vector)
            if value
        )

    result = {()}
    for name in generator_names:
        result.add(sparse({name: 1}))
        result.add(sparse({name: -1}))

    a_names = sorted(
        (name for name in generator_names if name.startswith("A")),
        key=lambda name: int(name[1:]),
    )
    b_names = sorted(
        (name for name in generator_names if name.startswith("B")),
        key=lambda name: int(name[1:]),
    )
    c_names = sorted(
        (name for name in generator_names if name.startswith("C")),
        key=lambda name: int(name[1:]),
    )
    if a_names:
        result.add(sparse({name: 1 for name in a_names}))
    if b_names:
        entries = {name: 1 for name in b_names}
        entries["A0"] = -1
        result.add(sparse(entries))
        for name in b_names:
            ell = int(name[1:])
            successor = f"A{ell + 1}"
            if successor in parsed:
                result.add(sparse({name: -1, successor: -1}))
    if c_names:
        result.add(sparse({name: 1 for name in c_names}))
    return result


def gale_circuit_diagnostics(classification):
    """Express every facet as a positive circuit of the kernel Gale rows.

    If ``A`` is the packet matrix and ``K`` is a basis matrix for its kernel,
    the packet slacks of a facet lie in

        ker(K^T) intersect R_{>=0}^{packets}.

    Extreme rays of this cone are positive circuits of the Gale row vectors.
    """
    domain = classification["domain"]
    packets = classification["packets"]
    generators = correction_ansatz.ordered_generators(
        kernel_lattice.natural_kernel_generators(domain)
    )
    parents = domain["parents"]
    gale = matrix(
        ZZ,
        len(parents),
        len(generators),
        lambda row, column: generators[column].as_dict().get(
            parents[row], 0
        ),
    )
    if packets * gale != 0:
        raise ValueError("Natural kernel generators do not give a Gale matrix")
    if gale.rank() != len(generators):
        raise ValueError("Gale matrix does not have full kernel rank")

    generator_names = tuple(
        correction_ansatz.family_label(generator)
        for generator in generators
    )
    gale_rows = tuple(
        tuple(int(value) for value in gale.row(row))
        for row in range(gale.nrows())
    )
    gale_row_signatures = tuple(
        tuple(
            (name, value)
            for name, value in zip(generator_names, row)
            if value
        )
        for row in gale_rows
    )
    row_type_counts = Counter(gale_row_signatures)
    zero = ()
    unique_type_classes = Counter()
    for row_type in row_type_counts:
        nonzero = tuple(value for _name, value in row_type)
        if not nonzero:
            unique_type_classes["zero"] += 1
        elif len(nonzero) == 1 and abs(nonzero[0]) == 1:
            unique_type_classes["signed-coordinate"] += 1
        else:
            unique_type_classes["composite"] += 1

    circuit_type_counts = Counter()
    circuit_support_histogram = Counter()
    circuit_coefficient_histogram = Counter()
    reference_support_histogram = Counter()
    reference_supports = set()
    all_kernel_relations = True
    reference_parents, reference = restriction_semigroup.reference_matrix(domain)
    if abs(reference.det()) != 1:
        raise ValueError("Reference packet matrix is not unimodular")
    parent_index = {parent: index for index, parent in enumerate(parents)}
    reference_indices = {
        parent_index[parent] for parent in reference_parents
    }
    for table in classification["facets"]:
        functional = dict(table)
        slacks = tuple(
            sum(
                functional.get(weight, 0) * multiplicity
                for weight, multiplicity in domain["branch_tables"][parent].items()
            )
            for parent in parents
        )
        if any(value < 0 for value in slacks):
            raise ValueError("Facet slack is negative on a packet")
        support = tuple(index for index, value in enumerate(slacks) if value)
        circuit_support_histogram[len(support)] += 1
        circuit_coefficient_histogram[max(slacks, default=0)] += 1
        signature = tuple(
            sorted(gale_row_signatures[index] for index in support)
        )
        circuit_type_counts[signature] += 1
        reference_support = tuple(
            sorted(index for index in support if index in reference_indices)
        )
        if not reference_support:
            raise ValueError("Facet circuit has no reference-packet support")
        reference_support_histogram[len(reference_support)] += 1
        reference_supports.add(reference_support)
        slack_column = matrix(ZZ, len(slacks), 1, slacks)
        all_kernel_relations = all_kernel_relations and (
            gale.transpose() * slack_column == 0
        )

    multiplicities_match = True
    for signature, observed in circuit_type_counts.items():
        signature_counts = Counter(signature)
        predicted = math.prod(
            math.comb(row_type_counts[row_type], count)
            for row_type, count in signature_counts.items()
        )
        multiplicities_match = multiplicities_match and predicted == observed

    expected_gale_types = expected_abc_gale_types(generator_names)

    return {
        "generator_names": generator_names,
        "kernel_rank": gale.rank(),
        "gale": gale,
        "gale_rows": gale_rows,
        "gale_row_signatures": gale_row_signatures,
        "unique_gale_row_types": len(row_type_counts),
        "zero_gale_rows": row_type_counts[zero],
        "unique_type_classes": dict(sorted(unique_type_classes.items())),
        "gale_type_multiplicity_histogram": dict(
            sorted(Counter(row_type_counts.values()).items())
        ),
        "abc_gale_template_applicable": expected_gale_types is not None,
        "abc_gale_template_matches": (
            expected_gale_types is not None
            and set(row_type_counts) == expected_gale_types
        ),
        "unique_circuit_types": len(circuit_type_counts),
        "circuit_type_counts": circuit_type_counts,
        "circuit_type_set": set(circuit_type_counts),
        "unique_circuit_support_histogram": dict(
            sorted(
                Counter(len(signature) for signature in circuit_type_counts).items()
            )
        ),
        "circuit_type_multiplicity_histogram": dict(
            sorted(Counter(circuit_type_counts.values()).items())
        ),
        "circuit_support_histogram": dict(
            sorted(circuit_support_histogram.items())
        ),
        "circuit_coefficient_histogram": dict(
            sorted(circuit_coefficient_histogram.items())
        ),
        "reference_support_histogram": dict(
            sorted(reference_support_histogram.items())
        ),
        "unique_reference_supports": len(reference_supports),
        "reference_supports_are_unique": (
            len(reference_supports) == len(classification["facets"])
        ),
        "all_reference_supports_nonempty": (
            sum(reference_support_histogram.values())
            == len(classification["facets"])
        ),
        "all_circuit_coefficients_one": set(
            circuit_coefficient_histogram
        ) == {1},
        "all_kernel_relations": all_kernel_relations,
        "combinatorial_multiplicities_match": multiplicities_match,
    }


def classify_domain(domain, include_packet_slacks=False):
    """Compute exact facets and their shift/translation classifications."""
    packets = restriction_semigroup.packet_matrix(domain)
    cone = restriction_semigroup.cone_diagnostics(packets)
    facets = tuple(
        facet_table(domain["weights"], inequality)
        for inequality in cone["inequalities"]
    )
    if len(set(facets)) != len(facets):
        raise ValueError("Canonical facet tables are not unique")

    ell_signatures = {
        translation_signature(table, axes=(0,)) for table in facets
    }
    full_translation_signatures = {
        translation_signature(table) for table in facets
    }
    result = {
        "domain": domain,
        "packets": packets,
        "cone": cone,
        "facets": facets,
        "facet_set": set(facets),
        "morphology": facet_morphology(facets),
        "ell_signatures": ell_signatures,
        "full_translation_signatures": full_translation_signatures,
        "shift_orbits": {
            AXIS_NAMES[axis]: shift_orbit_diagnostics(
                facets, domain["weights"], axis
            )
            for axis in range(4)
        },
    }
    if include_packet_slacks:
        result["packet_slacks"] = packet_slack_diagnostics(
            facets, domain["weights"], domain
        )
    return result


def compare_nested_classifications(previous, current):
    """Compare exact and translation-reduced facet templates at two horizons."""
    previous_facets = previous["facet_set"]
    current_facets = current["facet_set"]
    previous_ell = previous["ell_signatures"]
    current_ell = current["ell_signatures"]
    previous_full = previous["full_translation_signatures"]
    current_full = current["full_translation_signatures"]
    previous_circuits = previous["gale_circuits"]["circuit_type_set"]
    current_circuits = current["gale_circuits"]["circuit_type_set"]
    return {
        "exact_retained": len(previous_facets & current_facets),
        "exact_lost": len(previous_facets - current_facets),
        "exact_new": len(current_facets - previous_facets),
        "ell_retained": len(previous_ell & current_ell),
        "ell_lost": len(previous_ell - current_ell),
        "ell_new": len(current_ell - previous_ell),
        "full_retained": len(previous_full & current_full),
        "full_lost": len(previous_full - current_full),
        "full_new": len(current_full - previous_full),
        "circuit_retained": len(previous_circuits & current_circuits),
        "circuit_lost": len(previous_circuits - current_circuits),
        "circuit_new": len(current_circuits - previous_circuits),
    }


def analyze_interlacing_facets(max_level=11, min_level=1):
    """Run the complete nested-horizon TK6B.2 classification."""
    if min_level < 1 or min_level > max_level:
        raise ValueError("Require 1 <= min_level <= max_level")
    master = kernel_lattice.build_finite_domain(max_level)
    classifications = {}
    for horizon in range(min_level, max_level + 1):
        domain = (
            master
            if horizon == max_level
            else build_nested_domain(master, horizon)
        )
        classifications[horizon] = classify_domain(
            domain, include_packet_slacks=(horizon == max_level)
        )
    for classification in classifications.values():
        classification["gale_circuits"] = gale_circuit_diagnostics(
            classification
        )
    transitions = {
        horizon: compare_nested_classifications(
            classifications[horizon - 1], classifications[horizon]
        )
        for horizon in range(min_level + 1, max_level + 1)
    }
    final = classifications[max_level]
    return {
        "min_level": min_level,
        "max_level": max_level,
        "master": master,
        "classifications": classifications,
        "transitions": transitions,
        "final": final,
        "ell_templates_stabilized": bool(transitions) and all(
            transition["ell_new"] == 0 and transition["ell_lost"] == 0
            for transition in transitions.values()
        ),
        "full_templates_stabilized": bool(transitions) and all(
            transition["full_new"] == 0 and transition["full_lost"] == 0
            for transition in transitions.values()
        ),
    }


def run_analysis(max_level=11, min_level=1, verbose=False):
    """Print the reproducible TK6B.2 facet classification."""
    print("=" * 118)
    print("TK6B.2 — INTERLACING-PACKET FACET CLASSIFICATION")
    print("=" * 118)
    started = time.time()
    result = analyze_interlacing_facets(max_level=max_level, min_level=min_level)

    print("\nNested packet cones:")
    print(
        "  horizon  rows  packets  facets   ell templates  "
        "translation templates  Gale circuits"
    )
    for horizon, item in result["classifications"].items():
        print(
            f"  {horizon:<8} {item['packets'].nrows():<5} "
            f"{item['packets'].ncols():<8} {len(item['facets']):<8} "
            f"{len(item['ell_signatures']):<14} "
            f"{len(item['full_translation_signatures']):<22} "
            f"{item['gale_circuits']['unique_circuit_types']}"
        )

    print("\nChanges from the preceding horizon:")
    print(
        "  horizon  exact retained/lost/new  ell retained/lost/new  "
        "full-translation retained/lost/new"
    )
    for horizon, transition in result["transitions"].items():
        print(
            f"  {horizon:<8} "
            f"{transition['exact_retained']}/{transition['exact_lost']}/"
            f"{transition['exact_new']:<8} "
            f"{transition['ell_retained']}/{transition['ell_lost']}/"
            f"{transition['ell_new']:<8} "
            f"{transition['full_retained']}/{transition['full_lost']}/"
            f"{transition['full_new']}"
        )
    print("\nGale-circuit changes from the preceding horizon:")
    print("  horizon  retained/lost/new")
    for horizon, transition in result["transitions"].items():
        print(
            f"  {horizon:<8} {transition['circuit_retained']}/"
            f"{transition['circuit_lost']}/{transition['circuit_new']}"
        )

    final = result["final"]
    print(f"\nExact one-step shift covariance at horizon {max_level}:")
    print("  axis  eligible  matched  fraction  seeds  nontrivial  max orbit")
    for axis in AXIS_NAMES:
        orbit = final["shift_orbits"][axis]
        fraction = orbit["eligible_match_fraction"]
        fraction_text = "-" if fraction is None else f"{fraction:.3f}"
        print(
            f"  {axis:<5} {orbit['forward_eligible']:<9} "
            f"{orbit['forward_matches']:<8} {fraction_text:<9} "
            f"{orbit['seeds']:<6} {orbit['nontrivial_orbits']:<11} "
            f"{orbit['maximum_orbit_length']}"
        )

    morphology = final["morphology"]
    packet_slacks = final["packet_slacks"]
    gale = final["gale_circuits"]
    print("\nFinal-horizon facet morphology:")
    print(f"  Pure coordinate/positivity facets: {morphology['pure_nonnegative']}")
    print(f"  Mixed-sign covering facets: {morphology['mixed_sign']}")
    print(f"  Zero coefficient-sum facets: {morphology['zero_sum']}")
    print(
        "  Facet support range: "
        f"{min(morphology['support_histogram'])}.."
        f"{max(morphology['support_histogram'])}"
    )
    print(
        "  Tight packet rays per facet: "
        f"{packet_slacks['minimum_tight_rays']}.."
        f"{packet_slacks['maximum_tight_rays']}"
    )
    if verbose:
        print(f"  Support histogram: {morphology['support_histogram']}")
        print(
            "  Maximum coefficient histogram: "
            f"{morphology['maximum_coefficient_histogram']}"
        )
        print(
            "  Packet positive-ray histogram: "
            f"{packet_slacks['positive_ray_histogram']}"
        )

    print("\nKernel/Gale positive-circuit classification:")
    print(f"  Kernel rank: {gale['kernel_rank']}")
    print(f"  Distinct Gale row types: {gale['unique_gale_row_types']}")
    print(f"  Zero Gale rows: {gale['zero_gale_rows']}")
    print(f"  Gale type classes: {gale['unique_type_classes']}")
    print(
        "  Compact A/B/C Gale-row template exact: "
        f"{gale['abc_gale_template_matches']}"
    )
    print(f"  Distinct positive-circuit types: {gale['unique_circuit_types']}")
    print(
        "  Every circuit has unit coefficients: "
        f"{gale['all_circuit_coefficients_one']}"
    )
    print(
        "  Type multiplicities reconstruct all facets: "
        f"{gale['combinatorial_multiplicities_match']}"
    )
    print(
        "  Facets become distinct zero-one reference subsets: "
        f"{gale['reference_supports_are_unique']}"
    )
    print(
        "  Reference-subset size range: "
        f"{min(gale['reference_support_histogram'])}.."
        f"{max(gale['reference_support_histogram'])}"
    )
    if verbose:
        print(
            "  Circuit support histogram: "
            f"{gale['circuit_support_histogram']}"
        )
        print(
            "  Gale-type multiplicity histogram: "
            f"{gale['gale_type_multiplicity_histogram']}"
        )
        print(
            "  Unique circuit support histogram: "
            f"{gale['unique_circuit_support_histogram']}"
        )
        print(
            "  Circuit-template multiplicity histogram: "
            f"{gale['circuit_type_multiplicity_histogram']}"
        )
        print(
            "  Reference-subset size histogram: "
            f"{gale['reference_support_histogram']}"
        )

    checks = (
        all(
            item["cone"]["dimension"] == item["packets"].nrows()
            and item["cone"]["extreme_rays"] == item["packets"].ncols()
            and item["gale_circuits"]["abc_gale_template_matches"]
            and item["gale_circuits"]["all_kernel_relations"]
            and item["gale_circuits"]["all_circuit_coefficients_one"]
            and item["gale_circuits"]["combinatorial_multiplicities_match"]
            and item["gale_circuits"]["reference_supports_are_unique"]
            and item["gale_circuits"]["all_reference_supports_nonempty"]
            and all(
                orbit["all_facets_covered"]
                for orbit in item["shift_orbits"].values()
            )
            for item in result["classifications"].values()
        )
        and len(final["facets"]) == 2508
        and morphology["pure_nonnegative"] + morphology["mixed_sign"]
        == len(final["facets"])
        and gale["all_kernel_relations"]
        and gale["abc_gale_template_matches"]
        and gale["all_circuit_coefficients_one"]
        and gale["combinatorial_multiplicities_match"]
        and gale["reference_supports_are_unique"]
        and gale["all_reference_supports_nonempty"]
    )
    print("\nStabilization verdict:")
    print(
        "  Leading-shift template set stabilized: "
        f"{result['ell_templates_stabilized']}"
    )
    print(
        "  Full-translation template set stabilized: "
        f"{result['full_templates_stabilized']}"
    )
    print("-" * 118)
    print("Protected SO(10) baseline imported: NO")
    print(f"TK6B.2 finite classification: {'PASS' if checks else 'FAIL'}")
    print(f"Runtime: {time.time() - started:.3f}s")
    result["all_checks"] = checks
    return result


def run_self_test():
    """Check exact facet translations and orbit bookkeeping synthetically."""
    facets = (
        (((0, 0, 0, 0), -1), ((1, 0, 0, 0), 1)),
        (((1, 0, 0, 0), -1), ((2, 0, 0, 0), 1)),
        (((0, 1, 0, 0), 1),),
    )
    weights = tuple(
        (ell, m, 0, 0)
        for ell in range(3)
        for m in range(2)
    )
    orbit = shift_orbit_diagnostics(facets, weights, axis=0)
    if orbit["forward_matches"] != 1:
        raise AssertionError("Synthetic leading-shift edge was not found")
    if orbit["maximum_orbit_length"] != 2:
        raise AssertionError("Synthetic facet orbit has the wrong length")
    if len({translation_signature(table, axes=(0,)) for table in facets}) != 2:
        raise AssertionError("Synthetic leading-translation signatures failed")
    print("TK6B.2 INTERLACING-FACET SELF-TEST")
    print("  Translation signatures: PASS")
    print("  Exact shift orbits: PASS")
    print("  Protected SO(10) baseline imported: NO")
    return True


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Classify finite D5 -> B4 packet-cone facets"
    )
    parser.add_argument("--max-level", type=int, default=11)
    parser.add_argument("--min-level", type=int, default=1)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args(argv)

    try:
        if args.self_test:
            run_self_test()
            return 0
        result = run_analysis(
            max_level=args.max_level,
            min_level=args.min_level,
            verbose=args.verbose,
        )
    except Exception as error:
        print(f"TK6B.2 FAILED: {error}", file=sys.stderr)
        return 1
    return 0 if result["all_checks"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
