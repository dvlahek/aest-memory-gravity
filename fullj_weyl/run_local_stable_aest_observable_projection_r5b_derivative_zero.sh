#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local

BASE_PY="$(command -v python3 || command -v python)"
[[ -n "$BASE_PY" ]] || { echo 'STABLE_AEST_OBSERVABLE_PROJECTION_R5B: python missing' >&2; exit 2; }
VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then "$BASE_PY" -m venv "$VENV"; fi
export PATH="$VENV/bin:$PATH"
python -m pip install numpy scipy cython >/dev/null
python -m py_compile \
  fullj_weyl/stable_aest_observable_projection_r5b_derivative_zero.py \
  fullj_weyl/aest_ulp_initial_amplitude_localization.py \
  fullj_weyl/aest_stable_chi_precision_convergence.py \
  fullj_weyl/apply_aest_stable_chi_residual_patch.py
echo STABLE_AEST_OBSERVABLE_PROJECTION_R5B_IMPORT_PASS

for f in \
  docs/stable_aest_observable_projection_r5b_derivative_zero_predata.md \
  docs/stable_aest_observable_projection_r5a_local_eta_postdata.md \
  results/stable_aest_observable_projection_r5a_local_eta.json \
  results/nl1c6d2n_corrected_class_densek64_env.sh; do
  [[ -f "$f" ]] || { echo "STABLE_AEST_OBSERVABLE_PROJECTION_R5B: missing $f" >&2; exit 3; }
done

PREDATA_LOCK='f6886b2b934330036e9239e3fb2d3678dee3c72f'
R5A_POSTDATA_LOCK='118c680c3c05e7ca95bbc16700bd846e200a7ab6'
git merge-base --is-ancestor "$PREDATA_LOCK" HEAD
git merge-base --is-ancestor "$R5A_POSTDATA_LOCK" HEAD
echo "STABLE_AEST_OBSERVABLE_PROJECTION_R5B_SCIENCE_LOCK_PASS predata=$PREDATA_LOCK r5a_postdata=$R5A_POSTDATA_LOCK"

# Anti-stale audit. R5b must be a new derivative-at-zero test, not copied R5/R5a science logic.
python - <<'PY'
from pathlib import Path
p=Path('fullj_weyl/stable_aest_observable_projection_r5b_derivative_zero.py').read_text()
required=[
 'PREDATA_LOCK = "f6886b2b934330036e9239e3fb2d3678dee3c72f"',
 'R5A_POSTDATA_LOCK = "118c680c3c05e7ca95bbc16700bd846e200a7ab6"',
 'R5A_CLASS = "STABLE_AEST_OBSERVABLE_PROJECTION_R5A_LOCAL_ETA_SCALING_FAIL"',
 'ETA_CERT = (0.0, 0.01, 0.025, 0.05)',
 'ETA_BRIDGE = 0.1',
 '("tight_e0p01", 0.01, TOL_TIGHT)',
 '"eta0p05_vs_eta0p1": bm',
 '"eta0p1_bridge_is_gating": False',
]
for token in required:
    assert token in p, token
for forbidden in (
 'nominal_e10','tight_e10','nominal_e0p25','nominal_e0p5',
 'R5_POSTDATA_LOCK','R4_POSTDATA_LOCK','R5_JSON =','R4_JSON =',
 'stablechi_r5source','stablechi_r5asource'
):
    assert forbidden not in p, forbidden
# Certification logic must only contain the two small-eta comparisons.
needle='derivative_pass = bool(m01_025["E"] <= 0.10 and m01_025["C"] >= 0.995\n                                   and m025_05["E"] <= 0.10 and m025_05["C"] >= 0.995)'
assert needle in p
print('STABLE_AEST_OBSERVABLE_PROJECTION_R5B_ANTI_STALE_CODE_PASS')
PY

python - <<'PY'
import json
from pathlib import Path
r=json.loads(Path('results/stable_aest_observable_projection_r5a_local_eta.json').read_text())
assert r['classification']=='STABLE_AEST_OBSERVABLE_PROJECTION_R5A_LOCAL_ETA_SCALING_FAIL',r['classification']
assert r.get('diagnostic_complete') is True
assert r['gates']['R5A_G1_provenance_and_parent_lock'] is True
assert r['gates']['R5A_G2_single_channel_source_topology'] is True
assert r['gates']['R5A_G3_finite_observable_runs'] is True
assert r['gates']['R5A_G4_smallest_eta_precision_stability'] is True
assert r['gates']['R5A_G5_local_eta_tangent_consistency'] is False
print('STABLE_AEST_OBSERVABLE_PROJECTION_R5B_PARENT_PASS')
PY

source results/nl1c6d2n_corrected_class_densek64_env.sh
OLD_ROOT="$NL1C6D2N_CLASS_ROOT"
EXPECTED_CLASS_HEAD='e85808324f51fc694d12e3ed7439552a3c3f9540'
EXPECTED_MEMORY_SHA='4d5ab5dc7066d4880f06fcfc731d6534ed0ff992e3cc15fb473dddccb25a594f'
[[ "$(git -C "$OLD_ROOT" rev-parse HEAD)" == "$EXPECTED_CLASS_HEAD" ]]
[[ "$(sha256sum "$OLD_ROOT/source/aest_memory.c" | awk '{print $1}')" == "$EXPECTED_MEMORY_SHA" ]]
echo "STABLE_AEST_OBSERVABLE_PROJECTION_R5B_OLD_PROVENANCE_PASS head=$EXPECTED_CLASS_HEAD"

