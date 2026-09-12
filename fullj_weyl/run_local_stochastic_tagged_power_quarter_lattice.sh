#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

BASE_PY=""
if command -v python3 >/dev/null 2>&1; then BASE_PY="$(command -v python3)";
elif command -v python >/dev/null 2>&1; then BASE_PY="$(command -v python)";
else echo "FULLJ_QUARTER_LATTICE: python missing" >&2; exit 2; fi

VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then
  "$BASE_PY" -m venv "$VENV" || { echo "FULLJ_QUARTER_LATTICE: install python3-venv" >&2; exit 2; }
fi
export PATH="$VENV/bin:$PATH"
python -m pip install --upgrade pip setuptools wheel >/dev/null
python -m pip install numpy scipy cython >/dev/null

python -m py_compile \
  fullj_weyl/stochastic_tagged_power_quarter_lattice.py \
  fullj_weyl/stochastic_tagged_power_lattice_kmask_regression.py \
  fullj_weyl/metric_projection_physical_kmask_repair.py \
  fullj_weyl/stochastic_tagged_power_lattice.py \
  fullj_weyl/stochastic_tagged_mode_poc.py \
  fullj_weyl/evolving_flrw_weyl_bridge_r2.py

for f in \
  docs/fullj_stochastic_tagged_power_quarter_lattice_predata.md \
  docs/fullj_stochastic_tagged_power_lattice_kmask_regression_result.md \
  docs/fullj_metric_projection_physical_kmask_repair_result.md \
  results/fullj_stochastic_tagged_power_lattice_kmask_regression.json \
  results/fullj_stochastic_tagged_power_lattice_kmask_regression.npz; do
  if [[ ! -f "$f" ]]; then
    echo "FULLJ_QUARTER_LATTICE: missing required lock/input $f" >&2
    exit 3
  fi
done

python - <<'PY'
import hashlib, json
from pathlib import Path
from fullj_weyl import stochastic_tagged_power_quarter_lattice as q
from fullj_weyl import metric_projection_physical_kmask_repair as km

assert q.PREDATA_LOCK == '3d309b51e44eb38569a7be263dbb14963ba4bd17'
assert q.PARENT_NPZ_SHA256 == '83fb7462ec970bfef953e3804d11a81fd5843745347fe77c318c9e39b8e6e82d'
assert km.REPAIR_ACTIVE is True
ident=km.original_r2_mask_identity(128)
assert ident['identical'] and ident['mismatch_count']==0
assert abs(km.METRIC_KMAX_H-0.32)<1e-15
assert abs(q.KF_Q-0.00125)<1e-15 and q.NX_Q==1024
assert len(q.K_QUARTER)==18
assert len(q.K_QUARTER)*len(q.B2)*2 == 72

p=Path('results/fullj_stochastic_tagged_power_lattice_kmask_regression.npz')
h=hashlib.sha256(p.read_bytes()).hexdigest()
assert h==q.PARENT_NPZ_SHA256, (h,q.PARENT_NPZ_SHA256)
meta=json.loads(Path('results/fullj_stochastic_tagged_power_lattice_kmask_regression.json').read_text())
assert meta['classification']=='FULLJ_STOCHASTIC_TAGGED_POWER_LATTICE_KMASK_REGRESSION_FAIL'
for k in ['KR_G1_provenance_and_frozen_identity','KR_G2_overlap_reuse_certification','KR_G3_stageA_repaired_health_and_saturation','KR_G4_repaired_hybrid_power_sanity','KR_G5_stageB_repaired_health_and_saturation']:
    assert meta['gates'][k] is True
for k in ['KR_G6_repaired_half_lattice_power_interpolation_accuracy','KR_G7_no_unresolved_repaired_half_lattice_power_spike']:
    assert meta['gates'][k] is False
print('FULLJ_QUARTER_LATTICE_IMPORT_CHAIN_PASS')
print('FULLJ_QUARTER_LATTICE_PARENT_LOCK_PASS sha256='+h)
print('FULLJ_QUARTER_LATTICE_GRID_PASS windows=3 quarter_nodes=18 backgrounds=2 signs=2 total=72')
print('FULLJ_QUARTER_LATTICE_PHYSICAL_MASK_PASS kmax_h=0.32 mismatch_count=0')
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
  echo "FULLJ_QUARTER_LATTICE: reusing isolated corrected CLASS dense-k64 environment..."
