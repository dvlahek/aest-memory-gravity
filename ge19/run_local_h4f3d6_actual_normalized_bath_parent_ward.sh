#!/usr/bin/env bash
# GE19 H4F3d6: actual R1 bath Euler/Ward SUBSET on frozen physical parents.
# Never overwrites historical Repair37, H3F/H3G, Z11 or H4F3b results.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results

test "$(git rev-parse HEAD:ge19/h4f3d6_predata_actual_normalized_bath_parent_ward.json)" = "d283086a6ae95efd184db570d6c2f9a8aa32ac7c"
test "$(git rev-parse HEAD:ge19/h4f3d6_actual_normalized_bath_parent_ward.py)" = "0419145499f5f44e06ba0c96f779c2a604e84ce7"
test "$(git rev-parse HEAD:docs/ge19_h4f3d6_bath_convolution_compiler_valid_freeze.md)" = "5695cc61be84098787af2cec8585f7daea6ced38"
test "$(git rev-parse HEAD:.github/workflows/ge19-h4f3d6-bath-parent-ward.yml)" = "ec0d9c94eaa6295ed46eb858b62a278ec05e8c02"
test "$(git rev-parse HEAD:ge19/h4f3b_actual_corrected_six_piece_source.py)" = "0423cbc64f6cda3b2a9aeb67c734935ef3ae7f9c"
test "$(git rev-parse HEAD:ge19/h4f3d5_normalized_bath_parent_residual_compiler.py)" = "62cbd02902ccb514c535213ff9801a9abcd46ffb"
test "$(git rev-parse HEAD:ge19/repair24_q20_construction.py)" = "fc271987d1bddcd023cc9c057ddcad036b1d72fb"
for p in \
  ge19/h4f3d6_predata_actual_normalized_bath_parent_ward.json \
  ge19/h4f3d6_actual_normalized_bath_parent_ward.py \
  ge19/h4f3b_actual_corrected_six_piece_source.py \
  ge19/h4f3d5_normalized_bath_parent_residual_compiler.py \
  ge19/repair24_q20_construction.py
do
  git diff --quiet -- "$p"
  git diff --cached --quiet -- "$p"
done
echo GE19_H4F3D6_LOCAL_LOCK_PASS

if [[ -z "${VIRTUAL_ENV:-}" ]]; then
  echo "GE19_H4F3D6_VENV_NOT_ACTIVE: source .venv/bin/activate"
  exit 5
fi
python3 -c 'import numpy, scipy, sympy'
python3 -m py_compile ge19/h4f3d6_actual_normalized_bath_parent_ward.py
echo GE19_H4F3D6_LOCAL_PREEXECUTION_PASS

SOURCE_JSON="$ROOT/results/ge19_h4f3b_actual_corrected_six_piece_source.json"
SOURCE_NPZ="$ROOT/results/ge19_h4f3b_actual_corrected_six_piece_source.npz"
test -s "$SOURCE_JSON" && test -s "$SOURCE_NPZ" || {
  echo GE19_H4F3D6_MISSING_ACTUAL_H4F3B_SOURCE
  exit 6
}
test "$(sha256sum "$SOURCE_JSON" | awk '{print $1}')" = "1ec88fd3fd6b81bf30614b0cb78d722a02dd4f745e1f22cb9b8f956a44bac6c1"
test "$(sha256sum "$SOURCE_NPZ" | awk '{print $1}')" = "787d5d177838b05078057aa932f379dd529449ce203f5664c36cf723acb0116b"
echo GE19_H4F3D6_H4F3B_SOURCE_INPUT_PASS

TRACE=""
if [[ -d "$ROOT/frozen_repair26_repair27" ]]; then
  TRACE="$(find "$ROOT/frozen_repair26_repair27" -type f -name ge19_repair26_R1_full_history_trace.dat -print -quit)"
fi
if [[ -z "$TRACE" ]]; then
  if ! command -v gh >/dev/null 2>&1; then
    echo "GE19_H4F3D6_R1_TRACE_UNAVAILABLE: restore frozen Repair26 or authenticate gh"
    exit 6
  fi
  mkdir -p "$ROOT/frozen_repair26_repair27"
  gh run download 35721220889 \
    --repo dvlahek/aest-memory-gravity \
    --name results_bundle_ge19_repair26_cancellation_free_full_history_bath_boundary \
    --dir "$ROOT/frozen_repair26_repair27"
  TRACE="$(find "$ROOT/frozen_repair26_repair27" -type f -name ge19_repair26_R1_full_history_trace.dat -print -quit)"
