# All-Orders Bars III.B Research Implementation Plan

**Created:** 25 September 2026

**Status:** active research plan; TK6A, TK6B.1, finite TK6B.2, the TK6B.3
all-split boundary-shell theorem, finite TK6B.4 weighted circuits, the TK6B.5
local HFT pullback, the TK6B.5b/c prefix-shell/Regge-tail reduction and the
TK6B.5d stable Pieri theorem completed; TK6B.5e reduced the remaining
stable-range premise to an explicit filtered HFT support theorem, and
TK6B.5f has proved that support theorem at all oscillator degrees

**Last updated:** 30 September 2026

## Objective

The central target is an all-orders existence proof for the minimal Bars
III.B proposal. Given the perturbative characters

$$
r_n^9\in R(\operatorname{Spin}(9)),
$$

define

$$
R_n^9=\sum_{i=1}^n r_i^9.
$$

The required theorem is that, for every $n$, there is at least one positive
integral $\operatorname{Spin}(10)$ character $X_n$ such that

$$
X_n\downarrow\operatorname{Spin}(9)=R_n^9.
$$

Bars did not require uniqueness or prescribe an all-level chirality choice.
Agreement with the protected algorithmic continuation through level 10 is a
stronger secondary comparison, not part of the theorem.

Two logical statements must remain separate:

1. every HFT-derived $r_n^9$ is a positive integral $\operatorname{Spin}(9)$
   character;
2. every cumulative $R_n^9$ has a positive integral
   $\operatorname{Spin}(10)$ lift.

The first implementation target may prove the second statement conditional on
the first. Any final theorem must state explicitly whether perturbative
positivity is assumed or proved.

## Track A — Principal restriction-kernel ideal

### A1. Global representation-ring presentation

Implement the restriction of fundamental characters

$$
10\mapsto1+9,
$$

$$
45\mapsto9+36,
$$

$$
120\mapsto36+84,
$$

$$
16_+\mapsto16,
$$

$$
16_-\mapsto16.
$$

Using polynomial generation by fundamental characters, verify the exact
presentation

$$
\ker\!\left(R(\operatorname{Spin}(10))\to
R(\operatorname{Spin}(9))\right)=(J),
$$

where

$$
J=16_+-16_-.
$$

The implementation must convert exactly between irreducible-character
coordinates and polynomials in the fundamental characters.

### A2. Divide the finite kernel generators by $J$

For every natural restriction-kernel generator in the baseline-free level-11
closure, compute and verify

$$
K=JH.
$$

Classify each quotient $H$ as positive irreducible, positive reducible or
virtual, and study its behavior under the corrected GMSZ shifts. In particular,
verify

$$
A_0=16_-J,
$$

$$
C_0=126_-J,
$$

up to the fixed chirality convention.

### A3. Auxiliary kernel series

Choose a fixed virtual ring section $s$. Rewrite baseline-free positive lifts
as

$$
X_n=s(R_n^9)+JH_n.
$$

Study

$$
H(q)=\sum_nH_nq^n
$$

under corrected $\ell$-shifts, GMSZ $m$-shifts, multiplication by fundamental
characters and outer conjugation. Continue toward a recurrence only if the
quotients occupy a demonstrably smaller module than the original kernel
coordinates.

### TK6A deliverables

- `trajectory_kernel/principal_ideal.py`
- `trajectory_kernel/reports/TK6A_PRINCIPAL_KERNEL_IDEAL.md`
- exact self-tests and a level-11 quotient analysis

The milestone succeeds when every tested finite kernel generator factors
exactly through $J$. Failure of the quotients to simplify further must be
reported rather than hidden.

## Track B — Positive restriction semigroup

### B1. Exact covering formulation

For a finite $B_4$ target

$$
Y=\sum_\mu m(\mu)[\mu],
$$

construct every relevant $D_5$ parent. Collapse outer-conjugate parents into
one unoriented column, because chirality orientation is irrelevant to
existence. Form the exact nonnegative integer system

