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
  echo "ACT_DR6_R8: neither python3 nor python is installed" >&2
  exit 2
fi

VENV="$ROOT/.local/act_dr6_lensing_venv"
if [[ ! -x "$VENV/bin/python" ]]; then
  "$BASE_PY" -m venv "$VENV" || {
    echo "ACT_DR6_R8: Python venv support missing; install python3-venv" >&2
    exit 2
  }
fi
export PATH="$VENV/bin:$PATH"
python -m pip install --upgrade pip setuptools wheel >/dev/null
python -m pip install numpy >/dev/null

need_setup=0
if [[ ! -f results/c3_r5_class_env.sh ]]; then
  need_setup=1
else
  # shellcheck disable=SC1091
  source results/c3_r5_class_env.sh
  if [[ -z "${C3_R5_CLASS_ROOT:-}" || ! -d "${C3_R5_CLASS_ROOT}" ]]; then
    need_setup=1
  fi
fi
if [[ "$need_setup" -eq 1 ]]; then
  echo "ACT_DR6_R8: preparing pinned zero-safe finite-memory CLASS source tree..."
  bash nl1c6d2c6c_r5/setup_zero_safe_class.sh
  # shellcheck disable=SC1091
  source results/c3_r5_class_env.sh
else
  echo "ACT_DR6_R8: reusing CLASS source tree at ${C3_R5_CLASS_ROOT}"
fi

echo "ACT_DR6_R8: building CLASS executable..."
make -C "$C3_R5_CLASS_ROOT" -j2 class >/dev/null
test -x "$C3_R5_CLASS_ROOT/class"

export OMP_NUM_THREADS=1
unset AEST_TANGENT_FORCE_FILE || true
unset AEST_TANGENT_LAMBDA || true
unset AEST_TANGENT_TRACE_FILE || true
unset AEST_OFFLINE_TRACE_FILE || true

python -m py_compile obs_act_dr6_lensing/act_dr6_limber_switch_localization_r8.py

LOG="results/act_dr6_lensing_exploratory_r8_limber_switch_localization.log"
JSON="results/act_dr6_lensing_exploratory_r8_limber_switch_localization.json"
NPZ="results/act_dr6_lensing_exploratory_r8_limber_switch_localization.npz"
ZIP="results/act_dr6_lensing_exploratory_r8_limber_switch_localization_bundle.zip"
rm -f "$LOG" "$JSON" "$NPZ" "$ZIP" \
  results/act_dr6_r8_class_*.log \
  results/act_dr6_r8_*__cl.dat \
  results/act_dr6_r8_*.ini

set +e
python -u obs_act_dr6_lensing/act_dr6_limber_switch_localization_r8.py \
  --class-root "$C3_R5_CLASS_ROOT" \
  --json-out "$JSON" --npz-out "$NPZ" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

python - "$ZIP" "$LOG" "$JSON" "$NPZ" <<'PY'
from pathlib import Path
import sys, zipfile
zip_path=Path(sys.argv[1])
paths=[Path(sys.argv[2]),Path(sys.argv[3]),Path(sys.argv[4])]
paths += sorted(Path('results').glob('act_dr6_r8_class_*.log'))
paths += sorted(Path('results').glob('act_dr6_r8_*__cl.dat'))
paths += sorted(Path('results').glob('act_dr6_r8_*.ini'))
paths += [
    Path('docs/obs_act_dr6_lensing_exploratory_r8_limber_switch_localization_predata.md'),
    Path('obs_act_dr6_lensing/act_dr6_limber_switch_localization_r8.py'),
    Path('obs_act_dr6_lensing/run_local_r8.sh'),
    Path('v019p/pre/p3.pre'),
]
with zipfile.ZipFile(zip_path,'w',compression=zipfile.ZIP_DEFLATED) as zf:
    seen=set()
    for p in paths:
        if p.exists() and p not in seen:
            zf.write(p,arcname=str(p)); seen.add(p)
print(f'ACT_DR6_R8_BUNDLE={zip_path}')
PY

echo "ACT_DR6_R8_EXIT=$code"
echo "ACT_DR6_R8_LOG=$LOG"
echo "ACT_DR6_R8_JSON=$JSON"
echo "ACT_DR6_R8_NPZ=$NPZ"
echo "ACT_DR6_R8_ZIP=$ZIP"
exit "$code"
