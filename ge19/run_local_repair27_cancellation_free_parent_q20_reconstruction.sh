#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results

echo "=== GE19 Repair27 lock audit ==="

test "$(git rev-parse HEAD:ge19/repair27_predata_cancellation_free_parent_q20_reconstruction.json)" = "392844e89bab78efdef3c5f8c84f4068cf71cb03"
test "$(git rev-parse HEAD:ge19/repair27_cancellation_free_parent_q20_reconstruction.py)" = "adbab56e67f765ab5e2b37980abae42312a55b44"
test "$(git rev-parse HEAD:.github/workflows/ge19-repair27-prelock-audit.yml)" = "5ce383c8c47c4f4dc935ddefeccb492e591d8941"
test "$(git rev-parse HEAD:docs/ge19_repair27_cancellation_free_parent_q20_reconstruction_implementation_lock.md)" = "5444fc47dbf08d0d3b861ee607efaefd9dd1e83c"
test "$(git rev-parse HEAD:docs/ge19_repair26_cancellation_free_full_history_bath_boundary_result_freeze.md)" = "4a620b1ace8445085d3618db177ca76ef9cadb6a"
test "$(git rev-parse HEAD:ge19/repair24_q20_construction.py)" = "fc271987d1bddcd023cc9c057ddcad036b1d72fb"

for sha in \
  2c711fe61d7a8a98dac1141d314663cc34927dcf \
  bb43045a5a708f34ea6af645a616aa812babee00 \
  2cbc212d51b40364e12f2d2bd8b9c5439cb540ee \
  6564ae09e808bc29889cc11c7f5ab34590452d19
do
  git merge-base --is-ancestor "$sha" HEAD
done

echo "GE19_REPAIR27_LOCK_PASS"

if [[ -z "${VIRTUAL_ENV:-}" ]]; then
  echo "GE19_REPAIR27_VENV_NOT_ACTIVE"
  echo "Run: source .venv/bin/activate"
  exit 5
fi

python3 -m py_compile \
  ge19/repair24_q20_construction.py \
  ge19/repair27_cancellation_free_parent_q20_reconstruction.py

python3 - <<'PY'
import importlib.util, json
from pathlib import Path

p=json.load(open("ge19/repair27_predata_cancellation_free_parent_q20_reconstruction.json"))
assert p["classification"]=="GE19_REPAIR27_PREDATA_CANCELLATION_FREE_PARENT_Q20_RECONSTRUCTION"
assert p["created_before_repair27_result"] is True
assert p["frozen_repair26_parent"]["workflow_run_id"]==35721220889
assert p["frozen_repair26_parent"]["artifact_id"]==10690709843
assert p["frozen_repair26_parent"]["R1_full_history_trace_sha256"]=="608ee0b4c868a701db6976f756b9a551cd9ddffe1e8e4ab37c5cd2361405a6f8"
assert p["only_allowed_change"]["fitted_rescaling"] is False
assert p["only_allowed_change"]["Repair25_per_mode_scales_used"] is False

spec=importlib.util.spec_from_file_location(
    "r27",Path("ge19/repair27_cancellation_free_parent_q20_reconstruction.py")
)
r27=importlib.util.module_from_spec(spec)
spec.loader.exec_module(r27)
r27.audit_core()
assert r27.REPAIR26_R1_TRACE_SHA=="608ee0b4c868a701db6976f756b9a551cd9ddffe1e8e4ab37c5cd2361405a6f8"
assert r27.REPAIR26_R1_TRACE_BYTES==26643162
assert r27.EXPECTED_CORE_CONSTANTS["X_INITIAL_MAX"]==1e-10
assert r27.EXPECTED_CORE_CONSTANTS["SPATIAL_MAX"]==1e-10
assert r27.EXPECTED_CORE_CONSTANTS["QUAD_MAX"]==1e-2
assert r27.EXPECTED_CORE_CONSTANTS["TIME_MAX"]==5e-3
print("GE19_REPAIR27_LOCAL_PREEXECUTION_AUDIT_PASS")
PY

echo "=== GE19 Repair27 frozen local GE19 inputs ==="
for f in \
  results/ge19_repair22_on_shell_parent_z20_certification.json \
  results/ge19_repair22_on_shell_parent_z20_certification.npz \
  results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.json \
  results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz \
  results/ge15_R1_dense_accepted_step_trace.dat \
  results/ge15_R1_cli_background.dat
do
  test -s "$f" || { echo "MISSING=$f"; exit 4; }
done

test "$(sha256sum results/ge19_repair22_on_shell_parent_z20_certification.json | awk '{print $1}')" = \
  "7d53b2458183c6b2cc326acdded70b2c3ce1fab959d8456e56d3b4f1f86ef374"
test "$(sha256sum results/ge19_repair22_on_shell_parent_z20_certification.npz | awk '{print $1}')" = \
  "3020e0d040f902ab2609e05705f4508d9919665b1344fa0e641644ea8fc41a16"
test "$(sha256sum results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.json | awk '{print $1}')" = \
  "ae3cc790ecffbd5498b5852273c72ae578d4615de29bbb616673c05cdb3e74b7"
