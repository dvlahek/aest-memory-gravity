#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results

test "$(git rev-parse HEAD:ge19/repair42_predata_direct_target_h4_propagation_diagnostic.json)" = "cbdb7b66e57a24c44fb03c0856ffdc1977303844"
test "$(git rev-parse HEAD:ge19/repair42_direct_target_h4_propagation_diagnostic.py)" = "8576118fec60dd6ac1593459da9354d424d04fd5"
test "$(git rev-parse HEAD:.github/workflows/ge19-repair42-prelock-audit.yml)" = "ece1e7ca5522b71ad92f045bf7cc6cefbd896080"
test "$(git rev-parse HEAD:docs/ge19_repair41_valid_direct_fine_grid_target_reference_freeze.md)" = "cfbc013969a6572c52c5d8d3d090355755b81ee2"
test "$(git rev-parse HEAD:docs/ge19_repair42_direct_target_h4_implementation_lock.md)" = "d79c5ac42e828cf1d2bbd4308f57792b3bc80986"

for c in   1e1ffa694eb9661be72907f59b1de317d87f713d   8aa14dffd3d508bcc4920b9cb68ff520a4d2520d   e2634cfe7be0eb5590305ae55197d483dbd9818f   a7303cb29ec0929c8e2d00350804af70856a60fb   b6ebbd5e896b37c7f0591bedb18734cc7ba47d79
do
  git merge-base --is-ancestor "$c" HEAD
done
echo GE19_REPAIR42_LOCK_PASS

if [[ -z "${VIRTUAL_ENV:-}" ]]; then
  echo GE19_REPAIR42_VENV_NOT_ACTIVE
  echo "Run: source .venv/bin/activate"
  exit 5
fi

python3 -m py_compile ge19/repair42_direct_target_h4_propagation_diagnostic.py
python3 ge19/repair42_direct_target_h4_propagation_diagnostic.py --help >/tmp/r42_help.txt
grep -q -- "--results-dir" /tmp/r42_help.txt
grep -q -- "--json-out" /tmp/r42_help.txt
grep -q -- "--npz-out" /tmp/r42_help.txt
echo GE19_REPAIR42_LOCAL_PREEXECUTION_AUDIT_PASS

declare -A HASHES
HASHES["results/ge19_repair41_direct_fine_grid_target_source_reconstruction.json"]="1b18fede26b021e077ffe5c8b6b7ff0dc727b4defaab48e63491c86d868d1320"
HASHES["results/ge19_repair41_direct_fine_grid_target_source_reconstruction.npz"]="6bfb87ea21d55e2a1d2b16aee9bc8d7246111f91a064a78b74d2ed946ec2ba45"
HASHES["results/ge19_repair37_cancellation_safe_fd8_h4_z21_reclosure.json"]="da8f2f00c22c866ec3f82381d23f69bf036e630fe2a29c5c44657984b760f61a"
HASHES["results/ge19_repair37_cancellation_safe_fd8_h4_z21_reclosure.npz"]="572d8937c1d742b10da66e34cc076377c1b2feb20b8f72eb25c3eaf31a59829f"
HASHES["results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz"]="011c0ae54fd21d70c0e2c695ce62e7b74a3c5529a07c9023c882a447d5b40ca3"
HASHES["results/ge15_R1_dense_accepted_step_trace.dat"]="7f57ab676f2a31cf0abf93ff0f8b0f1f2f80bb9a58d7cf1e47e10a158c57c69f"

for f in "${!HASHES[@]}"; do
  if [[ ! -f "$f" ]]; then
    echo "GE19_REPAIR42_MISSING_LOCAL_INPUT: $f"
    exit 6
  fi
  got="$(sha256sum "$f" | awk '{print $1}')"
  test "$got" = "${HASHES[$f]}"
done
test -s results/ge15_R1_cli_background.dat
echo GE19_REPAIR42_FROZEN_INPUTS_PASS

JSON="results/ge19_repair42_direct_target_h4_propagation_diagnostic.json"
NPZ="results/ge19_repair42_direct_target_h4_propagation_diagnostic.npz"
FULL="results/ge19_repair42_direct_target_h4_propagation_diagnostic_FULL.log"
rm -f "$JSON" "$NPZ" "$FULL"

set +e
python3 ge19/repair42_direct_target_h4_propagation_diagnostic.py   --results-dir results   --json-out "$JSON"   --npz-out "$NPZ"   2>&1 | tee "$FULL"
rc=${PIPESTATUS[0]}
set -e

if [[ -s "$JSON" ]]; then
python3 - <<'PY'
import json
d=json.load(open("results/ge19_repair42_direct_target_h4_propagation_diagnostic.json"))
print("CLASSIFICATION =",d["classification"])
print("ROUTE =",d["routing"]["next_route"])
print("SOURCE_BINDING =",d["source_binding_controls"])
print("BASELINE_REPRO =",d["baseline_reproduction"])
print("VARIANTS:")
for k,v in d["variant_results"].items():
    print(" ",k,"=",v)
print("DIRECT_DELTA =",d["direct_delta_response_report_only"])
print("382_VS_763 =",d["direct382_vs_direct763_report_only"])
print("IMPLEMENTATION_GATES =",d["implementation_gates"])
print("Z21_CERTIFIED =",d["Z21_window_local_particular_certified"])
print("SCIENCE_RECLOSURE =",d["science_H4_Z21_reclosure_performed"])
print("LENSING_LICENSED =",d["lensing_licensed"])
PY
fi

for f in "$JSON" "$NPZ" "$FULL"; do
  if [[ -f "$f" ]]; then
    sha256sum "$f"
    wc -c "$f"
  fi
done

if [[ "$rc" -eq 0 && -s "$JSON" ]]; then
  echo GE19_REPAIR42_DIAGNOSTIC_COMPLETE
elif [[ "$rc" -eq 3 && -s "$JSON" ]]; then
  echo GE19_REPAIR42_IMPLEMENTATION_REPRODUCTION_FAIL
else
  echo GE19_REPAIR42_IMPLEMENTATION_OR_EXECUTION_FAILURE
fi
exit "$rc"
