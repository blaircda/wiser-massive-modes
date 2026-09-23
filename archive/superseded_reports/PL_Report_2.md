# Waystone Report 2: Plethystic Analysis of Perturbative $r(q)$ vs. Cumulative $R(q)

> **Superseded (23 September 2026):** The formal identity
> $\operatorname{PL}[R]=\operatorname{PL}[r]+\mathbf 1q$ remains valid. The
> generator/relation, algebraic-variety and pure-spinor interpretations are
> withdrawn. See `PLETHYSTIC_STATUS.md`.

**Date:** September 2026  
**Status:** Complete & Exactly Verified  
**Scope:**
1. Comparison of $\operatorname{PL}[r(q)]$ and $\operatorname{PL}[R(q)]$ in $SO(10)$ (virtual series).
2. Direct computation of $\operatorname{PL}_{SO(9)}[r(q)]$ from the perturbative string Fock space and verification of the Branching Commutativity Theorem:
   $$\operatorname{branch}_{D_5 \to B_4}(\operatorname{PL}_{SO(10)}[R(q)]) - \mathbf{1}_{SO(9)} q \equiv \operatorname{PL}_{SO(9)}[r(q)].$$
3. Verification across both Total ($R_B + R_F$) and Super-Graded ($R_B - R_F$) representations through order $q^9$ (levels 1-10).  

---

## 1. Executive Summary & Main Findings

This report addresses the question: *Does the complex generator and syzygy structure observed in $\operatorname{PL}[R(q)]$ originate from the Bars cumulative summation $\frac{1}{1-q}$, or is it already inherent in the perturbative string spectrum $r(q)$?*

### Key Results:
1. **The Algebraic Subtraction Theorem (in $SO(10)$):**
   When $r(q) = (1-q)R(q)$ is treated as a virtual series in $\mathcal{R}(SO(10))$, its Plethystic Logarithm is **strictly identical** to $\operatorname{PL}[R(q)]$ at every order $q^n$ for $n \ge 2$:
   $$\operatorname{PL}[r(q)]_n = \operatorname{PL}[R(q)]_n \quad (\forall n \ge 2).$$
   The two series differ **only at order $q^1$**, where the vector generator $+ \mathbf{10}$ is replaced by $\mathbf{10} - \mathbf{1}$:
   $$\operatorname{PL}[R(q)] - \operatorname{PL}[r(q)] = \mathbf{1} q.$$
2. **The Branching Commutativity Theorem (in $SO(9)$):**
   When $r(q)$ is computed directly as genuine positive representations of $SO(9)$ ($B_4$) from the string oscillator Fock space:
   $$\operatorname{branch}_{D_5 \to B_4}\Big(\operatorname{PL}_{SO(10)}[R(q)]\Big) - \mathbf{1}_{SO(9)} q \equiv \operatorname{PL}_{SO(9)}\Big[r(q)\Big].$$
   Every generator ($+$) and relation ($-$) in $SO(9)$ is the exact restriction of an $SO(10)$ generator or relation!
3. **Physical Meaning:**
   - The entire tower of generators (spinors $\mathbf{16}$, 2-forms $\mathbf{45} \to \mathbf{9} \oplus \mathbf{36}$, vector-spinors $\mathbf{144} \to \mathbf{16} \oplus \mathbf{128}$) and relations (including the **pure spinor relation** $-\mathbf{126} \to -\mathbf{126}$) is **already fully present in the perturbative string spectrum $r(q)$**.
   - The Bars cumulative factor $\frac{1}{1-q}$ does not create or alter this algebraic variety: it simply provides the single singlet generator $\mathbf{1}q$ that cancels the on-shell singlet relation $-\mathbf{1}q^2$, allowing the cumulative sums to organize into genuine positive $SO(10)$ multiplets.

## 2. Mathematical Proof of Identity

In any representation ring $\mathcal{R}$, the Plethystic Exponential satisfies $\operatorname{PE}[A + B] = \operatorname{PE}[A] \cdot \operatorname{PE}[B]$, which implies that $\operatorname{PL}[A \cdot B] = \operatorname{PL}[A] + \operatorname{PL}[B]$.
Since:
$$R(q) = \frac{r(q)}{1-q} = r(q) \cdot \frac{1}{1-q},$$
and:
$$\frac{1}{1-q} = 1 + q + q^2 + \cdots = \operatorname{PE}[\mathbf{1} q],$$
we have:
$$\operatorname{PL}[R(q)] = \operatorname{PL}[r(q)] + \operatorname{PL}\left[\frac{1}{1-q}\right] = \operatorname{PL}[r(q)] + \mathbf{1} q.$$
Rearranging:
$$\operatorname{PL}[r(q)] = \operatorname{PL}[R(q)] - \mathbf{1} q.$$
Since the correction $-\mathbf{1}q$ is strictly degree 1, all orders $q^2, q^3, \dots, q^9$ are mathematically identical.

