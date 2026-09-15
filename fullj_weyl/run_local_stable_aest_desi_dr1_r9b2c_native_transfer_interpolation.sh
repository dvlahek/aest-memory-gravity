#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

PREFIT_LOCK='1e999d87c1158ee7be764e6055164d75a179b059'
POSTDATA_LOCK='3101581468bc8a5b85eb2b34c33df22418f1ce88'
IMPLEMENTATION_LOCK='cb15af792b6d2deca3c495a47f75238986e85c00'
ADAPTER_LOCK='f5484b4572b673dfcead51875e3aa790c698a18c'
V078_LOCK='31c05c22b86e8ac01ce822306efecdcb03cff1d5'
R9B2B_JSON_SHA='bc0013a70a1e13ef925efc39b57f8810d7c5bab80091eed1ba4407bc1862314e'
ADAPTER_JSON_SHA='c4d9281cd504785a9e4fb187b02db2860e24622bbe1ccf4a52e44446be0a119a'

for lock in "$PREFIT_LOCK" "$POSTDATA_LOCK" "$IMPLEMENTATION_LOCK" "$ADAPTER_LOCK" "$V078_LOCK"; do
  git merge-base --is-ancestor "$lock" HEAD
 done

echo "STABLE_AEST_DESI_DR1_R9B2C_LOCK_PASS prefit=$PREFIT_LOCK postdata=$POSTDATA_LOCK implementation=$IMPLEMENTATION_LOCK"

R9B2B_JSON='results/stable_aest_desi_dr1_r9b2b_source_state_extraction.json'
ADAPTER_JSON='results/stable_aest_desi_dr1_r9b2_velocity_adapter_validation.json'
[[ -s "$R9B2B_JSON" ]] || { echo 'R9B2C: R9b2b JSON missing' >&2; exit 3; }
[[ -s "$ADAPTER_JSON" ]] || { echo 'R9B2C: adapter JSON missing' >&2; exit 3; }
[[ "$(sha256sum "$R9B2B_JSON" | awk '{print $1}')" == "$R9B2B_JSON_SHA" ]] || { echo 'R9B2C: R9b2b JSON SHA mismatch' >&2; exit 3; }
[[ "$(sha256sum "$ADAPTER_JSON" | awk '{print $1}')" == "$ADAPTER_JSON_SHA" ]] || { echo 'R9B2C: adapter JSON SHA mismatch' >&2; exit 3; }
grep -q 'V078_TIME_INTERPOLATION_OPERATOR_CLOSURE_PASS' docs/v078_preserved_interpretation.md
grep -q 'V078_TIME_INTERPOLATION_OPERATOR_DISCREPANCY_LOCALIZED' docs/v078_preserved_interpretation.md

BASE_PY="$(command -v python3 || command -v python || true)"
[[ -n "$BASE_PY" ]] || { echo 'R9B2C: Python missing' >&2; exit 2; }
VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then "$BASE_PY" -m venv "$VENV"; fi
export PATH="$VENV/bin:$PATH"

python -m pip install -q numpy scipy cython h5py
python -m pip install -q 'git+https://github.com/cosmodesi/cosmoprimo.git@2e59c963c9b8e7cba1a4c8f161e978c6f4d80c2d'
python -m py_compile fullj_weyl/stable_aest_desi_dr1_r9b2c_native_transfer_interpolation.py

echo STABLE_AEST_DESI_DR1_R9B2C_IMPORT_PASS

R9B_ROOT="$ROOT/.local/class_corrected_e8580832_densek64_stablechi_r9bdesi"
R9B_PYTARGET="$ROOT/.local/classy_corrected_e8580832_densek64_stablechi_r9bdesi"
[[ -d "$R9B_ROOT" ]] || { echo "R9B2C: missing $R9B_ROOT" >&2; exit 3; }
[[ -d "$R9B_PYTARGET" ]] || { echo "R9B2C: missing $R9B_PYTARGET" >&2; exit 3; }

grep -q 'FULLJ_AEST_STABLE_CHI_RESIDUAL_V1' "$R9B_ROOT/source/perturbations.c"
grep -q 'FULLJ_STABLE_AEST_R7A_LIVE_EPOCH_V1' "$R9B_ROOT/source/perturbations.c"
[[ "$(grep -Fc 'Bchi_aest *= pba->aest_eta*aest_r7a_epoch_weight(a);' "$R9B_ROOT/source/perturbations.c")" -eq 1 ]]
[[ "$(grep -Fc 'E_rhs_aest -= 0.5*Q_aest*Bchi_aest;' "$R9B_ROOT/source/perturbations.c")" -eq 1 ]]

echo STABLE_AEST_DESI_DR1_R9B2C_SOURCE_PASS

export AEST_STABLE_R8A_CLASS_ROOT="$R9B_ROOT"
export AEST_R7A_EPOCH_MODE=full
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
unset AEST_R9B_DESI_DATA_DIR AEST_R9B_DESI_REPO || true
unset AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE \
  AEST_R2D_TRACE_FILE AEST_R2D_TRACE_KH AEST_R2D_TRACE_ALL_K \
  AEST_TANGENT_ALLOW_K_MISS AEST_ERHS_TRACE_FILE AEST_ERHS_TRACE_K || true

JSON='results/stable_aest_desi_dr1_r9b2c_native_transfer_interpolation.json'
LOG='results/stable_aest_desi_dr1_r9b2c_native_transfer_interpolation.log'
rm -f "$JSON" "$LOG"

set +e
PYTHONPATH="$R9B_PYTARGET:${PYTHONPATH:-}" python -u -m fullj_weyl.stable_aest_desi_dr1_r9b2c_native_transfer_interpolation \
  2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

echo "STABLE_AEST_DESI_DR1_R9B2C_EXIT=$code"
echo "STABLE_AEST_DESI_DR1_R9B2C_JSON=$JSON"
echo "STABLE_AEST_DESI_DR1_R9B2C_LOG=$LOG"
exit "$code"
