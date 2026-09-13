#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

BASE_PY=""
if command -v python3 >/dev/null 2>&1; then BASE_PY="$(command -v python3)";
elif command -v python >/dev/null 2>&1; then BASE_PY="$(command -v python)";
else echo "FULLJ_AEST_STABLE_CHI_FLOOR: python missing" >&2; exit 2; fi

VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then
  "$BASE_PY" -m venv "$VENV" || { echo "FULLJ_AEST_STABLE_CHI_FLOOR: install python3-venv" >&2; exit 2; }
fi
export PATH="$VENV/bin:$PATH"
python -m pip install --upgrade pip setuptools wheel >/dev/null
python -m pip install numpy scipy cython >/dev/null
python -m py_compile \
  fullj_weyl/aest_stable_chi_precision_floor.py \
  fullj_weyl/aest_stable_chi_precision_convergence.py \
  fullj_weyl/apply_aest_stable_chi_residual_patch.py

echo "FULLJ_AEST_STABLE_CHI_FLOOR_IMPORT_PASS"

for f in \
  docs/fullj_aest_stable_chi_precision_floor_predata.md \
  results/fullj_aest_stable_chi_precision_convergence.json \
  results/fullj_aest_stable_chi_precision_stable.npz \
  results/nl1c6d2n_corrected_class_densek64_env.sh; do
  [[ -f "$f" ]] || { echo "FULLJ_AEST_STABLE_CHI_FLOOR: missing $f" >&2; exit 3; }
done

PREDATA_LOCK="4b7acaf908e91a83b2fa69260ae3dbd13ad2226b"
git merge-base --is-ancestor "$PREDATA_LOCK" HEAD
echo "FULLJ_AEST_STABLE_CHI_FLOOR_SCIENCE_LOCK_PASS predata=$PREDATA_LOCK"

python - <<'PY'
import json
from pathlib import Path
j=json.loads(Path('results/fullj_aest_stable_chi_precision_convergence.json').read_text())
assert j['classification']=='FULLJ_AEST_STABLE_CHI_NOT_PRECISION_CONVERGED',j['classification']
assert j['diagnostic_complete'] is True
print('FULLJ_AEST_STABLE_CHI_FLOOR_PARENT_PASS')
PY

# Frozen corrected CLASS provenance and stable residual copy.
source results/nl1c6d2n_corrected_class_densek64_env.sh
OLD_ROOT="$NL1C6D2N_CLASS_ROOT"
EXPECTED_CLASS_HEAD="e85808324f51fc694d12e3ed7439552a3c3f9540"
EXPECTED_MEMORY_SHA="4d5ab5dc7066d4880f06fcfc731d6534ed0ff992e3cc15fb473dddccb25a594f"
[[ "$(git -C "$OLD_ROOT" rev-parse HEAD)" == "$EXPECTED_CLASS_HEAD" ]]
[[ "$(sha256sum "$OLD_ROOT/source/aest_memory.c" | awk '{print $1}')" == "$EXPECTED_MEMORY_SHA" ]]
echo "FULLJ_AEST_STABLE_CHI_FLOOR_OLD_PROVENANCE_PASS head=$EXPECTED_CLASS_HEAD"

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
  echo "FULLJ_AEST_STABLE_CHI_FLOOR: preparing stable-residual CLASS copy..."
  rm -rf "$STABLE_ROOT" "$STABLE_PYTARGET"
  cp -a "$OLD_ROOT" "$STABLE_ROOT"
  python fullj_weyl/apply_aest_stable_chi_residual_patch.py "$STABLE_ROOT"
  rm -rf "$STABLE_ROOT/build" "$STABLE_ROOT/python/build" "$STABLE_ROOT/python/classy.egg-info" 2>/dev/null || true
  mkdir -p "$STABLE_PYTARGET"
  python -m pip install --no-deps --no-build-isolation --target "$STABLE_PYTARGET" "$STABLE_ROOT"
else
  echo "FULLJ_AEST_STABLE_CHI_FLOOR: reusing stable-residual CLASS copy"
fi

grep -q 'FULLJ_AEST_STABLE_CHI_RESIDUAL_V1' "$STABLE_ROOT/source/perturbations.c"
grep -q '3\.\*cad2_aest\*a_prime_over_a\*(s_aest-alpha_aest)' "$STABLE_ROOT/source/perturbations.c"
[[ "$(sha256sum "$STABLE_ROOT/source/aest_memory.c" | awk '{print $1}')" == "$EXPECTED_MEMORY_SHA" ]]
echo "FULLJ_AEST_STABLE_CHI_FLOOR_STABLE_SOURCE_PASS"

export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1
unset AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE AEST_OFFLINE_TRACE_FILE AEST_TANGENT_ALLOW_K_MISS AEST_ERHS_TRACE_FILE AEST_ERHS_TRACE_K || true

export AEST_STABLE_CLASS_ROOT="$STABLE_ROOT"
JSON="results/fullj_aest_stable_chi_precision_floor.json"
NPZ="results/fullj_aest_stable_chi_precision_floor.npz"
LOG="results/fullj_aest_stable_chi_precision_floor.log"
ZIP="results/fullj_aest_stable_chi_precision_floor_bundle.zip"
rm -f "$JSON" "$NPZ" "$LOG" "$ZIP"

set +e
PYTHONPATH="$STABLE_PYTARGET" python -u -m fullj_weyl.aest_stable_chi_precision_floor \
  --json-out "$JSON" --npz-out "$NPZ" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

python - "$ZIP" "$LOG" "$JSON" "$NPZ" <<'PY'
from pathlib import Path
import sys,zipfile
zp=Path(sys.argv[1])
paths=[Path(x) for x in sys.argv[2:]]+[
 Path('docs/fullj_aest_stable_chi_precision_floor_predata.md'),
 Path('fullj_weyl/aest_stable_chi_precision_floor.py'),
 Path('fullj_weyl/aest_stable_chi_precision_convergence.py'),
 Path('fullj_weyl/apply_aest_stable_chi_residual_patch.py'),
 Path('fullj_weyl/run_local_aest_stable_chi_precision_floor.sh'),
 Path('results/fullj_aest_stable_chi_precision_convergence.json'),
 Path('results/fullj_aest_stable_chi_precision_stable.npz'),
 Path('results/nl1c6d2n_corrected_class_densek64_env.sh'),
]
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED) as zf:
  seen=set()
  for p in paths:
    if p.exists() and p not in seen:
      zf.write(p,arcname=str(p)); seen.add(p)
print('FULLJ_AEST_STABLE_CHI_FLOOR_BUNDLE='+str(zp))
PY

echo "FULLJ_AEST_STABLE_CHI_FLOOR_EXIT=$code"
echo "FULLJ_AEST_STABLE_CHI_FLOOR_LOG=$LOG"
echo "FULLJ_AEST_STABLE_CHI_FLOOR_JSON=$JSON"
echo "FULLJ_AEST_STABLE_CHI_FLOOR_NPZ=$NPZ"
echo "FULLJ_AEST_STABLE_CHI_FLOOR_ZIP=$ZIP"
exit "$code"
