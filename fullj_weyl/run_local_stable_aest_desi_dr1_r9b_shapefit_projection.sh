#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

BASE_PY="$(command -v python3 || command -v python)"
[[ -n "$BASE_PY" ]] || { echo 'R9B: python missing' >&2; exit 2; }
VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then "$BASE_PY" -m venv "$VENV"; fi
export PATH="$VENV/bin:$PATH"

DESI_COMMIT='7d51f4f86dc3bee6bf10f1a684913c943a89a844'
LSSTYPES_COMMIT='53f048e610bcb008548f66822b0879ce9df58cb1'
COSMOPRIMO_COMMIT='2e59c963c9b8e7cba1a4c8f161e978c6f4d80c2d'
PREFIT_LOCK='f19f7ddb85ee37d86a516ebdf41d73b96aef311e'
PREFIT_REPAIR01_LOCK='76f2a9002b9fde5e568670d3ea2f638f999cef74'
R9A_POSTDATA_LOCK='a6c0ed87dbc489f929c2a62fdac93ca6e4a2fd37'
R8B_POSTDATA_LOCK='9e21c61210979ab841918ba16f2210020daa245a'
R8A2_POSTDATA_LOCK='590dbc69e2823f583b157af2297e357991103c47'
R7A_POSTDATA_LOCK='86c03e6ba2ee9fcbf33a9d319d12ae778a747881'

python -m pip install -q numpy scipy cython requests beautifulsoup4 h5py camb
python -m pip install -q "git+https://github.com/adematti/lsstypes.git@$LSSTYPES_COMMIT"
python -m pip install -q "git+https://github.com/cosmodesi/cosmoprimo.git@$COSMOPRIMO_COMMIT"
python -m py_compile \
  fullj_weyl/stable_aest_desi_dr1_r9b_shapefit_projection.py \
  fullj_weyl/stable_aest_observable_projection_r5b_derivative_zero.py \
  fullj_weyl/stable_aest_cosmic_memory_r8a_tau_amplitude_scan.py \
  fullj_weyl/apply_stable_aest_r7a_live_epoch_patch.py \
  fullj_weyl/apply_aest_stable_chi_residual_patch.py
echo STABLE_AEST_DESI_DR1_R9B_IMPORT_PASS

for f in \
  docs/stable_aest_desi_dr1_r9b_shapefit_growth_shape_prefit.md \
  docs/stable_aest_desi_dr1_r9b_shapefit_growth_shape_prefit_repair01.md \
  docs/stable_aest_boss_dr12_r9a_growth_fixed_template_postdata.md \
  docs/stable_aest_cosmic_memory_r8b_two_tau_lookback_postdata.md \
  docs/stable_aest_cosmic_memory_r8a2_precision_qualified_tau_scan_postdata.md \
  docs/stable_aest_cosmic_memory_r7a_live_epoch_derivative_postdata.md \
  results/stable_aest_boss_dr12_r9a_growth_fixed_template.json \
  results/stable_aest_cosmic_memory_r8b_two_tau_lookback.json \
  results/stable_aest_cosmic_memory_r8a2_precision_qualified_tau_scan.json \
  results/stable_aest_cosmic_memory_r7a_live_epoch_derivative.json \
  results/nl1c6d2n_corrected_class_densek64_env.sh; do
  [[ -f "$f" ]] || { echo "R9B: missing $f" >&2; exit 3; }
done

for x in "$PREFIT_LOCK" "$PREFIT_REPAIR01_LOCK" "$R9A_POSTDATA_LOCK" "$R8B_POSTDATA_LOCK" "$R8A2_POSTDATA_LOCK" "$R7A_POSTDATA_LOCK"; do
  git merge-base --is-ancestor "$x" HEAD
 done
echo "STABLE_AEST_DESI_DR1_R9B_SCIENCE_LOCK_PASS prefit=$PREFIT_LOCK repair=$PREFIT_REPAIR01_LOCK r9a=$R9A_POSTDATA_LOCK"

