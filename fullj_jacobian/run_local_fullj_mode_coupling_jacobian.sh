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
  echo "FULLJ_JAC: python missing" >&2
  exit 2
fi

VENV="$ROOT/.local/fullj_jacobian_venv"
if [[ ! -x "$VENV/bin/python" ]]; then
  "$BASE_PY" -m venv "$VENV" || { echo "FULLJ_JAC: install python3-venv" >&2; exit 2; }
fi
export PATH="$VENV/bin:$PATH"
python -m pip install --upgrade pip setuptools wheel >/dev/null
python -m pip install numpy scipy cython >/dev/null

python -m py_compile \
  fullj_jacobian/mode_coupling_jacobian.py \
  fullj_jacobian/mode_coupling_jacobian_densefix.py \
  fullj_dense/dense_reclosure_map.py \
  fullj_poc/cosmological_reclosure_poc.py \
  nl1c6/full_j_baryonic_reclosure.py

echo "FULLJ_JAC: preparing pinned nonredundant F-state CLASS source extractor..."
bash act_fstate/setup_fstate_class.sh
# shellcheck disable=SC1091
source results/act_fstate_class_env.sh

test -x "$FSTATE_CLASS_ROOT/class"
python - <<'PY'
import numpy, scipy
from classy import Class
import classy
print('FULLJ_JAC_ENV_PASS')
print('numpy='+numpy.__version__)
print('scipy='+scipy.__version__)
print('classy_module='+str(classy.__file__))
c=Class(); c.empty()
PY

LOG="results/fullj_mode_coupling_jacobian.log"
JSON="results/fullj_mode_coupling_jacobian.json"
NPZ="results/fullj_mode_coupling_jacobian.npz"
MCSV="results/fullj_mode_coupling_jacobian_matrix.csv"
SCSV="results/fullj_mode_coupling_jacobian_summary.csv"
ZIP="results/fullj_mode_coupling_jacobian_bundle.zip"
rm -f "$LOG" "$JSON" "$NPZ" "$MCSV" "$SCSV" "$ZIP"

export OMP_NUM_THREADS=1
unset AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE AEST_OFFLINE_TRACE_FILE AEST_TANGENT_ALLOW_K_MISS || true

set +e
python -u fullj_jacobian/mode_coupling_jacobian_densefix.py \
  --json-out "$JSON" \
  --npz-out "$NPZ" \
  --matrix-csv-out "$MCSV" \
  --summary-csv-out "$SCSV" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

python - "$ZIP" "$LOG" "$JSON" "$NPZ" "$MCSV" "$SCSV" <<'PY'
from pathlib import Path
import sys, zipfile
zp=Path(sys.argv[1])
paths=[Path(x) for x in sys.argv[2:]] + [
    Path('docs/fullj_mode_coupling_jacobian_predata.md'),
    Path('docs/fullj_mode_coupling_jacobian_dense_background_fix.md'),
    Path('fullj_jacobian/mode_coupling_jacobian.py'),
    Path('fullj_jacobian/mode_coupling_jacobian_densefix.py'),
    Path('fullj_jacobian/run_local_fullj_mode_coupling_jacobian.sh'),
    Path('fullj_dense/dense_reclosure_map.py'),
    Path('docs/fullj_dense_reclosure_map_predata.md'),
    Path('fullj_poc/cosmological_reclosure_poc.py'),
    Path('nl1c6/full_j_baryonic_reclosure.py'),
    Path('results/act_fstate_apply_report.json'),
]
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED) as zf:
    seen=set()
    for p in paths:
        if p.exists() and p not in seen:
            zf.write(p,arcname=str(p)); seen.add(p)
print('FULLJ_JAC_BUNDLE='+str(zp))
PY

echo "FULLJ_JAC_EXIT=$code"
echo "FULLJ_JAC_LOG=$LOG"
echo "FULLJ_JAC_JSON=$JSON"
echo "FULLJ_JAC_NPZ=$NPZ"
echo "FULLJ_JAC_MATRIX_CSV=$MCSV"
echo "FULLJ_JAC_SUMMARY_CSV=$SCSV"
echo "FULLJ_JAC_ZIP=$ZIP"
exit "$code"
