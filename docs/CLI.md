# BMAD CLI

The CLI is a small helper to manage:
- current strategy workspace
- phase progression (1..5)
- gate checklists (GATE-01..GATE-04)
- audit (traceability presence check)
- export (zip)

Run everything from the project root (the directory that contains `.bmad/` after init).

## Commands

Initialize the project:

```bash
python -m bmad init
```

Start a strategy:

```bash
python -m bmad start --name "RSI EMA Trend" --version 1.0 --author "Alice"
```

Show status:

```bash
python -m bmad status
```

Gate checklist for the current phase:

```bash
python -m bmad gate
python -m bmad gate show
python -m bmad gate set G01-C01 true --note "LONG rules listed in spec section 3.1"
```

Advance / rollback phase:

```bash
python -m bmad phase next
python -m bmad rollback
```

Generate audit report (traceability matrix) in the current strategy folder:

```bash
python -m bmad audit
```

Export current strategy workspace to `exports/`:

```bash
python -m bmad export
```

Print an agent prompt (for use with your LLM):

```bash
python -m bmad agent orchestrator
python -m bmad agent analyst
```

Interactive shell (slash commands):

```bash
python -m bmad shell
```

Examples inside the shell:

```
/status
/gate
/phase next
/audit
/export
```
