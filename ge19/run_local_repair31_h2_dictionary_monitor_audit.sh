#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results

test "$(git rev-parse HEAD:ge19/repair31_predata_repair30_h2_dictionary_monitor_audit.json)" = "0f118cc2b1bee07ee29841a8cb4ebbba6b7c81c3"
test "$(git rev-parse HEAD:ge19/repair31_repair30_h2_dictionary_monitor_audit.py)" = "4d8c60c1f3953a179e6a4081ac3f0f507d03e8b9"
test "$(git rev-parse HEAD:.github/workflows/ge19-repair31-prelock-audit.yml)" = "90608be0266bc16197a5ee2cd9ca028fd7c94e72"
test "$(git rev-parse HEAD:docs/ge19_repair30_reduced_h2_z11_reclosure_result_freeze.md)" = "d51f673ce825ec3b6aa474675f570e23e0538541"

for c in \
  86887a238263a92280c575a50c8ef0d940c6ca8b \
  3da9acb3dcc8cbd3dd34b3effd386a7e21c2dad1 \
  3fd1eaf05df732cec55cd8e983d01e274f4635df \
  076b8ad0f5d7579fc74e5c5550b138bc8508eae3; do
  git merge-base --is-ancestor "$c" HEAD
done
echo GE19_REPAIR31_LOCK_PASS

if [[ -z "${VIRTUAL_ENV:-}" ]]; then
  echo GE19_REPAIR31_VENV_NOT_ACTIVE
  echo "Run: source .venv/bin/activate"
  exit 5
fi

JSON30="results/ge19_repair30_reduced_h2_z11_reclosure.json"
NPZ30="results/ge19_repair30_reduced_h2_z11_reclosure.npz"

test -f "$JSON30"
test -f "$NPZ30"
test "$(sha256sum "$JSON30" | awk '{print $1}')" = "de2d282eb0729b12f96e08be434b7bc0a320a606dd96d94057f1a2c94af22ce5"
test "$(sha256sum "$NPZ30" | awk '{print $1}')" = "02d7d9d52ca53f2495b84e5a339d396b3f63f9b03d05fd5416dcd4012c454429"
echo GE19_REPAIR31_REPAIR30_PARENT_PASS

OUT="results/ge19_repair31_repair30_h2_dictionary_monitor_audit.json"
FULL="results/ge19_repair31_repair30_h2_dictionary_monitor_audit_FULL.log"
rm -f "$OUT" "$FULL"

python3 ge19/repair31_repair30_h2_dictionary_monitor_audit.py \
  --results-dir results \
  --repair30-json "$JSON30" \
  --repair30-npz "$NPZ30" \
  --json-out "$OUT" \
  2>&1 | tee "$FULL"

python3 - <<'PY'
import json
d=json.load(open("results/ge19_repair31_repair30_h2_dictionary_monitor_audit.json"))
print("CLASSIFICATION =",d["classification"])
print("REPAIR30_RELABELLED =",d["Repair30_relabelled"])
print("H2_REINTEGRATED =",d["Repair30_H2_reintegrated"])
print("SHIFT =",d["shift_monitor_audit"])
print("STATE =",d["state_precision_audit"])
print("CHI =",d["chi_parent_audit"])
print("OPERATOR_SUMMARY =",d["operator_residual_localization"]["summary"])
print("SOURCE_IDENTITY =",d["source_identity_audit"])
print("ROUTE =",d["routing"])
PY

sha256sum "$OUT" "$FULL"
wc -c "$OUT" "$FULL"
echo GE19_REPAIR31_EXECUTION_COMPLETE