test "$(sha256sum results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz | awk '{print $1}')" = \
  "011c0ae54fd21d70c0e2c695ce62e7b74a3c5529a07c9023c882a447d5b40ca3"
test "$(sha256sum results/ge15_R1_dense_accepted_step_trace.dat | awk '{print $1}')" = \
  "7f57ab676f2a31cf0abf93ff0f8b0f1f2f80bb9a58d7cf1e47e10a158c57c69f"

echo "GE19_REPAIR27_GE19_INPUTS_PASS"

echo "=== GE19 Repair27 frozen Repair26 R1 artifact ==="
ARTROOT="$ROOT/frozen_repair26_repair27"
TRACE="$(find "$ARTROOT" -type f -name ge19_repair26_R1_full_history_trace.dat -print -quit 2>/dev/null || true)"

if [[ -z "$TRACE" ]]; then
  command -v gh >/dev/null 2>&1 || {
    echo "GE19_REPAIR27_GH_NOT_AVAILABLE"
    echo "Install/authenticate GitHub CLI or place artifact 10690709843 under $ARTROOT"
    exit 6
  }
  rm -rf "$ARTROOT"
  mkdir -p "$ARTROOT"
  gh run download 35721220889 \
    --repo dvlahek/aest-memory-gravity \
    --name results_bundle_ge19_repair26_cancellation_free_full_history_bath_boundary \
    --dir "$ARTROOT"
  TRACE="$(find "$ARTROOT" -type f -name ge19_repair26_R1_full_history_trace.dat -print -quit)"
fi

test -n "$TRACE"
test -s "$TRACE"
test "$(sha256sum "$TRACE" | awk '{print $1}')" = \
  "608ee0b4c868a701db6976f756b9a551cd9ddffe1e8e4ab37c5cd2361405a6f8"
test "$(wc -c < "$TRACE" | tr -d ' ')" = "26643162"

echo "TRACE=$TRACE"
echo "GE19_REPAIR27_REPAIR26_PARENT_PASS"

rm -f \
  results/ge19_repair27_cancellation_free_parent_q20_reconstruction.json \
  results/ge19_repair27_cancellation_free_parent_q20_reconstruction.npz \
  results/ge19_repair27_cancellation_free_parent_q20_reconstruction_FULL.log

echo "=== GE19 Repair27 q20 science execution ==="
set +e
set -o pipefail
python3 ge19/repair27_cancellation_free_parent_q20_reconstruction.py \
  --results-dir results \
  --repair26-trace "$TRACE" \
  --json-out results/ge19_repair27_cancellation_free_parent_q20_reconstruction.json \
  --npz-out results/ge19_repair27_cancellation_free_parent_q20_reconstruction.npz \
  2>&1 | tee results/ge19_repair27_cancellation_free_parent_q20_reconstruction_FULL.log
SCIENCE_EXIT=${PIPESTATUS[0]}
set -e

echo "=== GE19 Repair27 summary ==="
if [[ -s results/ge19_repair27_cancellation_free_parent_q20_reconstruction.json ]]; then
python3 - <<'PY'
import hashlib,json
from pathlib import Path

p=Path("results/ge19_repair27_cancellation_free_parent_q20_reconstruction.json")
d=json.loads(p.read_text())
print("CLASSIFICATION =",d["classification"])
print("ROUTE =",d["routing"]["next_route"])
print("Q20_RERUN_PERFORMED =",d["q20_rerun_performed"])
print("Q20_CONSTRUCTED =",d["q20_constructed"])
print("Q20_CERTIFIED_PROJECTION =",d["q20_certified_projection"])
print("H4_Z21_LICENSED =",d["H4_Z21_construction_licensed_after_result_freeze"])
print("PARENT_CHANGE =",d["parent_change"])
print("FULL_HISTORY_BOUNDARY =",d["full_history_boundary"])
print("CONTROLS =",d["controls"])
print("GATES =",d["gates"])
print("CLAIM_BOUNDARY =",d["claim_boundary"])

for fn in [
  "results/ge19_repair27_cancellation_free_parent_q20_reconstruction.json",
  "results/ge19_repair27_cancellation_free_parent_q20_reconstruction.npz",
  "results/ge19_repair27_cancellation_free_parent_q20_reconstruction_FULL.log",
]:
    q=Path(fn)
    if q.exists():
        print("SHA256",fn,hashlib.sha256(q.read_bytes()).hexdigest(),"BYTES",q.stat().st_size)
PY
fi

echo "GE19_REPAIR27_SCIENCE_EXIT=$SCIENCE_EXIT"
if [[ "$SCIENCE_EXIT" -eq 0 ]]; then
  echo "GE19_REPAIR27_EXECUTION_COMPLETE"
elif [[ "$SCIENCE_EXIT" -eq 2 ]]; then
  echo "GE19_REPAIR27_VALID_SCIENCE_FAIL_FREEZE_REQUIRED"
else
  echo "GE19_REPAIR27_IMPLEMENTATION_OR_EXECUTION_FAILURE"
fi
exit "$SCIENCE_EXIT"
