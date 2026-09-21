#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results

echo "=== GE19 Repair12 lock audit ==="

test "$(git rev-parse HEAD:docs/ge19_repair11_lambda_h1_result_freeze.md)" = "a1b5c9a6e638305ecd0a9a16096b109befdd2dd3"
test "$(git rev-parse HEAD:ge19/repair12_predata_remaining_standard_momentum_audit.json)" = "c5845dd439ad00e49cc0b06213b0c06a07b51247"
test "$(git rev-parse HEAD:ge19/repair12_predata_amendment01_metric_and_reproduction_lock.json)" = "fc5d084b85d12c35c3a7b44bb08f43c25a13ebff"
test "$(git rev-parse HEAD:ge19/repair12_remaining_standard_momentum_audit.py)" = "6861ada55e28e5834df30e192b404fb8b3e6322b"
test "$(git rev-parse HEAD:.github/workflows/ge19-repair12-prelock-audit.yml)" = "c55b4b1ea9f5f46e12b5aa9e2ac713659e676718"
test "$(git rev-parse HEAD:docs/ge19_repair12_standard_momentum_audit_lock.md)" = "33063f946f00ed4d61d5c52593bd69262bbf27fd"

for sha in   2943869fc88146176e62147bf7b4175d9216df41   2f6e2b7da3d8e14b29a9f7998d30a6926aecf00e   5a278b0ee78d6888a11eaa6ecd22cb1dcee9ec21   67af4ee595a298000aadee1d04820a9e9564431a   79ef0208a436a1113ee8e1753bf8a1f953c0de2c   159865a3b19a2f1a786aa093a9fcb244e828ae3c
do
  git merge-base --is-ancestor "$sha" HEAD
done

echo "GE19_REPAIR12_LOCK_PASS"

if [[ -z "${VIRTUAL_ENV:-}" ]]; then
  echo "GE19_REPAIR12_VENV_NOT_ACTIVE"
  echo "Run: source .venv/bin/activate"
  exit 5
fi

python3 -m py_compile ge19/repair12_remaining_standard_momentum_audit.py

echo "=== GE19 Repair12 required frozen local inputs ==="
for f in   results/ge15_R1_dense_accepted_step_trace.dat   results/ge15_R1_cli_background.dat   results/ge19_repair11_lambda_inclusive_reduced_h1_reclosure.json   results/ge19_repair11_lambda_inclusive_reduced_h1_reclosure.npz   results/ge15_R1_cli_perturbations_k0_s.dat   results/ge15_R1_cli_perturbations_k1_s.dat   results/ge15_R1_cli_perturbations_k2_s.dat   results/ge15_R1_cli_perturbations_k3_s.dat   results/ge15_R1_cli_perturbations_k4_s.dat   results/ge15_R1_cli_perturbations_k5_s.dat
do
  test -s "$f" || { echo "MISSING=$f"; exit 4; }
done

test "$(sha256sum results/ge19_repair11_lambda_inclusive_reduced_h1_reclosure.json | awk '{print $1}')" =   "5283dd425864e8f6613678a1ad90a71e2d69243cbecd868685af45c52be077ab"
test "$(sha256sum results/ge19_repair11_lambda_inclusive_reduced_h1_reclosure.npz | awk '{print $1}')" =   "ed2431e59d89f820796f6e9b534b8ca19ae026ad55597302bf92ddb120dfec83"

echo "GE19_REPAIR12_LOCAL_INPUTS_PRESENT"

rm -f   results/ge19_repair12_remaining_standard_momentum_audit.json   results/ge19_repair12_remaining_standard_momentum_audit_FULL.log

echo "=== GE19 Repair12 diagnostic execution ==="
python3 ge19/repair12_remaining_standard_momentum_audit.py   --results-dir results   --json-out results/ge19_repair12_remaining_standard_momentum_audit.json   2>&1 | tee results/ge19_repair12_remaining_standard_momentum_audit_FULL.log

echo "=== GE19 Repair12 summary ==="
python3 - <<'PY'
import hashlib,json
from pathlib import Path

p=Path("results/ge19_repair12_remaining_standard_momentum_audit.json")
d=json.loads(p.read_text())

print("CLASSIFICATION =",d["classification"])
print("REPRODUCTION =",d["reproduction"])
print("GLOBAL =",d["global"])
print("ROUTING =",d["routing"])
print("CLAIM_BOUNDARY =",d["claim_boundary"])

for q in d["per_case"]:
    print(
        "CASE",
        q["C"],
        q["grid"],
        "m=",q["m"],
        "repair11=",q["repair11_science_shift_metric"]["max"],
        "current_pair=",q["repair11_current_pair_metric"]["max"],
        "full_pair=",q["full_standard_counterfactual_pair_metric"]["max"],
        "corr/current=",q["omitted_correction_over_current_residual"]["max"],
        "identity=",q["identity_abs_max"],
    )

for fn in [
  "results/ge19_repair12_remaining_standard_momentum_audit.json",
  "results/ge19_repair12_remaining_standard_momentum_audit_FULL.log",
]:
    q=Path(fn)
    print("SHA256",fn,hashlib.sha256(q.read_bytes()).hexdigest(),"BYTES",q.stat().st_size)
PY

echo "GE19_REPAIR12_DIAGNOSTIC_COMPLETE"
