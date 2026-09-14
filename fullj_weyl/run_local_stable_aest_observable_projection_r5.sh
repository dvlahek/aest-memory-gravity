#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"; mkdir -p results .local

BASE_PY="$(command -v python3 || command -v python)"
[[ -n "$BASE_PY" ]] || { echo 'STABLE_AEST_OBSERVABLE_PROJECTION_R5: python missing' >&2; exit 2; }
VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then "$BASE_PY" -m venv "$VENV"; fi
export PATH="$VENV/bin:$PATH"
python -m pip install numpy scipy cython >/dev/null
python -m py_compile \
  fullj_weyl/stable_aest_observable_projection_r5.py \
  fullj_weyl/stable_aest_growth_weyl_memory_r4_common_mode_mechanism.py \
  fullj_weyl/aest_ulp_initial_amplitude_localization.py \
  fullj_weyl/aest_stable_chi_precision_convergence.py \
  fullj_weyl/apply_aest_stable_chi_residual_patch.py
echo STABLE_AEST_OBSERVABLE_PROJECTION_R5_IMPORT_PASS

for f in \
 docs/stable_aest_observable_projection_r5_predata.md \
 docs/stable_aest_growth_weyl_memory_r4_common_mode_mechanism_postdata.md \
 results/stable_aest_growth_weyl_memory_r4_common_mode_mechanism.json \
 results/nl1c6d2n_corrected_class_densek64_env.sh; do
 [[ -f "$f" ]] || { echo "STABLE_AEST_OBSERVABLE_PROJECTION_R5: missing $f" >&2; exit 3; }
done

PREDATA_LOCK='773ee8b0ab1d41dc1737eaf53f1961ea2f644bde'
R4_POSTDATA_LOCK='c7c317be346371d0943e29b1b16016f9c36ef704'
git merge-base --is-ancestor "$PREDATA_LOCK" HEAD
git merge-base --is-ancestor "$R4_POSTDATA_LOCK" HEAD
echo "STABLE_AEST_OBSERVABLE_PROJECTION_R5_SCIENCE_LOCK_PASS predata=$PREDATA_LOCK r4_postdata=$R4_POSTDATA_LOCK"

python - <<'PY'
import json
from pathlib import Path
r4=json.loads(Path('results/stable_aest_growth_weyl_memory_r4_common_mode_mechanism.json').read_text())
assert r4['classification']=='STABLE_AEST_GROWTH_WEYL_MEMORY_R4_SINGLE_AMPLITUDE_MODE_CERTIFIED',r4['classification']
assert all(bool(v) for v in r4['gates'].values()),r4['gates']
print('STABLE_AEST_OBSERVABLE_PROJECTION_R5_PARENT_PASS')
PY

source results/nl1c6d2n_corrected_class_densek64_env.sh
OLD_ROOT="$NL1C6D2N_CLASS_ROOT"
EXPECTED_CLASS_HEAD='e85808324f51fc694d12e3ed7439552a3c3f9540'
EXPECTED_MEMORY_SHA='4d5ab5dc7066d4880f06fcfc731d6534ed0ff992e3cc15fb473dddccb25a594f'
[[ "$(git -C "$OLD_ROOT" rev-parse HEAD)" == "$EXPECTED_CLASS_HEAD" ]]
[[ "$(sha256sum "$OLD_ROOT/source/aest_memory.c" | awk '{print $1}')" == "$EXPECTED_MEMORY_SHA" ]]
echo "STABLE_AEST_OBSERVABLE_PROJECTION_R5_OLD_PROVENANCE_PASS head=$EXPECTED_CLASS_HEAD"

R5_ROOT="$ROOT/.local/class_corrected_e8580832_densek64_stablechi_r5source"
rm -rf "$R5_ROOT"
cp -a "$OLD_ROOT" "$R5_ROOT"
python fullj_weyl/apply_aest_stable_chi_residual_patch.py "$R5_ROOT"
[[ "$(git -C "$R5_ROOT" rev-parse HEAD)" == "$EXPECTED_CLASS_HEAD" ]]
[[ "$(sha256sum "$R5_ROOT/source/aest_memory.c" | awk '{print $1}')" == "$EXPECTED_MEMORY_SHA" ]]

# Remove the one dormant historical variational forcing injection from the
# disposable R5 science source. Physical memory equations remain untouched.
python - "$R5_ROOT/source/perturbations.c" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]); s=p.read_text()
hook='        dy[pv->index_pt_E_aest] += aest_tangent_external_force(k,tau);'
n=s.count(hook)
if n != 1:
    raise SystemExit(f'STABLE_AEST_OBSERVABLE_PROJECTION_R5_DIAGNOSTIC_HOOK_COUNT_FAIL count={n}')
