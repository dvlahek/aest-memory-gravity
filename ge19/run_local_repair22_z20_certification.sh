#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results

echo "=== GE19 Repair22 lock audit ==="

test "$(git rev-parse HEAD:docs/ge19_repair21_on_shell_h1_matched_shift_result_freeze.md)" = "a5deb856a60c8df1c921110dc255e379806087e5"
test "$(git rev-parse HEAD:ge19/repair22_predata_on_shell_parent_z20_certification.json)" = "a3d34b23acedf071b4331c0ca27be85d3e7f5e4b"
test "$(git rev-parse HEAD:ge19/repair22_on_shell_parent_z20_certification.py)" = "4860d13c881f41dbacbdc16ff179e917644ea6a5"
test "$(git rev-parse HEAD:.github/workflows/ge19-repair22-prelock-audit.yml)" = "e39a27ccfa78a6d4c03dcefafd14bdd9284f2b0c"
test "$(git rev-parse HEAD:docs/ge19_repair22_z20_certification_implementation_lock.md)" = "c40aba27c035efe68484ad626a2547439f178868"

for sha in   a6fea1e32aebef65e43151030fe90fc6263d6ce0   515a6ac728d056330d33f4e266a53f5693fc6548   f7aef2aa9ca8a34bd2ffe0e53a7a230f461a1926   e6c70b4983603b6201449286f0d575b1674de420   e0aabdaa9367c8f8bcc828da4c450a8108993c44
do
  git merge-base --is-ancestor "$sha" HEAD
done

test "$(git rev-parse HEAD:ge19/repair07_window_retarded_reduced_h3_z20_particular.py)" = "e34d28a2062c748f48bc82fa928844b02631de25"
test "$(git rev-parse HEAD:ge19/repair13_self_consistent_reduced_background_h1_reclosure.py)" = "362d63d03d7b850fceae393f535353ded79aeea7"
test "$(git rev-parse HEAD:ge19/repair14_self_consistent_reduced_h3_z20_particular.py)" = "06c5ced952c2370cfa4aaadb6ef8f72d2d7221de"
test "$(git rev-parse HEAD:ge19/repair18_zero_coordinate_constraint_projected_momentum_boundary.py)" = "c7b3a5c689bd78a65a8150c26e1fbfae108cb580"
test "$(git rev-parse HEAD:ge19/repair21_on_shell_h1_parent_matched_shift_audit.py)" = "73e7fa0f5b3a58f0462308bf11d2a53b7616abfb"

echo "GE19_REPAIR22_LOCK_PASS"

if [[ -z "${VIRTUAL_ENV:-}" ]]; then
  echo "GE19_REPAIR22_VENV_NOT_ACTIVE"
  echo "Run: source .venv/bin/activate"
  exit 5
fi

python3 -m py_compile ge19/repair22_on_shell_parent_z20_certification.py

echo "=== GE19 Repair22 frozen local inputs ==="
for f in   results/ge15_R1_dense_accepted_step_trace.dat   results/ge15_R1_cli_background.dat   results/ge18_repair01_on_shell_matched_dust_first_order_bridge.npz   results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.json   results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz   results/ge19_repair18_zero_coordinate_constraint_projected_momentum_boundary.json   results/ge19_repair19_projected_boundary_reduced_h3_z20_propagation.json   results/ge19_repair20_shift_near_null_time_resolution_audit.json   results/ge19_repair20_shift_near_null_time_resolution_audit.npz   results/ge19_repair21_on_shell_h1_parent_matched_shift_audit.json   results/ge19_repair21_on_shell_h1_parent_matched_shift_audit.npz
do
  test -s "$f" || { echo "MISSING=$f"; exit 4; }
done

