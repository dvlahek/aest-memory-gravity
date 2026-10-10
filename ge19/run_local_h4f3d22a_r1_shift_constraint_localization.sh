#!/usr/bin/env bash
set -euo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
[[ "$(git symbolic-ref --quiet --short HEAD)" == "physics-first-gravitational-elasticity" ]] || { echo GE19_D22AR1_WRONG_BRANCH; exit 4; }
if [[ -z "${VIRTUAL_ENV:-}" ]];then
  [[ -f "$ROOT/.venv/bin/activate" ]] || { echo GE19_D22AR1_VENV_MISSING; exit 5; }
  source "$ROOT/.venv/bin/activate"
fi
export PYTHONPATH="$ROOT" PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS="${OPENBLAS_NUM_THREADS:-1}"
[[ "$(sha256sum "$ROOT/ge19/h4f3d22a_r1_shift_constraint_localization.py" | awk '{print $1}')" == "96b640912b0dffe026a4238342a069615d3165f11f85b1f1c174ea333d45e74c" ]] || { echo GE19_D22AR1_SOURCE_SHA_FAIL; exit 6; }
python3 -B - <<'PYTEST'
from ge19.h4f3d22a_r1_shift_constraint_localization import manufactured
manufactured()
PYTEST
TRACE="${GE19_REPAIR26_R1_TRACE:-}"
if [[ -z "$TRACE" && -s "$ROOT/results/ge19_repair26_R1_full_history_trace.dat" ]];then TRACE="$ROOT/results/ge19_repair26_R1_full_history_trace.dat";fi
if [[ -z "$TRACE" && -d "$ROOT/frozen_repair26_repair27" ]];then
  mapfile -d '' -t found < <(find "$ROOT/frozen_repair26_repair27" -type f -name ge19_repair26_R1_full_history_trace.dat -print0)
  if [[ "${#found[@]}" -eq 1 ]];then TRACE="${found[0]}";fi
fi
[[ -n "$TRACE" && -s "$TRACE" ]] || { echo GE19_D22AR1_REPAIR26_TRACE_MISSING; exit 6; }
TRACE="$(realpath "$TRACE")"
[[ "$(sha256sum "$TRACE" | awk '{print $1}')" == "608ee0b4c868a701db6976f756b9a551cd9ddffe1e8e4ab37c5cd2361405a6f8" ]] || { echo GE19_D22AR1_REPAIR26_TRACE_SHA_FAIL; exit 6; }
J="$ROOT/results/ge19_h4f3d22a_r1_shift_forensic.json"
N="$ROOT/results/ge19_h4f3d22a_r1_shift_forensic.npz"
F="$ROOT/results/ge19_h4f3d22a_r1_shift_forensic_FULL.log"
for f in "$J" "$N" "$F";do [[ ! -e "$f" ]] || { echo "GE19_D22AR1_NO_OVERWRITE $f"; exit 7; };done
mkdir -p "$ROOT/results"
TMP="$(mktemp -d)";trap 'rm -rf -- "$TMP"' EXIT
cd "$TMP"
echo GE19_D22AR1_LOCALIZE_ARCHIVED_D22A_FAILED_SHIFT_WITHOUT_RESOLVING
set +e
python3 -B -m ge19.h4f3d22a_r1_shift_constraint_localization   --results-dir "$ROOT/results" --repair26-trace "$TRACE"   --json-out "$J" --npz-out "$N" 2>&1 | tee "$F"
rc="${PIPESTATUS[0]}"
set -e
for f in "$J" "$N" "$F";do
  if [[ -s "$f" ]];then sha256sum "$f";wc -c "$f";fi
done
if [[ "$rc" -ne 0 || ! -s "$J" || ! -s "$N" ]];then
  echo GE19_D22AR1_DIAGNOSTIC_EXECUTION_FAIL
  [[ "$rc" -ne 0 ]] && exit "$rc" || exit 1
fi
python3 -B - "$J" <<'PYREPORT'
import json,sys
j=json.load(open(sys.argv[1]))
assert j["D22A_science_fail_immutable"] is True
assert j["Z11_certified"] is False and j["Z20_certified"] is False
assert j["q20_B20_recomputed"] is False and j["Z21_certified"] is False
print("GE19_D22AR1_SHIFT_LOCALIZATION_COMPLETE_PARENT_SCIENCE_FAIL_UNCHANGED",
      "reproduced="+str(j["original_action_D22A_shift_max_reproduced"]),flush=True)
PYREPORT
