#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results

test "$(git rev-parse HEAD:ge19/repair41_predata_direct_fine_grid_target_source_reconstruction.json)" = "bc07d4130a22906496588f4bc539b19119b21885"
test "$(git rev-parse HEAD:ge19/repair41_direct_fine_grid_target_source_reconstruction.py)" = "b04d39d650afaa0a4657d4d96232ea67a35d725d"
test "$(git rev-parse HEAD:.github/workflows/ge19-repair41-prelock-audit.yml)" = "f1ab26164b565677f757edab9d02f078ece27743"
test "$(git rev-parse HEAD:docs/ge19_repair40_valid_piecewise_stage_source_decomposition_freeze.md)" = "d2dfd61d765a8fd3c96382bd19b89b7295c841f5"
test "$(git rev-parse HEAD:docs/ge19_repair41_direct_fine_grid_target_implementation_lock.md)" = "7079974b8d3dd7fad24fd196ca5c7ac0eea79864"

for c in   bd9446feccb28779fa3f59bd0206e18d2ebaed4e   70caf9cdc460c8b1123677ae4a669ae58445cc90   71fd90acb593201294c02f1f435a3652edc0ed0b   faf3fd436265325cfc50e7f3e9e3fd2f2f85d9c3   2355763775fc026816929c17a115bab62f498616
do
  git merge-base --is-ancestor "$c" HEAD
done
echo GE19_REPAIR41_LOCK_PASS

if [[ -z "${VIRTUAL_ENV:-}" ]]; then
  echo GE19_REPAIR41_VENV_NOT_ACTIVE
  echo "Run: source .venv/bin/activate"
  exit 5
fi

python3 -m py_compile ge19/repair41_direct_fine_grid_target_source_reconstruction.py
python3 ge19/repair41_direct_fine_grid_target_source_reconstruction.py --help >/tmp/r41_help.txt
grep -q -- "--repair26-trace" /tmp/r41_help.txt
grep -q -- "--repair28-npz" /tmp/r41_help.txt
grep -q -- "--json-out" /tmp/r41_help.txt
grep -q -- "--npz-out" /tmp/r41_help.txt
echo GE19_REPAIR41_LOCAL_PREEXECUTION_AUDIT_PASS

declare -A HASHES
HASHES["results/ge19_repair40_piecewise_stage_source_decomposition.json"]="f5618344db31328dc4e680eb41bb6a715da3fbe7e54ddff3cb53bc027386bf44"
HASHES["results/ge19_repair40_piecewise_stage_source_decomposition.npz"]="06c7799787abcc510259c626bcb9ca925f96efce13c7949a89690f243fbf01b5"
HASHES["results/ge19_repair37_cancellation_safe_fd8_h4_z21_reclosure.json"]="da8f2f00c22c866ec3f82381d23f69bf036e630fe2a29c5c44657984b760f61a"
HASHES["results/ge19_repair37_cancellation_safe_fd8_h4_z21_reclosure.npz"]="572d8937c1d742b10da66e34cc076377c1b2feb20b8f72eb25c3eaf31a59829f"
HASHES["results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz"]="011c0ae54fd21d70c0e2c695ce62e7b74a3c5529a07c9023c882a447d5b40ca3"
HASHES["results/ge19_repair18_zero_coordinate_constraint_projected_momentum_boundary.json"]="d5603138c2f488413686323d1241613f6ef707b586116aa7fe865ae25ceb0edc"
HASHES["results/ge19_repair22_on_shell_parent_z20_certification.json"]="7d53b2458183c6b2cc326acdded70b2c3ce1fab959d8456e56d3b4f1f86ef374"
HASHES["results/ge19_repair22_on_shell_parent_z20_certification.npz"]="3020e0d040f902ab2609e05705f4508d9919665b1344fa0e641644ea8fc41a16"
HASHES["results/ge19_repair27_cancellation_free_parent_q20_reconstruction.json"]="99a2183e7088c7492f624cae2d294612380714c1d81aa7ff49cc4fcd1c62c74b"
HASHES["results/ge19_repair27_cancellation_free_parent_q20_reconstruction.npz"]="2b1566d402e4c9e8daee8e5c7084b3da7735442b4fb604d51489b708662fd9c0"
HASHES["results/ge19_repair32a_ge06_ge05_raw_residual_normalization_dictionary_audit.json"]="adef8fad50233c7fa5df3d57e7f21df80ed99228402831b2861ad06256519725"
HASHES["results/ge19_repair32b_factor2_corrected_reduced_h2_z11_reconstruction.json"]="226dd2a2a0e86ddccc39a62d833960bdf9d5a9af038ad3bf225bbbf69d0b95cf"
HASHES["results/ge19_repair32b_factor2_corrected_reduced_h2_z11_reconstruction.npz"]="5d4a0a72c08d09d096a8de0b428b3c8443fc33e8ad442ed6d997d6bf2bc6e327"
HASHES["results/ge19_repair32c_artifact_only_reduced_z11_certification.json"]="037314effa33c5bfaf51f6f3c72459de43cb486c6ef5e9a94f5b1984a68611b9"
HASHES["results/ge18_repair01_on_shell_matched_dust_first_order_bridge.npz"]="b6ccaf2257fbb09df701c43bc9a593a3f68238826277a510a0b3b531ea9fa6fe"
HASHES["results/ge15_R1_dense_accepted_step_trace.dat"]="7f57ab676f2a31cf0abf93ff0f8b0f1f2f80bb9a58d7cf1e47e10a158c57c69f"

