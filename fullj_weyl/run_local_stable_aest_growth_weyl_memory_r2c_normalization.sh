#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"; mkdir -p results .local

BASE_PY="$(command -v python3 || command -v python)"
[[ -n "$BASE_PY" ]] || { echo 'STABLE_AEST_GROWTH_WEYL_MEMORY_R2C: python missing' >&2; exit 2; }
VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then "$BASE_PY" -m venv "$VENV"; fi
export PATH="$VENV/bin:$PATH"
python -m pip install --upgrade pip setuptools wheel >/dev/null
python -m pip install numpy scipy cython >/dev/null
python -m py_compile \
  fullj_weyl/stable_aest_growth_weyl_memory_r2c_normalization.py \
  fullj_weyl/stable_aest_growth_weyl_memory_r2.py \
  fullj_weyl/apply_stable_aest_r2b_variational_patch.py \
  fullj_weyl/apply_aest_stable_chi_residual_patch.py \
  v019w/normalize_force_table.py
echo STABLE_AEST_GROWTH_WEYL_MEMORY_R2C_IMPORT_PASS

for f in \
 docs/stable_aest_growth_weyl_memory_r2c_normalization_predata.md \
 docs/stable_aest_growth_weyl_memory_r2b_variational_postdata.md \
 results/stable_aest_growth_weyl_memory_r2b_variational.json \
 results/stable_aest_growth_weyl_memory_r2.npz \
 results/stable_aest_finite_memory_r1c.json \
 results/fullj_aest_stable_chi_precision_floor.json \
 results/nl1c6d2n_corrected_class_densek64_env.sh; do
 [[ -f "$f" ]] || { echo "STABLE_AEST_GROWTH_WEYL_MEMORY_R2C: missing $f" >&2; exit 3; }
done

PREDATA_LOCK='6459fa6ceab26dfd56c4ba558613f3d1a4bd43c9'
R2B_POSTDATA_LOCK='35913eb794d7427431e5f5050f05a71ecfbccbbe'
git merge-base --is-ancestor "$PREDATA_LOCK" HEAD
git merge-base --is-ancestor "$R2B_POSTDATA_LOCK" HEAD
echo "STABLE_AEST_GROWTH_WEYL_MEMORY_R2C_SCIENCE_LOCK_PASS predata=$PREDATA_LOCK r2b_postdata=$R2B_POSTDATA_LOCK"

python - <<'PY'
import json
from pathlib import Path
r=json.loads(Path('results/stable_aest_growth_weyl_memory_r2b_variational.json').read_text())
r1=json.loads(Path('results/stable_aest_finite_memory_r1c.json').read_text())
h=json.loads(Path('results/fullj_aest_stable_chi_precision_floor.json').read_text())
assert r['classification']=='STABLE_AEST_GROWTH_WEYL_MEMORY_R2B_COMMON_MODE_BOUND_CERTIFIED',r['classification']
assert r1['classification']=='STABLE_AEST_FINITE_MEMORY_R1C_LONG_RELAXATION_CERTIFIED',r1['classification']
assert h['classification']=='FULLJ_AEST_STABLE_CHI_PRECISION_FLOOR_CERTIFIED',h['classification']
print('STABLE_AEST_GROWTH_WEYL_MEMORY_R2C_PARENT_PASS')
PY

source results/nl1c6d2n_corrected_class_densek64_env.sh
OLD_ROOT="$NL1C6D2N_CLASS_ROOT"
EXPECTED_CLASS_HEAD='e85808324f51fc694d12e3ed7439552a3c3f9540'
EXPECTED_MEMORY_SHA='4d5ab5dc7066d4880f06fcfc731d6534ed0ff992e3cc15fb473dddccb25a594f'
[[ "$(git -C "$OLD_ROOT" rev-parse HEAD)" == "$EXPECTED_CLASS_HEAD" ]]
[[ "$(sha256sum "$OLD_ROOT/source/aest_memory.c" | awk '{print $1}')" == "$EXPECTED_MEMORY_SHA" ]]
echo "STABLE_AEST_GROWTH_WEYL_MEMORY_R2C_OLD_PROVENANCE_PASS head=$EXPECTED_CLASS_HEAD"

STABLE_ROOT="$ROOT/.local/class_corrected_e8580832_densek64_stablechi"
if [[ ! -d "$STABLE_ROOT/.git" ]] || ! grep -q 'FULLJ_AEST_STABLE_CHI_RESIDUAL_V1' "$STABLE_ROOT/source/perturbations.c"; then
  rm -rf "$STABLE_ROOT"; cp -a "$OLD_ROOT" "$STABLE_ROOT"
  python fullj_weyl/apply_aest_stable_chi_residual_patch.py "$STABLE_ROOT"
fi
[[ "$(git -C "$STABLE_ROOT" rev-parse HEAD)" == "$EXPECTED_CLASS_HEAD" ]]
[[ "$(sha256sum "$STABLE_ROOT/source/aest_memory.c" | awk '{print $1}')" == "$EXPECTED_MEMORY_SHA" ]]

