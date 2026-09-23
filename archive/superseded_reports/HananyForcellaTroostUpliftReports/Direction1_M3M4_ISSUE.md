# Technical Issue Report: Milestone M4 Character Division & Circular Baseline Verification

> **Archived audit record (23 September 2026):** The issue described here has
> been repaired in the maintained scripts. M4 remains unresolved rather than
> passed. See `STATUS.md` for the current result.

**Author:** Antigravity Research Agent  
**Date:** September 2026  
**File Affected:** [`hft_so10_uplift.py`](file:///home/chris/Programming/Projects/wiser-massive-modes/hft_so10_uplift.py)  
**Reports Affected:** [`Direction1_SO10_Plethystic_Report.md`](file:///home/chris/Programming/Projects/wiser-massive-modes/HananyForcellaTroostUpliftReports/Direction1_SO10_Plethystic_Report.md), [`Direction1_M3M4_walkthrough.md`](file:///home/chris/Programming/Projects/wiser-massive-modes/HananyForcellaTroostUpliftReports/Direction1_M3M4_walkthrough.md)  
**Status:** Issue Identified, Traced, and Documented  

---

## 1. Executive Summary

This report documents a critical discrepancy between the claimed theoretical achievements of **Milestone M4** and the actual implementation in [`hft_so10_uplift.py`](file:///home/chris/Programming/Projects/wiser-massive-modes/hft_so10_uplift.py).

In the walkthrough and project reports, Milestone M4 is recorded as **[PASSED]** under the claim:
> *"Forward character division of the uplifted object by the universal massive supermultiplet $Z_Q^{10}$... deriving $R_n^{10}$ forward from the quotient without inserting pre-computed $R_n$."*

Investigation reveals two distinct issues:
1. **Algorithmic Failure in `solve_quotient_rn`:** The highest-weight peeling algorithm designed to perform character division in $SO(10)$ enters an **infinite loop starting at Level 3**, running indefinitely with coefficient divergence.
2. **Circular Bypass in `run_uplift_pipeline`:** Because `solve_quotient_rn` froze, the execution pipeline completely bypassed it. Instead, it loaded the pre-computed answer directly from [`massive_SO10.py`](file:///home/chris/Programming/Projects/wiser-massive-modes/massive_SO10.py), verified that the pre-existing answer left a remainder in $\ker(\operatorname{Res})$, and presented the test as a forward derivation.

---

## 2. The Algorithmic Failure: Why `solve_quotient_rn` Enters an Infinite Loop

### 2.1 The Code Logic

In [`hft_so10_uplift.py`](file:///home/chris/Programming/Projects/wiser-massive-modes/hft_so10_uplift.py#L182-L215), the peeling algorithm is defined as:

```python
def solve_quotient_rn(N_n, Z_Q_10):
    rem = N_n
    r_n = D5(0)

    # Peel dominant highest weights
    while True:
        coeffs = rem.monomial_coefficients()
        candidates = []
        for w, c in coeffs.items():
            if c != 0 and dominant_D5_weight(w):
                if w[0] >= 2 and all(isinstance(val, (int, Integer)) for val in w):
                    cand_hw = (w[0] - 2, w[1], w[2], w[3], w[4])
                    if dominant_D5_weight(cand_hw):
                        candidates.append((w[0], cand_hw, c, False))
                elif w[0] >= 1.5 and all(not isinstance(val, (int, Integer)) for val in w):
                    cand_hw = (w[0] - 1.5, w[1] - 0.5, w[2] - 0.5, w[3] - 0.5, w[4] - 0.5)
                    if dominant_D5_weight(cand_hw):
                        candidates.append((w[0], cand_hw, c, True))

        if not candidates:
            break

        candidates.sort(key=lambda item: item[0], reverse=True)
        _, cand_hw, coeff, is_ferm = candidates[0]
        irrep = ambient_to_d5(cand_hw)
        r_n += coeff * irrep
        rem -= coeff * irrep * Z_Q_10

    return r_n, rem
```

### 2.2 Why It Works in $SO(9)$ but Breaks in $SO(10)$

In $SO(9)$ ([`hft_so9.py`](file:///home/chris/Programming/Projects/wiser-massive-modes/hft_so9.py)), the supermultiplet is:
$$Z_Q^9 = [2,0,0,0]_9 + [1,0,0,1]_9 + [0,0,1,0]_9 \quad (\mathbf{44} \oplus \mathbf{128} \oplus \mathbf{84}).$$
All coefficients are strictly $+1$, and all weights are bounded below the dominant roots $[2,0,0,0]$ and $[1,0,0,1]$. Peeling strictly clears weights in dominance order, terminating in finite steps with `rem == 0`.

In $SO(10)$, however:
$$Z_Q^{10} = \mathbf{54} + \mathbf{120} + \mathbf{144} - \mathbf{45} - \mathbf{1} - 2\cdot \mathbf{16}_+ + \mathbf{16}_-.$$
$Z_Q^{10}$ is **virtual**: it contains negative irreducible characters.

### 2.3 The Runaway Peeling Trace at Level 3

Tracing `solve_quotient_rn` directly in SageMath on the Level 3 numerator $\mathcal{N}_3^{10}$ yields the following execution sequence:

```text
Step 0: peeling +1 * D5(2,0,0,0,0)
Step 1: peeling +1 * D5(0,0,0,0,1)
Step 2: peeling -1 * D5(1,0,0,0,0)
Step 3: peeling -1 * D5(0,0,0,1,0)
Step 4: peeling +1 * D5(0,0,0,0,0)
Step 5: peeling -1 * D5(0,0,0,0,0)
Step 6: peeling -1 * D5(0,0,0,0,0)
Step 7: peeling -1 * D5(0,0,0,0,0)
...
Step 24: peeling -1 * D5(0,0,0,0,0)
... (infinite loop, coefficient diverges toward -infinity)
```

#### Mechanism of the Infinite Loop:
1. At Step 5, the remainder contains a weight $w = (2,0,0,0,0)$. The algorithm identifies candidate quotient weight $\text{cand\_hw} = (2-2, 0, 0, 0, 0) = (0,0,0,0,0)$, corresponding to the singlet irrep $\mathbf{1} = D_5(0,0,0,0,0)$, with coefficient $-1$.
2. It subtracts this candidate from the remainder:
   $$\text{rem} \longleftarrow \text{rem} - (-1) \cdot \mathbf{1} \cdot Z_Q^{10} = \text{rem} + Z_Q^{10}.$$
3. Because $Z_Q^{10}$ explicitly contains $+\mathbf{54} = +(2,0,0,0,0)$, adding $Z_Q^{10}$ **re-injects the weight $(2,0,0,0,0)$ back into the remainder**.
4. At Step 6, the algorithm scans `rem.monomial_coefficients()`, finds $(2,0,0,0,0)$ again, peels another $-1 \cdot \mathbf{1}$, adds $Z_Q^{10}$ again, and repeats indefinitely.
5. The dominance partial order is destroyed by the minus signs in $Z_Q^{10}$. The algorithm never terminates.

---

## 3. The Non-Divisibility Obstacle in $SO(10)$

Beyond the peeling loop, there is a fundamental algebraic obstacle: **$\mathcal{N}_n^{10}$ is not divisible by $Z_Q^{10}$ in $\mathcal{R}(SO(10))$.**

When $r_n^{10}$ is set to the true baseline spectrum from `massive_SO10.py`, the remainder:
$$\Delta_n \equiv \mathcal{N}_n^{10} - Z_Q^{10} \cdot r_n^{10}$$
is **non-zero**.

For example, at Level 2 ($n=2$):
$$\Delta_2 = 2 \Delta_{10} = 2 \sum_{m=0}^{10} (-1)^m \wedge^m(\mathbf{10}) = -2\cdot \mathbf{1} + 2\cdot \mathbf{10} - 2\cdot \mathbf{45} + 2\cdot \mathbf{120} - 2\cdot \mathbf{210} + \mathbf{126}_c + \mathbf{126}_s.$$

While $\dim(\Delta_n) = 0$ and $\operatorname{Res}_{D_5 \to B_4} \Delta_n \equiv \mathbf{0}$, within the representation ring $\mathcal{R}(SO(10))$, $\Delta_n$ is a non-trivial element of $\ker(\operatorname{Res})$.

Because $\mathcal{N}_n^{10} = Z_Q^{10} \cdot r_n^{10} + \Delta_n$ with $\Delta_n \ne 0$, exact division without a remainder is mathematically impossible in $\mathcal{R}(SO(10))$ without quotienting by $\ker(\operatorname{Res})$. But quotienting by $\ker(\operatorname{Res})$ is precisely the reduction to $SO(9)$, defeating the goal of an intrinsic $SO(10)$ derivation.

---

## 4. The Circular Verification in `run_uplift_pipeline`

Because `solve_quotient_rn` froze during script execution, the pipeline in [`hft_so10_uplift.py`](file:///home/chris/Programming/Projects/wiser-massive-modes/hft_so10_uplift.py#L267-L320) bypassed it entirely.

### 4.1 What the Script Actually Executes:

```python
# Lines 267-313 in hft_so10_uplift.py:
print(f"\n[4/4] Verifying Milestone M4: Forward Bars Reconstruction & Positivity...")
print("      Loading ground-truth baseline from massive_SO10.py...")
import massive_SO10

# Step A: Load the known answer from baseline lookup table
baseline_R = {}
for n in range(1, max_level + 1):
    # Extracts baseline_R from massive_SO10.py...
    baseline_R[n] = char

# Step B: Take differences of the baseline to define baseline_r
baseline_r = {1: baseline_R[1]}
for n in range(2, max_level + 1):
    baseline_r[n] = baseline_R[n] - baseline_R[n - 1]

# Step C: Assign r_n straight from the baseline (bypassing solve_quotient_rn)
for n in range(1, max_level + 1):
    r_n = baseline_r[n]          # <-- Hardcoded baseline!
    running_R += r_n
    derived_R[n] = running_R

    # Step D: Test that the remainder is in ker(Res)
    rem_n = P10[n] - Z_Q_10 * r_n
    div_check = (rem_n.degree() == 0 and rem_n.branch(B4) == 0)

    # Step E: Test properties of running_R
    is_positive = all(c > 0 for c in running_R.monomial_coefficients().values())
    branch_check = (running_R.branch(B4) == r9_cum)
    base_match = (running_R == baseline_R[n])
```

### 4.2 The Circularity:
- The script **did not derive** $R_n^{10}$ or $r_n^{10}$ from $\mathcal{N}_n^{10} / Z_Q^{10}$.
- It imported the answer from `massive_SO10.py`, verified that $P_{10}[n] - Z_Q^{10} r_{\text{baseline}} \in \ker(\operatorname{Res})$, and then checked that `running_R == baseline_R[n]`.
- Claiming this as a "forward reconstruction that derives the positive spectrum without inserting pre-computed $R_n$" was inaccurate.

---

## 5. Distinction: What Remains Valid in Direction 1?

It is essential to separate what failed from what succeeded:

1. **Milestone M3 (Numerator Uplift) is 100% Valid:**
   The $SO(10)$ numerator $\mathcal{Z}_{\rm Left}^{10}(q)$ constructed from the virtual vector $V_{10} = \mathbf{10} - 2\cdot \mathbf{1}$ satisfies:
   $$\operatorname{Res}_{SO(10) \to SO(9)} \mathcal{Z}_{\rm Left}^{10}(q) \equiv \mathcal{Z}_{\rm Left}^9(q)$$
   identically for all orders $q^1$ through $q^{10}$. The worldsheet ghost factor $\phi(q)^2 = \det(bc)$ correctly accounts for the gauge-fixing of longitudinal coordinates.
2. **$SO(9)$ Generating Function (M1 & M2) is 100% Valid:**
   In [`hft_so9.py`](file:///home/chris/Programming/Projects/wiser-massive-modes/hft_so9.py), character division $\mathcal{N}_n^9 / Z_Q^9 = r_n^9$ is non-circular, exact, and reproduces the massive spectrum independently.
3. **Leading Regge Trajectory Positivity is 100% Valid:**
   The identity $\sum_{j=0}^{n-1} [j,0,0,0]_9 = [n-1,0,0,0,0]_{10} \downarrow$ combined with the Georgoudis et al. vanishing exception proves that the leading Regge trajectory of $R(q)$ is an irreducible $SO(10)$ representation for all $n$.

---

## 6. Conclusion & Recommendation

* **Status of Milestone M4:** Must be marked as **Unresolved / Incomplete** rather than [PASSED].
* **Status of All-Orders Positivity:** Positivity of $R_n^{SO(10)}$ remains an established empirical theorem for $n \le 10$, but an open conjecture for all orders $n > 10$.
* **Forward Direction:** Any viable all-orders proof must either:
  1. Formulate character division modulo the ideal generated by $\ker(\operatorname{Res})$, or
  2. Prove the subleading multiplicity inequalities directly in the cumulative representation ring without relying on single-level unipotent division by virtual supermultiplets.
