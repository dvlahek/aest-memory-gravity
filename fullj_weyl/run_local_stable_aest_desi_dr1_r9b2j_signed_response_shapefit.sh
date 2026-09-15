#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

PREFIT_LOCK='dbf354f4ef3122fff44b1b389f1adc839e9e7f9d'
IMPLEMENTATION_LOCK='342ab7d85366e4f4521a7e3e2d19741e878aec3a'
R9B2I_RUNNER_LOCK='2264f6dace0e6da1c4e9966f01d446d0de7e68a0'
R9B2I_JSON='results/stable_aest_desi_dr1_r9b2i_native_variance_response_shapefit.json'
R9B2I_SHA='859d92d849c295d3a5219980a9caa82c283952f814e98df19a1b44ca5fe97164'
DESI_COMMIT='7d51f4f86dc3bee6bf10f1a684913c943a89a844'
LSSTYPES_COMMIT='53f048e610bcb008548f66822b0879ce9df58cb1'
COSMOPRIMO_COMMIT='2e59c963c9b8e7cba1a4c8f161e978c6f4d80c2d'

for lock in "$PREFIT_LOCK" "$IMPLEMENTATION_LOCK" "$R9B2I_RUNNER_LOCK"; do
  git merge-base --is-ancestor "$lock" HEAD
 done
[[ -s "$R9B2I_JSON" ]] || { echo 'R9B2J: completed local R9b2i JSON missing' >&2; exit 3; }
[[ "$(sha256sum "$R9B2I_JSON" | awk '{print $1}')" == "$R9B2I_SHA" ]] || { echo 'R9B2J: R9b2i JSON SHA mismatch' >&2; exit 3; }
echo "STABLE_AEST_DESI_DR1_R9B2J_LOCK_PASS prefit=$PREFIT_LOCK implementation=$IMPLEMENTATION_LOCK r9b2i=$R9B2I_SHA"

BASE_PY="$(command -v python3 || command -v python || true)"
[[ -n "$BASE_PY" ]] || { echo 'R9B2J: Python missing' >&2; exit 2; }
VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then "$BASE_PY" -m venv "$VENV"; fi
export PATH="$VENV/bin:$PATH"
python -m pip install -q numpy scipy cython requests beautifulsoup4 h5py camb
python -m pip install -q "git+https://github.com/adematti/lsstypes.git@$LSSTYPES_COMMIT"
python -m pip install -q "git+https://github.com/cosmodesi/cosmoprimo.git@$COSMOPRIMO_COMMIT"
python -m py_compile \
  fullj_weyl/stable_aest_desi_dr1_r9b2j_signed_response_shapefit.py \
  fullj_weyl/stable_aest_desi_dr1_r9b2i_native_variance_response_shapefit.py \
  fullj_weyl/stable_aest_desi_dr1_r9b2f_full_grid_rogue_node.py \
  fullj_weyl/stable_aest_desi_dr1_r9b_shapefit_projection.py

python - <<'PY'
from pathlib import Path
p=Path('fullj_weyl/stable_aest_desi_dr1_r9b2j_signed_response_shapefit.py').read_text()
required=(
 'Dd=(np.asarray(sp["pdd"],float)-np.asarray(sm["pdd"],float))/(2.*eps)',
 'Dt=(np.asarray(sp["ptt"],float)-np.asarray(sm["ptt"],float))/(2.*eps)',
 'PchipInterpolator(x,dpk,extrapolate=False)',
 'np.interp(xg,x,dpk)',
 'linear4096', 'linear8192', 'linear16384', 'pchip8192',
 'STABLE_AEST_DESI_DR1_R9B2J_SIGNED_RESPONSE_SHAPEFIT_CERTIFIED',
 'source_shape(c,st,float(z),fid,fcache)',
)
for token in required: assert token in p, token
assert 'c.pk_cb_lin' not in p
assert 'E_GATE=i.E_GATE' in p and 'C_GATE=i.C_GATE' in p
print('STABLE_AEST_DESI_DR1_R9B2J_IMPORT_PASS')
PY

