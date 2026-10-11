#!/usr/bin/env bash
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"
source .venv/bin/activate

export PYTHONUNBUFFERED=1
export PYTHONPATH="$PWD${PYTHONPATH:+:$PYTHONPATH}"

OUT="results/ge19_h4f3d12r4r1_y_spatial_zeroset_structural_repair.json"
LOG="results/ge19_H4F3D12R4R1_LOCAL_runner.log"

test ! -e "$OUT"
test ! -e "$LOG"

python3 -m ge19.h4f3d12r4r1_y_spatial_zeroset_structural_repair \
    --json-out "$OUT" \
    >"$LOG" 2>&1

tail -n 12 "$LOG"

python3 - <<'PY'
import json

j=json.load(open(
 "results/ge19_h4f3d12r4r1_y_spatial_zeroset_structural_repair.json"
))

assert j["spatial_zero_exists_for_every_time_slice"] is True
assert j["global_abs_g10_positive_separation_possible"] is False
assert j["Y_lower_regularity_route_selected"] is True
assert j["candidate_full_Ward_residual_read"] is False
assert j["B_total_defined"] is False
assert j["Z21_certified"] is False

print("D12R4R1_POSTCHECK_PASS")
PY
