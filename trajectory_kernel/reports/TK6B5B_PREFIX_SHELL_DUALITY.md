# TK6B.5b/c — Prefix-Shell Duality and Regge Tails

**Status:** pivot-elimination theorem proved; fixed finite-circuit route
obstructed; universal interval-tail family proved; exact HFT Regge
factorization implemented; stable Pieri lemma subsequently proved in
TK6B.5d; all-degree remainder support remains open

**Provenance:** baseline-free

**Last updated:** 25 September 2026

## Result

The growing Gale system of TK6B.4 has a cutoff-independent local
presentation. Every non-all-chiral parent is the unique positive unit pivot
of one natural shell coordinate. Eliminating these pivots replaces the Gale
circuit equation by explicit prefix-shell inequalities on nonnegative
functions over all-chiral parents.

This yields three new conclusions.

1. The finite weighted-circuit criterion is exactly dual to a local shell
   decomposition problem; no circuit enumeration is needed to state it.
2. The full infinite operator has no nonzero finitely supported positive
   circuit. Finite-horizon circuits are necessarily moving boundary objects,
   which explains why their lists do not stabilize.
3. Important horizon-growing circuits nevertheless telescope after the
   TK6B.5 Möbius pullback. A universal split-chain tail has at most eight HFT
   endpoint terms, independently of its length.

The simple endpoint phenomenon does not cover every mixed circuit. In the
small box $0\leq m\leq1$, $r=0$, $2\leq s\leq4$, increasing the leading-label
horizon from $\ell=0$ to $\ell\leq1$ increases the largest pulled-functional
support from 24 to 45. Thus a further tail-module or core decomposition is
required.

On the HFT side, the exact symmetric-vector factorization suggested by
Hanany--Forcella--Troost has been implemented. Through level 13:

- its convolution reconstructs the primary series exactly;
- all 185 eligible adjacent $\ell$ shifts hold separately at every virtual
  remainder degree;
- the degree-$d$ remainder obeys
  $2\ell+2m+2r+s\leq d-1$ for every observed term with $d\geq2$;
- the first $A$-chain endpoint multiplicities are $(1,3,3)$, so that tail's
  slack is the cumulative singlet multiplicity minus one.

These are exact finite computations, not an all-orders proof. They identify a
concrete next theorem: prove the remainder support bound from the oscillator
product and prove the associated stable $B_4$ Pieri shift.

## 1. Eliminating the alternative pivots

Let $g=(\mu,k)$ label a natural relation between the $k$th parent above
$\mu=[\ell,m,r,s]_9$ and the all-chiral section. Write its all-chiral part as
$V_{p,g}$. The non-chiral parent $P_k$ occurs in this relation with
coefficient $+1$ and occurs in no other natural relation. If $x_g$ is its
coefficient in a positive Gale relation and $y_p$ is the coefficient on an
all-chiral parent, the Gale equation is

$$
x_g+\sum_pV_{p,g}y_p=0.
$$

Define

$$
L_{g,p}=-V_{p,g}.
$$

Then

$$
x_g=(Ly)_g.
$$

Consequently the positive Gale cone is linearly isomorphic to

$$
\mathcal Y={y:y\geq0,\ Ly\geq0}.
$$

The inverse map is unique: retain $y$ on all-chiral parents and restore the
alternative pivots as $x=Ly$. It preserves extreme rays. Exact PPL
enumeration verifies the ray-by-ray bijection in the test systems, including
all 4,900 full circuits of the coefficient-two box
$0\leq\ell,m\leq1$, $r=0$, $2\leq s\leq4$.

## 2. Closed prefix-shell operator

For a nonnegative function $y$ on $B_4$ top labels, the row indexed by
$g=(\ell,m,r,s;k)$ is

$$
(Ly)_g
=y_{\ell,m,r,s}
+\sum_{t=1}^{k}
\left(
y_{Q_{1,t}}-y_{Q_{2,t}}+y_{Q_{3,t}}-y_{Q_{4,t}}
\right),
$$

where the four $Q$ labels are the top $B_4$ labels of the TK6B.3 shell
packets. Explicitly,

$$
Q_{1,t}=(\ell,m,r+t,s-2t),
$$

$$
Q_{2,t}=(\ell,m+r+1,t-1,s-2t),
$$

