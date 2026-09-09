#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

mkdir -p results
python3 -u nl1c6d2c/completion_identity_audit.py \
  --json-out results/nl1c6d2c_completion_identity_audit.json \
  | tee results/nl1c6d2c_completion_identity_audit.log
