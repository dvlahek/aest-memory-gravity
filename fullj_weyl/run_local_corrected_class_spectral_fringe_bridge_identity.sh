#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

BASE_PY=""
if command -v python3 >/dev/null 2>&1; then BASE_PY="$(command -v python3)";
elif command -v python >/dev/null 2>&1; then BASE_PY="$(command -v python)";
else echo "FULLJ_CLASS_FRINGE_BRIDGE_IDENTITY: python missing" >&2; exit 2; fi

VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then
  "$BASE_PY" -m venv "$VENV" || { echo "FULLJ_CLASS_FRINGE_BRIDGE_IDENTITY: install python3-venv" >&2; exit 2; }
fi
export PATH="$VENV/bin:$PATH"
python -m pip install --upgrade pip setuptools wheel >/dev/null
python -m pip install numpy scipy cython >/dev/null

python -m py_compile \
  fullj_weyl/corrected_class_spectral_fringe_bridge_identity.py \
  fullj_weyl/corrected_class_spectral_fringe_gr_control.py \
  fullj_weyl/corrected_class_spectral_fringe_gr_control_r3.py \
  fullj_weyl/spectral_fringe_source_decomposition.py

echo "FULLJ_CLASS_FRINGE_BRIDGE_IDENTITY_IMPORT_PASS"

for f in \
  docs/fullj_corrected_class_spectral_fringe_bridge_identity_predata.md \
  results/fullj_corrected_class_spectral_fringe_extractor_equivalence.json \
  results/fullj_corrected_class_spectral_fringe_extractor_equivalence.npz \
  results/fullj_corrected_class_spectral_fringe_gr_control.json \
  results/fullj_corrected_class_spectral_fringe_gr_control.npz \
  results/nl1c6d2n_corrected_class_densek64_env.sh; do
  if [[ ! -f "$f" ]]; then
    echo "FULLJ_CLASS_FRINGE_BRIDGE_IDENTITY: missing required input $f" >&2
    exit 3
  fi
done

python - <<'PY'
import json
from pathlib import Path
from fullj_weyl import corrected_class_spectral_fringe_bridge_identity as q
assert q.PREDATA_LOCK == '82d6f80495f9b3265c4cd949e573a39abea69df3'
e=json.loads(Path('results/fullj_corrected_class_spectral_fringe_extractor_equivalence.json').read_text())
r=json.loads(Path('results/fullj_corrected_class_spectral_fringe_gr_control.json').read_text())
assert e['classification']=='FULLJ_CLASS_FRINGE_EXTRACTOR_MISMATCH_CERTIFIED'
assert all(e['gates'].values())
assert r['classification']=='FULLJ_CORRECTED_CLASS_SPECTRAL_FRINGE_NUMERICAL_CONTROL_FAIL'
assert r['gates']['DG_G3_requested_k_list_invariance'] is True
assert r['gates']['DG_G4_dense_grid_health'] is True
assert r['gates']['DG_G5_fine_grid_spectral_structure'] is True
assert r['gates']['DG_G6_AeST_specificity_against_GR'] is True
print('FULLJ_CLASS_FRINGE_BRIDGE_IDENTITY_SCIENCE_LOCKS_PASS')
PY

# Reuse exact corrected dense-k64 runtime from R3/extractor audit.
# shellcheck disable=SC1090
source results/nl1c6d2n_corrected_class_densek64_env.sh
EXPECTED_CLASS_HEAD="e85808324f51fc694d12e3ed7439552a3c3f9540"
EXPECTED_RUNTIME_SHA="4d5ab5dc7066d4880f06fcfc731d6534ed0ff992e3cc15fb473dddccb25a594f"
ACTUAL_CLASS_HEAD="$(git -C "$NL1C6D2N_CLASS_ROOT" rev-parse HEAD)"
ACTUAL_RUNTIME_SHA="$(sha256sum "$NL1C6D2N_CLASS_ROOT/source/aest_memory.c" | awk '{print $1}')"
[[ "$ACTUAL_CLASS_HEAD" == "$EXPECTED_CLASS_HEAD" ]]
[[ "$ACTUAL_RUNTIME_SHA" == "$EXPECTED_RUNTIME_SHA" ]]
grep -Eq '^#define[[:space:]]+_MAX_NUMBER_OF_K_FILES_[[:space:]]+64[[:space:]]*$' "$NL1C6D2N_CLASS_ROOT/include/perturbations.h"
echo "FULLJ_CLASS_FRINGE_BRIDGE_IDENTITY_RUNTIME_PROVENANCE_PASS head=$ACTUAL_CLASS_HEAD source_sha256=$ACTUAL_RUNTIME_SHA kfile_limit=64"

python - <<'PY'
import classy, numpy, scipy, os
print('FULLJ_CLASS_FRINGE_BRIDGE_IDENTITY_ENV_PASS')
print('numpy='+numpy.__version__)
print('scipy='+scipy.__version__)
print('classy_module='+str(classy.__file__))
print('NL1C6D2N_CLASS_ROOT='+os.environ['NL1C6D2N_CLASS_ROOT'])
PY

JSON="results/fullj_corrected_class_spectral_fringe_bridge_identity.json"
NPZ="results/fullj_corrected_class_spectral_fringe_bridge_identity.npz"
LOG="results/fullj_corrected_class_spectral_fringe_bridge_identity.log"
ZIP="results/fullj_corrected_class_spectral_fringe_bridge_identity_bundle.zip"
rm -f "$JSON" "$NPZ" "$LOG" "$ZIP"

export OMP_NUM_THREADS=1
unset AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE AEST_OFFLINE_TRACE_FILE AEST_TANGENT_ALLOW_K_MISS || true

set +e
python -u -m fullj_weyl.corrected_class_spectral_fringe_bridge_identity \
  --json-out "$JSON" --npz-out "$NPZ" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

python - "$ZIP" "$LOG" "$JSON" "$NPZ" <<'PY'
from pathlib import Path
import sys, zipfile
zp=Path(sys.argv[1])
paths=[Path(x) for x in sys.argv[2:]] + [
    Path('docs/fullj_corrected_class_spectral_fringe_bridge_identity_predata.md'),
    Path('fullj_weyl/corrected_class_spectral_fringe_bridge_identity.py'),
    Path('fullj_weyl/run_local_corrected_class_spectral_fringe_bridge_identity.sh'),
    Path('results/fullj_corrected_class_spectral_fringe_extractor_equivalence.json'),
    Path('results/fullj_corrected_class_spectral_fringe_extractor_equivalence.npz'),
    Path('results/fullj_corrected_class_spectral_fringe_gr_control.json'),
    Path('results/fullj_corrected_class_spectral_fringe_gr_control.npz'),
    Path('results/nl1c6d2n_corrected_class_densek64_env.sh'),
]
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED) as zf:
    seen=set()
    for p in paths:
        if p.exists() and p not in seen:
            zf.write(p,arcname=str(p)); seen.add(p)
print('FULLJ_CLASS_FRINGE_BRIDGE_IDENTITY_BUNDLE='+str(zp))
PY

echo "FULLJ_CLASS_FRINGE_BRIDGE_IDENTITY_EXIT=$code"
echo "FULLJ_CLASS_FRINGE_BRIDGE_IDENTITY_LOG=$LOG"
echo "FULLJ_CLASS_FRINGE_BRIDGE_IDENTITY_JSON=$JSON"
echo "FULLJ_CLASS_FRINGE_BRIDGE_IDENTITY_NPZ=$NPZ"
echo "FULLJ_CLASS_FRINGE_BRIDGE_IDENTITY_ZIP=$ZIP"
exit "$code"