Furthermore, because restriction to a subgroup $\operatorname{branch}_{D_5 \to B_4}: \mathcal{R}(D_5) \to \mathcal{R}(B_4)$ is a ring homomorphism that commutes with Adams operations ($\operatorname{branch}(\Psi^k(V)) = \Psi^k(\operatorname{branch}(V))$), the identity descends faithfully to $SO(9)$.

## 3. Verification Summary Across All 9 Orders

| Order | Massive Level | $SO(10)$: $\operatorname{PL}[R]_n - \operatorname{PL}[r]_n$ | $SO(9)$: $\operatorname{branch}(\operatorname{PL}[R]_n) - \operatorname{PL}_{SO(9)}[r]_n$ | Status |
| :---: | :---: | :---: | :---: | :---: |
| $q^1$ | Level  2 | $+ \mathbf{1}_{SO(10)}$ | $+ \mathbf{1}_{SO(9)}$ | **EXACT THEOREM MATCH** |
| $q^2$ | Level  3 | $0$ (Identical) | $0$ (Identical) | **EXACT THEOREM MATCH** |
| $q^3$ | Level  4 | $0$ (Identical) | $0$ (Identical) | **EXACT THEOREM MATCH** |
| $q^4$ | Level  5 | $0$ (Identical) | $0$ (Identical) | **EXACT THEOREM MATCH** |
| $q^5$ | Level  6 | $0$ (Identical) | $0$ (Identical) | **EXACT THEOREM MATCH** |
| $q^6$ | Level  7 | $0$ (Identical) | $0$ (Identical) | **EXACT THEOREM MATCH** |
| $q^7$ | Level  8 | $0$ (Identical) | $0$ (Identical) | **EXACT THEOREM MATCH** |
| $q^8$ | Level  9 | $0$ (Identical) | $0$ (Identical) | **EXACT THEOREM MATCH** |
| $q^9$ | Level 10 | $0$ (Identical) | $0$ (Identical) | **EXACT THEOREM MATCH** |

Both the Total ($R_B + R_F$) and Super-Graded ($R_B - R_F$) cases satisfy this theorem exactly.

---

## 4. Explicit Representation Tables for $\operatorname{PL}_{SO(9)}[r(q)]$ (Total $r_B + r_F$)

Here we list the generators and relations of the **perturbative string spectrum $r(q)$** directly in $SO(9)$ ($B_4$).
Notice that at $q^1$, the vector $\mathbf{9} = (1,0,0,0)$ appears (since $\mathbf{10} \to \mathbf{9} \oplus \mathbf{1}$, and the singlet $\mathbf{1}$ is subtracted).

### Order $q^1$ (Oscillator Level 2)

- **Summary:** +1 generators (gross dim 9) | -0 relations (gross dim 0) | Net dim: 9

| Type | Mult | Dim | Dynkin $(a_1, a_2, a_3, a_4)$ |
| :--- | :---: | :---: | :--- |
| **Generator (+)** | 1 | 9 | `(1, 0, 0, 0)` |


### Order $q^2$ (Oscillator Level 3)

- **Summary:** +1 generators (gross dim 16) | -1 relations (gross dim 1) | Net dim: 15

| Type | Mult | Dim | Dynkin $(a_1, a_2, a_3, a_4)$ |
| :--- | :---: | :---: | :--- |
| **Generator (+)** | 1 | 16 | `(0, 0, 0, 1)` |
| **Relation (-)** | 1 | 1 | `(0, 0, 0, 0)` |


### Order $q^3$ (Oscillator Level 4)

- **Summary:** +2 generators (gross dim 45) | -1 relations (gross dim 16) | Net dim: 29

| Type | Mult | Dim | Dynkin $(a_1, a_2, a_3, a_4)$ |
| :--- | :---: | :---: | :--- |
| **Generator (+)** | 1 | 9 | `(1, 0, 0, 0)` |
| **Generator (+)** | 1 | 36 | `(0, 1, 0, 0)` |
| **Relation (-)** | 1 | 16 | `(0, 0, 0, 1)` |


