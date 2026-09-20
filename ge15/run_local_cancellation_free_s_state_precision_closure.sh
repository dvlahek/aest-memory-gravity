#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

CLASS_COMMIT="e85808324f51fc694d12e3ed7439552a3c3f9540"
CLASS_DIR="${1:-$ROOT/class_ge15}"

mkdir -p results

echo "=== GE15 lock audit ==="
test "$(git rev-parse HEAD:ge15/predata_cancellation_free_s_state_precision_closure.json)" = "18cc9e69fad27429fe91b6cb7168c087349c5b8d"
test "$(git rev-parse HEAD:ge15/apply_cancellation_free_s_state_patch.py)" = "66b919b362b05721d1023441ab4a7c18f86f500c"
test "$(git rev-parse HEAD:ge15/cancellation_free_s_state_precision_closure.py)" = "8e918742f7563dc64a1e94220dff63ac29d9e388"
test "$(git rev-parse HEAD:docs/ge15_cancellation_free_s_state_precision_closure_implementation_lock.md)" = "439d1004aa89e3d59924be5fc6f5a2e3f4a47c4f"
echo "GE15_LOCK_PASS"

python3 -m py_compile   ge15/apply_cancellation_free_s_state_patch.py   ge15/cancellation_free_s_state_precision_closure.py

python3 -m pip install --user numpy scipy >/dev/null

echo "=== Prepare pinned CLASS ==="
if [ ! -d "$CLASS_DIR/.git" ]; then
  git clone https://github.com/lesgourg/class_public.git "$CLASS_DIR"
fi
git -C "$CLASS_DIR" fetch --quiet origin "$CLASS_COMMIT"
git -C "$CLASS_DIR" reset --hard "$CLASS_COMMIT"
git -C "$CLASS_DIR" clean -fdx

echo "=== Active precision-key audit ==="
python3 - "$CLASS_DIR" <<'PY'
from pathlib import Path
import sys
root=Path(sys.argv[1])
h=(root/"include"/"precisions.h").read_text()
assert "class_precision_parameter(tol_perturbations_integration,double,1.0e-5)" in h
assert "class_precision_parameter(perturbations_sampling_stepsize,double,0.1)" in h
for fn, tol, step in [
    ("ge11/pre/R1_repair01.pre","2.5e-8","0.00125"),
    ("ge11/pre/R2_repair01.pre","1.25e-8","0.000625"),
]:
    s=Path(fn).read_text()
    assert f"tol_perturbations_integration = {tol}" in s
    assert f"perturbations_sampling_stepsize = {step}" in s
    assert "tol_perturb_integration" not in s
    assert "perturb_sampling_stepsize" not in s
print("GE15_PRECISION_KEYS_PASS")
PY

echo "=== Apply validated AeST chain ==="
python3 v019/apply_patch_v019.py "$CLASS_DIR"
python3 v019i/apply_ic_patch.py "$CLASS_DIR"
python3 v019j/apply_memory_patch.py "$CLASS_DIR"
python3 v019w/apply_variational_forcing_patch.py "$CLASS_DIR"
python3 v019y/apply_output_precision_patch.py "$CLASS_DIR"
python3 v023/apply_source_grid_trace_patch.py "$CLASS_DIR"
python3 tools/apply_v072_offline_trace_runtime_reload_patch.py "$CLASS_DIR"
python3 tools/apply_v063_classy_runtime_reload_patch.py "$CLASS_DIR"
python3 ge08/apply_full_state_trace_patch.py "$CLASS_DIR"
python3 ge09/apply_dense_accepted_step_trace_patch.py "$CLASS_DIR"

echo "=== Apply locked GE15 cancellation-free state ==="
python3 ge15/apply_cancellation_free_s_state_patch.py "$CLASS_DIR"

python3 - <<'PY'
import json
p=json.load(open("results/ge15_s_state_patch.json"))
assert p["classification"]=="GE15_CANCELLATION_FREE_S_STATE_PATCH_PASS"
assert p["physics_modified"] is False
assert p["state_dimension_modified"] is False
assert p["initial_s"] == 0.0
assert all(p["checks"].values())
print("GE15_S_STATE_PATCH_AUDIT_PASS")
PY

echo "=== Build CLASS ==="
make -C "$CLASS_DIR" -j2 class

echo "=== Run locked R1/R2 closure ==="
set +e
PYTHONPATH="$ROOT" python3 ge15/cancellation_free_s_state_precision_closure.py   --class-root "$CLASS_DIR"   --json-out results/ge15_cancellation_free_s_state_precision_closure.json   --npz-out results/ge15_cancellation_free_s_state_precision_closure.npz   2>&1 | tee results/ge15_cancellation_free_s_state_precision_closure_FULL.log
RC=${PIPESTATUS[0]}
set -e

echo "=== GE15 summary ==="
if [ -s results/ge15_cancellation_free_s_state_precision_closure.json ]; then
python3 - <<'PY'
import json
d=json.load(open("results/ge15_cancellation_free_s_state_precision_closure.json"))
print("CLASSIFICATION =",d["classification"])
if "levels" in d:
    for tag in ("R1","R2"):
        r=d["levels"][tag]
        print(tag,"SOURCE_MAX =",r["source_grid_validation"]["abs_or_rel_max"])
        print(tag,"INTERNAL_GL2 =",r["jet_control"]["global_relative_L2_max"])
        print(tag,"INTERNAL_POINT =",r["jet_control"]["pointwise_abs_or_rel_max"])
        print(tag,"PT =",r["pt_identity_abs_or_rel_max"])
    q=d["refinement_control"]
    print("R1_R2_JET_GL2 =",q["global_relative_L2_max"])
    print("R1_R2_JET_POINT =",q["pointwise_abs_or_rel_max"])
    print("SHAPE_COS_MIN =",d["physical_shape_control"]["cosine_min"])
    print("REPRESENTATION_GATES =",d["representation_gates"])
    print("CLOSURE_GATES =",d["closure_gates"])
print("PROJECT_BOUNDARY =",d.get("project_boundary"))
PY
fi

echo "EXIT=$RC"
exit "$RC"
