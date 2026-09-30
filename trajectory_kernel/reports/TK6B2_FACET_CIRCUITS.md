# TK6B.2 — Facets as Positive Kernel Circuits

**Status:** finite classification complete through the baseline-free level-11
closure; conditional all-level circuit template formulated

**Provenance:** baseline-free

**Last updated:** 25 September 2026

> **TK6B.3 update.** The $A/B/C$ row rule below is exact for arbitrary
> lengths of those three chains, but $A/B/C$ completeness fails in the actual
> baseline-free HFT closure at level 12, where two new kernel families enter.
> The proposed all-level statements 1 and 2 in Section 7 are therefore false
> as written. They are superseded by the universal all-split shell identities
> and collision-hypergraph formulation in `TK6B3_BOUNDARY_SHELL.md`.
> TK6B.4 subsequently refutes statement 3: eight primitive circuit types in
> the complete HFT level-13 closure have coefficient two. The exact
> replacement is the weighted criterion in `TK6B4_WEIGHTED_CIRCUITS.md`.

## Result

The 2,508 facets of the level-11 packet cone do not organize directly into a
small collection of translated $B_4$ multiplicity inequalities. Even after
quotienting by all common Dynkin-label translations, 2,444 distinct
weight-space templates remain. From level 10 to level 11, 2,399 new translated
templates appear and 527 disappear.

There is, however, a much smaller exact classification in the Gale transform
of the restriction-kernel lattice:

- the kernel rank is 11;
- the 84 packet columns give only 29 distinct Gale row types;
- those 29 types obey one explicit $A/B/C$ template;
- the 2,508 facets reduce to 40 positive-circuit types;
- every positive circuit has coefficient one;
- the multiplicities of those 40 types reproduce all 2,508 facets exactly.

Equivalently, after triangular all-chiral inversion, every complicated
weight-space facet becomes a zero-one subset-sum inequality. This is the first
exact Hall-type form found in the programme.

The finite circuit types have not stabilized with the HFT horizon, so this is
not an all-orders proof. The compact Gale **row** template is stable throughout
the tested nested closures and supplies a concrete conditional conjecture.

## 1. Failure of direct translation classification

The exact cones at nested horizons have the following sizes:

| Horizon | $B_4$ rows | Packets | Facets | Leading-shift templates | Full-translation templates |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 5 | 11 | 11 | 11 | 10 | 6 |
| 6 | 17 | 18 | 21 | 20 | 11 |
| 7 | 24 | 26 | 36 | 34 | 21 |
| 8 | 33 | 36 | 65 | 62 | 42 |
| 9 | 44 | 49 | 177 | 173 | 145 |
| 10 | 57 | 65 | 619 | 609 | 572 |
| 11 | 73 | 84 | 2,508 | 2,494 | 2,444 |

At horizon 11, only 63 facets can be shifted forward in the leading Dynkin
label while keeping their support inside the row domain. Only 14 of those 63
shifted functionals are again facets. They form eight nontrivial orbits, with
maximum length five. No eligible $m$-shifted facet survives, while four of five
eligible $s$-shifts survive. The $r$-domain is too narrow for a forward test.

Thus raw Dynkin translation is not the organizing principle for the dual
cone. This is consistent with the earlier discovery that corrected rather than
raw shifts organize the restriction kernel itself.

## 2. Gale transform of the packet system

Let

$$
A\in\mathbb Z^{d\times p}
$$

be the packet matrix and let

$$
K\in\mathbb Z^{p\times k}
$$

have as columns the natural integral restriction-kernel generators. Then

$$
AK=0,
$$

and the $p$ rows

$$
g_j\in\mathbb Z^k
$$

of $K$ are the Gale vectors of the packet rays.

If $y$ is a facet functional, its packet-slack vector is

$$
s=A^Ty.
$$

It obeys

$$
s\geq0,
$$

$$
K^Ts=0.
$$

Because $A$ has full row rank, $A^T$ is injective. Facets of the packet cone
therefore correspond exactly to extreme rays of

$$
\{s\geq0:K^Ts=0\}.
$$

These extreme rays are the positive circuits of the Gale vectors: minimally
supported positive relations among the $g_j$.

## 3. The compact $A/B/C$ Gale-row template

At horizon 11 the natural kernel coordinates are

$$
A_0,\ldots,A_5,
$$

$$
B_0,\ldots,B_2,
$$

$$
C_0,C_1.
$$

Write $e_G$ for the unit vector in the coordinate of generator $G$. The 29
distinct Gale row types are exactly

$$
0,
$$

$$
\pm e_G
\quad\text{for every available }G,
$$

$$
-e_{B_i}-e_{A_{i+1}}
\quad\text{for }0\leq i\leq2,
$$

$$
\sum_{i=0}^{5}e_{A_i},
$$

$$
\sum_{i=0}^{2}e_{B_i}-e_{A_0},
$$

$$
\sum_{i=0}^{1}e_{C_i}.
$$

There are no other Gale row types. The same schematic rule, truncated to the
kernel generators available at that horizon, is exact in every nested closure
through level 11, including the zero-kernel low-level domains.

This pattern has a direct relation to TK5b and TK6A:

