"""
massive_plethystic_SO10.py

Investigation of the 11-dimensional structure hidden in the massive levels
of the type IIA superstring via character-valued Plethystic Logarithm (PL).

Computes PL[R(q)] directly in the representation ring of SO(10) (D5) without
reducing to dimensions, and verifies exact round-trip reconstruction PE[PL[R(q)]] == R(q)
through order q^9 (level 10).
"""

import time
from sage.all import (
    WeylCharacterRing, Rational, divisors, moebius
)
from massive_SO10 import SO10_SUPERMULTIPLETS_DYNKIN

# Initialize D5 with QQ base ring to support rational coefficients in PL/PE recurrences
D5 = WeylCharacterRing("D5", base_ring=Rational(1).parent(), style="coroots")


def parse_coroots(monomial):
    """Extract Dynkin coroots tuple from a monomial WeylCharacter."""
    rep = repr(monomial)
    inner = rep[rep.find("(") + 1 : rep.rfind(")")]
    return tuple(int(x.strip()) for x in inner.split(","))


def get_so10_character_qq(level, super_graded=False):
    """
    Construct the SO(10) character at a given level in D5 (with QQ coefficients).
    If super_graded=True, fermions enter with a minus sign (-1)^F.
    """
    char = D5(0)
    for mult, dim, coroots in SO10_SUPERMULTIPLETS_DYNKIN[level]["bosons"]:
        irrep = D5(*coroots)
        assert irrep.degree() == dim, f"Dimension mismatch: {irrep.degree()} != {dim}"
        char += mult * irrep

    sign = -1 if super_graded else 1
    for mult, dim, coroots in SO10_SUPERMULTIPLETS_DYNKIN[level]["fermions"]:
        irrep = D5(*coroots)
        assert irrep.degree() == dim, f"Dimension mismatch: {irrep.degree()} != {dim}"
        char += sign * mult * irrep
    return char


def compute_log_coefficients(b_dict, max_degree):
    """
    Compute L_n = [q^n] log(B(q)) for B(q) = 1 + sum_{n>=1} b_n q^n
    using the logarithmic derivative triangular recurrence:
        q B'(q) = B(q) * q L'(q)
        => n b_n = n L_n + sum_{j=1}^{n-1} j L_j * b_{n-j}
        => L_n = b_n - (1/n) * sum_{j=1}^{n-1} j L_j * b_{n-j}
    """
    L = {}
    for n in range(1, max_degree + 1):
        term = b_dict[n]
        for j in range(1, n):
            term -= Rational((j, n)) * (L[j] * b_dict[n - j])
        L[n] = term
    return L


