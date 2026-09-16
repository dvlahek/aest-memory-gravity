#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

PREFIT_LOCK='bb69d8ac1d83228ba879316c61141823c3e5c665'
IMPLEMENTATION_LOCK='1af8327e73fbe1f70d1a8c8d14564b80c4bfacc1'
IMPLEMENTATION_BLOB='eb74909410c773bce93902765ddf4f57ec987415'
REPAIR01_PREFIT_LOCK='1ca886585e03dc11db0a3e109884a869eb8468b9'
REPAIR01_IMPLEMENTATION_LOCK='05d638089fcea26cb7a70e06273fbc282b794af7'
REPAIR01_BLOB='4a77b0021296cac47b03334efbb142477a6e8d13'
R8A2_POSTDATA_LOCK='590dbc69e2823f583b157af2297e357991103c47'
R10A_POSTDATA_LOCK='b7da648f1810ea0c047b6e511e3f87211e830329'
R11A_R02_POSTDATA_LOCK='84c4ba550ce3b262c78c69054056ab2778014677'
R8A2_JSON_SHA='2d6289c2fbd37bebcb904dade89f64c15a009e5c7454754b39d4dcc72924ca66'
R8A2_NPZ_SHA='c81b2093a88719423e87ff5c180d790a56da6f396c0070858624879c90f26ee1'
R11A_R02_JSON_SHA='f5166409be08edc93e739b2b901bd183a2a588325eb6c71eb0ad0e8a82d2b4a1'

PREFIT='docs/stable_aest_r12a_eg_weyl_growth_consistency_prefit.md'
REPAIR01_PREFIT='docs/stable_aest_r12a_eg_weyl_growth_consistency_repair01_predata.md'
IMPL='fullj_weyl/stable_aest_r12a_eg_weyl_growth_consistency.py'
REPAIR01_IMPL='fullj_weyl/stable_aest_r12a_eg_weyl_growth_consistency_repair01.py'
R8A2_JSON='results/stable_aest_cosmic_memory_r8a2_precision_qualified_tau_scan.json'
R8A2_NPZ='results/stable_aest_cosmic_memory_r8a2_precision_qualified_tau_scan.npz'
R11A_R02_JSON='results/stable_aest_ksz_r11a_dense_resolution_repair02.json'

for f in "$PREFIT" "$REPAIR01_PREFIT" "$IMPL" "$REPAIR01_IMPL" "$R8A2_JSON" "$R8A2_NPZ" "$R11A_R02_JSON"; do
  [[ -f "$f" ]] || { echo "STABLE_AEST_R12A_R01_MISSING file=$f" >&2; exit 3; }
done
for lock in "$PREFIT_LOCK" "$IMPLEMENTATION_LOCK" "$REPAIR01_PREFIT_LOCK" "$REPAIR01_IMPLEMENTATION_LOCK" "$R8A2_POSTDATA_LOCK" "$R10A_POSTDATA_LOCK" "$R11A_R02_POSTDATA_LOCK"; do
  git merge-base --is-ancestor "$lock" HEAD || { echo "STABLE_AEST_R12A_R01_LOCK_FAIL lock=$lock" >&2; exit 3; }
done
[[ "$(git hash-object "$IMPL")" == "$IMPLEMENTATION_BLOB" ]] || { echo STABLE_AEST_R12A_R01_BASE_IMPLEMENTATION_BLOB_FAIL >&2; exit 3; }
[[ "$(git hash-object "$REPAIR01_IMPL")" == "$REPAIR01_BLOB" ]] || { echo STABLE_AEST_R12A_R01_REPAIR_IMPLEMENTATION_BLOB_FAIL >&2; exit 3; }
[[ "$(sha256sum "$R8A2_JSON" | awk '{print $1}')" == "$R8A2_JSON_SHA" ]] || { echo STABLE_AEST_R12A_R01_R8A2_JSON_HASH_FAIL >&2; exit 3; }
[[ "$(sha256sum "$R8A2_NPZ" | awk '{print $1}')" == "$R8A2_NPZ_SHA" ]] || { echo STABLE_AEST_R12A_R01_R8A2_NPZ_HASH_FAIL >&2; exit 3; }
[[ "$(sha256sum "$R11A_R02_JSON" | awk '{print $1}')" == "$R11A_R02_JSON_SHA" ]] || { echo STABLE_AEST_R12A_R01_R11A_JSON_HASH_FAIL >&2; exit 3; }
echo "STABLE_AEST_R12A_R01_LOCK_PASS prefit=$PREFIT_LOCK implementation=$IMPLEMENTATION_LOCK repair_prefit=$REPAIR01_PREFIT_LOCK repair_impl=$REPAIR01_IMPLEMENTATION_LOCK r8a2=$R8A2_POSTDATA_LOCK r10a=$R10A_POSTDATA_LOCK r11a_r02=$R11A_R02_POSTDATA_LOCK"

