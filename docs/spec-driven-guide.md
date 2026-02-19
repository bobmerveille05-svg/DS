# Spec-Driven Guide

Ce template fusionne deux logiques:

1. **spec-kit** pour produire les artefacts de conception (`spec.md`, `plan.md`, `tasks.md`).
2. **Atlas** pour orchestrer l'exécution multi-agents par phase (`atlas-phases.md`).

## Flux recommandé

1. `specify init . --here --ai copilot`
2. `/speckit.specify`
3. `/speckit.plan`
4. `/speckit.tasks`
5. `python3 .specify/scripts/spec-to-atlas.py <feature-id>`
6. `@Prometheus validate`
7. `@Atlas implement`

## Vérification locale

```bash
./scripts/verify-template-alignment.sh
```
