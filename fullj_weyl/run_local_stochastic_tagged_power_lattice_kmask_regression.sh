#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

BASE_PY=""
if command -v python3 >/dev/null 2>&1; then BASE_PY="$(command -v python3)";
elif command -v python >/dev/null 2>&1; then BASE_PY="$(command -v python)";
else echo "FULLJ_POWER_KMASK_REG: python missing" >&2; exit 2; fi

VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then
  "$BASE_PY" -m venv "$VENV" || { echo "FULLJ_POWER_KMASK_REG: install python3-venv" >&2; exit 2; }
fi
export PATH="$VENV/bin:$PATH"
python -m pip install --upgrade pip setuptools wheel >/dev/null
python -m pip install numpy scipy cython >/dev/null

python -m py_compile \
  fullj_weyl/stochastic_tagged_power_lattice_kmask_regression.py \
  fullj_weyl/stochastic_tagged_power_lattice_kmask_regression_r1.py \
  fullj_weyl/metric_projection_physical_kmask_repair.py \
  fullj_weyl/stochastic_tagged_power_lattice.py \
  fullj_weyl/stochastic_tagged_mode_poc.py \
  fullj_weyl/evolving_flrw_weyl_bridge_r2.py

for f in \
  docs/fullj_stochastic_tagged_power_lattice_kmask_regression_predata.md \
  docs/fullj_metric_projection_physical_kmask_repair_result.md \
  results/fullj_stochastic_tagged_power_lattice.json \
  results/fullj_stochastic_tagged_power_lattice.npz \
  results/fullj_metric_projection_physical_kmask_repair_audit.json; do
  if [[ ! -f "$f" ]]; then
    echo "FULLJ_POWER_KMASK_REG: missing required lock/input $f" >&2
    exit 3
  fi
done

python - <<'PY'
import json
from pathlib import Path
from fullj_weyl import stochastic_tagged_power_lattice_kmask_regression_r1 as q
from fullj_weyl import metric_projection_physical_kmask_repair as km

assert q.mod.PREDATA_LOCK == 'dde7ae43d974451b49f73df7473025812e906e83'
assert q.PREDATA_LOCK_CORRECTION_ONLY is True
assert km.REPAIR_ACTIVE is True
ident=km.original_r2_mask_identity(128)
assert ident['identical'] and ident['mismatch_count']==0
assert abs(km.METRIC_KMAX_H-0.32)<1e-15
assert len(q.mod.K_OVERLAP)*2*2 == 12
assert len(q.mod.K_REPAIR)*2*2 == 32
assert q.mod.pl.N_HALF*2*2 == 64
assert 12+32+64 == 108

hist=json.loads(Path('results/fullj_stochastic_tagged_power_lattice.json').read_text())
assert hist['classification']=='FULLJ_STOCHASTIC_TAGGED_POWER_LATTICE_FAIL'
for k in ['PL_G1_provenance_and_frozen_identity','PL_G2_stageA_solver_constraint_health','PL_G3_stageA_broadband_saturated_closure','PL_G4_complete_lattice_algebra_background_sanity','PL_G5_stageB_solver_constraint_saturation_health']:
    assert hist['gates'][k] is True
for k in ['PL_G6_power_half_lattice_interpolation_accuracy','PL_G7_no_unresolved_selected_interval_power_spike']:
    assert hist['gates'][k] is False
rep=json.loads(Path('results/fullj_metric_projection_physical_kmask_repair_audit.json').read_text())
assert rep['classification']=='FULLJ_METRIC_PROJECTION_PHYSICAL_KMASK_REPAIR_PASS'
assert all(rep['gates'].values())
assert rep['METRIC_PROJECTION_PHYSICAL_KMASK_REPAIR_VALIDATED'] is True
assert rep['STOCHASTIC_TAGGED_BOX_DOUBLING_INVARIANCE_REPAIRED'] is True
print('FULLJ_POWER_KMASK_REG_IMPORT_CHAIN_PASS')
print('FULLJ_POWER_KMASK_REG_LOCKS_PASS historical_PL=FAIL repair=PASS')
print('FULLJ_POWER_KMASK_REG_GRID_PASS stageA_overlap=12 stageA_repair=32 stageB=64 total=108')
print('FULLJ_POWER_KMASK_REG_PHYSICAL_MASK_PASS kmax_h=0.32 mismatch_count=0')
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
  echo "FULLJ_POWER_KMASK_REG: reusing isolated corrected CLASS dense-k64 environment..."
