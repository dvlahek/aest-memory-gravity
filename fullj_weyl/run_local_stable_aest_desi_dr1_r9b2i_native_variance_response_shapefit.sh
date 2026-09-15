#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

PREFIT_LOCK='f7d05f034046388833b74f990c071e65b0ab2f14'
POSTDATA_LOCK='ffd0a10892c65bf71f134c6d9e78dc9dc13f1a16'
IMPLEMENTATION_LOCK='44bd66e087e1519f1ea0d41513c779ccc3be832d'
R9B2H_JSON='results/stable_aest_desi_dr1_r9b2h_derivative_stable_quadrature.json'
R9B2H_SHA='7cdf0f17572c351acb118e858a8fc5c206484fa6af2cf8e66531b8cd5927eea2'
DESI_COMMIT='7d51f4f86dc3bee6bf10f1a684913c943a89a844'
LSSTYPES_COMMIT='53f048e610bcb008548f66822b0879ce9df58cb1'
COSMOPRIMO_COMMIT='2e59c963c9b8e7cba1a4c8f161e978c6f4d80c2d'

for lock in "$PREFIT_LOCK" "$POSTDATA_LOCK" "$IMPLEMENTATION_LOCK"; do
  git merge-base --is-ancestor "$lock" HEAD
 done
[[ -s "$R9B2H_JSON" ]] || { echo 'R9B2I: local completed R9b2h JSON missing' >&2; exit 3; }
[[ "$(sha256sum "$R9B2H_JSON" | awk '{print $1}')" == "$R9B2H_SHA" ]] || { echo 'R9B2I: R9b2h JSON SHA mismatch' >&2; exit 3; }
echo "STABLE_AEST_DESI_DR1_R9B2I_LOCK_PASS prefit=$PREFIT_LOCK postdata=$POSTDATA_LOCK implementation=$IMPLEMENTATION_LOCK"

BASE_PY="$(command -v python3 || command -v python || true)"
[[ -n "$BASE_PY" ]] || { echo 'R9B2I: Python missing' >&2; exit 2; }
VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then "$BASE_PY" -m venv "$VENV"; fi
export PATH="$VENV/bin:$PATH"
python -m pip install -q numpy scipy cython requests beautifulsoup4 h5py camb
python -m pip install -q "git+https://github.com/adematti/lsstypes.git@$LSSTYPES_COMMIT"
python -m pip install -q "git+https://github.com/cosmodesi/cosmoprimo.git@$COSMOPRIMO_COMMIT"
python -m py_compile \
  fullj_weyl/stable_aest_desi_dr1_r9b2i_native_variance_response_shapefit.py \
  fullj_weyl/stable_aest_desi_dr1_r9b2f_full_grid_rogue_node.py \
  fullj_weyl/stable_aest_desi_dr1_r9b_shapefit_projection.py
python - <<'PY'
from pathlib import Path
p=Path('fullj_weyl/stable_aest_desi_dr1_r9b2i_native_variance_response_shapefit.py').read_text()
required=[
 'D_dd = [P_dd(+epsilon)-P_dd(-epsilon)]/(2 epsilon)',
]
# executable anti-stale checks use implementation tokens, not the prose prereg expression above
for token in ('Dd=(np.asarray(sp["pdd"])-np.asarray(sm["pdd"]))/(2.0*eps)',
              'Dt=(np.asarray(sp["ptt"])-np.asarray(sm["ptt"]))/(2.0*eps)',
              'simpson(y, x=x)', 'np.trapezoid(y, x=x)',
              'E_GATE = 0.05', 'C_GATE = 0.995',
              'STABLE_AEST_DESI_DR1_R9B2I_NATIVE_VARIANCE_RESPONSE_SHAPEFIT_CERTIFIED'):
    assert token in p, token
assert 'PowerSpectrumInterpolator1D' not in p
print('STABLE_AEST_DESI_DR1_R9B2I_IMPORT_PASS')
PY

# Reuse the corrected stable-AeST CLASS build from the completed R9b2 series.
R9B_ROOT="$ROOT/.local/class_corrected_e8580832_densek64_stablechi_r9bdesi"
R9B_PYTARGET="$ROOT/.local/classy_corrected_e8580832_densek64_stablechi_r9bdesi"
[[ -d "$R9B_ROOT" ]] || { echo "R9B2I: missing corrected CLASS source $R9B_ROOT" >&2; exit 3; }
[[ -d "$R9B_PYTARGET" ]] || { echo "R9B2I: missing corrected classy target $R9B_PYTARGET" >&2; exit 3; }
[[ "$(git -C "$R9B_ROOT" rev-parse HEAD)" == 'e85808324f51fc694d12e3ed7439552a3c3f9540' ]]
grep -q 'FULLJ_AEST_STABLE_CHI_RESIDUAL_V1' "$R9B_ROOT/source/perturbations.c"
grep -q 'FULLJ_STABLE_AEST_R7A_LIVE_EPOCH_V1' "$R9B_ROOT/source/perturbations.c"
[[ "$(grep -Fc 'Bchi_aest *= pba->aest_eta*aest_r7a_epoch_weight(a);' "$R9B_ROOT/source/perturbations.c")" -eq 1 ]]
[[ "$(grep -Fc 'E_rhs_aest -= 0.5*Q_aest*Bchi_aest;' "$R9B_ROOT/source/perturbations.c")" -eq 1 ]]
echo STABLE_AEST_DESI_DR1_R9B2I_SOURCE_PASS

