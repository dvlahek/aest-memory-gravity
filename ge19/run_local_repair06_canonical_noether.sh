#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results

echo "=== GE19 Repair06 lock audit ==="

test "$(git rev-parse HEAD:docs/ge19_repair05_reduced_h1_result_freeze.md)" = "51a8ade089fd3bc1521f72dd6415fd21aa179e45"
test "$(git rev-parse HEAD:ge19/repair06_predata_canonical_momentum_time_march.json)" = "8f2764ef1b1ffc1517b35973f5badc50a43cd813"
test "$(git rev-parse HEAD:ge19/repair06_predata_amendment01_noether_regularized_dae_partition.json)" = "458fd5958f2915e49dda36063ccaaa468d4b6e7c"
test "$(git rev-parse HEAD:ge19/repair06_predata_amendment02_full_stable_Z_polynomial_normalization.json)" = "cf4c2e03029ce7cfc493207592fc1122e33c4ecd"
test "$(git rev-parse HEAD:ge19/repair06_window_retarded_reduced_h3_z20_particular.py)" = "98690421ed57f266745348bf56e2664d6fb9047a"
test "$(git rev-parse HEAD:.github/workflows/ge19-repair06-prelock-audit.yml)" = "4d3dcc68ba03c4de8b5db18830ad542ca01db3f6"
test "$(git rev-parse HEAD:docs/ge19_repair06_canonical_noether_implementation_lock.md)" = "a10c06e26e985d875283526a50aa7bd4accf828f"

test "$(git rev-parse HEAD:ge06/analytic_aest_directional_source_generator.py)" = "a7afe0035054a9dca55d74a6497c081422114b4c"
test "$(git rev-parse HEAD:ge07/pressureless_matter_directional_source_generator.py)" = "cde8da77a80799cef00fc7c09c3633310fc9e3d4"
test "$(git rev-parse HEAD:ge09/repair01_dense_accepted_step_local_jet_bridge.py)" = "509fa9d7bb323034bbf77b26792f35e1cc2ff7c7"

for sha in   9a23f885cb96005a3a0199abe545f8283ba44027   0093500d8be6e7979544222157ce0dd268a8292d   8c9e4fac8b3fe0dd9326ff0b17615f8a346c26c3   f0283e875258b68c071888062d9519a81d968f24   bee22d28ec5dba8f19ad2da29096bc6bfea7d288   37f0206de022a440f0f69a3fa57c9e58223008f1   075df17104ddf8b970633e3acec1fd122b06b9ca
do
  git merge-base --is-ancestor "$sha" HEAD
done

echo "GE19_REPAIR06_LOCK_PASS"

echo "=== GE19 Repair06 Python environment ==="
if [[ -z "${VIRTUAL_ENV:-}" ]]; then
  echo "GE19_REPAIR06_VENV_NOT_ACTIVE"
  echo "Run: source .venv/bin/activate"
  exit 5
fi
python3 - <<'PY'
import numpy, scipy, sympy
print("GE19_REPAIR06_PYTHON_ENV_PASS")
print("PYTHON_NUMPY =",numpy.__version__)
print("PYTHON_SCIPY =",scipy.__version__)
print("PYTHON_SYMPY =",sympy.__version__)
PY
python3 -m py_compile ge19/repair06_window_retarded_reduced_h3_z20_particular.py

echo "=== GE19 Repair06 required frozen local parents ==="
for f in   results/ge15_R1_dense_accepted_step_trace.dat   results/ge15_cancellation_free_s_state_precision_closure.json   results/ge15_cancellation_free_s_state_precision_closure.npz   results/ge18_repair01_on_shell_matched_dust_first_order_bridge.json   results/ge18_repair01_on_shell_matched_dust_first_order_bridge.npz
do
  test -s "$f" || { echo "MISSING=$f"; exit 4; }
done
echo "GE19_REPAIR06_LOCAL_INPUTS_PRESENT"

rm -f   results/ge19_repair06_window_retarded_reduced_h3_z20_particular.json   results/ge19_repair06_window_retarded_reduced_h3_z20_particular.npz   results/ge19_repair06_window_retarded_reduced_h3_z20_particular_FULL.log

echo "=== GE19 Repair06 science execution ==="
set +e
python3 ge19/repair06_window_retarded_reduced_h3_z20_particular.py   --results-dir results   --json-out results/ge19_repair06_window_retarded_reduced_h3_z20_particular.json   --npz-out results/ge19_repair06_window_retarded_reduced_h3_z20_particular.npz   2>&1 | tee results/ge19_repair06_window_retarded_reduced_h3_z20_particular_FULL.log
RC=${PIPESTATUS[0]}
set -e

echo "=== GE19 Repair06 summary ==="
if test -s results/ge19_repair06_window_retarded_reduced_h3_z20_particular.json; then
python3 - <<'PY'
import hashlib,json
from pathlib import Path
p=Path("results/ge19_repair06_window_retarded_reduced_h3_z20_particular.json")
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
    print("STAGE_A_MAX_SHIFT_CONSTRAINT =",c.get("max_shift_constraint_relative_L2"))
    print("STAGE_A_MAX_ANISOTROPY_CONSTRAINT =",c.get("max_anisotropy_constraint_relative_L2"))
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
        print("STAGE_A_RADAU_SCALED_RES_MAX =",mx("radau_block_scaled_relative_L2_residual_max"))
        print("STAGE_A_RADAU_CONDITION_MAX =",mx("radau_scaled_condition_2_max"))
        print("STAGE_A_LOCAL_ALG_CONDITION_MAX =",mx("local_algebraic_scaled_condition_2_max"))
        print("STAGE_A_LAPSE_NOETHER_RES_MAX =",mx("lapse_noether_row_relative_residual_max"))
        print("STAGE_A_NOETHER_NULL_MAX =",mx("old_partition_noether_null_scaled_L2"))

if "source_spatial_convergence" in d:
    z=d["source_spatial_convergence"]
    print("SOURCE_SPATIAL_MAX =",z.get("relative_L2_max"))
if "primary_solve_controls" in d:
    z=d["primary_solve_controls"]
    print("Z20_LINEAR_RES_MAX =",z.get("max_linear_system_relative_L2"))
    print("Z20_SHIFT_CONSTRAINT_MAX =",z.get("max_shift_constraint_relative_L2"))
    print("Z20_ANISOTROPY_CONSTRAINT_MAX =",z.get("max_anisotropy_constraint_relative_L2"))
if "time_grid_control" in d:
    z=d["time_grid_control"]
    print("Z20_TIME_GRID_MAX =",z.get("state_relative_L2_max"))

print("Z20_CONSTRUCTED =",d.get("Z20_constructed"))
print("GATES =",d.get("gates"))
print("CLAIM_BOUNDARY =",d.get("claim_boundary",d.get("project_boundary")))

for fn in [
  "results/ge19_repair06_window_retarded_reduced_h3_z20_particular.json",
  "results/ge19_repair06_window_retarded_reduced_h3_z20_particular.npz",
  "results/ge19_repair06_window_retarded_reduced_h3_z20_particular_FULL.log",
]:
    q=Path(fn)
    if q.exists():
        print("SHA256",fn,hashlib.sha256(q.read_bytes()).hexdigest(),"BYTES",q.stat().st_size)
PY
fi

echo "GE19_REPAIR06_EXIT=$RC"
exit "$RC"
