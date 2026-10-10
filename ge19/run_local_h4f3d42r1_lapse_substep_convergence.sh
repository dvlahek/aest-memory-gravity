#!/usr/bin/env bash
set -euo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
[[ "$(git branch --show-current)" == 'physics-first-gravitational-elasticity' ]] || { echo GE19_D42R1_WRONG_BRANCH; exit 4; }
[[ -f .venv/bin/activate ]] || { echo GE19_D42R1_MISSING_VENV; exit 5; }
source .venv/bin/activate
export PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$ROOT" OPENBLAS_NUM_THREADS="${OPENBLAS_NUM_THREADS:-1}"
mkdir -p results
P='results/ge19_h4f3d42r1_lapse_substep_convergence'
for f in "${P}.json" "${P}.npz" "${P}_FULL.log"; do
  [[ ! -e "$f" ]] || { echo "GE19_D42R1_REFUSE_OVERWRITE $f"; exit 6; }
done
# D42R1 implementation-only repair. Preserve the original failed D42 source and logs.
BASE='ge19/h4f3d42_lapse_substep_convergence.py'
REPAIRED='ge19/h4f3d42r1_lapse_substep_convergence.py'
[[ "$(sha256sum "$BASE" | awk '{print $1}')" == 'e590deb370849556d6419b145fc70218fd9fc6c621d0b691a6e5b05f8993a392' ]] || { echo GE19_D42R1_ORIGINAL_SOURCE_CHANGED; exit 7; }
[[ "$(sha256sum "$REPAIRED" | awk '{print $1}')" == '1c0637d23efc4d48d91a8dc494ea7c7feae9a621712be54b15901433d5b9c3ab' ]] || { echo GE19_D42R1_REPAIRED_SOURCE_CHANGED; exit 8; }
python - "$BASE" "$REPAIRED" <<'PY_DIFFERENCE'
from pathlib import Path
import ast,sys
a=Path(sys.argv[1]).read_text();b=Path(sys.argv[2]).read_text()
old="j41=json.loads((rd/STEM.replace('d42_lapse_substep_convergence','d41_full_window_two_constraint_audit')+'.json').read_text())"
new="j41=json.loads((rd/'ge19_h4f3d41_full_window_two_constraint_audit.json').read_text())"
assert a.count(old)==1 and b==a.replace(old,new), 'D42R1_NOT_EXACT_ONE_LINE_REPAIR'
ast.parse(b)
print('GE19_D42R1_EXACT_ONE_LINE_PATH_REPAIR_AND_AST_PASS',flush=True)
PY_DIFFERENCE
python -u ge19/h4f3d42_lapse_substep_convergence_static_test.py
set +e
python -u -m ge19.h4f3d42r1_lapse_substep_convergence \
  --results-dir "$ROOT/results" --json-out "$ROOT/${P}.json" --npz-out "$ROOT/${P}.npz" \
  2>&1 | tee "${P}_FULL.log"
rc=${PIPESTATUS[0]}
set -e
echo "EXIT=$rc"
if [[ "$rc" -ne 0 ]]; then echo "GE19_D42R1_EXECUTION_FAIL rc=$rc"; exit "$rc"; fi
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
echo GE19_D42R1_EXECUTION_COMPLETE
