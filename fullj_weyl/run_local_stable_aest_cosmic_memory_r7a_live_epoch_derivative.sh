#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

BASE_PY="$(command -v python3 || command -v python)"
[[ -n "$BASE_PY" ]] || { echo 'R7A: python missing' >&2; exit 2; }
VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then "$BASE_PY" -m venv "$VENV"; fi
export PATH="$VENV/bin:$PATH"
python -m pip install numpy scipy cython >/dev/null
python -m py_compile \
  fullj_weyl/stable_aest_cosmic_memory_r7a_live_epoch_derivative.py \
  fullj_weyl/stable_aest_observable_projection_r5b_derivative_zero.py \
  fullj_weyl/apply_stable_aest_r7a_live_epoch_patch.py \
  fullj_weyl/apply_aest_stable_chi_residual_patch.py
echo STABLE_AEST_COSMIC_MEMORY_R7A_IMPORT_PASS

for f in \
  docs/stable_aest_cosmic_memory_r7a_live_epoch_derivative_predata.md \
  docs/stable_aest_cosmic_memory_r7_lookback_decomposition_postdata.md \
  docs/stable_aest_observable_projection_r5b_derivative_zero_postdata.md \
  results/stable_aest_cosmic_memory_r7_lookback_decomposition.json \
  results/stable_aest_observable_projection_r5b_derivative_zero.json \
  results/stable_aest_observable_projection_r5b_derivative_zero.npz \
  results/nl1c6d2n_corrected_class_densek64_env.sh; do
  [[ -f "$f" ]] || { echo "R7A: missing $f" >&2; exit 3; }
done

PREDATA_LOCK='04c15f83032dd8a4a1baf2d26b576b00cc4c2681'
R7_POSTDATA_LOCK='cf0132f7877160948e1ba4670eda19750d82159b'
R5B_POSTDATA_LOCK='3242335ece23fbeb743f075a1df1aa70acaab211'
git merge-base --is-ancestor "$PREDATA_LOCK" HEAD
git merge-base --is-ancestor "$R7_POSTDATA_LOCK" HEAD
git merge-base --is-ancestor "$R5B_POSTDATA_LOCK" HEAD
echo "STABLE_AEST_COSMIC_MEMORY_R7A_SCIENCE_LOCK_PASS predata=$PREDATA_LOCK r7=$R7_POSTDATA_LOCK r5b=$R5B_POSTDATA_LOCK"

python - <<'PY'
from pathlib import Path
p=Path('fullj_weyl/stable_aest_cosmic_memory_r7a_live_epoch_derivative.py').read_text()
required=[
 'PREDATA_LOCK = "04c15f83032dd8a4a1baf2d26b576b00cc4c2681"',
 'R7_POSTDATA_LOCK = "cf0132f7877160948e1ba4670eda19750d82159b"',
 'R5B_POSTDATA_LOCK = "3242335ece23fbeb743f075a1df1aa70acaab211"',
 'EPS_PRIMARY = 0.025',
 'EPS_CONTROL = 0.05',
 'EPOCHS = ("ancient", "intermediate", "recent_structure", "late")',
 'CLS_PASS = "STABLE_AEST_COSMIC_MEMORY_R7A_LIVE_LOOKBACK_DECOMPOSITION_CERTIFIED"',
 '"AEST_R7A_EPOCH_MODE"',
]
for token in required:
    assert token in p,token
for forbidden in (
 'force_full.dat','force_ancient.dat','normalize_force(','partition_force(',
 'AEST_TANGENT_FORCE_FILE"] =','AEST_TANGENT_LAMBDA"] =','AEST_R2D_TRACE_FILE"] ='
):
    assert forbidden not in p,forbidden
print('STABLE_AEST_COSMIC_MEMORY_R7A_ANTI_STALE_CODE_PASS')
PY

python - <<'PY'
import hashlib,json
from pathlib import Path
r7=json.loads(Path('results/stable_aest_cosmic_memory_r7_lookback_decomposition.json').read_text())
assert r7['classification']=='STABLE_AEST_COSMIC_MEMORY_R7_PHYSICAL_BRIDGE_FAIL',r7['classification']
assert r7.get('diagnostic_complete') is True
r5j=Path('results/stable_aest_observable_projection_r5b_derivative_zero.json')
r5n=Path('results/stable_aest_observable_projection_r5b_derivative_zero.npz')
assert hashlib.sha256(r5j.read_bytes()).hexdigest()=='26ce723e2b7b783fcd19765c9c7f01b6101992a3f09e6ee321299bf148259ca9'
assert hashlib.sha256(r5n.read_bytes()).hexdigest()=='a88f99254bc1a7393e40691d5dc539bb1e1648eae1b892e43b63f593f8e367e1'
r5=json.loads(r5j.read_text())
assert r5['classification']=='STABLE_AEST_OBSERVABLE_PROJECTION_R5B_DERIVATIVE_ZERO_CERTIFIED',r5['classification']
assert r5.get('diagnostic_complete') is True
assert all(r5['gates'].values())
print('STABLE_AEST_COSMIC_MEMORY_R7A_PARENT_PASS')
PY

