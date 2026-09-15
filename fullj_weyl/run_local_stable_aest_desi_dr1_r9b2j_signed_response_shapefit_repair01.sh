#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

REPAIR_PREFIT='040d169407d4bdde0f59f9b15380c3623a5abfe8'
REPAIR_IMPL='ba2ee3afecce27485ffa606586ba129fdc89c2d8'
ORIGINAL_PREFIT='dbf354f4ef3122fff44b1b389f1adc839e9e7f9d'
ORIGINAL_IMPL='342ab7d85366e4f4521a7e3e2d19741e878aec3a'
ORIGINAL_RUNNER='2e3bf71cb403e9c31782d2afd142a2c87fe01e79'
R9B2I_JSON='results/stable_aest_desi_dr1_r9b2i_native_variance_response_shapefit.json'
R9B2I_SHA='859d92d849c295d3a5219980a9caa82c283952f814e98df19a1b44ca5fe97164'
DESI_COMMIT='7d51f4f86dc3bee6bf10f1a684913c943a89a844'
LSSTYPES_COMMIT='53f048e610bcb008548f66822b0879ce9df58cb1'
COSMOPRIMO_COMMIT='2e59c963c9b8e7cba1a4c8f161e978c6f4d80c2d'

for lock in "$REPAIR_PREFIT" "$REPAIR_IMPL" "$ORIGINAL_PREFIT" "$ORIGINAL_IMPL" "$ORIGINAL_RUNNER"; do
  git merge-base --is-ancestor "$lock" HEAD
 done
[[ -s "$R9B2I_JSON" ]] || { echo 'R9B2J-R01: completed R9b2i JSON missing' >&2; exit 3; }
[[ "$(sha256sum "$R9B2I_JSON" | awk '{print $1}')" == "$R9B2I_SHA" ]] || { echo 'R9B2J-R01: R9b2i JSON SHA mismatch' >&2; exit 3; }
echo "STABLE_AEST_DESI_DR1_R9B2J_REPAIR01_LOCK_PASS prefit=$REPAIR_PREFIT implementation=$REPAIR_IMPL r9b2i=$R9B2I_SHA"

BASE_PY="$(command -v python3 || command -v python || true)"
[[ -n "$BASE_PY" ]] || { echo 'R9B2J-R01: Python missing' >&2; exit 2; }
VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then "$BASE_PY" -m venv "$VENV"; fi
export PATH="$VENV/bin:$PATH"
python -m pip install -q numpy scipy cython requests beautifulsoup4 h5py camb
python -m pip install -q "git+https://github.com/adematti/lsstypes.git@$LSSTYPES_COMMIT"
python -m pip install -q "git+https://github.com/cosmodesi/cosmoprimo.git@$COSMOPRIMO_COMMIT"
python -m py_compile \
  fullj_weyl/stable_aest_desi_dr1_r9b2j_signed_response_shapefit_repair01.py \
  fullj_weyl/stable_aest_desi_dr1_r9b2j_signed_response_shapefit.py \
  fullj_weyl/stable_aest_desi_dr1_r9b2i_native_variance_response_shapefit.py
python - <<'PY'
from pathlib import Path
p=Path('fullj_weyl/stable_aest_desi_dr1_r9b2j_signed_response_shapefit_repair01.py').read_text()
for token in (
 'subprocess.run(cmd,env=os.environ.copy())',
 'checkpoint_reused',
 'STABLE_AEST_DESI_DR1_R9B2J_REPAIR01_STAGE_A_PASS_LOADING_DESI',
 'fid,fcache=r9b._get_fiducial_cache(ZEFF)',
 'source_shape_saved(row,fid,fcache)',
 'science_definition":"unchanged from R9b2j preregistration"',
): assert token in p, token
assert p.index('STABLE_AEST_DESI_DR1_R9B2J_REPAIR01_STAGE_A_PASS_LOADING_DESI') < p.index('fid,fcache=r9b._get_fiducial_cache(ZEFF)')
print('STABLE_AEST_DESI_DR1_R9B2J_REPAIR01_IMPORT_PASS')
PY

