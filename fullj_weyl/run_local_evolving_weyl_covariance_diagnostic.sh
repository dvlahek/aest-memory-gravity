#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

PY=""
if [[ -x "$ROOT/.local/fullj_weyl_bridge_venv/bin/python" ]]; then
  PY="$ROOT/.local/fullj_weyl_bridge_venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then
  PY="$(command -v python3)"
elif command -v python >/dev/null 2>&1; then
  PY="$(command -v python)"
else
  echo "FULLJ_EVOLVING_WEYL_COV: python missing" >&2
  exit 2
fi

"$PY" - <<'PY'
import numpy
print('FULLJ_EVOLVING_WEYL_COV_ENV_PASS')
print('numpy='+numpy.__version__)
PY
"$PY" -m py_compile fullj_weyl/evolving_weyl_covariance_diagnostic.py

R2JSON="results/fullj_evolving_weyl_bridge_r2.json"
R2NPZ="results/fullj_evolving_weyl_bridge_r2.npz"
JSON="results/fullj_evolving_weyl_covariance_diagnostic.json"
CSV="results/fullj_evolving_weyl_covariance_diagnostic.csv"
NPZ="results/fullj_evolving_weyl_covariance_diagnostic.npz"
LOG="results/fullj_evolving_weyl_covariance_diagnostic.log"
ZIP="results/fullj_evolving_weyl_covariance_diagnostic_bundle.zip"

if [[ ! -f "$R2JSON" || ! -f "$R2NPZ" ]]; then
  echo "FULLJ_EVOLVING_WEYL_COV: missing R2 result files" >&2
  exit 2
fi
rm -f "$JSON" "$CSV" "$NPZ" "$LOG" "$ZIP"

set +e
"$PY" -u fullj_weyl/evolving_weyl_covariance_diagnostic.py \
  --r2-json "$R2JSON" --r2-npz "$R2NPZ" \
  --json-out "$JSON" --csv-out "$CSV" --npz-out "$NPZ" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

"$PY" - "$ZIP" "$LOG" "$JSON" "$CSV" "$NPZ" <<'PY'
from pathlib import Path
import sys, zipfile
zp=Path(sys.argv[1])
paths=[Path(x) for x in sys.argv[2:]] + [
    Path('docs/fullj_evolving_weyl_bridge_r2_result.md'),
    Path('docs/fullj_evolving_weyl_covariance_diagnostic_predata.md'),
    Path('fullj_weyl/evolving_weyl_covariance_diagnostic.py'),
    Path('fullj_weyl/run_local_evolving_weyl_covariance_diagnostic.sh'),
    Path('results/fullj_evolving_weyl_bridge_r2.json'),
]
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED) as zf:
    seen=set()
    for p in paths:
        if p.exists() and p not in seen:
            zf.write(p,arcname=str(p)); seen.add(p)
print('FULLJ_EVOLVING_WEYL_COV_BUNDLE='+str(zp))
PY

echo "FULLJ_EVOLVING_WEYL_COV_EXIT=$code"
echo "FULLJ_EVOLVING_WEYL_COV_JSON=$JSON"
echo "FULLJ_EVOLVING_WEYL_COV_CSV=$CSV"
echo "FULLJ_EVOLVING_WEYL_COV_NPZ=$NPZ"
echo "FULLJ_EVOLVING_WEYL_COV_ZIP=$ZIP"
exit "$code"
