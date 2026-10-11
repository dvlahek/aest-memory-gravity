#!/usr/bin/env bash
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"
source .venv/bin/activate

export PYTHONUNBUFFERED=1
export PYTHONPATH="$PWD${PYTHONPATH:+:$PYTHONPATH}"

JSON="results/ge19_h4f3d12r5r1_continuous_x11_collocation_enclosure.json"
LOG="results/ge19_H4F3D12R5R1_LOCAL_runner.log"

if [[ -e "$JSON" || -e "$LOG" ]]; then
    echo "ERROR: D12R5R1 output exists; no overwrite"
    exit 20
fi

set +e

/usr/bin/time -v \
python3 -m ge19.h4f3d12r5r1_continuous_x11_collocation_enclosure \
    --json-out "$JSON" \
    >"$LOG" 2>&1

RC=$?

set -e

echo "=== D12R5R1 SUMMARY ==="

if [[ -s "$JSON" ]]; then
python3 - <<'PY'
import json

p="results/ge19_h4f3d12r5r1_continuous_x11_collocation_enclosure.json"
j=json.load(open(p))

for k in (
    "classification",
    "global_realspace_M1_sup_abs_g11_upper",
    "global_realspace_L1_Lipschitz_dx_upper",
    "max_endpoint_replay_relative",
    "max_endpoint_stitch_abs",
    "all_6_C_Nt_cases_certified",
    "continuous_X11_collocation_representation_certified",
    "continuous_physical_H2_solution_error_enclosed",
    "Y_M0_L0_certified",
    "Y_full_M0_M1_L0_L1_modulus_certified",
    "full_Ward_execution_licensed",
    "next_route",
):
    print(k,"=",j[k])
PY

echo
echo "SHA256:"
sha256sum "$JSON"
fi

echo
echo "=== LAST 20 FULL LOG LINES ==="
tail -n 20 "$LOG" || true

echo
echo "EXIT=$RC"

exit "$RC"
