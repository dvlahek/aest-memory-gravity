#!/usr/bin/env bash
# Reproduce the frozen exact H4 Stage D GR-anchored Y action audit locally.
# No H3/H4/Z21 numerical solver and no historical source patch.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results

test "$(git rev-parse HEAD:ge19/h4_structural_stage_d_predata_global_y_normalization.json)" = "764d064c76d44bc597ab6c4f96044ba2a90433a5"
test "$(git rev-parse HEAD:ge19/h4_structural_stage_d_common_action_y_rows.py)" = "162357ce845a93982b46aef7d839a7171964b47e"
test "$(git rev-parse HEAD:docs/ge19_h4_staged_common_y_action_rows_valid_freeze.md)" = "7d140a608d91a39106c34565cd50e4aa729ec30b"
test "$(git rev-parse HEAD:.github/workflows/ge19-h4-staged-common-y-action.yml)" = "648e9276e0b3aba74a3a3a360e5b1271d3eebc44"
echo GE19_H4_STAGED_LOCAL_LOCK_PASS

for f in \
  ge19/h4_structural_stage_d_predata_global_y_normalization.json \
  ge19/h4_structural_stage_d_common_action_y_rows.py \
  docs/ge19_h4_stagec_local_analytic_reproduction_freeze.md \
  docs/ge19_h4_stagec_y_raw_ge19_conventions_valid_freeze.md \
  docs/nl0c_y_sector_weakly_nonlinear_result.md \
  nl1c6/spherical_self_gravity_g1_g10.py \
  ge06/analytic_aest_directional_source_generator.py \
  docs/ge06_analytic_aest_directional_source_generator_implementation_lock.md
do
  git diff --quiet -- "$f"
  git diff --cached --quiet -- "$f"
done

if [[ -z "${VIRTUAL_ENV:-}" ]]; then
  echo GE19_H4_STAGED_VENV_NOT_ACTIVE
  echo "Run: source .venv/bin/activate"
  exit 5
fi

python3 -c 'import sympy'
python3 -m py_compile ge19/h4_structural_stage_d_common_action_y_rows.py
echo GE19_H4_STAGED_LOCAL_PREEXECUTION_PASS

JSON="results/ge19_h4_staged_common_y_action_rows_LOCAL.json"
FULL="results/ge19_h4_staged_common_y_action_rows_LOCAL_FULL.log"
rm -f "$JSON" "$FULL"

set +e
python3 ge19/h4_structural_stage_d_common_action_y_rows.py \
  --json-out "$JSON" 2>&1 | tee "$FULL"
rc=${PIPESTATUS[0]}
set -e

if [[ "$rc" -ne 0 || ! -s "$JSON" ]]; then
  echo GE19_H4_STAGED_LOCAL_ANALYTIC_FAIL
  if [[ "$rc" -ne 0 ]]; then exit "$rc"; fi
  exit 3
fi

python3 - <<'PY'
import json
d=json.load(open("results/ge19_h4_staged_common_y_action_rows_LOCAL.json"))
assert d["classification"]=="GE19_H4_STAGED_COMMON_GR_NORMALIZATION_AND_Y_ROWS_DERIVED"
assert d["all_analytic_gates_pass"] is True
assert all(v["exact"] for v in d["frozen_blob_controls"].values())
assert all(d["common_action_normalization"]["checks"].values())
assert all(d["complete_Y_sector_raw_source_rows"]["checks"].values())
assert d["common_action_normalization"]["relative_Y_sector_action_prefactor_in_GE06_raw_units"]=="1"
assert d["full_H4_Noether_identity_derived"] is False
assert d["numerical_H3_H4_Z21_solve_performed"] is False
assert d["historical_results_relabelled"] is False
assert d["window_local_particular_Z21_certified"] is False
assert d["lensing_licensed"] is False
print("CLASSIFICATION =",d["classification"])
print("RELATIVE_Y_ACTION_FACTOR =",d["common_action_normalization"]["relative_Y_sector_action_prefactor_in_GE06_raw_units"])
print("COMPLETE_Y_SOURCE_ROWS =",d["complete_Y_sector_raw_source_rows"])
print("FULL_H4_NOETHER_DERIVED =",d["full_H4_Noether_identity_derived"])
print("Z21_CERTIFIED =",d["window_local_particular_Z21_certified"])
print("GE19_H4_STAGED_LOCAL_ANALYTIC_PASS")
PY

sha256sum "$JSON" "$FULL"
wc -c "$JSON" "$FULL"
