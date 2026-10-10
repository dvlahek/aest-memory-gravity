#!/usr/bin/env bash
set -euo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
[[ "$(git branch --show-current)" == 'physics-first-gravitational-elasticity' ]] || { echo GE19_D46_WRONG_BRANCH_MAIN_FORBIDDEN; exit 4; }
[[ -x .venv/bin/python ]] || { echo GE19_D46_MISSING_ORIGINAL_GE19_VENV; exit 5; }
PY="$ROOT/.venv/bin/python"
export PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$ROOT" OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
mkdir -p results
P='results/ge19_h4f3d46_source_interpolation_counterfactual'
for f in "${P}.json" "${P}.npz" "${P}_FULL.log"; do
    [[ ! -e "$f" ]] || { echo "GE19_D46_REFUSE_OVERWRITE $f"; exit 6; }
done
# SHA-256 seals only new D46 inputs. Historical original-action parents are checked by D41.
for pair in \
  'ge19/h4f3d46_source_interpolation_counterfactual.py 0b45c930b45623990567cdb085c831bf0fb2e0fe738710136f2ca856d0a8c56c' \
  'ge19/h4f3d46_source_interpolation_counterfactual_prereg.json 8970c074786348ff6b04702a97e10d6f2f47d42582c793a0b97f4844b304946e' \
  'ge19/h4f3d46_source_interpolation_counterfactual_static_test.py 43d65d94ef3908efd49fd3faf5dcfc396c919c7bcc98b8b21adb361f027254ec'; do
    read -r f want <<< "$pair"
    [[ "$(sha256sum "$f" | awk '{print $1}')" == "$want" ]] || { echo "GE19_D46_SELF_SHA_CHANGED $f"; exit 7; }
done
"$PY" -u ge19/h4f3d46_source_interpolation_counterfactual_static_test.py
"$PY" -u -m ge19.h4f3d46_source_interpolation_counterfactual --self-test --preflight-only --results-dir "$ROOT/results"
set +e
"$PY" -u -m ge19.h4f3d46_source_interpolation_counterfactual \
    --results-dir "$ROOT/results" \
    --json-out "$ROOT/${P}.json" \
    --npz-out "$ROOT/${P}.npz" \
    2>&1 | tee "${P}_FULL.log"
rc=${PIPESTATUS[0]}
set -e
echo "GE19_D46_PYTHON_EXIT=$rc"
[[ "$rc" -eq 0 ]] || { echo GE19_D46_IMPLEMENTATION_FAIL_PRESERVE_FULL_LOG; exit "$rc"; }
"$PY" - "${P}.json" "${P}.npz" <<'PY_POST'
import json,sys,numpy as np
j=json.load(open(sys.argv[1]))
assert j['classification'] in (
 'GE19_D46_FIVE_MODE_SOURCE_INTERPOLATION_COUNTERFACTUAL_COMPLETE_PARENTS_UNCERTIFIED',
 'GE19_D46_ALTERNATIVE_SOURCE_INTERPOLATION_CONTROL_INCOMPLETE_PARENTS_UNCERTIFIED')
assert j['original_action_modified'] is False and j['original_D33_source_knots_modified'] is False
assert j['original_PCHIP_production_modified'] is False and j['original_shift_gate_unchanged'] is True
assert not any(j[k] for k in ('H1_on_shell_verified','H3_full_window_certified','Noether_ward_verified',
                             'Z11_certified','Z20_certified','Z21_certified','lensing_licensed'))
with np.load(sys.argv[2],allow_pickle=False) as z:
    assert z['diagnostic_modes'].tolist()==[1,6,14,26,40]
    assert z['alternative_evaluated'].shape==(128,5,3)
    assert z['alternative_y_by_node_mode_beta'].shape==(128,5,3,8)
    assert z['original_frozen_n4_lapse'].shape==(128,5,3)
    assert np.isfinite(z['alternative_lapse'][z['alternative_evaluated']]).all()
if j['classification']!='GE19_D46_FIVE_MODE_SOURCE_INTERPOLATION_COUNTERFACTUAL_COMPLETE_PARENTS_UNCERTIFIED':
    print('GE19_D46_CONTROL_INCOMPLETE_NO_PARENTS_PROMOTED',flush=True)
    sys.exit(12)
assert j['alternative_propagated_endpoints_evaluated']==j['alternative_propagated_endpoints_expected']==1905
print('GE19_D46_ALL_1905_ALT_ENDPOINTS_AND_SCOPE_POSTRUN_PASS',flush=True)
PY_POST
sha256sum "${P}.json" "${P}.npz" "${P}_FULL.log"
echo GE19_D46_FIVE_MODE_SOURCE_INTERPOLATION_NUMERICAL_COUNTERFACTUAL_COMPLETE_NO_H1_Z21_LENSING
