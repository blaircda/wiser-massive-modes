# Trajectory–Kernel Programme Status

**Last updated:** 25 September 2026

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
- GLPK reports exhaustion after respectively $1,2,2,3,6$ minimal source
  vectors. Every returned vector and exclusion cut is checked exactly, while
  exhaustion itself remains solver-backed. Non-uniqueness begins at level 8
  and persists.
- Adjacent optimal faces are compatible for $7\to8$ and $8\to9$, but not for
  $9\to10$ or $10\to11$.
- Every horizon-10 minimum has a level-9 prefix of charge 5 or 6, above the
  independent level-9 minimum 4. Every horizon-11 minimum has a level-10
  prefix of charge 12 or 13, above the independent level-10 minimum 11.
- Hence no witness is minimal at every cutoff from 7 through 11. Ungraded
  source sparsity is an exact finite optimization criterion but not a
  recursive analytic selector.
- See `reports/TK5C_MINIMAL_CORE_WITNESSES.md`.

## TK6a result

**TK6a — Principal restriction-kernel ideal: global ring presentation and
finite quotient analysis complete.**

- The fundamental-character restriction map is surjective and has the exact
  global kernel
  $\ker(\operatorname{Res})=(J)$, where $J=16_+-16_-$.
- A new exact triangular converter expresses finite $D_5$ characters as
  polynomials in the five fundamental characters and verifies every conversion
  back in the Weyl character ring.
- All eleven natural kernel generators in the baseline-free level-11 closure
  divide exactly by $J$.
- Every quotient is a positive integral $SO(10)$ character with unit
  coefficients. Two quotients are irreducible and nine are positive reducible
  characters.
- The finite-window quotient formulas are

$$
A_\ell/J=\sum_{i=0}^{\ell}[i,0,0,0,1],
\qquad 0\leq\ell\leq5,
$$

$$
B_\ell/J=\sum_{i=0}^{\ell}
\left([i+1,0,0,0,1]+[i,1,0,0,1]\right),
\qquad 0\leq\ell\leq2,
$$

$$
C_\ell/J=\sum_{i=0}^{\ell}[i,0,0,0,2],
\qquad 0\leq\ell\leq1.
$$

- In particular, the two nontransported TK5b seeds obey
  $A_0=16_-J$ and $C_0=126_-J$. They are different positive multiples of one
  global kernel generator, not algebraically independent ring-kernel
  directions.
- The partial-sum formulas are exact in the stated ranges but are not yet
  proved for arbitrary $\ell$.
- See `reports/TK6A_PRINCIPAL_KERNEL_IDEAL.md`.

## TK6b.1 result

**TK6b.1 — Finite positive restriction semigroup: exact cone and Hilbert-basis
audit complete through the baseline-free level-11 closure.**

- Collapsing outer-conjugate parents gives a binary multiplicity-free packet
  matrix with 73 $B_4$ rows, 84 $D_5$ columns, rank 73 and kernel rank 11.
- The all-chiral square submatrix has determinant one, so the columns generate
  the full ambient lattice $\mathbb Z^{73}$.
- Total unimodularity fails: an explicit $3\times3$ packet minor has
  determinant 2.
- The exact rational cone is 73-dimensional. All 84 packet columns are
  extreme rays, and its irredundant dual description has 2,508 facets.
- Despite the non-TU minor, the Normaliz Hilbert basis has exactly 84 elements
  and equals the packet columns. The finite semigroup is saturated and has no
  additional Hilbert generators.
- Hence, within this finite closure, an integral target has a positive
  integral lift if and only if it satisfies all rational facet inequalities.
- Every cumulative HFT target through level 11 satisfies all 2,508 facets and
  has a separately verified nonnegative integral packet decomposition.
- This does not prove saturation for arbitrary interlacing domains or that all
  future HFT targets satisfy a stable all-level family of inequalities.
- See `reports/TK6B1_POSITIVE_RESTRICTION_SEMIGROUP.md`.

