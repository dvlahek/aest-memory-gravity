#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results

echo "=== GE19 Repair21 lock audit ==="

test "$(git rev-parse HEAD:docs/ge19_repair20_shift_time_resolution_result_freeze.md)" = "34ee88238837e5b661d7f633b6df6df2e6c3662a"
test "$(git rev-parse HEAD:ge19/repair21_predata_on_shell_h1_parent_matched_shift_audit.json)" = "2d1925a043348422693e0e66edb5a73e5e9daebc"
test "$(git rev-parse HEAD:ge19/repair21_on_shell_h1_parent_matched_shift_audit.py)" = "73e7fa0f5b3a58f0462308bf11d2a53b7616abfb"
test "$(git rev-parse HEAD:.github/workflows/ge19-repair21-prelock-audit.yml)" = "1e61e09d25aceed56b4c778976a0ebcf8d3c1d35"
test "$(git rev-parse HEAD:docs/ge19_repair21_on_shell_h1_matched_shift_audit_lock.md)" = "51c868b93fdf3e578174480e0396b51a0a4d444c"

for sha in   317b4219f6630b0c1f0f15081e8db62e6470a47c   434dc92f0f59e34d84ca730ea041edecb004271c   9d75bd9a457a2d54089286e3fc6ff5a3c84a3aa0   9a23dedaad79887b0f1626541031e0b650743197   1d3b1f25f12c856fbe43d92759fc4e34c970b0cc
do
  git merge-base --is-ancestor "$sha" HEAD
done

test "$(git rev-parse HEAD:ge19/repair07_window_retarded_reduced_h3_z20_particular.py)" = "e34d28a2062c748f48bc82fa928844b02631de25"
test "$(git rev-parse HEAD:ge19/repair13_self_consistent_reduced_background_h1_reclosure.py)" = "362d63d03d7b850fceae393f535353ded79aeea7"
test "$(git rev-parse HEAD:ge19/repair14_self_consistent_reduced_h3_z20_particular.py)" = "06c5ced952c2370cfa4aaadb6ef8f72d2d7221de"
test "$(git rev-parse HEAD:ge19/repair18_zero_coordinate_constraint_projected_momentum_boundary.py)" = "c7b3a5c689bd78a65a8150c26e1fbfae108cb580"

echo "GE19_REPAIR21_LOCK_PASS"

if [[ -z "${VIRTUAL_ENV:-}" ]]; then
  echo "GE19_REPAIR21_VENV_NOT_ACTIVE"
  echo "Run: source .venv/bin/activate"
  exit 5
fi

python3 -m py_compile ge19/repair21_on_shell_h1_parent_matched_shift_audit.py

echo "=== GE19 Repair21 frozen local inputs ==="
for f in   results/ge15_R1_dense_accepted_step_trace.dat   results/ge15_R1_cli_background.dat   results/ge18_repair01_on_shell_matched_dust_first_order_bridge.npz   results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.json   results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz   results/ge19_repair18_zero_coordinate_constraint_projected_momentum_boundary.json   results/ge19_repair19_projected_boundary_reduced_h3_z20_propagation.json   results/ge19_repair20_shift_near_null_time_resolution_audit.json   results/ge19_repair20_shift_near_null_time_resolution_audit.npz
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

echo "GE19_REPAIR21_LOCAL_INPUTS_PRESENT"

rm -f   results/ge19_repair21_on_shell_h1_parent_matched_shift_audit.json   results/ge19_repair21_on_shell_h1_parent_matched_shift_audit.npz   results/ge19_repair21_on_shell_h1_parent_matched_shift_audit_FULL.log

echo "=== GE19 Repair21 diagnostic execution ==="
python3 ge19/repair21_on_shell_h1_parent_matched_shift_audit.py   --results-dir results   --json-out results/ge19_repair21_on_shell_h1_parent_matched_shift_audit.json   --npz-out results/ge19_repair21_on_shell_h1_parent_matched_shift_audit.npz   2>&1 | tee results/ge19_repair21_on_shell_h1_parent_matched_shift_audit_FULL.log

echo "=== GE19 Repair21 summary ==="
python3 - <<'PY'
import hashlib,json
from pathlib import Path

p=Path("results/ge19_repair21_on_shell_h1_parent_matched_shift_audit.json")
d=json.loads(p.read_text())

print("CLASSIFICATION =",d["classification"])
print("H1_ON_SHELL =",d["H1_on_shell_controls"])
print("INTERP_COUNTERFACTUAL =",d["Repair20_interpolated_parent_counterfactual"])
print("NEAR_NULL =",d["near_null_definition"])
print("PER_GRID =",d["per_grid"])
print("MATCHED_SHIFT =",d["matched_shift"])
print("H3_CONTROLS =",d["H3_controls"])
print("ROUTING =",d["routing"])
print("INTERPRETATION_BOUNDARY =",d["interpretation_boundary"])

for fn in [
  "results/ge19_repair21_on_shell_h1_parent_matched_shift_audit.json",
  "results/ge19_repair21_on_shell_h1_parent_matched_shift_audit.npz",
  "results/ge19_repair21_on_shell_h1_parent_matched_shift_audit_FULL.log",
]:
    q=Path(fn)
    print("SHA256",fn,hashlib.sha256(q.read_bytes()).hexdigest(),"BYTES",q.stat().st_size)
PY

echo "GE19_REPAIR21_DIAGNOSTIC_COMPLETE"