else
  echo "FULLJ_QUARTER_LATTICE: preparing isolated corrected CLASS dense-k64 environment..."
  bash fullj_weyl/setup_corrected_class_dense_k64_local.sh
  # shellcheck disable=SC1090
  source "$ENVFILE"
fi

grep -Eq '^#define[[:space:]]+_MAX_NUMBER_OF_K_FILES_[[:space:]]+64[[:space:]]*$' \
  "$NL1C6D2N_CLASS_ROOT/include/perturbations.h"

python - <<'PY'
import os, numpy, scipy, classy
from classy import Class
print('FULLJ_QUARTER_LATTICE_CLASS_KFILE_LIMIT_PASS value='+os.environ.get('FULLJ_DENSE_RESIDUAL_R2_CLASS_KFILE_LIMIT',''))
print('FULLJ_QUARTER_LATTICE_ENV_PASS')
print('numpy='+numpy.__version__)
print('scipy='+scipy.__version__)
print('classy_module='+str(classy.__file__))
print('NL1C6D2N_CLASS_ROOT='+os.environ['NL1C6D2N_CLASS_ROOT'])
c=Class(); c.empty()
PY

JSON="results/fullj_stochastic_tagged_power_quarter_lattice.json"
NPZ="results/fullj_stochastic_tagged_power_quarter_lattice.npz"
CSV="results/fullj_stochastic_tagged_power_quarter_lattice.csv"
LOG="results/fullj_stochastic_tagged_power_quarter_lattice.log"
ZIP="results/fullj_stochastic_tagged_power_quarter_lattice_bundle.zip"
rm -f "$JSON" "$NPZ" "$CSV" "$LOG" "$ZIP"

export OMP_NUM_THREADS=1
unset AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE AEST_OFFLINE_TRACE_FILE AEST_TANGENT_ALLOW_K_MISS || true

set +e
python -u -m fullj_weyl.stochastic_tagged_power_quarter_lattice \
  --json-out "$JSON" --npz-out "$NPZ" --csv-out "$CSV" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

python - "$ZIP" "$LOG" "$JSON" "$NPZ" "$CSV" <<'PY'
from pathlib import Path
import sys, zipfile
zp=Path(sys.argv[1])
paths=[Path(x) for x in sys.argv[2:]] + [
    Path('docs/fullj_stochastic_tagged_power_quarter_lattice_predata.md'),
    Path('docs/fullj_stochastic_tagged_power_lattice_kmask_regression_result.md'),
    Path('docs/fullj_metric_projection_physical_kmask_repair_result.md'),
    Path('docs/fullj_evolving_weyl_bridge_history.md'),
    Path('fullj_weyl/stochastic_tagged_power_quarter_lattice.py'),
    Path('fullj_weyl/run_local_stochastic_tagged_power_quarter_lattice.sh'),
    Path('fullj_weyl/metric_projection_physical_kmask_repair.py'),
    Path('results/fullj_stochastic_tagged_power_lattice_kmask_regression.json'),
    Path('results/fullj_stochastic_tagged_power_lattice_kmask_regression.npz'),
    Path('results/nl1c6d2n_corrected_class_densek64_env.sh'),
]
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED) as zf:
    seen=set()
    for p in paths:
        if p.exists() and p not in seen:
            zf.write(p,arcname=str(p)); seen.add(p)
print('FULLJ_QUARTER_LATTICE_BUNDLE='+str(zp))
PY

echo "FULLJ_QUARTER_LATTICE_EXIT=$code"
echo "FULLJ_QUARTER_LATTICE_LOG=$LOG"
echo "FULLJ_QUARTER_LATTICE_JSON=$JSON"
echo "FULLJ_QUARTER_LATTICE_NPZ=$NPZ"
echo "FULLJ_QUARTER_LATTICE_CSV=$CSV"
echo "FULLJ_QUARTER_LATTICE_ZIP=$ZIP"
exit "$code"
