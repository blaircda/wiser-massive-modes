# TK6B.3 — Boundary Shells and the Failure of $A/B/C$ Completeness

**Status:** universal all-split kernel identity proved; arbitrary-length
$A/B/C$ row theorem proved conditionally; $A/B/C$ completeness refuted by the
baseline-free level-12 HFT shell

**Provenance:** baseline-free

**Last updated:** 25 September 2026

## Result

TK6B.2 observed that the level-11 Gale rows were controlled by three kernel
chains $A$, $B$ and $C$. Two logically different conjectures were implicit in
that observation:

1. if the kernel coordinates consist of arbitrary initial segments of the
   $A$, $B$ and $C$ chains, their Gale rows obey the compact TK6B.2 template;
2. the HFT branching closures continue to contain only those three chains.

The first statement is true. It follows exactly from the support collisions
among the six terms of the three kernel identities, for arbitrary chain
lengths.

The second statement is false at the first untested horizon. The baseline-free
level-12 HFT closure has 16 kernel generators. Besides the extensions $A_6$,
$B_3$ and $C_2$, it contains the two new top weights

$$
[0,2,0,2]_9,
$$

$$
[0,0,1,2]_9.
$$

Thus the level-11 $A/B/C$ template is not the all-orders Gale template.

There is nevertheless a stronger local theorem. Every consecutive pair of
allowed parents is related by one universal six-term interlacing-shell
identity. The natural relation between the $k$th parent and the all-chiral
parent is the telescoping sum of the first $k$ shells and has $4k+2$ terms.
This closes the local kernel formula for every possible parent split. The
correct organizing object is therefore a sparse collision hypergraph of local
interlacing-shell relations, not a fixed list of three trajectory families.

## 1. Universal all-split shell theorem

Let

$$
\mu=[\ell,m,r,s]_9,
$$

and put

$$
P_k=[\ell,m,r,k,s-k]_{10},
$$

where

$$
0\leq k\leq\left\lfloor\frac{s}{2}\right\rfloor.
$$

For $1\leq k\leq\lfloor s/2\rfloor$, define four all-chiral packets

$$
Q_{1,k}=[\ell,m,r+k,0,s-2k],
$$

$$
Q_{2,k}=[\ell,m+r+1,k-1,0,s-2k],
$$

$$
Q_{3,k}=[\ell+m+1,r,k-1,0,s-2k],
$$

$$
Q_{4,k}=[m,r,k-1,0,s-2k].
$$

The consecutive-shell character is

$$
\mathcal S_k
=P_k-P_{k-1}-Q_{1,k}+Q_{2,k}-Q_{3,k}+Q_{4,k}.
$$

For every nonnegative $\ell,m,r,s$ and every allowed $k\geq1$,

$$
\operatorname{Res}^{D_5}_{B_4}\mathcal S_k=0.
$$

All six terms are distinct and all coefficients are $+1$ or $-1$.

### Interlacing proof

Write the orthogonal coordinates of the common top boundary as

$$
a=\ell+m+r+\frac{s}{2},
$$

$$
b=m+r+\frac{s}{2},
$$

$$
c=r+\frac{s}{2},
$$

$$
d=\frac{s}{2},
$$

and let

$$
e=d-k.
$$

The orthogonal coordinates of $P_k$ are

$$
(a,b,c,d,e).
$$

The difference between the restrictions of $P_k$ and $P_{k-1}$ is exactly
the interlacing slice

$$
a\geq x_1\geq b\geq x_2\geq c\geq x_3\geq d,
$$

$$
x_4=e.
$$

Write $Q(A,B,C,E)$ for the all-chiral $D_5$ packet with orthogonal highest
weight $(A,B,C,E,E)$. Inclusion-exclusion on the unwanted lower face gives

$$
\operatorname{Res}(P_k-P_{k-1})
=Q(a,b,c,e)-Q(a,b,d-1,e)
$$

$$
\mathrel{\phantom{\operatorname{Res}(P_k-P_{k-1})=}}
+Q(a,c-1,d-1,e)-Q(b-1,c-1,d-1,e).
$$

Converting these four orthogonal weights back to $D_5$ Dynkin labels gives
exactly $Q_{1,k},Q_{2,k},Q_{3,k},Q_{4,k}$. Since
$D_5\downarrow B_4$ branching is multiplicity-free, the slice-indicator
identity proves the character identity for arbitrary labels and splits.

