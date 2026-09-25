# TK4a — First Analytic Trajectory-Selection Experiment

**Status:** completed baseline-free experiment; simple extremal principles are
insufficient  
**Provenance:** baseline-free through HFT level 11  
**Last updated:** 23 September 2026

## Question

TK3 leaves 6,057 positive lifts at level 10. TK4a tests whether the exact TK2
corrected shift, supplemented only by a minimality principle, selects a
distinguished path through these positive fibres.

The experiment deliberately does not inspect the protected $SO(10)$
completion.

## 1. Coordinate transport

For each kernel family, the exact corrected shift sends

$$
K^F_\ell\longmapsto K^F_{\ell+1}.
$$

Hence a coordinate vector at level $n$ predicts the interior coordinates at
level $n+1$ by

$$
z^F_{\ell+1}(n+1)=z^F_\ell(n).
$$

The $\ell=0$ coordinate has no predecessor and is treated as new boundary
data. For a proposed transition the implementation measures:

- **interior defect:** the total absolute failure of the transported
  coordinates;
- **boundary injection:** the total new $\ell=0$ population;
- **population:** the total number of kernel generators used;
- **support:** the number of nonzero coordinates, used only as a final
  finite-window tie-break.

Three lexicographic priorities were tested:

1. transport first, then boundary injection, population and support;
2. boundary injection first, then transport, population and support;
3. total deviation (transport plus boundary), then population, support and
   transport.

These are intrinsic to the baseline-free trajectory construction, but none is
asserted in advance to be physically preferred.

## 2. Local extremality does not select a lift

At level 10 the positive fibre has 6,057 points. Simple level-local criteria
leave substantial ambiguity:

| Criterion | Minimum | Number of minimizers |
| --- | ---: | ---: |
| Total kernel population | 11 | 94 |
| Number of occupied coordinates | 3 | 2 |
| Boundary population | 1 | 58 |

Thus neither sparsity nor minimal correction size supplies a unique answer.

## 3. Global paths through level 10

Exact dynamic programming over all positive fibres gives:

| Priority | Optimal cost | Optimal final states | Optimal paths |
| --- | --- | ---: | ---: |
| Transport first | $(3,9,19,11)$ | 6 | 8 |
| Boundary first | $(2,9,18,8)$ | 3 | 3 |
| Total deviation | $(11,18,8,6)$ | 1 | 1 |

All selected prefixes are themselves optimal at every shorter cutoff. This is
a useful consistency property: none of the rules needs future level-10 data to
revise an earlier optimum.

However, the three rules select different final coordinates. The apparent
uniqueness of the total-deviation path therefore comes from its chosen ordering
of reasonable costs, not from a rule forced by the representation theory.

For example, the transport-first representative evolves as

| Level | Nonzero coordinates |
| ---: | --- |
| 7 | $A_0=1$ |
| 8 | $A_1=1$, $A_0=1$ |
| 9 | $A_2=1$, $A_1=2$, $A_0=1$ |
| 10 | $A_3=1$, $A_2=2$, $B_0=2$, $A_1=3$, $A_0=4$ |

This is orderly, but seven other paths have exactly the same transport-first
cost.

## 4. Baseline-free level-11 holdout

The HFT calculation was extended to level 11 before any baseline comparison.
The finite closure becomes:

| Object | Level 10 | Level 11 |
| --- | ---: | ---: |
| $B_4$ row weights | 57 | 73 |
| $D_5$ parent columns | 65 | 84 |
| Kernel generators | 8 | 11 |

The new generators are exactly

$$
A_5,\qquad B_2,\qquad C_1.
$$

No new fixed-tail seed family appears. This is positive evidence, through one
additional level, for the finite-seed trajectory organization.

The full level-11 positive fibre is too large to be useful to materialize.
Instead, a full-horizon mixed-integer calculation optimizes directly over all
positive integral lifts at levels 1--11. There is no coordinate cutoff.

| Priority | Level-10 primary optimum | Level-11 primary optimum | Prefix remains level-10 optimal? |
| --- | --- | --- | --- |
| Transport first | $(3,9,19)$ | $(4,21,44)$ | Yes |
| Boundary first | $(2,9,18)$ | $(4,16,38)$ | Yes |
| Total deviation | $(11,18,4)$ | $(20,38,10)$ | Yes |

Level 11 does not break the degeneracy. For example, under transport-first
optimization the following final coordinates remain variable while all three
primary optima are fixed:

$$
0\leq A_5\leq1,
$$

$$
1\leq A_4\leq2,
$$

$$
1\leq A_3\leq5,
$$

$$
1\leq A_2\leq4,
$$

$$
4\leq A_1\leq5.
$$

The other two priorities also retain nontrivial optimal ranges, and the three
priorities again choose different representatives.

## 5. Conclusion

The experiment separates two statements:

1. The corrected shift is a real and useful organizational structure. It is
   cutoff-stable in all three tests, and level 11 adds only shifted members of
   the existing seed families.
2. Minimal corrected-shift transport is not, by itself, the missing analytic
   selection principle. Reasonable intrinsic orderings disagree, and their
   optima remain non-unique at the level-11 holdout.

It would be artificial to declare one lexicographic ordering canonical merely
because it returns a single level-10 path.

The next refinement should act on the **kernel-valued generating function as a
whole**, not on norms of its finite coefficient vectors. Promising conditions
include rationality with a small denominator, finite boundary-source series,
or compatibility with the HFT numerator before the problematic $Z_Q$
division. Such a condition could distinguish algebraic complexity rather than
an arbitrary notion of coordinate size.

## Reproduction

```text
./bin/sage-run -m trajectory_kernel.trajectory_selection --self-test
./bin/sage-run -m trajectory_kernel.trajectory_selection --max-level 10 --verbose
./bin/sage-run -m trajectory_kernel.trajectory_selection --max-level 11 --probe-next-level
```

The level-11 command uses full-horizon integer optimization and verifies that
each returned positive character restricts to its HFT target.
