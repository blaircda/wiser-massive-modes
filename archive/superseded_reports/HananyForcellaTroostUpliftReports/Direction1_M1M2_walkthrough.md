# Walkthrough: Milestones M1 & M2 Completed

> **Archived (23 September 2026):** Historical implementation notes. The
> maintained baseline-free derivation is `hft_so9.py`; its separate comparison
> is `verify_hft_so9_against_baseline.py`. `STATUS.md` is authoritative.

We have successfully implemented and verified the Hanany–Forcella–Troost (HFT, arXiv:1007.2622) $SO(9)$ closed-form generating function and character-division pipeline in [`hft_so9.py`](file:///home/chris/Programming/Projects/wiser-massive-modes/hft_so9.py).

Both **Milestone M1** (levels 1–5) and **Milestone M2** (levels 6–10) have passed with 100% exact character matches against the established baseline from [`massive_SO10.py`](file:///home/chris/Programming/Projects/wiser-massive-modes/massive_SO10.py).

---

## 1. What Was Done

1. **Created [`hft_so9.py`](file:///home/chris/Programming/Projects/wiser-massive-modes/hft_so9.py)**:
   - Standalone, self-contained implementation strictly adhering to the read-only constraint on all baseline files (`massive_SO10.py`, `massive_SO8_construct.py`, `massive_SO8_to_S010.py`, `massive_SO8_to_SO9.py`).
   - Implemented closed-form representations for the transverse oscillator plethystic exponentials:
     - **Exterior powers**: Explicit closed-form decomposition in $\mathcal{R}(B_4)$ of the 8 exterior powers $\Lambda_j = \bigwedge^j(\mathbf{8}_v)$ with dimensions $[1, 8, 28, 56, 70, 56, 28, 8, 1]$.
     - **Symmetric powers**: Explicit algebraic formula for $\operatorname{Sym}^k(V_9)$ in $\mathcal{R}(B_4)$ as $\sum_{j=0}^{\lfloor k/2 \rfloor} ([k-2j, 0, 0, 0] - [k-2j-1, 0, 0, 0])$.
     - **Chiral GSO sum**: Evaluates $\mathcal{Z}_{\rm Left}^9(q) = \frac{1}{2}\left[\mathcal{Z}_{\rm NS}^9(q) - \mathcal{Z}_{\rm NS, (-1)^F}^9(q) - \mathcal{Z}_{\rm R}^9(q) + \mathcal{Z}_{\rm R, (-1)^F}^9(q)\right]$.
   - Subtracted massless vacuum $\mathcal{Z}_0 = [1,0,0,0] + [0,0,0,1]$ and extracted numerator polynomial $\mathcal{N}_n = [\mathcal{Z}_{\rm Left}^9(q) - \mathcal{Z}_0]_{q^n}$.

2. **Implemented Non-Circular Highest-Weight Character Division**:
   - `divide_by_zq(P_n)` solves the exact character equation $\mathcal{N}_n = Z_Q \cdot r_n$ in $\mathcal{R}(B_4)$ using greedy peeling ordered by highest weight:
     \[
     Z_Q = [2,0,0,0] + [1,0,0,1] + [0,0,1,0].
     \]
   - The quotient $r_n$ is derived strictly from first principles without any prior knowledge or assumption of the known multiplet structure.

3. **Benchmarked and Verified**:
   - Checked that $Z_Q \cdot r_n \equiv \mathcal{N}_n$ identically in $\mathcal{R}(B_4)$ at every level.
   - Compared derived $r_n$ against the branched baseline from `massive_SO10.py`:
     \[
     r_n^{\rm baseline} = (S_n - S_{n-1}) \downarrow B_4.
     \]

---

## 2. Validation Results

Execution via `./bin/sage-run hft_so9.py` yielded:

```
================================================================================
HANANY-FORCELLA-TROOST (HFT) SO(9) CLOSED-FORM GENERATING FUNCTION
Target: Mass Levels 1 through 10
================================================================================

[1/3] Evaluating HFT chiral partition function in B4 (order q^10)...
      Closed-form numerator computed in 5.711s.

[2/3] Extracting baseline r_n from massive_SO10.py branching...
      Baseline loaded in 17.816s.

[3/3] Performing character division N_n / Z_Q and verifying...
--------------------------------------------------------------------------------
Level  Dimension   Check Z_Q*r=N   Match Baseline  Time      
--------------------------------------------------------------------------------
1      1           True            True            0.001s
2      9           True            True            0.001s
3      60          True            True            0.012s
4      329         True            True            0.026s
5      1566        True            True            0.067s
6      6684        True            True            0.130s
7      26136       True            True            0.215s
8      95049       True            True            0.378s
9      325077      True            True            0.455s
10     1054478     True            True            0.917s
--------------------------------------------------------------------------------
Total pipeline execution time: 26.462s
================================================================================

MILESTONE VERIFICATION SUMMARY:
  * Milestone M1 (Levels 1-5):  [PASSED]
  * Milestone M2 (Levels 6-10): [PASSED]
================================================================================
```

### Key Performance Highlights:
- Closed-form numerator generation for all 10 levels: **5.7 seconds**.
- Full character division for all 10 levels (from 1 state up to 1,054,478 states at level 10): **2.2 seconds**.
- Both milestones **[PASSED]** without any discrepancy.

---

## 3. Ready for Next Milestones (M3 & M4)

With M1 and M2 verified, the $SO(9)$ side is complete. The next steps are:
- **Milestone M3**: Independent $SO(10)$ numerator uplift $\mathcal{Z}_{\rm Left}^{10}(q)$ in [`hft_so10_uplift.py`](file:///home/chris/Programming/Projects/wiser-massive-modes/hft_so10_uplift.py), verifying $\operatorname{Res}_{SO(10)\to SO(9)} \mathcal{Z}_{\rm Left}^{10} = \mathcal{Z}_{\rm Left}^9$ coefficient-by-coefficient up to level 10.
- **Milestone M4**: Exact character division in $D_5$ by the $SO(10)$ supermultiplet $Z_Q^{10} = [2,0,0,0,0] + [1,0,0,1,0] + [0,0,0,0,2]$, reconstructing $R_n^{SO(10)}$ directly from the uplifted object.
