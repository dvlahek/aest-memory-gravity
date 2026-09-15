#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

BASE_PY="$(command -v python3 || command -v python)"
[[ -n "$BASE_PY" ]] || { echo 'R8B: python missing' >&2; exit 2; }
VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then "$BASE_PY" -m venv "$VENV"; fi
export PATH="$VENV/bin:$PATH"
python -m pip install numpy scipy cython >/dev/null
python -m py_compile \
  fullj_weyl/stable_aest_cosmic_memory_r8b_two_tau_lookback.py \
  fullj_weyl/stable_aest_cosmic_memory_r8a2_precision_qualified_tau_scan.py \
  fullj_weyl/stable_aest_cosmic_memory_r8a_tau_amplitude_scan.py \
  fullj_weyl/stable_aest_observable_projection_r5b_derivative_zero.py \
  fullj_weyl/apply_stable_aest_r7a_live_epoch_patch.py \
  fullj_weyl/apply_aest_stable_chi_residual_patch.py
echo STABLE_AEST_COSMIC_MEMORY_R8B_IMPORT_PASS

for f in \
  docs/stable_aest_cosmic_memory_r8b_two_tau_lookback_predata.md \
  docs/stable_aest_cosmic_memory_r8a2_precision_qualified_tau_scan_postdata.md \
  docs/stable_aest_cosmic_memory_r7a_live_epoch_derivative_postdata.md \
  results/stable_aest_cosmic_memory_r8a2_precision_qualified_tau_scan.json \
  results/stable_aest_cosmic_memory_r8a2_precision_qualified_tau_scan.npz \
  results/stable_aest_cosmic_memory_r7a_live_epoch_derivative.json \
  results/stable_aest_cosmic_memory_r7a_live_epoch_derivative.npz \
  results/nl1c6d2n_corrected_class_densek64_env.sh; do
  [[ -f "$f" ]] || { echo "R8B: missing $f" >&2; exit 3; }
done

PREDATA_LOCK='26ad0f310e0cc203c3350330a17e6822771515a0'
R7A_POSTDATA_LOCK='86c03e6ba2ee9fcbf33a9d319d12ae778a747881'
R8A2_POSTDATA_LOCK='590dbc69e2823f583b157af2297e357991103c47'
git merge-base --is-ancestor "$PREDATA_LOCK" HEAD
git merge-base --is-ancestor "$R7A_POSTDATA_LOCK" HEAD
git merge-base --is-ancestor "$R8A2_POSTDATA_LOCK" HEAD
echo "STABLE_AEST_COSMIC_MEMORY_R8B_SCIENCE_LOCK_PASS predata=$PREDATA_LOCK r7a=$R7A_POSTDATA_LOCK r8a2=$R8A2_POSTDATA_LOCK"

python - <<'PY'
from pathlib import Path
p=Path('fullj_weyl/stable_aest_cosmic_memory_r8b_two_tau_lookback.py').read_text()
required=[
 'PREDATA_LOCK = "26ad0f310e0cc203c3350330a17e6822771515a0"',
 'R7A_POSTDATA_LOCK = "86c03e6ba2ee9fcbf33a9d319d12ae778a747881"',
 'R8A2_POSTDATA_LOCK = "590dbc69e2823f583b157af2297e357991103c47"',
 'TAU = 1.25',
 'EPS_PRIMARY = 0.025',
 'EPS_CONTROL = 0.05',
 'EPOCHS = ("ancient", "intermediate", "recent_structure", "late")',
 'CLS_PASS = "STABLE_AEST_COSMIC_MEMORY_R8B_TWO_TAU_LOOKBACK_CERTIFIED"',
 '"delta_signed_projection_fraction"',
 '"cross_tau_epoch_cosine"',
 '"epoch_amplitude_ratio_tau1p25_to_tau10"',
]
for token in required:
    assert token in p, token
for forbidden in (
 'TAU = 1.0', 'TAU = 2.5',
 'force_full.dat','normalize_force(','partition_force(',
 'delta_signed_projection_fraction"] >','delta_signed_projection_fraction"] <',
):
    assert forbidden not in p, forbidden
print('STABLE_AEST_COSMIC_MEMORY_R8B_ANTI_STALE_CODE_PASS')
PY

python - <<'PY'
import hashlib,json
from pathlib import Path
parents=[
 ('results/stable_aest_cosmic_memory_r7a_live_epoch_derivative.json','94977acfe47f3f58337ce45dd8df982cd04ff6459434ed9780e229623bc92c0b'),
 ('results/stable_aest_cosmic_memory_r7a_live_epoch_derivative.npz','cc3e9b70809c44c8154abfc4cd3961d5f785f5cd3b327def2666e39bec789771'),
 ('results/stable_aest_cosmic_memory_r8a2_precision_qualified_tau_scan.json','2d6289c2fbd37bebcb904dade89f64c15a009e5c7454754b39d4dcc72924ca66'),
 ('results/stable_aest_cosmic_memory_r8a2_precision_qualified_tau_scan.npz','c81b2093a88719423e87ff5c180d790a56da6f396c0070858624879c90f26ee1'),
]
for fn, expected in parents:
    got=hashlib.sha256(Path(fn).read_bytes()).hexdigest()
    assert got==expected,(fn,got,expected)
