# D5 to B4 Candidate Sets, Branching Triangularity, and Multiplicity Inversion: A Rigorous Analysis

> **Correction notice (23 September 2026):** This report is superseded by
> `STATUS.md` and `FINITE_CROSS_SECTION_REPORT.md`. The level-dependent choice
> of the 126 through level 6 and the 210 from level 7 onward is not one fixed
> cross-section. An exhaustive baseline-free search now shows that none of the
> 256 level-independent irreducible-parent cross-sections relevant through
> level 10 preserves cumulative positivity at all ten levels. The triangular
> and integral inversion statements remain valid; the claimed positivity
> mechanism does not.

**Authors:** Antigravity Theoretical Physics & Representation Theory Team  
**Date:** September 2026  
**Status:** Formal Mathematical Analysis & Candidate-Set Theorem  
**Scope:** Independent proof of branching triangularity and injectivity under physical chirality restrictions, identification of the exterior algebra kernel, and rigorous critique of single-level multiplicity inversion.

---

## 1. Coordinate Systems: Dynkin Labels vs. Orthogonal Coordinates

To ensure complete mathematical clarity, we explicitly define both coordinate frames and their mutual linear bijection:

### A. Orthogonal (Ambient) Coordinates
- **For $D_5 = \mathfrak{so}(10)$:**  
  A highest weight is a 5-tuple $\lambda = (\lambda_1, \lambda_2, \lambda_3, \lambda_4, \lambda_5)$ satisfying the dominance condition:
  $$\lambda_1 \ge \lambda_2 \ge \lambda_3 \ge \lambda_4 \ge |\lambda_5|$$
  where either all $\lambda_i \in \mathbb{Z}_{\ge 0}$ (tensor representations) or all $\lambda_i \in \mathbb{Z}_{\ge 0} + \frac{1}{2}$ (spinor representations).

- **For $B_4 = \mathfrak{so}(9)$:**  
  A highest weight is a 4-tuple $\mu = (\mu_1, \mu_2, \mu_3, \mu_4)$ satisfying:
  $$\mu_1 \ge \mu_2 \ge \mu_3 \ge \mu_4 \ge 0$$
  where either all $\mu_i \in \mathbb{Z}_{\ge 0}$ or all $\mu_i \in \mathbb{Z}_{\ge 0} + \frac{1}{2}$.

### B. Dynkin Labels (Coroots)
- **For $D_5$:** $A = [A_1, A_2, A_3, A_4, A_5]$, where:
  $$A_1 = \lambda_1 - \lambda_2$$
  $$A_2 = \lambda_2 - \lambda_3$$
  $$A_3 = \lambda_3 - \lambda_4$$
  $$A_4 = \lambda_4 - \lambda_5$$
  $$A_5 = \lambda_4 + \lambda_5$$
  Inverting this system yields:
  $$\lambda_1 = A_1 + A_2 + A_3 + \frac{A_4 + A_5}{2}$$
  $$\lambda_2 = A_2 + A_3 + \frac{A_4 + A_5}{2}$$
  $$\lambda_3 = A_3 + \frac{A_4 + A_5}{2}$$
  $$\lambda_4 = \frac{A_4 + A_5}{2}$$
  $$\lambda_5 = \frac{A_5 - A_4}{2}$$

- **For $B_4$:** $[\ell, m, r, s]$, where:
  $$\ell = \mu_1 - \mu_2$$
  $$m = \mu_2 - \mu_3$$
  $$r = \mu_3 - \mu_4$$
  $$s = 2\mu_4$$
  Inverting this system yields:
  $$\mu_1 = \ell + m + r + \frac{s}{2}$$
  $$\mu_2 = m + r + \frac{s}{2}$$
  $$\mu_3 = r + \frac{s}{2}$$
  $$\mu_4 = \frac{s}{2}$$

### C. Gelfand–Tsetlin Branching Rule
In orthogonal coordinates, an irreducible representation $\Lambda = (\lambda_1, \dots, \lambda_5)$ of $D_5$ branches into $B_4$ representations $\mu = (\mu_1, \dots, \mu_4)$ with multiplicity 1 if and only if the coordinates **interlace**:
$$\lambda_1 \ge \mu_1 \ge \lambda_2 \ge \mu_2 \ge \lambda_3 \ge \mu_3 \ge \lambda_4 \ge \mu_4 \ge |\lambda_5|$$
and multiplicity 0 otherwise.

