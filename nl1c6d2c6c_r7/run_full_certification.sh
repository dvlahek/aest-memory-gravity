#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results

if [[ ! -f results/c3_r5_class_env.sh ]]; then
  echo "missing R5 zero-safe CLASS environment; run nl1c6d2c6c_r5/setup_zero_safe_class.sh first" >&2
  exit 2
fi
source results/c3_r5_class_env.sh

# Rebuild the corrected frozen-metric C3 reference from frozen code.  This is
# the only repaired input relative to the historical D2C6C-R3 all-27 run.
python -u nl1c6d2c6c_r6/build_frozen_metric_reference.py \
  --out results/nl1c6d2c6c_r7_linear_tangent_reference.npz \
  --meta-out results/nl1c6d2c6c_r7_linear_tangent_reference.json \
  --force-out results/nl1c6d2c6c_r7_eta0_force39.dat \
  2>&1 | tee results/nl1c6d2c6c_r7_reference.log

# Run the unchanged full D2C6C all-27 certification implementation, including
# all original C1-C8 gates, with only the corrected C3 reference substituted.
python -u nl1c6d2c6c/r3_modewise_full_prehistory.py \
  --linear-reference results/nl1c6d2c6c_r7_linear_tangent_reference.npz \
  --json-out results/nl1c6d2c6c_r7_full_certification.json \
  2>&1 | tee results/nl1c6d2c6c_r7_full_certification.log