### Order $q^4$ (Oscillator Level 5)

- **Summary:** +2 generators (gross dim 160) | -3 relations (gross dim 145) | Net dim: 15

| Type | Mult | Dim | Dynkin $(a_1, a_2, a_3, a_4)$ |
| :--- | :---: | :---: | :--- |
| **Generator (+)** | 2 | 16 | `(0, 0, 0, 1)` |
| **Generator (+)** | 1 | 128 | `(1, 0, 0, 1)` |
| **Relation (-)** | 1 | 1 | `(0, 0, 0, 0)` |
| **Relation (-)** | 2 | 9 | `(1, 0, 0, 0)` |
| **Relation (-)** | 1 | 126 | `(0, 0, 0, 2)` |


### Order $q^5$ (Oscillator Level 6)

- **Summary:** +7 generators (gross dim 703) | -3 relations (gross dim 736) | Net dim: -33

| Type | Mult | Dim | Dynkin $(a_1, a_2, a_3, a_4)$ |
| :--- | :---: | :---: | :--- |
| **Generator (+)** | 2 | 1 | `(0, 0, 0, 0)` |
| **Generator (+)** | 2 | 9 | `(1, 0, 0, 0)` |
| **Generator (+)** | 2 | 36 | `(0, 1, 0, 0)` |
| **Generator (+)** | 1 | 44 | `(2, 0, 0, 0)` |
| **Generator (+)** | 1 | 84 | `(0, 0, 1, 0)` |
| **Generator (+)** | 2 | 126 | `(0, 0, 0, 2)` |
| **Generator (+)** | 1 | 231 | `(1, 1, 0, 0)` |
| **Relation (-)** | 3 | 16 | `(0, 0, 0, 1)` |
| **Relation (-)** | 2 | 128 | `(1, 0, 0, 1)` |
| **Relation (-)** | 1 | 432 | `(0, 1, 0, 1)` |


### Order $q^6$ (Oscillator Level 7)

- **Summary:** +5 generators (gross dim 3,520) | -10 relations (gross dim 3,630) | Net dim: -110

| Type | Mult | Dim | Dynkin $(a_1, a_2, a_3, a_4)$ |
| :--- | :---: | :---: | :--- |
| **Generator (+)** | 7 | 16 | `(0, 0, 0, 1)` |
| **Generator (+)** | 6 | 128 | `(1, 0, 0, 1)` |
| **Generator (+)** | 3 | 432 | `(0, 1, 0, 1)` |
| **Generator (+)** | 1 | 576 | `(2, 0, 0, 1)` |
| **Generator (+)** | 1 | 768 | `(0, 0, 1, 1)` |
| **Relation (-)** | 3 | 1 | `(0, 0, 0, 0)` |
| **Relation (-)** | 4 | 9 | `(1, 0, 0, 0)` |
| **Relation (-)** | 4 | 36 | `(0, 1, 0, 0)` |
| **Relation (-)** | 3 | 44 | `(2, 0, 0, 0)` |
| **Relation (-)** | 4 | 84 | `(0, 0, 1, 0)` |
| **Relation (-)** | 4 | 126 | `(0, 0, 0, 2)` |
| **Relation (-)** | 2 | 231 | `(1, 1, 0, 0)` |
| **Relation (-)** | 1 | 495 | `(0, 2, 0, 0)` |
| **Relation (-)** | 1 | 594 | `(1, 0, 1, 0)` |
| **Relation (-)** | 1 | 924 | `(1, 0, 0, 2)` |


### Order $q^7$ (Oscillator Level 8)

- **Summary:** +14 generators (gross dim 18,131) | -7 relations (gross dim 18,032) | Net dim: 99

