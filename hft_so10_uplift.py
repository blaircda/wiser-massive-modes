"""
hft_so10_uplift.py

SO(10) Closed-Form Numerator Uplift and Quotient Obstruction Diagnostic
========================================================================

This module implements:
  - Milestone M3: Independent construction of the SO(10) Hanany-Forcella-Troost (HFT)
    closed-form numerator Z^10_Left(q), and proof of the coefficient-by-coefficient
    branching identity:
        Res_{SO(10) -> SO(9)} Z^10_Left(q) == Z^9_Left(q)  (Levels 1 to 10).
  - A bounded diagnostic for the proposed Milestone M4 character division by the
    virtual character Z_Q^10.  The diagnostic stops on repeated peeling or after a
    caller-selected step limit and reports the unresolved remainder.

This module deliberately does not import any baseline spectrum.  It does not claim
to reconstruct Bars' SO(10) multiplets.  Baseline comparisons are isolated in
verify_hft_so10_against_baseline.py.

References:
  - Hanany, Forcella, Troost (arXiv:1007.2622 [hep-th])
  - Bars (hep-th/9503228)
"""

import sys
import time
import argparse

from sage.all import *

# ==============================================================================
# 1. Setup Lie Algebra Representation Rings
# ==============================================================================

D5 = WeylCharacterRing("D5", base_ring=QQ, style="coroots")
B4 = WeylCharacterRing("B4", base_ring=QQ, style="coroots")

# SO(10) Chiral Spinor 16_+ (highest weight [0,0,0,0,1])
S10 = D5(0, 0, 0, 0, 1)

# SO(10) Defining Vector 10 (highest weight [1,0,0,0,0])
VEC10 = D5(1, 0, 0, 0, 0)
ONE10 = D5(0, 0, 0, 0, 0)

# Virtual Transverse Vector V_10 = [1,0,0,0,0] - 2 * [0,0,0,0,0]
# Transverse dimension: 10 - 2 = 8.
V10 = VEC10 - 2 * ONE10

# Exterior powers of the defining vector 10 in D5
WEDGE_10 = [
    D5(0, 0, 0, 0, 0),                       # wedge^0: 1
    D5(1, 0, 0, 0, 0),                       # wedge^1: 10
    D5(0, 1, 0, 0, 0),                       # wedge^2: 45
    D5(0, 0, 1, 0, 0),                       # wedge^3: 120
    D5(0, 0, 0, 1, 1),                       # wedge^4: 210
    D5(0, 0, 0, 2, 0) + D5(0, 0, 0, 0, 2),   # wedge^5: 126_c + 126_s = 252
    D5(0, 0, 0, 1, 1),                       # wedge^6: 210
    D5(0, 0, 1, 0, 0),                       # wedge^7: 120
    D5(0, 1, 0, 0, 0),                       # wedge^8: 45
    D5(1, 0, 0, 0, 0),                       # wedge^9: 10
    D5(0, 0, 0, 0, 0),                       # wedge^10: 1
]


# ==============================================================================
# 2. Closed-Form Transverse Powers in SO(10)
# ==============================================================================

def get_sym_v10(k):
    """
    Closed-form symmetric power Sym^k(V_10) for V_10 = [1,0,0,0,0] - 2:
        Sym^k(V_10) = [k,0,0,0,0] + 2 * sum_{j=0}^{k-1} (-1)^(k-j) [j,0,0,0,0].
    """
    if k == 0:
        return ONE10
    res = D5(k, 0, 0, 0, 0)
    for j in range(k):
        sign = (-1) ** (k - j)
        res += 2 * sign * D5(j, 0, 0, 0, 0)
    return res


