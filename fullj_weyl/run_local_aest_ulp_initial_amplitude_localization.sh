#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

BASE_PY=""
if command -v python3 >/dev/null 2>&1; then BASE_PY="$(command -v python3)";
elif command -v python >/dev/null 2>&1; then BASE_PY="$(command -v python)";
else echo "FULLJ_AEST_ULP_INITIAL_AMPLITUDE: python missing" >&2; exit 2; fi

VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then
  "$BASE_PY" -m venv "$VENV" || { echo "FULLJ_AEST_ULP_INITIAL_AMPLITUDE: install python3-venv" >&2; exit 2; }
fi
export PATH="$VENV/bin:$PATH"
python -m pip install --upgrade pip setuptools wheel >/dev/null
python -m pip install numpy scipy cython >/dev/null

python -m py_compile \
  fullj_weyl/aest_ulp_initial_amplitude_localization.py \
  fullj_weyl/corrected_class_spectral_fringe_k_ulp_forensics.py \
  fullj_weyl/corrected_class_spectral_fringe_bridge_identity.py

echo "FULLJ_AEST_ULP_INITIAL_AMPLITUDE_IMPORT_PASS"

for f in \
  docs/fullj_aest_ulp_initial_amplitude_localization_predata.md \
  results/fullj_corrected_class_spectral_fringe_k_ulp_forensics.json \
  results/fullj_corrected_class_spectral_fringe_k_ulp_forensics.npz \
  results/nl1c6d2n_corrected_class_densek64_env.sh; do
  [[ -f "$f" ]] || { echo "FULLJ_AEST_ULP_INITIAL_AMPLITUDE: missing $f" >&2; exit 3; }
done

python - <<'PY'
import json
from pathlib import Path
j=json.loads(Path('results/fullj_corrected_class_spectral_fringe_k_ulp_forensics.json').read_text())
assert j['classification']=='FULLJ_CLASS_FRINGE_AEST_ULP_SENSITIVITY_CERTIFIED'
assert j['diagnostic_complete'] is True
assert all(j['gates'].values())
print('FULLJ_AEST_ULP_INITIAL_AMPLITUDE_PARENT_PASS')
PY

PREDATA_LOCK="429c61c366d5f92073d72d4c963df3ea39f7c48f"
if ! git merge-base --is-ancestor "$PREDATA_LOCK" HEAD; then
  echo "FULLJ_AEST_ULP_INITIAL_AMPLITUDE_PREDATA_LOCK_FAIL" >&2
  exit 3
fi

source results/nl1c6d2n_corrected_class_densek64_env.sh
EXPECTED_CLASS_HEAD="e85808324f51fc694d12e3ed7439552a3c3f9540"
EXPECTED_RUNTIME_SHA="4d5ab5dc7066d4880f06fcfc731d6534ed0ff992e3cc15fb473dddccb25a594f"
ACTUAL_CLASS_HEAD="$(git -C "$NL1C6D2N_CLASS_ROOT" rev-parse HEAD)"
ACTUAL_RUNTIME_SHA="$(sha256sum "$NL1C6D2N_CLASS_ROOT/source/aest_memory.c" | awk '{print $1}')"
[[ "$ACTUAL_CLASS_HEAD" == "$EXPECTED_CLASS_HEAD" ]]
[[ "$ACTUAL_RUNTIME_SHA" == "$EXPECTED_RUNTIME_SHA" ]]
grep -Eq '^#define[[:space:]]+_MAX_NUMBER_OF_K_FILES_[[:space:]]+64[[:space:]]*$' "$NL1C6D2N_CLASS_ROOT/include/perturbations.h"
echo "FULLJ_AEST_ULP_INITIAL_AMPLITUDE_RUNTIME_PROVENANCE_PASS head=$ACTUAL_CLASS_HEAD source_sha256=$ACTUAL_RUNTIME_SHA kfile_limit=64"

TRACE="results/fullj_aest_ulp_initial_amplitude_source_trace.txt"
{
  echo "# Read-only source trace"
  echo "# CLASS_HEAD=$ACTUAL_CLASS_HEAD"
  echo "# AEST_MEMORY_SHA256=$ACTUAL_RUNTIME_SHA"
  for src in "$NL1C6D2N_CLASS_ROOT/source/aest_memory.c" "$NL1C6D2N_CLASS_ROOT/source/perturbations.c"; do
    echo
    echo "===== $src ====="
    grep -nEi -C 4 'k_output_values|index_k_output|alpha_aest|E_aest|alpha|initial|aest' "$src" || true
  done
} > "$TRACE"
echo "FULLJ_AEST_ULP_INITIAL_AMPLITUDE_SOURCE_TRACE_PASS file=$TRACE"

JSON="results/fullj_aest_ulp_initial_amplitude_localization.json"
NPZ="results/fullj_aest_ulp_initial_amplitude_localization.npz"
LOG="results/fullj_aest_ulp_initial_amplitude_localization.log"
ZIP="results/fullj_aest_ulp_initial_amplitude_localization_bundle.zip"
rm -f "$JSON" "$NPZ" "$LOG" "$ZIP"

export OMP_NUM_THREADS=1
unset AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE AEST_OFFLINE_TRACE_FILE AEST_TANGENT_ALLOW_K_MISS || true

set +e
python -u -m fullj_weyl.aest_ulp_initial_amplitude_localization \
  --json-out "$JSON" --npz-out "$NPZ" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

python - "$ZIP" "$LOG" "$JSON" "$NPZ" "$TRACE" <<'PY'
from pathlib import Path
import sys, zipfile
zp=Path(sys.argv[1])
paths=[Path(x) for x in sys.argv[2:]] + [
    Path('docs/fullj_aest_ulp_initial_amplitude_localization_predata.md'),
    Path('fullj_weyl/aest_ulp_initial_amplitude_localization.py'),
    Path('fullj_weyl/run_local_aest_ulp_initial_amplitude_localization.sh'),
    Path('results/fullj_corrected_class_spectral_fringe_k_ulp_forensics.json'),
    Path('results/fullj_corrected_class_spectral_fringe_k_ulp_forensics.npz'),
    Path('results/nl1c6d2n_corrected_class_densek64_env.sh'),
]
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED) as zf:
    seen=set()
    for p in paths:
        if p.exists() and p not in seen:
            zf.write(p,arcname=str(p)); seen.add(p)
print('FULLJ_AEST_ULP_INITIAL_AMPLITUDE_BUNDLE='+str(zp))
PY

echo "FULLJ_AEST_ULP_INITIAL_AMPLITUDE_EXIT=$code"
echo "FULLJ_AEST_ULP_INITIAL_AMPLITUDE_LOG=$LOG"
echo "FULLJ_AEST_ULP_INITIAL_AMPLITUDE_JSON=$JSON"
echo "FULLJ_AEST_ULP_INITIAL_AMPLITUDE_NPZ=$NPZ"
echo "FULLJ_AEST_ULP_INITIAL_AMPLITUDE_TRACE=$TRACE"
echo "FULLJ_AEST_ULP_INITIAL_AMPLITUDE_ZIP=$ZIP"
exit "$code"
