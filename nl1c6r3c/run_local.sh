#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ ! -f results/nl1c5bc_corrected_baryon_source_freeze.npz ]]; then
  echo "missing corrected source NPZ; run nl1c5bc/run_local.sh first" >&2
  exit 2
fi

python nl1c6r3c/confirm_corrected_blocking_snapshot.py \
  --input-npz results/nl1c5bc_corrected_baryon_source_freeze.npz \
  --json-out results/nl1c6r3c_corrected_blocking_snapshot.json \
  2>&1 | tee results/nl1c6r3c_corrected_blocking_snapshot.log
