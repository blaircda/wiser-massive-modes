# GU3 — Type-IIA Closed Refinement

**Status:** complete through level 7 in the resolved finite domain  
**Last updated:** 24 September 2026

## 1. Motivation and scope

The grading tested in GU1--GU2 comes from type-IIB string theory on
$AdS_5\times S^5$. That construction tensors two identical chiral spectra.
Type IIA instead has opposite left/right Ramond chirality, and Bars' proposal
is specifically an IIA/M-theory proposal in which additional nonperturbative
states complete eleven-dimensional $SO(10)$ multiplets.

GU3 tests the minimal representation-theoretic IIA modification:

1. outer-conjugate the right $D_5$ factor;
2. retain the left and right oscillator gradings separately;
3. retain Bars' nonperturbative label
   $\ell'=n-\ell$ separately in each sector;
4. compare the resulting closed character with the protected Bars completion
   only in a separate comparison module.

This does not assert that the IIB conformal dimension $\Delta$ has a direct
IIA interpretation. It asks whether the chirality-corrected algebraic grading
can nevertheless resolve the Bars ambiguity.

## 2. Opposite chirality and the axial grading

Let $\tau$ be the $D_5$ outer automorphism

$$
\tau[a_1,a_2,a_3,a_4,a_5]
=[a_1,a_2,a_3,a_5,a_4].
$$

Let $\sigma$ exchange the two $D_4$ spinor nodes. Exact charged branching
gives

$$
\Phi_{-}(\tau V)=\sigma\Phi_{-}(V),
$$

where $\Phi_{-}$ uses

$$
\nu=\Delta-J.
$$

Equivalently, without conjugating the right $D_5$ label, the right-moving map
uses

$$
\nu_R=\Delta_R+J_R.
$$

Thus the IIA closed grading is

$$
\nu_L+\nu_R
=\Delta_L+\Delta_R-(J_L-J_R),
$$

rather than the IIB diagonal combination involving $J_L+J_R$.

The transcribed paper candidate satisfies both equivalent right-sector tests
exactly at every level 1--7:

- conjugate the $D_5$ labels and retain $\nu=\Delta-J$;
- retain the labels and use $\nu=\Delta+J$.

## 3. Bars' nonperturbative level

At fixed mass level $n$, Bars introduces

$$
n=\ell+\ell',
$$

with

$$
(\ell',\ell)=(0,n),(1,n-1),\ldots,(n-1,1).
$$

GU3 therefore stores every source block under

$$
(\ell',\nu)=(n-\ell,\nu)
$$

before summing. The right block is its $D_4$ chirality conjugate. Every left
and right block agrees exactly with the independently derived refined
oscillator spectrum through mass level 7.

Forgetting $\ell'$ gives the cumulative paper character. It is positive and
has the required cumulative HFT $SO(9)$ restriction at every tested level.

## 4. Injectivity of the resolved grading

For each oscillator level, GU3 constructs the complete `outer-closed` finite
candidate domain from GU2 and computes the exact rank over $\mathbb Q$ of the
map to the full $\nu$-graded $D_4$ character.

| Level | Rows | Candidate columns | Rank |
| ---: | ---: | ---: | ---: |
| 1 | 4 | 3 | 3 |
| 2 | 14 | 9 | 9 |
| 3 | 37 | 22 | 22 |
| 4 | 81 | 46 | 46 |
| 5 | 158 | 88 | 88 |
| 6 | 289 | 159 | 159 |
| 7 | 489 | 269 | 269 |

Every map has full column rank. Because $\ell'$ is retained, the cumulative
chiral map is a direct sum of these injective maps. At horizons 6 and 7 its
ranks are respectively

$$
327/327
$$

and

$$
596/596.
$$

Retaining the separate left and right labels makes the closed map their tensor
product. Its ranks are therefore

$$
106929/106929
$$

at horizon 6 and

$$
355216/355216
$$

at horizon 7.

Consequently the fully resolved closed target has a unique preimage in this
finite tensor-product domain. Since the target factorizes into the verified
left and right oscillator characters, that preimage is precisely the paper
candidate tensored with its outer conjugate. Allowing general non-factorized
coefficients does not introduce additional freedom here.

## 5. Protected comparison with Bars

Let $P_n$ be the positive cumulative paper character and $B_n$ the protected
Bars character. The two natural IIA closed candidates are

$$
C_n^{\mathrm{paper}}=P_n\otimes\tau(P_n)
$$

and

$$
C_n^{\mathrm{Bars}}=B_n\otimes\tau(B_n).
$$

| Level | $P_n=B_n$ | $C_n^{\mathrm{paper}}=C_n^{\mathrm{Bars}}$ | Difference terms | Difference coefficient range |
| ---: | ---: | ---: | ---: | ---: |
| 1--5 | yes | yes | 0 | -- |
| 6 | no | no | 64 | $[-4,4]$ |
| 7 | no | no | 140 | $[-8,4]$ |

Both closed candidates are positive integral $SO(10)$ characters and have the
same dimension and closed $SO(9)$ restriction. Their difference is nonzero,
outer-even and restricts to zero.

Writing

$$
K_n=P_n-B_n,
$$

the level-6 and level-7 chiral discrepancies satisfy

$$
\tau(K_n)=-K_n.
$$

The closed discrepancy obeys the exact factorization

$$
C_n^{\mathrm{paper}}-C_n^{\mathrm{Bars}}
=K_n\bigl(\tau(P_n)-B_n\bigr).
$$

Thus opposite-chirality pairing converts the outer-odd chiral ambiguity into
an outer-even closed restriction-kernel element; it does not cancel it.

## 6. Conclusion

GU3 establishes a solid link with the standard IIA structure:

- left and right sectors have opposite chirality;
- the right grading is axial, $\nu_R=\Delta_R+J_R$;
- Bars' $\ell'$ label explains why lower oscillator levels accumulate at a
  fixed mass level;
- the closed candidate is naturally outer-invariant.

But these facts do not select the protected Bars completion. If the full
IIB-derived oscillator grading is retained separately, it is so rigid that it
uniquely selects the paper candidate even after passing to the IIA closed
sector.

This sharpens the conceptual boundary: $\ell'$ and the D0/Kaluza--Klein charge
$W$ are genuine IIA/M-theory data, whereas $\Delta-J=\nu$ is an additional
AdS/IIB condition. A genuinely IIA selector should therefore be sought in a
direct closed construction using $(\ell',W)$ and the intrinsic positive closed
supermultiplet, without requiring each chiral factor to carry the IIB
$\Delta$ grading.

## 7. Reproduction

```text
./bin/sage-run -m graded_uplift.iia_closed_refinement --self-test
./bin/sage-run -m graded_uplift.iia_closed_refinement --max-level 7
./bin/sage-run -m graded_uplift.verify_iia_closed_against_baseline --max-level 7 --verbose
```

`iia_closed_refinement.py` is baseline-free. The protected completion is
imported only by `verify_iia_closed_against_baseline.py`.
