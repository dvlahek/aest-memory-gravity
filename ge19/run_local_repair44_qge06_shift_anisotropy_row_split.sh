#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results

test "$(git rev-parse HEAD:ge19/repair44_predata_qge06_shift_anisotropy_row_split.json)" = "85b20ae36482cc343ce756c00970250ea51f1624"
test "$(git rev-parse HEAD:ge19/repair44_qge06_shift_anisotropy_row_split.py)" = "3c734e55a8ac72874e78bd48b8fdd14112cd321f"
test "$(git rev-parse HEAD:.github/workflows/ge19-repair44-prelock-audit.yml)" = "343354af896c612baf957bfd598b0efaa1150164"
test "$(git rev-parse HEAD:docs/ge19_repair43_valid_ge06_constraint_family_freeze.md)" = "2d3daec4c6f52d9d53071ee04fd8834825c2ce10"
test "$(git rev-parse HEAD:docs/ge19_repair44_qge06_row_split_implementation_lock.md)" = "928c24954ab86a8029701aea69ba9c44d7121282"

for c in \
  91446ddb1987e834200204cb6d8c4f8c4008a5be \
  3fa98dd405199cbb125c0fcc0f1c00f87b382430 \
  589859ac041c54e5702bf391e8623002d944a663 \
  78fe09def03d16b2fa65d3bfc667a3b1b35aa463 \
  51cc1c14fc4aed7073e95f8a3b506580b55ca51a
do
  git merge-base --is-ancestor "$c" HEAD
done
echo GE19_REPAIR44_LOCK_PASS

if [[ -z "${VIRTUAL_ENV:-}" ]]; then
  echo GE19_REPAIR44_VENV_NOT_ACTIVE
  echo "Run: source .venv/bin/activate"
  exit 5
fi

python3 -m py_compile ge19/repair44_qge06_shift_anisotropy_row_split.py
python3 ge19/repair44_qge06_shift_anisotropy_row_split.py --help >/tmp/r44_help.txt
grep -q -- "--results-dir" /tmp/r44_help.txt
grep -q -- "--json-out" /tmp/r44_help.txt
grep -q -- "--npz-out" /tmp/r44_help.txt
echo GE19_REPAIR44_LOCAL_PREEXECUTION_AUDIT_PASS

declare -A HASHES
HASHES["results/ge19_repair43_qge06_main_constraint_stage_split.json"]="559ae65ffc5d21433799e4e33aa6d91237a9aa41b9799463971bc45dabecae44"
HASHES["results/ge19_repair43_qge06_main_constraint_stage_split.npz"]="d5c8c02c7f8272dc390ce9e4d2374a35b2ce1b14da5b60e69dc8366499bfe71c"
HASHES["results/ge19_repair42_direct_target_h4_propagation_diagnostic.json"]="4a211581a77c1ad00e14cc398ca7a19b12642f3f3e35b416314d6721f5f81e25"
HASHES["results/ge19_repair42_direct_target_h4_propagation_diagnostic.npz"]="a60515f3d92bbd388fd2fadae6cf2dd07f3ee68e8690b07632bbe5091e9013c5"
HASHES["results/ge19_repair41_direct_fine_grid_target_source_reconstruction.json"]="1b18fede26b021e077ffe5c8b6b7ff0dc727b4defaab48e63491c86d868d1320"
HASHES["results/ge19_repair41_direct_fine_grid_target_source_reconstruction.npz"]="6bfb87ea21d55e2a1d2b16aee9bc8d7246111f91a064a78b74d2ed946ec2ba45"
HASHES["results/ge19_repair37_cancellation_safe_fd8_h4_z21_reclosure.json"]="da8f2f00c22c866ec3f82381d23f69bf036e630fe2a29c5c44657984b760f61a"
HASHES["results/ge19_repair37_cancellation_safe_fd8_h4_z21_reclosure.npz"]="572d8937c1d742b10da66e34cc076377c1b2feb20b8f72eb25c3eaf31a59829f"
HASHES["results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz"]="011c0ae54fd21d70c0e2c695ce62e7b74a3c5529a07c9023c882a447d5b40ca3"
HASHES["results/ge15_R1_dense_accepted_step_trace.dat"]="7f57ab676f2a31cf0abf93ff0f8b0f1f2f80bb9a58d7cf1e47e10a158c57c69f"

for f in "${!HASHES[@]}"; do
  if [[ ! -f "$f" ]]; then
    echo "GE19_REPAIR44_MISSING_LOCAL_INPUT: $f"
    exit 6
  fi
  got="$(sha256sum "$f" | awk '{print $1}')"
  test "$got" = "${HASHES[$f]}"
done
test -s results/ge15_R1_cli_background.dat
echo GE19_REPAIR44_FROZEN_INPUTS_PASS

JSON="results/ge19_repair44_qge06_shift_anisotropy_row_split.json"
NPZ="results/ge19_repair44_qge06_shift_anisotropy_row_split.npz"
FULL="results/ge19_repair44_qge06_shift_anisotropy_row_split_FULL.log"
rm -f "$JSON" "$NPZ" "$FULL"

set +e
python3 ge19/repair44_qge06_shift_anisotropy_row_split.py \
  --results-dir results \
  --json-out "$JSON" \
  --npz-out "$NPZ" \
  2>&1 | tee "$FULL"
rc=${PIPESTATUS[0]}
set -e

if [[ -s "$JSON" ]]; then
python3 - <<'PY'
import json
d=json.load(open("results/ge19_repair44_qge06_shift_anisotropy_row_split.json"))
print("CLASSIFICATION =",d["classification"])
print("ROUTE =",d["routing"]["next_route"])
print("SOURCE_BINDING =",d["stage_and_source_binding"])
print("REPAIR43_REPRO =",d["Repair43_reproduction"])
print("SHIFT_ROW0_Z21_EXACT =",d["shift_row0_only_Z21_exact_baseline"])
print("SHIFT_ROW0_Z21_MAX_ABS =",d["shift_row0_only_Z21_max_absolute_difference"])
print("VARIANTS:")
for k,v in d["variant_results"].items():
    print(" ",k,"=",v)
print("ROW_LEVEL_ATTRIBUTION =",d["row_level_active_field_attribution"])
print("REGISTERED_HOTSPOT =",d["registered_hotspot"])
print("IMPLEMENTATION_GATES =",d["implementation_gates"])
print("Z21_CERTIFIED =",d["Z21_window_local_particular_certified"])
print("SCIENCE_RECLOSURE =",d["science_H4_Z21_reclosure_performed"])
print("LENSING_LICENSED =",d["lensing_licensed"])
PY
fi

for f in "$JSON" "$NPZ" "$FULL"; do
  if [[ -f "$f" ]]; then
    sha256sum "$f"
    wc -c "$f"
  fi
done

if [[ "$rc" -eq 0 && -s "$JSON" ]]; then
  echo GE19_REPAIR44_DIAGNOSTIC_COMPLETE
elif [[ "$rc" -eq 3 && -s "$JSON" ]]; then
  echo GE19_REPAIR44_IMPLEMENTATION_REPRODUCTION_FAIL
else
  echo GE19_REPAIR44_IMPLEMENTATION_OR_EXECUTION_FAILURE
fi
exit "$rc"
