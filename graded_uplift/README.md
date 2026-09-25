# Oscillator-Graded Uplift Programme

This directory tests whether the oscillator-count grading used in
hep-th/0310292 can constrain the $SO(9)\to SO(10)$ lift relevant to the Bars
massive-mode problem.

The physical interpretation in that paper belongs to type-IIB string theory
on $AdS_5\times S^5$. It is not assumed to apply to the type-IIA/eleven-
dimensional Bars proposal. Only the representation-theoretic refinement

$$
\nu=\Delta-J
$$

is tested here.

## Provenance boundary

- `refined_spectrum.py` derives the $(\ell,\nu)$-graded $SO(8)$ chiral
  primaries directly from the oscillator Fock space.
- `refined_branching.py` implements exact
  $SO(10)\to SO(8)\times SO(2)_J$ branching.
- `paper_levels.py` is a clearly marked transcription of external Appendix B
  data; it is candidate input for verification, not a derivation.
- `verify_paper_grading.py` checks the literature candidate against the
  independently derived graded spectrum and the baseline-free HFT $SO(9)$
  quotient.
- `verify_against_baseline.py` is the only module here permitted to import the
  protected Bars completion during GU1.
- `graded_kernel.py` constructs the baseline-free finite GU2 domains and exact
  graded linear systems.
- `verify_bars_compatibility.py` and `scan_delta_bound.py` are protected GU2
  comparison layers; they use Bars only as an ungraded target.
- `iia_closed_refinement.py` implements the baseline-free GU3 opposite-
  chirality, axial-grading and $\ell'$-resolved closed construction.
- `verify_iia_closed_against_baseline.py` is the protected GU3 comparison.
- `direct_closed_low_levels.py` performs the baseline-free GU4 exhaustive
  direct closed lift through level 3, including outer invariance, the intrinsic
  closed universal factor, and interlacing-depth reconstruction of $\ell'$.
- `interlacing_depth_audit.py` performs the baseline-free GU5 positive-fibre
  audit of the proposed identification
  $\ell'=\lambda_1-\mu_1$ through level 6.
- `direct_closed_level6.py` gives a baseline-free pair of distinct positive
  outer-invariant closed level-6 lifts.
- `verify_level6_depth_candidates.py` is the protected GU5 Bars/paper
  comparison layer.

No module in this directory is allowed to feed protected data back into a
derivation or repair a failed graded lift.

## Reproduction

```text
./bin/sage-run -m graded_uplift.verify_paper_grading --self-test
./bin/sage-run -m graded_uplift.verify_paper_grading --max-level 7 --verbose
./bin/sage-run -m graded_uplift.verify_against_baseline --max-level 7 --verbose
./bin/sage-run -m graded_uplift.verify_bars_compatibility --max-level 7
./bin/sage-run -m graded_uplift.scan_delta_bound --level 6 --max-slack 3 --exact-rank
./bin/sage-run -m graded_uplift.iia_closed_refinement --max-level 7
./bin/sage-run -m graded_uplift.verify_iia_closed_against_baseline --max-level 7 --verbose
./bin/sage-run -m graded_uplift.direct_closed_low_levels --self-test
./bin/sage-run -m graded_uplift.direct_closed_low_levels --max-level 3 --verbose
./bin/sage-run -m graded_uplift.interlacing_depth_audit --max-level 6 --verbose
./bin/sage-run -m graded_uplift.direct_closed_level6 --verbose
./bin/sage-run -m graded_uplift.verify_level6_depth_candidates --max-level 6 --verbose
```
