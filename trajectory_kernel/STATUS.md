# Trajectory–Kernel Programme Status

**Last updated:** 24 September 2026

This is the local status document for the new analytic programme. The root
`STATUS.md` remains authoritative for the project as a whole.

## Current status

**TK0 — Programme setup: complete.**

- The derivation/comparison boundary is documented.
- Package execution through `bin/sage-run -m ...` is supported.
- Minimal Regge-column label and shift primitives are implemented and tested.
- No positivity or hidden-symmetry result was claimed at this stage.

**TK1 — Baseline-free Regge-column extraction: complete through level 10,
with a level-11 support addendum.**

- The HFT $SO(9)$ spectrum gives 185 nonzero irreducible entries in 13
  fixed-$(m,r,s)$ columns and 56 reduced-depth orbits.
- The shift-invariant orbit coordinate is
  $\delta=n-\ell-3m$, not merely $n-\ell$.
- Of 134 adjacent comparisons, 80 match and 54 do not. Regge-shift invariance
  is therefore not a global multiplicity identity.
- Twenty-four orbits have a constant observed suffix of length at least two;
  19 of these suffixes have length at least three. This is finite-window
  evidence only.
- Thirty-two orbits remain unresolved; 13 have only one available point.
- HFT's finite-order observation that the third $B_4$ Dynkin label satisfies
  $a_3\leq1$ holds through level 10 in this convention but first fails at
  level 11:
  $2[0,0,2,0]_9$ occurs in the exact positive quotient $r_{11}^9$.
- This creates a new fixed-tail $SO(9)$ trajectory column at reduced depth
  $\delta=11$. It creates no new branching-kernel family because its fourth
  label is zero and its unique top parent is $[0,0,2,0,0]_{10}$.
- See `reports/TK1_REGGE_COLUMNS.md` for the complete finite-window audit.

**TK2 — Branching and kernel shift identities: complete.**

- Exact branching identity:
  $\operatorname{Res}(\sigma_DV)=\sigma_B\operatorname{Res}(V)+\partial V$,
  where $\partial V$ is the nonnegative multiplicity-free
  $\mu_1=\lambda_2$ boundary slice and is independent of $a_1$.
- On the level-10 finite closure, the restriction matrix has 57 rows, 65
  parent columns, rank 57 and kernel rank 8.
- Eight explicit six-term relations form an integral triangular kernel basis.
- Raw shifting preserves none of these eight generators. The chiral-section
  boundary-corrected shift preserves all eight and equals the next natural
  generator in every case.
- Seven generators lie on $\delta=6$ trajectories; the remaining generator
  begins a $\delta=10$ family.
- The seed over $[0,0,0,2]_9$ is the exact zero-restriction combination
  $210-126-120+45-10+1$.
- See `reports/TK2_BRANCHING_KERNEL_SHIFTS.md`.

**TK3 — Positive fibres in trajectory-kernel coordinates: complete through
level 10.**

- Every integral lift in the 65-parent domain has unique coordinates in the
  eight-generator TK2 kernel basis.
- Exact triangular bounds enumerate all positive lifts without a search
  cutoff.
- The positive-fibre counts at levels 1--10 are
  $1,1,1,1,1,1,2,8,72,6057$.
- The first forced correction is the 126/210 family-A seed at level 7.
- At level 10, the family-A coordinates must repair a scalar deficit of ten,
  and the family-B seed coordinate is also forced to be positive.
- The three TK2 families suffice in the finite window; no additional seed is
  required for positivity through level 10.
- Positivity is highly non-unique and does not yet supply an analytic selection
  rule.
- The optional stronger demand of nonnegative consecutive $SO(10)$ increments
  fails already at $1\to2$; it is not required for positive cumulative lifts.
- See `reports/TK3_POSITIVE_FIBRES.md`.

## Next milestone

**TK4 — Analytic trajectory selection: first experiment complete, programme
still open.**

- Local minimum population, support and boundary criteria are non-unique at
  level 10.
- Three global corrected-shift priorities are cutoff-stable but select
  different points; transport-first retains eight tied optimal paths.
