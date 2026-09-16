#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

R03_PREFIT_LOCK='de7511bed7fc984bf0ba40d1afc70a63de88ebb2'
R03_IMPL_LOCK='6ab94ed0365a12deae546f71088aee267300f39b'
R03_IMPL_BLOB='77e1dfb337e9e190fdac85da809432c972316513'
R02_POSTDATA_LOCK='472ab501cfe564510b38e1c2831c4024ae012ecf'
R8A2_POSTDATA_LOCK='590dbc69e2823f583b157af2297e357991103c47'
R10A_POSTDATA_LOCK='b7da648f1810ea0c047b6e511e3f87211e830329'
R11A_R02_POSTDATA_LOCK='84c4ba550ce3b262c78c69054056ab2778014677'
R02_JSON_SHA='8c7268c12afacf3faed98264d4154a613544f1d0529854773ef6b6563c8e22f2'
R8A2_JSON_SHA='2d6289c2fbd37bebcb904dade89f64c15a009e5c7454754b39d4dcc72924ca66'
R8A2_NPZ_SHA='c81b2093a88719423e87ff5c180d790a56da6f396c0070858624879c90f26ee1'
R11A_R02_JSON_SHA='f5166409be08edc93e739b2b901bd183a2a588325eb6c71eb0ad0e8a82d2b4a1'

R03_PREFIT='docs/stable_aest_r12a_eg_weyl_growth_consistency_repair03_direct_transfer_predata.md'
R03_IMPL='fullj_weyl/stable_aest_r12a_eg_weyl_growth_consistency_repair03.py'
R02_JSON='results/stable_aest_r12a_eg_weyl_growth_consistency_repair02.json'
R8A2_JSON='results/stable_aest_cosmic_memory_r8a2_precision_qualified_tau_scan.json'
R8A2_NPZ='results/stable_aest_cosmic_memory_r8a2_precision_qualified_tau_scan.npz'
R11A_R02_JSON='results/stable_aest_ksz_r11a_dense_resolution_repair02.json'

for f in "$R03_PREFIT" "$R03_IMPL" "$R02_JSON" "$R8A2_JSON" "$R8A2_NPZ" "$R11A_R02_JSON"; do
  [[ -f "$f" ]] || { echo "STABLE_AEST_R12A_R03_MISSING file=$f" >&2; exit 3; }
done
for lock in "$R03_PREFIT_LOCK" "$R03_IMPL_LOCK" "$R02_POSTDATA_LOCK" "$R8A2_POSTDATA_LOCK" "$R10A_POSTDATA_LOCK" "$R11A_R02_POSTDATA_LOCK"; do
  git merge-base --is-ancestor "$lock" HEAD || { echo "STABLE_AEST_R12A_R03_LOCK_FAIL lock=$lock" >&2; exit 3; }
done
[[ "$(git hash-object "$R03_IMPL")" == "$R03_IMPL_BLOB" ]] || { echo STABLE_AEST_R12A_R03_IMPL_BLOB_FAIL >&2; exit 3; }
[[ "$(sha256sum "$R02_JSON" | awk '{print $1}')" == "$R02_JSON_SHA" ]] || { echo STABLE_AEST_R12A_R03_R02_JSON_HASH_FAIL >&2; exit 3; }
[[ "$(sha256sum "$R8A2_JSON" | awk '{print $1}')" == "$R8A2_JSON_SHA" ]] || { echo STABLE_AEST_R12A_R03_R8A2_JSON_HASH_FAIL >&2; exit 3; }
[[ "$(sha256sum "$R8A2_NPZ" | awk '{print $1}')" == "$R8A2_NPZ_SHA" ]] || { echo STABLE_AEST_R12A_R03_R8A2_NPZ_HASH_FAIL >&2; exit 3; }
[[ "$(sha256sum "$R11A_R02_JSON" | awk '{print $1}')" == "$R11A_R02_JSON_SHA" ]] || { echo STABLE_AEST_R12A_R03_R11A_JSON_HASH_FAIL >&2; exit 3; }
echo "STABLE_AEST_R12A_R03_LOCK_PASS prefit=$R03_PREFIT_LOCK impl=$R03_IMPL_LOCK r02_postdata=$R02_POSTDATA_LOCK r11a=$R11A_R02_POSTDATA_LOCK"

