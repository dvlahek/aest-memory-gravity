#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results
python nl1c6d2c4r1/derivative_control_repair.py \
  --json-out results/nl1c6d2c4r1_derivative_control_repair.json \
  2>&1 | tee results/nl1c6d2c4r1_derivative_control_repair.log