# Always construct a fresh disposable source and Python target for R5b.
R5B_ROOT="$ROOT/.local/class_corrected_e8580832_densek64_stablechi_r5bsource"
R5B_PYTARGET="$ROOT/.local/classy_corrected_e8580832_densek64_stablechi_r5b"
rm -rf "$R5B_ROOT" "$R5B_PYTARGET"
cp -a "$OLD_ROOT" "$R5B_ROOT"
python fullj_weyl/apply_aest_stable_chi_residual_patch.py "$R5B_ROOT"
[[ "$(git -C "$R5B_ROOT" rev-parse HEAD)" == "$EXPECTED_CLASS_HEAD" ]]
[[ "$(sha256sum "$R5B_ROOT/source/aest_memory.c" | awk '{print $1}')" == "$EXPECTED_MEMORY_SHA" ]]

# Neutralize exactly one dormant historical variational forcing hook in the disposable tree only.
python - "$R5B_ROOT/source/perturbations.c" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]); s=p.read_text()
hook='        dy[pv->index_pt_E_aest] += aest_tangent_external_force(k,tau);'
n=s.count(hook)
if n != 1:
    raise SystemExit(f'STABLE_AEST_OBSERVABLE_PROJECTION_R5B_DIAGNOSTIC_HOOK_COUNT_FAIL count={n}')
p.write_text(s.replace(hook,'',1))
print('STABLE_AEST_OBSERVABLE_PROJECTION_R5B_DIAGNOSTIC_HOOK_NEUTRALIZED count_before=1 count_after=0')
PY

grep -q 'FULLJ_AEST_STABLE_CHI_RESIDUAL_V1' "$R5B_ROOT/source/perturbations.c"
[[ "$(grep -Fc 'Bchi_aest *= pba->aest_eta;' "$R5B_ROOT/source/perturbations.c")" -eq 1 ]]
[[ "$(grep -Fc 'E_rhs_aest -= 0.5*Q_aest*Bchi_aest;' "$R5B_ROOT/source/perturbations.c")" -eq 1 ]]
HOOK='dy[pv->index_pt_E_aest] += aest_tangent_external_force(k,tau);'
[[ "$(grep -Fc "$HOOK" "$R5B_ROOT/source/perturbations.c")" -eq 0 ]]
echo STABLE_AEST_OBSERVABLE_PROJECTION_R5B_SINGLE_CHANNEL_SOURCE_PASS

rm -rf "$R5B_ROOT/build" "$R5B_ROOT/python/build" "$R5B_ROOT/python/classy.egg-info" 2>/dev/null || true
mkdir -p "$R5B_PYTARGET"
python -m pip install --no-deps --no-build-isolation --target "$R5B_PYTARGET" "$R5B_ROOT"

export AEST_STABLE_CLASS_ROOT="$R5B_ROOT"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
unset AEST_TANGENT_FORCE_FILE AEST_TANGENT_LAMBDA AEST_TANGENT_TRACE_FILE \
  AEST_R2D_TRACE_FILE AEST_R2D_TRACE_KH AEST_R2D_TRACE_ALL_K \
  AEST_TANGENT_ALLOW_K_MISS AEST_ERHS_TRACE_FILE AEST_ERHS_TRACE_K || true

echo STABLE_AEST_OBSERVABLE_PROJECTION_R5B_DIRECT_PHYSICAL_PASS

JSON='results/stable_aest_observable_projection_r5b_derivative_zero.json'
NPZ='results/stable_aest_observable_projection_r5b_derivative_zero.npz'
LOG='results/stable_aest_observable_projection_r5b_derivative_zero.log'
ZIP='results/stable_aest_observable_projection_r5b_derivative_zero_bundle.zip'
rm -f "$JSON" "$NPZ" "$LOG" "$ZIP"

set +e
PYTHONPATH="$R5B_PYTARGET" python -u -m fullj_weyl.stable_aest_observable_projection_r5b_derivative_zero \
  --json-out "$JSON" --npz-out "$NPZ" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

python - "$ZIP" "$LOG" "$JSON" "$NPZ" <<'PY'
from pathlib import Path
import sys, zipfile
zp=Path(sys.argv[1])
paths=[Path(x) for x in sys.argv[2:5]]+[
 Path('docs/stable_aest_observable_projection_r5b_derivative_zero_predata.md'),
 Path('docs/stable_aest_observable_projection_r5a_local_eta_postdata.md'),
 Path('fullj_weyl/stable_aest_observable_projection_r5b_derivative_zero.py'),
 Path('fullj_weyl/run_local_stable_aest_observable_projection_r5b_derivative_zero.sh'),
 Path('fullj_weyl/apply_aest_stable_chi_residual_patch.py'),
 Path('results/stable_aest_observable_projection_r5a_local_eta.json'),
 Path('results/nl1c6d2n_corrected_class_densek64_env.sh')]
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED) as zf:
    seen=set()
    for p in paths:
        if p.exists() and p not in seen:
            zf.write(p,arcname=str(p)); seen.add(p)
print('STABLE_AEST_OBSERVABLE_PROJECTION_R5B_BUNDLE='+str(zp))
PY

echo "STABLE_AEST_OBSERVABLE_PROJECTION_R5B_EXIT=$code"
echo "STABLE_AEST_OBSERVABLE_PROJECTION_R5B_LOG=$LOG"
echo "STABLE_AEST_OBSERVABLE_PROJECTION_R5B_JSON=$JSON"
echo "STABLE_AEST_OBSERVABLE_PROJECTION_R5B_NPZ=$NPZ"
echo "STABLE_AEST_OBSERVABLE_PROJECTION_R5B_ZIP=$ZIP"
exit "$code"
