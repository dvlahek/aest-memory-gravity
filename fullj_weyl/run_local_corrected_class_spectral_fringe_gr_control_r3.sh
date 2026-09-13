#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

BASE_PY=""
if command -v python3 >/dev/null 2>&1; then BASE_PY="$(command -v python3)";
elif command -v python >/dev/null 2>&1; then BASE_PY="$(command -v python)";
else echo "FULLJ_DIRECT_CLASS_FRINGE_R3: python missing" >&2; exit 2; fi

VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then
  "$BASE_PY" -m venv "$VENV" || { echo "FULLJ_DIRECT_CLASS_FRINGE_R3: install python3-venv" >&2; exit 2; }
fi
export PATH="$VENV/bin:$PATH"
python -m pip install --upgrade pip setuptools wheel >/dev/null
python -m pip install numpy scipy cython >/dev/null

python -m py_compile \
  fullj_weyl/corrected_class_spectral_fringe_gr_control.py \
  fullj_weyl/corrected_class_spectral_fringe_gr_control_r1.py \
  fullj_weyl/corrected_class_spectral_fringe_gr_control_r2.py \
  fullj_weyl/corrected_class_spectral_fringe_gr_control_r3.py \
  nl1c6d2n/corrected_class_baseline.py \
  nl1c6d2a/baryon_matter_sector_audit.py

for f in \
  docs/fullj_corrected_class_spectral_fringe_gr_control_predata.md \
  docs/fullj_corrected_class_spectral_fringe_runtime_provenance_repair.md \
  docs/fullj_corrected_class_spectral_fringe_transfer_input_repair.md \
  docs/fullj_corrected_class_spectral_fringe_k_serialization_repair.md \
  docs/fullj_spectral_fringe_source_decomposition_result.md \
  results/fullj_spectral_fringe_source_decomposition.json \
  results/fullj_spectral_fringe_source_decomposition.npz; do
  if [[ ! -f "$f" ]]; then
    echo "FULLJ_DIRECT_CLASS_FRINGE_R3: missing required lock/input $f" >&2
    exit 3
  fi
done

python - <<'PY'
from fullj_weyl import corrected_class_spectral_fringe_gr_control as q
from fullj_weyl import corrected_class_spectral_fringe_gr_control_r3 as r
assert q.PREDATA_LOCK == '0e26b4688eeeedd522b8dd153f84a76137d7e43c'
assert r.RUNTIME_REPAIR_LOCK == '1812f015682a946125e747f81b97b902dcf1bec0'
assert r.INPUT_REPAIR_LOCK == 'b16eed79f9fc730d651ed75b44ed161bf8b4a69d'
assert r.SERIALIZATION_REPAIR_LOCK == 'b691d6ef9e6fa061d7fca842bfc71cfbe81978c1'
assert r.DENSE_RUNTIME_SOURCE_SHA == '4d5ab5dc7066d4880f06fcfc731d6534ed0ff992e3cc15fb473dddccb25a594f'
assert len(q.K_DENSE)==51 and len(q.K_ANCHOR)==15
assert abs(q.DK-0.000625)<1e-15
assert q.MIN_SPEC_RATIO==10.0 and q.MIN_AEST_KAPPA==5.0e-2
old=', '.join(f'{x*q.cb.h:.17g}' for x in q.K_DENSE)
new,meta=r.serialize_requested_k(q.K_DENSE)
anchor,ameta=r.serialize_requested_k(q.K_ANCHOR)
assert len(old)==1080
assert old[:1023].count(',')+1==49
assert len(new)==982 and meta['value_count']==51
assert len(anchor)==288 and ameta['value_count']==15
assert meta['max_abs_k_h_Mpc_displacement'] <= 1e-12
assert ameta['max_abs_k_h_Mpc_displacement'] <= 1e-12
print('FULLJ_DIRECT_CLASS_FRINGE_R3_IMPORT_CHAIN_PASS')
print('FULLJ_DIRECT_CLASS_FRINGE_R3_SCIENCE_LOCKS_UNCHANGED_PASS')
print('FULLJ_DIRECT_CLASS_FRINGE_R3_SERIALIZATION_DIAG_PASS old_chars=1080 old_prefix_values=49 dense_chars=982 dense_n=51 anchor_chars=288 anchor_n=15')
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
  echo "FULLJ_DIRECT_CLASS_FRINGE_R3: reusing exact dense-k64 environment rebuilt by R1..."
else
  echo "FULLJ_DIRECT_CLASS_FRINGE_R3: dense-k64 environment missing; rebuilding..."
  bash fullj_weyl/setup_corrected_class_dense_k64_local.sh
  # shellcheck disable=SC1090
  source "$ENVFILE"
fi