BASE_PY="$(command -v python3 || command -v python || true)"
[[ -n "$BASE_PY" ]] || { echo 'STABLE_AEST_R12A_R01: python missing' >&2; exit 2; }
VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then "$BASE_PY" -m venv "$VENV"; fi
export PATH="$VENV/bin:$PATH"
python -m pip install numpy scipy cython >/dev/null
python -m py_compile \
  "$IMPL" "$REPAIR01_IMPL" \
  fullj_weyl/stable_aest_observable_projection_r5b_derivative_zero.py \
  fullj_weyl/stable_aest_cosmic_memory_r8a_tau_amplitude_scan.py \
  fullj_weyl/stable_aest_desi_dr1_r9b_shapefit_projection.py \
  nl1c6d2a/baryon_matter_sector_audit.py
echo STABLE_AEST_R12A_R01_IMPORT_PASS

python - <<'PY'
from pathlib import Path
base=Path('fullj_weyl/stable_aest_r12a_eg_weyl_growth_consistency.py').read_text()
rep=Path('fullj_weyl/stable_aest_r12a_eg_weyl_growth_consistency_repair01.py').read_text()
assert 'R11A_R02_POSTDATA_LOCK = "d9e2e0e6da65126a81d02f32e65f83410bc8cc7c"' in base
assert 'CORRECT_R11A_R02_POSTDATA_LOCK = "84c4ba550ce3b262c78c69054056ab2778014677"' in rep
assert 'base.R11A_R02_POSTDATA_LOCK = CORRECT_R11A_R02_POSTDATA_LOCK' in rep
for token in (
 'TAUS = (10.0, 5.0, 2.5, 1.25)',
 'ETAS = (0.0, 0.025, -0.025, 0.05, -0.05)',
 'K_H = np.asarray([0.03, 0.05, 0.08, 0.10, 0.15, 0.20], float)',
 'fdelta=-theta/Hconf',
 'EG=-(kmpc*kmpc)*W/(3.0*H0*H0*(1.0+Z)*fdelta)',
 'rhs=tangents[(tau,EPS_PRIMARY,method,"W")]-tangents[(tau,EPS_PRIMARY,method,"fdelta")]',
 'CLS_PASS = "STABLE_AEST_R12A_EG_WEYL_GROWTH_CONSISTENCY_CERTIFIED"',
):
    assert token in base, token
for forbidden in ('np.clip(', 'smooth_pk_interpolator', 'act_dr6_lenslike', 'load_desi(', 'get_data('):
    assert forbidden not in base, forbidden
print('STABLE_AEST_R12A_R01_ANTI_STALE_CODE_PASS')
PY

python - <<'PY'
import json
from pathlib import Path
r8=json.loads(Path('results/stable_aest_cosmic_memory_r8a2_precision_qualified_tau_scan.json').read_text())
r11=json.loads(Path('results/stable_aest_ksz_r11a_dense_resolution_repair02.json').read_text())
assert r8['classification']=='STABLE_AEST_COSMIC_MEMORY_R8A2_TAU_GENERALITY_CERTIFIED'
assert r8.get('diagnostic_complete') is True and all(r8['gates'].values())
assert r11['classification']=='STABLE_AEST_KSZ_R11A_REPAIR02_DENSE_RESOLUTION_CERTIFIED'
assert r11.get('diagnostic_complete') is True and all(r11['gates'].values())
print('STABLE_AEST_R12A_R01_PARENT_PASS')
PY

