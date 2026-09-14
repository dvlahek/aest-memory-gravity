#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"; mkdir -p results .local

BASE_PY="$(command -v python3 || command -v python)"
[[ -n "$BASE_PY" ]] || { echo 'STABLE_AEST_GROWTH_WEYL_MEMORY_R4: python missing' >&2; exit 2; }
VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then "$BASE_PY" -m venv "$VENV"; fi
export PATH="$VENV/bin:$PATH"
python -m pip install numpy scipy cython >/dev/null
python -m py_compile \
  fullj_weyl/stable_aest_growth_weyl_memory_r4_common_mode_mechanism.py \
  fullj_weyl/stable_aest_growth_weyl_memory_r3_scale_generality.py \
  fullj_weyl/stable_aest_growth_weyl_memory_r2.py \
  fullj_weyl/apply_aest_stable_chi_residual_patch.py
echo STABLE_AEST_GROWTH_WEYL_MEMORY_R4_IMPORT_PASS

for f in \
 docs/stable_aest_growth_weyl_memory_r4_common_mode_mechanism_predata.md \
 docs/stable_aest_growth_weyl_memory_r4_technical_repair_01.md \
 docs/stable_aest_growth_weyl_memory_r4_repair2_predata.md \
 docs/stable_aest_growth_weyl_memory_r3_scale_generality_postdata.md \
 docs/stable_aest_growth_weyl_memory_r2e_single_hook_postdata.md \
 results/stable_aest_growth_weyl_memory_r3_scale_generality.json \
 results/stable_aest_growth_weyl_memory_r2e_single_hook.json \
 results/stable_aest_finite_memory_r1c.json \
 results/fullj_aest_stable_chi_precision_floor.json \
 results/nl1c6d2n_corrected_class_densek64_env.sh; do
 [[ -f "$f" ]] || { echo "STABLE_AEST_GROWTH_WEYL_MEMORY_R4: missing $f" >&2; exit 3; }
done

PREDATA_LOCK='f742cfb33bd00ec8e1b637d7d1e7201d464fc433'
R3_POSTDATA_LOCK='8094cf2a3a40659419e64ea0c45fd27491decae3'
git merge-base --is-ancestor "$PREDATA_LOCK" HEAD
git merge-base --is-ancestor "$R3_POSTDATA_LOCK" HEAD
echo "STABLE_AEST_GROWTH_WEYL_MEMORY_R4_SCIENCE_LOCK_PASS predata=$PREDATA_LOCK r3_postdata=$R3_POSTDATA_LOCK"

python - <<'PY'
import json
from pathlib import Path
r3=json.loads(Path('results/stable_aest_growth_weyl_memory_r3_scale_generality.json').read_text())
r2e=json.loads(Path('results/stable_aest_growth_weyl_memory_r2e_single_hook.json').read_text())
r1=json.loads(Path('results/stable_aest_finite_memory_r1c.json').read_text())
h=json.loads(Path('results/fullj_aest_stable_chi_precision_floor.json').read_text())
assert r3['classification']=='STABLE_AEST_GROWTH_WEYL_MEMORY_R3_SCALE_GENERALITY_CERTIFIED',r3['classification']
assert r2e['classification']=='STABLE_AEST_GROWTH_WEYL_MEMORY_R2E_SINGLE_HOOK_ABSOLUTE_COMMON_MODE_CERTIFIED',r2e['classification']
assert r1['classification']=='STABLE_AEST_FINITE_MEMORY_R1C_LONG_RELAXATION_CERTIFIED',r1['classification']
assert h['classification']=='FULLJ_AEST_STABLE_CHI_PRECISION_FLOOR_CERTIFIED',h['classification']
print('STABLE_AEST_GROWTH_WEYL_MEMORY_R4_PARENT_PASS')
PY

source results/nl1c6d2n_corrected_class_densek64_env.sh
OLD_ROOT="$NL1C6D2N_CLASS_ROOT"
EXPECTED_CLASS_HEAD='e85808324f51fc694d12e3ed7439552a3c3f9540'
EXPECTED_MEMORY_SHA='4d5ab5dc7066d4880f06fcfc731d6534ed0ff992e3cc15fb473dddccb25a594f'
[[ "$(git -C "$OLD_ROOT" rev-parse HEAD)" == "$EXPECTED_CLASS_HEAD" ]]
[[ "$(sha256sum "$OLD_ROOT/source/aest_memory.c" | awk '{print $1}')" == "$EXPECTED_MEMORY_SHA" ]]
echo "STABLE_AEST_GROWTH_WEYL_MEMORY_R4_OLD_PROVENANCE_PASS head=$EXPECTED_CLASS_HEAD"

# R4 intentionally uses a fresh disposable source tree. Do not reuse the
# mutable shared stablechi cache because R4 audits source topology.
R4_ROOT="$ROOT/.local/class_corrected_e8580832_densek64_stablechi_r4source"
rm -rf "$R4_ROOT"
cp -a "$OLD_ROOT" "$R4_ROOT"
python fullj_weyl/apply_aest_stable_chi_residual_patch.py "$R4_ROOT"
[[ "$(git -C "$R4_ROOT" rev-parse HEAD)" == "$EXPECTED_CLASS_HEAD" ]]
[[ "$(sha256sum "$R4_ROOT/source/aest_memory.c" | awk '{print $1}')" == "$EXPECTED_MEMORY_SHA" ]]

