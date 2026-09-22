#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results

# Canonical Repair32B reconstruction contract.
test "$(git rev-parse HEAD:ge19/repair32b_predata_factor2_corrected_reduced_h2_z11_reconstruction.json)" = "cce721ac498f84ffd084111065056fef86b5c719"
test "$(git rev-parse HEAD:ge19/repair32b_factor2_corrected_reduced_h2_z11_reconstruction.py)" = "6ece578e8a30f48faaded8808687a9bd5c114608"
test "$(git rev-parse HEAD:.github/workflows/ge19-repair32b-reconstruction-prelock-audit.yml)" = "25c5332ad654d517d76564cf1b0d8343a4e56c32"
test "$(git rev-parse HEAD:docs/ge19_repair32a_ge06_ge05_raw_residual_normalization_dictionary_result_freeze.md)" = "6c5b7f830cbae95209eda0e8c8663c6620ab7071"

for c in \
  5a785ff59007807c5bdadf1da0cdd12de78873a8 \
  2bc93cad7aaee8210b4779cd92839946dafa4fbb \
  189ce1a9381de277bc5d2a2cf0ead324a9f43b77 \
  cb06051bfa3359ff10681fa4eefac4fae17c25e7; do
  git merge-base --is-ancestor "$c" HEAD
done
echo GE19_REPAIR32B_LOCK_PASS

if [[ -z "${VIRTUAL_ENV:-}" ]]; then
  echo GE19_REPAIR32B_VENV_NOT_ACTIVE
  echo "Run: source .venv/bin/activate"
  exit 5
fi

python3 -m py_compile ge19/repair32b_factor2_corrected_reduced_h2_z11_reconstruction.py

python3 - <<'PY'
import json
import numpy as np
import ge19.repair30_reduced_h2_z11_reclosure as r30
import ge19.repair32b_factor2_corrected_reduced_h2_z11_reconstruction as r32

p=json.load(open("ge19/repair32b_predata_factor2_corrected_reduced_h2_z11_reconstruction.json"))
assert p["classification"]=="GE19_REPAIR32B_PREDATA_FACTOR2_CORRECTED_REDUCED_H2_Z11_RECONSTRUCTION"
assert p["sole_physics_dictionary_change"]["GE05_M1_to_GE06_raw_residual_scale"]==2
assert p["stop_boundary"]["no_Z11_certification_in_Repair32B"] is True
assert p["stop_boundary"]["no_H4_Z21"] is True
assert r32.RAW_RESIDUAL_DICTIONARY_SCALE==2.0

bg={"Q_action":np.asarray([1.2,1.3]),"a":np.asarray([0.4,0.5])}
B=np.asarray([[1+2j,3+4j]]*len(r32.r7.FOURIER_N),complex)
assert np.array_equal(r32.source_from_B(bg,B),2.0*r30.source_from_B(bg,B))
print("GE19_REPAIR32B_LOCAL_PREEXECUTION_AUDIT_PASS")
PY

# Frozen local parents inherited from Repair30.
declare -A HASHES
HASHES["results/ge15_R1_dense_accepted_step_trace.dat"]="7f57ab676f2a31cf0abf93ff0f8b0f1f2f80bb9a58d7cf1e47e10a158c57c69f"
HASHES["results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.json"]="ae3cc790ecffbd5498b5852273c72ae578d4615de29bbb616673c05cdb3e74b7"
HASHES["results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz"]="011c0ae54fd21d70c0e2c695ce62e7b74a3c5529a07c9023c882a447d5b40ca3"
HASHES["results/ge19_repair22_on_shell_parent_z20_certification.json"]="7d53b2458183c6b2cc326acdded70b2c3ce1fab959d8456e56d3b4f1f86ef374"
HASHES["results/ge19_repair22_on_shell_parent_z20_certification.npz"]="3020e0d040f902ab2609e05705f4508d9919665b1344fa0e641644ea8fc41a16"
HASHES["results/ge19_repair27_cancellation_free_parent_q20_reconstruction.json"]="99a2183e7088c7492f624cae2d294612380714c1d81aa7ff49cc4fcd1c62c74b"
HASHES["results/ge19_repair27_cancellation_free_parent_q20_reconstruction.npz"]="2b1566d402e4c9e8daee8e5c7084b3da7735442b4fb604d51489b708662fd9c0"
HASHES["results/ge19_repair32a_ge06_ge05_raw_residual_normalization_dictionary_audit.json"]="adef8fad50233c7fa5df3d57e7f21df80ed99228402831b2861ad06256519725"

