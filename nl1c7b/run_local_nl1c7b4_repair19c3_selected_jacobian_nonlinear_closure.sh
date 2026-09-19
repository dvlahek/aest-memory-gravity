#!/usr/bin/env bash
set -euo pipefail

R19C2_FREEZE_COMMIT='5f51cae7943679f6e96dcdefc7814c0f1551e244'
PREREG_COMMIT='39d36344c9746c51f57cc2f1d85c773b62df2d3c'
IMPLEMENTATION_COMMIT='0f5ac90a7b618f9769bcdf2367aeecdec8f4217d'
LOCK_COMMIT='d4dd685940fd3eb7d4d1b1dafa5e5d33a07db3ff'

R19C2_FREEZE_BLOB='6a4df5a5e3ab71abf5339db10b358acbdd31dfa4'
PREREG_BLOB='6e7d2c2ecdad036e5755db05a1519222b2f2d264'
IMPLEMENTATION_BLOB='08985f1ee334f038a7125cc239fb6b8929d428af'
LOCK_BLOB='91777406908978fb8a9454cd40caeb44d02c82b1'

R19C_BLOB='f27ed8b39c1351e27d4f3b43b195ff4423e04c76'
R19A_BLOB='3322ed5cb6ed36471b5d700966d9a3fba646d2d8'
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
R19A_JSON='results/nl1c7b4_repair19a_gauge_fixed_linear_conditioning_audit.json'
R19B_JSON='results/nl1c7b4_repair19b_direct_reduced_linear_feasibility_audit.json'
R19B1_JSON='results/nl1c7b4_repair19b1_orthonormal_direct_linear_feasibility.json'
R19C_JSON='results/nl1c7b4_repair19c_orthonormal_direct_gn_nonlinear_closure.json'
R19C1_JSON='results/nl1c7b4_repair19c1_first_step_directional_jacobian_fidelity.json'
R19C2_JSON='results/nl1c7b4_repair19c2_finite_difference_step_scale_audit.json'

OUT='results/nl1c7b4_repair19c3_selected_jacobian_nonlinear_closure.json'
STATE='results/nl1c7b4_repair19c3_selected_jacobian_lambda1_states.npz'
LOG='results/nl1c7b4_repair19c3_selected_jacobian_nonlinear_closure.log'

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
R19A_JSON_SHA='b9b79d1fe12dff7b59d80260572129b746322412bf96ff214204f9651bd77761'
R19B_JSON_SHA='d177394b45e19ac2bca739d4ff256694c5df65e9331276e3c1b1466f4fbe5929'
R19B1_JSON_SHA='33774c721bfd15c1c2f6b776408b3fc4623e3720f9199aa04fc43e8415be1a26'
R19C_JSON_SHA='5ad02254c512f90d0f82a42d0f5aa00f15c1dae6248bdbe7ad69addb183b600a'
R19C1_JSON_SHA='b4898fed6c6bbe7d4c91f8144ed35d03e6f318b298a2fc13c0daaef038c0e3cd'
R19C2_JSON_SHA='6a724f46a70be8d23e7b9898fe6e70073879c12f77eefbdbddc63d87fb47a17c'

for c in "$R19C2_FREEZE_COMMIT" "$PREREG_COMMIT" "$IMPLEMENTATION_COMMIT" "$LOCK_COMMIT"; do
  git merge-base --is-ancestor "$c" HEAD || { echo "LOCK ancestry failure: $c" >&2; exit 91; }
done

check_blob () {
  local p="$1" expected="$2"
  local got
  got="$(git rev-parse "HEAD:$p")"
  test "$got" = "$expected" || { echo "blob mismatch $p: $got != $expected" >&2; exit 92; }
}

check_blob docs/nl1c7b4_repair19c2_result_freeze.md "$R19C2_FREEZE_BLOB"
check_blob docs/nl1c7b4_repair19c3_predata_selected_jacobian_nonlinear_closure.md "$PREREG_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair19c3.py "$IMPLEMENTATION_BLOB"
check_blob docs/nl1c7b4_repair19c3_implementation_lock.md "$LOCK_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair19c.py "$R19C_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair19a.py "$R19A_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair18a.py "$R18A_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair16.py "$R16_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair01.py "$R1_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair09.py "$R9_BLOB"
check_blob nl1c7b/initial_constraint_certification.py "$B4_BLOB"
check_blob nl1c7a/evaluate_identity_preserving_repair08.py "$R8_BLOB"
check_blob nl1c7a/a6_a10_spherical_reconstruction.py "$REC_BLOB"

