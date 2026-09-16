#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

PREFIT_LOCK='608851bff8d4fc8ab063cc338ec0cd102a9f74f8'
IMPLEMENTATION_LOCK='11f51614a5c5ddecdcb24e898011d0d47df2b7ea'
IMPLEMENTATION_BLOB='804ba97db8c6446d91f022cec0e19c44dd611c0d'
R11A_POSTDATA_LOCK='94efaf95b4582a177bd80dd566d5d2c26b4e212c'
R9B2K_POSTDATA_LOCK='dd3981b2fd838fb24a997af77f913c3d5dd8d07b'
REPAIR02_POSTDATA_LOCK='d3fd6191d55f4e74aa8666f842dae64bd8aee09b'
R10A_POSTDATA_LOCK='b7da648f1810ea0c047b6e511e3f87211e830329'
R11A_JSON_SHA='a868dbbb6b5b08bf54139abf9d3a288d52bee501f23cc4b61f9422f9fb2d98ab'

PREFIT='docs/stable_aest_ksz_r11a_response_before_integration_repair01_prefit.md'
IMPL='fullj_weyl/stable_aest_ksz_r11a_response_before_integration_repair01.py'
R11A_JSON='results/stable_aest_ksz_r11a_pairwise_velocity_response.json'
WORK='results/stable_aest_desi_dr1_r9b2k_work'

for f in "$PREFIT" "$IMPL" "$R11A_JSON" docs/stable_aest_ksz_r11a_pairwise_velocity_response_postdata.md; do
  [[ -f "$f" ]] || { echo "STABLE_AEST_KSZ_R11A_REPAIR01_MISSING file=$f" >&2; exit 3; }
done
[[ -d "$WORK" ]] || { echo "STABLE_AEST_KSZ_R11A_REPAIR01_MISSING workdir=$WORK" >&2; exit 3; }

for lock in "$PREFIT_LOCK" "$IMPLEMENTATION_LOCK" "$R11A_POSTDATA_LOCK" "$R9B2K_POSTDATA_LOCK" "$REPAIR02_POSTDATA_LOCK" "$R10A_POSTDATA_LOCK"; do
  git merge-base --is-ancestor "$lock" HEAD || { echo "STABLE_AEST_KSZ_R11A_REPAIR01_LOCK_FAIL lock=$lock" >&2; exit 3; }
done
[[ "$(git hash-object "$IMPL")" == "$IMPLEMENTATION_BLOB" ]] || {
  echo STABLE_AEST_KSZ_R11A_REPAIR01_IMPLEMENTATION_BLOB_FAIL >&2; exit 3;
}
[[ "$(sha256sum "$R11A_JSON" | awk '{print $1}')" == "$R11A_JSON_SHA" ]] || {
  echo STABLE_AEST_KSZ_R11A_REPAIR01_R11A_JSON_HASH_FAIL >&2; exit 3;
}
echo "STABLE_AEST_KSZ_R11A_REPAIR01_LOCK_PASS prefit=$PREFIT_LOCK implementation=$IMPLEMENTATION_LOCK r11a_postdata=$R11A_POSTDATA_LOCK r9b2k=$R9B2K_POSTDATA_LOCK repair02=$REPAIR02_POSTDATA_LOCK r10a=$R10A_POSTDATA_LOCK"

BASE_PY="$(command -v python3 || command -v python || true)"
[[ -n "$BASE_PY" ]] || { echo 'STABLE_AEST_KSZ_R11A_REPAIR01: python missing' >&2; exit 2; }
VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then "$BASE_PY" -m venv "$VENV"; fi
export PATH="$VENV/bin:$PATH"
python -m pip install numpy scipy >/dev/null

python -m py_compile \
  fullj_weyl/stable_aest_ksz_r11a_response_before_integration_repair01.py \
  fullj_weyl/stable_aest_ksz_r11a_pairwise_velocity_response.py \
  fullj_weyl/stable_aest_desi_dr1_r9b2k_native_k_density_convergence.py
echo STABLE_AEST_KSZ_R11A_REPAIR01_IMPORT_PASS

