#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results

echo "=== GE19 Repair11 lock audit ==="

test "$(git rev-parse HEAD:docs/ge19_repair10_reduced_background_vacuum_onshell_result_freeze.md)" = "b24435a4c6233ab383a544a0bf231fa0e6db9c19"
test "$(git rev-parse HEAD:ge19/repair11_predata_lambda_inclusive_reduced_h1_reclosure.json)" = "1487b99fa3ab403134fe19a073d35c32279ea813"
test "$(git rev-parse HEAD:ge19/repair11_lambda_inclusive_reduced_h1_reclosure.py)" = "dbfa43ae11dbd3cfeeb1994a30237e9374dbb3e7"
test "$(git rev-parse HEAD:.github/workflows/ge19-repair11-prelock-audit.yml)" = "ffb633e67eda142cf1dce882d65dfeb1baaa62e5"
test "$(git rev-parse HEAD:docs/ge19_repair11_lambda_h1_implementation_lock.md)" = "d0f03ee535b5c9f288253340ea3e8b5a7c9f7b3c"

test "$(git rev-parse HEAD:ge06/analytic_aest_directional_source_generator.py)" = "a7afe0035054a9dca55d74a6497c081422114b4c"
test "$(git rev-parse HEAD:ge07/pressureless_matter_directional_source_generator.py)" = "cde8da77a80799cef00fc7c09c3633310fc9e3d4"
test "$(git rev-parse HEAD:ge09/repair01_dense_accepted_step_local_jet_bridge.py)" = "509fa9d7bb323034bbf77b26792f35e1cc2ff7c7"

for sha in   b66e780b9d3b5f119ef4deafa0cd2e82d5333580   6eee56fb6764926117d1a0b93705d4ba3acc617d   03b428155f06ed7764ca520acb80fd1d63e13d95   60f99e4f92acd1e718440e9edc5e36e1977bc33a   083df54525d93ad595ff6cf6d1805b72ed4a1884
do
  git merge-base --is-ancestor "$sha" HEAD
done

echo "GE19_REPAIR11_LOCK_PASS"

echo "=== GE19 Repair11 Python environment ==="
if [[ -z "${VIRTUAL_ENV:-}" ]]; then
  echo "GE19_REPAIR11_VENV_NOT_ACTIVE"
  echo "Run: source .venv/bin/activate"
  exit 5
fi

python3 - <<'PY'
import numpy, scipy, sympy
print("GE19_REPAIR11_PYTHON_ENV_PASS")
print("NUMPY =",numpy.__version__)
print("SCIPY =",scipy.__version__)
print("SYMPY =",sympy.__version__)
PY

python3 -m py_compile ge19/repair11_lambda_inclusive_reduced_h1_reclosure.py

echo "=== GE19 Repair11 required frozen local inputs ==="
for f in   results/ge15_R1_dense_accepted_step_trace.dat   results/ge15_R1_cli_background.dat   results/ge15_cancellation_free_s_state_precision_closure.json   results/ge15_cancellation_free_s_state_precision_closure.npz   results/ge18_repair01_on_shell_matched_dust_first_order_bridge.json   results/ge18_repair01_on_shell_matched_dust_first_order_bridge.npz   results/ge19_repair10_reduced_background_vacuum_onshell_audit.json
do
  test -s "$f" || { echo "MISSING=$f"; exit 4; }
done

test "$(sha256sum results/ge19_repair10_reduced_background_vacuum_onshell_audit.json | awk '{print $1}')" =   "0903363695f071e635f91875903893041bfe728d9ff6c85b424604b933c8baa5"

echo "GE19_REPAIR11_LOCAL_INPUTS_PRESENT"

echo "=== GE19 Repair11 local Lambda matrix self-audit ==="
python3 - <<'PY'
import importlib.util
from pathlib import Path
import numpy as np

p=Path("ge19/repair11_lambda_inclusive_reduced_h1_reclosure.py").resolve()
spec=importlib.util.spec_from_file_location("r11local",p)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

