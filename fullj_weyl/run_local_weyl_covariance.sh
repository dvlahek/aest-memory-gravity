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
  echo "FULLJ_LOCAL_WEYL_COV: python missing" >&2
  exit 2
fi

VENV="$ROOT/.local/fullj_weyl_venv"
if [[ ! -x "$VENV/bin/python" ]]; then
  "$BASE_PY" -m venv "$VENV" || { echo "FULLJ_LOCAL_WEYL_COV: install python3-venv" >&2; exit 2; }
fi
export PATH="$VENV/bin:$PATH"

if ! python - <<'PY'
import numpy
print('FULLJ_LOCAL_WEYL_COV_ENV_PASS')
print('numpy='+numpy.__version__)
PY
then
  python -m pip install --upgrade pip setuptools wheel >/dev/null
  python -m pip install numpy >/dev/null
fi

python -m py_compile fullj_weyl/local_weyl_covariance.py

IN_JSON="results/fullj_mode_coupling_jacobian.json"
OUT_JSON="results/fullj_local_weyl_covariance.json"
OUT_CSV="results/fullj_local_weyl_covariance_summary.csv"
OUT_NPZ="results/fullj_local_weyl_covariance.npz"
LOG="results/fullj_local_weyl_covariance.log"
ZIP="results/fullj_local_weyl_covariance_bundle.zip"

if [[ ! -f "$IN_JSON" ]]; then
  echo "FULLJ_LOCAL_WEYL_COV: required locked Jacobian JSON missing: $IN_JSON" >&2
  exit 2
fi
rm -f "$OUT_JSON" "$OUT_CSV" "$OUT_NPZ" "$LOG" "$ZIP"

set +e
python -u fullj_weyl/local_weyl_covariance.py \
  --jacobian-json "$IN_JSON" \
  --json-out "$OUT_JSON" \
  --csv-out "$OUT_CSV" \
  --npz-out "$OUT_NPZ" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

python - "$ZIP" "$LOG" "$OUT_JSON" "$OUT_CSV" "$OUT_NPZ" <<'PY'
from pathlib import Path
import sys, zipfile
zp=Path(sys.argv[1])
paths=[Path(x) for x in sys.argv[2:]] + [
    Path('docs/fullj_local_weyl_covariance_design.md'),
    Path('docs/fullj_weyl_lensing_closure_audit.md'),
    Path('docs/fullj_static_snapshot_weyl_operator_result.md'),
    Path('fullj_weyl/local_weyl_covariance.py'),
    Path('fullj_weyl/run_local_weyl_covariance.sh'),
]
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED) as zf:
    seen=set()
    for p in paths:
        if p.exists() and p not in seen:
            zf.write(p,arcname=str(p)); seen.add(p)
print('FULLJ_LOCAL_WEYL_COV_BUNDLE='+str(zp))
PY

echo "FULLJ_LOCAL_WEYL_COV_EXIT=$code"
echo "FULLJ_LOCAL_WEYL_COV_LOG=$LOG"
echo "FULLJ_LOCAL_WEYL_COV_JSON=$OUT_JSON"
echo "FULLJ_LOCAL_WEYL_COV_CSV=$OUT_CSV"
echo "FULLJ_LOCAL_WEYL_COV_NPZ=$OUT_NPZ"
echo "FULLJ_LOCAL_WEYL_COV_ZIP=$ZIP"
exit "$code"
