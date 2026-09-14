#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

PREDATA_LOCK='05d338e1dde7719cc78b132cd146a408c6a90d62'
R5B_POSTDATA_LOCK='3242335ece23fbeb743f075a1df1aa70acaab211'
R5B_JSON_SHA='26ce723e2b7b783fcd19765c9c7f01b6101992a3f09e6ee321299bf148259ca9'
R5B_NPZ_SHA='a88f99254bc1a7393e40691d5dc539bb1e1648eae1b892e43b63f593f8e367e1'
ACT_COMMIT='b386ddbb5821c1216c709f051c9289292f174d30'
ACT_REPO='https://github.com/ACTCollaboration/act_dr6_lenslike.git'

for f in \
  docs/stable_aest_act_dr6_r6a_fixed_template_projection_predata.md \
  docs/stable_aest_observable_projection_r5b_derivative_zero_postdata.md \
  results/stable_aest_observable_projection_r5b_derivative_zero.json \
  results/stable_aest_observable_projection_r5b_derivative_zero.npz \
  fullj_weyl/stable_aest_act_dr6_r6a_fixed_template_projection.py; do
  [[ -f "$f" ]] || { echo "STABLE_AEST_ACT_DR6_R6A: missing $f" >&2; exit 3; }
done

git merge-base --is-ancestor "$PREDATA_LOCK" HEAD
git merge-base --is-ancestor "$R5B_POSTDATA_LOCK" HEAD
[[ "$(sha256sum results/stable_aest_observable_projection_r5b_derivative_zero.json | awk '{print $1}')" == "$R5B_JSON_SHA" ]]
[[ "$(sha256sum results/stable_aest_observable_projection_r5b_derivative_zero.npz | awk '{print $1}')" == "$R5B_NPZ_SHA" ]]
echo "STABLE_AEST_ACT_DR6_R6A_SCIENCE_LOCK_PASS predata=$PREDATA_LOCK r5b_postdata=$R5B_POSTDATA_LOCK"

BASE_PY="$(command -v python3 || true)"
[[ -n "$BASE_PY" ]] || { echo 'STABLE_AEST_ACT_DR6_R6A: python3 missing' >&2; exit 2; }

# Static anti-stale audit before any ACT data are accessed.
"$BASE_PY" - <<'PY'
from pathlib import Path
p=Path('fullj_weyl/stable_aest_act_dr6_r6a_fixed_template_projection.py').read_text()
required=[
 'PREDATA_LOCK = "05d338e1dde7719cc78b132cd146a408c6a90d62"',
 'R5B_POSTDATA_LOCK = "3242335ece23fbeb743f075a1df1aa70acaab211"',
 'ACT_COMMIT = "b386ddbb5821c1216c709f051c9289292f174d30"',
 'ACT_INTERNAL_VERSION = "1.2.0"',
 'ACT_VARIANT = "act_baseline"',
 'NSIMS_ACT = 796',
 'TRIM_LMAX = 2998',
 'ETA_GRID = (0.0, 0.01, 0.025, 0.05)',
 'like_corrections=False',
 'lens_only=True',
]
for token in required:
    assert token in p, token
for forbidden in (
    'actplanck_baseline', 'act_extended', 'non_linear =', 'Halofit',
    'nominal_e10', 'eta=10', 'v0.62', 'v0.65'
):
    assert forbidden not in p, forbidden
assert 'No measured value' not in p  # claim discipline lives in prereg, not result logic
print('STABLE_AEST_ACT_DR6_R6A_ANTI_STALE_CODE_PASS')
PY

"$BASE_PY" -m py_compile fullj_weyl/stable_aest_act_dr6_r6a_fixed_template_projection.py
echo STABLE_AEST_ACT_DR6_R6A_IMPORT_PASS

# Dedicated clean R6a Python environment.
VENV="$ROOT/.local/stable_aest_act_dr6_r6a_venv"
rm -rf "$VENV"
"$BASE_PY" -m venv "$VENV"
export PATH="$VENV/bin:$PATH"
python -m pip install --upgrade pip >/dev/null
python -m pip install numpy scipy requests tqdm >/dev/null

# Fresh exact official ACT likelihood source. Never reuse historical local ACT code.
ACTSRC="$ROOT/.local/act_dr6_lenslike_r6a_source"
rm -rf "$ACTSRC"
git clone --quiet "$ACT_REPO" "$ACTSRC"
git -C "$ACTSRC" checkout --quiet --detach "$ACT_COMMIT"
[[ "$(git -C "$ACTSRC" rev-parse HEAD)" == "$ACT_COMMIT" ]]
python -m pip install --no-deps -e "$ACTSRC" >/dev/null
export R6A_ACT_SOURCE_ROOT="$ACTSRC"

