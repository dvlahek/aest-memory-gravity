#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results

echo "=== GE19 Repair04 lock audit ==="
test "$(git rev-parse HEAD:ge19/repair04_predata_linear_operator_Z_coordinate_and_provenance.json)" = "c16cb534db9215a057ffff93ab005f44284901ca"
test "$(git rev-parse HEAD:ge19/repair04_window_retarded_reduced_h3_z20_particular.py)" = "35a8f4b6039e435e7d658e3b5cac34fdc7737f13"
test "$(git rev-parse HEAD:docs/ge19_repair04_linear_Z_coordinate_implementation_lock.md)" = "5474e7d71a979d39564e9a743f75649ca1c275b7"
test "$(git rev-parse HEAD:.github/workflows/ge19-repair04-prelock-audit.yml)" = "8107889c62a6abbbf5847337ac21685a4edd6847"
test "$(git rev-parse HEAD:docs/ge19_repair03_reduced_h1_result_freeze.md)" = "6542c64474361c734be9c9a217a719978afd478b"

test "$(git rev-parse HEAD:ge06/analytic_aest_directional_source_generator.py)" = "a7afe0035054a9dca55d74a6497c081422114b4c"
test "$(git rev-parse HEAD:ge07/pressureless_matter_directional_source_generator.py)" = "cde8da77a80799cef00fc7c09c3633310fc9e3d4"
test "$(git rev-parse HEAD:ge09/repair01_dense_accepted_step_local_jet_bridge.py)" = "509fa9d7bb323034bbf77b26792f35e1cc2ff7c7"

git merge-base --is-ancestor 90d5131f8c835dea066aa78e0992b94af7462b5a HEAD
git merge-base --is-ancestor 3e1f2a7e66c8eac5aa220e041e8fd9279be1855e HEAD
git merge-base --is-ancestor cba58cc46fbeb83e3d69ed7887dad08cd02a9292 HEAD
git merge-base --is-ancestor 6301872b811000558303e62e7d5e6659efa5ff13 HEAD

echo "GE19_REPAIR04_LOCK_PASS"

echo "=== GE19 Repair04 required local parents ==="
for f in   results/ge15_R1_dense_accepted_step_trace.dat   results/ge15_cancellation_free_s_state_precision_closure.json   results/ge15_cancellation_free_s_state_precision_closure.npz   results/ge18_repair01_on_shell_matched_dust_first_order_bridge.json   results/ge18_repair01_on_shell_matched_dust_first_order_bridge.npz
do
  test -s "$f" || { echo "MISSING=$f"; exit 4; }
done
echo "GE19_REPAIR04_LOCAL_INPUTS_PRESENT"

python3 -m pip install numpy scipy sympy >/dev/null
python3 -m py_compile ge19/repair04_window_retarded_reduced_h3_z20_particular.py

echo "=== GE19 Repair04 mandatory local coordinate self-audit ==="
python3 - <<'PY'
import importlib.util
from pathlib import Path
from types import SimpleNamespace
import numpy as np

root=Path.cwd()
spec=importlib.util.spec_from_file_location(
    "ge19r4",
    root/"ge19/repair04_window_retarded_reduced_h3_z20_particular.py"
)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

g6=m.load_frozen_generator(
    (root/"ge06/analytic_aest_directional_source_generator.py").resolve(),
    "ge19r4_local_ge06"
)
stable=m.build_stable_ge06_generator(g6)
benign=m.ge06_stable_benign_equivalence(g6,stable)
physical=m.ge06_physical_parameter_probe(stable)

assert benign["all_stable_outputs_finite"], benign
assert benign["coeff1_source_global_relative_L2"]<=1e-10, benign
assert benign["coeff2_source_global_relative_L2"]<=1e-10, benign
assert physical["c1"]["all_partials_finite"], physical
assert physical["c2"]["all_partials_finite"], physical

for order in ("c1","c2"):
    a=stable.symbolic_exp_audit[order]
    assert a["all_exp_args_equivalent_to_Zb_squared"], a
    assert a["all_exp_args_Q0_free"], a
    assert a["all_exp_args_Z0_free"], a

g7=m.load_frozen_generator(
    (root/"ge07/pressureless_matter_directional_source_generator.py").resolve(),
    "ge19r4_local_ge07"
)

seen=[]
wrapped={}
for name,fn in stable.f_c1.items():
    def make(fn,name):
        def w(*args):
            seen.append((name,np.asarray(args[2],float).copy()))
            return fn(*args)
        return w
    wrapped[name]=make(fn,name)
