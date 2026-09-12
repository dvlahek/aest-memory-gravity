#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

BASE_PY=""
if command -v python3 >/dev/null 2>&1; then BASE_PY="$(command -v python3)";
elif command -v python >/dev/null 2>&1; then BASE_PY="$(command -v python)";
else echo "FULLJ_DENSE_RESIDUAL_R2: python missing" >&2; exit 2; fi

VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then
  "$BASE_PY" -m venv "$VENV" || { echo "FULLJ_DENSE_RESIDUAL_R2: install python3-venv" >&2; exit 2; }
fi
export PATH="$VENV/bin:$PATH"
python -m pip install --upgrade pip setuptools wheel >/dev/null
python -m pip install numpy scipy cython >/dev/null

python -m py_compile \
  fullj_weyl/apply_class_kfile_limit_patch.py \
  fullj_weyl/dense_radial_class_residual_r2.py \
  fullj_weyl/dense_radial_class_residual_r2_r1.py \
  fullj_weyl/dense_radial_weyl_extension.py \
  fullj_weyl/dense_radial_weyl_extension_r1.py \
  fullj_weyl/evolving_flrw_weyl_bridge_r2.py \
  fullj_weyl/evolving_flrw_weyl_bridge_r1.py \
  fullj_weyl/evolving_flrw_weyl_bridge.py \
  nl1c6d2c6b/all27_physical_nonlinear_trajectories.py

python - <<'PY'
import json
from fullj_weyl import dense_radial_weyl_extension_r1 as fix
from fullj_weyl import dense_radial_class_residual_r2_r1 as prov
x = prov.base
assert fix.DENSE_HISTORY_LOADER_REPAIR_ACTIVE
assert 'len(histories)!=len(K_MPC)' in fix.DENSE_HISTORY_LOADER_RUNTIME_SOURCE
assert prov.DENSE_RESIDUAL_R2_GAUSS_PROVENANCE_REPAIR_ACTIVE
status = prov.gaussian_provenance_status()
assert status['pass']
k1,k2,k3,h3=x.grids()
assert (len(k1),len(k2),len(k3),len(h3)) == (11,21,41,20)
assert x.N_EMBED == 10
print('FULLJ_DENSE_RESIDUAL_R2_IMPORT_CHAIN_PASS')
print('FULLJ_DENSE_RESIDUAL_R2_HISTORY_LOADER_REPAIR_PASS expected_from_K_MPC=True')
print('FULLJ_DENSE_RESIDUAL_R2_GAUSS_PROVENANCE_REPAIR_PRECHECK='+json.dumps(status,sort_keys=True))
PY

if [[ ! -f results/fullj_dense_radial_weyl_extension.json ]]; then
  echo "FULLJ_DENSE_RESIDUAL_R2: missing completed dense FAIL JSON" >&2; exit 3
fi

# This milestone needs 41 perturbation-output histories. Use an isolated CLASS
# build with only the compile-time output-capacity macro raised from 30 to 64.
ENVFILE="$ROOT/results/nl1c6d2n_corrected_class_densek64_env.sh"
reuse=0
if [[ -f "$ENVFILE" ]]; then
  # shellcheck disable=SC1090
  source "$ENVFILE"
  if [[ -n "${NL1C6D2N_CLASS_ROOT:-}" && -d "$NL1C6D2N_CLASS_ROOT/.git" \
        && -f "$NL1C6D2N_CLASS_ROOT/source/aest_memory.c" \
        && -f "$NL1C6D2N_CLASS_ROOT/include/perturbations.h" \
        && -n "${NL1C6D2N_PYTARGET:-}" && -f "$NL1C6D2N_PYTARGET/classy/__init__.py" \
        && "${FULLJ_DENSE_RESIDUAL_R2_CLASS_KFILE_LIMIT:-}" == "64" ]] \
        && grep -Eq '^#define[[:space:]]+_MAX_NUMBER_OF_K_FILES_[[:space:]]+64[[:space:]]*$' \
             "$NL1C6D2N_CLASS_ROOT/include/perturbations.h"; then
    reuse=1
  fi
fi
if [[ "$reuse" -eq 1 ]]; then
  echo "FULLJ_DENSE_RESIDUAL_R2: reusing isolated corrected CLASS dense-k64 environment..."
