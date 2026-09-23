#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results

test "$(git rev-parse HEAD:ge19/repair40_predata_piecewise_stage_source_decomposition.json)" = "05b34db63552d8e0c6be9ee90d705770350bd567"
test "$(git rev-parse HEAD:ge19/repair40_piecewise_stage_source_decomposition.py)" = "b0cd4b29e20339d11cac83a073fb0c662094f891"
test "$(git rev-parse HEAD:.github/workflows/ge19-repair40-prelock-audit.yml)" = "de7fcb70fd6b947881c8c66a00454152e3fc8c91"
test "$(git rev-parse HEAD:docs/ge19_repair39_valid_stage_source_dependence_freeze.md)" = "1e93a0111d385fb062fb1eff2f34af6d722487e1"
test "$(git rev-parse HEAD:docs/ge19_repair40_repair01_direct_delta_closure_implementation_lock.md)" = "11c1cc0634b4452c9b641054ad8cff104dc02323"

for c in   5c6740d3ca4dbc49f148c869a2cbcca092b844cb   98faa110fd46432e93e5637c2102691c4d3d9c96   edebd3a279b0e1732c4fd59c87ea051e6f678413   972a589e3897b31dd40d2be4b703a4a2b7481a5c   7194f5543a9297794e8b2847a91dc7336b652d22 \
  4ddadecae27fde6e13009005f355e2a3c0bddff5 \
  547b9a5bb897f7d44720358af59d73716b5f7efc \
  3ed249d33c06e21502be6fe5b9be0a28e9e10550 \
  3130550544c52da1590b4727cc77392556da01c8
do
  git merge-base --is-ancestor "$c" HEAD
done
echo GE19_REPAIR40_REPAIR01_LOCK_PASS

if [[ -z "${VIRTUAL_ENV:-}" ]]; then
  echo GE19_REPAIR40_VENV_NOT_ACTIVE
  echo "Run: source .venv/bin/activate"
  exit 5
fi

python3 -m py_compile ge19/repair40_piecewise_stage_source_decomposition.py
python3 ge19/repair40_piecewise_stage_source_decomposition.py --help >/tmp/r40_help.txt
grep -q -- "--results-dir" /tmp/r40_help.txt
grep -q -- "--json-out" /tmp/r40_help.txt
grep -q -- "--npz-out" /tmp/r40_help.txt
echo GE19_REPAIR40_REPAIR01_LOCAL_PREEXECUTION_AUDIT_PASS

declare -A HASHES
HASHES["results/ge19_repair39_frozen_source_stage_interpolation_localization.json"]="b058d4acb51dd4e0b964fcccb306b7eb105466941b5e0900ae0c84a29374624e"
HASHES["results/ge19_repair39_frozen_source_stage_interpolation_localization.npz"]="0bf5b0c2f26cc06b98eab1fb326757ed409cf91c86c23e995251dfd32571c451"
HASHES["results/ge19_repair37_cancellation_safe_fd8_h4_z21_reclosure.json"]="da8f2f00c22c866ec3f82381d23f69bf036e630fe2a29c5c44657984b760f61a"
HASHES["results/ge19_repair37_cancellation_safe_fd8_h4_z21_reclosure.npz"]="572d8937c1d742b10da66e34cc076377c1b2feb20b8f72eb25c3eaf31a59829f"
HASHES["results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz"]="011c0ae54fd21d70c0e2c695ce62e7b74a3c5529a07c9023c882a447d5b40ca3"
HASHES["results/ge15_R1_dense_accepted_step_trace.dat"]="7f57ab676f2a31cf0abf93ff0f8b0f1f2f80bb9a58d7cf1e47e10a158c57c69f"

for f in "${!HASHES[@]}"; do
  if [[ ! -f "$f" ]]; then
    echo "GE19_REPAIR40_MISSING_LOCAL_INPUT: $f"
    exit 6
  fi
  got="$(sha256sum "$f" | awk '{print $1}')"
  test "$got" = "${HASHES[$f]}"
done

test -s results/ge15_R1_cli_background.dat
echo GE19_REPAIR40_REPAIR01_FROZEN_INPUTS_PASS

JSON="results/ge19_repair40_piecewise_stage_source_decomposition.json"
NPZ="results/ge19_repair40_piecewise_stage_source_decomposition.npz"
FULL="results/ge19_repair40_repair01_piecewise_stage_source_decomposition_FULL.log"
rm -f "$JSON" "$NPZ" "$FULL"

set +e
python3 ge19/repair40_piecewise_stage_source_decomposition.py   --results-dir results   --json-out "$JSON"   --npz-out "$NPZ"   2>&1 | tee "$FULL"
rc=${PIPESTATUS[0]}
set -e

if [[ -s "$JSON" ]]; then
python3 - <<'PY'
import json
d=json.load(open("results/ge19_repair40_piecewise_stage_source_decomposition.json"))
print("CLASSIFICATION =",d["classification"])
print("ROUTE =",d["routing"]["next_route"])
print("BASELINE_FULL_REPRO =",d["baseline_full_reproduction"])
print("SOURCE_DECOMPOSITION =",d["source_decomposition"])
print("BASELINE_FULL_RESULTS =",d["baseline_and_full_results"])
print("Z21_CLOSURE =",d["propagated_linear_response_closure"])
print("RANK_Z21 =",d["rankings"]["descending_Z21_response_L2"])
print("RANK_SHIFT =",d["rankings"]["descending_active_shift_metric_difference_RMS"])
print("NEXT_TARGET =",d["deterministic_next_target"])
print("IMPLEMENTATION_GATES =",d["implementation_gates"])
print("Z21_CERTIFIED =",d["Z21_window_local_particular_certified"])
print("LENSING_LICENSED =",d["lensing_licensed"])
print("COMPONENTS:")
for k,v in d["component_results"].items():
    print(" ",k,"=",v)
PY
fi

for f in "$JSON" "$NPZ" "$FULL"; do
  if [[ -f "$f" ]]; then
    sha256sum "$f"
    wc -c "$f"
  fi
done

if [[ "$rc" -eq 0 && -s "$JSON" ]]; then
  echo GE19_REPAIR40_REPAIR01_DIAGNOSTIC_COMPLETE
elif [[ "$rc" -eq 3 && -s "$JSON" ]]; then
  echo GE19_REPAIR40_REPAIR01_IMPLEMENTATION_REPRODUCTION_FAIL
else
  echo GE19_REPAIR40_REPAIR01_IMPLEMENTATION_OR_EXECUTION_FAILURE
fi
exit "$rc"
