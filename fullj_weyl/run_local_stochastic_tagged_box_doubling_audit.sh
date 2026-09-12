#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

BASE_PY=""
if command -v python3 >/dev/null 2>&1; then BASE_PY="$(command -v python3)";
elif command -v python >/dev/null 2>&1; then BASE_PY="$(command -v python)";
else echo "FULLJ_BOX_AUDIT: python missing" >&2; exit 2; fi

VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then
  "$BASE_PY" -m venv "$VENV" || { echo "FULLJ_BOX_AUDIT: install python3-venv" >&2; exit 2; }
fi
export PATH="$VENV/bin:$PATH"
python -m pip install --upgrade pip setuptools wheel >/dev/null
python -m pip install numpy scipy cython >/dev/null

python -m py_compile \
  fullj_weyl/stochastic_tagged_box_doubling_audit.py \
  fullj_weyl/stochastic_tagged_power_lattice.py \
  fullj_weyl/stochastic_response_kernel_poc.py \
  fullj_weyl/stochastic_tagged_mode_poc.py

for f in \
  results/fullj_stochastic_tagged_power_lattice.json \
  results/fullj_stochastic_tagged_power_lattice.npz \
  docs/fullj_stochastic_tagged_power_lattice_result.md \
  docs/fullj_evolving_weyl_history_power_lattice_addendum.md \
  docs/fullj_stochastic_tagged_box_doubling_audit_predata.md; do
  if [[ ! -f "$f" ]]; then
    echo "FULLJ_BOX_AUDIT: missing required locked/local file $f" >&2
    exit 3
  fi
done

python - <<'PY'
import json
from pathlib import Path
import numpy as np
from fullj_weyl import stochastic_tagged_box_doubling_audit as q
from fullj_weyl import stochastic_tagged_mode_poc as p

_,_,digest=p.coeff_draw()
assert digest==q.COEFF_HASH
assert q.B2==(0,1)
assert np.allclose(q.AUDIT_K,[0.030,0.060,0.095,0.100,0.120,0.160,0.195,0.200],rtol=0,atol=5e-14)
assert q.EPS==0.05 and q.NSTEP==4096
assert q.KF_A==0.005 and q.NX_A==256
assert q.KF_B==0.0025 and q.NX_B==512
meta=json.loads(Path('results/fullj_stochastic_tagged_power_lattice.json').read_text())
assert meta['classification']=='FULLJ_STOCHASTIC_TAGGED_POWER_LATTICE_FAIL'
g=meta['gates']
for k in ['PL_G1_provenance_and_frozen_identity','PL_G2_stageA_solver_constraint_health','PL_G3_stageA_broadband_saturated_closure','PL_G4_complete_lattice_algebra_background_sanity','PL_G5_stageB_solver_constraint_saturation_health']:
    assert g[k] is True
for k in ['PL_G6_power_half_lattice_interpolation_accuracy','PL_G7_no_unresolved_selected_interval_power_spike']:
    assert g[k] is False
print('FULLJ_BOX_AUDIT_IMPORT_CHAIN_PASS')
print('FULLJ_BOX_AUDIT_LOCAL_LOCKS_PASS')
print('FULLJ_BOX_AUDIT_FROZEN_HASH_PASS sha256='+digest)
print('FULLJ_BOX_AUDIT_GRID_PASS nodes=8 backgrounds=2 signs=2 total_runs=32 kF_A_h=0.005 NX_A=256 kF_B_h=0.0025 NX_B=512')
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
  echo "FULLJ_BOX_AUDIT: reusing isolated corrected CLASS dense-k64 environment..."
else
  echo "FULLJ_BOX_AUDIT: preparing isolated corrected CLASS dense-k64 environment..."
  bash fullj_weyl/setup_corrected_class_dense_k64_local.sh
  # shellcheck disable=SC1090
  source "$ENVFILE"
fi

grep -Eq '^#define[[:space:]]+_MAX_NUMBER_OF_K_FILES_[[:space:]]+64[[:space:]]*$' \
  "$NL1C6D2N_CLASS_ROOT/include/perturbations.h"

python - <<'PY'
import os, numpy, scipy, classy
from classy import Class
print('FULLJ_BOX_AUDIT_CLASS_KFILE_LIMIT_PASS value='+os.environ.get('FULLJ_DENSE_RESIDUAL_R2_CLASS_KFILE_LIMIT',''))
print('FULLJ_BOX_AUDIT_ENV_PASS')
print('numpy='+numpy.__version__)
print('scipy='+scipy.__version__)
print('classy_module='+str(classy.__file__))
print('NL1C6D2N_CLASS_ROOT='+os.environ['NL1C6D2N_CLASS_ROOT'])
c=Class(); c.empty()
PY

JSON="results/fullj_stochastic_tagged_box_doubling_audit.json"
NPZ="results/fullj_stochastic_tagged_box_doubling_audit.npz"
CSV="results/fullj_stochastic_tagged_box_doubling_audit.csv"
LOG="results/fullj_stochastic_tagged_box_doubling_audit.log"
ZIP="results/fullj_stochastic_tagged_box_doubling_audit_bundle.zip"
rm -f "$JSON" "$NPZ" "$CSV" "$LOG" "$ZIP"

export OMP_NUM_THREADS=1
unset AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE AEST_OFFLINE_TRACE_FILE AEST_TANGENT_ALLOW_K_MISS || true

set +e
python -u -m fullj_weyl.stochastic_tagged_box_doubling_audit \
  --json-out "$JSON" --npz-out "$NPZ" --csv-out "$CSV" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

python - "$ZIP" "$LOG" "$JSON" "$NPZ" "$CSV" <<'PY'
from pathlib import Path
import sys, zipfile
zp=Path(sys.argv[1])
paths=[Path(x) for x in sys.argv[2:]] + [
    Path('docs/fullj_stochastic_tagged_box_doubling_audit_predata.md'),
    Path('docs/fullj_stochastic_tagged_power_lattice_result.md'),
    Path('docs/fullj_evolving_weyl_history_power_lattice_addendum.md'),
    Path('fullj_weyl/stochastic_tagged_box_doubling_audit.py'),
    Path('fullj_weyl/run_local_stochastic_tagged_box_doubling_audit.sh'),
    Path('fullj_weyl/stochastic_tagged_power_lattice.py'),
    Path('results/fullj_stochastic_tagged_power_lattice.json'),
    Path('results/fullj_stochastic_tagged_power_lattice.npz'),
    Path('results/nl1c6d2n_corrected_class_densek64_env.sh'),
]
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED) as zf:
    seen=set()
    for p in paths:
        if p.exists() and p not in seen:
            zf.write(p,arcname=str(p)); seen.add(p)
print('FULLJ_BOX_AUDIT_BUNDLE='+str(zp))
PY

echo "FULLJ_BOX_AUDIT_EXIT=$code"
echo "FULLJ_BOX_AUDIT_LOG=$LOG"
echo "FULLJ_BOX_AUDIT_JSON=$JSON"
echo "FULLJ_BOX_AUDIT_NPZ=$NPZ"
echo "FULLJ_BOX_AUDIT_CSV=$CSV"
echo "FULLJ_BOX_AUDIT_ZIP=$ZIP"
exit "$code"
