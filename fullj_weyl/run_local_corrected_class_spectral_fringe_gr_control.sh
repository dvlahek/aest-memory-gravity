#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

BASE_PY=""
if command -v python3 >/dev/null 2>&1; then BASE_PY="$(command -v python3)";
elif command -v python >/dev/null 2>&1; then BASE_PY="$(command -v python)";
else echo "FULLJ_DIRECT_CLASS_FRINGE: python missing" >&2; exit 2; fi

VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then
  "$BASE_PY" -m venv "$VENV" || { echo "FULLJ_DIRECT_CLASS_FRINGE: install python3-venv" >&2; exit 2; }
fi
export PATH="$VENV/bin:$PATH"
python -m pip install --upgrade pip setuptools wheel >/dev/null
python -m pip install numpy scipy cython >/dev/null

python -m py_compile \
  fullj_weyl/corrected_class_spectral_fringe_gr_control.py \
  nl1c6d2n/corrected_class_baseline.py \
  nl1c6d2a/baryon_matter_sector_audit.py

for f in \
  docs/fullj_corrected_class_spectral_fringe_gr_control_predata.md \
  docs/fullj_spectral_fringe_source_decomposition_result.md \
  results/fullj_spectral_fringe_source_decomposition.json \
  results/fullj_spectral_fringe_source_decomposition.npz; do
  if [[ ! -f "$f" ]]; then
    echo "FULLJ_DIRECT_CLASS_FRINGE: missing required lock/input $f" >&2
    exit 3
  fi
done

python - <<'PY'
import hashlib, json
from pathlib import Path
from fullj_weyl import corrected_class_spectral_fringe_gr_control as q

assert q.PREDATA_LOCK == '0e26b4688eeeedd522b8dd153f84a76137d7e43c'
assert q.DECOMP_RESULT_LOCK == '0e4a3be830e2c6a5e87a7cb259a09bcb459f9d5f'
assert len(q.K_DENSE) == 51
assert len(q.K_ANCHOR) == 15
assert abs(q.DK-0.000625) < 1e-15
assert all(len(w)==17 for w in q.WINDOWS)
assert q.MIN_SPEC_RATIO == 10.0
p=Path('results/fullj_spectral_fringe_source_decomposition.npz')
h=hashlib.sha256(p.read_bytes()).hexdigest()
assert h == q.SOURCE_NPZ_SHA256, (h,q.SOURCE_NPZ_SHA256)
meta=json.loads(Path('results/fullj_spectral_fringe_source_decomposition.json').read_text())
assert meta['classification']=='FULLJ_SPECTRAL_FRINGE_SOURCE_DECOMPOSITION_CORRECTED_CLASS_LINEAR_SECTOR_DOMINATED'
print('FULLJ_DIRECT_CLASS_FRINGE_IMPORT_CHAIN_PASS')
print('FULLJ_DIRECT_CLASS_FRINGE_PARENT_LOCK_PASS sha256='+h)
print('FULLJ_DIRECT_CLASS_FRINGE_GRID_PASS dense=51 anchors=15 windows=3 points_per_window=17 dk_h=0.000625')
print('FULLJ_DIRECT_CLASS_FRINGE_CONTROLS_PASS aest_dense=51 aest_sparse=15 gr_dense=51')
PY

ENVFILE="$ROOT/results/nl1c6d2n_corrected_class_densek64_env.sh"
reuse=0
if [[ -f "$ENVFILE" ]]; then
  # shellcheck disable=SC1090
  source "$ENVFILE"
  if [[ -n "${NL1C6D2N_CLASS_ROOT:-}" && -d "$NL1C6D2N_CLASS_ROOT/.git" \
        && -f "$NL1C6D2N_CLASS_ROOT/source/aest_memory.c" \
        && -f "$NL1C6D2N_CLASS_ROOT/include/perturbations.h" \
        && -n "${NL1C6D2N_PYTARGET:-}" && -f "$NL1C6D2N_PYTARGET/classy/__init__.py" \
        && "${FULLJ_DENSE_RESIDUAL_R2_CLASS_KFILE_LIMIT:-}" == "64" ]]; then
    reuse=1
  fi
