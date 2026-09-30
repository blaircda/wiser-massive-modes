# TK6B.5e — Pieri Hazard and the Filtered HFT Remainder

**Status:** this milestone reduced the contribution-wise stable-range problem
to an exact finite affine support theorem; that remaining theorem is now
proved in TK6B.5f

**Provenance:** baseline-free

**Last updated:** 30 September 2026

## Result

The four affine pieces of the GMSZ exterior cost do **not** define
multiplicative filtrations of the $B_4$ representation ring. Exact small
tensor products give a counterexample for every piece. The proposed
four-filtration proof route in TK6B.5d is therefore invalid as stated.

There is nevertheless an exact replacement adapted to the stable Pieri
theorem. For a dominant $B_4$ weight $\mu$, define the harmonic Pieri hazard

$$
H(\mu)=\max_{\substack{k,\ V_\lambda\subset V_\mu\otimes H_k\\
\lambda_1<\mu_1}}
\bigl(E(\lambda)-k\bigr).
$$

Only finitely many harmonic degrees enter this maximum. If $H_k$ occurs in
$V_\mu\otimes V_\lambda$, then $k e_1$ is a weight of that tensor product, so

$$
k\leq\mu_1+\lambda_1.
$$

For an unstable target, $\lambda_1<\mu_1$, and hence

$$
k<2\mu_1.
$$

Define

$$
K(\mu)=\max\bigl(E(\mu)-1,H(\mu)\bigr).
$$

If an HFT remainder irrep $V_\mu$ occurs in degree $d$ with

$$
d\geq K(\mu),
$$

then both outstanding obligations from TK6B.5d follow:

1. every unstable constituent of
   $V_\mu\otimes\operatorname{Sym}^{R}(V)$ obeys
   $E(\lambda)\leq d+R$;
2. the unpaired top-degree term is outside the translated GMSZ target.

Most importantly, $K$ has a closed wall-piecewise affine formula. For
$\mu=(\ell,m,r,s)$,

$$
K(0,m,r,s)=E(0,m,r,s)-1.
$$

For $\ell\geq1$,

$$
K(\ell,m,r,s)=\max\bigl(
E(\ell,m,r,s)-1,
2\ell+5m+6r+3s-4,
2\ell+5m+7r+4s-5,
2\ell+5m+9r+5s-9
\bigr).
$$

This formula holds for both tensorial and spinorial $B_4$ weights. It removed
the open-ended tensor-product search and isolated the HFT support inclusion

$$
[V_\mu]F_d\neq0\quad\Longrightarrow\quad d\geq K(\mu).
$$

This milestone verified the implication through $d=12$; TK6B.5f now proves it
for the full HFT oscillator series.

## 1. Why the four-filtration route fails

Write the four linear pieces as

$$
L_1=(2,3,6,5),
$$

$$
L_2=(2,3,6,4),
$$

$$
L_3=(2,3,6,3),
$$

$$
L_4=(2,3,0,2).
$$

For a multiplicative highest-weight filtration one would require

$$
L_i(\nu)\leq L_i(\lambda)+L_i(\mu)
$$

whenever $V_\nu$ occurs in $V_\lambda\otimes V_\mu$. Exact $B_4$ products
give the following counterexamples:

| form | product | constituent | excess |
|---|---|---|---:|
| $L_1$ | $(0,0,1,0)\otimes(0,0,1,0)$ | $(0,1,0,2)$ | 1 |
| $L_2$ | $(0,0,1,0)\otimes(0,1,0,0)$ | $(1,0,0,2)$ | 1 |
| $L_3$ | $(0,1,0,0)\otimes(0,1,0,0)$ | $(1,0,1,0)$ | 2 |
| $L_4$ | $(0,0,0,1)\otimes(0,0,1,0)$ | $(0,1,0,1)$ | 3 |

Thus nonnegative coefficients on Dynkin labels do not suffice to define a
tensor-product filtration. This corrects the claim made in the previous
TK6B.5d report.

## 2. Finite harmonic cutoff

The stable Pieri theorem fails only when $\lambda_1<\mu_1$. Because every
$B_4$ representation is self-dual, the occurrence of $V_\lambda$ in
$V_\mu\otimes H_k$ is equivalent to the occurrence of $H_k$ in
$V_\mu\otimes V_\lambda$. Every weight coordinate of $V_\mu$ has absolute
value at most $\mu_1$, and similarly for $V_\lambda$. Therefore the weight
$k e_1$ can occur only when

