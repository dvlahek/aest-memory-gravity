#!/usr/bin/env bash
set -euo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
[[ "$(git branch --show-current)" == 'physics-first-gravitational-elasticity' ]] || { echo GE19_D36_WRONG_BRANCH; exit 4; }
[[ -f .venv/bin/activate ]] || { echo GE19_D36_MISSING_VENV; exit 5; }
source .venv/bin/activate
export PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$ROOT" OPENBLAS_NUM_THREADS="${OPENBLAS_NUM_THREADS:-1}"
mkdir -p results
P='results/ge19_h4f3d36_second_interval_continuation'
for f in "${P}.json" "${P}.npz" "${P}_FULL.log"; do
  [[ ! -e "$f" ]] || { echo "GE19_D36_REFUSE_OVERWRITE $f"; exit 6; }
done
python -u ge19/h4f3d36_second_interval_continuation_static_test.py
set +e
python -u -m ge19.h4f3d36_second_interval_continuation \
  --results-dir "$ROOT/results" --json-out "$ROOT/${P}.json" --npz-out "$ROOT/${P}.npz" \
  2>&1 | tee "${P}_FULL.log"
rc=${PIPESTATUS[0]}
set -e
echo "EXIT=$rc"
if [[ "$rc" -ne 0 ]]; then echo "GE19_D36_EXECUTION_FAIL rc=$rc"; exit "$rc"; fi
python - "$ROOT/${P}.json" "$ROOT/${P}.npz" <<'PYRUN'
import json,sys,numpy as np
j=json.load(open(sys.argv[1]))
assert j['D35_first_interval_parent_sha_frozen'] and j['D35_all_240_first_interval_original_shift_gates_pass']
assert j['D34_D34R1_original_m26_boundary_FAIL_immutable'] and j['D35_m26_posthoc_momentum_representation_not_original_bitwise']
assert j['original_action_modified'] is False and j['production_H3F_source_modified'] is False
assert j['original_shift_gate_unchanged'] and j['nonanalytic_StageE_Y_retained'] and j['m0_source_retained_separately']
assert j['no_reprojection_at_second_interval_start']
assert not any(j[v] for v in ('H3_full_window_solve_performed','Z11_certified','Z20_certified','Z21_certified','lensing_licensed'))
assert j['expected_endpoint_count']==240 and j['evaluated_endpoint_count']+j['unevaluated_endpoint_count']==240
assert j['observed_shift_gate_fail_count']==len(j['observed_shift_gate_failures'])
if not j['all_endpoints_evaluated']:
    assert j['all_original_shift_gates_pass'] is None and j['shift_gate_fail_count'] is None
else:
    assert j['all_original_shift_gates_pass']==(j['shift_gate_fail_count']==0)
with np.load(sys.argv[2],allow_pickle=False) as z:
    assert z['first_interval_x1_valid'].shape==(40,3,2) and np.all(z['first_interval_x1_valid'])
    assert z['second_interval_x2_valid'].shape==(40,3,2)
    assert int(z['second_interval_x2_valid'].sum())==j['evaluated_endpoint_count']
    assert np.isfinite(z['second_interval_x2_8']).all()
    for k in ('second_interval_relative_shift','second_interval_absolute_shift','second_interval_Radau_backward'):
        assert np.isfinite(z[k][z['second_interval_x2_valid']]).all()
        assert np.isnan(z[k][~z['second_interval_x2_valid']]).all()
print('GE19_D36_RESULT_AND_UNCERTIFIED_GATE_SCOPE_PASS',flush=True)
print('GE19_D36_EVALUATED',j['evaluated_endpoint_count'],'UNEVALUATED',j['unevaluated_endpoint_count'],
      'OBSERVED_GATE_FAILS',j['observed_shift_gate_fail_count'],flush=True)
PYRUN
sha256sum "${P}.json" "${P}.npz" "${P}_FULL.log"
echo GE19_D36_EXECUTION_COMPLETE
