#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

BASE_PY=""
if command -v python3 >/dev/null 2>&1; then BASE_PY="$(command -v python3)";
elif command -v python >/dev/null 2>&1; then BASE_PY="$(command -v python)";
else echo "FULLJ_CLASS_FRINGE_PARAMETER_FACTORIZATION: python missing" >&2; exit 2; fi

VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then
  "$BASE_PY" -m venv "$VENV" || { echo "FULLJ_CLASS_FRINGE_PARAMETER_FACTORIZATION: install python3-venv" >&2; exit 2; }
fi
export PATH="$VENV/bin:$PATH"
python -m pip install --upgrade pip setuptools wheel >/dev/null
python -m pip install numpy scipy cython >/dev/null

python -m py_compile \
  fullj_weyl/corrected_class_spectral_fringe_parameter_factorization.py \
  fullj_weyl/corrected_class_spectral_fringe_bridge_identity.py \
  fullj_weyl/corrected_class_spectral_fringe_bridge_identity_r1.py

echo "FULLJ_CLASS_FRINGE_PARAMETER_FACTORIZATION_IMPORT_PASS"

for f in \
  docs/fullj_corrected_class_spectral_fringe_parameter_factorization_predata.md \
  results/fullj_corrected_class_spectral_fringe_bridge_identity.json \
  results/fullj_corrected_class_spectral_fringe_bridge_identity.npz \
  results/nl1c6d2n_corrected_class_densek64_env.sh; do
  [[ -f "$f" ]] || { echo "FULLJ_CLASS_FRINGE_PARAMETER_FACTORIZATION: missing $f" >&2; exit 3; }
done

python - <<'PY'
import json
from pathlib import Path
j=json.loads(Path('results/fullj_corrected_class_spectral_fringe_bridge_identity.json').read_text())
assert j['classification']=='FULLJ_CLASS_FRINGE_BRIDGE_PARAMETER_DEPENDENCE'
assert j['diagnostic_complete'] is True
assert j['gates']['BI_G1_provenance_and_frozen_identity'] is True
assert j['gates']['BI_G2_bridge_list_invariance_direct_params'] is True
assert j['gates']['BI_G3_parameter_construction_identity'] is False
assert j['gates']['BI_G4_history_order_identity'] is True
assert j['gates']['BI_G5_bridge_time_coordinate_identity'] is True
assert j['gates']['BI_G6_basis_fourier_extraction_identity'] is True
assert j['gates']['BI_REPAIR_single_k_fingerprint_identity'] is True
print('FULLJ_CLASS_FRINGE_PARAMETER_FACTORIZATION_SCIENCE_LOCKS_PASS')
PY

source results/nl1c6d2n_corrected_class_densek64_env.sh
EXPECTED_CLASS_HEAD="e85808324f51fc694d12e3ed7439552a3c3f9540"
EXPECTED_RUNTIME_SHA="4d5ab5dc7066d4880f06fcfc731d6534ed0ff992e3cc15fb473dddccb25a594f"
ACTUAL_CLASS_HEAD="$(git -C "$NL1C6D2N_CLASS_ROOT" rev-parse HEAD)"
ACTUAL_RUNTIME_SHA="$(sha256sum "$NL1C6D2N_CLASS_ROOT/source/aest_memory.c" | awk '{print $1}')"
[[ "$ACTUAL_CLASS_HEAD" == "$EXPECTED_CLASS_HEAD" ]]
[[ "$ACTUAL_RUNTIME_SHA" == "$EXPECTED_RUNTIME_SHA" ]]
grep -Eq '^#define[[:space:]]+_MAX_NUMBER_OF_K_FILES_[[:space:]]+64[[:space:]]*$' "$NL1C6D2N_CLASS_ROOT/include/perturbations.h"
echo "FULLJ_CLASS_FRINGE_PARAMETER_FACTORIZATION_RUNTIME_PROVENANCE_PASS head=$ACTUAL_CLASS_HEAD source_sha256=$ACTUAL_RUNTIME_SHA kfile_limit=64"

JSON="results/fullj_corrected_class_spectral_fringe_parameter_factorization.json"
NPZ="results/fullj_corrected_class_spectral_fringe_parameter_factorization.npz"
LOG="results/fullj_corrected_class_spectral_fringe_parameter_factorization.log"
ZIP="results/fullj_corrected_class_spectral_fringe_parameter_factorization_bundle.zip"
rm -f "$JSON" "$NPZ" "$LOG" "$ZIP"

export OMP_NUM_THREADS=1
unset AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE AEST_OFFLINE_TRACE_FILE AEST_TANGENT_ALLOW_K_MISS || true

set +e
python -u -m fullj_weyl.corrected_class_spectral_fringe_parameter_factorization \
  --json-out "$JSON" --npz-out "$NPZ" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

python - "$ZIP" "$LOG" "$JSON" "$NPZ" <<'PY'
from pathlib import Path
import sys, zipfile
zp=Path(sys.argv[1])
paths=[Path(x) for x in sys.argv[2:]] + [
    Path('docs/fullj_corrected_class_spectral_fringe_parameter_factorization_predata.md'),
    Path('fullj_weyl/corrected_class_spectral_fringe_parameter_factorization.py'),
    Path('fullj_weyl/run_local_corrected_class_spectral_fringe_parameter_factorization.sh'),
    Path('results/fullj_corrected_class_spectral_fringe_bridge_identity.json'),
    Path('results/fullj_corrected_class_spectral_fringe_bridge_identity.npz'),
    Path('results/nl1c6d2n_corrected_class_densek64_env.sh'),
]
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED) as zf:
    seen=set()
    for p in paths:
        if p.exists() and p not in seen:
            zf.write(p,arcname=str(p)); seen.add(p)
print('FULLJ_CLASS_FRINGE_PARAMETER_FACTORIZATION_BUNDLE='+str(zp))
PY

echo "FULLJ_CLASS_FRINGE_PARAMETER_FACTORIZATION_EXIT=$code"
echo "FULLJ_CLASS_FRINGE_PARAMETER_FACTORIZATION_LOG=$LOG"
echo "FULLJ_CLASS_FRINGE_PARAMETER_FACTORIZATION_JSON=$JSON"
echo "FULLJ_CLASS_FRINGE_PARAMETER_FACTORIZATION_NPZ=$NPZ"
echo "FULLJ_CLASS_FRINGE_PARAMETER_FACTORIZATION_ZIP=$ZIP"
exit "$code"
