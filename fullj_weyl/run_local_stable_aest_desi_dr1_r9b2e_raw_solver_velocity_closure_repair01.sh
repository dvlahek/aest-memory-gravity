#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

ORIGINAL_PREFIT_LOCK='756eb268bdc4d0c3ba8dc6bfa94ba74eb11bdab1'
ORIGINAL_POSTDATA_LOCK='6b26243f78b477f7d4040c6499085faf05e8ffac'
ORIGINAL_IMPLEMENTATION_LOCK='4fedc11b3d501ea486c9838506b487789203b66c'
REPAIR_PREFIT_LOCK='28e98f6490ab02a979461b150af972898156d1fa'
REPAIR_IMPLEMENTATION_LOCK='02c95668f655afe96c9351b573c020cb1f241acb'
R9B2D_JSON='results/stable_aest_desi_dr1_r9b2d_kgrid_inheritance.json'
R9B2D_JSON_SHA='54db5acc49d4099d1173aa029a58e02cdac0e844c03aa72d95fa08b86a6f70df'

for lock in "$ORIGINAL_PREFIT_LOCK" "$ORIGINAL_POSTDATA_LOCK" "$ORIGINAL_IMPLEMENTATION_LOCK" \
            "$REPAIR_PREFIT_LOCK" "$REPAIR_IMPLEMENTATION_LOCK"; do
  git merge-base --is-ancestor "$lock" HEAD
done

echo "STABLE_AEST_DESI_DR1_R9B2E_REPAIR01_LOCK_PASS repair_prefit=$REPAIR_PREFIT_LOCK repair_implementation=$REPAIR_IMPLEMENTATION_LOCK"

[[ -s "$R9B2D_JSON" ]] || { echo 'R9B2E repair01: R9b2d JSON missing' >&2; exit 3; }
[[ "$(sha256sum "$R9B2D_JSON" | awk '{print $1}')" == "$R9B2D_JSON_SHA" ]] || { echo 'R9B2E repair01: R9b2d JSON SHA mismatch' >&2; exit 3; }

BASE_PY="$(command -v python3 || command -v python || true)"
[[ -n "$BASE_PY" ]] || { echo 'R9B2E repair01: Python missing' >&2; exit 2; }
VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then "$BASE_PY" -m venv "$VENV"; fi
export PATH="$VENV/bin:$PATH"
python -m pip install -q numpy scipy cython h5py
python -m py_compile \
  fullj_weyl/stable_aest_desi_dr1_r9b2e_raw_solver_velocity_closure.py \
  fullj_weyl/stable_aest_desi_dr1_r9b2e_raw_solver_velocity_closure_repair01.py
echo STABLE_AEST_DESI_DR1_R9B2E_REPAIR01_IMPORT_PASS

R9B_ROOT="$ROOT/.local/class_corrected_e8580832_densek64_stablechi_r9bdesi"
R9B_PYTARGET="$ROOT/.local/classy_corrected_e8580832_densek64_stablechi_r9bdesi"
[[ -d "$R9B_ROOT" ]] || { echo "R9B2E repair01: missing $R9B_ROOT" >&2; exit 3; }
[[ -d "$R9B_PYTARGET" ]] || { echo "R9B2E repair01: missing $R9B_PYTARGET" >&2; exit 3; }
grep -q 'FULLJ_AEST_STABLE_CHI_RESIDUAL_V1' "$R9B_ROOT/source/perturbations.c"
grep -q 'FULLJ_STABLE_AEST_R7A_LIVE_EPOCH_V1' "$R9B_ROOT/source/perturbations.c"
[[ "$(grep -Fc 'Bchi_aest *= pba->aest_eta*aest_r7a_epoch_weight(a);' "$R9B_ROOT/source/perturbations.c")" -eq 1 ]]
[[ "$(grep -Fc 'E_rhs_aest -= 0.5*Q_aest*Bchi_aest;' "$R9B_ROOT/source/perturbations.c")" -eq 1 ]]
echo STABLE_AEST_DESI_DR1_R9B2E_REPAIR01_SOURCE_PASS

export AEST_STABLE_R8A_CLASS_ROOT="$R9B_ROOT"
export AEST_R7A_EPOCH_MODE=full
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
unset AEST_R9B_DESI_DATA_DIR AEST_R9B_DESI_REPO || true
unset AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE \
  AEST_R2D_TRACE_FILE AEST_R2D_TRACE_KH AEST_R2D_TRACE_ALL_K \
  AEST_TANGENT_ALLOW_K_MISS AEST_ERHS_TRACE_FILE AEST_ERHS_TRACE_K || true

JSON='results/stable_aest_desi_dr1_r9b2e_raw_solver_velocity_closure.json'
LOG='results/stable_aest_desi_dr1_r9b2e_raw_solver_velocity_closure.log'
if [[ -s "$JSON" ]] && grep -q 'STABLE_AEST_DESI_DR1_R9B2E_RUN_FAIL' "$JSON"; then
  cp -f "$JSON" results/stable_aest_desi_dr1_r9b2e_raw_solver_velocity_closure_technical_runfail_pre_repair01.json
fi
if [[ -s "$LOG" ]] && grep -q 'raw history lacks recognized k field' "$LOG"; then
  cp -f "$LOG" results/stable_aest_desi_dr1_r9b2e_raw_solver_velocity_closure_technical_runfail_pre_repair01.log
fi
rm -f "$JSON" "$LOG"

set +e
PYTHONPATH="$R9B_PYTARGET:${PYTHONPATH:-}" python -u -m fullj_weyl.stable_aest_desi_dr1_r9b2e_raw_solver_velocity_closure_repair01 \
  2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

echo "STABLE_AEST_DESI_DR1_R9B2E_REPAIR01_EXIT=$code"
echo "STABLE_AEST_DESI_DR1_R9B2E_REPAIR01_JSON=$JSON"
echo "STABLE_AEST_DESI_DR1_R9B2E_REPAIR01_LOG=$LOG"
exit "$code"
