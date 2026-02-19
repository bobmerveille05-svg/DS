#!/usr/bin/env bash
set -euo pipefail

FEATURE_ID="${1:?Usage: $0 <feature-id>}"
SPEC_DIR=".specify/specs/${FEATURE_ID}"
mkdir -p "$SPEC_DIR"
cp .specify/templates/spec-template.md "$SPEC_DIR/spec.md"
cp .specify/templates/plan-template.md "$SPEC_DIR/plan.md"
cp .specify/templates/tasks-template.md "$SPEC_DIR/tasks.md"
echo "✅ Created spec scaffolding at $SPEC_DIR"
