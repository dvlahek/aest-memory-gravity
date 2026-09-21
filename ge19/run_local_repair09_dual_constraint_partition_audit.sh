#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results

echo "=== GE19 Repair09 lock audit ==="

test "$(git rev-parse HEAD:docs/ge19_repair08_shift_localization_result_freeze.md)" = "9f2661fee8eb6a0efad805644ecdf370b0fb60ba"
test "$(git rev-parse HEAD:ge19/repair09_predata_dual_constraint_partition_audit.json)" = "9716f45898959bfec49128195035a2c61327b041"
test "$(git rev-parse HEAD:ge19/repair09_dual_constraint_partition_audit.py)" = "b07572411b14266f40cdc849174bd01e31771f0e"
test "$(git rev-parse HEAD:.github/workflows/ge19-repair09-prelock-audit.yml)" = "b69a21546a87671d119b9f0910635ca253993255"
test "$(git rev-parse HEAD:docs/ge19_repair09_dual_constraint_partition_audit_lock.md)" = "f9552436ed9dc1a50cca2bdbb846da84f2974bea"

for sha in   f08f3d076e58240766afa21df5df6b927146d67c   d4d280748ff5f6140833ed876c484f7a6497d550   d5312a74be737646739a0220c0414c44551f3577   fa4c2576730e0fcb3e82c1407deaf2764f556e19   1224c1bd58adf4ff510ec8ce49982ab55b6456b3
do
  git merge-base --is-ancestor "$sha" HEAD
done

echo "GE19_REPAIR09_LOCK_PASS"

if [[ -z "${VIRTUAL_ENV:-}" ]]; then
  echo "GE19_REPAIR09_VENV_NOT_ACTIVE"
  echo "Run: source .venv/bin/activate"
  exit 5
fi

python3 - <<'PY'
import numpy, scipy, sympy
print("GE19_REPAIR09_PYTHON_ENV_PASS")
print("NUMPY =",numpy.__version__)
print("SCIPY =",scipy.__version__)
print("SYMPY =",sympy.__version__)
PY

python3 -m py_compile ge19/repair09_dual_constraint_partition_audit.py

echo "=== GE19 Repair09 required frozen local inputs ==="
for f in   results/ge15_R1_dense_accepted_step_trace.dat   results/ge15_cancellation_free_s_state_precision_closure.json   results/ge18_repair01_on_shell_matched_dust_first_order_bridge.json   results/ge18_repair01_on_shell_matched_dust_first_order_bridge.npz   results/ge19_repair08_shift_constraint_localization_audit.json
do
  test -s "$f" || { echo "MISSING=$f"; exit 4; }
done

test "$(sha256sum results/ge19_repair08_shift_constraint_localization_audit.json | awk '{print $1}')" =   "8402a9f3ede227ca4c0c762976c8de247dd07161b41f504c438c6f248361d7d0"

echo "GE19_REPAIR09_LOCAL_INPUTS_PRESENT"

rm -f   results/ge19_repair09_dual_constraint_partition_audit.json   results/ge19_repair09_dual_constraint_partition_audit_FULL.log

echo "=== GE19 Repair09 diagnostic execution ==="
python3 ge19/repair09_dual_constraint_partition_audit.py   --results-dir results   --json-out results/ge19_repair09_dual_constraint_partition_audit.json   2>&1 | tee results/ge19_repair09_dual_constraint_partition_audit_FULL.log

echo "=== GE19 Repair09 summary ==="
python3 - <<'PY'
import hashlib,json
from pathlib import Path

p=Path("results/ge19_repair09_dual_constraint_partition_audit.json")
d=json.loads(p.read_text())
g=d["global"]
r=d["routing"]

print("CLASSIFICATION =",d["classification"])
print("LINEAR_RESIDUAL_MAX =",g["linear_system_relative_L2_max"])
print("SHIFT_BACKWARD_ERROR_MAX =",g["shift_constraint_backward_error_max"])
print("ANISOTROPY_BACKWARD_ERROR_MAX =",g["anisotropy_constraint_backward_error_max"])
print("INITIAL_MATCH_MAX =",g["initial_dynamic_match_abs_or_rel_max"])
print("TIME_64_32_MAX =",g["primary64_vs_control32_state_global_relative_L2_max"])
print("ALL_OUTPUTS_FINITE =",g["all_outputs_finite"])
print("NUMERICAL_CONTROLS_HEALTHY =",r["numerical_controls_healthy"])
print("NEXT_ROUTE =",r["next_route"])
print("HISTORICAL_REPAIR07_SHIFT_MAX =",d["historical_repair07_shift_max"])

for row in d["rows"]:
    for grid in ("primary","control"):
        q=row[grid]
        diags=q.get("canonical_march_diagnostics",[])
        cond=max((x.get("local_algebraic_scaled_condition_2_max",0.0) for x in diags),default=0.0)
        rad=max((x.get("radau_scaled_condition_2_max",0.0) for x in diags),default=0.0)
        lapse=max((x.get("lapse_noether_row_relative_residual_max",0.0) for x in diags),default=0.0)
        print(
            "CASE",row["C"],grid,
            "linear=",q["linear_system_relative_L2_max"],
            "shift=",q["shift_constraint_relative_L2_max"],
            "aniso=",q["anisotropy_constraint_relative_L2_max"],
            "init=",q["initial_dynamic_match_abs_or_rel_max"],
            "local_cond_max=",cond,
            "radau_cond_max=",rad,
            "lapse_max=",lapse,
        )

for q in d["time_control"]:
    print("TIME_CASE",q["C"],"max=",q["max"])

for fn in [
  "results/ge19_repair09_dual_constraint_partition_audit.json",
  "results/ge19_repair09_dual_constraint_partition_audit_FULL.log",
]:
    q=Path(fn)
    print("SHA256",fn,hashlib.sha256(q.read_bytes()).hexdigest(),"BYTES",q.stat().st_size)
PY

echo "GE19_REPAIR09_DIAGNOSTIC_COMPLETE"
