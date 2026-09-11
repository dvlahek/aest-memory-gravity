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
  echo "FULLJ_PHASE: python missing" >&2
  exit 2
fi

VENV="$ROOT/.local/fullj_phase_venv"
if [[ ! -x "$VENV/bin/python" ]]; then
  "$BASE_PY" -m venv "$VENV" || { echo "FULLJ_PHASE: install python3-venv" >&2; exit 2; }
fi
export PATH="$VENV/bin:$PATH"
python -m pip install --upgrade pip setuptools wheel >/dev/null
python -m pip install numpy scipy cython >/dev/null

python -m py_compile \
  fullj_weyl/phase_robustness.py \
  fullj_jacobian/mode_coupling_jacobian.py \
  fullj_dense/dense_reclosure_map.py \
  fullj_poc/cosmological_reclosure_poc.py \
  nl1c6/full_j_baryonic_reclosure.py

echo "FULLJ_PHASE: preparing pinned nonredundant F-state CLASS source extractor..."
bash act_fstate/setup_fstate_class.sh
# shellcheck disable=SC1091
source results/act_fstate_class_env.sh

test -x "$FSTATE_CLASS_ROOT/class"
python - <<'PY'
import numpy, scipy
from classy import Class
import classy
print('FULLJ_PHASE_ENV_PASS')
print('numpy='+numpy.__version__)
print('scipy='+scipy.__version__)
print('classy_module='+str(classy.__file__))
c=Class(); c.empty()
PY

LOCKED="results/fullj_mode_coupling_jacobian.json"
JSON="results/fullj_phase_robustness.json"
CSV="results/fullj_phase_robustness_summary.csv"
LOG="results/fullj_phase_robustness.log"
ZIP="results/fullj_phase_robustness_bundle.zip"

if [[ ! -f "$LOCKED" ]]; then
  echo "FULLJ_PHASE: locked Jacobian JSON missing: $LOCKED" >&2
  exit 2
fi
rm -f "$JSON" "$CSV" "$LOG" "$ZIP"

export OMP_NUM_THREADS=1
unset AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE AEST_OFFLINE_TRACE_FILE AEST_TANGENT_ALLOW_K_MISS || true

set +e
python -u fullj_weyl/phase_robustness.py \
  --locked-json "$LOCKED" \
  --json-out "$JSON" \
  --csv-out "$CSV" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

python - "$ZIP" "$LOG" "$JSON" "$CSV" <<'PY'
from pathlib import Path
import sys, zipfile
zp=Path(sys.argv[1])
paths=[Path(x) for x in sys.argv[2:]] + [
    Path('docs/fullj_phase_robustness_predata.md'),
    Path('docs/fullj_mode_coupling_jacobian_LOCKED_RESULT.md'),
    Path('docs/fullj_weyl_lensing_closure_audit.md'),
    Path('docs/fullj_local_weyl_covariance_result.md'),
    Path('fullj_weyl/phase_robustness.py'),
    Path('fullj_weyl/run_local_phase_robustness.sh'),
    Path('fullj_jacobian/mode_coupling_jacobian.py'),
    Path('fullj_dense/dense_reclosure_map.py'),
    Path('fullj_poc/cosmological_reclosure_poc.py'),
    Path('nl1c6/full_j_baryonic_reclosure.py'),
    Path('results/act_fstate_apply_report.json'),
]
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED) as zf:
    seen=set()
    for p in paths:
        if p.exists() and p not in seen:
            zf.write(p,arcname=str(p)); seen.add(p)
print('FULLJ_PHASE_BUNDLE='+str(zp))
PY

echo "FULLJ_PHASE_EXIT=$code"
echo "FULLJ_PHASE_LOG=$LOG"
echo "FULLJ_PHASE_JSON=$JSON"
echo "FULLJ_PHASE_CSV=$CSV"
echo "FULLJ_PHASE_ZIP=$ZIP"
exit "$code"