fi

if [[ "$reuse" -eq 1 ]]; then
  echo "FULLJ_DIRECT_CLASS_FRINGE: reusing isolated corrected CLASS dense-k64 environment..."
else
  echo "FULLJ_DIRECT_CLASS_FRINGE: preparing isolated corrected CLASS dense-k64 environment..."
  bash fullj_weyl/setup_corrected_class_dense_k64_local.sh
  # shellcheck disable=SC1090
  source "$ENVFILE"
fi

grep -Eq '^#define[[:space:]]+_MAX_NUMBER_OF_K_FILES_[[:space:]]+64[[:space:]]*$' \
  "$NL1C6D2N_CLASS_ROOT/include/perturbations.h"

python - <<'PY'
import os, numpy, scipy, classy
from classy import Class
print('FULLJ_DIRECT_CLASS_FRINGE_CLASS_KFILE_LIMIT_PASS value='+os.environ.get('FULLJ_DENSE_RESIDUAL_R2_CLASS_KFILE_LIMIT',''))
print('FULLJ_DIRECT_CLASS_FRINGE_ENV_PASS')
print('numpy='+numpy.__version__)
print('scipy='+scipy.__version__)
print('classy_module='+str(classy.__file__))
print('NL1C6D2N_CLASS_ROOT='+os.environ['NL1C6D2N_CLASS_ROOT'])
c=Class(); c.empty()
PY

JSON="results/fullj_corrected_class_spectral_fringe_gr_control.json"
NPZ="results/fullj_corrected_class_spectral_fringe_gr_control.npz"
LOG="results/fullj_corrected_class_spectral_fringe_gr_control.log"
ZIP="results/fullj_corrected_class_spectral_fringe_gr_control_bundle.zip"
rm -f "$JSON" "$NPZ" "$LOG" "$ZIP"

export OMP_NUM_THREADS=1
unset AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE AEST_OFFLINE_TRACE_FILE AEST_TANGENT_ALLOW_K_MISS || true

set +e
python -u -m fullj_weyl.corrected_class_spectral_fringe_gr_control \
  --json-out "$JSON" --npz-out "$NPZ" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

python - "$ZIP" "$LOG" "$JSON" "$NPZ" <<'PY'
from pathlib import Path
import sys, zipfile
zp=Path(sys.argv[1])
paths=[Path(x) for x in sys.argv[2:]] + [
    Path('docs/fullj_corrected_class_spectral_fringe_gr_control_predata.md'),
    Path('docs/fullj_spectral_fringe_source_decomposition_result.md'),
    Path('fullj_weyl/corrected_class_spectral_fringe_gr_control.py'),
    Path('fullj_weyl/run_local_corrected_class_spectral_fringe_gr_control.sh'),
    Path('results/fullj_spectral_fringe_source_decomposition.json'),
    Path('results/fullj_spectral_fringe_source_decomposition.npz'),
    Path('results/nl1c6d2n_corrected_class_densek64_env.sh'),
]
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED) as zf:
    seen=set()
    for p in paths:
        if p.exists() and p not in seen:
            zf.write(p,arcname=str(p)); seen.add(p)
print('FULLJ_DIRECT_CLASS_FRINGE_BUNDLE='+str(zp))
PY

echo "FULLJ_DIRECT_CLASS_FRINGE_EXIT=$code"
echo "FULLJ_DIRECT_CLASS_FRINGE_LOG=$LOG"
echo "FULLJ_DIRECT_CLASS_FRINGE_JSON=$JSON"
echo "FULLJ_DIRECT_CLASS_FRINGE_NPZ=$NPZ"
echo "FULLJ_DIRECT_CLASS_FRINGE_ZIP=$ZIP"
exit "$code"
