# TK6B.5d — Stable $B_4$ Pieri Translation

**Status:** stable translation theorem proved for tensorial and spinorial
$B_n$ weights; all active HFT remainder couplings certified through level 13;
the formerly open all-orders HFT stable-range premise is proved in TK6B.5f

**Provenance:** baseline-free

**Last updated:** 30 September 2026

## Result

Let $V_\mu$ and $V_\lambda$ be arbitrary irreducible representations of
$B_n$, including half-integral spinorial weights. Write their orthogonal
coordinates as

$$
\mu_1\geq\cdots\geq\mu_n\geq0,
$$

$$
\lambda_1\geq\cdots\geq\lambda_n\geq0.
$$

Let $H_k=V_{k\omega_1}$ be the harmonic one-row representation. If

$$
\lambda_1\geq\mu_1,
$$

then

$$
[V_\lambda:V_\mu\otimes H_k]
=
[V_{\lambda+\omega_1}:V_\mu\otimes H_{k+1}]
$$

for every $k\geq0$. Consequently,

$$
[V_\lambda:V_\mu\otimes\operatorname{Sym}^{R}(V)]
=
[V_{\lambda+\omega_1}:
 V_\mu\otimes\operatorname{Sym}^{R+1}(V)]
$$

for every $R\geq0$.

This is a genuine all-rank, all-order representation-theoretic statement.
It is not an empirical property of the string spectrum. In particular, the
proof does not distinguish tensorial and spinorial weight cosets. This
removes chirality as an obstruction to the leading-label Regge translation
itself.

Applied irrep by irrep to the exact HFT factorization

$$
Z_m(q)=PE([1,0,0,0]_9q)Z'_m(q),
$$

the theorem certifies all 524 active remainder couplings in the 185 eligible
adjacent $\ell$ shifts through level 13. Of these active couplings, 310 are
tensorial and 214 spinorial; 44 carry a negative coefficient in the virtual
remainder. There are no active pairs outside the stable range, no unpaired
top-degree remainder term, and no multiplicity failure in that window.

The all-orders problem left by this milestone was narrower than the earlier
"prove the GMSZ shift" formulation: every HFT remainder irrep contributing in
the exterior chamber had to satisfy the stable-range inequality, while the
new top-degree coefficient had to miss the translated target. TK6B.5f now
proves this statement. The sharper exterior-cost inequality found here passed
through total degree 12 and converted the problem exactly into exclusion from
the GMSZ chamber. A bound on all remainder irreps without regard to whether
they can couple was not sufficient, and a tempting generic Pieri-cost
shortcut has an exact counterexample.

## 1. Racah–Speiser proof

For $B_n$, put

$$
\rho=(n-\tfrac12,n-\tfrac32,\ldots,\tfrac12).
$$

The Weyl group is the group of signed permutations of the orthogonal basis
$e_1,\ldots,e_n$. Racah–Speiser gives

$$
[V_\lambda:V_\mu\otimes V_{k\omega_1}]
=
\sum_{w\in W}(-1)^w
\operatorname{mult}_{V_\mu}
\left(w(\lambda+\rho)-(k\omega_1+\rho)\right).
$$

Every weight $\nu$ of $V_\mu$ lies in the convex hull of the Weyl orbit of
$\mu$. Hence

$$
|\nu_i|\leq\mu_1
$$

for every coordinate.

Suppose $w(e_1)\neq e_1$. If $w$ sends $e_1$ to $\pm e_j$ with $j\geq2$,
the $j$th coordinate of the argument of the weight multiplicity has absolute
value at least

$$
\lambda_1+\rho_1-\rho_j
\geq\lambda_1+1
>\mu_1.
$$

If $w(e_1)=-e_1$, its first coordinate has still larger absolute value.
Thus every such Weyl term vanishes when $\lambda_1\geq\mu_1$.

Only the stabilizer of $e_1$ survives. For each $w$ in that stabilizer,

$$
w(\lambda+\omega_1+\rho)
-((k+1)\omega_1+\rho)
=
w(\lambda+\rho)-(k\omega_1+\rho).
$$

The two Racah–Speiser sums are therefore termwise identical. This proves the
harmonic one-row identity on both the integral and half-integral weight
cosets.

## 2. Passing from harmonics to symmetric powers

For the defining orthogonal representation $V$,