for f in "$TRACE" "$COVERAGE" "$R15A_JSON" "$R15A_NPZ" "$R16_JSON" "$R17_JSON" "$R18_JSON" "$R18A_JSON" "$R18B_JSON" "$R18B1_JSON" "$R18C_JSON" "$R18D_JSON" "$R18D1_JSON" "$R19_JSON" "$R19A_JSON" "$R19B_JSON" "$R19B1_JSON" "$R19C_JSON" "$R19C1_JSON" "$R19C2_JSON"; do
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
test "$(sha256sum "$R19A_JSON" | awk '{print $1}')" = "$R19A_JSON_SHA" || exit 106
test "$(sha256sum "$R19B_JSON" | awk '{print $1}')" = "$R19B_JSON_SHA" || exit 107
test "$(sha256sum "$R19B1_JSON" | awk '{print $1}')" = "$R19B1_JSON_SHA" || exit 108
test "$(sha256sum "$R19C_JSON" | awk '{print $1}')" = "$R19C_JSON_SHA" || exit 109
test "$(sha256sum "$R19C1_JSON" | awk '{print $1}')" = "$R19C1_JSON_SHA" || exit 110
test "$(sha256sum "$R19C2_JSON" | awk '{print $1}')" = "$R19C2_JSON_SHA" || exit 111

echo 'NL1C7B4_REPAIR19C3_LOCK_PASS'
echo "HEAD=$(git rev-parse HEAD)"
echo "REPAIR19C2_JSON_SHA256=$R19C2_JSON_SHA"

mkdir -p results
rm -f "$STATE"

set +e
PYTHONPATH="$PWD" python nl1c7b/initial_constraint_certification_repair19c3.py   --trace "$TRACE"   --coverage-json "$COVERAGE"   --repair15a-json "$R15A_JSON"   --repair15a-npz "$R15A_NPZ"   --repair16-json "$R16_JSON"   --repair17-json "$R17_JSON"   --repair18-json "$R18_JSON"   --repair18a-json "$R18A_JSON"   --repair18b-json "$R18B_JSON"   --repair18b1-json "$R18B1_JSON"   --repair18c-json "$R18C_JSON"   --repair18d-json "$R18D_JSON"   --repair18d1-json "$R18D1_JSON"   --repair19-json "$R19_JSON"   --repair19a-json "$R19A_JSON"   --repair19b-json "$R19B_JSON"   --repair19b1-json "$R19B1_JSON"   --repair19c-json "$R19C_JSON"   --repair19c1-json "$R19C1_JSON"   --repair19c2-json "$R19C2_JSON"   --out "$OUT"   --state-npz "$STATE"   2>&1 | tee "$LOG"
rc=$?
set -e

echo "SCIENCE_RC=$rc"
test "$rc" -eq 0 -o "$rc" -eq 2

python - <<'PY'
import hashlib, json, pathlib
p=pathlib.Path('results/nl1c7b4_repair19c3_selected_jacobian_nonlinear_closure.json')
d=json.loads(p.read_text())
print('CLASSIFICATION=',d['classification'])
print('GATES=',d['gates'])
print('SUMMARY=',d['summary'])
print('OUTPUT=',d['output'])
for r in d['solve_rows']:
    print('scale=',r['scale_hinv_Mpc'],'Nr=',r['Nr'],'lambda=',r['lambda'],
          '| pass=',r['pass'],'| fail=',r['fail_reason'],
          '| it=',r['accepted_iterations'],
          '| H=',r['max_epsilon_H'],'| M=',r['max_epsilon_M'],
          '| yL=',r['max_abs_yL'],'| qRt=',r['max_abs_qRt'])
    if r['lambda']==1.0:
        print('  first=',r['first_step_reproduction'])
print('JSON_SHA256=',hashlib.sha256(p.read_bytes()).hexdigest())
s=pathlib.Path('results/nl1c7b4_repair19c3_selected_jacobian_lambda1_states.npz')
if s.exists():
    print('STATE_NPZ_BYTES=',s.stat().st_size)
    print('STATE_NPZ_SHA256=',hashlib.sha256(s.read_bytes()).hexdigest())
else:
    print('STATE_NPZ_ABSENT=1')
PY

exit "$rc"