# The frozen parent carries one dormant historical v0.19w diagnostic forcing
# hook. It is zero when AEST_TANGENT_* is unset, but R4 requires literal
# physical single-channel topology. Remove exactly that one hook in this
# disposable source only; do not change the physical memory closure.
python - "$R4_ROOT/source/perturbations.c" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]); s=p.read_text()
hook='        dy[pv->index_pt_E_aest] += aest_tangent_external_force(k,tau);'
n=s.count(hook)
if n != 1:
    raise SystemExit(f'STABLE_AEST_GROWTH_WEYL_MEMORY_R4_DIAGNOSTIC_HOOK_COUNT_FAIL count={n}')
p.write_text(s.replace(hook,'',1))
print('STABLE_AEST_GROWTH_WEYL_MEMORY_R4_DIAGNOSTIC_HOOK_NEUTRALIZED count_before=1 count_after=0')
PY

grep -q 'FULLJ_AEST_STABLE_CHI_RESIDUAL_V1' "$R4_ROOT/source/perturbations.c"
grep -q 'double chi_aest = Q_aest\*s_aest;' "$R4_ROOT/source/perturbations.c"
[[ "$(grep -Fc 'Bchi_aest *= pba->aest_eta;' "$R4_ROOT/source/perturbations.c")" -eq 1 ]]
[[ "$(grep -Fc 'E_rhs_aest -= 0.5*Q_aest*Bchi_aest;' "$R4_ROOT/source/perturbations.c")" -eq 1 ]]
HOOK='dy[pv->index_pt_E_aest] += aest_tangent_external_force(k,tau);'
[[ "$(grep -Fc "$HOOK" "$R4_ROOT/source/perturbations.c")" -eq 0 ]]
echo STABLE_AEST_GROWTH_WEYL_MEMORY_R4_SINGLE_CHANNEL_SOURCE_PASS

PYTARGET="$ROOT/.local/classy_corrected_e8580832_densek64_stablechi_r4"
rm -rf "$PYTARGET"; mkdir -p "$PYTARGET"
rm -rf "$R4_ROOT/build" "$R4_ROOT/python/build" "$R4_ROOT/python/classy.egg-info" 2>/dev/null || true
python -m pip install --no-deps --no-build-isolation --target "$PYTARGET" "$R4_ROOT"

export AEST_STABLE_CLASS_ROOT="$R4_ROOT"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
unset AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE AEST_R2D_TRACE_FILE AEST_R2D_TRACE_KH AEST_R2D_TRACE_ALL_K AEST_TANGENT_ALLOW_K_MISS AEST_ERHS_TRACE_FILE AEST_ERHS_TRACE_K || true

echo STABLE_AEST_GROWTH_WEYL_MEMORY_R4_DIRECT_FINITE_ETA_PASS
JSON='results/stable_aest_growth_weyl_memory_r4_common_mode_mechanism.json'
NPZ='results/stable_aest_growth_weyl_memory_r4_common_mode_mechanism.npz'
LOG='results/stable_aest_growth_weyl_memory_r4_common_mode_mechanism.log'
ZIP='results/stable_aest_growth_weyl_memory_r4_common_mode_mechanism_bundle.zip'
rm -f "$JSON" "$NPZ" "$LOG" "$ZIP"

set +e
PYTHONPATH="$PYTARGET" python -u -m fullj_weyl.stable_aest_growth_weyl_memory_r4_common_mode_mechanism \
 --json-out "$JSON" --npz-out "$NPZ" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

python - "$ZIP" "$LOG" "$JSON" "$NPZ" <<'PY'
from pathlib import Path
import sys,zipfile
zp=Path(sys.argv[1])
paths=[Path(x) for x in sys.argv[2:5]]+[
 Path('docs/stable_aest_growth_weyl_memory_r4_common_mode_mechanism_predata.md'),
 Path('docs/stable_aest_growth_weyl_memory_r4_technical_repair_01.md'),
 Path('docs/stable_aest_growth_weyl_memory_r4_repair2_predata.md'),
 Path('docs/stable_aest_growth_weyl_memory_r3_scale_generality_postdata.md'),
 Path('docs/stable_aest_growth_weyl_memory_r2e_single_hook_postdata.md'),
 Path('fullj_weyl/stable_aest_growth_weyl_memory_r4_common_mode_mechanism.py'),
 Path('fullj_weyl/run_local_stable_aest_growth_weyl_memory_r4_common_mode_mechanism.sh'),
 Path('fullj_weyl/stable_aest_growth_weyl_memory_r3_scale_generality.py'),
 Path('fullj_weyl/apply_aest_stable_chi_residual_patch.py'),
 Path('results/stable_aest_growth_weyl_memory_r3_scale_generality.json'),
 Path('results/stable_aest_growth_weyl_memory_r2e_single_hook.json'),
 Path('results/stable_aest_finite_memory_r1c.json'),
 Path('results/fullj_aest_stable_chi_precision_floor.json'),
 Path('results/nl1c6d2n_corrected_class_densek64_env.sh')]
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED) as zf:
 seen=set()
 for p in paths:
  if p.exists() and p not in seen:
   zf.write(p,arcname=str(p)); seen.add(p)
print('STABLE_AEST_GROWTH_WEYL_MEMORY_R4_BUNDLE='+str(zp))
PY

echo "STABLE_AEST_GROWTH_WEYL_MEMORY_R4_EXIT=$code"
echo "STABLE_AEST_GROWTH_WEYL_MEMORY_R4_LOG=$LOG"
echo "STABLE_AEST_GROWTH_WEYL_MEMORY_R4_JSON=$JSON"
echo "STABLE_AEST_GROWTH_WEYL_MEMORY_R4_NPZ=$NPZ"
echo "STABLE_AEST_GROWTH_WEYL_MEMORY_R4_ZIP=$ZIP"
exit "$code"
