#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results

echo "=== GE19 Repair13 lock audit ==="

test "$(git rev-parse HEAD:docs/ge19_repair12_standard_momentum_result_freeze.md)" = "7705cd781a7eed33d0c1a07354c97faebc624620"
test "$(git rev-parse HEAD:ge19/repair13_predata_self_consistent_reduced_background_h1_reclosure.json)" = "8e960e80da0b1acee3b1724169f222a4edc7bf1b"
test "$(git rev-parse HEAD:ge19/repair13_self_consistent_reduced_background_h1_reclosure.py)" = "362d63d03d7b850fceae393f535353ded79aeea7"
test "$(git rev-parse HEAD:.github/workflows/ge19-repair13-prelock-audit.yml)" = "edac57861eb719638b37516326c5cca56d02ecd4"
test "$(git rev-parse HEAD:docs/ge19_repair13_reduced_background_h1_implementation_lock.md)" = "168d4fcd6331c04d0c587c587eac909a623dfa0e"

test "$(git rev-parse HEAD:ge06/analytic_aest_directional_source_generator.py)" = "a7afe0035054a9dca55d74a6497c081422114b4c"
test "$(git rev-parse HEAD:ge07/pressureless_matter_directional_source_generator.py)" = "cde8da77a80799cef00fc7c09c3633310fc9e3d4"
test "$(git rev-parse HEAD:ge09/repair01_dense_accepted_step_local_jet_bridge.py)" = "509fa9d7bb323034bbf77b26792f35e1cc2ff7c7"

for sha in   8d27fe6cba7ce3e00f8b6714a22dc9d47de24c6a   3a7e6931c4ba18cfe7c5da7221c9b98cb09d6b2f   b4e0fa9a051f28ab8c8413e9b49485d06f740bc5   3821700aabc190a0305028509ad1a4ac8f369bd9   827bd069e0938d13c460b56125143297bc3a627a
do
  git merge-base --is-ancestor "$sha" HEAD
done

echo "GE19_REPAIR13_LOCK_PASS"

if [[ -z "${VIRTUAL_ENV:-}" ]]; then
  echo "GE19_REPAIR13_VENV_NOT_ACTIVE"
  echo "Run: source .venv/bin/activate"
  exit 5
fi

python3 - <<'PY'
import numpy, scipy, sympy
print("GE19_REPAIR13_PYTHON_ENV_PASS")
print("NUMPY =",numpy.__version__)
print("SCIPY =",scipy.__version__)
print("SYMPY =",sympy.__version__)
PY

python3 -m py_compile ge19/repair13_self_consistent_reduced_background_h1_reclosure.py

echo "=== GE19 Repair13 required frozen local inputs ==="
for f in   results/ge15_R1_dense_accepted_step_trace.dat   results/ge15_R1_cli_background.dat   results/ge15_cancellation_free_s_state_precision_closure.json   results/ge18_repair01_on_shell_matched_dust_first_order_bridge.json   results/ge18_repair01_on_shell_matched_dust_first_order_bridge.npz   results/ge19_repair12_remaining_standard_momentum_audit.json
do
  test -s "$f" || { echo "MISSING=$f"; exit 4; }
done

test "$(sha256sum results/ge19_repair12_remaining_standard_momentum_audit.json | awk '{print $1}')" =   "e442e37dab7df97f890cc2b210d34446a204437650226f82a4887e1e2d0dc270"

echo "GE19_REPAIR13_LOCAL_INPUTS_PRESENT"

rm -f   results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.json   results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz   results/ge19_repair13_self_consistent_reduced_background_h1_reclosure_FULL.log

echo "=== GE19 Repair13 Stage-A science execution ==="
set +e
python3 ge19/repair13_self_consistent_reduced_background_h1_reclosure.py   --results-dir results   --json-out results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.json   --npz-out results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz   2>&1 | tee results/ge19_repair13_self_consistent_reduced_background_h1_reclosure_FULL.log
RC=${PIPESTATUS[0]}
set -e

echo "=== GE19 Repair13 summary ==="
if test -s results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.json; then
python3 - <<'PY'
import hashlib,json
from pathlib import Path

p=Path("results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.json")
d=json.loads(p.read_text())
b=d["background_controls"]
s=d["stage_A_controls"]

print("CLASSIFICATION =",d["classification"])
print("STAGE_A_PASS =",d["stage_A_pass"])
print("BACKGROUND_FRIEDMANN_MAX =",b["friedmann_relative_L2_max"])
print("BACKGROUND_PRESSURE_IDENTITY_MAX =",b["pressure_identity_relative_L2_max"])
print("BACKGROUND_GATES =",b["gates"])
print("LINEAR_RESIDUAL_MAX =",s["max_linear_system_relative_L2"])
print("SHIFT_BACKWARD_ERROR_MAX =",s["max_shift_constraint_relative_L2"])
print("ANISOTROPY_BACKWARD_ERROR_MAX =",s["max_anisotropy_constraint_relative_L2"])
print("INITIAL_MATCH_MAX =",s["max_initial_dynamic_match_abs_or_rel"])
print("TIME_64_32_MAX =",s["primary64_vs_control32_state_global_relative_L2_max"])
print("ALL_OUTPUTS_FINITE =",s["all_outputs_finite"])
print("STAGE_A_GATES =",s["gates"])
print("Z20_CONSTRUCTED =",d["Z20_constructed"])
print("NEXT_STEP =",d["next_step"])

for q in b["rows"]:
    print(
      "BACKGROUND_CASE",q["C"],
      "Hdiff_primary=",q["primary"]["H_red_vs_CLASS_full_global_relative_L2"],
      "Hdiff_control=",q["control"]["H_red_vs_CLASS_full_global_relative_L2"],
      "fried_primary=",q["primary"]["friedmann_relative_L2"],
      "pressure_primary=",q["primary"]["pressure_identity_relative_L2"],
    )

for row in s["rows"]:
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

for q in s["time_control"]:
    print("TIME_CASE",q["C"],"max=",q["max"])

for fn in [
  "results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.json",
  "results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz",
  "results/ge19_repair13_self_consistent_reduced_background_h1_reclosure_FULL.log",
]:
    q=Path(fn)
    if q.exists():
        print("SHA256",fn,hashlib.sha256(q.read_bytes()).hexdigest(),"BYTES",q.stat().st_size)
PY
fi

echo "GE19_REPAIR13_EXIT=$RC"
exit "$RC"
