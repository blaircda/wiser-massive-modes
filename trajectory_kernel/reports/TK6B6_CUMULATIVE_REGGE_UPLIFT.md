# TK6B.6 — Cumulative Regge-Tower Uplift

**Status:** an exact target-specific `D5` construction has been isolated;
its two-seed specialization is positive through HFT level 13; the remaining
all-orders statement is one explicit coefficientwise positivity theorem

**Provenance:** baseline-free; no protected `SO(10)` completion is imported

**Last updated:** 1 October 2026

## Result

Let

$$
Z_m(q)=\sum_{N\geq0}r^9_{N+1}q^N
$$

be the HFT massive-primary series, and use its exact Regge factorization

$$
Z_m(q)=\operatorname{PE}(qV_9)F(q).
$$

The Bars III.B cumulative series is

$$
\mathcal R(q)
=\sum_{N\geq0}R^9_{N+1}q^N
=\frac{Z_m(q)}{1-q}.
$$

Since the defining representation restricts as

$$
V_{10}\downarrow B_4=\mathbf1+V_9,
$$

one has the formal all-orders identity

$$
\operatorname{Res}\operatorname{PE}(qV_{10})
=\frac{\operatorname{PE}(qV_9)}{1-q}.
$$

Consequently, if $\widetilde F(q)$ is **any** coefficientwise virtual
integral `D5` lift of $F(q)$, then

$$
X(q)=\operatorname{PE}(qV_{10})\widetilde F(q)
$$

restricts exactly to the complete Bars cumulative series.  This is already a
useful change of problem: Bars positivity can be proved by finding one
virtual core $\widetilde F$ whose convolution with the positive symmetric
`D5` vector tower is coefficientwise positive.

The fixed all-chiral triangular section $S$ is not enough by itself.  Both
natural triangular policies tested in the project produce a single negative
half-spinor at physical level 4.  In the project's chirality convention, the
all-chiral section has the virtual defect

$$
+16_+-16_-=J.
$$

Put

$$
J=16_+-16_-,
$$

and let $A_0$ be the first six-term shell character,

$$
A_0
=210-126_- -120+45-10+1
=16_-J.
$$

The corrected virtual core

$$
\widetilde F(q)
=S(F(q))-q^3J+A(q)A_0
$$

gives a positive integral cumulative `D5` series through physical level 13
for

$$
A(q)=q^9+2q^{10}+2q^{11}+3q^{12}+O(q^{13}).
$$

These coefficients were not read from a protected completion and were not
chosen by a general-purpose optimizer.  They are obtained recursively as the
smallest nonnegative multiples of $A_0$ that make the next coefficient
positive.  More strongly, they agree exactly with a closed scalar-diagonal
formula described below.

This is not yet an all-orders proof.  It replaces the two earlier global
unknowns—classification of every moving weighted circuit and saturation of
every packet semigroup—by one target-specific character-positivity theorem.
If that theorem is proved, integrality is automatic from the displayed
construction.

## 1. Why the cumulative sum is the decisive factor

For the defining orthogonal representations,

$$
\operatorname{Sym}^N(V_{10})\downarrow B_4
=\bigoplus_{j=0}^{N}\operatorname{Sym}^j(V_9).
$$

Equivalently,

$$
\sum_{N\geq0}q^N
\operatorname{Res}\operatorname{Sym}^N(V_{10})
=\frac{1}{1-q}
\sum_{j\geq0}q^j\operatorname{Sym}^j(V_9).
$$

The factor $1/(1-q)$ is precisely the cumulative factor in Bars III.B.  It
therefore does more than sum previously known `B4` characters: it completes
the `B4` symmetric-vector Regge tower into the restriction of the `D5`
symmetric-vector tower.

Writing

$$
F(q)=\sum_{d\geq0}F_dq^d,
$$

the coefficient at physical level $n=N+1$ is constructed as

$$
X_N=\sum_{d=0}^{N}
\operatorname{Sym}^{N-d}(V_{10})\,\widetilde F_d.
$$

Exact restriction gives

