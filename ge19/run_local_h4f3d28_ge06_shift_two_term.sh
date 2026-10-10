#!/usr/bin/env bash
set -euo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
[[ "$(git branch --show-current)" == 'physics-first-gravitational-elasticity' ]] || { echo GE19_D28_WRONG_BRANCH; exit 4; }
[[ -f .venv/bin/activate ]] || { echo GE19_D28_MISSING_VENV; exit 5; }
source .venv/bin/activate
export PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$ROOT" OPENBLAS_NUM_THREADS="${OPENBLAS_NUM_THREADS:-1}"
python -u ge19/h4f3d28_ge06_shift_two_term_static_test.py
mkdir -p results
P="results/ge19_h4f3d28_ge06_shift_two_term_provenance"
for f in "${P}.json" "${P}.npz" "${P}_FULL.log"; do
  [[ ! -e "$f" ]] || { echo "GE19_D28_REFUSE_OVERWRITE $f"; exit 6; }
done
set +e
python -u -m ge19.h4f3d28_ge06_shift_two_term_provenance \
  --results-dir "$ROOT/results" --json-out "$ROOT/${P}.json" --npz-out "$ROOT/${P}.npz" \
  2>&1 | tee "${P}_FULL.log"
rc=${PIPESTATUS[0]}
set -e
echo "EXIT=$rc"
if [[ "$rc" -ne 0 ]]; then echo "GE19_D28_EXECUTION_FAIL rc=$rc"; exit "$rc"; fi
python - "$ROOT/${P}.json" <<'PYRUN'
import json,sys
r=json.load(open(sys.argv[1]))
assert r['classification']=='GE19_D28_FROZEN_GE06_SHIFT_BF_GRADBX_DIAGNOSTIC_COMPLETE_PARENTS_UNCERTIFIED'
assert len(r['per_case'])==3
assert r['D27R2_original_selected_triplet_FAIL_immutable'] and r['D22A_science_FAIL_immutable']
assert not r['Z20_certified'] and not r['Z21_certified'] and not r['full_H4_Ward_certified']
print('GE19_D28_RESULT_AND_SCIENCE_SCOPE_PASS',flush=True)
PYRUN
sha256sum "${P}.json" "${P}.npz" "${P}_FULL.log"
echo GE19_D28_EXECUTION_COMPLETE
