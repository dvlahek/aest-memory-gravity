#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p results
export PYTHONPATH="${PYTHONPATH:-}:$(pwd)"
python3 -u nl1c6d1/longitudinal_weakfield_reduction_audit.py \
  --json-out results/nl1c6d1a_longitudinal_weakfield_reduction_audit.json \
  | tee results/nl1c6d1a_longitudinal_weakfield_reduction_audit.log