$$
X_N\downarrow B_4
=\sum_{i=1}^{N+1}r_i^9
=R^9_{N+1}.
$$

No finite cutoff enters this identity.

## 2. The first obstruction and its exact repair

Take $S$ to be the integral all-chiral triangular section

$$
[\ell,m,r,s]_9\longmapsto[\ell,m,r,0,s]_{10}
$$

followed by exact unipotent branching inversion.  The resulting series

$$
X^{(0)}(q)=\operatorname{PE}(qV_{10})S(F(q))
$$

has the correct restriction at every degree, but is not positive.  Its first
failure is

$$
[q^3]X^{(0)}\supset16_+ -16_-=J.
$$

Adding $-q^3J$ to the virtual core cancels these two coefficients exactly.
Because $J$ restricts to zero, this changes no `B4` target.  The corrected
series remains positive through physical level 9 without another source.

At degree 9 a scalar deficit appears.  The smallest available natural shell
which adds a scalar is $A_0$.  Its three positive and three negative terms
make the degree-local feasibility condition completely explicit.  If $Y$ is
the coefficient before adding $tA_0$, then $Y+tA_0\geq0$ is equivalent to

$$
t\geq
\max(0,-Y_{210},-Y_{45},-Y_1)
$$

and

$$
t\leq
\min(Y_{126_-},Y_{120},Y_{10}),
$$

together with nonnegativity of every coefficient outside these six irreps.
Thus each recursive step has an exact integer interval and an exact
obstruction certificate if the interval is empty.

For the all-chiral section the degree-by-degree result is:

| HFT degree $N$ | physical level | allowed seed | selected coefficient | exact feasible interval |
|---:|---:|---|---:|---:|
| 0 | 1 | $A_0$ | 0 | $[0,0]$ |
| 1 | 2 | $A_0$ | 0 | $[0,0]$ |
| 2 | 3 | $A_0$ | 0 | $[0,0]$ |
| 3 | 4 | $-J$ | 1 | $[1,1]$ |
| 4 | 5 | $A_0$ | 0 | $[0,0]$ |
| 5 | 6 | $A_0$ | 0 | $[0,0]$ |
| 6 | 7 | $A_0$ | 0 | $[0,0]$ |
| 7 | 8 | $A_0$ | 0 | $[0,0]$ |
| 8 | 9 | $A_0$ | 0 | $[0,1]$ |
| 9 | 10 | $A_0$ | 1 | $[1,1]$ |
| 10 | 11 | $A_0$ | 2 | $[2,4]$ |
| 11 | 12 | $A_0$ | 2 | $[2,3]$ |
| 12 | 13 | $A_0$ | 3 | $[3,6]$ |

Every corrected coefficient is an exact positive integral `D5` character and
branches to the independently derived cumulative HFT target.

## 3. The scalar diagonal determines $A(q)$

Let

$$
S(F_d)=\sum_\lambda c_d(\lambda)V_\lambda.
$$

The one-row section coefficient is already an explicit six-ray HFT
functional.  If $M_d(\ell,m,r,s)$ is the multiplicity in $F_d$, the general
eight-term Möbius formula reduces on this boundary to

$$
c_d([\ell,0,0,0,0])
=M_d(\ell,0,0,0)-M_d(\ell+1,0,0,0)
$$

$$
\mathrel{\phantom{c_d([\ell,0,0,0,0])=}}
-M_d(\ell-1,1,0,0)+M_d(\ell,1,0,0)
$$

$$
\mathrel{\phantom{c_d([\ell,0,0,0,0])=}}
+M_d(\ell-1,0,1,0)-M_d(\ell,0,1,0),
$$

where entries with negative labels vanish.  Equivalently, define the three
leading-label series

$$
U_d(x)=\sum_{\ell\geq0}M_d(\ell,0,0,0)x^\ell,
$$

$$
V_d(x)=\sum_{\ell\geq0}M_d(\ell,1,0,0)x^\ell,
$$

$$
W_d(x)=\sum_{\ell\geq0}M_d(\ell,0,1,0)x^\ell.
$$

Then

