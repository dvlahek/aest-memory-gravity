#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

BASE_PY=""
if command -v python3 >/dev/null 2>&1; then BASE_PY="$(command -v python3)"; elif command -v python >/dev/null 2>&1; then BASE_PY="$(command -v python)"; else echo "ACT_DR6_R9: python missing" >&2; exit 2; fi
VENV="$ROOT/.local/act_dr6_lensing_venv"
if [[ ! -x "$VENV/bin/python" ]]; then "$BASE_PY" -m venv "$VENV" || { echo "ACT_DR6_R9: install python3-venv" >&2; exit 2; }; fi
export PATH="$VENV/bin:$PATH"
python -m pip install --upgrade pip setuptools wheel >/dev/null
python -m pip install numpy scipy cython "act_dr6_lenslike==1.2.1" >/dev/null

need_setup=0
if [[ ! -f results/c3_r5_class_env.sh ]]; then need_setup=1; else source results/c3_r5_class_env.sh; [[ -n "${C3_R5_CLASS_ROOT:-}" && -d "$C3_R5_CLASS_ROOT" ]] || need_setup=1; fi
if [[ "$need_setup" -eq 1 ]]; then
  echo "ACT_DR6_R9: preparing pinned zero-safe finite-memory CLASS..."
  bash nl1c6d2c6c_r5/setup_zero_safe_class.sh
  source results/c3_r5_class_env.sh
else
  echo "ACT_DR6_R9: reusing CLASS source tree at ${C3_R5_CLASS_ROOT}"
fi

echo "ACT_DR6_R9: building CLASS executable..."
make -C "$C3_R5_CLASS_ROOT" -j2 class >/dev/null
test -x "$C3_R5_CLASS_ROOT/class"
export OMP_NUM_THREADS=1
unset AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE AEST_OFFLINE_TRACE_FILE || true

python - <<'PY'
import importlib.metadata as md
import act_dr6_lenslike as alike
v=md.version('act-dr6-lenslike'); print('ACT_DR6_PACKAGE_VERSION='+v)
if v!='1.2.1': raise SystemExit('unexpected act_dr6_lenslike version '+v)
alike.get_data(version='v1.2')
d=alike.load_data('act_baseline',lens_only=True,like_corrections=False,trim_lmax=2998,version='v1.2')
print('ACT_DR6_DATA_READY bins='+str(len(d['data_binned_clkk'])))
PY

python -m py_compile obs_act_dr6_lensing/act_dr6_direct_los_certified_r9.py
LOG="results/act_dr6_lensing_exploratory_r9_direct_los_certified_eta_scan.log"
JSON="results/act_dr6_lensing_exploratory_r9_direct_los_certified_eta_scan.json"
NPZ="results/act_dr6_lensing_exploratory_r9_direct_los_certified_eta_scan.npz"
ZIP="results/act_dr6_lensing_exploratory_r9_direct_los_certified_eta_scan_bundle.zip"
rm -f "$LOG" "$JSON" "$NPZ" "$ZIP" results/act_dr6_r9_class_*.log results/act_dr6_r9_*__cl.dat results/act_dr6_r9_*.ini results/act_dr6_r9_*.pre

set +e
python -u obs_act_dr6_lensing/act_dr6_direct_los_certified_r9.py --class-root "$C3_R5_CLASS_ROOT" --json-out "$JSON" --npz-out "$NPZ" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

python - "$ZIP" "$LOG" "$JSON" "$NPZ" <<'PY'
from pathlib import Path
import sys, zipfile
zp=Path(sys.argv[1]); paths=[Path(sys.argv[2]),Path(sys.argv[3]),Path(sys.argv[4])]
paths += sorted(Path('results').glob('act_dr6_r9_class_*.log'))
paths += sorted(Path('results').glob('act_dr6_r9_*__cl.dat'))
paths += sorted(Path('results').glob('act_dr6_r9_*.ini'))
paths += sorted(Path('results').glob('act_dr6_r9_*.pre'))
paths += [Path('docs/obs_act_dr6_lensing_exploratory_r9_direct_los_certified_predata.md'),Path('obs_act_dr6_lensing/act_dr6_direct_los_certified_r9.py'),Path('obs_act_dr6_lensing/run_local_r9.sh'),Path('v019p/pre/p3.pre')]
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED) as zf:
    seen=set()
    for p in paths:
        if p.exists() and p not in seen: zf.write(p,arcname=str(p)); seen.add(p)
print('ACT_DR6_R9_BUNDLE='+str(zp))
PY

echo "ACT_DR6_R9_EXIT=$code"
echo "ACT_DR6_R9_LOG=$LOG"
echo "ACT_DR6_R9_JSON=$JSON"
echo "ACT_DR6_R9_NPZ=$NPZ"
echo "ACT_DR6_R9_ZIP=$ZIP"
exit "$code"