BASE_PY="$(command -v python3 || command -v python || true)"
[[ -n "$BASE_PY" ]] || { echo 'STABLE_AEST_R12A_R03: python missing' >&2; exit 2; }
VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then "$BASE_PY" -m venv "$VENV"; fi
export PATH="$VENV/bin:$PATH"
python -m pip install numpy scipy cython >/dev/null
python -m py_compile "$R03_IMPL" \
  fullj_weyl/stable_aest_r12a_eg_weyl_growth_consistency.py \
  fullj_weyl/stable_aest_observable_projection_r5b_derivative_zero.py \
  fullj_weyl/stable_aest_desi_dr1_r9b_shapefit_projection.py
echo STABLE_AEST_R12A_R03_IMPORT_PASS

python - <<'PY'
from pathlib import Path
s=Path('fullj_weyl/stable_aest_r12a_eg_weyl_growth_consistency_repair03.py').read_text()
required=[
 'PREFIT_R03 = "de7511bed7fc984bf0ba40d1afc70a63de88ebb2"',
 'POSTDATA_R02 = "472ab501cfe564510b38e1c2831c4024ae012ecf"',
 'TAUS = (10.0, 5.0, 2.5, 1.25)',
 'ETAS = (0.0, 0.025, -0.025, 0.05, -0.05)',
 'K_H = np.asarray([0.03, 0.05, 0.08, 0.10, 0.15, 0.20], float)',
 'p.pop("k_output_values",None)',
 'tk=c.get_transfer(float(z), output_format="class")',
 'T=(cp[field]-cm[field])/(2.0*eps*c0[field])',
 'primary_k_interpolation":"PCHIP in ln k after response formation"',
 'PASS = "STABLE_AEST_R12A_REPAIR03_DIRECT_TRANSFER_CERTIFIED"',
]
for token in required: assert token in s, token
for forbidden in ('get_perturbations(', 'CubicSpline(', '_eval_field(', 'smooth_pk_interpolator', 'np.clip('):
    assert forbidden not in s, forbidden
print('STABLE_AEST_R12A_R03_ANTI_STALE_CODE_PASS')
PY

python - <<'PY'
import json
from pathlib import Path
r02=json.loads(Path('results/stable_aest_r12a_eg_weyl_growth_consistency_repair02.json').read_text())
r8=json.loads(Path('results/stable_aest_cosmic_memory_r8a2_precision_qualified_tau_scan.json').read_text())
r11=json.loads(Path('results/stable_aest_ksz_r11a_dense_resolution_repair02.json').read_text())
assert r02['classification']=='STABLE_AEST_R12A_INTERPOLATION_CONTROL_FAIL'
assert r02.get('diagnostic_complete') is True and r02.get('science_evaluated') is False
assert r02['gates']['R12A_G5_interpolation_control'] is False
assert r02['gates']['R12A_G6_epsilon_consistency'] is False
assert r8['classification']=='STABLE_AEST_COSMIC_MEMORY_R8A2_TAU_GENERALITY_CERTIFIED'
assert r8.get('diagnostic_complete') is True and all(r8['gates'].values())
assert r11['classification']=='STABLE_AEST_KSZ_R11A_REPAIR02_DENSE_RESOLUTION_CERTIFIED'
assert r11.get('diagnostic_complete') is True and all(r11['gates'].values())
print('STABLE_AEST_R12A_R03_PARENT_PASS')
PY

