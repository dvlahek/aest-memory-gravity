#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

BASE_PY=""
if command -v python3 >/dev/null 2>&1; then BASE_PY="$(command -v python3)";
elif command -v python >/dev/null 2>&1; then BASE_PY="$(command -v python)";
else echo "FULLJ_AEST_ULP_E_RHS: python missing" >&2; exit 2; fi

VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then
  "$BASE_PY" -m venv "$VENV" || { echo "FULLJ_AEST_ULP_E_RHS: install python3-venv" >&2; exit 2; }
fi
export PATH="$VENV/bin:$PATH"
python -m pip install --upgrade pip setuptools wheel >/dev/null
python -m pip install numpy scipy cython >/dev/null

python -m py_compile \
  fullj_weyl/apply_aest_E_rhs_trace_patch.py \
  fullj_weyl/aest_ulp_E_rhs_decomposition.py \
  fullj_weyl/aest_ulp_initial_amplitude_localization.py

echo "FULLJ_AEST_ULP_E_RHS_IMPORT_PASS"

for f in \
  docs/fullj_aest_ulp_E_rhs_decomposition_predata.md \
  docs/fullj_aest_ulp_E_rhs_trace_newline_repair.md \
  results/fullj_aest_ulp_initial_amplitude_localization.json \
  results/fullj_aest_ulp_initial_amplitude_localization.npz \
  results/nl1c6d2n_corrected_class_densek64_env.sh; do
  [[ -f "$f" ]] || { echo "FULLJ_AEST_ULP_E_RHS: missing $f" >&2; exit 3; }
done

python - <<'PY'
import json
from pathlib import Path
j=json.loads(Path('results/fullj_aest_ulp_initial_amplitude_localization.json').read_text())
assert j['classification']=='FULLJ_AEST_ULP_LATE_EVOLUTION_DIVERGENCE'
assert j['diagnostic_complete'] is True
print('FULLJ_AEST_ULP_E_RHS_PARENT_PASS')
PY

PREDATA_LOCK="0c8dce2022626e194fa90aafe45242f2ed1fc8a7"
git merge-base --is-ancestor "$PREDATA_LOCK" HEAD
echo "FULLJ_AEST_ULP_E_RHS_SCIENCE_LOCK_PASS predata=$PREDATA_LOCK"

source results/nl1c6d2n_corrected_class_densek64_env.sh
ORIG_ROOT="$NL1C6D2N_CLASS_ROOT"
EXPECTED_CLASS_HEAD="e85808324f51fc694d12e3ed7439552a3c3f9540"
EXPECTED_MEMORY_SHA="4d5ab5dc7066d4880f06fcfc731d6534ed0ff992e3cc15fb473dddccb25a594f"
[[ "$(git -C "$ORIG_ROOT" rev-parse HEAD)" == "$EXPECTED_CLASS_HEAD" ]]
[[ "$(sha256sum "$ORIG_ROOT/source/aest_memory.c" | awk '{print $1}')" == "$EXPECTED_MEMORY_SHA" ]]
grep -Eq '^#define[[:space:]]+_MAX_NUMBER_OF_K_FILES_[[:space:]]+64[[:space:]]*$' "$ORIG_ROOT/include/perturbations.h"
echo "FULLJ_AEST_ULP_E_RHS_ORIGINAL_PROVENANCE_PASS head=$EXPECTED_CLASS_HEAD"

DIAG_ROOT="$ROOT/.local/class_corrected_e8580832_densek64_erhsdiag"
DIAG_PYTARGET="$ROOT/.local/classy_corrected_e8580832_densek64_erhsdiag"
need_build=1
if [[ -d "$DIAG_ROOT/.git" && -f "$DIAG_ROOT/source/perturbations.c" \
      && -f "$DIAG_PYTARGET/classy/__init__.py" ]] \
   && grep -q 'FULLJ_AEST_ERHS_TRACE_V2' "$DIAG_ROOT/source/perturbations.c"; then
  if [[ "$(git -C "$DIAG_ROOT" rev-parse HEAD)" == "$EXPECTED_CLASS_HEAD" \
        && "$(sha256sum "$DIAG_ROOT/source/aest_memory.c" | awk '{print $1}')" == "$EXPECTED_MEMORY_SHA" ]]; then
    need_build=0
  fi
fi

