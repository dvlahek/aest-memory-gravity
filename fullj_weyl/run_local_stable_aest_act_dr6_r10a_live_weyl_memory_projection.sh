#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

PREFIT_LOCK='4c46fd21df048553b577a1927d8404bc493f649e'
IMPLEMENTATION_LOCK='af2b85cf2a4d564c7575aa9bdcdd9039ff48ba0f'
IMPLEMENTATION_BLOB='1f20aa1c636b693985c93c5f21b64328d973b0fd'
R6A_POSTDATA_LOCK='540f8f85c618209abb509e3c9c7dc188698d8e25'
R8A2_POSTDATA_LOCK='590dbc69e2823f583b157af2297e357991103c47'
R8A2_JSON_SHA='2d6289c2fbd37bebcb904dade89f64c15a009e5c7454754b39d4dcc72924ca66'
R8A2_NPZ_SHA='c81b2093a88719423e87ff5c180d790a56da6f396c0070858624879c90f26ee1'
ACT_COMMIT='b386ddbb5821c1216c709f051c9289292f174d30'
ACT_REPO='https://github.com/ACTCollaboration/act_dr6_lenslike.git'

PREFIT='docs/stable_aest_act_dr6_r10a_live_weyl_memory_projection_prefit.md'
IMPL='fullj_weyl/stable_aest_act_dr6_r10a_live_weyl_memory_projection.py'
R8JSON='results/stable_aest_cosmic_memory_r8a2_precision_qualified_tau_scan.json'
R8NPZ='results/stable_aest_cosmic_memory_r8a2_precision_qualified_tau_scan.npz'

for f in \
  "$PREFIT" "$IMPL" \
  docs/stable_aest_act_dr6_r6a_fixed_template_projection_postdata.md \
  docs/stable_aest_cosmic_memory_r8a2_precision_qualified_tau_scan_postdata.md \
  fullj_weyl/stable_aest_act_dr6_r6a_fixed_template_projection.py \
  "$R8JSON" "$R8NPZ"; do
  [[ -f "$f" ]] || { echo "STABLE_AEST_ACT_DR6_R10A_MISSING file=$f" >&2; exit 3; }
done

for lock in "$PREFIT_LOCK" "$IMPLEMENTATION_LOCK" "$R6A_POSTDATA_LOCK" "$R8A2_POSTDATA_LOCK"; do
  git merge-base --is-ancestor "$lock" HEAD || { echo "STABLE_AEST_ACT_DR6_R10A_LOCK_FAIL lock=$lock" >&2; exit 3; }
done
[[ "$(git hash-object "$IMPL")" == "$IMPLEMENTATION_BLOB" ]] || {
  echo "STABLE_AEST_ACT_DR6_R10A_IMPLEMENTATION_BLOB_FAIL" >&2; exit 3;
}
[[ "$(sha256sum "$R8JSON" | awk '{print $1}')" == "$R8A2_JSON_SHA" ]] || {
  echo "STABLE_AEST_ACT_DR6_R10A_R8A2_JSON_HASH_FAIL" >&2; exit 3;
}
[[ "$(sha256sum "$R8NPZ" | awk '{print $1}')" == "$R8A2_NPZ_SHA" ]] || {
  echo "STABLE_AEST_ACT_DR6_R10A_R8A2_NPZ_HASH_FAIL" >&2; exit 3;
}
echo "STABLE_AEST_ACT_DR6_R10A_LOCK_PASS prefit=$PREFIT_LOCK implementation=$IMPLEMENTATION_LOCK r6a=$R6A_POSTDATA_LOCK r8a2=$R8A2_POSTDATA_LOCK"

BASE_PY="$(command -v python3 || command -v python || true)"
[[ -n "$BASE_PY" ]] || { echo 'STABLE_AEST_ACT_DR6_R10A: python missing' >&2; exit 2; }
VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then "$BASE_PY" -m venv "$VENV"; fi
export PATH="$VENV/bin:$PATH"
python -m pip install numpy scipy requests tqdm >/dev/null

python -m py_compile \
  fullj_weyl/stable_aest_act_dr6_r10a_live_weyl_memory_projection.py \
  fullj_weyl/stable_aest_act_dr6_r6a_fixed_template_projection.py
echo STABLE_AEST_ACT_DR6_R10A_IMPORT_PASS

python - <<'PY'
from pathlib import Path
p=Path('fullj_weyl/stable_aest_act_dr6_r10a_live_weyl_memory_projection.py').read_text()
required=[
 'PREFIT_LOCK = "4c46fd21df048553b577a1927d8404bc493f649e"',
 'R6A_POSTDATA_LOCK = "540f8f85c618209abb509e3c9c7dc188698d8e25"',
 'R8A2_POSTDATA_LOCK = "590dbc69e2823f583b157af2297e357991103c47"',
 'R8A2_JSON_SHA256 = "2d6289c2fbd37bebcb904dade89f64c15a009e5c7454754b39d4dcc72924ca66"',
 'R8A2_NPZ_SHA256 = "c81b2093a88719423e87ff5c180d790a56da6f396c0070858624879c90f26ee1"',
 'TAUS = (10.0, 5.0, 2.5, 1.25)',
 'ETA_GRID = (0.0, 0.01, 0.025, 0.05)',
 'CENTRAL_E_TOL = 0.10',
 'CENTRAL_C_TOL = 0.995',
 'TAU_C_TOL = 0.98',
 'BASELINE_TAU_TOL = 1e-8',
 'CLS_PASS = "STABLE_AEST_ACT_DR6_R10A_LIVE_WEYL_MEMORY_PROJECTION_CERTIFIED"',
 'd25_full[idx] = c0 * T25',
 'd50_full[idx] = c0 * T50',
]
for token in required:
    assert token in p,token
