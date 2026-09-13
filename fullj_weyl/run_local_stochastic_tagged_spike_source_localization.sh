#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

BASE_PY=""
if command -v python3 >/dev/null 2>&1; then BASE_PY="$(command -v python3)";
elif command -v python >/dev/null 2>&1; then BASE_PY="$(command -v python)";
else echo "FULLJ_SPIKE_LOCALIZATION: python missing" >&2; exit 2; fi

VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then
  "$BASE_PY" -m venv "$VENV" || { echo "FULLJ_SPIKE_LOCALIZATION: install python3-venv" >&2; exit 2; }
fi
export PATH="$VENV/bin:$PATH"
python -m pip install --upgrade pip setuptools wheel >/dev/null
python -m pip install numpy scipy cython >/dev/null

python -m py_compile \
  fullj_weyl/stochastic_tagged_spike_source_localization.py \
  fullj_weyl/stochastic_tagged_power_quarter_lattice.py \
  fullj_weyl/metric_projection_physical_kmask_repair.py \
  fullj_weyl/stochastic_tagged_power_lattice.py \
  fullj_weyl/stochastic_tagged_mode_poc.py \
  fullj_weyl/evolving_flrw_weyl_bridge_r2.py

for f in \
  docs/fullj_stochastic_tagged_spike_source_localization_predata.md \
  docs/fullj_stochastic_tagged_power_quarter_lattice_result.md \
  docs/fullj_metric_projection_physical_kmask_repair_result.md \
  docs/fullj_evolving_weyl_bridge_history.md \
  results/fullj_stochastic_tagged_power_quarter_lattice.json \
  results/fullj_stochastic_tagged_power_quarter_lattice.npz \
  results/fullj_metric_projection_physical_kmask_repair_audit.json; do
  if [[ ! -f "$f" ]]; then
    echo "FULLJ_SPIKE_LOCALIZATION: missing required lock/input $f" >&2
    exit 3
  fi
done

python - <<'PY'
import hashlib, json
from pathlib import Path
from fullj_weyl import stochastic_tagged_spike_source_localization as q
from fullj_weyl import metric_projection_physical_kmask_repair as km

assert q.PREDATA_LOCK == 'a7b63fdaeb501fb01e9ef31e66ba7829b01c5472'
assert q.QUARTER_FAIL_RESULT_LOCK == 'c1dd14b2d15fcd48519c328eb4906ef5d1b265b4'
assert q.HISTORY_LOCK == 'ce8ef79da695fae7b37793f325678096eb5dc2ac'
assert q.BG == 0
assert q.NSTEP_BASE == 4096 and q.NSTEP_FINE == 8192
assert abs(q.EPS_BASE-0.05) < 1e-15 and abs(q.EPS_HALF-0.025) < 1e-15
assert len(q.K_LOCAL) == 9 and len(q.CENTERS) == 3
assert 18+6+6+6+18 == 54
assert abs(q.KF_BASE-0.00125) < 1e-15 and q.NX_BASE == 1024
assert abs(q.KF_BOX-0.000625) < 1e-15 and q.NX_BOX == 2048
assert km.REPAIR_ACTIVE is True
ident=km.original_r2_mask_identity(128)
assert ident['identical'] and ident['mismatch_count']==0
assert abs(km.METRIC_KMAX_H-0.32) < 1e-15

p=Path('results/fullj_stochastic_tagged_power_quarter_lattice.npz')
h=hashlib.sha256(p.read_bytes()).hexdigest()
assert h == q.PARENT_NPZ_SHA256, (h, q.PARENT_NPZ_SHA256)
meta=json.loads(Path('results/fullj_stochastic_tagged_power_quarter_lattice.json').read_text())
assert meta['classification']=='FULLJ_STOCHASTIC_TAGGED_POWER_QUARTER_LATTICE_FAIL'
for k in ['QL_G1_provenance_and_frozen_identity','QL_G2_solver_constraint_health','QL_G3_broadband_saturated_closure','QL_G4_quarter_stochastic_algebra_sanity']:
    assert meta['gates'][k] is True
for k in ['QL_G5_absolute_quarter_power_interpolation_accuracy','QL_G6_no_new_unresolved_quarter_power_spike','QL_G7_refinement_improves_over_005']:
    assert meta['gates'][k] is False
