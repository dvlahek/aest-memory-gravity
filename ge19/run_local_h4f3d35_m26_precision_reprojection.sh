#!/usr/bin/env bash
set -euo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
[[ "$(git branch --show-current)" == 'physics-first-gravitational-elasticity' ]] || { echo GE19_D35_WRONG_BRANCH; exit 4; }
[[ -f .venv/bin/activate ]] || { echo GE19_D35_MISSING_VENV; exit 5; }
source .venv/bin/activate
export PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$ROOT" OPENBLAS_NUM_THREADS="${OPENBLAS_NUM_THREADS:-1}"
mkdir -p results
P='results/ge19_h4f3d35_m26_precision_reprojection'
for f in "${P}.json" "${P}.npz" "${P}_FULL.log"; do
  [[ ! -e "$f" ]] || { echo "GE19_D35_REFUSE_OVERWRITE $f"; exit 6; }
done
python -u ge19/h4f3d35_m26_precision_reprojection_static_test.py
set +e
python -u -m ge19.h4f3d35_m26_precision_reprojection \
  --results-dir "$ROOT/results" --json-out "$ROOT/${P}.json" --npz-out "$ROOT/${P}.npz" \
  2>&1 | tee "${P}_FULL.log"
rc=${PIPESTATUS[0]}
set -e
echo "EXIT=$rc"
if [[ "$rc" -ne 0 ]]; then echo "GE19_D35_EXECUTION_FAIL rc=$rc"; exit "$rc"; fi
python - "$ROOT/${P}.json" "$ROOT/${P}.npz" <<'PYRUN'
import json,sys,numpy as np
j=json.load(open(sys.argv[1]))
assert j['D34_original_m26_boundary_FAIL_immutable'] and j['D34R1_original_m26_three_boundary_FAIL_immutable']
assert j['D34R1_234_observed_endpoints_SHA_frozen']
assert j['original_shift_gate_unchanged'] and j['nonanalytic_StageE_Y_retained']
assert j['m0_source_retained_separately'] and j['all_modes_retained']
assert j['production_H3F_source_modified'] is False and j['original_action_modified'] is False
assert j['H3_full_window_solve_performed'] is False and not any(j[k] for k in ('Z11_certified','Z20_certified','Z21_certified','lensing_licensed'))
assert len(j['m26_per_beta'])==3 and j['D35_new_endpoint_count']+j['D35_unevaluated_endpoint_count']==6
assert j['D35_all_240_endpoint_values_evaluated']==(j['D35_new_endpoint_count']==6)
if j['D35_new_endpoint_count']!=6:
    assert j['D35_all_240_first_interval_shift_gates_pass'] is None and j['D35_shift_gate_fail_count'] is None
with np.load(sys.argv[2],allow_pickle=False) as z:
    assert z['m26_original_y0_by_beta_8'].shape==(3,8)
    assert z['m26_candidate_y1_by_beta_substep_8'].shape==(3,2,8)
    assert np.count_nonzero(z['m26_candidate_y1_valid_by_beta_substep'])==j['D35_new_endpoint_count']
    assert all(np.isfinite(z[k]).all() for k in z.files)
print('GE19_D35_RESULT_AND_ORIGINAL_FAILURE_SCOPE_PASS',flush=True)
print('GE19_D35_NEW_ENDPOINTS',j['D35_new_endpoint_count'],
      'UNOBSERVED_ENDPOINTS',j['D35_unevaluated_endpoint_count'],
      'OBSERVED_SHIFT_GATE_FAILS',j['D35_observed_shift_gate_fail_count'],flush=True)
PYRUN
sha256sum "${P}.json" "${P}.npz" "${P}_FULL.log"
echo GE19_D35_EXECUTION_COMPLETE