The **top component** of $\Lambda$ under branching is obtained by maximizing each $\mu_i$ within its interlacing range:
$$\mu_{\rm top}(\Lambda) = (\lambda_1, \lambda_2, \lambda_3, \lambda_4)$$
In Dynkin labels, this correspondence is:
$$\ell_{\rm top} = A_1$$
$$m_{\rm top} = A_2$$
$$r_{\rm top} = A_3$$
$$s_{\rm top} = A_4 + A_5$$
Notice that $\mu_{\rm top}(\Lambda)$ depends **only on the first four orthogonal coordinates**, and is completely invariant under the sign of $\lambda_5$ (i.e. invariant under $A_4 \leftrightarrow A_5$).

---

## 2. The Exact Candidate Set at Fixed Level $n$ and the Kernel Obstruction

### A. The Unrestricted Kernel
Because the outer automorphism of $D_5$ ($A_4 \leftrightarrow A_5$, or $\lambda_5 \leftrightarrow -\lambda_5$) leaves the $B_4$ subalgebra point-wise invariant, any linear combination of representations differing only in the sign of $\lambda_5$ branches to zero:
$$[\lambda_1, \lambda_2, \lambda_3, \lambda_4, \lambda_5]_{10} - [\lambda_1, \lambda_2, \lambda_3, \lambda_4, -\lambda_5]_{10} \in \ker(\operatorname{Res}_{D_5 \to B_4})$$
For example, the chiral spinor $\mathbf{16}_+ = [0,0,0,0,1]_{10}$ and anti-chiral spinor $\mathbf{16}_- = [0,0,0,1,0]_{10}$ have identical branching to $[0,0,0,1]_9$.

### B. The Physical Chirality Restriction
In the left-moving physical sector of Type IIA string theory:
1. **Fermions:** All fermions have positive spacetime chirality:
   $$A_4 = 0, \quad A_5 = s_{\rm top} > 0 \iff \lambda_5 = \lambda_4 = \frac{s_{\rm top}}{2} > 0$$
2. **Bosons:** All tensors satisfy:
   $$A_5 \ge A_4 \ge 0 \iff \lambda_5 = \frac{A_5 - A_4}{2} \ge 0$$

### C. The Exterior Algebra Kernel at Level $n \ge 7$
A subtle and crucial mathematical obstruction arises if one attempts to include all representations with $\lambda_5 \ge 0$.  
Consider the exterior algebra of the defining vector $\mathbf{10} = [1,0,0,0,0]_{10}$. Since $\mathbf{10} \downarrow_{SO(9)} = \mathbf{9} \oplus \mathbf{1}$, we have:
$$\wedge^k \mathbf{10} \downarrow = \wedge^k \mathbf{9} \oplus \wedge^{k-1} \mathbf{9}$$
Taking the alternating sum:
$$\sum_{k=0}^4 (-1)^k \wedge^k \mathbf{10} \downarrow_{SO(9)} = \wedge^4 \mathbf{9} = [0,0,0,2]_9$$
In $D_5$, the 4-form is $\wedge^4 \mathbf{10} = [0,0,0,1,1]_{10}$ ($\lambda_5 = 0$), while the chiral self-dual 5-form is $\mathbf{126}_+ = [0,0,0,0,2]_{10}$ ($\lambda_5 = 1$). Both branch to include $[0,0,0,2]_9$.  
Evaluating the alternating sum in $\mathcal{R}(D_5)$ gives:
$$v_{\rm null} \equiv [0,0,0,1,1]_{10} - [0,0,0,0,2]_{10} - [0,0,1,0,0]_{10} + [0,1,0,0,0]_{10} - [1,0,0,0,0]_{10} + [0,0,0,0,0]_{10}$$
Branching each term to $B_4$:
$$\operatorname{Res}(v_{\rm null}) = (\mathbf{126} + \mathbf{84}) - \mathbf{126} - (\mathbf{84} + \mathbf{36}) + (\mathbf{36} + \mathbf{9}) - (\mathbf{9} + \mathbf{1}) + \mathbf{1} \equiv \mathbf{0}$$
Thus, $v_{\rm null} \in \ker(\operatorname{Res}_{D_5 \to B_4})$.  
Because $[0,0,0,1,1]_{10}$ appears at level 7, any candidate set containing both the 4-form and the chiral 5-form possesses a non-trivial kernel.

