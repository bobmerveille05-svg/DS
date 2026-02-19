#!/usr/bin/env bash
set -euo pipefail

require_spec_dir() {
  local dir="${1:-.specify/specs}"
  mkdir -p "$dir"
}
