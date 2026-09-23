# Plethystic Identities: Current Status

**Date:** 23 September 2026  
**Status:** Formal identities separated from baseline-dependent data analysis  
**Supersedes:** `PL_Report_1.md`, `PL_Report_2.md`, `PL_Report_3.md`, and the
plethystic interpretation in `Direction1_SO10_Plethystic_Report.md`.

## Established formal identity

Use the convention

$$
r(q)=\sum_{n\geq1}r_nq^{n-1},
$$

and

$$
R(q)=\sum_{n\geq1}R_nq^{n-1},
\qquad
R_n=\sum_{i=1}^n r_i.
$$

Then

$$
R(q)=\frac{r(q)}{1-q}.
$$

Because

$$
\frac{1}{1-q}=\operatorname{PE}[\mathbf 1 q],
$$

the plethystic logarithm satisfies the exact formal identity

$$
\operatorname{PL}[R(q)]
=
\operatorname{PL}[r(q)]+\mathbf 1 q.
$$

This holds in any suitable completed representation ring. It is not peculiar to
the known level-1--10 spectrum and does not depend on an $SO(10)$ lift.

`verify_plethystic_identity_so9.py` verifies the identity through level 10 using
the independently derived HFT $SO(9)$ characters. It imports no protected
baseline file. The reusable logarithm, Möbius inversion, Adams-operation and
plethystic-exponential recurrences now live in the baseline-free module
`plethystic_series.py`.

## What the identity does and does not show

The identity shows exactly what the cumulative factor contributes in
plethystic coordinates: one degree-one singlet. It does **not** show that the
coefficients of $R(q)$ lift positively to $SO(10)$.

Likewise, the round trip

$$
\operatorname{PE}[\operatorname{PL}[F(q)]]=F(q)
$$

checks the implementation of mutually inverse formal operations. It does not,
by itself, identify a new algebraic variety or physical constraint.

For a general character-valued series, positive and negative irreducible
coefficients in its ordinary bosonic plethystic logarithm are signed formal
data. Calling every positive term a generator and every negative term a
relation or syzygy requires additional evidence that the series is a Hilbert
series of an appropriate graded algebra. No such algebra has been established
for the Bars spectrum.

## Withdrawn interpretations

The following earlier interpretations are withdrawn:

- The coefficient $-\mathbf{126}$ is not established as a pure-spinor
  relation. In the standard ten-dimensional pure-spinor constraint, the
  constrained bilinear transforms as the vector $\mathbf{10}$, not the
  $\mathbf{126}$.
- The negative singlet at order $q^2$ is not established by the plethystic
  computation alone as an on-shell scalar relation.
- Adding $\mathbf 1q$ to the plethystic logarithm does not explain or guarantee
  the observed positive $SO(10)$ cumulative multiplets.
- The higher signed coefficients should not be described as a proven tower of
  generators and syzygies.

These withdrawals concern interpretation, not the computed coefficients or the
formal identity between the two plethystic logarithms.

## Baseline-dependent computations

`massive_plethystic_SO10.py` computes the plethystic logarithm of the protected
$SO(10)$ level-1--10 data and verifies exact round-trip reconstruction. It is a
descriptive analysis of the known answer and imports `massive_SO10.py`.

`massive_compare_r_R.py` compares the protected $SO(10)$ series and its virtual
consecutive difference, and checks compatibility with restriction. It also
imports the baseline. Its tables are formal signed decompositions only.

## Bars III.C

The identity

$$
R^{\mathrm{III.C}}(q)
=
R^{\mathrm{III.B}}(q)
\prod_{n=2}^{\infty}\frac{1}{1-q^n}
$$

implies

$$
\operatorname{PL}[R^{\mathrm{III.C}}(q)]
-
\operatorname{PL}[R^{\mathrm{III.B}}(q)]
=
\sum_{n=2}^{\infty}\mathbf 1 q^n.
$$

This is another exact formal identity. The positivity of III.C follows from its
nonnegative convolution with III.B only conditionally on III.B positivity. The
signed plethystic difference does not independently establish a membrane,
Howe-dual, or syzygy interpretation.

## Reproduction

```text
./bin/sage-run verify_plethystic_identity_so9.py --max-level 10
./bin/sage-run massive_plethystic_SO10.py
./bin/sage-run massive_compare_r_R.py
./bin/sage-run massive_scheme_IIIC.py
```
