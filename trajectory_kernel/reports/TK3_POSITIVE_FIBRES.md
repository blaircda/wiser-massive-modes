# TK3 — Positive Lift Fibres in Trajectory-Kernel Coordinates

**Status:** complete on the baseline-free HFT level-1--10 finite domain  
**Provenance:** baseline-free  
**Last updated:** 23 September 2026

## Result

Every cumulative HFT $SO(9)$ character $R_n^9$, for $1\leq n\leq10$, has at
least one positive integral $SO(10)$ lift inside the 65-column parent domain
constructed in TK2. No additional kernel seed or larger parent domain is
forced by positivity through level 10.

The positive lift is unique through level 6, but it ceases to be unique from
level 7 onward. The number of positive lifts grows to 6,057 at level 10.
Thus positivity resolves the failure of the one-parent cross-section ansatz,
but positivity alone does not select a canonical $SO(10)$ completion.

No protected $SO(10)$ data is imported or used to choose any solution.

## 1. Complete finite parameterization

Let $s_{\mathrm{ch}}$ be the all-chiral triangular section and let the eight
TK2 kernel generators be grouped as follows:

- $K^A_\ell$ lies over $[\ell,0,0,2]_9$, for $0\leq\ell\leq4$;
- $K^B_\ell$ lies over $[\ell,1,0,2]_9$, for $0\leq\ell\leq1$;
- $K^C_0$ lies over $[0,0,0,3]_9$.

Every integral lift inside the finite parent domain has a unique expression

$$
L_n=s_{\mathrm{ch}}(R_n^9)
+\sum_{\ell=0}^4 x_\ell K^A_\ell
+\sum_{\ell=0}^1 y_\ell K^B_\ell
+wK^C_0,
$$

with integer coordinates. This is complete because the TK2 restriction
matrix has kernel rank eight and these eight generators form an integral
basis.

For each generator, its non-reference parent has coefficient equal to its
coordinate, while its reference top parent has coefficient equal to the
currently available multiplicity minus that coordinate. Ordering the
generators by decreasing top weight therefore gives exact finite bounds

$$
0\leq z_i\leq c_i^{\mathrm{available}}.
$$

The enumeration uses these derived bounds. It has no artificial search cutoff.

## 2. Positive-fibre counts

| Level | Negative terms in the all-chiral lift | Minimum coefficient | Positive lifts |
| ---: | ---: | ---: | ---: |
| 1 | 0 | 0 | 1 |
| 2 | 0 | 0 | 1 |
| 3 | 0 | 0 | 1 |
| 4 | 0 | 0 | 1 |
| 5 | 0 | 0 | 1 |
| 6 | 0 | 0 | 1 |
| 7 | 2 | $-1$ | 2 |
| 8 | 1 | $-2$ | 8 |
| 9 | 1 | $-4$ | 72 |
| 10 | 2 | $-10$ | 6,057 |

The result sharpens the earlier cross-section obstruction. No choice of one
irreducible parent for every top weight works at level 10, but allowing an
integral distribution between parents along the TK2 kernel directions produces
many positive lifts.

## 3. Activation of the trajectory coordinates

The exact coordinate ranges on each positive fibre are:

| Level | Nonzero-capable coordinates |
| ---: | --- |
| 1--6 | all coordinates forced to zero |
| 7 | $0\leq x_1\leq1$, $x_0=1$ |
| 8 | $0\leq x_2\leq1$, $0\leq x_1\leq2$, $0\leq x_0\leq1$ |
| 9 | $0\leq x_3\leq1$, $0\leq x_2\leq2$, $0\leq y_0\leq1$, $0\leq x_1\leq4$, $0\leq x_0\leq1$ |
| 10 | $0\leq x_4\leq1$, $0\leq x_3\leq2$, $0\leq y_1\leq1$, $0\leq x_2\leq5$, $1\leq y_0\leq3$, $0\leq x_1\leq5$, $0\leq w\leq2$, $0\leq x_0\leq4$ |

These are marginal ranges; the coordinates are correlated by the positivity
inequalities and not every tuple in the Cartesian product is allowed.

At level 7 the two solutions are

$$
x_0=1,
$$

and

$$
x_0=x_1=1.
$$

Thus the first compulsory correction is precisely the $K^A_0$ seed containing
the 126/210 relation found in TK2. The next member of the same corrected-shift
trajectory is optional at that level.

## 4. Structure of the level-10 cone

Two especially informative level-10 inequalities are the scalar constraint

$$
-10+x_0+x_1+x_2+x_3+x_4\geq0,
$$

and the family-B boundary constraint

$$
-1+y_0\geq0.
$$

The first says that the all-chiral scalar deficit of ten must be repaired by a
total of at least ten corrections distributed along the five-member family-A
trajectory. The second forces the family-B seed $K^B_0$ to occur at least
once. Together with the remaining upper and mixed bounds, the exact integer
polytope contains 6,057 points.

The family-C coordinate is optional, with $0\leq w\leq2$. Hence the new
$\delta=10$ seed is available but is not required merely to obtain positivity
at level 10.

## 5. Optional nonnegative-increment test

As an additional diagnostic, the implementation asks whether the positive
cumulative lifts can be chosen so that

$$
L_n-L_{n-1}
$$

is also a positive $SO(10)$ character at every step. This stronger condition
already fails at $1\to2$: the unique lifts differ by a coefficient $-1$ on the
trivial representation.

This is **not** an obstruction to TK3. The project only requires each
cumulative $R_n^{10}$ to be positive; choosing an $SO(10)$ lift need not
commute with taking consecutive differences. The earlier negative-tail audit
likewise found virtual consecutive $SO(10)$ differences. The test is retained
to prevent the stronger, false property from being assumed later.

## 6. Interpretation and limitations

TK3 establishes three points:

1. The three TK2 trajectory families suffice for positive lifts throughout
   the tested finite window.
2. The first necessary correction is the 126/210 kernel seed at level 7.
3. Positivity rapidly becomes highly non-unique and therefore cannot by itself
   be the hidden selection principle.

The count 6,057 is exact for the 65-column, fixed-positive-chirality domain. It
is not a count of every possible formulation using outer-conjugate labels, nor
an all-orders statement. New HFT weights at higher levels can introduce new
parent ambiguities and new kernel-seed families.

The appropriate next question is to find an analytic principle that selects a
trajectory-compatible point, or a much smaller distinguished subfamily, in
these positive fibres without consulting the protected completion.

## Reproduction

```text
./bin/sage-run -m trajectory_kernel.correction_ansatz --self-test
./bin/sage-run -m trajectory_kernel.correction_ansatz --max-level 10
./bin/sage-run -m trajectory_kernel.correction_ansatz --max-level 10 --verbose
```

The verbose command prints representative coordinate tuples and all
nonconstant level-10 positivity inequalities. A fresh full run takes roughly
one to two minutes because it reconstructs the finite branching domain.