$$
Q_{3,t}=(\ell+m+1,r,t-1,s-2t),
$$

$$
Q_{4,t}=(m,r,t-1,s-2t).
$$

This formula is exact for arbitrary labels and splits. The implementation
compares it entry by entry with the transposed natural shell relations.

Let $c$ be the all-chiral section coordinates of a target. Nonnegative shell
counts $z$ give final coefficients

$$
u=c-L^Tz
$$

on all-chiral parents and $z$ on alternative parents. Hence rational positive
liftability is equivalent to

$$
c=u+L^Tz,
$$

$$
u\geq0,
$$

$$
z\geq0.
$$

The dual identity is

$$
\langle y,c\rangle
=\langle y,u\rangle+\langle Ly,z\rangle.
$$

Farkas duality therefore gives the uniform criterion

$$
\langle y,c\rangle\geq0
\quad\hbox{for every}\quad y\geq0,\ Ly\geq0.
$$

Primitive weighted circuits are simply the extreme rays of this cone.

## 3. No finite-support circuit in the full infinite system

The infinite shell operator is column-finite but not row-finite. The packet
$Q_{4,t}$ forgets the leading label $\ell$. This produces an exact
obstruction to the former idea of classifying fixed finite circuits.

Take any nonzero finitely supported $y\geq0$ and choose a label

$$
p=(L,M,R,S)
$$

with $y_p>0$. Put

$$
k=R+1
$$

and consider shell coordinates with top weight

$$
\mu_E=(E,L,M,S+2R+2)
$$

as $E$ tends to infinity. At step $t=k$, the fourth packet is exactly $p$.
For $E$ larger than every leading label in the finite support, the reference,
$Q_1$, $Q_2$ and $Q_3$ terms all vanish. The surviving terms give

$$
(Ly)_{(\mu_E,k)}
=-
\sum_{t=1}^{k}
y_{L,M,t-1,S+2(k-t)}
\leq-y_p<0.
$$

Thus

$$
y\geq0,\quad Ly\geq0,\quad
\operatorname{supp}(y)\ \hbox{finite}
$$

implies $y=0$ in the complete infinite system.

This does not make the finite-horizon inequalities irrelevant. It says their
supports must move or grow with the horizon. An all-orders proof must control
coherent boundary-tail families rather than expect a fixed finite circuit
list.

## 4. Universal interval tails

Fix one top-weight family

$$
(\ell,m,r,s),\qquad 0\leq\ell\leq H,
$$

and one allowed split $t$. Define $y$ to equal one on the interval

$$
(j,r,t-1,s-2t),
\qquad m\leq j\leq m+H+1,
$$

and zero elsewhere. In every relevant shell coordinate, the $Q_{3,t}$ and
$Q_{4,t}$ values cancel. All other terms vanish. Hence $Ly=0$ on this finite
family. Exact cone enumeration confirms that this is a primitive extreme ray.

Pairing it with the section coordinates gives

$$
\sum_{j=A}^{B}c_{j,p,q,u}.
$$

The leading-coordinate factor of the TK6B.5 Möbius operator telescopes. Its
HFT pullback is

$$
\sum_{\epsilon_2,\epsilon_3\in\{0,1\}}
(-1)^{\epsilon_2+\epsilon_3}
\left[
M_{A-\epsilon_2,
  p+\epsilon_2-\epsilon_3,
  q+\epsilon_3,u}
-M_{B+1-\epsilon_2,
  p+\epsilon_2-\epsilon_3,
  q+\epsilon_3,u}
\right],
$$

with invalid labels omitted. There are at most eight endpoint terms,
regardless of $H$.

For the $A_\ell$ chain, $m=r=0$, $s=2$, $t=1$, this becomes

$$
\sum_{\ell=0}^{H+1}c_{\ell,0,0,0}
=M_{0,0,0,0}
-M_{H+1,0,1,0}
+M_{H+1,1,0,0}
-M_{H+2,0,0,0}.
$$

At HFT level $n$, the complete $A$ chain has $H=n-6$ in the tested range.
Through level 13 the three moving endpoint multiplicities are exactly
$(1,3,3)$, so this slack is

$$
M_n(0,0,0,0)-1.
$$