if [[ "$need_build" -eq 1 ]]; then
  echo "FULLJ_AEST_ULP_E_RHS: preparing diagnostic CLASS copy..."
  rm -rf "$DIAG_ROOT" "$DIAG_PYTARGET"
  cp -a "$ORIG_ROOT" "$DIAG_ROOT"
  python fullj_weyl/apply_aest_E_rhs_trace_patch.py "$DIAG_ROOT"
  rm -rf "$DIAG_ROOT/build" "$DIAG_ROOT/python/build" "$DIAG_ROOT/python/classy.egg-info" 2>/dev/null || true
  mkdir -p "$DIAG_PYTARGET"
  python -m pip install --no-deps --no-build-isolation --target "$DIAG_PYTARGET" "$DIAG_ROOT"
else
  echo "FULLJ_AEST_ULP_E_RHS: reusing diagnostic CLASS copy"
fi

grep -q 'FULLJ_AEST_ERHS_TRACE_V2' "$DIAG_ROOT/source/perturbations.c"
[[ "$(sha256sum "$DIAG_ROOT/source/aest_memory.c" | awk '{print $1}')" == "$EXPECTED_MEMORY_SHA" ]]

export PYTHONPATH="$DIAG_PYTARGET${PYTHONPATH:+:$PYTHONPATH}"
python - <<PY
from classy import Class
import classy
p=str(classy.__file__)
assert p.startswith('$DIAG_PYTARGET'), p
print('FULLJ_AEST_ULP_E_RHS_DIAGNOSTIC_CLASSY_PASS module='+p)
c=Class(); c.empty()
PY

python - "$DIAG_ROOT/source/perturbations.c" results/fullj_aest_ulp_E_rhs_source_excerpt.txt <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]); out=Path(sys.argv[2]); lines=p.read_text().splitlines()
i=next(i for i,s in enumerate(lines) if 'FULLJ_AEST_ERHS_TRACE_V2' in s)
lo=max(0,i-28); hi=min(len(lines),i+75)
out.write_text('\n'.join(f'{j+1}: {lines[j]}' for j in range(lo,hi))+'\n')
print('FULLJ_AEST_ULP_E_RHS_SOURCE_TRACE_PASS file='+str(out))
PY

JSON="results/fullj_aest_ulp_E_rhs_decomposition.json"
NPZ="results/fullj_aest_ulp_E_rhs_decomposition.npz"
LOG="results/fullj_aest_ulp_E_rhs_decomposition.log"
ZIP="results/fullj_aest_ulp_E_rhs_decomposition_bundle.zip"
TRACE_DIR="results/fullj_aest_ulp_E_rhs_traces"
rm -f "$JSON" "$NPZ" "$LOG" "$ZIP"
rm -rf "$TRACE_DIR" && mkdir -p "$TRACE_DIR"

export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1
unset AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE AEST_OFFLINE_TRACE_FILE AEST_TANGENT_ALLOW_K_MISS AEST_ERHS_TRACE_FILE AEST_ERHS_TRACE_K || true

set +e
python -u -m fullj_weyl.aest_ulp_E_rhs_decomposition \
  --json-out "$JSON" --npz-out "$NPZ" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

python - "$ZIP" "$LOG" "$JSON" "$NPZ" <<'PY'
from pathlib import Path
import sys, zipfile
zp=Path(sys.argv[1])
paths=[Path(x) for x in sys.argv[2:]] + [
    Path('docs/fullj_aest_ulp_E_rhs_decomposition_predata.md'),
    Path('docs/fullj_aest_ulp_E_rhs_trace_newline_repair.md'),
    Path('fullj_weyl/apply_aest_E_rhs_trace_patch.py'),
    Path('fullj_weyl/aest_ulp_E_rhs_decomposition.py'),
    Path('fullj_weyl/run_local_aest_ulp_E_rhs_decomposition.sh'),
    Path('results/fullj_aest_ulp_initial_amplitude_localization.json'),
    Path('results/fullj_aest_ulp_initial_amplitude_localization.npz'),
    Path('results/fullj_aest_ulp_E_rhs_source_excerpt.txt'),
    Path('results/nl1c6d2n_corrected_class_densek64_env.sh'),
]
paths += sorted(Path('results/fullj_aest_ulp_E_rhs_traces').glob('*.txt'))
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED) as zf:
    seen=set()
    for p in paths:
        if p.exists() and p not in seen:
            zf.write(p,arcname=str(p)); seen.add(p)
print('FULLJ_AEST_ULP_E_RHS_BUNDLE='+str(zp))
PY

echo "FULLJ_AEST_ULP_E_RHS_EXIT=$code"
echo "FULLJ_AEST_ULP_E_RHS_LOG=$LOG"
echo "FULLJ_AEST_ULP_E_RHS_JSON=$JSON"
echo "FULLJ_AEST_ULP_E_RHS_NPZ=$NPZ"
echo "FULLJ_AEST_ULP_E_RHS_ZIP=$ZIP"
exit "$code"
