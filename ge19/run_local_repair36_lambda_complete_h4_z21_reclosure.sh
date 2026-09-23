#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results

test "$(git rev-parse HEAD:ge19/repair36_predata_lambda_complete_h4_z21_reclosure.json)" = "89ec97f3b3e92d1077c9faf174a308ea73dce339"
test "$(git rev-parse HEAD:ge19/repair36_lambda_complete_h4_z21_reclosure.py)" = "cf2caafd5ae2399cd3e6f6db7716aece20e8bb6c"
test "$(git rev-parse HEAD:.github/workflows/ge19-repair36-prelock-audit.yml)" = "7d268babcf468ba1e150bc8030cb3f6d0df428c4"
test "$(git rev-parse HEAD:docs/ge19_repair35_h4_z21_valid_fail_lambda_omission_freeze.md)" = "578510ab2cf270edc518f0cbbe90c8e0ef50f4cd"
test "$(git rev-parse HEAD:docs/ge19_repair36_lambda_complete_h4_implementation_lock.md)" = "7aaa8ca967935d3a6c12b1aef2c938da00a1e91d"

for c in   73dd25c9512256100e5a2e6391cd6d5cea822117   fa5f6766bdc4df5f05147a57de292638a90af998   6b12114ff89be6b954f2dbcb5c09e0424e666a0c   f4b949166deb0830d219913d334964636f3646f0   e3c60d0ac76a2c9cfcd3d0fe3c641136a421bb4a
do
  git merge-base --is-ancestor "$c" HEAD
done
echo GE19_REPAIR36_LOCK_PASS

if [[ -z "${VIRTUAL_ENV:-}" ]]; then
  echo GE19_REPAIR36_VENV_NOT_ACTIVE
  echo "Run: source .venv/bin/activate"
  exit 5
fi

python3 -m py_compile ge19/repair36_lambda_complete_h4_z21_reclosure.py
python3 ge19/repair36_lambda_complete_h4_z21_reclosure.py --help >/tmp/r36_help.txt
grep -q -- "--repair26-trace" /tmp/r36_help.txt
echo GE19_REPAIR36_LOCAL_PREEXECUTION_AUDIT_PASS

declare -A HASHES
HASHES["results/ge15_R1_dense_accepted_step_trace.dat"]="7f57ab676f2a31cf0abf93ff0f8b0f1f2f80bb9a58d7cf1e47e10a158c57c69f"
HASHES["results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz"]="011c0ae54fd21d70c0e2c695ce62e7b74a3c5529a07c9023c882a447d5b40ca3"
HASHES["results/ge19_repair22_on_shell_parent_z20_certification.json"]="7d53b2458183c6b2cc326acdded70b2c3ce1fab959d8456e56d3b4f1f86ef374"
HASHES["results/ge19_repair22_on_shell_parent_z20_certification.npz"]="3020e0d040f902ab2609e05705f4508d9919665b1344fa0e641644ea8fc41a16"
HASHES["results/ge19_repair27_cancellation_free_parent_q20_reconstruction.json"]="99a2183e7088c7492f624cae2d294612380714c1d81aa7ff49cc4fcd1c62c74b"
HASHES["results/ge19_repair27_cancellation_free_parent_q20_reconstruction.npz"]="2b1566d402e4c9e8daee8e5c7084b3da7735442b4fb604d51489b708662fd9c0"
HASHES["results/ge19_repair32b_factor2_corrected_reduced_h2_z11_reconstruction.json"]="226dd2a2a0e86ddccc39a62d833960bdf9d5a9af038ad3bf225bbbf69d0b95cf"
HASHES["results/ge19_repair32b_factor2_corrected_reduced_h2_z11_reconstruction.npz"]="5d4a0a72c08d09d096a8de0b428b3c8443fc33e8ad442ed6d997d6bf2bc6e327"
HASHES["results/ge19_repair32c_artifact_only_reduced_z11_certification.json"]="037314effa33c5bfaf51f6f3c72459de43cb486c6ef5e9a94f5b1984a68611b9"

