# TK6a — The Principal Restriction-Kernel Ideal

**Status:** exact global representation-ring presentation implemented; finite
kernel quotients classified through baseline-free HFT level 11

**Provenance:** baseline-free

**Last updated:** 25 September 2026

## Result

Let

$$
\operatorname{Res}:R(\operatorname{Spin}(10))\longrightarrow
R(\operatorname{Spin}(9))
$$

be restriction and define

$$
J=16_+-16_-.
$$

The standard fundamental-character presentation gives the exact global ring
identity

$$
\ker(\operatorname{Res})=(J).
$$

The new implementation converts arbitrary finite $D_5$ characters to
polynomials in the five fundamental characters, divides kernel characters by
$J$, and verifies the result back in the Weyl character ring.

Applied to the complete natural kernel basis in the baseline-free level-11
closure, all eleven generators divide exactly by $J$. More strongly, every
quotient is a positive integral $SO(10)$ character with unit coefficients.
The quotients obey three simple finite-window partial-sum formulas:

$$
\frac{A_\ell}{J}
=\sum_{i=0}^{\ell}[i,0,0,0,1],
\qquad 0\leq\ell\leq5,
$$

$$
\frac{B_\ell}{J}
=\sum_{i=0}^{\ell}
\left([i+1,0,0,0,1]+[i,1,0,0,1]\right),
\qquad 0\leq\ell\leq2,
$$

$$
\frac{C_\ell}{J}
=\sum_{i=0}^{\ell}[i,0,0,0,2],
\qquad 0\leq\ell\leq1.
$$

Every equality in these stated ranges is checked exactly. The displayed
formulas are natural candidates for all-$\ell$ identities, but the finite
agreement is not by itself an all-orders proof.

## 1. Global polynomial presentation

Write $f_1,\ldots,f_5$ for the five fundamental $D_5$ characters and
$b_1,\ldots,b_4$ for the four fundamental $B_4$ characters. Exact branching
gives

$$
f_1\longmapsto1+b_1,
$$

$$
f_2\longmapsto b_1+b_2,
$$

$$
f_3\longmapsto b_2+b_3,
$$

$$
f_4\longmapsto b_4,
$$

$$
f_5\longmapsto b_4.
$$

The map is surjective. One polynomial right inverse is

$$
b_1\longmapsto f_1-1,
$$

$$
b_2\longmapsto f_2-f_1+1,
$$

$$
b_3\longmapsto f_3-f_2+f_1-1,
$$

$$
b_4\longmapsto f_5.
$$

After subtracting this section, every polynomial is divisible by

$$
f_4-f_5.
$$

Since $f_4$ and $f_5$ are the two half-spinor characters, this proves the
principal kernel presentation. The code verifies both the restriction map and
the polynomial right inverse exactly.

## 2. Exact conversion to fundamental-character polynomials

For a dominant $D_5$ label

$$
\lambda=[a_1,a_2,a_3,a_4,a_5],
$$

the product

$$
f_1^{a_1}f_2^{a_2}f_3^{a_3}f_4^{a_4}f_5^{a_5}
$$

contains $V_\lambda$ as its Cartan component with multiplicity one. All other
components are lower in dominance order. Recursive triangular subtraction
therefore expresses every finite virtual character exactly as a polynomial in
the $f_i$.

The implementation checks every conversion by evaluating the polynomial back
in the Sage Weyl character ring. No numerical character evaluation or
floating-point reconstruction is used.

## 3. Quotients of the level-11 natural kernel basis

The exact quotient table is:

| Generator | First HFT level | $K/J$ terms | Minimum/maximum coefficient | Positive? |
| --- | ---: | ---: | ---: | --- |
| $A_0$ | 6 | 1 | 1 / 1 | yes |
| $A_1$ | 7 | 2 | 1 / 1 | yes |
| $A_2$ | 8 | 3 | 1 / 1 | yes |
| $A_3$ | 9 | 4 | 1 / 1 | yes |
| $A_4$ | 10 | 5 | 1 / 1 | yes |
| $A_5$ | 11 | 6 | 1 / 1 | yes |
| $B_0$ | 9 | 2 | 1 / 1 | yes |
| $B_1$ | 10 | 4 | 1 / 1 | yes |
| $B_2$ | 11 | 6 | 1 / 1 | yes |
| $C_0$ | 10 | 1 | 1 / 1 | yes |
| $C_1$ | 11 | 2 | 1 / 1 | yes |

Only the two nontransported seeds have irreducible quotients:

$$
A_0=16_-J,
$$

$$
C_0=126_-J.
$$

Thus the two TK5b seeds are not algebraically independent generators of the
global restriction kernel. They are different positive multiples of the same
principal generator. Their distinct roles in the finite positivity problem
come from the positive semiring and from where their top weights enter the HFT
spectrum, not from independent ring-kernel directions.

## 4. Interpretation

TK6a changes the useful coordinates for the existence problem. After choosing
any virtual section $s$, every lift can be written as

$$
X_n=s(R_n^9)+JH_n.
$$

The finite trajectory generators correspond to positive candidate directions
in the auxiliary character $H_n$. In the tested window, the corrected
trajectory shifts simply lengthen the positive partial sums displayed above.

This is encouraging but does not prove Bars III.B positivity. Multiplication
by the virtual character $J$ introduces both signs, and a positive quotient
$H$ does not imply that either

$$
s(R_n^9)+JH
$$

or

$$
s(R_n^9)-JH
$$

is positive. The positive restriction fibre remains a semiring problem. TK6b
will study that problem directly through the interlacing-packet cone.

## 5. Limits and next questions

- The principal-ideal statement is global in the representation ring.
- Positivity of all eleven displayed quotients is established only for the
  natural finite generators present through HFT level 11.
- The partial-sum formulas have not yet been proved for arbitrary $\ell$.
- No protected $SO(10)$ completion is imported.
- No preferred chirality orientation is inferred from the choice
  $J=16_+-16_-$. Reversing convention changes the signs of $J$ and the
  corresponding quotients together.

The next useful algebraic question is whether the three partial-sum formulas
follow from an exact all-$\ell$ tensor-product identity. The next central
existence question is independent: characterize which $SO(9)$ multiplicity
functions are nonnegative sums of $D_5\downarrow B_4$ interlacing packets.

## Reproduction

```text
./bin/sage-run -m trajectory_kernel.principal_ideal --self-test
./bin/sage-run -m trajectory_kernel.principal_ideal --max-level 11
./bin/sage-run -m trajectory_kernel.principal_ideal --max-level 11 --verbose
```

The full level-11 run takes approximately one minute in the current
environment.
