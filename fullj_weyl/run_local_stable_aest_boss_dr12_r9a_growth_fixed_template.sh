#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

BASE_PY="$(command -v python3 || command -v python)"
[[ -n "$BASE_PY" ]] || { echo 'R9A: python missing' >&2; exit 2; }
VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then "$BASE_PY" -m venv "$VENV"; fi
export PATH="$VENV/bin:$PATH"
python -m pip install numpy scipy cython >/dev/null
python -m py_compile \
  fullj_weyl/stable_aest_boss_dr12_r9a_growth_fixed_template.py \
  fullj_weyl/stable_aest_cosmic_memory_r8a_tau_amplitude_scan.py \
  fullj_weyl/stable_aest_observable_projection_r5b_derivative_zero.py \
  fullj_weyl/apply_stable_aest_r7a_live_epoch_patch.py \
  fullj_weyl/apply_aest_stable_chi_residual_patch.py
echo STABLE_AEST_BOSS_DR12_R9A_IMPORT_PASS

for f in \
  docs/stable_aest_boss_dr12_r9a_growth_fixed_template_prefit.md \
  docs/stable_aest_cosmic_memory_r7a_live_epoch_derivative_postdata.md \
  docs/stable_aest_cosmic_memory_r8a2_precision_qualified_tau_scan_postdata.md \
  docs/stable_aest_cosmic_memory_r8b_two_tau_lookback_postdata.md \
  results/stable_aest_cosmic_memory_r7a_live_epoch_derivative.json \
  results/stable_aest_cosmic_memory_r8a2_precision_qualified_tau_scan.json \
  results/stable_aest_cosmic_memory_r8b_two_tau_lookback.json \
  results/stable_aest_cosmic_memory_r8b_two_tau_lookback.npz \
  results/nl1c6d2n_corrected_class_densek64_env.sh; do
  [[ -f "$f" ]] || { echo "R9A: missing $f" >&2; exit 3; }
done

PREFIT_LOCK='63f4bea97c95a5627f659415f556636c1af21fad'
R7A_POSTDATA_LOCK='86c03e6ba2ee9fcbf33a9d319d12ae778a747881'
R8A2_POSTDATA_LOCK='590dbc69e2823f583b157af2297e357991103c47'
R8B_POSTDATA_LOCK='9e21c61210979ab841918ba16f2210020daa245a'
for x in "$PREFIT_LOCK" "$R7A_POSTDATA_LOCK" "$R8A2_POSTDATA_LOCK" "$R8B_POSTDATA_LOCK"; do
  git merge-base --is-ancestor "$x" HEAD
 done
echo "STABLE_AEST_BOSS_DR12_R9A_SCIENCE_LOCK_PASS prefit=$PREFIT_LOCK r7a=$R7A_POSTDATA_LOCK r8a2=$R8A2_POSTDATA_LOCK r8b=$R8B_POSTDATA_LOCK"

python - <<'PY'
from pathlib import Path
p=Path('fullj_weyl/stable_aest_boss_dr12_r9a_growth_fixed_template.py').read_text()
required=[
 'PREFIT_LOCK = "63f4bea97c95a5627f659415f556636c1af21fad"',
 'R7A_POSTDATA_LOCK = "86c03e6ba2ee9fcbf33a9d319d12ae778a747881"',
 'R8A2_POSTDATA_LOCK = "590dbc69e2823f58343830d974e99b"'[:0],
]
# Explicit checks kept separate to avoid accidental typo hiding in a composite list.
assert 'R8A2_POSTDATA_LOCK = "590dbc69e2823f583b157af2297e357991103c47"' in p
assert 'R8B_POSTDATA_LOCK = "9e21c61210979ab841918ba16f2210020daa245a"' in p
assert 'BOSS_REPO_COMMIT = "bb0c1c9009dc76d1391300e169e8df38fd1096db"' in p
assert 'Z_BOSS = np.asarray([0.38, 0.51, 0.61]' in p
assert 'FS_INDICES = np.asarray([2, 5, 8]' in p
assert 'TAUS = (10.0, 5.0, 2.5, 1.25)' in p
assert 'EPS_PRIMARY = 0.025' in p and 'EPS_CONTROL = 0.05' in p
assert 'ETA_PHYS_MAX = 0.05' in p
assert 'tperp = t - proj * a' in p
assert 'gls_two_column' in p
assert 'physical_delta_chi2_vs_eta0' in p
for forbidden in ('force_full.dat','normalize_force(','partition_force(', 'AEST_TANGENT_FORCE_FILE"] ='):
    assert forbidden not in p, forbidden
