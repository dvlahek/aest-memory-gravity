#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"; mkdir -p results .local

BASE_PY="$(command -v python3 || command -v python)"
[[ -n "$BASE_PY" ]] || { echo 'R2E: python missing' >&2; exit 2; }
VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then "$BASE_PY" -m venv "$VENV"; fi
export PATH="$VENV/bin:$PATH"
python -m pip install --upgrade pip setuptools wheel >/dev/null
python -m pip install numpy scipy cython >/dev/null
python -m py_compile \
  fullj_weyl/stable_aest_growth_weyl_memory_r2e_single_hook.py \
  fullj_weyl/stable_aest_growth_weyl_memory_r2d_full_history.py \
  fullj_weyl/apply_stable_aest_r2e_single_hook_patch.py \
  fullj_weyl/apply_stable_aest_r2d_full_history_patch.py \
  fullj_weyl/apply_stable_aest_r2b_variational_patch.py \
  fullj_weyl/apply_aest_stable_chi_residual_patch.py
echo STABLE_AEST_GROWTH_WEYL_MEMORY_R2E_IMPORT_PASS

for f in \
 docs/stable_aest_growth_weyl_memory_r2e_single_hook_predata.md \
 docs/stable_aest_growth_weyl_memory_r2d_full_history_postdata.md \
 results/stable_aest_growth_weyl_memory_r2d_full_history.json \
 results/stable_aest_growth_weyl_memory_r2d_full_history.npz \
 results/stable_aest_growth_weyl_memory_r2c_normalization.json \
 results/stable_aest_growth_weyl_memory_r2b_variational.json \
 results/stable_aest_growth_weyl_memory_r2.npz \
 results/stable_aest_finite_memory_r1c.json \
 results/fullj_aest_stable_chi_precision_floor.json \
 results/nl1c6d2n_corrected_class_densek64_env.sh \
 results/stable_aest_growth_weyl_memory_r2d_work/rhs_force_0p09875.dat \
 results/stable_aest_growth_weyl_memory_r2d_work/rhs_force_0p16125.dat \
 results/stable_aest_growth_weyl_memory_r2d_work/rhs_force_0p19500.dat; do
 [[ -f "$f" ]] || { echo "R2E: missing $f" >&2; exit 3; }
done

PREDATA_LOCK='176b69261d61c9d43116a9bf82a99839fe328b43'
R2D_POSTDATA_LOCK='d2589759cda81a590008c184cc2b061eada3ee28'
git merge-base --is-ancestor "$PREDATA_LOCK" HEAD
git merge-base --is-ancestor "$R2D_POSTDATA_LOCK" HEAD
echo "STABLE_AEST_GROWTH_WEYL_MEMORY_R2E_SCIENCE_LOCK_PASS predata=$PREDATA_LOCK r2d_postdata=$R2D_POSTDATA_LOCK"

python - <<'PY'
import json
from pathlib import Path
checks=[
 ('results/stable_aest_growth_weyl_memory_r2d_full_history.json','STABLE_AEST_GROWTH_WEYL_MEMORY_R2D_NON_HISTORY_NORMALIZATION_MISMATCH_CERTIFIED'),
 ('results/stable_aest_growth_weyl_memory_r2c_normalization.json','STABLE_AEST_GROWTH_WEYL_MEMORY_R2C_GLOBAL_NORMALIZATION_MISMATCH_CERTIFIED'),
 ('results/stable_aest_growth_weyl_memory_r2b_variational.json','STABLE_AEST_GROWTH_WEYL_MEMORY_R2B_COMMON_MODE_BOUND_CERTIFIED'),
 ('results/stable_aest_finite_memory_r1c.json','STABLE_AEST_FINITE_MEMORY_R1C_LONG_RELAXATION_CERTIFIED'),
 ('results/fullj_aest_stable_chi_precision_floor.json','FULLJ_AEST_STABLE_CHI_PRECISION_FLOOR_CERTIFIED')]
