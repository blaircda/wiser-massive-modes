# TK6B.5 — Local HFT Form of the Weighted Inequalities

**Status:** all-label Möbius formula and circuit pullback proved; exact
translation covariance proved; all-orders circuit positivity remains open

**Provenance:** baseline-free

**Last updated:** 25 September 2026

## Result

The triangular all-chiral section used in TK6B.2--TK6B.4 has a closed local
inverse. If

$$
M(\ell,m,r,s)
$$

is the multiplicity of $[\ell,m,r,s]_9$ in an arbitrary finite $B_4$
character, then the coefficient of the selected $D_5$ parent
$[\ell,m,r,0,s]_{10}$ is

$$
c_{\ell,m,r,s}
=
\sum_{\epsilon_1,\epsilon_2,\epsilon_3\in\{0,1\}}
(-1)^{\epsilon_1+\epsilon_2+\epsilon_3}
M(\ell+\epsilon_1-\epsilon_2,
  m+\epsilon_2-\epsilon_3,
  r+\epsilon_3,s).
$$

Here $M$ is extended by zero outside the dominant chamber. Thus every
weighted circuit inequality has an explicit pullback to a finite signed sum
of HFT $B_4$ multiplicities. A circuit supported on $t$ all-chiral parents
uses at most $8t$ multiplicity entries before cancellations.

This is an all-label statement about $B_4\subset D_5$ branching. It contains
no HFT cutoff. The implementation agrees with independent exact triangular
matrix inversion on every cumulative HFT target through level 13, including
all 113 labels in the complete level-13 closure.

The formula narrows, but does not finish, TK6B.5. The remaining theorem is
positivity of these signed HFT partial sums for the complete recursively
generated family of weighted circuits. Integral liftability also still
requires a general saturation theorem or a direct integral packetization.

## 1. Interlacing derivation

Write the orthogonal coordinates of an all-chiral parent as

$$
\lambda=(a,b,c,d,d)
$$

and those of a $B_4$ child as

$$
\mu=(x,y,z,w).
$$

The multiplicity-free $D_5\downarrow B_4$ interlacing inequalities are

$$
a\geq x\geq b\geq y\geq c\geq z\geq d\geq w\geq |d|.
$$

Hence $w=d$. If $C(a,b,c,d)$ is the coefficient of the all-chiral parent,
the target multiplicity is

$$
M(x,y,z,d)
=
\sum_{a\geq x}\sum_{y\leq b\leq x}\sum_{z\leq c\leq y}
C(a,b,c,d).
$$

Take a forward difference in $z$:

$$
M(x,y,z,d)-M(x,y,z+1,d)
=
\sum_{a\geq x}\sum_{y\leq b\leq x}C(a,b,z,d).
$$

A forward difference in $y$ then leaves

$$
\sum_{a\geq x}C(a,y,z,d),
$$

and a forward difference in $x$ leaves $C(x,y,z,d)$. Zero extension handles
the walls $x=y$ and $y=z$ without separate correction terms.

For $[\ell,m,r,s]_9$ the orthogonal coordinates are

$$
x=\ell+m+r+s/2,
$$

$$
y=m+r+s/2,
$$

$$
z=r+s/2,
$$

$$
d=s/2.
$$

Increasing $(x,y,z)$ by $(\epsilon_1,\epsilon_2,\epsilon_3)$ gives the Dynkin
labels in the displayed eight-term formula. This proves the formula for all
integral and spinorial label cosets at once.

## 2. Pullback of a weighted circuit

Let a finite positive Gale circuit give the section-coordinate inequality

$$
\sum_\mu \alpha_\mu c_\mu\geq0,
$$

where $\alpha_\mu$ is the circuit coefficient on an all-chiral parent;
non-reference parents contribute zero in these coordinates. Substitution of
the local formula gives

$$
\sum_\lambda \beta_\lambda M(\lambda)\geq0,
$$

with

$$
\beta_\lambda
=
\sum_{\mu,\epsilon:\,\lambda=\mu+\delta(\epsilon)}
\alpha_\mu(-1)^{|\epsilon|}.
$$

The map $\alpha\mapsto\beta$ is implemented exactly by
`pullback_coordinate_functional`. It applies without a unit-coefficient
assumption, so the coefficient-two circuits found in TK6B.4 require no
special case.

