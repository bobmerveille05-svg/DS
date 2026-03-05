# BMAD-Trading Method (Overview)

Principle:

No code before logic is proven on paper. No live deployment before statistical proof.

Pipeline:

Idea -> Spec -> Logic -> Code -> Test -> Proof -> Deploy/Reject

## Phases

Phase 1 - CAPTURE (Analyst)
- Output: STRATEGY-SPEC
- Gate: GATE-01 (Spec Complete)

Phase 2 - LOGIC (Quant)
- Output: LOGIC-MODEL
- Gate: GATE-02 (Logic Verified)

Phase 3 - CODE (Coder)
- Output: SOURCE-CODE (MT4/MT5/TradingView)
- Gate: GATE-03 (Code Review)

Phase 4 - TEST (Tester)
- Output: TEST-REPORT
- Gate: GATE-04 (Test Validated)

Phase 5 - PROOF (Auditor)
- Output: PROOF-CERTIFICATE
- Final decision: CERTIFIED / CONDITIONAL / REJECTED

## Gates

Gate definitions live in `bmad/data/gates.json`.

The CLI stores your gate answers in each strategy workspace at:
- `work/<strategy>/.bmad/state.json`

Rule:
- A gate is PASS only if 100% of required checklist items are true.
- If a gate fails, you must rollback and fix the previous phase artefact.

## Artefacts and IDs

The method relies on stable IDs to keep full traceability:

- Indicator IDs: IND-1, IND-2, ...
- Entry IDs: LONG-1.., SHORT-1..
- Filter IDs: FLT-1..
- Parameter IDs: P-01..
- Edge case IDs: CL-01..

Expected convention:
- STRATEGY-SPEC defines the IDs
- LOGIC-MODEL references them 1:1
- Code comments include the IDs (e.g. `// [LONG-1] ...`)
- Tests reference them (TU/TS/TF/TR/SC IDs)

The CLI command `python -m bmad audit` generates a simple presence matrix.
