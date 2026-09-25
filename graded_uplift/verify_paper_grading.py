"""GU1: verify the hep-th/0310292 grading and its cumulative SO(10) lift.

The oscillator-refined SO(8) data are derived independently.  The Appendix B
table is external literature input and is used only as a candidate to verify.
The protected Bars SO(10) completion is neither imported nor consulted.
"""

import argparse
import time
from collections import Counter

import hft_so9
from graded_uplift import paper_levels
from graded_uplift import refined_branching
from graded_uplift import refined_spectrum
from trajectory_kernel import correction_ansatz
from trajectory_kernel import kernel_lattice


def paper_level_image(level):
    return refined_branching.image_of_terms(
        paper_levels.expanded_terms(level), signed=True
    )


def target_level_image(refined, level):
    return {
        nu: character
        for (candidate_level, nu), character in refined["signed"].items()
        if candidate_level == level and character != refined_spectrum.D4(0)
    }


def cumulative_ungraded_coefficients(max_level):
    result = Counter()
    by_level = {}
    for level in range(1, max_level + 1):
        for _twice_delta, coefficient, label in paper_levels.expanded_terms(level):
            result[label] += coefficient
            if not result[label]:
                del result[label]
        by_level[level] = dict(sorted(result.items()))
    return by_level


def d5_character(coefficients):
    return sum(
        (
            coefficient * refined_branching.D5(*label)
            for label, coefficient in coefficients.items()
        ),
        refined_branching.D5(0),
    )


def paper_kernel_coordinates(max_level, cumulative_coefficients):
    domain = kernel_lattice.build_finite_domain(max_level)
    generators = correction_ansatz.ordered_generators(
        kernel_lattice.natural_kernel_generators(domain)
    )
    coordinates = {}
    outside_domain = {}
    sources = []
    keys = tuple(
        (generator.top_weight[1:], generator.top_weight[0])
        for generator in generators
    )
    key_index = {key: index for index, key in enumerate(keys)}
    previous = tuple(0 for _generator in generators)
    for level in range(1, max_level + 1):
        outside_domain[level] = tuple(
            sorted(set(cumulative_coefficients[level]) - set(domain["parents"]))
        )
        if outside_domain[level]:
            continue
        current = tuple(
            int(cumulative_coefficients[level].get(generator.alternative_parent, 0))
            for generator in generators
        )
        coordinates[level] = current
        for index, (generator, key) in enumerate(zip(generators, keys)):
            ell = key[1]
            predecessor = None if ell == 0 else key_index.get((key[0], ell - 1))
            transported = 0 if predecessor is None else previous[predecessor]
            source = current[index] - transported
            if source:
                sources.append(
                    (
                        level,
                        correction_ansatz.family_label(generator),
                        source,
                    )
                )
        previous = current
    return domain, generators, coordinates, tuple(sources), outside_domain


