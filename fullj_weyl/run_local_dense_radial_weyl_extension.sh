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
  echo "FULLJ_DENSE_RADIAL: python missing" >&2
  exit 2
fi

VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then
  "$BASE_PY" -m venv "$VENV" || { echo "FULLJ_DENSE_RADIAL: install python3-venv" >&2; exit 2; }
fi
export PATH="$VENV/bin:$PATH"
python -m pip install --upgrade pip setuptools wheel >/dev/null
python -m pip install numpy scipy cython >/dev/null

python -m py_compile \
  fullj_weyl/dense_radial_weyl_extension.py \
  fullj_weyl/dense_radial_weyl_extension_r1.py \
  fullj_weyl/evolving_flrw_weyl_bridge_r2.py \
  fullj_weyl/evolving_flrw_weyl_bridge_r1.py \
  fullj_weyl/evolving_flrw_weyl_bridge.py \
  nl1c6d2c6b/all27_physical_nonlinear_trajectories.py

python - <<'PY'
from fullj_weyl import dense_radial_weyl_extension_r1 as fix
from fullj_weyl import evolving_flrw_weyl_bridge_r2 as r2
assert fix.mod.r2 is r2
assert len(fix.mod.nested_grids()[2]) == 21
assert fix.mod.N_EMBED == 10
print('FULLJ_DENSE_RADIAL_IMPORT_CHAIN_PASS')
PY

if [[ ! -f results/fullj_isotropic_weyl_transfer_nodes.json ]]; then
  echo "FULLJ_DENSE_RADIAL: missing results/fullj_isotropic_weyl_transfer_nodes.json" >&2
  exit 3
fi
if [[ ! -f results/fullj_isotropic_weyl_transfer_nodes_r1_phase_audit.json ]]; then
  echo "FULLJ_DENSE_RADIAL: missing results/fullj_isotropic_weyl_transfer_nodes_r1_phase_audit.json" >&2
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
  echo "FULLJ_DENSE_RADIAL: reusing existing D2C6-certified corrected CLASS environment..."
else
  echo "FULLJ_DENSE_RADIAL: preparing D2C6-certified corrected CLASS environment..."
  bash nl1c6d2n/setup_corrected_class_local.sh
  # shellcheck disable=SC1091
  source "$ENVFILE"
fi

python - <<'PY'
import os, numpy, scipy, classy
from classy import Class
print('FULLJ_DENSE_RADIAL_ENV_PASS')
print('numpy='+numpy.__version__)
print('scipy='+scipy.__version__)
print('classy_module='+str(classy.__file__))
print('NL1C6D2N_CLASS_ROOT='+os.environ['NL1C6D2N_CLASS_ROOT'])
c=Class(); c.empty()
PY

JSON="results/fullj_dense_radial_weyl_extension.json"
NPZ="results/fullj_dense_radial_weyl_extension.npz"
CSV="results/fullj_dense_radial_weyl_extension.csv"
LOG="results/fullj_dense_radial_weyl_extension.log"
ZIP="results/fullj_dense_radial_weyl_extension_bundle.zip"
rm -f "$JSON" "$NPZ" "$CSV" "$LOG" "$ZIP"

export OMP_NUM_THREADS=1
unset AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE AEST_OFFLINE_TRACE_FILE AEST_TANGENT_ALLOW_K_MISS || true

set +e
python -u fullj_weyl/dense_radial_weyl_extension_r1.py \
  --json-out "$JSON" \
  --npz-out "$NPZ" \
  --csv-out "$CSV" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

python - "$ZIP" "$LOG" "$JSON" "$NPZ" "$CSV" <<'PY'
from pathlib import Path
import sys, zipfile
zp=Path(sys.argv[1])
paths=[Path(x) for x in sys.argv[2:]] + [
    Path('docs/fullj_isotropic_weyl_transfer_nodes_r1_phase_audit_result.md'),
    Path('docs/fullj_dense_radial_weyl_extension_predata.md'),
    Path('fullj_weyl/dense_radial_weyl_extension.py'),
    Path('fullj_weyl/dense_radial_weyl_extension_r1.py'),
    Path('fullj_weyl/run_local_dense_radial_weyl_extension.sh'),
    Path('fullj_weyl/evolving_flrw_weyl_bridge_r2.py'),
    Path('results/fullj_isotropic_weyl_transfer_nodes.json'),
    Path('results/fullj_isotropic_weyl_transfer_nodes_r1_phase_audit.json'),
    Path('results/nl1c6d2n_corrected_class_env.sh'),
]
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED) as zf:
    seen=set()
    for p in paths:
        if p.exists() and p not in seen:
            zf.write(p,arcname=str(p)); seen.add(p)
print('FULLJ_DENSE_RADIAL_BUNDLE='+str(zp))
PY

echo "FULLJ_DENSE_RADIAL_EXIT=$code"
echo "FULLJ_DENSE_RADIAL_LOG=$LOG"
echo "FULLJ_DENSE_RADIAL_JSON=$JSON"
echo "FULLJ_DENSE_RADIAL_NPZ=$NPZ"
echo "FULLJ_DENSE_RADIAL_CSV=$CSV"
echo "FULLJ_DENSE_RADIAL_ZIP=$ZIP"
exit "$code"
