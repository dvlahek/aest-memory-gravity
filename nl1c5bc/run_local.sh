#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ ! -f results/nl1c6d2n_corrected_class_env.sh ]]; then
  echo "missing results/nl1c6d2n_corrected_class_env.sh; run bash nl1c6d2n/setup_corrected_class_local.sh first" >&2
  exit 2
fi

source results/nl1c6d2n_corrected_class_env.sh

python nl1c5bc/corrected_baryon_source_freeze.py \
  --json-out results/nl1c5bc_corrected_baryon_source_freeze.json \
  --npz-out results/nl1c5bc_corrected_baryon_source_freeze.npz \
  2>&1 | tee results/nl1c5bc_corrected_baryon_source_freeze.log
