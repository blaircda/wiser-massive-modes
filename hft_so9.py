#!/usr/bin/env python3
"""
hft_so9.py

Baseline-Free Hanany-Forcella-Troost (HFT) SO(9) Generating Function
and Universal Supermultiplet Character Division.

Reference:
    "The covariant perturbative string spectrum"
    Amihay Hanany, Davide Forcella, Jan Troost (arXiv:1007.2622)

This script implements:
1. Exact closed-form evaluation of the chiral partition function in B4:
     Z_B(q)  = PE[ q/(1-q) * ([1,0,0,0]_9 - 1) ]
     Z_F(q)  = PE_F[ q/(1-q) * ([1,0,0,0]_9 - 1) ]
     Z_NS(q) = 1/(2 sqrt(q)) * ( PE_F[ sqrt(q)/(1-q) * V_9 ] - PE_F[ -sqrt(q)/(1-q) * V_9 ] )
     Z_Left(q) = Z_B * ( Z_NS + 1/2 [0,0,0,1]_9 Z_F(q) )
2. Exact subtraction of the massless super-Yang-Mills sector:
     N(q) = Z_Left(q) - Z_0
3. Character polynomial division by the universal massive supermultiplet:
     Z_Q = [2,0,0,0]_9 + [1,0,0,1]_9 + [0,0,1,0]_9  (dim = 44 + 128 + 84 = 256)
     N_n = Z_Q * r_n  =>  solves for r_n in R(B4) via greedy highest-weight reduction.
4. Internal verification that every derived quotient satisfies N_n = Z_Q * r_n
   and is a positive integral SO(9) character.

This derivation module deliberately does not import any baseline SO(10) data.
Comparison with the human-established baseline is performed separately by
verify_hft_so9_against_baseline.py.

Usage:
    ./bin/sage-run hft_so9.py [--max-level N] [--verbose]
"""

import sys
import time
import argparse
from sage.all import *


# ==============================================================================
# 1. Algebraic & Representation Ring Setup
# ==============================================================================

B4 = WeylCharacterRing("B4", base_ring=QQ, style="coroots")

# Universal massive supermultiplet in B4 (dim = 44 + 128 + 84 = 256)
Z_Q = B4(2, 0, 0, 0) + B4(1, 0, 0, 1) + B4(0, 0, 1, 0)

# Spinor 16 in B4
S9 = B4(0, 0, 0, 1)

# Dominant highest weights of Z_Q
OMEGA_B = B4(2, 0, 0, 0).highest_weight()
OMEGA_F = B4(1, 0, 0, 1).highest_weight()


def dominant_B4(w):
    """Check if weight w is in the dominant Weyl chamber of B4."""
    x = w.to_vector()
    return x[0] >= x[1] >= x[2] >= x[3] >= 0


# ==============================================================================
# 2. Closed-Form Transverse Exterior & Symmetric Powers
# ==============================================================================

# Precomputed exterior powers of [1,0,0,0]_9 in B4
_WEDGE_9 = [
    B4(0, 0, 0, 0),  # 1
    B4(1, 0, 0, 0),  # 9
    B4(0, 1, 0, 0),  # 36
    B4(0, 0, 1, 0),  # 84
    B4(0, 0, 0, 2),  # 126
    B4(0, 0, 0, 2),  # 126
    B4(0, 0, 1, 0),  # 84
    B4(0, 1, 0, 0),  # 36
    B4(1, 0, 0, 0),  # 9
    B4(0, 0, 0, 0),  # 1
]

# Transverse exterior powers Lambda_j = wedge^j(8_v) in B4:
# (1 + f) * sum_{j=0}^8 f^j Lambda_j = sum_{j=0}^9 f^j wedge^j(9)
LAMBDA = [_WEDGE_9[0]]
for _j in range(1, 9):
    LAMBDA.append(_WEDGE_9[_j] - LAMBDA[_j - 1])


