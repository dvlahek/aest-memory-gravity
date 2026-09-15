#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

BASE_PY="$(command -v python3 || command -v python)"
[[ -n "$BASE_PY" ]] || { echo 'R8A2: python missing' >&2; exit 2; }
VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then "$BASE_PY" -m venv "$VENV"; fi
export PATH="$VENV/bin:$PATH"
python -m pip install numpy scipy cython >/dev/null
python -m py_compile \
  fullj_weyl/stable_aest_cosmic_memory_r8a2_precision_qualified_tau_scan.py \
  fullj_weyl/stable_aest_cosmic_memory_r8a_tau_amplitude_scan.py \
  fullj_weyl/stable_aest_observable_projection_r5b_derivative_zero.py \
  fullj_weyl/apply_stable_aest_r7a_live_epoch_patch.py \
  fullj_weyl/apply_aest_stable_chi_residual_patch.py
echo STABLE_AEST_COSMIC_MEMORY_R8A2_IMPORT_PASS

for f in \
  docs/stable_aest_cosmic_memory_r8a2_precision_qualified_tau_scan_predata.md \
  docs/stable_aest_cosmic_memory_r8a_tau_amplitude_scan_postdata.md \
  docs/stable_aest_cosmic_memory_r7a_live_epoch_derivative_postdata.md \
  results/stable_aest_cosmic_memory_r8a_tau_amplitude_scan.json \
  results/stable_aest_cosmic_memory_r7a_live_epoch_derivative.json \
  results/stable_aest_cosmic_memory_r7a_live_epoch_derivative.npz \
  results/nl1c6d2n_corrected_class_densek64_env.sh; do
  [[ -f "$f" ]] || { echo "R8A2: missing $f" >&2; exit 3; }
done

PREDATA_LOCK='e01db75882717b7f2e230d634ff8f930604d8011'
R7A_POSTDATA_LOCK='86c03e6ba2ee9fcbf33a9d319d12ae778a747881'
R8A_POSTDATA_LOCK='9b138cf04d3a8c323bbf3a82e3e747deea0393dc'
git merge-base --is-ancestor "$PREDATA_LOCK" HEAD
git merge-base --is-ancestor "$R7A_POSTDATA_LOCK" HEAD
git merge-base --is-ancestor "$R8A_POSTDATA_LOCK" HEAD
echo "STABLE_AEST_COSMIC_MEMORY_R8A2_SCIENCE_LOCK_PASS predata=$PREDATA_LOCK r7a=$R7A_POSTDATA_LOCK r8a=$R8A_POSTDATA_LOCK"

python - <<'PY'
from pathlib import Path
p=Path('fullj_weyl/stable_aest_cosmic_memory_r8a2_precision_qualified_tau_scan.py').read_text()
required=[
 'PREDATA_LOCK = "e01db75882717b7f2e230d634ff8f930604d8011"',
 'R7A_POSTDATA_LOCK = "86c03e6ba2ee9fcbf33a9d319d12ae778a747881"',
 'R8A_POSTDATA_LOCK = "9b138cf04d3a8c323bbf3a82e3e747deea0393dc"',
 'TAUS = (10.0, 5.0, 2.5, 1.25)',
 'EPS_PRIMARY = 0.025',
 'EPS_CONTROL = 0.05',
 'TOL_NOMINAL = 3e-8',
 'TOL_TIGHT = 1e-8',
 'CLS_PASS = "STABLE_AEST_COSMIC_MEMORY_R8A2_TAU_GENERALITY_CERTIFIED"',
 '"cross_tau_eta0_is_gating": False',
 'pm["E"] <= 1e-7',
 'pm["C"] >= 0.99999999',
]
for token in required:
    assert token in p,token
for forbidden in (
 'TAUS = (10.0, 5.0, 2.5, 1.25, 1.0)',
 'amplitude_ratio_to_tau10"] >','amplitude_ratio_to_tau10"] <',
 'force_full.dat','normalize_force(','partition_force(',
):
    assert forbidden not in p,forbidden
print('STABLE_AEST_COSMIC_MEMORY_R8A2_ANTI_STALE_CODE_PASS')
PY

