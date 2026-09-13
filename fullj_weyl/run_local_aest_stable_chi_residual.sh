#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

BASE_PY=""
if command -v python3 >/dev/null 2>&1; then BASE_PY="$(command -v python3)";
elif command -v python >/dev/null 2>&1; then BASE_PY="$(command -v python)";
else echo "FULLJ_AEST_STABLE_CHI: python missing" >&2; exit 2; fi

VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then
  "$BASE_PY" -m venv "$VENV" || { echo "FULLJ_AEST_STABLE_CHI: install python3-venv" >&2; exit 2; }
fi
export PATH="$VENV/bin:$PATH"
python -m pip install --upgrade pip setuptools wheel >/dev/null
python -m pip install numpy scipy cython >/dev/null

python -m py_compile \
  fullj_weyl/apply_aest_stable_chi_residual_patch.py \
  fullj_weyl/aest_stable_chi_residual_intervention.py \
  fullj_weyl/aest_ulp_initial_amplitude_localization.py

echo "FULLJ_AEST_STABLE_CHI_IMPORT_PASS"

for f in \
  docs/fullj_aest_stable_chi_residual_predata.md \
  docs/fullj_aest_ulp_chi_cancellation_posthoc.md \
  results/fullj_aest_ulp_initial_amplitude_localization.json \
  results/fullj_aest_ulp_initial_amplitude_localization.npz \
  results/nl1c6d2n_corrected_class_densek64_env.sh; do
  [[ -f "$f" ]] || { echo "FULLJ_AEST_STABLE_CHI: missing $f" >&2; exit 3; }
done

PREDATA_LOCK="63d673b0e7f6349a2a10c762aac970f301646abd"
POSTHOC_LOCK="9e3d8e51fc3013894d071e3d1850177110866287"
git merge-base --is-ancestor "$PREDATA_LOCK" HEAD
git merge-base --is-ancestor "$POSTHOC_LOCK" HEAD
python - <<'PY'
import json
from pathlib import Path
j=json.loads(Path('results/fullj_aest_ulp_initial_amplitude_localization.json').read_text())
assert j['classification']=='FULLJ_AEST_ULP_LATE_EVOLUTION_DIVERGENCE'
assert j['diagnostic_complete'] is True
print('FULLJ_AEST_STABLE_CHI_PARENT_PASS')
PY
echo "FULLJ_AEST_STABLE_CHI_SCIENCE_LOCK_PASS predata=$PREDATA_LOCK posthoc=$POSTHOC_LOCK"

# Certified unmodified runtime.
source results/nl1c6d2n_corrected_class_densek64_env.sh
ORIG_ROOT="$NL1C6D2N_CLASS_ROOT"
ORIG_PYTARGET="$NL1C6D2N_PYTARGET"
EXPECTED_CLASS_HEAD="e85808324f51fc694d12e3ed7439552a3c3f9540"
EXPECTED_MEMORY_SHA="4d5ab5dc7066d4880f06fcfc731d6534ed0ff992e3cc15fb473dddccb25a594f"
[[ "$(git -C "$ORIG_ROOT" rev-parse HEAD)" == "$EXPECTED_CLASS_HEAD" ]]
[[ "$(sha256sum "$ORIG_ROOT/source/aest_memory.c" | awk '{print $1}')" == "$EXPECTED_MEMORY_SHA" ]]
grep -Eq '^#define[[:space:]]+_MAX_NUMBER_OF_K_FILES_[[:space:]]+64[[:space:]]*$' "$ORIG_ROOT/include/perturbations.h"
echo "FULLJ_AEST_STABLE_CHI_ORIGINAL_PROVENANCE_PASS head=$EXPECTED_CLASS_HEAD"

REF_JSON="results/fullj_aest_stable_chi_reference.json"
REF_NPZ="results/fullj_aest_stable_chi_reference.npz"
JSON="results/fullj_aest_stable_chi_residual.json"
NPZ="results/fullj_aest_stable_chi_residual.npz"
LOG="results/fullj_aest_stable_chi_residual.log"
ZIP="results/fullj_aest_stable_chi_residual_bundle.zip"
rm -f "$REF_JSON" "$REF_NPZ" "$JSON" "$NPZ" "$LOG" "$ZIP"

export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
unset AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE AEST_OFFLINE_TRACE_FILE AEST_TANGENT_ALLOW_K_MISS AEST_ERHS_TRACE_FILE AEST_ERHS_TRACE_K AEST_STABLE_CLASS_ROOT || true

# Reference rerun under the frozen unmodified implementation, before intervention.
export PYTHONPATH="$ORIG_PYTARGET${PYTHONPATH:+:$PYTHONPATH}"
python - <<PY
import classy
p=str(classy.__file__)
assert p.startswith('$ORIG_PYTARGET'), p
print('FULLJ_AEST_STABLE_CHI_REFERENCE_CLASSY_PASS module='+p)
PY
python -u -m fullj_weyl.aest_stable_chi_residual_intervention \
  --mode reference --reference-json "$REF_JSON" --reference-npz "$REF_NPZ"