$$
k\leq\mu_1+\lambda_1.
$$

Since $\mu$ and $\lambda$ lie in the same integral or half-integral weight
coset, instability strengthens this to

$$
k\leq2\mu_1-1.
$$

The hazard is consequently a finite invariant of the source irrep, not a
level-cutoff statistic.

Using

$$
\operatorname{Sym}^{R}(V)
=\bigoplus_{j=0}^{\lfloor R/2\rfloor}H_{R-2j},
$$

every unstable symmetric-power constituent satisfies

$$
E(\lambda)-R\leq H(\mu).
$$

This proves the stated sufficiency of $d\geq K(\mu)$.

## 3. Closed wall formula

Write the orthogonal coordinates of $\mu$ as

$$
(a,b,c,d),\qquad a\geq b\geq c\geq d\geq0.
$$

For tensorial weights, the odd-orthogonal Pieri rule describes a constituent
$\lambda=(x,y,z,w)$ using an intermediate partition
$\xi=(u,v,t,p)$ with

$$
a\geq u\geq b\geq v\geq c\geq t\geq d\geq p\geq0,
$$

$$
x\geq u\geq y\geq v\geq z\geq t\geq w\geq p\geq0.
$$

On the ordinary branch,

$$
k=|\mu-\xi|+|\lambda-\xi|.
$$

The exceptional odd-orthogonal branch instead has
$|\mu-\xi|+|\lambda-\xi|=k-1$, which lowers
$E(\lambda)-k$ by one at fixed strips and cannot enlarge the hazard.
This is the horizontal-strip rule of Okada, Corollary 3.4.

If $\ell=0$, then $a=b$. Instability would require $x<a$, while interlacing
requires $x\geq u\geq b=a$, a contradiction. Thus there is no unstable
harmonic target on this wall.

If $\ell\geq1$, then $x\leq a-1$. Maximizing the four affine pieces of
$E(\lambda)-k$ over the interlacing polytope gives

$$
2a+3b+4c+d-9,
$$

$$
2a+3b+2c+d-5,
$$

$$
2a+3b+c-4,
$$

$$
2a+b+d-2.
$$

The first two maxima are attained at

$$
\xi=(a-1,b,c,d),\qquad\lambda=(a-1,b,b,c).
$$

The third is attained at

$$
\xi=(a-1,b,c,d),\qquad\lambda=(a-1,b,b,d),
$$

and the fourth at

$$
\xi=(a-1,b,c,d),\qquad\lambda=(a-1,b,c,c).
$$

The first three become, in Dynkin coordinates,

$$
2\ell+5m+9r+5s-9,
$$

$$
2\ell+5m+7r+4s-5,
$$

$$
2\ell+5m+6r+3s-4.
$$

The fourth becomes

$$
2\ell+3m+3r+2s-2
$$

and is dominated by the $L_3$ piece of $E(\mu)-1$ by exactly $3r+s$.
The maxima are attained by explicit interlacing vertices, so these are
equalities, not merely upper bounds.

### Spinorial extension

For a spinorial weight write

$$
\mu=\alpha+\omega_4,
$$

where $\alpha$ is an integral four-row partition. The type-$B_4$ Weyl
character formula factors as

$$
\operatorname{ch}_{B_4}(\alpha+\omega_4)
=\operatorname{ch}_{B_4}(\omega_4)
\operatorname{ch}_{C_4}(\alpha).
$$

On the common torus, the one-row harmonic characters obey

$$
\operatorname{ch}_{B_4}(H_k)
=\operatorname{ch}_{C_4}(H_k)
+\operatorname{ch}_{C_4}(H_{k-1}).
$$

Symplectic Pieri therefore gives the same interlacing rule after subtracting
the universal half-spin shift, with strip-size sum $k$ or $k-1$. The latter
again lowers the hazard. The same linear optimization proves the wall formula
on the spinorial coset. This also explains directly why chirality does not
alter the hazard bound.

## 4. Exact audits

`hft_pieri_hazard.py` performs the following baseline-free checks:

- all four proposed linear filtrations have exact counterexamples;
- no unstable constituent appears at or beyond the analytic cutoff in the
  small audit;
- the harmonic hazard controls the corresponding direct symmetric powers;
- 678 spinorial harmonic-product constituents agree with the shifted
  symplectic-Pieri formula, with no missing or spurious target;
- the closed wall formula agrees with exact tensor products for all 210
  dominant labels of total Dynkin-label sum at most six: 130 tensorial and 80
  spinorial cases, with no failure;
