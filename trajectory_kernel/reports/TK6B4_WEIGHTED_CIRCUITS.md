# TK6B.4 — Weighted Positive Circuits

**Status:** exact weighted-circuit criterion proved for every finite packet
closure; unit-coefficient conjecture refuted; baseline-free HFT closures
classified through level 13

**Provenance:** baseline-free

**Last updated:** 25 September 2026

## Result

TK6B.2 found that every positive Gale circuit through HFT horizon 11 had
coefficient one. TK6B.3 replaced the finite $A/B/C$ kernel list by a universal
all-split collision hypergraph. TK6B.4 now shows:

1. positive liftability in any finite closure has an exact **weighted**
   circuit formulation;
2. repeated Gale rows can be compressed without losing circuit types, and the
   full facet count is recovered combinatorially;
3. the unit-coefficient phenomenon survives the complete HFT closures through
   level 12;
4. it fails in the complete level-13 HFT closure, where eight primitive
   circuit types have coefficient two;
5. the cumulative level-13 HFT target nevertheless satisfies all 162,739
   expanded facet inequalities and has an exactly verified nonnegative
   integral packet decomposition.

Thus the former zero-one Hall criterion is not the all-orders statement. Its
replacement is a weighted Hall-type criterion indexed by primitive positive
circuits of the universal shell hypergraph.

## 1. General finite weighted-circuit criterion

Let

$$
A\in\mathbb Z^{d\times p}
$$

be a finite $D_5\downarrow B_4$ packet matrix. Let

$$
K\in\mathbb Z^{p\times k}
$$

be the natural all-chiral-section kernel basis supplied by the TK6B.3
all-split formulas. Then

$$
AK=0.
$$

The closed shell formulas have one unique non-reference pivot per coordinate,
so they form an integral triangular basis of the kernel. Write $g_j$ for the
$j$th row of $K$. A packet-slack vector belongs to the dual cone precisely
when

$$
x_j\geq0,
$$

$$
\sum_{j=1}^{p}x_jg_j=0.
$$

The primitive extreme rays of this cone are the positive Gale circuits. Since
the all-chiral packet submatrix $U$ is unimodular, a $B_4$ target $m$ has
integral triangular coordinates

$$
c=U^{-1}m.
$$

If $x$ is a positive circuit, its facet inequality is

$$
\sum_{j\in\operatorname{Ref}}x_jc_j\geq0.
$$

This is an exact rational liftability criterion for every finite closure. It
becomes a subset-sum inequality only when all nonzero $x_j$ equal one.

Saturation of the packet semigroup is a separate question. When saturation is
unknown, the weighted inequalities prove rational cone membership, while an
explicit nonnegative integral packet witness proves integral liftability for
the particular target.

## 2. Exact compression by Gale row type

Suppose a Gale row type $g$ occurs several times. An extreme nonnegative
relation cannot use two different copies of $g$: transferring a sufficiently
small amount between the two copies gives a nontrivial two-sided perturbation,
contradicting extremality. Therefore every full positive circuit selects at
most one realization of each distinct Gale row type.

Conversely, take a primitive circuit of the distinct row types and choose one
actual parent realizing every supported type. The resulting full slack vector
is again extreme. Indeed, any decomposition would project to a decomposition
of the type circuit; extremality fixes the projected summands, while the
chosen support prevents redistribution among duplicate rows.

Consequently, if a type circuit uses types $t$ with multiplicities $m_t$, it
expands into exactly

$$
\prod_t m_t
$$

actual facets. This compression reproduces the previously known 2,508
level-11 facets exactly, without constructing the packet cone's full
$H$-representation.

For testing a target, the minimum over every expansion is also separable by
row type: for each supported type, choose the realization which minimizes its
weighted reference-coordinate contribution. Thus every expanded inequality
can be checked without listing it individually.

## 3. Complete HFT closures through level 13

The exact results are:

| HFT horizon | $B_4$ rows | Packets | Kernel rank | Gale row types | Circuit types | Expanded facets | Circuit coefficients |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 11 | 73 | 84 | 11 | 29 | 40 | 2,508 | 40 with maximum 1 |
| 12 | 92 | 108 | 16 | 43 | 140 | 18,923 | 140 with maximum 1 |
| 13 | 113 | 135 | 22 | 60 | 495 | 162,739 | 487 with maximum 1; 8 with maximum 2 |

The level-11 row and circuit counts reproduce TK6B.2 exactly. At every
horizon the closed TK6B.3 relations form the full kernel basis, and every
enumerated circuit support has rank one less than its cardinality, confirming
minimality independently of the polyhedral extreme-ray flag.

The cumulative targets behave as follows:

| HFT horizon | Negative triangular coordinates | Minimum coordinate | Minimum weighted-facet slack | Exact integral packet witness |
| ---: | ---: | ---: | ---: | --- |
| 11 | 2 | -18 | 0 | yes |
| 12 | 4 | -33 | 0 | yes |
| 13 | 6 | -59 | 0 | yes |

The witnesses are returned by the integer solver and then rechecked with exact
integer matrix arithmetic. Their existence is therefore an exact positive
certificate; no claim of exact solver optimality or infeasibility is needed.