| Type | Mult | Dim | Dynkin $(a_1, a_2, a_3, a_4)$ |
| :--- | :---: | :---: | :--- |
| **Generator (+)** | 6 | 1 | `(0, 0, 0, 0)` |
| **Generator (+)** | 11 | 9 | `(1, 0, 0, 0)` |
| **Generator (+)** | 12 | 36 | `(0, 1, 0, 0)` |
| **Generator (+)** | 5 | 44 | `(2, 0, 0, 0)` |
| **Generator (+)** | 11 | 84 | `(0, 0, 1, 0)` |
| **Generator (+)** | 10 | 126 | `(0, 0, 0, 2)` |
| **Generator (+)** | 1 | 156 | `(3, 0, 0, 0)` |
| **Generator (+)** | 7 | 231 | `(1, 1, 0, 0)` |
| **Generator (+)** | 1 | 495 | `(0, 2, 0, 0)` |
| **Generator (+)** | 5 | 594 | `(1, 0, 1, 0)` |
| **Generator (+)** | 1 | 910 | `(2, 1, 0, 0)` |
| **Generator (+)** | 5 | 924 | `(1, 0, 0, 2)` |
| **Generator (+)** | 1 | 1,650 | `(0, 1, 1, 0)` |
| **Generator (+)** | 1 | 2,772 | `(0, 1, 0, 2)` |
| **Relation (-)** | 16 | 16 | `(0, 0, 0, 1)` |
| **Relation (-)** | 16 | 128 | `(1, 0, 0, 1)` |
| **Relation (-)** | 9 | 432 | `(0, 1, 0, 1)` |
| **Relation (-)** | 4 | 576 | `(2, 0, 0, 1)` |
| **Relation (-)** | 2 | 672 | `(0, 0, 0, 3)` |
| **Relation (-)** | 4 | 768 | `(0, 0, 1, 1)` |
| **Relation (-)** | 2 | 2,560 | `(1, 1, 0, 1)` |


### Order $q^8$ (Oscillator Level 9)

- **Summary:** +11 generators (gross dim 93,824) | -18 relations (gross dim 93,059) | Net dim: 765

| Type | Mult | Dim | Dynkin $(a_1, a_2, a_3, a_4)$ |
| :--- | :---: | :---: | :--- |
| **Generator (+)** | 39 | 16 | `(0, 0, 0, 1)` |
| **Generator (+)** | 45 | 128 | `(1, 0, 0, 1)` |
| **Generator (+)** | 30 | 432 | `(0, 1, 0, 1)` |
| **Generator (+)** | 15 | 576 | `(2, 0, 0, 1)` |
| **Generator (+)** | 7 | 672 | `(0, 0, 0, 3)` |
| **Generator (+)** | 15 | 768 | `(0, 0, 1, 1)` |
| **Generator (+)** | 1 | 1,920 | `(3, 0, 0, 1)` |
| **Generator (+)** | 9 | 2,560 | `(1, 1, 0, 1)` |
| **Generator (+)** | 1 | 4,608 | `(1, 0, 0, 3)` |
| **Generator (+)** | 1 | 4,928 | `(0, 2, 0, 1)` |
| **Generator (+)** | 3 | 5,040 | `(1, 0, 1, 1)` |
| **Relation (-)** | 13 | 1 | `(0, 0, 0, 0)` |
| **Relation (-)** | 27 | 9 | `(1, 0, 0, 0)` |
| **Relation (-)** | 31 | 36 | `(0, 1, 0, 0)` |
| **Relation (-)** | 14 | 44 | `(2, 0, 0, 0)` |
| **Relation (-)** | 28 | 84 | `(0, 0, 1, 0)` |
| **Relation (-)** | 30 | 126 | `(0, 0, 0, 2)` |
| **Relation (-)** | 4 | 156 | `(3, 0, 0, 0)` |
| **Relation (-)** | 20 | 231 | `(1, 1, 0, 0)` |
| **Relation (-)** | 5 | 495 | `(0, 2, 0, 0)` |
| **Relation (-)** | 20 | 594 | `(1, 0, 1, 0)` |
| **Relation (-)** | 3 | 910 | `(2, 1, 0, 0)` |
| **Relation (-)** | 18 | 924 | `(1, 0, 0, 2)` |
| **Relation (-)** | 6 | 1,650 | `(0, 1, 1, 0)` |
| **Relation (-)** | 2 | 2,457 | `(2, 0, 1, 0)` |
| **Relation (-)** | 1 | 2,574 | `(1, 2, 0, 0)` |
| **Relation (-)** | 6 | 2,772 | `(0, 1, 0, 2)` |
| **Relation (-)** | 2 | 3,900 | `(2, 0, 0, 2)` |
| **Relation (-)** | 1 | 4,158 | `(0, 0, 1, 2)` |


### Order $q^9$ (Oscillator Level 10)

- **Summary:** +24 generators (gross dim 491,337) | -14 relations (gross dim 490,368) | Net dim: 969

