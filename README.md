# 🚀 Spec-Atlas Template

> Spec-Driven Development + Multi-Agent Execution

## Quick Start

```bash
# 1. Use this template
gh repo create my-project --template your-username/spec-atlas-template
cd my-project

# 2. Bootstrap
./scripts/bootstrap.sh

# 3. Spec Phase (terminal)
specify init . --here --ai copilot

# 4. Start specifying
/speckit.constitution
/speckit.specify "..."
/speckit.plan "..."
/speckit.tasks

# 5. Execute (VS Code)
@Prometheus validate and convert specs to Atlas phases
@Atlas implement
```

## Workflow
Spec → Plan → Tasks → Atlas Phases → Implementation → Review → Commit


## Validation rapide

```bash
./scripts/verify-template-alignment.sh
```
