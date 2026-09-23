# Project Status

**Last updated:** 23 September 2026

This is the central status document for the Bars massive-modes project. It is
intended to distinguish established results, reproducible computations,
conditional statements, and open problems. When an older report conflicts with
this file, this file records the current project position.

## Protected Baseline

The following human-established verification files are read-only and must never
be used as inputs to a script claiming an independent derivation:

- `massive_SO10.py`
- `massive_SO8_construct.py`
- `massive_SO8_to_S010.py`
- `massive_SO8_to_SO9.py`

They encode the known level-1--10 result and are used only by explicitly named
verification scripts.

## Current Mathematical Status

### Bars III.B through level 10

The cumulative spectra

$$
R_n=\sum_{i=1}^n r_i
$$

are recorded in the protected baseline as positive integral $SO(10)$ characters
for levels 1 through 10. This is the finite-level result to be explained, not an
input permitted in first-principles derivations.

### HFT $SO(9)$ reconstruction

**Status: independently derived and separately benchmarked through level 10.**

`hft_so9.py` constructs the Hanany--Forcella--Troost numerator in $SO(9)$ and
performs character division by the positive universal massive supermultiplet
$Z_Q$. It imports no protected baseline file. At every level 1--10:

- the quotient is a positive integral $SO(9)$ character;
- the exact identity $N_n=Z_Q r_n$ holds.

`verify_hft_so9_against_baseline.py` is a separate comparison layer. It verifies
that the independently derived $r_n$ agree with consecutive differences of the
protected cumulative spectrum after restriction to $SO(9)$. All levels 1--10
match exactly.

### HFT virtual $SO(10)$ numerator uplift (M3)

**Status: verified through level 10.**

`hft_so10_uplift.py` constructs the virtual $SO(10)$ numerator using
$V_{10}=\mathbf{10}-2\mathbf{1}$ and does not import the protected baseline. The
coefficient-by-coefficient restriction identity

$$
\operatorname{Res}_{SO(10)\to SO(9)}N_n^{10}=N_n^9
$$

has been verified exactly for levels 1--10.

This is a finite-order identity for the virtual numerator. By itself it does not
derive the positive Bars $SO(10)$ spectrum.

### Direct $SO(10)$ quotient reconstruction (M4)

**Status: unresolved; the previously claimed pass is withdrawn.**

The proposed highest-weight division by the virtual character $Z_Q^{10}$ is not
monotone. The repaired diagnostic is exact at level 1 but cannot complete the
proposed quotient at level 2. It stops at this first obstruction by default and
has hard repetition and step limits for optional deeper experiments.

The separate script `verify_hft_so10_against_baseline.py` substitutes the known
baseline single-level lifts for comparison only. It finds:

- exact agreement after restriction to $SO(9)$ through level 10;
- a nonzero $SO(10)$ remainder at every level 2--10;
- every such remainder has dimension zero and restricts to zero in $SO(9)$.

Thus the known spectrum is compatible with the HFT numerator only modulo the
restriction kernel. This comparison is not a derivation and does not establish
that no alternative exact quotient exists in the full representation ring.

### All-orders positivity

**Status: open.**

No current script or report proves that $R_n$ is a positive $SO(10)$ character
for all levels. Leading-Regge identities and finite-level data provide evidence,
but the subleading multiplicity problem remains unresolved.

### Finite $D_5\downarrow B_4$ cross-sections

**Status: exact integral inversion implemented; irreducible-parent positivity
ansatz ruled out through level 10.**

`finite_cross_section.py` constructs a finite branching closure from the
baseline-free cumulative HFT $SO(9)$ spectrum and performs exact unipotent
inversion for an explicitly selected, level-independent parent of every $B_4$
top weight. Both natural global policies pass all section, triangularity,
integrality and restriction checks through level 10.

They do not preserve positivity. The all-chiral policy first fails at level 7;
the fermion-chiral/tensor-balanced policy first fails at level 6.

`search_finite_cross_sections.py` exhaustively tests all 256 inequivalent global
irreducible-parent selections on the 57-weight closure through level 10. None is
positive at every level. The obstruction is forced by $[0,0,0,2]_9$:

- selecting $[0,0,0,0,2]_{10}$ forces a negative 45 at level 7;
- selecting $[0,0,0,1,1]_{10}$ forces a negative 120 at level 6.

When levels are tested separately, the numbers of positive selections among
the 256 candidates are 256 for each of levels 1--5, 128 at level 6, 128 at level
7, 64 at level 8, 16 at level 9, and zero at level 10. Therefore level 10 cannot
be lifted positively even by choosing a new irreducible-parent section solely
for that level.

This does not rule out more general additive sections containing kernel
corrections or several $D_5$ irreducibles with the same top weight. It does show
that the earlier level-dependent 126/210 switch is not a single analytic
cross-section. See `FINITE_CROSS_SECTION_REPORT.md`.

### Bars III.C

**Status: exact reduction to III.B; all-orders positivity is conditional.**

The convolution coefficients $p(k)-p(k-1)$ are nonnegative, so III.C is positive
at every level provided III.B is positive at every level. The explicit III.C
spectrum has been checked through level 10 using the protected III.B data.

### Plethystic identities

**Status: formal algebra isolated and verified; earlier geometric
interpretations withdrawn.**

