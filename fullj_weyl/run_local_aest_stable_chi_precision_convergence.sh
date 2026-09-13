#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

BASE_PY=""
if command -v python3 >/dev/null 2>&1; then BASE_PY="$(command -v python3)";
elif command -v python >/dev/null 2>&1; then BASE_PY="$(command -v python)";
else echo "FULLJ_AEST_STABLE_CHI_PRECISION: python missing" >&2; exit 2; fi

VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then
  "$BASE_PY" -m venv "$VENV" || { echo "FULLJ_AEST_STABLE_CHI_PRECISION: install python3-venv" >&2; exit 2; }
fi
export PATH="$VENV/bin:$PATH"
python -m pip install --upgrade pip setuptools wheel >/dev/null
python -m pip install numpy scipy cython >/dev/null
python -m py_compile fullj_weyl/aest_stable_chi_precision_convergence.py fullj_weyl/apply_aest_stable_chi_residual_patch.py

echo "FULLJ_AEST_STABLE_CHI_PRECISION_IMPORT_PASS"

for f in \
  docs/fullj_aest_stable_chi_precision_convergence_predata.md \
  docs/fullj_aest_stable_chi_residual_predata.md \
  results/fullj_aest_stable_chi_residual.json \
  results/nl1c6d2n_corrected_class_densek64_env.sh; do
  [[ -f "$f" ]] || { echo "FULLJ_AEST_STABLE_CHI_PRECISION: missing $f" >&2; exit 3; }
done

PREDATA_LOCK="167a556247e334a4a3652d61b365a4d8af3b523f"
git merge-base --is-ancestor "$PREDATA_LOCK" HEAD
echo "FULLJ_AEST_STABLE_CHI_PRECISION_SCIENCE_LOCK_PASS predata=$PREDATA_LOCK"

python - <<'PY'
import json
from pathlib import Path
j=json.loads(Path('results/fullj_aest_stable_chi_residual.json').read_text())
assert j['classification']=='FULLJ_AEST_STABLE_CHI_REFERENCE_MISMATCH',j['classification']
assert j['diagnostic_complete'] is True
print('FULLJ_AEST_STABLE_CHI_PRECISION_PARENT_PASS')
PY

# Frozen unmodified corrected CLASS runtime.
source results/nl1c6d2n_corrected_class_densek64_env.sh
OLD_ROOT="$NL1C6D2N_CLASS_ROOT"
OLD_PYTARGET="$NL1C6D2N_PYTARGET"
EXPECTED_CLASS_HEAD="e85808324f51fc694d12e3ed7439552a3c3f9540"
EXPECTED_MEMORY_SHA="4d5ab5dc7066d4880f06fcfc731d6534ed0ff992e3cc15fb473dddccb25a594f"
[[ "$(git -C "$OLD_ROOT" rev-parse HEAD)" == "$EXPECTED_CLASS_HEAD" ]]
[[ "$(sha256sum "$OLD_ROOT/source/aest_memory.c" | awk '{print $1}')" == "$EXPECTED_MEMORY_SHA" ]]
echo "FULLJ_AEST_STABLE_CHI_PRECISION_OLD_PROVENANCE_PASS head=$EXPECTED_CLASS_HEAD"

# Stable residual copy. Rebuild only when absent or not the locked V1 source intervention.
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
  echo "FULLJ_AEST_STABLE_CHI_PRECISION: preparing stable-residual CLASS copy..."
  rm -rf "$STABLE_ROOT" "$STABLE_PYTARGET"
  cp -a "$OLD_ROOT" "$STABLE_ROOT"
  python fullj_weyl/apply_aest_stable_chi_residual_patch.py "$STABLE_ROOT"
  rm -rf "$STABLE_ROOT/build" "$STABLE_ROOT/python/build" "$STABLE_ROOT/python/classy.egg-info" 2>/dev/null || true
  mkdir -p "$STABLE_PYTARGET"
  python -m pip install --no-deps --no-build-isolation --target "$STABLE_PYTARGET" "$STABLE_ROOT"
else
  echo "FULLJ_AEST_STABLE_CHI_PRECISION: reusing stable-residual CLASS copy"
fi