python - <<'PY'
from pathlib import Path
p=Path('fullj_weyl/stable_aest_ksz_r11a_response_before_integration_repair01.py').read_text()
required=[
 'PREFIT_LOCK = "608851bff8d4fc8ab063cc338ec0cd102a9f74f8"',
 'R11A_POSTDATA_LOCK = "94efaf95b4582a177bd80dd566d5d2c26b4e212c"',
 'R11A_JSON_SHA256 = "a868dbbb6b5b08bf54139abf9d3a288d52bee501f23cc4b61f9422f9fb2d98ab"',
 'R_MPC_H = np.arange(40.0, 201.0, 10.0)',
 'EPS_PRIMARY = 0.025',
 'EPS_CONTROL = 0.05',
 'Dp = (pp - pm) / (2.0 * float(eps))',
 'Df = (fp - fm) / (2.0 * float(eps))',
 'T = DlnA + DI / I0 - Dxi / (1.0 + xi0)',
 'CLS_PASS = "STABLE_AEST_KSZ_R11A_REPAIR01_RESPONSE_BEFORE_INTEGRATION_CERTIFIED"',
]
for token in required:
    assert token in p, token
for forbidden in (
    'from classy import Class', 'Class()', 'smooth_pk_interpolator',
    'act_dr6_lenslike', 'load_desi(', 'get_data(', 'np.clip(',
):
    assert forbidden not in p, forbidden
print('STABLE_AEST_KSZ_R11A_REPAIR01_ANTI_STALE_CODE_PASS')
PY

python - "$WORK" <<'PY'
from pathlib import Path
import sys
w=Path(sys.argv[1])
files=list(w.glob('*.pkl'))
if len(files) < 25:
    raise SystemExit(f'STABLE_AEST_KSZ_R11A_REPAIR01_CHECKPOINT_COUNT_FAIL count={len(files)}')
print(f'STABLE_AEST_KSZ_R11A_REPAIR01_CHECKPOINT_FILES_PRESENT count={len(files)}')
PY

export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
JSON='results/stable_aest_ksz_r11a_response_before_integration_repair01.json'
NPZ='results/stable_aest_ksz_r11a_response_before_integration_repair01.npz'
LOG='results/stable_aest_ksz_r11a_response_before_integration_repair01.log'
ENVOUT='results/stable_aest_ksz_r11a_response_before_integration_repair01_environment.txt'
rm -f "$JSON" "$NPZ" "$LOG" "$ENVOUT"

{
  echo "repo_head=$(git rev-parse HEAD)"
  echo "prefit_lock=$PREFIT_LOCK"
  echo "implementation_lock=$IMPLEMENTATION_LOCK"
  echo "implementation_blob=$IMPLEMENTATION_BLOB"
  echo "r11a_postdata_lock=$R11A_POSTDATA_LOCK"
  echo "r9b2k_postdata_lock=$R9B2K_POSTDATA_LOCK"
  echo "repair02_postdata_lock=$REPAIR02_POSTDATA_LOCK"
  echo "r10a_postdata_lock=$R10A_POSTDATA_LOCK"
  echo "python=$(python --version 2>&1)"
  echo "checkpoint_count=$(find "$WORK" -maxdepth 1 -type f -name '*.pkl' | wc -l)"
} > "$ENVOUT"

set +e
python -u -m fullj_weyl.stable_aest_ksz_r11a_response_before_integration_repair01 \
  --workdir "$WORK" --json-out "$JSON" --npz-out "$NPZ" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

echo "STABLE_AEST_KSZ_R11A_REPAIR01_EXIT=$code"
[[ -f "$JSON" ]] && sha256sum "$JSON"
[[ -f "$NPZ" ]] && sha256sum "$NPZ"
sha256sum "$LOG"
echo "STABLE_AEST_KSZ_R11A_REPAIR01_JSON=$JSON"
echo "STABLE_AEST_KSZ_R11A_REPAIR01_NPZ=$NPZ"
echo "STABLE_AEST_KSZ_R11A_REPAIR01_LOG=$LOG"
exit "$code"
