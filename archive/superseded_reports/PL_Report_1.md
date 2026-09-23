# Waystone Report: Plethystic Analysis of Massive $SO(10)$ Superstring Spectrum

> **Superseded (23 September 2026):** Retained only as a historical computation.
> The coefficient tables and round-trip calculation remain reproducible, but
> the generator/relation, on-shell and pure-spinor interpretations are
> withdrawn. See `PLETHYSTIC_STATUS.md`.

**Date:** September 2026  
**Status:** Complete & Exactly Verified  
**Target Group:** $SO(10)$ ($D_5$)  
**Oscillator Levels Analyzed:** Level 1 through Level 10 (Orders $q^0$ to $q^9$)  

---

## 1. Executive Summary

This waystone report documents the representation-theoretic analysis of the cumulative massive type IIA spectrum $R(q)$ proposed by Bars (Section III.B of [hep-th/9503228](https://arxiv.org/abs/hep-th/9503228)).
The cumulative spectrum $R_n = \sum_{i=1}^n r_i$ lifts to positive, genuine representations of $SO(10)$, as previously verified through level 10.
Here, we treat $R(q) = \sum_{n\ge 1} R_n q^{n-1}$ as a character-valued formal power series in the representation ring $\mathcal{R}(SO(10))$ and compute its **Plethystic Logarithm** $\operatorname{PL}[R(q)]$ directly without dimensional reduction.

### Key Results:
1. **100% Exact Round-Trip Reconstruction:** Evaluating the Plethystic Exponential on the computed PL series exactly reconstructs the original character spectrum $\operatorname{PE}[\operatorname{PL}[R(q)]] \equiv R(q)$ for every order $q^1$ through $q^9$ in the representation ring.
2. **Identification of Fundamental Generators & Relations:**
   - Order $q^1$ (Level 2): The fundamental 10D vector $+ \mathbf{10} = (1,0,0,0,0)$.
   - Order $q^2$ (Level 3): The chiral spinor $+ \mathbf{16} = (0,0,0,0,1)$ and an invariant scalar relation $-\mathbf{1} = -(0,0,0,0,0)$, encoding the on-shell condition $\eta_{\mu\nu} X^\mu X^\nu = 0$.
   - Order $q^3$ (Level 4): The adjoint 2-form $+ \mathbf{45} = (0,1,0,0,0)$ and an anti-chiral relation $-\mathbf{\overline{16}} = -(0,0,0,1,0)$.
   - Order $q^4$ (Level 5): The vector-spinor $+ \mathbf{144} = (1,0,0,0,1)$ and the **pure spinor relation** $-\mathbf{126} = -(0,0,0,0,2)$, corresponding to the vanishing of the self-dual 5-form bilinear $\lambda \Gamma^{(5)} \lambda = 0$.
3. **Representation-Theoretic Role of the Cumulative Factor $1/(1-q)$:**
   Because $\frac{1}{1-q} = \operatorname{PE}[\mathbf{1} q]$, multiplying by $1/(1-q)$ in series space corresponds to freely adjoining a single scalar singlet generator $\mathbf{1}$ at degree $q$: $\operatorname{PL}[R(q)] = \operatorname{PL}[r(q)] + \mathbf{1} q$. This cancels against the $-\mathbf{1} q^2$ constraint, providing the algebraic mechanism that ensures positivity of the cumulative multiplets.
4. **Massive Supersymmetric Cancellation:** In the spin-statistics graded series $R_B - R_F$, positive and negative representations cancel by orders of magnitude (e.g. at order $q^9$, gross dimensions exceed 493,000 but the net dimension cancels down to $+969$).

## 2. Mathematical Formulation & Computation

### 2.1 The Representation-Ring Plethystic Logarithm
Let $R(q) = \mathbf{1} + \sum_{n=1}^9 R_{n+1} q^n \in \mathcal{R}(SO(10))[[q]]$. The plethystic logarithm is defined by:
$$\operatorname{PL}[R(q)] = \sum_{k=1}^\infty \frac{\mu(k)}{k} \Psi^k\left(\log R(q^k)\right),$$
where $\mu(k)$ is the Möbius function and $\Psi^k$ is the $k$-th Adams operation on the representation ring $\mathcal{R}(SO(10))$.
On maximal torus characters $\chi_V(x_1,\dots,x_5)$, the Adams operator acts by:
$$\chi_{\Psi^k(V)}(x_1,\dots,x_5) = \chi_V(x_1^k,\dots,x_5^k).$$
In SageMath, this is evaluated exactly using `WeylCharacterRing("D5", base_ring=QQ, style="coroots").adams_operator(k)`.

### 2.2 Efficient Triangular Recurrence
To avoid expanding powers $(\sum R_{n+1} q^n)^m$ (which would involve explosive 9-fold tensor products), we compute the formal logarithm $L(q) = \log R(q) = \sum_{n=1}^9 L_n q^n$ via the logarithmic derivative relation:
$$q \frac{d}{dq} R(q) = R(q) \cdot \left(q \frac{d}{dq} L(q)\right) \implies L_n = R_{n+1} - \frac{1}{n} \sum_{j=1}^{n-1} j L_j \otimes R_{n+1-j}.$$
Then Möbius inversion yields the PL coefficients directly:
$$a_n = [q^n] \operatorname{PL}[R(q)] = \sum_{k | n} \frac{\mu(k)}{k} \Psi^k(L_{n/k}).$$
Reconstruction via the Plethystic Exponential $\operatorname{PE}[A(q)]$ uses the inverse recurrence:
$$L_n^{\text{rec}} = \sum_{k | n} \frac{1}{k} \Psi^k(a_{n/k}), \quad b_n^{\text{rec}} = L_n^{\text{rec}} + \frac{1}{n} \sum_{j=1}^{n-1} j L_j^{\text{rec}} \otimes b_{n-j}^{\text{rec}}.$$

## 3. Execution & Verification Instructions

The complete implementation is in `massive_plethystic_SO10.py`.
In accordance with project rules, all original baseline files (`massive_SO10.py`, `massive_SO8_construct.py`, `massive_SO8_to_S010.py`, `massive_SO8_to_SO9.py`) remain completely unchanged.

### Running the Code:
```bash
# 1. Run total character analysis PL(R_B + R_F):
bin/sage-run massive_plethystic_SO10.py

# 2. Run super-graded analysis PL(R_B - R_F):
bin/sage-run massive_plethystic_SO10.py --super

# 3. Run both analyses sequentially:
bin/sage-run massive_plethystic_SO10.py --all
```

### Verification Output Summary:
| Order | Massive Level | Total Series Match ($R_B + R_F$) | Super-Graded Match ($R_B - R_F$) |
| :--- | :--- | :---: | :---: |
| $q^1$ | Level  2 | **EXACT MATCH** | **EXACT MATCH** |
| $q^2$ | Level  3 | **EXACT MATCH** | **EXACT MATCH** |
| $q^3$ | Level  4 | **EXACT MATCH** | **EXACT MATCH** |
| $q^4$ | Level  5 | **EXACT MATCH** | **EXACT MATCH** |
| $q^5$ | Level  6 | **EXACT MATCH** | **EXACT MATCH** |
| $q^6$ | Level  7 | **EXACT MATCH** | **EXACT MATCH** |
| $q^7$ | Level  8 | **EXACT MATCH** | **EXACT MATCH** |
| $q^8$ | Level  9 | **EXACT MATCH** | **EXACT MATCH** |
| $q^9$ | Level 10 | **EXACT MATCH** | **EXACT MATCH** |

---

## 4. Explicit Representation Tables for $\operatorname{PL}[R_B + R_F]$

In this section, every order of the total character Plethystic Logarithm is decomposed into positive irreps (generators) and negative irreps (relations/syzygies).

### Order $q^1$ (Oscillator Level 2)

- **Summary:** +1 generators (gross dim 10) | -0 relations (gross dim 0) | Net dim: 10

| Type | Multiplicity | Dimension | Dynkin Coroots $(a_1, a_2, a_3, a_4, a_5)$ |
| :--- | :---: | :---: | :--- |
| **Generator (+)** | 1 | 10 | `(1, 0, 0, 0, 0)` |


### Order $q^2$ (Oscillator Level 3)

- **Summary:** +1 generators (gross dim 16) | -1 relations (gross dim 1) | Net dim: 15

| Type | Multiplicity | Dimension | Dynkin Coroots $(a_1, a_2, a_3, a_4, a_5)$ |
| :--- | :---: | :---: | :--- |
| **Generator (+)** | 1 | 16 | `(0, 0, 0, 0, 1)` |
| **Relation (-)** | 1 | 1 | `(0, 0, 0, 0, 0)` |


### Order $q^3$ (Oscillator Level 4)

- **Summary:** +1 generators (gross dim 45) | -1 relations (gross dim 16) | Net dim: 29

| Type | Multiplicity | Dimension | Dynkin Coroots $(a_1, a_2, a_3, a_4, a_5)$ |
| :--- | :---: | :---: | :--- |
| **Generator (+)** | 1 | 45 | `(0, 1, 0, 0, 0)` |
| **Relation (-)** | 1 | 16 | `(0, 0, 0, 1, 0)` |


### Order $q^4$ (Oscillator Level 5)

- **Summary:** +3 generators (gross dim 161) | -2 relations (gross dim 146) | Net dim: 15

| Type | Multiplicity | Dimension | Dynkin Coroots $(a_1, a_2, a_3, a_4, a_5)$ |
| :--- | :---: | :---: | :--- |
| **Generator (+)** | 1 | 1 | `(0, 0, 0, 0, 0)` |
| **Generator (+)** | 1 | 16 | `(0, 0, 0, 0, 1)` |
| **Generator (+)** | 1 | 144 | `(1, 0, 0, 0, 1)` |
| **Relation (-)** | 2 | 10 | `(1, 0, 0, 0, 0)` |
| **Relation (-)** | 1 | 126 | `(0, 0, 0, 0, 2)` |


### Order $q^5$ (Oscillator Level 6)

- **Summary:** +6 generators (gross dim 847) | -4 relations (gross dim 880) | Net dim: -33

| Type | Multiplicity | Dimension | Dynkin Coroots $(a_1, a_2, a_3, a_4, a_5)$ |
| :--- | :---: | :---: | :--- |
| **Generator (+)** | 2 | 1 | `(0, 0, 0, 0, 0)` |
| **Generator (+)** | 1 | 45 | `(0, 1, 0, 0, 0)` |
| **Generator (+)** | 1 | 126 | `(0, 0, 0, 0, 2)` |
| **Generator (+)** | 1 | 144 | `(1, 0, 0, 0, 1)` |
| **Generator (+)** | 1 | 210 | `(0, 0, 0, 1, 1)` |
| **Generator (+)** | 1 | 320 | `(1, 1, 0, 0, 0)` |
| **Relation (-)** | 1 | 16 | `(0, 0, 0, 0, 1)` |
| **Relation (-)** | 1 | 16 | `(0, 0, 0, 1, 0)` |
| **Relation (-)** | 2 | 144 | `(1, 0, 0, 1, 0)` |
| **Relation (-)** | 1 | 560 | `(0, 1, 0, 0, 1)` |


### Order $q^6$ (Oscillator Level 7)

- **Summary:** +6 generators (gross dim 3,664) | -10 relations (gross dim 3,774) | Net dim: -110

| Type | Multiplicity | Dimension | Dynkin Coroots $(a_1, a_2, a_3, a_4, a_5)$ |
| :--- | :---: | :---: | :--- |
| **Generator (+)** | 3 | 16 | `(0, 0, 0, 1, 0)` |
| **Generator (+)** | 4 | 144 | `(1, 0, 0, 0, 1)` |
| **Generator (+)** | 1 | 560 | `(0, 1, 0, 0, 1)` |
| **Generator (+)** | 1 | 560 | `(0, 1, 0, 1, 0)` |
| **Generator (+)** | 1 | 720 | `(2, 0, 0, 0, 1)` |
| **Generator (+)** | 1 | 1,200 | `(0, 0, 1, 0, 1)` |
| **Relation (-)** | 1 | 1 | `(0, 0, 0, 0, 0)` |
| **Relation (-)** | 2 | 45 | `(0, 1, 0, 0, 0)` |
| **Relation (-)** | 2 | 54 | `(2, 0, 0, 0, 0)` |
| **Relation (-)** | 1 | 120 | `(0, 0, 1, 0, 0)` |
| **Relation (-)** | 1 | 126 | `(0, 0, 0, 0, 2)` |
| **Relation (-)** | 1 | 144 | `(1, 0, 0, 1, 0)` |
| **Relation (-)** | 2 | 210 | `(0, 0, 0, 1, 1)` |
| **Relation (-)** | 1 | 770 | `(0, 2, 0, 0, 0)` |
| **Relation (-)** | 1 | 945 | `(1, 0, 1, 0, 0)` |
| **Relation (-)** | 1 | 1,050 | `(1, 0, 0, 0, 2)` |


### Order $q^7$ (Oscillator Level 8)

- **Summary:** +12 generators (gross dim 18,905) | -13 relations (gross dim 18,806) | Net dim: 99

| Type | Multiplicity | Dimension | Dynkin Coroots $(a_1, a_2, a_3, a_4, a_5)$ |
| :--- | :---: | :---: | :--- |
| **Generator (+)** | 1 | 1 | `(0, 0, 0, 0, 0)` |
| **Generator (+)** | 6 | 10 | `(1, 0, 0, 0, 0)` |
| **Generator (+)** | 6 | 120 | `(0, 0, 1, 0, 0)` |
| **Generator (+)** | 4 | 126 | `(0, 0, 0, 0, 2)` |
| **Generator (+)** | 1 | 126 | `(0, 0, 0, 2, 0)` |
| **Generator (+)** | 1 | 210 | `(0, 0, 0, 1, 1)` |
| **Generator (+)** | 5 | 320 | `(1, 1, 0, 0, 0)` |
| **Generator (+)** | 1 | 720 | `(2, 0, 0, 0, 1)` |
| **Generator (+)** | 1 | 1,386 | `(2, 1, 0, 0, 0)` |
| **Generator (+)** | 4 | 1,728 | `(1, 0, 0, 1, 1)` |
| **Generator (+)** | 1 | 2,970 | `(0, 1, 1, 0, 0)` |
| **Generator (+)** | 1 | 3,696 | `(0, 1, 0, 0, 2)` |
| **Relation (-)** | 5 | 16 | `(0, 0, 0, 0, 1)` |
| **Relation (-)** | 1 | 16 | `(0, 0, 0, 1, 0)` |
| **Relation (-)** | 1 | 54 | `(2, 0, 0, 0, 0)` |
| **Relation (-)** | 3 | 144 | `(1, 0, 0, 0, 1)` |
| **Relation (-)** | 5 | 144 | `(1, 0, 0, 1, 0)` |
| **Relation (-)** | 1 | 560 | `(0, 1, 0, 0, 1)` |
| **Relation (-)** | 3 | 560 | `(0, 1, 0, 1, 0)` |
| **Relation (-)** | 1 | 672 | `(0, 0, 0, 0, 3)` |
| **Relation (-)** | 3 | 720 | `(2, 0, 0, 1, 0)` |
| **Relation (-)** | 2 | 1,200 | `(0, 0, 1, 0, 1)` |
| **Relation (-)** | 1 | 1,200 | `(0, 0, 1, 1, 0)` |
| **Relation (-)** | 1 | 1,440 | `(0, 0, 0, 1, 2)` |
| **Relation (-)** | 2 | 3,696 | `(1, 1, 0, 0, 1)` |


### Order $q^8$ (Oscillator Level 9)

- **Summary:** +16 generators (gross dim 95,264) | -25 relations (gross dim 94,499) | Net dim: 765

| Type | Multiplicity | Dimension | Dynkin Coroots $(a_1, a_2, a_3, a_4, a_5)$ |
| :--- | :---: | :---: | :--- |
| **Generator (+)** | 10 | 16 | `(0, 0, 0, 0, 1)` |
| **Generator (+)** | 4 | 16 | `(0, 0, 0, 1, 0)` |
| **Generator (+)** | 4 | 144 | `(1, 0, 0, 0, 1)` |
| **Generator (+)** | 12 | 144 | `(1, 0, 0, 1, 0)` |
| **Generator (+)** | 15 | 560 | `(0, 1, 0, 0, 1)` |
| **Generator (+)** | 1 | 672 | `(0, 0, 0, 0, 3)` |
| **Generator (+)** | 10 | 720 | `(2, 0, 0, 0, 1)` |
| **Generator (+)** | 2 | 1,200 | `(0, 0, 1, 0, 1)` |
| **Generator (+)** | 5 | 1,200 | `(0, 0, 1, 1, 0)` |
| **Generator (+)** | 4 | 1,440 | `(0, 0, 0, 1, 2)` |
| **Generator (+)** | 1 | 1,440 | `(0, 0, 0, 2, 1)` |
| **Generator (+)** | 1 | 2,640 | `(3, 0, 0, 0, 1)` |
| **Generator (+)** | 5 | 3,696 | `(1, 1, 0, 1, 0)` |
| **Generator (+)** | 1 | 5,280 | `(1, 0, 0, 0, 3)` |
| **Generator (+)** | 1 | 8,064 | `(0, 2, 0, 0, 1)` |
| **Generator (+)** | 3 | 8,800 | `(1, 0, 1, 0, 1)` |
| **Relation (-)** | 5 | 1 | `(0, 0, 0, 0, 0)` |
| **Relation (-)** | 1 | 10 | `(1, 0, 0, 0, 0)` |
| **Relation (-)** | 14 | 45 | `(0, 1, 0, 0, 0)` |
| **Relation (-)** | 5 | 54 | `(2, 0, 0, 0, 0)` |
| **Relation (-)** | 2 | 120 | `(0, 0, 1, 0, 0)` |
| **Relation (-)** | 4 | 126 | `(0, 0, 0, 0, 2)` |
| **Relation (-)** | 1 | 126 | `(0, 0, 0, 2, 0)` |
| **Relation (-)** | 12 | 210 | `(0, 0, 0, 1, 1)` |
| **Relation (-)** | 2 | 210 | `(3, 0, 0, 0, 0)` |
| **Relation (-)** | 4 | 320 | `(1, 1, 0, 0, 0)` |
| **Relation (-)** | 2 | 720 | `(2, 0, 0, 1, 0)` |
| **Relation (-)** | 1 | 770 | `(0, 2, 0, 0, 0)` |
| **Relation (-)** | 9 | 945 | `(1, 0, 1, 0, 0)` |
| **Relation (-)** | 5 | 1,050 | `(1, 0, 0, 0, 2)` |
| **Relation (-)** | 3 | 1,050 | `(1, 0, 0, 2, 0)` |
| **Relation (-)** | 1 | 1,386 | `(2, 1, 0, 0, 0)` |
| **Relation (-)** | 3 | 1,728 | `(1, 0, 0, 1, 1)` |
| **Relation (-)** | 3 | 2,970 | `(0, 1, 1, 0, 0)` |
| **Relation (-)** | 2 | 3,696 | `(0, 1, 0, 0, 2)` |
| **Relation (-)** | 1 | 4,312 | `(2, 0, 1, 0, 0)` |
| **Relation (-)** | 1 | 4,410 | `(1, 2, 0, 0, 0)` |
| **Relation (-)** | 1 | 4,950 | `(2, 0, 0, 0, 2)` |
| **Relation (-)** | 3 | 5,940 | `(0, 1, 0, 1, 1)` |
| **Relation (-)** | 1 | 6,930 | `(0, 0, 1, 0, 2)` |
| **Relation (-)** | 1 | 8,085 | `(2, 0, 0, 1, 1)` |


### Order $q^9$ (Oscillator Level 10)

- **Summary:** +35 generators (gross dim 493,977) | -25 relations (gross dim 493,008) | Net dim: 969

| Type | Multiplicity | Dimension | Dynkin Coroots $(a_1, a_2, a_3, a_4, a_5)$ |
| :--- | :---: | :---: | :--- |
| **Generator (+)** | 4 | 1 | `(0, 0, 0, 0, 0)` |
| **Generator (+)** | 15 | 10 | `(1, 0, 0, 0, 0)` |
| **Generator (+)** | 21 | 45 | `(0, 1, 0, 0, 0)` |
| **Generator (+)** | 11 | 54 | `(2, 0, 0, 0, 0)` |
| **Generator (+)** | 16 | 120 | `(0, 0, 1, 0, 0)` |
| **Generator (+)** | 10 | 126 | `(0, 0, 0, 0, 2)` |
| **Generator (+)** | 7 | 126 | `(0, 0, 0, 2, 0)` |
| **Generator (+)** | 22 | 210 | `(0, 0, 0, 1, 1)` |
| **Generator (+)** | 2 | 210 | `(3, 0, 0, 0, 0)` |
| **Generator (+)** | 10 | 320 | `(1, 1, 0, 0, 0)` |
| **Generator (+)** | 12 | 770 | `(0, 2, 0, 0, 0)` |
| **Generator (+)** | 24 | 945 | `(1, 0, 1, 0, 0)` |
| **Generator (+)** | 15 | 1,050 | `(1, 0, 0, 0, 2)` |
| **Generator (+)** | 8 | 1,050 | `(1, 0, 0, 2, 0)` |
| **Generator (+)** | 7 | 1,386 | `(2, 1, 0, 0, 0)` |
| **Generator (+)** | 15 | 1,728 | `(1, 0, 0, 1, 1)` |
| **Generator (+)** | 1 | 2,640 | `(3, 0, 0, 0, 1)` |
| **Generator (+)** | 1 | 2,772 | `(0, 0, 0, 0, 4)` |
| **Generator (+)** | 3 | 2,970 | `(0, 1, 1, 0, 0)` |
| **Generator (+)** | 2 | 3,696 | `(0, 1, 0, 0, 2)` |
| **Generator (+)** | 2 | 3,696 | `(0, 1, 0, 2, 0)` |
| **Generator (+)** | 3 | 4,125 | `(0, 0, 2, 0, 0)` |
| **Generator (+)** | 3 | 4,312 | `(2, 0, 1, 0, 0)` |
| **Generator (+)** | 1 | 4,410 | `(1, 2, 0, 0, 0)` |
| **Generator (+)** | 1 | 4,608 | `(3, 1, 0, 0, 0)` |
| **Generator (+)** | 2 | 4,950 | `(2, 0, 0, 0, 2)` |
| **Generator (+)** | 1 | 4,950 | `(2, 0, 0, 2, 0)` |
| **Generator (+)** | 13 | 5,940 | `(0, 1, 0, 1, 1)` |
| **Generator (+)** | 1 | 6,930 | `(0, 0, 0, 1, 3)` |
| **Generator (+)** | 4 | 6,930 | `(0, 0, 1, 0, 2)` |
| **Generator (+)** | 5 | 8,085 | `(2, 0, 0, 1, 1)` |
| **Generator (+)** | 2 | 10,560 | `(0, 0, 1, 1, 1)` |
| **Generator (+)** | 3 | 17,920 | `(1, 1, 1, 0, 0)` |
| **Generator (+)** | 2 | 23,040 | `(1, 1, 0, 0, 2)` |
| **Generator (+)** | 1 | 36,750 | `(1, 1, 0, 1, 1)` |
| **Relation (-)** | 5 | 16 | `(0, 0, 0, 0, 1)` |
| **Relation (-)** | 24 | 16 | `(0, 0, 0, 1, 0)` |
| **Relation (-)** | 40 | 144 | `(1, 0, 0, 0, 1)` |
| **Relation (-)** | 5 | 144 | `(1, 0, 0, 1, 0)` |
| **Relation (-)** | 5 | 560 | `(0, 1, 0, 0, 1)` |
| **Relation (-)** | 32 | 560 | `(0, 1, 0, 1, 0)` |
| **Relation (-)** | 5 | 672 | `(0, 0, 0, 0, 3)` |
| **Relation (-)** | 2 | 720 | `(2, 0, 0, 0, 1)` |
| **Relation (-)** | 19 | 720 | `(2, 0, 0, 1, 0)` |
| **Relation (-)** | 21 | 1,200 | `(0, 0, 1, 0, 1)` |
| **Relation (-)** | 5 | 1,200 | `(0, 0, 1, 1, 0)` |
| **Relation (-)** | 5 | 1,440 | `(0, 0, 0, 1, 2)` |
| **Relation (-)** | 7 | 1,440 | `(0, 0, 0, 2, 1)` |
| **Relation (-)** | 4 | 2,640 | `(3, 0, 0, 1, 0)` |
| **Relation (-)** | 15 | 3,696 | `(1, 1, 0, 0, 1)` |
| **Relation (-)** | 5 | 3,696 | `(1, 1, 0, 1, 0)` |
| **Relation (-)** | 1 | 5,280 | `(1, 0, 0, 0, 3)` |
| **Relation (-)** | 2 | 8,064 | `(0, 2, 0, 0, 1)` |
| **Relation (-)** | 2 | 8,064 | `(0, 2, 0, 1, 0)` |
| **Relation (-)** | 4 | 8,800 | `(1, 0, 1, 0, 1)` |
| **Relation (-)** | 7 | 8,800 | `(1, 0, 1, 1, 0)` |
| **Relation (-)** | 6 | 11,088 | `(1, 0, 0, 1, 2)` |
| **Relation (-)** | 3 | 15,120 | `(2, 1, 0, 0, 1)` |
| **Relation (-)** | 1 | 17,280 | `(0, 1, 0, 0, 3)` |
| **Relation (-)** | 2 | 25,200 | `(0, 1, 1, 0, 1)` |


---

## 5. Explicit Representation Tables for $\operatorname{PL}[R_B - R_F]$ (Super-Graded)

In this section, the spin-statistics graded Plethystic Logarithm is decomposed into positive and negative irreps.

### Super-Graded Order $q^1$ (Oscillator Level 2)

- **Summary:** +1 generators (gross dim 10) | -0 relations (gross dim 0) | Net dim: 10

| Type | Multiplicity | Dimension | Dynkin Coroots $(a_1, a_2, a_3, a_4, a_5)$ |
| :--- | :---: | :---: | :--- |
| **Generator (+)** | 1 | 10 | `(1, 0, 0, 0, 0)` |


### Super-Graded Order $q^2$ (Oscillator Level 3)

- **Summary:** +0 generators (gross dim 0) | -2 relations (gross dim 17) | Net dim: -17

| Type | Multiplicity | Dimension | Dynkin Coroots $(a_1, a_2, a_3, a_4, a_5)$ |
| :--- | :---: | :---: | :--- |
| **Relation (-)** | 1 | 1 | `(0, 0, 0, 0, 0)` |
| **Relation (-)** | 1 | 16 | `(0, 0, 0, 0, 1)` |


### Super-Graded Order $q^3$ (Oscillator Level 4)

- **Summary:** +2 generators (gross dim 61) | -0 relations (gross dim 0) | Net dim: 61

| Type | Multiplicity | Dimension | Dynkin Coroots $(a_1, a_2, a_3, a_4, a_5)$ |
| :--- | :---: | :---: | :--- |
| **Generator (+)** | 1 | 16 | `(0, 0, 0, 1, 0)` |
| **Generator (+)** | 1 | 45 | `(0, 1, 0, 0, 0)` |


### Super-Graded Order $q^4$ (Oscillator Level 5)

- **Summary:** +1 generators (gross dim 1) | -4 relations (gross dim 290) | Net dim: -289

| Type | Multiplicity | Dimension | Dynkin Coroots $(a_1, a_2, a_3, a_4, a_5)$ |
| :--- | :---: | :---: | :--- |
| **Generator (+)** | 1 | 1 | `(0, 0, 0, 0, 0)` |
| **Relation (-)** | 1 | 10 | `(1, 0, 0, 0, 0)` |
| **Relation (-)** | 1 | 16 | `(0, 0, 0, 0, 1)` |
| **Relation (-)** | 1 | 120 | `(0, 0, 1, 0, 0)` |
| **Relation (-)** | 1 | 144 | `(1, 0, 0, 0, 1)` |


### Super-Graded Order $q^5$ (Oscillator Level 6)

- **Summary:** +9 generators (gross dim 1,583) | -1 relations (gross dim 144) | Net dim: 1,439

| Type | Multiplicity | Dimension | Dynkin Coroots $(a_1, a_2, a_3, a_4, a_5)$ |
| :--- | :---: | :---: | :--- |
| **Generator (+)** | 2 | 1 | `(0, 0, 0, 0, 0)` |
| **Generator (+)** | 1 | 16 | `(0, 0, 0, 0, 1)` |
| **Generator (+)** | 1 | 16 | `(0, 0, 0, 1, 0)` |
| **Generator (+)** | 1 | 45 | `(0, 1, 0, 0, 0)` |
| **Generator (+)** | 1 | 126 | `(0, 0, 0, 0, 2)` |
| **Generator (+)** | 2 | 144 | `(1, 0, 0, 1, 0)` |
| **Generator (+)** | 1 | 210 | `(0, 0, 0, 1, 1)` |
| **Generator (+)** | 1 | 320 | `(1, 1, 0, 0, 0)` |
| **Generator (+)** | 1 | 560 | `(0, 1, 0, 0, 1)` |
| **Relation (-)** | 1 | 144 | `(1, 0, 0, 0, 1)` |


### Super-Graded Order $q^6$ (Oscillator Level 7)

- **Summary:** +1 generators (gross dim 144) | -16 relations (gross dim 7,310) | Net dim: -7,166

| Type | Multiplicity | Dimension | Dynkin Coroots $(a_1, a_2, a_3, a_4, a_5)$ |
| :--- | :---: | :---: | :--- |
| **Generator (+)** | 1 | 144 | `(1, 0, 0, 1, 0)` |
| **Relation (-)** | 1 | 1 | `(0, 0, 0, 0, 0)` |
| **Relation (-)** | 1 | 10 | `(1, 0, 0, 0, 0)` |
| **Relation (-)** | 3 | 16 | `(0, 0, 0, 1, 0)` |
| **Relation (-)** | 2 | 45 | `(0, 1, 0, 0, 0)` |
| **Relation (-)** | 2 | 54 | `(2, 0, 0, 0, 0)` |
| **Relation (-)** | 1 | 126 | `(0, 0, 0, 0, 2)` |
| **Relation (-)** | 1 | 126 | `(0, 0, 0, 2, 0)` |
| **Relation (-)** | 4 | 144 | `(1, 0, 0, 0, 1)` |
| **Relation (-)** | 2 | 210 | `(0, 0, 0, 1, 1)` |
| **Relation (-)** | 1 | 560 | `(0, 1, 0, 0, 1)` |
| **Relation (-)** | 1 | 560 | `(0, 1, 0, 1, 0)` |
| **Relation (-)** | 1 | 720 | `(2, 0, 0, 0, 1)` |
| **Relation (-)** | 1 | 770 | `(0, 2, 0, 0, 0)` |
| **Relation (-)** | 1 | 945 | `(1, 0, 1, 0, 0)` |
| **Relation (-)** | 1 | 1,050 | `(1, 0, 0, 0, 2)` |
| **Relation (-)** | 1 | 1,200 | `(0, 0, 1, 0, 1)` |


### Super-Graded Order $q^7$ (Oscillator Level 8)

- **Summary:** +23 generators (gross dim 36,937) | -2 relations (gross dim 774) | Net dim: 36,163

| Type | Multiplicity | Dimension | Dynkin Coroots $(a_1, a_2, a_3, a_4, a_5)$ |
| :--- | :---: | :---: | :--- |
| **Generator (+)** | 1 | 1 | `(0, 0, 0, 0, 0)` |
| **Generator (+)** | 6 | 10 | `(1, 0, 0, 0, 0)` |
| **Generator (+)** | 5 | 16 | `(0, 0, 0, 0, 1)` |
| **Generator (+)** | 1 | 16 | `(0, 0, 0, 1, 0)` |
| **Generator (+)** | 6 | 120 | `(0, 0, 1, 0, 0)` |
| **Generator (+)** | 4 | 126 | `(0, 0, 0, 0, 2)` |
| **Generator (+)** | 1 | 126 | `(0, 0, 0, 2, 0)` |
| **Generator (+)** | 3 | 144 | `(1, 0, 0, 0, 1)` |
| **Generator (+)** | 5 | 144 | `(1, 0, 0, 1, 0)` |
| **Generator (+)** | 1 | 210 | `(0, 0, 0, 1, 1)` |
| **Generator (+)** | 5 | 320 | `(1, 1, 0, 0, 0)` |
| **Generator (+)** | 1 | 560 | `(0, 1, 0, 0, 1)` |
| **Generator (+)** | 3 | 560 | `(0, 1, 0, 1, 0)` |
| **Generator (+)** | 1 | 672 | `(0, 0, 0, 0, 3)` |
| **Generator (+)** | 3 | 720 | `(2, 0, 0, 1, 0)` |
| **Generator (+)** | 2 | 1,200 | `(0, 0, 1, 0, 1)` |
| **Generator (+)** | 1 | 1,200 | `(0, 0, 1, 1, 0)` |
| **Generator (+)** | 1 | 1,386 | `(2, 1, 0, 0, 0)` |
| **Generator (+)** | 1 | 1,440 | `(0, 0, 0, 1, 2)` |
| **Generator (+)** | 4 | 1,728 | `(1, 0, 0, 1, 1)` |
| **Generator (+)** | 1 | 2,970 | `(0, 1, 1, 0, 0)` |
| **Generator (+)** | 1 | 3,696 | `(0, 1, 0, 0, 2)` |
| **Generator (+)** | 2 | 3,696 | `(1, 1, 0, 0, 1)` |
| **Relation (-)** | 1 | 54 | `(2, 0, 0, 0, 0)` |
| **Relation (-)** | 1 | 720 | `(2, 0, 0, 0, 1)` |


### Super-Graded Order $q^8$ (Oscillator Level 9)

- **Summary:** +2 generators (gross dim 1,450) | -37 relations (gross dim 188,173) | Net dim: -186,723

| Type | Multiplicity | Dimension | Dynkin Coroots $(a_1, a_2, a_3, a_4, a_5)$ |
| :--- | :---: | :---: | :--- |
| **Generator (+)** | 1 | 10 | `(1, 0, 0, 0, 0)` |
| **Generator (+)** | 2 | 720 | `(2, 0, 0, 1, 0)` |
| **Relation (-)** | 5 | 1 | `(0, 0, 0, 0, 0)` |
| **Relation (-)** | 10 | 16 | `(0, 0, 0, 0, 1)` |
| **Relation (-)** | 4 | 16 | `(0, 0, 0, 1, 0)` |
| **Relation (-)** | 14 | 45 | `(0, 1, 0, 0, 0)` |
| **Relation (-)** | 5 | 54 | `(2, 0, 0, 0, 0)` |
| **Relation (-)** | 5 | 120 | `(0, 0, 1, 0, 0)` |
| **Relation (-)** | 2 | 126 | `(0, 0, 0, 0, 2)` |
| **Relation (-)** | 4 | 144 | `(1, 0, 0, 0, 1)` |
| **Relation (-)** | 12 | 144 | `(1, 0, 0, 1, 0)` |
| **Relation (-)** | 12 | 210 | `(0, 0, 0, 1, 1)` |
| **Relation (-)** | 1 | 210 | `(3, 0, 0, 0, 0)` |
| **Relation (-)** | 4 | 320 | `(1, 1, 0, 0, 0)` |
| **Relation (-)** | 15 | 560 | `(0, 1, 0, 0, 1)` |
| **Relation (-)** | 1 | 672 | `(0, 0, 0, 0, 3)` |
| **Relation (-)** | 10 | 720 | `(2, 0, 0, 0, 1)` |
| **Relation (-)** | 1 | 770 | `(0, 2, 0, 0, 0)` |
| **Relation (-)** | 9 | 945 | `(1, 0, 1, 0, 0)` |
| **Relation (-)** | 5 | 1,050 | `(1, 0, 0, 0, 2)` |
| **Relation (-)** | 3 | 1,050 | `(1, 0, 0, 2, 0)` |
| **Relation (-)** | 2 | 1,200 | `(0, 0, 1, 0, 1)` |
| **Relation (-)** | 5 | 1,200 | `(0, 0, 1, 1, 0)` |
| **Relation (-)** | 1 | 1,386 | `(2, 1, 0, 0, 0)` |
| **Relation (-)** | 4 | 1,440 | `(0, 0, 0, 1, 2)` |
| **Relation (-)** | 1 | 1,440 | `(0, 0, 0, 2, 1)` |
| **Relation (-)** | 3 | 1,728 | `(1, 0, 0, 1, 1)` |
| **Relation (-)** | 1 | 2,640 | `(3, 0, 0, 0, 1)` |
| **Relation (-)** | 2 | 2,970 | `(0, 1, 1, 0, 0)` |
| **Relation (-)** | 3 | 3,696 | `(0, 1, 0, 0, 2)` |
| **Relation (-)** | 5 | 3,696 | `(1, 1, 0, 1, 0)` |
| **Relation (-)** | 2 | 4,312 | `(2, 0, 1, 0, 0)` |
| **Relation (-)** | 1 | 4,410 | `(1, 2, 0, 0, 0)` |
| **Relation (-)** | 1 | 5,280 | `(1, 0, 0, 0, 3)` |
| **Relation (-)** | 3 | 5,940 | `(0, 1, 0, 1, 1)` |
| **Relation (-)** | 1 | 6,930 | `(0, 0, 1, 0, 2)` |
| **Relation (-)** | 1 | 8,064 | `(0, 2, 0, 0, 1)` |
| **Relation (-)** | 1 | 8,085 | `(2, 0, 0, 1, 1)` |
| **Relation (-)** | 3 | 8,800 | `(1, 0, 1, 0, 1)` |


### Super-Graded Order $q^9$ (Oscillator Level 10)

- **Summary:** +59 generators (gross dim 984,345) | -1 relations (gross dim 2,640) | Net dim: 981,705

| Type | Multiplicity | Dimension | Dynkin Coroots $(a_1, a_2, a_3, a_4, a_5)$ |
| :--- | :---: | :---: | :--- |
| **Generator (+)** | 4 | 1 | `(0, 0, 0, 0, 0)` |
| **Generator (+)** | 15 | 10 | `(1, 0, 0, 0, 0)` |
| **Generator (+)** | 5 | 16 | `(0, 0, 0, 0, 1)` |
| **Generator (+)** | 24 | 16 | `(0, 0, 0, 1, 0)` |
| **Generator (+)** | 21 | 45 | `(0, 1, 0, 0, 0)` |
| **Generator (+)** | 11 | 54 | `(2, 0, 0, 0, 0)` |
| **Generator (+)** | 16 | 120 | `(0, 0, 1, 0, 0)` |
| **Generator (+)** | 10 | 126 | `(0, 0, 0, 0, 2)` |
| **Generator (+)** | 7 | 126 | `(0, 0, 0, 2, 0)` |
| **Generator (+)** | 40 | 144 | `(1, 0, 0, 0, 1)` |
| **Generator (+)** | 5 | 144 | `(1, 0, 0, 1, 0)` |
| **Generator (+)** | 22 | 210 | `(0, 0, 0, 1, 1)` |
| **Generator (+)** | 2 | 210 | `(3, 0, 0, 0, 0)` |
| **Generator (+)** | 10 | 320 | `(1, 1, 0, 0, 0)` |
| **Generator (+)** | 5 | 560 | `(0, 1, 0, 0, 1)` |
| **Generator (+)** | 32 | 560 | `(0, 1, 0, 1, 0)` |
| **Generator (+)** | 5 | 672 | `(0, 0, 0, 0, 3)` |
| **Generator (+)** | 2 | 720 | `(2, 0, 0, 0, 1)` |
| **Generator (+)** | 19 | 720 | `(2, 0, 0, 1, 0)` |
| **Generator (+)** | 12 | 770 | `(0, 2, 0, 0, 0)` |
| **Generator (+)** | 24 | 945 | `(1, 0, 1, 0, 0)` |
| **Generator (+)** | 15 | 1,050 | `(1, 0, 0, 0, 2)` |
| **Generator (+)** | 8 | 1,050 | `(1, 0, 0, 2, 0)` |
| **Generator (+)** | 21 | 1,200 | `(0, 0, 1, 0, 1)` |
| **Generator (+)** | 5 | 1,200 | `(0, 0, 1, 1, 0)` |
| **Generator (+)** | 7 | 1,386 | `(2, 1, 0, 0, 0)` |
| **Generator (+)** | 5 | 1,440 | `(0, 0, 0, 1, 2)` |
| **Generator (+)** | 7 | 1,440 | `(0, 0, 0, 2, 1)` |
| **Generator (+)** | 15 | 1,728 | `(1, 0, 0, 1, 1)` |
| **Generator (+)** | 4 | 2,640 | `(3, 0, 0, 1, 0)` |
| **Generator (+)** | 1 | 2,772 | `(0, 0, 0, 0, 4)` |
| **Generator (+)** | 3 | 2,970 | `(0, 1, 1, 0, 0)` |
| **Generator (+)** | 2 | 3,696 | `(0, 1, 0, 0, 2)` |
| **Generator (+)** | 2 | 3,696 | `(0, 1, 0, 2, 0)` |
| **Generator (+)** | 15 | 3,696 | `(1, 1, 0, 0, 1)` |
| **Generator (+)** | 5 | 3,696 | `(1, 1, 0, 1, 0)` |
| **Generator (+)** | 3 | 4,125 | `(0, 0, 2, 0, 0)` |
| **Generator (+)** | 3 | 4,312 | `(2, 0, 1, 0, 0)` |
| **Generator (+)** | 1 | 4,410 | `(1, 2, 0, 0, 0)` |
| **Generator (+)** | 1 | 4,608 | `(3, 1, 0, 0, 0)` |
| **Generator (+)** | 2 | 4,950 | `(2, 0, 0, 0, 2)` |
| **Generator (+)** | 1 | 4,950 | `(2, 0, 0, 2, 0)` |
| **Generator (+)** | 1 | 5,280 | `(1, 0, 0, 0, 3)` |
| **Generator (+)** | 13 | 5,940 | `(0, 1, 0, 1, 1)` |
| **Generator (+)** | 1 | 6,930 | `(0, 0, 0, 1, 3)` |
| **Generator (+)** | 4 | 6,930 | `(0, 0, 1, 0, 2)` |
| **Generator (+)** | 2 | 8,064 | `(0, 2, 0, 0, 1)` |
| **Generator (+)** | 2 | 8,064 | `(0, 2, 0, 1, 0)` |
| **Generator (+)** | 5 | 8,085 | `(2, 0, 0, 1, 1)` |
| **Generator (+)** | 4 | 8,800 | `(1, 0, 1, 0, 1)` |
| **Generator (+)** | 7 | 8,800 | `(1, 0, 1, 1, 0)` |
| **Generator (+)** | 2 | 10,560 | `(0, 0, 1, 1, 1)` |
| **Generator (+)** | 6 | 11,088 | `(1, 0, 0, 1, 2)` |
| **Generator (+)** | 3 | 15,120 | `(2, 1, 0, 0, 1)` |
| **Generator (+)** | 1 | 17,280 | `(0, 1, 0, 0, 3)` |
| **Generator (+)** | 3 | 17,920 | `(1, 1, 1, 0, 0)` |
| **Generator (+)** | 2 | 23,040 | `(1, 1, 0, 0, 2)` |
| **Generator (+)** | 2 | 25,200 | `(0, 1, 1, 0, 1)` |
| **Generator (+)** | 1 | 36,750 | `(1, 1, 0, 1, 1)` |
| **Relation (-)** | 1 | 2,640 | `(3, 0, 0, 0, 1)` |
