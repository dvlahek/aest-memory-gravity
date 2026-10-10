#!/usr/bin/env bash
set -euo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
[[ "$(git symbolic-ref --quiet --short HEAD)" == "physics-first-gravitational-elasticity" ]] || { echo GE19_D22A_WRONG_BRANCH; exit 4; }
if [[ -z "${VIRTUAL_ENV:-}" ]];then
  [[ -f "$ROOT/.venv/bin/activate" ]] || { echo GE19_D22A_VENV_MISSING; exit 5; }
  source "$ROOT/.venv/bin/activate"
fi
export PYTHONPATH="$ROOT" PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS="${OPENBLAS_NUM_THREADS:-1}"
check(){ local got; [[ -s "$1" ]] || { echo "GE19_D22A_MISSING $1"; exit 6; }; got="$(sha256sum "$1" | awk '{print $1}')"; [[ "$got" == "$2" ]] || { echo "GE19_D22A_SHA_MISMATCH $1 $got"; exit 6; }; }
check "$ROOT/ge19/h4f3d22a_predata_original_action_parent_reclosure.json" f54e51abd032bc226aa969dcf2d4c54b91af2d114fd7e77162f98b58f1a0efd3
check "$ROOT/ge19/h4f3d22a_action_parent_reclosure.py" ca3bd645bb3bf9f5755a55f1168501de57f93c8e39aa8da8f50e78c9a75f23f2
check "$ROOT/ge19/h4f3d22a_static_parent_contract_test.py" 7b8fafe014b5c5b77c163236a6a3ee33ffe12645c435b72024cbb4a961abbbb0
python3 -B "$ROOT/ge19/h4f3d22a_static_parent_contract_test.py"
TRACE="${GE19_REPAIR26_R1_TRACE:-}"
if [[ -z "$TRACE" && -s "$ROOT/results/ge19_repair26_R1_full_history_trace.dat" ]];then
  TRACE="$ROOT/results/ge19_repair26_R1_full_history_trace.dat"
fi
if [[ -z "$TRACE" && -d "$ROOT/frozen_repair26_repair27" ]];then
  mapfile -d '' -t found < <(find "$ROOT/frozen_repair26_repair27" -type f -name ge19_repair26_R1_full_history_trace.dat -print0)
  if [[ "${#found[@]}" -eq 1 ]];then TRACE="${found[0]}";fi
fi
[[ -n "$TRACE" && -s "$TRACE" ]] || { echo GE19_D22A_REPAIR26_TRACE_MISSING; exit 6; }
TRACE="$(realpath "$TRACE")"
check "$TRACE" 608ee0b4c868a701db6976f756b9a551cd9ddffe1e8e4ab37c5cd2361405a6f8
mkdir -p "$ROOT/results"
PREFIX="$ROOT/results/ge19_h4f3d22a_actual_Cstar_action_B10_Z11_Z20_parent_candidates"
J="${PREFIX}.json";N="${PREFIX}.npz";FULL="${PREFIX}_FULL.log"
for f in "$J" "$N" "$FULL";do
  [[ ! -e "$f" ]] || { echo "GE19_D22A_NO_OVERWRITE $f"; exit 7; }
done
TMP="$(mktemp -d)";trap 'rm -rf -- "$TMP"' EXIT
mkdir -p "$TMP/results"
cd "$TMP"
echo GE19_D22A_ACTUAL_CSTAR_D17_D19_DEPENDENT_PARENT_SOLVE_BEGIN
set +e
python3 -B -m ge19.h4f3d22a_action_parent_reclosure \
  --results-dir "$ROOT/results" --repair26-trace "$TRACE" \
  --json-out "$J" --npz-out "$N" 2>&1 | tee "$FULL"
rc="${PIPESTATUS[0]}"
set -e
for f in "$J" "$N" "$FULL";do
  if [[ -s "$f" ]];then sha256sum "$f";wc -c "$f";fi
done
if [[ "$rc" -ne 0 || ! -s "$J" || ! -s "$N" ]];then
  echo GE19_D22A_PARENT_EXECUTION_OR_SCIENCE_GATE_FAIL
  [[ "$rc" -eq 0 ]] && exit 1 || exit "$rc"
fi
python3 -B - "$J" <<'PYCHECK'
import json,sys
r=json.load(open(sys.argv[1]))
assert r['q20_and_B20_recomputed'] is False
assert r['Z21_certified'] is False and r['lensing_licensed'] is False
assert r['full_original_H4_Ward_certified'] is False
print('GE19_D22A_RESULT',r['classification'])
PYCHECK
