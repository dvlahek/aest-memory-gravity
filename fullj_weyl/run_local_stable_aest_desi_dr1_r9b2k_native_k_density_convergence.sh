#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

PREFIT_LOCK='cbd4cd2a0fbf8315de3db7dee054e2fbf845f7c8'
POSTDATA_LOCK='ce3d170e68244d6bbfea5374e6a5a5f7cc4efbc4'
IMPLEMENTATION_LOCK='874218ec2db38f505307b8183e199fe9d4c73d98'
R9B2J_JSON='results/stable_aest_desi_dr1_r9b2j_signed_response_shapefit_repair01.json'
R9B2J_SHA='e61b05279e0b2cb58c12a66cc0455f4c894ba5be2ec7d656be13cf6b8cf8c602'
DESI_COMMIT='7d51f4f86dc3bee6bf10f1a684913c943a89a844'
LSSTYPES_COMMIT='53f048e610bcb008548f66822b0879ce9df58cb1'
COSMOPRIMO_COMMIT='2e59c963c9b8e7cba1a4c8f161e978c6f4d80c2d'

for lock in "$PREFIT_LOCK" "$POSTDATA_LOCK" "$IMPLEMENTATION_LOCK"; do
  git merge-base --is-ancestor "$lock" HEAD
 done
[[ -s "$R9B2J_JSON" ]] || { echo 'R9B2K: completed R9b2j Repair01 JSON missing' >&2; exit 3; }
[[ "$(sha256sum "$R9B2J_JSON" | awk '{print $1}')" == "$R9B2J_SHA" ]] || { echo 'R9B2K: R9b2j Repair01 JSON SHA mismatch' >&2; exit 3; }
echo "STABLE_AEST_DESI_DR1_R9B2K_LOCK_PASS prefit=$PREFIT_LOCK postdata=$POSTDATA_LOCK implementation=$IMPLEMENTATION_LOCK r9b2j=$R9B2J_SHA"

BASE_PY="$(command -v python3 || command -v python || true)"
[[ -n "$BASE_PY" ]] || { echo 'R9B2K: Python missing' >&2; exit 2; }
VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then "$BASE_PY" -m venv "$VENV"; fi
export PATH="$VENV/bin:$PATH"
python -m pip install -q numpy scipy cython requests beautifulsoup4 h5py camb
python -m pip install -q "git+https://github.com/adematti/lsstypes.git@$LSSTYPES_COMMIT"
python -m pip install -q "git+https://github.com/cosmodesi/cosmoprimo.git@$COSMOPRIMO_COMMIT"
python -m py_compile \
  fullj_weyl/stable_aest_desi_dr1_r9b2k_native_k_density_convergence.py \
  fullj_weyl/stable_aest_desi_dr1_r9b2j_signed_response_shapefit_repair01.py \
  fullj_weyl/stable_aest_desi_dr1_r9b2j_signed_response_shapefit.py \
  fullj_weyl/stable_aest_desi_dr1_r9b2i_native_variance_response_shapefit.py

python - <<'PY'
from pathlib import Path
p=Path('fullj_weyl/stable_aest_desi_dr1_r9b2k_native_k_density_convergence.py').read_text()
for token in (
    '"D1": (80.0, 560.0)',
    '"D2": (160.0, 1120.0)',
    'p["k_per_decade_for_pk"] = float(kp)',
    'p["k_per_decade_for_bao"] = float(kb)',
    'n2 > n1 > DEFAULT_NK',
    'R9B2K_K5_native_density_convergence',
    'R9B2K_K6_cross_operator',
    'STABLE_AEST_DESI_DR1_R9B2K_NATIVE_K_DENSITY_SHAPEFIT_CERTIFIED',
    'r01.source_shape_saved(row, fid, fcache)',
):
    assert token in p, token
assert 'pk_cb_lin(' not in p
assert 'E_GATE = j.E_GATE' in p and 'C_GATE = j.C_GATE' in p
print('STABLE_AEST_DESI_DR1_R9B2K_IMPORT_PASS')
PY

