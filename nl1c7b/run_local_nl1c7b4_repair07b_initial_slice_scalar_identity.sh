#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

# Locked ancestry.
git merge-base --is-ancestor a7bf8abe83e3cc50ecdf23ab291ed5df673b20c5 HEAD
git merge-base --is-ancestor 463bf43a41b47c7a321adf195a36acafc990df9e HEAD
git merge-base --is-ancestor 82090bc98bf96276b9f7b12c2d3a9d969e7ed5fb HEAD
git merge-base --is-ancestor 31b44a1424822013c880690068c989081d447f65 HEAD

# Locked blobs.
test "$(git rev-parse HEAD:docs/nl1c7b4_repair07b_initial_slice_scalar_identity.md)" = "7abf9c060dab3da6d3e1ee3d535e848702c6232b"
test "$(git rev-parse HEAD:nl1c7b/initial_constraint_certification_repair07b.py)" = "1b9c4f6c8cb62f1d4e6dc8cf818941288c64ed1b"
test "$(git rev-parse HEAD:nl1c7b/initial_constraint_certification_repair07a.py)" = "59cac7b5105bc779c27ce1daea9e1a52fe582cae"
test "$(git rev-parse HEAD:nl1c7b/initial_constraint_certification_repair07.py)" = "ef591df4e92b262963e928218e3932943ab9e45c"
test "$(git rev-parse HEAD:nl1c7b/initial_constraint_certification_repair05.py)" = "34fd22c73171fce5e32920a94d71d05de61521f6"
test "$(git rev-parse HEAD:nl1c7b/initial_constraint_certification.py)" = "8559120dc273be3174eca130ca313ed6ff5acb25"

echo "NL1C7B4_REPAIR07B_LOCK_PASS"

# Exact retained local inputs. These are the artifacts already downloaded for R07/R07a.
test -s input/repair06/nl1c7b4_repair06_highres_analytic_momentum.json
test -s input/final/nl1c7a_repair01_evalfix_primary_states.npz
test -s input/dense/nl1c7a_repair01_dense_trace.dat
test -s input/dense/nl1c7a_repair01_dense_coverage.json

mkdir -p results
OUT="results/nl1c7b4_repair07b_initial_slice_scalar_identity.json"
LOG="results/nl1c7b4_repair07b_initial_slice_scalar_identity.log"

set +e
PYTHONPATH="$PWD" python nl1c7b/initial_constraint_certification_repair07b.py \
  --trace input/dense/nl1c7a_repair01_dense_trace.dat \
  --coverage-json input/dense/nl1c7a_repair01_dense_coverage.json \
  --official-npz input/final/nl1c7a_repair01_evalfix_primary_states.npz \
  --parent-json input/repair06/nl1c7b4_repair06_highres_analytic_momentum.json \
  --out "$OUT" \
  2>&1 | tee "$LOG"
rc=${PIPESTATUS[0]}
set -e

echo "SCIENCE_RC=${rc}"

if [[ "$rc" -ne 0 && "$rc" -ne 2 ]]; then
  exit "$rc"
fi

python - "$OUT" <<'PY'
import json, sys
p=sys.argv[1]
d=json.load(open(p))
allowed={
  'NL1C7B4_REPAIR07B_INITIAL_SLICE_BRIDGE_DIAGNOSTIC_PASS',
  'NL1C7B4_REPAIR07B_COVARIANT_FOURIER_INTERFACE_MISMATCH',
  'NL1C7B4_REPAIR07B_IMPLEMENTATION_FAIL',
}
assert d['classification'] in allowed
assert d['locks']['eta'] == 0.0
assert d['locks']['scales_hinv_Mpc'] == [5.0,10.0,20.0]
assert d['locks']['radial_resolutions'] == [256,512]
assert abs(d['locks']['state_reproduction_limit']-1e-12) < 1e-24
assert abs(d['locks']['algebra_identity_limit']-1e-10) < 1e-22
assert abs(d['locks']['inherited_C7A_fourier_envelope']-2e-2) < 1e-15
assert abs(d['locks']['B4_raw_constraint_limit_unchanged']-1e-7) < 1e-20
assert abs(d['locks']['Repair05_06_linear_interface_limit_unchanged']-1e-5) < 1e-18
r=d['repair07b_scalar_identity_domain']
assert r['historical_full_trace_is_repair07b_gate'] is False
assert r['historical_full_trace_repair07a_pass'] is False
assert d['claim_boundary']['historical_repair07a_full_trace_failure_preserved'] is True
assert d['claim_boundary']['repair07b_changed_identity_threshold'] is False
assert d['claim_boundary']['B4_pass_claimed'] is False

print('CLASSIFICATION=', d['classification'])
print('gates=', d['gates'])
print('state_reproduction=', d['state_reproduction'])
print('scalar_domain=', d['repair07b_scalar_identity_domain'])
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
