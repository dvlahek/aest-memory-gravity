#!/usr/bin/env bash
set -euo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
[[ "$(git symbolic-ref --quiet --short HEAD)" == "physics-first-gravitational-elasticity" ]] || { echo GE19_D22AR2_WRONG_BRANCH; exit 4; }
if [[ -z "${VIRTUAL_ENV:-}" ]];then
  [[ -f "$ROOT/.venv/bin/activate" ]] || { echo GE19_D22AR2_VENV_MISSING; exit 5; }
  source "$ROOT/.venv/bin/activate"
fi
export PYTHONPATH="$ROOT" PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS="${OPENBLAS_NUM_THREADS:-1}"
[[ "$(sha256sum "$ROOT/ge19/h4f3d22a_r2_shift_constraint_serialization_repair.py" | awk '{print $1}')" == "5e435bdb823a70277d7021e06564fc47e7402fe1923a6d0e8b0bbea10c15f83b" ]] || { echo GE19_D22AR2_SOURCE_SHA_FAIL; exit 6; }
[[ "$(sha256sum "$ROOT/ge19/h4f3d22a_r1_shift_constraint_localization.py" | awk '{print $1}')" == "96b640912b0dffe026a4238342a069615d3165f11f85b1f1c174ea333d45e74c" ]] || { echo GE19_D22AR2_FROZEN_R1_SOURCE_SHA_FAIL; exit 6; }
python3 -B - <<'PYTEST'
import json
import numpy as np
from ge19.h4f3d22a_r2_shift_constraint_serialization_repair import (manufactured,location,json_numpy_scalar)
manufactured()
shape=(3,40,128)
metric=np.zeros(shape)
metric[1,19,45]=0.94
scalar=np.ones(shape)
compl=np.zeros(shape,dtype=complex)
loc=location(metric,scalar,scalar,compl,compl,scalar,np.arange(128,dtype=float),"Z20",(1.0,0.5,0.1))
assert loc["mode"]==20 and type(loc["mode"]) is int and loc["beta"]==0.5
payload={"worst":loc,"count":np.int64(40),"error":np.float32(0.125),"gate":np.bool_(True)}
assert json.loads(json.dumps(payload,allow_nan=False,default=json_numpy_scalar))["count"]==40
for obj in (complex(1,2),np.array([1,2])):
    try: json.dumps({"unsupported":obj},default=json_numpy_scalar)
    except TypeError: pass
    else: raise AssertionError("non-scalar JSON diagnostic silently accepted")
try: json.dumps({"nonfinite":float("nan")},allow_nan=False,default=json_numpy_scalar)
except ValueError: pass
else: raise AssertionError("nonfinite JSON diagnostic silently accepted")
print("GE19_D22AR2_NUMPY_SCALAR_JSON_AND_NEGATIVE_CONTROLS_PASS",flush=True)
PYTEST
TRACE="${GE19_REPAIR26_R1_TRACE:-}"
if [[ -z "$TRACE" && -s "$ROOT/results/ge19_repair26_R1_full_history_trace.dat" ]];then TRACE="$ROOT/results/ge19_repair26_R1_full_history_trace.dat";fi
if [[ -z "$TRACE" && -d "$ROOT/frozen_repair26_repair27" ]];then
  mapfile -d '' -t found < <(find "$ROOT/frozen_repair26_repair27" -type f -name ge19_repair26_R1_full_history_trace.dat -print0)
  if [[ "${#found[@]}" -eq 1 ]];then TRACE="${found[0]}";fi
fi
[[ -n "$TRACE" && -s "$TRACE" ]] || { echo GE19_D22AR2_REPAIR26_TRACE_MISSING; exit 6; }
TRACE="$(realpath "$TRACE")"
[[ "$(sha256sum "$TRACE" | awk '{print $1}')" == "608ee0b4c868a701db6976f756b9a551cd9ddffe1e8e4ab37c5cd2361405a6f8" ]] || { echo GE19_D22AR2_REPAIR26_TRACE_SHA_FAIL; exit 6; }
J="$ROOT/results/ge19_h4f3d22a_r2_shift_forensic.json"
N="$ROOT/results/ge19_h4f3d22a_r2_shift_forensic.npz"
F="$ROOT/results/ge19_h4f3d22a_r2_shift_forensic_FULL.log"
for f in "$J" "$N" "$F";do [[ ! -e "$f" ]] || { echo "GE19_D22AR2_NO_OVERWRITE $f"; exit 7; };done
mkdir -p "$ROOT/results"
TMP="$(mktemp -d)";trap 'rm -rf -- "$TMP"' EXIT
cd "$TMP"
echo GE19_D22AR2_LOCALIZE_ARCHIVED_D22A_FAILED_SHIFT_WITHOUT_RESOLVING
set +e
python3 -B -m ge19.h4f3d22a_r2_shift_constraint_serialization_repair   --results-dir "$ROOT/results" --repair26-trace "$TRACE"   --json-out "$J" --npz-out "$N" 2>&1 | tee "$F"
rc="${PIPESTATUS[0]}"
set -e
for f in "$J" "$N" "$F";do
  if [[ -s "$f" ]];then sha256sum "$f";wc -c "$f";fi
done
if [[ "$rc" -ne 0 || ! -s "$J" || ! -s "$N" ]];then
  echo GE19_D22AR2_DIAGNOSTIC_EXECUTION_FAIL
  [[ "$rc" -ne 0 ]] && exit "$rc" || exit 1
fi
python3 -B - "$J" <<'PYREPORT'
import json,sys
j=json.load(open(sys.argv[1]))
assert j["D22A_science_fail_immutable"] is True
assert j["Z11_certified"] is False and j["Z20_certified"] is False
assert j["q20_B20_recomputed"] is False and j["Z21_certified"] is False
print("GE19_D22AR2_SHIFT_LOCALIZATION_COMPLETE_PARENT_SCIENCE_FAIL_UNCHANGED",
      "reproduced="+str(j["original_action_D22A_shift_max_reproduced"]),flush=True)
PYREPORT