# Reuse the exact frozen R8a2 patched CLASS build.
R8A2_ROOT="$ROOT/.local/class_corrected_e8580832_densek64_stablechi_r8a2tau"
R8A2_PYTARGET="$ROOT/.local/classy_corrected_e8580832_densek64_stablechi_r8a2tau"
[[ -d "$R8A2_ROOT" && -d "$R8A2_PYTARGET" ]] || {
  echo "STABLE_AEST_R12A_R01_R8A2_CLASS_BUILD_MISSING root=$R8A2_ROOT pytarget=$R8A2_PYTARGET" >&2
  echo "Rerun the frozen R8a2 environment setup; do not substitute another CLASS build." >&2
  exit 3
}
EXPECTED_CLASS_HEAD='e85808324f51fc694d12e3ed7439552a3c3f9540'
[[ "$(git -C "$R8A2_ROOT" rev-parse HEAD)" == "$EXPECTED_CLASS_HEAD" ]] || { echo STABLE_AEST_R12A_R01_CLASS_HEAD_FAIL >&2; exit 3; }
grep -q 'FULLJ_AEST_STABLE_CHI_RESIDUAL_V1' "$R8A2_ROOT/source/perturbations.c"
grep -q 'FULLJ_STABLE_AEST_R7A_LIVE_EPOCH_V1' "$R8A2_ROOT/source/perturbations.c"
[[ "$(grep -Fc 'Bchi_aest *= pba->aest_eta*aest_r7a_epoch_weight(a);' "$R8A2_ROOT/source/perturbations.c")" -eq 1 ]]
[[ "$(grep -Fc 'E_rhs_aest -= 0.5*Q_aest*Bchi_aest;' "$R8A2_ROOT/source/perturbations.c")" -eq 1 ]]
[[ "$(grep -Fc 'dy[pv->index_pt_E_aest] += aest_tangent_external_force(k,tau);' "$R8A2_ROOT/source/perturbations.c")" -eq 0 ]]
[[ "$(grep -Fc 'aest_r2d_trace_force(k,pba->h,tau' "$R8A2_ROOT/source/perturbations.c")" -eq 0 ]]
! grep -q 'pba->aest_eta < 0.' "$R8A2_ROOT/source/input.c"
echo STABLE_AEST_R12A_R01_SOURCE_PASS

export AEST_STABLE_R8A_CLASS_ROOT="$R8A2_ROOT"
export AEST_R7A_EPOCH_MODE=full
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
unset AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE \
  AEST_R2D_TRACE_FILE AEST_R2D_TRACE_KH AEST_R2D_TRACE_ALL_K \
  AEST_TANGENT_ALLOW_K_MISS AEST_ERHS_TRACE_FILE AEST_ERHS_TRACE_K || true

PYTHONPATH="$R8A2_PYTARGET${PYTHONPATH:+:$PYTHONPATH}" python - <<'PY'
from classy import Class
from fullj_weyl import stable_aest_r12a_eg_weyl_growth_consistency_repair01 as r
assert r.base.R11A_R02_POSTDATA_LOCK == '84c4ba550ce3b262c78c69054056ab2778014677'
print('STABLE_AEST_R12A_R01_CLASSY_IMPORT_PASS')
PY

JSON='results/stable_aest_r12a_eg_weyl_growth_consistency.json'
NPZ='results/stable_aest_r12a_eg_weyl_growth_consistency.npz'
LOG='results/stable_aest_r12a_eg_weyl_growth_consistency.log'
ENVOUT='results/stable_aest_r12a_eg_weyl_growth_consistency_environment.txt'
WORK='results/stable_aest_r12a_eg_work'
rm -f "$JSON" "$NPZ" "$LOG" "$ENVOUT"
mkdir -p "$WORK"

{
  echo "repo_head=$(git rev-parse HEAD)"
  echo "prefit_lock=$PREFIT_LOCK"
  echo "implementation_lock=$IMPLEMENTATION_LOCK"
  echo "implementation_blob=$IMPLEMENTATION_BLOB"
  echo "repair01_prefit_lock=$REPAIR01_PREFIT_LOCK"
  echo "repair01_implementation_lock=$REPAIR01_IMPLEMENTATION_LOCK"
  echo "repair01_blob=$REPAIR01_BLOB"
  echo "r8a2_postdata_lock=$R8A2_POSTDATA_LOCK"
  echo "r10a_postdata_lock=$R10A_POSTDATA_LOCK"
  echo "r11a_r02_postdata_lock=$R11A_R02_POSTDATA_LOCK"
  echo "class_parent_head=$EXPECTED_CLASS_HEAD"
  echo "class_root=$R8A2_ROOT"
  echo "classy_target=$R8A2_PYTARGET"
  echo "python=$(python --version 2>&1)"
} > "$ENVOUT"

set +e
PYTHONPATH="$R8A2_PYTARGET${PYTHONPATH:+:$PYTHONPATH}" python -u -m fullj_weyl.stable_aest_r12a_eg_weyl_growth_consistency_repair01 \
  --workdir "$WORK" --json-out "$JSON" --npz-out "$NPZ" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

echo "STABLE_AEST_R12A_R01_EXIT=$code"
[[ -f "$JSON" ]] && sha256sum "$JSON"
[[ -f "$NPZ" ]] && sha256sum "$NPZ"
sha256sum "$LOG" "$ENVOUT"
echo "STABLE_AEST_R12A_R01_JSON=$JSON"
echo "STABLE_AEST_R12A_R01_NPZ=$NPZ"
echo "STABLE_AEST_R12A_R01_LOG=$LOG"
exit "$code"
