#!/usr/bin/env bash
set -euo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
[[ "$(git branch --show-current)" == 'physics-first-gravitational-elasticity' ]] || { echo GE19_D32_WRONG_BRANCH; exit 4; }
[[ -f .venv/bin/activate ]] || { echo GE19_D32_MISSING_VENV; exit 5; }
source .venv/bin/activate
export PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$ROOT" OPENBLAS_NUM_THREADS="${OPENBLAS_NUM_THREADS:-1}"
mkdir -p results
P='results/ge19_h4f3d32_independent_sector_first_interval'
for f in "${P}.json" "${P}.npz" "${P}_FULL.log"; do
  [[ ! -e "$f" ]] || { echo "GE19_D32_REFUSE_OVERWRITE $f"; exit 6; }
done
python -u ge19/h4f3d32_independent_sector_first_interval_static_test.py
set +e
python -u -m ge19.h4f3d32_independent_sector_first_interval \
  --results-dir "$ROOT/results" --json-out "$ROOT/${P}.json" --npz-out "$ROOT/${P}.npz" \
  2>&1 | tee "${P}_FULL.log"
rc=${PIPESTATUS[0]}
set -e
echo "EXIT=$rc"
if [[ "$rc" -ne 0 ]]; then echo "GE19_D32_EXECUTION_FAIL rc=$rc"; exit "$rc"; fi
python - "$ROOT/${P}.json" "$ROOT/${P}.npz" <<'PYRUN'
import sys,json,numpy as np
j=json.load(open(sys.argv[1]))
assert j['classification']=='GE19_D32_INDEPENDENT_SIGNED_GE06_GE07_LAMBDA_STAGEE_FIRST_INTERVAL_DIAGNOSTIC_COMPLETE_PARENTS_UNCERTIFIED'
assert j['D22A_science_FAIL_immutable'] and j['D31R1_parent_diagnostic_only']
assert j['original_shift_gate_unchanged'] and j['nonanalytic_StageE_Y_retained']
assert not j['Z11_certified'] and not j['Z20_certified'] and not j['Z21_certified'] and not j['lensing_licensed']
assert not j['production_H3F_source_modified'] and j['boundary_rule_unchanged_candidate_momenta_reprojected']
assert [(c['mode'],c['beta']) for c in j['per_case']]==[(14,0.1),(1,1.0),(40,0.1)]
assert all(len(c['comparisons'])==2 for c in j['per_case'])
with np.load(sys.argv[2],allow_pickle=False) as z:
 assert len(z.files)==15 and all(np.isfinite(z[k]).all() for k in z.files)
print('GE19_D32_RESULT_AND_UNCERTIFIED_SCOPE_PASS',flush=True)
PYRUN
sha256sum "${P}.json" "${P}.npz" "${P}_FULL.log"
echo GE19_D32_EXECUTION_COMPLETE
