#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ ! -f results/nl1c6d2n_corrected_class_env.sh ]]; then
  echo "missing corrected CLASS environment; run nl1c6d2n/setup_corrected_class_local.sh first" >&2
  exit 2
fi
if [[ ! -f results/nl1c5bc_corrected_baryon_source_freeze.npz ]]; then
  echo "missing corrected source NPZ; run nl1c5bc/run_local.sh first" >&2
  exit 2
fi

source results/nl1c6d2n_corrected_class_env.sh
python nl1c6d2ac/corrected_baryon_matter_sector_audit.py \
  --input-npz results/nl1c5bc_corrected_baryon_source_freeze.npz \
  --json-out results/nl1c6d2ac_corrected_baryon_matter_sector_audit.json \
  --npz-out results/nl1c6d2ac_corrected_baryon_matter_sector.npz \
  2>&1 | tee results/nl1c6d2ac_corrected_baryon_matter_sector_audit.log
