#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

BASE_PY=""
if command -v python3 >/dev/null 2>&1; then BASE_PY="$(command -v python3)";
elif command -v python >/dev/null 2>&1; then BASE_PY="$(command -v python)";
else echo "FULLJ_FRINGE_SOURCE_DECOMP: python missing" >&2; exit 2; fi

VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then
  "$BASE_PY" -m venv "$VENV" || { echo "FULLJ_FRINGE_SOURCE_DECOMP: install python3-venv" >&2; exit 2; }
fi
export PATH="$VENV/bin:$PATH"
python -m pip install --upgrade pip setuptools wheel >/dev/null
python -m pip install numpy scipy cython >/dev/null

python -m py_compile \
  fullj_weyl/spectral_fringe_source_decomposition.py \
  fullj_weyl/stochastic_tagged_spike_source_localization.py \
  fullj_weyl/stochastic_tagged_spectral_fringe_geometry_audit.py \
  fullj_weyl/metric_projection_physical_kmask_repair.py

for f in \
  docs/fullj_spectral_fringe_source_decomposition_predata.md \
  docs/fullj_stochastic_tagged_spectral_fringe_geometry_audit_result.md \
  results/fullj_stochastic_tagged_spike_source_localization.json \
  results/fullj_stochastic_tagged_spike_source_localization.npz \
  results/fullj_stochastic_tagged_spectral_fringe_geometry_audit.json \
  results/fullj_stochastic_tagged_spectral_fringe_geometry_audit.npz; do
  if [[ ! -f "$f" ]]; then
    echo "FULLJ_FRINGE_SOURCE_DECOMP: missing required input $f" >&2
    exit 3
  fi
done

python - <<'PY'
import hashlib
from pathlib import Path
from fullj_weyl import spectral_fringe_source_decomposition as q
from fullj_weyl import metric_projection_physical_kmask_repair as km
assert q.PREDATA_LOCK == '82554256e89829b906e652700cbe5110bcbbecfb'
assert q.GEOMETRY_RESULT_LOCK == '73fb42d64e61d69820d31a9c9f71c8d536b2376e'
assert q.SOURCE_RESULT_LOCK == '86ab13ffa1048860731f65348074ede1b469c644'
assert len(q.TARGETS)==6 and q.BG==0 and q.NSTEP==4096 and q.NX==1024
assert abs(q.KF-0.00125)<1e-15 and abs(q.EPS-0.05)<1e-15
assert km.REPAIR_ACTIVE is True and abs(km.METRIC_KMAX_H-0.32)<1e-15
ident=km.original_r2_mask_identity(128)
assert ident['identical'] and ident['mismatch_count']==0
for path, expected in [
 ('results/fullj_stochastic_tagged_spike_source_localization.npz', q.SOURCE_NPZ_SHA256),
 ('results/fullj_stochastic_tagged_spectral_fringe_geometry_audit.npz', q.GEOM_NPZ_SHA256),
]:
    got=hashlib.sha256(Path(path).read_bytes()).hexdigest()
    assert got==expected, (path,got,expected)
print('FULLJ_FRINGE_SOURCE_DECOMP_IMPORT_CHAIN_PASS')
print('FULLJ_FRINGE_SOURCE_DECOMP_PARENT_LOCKS_PASS')
print('FULLJ_FRINGE_SOURCE_DECOMP_GRID_PASS targets=6 signs=2 total_runs=12')
print('FULLJ_FRINGE_SOURCE_DECOMP_PHYSICAL_MASK_PASS kmax_h=0.32 mismatch_count=0')
PY