- all 176 nonzero HFT remainder terms through $d=12$, comprising 44 distinct
  labels, satisfy $d\geq K(\mu)$; the minimum margin is zero and 18 terms are
  tight;
- none of those 176 terms needs a stronger threshold than the earlier scalar
  inequality $d\geq E(\mu)-1$, although such strengthening is necessary for
  generic $B_4$ sources.

The exact generic obstruction is

$$
\mu=(1,0,2,1),\qquad k=3,\qquad\lambda=(0,0,0,5).
$$

Here

$$
E(\mu)-1=15,
$$

while

$$
E(\lambda)-k=16.
$$

Thus the old scalar threshold is genuinely insufficient outside the special
HFT support.

## 5. Exact oscillator numerator

The remaining HFT statement can be written without referring to successively
higher levels. Let $R(q)$ be the massive-primary series, let $F$ be the HFT
remainder used in TK6B.5d, and remove all vector modes once more by defining
$C$ through

$$
R(q)=\operatorname{PE}\!\left(\frac{q}{1-q}V\right)C(q).
$$

Let

$$
\phi(q)=\prod_{m\geq1}(1-q^m),
$$

and let $S(q)$ be the combined HFT NS/R fermion series before the transverse
bosonic factor. Exact manipulation of the HFT product gives

$$
qZ_Q C(q)
=\phi(q)S(q)-S(0)
\operatorname{PE}\!\left(-\frac{q}{1-q}V\right).
$$

For the original level-one-vector remainder,

$$
qZ_Q F(q)
=\operatorname{PE}\!\left(\frac{q^2}{1-q}V\right)
\phi(q)S(q)-S(0)\operatorname{PE}(-qV).
$$

These are formal all-order identities. `hft_filtered_core.py` reconstructs
both sides independently through level 13. There are no coefficient failures,
and direct removal of the full vector tower agrees with the earlier two-stage
factorization.

The all-vector-free core contains 103 irreducible terms through degree 12,
including 43 negative coefficients. Every term satisfies its $K$ bound; six
terms are tight. The number of core terms still grows with degree, so this is
not a finite-support proof. It is instead a concrete target for a filtered
complex or recurrence: prove coefficientwise that the explicit numerator at
degree $d+1$ lies in $Z_Q$ times the span of labels with $K(\mu)\leq d$.

## 6. Failed shortcuts

Three tempting simplifications are now ruled out.

1. **Four independent tensor filtrations.** All four fail by the exact
   counterexamples in Section 1.
2. **Uncancelled Racah--Speiser support.** It is an upper bound in the small
   audit but has 13 cancellation gaps already for total Dynkin-label sum two.
   Applied to the HFT remainder through degree 12, it falsely rejects 25
   actual terms.
3. **One-vector induction.** There are 13 exact small transitions for which
   tensoring by $V$ raises $K$ by more than two. Hence support of the core does
   not propagate through the higher vector tower by a generic local estimate.

The exact HFT convolution avoids these bad transitions through degree 12.
TK6B.5f supplies the all-orders argument by changing to the Green--Schwarz
telescoping representation before applying support estimates.

## 7. The theorem left to TK6B.5f

The analytic target left by this milestone was the filtered divisibility
statement

$$
[q^{d+1}]\left(
\operatorname{PE}\!\left(\frac{q^2}{1-q}V\right)
\phi(q)S(q)-S(0)\operatorname{PE}(-qV)
\right)
\in Z_Q\mathcal{F}_d,
$$

where $\mathcal{F}_d$ is the integral span of $B_4$ irreps with
$K(\mu)\leq d$. TK6B.5f proves it using an exact character identity and a
finite low-mode certificate. The failed multiplicative-filtration and
generator-wise routes remain invalid without additional cancellation data.

## References

- A. Hanany, D. Forcella and J. Troost, [The Covariant Perturbative String
  Spectrum](https://arxiv.org/abs/1007.2622).
- S. Okada, [Pieri Rules for Classical Groups and Equinumeration Between
  Generalized Oscillating Tableaux and Semistandard
  Tableaux](https://arxiv.org/abs/1606.02375), especially Corollary 3.4.

## Reproduction

```text
./bin/sage-run -m trajectory_kernel.hft_pieri_hazard --max-level 13 --maximum-label-sum 2 --formula-label-sum 6
./bin/sage-run -m trajectory_kernel.hft_filtered_core --max-level 13
```
