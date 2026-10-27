# All-Orders Bars III.B Research Implementation Plan

**Created:** 25 September 2026

**Status:** active research plan; TK6A, TK6B.1, finite TK6B.2, the TK6B.3
all-split boundary-shell theorem, finite TK6B.4 weighted circuits, the TK6B.5
local HFT pullback, the TK6B.5b/c prefix-shell/Regge-tail reduction and the
TK6B.5d stable Pieri theorem completed; TK6B.5e reduced the remaining
stable-range premise to an explicit filtered HFT support theorem, and
TK6B.5f has proved that support theorem at all oscillator degrees; TK6B.6e
has isolated the primitive DDF/Koszul quotient and its exact gamma-traceless
top symbol required by the remaining scalar sign theorem, together with a
canonical cumulative $B_4$ Koszul core positive through degree 20;
TK6B.6g now gives the exact full gamma-trace triangle and local transfer
operators needed to combine projected wedge with the multiplicity-side
Clifford action

**Last updated:** 13 October 2026

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
- `trajectory_kernel/hft_analytic_support.py`
- `trajectory_kernel/cumulative_regge_uplift.py`
- `trajectory_kernel/scalar_boundary_functional.py`
- `trajectory_kernel/ddf_koszul_audit.py`
- `trajectory_kernel/gamma_symbol_complex.py`
- `trajectory_kernel/reports/TK6B1_POSITIVE_RESTRICTION_SEMIGROUP.md`
- `trajectory_kernel/reports/TK6B2_FACET_CIRCUITS.md`
- `trajectory_kernel/reports/TK6B3_BOUNDARY_SHELL.md`
- `trajectory_kernel/reports/TK6B4_WEIGHTED_CIRCUITS.md`
- `trajectory_kernel/reports/TK6B5_HFT_WEIGHTED_INEQUALITIES.md`
- `trajectory_kernel/reports/TK6B5B_PREFIX_SHELL_DUALITY.md`
- `trajectory_kernel/reports/TK6B5D_STABLE_PIERI_TRANSLATION.md`
- `trajectory_kernel/reports/TK6B5E_PIERI_HAZARD.md`
- `trajectory_kernel/reports/TK6B5F_ANALYTIC_HFT_SUPPORT.md`
- `trajectory_kernel/reports/TK6B6_CUMULATIVE_REGGE_UPLIFT.md`
- `trajectory_kernel/reports/TK6B6_SCALAR_BOUNDARY_REDUCTION.md`

### B6. Target-specific cumulative Regge construction

Use the exact factorization

$$
Z_m(q)=\operatorname{PE}(qV_9)F(q)
$$

and the newly isolated cumulative core

$$
\widehat G(q)=
\frac{\sum_{j=0}^9(-q)^j\Lambda^jV_9}{1-q}\,Z_m(q),
$$

for which

$$
F(q)=(1-q)\widehat G(q),
$$

$$
\frac{Z_m(q)}{1-q}
=\operatorname{PE}(qV_9)\widehat G(q).
$$

The coefficients of $\widehat G$ are positive through degree 20 and its
restriction is the transverse series $G$. This is an exact character
factorization plus finite positivity evidence, not yet an actual free-module
or all-orders regular-sequence theorem. Together with the identity

$$
\operatorname{Res}\operatorname{PE}(qV_{10})
=\frac{\operatorname{PE}(qV_9)}{1-q}
$$

to replace the general packet problem by positivity of one explicit `D5`
series.  With $S$ the all-chiral triangular section, test and then prove

$$
\operatorname{PE}(qV_{10})
\left(S(F)-q^3J+A(q)A_0\right)\geq0,
$$

where $A(q)$ is fixed by the scalar diagonal of $S(F)$.  The finite
construction is positive through level 13.  The analytic tasks are:

1. prove coefficientwise nonnegativity of the scalar-tail series $A(q)$;
2. prove one-shell dominance of the $A_0$ correction outside the scalar;
3. use stable $D_5$ Pieri translation to reduce the moving upper chamber;
4. express the residual boundary coefficients through the Green--Schwarz
   telescope and close them by uniform tail bounds plus a finite low-mode
   certificate.

The first task has now been reduced further. If $C(q)=\sum c_Nq^N$ is the
one-row diagonal, the exact boundary value $b_8=0$ gives

$$
a_N=-\sum_{k\leq N}c_k\qquad(N\geq9).
$$

