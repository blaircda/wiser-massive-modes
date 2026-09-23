# Finite $D_5\downarrow B_4$ Cross-Section Report

**Date:** 23 September 2026  
**Status:** Implemented and exhaustively tested through level 10  
**Supersedes:** the claim in `Candidate_Set_Branching_Analysis.md` that the
level-dependent 126/210 prescription is a single canonical cross-section.

## Result

An explicit finite cross-section construction has now been implemented without
using the protected $SO(10)$ baseline. It proves that restriction can be
inverted exactly and integrally on either of two natural, level-independent
sections. However, neither section preserves positivity through level 10.

More strongly, an exhaustive search over all inequivalent choices of one
irreducible $D_5$ top parent for every relevant $B_4$ highest weight finds no
single level-independent section whose lifts of all cumulative spectra
$R_1^9,\ldots,R_{10}^9$ are positive.

This is a no-go result for the tested **irreducible-parent cross-section
ansatz**. It is not a no-go theorem for more general additive sections involving
kernel combinations, nor for the existence of the positive Bars lifts.

## 1. Explicit candidate family

For a $B_4$ highest weight

$$
\mu=[\ell,m,r,s],
$$

the top $B_4$ component of a dominant $D_5$ weight
$[a_1,a_2,a_3,a_4,a_5]$ is

$$
[a_1,a_2,a_3,a_4+a_5].
$$

All dominant $D_5$ parents with top component $\mu$ are therefore

$$
[\ell,m,r,k,s-k],\qquad 0\leq k\leq s.
$$

The outer automorphism exchanges $k$ and $s-k$ and leaves the $B_4$
restriction unchanged. The implementation fixes the positive-chirality
orientation $a_5\geq a_4$, leaving the complete inequivalent family

$$
0\leq k\leq \left\lfloor\frac{s}{2}\right\rfloor.
$$

Selecting one member of this family for every $\mu$ gives the class of
irreducible-parent cross-sections tested here.

## 2. Finite triangular inversion

At each level, the initial finite set is the support of the independently
derived cumulative HFT $SO(9)$ character. It is enlarged until it is closed
under the restriction of every selected parent. This avoids assuming the
unproved oscillator-energy cutoff stated in the earlier report.

The closed weights are ordered by decreasing orthogonal coordinates. Every
selected parent restricts to its chosen top weight with multiplicity one and to
strictly lower weights otherwise. The finite branching matrix is consequently
unipotent triangular, so back-substitution gives a unique integral lift on the
chosen section. The scripts check explicitly that:

- the selected parent has the declared top weight;
- the diagonal branching coefficient is one;
- every other component is lower in the ordering;
- the final residual is zero;
- restricting the constructed lift returns the input character exactly.

These structural checks pass at every level 1--10.

## 3. Two natural global policies

The implementation first tests two level-independent rules.

1. **All-chiral policy**

   $$
   [\ell,m,r,s]_9\longmapsto[\ell,m,r,0,s]_{10}.
   $$

   The cumulative lifts are positive through level 6. They become virtual at
   levels 7--10.

2. **Fermion-chiral, tensor-balanced policy**

   For odd $s$, select $[\ell,m,r,0,s]$. For even $s$, select
   $[\ell,m,r,s/2,s/2]$. The cumulative lift first becomes virtual at level 6;
   level 7 happens to be positive, but levels 8--10 are again virtual.

Thus exact integral inversion is robust, while positivity depends on the
section and is not preserved by either natural global convention.

## 4. Exhaustive finite search

Through level 10 the full branching closure contains 57 $B_4$ top weights.
Only eight have more than one inequivalent parent, and each has exactly two.
The search therefore tests all

$$
2^8=256
$$

global selections.

No selection is positive at every level 1--10. The obstruction is already
forced by the treatment of $[0,0,0,2]_9$:

- If $[0,0,0,2]_9$ is represented by the chiral 5-form
  $[0,0,0,0,2]_{10}$, every one of the 128 remaining selections first fails at
  level 7. The coefficient of $[0,1,0,0,0]_{10}$ is unavoidably $-1$.
- If it is represented by the 4-form $[0,0,0,1,1]_{10}$, every one of the 128
  remaining selections first fails at level 6. The coefficient of
  $[0,0,1,0,0]_{10}$ is unavoidably $-1$.

This explains why the old level-dependent rule switched from the 126 to the
210: the switch avoids each local obstruction separately. But a rule that
changes with the target level is not one fixed cross-section of the
representation rings and cannot supply the desired analytic lift by itself.

Testing each cumulative level separately gives the following number of positive
selections out of 256:

| Level | Positive irreducible-parent selections |
| ---: | ---: |
| 1--5 | 256 at each level |
| 6 | 128 |
| 7 | 128 |
| 8 | 64 |
| 9 | 16 |
| 10 | 0 |

Thus levels 8 and 9 still possess positive lifts inside this ansatz when treated
individually, although the admissible choices become progressively more
restricted. At level 10, no irreducible-parent cross-section is positive even
for $R_{10}^9$ alone. Its known positive Bars lift necessarily lies outside this
ansatz.

## 5. Comparison with the protected baseline

The comparison is performed only in the separate verification script.

- The all-chiral lift agrees exactly with the protected completion at levels
  1--6, then differs from it by nonzero restriction-kernel elements at levels
  7--10.
- The tensor-balanced lift agrees exactly at levels 1--5, then differs by
  restriction-kernel elements at levels 6--10.
- Every difference checked has zero dimension and restricts identically to zero
  in $SO(9)$.

The protected completion remains positive at all ten levels. Its later spectra
can contain more than one $D_5$ representation with the same $B_4$ top weight,
so it is not constrained to lie in an irreducible-parent cross-section.

## 6. Implication for the analytic programme

The finite cross-section has achieved its diagnostic purpose. It separates two
facts that had previously been conflated:

1. A level-independent section gives a rigorous, exact and integral inverse to
   restriction on the finite support.
2. Positivity of that inverse is an additional property, and it fails for every
   irreducible-parent section through level 10.

Accordingly, the next analytic step should not attempt to prove positivity for
this ansatz. It should enlarge the lift by controlled elements of
$\ker(\operatorname{Res})$, or formulate a more general additive section whose
images may contain several $D_5$ irreducibles with the same top weight. The
level-6/7 obstruction gives a concrete minimal test that any such construction
must resolve.

## Reproduction

```text
./bin/sage-run finite_cross_section.py --max-level 10 --policy chiral
./bin/sage-run finite_cross_section.py --max-level 10 --policy fermion-chiral-tensor-balanced
./bin/sage-run search_finite_cross_sections.py --max-level 10
./bin/sage-run verify_finite_cross_section_against_baseline.py --max-level 10
```
