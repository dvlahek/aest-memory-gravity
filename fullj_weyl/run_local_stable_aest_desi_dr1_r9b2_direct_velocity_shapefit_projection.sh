#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

PREFIT_LOCK='5864a8a56f420c578629763d478f60dfc49c2620'
ADAPTER_RESULT_LOCK='f5484b4572b673dfcead51875e3aa790c698a18c'
IMPLEMENTATION_LOCK='c10d18549ff1ab2ca6f948f7786dfdbc5225ab73'
R9B_POSTDATA_LOCK='22583094f3c5a417e7af6b1d7f284f739553048b'
DESI_COMMIT='7d51f4f86dc3bee6bf10f1a684913c943a89a844'
LSSTYPES_COMMIT='53f048e610bcb008548f66822b0879ce9df58cb1'
COSMOPRIMO_COMMIT='2e59c963c9b8e7cba1a4c8f161e978c6f4d80c2d'
COBAYA_COMMIT='b76b6fed2a6c8c5594c6f92d5058bef10079746a'
ADAPTER_JSON_SHA='c4d9281cd504785a9e4fb187b02db2860e24622bbe1ccf4a52e44446be0a119a'

git merge-base --is-ancestor "$PREFIT_LOCK" HEAD
git merge-base --is-ancestor "$ADAPTER_RESULT_LOCK" HEAD
git merge-base --is-ancestor "$IMPLEMENTATION_LOCK" HEAD
git merge-base --is-ancestor "$R9B_POSTDATA_LOCK" HEAD

echo "STABLE_AEST_DESI_DR1_R9B2_SCIENCE_LOCK_PASS prefit=$PREFIT_LOCK adapter=$ADAPTER_RESULT_LOCK implementation=$IMPLEMENTATION_LOCK r9b=$R9B_POSTDATA_LOCK"

BASE_PY="$(command -v python3 || command -v python)"
[[ -n "$BASE_PY" ]] || { echo 'R9B2: python missing' >&2; exit 2; }
VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then "$BASE_PY" -m venv "$VENV"; fi
export PATH="$VENV/bin:$PATH"

python -m pip install -q numpy scipy cython h5py camb
python -m pip install -q "git+https://github.com/adematti/lsstypes.git@$LSSTYPES_COMMIT"
python -m pip install -q "git+https://github.com/cosmodesi/cosmoprimo.git@$COSMOPRIMO_COMMIT"
python -m pip install -q "git+https://github.com/CobayaSampler/cobaya.git@$COBAYA_COMMIT"
python -m py_compile \
  fullj_weyl/stable_aest_desi_dr1_r9b2_direct_velocity_shapefit_projection.py \
  fullj_weyl/stable_aest_desi_dr1_r9b_shapefit_projection.py \
  fullj_weyl/stable_aest_observable_projection_r5b_derivative_zero.py

echo STABLE_AEST_DESI_DR1_R9B2_IMPORT_PASS

R9B_JSON='results/stable_aest_desi_dr1_r9b_shapefit_projection.json'
ADAPTER_JSON='results/stable_aest_desi_dr1_r9b2_velocity_adapter_validation.json'
[[ -s "$R9B_JSON" ]] || { echo "R9B2: missing historical R9b JSON" >&2; exit 3; }
[[ -s "$ADAPTER_JSON" ]] || { echo "R9B2: missing adapter JSON" >&2; exit 3; }
[[ "$(sha256sum "$ADAPTER_JSON" | awk '{print $1}')" == "$ADAPTER_JSON_SHA" ]] || { echo 'R9B2: adapter JSON SHA mismatch' >&2; exit 3; }

python - <<'PY'
import json
from pathlib import Path
r9=json.loads(Path('results/stable_aest_desi_dr1_r9b_shapefit_projection.json').read_text())
a=json.loads(Path('results/stable_aest_desi_dr1_r9b2_velocity_adapter_validation.json').read_text())
assert r9['classification']=='STABLE_AEST_DESI_DR1_R9B_CENTRAL_DERIVATIVE_FAIL'
assert r9['diagnostic_complete'] is True
assert r9['gates']['R9B_G1_parent_and_official_data_provenance'] is True
assert r9['gates']['R9B_G2_direct_physical_source_topology'] is True
assert r9['gates']['R9B_G3_shapefit_data_construction'] is True
assert r9['gates']['R9B_G4_central_derivative_consistency'] is False
assert a['classification']=='STABLE_AEST_DESI_DR1_R9B2_VELOCITY_ADAPTER_VALIDATED'
assert a['diagnostic_complete'] is True
assert a['science_evaluated'] is False
assert len(a['rows'])==6 and all(x['pass'] for x in a['rows'])
assert max(x['rel_f'] for x in a['rows']) <= 5e-3
print('STABLE_AEST_DESI_DR1_R9B2_PARENT_ADAPTER_PASS')
PY

# Reuse the exact official DESI repository, downloaded likelihood data, and disposable
# direct-physical modified CLASS build already established by the completed R9b run.
DESI_REPO="$ROOT/.local/desi_kp_likelihoods_r9b"
DESI_DATA="$ROOT/.local/desi_dr1_r9b_likelihood_data"
R9B_ROOT="$ROOT/.local/class_corrected_e8580832_densek64_stablechi_r9bdesi"
R9B_PYTARGET="$ROOT/.local/classy_corrected_e8580832_densek64_stablechi_r9bdesi"