def get_sym_v(k):
    """
    Compute the k-th symmetric power of the virtual transverse vector
    V_9 = [1,0,0,0]_9 - 1 in B4:
        Sym^k(V_9) = sum_{j=0}^{floor(k/2)} ( [k-2j,0,0,0]_9 - [k-2j-1,0,0,0]_9 ).
    """
    if k == 0:
        return B4(0, 0, 0, 0)
    res = B4(0)
    for j in range(k // 2 + 1):
        p = k - 2 * j
        res += B4(p, 0, 0, 0)
        if p - 1 >= 0:
            res -= B4(p - 1, 0, 0, 0)
    return res


def multiply_formal_series(poly_list, max_deg):
    """Multiply formal power series of characters truncated at max_deg."""
    res = {0: B4(0, 0, 0, 0)}
    for p in poly_list:
        new_res = {}
        for deg1, c1 in res.items():
            for deg2, c2 in p.items():
                d = deg1 + deg2
                if d <= max_deg:
                    new_res[d] = new_res.get(d, B4(0)) + c1 * c2
        res = new_res
    return {i: res.get(i, B4(0)) for i in range(max_deg + 1)}


# ==============================================================================
# 3. Generating Function Evaluation
# ==============================================================================

def compute_hft_numerator(max_level):
    """
    Evaluate the HFT chiral partition function and subtract massless ground state.
    Returns:
        P: dict mapping mass level n (1..max_level) to the numerator character P_n.
    """
    N = max_level
    sym_cache = {k: get_sym_v(k) for k in range(N + 1)}

    # 1. Bosonic partition function Z_B(q):
    #    Z_B(q) = prod_{m=1}^N ( sum_k q^(m*k) Sym^k(V_9) )
    boson_factors = [
        {m * k: sym_cache[k] for k in range(N // m + 1)}
        for m in range(1, N + 1)
    ]
    ZB = multiply_formal_series(boson_factors, N)

    # 2. Fermionic partition function Z_F(q):
    #    Z_F(q) = prod_{m=1}^N ( sum_j q^(m*j) Lambda_j )
    fermion_r_factors = [
        {m * j: LAMBDA[j] for j in range(min(9, N // m + 1))}
        for m in range(1, N + 1)
    ]
    ZF = multiply_formal_series(fermion_r_factors, N)

    # 3. Fermionic Neveu-Schwarz partition function Z_NS(q):
    #    Product over odd frequencies (2k+1)/2 in powers of t = sqrt(q):
    max_t_deg = 2 * N + 1
    fermion_ns_factors = [
        {freq * j: LAMBDA[j] for j in range(min(9, max_t_deg // freq + 1))}
        for freq in [2 * k + 1 for k in range(N + 1)]
        if freq <= max_t_deg
    ]
    ZF_t = multiply_formal_series(fermion_ns_factors, max_t_deg)
    Z_NS = {j: ZF_t.get(2 * j + 1, B4(0)) for j in range(N + 1)}

    # 4. Total chiral partition function:
    #    P(q) = Z_B * ( Z_NS + 1/2 S_9 * Z_F )
    S_poly = {n: Z_NS[n] + (Rational(1)/2) * S9 * ZF[n] for n in range(N + 1)}
    P = multiply_formal_series([ZB, S_poly], N)

    # Note: P[0] = V_9 + 1/2 S9 cancels identically against Z_0.
    # The massive numerator for n >= 1 is precisely P[n].
    return P


# ==============================================================================
# 4. Character Division by Universal Multiplet Z_Q
# ==============================================================================

def divide_by_zq(target_char):
    """
    Solve target_char = Z_Q * r_n for r_n in R(B4) via greedy highest-weight peeling.
    """
    rem = target_char
    r_decomp = B4(0)

    while rem != B4(0):
        coeffs = rem.monomial_coefficients()
        dom_weights = [w for w in coeffs if dominant_B4(w) and coeffs[w] > 0]
        if not dom_weights:
            raise ValueError(f"No positive dominant weight in remainder: {rem}")

        hw = max(dom_weights, key=lambda w: tuple(w.to_vector()))
        coeff = coeffs[hw]

        candidates = []
        for omega in [OMEGA_B, OMEGA_F]:
            q_hw = hw - omega
            if dominant_B4(q_hw):
                try:
                    q_irrep = B4(q_hw)
                    test = rem - coeff * (Z_Q * q_irrep)
                    if all(c >= 0 for c in test.monomial_coefficients().values()):
                        candidates.append(q_irrep)
                except Exception:
                    pass

        if len(candidates) != 1:
            raise ValueError(
                f"Could not uniquely determine candidate for hw={hw}. "
                f"Found {len(candidates)} candidates: {candidates}"
            )

        q_irrep = candidates[0]
        r_decomp += coeff * q_irrep
        rem -= coeff * (Z_Q * q_irrep)

    return r_decomp


# ==============================================================================
# 5. Baseline-Free Derivation Pipeline
# ==============================================================================

def derive_hft_spectrum(max_level):
    """Return the HFT numerator and independently derived r_n characters."""
    numerator = compute_hft_numerator(max_level)
    derived_r = {
        n: divide_by_zq(numerator[n])
        for n in range(1, max_level + 1)
    }
    return numerator, derived_r


def run_pipeline(max_level=10, verbose=False):
    print("=" * 80)
    print("HANANY-FORCELLA-TROOST (HFT) SO(9) CLOSED-FORM GENERATING FUNCTION")
    print(f"Target: Mass Levels 1 through {max_level}")
    print("=" * 80)

    t_start = time.time()

    # Step 1: Compute closed-form numerator
    print(f"\n[1/2] Evaluating HFT chiral partition function in B4 (order q^{max_level})...")
    t0 = time.time()
    P = compute_hft_numerator(max_level)
    print(f"      Closed-form numerator computed in {time.time() - t0:.3f}s.")

    # Step 2: Character division and internal verification
    print("\n[2/2] Performing character division N_n / Z_Q and verifying...")
    print("-" * 80)
    print(f"{'Level':<7}{'Dimension':<12}{'Check Z_Q*r=N':<18}{'Positive Integral':<20}{'Time':<10}")
    print("-" * 80)

    low_levels_pass = True
    high_levels_pass = True

    derived_r = {}

    for n in range(1, max_level + 1):
        t_n = time.time()
        r_n = divide_by_zq(P[n])
        dt = time.time() - t_n
        derived_r[n] = r_n

        zq_check = (Z_Q * r_n == P[n])
        coeffs = r_n.monomial_coefficients().values()
        positive_integral = all(c in ZZ and c >= 0 for c in coeffs)

        if n <= 5 and not (zq_check and positive_integral):
            low_levels_pass = False
        if n > 5 and not (zq_check and positive_integral):
            high_levels_pass = False

        dim_val = int(r_n.degree())
        print(f"{n:<7}{dim_val:<12}{str(zq_check):<18}{str(positive_integral):<20}{dt:.3f}s")

        if verbose:
            print(f"      r_{n} = {r_n}")

    print("-" * 80)
    print(f"Total pipeline execution time: {time.time() - t_start:.3f}s")
    print("=" * 80)

    print("\nBASELINE-FREE DERIVATION SUMMARY:")
    low_end = min(5, max_level)
    print(f"  * Levels 1-{low_end}: {'[PASSED]' if low_levels_pass else '[FAILED]'}")
    if max_level > 5:
        print(f"  * Levels 6-{max_level}: {'[PASSED]' if high_levels_pass else '[FAILED]'}")
    print("  * Baseline data imported: NO")
    print("=" * 80)

    return low_levels_pass and high_levels_pass


if __name__ == "__main__" or (__name__ == "sage.all" and len(sys.argv) > 0 and "hft_so9" in sys.argv[0]):
    parser = argparse.ArgumentParser(description="HFT SO(9) Generating Function & Character Division")
    parser.add_argument("--max-level", type=int, default=10, help="Maximum mass level to compute (default: 10)")
    parser.add_argument("--verbose", action="store_true", help="Print full character expressions at each level")

    # Filter argv if called via sage wrapper
    args_list = sys.argv[1:]
    if args_list and args_list[0].endswith(".py"):
        args_list = args_list[1:]
    args = parser.parse_args(args_list)

    success = run_pipeline(max_level=args.max_level, verbose=args.verbose)
    sys.exit(0 if success else 1)