def get_lambda_true_v10(max_j):
    """
    Fermionic exterior powers Lambda_j(V_10) = [f^j] PE_F[f * V_10] in D5:
        PE_F[f * V_10] = (sum_{m=0}^10 f^m wedge^m(10)) / (1 + f)^2
                       = sum_{m=0}^10 f^m wedge^m(10) * sum_{k=0}^infty (-1)^k (k+1) f^k.
    """
    coeffs = []
    for j in range(max_j + 1):
        c = D5(0)
        for m in range(min(j + 1, 11)):
            k = j - m
            factor = (-1) ** k * (k + 1)
            c += factor * WEDGE_10[m]
        coeffs.append(c)
    return coeffs


def multiply_formal_series_d5(poly_list, max_deg):
    """Multiply formal power series of D5 characters truncated at max_deg."""
    res = {0: ONE10}
    for p in poly_list:
        new_res = {}
        for deg1, c1 in res.items():
            for deg2, c2 in p.items():
                d = deg1 + deg2
                if d <= max_deg:
                    new_res[d] = new_res.get(d, D5(0)) + c1 * c2
        res = new_res
    return {i: res.get(i, D5(0)) for i in range(max_deg + 1)}


# ==============================================================================
# 3. Generating Function Evaluation in SO(10)
# ==============================================================================

