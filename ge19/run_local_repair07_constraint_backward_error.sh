#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results

echo "=== GE19 Repair07 lock audit ==="

test "$(git rev-parse HEAD:docs/ge19_repair06_reduced_h1_result_freeze.md)" = "db1097ff22a4df3212d6d9e78a2219e0dd1daa6c"
test "$(git rev-parse HEAD:ge19/repair07_predata_row_scaled_constraint_monitors.json)" = "2fbe567620009096b9789738c25e42ce372615a3"
test "$(git rev-parse HEAD:ge19/repair07_predata_amendment01_componentwise_backward_error_scale.json)" = "05fa5ac42b3c182876893762163dd699fe299333"
test "$(git rev-parse HEAD:ge19/repair07_window_retarded_reduced_h3_z20_particular.py)" = "e34d28a2062c748f48bc82fa928844b02631de25"
test "$(git rev-parse HEAD:.github/workflows/ge19-repair07-prelock-audit.yml)" = "3fb848eb344dcac9d9fd7dadb6d0e9c9962a6dd9"
test "$(git rev-parse HEAD:docs/ge19_repair07_constraint_monitor_implementation_lock.md)" = "80ea52b04f917f59a779fccfe124272c715889d6"

test "$(git rev-parse HEAD:ge06/analytic_aest_directional_source_generator.py)" = "a7afe0035054a9dca55d74a6497c081422114b4c"
test "$(git rev-parse HEAD:ge07/pressureless_matter_directional_source_generator.py)" = "cde8da77a80799cef00fc7c09c3633310fc9e3d4"
test "$(git rev-parse HEAD:ge09/repair01_dense_accepted_step_local_jet_bridge.py)" = "509fa9d7bb323034bbf77b26792f35e1cc2ff7c7"

for sha in   670990858ea38c56dbad1402eb360b7152d01350   ec93b9ebe23a5a5f0af3611c3291eb53fc55d777   d9e47705e98f22e36bd0a5fd53212962f1f67cc3   b129b1cebac4fb1d36060e4bef2a580eeb0e3b1f   442132d0a075b2f68b7b50a0e4ef0cf2bf90cd31
do
  git merge-base --is-ancestor "$sha" HEAD
done

echo "GE19_REPAIR07_LOCK_PASS"

echo "=== GE19 Repair07 Python environment ==="
if [[ -z "${VIRTUAL_ENV:-}" ]]; then
  echo "GE19_REPAIR07_VENV_NOT_ACTIVE"
  echo "Run: source .venv/bin/activate"
  exit 5
fi

python3 - <<'PY'
import numpy, scipy, sympy
print("GE19_REPAIR07_PYTHON_ENV_PASS")
print("PYTHON_NUMPY =",numpy.__version__)
print("PYTHON_SCIPY =",scipy.__version__)
print("PYTHON_SYMPY =",sympy.__version__)
PY

python3 -m py_compile ge19/repair07_window_retarded_reduced_h3_z20_particular.py

echo "=== GE19 Repair07 local monitor self-audit ==="
python3 - <<'PY'
import importlib.util
from pathlib import Path
import numpy as np

p=Path("ge19/repair07_window_retarded_reduced_h3_z20_particular.py").resolve()
spec=importlib.util.spec_from_file_location("ge19r7",p)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

g=m._constraint_backward_error(
    np.asarray([1.0,1.0],complex),
    np.asarray([1.0,1.0],complex),
    0.0,1.0,1.0
)
c=m._constraint_backward_error(
    np.asarray([1.0,-1.0],complex),
    np.asarray([1.0,1.0],complex),
    0.0,1.0,-1.0
)
eps=2.0**-45
q=m._constraint_backward_error(
    np.asarray([1.0,-1.0+eps],complex),
    np.asarray([1.0,1.0],complex),
    0.0,1.0,-1.0+eps
)
assert abs(g["metric"]-1.0)<=1e-15, g
assert c["metric"]==0.0, c
assert q["metric"]<1e-12, q
print("GE19_REPAIR07_LOCAL_MONITOR_SELF_AUDIT_PASS")
print("GENUINE_VIOLATION_METRIC =",g)
print("EXACT_CANCELLATION_METRIC =",c)
print("NEAR_CANCELLATION_METRIC =",q)
PY

echo "=== GE19 Repair07 required frozen local parents ==="
for f in   results/ge15_R1_dense_accepted_step_trace.dat   results/ge15_cancellation_free_s_state_precision_closure.json   results/ge15_cancellation_free_s_state_precision_closure.npz   results/ge18_repair01_on_shell_matched_dust_first_order_bridge.json   results/ge18_repair01_on_shell_matched_dust_first_order_bridge.npz
do
  test -s "$f" || { echo "MISSING=$f"; exit 4; }
done
echo "GE19_REPAIR07_LOCAL_INPUTS_PRESENT"

rm -f   results/ge19_repair07_window_retarded_reduced_h3_z20_particular.json   results/ge19_repair07_window_retarded_reduced_h3_z20_particular.npz   results/ge19_repair07_window_retarded_reduced_h3_z20_particular_FULL.log

