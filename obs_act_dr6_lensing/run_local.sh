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
  echo "ACT_DR6: neither python3 nor python is installed" >&2
  exit 2
fi

VENV="$ROOT/.local/act_dr6_lensing_venv"
if [[ ! -x "$VENV/bin/python" ]]; then
  "$BASE_PY" -m venv "$VENV" || {
    echo "ACT_DR6: Python venv support missing; install python3-venv" >&2
    exit 2
  }
fi
export PATH="$VENV/bin:$PATH"

python -m pip install --upgrade pip setuptools wheel >/dev/null
python -m pip install numpy scipy cython "act_dr6_lenslike==1.2.1"

need_setup=0
if [[ ! -f results/c3_r5_class_env.sh ]]; then
  need_setup=1
else
  # shellcheck disable=SC1091
  source results/c3_r5_class_env.sh
  if [[ -z "${C3_R5_PYTARGET:-}" || ! -d "${C3_R5_PYTARGET}" || -z "${C3_R5_CLASS_ROOT:-}" || ! -d "${C3_R5_CLASS_ROOT}" ]]; then
    need_setup=1
  fi
fi

if [[ "$need_setup" -eq 1 ]]; then
  echo "ACT_DR6: building pinned zero-safe AeST+memory CLASS..."
  bash nl1c6d2c6c_r5/setup_zero_safe_class.sh
  # shellcheck disable=SC1091
  source results/c3_r5_class_env.sh
else
  echo "ACT_DR6: reusing CLASS at ${C3_R5_CLASS_ROOT}"
fi

# Ensure local repository modules and the isolated modified classy are first.
export PYTHONPATH="$ROOT:${C3_R5_PYTARGET}${PYTHONPATH:+:$PYTHONPATH}"
export OMP_NUM_THREADS=1
unset AEST_TANGENT_FORCE_FILE || true
unset AEST_TANGENT_LAMBDA || true
unset AEST_TANGENT_TRACE_FILE || true

python - <<'PY'
import importlib.metadata as md
from classy import Class
import act_dr6_lenslike as alike
v=md.version('act-dr6-lenslike')
print('ACT_DR6_PACKAGE_VERSION=',v)
if v != '1.2.1':
    raise SystemExit('unexpected act_dr6_lenslike version '+v)
c=Class(); c.empty()
print('ACT_DR6_CLASSY_IMPORT_PASS')
# Official package downloads the default LAMBDA v1.2 dataset into its package data directory.
alike.get_data(version='v1.2')
print('ACT_DR6_DATA_READY')
PY

python -m py_compile obs_act_dr6_lensing/act_dr6_exploratory_scan.py

LOG="results/act_dr6_lensing_exploratory.log"
JSON="results/act_dr6_lensing_exploratory.json"
NPZ="results/act_dr6_lensing_exploratory.npz"
ZIP="results/act_dr6_lensing_exploratory_bundle.zip"
rm -f "$LOG" "$JSON" "$NPZ" "$ZIP"

set +e
python -u obs_act_dr6_lensing/act_dr6_exploratory_scan.py \
  --json-out "$JSON" --npz-out "$NPZ" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

python - "$ZIP" "$LOG" "$JSON" "$NPZ" <<'PY'
from pathlib import Path
import sys, zipfile
zip_path=Path(sys.argv[1])
paths=[
    Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4]),
    Path('docs/obs_act_dr6_lensing_exploratory_scope.md'),
    Path('obs_act_dr6_lensing/act_dr6_exploratory_scan.py'),
    Path('obs_act_dr6_lensing/run_local.sh'),
    Path('obs_act_dr6_lensing/README_LOCAL.md'),
    Path('docs/nl1c6d2c6h_final_self_consistent_metric_feedback_predata.md'),
]
with zipfile.ZipFile(zip_path,'w',compression=zipfile.ZIP_DEFLATED) as zf:
    for p in paths:
        if p.exists():
            zf.write(p,arcname=str(p))
print(f'ACT_DR6_BUNDLE={zip_path}')
PY

echo "ACT_DR6_EXIT=$code"
echo "ACT_DR6_LOG=$LOG"
echo "ACT_DR6_JSON=$JSON"
echo "ACT_DR6_NPZ=$NPZ"
echo "ACT_DR6_ZIP=$ZIP"
exit "$code"
