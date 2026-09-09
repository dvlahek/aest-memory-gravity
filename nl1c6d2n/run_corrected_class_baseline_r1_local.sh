#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results
source results/nl1c6d2n_corrected_class_env.sh
python nl1c6d2n/corrected_class_baseline_r1.py \
  --json-out results/nl1c6d2n_corrected_class_baseline_r1.json \
  --npz-out results/nl1c6d2n_corrected_class_baseline_r1.npz \
  2>&1 | tee results/nl1c6d2n_corrected_class_baseline_r1.log
