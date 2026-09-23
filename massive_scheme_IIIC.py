"""
massive_scheme_IIIC.py

Implementation and Plethystic Analysis of Bars' Section III.C Higher Multiplicity Scheme
for the 11-Dimensional Uplift of Massive Type IIA Superstring Spectrum.

Key Relations:
  R^{III.C}(q) = R^{III.B}(q) * prod_{n=2}^infty 1/(1-q^n) = r(q) * prod_{n=1}^infty 1/(1-q^n)
  R^{III.C}_n = sum_{k=0}^{n-1} c_k R^{III.B}_{n-k}, where c_k = p(k) - p(k-1)
  PL[R^{III.C}(q)] = PL[R^{III.B}(q)] + sum_{n=2}^infty 1_{SO(10)} q^n
                   = PL[r(q)] + sum_{n=1}^infty 1_{SO(10)} q^n

Can be executed in SageMath:
  bin/sage-run massive_scheme_IIIC.py
or in standard Python 3 (dimensional & structural checks):
  python3 massive_scheme_IIIC.py
"""

import sys

# Precomputed partition function p(k) for k=0..12
PARTITIONS = [1, 1, 2, 3, 5, 7, 11, 15, 22, 30, 42, 56, 77]
C_COEFFS = [PARTITIONS[k] - (PARTITIONS[k - 1] if k > 0 else 0) for k in range(len(PARTITIONS))]

try:
    from massive_SO10 import SO10_SUPERMULTIPLETS_DYNKIN
except ImportError:
    # Running in standard Python without SageMath: extract dictionary directly from source
    import os
    base_path = os.path.join(os.path.dirname(__file__), "massive_SO10.py")
    with open(base_path, "r") as f:
        src = f.read()
    dict_start = src.find("SO10_SUPERMULTIPLETS_DYNKIN = {")
    dict_end = src.find("\n# ---", dict_start)
    loc = {}
    exec(src[dict_start:dict_end], loc)
    SO10_SUPERMULTIPLETS_DYNKIN = loc["SO10_SUPERMULTIPLETS_DYNKIN"]


def get_scheme_iiic_multiplets(max_level=10):
    """
    Construct the explicit SO(10) representations for Scheme III.C
    at each level n from 1 to max_level.
    Returns: dict level -> {'bosons': [(mult, dim, coroots), ...], 'fermions': [(mult, dim, coroots), ...]}
    """
    iiic_multiplets = {}
    for n in range(1, max_level + 1):
        bosons = {}
        fermions = {}
        for k in range(n):
            coeff = C_COEFFS[k]
            if coeff == 0:
                continue
            prev_lvl = n - k
            for mult, dim, coroots in SO10_SUPERMULTIPLETS_DYNKIN[prev_lvl]["bosons"]:
                key = (dim, coroots)
                bosons[key] = bosons.get(key, 0) + coeff * mult
            for mult, dim, coroots in SO10_SUPERMULTIPLETS_DYNKIN[prev_lvl]["fermions"]:
                key = (dim, coroots)
                fermions[key] = fermions.get(key, 0) + coeff * mult

        b_list = [(mult, dim, coroots) for (dim, coroots), mult in bosons.items()]
        f_list = [(mult, dim, coroots) for (dim, coroots), mult in fermions.items()]
        b_list.sort(key=lambda x: (x[1], x[2]))
        f_list.sort(key=lambda x: (x[1], x[2]))
        iiic_multiplets[n] = {"bosons": b_list, "fermions": f_list}
    return iiic_multiplets


def run_sage_analysis():
    """Run exact character-valued plethystic analysis in SageMath."""
    from sage.all import WeylCharacterRing, Rational
    from plethystic_series import (
        compute_log_coefficients, compute_plethystic_log, compute_plethystic_exp,
    )

    D5 = WeylCharacterRing("D5", base_ring=Rational(1).parent(), style="coroots")
    singlet = D5(0, 0, 0, 0, 0)

    print("=" * 76)
    print("SAGE VERIFICATION: BARS' SCHEME III.C HIGHER MULTIPLICITY SPECTRUM IN SO(10)")
    print("=" * 76)

    iiic_reps = get_scheme_iiic_multiplets(10)

    for super_g in [False, True]:
        sign = -1 if super_g else 1
        label = "Super-Graded (R_B - R_F)" if super_g else "Total (R_B + R_F)"
        print(f"\n--- Analyzing {label} ---")

        # 1. Build R^{III.B} and R^{III.C} series
        R_B = {0: singlet}
        R_C = {0: singlet}
        for lvl in range(1, 11):
            cB = D5(0)
            for mult, dim, coroots in SO10_SUPERMULTIPLETS_DYNKIN[lvl]["bosons"]:
                cB += mult * D5(*coroots)
            for mult, dim, coroots in SO10_SUPERMULTIPLETS_DYNKIN[lvl]["fermions"]:
                cB += sign * mult * D5(*coroots)
            R_B[lvl - 1] = cB

            cC = D5(0)
            for mult, dim, coroots in iiic_reps[lvl]["bosons"]:
                cC += mult * D5(*coroots)
            for mult, dim, coroots in iiic_reps[lvl]["fermions"]:
                cC += sign * mult * D5(*coroots)
            R_C[lvl - 1] = cC

        # 2. Compute PL series
        L_B = compute_log_coefficients(R_B, 9)
        PL_B = compute_plethystic_log(L_B, 9)

        L_C = compute_log_coefficients(R_C, 9)
        PL_C = compute_plethystic_log(L_C, 9)

        # 3. Verify Round-Trip Reconstruction: PE[PL[R_C]] == R_C
        R_C_rec = compute_plethystic_exp(PL_C, 9)
        for n in range(1, 10):
            assert R_C_rec[n] == R_C[n], f"Reconstruction failed at q^{n}"
        print("  [PASSED] 100% Exact PE[PL[R^{III.C}]] == R^{III.C} Round-Trip Reconstruction.")

        # 4. Verify Exact Cancellation Theorem:
        # PL[R^{III.C}]_1 == PL[R^{III.B}]_1
        # PL[R^{III.C}]_n == PL[R^{III.B}]_n + 1_{SO(10)} for n = 2..9
        assert PL_C[1] == PL_B[1], "Mismatch at q^1: extra mode should only appear at n>=2"
        for n in range(2, 10):
            diff = PL_C[n] - PL_B[n]
            assert diff == singlet, f"Mismatch at q^{n}: expected +1 singlet, got {diff}"
        print("  [PASSED] Exact Cancellation Theorem PL[R^{III.C}] == PL[R^{III.B}] + sum_{n=2}^9 1 q^n verified at all orders!")


