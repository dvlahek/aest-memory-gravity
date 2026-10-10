#!/usr/bin/env bash
set -euo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
[[ "$(git branch --show-current)" == 'physics-first-gravitational-elasticity' ]] || { echo GE19_D34R1_WRONG_BRANCH; exit 4; }
[[ -f .venv/bin/activate ]] || { echo GE19_D34R1_MISSING_VENV; exit 5; }
source .venv/bin/activate
export PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$ROOT" OPENBLAS_NUM_THREADS="${OPENBLAS_NUM_THREADS:-1}"
mkdir -p results
P='results/ge19_h4f3d34r1_boundary_failure_cohort'
for f in "${P}.json" "${P}.npz" "${P}_FULL.log"; do
  [[ ! -e "$f" ]] || { echo "GE19_D34R1_REFUSE_OVERWRITE $f"; exit 6; }
done
python -u ge19/h4f3d34r1_boundary_failure_cohort_static_test.py
set +e
python -u -m ge19.h4f3d34r1_boundary_failure_cohort \
  --results-dir "$ROOT/results" --json-out "$ROOT/${P}.json" --npz-out "$ROOT/${P}.npz" \
  2>&1 | tee "${P}_FULL.log"
rc=${PIPESTATUS[0]}
set -e
echo "EXIT=$rc"
if [[ "$rc" -ne 0 ]]; then echo "GE19_D34R1_EXECUTION_FAIL rc=$rc"; exit "$rc"; fi
python - "$ROOT/${P}.json" "$ROOT/${P}.npz" <<'PYRUN'
import json,sys,numpy as np
j=json.load(open(sys.argv[1]))
assert j['all_case_count']==240 and j['boundary_attempt_count']==120
assert len(j['all_initial_boundary_attempts'])==120
assert j['evaluated_shift_case_count']+j['unevaluated_shift_case_count']==240
assert j['initial_boundary_failure_count']*2==j['unevaluated_shift_case_count']
assert j['missing_endpoint_values_are_not_science_passes']
assert j['D34_original_m26_boundary_FAIL_immutable'] and j['original_shift_gate_unchanged']
assert j['m0_source_retained_separate_from_reduced_k0_evolution'] and j['nonanalytic_StageE_Y_retained']
assert j['H3_full_window_solve_performed'] is False
assert not any(j[k] for k in ('Z11_certified','Z20_certified','Z21_certified','lensing_licensed','production_H3F_source_modified'))
if j['initial_boundary_failure_count']:
 assert j['shift_gate_fail_count'] is None and j['all_first_interval_original_shift_gates_pass'] is None
 assert j['classification']=='GE19_D34R1_BOUNDARY_COHORT_INCOMPLETE_SHIFT_DIAGNOSTIC_PARENTS_UNCERTIFIED' or j['classification']=='GE19_D34R1_FROZEN_D33_CONTROL_REPLAY_UNRESOLVED_BOUNDARY_DIAGNOSTIC'
else:
 assert j['all_240_shift_cases_evaluated'] and j['shift_gate_fail_count'] is not None
with np.load(sys.argv[2],allow_pickle=False) as z:
 assert z['candidate_C_y1_by_mode_beta_substep_8'].shape==(40,3,2,8)
 assert z['candidate_C_y1_valid_by_mode_beta_substep'].shape==(40,3,2)
 assert np.count_nonzero(z['candidate_C_y1_valid_by_mode_beta_substep'])==j['evaluated_shift_case_count']
 assert np.count_nonzero(z['candidate_C_y0_valid_by_mode_beta'])==120-j['initial_boundary_failure_count']
 assert all(np.isfinite(z[k]).all() for k in z.files)
print('GE19_D34R1_BOUNDARY_LEDGER_AND_UNCERTIFIED_SCOPE_PASS',flush=True)
print('GE19_D34R1_BOUNDARY_FAILURE_COUNT',j['initial_boundary_failure_count'],
      'EVALUATED_SHIFT_CASES',j['evaluated_shift_case_count'],
      'UNOBSERVED_SHIFT_CASES',j['unevaluated_shift_case_count'],flush=True)
PYRUN
sha256sum "${P}.json" "${P}.npz" "${P}_FULL.log"
echo GE19_D34R1_EXECUTION_COMPLETE
