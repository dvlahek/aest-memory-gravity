#!/usr/bin/env bash
# First actual corrected-parent H4F3b six-source calculation.
# This runner NEVER executes a Z21 solve or overwrites Repair37 results.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results
test "$(git rev-parse HEAD:ge19/h4f3b_predata_actual_corrected_six_piece_source.json)" = "c3362f5360c2a9951d77060027c82830c031c145"
test "$(git rev-parse HEAD:ge19/h4f3b_actual_corrected_six_piece_source.py)" = "0423cbc64f6cda3b2a9aeb67c734935ef3ae7f9c"
test "$(git rev-parse HEAD:ge19/h4f3_predata_integrated_corrected_parent_ward.json)" = "3e17163cb6f52f3a78c41e6f37f83ef682359162"
test "$(git rev-parse HEAD:ge19/repair37_cancellation_safe_fd8_h4_z21_reclosure.py)" = "45d203a092f9ac71cc612b15df5f0c0c630f5898"
test "$(git rev-parse HEAD:ge19/h4f2g_action_completed_six_piece_source_ledger.py)" = "d9778da0bb6cc52a15015238810c79978527ffc5"
test "$(git rev-parse HEAD:ge19/h4f2h_physical_time_source_ward_bridge.py)" = "65ce1e68a2f77e063c4bb8848d770abb4baeeebf"
for p in \
  ge19/h4f3b_predata_actual_corrected_six_piece_source.json \
  ge19/h4f3b_actual_corrected_six_piece_source.py \
  ge19/repair37_cancellation_safe_fd8_h4_z21_reclosure.py \
  ge19/h4f2g_action_completed_six_piece_source_ledger.py \
  ge19/h4f2h_physical_time_source_ward_bridge.py
do
  git diff --quiet -- "$p"
  git diff --cached --quiet -- "$p"
done
echo GE19_H4F3B_LOCAL_SOURCE_LOCK_PASS

if [[ -z "${VIRTUAL_ENV:-}" ]]; then
  echo "Activate the scientific venv: source .venv/bin/activate"
  exit 5
fi
python3 -c 'import numpy, scipy, sympy'
python3 -m py_compile ge19/h4f3b_actual_corrected_six_piece_source.py

TRACE=""
if [[ -d "$ROOT/frozen_repair26_repair27" ]]; then
  TRACE="$(find "$ROOT/frozen_repair26_repair27" -type f -name ge19_repair26_R1_full_history_trace.dat -print -quit)"
fi
if [[ -z "$TRACE" ]]; then
  if ! command -v gh >/dev/null 2>&1; then
    echo "Missing frozen Repair26 R1 trace. Run H3G frozen-artifact download or install/authenticate gh."
    exit 6
  fi
  mkdir -p "$ROOT/frozen_repair26_repair27"
  gh run download 35721220889 \
    --repo dvlahek/aest-memory-gravity \
    --name results_bundle_ge19_repair26_cancellation_free_full_history_bath_boundary \
    --dir "$ROOT/frozen_repair26_repair27"
  TRACE="$(find "$ROOT/frozen_repair26_repair27" -type f -name ge19_repair26_R1_full_history_trace.dat -print -quit)"
fi
test -n "$TRACE"
TRACE="$(realpath "$TRACE")"

export PYTHONPATH="$ROOT"
# Generators imported by old modules are executed in a disposable CWD,
# and the only persistent writes are explicitly named new H4F3b results.
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/results"
cd "$TMP"

python3 - "$ROOT/results" "$TRACE" <<'PY'
import sys
from pathlib import Path
from ge19 import h4f3b_actual_corrected_six_piece_source as s
rd=Path(sys.argv[1]);trace=Path(sys.argv[2])
checks=s.code_lock()
paths,hashes=s.frozen_inputs(rd,trace)
assert all(z["exact"] for z in checks.values())
assert all(z["exact"] for k,z in hashes.items() if k!="Repair26_R1_trace")
print("GE19_H4F3B_ACTUAL_CORRECTED_PARENT_PREEXECUTION_PASS")
print("Z11 =",paths["z11"])
print("R1_TRACE =",trace)
PY

JSON="$ROOT/results/ge19_h4f3b_actual_corrected_six_piece_source.json"
NPZ="$ROOT/results/ge19_h4f3b_actual_corrected_six_piece_source.npz"
FULL="$ROOT/results/ge19_h4f3b_actual_corrected_six_piece_source_FULL.log"
rm -f "$JSON" "$NPZ" "$FULL"

set +e
set -o pipefail
python3 -m ge19.h4f3b_actual_corrected_six_piece_source \
  --results-dir "$ROOT/results" --repair26-trace "$TRACE" \
  --json-out "$JSON" --npz-out "$NPZ" \
  2>&1 | tee "$FULL" | tail -n 35
rc=${PIPESTATUS[0]}
set -e
cd "$ROOT"

if [[ -s "$JSON" ]]; then
  python3 - <<'PY'
import json
d=json.load(open("results/ge19_h4f3b_actual_corrected_six_piece_source.json"))
print("CLASSIFICATION =",d["classification"])
print("GATES =",d["gates"])
print("FAILED_GATES =",d["failure_gates"])
print("CONTROLS =",len(d["controls"]))
print("NEXT_ROUTE =",d["next_route"])
print("FULL_H4_NOETHER_DERIVED =",d["full_all_sector_H4_Noether_derived"])
print("Z21_CERTIFIED =",d["Z21_certified"])
PY
fi
for p in "$JSON" "$NPZ" "$FULL"; do
  if [[ -s "$p" ]]; then
    sha256sum "$p"
    wc -c "$p"
  fi
done
if [[ "$rc" -eq 0 && -s "$JSON" && -s "$NPZ" ]]; then
  echo GE19_H4F3B_ACTUAL_SIX_SOURCE_PASS_FULL_WARD_OPEN
elif [[ "$rc" -eq 2 && -s "$JSON" && -s "$NPZ" ]]; then
  echo GE19_H4F3B_ACTUAL_SIX_SOURCE_SCIENCE_FAIL
else
  echo GE19_H4F3B_IMPLEMENTATION_OR_EXECUTION_FAIL
fi
exit "$rc"
