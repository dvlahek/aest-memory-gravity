#!/usr/bin/env bash
# D20: progress-streamed dependent-source numerical diagnostic, no parent overwrite.
set -euo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
[[ "$(git symbolic-ref --quiet --short HEAD)" == "physics-first-gravitational-elasticity" ]] || { echo GE19_D20R1_WRONG_BRANCH; exit 4; }
if [[ -z "${VIRTUAL_ENV:-}" ]];then
 [[ -f "$ROOT/.venv/bin/activate" ]] || { echo GE19_D20R1_VENV_MISSING; exit 5; }
 source "$ROOT/.venv/bin/activate"
fi
export PYTHONPATH="$ROOT" PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
check(){ local got; [[ -s "$1" ]] || { echo "GE19_D20R1_MISSING $1"; exit 6; }; got="$(sha256sum "$1" | awk '{print $1}')"; [[ "$got" == "$2" ]] || { echo "GE19_D20R1_PARENT_SHA_MISMATCH $1 $got"; exit 6; }; }
check "$ROOT/ge19/h4f3d20r1_predata_canonical_backward_repair.json" 2e0fa8c227d66ecac1365729714ce09192924c30734e60c97f3a8da2f86ed088
check "$ROOT/results/ge19_h4f3d17_actual_original_action_dense_canonical_H1.json" 05154b61dfe9e6a35bd3d4c86a3fe46cbbc5d09bf2143d0e55de4e4310b00294
check "$ROOT/results/ge19_h4f3d17_actual_original_action_dense_canonical_H1.npz" cd3bcf8cf5ac9ab14385baa4d90bd53400daae9f2bb89d4d22bfa2a581846359
check "$ROOT/results/ge19_h4f3d19r1_actual_Cstar_Nt128_Nq2048_numerical_reclosure.json" 56027906e54bae8430203b796ab31182ae3ed743639714857bf6a6af38ec73de
check "$ROOT/results/ge19_h4f3d19r1_actual_Cstar_Nt128_Nq2048_numerical_reclosure.npz" 31a03042d467732d1463312c4a850c349c88411a0048a03d655caa16fc7dca86
check "$ROOT/ge19/h4f3d20_recompute_five_sources_and_bath_ward.py" a81871e76b32c81c16367330a16bc081219e2aa9779ecf5baf8433d51bed88f7
check "$ROOT/ge19/h4f3d20r1_recompute_five_sources_and_bath_ward.py" 6dcaae0648dda370f8c84483b60594556c8e38dd8d7f162ed57dca0dcc1b7e41
check "$ROOT/ge19/h4f3d20r1_static_canonical_backward_test.py" 04c9159760d6a2d698cfa733dc922acb0999c82111376df6c5ff00203c4e7868
python3 -B -m ge19.h4f3d20r1_static_canonical_backward_test
TRACE="${GE19_REPAIR26_R1_TRACE:-}"
if [[ -z "$TRACE" && -s "$ROOT/results/ge19_repair26_R1_full_history_trace.dat" ]];then TRACE="$ROOT/results/ge19_repair26_R1_full_history_trace.dat";fi
if [[ -z "$TRACE" && -d "$ROOT/frozen_repair26_repair27" ]];then
 mapfile -d '' -t found < <(find "$ROOT/frozen_repair26_repair27" -type f -name ge19_repair26_R1_full_history_trace.dat -print0)
 if [[ "${#found[@]}" -eq 1 ]];then TRACE="${found[0]}";fi
fi
[[ -n "$TRACE" && -s "$TRACE" ]] || { echo GE19_D20R1_REPAIR26_TRACE_MISSING; exit 6; }
TRACE="$(realpath "$TRACE")"
check "$TRACE" 608ee0b4c868a701db6976f756b9a551cd9ddffe1e8e4ab37c5cd2361405a6f8
mkdir -p "$ROOT/results"
PREFIX="$ROOT/results/ge19_h4f3d20r1_actual_Cstar_five_sources_GE05_ward_subset"
J="${PREFIX}.json";N="${PREFIX}.npz";FULL="${PREFIX}_FULL.log"
for f in "$J" "$N" "$FULL";do [[ ! -e "$f" ]] || { echo "GE19_D20R1_NO_OVERWRITE $f"; exit 7; };done
TMP="$(mktemp -d)";trap 'rm -rf -- "$TMP"' EXIT
mkdir -p "$TMP/results"
cd "$TMP"
echo GE19_D20R1_ACTUAL_D17_D19R1_DEPENDENT_SOURCE_EXECUTION
set +e
python3 -B -m ge19.h4f3d20r1_recompute_five_sources_and_bath_ward \
 --results-dir "$ROOT/results" --repair26-trace "$TRACE" \
 --json-out "$J" --npz-out "$N" 2>&1 | tee "$FULL"
rc="${PIPESTATUS[0]}"
set -e
for f in "$J" "$N" "$FULL";do if [[ -s "$f" ]];then sha256sum "$f";wc -c "$f";fi;done
if [[ "$rc" -ne 0 || ! -s "$J" || ! -s "$N" ]];then
 echo GE19_D20R1_EXECUTION_OR_SOURCE_FAIL; [[ "$rc" -eq 0 ]] && exit 1 || exit "$rc"
fi
python3 -B - "$J" <<'PY'
import json,sys
r=json.load(open(sys.argv[1])); print('GE19_D20R1_RESULT',r['classification'])
assert not r['full_original_H4_Ward_certified']
assert not r['Z21_certified']
PY