This is the desired bridge from the branching cone to HFT data: a facet is no
longer an inequality involving a matrix inverse, but a local signed
multiplicity inequality.

## 3. Cumulative HFT series

Let $m_n(\lambda)$ be the multiplicity in the single-level primary $r_n^9$
and let

$$
M_n(\lambda)=\sum_{i=1}^n m_i(\lambda).
$$

The finite-difference operator is linear, so

$$
c_n(\mu)=\sum_{i=1}^n (D m_i)(\mu).
$$

For a fixed weighted circuit functional $\Phi$ this gives

$$
\sum_{n\geq1}\Phi(M_n)q^n
=
\frac{1}{1-q}\Phi\!\left(\sum_{n\geq1}m_nq^n\right).
$$

Thus TK6B.5 is precisely a partial-sum positivity problem for explicit local
coefficient functionals of the HFT quotient series. The implementation checks
this commutation directly through level 13, but the identity itself is formal
and cutoff-independent.

## 4. Translation covariance and the GMSZ route

The eight-term operator has constant coefficients on the Dynkin-label
lattice. If $T_\delta$ translates a multiplicity table and all translated
labels remain dominant, then

$$
D(T_\delta M)=T_\delta(DM).
$$

Consequently, whenever a GMSZ multiplicity shift holds on the complete
eight-point stencil of a section coordinate, that section coordinate obeys
the same shift. A simultaneously translated weighted circuit has the same
slack. This gives a precise conditional induction mechanism:

1. translate interior shell circuits back toward a boundary or residual core;
2. use HFT/GMSZ multiplicity transport on every required stencil;
3. prove only the circuit inequalities which cannot be transported further.

What is not yet known is whether the residual circuit core is finite or has a
uniform recursive description. The GMSZ relations used elsewhere in the
project are also finite-window empirical identities until derived from the
oscillator product. Translation covariance of $D$ therefore supplies the
intertwiner needed by an induction, not the induction hypothesis itself.

## 5. Why finite circuit checks do not close the proof

A circuit in a horizon-$N$ Gale matrix is a relation among rows in the kernel
coordinates visible at that horizon. When later shell generators are added,
those parent rows can acquire new coordinates. The old relation is not
automatically a circuit, or even a relation, of the enlarged Gale
configuration. This is why checking higher and higher levels alone cannot
produce a closed statement.

The next all-orders object is the column-finite infinite shell operator, or an
equivalent recursive presentation. Its rows need not have finite support; the
$Q_4$ collision already creates leading-label tails. As proved in the
follow-up TK6B.5b report, the complete infinite positive circuit cone has no
nonzero finitely supported ray. One must therefore show that every relevant
horizon-dependent circuit is either:

- a translate of a controlled earlier circuit;
- generated by a controlled boundary/core operation; or
- dominated by inequalities already proved.

Only after that structural statement can the local HFT pullback eliminate the
level cutoff.

There is also a separate integrality issue. Weighted circuit inequalities
characterize rational cone membership in each finite closure. The level-11
packet semigroup is saturated, while level 12 and 13 have exact integral
witnesses for the particular HFT targets. Neither fact proves saturation of
every finite downward-closed packet domain.

## 6. Next exact targets

The next useful work is now sharply defined:

1. formulate the infinite all-split shell operator and classify coherent
   boundary-tail circuit families under $\ell$, $m$ and $r$ translations;
2. identify the irreducible boundary/core circuit operations;
3. pull those templates back with the eight-term formula;
4. derive the resulting partial-sum inequalities from the HFT oscillator
   product or from a proved GMSZ recurrence;
5. independently prove saturation or give a recursive integral packetization.

The direct $D_5$ HFT numerator quotient does not currently bypass these
steps: TK4B/TK4C record an exact level-2 kernel anomaly for the naïve quotient
construction.

## Reproduction

```text
./bin/sage-run -m trajectory_kernel.hft_weighted_inequalities --max-level 13
```

The command derives the $B_4$ targets from the HFT oscillator formula,
compares the local expression with an independent exact matrix inverse,
checks cumulative commutation and weighted-functional pullback, and exercises
translation and dominance-wall cases. It imports no protected $SO(10)$
completion.