EXPECTED_CLASS_HEAD="e85808324f51fc694d12e3ed7439552a3c3f9540"
EXPECTED_RUNTIME_SHA="4d5ab5dc7066d4880f06fcfc731d6534ed0ff992e3cc15fb473dddccb25a594f"
ACTUAL_CLASS_HEAD="$(git -C "$NL1C6D2N_CLASS_ROOT" rev-parse HEAD)"
ACTUAL_RUNTIME_SHA="$(sha256sum "$NL1C6D2N_CLASS_ROOT/source/aest_memory.c" | awk '{print $1}')"

if [[ "$ACTUAL_CLASS_HEAD" != "$EXPECTED_CLASS_HEAD" ]]; then
  echo "FULLJ_DIRECT_CLASS_FRINGE_R3: CLASS head mismatch $ACTUAL_CLASS_HEAD" >&2
  exit 3
fi
if [[ "$ACTUAL_RUNTIME_SHA" != "$EXPECTED_RUNTIME_SHA" ]]; then
  echo "FULLJ_DIRECT_CLASS_FRINGE_R3: runtime SHA mismatch $ACTUAL_RUNTIME_SHA" >&2
  exit 3
fi
grep -Eq '^#define[[:space:]]+_MAX_NUMBER_OF_K_FILES_[[:space:]]+64[[:space:]]*$' \
  "$NL1C6D2N_CLASS_ROOT/include/perturbations.h"

echo "FULLJ_DIRECT_CLASS_FRINGE_R3_RUNTIME_PROVENANCE_PASS head=$ACTUAL_CLASS_HEAD source_sha256=$ACTUAL_RUNTIME_SHA kfile_limit=64"

python - <<'PY'
import os, classy, numpy, scipy
from classy import Class
print('FULLJ_DIRECT_CLASS_FRINGE_R3_ENV_PASS')
print('numpy='+numpy.__version__)
print('scipy='+scipy.__version__)
print('classy_module='+str(classy.__file__))
print('NL1C6D2N_CLASS_ROOT='+os.environ['NL1C6D2N_CLASS_ROOT'])
c=Class(); c.empty()
PY

JSON="results/fullj_corrected_class_spectral_fringe_gr_control.json"
NPZ="results/fullj_corrected_class_spectral_fringe_gr_control.npz"
LOG="results/fullj_corrected_class_spectral_fringe_gr_control_r3.log"
ZIP="results/fullj_corrected_class_spectral_fringe_gr_control_r3_bundle.zip"
rm -f "$JSON" "$NPZ" "$LOG" "$ZIP"

export OMP_NUM_THREADS=1
unset AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE AEST_OFFLINE_TRACE_FILE AEST_TANGENT_ALLOW_K_MISS || true

set +e
python -u -m fullj_weyl.corrected_class_spectral_fringe_gr_control_r3 \
  --json-out "$JSON" --npz-out "$NPZ" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

python - "$ZIP" "$LOG" "$JSON" "$NPZ" <<'PY'
from pathlib import Path
import sys, zipfile
zp=Path(sys.argv[1])
paths=[Path(x) for x in sys.argv[2:]] + [
    Path('docs/fullj_corrected_class_spectral_fringe_gr_control_predata.md'),
    Path('docs/fullj_corrected_class_spectral_fringe_runtime_provenance_repair.md'),
    Path('docs/fullj_corrected_class_spectral_fringe_transfer_input_repair.md'),
    Path('docs/fullj_corrected_class_spectral_fringe_k_serialization_repair.md'),
    Path('docs/fullj_spectral_fringe_source_decomposition_result.md'),
    Path('fullj_weyl/corrected_class_spectral_fringe_gr_control.py'),
    Path('fullj_weyl/corrected_class_spectral_fringe_gr_control_r1.py'),
    Path('fullj_weyl/corrected_class_spectral_fringe_gr_control_r2.py'),
    Path('fullj_weyl/corrected_class_spectral_fringe_gr_control_r3.py'),
    Path('fullj_weyl/run_local_corrected_class_spectral_fringe_gr_control_r3.sh'),
    Path('fullj_weyl/setup_corrected_class_dense_k64_local.sh'),
    Path('results/fullj_spectral_fringe_source_decomposition.json'),
    Path('results/fullj_spectral_fringe_source_decomposition.npz'),
    Path('results/nl1c6d2n_corrected_class_densek64_env.sh'),
]
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED) as zf:
    seen=set()
    for p in paths:
        if p.exists() and p not in seen:
            zf.write(p,arcname=str(p)); seen.add(p)
print('FULLJ_DIRECT_CLASS_FRINGE_R3_BUNDLE='+str(zp))
PY

echo "FULLJ_DIRECT_CLASS_FRINGE_R3_EXIT=$code"
echo "FULLJ_DIRECT_CLASS_FRINGE_R3_LOG=$LOG"
echo "FULLJ_DIRECT_CLASS_FRINGE_R3_JSON=$JSON"
echo "FULLJ_DIRECT_CLASS_FRINGE_R3_NPZ=$NPZ"
echo "FULLJ_DIRECT_CLASS_FRINGE_R3_ZIP=$ZIP"
exit "$code"
