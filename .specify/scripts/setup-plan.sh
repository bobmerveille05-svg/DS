#!/usr/bin/env bash
set -euo pipefail

FEATURE_ID="${1:?Usage: $0 <feature-id>}"
SPEC_DIR=".specify/specs/${FEATURE_ID}"
mkdir -p "$SPEC_DIR"
if [ ! -f "$SPEC_DIR/plan.md" ]; then
  cp .specify/templates/plan-template.md "$SPEC_DIR/plan.md"
fi
echo "✅ Plan ready: $SPEC_DIR/plan.md"
