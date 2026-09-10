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
python -u nl1c6d2c6b/all27_physical_nonlinear_trajectories.py \
  --json-out results/nl1c6d2c6b_all27_physical_nonlinear_trajectories.json \
  2>&1 | tee results/nl1c6d2c6b_all27_physical_nonlinear_trajectories.log
