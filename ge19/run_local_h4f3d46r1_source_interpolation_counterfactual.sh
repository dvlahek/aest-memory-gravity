#!/usr/bin/env bash
set -euo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
[[ "$(git branch --show-current)" == 'physics-first-gravitational-elasticity' ]] || { echo GE19_D46R1_WRONG_BRANCH_MAIN_FORBIDDEN; exit 4; }
[[ -x .venv/bin/python ]] || { echo GE19_D46R1_MISSING_ORIGINAL_GE19_VENV; exit 5; }
PY="$ROOT/.venv/bin/python"
export PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$ROOT" OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
mkdir -p results
P='results/ge19_h4f3d46r1_source_interpolation_counterfactual'
for f in "${P}.json" "${P}.npz" "${P}_FULL.log"; do
    [[ ! -e "$f" ]] || { echo "GE19_D46R1_REFUSE_OVERWRITE $f"; exit 6; }
done
for pair in   'ge19/h4f3d46_source_interpolation_counterfactual.py 0b45c930b45623990567cdb085c831bf0fb2e0fe738710136f2ca856d0a8c56c'   'ge19/h4f3d46_source_interpolation_counterfactual_prereg.json 8970c074786348ff6b04702a97e10d6f2f47d42582c793a0b97f4844b304946e'   'ge19/h4f3d46r1_source_interpolation_counterfactual.py 4d962b98d6017a75fe70096730629a679c53adccf6b135efa0348afee6832621'   'ge19/h4f3d46r1_source_interpolation_counterfactual_prereg.json 2b59bf00b4f435f0e34d26a9293cc098d14e07ddc66ce88e56d5e21bc54f28bd'   'ge19/h4f3d46r1_manifest_repair_selftest.py 27aabe60096e15ab7a0428e4d9a9578792eb25eae5161eba3b33a9e8db5f3822'; do
    read -r f want <<< "$pair"
    [[ "$(sha256sum "$f" | awk '{print $1}')" == "$want" ]] || { echo "GE19_D46R1_SHA_CHANGED $f"; exit 7; }
done
[[ -f results/ge19_h4f3d46_source_interpolation_counterfactual_FULL.log ]] || { echo GE19_D46R1_ORIGINAL_FAIL_LOG_MISSING; exit 8; }
grep -Fq 'GE19_D46_PARENT_SHA_FAIL_ge19_h4f3d33_direct_ge07_paired_first_interval.npz' results/ge19_h4f3d46_source_interpolation_counterfactual_FULL.log || { echo GE19_D46R1_ORIGINAL_FAILURE_NOT_RECORDED; exit 8; }
"$PY" -u ge19/h4f3d46r1_manifest_repair_selftest.py
"$PY" -u -m ge19.h4f3d46r1_source_interpolation_counterfactual --self-test --preflight-only --results-dir "$ROOT/results"
set +e
"$PY" -u -m ge19.h4f3d46r1_source_interpolation_counterfactual     --results-dir "$ROOT/results"     --json-out "$ROOT/${P}.json"     --npz-out "$ROOT/${P}.npz"     2>&1 | tee "${P}_FULL.log"
rc=${PIPESTATUS[0]}
set -e
echo "GE19_D46R1_PYTHON_EXIT=$rc"
[[ "$rc" -eq 0 ]] || { echo GE19_D46R1_IMPLEMENTATION_OR_SCIENCE_FAIL_PRESERVE_FULL_LOG; exit "$rc"; }
"$PY" - "${P}.json" "${P}.npz" <<'PY_POST'
import json,sys,numpy as np
j=json.load(open(sys.argv[1]))
assert j['classification'] in ('GE19_D46_FIVE_MODE_SOURCE_INTERPOLATION_COUNTERFACTUAL_COMPLETE_PARENTS_UNCERTIFIED',
                              'GE19_D46_ALTERNATIVE_SOURCE_INTERPOLATION_CONTROL_INCOMPLETE_PARENTS_UNCERTIFIED')
assert j['preregistration']=='GE19_D46R1_PREEXEC_FROZEN_D33_PCHIP_VS_LINEAR_SOURCE_INTERPOLATION_COUNTERFACTUAL_SHA_REPAIR'
assert j['original_action_modified'] is False and j['original_D33_source_knots_modified'] is False
assert j['original_PCHIP_production_modified'] is False and j['original_shift_gate_unchanged'] is True
assert not any(j[k] for k in ('H1_on_shell_verified','H3_full_window_certified','Noether_ward_verified',
                             'Z11_certified','Z20_certified','Z21_certified','lensing_licensed'))
assert j['frozen_original_parent_sha256']['ge19_h4f3d33_direct_ge07_paired_first_interval.npz']=='41c75b883b7df7b1f57b72f0309d71e1c7c3779f291e524f33fa7532861eb264'
with np.load(sys.argv[2],allow_pickle=False) as z:
    assert z['diagnostic_modes'].tolist()==[1,6,14,26,40]
    assert z['alternative_evaluated'].shape==(128,5,3)
    assert z['alternative_y_by_node_mode_beta'].shape==(128,5,3,8)
    assert z['original_frozen_n4_lapse'].shape==(128,5,3)
    assert np.isfinite(z['alternative_lapse'][z['alternative_evaluated']]).all()
if j['classification']!='GE19_D46_FIVE_MODE_SOURCE_INTERPOLATION_COUNTERFACTUAL_COMPLETE_PARENTS_UNCERTIFIED':
    print('GE19_D46R1_CONTROL_INCOMPLETE_NO_PARENTS_PROMOTED',flush=True)
    sys.exit(12)
assert j['alternative_propagated_endpoints_evaluated']==j['alternative_propagated_endpoints_expected']==1905
print('GE19_D46R1_ALL_1905_ALT_ENDPOINTS_AND_SCOPE_POSTRUN_PASS',flush=True)
PY_POST
sha256sum "${P}.json" "${P}.npz" "${P}_FULL.log"
echo GE19_D46R1_SOURCE_INTERPOLATION_COUNTERFACTUAL_COMPLETE_PARENTS_UNCERTIFIED
