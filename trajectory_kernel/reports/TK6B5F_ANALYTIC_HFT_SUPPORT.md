# TK6B.5f — Analytic HFT Support by Green--Schwarz Telescoping

**Status:** the all-degree filtered-support theorem for the HFT virtual
remainder is proved, using analytic tail estimates and a finite exact
low-mode certificate

**Provenance:** baseline-free; no protected $SO(10)$ completion is imported

**Last updated:** 30 September 2026

## Result

Let

$$
F(q)=\sum_{d\geq0}F_dq^d
$$

be the virtual $B_4=\operatorname{Spin}(9)$ remainder obtained after removing
the level-one symmetric-vector tower from the HFT massive-primary series.
For a dominant $B_4$ label $\mu=(\ell,m,r,s)$, let $K_7(\mu)$ be the maximum
of the seven affine forms

$$
2\ell+3m+6r+5s-7,
$$

$$
2\ell+3m+6r+4s-3,
$$

$$
2\ell+3m+6r+3s-2,
$$

$$
2\ell+3m+2s,
$$

$$
2\ell+5m+6r+3s-4,
$$

$$
2\ell+5m+7r+4s-5,
$$

$$
2\ell+5m+9r+5s-9.
$$

Then

$$
[V_\mu]F_d\neq0\quad\Longrightarrow\quad d\geq K_7(\mu)
$$

at every degree. Since $K_7$ agrees with, or strengthens on the wall
$\ell=0$, the Pieri hazard $K$ proved in TK6B.5e, this proves the required
support implication

$$
[V_\mu]F_d\neq0\quad\Longrightarrow\quad d\geq K(\mu).
$$

Consequently the contribution-wise stable-range premise left open in
TK6B.5d is now closed at all orders. This is an all-degree statement about
the HFT oscillator series, not an extrapolation from levels 1--13.

It is not by itself a proof of the full Bars III.B existence claim. The
separate recursive weighted-circuit or integral-packetization step remains.

## 1. Exact $D_4$ oscillator identity

Work first on the common maximal torus of
$D_4=\operatorname{Spin}(8)$ and $B_4=\operatorname{Spin}(9)$. Write $V$ for
$8_v$, $S$ for the oscillator half-spinor and $C$ for the other half-spinor.
Set

$$
D(u)=\sum_{j=0}^8(-u)^j\Lambda^jV,
$$

$$
E(u)=\sum_{j=0}^8u^j\Lambda^jS,
$$

$$
H=V+S.
$$

Triality and the finite exterior-power tables give the exact divisibility
identity

$$
E(u)-D(u)=uH B(u),
$$

where

$$
B(u)=1+(C-1)u^2+(V-S)u^3+(C-1)u^4+u^6.
$$

