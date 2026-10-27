"""TK6B.6a: scalar-tail correction from the Green--Schwarz telescope.

The cumulative Regge construction reduces one part of the Bars positivity
problem to the scalar series

    B(q) = [1] PE(q V_10) S(F(q)) = C(q)/(1-q^2),

where ``S`` is the all-chiral triangular section and ``C`` is a diagonal
six-ray Möbius functional of the HFT remainder.  This module applies that
functional directly to the exact ``D4`` Green--Schwarz telescoping summands
of TK6B.5f.  It therefore exposes the contribution of every pivot without
using a protected ``SO(10)`` lift or first deriving higher cumulative lifts.
"""

import argparse
import sys
import time

from trajectory_kernel import cumulative_regge_uplift
from trajectory_kernel import hft_analytic_support


def add_series(left, right):
    """Add equal-length integer coefficient tuples."""
    if len(left) != len(right):
        raise ValueError("Cannot add scalar series of different lengths")
    return tuple(int(a) + int(b) for a, b in zip(left, right))


def diagonal_from_b4_tables(tables, maximum_degree):
    """Apply the six-ray one-row functional along ``degree + ell``."""
    maximum_degree = int(maximum_degree)
    diagonal = [0] * (maximum_degree + 1)
    for degree, table in tables.items():
        for ell in range(maximum_degree - int(degree) + 1):
            diagonal[int(degree) + ell] += (
                cumulative_regge_uplift.one_row_chiral_coordinate(table, ell)
            )
    return tuple(diagonal)


def correction_from_scalar(scalar, tail_start=9):
    """Return coefficients of ``-(1+q) B_{>=tail_start}``."""
    scalar = tuple(map(int, scalar))
    tail_start = int(tail_start)
    if tail_start < 0:
        raise ValueError("tail_start must be nonnegative")
    correction = [0] * len(scalar)
    for degree in range(tail_start, len(scalar)):
        correction[degree] = -scalar[degree]
        if degree - 1 >= tail_start:
            correction[degree] -= scalar[degree - 1]
    return tuple(correction)


def prefix_correction_from_diagonal(diagonal, tail_start=9):
    """Return the scalar correction as a prefix sum of ``C``.

    Globally, ``(1+q)B=C/(1-q)`` because ``B=C/(1-q^2)``.  The
    correction used in TK6B.6 truncates ``B`` before multiplying by
    ``1+q``.  The two descriptions consequently agree from ``tail_start``
    onward precisely when the preceding scalar coefficient vanishes.  In
    the HFT application ``tail_start=9`` and the exact low-degree check is
    ``b_8=0``.
    """
    diagonal = tuple(map(int, diagonal))
    tail_start = int(tail_start)
    if tail_start < 0:
        raise ValueError("tail_start must be nonnegative")
    running = 0
    correction = [0] * len(diagonal)
    for degree, coefficient in enumerate(diagonal):
        running += coefficient
        if degree >= tail_start:
            correction[degree] = -running
    return tuple(correction)


def green_schwarz_scalar_tail(maximum_degree, tail_start=9):
    """Evaluate the scalar diagonal pivot by pivot from the exact telescope."""
    maximum_degree = int(maximum_degree)
    terms = hft_analytic_support.d4_telescoping_terms(maximum_degree)
    pivot_tables = {}
    pivot_diagonals = {}
    pivot_scalars = {}
    pivot_corrections = {}
    zero = tuple(0 for _ in range(maximum_degree + 1))
    total_diagonal = zero

    for pivot, series in sorted(terms.items()):
        tables = {
            degree: hft_analytic_support.d4_dirac_dominant_table(character)
            for degree, character in series.items()
        }
        diagonal = diagonal_from_b4_tables(tables, maximum_degree)
        scalar = cumulative_regge_uplift.scalar_regge_series_from_diagonal(
            diagonal
        )
        correction = correction_from_scalar(scalar, tail_start=tail_start)
        pivot_tables[pivot] = tables
        pivot_diagonals[pivot] = diagonal
        pivot_scalars[pivot] = scalar
        pivot_corrections[pivot] = correction
        total_diagonal = add_series(total_diagonal, diagonal)

    total_scalar = cumulative_regge_uplift.scalar_regge_series_from_diagonal(
        total_diagonal
    )
    total_correction = correction_from_scalar(
        total_scalar, tail_start=tail_start
    )
    prefix_correction = prefix_correction_from_diagonal(
        total_diagonal, tail_start=tail_start
    )
    boundary_scalar = (
        total_scalar[tail_start - 1]
        if 0 < tail_start <= maximum_degree
        else 0
    )
    summed_correction = zero
    for correction in pivot_corrections.values():
        summed_correction = add_series(summed_correction, correction)
    return {
        "maximum_degree": maximum_degree,
        "tail_start": int(tail_start),
        "terms": terms,
        "pivot_tables": pivot_tables,
        "pivot_diagonals": pivot_diagonals,
        "pivot_scalars": pivot_scalars,
        "pivot_corrections": pivot_corrections,
        "total_diagonal": total_diagonal,
        "total_scalar": total_scalar,
        "total_correction": total_correction,
        "prefix_correction": prefix_correction,
        "boundary_scalar": boundary_scalar,
        "prefix_identity_exact": (
            boundary_scalar == 0 and prefix_correction == total_correction
        ),
        "pivot_sum_exact": summed_correction == total_correction,
        "tail_nonnegative": all(
            value >= 0
            for value in total_correction[int(tail_start):]
        ),
    }


