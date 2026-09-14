#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

BASE_PY="$(command -v python3 || command -v python)"
[[ -n "$BASE_PY" ]] || { echo 'STABLE_AEST_OBSERVABLE_PROJECTION_R5A: python missing' >&2; exit 2; }
VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then
  "$BASE_PY" -m venv "$VENV"
fi
export PATH="$VENV/bin:$PATH"
python -m pip install numpy scipy cython >/dev/null
python -m py_compile \
  fullj_weyl/stable_aest_observable_projection_r5a_local_eta.py \
  fullj_weyl/aest_ulp_initial_amplitude_localization.py \
  fullj_weyl/aest_stable_chi_precision_convergence.py \
  fullj_weyl/apply_aest_stable_chi_residual_patch.py
echo STABLE_AEST_OBSERVABLE_PROJECTION_R5A_IMPORT_PASS

for f in \
  docs/stable_aest_observable_projection_r5a_local_eta_predata.md \
  docs/stable_aest_observable_projection_r5_postdata.md \
  results/stable_aest_observable_projection_r5.json \
  results/nl1c6d2n_corrected_class_densek64_env.sh; do
  [[ -f "$f" ]] || { echo "STABLE_AEST_OBSERVABLE_PROJECTION_R5A: missing $f" >&2; exit 3; }
done

PREDATA_LOCK='d728b9629866da83182f5324988dea659eb61f0d'
R5_POSTDATA_LOCK='7e02d7789c7478f56c1c63b7fa94ca59192d4ac4'
git merge-base --is-ancestor "$PREDATA_LOCK" HEAD
git merge-base --is-ancestor "$R5_POSTDATA_LOCK" HEAD
echo "STABLE_AEST_OBSERVABLE_PROJECTION_R5A_SCIENCE_LOCK_PASS predata=$PREDATA_LOCK r5_postdata=$R5_POSTDATA_LOCK"

# Static anti-stale audit: R5a must be local-eta only and must not depend on
# the earlier R4 parent or the old R5 eta=10 run labels/build tree.
python - <<'PY'
from pathlib import Path
p=Path('fullj_weyl/stable_aest_observable_projection_r5a_local_eta.py').read_text()
required=[
    'PREDATA_LOCK = "d728b9629866da83182f5324988dea659eb61f0d"',
    'R5_POSTDATA_LOCK = "7e02d7789c7478f56c1c63b7fa94ca59192d4ac4"',
    'R5_CLASS = "STABLE_AEST_OBSERVABLE_PROJECTION_R5_ETA_SCALING_FAIL"',
    'ETA_SCAN = (0.0, 0.1, 0.25, 0.5)',
    '("tight_e0p1", 0.1, TOL_TIGHT)',
]
for token in required:
    assert token in p, token
for forbidden in ('nominal_e10','tight_e10','R4_POSTDATA_LOCK','R4_JSON','stablechi_r5source'):
    assert forbidden not in p, forbidden
print('STABLE_AEST_OBSERVABLE_PROJECTION_R5A_ANTI_STALE_CODE_PASS')
PY

python - <<'PY'
import json
from pathlib import Path
r5=json.loads(Path('results/stable_aest_observable_projection_r5.json').read_text())
assert r5['classification']=='STABLE_AEST_OBSERVABLE_PROJECTION_R5_ETA_SCALING_FAIL',r5['classification']
assert r5.get('diagnostic_complete') is True,r5.get('diagnostic_complete')
assert r5['gates']['R5_G1_provenance_and_parent_lock'] is True
assert r5['gates']['R5_G2_single_channel_source_topology'] is True
assert r5['gates']['R5_G3_finite_observable_runs'] is True
assert r5['gates']['R5_G4_physical_eta_tangent_consistency'] is False
print('STABLE_AEST_OBSERVABLE_PROJECTION_R5A_PARENT_PASS')
PY

source results/nl1c6d2n_corrected_class_densek64_env.sh
OLD_ROOT="$NL1C6D2N_CLASS_ROOT"
EXPECTED_CLASS_HEAD='e85808324f51fc694d12e3ed7439552a3c3f9540'
EXPECTED_MEMORY_SHA='4d5ab5dc7066d4880f06fcfc731d6534ed0ff992e3cc15fb473dddccb25a594f'
[[ "$(git -C "$OLD_ROOT" rev-parse HEAD)" == "$EXPECTED_CLASS_HEAD" ]]
[[ "$(sha256sum "$OLD_ROOT/source/aest_memory.c" | awk '{print $1}')" == "$EXPECTED_MEMORY_SHA" ]]
echo "STABLE_AEST_OBSERVABLE_PROJECTION_R5A_OLD_PROVENANCE_PASS head=$EXPECTED_CLASS_HEAD"