Writing the Green--Schwarz telescope as $F=(1-q)G$ identifies this prefix sum
with $[q^N]\Phi_q(G)$. The all-label functional $\Phi$ is supported on only
nine transverse `D4` rays; its interior values have a common $(1-q)^2$
factor and only five low-wall endpoint formulas remain exceptional. The next
implementation step is therefore a uniform sign proof for this finite-ray
index. The four adjacent-ray groupings are signed Euler series, not separate
Hilbert series, so the earlier literal state-injection proposal is rejected.
Instead use the exact decomposition

$$
\Phi_q(G)=(1-q)^2R_{\mathrm{st}}+\Omega,
$$

where $R_{\mathrm{st}}$ contains only stable first arms and $\Omega$ contains
the five actual endpoint multiplicity series. The scalar
coefficient is $a_N=W_N-I_N$, where
$I_N=R_{\mathrm{st},N}-2R_{\mathrm{st},N-1}+R_{\mathrm{st},N-2}$ and
$W_N=-[q^N]\Omega$. Prove the wall-dominance
inequality $W_N\geq I_N$ either by a direct constant-term estimate or by
constructing a cohomological model. For the latter, exploit the exact fact
that at fixed first modified-Frobenius arm the nine rays share one Regge
monomial and occupy a fixed nine-element slice of the $3\times2$ tail
rectangle. Use the exact rank-two Plücker factorization of its coefficient
vector as two exterior operations. Its Laplace expansion packages all nine
Weyl numerators into one bordered determinant, which should be applied
directly to the oscillator product. Clear its vector exterior denominator to
obtain the exact degree-seven numerator $N(t)$, and apply the adjoint
symmetric-vector operation to its eight fixed coefficients rather than
handling infinitely many arms. Since the vector tower is self-dual, move it
through the character inner product and cancel it against the vector-exterior
factor in $G$. Combine the endpoint terms and the relative $D_4/B_4$ Weyl
denominator to obtain the final scalar target

$$
\Phi_q(G)=\langle\mathscr C(q),Z_m(q)\rangle_{B_4},
$$

or, on the cumulative core,

$$
\Phi_q(G)=\left\langle
\sum_{k\geq0}q^k(R_k-R_{k+1}),\widehat G(q)
\right\rangle_{B_4},
$$

where

$$
R_k=[k,0,0,0]-[k-1,1,0,0]+[k-1,0,1,0].
$$

The latter identity is proved at all orders by nine exact boundary
coefficients followed by the order-eight $B_4$ Weyl-alternant recurrence. It
reduces the support to the three principal hook trajectories $(k)$, $(k,1)$
and $(k,1,1)$ and should be the preferred interface to orthosymplectic
lowest-weight modules.

The local symbol on those hooks is also known at all first-row lengths.
Projected contraction and exterior multiplication evaluated at a nonzero
vector give

$$
(k,1)\mathord\downarrow_{D_4}
\hookrightarrow
\bigl((k)\oplus(k,1,1)\bigr)\mathord\downarrow_{D_4},
$$

with cokernel
$1\oplus\bigoplus_{j=0}^{k-1}[j,0,1,1]_{D_4}$. Equivalently,
$(R_{k+1}-R_k)\downarrow_{D_4}=[k,0,1,1]_{D_4}$. The task is therefore to
lift this exact symbol to the mass-graded multiplicity modules of
$\widehat G$, rather than to search for a new representation-level map.
Apply the positive relative-Dirac half first. The three hooks then become
$[k,0,1,0]$, $[k-1,1,1,0]$ and $[k-1,0,2,1]$ in $D_4$, and their
$D_4\downarrow B_3$ telescope proves an injective degree-one map of free
$\operatorname{Sym}(8_v)$-modules for every $k$. Denote its cokernel by
$\mathcal C_k^{\mathrm{sym}}$; after tensoring with the physical multiplicity
module $\mathcal P$, the kernel of this *truncated* map is
$\operatorname{Tor}^{\operatorname{Sym}(8_v)}_1
(\mathcal C_k^{\mathrm{sym}},\mathcal P)$.
This Tor group should not be assumed to vanish. The five low-form
gamma-traceless modules admit explicit projected-wedge maps and the exact
polynomial resolution

$$
0\longrightarrow S_V(-4)U_0\longrightarrow S_V(-3)U_1
\longrightarrow S_V(-2)U_2\longrightarrow S_V(-1)U_3
\longrightarrow S_VU_4\longrightarrow\mathcal T\longrightarrow0,
$$

