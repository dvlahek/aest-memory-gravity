#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

PREDATA_LOCK='5d4c514799f22fe13cc0ecf9a0be4d3e2326a514'
R2E_POSTDATA_LOCK='c0fe57f73a7785c21b1fecd7455f19148d5f812d'
R5B_POSTDATA_LOCK='3242335ece23fbeb743f075a1df1aa70acaab211'
R6A_POSTDATA_LOCK='540f8f85c618209abb509e3c9c7dc188698d8e25'
R5B_JSON_SHA='26ce723e2b7b783fcd19765c9c7f01b6101992a3f09e6ee321299bf148259ca9'
R5B_NPZ_SHA='a88f99254bc1a7393e40691d5dc539bb1e1648eae1b892e43b63f593f8e367e1'
EXPECTED_CLASS_HEAD='e85808324f51fc694d12e3ed7439552a3c3f9540'
EXPECTED_MEMORY_SHA='4d5ab5dc7066d4880f06fcfc731d6534ed0ff992e3cc15fb473dddccb25a594f'

for f in \
  docs/stable_aest_cosmic_memory_r7_lookback_decomposition_predata.md \
  docs/stable_aest_growth_weyl_memory_r2e_single_hook_postdata.md \
  docs/stable_aest_observable_projection_r5b_derivative_zero_postdata.md \
  docs/stable_aest_act_dr6_r6a_fixed_template_projection_postdata.md \
  results/stable_aest_observable_projection_r5b_derivative_zero.json \
  results/stable_aest_observable_projection_r5b_derivative_zero.npz \
  results/nl1c6d2n_corrected_class_densek64_env.sh \
  fullj_weyl/stable_aest_cosmic_memory_r7_lookback_decomposition.py \
  fullj_weyl/apply_aest_stable_chi_residual_patch.py \
  fullj_weyl/apply_stable_aest_r2b_variational_patch.py \
  fullj_weyl/apply_stable_aest_r2d_full_history_patch.py \
  fullj_weyl/apply_stable_aest_r2e_single_hook_patch.py; do
  [[ -f "$f" ]] || { echo "R7: missing $f" >&2; exit 3; }
done

git merge-base --is-ancestor "$PREDATA_LOCK" HEAD
git merge-base --is-ancestor "$R2E_POSTDATA_LOCK" HEAD
git merge-base --is-ancestor "$R5B_POSTDATA_LOCK" HEAD
git merge-base --is-ancestor "$R6A_POSTDATA_LOCK" HEAD
[[ "$(sha256sum results/stable_aest_observable_projection_r5b_derivative_zero.json | awk '{print $1}')" == "$R5B_JSON_SHA" ]]
[[ "$(sha256sum results/stable_aest_observable_projection_r5b_derivative_zero.npz | awk '{print $1}')" == "$R5B_NPZ_SHA" ]]
echo "STABLE_AEST_COSMIC_MEMORY_R7_SCIENCE_LOCK_PASS predata=$PREDATA_LOCK r2e=$R2E_POSTDATA_LOCK r5b=$R5B_POSTDATA_LOCK r6a=$R6A_POSTDATA_LOCK"

BASE_PY="$(command -v python3 || true)"
[[ -n "$BASE_PY" ]] || { echo 'R7: python3 missing' >&2; exit 2; }

# Pre-run anti-stale audit: the R7 implementation must contain only the frozen
# tau=10 lookback design and must not import an ACT likelihood or a broad eta scan.
"$BASE_PY" - <<'PY'
from pathlib import Path
p=Path('fullj_weyl/stable_aest_cosmic_memory_r7_lookback_decomposition.py').read_text()
required=[
 'PREDATA_LOCK = "5d4c514799f22fe13cc0ecf9a0be4d3e2326a514"',
 'R2E_POSTDATA_LOCK = "c0fe57f73a7785c21b1fecd7455f19148d5f812d"',
 'R5B_POSTDATA_LOCK = "3242335ece23fbeb743f075a1df1aa70acaab211"',
 'R6A_POSTDATA_LOCK = "540f8f85c618209abb509e3c9c7dc188698d8e25"',
 'TAU_H0 = 10.0',
 'ORDER = 20',
 'TOL = 3e-8',
 'FULL_LAMBDAS = (30.0, -30.0, 10.0, -10.0)',
 'EPOCHS = ("ancient", "intermediate", "recent_structure", "late")',
 'if z >= 10.0:',
 'if z >= 2.0:',
 'if z >= 0.5:',
 'AEST_R2D_TRACE_ALL_K',
]
for token in required:
    assert token in p, token
for forbidden in ('act_dr6_lenslike','eta=10','nominal_e10','Halofit','actplanck_baseline'):
    assert forbidden not in p, forbidden