def compute_hft_d5(max_level):
    """
    Evaluate the independent SO(10) HFT chiral partition function through max_level.
    Returns:
        P10: dict mapping level n (1..max_level) to numerator character N_n^10.
    """
    N = max_level
    sym_cache = {k: get_sym_v10(k) for k in range(N + 1)}
    lambda_cache = get_lambda_true_v10(max(2 * N + 1, 25))

    # 1. Bosonic partition function Z_B(q):
    boson_factors = [
        {m * k: sym_cache[k] for k in range(N // m + 1)}
        for m in range(1, N + 1)
    ]
    ZB = multiply_formal_series_d5(boson_factors, N)

    # 2. Fermionic Ramond partition function Z_F(q):
    fermion_r_factors = [
        {m * j: lambda_cache[j] for j in range(N // m + 1)}
        for m in range(1, N + 1)
    ]
    ZF = multiply_formal_series_d5(fermion_r_factors, N)

    # 3. Fermionic Neveu-Schwarz partition function Z_NS(q):
    max_t_deg = 2 * N + 1
    fermion_ns_factors = [
        {freq * j: lambda_cache[j] for j in range(max_t_deg // freq + 1)}
        for freq in [2 * k + 1 for k in range(N + 1)]
        if freq <= max_t_deg
    ]
    ZF_t = multiply_formal_series_d5(fermion_ns_factors, max_t_deg)
    Z_NS = {j: ZF_t.get(2 * j + 1, D5(0)) for j in range(N + 1)}

    # 4. Total chiral partition function:
    #    Z_Left^10 = Z_B * ( Z_NS + 1/2 S10 * Z_F )
    S_poly = {n: Z_NS[n] + (Rational(1) / 2) * S10 * ZF[n] for n in range(N + 1)}
    P10 = multiply_formal_series_d5([ZB, S_poly], N)

    return P10


# ==============================================================================
# 4. Bounded Quotient Diagnostic
# ==============================================================================

def ambient_to_d5(x):
    """Convert ambient highest weight tuple (x0,x1,x2,x3,x4) to D5 Dynkin labels."""
    a1 = x[0] - x[1]
    a2 = x[1] - x[2]
    a3 = x[2] - x[3]
    a4 = x[3] - x[4]
    a5 = x[3] + x[4]
    return D5(a1, a2, a3, a4, a5)


def dominant_D5_weight(x):
    """Check if ambient weight x is in the dominant Weyl chamber of D5."""
    return x[0] >= x[1] >= x[2] >= x[3] >= abs(x[4])


def attempt_quotient_rn(N_n, Z_Q_10, max_steps=50, repeat_limit=4):
    """
    Attempt highest-weight peeling of N_n^10 by the virtual character Z_Q_10.

    This is a diagnostic, not a derivation.  Negative terms in Z_Q_10 destroy the
    monotone dominance order used by the successful SO(9) division.  To guarantee
    termination, stop after max_steps or when the same quotient candidate is
    selected repeat_limit consecutive times.

    Returns (quotient, remainder, diagnostic), where diagnostic has keys
    ``status``, ``steps``, and ``last_candidate``.  Status is one of ``exact``,
    ``no_candidate``, ``repeated_candidate``, or ``step_limit``.
    """
    rem = N_n
    r_n = D5(0)
    previous_candidate = None
    consecutive_repeats = 0

    for step in range(max_steps):
        if rem == D5(0):
            return r_n, rem, {
                "status": "exact",
                "steps": step,
                "last_candidate": previous_candidate,
            }

        coeffs = rem.monomial_coefficients()
        candidates = []
        for w, c in coeffs.items():
            if c != 0 and dominant_D5_weight(w):
                if w[0] >= 2 and all(isinstance(val, (int, Integer)) for val in w):
                    cand_hw = (w[0] - 2, w[1], w[2], w[3], w[4])
                    if dominant_D5_weight(cand_hw):
                        candidates.append((tuple(w), cand_hw, c, False))
                elif w[0] >= 1.5 and all(not isinstance(val, (int, Integer)) for val in w):
                    cand_hw = (w[0] - 1.5, w[1] - 0.5, w[2] - 0.5, w[3] - 0.5, w[4] - 0.5)
                    if dominant_D5_weight(cand_hw):
                        candidates.append((tuple(w), cand_hw, c, True))

        if not candidates:
            return r_n, rem, {
                "status": "no_candidate",
                "steps": step,
                "last_candidate": previous_candidate,
            }

        candidates.sort(key=lambda item: item[0], reverse=True)
        _, cand_hw, coeff, _is_ferm = candidates[0]
        candidate_signature = (tuple(cand_hw), coeff)
        if candidate_signature == previous_candidate:
            consecutive_repeats += 1
        else:
            previous_candidate = candidate_signature
            consecutive_repeats = 1

        if consecutive_repeats >= repeat_limit:
            return r_n, rem, {
                "status": "repeated_candidate",
                "steps": step,
                "last_candidate": candidate_signature,
            }

        irrep = ambient_to_d5(cand_hw)
        r_n += coeff * irrep
        rem -= coeff * irrep * Z_Q_10

    return r_n, rem, {
        "status": "step_limit",
        "steps": max_steps,
        "last_candidate": previous_candidate,
    }


# ==============================================================================
# 5. Pipeline Execution and Milestone Verification
# ==============================================================================

def run_uplift_pipeline(
    max_level=10,
    verbose=False,
    max_quotient_steps=50,
    diagnose_all_levels=False,
):
    print("=" * 80)
    print("HFT SO(10) NUMERATOR UPLIFT & BOUNDED QUOTIENT DIAGNOSTIC")
    print(f"Target: Mass Levels 1 through {max_level}")
    print("=" * 80)

    t_start = time.time()

    # Step 1: Compute SO(10) Numerator
    print(f"\n[1/4] Evaluating independent HFT SO(10) chiral partition function (order q^{max_level})...")
    t0 = time.time()
    P10 = compute_hft_d5(max_level)
    print(f"      SO(10) numerator evaluated in {time.time() - t0:.3f}s.")

    # Universal massive supermultiplet Z_Q^10 = N_1^10
    Z_Q_10 = P10[1]
    print(f"      Z_Q^10 identified: dimension = {int(Z_Q_10.degree())} (dim 128_B + 128_F = 256).")

    # Step 2: Compute SO(9) Numerator
    print(f"\n[2/4] Independently evaluating HFT SO(9) generating function...")
    t0 = time.time()
    import hft_so9
    P9 = hft_so9.compute_hft_numerator(max_level)
    print(f"      SO(9) numerator evaluated in {time.time() - t0:.3f}s.")

    # Step 3: Verify Milestone M3 (Branching Identity)
    print(f"\n[3/4] Verifying Milestone M3: Res_{{SO(10)->SO(9)}} Z_Left^10 == Z_Left^9 ...")
    print("-" * 80)
    print(f"{'Level':<7}{'dim(SO10)':<12}{'dim(SO9)':<12}{'Res(Z^10)==Z^9':<20}{'Status'}")
    print("-" * 80)
    m3_pass = True
    for n in range(1, max_level + 1):
        p10_br = P10[n].branch(B4)
        diff = p10_br - P9[n]
        match = (diff == 0)
        if not match:
            m3_pass = False
        d10 = int(P10[n].degree())
        d9 = int(P9[n].degree())
        print(f"{n:<7}{d10:<12}{d9:<12}{str(match):<20}{'PASS' if match else 'FAIL'}")

    print("-" * 80)
    print(f"Milestone M3 Result: {'[PASSED]' if m3_pass else '[FAILED]'}")

    # Step 4: Attempt the proposed quotient without baseline seeding.
    print("\n[4/4] Diagnosing direct division by the virtual SO(10) character Z_Q^10...")
    print("-" * 96)
    print(f"{'Level':<7}{'Status':<22}{'Steps':<9}{'Exact':<9}{'Remainder Res=0':<19}{'Quotient Res=r9'}")
    print("-" * 96)

    quotient_results = {}
    for n in range(1, max_level + 1):
        quotient, remainder, diagnostic = attempt_quotient_rn(
            P10[n], Z_Q_10, max_steps=max_quotient_steps
        )
        exact = remainder == D5(0)
        remainder_branch_zero = remainder.branch(B4) == B4(0)
        derived_r9 = hft_so9.divide_by_zq(P9[n])
        quotient_branch_match = quotient.branch(B4) == derived_r9
        quotient_results[n] = (quotient, remainder, diagnostic)
        print(
            f"{n:<7}{diagnostic['status']:<22}{diagnostic['steps']:<9}"
            f"{str(exact):<9}{str(remainder_branch_zero):<19}{quotient_branch_match}"
        )
        if verbose and not exact:
            print(f"      last candidate: {diagnostic['last_candidate']}")
            print(f"      remainder dimension: {remainder.degree()}")
        if not exact and not diagnose_all_levels:
            print(
                "      Stopping at the first non-exact quotient; this is sufficient "
                "to show that the proposed forward pipeline does not reconstruct all levels."
            )
            break

    print("-" * 96)
    print(f"Total execution time: {time.time() - t_start:.3f}s")
    print("=" * 80)
    print("\nCURRENT MILESTONE STATUS:")
    print(f"  * Milestone M3 (Independent SO(10) Numerator Uplift): {'[PASSED]' if m3_pass else '[FAILED]'}")
    print("  * Milestone M4 (Direct quotient reconstruction):      [UNRESOLVED]")
    print("  * Baseline data imported:                              NO")
    print("=" * 80)

    return m3_pass


if __name__ == "__main__" or (__name__ == "sage.all" and len(sys.argv) > 0 and "hft_so10_uplift" in sys.argv[0]):
    parser = argparse.ArgumentParser(description="HFT SO(10) Uplift & Bars Reconstruction")
    parser.add_argument("--max-level", type=int, default=10, help="Maximum mass level (default: 10)")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    parser.add_argument(
        "--max-quotient-steps",
        type=int,
        default=50,
        help="Hard limit for each quotient diagnostic (default: 50)",
    )
    parser.add_argument(
        "--diagnose-all-levels",
        action="store_true",
        help="Continue quotient diagnostics after the first non-exact level",
    )

    args_list = sys.argv[1:]
    if args_list and args_list[0].endswith(".py"):
        args_list = args_list[1:]
    args = parser.parse_args(args_list)

    success = run_uplift_pipeline(
        max_level=args.max_level,
        verbose=args.verbose,
        max_quotient_steps=args.max_quotient_steps,
        diagnose_all_levels=args.diagnose_all_levels,
    )
    sys.exit(0 if success else 1)
