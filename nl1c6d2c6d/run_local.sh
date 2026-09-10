#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results

if [[ ! -f results/c3_r5_class_env.sh ]]; then
  echo "missing zero-safe CLASS environment; run nl1c6d2c6c_r5/setup_zero_safe_class.sh first" >&2
  exit 2
fi
source results/c3_r5_class_env.sh

python -u nl1c6d2c6d/finite_positive_eta_retained.py \
  --json-out results/nl1c6d2c6d_finite_positive_eta_retained.json \
  2>&1 | tee results/nl1c6d2c6d_finite_positive_eta_retained.log
