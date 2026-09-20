#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results

echo "=== GE18 lock audit ==="
test "$(git rev-parse HEAD:ge18/predata_on_shell_matched_dust_first_order_bridge.json)" = "f45ef8fae9b58870639ebc89e247a62551206dd0"
test "$(git rev-parse HEAD:ge18/on_shell_matched_dust_first_order_bridge.py)" = "769deae8001153c4c4feeba0584df288df334eb1"
test "$(git rev-parse HEAD:docs/ge18_on_shell_matched_dust_first_order_bridge_implementation_lock.md)" = "030908b1869a411284b81a853c9c594314aed082"
echo "GE18_LOCK_PASS"

python3 -m py_compile ge18/on_shell_matched_dust_first_order_bridge.py

echo "=== Required local GE15 outputs ==="
for f in   results/ge15_R1_dense_accepted_step_trace.dat   results/ge15_R1_cli_background.dat   results/ge15_cancellation_free_s_state_precision_closure.json   results/ge15_R1_cli_perturbations_k0_s.dat   results/ge15_R1_cli_perturbations_k1_s.dat   results/ge15_R1_cli_perturbations_k2_s.dat   results/ge15_R1_cli_perturbations_k3_s.dat   results/ge15_R1_cli_perturbations_k4_s.dat   results/ge15_R1_cli_perturbations_k5_s.dat
do
  test -s "$f" || { echo "MISSING=$f"; exit 4; }
done
echo "GE18_LOCAL_INPUTS_PASS"

set +e
python3 ge18/on_shell_matched_dust_first_order_bridge.py   --results-dir results   --json-out results/ge18_on_shell_matched_dust_first_order_bridge.json   --npz-out results/ge18_on_shell_matched_dust_first_order_bridge.npz   2>&1 | tee results/ge18_on_shell_matched_dust_first_order_bridge_FULL.log
RC=${PIPESTATUS[0]}
set -e

echo "=== GE18 summary ==="
if test -s results/ge18_on_shell_matched_dust_first_order_bridge.json; then
python3 - <<'PY'
import json
d=json.load(open("results/ge18_on_shell_matched_dust_first_order_bridge.json"))
print("CLASSIFICATION =",d["classification"])
print("GATES =",d["gates"])
print("GLOBAL_MODEL_ERROR =",d["global_model_error"])
print("INTEGRATOR_CONTROLS =",d["integrator_controls"])
print("EXACT_MAP =",d["exact_map"])
print("PROJECT_BOUNDARY =",d["project_boundary"])
print("PER_K_CSTAR =")
for row in d["per_k_model_error"]["C_star"]:
    print(row)
PY
fi

echo "EXIT=$RC"
exit "$RC"
