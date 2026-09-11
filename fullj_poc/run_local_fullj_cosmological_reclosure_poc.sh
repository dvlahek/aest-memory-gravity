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
  echo "FULLJ_POC: python missing" >&2
  exit 2
fi

VENV="$ROOT/.local/fullj_cosmo_poc_venv"
if [[ ! -x "$VENV/bin/python" ]]; then
  "$BASE_PY" -m venv "$VENV" || { echo "FULLJ_POC: install python3-venv" >&2; exit 2; }
fi
export PATH="$VENV/bin:$PATH"
python -m pip install --upgrade pip setuptools wheel >/dev/null
python -m pip install numpy scipy cython >/dev/null

python -m py_compile fullj_poc/cosmological_reclosure_poc.py nl1c6/full_j_baryonic_reclosure.py

echo "FULLJ_POC: preparing pinned nonredundant F-state CLASS source extractor..."
bash act_fstate/setup_fstate_class.sh
# shellcheck disable=SC1091
source results/act_fstate_class_env.sh

test -x "$FSTATE_CLASS_ROOT/class"
python - <<'PY'
import numpy, scipy
from classy import Class
import classy
print('FULLJ_POC_ENV_PASS')
print('numpy='+numpy.__version__)
print('scipy='+scipy.__version__)
print('classy_module='+str(classy.__file__))
c=Class(); c.empty()
PY

LOG="results/fullj_cosmological_reclosure_poc.log"
JSON="results/fullj_cosmological_reclosure_poc.json"
NPZ="results/fullj_cosmological_reclosure_poc.npz"
ZIP="results/fullj_cosmological_reclosure_poc_bundle.zip"
rm -f "$LOG" "$JSON" "$NPZ" "$ZIP"

export OMP_NUM_THREADS=1
unset AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE AEST_OFFLINE_TRACE_FILE AEST_TANGENT_ALLOW_K_MISS || true

set +e
python -u fullj_poc/cosmological_reclosure_poc.py \
  --json-out "$JSON" --npz-out "$NPZ" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

python - "$ZIP" "$LOG" "$JSON" "$NPZ" <<'PY'
from pathlib import Path
import sys, zipfile
zp=Path(sys.argv[1])
paths=[Path(sys.argv[2]),Path(sys.argv[3]),Path(sys.argv[4]),
       Path('docs/fullj_cosmological_reclosure_poc_predata.md'),
       Path('fullj_poc/cosmological_reclosure_poc.py'),
       Path('fullj_poc/run_local_fullj_cosmological_reclosure_poc.sh'),
       Path('nl1c6/full_j_baryonic_reclosure.py'),
       Path('nl1c6r/solver_globalization_repair.py'),
       Path('docs/nl1c6_predata_full_j_baryonic_reclosure.md'),
       Path('docs/nl1c6r_solver_globalization_repair_result.md'),
       Path('results/act_fstate_apply_report.json')]
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED) as zf:
    seen=set()
    for p in paths:
        if p.exists() and p not in seen:
            zf.write(p,arcname=str(p)); seen.add(p)
print('FULLJ_POC_BUNDLE='+str(zp))
PY

echo "FULLJ_POC_EXIT=$code"
echo "FULLJ_POC_LOG=$LOG"
echo "FULLJ_POC_JSON=$JSON"
echo "FULLJ_POC_NPZ=$NPZ"
echo "FULLJ_POC_ZIP=$ZIP"
exit "$code"
