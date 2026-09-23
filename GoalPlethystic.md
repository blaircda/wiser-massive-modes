# Background

The ultimate goal is to understand possible 11-dimensional structure present in the massive levels of the type IIA superstring.

We are investigating an old proposal of Bars found in https://arxiv.org/abs/hep-th/9503228, specifically the proposal of Section III.B.

The logic is roughly as follows.

Consider the left- or right-moving sector of the type IIA superstring. The massive states can be ordered by level \(l=1,2,\ldots\). They are initially constructed in light-cone gauge and given as \(SO(8)\) multiplets \(F_l\). As massive states in 10 dimensions, they reorganise into \(SO(9)\) multiplets. These turn out to have the form

$$
F_l = r_l \otimes (44+84+128),
$$

where the universal factor \((44+84+128)\) is the basic massive supermultiplet.

The idea is to find an 11-dimensional uplift in which we reorganise the full string states into \(SO(10)\) multiplets. When we form the full string states by tensoring left- and right-moving sectors, the `square' of the massive supermultiplet can be shown to lift to \(SO(10)\). The individual \(r_l\), or their products, do not.

Bars conjectures that one should add additional non-perturbative states to fill out \(SO(10)\) multiplets.

The simplest conjecture, which we will refer to as the minimal conjecture, is that of Section III.B of https://arxiv.org/abs/hep-th/9503228. This claims that

$$
R_l = \sum_{l'=1}^{l} r_{l'}
$$

form \(SO(10)\) multiplets, and verifies this for \(l=1,2,3,4,5\).

In this project we have extended this to \(l=6,7,8,9,10\).

This has been done in two ways: firstly by writing raw Python code to do the group theory ourselves (using Gemini agents in Antigravity), and then by re-verifying this using Sage.

In this working directory, the latter can be checked by running

```text
bin/sage-run massive_SO8_to_S010.py
```

The found \(SO(10)\) multiplets are located in `massive_SO10.py`.

Our goal now is to try to find hints for an analytic understanding of these multiplets.

# Cumulative SO(10) Spectrum and Plethystic Structure

Let \(r_n\) denote the ordinary perturbative massive type-IIA spectrum at oscillator level \(n\), reduced to its \(SO(9)\) representation content. Define the generating series

$$
r(q)=\sum_{n\geq1} r_n q^{n-1}.
$$

Bars III.B proposes that the corresponding new massive level \(n\) carries the cumulative spectrum

$$
R_n=\sum_{i=1}^{n}r_i.
$$

Hence the generating series for the proposed spectrum is

$$
R(q)=\sum_{n\geq1}R_n q^{n-1}
    =\frac{r(q)}{1-q}.
$$

The factor

$$
\frac1{1-q}=1+q+q^2+\cdots
$$

therefore implements the additional oscillator \(l'\), which carries no \(SO(9)\) quantum numbers and simply repeats each \(r_i\) at all subsequent levels.

## Plethystic investigation

Treat \(R(q)\) as a character-valued formal power series after lifting its coefficients to \(SO(10)\). Compute its plethystic logarithm

$$
\operatorname{PL}[R(q)]
=
\sum_{k\geq1}\frac{\mu(k)}{k}
\log\!\left(R(q^k)\right),
$$

with the logarithm interpreted in the representation ring via Adams operations.

The aim is to determine whether the observed positive \(SO(10)\) decomposition of every \(R_n\) reflects a deeper structure. In particular:

1. identify the signed \(SO(10)\) representations appearing in the plethystic logarithm;
2. determine whether any independent graded-algebra construction justifies
   interpreting those signs as generators and relations;
3. look for a simple representation-theoretic explanation of the \(1/(1-q)\) cumulative construction;
4. determine whether the resulting structure gives evidence for an analytic explanation of Bars III.B, rather than merely an empirical level-by-level character identity.

This is a test of the \(SO(10)\) character identity itself.

## Current conclusion

The exact formal identity

$$
\operatorname{PL}[R(q)]=\operatorname{PL}[r(q)]+\mathbf 1q
$$

is established, but it does not explain $SO(10)$ positivity. Earlier
pure-spinor, on-shell-relation and general syzygy interpretations of individual
signed coefficients have been withdrawn. See `PLETHYSTIC_STATUS.md` for the
authoritative account.
