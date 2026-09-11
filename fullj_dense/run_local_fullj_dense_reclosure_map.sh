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
  echo "FULLJ_DENSE: python missing" >&2
  exit 2
fi

VENV="$ROOT/.local/fullj_dense_reclosure_venv"
if [[ ! -x "$VENV/bin/python" ]]; then
  "$BASE_PY" -m venv "$VENV" || { echo "FULLJ_DENSE: install python3-venv" >&2; exit 2; }
fi
export PATH="$VENV/bin:$PATH"
python -m pip install --upgrade pip setuptools wheel >/dev/null
python -m pip install numpy scipy cython >/dev/null

python -m py_compile \
  fullj_dense/dense_reclosure_map.py \
  fullj_poc/cosmological_reclosure_poc.py \
  nl1c6/full_j_baryonic_reclosure.py

echo "FULLJ_DENSE: preparing pinned nonredundant F-state CLASS source extractor..."
bash act_fstate/setup_fstate_class.sh
# shellcheck disable=SC1091
source results/act_fstate_class_env.sh

test -x "$FSTATE_CLASS_ROOT/class"
python - <<'PY'
import numpy, scipy
from classy import Class
import classy
print('FULLJ_DENSE_ENV_PASS')
print('numpy='+numpy.__version__)
print('scipy='+scipy.__version__)
print('classy_module='+str(classy.__file__))
c=Class(); c.empty()
PY

LOG="results/fullj_dense_reclosure_map.log"
JSON="results/fullj_dense_reclosure_map.json"
NPZ="results/fullj_dense_reclosure_map.npz"
CSV="results/fullj_dense_reclosure_map.csv"
AGG="results/fullj_dense_reclosure_kernel_median.csv"
ZIP="results/fullj_dense_reclosure_map_bundle.zip"
rm -f "$LOG" "$JSON" "$NPZ" "$CSV" "$AGG" "$ZIP"

export OMP_NUM_THREADS=1
unset AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE AEST_OFFLINE_TRACE_FILE AEST_TANGENT_ALLOW_K_MISS || true

set +e
python -u fullj_dense/dense_reclosure_map.py \
  --json-out "$JSON" \
  --npz-out "$NPZ" \
  --csv-out "$CSV" \
  --aggregate-csv-out "$AGG" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

python - "$ZIP" "$LOG" "$JSON" "$NPZ" "$CSV" "$AGG" <<'PY'
from pathlib import Path
import sys, zipfile
zp=Path(sys.argv[1])
paths=[Path(x) for x in sys.argv[2:]] + [
    Path('docs/fullj_dense_reclosure_map_predata.md'),
    Path('fullj_dense/dense_reclosure_map.py'),
    Path('fullj_dense/run_local_fullj_dense_reclosure_map.sh'),
    Path('fullj_poc/cosmological_reclosure_poc.py'),
    Path('docs/fullj_cosmological_reclosure_poc_predata.md'),
    Path('nl1c6/full_j_baryonic_reclosure.py'),
    Path('docs/nl1c6_predata_full_j_baryonic_reclosure.md'),
    Path('docs/nl1c6r_solver_globalization_repair_result.md'),
    Path('results/act_fstate_apply_report.json'),
]
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED) as zf:
    seen=set()
    for p in paths:
        if p.exists() and p not in seen:
            zf.write(p,arcname=str(p)); seen.add(p)
print('FULLJ_DENSE_BUNDLE='+str(zp))
PY

echo "FULLJ_DENSE_EXIT=$code"
echo "FULLJ_DENSE_LOG=$LOG"
echo "FULLJ_DENSE_JSON=$JSON"
echo "FULLJ_DENSE_NPZ=$NPZ"
echo "FULLJ_DENSE_CSV=$CSV"
echo "FULLJ_DENSE_AGGREGATE_CSV=$AGG"
echo "FULLJ_DENSE_ZIP=$ZIP"
exit "$code"
