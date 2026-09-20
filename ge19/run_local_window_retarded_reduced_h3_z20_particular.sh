#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results

echo "=== GE19 lock audit ==="
test "$(git rev-parse HEAD:ge19/predata_window_retarded_reduced_h3_z20_particular.json)" = "4339e87d2e9aa38f09bb1d7cd0a43305f10286e1"
test "$(git rev-parse HEAD:ge19/predata_amendment01_reduced_h1_reclosure.json)" = "180b41bd6e74fecb522a50415aadef0fd1442390"
test "$(git rev-parse HEAD:ge19/window_retarded_reduced_h3_z20_particular.py)" = "bcb3b9aabbea6be1e20c2b381652d90fc1012918"
test "$(git rev-parse HEAD:docs/ge19_window_retarded_reduced_h3_z20_particular_implementation_lock.md)" = "0f897503127bf76c76877bda2b1f5116509fb064"

test "$(git rev-parse HEAD:ge06/analytic_aest_directional_source_generator.py)" = "a7afe0035054a9dca55d74a6497c081422114b4c"
test "$(git rev-parse HEAD:ge07/pressureless_matter_directional_source_generator.py)" = "cde8da77a80799cef00fc7c09c3633310fc9e3d4"
test "$(git rev-parse HEAD:ge09/repair01_dense_accepted_step_local_jet_bridge.py)" = "509fa9d7bb323034bbf77b26792f35e1cc2ff7c7"
test "$(git rev-parse HEAD:ge18/repair01_on_shell_matched_dust_first_order_bridge.py)" = "b469b3c44eb8cf6c2545f80fccce5ad811ba8c33"
test "$(git rev-parse HEAD:docs/ge18_repair01_on_shell_matched_dust_first_order_bridge_result_freeze.md)" = "fffcb475ea4279bd608df8e70cbf20f3e0f33b74"
test "$(git rev-parse HEAD:.github/workflows/ge19-static-prelock-audit.yml)" = "109713ca676f4b2b241c10a34966009ed3857cfb"

git merge-base --is-ancestor c1808a3e6e746dfdda08c34a957f2db64bb66e0e HEAD
git merge-base --is-ancestor 1e3dd6c3d08a18b35ad42ab08b3ce9a2cb8382f1 HEAD
git merge-base --is-ancestor dcfe59d85c53f244fa6c3c131575d14566339089 HEAD
git merge-base --is-ancestor f8ee1f794052791a46ad72ddea1bf00b4df24e3b HEAD

echo "GE19_LOCK_PASS"

echo "=== GE19 required local parents ==="
for f in   results/ge15_R1_dense_accepted_step_trace.dat   results/ge15_cancellation_free_s_state_precision_closure.json   results/ge15_cancellation_free_s_state_precision_closure.npz   results/ge18_repair01_on_shell_matched_dust_first_order_bridge.json   results/ge18_repair01_on_shell_matched_dust_first_order_bridge.npz
do
  test -s "$f" || { echo "MISSING=$f"; exit 4; }
done
echo "GE19_LOCAL_INPUTS_PRESENT"

python3 -m pip install numpy scipy sympy >/dev/null
python3 -m py_compile ge19/window_retarded_reduced_h3_z20_particular.py

rm -f   results/ge19_window_retarded_reduced_h3_z20_particular.json   results/ge19_window_retarded_reduced_h3_z20_particular.npz   results/ge19_window_retarded_reduced_h3_z20_particular_FULL.log

echo "=== GE19 science execution ==="
set +e
python3 ge19/window_retarded_reduced_h3_z20_particular.py   --results-dir results   --json-out results/ge19_window_retarded_reduced_h3_z20_particular.json   --npz-out results/ge19_window_retarded_reduced_h3_z20_particular.npz   2>&1 | tee results/ge19_window_retarded_reduced_h3_z20_particular_FULL.log
RC=${PIPESTATUS[0]}
set -e

echo "=== GE19 summary ==="
if test -s results/ge19_window_retarded_reduced_h3_z20_particular.json; then
python3 - <<'PY'
import hashlib, json
from pathlib import Path

p=Path("results/ge19_window_retarded_reduced_h3_z20_particular.json")
d=json.loads(p.read_text())
print("CLASSIFICATION =",d.get("classification"))
print("FAILURE_STAGE =",d.get("failure_stage"))
print("PROVENANCE =",d.get("provenance"))

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
    "results/ge19_window_retarded_reduced_h3_z20_particular.json",
    "results/ge19_window_retarded_reduced_h3_z20_particular.npz",
    "results/ge19_window_retarded_reduced_h3_z20_particular_FULL.log",
]:
    q=Path(fn)
    if q.exists():
        print("SHA256",fn,hashlib.sha256(q.read_bytes()).hexdigest(),"BYTES",q.stat().st_size)
PY
fi

if [ "$RC" -ne 0 ]; then
  echo "GE19_EXIT=$RC"
  exit "$RC"
fi

test -s results/ge19_window_retarded_reduced_h3_z20_particular.npz
echo "GE19_EXIT=0"