| Type | Mult | Dim | Dynkin $(a_1, a_2, a_3, a_4)$ |
| :--- | :---: | :---: | :--- |
| **Generator (+)** | 32 | 1 | `(0, 0, 0, 0)` |
| **Generator (+)** | 67 | 9 | `(1, 0, 0, 0)` |
| **Generator (+)** | 82 | 36 | `(0, 1, 0, 0)` |
| **Generator (+)** | 44 | 44 | `(2, 0, 0, 0)` |
| **Generator (+)** | 85 | 84 | `(0, 0, 1, 0)` |
| **Generator (+)** | 85 | 126 | `(0, 0, 0, 2)` |
| **Generator (+)** | 11 | 156 | `(3, 0, 0, 0)` |
| **Generator (+)** | 64 | 231 | `(1, 1, 0, 0)` |
| **Generator (+)** | 1 | 450 | `(4, 0, 0, 0)` |
| **Generator (+)** | 22 | 495 | `(0, 2, 0, 0)` |
| **Generator (+)** | 67 | 594 | `(1, 0, 1, 0)` |
| **Generator (+)** | 15 | 910 | `(2, 1, 0, 0)` |
| **Generator (+)** | 66 | 924 | `(1, 0, 0, 2)` |
| **Generator (+)** | 25 | 1,650 | `(0, 1, 1, 0)` |
| **Generator (+)** | 5 | 1,980 | `(0, 0, 2, 0)` |
| **Generator (+)** | 12 | 2,457 | `(2, 0, 1, 0)` |
| **Generator (+)** | 4 | 2,574 | `(1, 2, 0, 0)` |
| **Generator (+)** | 2 | 2,772 | `(0, 0, 0, 4)` |
| **Generator (+)** | 26 | 2,772 | `(0, 1, 0, 2)` |
| **Generator (+)** | 1 | 2,772 | `(3, 1, 0, 0)` |
| **Generator (+)** | 11 | 3,900 | `(2, 0, 0, 2)` |
| **Generator (+)** | 7 | 4,158 | `(0, 0, 1, 2)` |
| **Generator (+)** | 4 | 9,009 | `(1, 1, 1, 0)` |
| **Generator (+)** | 3 | 15,444 | `(1, 1, 0, 2)` |
| **Relation (-)** | 98 | 16 | `(0, 0, 0, 1)` |
| **Relation (-)** | 129 | 128 | `(1, 0, 0, 1)` |
| **Relation (-)** | 97 | 432 | `(0, 1, 0, 1)` |
| **Relation (-)** | 51 | 576 | `(2, 0, 0, 1)` |
| **Relation (-)** | 24 | 672 | `(0, 0, 0, 3)` |
| **Relation (-)** | 55 | 768 | `(0, 0, 1, 1)` |
| **Relation (-)** | 6 | 1,920 | `(3, 0, 0, 1)` |
| **Relation (-)** | 40 | 2,560 | `(1, 1, 0, 1)` |
| **Relation (-)** | 8 | 4,608 | `(1, 0, 0, 3)` |
| **Relation (-)** | 6 | 4,928 | `(0, 2, 0, 1)` |
| **Relation (-)** | 19 | 5,040 | `(1, 0, 1, 1)` |
| **Relation (-)** | 3 | 9,504 | `(2, 1, 0, 1)` |
| **Relation (-)** | 1 | 12,672 | `(0, 1, 0, 3)` |
| **Relation (-)** | 2 | 12,672 | `(0, 1, 1, 1)` |


---

## 5. Explicit Representation Tables for $\operatorname{PL}_{SO(9)}[r_B - r_F]$ (Super-Graded)

Below are the tables for the super-graded perturbative series in $SO(9)$:

### Super-Graded Order $q^1$ (Oscillator Level 2)

- **Summary:** +1 generators (gross dim 9) | -0 relations (gross dim 0) | Net dim: 9

| Type | Mult | Dim | Dynkin $(a_1, a_2, a_3, a_4)$ |
| :--- | :---: | :---: | :--- |
| **Generator (+)** | 1 | 9 | `(1, 0, 0, 0)` |


### Super-Graded Order $q^2$ (Oscillator Level 3)

- **Summary:** +0 generators (gross dim 0) | -2 relations (gross dim 17) | Net dim: -17

