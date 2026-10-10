#!/usr/bin/env bash
set -euo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
[[ "$(git branch --show-current)" == 'physics-first-gravitational-elasticity' ]] || { echo GE19_D38_WRONG_BRANCH; exit 4; }
[[ -f .venv/bin/activate ]] || { echo GE19_D38_MISSING_VENV; exit 5; }
source .venv/bin/activate
export PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$ROOT" OPENBLAS_NUM_THREADS="${OPENBLAS_NUM_THREADS:-1}"
mkdir -p results
P='results/ge19_h4f3d38_x16_x32_original_action_continuation'
for f in "${P}.json" "${P}.npz" "${P}_FULL.log"; do
  [[ ! -e "$f" ]] || { echo "GE19_D38_REFUSE_OVERWRITE $f"; exit 6; }
done
python -u ge19/h4f3d38_x16_x32_original_action_continuation_static_test.py
set +e
python -u -m ge19.h4f3d38_x16_x32_original_action_continuation \
  --results-dir "$ROOT/results" --json-out "$ROOT/${P}.json" --npz-out "$ROOT/${P}.npz" \
  2>&1 | tee "${P}_FULL.log"
rc=${PIPESTATUS[0]}
set -e
echo "EXIT=$rc"
if [[ "$rc" -ne 0 ]]; then echo "GE19_D38_EXECUTION_FAIL rc=$rc"; exit "$rc"; fi
python - "$ROOT/${P}.json" "$ROOT/${P}.npz" <<'PYRUN'
import json,sys,numpy as np
j=json.load(open(sys.argv[1]))
assert j['D36_240_second_interval_gate_pass_SHA_frozen'] and j['D37_3360_prefix_gate_pass_SHA_frozen']
assert j['D35_m26_posthoc_momentum_representation_not_original_bitwise']
assert j['D22A_original_science_FAIL_immutable'] and j['D34_D34R1_original_m26_boundary_FAIL_immutable']
assert not j['original_action_modified'] and not j['production_H3F_source_modified']
assert j['original_shift_gate_unchanged'] and j['nonanalytic_StageE_Y_retained'] and j['m0_source_retained_separately']
assert j['no_reprojection_at_x2_or_later_knots'] and j['no_reprojection_at_x16_or_later_knots']
assert not any(j[v] for v in ('H3_full_window_solve_performed','Z11_certified','Z20_certified','Z21_certified','lensing_licensed'))
assert len(j['interval_summaries'])==16 and j['expected_new_endpoint_count']==3840
assert j['evaluated_new_endpoint_count']+j['unevaluated_new_endpoint_count']==3840
assert len(j['numerical_or_blocked_endpoint_errors'])==j['unevaluated_new_endpoint_count']
assert len(j['observed_original_shift_gate_failures'])==j['observed_original_shift_gate_fail_count']
if not j['all_new_endpoints_evaluated']:
    assert j['all_original_shift_gates_pass'] is None
else:
    assert j['all_original_shift_gates_pass']==(j['observed_original_shift_gate_fail_count']==0)
with np.load(sys.argv[2],allow_pickle=False) as z:
    assert z['candidate_C_state_8_by_node_mode_beta_substep'].shape==(17,40,3,2,8)
    assert np.array_equal(z['clock_node_indices'],np.arange(16,33))
    v=z['candidate_C_state_numerically_evaluated'];p=z['candidate_C_shift_original_gate_pass']
    assert v.shape==(17,40,3,2) and v[0].all() and p[0].all()
    assert int(v[1:].sum())==j['evaluated_new_endpoint_count'] and np.all(~p[~v])
    assert np.isfinite(z['candidate_C_state_8_by_node_mode_beta_substep']).all()
    for key in ('candidate_C_shift_relative_backward','candidate_C_shift_absolute_residual','candidate_C_Radau_backward_report_only'):
        a=z[key];assert np.isfinite(a[v]).all() and np.isnan(a[~v]).all()
    assert np.array_equal(p[v],z['candidate_C_shift_relative_backward'][v]<=1e-6)
print('GE19_D38_RESULT_AND_UNCERTIFIED_X16_X32_GATE_SCOPE_PASS',flush=True)
print('GE19_D38_EVALUATED',j['evaluated_new_endpoint_count'],'UNEVALUATED',j['unevaluated_new_endpoint_count'],
      'OBSERVED_GATE_FAILS',j['observed_original_shift_gate_fail_count'],flush=True)
PYRUN
sha256sum "${P}.json" "${P}.npz" "${P}_FULL.log"
echo GE19_D38_EXECUTION_COMPLETE
