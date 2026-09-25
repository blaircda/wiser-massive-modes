"""GU3: baseline-free Type-IIA closed refinement of the paper grading.

The Type-IIB construction uses identical left and right chiral spectra.  The
minimal Type-IIA modification outer-conjugates the right D5 factor.  In a
common left-sector convention this changes the right grading from
``nu=Delta-J`` to ``nu=Delta+J``.

Bars' additional nonperturbative level is retained as ``ell_prime=n-ell``.
No protected SO(10) completion is imported here.
"""

import argparse

from sage.all import QQ, matrix

import hft_so9
from graded_uplift import graded_kernel
from graded_uplift import paper_levels
from graded_uplift import refined_branching
from graded_uplift import refined_spectrum
from graded_uplift import verify_paper_grading


def d4_outer_conjugate(character):
    """Exchange the two D4 spinor nodes."""
    return sum(
        (
            coefficient * refined_spectrum.D4(a1, a2, a4, a3)
            for (a1, a2, a3, a4), coefficient
            in refined_spectrum.d4_coefficients(character).items()
        ),
        refined_spectrum.D4(0),
    )


def d5_coefficients(character):
    """Return irreducible D5 coefficients keyed by Dynkin label."""
    result = {}
    for weight, coefficient in character.monomial_coefficients().items():
        x1, x2, x3, x4, x5 = weight.to_vector()
        label = (
            int(x1 - x2),
            int(x2 - x3),
            int(x3 - x4),
            int(x4 - x5),
            int(x4 + x5),
        )
        result[label] = int(coefficient)
    return {label: value for label, value in sorted(result.items()) if value}


def d5_character(coefficients):
    return sum(
        (
            coefficient * refined_branching.D5(*label)
            for label, coefficient in coefficients.items()
        ),
        refined_branching.D5(0),
    )


def d5_outer_conjugate(character):
    """Apply the D5 outer automorphism a4 <-> a5."""
    return d5_character(
        {
            (a1, a2, a3, a5, a4): coefficient
            for (a1, a2, a3, a4, a5), coefficient
            in d5_coefficients(character).items()
        }
    )


def conjugate_terms(terms):
    """Outer-conjugate every D5 label while preserving Delta."""
    return tuple(
        (twice_delta, coefficient, (a1, a2, a3, a5, a4))
        for twice_delta, coefficient, (a1, a2, a3, a4, a5) in terms
    )


def right_target_image(refined, level):
    """Opposite-chirality right oscillator target at one level."""
    return {
        nu: d4_outer_conjugate(character)
        for nu, character in verify_paper_grading.target_level_image(
            refined, level
        ).items()
    }


def nonperturbative_blocks(refined, mass_level, right=False):
    """Return ``(ell_prime,nu)`` blocks with ell_prime=mass_level-ell."""
    result = {}
    for oscillator_level in range(1, mass_level + 1):
        ell_prime = mass_level - oscillator_level
        image = verify_paper_grading.target_level_image(
            refined, oscillator_level
        )
        for nu, character in image.items():
            result[ell_prime, nu] = (
                d4_outer_conjugate(character) if right else character
            )
    return dict(sorted(result.items()))


def graded_branching_rank(level, policy="outer-closed"):
    """Exact rank of the tagged D5 -> nu-graded D4 map."""
    terms = graded_kernel.candidate_terms(level, policy)
    images = {
        term: graded_kernel.tagged_term_image(*term)
        for term in terms
    }
    rows = sorted(set().union(*(set(image) for image in images.values())))
    row_index = {row: index for index, row in enumerate(rows)}
    entries = {
        (row_index[row], column): coefficient
        for column, term in enumerate(terms)
        for row, coefficient in images[term].items()
    }
    branching_matrix = matrix(
        QQ, len(rows), len(terms), entries, sparse=True
    )
    return {
        "rows": len(rows),
        "columns": len(terms),
        "rank": branching_matrix.rank(),
    }


