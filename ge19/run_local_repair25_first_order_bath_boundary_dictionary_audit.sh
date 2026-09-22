#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results

echo "=== GE19 Repair25 lock audit ==="

test "$(git rev-parse HEAD:docs/ge19_repair24_q20_construction_result_freeze.md)" = "3edde5ac2b751ce78bc42de5a6843934804f9b68"
test "$(git rev-parse HEAD:docs/ge19_repair22_z20_certification_result_freeze.md)" = "fb4ef607d17b5545985edf557aa67d02bc4dff0f"
test "$(git rev-parse HEAD:docs/ge15_cancellation_free_s_state_precision_closure_local_result_freeze.md)" = "84511c8d40be8a7dad38ad0f3648c81309a559b4"
test "$(git rev-parse HEAD:ge19/repair25_predata_first_order_bath_boundary_dictionary_audit.json)" = "1e7f25eba5a4c8b297b563edfe6f9c4f276ec6c9"
test "$(git rev-parse HEAD:ge19/repair25_amendment01_complete_boundary_dictionary_diagnostics.json)" = "23c85b181fdb095e7c91d2601cee251878b57b5c"
test "$(git rev-parse HEAD:ge19/repair25_first_order_bath_boundary_dictionary_audit.py)" = "1827b1a03268964043be9f7b13fdc704f54d4d05"
test "$(git rev-parse HEAD:.github/workflows/ge19-repair25-prelock-audit.yml)" = "2c5e5b94cffc040df09dd1af676834b2291cda19"
test "$(git rev-parse HEAD:docs/ge19_repair25_amendment01_complete_boundary_dictionary_diagnostics_implementation_lock.md)" = "d3317e75d88e7c083644d38a1394f6f5c09ba9ce"
test "$(git rev-parse HEAD:ge19/repair07_window_retarded_reduced_h3_z20_particular.py)" = "e34d28a2062c748f48bc82fa928844b02631de25"
test "$(git rev-parse HEAD:ge19/repair11_lambda_inclusive_reduced_h1_reclosure.py)" = "dbfa43ae11dbd3cfeeb1994a30237e9374dbb3e7"
test "$(git rev-parse HEAD:ge19/repair13_self_consistent_reduced_background_h1_reclosure.py)" = "362d63d03d7b850fceae393f535353ded79aeea7"
test "$(git rev-parse HEAD:ge09/repair01_dense_accepted_step_local_jet_bridge.py)" = "509fa9d7bb323034bbf77b26792f35e1cc2ff7c7"
test "$(git rev-parse HEAD:nl1c4/expanding_memory_source_trajectory.py)" = "7a9ffab9fa903ca61e88627052e2aa589b4bf459"

for sha in \
  82f1f56912f92e628797997d82ffd64de2a4a926 \
  d02245e5f23ece8fda49c10ede70caf453fd9976 \
  99d5ab968020d59de72ca588711946edf1d82975 \
  c63f3bd8ddf6da3619e8a955e38aa1da970a4efd \
  72d03f4d15d6d0549f68df5d7ee9c0f7f541c82f \
  1f97e4f08ad40abc1623ec529a41bbca1531dcaa \
  996ad5a0ac8e27e102f766bff52df46417d327a0
do
  git merge-base --is-ancestor "$sha" HEAD
done

echo "GE19_REPAIR25_LOCK_PASS"

if [[ -z "${VIRTUAL_ENV:-}" ]]; then
  echo "GE19_REPAIR25_VENV_NOT_ACTIVE"
  echo "Run: source .venv/bin/activate"
  exit 5
fi

python3 -m py_compile ge19/repair25_first_order_bath_boundary_dictionary_audit.py

echo "=== GE19 Repair25 frozen local inputs ==="
for f in \
  results/ge19_repair24_q20_construction.json \
  results/ge19_repair22_on_shell_parent_z20_certification.json \
  results/ge19_repair22_on_shell_parent_z20_certification.npz \
  results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.json \
  results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz \
  results/ge15_cancellation_free_s_state_precision_closure.json \
  results/ge15_R1_dense_accepted_step_trace.dat \
  results/ge15_R1_cli_background.dat
do
  test -s "$f" || { echo "MISSING=$f"; exit 4; }
done

test "$(sha256sum results/ge19_repair24_q20_construction.json | awk '{print $1}')" = \
  "71f463524b47f72d2c5082667fe99141d2286ebc2938c4eed6b89a1583339f2a"
test "$(sha256sum results/ge19_repair22_on_shell_parent_z20_certification.json | awk '{print $1}')" = \
  "7d53b2458183c6b2cc326acdded70b2c3ce1fab959d8456e56d3b4f1f86ef374"
test "$(sha256sum results/ge19_repair22_on_shell_parent_z20_certification.npz | awk '{print $1}')" = \
  "3020e0d040f902ab2609e05705f4508d9919665b1344fa0e641644ea8fc41a16"
test "$(sha256sum results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.json | awk '{print $1}')" = \
  "ae3cc790ecffbd5498b5852273c72ae578d4615de29bbb616673c05cdb3e74b7"
test "$(sha256sum results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz | awk '{print $1}')" = \
  "011c0ae54fd21d70c0e2c695ce62e7b74a3c5529a07c9023c882a447d5b40ca3"
test "$(sha256sum results/ge15_cancellation_free_s_state_precision_closure.json | awk '{print $1}')" = \
  "5975774bf7af0f3af9acf16c8de2dbac0ca032894dc5c6879346a3e11efe84c1"

