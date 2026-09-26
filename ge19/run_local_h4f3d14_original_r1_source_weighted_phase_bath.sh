#!/usr/bin/env bash
# D14: original GE05 R1 source-weighted signed/unsigned high-phase diagnostic ONLY.
# Reuse frozen original D13 actual bath parent, original Repair26 R1 history and
# all original GE05 action/phase/mode conventions. No on-shell/full Ward claim.
set -euo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
[[ "$(git symbolic-ref --quiet --short HEAD)" == "physics-first-gravitational-elasticity" ]] || {
 echo GE19_H4F3D14_WRONG_BRANCH; exit 4;
}
PINS=(
 "ge19/h4f3d14_predata_original_r1_phase_weighted_signed_bath_error.json:321217d3661bf09fe67f1359606a5296faa4d304"
 "ge19/h4f3d14_original_r1_source_weighted_phase_bath_partition.py:727a8abb63a4aaa314d09e3396d7e2fbeb03bd71"
 "ge19/h4f3d14_actual_original_r1_source_weighted_phase_bath.py:cb823960e9b2cf1b82b1accd458ec75f4acf4547"
 "ge19/h4f3d13_predata_original_r1_interval_signed_bath_parent.json:ec07d6be5c267dcbbdb05395ea81cc5e7405781e"
 "ge19/h4f3d13_original_r1_interval_signed_bath_assembly.py:64641d11c34a729508dbfa29d2fe65ccae3a031a"
 "ge19/h4f3d13_actual_original_r1_signed_interval_bath_parent.py:5cce06a82869d5b7ff70c12a92e70b9257073c42"
 "ge19/h4f3d13_actual_original_r1_signed_interval_bath_independent_archive_audit.json:886ac54bd7ad6f802895145fd7776f2ebd6c64d1"
 "ge05/memory_directional_source_generator.py:40837d77f89028da30c28899e2d0530a4401844e"
 "ge19/h4f3d6_actual_normalized_bath_parent_ward.py:0419145499f5f44e06ba0c96f779c2a604e84ce7"
)
for entry in "${PINS[@]}"; do
  rel="${entry%%:*}"; want="${entry#*:}"
  [[ "$(git rev-parse "HEAD:$rel")" == "$want" ]] || { echo "GE19_H4F3D14_GIT_BLOB_MISMATCH $rel"; exit 4; }
  [[ "$(git hash-object "$ROOT/$rel")" == "$want" ]] || { echo "GE19_H4F3D14_WORKTREE_BLOB_MISMATCH $rel"; exit 4; }
done
git diff --quiet -- ge19/run_local_h4f3d14_original_r1_source_weighted_phase_bath.sh
git diff --cached --quiet -- ge19/run_local_h4f3d14_original_r1_source_weighted_phase_bath.sh
echo GE19_H4F3D14_ORIGINAL_SOURCE_AND_PREDATA_LOCK_PASS
if [[ -z "${VIRTUAL_ENV:-}" ]]; then
 [[ -f "$ROOT/.venv/bin/activate" ]] || { echo GE19_H4F3D14_VENV_MISSING; exit 5; }
 source "$ROOT/.venv/bin/activate"
fi
export PYTHONPATH="$ROOT"
export PYTHONDONTWRITEBYTECODE=1
TRACE="${GE19_REPAIR26_R1_TRACE:-}"
if [[ -z "$TRACE" && -s "$ROOT/results/ge19_repair26_R1_full_history_trace.dat" ]]; then
 TRACE="$ROOT/results/ge19_repair26_R1_full_history_trace.dat"
fi
if [[ -z "$TRACE" && -d "$ROOT/frozen_repair26_repair27" ]]; then
 mapfile -d '' -t found < <(find "$ROOT/frozen_repair26_repair27" -type f -name ge19_repair26_R1_full_history_trace.dat -print0)
 if [[ "${#found[@]}" -eq 1 ]]; then TRACE="${found[0]}"; fi
fi
[[ -n "$TRACE" && -s "$TRACE" ]] || { echo GE19_H4F3D14_MISSING_OR_AMBIGUOUS_ORIGINAL_R1_TRACE; exit 6; }
TRACE="$(realpath "$TRACE")"
check() {
 local file="$1" want="$2" got
 [[ -s "$file" ]] || { echo "GE19_H4F3D14_MISSING $file"; exit 6; }
 got="$(sha256sum "$file" | awk '{print $1}')"
 [[ "$got" == "$want" ]] || { echo "GE19_H4F3D14_SHA_MISMATCH $file $got"; exit 6; }
}
check "$TRACE" 608ee0b4c868a701db6976f756b9a551cd9ddffe1e8e4ab37c5cd2361405a6f8
[[ "$(wc -c < "$TRACE" | tr -d ' ')" == "26643162" ]] || exit 6
check "$ROOT/results/ge19_h4f3d13_actual_original_r1_signed_interval_bath_parent.json" 2b4dfbd30ec6466292e0dcf62eeed8b723555d1890a127a5e0a6ff761d2ebe76
check "$ROOT/results/ge19_h4f3d13_actual_original_r1_signed_interval_bath_parent.npz" 1608fe98dd924b2b235ecf0f8fce768f2f3a2fa4a2854de04a56fe622ad3df89
echo GE19_H4F3D14_ORIGINAL_R1_AND_D13_ACTUAL_PHYSICAL_PARENT_SHA_PASS
JSON="$ROOT/results/ge19_h4f3d14_actual_original_r1_source_weighted_phase_bath.json"
NPZ="$ROOT/results/ge19_h4f3d14_actual_original_r1_source_weighted_phase_bath.npz"
FULL="$ROOT/results/ge19_h4f3d14_actual_original_r1_source_weighted_phase_bath_FULL.log"
for out in "$JSON" "$NPZ" "$FULL"; do
 [[ ! -e "$out" ]] || { echo "GE19_H4F3D14_NO_OVERWRITE $out"; exit 7; }
done
TMP="$(mktemp -d)"
trap 'rm -rf -- "$TMP"' EXIT
mkdir -p "$TMP/results"
cd "$TMP"
python3 -B -c 'import numpy,scipy,sympy'
echo GE19_H4F3D14_ORIGINAL_R1_ISOLATED_LOCAL_PHYSICAL_EXECUTION
set +e
python3 -B -m ge19.h4f3d14_actual_original_r1_source_weighted_phase_bath \
 --results-dir "$ROOT/results" --repair26-trace "$TRACE" \
 --json-out "$JSON" --npz-out "$NPZ" 2>&1 | tee "$FULL" | tail -n 32
rc="${PIPESTATUS[0]}"
set -e
for file in "$JSON" "$NPZ" "$FULL"; do
 if [[ -s "$file" ]]; then sha256sum "$file"; wc -c "$file"; fi
done
if [[ "$rc" -eq 0 && -s "$JSON" && -s "$NPZ" ]]; then
 echo GE19_H4F3D14_SOURCE_WEIGHTED_PHASE_BATH_DIAGNOSTIC_PASS_ONSHELL_OPEN
else
 echo GE19_H4F3D14_IMPLEMENTATION_OR_PARENT_IDENTITY_FAIL
fi
exit "$rc"