def run_audit(max_level=7, compute_ranks_from=1):
    if max_level < 1 or max_level > max(paper_levels.PAPER_LEVELS):
        raise ValueError("GU3 literature transcription currently covers levels 1--7")
    refined = refined_spectrum.derive_refined_primaries(max_level)
    cumulative = verify_paper_grading.cumulative_ungraded_coefficients(max_level)
    _numerator, hft_levels = hft_so9.derive_hft_spectrum(max_level)

    results = {}
    running_hft = hft_so9.B4(0)
    print("=" * 118)
    print("GU3 — TYPE-IIA OPPOSITE-CHIRALITY AND NONPERTURBATIVE-LEVEL REFINEMENT")
    print("=" * 118)
    print(
        " level | conjugated right exact | axial right exact | ell-prime blocks exact | "
        "cumulative positive | SO9 exact | graded rank"
    )
    for level in range(1, max_level + 1):
        terms = paper_levels.expanded_terms(level)
        right_target = right_target_image(refined, level)
        conjugated_right = refined_branching.image_of_terms(
            conjugate_terms(terms), signed=True
        )
        axial_right = refined_branching.axial_image_of_terms(
            terms, signed=True
        )
        right_conjugation_exact = conjugated_right == right_target
        axial_exact = axial_right == right_target

        left_blocks = nonperturbative_blocks(refined, level, right=False)
        right_blocks = nonperturbative_blocks(refined, level, right=True)
        block_exact = all(
            refined_branching.image_of_terms(
                paper_levels.expanded_terms(oscillator_level), signed=True
            )
            == verify_paper_grading.target_level_image(
                refined, oscillator_level
            )
            for oscillator_level in range(1, level + 1)
        ) and all(
            refined_branching.image_of_terms(
                conjugate_terms(paper_levels.expanded_terms(oscillator_level)),
                signed=True,
            )
            == right_target_image(refined, oscillator_level)
            for oscillator_level in range(1, level + 1)
        )

        paper_character = d5_character(cumulative[level])
        positive = all(value >= 0 for value in cumulative[level].values())
        running_hft += hft_levels[level]
        left_restriction = paper_character.branch(hft_so9.B4, rule="default")
        right_restriction = d5_outer_conjugate(paper_character).branch(
            hft_so9.B4, rule="default"
        )
        restriction_exact = left_restriction == running_hft == right_restriction

        rank_data = None
        if level >= compute_ranks_from:
            rank_data = graded_branching_rank(level)
        rank_text = (
            "--"
            if rank_data is None
            else f"{rank_data['rank']}/{rank_data['columns']}"
        )
        results[level] = {
            "right_conjugation_exact": right_conjugation_exact,
            "axial_exact": axial_exact,
            "left_blocks": left_blocks,
            "right_blocks": right_blocks,
            "block_exact": block_exact,
            "positive": positive,
            "restriction_exact": restriction_exact,
            "rank": rank_data,
            "paper_character": paper_character,
        }
        print(
            f" {level:5d} | {str(right_conjugation_exact):>22s} | "
            f"{str(axial_exact):>17s} | {str(block_exact):>22s} | "
            f"{str(positive):>19s} | {str(restriction_exact):>9s} | "
            f"{rank_text:>11s}"
        )

    checks_pass = all(
        result["right_conjugation_exact"]
        and result["axial_exact"]
        and result["block_exact"]
        and result["positive"]
        and result["restriction_exact"]
        and (
            result["rank"] is None
            or result["rank"]["rank"] == result["rank"]["columns"]
        )
        for result in results.values()
    )
    cumulative_rank_data = {}
    if all(results[level]["rank"] is not None for level in results):
        for horizon in range(1, max_level + 1):
            chiral_columns = sum(
                results[level]["rank"]["columns"]
                for level in range(1, horizon + 1)
            )
            chiral_rank = sum(
                results[level]["rank"]["rank"]
                for level in range(1, horizon + 1)
            )
            cumulative_rank_data[horizon] = {
                "chiral_columns": chiral_columns,
                "chiral_rank": chiral_rank,
                "closed_columns": chiral_columns * chiral_columns,
                "closed_rank": chiral_rank * chiral_rank,
            }
    print("-" * 118)
    print("IIA rule: left nu=Delta-J; right nu=Delta+J")
    print("Equivalent right rule: outer-conjugate D5 and retain nu=Delta-J")
    print("Bars tag retained independently: ell_prime=mass level-oscillator level")
    for horizon in range(max(6, 1), max_level + 1):
        if horizon in cumulative_rank_data:
            rank_data = cumulative_rank_data[horizon]
            print(
                f"Resolved horizon {horizon}: chiral rank "
                f"{rank_data['chiral_rank']}/{rank_data['chiral_columns']}; "
                f"closed tensor rank "
                f"{rank_data['closed_rank']}/{rank_data['closed_columns']}"
            )
    print("Protected Bars completion imported: NO")
    print(f"GU3 baseline-free checks: {'PASS' if checks_pass else 'FAIL'}")
    return {
        "refined": refined,
        "cumulative": cumulative,
        "results": results,
        "cumulative_rank_data": cumulative_rank_data,
        "all_checks": checks_pass,
    }


def run_self_test():
    spinor_s = refined_spectrum.D4(0, 0, 0, 1)
    spinor_c = refined_spectrum.D4(0, 0, 1, 0)
    d5_spinor = refined_branching.D5(0, 0, 0, 0, 1)
    checks = (
        d4_outer_conjugate(spinor_s) == spinor_c,
        d5_outer_conjugate(d5_spinor)
        == refined_branching.D5(0, 0, 0, 1, 0),
        d5_outer_conjugate(d5_outer_conjugate(d5_spinor)) == d5_spinor,
    )
    passed = all(checks)
    print("GU3 TYPE-IIA REFINEMENT SELF-TEST")
    print(f"D4/D5 chirality involutions: {'PASS' if passed else 'FAIL'}")
    print("Protected SO(10) baseline imported: NO")
    return passed


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Test the Type-IIA opposite-chirality graded construction"
    )
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--max-level", type=int, default=7)
    parser.add_argument("--compute-ranks-from", type=int, default=1)
    arguments = parser.parse_args()
    if arguments.self_test:
        raise SystemExit(0 if run_self_test() else 1)
    audit = run_audit(arguments.max_level, arguments.compute_ranks_from)
    raise SystemExit(0 if audit["all_checks"] else 1)
