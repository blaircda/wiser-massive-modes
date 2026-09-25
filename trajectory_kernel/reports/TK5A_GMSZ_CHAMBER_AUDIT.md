# TK5a — GMSZ Support-Chamber and Shift Audit

**Status:** complete through HFT level 11  
**Last updated:** 24 September 2026  
**Provenance:** baseline-free

## 1. Question

Georgoudis, Minahan, Ström and Zoumis (GMSZ) give an empirical support rule
and three families of multiplicity shifts for the massive $SO(9)$
super-representations in
[arXiv:2609.04107](https://arxiv.org/abs/2609.04107). TK5a asks:

1. whether their support polytope reproduces the HFT-derived spectrum in our
   conventions;
2. whether their restricted shift chambers explain why the raw Regge shift in
   TK1 sometimes succeeds and sometimes fails;
3. which of the published shift families are actually testable through level
   11.

The implementation is `trajectory_kernel/chamber_audit.py`. It derives the
$SO(9)$ characters from `hft_so9.py` and imports no protected $SO(10)$ data.

The GMSZ rules remain empirical. Exact agreement in this finite window is not
an all-orders proof.

## 2. Support polytope

For an $SO(9)$ highest weight $[\ell,m,r,s]_9$, define

$$
\widetilde n=n-\ell-3m.
$$

GMSZ claim for $n>6$ that the representation is present precisely when

$$
6r+5s\leq\widetilde n+6,
$$

$$
6r+4s\leq\widetilde n+2,
$$

$$
6r+3s\leq\widetilde n+1,
$$

$$
2s\leq\widetilde n-1,
$$

apart from the isolated gap $[n-2,0,0,0]_9$.

Equivalently, at fixed $(n,m,r,s)$ the largest permitted leading label is

$$
\ell_{\max}=n-3m-c(r,s),
$$

where

$$
c(r,s)=\max(6r+5s-6,\,6r+4s-2,\,6r+3s-1,\,2s+1).
$$

The predicted and independently observed supports agree exactly at every
level in the claimed range available to us:

| Level | Predicted irreps | HFT irreps | Missing | Unexpected |
| ---: | ---: | ---: | ---: | ---: |
| 7 | 23 | 23 | 0 | 0 |
| 8 | 32 | 32 | 0 | 0 |
| 9 | 43 | 43 | 0 | 0 |
| 10 | 56 | 56 | 0 | 0 |
| 11 | 72 | 72 | 0 | 0 |

The formula is deliberately also evaluated below its claimed range, but only
as a diagnostic. The extra predicted but absent labels are:

| Level | Predicted but absent |
| ---: | --- |
| 1 | none |
| 2 | none |
| 3 | $[0,0,0,0]$ |
| 4 | $[0,0,0,0]$, $[0,0,0,1]$ |
| 5 | $[1,0,0,0]$ |
| 6 | $[0,0,0,0]$, $[0,0,1,0]$ |

These are not counterexamples because GMSZ state the rule only for $n>6$.
In particular, the isolated low-level behavior of $[0,0,1,0]_9$ does not
contradict the stable support chamber beginning at level 7.

For $s=0$ and $r\geq1$, the support condition becomes

$$
n\geq\ell+3m+6r-1.
$$

It therefore explains the level-11 entrance of $[0,0,2,0]_9$ and, if the
empirical rule persists, predicts $[0,0,3,0]_9$ at level 17.

## 3. Multiplicity-shift chambers

TK5a encodes equations (3.32)--(3.35) literally. A comparison is made only
when the target is in the claimed $n>6$ domain and the shifted representation
actually belongs to the lower-level allowed set, as required by GMSZ. Every
admissible positive shift size $k$ is tested; their optional computational
shortcut of taking only the largest $k$ in the first applicable family is not
imposed.

The results are:

| Shift family | Level cost per step | Tests | Failures |
| --- | ---: | ---: | ---: |
| $\ell\mapsto\ell-k$ | $k$ | 253 | 0 |
| $m\mapsto m-k$ | $3k$ | 50 | 0 |
| $r\mapsto r-k$ | $6k$ | 0 | — |
| **Total** |  | **303** | **0** |

The 253 $\ell$-shift tests include

$$
k=1:95,\quad k=2:49,\quad k=3:49,\quad k=4:21,
$$

$$
k=5:21,\quad k=6:7,\quad k=7:7,\quad k=8:2,
\quad k=9:2.
$$

The 50 $m$-shift tests split as $36,12,2$ for $k=1,2,3$.

No $r$-shift relation is admissible through level 11. This family is
**untested**, not verified. Its level cost and chamber inequality postpone its
first applicable examples beyond the current HFT window.

## 4. Resolution of the TK1 Regge mismatches

Restrict to adjacent comparisons whose target level is at least 7. The
unrestricted TK1 shift gives:

| Region | Comparisons | Matches | Mismatches |
| --- | ---: | ---: | ---: |
| Inside the GMSZ $\ell$ chamber | 95 | 95 | 0 |
| Outside the GMSZ $\ell$ chamber | 75 | 3 | 72 |
| **Total** | **170** | **98** | **72** |

Thus the published chamber inequality does much more than identify a sector
where the Regge shift happens to work. In the current window it captures 95
of the 98 matches and excludes every mismatch. The three matches outside the
chamber are not promoted to a rule; they may be accidental or consequences of
additional structure.

This sharply refines the TK1 conclusion. Raw Regge transport is not a global
identity, but it is exact on the tested GMSZ upper chamber.

## 5. Interpretation and limits

TK5a establishes a useful decomposition of the $SO(9)$ problem:

- an upper chamber whose multiplicities are transported from lower levels;
- a complementary core where the empirical transport rule supplies no
  value and genuinely new multiplicity data may enter.

It does not yet establish that the core has finite width or finitely many
source types. It also does not determine an $SO(10)$ lift: all these relations
are visible after restriction to $SO(9)$ and therefore cannot by themselves
distinguish representatives differing by the restriction kernel.

The corresponding decomposition and kernel-source test are carried out in
`TK5B_CHAMBER_CORE_KERNEL_SOURCES.md`.

## 6. Reproduction

```text
./bin/sage-run -m trajectory_kernel.chamber_audit --self-test
./bin/sage-run -m trajectory_kernel.chamber_audit --max-level 11
./bin/sage-run -m trajectory_kernel.chamber_audit --max-level 11 --verbose
```

The verbose form prints any support or shift violation. A clean finite run
does not convert the empirical GMSZ statements into proven identities.