p.write_text(s.replace(hook,'',1))
print('STABLE_AEST_OBSERVABLE_PROJECTION_R5_DIAGNOSTIC_HOOK_NEUTRALIZED count_before=1 count_after=0')
PY

grep -q 'FULLJ_AEST_STABLE_CHI_RESIDUAL_V1' "$R5_ROOT/source/perturbations.c"
[[ "$(grep -Fc 'Bchi_aest *= pba->aest_eta;' "$R5_ROOT/source/perturbations.c")" -eq 1 ]]
[[ "$(grep -Fc 'E_rhs_aest -= 0.5*Q_aest*Bchi_aest;' "$R5_ROOT/source/perturbations.c")" -eq 1 ]]
HOOK='dy[pv->index_pt_E_aest] += aest_tangent_external_force(k,tau);'
[[ "$(grep -Fc "$HOOK" "$R5_ROOT/source/perturbations.c")" -eq 0 ]]
echo STABLE_AEST_OBSERVABLE_PROJECTION_R5_SINGLE_CHANNEL_SOURCE_PASS

PYTARGET="$ROOT/.local/classy_corrected_e8580832_densek64_stablechi_r5"
rm -rf "$PYTARGET"; mkdir -p "$PYTARGET"
rm -rf "$R5_ROOT/build" "$R5_ROOT/python/build" "$R5_ROOT/python/classy.egg-info" 2>/dev/null || true
python -m pip install --no-deps --no-build-isolation --target "$PYTARGET" "$R5_ROOT"

export AEST_STABLE_CLASS_ROOT="$R5_ROOT"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
unset AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE AEST_R2D_TRACE_FILE AEST_R2D_TRACE_KH AEST_R2D_TRACE_ALL_K AEST_TANGENT_ALLOW_K_MISS AEST_ERHS_TRACE_FILE AEST_ERHS_TRACE_K || true

echo STABLE_AEST_OBSERVABLE_PROJECTION_R5_DIRECT_PHYSICAL_PASS
JSON='results/stable_aest_observable_projection_r5.json'
NPZ='results/stable_aest_observable_projection_r5.npz'
LOG='results/stable_aest_observable_projection_r5.log'
ZIP='results/stable_aest_observable_projection_r5_bundle.zip'
rm -f "$JSON" "$NPZ" "$LOG" "$ZIP"

set +e
PYTHONPATH="$PYTARGET" python -u -m fullj_weyl.stable_aest_observable_projection_r5 \
 --json-out "$JSON" --npz-out "$NPZ" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

python - "$ZIP" "$LOG" "$JSON" "$NPZ" <<'PY'
from pathlib import Path
import sys,zipfile
zp=Path(sys.argv[1])
paths=[Path(x) for x in sys.argv[2:5]]+[
 Path('docs/stable_aest_observable_projection_r5_predata.md'),
 Path('docs/stable_aest_growth_weyl_memory_r4_common_mode_mechanism_postdata.md'),
 Path('fullj_weyl/stable_aest_observable_projection_r5.py'),
 Path('fullj_weyl/run_local_stable_aest_observable_projection_r5.sh'),
 Path('fullj_weyl/stable_aest_growth_weyl_memory_r4_common_mode_mechanism.py'),
 Path('fullj_weyl/apply_aest_stable_chi_residual_patch.py'),
 Path('results/stable_aest_growth_weyl_memory_r4_common_mode_mechanism.json'),
 Path('results/nl1c6d2n_corrected_class_densek64_env.sh')]
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED) as zf:
 seen=set()
 for p in paths:
  if p.exists() and p not in seen:
   zf.write(p,arcname=str(p)); seen.add(p)
print('STABLE_AEST_OBSERVABLE_PROJECTION_R5_BUNDLE='+str(zp))
PY

echo "STABLE_AEST_OBSERVABLE_PROJECTION_R5_EXIT=$code"
echo "STABLE_AEST_OBSERVABLE_PROJECTION_R5_LOG=$LOG"
echo "STABLE_AEST_OBSERVABLE_PROJECTION_R5_JSON=$JSON"
echo "STABLE_AEST_OBSERVABLE_PROJECTION_R5_NPZ=$NPZ"
echo "STABLE_AEST_OBSERVABLE_PROJECTION_R5_ZIP=$ZIP"
exit "$code"
