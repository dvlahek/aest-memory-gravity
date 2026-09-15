#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

PREFIT_LOCK='9ce2e1a1accdd063c565d9cc373ce764636f9913'
POSTDATA_LOCK='dd3981b2fd838fb24a997af77f913c3d5dd8d07b'
HISTORY_LOCK='be036d4e2b3e3f837f963415d1fc605b769c727e'
PARENT_IMPL_LOCK='874218ec2db38f505307b8183e199fe9d4c73d98'
PARENT_RUNNER_LOCK='f04a9211b6455f3d541b9679c79c56d22fed0c04'
IMPLEMENTATION_LOCK='c0a9f430053f4080ca4990d1549a5eca32e6515e'
PARENT_JSON='results/stable_aest_desi_dr1_r9b2k_native_k_density_convergence.json'
PARENT_SHA='f4323f84dfa93c5ac3ef449fbe666ce3add45a50331079fe66bd27beb2b30c7e'
DESI_COMMIT='7d51f4f86dc3bee6bf10f1a684913c943a89a844'
LSSTYPES_COMMIT='53f048e610bcb008548f66822b0879ce9df58cb1'
COSMOPRIMO_COMMIT='2e59c963c9b8e7cba1a4c8f161e978c6f4d80c2d'

for lock in "$PREFIT_LOCK" "$POSTDATA_LOCK" "$HISTORY_LOCK" "$PARENT_IMPL_LOCK" "$PARENT_RUNNER_LOCK" "$IMPLEMENTATION_LOCK"; do
  git merge-base --is-ancestor "$lock" HEAD
done
[[ -s "$PARENT_JSON" ]] || { echo 'R9B2K-DM-REPAIR01: frozen parent JSON missing' >&2; exit 3; }
[[ "$(sha256sum "$PARENT_JSON" | awk '{print $1}')" == "$PARENT_SHA" ]] || { echo 'R9B2K-DM-REPAIR01: frozen parent JSON SHA mismatch' >&2; exit 3; }

echo "STABLE_AEST_DESI_DR1_R9B2K_DM_REPAIR01_LOCK_PASS prefit=$PREFIT_LOCK postdata=$POSTDATA_LOCK history=$HISTORY_LOCK implementation=$IMPLEMENTATION_LOCK parent=$PARENT_SHA"

WORK='results/stable_aest_desi_dr1_r9b2k_work'
[[ -d "$WORK" ]] || { echo 'R9B2K-DM-REPAIR01: R9b2k work directory missing' >&2; exit 3; }
D2_COUNT="$(find "$WORK" -maxdepth 1 -type f -name 'D2_tau*_eta*.pkl' | wc -l | tr -d ' ')"
[[ "$D2_COUNT" -eq 20 ]] || { echo "R9B2K-DM-REPAIR01: expected exactly 20 D2 checkpoints, found $D2_COUNT" >&2; exit 3; }
echo "STABLE_AEST_DESI_DR1_R9B2K_DM_REPAIR01_CHECKPOINT_FILES_PASS count=$D2_COUNT"

BASE_PY="$(command -v python3 || command -v python || true)"
[[ -n "$BASE_PY" ]] || { echo 'R9B2K-DM-REPAIR01: Python missing' >&2; exit 2; }
VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then "$BASE_PY" -m venv "$VENV"; fi
export PATH="$VENV/bin:$PATH"
python -m pip install -q numpy scipy cython requests beautifulsoup4 h5py camb
python -m pip install -q "git+https://github.com/adematti/lsstypes.git@$LSSTYPES_COMMIT"
python -m pip install -q "git+https://github.com/cosmodesi/cosmoprimo.git@$COSMOPRIMO_COMMIT"

python -m py_compile \
  fullj_weyl/stable_aest_desi_dr1_r9b2k_shapefit_dm_repair01.py \
  fullj_weyl/stable_aest_desi_dr1_r9b2k_native_k_density_convergence.py \
  fullj_weyl/stable_aest_desi_dr1_r9b2i_native_variance_response_shapefit.py \
  fullj_weyl/stable_aest_desi_dr1_r9b_shapefit_projection.py

python - <<'PY'
from pathlib import Path
p=Path('fullj_weyl/stable_aest_desi_dr1_r9b2k_shapefit_dm_repair01.py').read_text()
for bad in ('from classy import Class', 'Class()', '--worker'):
    assert bad not in p, f'forbidden CLASS rerun token: {bad}'
