#!/usr/bin/env bash
set -euo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
[[ "$(git symbolic-ref --quiet --short HEAD)" == "physics-first-gravitational-elasticity" ]] || { echo GE19_D21_WRONG_BRANCH; exit 4; }
if [[ -z "${VIRTUAL_ENV:-}" ]];then
  [[ -f "$ROOT/.venv/bin/activate" ]] || { echo GE19_D21_VENV_MISSING; exit 5; }
  source "$ROOT/.venv/bin/activate"
fi
export PYTHONPATH="$ROOT" PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
check(){ local got; [[ -s "$1" ]] || { echo "GE19_D21_MISSING $1"; exit 6; }; got="$(sha256sum "$1" | awk '{print $1}')"; [[ "$got" == "$2" ]] || { echo "GE19_D21_SHA_MISMATCH $1 $got"; exit 6; }; }
check "$ROOT/ge19/h4f3d21_predata_GE05_phase_safe_M2_reclosure.json" 0806b43cff7477dd547cde1d813a17fd2ca38bd31a9d583114add05a573df17c
check "$ROOT/ge19/h4f3d21_GE05_phase_safe_M2_core.py" 8aefd593af4a54a0134551d962c7a4aa59f7c9ca553805f601cebef40ef1fab7
check "$ROOT/ge19/h4f3d21_actual_GE05_phase_safe_M2_reclosure.py" a31f7ef8c9f02c047dcaabaf96576205c79c5a18919f768b549a52549626cdef
check "$ROOT/ge19/h4f3d21_static_GE05_phase_safe_M2_test.py" 31166de5254b6df7df39d85869cc487bf790d512de53f02be4dc4fa60983a55a
check "$ROOT/ge19/h4f3d21_static_source_contract_test.py" 9ac4119d0d1f138cbc3d537779aca2e1d96021a3fc2c8e0e5735243fa5e7a1a7
check "$ROOT/results/ge19_h4f3d17_actual_original_action_dense_canonical_H1.json" 05154b61dfe9e6a35bd3d4c86a3fe46cbbc5d09bf2143d0e55de4e4310b00294
check "$ROOT/results/ge19_h4f3d17_actual_original_action_dense_canonical_H1.npz" cd3bcf8cf5ac9ab14385baa4d90bd53400daae9f2bb89d4d22bfa2a581846359
check "$ROOT/results/ge19_h4f3d19r1_actual_Cstar_Nt128_Nq2048_numerical_reclosure.json" 56027906e54bae8430203b796ab31182ae3ed743639714857bf6a6af38ec73de
check "$ROOT/results/ge19_h4f3d19r1_actual_Cstar_Nt128_Nq2048_numerical_reclosure.npz" 31a03042d467732d1463312c4a850c349c88411a0048a03d655caa16fc7dca86
check "$ROOT/results/ge19_h4f3d20r1_actual_Cstar_five_sources_GE05_ward_subset.json" 89b3da03257916f1d522574b6ab1747a7ed96892ec88d6c387624115fabdf6f9
check "$ROOT/results/ge19_h4f3d20r1_actual_Cstar_five_sources_GE05_ward_subset.npz" 1b44036ab9362015bf6e0b8faa1af78f58c050edc308a592eb787f7b26f309dc
python3 -B -m ge19.h4f3d21_static_GE05_phase_safe_M2_test
python3 -B -m ge19.h4f3d21_static_source_contract_test
TRACE="${GE19_REPAIR26_R1_TRACE:-}"
if [[ -z "$TRACE" && -s "$ROOT/results/ge19_repair26_R1_full_history_trace.dat" ]];then
  TRACE="$ROOT/results/ge19_repair26_R1_full_history_trace.dat"
fi
if [[ -z "$TRACE" && -d "$ROOT/frozen_repair26_repair27" ]];then
  mapfile -d '' -t found < <(find "$ROOT/frozen_repair26_repair27" -type f -name ge19_repair26_R1_full_history_trace.dat -print0)
  if [[ "${#found[@]}" -eq 1 ]];then TRACE="${found[0]}";fi
fi
[[ -n "$TRACE" && -s "$TRACE" ]] || { echo GE19_D21_REPAIR26_TRACE_MISSING; exit 6; }
TRACE="$(realpath "$TRACE")"
check "$TRACE" 608ee0b4c868a701db6976f756b9a551cd9ddffe1e8e4ab37c5cd2361405a6f8
mkdir -p "$ROOT/results"
PREFIX="$ROOT/results/ge19_h4f3d21_actual_Cstar_GE05_phase_safe_M2_source"
J="${PREFIX}.json";N="${PREFIX}.npz";FULL="${PREFIX}_FULL.log"
for f in "$J" "$N" "$FULL";do
  [[ ! -e "$f" ]] || { echo "GE19_D21_NO_OVERWRITE $f"; exit 7; }
done
TMP="$(mktemp -d)";trap 'rm -rf -- "$TMP"' EXIT
mkdir -p "$TMP/results"
cd "$TMP"
echo GE19_D21_ACTUAL_EXACT_ORIGINAL_ACTION_PT_M2_REPAIR_BEGIN
set +e
python3 -B -m ge19.h4f3d21_actual_GE05_phase_safe_M2_reclosure \
  --results-dir "$ROOT/results" --repair26-trace "$TRACE" \
  --json-out "$J" --npz-out "$N" 2>&1 | tee "$FULL"
rc="${PIPESTATUS[0]}"
set -e
for f in "$J" "$N" "$FULL";do
 if [[ -s "$f" ]];then sha256sum "$f";wc -c "$f";fi
done
if [[ "$rc" -ne 0 || ! -s "$J" || ! -s "$N" ]];then
  echo GE19_D21_SOURCE_REPAIR_EXECUTION_FAIL
  [[ "$rc" -eq 0 ]] && exit 1 || exit "$rc"
fi
python3 -B - "$J" <<'PYCHECK'
import json,sys
r=json.load(open(sys.argv[1]))
assert r['full_original_H4_Ward_certified'] is False
assert r['Z21_certified'] is False and r['lensing_licensed'] is False
assert r['new_physical_q20_and_Z11_recomputed'] is False
print('GE19_D21_RESULT',r['classification'])
PYCHECK