proxy=SimpleNamespace(f_c1=wrapped)

nt=8
x=np.linspace(np.log(0.4),np.log(1.0/1.2),nt)
a=np.exp(x)
Z=np.linspace(4.45,4.68,nt)
Q=np.full(nt,1.0e-4)
bg={
    "x":x,
    "a":a,
    "H":np.linspace(1.4e-4,7.5e-5,nt),
    "Z_action":Z,
    "Q_action":Q,
}
Y=np.zeros((6,nt,1),complex)
Y[0,:,0]=1e-8
Y[1,:,0]=np.linspace(0,1e-8,nt)
Y[2,:,0]=2e-8
Y[3,:,0]=3e-18
Y[4,:,0]=4e-8
Y[5,:,0]=5e-12

main,con=m.linear_operator_batch(proxy,g7,bg,"C_star",0.01,Y)
assert np.all(np.isfinite(main)), "nonfinite main operator probe"
assert np.all(np.isfinite(con)), "nonfinite constraint operator probe"
assert seen, "stable c1 callbacks were not called"

for name,arg3 in seen:
    target=np.broadcast_to(Z[:,None],arg3.shape)
    wrong=np.broadcast_to(Q[:,None],arg3.shape)
    assert np.array_equal(arg3,target), (name,arg3,target)
    assert not np.array_equal(arg3,wrong), name

print("GE19_REPAIR04_COORDINATE_SELF_AUDIT_PASS")
print("BENIGN_EQUIVALENCE =",benign)
print("PHYSICAL_PARAMETER_PROBE =",physical)
print("LINEAR_COORDINATE_CALLS =",len(seen))
print("LINEAR_COORDINATE_Z_MINMAX =",float(min(v.min() for _,v in seen)),float(max(v.max() for _,v in seen)))
print("LINEAR_OPERATOR_PROBE_MAIN_NORM =",float(np.linalg.norm(main)))
print("LINEAR_OPERATOR_PROBE_CONSTRAINT_NORM =",float(np.linalg.norm(con)))
PY

rm -f   results/ge19_repair04_window_retarded_reduced_h3_z20_particular.json   results/ge19_repair04_window_retarded_reduced_h3_z20_particular.npz   results/ge19_repair04_window_retarded_reduced_h3_z20_particular_FULL.log

echo "=== GE19 Repair04 science execution ==="
set +e
python3 ge19/repair04_window_retarded_reduced_h3_z20_particular.py   --results-dir results   --json-out results/ge19_repair04_window_retarded_reduced_h3_z20_particular.json   --npz-out results/ge19_repair04_window_retarded_reduced_h3_z20_particular.npz   2>&1 | tee results/ge19_repair04_window_retarded_reduced_h3_z20_particular_FULL.log
RC=${PIPESTATUS[0]}
set -e

echo "=== GE19 Repair04 summary ==="
if test -s results/ge19_repair04_window_retarded_reduced_h3_z20_particular.json; then
python3 - <<'PY'
import hashlib, json
from pathlib import Path

p=Path("results/ge19_repair04_window_retarded_reduced_h3_z20_particular.json")
d=json.loads(p.read_text())

print("CLASSIFICATION =",d.get("classification"))
print("FAILURE_STAGE =",d.get("failure_stage"))

prov=d.get("provenance",{})
print("ACTIVE_LINEAR_GE06_COORDINATE =",prov.get("active_linear_GE06_background_coordinate"))
print("BACKGROUND_MODE_MISMATCH =",prov.get("GE15_background_mode_mismatch_max"))
print("BACKGROUND_MODE_MISMATCH_STATUS =",prov.get("GE15_background_mode_mismatch_gate_status"))
print("STABLE_GE06_SYMBOLIC_EXP_AUDIT =",prov.get("stable_GE06_symbolic_exp_audit"))
print("STABLE_GE06_PHYSICAL_PARAMETER_PROBE =",prov.get("stable_GE06_physical_parameter_probe"))

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
    "results/ge19_repair04_window_retarded_reduced_h3_z20_particular.json",
    "results/ge19_repair04_window_retarded_reduced_h3_z20_particular.npz",
    "results/ge19_repair04_window_retarded_reduced_h3_z20_particular_FULL.log",
]:
    q=Path(fn)
    if q.exists():
        print("SHA256",fn,hashlib.sha256(q.read_bytes()).hexdigest(),"BYTES",q.stat().st_size)
PY
fi

echo "GE19_REPAIR04_EXIT=$RC"
exit "$RC"