for f in "${!HASHES[@]}"; do
  if [[ ! -f "$f" ]]; then
    echo "GE19_REPAIR32B_MISSING_LOCAL_PARENT: $f"
    exit 6
  fi
  got="$(sha256sum "$f" | awk '{print $1}')"
  test "$got" = "${HASHES[$f]}"
done
echo GE19_REPAIR32B_LOCAL_PARENTS_PASS

# Lean immutable R2 reference used by Repair30/31.
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
echo GE19_REPAIR32B_R2_REFERENCE_PASS

JSON="results/ge19_repair32b_factor2_corrected_reduced_h2_z11_reconstruction.json"
NPZ="results/ge19_repair32b_factor2_corrected_reduced_h2_z11_reconstruction.npz"
FULL="results/ge19_repair32b_factor2_corrected_reduced_h2_z11_reconstruction_FULL.log"
rm -f "$JSON" "$NPZ" "$FULL"

set +e
python3 ge19/repair32b_factor2_corrected_reduced_h2_z11_reconstruction.py \
  --results-dir results \
  --repair28-npz "$REF" \
  --repair32a-json results/ge19_repair32a_ge06_ge05_raw_residual_normalization_dictionary_audit.json \
  --json-out "$JSON" \
  --npz-out "$NPZ" \
  2>&1 | tee "$FULL"
rc=${PIPESTATUS[0]}
set -e

if [[ -s "$JSON" ]]; then
  python3 - <<'PY'
import json
d=json.load(open("results/ge19_repair32b_factor2_corrected_reduced_h2_z11_reconstruction.json"))
print("CLASSIFICATION =",d["classification"])
print("CORRECTED_H2_VALIDATED =",d["corrected_H2_reconstruction_validated"])
print("Z11_CERTIFIED =",d["Z11_certified"])
print("ROUTE =",d["routing"]["next_route"])
print("H4_Z21_LICENSED =",d["routing"]["H4_Z21_licensed"])
print("DICTIONARY =",d["raw_residual_dictionary"])
print("B10_TIME =",d["memory_source_control"]["B10_primary_vs_time_control_relative_L2_max"])
print("STATE_GLOBAL =",d["solve_controls"]["primary128_vs_control64_full_six_field_global_relative_L2_max"])
print("STATE_DYNAMIC =",d["solve_controls"]["primary128_vs_control64_dynamic_global_relative_L2_max"])
print("STATE_MAX_PER_FIELD_REPORT_ONLY =",d["solve_controls"]["primary128_vs_control64_state_relative_L2_max_report_only"])
print("CHI_PARENT =",d["chi11_controls"]["reduced_vs_Repair29B_R2_parent_relative_L2_max"])
print("CHI_C_ENVELOPE =",d["chi11_controls"]["C_envelope_relative_L2_max"])
print("HISTORICAL_MONITORS =",d["historical_Repair30_monitors_report_only"])
print("VALIDATION_GATES =",d["validation_gates"])
PY
fi

for f in "$JSON" "$NPZ" "$FULL"; do
  if [[ -f "$f" ]]; then
    sha256sum "$f"
    wc -c "$f"
  fi
done

if [[ "$rc" -eq 0 ]]; then
  echo GE19_REPAIR32B_EXECUTION_COMPLETE
elif [[ "$rc" -eq 2 && -s "$JSON" ]]; then
  echo GE19_REPAIR32B_VALID_SCIENCE_FAIL_FREEZE_REQUIRED
else
  echo GE19_REPAIR32B_IMPLEMENTATION_OR_EXECUTION_FAILURE
fi
exit "$rc"
