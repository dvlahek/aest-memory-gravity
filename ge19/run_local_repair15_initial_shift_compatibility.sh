#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results

echo "=== GE19 Repair15 lock audit ==="

test "$(git rev-parse HEAD:docs/ge19_repair14_h3_z20_result_freeze.md)" = "58980049061a2a3161b56d00c734ee9fcd89c123"
test "$(git rev-parse HEAD:ge19/repair15_predata_h3_initial_shift_noether_compatibility_audit.json)" = "eca7c1c6ac9a512b843753d78da41547ea88f112"
test "$(git rev-parse HEAD:ge19/repair15_h3_initial_shift_noether_compatibility_audit.py)" = "c366894df6642df07abd9e0b9b53d98f7181aee0"
test "$(git rev-parse HEAD:.github/workflows/ge19-repair15-prelock-audit.yml)" = "953ca958a67289bcca7dee9d1aa9b69da40f20b5"
test "$(git rev-parse HEAD:docs/ge19_repair15_initial_shift_compatibility_audit_lock.md)" = "084da62c2140d7f95f038a6b30ff9fb03b092d6b"

for sha in   7ba8b312f7dd8ca7035958be2abdf03df98a5bae   576eca2dce3632037704f6c5f13f2c99a14ac87b   f3713fe784922d8def78ba1b7e8dc0bd7dc47d01   f6498a2085e6bd85aafe055cd59a68ee1fcc86d1   3356adeb403b8ed957bb7ba4c629982f5d8c1050
do
  git merge-base --is-ancestor "$sha" HEAD
done

echo "GE19_REPAIR15_LOCK_PASS"

if [[ -z "${VIRTUAL_ENV:-}" ]]; then
  echo "GE19_REPAIR15_VENV_NOT_ACTIVE"
  echo "Run: source .venv/bin/activate"
  exit 5
fi

python3 -m py_compile ge19/repair15_h3_initial_shift_noether_compatibility_audit.py

echo "=== GE19 Repair15 frozen local inputs ==="
for f in   results/ge15_R1_dense_accepted_step_trace.dat   results/ge15_R1_cli_background.dat   results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.json   results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz   results/ge19_repair14_self_consistent_reduced_h3_z20_particular.json
do
  test -s "$f" || { echo "MISSING=$f"; exit 4; }
done

test "$(sha256sum results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.json | awk '{print $1}')" =   "ae3cc790ecffbd5498b5852273c72ae578d4615de29bbb616673c05cdb3e74b7"
test "$(sha256sum results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz | awk '{print $1}')" =   "011c0ae54fd21d70c0e2c695ce62e7b74a3c5529a07c9023c882a447d5b40ca3"
test "$(sha256sum results/ge19_repair14_self_consistent_reduced_h3_z20_particular.json | awk '{print $1}')" =   "741da95a0aaffa31e27f2b05d42b8a7f011574013de8639812e453d7b130fe57"

echo "GE19_REPAIR15_LOCAL_INPUTS_PRESENT"

rm -f   results/ge19_repair15_h3_initial_shift_noether_compatibility_audit.json   results/ge19_repair15_h3_initial_shift_noether_compatibility_audit_FULL.log

echo "=== GE19 Repair15 diagnostic execution ==="
python3 ge19/repair15_h3_initial_shift_noether_compatibility_audit.py   --results-dir results   --json-out results/ge19_repair15_h3_initial_shift_noether_compatibility_audit.json   2>&1 | tee results/ge19_repair15_h3_initial_shift_noether_compatibility_audit_FULL.log

echo "=== GE19 Repair15 summary ==="
python3 - <<'PY'
import hashlib,json
from pathlib import Path

p=Path("results/ge19_repair15_h3_initial_shift_noether_compatibility_audit.json")
d=json.loads(p.read_text())

print("CLASSIFICATION =",d["classification"])
print("GLOBAL =",d["global"])
print("ROUTING =",d["routing"])
print("CLAIM_BOUNDARY =",d["claim_boundary"])

# Print only the worst material cases by left-null residual.
rows=[q for q in d["per_case"] if q["material_source_case"]]
rows=sorted(
    rows,
    key=lambda q:q["compatibility_3x2"]["left_null_compatibility_residual"],
    reverse=True
)
for q in rows[:20]:
    c=q["compatibility_3x2"]
    print(
      "CASE",
      q["grid"],q["C"],"beta=",q["beta0"],"m=",q["m"],
      "current_shift=",q["current_initial"]["shift_metric"],
      "ls=",c["least_squares_relative_residual"],
      "left=",c["left_null_compatibility_residual"],
      "rank=",c["coefficient_rank"],
      "aug_rank=",c["augmented_rank"],
      "best_pair_third=",q["best_pair_unfitted_equation_metric"],
    )

for fn in [
  "results/ge19_repair15_h3_initial_shift_noether_compatibility_audit.json",
  "results/ge19_repair15_h3_initial_shift_noether_compatibility_audit_FULL.log",
]:
    q=Path(fn)
    print("SHA256",fn,hashlib.sha256(q.read_bytes()).hexdigest(),"BYTES",q.stat().st_size)
PY

echo "GE19_REPAIR15_DIAGNOSTIC_COMPLETE"
