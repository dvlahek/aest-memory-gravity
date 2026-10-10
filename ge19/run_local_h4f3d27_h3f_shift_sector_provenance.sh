#!/usr/bin/env bash
set -euo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
[[ "$(git branch --show-current)" == "physics-first-gravitational-elasticity" ]] || { echo GE19_D27_WRONG_BRANCH; exit 4; }
[[ -f .venv/bin/activate ]] || { echo GE19_D27_VENV_MISSING; exit 5; }
source .venv/bin/activate
export PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$ROOT" OPENBLAS_NUM_THREADS="${OPENBLAS_NUM_THREADS:-1}"
python -u ge19/h4f3d27_h3f_shift_sector_provenance_static_test.py
mkdir -p results
P="results/ge19_h4f3d27_h3f_shift_sector_provenance"
for f in "${P}.json" "${P}.npz" "${P}_FULL.log"; do
  [[ ! -e "$f" ]] || { echo "GE19_D27_REFUSE_OVERWRITE $f"; exit 6; }
done
set +e
python -u -m ge19.h4f3d27_h3f_shift_sector_provenance \
  --results-dir "$ROOT/results" --json-out "$ROOT/${P}.json" --npz-out "$ROOT/${P}.npz" \
  2>&1 | tee "${P}_FULL.log"
rc=${PIPESTATUS[0]}
set -e
if [[ "$rc" -ne 0 ]]; then echo "GE19_D27_EXECUTION_FAIL rc=$rc"; exit "$rc"; fi
python - "$ROOT/${P}.json" <<'PY'
import json,sys
r=json.load(open(sys.argv[1]))
assert r['classification']=='GE19_D27_ORIGINAL_ACTION_H3F_SHIFT_SOURCE_SECTOR_PROVENANCE_DIAGNOSTIC_COMPLETE_PARENTS_UNCERTIFIED'
assert r['D22A_science_FAIL_immutable'] and not r['Z20_certified'] and not r['Z21_certified']
assert len(r['per_case'])==3
print('GE19_D27_RESULT_AND_SCOPE_PASS',flush=True)
PY
sha256sum "${P}.json" "${P}.npz" "${P}_FULL.log"
echo GE19_D27_EXECUTION_COMPLETE
