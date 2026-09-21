#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results

echo "=== GE19 Repair20 lock audit ==="

test "$(git rev-parse HEAD:docs/ge19_repair19_projected_boundary_h3_z20_result_freeze.md)" = "642006d7f5dac17edb6ff39822fc2e09b74fd5e3"
test "$(git rev-parse HEAD:ge19/repair20_predata_shift_near_null_time_resolution_audit.json)" = "ef26c42b8f7ec72bae23c7c173c5b8e0c3232599"
test "$(git rev-parse HEAD:ge19/repair20_shift_near_null_time_resolution_audit.py)" = "09c46fa2a585ba8d055ff396abc48f0bf7e40812"
test "$(git rev-parse HEAD:.github/workflows/ge19-repair20-prelock-audit.yml)" = "111d8ea596cf9c2f640fdb6a7cf4121c2925e78e"
test "$(git rev-parse HEAD:docs/ge19_repair20_shift_time_resolution_audit_lock.md)" = "0cc64df365cc3c11ae23b85f760f2ea5492ffd99"

for sha in   71e1e60e133b79828163fe077f5991e98d40d6bb   7af03dcf16023dee12df1d93a36abf1a97881ec8   fe4ba2f9b0bf176fc5dd9f92c3ee2dcbb9da352e   01906c451c789b07e0050b16b0f2dda81582aee0   f2837e5154f8a9ca999c6bbeed4c9d62603185d8 \
  9bb8e4fd36be3fd26fb11b06a215b2806a269467 \
  410e6c35544a7225a91ca659c4001904c483cc12 \
  76256a4c1b59a680d46531bd783b4f273c37e6c5
do
  git merge-base --is-ancestor "$sha" HEAD
done

test "$(git rev-parse HEAD:ge19/repair07_window_retarded_reduced_h3_z20_particular.py)" = "e34d28a2062c748f48bc82fa928844b02631de25"
test "$(git rev-parse HEAD:ge19/repair14_self_consistent_reduced_h3_z20_particular.py)" = "06c5ced952c2370cfa4aaadb6ef8f72d2d7221de"
test "$(git rev-parse HEAD:ge19/repair18_zero_coordinate_constraint_projected_momentum_boundary.py)" = "c7b3a5c689bd78a65a8150c26e1fbfae108cb580"

echo "GE19_REPAIR20_LOCK_PASS"

if [[ -z "${VIRTUAL_ENV:-}" ]]; then
  echo "GE19_REPAIR20_VENV_NOT_ACTIVE"
  echo "Run: source .venv/bin/activate"
  exit 5
fi

python3 -m py_compile ge19/repair20_shift_near_null_time_resolution_audit.py

echo "=== GE19 Repair20 frozen local inputs ==="
for f in   results/ge15_R1_dense_accepted_step_trace.dat   results/ge15_R1_cli_background.dat   results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.json   results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz   results/ge19_repair18_zero_coordinate_constraint_projected_momentum_boundary.json   results/ge19_repair19_projected_boundary_reduced_h3_z20_propagation.json   results/ge19_repair19_projected_boundary_reduced_h3_z20_propagation.npz
do
  test -s "$f" || { echo "MISSING=$f"; exit 4; }
done

test "$(sha256sum results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.json | awk '{print $1}')" =   "ae3cc790ecffbd5498b5852273c72ae578d4615de29bbb616673c05cdb3e74b7"
test "$(sha256sum results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz | awk '{print $1}')" =   "011c0ae54fd21d70c0e2c695ce62e7b74a3c5529a07c9023c882a447d5b40ca3"
test "$(sha256sum results/ge19_repair18_zero_coordinate_constraint_projected_momentum_boundary.json | awk '{print $1}')" =   "d5603138c2f488413686323d1241613f6ef707b586116aa7fe865ae25ceb0edc"
test "$(sha256sum results/ge19_repair19_projected_boundary_reduced_h3_z20_propagation.json | awk '{print $1}')" =   "32837e04a9ea6c83642a0d465f0312cc17a02ddad168760764f3c7b999a0a14d"
test "$(sha256sum results/ge19_repair19_projected_boundary_reduced_h3_z20_propagation.npz | awk '{print $1}')" =   "d638c86e48dd5c912629068f56c3780d0a611ed26ff5c161cd792a14328f7215"

echo "GE19_REPAIR20_LOCAL_INPUTS_PRESENT"

rm -f   results/ge19_repair20_shift_near_null_time_resolution_audit.json   results/ge19_repair20_shift_near_null_time_resolution_audit.npz   results/ge19_repair20_shift_near_null_time_resolution_audit_FULL.log

echo "=== GE19 Repair20 diagnostic execution ==="
python3 ge19/repair20_shift_near_null_time_resolution_audit.py   --results-dir results   --json-out results/ge19_repair20_shift_near_null_time_resolution_audit.json   --npz-out results/ge19_repair20_shift_near_null_time_resolution_audit.npz   2>&1 | tee results/ge19_repair20_shift_near_null_time_resolution_audit_FULL.log

echo "=== GE19 Repair20 summary ==="
python3 - <<'PY'
import hashlib,json
from pathlib import Path

p=Path("results/ge19_repair20_shift_near_null_time_resolution_audit.json")
d=json.loads(p.read_text())

print("CLASSIFICATION =",d["classification"])
print("NEAR_NULL_DEFINITION =",d["near_null_definition"])
for nt in ("32","64","128"):
    q=d["per_grid"][nt]
    print(
      "NT",nt,
      "all_shift=",q["original_all_row_shift_backward_error_max"],
      "active_shift=",q["active_shift_relative_max"],
      "active_abs=",q["active_shift_absolute_residual_max"],
      "near_null_abs=",q["near_null_shift_absolute_residual_max"],
      "active_n=",q["active_sample_count"],
      "null_n=",q["near_null_sample_count"],
      "active_scale_min=",q["active_scale_min"],
      "active_scale_max=",q["active_scale_max"],
      "linear=",q["linear_system_relative_L2_residual_max"],
      "aniso=",q["anisotropy_backward_error_max"],
    )
    print("WORST_ACTIVE",nt,q["worst_active_sample"])
    print("WORST_ALL",nt,q["worst_all_row_sample"])

print("CONTROLS =",d["controls"])
print("GATES =",d["gates"])
print("ROUTING =",d["routing"])
print("INTERPRETATION_BOUNDARY =",d["interpretation_boundary"])

for fn in [
  "results/ge19_repair20_shift_near_null_time_resolution_audit.json",
  "results/ge19_repair20_shift_near_null_time_resolution_audit.npz",
  "results/ge19_repair20_shift_near_null_time_resolution_audit_FULL.log",
]:
    q=Path(fn)
    print("SHA256",fn,hashlib.sha256(q.read_bytes()).hexdigest(),"BYTES",q.stat().st_size)
PY

echo "GE19_REPAIR20_DIAGNOSTIC_COMPLETE"
