#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

PREFIT_LOCK='819e40eeea3dec55181fc63233e4002cda005a2e'
IMPLEMENTATION_LOCK='9db2f444c310a311116b58659b8154743ca707d5'
IMPLEMENTATION_BLOB='aaebb2206e54c2a1c8f5899b5d1e0c28081a6c52'
R9B2K_POSTDATA_LOCK='dd3981b2fd838fb24a997af77f913c3d5dd8d07b'
REPAIR02_POSTDATA_LOCK='d3fd6191d55f4e74aa8666f842dae64bd8aee09b'
R10A_POSTDATA_LOCK='b7da648f1810ea0c047b6e511e3f87211e830329'
REPAIR02_JSON_SHA='eb221160bf64b0905ec0b620fb8441aea2a1e55fc2981f8b3974954917f1cea4'

PREFIT='docs/stable_aest_ksz_r11a_pairwise_velocity_response_prefit.md'
IMPL='fullj_weyl/stable_aest_ksz_r11a_pairwise_velocity_response.py'
REPAIR02_JSON='results/stable_aest_desi_dr1_r9b2k_shapefit_dm_repair02.json'
WORK='results/stable_aest_desi_dr1_r9b2k_work'

for f in "$PREFIT" "$IMPL" "$REPAIR02_JSON"; do
  [[ -f "$f" ]] || { echo "STABLE_AEST_KSZ_R11A_MISSING file=$f" >&2; exit 3; }
done
[[ -d "$WORK" ]] || { echo "STABLE_AEST_KSZ_R11A_MISSING workdir=$WORK" >&2; exit 3; }

for lock in "$PREFIT_LOCK" "$IMPLEMENTATION_LOCK" "$R9B2K_POSTDATA_LOCK" "$REPAIR02_POSTDATA_LOCK" "$R10A_POSTDATA_LOCK"; do
  git merge-base --is-ancestor "$lock" HEAD || { echo "STABLE_AEST_KSZ_R11A_LOCK_FAIL lock=$lock" >&2; exit 3; }
done
[[ "$(git hash-object "$IMPL")" == "$IMPLEMENTATION_BLOB" ]] || {
  echo STABLE_AEST_KSZ_R11A_IMPLEMENTATION_BLOB_FAIL >&2; exit 3;
}
[[ "$(sha256sum "$REPAIR02_JSON" | awk '{print $1}')" == "$REPAIR02_JSON_SHA" ]] || {
  echo STABLE_AEST_KSZ_R11A_REPAIR02_JSON_HASH_FAIL >&2; exit 3;
}

echo "STABLE_AEST_KSZ_R11A_LOCK_PASS prefit=$PREFIT_LOCK implementation=$IMPLEMENTATION_LOCK r9b2k=$R9B2K_POSTDATA_LOCK repair02=$REPAIR02_POSTDATA_LOCK r10a=$R10A_POSTDATA_LOCK"

BASE_PY="$(command -v python3 || command -v python || true)"
[[ -n "$BASE_PY" ]] || { echo 'STABLE_AEST_KSZ_R11A: python missing' >&2; exit 2; }
VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then "$BASE_PY" -m venv "$VENV"; fi
export PATH="$VENV/bin:$PATH"
python -m pip install numpy scipy >/dev/null

python -m py_compile \
  fullj_weyl/stable_aest_ksz_r11a_pairwise_velocity_response.py \
  fullj_weyl/stable_aest_desi_dr1_r9b2k_native_k_density_convergence.py
echo STABLE_AEST_KSZ_R11A_IMPORT_PASS

python - <<'PY'
from pathlib import Path
p=Path('fullj_weyl/stable_aest_ksz_r11a_pairwise_velocity_response.py').read_text()
required=[
 'PREFIT_LOCK = "819e40eeea3dec55181fc63233e4002cda005a2e"',
 'R9B2K_POSTDATA_LOCK = "dd3981b2fd838fb24a997af77f913c3d5dd8d07b"',
 'REPAIR02_POSTDATA_LOCK = "d3fd6191d55f4e74aa8666f842dae64bd8aee09b"',
 'R10A_POSTDATA_LOCK = "b7da648f1810ea0c047b6e511e3f87211e830329"',
 'R_MPC_H = np.arange(20.0, 201.0, 10.0)',
 'EPS_PRIMARY = 0.025',
 'EPS_CONTROL = 0.05',
 'pdf = sign * np.sqrt(pdd * ptt)',
 'v12 = -2.0 * a * (H_kms_mpc / h) * Idf / denom',
 'CLS_PASS = "STABLE_AEST_KSZ_R11A_PAIRWISE_VELOCITY_RESPONSE_CERTIFIED"',
]
for token in required:
    assert token in p, token
for forbidden in (
    'from classy import Class', 'Class()', 'smooth_pk_interpolator',
    'act_dr6_lenslike', 'load_desi(', 'get_data(',
):
    assert forbidden not in p, forbidden
print('STABLE_AEST_KSZ_R11A_ANTI_STALE_CODE_PASS')
PY

python - "$WORK" <<'PY'
from pathlib import Path
import sys
w=Path(sys.argv[1])
files=list(w.glob('*.pkl'))
if len(files) < 25:
    raise SystemExit(f'STABLE_AEST_KSZ_R11A_CHECKPOINT_COUNT_FAIL count={len(files)}')
print(f'STABLE_AEST_KSZ_R11A_CHECKPOINT_FILES_PRESENT count={len(files)}')
PY

export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
JSON='results/stable_aest_ksz_r11a_pairwise_velocity_response.json'
NPZ='results/stable_aest_ksz_r11a_pairwise_velocity_response.npz'
LOG='results/stable_aest_ksz_r11a_pairwise_velocity_response.log'
ENVOUT='results/stable_aest_ksz_r11a_environment.txt'
rm -f "$JSON" "$NPZ" "$LOG" "$ENVOUT"

{
  echo "repo_head=$(git rev-parse HEAD)"
  echo "prefit_lock=$PREFIT_LOCK"
  echo "implementation_lock=$IMPLEMENTATION_LOCK"
  echo "implementation_blob=$IMPLEMENTATION_BLOB"
  echo "r9b2k_postdata_lock=$R9B2K_POSTDATA_LOCK"
  echo "repair02_postdata_lock=$REPAIR02_POSTDATA_LOCK"
  echo "r10a_postdata_lock=$R10A_POSTDATA_LOCK"
  echo "python=$(python --version 2>&1)"
  echo "checkpoint_count=$(find "$WORK" -maxdepth 1 -type f -name '*.pkl' | wc -l)"
} > "$ENVOUT"

set +e
python -u -m fullj_weyl.stable_aest_ksz_r11a_pairwise_velocity_response \
  --workdir "$WORK" --json-out "$JSON" --npz-out "$NPZ" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

echo "STABLE_AEST_KSZ_R11A_EXIT=$code"
[[ -f "$JSON" ]] && sha256sum "$JSON"
[[ -f "$NPZ" ]] && sha256sum "$NPZ"
sha256sum "$LOG"
echo "STABLE_AEST_KSZ_R11A_JSON=$JSON"
echo "STABLE_AEST_KSZ_R11A_NPZ=$NPZ"
echo "STABLE_AEST_KSZ_R11A_LOG=$LOG"
exit "$code"