The baseline-free module `plethystic_series.py` contains the generic formal
recurrences. `verify_plethystic_identity_so9.py` uses the independently derived
HFT spectrum to verify

$$
\operatorname{PL}[R(q)]=\operatorname{PL}[r(q)]+\mathbf 1q
$$

through level 10 without importing protected data. The identity is exact
formally and does not prove $SO(10)$ positivity.

The older pure-spinor, on-shell-relation and general generator/syzygy
interpretations of individual signed plethystic coefficients are withdrawn.
See `PLETHYSTIC_STATUS.md`.

### Legacy negative-tail tables

**Status: numerically reconstructed; former proof interpretation withdrawn.**

The original `test_neg_analysis.py` is absent. Its level-1--10 dimensions,
supports and multiplicities have been reconstructed exactly by
`verify_legacy_negative_tail_claims.py` from consecutive differences of the
protected cumulative $SO(10)$ characters.

Because the script defines $r_n^{10}=R_n^{10}-R_{n-1}^{10}$ using the already
known positive answer, the resulting inequality
$\operatorname{neg}_n\leq R_{n-1}$ is equivalent to baseline positivity. It is
a consistency check, not an independent proof. See
`LEGACY_NEGATIVE_TAIL_AUDIT.md`.

### Report archive

All superseded working reports have been moved to `archive/superseded_reports/`
and retain prominent correction notices. `archive/README.md` records why each
was archived and names its authoritative replacement.

## Authoritative Documents

| Document | Role |
| --- | --- |
| `STATUS.md` | Central statement of established, conditional and open results |
| `GoalPlethystic.md` | Project motivation and corrected plethystic question |
| `PLETHYSTIC_STATUS.md` | Formal identities and withdrawn interpretations |
| `FINITE_CROSS_SECTION_REPORT.md` | Finite-section construction and obstruction |
| `LEGACY_NEGATIVE_TAIL_AUDIT.md` | Reconstruction and provenance of old tail tables |
| `archive/README.md` | Index of superseded historical reports |

## Canonical Scripts

| Script | Role | May import baseline? |
| --- | --- | ---: |
| `hft_so9.py` | Baseline-free HFT $SO(9)$ derivation | No |
| `verify_hft_so9_against_baseline.py` | Compare derived $r_n$ with levels 1--10 | Yes |
| `hft_so10_uplift.py` | Baseline-free M3 and bounded M4 diagnostic | No |
| `verify_hft_so10_against_baseline.py` | Restriction and kernel-remainder comparison | Yes |
| `finite_cross_section.py` | Explicit baseline-free finite-section inversion | No |
| `search_finite_cross_sections.py` | Exhaustive finite irreducible-parent section search | No |
| `verify_finite_cross_section_against_baseline.py` | Compare canonical section lifts with known completion | Yes |
| `plethystic_series.py` | Generic formal plethystic recurrences | No |
| `verify_plethystic_identity_so9.py` | Verify the formal Bars identity from HFT $SO(9)$ data | No |
| `massive_plethystic_SO10.py` | Describe the PL of protected $SO(10)$ data | Yes |
| `massive_compare_r_R.py` | Baseline-dependent PL and restriction comparison | Yes |
| `verify_legacy_negative_tail_claims.py` | Reconstruct historical negative-tail tables | Yes |
| `massive_scheme_IIIC.py` | III.C convolution from known III.B data | Yes, explicitly conditional |

## Reproduction Commands

```text
./bin/sage-run hft_so9.py --max-level 10
./bin/sage-run verify_hft_so9_against_baseline.py --max-level 10
./bin/sage-run hft_so10_uplift.py --max-level 10
./bin/sage-run verify_hft_so10_against_baseline.py --max-level 10
./bin/sage-run finite_cross_section.py --max-level 10 --policy chiral
./bin/sage-run finite_cross_section.py --max-level 10 --policy fermion-chiral-tensor-balanced
./bin/sage-run search_finite_cross_sections.py --max-level 10
./bin/sage-run verify_finite_cross_section_against_baseline.py --max-level 10
./bin/sage-run verify_plethystic_identity_so9.py --max-level 10
./bin/sage-run verify_legacy_negative_tail_claims.py --max-level 10 --verbose
```

The $SO(10)$ level-10 branching checks can take several minutes.

## Cleanup Boundary

The inherited repair work is complete:

- derivation and baseline comparison layers are separated;
- M4 is recorded as unresolved rather than passed;
- the finite irreducible-parent cross-section ansatz has been exhaustively
  tested and its obstruction documented;
- formal plethystic identities are separated from baseline-dependent tables and
  speculative interpretations;
- missing-script numerical claims have been reconstructed with explicit
  baseline provenance;
- superseded reports are archived and indexed.

## New Research Direction

The next work is no longer repair or pruning. It is a new analytic programme:

1. Decompose the baseline-free HFT $SO(9)$ spectrum into fixed-$(m,r,s)$ Regge
   columns.
2. Construct the restriction-kernel lattice and mixed-parent corrections in a
   trajectory-adapted basis.
3. Test whether corrections are generated from finitely many boundary seeds by
   Regge shifts, while imposing positivity and chirality.
4. Use the protected levels 1--10 only as a later comparison layer, not as input
   to the construction.