print('STABLE_AEST_COSMIC_MEMORY_R7_ANTI_STALE_CODE_PASS')
PY

# Dedicated clean Python environment; no historical classy wheel is reused.
VENV="$ROOT/.local/stable_aest_cosmic_memory_r7_venv"
rm -rf "$VENV"
"$BASE_PY" -m venv "$VENV"
export PATH="$VENV/bin:$PATH"
python -m pip install --upgrade pip setuptools wheel >/dev/null
python -m pip install numpy scipy cython >/dev/null
python -m py_compile \
  fullj_weyl/stable_aest_cosmic_memory_r7_lookback_decomposition.py \
  fullj_weyl/stable_aest_observable_projection_r5b_derivative_zero.py \
  fullj_weyl/apply_aest_stable_chi_residual_patch.py \
  fullj_weyl/apply_stable_aest_r2b_variational_patch.py \
  fullj_weyl/apply_stable_aest_r2d_full_history_patch.py \
  fullj_weyl/apply_stable_aest_r2e_single_hook_patch.py
echo STABLE_AEST_COSMIC_MEMORY_R7_IMPORT_PASS

python - <<'PY'
import json
from pathlib import Path
p=json.loads(Path('results/stable_aest_observable_projection_r5b_derivative_zero.json').read_text())
assert p.get('classification')=='STABLE_AEST_OBSERVABLE_PROJECTION_R5B_DERIVATIVE_ZERO_CERTIFIED',p.get('classification')
assert p.get('diagnostic_complete') is True
assert all(bool(v) for v in p.get('gates',{}).values())
print('STABLE_AEST_COSMIC_MEMORY_R7_PARENT_PASS')
PY

source results/nl1c6d2n_corrected_class_densek64_env.sh
OLD_ROOT="$NL1C6D2N_CLASS_ROOT"
[[ -d "$OLD_ROOT/.git" ]]
[[ "$(git -C "$OLD_ROOT" rev-parse HEAD)" == "$EXPECTED_CLASS_HEAD" ]]
[[ "$(sha256sum "$OLD_ROOT/source/aest_memory.c" | awk '{print $1}')" == "$EXPECTED_MEMORY_SHA" ]]
echo "STABLE_AEST_COSMIC_MEMORY_R7_OLD_PROVENANCE_PASS head=$EXPECTED_CLASS_HEAD"

# Build a completely fresh disposable R7 source from the frozen parent.
R7_ROOT="$ROOT/.local/class_corrected_e8580832_densek64_stablechi_r7lookback"
R7_PYTARGET="$ROOT/.local/classy_corrected_e8580832_densek64_stablechi_r7lookback"
rm -rf "$R7_ROOT" "$R7_PYTARGET"
cp -a "$OLD_ROOT" "$R7_ROOT"
python fullj_weyl/apply_aest_stable_chi_residual_patch.py "$R7_ROOT"
python fullj_weyl/apply_stable_aest_r2b_variational_patch.py "$R7_ROOT"
python fullj_weyl/apply_stable_aest_r2d_full_history_patch.py "$R7_ROOT"
python fullj_weyl/apply_stable_aest_r2e_single_hook_patch.py "$R7_ROOT"

HOOK='dy[pv->index_pt_E_aest] += aest_tangent_external_force(k,tau);'
TRACE='aest_r2d_trace_force(k,pba->h,tau,-0.5*a*Q_aest*Bchi_aest/pba->aest_KB);'
[[ "$(grep -Fc "$HOOK" "$R7_ROOT/source/perturbations.c")" == '1' ]]
[[ "$(grep -Fc "$TRACE" "$R7_ROOT/source/perturbations.c")" == '1' ]]
[[ "$(grep -Fc 'Bchi_aest *= pba->aest_eta;' "$R7_ROOT/source/perturbations.c")" == '1' ]]
[[ "$(grep -Fc 'E_rhs_aest -= 0.5*Q_aest*Bchi_aest;' "$R7_ROOT/source/perturbations.c")" == '1' ]]
[[ "$(grep -Ec 'double[[:space:]]+aest_tangent_external_force[[:space:]]*\(' "$R7_ROOT/source/aest_memory.c")" == '1' ]]
grep -q 'FULLJ_AEST_STABLE_CHI_RESIDUAL_V1' "$R7_ROOT/source/perturbations.c"
grep -q 'FULLJ_STABLE_AEST_R2D_FULL_HISTORY_V1' "$R7_ROOT/source/perturbations.c"
grep -q 'FULLJ_STABLE_AEST_R2E_SINGLE_HOOK_V1' "$R7_ROOT/source/perturbations.c"
echo STABLE_AEST_COSMIC_MEMORY_R7_SINGLE_HOOK_FULL_HISTORY_SOURCE_PASS

