#!/usr/bin/env bash
set -euo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
[[ "$(git branch --show-current)" == 'physics-first-gravitational-elasticity' ]] || { echo GE19_D34_WRONG_BRANCH; exit 4; }
[[ -f .venv/bin/activate ]] || { echo GE19_D34_MISSING_VENV; exit 5; }
source .venv/bin/activate
export PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$ROOT" OPENBLAS_NUM_THREADS="${OPENBLAS_NUM_THREADS:-1}"
mkdir -p results
P='results/ge19_h4f3d34_all_mode_first_interval_gate_scan'
for f in "${P}.json" "${P}.npz" "${P}_FULL.log"; do
  [[ ! -e "$f" ]] || { echo "GE19_D34_REFUSE_OVERWRITE $f"; exit 6; }
done
python -u ge19/h4f3d34_all_mode_first_interval_gate_scan_static_test.py
set +e
python -u -m ge19.h4f3d34_all_mode_first_interval_gate_scan \
  --results-dir "$ROOT/results" --json-out "$ROOT/${P}.json" --npz-out "$ROOT/${P}.npz" \
  2>&1 | tee "${P}_FULL.log"
rc=${PIPESTATUS[0]}
set -e
echo "EXIT=$rc"
if [[ "$rc" -ne 0 ]]; then echo "GE19_D34_EXECUTION_FAIL rc=$rc"; exit "$rc"; fi
python - "$ROOT/${P}.json" "$ROOT/${P}.npz" <<'PYRUN'
import json,sys,numpy as np
j=json.load(open(sys.argv[1]))
assert j['classification']=='GE19_D34_ALL_M1_TO_M40_ALL_BETA_FIRST_INTERVAL_DIAGNOSTIC_COMPLETE_PARENTS_UNCERTIFIED'
assert j['all_case_count']==240 and len(j['per_case'])==240
assert j['original_D33_selected_control_replayed'] and j['nonanalytic_StageE_Y_retained']
assert j['original_shift_gate_unchanged'] and j['all_reduced_modes_m1_to_m40_retained']
assert j['m0_source_retained_separate_from_reduced_k0_evolution']
assert j['H3_full_window_solve_performed'] is False
assert not any(j[k] for k in ('Z11_certified','Z20_certified','Z21_certified','lensing_licensed','production_H3F_source_modified'))
assert len(j['per_beta_summary'])==3 and all(r['beta'] in (1.0,0.5,0.1) for r in j['per_case'])
with np.load(sys.argv[2],allow_pickle=False) as z:
 assert z['candidate_C_y1_by_mode_beta_substep_8'].shape==(40,3,2,8)
 assert z['candidate_C_y0_by_mode_beta_8'].shape==(40,3,8)
 assert all(np.isfinite(z[k]).all() for k in z.files)
print('GE19_D34_RESULT_AND_UNCERTIFIED_SCOPE_PASS',flush=True)
print('GE19_D34_ORIGINAL_SHIFT_GATE_ALL_MODES_REPORT_ONLY',j['all_first_interval_original_shift_gates_pass'],
      'failures',j['shift_gate_fail_count'],flush=True)
PYRUN
sha256sum "${P}.json" "${P}.npz" "${P}_FULL.log"
echo GE19_D34_EXECUTION_COMPLETE
