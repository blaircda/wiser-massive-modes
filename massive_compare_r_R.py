"""
massive_compare_r_R.py

Comparison of Plethystic Logarithm of perturbative spectrum r(q)
and cumulative spectrum R(q) in both SO(10) (D5) and SO(9) (B4).

Verifies:
1. PL_SO10[R(q)] - PL_SO10[r(q)] == 1 * q
2. branch_{D5 -> B4}(PL_SO10[R(q)]) - 1_{SO9} * q == PL_SO9[r(q)]
for both Total (R_B + R_F) and Super-Graded (R_B - R_F) series through order q^9 (levels 1-10).

Can optionally generate supplemental signed-coefficient tables under scratch/.
"""

import argparse
import os

from sage.all import WeylCharacterRing, QQ
from massive_SO10 import SO10_SUPERMULTIPLETS_DYNKIN
from plethystic_series import (
    compute_log_coefficients, compute_plethystic_log
)

D5 = WeylCharacterRing("D5", base_ring=QQ, style="coroots")
B4 = WeylCharacterRing("B4", base_ring=QQ, style="coroots")


def parse_b4_coroots(mon):
    rep = repr(mon)
    inner = rep[rep.find("(") + 1 : rep.rfind(")")]
    return tuple(int(x.strip()) for x in inner.split(","))


def decompose_b4_term(char):
    pos_items = []
    neg_items = []
    for wt, coeff in char.monomial_coefficients().items():
        mon = B4.monomial(wt)
        coroots = parse_b4_coroots(mon)
        dim = int(mon.degree())
        c = int(coeff)
        if c > 0:
            pos_items.append((c, dim, coroots))
        elif c < 0:
            neg_items.append((-c, dim, coroots))
    pos_items.sort(key=lambda x: (x[1], x[2]))
    neg_items.sort(key=lambda x: (x[1], x[2]))
    return pos_items, neg_items


def format_table(pos_items, neg_items):
    lines = []
    lines.append("| Type | Mult | Dim | Dynkin $(a_1, a_2, a_3, a_4)$ |")
    lines.append("| :--- | :---: | :---: | :--- |")
    for c, dim, coroots in pos_items:
        lines.append(f"| **Positive term (+)** | {c} | {dim:,} | `{coroots}` |")
    for c, dim, coroots in neg_items:
        lines.append(f"| **Negative term (-)** | {c} | {dim:,} | `{coroots}` |")
    if not pos_items and not neg_items:
        lines.append("| None | - | - | - |")
    return "\n".join(lines)


def run_comparisons():
    print("=" * 72)
    print("COMPARING PL[r(q)] AND PL[R(q)] ACROSS SO(10) AND SO(9)")
    print("=" * 72)

    results = {}
    for super_g in [False, True]:
        sign = -1 if super_g else 1
        label = "Super-Graded (R_B - R_F)" if super_g else "Total (R_B + R_F)"
        print(f"\nEvaluating {label}...")

        # 1. Construct R in SO(10)
        R_so10 = {0: D5(0, 0, 0, 0, 0)}
        for lvl in range(1, 11):
            c = D5(0)
            for mult, dim, coroots in SO10_SUPERMULTIPLETS_DYNKIN[lvl]["bosons"]:
                c += mult * D5(*coroots)
            for mult, dim, coroots in SO10_SUPERMULTIPLETS_DYNKIN[lvl]["fermions"]:
                c += sign * mult * D5(*coroots)
            R_so10[lvl - 1] = c

        # 2. Construct r in SO(10): r_1 = R_1, r_n = R_n - R_{n-1}
        r_so10 = {0: D5(0, 0, 0, 0, 0)}
        for n in range(1, 10):
            r_so10[n] = R_so10[n] - R_so10[n - 1]

        # 3. Compute PL in SO(10)
        PL_R10 = compute_plethystic_log(compute_log_coefficients(R_so10, 9), 9)
        PL_r10 = compute_plethystic_log(compute_log_coefficients(r_so10, 9), 9)

        # Verify SO(10) theorem: PL[R] - PL[r] == 1 * q
        assert PL_R10[1] - PL_r10[1] == D5(0, 0, 0, 0, 0), "Mismatch at q^1 in SO(10)"
        for n in range(2, 10):
            assert PL_R10[n] == PL_r10[n], f"Mismatch at q^{n} in SO(10)"
        print("  [PASSED] SO(10) identity: PL[R] - PL[r] == 1*q holds exactly at all 9 orders.")

        # 4. Construct r in SO(9)
        r_so9 = {0: B4(0, 0, 0, 0)}
        for n in range(1, 10):
            r_so9[n] = r_so10[n].branch(B4, rule="default")

        # 5. Compute PL in SO(9)
        PL_r9 = compute_plethystic_log(compute_log_coefficients(r_so9, 9), 9)

        # Verify Branching theorem: branch(PL_R10) - 1_{SO9} * q == PL_r9
        assert PL_R10[1].branch(B4, rule="default") - PL_r9[1] == B4(0, 0, 0, 0), "Mismatch at q^1 in SO(9)"
        for n in range(2, 10):
            assert PL_R10[n].branch(B4, rule="default") == PL_r9[n], f"Mismatch at q^{n} in SO(9)"
        print("  [PASSED] SO(9) branching commutativity: branch(PL[R]) - 1*q == PL[r] holds exactly at all 9 orders.")

        results[super_g] = {
            "PL_r9": PL_r9,
            "PL_R10": PL_R10,
            "PL_r10": PL_r10
        }

    return results