r7=json.loads(Path(parents[0][0]).read_text())
r8=json.loads(Path(parents[2][0]).read_text())
assert r7['classification']=='STABLE_AEST_COSMIC_MEMORY_R7A_LIVE_LOOKBACK_DECOMPOSITION_CERTIFIED'
assert r7.get('diagnostic_complete') is True and all(r7['gates'].values())
assert r8['classification']=='STABLE_AEST_COSMIC_MEMORY_R8A2_TAU_GENERALITY_CERTIFIED'
assert r8.get('diagnostic_complete') is True and all(r8['gates'].values())
print('STABLE_AEST_COSMIC_MEMORY_R8B_PARENT_PASS')
PY

source results/nl1c6d2n_corrected_class_densek64_env.sh
OLD_ROOT="$NL1C6D2N_CLASS_ROOT"
EXPECTED_CLASS_HEAD='e85808324f51fc694d12e3ed7439552a3c3f9540'
EXPECTED_MEMORY_SHA='4d5ab5dc7066d4880f06fcfc731d6534ed0ff992e3cc15fb473dddccb25a594f'
[[ "$(git -C "$OLD_ROOT" rev-parse HEAD)" == "$EXPECTED_CLASS_HEAD" ]]
[[ "$(sha256sum "$OLD_ROOT/source/aest_memory.c" | awk '{print $1}')" == "$EXPECTED_MEMORY_SHA" ]]
echo "STABLE_AEST_COSMIC_MEMORY_R8B_OLD_PROVENANCE_PASS head=$EXPECTED_CLASS_HEAD"

R8B_ROOT="$ROOT/.local/class_corrected_e8580832_densek64_stablechi_r8blookback"
R8B_PYTARGET="$ROOT/.local/classy_corrected_e8580832_densek64_stablechi_r8blookback"
rm -rf "$R8B_ROOT" "$R8B_PYTARGET"
cp -a "$OLD_ROOT" "$R8B_ROOT"
python fullj_weyl/apply_aest_stable_chi_residual_patch.py "$R8B_ROOT"
[[ "$(git -C "$R8B_ROOT" rev-parse HEAD)" == "$EXPECTED_CLASS_HEAD" ]]
[[ "$(sha256sum "$R8B_ROOT/source/aest_memory.c" | awk '{print $1}')" == "$EXPECTED_MEMORY_SHA" ]]

python - "$R8B_ROOT/source/perturbations.c" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]); s=p.read_text()
hook='        dy[pv->index_pt_E_aest] += aest_tangent_external_force(k,tau);'
n=s.count(hook)
if n != 1:
    raise SystemExit(f'R8B_DIAGNOSTIC_HOOK_COUNT_FAIL count={n}')
p.write_text(s.replace(hook,'',1))
print('STABLE_AEST_COSMIC_MEMORY_R8B_DORMANT_HOOK_NEUTRALIZED count_before=1 count_after=0')
PY

! grep -q 'aest_r2d_trace_force(k,pba->h,tau' "$R8B_ROOT/source/perturbations.c"
python fullj_weyl/apply_stable_aest_r7a_live_epoch_patch.py "$R8B_ROOT"

grep -q 'FULLJ_AEST_STABLE_CHI_RESIDUAL_V1' "$R8B_ROOT/source/perturbations.c"
grep -q 'FULLJ_STABLE_AEST_R7A_LIVE_EPOCH_V1' "$R8B_ROOT/source/perturbations.c"
[[ "$(grep -Fc 'Bchi_aest *= pba->aest_eta*aest_r7a_epoch_weight(a);' "$R8B_ROOT/source/perturbations.c")" -eq 1 ]]
[[ "$(grep -Fc 'E_rhs_aest -= 0.5*Q_aest*Bchi_aest;' "$R8B_ROOT/source/perturbations.c")" -eq 1 ]]
HOOK='dy[pv->index_pt_E_aest] += aest_tangent_external_force(k,tau);'
[[ "$(grep -Fc "$HOOK" "$R8B_ROOT/source/perturbations.c")" -eq 0 ]]
[[ "$(grep -Fc 'aest_r2d_trace_force(k,pba->h,tau' "$R8B_ROOT/source/perturbations.c")" -eq 0 ]]
[[ "$(grep -Ec 'double[[:space:]]+aest_r7a_epoch_weight[[:space:]]*\(' "$R8B_ROOT/source/aest_memory.c")" -eq 1 ]]
! grep -q 'pba->aest_eta < 0.' "$R8B_ROOT/source/input.c"
[[ "$(grep -Fc 'FULLJ_STABLE_AEST_R7A_SIGNED_ETA_DIAGNOSTIC_V1' "$R8B_ROOT/source/input.c")" -eq 1 ]]
echo STABLE_AEST_COSMIC_MEMORY_R8B_DIRECT_SOURCE_PASS