else
  echo "FULLJ_DENSE_RESIDUAL_R2: preparing isolated corrected CLASS dense-k64 environment..."
  bash fullj_weyl/setup_corrected_class_dense_k64_local.sh
  # shellcheck disable=SC1090
  source "$ENVFILE"
fi

grep -Eq '^#define[[:space:]]+_MAX_NUMBER_OF_K_FILES_[[:space:]]+64[[:space:]]*$' \
  "$NL1C6D2N_CLASS_ROOT/include/perturbations.h"
[[ "${FULLJ_DENSE_RESIDUAL_R2_CLASS_KFILE_LIMIT:-}" == "64" ]]
echo "FULLJ_DENSE_RESIDUAL_R2_CLASS_KFILE_LIMIT_PASS value=64"

python - <<'PY'
import os, numpy, scipy, classy
from classy import Class
print('FULLJ_DENSE_RESIDUAL_R2_ENV_PASS')
print('numpy='+numpy.__version__)
print('scipy='+scipy.__version__)
print('classy_module='+str(classy.__file__))
print('NL1C6D2N_CLASS_ROOT='+os.environ['NL1C6D2N_CLASS_ROOT'])
print('FULLJ_DENSE_RESIDUAL_R2_CLASS_KFILE_LIMIT='+os.environ['FULLJ_DENSE_RESIDUAL_R2_CLASS_KFILE_LIMIT'])
c=Class(); c.empty()
PY

JSON="results/fullj_dense_radial_class_residual_r2.json"
NPZ="results/fullj_dense_radial_class_residual_r2.npz"
CSV="results/fullj_dense_radial_class_residual_r2.csv"
LOG="results/fullj_dense_radial_class_residual_r2.log"
ZIP="results/fullj_dense_radial_class_residual_r2_bundle.zip"
rm -f "$JSON" "$NPZ" "$CSV" "$LOG" "$ZIP"

export OMP_NUM_THREADS=1
unset AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE AEST_OFFLINE_TRACE_FILE AEST_TANGENT_ALLOW_K_MISS || true

set +e
python -u -m fullj_weyl.dense_radial_class_residual_r2_r1 \
  --json-out "$JSON" --npz-out "$NPZ" --csv-out "$CSV" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

python - "$ZIP" "$LOG" "$JSON" "$NPZ" "$CSV" <<'PY'
from pathlib import Path
import sys, zipfile
zp=Path(sys.argv[1])
paths=[Path(x) for x in sys.argv[2:]] + [
    Path('docs/fullj_dense_radial_weyl_extension_result.md'),
    Path('docs/fullj_dense_radial_class_residual_r2_predata.md'),
    Path('docs/fullj_dense_radial_class_residual_r2_provenance_repair.md'),
    Path('docs/fullj_dense_radial_class_residual_r2_kfile_limit_repair.md'),
    Path('fullj_weyl/apply_class_kfile_limit_patch.py'),
    Path('fullj_weyl/setup_corrected_class_dense_k64_local.sh'),
    Path('fullj_weyl/dense_radial_class_residual_r2.py'),
    Path('fullj_weyl/dense_radial_class_residual_r2_r1.py'),
    Path('fullj_weyl/dense_radial_weyl_extension_r1.py'),
    Path('fullj_weyl/run_local_dense_radial_class_residual_r2.sh'),
    Path('results/fullj_dense_radial_weyl_extension.json'),
    Path('results/nl1c6d2n_corrected_class_densek64_env.sh'),
]
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED) as zf:
    seen=set()
    for p in paths:
        if p.exists() and p not in seen:
            zf.write(p,arcname=str(p)); seen.add(p)
print('FULLJ_DENSE_RESIDUAL_R2_BUNDLE='+str(zp))
PY

echo "FULLJ_DENSE_RESIDUAL_R2_EXIT=$code"
echo "FULLJ_DENSE_RESIDUAL_R2_LOG=$LOG"
echo "FULLJ_DENSE_RESIDUAL_R2_JSON=$JSON"
echo "FULLJ_DENSE_RESIDUAL_R2_NPZ=$NPZ"
echo "FULLJ_DENSE_RESIDUAL_R2_CSV=$CSV"
echo "FULLJ_DENSE_RESIDUAL_R2_ZIP=$ZIP"
exit "$code"