def moebius(n):
    if n == 1:
        return 1
    p, d, temp = 0, 2, n
    while d * d <= temp:
        if temp % d == 0:
            p += 1
            temp //= d
            if temp % d == 0:
                return 0
        d += 1
    if temp > 1:
        p += 1
    return -1 if p % 2 == 1 else 1


def compute_PL_dim(series, order):
    """Compute dimensional Plethystic Logarithm via triangular recurrence and Möbius inversion."""
    L = {0: 0}
    for n in range(1, order + 1):
        s = series[n]
        for j in range(1, n):
            s -= (j / n) * L[j] * series[n - j]
        L[n] = s

    PL = {}
    for n in range(1, order + 1):
        val = 0
        for k in range(1, n + 1):
            if n % k == 0:
                val += (moebius(k) / k) * L[n // k]
        PL[n] = val
    return PL


def run_python_analysis():
    """Run pure Python verification of Scheme III.C structure, dimensions, and PL theorem."""
    print("=" * 76)
    print("PURE PYTHON VERIFICATION: BARS' SCHEME III.C HIGHER MULTIPLICITY SPECTRUM")
    print("=" * 76)

    iiic_reps = get_scheme_iiic_multiplets(10)

    print("\nLevel | Composition in Scheme III.B terms           | Boson Dim  | Fermion Dim| Net (B-F)")
    print("-" * 76)
    dim_RB_tot = {0: 1}
    dim_RC_tot = {0: 1}
    dim_RB_sup = {0: 1}
    dim_RC_sup = {0: 1}

    for n in range(1, 11):
        comp = [f"{C_COEFFS[k]}*R_B[{n-k}]" for k in range(n) if C_COEFFS[k] > 0]
        comp_str = " + ".join(comp)
        b_dim = sum(m * d for m, d, c in iiic_reps[n]["bosons"])
        f_dim = sum(m * d for m, d, c in iiic_reps[n]["fermions"])
        net = b_dim - f_dim
        print(f"{n:5d} | {comp_str:44s} | {b_dim:10,d} | {f_dim:10,d} | {net:9,d}")

        if n > 1:
            order = n - 1
            b_b = sum(m * d for m, d, c in SO10_SUPERMULTIPLETS_DYNKIN[n]["bosons"])
            f_b = sum(m * d for m, d, c in SO10_SUPERMULTIPLETS_DYNKIN[n]["fermions"])
            dim_RB_tot[order] = b_b + f_b
            dim_RB_sup[order] = b_b - f_b
            dim_RC_tot[order] = b_dim + f_dim
            dim_RC_sup[order] = net

    print("\nKey Algebraic Properties Verified:")
    print("1. All coefficients c_k = p(k) - p(k-1) are strictly non-negative integers:")
    print("   ", [f"c_{k}={C_COEFFS[k]}" for k in range(10)])
    print("2. For every supplied positive R^{III.B}_m input, the nonnegative convolution")
    print("   produces a positive R^{III.C}_n. All-orders positivity remains conditional on III.B.")

    print("\n--- Verifying Exact Plethystic Logarithm Cancellation Theorem ---")
    PL_RB_tot = compute_PL_dim(dim_RB_tot, 9)
    PL_RC_tot = compute_PL_dim(dim_RC_tot, 9)
    PL_RB_sup = compute_PL_dim(dim_RB_sup, 9)
    PL_RC_sup = compute_PL_dim(dim_RC_sup, 9)

    print("Order | Level | PL[R_B](tot) | PL[R_C](tot) | Diff(tot) | PL[R_B](sup) | PL[R_C](sup) | Diff(sup)")
    print("-" * 88)
    for order in range(1, 10):
        lvl = order + 1
        d_tot = round(PL_RC_tot[order] - PL_RB_tot[order], 6)
        d_sup = round(PL_RC_sup[order] - PL_RB_sup[order], 6)
        print(f"q^{order}   | {lvl:5d} | {PL_RB_tot[order]:12.1f} | {PL_RC_tot[order]:12.1f} | {d_tot:9.1f} | {PL_RB_sup[order]:12.1f} | {PL_RC_sup[order]:12.1f} | {d_sup:9.1f}")
        if order == 1:
            assert d_tot == 0.0 and d_sup == 0.0, "Mismatch at q^1"
        else:
            assert d_tot == 1.0 and d_sup == 1.0, f"Mismatch at q^{order}: expected +1.0"
    print("\n[PASSED] Numerical dimensional check through all 9 available orders.")


if __name__ == "__main__":
    try:
        import sage.all
        run_sage_analysis()
    except ImportError:
        run_python_analysis()
