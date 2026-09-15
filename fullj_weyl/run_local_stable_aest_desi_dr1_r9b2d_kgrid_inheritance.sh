#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

PREFIT_LOCK='bb15759f23246d3b7af734ff7f7cb2052f44d651'
POSTDATA_LOCK='7c4cc8a0a9f2a59a91cbb288a157f880d630f309'
IMPLEMENTATION_LOCK='a18020d3b307294b742614edc75a5ed28d7a91e8'
for lock in "$PREFIT_LOCK" "$POSTDATA_LOCK" "$IMPLEMENTATION_LOCK"; do
  git merge-base --is-ancestor "$lock" HEAD
done

echo "STABLE_AEST_DESI_DR1_R9B2D_LOCK_PASS prefit=$PREFIT_LOCK postdata=$POSTDATA_LOCK implementation=$IMPLEMENTATION_LOCK"

BASE_PY="$(command -v python3 || command -v python || true)"
[[ -n "$BASE_PY" ]] || { echo 'R9B2D: Python missing' >&2; exit 2; }
VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then "$BASE_PY" -m venv "$VENV"; fi
export PATH="$VENV/bin:$PATH"
python -m pip install -q numpy scipy cython h5py
python -m pip install -q 'git+https://github.com/cosmodesi/cosmoprimo.git@2e59c963c9b8e7cba1a4c8f161e978c6f4d80c2d'
python -m py_compile fullj_weyl/stable_aest_desi_dr1_r9b2d_kgrid_inheritance.py
echo STABLE_AEST_DESI_DR1_R9B2D_IMPORT_PASS

R9B_ROOT="$ROOT/.local/class_corrected_e8580832_densek64_stablechi_r9bdesi"
R9B_PYTARGET="$ROOT/.local/classy_corrected_e8580832_densek64_stablechi_r9bdesi"
[[ -d "$R9B_ROOT" ]] || { echo "R9B2D: missing $R9B_ROOT" >&2; exit 3; }
[[ -d "$R9B_PYTARGET" ]] || { echo "R9B2D: missing $R9B_PYTARGET" >&2; exit 3; }
grep -q 'FULLJ_AEST_STABLE_CHI_RESIDUAL_V1' "$R9B_ROOT/source/perturbations.c"
grep -q 'FULLJ_STABLE_AEST_R7A_LIVE_EPOCH_V1' "$R9B_ROOT/source/perturbations.c"
[[ "$(grep -Fc 'Bchi_aest *= pba->aest_eta*aest_r7a_epoch_weight(a);' "$R9B_ROOT/source/perturbations.c")" -eq 1 ]]
[[ "$(grep -Fc 'E_rhs_aest -= 0.5*Q_aest*Bchi_aest;' "$R9B_ROOT/source/perturbations.c")" -eq 1 ]]
echo STABLE_AEST_DESI_DR1_R9B2D_SOURCE_PASS

export AEST_STABLE_R8A_CLASS_ROOT="$R9B_ROOT"
export AEST_R7A_EPOCH_MODE=full
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
unset AEST_R9B_DESI_DATA_DIR AEST_R9B_DESI_REPO || true
unset AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE \
  AEST_R2D_TRACE_FILE AEST_R2D_TRACE_KH AEST_R2D_TRACE_ALL_K \
  AEST_TANGENT_ALLOW_K_MISS AEST_ERHS_TRACE_FILE AEST_ERHS_TRACE_K || true

JSON='results/stable_aest_desi_dr1_r9b2d_kgrid_inheritance.json'
LOG='results/stable_aest_desi_dr1_r9b2d_kgrid_inheritance.log'
rm -f "$JSON" "$LOG"
set +e
PYTHONPATH="$R9B_PYTARGET:${PYTHONPATH:-}" python -u -m fullj_weyl.stable_aest_desi_dr1_r9b2d_kgrid_inheritance 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

echo "STABLE_AEST_DESI_DR1_R9B2D_EXIT=$code"
echo "STABLE_AEST_DESI_DR1_R9B2D_JSON=$JSON"
echo "STABLE_AEST_DESI_DR1_R9B2D_LOG=$LOG"
exit "$code"
