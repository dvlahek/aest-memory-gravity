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
  echo "FULLJ_GAUSS1D: python missing" >&2
  exit 2
fi

VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then
  "$BASE_PY" -m venv "$VENV" || { echo "FULLJ_GAUSS1D: install python3-venv" >&2; exit 2; }
fi
export PATH="$VENV/bin:$PATH"
python -m pip install --upgrade pip setuptools wheel >/dev/null
python -m pip install numpy scipy cython >/dev/null

python -m py_compile \
  fullj_weyl/evolving_weyl_gaussian_1d_ensemble.py \
  fullj_weyl/evolving_flrw_weyl_bridge_r2.py \
  fullj_weyl/evolving_flrw_weyl_bridge_r1.py \
  fullj_weyl/evolving_flrw_weyl_bridge.py \
  nl1c6d2c6b/all27_physical_nonlinear_trajectories.py \
  nl1c6d2c6ar1/stable_canonical_integrator.py \
  nl1c6d2c6a/physical_time_scalar_current_integrator_v4.py \
  nl1c6d2c6a/physical_time_scalar_current_integrator_v5.py \
  nl1c6d2c6a/physical_time_scalar_current_integrator_v6.py

python - <<'PY'
from fullj_weyl import evolving_weyl_gaussian_1d_ensemble as g
from fullj_weyl import evolving_flrw_weyl_bridge_r2 as r2
from nl1c6d2c6b import all27_physical_nonlinear_trajectories as d2b
assert g.r2 is r2
assert g.d2b is d2b
assert g.m is r2.m
xy, coeff, digest = g.coefficient_draw()
assert xy.shape == (32, 6, 2)
assert coeff.shape == (32, 6)
print('FULLJ_GAUSS1D_IMPORT_CHAIN_PASS')
print('FULLJ_GAUSS1D_COEFF_SHA256='+digest)
PY

ENVFILE="$ROOT/results/nl1c6d2n_corrected_class_env.sh"
reuse=0
if [[ -f "$ENVFILE" ]]; then
  # shellcheck disable=SC1090
  source "$ENVFILE"
  if [[ -n "${NL1C6D2N_CLASS_ROOT:-}" && -d "$NL1C6D2N_CLASS_ROOT/.git" \
        && -f "$NL1C6D2N_CLASS_ROOT/source/aest_memory.c" \
        && -n "${NL1C6D2N_PYTARGET:-}" && -f "$NL1C6D2N_PYTARGET/classy/__init__.py" ]]; then
    reuse=1
  fi
fi

if [[ "$reuse" -eq 1 ]]; then
  echo "FULLJ_GAUSS1D: reusing existing D2C6-certified corrected CLASS environment..."
else
  echo "FULLJ_GAUSS1D: preparing D2C6-certified corrected CLASS environment..."
  bash nl1c6d2n/setup_corrected_class_local.sh
  # shellcheck disable=SC1091
  source "$ENVFILE"
fi

python - <<'PY'
import os, numpy, scipy
from classy import Class
import classy
print('FULLJ_GAUSS1D_ENV_PASS')
print('numpy='+numpy.__version__)
print('scipy='+scipy.__version__)
print('classy_module='+str(classy.__file__))
print('NL1C6D2N_CLASS_ROOT='+os.environ['NL1C6D2N_CLASS_ROOT'])
c=Class(); c.empty()
PY

JSON="results/fullj_evolving_weyl_gaussian_1d_ensemble.json"
NPZ="results/fullj_evolving_weyl_gaussian_1d_ensemble.npz"
LOG="results/fullj_evolving_weyl_gaussian_1d_ensemble.log"
ZIP="results/fullj_evolving_weyl_gaussian_1d_ensemble_bundle.zip"
rm -f "$JSON" "$NPZ" "$LOG" "$ZIP"

export OMP_NUM_THREADS=1
unset AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE AEST_OFFLINE_TRACE_FILE AEST_TANGENT_ALLOW_K_MISS || true

set +e
python -u fullj_weyl/evolving_weyl_gaussian_1d_ensemble.py \
  --json-out "$JSON" \
  --npz-out "$NPZ" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

python - "$ZIP" "$LOG" "$JSON" "$NPZ" <<'PY'
from pathlib import Path
import sys, zipfile
zp=Path(sys.argv[1])
paths=[Path(x) for x in sys.argv[2:]] + [
    Path('docs/fullj_evolving_weyl_covariance_diagnostic_result.md'),
    Path('docs/fullj_evolving_weyl_gaussian_1d_ensemble_predata.md'),
    Path('docs/fullj_evolving_weyl_bridge_r2_result.md'),
    Path('docs/fullj_evolving_weyl_bridge_r2_predata.md'),
    Path('fullj_weyl/evolving_weyl_gaussian_1d_ensemble.py'),
    Path('fullj_weyl/evolving_flrw_weyl_bridge_r2.py'),
    Path('fullj_weyl/run_local_evolving_weyl_gaussian_1d_ensemble.sh'),
    Path('results/nl1c6d2n_corrected_class_env.sh'),
]
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED) as zf:
    seen=set()
    for p in paths:
        if p.exists() and p not in seen:
            zf.write(p,arcname=str(p)); seen.add(p)
print('FULLJ_GAUSS1D_BUNDLE='+str(zp))
PY

echo "FULLJ_GAUSS1D_EXIT=$code"
echo "FULLJ_GAUSS1D_LOG=$LOG"
echo "FULLJ_GAUSS1D_JSON=$JSON"
echo "FULLJ_GAUSS1D_NPZ=$NPZ"
echo "FULLJ_GAUSS1D_ZIP=$ZIP"
exit "$code"
