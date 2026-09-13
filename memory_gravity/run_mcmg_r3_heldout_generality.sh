#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

BASE_PY=""
if command -v python3 >/dev/null 2>&1; then BASE_PY="$(command -v python3)";
elif command -v python >/dev/null 2>&1; then BASE_PY="$(command -v python)";
else echo "MCMG_R3: python missing" >&2; exit 2; fi

VENV="$ROOT/.local/mcmg_venv"
if [[ ! -x "$VENV/bin/python" ]]; then
  "$BASE_PY" -m venv "$VENV" || { echo "MCMG_R3: install python3-venv" >&2; exit 2; }
fi
export PATH="$VENV/bin:$PATH"
python -m pip install --upgrade pip setuptools wheel >/dev/null
python -m pip install numpy scipy >/dev/null

python -m py_compile memory_gravity/mcmg_r3_heldout_generality.py

echo "MCMG_R3_IMPORT_PASS"

for f in \
  docs/mcmg_r3_heldout_generality_predata.md \
  memory_gravity/mcmg_r3_heldout_generality.py \
  results/mcmg_r2_self_consistent_growth_weyl.json; do
  [[ -f "$f" ]] || { echo "MCMG_R3: missing $f" >&2; exit 3; }
done

PREDATA_LOCK="c76075ec27325f525fde70154551c20bf23d0759"
if ! git merge-base --is-ancestor "$PREDATA_LOCK" HEAD; then
  echo "MCMG_R3_PREDATA_LOCK_FAIL" >&2
  exit 3
fi

python - <<'PY'
import json
from pathlib import Path
p=Path('results/mcmg_r2_self_consistent_growth_weyl.json')
o=json.loads(p.read_text())
assert o.get('classification') == 'MCMG_SELF_CONSISTENT_GROWTH_WEYL_MEMORY_PASS'
assert all(o.get('gates',{}).values())
print('MCMG_R3_PARENT_R2_PASS')
PY

echo "MCMG_R3_SCIENCE_LOCK_PASS predata=$PREDATA_LOCK"
echo "MCMG_R3_HEAD=$(git rev-parse HEAD)"

JSON="results/mcmg_r3_heldout_generality.json"
NPZ="results/mcmg_r3_heldout_generality.npz"
LOG="results/mcmg_r3_heldout_generality.log"
ZIP="results/mcmg_r3_heldout_generality_bundle.zip"
rm -f "$JSON" "$NPZ" "$LOG" "$ZIP"

export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1

set +e
python -u memory_gravity/mcmg_r3_heldout_generality.py \
  --json-out "$JSON" --npz-out "$NPZ" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

python - "$ZIP" "$LOG" "$JSON" "$NPZ" <<'PY'
from pathlib import Path
import sys, zipfile
zp=Path(sys.argv[1])
paths=[Path(x) for x in sys.argv[2:]] + [
    Path('docs/mcmg_r3_heldout_generality_predata.md'),
    Path('memory_gravity/mcmg_r3_heldout_generality.py'),
    Path('memory_gravity/run_mcmg_r3_heldout_generality.sh'),
    Path('results/mcmg_r2_self_consistent_growth_weyl.json'),
]
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED) as zf:
    seen=set()
    for p in paths:
        if p.exists() and p not in seen:
            zf.write(p,arcname=str(p)); seen.add(p)
print('MCMG_R3_BUNDLE='+str(zp))
PY

echo "MCMG_R3_EXIT=$code"
echo "MCMG_R3_LOG=$LOG"
echo "MCMG_R3_JSON=$JSON"
echo "MCMG_R3_NPZ=$NPZ"
echo "MCMG_R3_ZIP=$ZIP"
exit "$code"
