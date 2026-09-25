#!/usr/bin/env bash
# GE19 H4F3d10r1 lossless-Nyquist implementation repair of original PHYSICAL archive.
# Known first-order parent and L/shift boundary only. No all-sector H4 Ward.
set -euo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
[[ "$(git symbolic-ref --quiet --short HEAD)" == "physics-first-gravitational-elasticity" ]] || {
  echo GE19_H4F3D10R1_WRONG_BRANCH; exit 4;
}
PINS=(
 "ge19/h4f3d10_predata_actual_nonbath_first_order_known_boundary.json:7aafe872f32057ab46ed99650b3df1803050077e"
 "ge19/h4f3d10_actual_nonbath_first_order_known_boundary.py:c570546caa301ec6899b4e669b663726fd4fdc2f"
 "ge19/h4f3d10_nonbath_first_order_local_partials.py:4c3968d7186e27f15b10992198d7bccedf207bfb"
 "ge19/h4f3d10_known_parent_boundary_assembly.py:d3a43a0ebbd78e03f2313592bdb1455977cb1d1c"
 "ge19/h4f3d10_physical_main.py:1eec8381ba107a02ba3dc41bfd18fcc7e12d224e"
 "ge19/run_local_h4f3d10_actual_nonbath_first_order_known_boundary.sh:4c873192001a1fd8f3652a9e47ec13c11d999199"
 "ge19/h4f3d10_original_physical_archive_projection_failure_independent_audit.json:b4bce81d944201e663717e5f2d0dace546abd535"
 "ge19/h4f3d10r1_predata_lossless_fourier_archive_repair.json:418859847f108b31cf66ac71c998cc604ca35c31"
 "ge19/h4f3d10r1_lossless_known_parent_boundary_assembly.py:d4f67adc2c9267cd3e4fd0e6dd1358c2c97a8545"
 "ge19/h4f3d10r1_lossless_fourier_physical_main.py:659ba72aafedc6f62d519f5fe09e47736074e90a"
 "ge19/h4f3d8_independent_nonbath_euler_and_boundary.py:861cd5a81c17380a727777a4e1ff08cd7e857522"
 "ge19/h4f3b_actual_corrected_six_piece_source.py:0423cbc64f6cda3b2a9aeb67c734935ef3ae7f9c"
 "ge19/h4f3d6_actual_normalized_bath_parent_ward.py:0419145499f5f44e06ba0c96f779c2a604e84ce7"
 "ge19/h4f3d7r1_physical_output_finite_check_repair.py:e4cb9d6638b427368647a29b86ccf5445b43d7a2"
 "ge19/repair37_cancellation_safe_fd8_h4_z21_reclosure.py:45d203a092f9ac71cc612b15df5f0c0c630f5898"
 "ge19/repair07_window_retarded_reduced_h3_z20_particular.py:e34d28a2062c748f48bc82fa928844b02631de25"
 "ge19/repair11_lambda_inclusive_reduced_h1_reclosure.py:dbfa43ae11dbd3cfeeb1994a30237e9374dbb3e7"
 "ge19/repair13_self_consistent_reduced_background_h1_reclosure.py:362d63d03d7b850fceae393f535353ded79aeea7"
 "ge19/repair14_self_consistent_reduced_h3_z20_particular.py:06c5ced952c2370cfa4aaadb6ef8f72d2d7221de"
 "ge19/repair24_q20_construction.py:fc271987d1bddcd023cc9c057ddcad036b1d72fb"
 "ge06/analytic_aest_directional_source_generator.py:a7afe0035054a9dca55d74a6497c081422114b4c"
 "ge07/pressureless_matter_directional_source_generator.py:cde8da77a80799cef00fc7c09c3633310fc9e3d4"
)
for entry in "${PINS[@]}"; do
  rel="${entry%%:*}"; want="${entry#*:}"
  [[ "$(git rev-parse "HEAD:$rel")" == "$want" ]] || { echo "GE19_H4F3D10R1_BLOB_MISMATCH $rel"; exit 4; }
  git diff --quiet -- "$rel" || { echo "GE19_H4F3D10R1_DIRTY $rel"; exit 4; }
  git diff --cached --quiet -- "$rel" || { echo "GE19_H4F3D10R1_STAGED $rel"; exit 4; }
done
git diff --quiet -- ge19/run_local_h4f3d10r1_lossless_fourier_archive_repair.sh
git diff --cached --quiet -- ge19/run_local_h4f3d10r1_lossless_fourier_archive_repair.sh
echo GE19_H4F3D10R1_ORIGINAL_CODE_LOCK_PASS