python - "$ACTSRC" "$ACT_COMMIT" <<'PY'
from pathlib import Path
import subprocess,sys
src=Path(sys.argv[1]); expected=sys.argv[2]
import act_dr6_lenslike as alike
head=subprocess.check_output(['git','-C',str(src),'rev-parse','HEAD'],text=True).strip()
assert head==expected,(head,expected)
assert Path(alike.__file__).resolve().is_relative_to(src.resolve()), (alike.__file__,src)
assert getattr(alike,'__version__',None)=='1.2.0', getattr(alike,'__version__',None)
print(f'STABLE_AEST_ACT_DR6_R6A_OFFICIAL_SOURCE_PASS head={head} internal_version={alike.__version__}')
PY

# Official v1.2 likelihood data. Cache only the official downloaded data between reruns;
# every consumed file is hashed again by the R6a science driver and the official chi2
# control must pass before projection.
DATA_CACHE="$ROOT/.local/act_dr6_lenslike_data_v1.2_cache"
PKG_DATA="$ACTSRC/act_dr6_lenslike/data"
if [[ -d "$DATA_CACHE/v1.2" ]]; then
  mkdir -p "$PKG_DATA"
  rm -rf "$PKG_DATA/v1.2"
  cp -a "$DATA_CACHE/v1.2" "$PKG_DATA/v1.2"
  echo STABLE_AEST_ACT_DR6_R6A_DATA_CACHE_REUSED
else
  python - <<'PY'
import act_dr6_lenslike as alike
alike.get_data(version='v1.2')
print('STABLE_AEST_ACT_DR6_R6A_OFFICIAL_DATA_DOWNLOAD_PASS')
PY
  [[ -d "$PKG_DATA/v1.2" ]]
  mkdir -p "$DATA_CACHE"
  cp -a "$PKG_DATA/v1.2" "$DATA_CACHE/v1.2"
fi

ENVTXT='results/stable_aest_act_dr6_r6a_environment.txt'
{
  echo "repo_head=$(git rev-parse HEAD)"
  echo "predata_lock=$PREDATA_LOCK"
  echo "r5b_postdata_lock=$R5B_POSTDATA_LOCK"
  echo "act_source_head=$(git -C "$ACTSRC" rev-parse HEAD)"
  echo "python=$(python --version 2>&1)"
  python - <<'PY'
import pathlib
import act_dr6_lenslike as a
print('act_internal_version='+str(a.__version__))
print('act_module='+str(pathlib.Path(a.__file__).resolve()))
PY
  echo '--- pip freeze ---'
  python -m pip freeze
} > "$ENVTXT"

export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
JSON='results/stable_aest_act_dr6_r6a_fixed_template_projection.json'
NPZ='results/stable_aest_act_dr6_r6a_fixed_template_projection.npz'
LOG='results/stable_aest_act_dr6_r6a_fixed_template_projection.log'
ZIP='results/stable_aest_act_dr6_r6a_fixed_template_projection_bundle.zip'
rm -f "$JSON" "$NPZ" "$LOG" "$ZIP"

set +e
python -u -m fullj_weyl.stable_aest_act_dr6_r6a_fixed_template_projection \
  --json-out "$JSON" --npz-out "$NPZ" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

python - "$ZIP" "$LOG" "$JSON" "$NPZ" "$ENVTXT" <<'PY'
from pathlib import Path
import sys,zipfile
zp=Path(sys.argv[1])
paths=[Path(x) for x in sys.argv[2:6]]+[
 Path('docs/stable_aest_act_dr6_r6a_fixed_template_projection_predata.md'),
 Path('docs/stable_aest_observable_projection_r5b_derivative_zero_postdata.md'),
 Path('fullj_weyl/stable_aest_act_dr6_r6a_fixed_template_projection.py'),
 Path('fullj_weyl/run_local_stable_aest_act_dr6_r6a_fixed_template_projection.sh'),
 Path('results/stable_aest_observable_projection_r5b_derivative_zero.json'),
 Path('results/stable_aest_observable_projection_r5b_derivative_zero.npz'),
]
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED) as zf:
    seen=set()
    for p in paths:
        if p.exists() and p not in seen:
            zf.write(p,arcname=str(p)); seen.add(p)
print('STABLE_AEST_ACT_DR6_R6A_BUNDLE='+str(zp))
PY

echo "STABLE_AEST_ACT_DR6_R6A_EXIT=$code"
echo "STABLE_AEST_ACT_DR6_R6A_LOG=$LOG"
echo "STABLE_AEST_ACT_DR6_R6A_JSON=$JSON"
echo "STABLE_AEST_ACT_DR6_R6A_NPZ=$NPZ"
echo "STABLE_AEST_ACT_DR6_R6A_ZIP=$ZIP"
exit "$code"