## TK6b.2 result

**TK6b.2 — Facets as positive kernel circuits: finite classification complete
through the baseline-free level-11 closure.**

- Direct weight-space classification does not stabilize. At level 11, the
  2,508 facets retain 2,494 distinct leading-shift templates and 2,444
  full-translation templates. From level 10 to 11, 2,399 new translated
  templates appear.
- Only 14 of 63 eligible one-step leading-label shifts preserve a facet.
  Raw Dynkin translation is therefore not the organizing principle.
- In the 11-dimensional Gale transform supplied by the natural kernel basis,
  the 84 packet columns have only 29 distinct row types: one zero type, 22
  signed-coordinate types and six composite types.
- Those 29 rows obey one exact $A/B/C$ template consisting of zero, the signed
  coordinate vectors, the adjacent vectors $-e_{B_i}-e_{A_{i+1}}$, and three
  boundary sums over the available $A$, $B$ and $C$ chains. The template is
  exact at every tested nested horizon.
- All 2,508 facets are positive Gale circuits with unit coefficients. After
  quotienting repeated Gale rows, only 40 circuit types remain, and their
  combinatorial multiplicities reconstruct all facets exactly.
- With $c=U^{-1}m$ the triangular all-chiral section coordinates, every facet
  is a zero-one Hall-type inequality
  $\sum_{j\in S\cap\operatorname{Ref}}c_j\geq0$ for a positive circuit $S$.
- The circuit types still grow, from 23 at level 10 to 40 at level 11. The
  compact Gale-row rule, rather than a fixed finite circuit list, was the
  resulting candidate structure; TK6b.3 below refines it after new families
  enter.
- See `reports/TK6B2_FACET_CIRCUITS.md`.

## TK6b.3 result

**TK6b.3 — All-split boundary-shell theorem and first new-family obstruction
complete.**

- The compact TK6b.2 $A/B/C$ Gale-row rule is proved from the support
  collisions of the six-term kernel relations for arbitrary initial lengths
  of those three chains.
- More generally, every consecutive pair of allowed parents over
  $[\ell,m,r,s]_9$ obeys one universal six-term restriction-kernel identity.
  Its coefficients are $\pm1$, and interlacing-shell inclusion-exclusion
  proves it for arbitrary nonnegative labels and every
  $1\leq k\leq\lfloor s/2\rfloor$.
- Telescoping gives the natural relation between the $k$th parent and the
  all-chiral parent in closed form, with exactly $4k+2$ unit-coefficient terms.
  Exact branching, telescoping and independent chiral-section inversion agree
  for sampled splits through $k=3$.
- The actual HFT closure does not remain $A/B/C$-complete. At level 12, the
  domain has 92 $B_4$ rows, 108 packets and kernel rank 16. In addition to
  $A_6,B_3,C_2$, generators with top weights $(0,2,0,2)$ and $(0,0,1,2)$
  enter.
- All 16 level-12 generators are instances of the universal first-split
  identity. Their Gale matrix has 43 row types: one zero, 32 signed-coordinate
  and ten composite collision types.
- A raw level-13 HFT look-ahead extends the two new families and adds the tail
  $(m,r,s)=(1,0,3)$. Family growth is continuing.
- The revised all-orders object is an all-split collision hypergraph of local
  shell relations, not a fixed finite $A/B/C$ list.
- See `reports/TK6B3_BOUNDARY_SHELL.md`.

## TK6b.4 result

**TK6b.4 — Weighted-circuit obstruction and finite HFT audit through level 13
complete.**

- For every finite packet closure, primitive positive Gale circuits give an
  exact weighted liftability criterion in the triangular all-chiral section
  coordinates.
- Repeated Gale rows admit an exact compression: a circuit uses at most one
  realization of each row type, and expands by the product of the supported
  type multiplicities.
