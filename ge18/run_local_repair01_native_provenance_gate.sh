#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results

echo "=== GE18 Repair01 lock audit ==="
test "$(git rev-parse HEAD:ge18/repair01_predata_native_provenance_gate.json)" = "2f5d9f7cd07cde97e1c1747c1bff015006ef2d96"
test "$(git rev-parse HEAD:ge18/repair01_on_shell_matched_dust_first_order_bridge.py)" = "b469b3c44eb8cf6c2545f80fccce5ad811ba8c33"
test "$(git rev-parse HEAD:docs/ge18_repair01_native_provenance_gate_implementation_lock.md)" = "41e2acf166b34011fffaaa0cb413473929b40c8a"
echo "GE18_REPAIR01_LOCK_PASS"

python3 -m py_compile ge18/repair01_on_shell_matched_dust_first_order_bridge.py

echo "=== Required local GE15 outputs ==="
for f in   results/ge15_R1_dense_accepted_step_trace.dat   results/ge15_R1_cli_background.dat   results/ge15_cancellation_free_s_state_precision_closure.json   results/ge15_R1_cli_perturbations_k0_s.dat   results/ge15_R1_cli_perturbations_k1_s.dat   results/ge15_R1_cli_perturbations_k2_s.dat   results/ge15_R1_cli_perturbations_k3_s.dat   results/ge15_R1_cli_perturbations_k4_s.dat   results/ge15_R1_cli_perturbations_k5_s.dat
do
  test -s "$f" || { echo "MISSING=$f"; exit 4; }
done
echo "GE18_REPAIR01_LOCAL_INPUTS_PASS"

set +e
python3 ge18/repair01_on_shell_matched_dust_first_order_bridge.py   --results-dir results   --json-out results/ge18_repair01_on_shell_matched_dust_first_order_bridge.json   --npz-out results/ge18_repair01_on_shell_matched_dust_first_order_bridge.npz   2>&1 | tee results/ge18_repair01_on_shell_matched_dust_first_order_bridge_FULL.log
RC=${PIPESTATUS[0]}
set -e

echo "=== GE18 Repair01 summary ==="
if test -s results/ge18_repair01_on_shell_matched_dust_first_order_bridge.json; then
python3 - <<'PY'
import json
d=json.load(open("results/ge18_repair01_on_shell_matched_dust_first_order_bridge.json"))
print("CLASSIFICATION =",d["classification"])
print("GATES =",d["gates"])
print("INPUT_PROVENANCE =",d["input_provenance"])
print("GLOBAL_MODEL_ERROR =",d["global_model_error"])
print("INTEGRATOR_CONTROLS =",d["integrator_controls"])
print("EXACT_MAP =",d["exact_map"])
print("PROJECT_BOUNDARY =",d["project_boundary"])
PY
fi

echo "EXIT=$RC"
exit "$RC"