R9B_ROOT="$ROOT/.local/class_corrected_e8580832_densek64_stablechi_r9bdesi"
R9B_PYTARGET="$ROOT/.local/classy_corrected_e8580832_densek64_stablechi_r9bdesi"
[[ -d "$R9B_ROOT" ]] || { echo "R9B2J: missing corrected CLASS source $R9B_ROOT" >&2; exit 3; }
[[ -d "$R9B_PYTARGET" ]] || { echo "R9B2J: missing corrected classy target $R9B_PYTARGET" >&2; exit 3; }
[[ "$(git -C "$R9B_ROOT" rev-parse HEAD)" == 'e85808324f51fc694d12e3ed7439552a3c3f9540' ]]
grep -q 'FULLJ_AEST_STABLE_CHI_RESIDUAL_V1' "$R9B_ROOT/source/perturbations.c"
grep -q 'FULLJ_STABLE_AEST_R7A_LIVE_EPOCH_V1' "$R9B_ROOT/source/perturbations.c"
[[ "$(grep -Fc 'Bchi_aest *= pba->aest_eta*aest_r7a_epoch_weight(a);' "$R9B_ROOT/source/perturbations.c")" -eq 1 ]]
[[ "$(grep -Fc 'E_rhs_aest -= 0.5*Q_aest*Bchi_aest;' "$R9B_ROOT/source/perturbations.c")" -eq 1 ]]
echo STABLE_AEST_DESI_DR1_R9B2J_SOURCE_PASS

DESI_REPO="$ROOT/.local/desi_kp_likelihoods_r9b"
if [[ ! -d "$DESI_REPO/.git" ]] || [[ "$(git -C "$DESI_REPO" rev-parse HEAD 2>/dev/null || true)" != "$DESI_COMMIT" ]]; then
  rm -rf "$DESI_REPO"
  git clone -q https://github.com/cosmodesi/desi-kp-cosmological-likelihoods.git "$DESI_REPO"
  git -C "$DESI_REPO" checkout -q "$DESI_COMMIT"
fi
[[ "$(git -C "$DESI_REPO" rev-parse HEAD)" == "$DESI_COMMIT" ]]
echo "STABLE_AEST_DESI_DR1_R9B2J_OFFICIAL_REPO_PASS head=$DESI_COMMIT"

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
if [[ "$need_download" -eq 1 ]]; then
  python "$DESI_REPO/dr1/cobaya/download.py" --data-dir "$DESI_DATA"
fi
for f in "${required_h5[@]}"; do [[ -s "$DESI_DATA/$f" ]] || { echo "R9B2J: required DESI HDF5 missing: $f" >&2; exit 4; }; done
echo STABLE_AEST_DESI_DR1_R9B2J_DATA_READY

export AEST_STABLE_R8A_CLASS_ROOT="$R9B_ROOT"
export AEST_R9B_DESI_DATA_DIR="$DESI_DATA"
export AEST_R9B_DESI_REPO="$DESI_REPO"
export AEST_R7A_EPOCH_MODE=full
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
unset AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE AEST_R2D_TRACE_FILE AEST_R2D_TRACE_KH AEST_R2D_TRACE_ALL_K AEST_ERHS_TRACE_FILE AEST_ERHS_TRACE_K || true

JSON='results/stable_aest_desi_dr1_r9b2j_signed_response_shapefit.json'
NPZ='results/stable_aest_desi_dr1_r9b2j_signed_response_shapefit.npz'
LOG='results/stable_aest_desi_dr1_r9b2j_signed_response_shapefit.log'
rm -f "$JSON" "$NPZ" "$LOG"

set +e
PYTHONPATH="$R9B_PYTARGET:${PYTHONPATH:-}" python -u -m fullj_weyl.stable_aest_desi_dr1_r9b2j_signed_response_shapefit \
  --data-dir "$DESI_DATA" --official-repo "$DESI_REPO" --json-out "$JSON" --npz-out "$NPZ" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

echo "STABLE_AEST_DESI_DR1_R9B2J_EXIT=$code"
[[ -s "$JSON" ]] && sha256sum "$JSON"
[[ -s "$LOG" ]] && sha256sum "$LOG"
exit "$code"
