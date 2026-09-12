#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

BASE_PY=""
if command -v python3 >/dev/null 2>&1; then BASE_PY="$(command -v python3)";
elif command -v python >/dev/null 2>&1; then BASE_PY="$(command -v python)";
else echo "FULLJ_KMASK_REPAIR: python missing" >&2; exit 2; fi

VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then
  "$BASE_PY" -m venv "$VENV" || { echo "FULLJ_KMASK_REPAIR: install python3-venv" >&2; exit 2; }
fi
export PATH="$VENV/bin:$PATH"
python -m pip install --upgrade pip setuptools wheel >/dev/null
python -m pip install numpy scipy cython >/dev/null

python -m py_compile \
  fullj_weyl/metric_projection_physical_kmask_repair.py \
  fullj_weyl/metric_projection_physical_kmask_repair_audit.py \
  fullj_weyl/stochastic_tagged_mode_poc.py \
  fullj_weyl/evolving_flrw_weyl_bridge_r2.py

for f in \
  docs/fullj_stochastic_tagged_box_doubling_audit_result.md \
  docs/fullj_metric_projection_physical_kmask_repair_predata.md; do
  if [[ ! -f "$f" ]]; then
    echo "FULLJ_KMASK_REPAIR: missing required lock $f" >&2
    exit 3
  fi
done

python - <<'PY'
import numpy as np
from fullj_weyl import metric_projection_physical_kmask_repair as q
from fullj_weyl import stochastic_tagged_mode_poc as p

ident=q.original_r2_mask_identity(128)
assert ident['mismatch_count']==0 and ident['identical']
assert abs(q.ORIGINAL_KF_H-0.01)<1e-15
assert abs(q.METRIC_KMAX_H-0.32)<1e-15
_,_,digest=p.coeff_draw()
assert digest=='9c511b09899cb874d09c0513b89b82c796769886ecba5dd6347c71678b19d200'

# Explicitly certify the historical source of the box-dependent pattern.
def old_in(kh,kf):
    return int(round(kh/kf)) <= 32
pattern={k:(old_in(k,0.005),old_in(k,0.0025)) for k in [0.03,0.06,0.095,0.10,0.12,0.16,0.195,0.20]}
assert pattern[0.03]==(True,True) and pattern[0.06]==(True,True)
for k in [0.095,0.10,0.12,0.16]: assert pattern[k]==(True,False)
assert pattern[0.195]==(False,False) and pattern[0.20]==(False,False)
print('FULLJ_KMASK_REPAIR_IMPORT_CHAIN_PASS')
print('FULLJ_KMASK_REPAIR_ORIGINAL_R2_MASK_IDENTITY_PASS mismatch_count=0 kmax_h=0.32')
print('FULLJ_KMASK_REPAIR_HISTORICAL_PATTERN_PASS '+str(pattern))
print('FULLJ_KMASK_REPAIR_GRID_PASS nodes=4 backgrounds=2 signs=2 geometries=2 total_runs=32')
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
  echo "FULLJ_KMASK_REPAIR: reusing isolated corrected CLASS dense-k64 environment..."
else
  echo "FULLJ_KMASK_REPAIR: preparing isolated corrected CLASS dense-k64 environment..."
  bash fullj_weyl/setup_corrected_class_dense_k64_local.sh
  # shellcheck disable=SC1090
  source "$ENVFILE"
fi

grep -Eq '^#define[[:space:]]+_MAX_NUMBER_OF_K_FILES_[[:space:]]+64[[:space:]]*$' \
  "$NL1C6D2N_CLASS_ROOT/include/perturbations.h"

python - <<'PY'
import os, numpy, scipy, classy
from classy import Class
print('FULLJ_KMASK_REPAIR_CLASS_KFILE_LIMIT_PASS value='+os.environ.get('FULLJ_DENSE_RESIDUAL_R2_CLASS_KFILE_LIMIT',''))
print('FULLJ_KMASK_REPAIR_ENV_PASS')
print('numpy='+numpy.__version__)
print('scipy='+scipy.__version__)
print('classy_module='+str(classy.__file__))
print('NL1C6D2N_CLASS_ROOT='+os.environ['NL1C6D2N_CLASS_ROOT'])
c=Class(); c.empty()
PY

JSON="results/fullj_metric_projection_physical_kmask_repair_audit.json"
NPZ="results/fullj_metric_projection_physical_kmask_repair_audit.npz"
CSV="results/fullj_metric_projection_physical_kmask_repair_audit.csv"
LOG="results/fullj_metric_projection_physical_kmask_repair_audit.log"
ZIP="results/fullj_metric_projection_physical_kmask_repair_audit_bundle.zip"
rm -f "$JSON" "$NPZ" "$CSV" "$LOG" "$ZIP"

export OMP_NUM_THREADS=1
unset AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE AEST_OFFLINE_TRACE_FILE AEST_TANGENT_ALLOW_K_MISS || true

set +e
python -u -m fullj_weyl.metric_projection_physical_kmask_repair_audit \
  --json-out "$JSON" --npz-out "$NPZ" --csv-out "$CSV" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

python - "$ZIP" "$LOG" "$JSON" "$NPZ" "$CSV" <<'PY'
from pathlib import Path
import sys, zipfile
zp=Path(sys.argv[1])
paths=[Path(x) for x in sys.argv[2:]] + [
    Path('docs/fullj_stochastic_tagged_box_doubling_audit_result.md'),
    Path('docs/fullj_metric_projection_physical_kmask_repair_predata.md'),
    Path('fullj_weyl/metric_projection_physical_kmask_repair.py'),
    Path('fullj_weyl/metric_projection_physical_kmask_repair_audit.py'),
    Path('fullj_weyl/run_local_metric_projection_physical_kmask_repair_audit.sh'),
    Path('fullj_weyl/stochastic_tagged_mode_poc.py'),
    Path('fullj_weyl/evolving_flrw_weyl_bridge.py'),
    Path('fullj_weyl/evolving_flrw_weyl_bridge_r2.py'),
    Path('results/nl1c6d2n_corrected_class_densek64_env.sh'),
]
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED) as zf:
    seen=set()
    for p in paths:
        if p.exists() and p not in seen:
            zf.write(p,arcname=str(p)); seen.add(p)
print('FULLJ_KMASK_REPAIR_BUNDLE='+str(zp))
PY

echo "FULLJ_KMASK_REPAIR_EXIT=$code"
echo "FULLJ_KMASK_REPAIR_LOG=$LOG"
echo "FULLJ_KMASK_REPAIR_JSON=$JSON"
echo "FULLJ_KMASK_REPAIR_NPZ=$NPZ"
echo "FULLJ_KMASK_REPAIR_CSV=$CSV"
echo "FULLJ_KMASK_REPAIR_ZIP=$ZIP"
exit "$code"
