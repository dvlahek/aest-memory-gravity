#!/usr/bin/env bash
# GE19 H3F: separately versioned corrected-Y Z20 science reclosure.
# Do NOT edit or overwrite frozen Repair22/27/37--44 results.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results

test "$(git rev-parse HEAD:ge19/h3f_predata_action_completed_y_z20_parent_reclosure.json)" = "6ae1dd8c27ee1f94d85831cd5ae7b5ec21e3794e"
test "$(git rev-parse HEAD:ge19/h3f_corrected_y_source_adapter.py)" = "395294868191111b9b01201315cd2e6a30e47578"
test "$(git rev-parse HEAD:ge19/h3f_corrected_y_parent_core.py)" = "7e1da10ae8d79b6269b306f5483783de0fd3fd30"
test "$(git rev-parse HEAD:ge19/h3f_corrected_y_z20_science_reclosure.py)" = "31e36aaf16c8d68f0ad1ffaff97459d67a23a8b0"
test "$(git rev-parse HEAD:docs/ge19_h3f_complete_y_source_adapter_valid_freeze.md)" = "01aa03757568a4f42223407a3bf10805d6f012e0"
test "$(git rev-parse HEAD:.github/workflows/ge19-h3f-corrected-y-preexecution.yml)" = "fc32bf577d3d50df21f67324f3bc7590f9dc4aa8"
test "$(git rev-parse HEAD:ge19/h4_stagee_versioned_y_source_rows.py)" = "282166ea5840d7fba4dbc328d40d7687afa6fa0f"
test "$(git rev-parse HEAD:ge19/repair07_window_retarded_reduced_h3_z20_particular.py)" = "e34d28a2062c748f48bc82fa928844b02631de25"
test "$(git rev-parse HEAD:ge19/repair14_self_consistent_reduced_h3_z20_particular.py)" = "06c5ced952c2370cfa4aaadb6ef8f72d2d7221de"
test "$(git rev-parse HEAD:ge19/repair21_on_shell_h1_parent_matched_shift_audit.py)" = "73e7fa0f5b3a58f0462308bf11d2a53b7616abfb"
test "$(git rev-parse HEAD:ge19/repair22_on_shell_parent_z20_certification.py)" = "4860d13c881f41dbacbdc16ff179e917644ea6a5"
echo GE19_H3F_LOCK_PASS

for f in \
  ge19/h3f_predata_action_completed_y_z20_parent_reclosure.json \
  ge19/h3f_corrected_y_source_adapter.py \
  ge19/h3f_corrected_y_parent_core.py \
  ge19/h3f_corrected_y_z20_science_reclosure.py \
  ge19/h4_stagee_versioned_y_source_rows.py \
  ge19/repair07_window_retarded_reduced_h3_z20_particular.py \
  ge19/repair14_self_consistent_reduced_h3_z20_particular.py \
  ge19/repair21_on_shell_h1_parent_matched_shift_audit.py \
  ge19/repair22_on_shell_parent_z20_certification.py
do
  git diff --quiet -- "$f"
  git diff --cached --quiet -- "$f"
done

if [[ -z "${VIRTUAL_ENV:-}" ]]; then
  echo GE19_H3F_VENV_NOT_ACTIVE
  echo "Run: source .venv/bin/activate"
  exit 5
fi

python3 -c 'import numpy, scipy, sympy'
python3 -m py_compile \
  ge19/h3f_corrected_y_source_adapter.py \
  ge19/h3f_corrected_y_parent_core.py \
  ge19/h3f_corrected_y_z20_science_reclosure.py
python3 -m ge19.h3f_corrected_y_z20_science_reclosure --help >/dev/null
echo GE19_H3F_LOCAL_PREEXECUTION_AUDIT_PASS

