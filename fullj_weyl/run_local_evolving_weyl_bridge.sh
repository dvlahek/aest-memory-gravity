#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

BASE_PY=""
if command -v python3 >/dev/null 2>&1; then
  BASE_PY="$(command -v python3)"
elif command -v python >/dev/null 2>&1; then
  BASE_PY="$(command -v python)"
else
  echo "FULLJ_WEYL: python missing" >&2
  exit 2
fi

VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then
  "$BASE_PY" -m venv "$VENV" || { echo "FULLJ_WEYL: install python3-venv" >&2; exit 2; }
fi
export PATH="$VENV/bin:$PATH"
python -m pip install --upgrade pip setuptools wheel >/dev/null
python -m pip install numpy scipy cython >/dev/null

python -m py_compile \
  fullj_weyl/evolving_flrw_weyl_bridge.py \
  nl1c6d2c6b/all27_physical_nonlinear_trajectories.py \
  nl1c6d2c6ar1/stable_canonical_integrator.py \
  nl1c6d2c6a/physical_time_scalar_current_integrator.py \
  nl1c6d2n/corrected_class_baseline.py \
  nl1c6d2a/baryon_matter_sector_audit.py \
  nl1c6/full_j_baryonic_reclosure.py

echo "FULLJ_WEYL: preparing pinned corrected/F-state CLASS environment..."
bash act_fstate/setup_fstate_class.sh
# shellcheck disable=SC1091
source results/act_fstate_class_env.sh

# D2C6 expects the corrected CLASS root under this historical variable name.
export NL1C6D2N_CLASS_ROOT="$FSTATE_CLASS_ROOT"
test -x "$NL1C6D2N_CLASS_ROOT/class"

python - <<'PY'
import numpy, scipy
from classy import Class
import classy, os
print('FULLJ_WEYL_ENV_PASS')
print('numpy='+numpy.__version__)
print('scipy='+scipy.__version__)
print('classy_module='+str(classy.__file__))
print('NL1C6D2N_CLASS_ROOT='+os.environ['NL1C6D2N_CLASS_ROOT'])
c=Class(); c.empty()
PY

JSON="results/fullj_evolving_weyl_bridge.json"
NPZ="results/fullj_evolving_weyl_bridge.npz"
LOG="results/fullj_evolving_weyl_bridge.log"
ZIP="results/fullj_evolving_weyl_bridge_bundle.zip"
rm -f "$JSON" "$NPZ" "$LOG" "$ZIP"

export OMP_NUM_THREADS=1
unset AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE AEST_OFFLINE_TRACE_FILE AEST_TANGENT_ALLOW_K_MISS || true

set +e
python -u fullj_weyl/evolving_flrw_weyl_bridge.py \
  --json-out "$JSON" \
  --npz-out "$NPZ" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

python - "$ZIP" "$LOG" "$JSON" "$NPZ" <<'PY'
from pathlib import Path
import sys, zipfile
zp=Path(sys.argv[1])
paths=[Path(x) for x in sys.argv[2:]] + [
    Path('docs/fullj_evolving_weyl_bridge_predata.md'),
    Path('docs/fullj_phase_robustness_LOCKED_RESULT.md'),
    Path('docs/nl1c6d2c5_action_level_flrw_longitudinal_derivation.md'),
    Path('fullj_weyl/evolving_flrw_weyl_bridge.py'),
    Path('fullj_weyl/run_local_evolving_weyl_bridge.sh'),
    Path('nl1c6d2c6b/all27_physical_nonlinear_trajectories.py'),
    Path('nl1c6d2c6ar1/stable_canonical_integrator.py'),
    Path('nl1c6d2c6g/eta0_metric_tangent_calibration.py'),
    Path('results/act_fstate_apply_report.json'),
]
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED) as zf:
    seen=set()
    for p in paths:
        if p.exists() and p not in seen:
            zf.write(p,arcname=str(p)); seen.add(p)
print('FULLJ_WEYL_BUNDLE='+str(zp))
PY

echo "FULLJ_WEYL_EXIT=$code"
echo "FULLJ_WEYL_LOG=$LOG"
echo "FULLJ_WEYL_JSON=$JSON"
echo "FULLJ_WEYL_NPZ=$NPZ"
echo "FULLJ_WEYL_ZIP=$ZIP"
exit "$code"