if [[ -z "${VIRTUAL_ENV:-}" ]]; then
  [[ -f "$ROOT/.venv/bin/activate" ]] || { echo GE19_H4F3D10R1_VENV_MISSING; exit 5; }
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
[[ -n "$TRACE" && -s "$TRACE" ]] || { echo GE19_H4F3D10R1_MISSING_OR_AMBIGUOUS_R1_TRACE; exit 6; }
TRACE="$(realpath "$TRACE")"
check() {
 local path="$1" want="$2" got
 [[ -s "$path" ]] || { echo "GE19_H4F3D10R1_MISSING $path"; exit 6; }
 got="$(sha256sum "$path" | awk '{print $1}')"
 [[ "$got" == "$want" ]] || { echo "GE19_H4F3D10R1_SHA_MISMATCH $path $got"; exit 6; }
}
check "$TRACE" 608ee0b4c868a701db6976f756b9a551cd9ddffe1e8e4ab37c5cd2361405a6f8
[[ "$(wc -c < "$TRACE" | tr -d ' ')" == "26643162" ]] || exit 6
check "$ROOT/results/ge19_h4f3b_actual_corrected_six_piece_source.json" 1ec88fd3fd6b81bf30614b0cb78d722a02dd4f745e1f22cb9b8f956a44bac6c1
check "$ROOT/results/ge19_h4f3b_actual_corrected_six_piece_source.npz" 787d5d177838b05078057aa932f379dd529449ce203f5664c36cf723acb0116b
check "$ROOT/results/ge19_h4f3d6_actual_normalized_bath_parent_ward.json" 4607edde17c6820c85f32c0bbd774d5a58148eb01bfd0c81ce592e8c1b907791
check "$ROOT/results/ge19_h4f3d6_actual_normalized_bath_parent_ward.npz" 17b50c6ee584b2a8886f7114a90ea9396a127172dd9e02976b0e6275fe2fedc0
check "$ROOT/results/ge19_h4f3d7r1_physical_r1_fd4_vs_interval_ode.json" 031229d570d29ae9c4ea0ab8e25222d94e9cda4520c991cd203e9d7b97e01dc9
check "$ROOT/results/ge19_h4f3d7r1_physical_r1_fd4_vs_interval_ode.npz" 4f011c96c2c11165df6332eafc459c5d2c5e7bc5164a436bde3d1563696f0e13
check "$ROOT/results/ge19_h4f3d10_actual_nonbath_first_order_known_boundary.json" df4240b40aa7f3b787e36dd0fd87212c6dcb746b35278f6cb36fc1083aa4ea21
check "$ROOT/results/ge19_h4f3d10_actual_nonbath_first_order_known_boundary.npz" 1b9ff8e421f2b9241cd0ffbc65967ecc4f5efc8afc43d5747ae1216f5d944fab
check "$ROOT/results/ge19_h4f3d10_actual_nonbath_first_order_known_boundary_FULL.log" df4240b40aa7f3b787e36dd0fd87212c6dcb746b35278f6cb36fc1083aa4ea21
echo GE19_H4F3D10R1_ORIGINAL_PHYSICAL_INPUT_SHA_PASS

JSON="$ROOT/results/ge19_h4f3d10r1_lossless_fourier_known_boundary.json"
NPZ="$ROOT/results/ge19_h4f3d10r1_lossless_fourier_known_boundary.npz"
FULL="$ROOT/results/ge19_h4f3d10r1_lossless_fourier_known_boundary_FULL.log"
for dest in "$JSON" "$NPZ" "$FULL"; do
  [[ ! -e "$dest" ]] || { echo "GE19_H4F3D10R1_NO_OVERWRITE $dest"; exit 7; }
done
TMP="$(mktemp -d)"
trap 'rm -rf -- "$TMP"' EXIT
mkdir -p "$TMP/results"
cd "$TMP"
python3 -B -c 'import numpy,scipy,sympy'
echo GE19_H4F3D10R1_ISOLATED_LOCAL_EXECUTION
set +e
python3 -B -m ge19.h4f3d10r1_lossless_fourier_physical_main --results-dir "$ROOT/results" --repair26-trace "$TRACE" --json-out "$JSON" --npz-out "$NPZ" 2>&1 | tee "$FULL" | tail -n 28
rc="${PIPESTATUS[0]}"
set -e
for file in "$JSON" "$NPZ" "$FULL"; do
  if [[ -s "$file" ]]; then sha256sum "$file"; wc -c "$file"; fi
done
if [[ "$rc" -eq 0 && -s "$JSON" && -s "$NPZ" ]]; then
  echo GE19_H4F3D10R1_LOSSLESS_ARCHIVE_KNOWN_NONBATH_DIAGNOSTIC_PASS_FULL_OPEN
else
  echo GE19_H4F3D10R1_PHYSICAL_IMPLEMENTATION_OR_ARCHIVE_DIAGNOSTIC_FAIL
fi
exit "$rc"
