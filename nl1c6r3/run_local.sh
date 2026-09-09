#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

REPO="dvlahek/aest-memory-gravity"
ARTIFACT_ID="10101422385"
ARTIFACT_SHA256="0ab60cbc32210ad3fb75c881f91a9db11148280e9223ea644680ed8cdfbaa590"
INPUT_DIR="input/nl1c5b"
ZIP_IN="input/nl1c5b.zip"
RESULT_DIR="results"

mkdir -p "$INPUT_DIR" "$RESULT_DIR"

python3 - <<'PY'
import numpy, scipy
print('numpy', numpy.__version__)
print('scipy', scipy.__version__)
PY

need_download=1
if [[ -s "$ZIP_IN" ]]; then
  got="$(sha256sum "$ZIP_IN" | awk '{print $1}')"
  if [[ "$got" == "$ARTIFACT_SHA256" ]]; then
    need_download=0
  fi
fi

if [[ "$need_download" -eq 1 ]]; then
  command -v gh >/dev/null 2>&1 || { echo 'ERROR: GitHub CLI (gh) is required to download the frozen NL1C5B artifact.'; exit 3; }
  echo "Downloading frozen NL1C5B artifact $ARTIFACT_ID ..."
  gh api "/repos/$REPO/actions/artifacts/$ARTIFACT_ID/zip" > "$ZIP_IN"
fi

echo "$ARTIFACT_SHA256  $ZIP_IN" | sha256sum -c -
rm -rf "$INPUT_DIR"
mkdir -p "$INPUT_DIR"
unzip -q "$ZIP_IN" -d "$INPUT_DIR"
NL1C5B_NPZ="$(find "$INPUT_DIR" -type f -name 'nl1c5b_baryon_source_freeze.npz' -print -quit)"
test -n "$NL1C5B_NPZ"
test -s "$NL1C5B_NPZ"

echo "Frozen input: $NL1C5B_NPZ"
echo "Git HEAD: $(git rev-parse HEAD)"
echo "Branch: $(git branch --show-current)"

python3 -m py_compile nl1c6/full_j_baryonic_reclosure.py
python3 -m py_compile nl1c6r3/fixed_source_constitutive_homotopy.py

python3 - <<'PY'
import numpy as np
from nl1c6 import full_j_baryonic_reclosure as b
from nl1c6r3 import fixed_source_constitutive_homotopy as r3
n=256; a=1/7; beta=1.0; kind='simple'
x=np.arange(n)*b.BOX/n
chi=1e-7*np.cos(2*np.pi*3*x/b.BOX)+2e-8*np.sin(2*np.pi*5*x/b.BOX)
rhs=3e-9*np.cos(2*np.pi*3*x/b.BOX); rhs-=rhs.mean()
rb=b.residual_state(chi,rhs,a,beta,kind)[0]
for route in ('screened','mass'):
    rr=r3.residual_theta(chi,rhs,a,beta,kind,1.0,route)[0]
    err=np.linalg.norm(rr-rb)/max(np.linalg.norm(rb),1e-300)
    print('endpoint_identity', route, err)
    assert err < 1e-13
print('NL1C6R3_THETA1_ENDPOINT_IDENTITY_PASS')
PY

JSON_OUT="$RESULT_DIR/nl1c6r3_full_j_baryonic_reclosure.json"
NPZ_OUT="$RESULT_DIR/nl1c6r3_full_j_baryonic_reclosure.npz"
LOG_OUT="$RESULT_DIR/nl1c6r3_stdout.log"
PROV_OUT="$RESULT_DIR/nl1c6r3_local_provenance.txt"
BUNDLE_OUT="$RESULT_DIR/nl1c6r3_local_bundle.zip"

{
  echo "git_head=$(git rev-parse HEAD)"
  echo "branch=$(git branch --show-current)"
  echo "input_artifact_id=$ARTIFACT_ID"
  echo "input_zip_sha256=$ARTIFACT_SHA256"
  echo "python=$(python3 --version 2>&1)"
  python3 - <<'PY'
import platform, numpy, scipy
print('platform='+platform.platform())
print('numpy='+numpy.__version__)
print('scipy='+scipy.__version__)
PY
} > "$PROV_OUT"

echo "Starting preregistered NL1C6R3 locally..."
start_epoch="$(date +%s)"
set +e
python3 -u nl1c6r3/fixed_source_constitutive_homotopy.py \
  --input-npz "$NL1C5B_NPZ" \
  --input-zip-sha256 "$ARTIFACT_SHA256" \
  --json-out "$JSON_OUT" \
  --npz-out "$NPZ_OUT" \
  2>&1 | tee "$LOG_OUT"
status=${PIPESTATUS[0]}
set -e
end_epoch="$(date +%s)"
echo "runtime_seconds=$((end_epoch-start_epoch))" | tee -a "$PROV_OUT"
echo "process_exit_code=$status" | tee -a "$PROV_OUT"

if [[ "$status" -ne 0 && "$status" -ne 2 ]]; then
  echo "Technical failure: exit $status"
  exit "$status"
fi

test -s "$JSON_OUT"
test -s "$NPZ_OUT"

python3 - <<'PY'
import json
p='results/nl1c6r3_full_j_baryonic_reclosure.json'
d=json.load(open(p))
print('\nFINAL CLASSIFICATION:', d['classification'])
print('GATES:', json.dumps(d['gates'], sort_keys=True))
print('GLOBAL METRICS:', json.dumps(d['global_metrics'], sort_keys=True))
print('anchor_multibranch_found=', d.get('anchor_multibranch_found'))
print('anchor_max_lowmode_difference=', d.get('anchor_max_lowmode_difference'))
PY

sha256sum "$JSON_OUT" "$NPZ_OUT" "$LOG_OUT" "$PROV_OUT" > "$RESULT_DIR/nl1c6r3_local_SHA256SUMS.txt"
rm -f "$BUNDLE_OUT"
zip -q "$BUNDLE_OUT" \
  "$JSON_OUT" "$NPZ_OUT" "$LOG_OUT" "$PROV_OUT" \
  "$RESULT_DIR/nl1c6r3_local_SHA256SUMS.txt" \
  docs/nl1c6r3_predata_fixed_source_constitutive_homotopy.md \
  nl1c6r3/fixed_source_constitutive_homotopy.py \
  nl1c6/full_j_baryonic_reclosure.py

echo "Bundle ready: $BUNDLE_OUT"
exit "$status"