where $S_V=\operatorname{Sym}(8_v)$ and
$\mathcal T_n=[n,0,3,0]_{D_4}$. Its nonzero null fibre has
twenty-dimensional homology in each of its last two positions. The correct
physical operation is therefore the derived tensor product of this complete
resolution, not a flatness assertion for its final two terms.
The local combination with the multiplicity-side Clifford symbol is also now
fixed. On the full spinor-form spaces $A_p^\epsilon$, the four operators
$\Gamma$, $G$, $E_v$ and $C_v$ satisfy

$$
\Gamma E_v+E_v\Gamma=C_v,
\qquad
\Gamma G-G\Gamma=(8-2p)\operatorname{id}.
$$

The trace coordinate omitted by the projected row is
$(\Gamma G)^{-1}C_v$, with spectra $(8)$, $(6,14)$, $(4,10,18)$ and
$(2,6,12,20)$ in the four required degrees. A direct projected Clifford map
is not a chain map, but its entire defect is the explicit trace-mediated term

$$
-2P'E_v(\Gamma G)^{-1}C_vI.
$$

Therefore implement the physical descent on the complete recursively split
triangle
$A_p^\epsilon\simeq U_p^\epsilon\oplus U_{p-1}^{\bar\epsilon}\oplus\cdots$,
filtered by gamma-trace depth. Do not search for an unrelated correction map
on the top $U_p$ row: the off-diagonal transfer is already determined.
Termwise shell pairing is already known to fail: negative
$\langle R_{k+1}-R_k,\widehat G_d\rangle$ occur through the tested range.
The lift must implement the diagonal level shift and cannot be a direct sum
of independent fixed-$(d,k)$ injections.

Implement that lift on the diagonal trajectory spaces

$$
\mathcal D_N^{(p)}=\bigoplus_{d+k=N}
\operatorname{Hom}_{B_4}(H_k^{(p)},\widehat{\mathcal G}_d).
$$

Do not infer level-raising maps from the dimension identity alone. Literally,
the hook births are first-row differences at fixed $d$, and a termwise Regge
injection is refuted by 122 negative differences in $d+k\leq20$, 108 in the
Bars range. Instead construct a diagonal filtration mixing the mass and
first-row gradings so that its associated cokernels have the hook birth
dimensions, including the known one-row scalar endpoint. Tensor the complete
five-term resolution with that filtered module and identify the relevant
derived homology. Only then make contraction/wedge descend to

$$
\operatorname{coker}T_N^{(1)}
\hookrightarrow
\operatorname{coker}T_N^{(0)}\oplus
\operatorname{coker}T_N^{(2)}.
$$

Its dimension inequality is the scalar theorem. The exact resolution already
moves through the cumulative-core pairing. If
$B(q)=\langle\mathcal T(q),\mathfrak D^+(\widehat G(q))\rangle$, then

$$
(1-q)\Phi=(1+q)H_4-(1+q^2)B_\Gamma.
$$

Thus the remaining scalar target is equivalently a prefix dominance between
the positive-resolution series $B_\Gamma$ and the fourth primitive series $H_4$.
After outer antisymmetrization is performed in the required order, this
prefix kernel is exactly
$\mathfrak D^+(R_{n+1}-R_n)=E_n-E_{n-1}$, where
$E_n=[n+1,0,1,0]-[n,1,1,0]+[n,0,2,1]$. It restricts to the positive
$B_3$ shell $[n,0,3]$ but remains virtual in $D_4$. Thus the resolution
recovers the existing three-hook obstruction and does not furnish a bare
coefficientwise proof.
Treat the curvature $T^{11}$ and the derived homology as concrete data to be
computed, not generic caveats or groups required a priori to vanish.

