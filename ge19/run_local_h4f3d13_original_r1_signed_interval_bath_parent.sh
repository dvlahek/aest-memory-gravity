#!/usr/bin/env bash
# GE19 H4F3d13 actual original R1 interval-native signed GE05 bath diagnostic.
# Strictly NO bath on-shell, full H4 Ward, F21, Z21 or lensing claim.
set -euo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
[[ "$(git symbolic-ref --quiet --short HEAD)" == "physics-first-gravitational-elasticity" ]] || {
 echo GE19_H4F3D13_WRONG_BRANCH; exit 4;
}
PINS=(
 "ge19/h4f3d13_predata_original_r1_interval_signed_bath_parent.json:ec07d6be5c267dcbbdb05395ea81cc5e7405781e"
 "ge19/h4f3d13_original_r1_interval_signed_bath_assembly.py:64641d11c34a729508dbfa29d2fe65ccae3a031a"
 "ge19/h4f3d13_actual_original_r1_signed_interval_bath_parent.py:5cce06a82869d5b7ff70c12a92e70b9257073c42"
 "ge19/h4f3d6_actual_normalized_bath_parent_ward.py:0419145499f5f44e06ba0c96f779c2a604e84ce7"
 "ge19/h4f3d7_bath_fd4_vs_original_r1_interval_ode.py:b598a5cc49b3d87827b4758c55d3ce7f3a1198a8"
 "ge19/h4f3d7r1_physical_output_finite_check_repair.py:e4cb9d6638b427368647a29b86ccf5445b43d7a2"
 "ge19/h4f3b_actual_corrected_six_piece_source.py:0423cbc64f6cda3b2a9aeb67c734935ef3ae7f9c"
 "ge19/repair24_q20_construction.py:fc271987d1bddcd023cc9c057ddcad036b1d72fb"
 "ge05/memory_directional_source_generator.py:40837d77f89028da30c28899e2d0530a4401844e"
 "ge19/h4f3d12_freeze_manifest.json:b7b8a97ea9e27e6f31a85e7724532bb4dfc4fc4b"
)
for entry in "${PINS[@]}"; do
  rel="${entry%%:*}"; want="${entry#*:}"
  [[ "$(git rev-parse "HEAD:$rel")" == "$want" ]] || { echo "GE19_H4F3D13_BLOB_MISMATCH $rel"; exit 4; }
  [[ "$(git hash-object "$ROOT/$rel")" == "$want" ]] || { echo "GE19_H4F3D13_WORKTREE_MISMATCH $rel"; exit 4; }
done
git diff --quiet -- ge19/run_local_h4f3d13_original_r1_signed_interval_bath_parent.sh
git diff --cached --quiet -- ge19/run_local_h4f3d13_original_r1_signed_interval_bath_parent.sh
echo GE19_H4F3D13_EXACT_ORIGINAL_SOURCE_CODE_LOCK_PASS
if [[ -z "${VIRTUAL_ENV:-}" ]]; then
  [[ -f "$ROOT/.venv/bin/activate" ]] || { echo GE19_H4F3D13_VENV_MISSING; exit 5; }
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
[[ -n "$TRACE" && -s "$TRACE" ]] || { echo GE19_H4F3D13_MISSING_OR_AMBIGUOUS_R1_TRACE; exit 6; }
TRACE="$(realpath "$TRACE")"
check() {
 local file="$1" want="$2" got
 [[ -s "$file" ]] || { echo "GE19_H4F3D13_MISSING $file"; exit 6; }
 got="$(sha256sum "$file" | awk '{print $1}')"
 [[ "$got" == "$want" ]] || { echo "GE19_H4F3D13_PARENT_SHA_MISMATCH $file $got"; exit 6; }
}
check "$TRACE" 608ee0b4c868a701db6976f756b9a551cd9ddffe1e8e4ab37c5cd2361405a6f8
[[ "$(wc -c < "$TRACE" | tr -d ' ')" == "26643162" ]] || exit 6
check "$ROOT/results/ge19_h4f3b_actual_corrected_six_piece_source.json" 1ec88fd3fd6b81bf30614b0cb78d722a02dd4f745e1f22cb9b8f956a44bac6c1
check "$ROOT/results/ge19_h4f3b_actual_corrected_six_piece_source.npz" 787d5d177838b05078057aa932f379dd529449ce203f5664c36cf723acb0116b
check "$ROOT/results/ge19_h4f3d6_actual_normalized_bath_parent_ward.json" 4607edde17c6820c85f32c0bbd774d5a58148eb01bfd0c81ce592e8c1b907791
check "$ROOT/results/ge19_h4f3d6_actual_normalized_bath_parent_ward.npz" 17b50c6ee584b2a8886f7114a90ea9396a127172dd9e02976b0e6275fe2fedc0
check "$ROOT/results/ge19_h4f3d7r1_physical_r1_fd4_vs_interval_ode.json" 031229d570d29ae9c4ea0ab8e25222d94e9cda4520c991cd203e9d7b97e01dc9
check "$ROOT/results/ge19_h4f3d7r1_physical_r1_fd4_vs_interval_ode.npz" 4f011c96c2c11165df6332eafc459c5d2c5e7bc5164a436bde3d1563696f0e13
echo GE19_H4F3D13_ORIGINAL_R1_AND_SIGNED_BATH_PARENT_INPUT_SHA_PASS
JSON="$ROOT/results/ge19_h4f3d13_actual_original_r1_signed_interval_bath_parent.json"
NPZ="$ROOT/results/ge19_h4f3d13_actual_original_r1_signed_interval_bath_parent.npz"
FULL="$ROOT/results/ge19_h4f3d13_actual_original_r1_signed_interval_bath_parent_FULL.log"
for out in "$JSON" "$NPZ" "$FULL"; do
 [[ ! -e "$out" ]] || { echo "GE19_H4F3D13_NO_OVERWRITE $out"; exit 7; }
done
TMP="$(mktemp -d)"
trap 'rm -rf -- "$TMP"' EXIT
mkdir -p "$TMP/results"
cd "$TMP"
python3 -B -c 'import numpy,scipy,sympy'
echo GE19_H4F3D13_ORIGINAL_R1_ISOLATED_LOCAL_PHYSICAL_EXECUTION
set +e
python3 -B -m ge19.h4f3d13_actual_original_r1_signed_interval_bath_parent \
 --results-dir "$ROOT/results" --repair26-trace "$TRACE" \
 --json-out "$JSON" --npz-out "$NPZ" 2>&1 | tee "$FULL" | tail -n 32
rc="${PIPESTATUS[0]}"
set -e
for file in "$JSON" "$NPZ" "$FULL"; do
 if [[ -s "$file" ]]; then sha256sum "$file"; wc -c "$file"; fi
done
if [[ "$rc" -eq 0 && -s "$JSON" && -s "$NPZ" ]]; then
 echo GE19_H4F3D13_ORIGINAL_R1_SIGNED_INTERVAL_BATH_DIAGNOSTIC_PASS_ONSHELL_OPEN
else
 echo GE19_H4F3D13_ORIGINAL_PHYSICAL_OR_PARENT_IDENTITY_FAIL
fi
exit "$rc"