### D. Definition of the Injective Candidate Set $\mathcal{C}_n$
To guarantee injectivity, the candidate set $\mathcal{C}_n$ must be a **cross-section** that selects a unique representative for each $B_4$ top component $\mu = (\mu_1, \mu_2, \mu_3, \mu_4)$.  
For a fixed mass level $n$, let $\mathcal{S}_n(B_4)$ be the finite set of physical $SO(9)$ representations with total oscillator energy $\sum \mu_i \le n - 1$.  
We define the candidate set $\mathcal{C}_n$ via the canonical injection $\iota: \mathcal{S}_n(B_4) \hookrightarrow \mathcal{P}^+(D_5)$:
$$\iota(\mu) = (\mu_1, \mu_2, \mu_3, \mu_4, \sigma(\mu))$$
where the fifth coordinate $\sigma(\mu)$ is fixed by the physical Type IIA selection rule:
- If $\mu_4 \in \mathbb{Z} + \frac{1}{2}$ (fermions), $\sigma(\mu) = \mu_4$ (so $A_4 = 0, A_5 = 2\mu_4$).
- If $\mu_4 \in \mathbb{Z}$ and $\mu \ne [0,0,0,2]$ (standard tensors), $\sigma(\mu) = 0$ (so $A_4 = A_5 = 0$).
- If $\mu = [0,0,0,2]$ for $n \le 6$ (chiral 5-form $\mathbf{126}_+$), $\sigma(\mu) = 1$.
- If $\mu = [0,0,0,2]$ for $n \ge 7$ (4-form $\mathbf{210}$), $\sigma(\mu) = 0$.

Because $|\mathcal{S}_n(B_4)|$ is finite, $\mathcal{C}_n$ is a strictly finite set of dominant $D_5$ weights.

---

## 3. Construction of the Branching Matrix $K$ and Proof of Triangularity and Injectivity

Let $\mathcal{C}_n = \{ \Lambda_1, \Lambda_2, \dots, \Lambda_N \}$ and $\mathcal{S}_n(B_4) = \{ \mu_1, \mu_2, \dots, \mu_N \}$, ordered such that $\mu_j = \mu_{\rm top}(\Lambda_j)$ for all $j \in \{1, \dots, N\}$.

Order both bases by decreasing dominance order on weights (or lexicographic order on orthogonal coordinates):
$$\Lambda_1 \succ \Lambda_2 \succ \dots \succ \Lambda_N, \qquad \mu_1 \succ \mu_2 \succ \dots \succ \mu_N$$

The branching matrix $K \in M_{N \times N}(\mathbb{Z})$ is defined by:
$$\Lambda_j \downarrow_{SO(9)} = \sum_{i=1}^N K_{i, j} \mu_i$$
where $K_{i, j} \in \{0, 1\}$ is given by the Gelfand–Tsetlin interlacing conditions between $\Lambda_j$ and $\mu_i$.

### Theorem (Unipotence, Triangularity, and Injectivity)
1. **Diagonal Entries:** For every $j$, the maximal component in $\Lambda_j \downarrow$ is $\mu_{\rm top}(\Lambda_j) = \mu_j$. By the Gelfand–Tsetlin theorem, this component appears with multiplicity exactly $1$:
   $$K_{j, j} = 1 \quad \text{for all } j \in \{1, \dots, N\}$$
2. **Triangularity:** For any $i < j$, the weight $\mu_i$ is strictly higher than $\mu_j = \mu_{\rm top}(\Lambda_j)$ in the dominance order ($\mu_i \succ \mu_j$). Since Gelfand–Tsetlin branching satisfies $\mu_k \preceq \mu_{\rm top}(\Lambda_j)$ for all components appearing in the branch, $\mu_i$ cannot appear in $\Lambda_j \downarrow$:
   $$K_{i, j} = 0 \quad \text{for all } i < j$$
3. **Determinant and Invertibility:** Because $K$ is lower-triangular with diagonal $1$:
   $$\det(K) = \prod_{j=1}^N K_{j, j} = 1$$
4. **Injectivity:** Because $\det(K) = 1 \ne 0$, the branching map $\operatorname{Res}: \operatorname{span}(\mathcal{C}_n) \to \operatorname{span}(\mathcal{S}_n(B_4))$ has trivial kernel ($\ker(K) = \{0\}$). It is an isomorphism over $\mathbb{Z}$, and its inverse $K^{-1} \in M_{N \times N}(\mathbb{Z})$ has strictly integer entries.