python - <<'PY'
import json
from pathlib import Path
r7=json.loads(Path('results/stable_aest_cosmic_memory_r7a_live_epoch_derivative.json').read_text())
r8=json.loads(Path('results/stable_aest_cosmic_memory_r8a_tau_amplitude_scan.json').read_text())
assert r7['classification']=='STABLE_AEST_COSMIC_MEMORY_R7A_LIVE_LOOKBACK_DECOMPOSITION_CERTIFIED',r7['classification']
assert r7.get('diagnostic_complete') is True
assert all(r7['gates'].values())
assert r8['classification']=='STABLE_AEST_COSMIC_MEMORY_R8A_RUN_FAIL',r8['classification']
assert r8.get('diagnostic_complete') is True
assert r8['gates']['R8A_G1_provenance_and_parent_lock'] is True
assert r8['gates']['R8A_G2_direct_physical_source_topology'] is True
assert r8['gates']['R8A_G3_finite_tau_grid_runs_and_eta0_identity'] is False
assert all(x.get('finite') and x.get('domain_positive') for x in r8['runs'])
print('STABLE_AEST_COSMIC_MEMORY_R8A2_PARENT_PASS')
PY

source results/nl1c6d2n_corrected_class_densek64_env.sh
OLD_ROOT="$NL1C6D2N_CLASS_ROOT"
EXPECTED_CLASS_HEAD='e85808324f51fc694d12e3ed7439552a3c3f9540'
EXPECTED_MEMORY_SHA='4d5ab5dc7066d4880f06fcfc731d6534ed0ff992e3cc15fb473dddccb25a594f'
[[ "$(git -C "$OLD_ROOT" rev-parse HEAD)" == "$EXPECTED_CLASS_HEAD" ]]
[[ "$(sha256sum "$OLD_ROOT/source/aest_memory.c" | awk '{print $1}')" == "$EXPECTED_MEMORY_SHA" ]]
echo "STABLE_AEST_COSMIC_MEMORY_R8A2_OLD_PROVENANCE_PASS head=$EXPECTED_CLASS_HEAD"

R8A2_ROOT="$ROOT/.local/class_corrected_e8580832_densek64_stablechi_r8a2tau"
R8A2_PYTARGET="$ROOT/.local/classy_corrected_e8580832_densek64_stablechi_r8a2tau"
rm -rf "$R8A2_ROOT" "$R8A2_PYTARGET"
cp -a "$OLD_ROOT" "$R8A2_ROOT"
python fullj_weyl/apply_aest_stable_chi_residual_patch.py "$R8A2_ROOT"
[[ "$(git -C "$R8A2_ROOT" rev-parse HEAD)" == "$EXPECTED_CLASS_HEAD" ]]
[[ "$(sha256sum "$R8A2_ROOT/source/aest_memory.c" | awk '{print $1}')" == "$EXPECTED_MEMORY_SHA" ]]

python - "$R8A2_ROOT/source/perturbations.c" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]); s=p.read_text()
hook='        dy[pv->index_pt_E_aest] += aest_tangent_external_force(k,tau);'
n=s.count(hook)
if n != 1:
    raise SystemExit(f'R8A2_DIAGNOSTIC_HOOK_COUNT_FAIL count={n}')
p.write_text(s.replace(hook,'',1))
print('STABLE_AEST_COSMIC_MEMORY_R8A2_DORMANT_HOOK_NEUTRALIZED count_before=1 count_after=0')
PY

! grep -q 'aest_r2d_trace_force(k,pba->h,tau' "$R8A2_ROOT/source/perturbations.c"
python fullj_weyl/apply_stable_aest_r7a_live_epoch_patch.py "$R8A2_ROOT"

grep -q 'FULLJ_AEST_STABLE_CHI_RESIDUAL_V1' "$R8A2_ROOT/source/perturbations.c"
grep -q 'FULLJ_STABLE_AEST_R7A_LIVE_EPOCH_V1' "$R8A2_ROOT/source/perturbations.c"
[[ "$(grep -Fc 'Bchi_aest *= pba->aest_eta*aest_r7a_epoch_weight(a);' "$R8A2_ROOT/source/perturbations.c")" -eq 1 ]]
[[ "$(grep -Fc 'E_rhs_aest -= 0.5*Q_aest*Bchi_aest;' "$R8A2_ROOT/source/perturbations.c")" -eq 1 ]]
HOOK='dy[pv->index_pt_E_aest] += aest_tangent_external_force(k,tau);'
[[ "$(grep -Fc "$HOOK" "$R8A2_ROOT/source/perturbations.c")" -eq 0 ]]
[[ "$(grep -Fc 'aest_r2d_trace_force(k,pba->h,tau' "$R8A2_ROOT/source/perturbations.c")" -eq 0 ]]
! grep -q 'pba->aest_eta < 0.' "$R8A2_ROOT/source/input.c"
echo STABLE_AEST_COSMIC_MEMORY_R8A2_DIRECT_SOURCE_PASS