$$
\operatorname{Sym}^{R}(V)
=
\bigoplus_{j=0}^{\lfloor R/2\rfloor}H_{R-2j}.
$$

Every summand on the left pairs with $H_{R+1-2j}$ after translation. When
$R$ is odd, $\operatorname{Sym}^{R+1}(V)$ also contains one unpaired copy of
$H_0$. It could contribute only if

$$
\lambda+\omega_1=\mu,
$$

which would imply $\mu_1=\lambda_1+1$ and contradict the stable-range
hypothesis. The symmetric-power identity follows.

Okada's orthogonal Pieri rule gives a complementary partition proof in the
tensorial sector: the translated first-row box lies beyond every possible
intermediate partition and is therefore forced. The Racah–Speiser proof is
preferable here because it also covers spinorial $B_n$ representations.

## 3. Exact HFT reduction

Write the HFT series degree as $N$, with physical level $N+1$, and write

$$
Z'_m(q)=\sum_{d\geq0}F_dq^d.
$$

Then

$$
[q^N]Z_m
=
\sum_{d=0}^{N}
\operatorname{Sym}^{N-d}(V)\otimes F_d.
$$

Consider an adjacent shift from $V_\lambda$ at degree $N-1$ to
$V_{\lambda+\omega_1}$ at degree $N$. For every irreducible $V_\mu$ in
$F_d$ with $d\leq N-1$, the two contributions are consecutive symmetric
powers. They are equal whenever

$$
\lambda_1\geq\mu_1.
$$

This remains true if the coefficient of $V_\mu$ in $F_d$ is negative. At
$d=N$ there is no source term, so the separate boundary requirement is

$$
[V_{\lambda+\omega_1}:F_N]=0.
$$

Thus an adjacent HFT Regge shift follows from two support statements:

1. every remainder irrep that couples to either side lies in the stable
   range;
2. the unpaired coefficient $F_N$ misses the translated target.

No cancellation between distinct remainder degrees is needed.

## 4. Exterior-cost refinement

The finite data suggest a sharper formulation tied directly to the GMSZ
chamber. Define

$$
E(\ell,m,r,s)
=2\ell+3m+\operatorname{cost}(r,s),
$$

where

$$
\operatorname{cost}(r,s)
=\max(6r+5s-6,6r+4s-2,6r+3s-1,2s+1).
$$

Every one of the 176 nonzero virtual-remainder terms through degree 12 obeys

$$
E(\mu)\leq d+1.
$$

The minimum margin is zero and 18 terms saturate the inequality. This bound
is stronger and more direction-sensitive than the first-coordinate
half-slope observation.

There is also a direct contribution-wise candidate. If
$V_\lambda$ occurs in
$V_\mu\otimes\operatorname{Sym}^{R}(V)$, with $V_\mu$ in $F_d$, and the
stable-range inequality fails, the observed bound is

$$
E(\lambda)\leq d+R.
$$

Put $T=d+R$. At the next physical level $n=T+2$, the translated target has
leading label $\ell+1$ and

$$
\ell_{\max}=T+2-3m-\operatorname{cost}(r,s).
$$

The displayed energy bound implies

$$
\ell_{\max}\geq2\ell+2.
$$

Therefore $\ell+1\leq\lfloor\ell_{\max}/2\rfloor$, exactly excluding the
translated target from the eligible adjacent-shift chamber. Through total
degree 12, all 363 unstable HFT product terms obey this inequality; the
minimum margin is two.

This energy inequality is still finite evidence and is genuinely
HFT-specific. The tempting generic estimate

$$
E(\lambda)\leq E(\mu)+R-1
$$

is false for arbitrary $B_4$ sources. An exact counterexample is

$$
\mu=(1,0,2,1),\qquad R=3,\qquad\lambda=(0,0,0,5),
$$

where $V_\lambda$ occurs with multiplicity one and the coupling is unstable,
but

$$
E(\mu)=16,
$$

$$
E(\lambda)=19>18=E(\mu)+R-1.
$$

Thus a proof must use more than a generic Pieri estimate plus the scalar
bound $E(\mu)\leq d+1$; it must exploit the special support of the HFT
remainder or prove the combined contribution-wise inequality directly.