fi
test -n "$TRACE"
TRACE="$(realpath "$TRACE")"
test "$(sha256sum "$TRACE" | awk '{print $1}')" = "608ee0b4c868a701db6976f756b9a551cd9ddffe1e8e4ab37c5cd2361405a6f8"
test "$(wc -c < "$TRACE" | tr -d ' ')" = "26643162"
echo GE19_H4F3D6_REPAIR26_R1_INPUT_PASS

# Frozen generators in historical imports may write relative to CWD:
# run only in disposable tmp/results, with all outputs under absolute ROOT.
export PYTHONPATH="$ROOT"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/results"
cd "$TMP"
python3 - "$ROOT/results" "$TRACE" "$SOURCE_JSON" "$SOURCE_NPZ" <<'PY'
from pathlib import Path
import json
import sys
from ge19 import h4f3b_actual_corrected_six_piece_source as s
from ge19 import h4f3d6_actual_normalized_bath_parent_ward as d6
rd,trace,js,npz=map(Path,sys.argv[1:])
assert all(v["exact"] for v in d6.check_code_lock().values())
assert all(v["exact"] for v in s.code_lock().values())
paths,parents=s.frozen_inputs(rd,trace)
assert d6.sha256(js)==d6.SOURCE_JSON_SHA
assert d6.sha256(npz)==d6.SOURCE_NPZ_SHA
source=json.loads(js.read_text())
assert source["classification"]=="GE19_H4F3B_ACTUAL_CORRECTED_SIX_SOURCE_PASS_FULL_WARD_OPEN"
assert all(source["gates"].values())
print("GE19_H4F3D6_ACTUAL_CORRECTED_PARENT_INPUT_PASS")
print("Z11 =",paths["z11"])
print("SOURCE_NPZ =",npz)
PY

JSON="$ROOT/results/ge19_h4f3d6_actual_normalized_bath_parent_ward.json"
NPZ="$ROOT/results/ge19_h4f3d6_actual_normalized_bath_parent_ward.npz"
FULL="$ROOT/results/ge19_h4f3d6_actual_normalized_bath_parent_ward_FULL.log"
rm -f "$JSON" "$NPZ" "$FULL"

set +e
set -o pipefail
python3 -m ge19.h4f3d6_actual_normalized_bath_parent_ward \
  --results-dir "$ROOT/results" \
  --repair26-trace "$TRACE" \
  --source-json "$SOURCE_JSON" --source-npz "$SOURCE_NPZ" \
  --json-out "$JSON" --npz-out "$NPZ" \
  2>&1 | tee "$FULL" | tail -n 38
rc=${PIPESTATUS[0]}
set -e
cd "$ROOT"

if [[ -s "$JSON" ]]; then
  python3 - <<'PY'
import json
d=json.load(open("results/ge19_h4f3d6_actual_normalized_bath_parent_ward.json"))
print("CLASSIFICATION =",d["classification"])
print("GATES =",d["gates"])
print("FAILED_GATES =",d["failed_gates"])
print("ACTUAL_COHORTS =",len(d["cases"]))
print("SOURCE_PLUS_BATH_ZERO_GATE = NONE")
print("FULL_NOETHER_CERTIFIED =",d["full_all_sector_H4_Noether_certified"])
print("Z21_CERTIFIED =",d["Z21_certified"])
PY
fi
for p in "$JSON" "$NPZ" "$FULL"; do
  if [[ -s "$p" ]]; then
    sha256sum "$p"
    wc -c "$p"
  fi
done
if [[ "$rc" -eq 0 && -s "$JSON" && -s "$NPZ" ]]; then
  echo GE19_H4F3D6_ACTUAL_BATH_SUBSET_PASS_FULL_NOETHER_OPEN
elif [[ "$rc" -eq 2 && -s "$JSON" && -s "$NPZ" ]]; then
  echo GE19_H4F3D6_ACTUAL_BATH_SUBSET_FAIL
else
  echo GE19_H4F3D6_IMPLEMENTATION_OR_INPUT_FAIL
fi
exit "$rc"