- The baseline-free level-11 closure has 73 $B_4$ rows, 84 $D_5$ parent
  columns and kernel rank 11.
- Level 11 introduces only the shifted generators $A_5$, $B_2$ and $C_1$; no
  new fixed-tail seed family appears.
- Full-horizon integer optimization avoids materializing the large level-11
  fibre. All three priorities remain cutoff-stable, but their final optima are
  still non-unique and mutually different.
- Therefore minimal corrected-shift transport is an organizing principle but
  not a complete analytic selection principle.
- See `reports/TK4_SELECTION_EXPERIMENT.md`.

## TK4b result

**TK4b — Kernel-valued generating-function constraints.**

**First TK4b tests: complete, with two obstructions.**

- The exact source transform is
  $S_F(q,t)=(1-qt)C_F(q,t)$, with $C_F$ the coordinate series and $S_F$ the
  source series. This notation avoids collision with the HFT fermionic $Z_F$.
- Strict boundary-only generation is possible through level 8 but impossible
  at level 9. Minimum interior-source charge is 1, 3 and 4 through horizons 9,
  10 and 11.
- Exact positive HFT numerator compatibility
  $N_n^{10}=Z_Q^{10}(L_n-L_{n-1})$ fails already at level 2.
- The fixed level-2 remainder has dimension zero, restricts to zero, and equals
  $-2A_0+J_{126}$, where $J_{126}$ is the outer-chirality difference.
- Thus direct M4 division is algebraically incompatible with the positive
  cumulative lifts, not merely difficult for the peeling algorithm.
- See `reports/TK4B_KERNEL_GENERATING_SERIES.md`.

## TK4c result

**TK4c — Structured kernel anomaly: first class-level analysis complete.**

- The lift-independent object is
  $[\kappa_n]\in\ker(\operatorname{Res})/
  Z_Q^{10}\ker(\operatorname{Res})$.
- Exact Laurent-ring division proves that $[\kappa_2]\neq0$. Thus the
  level-2 obstruction cannot be removed by any virtual kernel correction;
  positivity is not the cause of the failure.
- The representative remains
  $\kappa_2=-2A_0+J_{126}$, but the complete character is outer-chirality even.
- Corrected shifts of this seed do not equal the later reference anomalies,
  beginning at level 3 and continuing through level 11.
- Generic regular-torus certificates show that
  $[\kappa_2],\ldots,[\kappa_6]$ are nonzero and linearly independent, and
  that the later classes do not lie in the span of the shifted seed orbit.
- The affine change of representative under three positive lift paths was
  checked exactly through level 11.
- See `reports/TK4C_KERNEL_ANOMALY.md`.

The protected $SO(10)$ data were not consulted.

## TK4d result

**TK4d — Exact closed-string level-2 test: complete.**

- The intrinsic closed universal factor
  $Q_{\mathrm{cl}}=\bigoplus_{j=0}^{16}\Lambda^j\mathbf{16}$ is an
  outer-even positive $SO(10)$ character of dimension 65,536.
- Its restriction is exactly $(Z_Q^9)^2$.
- It is not equal to either literal product $z^2$ or $z\tau(z)$ of the
  virtual chiral HFT uplift; both differences lie in the restriction kernel.
- The raw same- and opposite-chirality products are already nonpositive at
  level 1.
- At level 2, neither $N_2^2$ nor $N_2\tau(N_2)$ is divisible by
  $Q_{\mathrm{cl}}$ in the exact Laurent weight ring.
- Therefore “uplift each chiral half, then tensor” does not cure the quotient
  obstruction. This does not rule out a direct closed construction that
  combines left and right before uplifting.
- See `reports/TK4D_CLOSED_LEVEL2.md`.

## TK5a result

**TK5a — GMSZ support-chamber and shift audit: complete through level 11.**

- The empirical GMSZ support polytope is exact at every tested level in its
  claimed domain $n>6$: the predicted and HFT-derived support counts are
  $23,32,43,56,72$ at levels 7--11, with no missing or unexpected irreps.