VAR_ROOT="$ROOT/.local/class_corrected_e8580832_densek64_stablechi_r2bvar"
VAR_PYTARGET="$ROOT/.local/classy_corrected_e8580832_densek64_stablechi_r2bvar"
reuse=0
if [[ -d "$VAR_ROOT/.git" && -f "$VAR_PYTARGET/classy/__init__.py" ]] \
   && grep -q 'FULLJ_STABLE_AEST_R2B_VARIATIONAL_V1' "$VAR_ROOT/source/perturbations.c" \
   && grep -q 'aest_tangent_external_force' "$VAR_ROOT/source/aest_memory.c"; then
  reuse=1
fi
if [[ "$reuse" -eq 1 ]]; then
  echo STABLE_AEST_GROWTH_WEYL_MEMORY_R2C_VARIATIONAL_BUILD_REUSE_PASS
else
  rm -rf "$VAR_ROOT" "$VAR_PYTARGET"; cp -a "$STABLE_ROOT" "$VAR_ROOT"
  python fullj_weyl/apply_stable_aest_r2b_variational_patch.py "$VAR_ROOT"
  rm -rf "$VAR_ROOT/build" "$VAR_ROOT/python/build" "$VAR_ROOT/python/classy.egg-info" 2>/dev/null || true
  mkdir -p "$VAR_PYTARGET"
  python -m pip install --no-deps --no-build-isolation --target "$VAR_PYTARGET" "$VAR_ROOT"
fi

grep -q 'FULLJ_AEST_STABLE_CHI_RESIDUAL_V1' "$VAR_ROOT/source/perturbations.c"
grep -q 'FULLJ_STABLE_AEST_R2B_VARIATIONAL_V1' "$VAR_ROOT/source/perturbations.c"
grep -q 'double s_aest=y\[ppw->pv->index_pt_s_aest\];' "$VAR_ROOT/source/perturbations.c"
grep -q 'aest_tangent_trace_force' "$VAR_ROOT/source/perturbations.c"
grep -q 'aest_tangent_external_force' "$VAR_ROOT/source/perturbations.c"
grep -q 'E_rhs_aest -= 0.5\*Q_aest\*Bchi_aest' "$VAR_ROOT/source/perturbations.c"
echo STABLE_AEST_GROWTH_WEYL_MEMORY_R2C_SOURCE_PASS

export AEST_STABLE_VAR_CLASS_ROOT="$VAR_ROOT"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
unset AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE AEST_OFFLINE_TRACE_FILE AEST_TANGENT_ALLOW_K_MISS AEST_ERHS_TRACE_FILE AEST_ERHS_TRACE_K || true

JSON='results/stable_aest_growth_weyl_memory_r2c_normalization.json'
NPZ='results/stable_aest_growth_weyl_memory_r2c_normalization.npz'
LOG='results/stable_aest_growth_weyl_memory_r2c_normalization.log'
ZIP='results/stable_aest_growth_weyl_memory_r2c_normalization_bundle.zip'
WORK='results/stable_aest_growth_weyl_memory_r2c_work'
rm -f "$JSON" "$NPZ" "$LOG" "$ZIP"; rm -rf "$WORK"

set +e
PYTHONPATH="$VAR_PYTARGET" python -u -m fullj_weyl.stable_aest_growth_weyl_memory_r2c_normalization \
 --json-out "$JSON" --npz-out "$NPZ" --workdir "$WORK" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

python - "$ZIP" "$LOG" "$JSON" "$NPZ" "$WORK" <<'PY'
from pathlib import Path
import sys,zipfile
zp=Path(sys.argv[1]); work=Path(sys.argv[5])
paths=[Path(x) for x in sys.argv[2:5]]+[
 Path('docs/stable_aest_growth_weyl_memory_r2c_normalization_predata.md'),
 Path('docs/stable_aest_growth_weyl_memory_r2b_variational_postdata.md'),
 Path('fullj_weyl/stable_aest_growth_weyl_memory_r2c_normalization.py'),
 Path('fullj_weyl/run_local_stable_aest_growth_weyl_memory_r2c_normalization.sh'),
 Path('fullj_weyl/apply_stable_aest_r2b_variational_patch.py'),
 Path('v019w/normalize_force_table.py'),
 Path('results/stable_aest_growth_weyl_memory_r2b_variational.json'),
 Path('results/stable_aest_growth_weyl_memory_r2.npz'),
 Path('results/stable_aest_finite_memory_r1c.json'),Path('results/fullj_aest_stable_chi_precision_floor.json'),
 Path('results/nl1c6d2n_corrected_class_densek64_env.sh')]
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED) as zf:
 seen=set()
 for p in paths:
  if p.exists() and p not in seen: zf.write(p,arcname=str(p)); seen.add(p)
 if work.exists():
  for p in sorted(work.rglob('*')):
   if p.is_file(): zf.write(p,arcname=str(p))
print('STABLE_AEST_GROWTH_WEYL_MEMORY_R2C_BUNDLE='+str(zp))
PY

echo "STABLE_AEST_GROWTH_WEYL_MEMORY_R2C_EXIT=$code"
echo "STABLE_AEST_GROWTH_WEYL_MEMORY_R2C_LOG=$LOG"
echo "STABLE_AEST_GROWTH_WEYL_MEMORY_R2C_JSON=$JSON"
echo "STABLE_AEST_GROWTH_WEYL_MEMORY_R2C_NPZ=$NPZ"
echo "STABLE_AEST_GROWTH_WEYL_MEMORY_R2C_ZIP=$ZIP"
exit "$code"
