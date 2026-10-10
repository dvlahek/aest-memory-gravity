#!/usr/bin/env bash
set -euo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
[[ "$(git branch --show-current)" == 'physics-first-gravitational-elasticity' ]] || { echo GE19_D29R1_WRONG_BRANCH; exit 4; }
[[ -f .venv/bin/activate ]] || { echo GE19_D29R1_MISSING_VENV; exit 5; }
source .venv/bin/activate
export PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$ROOT" OPENBLAS_NUM_THREADS="${OPENBLAS_NUM_THREADS:-1}"
python -u ge19/h4f3d29r1_analytic_quadratic_support_static_test.py
mkdir -p results
P="results/ge19_h4f3d29r1_analytic_quadratic_support"
for f in "${P}.json" "${P}.npz" "${P}_FULL.log"; do
  [[ ! -e "$f" ]] || { echo "GE19_D29R1_REFUSE_OVERWRITE $f"; exit 6; }
done
set +e
python -u -m ge19.h4f3d29r1_analytic_quadratic_support \
  --results-dir "$ROOT/results" --json-out "$ROOT/${P}.json" --npz-out "$ROOT/${P}.npz" \
  2>&1 | tee "${P}_FULL.log"
rc=${PIPESTATUS[0]}
set -e
echo "EXIT=$rc"
if [[ "$rc" -ne 0 ]]; then echo "GE19_D29R1_EXECUTION_FAIL rc=$rc"; exit "$rc"; fi
python - "$ROOT/${P}.json" <<'PYRUN'
import json,sys
v=json.load(open(sys.argv[1]))
assert v['classification']=='GE19_D29R1_ORIGINAL_ACTION_QUADRATIC_HARMONIC_SELECTION_AND_M40_DIRECT_REPLAY_DIAGNOSTIC_COMPLETE_PARENTS_UNCERTIFIED'
assert v['D29_original_43_character_SHA_lock_FAIL_immutable']
assert len(v['per_case'])==3 and not v['Z20_certified'] and not v['Z21_certified']
assert v['D22A_original_shift_FAIL_immutable'] and v['Y_nonanalytic_source_not_removed']
assert v['original_shift_threshold_unchanged'] and v['no_mode_exclusion']
print('GE19_D29R1_RESULT_AND_SCOPE_PASS',flush=True)
PYRUN
sha256sum "${P}.json" "${P}.npz" "${P}_FULL.log"
echo GE19_D29R1_EXECUTION_COMPLETE
