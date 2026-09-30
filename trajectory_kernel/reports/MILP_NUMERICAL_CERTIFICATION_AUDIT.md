# Floating-Point MILP Certification Audit

**Status:** reported rounding risk confirmed and hardened; exact primal
verification added; solver optimality and infeasibility remain GLPK-backed

**Scope:** `trajectory_selection.py`, `kernel_generating_series.py`,
`chamber_core.py`, `chamber_witness.py`, `restriction_semigroup.py`

**Last updated:** 25 September 2026

## Finding

Sage's GLPK mixed-integer backend returns floating-point objective and variable
values even for integral models. The reported concern was valid:

- `trajectory_selection.py` rounded each lexicographic objective and
  immediately imposed the rounded integer as a hard equality without first
  checking the numerical drift;
- its final-coordinate minima and maxima were rounded without extracting and
  exactly verifying endpoint paths;
- the other audited modules generally performed exact representation-theoretic
  checks later, but still silently rounded raw integer-variable values.

No incorrect existing numerical result was found by the focused reruns. The
unguarded path was nevertheless fragile and did not meet the project's desired
standard of explicit certification.

## Changes

The new shared module `trajectory_kernel/milp_certification.py` rejects
nonfinite values and any putatively integral value farther than $10^{-6}$ from
its nearest integer.

The audited callers now add the following domain-specific checks:

- `trajectory_selection.py` checks every lexicographic objective before
  freezing it, extracts an integral path at every stage, recomputes the stage
  cost exactly, and verifies positivity and exact restriction. Every reported
  final-coordinate endpoint now has a separately extracted exact path on the
  optimized face.
- `kernel_generating_series.py` checks every coordinate and verifies the full
  character identity

$$
N_n^{10}=Z_Q^{10}(L_n-L_{n-1})
$$

  exactly for every feasible prefix.
- `chamber_core.py` checks every extracted coordinate before its existing
  exact positivity and restriction verification.
- `chamber_witness.py` checks coordinates, positive and negative source
  variables, and binary activity variables. It verifies source transport
  equations, rigorous source and coordinate bounds, positivity and exact
  restriction for representative and enumerated witnesses.
- `restriction_semigroup.py` checks the objective and every packet
  multiplicity before its existing exact reconstruction test $Ax=m$.

## Remaining limitation

These changes provide exact certification of every reported **primal
witness** after it has been returned by GLPK. They do not turn GLPK's
floating-point branch-and-bound proof into an exact rational certificate of
global optimality or infeasibility.

Accordingly:

- achieved objective values and range endpoints have exact integer witnesses;
- positive feasibility claims have exact witnesses;
- claims that no better solution exists, that an enumeration is exhausted, or
  that a model is infeasible remain dependent on GLPK's solver status.

Future results requiring proof-grade negative MILP certificates should use an
exact independent obstruction, exhaustive bounded enumeration, or a solver
capable of emitting a checkable certificate. Existing algebraic obstruction
arguments, such as exact nondivisibility results, remain independent of this
limitation.

## Focused verification

The following paths passed after hardening:

```text
./bin/sage-run -m trajectory_kernel.trajectory_selection --max-level 7 --probe-next-level
./bin/sage-run -m trajectory_kernel.kernel_generating_series --max-level 2
./bin/sage-run -m trajectory_kernel.chamber_core --max-level 7
./bin/sage-run -m trajectory_kernel.chamber_witness --max-level 7 --first-level 7 --enumeration-cap 5
./bin/sage-run -m trajectory_kernel.restriction_semigroup --self-test --skip-normaliz
```

A synthetic integral packet-witness solve and the new shared numerical guard
also passed. No protected $SO(10)$ completion was imported by these tests.