| Type | Mult | Dim | Dynkin $(a_1, a_2, a_3, a_4)$ |
| :--- | :---: | :---: | :--- |
| **Relation (-)** | 1 | 1 | `(0, 0, 0, 0)` |
| **Relation (-)** | 1 | 16 | `(0, 0, 0, 1)` |


### Super-Graded Order $q^3$ (Oscillator Level 4)

- **Summary:** +3 generators (gross dim 61) | -0 relations (gross dim 0) | Net dim: 61

| Type | Mult | Dim | Dynkin $(a_1, a_2, a_3, a_4)$ |
| :--- | :---: | :---: | :--- |
| **Generator (+)** | 1 | 9 | `(1, 0, 0, 0)` |
| **Generator (+)** | 1 | 16 | `(0, 0, 0, 1)` |
| **Generator (+)** | 1 | 36 | `(0, 1, 0, 0)` |


### Super-Graded Order $q^4$ (Oscillator Level 5)

- **Summary:** +0 generators (gross dim 0) | -5 relations (gross dim 289) | Net dim: -289

| Type | Mult | Dim | Dynkin $(a_1, a_2, a_3, a_4)$ |
| :--- | :---: | :---: | :--- |
| **Relation (-)** | 1 | 9 | `(1, 0, 0, 0)` |
| **Relation (-)** | 2 | 16 | `(0, 0, 0, 1)` |
| **Relation (-)** | 1 | 36 | `(0, 1, 0, 0)` |
| **Relation (-)** | 1 | 84 | `(0, 0, 1, 0)` |
| **Relation (-)** | 1 | 128 | `(1, 0, 0, 1)` |


### Super-Graded Order $q^5$ (Oscillator Level 6)

- **Summary:** +10 generators (gross dim 1,439) | -0 relations (gross dim 0) | Net dim: 1,439

| Type | Mult | Dim | Dynkin $(a_1, a_2, a_3, a_4)$ |
| :--- | :---: | :---: | :--- |
| **Generator (+)** | 2 | 1 | `(0, 0, 0, 0)` |
| **Generator (+)** | 2 | 9 | `(1, 0, 0, 0)` |
| **Generator (+)** | 3 | 16 | `(0, 0, 0, 1)` |
| **Generator (+)** | 2 | 36 | `(0, 1, 0, 0)` |
| **Generator (+)** | 1 | 44 | `(2, 0, 0, 0)` |
| **Generator (+)** | 1 | 84 | `(0, 0, 1, 0)` |
| **Generator (+)** | 2 | 126 | `(0, 0, 0, 2)` |
| **Generator (+)** | 2 | 128 | `(1, 0, 0, 1)` |
| **Generator (+)** | 1 | 231 | `(1, 1, 0, 0)` |
| **Generator (+)** | 1 | 432 | `(0, 1, 0, 1)` |


### Super-Graded Order $q^6$ (Oscillator Level 7)

- **Summary:** +0 generators (gross dim 0) | -15 relations (gross dim 7,166) | Net dim: -7,166

| Type | Mult | Dim | Dynkin $(a_1, a_2, a_3, a_4)$ |
| :--- | :---: | :---: | :--- |
| **Relation (-)** | 4 | 1 | `(0, 0, 0, 0)` |
| **Relation (-)** | 5 | 9 | `(1, 0, 0, 0)` |
| **Relation (-)** | 7 | 16 | `(0, 0, 0, 1)` |
| **Relation (-)** | 3 | 36 | `(0, 1, 0, 0)` |
| **Relation (-)** | 3 | 44 | `(2, 0, 0, 0)` |
| **Relation (-)** | 3 | 84 | `(0, 0, 1, 0)` |
| **Relation (-)** | 5 | 126 | `(0, 0, 0, 2)` |
| **Relation (-)** | 6 | 128 | `(1, 0, 0, 1)` |
| **Relation (-)** | 2 | 231 | `(1, 1, 0, 0)` |
| **Relation (-)** | 3 | 432 | `(0, 1, 0, 1)` |
| **Relation (-)** | 1 | 495 | `(0, 2, 0, 0)` |
| **Relation (-)** | 1 | 576 | `(2, 0, 0, 1)` |
| **Relation (-)** | 1 | 594 | `(1, 0, 1, 0)` |
| **Relation (-)** | 1 | 768 | `(0, 0, 1, 1)` |
| **Relation (-)** | 1 | 924 | `(1, 0, 0, 2)` |


### Super-Graded Order $q^7$ (Oscillator Level 8)

