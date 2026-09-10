#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results

if [[ ! -f results/nl1c6d2c6c_class_env.sh ]]; then
  echo "missing D2C6C corrected tau1 CLASS environment; run setup_corrected_class_tau1.sh first" >&2
  exit 2
fi
source results/nl1c6d2c6c_class_env.sh

python -u nl1c6d2c6c/build_linear_reference.py \
  --out results/nl1c6d2c6c_linear_tangent_reference.npz \
  --force-out results/nl1c6d2c6c_eta0_force39.dat \
  --meta-out results/nl1c6d2c6c_linear_tangent_reference.json \
  2>&1 | tee results/nl1c6d2c6c_linear_reference.log

python -u nl1c6d2c6c/r3_modewise_full_prehistory.py \
  --linear-reference results/nl1c6d2c6c_linear_tangent_reference.npz \
  --json-out results/nl1c6d2c6c_eta0_nonlinear_memory_tangent.json \
  2>&1 | tee results/nl1c6d2c6c_eta0_nonlinear_memory_tangent.log
