#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results

echo "=== GE19 Repair17 lock audit ==="

test "$(git rev-parse HEAD:docs/ge19_repair16_canonical_zero_initial_result_freeze.md)" = "f5f793e41d81e450daa849786b7da7db4a2def5e"
test "$(git rev-parse HEAD:ge19/repair17_predata_full_canonical_initial_manifold_audit.json)" = "793ae9eebb100f71b425403f14d743ff2cbde5d5"
test "$(git rev-parse HEAD:ge19/repair17_full_canonical_initial_manifold_audit.py)" = "531939bc5859a66c80b9f59755d6f10a0dae4ca7"
test "$(git rev-parse HEAD:.github/workflows/ge19-repair17-prelock-audit.yml)" = "b260d33d803d5359ca26044c21f3dad7e6930b6e"
test "$(git rev-parse HEAD:docs/ge19_repair17_canonical_initial_manifold_audit_lock.md)" = "d111ec2beee9e069a84c2d617b37d374a288b716"

for sha in   d5a619495f0f8fb2da53528b46476a15c1a32922   7d5664743b2bda32fcd1a444ece37cdc14a3d96d   753015f7a377ca8bfe541cace99fb239b49a7654   159f68307990ab6a1b131a9b74c350c831f5ecdb   17487d847ddfaf6ac64b0c648156f1b69295b3ec
do
  git merge-base --is-ancestor "$sha" HEAD
done

echo "GE19_REPAIR17_LOCK_PASS"

if [[ -z "${VIRTUAL_ENV:-}" ]]; then
  echo "GE19_REPAIR17_VENV_NOT_ACTIVE"
  echo "Run: source .venv/bin/activate"
  exit 5
fi

python3 -m py_compile ge19/repair17_full_canonical_initial_manifold_audit.py

echo "=== GE19 Repair17 frozen local inputs ==="
for f in   results/ge15_R1_dense_accepted_step_trace.dat   results/ge15_R1_cli_background.dat   results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.json   results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz   results/ge19_repair14_self_consistent_reduced_h3_z20_particular.json   results/ge19_repair15_h3_initial_shift_noether_compatibility_audit.json   results/ge19_repair16_canonical_zero_initial_state_audit.json
do
  test -s "$f" || { echo "MISSING=$f"; exit 4; }
done

test "$(sha256sum results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.json | awk '{print $1}')" =   "ae3cc790ecffbd5498b5852273c72ae578d4615de29bbb616673c05cdb3e74b7"
test "$(sha256sum results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz | awk '{print $1}')" =   "011c0ae54fd21d70c0e2c695ce62e7b74a3c5529a07c9023c882a447d5b40ca3"
test "$(sha256sum results/ge19_repair14_self_consistent_reduced_h3_z20_particular.json | awk '{print $1}')" =   "741da95a0aaffa31e27f2b05d42b8a7f011574013de8639812e453d7b130fe57"
test "$(sha256sum results/ge19_repair15_h3_initial_shift_noether_compatibility_audit.json | awk '{print $1}')" =   "a8c86b6056a3d6ab2f6f443850bef34881452b4a11b32bb6a66e2ac7920f1e50"
test "$(sha256sum results/ge19_repair16_canonical_zero_initial_state_audit.json | awk '{print $1}')" =   "768d5a2de7cd62059e7149a4765ab5a9663eef708fc29989c05192f607c5bf68"

echo "GE19_REPAIR17_LOCAL_INPUTS_PRESENT"

rm -f   results/ge19_repair17_full_canonical_initial_manifold_audit.json   results/ge19_repair17_full_canonical_initial_manifold_audit_FULL.log

echo "=== GE19 Repair17 diagnostic execution ==="
python3 ge19/repair17_full_canonical_initial_manifold_audit.py   --results-dir results   --json-out results/ge19_repair17_full_canonical_initial_manifold_audit.json   2>&1 | tee results/ge19_repair17_full_canonical_initial_manifold_audit_FULL.log

echo "=== GE19 Repair17 summary ==="
python3 - <<'PY'
import hashlib,json
from pathlib import Path

p=Path("results/ge19_repair17_full_canonical_initial_manifold_audit.json")
d=json.loads(p.read_text())

print("CLASSIFICATION =",d["classification"])
print("GLOBAL =",d["global"])
print("ROUTING =",d["routing"])
print("CLAIM_BOUNDARY =",d["claim_boundary"])

rows=[q for q in d["per_case"] if q["material_source_case"]]
rows=sorted(
    rows,
    key=lambda q:max(
      q["candidates"]["full_y"]["lapse"]["metric"],
      q["candidates"]["full_y"]["shift"]["metric"],
      q["candidates"]["full_y"]["relative_residual"],
    ),
    reverse=True
)
for q in rows[:20]:
    f=q["candidates"]["full_y"]
    qo=q["candidates"]["q_only"]
    po=q["candidates"]["p_only"]
    print(
      "CASE",q["grid"],q["C"],"beta=",q["beta0"],"m=",q["m"],
      "full_res=",f["relative_residual"],
      "full_rank=",f["coefficient_rank"],
      "full_aug=",f["augmented_rank"],
      "full_lapse=",f["lapse"]["metric"],
      "full_shift=",f["shift"]["metric"],
      "full_alg=",f["algebraic_relative_residual"],
      "full_yL2=",f["y_L2"],
      "qonly_res=",qo["relative_residual"],
      "ponly_res=",po["relative_residual"],
    )

for fn in [
  "results/ge19_repair17_full_canonical_initial_manifold_audit.json",
  "results/ge19_repair17_full_canonical_initial_manifold_audit_FULL.log",
]:
    q=Path(fn)
    print("SHA256",fn,hashlib.sha256(q.read_bytes()).hexdigest(),"BYTES",q.stat().st_size)
PY

echo "GE19_REPAIR17_DIAGNOSTIC_COMPLETE"
