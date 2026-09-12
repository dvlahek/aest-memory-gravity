#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

BASE_PY=""
if command -v python3 >/dev/null 2>&1; then BASE_PY="$(command -v python3)";
elif command -v python >/dev/null 2>&1; then BASE_PY="$(command -v python)";
else echo "FULLJ_RESPONSE_KERNEL: python missing" >&2; exit 2; fi

VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then
  "$BASE_PY" -m venv "$VENV" || { echo "FULLJ_RESPONSE_KERNEL: install python3-venv" >&2; exit 2; }
fi
export PATH="$VENV/bin:$PATH"
python -m pip install --upgrade pip setuptools wheel >/dev/null
python -m pip install numpy scipy cython >/dev/null

python -m py_compile \
  fullj_weyl/stochastic_response_kernel_poc.py \
  fullj_weyl/stochastic_tagged_radial_k2_refinement.py \
  fullj_weyl/stochastic_tagged_radial_convergence.py \
  fullj_weyl/stochastic_tagged_mode_poc.py

for f in \
  results/fullj_stochastic_tagged_radial_k2_refinement.json \
  results/fullj_stochastic_tagged_radial_k2_refinement.npz \
  docs/fullj_stochastic_tagged_radial_k2_refinement_result.md \
  docs/fullj_stochastic_response_kernel_poc_predata.md \
  docs/fullj_evolving_weyl_history.md; do
  if [[ ! -f "$f" ]]; then
    echo "FULLJ_RESPONSE_KERNEL: missing required locked/local file $f" >&2
    exit 3
  fi
done

python - <<'PY'
import json
from pathlib import Path
import numpy as np
from fullj_weyl import stochastic_response_kernel_poc as q
from fullj_weyl import stochastic_tagged_mode_poc as p

_,_,digest=p.coeff_draw()
assert digest==q.COEFF_HASH
assert q.B4==(0,1,2,3) and q.B2==(0,1)
assert np.allclose(q.INPUTS,[0.095,0.110,0.135,0.160,0.185],rtol=0,atol=5e-14)
assert q.EPS==0.05 and q.EPS_HALF==0.025
assert q.KF_H==0.005 and q.NX==256 and q.NX_HI==512 and q.NSTEP==4096
assert q.NOUT==127 and q.BOUND_N_MIN==6 and q.BOUND_N_MAX==40
meta=json.loads(Path('results/fullj_stochastic_tagged_radial_k2_refinement.json').read_text())
assert meta['classification']=='FULLJ_STOCHASTIC_TAGGED_RADIAL_K2_REFINEMENT_FAIL'
g=meta['gates']
for k in ['K2_G1_provenance_and_locked_K1_identity','K2_G2_all_80_new_runs_finite_constraint_clean','K2_G3_broadband_saturated_closure','K2_G4_tagged_response_power_algebra','K2_G5_new_node_background_convergence_B2_to_B4','K2_G9_refinement_improves_every_redshift']:
    assert g[k] is True
for k in ['K2_G6_direct_K1_to_K2_holdout_accuracy','K2_G7_continuous_K1_to_K2_radial_convergence','K2_G8_direct_radial_smoothness_spike_veto']:
    assert g[k] is False
print('FULLJ_RESPONSE_KERNEL_IMPORT_CHAIN_PASS')
print('FULLJ_RESPONSE_KERNEL_LOCAL_LOCKS_PASS')
print('FULLJ_RESPONSE_KERNEL_FROZEN_HASH_PASS sha256='+digest)
print('FULLJ_RESPONSE_KERNEL_GRID_PASS inputs=5 backgrounds=4 primary_runs=40 total_runs=44 kF_h=0.005 NX=256 NX_HI=512')
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
  echo "FULLJ_RESPONSE_KERNEL: reusing isolated corrected CLASS dense-k64 environment..."
else
  echo "FULLJ_RESPONSE_KERNEL: preparing isolated corrected CLASS dense-k64 environment..."
  bash fullj_weyl/setup_corrected_class_dense_k64_local.sh
  # shellcheck disable=SC1090
  source "$ENVFILE"
fi

grep -Eq '^#define[[:space:]]+_MAX_NUMBER_OF_K_FILES_[[:space:]]+64[[:space:]]*$' \
  "$NL1C6D2N_CLASS_ROOT/include/perturbations.h"

python - <<'PY'
import os, numpy, scipy, classy
from classy import Class
print('FULLJ_RESPONSE_KERNEL_CLASS_KFILE_LIMIT_PASS value='+os.environ.get('FULLJ_DENSE_RESIDUAL_R2_CLASS_KFILE_LIMIT',''))
print('FULLJ_RESPONSE_KERNEL_ENV_PASS')
print('numpy='+numpy.__version__)
print('scipy='+scipy.__version__)
print('classy_module='+str(classy.__file__))
print('NL1C6D2N_CLASS_ROOT='+os.environ['NL1C6D2N_CLASS_ROOT'])
c=Class(); c.empty()
PY

JSON="results/fullj_stochastic_response_kernel_poc.json"
NPZ="results/fullj_stochastic_response_kernel_poc.npz"
CSV="results/fullj_stochastic_response_kernel_poc.csv"
LOG="results/fullj_stochastic_response_kernel_poc.log"
ZIP="results/fullj_stochastic_response_kernel_poc_bundle.zip"
rm -f "$JSON" "$NPZ" "$CSV" "$LOG" "$ZIP"

export OMP_NUM_THREADS=1
unset AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE AEST_OFFLINE_TRACE_FILE AEST_TANGENT_ALLOW_K_MISS || true

set +e
python -u -m fullj_weyl.stochastic_response_kernel_poc \
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
    Path('docs/fullj_stochastic_response_kernel_poc_predata.md'),
    Path('fullj_weyl/stochastic_response_kernel_poc.py'),
    Path('fullj_weyl/run_local_stochastic_response_kernel_poc.sh'),
    Path('fullj_weyl/stochastic_tagged_mode_poc.py'),
    Path('fullj_weyl/stochastic_tagged_radial_k2_refinement.py'),
    Path('fullj_weyl/setup_corrected_class_dense_k64_local.sh'),
    Path('results/fullj_stochastic_tagged_radial_k2_refinement.json'),
    Path('results/fullj_stochastic_tagged_radial_k2_refinement.npz'),
    Path('results/nl1c6d2n_corrected_class_densek64_env.sh'),
]
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED) as zf:
    seen=set()
    for p in paths:
        if p.exists() and p not in seen:
            zf.write(p,arcname=str(p)); seen.add(p)
print('FULLJ_RESPONSE_KERNEL_BUNDLE='+str(zp))
PY

echo "FULLJ_RESPONSE_KERNEL_EXIT=$code"
echo "FULLJ_RESPONSE_KERNEL_LOG=$LOG"
echo "FULLJ_RESPONSE_KERNEL_JSON=$JSON"
echo "FULLJ_RESPONSE_KERNEL_NPZ=$NPZ"
echo "FULLJ_RESPONSE_KERNEL_CSV=$CSV"
echo "FULLJ_RESPONSE_KERNEL_ZIP=$ZIP"
exit "$code"