Conditional on the all-orders endpoint stability and HFT positivity, this
entire infinite family is therefore nonnegative because the level-1 singlet
persists in the cumulative spectrum.

## 5. Mixed-circuit obstruction

The endpoint collapse is not automatic for every primitive circuit. Exact
finite boxes give:

| Top-weight box | Full circuits | Maximum circuit coefficient | Largest HFT pullback support |
| --- | ---: | ---: | ---: |
| $\ell=0$, $0\leq m\leq1$, $r=0$, $2\leq s\leq4$ | 178 | 1 | 24 |
| $0\leq\ell,m\leq1$, $r=0$, $2\leq s\leq4$ | 4,900 | 2 | 45 |

Thus neither primitive circuit support nor pulled-functional support is
uniformly bounded by the simple interval-tail theorem. A successful induction
must prove that mixed circuits are assembled from a recursively controlled
tail module and boundary core, or dominate inequalities of that form. The
present data do not establish such a decomposition.

## 6. Exact HFT symmetric-vector factorization

Hanany--Forcella--Troost give the exact formal factorization

$$
Z_m(q)=\operatorname{PE}([1,0,0,0]_9q)Z'_m(q).
$$

The symmetric-vector coefficient is

$$
[q^a]\operatorname{PE}([1,0,0,0]_9q)
=\sum_{j=0}^{\lfloor a/2\rfloor}[a-2j,0,0,0]_9.
$$

Writing the project level as $n=a+1$, the implementation reconstructs the
virtual remainder recursively and verifies the convolution exactly. The
remainder is genuinely virtual: negative irreducible coefficients occur at
degrees 2, 3, 4 and 7 in the window through degree 12.

Two finite observations are especially useful.

First, every observed remainder term at degree $d\geq2$ obeys

$$
2\ell+2m+2r+s\leq d-1.
$$

This is a half-slope bound on the first orthogonal coordinate after the full
leading Regge tower is removed.

Second, for every adjacent $\ell$ shift which satisfies the empirical GMSZ
chamber condition through level 13, the equality holds separately in every
summand

$$
\operatorname{Sym}^{a-d}([1,0,0,0]_9)\otimes Z'_{m,d}.
$$

There are 185 such shifts and no termwise failure. Therefore the observed
shift is not produced by cancellation among different remainder degrees in
this window.

The natural all-orders proof target identified at this stage was:

1. derive the half-slope support bound for every $Z'_{m,d}$ directly from the
   HFT oscillator product;
2. prove a stable $B_4$ Pieri lemma showing that multiplication by consecutive
   symmetric-vector coefficients transports outer-chamber multiplicities by
   $\ell\mapsto\ell+1$;
3. apply that lemma term by term to derive the $\ell$ shift, rather than assume
   the empirical GMSZ recurrence.

This would prove the endpoint stability of the interval-tail inequalities and
provide the first analytic piece of the required circuit induction. It would
not by itself control all mixed circuits or settle integrality.

The second item is now proved, in fact for arbitrary tensorial and spinorial
$B_n$ weights, by the Racah--Speiser stabilizer argument in
`TK6B5D_STABLE_PIERI_TRANSLATION.md`. The finite half-slope bound alone is not
strong enough to imply its hypothesis for every formal remainder term; the
remaining statement must include the tensor-product coupling conditions.

## 7. Literature boundary

The HFT paper supplies the exact covariant generating series and explicitly
factors the symmetric-vector tower, while warning that the remaining series
can contain negative terms. See
[arXiv:1007.2622](https://arxiv.org/abs/1007.2622) and its
[INSPIRE record](https://inspirehep.net/literature/861347).

Georgoudis--Minahan--Ström--Zoumis compute very high finite orders and state
the $\ell$, $m$ and $r$ relations as **empirical shift relations**. They are
valuable evidence and an efficient computational rule, but not an available
all-orders theorem. See
[arXiv:2609.04107](https://arxiv.org/abs/2609.04107) and its
[INSPIRE record](https://inspirehep.net/literature/3199641).

## Reproduction

```text
./bin/sage-run -m trajectory_kernel.shell_duality --self-test
./bin/sage-run -m trajectory_kernel.regge_factorization --max-level 13
```

Both modules derive their branching or HFT input independently and import no
protected $SO(10)$ completion.
