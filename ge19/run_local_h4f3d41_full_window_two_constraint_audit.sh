#!/usr/bin/env bash
set -euo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
[[ "$(git branch --show-current)" == 'physics-first-gravitational-elasticity' ]] || { echo GE19_D41_WRONG_BRANCH; exit 4; }
[[ -f .venv/bin/activate ]] || { echo GE19_D41_MISSING_VENV; exit 5; }
source .venv/bin/activate
export PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$ROOT" OPENBLAS_NUM_THREADS="${OPENBLAS_NUM_THREADS:-1}"
mkdir -p results
P='results/ge19_h4f3d41_full_window_two_constraint_audit'
for f in "${P}.json" "${P}.npz" "${P}_FULL.log"; do
  [[ ! -e "$f" ]] || { echo "GE19_D41_REFUSE_OVERWRITE $f"; exit 6; }
done
python -u ge19/h4f3d41_full_window_two_constraint_audit_static_test.py
set +e
python -u -m ge19.h4f3d41_full_window_two_constraint_audit \
  --results-dir "$ROOT/results" --json-out "$ROOT/${P}.json" --npz-out "$ROOT/${P}.npz" \
  2>&1 | tee "${P}_FULL.log"
rc=${PIPESTATUS[0]}
set -e
echo "EXIT=$rc"
if [[ "$rc" -ne 0 ]]; then echo "GE19_D41_EXECUTION_FAIL rc=$rc"; exit "$rc"; fi
python - "$ROOT/${P}.json" "$ROOT/${P}.npz" <<'PYRUN'
import json,sys,numpy as np
j=json.load(open(sys.argv[1]))
assert j['classification']=='GE19_D41_FULL_CLOCK_NUMERICAL_CONSTRAINT_AUDIT_COMPLETE_PARENTS_UNCERTIFIED'
assert j['evaluated_case_node_count']==30720 and j['evaluated_propagated_endpoint_count']==30480
assert j['all_30720_original_shift_replays_pass'] and j['all_128_nodes_present'] and j['all_240_cases_per_node']
assert j['D35_m26_posthoc_momentum_representation_not_original_bitwise'] and j['D22A_original_science_FAIL_immutable']
assert j['D34_D34R1_original_m26_boundary_FAIL_immutable'] and j['source_beta_specific_Y_and_m0_retained']
assert j['no_new_evolution_or_projection'] and not j['original_action_modified'] and not j['production_H3F_source_modified']
assert not any(j[k] for k in ('H1_on_shell_verified','Noether_ward_verified','H3_full_window_certified','full_H4_Ward_certified','Z11_certified','Z20_certified','Z21_certified','lensing_licensed'))
with np.load(sys.argv[2],allow_pickle=False) as z:
 assert z['original_lapse_relative_backward_audit'].shape==(128,40,3,2)
 assert all(np.isfinite(z[k]).all() for k in ('original_shift_relative_backward_replay','original_lapse_relative_backward_audit','original_anisotropy_relative_backward_audit','original_canonical_algebraic_relative_audit'))
 assert np.all(z['original_shift_relative_backward_replay']<=1e-6)
 assert np.array_equal(z['clock_node_x'].shape,(128,))
 assert np.max(z['original_lapse_relative_backward_audit'])==j['lapse_max_relative_backward']
 assert np.max(z['original_anisotropy_relative_backward_audit'])==j['anisotropy_max_relative_backward']
 assert np.max(z['original_canonical_algebraic_relative_audit'])==j['canonical_algebraic_max_relative_report_only']
print('GE19_D41_RESULT_COMPLETE_ORIGINAL_SHIFT_ONLY_CERTIFICATE_SCOPE_PASS',flush=True)
print('GE19_D41_LAPSE_ABOVE_REPORT_ONLY',j['lapse_over_original_boundary_threshold_report_only_count'],flush=True)
PYRUN
sha256sum "${P}.json" "${P}.npz" "${P}_FULL.log"
echo GE19_D41_EXECUTION_COMPLETE