def independent_hft_diagonal(maximum_degree):
    """Derive the same diagonal through the independent HFT quotient route."""
    import hft_so9
    from trajectory_kernel import regge_factorization

    maximum_degree = int(maximum_degree)
    _numerator, single_levels = hft_so9.derive_hft_spectrum(
        maximum_degree + 1
    )
    factorization = regge_factorization.factor_symmetric_vector_tower(
        single_levels, maximum_degree + 1
    )
    return cumulative_regge_uplift.diagonal_hft_mobius_series(
        factorization["remainder"], maximum_degree
    )


def run_analysis(maximum_degree=12, tail_start=9, compare_hft=False):
    """Run the direct Green--Schwarz scalar-tail calculation."""
    started = time.time()
    result = green_schwarz_scalar_tail(maximum_degree, tail_start=tail_start)
    independent = None
    if compare_hft:
        independent = independent_hft_diagonal(maximum_degree)
    result["independent_hft_diagonal"] = independent
    result["independent_match"] = (
        independent is None or independent == result["total_diagonal"]
    )

    print("=" * 100)
    print("TK6B.6a — GREEN--SCHWARZ SCALAR TAIL")
    print("=" * 100)
    print(f"Degrees: 0 through {int(maximum_degree)}")
    print(f"Telescoping pivots: {len(result['terms'])}")
    print(f"Pivot sum exact: {result['pivot_sum_exact']}")
    print(f"Independent HFT comparison requested: {bool(compare_hft)}")
    if compare_hft:
        print(f"Independent HFT diagonal matches: {result['independent_match']}")
    print(f"Diagonal C_N: {result['total_diagonal']}")
    print(f"Scalar B_N: {result['total_scalar']}")
    print(f"Correction A_N: {result['total_correction']}")
    print(
        "Prefix-sum formula exact: "
        f"{result['prefix_identity_exact']} "
        f"(preceding scalar b_{int(tail_start) - 1}="
        f"{result['boundary_scalar']})"
    )
    print(
        f"Correction nonnegative from degree {int(tail_start)}: "
        f"{result['tail_nonnegative']}"
    )
    print("Nonzero pivot correction contributions:")
    for pivot, correction in result["pivot_corrections"].items():
        nonzero = {
            degree: value
            for degree, value in enumerate(correction)
            if value
        }
        if nonzero:
            print(f"  pivot {pivot}: {nonzero}")
    print("Protected SO(10) baseline imported: NO")
    print(f"Runtime: {time.time() - started:.3f}s")
    return result


def run_self_test():
    """Compare the D4 telescope and independent HFT paths at low degree."""
    result = run_analysis(maximum_degree=10, tail_start=9, compare_hft=True)
    if not result["pivot_sum_exact"]:
        raise AssertionError("The scalar pivot sum failed")
    if not result["independent_match"]:
        raise AssertionError("The Green--Schwarz/HFT scalar diagonal failed")
    if not result["prefix_identity_exact"]:
        raise AssertionError("The diagonal prefix-sum identity failed")
    if not result["tail_nonnegative"]:
        raise AssertionError("The first scalar-tail coefficients are negative")
    return True


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Pull the TK6B.6 scalar tail through the Green--Schwarz telescope"
    )
    parser.add_argument("--maximum-degree", type=int, default=12)
    parser.add_argument("--tail-start", type=int, default=9)
    parser.add_argument("--compare-hft", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.self_test:
            return 0 if run_self_test() else 1
        result = run_analysis(
            maximum_degree=args.maximum_degree,
            tail_start=args.tail_start,
            compare_hft=args.compare_hft,
        )
    except Exception as error:
        print(f"TK6B.6a FAILED: {error}", file=sys.stderr)
        return 1
    return 0 if result["pivot_sum_exact"] and result["independent_match"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
