#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results

test "$(git rev-parse HEAD:ge19/repair38_predata_frozen_source_radau_substep_localization.json)" = "41a2925cf4f705c4bf8418cbcc2cee48af4a673d"
test "$(git rev-parse HEAD:ge19/repair38_frozen_source_radau_substep_localization.py)" = "fd0c80f73f0e1b485ecb895566bef078a12ba957"
test "$(git rev-parse HEAD:.github/workflows/ge19-repair38-prelock-audit.yml)" = "dd88bc6ef75003b927869b4e900e7071368b2d23"
test "$(git rev-parse HEAD:docs/ge19_repair37_valid_fail_propagation_order_localization_freeze.md)" = "d120915221b5fc1b0860c682cb8edac876571e83"
test "$(git rev-parse HEAD:docs/ge19_repair38_frozen_source_radau_substep_implementation_lock.md)" = "00d6f1deda247c82cf0847333965acbb97b5672d"

for c in   8ef52885d33aac1f91bc75261d53ce8b3b4c54dc   a3c5ac84c7a0769f91f26fd3ead17445549bc964   7ac789069eda7af0f86ff8a7003428cc5c4d0c24   07606e314310d77cad1d04a0234997be1dc10f3a   a569565c380605717fb7360d245224a4c2ffb4e6
do
  git merge-base --is-ancestor "$c" HEAD
done
echo GE19_REPAIR38_LOCK_PASS

if [[ -z "${VIRTUAL_ENV:-}" ]]; then
  echo GE19_REPAIR38_VENV_NOT_ACTIVE
  echo "Run: source .venv/bin/activate"
  exit 5
fi

python3 -m py_compile ge19/repair38_frozen_source_radau_substep_localization.py
python3 ge19/repair38_frozen_source_radau_substep_localization.py --help >/tmp/r38_help.txt
grep -q -- "--results-dir" /tmp/r38_help.txt
grep -q -- "--json-out" /tmp/r38_help.txt
grep -q -- "--npz-out" /tmp/r38_help.txt
echo GE19_REPAIR38_LOCAL_PREEXECUTION_AUDIT_PASS

declare -A HASHES
HASHES["results/ge19_repair37_cancellation_safe_fd8_h4_z21_reclosure.json"]="da8f2f00c22c866ec3f82381d23f69bf036e630fe2a29c5c44657984b760f61a"
HASHES["results/ge19_repair37_cancellation_safe_fd8_h4_z21_reclosure.npz"]="572d8937c1d742b10da66e34cc076377c1b2feb20b8f72eb25c3eaf31a59829f"
HASHES["results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz"]="011c0ae54fd21d70c0e2c695ce62e7b74a3c5529a07c9023c882a447d5b40ca3"
HASHES["results/ge15_R1_dense_accepted_step_trace.dat"]="7f57ab676f2a31cf0abf93ff0f8b0f1f2f80bb9a58d7cf1e47e10a158c57c69f"

for f in "${!HASHES[@]}"; do
  if [[ ! -f "$f" ]]; then
    echo "GE19_REPAIR38_MISSING_LOCAL_INPUT: $f"
    exit 6
  fi
  got="$(sha256sum "$f" | awk '{print $1}')"
  test "$got" = "${HASHES[$f]}"
done

test -s results/ge15_R1_cli_background.dat
echo GE19_REPAIR38_FROZEN_INPUTS_PASS

JSON="results/ge19_repair38_frozen_source_radau_substep_localization.json"
NPZ="results/ge19_repair38_frozen_source_radau_substep_localization.npz"
FULL="results/ge19_repair38_frozen_source_radau_substep_localization_FULL.log"
rm -f "$JSON" "$NPZ" "$FULL"

set +e
python3 ge19/repair38_frozen_source_radau_substep_localization.py   --results-dir results   --json-out "$JSON"   --npz-out "$NPZ"   2>&1 | tee "$FULL"
rc=${PIPESTATUS[0]}
set -e

if [[ -s "$JSON" ]]; then
python3 - <<'PY'
import json
d=json.load(open("results/ge19_repair38_frozen_source_radau_substep_localization.json"))
print("CLASSIFICATION =",d["classification"])
print("ROUTE =",d["routing"]["next_route"])
print("FACTOR1_REPRO =",d["factor1_reproduction"])
print("SUBSTEP1 =",d["substep_results"]["1"])
print("SUBSTEP2 =",d["substep_results"]["2"])
print("SUBSTEP4 =",d["substep_results"]["4"])
print("CONVERGENCE =",d["convergence"])
print("DIAGNOSTIC_FLAGS =",d["diagnostic_flags"])
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
  echo GE19_REPAIR38_DIAGNOSTIC_COMPLETE
elif [[ "$rc" -eq 3 && -s "$JSON" ]]; then
  echo GE19_REPAIR38_IMPLEMENTATION_REPRODUCTION_FAIL
else
  echo GE19_REPAIR38_IMPLEMENTATION_OR_EXECUTION_FAILURE
fi
exit "$rc"
