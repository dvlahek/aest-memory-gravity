#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results

test "$(git rev-parse HEAD:ge19/repair32c_predata_artifact_only_reduced_z11_certification.json)" = "08160cf56534468aa95f5bad08a7d476d8d6e276"
test "$(git rev-parse HEAD:ge19/repair32c_artifact_only_reduced_z11_certification.py)" = "b2e89fe8e3dc66a430ee47e4d0ba085b82e9ad57"
test "$(git rev-parse HEAD:.github/workflows/ge19-repair32c-repair01-prelock-audit.yml)" = "59b44fa84d265836ed77d8db31be0a713aae4869"
test "$(git rev-parse HEAD:docs/ge19_repair32c_initial_execution_import_fail_freeze.md)" = "f57129227ad6a06604a195238c10eaeb8119f3aa"
test "$(git rev-parse HEAD:docs/ge19_repair32c_repair01_import_path_lock.md)" = "a557188a16713f16b34bbc7f9cdd4a7501e9ffef"
test "$(git rev-parse HEAD:docs/ge19_repair32b_factor2_corrected_h2_reconstruction_result_freeze.md)" = "9a5bda89c15ca276d102ca58236ce0a7275c7601"

for c in \
  919a0fc095bebdc8747394a39c6ca1c6ae894489 \
  752e3ff755a0bc768d15bfb9f8de05957262a6b7 \
  743c9eb6505ca3f318257c22601e80b35ed0a028 \
  5f7cc60c0ff45badadd2b01d7d549512040f3b5d \
  87036cc935ba18b109fc02130ac1b59e450094f7 \
  6099ec3c0158231947ef30e0a63450ac115b1174; do
  git merge-base --is-ancestor "$c" HEAD
done
echo GE19_REPAIR32C_LOCK_PASS

if [[ -z "${VIRTUAL_ENV:-}" ]]; then
  echo GE19_REPAIR32C_VENV_NOT_ACTIVE
  echo "Run: source .venv/bin/activate"
  exit 5
fi

python3 -m py_compile ge19/repair32c_artifact_only_reduced_z11_certification.py

R32B_JSON="results/ge19_repair32b_factor2_corrected_reduced_h2_z11_reconstruction.json"
R32B_NPZ="results/ge19_repair32b_factor2_corrected_reduced_h2_z11_reconstruction.npz"

test -f "$R32B_JSON"
test -f "$R32B_NPZ"
test "$(sha256sum "$R32B_JSON" | awk '{print $1}')" = "226dd2a2a0e86ddccc39a62d833960bdf9d5a9af038ad3bf225bbbf69d0b95cf"
test "$(wc -c < "$R32B_JSON" | tr -d ' ')" = "68434"
test "$(sha256sum "$R32B_NPZ" | awk '{print $1}')" = "5d4a0a72c08d09d096a8de0b428b3c8443fc33e8ad442ed6d997d6bf2bc6e327"
test "$(wc -c < "$R32B_NPZ" | tr -d ' ')" = "1082578"
echo GE19_REPAIR32C_REPAIR32B_PARENT_PASS

# Artifact-only operator context: unchanged frozen GE15 and Repair13 parents.
test -f results/ge15_R1_dense_accepted_step_trace.dat
test -f results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz
test "$(sha256sum results/ge15_R1_dense_accepted_step_trace.dat | awk '{print $1}')" = "7f57ab676f2a31cf0abf93ff0f8b0f1f2f80bb9a58d7cf1e47e10a158c57c69f"
test "$(sha256sum results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz | awk '{print $1}')" = "011c0ae54fd21d70c0e2c695ce62e7b74a3c5529a07c9023c882a447d5b40ca3"
echo GE19_REPAIR32C_OPERATOR_CONTEXT_PASS

OUT="results/ge19_repair32c_artifact_only_reduced_z11_certification.json"
FULL="results/ge19_repair32c_artifact_only_reduced_z11_certification_FULL.log"
rm -f "$OUT" "$FULL"

set +e
python3 ge19/repair32c_artifact_only_reduced_z11_certification.py \
  --results-dir results \
  --repair32b-json "$R32B_JSON" \
  --repair32b-npz "$R32B_NPZ" \
  --json-out "$OUT" \
  2>&1 | tee "$FULL"
rc=${PIPESTATUS[0]}
set -e

if [[ -s "$OUT" ]]; then
  python3 - <<'PY'
import json
d=json.load(open("results/ge19_repair32c_artifact_only_reduced_z11_certification.json"))
print("CLASSIFICATION =",d["classification"])
print("Z11_CERTIFIED =",d["Z11_certified"])
print("H4_Z21_LICENSED =",d["routing"]["H4_Z21_licensed"])
print("ROUTE =",d["routing"]["next_route"])
x=d["diagnostics"]
print("STATE_GLOBAL =",x["state_precision"]["full_six_field_global_relative_L2_max"])
print("STATE_DYNAMIC =",x["state_precision"]["dynamic_global_relative_L2_max"])
print("CHI_PARENT =",x["chi_parent"]["relative_L2_max"])
print("CHI_INITIAL =",x["chi_parent"]["initial_abs_or_rel_max"])
print("DRIVEN_OPERATOR_MAX =",x["driven_rows_global_relative_L2_max"])
print("SOURCE_FREE_OPERATOR_MAX =",x["source_free_rows"]["max_absolute_over_global_main_operator_scale"])
print("SHIFT_GLOBAL =",x["shift_global_relative_to_operator_scale"])
print("ANISO_GLOBAL =",x["anisotropy_global_relative_to_operator_scale"])
print("CHI_C_ENVELOPE =",x["chi11_C_envelope"]["relative_L2_max"])
print("GATES =",d["gates"])
PY
fi

for f in "$OUT" "$FULL"; do
  if [[ -f "$f" ]]; then
    sha256sum "$f"
    wc -c "$f"
  fi
done

if [[ "$rc" -eq 0 ]]; then
  echo GE19_REPAIR32C_EXECUTION_COMPLETE
elif [[ "$rc" -eq 2 && -s "$OUT" ]]; then
  echo GE19_REPAIR32C_VALID_SCIENCE_FAIL_FREEZE_REQUIRED
else
  echo GE19_REPAIR32C_IMPLEMENTATION_OR_EXECUTION_FAILURE
fi
exit "$rc"
