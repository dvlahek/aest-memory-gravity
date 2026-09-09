#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
mkdir -p results

export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1

python3 -u nl1c6d2b/flrw_source_gravity_coupling_audit.py \
  --d2a-json results/nl1c6d2a_baryon_matter_sector_audit.json \
  --d2a-npz results/nl1c6d2a_baryon_matter_sector.npz \
  --json-out results/nl1c6d2b_flrw_source_gravity_coupling_audit.json \
  | tee results/nl1c6d2b_flrw_source_gravity_coupling_audit.log