else
  echo "FULLJ_POWER_KMASK_REG: preparing isolated corrected CLASS dense-k64 environment..."
  bash fullj_weyl/setup_corrected_class_dense_k64_local.sh
  # shellcheck disable=SC1090
  source "$ENVFILE"
fi

grep -Eq '^#define[[:space:]]+_MAX_NUMBER_OF_K_FILES_[[:space:]]+64[[:space:]]*$' \
  "$NL1C6D2N_CLASS_ROOT/include/perturbations.h"

python - <<'PY'
import os, numpy, scipy, classy
from classy import Class
print('FULLJ_POWER_KMASK_REG_CLASS_KFILE_LIMIT_PASS value='+os.environ.get('FULLJ_DENSE_RESIDUAL_R2_CLASS_KFILE_LIMIT',''))
print('FULLJ_POWER_KMASK_REG_ENV_PASS')
print('numpy='+numpy.__version__)
print('scipy='+scipy.__version__)
print('classy_module='+str(classy.__file__))
print('NL1C6D2N_CLASS_ROOT='+os.environ['NL1C6D2N_CLASS_ROOT'])
c=Class(); c.empty()
PY

JSON="results/fullj_stochastic_tagged_power_lattice_kmask_regression.json"
NPZ="results/fullj_stochastic_tagged_power_lattice_kmask_regression.npz"
CSV="results/fullj_stochastic_tagged_power_lattice_kmask_regression.csv"
LOG="results/fullj_stochastic_tagged_power_lattice_kmask_regression.log"
ZIP="results/fullj_stochastic_tagged_power_lattice_kmask_regression_bundle.zip"
rm -f "$JSON" "$NPZ" "$CSV" "$LOG" "$ZIP"

export OMP_NUM_THREADS=1
unset AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE AEST_OFFLINE_TRACE_FILE AEST_TANGENT_ALLOW_K_MISS || true

set +e
python -u -m fullj_weyl.stochastic_tagged_power_lattice_kmask_regression_r1 \
  --json-out "$JSON" --npz-out "$NPZ" --csv-out "$CSV" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

python - "$ZIP" "$LOG" "$JSON" "$NPZ" "$CSV" <<'PY'
from pathlib import Path
import sys, zipfile
zp=Path(sys.argv[1])
paths=[Path(x) for x in sys.argv[2:]] + [
    Path('docs/fullj_stochastic_tagged_power_lattice_kmask_regression_predata.md'),
    Path('docs/fullj_metric_projection_physical_kmask_repair_result.md'),
    Path('docs/fullj_evolving_weyl_bridge_history.md'),
    Path('fullj_weyl/stochastic_tagged_power_lattice_kmask_regression.py'),
    Path('fullj_weyl/stochastic_tagged_power_lattice_kmask_regression_r1.py'),
    Path('fullj_weyl/run_local_stochastic_tagged_power_lattice_kmask_regression.sh'),
    Path('fullj_weyl/metric_projection_physical_kmask_repair.py'),
    Path('fullj_weyl/stochastic_tagged_power_lattice.py'),
    Path('results/fullj_stochastic_tagged_power_lattice.json'),
    Path('results/fullj_stochastic_tagged_power_lattice.npz'),
    Path('results/fullj_metric_projection_physical_kmask_repair_audit.json'),
    Path('results/nl1c6d2n_corrected_class_densek64_env.sh'),
]
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED) as zf:
    seen=set()
    for p in paths:
        if p.exists() and p not in seen:
            zf.write(p,arcname=str(p)); seen.add(p)
print('FULLJ_POWER_KMASK_REG_BUNDLE='+str(zp))
PY

echo "FULLJ_POWER_KMASK_REG_EXIT=$code"
echo "FULLJ_POWER_KMASK_REG_LOG=$LOG"
echo "FULLJ_POWER_KMASK_REG_JSON=$JSON"
echo "FULLJ_POWER_KMASK_REG_NPZ=$NPZ"
echo "FULLJ_POWER_KMASK_REG_CSV=$CSV"
echo "FULLJ_POWER_KMASK_REG_ZIP=$ZIP"
exit "$code"
