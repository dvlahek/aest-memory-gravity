#!/usr/bin/env bash
set -euo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
[[ "$(git branch --show-current)" == 'physics-first-gravitational-elasticity' ]] || { echo GE19_D43_WRONG_BRANCH; exit 4; }
[[ -f .venv/bin/activate ]] || { echo GE19_D43_MISSING_G19_VENV; exit 5; }
source .venv/bin/activate
export PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$ROOT" OPENBLAS_NUM_THREADS="${OPENBLAS_NUM_THREADS:-1}"
mkdir -p results
P='results/ge19_h4f3d43_full_40_mode_n2_n4_lapse'
for f in "${P}.json" "${P}.npz" "${P}_FULL.log"; do
 [[ ! -e "$f" ]] || { echo "GE19_D43_REFUSE_OVERWRITE $f"; exit 6; }
done
[[ "$(sha256sum ge19/h4f3d43_full_40_mode_n2_n4_lapse.py | awk '{print $1}')" == 'adcb8bfe55ee9f9b7a09ed101f10cc52540af1f19b845a275dbbf0da4139fdd0' ]] || { echo GE19_D43_SOURCE_CHANGED; exit 7; }
[[ "$(sha256sum ge19/h4f3d43_full_40_mode_n2_n4_prereg.json | awk '{print $1}')" == '9d186789e8f50e7946b8b5b4565b9db7564b094d437490b16616273142714d94' ]] || { echo GE19_D43_PRE_CHANGED; exit 8; }
[[ "$(sha256sum ge19/h4f3d42r2_lapse_substep_convergence.py | awk '{print $1}')" == '66a1e01a869eaaea8d1a4158b258f95f1480325ad59fd33d04ec58aef23b2654' ]] || { echo GE19_D43_D42R2_CODE_CHANGED; exit 9; }
for pair in  'ge19_h4f3d42r2_lapse_substep_convergence.json 4d958da57587c03cd5a23a82681e031d59af90775961774363c34ae5cc903e28'  'ge19_h4f3d42r2_lapse_substep_convergence.npz 5d949fe54a706cf1ebfe0702233ee416ae8c3e96615243dab0015d5fedb10218'; do
 read -r f want <<< "$pair"
 [[ "$(sha256sum "results/$f" | awk '{print $1}')" == "$want" ]] || { echo "GE19_D43_PARENT_OUTPUT_CHANGED $f"; exit 10; }
done
python -u ge19/h4f3d43_full_40_mode_n2_n4_static_test.py
set +e
python -u -m ge19.h4f3d43_full_40_mode_n2_n4_lapse \
 --results-dir "$ROOT/results" --json-out "$ROOT/${P}.json" --npz-out "$ROOT/${P}.npz" \
 2>&1 | tee "${P}_FULL.log"
rc=${PIPESTATUS[0]}
set -e
echo "GE19_D43_PYTHON_EXIT=$rc"
[[ "$rc" -eq 0 ]] || { echo "GE19_D43_EXECUTION_FAIL rc=$rc"; exit "$rc"; }
python - "$ROOT/${P}.json" "$ROOT/${P}.npz" <<'PY_POST'
import json,sys,numpy as np
j=json.load(open(sys.argv[1]))
assert j['new_endpoint_expected']==30480 and j['new_endpoint_evaluated']+j['new_endpoint_unevaluated']==30480
assert j['D22A_original_science_FAIL_immutable'] and j['D34_D34R1_original_m26_boundary_FAIL_immutable']
assert j['D35_m26_posthoc_momentum_representation_not_original_bitwise']
assert not any(j[k] for k in ('original_action_modified','production_H3F_source_modified','H1_on_shell_verified',
  'Noether_ward_verified','H3_full_window_certified','Z11_certified','Z20_certified','Z21_certified','lensing_licensed'))
with np.load(sys.argv[2],allow_pickle=False) as z:
 assert np.array_equal(z['diagnostic_modes'],np.arange(1,41)) and np.array_equal(z['sample_substeps'],[1,2,4,8])
 assert z['new_state_numerically_evaluated'].shape==(128,40,3,2)
 assert np.count_nonzero(z['new_state_numerically_evaluated'][1:])==j['new_endpoint_evaluated']
print('GE19_D43_ARCHIVE_AND_IMMUTABLE_SCOPE_PASS',flush=True)
print('GE19_D43_NEW_EVALUATED',j['new_endpoint_evaluated'],'UNEVALUATED',j['new_endpoint_unevaluated'],
      'SHIFT_GATE_FAIL',j['observed_new_shift_gate_fail_count'],'LAPSE_ABOVE_REFERENCE',j['observed_new_lapse_over_reference_count'],flush=True)
PY_POST
sha256sum "${P}.json" "${P}.npz" "${P}_FULL.log"
if [[ "$(python - "$ROOT/${P}.json" <<'PY_GATE'
import sys,json
j=json.load(open(sys.argv[1]))
print('PASS' if j['new_endpoint_unevaluated']==j['observed_new_shift_gate_fail_count']==0 else 'FAIL')
PY_GATE
)" != PASS ]]; then
 echo GE19_D43_ORIGINAL_SHIFT_OR_MISSING_ENDPOINT_GATE_FAIL_PRESERVE_ARTIFACTS
 exit 41
fi
echo GE19_D43_FULL_40_MODE_N2_N4_NUMERICAL_COHORT_COMPLETE_PARENTS_UNCERTIFIED