This identity is checked coefficient by coefficient in the $D_4$ character
ring. It is also the finite algebraic form of the generalized Jacobi identity
used to pass between the RNS and Green--Schwarz oscillator products. See
[Bourget--Troost](https://arxiv.org/abs/1512.03649), especially equations
(3.31)--(3.35). The original covariant spectrum and massive-multiplet
division are from
[Hanany--Forcella--Troost](https://arxiv.org/abs/1007.2622).

## 2. Telescoping the ground-multiplet division

Put

$$
A(u)=\frac{E(u)}{D(u)}.
$$

The one-mode identity gives

$$
A(u)-1=\frac{uH B(u)}{D(u)}.
$$

Telescoping the first oscillator mode at which the product differs from one
therefore yields

$$
\frac{\prod_{m\geq1}A(q^m)-1}{qH}
=\sum_{n\geq1}q^{n-1}B(q^n)
\frac{\prod_{m=1}^{n-1}E(q^m)}
{\prod_{m=1}^{n}D(q^m)}.
$$

Removing the level-one $B_4$ vector tower contributes
$(1-q)D(q)$. Hence the exact remainder is

$$
F(q)=(1-q)\sum_{n\geq1}q^{n-1}B(q^n)
\frac{\prod_{m=1}^{n-1}E(q^m)}
{\prod_{m=2}^{n}D(q^m)}.
$$

This formula performs the universal-multiplet division before any support
estimate. It preserves cancellations which are lost in a termwise Koszul
bound. Weight-for-weight comparison with the independently derived $B_4$
remainder passes through degree 5 in the standard run.

## 3. The $D_4$-to-$B_4$ Weyl numerator

The Weyl denominators satisfy

$$
\frac{A_{\rho_{B_4}}}{A_{\rho_{D_4}}}
=\prod_{i=1}^4\left(e^{e_i/2}-e^{-e_i/2}\right).
$$

Thus a $D_4$ irrep can be sent to the dominant part of the $B_4$ Weyl
numerator using a finite $192\times16$ signed alternant calculation,
independently of the size of its highest weight.

Let a dominant $D_4$ highest weight have orthogonal coordinates

$$
(a,b,c,d),\qquad a\geq b\geq c\geq|d|,
$$

and fold its chirality to

$$
\widehat\lambda=(a,b,c,|d|).
$$

Every dominant $B_4$ term $\nu=(x_1,x_2,x_3,x_4)$ in the Weyl numerator
obeys

$$
x_i\leq\widehat\lambda_i\qquad(1\leq i\leq4).
$$

To see this, order the absolute coordinates of
$w(\lambda+\rho_{D_4})+\varepsilon/2$. Its $i$th order statistic is no larger
than $\widehat\lambda_i+(\rho_{B_4})_i$. Subtracting $\rho_{B_4}$ gives the
displayed componentwise bound.

Six of the seven walls defining $K_7$ have nonnegative coefficients in
orthogonal coordinates, so the bound is immediate for them. The exceptional
wall is

$$
2x_1+x_2-3x_3+4x_4.
$$

If $c=|d|$, this wall itself is monotone under the componentwise bound. If
$c>|d|$, the lattice gap is at least one and

$$
2x_1+x_2-3x_3+4x_4
\leq2a+b+|d|
\leq2a+b+3c-2,
$$

which is the third wall evaluated on $\widehat\lambda$. Therefore

$$
K_7(\nu)\leq K_7(\widehat\lambda).
$$

This is the step which makes the chirality fold harmless for the support
theorem. It does not choose a chirality for an $SO(10)$ lift.

## 4. Closing the infinite oscillator tail

Inspection of the seven affine forms in orthogonal coordinates proves two
uniform Lipschitz bounds:

- tensoring by one $D_4$ vector can raise the folded $K_7$ degree by at most
  4;
- tensoring by one $D_4$ spinor can raise it by at most 5.

It follows that:

- every bosonic vector mode $m\geq4$ preserves degree at least $K_7$;
- every fermionic spinor mode $m\geq5$ preserves degree at least $K_7$;
- every factor $B(q^n)$ with $n\geq3$ preserves degree at least $K_7$.

For the last assertion, the nontrivial coefficients of $B$ occur at powers
$2,3,4$, while the possible spinor and vector increases are at most 5 and 4.
The degree charges are already at least $6,9,12$ when $n\geq3$.

Thus an infinite product has been reduced to fermion modes 1--4, vector modes
2 and 3, and finitely many pivot classes.

## 5. Closed low-vector hazard bounds

For a folded $D_4$ source label $\alpha$, define the mode-two closure by

$$
H_2(\alpha)=
\max_{k,\,V_\beta\subset V_\alpha\otimes H_k}
\bigl(K_7(\widehat\beta)-2k\bigr).
$$

Every actual harmonic constituent lies in the orthogonal horizontal-strip
Pieri polytope. Maximizing each affine wall on this polytope therefore gives
the following certified upper bounds. Each row records the input wall and its
mode-two upper closure.

| input wall | mode-two closure |
|---|---|
| $(2,3,6,5)-7$ | $(2,3,8,5)-7$ |
| $(2,3,6,4)-3$ | $(2,4,6,4)-3$ |
| $(2,3,6,3)-2$ | $(2,4,6,3)-2$ |
| $(2,3,0,2)$ | $(2,3,0,2)$ |
| $(2,5,6,3)-4$ | $(3,5,6,3)-4$ |
| $(2,5,7,4)-5$ | $(3,5,7,4)-5$ |
| $(2,5,9,5)-9$ | $(3,7,9,5)-9$ |

Here $(p_1,p_2,p_3,p_4)-c$ denotes
$p_1\ell+p_2m+p_3r+p_4s-c$. The calculation is finite because the objective
is linear in the source strip, intermediate partition and target strip. Each
coordinate is therefore placed at an interlacing endpoint according to the
sign of its coefficient. Removing the common half-spin shift gives the same
endpoint calculation in the spinorial coset.

Applying the same endpoint calculation to vector mode three leaves these
seven upper pieces and adds only

$$
(4,7,9,5)-9.
$$

Consequently the exact joint hazard obeys

$$
H_{23}(\alpha)\leq\max\bigl(
H_2(\alpha),
4\ell+7m+9r+5s-9
\bigr).
$$

These bounds remove the formerly expensive nested search over arbitrarily
large harmonic degrees. Direct $D_4$ character products independently attain
the bounds on the regression simplex and on the exceptional sources used in
the finite core. Equality is useful diagnostically, but only the proved upper
bounds enter the support theorem.

## 6. The finite low-mode certificate

The $n$th telescoping summand has base degree $n-1$. After the tail estimates,
the cases are:

- pivot 1: $(1-q)B(q)$;
- pivot 2: $qB(q^2)E(q)/D(q^2)$;
- pivot 3: base degree 2, fermion modes 1--2, vector modes 2--3;
- pivot 4: base degree 3, fermion modes 1--3, vector modes 2--3;
- every pivot $n\geq5$: the worst base degree 4, fermion modes 1--4, vector
  modes 2--3.

For each finite fermion product, only the first degree at which a $D_4$ irrep
occurs need be retained. Later copies have more degree and the same hazard.
The exact certificate is:

| pivot class | finite records | minimum margin $d-H$ | failures |
|---:|---:|---:|---:|
| 1 | 8 | 0 | 0 |
| 2 | 140 | 0 | 0 |
| 3 | 20 | 0 | 0 |
| 4 | 50 | 0 | 0 |
| $n\geq5$ | 105 | 1 | 0 |
| **total** | **323** | **0** | **0** |

All character decompositions and coefficients are exact. Negative
coefficients in the virtual polynomial $B$ are retained; no positivity
assumption or ground-truth lookup enters the certificate. The factor $(1-q)$
only produces a second copy one degree later and therefore cannot worsen a
support bound.

This finite certificate, together with the analytic tail closure, proves the
support theorem at every oscillator degree.

## 7. Independent diagnostics and the failed shortcut

The full standard run reports:

- 0 failures in the finite triality identity;
- exact telescoping reconstruction in degrees 0--5;
- 0 support failures in 33 separate telescoping terms;
- 0 failures in 30 finite Dirac-fold regression terms;
- 0 failures in 15 direct low-vector hazard comparisons;
- 0 failures in the 323-record finite core;
- 0 observed support failures in 176 HFT remainder irreps through physical
  level 13.

The generic principal-embedding/Koszul shortcut has 165 obstructions in the
same run. This is expected: for example, an unsafe virtual term can be
cancelled by another Koszul term. The shortcut is therefore not used in the
proof. Principal-embedding formulas remain useful independent diagnostics;
see [Basile--Markou](https://arxiv.org/abs/2405.18467), equations (4.40) and
(4.44).

## 8. Consequence and remaining work

Combining TK6B.5e with the theorem above proves that every HFT remainder
contribution lies in the stable Pieri range needed for the transported
$\ell$-shift, including tensorial and spinorial contributions and signed
virtual coefficients.

The next all-orders obstacle is no longer higher oscillator levels. It is the
global positive-lift problem: organize the moving weighted circuits into a
recursive boundary-tail theorem, or construct integral interlacing packets
directly. Saturation/integrality also remains logically separate from the
rational circuit inequalities.

## Reproduction

```text
./bin/sage-run -m trajectory_kernel.hft_analytic_support \
  --max-level 13 \
  --maximum-label-sum 2 \
  --telescoping-degree 5 \
  --core-pivot 3 --core-pivot 4 --core-pivot 5 --progress
```

The reported complete finite certificate is independent of the chosen HFT
diagnostic level. Increasing `--max-level` extends only the comparison with
explicit HFT coefficients, not the proof domain.
