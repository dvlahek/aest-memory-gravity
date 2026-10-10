#!/usr/bin/env bash
set -euo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
[[ "$(git symbolic-ref --quiet --short HEAD)" == "physics-first-gravitational-elasticity" ]] || { echo GE19_D23_WRONG_BRANCH;exit 4; }
if [[ -z "${VIRTUAL_ENV:-}" ]];then
 [[ -f "$ROOT/.venv/bin/activate" ]] || { echo GE19_D23_VENV_MISSING;exit 5; }
 source "$ROOT/.venv/bin/activate"
fi
export PYTHONPATH="$ROOT" PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS="${OPENBLAS_NUM_THREADS:-1}"
verify() { local got;[[ -s "$1" ]] || { echo "GE19_D23_MISSING $1";exit 6; };got="$(sha256sum "$1" | cut -d ' ' -f1)";[[ "$got" == "$2" ]] || { echo "GE19_D23_SHA_FAIL $1 $got";exit 6; }; }
verify "$ROOT/ge19/h4f3d23_action_constraint_boundary_transport.py" bec8a63ab96bfe8dd1d7b0b61e8f17731f4af8ac816e84df5a564daa1e43f63f
verify "$ROOT/ge19/h4f3d23_static_test.py" 1bcc8be78a4d74803b752609d5a6489732892a56a9b8146c7f5c9a138f48ff6e
python3 -B "$ROOT/ge19/h4f3d23_static_test.py"
TRACE="${GE19_REPAIR26_R1_TRACE:-}"
if [[ -z "$TRACE" && -s "$ROOT/results/ge19_repair26_R1_full_history_trace.dat" ]];then TRACE="$ROOT/results/ge19_repair26_R1_full_history_trace.dat";fi
if [[ -z "$TRACE" && -d "$ROOT/frozen_repair26_repair27" ]];then
 mapfile -d '' -t found < <(find "$ROOT/frozen_repair26_repair27" -type f -name ge19_repair26_R1_full_history_trace.dat -print0)
 if [[ "${#found[@]}" -eq 1 ]];then TRACE="${found[0]}";fi
fi
[[ -n "$TRACE" && -s "$TRACE" ]] || { echo GE19_D23_TRACE_MISSING;exit 6; }
TRACE="$(realpath "$TRACE")"
verify "$TRACE" 608ee0b4c868a701db6976f756b9a551cd9ddffe1e8e4ab37c5cd2361405a6f8
mkdir -p "$ROOT/results"
P="$ROOT/results/ge19_h4f3d23_action_constraint_boundary_transport"
J="${P}.json";N="${P}.npz";FULL="${P}_FULL.log"
for f in "$J" "$N" "$FULL";do [[ ! -e "$f" ]] || { echo "GE19_D23_REFUSE_OVERWRITE $f";exit 7; };done
TMP="$(mktemp -d)";trap 'rm -rf -- "$TMP"' EXIT
mkdir -p "$TMP/results";cd "$TMP"
echo GE19_D23_ACTION_CONSTRAINT_BOUNDARY_AND_H3_FIRST_INTERVAL_BEGIN
set +e
python3 -B -m ge19.h4f3d23_action_constraint_boundary_transport \
 --results-dir "$ROOT/results" --repair26-trace "$TRACE" \
 --json-out "$J" --npz-out "$N" 2>&1 | tee "$FULL"
rc="${PIPESTATUS[0]}"
set -e
for f in "$J" "$N" "$FULL";do if [[ -s "$f" ]];then sha256sum "$f";wc -c "$f";fi;done
if [[ "$rc" -ne 0 || ! -s "$J" || ! -s "$N" ]];then echo GE19_D23_EXECUTION_FAIL;exit 8;fi
python3 -B - "$J" <<'PYCHECK'
import json,sys
r=json.load(open(sys.argv[1]))
assert r['D22A_SCIENCE_FAIL_immutable'] is True and r['Z11_certified'] is False
assert r['Z20_certified'] is False and r['Z21_certified'] is False
assert r['full_H4_Ward_certified'] is False and r['q20_B20_recomputed'] is False
assert r['H3_40_modes_not_recomputed'] is True
print('GE19_D23_RESULT',r['classification'])
PYCHECK