$$
Ax=m,
$$

$$
x\in\mathbb Z_{\geq0}.
$$

Each column is the indicator of a multiplicity-free interlacing packet.

### B2. Integrality audit

For increasing finite closures:

- test total unimodularity;
- compute rational cone facets;
- compute the Hilbert basis of the integer semigroup;
- compare the Hilbert basis with the original branching columns;
- search for integral holes in the rational cone.

Do not assume that saturation of the individual branching-pair semigroup
implies normality of this character-covering semigroup.

### B3. Farkas and Hall inequalities

Compute the extremal rays of the dual cone and seek a combinatorial
description in terms of:

- downward-closed sets in the interlacing poset;
- alternating finite differences;
- lower boundary slices;
- Hall-type neighborhood inequalities;
- Möbius transforms of the multiplicity function.

Allow primitive circuit coefficients greater than one: TK6B.4 proves that
zero-one subset inequalities already fail at HFT level 13. Classify the finite
weighted inequalities under the GMSZ $\ell$, $m$ and $r$ shifts.

### B4. Constructive packetization

Develop an exact algorithm which groups copies of $B_4$ irreps into complete
interlacing packets. Candidate implementations include global-slack peeling,
network flow, Hall matching and Möbius inversion followed by controlled kernel
redistribution. On failure, return an exact obstruction certificate.

### B5. Inductive theorem

If the facet or packet types stabilize, or admit a uniform recursive
generation rule, prove preservation under the GMSZ transported shifts and
reduce the all-orders theorem to residual-core inequalities. The core need
not be finite; a finite or recursively controlled family of weighted
inequality or packet types is sufficient.

### TK6B deliverables

- `trajectory_kernel/restriction_semigroup.py`
- `trajectory_kernel/interlacing_facets.py`
- `trajectory_kernel/boundary_shell.py`
- `trajectory_kernel/all_split_circuits.py`
- `trajectory_kernel/hft_weighted_inequalities.py`
- `trajectory_kernel/shell_duality.py`
- `trajectory_kernel/regge_factorization.py`
- `trajectory_kernel/stable_pieri.py`
- `trajectory_kernel/reports/TK6B1_POSITIVE_RESTRICTION_SEMIGROUP.md`
- `trajectory_kernel/reports/TK6B2_FACET_CIRCUITS.md`
- `trajectory_kernel/reports/TK6B3_BOUNDARY_SHELL.md`
- `trajectory_kernel/reports/TK6B4_WEIGHTED_CIRCUITS.md`
- `trajectory_kernel/reports/TK6B5_HFT_WEIGHTED_INEQUALITIES.md`
- `trajectory_kernel/reports/TK6B5B_PREFIX_SHELL_DUALITY.md`
- `trajectory_kernel/reports/TK6B5D_STABLE_PIERI_TRANSLATION.md`

## Track C — BBMS cumulative positivity

### C1. Generate rather than transcribe the graded candidate

Extend the existing refined oscillator and branching machinery. At every
level:

1. derive the $(\ell,\nu)$-graded $SO(8)$ target;
2. construct the complete finite $(\lambda,\Delta)$ candidate domain;
3. solve the exact graded branching system;
4. verify uniqueness where the matrix has full column rank;
5. forget $\Delta$;
6. cumulatively sum;
7. test $SO(10)$ positivity and exact $SO(9)$ restriction.

Initially extend the existing computation beyond level 7 as far as exact
arithmetic remains practical. No protected $SO(10)$ data may enter this
derivation.

### C2. Telescoping ansatz

For the virtual single-level characters, search for

$$
V_n^{\mathrm{BBMS}}=P_n+C_n-C_{n-1},
$$

with $P_n$ and $C_n$ positive. Construct a cancellation graph pairing every
negative tagged irrep with its positive predecessor or successor and recording
all unmatched boundary terms.

### C3. Filtration or complex