This extends the baseline-free finite evidence for the Bars III.B existence
claim through level 13. It does not prove saturation of the complete level-12
or level-13 packet semigroups, nor does it establish the result at arbitrary
level.

## 4. First HFT coefficient-two circuit

All coordinates in the first level-13 obstruction have $s=2$ and hence only
the first parent split. Write

$$
e_{\ell,m,r}=e_{([\ell,m,r,2],1)}.
$$

The following ten distinct Gale row types occur in the level-13 closure:

$$
g_1=-e_{0,0,0},
$$

$$
g_2=-e_{0,0,1}+e_{1,0,0},
$$

$$
g_3=-e_{0,1,0}+e_{0,2,0}-e_{1,0,0}+e_{1,2,0},
$$

$$
g_4=-e_{0,2,0}-e_{1,1,0}-e_{2,0,0},
$$

$$
g_5=-e_{1,0,1}+e_{2,0,0},
$$

$$
g_6=-e_{1,2,0},
$$

$$
g_7=-e_{2,0,0},
$$

$$
g_8=e_{1,0,1}+e_{1,1,0},
$$

$$
g_9=e_{0,1,0},
$$

$$
g_{10}=e_{0,0,0}+e_{0,0,1}+e_{1,0,1}.
$$

They obey the primitive positive relation

$$
g_1+g_2+g_3+g_4+2g_5+g_6+g_7+g_8+g_9+g_{10}=0.
$$

The ten supported rows have rank nine, so the relation is minimally
supported. Its coefficients have greatest common divisor one. This is an exact
positive circuit, not merely a nonminimal sum of zero-one circuits.

One realization uses the all-chiral parents

$$
(0,0,0,0,2),\ (1,1,0,0,0),\ (2,0,0,0,0),\ (3,0,0,0,0),
$$

$$
(2,1,0,0,0),\ (1,2,0,0,2),\ (2,0,0,0,2),\ (1,2,0,0,0),
$$

$$
(0,1,0,0,0),
$$

and the non-reference parent

$$
(0,1,0,1,1).
$$

The resulting facet inequality is weighted, with coefficient two on the
reference coordinate belonging to $(2,1,0,0,0)$.

## 5. Synthetic all-split obstruction

The failure is not tied to the HFT support. Synthetic finite boxes built
directly from the universal TK6B.3 relations give:

| Top-weight box | Kernel coordinates | Gale row types | Circuit types | Maximum coefficients |
| --- | ---: | ---: | ---: | --- |
| $\ell=m=r=0$, $2\leq s\leq4$ | 4 | 11 | 8 | all 1 |
| $\ell=m=r=0$, $2\leq s\leq6$ | 9 | 29 | 38 | all 1 |
| $0\leq\ell\leq1$, $m=r=0$, $2\leq s\leq5$ | 12 | 38 | 76 | all 1 |
| $0\leq\ell,m\leq1$, $r=0$, $2\leq s\leq3$ | 8 | 22 | 22 | all 1 |
| $0\leq\ell,m\leq1$, $r=0$, $2\leq s\leq4$ | 16 | 47 | 439 | 398 with maximum 1; 41 with maximum 2 |
| $0\leq\ell,r\leq1$, $m=0$, $2\leq s\leq4$ | 16 | 50 | 804 | 683 with maximum 1; 121 with maximum 2 |
| $0\leq m,r\leq1$, $\ell=0$, $2\leq s\leq4$ | 16 | 52 | 706 | 642 with maximum 1; 64 with maximum 2 |

Thus later splits can produce coefficient-two circuits in small mixed-label
systems, but later splits are not necessary: the actual HFT level-13
certificate uses only $k=1$. The obstruction comes from collision geometry,
not from a single isolated shell formula.

No computation here establishes that two is a universal coefficient bound.

## 6. Revised route to all orders

The local kernel relations are known for all labels and splits, and the finite
positive cone has a uniform exact description. The remaining all-orders work
is now narrower:

1. classify or recursively generate the primitive **weighted** circuits of
   the all-split collision hypergraph;
2. prove that the cumulative HFT triangular coordinates satisfy every
   weighted circuit inequality;
3. prove semigroup saturation in the relevant growing closures, or construct
   an integral packet witness directly at every level.

The finite computations suggest that the cumulative targets lie on many
facet walls, since the minimum slack is zero at each tested horizon. This is
an observation, not yet evidence for a specific recurrence or physical
mechanism.

## Reproduction

```text
./bin/sage-run -m trajectory_kernel.all_split_circuits --self-test
./bin/sage-run -m trajectory_kernel.all_split_circuits --max-ell 1 --max-m 1 --max-s 4 --verbose
./bin/sage-run -m trajectory_kernel.all_split_circuits --hft-level 11
./bin/sage-run -m trajectory_kernel.all_split_circuits --hft-level 12
./bin/sage-run -m trajectory_kernel.all_split_circuits --hft-level 13 --verbose
```

The HFT commands construct their targets and branching closures independently
and import no protected $SO(10)$ completion. Circuit and rank computations use
exact rational or integer arithmetic. Positive packet witnesses are rechecked
exactly after the solver returns them.
