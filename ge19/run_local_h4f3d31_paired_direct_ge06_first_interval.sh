#!/usr/bin/env bash
set -euo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
[[ "$(git branch --show-current)" == 'physics-first-gravitational-elasticity' ]] || { echo GE19_D31_WRONG_BRANCH; exit 4; }
[[ -f .venv/bin/activate ]] || { echo GE19_D31_MISSING_VENV; exit 5; }
source .venv/bin/activate
export PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$ROOT" OPENBLAS_NUM_THREADS="${OPENBLAS_NUM_THREADS:-1}"
mkdir -p results
P='results/ge19_h4f3d31_paired_direct_ge06_first_interval'
for f in "${P}.json" "${P}.npz" "${P}_FULL.log"; do
  [[ ! -e "$f" ]] || { echo "GE19_D31_REFUSE_OVERWRITE $f"; exit 6; }
done
python -u ge19/h4f3d31_paired_direct_ge06_first_interval_static_test.py
set +e
python -u -m ge19.h4f3d31_paired_direct_ge06_first_interval \
  --results-dir "$ROOT/results" --json-out "$ROOT/${P}.json" --npz-out "$ROOT/${P}.npz" \
  2>&1 | tee "${P}_FULL.log"
rc=${PIPESTATUS[0]}
set -e
echo "EXIT=$rc"
if [[ "$rc" -ne 0 ]]; then echo "GE19_D31_EXECUTION_FAIL rc=$rc"; exit "$rc"; fi
python - "$ROOT/${P}.json" "$ROOT/${P}.npz" <<'PYRUN'
import json,sys,numpy as np
j=json.load(open(sys.argv[1]))
assert j['classification']=='GE19_D31_PAIRED_DIRECT_GE06_FIRST_INTERVAL_DIAGNOSTIC_COMPLETE_PARENTS_UNCERTIFIED'
assert not j['Z20_certified'] and not j['Z21_certified'] and not j['lensing_licensed']
assert j['original_D22A_science_FAIL_immutable'] and j['original_D27_triplet_FAIL_immutable']
assert j['original_shift_gate_unchanged'] and j['nonanalytic_StageE_Y_retained']
assert j['boundary_rule_unchanged_candidate_momenta_reprojected'] and not j['production_H3F_source_modified']
assert [(c['mode'],c['beta']) for c in j['per_case']]==[(14,0.1),(1,1.0),(40,0.1)]
with np.load(sys.argv[2],allow_pickle=False) as z:
 assert len(z.files)==24 and all(np.isfinite(z[k]).all() for k in z.files)
print('GE19_D31_RESULT_AND_UNCERTIFIED_SCOPE_PASS',flush=True)
PYRUN
sha256sum "${P}.json" "${P}.npz" "${P}_FULL.log"
echo GE19_D31_EXECUTION_COMPLETE