- **Summary:** +21 generators (gross dim 36,163) | -0 relations (gross dim 0) | Net dim: 36,163

| Type | Mult | Dim | Dynkin $(a_1, a_2, a_3, a_4)$ |
| :--- | :---: | :---: | :--- |
| **Generator (+)** | 6 | 1 | `(0, 0, 0, 0)` |
| **Generator (+)** | 11 | 9 | `(1, 0, 0, 0)` |
| **Generator (+)** | 16 | 16 | `(0, 0, 0, 1)` |
| **Generator (+)** | 12 | 36 | `(0, 1, 0, 0)` |
| **Generator (+)** | 5 | 44 | `(2, 0, 0, 0)` |
| **Generator (+)** | 11 | 84 | `(0, 0, 1, 0)` |
| **Generator (+)** | 10 | 126 | `(0, 0, 0, 2)` |
| **Generator (+)** | 16 | 128 | `(1, 0, 0, 1)` |
| **Generator (+)** | 1 | 156 | `(3, 0, 0, 0)` |
| **Generator (+)** | 7 | 231 | `(1, 1, 0, 0)` |
| **Generator (+)** | 9 | 432 | `(0, 1, 0, 1)` |
| **Generator (+)** | 1 | 495 | `(0, 2, 0, 0)` |
| **Generator (+)** | 4 | 576 | `(2, 0, 0, 1)` |
| **Generator (+)** | 5 | 594 | `(1, 0, 1, 0)` |
| **Generator (+)** | 2 | 672 | `(0, 0, 0, 3)` |
| **Generator (+)** | 4 | 768 | `(0, 0, 1, 1)` |
| **Generator (+)** | 1 | 910 | `(2, 1, 0, 0)` |
| **Generator (+)** | 5 | 924 | `(1, 0, 0, 2)` |
| **Generator (+)** | 1 | 1,650 | `(0, 1, 1, 0)` |
| **Generator (+)** | 2 | 2,560 | `(1, 1, 0, 1)` |
| **Generator (+)** | 1 | 2,772 | `(0, 1, 0, 2)` |


### Super-Graded Order $q^8$ (Oscillator Level 9)

- **Summary:** +0 generators (gross dim 0) | -29 relations (gross dim 186,723) | Net dim: -186,723

| Type | Mult | Dim | Dynkin $(a_1, a_2, a_3, a_4)$ |
| :--- | :---: | :---: | :--- |
| **Relation (-)** | 10 | 1 | `(0, 0, 0, 0)` |
| **Relation (-)** | 24 | 9 | `(1, 0, 0, 0)` |
| **Relation (-)** | 39 | 16 | `(0, 0, 0, 1)` |
| **Relation (-)** | 35 | 36 | `(0, 1, 0, 0)` |
| **Relation (-)** | 13 | 44 | `(2, 0, 0, 0)` |
| **Relation (-)** | 32 | 84 | `(0, 0, 1, 0)` |
| **Relation (-)** | 26 | 126 | `(0, 0, 0, 2)` |
| **Relation (-)** | 45 | 128 | `(1, 0, 0, 1)` |
| **Relation (-)** | 3 | 156 | `(3, 0, 0, 0)` |
| **Relation (-)** | 20 | 231 | `(1, 1, 0, 0)` |
| **Relation (-)** | 30 | 432 | `(0, 1, 0, 1)` |
| **Relation (-)** | 4 | 495 | `(0, 2, 0, 0)` |
| **Relation (-)** | 15 | 576 | `(2, 0, 0, 1)` |
| **Relation (-)** | 20 | 594 | `(1, 0, 1, 0)` |
| **Relation (-)** | 7 | 672 | `(0, 0, 0, 3)` |
| **Relation (-)** | 15 | 768 | `(0, 0, 1, 1)` |
| **Relation (-)** | 4 | 910 | `(2, 1, 0, 0)` |
| **Relation (-)** | 18 | 924 | `(1, 0, 0, 2)` |
| **Relation (-)** | 5 | 1,650 | `(0, 1, 1, 0)` |
| **Relation (-)** | 1 | 1,920 | `(3, 0, 0, 1)` |
| **Relation (-)** | 3 | 2,457 | `(2, 0, 1, 0)` |
| **Relation (-)** | 9 | 2,560 | `(1, 1, 0, 1)` |
| **Relation (-)** | 1 | 2,574 | `(1, 2, 0, 0)` |
| **Relation (-)** | 7 | 2,772 | `(0, 1, 0, 2)` |
| **Relation (-)** | 1 | 3,900 | `(2, 0, 0, 2)` |
| **Relation (-)** | 1 | 4,158 | `(0, 0, 1, 2)` |
| **Relation (-)** | 1 | 4,608 | `(1, 0, 0, 3)` |
| **Relation (-)** | 1 | 4,928 | `(0, 2, 0, 1)` |
| **Relation (-)** | 3 | 5,040 | `(1, 0, 1, 1)` |


