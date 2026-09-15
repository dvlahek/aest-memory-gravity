#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

PREFIT_LOCK='950b4d37a9a6480e7f8e65d2a5a946230987b09a'
POSTDATA_LOCK='5f453a296d367556927cfa8e1e86b7ea103a9b52'
IMPLEMENTATION_LOCK='c63229f7bc9fe7137b276a5df7bf00ee97ebccb5'
R9B2_JSON_SHA='b0afd658758eb63708f837884f9e236f945879a97b56daef571abb9342ab4697'

git merge-base --is-ancestor "$PREFIT_LOCK" HEAD
git merge-base --is-ancestor "$POSTDATA_LOCK" HEAD
git merge-base --is-ancestor "$IMPLEMENTATION_LOCK" HEAD

echo "STABLE_AEST_DESI_DR1_R9B2A_LOCK_PASS prefit=$PREFIT_LOCK postdata=$POSTDATA_LOCK implementation=$IMPLEMENTATION_LOCK"

R9B2_JSON='results/stable_aest_desi_dr1_r9b2_direct_velocity_shapefit_projection.json'
[[ -s "$R9B2_JSON" ]] || { echo 'R9B2A: historical R9b2 JSON missing' >&2; exit 3; }
[[ "$(sha256sum "$R9B2_JSON" | awk '{print $1}')" == "$R9B2_JSON_SHA" ]] || { echo 'R9B2A: historical R9b2 JSON SHA mismatch' >&2; exit 3; }

BASE_PY="$(command -v python3 || command -v python || true)"
[[ -n "$BASE_PY" ]] || { echo 'R9B2A: Python missing' >&2; exit 2; }
VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then "$BASE_PY" -m venv "$VENV"; fi
export PATH="$VENV/bin:$PATH"

python -m pip install -q numpy scipy cython h5py camb
python -m pip install -q 'git+https://github.com/cosmodesi/cosmoprimo.git@2e59c963c9b8e7cba1a4c8f161e978c6f4d80c2d'
python -m py_compile fullj_weyl/stable_aest_desi_dr1_r9b2a_extraction_invariance.py

echo STABLE_AEST_DESI_DR1_R9B2A_IMPORT_PASS

R9B_ROOT="$ROOT/.local/class_corrected_e8580832_densek64_stablechi_r9bdesi"
R9B_PYTARGET="$ROOT/.local/classy_corrected_e8580832_densek64_stablechi_r9bdesi"
[[ -d "$R9B_ROOT" ]] || { echo "R9B2A: missing $R9B_ROOT" >&2; exit 3; }
[[ -d "$R9B_PYTARGET" ]] || { echo "R9B2A: missing $R9B_PYTARGET" >&2; exit 3; }

grep -q 'FULLJ_AEST_STABLE_CHI_RESIDUAL_V1' "$R9B_ROOT/source/perturbations.c"
grep -q 'FULLJ_STABLE_AEST_R7A_LIVE_EPOCH_V1' "$R9B_ROOT/source/perturbations.c"
[[ "$(grep -Fc 'Bchi_aest *= pba->aest_eta*aest_r7a_epoch_weight(a);' "$R9B_ROOT/source/perturbations.c")" -eq 1 ]]
[[ "$(grep -Fc 'E_rhs_aest -= 0.5*Q_aest*Bchi_aest;' "$R9B_ROOT/source/perturbations.c")" -eq 1 ]]

echo STABLE_AEST_DESI_DR1_R9B2A_SOURCE_PASS

export AEST_STABLE_R8A_CLASS_ROOT="$R9B_ROOT"
export AEST_R7A_EPOCH_MODE=full
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
unset AEST_R9B_DESI_DATA_DIR AEST_R9B_DESI_REPO || true
unset AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE \
  AEST_R2D_TRACE_FILE AEST_R2D_TRACE_KH AEST_R2D_TRACE_ALL_K \
  AEST_TANGENT_ALLOW_K_MISS AEST_ERHS_TRACE_FILE AEST_ERHS_TRACE_K || true

JSON='results/stable_aest_desi_dr1_r9b2a_extraction_invariance.json'
LOG='results/stable_aest_desi_dr1_r9b2a_extraction_invariance.log'
rm -f "$JSON" "$LOG"

set +e
PYTHONPATH="$R9B_PYTARGET:${PYTHONPATH:-}" python -u -m fullj_weyl.stable_aest_desi_dr1_r9b2a_extraction_invariance \
  2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

echo "STABLE_AEST_DESI_DR1_R9B2A_EXIT=$code"
echo "STABLE_AEST_DESI_DR1_R9B2A_JSON=$JSON"
echo "STABLE_AEST_DESI_DR1_R9B2A_LOG=$LOG"
exit "$code"