for p,c in checks:
    got=json.loads(Path(p).read_text())['classification']
    assert got==c,(p,got,c)
print('STABLE_AEST_GROWTH_WEYL_MEMORY_R2E_PARENT_PASS')
PY

# Lock exact reused full-history force-table provenance without copying them into the bundle.
MANIFEST='results/stable_aest_growth_weyl_memory_r2e_force_manifest.txt'
: > "$MANIFEST"
for f in \
 results/stable_aest_growth_weyl_memory_r2d_work/rhs_force_0p09875.dat \
 results/stable_aest_growth_weyl_memory_r2d_work/rhs_force_0p16125.dat \
 results/stable_aest_growth_weyl_memory_r2d_work/rhs_force_0p19500.dat; do
  printf '%s bytes=%s lines=%s sha256=' "$f" "$(stat -c%s "$f")" "$(wc -l < "$f")" >> "$MANIFEST"
  sha256sum "$f" | awk '{print $1}' >> "$MANIFEST"
done
echo STABLE_AEST_GROWTH_WEYL_MEMORY_R2E_FORCE_MANIFEST_PASS
cat "$MANIFEST"

source results/nl1c6d2n_corrected_class_densek64_env.sh
OLD_ROOT="$NL1C6D2N_CLASS_ROOT"
EXPECTED_CLASS_HEAD='e85808324f51fc694d12e3ed7439552a3c3f9540'
EXPECTED_MEMORY_SHA='4d5ab5dc7066d4880f06fcfc731d6534ed0ff992e3cc15fb473dddccb25a594f'
[[ "$(git -C "$OLD_ROOT" rev-parse HEAD)" == "$EXPECTED_CLASS_HEAD" ]]
[[ "$(sha256sum "$OLD_ROOT/source/aest_memory.c" | awk '{print $1}')" == "$EXPECTED_MEMORY_SHA" ]]
echo "STABLE_AEST_GROWTH_WEYL_MEMORY_R2E_OLD_PROVENANCE_PASS head=$EXPECTED_CLASS_HEAD"

STABLE_ROOT="$ROOT/.local/class_corrected_e8580832_densek64_stablechi"
if [[ ! -d "$STABLE_ROOT/.git" ]] || ! grep -q 'FULLJ_AEST_STABLE_CHI_RESIDUAL_V1' "$STABLE_ROOT/source/perturbations.c"; then
  rm -rf "$STABLE_ROOT"; cp -a "$OLD_ROOT" "$STABLE_ROOT"
  python fullj_weyl/apply_aest_stable_chi_residual_patch.py "$STABLE_ROOT"
fi

R2E_ROOT="$ROOT/.local/class_corrected_e8580832_densek64_stablechi_r2evar"
R2E_PYTARGET="$ROOT/.local/classy_corrected_e8580832_densek64_stablechi_r2evar"
rm -rf "$R2E_ROOT" "$R2E_PYTARGET"
cp -a "$STABLE_ROOT" "$R2E_ROOT"
python fullj_weyl/apply_stable_aest_r2b_variational_patch.py "$R2E_ROOT"
python fullj_weyl/apply_stable_aest_r2d_full_history_patch.py "$R2E_ROOT"
# The historical chain above intentionally reproduces the completed double-hook source;
# R2e then applies exactly the preregistered diagnostic correction.
python fullj_weyl/apply_stable_aest_r2e_single_hook_patch.py "$R2E_ROOT"

HOOK='dy[pv->index_pt_E_aest] += aest_tangent_external_force(k,tau);'
[[ "$(grep -Fc "$HOOK" "$R2E_ROOT/source/perturbations.c")" == '1' ]]
grep -q 'FULLJ_STABLE_AEST_R2E_SINGLE_HOOK_V1' "$R2E_ROOT/source/perturbations.c"
[[ "$(grep -Fc 'Bchi_aest *= pba->aest_eta;' "$R2E_ROOT/source/perturbations.c")" == '1' ]]
[[ "$(grep -Fc 'E_rhs_aest -= 0.5*Q_aest*Bchi_aest;' "$R2E_ROOT/source/perturbations.c")" == '1' ]]
echo STABLE_AEST_GROWTH_WEYL_MEMORY_R2E_SINGLE_HOOK_SOURCE_PASS