grep -q 'FULLJ_AEST_STABLE_CHI_RESIDUAL_V1' "$STABLE_ROOT/source/perturbations.c"
grep -q '3\.\*cad2_aest\*a_prime_over_a\*(s_aest-alpha_aest)' "$STABLE_ROOT/source/perturbations.c"
[[ "$(sha256sum "$STABLE_ROOT/source/aest_memory.c" | awk '{print $1}')" == "$EXPECTED_MEMORY_SHA" ]]
echo "FULLJ_AEST_STABLE_CHI_PRECISION_STABLE_SOURCE_PASS"

export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1
unset AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE AEST_OFFLINE_TRACE_FILE AEST_TANGENT_ALLOW_K_MISS AEST_ERHS_TRACE_FILE AEST_ERHS_TRACE_K || true

OLD_NPZ="results/fullj_aest_stable_chi_precision_old.npz"
OLD_JSON="results/fullj_aest_stable_chi_precision_old.json"
STABLE_NPZ="results/fullj_aest_stable_chi_precision_stable.npz"
STABLE_JSON="results/fullj_aest_stable_chi_precision_stable.json"
JSON="results/fullj_aest_stable_chi_precision_convergence.json"
NPZ="results/fullj_aest_stable_chi_precision_convergence.npz"
LOG="results/fullj_aest_stable_chi_precision_convergence.log"
ZIP="results/fullj_aest_stable_chi_precision_convergence_bundle.zip"
rm -f "$OLD_NPZ" "$OLD_JSON" "$STABLE_NPZ" "$STABLE_JSON" "$JSON" "$NPZ" "$LOG" "$ZIP"

set +e
{
  echo "FULLJ_AEST_STABLE_CHI_PRECISION_START"
  echo "FULLJ_AEST_STABLE_CHI_PRECISION_COLLECT_OLD"
  PYTHONPATH="$OLD_PYTARGET" python -u -m fullj_weyl.aest_stable_chi_precision_convergence collect \
    --mode old --npz-out "$OLD_NPZ" --json-out "$OLD_JSON" || exit $?

  echo "FULLJ_AEST_STABLE_CHI_PRECISION_COLLECT_STABLE"
  PYTHONPATH="$STABLE_PYTARGET" python -u -m fullj_weyl.aest_stable_chi_precision_convergence collect \
    --mode stable --npz-out "$STABLE_NPZ" --json-out "$STABLE_JSON" || exit $?

  echo "FULLJ_AEST_STABLE_CHI_PRECISION_AGGREGATE"
  PYTHONPATH="$OLD_PYTARGET" python -u -m fullj_weyl.aest_stable_chi_precision_convergence aggregate \
    --old-npz "$OLD_NPZ" --stable-npz "$STABLE_NPZ" --stable-json "$STABLE_JSON" \
    --json-out "$JSON" --npz-out "$NPZ"
} 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

python - "$ZIP" "$LOG" "$JSON" "$NPZ" "$OLD_JSON" "$OLD_NPZ" "$STABLE_JSON" "$STABLE_NPZ" <<'PY'
from pathlib import Path
import sys,zipfile
zp=Path(sys.argv[1]); paths=[Path(x) for x in sys.argv[2:]]+[
 Path('docs/fullj_aest_stable_chi_precision_convergence_predata.md'),
 Path('docs/fullj_aest_stable_chi_residual_predata.md'),
 Path('fullj_weyl/aest_stable_chi_precision_convergence.py'),
 Path('fullj_weyl/apply_aest_stable_chi_residual_patch.py'),
 Path('fullj_weyl/run_local_aest_stable_chi_precision_convergence.sh'),
 Path('results/fullj_aest_stable_chi_residual.json'),
 Path('results/nl1c6d2n_corrected_class_densek64_env.sh'),
]
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED) as zf:
  seen=set()
  for p in paths:
    if p.exists() and p not in seen:
      zf.write(p,arcname=str(p)); seen.add(p)
print('FULLJ_AEST_STABLE_CHI_PRECISION_BUNDLE='+str(zp))
PY

echo "FULLJ_AEST_STABLE_CHI_PRECISION_EXIT=$code"
echo "FULLJ_AEST_STABLE_CHI_PRECISION_LOG=$LOG"
echo "FULLJ_AEST_STABLE_CHI_PRECISION_JSON=$JSON"
echo "FULLJ_AEST_STABLE_CHI_PRECISION_NPZ=$NPZ"
echo "FULLJ_AEST_STABLE_CHI_PRECISION_ZIP=$ZIP"
exit "$code"