print('FULLJ_SPIKE_LOCALIZATION_IMPORT_CHAIN_PASS')
print('FULLJ_SPIKE_LOCALIZATION_PARENT_LOCK_PASS sha256='+h)
print('FULLJ_SPIKE_LOCALIZATION_GRID_PASS local_nodes=9 centers=3 total_runs=54')
print('FULLJ_SPIKE_LOCALIZATION_CONTROLS_PASS baseline=18 time=6 epsilon=6 box2x=6 saturated=18')
print('FULLJ_SPIKE_LOCALIZATION_PHYSICAL_MASK_PASS kmax_h=0.32 mismatch_count=0')
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
  echo "FULLJ_SPIKE_LOCALIZATION: reusing isolated corrected CLASS dense-k64 environment..."
else
  echo "FULLJ_SPIKE_LOCALIZATION: preparing isolated corrected CLASS dense-k64 environment..."
  bash fullj_weyl/setup_corrected_class_dense_k64_local.sh
  # shellcheck disable=SC1090
  source "$ENVFILE"
fi

grep -Eq '^#define[[:space:]]+_MAX_NUMBER_OF_K_FILES_[[:space:]]+64[[:space:]]*$' \
  "$NL1C6D2N_CLASS_ROOT/include/perturbations.h"

python - <<'PY'
import os, numpy, scipy, classy
from classy import Class
print('FULLJ_SPIKE_LOCALIZATION_CLASS_KFILE_LIMIT_PASS value='+os.environ.get('FULLJ_DENSE_RESIDUAL_R2_CLASS_KFILE_LIMIT',''))
print('FULLJ_SPIKE_LOCALIZATION_ENV_PASS')
print('numpy='+numpy.__version__)
print('scipy='+scipy.__version__)
print('classy_module='+str(classy.__file__))
print('NL1C6D2N_CLASS_ROOT='+os.environ['NL1C6D2N_CLASS_ROOT'])
c=Class(); c.empty()
PY

JSON="results/fullj_stochastic_tagged_spike_source_localization.json"
NPZ="results/fullj_stochastic_tagged_spike_source_localization.npz"
CSV="results/fullj_stochastic_tagged_spike_source_localization.csv"
LOG="results/fullj_stochastic_tagged_spike_source_localization.log"
ZIP="results/fullj_stochastic_tagged_spike_source_localization_bundle.zip"
rm -f "$JSON" "$NPZ" "$CSV" "$LOG" "$ZIP"

export OMP_NUM_THREADS=1
unset AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE AEST_OFFLINE_TRACE_FILE AEST_TANGENT_ALLOW_K_MISS || true

set +e
python -u -m fullj_weyl.stochastic_tagged_spike_source_localization \
  --json-out "$JSON" --npz-out "$NPZ" --csv-out "$CSV" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

python - "$ZIP" "$LOG" "$JSON" "$NPZ" "$CSV" <<'PY'
from pathlib import Path
import sys, zipfile
zp=Path(sys.argv[1])
paths=[Path(x) for x in sys.argv[2:]] + [
    Path('docs/fullj_stochastic_tagged_spike_source_localization_predata.md'),
    Path('docs/fullj_stochastic_tagged_power_quarter_lattice_result.md'),
    Path('docs/fullj_metric_projection_physical_kmask_repair_result.md'),
    Path('docs/fullj_evolving_weyl_bridge_history.md'),
    Path('fullj_weyl/stochastic_tagged_spike_source_localization.py'),
    Path('fullj_weyl/run_local_stochastic_tagged_spike_source_localization.sh'),
    Path('fullj_weyl/stochastic_tagged_power_quarter_lattice.py'),
    Path('fullj_weyl/metric_projection_physical_kmask_repair.py'),
    Path('results/fullj_stochastic_tagged_power_quarter_lattice.json'),
    Path('results/fullj_stochastic_tagged_power_quarter_lattice.npz'),
    Path('results/fullj_metric_projection_physical_kmask_repair_audit.json'),
    Path('results/nl1c6d2n_corrected_class_densek64_env.sh'),
]
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED) as zf:
    seen=set()
    for p in paths:
        if p.exists() and p not in seen:
            zf.write(p,arcname=str(p)); seen.add(p)
print('FULLJ_SPIKE_LOCALIZATION_BUNDLE='+str(zp))
PY

echo "FULLJ_SPIKE_LOCALIZATION_EXIT=$code"
echo "FULLJ_SPIKE_LOCALIZATION_LOG=$LOG"
echo "FULLJ_SPIKE_LOCALIZATION_JSON=$JSON"
echo "FULLJ_SPIKE_LOCALIZATION_NPZ=$NPZ"
echo "FULLJ_SPIKE_LOCALIZATION_CSV=$CSV"
echo "FULLJ_SPIKE_LOCALIZATION_ZIP=$ZIP"
exit "$code"
