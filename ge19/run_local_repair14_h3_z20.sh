#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results

echo "=== GE19 Repair14 lock audit ==="

test "$(git rev-parse HEAD:docs/ge19_repair13_reduced_background_h1_result_freeze.md)" = "06530bf2df460c27c48e4fca4bd6e089dd839137"
test "$(git rev-parse HEAD:ge19/repair14_predata_self_consistent_reduced_h3_z20_particular.json)" = "abf5b794ac4d53c2098bf596247f996cb07fa6c2"
test "$(git rev-parse HEAD:ge19/repair14_self_consistent_reduced_h3_z20_particular.py)" = "06c5ced952c2370cfa4aaadb6ef8f72d2d7221de"
test "$(git rev-parse HEAD:.github/workflows/ge19-repair14-prelock-audit.yml)" = "70ca950c5ead671be8e62f681bc43a0ddaae6cd6"
test "$(git rev-parse HEAD:docs/ge19_repair14_h3_z20_implementation_lock.md)" = "22cd11c51e0059b6fbcb2593fc127615beef5c4e"

for sha in   5461f89f77f91e931f14abb6a2e5014597e0cb6f   83faed57a2f49a30a1a0010995e1966cc49aebb6   5a969ff0dc00b8683fe239733ae25c935c2b8f70   3ad4572442bf0a08d465ed63111b8d59cfcc133a   aeb7b4d9b1317aae1e93f5bd0c2e04e1e079e866
do
  git merge-base --is-ancestor "$sha" HEAD
done

echo "GE19_REPAIR14_LOCK_PASS"

if [[ -z "${VIRTUAL_ENV:-}" ]]; then
  echo "GE19_REPAIR14_VENV_NOT_ACTIVE"
  echo "Run: source .venv/bin/activate"
  exit 5
fi

python3 - <<'PY'
import numpy, scipy, sympy
print("GE19_REPAIR14_PYTHON_ENV_PASS")
print("NUMPY =",numpy.__version__)
print("SCIPY =",scipy.__version__)
print("SYMPY =",sympy.__version__)
PY

python3 -m py_compile ge19/repair14_self_consistent_reduced_h3_z20_particular.py

echo "=== GE19 Repair14 required frozen local inputs ==="
for f in   results/ge15_R1_dense_accepted_step_trace.dat   results/ge15_R1_cli_background.dat   results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.json   results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz
do
  test -s "$f" || { echo "MISSING=$f"; exit 4; }
done

test "$(sha256sum results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.json | awk '{print $1}')" =   "ae3cc790ecffbd5498b5852273c72ae578d4615de29bbb616673c05cdb3e74b7"
test "$(sha256sum results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz | awk '{print $1}')" =   "011c0ae54fd21d70c0e2c695ce62e7b74a3c5529a07c9023c882a447d5b40ca3"

echo "GE19_REPAIR14_LOCAL_INPUTS_PRESENT"

rm -f   results/ge19_repair14_self_consistent_reduced_h3_z20_particular.json   results/ge19_repair14_self_consistent_reduced_h3_z20_particular.npz   results/ge19_repair14_self_consistent_reduced_h3_z20_particular_FULL.log

echo "=== GE19 Repair14 H3/Z20 science execution ==="
set +e
python3 ge19/repair14_self_consistent_reduced_h3_z20_particular.py   --results-dir results   --json-out results/ge19_repair14_self_consistent_reduced_h3_z20_particular.json   --npz-out results/ge19_repair14_self_consistent_reduced_h3_z20_particular.npz   2>&1 | tee results/ge19_repair14_self_consistent_reduced_h3_z20_particular_FULL.log
RC=${PIPESTATUS[0]}
set -e

echo "=== GE19 Repair14 summary ==="
if test -s results/ge19_repair14_self_consistent_reduced_h3_z20_particular.json; then
python3 - <<'PY'
import hashlib,json
from pathlib import Path

p=Path("results/ge19_repair14_self_consistent_reduced_h3_z20_particular.json")
d=json.loads(p.read_text())

print("CLASSIFICATION =",d["classification"])
print("PROVENANCE =",d["provenance"])
print("SOURCE_SPATIAL_MAX =",d["source_spatial_convergence"]["relative_L2_max"])
print("PRIMARY_LINEAR_RESIDUAL_MAX =",d["primary_solve_controls"]["max_linear_system_relative_L2"])
print("PRIMARY_SHIFT_MAX =",d["primary_solve_controls"]["max_shift_constraint_relative_L2"])
print("PRIMARY_ANISOTROPY_MAX =",d["primary_solve_controls"]["max_anisotropy_constraint_relative_L2"])
print("CONTROL_LINEAR_RESIDUAL_MAX =",d["control_solve_controls"]["max_linear_system_relative_L2"])
print("CONTROL_SHIFT_MAX =",d["control_solve_controls"]["max_shift_constraint_relative_L2"])
print("CONTROL_ANISOTROPY_MAX =",d["control_solve_controls"]["max_anisotropy_constraint_relative_L2"])
print("TIME_64_32_MAX =",d["time_grid_control"]["state_relative_L2_max"])
print("GATES =",d["gates"])
print("PROJECT_BOUNDARY =",d["project_boundary"])

for q in d["source_decomposition"]:
    print(
      "SOURCE",
      q["C"],
      "beta=",q["beta0"],
      "Qga=",q["Einstein_AeST_Q_L2"],
      "Qdust=",q["dust_Q_L2"],
      "Qlambda=",q["lambda_Q_L2"],
      "Y=",q["Y_H3_L2"],
      "lambda/(ga+dust)=",q["lambda_over_Einstein_AeST_plus_dust"],
      "Y/analytic=",q["Y_over_total_analytic"],
      "Ycos=",q["Y_cosine_total_analytic"],
    )

for q in d["matter_background_envelope"]:
    print("C_ENVELOPE",q)
for q in d["beta0_state_dependence"]:
    print("BETA_STATE",q)

for fn in [
  "results/ge19_repair14_self_consistent_reduced_h3_z20_particular.json",
  "results/ge19_repair14_self_consistent_reduced_h3_z20_particular.npz",
  "results/ge19_repair14_self_consistent_reduced_h3_z20_particular_FULL.log",
]:
    q=Path(fn)
    if q.exists():
        print("SHA256",fn,hashlib.sha256(q.read_bytes()).hexdigest(),"BYTES",q.stat().st_size)
PY
fi

echo "GE19_REPAIR14_EXIT=$RC"
exit "$RC"
