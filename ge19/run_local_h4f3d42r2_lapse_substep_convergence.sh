#!/usr/bin/env bash
set -euo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
[[ "$(git branch --show-current)" == 'physics-first-gravitational-elasticity' ]] || { echo GE19_D42R2_WRONG_BRANCH; exit 4; }
[[ -f .venv/bin/activate ]] || { echo GE19_D42R2_MISSING_VENV; exit 5; }
source .venv/bin/activate
export PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$ROOT" OPENBLAS_NUM_THREADS="${OPENBLAS_NUM_THREADS:-1}"
mkdir -p results
P='results/ge19_h4f3d42r2_lapse_substep_convergence'
for f in "${P}.json" "${P}.npz" "${P}_FULL.log"; do
  [[ ! -e "$f" ]] || { echo "GE19_D42R2_REFUSE_OVERWRITE $f"; exit 6; }
done
BASE='ge19/h4f3d42_lapse_substep_convergence.py'
PREVIOUS='ge19/h4f3d42r1_lapse_substep_convergence.py'
REPAIRED='ge19/h4f3d42r2_lapse_substep_convergence.py'
[[ "$(sha256sum "$BASE" | awk '{print $1}')" == 'e590deb370849556d6419b145fc70218fd9fc6c621d0b691a6e5b05f8993a392' ]] || { echo GE19_D42R2_ORIGINAL_SOURCE_CHANGED; exit 7; }
[[ "$(sha256sum "$PREVIOUS" | awk '{print $1}')" == '1c0637d23efc4d48d91a8dc494ea7c7feae9a621712be54b15901433d5b9c3ab' ]] || { echo GE19_D42R2_R1_SOURCE_CHANGED; exit 8; }
[[ "$(sha256sum "$REPAIRED" | awk '{print $1}')" == '66a1e01a869eaaea8d1a4158b258f95f1480325ad59fd33d04ec58aef23b2654' ]] || { echo GE19_D42R2_REPAIRED_SOURCE_CHANGED; exit 9; }
python - "$BASE" "$PREVIOUS" "$REPAIRED" "$ROOT/results/ge19_h4f3d41_full_window_two_constraint_audit.npz" <<'PY_PREFLIGHT'
from pathlib import Path
import ast, sys, hashlib
import numpy as np
old, r1, r2, data=map(Path,sys.argv[1:])
a=old.read_text();b=r1.read_text();c=r2.read_text()
path_old="j41=json.loads((rd/STEM.replace('d42_lapse_substep_convergence','d41_full_window_two_constraint_audit')+'.json').read_text())"
path_new="j41=json.loads((rd/'ge19_h4f3d41_full_window_two_constraint_audit.json').read_text())"
assert a.count(path_old)==1 and b==a.replace(path_old,path_new),'D42R1_INHERITED_PATH_DIFF_MISMATCH'
changes=[
 ('lap[:,:,:,entry_for_sub(n)]=frozenlap[:,selected_indices,:,0 if n==1 else 1]',
  'lap[:,:,:,entry_for_sub(n)]=np.take(frozenlap[:,:,:,0 if n==1 else 1],selected_indices,axis=1)'),
 ('shift[:,:,:,entry_for_sub(n)]=frozenshift[:,selected_indices,:,0 if n==1 else 1]',
  'shift[:,:,:,entry_for_sub(n)]=np.take(frozenshift[:,:,:,0 if n==1 else 1],selected_indices,axis=1)')]
want=b
for x,y in changes:
 assert want.count(x)==1 and c.count(y)==1, 'D42R2_EXPECTED_EXACTLY_ONE_COPY_ASSIGNMENT'
 want=want.replace(x,y)
assert c==want,'D42R2_NOT_EXACT_TWO_ASSIGNMENT_REPAIR'
ast.parse(c)
print('GE19_D42R2_EXACT_TWO_FROZEN_AXIS_ASSIGNMENTS_AND_AST_PASS',flush=True)
assert hashlib.sha256(data.read_bytes()).hexdigest()=='17a64a7f0329a362d73f16705a547027c3743d2f146cbaa70ce65dd8bf95f82c','D42R2_FROZEN_D41_NPZ_SHA_MISMATCH'
with np.load(data,allow_pickle=False) as z:
 modes=np.asarray(z['modes'],int)
 assert np.array_equal(modes,np.arange(1,41))
 assert np.array_equal(z['substeps'],[1,8])
 for key in ['original_lapse_relative_backward_audit','original_shift_relative_backward_replay']:
  a=z[key]
  assert a.shape==(128,40,3,2), (key,a.shape)
  idx=np.array([1,6,14,26,40])-1
  for old_sub in [0,1]:
   v=np.take(a[:,:,:,old_sub],idx,axis=1)
   reference=np.stack([a[:,int(j),:,old_sub] for j in idx],axis=1)
   assert v.shape==(128,5,3) and np.array_equal(v,reference),key
print('GE19_D42R2_REAL_FROZEN_D41_128x5x3_AXIS_AND_MODE_ORDER_PASS',flush=True)
PY_PREFLIGHT
python -u ge19/h4f3d42_lapse_substep_convergence_static_test.py
set +e
python -u -m ge19.h4f3d42r2_lapse_substep_convergence \
  --results-dir "$ROOT/results" --json-out "$ROOT/${P}.json" --npz-out "$ROOT/${P}.npz" \
  2>&1 | tee "${P}_FULL.log"
rc=${PIPESTATUS[0]}
set -e
echo "EXIT=$rc"
if [[ "$rc" -ne 0 ]]; then echo "GE19_D42R2_EXECUTION_FAIL rc=$rc"; exit "$rc"; fi
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
 print('GE19_D42R2_RESULT_AND_UNCERTIFIED_DIAGNOSTIC_SCOPE_PASS',flush=True)
 print('GE19_D42R2_NEW_EVALUATED',j['new_endpoint_evaluated'],'UNOBSERVED',j['new_endpoint_unevaluated'],
       'NEW_LAPSE_REPORT_ONLY_ABOVE',j['observed_new_lapse_over_reference_count'],flush=True)
PYRUN
sha256sum "${P}.json" "${P}.npz" "${P}_FULL.log"
echo GE19_D42R2_EXECUTION_COMPLETE