- the signed unit vectors encode individual natural kernel pivots;
- the adjacent $-B_i-A_{i+1}$ rows link the $m$-transported $B$ family to the
  shifted $A$ family;
- the three sum rows are global boundary rows for the observed $A$, $B$ and
  $C$ chains.

That interpretation is suggestive, but the persistence of only these three
kernel families at arbitrary level has not been proved.

## 4. Forty circuit types generate all 2,508 facets

Every level-11 facet slack vector has entries only zero or one. Hence each
facet is indexed by a minimally zero-sum subset

$$
S\subseteq\{1,\ldots,84\}
$$

satisfying

$$
\sum_{j\in S}g_j=0.
$$

After forgetting which repeated packet realizes a given Gale row type, only 40
different circuit types remain. Their support sizes are distributed as follows:

| Circuit support | Number of circuit types | Number of actual facets |
| ---: | ---: | ---: |
| 1 | 1 | 30 |
| 2 | 11 | 52 |
| 3 | 4 | 21 |
| 4 | 0 | 0 |
| 5 | 1 | 16 |
| 6 | 3 | 48 |
| 7 | 5 | 201 |
| 8 | 7 | 556 |
| 9 | 6 | 864 |
| 10 | 2 | 720 |

The difference between 40 types and 2,508 facets comes entirely from choosing
among repeated packet columns with the same Gale row. There are 29 Gale row
types: one zero type, 22 signed-coordinate types and six composite types. Their
multiplicities are:

- six types occur once;
- eighteen types occur twice;
- four types occur three times;
- the zero type occurs thirty times.

For each circuit type, multiplying the relevant binomial choices of repeated
rows reproduces its observed facet multiplicity. Summing over the 40 types
gives exactly 2,508. This is an exact combinatorial reconstruction, not a
clustering heuristic.

## 5. Hall-type subset inequalities

Let $U$ be the square all-chiral packet submatrix. TK6B.1 proves

$$
\det U=1.
$$

For an integral $B_4$ target multiplicity vector $m$, define its triangular
section coordinates

$$
c=U^{-1}m.
$$

These coordinates need not be nonnegative. For a facet circuit $S$, restrict
its zero-one packet-slack vector to the reference columns of $U$. Then

$$
y^Tm
=
\sum_{j\in S\cap\operatorname{Ref}}c_j.
$$

Consequently the complete level-11 liftability test can be written as

$$
\sum_{j\in S\cap\operatorname{Ref}}c_j\geq0
$$

for every positive Gale circuit $S$.

All 2,508 resulting reference subsets are distinct and nonempty. Their sizes
range from 1 to 10. This is Hall-like in a precise sense: negative coefficients
created by the triangular section are permitted only when they can be covered
by the other section coefficients selected by every minimal kernel circuit.

Combined with TK6B.1 saturation, these rational subset inequalities are also
sufficient for an integral positive lift in the tested closure.

## 6. Nested-horizon behavior

The Gale compression is substantial but has not stabilized:

| Horizon | Distinct circuit types | Retained/lost/new from previous horizon |
| ---: | ---: | ---: |
| 5 | 1 | -- |
| 6 | 2 | 1 / 0 / 1 |
| 7 | 4 | 2 / 0 / 2 |
| 8 | 5 | 3 / 1 / 2 |
| 9 | 13 | 4 / 1 / 9 |
| 10 | 23 | 7 / 6 / 16 |
| 11 | 40 | 11 / 12 / 29 |

Thus it would be premature to claim that the 40 level-11 circuits form a
fixed all-level list. What is stable is the more compact rule for the Gale row
types. The changing positive circuits are generated combinatorially from that
small row system as new kernel coordinates and repeated packet realizations
enter.

## 7. Historical conditional all-level conjecture

The finite evidence motivates the following guarded conjectural mechanism:

1. the natural kernel continues to consist only of the three transported
   families $A_i$, $B_i$ and $C_i$;
2. its Gale rows continue to have exactly the truncated template in Section 3;
3. every positive Gale circuit continues to have unit coefficients;
4. the packet semigroup remains saturated;
5. the cumulative HFT section coordinates obey every circuit subset
   inequality.

Under these five statements, Bars III.B positivity would follow constructively
at every level. Statements 1--4 concern the branching/kernel system; statement
5 is the HFT multiplicity inequality.

The first three statements have exact finite evidence through level 11, and
TK6B.1 supplies the same finite evidence for statement 4. TK6B.3 subsequently
refuted statements 1 and 2 for the actual HFT closure at level 12: two new
kernel families enter and reorganize the row types. TK6B.4 refutes statement 3
at level 13 with exact coefficient-two circuits. The universal all-split
identities and their weighted circuit inequalities are the replacement
candidate. The level-11 circuit classification and subset inequalities remain
exact finite results.

## Reproduction

```text
./bin/sage-run -m trajectory_kernel.interlacing_facets --self-test
./bin/sage-run -m trajectory_kernel.interlacing_facets --max-level 11 --min-level 5
./bin/sage-run -m trajectory_kernel.interlacing_facets --max-level 11 --min-level 5 --verbose
```

The nested exact cone calculation takes several minutes. No protected
$SO(10)$ completion is imported.
