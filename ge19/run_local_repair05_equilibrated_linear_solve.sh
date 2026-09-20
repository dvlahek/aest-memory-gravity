#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results

echo "=== GE19 Repair05 lock audit ==="

test "$(git rev-parse HEAD:docs/ge19_repair04_reduced_h1_result_freeze.md)" = "d7057f104dbc95ac5cf5215ee0e7fe28b6ad462f"
test "$(git rev-parse HEAD:ge19/repair05_predata_equilibrated_linear_solve.json)" = "4ce7086dcf61e4ec704ec4a5f9fbbffa60fe9893"
test "$(git rev-parse HEAD:ge19/repair05_window_retarded_reduced_h3_z20_particular.py)" = "61a34c2253f5d7c6f66efb7ee50444d2a24ce03d"
test "$(git rev-parse HEAD:.github/workflows/ge19-repair05-prelock-audit.yml)" = "4bbc1b8504e735b985f00ee5122dcdbeb3d9aee3"
test "$(git rev-parse HEAD:docs/ge19_repair05_equilibrated_linear_solve_implementation_lock.md)" = "66cf64b996d6a3487339c0707d046df09664d463"

test "$(git rev-parse HEAD:ge06/analytic_aest_directional_source_generator.py)" = "a7afe0035054a9dca55d74a6497c081422114b4c"
test "$(git rev-parse HEAD:ge07/pressureless_matter_directional_source_generator.py)" = "cde8da77a80799cef00fc7c09c3633310fc9e3d4"
test "$(git rev-parse HEAD:ge09/repair01_dense_accepted_step_local_jet_bridge.py)" = "509fa9d7bb323034bbf77b26792f35e1cc2ff7c7"

git merge-base --is-ancestor 8b12628c5c80c1f92e3315c0e2dfbecbc58b419b HEAD
git merge-base --is-ancestor d488d1d406e523166777dfa46cf62bf98321fb9f HEAD
git merge-base --is-ancestor 01def6f57c37f5bd0e5e3d68c27ac5375aed4b83 HEAD
git merge-base --is-ancestor 0e4179f11cbe6cab15c1ea0611440ab4223fa590 HEAD
git merge-base --is-ancestor 64d7d0b4a9461184d45392c72b11fb3b5ed6f53a HEAD

echo "GE19_REPAIR05_LOCK_PASS"

echo "=== GE19 Repair05 Python environment ==="
if [[ -z "${VIRTUAL_ENV:-}" ]]; then
  echo "GE19_REPAIR05_VENV_NOT_ACTIVE"
  echo "Activate the repository .venv before running this locked diagnostic."
  exit 5
fi

python3 - <<'PY'
import numpy, scipy, sympy
print("GE19_REPAIR05_PYTHON_ENV_PASS")
print("PYTHON_NUMPY =", numpy.__version__)
print("PYTHON_SCIPY =", scipy.__version__)
print("PYTHON_SYMPY =", sympy.__version__)
PY

python3 -m py_compile ge19/repair05_window_retarded_reduced_h3_z20_particular.py

echo "=== GE19 Repair05 required local parents ==="
for f in \
  results/ge15_R1_dense_accepted_step_trace.dat \
  results/ge15_cancellation_free_s_state_precision_closure.json \
  results/ge15_cancellation_free_s_state_precision_closure.npz \
  results/ge18_repair01_on_shell_matched_dust_first_order_bridge.json \
  results/ge18_repair01_on_shell_matched_dust_first_order_bridge.npz
do
  test -s "$f" || { echo "MISSING=$f"; exit 4; }
done
echo "GE19_REPAIR05_LOCAL_INPUTS_PRESENT"

echo "=== GE19 Repair05 local numerical self-audit ==="
python3 - <<'PY'
import importlib.util
import inspect
from pathlib import Path
import numpy as np
from scipy.sparse import csr_matrix, diags

root=Path.cwd()
spec=importlib.util.spec_from_file_location(
    "ge19r5",
    root/"ge19/repair05_window_retarded_reduced_h3_z20_particular.py"
)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

src=inspect.getsource(m.linear_operator_batch)
assert 'Zb=bg["Z_action"][:,None]' in src
assert 'vals6=(aa,adot,Zb,' in src
assert 'Qb=bg["Q_action"][:,None]' not in src

n=48
base=np.eye(n,dtype=complex)
for i in range(n-1):
    base[i,i+1]=0.08+0.03j
    base[i+1,i]=-0.04+0.02j
row_phys=np.logspace(-24,24,n)
col_phys=np.logspace(20,-20,n)
A=diags(row_phys) @ csr_matrix(base) @ diags(col_phys)
x1=np.linspace(0.5,1.5,n)+1j*np.linspace(-0.2,0.3,n)
x2=np.cos(np.linspace(0,2,n))+0.1j*np.sin(np.linspace(0,3,n))
B=np.column_stack([A@x1,A@x2])

X,d=m.equilibrated_solve(A,B,max_refine=4)
rr=[]
for j in range(B.shape[1]):
    ax=A@X[:,j]
    rr.append(np.linalg.norm(ax-B[:,j])/max(np.linalg.norm(ax),np.linalg.norm(B[:,j]),m.TINY))