If the cancellation graph is uniform, reinterpret it as a filtered module,
two-term complex, spectral sequence or sign-reversing involution. An
all-orders positive BBMS lift proves Bars III.B existence even if its IIB
chirality choice has no established IIA interpretation.

### GU6 deliverables

- `graded_uplift/bbms_cumulative.py`
- `graded_uplift/bbms_cancellation_graph.py`
- `graded_uplift/reports/GU6_BBMS_CUMULATIVE_POSITIVITY.md`

## Integration

For any two positive lift constructions, compare their auxiliary characters
in

$$
X_n=s(R_n^9)+JH_n.
$$

In particular compare BBMS lifts, interlacing-packet lifts and existing
baseline-free finite witnesses. This may reveal that apparently distinct
completions are different positive realizations of a small $J$-module.

Only one of the following final proof forms is required:

1. a cone theorem showing that every cumulative HFT character satisfies the
   complete liftability inequalities;
2. a constructive theorem giving an all-level packetization algorithm;
3. a BBMS theorem showing that the graded virtual series telescopes to a
   positive cumulative $SO(10)$ series.

## Milestones

| Milestone | Deliverable | Success criterion |
| --- | --- | --- |
| TK6A | Principal-kernel implementation and report | Every tested kernel relation factors exactly through $J$ |
| TK6B.1 | Finite restriction-semigroup audit | Exact cone, Hilbert-basis and obstruction data through level 11 |
| TK6B.2 | Facet or packet conjecture | Stable, explicitly stated candidate all-level criterion |
| TK6B.3 | Boundary-shell induction | Prove or obstruct the $A/B/C$ continuation and derive every parent-split relation |
| TK6B.4 | All-split circuit criterion | Establish the weighted criterion and identify whether unit circuits persist |
| TK6B.5 | HFT weighted inequalities | Prove every cumulative target satisfies all weighted circuit inequalities |
| TK6B.5d | Stable Pieri transport | Prove consecutive symmetric-power translation in both weight cosets and isolate its HFT support hypothesis |
| TK6B.5e | Finite Pieri hazard | Derive the exact source threshold and reduce HFT stable-range coverage to a closed filtered-divisibility statement |
| TK6B.5f | Analytic HFT support | Prove the filtered-divisibility statement by exact oscillator telescoping and a level-independent finite certificate |
| GU6.1 | Generated BBMS levels beyond 7 | Exact graded reconstruction, cumulative positivity and restriction checks |
| GU6.2 | Telescoping analysis | Uniform cancellation rule or exact first obstruction |
| Final | All-orders argument | Baseline-free existence proof with all assumptions stated |

## Progress record

**TK6A is complete.** The global restriction kernel is the principal ideal
generated by $J=16_+-16_-$. All eleven natural generators in the baseline-free
level-11 closure factor exactly through $J$, and all eleven quotients are
positive integral $SO(10)$ characters. The observed $A$, $B$ and $C$ quotient
families obey exact partial-sum formulas throughout the tested window. Those
formulas remain conjectural for arbitrary trajectory length. See
`trajectory_kernel/reports/TK6A_PRINCIPAL_KERNEL_IDEAL.md`.

**TK6B.1 is complete.** The level-11 unoriented packet matrix has 73 rows and
84 columns. It is not totally unimodular, but its exact Hilbert basis is
precisely the 84 packet columns, so the finite semigroup is saturated. Its
rational cone has 2,508 irredundant facets, and every cumulative HFT target
through level 11 satisfies them and has an exact integral packet witness.
TK6B.2 and TK6B.3 record the subsequent circuit classification and first
boundary-shell correction. See
`trajectory_kernel/reports/TK6B1_POSITIVE_RESTRICTION_SEMIGROUP.md`.

**Finite TK6B.2 is complete.** Direct weight-space facet templates proliferate,
but the 2,508 level-11 facets reduce to 40 positive-circuit types of 29 Gale
row types in the eleven natural kernel coordinates. The Gale rows obey one
compact $A/B/C$ template, every circuit coefficient is one, and every facet is
a zero-one subset-sum inequality in the triangular section coordinates. The
circuit list itself has not stabilized. TK6B.3 subsequently shows that the
$A/B/C$ list is not complete beyond level 11. See
`trajectory_kernel/reports/TK6B2_FACET_CIRCUITS.md`.