The six coefficients of $\mathscr C$ are
$(s_3,s_4+s_2,s_3+s_1,s_2+s_0,s_1,s_0)$ and
$s_k=\sum_{j=0}^k(-1)^j\Lambda^j9$. Apply the exact primitive-form inversion
$h_k(d)=(-1)^k\langle s_k,Q_d\rangle$ and
$D=H_3-qH_2+q^2H_1-q^3H_0$, which gives
$\Phi=-(1+q^2)D+qH_4$. Prove the resulting sharp inequality
$D_N+D_{N-2}\geq h_4(N-1)$. Equivalently, apply the second inversion
$\Pi_k=\sum_{r=0}^k(-q)^rH_{k-r}$ and prove the adjacent bidegree inequality
$\pi_3(N)\geq\pi_4(N-1)$ by a degree-$(+1,-1)$
Koszul/physical-state map or directly from the HFT oscillator product. This
route should use the cumulative core as the candidate underlying module:
construct nine covariant degree-one operations on $Z_m/(1-q)$ and prove that
their Koszul quotient or homology is $\widehat G$. A regular-sequence theorem
would prove the observed core positivity at all orders and explain why the
cumulative completion is essential. A finite comparison shows, however, that
$\Pi_3$ and $\Pi_4$ are not raw low-form multiplicities of $\widehat G$, so a
refined primitive complex remains necessary. Use the transverse DDF vector
creators to form its ordinary Koszul differential. The raw middle map is not
injective:
$\ker d_4=\operatorname{im}d_5$. Therefore its source must be the primitive
quotient $K_4/\operatorname{im}d_5$. Compute the mass-level, little-group,
supermultiplet and exterior-degree refinement of the DDF/BRST complex;
identify $\Pi_4$ with that quotient and $\Pi_3$ with a target containing its
image. The bosonic differential is not spacetime-supersymmetric, and a
literal super-Koszul completion has a spinor where the compact kernel has a
shifted scalar, so the required descent must be filtered or Dirac-indexed.
The relative Dirac half now supplies an actual chiral Dirac-cohomology model
through the Gross--Kostant--Ramond--Sternberg/Kostant construction. The five
low forms become the gamma-traceless tower in the exact resolution above.
Lift the *complete resolution* to the level-one DDF action on
$\mathfrak D^+(Z_m)$. The orthosymplectic operator
$Q^1=\gamma\cdot\alpha_{-1}/\sqrt2$ is relevant on the multiplicity side,
where $\{Q^1,Q^1\}=T^{11}$, but it is a Lorentz scalar and is not the
adjacent projected-wedge map $U_j\to U_{j+1}$. Construct their combined
derived descent using the explicit full-triangle identities above. Prove that
universal-supermultiplet division respects gamma-trace depth, run the induced
spectral sequence, and show that its only relevant edge homologies are
$\Pi_4$ and $\Pi_3$; equivalently prove the $B_\Gamma$--$H_4$ prefix
dominance. The remaining issue is homology concentration, not the existence
of a local transfer formula.
Because $\widehat G$ has already removed the mode-one vector tower, construct
$Q^1$ before the Koszul/coinvariant descent and transfer it to primitive
homology; do not postulate an action directly on the core. The ordinary
no-ghost theorem alone has the wrong grading. Use the fixed Plücker factorization and
orthogonal--orthosymplectic oscillator duality to seek module-level
stable-arm exactness, with the finite wall terms as endpoints. This is
followed by analogous boundary functionals for the five non-scalar
coordinates of $A_0$.

This construction is integral by design.  If these statements are proved,
neither a general saturation theorem nor a classification of every circuit
is needed for the Bars targets.

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
| TK6B.6 | Cumulative Regge uplift | Reduce the explicit positive lift to scalar-tail positivity and five one-shell inequalities |
| TK6B.6e | Cumulative-core and primitive DDF/Koszul audit | Identify the cumulative $B_4$ core, the correct primitive quotient, and either construct its supersymmetric descent or record the exact obstruction |
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