# Build separate stable-residual CLASS copy.
STABLE_ROOT="$ROOT/.local/class_corrected_e8580832_densek64_stablechi"
STABLE_PYTARGET="$ROOT/.local/classy_corrected_e8580832_densek64_stablechi"
need_build=1
if [[ -d "$STABLE_ROOT/.git" && -f "$STABLE_ROOT/source/perturbations.c" \
      && -f "$STABLE_PYTARGET/classy/__init__.py" ]] \
   && grep -q 'FULLJ_AEST_STABLE_CHI_RESIDUAL_V1' "$STABLE_ROOT/source/perturbations.c"; then
  if [[ "$(git -C "$STABLE_ROOT" rev-parse HEAD)" == "$EXPECTED_CLASS_HEAD" \
        && "$(sha256sum "$STABLE_ROOT/source/aest_memory.c" | awk '{print $1}')" == "$EXPECTED_MEMORY_SHA" ]]; then
    need_build=0
  fi
fi

if [[ "$need_build" -eq 1 ]]; then
  echo "FULLJ_AEST_STABLE_CHI: preparing stable-residual CLASS copy..."
  rm -rf "$STABLE_ROOT" "$STABLE_PYTARGET"
  cp -a "$ORIG_ROOT" "$STABLE_ROOT"
  python fullj_weyl/apply_aest_stable_chi_residual_patch.py "$STABLE_ROOT"
  rm -rf "$STABLE_ROOT/build" "$STABLE_ROOT/python/build" "$STABLE_ROOT/python/classy.egg-info" 2>/dev/null || true
  mkdir -p "$STABLE_PYTARGET"
  python -m pip install --no-deps --no-build-isolation --target "$STABLE_PYTARGET" "$STABLE_ROOT"
else
  echo "FULLJ_AEST_STABLE_CHI: reusing stable-residual CLASS copy"
fi

grep -q 'FULLJ_AEST_STABLE_CHI_RESIDUAL_V1' "$STABLE_ROOT/source/perturbations.c"
[[ "$(sha256sum "$STABLE_ROOT/source/aest_memory.c" | awk '{print $1}')" == "$EXPECTED_MEMORY_SHA" ]]

# Stable intervention run in a fresh Python process.
export PYTHONPATH="$STABLE_PYTARGET:$ORIG_PYTARGET${PYTHONPATH:+:$PYTHONPATH}"
export AEST_STABLE_CLASS_ROOT="$STABLE_ROOT"
python - <<PY
import classy
p=str(classy.__file__)
assert p.startswith('$STABLE_PYTARGET'), p
print('FULLJ_AEST_STABLE_CHI_CLASSY_PASS module='+p)
from classy import Class
c=Class(); c.empty()
PY

set +e
python -u -m fullj_weyl.aest_stable_chi_residual_intervention \
  --mode stable --reference-json "$REF_JSON" --reference-npz "$REF_NPZ" \
  --json-out "$JSON" --npz-out "$NPZ" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

python - "$ZIP" "$LOG" "$JSON" "$NPZ" "$REF_JSON" "$REF_NPZ" <<'PY'
from pathlib import Path
import sys,zipfile
zp=Path(sys.argv[1])
paths=[Path(x) for x in sys.argv[2:]] + [
    Path('docs/fullj_aest_stable_chi_residual_predata.md'),
    Path('docs/fullj_aest_ulp_chi_cancellation_posthoc.md'),
    Path('fullj_weyl/apply_aest_stable_chi_residual_patch.py'),
    Path('fullj_weyl/aest_stable_chi_residual_intervention.py'),
    Path('fullj_weyl/run_local_aest_stable_chi_residual.sh'),
    Path('results/fullj_aest_ulp_initial_amplitude_localization.json'),
    Path('results/fullj_aest_ulp_initial_amplitude_localization.npz'),
    Path('results/nl1c6d2n_corrected_class_densek64_env.sh'),
]
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED) as zf:
    seen=set()
    for p in paths:
        if p.exists() and p not in seen:
            zf.write(p,arcname=str(p)); seen.add(p)
print('FULLJ_AEST_STABLE_CHI_BUNDLE='+str(zp))
PY

echo "FULLJ_AEST_STABLE_CHI_EXIT=$code"
echo "FULLJ_AEST_STABLE_CHI_LOG=$LOG"
echo "FULLJ_AEST_STABLE_CHI_JSON=$JSON"
echo "FULLJ_AEST_STABLE_CHI_NPZ=$NPZ"
echo "FULLJ_AEST_STABLE_CHI_ZIP=$ZIP"
exit "$code"
