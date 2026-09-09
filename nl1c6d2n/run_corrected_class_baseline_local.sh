#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results

ENV_FILE="$ROOT/results/nl1c6d2n_corrected_class_env.sh"
if [[ ! -f "$ENV_FILE" ]]; then
  echo "Missing $ENV_FILE" >&2
  echo "Run: bash nl1c6d2n/setup_corrected_class_local.sh" >&2
  exit 2
fi

# shellcheck disable=SC1090
source "$ENV_FILE"

python nl1c6d2n/corrected_class_baseline.py \
  --json-out results/nl1c6d2n_corrected_class_baseline.json \
  --npz-out results/nl1c6d2n_corrected_class_baseline.npz \
  2>&1 | tee results/nl1c6d2n_corrected_class_baseline.log
