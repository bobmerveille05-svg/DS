# Atlas Phases — {{FEATURE_NAME}}

## Source Artifacts
- Spec: `.specify/specs/{{FEATURE_ID}}/spec.md`
- Plan: `.specify/specs/{{FEATURE_ID}}/plan.md`
- Tasks: `.specify/specs/{{FEATURE_ID}}/tasks.md`
- Constitution: `.specify/memory/constitution.md`

## Phases

### Phase 1: {{PHASE_NAME}}
**Parallélisable:** Non (foundation)
**Agent principal:** Sisyphus-subagent
**Durée estimée:** ~

#### Tasks
- [ ] 1.1 {{TASK}} → `{{FILE_PATH}}`
- [ ] 1.2 {{TASK}} → `{{FILE_PATH}}`

#### Tests TDD requis
- [ ] Test: {{TEST_DESCRIPTION}}

#### Validation
- Agent: Code-Review-subagent
- Critères: Constitution § {{SECTION}}

---

### Phase 2: {{PHASE_NAME}} [PARALLEL]
**Parallélisable:** Oui
**Agents:** Sisyphus-subagent + Frontend-Engineer-subagent

#### Sisyphus Tasks
- [ ] 2.1 {{TASK}} → `{{FILE_PATH}}`

#### Frontend-Engineer Tasks
- [ ] 2.2 {{TASK}} → `{{FILE_PATH}}`

#### Validation
- Agent: Code-Review-subagent x2 (parallel)

---

## Commit Strategy
- Commit après chaque phase approuvée
- Format: `feat({{FEATURE_ID}}): {{PHASE_NAME}}`
