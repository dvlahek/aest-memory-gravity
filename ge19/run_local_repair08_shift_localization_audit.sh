#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results

echo "=== GE19 Repair08 lock audit ==="

test "$(git rev-parse HEAD:docs/ge19_repair07_reduced_h1_result_freeze.md)" = "8146ba26f0d147ba62315faaf5fb03156564d738"
test "$(git rev-parse HEAD:ge19/repair08_predata_shift_constraint_localization_audit.json)" = "7f584923203d371c344d9d6825a2f925069f6a28"
test "$(git rev-parse HEAD:ge19/repair08_shift_constraint_localization_audit.py)" = "6bf737ff455e54295dc099df933b99e1f1a64141"
test "$(git rev-parse HEAD:.github/workflows/ge19-repair08-prelock-audit.yml)" = "2b8a83fa17fdc1018dd1fb8105e151fa6c500705"
test "$(git rev-parse HEAD:docs/ge19_repair08_shift_localization_audit_lock.md)" = "f5876c75d300d5785583effe91183b4dddb2762f"

for sha in   8295046a26979b4045a39b8010f892d100d7a7c5   30b2672dd26ae164cd5a3363c5f12f5936e4545a   9c481e42f09e810afbf551ee8a8450c05da581fd   b2d1662cb82cca8baec173dc4089fa5b9a53db87   101984d78445318c2df75b795e23290d4a5f0f88
do
  git merge-base --is-ancestor "$sha" HEAD
done

echo "GE19_REPAIR08_LOCK_PASS"

if [[ -z "${VIRTUAL_ENV:-}" ]]; then
  echo "GE19_REPAIR08_VENV_NOT_ACTIVE"
  echo "Run: source .venv/bin/activate"
  exit 5
fi

python3 - <<'PY'
import numpy, scipy, sympy
print("GE19_REPAIR08_PYTHON_ENV_PASS")
print("NUMPY =",numpy.__version__)
print("SCIPY =",scipy.__version__)
print("SYMPY =",sympy.__version__)
PY

python3 -m py_compile ge19/repair08_shift_constraint_localization_audit.py

echo "=== GE19 Repair08 required frozen local inputs ==="
for f in   results/ge15_R1_dense_accepted_step_trace.dat   results/ge15_cancellation_free_s_state_precision_closure.json   results/ge15_cancellation_free_s_state_precision_closure.npz   results/ge15_R1_cli_background.dat   results/ge18_repair01_on_shell_matched_dust_first_order_bridge.json   results/ge18_repair01_on_shell_matched_dust_first_order_bridge.npz   results/ge19_repair07_window_retarded_reduced_h3_z20_particular.json   results/ge15_R1_cli_perturbations_k0_s.dat   results/ge15_R1_cli_perturbations_k1_s.dat   results/ge15_R1_cli_perturbations_k2_s.dat   results/ge15_R1_cli_perturbations_k3_s.dat   results/ge15_R1_cli_perturbations_k4_s.dat   results/ge15_R1_cli_perturbations_k5_s.dat
do
  test -s "$f" || { echo "MISSING=$f"; exit 4; }
done

test "$(sha256sum results/ge19_repair07_window_retarded_reduced_h3_z20_particular.json | awk '{print $1}')" =   "f27d31b637332bd043ebabdcc47a18e1126f05065aea2cca794ac8e0f2b2e894"

echo "GE19_REPAIR08_LOCAL_INPUTS_PRESENT"

rm -f   results/ge19_repair08_shift_constraint_localization_audit.json   results/ge19_repair08_shift_constraint_localization_audit_FULL.log

echo "=== GE19 Repair08 diagnostic execution ==="
python3 ge19/repair08_shift_constraint_localization_audit.py   --results-dir results   --json-out results/ge19_repair08_shift_constraint_localization_audit.json   2>&1 | tee results/ge19_repair08_shift_constraint_localization_audit_FULL.log

echo "=== GE19 Repair08 summary ==="
python3 - <<'PY'
import hashlib,json
from pathlib import Path

p=Path("results/ge19_repair08_shift_constraint_localization_audit.json")
d=json.loads(p.read_text())
g=d["global"]
r=d["routing"]

print("CLASSIFICATION =",d["classification"])
print("INITIAL_SHIFT_BACKWARD_ERROR_MAX =",g["initial_prescribed_shift_backward_error_max"])
print("REDUCED_REFERENCE_SHIFT_BACKWARD_ERROR_MAX =",g["mixed_reference_reduced_dust_shift_backward_error_max"])
print("CANONICAL_REPAIR07_SHIFT_BACKWARD_ERROR_MAX =",g["canonical_repair07_shift_backward_error_max"])
print("FULL_STANDARD_CLASS_PAIR_METRIC_MAX =",g["full_standard_CLASS_pair_metric_max"])
print("FULL_STANDARD_CLASS_WRONG_SIGN_PAIR_METRIC_MAX =",g["full_standard_CLASS_wrong_sign_pair_metric_max"])
print("INITIAL_T_SIGN_FLIP_PAIR_METRIC_MAX =",g["initial_matter_sign_flip_pair_metric_max"])
print("INITIAL_PHI_SIGN_FLIP_PAIR_METRIC_MAX =",g["initial_aest_scalar_phi_sign_flip_pair_metric_max"])
print("MAX_INITIAL_T_SIGN_IMPROVEMENT =",g["max_initial_matter_sign_flip_improvement_factor"])
print("MAX_INITIAL_PHI_SIGN_IMPROVEMENT =",g["max_initial_phi_sign_flip_improvement_factor"])
print("ROUTING =",r)

# Print compact per-case initial/crossing information.
for q in d["per_case"]:
    print(
        "CASE",
        q["C"],
        "m=",q["m"],
        "init=",q["initial_prescribed"]["shift_backward_error"],
        "refmax=",q["mixed_reference_reduced_dust"]["max"],
        "canonmax=",q["canonical_repair07"]["max"],
        "cross=",q["canonical_first_crossing_1e6"],
        "fullmax=",q["full_standard_CLASS_pair_metric"]["max"],
        "wrongfull=",q["full_standard_CLASS_wrong_sign_pair_metric"]["max"],
    )

for fn in [
  "results/ge19_repair08_shift_constraint_localization_audit.json",
  "results/ge19_repair08_shift_constraint_localization_audit_FULL.log",
]:
    q=Path(fn)
    print("SHA256",fn,hashlib.sha256(q.read_bytes()).hexdigest(),"BYTES",q.stat().st_size)
PY

echo "GE19_REPAIR08_DIAGNOSTIC_COMPLETE"