rm -rf "$R8A2_ROOT/build" "$R8A2_ROOT/python/build" "$R8A2_ROOT/python/classy.egg-info" 2>/dev/null || true
mkdir -p "$R8A2_PYTARGET"
python -m pip install --no-deps --no-build-isolation --target "$R8A2_PYTARGET" "$R8A2_ROOT"

export AEST_STABLE_R8A_CLASS_ROOT="$R8A2_ROOT"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
unset AEST_R7A_EPOCH_MODE \
  AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE \
  AEST_R2D_TRACE_FILE AEST_R2D_TRACE_KH AEST_R2D_TRACE_ALL_K \
  AEST_TANGENT_ALLOW_K_MISS AEST_ERHS_TRACE_FILE AEST_ERHS_TRACE_K || true

echo STABLE_AEST_COSMIC_MEMORY_R8A2_DIRECT_PHYSICAL_PASS

JSON='results/stable_aest_cosmic_memory_r8a2_precision_qualified_tau_scan.json'
NPZ='results/stable_aest_cosmic_memory_r8a2_precision_qualified_tau_scan.npz'
LOG='results/stable_aest_cosmic_memory_r8a2_precision_qualified_tau_scan.log'
ZIP='results/stable_aest_cosmic_memory_r8a2_precision_qualified_tau_scan_bundle.zip'
ENVOUT='results/stable_aest_cosmic_memory_r8a2_environment.txt'
WORK='results/stable_aest_cosmic_memory_r8a2_work'
rm -f "$JSON" "$NPZ" "$LOG" "$ZIP" "$ENVOUT"
rm -rf "$WORK"

{
  echo "repo_head=$(git rev-parse HEAD)"
  echo "predata_lock=$PREDATA_LOCK"
  echo "r7a_postdata_lock=$R7A_POSTDATA_LOCK"
  echo "r8a_postdata_lock=$R8A_POSTDATA_LOCK"
  echo "class_parent_head=$EXPECTED_CLASS_HEAD"
  echo "r8a2_source=$R8A2_ROOT"
  echo "python=$(python --version 2>&1)"
  echo '--- pip freeze ---'
  python -m pip freeze
} > "$ENVOUT"

set +e
PYTHONPATH="$R8A2_PYTARGET" python -u -m fullj_weyl.stable_aest_cosmic_memory_r8a2_precision_qualified_tau_scan \
  --json-out "$JSON" --npz-out "$NPZ" --workdir "$WORK" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

python - "$ZIP" "$LOG" "$JSON" "$NPZ" "$ENVOUT" "$WORK" <<'PY'
from pathlib import Path
import sys,zipfile
zp=Path(sys.argv[1]); work=Path(sys.argv[6])
paths=[Path(x) for x in sys.argv[2:6]]+[
 Path('docs/stable_aest_cosmic_memory_r8a2_precision_qualified_tau_scan_predata.md'),
 Path('docs/stable_aest_cosmic_memory_r8a_tau_amplitude_scan_postdata.md'),
 Path('docs/stable_aest_cosmic_memory_r7a_live_epoch_derivative_postdata.md'),
 Path('fullj_weyl/stable_aest_cosmic_memory_r8a2_precision_qualified_tau_scan.py'),
 Path('fullj_weyl/run_local_stable_aest_cosmic_memory_r8a2_precision_qualified_tau_scan.sh'),
 Path('fullj_weyl/apply_stable_aest_r7a_live_epoch_patch.py'),
 Path('fullj_weyl/apply_aest_stable_chi_residual_patch.py'),
 Path('results/stable_aest_cosmic_memory_r8a_tau_amplitude_scan.json'),
 Path('results/stable_aest_cosmic_memory_r7a_live_epoch_derivative.json'),
 Path('results/stable_aest_cosmic_memory_r7a_live_epoch_derivative.npz')]
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED) as zf:
    seen=set()
    for p in paths:
        if p.exists() and p not in seen:
            zf.write(p,arcname=str(p)); seen.add(p)
    if work.exists():
        for p in sorted(work.rglob('*')):
            if p.is_file(): zf.write(p,arcname=str(p))
print('STABLE_AEST_COSMIC_MEMORY_R8A2_BUNDLE='+str(zp))
PY

echo "STABLE_AEST_COSMIC_MEMORY_R8A2_EXIT=$code"
echo "STABLE_AEST_COSMIC_MEMORY_R8A2_LOG=$LOG"
echo "STABLE_AEST_COSMIC_MEMORY_R8A2_JSON=$JSON"
echo "STABLE_AEST_COSMIC_MEMORY_R8A2_NPZ=$NPZ"
echo "STABLE_AEST_COSMIC_MEMORY_R8A2_ZIP=$ZIP"
exit "$code"
