#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

PREFIT_LOCK='2ea44eb92319fc6c2a3273dc91254e14dc797e35'
POSTDATA_LOCK='b569aebc41efc841755f5fcec63b91092c192ba3'
IMPLEMENTATION_LOCK='ca8b788a40bc5de1649f53ff4cfe7ace5aa1500b'
for lock in "$PREFIT_LOCK" "$POSTDATA_LOCK" "$IMPLEMENTATION_LOCK"; do
  git merge-base --is-ancestor "$lock" HEAD
done

echo "STABLE_AEST_DESI_DR1_R9B2G_LOCK_PASS prefit=$PREFIT_LOCK postdata=$POSTDATA_LOCK implementation=$IMPLEMENTATION_LOCK"

BASE_PY="$(command -v python3 || command -v python || true)"
[[ -n "$BASE_PY" ]] || { echo 'R9B2G: Python missing' >&2; exit 2; }
VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then "$BASE_PY" -m venv "$VENV"; fi
export PATH="$VENV/bin:$PATH"
python -m pip install -q numpy scipy cython h5py
python -m pip install -q 'git+https://github.com/cosmodesi/cosmoprimo.git@2e59c963c9b8e7cba1a4c8f161e978c6f4d80c2d'
python -m py_compile fullj_weyl/stable_aest_desi_dr1_r9b2g_bounded_source_extraction.py
echo STABLE_AEST_DESI_DR1_R9B2G_IMPORT_PASS

R9B_ROOT="$ROOT/.local/class_corrected_e8580832_densek64_stablechi_r9bdesi"
R9B_PYTARGET="$ROOT/.local/classy_corrected_e8580832_densek64_stablechi_r9bdesi"
[[ -d "$R9B_ROOT" ]] || { echo "R9B2G: missing $R9B_ROOT" >&2; exit 3; }
[[ -d "$R9B_PYTARGET" ]] || { echo "R9B2G: missing $R9B_PYTARGET" >&2; exit 3; }
grep -q 'FULLJ_AEST_STABLE_CHI_RESIDUAL_V1' "$R9B_ROOT/source/perturbations.c"
grep -q 'FULLJ_STABLE_AEST_R7A_LIVE_EPOCH_V1' "$R9B_ROOT/source/perturbations.c"
echo STABLE_AEST_DESI_DR1_R9B2G_SOURCE_PASS

export AEST_STABLE_R8A_CLASS_ROOT="$R9B_ROOT"
export AEST_R7A_EPOCH_MODE=full
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
unset AEST_R9B_DESI_DATA_DIR AEST_R9B_DESI_REPO || true
unset AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE \
  AEST_R2D_TRACE_FILE AEST_R2D_TRACE_KH AEST_R2D_TRACE_ALL_K \
  AEST_TANGENT_ALLOW_K_MISS AEST_ERHS_TRACE_FILE AEST_ERHS_TRACE_K || true

JSON='results/stable_aest_desi_dr1_r9b2g_bounded_source_extraction.json'
LOG='results/stable_aest_desi_dr1_r9b2g_bounded_source_extraction.log'
rm -f "$JSON" "$LOG"
set +e
PYTHONPATH="$R9B_PYTARGET:${PYTHONPATH:-}" python -u -m fullj_weyl.stable_aest_desi_dr1_r9b2g_bounded_source_extraction 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

echo "STABLE_AEST_DESI_DR1_R9B2G_EXIT=$code"
echo "STABLE_AEST_DESI_DR1_R9B2G_JSON=$JSON"
echo "STABLE_AEST_DESI_DR1_R9B2G_LOG=$LOG"
exit "$code"