source results/nl1c6d2n_corrected_class_densek64_env.sh
OLD_ROOT="$NL1C6D2N_CLASS_ROOT"
EXPECTED_CLASS_HEAD='e85808324f51fc694d12e3ed7439552a3c3f9540'
EXPECTED_MEMORY_SHA='4d5ab5dc7066d4880f06fcfc731d6534ed0ff992e3cc15fb473dddccb25a594f'
[[ "$(git -C "$OLD_ROOT" rev-parse HEAD)" == "$EXPECTED_CLASS_HEAD" ]]
[[ "$(sha256sum "$OLD_ROOT/source/aest_memory.c" | awk '{print $1}')" == "$EXPECTED_MEMORY_SHA" ]]
echo "STABLE_AEST_COSMIC_MEMORY_R7A_OLD_PROVENANCE_PASS head=$EXPECTED_CLASS_HEAD"

R7A_ROOT="$ROOT/.local/class_corrected_e8580832_densek64_stablechi_r7alive"
R7A_PYTARGET="$ROOT/.local/classy_corrected_e8580832_densek64_stablechi_r7alive"
rm -rf "$R7A_ROOT" "$R7A_PYTARGET"
cp -a "$OLD_ROOT" "$R7A_ROOT"
python fullj_weyl/apply_aest_stable_chi_residual_patch.py "$R7A_ROOT"
[[ "$(git -C "$R7A_ROOT" rev-parse HEAD)" == "$EXPECTED_CLASS_HEAD" ]]
[[ "$(sha256sum "$R7A_ROOT/source/aest_memory.c" | awk '{print $1}')" == "$EXPECTED_MEMORY_SHA" ]]

# Neutralize exactly one dormant historical variational forcing hook, as in certified R5b.
python - "$R7A_ROOT/source/perturbations.c" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]); s=p.read_text()
hook='        dy[pv->index_pt_E_aest] += aest_tangent_external_force(k,tau);'
n=s.count(hook)
if n != 1:
    raise SystemExit(f'R7A_DIAGNOSTIC_HOOK_COUNT_FAIL count={n}')
p.write_text(s.replace(hook,'',1))
print('STABLE_AEST_COSMIC_MEMORY_R7A_DORMANT_HOOK_NEUTRALIZED count_before=1 count_after=0')
PY

# R7a is deliberately trace/replay free.
! grep -q 'aest_r2d_trace_force(k,pba->h,tau' "$R7A_ROOT/source/perturbations.c"
python fullj_weyl/apply_stable_aest_r7a_live_epoch_patch.py "$R7A_ROOT"

grep -q 'FULLJ_AEST_STABLE_CHI_RESIDUAL_V1' "$R7A_ROOT/source/perturbations.c"
grep -q 'FULLJ_STABLE_AEST_R7A_LIVE_EPOCH_V1' "$R7A_ROOT/source/perturbations.c"
[[ "$(grep -Fc 'Bchi_aest *= pba->aest_eta*aest_r7a_epoch_weight(a);' "$R7A_ROOT/source/perturbations.c")" -eq 1 ]]
[[ "$(grep -Fc 'E_rhs_aest -= 0.5*Q_aest*Bchi_aest;' "$R7A_ROOT/source/perturbations.c")" -eq 1 ]]
HOOK='dy[pv->index_pt_E_aest] += aest_tangent_external_force(k,tau);'
[[ "$(grep -Fc "$HOOK" "$R7A_ROOT/source/perturbations.c")" -eq 0 ]]
[[ "$(grep -Fc 'aest_r2d_trace_force(k,pba->h,tau' "$R7A_ROOT/source/perturbations.c")" -eq 0 ]]
[[ "$(grep -Ec 'double[[:space:]]+aest_r7a_epoch_weight[[:space:]]*\(' "$R7A_ROOT/source/aest_memory.c")" -eq 1 ]]
echo STABLE_AEST_COSMIC_MEMORY_R7A_LIVE_SOURCE_PASS

