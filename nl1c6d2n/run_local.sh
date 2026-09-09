#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results

python nl1c6d2n/exp_normalization_audit.py \
  --json-out results/nl1c6d2n_exp_normalization_audit.json \
  2>&1 | tee results/nl1c6d2n_exp_normalization_audit.log
