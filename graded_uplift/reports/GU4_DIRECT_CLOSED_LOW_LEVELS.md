# GU4 — Direct closed low-level lift

**Status:** exact baseline-free calculation complete through level 3.

## Question

Let

$$
R_n^9=\sum_{\ell=1}^n r_\ell^9
$$

be the cumulative $SO(9)$ primary obtained from the HFT formula. The direct
closed target is

$$
T_n=R_n^9\otimes R_n^9.
$$

We ask for all $SO(10)$ characters $X_n$ satisfying:

1. $X_n$ has nonnegative integral irreducible coefficients;
2. $X_n$ is invariant under the $D_5$ outer automorphism
   $a_4\leftrightarrow a_5$;
3. $X_n\downarrow SO(9)=T_n$.

This directly lifts the closed primary target. It does not tensor the virtual
chiral HFT numerator uplifts used in TK4d, and it imports no protected
$SO(10)$ baseline.

## Exhaustive finite domain

For a $B_4$ top weight

$$
\mu=[b_1,b_2,b_3,s],
$$

all possible $D_5$ top parents are

$$
[b_1,b_2,b_3,k,s-k],\qquad 0\leq k\leq s.
$$

The calculation closes the target support under the branchings of every such
parent. Parents are grouped into outer-automorphism orbits. At each top
weight, triangularity forces the residual top multiplicity to be partitioned
among these orbits. This gives an exhaustive enumeration with exact finite
bounds; no coefficient cutoff is imposed.

The common level-1--3 closure has 14 $B_4$ rows.

## Result

| level | terms in $T_n$ | positive lifts without outer invariance | positive outer-invariant lifts |
|---:|---:|---:|---:|
| 1 | 1 | 1 | 1 |
| 2 | 4 | 1 | 1 |
| 3 | 14 | 27 | 1 |

Thus outer-chirality invariance first becomes selective at level 3 in this
test: it reduces 27 positive lifts to a unique one.

### Level 2

Here

$$
r_1^9=1,
$$

$$
r_2^9=9,
$$

and therefore

$$
T_2=(1+9)\otimes(1+9)=2(1)+2(9)+36+44.
$$

The unique positive lift is

$$
X_2=1+45+54=10\otimes10.
$$

Exact restriction uses

$$
10\downarrow SO(9)=9+1,
$$

$$
45\downarrow SO(9)=36+9,
$$

$$
54\downarrow SO(9)=44+9+1.
$$

### Level 3

Define the two conjugate chiral factors

$$
A_+=54+16_+,
$$

$$
A_-=54+16_-.
$$

The unique positive outer-invariant lift is

$$
X_3=A_+\otimes A_-.
$$

Its dimension is $70^2=4900$, equal to the dimension of $T_3$. This answer
was identified after exhaustive enumeration; it was not imported from the
protected Bars data.

## What happens to the Bars source labels

At fixed mass level $n$, retain

$$
\ell'=n-\ell.
$$

At level 2 the four source blocks are

| $(\ell'_L,\ell'_R)$ | $SO(9)$ block | positive outer-invariant lift of that block alone |
|---|---|---:|
| $(1,1)$ | $1$ | 1 |
| $(1,0)$ | $9$ | 0 |
| $(0,1)$ | $9$ | 0 |
| $(0,0)$ | $1+36+44$ | 0 |

In particular, a bare $9$ cannot lift positively by itself: its smallest top
parent is the $10$, whose restriction also contains a scalar. Positivity is
therefore a property of the combined cumulative target, not of each
$\ell'$-source block separately.

There is nevertheless a natural exact way to retain the source information.
For a $D_5\downarrow B_4$ branching component with orthogonal highest weights
$\lambda$ and $\mu$, define the interlacing depth

$$
d=\lambda_1-\mu_1.
$$

Then

$$
\operatorname{grRes}(10)=r_2^9+t r_1^9,
$$

and

$$
\operatorname{grRes}(A_\pm)=r_3^9+t r_2^9+t^2r_1^9.
$$

Consequently the factorized representatives $10\otimes10$ and
$A_+\otimes A_-$ recover every separate
$(\ell'_L,\ell'_R)$ block exactly by assigning $d_L=\ell'_L$ and
$d_R=\ell'_R$ before decomposing the diagonal $SO(10)$ tensor product.

This distinction matters. The $\ell'$ labels are compatible with a
factorwise branching filtration, but they are not separately preserved
positive $SO(10)$ sectors. Decomposing the product into diagonal $SO(10)$
irreducibles forgets the separate left/right filtration.

## Role of the closed universal factor

The intrinsic character

$$
Q_{\mathrm{cl}}=\bigoplus_{j=0}^{16}\Lambda^j16
$$

is positive, outer invariant, has dimension $65{,}536$, and obeys

$$
Q_{\mathrm{cl}}\downarrow SO(9)=(Z_Q^9)^2.
$$

For every positive outer-invariant primary lift $X_n$, the character

$$
Y_n=Q_{\mathrm{cl}}X_n
$$

is automatically positive, outer invariant, exactly divisible by
$Q_{\mathrm{cl}}$, and has the required full $SO(9)$ restriction.

Therefore $Q_{\mathrm{cl}}$ does not further select among primary lifts when
$Y_n$ is defined after $X_n$. Divisibility becomes a genuinely independent
test only when a closed numerator $Y_n$ has first been constructed by another
principle. TK4d showed that the raw products of the present virtual chiral
HFT numerator uplifts fail that independent test.

## Interpretation and boundary of the result

The calculation establishes:

- direct closed positivity and exact restriction at levels 1--3;
- uniqueness through level 3 after imposing outer invariance;
- a concrete and exact interlacing-depth realization of the Bars $\ell'$
  bookkeeping through level 3;
- the first explicit instance in which outer invariance removes substantial
  positive-kernel freedom.

It does not establish:

- an all-level direct closed construction;
- that interlacing depth will select the protected Bars representative at the
  first ambiguous chiral levels;
- an independently constructed closed numerator divisible by
  $Q_{\mathrm{cl}}$;
- uniqueness beyond the tested finite domain.

GU5 has now performed the next test. The unmodified interlacing-depth rule
first has no positive lift at level 5, and positivity plus closed outer
invariance is non-unique at level 6. Thus the GU4 depth pattern is an exact
low-level observation, not by itself an analytic selector. See
`GU5_LEVEL6_DIRECT_CLOSED_AND_DEPTH.md`.

## Reproduction

```text
./bin/sage-run -m graded_uplift.direct_closed_low_levels --self-test
./bin/sage-run -m graded_uplift.direct_closed_low_levels --max-level 3 --verbose
```
