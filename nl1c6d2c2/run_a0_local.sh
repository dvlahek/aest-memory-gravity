#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results
python nl1c6d2c2/corrected_covariant_a0_structural_audit.py \
  --json-out results/nl1c6d2c2_corrected_covariant_a0_structural_audit.json \
  2>&1 | tee results/nl1c6d2c2_corrected_covariant_a0_structural_audit.log
