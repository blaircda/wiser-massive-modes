# Oscillator-Graded Uplift Status

**Last updated:** 24 September 2026

## GU1 — Literature grading audit

**Status:** complete through level 7.

- The chiral oscillator Fock space has been refined simultaneously by string
  level $\ell=\sum nN_n$ and oscillator count $\nu=\sum N_n$.
- Dividing each $(\ell,\nu)$ coefficient by the positive $8_v+8_s$ factor and
  then restoring fermion parity reproduces the paper's graded primary
  convention.
- Forgetting $\nu$ agrees exactly with the independently derived HFT $SO(9)$
  primary restricted to $SO(8)$ at every level 1--7.
- Exact weight-space branching verifies the transcribed Appendix B
  $SO(10)\times SO(2)_\Delta$ candidate against the refined oscillator data at
  every level 1--7.
- Forgetting $\Delta$ and cumulatively summing the Appendix B candidates gives
  a positive $SO(10)$ character at every tested horizon, with the exact
  cumulative HFT $SO(9)$ restriction.
- The literature candidate lies in the current fixed-positive-chirality TK
  domain only through level 5. At level 6 it contains the outer-conjugate
  parents $[0,0,0,1,0]$ and $[1,0,0,1,0]$.
- A separate protected comparison agrees with Bars through level 5 and first
  differs at level 6 by

$$
[0,0,0,1,0]+[1,0,0,1,0]
-[0,0,0,0,1]-[1,0,0,0,1].
$$

- At level 7 the difference is the analogous sum of outer-chirality
  differences for the 560, 144 and 720 representations.

Thus the IIB/AdS grading produces a coherent positive cumulative lift but not
the protected Bars lift from level 6 onward.

## GU2 — Bars compatibility in an outer-closed graded domain

**Status:** complete through level 7 under explicit finite bounds.

- The `paper-bound` domain implements
  $2\Delta_{\min}=2+2a_1+4a_2+6a_3+5a_4+3a_5$ and
  $\Delta\leq\ell+1$.
- The `outer-closed` domain adds every $a_4\leftrightarrow a_5$ conjugate at
  the same $\Delta$.
- Appendix B remains feasible at every level 1--7. Bars is feasible through
  level 5 and infeasible at levels 6 and 7 in both domains.
- Exact rational rank certificates for the outer-closed domain are
  $159<160$ at level 6 and $269<270$ at level 7 after adjoining the Bars
  target. Hence the failures are rational, not merely integral or numerical.
- Both coefficient matrices have full column rank. The feasible paper lift is
  therefore unique inside these finite domains.
- At level 6, nested outer-closed enlargements through
  $\Delta_{\max}=7,8,9,10$ all remain rationally infeasible for Bars, with
  full column ranks $159,269,436,681$ and augmented ranks one larger.

See `reports/GU2_GRADED_BARS_COMPATIBILITY.md`.

## GU3 — Type-IIA closed refinement

**Status:** complete through level 7 in the resolved finite domain.

- The Type-IIA right sector is the $D_5$ outer conjugate of the left sector.
  Equivalently its grading is $\nu_R=\Delta_R+J_R$ while the left relation is
  $\nu_L=\Delta_L-J_L$.
- Both formulations reproduce the opposite-chirality refined oscillator
  spectrum exactly at every level 1--7.
- Bars' nonperturbative label $\ell'=n-\ell$ is retained separately in each
  sector. Every $(\ell',\nu)$ source block is exact.
- The outer-closed graded maps have full column ranks
  $3,9,22,46,88,159,269$ through level 7. Hence the resolved cumulative maps
  and their left-right tensor products are injective.
- The unique resolved closed lift is the cumulative paper character tensored
  with its outer conjugate. It agrees with the Bars closed character through
  level 5 and first differs at level 6.
- The closed difference has 64 irreducible terms at level 6 and 140 at level
  7. It is nonzero, outer-even and lies in the closed restriction kernel.
- Opposite chirality therefore does not cancel the chiral ambiguity; it turns
  an outer-odd chiral difference into an outer-even closed difference.

See `reports/GU3_IIA_CLOSED_REFINEMENT.md`.

## GU4 — Direct closed low-level lift

**Status:** exact baseline-free calculation complete through level 3.

- The target is formed before uplifting:
  $T_n=R_n^9\otimes R_n^9$.
- The exhaustive finite domain contains every $D_5$ top parent, of both
  chiralities, in the complete branching closure.
- At levels 1 and 2 there is one positive lift even without imposing outer
  invariance. At level 3 there are 27 positive lifts, but exactly one is outer
  invariant.
- The unique answers are
  $X_2=10\otimes10=1+45+54$ and
  $X_3=(54+16_+)\otimes(54+16_-)$.
- Individual $\ell'$ source blocks generally do not have positive $SO(10)$
  lifts. At level 2, both cross blocks are bare $9$s and cannot lift
  positively on their own.
- The source labels are nevertheless recovered exactly in the factorized
  representative by the branching depth
  $d=\lambda_1-\mu_1$: $d=\ell'$ through level 3 in both chiral sectors.
- Multiplication by the intrinsic positive $Q_{\mathrm{cl}}$ preserves all
  desired properties but adds no selection constraint once a positive primary
  lift has already been chosen.

See `reports/GU4_DIRECT_CLOSED_LOW_LEVELS.md`.

## GU5 — Level-6 direct closed and interlacing-depth tests

**Status:** exact baseline-free results complete; protected comparison kept
separate.

- Positivity, exact restriction and outer invariance do not select a unique
  closed lift at level 6. Starting from one baseline-free positive chiral
  lift, flipping
  $[3,0,0,0,1]\to[3,0,0,1,0]$ gives another. Their closed products with
  their respective outer conjugates are distinct positive outer-even
  characters with the same $SO(9)$ restriction.
- The closed difference has 92 irreducible terms, coefficient range
  $[-8,8]$, dimension zero, and zero $SO(9)$ restriction.
- Exhaustive refined branching shows that the naive rule
  $\ell'=\lambda_1-\mu_1$ has positive solutions through level 4 but none at
  levels 5 or 6. The first obstruction is an excess spinor at depth 1 at
  level 5.
- A separate protected comparison finds that both the Bars and paper
  characters have exactly the same depth defect. At level 6 their characters
  differ, but their interlacing-depth images are identical because the depth
  is blind to outer chirality.
- Consequently the exact GU4 low-level depth pattern is not an analytic
  selector without an additional correction or label.

See `reports/GU5_LEVEL6_DIRECT_CLOSED_AND_DEPTH.md`.

## Next question

GU3 shows that imposing the full IIB-derived $\Delta$ grading separately on
the IIA left and right sectors remains too rigid and uniquely forces the paper
candidate. The next physically distinct question is whether Bars' genuine
IIA/M-theory labels $(\ell',W)$ support a direct closed uplift normalized by
the intrinsic positive closed supermultiplet, without first assigning an
IIB-style $\Delta$ to each chiral factor. The finite GU2 obstruction still
invites an analytic triangularity proof, but that proof would explain the IIB
selector rather than produce the Bars selector.

GU4 showed that dropping the IIB $\Delta$ grading is useful at low levels, but
GU5 rules out the simplest continuation: closed outer invariance is non-unique
at level 6, while unmodified interlacing depth fails already at level 5. The
next question is therefore whether the genuine IIA/M-theory label $W$ supplies
a principled correction to the filtration, or whether left and right source
data must be coupled before diagonal $SO(10)$ decomposition in a way not
captured by a one-factor depth.
