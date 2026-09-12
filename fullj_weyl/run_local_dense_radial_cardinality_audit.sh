#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

BASE_PY=""
if command -v python3 >/dev/null 2>&1; then BASE_PY="$(command -v python3)";
elif command -v python >/dev/null 2>&1; then BASE_PY="$(command -v python)";
else echo "FULLJ_CARDINALITY: python missing" >&2; exit 2; fi

VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then
  "$BASE_PY" -m venv "$VENV" || { echo "FULLJ_CARDINALITY: install python3-venv" >&2; exit 2; }
fi
export PATH="$VENV/bin:$PATH"
python -m pip install --upgrade pip setuptools wheel >/dev/null
python -m pip install numpy scipy cython >/dev/null

python -m py_compile \
  fullj_weyl/dense_radial_cardinality_audit.py \
  fullj_weyl/dense_radial_class_residual_r2.py \
  fullj_weyl/dense_radial_class_residual_r2_r1.py \
  fullj_weyl/dense_radial_weyl_extension.py \
  fullj_weyl/dense_radial_weyl_extension_r1.py

if [[ ! -f results/fullj_dense_radial_weyl_extension.json ]]; then
  echo "FULLJ_CARDINALITY: missing locked dense FAIL JSON" >&2; exit 3
fi
if [[ ! -f results/fullj_dense_radial_class_residual_r2.json ]]; then
  echo "FULLJ_CARDINALITY: missing completed residual-R2 FAIL JSON" >&2; exit 3
fi

python - <<'PY'
import json
from pathlib import Path
from fullj_weyl import dense_radial_class_residual_r2_r1 as repaired
from fullj_weyl import dense_radial_cardinality_audit as aud

assert repaired.DENSE_RESIDUAL_R2_GAUSS_PROVENANCE_REPAIR_ACTIVE
assert repaired.base.densefix.DENSE_HISTORY_LOADER_REPAIR_ACTIVE
assert aud.K_AUDIT.tolist() == [0.035,0.04,0.1,0.15,0.1625,0.175]
_,k2,k3,h3 = repaired.base.grids()
assert (len(k2),len(k3),len(h3)) == (21,41,20)

d1=json.loads(Path('results/fullj_dense_radial_weyl_extension.json').read_text())
d2=json.loads(Path('results/fullj_dense_radial_class_residual_r2.json').read_text())
assert d1['classification']=='FULLJ_DENSE_RADIAL_WEYL_EXTENSION_FAIL'
assert d2['classification']=='FULLJ_DENSE_RADIAL_CLASS_RESIDUAL_R2_FAIL'
print('FULLJ_CARDINALITY_IMPORT_CHAIN_PASS')
print('FULLJ_CARDINALITY_LOCAL_LOCKS_PASS')
PY

ENVFILE="$ROOT/results/nl1c6d2n_corrected_class_densek64_env.sh"
reuse=0
if [[ -f "$ENVFILE" ]]; then
  # shellcheck disable=SC1090
  source "$ENVFILE"
  if [[ -n "${NL1C6D2N_CLASS_ROOT:-}" && -d "$NL1C6D2N_CLASS_ROOT/.git" \
        && -f "$NL1C6D2N_CLASS_ROOT/source/aest_memory.c" \
        && -f "$NL1C6D2N_CLASS_ROOT/include/perturbations.h" \
        && -n "${NL1C6D2N_PYTARGET:-}" && -f "$NL1C6D2N_PYTARGET/classy/__init__.py" \
        && "${FULLJ_DENSE_RESIDUAL_R2_CLASS_KFILE_LIMIT:-}" == "64" ]]; then
    reuse=1
  fi
fi

if [[ "$reuse" -eq 1 ]]; then
  echo "FULLJ_CARDINALITY: reusing isolated corrected CLASS dense-k64 environment..."
else
  echo "FULLJ_CARDINALITY: preparing isolated corrected CLASS dense-k64 environment..."
  bash fullj_weyl/setup_corrected_class_dense_k64_local.sh
  # shellcheck disable=SC1090
  source "$ENVFILE"
fi

grep -Eq '^#define[[:space:]]+_MAX_NUMBER_OF_K_FILES_[[:space:]]+64[[:space:]]*$' \
  "$NL1C6D2N_CLASS_ROOT/include/perturbations.h"

python - <<'PY'
import os, numpy, scipy, classy
from classy import Class
print('FULLJ_CARDINALITY_CLASS_KFILE_LIMIT_PASS value='+os.environ.get('FULLJ_DENSE_RESIDUAL_R2_CLASS_KFILE_LIMIT',''))
print('FULLJ_CARDINALITY_ENV_PASS')
print('numpy='+numpy.__version__)
print('scipy='+scipy.__version__)
print('classy_module='+str(classy.__file__))
print('NL1C6D2N_CLASS_ROOT='+os.environ['NL1C6D2N_CLASS_ROOT'])
c=Class(); c.empty()
PY

JSON="results/fullj_dense_radial_cardinality_audit.json"
NPZ="results/fullj_dense_radial_cardinality_audit.npz"
CSV="results/fullj_dense_radial_cardinality_audit.csv"
LOG="results/fullj_dense_radial_cardinality_audit.log"
ZIP="results/fullj_dense_radial_cardinality_audit_bundle.zip"
rm -f "$JSON" "$NPZ" "$CSV" "$LOG" "$ZIP"

export OMP_NUM_THREADS=1
unset AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE AEST_OFFLINE_TRACE_FILE AEST_TANGENT_ALLOW_K_MISS || true

set +e
python -u -m fullj_weyl.dense_radial_cardinality_audit \
  --json-out "$JSON" --npz-out "$NPZ" --csv-out "$CSV" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

python - "$ZIP" "$LOG" "$JSON" "$NPZ" "$CSV" <<'PY'
from pathlib import Path
import sys, zipfile
zp=Path(sys.argv[1])
paths=[Path(x) for x in sys.argv[2:]] + [
    Path('docs/fullj_dense_radial_class_residual_r2_result.md'),
    Path('docs/fullj_dense_radial_cardinality_audit_predata.md'),
    Path('fullj_weyl/dense_radial_cardinality_audit.py'),
    Path('fullj_weyl/run_local_dense_radial_cardinality_audit.sh'),
    Path('fullj_weyl/setup_corrected_class_dense_k64_local.sh'),
    Path('results/fullj_dense_radial_weyl_extension.json'),
    Path('results/fullj_dense_radial_class_residual_r2.json'),
    Path('results/nl1c6d2n_corrected_class_densek64_env.sh'),
]
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED) as zf:
    seen=set()
    for p in paths:
        if p.exists() and p not in seen:
            zf.write(p,arcname=str(p)); seen.add(p)
print('FULLJ_CARDINALITY_BUNDLE='+str(zp))
PY

echo "FULLJ_CARDINALITY_EXIT=$code"
echo "FULLJ_CARDINALITY_LOG=$LOG"
echo "FULLJ_CARDINALITY_JSON=$JSON"
echo "FULLJ_CARDINALITY_NPZ=$NPZ"
echo "FULLJ_CARDINALITY_CSV=$CSV"
echo "FULLJ_CARDINALITY_ZIP=$ZIP"
exit "$code"
