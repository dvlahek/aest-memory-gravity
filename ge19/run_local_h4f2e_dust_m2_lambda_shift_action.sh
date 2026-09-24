#!/usr/bin/env bash
# GE19 H4F2e: source-only dust/M2/Lambda action-row local reproduction.
# Run the frozen GE05/GE07 generators in an isolated temporary CWD so
# their module-level output files NEVER overwrite historical repo/results.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results

test "$(git rev-parse HEAD:ge19/h4f2e_predata_dust_m2_lambda_shift_action.json)" = "a48ea8b15bf1c1141d9407c7400f416171f4b22b"
test "$(git rev-parse HEAD:ge19/h4f2e_dust_m2_lambda_shift_action_audit.py)" = "7dab9b996fc97ca9a291eb90166babec1abfba23"
test "$(git rev-parse HEAD:docs/ge19_h4f2e_dust_m2_lambda_shift_valid_freeze.md)" = "4323fc1dd5b71353a6ac418108953f473137363b"
test "$(git rev-parse HEAD:.github/workflows/ge19-h4f2e-shift-action.yml)" = "1e24ccf1efe98beb876e6a0f3741d13190641eac"
test "$(git rev-parse HEAD:ge05/memory_directional_source_generator.py)" = "40837d77f89028da30c28899e2d0530a4401844e"
test "$(git rev-parse HEAD:ge07/pressureless_matter_directional_source_generator.py)" = "cde8da77a80799cef00fc7c09c3633310fc9e3d4"
test "$(git rev-parse HEAD:ge19/repair37_cancellation_safe_fd8_h4_z21_reclosure.py)" = "45d203a092f9ac71cc612b15df5f0c0c630f5898"
for path in \
  ge19/h4f2e_predata_dust_m2_lambda_shift_action.json \
  ge19/h4f2e_dust_m2_lambda_shift_action_audit.py \
  docs/ge19_h4f2e_dust_m2_lambda_shift_valid_freeze.md \
  ge05/memory_directional_source_generator.py \
  ge07/pressureless_matter_directional_source_generator.py \
  ge19/repair37_cancellation_safe_fd8_h4_z21_reclosure.py
do
  git diff --quiet -- "$path"
  git diff --cached --quiet -- "$path"
done
echo GE19_H4F2E_LOCAL_LOCK_PASS

if [[ -z "${VIRTUAL_ENV:-}" ]]; then
  echo "GE19_H4F2E_VENV_NOT_ACTIVE: source .venv/bin/activate"
  exit 5
fi
python3 -c 'import numpy, scipy, sympy'
python3 -m py_compile ge19/h4f2e_dust_m2_lambda_shift_action_audit.py
echo GE19_H4F2E_LOCAL_PREEXECUTION_PASS

JSON="$ROOT/results/ge19_h4f2e_dust_m2_lambda_shift_action_LOCAL.json"
FULL="$ROOT/results/ge19_h4f2e_dust_m2_lambda_shift_action_LOCAL_FULL.log"
rm -f "$JSON" "$FULL"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/results"
export PYTHONPATH="$ROOT"
cd "$TMP"
echo GE19_H4F2E_GENERATOR_OUTPUT_ISOLATED_PASS

set +e
python3 -m ge19.h4f2e_dust_m2_lambda_shift_action_audit \
  --json-out "$JSON" 2>&1 | tee "$FULL" | tail -n 18
rc=${PIPESTATUS[0]}
set -e
cd "$ROOT"

if [[ -s "$JSON" ]]; then
python3 - <<'PY'
import json
d=json.load(open("results/ge19_h4f2e_dust_m2_lambda_shift_action_LOCAL.json"))
print("CLASSIFICATION =",d["classification"])
print("ALL_SUBSET_GATES_PASS =",d["all_subset_gates_pass"])
print("FAILED_BINDINGS =",[k for k,v in d["exact_source_action_bindings"].items() if not v])
print("FAILED_GE07_ACTION_GATES =",[k for k,v in d["GE07_mixed_shift_polarization"].items() if not v])
print("M2_NUMERIC =",d["deterministic_frozen_GE05_M2_shift"])
print("FULL_H4_NOETHER_DERIVED =",d["full_six_piece_H4_source_parent_Noether_derived"])
print("Z21_CERTIFIED =",d["Z21_certified"])
assert d["classification"]=="GE19_H4F2E_SHIFT_ACTION_SUBIDENTITY_PASS"
assert d["all_subset_gates_pass"] is True
assert all(x["exact"] for x in d["frozen_blobs"].values())
assert all(d["exact_source_action_bindings"].values())
assert all(d["GE07_mixed_shift_polarization"].values())
assert d["deterministic_frozen_GE05_M2_shift"]["gates_pass"] is True
assert d["full_six_piece_H4_source_parent_Noether_derived"] is False
assert d["corrected_parent_common_grid_evaluated"] is False
assert d["H4_Z21_solve_performed"] is False
assert d["Z21_certified"] is False
print("GE19_H4F2E_LOCAL_ACTION_SUBIDENTITY_PASS")
PY
fi
for p in "$JSON" "$FULL"; do
  if [[ -s "$p" ]]; then
    sha256sum "$p"
    wc -c "$p"
  fi
done
if [[ "$rc" -ne 0 || ! -s "$JSON" ]]; then
  echo GE19_H4F2E_LOCAL_SOURCE_OR_EXECUTION_FAIL
  if [[ "$rc" -ne 0 ]]; then exit "$rc"; fi
  exit 3
fi
