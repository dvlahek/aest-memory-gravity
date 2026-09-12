#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

BASE_PY=""
if command -v python3 >/dev/null 2>&1; then BASE_PY="$(command -v python3)";
elif command -v python >/dev/null 2>&1; then BASE_PY="$(command -v python)";
else echo "FULLJ_POWER_LATTICE: python missing" >&2; exit 2; fi

VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then
  "$BASE_PY" -m venv "$VENV" || { echo "FULLJ_POWER_LATTICE: install python3-venv" >&2; exit 2; }
fi
export PATH="$VENV/bin:$PATH"
python -m pip install --upgrade pip setuptools wheel >/dev/null
python -m pip install numpy scipy cython >/dev/null

python -m py_compile \
  fullj_weyl/stochastic_tagged_power_lattice.py \
  fullj_weyl/stochastic_response_kernel_poc.py \
  fullj_weyl/stochastic_tagged_radial_k2_refinement.py \
  fullj_weyl/stochastic_tagged_radial_convergence.py \
  fullj_weyl/stochastic_tagged_mode_poc.py

for f in \
  results/fullj_stochastic_tagged_radial_k2_refinement.json \
  results/fullj_stochastic_tagged_radial_k2_refinement.npz \
  results/fullj_stochastic_response_kernel_poc.json \
  docs/fullj_stochastic_tagged_radial_k2_refinement_result.md \
  docs/fullj_stochastic_response_kernel_poc_result.md \
  docs/fullj_stochastic_tagged_power_lattice_predata.md \
  docs/fullj_evolving_weyl_history.md; do
  if [[ ! -f "$f" ]]; then
    echo "FULLJ_POWER_LATTICE: missing required locked/local file $f" >&2
    exit 3
  fi
done

python - <<'PY'
import json
from pathlib import Path
import numpy as np
from fullj_weyl import stochastic_tagged_power_lattice as q
from fullj_weyl import stochastic_tagged_mode_poc as p

_,_,digest=p.coeff_draw()
assert digest==q.COEFF_HASH
assert q.B4==(0,1,2,3) and q.B2==(0,1)
assert q.EPS==0.05 and q.NSTEP==4096
assert q.KF_A==0.005 and q.NX_A==256
assert q.KF_B==0.0025 and q.NX_B==512
assert len(q.KFULL)==35 and len(q.HMISS)==14 and q.N_HALF==16
assert np.allclose(q.FIXED_HALF,[0.0325,0.0625,0.0925,0.1225,0.1625,0.1975],rtol=0,atol=5e-14)
km=json.loads(Path('results/fullj_stochastic_response_kernel_poc.json').read_text())
assert km['classification']=='FULLJ_STOCHASTIC_RESPONSE_KERNEL_POC_PASS'
assert km['STOCHASTIC_SCALAR_DIAGONAL_REDUCTION_SUPPORTED'] is True
assert km['STOCHASTIC_MODE_COUPLING_KERNEL_REQUIRED'] is False
k2=json.loads(Path('results/fullj_stochastic_tagged_radial_k2_refinement.json').read_text())
assert k2['classification']=='FULLJ_STOCHASTIC_TAGGED_RADIAL_K2_REFINEMENT_FAIL'
print('FULLJ_POWER_LATTICE_IMPORT_CHAIN_PASS')
print('FULLJ_POWER_LATTICE_LOCAL_LOCKS_PASS')
print('FULLJ_POWER_LATTICE_FROZEN_HASH_PASS sha256='+digest)
print('FULLJ_POWER_LATTICE_GRID_PASS full_nodes=35 missing_nodes=14 half_controls=16 stageA_runs=112 stageB_runs=64 total_runs=176')
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
  echo "FULLJ_POWER_LATTICE: reusing isolated corrected CLASS dense-k64 environment..."
else
  echo "FULLJ_POWER_LATTICE: preparing isolated corrected CLASS dense-k64 environment..."
  bash fullj_weyl/setup_corrected_class_dense_k64_local.sh
  # shellcheck disable=SC1090
  source "$ENVFILE"
