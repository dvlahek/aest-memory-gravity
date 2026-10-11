#!/usr/bin/env bash
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"
source .venv/bin/activate

export PYTHONUNBUFFERED=1
export PYTHONPATH="$PWD${PYTHONPATH:+:$PYTHONPATH}"

JSON="results/ge19_h4f3d12r6_matched_x10_physical_hermite_enclosure.json"
LOG="results/ge19_H4F3D12R6_LOCAL_runner.log"

test ! -e "$JSON"
test ! -e "$LOG"

set +e

/usr/bin/time -v \
python3 -m ge19.h4f3d12r6_matched_x10_physical_hermite_enclosure \
    --json-out "$JSON" \
    >"$LOG" 2>&1

RC=$?

set -e

echo "=== D12R6 SUMMARY ==="

if [[ -s "$JSON" ]]; then
python3 - <<'PY'
import json

p="results/ge19_h4f3d12r6_matched_x10_physical_hermite_enclosure.json"
j=json.load(open(p))

for k in (
    "classification",
    "global_realspace_M0_sup_abs_g10_upper",
    "global_realspace_L0_Lipschitz_dx_upper",
    "inherited_M1_sup_abs_g11_upper",
    "inherited_L1_Lipschitz_dx_upper",
    "candidate_Y_lower_regularity_modulus_coefficient",
    "all_6_C_Nt_cases_certified",
    "continuous_X10_physical_Hermite_representation_certified",
    "continuous_physical_H1_solution_error_enclosed",
    "Y_full_M0_M1_L0_L1_modulus_frozen",
    "full_Ward_execution_licensed",
    "next_route",
):
    print(k,"=",j[k])
PY

echo
sha256sum "$JSON"
fi

echo
echo "=== LAST LOG LINES ==="
tail -n 20 "$LOG" || true
echo "EXIT=$RC"

exit "$RC"
