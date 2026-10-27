# TK6B.6a--g — Scalar Tail and Gamma-Trace Transfer

**Status:** exact all-orders reduction and gamma-traceless polynomial free
resolution and explicit gamma-trace transfer formula obtained; scalar positivity is now a specific
$B_\Gamma$--$H_4$ prefix dominance in the original `B4` HFT series; the
canonical cumulative `B4` Koszul core is positive through degree 20, but its
all-orders positivity, the physical realization of the full spinor-form
triangle, and the resulting homology concentration remain open

**Provenance:** baseline-free; no protected `SO(10)` completion is imported

**Last updated:** 13 October 2026

## 1. Where this fits

Write the HFT massive-primary series as

$$
Z_m(q)=\operatorname{PE}(qV_9)F(q).
$$

The cumulative Bars target is lifted virtually by

$$
X^{(0)}(q)=\operatorname{PE}(qV_{10})S(F(q)),
$$

where $S$ is the fixed all-chiral triangular section.  After the isolated
degree-three chirality repair, the proposed positive lift is

$$
X(q)=\operatorname{PE}(qV_{10})
\left(S(F(q))-q^3J+A(q)A_0\right).
$$

Here

$$
J=16_+-16_-,
$$

and

$$
A_0=16_-J=210-126_- -120+45-10+1.
$$

The scalar coefficient fixes $A(q)$ uniquely once the correction is required
to start at degree nine.  The purpose of this note is to pull that scalar
condition completely through the Green--Schwarz telescope.

## 2. From the scalar convolution to a prefix sum

Let $C(q)$ be the diagonal series of one-row coefficients in $S(F)$:

$$
C(q)=\sum_{d,\ell\geq0}
 [\ell,0,0,0,0]S(F_d)\,q^{d+\ell}.
$$

The scalar coefficient of the uncorrected Regge convolution is

$$
B(q)=[1]X^{(0)}(q)=\frac{C(q)}{1-q^2}.
$$

Since

$$
[1]\operatorname{PE}(qV_{10})A_0=\frac1{1+q},
$$

the proposed tail is

$$
A(q)=-(1+q)B_{\geq9}(q).
$$

Globally one has the elementary identity

$$
(1+q)B(q)=\frac{C(q)}{1-q}.
$$

The exact low-degree calculation gives $b_8=0$.  Therefore truncating before
multiplication introduces no boundary term, and for every $N\geq9$,

$$
a_N=-\sum_{k=0}^{N}c_k.
$$

Thus scalar-tail positivity is equivalent to

$$
\sum_{k=0}^{N}c_k\leq0
\qquad(N\geq9).
$$

This is stronger and simpler than the earlier recurrence in the $b_N$: only
one prefix sum has to be controlled.

## 3. Removing the outer Green--Schwarz difference

The exact `D4` Green--Schwarz telescope has the form

$$
F(q)=(1-q)G(q),
$$

where

$$
G(q)=\sum_{p\geq1}q^{p-1}B(q^p)
\frac{\prod_{m<p}E(q^m)}{\prod_{2\leq m\leq p}D(q^m)}.
$$

Here $E$ is the exterior polynomial of the oscillator spinor, $D$ is the
alternating exterior polynomial of the vector, and the finite polynomial
$B$ is determined by

$$
E(u)-D(u)=u(V+S)B(u).
$$

Let $\Phi_x$ denote the composition

$$
R(D_4)\longrightarrow R(B_4)
\longrightarrow \mathbb Z[x]
$$

of equal-rank Dirac folding with the six-ray one-row coordinate of $S$.
Linearity gives

$$
C(q)=\Phi_q(F(q))=(1-q)\Phi_q(G(q)).
$$

Consequently,

$$
\frac{C(q)}{1-q}=\Phi_q(G(q)),
$$

and hence

$$
a_N=-[q^N]\Phi_q(G(q)),
\qquad N\geq9.
$$

The scalar theorem is therefore a sign theorem for the Green--Schwarz
telescope *before* its outer finite difference.  This explains why the
prefix sum is the natural object rather than an accidental numerical
simplification.

## 4. The nine-ray formula

Let $V_{a,b,c,d}$ be an irreducible `D4` character in Dynkin labels and put

$$
P_{a,b,c,d}(x)=\Phi_x(V_{a,b,c,d}).
$$

The functional vanishes away from nine transverse rays.  Apart from five
wall endpoints, every nonzero value contains the common factor $(x-1)^2$:

| transverse label $(b,c,d)$ | allowed $a$ | $P_{a,b,c,d}(x)$ |
|---|---:|---|
| $(0,0,0)$ | $a\geq2$ | $x^{a-2}(x-1)^2$ |
| $(1,0,0)$ | $a\geq1$ | $-2x^{a-1}(x-1)^2$ |
| $(2,0,0)$ | $a\geq0$ | $x^a(x-1)^2$ |
| $(0,0,2)$ | $a\geq1$ | $-3x^{a-1}(x-1)^2$ |
| $(0,1,1)$ | $a\geq1$ | $3x^{a-1}(x-1)^2$ |
| $(1,0,2)$ | $a\geq0$ | $2x^a(x-1)^2$ |
| $(1,1,1)$ | $a\geq0$ | $-2x^a(x-1)^2$ |
| $(0,1,3)$ | $a\geq0$ | $-x^a(x-1)^2$ |
| $(0,2,2)$ | $a\geq0$ | $x^a(x-1)^2$ |

The endpoint values replacing the first, second, fourth and fifth rows are

$$
P_{0,0,0,0}=1,
$$

$$
P_{1,0,0,0}=x-2,
$$

$$
P_{0,1,0,0}=-2x+3,
$$

$$
P_{0,0,0,2}=-3x+4,
$$

$$
P_{0,0,1,1}=3x-4.
$$

### Derivation

Insert the `D4` Weyl character formula into the equal-rank denominator
identity

$$
\frac{A_{\rho_{B_4}}}{A_{\rho_{D_4}}}
=\prod_{i=1}^{4}
\left(e^{e_i/2}-e^{-e_i/2}\right).
$$

In doubled orthogonal coordinates the shifted `D4` highest weight is

$$
(2a+2b+c+d+6,\;2b+c+d+4,\;c+d+2,\;-c+d).
$$

The six one-row Möbius terms ask for shifted `B4` weights whose last three
coordinates are selected from the fixed patterns built from $7,5,3,1$.
After adding the four independent short-root signs, comparison of the last
three absolute coordinates leaves precisely the nine transverse labels in
the table.  The remaining first coordinate fixes the power of $x$.
Combining the six Möbius signs gives the coefficients

$$
1,-2,1,-3,3,2,-2,-1,1
$$

and the common second difference $(x-1)^2$.  If that power would cross the
wall $a=0$, the dominant representative is missing; carrying out the same
six-term sum at the wall gives the five endpoint formulas above.  No bound
on $a$ enters this calculation.

The implementation separately evaluates the Weyl alternants.  As a
regression check, the closed formula agrees on all 715 irreducibles with
total Dynkin-label sum at most nine.  This finite audit checks conventions;
the formula itself comes from the preceding all-$a$ alternant reduction.

## 5. The exact wall--curvature inequality

The nine rows form four natural transverse Euler combinations with coefficient
patterns

$$
(1,-2,1),\qquad 3(-1,1),\qquad 2(1,-1),\qquad (-1,1).
$$

It is important, however, not to interpret these four combinations as four
sets of oscillator states. Before the common $(1-q)^2$ factor is applied, the
tensor and the third combination already have negative coefficients. They are
signed Euler series, not Hilbert series. Consequently, the previously
suggested literal injection from a ``demand sector'' into a ``supply sector''
is not a well-defined proof target.

There is a sharper exact decomposition. Let $M_{a,b,c,d}(q)$ be the
multiplicity series of $V_{a,b,c,d}$ in $G(q)$. Extend each of the nine
interior formulas uniformly to the wall, allowing the powers $q^{-1}$ and
$q^{-2}$ which occur there, and define

$$
R(q)=\sum_{(b,c,d)}\epsilon_{b,c,d}
\sum_{a\geq0}q^{a+s_{b,c,d}}M_{a,b,c,d}(q).
$$

Here $(\epsilon,s)$ are read directly from the nine-ray table: they are

$$
(1,-2),\ (-2,-1),\ (1,0),\ (-3,-1),\ (3,-1),
$$

$$
(2,0),\ (-2,0),\ (-1,0),\ (1,0).
$$

Then

$$
\Phi_q(G(q))=(1-q)^2R(q)+E(q),
$$

where the entire failure of uniform continuation is the five-endpoint wall
series

$$
E(q)=(-q^{-2}+2q^{-1})M_{0,0,0,0}(q)
-q^{-1}M_{1,0,0,0}(q)
$$

$$
\mathrel{\phantom{E(q)=}}
+(2q^{-1}-1)M_{0,1,0,0}(q)
+(3q^{-1}-2)M_{0,0,0,2}(q)
$$

$$
\mathrel{\phantom{E(q)=}}
+(-3q^{-1}+2)M_{0,0,1,1}(q).
$$

The Laurent continuation is useful for deriving the identity, but it is not
the cleanest inequality. Its $L=-1,0$ part is

$$
R_{<}(q)=q^{-2}M_{0,0,0,0}(q)
$$

$$
\mathrel{\phantom{R_{<}(q)=}}
+q^{-1}\bigl(M_{1,0,0,0}(q)-2M_{0,1,0,0}(q)
-3M_{0,0,0,2}(q)+3M_{0,0,1,1}(q)\bigr).
$$

Define the genuinely stable series

$$
R_{\mathrm{st}}(q)=R(q)-R_{<}(q).
$$

Combining $(1-q)^2R_<$ with $E$ removes every negative power and gives the
actual endpoint contribution

$$
\Omega(q)=M_{0,0,0,0}(q)+(q-2)M_{1,0,0,0}(q)
$$

$$
\mathrel{\phantom{\Omega(q)=}}
+(3-2q)M_{0,1,0,0}(q)+(4-3q)M_{0,0,0,2}(q)
$$

$$
\mathrel{\phantom{\Omega(q)=}}
+(3q-4)M_{0,0,1,1}(q).
$$

Hence the preferred Laurent-free decomposition is

$$
\Phi_q(G(q))=(1-q)^2R_{\mathrm{st}}(q)+\Omega(q).
$$

Put

$$
I_N=[q^N](1-q)^2R_{\mathrm{st}}(q)
=R_{\mathrm{st},N}-2R_{\mathrm{st},N-1}
+R_{\mathrm{st},N-2}
$$

and

$$
W_N=-[q^N]\Omega(q).
$$

The scalar correction is exactly

$$
a_N=W_N-I_N,
\qquad N\geq9.
$$

Thus the correct remaining theorem is the **wall-dominance inequality**

$$
W_N\geq I_N
\qquad(N\geq9).
$$

This is not merely a renaming of the desired sign. It separates a uniform
second finite difference over $L\geq1$ from the five genuine endpoint
representations at the dominant wall. The exact values currently available
are:

| $N$ | $I_N$ | $W_N$ | $W_N-I_N=a_N$ |
|---:|---:|---:|---:|
| 9 | 3 | 4 | 1 |
| 10 | 1 | 3 | 2 |
| 11 | 2 | 4 | 2 |
| 12 | 9 | 12 | 3 |
| 13 | 11 | 19 | 8 |
| 14 | 18 | 36 | 18 |
| 15 | 34 | 63 | 29 |
| 16 | 61 | 108 | 47 |
| 17 | 93 | 174 | 81 |
| 18 | 166 | 305 | 139 |

The table is finite evidence only. Neither positivity of $I_N$ and $W_N$
separately nor their ordering has yet been proved at all degrees.

### 5.1 Constant-term form

There is also a direct bridge from this inequality to oscillator weights.
Let

$$
\mathcal H(q;z)=A_{\rho_{D_4}}(z)G(q;z),
$$

