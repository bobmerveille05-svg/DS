#!/usr/bin/env bash
set -euo pipefail

echo "🔎 Verifying Spec-Atlas template alignment..."

required_files=(
  "AGENTS.md"
  "README.md"
  ".specify/memory/constitution.md"
  ".specify/scripts/spec-to-atlas.py"
  ".specify/templates/spec-template.md"
  ".specify/templates/plan-template.md"
  ".specify/templates/tasks-template.md"
  ".specify/templates/atlas-phases-template.md"
  ".vscode/prompts/Atlas.agent.md"
  ".vscode/prompts/Prometheus.agent.md"
  ".github/workflows/validate-specs.yml"
)

for path in "${required_files[@]}"; do
  [[ -f "$path" ]] || { echo "❌ Missing required file: $path"; exit 1; }
  echo "✅ $path"
done

if ! rg -n "spec\.md|plan\.md|tasks\.md" .github/workflows/validate-specs.yml >/dev/null; then
  echo "❌ validate-specs workflow does not enforce core spec-kit artifacts"
  exit 1
fi

echo "✅ Workflow checks required spec-kit artifacts"

if ! rg -n "constitution\.md|atlas-phases\.md" .vscode/prompts/Atlas.agent.md >/dev/null; then
  echo "❌ Atlas prompt does not enforce constitution + atlas-phases initialization"
  exit 1
fi

echo "✅ Atlas prompt enforces constitution + phase plan reading"

echo "🎉 Template alignment checks passed"
