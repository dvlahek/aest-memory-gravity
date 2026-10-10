#!/usr/bin/env bash
# D19R1: one real Cstar numerical bath reclosure. Streaming output, no overwrite.
set -euo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
[[ "$(git symbolic-ref --quiet --short HEAD)" == "physics-first-gravitational-elasticity" ]] || {
  echo GE19_D19R1_WRONG_BRANCH; exit 4;
}
check() {
 local f="$1" want="$2" got
 [[ -s "$f" ]] || { echo "GE19_D19R1_REQUIRED_FILE_MISSING $f";exit 6; }
 got="$(sha256sum "$f" | awk '{print $1}')"
 [[ "$got" == "$want" ]] || { echo "GE19_D19R1_LOCK_CHANGED $f $got";exit 6; }
}
# All original source/file SHA checks are repeated inside the Python driver.
# These short checks fail early before the costly bath propagation.
check "$ROOT/ge19/h4f3d19r1_actual_source_action_bath_numerical_reclosure.py" 247e8e5b571ca53c082aa806fb3bb83e3ccc9e4f09b3496e3982e28684d35128
check "$ROOT/ge19/h4f3d19r1_physical_bath_numerical_core.py" 1b3f550bb11fcfec9eab0b6f45f9723627498dc14aeed413d2b4422036e24889
check "$ROOT/ge19/h4f3d19r1_static_numerical_reclosure_test.py" afe85f8bd4dda39f943b027f9c9f7020a14a3e7118112f585cd2c103f315f086
check "$ROOT/ge19/h4f3d19r1_predata_numerical_reclosure.json" 041475e4bfb5ef9d4e9856995077ae25797b17d0bde86a56763c35d7cb83d7a5
check "$ROOT/results/ge19_h4f3d15a_actual_original_R1_clock_conditional.npz" f7f9c94a341ec514d7d97ade297097b29102754231746531cde4485b61b2273c
check "$ROOT/results/ge19_h4f3d16r1_actual_original_H1dot_Hermite_physical_bath.json" 4843901cf7b03e6a2657a55f1918d04641c4d84fde1b6d60f847b079b615d352
check "$ROOT/results/ge19_h4f3d16r1_actual_original_H1dot_Hermite_physical_bath.npz" 915709b21bae65c53f9521325a3920d4e0320b650e43458cad03109733d27a36
check "$ROOT/results/ge19_h4f3d17_actual_original_action_dense_canonical_H1.json" 05154b61dfe9e6a35bd3d4c86a3fe46cbbc5d09bf2143d0e55de4e4310b00294
check "$ROOT/results/ge19_h4f3d17_actual_original_action_dense_canonical_H1.npz" cd3bcf8cf5ac9ab14385baa4d90bd53400daae9f2bb89d4d22bfa2a581846359

if [[ -z "${VIRTUAL_ENV:-}" ]];then
 [[ -f "$ROOT/.venv/bin/activate" ]] || { echo GE19_D19R1_VENV_MISSING;exit 5; }
 source "$ROOT/.venv/bin/activate"
fi
export PYTHONPATH="$ROOT"
export PYTHONDONTWRITEBYTECODE=1
export PYTHONUNBUFFERED=1
python3 -B -c 'import numpy,scipy,sympy'
python3 -B -m ge19.h4f3d19r1_static_numerical_reclosure_test
TRACE="${GE19_REPAIR26_R1_TRACE:-}"
if [[ -z "$TRACE" && -s "$ROOT/results/ge19_repair26_R1_full_history_trace.dat" ]];then
 TRACE="$ROOT/results/ge19_repair26_R1_full_history_trace.dat"
fi
if [[ -z "$TRACE" && -d "$ROOT/frozen_repair26_repair27" ]];then
 mapfile -d '' -t found < <(find "$ROOT/frozen_repair26_repair27" -type f -name ge19_repair26_R1_full_history_trace.dat -print0)
 if [[ "${#found[@]}" -eq 1 ]];then TRACE="${found[0]}";fi
fi
[[ -n "$TRACE" && -s "$TRACE" ]] || { echo GE19_D19R1_REPAIR26_TRACE_MISSING;exit 6; }
TRACE="$(realpath "$TRACE")"
check "$TRACE" 608ee0b4c868a701db6976f756b9a551cd9ddffe1e8e4ab37c5cd2361405a6f8
[[ "$(wc -c < "$TRACE" | tr -d ' ')" == 26643162 ]] || exit 6
mkdir -p "$ROOT/results"
PREFIX="$ROOT/results/ge19_h4f3d19r1_actual_Cstar_Nt128_Nq2048_numerical_reclosure"
J="${PREFIX}.json";N="${PREFIX}.npz";FULL="${PREFIX}_FULL.log"
for p in "$J" "$N" "$FULL";do
 [[ ! -e "$p" ]] || { echo "GE19_D19R1_NO_OVERWRITE $p";exit 7; }
done
TMP="$(mktemp -d)"
trap 'rm -rf -- "$TMP"' EXIT
cd "$TMP"
mkdir -p "$TMP/results"
echo GE19_D19R1_ACTUAL_ORIGINAL_ACTION_PHYSICAL_BATH_EXECUTION
set +e
python3 -B -m ge19.h4f3d19r1_actual_source_action_bath_numerical_reclosure \
 --results-dir "$ROOT/results" --repair26-trace "$TRACE" \
 --json-out "$J" --npz-out "$N" 2>&1 | tee "$FULL"
rc="${PIPESTATUS[0]}"
set -e
for p in "$J" "$N" "$FULL";do
 if [[ -s "$p" ]];then sha256sum "$p";wc -c "$p";fi
done
if [[ "$rc" != 0 || ! -s "$J" || ! -s "$N" ]];then
 echo GE19_D19R1_EXECUTION_OR_SOURCE_FAIL
 if [[ "$rc" == 0 ]];then exit 1;else exit "$rc";fi
fi
if python3 -B -c 'import json,sys;sys.exit(0 if json.load(open(sys.argv[1]))["numerical_tol_pass"] else 1)' "$J";then
 echo GE19_D19R1_CSTAR_BATH_NUMERICAL_TOLERANCE_PASS_D17_H1_FULL_H4_OPEN
else
 echo GE19_D19R1_CSTAR_BATH_NUMERICAL_TOLERANCE_NOT_CLOSED_D17_H1_FULL_H4_OPEN
fi