python - <<'PY'
from pathlib import Path
p=Path('fullj_weyl/stable_aest_desi_dr1_r9b_shapefit_projection.py').read_text()
required=[
 'PREFIT_LOCK = "f19f7ddb85ee37d86a516ebdf41d73b96aef311e"',
 'PREFIT_REPAIR01_LOCK = "76f2a9002b9fde5e568670d3ea2f638f999cef74"',
 'R9A_POSTDATA_LOCK = "a6c0ed87dbc489f929c2a62fdac93ca6e4a2fd37"',
 'DESI_REPO_COMMIT = "7d51f4f86dc3bee6bf10f1a684913c943a89a844"',
 'TRACERS = (',
 'TAUS = (10.0, 5.0, 2.5, 1.25)',
 'EPS_PRIMARY = 0.025',
 'EPS_CONTROL = 0.05',
 'ETA_PHYS_MAX = 0.05',
 'f_eff = fsigma8/sigma8',
 'global_df_scale',
 'global_dm_offset',
 'Pperp = P-P@N@Minv@N.T@P',
 'CLS_PASS = "STABLE_AEST_DESI_DR1_R9B_SHAPEFIT_MEMORY_PROJECTION_CERTIFIED"',
]
for token in required:
    assert token in p, token
for forbidden in ('force_full.dat','normalize_force(','partition_force(', 'AEST_TANGENT_FORCE_FILE"] ='):
    assert forbidden not in p, forbidden
print('STABLE_AEST_DESI_DR1_R9B_ANTI_STALE_CODE_PASS')
PY

# Fresh, exact official DESI Key Project likelihood repository.
DESI_REPO="$ROOT/.local/desi_kp_likelihoods_r9b"
rm -rf "$DESI_REPO"
git clone -q https://github.com/cosmodesi/desi-kp-cosmological-likelihoods.git "$DESI_REPO"
git -C "$DESI_REPO" checkout -q "$DESI_COMMIT"
[[ "$(git -C "$DESI_REPO" rev-parse HEAD)" == "$DESI_COMMIT" ]]
echo "STABLE_AEST_DESI_DR1_R9B_OFFICIAL_REPO_PASS head=$DESI_COMMIT"

# Fresh official DESI DR1 likelihood download. This is intentionally NOT quiet:
# the terminal should visibly print every downloaded HDF5 file.
DESI_DATA="$ROOT/.local/desi_dr1_r9b_likelihood_data"
rm -rf "$DESI_DATA"
mkdir -p "$DESI_DATA"
python "$DESI_REPO/dr1/cobaya/download.py" --data-dir "$DESI_DATA"

required_h5=(
'likelihood_shapefit_spectrum-poles-rotated+bao-recon_syst-rotation-hod-photo_BGS_BRIGHT-21.5_GCcomb_z0.1-0.4_thetacut0.05.h5'
'likelihood_shapefit_spectrum-poles-rotated+bao-recon_syst-rotation-hod-photo_LRG_GCcomb_z0.4-0.6_thetacut0.05.h5'
'likelihood_shapefit_spectrum-poles-rotated+bao-recon_syst-rotation-hod-photo_LRG_GCcomb_z0.6-0.8_thetacut0.05.h5'
'likelihood_shapefit_spectrum-poles-rotated+bao-recon_syst-rotation-hod-photo_LRG_GCcomb_z0.8-1.1_thetacut0.05.h5'
'likelihood_shapefit_spectrum-poles-rotated+bao-recon_syst-rotation-hod-photo_ELG_LOPnotqso_GCcomb_z1.1-1.6_thetacut0.05.h5'
'likelihood_shapefit_spectrum-poles-rotated+bao-recon_syst-rotation-hod-photo_QSO_GCcomb_z0.8-2.1_thetacut0.05.h5'
)
MANIFEST='results/stable_aest_desi_dr1_r9b_data_manifest.txt'
: > "$MANIFEST"
for f in "${required_h5[@]}"; do
  [[ -s "$DESI_DATA/$f" ]] || { echo "R9B: required DESI HDF5 missing: $f" >&2; exit 4; }
  sha256sum "$DESI_DATA/$f" | tee -a "$MANIFEST"
done
echo STABLE_AEST_DESI_DR1_R9B_DATA_DOWNLOAD_PASS

# Parent-result classifications must remain frozen.
python - <<'PY'
import json
from pathlib import Path
checks=[
 ('results/stable_aest_boss_dr12_r9a_growth_fixed_template.json','STABLE_AEST_BOSS_DR12_R9A_GROWTH_TEMPLATE_PROJECTION_CERTIFIED'),
 ('results/stable_aest_cosmic_memory_r8b_two_tau_lookback.json','STABLE_AEST_COSMIC_MEMORY_R8B_TWO_TAU_LOOKBACK_CERTIFIED'),
 ('results/stable_aest_cosmic_memory_r8a2_precision_qualified_tau_scan.json','STABLE_AEST_COSMIC_MEMORY_R8A2_TAU_GENERALITY_CERTIFIED'),
 ('results/stable_aest_cosmic_memory_r7a_live_epoch_derivative.json','STABLE_AEST_COSMIC_MEMORY_R7A_LIVE_LOOKBACK_DECOMPOSITION_CERTIFIED'),
]
for fn, cls in checks:
    d=json.loads(Path(fn).read_text())
    assert d['classification']==cls,(fn,d['classification'])
    assert d.get('diagnostic_complete') is True,fn
    assert all(d['gates'].values()),fn
