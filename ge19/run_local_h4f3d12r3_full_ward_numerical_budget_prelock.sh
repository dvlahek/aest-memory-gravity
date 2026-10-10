#!/usr/bin/env bash
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"
source .venv/bin/activate

export PYTHONUNBUFFERED=1
export PYTHONPATH="$PWD${PYTHONPATH:+:$PYTHONPATH}"

OUT="results/ge19_h4f3d12r3_full_ward_numerical_budget_prelock.json"

if [[ -e "$OUT" ]]; then
    echo "ERROR: refusing overwrite: $OUT"
    exit 20
fi

python3 -m ge19.h4f3d12r3_full_ward_numerical_budget_prelock \
    --json-out "$OUT"

python3 - <<'PY'
import json
from pathlib import Path

p = Path("results/ge19_h4f3d12r3_full_ward_numerical_budget_prelock.json")
j = json.loads(p.read_text())

assert j["classification"] == (
    "GE19_H4F3D12R3_NUMERICAL_BUDGET_ROUTE_PRELOCK_PASS_FULL_BUDGET_OPEN"
)
assert j["candidate_full_Ward_residual_read"] is False
assert j["registered_hotspot_full_Ward_defect_read"] is False
assert j["B_total_defined"] is False
assert j["full_physical_FD4_FD8_structural_budget_complete"] is False
assert j["full_Ward_execution_licensed"] is False
assert j["full_original_H4_Ward_certified"] is False
assert j["Z21_certified"] is False
assert j["lensing_licensed"] is False
assert j["threshold_changed"] is False
assert j["source_coefficients_changed"] is False
assert j["observational_tuning"] is False

assert all(j["inherited_certified_closures"].values())
assert not any(j["remaining_budget_obligations"].values())

print("GE19_H4F3D12R3_RUNNER_POSTCHECK_PASS")
print("CLASSIFICATION =", j["classification"])
print("NEXT =", j["next_route"])
print("Nt128 h4*K4 =", j["physical_grid_stencil_prefactors"]["Nt128"]["h4_K4_max"])
print("Nt128 h8*K8 =", j["physical_grid_stencil_prefactors"]["Nt128"]["h8_K8_max"])
print("Nt64  h4*K4 =", j["physical_grid_stencil_prefactors"]["Nt64"]["h4_K4_max"])
print("Nt64  h8*K8 =", j["physical_grid_stencil_prefactors"]["Nt64"]["h8_K8_max"])
PY