print('STABLE_AEST_BOSS_DR12_R9A_ANTI_STALE_CODE_PASS')
PY

python - <<'PY'
import hashlib,json
from pathlib import Path
r7=json.loads(Path('results/stable_aest_cosmic_memory_r7a_live_epoch_derivative.json').read_text())
r82=json.loads(Path('results/stable_aest_cosmic_memory_r8a2_precision_qualified_tau_scan.json').read_text())
r8b_j=Path('results/stable_aest_cosmic_memory_r8b_two_tau_lookback.json')
r8b_n=Path('results/stable_aest_cosmic_memory_r8b_two_tau_lookback.npz')
r8b=json.loads(r8b_j.read_text())
assert r7['classification']=='STABLE_AEST_COSMIC_MEMORY_R7A_LIVE_LOOKBACK_DECOMPOSITION_CERTIFIED'
assert r82['classification']=='STABLE_AEST_COSMIC_MEMORY_R8A2_TAU_GENERALITY_CERTIFIED'
assert r8b['classification']=='STABLE_AEST_COSMIC_MEMORY_R8B_TWO_TAU_LOOKBACK_CERTIFIED'
assert all(r7['gates'].values()) and all(r82['gates'].values()) and all(r8b['gates'].values())
assert hashlib.sha256(r8b_j.read_bytes()).hexdigest()=='925d882609149720dc84360142085038953384b548f22945ddc58fdb83a6d861'
assert hashlib.sha256(r8b_n.read_bytes()).hexdigest()=='a9aaba1f0daf635358a24832bd5ccc3d606a6e70e65b4aa186dd0117ba757fa4'
print('STABLE_AEST_BOSS_DR12_R9A_PARENT_PASS')
PY

# Fresh, pinned observational-data checkout.
BOSS_COMMIT='bb0c1c9009dc76d1391300e169e8df38fd1096db'
BOSS_ROOT="$ROOT/.local/cobaya_bao_data_r9a"
rm -rf "$BOSS_ROOT"
mkdir -p "$BOSS_ROOT"
git -C "$BOSS_ROOT" init -q
git -C "$BOSS_ROOT" remote add origin https://github.com/CobayaSampler/bao_data.git
git -C "$BOSS_ROOT" fetch -q --depth=1 origin "$BOSS_COMMIT"
git -C "$BOSS_ROOT" checkout -q FETCH_HEAD
[[ "$(git -C "$BOSS_ROOT" rev-parse HEAD)" == "$BOSS_COMMIT" ]]
DATA_SHA="$(sha256sum "$BOSS_ROOT/sdss_DR12Consensus_final.dat" | awk '{print $1}')"
COV_SHA="$(sha256sum "$BOSS_ROOT/final_consensus_covtot_dM_Hz_fsig.txt" | awk '{print $1}')"
[[ "$DATA_SHA" == 'eae45d2629dc1214b351716b3ff9a6f5a22f170b71e3d0e93aeeddc169d80e30' ]]
[[ "$COV_SHA" == 'dea6d8d4893d2b84772f9b83d0653bf7d4ee81a0aeb63ce04859e20d0ad3a289' ]]
echo "STABLE_AEST_BOSS_DR12_R9A_DATA_PROVENANCE_PASS commit=$BOSS_COMMIT data_sha=$DATA_SHA cov_sha=$COV_SHA"

source results/nl1c6d2n_corrected_class_densek64_env.sh
OLD_ROOT="$NL1C6D2N_CLASS_ROOT"
EXPECTED_CLASS_HEAD='e85808324f51fc694d12e3ed7439552a3c3f9540'
EXPECTED_MEMORY_SHA='4d5ab5dc7066d4880f06fcfc731d6534ed0ff992e3cc15fb473dddccb25a594f'
[[ "$(git -C "$OLD_ROOT" rev-parse HEAD)" == "$EXPECTED_CLASS_HEAD" ]]
[[ "$(sha256sum "$OLD_ROOT/source/aest_memory.c" | awk '{print $1}')" == "$EXPECTED_MEMORY_SHA" ]]
echo "STABLE_AEST_BOSS_DR12_R9A_OLD_PROVENANCE_PASS head=$EXPECTED_CLASS_HEAD"