- The published formula is not claimed below level 7. Its low-level extra
  predictions have been recorded as diagnostics rather than counterexamples.
- All 253 admissible $\ell$-shift relations and all 50 admissible $m$-shift
  relations pass exactly. No $r$-shift relation is admissible through level
  11, so that family remains untested.
- For adjacent Regge comparisons with target level at least 7, the GMSZ
  $\ell$ chamber contains 95 comparisons, all matching. Outside the chamber,
  72 of 75 comparisons fail.
- Thus the chamber inequality sharply explains the TK1 mixture of matches and
  failures. It does not yet select an $SO(10)$ representative.
- See `reports/TK5A_GMSZ_CHAMBER_AUDIT.md`.

## TK5b result

**TK5b — Transported/core decomposition and kernel sources: complete through
level 11.**

- The published priority $\ell$, then $m$, then $r$, with the largest
  admissible step first, gives a deterministic partition into transported
  irreps and residual core. Every selected multiplicity identity is exact.
- The residual-core irrep counts at levels 7--11 are $13,17,22,30,37$; the
  core is growing and is not a thin finite-width boundary in this window.
- The level-11 finite kernel has 11 generators. Eight first appear by
  $\ell$-transport, one by $m$-transport, one in the pre-chamber range and one
  in the residual core.
- Every transported kernel generator is exactly the corrected D5 shift of its
  GMSZ source generator. The former family-B seed $B_0$ is the corrected
  $m$-shift of $A_0$.
- Consequently the full finite kernel lattice is generated from the two
  nontransported objects $A_0$ and $C_0$.
- Strict $\ell=0$ coordinate sources remain feasible only through level 8.
  Allowing a source precisely when its generator top weight lies in the GMSZ
  residual core gives positive cumulative lifts through level 11.
- This establishes existence of a core-supported path in the finite window,
  not uniqueness, canonicity or an all-orders theorem.
- See `reports/TK5B_CHAMBER_CORE_KERNEL_SOURCES.md`.

## TK5c result

**TK5c — Minimal core-supported witnesses: complete through level 11.**

- Lexicographically minimizing first the number of nonzero sources and then
  their absolute charge gives minima
  $(1,1),(2,2),(3,4),(5,11),(7,20)$ at horizons 7--11.
- Exact enumeration gives respectively $1,2,2,3,6$ minimal source vectors.
  Non-uniqueness therefore begins at level 8 and persists.
- Adjacent optimal faces are compatible for $7\to8$ and $8\to9$, but not for
  $9\to10$ or $10\to11$.
- Every horizon-10 minimum has a level-9 prefix of charge 5 or 6, above the
  independent level-9 minimum 4. Every horizon-11 minimum has a level-10
  prefix of charge 12 or 13, above the independent level-10 minimum 11.
- Hence no witness is minimal at every cutoff from 7 through 11. Ungraded
  source sparsity is an exact finite optimization criterion but not a
  recursive analytic selector.
- See `reports/TK5C_MINIMAL_CORE_WITNESSES.md`.

## Next refinement

TK5c rules out naive ungraded source sparsity as a cutoff-stable selector. The
remaining algebraic chamber question is whether core-supported feasibility
follows from a closed recurrence or finite source module without a minimality
prescription. The separate oscillator-graded uplift suggested by
hep-th/0310292 has now been tested through level 7. Its outer-chirality-closed
finite domain has a unique paper solution but no rational Bars solution at
levels 6 and 7; the level-6 obstruction persists through
$\Delta_{\max}=10$. This is a finite-domain result, not an all-$\Delta$
theorem. GU3 then restores the Type-IIA opposite chirality and Bars'
$\ell'=n-\ell$ label. The fully resolved closed map remains injective and
forces the paper-times-conjugate candidate, which still differs from Bars at
levels 6 and 7. Thus a genuinely new direct closed construction must use the
IIA/M-theory labels without imposing the IIB $\Delta$ grading separately on
each chiral factor. See `../graded_uplift/STATUS.md`. The direct closed-uplift
question and the class-valued anomaly series remain open; neither should be
conflated with the GMSZ chamber results.

