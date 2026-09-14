#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

BASE_PY="$(command -v python3 || command -v python)"
[[ -n "$BASE_PY" ]] || { echo 'STABLE_AEST_GROWTH_WEYL_MEMORY_R2: python missing' >&2; exit 2; }
VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then "$BASE_PY" -m venv "$VENV"; fi
export PATH="$VENV/bin:$PATH"
python -m pip install --upgrade pip setuptools wheel >/dev/null
python -m pip install numpy scipy cython >/dev/null
python -m py_compile fullj_weyl/stable_aest_growth_weyl_memory_r2.py fullj_weyl/apply_aest_stable_chi_residual_patch.py
echo STABLE_AEST_GROWTH_WEYL_MEMORY_R2_IMPORT_PASS

for f in \
  docs/stable_aest_growth_weyl_memory_r2_predata.md \
  docs/stable_aest_finite_memory_r1c_postdata.md \
  docs/project_history_checkpoint_2026-09-14.md \
  results/stable_aest_finite_memory_r1c.json \
  results/fullj_aest_stable_chi_precision_floor.json \
  results/nl1c6d2n_corrected_class_densek64_env.sh; do
  [[ -f "$f" ]] || { echo "STABLE_AEST_GROWTH_WEYL_MEMORY_R2: missing $f" >&2; exit 3; }
done

PREDATA_LOCK='5fdb18b7fb40898ad6963fe4d4e5874c39bc0617'
R1C_POSTDATA_LOCK='62d7649ebb5dd45a00be3272bf2ee8d5ab30a49a'
HISTORY_LOCK='3fcbb4f610844f20d3e45045e829a9a8a69be87c'
git merge-base --is-ancestor "$PREDATA_LOCK" HEAD
git merge-base --is-ancestor "$R1C_POSTDATA_LOCK" HEAD
git merge-base --is-ancestor "$HISTORY_LOCK" HEAD
echo "STABLE_AEST_GROWTH_WEYL_MEMORY_R2_SCIENCE_LOCK_PASS predata=$PREDATA_LOCK r1c_postdata=$R1C_POSTDATA_LOCK history=$HISTORY_LOCK"

python - <<'PY'
import json
from pathlib import Path
r=json.loads(Path('results/stable_aest_finite_memory_r1c.json').read_text())
h=json.loads(Path('results/fullj_aest_stable_chi_precision_floor.json').read_text())
assert r['classification']=='STABLE_AEST_FINITE_MEMORY_R1C_LONG_RELAXATION_CERTIFIED',r['classification']
assert r['interpretation']['long_relaxation_growth_Weyl_followup_licensed'] is True
assert h['classification']=='FULLJ_AEST_STABLE_CHI_PRECISION_FLOOR_CERTIFIED',h['classification']
print('STABLE_AEST_GROWTH_WEYL_MEMORY_R2_PARENT_PASS')
PY

source results/nl1c6d2n_corrected_class_densek64_env.sh
OLD_ROOT="$NL1C6D2N_CLASS_ROOT"
EXPECTED_CLASS_HEAD='e85808324f51fc694d12e3ed7439552a3c3f9540'
EXPECTED_MEMORY_SHA='4d5ab5dc7066d4880f06fcfc731d6534ed0ff992e3cc15fb473dddccb25a594f'
[[ "$(git -C "$OLD_ROOT" rev-parse HEAD)" == "$EXPECTED_CLASS_HEAD" ]]
[[ "$(sha256sum "$OLD_ROOT/source/aest_memory.c" | awk '{print $1}')" == "$EXPECTED_MEMORY_SHA" ]]
echo "STABLE_AEST_GROWTH_WEYL_MEMORY_R2_OLD_PROVENANCE_PASS head=$EXPECTED_CLASS_HEAD"

STABLE_ROOT="$ROOT/.local/class_corrected_e8580832_densek64_stablechi"
STABLE_PYTARGET="$ROOT/.local/classy_corrected_e8580832_densek64_stablechi"
need_build=1
if [[ -d "$STABLE_ROOT/.git" && -f "$STABLE_ROOT/source/perturbations.c" && -f "$STABLE_PYTARGET/classy/__init__.py" ]] \
  && grep -q 'FULLJ_AEST_STABLE_CHI_RESIDUAL_V1' "$STABLE_ROOT/source/perturbations.c"; then
  if [[ "$(git -C "$STABLE_ROOT" rev-parse HEAD)" == "$EXPECTED_CLASS_HEAD" \
    && "$(sha256sum "$STABLE_ROOT/source/aest_memory.c" | awk '{print $1}')" == "$EXPECTED_MEMORY_SHA" ]]; then
    need_build=0
  fi