R9A_ROOT="$ROOT/.local/class_corrected_e8580832_densek64_stablechi_r9aboss"
R9A_PYTARGET="$ROOT/.local/classy_corrected_e8580832_densek64_stablechi_r9aboss"
rm -rf "$R9A_ROOT" "$R9A_PYTARGET"
cp -a "$OLD_ROOT" "$R9A_ROOT"
python fullj_weyl/apply_aest_stable_chi_residual_patch.py "$R9A_ROOT"
[[ "$(git -C "$R9A_ROOT" rev-parse HEAD)" == "$EXPECTED_CLASS_HEAD" ]]
[[ "$(sha256sum "$R9A_ROOT/source/aest_memory.c" | awk '{print $1}')" == "$EXPECTED_MEMORY_SHA" ]]

python - "$R9A_ROOT/source/perturbations.c" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]); s=p.read_text()
hook='        dy[pv->index_pt_E_aest] += aest_tangent_external_force(k,tau);'
n=s.count(hook)
if n != 1:
    raise SystemExit(f'R9A_DIAGNOSTIC_HOOK_COUNT_FAIL count={n}')
p.write_text(s.replace(hook,'',1))
print('STABLE_AEST_BOSS_DR12_R9A_DORMANT_HOOK_NEUTRALIZED count_before=1 count_after=0')
PY

! grep -q 'aest_r2d_trace_force(k,pba->h,tau' "$R9A_ROOT/source/perturbations.c"
python fullj_weyl/apply_stable_aest_r7a_live_epoch_patch.py "$R9A_ROOT"

grep -q 'FULLJ_AEST_STABLE_CHI_RESIDUAL_V1' "$R9A_ROOT/source/perturbations.c"
grep -q 'FULLJ_STABLE_AEST_R7A_LIVE_EPOCH_V1' "$R9A_ROOT/source/perturbations.c"
[[ "$(grep -Fc 'Bchi_aest *= pba->aest_eta*aest_r7a_epoch_weight(a);' "$R9A_ROOT/source/perturbations.c")" -eq 1 ]]
[[ "$(grep -Fc 'E_rhs_aest -= 0.5*Q_aest*Bchi_aest;' "$R9A_ROOT/source/perturbations.c")" -eq 1 ]]
HOOK='dy[pv->index_pt_E_aest] += aest_tangent_external_force(k,tau);'
[[ "$(grep -Fc "$HOOK" "$R9A_ROOT/source/perturbations.c")" -eq 0 ]]
[[ "$(grep -Fc 'aest_r2d_trace_force(k,pba->h,tau' "$R9A_ROOT/source/perturbations.c")" -eq 0 ]]
! grep -q 'pba->aest_eta < 0.' "$R9A_ROOT/source/input.c"
echo STABLE_AEST_BOSS_DR12_R9A_DIRECT_SOURCE_PASS

rm -rf "$R9A_ROOT/build" "$R9A_ROOT/python/build" "$R9A_ROOT/python/classy.egg-info" 2>/dev/null || true
mkdir -p "$R9A_PYTARGET"
python -m pip install --no-deps --no-build-isolation --target "$R9A_PYTARGET" "$R9A_ROOT"

export AEST_STABLE_R8A_CLASS_ROOT="$R9A_ROOT"
export AEST_R9A_BOSS_DATA_DIR="$BOSS_ROOT"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
unset AEST_R7A_EPOCH_MODE \
  AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE \
  AEST_R2D_TRACE_FILE AEST_R2D_TRACE_KH AEST_R2D_TRACE_ALL_K \
  AEST_TANGENT_ALLOW_K_MISS AEST_ERHS_TRACE_FILE AEST_ERHS_TRACE_K || true

echo STABLE_AEST_BOSS_DR12_R9A_DIRECT_PHYSICAL_PASS

