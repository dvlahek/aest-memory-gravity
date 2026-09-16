#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

PREFIT_LOCK='f7dfff4cb6c4fc43fdd99a9a5679d509afa01714'
IMPLEMENTATION_LOCK='ce2e91c6617deef81c8db7da988ca39e9b9a4d6f'
IMPLEMENTATION_BLOB='c40b72c5944e7fb993ae974acfbe194cc6a4de02'
R11A_POSTDATA_LOCK='94efaf95b4582a177bd80dd566d5d2c26b4e212c'
R01_POSTDATA_LOCK='43ce2d7cd772438efe34edabc25572c7b7516bee'
R01_JSON_SHA='4fc3612674ae5ae6b2093e9642a3984bf4c7a3dbcd72b6b9eba6d9e664caa239'

PREFIT='docs/stable_aest_ksz_r11a_dense_resolution_repair02_prefit.md'
IMPL='fullj_weyl/stable_aest_ksz_r11a_dense_resolution_repair02.py'
R01JSON='results/stable_aest_ksz_r11a_response_before_integration_repair01.json'
WORK='results/stable_aest_desi_dr1_r9b2k_work'

for f in "$PREFIT" "$IMPL" "$R01JSON" docs/stable_aest_ksz_r11a_response_before_integration_repair01_postdata.md; do
  [[ -f "$f" ]] || { echo "STABLE_AEST_KSZ_R11A_REPAIR02_MISSING file=$f" >&2; exit 3; }
done
[[ -d "$WORK" ]] || { echo "STABLE_AEST_KSZ_R11A_REPAIR02_MISSING workdir=$WORK" >&2; exit 3; }

for lock in "$PREFIT_LOCK" "$IMPLEMENTATION_LOCK" "$R11A_POSTDATA_LOCK" "$R01_POSTDATA_LOCK"; do
  git merge-base --is-ancestor "$lock" HEAD || { echo "STABLE_AEST_KSZ_R11A_REPAIR02_LOCK_FAIL lock=$lock" >&2; exit 3; }
done
[[ "$(git hash-object "$IMPL")" == "$IMPLEMENTATION_BLOB" ]] || { echo STABLE_AEST_KSZ_R11A_REPAIR02_IMPLEMENTATION_BLOB_FAIL >&2; exit 3; }
[[ "$(sha256sum "$R01JSON" | awk '{print $1}')" == "$R01_JSON_SHA" ]] || { echo STABLE_AEST_KSZ_R11A_REPAIR02_R01_JSON_HASH_FAIL >&2; exit 3; }
echo "STABLE_AEST_KSZ_R11A_REPAIR02_LOCK_PASS prefit=$PREFIT_LOCK implementation=$IMPLEMENTATION_LOCK r11a=$R11A_POSTDATA_LOCK r01=$R01_POSTDATA_LOCK"

BASE_PY="$(command -v python3 || command -v python || true)"
[[ -n "$BASE_PY" ]] || { echo 'STABLE_AEST_KSZ_R11A_REPAIR02: python missing' >&2; exit 2; }
VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then "$BASE_PY" -m venv "$VENV"; fi
export PATH="$VENV/bin:$PATH"
python -m pip install numpy scipy >/dev/null

python -m py_compile \
  fullj_weyl/stable_aest_ksz_r11a_dense_resolution_repair02.py \
  fullj_weyl/stable_aest_ksz_r11a_response_before_integration_repair01.py
echo STABLE_AEST_KSZ_R11A_REPAIR02_IMPORT_PASS

python - <<'PY'
from pathlib import Path
p=Path('fullj_weyl/stable_aest_ksz_r11a_dense_resolution_repair02.py').read_text()
required=[
 'PREFIT_LOCK = "f7dfff4cb6c4fc43fdd99a9a5679d509afa01714"',
 'R01_POSTDATA_LOCK = "43ce2d7cd772438efe34edabc25572c7b7516bee"',
 'R01_JSON_SHA256 = "4fc3612674ae5ae6b2093e9642a3984bf4c7a3dbcd72b6b9eba6d9e664caa239"',
 'RES_E_GATE = 0.01',
 'RES_C_GATE = 0.999',
 'for n in (16384,32768,65536):',
 '"R11A_R02_G3_asymptotic_dense_resolution"',
 'CLS_PASS = "STABLE_AEST_KSZ_R11A_REPAIR02_DENSE_RESOLUTION_CERTIFIED"',
]
for token in required: assert token in p, token
for forbidden in ('from classy import Class','Class()','np.clip(','smooth_pk_interpolator','act_dr6_lenslike','load_desi(','get_data('):
    assert forbidden not in p, forbidden
print('STABLE_AEST_KSZ_R11A_REPAIR02_ANTI_STALE_CODE_PASS')
PY

python - "$WORK" <<'PY'
from pathlib import Path
import sys
w=Path(sys.argv[1]); files=list(w.glob('*.pkl'))
if len(files) < 25: raise SystemExit(f'STABLE_AEST_KSZ_R11A_REPAIR02_CHECKPOINT_COUNT_FAIL count={len(files)}')
print(f'STABLE_AEST_KSZ_R11A_REPAIR02_CHECKPOINT_FILES_PRESENT count={len(files)}')
PY

export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
JSON='results/stable_aest_ksz_r11a_dense_resolution_repair02.json'
NPZ='results/stable_aest_ksz_r11a_dense_resolution_repair02.npz'
LOG='results/stable_aest_ksz_r11a_dense_resolution_repair02.log'
ENVOUT='results/stable_aest_ksz_r11a_dense_resolution_repair02_environment.txt'
rm -f "$JSON" "$NPZ" "$LOG" "$ENVOUT"

{
  echo "repo_head=$(git rev-parse HEAD)"
  echo "prefit_lock=$PREFIT_LOCK"
  echo "implementation_lock=$IMPLEMENTATION_LOCK"
  echo "implementation_blob=$IMPLEMENTATION_BLOB"
  echo "r11a_postdata_lock=$R11A_POSTDATA_LOCK"
  echo "r01_postdata_lock=$R01_POSTDATA_LOCK"
  echo "python=$(python --version 2>&1)"
  echo "checkpoint_count=$(find "$WORK" -maxdepth 1 -type f -name '*.pkl' | wc -l)"
} > "$ENVOUT"

set +e
python -u -m fullj_weyl.stable_aest_ksz_r11a_dense_resolution_repair02 \
  --workdir "$WORK" --json-out "$JSON" --npz-out "$NPZ" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

echo "STABLE_AEST_KSZ_R11A_REPAIR02_EXIT=$code"
[[ -f "$JSON" ]] && sha256sum "$JSON"
[[ -f "$NPZ" ]] && sha256sum "$NPZ"
sha256sum "$LOG"
echo "STABLE_AEST_KSZ_R11A_REPAIR02_JSON=$JSON"
echo "STABLE_AEST_KSZ_R11A_REPAIR02_NPZ=$NPZ"
echo "STABLE_AEST_KSZ_R11A_REPAIR02_LOG=$LOG"
exit "$code"
