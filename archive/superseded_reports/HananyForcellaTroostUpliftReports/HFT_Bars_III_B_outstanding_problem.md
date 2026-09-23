# HFT, Bars III.B, and the outstanding all-orders problem

> **Superseded (23 September 2026):** The statement that the HFT $SO(10)$
> realization already gives positive cumulative coefficients is withdrawn.
> The formulation of the all-orders problem remains useful. See `STATUS.md` and
> `FINITE_CROSS_SECTION_REPORT.md` for the current obstruction.

(ChatGPT outlook post Direction1 M1, M2, M3, M4)

## Definitions

### The HFT massive-mode partition function

Forcella, Hanany and Troost (HFT), *The covariant perturbative string spectrum*, arXiv:1007.2622, construct an analytic generating function for the perturbative massive Type-II string spectrum in an \(SO(9)\)-covariant form.

After factoring out the universal massive supersymmetry multiplet, their massive-mode generating function is

\[
Z_m(q)=\frac{Z_{\mathrm{Left}}(q)-Z_0}{q\,Z_Q}.
\]

This is the object we identify with our perturbative residual spectrum. In our notation,

\[
\boxed{r(q)=Z_m(q)}
\]

with

\[
r(q)=\sum_{n\geq1} r_n q^{n-1}.
\]

Thus \(r_n\) is the residual \(SO(9)\) character at massive oscillator level \(n\), after removing the common massive SUSY factor.

### Our Bars III.B object

Bars III.B proposes adding the cumulative spectrum

\[
R_n=\sum_{i=1}^{n}r_i.
\]

Consequently our generating function is

\[
\boxed{
R(q)=\sum_{n\geq1}R_nq^{n-1}
     =\frac{r(q)}{1-q}.
}
\]

The factor \(1/(1-q)\) is the generating function for the additional oscillator \(l'\) in Bars III.B, which carries no \(SO(9)\) quantum numbers.

The question is whether every coefficient \(R_n\), initially an \(SO(9)\) character, is the restriction of a genuine positive-integral \(SO(10)\) representation.

## What HFT gives us

HFT give an **analytic generating function for the perturbative massive Type-II spectrum**, written in terms of \(SO(9)\) characters.

After removing the universal massive SUSY factor, their object is our

\[
r(q)=\sum_{n\ge1}r_nq^{n-1}.
\]

So this is not something we inferred numerically: we have an analytic expression for the whole formal series.

## What we do

We form

\[
\boxed{R(q)=\frac{r(q)}{1-q}}
\]

so that

\[
R_n=r_1+r_2+\cdots+r_n.
\]

That is precisely the cumulative spectrum appearing in Bars III.B.

Crucially, \(R(q)\) is initially only an \(SO(9)\)-character-valued series. There is no \(SO(10)\) symmetry built into the definition.

## The conjecture

We are asking whether

\[
\boxed{R(q)\in R(SO(10))[[q]]}
\]

in the strong sense that every coefficient \(R_n\) is the restriction of an honest positive integral \(SO(10)\) representation:

$$
R_n^{SO(9)}
=
\operatorname{Res}_{SO(10)\to SO(9)}
R_n^{SO(10)},
$$

with

$$
R_n^{SO(10)}
=
\sum_\lambda m_{\lambda,n}[\lambda],
\qquad m_{\lambda,n}\ge0.
$$

We have now established this through level 10.

The recent HFT experiments make this substantially stronger than simply taking the known \(R_n\)'s and finding \(SO(10)\) lifts. The HFT construction itself has an independent \(SO(10)\) realization, which reproduces the \(SO(9)\) HFT series and then gives the positive cumulative coefficients.

## So the actual outstanding mathematical problem

Exactly:

\[
\boxed{\text{Why is }r(q)/(1-q)\text{ an }SO(10)\text{ character to all orders?}}
\]

Or, more usefully:

> **Find an analytic proof that every coefficient of \(r(q)/(1-q)\) is the restriction of a positive-integral \(SO(10)\) character.**

There are three increasingly strong possible forms such a result could take.

### 1. A character-theoretic proof

Find an explicit \(SO(10)\)-valued generating function

$$
\mathcal R^{SO(10)}(q)
$$

such that

$$
\operatorname{Res}\mathcal R^{SO(10)}(q)
=
\frac{r^{SO(9)}(q)}{1-q},
$$

and prove that every coefficient of \(\mathcal R^{SO(10)}\) is positive integral.

**This would settle it.**

### 2. A structural branching identity

Perhaps the cumulative operation has a general representation-theoretic explanation. The leading Regge trajectory gives a particularly clean example:

$$
\sum_{j=0}^{n-1}[j,0,0,0]_{SO(9)}
=
[n-1,0,0,0,0]_{SO(10)}\downarrow SO(9).
$$

If the whole HFT spectrum can be organised into analogous branching identities, that could explain the positivity rather than merely verifying it.

### 3. A generating-function identity

This may be the most promising direction.

Find a closed expression of the form

$$
\boxed{
\frac{r^{SO(9)}(q)}{1-q}
=
\operatorname{Res}_{SO(10)\to SO(9)}
\mathcal F_{SO(10)}(q)
}
$$

where \(\mathcal F_{SO(10)}(q)\) has manifestly positive representation coefficients.

Then the all-orders theorem follows immediately.

## Where the plethystic logarithm fits

The plethystic-logarithm work is useful, but probably not itself the proof.

We have the exact all-orders algebraic identity

\[
PL[R]=PL[r]+q\,\mathbf1.
\]

Thus the Bars operation itself is extremely simple in multiplicative/PE language: it adds one trivial degree-one generator.

But this does not yet explain why the resulting coefficients reorganise into positive \(SO(10)\) characters.

## Present status

We can therefore state the research problem very cleanly:

> **We have reduced Bars III.B to an all-orders character identity for a known analytic HFT generating function. The identity has been verified exactly through level 10. The remaining problem is to find the representation-theoretic mechanism that makes the \(SO(10)\) positivity inevitable.**

The ten-level computation is now evidence for the conjecture rather than the main story.
