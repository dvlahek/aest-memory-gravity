#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results
if [[ ! -f results/nl1c6d2n_corrected_class_env.sh ]]; then
  echo "missing corrected CLASS environment; run bash nl1c6d2n/setup_corrected_class_local.sh first" >&2
  exit 2
fi
source results/nl1c6d2n_corrected_class_env.sh
python -u nl1c6d2c6ar1/stable_canonical_integrator.py \
  --json-out results/nl1c6d2c6ar1_stable_canonical_integrator.json \
  2>&1 | tee results/nl1c6d2c6ar1_stable_canonical_integrator.log
