#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

PREFIT_LOCK='9e9fd426e3030727f0723cf7e50ae4ef0c2799e8'
R1_POSTDATA_LOCK='8f789b8203dfbee4a9ef7a16ddfb1bfd201bc78b'
HISTORY_LOCK='ef6d291ecc99a0af950dd44fef743a87f708b81d'
R1_IMPL_LOCK='c0a9f430053f4080ca4990d1549a5eca32e6515e'
R1_RUNNER_LOCK='4a0c1ce46813ed1f3fb7b407bc49fff5fbd164f6'
IMPLEMENTATION_LOCK='aa3909146b438581f41f0de97171e6d0e2a34ec9'
PARENT_JSON='results/stable_aest_desi_dr1_r9b2k_native_k_density_convergence.json'
PARENT_SHA='f4323f84dfa93c5ac3ef449fbe666ce3add45a50331079fe66bd27beb2b30c7e'
R1_JSON='results/stable_aest_desi_dr1_r9b2k_shapefit_dm_repair01.json'
R1_SHA='af92b8f7c6186a5e04c7a4973840617dd64ef7afb33deddc24804c1b974f40ad'
DESI_COMMIT='7d51f4f86dc3bee6bf10f1a684913c943a89a844'
LSSTYPES_COMMIT='53f048e610bcb008548f66822b0879ce9df58cb1'
COSMOPRIMO_COMMIT='2e59c963c9b8e7cba1a4c8f161e978c6f4d80c2d'

for lock in "$PREFIT_LOCK" "$R1_POSTDATA_LOCK" "$HISTORY_LOCK" "$R1_IMPL_LOCK" "$R1_RUNNER_LOCK" "$IMPLEMENTATION_LOCK"; do
  git merge-base --is-ancestor "$lock" HEAD
 done
[[ -s "$PARENT_JSON" && "$(sha256sum "$PARENT_JSON" | awk '{print $1}')" == "$PARENT_SHA" ]] || { echo 'R9B2K DM Repair02: parent R9b2k JSON mismatch' >&2; exit 3; }
[[ -s "$R1_JSON" && "$(sha256sum "$R1_JSON" | awk '{print $1}')" == "$R1_SHA" ]] || { echo 'R9B2K DM Repair02: Repair01 JSON mismatch' >&2; exit 3; }
echo "STABLE_AEST_DESI_DR1_R9B2K_DM_REPAIR02_LOCK_PASS prefit=$PREFIT_LOCK r1post=$R1_POSTDATA_LOCK history=$HISTORY_LOCK implementation=$IMPLEMENTATION_LOCK parent=$PARENT_SHA repair01=$R1_SHA"

WORK='results/stable_aest_desi_dr1_r9b2k_work'
count=0
for tau in 10 5 2.5 1.25; do
  for eta in +0.000 +0.025 -0.025 +0.050 -0.050; do
    f="$WORK/D2_tau${tau}_eta${eta}.pkl"
    [[ -s "$f" ]] || { echo "R9B2K DM Repair02: missing checkpoint $f" >&2; exit 3; }
    count=$((count+1))
  done
 done
[[ "$count" -eq 20 ]]
echo "STABLE_AEST_DESI_DR1_R9B2K_DM_REPAIR02_CHECKPOINT_FILES_PASS count=$count"

BASE_PY="$(command -v python3 || command -v python || true)"
[[ -n "$BASE_PY" ]] || { echo 'R9B2K DM Repair02: Python missing' >&2; exit 2; }
VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then "$BASE_PY" -m venv "$VENV"; fi
export PATH="$VENV/bin:$PATH"
python -m pip install -q numpy scipy cython requests beautifulsoup4 h5py camb
python -m pip install -q "git+https://github.com/adematti/lsstypes.git@$LSSTYPES_COMMIT"
python -m pip install -q "git+https://github.com/cosmodesi/cosmoprimo.git@$COSMOPRIMO_COMMIT"
python -m py_compile fullj_weyl/stable_aest_desi_dr1_r9b2k_shapefit_dm_repair02.py
python - <<'PY'
from pathlib import Path
p=Path('fullj_weyl/stable_aest_desi_dr1_r9b2k_shapefit_dm_repair02.py').read_text()
assert 'Class(' not in p
assert 'smooth_pk_interpolator' not in p
for token in (
    'M_VALUE_GATE = 5e-3', 'MIN_SEGMENT_NODES = 8',
    'PchipInterpolator(lx, ly, extrapolate=False)',
    'np.interp(lq, lx, ly)',
    'R9B2K_DM2_P3_local_positive_pivot',
    'R9B2K_DM2_P4_local_m_operator',
    'STABLE_AEST_DESI_DR1_R9B2K_SHAPEFIT_DM_REPAIR02_CERTIFIED',
): assert token in p, token
print('STABLE_AEST_DESI_DR1_R9B2K_DM_REPAIR02_IMPORT_PASS')
PY

DESI_REPO="$ROOT/.local/desi_kp_likelihoods_r9b"
[[ -d "$DESI_REPO/.git" ]] || { echo 'R9B2K DM Repair02: missing DESI repo' >&2; exit 3; }
[[ "$(git -C "$DESI_REPO" rev-parse HEAD)" == "$DESI_COMMIT" ]]
DESI_DATA="$ROOT/.local/desi_dr1_r9b_likelihood_data"
[[ -d "$DESI_DATA" ]] || { echo 'R9B2K DM Repair02: missing DESI data dir' >&2; exit 3; }
echo "STABLE_AEST_DESI_DR1_R9B2K_DM_REPAIR02_OFFICIAL_REPO_PASS head=$DESI_COMMIT"

export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
JSON='results/stable_aest_desi_dr1_r9b2k_shapefit_dm_repair02.json'
NPZ='results/stable_aest_desi_dr1_r9b2k_shapefit_dm_repair02.npz'
LOG='results/stable_aest_desi_dr1_r9b2k_shapefit_dm_repair02.log'
rm -f "$JSON" "$NPZ" "$LOG"

echo STABLE_AEST_DESI_DR1_R9B2K_DM_REPAIR02_START_RUN
set +e
python -u -m fullj_weyl.stable_aest_desi_dr1_r9b2k_shapefit_dm_repair02 \
  --data-dir "$DESI_DATA" --official-repo "$DESI_REPO" --workdir "$WORK" \
  --json-out "$JSON" --npz-out "$NPZ" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

echo "STABLE_AEST_DESI_DR1_R9B2K_DM_REPAIR02_EXIT=$code"
[[ -s "$JSON" ]] && sha256sum "$JSON"
[[ -s "$LOG" ]] && sha256sum "$LOG"
exit "$code"