### Explicit Branching Matrices for Low Levels

#### Level 2 ($N=2$)
Basis: $\mathcal{C}_2 = \{ [1,0,0,0,0], [0,0,0,0,0] \}$, $\mathcal{S}_2 = \{ [1,0,0,0], [0,0,0,0] \}$:
$$K_2 = \begin{pmatrix} 1 & 0 \\ 1 & 1 \end{pmatrix}$$
$$K_2^{-1} = \begin{pmatrix} 1 & 0 \\ -1 & 1 \end{pmatrix}$$

#### Level 3 ($N=4$)
Basis: $\mathcal{C}_3 = \{ [2,0,0,0,0], [0,0,0,0,1], [1,0,0,0,0], [0,0,0,0,0] \}$:
$$K_3 = \begin{pmatrix}
1 & 0 & 0 & 0 \\
0 & 1 & 0 & 0 \\
1 & 0 & 1 & 0 \\
1 & 0 & 1 & 1
\end{pmatrix}$$
$$K_3^{-1} = \begin{pmatrix}
1 & 0 & 0 & 0 \\
0 & 1 & 0 & 0 \\
-1 & 0 & 1 & 0 \\
0 & 0 & -1 & 1
\end{pmatrix}$$

#### Level 4 ($N=7$)
Basis: $\mathcal{C}_4 = \{ [3,0,0,0,0], [0,1,0,0,0], [1,0,0,0,1], [2,0,0,0,0], [0,0,0,0,1], [1,0,0,0,0], [0,0,0,0,0] \}$:
$$K_4 = \begin{pmatrix}
1 & 0 & 0 & 0 & 0 & 0 & 0 \\
0 & 1 & 0 & 0 & 0 & 0 & 0 \\
0 & 0 & 1 & 0 & 0 & 0 & 0 \\
1 & 0 & 0 & 1 & 0 & 0 & 0 \\
0 & 0 & 1 & 0 & 1 & 0 & 0 \\
1 & 1 & 0 & 1 & 0 & 1 & 0 \\
1 & 0 & 0 & 1 & 0 & 1 & 1
\end{pmatrix}$$
$$K_4^{-1} = \begin{pmatrix}
1 & 0 & 0 & 0 & 0 & 0 & 0 \\
0 & 1 & 0 & 0 & 0 & 0 & 0 \\
0 & 0 & 1 & 0 & 0 & 0 & 0 \\
-1 & 0 & 0 & 1 & 0 & 0 & 0 \\
0 & 0 & -1 & 0 & 1 & 0 & 0 \\
0 & -1 & 0 & -1 & 0 & 1 & 0 \\
0 & 1 & 0 & 0 & 0 & -1 & 1
\end{pmatrix}$$

---

## 4. Derivation of the Single-Level Multiplicities and Scrutiny of the Negative-Part Formula

Let $c^{(n)} = (c_{\mu_1}^{(n)}, \dots, c_{\mu_N}^{(n)})^T$ be the physical $SO(9)$ multiplicity vector at level $n$.  
The single-level lift vector $m^{(n)} = (m_{\Lambda_1}^{(n)}, \dots, m_{\Lambda_N}^{(n)})^T$ is defined uniquely by:
$$K m^{(n)} = c^{(n)} \implies m^{(n)} = K^{-1} c^{(n)}$$

Writing out the $j$-th row of $K m^{(n)} = c^{(n)}$:
$$c_{\mu_j}^{(n)} = K_{j, j} m_{\Lambda_j}^{(n)} + \sum_{k < j} K_{j, k} m_{\Lambda_k}^{(n)} = m_{\Lambda_j}^{(n)} + \sum_{\Lambda_k \succ \Lambda_j} K_{j, k} m_{\Lambda_k}^{(n)}$$
Rearranging for $m_{\Lambda_j}^{(n)}$ yields the exact back-substitution formula:
$$m_{\Lambda_j}^{(n)} = c_{\mu_j}^{(n)} - \sum_{\Lambda_k \succ \Lambda_j} K_{j, k} m_{\Lambda_k}^{(n)}$$