def compute_plethystic_log(L_dict, max_degree):
    """
    Compute a_n = [q^n] PL[B(q)] via Möbius inversion of the Adams operator:
        a_n = sum_{k | n} (mu(k) / k) * Psi^k(L_{n/k})
    """
    a = {}
    parent = L_dict[1].parent() if 1 in L_dict else D5
    for n in range(1, max_degree + 1):
        val = parent(0)
        for k in divisors(n):
            coeff = Rational((moebius(k), k))
            val += coeff * (L_dict[n // k].adams_operator(k))
        a[n] = val
    return a


def compute_plethystic_exp(a_dict, max_degree):
    """
    Reconstruct B(q) = 1 + sum_{n>=1} b_n q^n from a_n = [q^n] PL[B(q)]
    using:
        L_n = sum_{k | n} (1 / k) * Psi^k(a_{n/k})
        b_n = L_n + (1/n) * sum_{j=1}^{n-1} j L_j * b_{n-j}
    """
    L_rec = {}
    parent = a_dict[1].parent() if 1 in a_dict else D5
    rank = parent.cartan_type().rank()
    b_rec = {0: parent(*([0] * rank))}
    for n in range(1, max_degree + 1):
        val = parent(0)
        for k in divisors(n):
            coeff = Rational((1, k))
            val += coeff * (a_dict[n // k].adams_operator(k))
        L_rec[n] = val

        term = L_rec[n]
        for j in range(1, n):
            term += Rational((j, n)) * (L_rec[j] * b_rec[n - j])
        b_rec[n] = term
    return b_rec


def decompose_pl_term(char):
    """Decompose a character in D5 into positive (generators) and negative (relations) irreps."""
    pos_items = []
    neg_items = []
    for wt, coeff in char.monomial_coefficients().items():
        mon = D5.monomial(wt)
        coroots = parse_coroots(mon)
        dim = int(mon.degree())
        c = int(coeff)
        if c > 0:
            pos_items.append((c, dim, coroots))
        elif c < 0:
            neg_items.append((-c, dim, coroots))

    pos_items.sort(key=lambda x: (x[1], x[2]))
    neg_items.sort(key=lambda x: (x[1], x[2]))
    return pos_items, neg_items


def run_analysis(max_level=10, super_graded=False):
    mode_name = "Super-Graded (R_B - R_F)" if super_graded else "Total (R_B + R_F)"
    print("=" * 72)
    print(f"PLETHYSTIC LOGARITHM ANALYSIS OF MASSIVE SO(10) MODES: {mode_name.upper()}")
    print("=" * 72)

    max_degree = max_level - 1  # level 1 is q^0, level 10 is q^9

    # Build series B(q) = 1 + sum_{n=1}^{max_degree} b_n q^n where b_n = R_{n+1}
    b = {0: D5(0, 0, 0, 0, 0)}
    for lvl in range(1, max_level + 1):
        b[lvl - 1] = get_so10_character_qq(lvl, super_graded=super_graded)

    t0 = time.time()
    print(f"\n[1/3] Computing formal logarithm coefficients L_n for n = 1..{max_degree}...")
    L = compute_log_coefficients(b, max_degree)
    print(f"      Logarithm computed in {time.time() - t0:.2f}s.")

    t1 = time.time()
    print(f"\n[2/3] Computing Plethystic Logarithm a_n = PL_n via Adams operations...")
    a = compute_plethystic_log(L, max_degree)
    print(f"      Plethystic Logarithm computed in {time.time() - t1:.2f}s.")

    t2 = time.time()
    print(f"\n[3/3] Exact Round-Trip Verification PE[PL[R(q)]] == R(q)...")
    b_rec = compute_plethystic_exp(a, max_degree)

    all_match = True
    for n in range(1, max_degree + 1):
        match = (b_rec[n] == b[n])
        status = "PASSED" if match else "FAILED"
        print(f"      Order q^{n} (Level {n+1:2d}): {status}")
        if not match:
            all_match = False

    assert all_match, "Reconstruction PE[PL[R(q)]] == R(q) FAILED!"
    print(f"      --> ALL ORDERS 1..{max_degree} RECONSTRUCT EXACTLY IN THE REPRESENTATION RING!")
    print(f"      Verification took {time.time() - t2:.2f}s.")

    print("\n" + "=" * 72)
    print("DETAILED REPRESENTATION-THEORETIC DECOMPOSITION OF PL[R(q)]")
    print("=" * 72)

    for n in range(1, max_degree + 1):
        pos_items, neg_items = decompose_pl_term(a[n])
        pos_dim = sum(c * dim for c, dim, _ in pos_items)
        neg_dim = sum(c * dim for c, dim, _ in neg_items)

        print(f"\n--- Order q^{n} (Oscillator Level {n+1}) ---")
        print(f"  Summary: +{len(pos_items)} generator irreps (dim {pos_dim}) | -{len(neg_items)} relation irreps (dim {neg_dim}) | Net dim: {pos_dim - neg_dim}")

        print("  GENERATORS (+):")
        if not pos_items:
            print("    None")
        for c, dim, coroots in pos_items:
            prefix = f"{c} * " if c > 1 else "     "
            print(f"    + {prefix}[dim {dim:6d}] Dynkin {coroots}")

        print("  RELATIONS (-):")
        if not neg_items:
            print("    None")
        for c, dim, coroots in neg_items:
            prefix = f"{c} * " if c > 1 else "     "
            print(f"    - {prefix}[dim {dim:6d}] Dynkin {coroots}")

    return a, b


if __name__ == "__main__" or "__file__" in globals():
    import sys
    args = sys.argv[1:] if "sys" in globals() else []
    if "--all" in args:
        run_analysis(max_level=10, super_graded=False)
        print("\n" * 2)
        run_analysis(max_level=10, super_graded=True)
    elif "--super" in args:
        run_analysis(max_level=10, super_graded=True)
    else:
        run_analysis(max_level=10, super_graded=False)