test "$(sha256sum results/ge18_repair01_on_shell_matched_dust_first_order_bridge.npz | awk '{print $1}')" =   "b6ccaf2257fbb09df701c43bc9a593a3f68238826277a510a0b3b531ea9fa6fe"
test "$(sha256sum results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.json | awk '{print $1}')" =   "ae3cc790ecffbd5498b5852273c72ae578d4615de29bbb616673c05cdb3e74b7"
test "$(sha256sum results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz | awk '{print $1}')" =   "011c0ae54fd21d70c0e2c695ce62e7b74a3c5529a07c9023c882a447d5b40ca3"
test "$(sha256sum results/ge19_repair18_zero_coordinate_constraint_projected_momentum_boundary.json | awk '{print $1}')" =   "d5603138c2f488413686323d1241613f6ef707b586116aa7fe865ae25ceb0edc"
test "$(sha256sum results/ge19_repair19_projected_boundary_reduced_h3_z20_propagation.json | awk '{print $1}')" =   "32837e04a9ea6c83642a0d465f0312cc17a02ddad168760764f3c7b999a0a14d"
test "$(sha256sum results/ge19_repair20_shift_near_null_time_resolution_audit.json | awk '{print $1}')" =   "5f1dc8e48963c6403f142958c8ce34ab1457953b47868d1a65317655cd0644eb"
test "$(sha256sum results/ge19_repair20_shift_near_null_time_resolution_audit.npz | awk '{print $1}')" =   "99937112b889bc556ada756bc7b4e834991a6019596fdbc353a40294ad3968a6"
test "$(sha256sum results/ge19_repair21_on_shell_h1_parent_matched_shift_audit.json | awk '{print $1}')" =   "e27d12f18a992a1c8c3217e67c0efd39dcf7c9d7aadcfbbb3220f7508bca1bb2"
test "$(sha256sum results/ge19_repair21_on_shell_h1_parent_matched_shift_audit.npz | awk '{print $1}')" =   "c6fcde7d39480ec7f03de2acf0f33f648a997404c9cca8f83990ed7b50667f3b"

echo "GE19_REPAIR22_LOCAL_INPUTS_PRESENT"

rm -f   results/ge19_repair22_on_shell_parent_z20_certification.json   results/ge19_repair22_on_shell_parent_z20_certification.npz   results/ge19_repair22_on_shell_parent_z20_certification_FULL.log

echo "=== GE19 Repair22 science execution ==="
set +e
python3 ge19/repair22_on_shell_parent_z20_certification.py   --results-dir results   --json-out results/ge19_repair22_on_shell_parent_z20_certification.json   --npz-out results/ge19_repair22_on_shell_parent_z20_certification.npz   2>&1 | tee results/ge19_repair22_on_shell_parent_z20_certification_FULL.log
RC=${PIPESTATUS[0]}
set -e

echo "=== GE19 Repair22 summary ==="
python3 - <<'PY'
import hashlib,json
from pathlib import Path

p=Path("results/ge19_repair22_on_shell_parent_z20_certification.json")
if not p.exists():
    raise SystemExit("Repair22 JSON missing")
d=json.loads(p.read_text())

print("CLASSIFICATION =",d["classification"])
print("Z20_CERTIFIED =",d["Z20_certified"])
print("H1_ON_SHELL =",d["H1_on_shell_controls"])
print("SOURCE_SPATIAL =",d["source_spatial_convergence"])
print("BOUNDARY =",{
  k:v for k,v in d["boundary_certification"].items() if k!="per_case"
})
print("SHIFT =",d["shift_certification"])
print("H3_CONTROLS =",d["H3_controls"])
print("COMPLETENESS =",d["completeness"])
print("GATES =",d["gates"])
print("PROJECT_BOUNDARY =",d["project_boundary"])
print("CLAIM_BOUNDARY =",d["claim_boundary"])

for fn in [
  "results/ge19_repair22_on_shell_parent_z20_certification.json",
  "results/ge19_repair22_on_shell_parent_z20_certification.npz",
  "results/ge19_repair22_on_shell_parent_z20_certification_FULL.log",
]:
    q=Path(fn)
    if q.exists():
        print("SHA256",fn,hashlib.sha256(q.read_bytes()).hexdigest(),"BYTES",q.stat().st_size)
PY

echo "GE19_REPAIR22_EXIT=$RC"
exit "$RC"
