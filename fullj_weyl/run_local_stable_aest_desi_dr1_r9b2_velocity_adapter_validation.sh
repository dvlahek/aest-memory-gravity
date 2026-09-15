#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

PREFIT_LOCK='5864a8a56f420c578629763d478f60dfc49c2620'
IMPL_LOCK='782ec0066d15eef7548d41841d1f8f15b8ad8e31'
COSMOPRIMO_COMMIT='2e59c963c9b8e7cba1a4c8f161e978c6f4d80c2d'
R9B_POSTDATA_LOCK='22583094f3c5a417e7af6b1d7f284f739553048b'

git merge-base --is-ancestor "$PREFIT_LOCK" HEAD
git merge-base --is-ancestor "$IMPL_LOCK" HEAD
git merge-base --is-ancestor "$R9B_POSTDATA_LOCK" HEAD

BASE_PY="$(command -v python3 || command -v python)"
[[ -n "$BASE_PY" ]] || { echo 'R9B2_ADAPTER: python missing' >&2; exit 2; }
VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then "$BASE_PY" -m venv "$VENV"; fi
export PATH="$VENV/bin:$PATH"

python -m pip install -q numpy scipy cython camb
python -m pip install -q "git+https://github.com/cosmodesi/cosmoprimo.git@$COSMOPRIMO_COMMIT"
python -m py_compile fullj_weyl/stable_aest_desi_dr1_r9b2_velocity_adapter_validation.py

# Reuse only the disposable direct-physical CLASS build created by the completed R9b run.
# This validation does not read DESI data vectors or evaluate a DESI likelihood.
R9B_ROOT="$ROOT/.local/class_corrected_e8580832_densek64_stablechi_r9bdesi"
R9B_PYTARGET="$ROOT/.local/classy_corrected_e8580832_densek64_stablechi_r9bdesi"
[[ -d "$R9B_ROOT" ]] || { echo "R9B2_ADAPTER: missing $R9B_ROOT; rerun the completed R9b repair03 runner once" >&2; exit 3; }
[[ -d "$R9B_PYTARGET" ]] || { echo "R9B2_ADAPTER: missing $R9B_PYTARGET; rerun the completed R9b repair03 runner once" >&2; exit 3; }

grep -q 'FULLJ_AEST_STABLE_CHI_RESIDUAL_V1' "$R9B_ROOT/source/perturbations.c"
grep -q 'FULLJ_STABLE_AEST_R7A_LIVE_EPOCH_V1' "$R9B_ROOT/source/perturbations.c"
[[ "$(grep -Fc 'Bchi_aest *= pba->aest_eta*aest_r7a_epoch_weight(a);' "$R9B_ROOT/source/perturbations.c")" -eq 1 ]]
[[ "$(grep -Fc 'E_rhs_aest -= 0.5*Q_aest*Bchi_aest;' "$R9B_ROOT/source/perturbations.c")" -eq 1 ]]

echo STABLE_AEST_DESI_DR1_R9B2_VELOCITY_ADAPTER_SOURCE_PASS

JSON='results/stable_aest_desi_dr1_r9b2_velocity_adapter_validation.json'
LOG='results/stable_aest_desi_dr1_r9b2_velocity_adapter_validation.log'
rm -f "$JSON" "$LOG"

export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
unset AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE \
  AEST_R2D_TRACE_FILE AEST_R2D_TRACE_KH AEST_R2D_TRACE_ALL_K \
  AEST_TANGENT_ALLOW_K_MISS AEST_ERHS_TRACE_FILE AEST_ERHS_TRACE_K || true

set +e
PYTHONPATH="$R9B_PYTARGET:${PYTHONPATH:-}" python -u -m fullj_weyl.stable_aest_desi_dr1_r9b2_velocity_adapter_validation \
  --json-out "$JSON" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

echo "STABLE_AEST_DESI_DR1_R9B2_VELOCITY_ADAPTER_EXIT=$code"
echo "STABLE_AEST_DESI_DR1_R9B2_VELOCITY_ADAPTER_JSON=$JSON"
echo "STABLE_AEST_DESI_DR1_R9B2_VELOCITY_ADAPTER_LOG=$LOG"
exit "$code"