rm -rf "$R2E_ROOT/build" "$R2E_ROOT/python/build" "$R2E_ROOT/python/classy.egg-info" 2>/dev/null || true
mkdir -p "$R2E_PYTARGET"
python -m pip install --no-deps --no-build-isolation --target "$R2E_PYTARGET" "$R2E_ROOT"

export AEST_STABLE_R2E_CLASS_ROOT="$R2E_ROOT"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
unset AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE AEST_R2D_TRACE_FILE AEST_R2D_TRACE_KH AEST_R2D_TRACE_ALL_K AEST_TANGENT_ALLOW_K_MISS || true

JSON='results/stable_aest_growth_weyl_memory_r2e_single_hook.json'
NPZ='results/stable_aest_growth_weyl_memory_r2e_single_hook.npz'
LOG='results/stable_aest_growth_weyl_memory_r2e_single_hook.log'
ZIP='results/stable_aest_growth_weyl_memory_r2e_single_hook_bundle.zip'
WORK='results/stable_aest_growth_weyl_memory_r2e_work'
rm -f "$JSON" "$NPZ" "$LOG" "$ZIP"; rm -rf "$WORK"

set +e
PYTHONPATH="$R2E_PYTARGET" python -u -m fullj_weyl.stable_aest_growth_weyl_memory_r2e_single_hook \
  --json-out "$JSON" --npz-out "$NPZ" --workdir "$WORK" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

python - "$ZIP" "$LOG" "$JSON" "$NPZ" "$MANIFEST" "$WORK" <<'PY'
from pathlib import Path
import sys,zipfile
zp=Path(sys.argv[1]); work=Path(sys.argv[6])
paths=[Path(x) for x in sys.argv[2:6]]+[
 Path('docs/stable_aest_growth_weyl_memory_r2e_single_hook_predata.md'),
 Path('docs/stable_aest_growth_weyl_memory_r2d_full_history_postdata.md'),
 Path('fullj_weyl/stable_aest_growth_weyl_memory_r2e_single_hook.py'),
 Path('fullj_weyl/run_local_stable_aest_growth_weyl_memory_r2e_single_hook.sh'),
 Path('fullj_weyl/apply_stable_aest_r2e_single_hook_patch.py'),
 Path('fullj_weyl/apply_stable_aest_r2d_full_history_patch.py'),
 Path('fullj_weyl/apply_stable_aest_r2b_variational_patch.py'),
 Path('results/stable_aest_growth_weyl_memory_r2d_full_history.json'),
 Path('results/stable_aest_growth_weyl_memory_r2d_full_history.npz'),
 Path('results/stable_aest_growth_weyl_memory_r2.npz')]
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED) as zf:
    seen=set()
    for p in paths:
        if p.exists() and p not in seen:
            zf.write(p,arcname=str(p)); seen.add(p)
    if work.exists():
        for p in sorted(work.rglob('*')):
            if p.is_file(): zf.write(p,arcname=str(p))
print('STABLE_AEST_GROWTH_WEYL_MEMORY_R2E_BUNDLE='+str(zp))
PY

echo "STABLE_AEST_GROWTH_WEYL_MEMORY_R2E_EXIT=$code"
echo "STABLE_AEST_GROWTH_WEYL_MEMORY_R2E_LOG=$LOG"
echo "STABLE_AEST_GROWTH_WEYL_MEMORY_R2E_JSON=$JSON"
echo "STABLE_AEST_GROWTH_WEYL_MEMORY_R2E_NPZ=$NPZ"
echo "STABLE_AEST_GROWTH_WEYL_MEMORY_R2E_ZIP=$ZIP"
exit "$code"
