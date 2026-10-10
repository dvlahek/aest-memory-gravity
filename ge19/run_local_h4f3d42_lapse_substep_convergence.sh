#!/usr/bin/env bash
set -euo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
[[ "$(git branch --show-current)" == 'physics-first-gravitational-elasticity' ]] || { echo GE19_D42_WRONG_BRANCH; exit 4; }
[[ -f .venv/bin/activate ]] || { echo GE19_D42_MISSING_VENV; exit 5; }
source .venv/bin/activate
export PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$ROOT" OPENBLAS_NUM_THREADS="${OPENBLAS_NUM_THREADS:-1}"
mkdir -p results
P='results/ge19_h4f3d42_lapse_substep_convergence'
for f in "${P}.json" "${P}.npz" "${P}_FULL.log"; do
  [[ ! -e "$f" ]] || { echo "GE19_D42_REFUSE_OVERWRITE $f"; exit 6; }
done
python -u ge19/h4f3d42_lapse_substep_convergence_static_test.py
set +e
python -u -m ge19.h4f3d42_lapse_substep_convergence \
  --results-dir "$ROOT/results" --json-out "$ROOT/${P}.json" --npz-out "$ROOT/${P}.npz" \
  2>&1 | tee "${P}_FULL.log"
rc=${PIPESTATUS[0]}
set -e
echo "EXIT=$rc"
if [[ "$rc" -ne 0 ]]; then echo "GE19_D42_EXECUTION_FAIL rc=$rc"; exit "$rc"; fi
python - "$ROOT/${P}.json" "$ROOT/${P}.npz" <<'PYRUN'
import json,sys,numpy as np
j=json.load(open(sys.argv[1]));assert j['classification']=='GE19_D42_TWO_SECTOR_LAPSE_SUBSTEP_CONVERGENCE_DIAGNOSTIC_PARENTS_UNCERTIFIED'
assert j['frozen_D41_original_lapse_above_1e_minus_6']==120
assert j['new_endpoint_expected']==5715 and j['new_endpoint_evaluated']+j['new_endpoint_unevaluated']==5715
assert j['D22A_original_science_FAIL_immutable'] and j['D34_D34R1_original_m26_boundary_FAIL_immutable']
assert j['D35_m26_posthoc_momentum_representation_not_original_bitwise']
assert not any(j[k] for k in ('original_action_modified','production_H3F_source_modified','H1_on_shell_verified',
                              'Noether_ward_verified','H3_full_window_certified','Z11_certified','Z20_certified','Z21_certified','lensing_licensed'))
with np.load(sys.argv[2],allow_pickle=False) as z:
 assert np.array_equal(z['diagnostic_modes'],[1,6,14,26,40]) and np.array_equal(z['sample_substeps'],[1,2,4,8,16])
 assert z['new_state_numerically_evaluated'].shape==(128,5,3,3)
 assert z['lapse_relative_backward_by_node_mode_beta_substep'].shape==(128,5,3,5)
 assert np.all(np.isfinite(z['lapse_relative_backward_by_node_mode_beta_substep'][:,:,:,[0,3]]))
 assert np.count_nonzero(z['new_state_numerically_evaluated'][1:])==j['new_endpoint_evaluated']
 print('GE19_D42_RESULT_AND_UNCERTIFIED_DIAGNOSTIC_SCOPE_PASS',flush=True)
 print('GE19_D42_NEW_EVALUATED',j['new_endpoint_evaluated'],'UNOBSERVED',j['new_endpoint_unevaluated'],
       'NEW_LAPSE_REPORT_ONLY_ABOVE',j['observed_new_lapse_over_reference_count'],flush=True)
PYRUN
sha256sum "${P}.json" "${P}.npz" "${P}_FULL.log"
echo GE19_D42_EXECUTION_COMPLETE
