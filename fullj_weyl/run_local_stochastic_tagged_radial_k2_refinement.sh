#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

BASE_PY=""
if command -v python3 >/dev/null 2>&1; then BASE_PY="$(command -v python3)";
elif command -v python >/dev/null 2>&1; then BASE_PY="$(command -v python)";
else echo "FULLJ_TAGGED_K2: python missing" >&2; exit 2; fi

VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then
  "$BASE_PY" -m venv "$VENV" || { echo "FULLJ_TAGGED_K2: install python3-venv" >&2; exit 2; }
fi
export PATH="$VENV/bin:$PATH"
python -m pip install --upgrade pip setuptools wheel >/dev/null
python -m pip install numpy scipy cython >/dev/null

python -m py_compile \
  fullj_weyl/stochastic_tagged_radial_k2_refinement.py \
  fullj_weyl/stochastic_tagged_radial_convergence.py \
  fullj_weyl/stochastic_tagged_mode_poc.py \
  fullj_weyl/dense_radial_weyl_extension_r1.py \
  fullj_weyl/evolving_flrw_weyl_bridge_r2.py

for f in \
  results/fullj_stochastic_tagged_radial_convergence.json \
  results/fullj_stochastic_tagged_radial_convergence.npz \
  docs/fullj_stochastic_tagged_radial_convergence_result.md \
  docs/fullj_stochastic_tagged_radial_k2_refinement_predata.md \
  docs/fullj_evolving_weyl_history.md; do
  if [[ ! -f "$f" ]]; then
    echo "FULLJ_TAGGED_K2: missing required locked/local file $f" >&2
    exit 3
  fi
done

python - <<'PY'
import json
from pathlib import Path
import numpy as np
from fullj_weyl import stochastic_tagged_radial_k2_refinement as q
from fullj_weyl import stochastic_tagged_mode_poc as p

_,g,digest=p.coeff_draw()
assert digest==q.COEFF_HASH
assert q.B4==(0,1,2,3)
assert q.B2==(0,1)
assert q.EPS==0.05
assert q.KF_H==0.005 and q.NX==256 and q.NSTEP==4096
assert q.H2.tolist()==[0.035,0.045,0.055,0.07,0.085,0.095,0.11,0.135,0.16,0.185]
assert q.K2.tolist()==[0.03,0.035,0.04,0.045,0.05,0.055,0.065,0.07,0.08,0.085,0.09,0.095,0.1,0.11,0.125,0.135,0.15,0.16,0.175,0.185,0.2]
meta=json.loads(Path('results/fullj_stochastic_tagged_radial_convergence.json').read_text())
assert meta['classification']=='FULLJ_STOCHASTIC_TAGGED_RADIAL_CONVERGENCE_FAIL'
assert meta['gates']['STR_G7_direct_K0_to_K1_holdout_accuracy'] is False
assert meta['gates']['STR_G8_K0_to_K1_continuous_radial_convergence'] is False
z=np.load('results/fullj_stochastic_tagged_radial_convergence.npz')
assert z['response'].shape==(4,11,9)
assert np.allclose(z['K1'],q.K1,rtol=0,atol=5e-14)
print('FULLJ_TAGGED_K2_IMPORT_CHAIN_PASS')
print('FULLJ_TAGGED_K2_LOCKED_K1_PASS')
print('FULLJ_TAGGED_K2_FROZEN_HASH_PASS sha256='+digest)
print('FULLJ_TAGGED_K2_GRID_PASS K1=11 H2=10 K2=21 kF_h=0.005 NX=256')
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
  echo "FULLJ_TAGGED_K2: reusing isolated corrected CLASS dense-k64 environment..."
else
  echo "FULLJ_TAGGED_K2: preparing isolated corrected CLASS dense-k64 environment..."
  bash fullj_weyl/setup_corrected_class_dense_k64_local.sh
  # shellcheck disable=SC1090
  source "$ENVFILE"
fi

grep -Eq '^#define[[:space:]]+_MAX_NUMBER_OF_K_FILES_[[:space:]]+64[[:space:]]*$' \
  "$NL1C6D2N_CLASS_ROOT/include/perturbations.h"

python - <<'PY'
import os, numpy, scipy, classy
from classy import Class
print('FULLJ_TAGGED_K2_CLASS_KFILE_LIMIT_PASS value='+os.environ.get('FULLJ_DENSE_RESIDUAL_R2_CLASS_KFILE_LIMIT',''))
print('FULLJ_TAGGED_K2_ENV_PASS')
print('numpy='+numpy.__version__)
print('scipy='+scipy.__version__)
print('classy_module='+str(classy.__file__))
print('NL1C6D2N_CLASS_ROOT='+os.environ['NL1C6D2N_CLASS_ROOT'])
c=Class(); c.empty()
PY

JSON="results/fullj_stochastic_tagged_radial_k2_refinement.json"
NPZ="results/fullj_stochastic_tagged_radial_k2_refinement.npz"
CSV="results/fullj_stochastic_tagged_radial_k2_refinement.csv"
LOG="results/fullj_stochastic_tagged_radial_k2_refinement.log"
ZIP="results/fullj_stochastic_tagged_radial_k2_refinement_bundle.zip"
rm -f "$JSON" "$NPZ" "$CSV" "$LOG" "$ZIP"

export OMP_NUM_THREADS=1
unset AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE AEST_OFFLINE_TRACE_FILE AEST_TANGENT_ALLOW_K_MISS || true

set +e
python -u -m fullj_weyl.stochastic_tagged_radial_k2_refinement \
  --json-out "$JSON" --npz-out "$NPZ" --csv-out "$CSV" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

python - "$ZIP" "$LOG" "$JSON" "$NPZ" "$CSV" <<'PY'
from pathlib import Path
import sys, zipfile
zp=Path(sys.argv[1])
paths=[Path(x) for x in sys.argv[2:]] + [
    Path('docs/fullj_evolving_weyl_history.md'),
    Path('docs/fullj_stochastic_tagged_radial_convergence_result.md'),
    Path('docs/fullj_stochastic_tagged_radial_k2_refinement_predata.md'),
    Path('fullj_weyl/stochastic_tagged_radial_k2_refinement.py'),
    Path('fullj_weyl/run_local_stochastic_tagged_radial_k2_refinement.sh'),
    Path('fullj_weyl/stochastic_tagged_radial_convergence.py'),
    Path('fullj_weyl/stochastic_tagged_mode_poc.py'),
    Path('fullj_weyl/setup_corrected_class_dense_k64_local.sh'),
    Path('results/fullj_stochastic_tagged_radial_convergence.json'),
    Path('results/fullj_stochastic_tagged_radial_convergence.npz'),
    Path('results/nl1c6d2n_corrected_class_densek64_env.sh'),
]
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED) as zf:
    seen=set()
    for p in paths:
        if p.exists() and p not in seen:
            zf.write(p,arcname=str(p)); seen.add(p)
print('FULLJ_TAGGED_K2_BUNDLE='+str(zp))
PY

echo "FULLJ_TAGGED_K2_EXIT=$code"
echo "FULLJ_TAGGED_K2_LOG=$LOG"
echo "FULLJ_TAGGED_K2_JSON=$JSON"
echo "FULLJ_TAGGED_K2_NPZ=$NPZ"
echo "FULLJ_TAGGED_K2_CSV=$CSV"
echo "FULLJ_TAGGED_K2_ZIP=$ZIP"
exit "$code"
