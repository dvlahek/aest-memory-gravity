#!/usr/bin/env bash
set -euo pipefail

R19B1_FREEZE_COMMIT='5f33dd543f9b722438faa9659858be942287f14f'
PREREG_COMMIT='3eaefcccb6c44f2db12b24caf3bfa3c3ec16a712'
IMPLEMENTATION_COMMIT='5216c1afb9e27a24957aaade43f0857641f1b12d'
LOCK_COMMIT='f3c93050db6b545b57d5a0de32d6fd0a56f78945'

R19B1_FREEZE_BLOB='58114df328eb4d47d8e5d049bdcfea4aa9c2bdd9'
PREREG_BLOB='7749938dadb43f6cff6b974a9ee4af58bdf72a09'
IMPLEMENTATION_BLOB='f27ed8b39c1351e27d4f3b43b195ff4423e04c76'
LOCK_BLOB='bf5b7ec878eecc06ba83f51e7662080e95fa169c'

R19B1_BLOB='11a14221a4d6d5d639781134b5e55233f863b799'
R19B_BLOB='862bb139ea9ff9f85907b0457119ad2916660278'
R19A_BLOB='3322ed5cb6ed36471b5d700966d9a3fba646d2d8'
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
R19A_JSON='results/nl1c7b4_repair19a_gauge_fixed_linear_conditioning_audit.json'
R19B_JSON='results/nl1c7b4_repair19b_direct_reduced_linear_feasibility_audit.json'
R19B1_JSON='results/nl1c7b4_repair19b1_orthonormal_direct_linear_feasibility.json'

OUT='results/nl1c7b4_repair19c_orthonormal_direct_gn_nonlinear_closure.json'
STATE_NPZ='results/nl1c7b4_repair19c_orthonormal_direct_gn_lambda1_states.npz'
LOG='results/nl1c7b4_repair19c_orthonormal_direct_gn_nonlinear_closure.log'

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

for c in "$R19B1_FREEZE_COMMIT" "$PREREG_COMMIT" "$IMPLEMENTATION_COMMIT" "$LOCK_COMMIT"; do
  git merge-base --is-ancestor "$c" HEAD || { echo "LOCK ancestry failure: $c" >&2; exit 91; }
done

check_blob () {
  local p="$1" expected="$2"
  local got
  got="$(git rev-parse "HEAD:$p")"
  test "$got" = "$expected" || { echo "blob mismatch $p: $got != $expected" >&2; exit 92; }
}

check_blob docs/nl1c7b4_repair19b1_result_freeze.md "$R19B1_FREEZE_BLOB"
check_blob docs/nl1c7b4_repair19c_predata_orthonormal_direct_gn_nonlinear_closure.md "$PREREG_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair19c.py "$IMPLEMENTATION_BLOB"
check_blob docs/nl1c7b4_repair19c_implementation_lock.md "$LOCK_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair19b1.py "$R19B1_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair19b.py "$R19B_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair19a.py "$R19A_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair19.py "$R19_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair18a.py "$R18A_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair16.py "$R16_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair01.py "$R1_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair09.py "$R9_BLOB"
check_blob nl1c7b/initial_constraint_certification.py "$B4_BLOB"
check_blob nl1c7a/evaluate_identity_preserving_repair08.py "$R8_BLOB"
check_blob nl1c7a/a6_a10_spherical_reconstruction.py "$REC_BLOB"

for f in "$TRACE" "$COVERAGE" "$R15A_JSON" "$R15A_NPZ" "$R16_JSON" "$R17_JSON" "$R18_JSON" "$R18A_JSON" "$R18B_JSON" "$R18B1_JSON" "$R18C_JSON" "$R18D_JSON" "$R18D1_JSON" "$R19_JSON" "$R19A_JSON" "$R19B_JSON" "$R19B1_JSON"; do
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

echo 'NL1C7B4_REPAIR19C_LOCK_PASS'
echo "HEAD=$(git rev-parse HEAD)"
echo "REPAIR19B1_JSON_SHA256=$R19B1_JSON_SHA"

mkdir -p results
rm -f "$STATE_NPZ"

set +e
PYTHONPATH="$PWD" python nl1c7b/initial_constraint_certification_repair19c.py   --trace "$TRACE"   --coverage-json "$COVERAGE"   --repair15a-json "$R15A_JSON"   --repair15a-npz "$R15A_NPZ"   --repair16-json "$R16_JSON"   --repair17-json "$R17_JSON"   --repair18-json "$R18_JSON"   --repair18a-json "$R18A_JSON"   --repair18b-json "$R18B_JSON"   --repair18b1-json "$R18B1_JSON"   --repair18c-json "$R18C_JSON"   --repair18d-json "$R18D_JSON"   --repair18d1-json "$R18D1_JSON"   --repair19-json "$R19_JSON"   --repair19a-json "$R19A_JSON"   --repair19b-json "$R19B_JSON"   --repair19b1-json "$R19B1_JSON"   --out "$OUT"   --state-npz "$STATE_NPZ"   2>&1 | tee "$LOG"
rc=$?
set -e

echo "SCIENCE_RC=$rc"
test "$rc" -eq 0 -o "$rc" -eq 2

python - <<'PY'
import hashlib, json, pathlib
p=pathlib.Path('results/nl1c7b4_repair19c_orthonormal_direct_gn_nonlinear_closure.json')
d=json.loads(p.read_text())
print('CLASSIFICATION=',d['classification'])
print('GATES=',d['gates'])
print('SUMMARY=',d['summary'])
print('OUTPUT=',d['output'])
print()
print('CANONICAL SOLVES:')
for r in d['solve_rows']:
    print(
        'scale=',r['scale_hinv_Mpc'],'Nr=',r['Nr'],'lambda=',r['lambda'],
        '| pass=',r['pass'],
        '| it=',r['accepted_iterations'],
        '| H=',r['max_epsilon_H'],
        '| M=',r['max_epsilon_M'],
        '| Y4=',r['Y4_residual'],
        '| Qmean=',r['Qmean_residual'],
        '| C=',r['correction']['combined_norm'],
        '| fail=',r['fail_reason']
    )
print()
print('SCALING:')
for r in d['correction_scaling']:
    print(r)
print()
print('GRID:')
for r in d['two_grid_control']:
    print(r)
print()
print('BRANCH_PASS=',sum(x.get('pass',False) for x in d['branch_retests']),'/',len(d['branch_retests']))
print('JSON_SHA256=',hashlib.sha256(p.read_bytes()).hexdigest())
npz=pathlib.Path('results/nl1c7b4_repair19c_orthonormal_direct_gn_lambda1_states.npz')
if npz.exists():
    print('NPZ_BYTES=',npz.stat().st_size)
    print('NPZ_SHA256=',hashlib.sha256(npz.read_bytes()).hexdigest())
else:
    print('NPZ_ABSENT=1')
PY

exit "$rc"
