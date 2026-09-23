# Archived Working Reports

This directory preserves superseded project reports for provenance. None of
these documents is authoritative. The current project position is maintained in
the root-level `STATUS.md` and the focused reports it names.

## Plethystic reports

| Archived report | Reason archived | Authoritative replacement |
| --- | --- | --- |
| `superseded_reports/PL_Report_1.md` | Correct coefficient computation, unsupported generator/relation, on-shell and pure-spinor interpretations | `PLETHYSTIC_STATUS.md` |
| `superseded_reports/PL_Report_2.md` | Valid formal identity mixed with unsupported algebraic-variety and pure-spinor claims | `PLETHYSTIC_STATUS.md` |
| `superseded_reports/PL_Report_3.md` | Partial retraction, but retained unsupported syzygy/telescoping claims and predates repaired M4 | `PLETHYSTIC_STATUS.md`, `STATUS.md` |
| `superseded_reports/Direction3_Bars_IIIC_Report.md` | Valid III.C convolution mixed with speculative membrane, Howe-dual and syzygy interpretations | `PLETHYSTIC_STATUS.md`, `STATUS.md` |

## HFT uplift and branching reports

These are under `superseded_reports/HananyForcellaTroostUpliftReports/`.

| Archived report | Reason archived | Authoritative replacement |
| --- | --- | --- |
| `Direction1_M1M2_walkthrough.md` | Historical implementation walkthrough | `hft_so9.py`, `verify_hft_so9_against_baseline.py`, `STATUS.md` |
| `Direction1_M3M4_walkthrough.md` | Claimed a circular M4 reconstruction as a pass | `STATUS.md` |
| `Direction1_M3M4_ISSUE.md` | Valuable historical audit; implementation has since been repaired | `hft_so10_uplift.py`, `verify_hft_so10_against_baseline.py`, `STATUS.md` |
| `Direction1_SO10_Plethystic_Report.md` | Mixed valid M3 with invalid M4, telescoping, positivity and pure-spinor claims | `STATUS.md`, `PLETHYSTIC_STATUS.md` |
| `HFT_Bars_III_B_outstanding_problem.md` | Useful problem statement but incorrectly claimed that HFT already supplied positive cumulative lifts | `STATUS.md`, `FINITE_CROSS_SECTION_REPORT.md` |
| `Candidate_Set_Branching_Analysis.md` | Level-dependent 126/210 choice was presented as one cross-section | `FINITE_CROSS_SECTION_REPORT.md` |
| `Linear_Identities_Proof_of_Concept.md` | Candidate-section and negative-tail conclusions were baseline-dependent | `FINITE_CROSS_SECTION_REPORT.md`, `LEGACY_NEGATIVE_TAIL_AUDIT.md` |
| `StrategyA_Asymptotic_Domination_Report.md` | Missing-script data provenance and unsupported asymptotic proof | `LEGACY_NEGATIVE_TAIL_AUDIT.md` |
| `StrategyA_Inductive_Proof_Attempt.md` | Assumed a unique fixed lift and left the subleading induction open | `FINITE_CROSS_SECTION_REPORT.md`, `STATUS.md` |

## Preservation policy

Archived reports are not deleted or silently rewritten. Prominent correction
notices record the central reason each document was superseded. Numerical claims
that remain useful must be reproduced by a maintained script before being cited
as current evidence.