Nor does the bound descend to primitive plethystic generators. Through degree
8, the plethystic logarithm $PL[Z'_m]$ contains 85 irreducible terms, of which
10 violate $E(\mu)\leq d+1$; the worst margin is $-3$. The coefficient series
$Z'_m$ nevertheless satisfies the bound in this window. Thus a proof based on
assigning the exterior cost independently to each plethystic generator is
also obstructed: the required support restriction is restored only after
nontrivial formal cancellations.

The exterior-cost bound is equivalent to four linear highest-weight bounds.
Define

$$
L_1=2\ell+3m+6r+5s,
$$

$$
L_2=2\ell+3m+6r+4s,
$$

$$
L_3=2\ell+3m+6r+3s,
$$

$$
L_4=2\ell+3m+2s.
$$

Then $E(\mu)\leq d+1$ says respectively

$$
L_1(\mu)\leq d+7,
$$

$$
L_2(\mu)\leq d+3,
$$

$$
L_3(\mu)\leq d+2,
$$

$$
L_4(\mu)\leq d.
$$

**Correction (TK6B.5e):** nonnegative coefficients in Dynkin coordinates do
not make these forms tensor-product filtrations. Each of the four $L_i$ has an
exact small $B_4$ tensor-product counterexample. Consequently, the proposed
four-filtration route is not valid as stated.

Independently, removing the level-one symmetric-vector tower changes the HFT
bosonic factor formally by

$$
\operatorname{PE}\!\left(\frac{q}{1-q}(V-1)\right)
\operatorname{PE}(-qV)
=
\operatorname{PE}\!\left(\frac{q^2}{1-q}V-\frac{q}{1-q}\right).
$$

The exceptional vector mode has thereby been removed, and the remaining
positive vector modes begin at degree two. TK6B.5e replaces the invalid
multiplicative-filtration shortcut by a finite harmonic Pieri hazard. It
derives a closed wall-piecewise affine source bound for tensorial and
spinorial weights and rewrites the remaining HFT obligation as filtered
divisibility of an explicit oscillator numerator. See
`TK6B5E_PIERI_HAZARD.md`.

## 5. Why the half-slope observation is not yet the proof

Through level 13 every remainder term of degree $d\geq2$ obeys

$$
2\mu_1\leq d-1.
$$

This is useful evidence about the remainder support, but it does not alone
imply $\lambda_1\geq\mu_1$ for every remainder irrep: the exterior chamber
contains target labels for which the global bound still permits larger
$\mu_1$. In the exact audit, those larger remainder irreps simply do not
couple to the target.

Accordingly, the next theorem should be phrased contribution-wise. One needs
either:

- a refined polyhedral support theorem for $F_d$ strong enough to include
  the tensor-product coupling conditions; or
- a direct argument that an unstable remainder irrep cannot satisfy the
  $B_4$ tensor-product selection rules for a target in the exterior chamber.

This distinction prevents a finite-window observation from being promoted
prematurely into an all-orders claim.

## 6. Computation

The implementation performs two independent checks.

- It tests 393 exact $B_4$ character-ring instances with small tensorial and
  spinorial source labels. Every instance satisfying the theorem hypothesis
  obeys the symmetric-power translation.
- It expands every eligible adjacent HFT shift irrep by irrep and remainder
  degree by remainder degree through level 13. All 524 active pairs satisfy
  the stable-range hypothesis and match exactly.
- It audits all unstable HFT remainder--symmetric-power products through total
  degree 12 against the exterior-cost inequality, and separately verifies the
  sharper remainder-support bound and the generic-cost counterexample.
- An optional plethystic audit records the failure of the same bound on
  $PL[Z'_m]$ through degree 8.

The HFT series is derived from the oscillator formula. No protected
$SO(10)$ lift is imported.

## References

- S. Okada, [*Pieri rules for classical groups and equinumeration between
  generalized oscillating tableaux and semistandard
  tableaux*](https://arxiv.org/abs/1606.02375), especially Corollaries 3.3
  and 3.4.
- D. Forcella, A. Hanany and J. Troost,
  [*The covariant perturbative string
  spectrum*](https://arxiv.org/abs/1007.2622), especially equations
  (3.21)--(3.24).

## Reproduction

```text
./bin/sage-run -m trajectory_kernel.stable_pieri --max-level 13
./bin/sage-run -m trajectory_kernel.stable_pieri --max-level 9 --plethystic-audit
```