$$
\sum_{\ell\geq0}c_d([\ell,0,0,0,0])x^\ell
=\left(1-\frac1x\right)U_d(x)
+\frac{M_d(0,0,0,0)}{x}
+(1-x)\bigl(V_d(x)-W_d(x)\bigr).
$$

The apparent negative power cancels because
$U_d(x)-M_d(0,0,0,0)$ is divisible by $x$.  Thus the scalar diagonal is a
closed local functional of only three HFT Regge rays:

$$
C(q)=\sum_{d\geq0}q^d\Phi_q(F_d),
$$

with $\Phi$ given by the preceding formula.  The implementation evaluates
this expression directly from HFT multiplicities and verifies that it equals
the independently inverted `D5` one-row diagonal.  This is the form to which
the Green--Schwarz telescope should next be applied.

Only a one-row `D5` irrep can pair with a constituent of
$\operatorname{Sym}^k(V_{10})$ to produce the scalar.  Define the diagonal
series

$$
C(q)=\sum_{d,\ell\geq0}
c_d([\ell,0,0,0,0])q^{d+\ell}.
$$

Since

$$
\operatorname{Sym}^k(V_{10})
=\bigoplus_{j=0}^{\lfloor k/2\rfloor}
[k-2j,0,0,0,0]_{10},
$$

the scalar series of $X^{(0)}$ is exactly

$$
B(q):=[\mathbf1]X^{(0)}(q)
=\frac{C(q)}{1-q^2}.
$$

The $-q^3J$ correction contributes no scalar because its constituents are
spinorial.  On the other hand,

$$
[\mathbf1]\bigl(\operatorname{PE}(qV_{10})A_0\bigr)
=1-q+q^2-q^3+\cdots
=\frac{1}{1+q}.
$$

Indeed, among the six terms of $A_0$, only the scalar and vector are one-row
irreps.  The scalar occurs in every even symmetric power and the vector in
every odd symmetric power, with opposite signs.

Let $B_{\geq9}(q)$ denote the tail of $B(q)$ beginning at degree 9.  The
closed candidate correction is therefore

$$
A(q)=-(1+q)B_{\geq9}(q).
$$

It cancels the complete scalar tail:

$$
[\mathbf1]\left(
X^{(0)}(q)+A(q)\operatorname{PE}(qV_{10})A_0
\right)
=B(q)-B_{\geq9}(q).
$$

In coefficients,

$$
a_9=-b_9,
$$

$$
a_N=-(b_N+b_{N-1}),\qquad N\geq10.
$$

The implementation verifies that this formula gives exactly
$1,2,2,3$ through degree 12, the same numbers found by the independent
degree-local positivity recursion.  The correction series is therefore not
a fit to the full `D5` spectrum.  It is determined by one explicit local HFT
functional.

### 3.1 Prefix-sum and pre-telescope form

The exact low-degree coefficient is $b_8=0$. Since

$$
(1+q)B(q)=\frac{C(q)}{1-q},
$$

the tail truncation creates no boundary term and the formula sharpens to

$$
a_N=-\sum_{k=0}^{N}c_k,
\qquad N\geq9.
$$

Moreover, the Green--Schwarz formula has an outer finite difference
$F(q)=(1-q)G(q)$. If $\Phi_x$ is the composition of the `D4` Dirac fold with
the six-ray one-row functional, then

$$
C(q)=(1-q)\Phi_q(G(q)),
$$

so

$$
a_N=-[q^N]\Phi_q(G(q)),
\qquad N\geq9.
$$

The all-label formula for $\Phi_x$ vanishes off nine fixed transverse `D4`
rays. Away from five low-wall endpoints, each nonzero value is a monomial
times $(1-x)^2$. Thus scalar positivity has become one explicit finite-ray
sign theorem for the pre-telescope oscillator product. This theorem is not
yet proved. See `TK6B6_SCALAR_BOUNDARY_REDUCTION.md` for the complete table
and derivation.

## 4. Stable `D5` Pieri translation