rm -rf "$R8B_ROOT/build" "$R8B_ROOT/python/build" "$R8B_ROOT/python/classy.egg-info" 2>/dev/null || true
mkdir -p "$R8B_PYTARGET"
python -m pip install --no-deps --no-build-isolation --target "$R8B_PYTARGET" "$R8B_ROOT"

export AEST_STABLE_R8B_CLASS_ROOT="$R8B_ROOT"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
unset AEST_R7A_EPOCH_MODE \
  AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE \
  AEST_R2D_TRACE_FILE AEST_R2D_TRACE_KH AEST_R2D_TRACE_ALL_K \
  AEST_TANGENT_ALLOW_K_MISS AEST_ERHS_TRACE_FILE AEST_ERHS_TRACE_K || true

echo STABLE_AEST_COSMIC_MEMORY_R8B_DIRECT_PHYSICAL_PASS

JSON='results/stable_aest_cosmic_memory_r8b_two_tau_lookback.json'
NPZ='results/stable_aest_cosmic_memory_r8b_two_tau_lookback.npz'
LOG='results/stable_aest_cosmic_memory_r8b_two_tau_lookback.log'
FULLLOG='results/stable_aest_cosmic_memory_r8b_two_tau_lookback_FULL_runner.log'
ZIP='results/stable_aest_cosmic_memory_r8b_two_tau_lookback_bundle.zip'
ENVOUT='results/stable_aest_cosmic_memory_r8b_environment.txt'
WORK='results/stable_aest_cosmic_memory_r8b_work'
rm -f "$JSON" "$NPZ" "$LOG" "$ZIP" "$ENVOUT"
rm -rf "$WORK"

{
  echo "repo_head=$(git rev-parse HEAD)"
  echo "predata_lock=$PREDATA_LOCK"
  echo "r7a_postdata_lock=$R7A_POSTDATA_LOCK"
  echo "r8a2_postdata_lock=$R8A2_POSTDATA_LOCK"
  echo "class_parent_head=$EXPECTED_CLASS_HEAD"
  echo "r8b_source=$R8B_ROOT"
  echo "python=$(python --version 2>&1)"
  echo '--- pip freeze ---'
  python -m pip freeze
} > "$ENVOUT"

set +e
PYTHONPATH="$R8B_PYTARGET" python -u -m fullj_weyl.stable_aest_cosmic_memory_r8b_two_tau_lookback \
  --json-out "$JSON" --npz-out "$NPZ" --workdir "$WORK" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

python - "$ZIP" "$LOG" "$JSON" "$NPZ" "$ENVOUT" "$WORK" <<'PY'
from pathlib import Path
import sys,zipfile
zp=Path(sys.argv[1]); work=Path(sys.argv[6])
paths=[Path(x) for x in sys.argv[2:6]]+[
 Path('docs/stable_aest_cosmic_memory_r8b_two_tau_lookback_predata.md'),
 Path('docs/stable_aest_cosmic_memory_r8a2_precision_qualified_tau_scan_postdata.md'),
 Path('docs/stable_aest_cosmic_memory_r7a_live_epoch_derivative_postdata.md'),
 Path('fullj_weyl/stable_aest_cosmic_memory_r8b_two_tau_lookback.py'),
 Path('fullj_weyl/run_local_stable_aest_cosmic_memory_r8b_two_tau_lookback.sh'),
 Path('fullj_weyl/stable_aest_cosmic_memory_r8a2_precision_qualified_tau_scan.py'),
 Path('fullj_weyl/apply_stable_aest_r7a_live_epoch_patch.py'),
 Path('fullj_weyl/apply_aest_stable_chi_residual_patch.py'),
 Path('results/stable_aest_cosmic_memory_r8a2_precision_qualified_tau_scan.json'),
 Path('results/stable_aest_cosmic_memory_r8a2_precision_qualified_tau_scan.npz'),
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
print('STABLE_AEST_COSMIC_MEMORY_R8B_BUNDLE='+str(zp))
PY

echo "STABLE_AEST_COSMIC_MEMORY_R8B_EXIT=$code"
echo "STABLE_AEST_COSMIC_MEMORY_R8B_LOG=$LOG"
echo "STABLE_AEST_COSMIC_MEMORY_R8B_JSON=$JSON"
echo "STABLE_AEST_COSMIC_MEMORY_R8B_NPZ=$NPZ"
echo "STABLE_AEST_COSMIC_MEMORY_R8B_ZIP=$ZIP"
exit "$code"
