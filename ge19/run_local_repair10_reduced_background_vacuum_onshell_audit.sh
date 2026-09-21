#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results

echo "=== GE19 Repair10 lock audit ==="

test "$(git rev-parse HEAD:docs/ge19_repair08_shift_localization_result_freeze.md)" = "9f2661fee8eb6a0efad805644ecdf370b0fb60ba"
test "$(git rev-parse HEAD:docs/ge19_repair09_constraint_partition_result_freeze.md)" = "b8fc626881cdd57624b8afff01b3d88338e61715"
test "$(git rev-parse HEAD:ge19/repair10_predata_reduced_background_vacuum_onshell_audit.json)" = "fc7759463c5c84667872971e763b91824298fbc3"
test "$(git rev-parse HEAD:ge19/repair10_reduced_background_vacuum_onshell_audit.py)" = "2487b809a55bc8a3d87c5add89fe4eb6372f88c6"
test "$(git rev-parse HEAD:.github/workflows/ge19-repair10-prelock-audit.yml)" = "15b08d663dd75537c416ada8bd9d131a8d90f269"
test "$(git rev-parse HEAD:docs/ge19_repair10_reduced_background_vacuum_onshell_audit_lock.md)" = "0407589672aa958613d626e64a94e3121adfa7ed"

for sha in   f08f3d076e58240766afa21df5df6b927146d67c   c0d0fe65e63eeaabcbe0ddd2a49e336089fe2097   2b87fcfe87a7b40455ca64b0f824c66fb4fc63fa   9be665966061f0673e6f4a8e1761d1d14b4f2857   371e30a88d62b6d799197695be99c3e8d1eed581   7e9408f22fd38a0c8ba61965ca5c98af041dbacc
do
  git merge-base --is-ancestor "$sha" HEAD
done

echo "GE19_REPAIR10_LOCK_PASS"

if [[ -z "${VIRTUAL_ENV:-}" ]]; then
  echo "GE19_REPAIR10_VENV_NOT_ACTIVE"
  echo "Run: source .venv/bin/activate"
  exit 5
fi

python3 - <<'PY'
import numpy, scipy, sympy
print("GE19_REPAIR10_PYTHON_ENV_PASS")
print("NUMPY =",numpy.__version__)
print("SCIPY =",scipy.__version__)
print("SYMPY =",sympy.__version__)
PY

python3 -m py_compile ge19/repair10_reduced_background_vacuum_onshell_audit.py

echo "=== GE19 Repair10 required frozen local inputs ==="
for f in   results/ge15_R1_dense_accepted_step_trace.dat   results/ge15_R1_cli_background.dat   results/ge15_cancellation_free_s_state_precision_closure.json   results/ge19_repair08_shift_constraint_localization_audit.json
do
  test -s "$f" || { echo "MISSING=$f"; exit 4; }
done

test "$(sha256sum results/ge19_repair08_shift_constraint_localization_audit.json | awk '{print $1}')" =   "8402a9f3ede227ca4c0c762976c8de247dd07161b41f504c438c6f248361d7d0"

echo "GE19_REPAIR10_LOCAL_INPUTS_PRESENT"

rm -f   results/ge19_repair10_reduced_background_vacuum_onshell_audit.json   results/ge19_repair10_reduced_background_vacuum_onshell_audit_FULL.log

echo "=== GE19 Repair10 diagnostic execution ==="
python3 ge19/repair10_reduced_background_vacuum_onshell_audit.py   --results-dir results   --json-out results/ge19_repair10_reduced_background_vacuum_onshell_audit.json   2>&1 | tee results/ge19_repair10_reduced_background_vacuum_onshell_audit_FULL.log

echo "=== GE19 Repair10 summary ==="
python3 - <<'PY'
import hashlib,json
from pathlib import Path

p=Path("results/ge19_repair10_reduced_background_vacuum_onshell_audit.json")
d=json.loads(p.read_text())

print("CLASSIFICATION =",d["classification"])
print("FULL_DENSITY_CLOSURE =",d["full_known_background_closure"]["density_required_vs_rho_std_plus_lambda_global_relative_L2"])
print("FULL_PRESSURE_CLOSURE =",d["full_known_background_closure"]["pressure_required_vs_p_std_minus_lambda_global_relative_L2"])
print("GLOBAL_LAMBDA_IMPROVEMENT =",d["global_lambda_improvement"])
print("CONTROLS =",d["controls"])
print("ROUTING =",d["routing"])
print("H_TRACE_VS_BG =",d["independent_diagnostics"]["dense_trace_H_vs_CLASS_background_H_global_relative_L2"])
print("AEST_DENSITY_VS_CLASS =",d["independent_diagnostics"]["stable_AeST_density_vs_CLASS_cdm_slot_global_relative_L2"])
print("ACTION_PRESSURE_VS_CLASS =",d["independent_diagnostics"]["action_required_pressure_vs_CLASS_p_tot_minus_stable_AeST_pressure_global_relative_L2"])

for tag,q in d["per_C"].items():
    print("CASE",tag)
    print("  DENSITY =",q["density"])
    print("  PRESSURE =",q["pressure"])
    print("  DUST_VS_STD_DENSITY =",q["dust_vs_full_standard_density_relative_L2"])
    print("  DUST_PLUS_LAMBDA_VS_FULL =",q["dust_plus_lambda_vs_full_known_density_relative_L2"])
    print("  MINUS_LAMBDA_VS_FULL_PRESSURE =",q["minus_lambda_vs_full_known_pressure_relative_L2"])

for fn in [
  "results/ge19_repair10_reduced_background_vacuum_onshell_audit.json",
  "results/ge19_repair10_reduced_background_vacuum_onshell_audit_FULL.log",
]:
    q=Path(fn)
    print("SHA256",fn,hashlib.sha256(q.read_bytes()).hexdigest(),"BYTES",q.stat().st_size)
PY

echo "GE19_REPAIR10_DIAGNOSTIC_COMPLETE"