python3 - <<'PY'
import hashlib, json
from pathlib import Path

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

r24=json.load(open("results/ge19_repair24_q20_construction.json"))
assert r24["classification"]=="GE19_REPAIR24_Q20_CONSTRUCTION_FAIL"
false=[k for k,v in r24["gates"].items() if not bool(v)]
assert false==["H1_X10_initial_match_abs_or_rel_le_1e10"],false

ge15=json.load(open("results/ge15_cancellation_free_s_state_precision_closure.json"))
assert ge15["classification"]=="GE15_CANCELLATION_FREE_S_STATE_PRECISION_CLOSURE_PASS"
expected=ge15["precision_binding"]["dense_trace_sha256"]["R1"]
got=sha("results/ge15_R1_dense_accepted_step_trace.dat")
assert got==expected,(got,expected)

r22=json.load(open("results/ge19_repair22_on_shell_parent_z20_certification.json"))
assert r22["classification"]=="GE19_REPAIR22_ON_SHELL_PARENT_Z20_CERTIFICATION_PASS"
assert r22["Z20_certified"] is True

r13=json.load(open("results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.json"))
assert r13["stage_A_pass"] is True

print("GE19_REPAIR25_LOCAL_PARENT_INPUTS_PASS")
print("GE15_R1_DENSE_SHA =",got)
PY

echo "=== GE19 Repair25 frozen v0.77 artifact ==="
TRACE=""
for ARTROOT in "$ROOT/frozen_v077_repair24" "$ROOT/frozen_v077_repair25"; do
  if [[ -d "$ARTROOT" ]]; then
    TRACE="$(find "$ARTROOT" -type f -name v076_v077_base_trace.dat -print -quit 2>/dev/null || true)"
    [[ -n "$TRACE" ]] && break
  fi
done

if [[ -z "$TRACE" ]]; then
  command -v gh >/dev/null 2>&1 || {
    echo "GE19_REPAIR25_GH_NOT_AVAILABLE"
    echo "Install/authenticate GitHub CLI or place artifact 10090367181 under frozen_v077_repair25"
    exit 6
  }
  ARTROOT="$ROOT/frozen_v077_repair25"
  rm -rf "$ARTROOT"
  mkdir -p "$ARTROOT"
  gh run download 34315590099 \
    --repo dvlahek/aest-memory-gravity \
    --name results_bundle_v077_native_state_tangent_affinity \
    --dir "$ARTROOT"
  TRACE="$(find "$ARTROOT" -type f -name v076_v077_base_trace.dat -print -quit)"
fi

test -n "$TRACE"
test -s "$TRACE"
test "$(sha256sum "$TRACE" | awk '{print $1}')" = \
  "98c8468e8ccdf902cad8d6e65f3852e863c6fd19df62ece61353ab725ac5a43e"
test "$(wc -c < "$TRACE" | tr -d ' ')" = "2657188"

echo "TRACE=$TRACE"
echo "GE19_REPAIR25_V077_INPUT_PASS"

OUT="results/ge19_repair25_first_order_bath_boundary_dictionary_audit.json"
LOG="results/ge19_repair25_first_order_bath_boundary_dictionary_audit_FULL.log"
rm -f "$OUT" "$LOG"

echo "=== GE19 Repair25 diagnostic science execution ==="
set +e
set -o pipefail
python3 ge19/repair25_first_order_bath_boundary_dictionary_audit.py \
  --results-dir results \
  --v077-trace "$TRACE" \
  --json-out "$OUT" \
  2>&1 | tee "$LOG"
SCIENCE_EXIT=${PIPESTATUS[0]}
set -e

echo "=== GE19 Repair25 summary ==="
if [[ -s "$OUT" ]]; then
python3 - <<'PY'
import json
d=json.load(open("results/ge19_repair25_first_order_bath_boundary_dictionary_audit.json"))
print("CLASSIFICATION =",d["classification"])
print("NEXT_ROUTE =",d["routing"]["next_route"])
print("Q20_RERUN_PERFORMED =",d["q20_rerun_performed"])
print("Z21_LICENSED =",d["Z21_licensed"])
print("EXACT_SURFACE =",d["exact_surface"])
print("OVERLAP_GLOBAL =",{
    k:v for k,v in d["overlap_window"].items()
    if k not in ("per_mode","candidate_factor_audits")
})
print("PER_MODE_OVERLAP =")
for row in d["overlap_window"]["per_mode"]:
    print(row)
print("CANDIDATE_FACTOR_AUDITS =")
for k,v in d["overlap_window"]["candidate_factor_audits"].items():
    print(k,v)
print("FROZEN_THRESHOLD_CHECKS =",d["frozen_threshold_checks"])
print("DIAGNOSTIC_AMENDMENT01 =",d["diagnostic_amendment01"])
PY
fi

echo "=== GE19 Repair25 artifact hashes ==="
echo "RUNNER_SHA256=$(sha256sum "$0" | awk '{print $1}')"
echo "RUNNER_BYTES=$(wc -c < "$0" | tr -d ' ')"
if [[ -s "$OUT" ]]; then
  sha256sum "$OUT"
  wc -c "$OUT"
fi
if [[ -s "$LOG" ]]; then
  sha256sum "$LOG"
  wc -c "$LOG"
fi

echo "SCIENCE_EXIT=$SCIENCE_EXIT"
exit "$SCIENCE_EXIT"
