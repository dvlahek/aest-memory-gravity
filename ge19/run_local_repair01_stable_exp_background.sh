#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results

echo "=== GE19 Repair01 lock audit ==="
test "$(git rev-parse HEAD:ge19/repair01_predata_stable_exp_background_coordinate.json)" = "0ffceb5537e18d71c8a37ce3d41e7a967cfd7288"
test "$(git rev-parse HEAD:ge19/repair01_predata_amendment01_native_I0_reconstruction.json)" = "17840209d46d8cda2f4042fce086faaadca17ef2"
test "$(git rev-parse HEAD:ge19/repair01_predata_amendment02_stable_symbolic_relambdification.json)" = "288ff23a705fb8ac6d81a1b63a970e8b8ae74944"
test "$(git rev-parse HEAD:ge19/repair01_window_retarded_reduced_h3_z20_particular.py)" = "930c658b7c135ba4bb31d783c65d330eaa8bfb7f"
test "$(git rev-parse HEAD:docs/ge19_repair01_stable_exp_background_implementation_lock.md)" = "61a9f64b27bcd6998e6a7fd1d12b76de62e773ae"
test "$(git rev-parse HEAD:.github/workflows/ge19-repair01-static-prelock-audit.yml)" = "23dfc50fda254c4a13e63820b5654bba9806ee1e"

test "$(git rev-parse HEAD:ge06/analytic_aest_directional_source_generator.py)" = "a7afe0035054a9dca55d74a6497c081422114b4c"
test "$(git rev-parse HEAD:ge07/pressureless_matter_directional_source_generator.py)" = "cde8da77a80799cef00fc7c09c3633310fc9e3d4"
test "$(git rev-parse HEAD:ge09/repair01_dense_accepted_step_local_jet_bridge.py)" = "509fa9d7bb323034bbf77b26792f35e1cc2ff7c7"

git merge-base --is-ancestor 57148a617503d8bf06c51dbe8fba308a7531fc9d HEAD
git merge-base --is-ancestor 2ba977a02781e46246b7daefd8f067e9fd93a648 HEAD
git merge-base --is-ancestor 807d207cfde68b62ccbbe474ea0b41ea524d38a1 HEAD
git merge-base --is-ancestor 9b0d0626bd1a5bc0e2e070076283499000c666cb HEAD
git merge-base --is-ancestor 608e4710f348bd99161abe7664f6e11d51e19335 HEAD

echo "GE19_REPAIR01_LOCK_PASS"

echo "=== GE19 Repair01 required local parents ==="
for f in   results/ge15_R1_dense_accepted_step_trace.dat   results/ge15_cancellation_free_s_state_precision_closure.json   results/ge15_cancellation_free_s_state_precision_closure.npz   results/ge18_repair01_on_shell_matched_dust_first_order_bridge.json   results/ge18_repair01_on_shell_matched_dust_first_order_bridge.npz
do
  test -s "$f" || { echo "MISSING=$f"; exit 4; }
done
echo "GE19_REPAIR01_LOCAL_INPUTS_PRESENT"

python3 -m pip install numpy scipy sympy >/dev/null
python3 -m py_compile ge19/repair01_window_retarded_reduced_h3_z20_particular.py

rm -f   results/ge19_repair01_window_retarded_reduced_h3_z20_particular.json   results/ge19_repair01_window_retarded_reduced_h3_z20_particular.npz   results/ge19_repair01_window_retarded_reduced_h3_z20_particular_FULL.log

echo "=== GE19 Repair01 science execution ==="
set +e
python3 ge19/repair01_window_retarded_reduced_h3_z20_particular.py   --results-dir results   --json-out results/ge19_repair01_window_retarded_reduced_h3_z20_particular.json   --npz-out results/ge19_repair01_window_retarded_reduced_h3_z20_particular.npz   2>&1 | tee results/ge19_repair01_window_retarded_reduced_h3_z20_particular_FULL.log
RC=${PIPESTATUS[0]}
set -e

echo "=== GE19 Repair01 summary ==="
if test -s results/ge19_repair01_window_retarded_reduced_h3_z20_particular.json; then
python3 - <<'PY'
import hashlib, json
from pathlib import Path

p=Path("results/ge19_repair01_window_retarded_reduced_h3_z20_particular.json")
d=json.loads(p.read_text())

print("CLASSIFICATION =",d.get("classification"))
print("FAILURE_STAGE =",d.get("failure_stage"))

prov=d.get("provenance",{})
print("STABLE_EXP_NATIVE_DIAGNOSTIC =",prov.get("stable_exp_background_native_diagnostic"))
print("STABLE_EXP_NATIVE_GATES =",prov.get("stable_exp_background_native_gates"))
print("STABLE_GE06_BENIGN_EQUIVALENCE =",prov.get("stable_GE06_benign_equivalence"))
print("PROVENANCE =",prov)

h1=d.get("stage_A_reduced_H1")
if h1:
    print("STAGE_A_PASS =",h1.get("pass"))
    print("STAGE_A_GATES =",h1.get("gates"))
    print("STAGE_A_CONTROLS =",h1.get("controls"))

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
    "results/ge19_repair01_window_retarded_reduced_h3_z20_particular.json",
    "results/ge19_repair01_window_retarded_reduced_h3_z20_particular.npz",
    "results/ge19_repair01_window_retarded_reduced_h3_z20_particular_FULL.log",
]:
    q=Path(fn)
    if q.exists():
        print("SHA256",fn,hashlib.sha256(q.read_bytes()).hexdigest(),"BYTES",q.stat().st_size)
PY
fi

echo "GE19_REPAIR01_EXIT=$RC"
exit "$RC"
