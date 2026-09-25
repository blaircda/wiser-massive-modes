# GU2 — Graded Compatibility of the Bars Representative

**Status:** complete through level 7 under the stated finite domains  
**Last updated:** 24 September 2026

## 1. Question

GU1 showed that the oscillator-count grading of hep-th/0310292 reconstructs
the paper's $SO(10)$ candidate exactly, but that its positive cumulative lift
differs from the protected Bars lift beginning at level 6. GU2 asks whether
this difference merely reflects the paper's asymmetric choice of outer
chirality, or whether the refined equation

$$
\nu=\Delta-J
$$

actually excludes the Bars representative in a larger, explicitly finite
graded domain.

The protected completion is used only to specify the comparison target

$$
b_\ell^{\mathrm{Bars}}=R_\ell-R_{\ell-1}.
$$

It is not imported by the refined-spectrum derivation, branching code or
candidate-domain construction.

## 2. Exact finite problem

For a $D_5$ label $\lambda=[a_1,a_2,a_3,a_4,a_5]$, define the paper bound

$$
2\Delta_{\min}(\lambda)
=2+2a_1+4a_2+6a_3+5a_4+3a_5.
$$

At string level $\ell$, the primary `paper-bound` domain contains every
tagged term $(\lambda,\Delta)$ satisfying

$$
\Delta_{\min}(\lambda)\leq\Delta\leq\ell+1
$$

with the appropriate integral step in $2\Delta$. The extra unit in the upper
bound is required by the predecessor of a starred Appendix-B term.

The `outer-closed` domain additionally includes

$$
[a_1,a_2,a_3,a_4,a_5]_\Delta
\longleftrightarrow
[a_1,a_2,a_3,a_5,a_4]_\Delta
$$

at the same value of $\Delta$. This is the smallest tested enlargement that
removes the paper bound's outer-chirality asymmetry.

For integer coefficients $x_{\lambda,\Delta}$, the solver imposes both

$$
\sum_{\lambda,\Delta}x_{\lambda,\Delta}
\Phi_{\lambda,\Delta}(\nu)=T_\ell(\nu)
$$

and

$$
\sum_{\lambda,\Delta}x_{\lambda,\Delta}[\lambda]
=b_\ell.
$$

Here $T_\ell(\nu)$ is derived directly from the oscillator Fock space and
$\Phi_{\lambda,\Delta}$ is the exact
$SO(10)\downarrow SO(8)\times SO(2)_J$ image placed at
$\nu=\Delta-J$. The first equation retains the complete oscillator-count
grading; the second fixes either the paper's or Bars' ungraded single-level
$SO(10)$ character.

## 3. Controls and finite-domain result

The transcribed Appendix-B target is feasible at every level 1--7. This is a
control that the candidate enumeration includes the starred predecessors and
that the combined constraints have the intended convention.

| Level | Paper target, paper-bound | Bars target, paper-bound | Bars target, outer-closed | Candidate terms, paper/outer |
| ---: | ---: | ---: | ---: | ---: |
| 1 | yes | yes | yes | 3 / 3 |
| 2 | yes | yes | yes | 8 / 9 |
| 3 | yes | yes | yes | 19 / 22 |
| 4 | yes | yes | yes | 39 / 46 |
| 5 | yes | yes | yes | 74 / 88 |
| 6 | yes | no | no | 132 / 159 |
| 7 | yes | no | no | 222 / 269 |

The agreement through level 5 is expected because the paper and protected
Bars cumulative lifts agree there. At level 6, allowing both outer chiralities
at every candidate tag does **not** make the Bars representative compatible
with the refined spectrum. The same failure occurs at level 7.

Thus the first mismatch cannot be repaired merely by replacing an
$a_4$-parent with its $a_5$ outer conjugate while retaining the same grading
law and finite bound.

## 4. Exact rational certificates

The failures above were independently checked by exact rank computations over
$\mathbb Q$. This is stronger than failure of an integer optimizer: a target
outside the rational column span cannot have an integral solution.

| Level | Domain | Matrix size | Rank | Augmented rank |
| ---: | --- | ---: | ---: | ---: |
| 6 | outer-closed, $\Delta_{\max}=7$ | $360\times159$ | 159 | 160 |
| 7 | outer-closed, $\Delta_{\max}=8$ | $599\times269$ | 269 | 270 |

The coefficient matrices have full column rank. Since the paper target is
feasible in each same domain, its tagged solution is unique over $\mathbb Q$
there. The Bars target is not a second refinement of the same graded data.

This is uniqueness only inside the stated finite candidate domains, not a
claim that Appendix B is the unique answer in every conceivable graded ring.

## 5. Enlarged cutoff at level 6

To test whether $\Delta\leq\ell+1$ artificially caused the obstruction, the
outer-closed domain was enlarged in nested steps. Raising the cutoff also
admits every new label whose paper bound has entered the window.

| $\Delta_{\max}$ | Matrix size | Rank | Augmented rank | Bars feasible over $\mathbb Q$? |
| ---: | ---: | ---: | ---: | ---: |
| 7 | $360\times159$ | 159 | 160 | no |
| 8 | $599\times269$ | 269 | 270 | no |
| 9 | $954\times436$ | 436 | 437 | no |
| 10 | $1462\times681$ | 681 | 682 | no |

The obstruction therefore survives through $\Delta_{\max}=10$. The persistent
one-rank mismatch and full column rank suggest a triangular structure worth
understanding analytically, but the finite calculation alone does not prove
that the mismatch persists for unbounded $\Delta$.

## 6. Interpretation

The oscillator-count grading resolves information that ordinary
$SO(10)\downarrow SO(9)$ restriction loses. Outer-chirality differences lie
in the ungraded restriction kernel, but the charged
$SO(8)\times SO(2)_J$ branching distinguishes them once
$\nu=\Delta-J$ is imposed.

This is a substantive representation-theoretic result, but it selects the
IIB/AdS paper candidate rather than the protected Bars candidate at the first
two levels where they differ. It therefore does not supply the missing Bars
selection principle. If the Bars proposal is to retain an oscillator grading,
some additional structure or a different refinement—possibly one intrinsic
to the closed IIA/eleven-dimensional problem—must alter this conclusion.

## 7. Reproduction

```text
./bin/sage-run -m graded_uplift.verify_bars_compatibility --self-test
./bin/sage-run -m graded_uplift.verify_bars_compatibility --max-level 7
./bin/sage-run -m graded_uplift.scan_delta_bound --level 6 --max-slack 3 --exact-rank
./bin/sage-run -m graded_uplift.scan_delta_bound --level 7 --max-slack 0 --exact-rank
```

`verify_bars_compatibility.py` and `scan_delta_bound.py` are explicitly
protected comparison layers. `graded_kernel.py` contains the baseline-free
domain construction, branching matrix and exact solver.