xerr=max(
    np.linalg.norm(X[:,0]-x1)/np.linalg.norm(x1),
    np.linalg.norm(X[:,1]-x2)/np.linalg.norm(x2),
)
assert max(rr)<=1e-12, (rr,d)
assert xerr<=1e-10, (xerr,d)
assert d["final_unscaled_relative_L2_max"]<=1e-12, d
assert d["scaled_matrix_abs_max"]<=1.0+1e-12, d
assert np.all(np.isfinite(X)), d

print("GE19_REPAIR05_LOCAL_NUMERICAL_SELF_AUDIT_PASS")
print("SYNTHETIC_RESIDUAL_MAX =",max(rr))
print("SYNTHETIC_SOLUTION_RELATIVE_L2_MAX =",xerr)
print("EQUILIBRATION_DIAGNOSTIC =",d)
PY

rm -f \
  results/ge19_repair05_window_retarded_reduced_h3_z20_particular.json \
  results/ge19_repair05_window_retarded_reduced_h3_z20_particular.npz \
  results/ge19_repair05_window_retarded_reduced_h3_z20_particular_FULL.log

echo "=== GE19 Repair05 science execution ==="
set +e
python3 ge19/repair05_window_retarded_reduced_h3_z20_particular.py \
  --results-dir results \
  --json-out results/ge19_repair05_window_retarded_reduced_h3_z20_particular.json \
  --npz-out results/ge19_repair05_window_retarded_reduced_h3_z20_particular.npz \
  2>&1 | tee results/ge19_repair05_window_retarded_reduced_h3_z20_particular_FULL.log
RC=${PIPESTATUS[0]}
set -e

echo "=== GE19 Repair05 summary ==="
if test -s results/ge19_repair05_window_retarded_reduced_h3_z20_particular.json; then
python3 - <<'PY'
import hashlib, json
from pathlib import Path

p=Path("results/ge19_repair05_window_retarded_reduced_h3_z20_particular.json")
d=json.loads(p.read_text())

print("CLASSIFICATION =",d.get("classification"))
print("FAILURE_STAGE =",d.get("failure_stage"))

prov=d.get("provenance",{})
print("ACTIVE_LINEAR_GE06_COORDINATE =",prov.get("active_linear_GE06_background_coordinate"))
print("BACKGROUND_MODE_MISMATCH =",prov.get("GE15_background_mode_mismatch_max"))
print("BACKGROUND_MODE_MISMATCH_STATUS =",prov.get("GE15_background_mode_mismatch_gate_status"))

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

    eq=[]
    for row in ctl.get("rows",[]):
        for grid in ("primary","control"):
            eq.extend(row.get(grid,{}).get("equilibrated_solve_diagnostics",[]))
    if eq:
        print("STAGE_A_EQ_ROW_DYNAMIC_MAX =",max(q["row_max_dynamic_range"] for q in eq))
        print("STAGE_A_EQ_COLUMN_DYNAMIC_MAX =",max(q["column_scale_dynamic_range"] for q in eq))
        print("STAGE_A_EQ_INITIAL_UNSCALED_RES_MAX =",max(q["initial_unscaled_relative_L2_max"] for q in eq))
        print("STAGE_A_EQ_FINAL_UNSCALED_RES_MAX =",max(q["final_unscaled_relative_L2_max"] for q in eq))
        print("STAGE_A_EQ_REFINEMENT_STEPS_MAX =",max(q["accepted_refinement_steps"] for q in eq))

if "source_spatial_convergence" in d:
    print("SOURCE_SPATIAL_MAX =",d["source_spatial_convergence"]["relative_L2_max"])
if "primary_solve_controls" in d:
    z=d["primary_solve_controls"]
    print("Z20_LINEAR_RES_MAX =",z["max_linear_system_relative_L2"])
    print("Z20_SHIFT_CONSTRAINT_MAX =",z["max_shift_constraint_relative_L2"])
    print("Z20_ANISOTROPY_CONSTRAINT_MAX =",z["max_anisotropy_constraint_relative_L2"])
    eq=[]
    for row in z.get("rows",[]):
        eq.extend(row.get("equilibrated_solve_diagnostics",[]))
    if eq:
        print("Z20_EQ_FINAL_UNSCALED_RES_MAX =",max(q["final_unscaled_relative_L2_max"] for q in eq))
if "time_grid_control" in d:
    print("Z20_TIME_GRID_MAX =",d["time_grid_control"]["state_relative_L2_max"])

print("GATES =",d.get("gates"))
print("PROJECT_BOUNDARY =",d.get("project_boundary"))

for fn in [
    "results/ge19_repair05_window_retarded_reduced_h3_z20_particular.json",
    "results/ge19_repair05_window_retarded_reduced_h3_z20_particular.npz",
    "results/ge19_repair05_window_retarded_reduced_h3_z20_particular_FULL.log",
]:
    q=Path(fn)
    if q.exists():
        print("SHA256",fn,hashlib.sha256(q.read_bytes()).hexdigest(),"BYTES",q.stat().st_size)
PY
fi

echo "GE19_REPAIR05_EXIT=$RC"
exit "$RC"
