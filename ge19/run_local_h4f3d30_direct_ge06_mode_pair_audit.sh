#!/usr/bin/env bash
set -euo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
[[ "$(git branch --show-current)" == 'physics-first-gravitational-elasticity' ]] || { echo GE19_D30_WRONG_BRANCH; exit 4; }
[[ -f .venv/bin/activate ]] || { echo GE19_D30_MISSING_VENV; exit 5; }
source .venv/bin/activate
export PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$ROOT" OPENBLAS_NUM_THREADS="${OPENBLAS_NUM_THREADS:-1}"
python -u ge19/h4f3d30_direct_ge06_mode_pair_audit_static_test.py
mkdir -p results
P="results/ge19_h4f3d30_direct_ge06_mode_pair_audit"
for f in "${P}.json" "${P}.npz" "${P}_FULL.log"; do
  [[ ! -e "$f" ]] || { echo "GE19_D30_REFUSE_OVERWRITE $f"; exit 6; }
done
set +e
python -u -m ge19.h4f3d30_direct_ge06_mode_pair_audit \
  --results-dir "$ROOT/results" --json-out "$ROOT/${P}.json" --npz-out "$ROOT/${P}.npz" \
  2>&1 | tee "${P}_FULL.log"
rc=${PIPESTATUS[0]}
set -e
echo "EXIT=$rc"
if [[ "$rc" -ne 0 ]]; then echo "GE19_D30_EXECUTION_FAIL rc=$rc"; exit "$rc"; fi
python - "$ROOT/${P}.json" <<'PYRUN'
import json,sys
v=json.load(open(sys.argv[1]))
assert v['classification']=='GE19_D30_FROZEN_ORIGINAL_ACTION_DIRECT_SIGNED_GE06_MODE_PAIR_DIAGNOSTIC_COMPLETE_PARENTS_UNCERTIFIED'
assert v['D29R1_m40_replayed'] and v['original_H3F_source_replayed']
assert v['original_D22A_shift_science_FAIL_immutable'] and v['original_D27_selected_mode_triplet_FAIL_immutable']
assert not v['Z20_certified'] and not v['Z21_certified'] and not v['production_GE06_source_modified']
assert v['original_shift_gate_unchanged'] and v['no_mode_exclusion'] and not v['solver_rerun']
assert [d['mode'] for d in v['selected_modes']]==[1,14,23,30,35,40]
print('GE19_D30_RESULT_AND_SCOPE_PASS',flush=True)
PYRUN
sha256sum "${P}.json" "${P}.npz" "${P}_FULL.log"
echo GE19_D30_EXECUTION_COMPLETE
