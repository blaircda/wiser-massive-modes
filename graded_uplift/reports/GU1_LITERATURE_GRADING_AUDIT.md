# GU1 — Oscillator-Count-Refined Literature Uplift

**Status:** complete through level 7  
**Last updated:** 24 September 2026

## 1. Scope

Beisert, Bianchi, Morales and Samtleben organize chiral flat-space string
primaries under $SO(10)\times SO(2)_\Delta$ by retaining the unweighted
oscillator number $\nu$ and imposing

$$
\Delta-J=\nu
$$

after branching $SO(10)\to SO(8)\times SO(2)_J$. Their physical argument is
specific to type-IIB string theory on $AdS_5\times S^5$. GU1 tests only the
resulting representation-theoretic construction. The source is
[hep-th/0310292](https://arxiv.org/abs/hep-th/0310292), with its
[INSPIRE entry](https://inspirehep.net/arxiv/hep-th/0310292).

## 2. Independent refined oscillator spectrum

The new module `graded_uplift/refined_spectrum.py` constructs the light-cone
$SO(8)$ Fock space while retaining both

$$
\ell=\sum_{n\geq1}nN_n
$$

and

$$
\nu=\sum_{n\geq1}N_n.
$$

Every $(\ell,\nu)$ coefficient is independently divided by the common positive
$8_v+8_s$ supersymmetry factor. The value of $\nu$ is retained rather than
reduced by one. Fermion parity is subsequently restored from the $D_4$
conjugacy class, producing the signed character convention used in the paper.

At every level 1--7, forgetting $\nu$ gives exactly the restriction to $SO(8)$
of the baseline-free HFT $SO(9)$ primary $r_\ell^9$.

## 3. Exact refined branching

`graded_uplift/refined_branching.py` groups every weight of a $D_5$ irrep by
its fifth orthogonal coordinate $J$. It thereby computes the exact branching
to $D_4\times SO(2)_J$ without discarding the charge. A term tagged by
$\Delta$ is then placed at $\nu=\Delta-J$.

The vector self-test gives

$$
\mathbf{10}\downarrow SO(8)\times SO(2)_J
=\mathbf 8_{v,0}+\mathbf1_{+1}+\mathbf1_{-1}.
$$

One subtlety in Appendix B is essential. A displayed starred term expands as

$$
[k,\ldots]^*_{\Delta}
=[k,\ldots]_{\Delta}-[k-1,\ldots]_{\Delta+1},
$$

not at fixed $\Delta$. With this convention, the transcribed Appendix B
candidate agrees exactly with the independently derived $(\ell,\nu)$ spectrum
at every level 1--7.

## 4. The positive cumulative accident

After forgetting $\Delta$, each individual Appendix B level is virtual because
of the starred differences. Nevertheless, every cumulative sum through levels
1--7 is a positive integral $SO(10)$ character. Its restriction is exactly the
cumulative baseline-free HFT $SO(9)$ character.

Thus the paper's unrelated IIB construction does reproduce the essential Bars
phenomenon in this finite window:

> virtual single-level $SO(10)$ data become positive after cumulative summation.

This is an exact representation-theoretic coincidence, not evidence that the
AdS mass formula has an eleven-dimensional interpretation.

## 5. Difference from the Bars completion

The coincidence does not select the protected Bars lift. The two cumulative
lifts agree through level 5. At level 6, the literature candidate minus the
protected completion is

$$
[0,0,0,1,0]+[1,0,0,1,0]
-[0,0,0,0,1]-[1,0,0,0,1].
$$

This difference is a sum of outer-chirality differences and restricts to zero
in $SO(9)$. Both cumulative lifts are positive.

At level 7, the literature candidate similarly chooses the opposite chirality
for the 560, 144 and 720 representations:

$$
[0,1,0,1,0]+[1,0,0,1,0]+[2,0,0,1,0]
$$

minus their three $a_4\leftrightarrow a_5$ conjugates.

The present trajectory-kernel programme fixed the positive-chirality parent
family from the outset, so the literature candidate exits that finite domain
at level 6. It therefore cannot yet be compared directly with the six TK5c
minimal witnesses.

## 6. Conclusion and limitation

GU1 establishes four exact finite facts:

1. the oscillator-count refinement is independently reproducible;
2. the Appendix B graded lift passes that refined check through level 7;
3. its cumulative ungraded lift is positive and has the desired $SO(9)$
   restriction;
4. it differs from the Bars lift by outer-chirality kernel directions beginning
   at level 6.

The calculation has not proved that the grading uniquely forces the literature
answer in the larger virtual graded ring. GU2 must include outer-chirality
kernel generators and test whether a graded refinement of the Bars completion
also exists under explicit finite $\Delta$ assumptions.

## 7. Reproduction

```text
./bin/sage-run -m graded_uplift.verify_paper_grading --self-test
./bin/sage-run -m graded_uplift.verify_paper_grading --max-level 7 --verbose
./bin/sage-run -m graded_uplift.verify_against_baseline --max-level 7 --verbose
```
