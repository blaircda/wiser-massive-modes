# TK5c — Minimal Core-Supported Witnesses

**Status:** complete through HFT level 11  
**Last updated:** 24 September 2026  
**Provenance:** baseline-free

## 1. Question

TK5b proved that at least one positive cumulative $SO(10)$ lift through level
11 has kernel-coordinate sources only at GMSZ residual-core positions. Its
displayed witness was selected only for feasibility.

TK5c asks three stronger finite-window questions:

1. How sparse can a core-supported witness be?
2. Is the resulting minimum unique?
3. Can one witness remain minimal as the level cutoff is increased?

The implementation is `trajectory_kernel/chamber_witness.py`. It imports no
protected $SO(10)$ completion.

## 2. Exact optimization criterion

For every allowed source site $(F,\ell,n)$, write the integral source as

$$
s_{F,\ell}(n)=s^+_{F,\ell}(n)-s^-_{F,\ell}(n),
$$

where $s^+$ and $s^-$ are nonnegative integers. A binary variable records
whether the site is active. TK5c optimizes lexicographically:

1. the number of active source sites;
2. the total absolute source charge

$$
\sum_{F,\ell,n}\left(s^+_{F,\ell}(n)+s^-_{F,\ell}(n)\right);
$$

3. the total kernel-coordinate population, used only to print one convenient
representative after the first two minima have been fixed.

The third objective is not part of the definition of a minimal witness and
has no proposed physical significance.

The binary formulation does not use an arbitrary numerical cutoff. A kernel
coordinate is the coefficient of its generator's alternative $D_5$ parent in
the final positive lift. Since that parent's restriction contains the
generator's top $B_4$ weight, the coordinate is bounded above by the exact
cumulative multiplicity of that $B_4$ weight. These bounds give rigorous
finite source bounds.

Distinct minimal source vectors were enumerated with exact exclusion cuts.
The cap was 20; every tested optimal face was exhausted below the cap.

## 3. Minimality and non-uniqueness

The exact results are:

| Horizon | Minimum source events | Minimum absolute charge | Number of minimal witnesses |
| ---: | ---: | ---: | ---: |
| 7 | 1 | 1 | 1 |
| 8 | 2 | 2 | 2 |
| 9 | 3 | 4 | 2 |
| 10 | 5 | 11 | 3 |
| 11 | 7 | 20 | 6 |

Thus the level-7 minimum is unique, but non-uniqueness begins already at level
8 and persists. At level 11 the ambiguity is finite and modest under this
particular criterion: there are exactly six minimal source vectors, rather
than a unique vector or an unbounded family.

One population-minimal representative at each horizon adds the following new
source data:

| Horizon | Nonzero sources in one representative |
| ---: | --- |
| 7 | $s_{A_0}(7)=1$ |
| 8 | previous entry and $s_{A_0}(8)=1$ |
| 9 | $s_{A_0}(7)=1$, $s_{A_0}(8)=1$, $s_{A_1}(9)=2$ |
| 10 | $s_{A_0}(7)=1$, $s_{A_0}(8)=1$, $s_{A_1}(9)=3$, $s_{B_0}(10)=1$, $s_{A_1}(10)=5$ |
| 11 | $s_{A_0}(7)=1$, $s_{A_0}(8)=1$, $s_{A_1}(9)=3$, $s_{B_0}(10)=2$, $s_{A_1}(10)=5$, $s_{A_1}(11)=6$, $s_{A_0}(11)=2$ |

Every resulting $D_5$ coefficient is nonnegative and every restriction is
exactly the intended cumulative HFT $B_4$ character.

These representatives should not be read as successive prefixes of one
rule. They were optimized independently, and the incompatibility below shows
that no sequence can realize all of the displayed horizon minima at once.

## 4. Cutoff instability

The optimal faces at horizons 7 and 8 have a common path, as do the optimal
faces at horizons 8 and 9. The next two transitions fail:

| Adjacent horizons | Compatible minimal faces? |
| --- | --- |
| $7\to8$ | yes |
| $8\to9$ | yes |
| $9\to10$ | no |
| $10\to11$ | no |

The failure lies in the secondary charge objective, not in the number of
events. Among the three horizon-10 minima, their prefixes through level 9
have event/charge profiles

$$
(3,5)\quad\text{or}\quad(3,6),
$$

whereas the independent horizon-9 minimum is $(3,4)$. Similarly, the six
horizon-11 minima have prefixes through level 10 with profiles

$$
(5,12)\quad\text{or}\quad(5,13),
$$

whereas the independent horizon-10 minimum is $(5,11)$.

Consequently there is no core-supported witness that is lexicographically
minimal at every cutoff from 7 through 11. A locally charge-minimal prefix
must be abandoned to obtain the later global minimum.

## 5. Interpretation

TK5c improves the TK5b existence statement but does not reveal an analytic
selection rule.

- Sparsity substantially reduces the TK5b feasibility witness: at level 11
  the minimum has 7 source events and charge 20, compared with 11 events and
  charge 22 in the unoptimized witness.
- The minimum remains non-unique: exactly six source vectors survive at level
  11.
- More importantly, the secondary minimum is not cutoff-stable beginning at
  $9\to10$. Thus “use as few and as small core sources as possible” is not a
  recursive rule whose earlier decisions can be retained.

This supports caution about extracting a canonical uplift from ungraded
kernel minimality alone. It does not prove that no organizing principle
exists. The finite kernel generators still have the exact two-seed transport
structure found in TK5b, and an additional grading or a different analytic
constraint could distinguish one of the feasible paths.

The most natural separate test is now the oscillator-number grading retained
in hep-th/0310292. It should be treated as new input to a graded uplift problem,
not as a reinterpretation of the failed ungraded minimality criterion.

## 6. Reproduction

```text
./bin/sage-run -m trajectory_kernel.chamber_witness --self-test
./bin/sage-run -m trajectory_kernel.chamber_witness --max-level 11 --enumeration-cap 20 --verbose
```

The full run derives the HFT data, constructs the finite branching domain,
solves the integer optimization at every cutoff and enumerates the minimal
source vectors. No protected baseline file is imported.
