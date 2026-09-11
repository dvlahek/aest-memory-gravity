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
  echo "FULLJ_STATIC_WEYL: python missing" >&2
  exit 2
fi

VENV="$ROOT/.local/fullj_weyl_venv"
if [[ ! -x "$VENV/bin/python" ]]; then
  "$BASE_PY" -m venv "$VENV" || { echo "FULLJ_STATIC_WEYL: install python3-venv" >&2; exit 2; }
fi
export PATH="$VENV/bin:$PATH"

if ! python - <<'PY'
import numpy
print('FULLJ_STATIC_WEYL_ENV_PASS')
print('numpy='+numpy.__version__)
PY
then
  python -m pip install --upgrade pip setuptools wheel >/dev/null
  python -m pip install numpy >/dev/null
fi

python -m py_compile fullj_weyl/static_snapshot_weyl_operator.py

IN_NPZ="results/fullj_mode_coupling_jacobian.npz"
IN_JSON="results/fullj_mode_coupling_jacobian.json"
OUT_NPZ="results/fullj_static_snapshot_weyl_operator.npz"
OUT_JSON="results/fullj_static_snapshot_weyl_operator.json"
OUT_CSV="results/fullj_static_snapshot_weyl_operator_summary.csv"
LOG="results/fullj_static_snapshot_weyl_operator.log"
ZIP="results/fullj_static_snapshot_weyl_operator_bundle.zip"

for p in "$IN_NPZ" "$IN_JSON"; do
  if [[ ! -f "$p" ]]; then
    echo "FULLJ_STATIC_WEYL: required locked Jacobian artifact missing: $p" >&2
    exit 2
  fi
done
rm -f "$OUT_NPZ" "$OUT_JSON" "$OUT_CSV" "$LOG" "$ZIP"

set +e
python -u fullj_weyl/static_snapshot_weyl_operator.py \
  --jacobian-npz "$IN_NPZ" \
  --jacobian-json "$IN_JSON" \
  --npz-out "$OUT_NPZ" \
  --json-out "$OUT_JSON" \
  --csv-out "$OUT_CSV" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

python - "$ZIP" "$LOG" "$OUT_JSON" "$OUT_NPZ" "$OUT_CSV" <<'PY'
from pathlib import Path
import sys, zipfile
zp=Path(sys.argv[1])
paths=[Path(x) for x in sys.argv[2:]] + [
    Path('docs/fullj_weyl_lensing_closure_audit.md'),
    Path('docs/fullj_mode_coupling_jacobian_LOCKED_RESULT.md'),
    Path('fullj_weyl/static_snapshot_weyl_operator.py'),
    Path('fullj_weyl/run_local_static_snapshot_weyl_operator.sh'),
]
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED) as zf:
    seen=set()
    for p in paths:
        if p.exists() and p not in seen:
            zf.write(p,arcname=str(p)); seen.add(p)
print('FULLJ_STATIC_WEYL_BUNDLE='+str(zp))
PY

echo "FULLJ_STATIC_WEYL_EXIT=$code"
echo "FULLJ_STATIC_WEYL_LOG=$LOG"
echo "FULLJ_STATIC_WEYL_JSON=$OUT_JSON"
echo "FULLJ_STATIC_WEYL_NPZ=$OUT_NPZ"
echo "FULLJ_STATIC_WEYL_CSV=$OUT_CSV"
echo "FULLJ_STATIC_WEYL_ZIP=$ZIP"
exit "$code"
