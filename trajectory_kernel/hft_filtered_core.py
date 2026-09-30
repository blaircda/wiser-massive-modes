"""TK6B.5e: isolate the HFT support problem after all vector modes.

Let ``R(q)`` be the massive HFT primary series in the project convention and
let ``V=[1,0,0,0]``.  This module defines the all-vector-free core ``C`` by

    R(q) = PE(q/(1-q) V) C(q).

The HFT oscillator formula then gives the exact formal identity

    q Z_Q C(q) = phi(q) S(q) - S(0) PE(-q/(1-q) V),

where ``phi(q)=prod_{m>=1}(1-q^m)`` and ``S`` is the combined NS/R fermion
series before multiplication by the transverse bosonic partition function.
For the original level-one-vector remainder ``F``, the corresponding identity
is

    q Z_Q F(q)
      = PE(q^2/(1-q)V) phi(q) S(q) - S(0) PE(-qV).

Thus the unresolved all-degree support statement is concentrated in a fixed
character division of an explicit oscillator numerator.  No protected SO(10)
completion is imported.
"""

import argparse
import sys
import time

from sage.all import QQ

import hft_so9
from trajectory_kernel import hft_pieri_hazard
from trajectory_kernel import regge_factorization


B4 = hft_so9.B4
SCALAR = B4(0, 0, 0, 0)


