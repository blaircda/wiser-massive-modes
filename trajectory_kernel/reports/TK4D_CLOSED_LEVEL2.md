# TK4d — Exact Closed-String Level-2 Test

**Status:** completed baseline-free level-2 calculation

**Provenance:** baseline-free

**Last updated:** 23 September 2026

## Result

The positive closed-string universal supermultiplet exists exactly as
expected, but it is not obtained by tensoring the present virtual chiral
$SO(10)$ uplifts.

Define the intrinsic closed factor by the fermionic Fock representation

$$
Q_{\mathrm{cl}}=\bigoplus_{j=0}^{16}\Lambda^j\mathbf{16}.
$$

The exact computation finds:

$$
\dim Q_{\mathrm{cl}}=2^{16}=65{,}536;
$$

$Q_{\mathrm{cl}}$ is a positive integral $SO(10)$ character with 23
irreducible terms; it is invariant under interchange of the two $D_5$ spinor
nodes; and

$$
\operatorname{Res}_{SO(10)\to SO(9)}Q_{\mathrm{cl}}
=(Z_Q^9)^2.
$$

Thus the basic positive closed supermultiplet is confirmed independently.

However, let $z=Z_Q^{10}$ denote the virtual single-chiral HFT uplift and let
$\tau$ exchange the two spinor nodes. Neither raw tensor-product uplift agrees
with the intrinsic factor:

$$
z^2\neq Q_{\mathrm{cl}},
$$

$$
z\,\tau(z)\neq Q_{\mathrm{cl}}.
$$

Both differences restrict to zero. The discrepancy therefore appears already
at the universal level, before considering excited massive characters.

At level 2, neither raw closed numerator is divisible by the positive factor:

$$
Q_{\mathrm{cl}}\nmid N_2^2,
$$

$$
Q_{\mathrm{cl}}\nmid N_2\tau(N_2).
$$

These are exact nondivisibility results in the injective five-variable Laurent
weight ring.

## 1. Positive closed factor

The complete decomposition produced by the calculation is

$$
Q_{\mathrm{cl}}=
2[0,0,0,0,0]+[0,0,0,1,0]+[0,0,0,0,1]
+2[0,0,1,0,0]+[0,1,0,1,0]+[0,1,0,0,1]
+[0,0,0,3,0]+[0,0,0,0,3]
$$

$$
{}+[1,0,0,2,0]+[1,0,0,0,2]
+2[0,2,0,0,0]+[0,1,0,2,0]+[0,1,0,0,2]
+[0,0,2,0,0]
$$

$$
{}+[1,1,0,1,0]+[1,1,0,0,1]
+[1,0,1,1,0]+[1,0,1,0,1]
+2[2,0,1,0,0]+[2,0,0,1,1]
$$

$$
{}+[3,0,0,1,0]+[3,0,0,0,1]+[4,0,0,0,0].
$$

Every coefficient is nonnegative. The displayed pairing of conjugate terms
also makes its outer-chirality invariance manifest.

## 2. Raw chiral tensor products

The literal same-chirality product $z^2$ contains 35 irreducible terms, of
which 12 have negative coefficients; its minimum coefficient is $-8$.

The opposite-chirality product $z\tau(z)$ contains 36 irreducible terms, of
which 11 have negative coefficients; its minimum coefficient is $-10$.

Both have the correct dimension and the correct $SO(9)$ restriction, but
neither is the positive closed representation. Explicitly,

$$
z^2-Q_{\mathrm{cl}}\in\ker(\operatorname{Res}),
$$

$$
z\tau(z)-Q_{\mathrm{cl}}\in\ker(\operatorname{Res}).
$$

This corrects the preliminary assumption that positivity of the full factor
could be tested using the literal product of the chosen chiral virtual
uplifts. Combining left and right after that uplift is not the same operation
as lifting the combined closed supermultiplet.

## 3. Level-2 numerator test

Let $r_2^9$ be the independently derived single-chiral $SO(9)$ quotient. Both
raw level-2 products have the required restriction

$$
\operatorname{Res}(N_2^2)
=(Z_Q^9)^2(r_2^9)^2,
$$

and

$$
\operatorname{Res}(N_2\tau(N_2))
=(Z_Q^9)^2(r_2^9)^2.
$$

Choose any reference lift $X_2^{\mathrm{ref}}$ of $(r_2^9)^2$ and define

$$
\Delta_2^{(+)}=N_2^2-Q_{\mathrm{cl}}X_2^{\mathrm{ref}},
$$

$$
\Delta_2^{(-)}=N_2\tau(N_2)-Q_{\mathrm{cl}}X_2^{\mathrm{ref}}.
$$

Both remainders have dimension zero and restrict to zero. Their irreducible
supports contain respectively 108 and 76 terms.

Exact Laurent division gives a nonzero remainder in both cases:

| Chiral product | Divisible by $Q_{\mathrm{cl}}$? | Laurent remainder terms |
| --- | --- | ---: |
| $N_2^2$ | no | 204,762 |
| $N_2\tau(N_2)$ | no | 195,815 |

The difference between the same- and opposite-chirality level-2 numerators is
also not divisible by $Q_{\mathrm{cl}}$. Their obstruction classes are
therefore distinct modulo
$Q_{\mathrm{cl}}\ker(\operatorname{Res})$.

## 4. Interpretation

The calculation rules out the simplest proposed cure:

> First uplift each chiral HFT numerator using the virtual $SO(10)$ formula,
> then tensor the two uplifts and divide by the positive closed
> supermultiplet.

That order of operations fails already at level 1, where it gives the wrong
$SO(10)$ lift of the universal factor, and neither chirality choice becomes
divisible at level 2.

It does **not** rule out the more interesting possibility that the full closed
theory possesses a direct $SO(10)$ construction. Such a construction must
combine the left and right sectors before making the $SO(10)$ uplift and must
produce $Q_{\mathrm{cl}}$, rather than $z^2$ or $z\tau(z)$, at level 1.

The positive closed factor is therefore informative: it tells us that the
restriction-kernel correction is required already in defining the universal
closed lift. The next question is whether the full level-matched HFT series has
an intrinsic $SO(10)$ uplift normalized by $Q_{\mathrm{cl}}$. Merely tensoring
the existing chiral uplift cannot answer that question.

## Reproduction

```text
./bin/sage-run -m trajectory_kernel.closed_level2 --self-test
./bin/sage-run -m trajectory_kernel.closed_level2
```

The full exterior-algebra decomposition and Laurent division can take one to
two minutes.
