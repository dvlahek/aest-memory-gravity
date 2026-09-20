#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results

echo "=== GE19 Repair03 lock audit ==="
test "$(git rev-parse HEAD:ge19/repair03_predata_canonical_exp_product_evaluation.json)" = "a70ca4ef4ef208256913cde842d0238178ab44bb"
test "$(git rev-parse HEAD:ge19/repair03_window_retarded_reduced_h3_z20_particular.py)" = "123750fbb4db21e36d8baeb7947a381ccb2bb43e"
test "$(git rev-parse HEAD:docs/ge19_repair03_canonical_exp_product_implementation_lock.md)" = "10a149bba81ca57ae1ab75049be5e0e9f9110740"
test "$(git rev-parse HEAD:.github/workflows/ge19-repair03-prelock-audit.yml)" = "ed6bf61253058b4432e7771ed11a99b330c76de8"

test "$(git rev-parse HEAD:ge19/repair02_predata_frozen_symbol_tuple_capture.json)" = "286891c23de22bdf58a6d0a11684b5d43d857f9e"
test "$(git rev-parse HEAD:ge19/repair01_predata_stable_exp_background_coordinate.json)" = "0ffceb5537e18d71c8a37ce3d41e7a967cfd7288"
test "$(git rev-parse HEAD:ge19/repair01_predata_amendment01_native_I0_reconstruction.json)" = "17840209d46d8cda2f4042fce086faaadca17ef2"
test "$(git rev-parse HEAD:ge19/repair01_predata_amendment02_stable_symbolic_relambdification.json)" = "288ff23a705fb8ac6d81a1b63a970e8b8ae74944"
test "$(git rev-parse HEAD:docs/ge19_repair02_exp_product_implementation_fail_freeze.md)" = "6da644078429014f36626d0849723b5c488f0343"

test "$(git rev-parse HEAD:ge06/analytic_aest_directional_source_generator.py)" = "a7afe0035054a9dca55d74a6497c081422114b4c"
test "$(git rev-parse HEAD:ge07/pressureless_matter_directional_source_generator.py)" = "cde8da77a80799cef00fc7c09c3633310fc9e3d4"
test "$(git rev-parse HEAD:ge09/repair01_dense_accepted_step_local_jet_bridge.py)" = "509fa9d7bb323034bbf77b26792f35e1cc2ff7c7"

git merge-base --is-ancestor 3b4f616da93d3da4f4c8af7b27f868cfba90d238 HEAD
git merge-base --is-ancestor 1795d627668b3e301f65df91deece007a6409cfb HEAD
git merge-base --is-ancestor 5e27feb8daafa05add9f366b0e245b9f31ebcaf4 HEAD
git merge-base --is-ancestor 911ff1847609ff2470012dab2388f153ff5a3d93 HEAD

echo "GE19_REPAIR03_LOCK_PASS"

echo "=== GE19 Repair03 required local parents ==="
for f in   results/ge15_R1_dense_accepted_step_trace.dat   results/ge15_cancellation_free_s_state_precision_closure.json   results/ge15_cancellation_free_s_state_precision_closure.npz   results/ge18_repair01_on_shell_matched_dust_first_order_bridge.json   results/ge18_repair01_on_shell_matched_dust_first_order_bridge.npz
do
  test -s "$f" || { echo "MISSING=$f"; exit 4; }
done
echo "GE19_REPAIR03_LOCAL_INPUTS_PRESENT"

python3 -m pip install numpy scipy sympy >/dev/null
python3 -m py_compile ge19/repair03_window_retarded_reduced_h3_z20_particular.py

rm -f   results/ge19_repair03_window_retarded_reduced_h3_z20_particular.json   results/ge19_repair03_window_retarded_reduced_h3_z20_particular.npz   results/ge19_repair03_window_retarded_reduced_h3_z20_particular_FULL.log