for token in (
    'PARENT_SHA = "f4323f84dfa93c5ac3ef449fbe666ce3add45a50331079fe66bd27beb2b30c7e"',
    'FILTER_REUSE_GATE = 1e-8',
    'PowerSpectrumBAOFilter(',
    'engine="peakaverage"',
    'cosmo_fid=fid',
    'R9B2K_DM_R3_support_matched_filter',
    'R9B2K_DM_R4_cached_vs_fresh_filter',
    'STABLE_AEST_DESI_DR1_R9B2K_SHAPEFIT_DM_REPAIR01_CERTIFIED',
):
    assert token in p, token
print('STABLE_AEST_DESI_DR1_R9B2K_DM_REPAIR01_IMPORT_PASS')
PY

DESI_REPO="$ROOT/.local/desi_kp_likelihoods_r9b"
if [[ ! -d "$DESI_REPO/.git" ]] || [[ "$(git -C "$DESI_REPO" rev-parse HEAD 2>/dev/null || true)" != "$DESI_COMMIT" ]]; then
  rm -rf "$DESI_REPO"
  git clone -q https://github.com/cosmodesi/desi-kp-cosmological-likelihoods.git "$DESI_REPO"
  git -C "$DESI_REPO" checkout -q "$DESI_COMMIT"
fi
[[ "$(git -C "$DESI_REPO" rev-parse HEAD)" == "$DESI_COMMIT" ]]
echo "STABLE_AEST_DESI_DR1_R9B2K_DM_REPAIR01_OFFICIAL_REPO_PASS head=$DESI_COMMIT"

DESI_DATA="$ROOT/.local/desi_dr1_r9b_likelihood_data"
mkdir -p "$DESI_DATA"
required_h5=(
'likelihood_shapefit_spectrum-poles-rotated+bao-recon_syst-rotation-hod-photo_BGS_BRIGHT-21.5_GCcomb_z0.1-0.4_thetacut0.05.h5'
'likelihood_shapefit_spectrum-poles-rotated+bao-recon_syst-rotation-hod-photo_LRG_GCcomb_z0.4-0.6_thetacut0.05.h5'
'likelihood_shapefit_spectrum-poles-rotated+bao-recon_syst-rotation-hod-photo_LRG_GCcomb_z0.6-0.8_thetacut0.05.h5'
'likelihood_shapefit_spectrum-poles-rotated+bao-recon_syst-rotation-hod-photo_LRG_GCcomb_z0.8-1.1_thetacut0.05.h5'
'likelihood_shapefit_spectrum-poles-rotated+bao-recon_syst-rotation-hod-photo_ELG_LOPnotqso_GCcomb_z1.1-1.6_thetacut0.05.h5'
'likelihood_shapefit_spectrum-poles-rotated+bao-recon_syst-rotation-hod-photo_QSO_GCcomb_z0.8-2.1_thetacut0.05.h5'
)
need_download=0
for f in "${required_h5[@]}"; do [[ -s "$DESI_DATA/$f" ]] || need_download=1; done
if [[ "$need_download" -eq 1 ]]; then python "$DESI_REPO/dr1/cobaya/download.py" --data-dir "$DESI_DATA"; fi
for f in "${required_h5[@]}"; do [[ -s "$DESI_DATA/$f" ]] || { echo "R9B2K-DM-REPAIR01: required DESI HDF5 missing: $f" >&2; exit 4; }; done
echo STABLE_AEST_DESI_DR1_R9B2K_DM_REPAIR01_DATA_READY

R9B_PYTARGET="$ROOT/.local/classy_corrected_e8580832_densek64_stablechi_r9bdesi"
[[ -d "$R9B_PYTARGET" ]] || { echo "R9B2K-DM-REPAIR01: missing existing corrected classy target $R9B_PYTARGET" >&2; exit 3; }
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1

JSON='results/stable_aest_desi_dr1_r9b2k_shapefit_dm_repair01.json'
NPZ='results/stable_aest_desi_dr1_r9b2k_shapefit_dm_repair01.npz'
LOG='results/stable_aest_desi_dr1_r9b2k_shapefit_dm_repair01.log'
rm -f "$JSON" "$NPZ" "$LOG"

echo STABLE_AEST_DESI_DR1_R9B2K_DM_REPAIR01_START_RUN
set +e
PYTHONPATH="$R9B_PYTARGET:${PYTHONPATH:-}" python -u -m fullj_weyl.stable_aest_desi_dr1_r9b2k_shapefit_dm_repair01 \
  --data-dir "$DESI_DATA" --official-repo "$DESI_REPO" --workdir "$WORK" \
  --json-out "$JSON" --npz-out "$NPZ" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

echo "STABLE_AEST_DESI_DR1_R9B2K_DM_REPAIR01_EXIT=$code"
[[ -s "$JSON" ]] && sha256sum "$JSON"
[[ -s "$NPZ" ]] && sha256sum "$NPZ"
[[ -s "$LOG" ]] && sha256sum "$LOG"
exit "$code"