for f in "${!HASHES[@]}"; do
  if [[ ! -f "$f" ]]; then
    echo "GE19_REPAIR41_MISSING_LOCAL_PARENT: $f"
    exit 6
  fi
  got="$(sha256sum "$f" | awk '{print $1}')"
  test "$got" = "${HASHES[$f]}"
done
test -s results/ge15_R1_cli_background.dat
echo GE19_REPAIR41_LOCAL_PARENTS_PASS

# Immutable Repair26 cancellation-free full-history bath trace.
ART26="$ROOT/frozen_repair26_repair41"
TRACE="$(find "$ART26" -type f -name ge19_repair26_R1_full_history_trace.dat -print -quit 2>/dev/null || true)"
if [[ -z "$TRACE" ]]; then
  command -v gh >/dev/null 2>&1 || {
    echo GE19_REPAIR41_GH_NOT_AVAILABLE
    exit 7
  }
  rm -rf "$ART26"
  mkdir -p "$ART26"
  gh run download 35721220889     --repo dvlahek/aest-memory-gravity     --name results_bundle_ge19_repair26_cancellation_free_full_history_bath_boundary     --dir "$ART26"
  TRACE="$(find "$ART26" -type f -name ge19_repair26_R1_full_history_trace.dat -print -quit)"
fi
test -n "$TRACE"
test -s "$TRACE"
test "$(sha256sum "$TRACE" | awk '{print $1}')" =   "608ee0b4c868a701db6976f756b9a551cd9ddffe1e8e4ab37c5cd2361405a6f8"
test "$(wc -c < "$TRACE" | tr -d ' ')" = "26643162"
echo GE19_REPAIR41_REPAIR26_PARENT_PASS

# Immutable Repair28 R2 tangent reference used by Repair32B.
ART28="$ROOT/frozen_repair28_repair41"
REF="$ART28/ge19_repair28_cancellation_free_full_state_eta_tangent.npz"
if [[ ! -f "$REF" ]]; then
  command -v gh >/dev/null 2>&1 || {
    echo GE19_REPAIR41_GH_NOT_AVAILABLE
    exit 7
  }
  rm -rf "$ART28"
  mkdir -p "$ART28"
  gh run download 35747827610     --repo dvlahek/aest-memory-gravity     --name ge19_repair30_r2_reference_only     --dir "$ART28"
fi
test -f "$REF"
test "$(sha256sum "$REF" | awk '{print $1}')" =   "101c38d91344d12071ecb343c35769326f80975e013b7d159f573aae73879705"
test "$(wc -c < "$REF" | tr -d ' ')" = "530980"
echo GE19_REPAIR41_R2_REFERENCE_PASS

JSON="results/ge19_repair41_direct_fine_grid_target_source_reconstruction.json"
NPZ="results/ge19_repair41_direct_fine_grid_target_source_reconstruction.npz"
FULL="results/ge19_repair41_direct_fine_grid_target_source_reconstruction_FULL.log"
rm -f "$JSON" "$NPZ" "$FULL"

set +e
python3 ge19/repair41_direct_fine_grid_target_source_reconstruction.py   --results-dir results   --repair26-trace "$TRACE"   --repair28-npz "$REF"   --json-out "$JSON"   --npz-out "$NPZ"   2>&1 | tee "$FULL"
rc=${PIPESTATUS[0]}
set -e

if [[ -s "$JSON" ]]; then
python3 - <<'PY'
import json
d=json.load(open("results/ge19_repair41_direct_fine_grid_target_source_reconstruction.json"))
print("CLASSIFICATION =",d["classification"])
print("ROUTE =",d["routing"]["next_route"])
print("GRIDS =",d["direct_time_grids"])
print("ADAPTER =",d["formula_adapter_reproduction"])
print("RESOLUTION =",d["direct_parent_and_target_resolution"])
print("DIRECT_VS_FROZEN =",d["direct763_vs_frozen_stage_representations"])
print("IMPLEMENTATION_GATES =",d["implementation_gates"])
print("RESOLUTION_GATES =",d["resolution_gates"])
print("Z21_CERTIFIED =",d["Z21_window_local_particular_certified"])
print("H4_RECLOSURE =",d["H4_Z21_reclosure_performed"])
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
  echo GE19_REPAIR41_DIAGNOSTIC_COMPLETE
elif [[ "$rc" -eq 3 && -s "$JSON" ]]; then
  echo GE19_REPAIR41_IMPLEMENTATION_REPRODUCTION_FAIL
else
  echo GE19_REPAIR41_IMPLEMENTATION_OR_EXECUTION_FAILURE
fi
exit "$rc"
