#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results

echo "=== GE19 Repair16 lock audit ==="

test "$(git rev-parse HEAD:docs/ge19_repair15_initial_shift_compatibility_result_freeze.md)" = "fb79a6fcb2e8cc172edcf3b1f4cdc25e643da8ca"
test "$(git rev-parse HEAD:ge19/repair16_predata_canonical_zero_initial_state_audit.json)" = "46dfc2004cfd4f8d3ba22f67c48518dc2af95269"
test "$(git rev-parse HEAD:ge19/repair16_canonical_zero_initial_state_audit.py)" = "232bae522de42225db0e95ce7ad685c6a5251e3d"
test "$(git rev-parse HEAD:.github/workflows/ge19-repair16-prelock-audit.yml)" = "af7235396e3a6c82373497fd449ab0e1610551a8"
test "$(git rev-parse HEAD:docs/ge19_repair16_canonical_zero_initial_audit_lock.md)" = "98e53ff9627f0a640be8690066d10bce65f2db3b"

for sha in   e2d642eb528fab10aa4d3ba0a2afc94b2dcacbaf   eceadb445335212621aa6563118882f6b6a8d8ab   d86abd3452827a491a1acc627873ff4b62752693   db4c441ae63186ab2f5b25d8b24e6101ddcd2e17   8e17ba47341718a350fd3b42e271408c4617914a
do
  git merge-base --is-ancestor "$sha" HEAD
done

echo "GE19_REPAIR16_LOCK_PASS"

if [[ -z "${VIRTUAL_ENV:-}" ]]; then
  echo "GE19_REPAIR16_VENV_NOT_ACTIVE"
  echo "Run: source .venv/bin/activate"
  exit 5
fi

python3 -m py_compile ge19/repair16_canonical_zero_initial_state_audit.py

echo "=== GE19 Repair16 frozen local inputs ==="
for f in   results/ge15_R1_dense_accepted_step_trace.dat   results/ge15_R1_cli_background.dat   results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.json   results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz   results/ge19_repair14_self_consistent_reduced_h3_z20_particular.json   results/ge19_repair15_h3_initial_shift_noether_compatibility_audit.json
do
  test -s "$f" || { echo "MISSING=$f"; exit 4; }
done

test "$(sha256sum results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.json | awk '{print $1}')" =   "ae3cc790ecffbd5498b5852273c72ae578d4615de29bbb616673c05cdb3e74b7"
test "$(sha256sum results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz | awk '{print $1}')" =   "011c0ae54fd21d70c0e2c695ce62e7b74a3c5529a07c9023c882a447d5b40ca3"
test "$(sha256sum results/ge19_repair14_self_consistent_reduced_h3_z20_particular.json | awk '{print $1}')" =   "741da95a0aaffa31e27f2b05d42b8a7f011574013de8639812e453d7b130fe57"
test "$(sha256sum results/ge19_repair15_h3_initial_shift_noether_compatibility_audit.json | awk '{print $1}')" =   "a8c86b6056a3d6ab2f6f443850bef34881452b4a11b32bb6a66e2ac7920f1e50"

echo "GE19_REPAIR16_LOCAL_INPUTS_PRESENT"

rm -f   results/ge19_repair16_canonical_zero_initial_state_audit.json   results/ge19_repair16_canonical_zero_initial_state_audit_FULL.log

echo "=== GE19 Repair16 diagnostic execution ==="
python3 ge19/repair16_canonical_zero_initial_state_audit.py   --results-dir results   --json-out results/ge19_repair16_canonical_zero_initial_state_audit.json   2>&1 | tee results/ge19_repair16_canonical_zero_initial_state_audit_FULL.log

echo "=== GE19 Repair16 summary ==="
python3 - <<'PY'
import hashlib,json
from pathlib import Path

p=Path("results/ge19_repair16_canonical_zero_initial_state_audit.json")
d=json.loads(p.read_text())

print("CLASSIFICATION =",d["classification"])
print("GLOBAL =",d["global"])
print("ROUTING =",d["routing"])
print("CLAIM_BOUNDARY =",d["claim_boundary"])

rows=[q for q in d["per_case"] if q["material_source_case"]]
rows=sorted(rows,key=lambda q:max(q["lapse"]["metric"],q["shift"]["metric"]),reverse=True)
for q in rows[:20]:
    print(
      "CASE",q["grid"],q["C"],"beta=",q["beta0"],"m=",q["m"],
      "alg=",q["algebraic_relative_residual"],
      "lapse=",q["lapse"]["metric"],
      "shift=",q["shift"]["metric"],
      "aniso=",q["anisotropy"]["metric"],
      "qdotL2=",q["determined_qdot_L2"],
      "cond=",q["algebraic_scaled_condition_2"],
    )

for fn in [
  "results/ge19_repair16_canonical_zero_initial_state_audit.json",
  "results/ge19_repair16_canonical_zero_initial_state_audit_FULL.log",
]:
    q=Path(fn)
    print("SHA256",fn,hashlib.sha256(q.read_bytes()).hexdigest(),"BYTES",q.stat().st_size)
PY

echo "GE19_REPAIR16_DIAGNOSTIC_COMPLETE"
