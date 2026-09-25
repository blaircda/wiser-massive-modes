# TK4c — The Restriction-Kernel Anomaly Class

**Status:** completed baseline-free structural experiment through level 11;
exact quotient certificates through level 6

**Provenance:** baseline-free

**Last updated:** 23 September 2026

## Result

For a cumulative $SO(10)$ lift $L_n$, define

$$
\kappa_n=N_n^{10}-Z_Q^{10}(L_n-L_{n-1}).
$$

Every $\kappa_n$ restricts to zero in $SO(9)$. The important invariant is not
an individual representative but its class

$$
[\kappa_n]\in
\ker(\operatorname{Res})/
Z_Q^{10}\ker(\operatorname{Res}).
$$

Changing the lifts by $L_n\mapsto L_n+H_n$, with
$H_n\in\ker(\operatorname{Res})$, gives the exact variation law

$$
\kappa_n\mapsto
\kappa_n-Z_Q^{10}(H_n-H_{n-1}).
$$

Therefore $[\kappa_n]$ is independent of the choice of lift.

The level-2 class is nonzero. This is established by embedding the $D_5$
representation ring injectively into the five-variable Laurent weight ring
and checking that $\kappa_2$ is not divisible by $Z_Q^{10}$. Consequently no
virtual kernel correction, positive or otherwise, can make the exact quotient
hold at level 2.

This upgrades the earlier failure of the peeling algorithm to an algebraic
obstruction for the particular $SO(10)$ HFT numerator uplift under study. It
does not challenge the valid $SO(9)$ quotient or the Bars spectrum after
restriction.

## 1. The fixed level-2 class

The all-chiral reference section gives

$$
\kappa_1=0,
$$

and

$$
\kappa_2=-2A_0+J_{126},
$$

where

$$
J_{126}=[0,0,0,2,0]-[0,0,0,0,2].
$$

Expanded in irreducibles,

$$
\kappa_2=-2[0,0,0,0,0]+[0,0,0,0,2]+[0,0,0,2,0]
-2[0,0,0,1,1]+2[0,0,1,0,0]-2[0,1,0,0,0]
+2[1,0,0,0,0].
$$

It has dimension zero and exact zero restriction. The five-variable Laurent
test gives

$$
Z_Q^{10}\nmid\kappa_2.
$$

Suppose an alternative quotient $Q_2$ restricting to the correct $SO(9)$
character existed. Its difference from the reference increment would lie in
the restriction kernel, say $Q_2-Q_2^{\mathrm{ref}}=H$. Exact division would
then imply $\kappa_2=Z_Q^{10}H$, contradicting the divisibility test. Thus the
obstruction is not caused by positivity or by a poor peeling order.

## 2. Chirality

Although the compact expression contains the outer-chirality difference
$J_{126}$, the complete level-2 anomaly is invariant under interchange of the
two $D_5$ spinor nodes:

$$
\tau(\kappa_2)=\kappa_2.
$$

The $J_{126}$ term compensates the chirality asymmetry of the all-chiral
section contribution $A_0$; it does not make the total obstruction
chirality-odd. A purely outer-chirality explanation of the seed is therefore
not supported.

The later all-chiral reference representatives are not outer-even, beginning
at level 3. Since representatives depend on the chosen section, this fact is
descriptive rather than a canonical statement about their quotient classes.

## 3. Does the level-2 seed generate the later classes?

Let $T$ be the exact boundary-corrected kernel shift from TK2. The simplest
one-seed proposal would identify $\kappa_n$ with $T^{n-2}\kappa_2$, either
exactly or modulo $Z_Q^{10}\ker(\operatorname{Res})$.

The exact equality already fails at level 3 and continues to fail through
level 11.

For a stronger quotient test, the implementation specializes the five torus
variables to a fixed generic regular one-parameter torus and performs exact
Laurent division. Nonzero specialized remainders are rigorous
nondivisibility certificates. Through level 6 it finds:

