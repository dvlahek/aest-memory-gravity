#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results
python nl1c6d2c2/a1_derivative_preservation_audit.py \
  --json-out results/nl1c6d2c2_a1_derivative_preservation.json \
  2>&1 | tee results/nl1c6d2c2_a1_derivative_preservation.log