echo "=== GE19 Repair03 science execution ==="
set +e
python3 ge19/repair03_window_retarded_reduced_h3_z20_particular.py   --results-dir results   --json-out results/ge19_repair03_window_retarded_reduced_h3_z20_particular.json   --npz-out results/ge19_repair03_window_retarded_reduced_h3_z20_particular.npz   2>&1 | tee results/ge19_repair03_window_retarded_reduced_h3_z20_particular_FULL.log
RC=${PIPESTATUS[0]}
set -e

echo "=== GE19 Repair03 summary ==="
if test -s results/ge19_repair03_window_retarded_reduced_h3_z20_particular.json; then
python3 - <<'PY'
import hashlib, json
from pathlib import Path

p=Path("results/ge19_repair03_window_retarded_reduced_h3_z20_particular.json")
d=json.loads(p.read_text())

print("CLASSIFICATION =",d.get("classification"))
print("FAILURE_STAGE =",d.get("failure_stage"))

prov=d.get("provenance",{})
print("STABLE_GE06_SYMBOL_CONTRACT =",prov.get("stable_GE06_symbol_contract"))
print("STABLE_GE06_SYMBOLIC_EXP_AUDIT =",prov.get("stable_GE06_symbolic_exp_audit"))
print("STABLE_GE06_BENIGN_EQUIVALENCE =",prov.get("stable_GE06_benign_equivalence"))
print("STABLE_GE06_PHYSICAL_PARAMETER_PROBE =",prov.get("stable_GE06_physical_parameter_probe"))
print("STABLE_EXP_NATIVE_DIAGNOSTIC =",prov.get("stable_exp_background_native_diagnostic"))
print("STABLE_EXP_NATIVE_GATES =",prov.get("stable_exp_background_native_gates"))

h1=d.get("stage_A_reduced_H1")
if h1:
    print("STAGE_A_PASS =",h1.get("pass"))
    print("STAGE_A_GATES =",h1.get("gates"))
    ctl=h1.get("controls",{})
    print("STAGE_A_MAX_LINEAR_RES =",ctl.get("max_linear_system_relative_L2"))
    print("STAGE_A_MAX_SHIFT_CONSTRAINT =",ctl.get("max_shift_constraint_relative_L2"))
    print("STAGE_A_MAX_ANISOTROPY_CONSTRAINT =",ctl.get("max_anisotropy_constraint_relative_L2"))
    print("STAGE_A_TIME_GRID_MAX =",ctl.get("primary64_vs_control32_state_global_relative_L2_max"))
    print("STAGE_A_INITIAL_MATCH_MAX =",ctl.get("max_initial_dynamic_match_abs_or_rel"))

if "source_spatial_convergence" in d:
    print("SOURCE_SPATIAL_MAX =",d["source_spatial_convergence"]["relative_L2_max"])
if "primary_solve_controls" in d:
    print("Z20_LINEAR_RES_MAX =",d["primary_solve_controls"]["max_linear_system_relative_L2"])
    print("Z20_SHIFT_CONSTRAINT_MAX =",d["primary_solve_controls"]["max_shift_constraint_relative_L2"])
    print("Z20_ANISOTROPY_CONSTRAINT_MAX =",d["primary_solve_controls"]["max_anisotropy_constraint_relative_L2"])
if "time_grid_control" in d:
    print("Z20_TIME_GRID_MAX =",d["time_grid_control"]["state_relative_L2_max"])

print("GATES =",d.get("gates"))
print("PROJECT_BOUNDARY =",d.get("project_boundary"))

for fn in [
    "results/ge19_repair03_window_retarded_reduced_h3_z20_particular.json",
    "results/ge19_repair03_window_retarded_reduced_h3_z20_particular.npz",
    "results/ge19_repair03_window_retarded_reduced_h3_z20_particular_FULL.log",
]:
    q=Path(fn)
    if q.exists():
        print("SHA256",fn,hashlib.sha256(q.read_bytes()).hexdigest(),"BYTES",q.stat().st_size)
PY
fi

echo "GE19_REPAIR03_EXIT=$RC"
exit "$RC"
