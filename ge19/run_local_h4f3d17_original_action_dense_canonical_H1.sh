#!/usr/bin/env bash
# D17 physical source-action H1 dense NUMERICAL DIAGNOSTIC only; H1 enclosure/GE05 on-shell OPEN.
set -euo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
[[ "$(git symbolic-ref --quiet --short HEAD)" == "physics-first-gravitational-elasticity" ]] || {
 echo GE19_D17_WRONG_BRANCH;exit 4;
}
check(){
 local f="$1" want="$2" got
 [[ -s "$f" ]] || { echo "GE19_D17_REQUIRED_FILE_MISSING $f";exit 6; }
 got="$(sha256sum "$f" | awk '{print $1}')"
 [[ "$got" == "$want" ]] || {
  echo "GE19_D17_PARENT_OR_SOURCE_SHA_CHANGED $f $got";exit 6;
 }
}
check "$ROOT/ge19/h4f3d17_predata_original_action_dense_canonical_H1.json" 44661484ab84c84a6413e80a9adba0e2448d29e74866bb13bac102b585fe9358
check "$ROOT/ge19/h4f3d17_original_action_dense_H1_core.py" 5dc876539c08146d0bf204e5cbaf4b8e824d335f4458093c975453a3365608b2
check "$ROOT/ge19/h4f3d17_static_canonical_source_test.py" 9c138ebec9edea776b66c76bfd249c5e284be1a1d50c48f8fa4a286448f66711
check "$ROOT/ge19/h4f3d17_actual_original_action_dense_canonical_H1.py" 3fdce421b04e34f3f4d5342960a0375a1ac21412b5dd7c104256c2d5bb580227
check "$ROOT/ge19/h4f3d16_original_H1dot_Hermite_physical_bath_core.py" 43f16e8d503d8e58313dd524bf7fa17dc1c5e4aca538c86bb41a0b6973ad3276
check "$ROOT/ge19/h4f3d16_predata_original_H1dot_Hermite_physical_bath_bridge.json" 60307c4abfba8a476b966b5148132c694daf3806170d28445d5c98ed90170280
check "$ROOT/ge19/h4f3d16r1_actual_original_H1dot_Hermite_physical_bath.py" ef046df2698585a253085c8b58e3ffeea64fe4138130f29074aa6bde64644618
check "$ROOT/ge19/h4f3d16r1_predata_repair26_bracket_initialization.json" 6a2855ee34c91e6bb43ad82799396fc91ece0ee6afbc8ca300cfaf2ada01b92e
check "$ROOT/ge19/h4f3d17_original_action_dense_H1_core.py" 5dc876539c08146d0bf204e5cbaf4b8e824d335f4458093c975453a3365608b2
check "$ROOT/results/ge19_h4f3d16r1_actual_original_H1dot_Hermite_physical_bath.json" 4843901cf7b03e6a2657a55f1918d04641c4d84fde1b6d60f847b079b615d352
check "$ROOT/results/ge19_h4f3d16r1_actual_original_H1dot_Hermite_physical_bath.npz" 915709b21bae65c53f9521325a3920d4e0320b650e43458cad03109733d27a36

if [[ -z "${VIRTUAL_ENV:-}" ]]; then
 [[ -f "$ROOT/.venv/bin/activate" ]] || { echo GE19_D17_VENV_MISSING;exit 5; }
 source "$ROOT/.venv/bin/activate"
fi
export PYTHONPATH="$ROOT"
export PYTHONDONTWRITEBYTECODE=1
python3 -B -c 'import numpy,scipy,sympy'
python3 -B -m ge19.h4f3d17_static_canonical_source_test
TRACE="${GE19_REPAIR26_R1_TRACE:-}"
if [[ -z "$TRACE" && -s "$ROOT/results/ge19_repair26_R1_full_history_trace.dat" ]]; then
 TRACE="$ROOT/results/ge19_repair26_R1_full_history_trace.dat"
fi
if [[ -z "$TRACE" && -d "$ROOT/frozen_repair26_repair27" ]];then
 mapfile -d '' -t found < <(find "$ROOT/frozen_repair26_repair27" -type f -name ge19_repair26_R1_full_history_trace.dat -print0)
 if [[ "${#found[@]}" -eq 1 ]];then TRACE="${found[0]}";fi
fi
[[ -n "$TRACE" && -s "$TRACE" ]] || { echo GE19_D17_ORIGINAL_REPAIR26_TRACE_MISSING;exit 6; }
TRACE="$(realpath "$TRACE")"
check "$TRACE" 608ee0b4c868a701db6976f756b9a551cd9ddffe1e8e4ab37c5cd2361405a6f8
[[ "$(wc -c < "$TRACE" | tr -d ' ')" == 26643162 ]] || exit 6
J="$ROOT/results/ge19_h4f3d17_actual_original_action_dense_canonical_H1.json"
N="$ROOT/results/ge19_h4f3d17_actual_original_action_dense_canonical_H1.npz"
FULL="$ROOT/results/ge19_h4f3d17_actual_original_action_dense_canonical_H1_FULL.log"
for p in "$J" "$N" "$FULL";do
 [[ ! -e "$p" ]] || { echo "GE19_D17_NO_OVERWRITE $p";exit 7; }
done
TMP="$(mktemp -d)"
trap 'rm -rf -- "$TMP"' EXIT
cd "$TMP"
mkdir -p "$TMP/results"
echo GE19_D17_ACTUAL_ORIGINAL_ACTION_DENSE_H1_EXECUTION
set +e
python3 -B -m ge19.h4f3d17_actual_original_action_dense_canonical_H1 \
 --results-dir "$ROOT/results" --repair26-trace "$TRACE" \
 --json-out "$J" --npz-out "$N" 2>&1 | tee "$FULL" | tail -n 38
rc="${PIPESTATUS[0]}"
set -e
for p in "$J" "$N" "$FULL";do
 if [[ -s "$p" ]];then sha256sum "$p";wc -c "$p";fi
done
if [[ "$rc" == 0 && -s "$J" && -s "$N" ]];then
 echo GE19_D17_SOURCE_ACTION_DENSE_H1_NUMERICAL_DIAGNOSTIC_PASS_TRUE_CONTINUOUS_X10_AND_GE05_OPEN
else
 echo GE19_D17_IMPLEMENTATION_OR_SOURCE_FAIL
fi
exit "$rc"
