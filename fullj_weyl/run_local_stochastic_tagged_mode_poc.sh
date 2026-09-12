#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

BASE_PY=""
if command -v python3 >/dev/null 2>&1; then BASE_PY="$(command -v python3)";
elif command -v python >/dev/null 2>&1; then BASE_PY="$(command -v python)";
else echo "FULLJ_TAGGED_POC: python missing" >&2; exit 2; fi

VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then
  "$BASE_PY" -m venv "$VENV" || { echo "FULLJ_TAGGED_POC: install python3-venv" >&2; exit 2; }
fi
export PATH="$VENV/bin:$PATH"
python -m pip install --upgrade pip setuptools wheel >/dev/null
python -m pip install numpy scipy cython >/dev/null

python -m py_compile \
  fullj_weyl/stochastic_tagged_mode_poc.py \
  fullj_weyl/dense_radial_weyl_extension.py \
  fullj_weyl/dense_radial_weyl_extension_r1.py \
  fullj_weyl/evolving_flrw_weyl_bridge_r2.py

if [[ ! -f results/fullj_dense_radial_class_residual_r2.json ]]; then
  echo "FULLJ_TAGGED_POC: missing locked residual-R2 FAIL JSON" >&2; exit 3
fi
if [[ ! -f results/fullj_dense_radial_cardinality_audit.json ]]; then
  echo "FULLJ_TAGGED_POC: missing locked cardinality PASS JSON" >&2; exit 3
fi

python - <<'PY'
import json
from pathlib import Path
from fullj_weyl import stochastic_tagged_mode_poc as p

xy,g,digest=p.coeff_draw()
assert digest==p.COEFF_HASH
assert p.BACKGROUND_IDS==(0,1,2)
assert p.TARGETS==(0.0375,0.10,0.175)
assert p.EPS_LEVELS==(0.10,0.05)
assert p.geometry(0.0375)[:3]==(0.0025,15,512)
assert p.geometry(0.10)[:3]==(0.01,10,128)
assert p.geometry(0.175)[:3]==(0.005,35,256)
r=json.loads(Path('results/fullj_dense_radial_class_residual_r2.json').read_text())
c=json.loads(Path('results/fullj_dense_radial_cardinality_audit.json').read_text())
assert r['classification']=='FULLJ_DENSE_RADIAL_CLASS_RESIDUAL_R2_FAIL'
assert c['classification']=='FULLJ_DENSE_RADIAL_CARDINALITY_AUDIT_PASS'
print('FULLJ_TAGGED_POC_IMPORT_CHAIN_PASS')
print('FULLJ_TAGGED_POC_LOCAL_LOCKS_PASS')
print('FULLJ_TAGGED_POC_FROZEN_HASH_PASS sha256='+digest)
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
  echo "FULLJ_TAGGED_POC: reusing isolated corrected CLASS dense-k64 environment..."
else
  echo "FULLJ_TAGGED_POC: preparing isolated corrected CLASS dense-k64 environment..."
  bash fullj_weyl/setup_corrected_class_dense_k64_local.sh
  # shellcheck disable=SC1090
  source "$ENVFILE"
fi

grep -Eq '^#define[[:space:]]+_MAX_NUMBER_OF_K_FILES_[[:space:]]+64[[:space:]]*$' \
  "$NL1C6D2N_CLASS_ROOT/include/perturbations.h"

python - <<'PY'
import os, numpy, scipy, classy
from classy import Class
print('FULLJ_TAGGED_POC_CLASS_KFILE_LIMIT_PASS value='+os.environ.get('FULLJ_DENSE_RESIDUAL_R2_CLASS_KFILE_LIMIT',''))
print('FULLJ_TAGGED_POC_ENV_PASS')
print('numpy='+numpy.__version__)
print('scipy='+scipy.__version__)
print('classy_module='+str(classy.__file__))
print('NL1C6D2N_CLASS_ROOT='+os.environ['NL1C6D2N_CLASS_ROOT'])
c=Class(); c.empty()
PY

JSON="results/fullj_stochastic_tagged_mode_poc.json"
NPZ="results/fullj_stochastic_tagged_mode_poc.npz"
CSV="results/fullj_stochastic_tagged_mode_poc.csv"
LOG="results/fullj_stochastic_tagged_mode_poc.log"
ZIP="results/fullj_stochastic_tagged_mode_poc_bundle.zip"
rm -f "$JSON" "$NPZ" "$CSV" "$LOG" "$ZIP"

export OMP_NUM_THREADS=1
unset AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE AEST_OFFLINE_TRACE_FILE AEST_TANGENT_ALLOW_K_MISS || true

set +e
python -u -m fullj_weyl.stochastic_tagged_mode_poc \
  --json-out "$JSON" --npz-out "$NPZ" --csv-out "$CSV" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

python - "$ZIP" "$LOG" "$JSON" "$NPZ" "$CSV" <<'PY'
from pathlib import Path
import sys, zipfile
zp=Path(sys.argv[1])
paths=[Path(x) for x in sys.argv[2:]] + [
    Path('docs/fullj_dense_radial_cardinality_audit_result.md'),
    Path('docs/fullj_stochastic_tagged_mode_poc_predata.md'),
    Path('fullj_weyl/stochastic_tagged_mode_poc.py'),
    Path('fullj_weyl/run_local_stochastic_tagged_mode_poc.sh'),
    Path('fullj_weyl/setup_corrected_class_dense_k64_local.sh'),
    Path('results/fullj_dense_radial_class_residual_r2.json'),
    Path('results/fullj_dense_radial_cardinality_audit.json'),
    Path('results/nl1c6d2n_corrected_class_densek64_env.sh'),
]
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED) as zf:
    seen=set()
    for p in paths:
        if p.exists() and p not in seen:
            zf.write(p,arcname=str(p)); seen.add(p)
print('FULLJ_TAGGED_POC_BUNDLE='+str(zp))
PY

echo "FULLJ_TAGGED_POC_EXIT=$code"
echo "FULLJ_TAGGED_POC_LOG=$LOG"
echo "FULLJ_TAGGED_POC_JSON=$JSON"
echo "FULLJ_TAGGED_POC_NPZ=$NPZ"
echo "FULLJ_TAGGED_POC_CSV=$CSV"
echo "FULLJ_TAGGED_POC_ZIP=$ZIP"
exit "$code"