# Reuse official DESI checkout if it is still exactly pinned; otherwise recreate it.
DESI_REPO="$ROOT/.local/desi_kp_likelihoods_r9b"
if [[ ! -d "$DESI_REPO/.git" ]] || [[ "$(git -C "$DESI_REPO" rev-parse HEAD 2>/dev/null || true)" != "$DESI_COMMIT" ]]; then
  rm -rf "$DESI_REPO"
  git clone -q https://github.com/cosmodesi/desi-kp-cosmological-likelihoods.git "$DESI_REPO"
  git -C "$DESI_REPO" checkout -q "$DESI_COMMIT"
fi
[[ "$(git -C "$DESI_REPO" rev-parse HEAD)" == "$DESI_COMMIT" ]]
echo "STABLE_AEST_DESI_DR1_R9B2I_OFFICIAL_REPO_PASS head=$DESI_COMMIT"

# Reuse the official R9b DESI files when present. Download only if a required file is missing.
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
MANIFEST='results/stable_aest_desi_dr1_r9b2i_data_manifest.txt'
: > "$MANIFEST"
for f in "${required_h5[@]}"; do
  [[ -s "$DESI_DATA/$f" ]] || { echo "R9B2I: required DESI HDF5 missing: $f" >&2; exit 4; }
  sha256sum "$DESI_DATA/$f" >> "$MANIFEST"
done
echo STABLE_AEST_DESI_DR1_R9B2I_DATA_READY

export AEST_STABLE_R8A_CLASS_ROOT="$R9B_ROOT"
export AEST_R9B_DESI_DATA_DIR="$DESI_DATA"
export AEST_R9B_DESI_REPO="$DESI_REPO"
export AEST_R7A_EPOCH_MODE=full
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
unset AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE \
  AEST_R2D_TRACE_FILE AEST_R2D_TRACE_KH AEST_R2D_TRACE_ALL_K \
  AEST_TANGENT_ALLOW_K_MISS AEST_ERHS_TRACE_FILE AEST_ERHS_TRACE_K || true

JSON='results/stable_aest_desi_dr1_r9b2i_native_variance_response_shapefit.json'
NPZ='results/stable_aest_desi_dr1_r9b2i_native_variance_response_shapefit.npz'
LOG='results/stable_aest_desi_dr1_r9b2i_native_variance_response_shapefit.log'
ENVOUT='results/stable_aest_desi_dr1_r9b2i_environment.txt'
rm -f "$JSON" "$NPZ" "$LOG" "$ENVOUT"
{
  echo "repo_head=$(git rev-parse HEAD)"
  echo "prefit_lock=$PREFIT_LOCK"
  echo "postdata_lock=$POSTDATA_LOCK"
  echo "implementation_lock=$IMPLEMENTATION_LOCK"
  echo "desi_repo_commit=$DESI_COMMIT"
  echo "class_parent_head=$(git -C "$R9B_ROOT" rev-parse HEAD)"
  echo "python=$(python --version 2>&1)"
  echo '--- DESI HDF5 manifest ---'
  cat "$MANIFEST"
  echo '--- pip freeze ---'
  python -m pip freeze
} > "$ENVOUT"

set +e
PYTHONPATH="$R9B_PYTARGET:${PYTHONPATH:-}" python -u -m fullj_weyl.stable_aest_desi_dr1_r9b2i_native_variance_response_shapefit \
  --data-dir "$DESI_DATA" --official-repo "$DESI_REPO" --json-out "$JSON" --npz-out "$NPZ" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

echo "STABLE_AEST_DESI_DR1_R9B2I_EXIT=$code"
echo "STABLE_AEST_DESI_DR1_R9B2I_JSON=$JSON"
echo "STABLE_AEST_DESI_DR1_R9B2I_NPZ=$NPZ"
echo "STABLE_AEST_DESI_DR1_R9B2I_LOG=$LOG"
[[ -f "$JSON" ]] && sha256sum "$JSON"
[[ -f "$NPZ" ]] && sha256sum "$NPZ"
[[ -f "$LOG" ]] && sha256sum "$LOG"
exit "$code"
