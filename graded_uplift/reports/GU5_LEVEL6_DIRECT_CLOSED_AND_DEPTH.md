# GU5 — Level-6 direct closed lift and interlacing-depth audit

**Status:** exact baseline-free obstruction and nonuniqueness results complete;
protected comparison performed separately.

## Questions

GU4 suggested two possible low-level principles:

1. positivity, exact restriction and closed outer-chirality invariance might
   select a unique direct closed lift;
2. the Bars source label might equal the standard branching depth

$$
\ell'=\lambda_1-\mu_1.
$$

GU5 tests both statements at level 6. The second test was also run at every
lower level in order to locate its first failure.

## 1. Direct closed conditions are non-unique at level 6

Starting only from the HFT-derived cumulative target $R_6^9$, the fixed
all-chiral cross-section gives a positive exact $SO(10)$ lift $A$. It contains
the parent

$$
p=[3,0,0,0,1].
$$

Replace one copy by its outer conjugate

$$
\tau(p)=[3,0,0,1,0]
$$

to obtain another positive character $B$. Since conjugate $D_5$ parents have
identical $B_4$ restrictions,

$$
A\downarrow SO(9)=B\downarrow SO(9)=R_6^9.
$$

Equivalently,

$$
B-A=[3,0,0,1,0]-[3,0,0,0,1]
$$

lies in the restriction kernel.

Now form the closed characters

$$
X_A=A\tau(A),
$$

$$
X_B=B\tau(B).
$$

Both are positive and outer invariant, and both restrict exactly to

$$
R_6^9\otimes R_6^9.
$$

Nevertheless,

$$
X_A\neq X_B.
$$

Their difference is outer invariant, has dimension zero, restricts to zero,
and contains 92 nonzero irreducible terms with coefficients ranging from
$-8$ to $8$.

This is a baseline-free two-witness proof of nonuniqueness. It is not a count
of the complete level-6 closed fibre, which may be much larger.

Multiplication by $Q_{\mathrm{cl}}$ preserves both candidates and their
distinction, so the universal factor adds no selection power when applied
after the primary lift.

## 2. The unmodified interlacing-depth rule is obstructed

For each level $n$, define the refined $SO(9)$ target

$$
P_n(t)=\sum_{\ell=1}^n t^{n-\ell}r_\ell^9.
$$

The proposed refined lift requires a positive $SO(10)$ character whose
$D_5\downarrow B_4$ component of depth

$$
d=\lambda_1-\mu_1
$$

equals the coefficient of $t^d$ in $P_n(t)$.

The search uses the complete full-parent branching closure. At each top
weight, exact triangularity bounds every parent coefficient. Outer-conjugate
parents have identical refined columns, so their total multiplicities are
enumerated first and all chirality orientations are counted exactly. No
coefficient cutoff is used.

| level | refined target rows | unoriented fibres | positive oriented lifts |
|---:|---:|---:|---:|
| 1 | 1 | 1 | 1 |
| 2 | 2 | 1 | 1 |
| 3 | 4 | 1 | 2 |
| 4 | 8 | 1 | 2 |
| 5 | 17 | 0 | 0 |
| 6 | 31 | 0 | 0 |

Thus the simple rule works through level 4 but fails before the intended
level-6 selection problem.

At level 5 the exhaustive search has one terminal branch. Its common negative
residual is

$$
-t[0,0,0,1]_9.
$$

In plain terms, the forced positive parents produce one excess $SO(9)$ spinor
at depth 1, whereas the proposed target places that spinor at depth 0.

At level 6 every search branch has the common negative residual entries

$$
-t[1,0,0,0]_9,
$$

$$
-t[0,1,0,0]_9,
$$

$$
-t^2[0,0,0,1]_9.
$$

These are exact finite obstruction certificates for positive lifts within the
complete relevant parent domain.

## 3. Separate Bars/paper comparison

A protected comparison checks the known Bars character and the transcribed
paper candidate only after the baseline-free search is complete.

- Both obey the naive depth rule through level 4.
- Both first fail it at level 5 with the same residual.
- Their refined images remain identical at level 6 even though the underlying
  $SO(10)$ characters differ.
- Their common level-6 discrepancy from the proposed target is

$$
d=0:\quad-[0,0,0,1]_9-[1,0,0,0]_9-[0,1,0,0]_9,
$$

$$
d=1:\quad+[1,0,0,0]_9+[0,1,0,0]_9,
$$

$$
d=2:\quad+[0,0,0,1]_9.
$$

The Bars/paper difference consists of outer-chirality choices. Standard
interlacing depth is invariant under the $D_5$ outer automorphism, so it cannot
see, and therefore cannot select between, those choices.

## Conclusion

The level-2 and level-3 success does not extend into a level-6 selection
principle:

- closed outer invariance no longer gives uniqueness;
- the unmodified identification $\ell'=\lambda_1-\mu_1$ is already
  positively obstructed at level 5;
- the depth data are intrinsically blind to the chirality distinction that
  separates the Bars and paper representatives at level 6.

This does not make the direct closed programme a dead end. It shows that a
useful refinement must contain more information than ordinary interlacing
depth. A corrected filtration involving the additional IIA/M-theory label
$W$, or a rule coupling left and right data before diagonal $SO(10)$
decomposition, remains possible. That is a new hypothesis to formulate, not a
consequence of GU4.

## Reproduction

```text
./bin/sage-run -m graded_uplift.interlacing_depth_audit --self-test
./bin/sage-run -m graded_uplift.interlacing_depth_audit --max-level 6 --verbose
./bin/sage-run -m graded_uplift.direct_closed_level6 --self-test
./bin/sage-run -m graded_uplift.direct_closed_level6 --verbose
./bin/sage-run -m graded_uplift.verify_level6_depth_candidates --max-level 6 --verbose
```