rm -rf "$R7A_ROOT/build" "$R7A_ROOT/python/build" "$R7A_ROOT/python/classy.egg-info" 2>/dev/null || true
mkdir -p "$R7A_PYTARGET"
python -m pip install --no-deps --no-build-isolation --target "$R7A_PYTARGET" "$R7A_ROOT"

export AEST_STABLE_R7A_CLASS_ROOT="$R7A_ROOT"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
unset AEST_R7A_EPOCH_MODE \
  AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE \
  AEST_R2D_TRACE_FILE AEST_R2D_TRACE_KH AEST_R2D_TRACE_ALL_K \
  AEST_TANGENT_ALLOW_K_MISS AEST_ERHS_TRACE_FILE AEST_ERHS_TRACE_K || true

echo STABLE_AEST_COSMIC_MEMORY_R7A_DIRECT_PHYSICAL_PASS

JSON='results/stable_aest_cosmic_memory_r7a_live_epoch_derivative.json'
NPZ='results/stable_aest_cosmic_memory_r7a_live_epoch_derivative.npz'
LOG='results/stable_aest_cosmic_memory_r7a_live_epoch_derivative.log'
FULLLOG='results/stable_aest_cosmic_memory_r7a_live_epoch_derivative_FULL_runner.log'
ZIP='results/stable_aest_cosmic_memory_r7a_live_epoch_derivative_bundle.zip'
ENVOUT='results/stable_aest_cosmic_memory_r7a_environment.txt'
WORK='results/stable_aest_cosmic_memory_r7a_work'
rm -f "$JSON" "$NPZ" "$LOG" "$ZIP" "$ENVOUT"
rm -rf "$WORK"

{
  echo "repo_head=$(git rev-parse HEAD)"
  echo "predata_lock=$PREDATA_LOCK"
  echo "r7_postdata_lock=$R7_POSTDATA_LOCK"
  echo "r5b_postdata_lock=$R5B_POSTDATA_LOCK"
  echo "class_parent_head=$EXPECTED_CLASS_HEAD"
  echo "r7a_source=$R7A_ROOT"
  echo "python=$(python --version 2>&1)"
  echo '--- pip freeze ---'
  python -m pip freeze
} > "$ENVOUT"

set +e
PYTHONPATH="$R7A_PYTARGET" python -u -m fullj_weyl.stable_aest_cosmic_memory_r7a_live_epoch_derivative \
  --json-out "$JSON" --npz-out "$NPZ" --workdir "$WORK" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

python - "$ZIP" "$LOG" "$JSON" "$NPZ" "$ENVOUT" "$WORK" <<'PY'
from pathlib import Path
import sys,zipfile
zp=Path(sys.argv[1]); work=Path(sys.argv[6])
paths=[Path(x) for x in sys.argv[2:6]]+[
 Path('docs/stable_aest_cosmic_memory_r7a_live_epoch_derivative_predata.md'),
 Path('docs/stable_aest_cosmic_memory_r7_lookback_decomposition_postdata.md'),
 Path('docs/stable_aest_observable_projection_r5b_derivative_zero_postdata.md'),
 Path('fullj_weyl/stable_aest_cosmic_memory_r7a_live_epoch_derivative.py'),
 Path('fullj_weyl/run_local_stable_aest_cosmic_memory_r7a_live_epoch_derivative.sh'),
 Path('fullj_weyl/apply_stable_aest_r7a_live_epoch_patch.py'),
 Path('fullj_weyl/apply_aest_stable_chi_residual_patch.py'),
 Path('results/stable_aest_cosmic_memory_r7_lookback_decomposition.json'),
 Path('results/stable_aest_observable_projection_r5b_derivative_zero.json'),
 Path('results/stable_aest_observable_projection_r5b_derivative_zero.npz')]
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED) as zf:
    seen=set()
    for p in paths:
        if p.exists() and p not in seen:
            zf.write(p,arcname=str(p)); seen.add(p)
    if work.exists():
        for p in sorted(work.rglob('*')):
            if p.is_file(): zf.write(p,arcname=str(p))
print('STABLE_AEST_COSMIC_MEMORY_R7A_BUNDLE='+str(zp))
PY

echo "STABLE_AEST_COSMIC_MEMORY_R7A_EXIT=$code"
echo "STABLE_AEST_COSMIC_MEMORY_R7A_LOG=$LOG"
echo "STABLE_AEST_COSMIC_MEMORY_R7A_JSON=$JSON"
echo "STABLE_AEST_COSMIC_MEMORY_R7A_NPZ=$NPZ"
echo "STABLE_AEST_COSMIC_MEMORY_R7A_ZIP=$ZIP"
exit "$code"
