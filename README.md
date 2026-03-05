# DS

This repo includes:
- `DS/` - existing project content
- `bmad-trading` - BMAD-Trading Method scaffold + CLI (command: `bmad`)

## BMAD-Trading Method (Scaffold + CLI)

This tool helps run the BMAD-Trading pipeline:

Idea -> Spec -> Logic -> Code -> Test -> Proof

It provides:
- Templates for each mandatory artefact (Phase 1..5)
- Gate checklists (GATE-01..GATE-04)
- Agent prompts (Orchestrator, Analyst, Quant, Coder, Tester, Auditor)
- A small Python CLI to track phase/gate status and export artefacts

All docs/templates are kept ASCII-only by default.

## Install (pip)

From this repo (editable, recommended during development):

```bash
python -m pip install -U pip setuptools wheel
python -m pip install -e .
```

After that, you can use either `bmad ...` or `python -m bmad ...`.

Python requirement: 3.10+

## Quickstart

1) Initialize the project:

```bash
bmad init
```

2) Start a new strategy workspace:

```bash
bmad start --name "My Strategy" --version 0.1 --author "Me"
```

This creates a folder under `work/` with:
- `artefacts/STRATEGY-SPEC-...md`
- `artefacts/LOGIC-MODEL-...md`
- `artefacts/SOURCE-CODE-.../*.mq4|*.mq5|*.pine`
- `artefacts/TEST-REPORT-...md`
- `artefacts/PROOF-CERTIFICATE-...md`

3) Fill the Phase 1 spec, then run the gate checklist:

```bash
bmad gate
bmad phase next
```

4) Repeat for Phase 2..4, then generate audit/export:

```bash
bmad audit
bmad export
```

## Slash-command style (optional)

If you want to mimic the method's slash commands, use:

```bash
bmad shell
```

Then type `/start`, `/status`, `/gate`, `/rollback`, `/audit`, `/export`, etc.

## Files

- `docs/CLI.md` - CLI usage
- `docs/METHOD.md` - method overview (phases, gates, artefacts)
- `prompts/*.md` - agent prompts
- `templates/*.template.md` - artefact templates
- `templates/code/*` - code skeleton templates
- `bmad/` - CLI implementation