GU4 has now begun the direct closed test. Through level 3, positivity plus
outer invariance gives a unique closed lift; at level 3 it reduces 27 positive
lifts to one. The Bars label $\ell'$ is realized exactly as factorwise
$D_5\downarrow B_4$ interlacing depth, while individual $\ell'$ source blocks
do not lift positively on their own. This is a low-level result and does not
yet settle the first restriction-kernel ambiguity. See
`../graded_uplift/reports/GU4_DIRECT_CLOSED_LOW_LEVELS.md`.

GU5 has now tested that ambiguity. Two distinct baseline-free positive
outer-even closed lifts exist at level 6, so closed outer invariance is not a
selector there. Moreover the naive identification of $\ell'$ with ordinary
$D_5\downarrow B_4$ interlacing depth has no positive lift starting at level
5. The Bars and paper candidates have the same depth defect, confirming that
this depth is blind to their outer-chirality difference. See
`../graded_uplift/reports/GU5_LEVEL6_DIRECT_CLOSED_AND_DEPTH.md`.

## Open questions

- Can the empirically exact GMSZ chamber inequalities and shift identities be
  derived from the HFT oscillator product?
- Is the complement of the transported chamber described by finitely many
  source types after passage to the $D_5\downarrow B_4$ kernel coordinates?
- Is the core-supported positive path unique after restoring the oscillator
  excitation-number grading discarded by the ungraded HFT quotient?
- What baseline-free analytic condition selects among the 6,057 positive
  level-10 lifts?
- Does the absence of a new seed family at level 11 persist at higher levels?
- Is there an independent finite-source construction of the class-valued
  kernel anomaly series $\mathcal K(q)$, despite failure of the one-seed ansatz?
- Can the level-matched closed HFT series be uplifted directly so that its
  level-1 coefficient is $Q_{\mathrm{cl}}$, without using chiral virtual
  tensor products?
- The exact first occurrences $[0,0,1,0]_9\subset r_5^9$ and
  $2[0,0,2,0]_9\subset r_{11}^9$ suggest the conjectural support bound
  $n\geq6a_3-1$. Can this be derived from the HFT oscillator product, and does
  $[0,0,3,0]_9$ first occur at level 17? This is a prediction, not a result.

## Reproduction

```text
./bin/sage-run -m trajectory_kernel.regge_columns --self-test
./bin/sage-run -m trajectory_kernel.regge_columns --max-level 10
./bin/sage-run -m trajectory_kernel.kernel_lattice --self-test
./bin/sage-run -m trajectory_kernel.kernel_lattice --max-level 10
./bin/sage-run -m trajectory_kernel.correction_ansatz --self-test
./bin/sage-run -m trajectory_kernel.correction_ansatz --max-level 10
./bin/sage-run -m trajectory_kernel.trajectory_selection --self-test
./bin/sage-run -m trajectory_kernel.trajectory_selection --max-level 10 --verbose
./bin/sage-run -m trajectory_kernel.trajectory_selection --max-level 11 --probe-next-level
./bin/sage-run -m trajectory_kernel.kernel_generating_series --self-test
./bin/sage-run -m trajectory_kernel.kernel_generating_series --max-level 11
./bin/sage-run -m trajectory_kernel.kernel_anomaly --self-test
./bin/sage-run -m trajectory_kernel.kernel_anomaly --max-level 11 --certificate-level 6
./bin/sage-run -m trajectory_kernel.closed_level2 --self-test
./bin/sage-run -m trajectory_kernel.closed_level2
./bin/sage-run -m trajectory_kernel.chamber_audit --self-test
./bin/sage-run -m trajectory_kernel.chamber_audit --max-level 11
./bin/sage-run -m trajectory_kernel.chamber_core --self-test
./bin/sage-run -m trajectory_kernel.chamber_core --max-level 11
./bin/sage-run -m trajectory_kernel.chamber_witness --self-test
./bin/sage-run -m trajectory_kernel.chamber_witness --max-level 11 --enumeration-cap 20
```
