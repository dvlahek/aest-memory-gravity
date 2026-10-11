#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

source .venv/bin/activate

export PYTHONUNBUFFERED=1
export PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}"

JSON="$ROOT/results/ge19_h4f3d12r4_y_zeroset_lower_regularity_route.json"
FULL="$ROOT/results/ge19_h4f3d12r4_y_zeroset_lower_regularity_route_FULL.log"

if [[ -e "$JSON" || -e "$FULL" ]]; then
    echo "ERROR: D12R4 output exists; no overwrite"
    exit 20
fi

TRACE=""

if [[ -d "$ROOT/frozen_repair26_repair27" ]]; then
    TRACE="$(
        find "$ROOT/frozen_repair26_repair27" \
        -type f \
        -name ge19_repair26_R1_full_history_trace.dat \
        -print -quit
    )"
fi

if [[ -z "$TRACE" ]]; then
    echo "ERROR: frozen Repair26 trace missing"
    exit 21
fi

TRACE="$(realpath "$TRACE")"

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

mkdir -p "$TMP/results"
cd "$TMP"

set +e

/usr/bin/time -v \
python3 -m ge19.h4f3d12r4_y_zeroset_lower_regularity_route \
    --results-dir "$ROOT/results" \
    --repair26-trace "$TRACE" \
    --json-out "$JSON" \
    >"$FULL" 2>&1

RC=$?

set -e

cd "$ROOT"

echo "=== D12R4 SUMMARY ==="

if [[ -s "$JSON" ]]; then
python3 - <<'PY'
import json

p = (
    "results/"
    "ge19_h4f3d12r4_y_zeroset_lower_regularity_route.json"
)

j = json.load(open(p))

for key in (
    "classification",
    "unique_C_Nt_case_count",
    "physical_beta_cohort_count",
    "strict_sign_change_count_total",
    "exact_zero_node_count_total",
    "actual_zero_set_witness_found",
    "Y_global_C9_FD8_Taylor_route_licensed",
    "Y_lower_regularity_route_selected",
    "Y_zero_set_lower_regularity_modulus_numerically_certified",
    "candidate_full_Ward_residual_read",
    "B_total_defined",
    "full_Ward_execution_licensed",
    "next_route",
):
    print(key, "=", j[key])
PY

    echo
    echo "SHA256:"
    sha256sum "$JSON"
else
    echo "D12R4 JSON missing"
fi

echo
echo "=== LAST 15 FULL-LOG LINES ==="
tail -n 15 "$FULL" || true

echo
echo "EXIT=$RC"

exit "$RC"