JSON='results/stable_aest_boss_dr12_r9a_growth_fixed_template.json'
NPZ='results/stable_aest_boss_dr12_r9a_growth_fixed_template.npz'
LOG='results/stable_aest_boss_dr12_r9a_growth_fixed_template.log'
ZIP='results/stable_aest_boss_dr12_r9a_growth_fixed_template_bundle.zip'
ENVOUT='results/stable_aest_boss_dr12_r9a_environment.txt'
WORK='results/stable_aest_boss_dr12_r9a_work'
rm -f "$JSON" "$NPZ" "$LOG" "$ZIP" "$ENVOUT"
rm -rf "$WORK"

{
  echo "repo_head=$(git rev-parse HEAD)"
  echo "prefit_lock=$PREFIT_LOCK"
  echo "r7a_postdata_lock=$R7A_POSTDATA_LOCK"
  echo "r8a2_postdata_lock=$R8A2_POSTDATA_LOCK"
  echo "r8b_postdata_lock=$R8B_POSTDATA_LOCK"
  echo "boss_commit=$BOSS_COMMIT"
  echo "boss_data_sha256=$DATA_SHA"
  echo "boss_cov_sha256=$COV_SHA"
  echo "class_parent_head=$EXPECTED_CLASS_HEAD"
  echo "r9a_source=$R9A_ROOT"
  echo "python=$(python --version 2>&1)"
  echo '--- pip freeze ---'
  python -m pip freeze
} > "$ENVOUT"

set +e
PYTHONPATH="$R9A_PYTARGET" python -u -m fullj_weyl.stable_aest_boss_dr12_r9a_growth_fixed_template \
  --boss-data-dir "$BOSS_ROOT" --json-out "$JSON" --npz-out "$NPZ" --workdir "$WORK" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

python - "$ZIP" "$LOG" "$JSON" "$NPZ" "$ENVOUT" "$WORK" "$BOSS_ROOT" <<'PY'
from pathlib import Path
import sys,zipfile
zp=Path(sys.argv[1]); work=Path(sys.argv[6]); boss=Path(sys.argv[7])
paths=[Path(x) for x in sys.argv[2:6]]+[
 Path('docs/stable_aest_boss_dr12_r9a_growth_fixed_template_prefit.md'),
 Path('docs/stable_aest_cosmic_memory_r7a_live_epoch_derivative_postdata.md'),
 Path('docs/stable_aest_cosmic_memory_r8a2_precision_qualified_tau_scan_postdata.md'),
 Path('docs/stable_aest_cosmic_memory_r8b_two_tau_lookback_postdata.md'),
 Path('fullj_weyl/stable_aest_boss_dr12_r9a_growth_fixed_template.py'),
 Path('fullj_weyl/run_local_stable_aest_boss_dr12_r9a_growth_fixed_template.sh'),
 Path('fullj_weyl/apply_stable_aest_r7a_live_epoch_patch.py'),
 Path('fullj_weyl/apply_aest_stable_chi_residual_patch.py'),
 Path('results/stable_aest_cosmic_memory_r7a_live_epoch_derivative.json'),
 Path('results/stable_aest_cosmic_memory_r8a2_precision_qualified_tau_scan.json'),
 Path('results/stable_aest_cosmic_memory_r8b_two_tau_lookback.json'),
 Path('results/stable_aest_cosmic_memory_r8b_two_tau_lookback.npz'),
 boss/'sdss_DR12Consensus_final.dat', boss/'final_consensus_covtot_dM_Hz_fsig.txt']
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED) as zf:
    seen=set()
    for p in paths:
        if p.exists() and p not in seen:
            arc=str(p)
            if p.is_relative_to(boss): arc='boss_data/'+p.name
            zf.write(p,arcname=arc); seen.add(p)
    if work.exists():
        for p in sorted(work.rglob('*')):
            if p.is_file(): zf.write(p,arcname=str(p))
print('STABLE_AEST_BOSS_DR12_R9A_BUNDLE='+str(zp))
PY

echo "STABLE_AEST_BOSS_DR12_R9A_EXIT=$code"
echo "STABLE_AEST_BOSS_DR12_R9A_LOG=$LOG"
echo "STABLE_AEST_BOSS_DR12_R9A_JSON=$JSON"
echo "STABLE_AEST_BOSS_DR12_R9A_NPZ=$NPZ"
echo "STABLE_AEST_BOSS_DR12_R9A_ZIP=$ZIP"
exit "$code"
