# Audit of the Legacy Negative-Tail Claims

**Date:** 23 September 2026  
**Status:** Numerical tables reconstructed; former proof interpretation withdrawn

## Provenance problem

Several older reports attributed their negative-tail tables to
`test_neg_analysis.py`. That file is absent, so the original execution path
cannot be audited.

The replacement `verify_legacy_negative_tail_claims.py` reconstructs the tables
directly and transparently from the protected cumulative $SO(10)$ data. It
defines

$$
r_n^{10}:=R_n^{10}-R_{n-1}^{10},
$$

and writes

$$
r_n^{10}=\operatorname{pos}_n-\operatorname{neg}_n
$$

by separating positive and negative irreducible coefficients.

## Reconstructed numerical results

| Level | $\dim R_n$ | $\dim R_{n-1}$ | $\dim\operatorname{neg}_n$ | $\dim(R_{n-1}-\operatorname{neg}_n)$ |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 1 | 0 | 0 | 0 |
| 2 | 10 | 1 | 1 | 0 |
| 3 | 70 | 10 | 10 | 0 |
| 4 | 399 | 70 | 70 | 0 |
| 5 | 1,965 | 399 | 255 | 144 |
| 6 | 8,649 | 1,965 | 781 | 1,184 |
| 7 | 34,785 | 8,649 | 2,228 | 6,421 |
| 8 | 129,834 | 34,785 | 5,234 | 29,551 |
| 9 | 454,911 | 129,834 | 11,905 | 117,929 |
| 10 | 1,509,389 | 454,911 | 22,523 | 432,388 |

The complete negative supports and multiplicities printed by the replacement
script agree with the old tables through level 10.

## Correct logical status

For the baseline-defined difference,

$$
R_n=R_{n-1}+\operatorname{pos}_n-\operatorname{neg}_n.
$$

Therefore

$$
\operatorname{neg}_n\leq R_{n-1}
$$

is equivalent to the already known nonnegativity of $R_n$ coefficient by
coefficient. Reconstructing this inequality is a consistency check on the
protected data, not an independent derivation or explanation of Bars
positivity.

The old language of a unique physical lift is also withdrawn. The finite
cross-section analysis shows that restriction has kernel ambiguity and that no
single irreducible-parent section preserves positivity through level 10.

## Claims retained and withdrawn

Retained:

- The numerical dimensions and negative supports through level 10 are exactly
  reproducible from consecutive protected-baseline differences.
- The leading symmetric-tensor branching identity and its telescoping
  cancellation are valid within a fixed chosen lift.

Withdrawn as independent evidence:

- The assertion that the negative-tail domination table proves or predicts
  positivity.
- The assertion that the table arose from a baseline-free uplift algorithm.
- The claimed asymptotic proof based on total dimensions. Total-dimensional
  domination does not imply the required pointwise irreducible multiplicity
  inequalities.
- The claimed all-orders uniqueness of the lift in a physical chirality
  sector.

## Reproduction

```text
./bin/sage-run verify_legacy_negative_tail_claims.py --max-level 10 --verbose
```