- The method reproduces the 2,508 level-11 facets exactly. The complete
  level-12 and level-13 closures have respectively 18,923 and 162,739 expanded
  facets.
- All 40 level-11 and 140 level-12 circuit types have unit coefficients. At
  level 13, eight of 495 primitive circuit types contain coefficient two. A
  ten-row, rank-nine relation is an exact minimal certificate.
- Independent synthetic all-split boxes also contain coefficient-two
  circuits. Hence the TK6b.2 subset-sum form is not a general branching
  theorem; the correct criterion is weighted.
- The cumulative HFT targets through level 13 satisfy every weighted circuit
  inequality and have exactly reconstructed nonnegative integral packet
  witnesses. This does not prove saturation of the level-12 or level-13
  semigroups.
- See `reports/TK6B4_WEIGHTED_CIRCUITS.md`.

## TK6b.5 result

**TK6b.5 — Local HFT pullback proved; all-orders positivity remains open.**

- The all-chiral triangular coordinate at $[\ell,m,r,s]_9$ is the exact
  three-fold forward difference of the $B_4$ target multiplicity in its first
  three orthogonal coordinates. In Dynkin labels this is an eight-term local
  formula, with zero extension outside the dominant chamber.
- Every weighted circuit inequality therefore pulls back to an explicit
  finite signed sum of HFT multiplicities. A circuit involving $t$ reference
  parents uses at most $8t$ multiplicity entries before cancellations.
- The formula is proved directly from multiplicity-free interlacing and has
  no mass-level cutoff. It agrees with independent exact triangular matrix
  inversion on the complete cumulative HFT closures through level 13.
- The finite-difference operator commutes exactly with cumulative level sums
  and Dynkin-label translations. Hence a GMSZ multiplicity shift on the full
  eight-point stencil transports the corresponding section coordinate and
  any simultaneously translated circuit slack.
- This supplies the analytic bridge from circuit facets to HFT coefficients,
  but not the missing positivity theorem. Circuits in a finite Gale matrix
  need not persist unchanged when later kernel coordinates are added. A
  recursive infinite-shell circuit classification, positivity of its HFT
  partial sums and a saturation or integral-packetization theorem remain
  open.
- See `reports/TK6B5_HFT_WEIGHTED_INEQUALITIES.md`.

## TK6b.5b/c result

**TK6b.5b/c — Prefix-shell duality proved; fixed finite circuits obstructed;
Regge-tail/Pieri route isolated.**

- Every natural shell coordinate has one unique non-chiral $+e_g$ pivot.
  Eliminating these pivots identifies the positive Gale cone exactly with
  $y\geq0$, $Ly\geq0$, where $L$ is the closed prefix-shell operator on
  all-chiral top labels.
- Positive liftability is equivalently a decomposition
  $c=u+L^Tz$ with $u,z\geq0$. The exact pairing identity
  $\langle y,c\rangle=\langle y,u\rangle+\langle Ly,z\rangle$ recovers the
  weighted criterion without enumerating circuits.
- The infinite operator is column-finite but not row-finite. Because the
  $Q_4$ packet forgets the leading label, every nonzero finitely supported
  $y\geq0$ violates a sufficiently distant shell inequality. Hence the full
  infinite system has no nonzero finitely supported positive circuit; finite
  facets are necessarily moving boundary-tail objects.
- For every fixed top-weight family and parent split, one universal interval
  tail is a primitive finite-horizon circuit. Its TK6B.5 Möbius pullback
  telescopes to at most eight HFT endpoint multiplicities, independent of the
  leading-label horizon.
- This bounded endpoint property is not universal. In the mixed box
  $0\leq m\leq1$, $r=0$, $2\leq s\leq4$, the largest pulled support grows
  from 24 at $\ell=0$ to 45 at $0\leq\ell\leq1$; the latter box has 4,900
  full circuits and coefficient two.