There is an all-orders propagation theorem parallel to TK6B.5d.  Let
$H_k=[k,0,0,0,0]_{D_n}$ and let $V_\mu,V_\lambda$ be arbitrary tensorial or
spinorial `D_n` irreps.  In orthogonal coordinates, if

$$
\lambda_1\geq\mu_1,
$$

then

$$
[V_\lambda:V_\mu\otimes H_k]
=
[V_{\lambda+\omega_1}:V_\mu\otimes H_{k+1}].
$$

The Racah--Speiser proof is the same stabilizer argument as in type `B`.
Here

$$
\rho_{D_n}=(n-1,n-2,\ldots,1,0).
$$

Every Weyl term not fixing $e_1$ asks for a weight of $V_\mu$ with one
coordinate of absolute value at least $\lambda_1+1>\mu_1$, and hence
vanishes.  The surviving stabilizer terms are unchanged when one adds
$\omega_1$ to $\lambda$ and replaces $k$ by $k+1$.  Summing the harmonic
decomposition of symmetric powers gives the consecutive symmetric-power
identity as well.

Thus every coefficient inequality in the stable leading-coordinate region
of the proposed `D5` series propagates automatically.  The remaining work is
confined to the boundary births where the stable inequality fails.  Unlike
the earlier circuit problem, those births now belong to one fixed explicit
series rather than to every extremal ray of a growing cone.

## 5. Precise all-orders theorem still required

Set

$$
Y(q)=\operatorname{PE}(qV_{10})
\left(S(F(q))-q^3J\right).
$$

Compute $B(q)=[\mathbf1]Y(q)$; this equals the scalar series above because
the $J$ term is scalar-free.  Define

$$
A(q)=-(1+q)B_{\geq9}(q).
$$

The remaining Bars theorem would follow from the following two statements.

1. **Scalar-tail positivity.**  The coefficients of $A(q)$ are nonnegative
   integers at every degree.
2. **One-shell dominance.**  The explicit series

$$
X(q)=Y(q)+A(q)\operatorname{PE}(qV_{10})A_0
$$

has nonnegative irreducible `D5` coefficients at every degree.

The second statement can equivalently be written as the exact six-coordinate
interval condition of Section 2 at every recursive step, plus positivity of
all coordinates outside the support of $A_0$.

These are analytic coefficient statements about the known HFT oscillator
product.  They do not ask for further protected levels.  The already proved
HFT support theorem and the `D5` stable-Pieri proposition transport their
upper-chamber part.  The next proof task is to express the remaining boundary
coefficients through the Green--Schwarz telescoping formula of TK6B.5f and
reduce them to uniform tail estimates plus a finite low-mode certificate.

## 6. Integrality and chirality

The construction is integral before positivity is imposed:

- the HFT coefficients $F_d$ are integral virtual `B4` characters;
- the all-chiral triangular section is integral and cutoff-independent;
- $J$ and $A_0$ are integral restriction-kernel characters;
- the proposed coefficients of $A(q)$ are integral local functionals of the
  HFT series;
- symmetric powers of $V_{10}$ are positive integral characters.

Therefore a proof of one-shell dominance would produce a direct integral
packetization and would make a separate saturation theorem unnecessary for
the Bars targets.

The simplicity of the two-seed module depends on the section.  The alternate
``fermion-chiral-tensor-balanced`` section encounters an exact obstruction at
physical level 6: it has a negative $120$, while the chosen orientation of
$A_0$ also has a negative $120$, giving the empty interval $[0,-1]$.  This
does **not** establish a physical chirality preference.  It shows only that
the all-chiral convention is adapted to this particular analytic
factorization.  Outer conjugation gives the equivalent globally reversed
convention.

## Reproduction

```text
./bin/sage-run -m trajectory_kernel.cumulative_regge_uplift --self-test
./bin/sage-run -m trajectory_kernel.cumulative_regge_uplift --max-level 13 --policy chiral
```

The module derives the HFT targets and the virtual remainder independently,
checks the symmetric-tower restriction identity, constructs the triangular
core, applies only the displayed kernel seeds, verifies every positivity
interval exactly, and rebranches every corrected coefficient.  It imports no
protected `SO(10)` data.