def generate_report_2(results):
    target_path = os.path.join(
        os.path.dirname(__file__),
        "scratch",
        "plethystic_baseline_tables.md",
    )
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    out = []
    out.append("# Supplemental Baseline-Dependent Plethystic Tables\n")
    out.append("**Date:** September 2026  ")
    out.append("**Status:** Descriptive tables from protected level-1--10 data  ")
    out.append("**Scope:**")
    out.append("1. Comparison of $\\operatorname{PL}[r(q)]$ and $\\operatorname{PL}[R(q)]$ in $SO(10)$ (virtual series).")
    out.append("2. Direct computation of $\\operatorname{PL}_{SO(9)}[r(q)]$ from the perturbative string Fock space and verification of the Branching Commutativity Theorem:")
    out.append("   $$\\operatorname{branch}_{D_5 \\to B_4}(\\operatorname{PL}_{SO(10)}[R(q)]) - \\mathbf{1}_{SO(9)} q \\equiv \\operatorname{PL}_{SO(9)}[r(q)].$$")
    out.append("3. Verification across both Total ($R_B + R_F$) and Super-Graded ($R_B - R_F$) representations through order $q^9$ (levels 1-10).  \n")
    out.append("---\n")

    out.append("## 1. Executive Summary & Main Findings\n")
    out.append("This report compares the signed coefficients of $\\operatorname{PL}[R(q)]$ and $\\operatorname{PL}[r(q)]$. The signs are formal representation-ring data and are not interpreted here as geometric generators, relations, or syzygies.\n")
    out.append("### Key Results:")
    out.append("1. **The Algebraic Subtraction Theorem (in $SO(10)$):**")
    out.append("   When $r(q) = (1-q)R(q)$ is treated as a virtual series in $\\mathcal{R}(SO(10))$, its Plethystic Logarithm is **strictly identical** to $\\operatorname{PL}[R(q)]$ at every order $q^n$ for $n \\ge 2$:")
    out.append("   $$\\operatorname{PL}[r(q)]_n = \\operatorname{PL}[R(q)]_n \\quad (\\forall n \\ge 2).$$")
    out.append("   The two series differ **only at order $q^1$**, where the coefficient $+ \\mathbf{10}$ is replaced by $\\mathbf{10} - \\mathbf{1}$:")
    out.append("   $$\\operatorname{PL}[R(q)] - \\operatorname{PL}[r(q)] = \\mathbf{1} q.$$")
    out.append("2. **The Branching Commutativity Theorem (in $SO(9)$):**")
    out.append("   When $r(q)$ is computed directly as genuine positive representations of $SO(9)$ ($B_4$) from the string oscillator Fock space:")
    out.append("   $$\\operatorname{branch}_{D_5 \\to B_4}\\Big(\\operatorname{PL}_{SO(10)}[R(q)]\\Big) - \\mathbf{1}_{SO(9)} q \\equiv \\operatorname{PL}_{SO(9)}\\Big[r(q)\\Big].$$")
    out.append("   Every signed coefficient in $SO(9)$ is the restriction of the corresponding formal $SO(10)$ coefficient.")
    out.append("3. **Interpretive limit:**")
    out.append("   - The higher-order signed PL coefficients are already present in the perturbative series $r(q)$. No geometric meaning is inferred from an individual negative coefficient such as $-\\mathbf{126}$.")
    out.append("   - The Bars factor contributes exactly one formal singlet term $+\\mathbf{1}q$ to the plethystic logarithm. This identity alone does not prove $SO(10)$ positivity.\n")

    out.append("## 2. Mathematical Proof of Identity\n")
    out.append("In any representation ring $\\mathcal{R}$, the Plethystic Exponential satisfies $\\operatorname{PE}[A + B] = \\operatorname{PE}[A] \\cdot \\operatorname{PE}[B]$, which implies that $\\operatorname{PL}[A \\cdot B] = \\operatorname{PL}[A] + \\operatorname{PL}[B]$.")
    out.append("Since:")
    out.append("$$R(q) = \\frac{r(q)}{1-q} = r(q) \\cdot \\frac{1}{1-q},$$")
    out.append("and:")
    out.append("$$\\frac{1}{1-q} = 1 + q + q^2 + \\cdots = \\operatorname{PE}[\\mathbf{1} q],$$")
    out.append("we have:")
    out.append("$$\\operatorname{PL}[R(q)] = \\operatorname{PL}[r(q)] + \\operatorname{PL}\\left[\\frac{1}{1-q}\\right] = \\operatorname{PL}[r(q)] + \\mathbf{1} q.$$")
    out.append("Rearranging:")
    out.append("$$\\operatorname{PL}[r(q)] = \\operatorname{PL}[R(q)] - \\mathbf{1} q.$$")
    out.append("Since the correction $-\\mathbf{1}q$ is strictly degree 1, all orders $q^2, q^3, \\dots, q^9$ are mathematically identical.\n")
    out.append("Furthermore, because restriction to a subgroup $\\operatorname{branch}_{D_5 \\to B_4}: \\mathcal{R}(D_5) \\to \\mathcal{R}(B_4)$ is a ring homomorphism that commutes with Adams operations ($\\operatorname{branch}(\\Psi^k(V)) = \\Psi^k(\\operatorname{branch}(V))$), the identity descends faithfully to $SO(9)$.\n")

    out.append("## 3. Verification Summary Across All 9 Orders\n")
    out.append("| Order | Massive Level | $SO(10)$: $\\operatorname{PL}[R]_n - \\operatorname{PL}[r]_n$ | $SO(9)$: $\\operatorname{branch}(\\operatorname{PL}[R]_n) - \\operatorname{PL}_{SO(9)}[r]_n$ | Status |")
    out.append("| :---: | :---: | :---: | :---: | :---: |")
    out.append("| $q^1$ | Level  2 | $+ \\mathbf{1}_{SO(10)}$ | $+ \\mathbf{1}_{SO(9)}$ | **EXACT THEOREM MATCH** |")
    for n in range(2, 10):
        out.append(f"| $q^{n}$ | Level {n+1:2d} | $0$ (Identical) | $0$ (Identical) | **EXACT THEOREM MATCH** |")
    out.append("\nBoth the Total ($R_B + R_F$) and Super-Graded ($R_B - R_F$) cases satisfy this theorem exactly.\n")

    out.append("---\n")
    out.append("## 4. Explicit Representation Tables for $\\operatorname{PL}_{SO(9)}[r(q)]$ (Total $r_B + r_F$)\n")
    out.append("Here we list the positive and negative signed coefficients of the **perturbative string spectrum $r(q)$** directly in $SO(9)$ ($B_4$).")
    out.append("Notice that at $q^1$, the vector $\\mathbf{9} = (1,0,0,0)$ appears (since $\\mathbf{10} \\to \\mathbf{9} \\oplus \\mathbf{1}$, and the singlet $\\mathbf{1}$ is subtracted).\n")

    PL_r9_tot = results[False]["PL_r9"]
    for n in range(1, 10):
        pos_items, neg_items = decompose_b4_term(PL_r9_tot[n])
        pos_dim = sum(c * dim for c, dim, _ in pos_items)
        neg_dim = sum(c * dim for c, dim, _ in neg_items)
        out.append(f"### Order $q^{n}$ (Oscillator Level {n+1})\n")
        out.append(f"- **Summary:** +{len(pos_items)} positive terms (gross dim {pos_dim:,}) | -{len(neg_items)} negative terms (gross dim {neg_dim:,}) | Net dim: {pos_dim - neg_dim:,}\n")
        out.append(format_table(pos_items, neg_items))
        out.append("\n")

    out.append("---\n")
    out.append("## 5. Explicit Representation Tables for $\\operatorname{PL}_{SO(9)}[r_B - r_F]$ (Super-Graded)\n")
    out.append("Below are the tables for the super-graded perturbative series in $SO(9)$:\n")

    PL_r9_sup = results[True]["PL_r9"]
    for n in range(1, 10):
        pos_items, neg_items = decompose_b4_term(PL_r9_sup[n])
        pos_dim = sum(c * dim for c, dim, _ in pos_items)
        neg_dim = sum(c * dim for c, dim, _ in neg_items)
        out.append(f"### Super-Graded Order $q^{n}$ (Oscillator Level {n+1})\n")
        out.append(f"- **Summary:** +{len(pos_items)} positive terms (gross dim {pos_dim:,}) | -{len(neg_items)} negative terms (gross dim {neg_dim:,}) | Net dim: {pos_dim - neg_dim:,}\n")
        out.append(format_table(pos_items, neg_items))
        out.append("\n")

    out.append("---\n")
    out.append("## 6. Execution Instructions\n")
    out.append("To reproduce this comparison at any time:\n")
    out.append("```bash")
    out.append("bin/sage-run massive_compare_r_R.py")
    out.append("```\n")

    content = "\n".join(out)
    with open(target_path, "w") as f:
        f.write(content)
        f.flush()
    print(f"Report written to: {target_path} ({len(content)} chars)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compare baseline-dependent plethystic series"
    )
    parser.add_argument(
        "--write-report",
        action="store_true",
        help="Write supplemental signed tables under scratch/",
    )
    args = parser.parse_args()
    res = run_comparisons()
    if args.write_report:
        generate_report_2(res)
