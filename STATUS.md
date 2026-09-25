# Project Status

**Last updated:** 25 September 2026

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

They encode the known level-1--10 result and are used only by explicitly named verification scripts.

## Useful papers

### Core Reference for the Entire Project

**Itzhak Bars** (1995)

*Stringy evidence for $D = 11$ structure in strongly coupled type IIA superstring*

[hep-th/9503228](https://arxiv.org/abs/hep-th/9503228) | [INSPIRE-HEP recid: 393910](https://inspirehep.net/literature/393910)

Proposed both the minimal cumulative scheme (Section III.B) and the higher multiplicity scheme (Section III.C).

### Follow ups by Bars:

These address compatibility of the massive modes with U-duality and clarify
that the minimal eleven-dimensional completion is not intended to be the only
possible nonperturbative spectrum.

**Itzhak Bars, Shimon Yankielowicz (1995)**

*U-duality multiplets and non-perturbative superstring states*

[hep-th/9511098](https://arxiv.org/abs/hep-th/9511098) | [INSPIRE-HEP recid: 402246](https://inspirehep.net/literature/402246)

**Itzhak Bars** (1996)

*Consistency between 11D and U-duality*

[hep-th/9601164](https://arxiv.org/abs/hep-th/9601164) | [INSPIRE-HEP recid: 404610](https://inspirehep.net/literature/404610)

### Inspirations for analytical approaches to establishing the Bars proposal(s) to all orders:

**Amihay Hanany, Davide Forcella, Jan Troost** (2010)

*The Covariant Perturbative String Spectrum*

[arXiv:1007.2622 [hep-th]](https://arxiv.org/abs/1007.2622) | [INSPIRE-HEP recid: 861347](https://inspirehep.net/literature/861347)

Analytical expression for the massive mode partition function as an SO(9) character (albeit not one that has manifestly positive coefficients at each level)

**Alessandro Georgoudis, Joseph A. Minahan, Gustav Ström, Athanasios Zoumis** (2026)

*The growth of $SO(9)$ super-representations in Type II string theory*

[arXiv:2609.04107 [hep-th]](https://arxiv.org/abs/2609.04107) | [INSPIRE-HEP recid: 3199641](https://inspirehep.net/literature/3199641)

Present an empirical formula that specifies which SO(9) representations appear at any level.

**Niklas Beisert, Massimo Bianchi, José F. Morales, Henning Samtleben** (2004)

*On the spectrum of AdS/CFT beyond supergravity*
[hep-th/0310292](https://arxiv.org/abs/hep-th/0310292)

In a different type-IIB/$AdS_5\times S^5$ context, Section 2.1 observes that
partial sums of chiral flat-space string primaries assemble into $SO(10)$
superrepresentations; its first three examples coincide with the Bars
cumulative pattern. The paper retains an additional oscillator-number grading
and uses $\Delta-J=\nu$ to resolve finite-level lift ambiguities. This is a
potential separate graded-uplift direction, not an all-orders derivation of
the Bars proposal. GU1 has now tested its Appendix B construction independently
through level 7: the refined branching works and its cumulative lift is
positive, but it first differs from the protected algorithmic continuation at
level 6 by outer-chirality kernel directions. Bars himself displayed the
minimal lift only through level 5, so this is not a disagreement with a
level-6 choice made by Bars. The paper cites Bars' 2002 work on hidden twelve-dimensional
structures but does not cite hep-th/9503228.

## Current Mathematical Status

### Scope and principal analytic goal

The principal goal is an all-orders **existence/admissibility proof** for the
minimal Bars III.B scheme. Given the HFT-derived perturbative character

$$
R_n^9=\sum_{i=1}^n r_i^9,
$$

we seek an explicit baseline-free construction proving that for every $n$
there is at least one positive integral $SO(10)$ character $X_n$ with

$$
X_n\downarrow SO(9)=R_n^9.
$$

Where possible, a construction may be compared with the protected algorithmic
continuation through level 10, but reproducing that particular continuation is
not part of the Bars III.B claim. Uniqueness is **not** part of the general
claim. Here “minimal” means that no extra III.C oscillator multiplicities or
additional complete, purely nonperturbative multiplets have been adjoined; it
does not mean that the positive restriction fibre contains a unique point or
that Bars selected a unique chirality convention.

Three different questions must remain separate:

1. **Fixed-target kernel freedom.** Distinct positive $SO(10)$ characters can
   restrict to the same $R_n^9$. GU1--GU5 and TK2--TK5 exhibit this freedom.
2. **Bars III.C multiplicity enlargement.** Allowing all proposed
   eleventh-direction oscillator partitions changes the multiplicities and
   therefore changes the target spectrum.
3. **Additional U-duality multiplets.** Complete $SO(10)$ multiplets made only
   of nonperturbative states may be added. They are not required to appear in
   the perturbative HFT character, which does not enumerate the full charged
   nonperturbative base space.

The unrestricted nonperturbative problem is therefore a classification of
admissible completions, not a uniqueness problem. Selection principles remain
meaningful only after a particular minimality condition and set of physical
labels have been fixed.

### Bars III.B through level 10

The cumulative spectra

$$
R_n=\sum_{i=1}^n r_i
$$

are recorded in the protected baseline as positive integral $SO(10)$ characters
for levels 1 through 10. Their provenance must be stated carefully:

- Bars explicitly displayed positive $SO(10)$ decompositions only through
  level 5.
- Levels 6--10 are a particular positive continuation produced by an external
  algorithm and then established as the protected human baseline for this
  project. They are not representations selected or published by Bars.

This is the finite-level result to be explained, not an input permitted in
first-principles derivations.

The open all-orders claim is existence of a positive lift, not uniqueness of
the lift. At levels 6--10 the finite protected character is one distinguished
algorithmic representative of a generally nontrivial positive restriction
fibre. It is useful as a comparison target, but agreement with it is a stronger
secondary condition rather than part of Bars III.B.

### HFT $SO(9)$ reconstruction

**Status: independently derived through level 11 and separately benchmarked
through level 10.**

`hft_so9.py` constructs the Hanany--Forcella--Troost numerator in $SO(9)$ and
performs character division by the positive universal massive supermultiplet
$Z_Q$. It imports no protected baseline file. At every level 1--11:

- the quotient is a positive integral $SO(9)$ character;
- the exact identity $N_n=Z_Q r_n$ holds.

`verify_hft_so9_against_baseline.py` is a separate comparison layer. It verifies
that the independently derived $r_n$ agree with consecutive differences of the
protected cumulative spectrum after restriction to $SO(9)$. All levels 1--10
match exactly.

The level-11 result is an internal baseline-free extension, not a comparison
with protected data. No current computation proves coefficientwise positive
integral $SO(9)$ quotients at all orders. HFT also identified this all-orders
positivity as a mathematical challenge despite its physical expectation.

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

**Status: algebraically obstructed at level 2 for the current virtual
$SO(10)$ HFT numerator uplift; the previously claimed pass is withdrawn.**

The proposed highest-weight division by the virtual character $Z_Q^{10}$ is not
monotone. The repaired peeling diagnostic is exact at level 1 but cannot
complete the proposed quotient at level 2.

TK4c strengthens this algorithmic failure. For any lift $Q_n$ of the derived
$SO(9)$ single-level character, define

$$
\kappa_n=N_n^{10}-Z_Q^{10}Q_n.
$$

Its class in
$\ker(\operatorname{Res})/Z_Q^{10}\ker(\operatorname{Res})$ is independent of
the lift. An injective five-variable Laurent-weight embedding proves that the
level-2 remainder is not divisible by $Z_Q^{10}$. Hence no alternative virtual
$SO(10)$ lift can make the exact quotient hold at level 2. This is independent
of positivity and of the peeling order. See
`trajectory_kernel/reports/TK4C_KERNEL_ANOMALY.md`.

The separate script `verify_hft_so10_against_baseline.py` substitutes the known
baseline single-level lifts for comparison only. It finds:

- exact agreement after restriction to $SO(9)$ through level 10;
- a nonzero $SO(10)$ remainder at every level 2--10;
- every such remainder has dimension zero and restricts to zero in $SO(9)$.

Thus the known spectrum is compatible with the HFT numerator only modulo the
restriction kernel. TK4c now independently rules out an alternative exact
quotient at level 2 in the full representation ring for this numerator uplift.
This does not affect the exact $SO(9)$ HFT division and does not exclude a
different $SO(10)$ analytic formulation with the same restriction.

### Closed-string universal factor and level-2 test

**Status: the intrinsic positive factor is verified; tensoring the current
virtual chiral uplifts does not give the required closed uplift.**

The baseline-free TK4d calculation constructs

$$
Q_{\mathrm{cl}}=\bigoplus_{j=0}^{16}\Lambda^j\mathbf{16}.
$$

It is a positive, outer-chirality-invariant $SO(10)$ character of dimension
65,536, and its restriction is exactly $(Z_Q^9)^2$. However, if $z$ is the
current virtual chiral $SO(10)$ uplift, neither $z^2$ nor $z\tau(z)$ equals
$Q_{\mathrm{cl}}$; both raw products are nonpositive and differ from the
intrinsic factor by restriction-kernel characters.

At level 2, neither raw numerator product $N_2^2$ nor
$N_2\tau(N_2)$ is divisible by $Q_{\mathrm{cl}}$. Thus positivity of the full
universal factor does not rescue the operation “uplift each chiral half, then
tensor.” This is not a no-go theorem for a direct closed-string uplift: such a
construction must combine left and right before making the $SO(10)$ uplift and
must be normalized by $Q_{\mathrm{cl}}$ already at level 1. See
`trajectory_kernel/reports/TK4D_CLOSED_LEVEL2.md`.

### Direct closed low-level lift (GU4)

**Status: exhaustive baseline-free calculation complete through level 3.**

Starting directly from $T_n=R_n^9\otimes R_n^9$, the full finite
$D_5\downarrow B_4$ parent closure contains a unique positive
outer-invariant lift at each level 1--3. The nontrivial answers are

$$
X_2=10\otimes10=1+45+54
$$

and

$$
X_3=(54+16_+)\otimes(54+16_-).
$$

At level 3 there are 27 positive lifts before imposing outer invariance, so
the closed chirality condition is genuinely selective in this first window.
Individual $\ell'$ source blocks do not generally lift positively; rather,
the factorized representatives recover the labels exactly as the branching
interlacing depths $d_L=\lambda_{1,L}-\mu_{1,L}$ and
$d_R=\lambda_{1,R}-\mu_{1,R}$. Multiplication by the intrinsic
$Q_{\mathrm{cl}}$ then preserves positivity and exact restriction but adds no
new selection condition. See
`graded_uplift/reports/GU4_DIRECT_CLOSED_LOW_LEVELS.md`.

### Level-6 direct closed and depth tests (GU5)

**Status: the low-level uniqueness and naive depth principles do not extend
to level 6.**

A baseline-free construction gives two distinct positive outer-invariant
closed $SO(10)$ characters restricting to the same
$R_6^9\otimes R_6^9$. They are obtained by reversing one chiral parent
$[3,0,0,0,1]\to[3,0,0,1,0]$ before tensoring with the outer conjugate. Their
difference is outer-even, has 92 terms, dimension zero, and zero $SO(9)$
restriction.

Separately, exhaustive refined branching proves that the naive identification

$$
\ell'=\lambda_1-\mu_1
$$

has positive lifts through level 4 but none at levels 5 or 6. The first
failure is an unavoidable excess $SO(9)$ spinor at depth 1. A protected
comparison finds the same defect for both the protected algorithmic
continuation and the paper candidate; at level 6 their refined depth images
are identical despite their different $SO(10)$ chirality assignments. See
`graded_uplift/reports/GU5_LEVEL6_DIRECT_CLOSED_AND_DEPTH.md`.

These results end the search for uniqueness based only on positivity,
restriction and closed outer invariance. They do not obstruct the principal
III.B existence problem: either level-6 candidate is an admissible positive
lift of the fixed perturbative target.

### All-orders positivity

**Status: open.**

Two logically prior all-orders statements remain unproved:

1. the HFT quotient $r_n^9$ has nonnegative integral $SO(9)$ coefficients for
   every $n$;
2. every cumulative $R_n^9$ admits at least one positive integral $SO(10)$
   lift.

The second statement is the central Bars III.B admissibility problem. It does
not require a unique lift. Leading-Regge identities, the GMSZ chamber
relations, the finite kernel-source construction and the verified levels
provide evidence, but the subleading/core multiplicity problem remains
unresolved.

### Existence versus chirality selection

The finite results now exhibit more than one positive completion of the same
cumulative $SO(9)$ target. In particular, the oscillator-graded candidate of
hep-th/0310292 and the protected algorithmic continuation agree through level
5 and first differ at level 6 by outer-chirality kernel directions. Both are
positive and have the same exact $SO(9)$ restriction.

This should be interpreted as evidence for nonuniqueness of the lift, not as a
conflict with Bars: Bars made no level-6 choice and did not require the lift to
have a particular form. It remains possible that outer-chirality orientation
is partly conventional, but no physical principle establishing that has been
identified. Conversely, the type-IIB/$AdS_5\times S^5$ origin of the grading
in hep-th/0310292 does not by itself justify importing its chirality choice
into the type-IIA/eleven-dimensional problem.

The role of U-duality may eventually constrain this freedom, but it is not
part of the current analytic programme. In particular, possible U-duality
completions should not be conflated with the minimal fixed-target existence
claim studied here.

### Global restriction-ring kernel reformulation

At the level of representation rings, the standard restrictions of the
fundamental characters are triangular:

$$
10\downarrow SO(9)=1+9,
$$

$$
45\downarrow SO(9)=9+36,
$$

$$
120\downarrow SO(9)=36+84,
$$

and both half-spinors restrict to the same $16$:

$$
16_+\downarrow SO(9)=16_-\downarrow SO(9)=16.
$$

Together with polynomial generation by the fundamental characters, this gives
the global ring presentation

$$
\ker\!\left(R(\operatorname{Spin}(10))\to
R(\operatorname{Spin}(9))\right)=(J),
\qquad J=16_+-16_-.
$$

Thus, after choosing any virtual section $s$, every lift can be written as

$$
X_n=s(R_n^9)+JH_n
$$

for a virtual $SO(10)$ character $H_n$. This does not solve positivity: the
positive semiring fibre is much subtler than the ring kernel. It does compress
the growing finite collection of kernel coordinates into one global ideal.
Two exact identities connect this presentation to TK5b's nontransported seeds:

$$
A_0=16_-J,
$$

$$
C_0=126_-J,
$$

up to the fixed chirality convention. Later trajectory generators are also
multiples of $J$ in the representation ring, although their quotients need not
be single positive irreducibles.

### Recommended next analytic directions

The present priority order is:

1. **Exploit the principal kernel ideal.** Replace separate $A,B,C,\ldots$
   corrections by an auxiliary character series
   $H(q)=\sum_nH_nq^n$ in
   $X(q)=s(R(q))+JH(q)$, and search for a finite recurrence or module
   presentation for $H(q)$.
2. **Characterize the positive restriction image.** Reformulate
   $D_5\downarrow B_4$ liftability as a nonnegative covering by
   multiplicity-free interlacing packets. Seek Hall-type inequalities,
   total-unimodularity or saturation statements that reduce existence to
   explicit inequalities on the cumulative HFT multiplicities. This attacks
   the theorem actually required and does not select a unique lift.
3. **Test cumulative positivity of the oscillator-graded candidate.** Its
   single-level tagged characters are virtual, but their cumulative ungraded
   sums are positive through level 7. Determine whether the starred
   differences telescope, or admit a complex/filtration interpretation, at
   arbitrary level. An all-orders proof for this candidate would establish
   Bars III.B existence even though it need not reproduce the protected
   algorithmic continuation.

### Oscillator-count-refined uplift

**Status: the hep-th/0310292 candidate is independently verified through
level 7; under the tested finite grading bounds it uniquely excludes the
protected algorithmic continuation from level 6 onward.**

`graded_uplift/refined_spectrum.py` derives the $SO(8)$ chiral primaries while
retaining both the string level $\ell=\sum nN_n$ and oscillator count
$\nu=\sum N_n$. Forgetting $\nu$ agrees exactly through level 7 with the
baseline-free HFT $SO(9)$ primary restricted to $SO(8)$.

Exact $SO(10)\to SO(8)\times SO(2)_J$ weight branching verifies the Appendix B
candidate of hep-th/0310292 under $\Delta-J=\nu$ through level 7. After
forgetting $\Delta$, all tested cumulative sums are positive $SO(10)$
characters and restrict to the intended cumulative HFT $SO(9)$ character.

A separate comparison with the protected algorithmic continuation agrees
through level 5. At level 6 the
literature candidate replaces $[0,0,0,0,1]$ and $[1,0,0,0,1]$ by their outer
conjugates. Further mixed-chirality choices occur at level 7. Thus the unrelated
IIB grading realizes the cumulative-positivity phenomenon but chooses a
different restriction-kernel representative. Since Bars displayed no
level-6 lift, this is not a disagreement with Bars. See
`graded_uplift/reports/GU1_LITERATURE_GRADING_AUDIT.md`.

GU2 closes the finite tagged domain under outer chirality and imposes both the
complete $\nu$-graded $SO(8)$ target and a chosen ungraded $SO(10)$ target.
The paper remains feasible, while the protected algorithmic single-level
target is rationally infeasible at levels 6 and 7. The exact outer-closed
ranks are $159<160$ and $269<270$ after target augmentation. At level 6 the
obstruction remains through
$\Delta_{\max}=10$. The full-column-rank matrices make the paper solution
unique inside these domains, but do not establish an unbounded-$\Delta$
theorem. See `graded_uplift/reports/GU2_GRADED_BARS_COMPATIBILITY.md`.

GU3 implements the Type-IIA chirality reversal. The right sector is the
$D_5$ outer conjugate of the left, or equivalently obeys
$\nu_R=\Delta_R+J_R$. Bars' nonperturbative label
$\ell'=n-\ell$ is retained separately on the two sides. All source blocks are
exact through level 7, but the resolved graded maps have full column rank, so
their closed tensor product uniquely forces the paper character tensored with
its outer conjugate. This positive closed character still differs from the
closed character formed from the protected algorithmic continuation at levels
6 and 7 by nonzero outer-even restriction-kernel elements. See
`graded_uplift/reports/GU3_IIA_CLOSED_REFINEMENT.md`.

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

Bars III.C is a different, enlarged spectrum rather than a competing point in
the same fixed-target restriction fibre:

$$
R_n^{\mathrm{III.C}}
=\sum_{\ell'=0}^{n-1}p(\ell')r_{n-\ell'}.
$$

Equivalently, it is a positive convolution of III.B with coefficients
$p(k)-p(k-1)$. These coefficients are nonnegative, so III.C is positive at
every level provided III.B is positive at every level. The explicit III.C
spectrum has been checked through level 10 using the protected III.B data.
III.C agrees with III.B at level 2 because $p(0)=p(1)=1$; its higher
multiplicities begin later.

### U-duality enlargement at oscillator level 2

**Status: literature proposal recorded; it is not a fixed-target uplift.**

Bars and Yankielowicz analyze compactified type-IIA index multiplets. For the
$(d,c)=(7,3)$ compactification, simultaneous compatibility with the
$K=SO(5)$ U-duality classification and with $SO(10)$ requires the level-2
collection below, with the common long-supermultiplet factor suppressed:

$$
1+3(10)+2(45)+54.
$$

The minimal eleven-dimensional completion is

$$
10_L\otimes10_R=1+45+54,
$$

so the additional purely nonperturbative content is

$$
3(10)+45.
$$

These are genuine extra multiplets, not restriction-kernel corrections and
not the Bars III.C level-2 multiplicity. The paper notes that they are not
required by the minimal completion in several other compactifications, while
suggesting that a common eleven-dimensional theory may nevertheless contain
them there as well. More generally it distinguishes minimal U-duality
completion from optional purely nonperturbative complete U-multiplets. See
[hep-th/9511098](https://arxiv.org/abs/hep-th/9511098) and the follow-up
[hep-th/9601164](https://arxiv.org/abs/hep-th/9601164).

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
| `trajectory_kernel/STATUS.md` | Local status for the new analytic programme |
| `graded_uplift/STATUS.md` | Local status for the oscillator-graded uplift test |

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
| `trajectory_kernel/regge_columns.py` | TK1 baseline-free Regge-column diagnostics | No |
| `trajectory_kernel/kernel_lattice.py` | TK2 branching shifts and finite integral kernel basis | No |
| `trajectory_kernel/correction_ansatz.py` | TK3 exact positive fibres in kernel coordinates | No |
| `trajectory_kernel/trajectory_selection.py` | TK4 corrected-shift selection and level-11 holdout | No |
| `trajectory_kernel/kernel_generating_series.py` | TK4b source series and HFT numerator obstruction | No |
| `trajectory_kernel/kernel_anomaly.py` | TK4c lift-independent kernel-anomaly classes and quotient certificates | No |
| `trajectory_kernel/closed_level2.py` | TK4d intrinsic closed factor and exact level-2 closed-product test | No |
| `trajectory_kernel/chamber_audit.py` | TK5a GMSZ support-chamber and multiplicity-shift audit | No |
| `trajectory_kernel/chamber_core.py` | TK5b transported/core decomposition and kernel-source test | No |
| `trajectory_kernel/chamber_witness.py` | TK5c minimal core-source witnesses and cutoff stability | No |
| `graded_uplift/refined_spectrum.py` | Derive the $(\ell,\nu)$-graded SO(8) primaries | No |
| `graded_uplift/refined_branching.py` | Exact $SO(10)\to SO(8)\times SO(2)_J$ branching | No |
| `graded_uplift/verify_paper_grading.py` | Verify Appendix B against graded oscillators and HFT | No |
| `graded_uplift/verify_against_baseline.py` | Compare the literature lift with the protected algorithmic continuation | Yes |
| `graded_uplift/graded_kernel.py` | Finite graded domains, exact branching matrices and solvers | No |
| `graded_uplift/verify_bars_compatibility.py` | Test the protected algorithmic target in finite graded domains | Yes |
| `graded_uplift/scan_delta_bound.py` | Scan finite $\Delta$ cutoffs and exact rational ranks | Yes |
| `graded_uplift/iia_closed_refinement.py` | Opposite-chirality, axial and $\ell'$-resolved IIA construction | No |
| `graded_uplift/verify_iia_closed_against_baseline.py` | Compare the resolved IIA closed candidate with the protected algorithmic continuation | Yes |
| `graded_uplift/direct_closed_low_levels.py` | GU4 exhaustive direct closed lift through level 3 | No |
| `graded_uplift/interlacing_depth_audit.py` | GU5 positive-fibre audit of naive interlacing depth | No |
| `graded_uplift/direct_closed_level6.py` | GU5 pair of distinct positive closed level-6 lifts | No |
| `graded_uplift/verify_level6_depth_candidates.py` | Compare the protected algorithmic and paper candidates with naive depth | Yes |

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
./bin/sage-run -m trajectory_kernel.regge_columns --max-level 10
./bin/sage-run -m trajectory_kernel.kernel_lattice --max-level 10
./bin/sage-run -m trajectory_kernel.correction_ansatz --max-level 10
./bin/sage-run -m trajectory_kernel.trajectory_selection --max-level 10 --verbose
./bin/sage-run -m trajectory_kernel.trajectory_selection --max-level 11 --probe-next-level
./bin/sage-run -m trajectory_kernel.kernel_generating_series --max-level 11
./bin/sage-run -m trajectory_kernel.kernel_anomaly --max-level 11 --certificate-level 6
./bin/sage-run -m trajectory_kernel.closed_level2
./bin/sage-run -m trajectory_kernel.chamber_audit --max-level 11
./bin/sage-run -m trajectory_kernel.chamber_core --max-level 11
./bin/sage-run -m trajectory_kernel.chamber_witness --max-level 11 --enumeration-cap 20
./bin/sage-run -m graded_uplift.verify_paper_grading --max-level 7
./bin/sage-run -m graded_uplift.verify_against_baseline --max-level 7 --verbose
./bin/sage-run -m graded_uplift.verify_bars_compatibility --max-level 7
./bin/sage-run -m graded_uplift.scan_delta_bound --level 6 --max-slack 3 --exact-rank
./bin/sage-run -m graded_uplift.iia_closed_refinement --max-level 7
./bin/sage-run -m graded_uplift.verify_iia_closed_against_baseline --max-level 7 --verbose
./bin/sage-run -m graded_uplift.direct_closed_low_levels --max-level 3 --verbose
./bin/sage-run -m graded_uplift.interlacing_depth_audit --max-level 6 --verbose
./bin/sage-run -m graded_uplift.direct_closed_level6 --verbose
./bin/sage-run -m graded_uplift.verify_level6_depth_candidates --max-level 6 --verbose
```

The $SO(10)$ level-10 branching checks can take several minutes.

## Cleanup Boundary

The inherited repair work is complete:

- derivation and baseline comparison layers are separated;
- M4 is recorded as algebraically obstructed at level 2 rather than passed;
- the finite irreducible-parent cross-section ansatz has been exhaustively
  tested and its obstruction documented;
- formal plethystic identities are separated from baseline-dependent tables and
  speculative interpretations;
- missing-script numerical claims have been reconstructed with explicit
  baseline provenance;
- superseded reports are archived and indexed.

## New Research Direction

The repair and pruning phase is complete. The analytic programme is now
reoriented toward an all-orders **existence construction** for Bars III.B and,
secondarily, a classification of the resulting positive fibres. The earlier
search for a universally unique representative was useful diagnostically but
is no longer the main objective.

The programme is isolated under `trajectory_kernel/`; its local `README.md` and
`STATUS.md` define the derivation/comparison boundary and milestone sequence.

1. **TK1 complete through level 10:** the baseline-free HFT $SO(9)$ spectrum
   has been decomposed into 13 fixed-$(m,r,s)$ columns and 56 orbits at fixed
   reduced depth $\delta=n-\ell-3m$. Of 134 adjacent shift comparisons, 54
   fail, so shift invariance is not a universal multiplicity identity. See
   `trajectory_kernel/reports/TK1_REGGE_COLUMNS.md`.
2. **TK2 complete:** the level-10 finite restriction matrix has size
   $57\times65$, rank 57 and an explicit integral kernel basis of rank 8. Raw
   Regge shifts fail on all eight generators, but an exact boundary-corrected
   shift advances every generator to the next one. The 126/210 seed is
   $210-126-120+45-10+1$. See
   `trajectory_kernel/reports/TK2_BRANCHING_KERNEL_SHIFTS.md`.
3. **TK3 complete:** every positive cumulative lift in the finite parent
   domain is parameterized by trajectory-adapted kernel coordinates without
   using the protected completion. Every level has a nonempty fibre, with counts
   $1,1,1,1,1,1,2,8,72,6057$ through level 10. The three TK2 kernel families
   suffice, but positivity is highly non-unique. See
   `trajectory_kernel/reports/TK3_POSITIVE_FIBRES.md`.
4. **Historical selection experiments, now concluded as uniqueness tests:**
   the programme tested whether a baseline-free analytic principle selects a
   distinguished trajectory-compatible lift from these fibres. The first TK4
   experiment found that
   corrected-shift minimality is cutoff-stable through the new HFT level 11,
   which introduces no new seed family, but reasonable cost priorities remain
   non-unique and disagree. See
   `trajectory_kernel/reports/TK4_SELECTION_EXPERIMENT.md`.
   **TK4b:** boundary-only source generation fails at level 9, and exact HFT
   numerator division with positive cumulative lifts fails already at level 2.
   The level-2 kernel remainder is $-2A_0+J_{126}$. See
   `trajectory_kernel/reports/TK4B_KERNEL_GENERATING_SERIES.md`.
   **TK4c:** the level-2 anomaly defines a nonzero class modulo
   $Z_Q\ker(\operatorname{Res})$, so no virtual kernel correction can restore
   exact division. The seed is outer-even, and its corrected shifts do not
   generate the later certified classes through level 6. See
   `trajectory_kernel/reports/TK4C_KERNEL_ANOMALY.md`.
   **TK4d:** the intrinsic positive closed factor
   $Q_{\mathrm{cl}}=\Lambda^\bullet\mathbf{16}$ restricts to $(Z_Q^9)^2$,
   but it is not the tensor product of either choice of virtual chiral uplift.
   Neither raw level-2 chiral product is divisible by $Q_{\mathrm{cl}}$.
   Therefore a viable full closed construction must combine left and right
   before uplifting. See
   `trajectory_kernel/reports/TK4D_CLOSED_LEVEL2.md`.
5. **TK5a complete through level 11:** the empirical GMSZ support polytope is
   exact at every level in its claimed domain $7\leq n\leq11$, with
   $23,32,43,56,72$ predicted and observed irreps. All 253 admissible
   $\ell$-shift relations and all 50 admissible $m$-shift relations pass; the
   $r$-shift chamber has not opened in this window and remains untested. Of 170
   adjacent Regge comparisons with target level at least 7, the GMSZ chamber
   contains 95, all matching; outside it, 72 of 75 fail. Thus the chamber rule
   sharply explains the TK1 partial transport without yet solving the
   $SO(10)$ kernel selection problem. See
   `trajectory_kernel/reports/TK5A_GMSZ_CHAMBER_AUDIT.md`.
6. **TK5b complete through level 11:** applying the published priority
   $\ell$, then $m$, then $r$ separates each $r_n^9$ into transported data and
   a residual core. Every selected transport identity is exact. All 11 finite
   restriction-kernel generators are exact corrected-shift descendants of two
   nontransported objects, $A_0$ and $C_0$; in particular the former family-B
   seed $B_0$ is a corrected $m$-shift of $A_0$. Strict $\ell=0$ coordinate
   sources still fail at level 9, while sources allowed only at GMSZ-core
   positions admit positive cumulative lifts through level 11. This is a
   finite existence result, not a unique or all-orders selection rule. See
   `trajectory_kernel/reports/TK5B_CHAMBER_CORE_KERNEL_SOURCES.md`.
7. **TK5c complete through level 11:** exact lexicographic minimization of
   core-supported sources gives event/charge minima
   $(1,1),(2,2),(3,4),(5,11),(7,20)$ at horizons 7--11, with respectively
   $1,2,2,3,6$ distinct minimal witnesses. The optimal faces cease to have
   compatible prefixes at $9\to10$ and again at $10\to11$, so ungraded source
   sparsity is not a cutoff-stable analytic selector. See
   `trajectory_kernel/reports/TK5C_MINIMAL_CORE_WITNESSES.md`.
8. **GU1 complete through level 7:** the oscillator-count-refined Appendix B
   construction of hep-th/0310292 is reproduced exactly and its cumulative
   ungraded lift is positive with the correct HFT $SO(9)$ restriction. It
   agrees with Bars' displayed lift, and with the protected algorithmic
   continuation, through level 5. Beginning at level 6 it differs from the
   protected continuation by outer-chirality kernel directions. This supplies
   an independent positive continuation of the existence pattern, not a
   disagreement with a higher-level choice made by Bars. See
   `graded_uplift/reports/GU1_LITERATURE_GRADING_AUDIT.md`.
9. **GU2 complete through level 7 under explicit finite bounds:** after
   closing the paper-bound tagged domain under outer chirality, the paper
   solution remains feasible but the protected algorithmic single-level
   targets are rationally infeasible at levels 6 and 7. Exact ranks are
   $159<160$ and $269<270$ after target augmentation; the candidate matrices
   have full column rank, so the paper solution is unique inside those
   domains. The level-6 obstruction persists under nested enlargements through
   $\Delta_{\max}=10$. This constrains compatibility with the BBMS grading; it
   is neither a failure of positive liftability nor an unbounded-$\Delta$
   theorem. See
   `graded_uplift/reports/GU2_GRADED_BARS_COMPATIBILITY.md`.
10. **GU3 complete through level 7 in the resolved IIA domain:** opposite
    right-moving chirality is exactly equivalent to the axial relation
    $\nu_R=\Delta_R+J_R$, and every Bars $(\ell',\nu)$ block is reproduced.
    The resolved chiral maps and their tensor products are injective, however,
    so the unique closed lift is the paper character times its outer
    conjugate. It first differs from the closed character formed from the
    protected algorithmic continuation at level 6 by an outer-even
    restriction-kernel element. See
    `graded_uplift/reports/GU3_IIA_CLOSED_REFINEMENT.md`.
11. **GU4 complete through level 3:** direct lifting of
    $R_n^9\otimes R_n^9$ in the full outer-closed parent domain gives a unique
    positive outer-invariant result. At level 3, outer invariance reduces 27
    positive lifts to one. The factorized representatives recover both Bars
    $\ell'$ labels as $D_5\downarrow B_4$ interlacing depths. See
    `graded_uplift/reports/GU4_DIRECT_CLOSED_LOW_LEVELS.md`.
12. **GU5 level-6 check complete:** the direct closed conditions admit at
    least two distinct positive outer-even lifts at level 6, while the naive
    interlacing-depth rule has no positive lift beginning already at level 5.
    The protected algorithmic continuation and the paper lift share the same
    depth defect, so this refinement cannot distinguish their level-6
    chirality choices. See
    `graded_uplift/reports/GU5_LEVEL6_DIRECT_CLOSED_AND_DEPTH.md`.
13. **Current objective:** use the kernel generators, corrected shifts and
    GMSZ transported/core decomposition constructively to prove that every
    cumulative HFT character has at least one positive integral $SO(10)$ lift.
    A recurrence or finite-source module would suffice; it need not choose a
    unique point of the positive fibre. Matching the protected algorithmic
    continuation is a stronger secondary question and is not part of Bars'
    all-orders existence claim.
14. Use the protected levels 1--10 only as a later comparison layer, not as
    input to the construction.