for f in "${!HASHES[@]}"; do
  if [[ ! -f "$f" ]]; then
    echo "GE19_REPAIR36_MISSING_LOCAL_PARENT: $f"
    exit 6
  fi
  got="$(sha256sum "$f" | awk '{print $1}')"
  test "$got" = "${HASHES[$f]}"
done
echo GE19_REPAIR36_LOCAL_PARENTS_PASS

ARTROOT="$ROOT/frozen_repair26_repair36"
TRACE="$(find "$ARTROOT" -type f -name ge19_repair26_R1_full_history_trace.dat -print -quit 2>/dev/null || true)"
if [[ -z "$TRACE" ]]; then
  command -v gh >/dev/null 2>&1 || {
    echo "GE19_REPAIR36_GH_NOT_AVAILABLE"
    exit 7
  }
  rm -rf "$ARTROOT"
  mkdir -p "$ARTROOT"
  gh run download 35721220889     --repo dvlahek/aest-memory-gravity     --name results_bundle_ge19_repair26_cancellation_free_full_history_bath_boundary     --dir "$ARTROOT"
  TRACE="$(find "$ARTROOT" -type f -name ge19_repair26_R1_full_history_trace.dat -print -quit)"
fi

test -n "$TRACE"
test -s "$TRACE"
test "$(sha256sum "$TRACE" | awk '{print $1}')" = "608ee0b4c868a701db6976f756b9a551cd9ddffe1e8e4ab37c5cd2361405a6f8"
test "$(wc -c < "$TRACE" | tr -d ' ')" = "26643162"
echo "TRACE=$TRACE"
echo GE19_REPAIR36_REPAIR26_TRACE_PASS

JSON="results/ge19_repair36_lambda_complete_h4_z21_reclosure.json"
NPZ="results/ge19_repair36_lambda_complete_h4_z21_reclosure.npz"
FULL="results/ge19_repair36_lambda_complete_h4_z21_reclosure_FULL.log"
rm -f "$JSON" "$NPZ" "$FULL"

set +e
python3 ge19/repair36_lambda_complete_h4_z21_reclosure.py   --results-dir results   --repair26-trace "$TRACE"   --json-out "$JSON"   --npz-out "$NPZ"   2>&1 | tee "$FULL"
rc=${PIPESTATUS[0]}
set -e

if [[ -s "$JSON" ]]; then
python3 - <<'PY'
import json
d=json.load(open("results/ge19_repair36_lambda_complete_h4_z21_reclosure.json"))
print("CLASSIFICATION =",d["classification"])
print("Z21_CERTIFIED =",d["Z21_window_local_particular_certified"])
print("PRIMORDIAL_Z21_CERTIFIED =",d["primordial_homogeneous_Z21_certified"])
print("FULL_SPECIES_Z21_CERTIFIED =",d["full_species_Z21_certified"])
print("ROUTE =",d["routing"]["next_route"])
print("SOURCE_CONTROLS =",d["source_controls"])
print("LAMBDA_OPERATOR =",d["solve_controls"]["Lambda_operator"])
print("MATCHED_SHIFT =",d["solve_controls"]["matched_shift"])
print("GATES =",d["gates"])
PY
fi

for f in "$JSON" "$NPZ" "$FULL"; do
  if [[ -f "$f" ]]; then
    sha256sum "$f"
    wc -c "$f"
  fi
done

if [[ "$rc" -eq 0 ]]; then
  echo GE19_REPAIR36_EXECUTION_COMPLETE
elif [[ "$rc" -eq 2 && -s "$JSON" ]]; then
  echo GE19_REPAIR36_VALID_SCIENCE_FAIL_FREEZE_REQUIRED
else
  echo GE19_REPAIR36_IMPLEMENTATION_OR_EXECUTION_FAILURE
fi
exit "$rc"
