#!/usr/bin/env bash
set -euo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
[[ "$(git symbolic-ref --quiet --short HEAD)" == "physics-first-gravitational-elasticity" ]] || { echo GE19_D22R3_WRONG_BRANCH; exit 4; }
if [[ -z "${VIRTUAL_ENV:-}" ]]; then
  [[ -f "$ROOT/.venv/bin/activate" ]] || { echo GE19_D22R3_VENV_MISSING; exit 5; }
  source "$ROOT/.venv/bin/activate"
fi
export PYTHONPATH="$ROOT" PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS="${OPENBLAS_NUM_THREADS:-1}"
check() { local got; [[ -s "$1" ]] || { echo "GE19_D22R3_MISSING $1"; exit 6; }; got="$(sha256sum "$1" | awk '{print $1}')"; [[ "$got" == "$2" ]] || { echo "GE19_D22R3_SHA_MISMATCH $1 $got"; exit 6; }; }
check "$ROOT/ge19/h4f3d22r3_direct_R2_boundary_reclosure.py" 3fe08c2296067c17c41a240a29e6d95302dfcd0ff31da99dd368814d53201536
check "$ROOT/ge19/h4f3d22r3_static_test.py" 15228dc421638a81125571a29c6a29cce1463f4f17d9a4613fecad6733900ac1
python3 -B "$ROOT/ge19/h4f3d22r3_static_test.py"
TRACE="${GE19_REPAIR26_R1_TRACE:-}"
if [[ -z "$TRACE" && -s "$ROOT/results/ge19_repair26_R1_full_history_trace.dat" ]]; then TRACE="$ROOT/results/ge19_repair26_R1_full_history_trace.dat"; fi
if [[ -z "$TRACE" && -d "$ROOT/frozen_repair26_repair27" ]]; then
  mapfile -d '' -t found < <(find "$ROOT/frozen_repair26_repair27" -type f -name ge19_repair26_R1_full_history_trace.dat -print0)
  if [[ "${#found[@]}" -eq 1 ]]; then TRACE="${found[0]}"; fi
fi
[[ -n "$TRACE" && -s "$TRACE" ]] || { echo GE19_D22R3_REPAIR26_TRACE_MISSING; exit 6; }
TRACE="$(realpath "$TRACE")"
check "$TRACE" 608ee0b4c868a701db6976f756b9a551cd9ddffe1e8e4ab37c5cd2361405a6f8
mkdir -p "$ROOT/results"
P="$ROOT/results/ge19_h4f3d22r3_fresh_R2_boundary_decision"
J="${P}.json";N="${P}.npz";FULL="${P}_FULL.log"
for f in "$J" "$N" "$FULL"; do [[ ! -e "$f" ]] || { echo "GE19_D22R3_NO_OVERWRITE $f";exit 7; };done
R28_ARGS=()
if [[ -n "${GE19_REPAIR28_R2_NPZ:-}" ]];then R28_ARGS=(--repair28-npz "$GE19_REPAIR28_R2_NPZ");fi
TMP="$(mktemp -d)";trap 'rm -rf -- "$TMP"' EXIT
mkdir -p "$TMP/results";cd "$TMP"
echo GE19_D22R3_ONE_DIRECT_FRESH_R2_BOUNDARY_DECISION_BEGIN
set +e
python3 -B -m ge19.h4f3d22r3_direct_R2_boundary_reclosure \
 --results-dir "$ROOT/results" --repair26-trace "$TRACE" "${R28_ARGS[@]}" \
 --json-out "$J" --npz-out "$N" 2>&1 | tee "$FULL"
rc="${PIPESTATUS[0]}"
set -e
for f in "$J" "$N" "$FULL"; do if [[ -s "$f" ]];then sha256sum "$f";wc -c "$f";fi;done
if [[ "$rc" -ne 0 || ! -s "$J" || ! -s "$N" ]];then echo GE19_D22R3_EXECUTION_FAIL;exit "$rc";fi
python3 -B - "$J" <<'PYCHECK'
import json,sys
r=json.load(open(sys.argv[1])); assert r['D22A_failure_immutable']
assert r['Z11_certified'] is False and r['Z20_certified'] is False
assert r['q20_B20_recomputed'] is False and r['Z21_certified'] is False
print('GE19_D22R3_RESULT',r['classification'])
PYCHECK