### Natural relation to the all-chiral section

The natural kernel coordinate compares $P_k$ directly with $P_0$. Summing the
consecutive shells telescopes:

$$
K^{(k)}_{\ell,m,r,s}
=\sum_{t=1}^{k}\mathcal S_t.
$$

Equivalently,

$$
K^{(k)}_{\ell,m,r,s}
=P_k-P_0
+\sum_{t=1}^{k}(-Q_{1,t}+Q_{2,t}-Q_{3,t}+Q_{4,t}).
$$

The terms for different $t$ have distinct fifth Dynkin labels, so this has
exactly $4k+2$ distinct terms, again with unit coefficients. In particular,
the formerly observed ten-term second-parent relations are the case $k=2$;
they are not new sporadic identities.

The implementation subjects the theorem to three complementary exact checks:

1. exact branching of every consecutive and telescoped relation;
2. direct equality between the telescoped sum and the closed formula;
3. exact triangular reconstruction of the natural relation from
   $\operatorname{Res}(P_k)$ on the all-chiral section.

The routine self-test includes nonzero leading labels and splits through
$k=3$. The main analysis checks every split for $[0,0,0,s]$ with
$2\leq s\leq6$ by default. None of these checks imports protected
$SO(10)$ completion data.

### First-split specialization

For $k=1$, the theorem reduces to the earlier six-term identity

$$
K_{\ell,m,r,s}^{(1)}
=
[\ell,m,r,1,s-1]
-[\ell,m,r,0,s]
-[\ell,m,r+1,0,s-2]
$$

$$
\mathrel{\phantom{K_{\ell,m,r,s}^{(1)}=}}
+[\ell,m+r+1,0,0,s-2]
+[m,r,0,0,s-2]
-[\ell+m+1,r,0,0,s-2].
$$

Every natural generator in the complete level-12 closure happens to have
$k=1$ and agrees with this specialization.

## 2. Why the arbitrary-length $A/B/C$ template is exact

The old families are the specializations

$$
A_\ell=K_{\ell,0,0,2}^{(1)},
$$

$$
B_\ell=K_{\ell,1,0,2}^{(1)},
$$

$$
C_\ell=K_{\ell,0,0,3}^{(1)}.
$$

For arbitrary initial chain lengths, transpose these six-term relations to
form the Gale rows. The two parent pivots of every generator give

$$
\pm e_G.
$$

The only nontrivial collisions among the four auxiliary parents are:

- all $A_\ell$ meet at the trivial parent;
- all $C_\ell$ meet at the chiral spinor parent;
- all $B_\ell$ meet at the vector parent, where $A_0$ has the opposite sign;
- the last parent of $B_i$ meets the last parent of $A_{i+1}$.

Consequently the distinct row types are exactly

$$
0,
$$

$$
\pm e_G,
$$

$$
-e_{B_i}-e_{A_{i+1}},
$$

$$
\sum_i e_{A_i},
$$

$$
\sum_i e_{B_i}-e_{A_0},
$$

$$
\sum_i e_{C_i},
$$

with absent chains or unavailable adjacent pairs simply omitted. This is a
support-collision proof for arbitrary chain lengths; it is not an extrapolation
from levels 1--11.

## 3. Exact level-12 obstruction

The nested domain sizes are:

| HFT horizon | $B_4$ rows | Packets | Kernel rank | Distinct Gale row types |
| ---: | ---: | ---: | ---: | ---: |
| 11 | 73 | 84 | 11 | 29 |
| 12 | 92 | 108 | 16 | 43 |

The five new level-12 generators are:

| Name | Top $B_4$ weight | Alternative $D_5$ parent | Status |
| --- | --- | --- | --- |
| $A_6$ | $(6,0,0,2)$ | $(6,0,0,1,1)$ | old family |
| $B_3$ | $(3,1,0,2)$ | $(3,1,0,1,1)$ | old family |
| $C_2$ | $(2,0,0,3)$ | $(2,0,0,1,2)$ | old family |
| $D_0$ | $(0,2,0,2)$ | $(0,2,0,1,1)$ | new family |
| $E_0$ | $(0,0,1,2)$ | $(0,0,1,1,1)$ | new family |

Here $D_0$ and $E_0$ are temporary report labels, not claims of canonical
nomenclature.