for forbidden in (
 'from classy import Class', 'Class()', 'T_ckk_eta0p01', 'ckk_nominal_e0',
 'eta=10', 'Halofit', 'non_linear =', 'actplanck_baseline',
):
    assert forbidden not in p,forbidden
print('STABLE_AEST_ACT_DR6_R10A_ANTI_STALE_CODE_PASS')
PY

python - "$R8JSON" "$R8NPZ" <<'PY'
import json,sys,numpy as np
from pathlib import Path
j=json.loads(Path(sys.argv[1]).read_text())
assert j['classification']=='STABLE_AEST_COSMIC_MEMORY_R8A2_TAU_GENERALITY_CERTIFIED',j['classification']
assert j.get('diagnostic_complete') is True
assert all(j['gates'].values())
q=np.load(sys.argv[2])
assert np.array_equal(np.asarray(q['ell'],float),np.arange(40.,2001.))
for tau in (10.0,5.0,2.5,1.25):
    tag=str(float(tau)).replace('.','p')
    for key in (f'baseline_tau{tag}_ckk',f'T_tau{tag}_ckk_eps025',f'T_tau{tag}_ckk_eps05'):
        assert key in q.files,key
print('STABLE_AEST_ACT_DR6_R10A_R8A2_PARENT_PASS')
PY

# Exact official ACT source. The theory arrays are never regenerated here.
ACTSRC="$ROOT/.local/act_dr6_lenslike_r10a_source"
rm -rf "$ACTSRC"
git clone --quiet "$ACT_REPO" "$ACTSRC"
git -C "$ACTSRC" checkout --quiet --detach "$ACT_COMMIT"
[[ "$(git -C "$ACTSRC" rev-parse HEAD)" == "$ACT_COMMIT" ]]
python -m pip install --no-deps -e "$ACTSRC" >/dev/null
export R10A_ACT_SOURCE_ROOT="$ACTSRC"

python - "$ACTSRC" "$ACT_COMMIT" <<'PY'
from pathlib import Path
import subprocess,sys
src=Path(sys.argv[1]).resolve(); expected=sys.argv[2]
import act_dr6_lenslike as alike
head=subprocess.check_output(['git','-C',str(src),'rev-parse','HEAD'],text=True).strip()
assert head==expected,(head,expected)
assert Path(alike.__file__).resolve().is_relative_to(src),(alike.__file__,src)
assert getattr(alike,'__version__',None)=='1.2.0',getattr(alike,'__version__',None)
print(f'STABLE_AEST_ACT_DR6_R10A_OFFICIAL_SOURCE_PASS head={head} internal_version={alike.__version__}')
PY

DATA_CACHE="$ROOT/.local/act_dr6_lenslike_data_v1.2_cache"
PKG_DATA="$ACTSRC/act_dr6_lenslike/data"
if [[ -d "$DATA_CACHE/v1.2" ]]; then
  mkdir -p "$PKG_DATA"
  rm -rf "$PKG_DATA/v1.2"
  cp -a "$DATA_CACHE/v1.2" "$PKG_DATA/v1.2"
  echo STABLE_AEST_ACT_DR6_R10A_DATA_CACHE_REUSED
else
  python - <<'PY'
import act_dr6_lenslike as alike
alike.get_data(version='v1.2')
print('STABLE_AEST_ACT_DR6_R10A_OFFICIAL_DATA_DOWNLOAD_PASS')
PY
  [[ -d "$PKG_DATA/v1.2" ]]
  mkdir -p "$DATA_CACHE"
  cp -a "$PKG_DATA/v1.2" "$DATA_CACHE/v1.2"
fi

export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
JSON='results/stable_aest_act_dr6_r10a_live_weyl_memory_projection.json'
NPZ='results/stable_aest_act_dr6_r10a_live_weyl_memory_projection.npz'
LOG='results/stable_aest_act_dr6_r10a_live_weyl_memory_projection.log'
ENVOUT='results/stable_aest_act_dr6_r10a_environment.txt'
rm -f "$JSON" "$NPZ" "$LOG" "$ENVOUT"

{
  echo "repo_head=$(git rev-parse HEAD)"
  echo "prefit_lock=$PREFIT_LOCK"
  echo "implementation_lock=$IMPLEMENTATION_LOCK"
  echo "implementation_blob=$IMPLEMENTATION_BLOB"
  echo "r6a_postdata_lock=$R6A_POSTDATA_LOCK"
  echo "r8a2_postdata_lock=$R8A2_POSTDATA_LOCK"
  echo "act_source_head=$(git -C "$ACTSRC" rev-parse HEAD)"
  echo "python=$(python --version 2>&1)"
  python - <<'PY'
from pathlib import Path
import act_dr6_lenslike as a
print('act_internal_version='+str(a.__version__))
print('act_module='+str(Path(a.__file__).resolve()))
PY
} > "$ENVOUT"

set +e
python -u -m fullj_weyl.stable_aest_act_dr6_r10a_live_weyl_memory_projection \
  --json-out "$JSON" --npz-out "$NPZ" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

echo "STABLE_AEST_ACT_DR6_R10A_EXIT=$code"
[[ -f "$JSON" ]] && sha256sum "$JSON"
[[ -f "$NPZ" ]] && sha256sum "$NPZ"
sha256sum "$LOG"
echo "STABLE_AEST_ACT_DR6_R10A_JSON=$JSON"
echo "STABLE_AEST_ACT_DR6_R10A_NPZ=$NPZ"
echo "STABLE_AEST_ACT_DR6_R10A_LOG=$LOG"
exit "$code"
