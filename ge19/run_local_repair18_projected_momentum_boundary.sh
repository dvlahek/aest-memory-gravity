#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results

echo "=== GE19 Repair18 lock audit ==="

test "$(git rev-parse HEAD:docs/ge19_repair17_canonical_initial_manifold_result_freeze.md)" = "37c1f93e1fa52ce9963707fe2be3bd5d076005fa"
test "$(git rev-parse HEAD:ge19/repair18_predata_zero_coordinate_constraint_projected_momentum_boundary.json)" = "884b26b4c65c3fc3c42defa9e7fdd37f9ca43850"
test "$(git rev-parse HEAD:ge19/repair18_zero_coordinate_constraint_projected_momentum_boundary.py)" = "c7b3a5c689bd78a65a8150c26e1fbfae108cb580"
test "$(git rev-parse HEAD:.github/workflows/ge19-repair18-prelock-audit.yml)" = "9ec8bac242cd48fa2fb83cb768ee59b1d632dbf9"
test "$(git rev-parse HEAD:docs/ge19_repair18_projected_momentum_boundary_lock.md)" = "72673537e3dfe3248072558e9867a94d0cb980cb"

for sha in   1ce72e3c3a732be59c1e390c8ef67859348b76c6   1e15c4f91827bdd068c3a0e19c55232345141e4d   b8a8a0b8fe3bad5a4d23b653c335fd0297302fcc   d9a1220bf1031aad39ad0044d48f60494b4085b5   47ed21b92b5043099631a563fcdc04022871cd3a
do
  git merge-base --is-ancestor "$sha" HEAD
done

echo "GE19_REPAIR18_LOCK_PASS"

if [[ -z "${VIRTUAL_ENV:-}" ]]; then
  echo "GE19_REPAIR18_VENV_NOT_ACTIVE"
  echo "Run: source .venv/bin/activate"
  exit 5
fi

python3 -m py_compile ge19/repair18_zero_coordinate_constraint_projected_momentum_boundary.py

echo "=== GE19 Repair18 frozen local inputs ==="
for f in   results/ge15_R1_dense_accepted_step_trace.dat   results/ge15_R1_cli_background.dat   results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.json   results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz   results/ge19_repair14_self_consistent_reduced_h3_z20_particular.json   results/ge19_repair15_h3_initial_shift_noether_compatibility_audit.json   results/ge19_repair16_canonical_zero_initial_state_audit.json   results/ge19_repair17_full_canonical_initial_manifold_audit.json
do
  test -s "$f" || { echo "MISSING=$f"; exit 4; }
done

test "$(sha256sum results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.json | awk '{print $1}')" =   "ae3cc790ecffbd5498b5852273c72ae578d4615de29bbb616673c05cdb3e74b7"
test "$(sha256sum results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz | awk '{print $1}')" =   "011c0ae54fd21d70c0e2c695ce62e7b74a3c5529a07c9023c882a447d5b40ca3"
test "$(sha256sum results/ge19_repair14_self_consistent_reduced_h3_z20_particular.json | awk '{print $1}')" =   "741da95a0aaffa31e27f2b05d42b8a7f011574013de8639812e453d7b130fe57"
test "$(sha256sum results/ge19_repair15_h3_initial_shift_noether_compatibility_audit.json | awk '{print $1}')" =   "a8c86b6056a3d6ab2f6f443850bef34881452b4a11b32bb6a66e2ac7920f1e50"
test "$(sha256sum results/ge19_repair16_canonical_zero_initial_state_audit.json | awk '{print $1}')" =   "768d5a2de7cd62059e7149a4765ab5a9663eef708fc29989c05192f607c5bf68"
test "$(sha256sum results/ge19_repair17_full_canonical_initial_manifold_audit.json | awk '{print $1}')" =   "f81ad8ef52eb3a7ff4d4286670a62c830f17872459f43812b059447f85e14184"

echo "GE19_REPAIR18_LOCAL_INPUTS_PRESENT"

rm -f   results/ge19_repair18_zero_coordinate_constraint_projected_momentum_boundary.json   results/ge19_repair18_zero_coordinate_constraint_projected_momentum_boundary_FULL.log

echo "=== GE19 Repair18 diagnostic execution ==="
python3 ge19/repair18_zero_coordinate_constraint_projected_momentum_boundary.py   --results-dir results   --json-out results/ge19_repair18_zero_coordinate_constraint_projected_momentum_boundary.json   2>&1 | tee results/ge19_repair18_zero_coordinate_constraint_projected_momentum_boundary_FULL.log

echo "=== GE19 Repair18 summary ==="
python3 - <<'PY'
import hashlib,json
from pathlib import Path

p=Path("results/ge19_repair18_zero_coordinate_constraint_projected_momentum_boundary.json")
d=json.loads(p.read_text())

print("CLASSIFICATION =",d["classification"])
print("BOUNDARY_RULE =",d["boundary_rule"])
print("GLOBAL =",d["global"])
print("ROUTING =",d["routing"])
print("CLAIM_BOUNDARY =",d["claim_boundary"])

rows=[q for q in d["per_case"] if q["material_source_case"]]
rows=sorted(
    rows,
    key=lambda q:max(
      q["boundary"]["shift"]["metric"],
      q["boundary"]["lapse"]["metric"],
      q["boundary"]["solver"]["scaled_relative_residual_final"],
    ),
    reverse=True
)
for q in rows[:20]:
    b=q["boundary"]
    print(
      "CASE",q["grid"],q["C"],"beta=",q["beta0"],"m=",q["m"],
      "scaled_res=",b["solver"]["scaled_relative_residual_final"],
      "rank=",b["solver"]["rank"],
      "aug_rank=",b["solver"]["augmented_rank"],
      "lapse=",b["lapse"]["metric"],
      "shift=",b["shift"]["metric"],
      "alg=",b["algebraic_relative_residual"],
      "aniso=",b["anisotropy"]["metric"],
      "pL2=",b["p_L2"],
      "qdotL2=",b["determined_qdot_L2"],
      "old_shift=",q["repair17_p_only_comparison"]["old_shift_metric"],
    )

for fn in [
  "results/ge19_repair18_zero_coordinate_constraint_projected_momentum_boundary.json",
  "results/ge19_repair18_zero_coordinate_constraint_projected_momentum_boundary_FULL.log",
]:
    q=Path(fn)
    print("SHA256",fn,hashlib.sha256(q.read_bytes()).hexdigest(),"BYTES",q.stat().st_size)
PY

echo "GE19_REPAIR18_DIAGNOSTIC_COMPLETE"