All 16 generators agree exactly with
$K_{\ell,m,r,s}^{(1)}$. Their 43 Gale row types consist of:

- one zero type;
- 32 signed-coordinate types $\pm e_G$;
- ten composite collision types.

Writing $D=D_0$ and $E=E_0$, the ten composites are

$$
\sum_{i=0}^{6}e_{A_i},
$$

$$
-e_{B_2}-e_{A_3},
$$

$$
-e_{B_3}-e_{A_4},
$$

$$
\sum_{i=0}^{3}e_{B_i}-e_{A_0},
$$

$$
\sum_{i=0}^{2}e_{C_i},
$$

$$
-e_E+e_{A_1},
$$

$$
e_E+e_{A_0},
$$

$$
e_E+e_{B_0},
$$

$$
-e_D-e_{B_1}-e_{A_2},
$$

$$
e_D-e_{B_0}-e_{A_1}.
$$

Thus the new families do not merely append independent coordinates. They
replace two former pairwise $A/B$ collisions by larger collision nodes.

## 4. Level-13 look-ahead

An independent baseline-free HFT computation, without constructing the full
level-13 packet cone, finds the following new ambiguous top weights directly
in the single-level spectrum:

$$
(0,1,0,3),
$$

$$
(1,0,1,2),
$$

$$
(1,2,0,2),
$$

$$
(3,0,0,3),
$$

$$
(4,1,0,2),
$$

$$
(7,0,0,2).
$$

In particular, the two level-12 families acquire their next leading-label
translate and the additional tail $(m,r,s)=(1,0,3)$ appears. Family growth is
therefore continuing rather than an isolated level-12 accident. All direct
ambiguous weights through this look-ahead still have $s\leq3$, so the finite
HFT data exercise only $k=1$. The all-$k$ theorem above is instead a structural
branching result and does not depend on waiting for an HFT level with $s\geq4$.

## 5. Revised all-orders object

For a finite set $T$ of ambiguous top weights, attach a coordinate
$e_{\mu,k}$ for every

$$
\mu=[\ell,m,r,s]\in T,
$$

$$
1\leq k\leq\left\lfloor\frac{s}{2}\right\rfloor.
$$

Use the natural telescoped relations $K^{(k)}_\mu$ as the kernel basis. The
non-reference parent $P_k$ gives the unique row $+e_{\mu,k}$. At each
all-chiral parent $p$, sum the signed incidences of every natural relation
which contains $p$. The Gale rows are then exactly:

- zero rows;
- the non-reference pivot rows $+e_{\mu,k}$;
- the nonzero signed incidence vectors at collision nodes $p$.

Equivalently, one may use the consecutive shells $\mathcal S_k$ as local
edges; the change to the natural basis is triangular and integral. This
collision hypergraph is a uniform construction even though its vertices and
circuits grow with the HFT horizon. The positive-facet problem becomes the
classification of primitive minimally supported nonnegative relations among
its incidence vectors. TK6B.4 shows that their coefficients need not all be
one.

The parent-split formula itself is therefore no longer a source of
level-by-level discovery. The mass level enters only by selecting a finite
induced sub-hypergraph and by supplying the target multiplicities on which its
positive-circuit inequalities must be tested.

This does not yet prove Bars III.B. The remaining tasks are now:

1. classify or recursively generate the primitive weighted circuits of the
   full all-split collision hypergraph;
2. prove the corresponding weighted circuit inequalities for the cumulative
   HFT triangular coordinates;
3. prove all-orders saturation or construct integral packetizations directly.

TK6B.4 answers the former unit-coefficient question negatively: the complete
HFT level-13 closure contains eight primitive coefficient-two circuit types.
See `TK6B4_WEIGHTED_CIRCUITS.md`.

The former conjecture that a fixed finite list of kernel families suffices
should not be used in an all-orders argument.

## Reproduction

```text
./bin/sage-run -m trajectory_kernel.boundary_shell --self-test
./bin/sage-run -m trajectory_kernel.boundary_shell --max-level 12 --previous-level 11 --branch-check-ell 2 --split-check-max-s 6
./bin/sage-run -m trajectory_kernel.boundary_shell --max-level 12 --previous-level 11 --branch-check-ell 2 --split-check-max-s 6 --lookahead-level 13 --verbose
```

The final command performs independent exact HFT and Weyl-character
calculations and can take several minutes. No protected $SO(10)$ completion is
imported.