- every $[\kappa_n]$, for $2\leq n\leq6$, is nonzero;
- for $3\leq n\leq6$, $[\kappa_n]$ is not the class of
  $T^{n-2}\kappa_2$;
- more strongly, $[\kappa_n]$ is outside the rational span of all shifted
  seed classes available through that level;
- the five classes $[\kappa_2],\ldots,[\kappa_6]$ are linearly independent
  over $\mathbb Q$.

The last statement follows because their images under the specialization have
rank five. This rules out the simplest proposal that the level-2 class and its
corrected Regge shifts generate the observed anomaly series. It does not rule
out a richer finite-generator recurrence using other operations.

The regular-torus certificates were deliberately bounded at level 6 because
the exact cost grows quickly. Structural anomaly and exact-shift checks were
continued through level 11.

## 4. Finite-window structure

Relative to the global all-chiral section, the anomaly has a unique expansion
in natural restriction-kernel relations. The finite counts are:

| Level | Irreducible terms | Natural-kernel coordinates | Dimension | Restriction |
| ---: | ---: | ---: | ---: | --- |
| 1 | 0 | 0 | 0 | zero |
| 2 | 7 | 2 | 0 | zero |
| 3 | 11 | 3 | 0 | zero |
| 4 | 31 | 11 | 0 | zero |
| 5 | 49 | 19 | 0 | zero |
| 6 | 71 | 31 | 0 | zero |
| 7 | 99 | 43 | 0 | zero |
| 8 | 141 | 65 | 0 | zero |
| 9 | 182 | 89 | 0 | zero |
| 10 | 253 | 127 | 0 | zero |
| 11 | 324 | 166 | 0 | zero |

The growth shows that the anomaly is not confined to the three positive-lift
families $A$, $B$ and $C$ after multiplication by $Z_Q$. This is not by itself
evidence of fundamental complexity: a compact generating function can have
rapidly growing coefficient support.

The exact affine variation law was also checked on the transport-first,
boundary-first and total-deviation positive paths through level 11. Their
representatives differ, as expected, but all define the same quotient class.

## 5. Interpretation and next question

TK4c separates two problems that had previously been entangled:

1. selecting a positive representative $L_n$ inside a branching fibre;
2. understanding the lift-independent obstruction class $[\kappa_n]$.

The second problem is logically prior. Exact $SO(10)$ division cannot select a
positive lift because it does not exist already at level 2. Any analytic
$SO(10)$ formulation must instead contain an explicit kernel-anomaly term or
work in a quotient that forgets it.

The next useful analytic question is no longer whether one shifted seed
generates the anomaly. It is whether the whole class-valued series

$$
\mathcal K(q)=\sum_{n\geq2}[\kappa_n]q^n
$$

has a compact presentation inherited directly from the HFT numerator—for
example as a finite module of sources under several natural operations. No
cohomological interpretation has yet been established.

## Limitations

- Exact structural computations and positive-path variation checks extend
  through level 11 only.
- Full five-variable Laurent nondivisibility was checked directly at levels 2
  and 3. The generic regular-torus specialization certifies the quotient-class
  statements through level 6.
- A nonzero specialization is a proof of nondivisibility; a vanishing
  specialization would be inconclusive. All claimed certificates are in the
  nonzero direction.
- The calculation concerns the chosen virtual $SO(10)$ uplift of the HFT
  numerator. It does not exclude a differently formulated analytic object
  with the same $SO(9)$ restriction.

## Reproduction

```text
./bin/sage-run -m trajectory_kernel.kernel_anomaly --self-test
./bin/sage-run -m trajectory_kernel.kernel_anomaly --max-level 6 --certificate-level 6
./bin/sage-run -m trajectory_kernel.kernel_anomaly --max-level 11 --certificate-level 6
```

The level-11 run is exact but can take several minutes.