ENVFILE="$ROOT/results/nl1c6d2n_corrected_class_densek64_env.sh"
reuse=0
if [[ -f "$ENVFILE" ]]; then
  # shellcheck disable=SC1090
  source "$ENVFILE"
  if [[ -n "${NL1C6D2N_CLASS_ROOT:-}" && -d "$NL1C6D2N_CLASS_ROOT/.git" \
        && -n "${NL1C6D2N_PYTARGET:-}" && -f "$NL1C6D2N_PYTARGET/classy/__init__.py" \
        && "${FULLJ_DENSE_RESIDUAL_R2_CLASS_KFILE_LIMIT:-}" == "64" ]]; then reuse=1; fi
fi
if [[ "$reuse" -eq 1 ]]; then
  echo "FULLJ_FRINGE_SOURCE_DECOMP: reusing isolated corrected CLASS dense-k64 environment..."
else
  echo "FULLJ_FRINGE_SOURCE_DECOMP: preparing isolated corrected CLASS dense-k64 environment..."
  bash fullj_weyl/setup_corrected_class_dense_k64_local.sh
  # shellcheck disable=SC1090
  source "$ENVFILE"
fi

python - <<'PY'
import os, numpy, scipy, classy
print('FULLJ_FRINGE_SOURCE_DECOMP_ENV_PASS')
print('numpy='+numpy.__version__)
print('scipy='+scipy.__version__)
print('classy_module='+str(classy.__file__))
print('NL1C6D2N_CLASS_ROOT='+os.environ['NL1C6D2N_CLASS_ROOT'])
PY

JSON="results/fullj_spectral_fringe_source_decomposition.json"
NPZ="results/fullj_spectral_fringe_source_decomposition.npz"
CSV="results/fullj_spectral_fringe_source_decomposition.csv"
LOG="results/fullj_spectral_fringe_source_decomposition.log"
ZIP="results/fullj_spectral_fringe_source_decomposition_bundle.zip"
rm -f "$JSON" "$NPZ" "$CSV" "$LOG" "$ZIP"

export OMP_NUM_THREADS=1
unset AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE AEST_OFFLINE_TRACE_FILE AEST_TANGENT_ALLOW_K_MISS || true

set +e
python -u -m fullj_weyl.spectral_fringe_source_decomposition \
  --json-out "$JSON" --npz-out "$NPZ" --csv-out "$CSV" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

python - "$ZIP" "$LOG" "$JSON" "$NPZ" "$CSV" <<'PY'
from pathlib import Path
import sys, zipfile
zp=Path(sys.argv[1])
paths=[Path(x) for x in sys.argv[2:]] + [
 Path('docs/fullj_spectral_fringe_source_decomposition_predata.md'),
 Path('docs/fullj_stochastic_tagged_spectral_fringe_geometry_audit_result.md'),
 Path('fullj_weyl/spectral_fringe_source_decomposition.py'),
 Path('fullj_weyl/run_local_spectral_fringe_source_decomposition.sh'),
 Path('results/fullj_stochastic_tagged_spike_source_localization.json'),
 Path('results/fullj_stochastic_tagged_spike_source_localization.npz'),
 Path('results/fullj_stochastic_tagged_spectral_fringe_geometry_audit.json'),
 Path('results/fullj_stochastic_tagged_spectral_fringe_geometry_audit.npz'),
]
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED) as zf:
    seen=set()
    for p in paths:
        if p.exists() and p not in seen:
            zf.write(p,arcname=str(p)); seen.add(p)
print('FULLJ_FRINGE_SOURCE_DECOMP_BUNDLE='+str(zp))
PY

echo "FULLJ_FRINGE_SOURCE_DECOMP_EXIT=$code"
echo "FULLJ_FRINGE_SOURCE_DECOMP_LOG=$LOG"
echo "FULLJ_FRINGE_SOURCE_DECOMP_JSON=$JSON"
echo "FULLJ_FRINGE_SOURCE_DECOMP_NPZ=$NPZ"
echo "FULLJ_FRINGE_SOURCE_DECOMP_CSV=$CSV"
echo "FULLJ_FRINGE_SOURCE_DECOMP_ZIP=$ZIP"
exit "$code"
