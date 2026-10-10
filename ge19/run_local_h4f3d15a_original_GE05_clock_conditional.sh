#!/usr/bin/env bash
# D15a actual original R1 x-embedded GE05 CLOCK + CONDITIONAL DRIVE collocation.
# No true continuous X10, all-time residual certificate, bath on-shell or H4 claim.
set -euo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
[[ "$(git symbolic-ref --quiet --short HEAD)" == "physics-first-gravitational-elasticity" ]] || {
  echo GE19_H4F3D15A_WRONG_BRANCH; exit 4;
}
# The new files are protected by their preregistered raw SHA-256 values;
# historical ORIGINAL sources remain pinned to the immutable HEAD Git blobs.
PINS=(
  "ge05/memory_directional_source_generator.py:40837d77f89028da30c28899e2d0530a4401844e"
  "ge19/repair13_self_consistent_reduced_background_h1_reclosure.py:362d63d03d7b850fceae393f535353ded79aeea7"
  "ge19/repair07_window_retarded_reduced_h3_z20_particular.py:e34d28a2062c748f48bc82fa928844b02631de25"
  "ge19/repair24_q20_construction.py:fc271987d1bddcd023cc9c057ddcad036b1d72fb"
  "ge19/h4f3d13_actual_original_r1_signed_interval_bath_parent.py:5cce06a82869d5b7ff70c12a92e70b9257073c42"
  "ge19/h4f3d14_actual_original_r1_source_weighted_phase_bath.py:cb823960e9b2cf1b82b1accd458ec75f4acf4547"
  "ge19/h4f3d14_actual_original_r1_source_weighted_phase_bath_independent_archive_audit.json:3f7acc17aee24c6b776578ef2b654a40b2db6af0"
)
for entry in "${PINS[@]}"; do
  rel="${entry%%:*}"; want="${entry#*:}"
  [[ "$(git rev-parse "HEAD:$rel")" == "$want" ]] || {
    echo "GE19_H4F3D15A_ORIGINAL_HEAD_BLOB_CHANGED $rel"; exit 4;
  }
  [[ "$(git hash-object "$ROOT/$rel")" == "$want" ]] || {
    echo "GE19_H4F3D15A_ORIGINAL_WORKTREE_BLOB_CHANGED $rel"; exit 4;
  }
done
check() {
  local file="$1" want="$2" got
  [[ -s "$file" ]] || { echo "GE19_H4F3D15A_MISSING $file"; exit 6; }
  got="$(sha256sum "$file" | awk '{print $1}')"
  [[ "$got" == "$want" ]] || {
    echo "GE19_H4F3D15A_INPUT_OR_SOURCE_SHA_CHANGED $file $got"; exit 6;
  }
}
check "$ROOT/ge19/h4f3d15a_predata_original_GE05_clock_consistent_conditional_collocation.json" c5cb22394dc8eabf12c9fe8d5f6acd57a24d90f356976122864723ec73513745
check "$ROOT/ge19/h4f3d15a_original_GE05_clock_embedded_source.py" 14da31797282fb7959c44793f04751f1dd0ff25765424e566ca6015e759a82ae
check "$ROOT/ge19/h4f3d15a_actual_original_R1_clock_conditional.py" 7006c5afc9cea07ee2d076ea518ad81d0722c5f19236e73d34f4f8818c1496ec
check "$ROOT/ge19/h4f3d15a_static_clock_source_test.py" 0a313f7fc4e49e56236e8673e58c523607b6c6ca309df6e22668b5a71947de21
check "$ROOT/ge19/h4f3d15a1_predata_original_GE05_interface_current_jump.json" da56f2c42e11ce480ee72a888f725d422c71a2e7a3c2c19d8b19cabda752874c
check "$ROOT/ge19/h4f3d15a1_original_GE05_interface_current_jump.py" d5e55055348cfeb9462d566d436e91da563d77c7b3f6d36b914a73c7711cce2c
check "$ROOT/ge19/h4f3d15a1_static_interface_test.py" e8fc7f30203acc75c271f1187fa930a4c3cd7a51500ff259fa2a1298cd515add
bash -n "$ROOT/ge19/run_local_h4f3d15a_original_GE05_clock_conditional.sh"
echo GE19_H4F3D15A_PREREG_AND_ORIGINAL_SOURCE_LOCK_PASS
if [[ -z "${VIRTUAL_ENV:-}" ]]; then
  [[ -f "$ROOT/.venv/bin/activate" ]] || {
    echo GE19_H4F3D15A_VENV_MISSING; exit 5;
  }
  source "$ROOT/.venv/bin/activate"