**TK6B.3 is complete as a local all-split theorem and through the first
untested HFT shell.** The $A/B/C$ row template is proved for arbitrary lengths
of those three chains. More generally, every consecutive pair of allowed
parents obeys a universal six-term interlacing-shell identity, and telescoping
gives the exact $4k+2$-term natural relation for the $k$th parent. The formula
is proved for arbitrary labels and splits and checked by exact branching and
independent chiral-section inversion through $k=3$. However, the actual HFT
closure acquires two new kernel families at level 12, so the former
$A/B/C$-completeness conjecture is false. The level-12 Gale rows remain sparse
and are exactly the signed incidence rows of collisions among the local shell
relations. Raw level-13 HFT support shows further family growth. The
replacement all-level candidate is a growing all-split collision hypergraph.
See
`trajectory_kernel/reports/TK6B3_BOUNDARY_SHELL.md`.

**Finite TK6B.4 is complete as a criterion and obstruction audit.** Primitive
positive circuits of the universal Gale rows give the exact weighted finite
liftability inequalities, and repeated Gale row types admit an exact
compression. The unit-coefficient conjecture is false: eight of the 495
level-13 HFT circuit types have coefficient two, with an explicit minimally
supported certificate. The compression gives 2,508, 18,923 and 162,739 facets
at HFT horizons 11, 12 and 13. Every cumulative target through level 13
satisfies the corresponding weighted inequalities and has an exactly checked
positive integral packet witness. This is not an all-orders circuit
classification, HFT inequality proof or saturation theorem. See
`trajectory_kernel/reports/TK6B4_WEIGHTED_CIRCUITS.md`.

**TK6B.5 has completed the local analytic reduction, but not the positivity
milestone.** The all-chiral triangular inverse is an explicit eight-term
Möbius difference of the $B_4$ multiplicity function. Hence every weighted
circuit pulls back to a finite signed HFT multiplicity functional. The
operator commutes with cumulative sums and with Dynkin-label translations,
which gives the exact intertwiner needed for a GMSZ/core induction. The
formula agrees with independent exact matrix inversion throughout the full
level-13 HFT closure. What remains is a recursive classification of circuits
in the growing shell matrix, positivity of the resulting HFT partial sums and
a general saturation or integral-packetization theorem. See
`trajectory_kernel/reports/TK6B5_HFT_WEIGHTED_INEQUALITIES.md`.

**TK6B.5b/c has replaced the fixed-circuit strategy by a boundary-tail
strategy.** Unique non-chiral pivot rows can be eliminated exactly, leaving
the uniform prefix-shell cone $y\geq0$, $Ly\geq0$. The complete infinite
operator has no nonzero finitely supported positive ray, so finite-horizon
circuits cannot stabilize as fixed objects. Universal split-chain tails do
have bounded endpoint pullbacks, but mixed circuits show growing pullback
support. Separately, the exact HFT factorization by
$\operatorname{PE}([1,0,0,0]q)$ makes all 185 tested $\ell$ shifts through
level 13 hold term by term in the virtual remainder. The next exact targets
were an all-degree remainder-support theorem and a stable $B_4$ Pieri lemma,
followed by recursive control of mixed boundary tails. See
`trajectory_kernel/reports/TK6B5B_PREFIX_SHELL_DUALITY.md`.

