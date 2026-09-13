#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

BASE_PY=""
if command -v python3 >/dev/null 2>&1; then BASE_PY="$(command -v python3)";
elif command -v python >/dev/null 2>&1; then BASE_PY="$(command -v python)";
else echo "MCMG_R1: python missing" >&2; exit 2; fi

VENV="$ROOT/.local/mcmg_venv"
if [[ ! -x "$VENV/bin/python" ]]; then
  "$BASE_PY" -m venv "$VENV" || { echo "MCMG_R1: install python3-venv" >&2; exit 2; }
fi
export PATH="$VENV/bin:$PATH"
python -m pip install --upgrade pip setuptools wheel >/dev/null
python -m pip install numpy scipy >/dev/null

python -m py_compile \
  memory_gravity/mcmg_r1_causal_first_moment.py \
  memory_gravity/mcmg_r1_causal_first_moment_r1.py

echo "MCMG_R1_IMPORT_PASS"

for f in \
  docs/minimal_causal_memory_gravity_program.md \
  docs/mcmg_r1_causal_first_moment_predata.md \
  memory_gravity/mcmg_r1_causal_first_moment.py \
  memory_gravity/mcmg_r1_causal_first_moment_r1.py; do
  [[ -f "$f" ]] || { echo "MCMG_R1: missing $f" >&2; exit 3; }
done

PREDATA_LOCK="a1f94c9d25152e80960cb1b0af32b1c469136597"
if ! git merge-base --is-ancestor "$PREDATA_LOCK" HEAD; then
  echo "MCMG_R1_PREDATA_LOCK_FAIL" >&2
  exit 3
fi

echo "MCMG_R1_SCIENCE_LOCK_PASS predata=$PREDATA_LOCK"
echo "MCMG_R1_HEAD=$(git rev-parse HEAD)"

JSON="results/mcmg_r1_causal_first_moment.json"
NPZ="results/mcmg_r1_causal_first_moment.npz"
LOG="results/mcmg_r1_causal_first_moment.log"
ZIP="results/mcmg_r1_causal_first_moment_bundle.zip"
rm -f "$JSON" "$NPZ" "$LOG" "$ZIP"

export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1

set +e
python -u -m memory_gravity.mcmg_r1_causal_first_moment_r1 \
  --json-out "$JSON" --npz-out "$NPZ" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

python - "$ZIP" "$LOG" "$JSON" "$NPZ" <<'PY'
from pathlib import Path
import sys, zipfile
zp=Path(sys.argv[1])
paths=[Path(x) for x in sys.argv[2:]] + [
    Path('docs/minimal_causal_memory_gravity_program.md'),
    Path('docs/mcmg_r1_causal_first_moment_predata.md'),
    Path('memory_gravity/mcmg_r1_causal_first_moment.py'),
    Path('memory_gravity/mcmg_r1_causal_first_moment_r1.py'),
    Path('memory_gravity/run_mcmg_r1_causal_first_moment.sh'),
]
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED) as zf:
    seen=set()
    for p in paths:
        if p.exists() and p not in seen:
            zf.write(p,arcname=str(p)); seen.add(p)
print('MCMG_R1_BUNDLE='+str(zp))
PY

echo "MCMG_R1_EXIT=$code"
echo "MCMG_R1_LOG=$LOG"
echo "MCMG_R1_JSON=$JSON"
echo "MCMG_R1_NPZ=$NPZ"
echo "MCMG_R1_ZIP=$ZIP"
exit "$code"