fi
export PYTHONPATH="$ROOT"
export PYTHONDONTWRITEBYTECODE=1
python3 -B -c 'import numpy,scipy,sympy'
python3 -B -m ge19.h4f3d15a_static_clock_source_test
python3 -B -m ge19.h4f3d15a1_static_interface_test
TRACE="${GE19_REPAIR26_R1_TRACE:-}"
if [[ -z "$TRACE" && -s "$ROOT/results/ge19_repair26_R1_full_history_trace.dat" ]]; then
  TRACE="$ROOT/results/ge19_repair26_R1_full_history_trace.dat"
fi
if [[ -z "$TRACE" && -d "$ROOT/frozen_repair26_repair27" ]]; then
  mapfile -d '' -t found < <(find "$ROOT/frozen_repair26_repair27" -type f -name ge19_repair26_R1_full_history_trace.dat -print0)
  if [[ "${#found[@]}" -eq 1 ]]; then TRACE="${found[0]}"; fi
fi
[[ -n "$TRACE" && -s "$TRACE" ]] || {
  echo GE19_H4F3D15A_ORIGINAL_R1_TRACE_MISSING_OR_AMBIGUOUS; exit 6;
}
TRACE="$(realpath "$TRACE")"
check "$TRACE" 608ee0b4c868a701db6976f756b9a551cd9ddffe1e8e4ab37c5cd2361405a6f8
[[ "$(wc -c < "$TRACE" | tr -d ' ')" == "26643162" ]] || exit 6
check "$ROOT/results/ge19_h4f3d13_actual_original_r1_signed_interval_bath_parent.json" 2b4dfbd30ec6466292e0dcf62eeed8b723555d1890a127a5e0a6ff761d2ebe76
check "$ROOT/results/ge19_h4f3d13_actual_original_r1_signed_interval_bath_parent.npz" 1608fe98dd924b2b235ecf0f8fce768f2f3a2fa4a2854de04a56fe622ad3df89
check "$ROOT/results/ge19_h4f3d14_actual_original_r1_source_weighted_phase_bath.json" 8d8244cf810447c96df82f6ece6c161a4dd0553f707e3a698ed0b29f37ff3c6e
check "$ROOT/results/ge19_h4f3d14_actual_original_r1_source_weighted_phase_bath.npz" f79d87f10dc1561ef2c61997b7952d62d85eda6674abaa015e5d38e161b55c48
echo GE19_H4F3D15A_ORIGINAL_R1_D13_D14_ACTUAL_PARENT_SHA_PASS
JSON="$ROOT/results/ge19_h4f3d15a_actual_original_R1_clock_conditional.json"
NPZ="$ROOT/results/ge19_h4f3d15a_actual_original_R1_clock_conditional.npz"
FULL="$ROOT/results/ge19_h4f3d15a_actual_original_R1_clock_conditional_FULL.log"
for out in "$JSON" "$NPZ" "$FULL"; do
  [[ ! -e "$out" ]] || {
    echo "GE19_H4F3D15A_NO_OVERWRITE $out"; exit 7;
  }
done
TMP="$(mktemp -d)"
trap 'rm -rf -- "$TMP"' EXIT
mkdir -p "$TMP/results"
cd "$TMP"
echo GE19_H4F3D15A_ORIGINAL_R1_CONDITIONAL_PHYSICAL_EXECUTION
set +e
python3 -B -m ge19.h4f3d15a_actual_original_R1_clock_conditional \
  --results-dir "$ROOT/results" --repair26-trace "$TRACE" \
  --json-out "$JSON" --npz-out "$NPZ" 2>&1 | tee "$FULL" | tail -n 32
rc="${PIPESTATUS[0]}"
set -e
for file in "$JSON" "$NPZ" "$FULL"; do
  if [[ -s "$file" ]]; then sha256sum "$file"; wc -c "$file"; fi
done
if [[ "$rc" -eq 0 && -s "$JSON" && -s "$NPZ" ]]; then
  echo GE19_H4F3D15A_CLOCK_AND_INTERFACE_CONDITIONAL_COLLOCATION_PASS_CONTINUOUS_X10_AND_GE05_ONSHELL_OPEN
else
  echo GE19_H4F3D15A_IMPLEMENTATION_OR_ORIGINAL_PARENT_FAIL
fi
exit "$rc"
