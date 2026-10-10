#!/usr/bin/env bash
# D18 polynomial-surrogate conditional Bernstein; original-action H1/GE05 OPEN.
set -euo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
[[ "$(git symbolic-ref --quiet --short HEAD)" == "physics-first-gravitational-elasticity" ]] || { echo GE19_D18_WRONG_BRANCH;exit 4; }
check(){
 local f="$1" want="$2" got
 [[ -s "$f" ]] || { echo "GE19_D18_REQUIRED_FILE_MISSING $f";exit 6; }
 got="$(sha256sum "$f" | awk '{print $1}')"
 [[ "$got" == "$want" ]] || { echo "GE19_D18_PARENT_OR_SOURCE_SHA_CHANGED $f $got";exit 6; }
}
check "$ROOT/ge19/h4f3d18_predata_source_action_bernstein_canonical_H1.json" 699fd676a3278e2af77c47cec2613aacd04a29aaedaf381f28a24663c8c10aba
check "$ROOT/ge19/h4f3d18_bernstein_affine_canonical_H1_core.py" f8a1757790cb2bee8e14b1bd4b4e04563ed0e5354782dfbe409c58db52f2d489
check "$ROOT/ge19/h4f3d18_actual_source_action_Bernstein_canonical_H1.py" 60c4012e5223ce96c3df82587a200e26513023782e9b84e795022b913f149e93
check "$ROOT/ge19/h4f3d18_static_bernstein_test.py" 87cf7b522fefa81de01cd9f6a2c1e287edc0abc05edc5f7a773ac167fd4a99dc
check "$ROOT/ge19/h4f3d17_predata_original_action_dense_canonical_H1.json" 44661484ab84c84a6413e80a9adba0e2448d29e74866bb13bac102b585fe9358
check "$ROOT/results/ge19_h4f3d17_actual_original_action_dense_canonical_H1.json" 05154b61dfe9e6a35bd3d4c86a3fe46cbbc5d09bf2143d0e55de4e4310b00294
check "$ROOT/results/ge19_h4f3d17_actual_original_action_dense_canonical_H1.npz" cd3bcf8cf5ac9ab14385baa4d90bd53400daae9f2bb89d4d22bfa2a581846359
check "$ROOT/results/ge19_h4f3d16r1_actual_original_H1dot_Hermite_physical_bath.json" 4843901cf7b03e6a2657a55f1918d04641c4d84fde1b6d60f847b079b615d352
check "$ROOT/results/ge19_h4f3d16r1_actual_original_H1dot_Hermite_physical_bath.npz" 915709b21bae65c53f9521325a3920d4e0320b650e43458cad03109733d27a36
if [[ -z "${VIRTUAL_ENV:-}" ]];then
 [[ -f "$ROOT/.venv/bin/activate" ]] || { echo GE19_D18_VENV_MISSING;exit 5; }
 source "$ROOT/.venv/bin/activate"
fi
export PYTHONPATH="$ROOT"
export PYTHONDONTWRITEBYTECODE=1
python3 -B -c 'import numpy,scipy,sympy'
python3 -B -m ge19.h4f3d18_static_bernstein_test
python3 -B -m ge19.h4f3d17_static_canonical_source_test
TRACE="${GE19_REPAIR26_R1_TRACE:-}"
if [[ -z "$TRACE" && -s "$ROOT/results/ge19_repair26_R1_full_history_trace.dat" ]]; then
 TRACE="$ROOT/results/ge19_repair26_R1_full_history_trace.dat"
fi
if [[ -z "$TRACE" && -d "$ROOT/frozen_repair26_repair27" ]];then
 mapfile -d '' -t found < <(find "$ROOT/frozen_repair26_repair27" -type f -name ge19_repair26_R1_full_history_trace.dat -print0)
 if [[ "${#found[@]}" -eq 1 ]];then TRACE="${found[0]}";fi
fi
[[ -n "$TRACE" && -s "$TRACE" ]] || { echo GE19_D18_ORIGINAL_REPAIR26_TRACE_MISSING;exit 6; }
TRACE="$(realpath "$TRACE")"
check "$TRACE" 608ee0b4c868a701db6976f756b9a551cd9ddffe1e8e4ab37c5cd2361405a6f8
[[ "$(wc -c < "$TRACE" | tr -d ' ')" == 26643162 ]] || exit 6
J="$ROOT/results/ge19_h4f3d18_actual_source_action_Bernstein_canonical_H1.json"
N="$ROOT/results/ge19_h4f3d18_actual_source_action_Bernstein_canonical_H1.npz"
FULL="$ROOT/results/ge19_h4f3d18_actual_source_action_Bernstein_canonical_H1_FULL.log"
for p in "$J" "$N" "$FULL";do
 [[ ! -e "$p" ]] || { echo "GE19_D18_NO_OVERWRITE $p";exit 7; }
done
TMP="$(mktemp -d)"
trap 'rm -rf -- "$TMP"' EXIT
cd "$TMP"
echo GE19_D18_ACTUAL_ORIGINAL_ACTION_AFFINE_OPERATOR_BERNSTEIN_EXECUTION
set +e
python3 -B -m ge19.h4f3d18_actual_source_action_Bernstein_canonical_H1 \
 --results-dir "$ROOT/results" --repair26-trace "$TRACE" \
 --json-out "$J" --npz-out "$N" 2>&1 | tee "$FULL"
rc="${PIPESTATUS[0]}"
set -e
for p in "$J" "$N" "$FULL";do
 if [[ -s "$p" ]];then sha256sum "$p";wc -c "$p";fi
done
if [[ "$rc" == 0 && -s "$J" && -s "$N" ]];then
 echo GE19_D18_BERNSTEIN_AFFINE_SURROGATE_DIAGNOSTIC_PASS_TRUE_ACTION_H1_GE05_OPEN
else
 echo GE19_D18_IMPLEMENTATION_OR_SOURCE_FAIL
fi
exit "$rc"
