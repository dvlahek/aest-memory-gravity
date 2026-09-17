#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

# Frozen Repair07a provenance.
git merge-base --is-ancestor 6a7971661ff612a1928413a3a4dc8ca31373dcf2 HEAD
git merge-base --is-ancestor 9fa982e454d0df4178e113e64d27cf9376aeb87f HEAD
git merge-base --is-ancestor f118ff6f28c6d4ab3ddc09019a1ec05bf7397074 HEAD

test "$(git rev-parse HEAD:docs/nl1c7b4_repair07a_thetaA_trace_bridge.md)" = "9a3a1742432bb5e93b51409dfdc7672ac1cfbf13"
test "$(git rev-parse HEAD:docs/nl1c7b4_repair07a_implementation_lock.md)" = "8ec1efa39011f6e91f65f5c525a48aef0f7b2fb5"
test "$(git rev-parse HEAD:nl1c7b/initial_constraint_certification_repair07a.py)" = "59cac7b5105bc779c27ce1daea9e1a52fe582cae"
test "$(git rev-parse HEAD:nl1c7b/initial_constraint_certification_repair07.py)" = "ef591df4e92b262963e928218e3932943ab9e45c"
test "$(git rev-parse HEAD:nl1c7b/initial_constraint_certification_repair05.py)" = "34fd22c73171fce5e32920a94d71d05de61521f6"
test "$(git rev-parse HEAD:nl1c7b/initial_constraint_certification.py)" = "8559120dc273be3174eca130ca313ed6ff5acb25"

test -s input/repair06/nl1c7b4_repair06_highres_analytic_momentum.json
test -s input/final/nl1c7a_repair01_evalfix_primary_states.npz
test -s input/dense/nl1c7a_repair01_dense_trace.dat
test -s input/dense/nl1c7a_repair01_dense_coverage.json

mkdir -p results

set +e
PYTHONPATH="$ROOT" python nl1c7b/initial_constraint_certification_repair07a.py \
  --trace input/dense/nl1c7a_repair01_dense_trace.dat \
  --coverage-json input/dense/nl1c7a_repair01_dense_coverage.json \
  --official-npz input/final/nl1c7a_repair01_evalfix_primary_states.npz \
  --parent-json input/repair06/nl1c7b4_repair06_highres_analytic_momentum.json \
  --out results/nl1c7b4_repair07a_thetaA_trace_bridge.json
rc=$?
set -e

echo "SCIENCE_RC=${rc}"
if [[ "$rc" -ne 0 && "$rc" -ne 2 ]]; then
  exit "$rc"
fi

python - <<'PY'
import json
p='results/nl1c7b4_repair07a_thetaA_trace_bridge.json'
d=json.load(open(p))
print('CLASSIFICATION=', d['classification'])
print('theta_A_bridge=', d['repair07a_theta_A_bridge'])
print('state_reproduction=', d['state_reproduction'])
print('K_symbolic=', d['symbolic_K_shift'])
print('scalar_composite=', d['scalar_composite'])
print('fourier_0i=', json.dumps(d['fourier_0i'], sort_keys=True))
for row in d['radial_diagnostics']:
    print('RADIAL', row['scale_hinv_Mpc'], row['Nr'],
          'phi_rel=', row['phi_current_vs_composite_relative_L2'],
          'K_rel=', row['K_current_vs_composite_relative_L2'],
          'GR_rel=', row['GR_R05_vs_closed_form_relative_L2'],
          'current_global=', row['current_route']['global_L2_ratio'],
          'composite_global=', row['composite_first_diagnostic_route']['global_L2_ratio'])
PY

exit "$rc"