[[ -d "$DESI_REPO" ]] || { echo "R9B2: missing $DESI_REPO; rerun R9b repair03 once" >&2; exit 3; }
[[ -d "$DESI_DATA" ]] || { echo "R9B2: missing $DESI_DATA; rerun R9b repair03 once" >&2; exit 3; }
[[ -d "$R9B_ROOT" ]] || { echo "R9B2: missing $R9B_ROOT; rerun R9b repair03 once" >&2; exit 3; }
[[ -d "$R9B_PYTARGET" ]] || { echo "R9B2: missing $R9B_PYTARGET; rerun R9b repair03 once" >&2; exit 3; }
[[ "$(git -C "$DESI_REPO" rev-parse HEAD)" == "$DESI_COMMIT" ]] || { echo 'R9B2: DESI repo commit mismatch' >&2; exit 3; }

grep -q 'FULLJ_AEST_STABLE_CHI_RESIDUAL_V1' "$R9B_ROOT/source/perturbations.c"
grep -q 'FULLJ_STABLE_AEST_R7A_LIVE_EPOCH_V1' "$R9B_ROOT/source/perturbations.c"
[[ "$(grep -Fc 'Bchi_aest *= pba->aest_eta*aest_r7a_epoch_weight(a);' "$R9B_ROOT/source/perturbations.c")" -eq 1 ]]
[[ "$(grep -Fc 'E_rhs_aest -= 0.5*Q_aest*Bchi_aest;' "$R9B_ROOT/source/perturbations.c")" -eq 1 ]]
! grep -q 'pba->aest_eta < 0.' "$R9B_ROOT/source/input.c"

echo STABLE_AEST_DESI_DR1_R9B2_DIRECT_SOURCE_PASS

export AEST_STABLE_R8A_CLASS_ROOT="$R9B_ROOT"
export AEST_R9B_DESI_DATA_DIR="$DESI_DATA"
export AEST_R9B_DESI_REPO="$DESI_REPO"
export AEST_R7A_EPOCH_MODE=full
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
unset AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE \
  AEST_R2D_TRACE_FILE AEST_R2D_TRACE_KH AEST_R2D_TRACE_ALL_K \
  AEST_TANGENT_ALLOW_K_MISS AEST_ERHS_TRACE_FILE AEST_ERHS_TRACE_K || true

JSON='results/stable_aest_desi_dr1_r9b2_direct_velocity_shapefit_projection.json'
NPZ='results/stable_aest_desi_dr1_r9b2_direct_velocity_shapefit_projection.npz'
LOG='results/stable_aest_desi_dr1_r9b2_direct_velocity_shapefit_projection.log'
ZIP='results/stable_aest_desi_dr1_r9b2_direct_velocity_shapefit_projection_bundle.zip'
ENVOUT='results/stable_aest_desi_dr1_r9b2_environment.txt'
WORK='results/stable_aest_desi_dr1_r9b2_work'
rm -f "$JSON" "$NPZ" "$LOG" "$ZIP" "$ENVOUT"
rm -rf "$WORK"

{
  echo "repo_head=$(git rev-parse HEAD)"
  echo "prefit_lock=$PREFIT_LOCK"
  echo "adapter_result_lock=$ADAPTER_RESULT_LOCK"
  echo "implementation_lock=$IMPLEMENTATION_LOCK"
  echo "r9b_postdata_lock=$R9B_POSTDATA_LOCK"
  echo "desi_repo_commit=$DESI_COMMIT"
  echo "adapter_json_sha256=$ADAPTER_JSON_SHA"
  echo "python=$(python --version 2>&1)"
  echo '--- pip freeze ---'
  python -m pip freeze
} > "$ENVOUT"

set +e
PYTHONPATH="$R9B_PYTARGET:${PYTHONPATH:-}" python -u -m fullj_weyl.stable_aest_desi_dr1_r9b2_direct_velocity_shapefit_projection \
  --data-dir "$DESI_DATA" --official-repo "$DESI_REPO" \
  --json-out "$JSON" --npz-out "$NPZ" --workdir "$WORK" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

python - "$ZIP" "$LOG" "$JSON" "$NPZ" "$ENVOUT" "$WORK" "$ADAPTER_JSON" "$R9B_JSON" <<'PY'
from pathlib import Path
import sys, zipfile
zp=Path(sys.argv[1])
items=[Path(x) for x in sys.argv[2:6]]
work=Path(sys.argv[6])
items += [Path(sys.argv[7]), Path(sys.argv[8])]
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED) as z:
    for p in items:
        if p.exists(): z.write(p,p.as_posix())
    if work.exists():
        for p in sorted(work.rglob('*')):
            if p.is_file(): z.write(p,p.as_posix())
print(f'STABLE_AEST_DESI_DR1_R9B2_BUNDLE={zp}')
PY

echo "STABLE_AEST_DESI_DR1_R9B2_EXIT=$code"
echo "STABLE_AEST_DESI_DR1_R9B2_LOG=$LOG"
echo "STABLE_AEST_DESI_DR1_R9B2_JSON=$JSON"
echo "STABLE_AEST_DESI_DR1_R9B2_NPZ=$NPZ"
echo "STABLE_AEST_DESI_DR1_R9B2_ZIP=$ZIP"
exit "$code"
