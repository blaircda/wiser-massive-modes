# Project Status

**Last updated:** 13 October 2026

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
relations, the finite kernel-source construction and TK6B.1's saturated
level-11 packet cone provide evidence. TK6B.2 supplies a compact conditional
Gale-circuit description of the required inequalities. TK6B.3 proves a
universal six-term relation for every consecutive parent split, and its
telescoping sum gives every natural kernel relation. It also refutes the
conjecture that only the three $A/B/C$ kernel chains persist: two new families
enter at level 12 and another tail appears in the raw level-13 HFT support.
TK6B.4 proves the exact weighted-circuit criterion for every finite closure and
refutes the unit-coefficient conjecture: eight coefficient-two circuit types
enter the actual HFT closure at level 13. The cumulative level-13 target still
satisfies all 162,739 expanded facet inequalities and has an exactly verified
positive integral packet witness. An all-level classification of the weighted
circuits, all-level saturation and the HFT circuit inequalities remain
unproved. The subleading/core multiplicity problem therefore remains
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

### Global restriction-ring kernel reformulation (TK6A)

**Status: global ring theorem implemented exactly; natural finite generators
classified through baseline-free HFT level 11.**

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

All eleven natural kernel generators in the level-11 finite closure divide
exactly by $J$. Their quotients are positive integral $SO(10)$ characters with
unit coefficients. In particular, the finite-window patterns are

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

The two nontransported TK5b seeds consequently obey

$$
A_0=16_-J,
$$

$$
C_0=126_-J,
$$

up to the fixed chirality convention. The two seeds are therefore distinct
positive multiples of one global kernel generator, rather than independent
ring-kernel directions. Nine of the eleven finite quotients are positive
reducible characters and two are irreducible. The displayed partial-sum
identities are exact in the stated window but are not yet all-$\ell$ theorems.
This algebraic compression does not by itself solve the positive-semiring lift
problem. See `trajectory_kernel/reports/TK6A_PRINCIPAL_KERNEL_IDEAL.md`.

### Finite positive restriction semigroup (TK6B.1)

**Status: exact cone and Hilbert-basis audit complete in the baseline-free
level-11 closure.**

After identifying outer-conjugate parents, the complete interlacing-packet
matrix has 73 $B_4$ rows and 84 $D_5$ columns. It has rank 73 and kernel rank
11. A square all-chiral submatrix has determinant one, so the packet columns
generate the full lattice $\mathbb Z^{73}$.

Total unimodularity fails: an explicit $3\times3$ minor has determinant 2.
Nevertheless, the exact Normaliz Hilbert basis has 84 elements and is exactly
the original set of packet columns. Therefore the finite packet semigroup is
saturated:

$$
A\mathbb Z_{\geq0}^{84}
=
A\mathbb R_{\geq0}^{84}\cap\mathbb Z^{73}.
$$

The rational cone is 73-dimensional, all 84 packet columns are extreme rays,
and its irredundant dual description has 2,508 facets. Every cumulative HFT
target through level 11 satisfies all of them and has a separately verified
nonnegative integral packet decomposition.

Thus no additional integrality obstruction occurs in this finite closure:
integral positive liftability is equivalent to the rational facet
inequalities. This is not an all-orders result. Saturation for arbitrary
interlacing domains and a stable classification of the 2,508 finite facets
remain open. See
`trajectory_kernel/reports/TK6B1_POSITIVE_RESTRICTION_SEMIGROUP.md`.

### Facets as positive kernel circuits (TK6B.2)

**Status: finite classification complete through the baseline-free level-11
closure; conditional all-level Gale template formulated.**

The 2,508 facets do not collapse directly into a small set of translated
$B_4$ multiplicity inequalities: 2,444 distinct templates remain even after
all common Dynkin-label translations, and 2,399 new translation types appear
from level 10 to 11. Only 14 of 63 eligible leading-label shifts preserve a
facet.

The kernel/Gale transform gives a much stronger compression. In the eleven
natural kernel coordinates, the 84 packet columns have only 29 distinct Gale
row types. They are exactly zero, the 22 signed coordinate vectors, three
adjacent vectors $-e_{B_i}-e_{A_{i+1}}$, and three boundary sums over the
available $A$, $B$ and $C$ chains. This compact row template is exact at every
tested nested horizon.

All 2,508 facets are positive Gale circuits with coefficient one. Identifying
repeated Gale rows leaves only 40 circuit types, whose binomial multiplicities
reconstruct every facet exactly. If $U$ is the unimodular all-chiral packet
submatrix and $c=U^{-1}m$, every facet becomes a zero-one Hall-type inequality

$$
\sum_{j\in S\cap\operatorname{Ref}}c_j\geq0
$$

for a minimally zero-sum Gale subset $S$. Together with TK6B.1 saturation,
these inequalities are necessary and sufficient for positive integral
liftability in the finite closure.

The circuit list itself is not stable: it grows from 23 types at level 10 to
40 at level 11. TK6B.2 therefore proposed the compact Gale-row rule and its
dynamically generated positive circuits, rather than a fixed facet list, as
the candidate all-level object. TK6B.3 below refines that proposal after new
families enter. See
`trajectory_kernel/reports/TK6B2_FACET_CIRCUITS.md`.

### Boundary shells and growing kernel families (TK6B.3)

**Status: universal all-split identity and conditional arbitrary-length
$A/B/C$ theorem proved; $A/B/C$ completeness refuted at level 12.**

For every $B_4$ top weight $[\ell,m,r,s]$, consecutive allowed parents
$[\ell,m,r,k,s-k]$ and $[\ell,m,r,k-1,s-k+1]$ differ by one universal
six-term restriction-kernel identity. Its four auxiliary all-chiral terms
follow from exact inclusion-exclusion on the intervening interlacing shell.
The identity holds for arbitrary nonnegative labels and every
$1\leq k\leq\lfloor s/2\rfloor$, with coefficients $\pm1$.

Telescoping the first $k$ shells gives a closed $4k+2$-term formula comparing
the $k$th parent directly with the all-chiral parent. Exact branching checks,
telescoping checks and independent triangular section inversion agree through
sampled splits $k=1,2,3$. The formula and proof contain no HFT mass level, so
later levels cannot introduce new kinds of local parent-split relation.

The old $A$, $B$ and $C$ relations are three specializations. Their support
collisions prove the TK6B.2 row template for arbitrary lengths of those chains.
This conditional theorem does not describe the actual next HFT shell. At
level 12 the domain grows from $73\times84$ with kernel rank 11 to
$92\times108$ with kernel rank 16. Besides $A_6,B_3,C_2$, new generators occur
at top weights $(0,2,0,2)$ and $(0,0,1,2)$.

The level-12 Gale transform still has a compact local form: 43 row types, made
of one zero type, 32 signed-coordinate types and ten composite collision
types. All 16 kernel generators are instances of the universal six-term
identity. A level-13 raw HFT look-ahead extends both new families and adds the
tail $(m,r,s)=(1,0,3)$. The revised candidate all-orders object is therefore a
growing all-split collision hypergraph of local interlacing shells, not a fixed
list of kernel families. See
`trajectory_kernel/reports/TK6B3_BOUNDARY_SHELL.md`.

### Weighted positive circuits (TK6B.4)

**Status: exact finite weighted criterion proved; unit-coefficient conjecture
refuted at HFT level 13; all-orders control open.**

For a finite packet matrix $A$ and the universal natural kernel basis $K$, the
facet slacks are precisely the primitive extreme rays of

$$
\{x\geq0:K^Tx=0\}.
$$

If $c=U^{-1}m$ are the triangular all-chiral coordinates of a target, the
corresponding exact liftability inequalities are