rm -rf "$R7_ROOT/build" "$R7_ROOT/python/build" "$R7_ROOT/python/classy.egg-info" 2>/dev/null || true
mkdir -p "$R7_PYTARGET"
python -m pip install --no-deps --no-build-isolation --target "$R7_PYTARGET" "$R7_ROOT"

export AEST_STABLE_R7_CLASS_ROOT="$R7_ROOT"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
unset AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE \
  AEST_R2D_TRACE_FILE AEST_R2D_TRACE_KH AEST_R2D_TRACE_ALL_K AEST_TANGENT_ALLOW_K_MISS || true

JSON='results/stable_aest_cosmic_memory_r7_lookback_decomposition.json'
NPZ='results/stable_aest_cosmic_memory_r7_lookback_decomposition.npz'
LOG='results/stable_aest_cosmic_memory_r7_lookback_decomposition.log'
FULLLOG='results/stable_aest_cosmic_memory_r7_lookback_decomposition_FULL_runner.log'
ZIP='results/stable_aest_cosmic_memory_r7_lookback_decomposition_bundle.zip'
ENVTXT='results/stable_aest_cosmic_memory_r7_environment.txt'
WORK='results/stable_aest_cosmic_memory_r7_lookback_work'
rm -f "$JSON" "$NPZ" "$LOG" "$ZIP" "$ENVTXT"
rm -rf "$WORK"

{
  echo "repo_head=$(git rev-parse HEAD)"
  echo "predata_lock=$PREDATA_LOCK"
  echo "r2e_postdata_lock=$R2E_POSTDATA_LOCK"
  echo "r5b_postdata_lock=$R5B_POSTDATA_LOCK"
  echo "r6a_postdata_lock=$R6A_POSTDATA_LOCK"
  echo "class_parent_head=$EXPECTED_CLASS_HEAD"
  echo "r7_source=$R7_ROOT"
  echo "python=$(python --version 2>&1)"
  echo '--- pip freeze ---'
  python -m pip freeze
} > "$ENVTXT"

set +e
PYTHONPATH="$R7_PYTARGET" python -u -m fullj_weyl.stable_aest_cosmic_memory_r7_lookback_decomposition \
  --json-out "$JSON" --npz-out "$NPZ" --workdir "$WORK" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

# Bundle only compact reproducibility material. The multi-million-row force tables
# stay in WORK and are represented in the bundle by their SHA/size manifest.
python - "$ZIP" "$LOG" "$JSON" "$NPZ" "$ENVTXT" "$WORK/force_manifest.json" <<'PY'
from pathlib import Path
import sys,zipfile
zp=Path(sys.argv[1])
paths=[Path(x) for x in sys.argv[2:7]]+[
 Path('docs/stable_aest_cosmic_memory_r7_lookback_decomposition_predata.md'),
 Path('docs/stable_aest_growth_weyl_memory_r2e_single_hook_postdata.md'),
 Path('docs/stable_aest_observable_projection_r5b_derivative_zero_postdata.md'),
 Path('docs/stable_aest_act_dr6_r6a_fixed_template_projection_postdata.md'),
 Path('fullj_weyl/stable_aest_cosmic_memory_r7_lookback_decomposition.py'),
 Path('fullj_weyl/run_local_stable_aest_cosmic_memory_r7_lookback_decomposition.sh'),
 Path('fullj_weyl/apply_stable_aest_r2b_variational_patch.py'),
 Path('fullj_weyl/apply_stable_aest_r2d_full_history_patch.py'),
 Path('fullj_weyl/apply_stable_aest_r2e_single_hook_patch.py'),
 Path('results/stable_aest_observable_projection_r5b_derivative_zero.json'),
 Path('results/stable_aest_observable_projection_r5b_derivative_zero.npz'),
]
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED) as zf:
    seen=set()
    for p in paths:
        if p.exists() and p not in seen:
            zf.write(p,arcname=str(p)); seen.add(p)
print('STABLE_AEST_COSMIC_MEMORY_R7_BUNDLE='+str(zp))
PY

echo "STABLE_AEST_COSMIC_MEMORY_R7_EXIT=$code"
echo "STABLE_AEST_COSMIC_MEMORY_R7_LOG=$LOG"
echo "STABLE_AEST_COSMIC_MEMORY_R7_JSON=$JSON"
echo "STABLE_AEST_COSMIC_MEMORY_R7_NPZ=$NPZ"
echo "STABLE_AEST_COSMIC_MEMORY_R7_ZIP=$ZIP"
exit "$code"
