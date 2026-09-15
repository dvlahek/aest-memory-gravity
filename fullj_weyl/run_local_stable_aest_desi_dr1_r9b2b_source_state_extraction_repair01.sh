#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

REPAIR_LOCK='cda4cf9f6c633a5711d2bc3b0a167ec3dff6e06e'
BASE_RUNNER_LOCK='0f4fcee56c02f8602c063483a0260b91177e2f7b'
BASE_IMPLEMENTATION_LOCK='0de8395673e56d4279cf038899c46fcf5aa003bf'

for lock in "$REPAIR_LOCK" "$BASE_RUNNER_LOCK" "$BASE_IMPLEMENTATION_LOCK"; do
  git merge-base --is-ancestor "$lock" HEAD
 done

echo "STABLE_AEST_DESI_DR1_R9B2B_REPAIR01_LOCK_PASS repair=$REPAIR_LOCK runner=$BASE_RUNNER_LOCK implementation=$BASE_IMPLEMENTATION_LOCK"

R9B2A_JSON='results/stable_aest_desi_dr1_r9b2a_extraction_invariance.json'
[[ -s "$R9B2A_JSON" ]] || { echo 'R9B2B_REPAIR01: R9b2a JSON missing' >&2; exit 3; }

BASE_PY="$(command -v python3 || command -v python || true)"
[[ -n "$BASE_PY" ]] || { echo 'R9B2B_REPAIR01: Python missing' >&2; exit 2; }

"$BASE_PY" - "$R9B2A_JSON" <<'PY'
import json, sys
p=sys.argv[1]
d=json.load(open(p))
expected={
 'R9B2A_A1_provenance_and_historical_fail_lock': True,
 'R9B2A_A2_internal_output_request_invariance': True,
 'R9B2A_A3_serialization_free_density_consistency': False,
 'R9B2A_A4_serialization_free_direct_velocity_sanity': False,
 'R9B2A_A5_eta0_tau_invariance': True,
 'R9B2A_A6_material_diagnostic_output_contamination': False,
}
assert d.get('classification') == 'STABLE_AEST_DESI_DR1_R9B2A_SERIALIZATION_FREE_EXTRACTION_UNRESOLVED', d.get('classification')
assert d.get('diagnostic_complete') is True
assert d.get('science_evaluated') is False
assert d.get('gates') == expected, d.get('gates')
print('STABLE_AEST_DESI_DR1_R9B2B_REPAIR01_R9B2A_SEMANTIC_PARENT_PASS')
PY

echo "STABLE_AEST_DESI_DR1_R9B2B_REPAIR01_R9B2A_LOCAL_SHA=$(sha256sum "$R9B2A_JSON" | awk '{print $1}')"

RUNNER='fullj_weyl/run_local_stable_aest_desi_dr1_r9b2b_source_state_extraction.sh'
IMPL='fullj_weyl/stable_aest_desi_dr1_r9b2b_source_state_extraction.py'
RUNNER_BAK="$(mktemp)"
IMPL_BAK="$(mktemp)"
cp "$RUNNER" "$RUNNER_BAK"
cp "$IMPL" "$IMPL_BAK"
restore() {
  cp "$RUNNER_BAK" "$RUNNER" || true
  cp "$IMPL_BAK" "$IMPL" || true
  rm -f "$RUNNER_BAK" "$IMPL_BAK"
}
trap restore EXIT

"$BASE_PY" - "$RUNNER" "$IMPL" <<'PY'
from pathlib import Path
import sys
runner=Path(sys.argv[1])
impl=Path(sys.argv[2])

r=runner.read_text()
old="[[ \"$(sha256sum \"$R9B2A_JSON\" | awk '{print $1}')\" == \"$R9B2A_JSON_SHA\" ]] || { echo 'R9B2B: R9b2a JSON SHA mismatch' >&2; exit 3; }"
new="echo \"STABLE_AEST_DESI_DR1_R9B2B_R9B2A_LOCAL_SHA=$(sha256sum \"$R9B2A_JSON\" | awk '{print $1}')\""
if r.count(old) != 1:
    raise SystemExit(f'runner SHA gate marker count={r.count(old)}')
runner.write_text(r.replace(old,new))

s=impl.read_text()
old2='            and sha256(R9B2A_JSON) == R9B2A_JSON_SHA256\n'
new2=(
'            and r9b2a.get("gates", {}).get("R9B2A_A1_provenance_and_historical_fail_lock") is True\n'
'            and r9b2a.get("gates", {}).get("R9B2A_A2_internal_output_request_invariance") is True\n'
'            and r9b2a.get("gates", {}).get("R9B2A_A3_serialization_free_density_consistency") is False\n'
'            and r9b2a.get("gates", {}).get("R9B2A_A4_serialization_free_direct_velocity_sanity") is False\n'
'            and r9b2a.get("gates", {}).get("R9B2A_A5_eta0_tau_invariance") is True\n'
'            and r9b2a.get("gates", {}).get("R9B2A_A6_material_diagnostic_output_contamination") is False\n'
)
if s.count(old2) != 1:
    raise SystemExit(f'implementation SHA gate marker count={s.count(old2)}')
impl.write_text(s.replace(old2,new2))
print('STABLE_AEST_DESI_DR1_R9B2B_REPAIR01_PATCH_PASS')
PY

"$BASE_PY" -m py_compile "$IMPL"

echo STABLE_AEST_DESI_DR1_R9B2B_REPAIR01_PROVENANCE_GATE_PASS

set +e
bash "$RUNNER"
code=$?
set -e

echo "STABLE_AEST_DESI_DR1_R9B2B_REPAIR01_EXIT=$code"
exit "$code"