fi

if [[ "$need_build" -eq 1 ]]; then
  echo 'STABLE_AEST_GROWTH_WEYL_MEMORY_R2: preparing stable-residual CLASS copy...'
  rm -rf "$STABLE_ROOT" "$STABLE_PYTARGET"
  cp -a "$OLD_ROOT" "$STABLE_ROOT"
  python fullj_weyl/apply_aest_stable_chi_residual_patch.py "$STABLE_ROOT"
  rm -rf "$STABLE_ROOT/build" "$STABLE_ROOT/python/build" "$STABLE_ROOT/python/classy.egg-info" 2>/dev/null || true
  mkdir -p "$STABLE_PYTARGET"
  python -m pip install --no-deps --no-build-isolation --target "$STABLE_PYTARGET" "$STABLE_ROOT"
else
  echo 'STABLE_AEST_GROWTH_WEYL_MEMORY_R2: reusing stable-residual CLASS copy'
fi

grep -q 'FULLJ_AEST_STABLE_CHI_RESIDUAL_V1' "$STABLE_ROOT/source/perturbations.c"
grep -q 'double chi_aest = Q_aest\*s_aest;' "$STABLE_ROOT/source/perturbations.c"
grep -q 'E_rhs_aest -= 0.5\*Q_aest\*Bchi_aest' "$STABLE_ROOT/source/perturbations.c"
grep -q 'if (order == 20)' "$STABLE_ROOT/source/aest_memory.c"
[[ "$(sha256sum "$STABLE_ROOT/source/aest_memory.c" | awk '{print $1}')" == "$EXPECTED_MEMORY_SHA" ]]
echo STABLE_AEST_GROWTH_WEYL_MEMORY_R2_SOURCE_PASS

export AEST_STABLE_CLASS_ROOT="$STABLE_ROOT"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
unset AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE AEST_OFFLINE_TRACE_FILE AEST_TANGENT_ALLOW_K_MISS AEST_ERHS_TRACE_FILE AEST_ERHS_TRACE_K || true

JSON='results/stable_aest_growth_weyl_memory_r2.json'
NPZ='results/stable_aest_growth_weyl_memory_r2.npz'
LOG='results/stable_aest_growth_weyl_memory_r2.log'
ZIP='results/stable_aest_growth_weyl_memory_r2_bundle.zip'
rm -f "$JSON" "$NPZ" "$LOG" "$ZIP"

set +e
PYTHONPATH="$STABLE_PYTARGET" python -u -m fullj_weyl.stable_aest_growth_weyl_memory_r2 \
  --json-out "$JSON" --npz-out "$NPZ" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

python - "$ZIP" "$LOG" "$JSON" "$NPZ" <<'PY'
from pathlib import Path
import sys,zipfile
zp=Path(sys.argv[1])
paths=[Path(x) for x in sys.argv[2:]]+[
 Path('docs/stable_aest_growth_weyl_memory_r2_predata.md'),
 Path('docs/stable_aest_finite_memory_r1c_postdata.md'),
 Path('docs/project_history_checkpoint_2026-09-14.md'),
 Path('fullj_weyl/stable_aest_growth_weyl_memory_r2.py'),
 Path('fullj_weyl/run_local_stable_aest_growth_weyl_memory_r2.sh'),
 Path('fullj_weyl/apply_aest_stable_chi_residual_patch.py'),
 Path('results/stable_aest_finite_memory_r1c.json'),
 Path('results/fullj_aest_stable_chi_precision_floor.json'),
 Path('results/nl1c6d2n_corrected_class_densek64_env.sh'),
]
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED) as zf:
  seen=set()
  for p in paths:
    if p.exists() and p not in seen:
      zf.write(p,arcname=str(p)); seen.add(p)
print('STABLE_AEST_GROWTH_WEYL_MEMORY_R2_BUNDLE='+str(zp))
PY

echo "STABLE_AEST_GROWTH_WEYL_MEMORY_R2_EXIT=$code"
echo "STABLE_AEST_GROWTH_WEYL_MEMORY_R2_LOG=$LOG"
echo "STABLE_AEST_GROWTH_WEYL_MEMORY_R2_JSON=$JSON"
echo "STABLE_AEST_GROWTH_WEYL_MEMORY_R2_NPZ=$NPZ"
echo "STABLE_AEST_GROWTH_WEYL_MEMORY_R2_ZIP=$ZIP"
exit "$code"
