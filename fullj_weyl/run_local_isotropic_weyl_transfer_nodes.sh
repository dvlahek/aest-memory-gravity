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
  echo "FULLJ_ISO_TRANSFER: python missing" >&2
  exit 2
fi

VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then
  "$BASE_PY" -m venv "$VENV" || { echo "FULLJ_ISO_TRANSFER: install python3-venv" >&2; exit 2; }
fi
export PATH="$VENV/bin:$PATH"
python -m pip install --upgrade pip setuptools wheel >/dev/null
python -m pip install numpy scipy cython >/dev/null

python -m py_compile \
  fullj_weyl/isotropic_weyl_transfer_nodes.py \
  fullj_weyl/evolving_flrw_weyl_bridge_r2.py \
  fullj_weyl/evolving_flrw_weyl_bridge_r1.py \
  fullj_weyl/evolving_flrw_weyl_bridge.py \
  nl1c6d2c6b/all27_physical_nonlinear_trajectories.py

python - <<'PY'
from fullj_weyl import isotropic_weyl_transfer_nodes as iso
from fullj_weyl import evolving_flrw_weyl_bridge_r2 as r2
assert iso.r2 is r2
assert iso.m is r2.m
print('FULLJ_ISO_TRANSFER_IMPORT_CHAIN_PASS')
PY

GAUSS_JSON="$ROOT/results/fullj_evolving_weyl_gaussian_1d_ensemble.json"
if [[ ! -f "$GAUSS_JSON" ]]; then
  echo "FULLJ_ISO_TRANSFER: missing locked local Gaussian 1D result JSON: $GAUSS_JSON" >&2
  exit 3
fi

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
  echo "FULLJ_ISO_TRANSFER: reusing existing D2C6-certified corrected CLASS environment..."
else
  echo "FULLJ_ISO_TRANSFER: preparing D2C6-certified corrected CLASS environment..."
  bash nl1c6d2n/setup_corrected_class_local.sh
  # shellcheck disable=SC1091
  source "$ENVFILE"
fi

python - <<'PY'
import os, numpy, scipy, classy
from classy import Class
print('FULLJ_ISO_TRANSFER_ENV_PASS')
print('numpy='+numpy.__version__)
print('scipy='+scipy.__version__)
print('classy_module='+str(classy.__file__))
print('NL1C6D2N_CLASS_ROOT='+os.environ['NL1C6D2N_CLASS_ROOT'])
c=Class(); c.empty()
PY

JSON="results/fullj_isotropic_weyl_transfer_nodes.json"
NPZ="results/fullj_isotropic_weyl_transfer_nodes.npz"
LOG="results/fullj_isotropic_weyl_transfer_nodes.log"
ZIP="results/fullj_isotropic_weyl_transfer_nodes_bundle.zip"
rm -f "$JSON" "$NPZ" "$LOG" "$ZIP"

export OMP_NUM_THREADS=1
unset AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE AEST_OFFLINE_TRACE_FILE AEST_TANGENT_ALLOW_K_MISS || true

set +e
python -u fullj_weyl/isotropic_weyl_transfer_nodes.py \
  --json-out "$JSON" \
  --npz-out "$NPZ" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

python - "$ZIP" "$LOG" "$JSON" "$NPZ" "$GAUSS_JSON" <<'PY'
from pathlib import Path
import sys, zipfile
zp=Path(sys.argv[1])
paths=[Path(x) for x in sys.argv[2:]] + [
    Path('docs/fullj_3d_saturated_constitutive_closure_result.md'),
    Path('docs/fullj_isotropic_weyl_transfer_nodes_predata.md'),
    Path('fullj_weyl/isotropic_weyl_transfer_nodes.py'),
    Path('fullj_weyl/run_local_isotropic_weyl_transfer_nodes.sh'),
    Path('fullj_weyl/evolving_flrw_weyl_bridge_r2.py'),
    Path('results/nl1c6d2n_corrected_class_env.sh'),
]
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED) as zf:
    seen=set()
    for p in paths:
        if p.exists() and p not in seen:
            zf.write(p,arcname=str(p)); seen.add(p)
print('FULLJ_ISO_TRANSFER_BUNDLE='+str(zp))
PY

echo "FULLJ_ISO_TRANSFER_EXIT=$code"
echo "FULLJ_ISO_TRANSFER_LOG=$LOG"
echo "FULLJ_ISO_TRANSFER_JSON=$JSON"
echo "FULLJ_ISO_TRANSFER_NPZ=$NPZ"
echo "FULLJ_ISO_TRANSFER_ZIP=$ZIP"
exit "$code"
