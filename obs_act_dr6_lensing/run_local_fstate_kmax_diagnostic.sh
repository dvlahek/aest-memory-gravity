#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

BASE_PY=""
if command -v python3 >/dev/null 2>&1; then BASE_PY="$(command -v python3)"; elif command -v python >/dev/null 2>&1; then BASE_PY="$(command -v python)"; else echo "KDIAG: python missing" >&2; exit 2; fi
VENV="$ROOT/.local/fstate_kmax_diag_venv"
if [[ ! -x "$VENV/bin/python" ]]; then "$BASE_PY" -m venv "$VENV" || { echo "KDIAG: install python3-venv" >&2; exit 2; }; fi
export PATH="$VENV/bin:$PATH"
python -m pip install --upgrade pip setuptools wheel >/dev/null
python -m pip install numpy cython >/dev/null

echo "KDIAG: preparing isolated nonredundant F-state CLASS tree..."
bash act_fstate/setup_fstate_class.sh
# shellcheck disable=SC1091
source results/act_fstate_class_env.sh

echo "KDIAG: CLASS_ROOT=$FSTATE_CLASS_ROOT"
test -x "$FSTATE_CLASS_ROOT/class"
python -m py_compile obs_act_dr6_lensing/act_dr6_fstate_kmax_diagnostic.py

LOG="results/act_dr6_fstate_kmax_diagnostic.log"
JSON="results/act_dr6_fstate_kmax_diagnostic.json"
NPZ="results/act_dr6_fstate_kmax_diagnostic.npz"
ZIP="results/act_dr6_fstate_kmax_diagnostic_bundle.zip"
rm -f "$LOG" "$JSON" "$NPZ" "$ZIP" \
  results/act_dr6_fs_kdiag_class_*.log results/act_dr6_fs_kdiag_*__cl.dat \
  results/act_dr6_fs_kdiag_*.ini results/act_dr6_fs_kdiag_*.pre

export OMP_NUM_THREADS=1
unset AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE AEST_OFFLINE_TRACE_FILE AEST_TANGENT_ALLOW_K_MISS || true

set +e
python -u obs_act_dr6_lensing/act_dr6_fstate_kmax_diagnostic.py \
  --class-root "$FSTATE_CLASS_ROOT" --json-out "$JSON" --npz-out "$NPZ" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

python - "$ZIP" "$LOG" "$JSON" "$NPZ" <<'PY'
from pathlib import Path
import sys, zipfile
zp=Path(sys.argv[1]); paths=[Path(sys.argv[2]),Path(sys.argv[3]),Path(sys.argv[4])]
paths += sorted(Path('results').glob('act_dr6_fs_kdiag_class_*.log'))
paths += sorted(Path('results').glob('act_dr6_fs_kdiag_*__cl.dat'))
paths += sorted(Path('results').glob('act_dr6_fs_kdiag_*.ini'))
paths += sorted(Path('results').glob('act_dr6_fs_kdiag_*.pre'))
paths += [Path('results/act_fstate_apply_report.json'),
          Path('docs/obs_act_dr6_fstate_kmax_diagnostic_predata.md'),
          Path('obs_act_dr6_lensing/act_dr6_fstate_kmax_diagnostic.py'),
          Path('obs_act_dr6_lensing/run_local_fstate_kmax_diagnostic.sh'),
          Path('act_fstate/apply_fstate_patch.py'),
          Path('act_fstate/setup_fstate_class.sh'),Path('v019p/pre/p3.pre')]
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED) as zf:
    seen=set()
    for p in paths:
        if p.exists() and p not in seen:
            zf.write(p,arcname=str(p)); seen.add(p)
print('KDIAG_BUNDLE='+str(zp))
PY

echo "KDIAG_EXIT=$code"
echo "KDIAG_LOG=$LOG"
echo "KDIAG_JSON=$JSON"
echo "KDIAG_NPZ=$NPZ"
echo "KDIAG_ZIP=$ZIP"
exit "$code"
