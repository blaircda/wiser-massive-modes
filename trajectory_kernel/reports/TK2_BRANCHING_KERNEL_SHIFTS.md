# TK2 — Branching and Restriction-Kernel Shift Identities

**Status:** complete on the HFT level-1--10 finite closure, with an exact
branching identity  
**Provenance:** baseline-free  
**Last updated:** 23 September 2026

## Result

TK2 finds that the naive leading-label shift does **not** commute with
$D_5\downarrow B_4$ restriction. It differs by a positive, multiplicity-free
lower-boundary character. Once that boundary term is lifted on the fixed
all-chiral section, every tested kernel generator advances exactly to the next
generator on its trajectory.

Thus the useful structure is a **boundary-corrected Regge shift**, not a raw
shift symmetry.

No protected $SO(10)$ spectrum is imported anywhere in this calculation.

## 1. Exact branching-column identity

Let $\sigma_D$ increase the first $D_5$ Dynkin label by one, and let
$\sigma_B$ increase the first $B_4$ Dynkin label by one:

$$
\sigma_D[a_1,a_2,a_3,a_4,a_5]
=[a_1+1,a_2,a_3,a_4,a_5],
$$

$$
\sigma_B[\ell,m,r,s]=[\ell+1,m,r,s].
$$

The multiplicity-free orthogonal branching rule interlaces the $D_5$
orthogonal coordinates $\lambda_i$ with the $B_4$ coordinates $\mu_i$.
Increasing $a_1$ raises $\lambda_1$ by one and leaves
$\lambda_2,\ldots,\lambda_5$ fixed. Therefore

$$
\operatorname{Res}(\sigma_D V_\lambda)
=\sigma_B\operatorname{Res}(V_\lambda)+\partial(V_\lambda),
$$

where $\partial(V_\lambda)$ is the sum of the interlacing $B_4$ irreps on the
lower slice

$$
\mu_1=\lambda_2.
$$

Consequently the boundary character is nonnegative, multiplicity-free and
independent of $a_1$. This is an exact consequence of the interlacing rule,
not an empirical claim about the Bars spectrum.

The implementation verifies the identity on all 65 $D_5$ parent columns in
the level-10 finite domain. All anomalies are nonnegative and
multiplicity-free, all lie on $\mu_1=\lambda_2$, and all 13 repeated fixed-tail
groups give identical anomalies for different values of $a_1$.

## 2. Exact finite kernel lattice

The baseline-free HFT cumulative spectra through level 10 generate a full
positive-chirality branching closure with:

| Object | Count |
| --- | ---: |
| $B_4$ row weights | 57 |
| Inequivalent positive-chirality $D_5$ parent columns | 65 |
| Restriction-matrix rank | 57 |
| Restriction-kernel rank | 8 |

The 57 all-chiral reference columns have determinant one. For each of the
eight non-reference parents, subtracting the unique all-chiral lift of its
restriction gives an integral kernel generator

$$
K_P=P-s_{\mathrm{ch}}(\operatorname{Res}P).
$$

Each generator has coefficient one on a distinct non-reference parent and
uses only reference parents otherwise. The eight generators are therefore an
integral triangular basis of the kernel of this finite $57\times65$
restriction matrix, not merely a rational nullspace basis.

This is a statement about the stated finite closure. It does not assert that
the full representation-ring kernel has rank eight.

## 3. Relation controlling the 126/210 ambiguity

The generator over the $B_4$ top weight $[0,0,0,2]_9$ is

$$
K^{(2)}_0
=[0,0,0,1,1]_{10}-[0,0,0,0,2]_{10}
-[0,0,1,0,0]_{10}+[0,1,0,0,0]_{10}
-[1,0,0,0,0]_{10}+[0,0,0,0,0]_{10}.
$$

In dimensions, with the chirality convention used here, this is the virtual
identity

$$
210-126-120+45-10+1,
$$

and its restriction to $SO(9)$ is exactly zero. This is the canonical
six-term generator relative to the all-chiral section underlying the earlier
126/210 choice: within this section, replacing one parent by the other brings
the four displayed lower $SO(10)$ terms with it.

