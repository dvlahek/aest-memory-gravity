#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
if [[ -f .venv/bin/activate ]]; then source .venv/bin/activate; fi
export PYTHONUNBUFFERED=1
mkdir -p results
JSON=results/ge19_h4f3d25_first_interval_shift_substep_decision.json
NPZ=results/ge19_h4f3d25_first_interval_shift_substep_decision.npz
LOG=results/ge19_h4f3d25_first_interval_shift_substep_decision_FULL.log
if [[ -e "$JSON" || -e "$NPZ" || -e "$LOG" ]]; then
  echo "GE19_D25_OUTPUT_EXISTS_REFUSE_OVERWRITE"; exit 2
fi
set +e
python -u -m ge19.h4f3d25_first_interval_shift_substep_decision \
  --results-dir "$ROOT/results" --json-out "$ROOT/$JSON" --npz-out "$ROOT/$NPZ" \
  2>&1 | tee "$LOG"
RC=${PIPESTATUS[0]}
set -e
if [[ "$RC" -ne 0 ]]; then echo "GE19_D25_EXECUTION_FAIL rc=$RC"; exit "$RC"; fi
sha256sum "$JSON" "$NPZ" "$LOG"
echo "GE19_D25_EXECUTION_COMPLETE"