$$
\sum_{j\in\operatorname{Ref}}x_jc_j\geq0.
$$

Repeated Gale rows can be compressed exactly: every circuit selects at most
one realization of a row type, and a type circuit expands by the product of
the supported row multiplicities. This reproduces all 2,508 level-11 facets
and gives 18,923 at level 12 and 162,739 at level 13 without constructing the
full high-dimensional facet descriptions.

The complete HFT closures have 40, 140 and 495 circuit types at levels 11, 12
and 13. All coefficients are one through level 12. At level 13, 487 circuit
types remain unit while eight primitive types contain coefficient two. An
explicit ten-row, rank-nine coefficient-two certificate shows that this is
not a nonminimal sum of subset circuits. Synthetic mixed-label boxes give
independent coefficient-two examples, including examples involving the second
parent split.

Despite this obstruction, the cumulative HFT targets through level 13 satisfy
every weighted inequality. The level-12 and level-13 targets also have
nonnegative integral packet witnesses checked by exact reconstruction. This
extends baseline-free finite evidence for Bars III.B; it does not prove
all-level saturation or positivity. See
`trajectory_kernel/reports/TK6B4_WEIGHTED_CIRCUITS.md`.

### Local HFT form of the weighted inequalities (TK6B.5)

**Status: exact all-label pullback proved; recursive circuit positivity and
integrality remain open.**

The inverse of the all-chiral branching section is local. If
$M(\ell,m,r,s)$ is a $B_4$ multiplicity, the coefficient of
$[\ell,m,r,0,s]_{10}$ is the eight-term mixed forward difference

$$
\sum_{\epsilon_1,\epsilon_2,\epsilon_3\in\{0,1\}}
(-1)^{\epsilon_1+\epsilon_2+\epsilon_3}
M(\ell+\epsilon_1-\epsilon_2,
  m+\epsilon_2-\epsilon_3,
  r+\epsilon_3,s),
$$

with zero extension outside the dominant chamber. This follows directly by
Möbius inversion of the three nested $D_5\downarrow B_4$ interlacing sums.
It has no HFT cutoff and agrees with independent exact matrix inversion on
the complete closures through level 13.

Substitution turns every weighted circuit facet into a finite signed HFT
multiplicity inequality. The operator commutes with cumulative sums and with
Dynkin-label translations, giving the exact intertwiner required for a
GMSZ/core induction. The missing steps are now structural: recursively
control the circuits of the growing infinite shell matrix, prove positivity
of the resulting HFT partial sums, and establish saturation or construct
integral packetizations. A circuit visible at one finite horizon need not
remain a circuit after new kernel coordinates appear. See
`trajectory_kernel/reports/TK6B5_HFT_WEIGHTED_INEQUALITIES.md`.

### Prefix-shell duality and Regge tails (TK6B.5b/c)

**Status: uniform dual operator proved; fixed finite-circuit strategy
obstructed; remainder/Pieri proof target isolated.**

Each natural shell coordinate has one unique non-chiral unit pivot.
Eliminating these pivots gives the exact cone

$$
y\geq0,
$$

$$
Ly\geq0,
$$

where $L$ is an explicit prefix-shell operator on all-chiral labels. Positive
liftability is equivalently $c=u+L^Tz$ with $u,z\geq0$, and the circuit
pairing is the exact Farkas identity

$$
\langle y,c\rangle
=\langle y,u\rangle+\langle Ly,z\rangle.
$$

The infinite operator is column-finite but not row-finite: its $Q_4$ packet
forgets the leading label. An exact tail argument shows that no nonzero
finitely supported $y\geq0$ can satisfy every infinite shell inequality.
Therefore finite-horizon circuits cannot stabilize as fixed finite objects;
they must be treated as coherent moving boundary tails.

One universal tail family is controlled. For every fixed top-weight family
and split, its leading-label interval is a primitive finite-horizon circuit,
and the TK6B.5 Möbius pullback telescopes to at most eight endpoint
multiplicities. Mixed circuits are harder: in a small mixed box the largest
pulled support grows from 24 to 45 when the leading-label horizon grows from
zero to one.

The exact HFT factorization
$Z_m=\operatorname{PE}([1,0,0,0]_9q)Z'_m$ now supplies a specific analytic
route. Through level 13 all 185 eligible adjacent $\ell$ shifts hold
separately at every virtual remainder degree, and every observed degree-$d$
remainder term obeys $2\ell+2m+2r+s\leq d-1$. These are exact finite results,
not an all-orders proof. Stable $B_4$ Pieri transport is now proved in the
follow-up TK6B.5d result below; the remaining HFT statement is
contribution-wise stable-range coverage, which is stronger than the displayed
global half-slope observation. See
`trajectory_kernel/reports/TK6B5B_PREFIX_SHELL_DUALITY.md`.

### Stable Pieri translation (TK6B.5d)

**Status: all-rank translation theorem proved; its formerly open all-degree
HFT stable-range premise is proved in TK6B.5f.**

For arbitrary tensorial or spinorial $B_n$ highest weights $\mu$ and
$\lambda$, a Racah--Speiser stabilizer argument proves

$$
[V_\lambda:V_\mu\otimes H_k]
=
[V_{\lambda+\omega_1}:V_\mu\otimes H_{k+1}]
$$

whenever $\lambda_1\geq\mu_1$ in orthogonal coordinates. Summing the
harmonic decomposition of the symmetric powers gives

$$
[V_\lambda:V_\mu\otimes\operatorname{Sym}^{R}(V)]
=
[V_{\lambda+\omega_1}:
V_\mu\otimes\operatorname{Sym}^{R+1}(V)].
$$

The proof works on both integral and half-integral weight cosets, so chirality
does not obstruct the leading-coordinate transport theorem. An independent
small character-ring audit has 393 exact cases and no failure.

In the exact HFT factorization through level 13, all 524 active irrep-level
remainder couplings in the 185 eligible adjacent $\ell$ shifts meet the
theorem hypothesis and match. This includes 214 spinorial couplings and 44
couplings with negative coefficients in the virtual remainder. There is no
unpaired top-degree contribution in the tested window.

What remains is a support theorem, not another multiplicity identity: prove
that every remainder irrep which can actually couple to an exterior-chamber
target lies in the stable range, and that the new top-degree remainder misses
the translated target. The observed half-slope bound alone does not imply
this, because it also includes remainder irreps which cannot couple.

