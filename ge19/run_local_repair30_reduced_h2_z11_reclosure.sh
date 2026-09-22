#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results

# Frozen repository contract.
test "$(git rev-parse HEAD:ge19/repair30_predata_reduced_h2_z11_reclosure.json)" = "264b52832e762dd2010df1eba83e5f2c1a4d8874"
test "$(git rev-parse HEAD:ge19/repair30_reduced_h2_z11_reclosure.py)" = "a014dd3a56914858cb6ca7e0f5bdd45afdf573db"
test "$(git rev-parse HEAD:.github/workflows/ge19-repair30-repair01-prelock-audit.yml)" = "4cad3fee8bc4574cbf0aec8dcbd31944b877c5d5"
test "$(git rev-parse HEAD:docs/ge19_repair30_initial_execution_implementation_fail_freeze.md)" = "4e803520f73c97272a3f35ff62b017021908dc1d"
test "$(git rev-parse HEAD:docs/ge19_repair30_repair01_implementation_lock.md)" = "6d41cbda64d0524217d342d8d45f728d4bba7948"

for c in \
  5fd14e9dc46ced04a838d79cc3b47319c4e4f22f \
  37d8b6f1e2e5980f1f423c014b6a6b60157f78bd \
  0939742f9c518818091bed8a84465b2148c73153 \
  dc6774329b53531fc0b90f66c3d60916ad05e9d8 \
  c19ff6dd3ccc859ec54c66edaa05048391f70a3c; do
  git merge-base --is-ancestor "$c" HEAD
done
echo GE19_REPAIR30_LOCK_PASS

if [[ -z "${VIRTUAL_ENV:-}" ]]; then
  echo GE19_REPAIR30_VENV_NOT_ACTIVE
  echo "Run: source .venv/bin/activate"
  exit 5
fi

python3 -m py_compile ge19/repair30_reduced_h2_z11_reclosure.py

python3 - <<'PY'
import json
import ge19.repair30_reduced_h2_z11_reclosure as r30
p=json.load(open("ge19/repair30_predata_reduced_h2_z11_reclosure.json"))
assert p["classification"]=="GE19_REPAIR30_PREDATA_REDUCED_H2_Z11_RECLOSURE"
assert p["created_before_repair30_result"] is True
assert p["hierarchy"]["equation"]=="L_total Z11 = -M1[Z10,q10]"
assert p["stop_boundary"]["no_H4_Z21_solve_in_Repair30"] is True
s=r30.symbolic_m1_audit()
assert s["partial_px_identity"] and s["partial_r_identity"]
assert r30.TIME_MAX==5e-3
assert r30.CHI_PARENT_MAX==5e-3
print("GE19_REPAIR30_LOCAL_PREEXECUTION_AUDIT_PASS")
PY

# Frozen local parents already produced by the certified local chain.
declare -A HASHES
HASHES["results/ge15_R1_dense_accepted_step_trace.dat"]="7f57ab676f2a31cf0abf93ff0f8b0f1f2f80bb9a58d7cf1e47e10a158c57c69f"
HASHES["results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.json"]="ae3cc790ecffbd5498b5852273c72ae578d4615de29bbb616673c05cdb3e74b7"
HASHES["results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz"]="011c0ae54fd21d70c0e2c695ce62e7b74a3c5529a07c9023c882a447d5b40ca3"
HASHES["results/ge19_repair22_on_shell_parent_z20_certification.json"]="7d53b2458183c6b2cc326acdded70b2c3ce1fab959d8456e56d3b4f1f86ef374"
HASHES["results/ge19_repair22_on_shell_parent_z20_certification.npz"]="3020e0d040f902ab2609e05705f4508d9919665b1344fa0e641644ea8fc41a16"
HASHES["results/ge19_repair27_cancellation_free_parent_q20_reconstruction.json"]="99a2183e7088c7492f624cae2d294612380714c1d81aa7ff49cc4fcd1c62c74b"
HASHES["results/ge19_repair27_cancellation_free_parent_q20_reconstruction.npz"]="2b1566d402e4c9e8daee8e5c7084b3da7735442b4fb604d51489b708662fd9c0"

for f in "${!HASHES[@]}"; do
  if [[ ! -f "$f" ]]; then
    echo "GE19_REPAIR30_MISSING_LOCAL_PARENT: $f"
    exit 6
  fi
  got="$(sha256sum "$f" | awk '{print $1}')"
  test "$got" = "${HASHES[$f]}"
done
echo GE19_REPAIR30_LOCAL_PARENTS_PASS

# Lean immutable copy of the Repair29B-certified R2 reference.
ARTROOT="$ROOT/frozen_repair28_repair30"
REF="$ARTROOT/ge19_repair28_cancellation_free_full_state_eta_tangent.npz"
if [[ ! -f "$REF" ]]; then
  rm -rf "$ARTROOT"
  mkdir -p "$ARTROOT"
  gh run download 35747827610 \
    --repo dvlahek/aest-memory-gravity \
    --name ge19_repair30_r2_reference_only \
    --dir "$ARTROOT"
fi
test -f "$REF"
test "$(sha256sum "$REF" | awk '{print $1}')" = "101c38d91344d12071ecb343c35769326f80975e013b7d159f573aae73879705"
test "$(wc -c < "$REF" | tr -d ' ')" = "530980"
echo GE19_REPAIR30_R2_REFERENCE_PASS

JSON="results/ge19_repair30_reduced_h2_z11_reclosure.json"
NPZ="results/ge19_repair30_reduced_h2_z11_reclosure.npz"
FULL="results/ge19_repair30_reduced_h2_z11_reclosure_FULL.log"
rm -f "$JSON" "$NPZ" "$FULL"

set +e
python3 ge19/repair30_reduced_h2_z11_reclosure.py \
  --results-dir results \
  --repair28-npz "$REF" \
  --json-out "$JSON" \
  --npz-out "$NPZ" \
  2>&1 | tee "$FULL"
rc=${PIPESTATUS[0]}
set -e

if [[ -s "$JSON" ]]; then
  python3 - <<'PY'
import json
d=json.load(open("results/ge19_repair30_reduced_h2_z11_reclosure.json"))
print("CLASSIFICATION =",d["classification"])
print("Z11_CONSTRUCTED =",d["Z11_constructed"])
print("Z11_CERTIFIED =",d["Z11_certified"])
print("ROUTE =",d["routing"]["next_route"])
print("H4_Z21_LICENSED =",d["routing"]["H4_Z21_licensed"])
print("B10_TIME =",d["memory_source_control"]["B10_primary_vs_time_control_relative_L2_max"])
print("STATE_TIME =",d["solve_controls"]["primary128_vs_control64_state_relative_L2_max"])
print("CHI_PARENT =",d["chi11_controls"]["reduced_vs_Repair29B_R2_parent_relative_L2_max"])
print("CHI_C_ENVELOPE =",d["chi11_controls"]["C_envelope_relative_L2_max"])
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
  echo GE19_REPAIR30_EXECUTION_COMPLETE
elif [[ "$rc" -eq 2 && -s "$JSON" ]]; then
  echo GE19_REPAIR30_VALID_SCIENCE_FAIL_FREEZE_REQUIRED
else
  echo GE19_REPAIR30_IMPLEMENTATION_OR_EXECUTION_FAILURE
fi
exit "$rc"
