#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

BASE_PY=""
if command -v python3 >/dev/null 2>&1; then BASE_PY="$(command -v python3)";
elif command -v python >/dev/null 2>&1; then BASE_PY="$(command -v python)";
else echo "MCMG_R2: python missing" >&2; exit 2; fi

VENV="$ROOT/.local/mcmg_venv"
if [[ ! -x "$VENV/bin/python" ]]; then
  "$BASE_PY" -m venv "$VENV" || { echo "MCMG_R2: install python3-venv" >&2; exit 2; }
fi
export PATH="$VENV/bin:$PATH"
python -m pip install --upgrade pip setuptools wheel >/dev/null
python -m pip install numpy scipy >/dev/null

python -m py_compile \
  memory_gravity/mcmg_r1_causal_first_moment.py \
  memory_gravity/mcmg_r2_self_consistent_growth_weyl.py

echo "MCMG_R2_IMPORT_PASS"

for f in \
  docs/mcmg_r2_self_consistent_growth_weyl_protocol.md \
  results/mcmg_r1_causal_first_moment.json; do
  [[ -f "$f" ]] || { echo "MCMG_R2: missing $f" >&2; exit 3; }
done

PROTOCOL_LOCK="9d5163251b8bead62ff62bcf008bc2e5001ab5e2"
if ! git merge-base --is-ancestor "$PROTOCOL_LOCK" HEAD; then
  echo "MCMG_R2_PROTOCOL_LOCK_FAIL" >&2
  exit 3
fi

python - <<'PY'
import json
from pathlib import Path
j=json.loads(Path('results/mcmg_r1_causal_first_moment.json').read_text())
assert j['classification']=='MCMG_CAUSAL_FIRST_MOMENT_UNIVERSALITY_PASS'
assert all(j['gates'].values())
print('MCMG_R2_PARENT_R1_PASS')
PY

echo "MCMG_R2_PROTOCOL_LOCK_PASS lock=$PROTOCOL_LOCK"
echo "MCMG_R2_HEAD=$(git rev-parse HEAD)"

JSON="results/mcmg_r2_self_consistent_growth_weyl.json"
NPZ="results/mcmg_r2_self_consistent_growth_weyl.npz"
LOG="results/mcmg_r2_self_consistent_growth_weyl.log"
ZIP="results/mcmg_r2_self_consistent_growth_weyl_bundle.zip"
rm -f "$JSON" "$NPZ" "$LOG" "$ZIP"

export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1

set +e
python -u -m memory_gravity.mcmg_r2_self_consistent_growth_weyl \
  --json-out "$JSON" --npz-out "$NPZ" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

python - "$ZIP" "$LOG" "$JSON" "$NPZ" <<'PY'
from pathlib import Path
import sys,zipfile
zp=Path(sys.argv[1])
paths=[Path(x) for x in sys.argv[2:]]+[
    Path('docs/mcmg_r2_self_consistent_growth_weyl_protocol.md'),
    Path('memory_gravity/mcmg_r2_self_consistent_growth_weyl.py'),
    Path('memory_gravity/run_mcmg_r2_self_consistent_growth_weyl.sh'),
    Path('results/mcmg_r1_causal_first_moment.json'),
]
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED) as zf:
    seen=set()
    for p in paths:
        if p.exists() and p not in seen:
            zf.write(p,arcname=str(p)); seen.add(p)
print('MCMG_R2_BUNDLE='+str(zp))
PY

echo "MCMG_R2_EXIT=$code"
echo "MCMG_R2_LOG=$LOG"
echo "MCMG_R2_JSON=$JSON"
echo "MCMG_R2_NPZ=$NPZ"
echo "MCMG_R2_ZIP=$ZIP"
exit "$code"