R8A2_ROOT="$ROOT/.local/class_corrected_e8580832_densek64_stablechi_r8a2tau"
R8A2_PYTARGET="$ROOT/.local/classy_corrected_e8580832_densek64_stablechi_r8a2tau"
[[ -d "$R8A2_ROOT" && -d "$R8A2_PYTARGET" ]] || {
  echo "STABLE_AEST_R12A_R03_R8A2_CLASS_BUILD_MISSING root=$R8A2_ROOT pytarget=$R8A2_PYTARGET" >&2
  exit 3
}
EXPECTED_CLASS_HEAD='e85808324f51fc694d12e3ed7439552a3c3f9540'
[[ "$(git -C "$R8A2_ROOT" rev-parse HEAD)" == "$EXPECTED_CLASS_HEAD" ]] || { echo STABLE_AEST_R12A_R03_CLASS_HEAD_FAIL >&2; exit 3; }
grep -q 'FULLJ_AEST_STABLE_CHI_RESIDUAL_V1' "$R8A2_ROOT/source/perturbations.c"
grep -q 'FULLJ_STABLE_AEST_R7A_LIVE_EPOCH_V1' "$R8A2_ROOT/source/perturbations.c"
[[ "$(grep -Fc 'Bchi_aest *= pba->aest_eta*aest_r7a_epoch_weight(a);' "$R8A2_ROOT/source/perturbations.c")" -eq 1 ]]
[[ "$(grep -Fc 'E_rhs_aest -= 0.5*Q_aest*Bchi_aest;' "$R8A2_ROOT/source/perturbations.c")" -eq 1 ]]
[[ "$(grep -Fc 'dy[pv->index_pt_E_aest] += aest_tangent_external_force(k,tau);' "$R8A2_ROOT/source/perturbations.c")" -eq 0 ]]
[[ "$(grep -Fc 'aest_r2d_trace_force(k,pba->h,tau' "$R8A2_ROOT/source/perturbations.c")" -eq 0 ]]
! grep -q 'pba->aest_eta < 0.' "$R8A2_ROOT/source/input.c"
echo STABLE_AEST_R12A_R03_SOURCE_PASS

export AEST_STABLE_R8A_CLASS_ROOT="$R8A2_ROOT"
export AEST_R7A_EPOCH_MODE=full
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
unset AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE \
  AEST_R2D_TRACE_FILE AEST_R2D_TRACE_KH AEST_R2D_TRACE_ALL_K \
  AEST_TANGENT_ALLOW_K_MISS AEST_ERHS_TRACE_FILE AEST_ERHS_TRACE_K || true
PYTHONPATH="$R8A2_PYTARGET${PYTHONPATH:+:$PYTHONPATH}" python - <<'PY'
from classy import Class
c=Class()
assert hasattr(c,'get_transfer'), 'frozen classy lacks get_transfer'
print('STABLE_AEST_R12A_R03_CLASSY_DIRECT_TRANSFER_API_PASS')
PY

JSON='results/stable_aest_r12a_eg_weyl_growth_consistency_repair03.json'
NPZ='results/stable_aest_r12a_eg_weyl_growth_consistency_repair03.npz'
LOG='results/stable_aest_r12a_eg_weyl_growth_consistency_repair03.log'
ENVOUT='results/stable_aest_r12a_eg_weyl_growth_consistency_repair03_environment.txt'
WORK='results/stable_aest_r12a_eg_work_repair03'
rm -f "$JSON" "$NPZ" "$LOG" "$ENVOUT"
mkdir -p "$WORK"

{
  echo "repo_head=$(git rev-parse HEAD)"
  echo "repair03_prefit=$R03_PREFIT_LOCK"
  echo "repair03_impl=$R03_IMPL_LOCK"
  echo "repair03_impl_blob=$R03_IMPL_BLOB"
  echo "repair02_postdata=$R02_POSTDATA_LOCK"
  echo "repair02_json_sha256=$R02_JSON_SHA"
  echo "r8a2_postdata=$R8A2_POSTDATA_LOCK"
  echo "r10a_postdata=$R10A_POSTDATA_LOCK"
  echo "r11a_r02_postdata=$R11A_R02_POSTDATA_LOCK"
  echo "class_parent_head=$EXPECTED_CLASS_HEAD"
  echo "class_root=$R8A2_ROOT"
  echo "python=$(python --version 2>&1)"
  echo "time_interpolation=none"
  echo "response_formation=native_transfer_k_before_target_k_interpolation"
  echo "primary_k_operator=PCHIP_logk"
  echo "control_k_operator=linear_logk"
} > "$ENVOUT"

set +e
PYTHONPATH="$R8A2_PYTARGET${PYTHONPATH:+:$PYTHONPATH}" python -u -m fullj_weyl.stable_aest_r12a_eg_weyl_growth_consistency_repair03 \
  --workdir "$WORK" --json-out "$JSON" --npz-out "$NPZ" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

echo "STABLE_AEST_R12A_R03_EXIT=$code"
[[ -f "$JSON" ]] && sha256sum "$JSON"
[[ -f "$NPZ" ]] && sha256sum "$NPZ"
sha256sum "$LOG" "$ENVOUT"
echo "STABLE_AEST_R12A_R03_JSON=$JSON"
echo "STABLE_AEST_R12A_R03_NPZ=$NPZ"
echo "STABLE_AEST_R12A_R03_LOG=$LOG"
exit "$code"