def hft_fermion_series(maximum_degree):
    """Return the combined HFT NS/R series ``S(q)`` exactly."""
    maximum_degree = int(maximum_degree)
    if maximum_degree < 0:
        raise ValueError("maximum_degree must be nonnegative")

    fermion_r_factors = [
        {
            mode * exterior_degree: hft_so9.LAMBDA[exterior_degree]
            for exterior_degree in range(
                min(9, maximum_degree // mode + 1)
            )
        }
        for mode in range(1, maximum_degree + 1)
    ]
    ramond = hft_so9.multiply_formal_series(
        fermion_r_factors, maximum_degree
    )

    maximum_t_degree = 2 * maximum_degree + 1
    fermion_ns_factors = [
        {
            frequency * exterior_degree: hft_so9.LAMBDA[exterior_degree]
            for exterior_degree in range(
                min(9, maximum_t_degree // frequency + 1)
            )
        }
        for frequency in range(1, maximum_t_degree + 1, 2)
    ]
    ns_in_t = hft_so9.multiply_formal_series(
        fermion_ns_factors, maximum_t_degree
    )
    neveu_schwarz = {
        degree: ns_in_t.get(2 * degree + 1, B4(0))
        for degree in range(maximum_degree + 1)
    }
    return {
        degree: neveu_schwarz[degree]
        + (QQ(1) / 2) * hft_so9.S9 * ramond[degree]
        for degree in range(maximum_degree + 1)
    }


def euler_scalar_series(maximum_degree):
    """Return ``prod_{m>=1}(1-q^m)`` through the requested degree."""
    maximum_degree = int(maximum_degree)
    factors = [
        {0: SCALAR, mode: -SCALAR}
        for mode in range(1, maximum_degree + 1)
    ]
    return hft_so9.multiply_formal_series(factors, maximum_degree)


def inverse_vector_tower(maximum_degree):
    """Return ``PE(-q/(1-q) V)`` through the requested degree."""
    maximum_degree = int(maximum_degree)
    factors = [
        {
            mode * exterior_degree: (
                (-1) ** exterior_degree
                * hft_so9._WEDGE_9[exterior_degree]
            )
            for exterior_degree in range(
                min(10, maximum_degree // mode + 1)
            )
        }
        for mode in range(1, maximum_degree + 1)
    ]
    return hft_so9.multiply_formal_series(factors, maximum_degree)


def inverse_level_one_vector(maximum_degree):
    """Return ``PE(-q V)`` through the requested degree."""
    maximum_degree = int(maximum_degree)
    factor = {
        exterior_degree: (
            (-1) ** exterior_degree * hft_so9._WEDGE_9[exterior_degree]
        )
        for exterior_degree in range(min(10, maximum_degree + 1))
    }
    return {
        degree: factor.get(degree, B4(0))
        for degree in range(maximum_degree + 1)
    }


def filtered_core_numerator(maximum_degree):
    """Return both sides of the explicit numerator before ``Z_Q`` division."""
    maximum_degree = int(maximum_degree)
    fermions = hft_fermion_series(maximum_degree)
    euler = euler_scalar_series(maximum_degree)
    inverse_vector = inverse_vector_tower(maximum_degree)
    euler_fermions = hft_so9.multiply_formal_series(
        [euler, fermions], maximum_degree
    )
    ground = fermions[0]
    numerator = {
        degree: euler_fermions[degree] - ground * inverse_vector[degree]
        for degree in range(maximum_degree + 1)
    }
    if numerator[0] != B4(0):
        raise ValueError("The massless ground term did not cancel")
    return {
        "fermions": fermions,
        "euler": euler,
        "inverse_vector": inverse_vector,
        "ground": ground,
        "numerator": numerator,
    }


def filtered_remainder_numerator(maximum_degree):
    """Return the explicit numerator for the level-one-vector remainder.

    If ``F`` is defined by ``R=PE(qV)F``, then

        q Z_Q F
        = PE(q^2/(1-q)V) phi S - S(0) PE(-qV).
    """
    maximum_degree = int(maximum_degree)
    core_data = filtered_core_numerator(maximum_degree)
    higher_vectors = hft_pieri_hazard.higher_vector_tower(maximum_degree)
    positive_part = hft_so9.multiply_formal_series(
        [higher_vectors, core_data["euler"], core_data["fermions"]],
        maximum_degree,
    )
    inverse_level_one = inverse_level_one_vector(maximum_degree)
    numerator = {
        degree: positive_part[degree]
        - core_data["ground"] * inverse_level_one[degree]
        for degree in range(maximum_degree + 1)
    }
    if numerator[0] != B4(0):
        raise ValueError("The remainder numerator ground term did not cancel")
    return {
        **core_data,
        "higher_vectors": higher_vectors,
        "inverse_level_one": inverse_level_one,
        "remainder_numerator": numerator,
    }


def convolve_primary_with_inverse_vector(single_levels, max_level):
    """Remove every positive vector oscillator mode from the HFT primaries."""
    maximum_degree = int(max_level) - 1
    primaries = {
        degree: single_levels[degree + 1]
        for degree in range(maximum_degree + 1)
    }
    inverse = inverse_vector_tower(maximum_degree)
    core = {
        degree: sum(
            (
                inverse[inverse_degree]
                * primaries[degree - inverse_degree]
                for inverse_degree in range(degree + 1)
            ),
            B4(0),
        )
        for degree in range(maximum_degree + 1)
    }
    return {
        "primaries": primaries,
        "inverse_vector": inverse,
        "core": core,
    }


def numerator_identity_audit(max_level=13):
    """Verify the Euler--fermion identity and filtered core through a cutoff."""
    max_level = int(max_level)
    if max_level < 1:
        raise ValueError("max_level must be positive")
    maximum_degree = max_level - 1
    _hft_numerator, single_levels = hft_so9.derive_hft_spectrum(max_level)
    direct = convolve_primary_with_inverse_vector(single_levels, max_level)
    explicit = filtered_remainder_numerator(max_level)

    zq_failures = []
    for degree in range(maximum_degree + 1):
        left = hft_so9.Z_Q * direct["core"][degree]
        right = explicit["numerator"][degree + 1]
        if left != right:
            zq_failures.append(
                {"core_degree": degree, "left": left, "right": right}
            )

    level_one_factorization = regge_factorization.factor_symmetric_vector_tower(
        single_levels, max_level
    )
    remainder_zq_failures = []
    for degree in range(maximum_degree + 1):
        left = hft_so9.Z_Q * level_one_factorization["remainder"][degree]
        right = explicit["remainder_numerator"][degree + 1]
        if left != right:
            remainder_zq_failures.append(
                {"remainder_degree": degree, "left": left, "right": right}
            )
    higher_factorization = hft_pieri_hazard.factor_higher_vector_tower(
        level_one_factorization["remainder"]
    )
    factorization_failures = tuple(
        degree
        for degree in range(maximum_degree + 1)
        if direct["core"][degree]
        != higher_factorization["core"][degree]
    )
    support = hft_pieri_hazard.filtered_character_audit(direct["core"])
    return {
        "max_level": max_level,
        "direct": direct,
        "explicit": explicit,
        "zq_failures": tuple(zq_failures),
        "remainder_zq_failures": tuple(remainder_zq_failures),
        "factorization_failures": factorization_failures,
        "support_audit": support,
        "all_identities": (
            not zq_failures
            and not remainder_zq_failures
            and not factorization_failures
        ),
        "all_checks": (
            not zq_failures
            and not remainder_zq_failures
            and not factorization_failures
            and support["all_satisfy"]
        ),
    }


def run_analysis(max_level=13):
    """Run the exact all-vector-free HFT core audit."""
    started = time.time()
    result = numerator_identity_audit(max_level)
    support = result["support_audit"]
    print("=" * 100)
    print("TK6B.5e — ALL-VECTOR-FREE HFT CORE")
    print("=" * 100)
    print(f"Physical HFT levels: 1 through {max_level}")
    print(
        "Euler--fermion numerator / qZ_Q identity failures: "
        f"{len(result['zq_failures'])}"
    )
    print(
        "Explicit level-one-remainder numerator identity failures: "
        f"{len(result['remainder_zq_failures'])}"
    )
    print(
        "Direct/full versus two-stage vector factorization failures: "
        f"{len(result['factorization_failures'])}"
    )
    print(
        "Core irreducible terms/filter failures: "
        f"{support['tested']}/{len(support['failures'])}"
    )
    print(
        "Core negative coefficients/minimum support margin: "
        f"{support['negative_coefficients']}/{support['minimum_margin']}"
    )
    print("Protected SO(10) baseline imported: NO")
    print(f"Runtime: {time.time() - started:.3f}s")
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Audit the all-vector-free HFT filtered core"
    )
    parser.add_argument("--max-level", type=int, default=13)
    args = parser.parse_args(argv)
    try:
        result = run_analysis(args.max_level)
    except Exception as error:
        print(f"TK6B.5e filtered core FAILED: {error}", file=sys.stderr)
        return 1
    return 0 if result["all_checks"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
