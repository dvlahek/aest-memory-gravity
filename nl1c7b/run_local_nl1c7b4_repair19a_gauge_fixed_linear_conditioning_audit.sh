#!/usr/bin/env bash
set -euo pipefail

R19_FREEZE_COMMIT='f42b238052d9db58f8eecf7098bd83c231863612'
PREREG_COMMIT='e022993a8f006c15e8a1ab845d0dc2837d9d4adb'
IMPLEMENTATION_COMMIT='c2f8e7896096066d7e997bb6f41b05efb01706af'
LOCK_COMMIT='a30aa051c7a2629f61ededf5d34cce1196bfa4e2'

R19_FREEZE_BLOB='88e20ee5c1a52258f0b8f40af328a1f6657ca433'
PREREG_BLOB='c1fa7153cfd3621898764b5a0569b2470da65ed6'
IMPLEMENTATION_BLOB='3322ed5cb6ed36471b5d700966d9a3fba646d2d8'
LOCK_BLOB='329bcd43523e0e11e6168880385fe55677d982d5'

R19_BLOB='2532094b518dfc2990fa0d77d8123d793b0107b3'
R18A_BLOB='767199e8ab620f5d6dabd50d0efde9828f22048b'
R16_BLOB='fbd7d24f748fc398638d4eea4b7707801161e52a'
R1_BLOB='253a0ae2a19a597f06358704ea276c9005973af3'
R9_BLOB='0cd67cecfbd590cb8819ad37314dc5b49047bc93'
B4_BLOB='8559120dc273be3174eca130ca313ed6ff5acb25'
R8_BLOB='94fb3f42a7c819b0525860f7344d5dbaff93da19'
REC_BLOB='ff383c1ddc2cb2a684e2b5dd11fde0ae811e4fac'

TRACE='input/dense/nl1c7a_repair01_dense_trace.dat'
COVERAGE='input/dense/nl1c7a_repair01_dense_coverage.json'

R15A_JSON='results/nl1c7b4_repair15a_density_q_completed_state.json'
R15A_NPZ='results/nl1c7b4_repair15a_density_q_completed_primary_states.npz'
R16_JSON='results/nl1c7b4_repair16_repair15a_exact_constraint_retest.json'
R17_JSON='results/nl1c7b4_repair17_repair16_source_localization.json'
R18_JSON='results/nl1c7b4_repair18_minimal_nonlinear_projection_feasibility.json'
R18A_JSON='results/nl1c7b4_repair18a_dimensionless_rt_coordinate_feasibility.json'
R18B_JSON='results/nl1c7b4_repair18b_jacobian_fidelity_diagnostic.json'
R18B1_JSON='results/nl1c7b4_repair18b1_boolean_provenance_harness_repair.json'
R18C_JSON='results/nl1c7b4_repair18c_two_mode_nullspace_characterization.json'
R18D_JSON='results/nl1c7b4_repair18d_nullspace_transversality_audit.json'
R18D1_JSON='results/nl1c7b4_repair18d1_svd_path_reproduction_harness_repair.json'
R19_JSON='results/nl1c7b4_repair19_gauge_fixed_exact_nonlinear_constraint_closure.json'

OUT='results/nl1c7b4_repair19a_gauge_fixed_linear_conditioning_audit.json'
LOG='results/nl1c7b4_repair19a_gauge_fixed_linear_conditioning_audit.log'

R15A_JSON_SHA='596c7b13c4683840bcf40f6850356e179e77f873c3a3b42ba0b54730ae80811d'
R15A_NPZ_SHA='997d0033eeed1f3e60c1907c7938a0ea87a1cf38de6ab860340bd003d18d6e6e'
R16_JSON_SHA='a225f435ef61eaf33a1b4466eea678b23d1a221a537589bd8e2b0717ed66335b'
R17_JSON_SHA='09750aeb9fdce7bbbbe148c8478b9af5067a72ab20a1e48171f5a9e3a1d4b82e'
R18_JSON_SHA='8f8b6ce1316bd5cad3442ebd0cba692e4d4c82060685da083517b990cac36922'
R18A_JSON_SHA='29a81013b42ebe22989ca1a00b48bb2bb33447677bb77db6aefee298c7159782'
R18B_JSON_SHA='cbb68157c2408d8d52c180586db0b7d6f007c584d48c5ffc8c8d272b74a6c855'
R18B1_JSON_SHA='8e0d796e0368372d0b4cf75a075fba12ebde154b651d74929e745118c1ca6dab'
R18C_JSON_SHA='d49600f8b27536aeb0dca28d1d777d09439a376241c7f8f93b74e754c502e24b'
R18D_JSON_SHA='adc1410d50118c8080c1f84e5733cb09e5ff7d8f51a4937f1e306a96fe416def'
R18D1_JSON_SHA='21d5be34660f0054bd8550908f300de64ec1ec9e8f81e0f150c7c1540e3bf04c'
R19_JSON_SHA='ccf4a362f6a8a791f681d565881ff5728520752b1cbd93d72024b0919e1fe879'

for c in "$R19_FREEZE_COMMIT" "$PREREG_COMMIT" "$IMPLEMENTATION_COMMIT" "$LOCK_COMMIT"; do
  git merge-base --is-ancestor "$c" HEAD || { echo "LOCK ancestry failure: $c" >&2; exit 91; }
done