declare -A HASHES
HASHES["results/ge15_R1_dense_accepted_step_trace.dat"]="7f57ab676f2a31cf0abf93ff0f8b0f1f2f80bb9a58d7cf1e47e10a158c57c69f"
HASHES["results/ge18_repair01_on_shell_matched_dust_first_order_bridge.npz"]="b6ccaf2257fbb09df701c43bc9a593a3f68238826277a510a0b3b531ea9fa6fe"
HASHES["results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.json"]="ae3cc790ecffbd5498b5852273c72ae578d4615de29bbb616673c05cdb3e74b7"
HASHES["results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz"]="011c0ae54fd21d70c0e2c695ce62e7b74a3c5529a07c9023c882a447d5b40ca3"
HASHES["results/ge19_repair18_zero_coordinate_constraint_projected_momentum_boundary.json"]="d5603138c2f488413686323d1241613f6ef707b586116aa7fe865ae25ceb0edc"
HASHES["results/ge19_repair19_projected_boundary_reduced_h3_z20_propagation.json"]="32837e04a9ea6c83642a0d465f0312cc17a02ddad168760764f3c7b999a0a14d"
HASHES["results/ge19_repair20_shift_near_null_time_resolution_audit.json"]="5f1dc8e48963c6403f142958c8ce34ab1457953b47868d1a65317655cd0644eb"
HASHES["results/ge19_repair20_shift_near_null_time_resolution_audit.npz"]="99937112b889bc556ada756bc7b4e834991a6019596fdbc353a40294ad3968a6"
HASHES["results/ge19_repair21_on_shell_h1_parent_matched_shift_audit.json"]="e27d12f18a992a1c8c3217e67c0efd39dcf7c9d7aadcfbbb3220f7508bca1bb2"
HASHES["results/ge19_repair21_on_shell_h1_parent_matched_shift_audit.npz"]="c6fcde7d39480ec7f03de2acf0f33f648a997404c9cca8f83990ed7b50667f3b"
HASHES["results/ge19_repair22_on_shell_parent_z20_certification.npz"]="3020e0d040f902ab2609e05705f4508d9919665b1344fa0e641644ea8fc41a16"
HASHES["results/ge19_h4_stagee_y_source_rows_LOCAL.json"]="c3ff4cc18dc8c7a69ba661a68ea3de987818f1b9c1db3275b08f2976c385896e"
for f in "${!HASHES[@]}"; do
  if [[ ! -f "$f" ]]; then
    echo "GE19_H3F_MISSING_FROZEN_INPUT: $f"
    exit 6
  fi
  got="$(sha256sum "$f" | awk '{print $1}')"
  if [[ "$got" != "${HASHES[$f]}" ]]; then
    echo "GE19_H3F_FROZEN_HASH_MISMATCH: $f"
    echo "EXPECTED=${HASHES[$f]}"
    echo "OBSERVED=$got"
    exit 7
  fi
done
test -s results/ge15_R1_cli_background.dat
echo GE19_H3F_FROZEN_PARENTS_PASS

JSON="results/ge19_h3f_corrected_y_z20_science_reclosure.json"
NPZ="results/ge19_h3f_corrected_y_z20_science_reclosure.npz"
FULL="results/ge19_h3f_corrected_y_z20_science_reclosure_FULL.log"
rm -f "$JSON" "$NPZ" "$FULL"

set +e
python3 -m ge19.h3f_corrected_y_z20_science_reclosure \
  --results-dir results \
  --json-out "$JSON" \
  --npz-out "$NPZ" \
  2>&1 | tee "$FULL" | tail -n 100
rc=${PIPESTATUS[0]}
set -e

if [[ -s "$JSON" ]]; then
python3 - <<'PY'
import json
p="results/ge19_h3f_corrected_y_z20_science_reclosure.json"
d=json.load(open(p))
print("CLASSIFICATION =",d["classification"])
print("Z20_CERTIFIED =",d["Z20_certified"])
print("LEGACY_Y_CONTROL =",d["legacy_Y_control"])
print("H1_ON_SHELL =",d["H1_on_shell_controls"])
print("SOURCE_SPATIAL =",d["source_spatial_convergence"]["relative_L2_m1_40_max"])
print("BOUNDARY =",{k:v for k,v in d["boundary_certification"].items() if k!="per_case"})
print("MATCHED_SHIFT =",{k:v for k,v in d["shift_certification"].items() if k not in ("near_null_definition",)})
print("H3_CONTROLS =",d["H3_controls"])
print("GATES =",d["gates"])
print("FAILED_GATES =",[k for k,v in d["gates"].items() if not v])
print("NEW_Q20_LICENSED =",d["project_boundary"]["new_corrected_q20_construction_licensed_after_freeze"])
print("Z21_LICENSED =",d["project_boundary"]["Z21_licensed"])
PY
fi

for f in "$JSON" "$NPZ" "$FULL"; do
  if [[ -s "$f" ]]; then
    sha256sum "$f"
    wc -c "$f"
  fi
done

if [[ "$rc" -eq 0 && -s "$JSON" && -s "$NPZ" ]]; then
  echo GE19_H3F_NEW_Z20_SCIENCE_PASS
elif [[ "$rc" -eq 2 && -s "$JSON" && -s "$NPZ" ]]; then
  echo GE19_H3F_NEW_Z20_SCIENCE_FAIL
else
  echo GE19_H3F_IMPLEMENTATION_OR_EXECUTION_FAIL
fi
exit "$rc"