fi

grep -Eq '^#define[[:space:]]+_MAX_NUMBER_OF_K_FILES_[[:space:]]+64[[:space:]]*$' \
  "$NL1C6D2N_CLASS_ROOT/include/perturbations.h"

python - <<'PY'
import os, numpy, scipy, classy
from classy import Class
print('FULLJ_POWER_LATTICE_CLASS_KFILE_LIMIT_PASS value='+os.environ.get('FULLJ_DENSE_RESIDUAL_R2_CLASS_KFILE_LIMIT',''))
print('FULLJ_POWER_LATTICE_ENV_PASS')
print('numpy='+numpy.__version__)
print('scipy='+scipy.__version__)
print('classy_module='+str(classy.__file__))
print('NL1C6D2N_CLASS_ROOT='+os.environ['NL1C6D2N_CLASS_ROOT'])
c=Class(); c.empty()
PY

JSON="results/fullj_stochastic_tagged_power_lattice.json"
NPZ="results/fullj_stochastic_tagged_power_lattice.npz"
CSV="results/fullj_stochastic_tagged_power_lattice.csv"
LOG="results/fullj_stochastic_tagged_power_lattice.log"
ZIP="results/fullj_stochastic_tagged_power_lattice_bundle.zip"
rm -f "$JSON" "$NPZ" "$CSV" "$LOG" "$ZIP"

export OMP_NUM_THREADS=1
unset AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE AEST_OFFLINE_TRACE_FILE AEST_TANGENT_ALLOW_K_MISS || true

set +e
python -u -m fullj_weyl.stochastic_tagged_power_lattice \
  --json-out "$JSON" --npz-out "$NPZ" --csv-out "$CSV" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

python - "$ZIP" "$LOG" "$JSON" "$NPZ" "$CSV" <<'PY'
from pathlib import Path
import sys, zipfile
zp=Path(sys.argv[1])
paths=[Path(x) for x in sys.argv[2:]] + [
    Path('docs/fullj_evolving_weyl_history.md'),
    Path('docs/fullj_stochastic_tagged_radial_k2_refinement_result.md'),
    Path('docs/fullj_stochastic_response_kernel_poc_result.md'),
    Path('docs/fullj_stochastic_tagged_power_lattice_predata.md'),
    Path('fullj_weyl/stochastic_tagged_power_lattice.py'),
    Path('fullj_weyl/run_local_stochastic_tagged_power_lattice.sh'),
    Path('fullj_weyl/stochastic_response_kernel_poc.py'),
    Path('fullj_weyl/stochastic_tagged_radial_k2_refinement.py'),
    Path('fullj_weyl/stochastic_tagged_mode_poc.py'),
    Path('fullj_weyl/setup_corrected_class_dense_k64_local.sh'),
    Path('results/fullj_stochastic_tagged_radial_k2_refinement.json'),
    Path('results/fullj_stochastic_tagged_radial_k2_refinement.npz'),
    Path('results/fullj_stochastic_response_kernel_poc.json'),
    Path('results/nl1c6d2n_corrected_class_densek64_env.sh'),
]
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED) as zf:
    seen=set()
    for p in paths:
        if p.exists() and p not in seen:
            zf.write(p,arcname=str(p)); seen.add(p)
print('FULLJ_POWER_LATTICE_BUNDLE='+str(zp))
PY

echo "FULLJ_POWER_LATTICE_EXIT=$code"
echo "FULLJ_POWER_LATTICE_LOG=$LOG"
echo "FULLJ_POWER_LATTICE_JSON=$JSON"
echo "FULLJ_POWER_LATTICE_NPZ=$NPZ"
echo "FULLJ_POWER_LATTICE_CSV=$CSV"
echo "FULLJ_POWER_LATTICE_ZIP=$ZIP"
exit "$code"