R9B_ROOT="$ROOT/.local/class_corrected_e8580832_densek64_stablechi_r9bdesi"
R9B_PYTARGET="$ROOT/.local/classy_corrected_e8580832_densek64_stablechi_r9bdesi"
[[ -d "$R9B_ROOT" ]] || { echo "R9B2K: missing corrected CLASS source $R9B_ROOT" >&2; exit 3; }
[[ -d "$R9B_PYTARGET" ]] || { echo "R9B2K: missing corrected classy target $R9B_PYTARGET" >&2; exit 3; }
[[ "$(git -C "$R9B_ROOT" rev-parse HEAD)" == 'e85808324f51fc694d12e3ed7439552a3c3f9540' ]]
grep -q 'FULLJ_AEST_STABLE_CHI_RESIDUAL_V1' "$R9B_ROOT/source/perturbations.c"
grep -q 'FULLJ_STABLE_AEST_R7A_LIVE_EPOCH_V1' "$R9B_ROOT/source/perturbations.c"
[[ "$(grep -Fc 'Bchi_aest *= pba->aest_eta*aest_r7a_epoch_weight(a);' "$R9B_ROOT/source/perturbations.c")" -eq 1 ]]
[[ "$(grep -Fc 'E_rhs_aest -= 0.5*Q_aest*Bchi_aest;' "$R9B_ROOT/source/perturbations.c")" -eq 1 ]]
echo STABLE_AEST_DESI_DR1_R9B2K_SOURCE_PASS

DESI_REPO="$ROOT/.local/desi_kp_likelihoods_r9b"
if [[ ! -d "$DESI_REPO/.git" ]] || [[ "$(git -C "$DESI_REPO" rev-parse HEAD 2>/dev/null || true)" != "$DESI_COMMIT" ]]; then
  rm -rf "$DESI_REPO"
  git clone -q https://github.com/cosmodesi/desi-kp-cosmological-likelihoods.git "$DESI_REPO"
  git -C "$DESI_REPO" checkout -q "$DESI_COMMIT"
fi
[[ "$(git -C "$DESI_REPO" rev-parse HEAD)" == "$DESI_COMMIT" ]]

echo "STABLE_AEST_DESI_DR1_R9B2K_OFFICIAL_REPO_PASS head=$DESI_COMMIT"
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
for f in "${required_h5[@]}"; do [[ -s "$DESI_DATA/$f" ]] || { echo "R9B2K: required DESI HDF5 missing: $f" >&2; exit 4; }; done
echo STABLE_AEST_DESI_DR1_R9B2K_DATA_READY

export AEST_STABLE_R8A_CLASS_ROOT="$R9B_ROOT"
export AEST_R9B_DESI_DATA_DIR="$DESI_DATA"
export AEST_R9B_DESI_REPO="$DESI_REPO"
export AEST_R7A_EPOCH_MODE=full
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
unset AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE \
  AEST_R2D_TRACE_FILE AEST_R2D_TRACE_KH AEST_R2D_TRACE_ALL_K \
  AEST_ERHS_TRACE_FILE AEST_ERHS_TRACE_K || true

JSON='results/stable_aest_desi_dr1_r9b2k_native_k_density_convergence.json'
NPZ='results/stable_aest_desi_dr1_r9b2k_native_k_density_convergence.npz'
LOG='results/stable_aest_desi_dr1_r9b2k_native_k_density_convergence.log'
WORK='results/stable_aest_desi_dr1_r9b2k_work'
rm -f "$JSON" "$NPZ" "$LOG"
mkdir -p "$WORK"

echo 'STABLE_AEST_DESI_DR1_R9B2K_MEMORY_BEFORE'
free -h || true

set +e
PYTHONPATH="$R9B_PYTARGET:${PYTHONPATH:-}" python -u -m fullj_weyl.stable_aest_desi_dr1_r9b2k_native_k_density_convergence \
  --data-dir "$DESI_DATA" --official-repo "$DESI_REPO" \
  --json-out "$JSON" --npz-out "$NPZ" --workdir "$WORK" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

echo 'STABLE_AEST_DESI_DR1_R9B2K_MEMORY_AFTER'
free -h || true
echo "STABLE_AEST_DESI_DR1_R9B2K_EXIT=$code"
[[ -s "$JSON" ]] && sha256sum "$JSON"
[[ -s "$LOG" ]] && sha256sum "$LOG"
echo "STABLE_AEST_DESI_DR1_R9B2K_WORK=$WORK"
exit "$code"