**TK6B.5d proves the stable Pieri lemma.** A Racah--Speiser stabilizer
argument proves consecutive harmonic and symmetric-power transport for every
tensorial or spinorial $B_n$ weight once the target before translation has
first orthogonal coordinate at least that of the remainder irrep. Through
level 13, all 524 active irrep-level HFT remainder couplings in the 185
eligible adjacent shifts satisfy this hypothesis, including 214 spinorial
and 44 negative-coefficient couplings. The remaining all-orders step is not
the Pieri identity but contribution-wise stable-range coverage for the HFT
remainder. The equivalent exterior-cost estimate passes for all 363 unstable
product terms through total degree 12, while a generic Pieri-cost shortcut has
an exact counterexample. The bound also fails termwise on $PL[Z'_m]$, so the
proof must use the special HFT coefficient recurrence and its cancellations.
See
`trajectory_kernel/reports/TK6B5D_STABLE_PIERI_TRANSLATION.md`.

**TK6B.5e replaces the proposed four-filtration route.** Each of the four
linear exterior-cost pieces has an exact tensor-product counterexample, so
none is a multiplicative representation-ring filtration. The correct
coupling-aware invariant is the finite harmonic hazard
$H(\mu)=\max(E(\lambda)-k)$ over unstable constituents. Its source threshold
$K(\mu)=\max(E(\mu)-1,H(\mu))$ has a closed wall-piecewise affine formula,
proved in both tensorial and spinorial weight cosets. Every HFT remainder term
through degree 12 satisfies $K(\mu)\leq d$. Exact all-order oscillator
identities now express $qZ_QF$ and the all-vector-free core as explicit
NS/R--Euler numerators. The remaining theorem is their filtered divisibility
into the wall module $K(\mu)\leq d$, not a further search for tensor-product
filtrations. See
`trajectory_kernel/reports/TK6B5E_PIERI_HAZARD.md`.

**TK6B.5f proves the filtered HFT support theorem.** Triality on the common
$D_4/B_4$ torus gives an exact Green--Schwarz telescope for the virtual
remainder. The finite Weyl/Dirac map does not raise the chirality-folded wall
degree, and uniform vector/spinor bounds close the infinite oscillator tail.
Horizontal-strip upper bounds leave five pivot classes and 323 exact
low-mode records; all pass with minimum margin zero. Thus
$[V_\mu]F_d\neq0\Rightarrow d\geq K(\mu)$ at every degree. This closes the
HFT premise of stable Pieri transport but not the later recursive-circuit or
integral-packetization step. See
`trajectory_kernel/reports/TK6B5F_ANALYTIC_HFT_SUPPORT.md`.

**The floating-point MILP audit is complete.** Integer objectives and variables
now have drift guards and all positive primal witnesses receive exact
domain-specific verification. GLPK optimality, infeasibility and enumeration
exhaustion remain solver-backed rather than exact certificates. See
`trajectory_kernel/reports/MILP_NUMERICAL_CERTIFICATION_AUDIT.md`.

## Research safeguards

- Never import the protected baseline in a derivation module.
- Keep all protected comparisons in explicitly named verification scripts.
- Use exact integer or rational arithmetic.
- Do not repair a failed construction with known level-1--10 answers.
- Treat nonuniqueness as expected rather than as an error.
- Distinguish $\operatorname{Spin}$ representation-ring statements from loose
  $SO$ terminology whenever spinors are present.
- Update the status documents only after a milestone has a reproducible script
  and report.

## Execution order

1. TK6A is complete and supplies the algebraic language needed by both later
   tracks.
2. TK6B.1 is complete: the finite cone and semigroup are known exactly through
   level 11.
3. TK6B.3 proves the shell identity for every parent split and refutes a fixed
   $A/B/C$ family list. Finite TK6B.4 proves the weighted-circuit criterion and
   refutes unit coefficients. TK6B.5 now supplies the local HFT pullback; its
   continuation shows that fixed finite circuits cannot stabilize. TK6B.5d
   proves the stable Pieri theorem, TK6B.5e reduces its contribution-wise HFT
   premise to filtered divisibility, and TK6B.5f proves that support theorem.
   Control coherent boundary-tail families and establish the resulting
   partial-sum inequalities.
4. Extend the BBMS construction beyond level 7 and test telescoping as an
   independent possible shortcut.