R9B_ROOT="$ROOT/.local/class_corrected_e8580832_densek64_stablechi_r9bdesi"
R9B_PYTARGET="$ROOT/.local/classy_corrected_e8580832_densek64_stablechi_r9bdesi"
[[ -d "$R9B_ROOT" ]] || { echo "R9B2J-R01: missing corrected CLASS source $R9B_ROOT" >&2; exit 3; }
[[ -d "$R9B_PYTARGET" ]] || { echo "R9B2J-R01: missing corrected classy target $R9B_PYTARGET" >&2; exit 3; }
[[ "$(git -C "$R9B_ROOT" rev-parse HEAD)" == 'e85808324f51fc694d12e3ed7439552a3c3f9540' ]]
grep -q 'FULLJ_AEST_STABLE_CHI_RESIDUAL_V1' "$R9B_ROOT/source/perturbations.c"
grep -q 'FULLJ_STABLE_AEST_R7A_LIVE_EPOCH_V1' "$R9B_ROOT/source/perturbations.c"
echo STABLE_AEST_DESI_DR1_R9B2J_REPAIR01_SOURCE_PASS

DESI_REPO="$ROOT/.local/desi_kp_likelihoods_r9b"
if [[ ! -d "$DESI_REPO/.git" ]] || [[ "$(git -C "$DESI_REPO" rev-parse HEAD 2>/dev/null || true)" != "$DESI_COMMIT" ]]; then
  rm -rf "$DESI_REPO"
  git clone -q https://github.com/cosmodesi/desi-kp-cosmological-likelihoods.git "$DESI_REPO"
  git -C "$DESI_REPO" checkout -q "$DESI_COMMIT"
fi
[[ "$(git -C "$DESI_REPO" rev-parse HEAD)" == "$DESI_COMMIT" ]]
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
for f in "${required_h5[@]}"; do [[ -s "$DESI_DATA/$f" ]] || { echo "R9B2J-R01: required DESI HDF5 missing: $f" >&2; exit 4; }; done
echo STABLE_AEST_DESI_DR1_R9B2J_REPAIR01_DATA_READY

export AEST_STABLE_R8A_CLASS_ROOT="$R9B_ROOT"
export AEST_R9B_DESI_DATA_DIR="$DESI_DATA"
export AEST_R9B_DESI_REPO="$DESI_REPO"
export AEST_R7A_EPOCH_MODE=full
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
unset AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE AEST_R2D_TRACE_FILE AEST_R2D_TRACE_KH AEST_R2D_TRACE_ALL_K AEST_ERHS_TRACE_FILE AEST_ERHS_TRACE_K || true

JSON='results/stable_aest_desi_dr1_r9b2j_signed_response_shapefit_repair01.json'
NPZ='results/stable_aest_desi_dr1_r9b2j_signed_response_shapefit_repair01.npz'
LOG='results/stable_aest_desi_dr1_r9b2j_signed_response_shapefit_repair01.log'
WORK='results/stable_aest_desi_dr1_r9b2j_repair01_work'
rm -f "$JSON" "$NPZ" "$LOG"
mkdir -p "$WORK"

set +e
PYTHONPATH="$R9B_PYTARGET:${PYTHONPATH:-}" python -u -m fullj_weyl.stable_aest_desi_dr1_r9b2j_signed_response_shapefit_repair01 \
  --data-dir "$DESI_DATA" --official-repo "$DESI_REPO" --json-out "$JSON" --npz-out "$NPZ" --workdir "$WORK" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

echo "STABLE_AEST_DESI_DR1_R9B2J_REPAIR01_EXIT=$code"
[[ -s "$JSON" ]] && sha256sum "$JSON"
[[ -s "$LOG" ]] && sha256sum "$LOG"
echo "STABLE_AEST_DESI_DR1_R9B2J_REPAIR01_WORK=$WORK"
exit "$code"