and let $\mathcal H_{u,v,w}(q;z_1)$ denote the coefficient with the last
three orthogonal exponents fixed to $(u,v,w)$, retaining only the dominant
terms whose first exponent is larger than $u$. By the Weyl character formula,
the coefficient at $z^{\lambda+\rho}$ is exactly the multiplicity of
$V_\lambda$ in $G$.

The nine rays correspond to the fixed triples

$$
(2,1,0),\ (3,1,0),\ (4,1,0),
$$

$$
(3,2,1),\ (3,2,0),\ (4,2,1),\ (4,2,0),
$$

$$
(4,3,1),\ (4,3,0).
$$

Define

$$
\mathcal K
=\mathcal H_{2,1,0}-2\mathcal H_{3,1,0}+\mathcal H_{4,1,0}
$$

$$
\mathrel{\phantom{\mathcal K=}}
-3\mathcal H_{3,2,1}+3\mathcal H_{3,2,0}
$$

$$
\mathrel{\phantom{\mathcal K=}}
+2\mathcal H_{4,2,1}-2\mathcal H_{4,2,0}
$$

$$
\mathrel{\phantom{\mathcal K=}}
-\mathcal H_{4,3,1}+\mathcal H_{4,3,0}.
$$

The first-coordinate offsets conspire to be the same on all nine rays, so
the interior contribution is simply

$$
q^{-5}(1-q)^2\mathcal K(q;z_1=q).
$$

This constant-term presentation is the most promising way to use the
oscillator product without first decomposing every coefficient into
irreducibles. It turns the remaining sign question into nine fixed
transverse coefficient extractions plus five named wall series. The code
independently verifies the Weyl-numerator extraction on the first
pre-telescope coefficients.

### 5.2 The fixed modified-Frobenius slice

There is a further exact organization of the nine rays. For a tensorial
`D4` label, the underlying four-row Young diagram is

$$
\lambda(a,b,c,d)=
\left(a+b+\frac{c+d}{2},\ b+\frac{c+d}{2},\
\frac{c+d}{2},\ \frac{|d-c|}{2}\right).
$$

Write a diagram in the modified Frobenius notation

$$
(L_1,L_2,\ldots\mid h_1,h_2,\ldots),
$$

where $L_i$ counts boxes to the right of the $i$th diagonal box and $h_i$
is the height of its column including that box. Fix $L=L_1\geq1$. The nine
rays become the following finite table.

| `D4` label | diagram | modified Frobenius data | coefficient |
|---|---|---|---:|
| $(L+1,0,0,0)$ | $(L+1)$ | $(L\mid1)$ | $1$ |
| $(L,1,0,0)$ | $(L+1,1)$ | $(L\mid2)$ | $-2$ |
| $(L-1,2,0,0)$ | $(L+1,2)$ | $(L,0\mid2,1)$ | $1$ |
| $(L,0,0,2)$ | $(L+1,1,1,1)$ | $(L\mid4)$ | $-3$ |
| $(L,0,1,1)$ | $(L+1,1,1)$ | $(L\mid3)$ | $3$ |
| $(L-1,1,0,2)$ | $(L+1,2,1,1)$ | $(L,0\mid4,1)$ | $2$ |
| $(L-1,1,1,1)$ | $(L+1,2,1)$ | $(L,0\mid3,1)$ | $-2$ |
| $(L-1,0,1,3)$ | $(L+1,2,2,1)$ | $(L,0\mid4,2)$ | $-1$ |
| $(L-1,0,2,2)$ | $(L+1,2,2)$ | $(L,0\mid3,2)$ | $1$ |

Every monomial in the uniform nine-ray formula is now the same:

$$
q^{a+s_{b,c,d}}=q^{L-1}.
$$

After deleting the common first row, the tails are

$$
\varnothing,\ (1),\ (2),\ (1,1),\ (1,1,1),\ (2,1),
\ (2,1,1),\ (2,2),\ (2,2,1).
$$

They are nine of the ten partitions in a $3\times2$ rectangle; only
$(2,2,2)$ is absent. Thus the moving part of $R(q)$ is a single finite
transverse Euler functional repeated at every first-arm length $L$, not nine
unrelated infinite families.

