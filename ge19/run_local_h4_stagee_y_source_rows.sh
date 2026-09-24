#!/usr/bin/env bash
# GE19 H4 Stage E: local deterministic source-only audit, no H3/H4 state solve.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results

test "$(git rev-parse HEAD:ge19/h4_stagee_predata_versioned_y_source_rows.json)" = "e5ff7d12e963fa7487a1dff42ce06053f4b8d82e"
test "$(git rev-parse HEAD:ge19/h4_stagee_versioned_y_source_rows.py)" = "282166ea5840d7fba4dbc328d40d7687afa6fa0f"
test "$(git rev-parse HEAD:ge19/h4_stagee_versioned_y_source_selftest.py)" = "05bbbb5d2dba2193adcbf468efc81eda6fb71ce6"
test "$(git rev-parse HEAD:docs/ge19_h4_stagee_versioned_y_rows_valid_freeze.md)" = "ddec5651400a843994779114d61203e4187cef04"
test "$(git rev-parse HEAD:.github/workflows/ge19-h4-stagee-versioned-y-rows.yml)" = "b3b020cf855b4638f2d5035c7d8ed1f091f999ad"
echo GE19_H4_STAGEE_LOCAL_LOCK_PASS

for f in \
  ge19/h4_stagee_predata_versioned_y_source_rows.json \
  ge19/h4_stagee_versioned_y_source_rows.py \
  ge19/h4_stagee_versioned_y_source_selftest.py \
  docs/ge19_h4_staged_local_analytic_reproduction_freeze.md \
  docs/ge19_h4_staged_common_y_action_rows_valid_freeze.md \
  ge19/h4_structural_stage_d_common_action_y_rows.py \
  ge19/repair07_window_retarded_reduced_h3_z20_particular.py \
  ge19/repair37_cancellation_safe_fd8_h4_z21_reclosure.py
do
  git diff --quiet -- "$f"
  git diff --cached --quiet -- "$f"
done

if [[ -z "${VIRTUAL_ENV:-}" ]]; then
  echo GE19_H4_STAGEE_VENV_NOT_ACTIVE
  echo "Run: source .venv/bin/activate"
  exit 5
fi

python3 -c "import numpy, scipy, sympy"
python3 -m py_compile \
  ge19/h4_stagee_versioned_y_source_rows.py \
  ge19/h4_stagee_versioned_y_source_selftest.py
echo GE19_H4_STAGEE_LOCAL_PREEXECUTION_PASS

JSON="results/ge19_h4_stagee_y_source_rows_LOCAL.json"
FULL="results/ge19_h4_stagee_y_source_rows_LOCAL_FULL.log"
rm -f "$JSON" "$FULL"

set +e
python3 -m ge19.h4_stagee_versioned_y_source_selftest \
  --json-out "$JSON" 2>&1 | tee "$FULL"
rc=${PIPESTATUS[0]}
set -e

if [[ "$rc" -ne 0 || ! -s "$JSON" ]]; then
  echo GE19_H4_STAGEE_LOCAL_IMPLEMENTATION_FAIL
  if [[ "$rc" -ne 0 ]]; then exit "$rc"; fi
  exit 3
fi

python3 - <<'PY'
import json
d=json.load(open("results/ge19_h4_stagee_y_source_rows_LOCAL.json"))
assert d["classification"]=="GE19_H4_STAGEE_Y_SOURCE_ROW_DICTIONARY_IMPLEMENTATION_PASS"
assert d["all_implementation_gates_pass"] is True
assert all(v["exact"] for v in d["frozen_blobs"].values())
assert all(t["pass"] and t["row_and_zero_set_exact"] for t in d["beta_cases"])
assert d["invalid_inputs_rejected"] is True
assert d["historical_H3_H4_sources_modified"] is False
assert d["H3_Z20_reclosure_performed"] is False
assert d["q20_reclosure_performed"] is False
assert d["full_H4_Noether_derived"] is False
assert d["H4_Z21_solve_performed"] is False
assert d["Z21_window_local_particular_certified"] is False
assert d["lensing_licensed"] is False
print("CLASSIFICATION =",d["classification"])
for test in d["beta_cases"]:
    print("BETA",test["beta"],"TANGENT_REL_L2",
          test["eta_tangent_relative_L2"],"FROZEN_H3_REL_L2",
          test["H3_vs_frozen_reduced_Y_scalar_low_modes_relative_L2"],
          "FROZEN_H4_REL_L2",
          test["H4_vs_frozen_DY_scalar_relative_L2"])
print("H3_PARENT_RECLOSURE_PERFORMED =",d["H3_Z20_reclosure_performed"])
print("Z21_CERTIFIED =",d["Z21_window_local_particular_certified"])
print("GE19_H4_STAGEE_LOCAL_SOURCE_ROWS_PASS")
PY

sha256sum "$JSON" "$FULL"
wc -c "$JSON" "$FULL"
