#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results
python nl1c6d2c4/derivative_bounded_completion_identity_audit.py \
  --json-out results/nl1c6d2c4_derivative_bounded_completion_identity.json \
  2>&1 | tee results/nl1c6d2c4_derivative_bounded_completion_identity.log