## 4. Boundary-corrected kernel shift

For a kernel relation $K$, the raw shift generally fails to remain in the
kernel:

$$
\operatorname{Res}(\sigma_DK)=\partial K.
$$

Let $s_{\mathrm{ch}}$ denote the fixed all-chiral section. The corrected shift

$$
T(K)=\sigma_DK-s_{\mathrm{ch}}(\partial K)
$$

does restrict to zero. More strongly, if $K_\mu$ is the natural generator
over the top weight $\mu$, triangular uniqueness gives the exact recurrence

$$
K_{\sigma_B\mu}=T(K_\mu).
$$

For the eight finite-domain generators the computation finds:

| Test | Result |
| --- | ---: |
| Raw shifted generators still in the kernel | 0 / 8 |
| Boundary-corrected shifts in the kernel | 8 / 8 |
| Corrected shifts equal the next natural generator | 8 / 8 |

The raw shift failure is therefore systematic, but so is its correction.

## 5. Three observed kernel trajectories

The eight generators in the finite closure lie in three fixed-tail families.

### Family A: top weights $[\ell,0,0,2]_9$

Five generators occur for $0\leq\ell\leq4$. Their first HFT appearances all
have reduced depth

$$
\delta=n-\ell-3m=6.
$$

Their exact recurrence is

$$
K^{(2)}_{\ell+1}
=\sigma_DK^{(2)}_\ell
-\left([1,0,0,0,0]_{10}-[0,0,0,0,0]_{10}\right).
$$

### Family B: top weights $[\ell,1,0,2]_9$

Two generators occur for $\ell=0,1$, again at $\delta=6$. The seed is

$$
L^{(2)}_0
=[0,1,0,1,1]_{10}-[0,1,0,0,2]_{10}
-[0,1,1,0,0]_{10}+[0,2,0,0,0]_{10}
+[1,0,0,0,0]_{10}-[2,0,0,0,0]_{10},
$$

and

$$
L^{(2)}_{\ell+1}
=\sigma_DL^{(2)}_\ell
-\left([2,0,0,0,0]_{10}-[1,0,0,0,0]_{10}\right).
$$

### Family C: top weights $[\ell,0,0,3]_9$

Only the $\ell=0$ seed occurs by level 10, at $\delta=10$:

$$
K^{(3)}_0
=[0,0,0,1,2]_{10}-[0,0,0,0,3]_{10}
-[0,0,1,0,1]_{10}+[0,1,0,0,1]_{10}
+[0,0,0,0,1]_{10}-[1,0,0,0,1]_{10}.
$$

Its exact algebraic continuation is

$$
K^{(3)}_{\ell+1}
=\sigma_DK^{(3)}_\ell
-\left([1,0,0,0,1]_{10}-[0,0,0,0,1]_{10}\right).
$$

The continuation is an identity of branching and the chosen section. Whether
the corresponding top weights enter the HFT spectrum with a useful physical
multiplicity beyond level 10 is a separate question.

## 6. Meaning for the programme

TK2 gives a more structured answer than a raw order-by-order lift:

- the level-6/7 126/210 ambiguity is one explicit kernel seed;
- its higher-leading-spin analogues are generated by a fixed corrected-shift
  recurrence;
- seven of the eight finite generators occupy two families at the same
  reduced depth $\delta=6$;
- a third family begins at $\delta=10$;
- raw shift covariance is false, so any future ansatz must carry the boundary
  correction explicitly.

What remains open is whether new fixed-tail seed families proliferate at
higher HFT levels and which integral combinations of these generators produce
positive cumulative lifts. Those are the appropriate TK3 questions.

## Reproduction

```text
./bin/sage-run -m trajectory_kernel.kernel_lattice --self-test
./bin/sage-run -m trajectory_kernel.kernel_lattice --max-level 10
./bin/sage-run -m trajectory_kernel.kernel_lattice --max-level 10 --verbose
```

The verbose run prints all eight six-term kernel relations and every boundary
correction. A fresh full run takes roughly one to two minutes because Sage must
compute the shifted branching columns.