A sharper statement is now available. Put
$E(\ell,m,r,s)=2\ell+3m+\operatorname{cost}(r,s)$, with the GMSZ support
cost. All 176 remainder terms through degree 12 satisfy $E(\mu)\leq d+1$,
and all 363 unstable HFT product terms through total degree 12 satisfy
$E(\lambda)\leq d+R$, with minimum margin two. The latter inequality places
the translated label outside the GMSZ chamber exactly. It is HFT-specific:
the generic shortcut $E(\lambda)\leq E(\mu)+R-1$ has an exact $B_4$
counterexample. A generator-wise proof also fails: $PL[Z'_m]$ has 10
exterior-cost violations through degree 8 even though $Z'_m$ itself obeys the
bound in that window.

TK6B.5e replaces the failed generic shortcut by the finite harmonic hazard
$H(\mu)=\max(E(\lambda)-k)$ over unstable constituents of
$V_\mu\otimes H_k$. Only $k<2\mu_1$ can contribute. The sufficient source
threshold $K(\mu)=\max(E(\mu)-1,H(\mu))$ has a closed wall-piecewise affine
formula, proved for both tensorial and spinorial weights. Its three new pieces
away from $\ell=0$ are

$$
2\ell+5m+6r+3s-4,
$$

$$
2\ell+5m+7r+4s-5,
$$

$$
2\ell+5m+9r+5s-9.
$$

All 176 HFT remainder terms through degree 12 satisfy $d\geq K(\mu)$.
However, all four previously proposed linear ``filtrations'' have exact
tensor-product counterexamples, so the four-filtration Newton-cone route was
not valid. This milestone reduced the problem to the explicit HFT support
theorem $[V_\mu]F_d\neq0\Rightarrow d\geq K(\mu)$, subsequently proved in
TK6B.5f. Exact oscillator identities express $qZ_QF$ and the
all-vector-free core as known NS/R--Euler numerators. See
`trajectory_kernel/reports/TK6B5E_PIERI_HAZARD.md`.

TK6B.5f proves this remaining support theorem. On the common $D_4/B_4$ torus,
the finite triality identity
$E(u)-D(u)=u(V+S)B(u)$ gives an exact Green--Schwarz telescope for $F(q)$.
The equal-rank Weyl/Dirac numerator cannot raise the chirality-folded
seven-wall degree. Uniform vector and spinor Lipschitz bounds close all vector
modes $m\geq4$, fermion modes $m\geq5$, and pivots $n\geq3$ outside a fixed
low-mode core. Horizontal-strip optimization bounds vector modes 2 and 3 by
eight affine walls. The remaining five pivot classes give 323 finite
exact records with no failure and minimum margin zero. Consequently

$$
[V_\mu]F_d\neq0\quad\Longrightarrow\quad d\geq K(\mu)
$$

at every degree. This closes the contribution-wise stable-range premise of
TK6B.5d. It does not yet prove the global recursive weighted-circuit or
integral-packetization statement required for Bars III.B. See
`trajectory_kernel/reports/TK6B5F_ANALYTIC_HFT_SUPPORT.md`.

### Cumulative Regge-tower uplift (TK6B.6)

The Bars cumulative factor combines exactly with the HFT level-one
symmetric-vector factor:

$$
\frac{Z_m(q)}{1-q}
=\operatorname{Res}\left(\operatorname{PE}(qV_{10})\right)F(q).
$$

Thus an integral virtual lift $\widetilde F$ of the HFT remainder gives an
exact cumulative virtual lift

$$
X(q)=\operatorname{PE}(qV_{10})\widetilde F(q).
$$

For the all-chiral triangular section, the uncorrected series first fails by
$16_+ -16_-=J$ at physical level 4. The exact kernel correction $-q^3J$, followed
only by multiples of the first six-term shell $A_0=16_-J$, gives positive
integral coefficients through level 13. The correction through the tested
window is

$$
-q^3J+(q^9+2q^{10}+2q^{11}+3q^{12})A_0.
$$

The $A_0$ coefficients are not fitted to the full representations. They are
fixed by a scalar diagonal of the HFT remainder. If $B(q)$ is the scalar
coefficient of the uncorrected cumulative lift, then

$$
[\mathbf1]\operatorname{PE}(qV_{10})A_0=\frac{1}{1+q},
$$

and the candidate correction is $A(q)=-(1+q)B_{\geq9}(q)$. It agrees exactly
with the independent greedy positivity recursion through degree 12. A
Racah--Speiser argument also proves stable leading-coordinate translation for
type $D_n$.

The scalar condition has now been pulled through the exact Green--Schwarz
telescope. If $C(q)=\sum c_Nq^N$ is the one-row diagonal, the exact low-degree
identity $b_8=0$ gives

$$
a_N=-\sum_{k=0}^{N}c_k\qquad(N\geq9).
$$

Writing $F(q)=(1-q)G(q)$ for the pre-telescope series turns this into
$a_N=-[q^N]\Phi_q(G(q))$. The composed Dirac/Möbius functional $\Phi_x$
vanishes off nine fixed transverse `D4` rays; away from five wall endpoints,
every value is a monomial times $(1-x)^2$. This is an all-orders finite-ray
reduction of scalar positivity, not yet its sign proof. The coefficients are
nonnegative through degree 20. A separate multiplicative fundamental-section
shortcut fails exactly at degree five because Dirac folding is not a ring
homomorphism. The nine rays group further into four adjacent-ray Euler
sectors, but two of the corresponding pre-factor series are signed, so they
cannot be interpreted as sets of states and the earlier literal-injection
proposal is discarded. Uniform Laurent continuation gives the sharper exact
identity

$$
\Phi_q(G)=(1-q)^2R_{\mathrm{st}}+\Omega,
$$

where $R_{\mathrm{st}}$ contains only stable first arms $L\geq1$ and
$\Omega$ involves the five actual endpoint representations. Thus
$a_N=W_N-I_N$, with
$I_N=R_{\mathrm{st},N}-2R_{\mathrm{st},N-1}+R_{\mathrm{st},N-2}$ and
$W_N=-[q^N]\Omega$; the remaining scalar theorem is the wall-dominance inequality
$W_N\geq I_N$. At fixed first modified-Frobenius arm $L\geq1$, all nine rays
have the same monomial $q^{L-1}$ and their Young-diagram tails are nine of the
ten partitions in a fixed $3\times2$ rectangle. With the natural Hodge signs,
their coefficient vector is exactly the Plücker vector of the rank-two matrix
with rows $(1,1,1,1,1)$ and $(0,0,1,2,3)$; the omitted tenth coefficient
vanishes because the first two columns coincide. This supplies two exact
exterior factors. Laplace expansion packages the nine `D4` Weyl numerators
into one $6\times6$ bordered determinant, and their virtual character has
dimension identically 15 for every stable arm. The geometric arm sum changes
only its first column, replacing it by
$z_i^5/(1-qz_i)\mathbin{\pm}z_i^{-5}/(1-q/z_i)$. Clearing the vector exterior
denominator gives the exact finite numerator
$D_V(q)\sum_{L\geq1}q^{L-1}K_L=N(q)$ with $\deg N=7$; equivalently the
infinite arm family is eight fixed virtual characters followed by
$\operatorname{PE}(qV)$. Tensoring by this self-dual tower is self-adjoint,
so it moves through the character inner product and cancels the vector
exterior factor in $G$. Combining the stable and endpoint terms and using
the relative $D_4/B_4$ Weyl denominator yields the still smaller all-orders
identity

$$
\Phi_q(G)=\langle\mathscr C(q),Z_m(q)\rangle_{B_4},
$$

where $\mathscr C$ has degree five and its six coefficients are
$s_3,s_4+s_2,s_3+s_1,s_2+s_0,s_1,s_0$, with
$s_k=\sum_{j=0}^k(-1)^j\Lambda^j9$. Thus the scalar theorem now involves
only the multiplicities of $1,9,36,84,126$ in six adjacent HFT levels. This
suggests a finite Koszul/physical-state complex, but no differential,
exactness theorem or direct sign estimate has yet been constructed. See
`trajectory_kernel/reports/TK6B6_SCALAR_BOUNDARY_REDUCTION.md`.

The follow-up DDF audit constructs the natural differential and corrects that
last sentence. On restriction to $D_4$, the compact kernel at $q=1$ is exactly
the vector Koszul Euler class and the square of the relative spinor Weyl
denominator. The pre-telescope series is
$G=D_{8_v}(q)(Z_m\downarrow_{D_4})$ and is a positive integral `D4` character
through degree 20; this remains finite evidence. More strongly, it is the
restriction of the canonical $B_4$ series

$$
\widehat G(q)=\frac{\sum_{j=0}^9(-q)^j\Lambda^j9}{1-q}\,Z_m(q).
$$

Odd-dimensional Hodge duality makes the quotient a degree-eight character
polynomial and proves the exact cumulative factorization

$$
\frac{Z_m(q)}{1-q}=\operatorname{PE}(q9)\widehat G(q).
$$

The relative-Dirac oriented inverse reconstructs this same $\widehat G$.
Its coefficients are positive integral `B4` characters through degree 20,
with 145 irreducible summands at degree 20 and least coefficient one. Thus the
old virtual remainder is precisely $(1-q)\widehat G$: cumulative completion
turns its tested first differences into a positive core. This is not yet an
all-orders positivity theorem or an actual free-module construction.

The commuting bosonic DDF creators give the desired degree-$(+1,-1)$ Koszul
map, but the raw middle map is not injective:
$\ker d_4=\operatorname{im}d_5$. The automatic injection is

$$
K_4/\operatorname{im}d_5\hookrightarrow K_3.
$$

The remaining analytic target is therefore to identify this primitive
quotient and its target with $\Pi_4$ and $\Pi_3$ after physical-state and
universal-supermultiplet reduction. The bosonic differential is BRST
compatible but not spacetime-supersymmetric; a literal super-Koszul
completion introduces a spinor where the compact kernel has a shifted scalar.
The relative Dirac factor resolves this representation mismatch at character
and symbol level. The Gross--Kostant--Ramond--Sternberg formula and Kostant
Dirac operator realize its positive half as actual chiral Dirac cohomology,
not just a virtual character choice. It sends the five low forms to
gamma-traceless `Spin(8)` modules of dimensions $(8,56,160,224,112)$. Their
`Spin(7)` restrictions telescope, and their unique adjacent vector couplings
suggest the required symbol sequence. An explicit rational Clifford model now
completes that argument: projected-wedge maps compose to zero, have non-null
ranks $(8,48,112,112)$, and form the exact polynomial free resolution

$$
0\longrightarrow S_V(-4)U_0\longrightarrow S_V(-3)U_1
\longrightarrow S_V(-2)U_2\longrightarrow S_V(-1)U_3
\longrightarrow S_VU_4\longrightarrow\mathcal T\longrightarrow0,
$$

where $S_V=\operatorname{Sym}(8_v)$ and
$\mathcal T_n=[n,0,3,0]_{D_4}$. The nonzero null fibre has ranks
$(8,48,112,92)$ and twenty-dimensional homology in each of the last two
positions. This is a computed Tor fibre, not a defect in the universal free
resolution. It shows that the previous plan to prove the truncated Tor group
vanishes on the trace quotient was too strong.

Pairing the complete resolution with the positive relative-Dirac half gives
a second exact all-orders reduction. Let

$$
B_\Gamma(q)=\left\langle
\sum_{n\geq0}q^n[n,0,3,0]_{D_4},
\mathfrak D^+(\widehat G(q))
\right\rangle_{D_4}.
$$

Then

$$
(1-q)\Phi=(1+q)H_4-(1+q^2)B_\Gamma,
$$

and hence

$$
a_N-a_{N-1}=B_{\Gamma,N}+B_{\Gamma,N-2}-h_4(N)-h_4(N-1).
$$

This identity is exact. The series $B_\Gamma$ is manifestly nonnegative whenever
$\widehat G$ is positive; that core positivity is currently verified only
through degree 20. The remaining scalar theorem is therefore a specific
prefix dominance between $B_\Gamma$ and $H_4$, not abstract flatness.

The correct outer-chirality order prevents a further shortcut. Moving $H_4$
to the cumulative core requires antisymmetrization before selecting the
positive orientation. The resulting prefix kernel is exactly

$$
\mathcal L_n=E_n-E_{n-1}
=\mathfrak D^+(R_{n+1}-R_n),
$$

where $E_n=[n+1,0,1,0]-[n,1,1,0]+[n,0,2,1]$ and $E_{-1}=U_0$. Its
restriction to `Spin(7)` is the positive shell $[n,0,3]$, but the `Spin(8)`
character is virtual. Convolution with $\mathfrak D^+(\widehat G)$ reproduces
the full Bars margin exactly. Hence the five-term resolution explains the
previous three-hook shell but does not make its sign coefficientwise.

Basile--Markou's Lorentz-scalar operator
$Q^1=\gamma\cdot\alpha_{-1}/\sqrt2$ remains relevant, but its role is now
sharper. It acts inside the Howe multiplicity module of a fixed Lorentz
irrep, whereas the adjacent maps above are projected wedge maps between
different gamma-traceless irreps. Moreover
$\{Q^1,Q^1\}=T^{11}$. The two structures must be combined by derived descent;
they should not be identified.

The first local part of that descent is now explicit. On the full
spinor-valued form triangle, gamma contraction $\Gamma$, gamma wedge $G$,
exterior multiplication $E_v$ and Clifford multiplication $C_v$ obey

$$
\Gamma E_v+E_v\Gamma=C_v,
\qquad
\Gamma G-G\Gamma=(8-2p)\operatorname{id}.
$$

The trace Laplacian $\Gamma_{p+1}G_p$ has spectra $(8)$, $(6,14)$,
$(4,10,18)$ and $(2,6,12,20)$ on the four degrees used by the resolution.
Consequently the discarded trace coordinate is exactly
$(\Gamma G)^{-1}C_v$ on a gamma-traceless source. A literal projected
Clifford action is not a chain map: its non-null defect ranks are
$(8,48,112,112)$ and its null ranks are $(4,24,56,56)$. However, the defect
factors entirely through the gamma-trace complement and reduces to the
one-sided transfer $-2P'E_v(\Gamma G)^{-1}C_vI$. Thus the needed local
homotopy correction is known at every first-row and mass degree. The open
problem is to realize the full triangle before universal-supermultiplet
division and prove concentration of its induced filtered complex; no further
low-level fit is involved.

A finite comparison also rules out identifying $\Pi_3$ or $\Pi_4$ with a raw
low exterior-form multiplicity in either $G$ or $\widehat G$. The cumulative
core is therefore a better candidate underlying module, not a shortcut around
the refined primitive complex. The tempting equality
$\pi_4(N)=[\Lambda^3 9:\widehat G_{N-1}]$ holds only for $6\leq N\leq10$ and
fails at $N=11$ ($12\neq8$).

There is nevertheless a new all-orders simplification on this core. Put

$$
R_k=[k,0,0,0]-[k-1,1,0,0]+[k-1,0,1,0],
$$

omitting invalid labels. Moving $(1-q)\operatorname{PE}(q9)$ through the
character inner product gives

$$
\mathscr C(q)(1-q)\operatorname{PE}(q9)
=\sum_{k\geq0}q^k(R_k-R_{k+1}).
$$

This is proved at all orders: exact character arithmetic supplies degrees
zero through eight, while the $B_4$ Weyl alternant gives the order-eight
recurrence for every fixed-lower-row family from degree nine onward. Hence

$$
a_N=\sum_{d=0}^N
\left\langle R_{N-d+1}-R_{N-d},\widehat G_d\right\rangle_{B_4}.
$$

The remaining scalar sign is therefore supported on just the three principal
hook trajectories $(k)$, $(k,1)$ and $(k,1,1)$. This is well aligned with the
orthosymplectic lowest-weight description, but the alternating hook Euler
sum is not sign-definite merely from positivity of $\widehat G$.

The corresponding local symbol is already exact at every first-row length.
For a nonzero $v\in9$, projected contraction and exterior multiplication give
a $D_4$-equivariant injection

$$
(k,1)\mathord\downarrow_{D_4}
\hookrightarrow\bigl((k)\oplus(k,1,1)\bigr)\mathord\downarrow_{D_4}.
$$

Multiplicity-free interlacing identifies its cokernel as
$1\oplus\bigoplus_{j=0}^{k-1}[j,0,1,1]_{D_4}$ and hence proves the shell
identity

$$
(R_{k+1}-R_k)\mathord\downarrow_{D_4}=[k,0,1,1]_{D_4}.
$$

What remains is no longer the existence of a hook symbol, but its action on
the mass-graded multiplicity spaces and the diagonal level shift. The
relative-Weyl issue is now removed exactly by the positive relative-Dirac
half: the hooks become the $D_4$ gamma-traceless families $[k,0,1,0]$,
$[k-1,1,1,0]$ and $[k-1,0,2,1]$. Their all-$k$ symbol is an injective map of
free $\operatorname{Sym}(8_v)$-modules. After descent to a physical module
$\mathcal P$, its possible kernel is the precise obstruction
$\operatorname{Tor}^{\operatorname{Sym}(8_v)}_1
(\mathcal C_k^{\mathrm{sym}},\mathcal P)$.

Through degree 20 the scalar margin is exactly nonnegative one-row plus
three-row supply minus nonnegative middle-hook demand. The dominance is not
termwise in $(d,k)$: 38 individual shell pairings are negative through
$d+k=20$, with the first Bars-range value
$\langle R_2-R_1,\widehat G_8\rangle=-2$. A successful operator must organize
the entire diagonal.

The diagonal dimension identity requires an extra caution. Define
$\mathcal D_N^{(p)}=\bigoplus_{d+k=N}
\operatorname{Hom}_{B_4}(H_k^{(p)},\widehat{\mathcal G}_d)$. The three birth
counts are consecutive dimension differences of these diagonal spaces, with
one explicit scalar endpoint for $p=0$, but literally they are first-row
differences at fixed core degree. A coefficientwise Regge injection is
impossible: there are 122 negative first-row differences in $d+k\leq20$, 108
in the Bars range. Fixed-hook level shifts and the oriented vector map remain
dimension-compatible in the tested tail, but dimensions do not construct the
maps.

The corrected task is to construct a diagonal filtration mixing the two
gradings, realize its birth spaces as genuine cokernels, evaluate the full
five-term derived tensor product, and then make contraction/wedge induce
$\operatorname{coker}T_N^{(1)}\hookrightarrow
\operatorname{coker}T_N^{(0)}\oplus\operatorname{coker}T_N^{(2)}$.
The resulting dimension inequality would be exactly $a_N\geq0$. Equivalently,
one may prove the displayed $B_\Gamma$--$H_4$ prefix dominance directly. Since
$\widehat G$ already removes the mode-one vector tower, $Q^1$ must be defined
before Koszul descent and transferred to primitive homology, rather than
postulated directly on the core. Its curvature and the derived homology are
the concrete data still to control.

This gives the current most economical analytic route. It remains to prove
the fixed six-level low-form HFT inequality equivalent to the nine-ray index,
and then that the single
$A_0$ correction dominates every non-scalar coefficient at all degrees.
Success would give a
direct integral construction, eliminating the need for a general saturation
theorem or a classification of all finite-horizon facets. See
`trajectory_kernel/reports/TK6B6_CUMULATIVE_REGGE_UPLIFT.md`.

### MILP numerical certification audit

The reported unchecked-rounding risk in the GLPK-backed integer programs was
confirmed. All audited integer objectives and variables now pass an explicit
drift guard, and positive primal witnesses are rechecked with exact integer or
representation-ring arithmetic. In particular, lexicographic stages and
reported coordinate-range endpoints now have exact attained witnesses.

This does not make GLPK's floating-point branch-and-bound status an exact
certificate of global optimality or infeasibility. Negative feasibility,
exhaustion and no-better-solution claims remain solver-backed unless a separate
algebraic or exhaustive certificate is supplied. See
`trajectory_kernel/reports/MILP_NUMERICAL_CERTIFICATION_AUDIT.md`.

### Recommended next analytic directions

The present priority order is:

1. **Evaluate the exact gamma-traceless resolution on the DDF multiplicity
   module.** Start from the complete five-term projected-wedge resolution,
   not only $U_4\hookrightarrow U_3$. Construct before
   universal-supermultiplet and mode-one descent the complete spinor-form
   triangle carrying $E$, $\Gamma$, $G$ and $C=\sqrt2Q^1$. The local
   off-diagonal maps are no longer unknown: they are fixed by the exact
   transfer $(\Gamma G)^{-1}C$. Filter by gamma-trace depth, prove that the
   quotient respects this filtration, and identify the two surviving edge
   homologies with $\Pi_4$ and $\Pi_3$. Keep the curvature
   $\{Q^1,Q^1\}=T^{11}$ on the pre-core Howe multiplicity side; it cannot be
   imposed after the trace and mode-one quotients.
   The equivalent numerical target is the exact prefix dominance implied by
   $(1-q)\Phi=(1+q)H_4-(1+q^2)B_\Gamma$; the known null-fibre Tor is to be computed by
   the resolution, not forced to vanish. Correct outer orientation reduces
   this prefix exactly to the known virtual three-hook shell, so the desired
   argument must use filtered physical-module exactness rather than bare
   `D4` coefficient positivity. In parallel, realize
   the exact cumulative factorization
   $Z_m/(1-q)=\operatorname{PE}(q9)\widehat G$ on actual DDF states. The
   natural concrete subproblem is to construct nine covariant degree-one
   operations, prove that they are a regular sequence, and identify their
   quotient or Koszul homology with $\widehat G$. This would turn the observed
   positivity of the core through degree 20 into an all-orders module theorem,
   although the refined $\Pi_4\to\Pi_3$ identification would still be needed.
2. **Prove the same dominance directly from the oscillator product if the
   descent does not close.** Use the exact relative Weyl Euler class, the
   observed-positive transverse quotient $G$, the fixed Plücker tensor and
   orthogonal--orthosymplectic multiplicity modules to seek a bounded
   Schur/Plücker resolution. The precise target is
   $\pi_3(N)\geq\pi_4(N-1)$, not additional low-level data. Equivalently,
   use the new exact three-hook kernel on $\widehat G$ and derive the
   lowest-weight multiplicity recurrences for $(k)$, $(k,1)$ and $(k,1,1)$.
   The contraction/wedge symbol already injects the middle hook into the two
   outer hooks for every $k$; a lift of that symbol, or a concentration
   theorem for the corresponding orthosymplectic modules, would prove the
   same scalar sign. The diagonal dimension identity alone is insufficient:
   coefficientwise Regge translation is explicitly refuted. Implement a
   filtered diagonal complex on the spaces $\mathcal D_N^{(p)}$ which mixes
   core degree and first-row degree, and only then identify its cokernels.
3. **Finish the explicit lift after the scalar theorem.** Derive the five
   non-scalar $A_0$ boundary functionals and prove one-shell dominance, with
   stable $D_5$ Pieri translation handling the upper chamber.
4. **Retain the structural alternatives.** TK6B.3 gives the
   universal shell relation for every allowed parent split, TK6B.4 shows that
   primitive circuits need not have unit coefficients, and TK6B.5 gives their
   exact local pullback to HFT multiplicities. TK6B.5b/c shows that fixed
   finite circuits cannot stabilize and replaces them by boundary-tail
   families. Stable Pieri transport is proved by TK6B.5d, and TK6B.5f now
   proves its contribution-wise HFT support premise. Use this transport to
   control the mixed tail/core module and its cumulative partial sums. Prove
   saturation or construct integral packetizations directly. In parallel,
   test cumulative positivity of the oscillator-graded candidate. Its
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
| `trajectory_kernel/reports/TK6A_PRINCIPAL_KERNEL_IDEAL.md` | Principal restriction-kernel theorem and finite quotient classification |
| `trajectory_kernel/reports/TK6B1_POSITIVE_RESTRICTION_SEMIGROUP.md` | Exact finite packet cone, Hilbert basis and saturation result |
| `trajectory_kernel/reports/TK6B2_FACET_CIRCUITS.md` | Positive Gale-circuit classification and conditional Hall-type criterion |
| `trajectory_kernel/reports/TK6B3_BOUNDARY_SHELL.md` | Universal all-split shell identities, collision hypergraph and level-12 new-family obstruction |
| `trajectory_kernel/reports/TK6B4_WEIGHTED_CIRCUITS.md` | Exact weighted-circuit criterion, coefficient-two obstruction and level-13 positive witness |
| `trajectory_kernel/reports/TK6B5_HFT_WEIGHTED_INEQUALITIES.md` | Local Möbius inverse, circuit pullback and translation-covariant HFT reduction |
| `trajectory_kernel/reports/TK6B5B_PREFIX_SHELL_DUALITY.md` | Prefix-shell cone, no-finite-circuit obstruction, Regge tails and HFT Pieri route |
| `trajectory_kernel/reports/TK6B5D_STABLE_PIERI_TRANSLATION.md` | Stable tensorial/spinorial Pieri theorem and contribution-wise HFT audit |
| `trajectory_kernel/reports/TK6B6_CUMULATIVE_REGGE_UPLIFT.md` | Target-specific cumulative uplift and finite positivity construction |
| `trajectory_kernel/reports/TK6B6_SCALAR_BOUNDARY_REDUCTION.md` | Scalar boundary reduction, exact gamma-traceless resolution and remaining prefix dominance |
| `trajectory_kernel/reports/MILP_NUMERICAL_CERTIFICATION_AUDIT.md` | MILP rounding hardening and remaining solver-status limitation |
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
| `trajectory_kernel/principal_ideal.py` | TK6A principal kernel presentation and exact finite quotients | No |
| `trajectory_kernel/restriction_semigroup.py` | TK6B.1 exact packet cone, non-TU and Hilbert-basis audit | No |
| `trajectory_kernel/interlacing_facets.py` | TK6B.2 facet shifts, Gale circuits and section-subset inequalities | No |
| `trajectory_kernel/boundary_shell.py` | TK6B.3 all-length shell identities and level-12/13 family-growth audit | No |
| `trajectory_kernel/all_split_circuits.py` | TK6B.4 weighted all-split circuits and HFT target inequalities | No |
| `trajectory_kernel/hft_weighted_inequalities.py` | TK6B.5 local Möbius inverse and weighted HFT pullbacks | No |
| `trajectory_kernel/shell_duality.py` | TK6B.5b pivot-eliminated prefix-shell cone and Regge tails | No |
| `trajectory_kernel/regge_factorization.py` | TK6B.5c exact HFT symmetric-vector factorization and termwise shifts | No |
| `trajectory_kernel/stable_pieri.py` | TK6B.5d stable $B_4$ Pieri theorem audit and HFT stable-range check | No |
| `trajectory_kernel/hft_analytic_support.py` | TK6B.5f all-degree Green--Schwarz support theorem | No |
| `trajectory_kernel/cumulative_regge_uplift.py` | TK6B.6 target-specific cumulative uplift and finite positivity audit | No |
| `trajectory_kernel/scalar_boundary_functional.py` | TK6B.6 scalar boundary and primitive-form reduction | No |
| `trajectory_kernel/ddf_koszul_audit.py` | TK6B.6e transverse DDF/Koszul, cumulative-core and primitive-quotient audit | No |
| `trajectory_kernel/gamma_symbol_complex.py` | TK6B.6f/g exact Clifford symbols, gamma-traceless free resolution and trace-transfer triangle | No |
| `trajectory_kernel/milp_certification.py` | Shared floating-point MILP integrality guards | No |
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
./bin/sage-run -m trajectory_kernel.principal_ideal --max-level 11
./bin/sage-run -m trajectory_kernel.restriction_semigroup --max-level 11
./bin/sage-run -m trajectory_kernel.interlacing_facets --max-level 11 --min-level 5
./bin/sage-run -m trajectory_kernel.boundary_shell --self-test
./bin/sage-run -m trajectory_kernel.boundary_shell --max-level 12 --previous-level 11 --branch-check-ell 2 --split-check-max-s 6 --lookahead-level 13
./bin/sage-run -m trajectory_kernel.all_split_circuits --self-test
./bin/sage-run -m trajectory_kernel.all_split_circuits --hft-level 13 --verbose
./bin/sage-run -m trajectory_kernel.hft_analytic_support --self-test
./bin/sage-run -m trajectory_kernel.cumulative_regge_uplift --self-test
./bin/sage-run -m trajectory_kernel.scalar_boundary_functional --self-test
./bin/sage-run -m trajectory_kernel.ddf_koszul_audit --self-test
./bin/sage-run -m trajectory_kernel.gamma_symbol_complex --self-test
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
7. **TK5c complete through level 11:** GLPK-backed lexicographic minimization
   of core-supported sources, with exact primal-witness verification, gives
   event/charge minima
   $(1,1),(2,2),(3,4),(5,11),(7,20)$ at horizons 7--11, with respectively
   $1,2,2,3,6$ distinct verified witnesses before solver-reported exhaustion.
   The optimal faces cease to have
   compatible prefixes at $9\to10$ and again at $10\to11$, so ungraded source
   sparsity is not a cutoff-stable analytic selector. See
   `trajectory_kernel/reports/TK5C_MINIMAL_CORE_WITNESSES.md`.
8. **TK6A complete globally at ring level and through the level-11 natural
   finite basis:** the restriction-ring kernel is the principal ideal
   $(16_+-16_-)$. Every one of the eleven natural finite kernel generators
   factors exactly through this element, and every quotient is a positive
   integral character with unit coefficients. The $A$, $B$ and $C$ quotient
   families obey simple partial-sum formulas throughout the available window;
   an all-$\ell$ proof remains open. See
   `trajectory_kernel/reports/TK6A_PRINCIPAL_KERNEL_IDEAL.md`.
9. **TK6B.1 complete through the level-11 finite closure:** the unoriented
   interlacing-packet matrix has size $73\times84$. It is not totally
   unimodular, as an exact determinant-two minor shows, but its Hilbert basis
   is exactly the 84 original packet columns. The semigroup is saturated, its
   rational cone has 2,508 irredundant facets, and every cumulative HFT target
   through level 11 satisfies them and has an exact integral packet witness.
   TK6B.2--TK6B.4 give the subsequent finite circuit classification, universal
   boundary-shell formulas and weighted-circuit refinement.
   See
   `trajectory_kernel/reports/TK6B1_POSITIVE_RESTRICTION_SEMIGROUP.md`.
10. **TK6B.2 finite facet classification complete:** direct Dynkin-translation
   types proliferate, but the 2,508 facets reduce to 40 positive-circuit types
   of 29 Gale row types in the eleven natural kernel coordinates. The Gale
   rows obey one compact $A/B/C$ template at every tested nested horizon, all
   circuit coefficients are one, and every facet becomes a zero-one subset
   inequality in triangular section coordinates. The circuit list itself has
   not stabilized; the conditional all-level object is the compact Gale-row
   rule and its dynamically generated circuits. See
   `trajectory_kernel/reports/TK6B2_FACET_CIRCUITS.md`.
11. **TK6B.3 boundary-shell theorem and obstruction complete:** the compact
   $A/B/C$ Gale-row rule is proved for arbitrary lengths of those chains, and
   every consecutive allowed parent split obeys one universal six-term
   interlacing identity. Telescoping gives the exact $4k+2$-term natural
   relation for the $k$th parent. However, two new kernel families enter the
   actual HFT closure at level 12. The $92\times108$ packet matrix has kernel
   rank 16 and 43 Gale row types: one zero, 32 signed-coordinate and ten
   composite collision types. Raw level-13 HFT support shows continuing family
   growth. The revised all-level object is an all-split collision hypergraph,
   not a fixed $A/B/C$ list. See
   `trajectory_kernel/reports/TK6B3_BOUNDARY_SHELL.md`.
12. **TK6B.4 weighted-circuit obstruction and finite level-13 audit
   complete:** positive circuits give the exact finite weighted liftability
   inequalities, and repeated Gale rows admit an exact type compression. The
   compression reproduces 2,508 level-11 facets and gives 18,923 at level 12
   and 162,739 at level 13. All circuits are unit through level 12, but eight
   primitive level-13 types have coefficient two. Nevertheless the cumulative
   HFT targets through level 13 satisfy every weighted inequality and have
   exactly checked nonnegative integral packet witnesses. This is finite
   evidence, not an all-orders circuit classification or saturation theorem.
   See `trajectory_kernel/reports/TK6B4_WEIGHTED_CIRCUITS.md`.
13. **TK6B.5 local HFT reduction complete:** the triangular all-chiral
   inverse is an eight-term Möbius difference of $B_4$ multiplicities. Every
   weighted circuit therefore becomes an explicit local HFT coefficient
   inequality, and the operator commutes with cumulative sums and label
   translations. The formula is proved for all labels and independently
   checked through the full level-13 closure. Recursive circuit control, HFT
   partial-sum positivity and general integrality remain open. See
   `trajectory_kernel/reports/TK6B5_HFT_WEIGHTED_INEQUALITIES.md`.
14. **TK6B.5b/c prefix-shell and Regge-tail reduction complete:** eliminating
   alternative pivots gives the exact prefix-shell cone. The complete infinite
   cone has no nonzero finitely supported circuit, so all-orders control must
   use moving boundary-tail families. Universal interval tails telescope to
   bounded HFT endpoints, while mixed pullbacks can grow. Exact symmetric-
   vector factorization makes all 185 eligible $\ell$ shifts through level 13
   hold separately at each remainder degree and reveals the candidate
   half-slope bound. Stable $B_4$ Pieri transport is proved in the next
   milestone; contribution-wise remainder support is the remaining analytic
   target. See
   `trajectory_kernel/reports/TK6B5B_PREFIX_SHELL_DUALITY.md`.
15. **TK6B.5d stable Pieri translation proved:** a Racah--Speiser argument
   proves consecutive harmonic and symmetric-power translation for arbitrary
   tensorial or spinorial $B_n$ weights in the exact stable range. All 524
   active HFT remainder couplings in the 185 eligible adjacent shifts through
   level 13 satisfy that hypothesis, including 214 spinorial and 44
   negative-coefficient couplings. A sharper exterior-cost inequality passes
   for every unstable HFT product term through total degree 12, but a generic
   Pieri-cost shortcut is false. The HFT-specific contribution-wise remainder
   support theorem is proved in TK6B.5f. See
   `trajectory_kernel/reports/TK6B5D_STABLE_PIERI_TRANSLATION.md`.
16. **TK6B.5f analytic HFT support proved:** the exact Green--Schwarz
   telescope, a finite Weyl/Dirac fold, and uniform oscillator-tail bounds
   reduce the support theorem to 323 low-mode records. All pass, with minimum
   margin zero. Hence $[V_\mu]F_d\neq0\Rightarrow d\geq K(\mu)$ at every
   degree, closing the HFT premise of stable Pieri transport. This is not yet
   the recursive circuit or integral packetization theorem. See
   `trajectory_kernel/reports/TK6B5F_ANALYTIC_HFT_SUPPORT.md`.
17. **TK6B.6 cumulative Regge-tower construction isolated:** the Bars
   cumulative factor completes the HFT $B_4$ symmetric-vector tower into the
   restriction of the $D_5$ symmetric-vector tower. Thus any virtual lift of
   the HFT remainder gives an exact cumulative virtual lift. The all-chiral
   section is repaired through level 13 by only
   $-q^3(16_+-16_-)+(q^9+2q^{10}+2q^{11}+3q^{12})A_0$, with every corrected
   coefficient positive, integral and exactly rebranched. The $A_0$
   coefficients are fixed independently by an exact scalar-diagonal formula,
   not by protected data or a fitted optimizer. Stable $D_n$ Pieri transport
   is proved. The scalar tail is now the negative of a pre-telescope boundary
   index supported on nine fixed `D4` rays, with a common $(1-q)^2$ interior
   factor and five endpoint exceptions. The remaining all-orders problem is
   the sign of that explicit index and one-shell dominance. A second
   primitive inversion reduces the scalar sign to
   $\pi_3(N)\geq\pi_4(N-1)$. The DDF audit identifies the exact transverse
   vector Euler class and a canonical cumulative $B_4$ core
   $\widehat G$. It proves
   $Z_m/(1-q)=\operatorname{PE}(q9)\widehat G$ exactly and finds
   $\widehat G$ positive through degree 20; the former virtual remainder is
   $(1-q)\widehat G$. This is finite evidence rather than an all-orders module
   theorem. The audit also identifies the correct candidate map, but proves
   that its raw middle term is not injective:
   $\ker d_4=\operatorname{im}d_5$. Only the induced map from
   $K_4/\operatorname{im}d_5$ is automatically injective. Descending that
   primitive quotient through the universal supermultiplet remains open
   because the bosonic DDF differential does not commute with spacetime
   supersymmetry. The relative Dirac half nevertheless completes the
   representation-theoretic descent: it produces five gamma-traceless
   modules, and explicit projected-wedge maps between them form an exact
   polynomial free resolution with positive cokernel
   $\bigoplus_{n\geq0}[n,0,3,0]_{D_4}$. Its nonzero null fibre has
   twenty-dimensional homology in each of the final two positions, so the
   old truncated-Tor-vanishing target is withdrawn. Pairing the full
   resolution with the cumulative core gives the exact identity
   $(1-q)\Phi=(1+q)H_4-(1+q^2)B_\Gamma$. The remaining scalar gap is the resulting
   prefix dominance between $B_\Gamma$ and $H_4$, or equivalently the derived
   homology statement on the mass-graded $\mathfrak D^+(Z_m)$ module. After
   the required outer antisymmetrization, this prefix is exactly
   $\mathfrak D^+(R_{n+1}-R_n)$, so the resolution closes back onto the known
   virtual three-hook shell rather than supplying a coefficientwise shortcut.
   The orthosymplectic operator $Q^1$ acts separately within the Howe
   multiplicity module and obeys $\{Q^1,Q^1\}=T^{11}$; it must be combined
   with, not identified with, the adjacent projected-wedge maps. The complete
   spinor-form triangle now supplies that local combination explicitly:
   $\Gamma E+E\Gamma=C$, the needed trace Laplacians are invertible, and the
   failure of the projected Clifford map factors exactly through the trace
   complement as $-2P'E(\Gamma G)^{-1}CI$. The remaining question is global
   compatibility with the HFT quotient and concentration of the resulting
   gamma-trace spectral sequence.
   Moving the cumulative vector tower through the scalar functional gives a
   second exact all-orders form supported only on the three principal hook
   families $(k)$, $(k,1)$ and $(k,1,1)$; its order-eight recurrence is proved
   from the $B_4$ Weyl alternant. This supplies a direct interface to the
   orthosymplectic lowest-weight modules. A coefficientwise Regge injection is
   refuted by 108 negative first-row differences in the tested Bars triangle,
   so the required filtered diagonal dominance remains open.
   If proved, this direct construction bypasses general circuit
   classification and semigroup saturation. See
   `trajectory_kernel/reports/TK6B6_CUMULATIVE_REGGE_UPLIFT.md` and
   `trajectory_kernel/reports/TK6B6_SCALAR_BOUNDARY_REDUCTION.md`.
18. **GU1 complete through level 7:** the oscillator-count-refined Appendix B
   construction of hep-th/0310292 is reproduced exactly and its cumulative
   ungraded lift is positive with the correct HFT $SO(9)$ restriction. It
   agrees with Bars' displayed lift, and with the protected algorithmic
   continuation, through level 5. Beginning at level 6 it differs from the
   protected continuation by outer-chirality kernel directions. This supplies
   an independent positive continuation of the existence pattern, not a
   disagreement with a higher-level choice made by Bars. See
   `graded_uplift/reports/GU1_LITERATURE_GRADING_AUDIT.md`.
19. **GU2 complete through level 7 under explicit finite bounds:** after
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
20. **GU3 complete through level 7 in the resolved IIA domain:** opposite
    right-moving chirality is exactly equivalent to the axial relation
    $\nu_R=\Delta_R+J_R$, and every Bars $(\ell',\nu)$ block is reproduced.
    The resolved chiral maps and their tensor products are injective, however,
    so the unique closed lift is the paper character times its outer
    conjugate. It first differs from the closed character formed from the
    protected algorithmic continuation at level 6 by an outer-even
    restriction-kernel element. See
    `graded_uplift/reports/GU3_IIA_CLOSED_REFINEMENT.md`.
21. **GU4 complete through level 3:** direct lifting of
    $R_n^9\otimes R_n^9$ in the full outer-closed parent domain gives a unique
    positive outer-invariant result. At level 3, outer invariance reduces 27
    positive lifts to one. The factorized representatives recover both Bars
    $\ell'$ labels as $D_5\downarrow B_4$ interlacing depths. See
    `graded_uplift/reports/GU4_DIRECT_CLOSED_LOW_LEVELS.md`.
22. **GU5 level-6 check complete:** the direct closed conditions admit at
    least two distinct positive outer-even lifts at level 6, while the naive
    interlacing-depth rule has no positive lift beginning already at level 5.
    The protected algorithmic continuation and the paper lift share the same
    depth defect, so this refinement cannot distinguish their level-6
    chirality choices. See
    `graded_uplift/reports/GU5_LEVEL6_DIRECT_CLOSED_AND_DEPTH.md`.
23. **Current objective:** prove negativity from degree nine of the explicit
    scalar boundary index in its smallest current form,
    $\Phi_q(G)=\langle\mathscr C(q),Z_m(q)\rangle_{B_4}$. Alternating
    inversion of the five low-form multiplicity series gives the sharper exact
    form $\Phi=-(1+q^2)D+qH_4$, so the scalar theorem is now
    $D_N+D_{N-2}\geq h_4(N-1)$ for $N\geq9$. Here
    $h_k(d)=(-1)^k\langle s_k,Q_d\rangle$ and
    $D=H_3-qH_2+q^2H_1-q^3H_0$. A second inversion
    $\Pi_k=\sum_{r=0}^k(-q)^rH_{k-r}$ sharpens this to the adjacent bidegree
    inequality $\pi_3(N)\geq\pi_4(N-1)$. The transverse DDF creators construct
    the natural degree-$(+1,-1)$ Koszul map. Cumulative completion gives the
    exact auxiliary factorization
    $Z_m/(1-q)=\operatorname{PE}(q9)\widehat G$, where $\widehat G$ is
    positive through degree 20 and restricts to the transverse quotient $G$.
    Proving this positivity by an actual regular-sequence construction is a
    newly isolated module-level target, but it does not alone imply the
    adjacent inequality: neither $\Pi_3$ nor $\Pi_4$ is a raw exterior-form
    multiplicity of the core in the finite scan. The raw middle map is not
    injective: $\ker d_4=\operatorname{im}d_5$. The preferred route is now to
    identify the primitive source $K_4/\operatorname{im}d_5$ and its
    degree-three target with $\Pi_4$ and $\Pi_3$ after physical-state and
    universal-supermultiplet descent. The relative Dirac half now gives the
    complete gamma-traceless free resolution above, not merely its injective
    top symbol. Its exact positive-core pairing sharpens the preferred next
    step: evaluate the full derived tensor product on
    $\mathfrak D^+(Z_m)$ and prove the $B_\Gamma$--$H_4$ prefix dominance. The
    correctly oriented prefix is already known to be precisely the virtual
    three-hook shell, so this reformulation is a structural model of the same
    sign problem rather than an independent positivity argument. The
    orthosymplectic generator $Q^1$ acts on the distinct Howe multiplicity
    factor; its curvature $\{Q^1,Q^1\}=T^{11}$ must be handled during that
    descent. The action must be constructed before the mode-one quotient and
    transferred to primitive homology. The local transfer is now fixed, not
    conjectural: the full spinor-form triangle obeys
    $\Gamma E+E\Gamma=C$, and the projected defect is exactly
    $-2P'E(\Gamma G)^{-1}CI$. Thus the next proof obligation is to show that
    universal-supermultiplet division preserves the gamma-trace filtration
    and that its spectral sequence has only the required $\Pi_4$ and $\Pi_3$
    edge homology. The direct
    fallback is a coefficient proof from the HFT oscillator product. In that
    fallback, the new
    all-orders identity
    $\mathscr C(1-q)\operatorname{PE}(q9)=\sum_{k\geq0}q^k(R_k-R_{k+1})$
    reduces the calculation to the three principal hook trajectories
    $(k)$, $(k,1)$ and $(k,1,1)$ on $\widehat G$. A termwise Regge injection
    between those trajectories is already refuted, so any successful proof
    must mix the two diagonal gradings.
    The standard superstring BRST no-ghost spectral sequence supplies a
    useful concentration template but not the result: its adjacent grading is
    ghost number, not the exterior degree above, and its two surviving copies
    are isomorphic. A BRST proof would first have to reproduce the compact
    refined kernel after universal-supermultiplet division. Moreover, the
    bosonic DDF differential is not spacetime-supersymmetric, while its
    literal super-Koszul completion begins with a spinor rather than the
    shifted scalar in the compact kernel before relative Dirac insertion.
    The exact Dirac resolution resolves that character mismatch and computes
    the universal Tor data, but not the remaining physical-module homology or
    prefix dominance.
    The wall--curvature, modified-Frobenius, Plücker and
    bordered-determinant reductions remain exact possible constructions of
    that complex. Then derive the five
    non-scalar $A_0$ boundary functionals and prove one-shell dominance, using
    stable $D_5$ Pieri transport to remove the upper chamber. The recursive
    boundary-tail/circuit and saturation programmes remain independent
    structural alternatives, but are not required if this explicit integral
    construction closes. In parallel, seek an all-$\ell$ proof of the TK6A
    quotient formulas and test whether the BBMS cumulative construction
    telescopes. Any one constructive all-orders existence proof would suffice;
    it need not choose a unique point of the positive fibre. Matching the
    protected algorithmic continuation is a stronger secondary question and
    is not part of Bars' all-orders existence claim.
24. Use the protected levels 1--10 only as a later comparison layer, not as
    input to the construction.
