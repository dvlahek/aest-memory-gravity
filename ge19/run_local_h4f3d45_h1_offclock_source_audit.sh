#!/usr/bin/env bash
set -euo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
[[ "$(git branch --show-current)" == 'physics-first-gravitational-elasticity' ]] || { echo GE19_D45_WRONG_BRANCH_MAIN_FORBIDDEN; exit 4; }
[[ -x .venv/bin/python ]] || { echo GE19_D45_MISSING_ORIGINAL_G19_VENV; exit 5; }
PY="$ROOT/.venv/bin/python"
export PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$ROOT" OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
mkdir -p results
P='results/ge19_h4f3d45_h1_offclock_source_audit'
for f in "${P}.json" "${P}.npz" "${P}_FULL.log"; do
    [[ ! -e "$f" ]] || { echo "GE19_D45_REFUSE_OVERWRITE $f"; exit 6; }
done
# This program and prereg are hash-checked before use; the script never patches ancestors.
for pair in \
  'ge19/h4f3d45_h1_offclock_source_audit.py 81c6273996c0c08afb005c24a76fb59feb30eaeaa38dc3f8f6409fb315a5b8f3' \
  'ge19/h4f3d45_h1_offclock_source_audit_prereg.json a89b8b0bcbca231edd4caf119a92bbc28ce2c4c7fd442be6f86f1009eead7b70' \
  'ge19/h4f3d45_h1_offclock_source_audit_static_test.py 99eeff0c04e466f540682881cd11cd5a6c17e5ba75ba846389fb165365fb3f5b'; do
    read -r f want <<< "$pair"
    [[ "$(sha256sum "$f" | awk '{print $1}')" == "$want" ]] || { echo "GE19_D45_SELF_SHA_CHANGED $f"; exit 7; }
done
"$PY" -u ge19/h4f3d45_h1_offclock_source_audit_static_test.py
set +e
"$PY" -u -m ge19.h4f3d45_h1_offclock_source_audit \
    --results-dir "$ROOT/results" \
    --json-out "$ROOT/${P}.json" \
    --npz-out "$ROOT/${P}.npz" \
    2>&1 | tee "${P}_FULL.log"
rc=${PIPESTATUS[0]}
set -e
echo "GE19_D45_PYTHON_EXIT=$rc"
[[ "$rc" -eq 0 ]] || { echo GE19_D45_IMPLEMENTATION_OR_DIAGNOSTIC_FAIL_PRESERVE_LOG; exit "$rc"; }
"$PY" - "$ROOT/${P}.json" "$ROOT/${P}.npz" <<'PY_POST'
import json,sys,numpy as np
j=json.load(open(sys.argv[1]))
assert j['classification']=='GE19_D45_OFFCLOCK_HOMOGENEOUS_BACKGROUND_AND_SOURCE_INTERPOLATION_DIAGNOSTIC_COMPLETE_PARENTS_UNCERTIFIED'
assert j['homogeneous_background']['clock_nodes']==128 and j['homogeneous_background']['midpoint_count']==127
assert j['source_interpolation']['source_modes']==41 and j['source_interpolation']['intervals']==127
assert not any(j[k] for k in ('original_action_modified','production_H3F_source_modified','H1_on_shell_verified','Noether_ward_verified','H3_full_window_certified','Z11_certified','Z20_certified','Z21_certified','lensing_licensed'))
with np.load(sys.argv[2],allow_pickle=False) as z:
  assert z['interval_mid_x'].shape==(127,)
  assert z['source_PCHIP_mid'].shape==(8,127,41,3)
  assert z['source_linear_mid'].shape==(8,127,41,3)
  assert z['original_action_H_mid'].shape==(127,)
  assert all(np.isfinite(z[k]).all() for k in z.files)
print('GE19_D45_POSTRUN_ORIGINAL_ACTION_OFFCLOCK_AND_UNCERTIFIED_SCOPE_PASS',flush=True)
PY_POST
sha256sum "${P}.json" "${P}.npz" "${P}_FULL.log"
echo GE19_D45_COMPLETED_DIAGNOSTIC_ONLY_H1_EOM_H3_Z21_LENSING_OPEN
