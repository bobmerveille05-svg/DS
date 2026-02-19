# Vérification d'alignement: Github-Copilot-Atlas + spec-kit

Ce document vérifie que le template capture la logique combinée de:
- **Github-Copilot-Atlas**: orchestration multi-agents en phases.
- **spec-kit**: artefacts structurés `spec.md` → `plan.md` → `tasks.md`.

## Hypothèses de référence

> Réseau GitHub indisponible dans l'environnement d'exécution (HTTP 403), donc cette vérification s'appuie sur:
> 1) les conventions déjà présentes dans ce dépôt,
> 2) les structures `kitty-specs/...` existantes,
> 3) le workflow demandé dans la spécification utilisateur.

## Mapping logique validé

1. **Pipeline artefacts**
   - spec-kit: `spec.md`, `plan.md`, `tasks.md`
   - template: mêmes fichiers sous `.specify/specs/<feature>/`

2. **Pont Atlas**
   - Conversion `tasks.md` → `atlas-phases.md` via `.specify/scripts/spec-to-atlas.py`.
   - Routage agent par type de tâche (frontend/backend) + détection `[P]` pour parallélisme.

3. **Orchestration agents**
   - Prompt `Atlas.agent.md` lit constitution + artefacts de feature avant action.
   - Prompt `Prometheus.agent.md` impose validation specs en amont.

4. **Garde-fous d'exécution**
   - Workflow CI `validate-specs.yml` vérifie la présence des artefacts requis.
   - Script de vérification locale `scripts/verify-template-alignment.sh` (ajouté) valide la cohérence template.

## Écarts corrigés

- Support des tâches spec-kit plus variées (WPs, IDs `T001`, bullets checkbox, listes numérotées).
- Ajout d'une commande de vérification rapide pour éviter les dérives de structure.

## Commandes de contrôle

```bash
./scripts/verify-template-alignment.sh
python3 .specify/scripts/spec-to-atlas.py <feature-id>
```