# Always build a fresh disposable R5a source tree from the frozen parent.
# Never reuse R4/R5/R5a mutable CLASS build directories.
R5A_ROOT="$ROOT/.local/class_corrected_e8580832_densek64_stablechi_r5asource"
R5A_PYTARGET="$ROOT/.local/classy_corrected_e8580832_densek64_stablechi_r5a"
rm -rf "$R5A_ROOT" "$R5A_PYTARGET"
cp -a "$OLD_ROOT" "$R5A_ROOT"
python fullj_weyl/apply_aest_stable_chi_residual_patch.py "$R5A_ROOT"
[[ "$(git -C "$R5A_ROOT" rev-parse HEAD)" == "$EXPECTED_CLASS_HEAD" ]]
[[ "$(sha256sum "$R5A_ROOT/source/aest_memory.c" | awk '{print $1}')" == "$EXPECTED_MEMORY_SHA" ]]

# Frozen parent carries one dormant historical variational forcing injection.
# Remove exactly that one diagnostic line in the disposable R5a source only.
python - "$R5A_ROOT/source/perturbations.c" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]); s=p.read_text()
hook='        dy[pv->index_pt_E_aest] += aest_tangent_external_force(k,tau);'
n=s.count(hook)
if n != 1:
    raise SystemExit(f'STABLE_AEST_OBSERVABLE_PROJECTION_R5A_DIAGNOSTIC_HOOK_COUNT_FAIL count={n}')
p.write_text(s.replace(hook,'',1))
print('STABLE_AEST_OBSERVABLE_PROJECTION_R5A_DIAGNOSTIC_HOOK_NEUTRALIZED count_before=1 count_after=0')
PY

grep -q 'FULLJ_AEST_STABLE_CHI_RESIDUAL_V1' "$R5A_ROOT/source/perturbations.c"
[[ "$(grep -Fc 'Bchi_aest *= pba->aest_eta;' "$R5A_ROOT/source/perturbations.c")" -eq 1 ]]
[[ "$(grep -Fc 'E_rhs_aest -= 0.5*Q_aest*Bchi_aest;' "$R5A_ROOT/source/perturbations.c")" -eq 1 ]]
HOOK='dy[pv->index_pt_E_aest] += aest_tangent_external_force(k,tau);'
[[ "$(grep -Fc "$HOOK" "$R5A_ROOT/source/perturbations.c")" -eq 0 ]]
echo STABLE_AEST_OBSERVABLE_PROJECTION_R5A_SINGLE_CHANNEL_SOURCE_PASS

rm -rf "$R5A_ROOT/build" "$R5A_ROOT/python/build" "$R5A_ROOT/python/classy.egg-info" 2>/dev/null || true
mkdir -p "$R5A_PYTARGET"
python -m pip install --no-deps --no-build-isolation --target "$R5A_PYTARGET" "$R5A_ROOT"

export AEST_STABLE_CLASS_ROOT="$R5A_ROOT"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
unset AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE \
  AEST_R2D_TRACE_FILE AEST_R2D_TRACE_KH AEST_R2D_TRACE_ALL_K \
  AEST_TANGENT_ALLOW_K_MISS AEST_ERHS_TRACE_FILE AEST_ERHS_TRACE_K || true

echo STABLE_AEST_OBSERVABLE_PROJECTION_R5A_DIRECT_PHYSICAL_PASS

JSON='results/stable_aest_observable_projection_r5a_local_eta.json'
NPZ='results/stable_aest_observable_projection_r5a_local_eta.npz'
LOG='results/stable_aest_observable_projection_r5a_local_eta.log'
ZIP='results/stable_aest_observable_projection_r5a_local_eta_bundle.zip'
rm -f "$JSON" "$NPZ" "$LOG" "$ZIP"

set +e
PYTHONPATH="$R5A_PYTARGET" python -u -m fullj_weyl.stable_aest_observable_projection_r5a_local_eta \
  --json-out "$JSON" --npz-out "$NPZ" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

python - "$ZIP" "$LOG" "$JSON" "$NPZ" <<'PY'
from pathlib import Path
import sys,zipfile
zp=Path(sys.argv[1])
paths=[Path(x) for x in sys.argv[2:5]]+[
 Path('docs/stable_aest_observable_projection_r5a_local_eta_predata.md'),
 Path('docs/stable_aest_observable_projection_r5_postdata.md'),
 Path('fullj_weyl/stable_aest_observable_projection_r5a_local_eta.py'),
 Path('fullj_weyl/run_local_stable_aest_observable_projection_r5a_local_eta.sh'),
 Path('fullj_weyl/apply_aest_stable_chi_residual_patch.py'),
 Path('results/stable_aest_observable_projection_r5.json'),
 Path('results/nl1c6d2n_corrected_class_densek64_env.sh')]
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED) as zf:
    seen=set()
    for p in paths:
        if p.exists() and p not in seen:
            zf.write(p,arcname=str(p)); seen.add(p)
print('STABLE_AEST_OBSERVABLE_PROJECTION_R5A_BUNDLE='+str(zp))
PY

echo "STABLE_AEST_OBSERVABLE_PROJECTION_R5A_EXIT=$code"
echo "STABLE_AEST_OBSERVABLE_PROJECTION_R5A_LOG=$LOG"
echo "STABLE_AEST_OBSERVABLE_PROJECTION_R5A_JSON=$JSON"
echo "STABLE_AEST_OBSERVABLE_PROJECTION_R5A_NPZ=$NPZ"
echo "STABLE_AEST_OBSERVABLE_PROJECTION_R5A_ZIP=$ZIP"
exit "$code"
