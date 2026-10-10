#!/usr/bin/env bash
# D16: frozen original H3F H1dot -> conditional Hermite drive -> physical GE05 bath.
# True off-grid H1 and all-interval/on-shell GE05 still OPEN.
set -euo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
[[ "$(git symbolic-ref --quiet --short HEAD)" == "physics-first-gravitational-elasticity" ]] || {
  echo GE19_H4F3D16_WRONG_BRANCH; exit 4;
}
check() {
  local f="$1" want="$2" got
  [[ -s "$f" ]] || { echo "GE19_H4F3D16_REQUIRED_FILE_MISSING $f"; exit 6; }
  got="$(sha256sum "$f" | awk '{print $1}')"
  [[ "$got" == "$want" ]] || {
    echo "GE19_H4F3D16_SOURCE_OR_ACTUAL_PARENT_SHA_CHANGED $f $got"; exit 6;
  }
}
check "$ROOT/ge19/h4f3d16_predata_original_H1dot_Hermite_physical_bath_bridge.json" 60307c4abfba8a476b966b5148132c694daf3806170d28445d5c98ed90170280
check "$ROOT/ge19/h4f3d16_original_H1dot_Hermite_physical_bath_core.py" 43f16e8d503d8e58313dd524bf7fa17dc1c5e4aca538c86bb41a0b6973ad3276
check "$ROOT/ge19/h4f3d16_actual_original_H1dot_Hermite_physical_bath.py" 59b0744421f93209ece1e4062bb56d2b6612f6c3aef303af21cd859dd1acfa31
check "$ROOT/ge19/h4f3d16_static_source_and_physical_clock_test.py" d6c878593866be5c8e60d434d9e09adaaed00bf41ebedbddedac8deb75f25c50
check "$ROOT/results/ge19_h4f3d15a_actual_original_R1_clock_conditional.json" cad2a1c548582177d49019153fab34aa5b0ab520c7dd62f361c9e780af22794d
check "$ROOT/results/ge19_h4f3d15a_actual_original_R1_clock_conditional.npz" f7f9c94a341ec514d7d97ade297097b29102754231746531cde4485b61b2273c
if [[ -z "${VIRTUAL_ENV:-}" ]]; then
  [[ -f "$ROOT/.venv/bin/activate" ]] || { echo GE19_H4F3D16_VENV_MISSING;exit 5; }
  source "$ROOT/.venv/bin/activate"
fi
export PYTHONPATH="$ROOT"
export PYTHONDONTWRITEBYTECODE=1
python3 -B -c 'import numpy,scipy,sympy'
python3 -B -m ge19.h4f3d16_static_source_and_physical_clock_test
echo GE19_H4F3D16_SOURCE_PREREG_STATIC_PASS_ACTUAL_PARENT_RUN_OPEN
TRACE="${GE19_REPAIR26_R1_TRACE:-}"
if [[ -z "$TRACE" && -s "$ROOT/results/ge19_repair26_R1_full_history_trace.dat" ]]; then
  TRACE="$ROOT/results/ge19_repair26_R1_full_history_trace.dat"
fi
if [[ -z "$TRACE" && -d "$ROOT/frozen_repair26_repair27" ]]; then
  mapfile -d '' -t found < <(find "$ROOT/frozen_repair26_repair27" -type f -name ge19_repair26_R1_full_history_trace.dat -print0)
  if [[ "${#found[@]}" -eq 1 ]]; then TRACE="${found[0]}"; fi
fi
[[ -n "$TRACE" && -s "$TRACE" ]] || { echo GE19_H4F3D16_ORIGINAL_R1_TRACE_MISSING;exit 6; }
TRACE="$(realpath "$TRACE")"
check "$TRACE" 608ee0b4c868a701db6976f756b9a551cd9ddffe1e8e4ab37c5cd2361405a6f8
[[ "$(wc -c < "$TRACE" | tr -d ' ')" == 26643162 ]] || exit 6
check "$ROOT/results/ge19_h4f3d13_actual_original_r1_signed_interval_bath_parent.json" 2b4dfbd30ec6466292e0dcf62eeed8b723555d1890a127a5e0a6ff761d2ebe76
check "$ROOT/results/ge19_h4f3d13_actual_original_r1_signed_interval_bath_parent.npz" 1608fe98dd924b2b235ecf0f8fce768f2f3a2fa4a2854de04a56fe622ad3df89
check "$ROOT/results/ge19_h4f3d14_actual_original_r1_source_weighted_phase_bath.json" 8d8244cf810447c96df82f6ece6c161a4dd0553f707e3a698ed0b29f37ff3c6e
check "$ROOT/results/ge19_h4f3d14_actual_original_r1_source_weighted_phase_bath.npz" f79d87f10dc1561ef2c61997b7952d62d85eda6674abaa015e5d38e161b55c48
echo GE19_H4F3D16_ACTUAL_ORIGINAL_R1_D13_D14_D15A_PARENT_SHA_PASS
J="$ROOT/results/ge19_h4f3d16_actual_original_H1dot_Hermite_physical_bath.json"
N="$ROOT/results/ge19_h4f3d16_actual_original_H1dot_Hermite_physical_bath.npz"
FULL="$ROOT/results/ge19_h4f3d16_actual_original_H1dot_Hermite_physical_bath_FULL.log"
for p in "$J" "$N" "$FULL"; do
  [[ ! -e "$p" ]] || { echo "GE19_H4F3D16_NO_OVERWRITE $p";exit 7; }
done
TMP="$(mktemp -d)"
trap 'rm -rf -- "$TMP"' EXIT
cd "$TMP"
mkdir -p "$TMP/results"
echo GE19_H4F3D16_ACTUAL_ORIGINAL_H1DOT_HERMITE_PHYSICAL_BATH_EXECUTION
set +e
python3 -B -m ge19.h4f3d16_actual_original_H1dot_Hermite_physical_bath \
  --results-dir "$ROOT/results" --repair26-trace "$TRACE" \
  --json-out "$J" --npz-out "$N" 2>&1 | tee "$FULL" | tail -n 32
rc="${PIPESTATUS[0]}"
set -e
for p in "$J" "$N" "$FULL"; do
  if [[ -s "$p" ]]; then sha256sum "$p"; wc -c "$p"; fi
done
if [[ "$rc" == 0 && -s "$J" && -s "$N" ]]; then
  echo GE19_H4F3D16_ORIGINAL_PHYSICAL_HERMITE_SURROGATE_DIAGNOSTIC_PASS_TRUE_X10_GE05_ONSHELL_OPEN
else
  echo GE19_H4F3D16_IMPLEMENTATION_OR_ORIGINAL_SOURCE_FAIL
fi
exit "$rc"