- Exact factorization of the HFT primary series by
  $\operatorname{PE}([1,0,0,0]_9q)$ reconstructs the series through level 13.
  All 185 eligible adjacent $\ell$ shifts in that window hold separately at
  every virtual remainder degree. Every observed degree-$d\geq2$ remainder
  term obeys $2\ell+2m+2r+s\leq d-1$.
- These finite facts isolated two all-orders lemmas: remainder support and
  stable $B_4$ Pieri transport. The latter is now proved in TK6b.5d; the
  contribution-wise remainder statement, mixed-tail recursion and integral
  packetization remain open.
- See `reports/TK6B5B_PREFIX_SHELL_DUALITY.md`.

## TK6b.5d result

**TK6b.5d — Stable $B_n$ Pieri translation proved; all-degree HFT coverage
remains open.**

- Racah--Speiser gives an exact all-rank theorem. For arbitrary tensorial or
  spinorial $B_n$ weights $\mu$ and $\lambda$, if
  $\lambda_1\geq\mu_1$ in orthogonal coordinates, then the multiplicity of
  $V_\lambda$ in $V_\mu\otimes H_k$ equals that of
  $V_{\lambda+\omega_1}$ in $V_\mu\otimes H_{k+1}$.
- Summing the harmonic decomposition of $\operatorname{Sym}^R(V)$ proves the
  corresponding consecutive symmetric-power identity. The possible extra
  scalar at alternating parity cannot contribute under the same inequality.
- The proof works uniformly on the integral and half-integral weight cosets.
  Chirality is therefore not an obstruction to this leading-coordinate
  transport theorem.
- A small exact character-ring regression tests 393 cases without failure.
  In the exact HFT factorization through level 13, all 524 active irrep-level
  couplings in the 185 eligible adjacent $\ell$ shifts lie in the theorem's
  stable range and match. They include 214 spinorial couplings and 44
  couplings with negative virtual-remainder coefficients.
- The remaining all-orders obligation is contribution-wise: prove that every
  remainder irrep which can couple to an exterior-chamber target satisfies
  the stable-range inequality, and that the new top-degree remainder misses
  the translated target. The observed half-slope bound alone is not logically
  sufficient because it also includes inactive remainder irreps.
- With $E(\ell,m,r,s)=2\ell+3m+\operatorname{cost}(r,s)$, all 176 remainder
  terms through degree 12 satisfy $E(\mu)\leq d+1$. More directly, all 363
  unstable HFT product terms through total degree 12 satisfy
  $E(\lambda)\leq d+R$, with minimum margin two; this inequality excludes the
  translated label from the GMSZ chamber exactly.
- That energy statement is HFT-specific. The generic shortcut
  $E(\lambda)\leq E(\mu)+R-1$ is false, with the exact counterexample
  $\mu=(1,0,2,1)$, $R=3$, $\lambda=(0,0,0,5)$. The next proof must therefore
  use the special remainder support or establish the combined HFT coupling
  inequality directly.