a=0.6
rho=3.451969239349119e-8
C=m.lambda_c1_matrix(a,rho)
assert C.shape==(16,10)
assert np.isclose(C[4,2],-18*rho*a*a,rtol=0,atol=1e-30)
assert np.isclose(C[6,0],-18*rho*a*a,rtol=0,atol=1e-30)
assert np.isclose(C[6,2],-36*rho*a,rtol=0,atol=1e-30)
mask=np.ones_like(C,dtype=bool)
mask[4,2]=False
mask[6,0]=False
mask[6,2]=False
assert np.max(np.abs(C[mask]))==0.0
print("GE19_REPAIR11_LOCAL_LAMBDA_MATRIX_SELF_AUDIT_PASS")
PY

rm -f   results/ge19_repair11_lambda_inclusive_reduced_h1_reclosure.json   results/ge19_repair11_lambda_inclusive_reduced_h1_reclosure.npz   results/ge19_repair11_lambda_inclusive_reduced_h1_reclosure_FULL.log

echo "=== GE19 Repair11 Stage-A science execution ==="
set +e
python3 ge19/repair11_lambda_inclusive_reduced_h1_reclosure.py   --results-dir results   --json-out results/ge19_repair11_lambda_inclusive_reduced_h1_reclosure.json   --npz-out results/ge19_repair11_lambda_inclusive_reduced_h1_reclosure.npz   2>&1 | tee results/ge19_repair11_lambda_inclusive_reduced_h1_reclosure_FULL.log
RC=${PIPESTATUS[0]}
set -e

echo "=== GE19 Repair11 summary ==="
if test -s results/ge19_repair11_lambda_inclusive_reduced_h1_reclosure.json; then
python3 - <<'PY'
import hashlib,json
from pathlib import Path

p=Path("results/ge19_repair11_lambda_inclusive_reduced_h1_reclosure.json")
d=json.loads(p.read_text())
c=d["controls"]

print("CLASSIFICATION =",d["classification"])
print("STAGE =",d["stage"])
print("STAGE_A_PASS =",d["stage_A_pass"])
print("LINEAR_RESIDUAL_MAX =",c["max_linear_system_relative_L2"])
print("SHIFT_BACKWARD_ERROR_MAX =",c["max_shift_constraint_relative_L2"])
print("ANISOTROPY_BACKWARD_ERROR_MAX =",c["max_anisotropy_constraint_relative_L2"])
print("INITIAL_MATCH_MAX =",c["max_initial_dynamic_match_abs_or_rel"])
print("TIME_64_32_MAX =",c["primary64_vs_control32_state_global_relative_L2_max"])
print("ALL_OUTPUTS_FINITE =",c["all_outputs_finite"])
print("GATES =",d["gates"])
print("LAMBDA_SUMMARY =",d["lambda_first_directional_matrix_summary"])
print("Z20_CONSTRUCTED =",d["Z20_constructed"])
print("NEXT_STEP =",d["next_step"])
print("CLAIM_BOUNDARY =",d["claim_boundary"])

for row in c["rows"]:
    print("CASE",row["C"])
    for grid in ("primary","control"):
        q=row[grid]
        print(
            " ",grid,
            "linear=",q["linear_system_relative_L2_max"],
            "shift=",q["shift_constraint_relative_L2_max"],
            "aniso=",q["anisotropy_constraint_relative_L2_max"],
            "init=",q["initial_dynamic_match_abs_or_rel_max"],
        )

for q in c["time_control"]:
    print("TIME_CASE",q["C"],"max=",q["max"])

for fn in [
  "results/ge19_repair11_lambda_inclusive_reduced_h1_reclosure.json",
  "results/ge19_repair11_lambda_inclusive_reduced_h1_reclosure.npz",
  "results/ge19_repair11_lambda_inclusive_reduced_h1_reclosure_FULL.log",
]:
    q=Path(fn)
    if q.exists():
        print("SHA256",fn,hashlib.sha256(q.read_bytes()).hexdigest(),"BYTES",q.stat().st_size)
PY
fi

echo "GE19_REPAIR11_EXIT=$RC"
exit "$RC"