**TK6B.6e corrects the naive Koszul target.** On restriction to $D_4$, the
compact kernel at $q=1$, the square of the relative spinor denominator and
the vector Koszul Euler class agree exactly. Removing the transverse
level-one vector gives
$G=D_{8_v}(q)(Z_m\downarrow_{D_4})$, whose coefficients are positive through
degree 20 and agree with an independent baseline-free HFT construction in
the tested range. The relative-Dirac inverse reconstructs the canonical
$B_4$ core
$\widehat G=(\sum_j(-q)^j\Lambda^j9)Z_m/(1-q)$, proving
$Z_m/(1-q)=\operatorname{PE}(q9)\widehat G$ exactly. The core is positive
through degree 20, but its all-orders positivity and an actual
regular-sequence realization remain open. Neither primitive series is a raw
low-form multiplicity of this core in the finite scan. Moving the cumulative
vector tower through the scalar kernel gives an all-orders three-hook formula
supported only on $(k)$, $(k,1)$ and $(k,1,1)$; the finite boundary plus
order-eight Weyl recurrence proves it without a level cutoff. Interlacing and
the unique vector projections further prove the local injection
$(k,1)\hookrightarrow(k)\oplus(k,1,1)$ at every $k$, with one positive
$D_4$ shell as consecutive cokernel. Positive relative-Dirac orientation
upgrades the entire family to an injective free $\operatorname{Sym}(8_v)$
symbol; after tensoring with a physical multiplicity module its exact descent
obstruction is a $\operatorname{Tor}_1$ group. A termwise Regge injection is
refuted by 108 negative first-row differences in the tested Bars triangle, so
the required lift must mix core and first-row degrees. The commuting bosonic DDF creators
supply the desired
degree-$(+1,-1)$ differential, but its raw middle map is not injective:
$\ker d_4=\operatorname{im}d_5$. Only
$K_4/\operatorname{im}d_5\hookrightarrow K_3$ is automatic. Moreover, the
bosonic differential does not commute with spacetime supersymmetry, while a
literal super-Koszul completion has a spinorial first auxiliary degree rather
than the shifted scalar in the compact kernel before relative Dirac
insertion. The positive relative-Dirac half maps the five low forms to
gamma-traceless modules of dimensions $(8,56,160,224,112)$. Explicit
projected-wedge maps form an exact five-term polynomial resolution with
positive cokernel $\bigoplus_n[n,0,3,0]_{D_4}$. The null fibre has nonzero
homology, so the old demand that the truncated Tor obstruction vanish is
withdrawn. Pairing the resolution with the cumulative core gives the exact
identity $(1-q)\Phi=(1+q)H_4-(1+q^2)B_\Gamma$. The remaining task is to realize this
complete resolution on the mass-graded $\mathfrak D^+(Z_m)$ DDF multiplicity
module and prove the corresponding $B_\Gamma$--$H_4$ prefix dominance. Its
correctly oriented prefix is exactly the previously known virtual three-hook
shell, so this is a derived realization of the same sign problem rather than
a coefficientwise shortcut. The
orthosymplectic operator $Q^1$ acts on the multiplicity side and satisfies
$\{Q^1,Q^1\}=T^{11}$; it must be combined with, not identified with, the
projected-wedge maps. The full spinor-form triangle now performs this local
combination exactly: $\Gamma E+E\Gamma=C$, its trace Laplacians are
invertible in every required degree, and the projected defect is
$-2P'E(\Gamma G)^{-1}CI$. The
mode-one action must be built before the core quotient and transferred to
primitive homology. What remains is to prove that the quotient preserves the
trace-depth filtration and that its spectral sequence concentrates; the
direct alternative is the same HFT coefficient inequality. See
`trajectory_kernel/reports/TK6B6_SCALAR_BOUNDARY_REDUCTION.md`.

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
   TK6B.6 reduces a target-specific construction to one scalar sign and five
   shell inequalities; TK6B.6e identifies both the primitive DDF/Koszul
   quotient, the canonical cumulative core $\widehat G$, and an exact
   gamma-traceless free resolution after relative Dirac descent. TK6B.6g
   constructs the complete spinor-form triangle and the exact trace-transfer
   formula relating its projected-wedge and Clifford actions. First seek an
   actual regular-sequence realization of
   $Z_m/(1-q)=\operatorname{PE}(q9)\widehat G$ while lifting the concrete
   full triangle to the mass-graded DDF multiplicity module. Keep the
   distinct multiplicity-side operator $Q^1$ before quotienting, prove the
   universal-supermultiplet quotient preserves gamma-trace depth, and
   identify the filtered derived homology with $\Pi_4,\Pi_3$. Equivalently,
   prove the exact prefix dominance between
   $B_\Gamma$ and $H_4$. Its oriented prefix is already exactly the
   three-hook kernel, so use the free resolution to prove the corresponding diagonal
   dominance in the three orthosymplectic lowest-weight modules. The local
   middle-to-outer hook symbol is already injective for every first row, so
   this step is specifically a filtered module-level derived-homology problem; a
   coefficientwise Regge lift is already refuted. The fallback is to prove
   the adjacent primitive-form dominance directly from the HFT product before returning
   to the five non-scalar shells. Coherent boundary-tail control remains the
   main structural alternative.
4. Extend the BBMS construction beyond level 7 and test telescoping as an
   independent possible shortcut.