echo "=== GE19 Repair07 science execution ==="
set +e
python3 ge19/repair07_window_retarded_reduced_h3_z20_particular.py   --results-dir results   --json-out results/ge19_repair07_window_retarded_reduced_h3_z20_particular.json   --npz-out results/ge19_repair07_window_retarded_reduced_h3_z20_particular.npz   2>&1 | tee results/ge19_repair07_window_retarded_reduced_h3_z20_particular_FULL.log
RC=${PIPESTATUS[0]}
set -e

echo "=== GE19 Repair07 summary ==="
if test -s results/ge19_repair07_window_retarded_reduced_h3_z20_particular.json; then
python3 - <<'PY'
import hashlib,json
from pathlib import Path

p=Path("results/ge19_repair07_window_retarded_reduced_h3_z20_particular.json")
d=json.loads(p.read_text())

print("CLASSIFICATION =",d.get("classification"))
print("FAILURE_STAGE =",d.get("failure_stage"))
prov=d.get("provenance",{})
print("ACTIVE_LINEAR_GE06_COORDINATE =",prov.get("active_linear_GE06_background_coordinate"))
print("BACKGROUND_MODE_MISMATCH =",prov.get("GE15_background_mode_mismatch_max"))
print("BACKGROUND_MODE_MISMATCH_STATUS =",prov.get("GE15_background_mode_mismatch_gate_status"))

h1=d.get("stage_A_reduced_H1")
if h1:
    c=h1.get("controls",{})
    print("STAGE_A_PASS =",h1.get("pass"))
    print("STAGE_A_GATES =",h1.get("gates"))
    print("STAGE_A_MAX_LINEAR_RES =",c.get("max_linear_system_relative_L2"))
    print("STAGE_A_MAX_SHIFT_BACKWARD_ERROR =",c.get("max_shift_constraint_relative_L2"))
    print("STAGE_A_MAX_ANISOTROPY_BACKWARD_ERROR =",c.get("max_anisotropy_constraint_relative_L2"))
    print("STAGE_A_TIME_GRID_MAX =",c.get("primary64_vs_control32_state_global_relative_L2_max"))
    print("STAGE_A_INITIAL_MATCH_MAX =",c.get("max_initial_dynamic_match_abs_or_rel"))

    diags=[]
    for row in c.get("rows",[]):
        for grid in ("primary","control"):
            diags.extend(row.get(grid,{}).get("canonical_march_diagnostics",[]))
    if diags:
        def mx(key):
            vals=[q.get(key) for q in diags if q.get(key) is not None]
            return max(vals) if vals else None
        print("STAGE_A_OLD_SHIFT_PIECE_METRIC_MAX =",mx("shift_constraint_piece_normalized_diagnostic_max"))
        print("STAGE_A_OLD_ANISOTROPY_PIECE_METRIC_MAX =",mx("anisotropy_constraint_piece_normalized_diagnostic_max"))
        print("STAGE_A_SHIFT_ABS_RESIDUAL_MAX =",mx("shift_constraint_absolute_residual_max"))
        print("STAGE_A_ANISOTROPY_ABS_RESIDUAL_MAX =",mx("anisotropy_constraint_absolute_residual_max"))
        print("STAGE_A_SHIFT_SCALE_MAX =",mx("shift_constraint_row_scale_max"))
        print("STAGE_A_ANISOTROPY_SCALE_MAX =",mx("anisotropy_constraint_row_scale_max"))
        print("STAGE_A_RADAU_SCALED_RES_MAX =",mx("radau_block_scaled_relative_L2_residual_max"))
        print("STAGE_A_RADAU_CONDITION_MAX =",mx("radau_scaled_condition_2_max"))
        print("STAGE_A_LOCAL_ALG_CONDITION_MAX =",mx("local_algebraic_scaled_condition_2_max"))
        print("STAGE_A_LAPSE_NOETHER_RES_MAX =",mx("lapse_noether_row_relative_residual_max"))

if "source_spatial_convergence" in d:
    z=d["source_spatial_convergence"]
    print("SOURCE_SPATIAL_MAX =",z.get("relative_L2_max"))
if "primary_solve_controls" in d:
    z=d["primary_solve_controls"]
    print("Z20_LINEAR_RES_MAX =",z.get("max_linear_system_relative_L2"))
    print("Z20_SHIFT_BACKWARD_ERROR_MAX =",z.get("max_shift_constraint_relative_L2"))
    print("Z20_ANISOTROPY_BACKWARD_ERROR_MAX =",z.get("max_anisotropy_constraint_relative_L2"))
if "time_grid_control" in d:
    print("Z20_TIME_GRID_MAX =",d["time_grid_control"].get("state_relative_L2_max"))

print("Z20_CONSTRUCTED =",d.get("Z20_constructed"))
print("GATES =",d.get("gates"))
print("CLAIM_BOUNDARY =",d.get("claim_boundary",d.get("project_boundary")))

for fn in [
  "results/ge19_repair07_window_retarded_reduced_h3_z20_particular.json",
  "results/ge19_repair07_window_retarded_reduced_h3_z20_particular.npz",
  "results/ge19_repair07_window_retarded_reduced_h3_z20_particular_FULL.log",
]:
    q=Path(fn)
    if q.exists():
        print("SHA256",fn,hashlib.sha256(q.read_bytes()).hexdigest(),"BYTES",q.stat().st_size)
PY
fi

echo "GE19_REPAIR07_EXIT=$RC"
exit "$RC"
