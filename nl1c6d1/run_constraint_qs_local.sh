#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
export PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}"
mkdir -p results
python3 -u nl1c6d1/constraint_qs_regression.py \
  --input-npz input/nl1c5b/results/nl1c5b_baryon_source_freeze.npz \
  --input-zip-sha256 0ab60cbc32210ad3fb75c881f91a9db11148280e9223ea644680ed8cdfbaa590 \
  --json-out results/nl1c6d1cde_constraint_qs_regression.json \
  | tee results/nl1c6d1cde_constraint_qs_regression.log