Decomposing $m_{\Lambda_j}^{(n)}$ into its positive and negative integer parts:
$$m_{\Lambda_j}^{(n)} = \text{pos}_{\Lambda_j}^{(n)} - \text{neg}_{\Lambda_j}^{(n)}$$
where $\text{pos}_{\Lambda_j}^{(n)} = \max(0, m_{\Lambda_j}^{(n)})$ and $\text{neg}_{\Lambda_j}^{(n)} = \max(0, -m_{\Lambda_j}^{(n)})$.

### Critical Analysis and Withdrawal of the Claimed Equivalence

In the earlier formulation, two claims were made:
1. That $\text{neg}_{\Lambda_j}^{(n)} = \max\left( 0, \, \sum_{\Lambda_k \succ \Lambda_j} K_{j, k} m_{\Lambda_k}^{(n)} - c_{\mu_j}^{(n)} \right)$.
2. That the cumulative positivity condition $C_\mu^{(n)} \ge \sum_{\Lambda \succ \Lambda(\mu)} K_{\Lambda, \mu} M_\Lambda^{(n)}$ is logically equivalent to the single-level condition $\text{neg}_n \le R_{n-1}^{SO(10)}$.

**We rigorously evaluate and withdraw these as general equivalences:**

1. **Sign Contamination in Back-Substitution:**  
   In the sum $\sum_{\Lambda_k \succ \Lambda_j} K_{j, k} m_{\Lambda_k}^{(n)}$, the parent coefficients $m_{\Lambda_k}^{(n)}$ are **signed integers**, not necessarily positive numbers.  
   If a higher parent has $m_{\Lambda_k}^{(n)} < 0$, its descent term *increases* $m_{\Lambda_j}^{(n)}$ rather than over-subtracting from it.  
   *(For example, in $K_4^{-1}$ above, the bottom row has $(K^{-1})_{7, 2} = +1$, meaning the scalar receives a positive push from the 2-form).*  
   Therefore, the single-level negative part cannot be represented as a purely positive descent sum unless all ancestors are known to be non-negative.

2. **Withdrawal of the Unconditional Equivalence to $\text{neg}_n \le R_{n-1}$:**  
   The cumulative system is:
   $$M_{\Lambda_j}^{(n)} = C_{\mu_j}^{(n)} - \sum_{\Lambda_k \succ \Lambda_j} K_{j, k} M_{\Lambda_k}^{(n)}$$
   Because $M^{(n)} = \sum_{k=1}^n m^{(k)} = M^{(n-1)} + m^{(n)}$, we have:
   $$M_{\Lambda_j}^{(n)} = M_{\Lambda_j}^{(n-1)} + \text{pos}_{\Lambda_j}^{(n)} - \text{neg}_{\Lambda_j}^{(n)}$$
   If $\text{neg}_{\Lambda_j}^{(n)} \le M_{\Lambda_j}^{(n-1)}$ holds, then because $\text{pos}_{\Lambda_j}^{(n)} \ge 0$, it is **sufficient** to ensure $M_{\Lambda_j}^{(n)} \ge 0$.  
   However, it is **not logically equivalent** without the global inductive premise that $M^{(n-1)} \ge 0$. Furthermore, in the cumulative equation, $M_{\Lambda_k}^{(n)}$ sums contributions across all levels, whereas $\text{neg}_{\Lambda_j}^{(n)}$ is an artifact of the single-level inversion $K^{-1} c^{(n)}$.

---

## 5. Summary of Rigorous Status

| Statement | Status | Mathematical Basis |
| :--- | :--- | :--- |
| **Branching Matrix Triangularity** | **Proved** | Gelfand–Tsetlin interlacing ensures $K_{j, j} = 1$ and $K_{i, j} = 0$ for $\mu_i \succ \mu_j$. |
| **Injectivity on Cross-Section $\mathcal{C}_n$** | **Proved** | $\det(K) = 1 \implies \ker(K) = \{0\}$ on the canonical Type IIA cross-section. |
| **Unrestricted Kernel ($n \ge 7$)** | **Proved** | Alternating exterior sum $v_{\rm null} \in \ker(\operatorname{Res})$ vanishes identically in $B_4$. |
| **Local Equivalence of Lemma 1 to $\text{neg}_n \le R_{n-1}$** | **Withdrawn** | Withdrawn as an unconditional identity due to signed back-substitution; retained only as an inductive sufficiency condition under $R_{n-1} \ge 0$. |
