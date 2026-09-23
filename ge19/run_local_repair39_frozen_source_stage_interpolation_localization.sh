#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results

test "$(git rev-parse HEAD:ge19/repair39_predata_frozen_source_stage_interpolation_localization.json)" = "7f289263768e0eb1e3a9af47ecc6b10f71f0065a"
test "$(git rev-parse HEAD:ge19/repair39_frozen_source_stage_interpolation_localization.py)" = "91e65251198983205394196893b862f08dd2a585"
test "$(git rev-parse HEAD:.github/workflows/ge19-repair39-prelock-audit.yml)" = "2470783b6cd3307c8d03922ebe9391cc82ebbd6b"
test "$(git rev-parse HEAD:docs/ge19_repair38_valid_diagnostic_pchip_or_other_floor_freeze.md)" = "040af5dcb90070d05e3ab7e98623a4e03aa25009"
test "$(git rev-parse HEAD:docs/ge19_repair39_stage_interpolation_implementation_lock.md)" = "a1c2f6d97d06c46a460c38c3327b772e732156d9"

for c in   ada593c99c7bc217313b1f7c8ff99504f13e8d10   87aff396a2a8505b50001a1a5169a3167477e1f7   0ae58cc9c71c7afac85654b30a85162d27d79f4f   9bcfdd4d9d93d7739079c3034bc7b9fe7dd32ac0   6e7f21073978a2c866bd467ed32e8a5fc39200d9
do
  git merge-base --is-ancestor "$c" HEAD
done
echo GE19_REPAIR39_LOCK_PASS

if [[ -z "${VIRTUAL_ENV:-}" ]]; then
  echo GE19_REPAIR39_VENV_NOT_ACTIVE
  echo "Run: source .venv/bin/activate"
  exit 5
fi

python3 -m py_compile ge19/repair39_frozen_source_stage_interpolation_localization.py
python3 ge19/repair39_frozen_source_stage_interpolation_localization.py --help >/tmp/r39_help.txt
grep -q -- "--results-dir" /tmp/r39_help.txt
grep -q -- "--json-out" /tmp/r39_help.txt
grep -q -- "--npz-out" /tmp/r39_help.txt
echo GE19_REPAIR39_LOCAL_PREEXECUTION_AUDIT_PASS

declare -A HASHES
HASHES["results/ge19_repair38_frozen_source_radau_substep_localization.json"]="08dd95c614118c66e37349e2b8d058e85163812fed77c9b048e0ce57e339e5dd"
HASHES["results/ge19_repair38_frozen_source_radau_substep_localization.npz"]="aff63771c1800b0db236cd020cf0d2772f6d9a0fd0328573d055392f2c60da67"
HASHES["results/ge19_repair37_cancellation_safe_fd8_h4_z21_reclosure.json"]="da8f2f00c22c866ec3f82381d23f69bf036e630fe2a29c5c44657984b760f61a"
HASHES["results/ge19_repair37_cancellation_safe_fd8_h4_z21_reclosure.npz"]="572d8937c1d742b10da66e34cc076377c1b2feb20b8f72eb25c3eaf31a59829f"
HASHES["results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz"]="011c0ae54fd21d70c0e2c695ce62e7b74a3c5529a07c9023c882a447d5b40ca3"
HASHES["results/ge15_R1_dense_accepted_step_trace.dat"]="7f57ab676f2a31cf0abf93ff0f8b0f1f2f80bb9a58d7cf1e47e10a158c57c69f"

for f in "${!HASHES[@]}"; do
  if [[ ! -f "$f" ]]; then
    echo "GE19_REPAIR39_MISSING_LOCAL_INPUT: $f"
    exit 6
  fi
  got="$(sha256sum "$f" | awk '{print $1}')"
  test "$got" = "${HASHES[$f]}"
done

test -s results/ge15_R1_cli_background.dat
echo GE19_REPAIR39_FROZEN_INPUTS_PASS

JSON="results/ge19_repair39_frozen_source_stage_interpolation_localization.json"
NPZ="results/ge19_repair39_frozen_source_stage_interpolation_localization.npz"
FULL="results/ge19_repair39_frozen_source_stage_interpolation_localization_FULL.log"
rm -f "$JSON" "$NPZ" "$FULL"

set +e
python3 ge19/repair39_frozen_source_stage_interpolation_localization.py   --results-dir results   --json-out "$JSON"   --npz-out "$NPZ"   2>&1 | tee "$FULL"
rc=${PIPESTATUS[0]}
set -e

if [[ -s "$JSON" ]]; then
python3 - <<'PY'
import json
d=json.load(open("results/ge19_repair39_frozen_source_stage_interpolation_localization.json"))
print("CLASSIFICATION =",d["classification"])
print("ROUTE =",d["routing"]["next_route"])
print("PCHIP_REPRO =",d["PCHIP_baseline_reproduction"])
print("NODAL =",d["nodal_interpolation_control"])
print("PCHIP =",d["method_results"]["PCHIP"])
print("CUBIC_SPLINE =",d["method_results"]["CUBIC_SPLINE"])
print("AKIMA =",d["method_results"]["AKIMA"])
print("REFERENCE =",d["diagnostic_reference_scale"])
print("SENSITIVITY =",d["representation_sensitivity"])
print("IMPLEMENTATION_GATES =",d["implementation_gates"])
print("Z21_CERTIFIED =",d["Z21_window_local_particular_certified"])
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
  echo GE19_REPAIR39_DIAGNOSTIC_COMPLETE
elif [[ "$rc" -eq 3 && -s "$JSON" ]]; then
  echo GE19_REPAIR39_IMPLEMENTATION_REPRODUCTION_FAIL
else
  echo GE19_REPAIR39_IMPLEMENTATION_OR_EXECUTION_FAILURE
fi
exit "$rc"
