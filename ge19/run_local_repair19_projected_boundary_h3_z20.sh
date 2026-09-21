#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results

echo "=== GE19 Repair19 lock audit ==="

test "$(git rev-parse HEAD:docs/ge19_repair18_projected_momentum_boundary_result_freeze.md)" = "c8bf1226cc6491c3be9246c629d958f681255e81"
test "$(git rev-parse HEAD:ge19/repair19_predata_projected_boundary_reduced_h3_z20_propagation.json)" = "8eefdfd8f3a5b07702a5e1f6b28f911dc3b6089a"
test "$(git rev-parse HEAD:ge19/repair19_projected_boundary_reduced_h3_z20_propagation.py)" = "ecf1577b19c7f03e8762c1c29822881158c3cb56"
test "$(git rev-parse HEAD:.github/workflows/ge19-repair19-prelock-audit.yml)" = "2b9c3bf4f817c427b1f9914c65aa77e401a1379f"
test "$(git rev-parse HEAD:docs/ge19_repair19_projected_boundary_h3_z20_implementation_lock.md)" = "c0cfb324e3cba0a60e4ed0958dddb89d22f4868f"

for sha in   3892ee81c8030ee7c5131d1aaf1f333cbdbe6509   ce0b1767874d71eee59b55ad4633033c3d714892   2bc808214b7b099ecb78084e5c41acebc1d3be7b   8fc5a47c9be57530805f197b0b5bccdd43f5c20f   ee82d96312463471b6ee2007a4eba14dec60b8d5
do
  git merge-base --is-ancestor "$sha" HEAD
done

test "$(git rev-parse HEAD:ge19/repair07_window_retarded_reduced_h3_z20_particular.py)" = "e34d28a2062c748f48bc82fa928844b02631de25"
test "$(git rev-parse HEAD:ge19/repair14_self_consistent_reduced_h3_z20_particular.py)" = "06c5ced952c2370cfa4aaadb6ef8f72d2d7221de"
test "$(git rev-parse HEAD:ge19/repair18_zero_coordinate_constraint_projected_momentum_boundary.py)" = "c7b3a5c689bd78a65a8150c26e1fbfae108cb580"

echo "GE19_REPAIR19_LOCK_PASS"

if [[ -z "${VIRTUAL_ENV:-}" ]]; then
  echo "GE19_REPAIR19_VENV_NOT_ACTIVE"
  echo "Run: source .venv/bin/activate"
  exit 5
fi

python3 -m py_compile ge19/repair19_projected_boundary_reduced_h3_z20_propagation.py

echo "=== GE19 Repair19 frozen local inputs ==="
for f in   results/ge15_R1_dense_accepted_step_trace.dat   results/ge15_R1_cli_background.dat   results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.json   results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz   results/ge19_repair18_zero_coordinate_constraint_projected_momentum_boundary.json
do
  test -s "$f" || { echo "MISSING=$f"; exit 4; }
done

test "$(sha256sum results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.json | awk '{print $1}')" =   "ae3cc790ecffbd5498b5852273c72ae578d4615de29bbb616673c05cdb3e74b7"
test "$(sha256sum results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz | awk '{print $1}')" =   "011c0ae54fd21d70c0e2c695ce62e7b74a3c5529a07c9023c882a447d5b40ca3"
test "$(sha256sum results/ge19_repair18_zero_coordinate_constraint_projected_momentum_boundary.json | awk '{print $1}')" =   "d5603138c2f488413686323d1241613f6ef707b586116aa7fe865ae25ceb0edc"

echo "GE19_REPAIR19_LOCAL_INPUTS_PRESENT"

rm -f   results/ge19_repair19_projected_boundary_reduced_h3_z20_propagation.json   results/ge19_repair19_projected_boundary_reduced_h3_z20_propagation.npz   results/ge19_repair19_projected_boundary_reduced_h3_z20_propagation_FULL.log

echo "=== GE19 Repair19 science execution ==="
set +e
python3 ge19/repair19_projected_boundary_reduced_h3_z20_propagation.py   --results-dir results   --json-out results/ge19_repair19_projected_boundary_reduced_h3_z20_propagation.json   --npz-out results/ge19_repair19_projected_boundary_reduced_h3_z20_propagation.npz   2>&1 | tee results/ge19_repair19_projected_boundary_reduced_h3_z20_propagation_FULL.log
RC=${PIPESTATUS[0]}
set -e

echo "=== GE19 Repair19 summary ==="
python3 - <<'PY'
import hashlib,json
from pathlib import Path

p=Path("results/ge19_repair19_projected_boundary_reduced_h3_z20_propagation.json")
if not p.exists():
    raise SystemExit("Repair19 JSON missing")
d=json.loads(p.read_text())

print("CLASSIFICATION =",d["classification"])
print("BOUNDARY_REPRODUCTION =",{
    k:v for k,v in d["initial_boundary_reproduction"].items()
    if k!="rows"
})
print("SOURCE_SPATIAL_MAX =",d["source_spatial_convergence"]["relative_L2_max"])
print("PRIMARY_CONTROLS =",{
  "linear":d["primary_solve_controls"]["max_linear_system_relative_L2"],
  "shift":d["primary_solve_controls"]["max_shift_constraint_relative_L2"],
  "anisotropy":d["primary_solve_controls"]["max_anisotropy_constraint_relative_L2"],
})
print("CONTROL_CONTROLS =",d["control_solve_controls"])
print("TIME_64_32_MAX =",d["time_grid_control"]["state_relative_L2_max"])
print("GATES =",d["gates"])
print("PROJECT_BOUNDARY =",d["project_boundary"])
print("CLAIM_BOUNDARY =",d["claim_boundary"])

for fn in [
  "results/ge19_repair19_projected_boundary_reduced_h3_z20_propagation.json",
  "results/ge19_repair19_projected_boundary_reduced_h3_z20_propagation.npz",
  "results/ge19_repair19_projected_boundary_reduced_h3_z20_propagation_FULL.log",
]:
    q=Path(fn)
    if q.exists():
        print("SHA256",fn,hashlib.sha256(q.read_bytes()).hexdigest(),"BYTES",q.stat().st_size)
PY

echo "GE19_REPAIR19_EXIT=$RC"
exit "$RC"
