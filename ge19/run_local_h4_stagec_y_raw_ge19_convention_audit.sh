#!/usr/bin/env bash
# Lightweight local reproduction of the frozen H4 Stage C analytic audit.
# Does not launch any H3/H4/Z21 numerical solver.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results

test "$(git rev-parse HEAD:ge19/h4_structural_stage_c_predata_y_raw_ge19_conventions.json)" = "cc43754e92eef83d025475a9c5f893aa6dd81ce4"
test "$(git rev-parse HEAD:ge19/h4_structural_stage_c_y_raw_ge19_convention_audit.py)" = "80e79006613f6067926adf39995fa08bffe51534"
test "$(git rev-parse HEAD:docs/ge19_h4_stagec_y_raw_ge19_conventions_valid_freeze.md)" = "a22a762148cb30f4d52c494f9df377c4613941d1"
test "$(git rev-parse HEAD:.github/workflows/ge19-h4-stagec-y-source-conventions.yml)" = "c9913803b5851c6e3b3756713178658fa9d20bae"
echo GE19_H4_STAGEC_LOCAL_LOCK_PASS

# Exact tracked source contents must match their committed blobs.
for f in \
  ge19/h4_structural_stage_c_predata_y_raw_ge19_conventions.json \
  ge19/h4_structural_stage_c_y_raw_ge19_convention_audit.py \
  docs/ge19_h4_stageb_y_aether_row_gap_valid_freeze.md \
  ge19/h4_structural_stage_b_y_variational_row_audit.py \
  docs/nl0c_y_sector_weakly_nonlinear_result.md \
  ge06/analytic_aest_directional_source_generator.py \
  ge19/repair07_window_retarded_reduced_h3_z20_particular.py \
  ge19/repair37_cancellation_safe_fd8_h4_z21_reclosure.py
do
  git diff --quiet -- "$f"
  git diff --cached --quiet -- "$f"
done

if [[ -z "${VIRTUAL_ENV:-}" ]]; then
  echo GE19_H4_STAGEC_VENV_NOT_ACTIVE
  echo "Run: source .venv/bin/activate"
  exit 5
fi

python3 -c 'import sympy'
python3 -m py_compile ge19/h4_structural_stage_c_y_raw_ge19_convention_audit.py
echo GE19_H4_STAGEC_LOCAL_PREEXECUTION_PASS

JSON="results/ge19_h4_stagec_y_raw_ge19_convention_audit_LOCAL.json"
FULL="results/ge19_h4_stagec_y_raw_ge19_convention_audit_LOCAL_FULL.log"

set +e
python3 ge19/h4_structural_stage_c_y_raw_ge19_convention_audit.py \
  --json-out "$JSON" 2>&1 | tee "$FULL"
rc=${PIPESTATUS[0]}
set -e

if [[ "$rc" -ne 0 || ! -s "$JSON" ]]; then
  echo GE19_H4_STAGEC_LOCAL_ANALYTIC_FAIL
  exit "$rc"
fi

python3 - <<'PY'
import json
p="results/ge19_h4_stagec_y_raw_ge19_convention_audit_LOCAL.json"
d=json.load(open(p))
expected="GE19_H4_STAGEC_RAW_Y_VOLUME_FACTOR_ESTABLISHED_GLOBAL_NORMALIZATION_OPEN"
assert d["classification"]==expected,d["classification"]
assert d["all_subset_gates_pass"] is True
assert all(v["exact"] for v in d["frozen_blob_controls"].values())
assert all(d["symbolic_action_to_physical_source"]["checks"].values())
assert all(d["frozen_GE19_implementation_conventions"].values())
assert d["symbolic_action_to_physical_source"]["geometric_volume_ratio_raw_EL2_to_code_2Y2"]=="a^3"
assert d["global_action_prefactor_independently_proven"] is False
assert d["complete_Y_source_dictionary_licensed"] is False
assert d["Z21_window_local_particular_certified"] is False
assert d["lensing_licensed"] is False
print("CLASSIFICATION =",d["classification"])
print("RAW_TO_PHYSICAL_GEOMETRIC_RATIO =",d["symbolic_action_to_physical_source"]["geometric_volume_ratio_raw_EL2_to_code_2Y2"])
print("GLOBAL_ACTION_NORMALIZATION_RESOLVED =",d["global_action_prefactor_independently_proven"])
print("COMPLETE_SOURCE_DICTIONARY_LICENSED =",d["complete_Y_source_dictionary_licensed"])
print("Z21_CERTIFIED =",d["Z21_window_local_particular_certified"])
print("GE19_H4_STAGEC_LOCAL_ANALYTIC_PASS")
PY

sha256sum "$JSON" "$FULL"
wc -c "$JSON" "$FULL"
