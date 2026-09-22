#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results

test "$(git rev-parse HEAD:ge19/repair32a_predata_ge06_ge05_raw_residual_normalization_dictionary_audit.json)" = "7a2b88d49ba1a6f81e5bd9818d5b63fa60d50fb1"
test "$(git rev-parse HEAD:ge19/repair32a_ge06_ge05_raw_residual_normalization_dictionary_audit.py)" = "3e10b9c2962b14d615ff8fbbc284e4dd46b3e8af"
test "$(git rev-parse HEAD:.github/workflows/ge19-repair32a-prelock-audit.yml)" = "0efd9324ef8d80187fa1eb21a432104bd0f7d217"
test "$(git rev-parse HEAD:docs/ge19_repair31_h2_dictionary_monitor_audit_result_freeze.md)" = "19004be2042257919bf80c54d796dfd5dc863684"

for c in \
  3e750030b6ac78d0da0503b65109abd8c36695fc \
  154b5072e0ff1412a39a43b28145076673c75957 \
  738643c657d7cd3546453b8c9b2141ce0e87a604 \
  8897792cc7e886956d3d6c89dd7549c832f6018b; do
  git merge-base --is-ancestor "$c" HEAD
done
echo GE19_REPAIR32A_LOCK_PASS

if [[ -z "${VIRTUAL_ENV:-}" ]]; then
  echo GE19_REPAIR32A_VENV_NOT_ACTIVE
  echo "Run: source .venv/bin/activate"
  exit 5
fi

R31="results/ge19_repair31_repair30_h2_dictionary_monitor_audit.json"
test -f "$R31"
test "$(sha256sum "$R31" | awk '{print $1}')" = "569ad9b16a26989fd8a9c9c02d83b77eb4afe23d9962fa56b87166d78d0ea33a"
echo GE19_REPAIR32A_REPAIR31_PARENT_PASS

OUT="results/ge19_repair32a_ge06_ge05_raw_residual_normalization_dictionary_audit.json"
FULL="results/ge19_repair32a_ge06_ge05_raw_residual_normalization_dictionary_audit_FULL.log"
rm -f "$OUT" "$FULL"

set -o pipefail
python3 ge19/repair32a_ge06_ge05_raw_residual_normalization_dictionary_audit.py \
  --repair31-json "$R31" \
  --json-out "$OUT" \
  2>&1 | tee "$FULL"
rc=${PIPESTATUS[0]}

if [[ "$rc" -ne 0 ]]; then
  echo "GE19_REPAIR32A_SCIENCE_EXIT=$rc"
  exit "$rc"
fi

python3 - <<'PY'
import json
d=json.load(open("results/ge19_repair32a_ge06_ge05_raw_residual_normalization_dictionary_audit.json"))
print("CLASSIFICATION =",d["classification"])
print("EXACT =",d["exact_symbolic_dictionary"])
print("IMPLEMENTATION =",d["implementation_convention_audit"])
print("EMPIRICAL =",d["Repair31_empirical_consistency"])
print("GATES =",d["gates"])
print("DICTIONARY =",d["derived_dictionary"])
print("ROUTE =",d["routing"])
PY

sha256sum "$OUT" "$FULL"
wc -c "$OUT" "$FULL"
echo GE19_REPAIR32A_EXECUTION_COMPLETE