- A generator-wise plethystic proof is also obstructed: through degree 8,
  $PL[Z'_m]$ has 10 exterior-cost violations among 85 terms, with minimum
  margin $-3$, although $Z'_m$ itself satisfies the bound in that window.
- The proposed next route is a four-filtration Newton-cone argument on the
  exact HFT product. The four linear forms underlying $E$ are multiplicative
  representation-ring filtrations, and removing
  $\operatorname{PE}(qV)$ moves the remaining positive bosonic vector modes
  to degree at least two. The NS/R combination, massless subtraction and
  division by $qZ_Q$ are the unresolved cancellation steps.
- See `reports/TK6B5D_STABLE_PIERI_TRANSLATION.md`.

## MILP certification audit

- The unchecked objective rounding reported in `trajectory_selection.py` was
  confirmed, and raw integer-variable rounding occurred in the other audited
  MILP modules.
- A shared drift guard now checks every integer objective and extracted
  variable. Lexicographic stages, range endpoints, source witnesses, numerator
  identities and packet decompositions receive domain-specific exact primal
  verification.
- Global optimality, infeasibility and enumeration exhaustion remain backed by
  GLPK's floating-point branch-and-bound status unless an independent exact
  obstruction is supplied.
- See `reports/MILP_NUMERICAL_CERTIFICATION_AUDIT.md`.

## Next refinement

TK6b.3 resolves both the proposed $A/B/C$ continuation and the local
parent-split problem. TK6b.4 proves the exact finite weighted criterion,
TK6b.5 pulls it back to HFT multiplicities, and TK6b.5b/c shows that fixed
finite circuits cannot survive the infinite leading-label limit. TK6b.5d now
proves stable Pieri transport for tensorial and spinorial $B_n$ weights. The
next central step is to prove all-degree, contribution-wise stable-range
coverage for the HFT remainder, preferably in the equivalent exterior-cost
form $E(\lambda)\leq d+R$, then organize the horizon-dependent circuits as a
recursive boundary-tail module with a controlled mixed core. Saturation or
recursive integral packetization is still required separately. In parallel,
the TK6a partial-sum quotient formulas invite an all-$\ell$ tensor-product
proof.

TK5c separately rules out naive ungraded source sparsity as a cutoff-stable
selector. The oscillator-graded uplift suggested by hep-th/0310292 has now
been tested through level 7. Its outer-chirality-closed finite domain has a
unique paper solution but no rational refinement of the protected algorithmic
continuation at levels 6 and 7; the level-6 obstruction persists through
$\Delta_{\max}=10$. This is a finite-domain result, not an all-$\Delta$
theorem. GU3 then restores the Type-IIA opposite chirality and Bars'
$\ell'=n-\ell$ label. The fully resolved closed map remains injective and
forces the paper-times-conjugate candidate, which differs at levels 6 and 7
from the protected algorithmic continuation. Bars supplied no lift at those
levels. Thus a genuinely new direct closed construction must use the
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
5. The protected algorithmic and paper candidates have the same depth defect,
confirming that this depth is blind to their outer-chirality difference. See
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
- Are coefficients of primitive all-split circuits uniformly bounded, or can
  they grow with the collision hypergraph?
- Is every finite downward-closed $D_5\downarrow B_4$ packet semigroup
  saturated, as the complete level-11 closure is?
- Can the horizon-dependent positive circuits be generated as a recursive
  boundary-tail module with a controlled mixed core?
- Can the weighted positive-circuit inequalities be derived directly from the
  HFT/GMSZ multiplicity recurrences without enumerating the cone facets?
- Can the observed HFT remainder bound
  $2\ell+2m+2r+s\leq d-1$ be proved at every degree, and combined with a
  stable $B_4$ Pieri theorem to derive the outer $\ell$ shift?
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
./bin/sage-run -m trajectory_kernel.principal_ideal --self-test
./bin/sage-run -m trajectory_kernel.principal_ideal --max-level 11
./bin/sage-run -m trajectory_kernel.restriction_semigroup --self-test
./bin/sage-run -m trajectory_kernel.restriction_semigroup --max-level 11
./bin/sage-run -m trajectory_kernel.interlacing_facets --self-test
./bin/sage-run -m trajectory_kernel.interlacing_facets --max-level 11 --min-level 5
./bin/sage-run -m trajectory_kernel.boundary_shell --self-test
./bin/sage-run -m trajectory_kernel.boundary_shell --max-level 12 --previous-level 11 --branch-check-ell 2 --split-check-max-s 6 --lookahead-level 13
./bin/sage-run -m trajectory_kernel.all_split_circuits --self-test
./bin/sage-run -m trajectory_kernel.all_split_circuits --hft-level 13 --verbose
./bin/sage-run -m trajectory_kernel.hft_weighted_inequalities --max-level 13
./bin/sage-run -m trajectory_kernel.shell_duality --self-test
./bin/sage-run -m trajectory_kernel.regge_factorization --max-level 13
```