def run_audit(max_level=7, verbose=False):
    if max_level < 1 or max_level > max(paper_levels.PAPER_LEVELS):
        raise ValueError("GU1 literature transcription currently covers levels 1--7")
    started = time.time()
    refined = refined_spectrum.derive_refined_primaries(max_level)
    _numerator, hft_levels = hft_so9.derive_hft_spectrum(max_level)

    refined_matches_hft = {}
    paper_matches_refined = {}
    for level in range(1, max_level + 1):
        unsigned = refined_spectrum.level_character(refined["positive"], level)
        refined_matches_hft[level] = unsigned == hft_levels[level].branch(
            refined_spectrum.D4, rule="default"
        )
        paper_matches_refined[level] = (
            paper_level_image(level) == target_level_image(refined, level)
        )

    cumulative = cumulative_ungraded_coefficients(max_level)
    positive = {
        level: all(coefficient >= 0 for coefficient in coefficients.values())
        for level, coefficients in cumulative.items()
    }
    restriction_exact = {}
    running_hft = hft_so9.B4(0)
    for level in range(1, max_level + 1):
        running_hft += hft_levels[level]
        restriction_exact[level] = (
            d5_character(cumulative[level]).branch(hft_so9.B4, rule="default")
            == running_hft
        )

    domain, generators, coordinates, sources, outside_domain = paper_kernel_coordinates(
        max_level, cumulative
    )
    coordinate_reconstruction = True
    for level in range(1, max_level + 1):
        if outside_domain[level]:
            continue
        reference = correction_ansatz.reference_lift(
            domain, domain["cumulative"][level]
        )
        reconstructed = correction_ansatz.coefficients_from_coordinates(
            reference, generators, coordinates[level]
        )
        coordinate_reconstruction = coordinate_reconstruction and (
            reconstructed == cumulative[level]
        )

    print("=" * 108)
    print("GU1 — OSCILLATOR-COUNT-REFINED LITERATURE UPLIFT")
    print("=" * 108)
    print("  level | refined SO8 -> ungraded HFT | Appendix B -> refined SO8 | cumulative positive | SO9 exact")
    for level in range(1, max_level + 1):
        print(
            f"  {level:5d} | {str(refined_matches_hft[level]):>27s} | "
            f"{str(paper_matches_refined[level]):>25s} | "
            f"{str(positive[level]):>19s} | {str(restriction_exact[level]):>9s}"
        )
    print(
        "Trajectory-kernel coordinate reconstruction exact where in domain: "
        f"{coordinate_reconstruction}"
    )
    compatible_through = next(
        (level - 1 for level in range(1, max_level + 1) if outside_domain[level]),
        max_level,
    )
    print(f"Inside fixed positive-chirality TK domain through level: {compatible_through}")
    if compatible_through < max_level:
        first_outside = compatible_through + 1
        print(
            f"First outside-domain D5 parents at n={first_outside}: "
            f"{outside_domain[first_outside]}"
        )
    print(f"Nonzero corrected-shift sources inside that domain: {sources}")
    if verbose:
        for level in range(1, max_level + 1):
            print(f"n={level} cumulative D5 coefficients: {cumulative[level]}")

    all_checks = (
        all(refined_matches_hft.values())
        and all(paper_matches_refined.values())
        and all(positive.values())
        and all(restriction_exact.values())
        and coordinate_reconstruction
    )
    print("-" * 108)
    print("Appendix B is external literature input; protected Bars completion imported: NO")
    print(f"GU1 exact checks: {'PASS' if all_checks else 'FAIL'}")
    print(f"Elapsed: {time.time() - started:.3f}s")
    return {
        "refined": refined,
        "hft_levels": hft_levels,
        "refined_matches_hft": refined_matches_hft,
        "paper_matches_refined": paper_matches_refined,
        "cumulative": cumulative,
        "positive": positive,
        "restriction_exact": restriction_exact,
        "domain": domain,
        "generators": generators,
        "coordinates": coordinates,
        "sources": sources,
        "outside_domain": outside_domain,
        "compatible_through": compatible_through,
        "coordinate_reconstruction": coordinate_reconstruction,
        "all_checks": all_checks,
    }


def run_self_test():
    vector_branch = refined_branching.branch_irrep_with_charge((1, 0, 0, 0, 0))
    expected = {
        -2: refined_spectrum.D4(0, 0, 0, 0),
        0: refined_spectrum.D4(1, 0, 0, 0),
        2: refined_spectrum.D4(0, 0, 0, 0),
    }
    passed = vector_branch == expected
    print("GU1 REFINED-BRANCHING SELF-TEST")
    print(f"10 -> 8v_0 + 1_+1 + 1_-1: {'PASS' if passed else 'FAIL'}")
    print("Protected SO(10) baseline imported: NO")
    return passed


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Verify the oscillator-count-refined literature uplift"
    )
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--max-level", type=int, default=7)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        raise SystemExit(0 if run_self_test() else 1)
    result = run_audit(args.max_level, args.verbose)
    raise SystemExit(0 if result["all_checks"] else 1)
