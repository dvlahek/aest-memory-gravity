#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results
python nl1c6d2c5/action_level_flrw_longitudinal_audit.py \
  --json-out results/nl1c6d2c5_action_level_flrw_longitudinal_audit.json \
  2>&1 | tee results/nl1c6d2c5_action_level_flrw_longitudinal_audit.log