### Super-Graded Order $q^9$ (Oscillator Level 10)

- **Summary:** +38 generators (gross dim 981,705) | -0 relations (gross dim 0) | Net dim: 981,705

| Type | Mult | Dim | Dynkin $(a_1, a_2, a_3, a_4)$ |
| :--- | :---: | :---: | :--- |
| **Generator (+)** | 32 | 1 | `(0, 0, 0, 0)` |
| **Generator (+)** | 67 | 9 | `(1, 0, 0, 0)` |
| **Generator (+)** | 98 | 16 | `(0, 0, 0, 1)` |
| **Generator (+)** | 82 | 36 | `(0, 1, 0, 0)` |
| **Generator (+)** | 44 | 44 | `(2, 0, 0, 0)` |
| **Generator (+)** | 85 | 84 | `(0, 0, 1, 0)` |
| **Generator (+)** | 85 | 126 | `(0, 0, 0, 2)` |
| **Generator (+)** | 129 | 128 | `(1, 0, 0, 1)` |
| **Generator (+)** | 11 | 156 | `(3, 0, 0, 0)` |
| **Generator (+)** | 64 | 231 | `(1, 1, 0, 0)` |
| **Generator (+)** | 97 | 432 | `(0, 1, 0, 1)` |
| **Generator (+)** | 1 | 450 | `(4, 0, 0, 0)` |
| **Generator (+)** | 22 | 495 | `(0, 2, 0, 0)` |
| **Generator (+)** | 51 | 576 | `(2, 0, 0, 1)` |
| **Generator (+)** | 67 | 594 | `(1, 0, 1, 0)` |
| **Generator (+)** | 24 | 672 | `(0, 0, 0, 3)` |
| **Generator (+)** | 55 | 768 | `(0, 0, 1, 1)` |
| **Generator (+)** | 15 | 910 | `(2, 1, 0, 0)` |
| **Generator (+)** | 66 | 924 | `(1, 0, 0, 2)` |
| **Generator (+)** | 25 | 1,650 | `(0, 1, 1, 0)` |
| **Generator (+)** | 6 | 1,920 | `(3, 0, 0, 1)` |
| **Generator (+)** | 5 | 1,980 | `(0, 0, 2, 0)` |
| **Generator (+)** | 12 | 2,457 | `(2, 0, 1, 0)` |
| **Generator (+)** | 40 | 2,560 | `(1, 1, 0, 1)` |
| **Generator (+)** | 4 | 2,574 | `(1, 2, 0, 0)` |
| **Generator (+)** | 2 | 2,772 | `(0, 0, 0, 4)` |
| **Generator (+)** | 26 | 2,772 | `(0, 1, 0, 2)` |
| **Generator (+)** | 1 | 2,772 | `(3, 1, 0, 0)` |
| **Generator (+)** | 11 | 3,900 | `(2, 0, 0, 2)` |
| **Generator (+)** | 7 | 4,158 | `(0, 0, 1, 2)` |
| **Generator (+)** | 8 | 4,608 | `(1, 0, 0, 3)` |
| **Generator (+)** | 6 | 4,928 | `(0, 2, 0, 1)` |
| **Generator (+)** | 19 | 5,040 | `(1, 0, 1, 1)` |
| **Generator (+)** | 4 | 9,009 | `(1, 1, 1, 0)` |
| **Generator (+)** | 3 | 9,504 | `(2, 1, 0, 1)` |
| **Generator (+)** | 1 | 12,672 | `(0, 1, 0, 3)` |
| **Generator (+)** | 2 | 12,672 | `(0, 1, 1, 1)` |
| **Generator (+)** | 3 | 15,444 | `(1, 1, 0, 2)` |


---

## 6. Execution Instructions

To reproduce this comparison at any time:

```bash
bin/sage-run massive_compare_r_R.py
```