check_blob () {
  local p="$1" expected="$2"
  local got
  got="$(git rev-parse "HEAD:$p")"
  test "$got" = "$expected" || { echo "blob mismatch $p: $got != $expected" >&2; exit 92; }
}

check_blob docs/nl1c7b4_repair19_result_freeze.md "$R19_FREEZE_BLOB"
check_blob docs/nl1c7b4_repair19a_predata_gauge_fixed_linear_conditioning_audit.md "$PREREG_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair19a.py "$IMPLEMENTATION_BLOB"
check_blob docs/nl1c7b4_repair19a_implementation_lock.md "$LOCK_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair19.py "$R19_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair18a.py "$R18A_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair16.py "$R16_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair01.py "$R1_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair09.py "$R9_BLOB"
check_blob nl1c7b/initial_constraint_certification.py "$B4_BLOB"
check_blob nl1c7a/evaluate_identity_preserving_repair08.py "$R8_BLOB"
check_blob nl1c7a/a6_a10_spherical_reconstruction.py "$REC_BLOB"

for f in "$TRACE" "$COVERAGE" "$R15A_JSON" "$R15A_NPZ" "$R16_JSON" "$R17_JSON" "$R18_JSON" "$R18A_JSON" "$R18B_JSON" "$R18B1_JSON" "$R18C_JSON" "$R18D_JSON" "$R18D1_JSON" "$R19_JSON"; do
  test -s "$f" || { echo "missing input: $f" >&2; exit 93; }
done

test "$(sha256sum "$R15A_JSON" | awk '{print $1}')" = "$R15A_JSON_SHA" || exit 94
test "$(sha256sum "$R15A_NPZ" | awk '{print $1}')" = "$R15A_NPZ_SHA" || exit 95
test "$(sha256sum "$R16_JSON" | awk '{print $1}')" = "$R16_JSON_SHA" || exit 96
test "$(sha256sum "$R17_JSON" | awk '{print $1}')" = "$R17_JSON_SHA" || exit 97
test "$(sha256sum "$R18_JSON" | awk '{print $1}')" = "$R18_JSON_SHA" || exit 98
test "$(sha256sum "$R18A_JSON" | awk '{print $1}')" = "$R18A_JSON_SHA" || exit 99
test "$(sha256sum "$R18B_JSON" | awk '{print $1}')" = "$R18B_JSON_SHA" || exit 100
test "$(sha256sum "$R18B1_JSON" | awk '{print $1}')" = "$R18B1_JSON_SHA" || exit 101
test "$(sha256sum "$R18C_JSON" | awk '{print $1}')" = "$R18C_JSON_SHA" || exit 102
test "$(sha256sum "$R18D_JSON" | awk '{print $1}')" = "$R18D_JSON_SHA" || exit 103
test "$(sha256sum "$R18D1_JSON" | awk '{print $1}')" = "$R18D1_JSON_SHA" || exit 104
test "$(sha256sum "$R19_JSON" | awk '{print $1}')" = "$R19_JSON_SHA" || exit 105

echo 'NL1C7B4_REPAIR19A_LOCK_PASS'
echo "HEAD=$(git rev-parse HEAD)"
echo "REPAIR19_JSON_SHA256=$R19_JSON_SHA"

mkdir -p results
set +e
PYTHONPATH="$PWD" python nl1c7b/initial_constraint_certification_repair19a.py   --trace "$TRACE"   --coverage-json "$COVERAGE"   --repair15a-json "$R15A_JSON"   --repair15a-npz "$R15A_NPZ"   --repair16-json "$R16_JSON"   --repair17-json "$R17_JSON"   --repair18-json "$R18_JSON"   --repair18a-json "$R18A_JSON"   --repair18b-json "$R18B_JSON"   --repair18b1-json "$R18B1_JSON"   --repair18c-json "$R18C_JSON"   --repair18d-json "$R18D_JSON"   --repair18d1-json "$R18D1_JSON"   --repair19-json "$R19_JSON"   --out "$OUT"   2>&1 | tee "$LOG"
rc=$?
set -e

echo "SCIENCE_RC=$rc"
test "$rc" -eq 0 -o "$rc" -eq 2

python - <<'PY'
import hashlib, json, pathlib
p=pathlib.Path('results/nl1c7b4_repair19a_gauge_fixed_linear_conditioning_audit.json')
d=json.loads(p.read_text())
print('CLASSIFICATION=',d['classification'])
print('GATES=',d['gates'])
print('SUMMARY=',d['summary'])
print()
print('BASIS:')
for b in d['basis_audit']:
    print(b)
print()
print('CASES:')
for r in d['rows']:
    print(
        'scale=',r['scale_hinv_Mpc'],'Nr=',r['Nr'],
        '| chain_rel=',r['chain_linear_probe']['relative_final_linear_residual'],
        '| orth_rel=',r['orth_linear_probe']['relative_final_linear_residual'],
        '| chain_cond_est=',r['chain_linear_probe']['condA_estimate'],
        '| orth_cond_est=',r['orth_linear_probe']['condA_estimate'],
        '| dx_diff=',r['physical_dx_relative_difference'],
        '| linear_pass=',r['linear_feasibility_pass'],
        '| agree=',r['physical_dx_agreement_pass']
    )
    print(' alpha_probes=',r['exact_nonlinear_alpha_probes_orth_dx'])
print('JSON_SHA256=',hashlib.sha256(p.read_bytes()).hexdigest())
PY

exit "$rc"