This observation also gives a precise possible role for super-Howe duality.
The oscillator Fock space decomposes into Lorentz irreducibles paired with
orthosymplectic lowest-weight multiplicity spaces, and the modified
Frobenius data encode those lowest weights; see
[Basile--Markou](https://arxiv.org/abs/2405.18467), especially Section 3.3.
The nine terms above are therefore neighboring candidate multiplicity spaces
with at most two diagonal boxes.

That statement is a guide, not yet a proof. The series $G$ also contains the
massive-ground-multiplet division and the removal of the level-one vector
tower. One must first realize those operations cohomologically, or verify
that the relevant orthosymplectic maps descend to their quotient. The Howe
decomposition of the unconstrained Fock space alone does not establish the
wall-dominance inequality.

### 5.3 Exact Plücker factorization of the transverse index

The nine coefficients themselves have an additional exact structure. Pad a
tail to

$$
\tau=(\tau_1,\tau_2,\tau_3)\subseteq(2,2,2)
$$

and associate the three-subset

$$
I_\tau=\{\tau_3+1,\ \tau_2+2,\ \tau_1+3\}
\subset\{1,2,3,4,5\}.
$$

The ten partitions in the rectangle thereby label the standard basis of
$\bigwedge^3\mathbb Z^5$. Let $J_\tau=\{j_1<j_2\}$ be the complementary
two-subset, and let $\sigma_\tau$ be the sign of the permutation obtained by
listing $I_\tau$ followed by $J_\tau$. Consider the rank-two matrix

$$
Q=
\begin{pmatrix}
1&1&1&1&1\\
0&0&1&2&3
\end{pmatrix}.
$$

For every one of the ten tails, including the absent one, its transverse
coefficient is exactly

$$
c_\tau=\sigma_\tau\det Q_{J_\tau}.
$$

For example, $\tau=(1)$ has $I_\tau=\{1,2,4\}$,
$J_\tau=\{3,5\}$ and $c_\tau=-(3-1)=-2$. The missing tail
$\tau=(2,2,2)$ has complementary set $\{1,2\}$, whose two columns in $Q$
are equal, so its coefficient is zero.

Equivalently, the ten-component coefficient vector is the Hodge dual of the
decomposable bivector

$$
(1,1,1,1,1)\wedge(0,0,1,2,3).
$$

All its Plücker quadratic relations therefore vanish. This is an exact
factorization of the transverse functional, not a numerical pattern, and it
explains at once why there are nine nonzero terms rather than ten. It also
supplies the algebraic skeleton for two successive exterior operations.
What is still missing is a realization of those operations as differentials
between the actual multiplicity spaces of $G$.

The Plücker formula also compresses the complete `D4` Weyl numerator. Put

$$
K_L=\sum_{\tau\subseteq(2,2,2)}c_\tau
[L+1,\tau]_{D_4},
$$

where $[L+1,\tau]_{D_4}$ denotes the tensor representation with first row
$L+1$ and tail $\tau$; the full-rectangle coefficient is understood to be
zero. The shifted orthogonal exponents of its summands are

$$
(L+4,k_1,k_2,k_3),
\qquad \{k_1,k_2,k_3\}\subset\{0,1,2,3,4\}.
$$

For torus variables $z_1,\ldots,z_4$, define

$$
f_i^\pm(k)=z_i^k\pm z_i^{-k}.
$$

Let $\mathcal B_L^\pm$ be the $6\times6$ matrix whose columns are indexed in
the order

$$
L+4,0,1,2,3,4,
$$

whose first four rows are $f_i^\pm(k)$, and whose final two rows are

$$
(0,1,1,1,1,1),
$$

$$
(0,0,0,1,2,3).
$$

Laplace expansion along the final two rows gives the all-$L$ identity

$$
A_{\rho_{D_4}}K_L
=-\frac12\left(\det\mathcal B_L^++\det\mathcal B_L^-\right).
$$

The two determinants on the right are precisely the two even-sign components
of the `D4` Weyl alternant. Thus nine moving Weyl numerators have become one
bordered determinant.

The complete stable-arm sum is no harder. Only the first column depends on
$L$, so linearity of the determinant and the geometric series give

$$
\sum_{L\geq1}q^{L-1}f_i^\pm(L+4)
=\frac{z_i^5}{1-qz_i}
\mathbin{\pm}\frac{z_i^{-5}}{1-q/z_i}.
$$

Let $\mathcal B^\pm(q)$ denote the same bordered matrix with this rational
first column. Then

$$
A_{\rho_{D_4}}\sum_{L\geq1}q^{L-1}K_L
=-\frac12\left(\det\mathcal B^+(q)+\det\mathcal B^-(q)\right),
$$

and, with the usual character inner product,

$$
R_{\mathrm{st}}(q)
=\left\langle\sum_{L\geq1}q^{L-1}K_L,\ G(q)\right\rangle_{D_4}.
$$

This removes the infinite arm sum before any estimate is made. As a useful
check on the cancellation, the Weyl
dimension formula gives the polynomial identity

$$
\dim K_L=15
\qquad(L\geq1),
$$

even though $K_L$ is a virtual character with large positive and negative
irreducible terms. The constant dimension does not imply positivity. The
value of the bordered form is that it can now be inserted directly into the
oscillator constant term; determinant or fermionic-Fock identities, rather
than nine separate multiplicity estimates, become available for the next
step.

There is an equivalent finite-numerator form. Let

$$
D_V(t)=\sum_{j=0}^{8}(-t)^j\Lambda^jV.
$$

The common denominator of the rational first column is precisely $D_V(t)$.
Consequently,

$$
D_V(t)\sum_{L\geq1}t^{L-1}K_L=N(t),
$$

where

$$
N(t)=\sum_{r=0}^{7}t^rN_r
$$

is a polynomial of degree at most seven in the `D4` representation ring.
There are no coefficients at degree eight or above; this follows directly
from the bordered determinant, since clearing the row denominator leaves a
first-column numerator of degree one and the remaining three row denominators
supply six further linear factors. The implementation also verifies the character
identity across and beyond the closing degree.

Since $\dim K_L=15$ and $\dim D_V(t)=(1-t)^8$, one obtains

$$
\dim N_r=15(-1)^r\binom{7}{r}.
$$

For orientation, the final coefficient is already supported entirely on the
five-wall neighborhood:

$$
N_7=-[1,0,0,0]+2[0,1,0,0]
+3[0,0,0,2]-3[0,0,1,1].
$$

Because $D_V(t)^{-1}=\operatorname{PE}(tV)$, the stable functional may also
be written

$$
R_{\mathrm{st}}(q)
=\left\langle \operatorname{PE}(qV)N(q),\ G(q)\right\rangle_{D_4},
$$

where the series-valued inner product adds the two displayed powers of $q$.
Thus the infinite stable-arm family is equivalent to eight fixed virtual
characters followed by the ordinary symmetric-vector tower.

### 5.4 Cancellation to six fixed `B4` functionals

In the representation ring, tensoring by a self-dual character is
self-adjoint:

$$
\langle AX,Y\rangle=\langle X,AY\rangle
$$

when $A=A^*$. This remains true coefficientwise for the convolution-valued
series inner product. Therefore

$$
R_{\mathrm{st}}(q)
=\left\langle N(q),\operatorname{PE}(qV)G(q)\right\rangle_{D_4}.
$$

But the exact HFT Regge factorization says

$$
Q(q):=\operatorname{PE}(qV)G(q)
=Z_m(q)\mathord\downarrow_{D_4},
$$

where $Z_m(q)$ is the original `B4` massive-primary series, with its constant
term at physical level one. Thus the symmetric-vector factor cancels exactly;
no skewing approximation is involved.

The five endpoint terms collapse at the same time. Define the `D4` polynomial

$$
U(q)=1-2[1,0,0,0]+3[0,1,0,0]
+4[0,0,0,2]-4[0,0,1,1]
$$

$$
\mathrel{\phantom{U(q)=}}
+q\bigl([1,0,0,0]-2[0,1,0,0]
-3[0,0,0,2]+3[0,0,1,1]\bigr).
$$

Then $\Omega(q)=\langle U(q),G(q)\rangle_{D_4}$. Since
$G(q)=D_V(q)Q(q)$, self-adjointness gives

$$
\Phi_q(G)=\langle P(q),Q(q)\rangle_{D_4},
$$

where

$$
P(q)=(1-q)^2N(q)+D_V(q)U(q).
$$

Although the two summands on the right can have degrees nine, their
coefficients cancel identically above degree five.

Let $\sigma$ exchange the two `D4` spinor nodes, and put

$$
J_8=8_s-8_c.
$$

The series $Q$, being restricted from `B4`, is $\sigma$-invariant. Only the
outer-symmetric part of $P$ can therefore contribute. Exact
fundamental-character algebra gives

$$
\frac{P(q)+\sigma P(q)}{2}
=\frac{J_8^2}{2}\operatorname{Res}^{B_4}_{D_4}\mathscr C(q),
$$

where $\mathscr C(q)=\sum_{r=0}^5q^rC_r$ is the following six-term `B4`
kernel. Write

$$
e_j=\Lambda^j9,
$$

$$
s_k=\sum_{j=0}^k(-1)^je_j.
$$

Then

$$
(C_0,C_1,C_2,C_3,C_4,C_5)
=(s_3,\ s_4+s_2,\ s_3+s_1,\ s_2+s_0,\ s_1,\ s_0).
$$

Equivalently:

| $r$ | $C_r$ |
|---:|---|
| 0 | $1-9+36-84$ |
| 1 | $2-2(9)+2(36)-84+126$ |
| 2 | $2-2(9)+36-84$ |
| 3 | $2-9+36$ |
| 4 | $1-9$ |
| 5 | $1$ |

The factor $J_8$ is, up to orientation, the relative Weyl denominator
$A_{\rho_{B_4}}/A_{\rho_{D_4}}$. Since
$|W(B_4)|=2|W(D_4)|$, Weyl integration gives

$$
\frac12\left\langle
J_8^2\operatorname{Res}^{B_4}_{D_4}X,
\operatorname{Res}^{B_4}_{D_4}Y
\right\rangle_{D_4}
=\langle X,Y\rangle_{B_4}.
$$

Applying this identity coefficientwise proves the all-orders reduction

$$
\boxed{\ \Phi_q(G(q))
=\left\langle\mathscr C(q),Z_m(q)\right\rangle_{B_4}.\ }
$$

If $Z_m(q)=\sum_{d\geq0}Q_dq^d$, the remaining scalar theorem is simply

$$
\sum_{r=0}^{5}\langle C_r,Q_{N-r}\rangle_{B_4}\leq0
\qquad(N\geq9).
$$

Only the multiplicities of $1,9,36,84$ and $126$ in six adjacent HFT levels
occur. Thus the moving Regge direction, the nine `D4` rays and the five
separate endpoint series have all disappeared from the final inequality.
The code verifies the representation-ring reduction exactly and checks the
resulting `B4` convolution against the independent HFT coefficients through
the available comparison range. This is still a reduction, not the sign
proof.

### 5.5 Primitive-form inversion and the final scalar dominance

The six-term inequality has one further exact simplification. Write the
low-form multiplicities in one HFT primary coefficient as

$$
m_j(d)=\langle e_j,Q_d\rangle_{B_4},
\qquad 0\leq j\leq4,
$$

and define their alternating, or primitive-form, coordinates by

$$
h_k(d)=(-1)^k\langle s_k,Q_d\rangle_{B_4}.
$$

Equivalently,

$$
h_k(d)=m_k(d)-m_{k-1}(d)+m_{k-2}(d)-\cdots+(-1)^km_0(d).
$$

This is a finite Möbius inversion along the exterior-form chain. The word
``primitive'' refers only to this alternating removal of the lower forms; it
does not yet assert that the resulting numbers are dimensions of an
all-orders physical space. Let

$$
H_k(q)=\sum_{d\geq0}h_k(d)q^d
$$

and form the four-level combination

$$
D(q)=H_3(q)-qH_2(q)+q^2H_1(q)-q^3H_0(q).
$$

Substituting the definitions of the six $C_r$ gives the representation-ring
identity

$$
\boxed{\ \Phi_q(G(q))=-(1+q^2)D(q)+qH_4(q).\ }
$$

Indeed, the functional kernel of $D$ is
$-(s_3+qs_2+q^2s_1+q^3s_0)$, so the coefficient at each of the six powers of
$q$ is respectively

$$
s_3,\quad s_4+s_2,\quad s_3+s_1,\quad
s_2+s_0,\quad s_1,\quad s_0.
$$

Therefore, if $D_N=[q^N]D(q)$, the complete remaining scalar theorem is

$$
\boxed{\ a_N=D_N+D_{N-2}-h_4(N-1)\geq0,
\qquad N\geq9.\ }
$$

There is a final useful inversion which exposes an adjacent exterior-degree
map. Put

$$
t_k=(-1)^ks_k.
$$

As a formal power series in an exterior-degree marker $x$,

$$
\sum_{k\geq0}t_kx^k=\frac{\Lambda_x9}{1+x}.
$$

The coefficients needed here stop at $k=4$, so no convergence or infinite
representation-ring assertion is involved. Define the second primitive
series

$$
\Pi_k(q)=\sum_{r=0}^k(-q)^rH_{k-r}(q).
$$

Equivalently,

$$
\sum_{k\geq0}\Pi_k(q)x^k
=\left\langle
\frac{\Lambda_x9}{(1+x)(1+qx)},Z_m(q)
\right\rangle_{B_4}.
$$

Expanding both inversions gives a particularly concrete triangular formula:

$$
\pi_k(N)=\sum_{a=0}^k(-1)^a
\sum_{r=0}^a m_{k-a}(N-r),
$$

where a multiplicity with negative level is zero. Thus every entry occurs
with unit coefficient; the binomial-looking multiplicities in the earlier
ray description arose only after collapsing this triangular array. This is
the Euler characteristic of a fixed finite staircase of low-form
multiplicity spaces. A proof by homological algebra would need horizontal
and vertical maps making that staircase exact away from its outer edge.

Then $D=\Pi_3$ and $\Pi_4=H_4-qD$. Consequently the whole scalar index is

$$
\boxed{\ \Phi_q(G)=q\Pi_4-\Pi_3.\ }
$$

At the character level the same statement is the single coefficient formula

$$
\boxed{\ \mathscr C(q)=[x^4]
\frac{\Lambda_x9}{(1+x)(1+qx)}(q-x).\ }
$$

The first division has an exact branching meaning rather than being merely
formal. Since $9\mathord\downarrow_{D_4}=8_v+1$, restriction cancels the
factor $1+x$ and gives

$$
\mathscr C(q)\mathord\downarrow_{D_4}
=[x^4]\Lambda_x8_v\frac{q-x}{1+qx}.
$$

Thus only the $q$-graded second inversion remains after passage to the
light-cone rotation group. Expanding this one coefficient reproduces the six
positive chain representations and alternating signs displayed below.

Thus, writing $\pi_k(N)=[q^N]\Pi_k(q)$, the smallest current form of the
scalar theorem is

$$
\boxed{\ \pi_3(N)\geq\pi_4(N-1),
\qquad N\geq9.\ }
$$

This is smaller than the six-term statement and sharper than the preceding
three-term expression: it compares adjacent exterior degrees with one unit
of oscillator-degree shift. The exact values in the first relevant range
are:

| $N$ | $\pi_3(N)$ | $\pi_4(N-1)$ | $a_N$ |
|---:|---:|---:|---:|
| 9 | 3 | 2 | 1 |
| 10 | 5 | 3 | 2 |
| 11 | 7 | 5 | 2 |
| 12 | 15 | 12 | 3 |

In the computed range all five $h_k(d)$ are nonnegative from $d=6$, and both
$\pi_3(d)$ and $\pi_4(d)$ are nonnegative from the same point. These
observations are useful evidence for a homological interpretation, but they
do not prove the adjacent-degree dominance.

The next analytic task is consequently very sharp. One must first realize
$\Pi_3$ and $\Pi_4$ as Hilbert series of actual spaces in the stable range,
and then construct a degree-$(+1,-1)$ injection from the space counted by
$\pi_4(N-1)$ to that counted by $\pi_3(N)$. Alternatively one may prove the
same coefficient inequality directly from the HFT oscillator product. The
code checks the compact character identity and its evaluation on
independently derived HFT primaries; no protected uplift enters the check.

### 5.6 A concrete cohomological proof target

Let $\mathcal M_{L,\tau}$ denote the graded multiplicity space associated
with first row $L+1$ and transverse tail $\tau$. At fixed $L$, the stable
nine-ray combination is

$$
\chi_L=\mathcal M_{L,\varnothing}-2\mathcal M_{L,(1)}
+\mathcal M_{L,(2)}+3\mathcal M_{L,(1,1)}
-3\mathcal M_{L,(1,1,1)}
$$

$$
\mathrel{\phantom{\chi_L=}}
-2\mathcal M_{L,(2,1)}+2\mathcal M_{L,(2,1,1)}
+\mathcal M_{L,(2,2)}-\mathcal M_{L,(2,2,1)}.
$$

The transverse Plücker factorization gives two exterior operations, while
the common $(1-q)^2$ is the Euler polynomial of a two-generator degree-one
Koszul complex. This suggests a specific analytic mechanism:

1. construct a bounded transverse complex whose Euler characteristic is
   $\chi_L$;
2. tensor it with the two-generator Koszul complex giving $(1-q)^2$;
3. prove exactness in the stable first-arm direction;
4. identify the failure of exactness at $L=0,-1$ with the five wall terms;
5. prove that the surviving homology occurs in the parity for which its
   Hilbert series is $W_N-I_N$.

Such a construction would prove $a_N\geq0$ because $A(q)$ would be a genuine
homology Hilbert series. However, the primitive-form reduction gives a
smaller target. Each $s_k$ is a truncated exterior, or Koszul, Euler
character of the vector $9$. The preferred cohomological route is now to
realize the degree-$(+1,-1)$ map implicit in
$\pi_3(N)-\pi_4(N-1)$ as one bounded complex acting on the HFT
massive-primary spaces and to prove that its degree-$N$ homology is
concentrated in the parity giving

$$
-\langle\mathscr C(q),Z_m(q)\rangle_{B_4}.
$$

This interpretation has an exact branching check. Since

$$
9\mathord\downarrow_{D_4}=8_v+1,
$$

the alternating sum telescopes to

$$
s_k\mathord\downarrow_{D_4}=(-1)^k\Lambda^k8_v.
$$

This is the top homology of the exterior complex obtained by contraction with
the distinguished one-dimensional direction. Consequently,

$$
\mathscr C(q)\mathord\downarrow_{D_4}
=-\Lambda^3 8_v
+q\bigl(\Lambda^4 8_v+\Lambda^2 8_v\bigr)
$$

$$
\mathrel{\phantom{\mathscr C(q)\mathord\downarrow_{D_4}=}}
-q^2\bigl(\Lambda^3 8_v+8_v\bigr)
+q^3\bigl(\Lambda^2 8_v+1\bigr)-q^4 8_v+q^5.
$$

Thus the proposed complex has six positive chain-group representations, of
dimensions $56,98,64,29,8,1$, with alternating parity. The branching identity
does not supply the differential on the HFT multiplicity spaces, but it
shows that the word ``Koszul'' here is structural rather than an analogy.

There is an important obstruction to the most naive differential. Although
$Z_m=\operatorname{PE}(q9)F$ is an exact representation-ring factorization,
the remainder $F$ is virtual: for example its degree-two coefficient already
contains the scalar with coefficient $-1$. The cumulative identity above
sharpens this observation to $F=(1-q)\widehat G$, with $\widehat G$ positive
through degree 20. This removes the simplest finite-level positivity
objection after cumulative completion, but it still does not construct an
actual free module. Ordinary Koszul exactness cannot be quoted until the
nine covariant degree-one maps and their regularity have been established on
the cumulative physical-state space.

A viable oscillator construction should instead be made before the
universal massive-supermultiplet division. It must commute with the massive
supercharges, so that it acts trivially on the universal multiplet and
descends to the primary multiplicity spaces. In concrete terms, the leading
bosonic creation/contraction map would need the fermionic completion required
by supersymmetry or BRST invariance. Establishing that commutation and then
identifying the resulting staircase Euler character with $\Pi_k$ would turn
the compact identity into an actual complex.

The fixed-$L$ Plücker complex remains a possible way to construct this
smaller complex. Odd orthosymplectic maps are suggestive, but Howe duality by
itself does not provide homomorphisms between distinct Lorentz multiplicity
spaces. No differential with the required descent through the massive
supermultiplet quotient has yet been constructed. The direct alternative is
to prove the displayed primitive-form dominance from the HFT oscillator
product.

### 5.7 Comparison with the superstring no-ghost complex

There is a physically well-motivated model for the kind of concentration
argument now required. Dedushenko's superstring no-ghost theorem
([arXiv](https://arxiv.org/abs/1212.3592),
[INSPIRE](https://inspirehep.net/literature/1207483)) filters the BRST complex
by light-cone degree. At nonzero momentum its spectral sequence removes the
longitudinal and ghost excitations, and the absolute BRST cohomology consists
of two copies of the light-cone spectrum at adjacent ghost numbers. The same
construction supplies a positive inner product on cohomology.

This is a useful proof template, not yet an identification with the present
complex. The grading in that theorem is BRST ghost number, whereas $x$ above
records exterior-form degree in the `SO(9)` representation ring. Moreover,
the two BRST copies are isomorphic, while the difference
$\pi_3(N)-\pi_4(N-1)=a_N$ is nonzero. Thus the ordinary no-ghost theorem
cannot by itself prove the scalar inequality.

The precise BRST question is narrower: refine the filtered BRST Euler
character simultaneously by mass level and massive little-group character,
divide out the universal massive supermultiplet, and then test whether its
exterior-degree-three/four slice is

$$
[x^4]\frac{\Lambda_x9}{(1+x)(1+qx)}(q-x).
$$

Only such a character identity would allow the no-ghost spectral-sequence
vanishing to be imported. The sole citing follow-up found in the INSPIRE
traversal concerns the covariant-to-light-cone map in superstring field
theory, not this representation-refined character, so it does not presently
close the gap.

### 5.8 DDF/Koszul audit and the primitive quotient

The light-cone DDF construction makes the proposed bidegree map considerably
more concrete, but it also exposes an important correction to the naive
injectivity claim. Write

$$
V=8_v,
$$

and let $S$ and $C$ be the two chiral eight-dimensional spinors of $D_4$.
The restriction of the universal massive supermultiplet factor is exactly

$$
Z_Qmathord\downarrow_{D_4}=(V+S)(V+C).
$$

If

$$
\delta=S-C
$$

and

$$
D_V(q)=\sum_{j=0}^{8}(-q)^j\Lambda^jV,
$$

then exact character arithmetic gives the triality identity

$$
\boxed{\ \delta^2=D_V(1)
=\sum_{j=0}^{8}(-1)^j\Lambda^jV.\ }
$$

The compact scalar kernel found above has precisely the same specialization:

$$
\boxed{\ \mathscr C(1)\mathord\downarrow_{D_4}=D_V(1).\ }
$$

This is also the relative Weyl-denominator factor for the equal-rank pair
$D_4\subset B_4$. In particular, for restrictions of $B_4$ characters $A$
and $B$, Weyl integration gives

$$
\langle A,B\rangle_{B_4}
=\frac12\left\langle
D_V(1)A\mathord\downarrow_{D_4},
B\mathord\downarrow_{D_4}
\right\rangle_{D_4}.
$$

Thus the appearance of the vector exterior Euler class in the scalar
functional is exact; it is not merely suggested by the dimensions of the
six chain groups.

There is a second useful exact identification. Since

$$
\operatorname{PE}(qV)D_V(q)=1,
$$

the pre-telescope series is

$$
\boxed{\ G(q)=D_V(q)\,
Z_m(q)\mathord\downarrow_{D_4}.\ }
$$

Equivalently, this removes the genuine transverse level-one vector factor,
rather than the formal $B_4$ vector $9=V+1$; the extra scalar is exactly why
the earlier remainder $F=(1-q)G$ can be virtual. The coefficients of $G$ are
positive integral $D_4$ characters through degree 20. Some diagnostics are:

| degree $d$ | number of irreducible terms in $G_d$ | least coefficient |
|---:|---:|---:|
| 0 | 1 | 1 |
| 4 | 6 | 1 |
| 8 | 28 | 1 |
| 12 | 67 | 1 |
| 16 | 133 | 1 |
| 20 | 231 | 1 |

The Green--Schwarz telescope and an independent restriction of the
baseline-free HFT primaries give the same $G$ in the comparison range. The
positivity through degree 20 is nevertheless finite evidence, not a theorem
that $G$ is the character of an all-orders quotient space.

#### The cumulative $B_4$ Koszul core

The relative Dirac orientation reveals that $G$ is the restriction of a
canonical $B_4$ series, and in this case that series has a direct formula.
Let $W=9$ and set

$$
E_W(q)=\sum_{j=0}^{9}(-q)^j\Lambda^jW.
$$

Odd-dimensional Hodge duality implies that $E_W(q)$ is divisible by $1-q$.
Writing

$$
K_W(q)=\frac{E_W(q)}{1-q}
=\sum_{r=0}^{8}q^rs_r,
$$

its coefficients are the partial exterior Euler sums

$$
s_r=\sum_{j=0}^r(-1)^j\Lambda^jW,
$$

and satisfy $s_{8-r}=s_r$. Since $W$ restricts to $V+1$ under
$B_4\supset D_4$,

$$
E_W(q)\mathord\downarrow_{D_4}=(1-q)D_V(q),
$$

and therefore

$$
\boxed{\ K_W(q)\mathord\downarrow_{D_4}=D_V(q).\ }
$$

Define the cumulative Koszul core

$$
\boxed{\ \widehat G(q)=K_W(q)Z_m(q).\ }
$$

It follows immediately that

$$
\widehat G(q)\mathord\downarrow_{D_4}=G(q).
$$

This is also exactly the character reconstructed from the positive relative
Dirac orientation. Indeed, if $[\,\cdot\,]_{c>d}$ selects the $D_4$ summands
whose third Dynkin label exceeds the fourth, then degree by degree

$$
\mathfrak D^+(\widehat G_d)
=\bigl[(S-C)G_d\bigr]_{c>d}.
$$

The relative Dirac identity then proves the reconstruction, rather than only
suggesting it: multiplication by $S-C$ gives equal characters, and the
character ring is an integral domain, so this nonzero factor cancels.

The coefficients of $\widehat G$ are positive integral $B_4$ characters
through degree 20. Selected diagnostics are:

| degree $d$ | number of irreducible terms in $\widehat G_d$ | least coefficient |
|---:|---:|---:|
| 0 | 1 | 1 |
| 4 | 3 | 1 |
| 8 | 19 | 1 |
| 12 | 44 | 1 |
| 16 | 85 | 1 |
| 20 | 145 | 1 |

This identity explains the previously troublesome virtual remainder. If

$$
Z_m(q)=\operatorname{PE}(qW)F(q),
$$

then

$$
F(q)=E_W(q)Z_m(q)=(1-q)\widehat G(q).
$$

Equivalently, the cumulative massive-primary series has the exact
factorization

$$
\boxed{\ \frac{Z_m(q)}{1-q}
=\operatorname{PE}(qW)\widehat G(q).\ }
$$

Thus the virtuality of $F$ is compatible with $F$ being the first difference
of a positive core; it is not evidence against a cumulative free-module
interpretation. This is especially suggestive for the Bars problem, where
the cumulative series is the physical target from the outset.

There is an exact oscillator interpretation of the same cancellation. The
HFT bosonic factor is

$$
Z_B(q)=\prod_{m\geq1}\operatorname{PE}\bigl(q^m(W-1)\bigr).
$$

Its mode-one factor is

$$
Z_{B,1}(q)=(1-q)\operatorname{PE}(qW),
$$

so that

$$
K_W(q)Z_{B,1}(q)=1.
$$

Thus $\widehat G$ is obtained, at character level, by completing the eight
transverse mode-one bosons to the $B_4$ vector $W$ using the cumulative
scalar and then removing that complete mode-one tower. If $P(q)$ is the HFT
left-moving numerator, $P_0$ its massless term, and
$P-P_0=qZ_QZ_m$, then the exact residual formula is

$$
qZ_Q\widehat G
=Z_{B,\geq2}(q)\mathcal S(q)-K_W(q)P_0,
$$

where $\mathcal S$ denotes the NS/R fermionic factor in the HFT expression.
This isolates the nonmanifest step: the higher-mode Fock factor is explicit,
but positivity after the finite massless subtraction and division by the
universal supermultiplet $Z_Q$ still needs a module construction.

The orthogonal--orthosymplectic Howe decomposition is relevant here because
the oscillator Fock space decomposes strongly multiplicity-freely into
Lorentz representations and lowest-weight orthosymplectic multiplicity
modules; see
[Basile--Markou, arXiv:2405.18467](https://arxiv.org/abs/2405.18467).
This makes a lowest-weight or Koszul realization of $\widehat G$ plausible.
That paper does not identify the cumulative scalar, the $Z_Q$ quotient, or
the particular core $\widehat G$, so it does not itself prove the required
positivity.

#### An all-orders three-hook boundary kernel

The cumulative core also reduces the scalar functional to three moving
$B_4$ hook families. Since tensoring by a self-dual character is adjoint to
itself, define

$$
L(q)=\mathscr C(q)(1-q)\operatorname{PE}(qW).
$$

Then

$$
\boxed{\ \Phi_q(G)=\langle L(q),\widehat G(q)\rangle_{B_4}.\ }
$$

For $k\geq0$, put

$$
R_k=[k,0,0,0]-[k-1,1,0,0]+[k-1,0,1,0],
$$

where terms with a negative Dynkin label are omitted. In tensor Young-diagram
notation these are the alternating hooks

$$
(k),\qquad (k,1),\qquad (k,1,1).
$$

Exact character algebra gives the all-orders identity

$$
\boxed{\ L(q)=\sum_{k\geq0}q^k\bigl(R_k-R_{k+1}\bigr).\ }
$$

Here is a finite proof rather than an extrapolation. On the common maximal
torus,

$$
K_W(q)=\prod_{i=1}^4(1-qz_i)(1-qz_i^{-1}).
$$

For any $B_4$ tensor family with fixed lower rows, expansion of the Weyl
alternant along its first column expresses the numerator as a linear
combination of $z_i^k$ and $z_i^{-k}$. Its characters therefore obey the
order-eight recurrence with characteristic polynomial $K_W$. All three hook
families above are in their dominant range for the recurrence beginning at
degree nine. Multiplying the proposed series by $K_W$ and performing exact
representation-ring arithmetic in degrees zero through eight gives precisely
$\mathscr C(q)$, whose degree is five. The recurrence makes every later
coefficient vanish. Since $K_W$ has constant term one, multiplication by it
is injective on formal character series, proving the displayed identity at
all orders.

Consequently the remaining scalar correction can equally be written as

$$
\boxed{\ a_N=\sum_{d=0}^N
\left\langle R_{N-d+1}-R_{N-d},\widehat G_d\right\rangle_{B_4},
\qquad N\geq9.\ }
$$

The three hooks also carry an exact all-row symbol complex. Write

$$
H_k^{(0)}=(k),\qquad H_k^{(1)}=(k,1),\qquad
H_k^{(2)}=(k,1,1),
$$

so that $R_k=H_k^{(0)}-H_k^{(1)}+H_k^{(2)}$. For the $D_4$ stabilizer of a
nonzero $v\in W$, define

$$
A_j=[j,0,0,0],\qquad B_j=[j,1,0,0],\qquad
C_j=[j,0,1,1].
$$

The multiplicity-free $B_4\downarrow D_4$ interlacing rule gives, for every
$k\geq1$,

$$
H_k^{(0)}\mathord\downarrow_{D_4}=\sum_{j=0}^kA_j,
$$

$$
H_k^{(1)}\mathord\downarrow_{D_4}
=\sum_{j=1}^kA_j+\sum_{j=0}^{k-1}B_j,
$$

$$
H_k^{(2)}\mathord\downarrow_{D_4}
=\sum_{j=0}^{k-1}B_j+\sum_{j=0}^{k-1}C_j.
$$

Both relevant vector couplings have multiplicity one:

$$
\dim\operatorname{Hom}_{B_4}
\bigl(H_k^{(0)},W\otimes H_k^{(1)}\bigr)=1,
$$

$$
\dim\operatorname{Hom}_{B_4}
\bigl(H_k^{(2)},W\otimes H_k^{(1)}\bigr)=1.
$$

Evaluate the two projected vector maps at $v$. Tensor contraction identifies
the $A_1,\ldots,A_k$ summands with those in $H_k^{(0)}$, while exterior
multiplication identifies the $B_0,\ldots,B_{k-1}$ summands with those in
$H_k^{(2)}$. Hence their direct sum is injective and gives the exact
$D_4$-symbol sequence

$$
0\longrightarrow H_k^{(1)}\mathord\downarrow_{D_4}
\longrightarrow
\bigl(H_k^{(0)}\oplus H_k^{(2)}\bigr)\mathord\downarrow_{D_4}
\longrightarrow
1\oplus\bigoplus_{j=0}^{k-1}C_j
\longrightarrow0.
$$

Equivalently,

$$
R_k\mathord\downarrow_{D_4}
=1+\sum_{j=0}^{k-1}[j,0,1,1],
$$

and the consecutive shell is the single positive irrep

$$
\boxed{\ (R_{k+1}-R_k)\mathord\downarrow_{D_4}
=[k,0,1,1].\ }
$$

This proves the required contraction/wedge injection at the representation
symbol level for every first-row length, not merely in a finite window. It
still does not prove the scalar sign. The pairing in the formula for $a_N$ is
the $B_4$ inner product, whose $D_4$ expression includes the relative Weyl
Euler factor, and the symbol must act on the mass-graded $\widehat G_d$
multiplicity spaces with the displayed diagonal level shift. Establishing
that module action and excluding torsion is now the precise remaining step.

For orientation, define the three diagonal birth counts

$$
s_N^{(p)}=\sum_{d=0}^N
\left\langle H_{N-d+1}^{(p)}-H_{N-d}^{(p)},
\widehat G_d\right\rangle_{B_4}.
$$

Then $a_N=s_N^{(0)}-s_N^{(1)}+s_N^{(2)}$. Exact finite values are:

| $N$ | one-row supply $s_N^{(0)}$ | middle-hook demand $s_N^{(1)}$ | three-row supply $s_N^{(2)}$ | margin $a_N$ |
|---:|---:|---:|---:|---:|
| 9 | 2 | 4 | 3 | 1 |
| 10 | 1 | 5 | 6 | 2 |
| 12 | 4 | 18 | 17 | 3 |
| 16 | 34 | 111 | 124 | 47 |
| 20 | 238 | 711 | 845 | 372 |

All three birth counts are nonnegative in this range, and the desired theorem
is the supply--demand inequality
$s_N^{(0)}+s_N^{(2)}\geq s_N^{(1)}$. These numbers are diagnostics, not an
all-orders proof of either their individual positivity or their dominance.

A still simpler termwise argument is false. In the triangle $d+k\leq20$ there
are 38 negative individual shell pairings

$$
\left\langle R_{k+1}-R_k,\widehat G_d\right\rangle_{B_4}<0.
$$

The first one in the Bars range occurs at $(d,k)=(8,1)$, contributes at
$N=9$, and has value $-2$. The positive margin emerges only after summing
along the complete diagonal $d+k=N$. Therefore the local hook symbol cannot
be applied coefficient by coefficient. Its lift must genuinely carry the
mass-level shift and pair contributions across adjacent core degrees, as in
the DDF/$Q^1$ construction.

This observation identifies a more precise module target, but it also forces
one to distinguish two different gradings. Suppose the positive core is
realized by graded $B_4$ modules $\widehat{\mathcal G}_d$, and put

$$
\mathcal M_{d,k}^{(p)}
=\operatorname{Hom}_{B_4}
\bigl(H_k^{(p)},\widehat{\mathcal G}_d\bigr),
$$

$$
\mathcal D_N^{(p)}
=\bigoplus_{d+k=N}\mathcal M_{d,k}^{(p)}.
$$

Direct reindexing of the definition of $s_N^{(p)}$ gives

$$
s_N^{(p)}
=\dim\mathcal D_{N+1}^{(p)}-\dim\mathcal D_N^{(p)}
-\delta_{p0}\,[1:\widehat G_{N+1}].
$$

The scalar term is the $k=0$ endpoint of the one-row family; the other two
hook families have no $k=0$ module. This identity is only a dimension
identity. By itself it does not produce maps
$\mathcal D_N^{(p)}\to\mathcal D_{N+1}^{(p)}$. The more literal formula is

$$
s_N^{(p)}=\sum_{d+k=N}
\left(\dim\mathcal M_{d,k+1}^{(p)}
-\dim\mathcal M_{d,k}^{(p)}\right).
$$

Thus $s_N^{(p)}$ is a first-row, or Regge, difference at fixed core degree,
not a core-level difference. A termwise Regge injection
$\mathcal M_{d,k}^{(p)}\hookrightarrow\mathcal M_{d,k+1}^{(p)}$ is impossible.
In the finite triangle $d+k\leq20$ there are 122 negative first-row
differences, 108 of them with $d+k\geq9$. For example,

$$
[H_1^{(0)}:\widehat G_8]=3,
\qquad
[H_2^{(0)}:\widehat G_8]=2.
$$

The positive $s_N^{(p)}$ therefore arises only after mixing different core
degrees along the complete diagonal. This rules out the most direct
interpretation of the preceding dimension identity as a collection of
coefficientwise cokernels.

Two weaker finite rank tests survive. Through degree 20, a fixed-hook
core-level shift

$$
\mathcal M_{d,k}^{(p)}\longrightarrow\mathcal M_{d+1,k}^{(p)}
$$

has no dimension obstruction for $d+k\geq9$; its only three negative
dimension differences occur below that range. Likewise, the necessary rank
inequality for a vector-symbol map

$$
\mathcal M_{d,k}^{(1)}\longrightarrow
\mathcal M_{d+1,k}^{(0)}\oplus\mathcal M_{d+1,k}^{(2)}
$$

has only two failures, at total degrees four and five. These are diagnostics,
not constructions: dimensions alone neither select the maps nor prove their
compatibility with physical-state or supermultiplet quotients.

There is, however, an exact way to remove the relative-Weyl mismatch in the
local symbol. Apply the positive relative-Dirac half to all three hook
families and write

$$
\mathcal U_k^{(p)}=\mathfrak D^+\left(H_k^{(p)}\right).
$$

Explicitly,

$$
\mathcal U_k^{(0)}=[k,0,1,0]_{D_4},
$$

$$
\mathcal U_k^{(1)}=[k-1,1,1,0]_{D_4},
$$

$$
\mathcal U_k^{(2)}=[k-1,0,2,1]_{D_4}.
$$

Let $B_3=\operatorname{Spin}(7)$ stabilize a nonzero transverse vector and
put

$$
\mathcal A_j=[j,0,1]_{B_3},\qquad
\mathcal B_j=[j,1,1]_{B_3},\qquad
\mathcal C_j=[j,0,3]_{B_3}.
$$

Multiplicity-free interlacing gives, for every $k\geq1$,

$$
\mathcal U_k^{(0)}\mathord\downarrow_{B_3}
=\sum_{j=0}^{k}\mathcal A_j,
$$

$$
\mathcal U_k^{(1)}\mathord\downarrow_{B_3}
=\sum_{j=1}^{k}\mathcal A_j+
\sum_{j=0}^{k-1}\mathcal B_j,
$$

$$
\mathcal U_k^{(2)}\mathord\downarrow_{B_3}
=\sum_{j=0}^{k-1}\mathcal B_j+
\sum_{j=0}^{k-1}\mathcal C_j.
$$

Both adjacent $D_4$ vector couplings have multiplicity one. Evaluating them
at the stabilizing vector identifies the shared $\mathcal A_j$ and
$\mathcal B_j$ summands, and hence proves the all-$k$ exact symbol sequence

$$
0\longrightarrow
\mathcal U_k^{(1)}\mathord\downarrow_{B_3}
\longrightarrow
\left(\mathcal U_k^{(0)}\oplus\mathcal U_k^{(2)}\right)
\mathord\downarrow_{B_3}
\longrightarrow
\mathcal A_0\oplus\bigoplus_{j=0}^{k-1}\mathcal C_j
\longrightarrow0.
$$

Its consecutive cokernel shell is $\mathcal C_k$. This is better adapted to
the scalar functional than the earlier $B_4\downarrow D_4$ symbol, because
$\mathfrak D^+$ is an isometry:

$$
\left\langle H_k^{(p)},\widehat G_d\right\rangle_{B_4}
=\left\langle
\mathcal U_k^{(p)},\mathfrak D^+(\widehat G_d)
\right\rangle_{D_4}.
$$

The same result has a useful commutative-algebra formulation. Let
$S_V=\operatorname{Sym}(V)$ for the transverse vector $V=8_v$. The unique
vector projections define a degree-one equivariant map

$$
S_V(-1)\otimes\mathcal U_k^{(1)}
\longrightarrow
S_V\otimes
\left(\mathcal U_k^{(0)}\oplus\mathcal U_k^{(2)}\right).
$$

The map is injective. Indeed, its specialization at one nonzero vector has
full column rank by the $B_3$ sequence, so a maximal minor is a nonzero
polynomial and the map has zero kernel over the polynomial domain. Denote its
cokernel by $\mathcal C_k^{\mathrm{sym}}$. Tensoring this universal exact
sequence with a mass-graded multiplicity module $\mathcal P$ produces the
exact obstruction term

$$
\operatorname{Tor}^{S_V}_1
\left(\mathcal C_k^{\mathrm{sym}},\mathcal P\right).
$$

Thus the previously informal warning about ``torsion'' is precise for this
*truncated* two-term symbol: it remains injective after descent exactly when
this Tor group vanishes. Flatness or freeness over the mode-one polynomial
algebra would suffice. The explicit five-term construction below shows that
Tor-freeness is not the right expectation on the trace quotient; the
truncated Tor is instead the first part of a longer computable resolution.

A constructive proof can now be stated without hiding the grading issue:

1. realize the two compact primitive series on an actual mass-graded module
   carrying the mode-one $S_V$ action, before taking its primitive or
   supermultiplet quotient;
2. identify a diagonal filtration whose associated Euler differences are the
   three $s_N^{(p)}$, including the one-row scalar endpoint;
3. embed the displayed Tor group in the complete five-term gamma-traceless
   resolution and compute its homology with favorable parity; and
4. descend the oriented symbol to an injection on the resulting diagonal
   cokernels:

$$
\operatorname{coker}T_N^{(1)}
\hookrightarrow
\operatorname{coker}T_N^{(0)}\oplus
\operatorname{coker}T_N^{(2)}.
$$

If these cokernels have dimensions $s_N^{(p)}$, their inequality is exactly
$s_N^{(1)}\leq s_N^{(0)}+s_N^{(2)}$. The required operator must contain a
bidegree-$(+1,-1)$ piece to redistribute the many negative Regge differences
along a complete diagonal. The orthosymplectic relation
$\{Q^1,Q^1\}=T^{11}$ independently controls the trace quotient of the Howe
multiplicity module. It should not be identified with the adjacent projected
wedge maps. The two structures have to be combined by derived descent.

One further caution follows from the cumulative construction itself. The
mode-one vector tower has been removed in forming $\widehat G$. Consequently
the mode-one creator, and hence $Q^1$, does not automatically act as an
endomorphism of $\widehat G$. Its action must be constructed before the
Koszul/coinvariant descent and then transferred to the primitive homology.
Simply postulating $Q^1$ on the positive core would be circular.

This is a genuine simplification of support: the six fixed low-form
functionals on $Z_m$ become three principal hook trajectories on the
cumulative core. These one-row and hook families lie directly in the class
organized by orthosymplectic lowest-weight methods. Their alternating signs
mean that positivity of $\widehat G$ alone still does not prove $a_N\geq0$.
The sharpened analytic task is now to construct the hook-to-hook maps on the
orthosymplectic multiplicity modules, or to prove the displayed diagonal
dominance from their lowest-weight recurrences.

Two cautions are essential. First, positivity of $\widehat G$ is presently
proved only through degree 20. A character factorization does not by itself
construct nine commuting covariant creation maps or prove that they form a
regular sequence on an actual cumulative module. Second, a finite comparison
through degree 11 finds that neither $\Pi_3$ nor $\Pi_4$, with nearby level
shifts, is a raw multiplicity of $\Lambda^jW$ in $\widehat G$. There is a
misleading short coincidence:
$\pi_4(N)=[\Lambda^3W:\widehat G_{N-1}]$ for $6\leq N\leq10$, but at $N=11$
the two sides are respectively $12$ and $8$. The core therefore supplies a
better candidate module, but the primitive quotient or homology construction
is still required.

#### The natural DDF differential

The pure-spinor DDF construction of Jusinskas supplies BRST-closed transverse
bosonic operators $\bar V_i(k)$ and fermionic operators
$\bar W_{\dot a}(k)$ with the canonical oscillator algebra. Schematically,

$$
[\bar V_i(k),\bar V_j(p)]\mathrel\propto
k\delta_{ij}\delta_{k+p,0},
$$

$$
[\bar V_i(k),\bar W_{\dot a}(p)]=0,
$$

$$
\{\bar W_{\dot a}(k),\bar W_{\dot b}(p)\}
\mathrel\propto\delta_{\dot a\dot b}\delta_{k+p,0}.
$$

See [Jusinskas, arXiv:1406.1902](https://arxiv.org/abs/1406.1902)
([INSPIRE](https://inspirehep.net/literature/1299709)) and the complementary
light-cone analysis of
[Berkovits--Jusinskas, arXiv:1406.2290](https://arxiv.org/abs/1406.2290).
The commuting level-one bosonic creators therefore define the ordinary
Koszul differential

$$
d_j:\Lambda^jV\otimes\operatorname{Sym}^{N+3-j}V
\longrightarrow
\Lambda^{j-1}V\otimes\operatorname{Sym}^{N+4-j}V.
$$

At the middle degree this is exactly the desired shift:

$$
d_4:\Lambda^4V\otimes\operatorname{Sym}^{N-1}V
\longrightarrow
\Lambda^3V\otimes\operatorname{Sym}^{N}V.
$$

Because the bosonic creators commute, $d^2=0$. However, the raw map $d_4$ is
not injective. Exactness of the ordinary eight-variable Koszul complex gives

$$
\boxed{\ \ker d_4=\operatorname{im}d_5.\ }
$$

The exact strand dimensions begin as follows:

| target $N$ | $\dim K_4$ | $\operatorname{rank}d_4$ | $\dim\ker d_4$ |
|---:|---:|---:|---:|
| 1 | 70 | 70 | 0 |
| 2 | 560 | 504 | 56 |
| 3 | 2520 | 2100 | 420 |
| 4 | 8400 | 6600 | 1800 |
| 5 | 23100 | 17325 | 5775 |

Here $K_j=\Lambda^jV\otimes\operatorname{Sym}^{N+3-j}V$ in the displayed
strand. The automatic injection is therefore not $K_4\hookrightarrow K_3$
but

$$
\boxed{\ \bar d_4:
K_4/\operatorname{im}d_5\hookrightarrow K_3.\ }
$$

This quotient is the natural meaning of ``primitive'' suggested by the
second inversion. The new analytic problem is to prove that, after the
physical-state and universal-supermultiplet reductions, the source counted
by $\pi_4(N-1)$ is this primitive quotient and the target counted by
$\pi_3(N)$ contains its image. A finite scan through degree 10 finds no
identification of either $\Pi_3$ or $\Pi_4$ with a raw multiplicity of
$\Lambda^jV$ in $G$, even after shifts by two levels in either direction.
This rules out only the simplest identification; it does not rule out the
primitive quotient, homology or a filtered realization.

#### Why BRST closure is not yet enough

The DDF operators are BRST closed, so the bosonic Koszul construction is
compatible with BRST cohomology. It is not, by itself, compatible with the
division by the universal spacetime supermultiplet. The same DDF construction
has spacetime-supersymmetry transformations of the schematic form

$$
[q_a,\bar V_i(k)]\mathrel\propto
k(\sigma_i)_{a\dot a}\bar W_{\dot a}(k),
$$

$$
\{q_a,\bar W_{\dot a}(k)\}\mathrel\propto
(\sigma_i)_{a\dot a}\bar V_i(k).
$$

Consequently the bosonic differential does not commute with the supercharges
without a fermionic completion. A literal super-Koszul completion introduces
a spinorial auxiliary generator already in exterior degree one. The compact
kernel above instead contains the shifted scalar factor $(1+qx)^{-1}$. Since

$$
\operatorname{Hom}_{D_4}(1,S)=0,
$$

the compact scalar cannot simply be identified with that spinorial ghost on
the first page of the complex. The relative Dirac factor in the equal-rank
Weyl measure is therefore essential. The next calculation shows that it
repairs the representation type at character level, though not yet at the
level of differentials. The field--antifield extension of the DDF algebra in
[arXiv:1510.05268](https://arxiv.org/abs/1510.05268) does not by itself
supply this additional exterior grading.

#### Relative Dirac half and the gamma-traceless symbol

Let $\tau$ exchange the two spinor nodes of $D_4$. The relative Dirac identity
has a particularly simple positive half. Define the additive map

$$
\mathfrak D^+:[a,b,c,d]_{B_4}
\longmapsto [a,b,c+d+1,c]_{D_4}.
$$

The Weyl character formula gives, for every $B_4$ character $X$,

$$
\boxed{\ \delta,X\mathord\downarrow_{D_4}
=\mathfrak D^+(X)-\tau\mathfrak D^+(X).\ }
$$

The two terms have disjoint support: the third $D_4$ label is respectively
larger or smaller than the fourth. Consequently $\mathfrak D^+$ is an
isometry of the irreducible-character lattices onto the positively oriented
half:

$$
\langle X,Y\rangle_{B_4}
=\langle\mathfrak D^+(X),\mathfrak D^+(Y)\rangle_{D_4}.
$$

In particular,

$$
\mathcal M(q)=\mathfrak D^+(Z_m(q))
$$

is a positive $D_4$ character series whenever the HFT primary coefficients
are positive. This removes the virtual outer-chirality difference without
choosing an $SO(10)$ uplift.

This positive half is not merely an ad hoc choice of terms. It is the
index-two $B_4/D_4$ specialization of the
Gross--Kostant--Ramond--Sternberg equal-rank character formula
([arXiv:math/9808133](https://arxiv.org/abs/math/9808133)). Kostant's relative
Dirac operator realizes the two members of this multiplet in its kernel; see
the finite-dimensional result reviewed and extended in
[Landweber, arXiv:math/0005057](https://arxiv.org/abs/math/0005057).
Consequently $\mathcal M(q)$ has a natural candidate realization as one
chiral half of relative Dirac cohomology, degree by degree. The unresolved
question is whether the level-one string operator below acts on that
cohomology with the required grading.

Put $e_j=\Lambda^j9$ and $U_j=\mathfrak D^+(e_j)$. The five low forms become
the following gamma-traceless spinor-form tower:

| $j$ | $U_j$ as a $D_4$ irrep | dimension |
|---:|---:|---:|
| 0 | $[0,0,1,0]$ | 8 |
| 1 | $[1,0,1,0]$ | 56 |
| 2 | $[0,1,1,0]$ | 160 |
| 3 | $[0,0,2,1]$ | 224 |
| 4 | $[0,0,3,0]$ | 112 |

Since

$$
\delta\,(1+x)\Lambda_xV
=\sum_j\bigl(U_j-\tau U_j\bigr)x^j,
$$

the complete compact kernel satisfies

$$
\boxed{\
\delta\frac{\Lambda_xV}{1+qx}
=\frac{\sum_j(U_j-\tau U_j)x^j}{(1+x)(1+qx)}.
\ }
$$

Thus the shifted scalar does become a spinorial, gamma-traceless index after
the exact relative Dirac insertion. The two primitive inversions are the two
scalar Euler factors acting on this actual spinor-form tower. This improves
the earlier conclusion: a Dirac descent is not merely hypothetical at the
character level.

There is also an exact candidate symbol map. Let $B_3=\operatorname{Spin}(7)$
be the stabilizer of a nonzero vector in $V$, and put

$$
A_0=[0,0,1],\quad A_1=[1,0,1],\quad
A_2=[0,1,1],\quad A_3=[0,0,3].
$$

The restrictions telescope multiplicity-freely:

$$
U_0\mathord\downarrow_{B_3}=A_0,
$$

$$
U_1\mathord\downarrow_{B_3}=A_0+A_1,
$$

$$
U_2\mathord\downarrow_{B_3}=A_1+A_2,
$$

$$
U_3\mathord\downarrow_{B_3}=A_2+A_3,
$$

$$
U_4\mathord\downarrow_{B_3}=A_3.
$$

Moreover,

$$
\dim\operatorname{Hom}_{D_4}(U_{j+1},V\otimes U_j)=1
\qquad(0\leq j<4),
$$

and no nonadjacent pair among these five modules is coupled by $V$. Evaluate
the unique nonzero projected vector map at any nonzero $v\in V$. On the
$B_3$ decompositions it maps the shared $A_j$ isomorphically and kills the
other summand. Hence its symbols form the exact sequence

$$
0\longrightarrow U_0\longrightarrow U_1\longrightarrow U_2
\longrightarrow U_3\longrightarrow U_4\longrightarrow0.
$$

Reversing the sequence gives, in particular, an injective top symbol

$$
\boxed{\ U_4\hookrightarrow U_3.\ }
$$

The branching calculation determines the possible ranks, but by itself it
does not prove that consecutive projected symbols compose to zero. There is
now an explicit Clifford model which supplies this missing check. Realize a
positive half-spin module as $S^+=\Lambda^{\mathrm{even}}\mathbb C^4$ and put

$$
U_p=\ker\left(
\gamma\mathbin\lrcorner:
\Lambda^pV\otimes S^+
\longrightarrow
\Lambda^{p-1}V\otimes S^-
\right),
\qquad 0\leq p\leq4.
$$

The resulting irreducibles are exactly the five $U_p$ above. Let $\pi_p$ be
the equivariant projection onto this gamma-traceless summand, along gamma
exterior multiplication. For $v\in V$, define

$$
\sigma_p(v)=\pi_{p+1}\circ(v\wedge-):U_p\longrightarrow U_{p+1}.
$$

Exact rational Clifford algebra gives

$$
\sigma_{p+1}(v)\sigma_p(v)=0.
$$

For a non-null vector the four ranks are

$$
(8,48,112,112),
$$

which proves exactness of the five-term symbol. For a nonzero complex null
vector the ranks are

$$
(8,48,112,92).
$$

The null rank drop will matter below. It is invisible in the compact real
stabilizer calculation because a nonzero Euclidean vector is never null.

This finite symbol extends to a genuine polynomial free resolution. Write
$S_V=\operatorname{Sym}(V)$ and use the polynomial degree shifts indicated
in parentheses. Then

$$
0\longrightarrow S_V(-4)\otimes U_0
\longrightarrow S_V(-3)\otimes U_1
\longrightarrow S_V(-2)\otimes U_2
\longrightarrow S_V(-1)\otimes U_3
\longrightarrow S_V\otimes U_4
\longrightarrow\mathcal T\longrightarrow0
$$

is exact. One direct proof uses the Buchsbaum--Eisenbud rank criterion. From
the right, the expected map ranks are $112,112,48,8$. The rightmost maximal
rank drops on the quadratic null cone, of codimension one, while the other
three ranks drop only at the origin, of codimension eight. These codimensions
satisfy the required lower bounds $1,2,3,4$.

The cokernel is not virtual. Its degree-$n$ component is the single positive
gamma-traceless trajectory

$$
\boxed{\ \mathcal T_n=[n,0,3,0]_{D_4}.\ }
$$

Equivalently, the full character identity is

$$
\sum_{n\geq0}q^n[n,0,3,0]_{D_4}
=\operatorname{PE}(qV)
\left(U_4-qU_3+q^2U_2-q^3U_1+q^4U_0\right).
$$

The identity follows by clearing the vector symmetric-power denominator in
the $D_4$ Weyl alternant. The resulting numerator closes at degree four and
is the displayed five-term polynomial. The implementation checks full
characters through and beyond that closure, as well as the exact Clifford
matrices. This is the monogenic or gamma-traceless row of the spinor-valued
form construction discussed in
[Bures, arXiv:math/9901039](https://arxiv.org/abs/math/9901039); that paper
does not make the string-theoretic identification needed here.

The same resolution unifies the preceding all-hook symbol. Interlacing gives

$$
[n,0,3,0]_{D_4}\mathord\downarrow_{B_3}
=\sum_{j=0}^n[j,0,3]_{B_3}.
$$

Hence the cokernel of the fixed-$k$ three-hook symbol is

$$
A_0\oplus
[k-1,0,3,0]_{D_4}\mathord\downarrow_{B_3},
$$

with the second term omitted at $k=0$. Its consecutive shell is precisely
$[k,0,3]_{B_3}$.

The null rank drop has a clean homological meaning. After tensoring the free
resolution with the residue field of a nonzero null vector, the fibre has
twenty-dimensional homology in each of the final two positions. This is a
fibrewise $\operatorname{Tor}$ group, not a failure of the polynomial
resolution. In particular, a proof that passes to the trace quotient
$S_V/(v^2)$ should not expect the earlier top-symbol $\operatorname{Tor}_1$
to vanish. The correct operation is to retain the full five-term resolution
and calculate its derived tensor product.

There is also an exact positive-core consequence. Put

$$
N(q)=U_4-qU_3+q^2U_2-q^3U_1+q^4U_0,
$$

$$
\mathcal T(q)=\operatorname{PE}(qV)N(q)
=\sum_{n\geq0}q^n[n,0,3,0]_{D_4},
$$

$$
\mathcal M(q)=\mathfrak D^+(Z_m(q)),
\qquad
\mathcal P(q)=\mathfrak D^+(\widehat G(q)).
$$

Outer antisymmetrization and
$D_V(q)(\mathcal M-\tau\mathcal M)=\mathcal P-\tau\mathcal P$
then give the convolution identity

$$
\boxed{\
\left\langle N(q),\mathcal M(q)\right\rangle_{D_4}
=\left\langle\mathcal T(q),\mathcal P(q)\right\rangle_{D_4}.
\ }
$$

The factor of two from the two outer orientations cancels on the two sides.
Thus this particular alternating expression is a manifestly positive
pairing whenever the cumulative core is positive. Its first coefficients
are

$$
0,0,0,0,0,1,1,1,3,6,10,19,34,59,\ldots.
$$

Call this series $B_\Gamma(q)$, to distinguish it from the unrelated scalar
convolution $B(q)$ in Section 2. It is not by itself the Bars margin. If

$$
J=N(1)=U_4-U_3+U_2-U_1+U_0,
$$

then the positive relative-Dirac half of the compact scalar kernel obeys

$$
(1-q)K_\Phi(q)=(1+q)J-(1+q^2)N(q).
$$

After pairing with $\mathcal M$, this becomes

$$
\boxed{\
(1-q)\Phi_q(G)
=(1+q)H_4(q)-(1+q^2)B_\Gamma(q).
\ }
$$

Consequently, with $a_N=-[q^N]\Phi_q(G)$ in the Bars tail and with negative
indices interpreted as zero,

$$
a_N-a_{N-1}
=B_{\Gamma,N}+B_{\Gamma,N-2}-h_4(N)-h_4(N-1).
$$

This is a sharper remaining target than abstract Tor-freeness: prove the
required prefix dominance between the positive gamma-traceless resolution
series $B_\Gamma$ and the fourth primitive series $H_4$. It also explains why the
most optimistic conjecture, that $a_N$ itself is simply one diagonal
$[k,0,0,2]_{B_4}$ multiplicity of $\widehat G$, is false in the finite
audit.

There is an important consistency check and obstruction here. To move the
$H_4$ term from $\mathcal M$ to the cumulative core $\mathcal P$, one must
first outer-antisymmetrize. Let $\operatorname{or}_+$ select the terms whose
third $D_4$ Dynkin label is larger than the fourth, and define

$$
\mathcal S^+(q)=\operatorname{or}_+\left[
\operatorname{PE}(qV)(J-\tau J)
\right].
$$

It would be incorrect to replace $\mathcal S^+$ by
$\operatorname{PE}(qV)J$ before taking this orientation. Put

$$
\mathcal K(q)=(1+q^2)\mathcal T(q)-(1+q)\mathcal S^+(q),
\qquad
\mathcal L(q)=\frac{\mathcal K(q)}{1-q}.
$$

For $n\geq0$, set

$$
E_n=[n+1,0,1,0]-[n,1,1,0]+[n,0,2,1],
\qquad
E_{-1}=U_0.
$$

Then the prefix kernel is exactly

$$
\boxed{\ \mathcal L_n=E_n-E_{n-1}.\ }
$$

For $n\geq1$, this is the six-term virtual character

$$
-[n,0,1,0]+[n-1,1,1,0]-[n-1,0,2,1]
+[n+1,0,1,0]-[n,1,1,0]+[n,0,2,1].
$$

Its stabilizer restriction is nevertheless the single positive shell

$$
\mathcal L_n\mathord\downarrow_{B_3}=[n,0,3]_{B_3}.
$$

This identity is not a new finite pattern. In the notation of the earlier
three-hook reduction,

$$
E_n=\mathfrak D^+(R_{n+1}),
$$

so it follows immediately from the already proved all-orders formula for
$R_{n+1}-R_n$. The $\mathfrak D^+$ isometry gives

$$
a_N=\sum_{d=0}^N
\left\langle\mathcal L_{N-d},\mathcal P_d\right\rangle_{D_4}.
$$

Thus the five-term resolution closes an exact consistency loop: its
$B_\Gamma$--$H_4$ prefix is precisely the previous three-hook shell. It does
not make that shell coefficientwise positive in $D_4$. The remaining gain is
structural---the shell is now the boundary Euler character of a known free
resolution---but a filtered module-level exactness or dominance argument is
still required.

Basile and Markou organize the transverse superstring oscillator space by an
orthogonal--orthosymplectic duality, with odd orthosymplectic generators
mixing bosonic and fermionic oscillators
([arXiv:2405.18467](https://arxiv.org/abs/2405.18467)). This remains relevant
to the multiplicity modules and their primitive trace quotients, but one must
distinguish its odd generator from the adjacent projected-wedge maps just
constructed. In the Ramond-sector notation of that paper,

$$
Q^1=\frac{1}{\sqrt2}\,\gamma\mathbin\cdot\alpha_{-1}.
$$

It commutes with the Lorentz algebra and raises oscillator level by one.
Precisely because it is a Lorentz scalar, it acts inside the Howe
multiplicity module of a fixed Lorentz irrep; it is not literally a map
$U_j\to U_{j+1}$ between distinct Lorentz irreducibles. The latter map is
$\sigma_j(v)$, where the vector creator acts on the physical module and the
projected wedge acts on the auxiliary gamma-traceless form. Confusing these
two actions would be circular.

The orthosymplectic operator nevertheless identifies the trace obstruction
on the multiplicity side:

$$
\{Q^1,Q^1\}=T^{11},
$$

where $T^{11}$ is the level-two bosonic trace-raising operator. Thus $Q^1$
organizes the primitive or trace quotient and may help identify the module on
which the projected-wedge resolution must be evaluated. It should not replace
that resolution. Passing to the trace quotient makes $Q^1$ nilpotent, but the
explicit null-vector calculation above warns that such a descent can have a
nonzero Tor fibre. The full five-term resolution retains the information
needed to compute it.

Moreover, $Q^1$ is defined before removal of the mode-one vector tower. Since
$\widehat G$ is the corresponding cumulative Koszul core, $Q^1$ cannot simply
be declared to act on $\mathfrak D^+(\widehat G)$. The correct operation is a
derived descent: act on the pre-core oscillator module, form the primitive or
Koszul complex, and calculate the induced map on its homology.

#### The gamma-trace transfer is explicit

There is now an exact answer to the first local part of that derived-descent
problem. Let

$$
A_p^\epsilon=\Lambda^p(V)\otimes S^\epsilon
$$

be the full space of chiral spinor-valued $p$-forms. Here $\epsilon$ is one
of the two `Spin(8)` chiralities and $\bar\epsilon$ denotes the other. On
these spaces introduce four elementary operators:

- $\Gamma$, contraction of one form index with a gamma matrix;
- $G$, exterior multiplication by the invariant gamma-valued one-form;
- $E_v$, exterior multiplication by a vector $v\in V$; and
- $C_v=\gamma(v)$, Clifford multiplication on the spinor factor.

The gamma-traceless module used above is

$$
U_p^\epsilon=\ker\bigl(\Gamma_p^\epsilon:
A_p^\epsilon\longrightarrow A_{p-1}^{\bar\epsilon}\bigr).
$$

For $0\leq p\leq4$ there is an exact direct-sum decomposition

$$
A_p^\epsilon
=U_p^\epsilon\mathbin\oplus G_{p-1}^{\bar\epsilon}
A_{p-1}^{\bar\epsilon}.
$$

Iterating it gives the full spinor-form triangle

$$
A_p^\epsilon\simeq
U_p^\epsilon\mathbin\oplus U_{p-1}^{\bar\epsilon}
\mathbin\oplus U_{p-2}^{\epsilon}\mathbin\oplus\cdots.
$$

The relevant dimensions are therefore

$$
A_4^\epsilon\simeq112\mathbin\oplus224\mathbin\oplus160
\mathbin\oplus56\mathbin\oplus8.
$$

This is not just a dimension decomposition. Direct Clifford algebra gives
the operator identities

$$
\Gamma_{p+1}^\epsilon E_v^\epsilon
+E_v^{\bar\epsilon}\Gamma_p^\epsilon=C_v^\epsilon,
$$

$$
\Gamma_{p+1}^{\bar\epsilon}G_p^\epsilon
-G_{p-1}^{\bar\epsilon}\Gamma_p^\epsilon
=(8-2p)\operatorname{id}_{A_p^\epsilon},
$$

$$
E_v^{\bar\epsilon}G_p^\epsilon
+G_{p+1}^\epsilon E_v^\epsilon=0,
$$

and

$$
C_v^{\bar\epsilon}G_p^\epsilon
+G_p^{\bar\epsilon}C_v^\epsilon=2E_v^\epsilon.
$$

The first formula is a Clifford-valued Cartan homotopy identity. It is the
finite algebraic analogue of the spinor-form relation used in higher-spin
Dirac complexes; compare the relation between the exterior derivative,
gamma contraction and the twisted Dirac operator in
[Bureš, arXiv:math/9901039](https://arxiv.org/abs/math/9901039). The sign in
that paper depends on its differential convention.

Define the trace Laplacian on $A_p^\epsilon$ by

$$
\Delta_p^\epsilon
=\Gamma_{p+1}^{\bar\epsilon}G_p^\epsilon.
$$

On the successive gamma-trace diagonals of the triangle its eigenvalues are

$$
\lambda_{p,j}=(j+1)(8-2p+j),
\qquad 0\leq j\leq p.
$$

For the four maps in the free resolution these spectra are

$$
(8),\qquad(6,14),\qquad(4,10,18),\qquad(2,6,12,20).
$$

They are all strictly positive. Thus the projection along the gamma-wedge
summand is not abstract: if $H_{p+1}$ denotes the coordinate of that summand,
then

$$
H_{p+1}=(\Gamma_{p+1}G_p)^{-1}\Gamma_{p+1}.
$$

In particular, on a gamma-traceless source $I_pU_p$ the trace leakage of
exterior multiplication is exactly

$$
H_{p+1}E_vI_p
=(\Gamma_{p+1}G_p)^{-1}C_vI_p.
$$

This formula is valid for every vector $v$ and contains no level-dependent
fit. The zero eigenvalue first appears on the leading diagonal at $p=4$.
That is precisely beyond the last outgoing map of the five-term resolution;
none of the four required transfers divides by it.

This calculation also resolves a possible shortcut. Let $I_p$ and $P_p$ be
the inclusion and projection for $U_p$, put $R_p=1-I_pP_p=G_{p-1}H_p$, and
define

$$
\sigma_p=P_{p+1}E_vI_p,
\qquad q_p=P_p'C_vI_p,
$$

where the prime means opposite chirality. The literal projected Clifford map
$q_p$ is not a chain map between the two gamma-traceless rows. Its defect is

$$
D_p=q_{p+1}\sigma_p-\sigma_p' q_p.
$$

Inserting $1=IP+R$ gives the exact factorization

$$
D_p=-P_{p+1}'C_vR_{p+1}E_vI_p
+P_{p+1}'E_vR_p'C_vI_p.
$$

Both terms pass through discarded gamma-trace spaces. The second term
vanishes identically by $E_vG+GE_v=0$, while the first reduces to

$$
\boxed{
D_p=-2P_{p+1}'E_v(\Gamma_{p+1}G_p)^{-1}C_vI_p.
}
$$

Hence the failure of the naive projected $Q^1$ action is neither numerical
nor an arbitrary representation mismatch: it is exactly the trace component
created by the projected-wedge differential. For a non-null vector the four
defect ranks are

$$
(8,48,112,112),
$$

and for a nonzero null vector they are

$$
(4,24,56,56).
$$

The result is the same for the two source chiralities. The full triangular
spinor-form complex restores the ambient identities exactly; only its top
gamma-traceless row loses them under projection. Thus a proof cannot simply
place $Q^1$ on the five $U_p$ modules. It must retain the trace diagonals, or
equivalently insert the displayed finite transfer terms before passing to
homology.

There is useful precedent but not a ready-made theorem for the remaining
step. Bureš supplies the relevant spinor-form homotopy algebra. Salač proves
formal exactness of $k$-Dirac resolutions by a relative-BGG double complex
and a spectral sequence
([arXiv:1705.09469](https://arxiv.org/abs/1705.09469),
[arXiv:1705.10168](https://arxiv.org/abs/1705.10168)); those complexes have
different parabolic data and do not by themselves identify the HFT massive
quotient. Likewise, the multiplicity-free orthogonal--orthosymplectic Howe
decomposition of the unreduced supersymmetric tensor algebra
([Cheng--Zhang, arXiv:math/0206036](https://arxiv.org/abs/math/0206036)) does
not prove compatibility with universal-supermultiplet division. These works
support the double-complex strategy, but applying it here remains a new
module-level statement.

The refined proof programme is now:

1. realize the orthosymplectic trace algebra and the uncontracted mode-one
   vector action on a pre-core physical multiplicity module whose character
   descends to $\mathcal M(q)=\mathfrak D^+(Z_m(q))$ after
   universal-supermultiplet division;
2. construct on that pre-core module the full spinor-form triangle with
   $E$, $\Gamma$, $G$ and $C=\sqrt2Q^1$, and prove that the trace ideal and
   universal-supermultiplet quotient respect its filtration;
3. filter by gamma-trace depth. The top diagonal is the five-term
   gamma-traceless resolution, while every off-diagonal differential is
   fixed by the invertible trace Laplacians displayed above;
4. prove that the resulting spectral sequence has no unwanted surviving
   homology and identify its two relevant edge terms with $\Pi_4$ and
   $\Pi_3$. This is equivalent to the $B_\Gamma$--$H_4$ prefix dominance of
   the same three-hook shell; and
5. identify the surviving Hilbert series with
   $A(q)=\sum_{N\geq9}a_Nq^N$.

The representation-theoretic symbol, its all-$k$ oriented extension, its
five-term free resolution, the Dirac-transformed Euler kernel, the full
gamma-trace triangle and its local transfer operators are now exact. What
remains open is the compatibility of this finite algebra with the HFT/DDF
multiplicity quotient and the resulting global homology concentration. The
audit has ruled out the unquotiented shortcut, a termwise Regge injection and
an uncorrected projected-$Q^1$ action. It has also replaced the earlier demand
for Tor vanishing by an explicit filtered derived tensor product whose local
transfer matrices are known.

The cumulative core gives a parallel way to organize Steps 1 and 2. One may
try to realize $Z_m/(1-q)$ as an actual module over the polynomial algebra on
$W=9$, with quotient or Koszul homology $\widehat G$. Proving that the nine
degree-one operations form a regular sequence would establish positivity of
$\widehat G$ at all orders and explain the cumulative completion
structurally. It would not by itself prove the adjacent
$\Pi_4\to\Pi_3$ dominance, because those series are not raw exterior-form
multiplicities of $\widehat G$ in the finite scan. The projected-wedge
resolution must still be combined with the orthosymplectic trace algebra to
identify the refined primitive slices.

## 6. What has and has not been proved

The original scalar-tail assertion

$$
a_N\geq0\qquad(N\geq9)
$$

is now exactly equivalent to

$$
[q^N]\Phi_q(G(q))\leq0\qquad(N\geq9),
$$

where $G$ is the explicit oscillator telescope and $\Phi$ is given by the
nine-row table.  This is a genuine all-orders reduction: neither the number
of rays nor their transverse labels grow with $N$.

More strongly, it is equivalent to the fixed `B4` inequality

$$
[q^N]\left\langle\mathscr C(q),Z_m(q)\right\rangle_{B_4}\leq0,
\qquad N\geq9,
$$

whose kernel has degree five and involves only the first five exterior powers
of the vector $9$. The two primitive inversions reduce this further to

$$
\pi_3(N)\geq\pi_4(N-1),
\qquad N\geq9.
$$

The cumulative completion also has the exact factorization

$$
\frac{Z_m(q)}{1-q}=\operatorname{PE}(q9)\widehat G(q),
$$

where $\widehat G$ is a canonical $B_4$ character series whose restriction
is $G$. Its coefficients are positive through degree 20. This is strong
evidence for a cumulative Koszul/DDF module, but neither that positivity nor
the required regular-sequence realization has yet been proved at all orders.
Moreover, $\Pi_3$ and $\Pi_4$ are not raw low-form multiplicities of this
core in the finite comparison, so the adjacent-map problem remains genuine.
On the other hand, moving the cumulative vector tower through the functional
does give an exact all-orders reduction to the three principal hook families
$(k)$, $(k,1)$ and $(k,1,1)$. This supplies a smaller direct
orthosymplectic-multiplicity target alongside the $\Pi_4\to\Pi_3$ complex.
Relative Dirac orientation strengthens the local part of that target: the
three hook families become the gamma-traceless $D_4$ families
$[k,0,1,0]$, $[k-1,1,1,0]$ and $[k-1,0,2,1]$, and their vector symbol is an
injective map of free $\operatorname{Sym}(8_v)$-modules for every $k$. The
five low-form modules further form an exact free resolution of the positive
tower $\bigoplus_{n\geq0}[n,0,3,0]$. The truncated Tor group displayed above
is generally nonzero on the null or trace quotient, but is computed by this
full resolution rather than left as an unspecified obstruction. Its pairing
with the positive core is the series $B_\Gamma$, and the scalar theorem is
exactly the displayed prefix dominance between $B_\Gamma$ and $H_4$.
The naive projected Clifford action does not commute with the projected-wedge
differential: its non-null defect ranks are $(8,48,112,112)$ and its null
defect ranks are $(4,24,56,56)$. This obstruction is now completely
localized. It factors through the discarded gamma-trace summand, and the
trace coordinate is the explicit operator
$(\Gamma G)^{-1}C_v$. The trace-Laplacian spectra needed by the four maps are
$(8)$, $(6,14)$, $(4,10,18)$ and $(2,6,12,20)$, so no singular inverse is
being assumed. The full spinor-form triangle restores all ambient Clifford
and Koszul identities exactly.
Correct outer orientation turns the prefix kernel back into
$\mathfrak D^+(R_{n+1}-R_n)$, so this is the same virtual three-hook shell in
derived form, not a coefficientwise-positive replacement. At the same time,
108 negative first-row differences in the tested Bars
triangle rule out a coefficientwise Regge injection. Any successful map must
therefore use the mass grading and the first-row grading together.

It is not yet the desired sign proof. Individual telescope pivots have both
signs, so a termwise-pivot positivity argument is false. Through degree 20,
the exact pre-telescope coefficients are

$$
1,1,0,0,1,1,0,0,0,-1,-2,-2,-3,-8,-18,-29,
$$

$$
-47,-81,-139,-226,-372.
$$

The negatives from degree nine reproduce

$$
A(q)=q^9+2q^{10}+2q^{11}+3q^{12}+8q^{13}
+18q^{14}+\cdots.
$$

These additional coefficients are evidence and diagnostics, not part of the
proof.

The next proof attempt is now more precise. The raw transverse Koszul map has
the correct bidegree but is not injective: its kernel is the image from
exterior degree five. Relative Dirac descent replaces the raw source by the
gamma-traceless tower $U_0,\ldots,U_4$. Its projected vector maps form an
exact polynomial resolution with positive cokernel
$\bigoplus_n[n,0,3,0]$, while its reverse top map is injective. What remains
is to realize the *whole resolution* on the mass-graded
$\mathfrak D^+(Z_m)$ multiplicity module together with its gamma-trace
diagonals. The newly explicit transfer formula determines every local
off-diagonal correction, so the remaining question is no longer how to guess
a map. It is whether universal-supermultiplet division preserves the
gamma-trace filtration and whether the resulting spectral sequence is
concentrated in the two edge terms $\Pi_4$ and $\Pi_3$. Equivalently, one may
prove the exact prefix dominance between $B_\Gamma$ and $H_4$. Its correctly
oriented prefix is the same virtual three-hook shell already isolated above,
so the complex must be used at module level rather than merely through its
Euler character. The fixed-$L$ Plücker and wall--curvature pictures remain
exact derivations and may help prove that concentration. More low-level Bars
or protected uplift data would not settle the theorem.

Once that sign theorem is established, the same method must be repeated for
the five non-scalar coordinates of $A_0$ and for boundary births outside its
support.  Stable `D5` Pieri translation already handles the upper chamber.
The remaining Bars theorem is therefore analytic effort on finitely many
boundary functionals, not a request for more protected low-level data.

## 7. A tempting shortcut that fails

The Dirac-folded images of the four `D4` fundamental characters admit simple
`D5` lifts.  Extending those four assignments multiplicatively looks like a
possible closed lift of the whole oscillator product.  It is not: Dirac
folding is additive but not a representation-ring homomorphism.

The multiplicative extension agrees with the triangular construction through
degree three and differs at degree four only by $J$.  At degree five its
restriction already differs from the required `B4` character.  This is an
exact obstruction, so the multiplicative shortcut is discarded rather than
repaired with baseline data.

## Reproduction

```text
./bin/sage-run -m trajectory_kernel.scalar_tail --maximum-degree 20
./bin/sage-run -m trajectory_kernel.scalar_boundary_functional --maximum-degree 15 --audit-label-sum 9
./bin/sage-run -m trajectory_kernel.ddf_koszul_audit --maximum-degree 20
./bin/sage-run -m trajectory_kernel.gamma_symbol_complex --self-test
./bin/sage-run -m trajectory_kernel.multiplicative_core --self-test
```