print('STABLE_AEST_DESI_DR1_R9B_PARENT_PASS')
PY

# Fresh disposable direct-physical stable-AeST source.
source results/nl1c6d2n_corrected_class_densek64_env.sh
OLD_ROOT="$NL1C6D2N_CLASS_ROOT"
EXPECTED_CLASS_HEAD='e85808324f51fc694d12e3ed7439552a3c3f9540'
EXPECTED_MEMORY_SHA='4d5ab5dc7066d4880f06fcfc731d6534ed0ff992e3cc15fb473dddccb25a594f'
[[ "$(git -C "$OLD_ROOT" rev-parse HEAD)" == "$EXPECTED_CLASS_HEAD" ]]
[[ "$(sha256sum "$OLD_ROOT/source/aest_memory.c" | awk '{print $1}')" == "$EXPECTED_MEMORY_SHA" ]]

echo "STABLE_AEST_DESI_DR1_R9B_OLD_PROVENANCE_PASS head=$EXPECTED_CLASS_HEAD"
R9B_ROOT="$ROOT/.local/class_corrected_e8580832_densek64_stablechi_r9bdesi"
R9B_PYTARGET="$ROOT/.local/classy_corrected_e8580832_densek64_stablechi_r9bdesi"
rm -rf "$R9B_ROOT" "$R9B_PYTARGET"
cp -a "$OLD_ROOT" "$R9B_ROOT"
python fullj_weyl/apply_aest_stable_chi_residual_patch.py "$R9B_ROOT"
[[ "$(git -C "$R9B_ROOT" rev-parse HEAD)" == "$EXPECTED_CLASS_HEAD" ]]
[[ "$(sha256sum "$R9B_ROOT/source/aest_memory.c" | awk '{print $1}')" == "$EXPECTED_MEMORY_SHA" ]]

python - "$R9B_ROOT/source/perturbations.c" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]); s=p.read_text()
hook='        dy[pv->index_pt_E_aest] += aest_tangent_external_force(k,tau);'
n=s.count(hook)
if n != 1:
    raise SystemExit(f'R9B_DIAGNOSTIC_HOOK_COUNT_FAIL count={n}')
p.write_text(s.replace(hook,'',1))
print('STABLE_AEST_DESI_DR1_R9B_DORMANT_HOOK_NEUTRALIZED count_before=1 count_after=0')
PY

! grep -q 'aest_r2d_trace_force(k,pba->h,tau' "$R9B_ROOT/source/perturbations.c"
python fullj_weyl/apply_stable_aest_r7a_live_epoch_patch.py "$R9B_ROOT"
grep -q 'FULLJ_AEST_STABLE_CHI_RESIDUAL_V1' "$R9B_ROOT/source/perturbations.c"
grep -q 'FULLJ_STABLE_AEST_R7A_LIVE_EPOCH_V1' "$R9B_ROOT/source/perturbations.c"
[[ "$(grep -Fc 'Bchi_aest *= pba->aest_eta*aest_r7a_epoch_weight(a);' "$R9B_ROOT/source/perturbations.c")" -eq 1 ]]
[[ "$(grep -Fc 'E_rhs_aest -= 0.5*Q_aest*Bchi_aest;' "$R9B_ROOT/source/perturbations.c")" -eq 1 ]]
HOOK='dy[pv->index_pt_E_aest] += aest_tangent_external_force(k,tau);'
[[ "$(grep -Fc "$HOOK" "$R9B_ROOT/source/perturbations.c")" -eq 0 ]]
[[ "$(grep -Fc 'aest_r2d_trace_force(k,pba->h,tau' "$R9B_ROOT/source/perturbations.c")" -eq 0 ]]
! grep -q 'pba->aest_eta < 0.' "$R9B_ROOT/source/input.c"
echo STABLE_AEST_DESI_DR1_R9B_DIRECT_SOURCE_PASS

rm -rf "$R9B_ROOT/build" "$R9B_ROOT/python/build" "$R9B_ROOT/python/classy.egg-info" 2>/dev/null || true
mkdir -p "$R9B_PYTARGET"
python -m pip install --no-deps --no-build-isolation --target "$R9B_PYTARGET" "$R9B_ROOT"

