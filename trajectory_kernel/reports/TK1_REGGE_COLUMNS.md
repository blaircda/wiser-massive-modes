# TK1 — Baseline-Free Regge-Column Extraction

**Status:** complete for the finite window $1\leq n\leq 10$  
**Last updated:** 23 September 2026

## Question and provenance

TK1 asks how the irreducible $SO(9)$ multiplicities in the HFT-derived
massive characters behave under the Regge shift

$$
(n,\ell,m,r,s)\longmapsto(n+1,\ell+1,m,r,s).
$$

The computation in `trajectory_kernel/regge_columns.py` derives every
$r_n^9$ directly from `hft_so9.py`. It does not import the protected $SO(10)$
completion. Thus the statements below concern the analytic HFT $SO(9)$
spectrum, not a pattern seeded from the known lift.

## Coordinates

For a $B_4$ highest weight $[\ell,m,r,s]_9$, a **Regge column** means fixed
$(m,r,s)$. Within a column, an individual shift orbit is specified by the
reduced depth

$$
\delta=n-\ell-3m.
$$

This is invariant under the Regge shift and is the reduced-level coordinate
already natural in the HFT support. At fixed $(\delta,m,r,s)$ the tested
multiplicity sequence is

$$
a_{\delta;m,r,s}(n)
=\operatorname{mult}_{r_n^9}
[n-3m-\delta,m,r,s]_9,
$$

whenever the first Dynkin label is nonnegative. Missing representations are
included with multiplicity zero.

## Finite-window results

Through level 10 the calculation finds:

| Quantity | Count |
| --- | ---: |
| Nonzero $SO(9)$ irreducible entries | 185 |
| Fixed-$(m,r,s)$ columns | 13 |
| Observed $(\delta,m,r,s)$ orbits | 56 |
| Adjacent shift comparisons, including implicit zeros | 134 |
| Exact adjacent matches | 80 |
| Adjacent mismatches | 54 |
| Nonzero $\ell=0$ boundary seeds | 50 |
| Orbits with an observed constant suffix of length at least 2 | 24 |
| Constant suffixes of length at least 3 | 19 |
| Orbits unresolved in the window | 32 |
| Unresolved orbits represented by only one available point | 13 |

The 13 Regge columns actually encountered are:

| $(m,r,s)$ | Levels present | Nonzero entries |
| --- | --- | ---: |
| $(0,0,0)$ | 1--10 | 42 |
| $(0,0,1)$ | 3--10 | 35 |
| $(0,0,2)$ | 6--10 | 15 |
| $(0,0,3)$ | 10 | 1 |
| $(0,1,0)$ | 5--10 | 20 |
| $(0,1,1)$ | 8--10 | 6 |
| $(1,0,0)$ | 4--10 | 28 |
| $(1,0,1)$ | 6--10 | 15 |
| $(1,0,2)$ | 9--10 | 3 |
| $(1,1,0)$ | 8--10 | 6 |
| $(2,0,0)$ | 7--10 | 10 |
| $(2,0,1)$ | 9--10 | 3 |
| $(3,0,0)$ | 10 | 1 |

The adjacent mismatches are distributed by transition as follows:

| Transition | Mismatches |
| --- | ---: |
| $3\to4$ | 1 |
| $4\to5$ | 1 |
| $5\to6$ | 4 |
| $6\to7$ | 6 |
| $7\to8$ | 10 |
| $8\to9$ | 13 |
| $9\to10$ | 19 |

There are no mismatches at $1\to2$ or $2\to3$. The growth thereafter is a
direct obstruction to treating Regge shift invariance as a universal identity
of all HFT multiplicities.

## Observed stable sector

The finite constant-suffix test finds the following 24 candidate stable
orbits. “Start” is the first level of the constant suffix and “run” is the
number of observed equal terms through level 10.

| $\delta$ | $(m,r,s)$ | Start | Value | Run |
| ---: | --- | ---: | ---: | ---: |
| 1 | $(0,0,0)$ | 1 | 1 | 10 |
| 1 | $(1,0,0)$ | 4 | 1 | 7 |
| 1 | $(2,0,0)$ | 7 | 1 | 4 |
| 2 | $(1,0,0)$ | 6 | 2 | 5 |
| 2 | $(2,0,0)$ | 9 | 2 | 2 |
| 3 | $(0,0,0)$ | 4 | 1 | 7 |
| 3 | $(0,0,1)$ | 3 | 1 | 8 |
| 3 | $(1,0,0)$ | 8 | 3 | 3 |
| 3 | $(1,0,1)$ | 6 | 1 | 5 |
| 3 | $(2,0,1)$ | 9 | 1 | 2 |
| 4 | $(0,0,0)$ | 6 | 1 | 5 |
| 4 | $(0,0,1)$ | 5 | 1 | 6 |
| 4 | $(1,0,1)$ | 8 | 3 | 3 |
| 5 | $(0,0,0)$ | 8 | 4 | 3 |
| 5 | $(0,0,1)$ | 7 | 3 | 4 |
| 5 | $(0,1,0)$ | 5 | 1 | 6 |
| 5 | $(1,1,0)$ | 8 | 1 | 3 |
| 6 | $(0,0,1)$ | 9 | 6 | 2 |
| 6 | $(0,0,2)$ | 6 | 1 | 5 |
| 6 | $(0,1,0)$ | 7 | 1 | 4 |
| 6 | $(1,0,2)$ | 9 | 1 | 2 |
| 7 | $(0,0,2)$ | 8 | 2 | 3 |
| 7 | $(0,1,0)$ | 9 | 5 | 2 |
| 8 | $(0,1,1)$ | 8 | 1 | 3 |

Fifteen of these suffixes are constant from their first nonzero observation;
nine stabilize only after earlier variation. Five of all 56 observed orbits
activate after an initial kinematically allowed zero.

Representative sequences make the distinction clear:

$$
a_{1;0,0,0}(n)=1,1,1,1,1,1,1,1,1,1,
$$

$$
a_{3;0,0,0}(n)=0,1,1,1,1,1,1,1,
$$

$$
a_{5;0,0,0}(n)=1,2,3,4,4,4,
$$

whereas the deeper scalar orbit

$$
a_{7;0,0,0}(n)=2,5,9,11
$$

has not stabilized in the available window.

## Interpretation and limits

TK1 establishes a useful Regge-orbit data layer, but it does **not** establish
a global shift law. In particular:

- 54 of 134 nontrivial adjacent comparisons fail;
- the stable suffixes are detected retrospectively at the right edge of a
  finite window, so even a long suffix is evidence rather than an all-orders
  theorem;
- five suffixes contain only two equal terms and are especially weak evidence;
- 19 unresolved orbits have more than one observed point and genuinely vary;
- the 13 one-point orbits cannot yet be classified.

Accordingly, TK2 should not impose multiplicity shift invariance on the whole
spectrum. It should instead test exact shift covariance of the
$D_5\downarrow B_4$ branching columns and restriction-kernel relations, and
then ask whether a trajectory-adapted correction rule has a stable interior
plus explicitly generated boundary data.

## Reproduction

```text
./bin/sage-run -m trajectory_kernel.regge_columns --self-test
./bin/sage-run -m trajectory_kernel.regge_columns --max-level 10
./bin/sage-run -m trajectory_kernel.regge_columns --max-level 10 --verbose
```

The non-verbose command prints aggregate diagnostics. The verbose command
prints every mismatch, boundary seed and orbit sequence.
