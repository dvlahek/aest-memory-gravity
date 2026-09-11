#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

BASE_PY=""
if command -v python3 >/dev/null 2>&1; then BASE_PY="$(command -v python3)"; elif command -v python >/dev/null 2>&1; then BASE_PY="$(command -v python)"; else echo "FSTATE: python missing" >&2; exit 2; fi
VENV="$ROOT/.local/act_dr6_lensing_venv"
if [[ ! -x "$VENV/bin/python" ]]; then "$BASE_PY" -m venv "$VENV" || { echo "FSTATE: install python3-venv" >&2; exit 2; }; fi
export PATH="$VENV/bin:$PATH"
python -m pip install --upgrade pip setuptools wheel >/dev/null
python -m pip install numpy scipy cython "act_dr6_lenslike==1.2.1" >/dev/null

echo "FSTATE: preparing isolated nonredundant CLASS tree..."
bash act_fstate/setup_fstate_class.sh
# shellcheck disable=SC1091
source results/act_fstate_class_env.sh

echo "FSTATE: CLASS_ROOT=$FSTATE_CLASS_ROOT"
test -x "$FSTATE_CLASS_ROOT/class"

python - <<'PY'
import importlib.metadata as md
import act_dr6_lenslike as alike
v=md.version('act-dr6-lenslike')
print('ACT_DR6_PACKAGE_VERSION='+v)
if v!='1.2.1': raise SystemExit('unexpected act_dr6_lenslike version '+v)
alike.get_data(version='v1.2')
d=alike.load_data('act_baseline',lens_only=True,like_corrections=False,trim_lmax=2998,version='v1.2')
print('ACT_DR6_DATA_READY bins='+str(len(d['data_binned_clkk'])))
PY

python -m py_compile act_fstate/apply_fstate_patch.py obs_act_dr6_lensing/act_dr6_fstate_final_scan.py

LOG="results/act_dr6_fstate_certified_eta_scan.log"
JSON="results/act_dr6_fstate_certified_eta_scan.json"
NPZ="results/act_dr6_fstate_certified_eta_scan.npz"
ZIP="results/act_dr6_fstate_certified_eta_scan_bundle.zip"
rm -f "$LOG" "$JSON" "$NPZ" "$ZIP" \
  results/act_dr6_fs_class_*.log results/act_dr6_fs_*__cl.dat \
  results/act_dr6_fs_*.ini results/act_dr6_fs_*.pre

export OMP_NUM_THREADS=1
unset AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE AEST_OFFLINE_TRACE_FILE AEST_TANGENT_ALLOW_K_MISS || true

set +e
python -u obs_act_dr6_lensing/act_dr6_fstate_final_scan.py \
  --class-root "$FSTATE_CLASS_ROOT" --json-out "$JSON" --npz-out "$NPZ" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

python - "$ZIP" "$LOG" "$JSON" "$NPZ" <<'PY'
from pathlib import Path
import sys,zipfile
zp=Path(sys.argv[1]); paths=[Path(sys.argv[2]),Path(sys.argv[3]),Path(sys.argv[4])]
paths += sorted(Path('results').glob('act_dr6_fs_class_*.log'))
paths += sorted(Path('results').glob('act_dr6_fs_*__cl.dat'))
paths += sorted(Path('results').glob('act_dr6_fs_*.ini'))
paths += sorted(Path('results').glob('act_dr6_fs_*.pre'))
paths += [Path('results/act_fstate_apply_report.json'),
          Path('docs/obs_act_dr6_fstate_production_fix_predata.md'),
          Path('act_fstate/apply_fstate_patch.py'),
          Path('act_fstate/setup_fstate_class.sh'),
          Path('obs_act_dr6_lensing/act_dr6_fstate_final_scan.py'),
          Path('obs_act_dr6_lensing/run_local_fstate.sh'),Path('v019p/pre/p3.pre')]
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED) as zf:
    seen=set()
    for p in paths:
        if p.exists() and p not in seen:
            zf.write(p,arcname=str(p)); seen.add(p)
print('FSTATE_BUNDLE='+str(zp))
PY

echo "FSTATE_EXIT=$code"
echo "FSTATE_LOG=$LOG"
echo "FSTATE_JSON=$JSON"
echo "FSTATE_NPZ=$NPZ"
echo "FSTATE_ZIP=$ZIP"
exit "$code"