export AEST_STABLE_R8A_CLASS_ROOT="$R9B_ROOT"
export AEST_R9B_DESI_DATA_DIR="$DESI_DATA"
export AEST_R9B_DESI_REPO="$DESI_REPO"
export AEST_R7A_EPOCH_MODE=full
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
unset AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE \
  AEST_R2D_TRACE_FILE AEST_R2D_TRACE_KH AEST_R2D_TRACE_ALL_K \
  AEST_TANGENT_ALLOW_K_MISS AEST_ERHS_TRACE_FILE AEST_ERHS_TRACE_K || true

echo STABLE_AEST_DESI_DR1_R9B_DIRECT_PHYSICAL_PASS

JSON='results/stable_aest_desi_dr1_r9b_shapefit_projection.json'
NPZ='results/stable_aest_desi_dr1_r9b_shapefit_projection.npz'
LOG='results/stable_aest_desi_dr1_r9b_shapefit_projection.log'
ZIP='results/stable_aest_desi_dr1_r9b_shapefit_projection_bundle.zip'
ENVOUT='results/stable_aest_desi_dr1_r9b_environment.txt'
WORK='results/stable_aest_desi_dr1_r9b_work'
rm -f "$JSON" "$NPZ" "$LOG" "$ZIP" "$ENVOUT"
rm -rf "$WORK"

{
  echo "repo_head=$(git rev-parse HEAD)"
  echo "prefit_lock=$PREFIT_LOCK"
  echo "prefit_repair01_lock=$PREFIT_REPAIR01_LOCK"
  echo "r9a_postdata_lock=$R9A_POSTDATA_LOCK"
  echo "desi_repo_commit=$DESI_COMMIT"
  echo "lsstypes_commit=$LSSTYPES_COMMIT"
  echo "cosmoprimo_commit=$COSMOPRIMO_COMMIT"
  echo "class_parent_head=$EXPECTED_CLASS_HEAD"
  echo "python=$(python --version 2>&1)"
  echo '--- DESI HDF5 manifest ---'
  cat "$MANIFEST"
  echo '--- pip freeze ---'
  python -m pip freeze
} > "$ENVOUT"

set +e
PYTHONPATH="$R9B_PYTARGET:$PYTHONPATH" python -u -m fullj_weyl.stable_aest_desi_dr1_r9b_shapefit_projection \
  --data-dir "$DESI_DATA" --official-repo "$DESI_REPO" \
  --json-out "$JSON" --npz-out "$NPZ" --workdir "$WORK" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

python - "$ZIP" "$LOG" "$JSON" "$NPZ" "$ENVOUT" "$WORK" "$DESI_DATA" "$MANIFEST" <<'PY'
from pathlib import Path
import sys,zipfile,json
zp=Path(sys.argv[1]); work=Path(sys.argv[6]); data=Path(sys.argv[7]); manifest=Path(sys.argv[8])
paths=[Path(x) for x in sys.argv[2:6]]+[
 manifest,
 Path('docs/stable_aest_desi_dr1_r9b_shapefit_growth_shape_prefit.md'),
 Path('docs/stable_aest_desi_dr1_r9b_shapefit_growth_shape_prefit_repair01.md'),
 Path('docs/stable_aest_boss_dr12_r9a_growth_fixed_template_postdata.md'),
 Path('fullj_weyl/stable_aest_desi_dr1_r9b_shapefit_projection.py'),
 Path('fullj_weyl/run_local_stable_aest_desi_dr1_r9b_shapefit_projection.sh')]
if Path(sys.argv[3]).exists():
    try:
        r=json.loads(Path(sys.argv[3]).read_text())
        for fn in r.get('data',{}).get('files_sha256',{}): paths.append(data/fn)
    except Exception: pass
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED) as zf:
    seen=set()
    for p in paths:
        if p.exists() and p not in seen:
            arc=('desi_data/'+p.name) if p.is_relative_to(data) else str(p)
            zf.write(p,arcname=arc); seen.add(p)
    if work.exists():
        for p in sorted(work.rglob('*')):
            if p.is_file(): zf.write(p,arcname=str(p))
print('STABLE_AEST_DESI_DR1_R9B_BUNDLE='+str(zp))
PY

echo "STABLE_AEST_DESI_DR1_R9B_EXIT=$code"
echo "STABLE_AEST_DESI_DR1_R9B_LOG=$LOG"
echo "STABLE_AEST_DESI_DR1_R9B_JSON=$JSON"
echo "STABLE_AEST_DESI_DR1_R9B_NPZ=$NPZ"
echo "STABLE_AEST_DESI_DR1_R9B_ZIP=$ZIP"
exit "$code"
