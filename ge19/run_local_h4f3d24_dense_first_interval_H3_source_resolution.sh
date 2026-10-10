#!/usr/bin/env bash
set -euo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
[[ "$(git symbolic-ref --quiet --short HEAD)" == "physics-first-gravitational-elasticity" ]] || { echo GE19_D24_WRONG_BRANCH;exit 4; }
if [[ -z "${VIRTUAL_ENV:-}" ]];then
 [[ -f "$ROOT/.venv/bin/activate" ]] || { echo GE19_D24_VENV_MISSING;exit 5; }
 source "$ROOT/.venv/bin/activate"
fi
export PYTHONPATH="$ROOT" PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS="${OPENBLAS_NUM_THREADS:-1}"
verify() { local got;[[ -s "$1" ]] || { echo "GE19_D24_MISSING $1";exit 6; };got="$(sha256sum "$1" | cut -d ' ' -f1)";[[ "$got" == "$2" ]] || { echo "GE19_D24_SHA_FAIL $1 $got";exit 6; }; }
verify "$ROOT/ge19/h4f3d24_dense_first_interval_H3_source_transport.py" d7d1994e04a5262b8aea898ca9010874a99a4238248dc335f514db9aa674cf11
verify "$ROOT/ge19/h4f3d24_static_first_interval_test.py" c04795c58035958e036ed6cebf3b6fd319d7e514ad6de2eb219759e37649dad7
verify "$ROOT/ge19/h4f3d24_predata_dense_first_interval_H3_source_transport.json" adc9cf2d020594d07c146b0cf1fddb96223b9c12a684bebee2fd0ee24381ae2a
python3 -B "$ROOT/ge19/h4f3d24_static_first_interval_test.py"
TRACE="${GE19_REPAIR26_R1_TRACE:-}"
if [[ -z "$TRACE" && -s "$ROOT/results/ge19_repair26_R1_full_history_trace.dat" ]];then TRACE="$ROOT/results/ge19_repair26_R1_full_history_trace.dat";fi
if [[ -z "$TRACE" && -d "$ROOT/frozen_repair26_repair27" ]];then
 mapfile -d '' -t found < <(find "$ROOT/frozen_repair26_repair27" -type f -name ge19_repair26_R1_full_history_trace.dat -print0)
 if [[ "${#found[@]}" -eq 1 ]];then TRACE="${found[0]}";fi
fi
[[ -n "$TRACE" && -s "$TRACE" ]] || { echo GE19_D24_TRACE_MISSING;exit 6; }
TRACE="$(realpath "$TRACE")"
verify "$TRACE" 608ee0b4c868a701db6976f756b9a551cd9ddffe1e8e4ab37c5cd2361405a6f8
mkdir -p "$ROOT/results"
P="$ROOT/results/ge19_h4f3d24_dense_first_interval_H3_source_resolution"
J="${P}.json";N="${P}.npz";FULL="${P}_FULL.log"
for f in "$J" "$N" "$FULL";do [[ ! -e "$f" ]] || { echo "GE19_D24_REFUSE_OVERWRITE $f";exit 7; };done
TMP="$(mktemp -d)";trap 'rm -rf -- "$TMP"' EXIT
mkdir -p "$TMP/results";cd "$TMP"
echo GE19_D24_D17_DENSE_ACTION_H3_FIRST_INTERVAL_BEGIN
set +e
python3 -B -m ge19.h4f3d24_dense_first_interval_H3_source_transport \
 --results-dir "$ROOT/results" --repair26-trace "$TRACE" \
 --json-out "$J" --npz-out "$N" 2>&1 | tee "$FULL"
rc="${PIPESTATUS[0]}"
set -e
for f in "$J" "$N" "$FULL";do if [[ -s "$f" ]];then sha256sum "$f";wc -c "$f";fi;done
if [[ "$rc" -ne 0 || ! -s "$J" || ! -s "$N" ]];then echo GE19_D24_EXECUTION_FAIL;exit 8;fi
python3 -B - "$J" <<'PYCHECK'
import json,sys,numpy as np
r=json.load(open(sys.argv[1]))
assert r['D22A_SCIENCE_FAIL_immutable'] is True and r['Z11_certified'] is False
assert r['Z20_certified'] is False and r['original_action_H3_full_Ward_certified'] is False
assert r['q20_B20_recomputed'] is False and r['H4_Z21_solve_performed'] is False
assert len(r['selected_first_step'])==3 and all(np.isfinite(t['dense']['first_step_shift_backward']) for t in r['selected_first_step'])
print('GE19_D24_RESULT',r['classification'])
PYCHECK
