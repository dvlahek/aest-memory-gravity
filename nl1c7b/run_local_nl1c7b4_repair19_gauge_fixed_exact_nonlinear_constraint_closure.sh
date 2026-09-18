#!/usr/bin/env bash
set -euo pipefail

R18D1_FREEZE_COMMIT='814450553dc9680f13f329cb6e578350498163aa'
PREREG_COMMIT='167eb24812d539dd273e6a5185d11c6402477940'
IMPLEMENTATION_COMMIT='9a7b5eb21f54603e157098e9dc62abbb5ea1ad03'
LOCK_COMMIT='2dfc76be675870d9b11aee426521bf392155702d'

R18D1_FREEZE_BLOB='a72bd095fbb2f66bb3e398a379f847634aace3b4'
PREREG_BLOB='f9c3ccfc78c671d9459bad56b466c5f04d839f2c'
IMPLEMENTATION_BLOB='2532094b518dfc2990fa0d77d8123d793b0107b3'
LOCK_BLOB='fce1f5efc361e85181d6eaecc685fd63084c9b6a'

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

OUT='results/nl1c7b4_repair19_gauge_fixed_exact_nonlinear_constraint_closure.json'
STATE='results/nl1c7b4_repair19_gauge_fixed_exact_nonlinear_states.npz'
LOG='results/nl1c7b4_repair19_gauge_fixed_exact_nonlinear_constraint_closure.log'

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

for c in "$R18D1_FREEZE_COMMIT" "$PREREG_COMMIT" "$IMPLEMENTATION_COMMIT" "$LOCK_COMMIT"; do
  git merge-base --is-ancestor "$c" HEAD || { echo "LOCK ancestry failure: $c" >&2; exit 91; }
done

check_blob () {
  local p="$1" expected="$2"
  local got
  got="$(git rev-parse "HEAD:$p")"
  test "$got" = "$expected" || { echo "blob mismatch $p: $got != $expected" >&2; exit 92; }
}

check_blob docs/nl1c7b4_repair18d1_result_freeze.md "$R18D1_FREEZE_BLOB"
check_blob docs/nl1c7b4_repair19_predata_gauge_fixed_exact_nonlinear_constraint_closure.md "$PREREG_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair19.py "$IMPLEMENTATION_BLOB"
check_blob docs/nl1c7b4_repair19_implementation_lock.md "$LOCK_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair18a.py "$R18A_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair16.py "$R16_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair01.py "$R1_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair09.py "$R9_BLOB"
check_blob nl1c7b/initial_constraint_certification.py "$B4_BLOB"
check_blob nl1c7a/evaluate_identity_preserving_repair08.py "$R8_BLOB"
check_blob nl1c7a/a6_a10_spherical_reconstruction.py "$REC_BLOB"

for f in "$TRACE" "$COVERAGE" "$R15A_JSON" "$R15A_NPZ" "$R16_JSON" "$R17_JSON" "$R18_JSON" "$R18A_JSON" "$R18B_JSON" "$R18B1_JSON" "$R18C_JSON" "$R18D_JSON" "$R18D1_JSON"; do
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

echo 'NL1C7B4_REPAIR19_LOCK_PASS'
echo "HEAD=$(git rev-parse HEAD)"
echo "REPAIR18D1_JSON_SHA256=$R18D1_JSON_SHA"

mkdir -p results
rm -f "$STATE"

set +e
PYTHONPATH="$PWD" python nl1c7b/initial_constraint_certification_repair19.py   --trace "$TRACE"   --coverage-json "$COVERAGE"   --repair15a-json "$R15A_JSON"   --repair15a-npz "$R15A_NPZ"   --repair16-json "$R16_JSON"   --repair17-json "$R17_JSON"   --repair18-json "$R18_JSON"   --repair18a-json "$R18A_JSON"   --repair18b-json "$R18B_JSON"   --repair18b1-json "$R18B1_JSON"   --repair18c-json "$R18C_JSON"   --repair18d-json "$R18D_JSON"   --repair18d1-json "$R18D1_JSON"   --out "$OUT"   --state-npz "$STATE"   2>&1 | tee "$LOG"
rc=$?
set -e

echo "SCIENCE_RC=$rc"
test "$rc" -eq 0 -o "$rc" -eq 2

python - <<'PY'
import hashlib, json, pathlib
p=pathlib.Path('results/nl1c7b4_repair19_gauge_fixed_exact_nonlinear_constraint_closure.json')
d=json.loads(p.read_text())
print('CLASSIFICATION=',d['classification'])
print('GATES=',d['gates'])
print('SUMMARY=',d['summary'])
print('OUTPUT=',d['output'])
print()
print('LAMBDA=1 CANONICAL:')
for row in d['solve_rows']:
    if row['lambda']==1.0:
        print(
            'scale=',row['scale_hinv_Mpc'],'Nr=',row['Nr'],
            '| success=',row['solver_success'],
            '| nfev=',row['nfev'],
            '| H=',row['max_epsilon_H'],
            '| M=',row['max_epsilon_M'],
            '| Y4=',row['Y4_residual'],
            '| Qmean=',row['Qmean_residual'],
            '| C=',row['correction']['combined_norm'],
            '| pass=',row['pass']
        )
print()
print('SCALING:')
for row in d['correction_scaling']:
    print(
        'scale=',row['scale_hinv_Mpc'],'Nr=',row['Nr'],
        '| norms=',row['combined_norms'],
        '| slopes=',row['adjacent_log2_slopes'],
        '| pass=',row['gated_pass']
    )
print()
print('GRID CONTROL:')
for row in d['two_grid_correction_control']:
    print(row)
print()
print('ALL-BRANCH FAILURES:')
fails=[r for r in d['all_branch_lambda1_rows'] if not r['pass']]
print('n_fail=',len(fails))
for row in fails[:20]:
    print(row)
print('JSON_SHA256=',hashlib.sha256(p.read_bytes()).hexdigest())
s=pathlib.Path('results/nl1c7b4_repair19_gauge_fixed_exact_nonlinear_states.npz')
if s.exists():
    print('NPZ_SHA256=',hashlib.sha256(s.read_bytes()).hexdigest())
    print('NPZ_BYTES=',s.stat().st_size)
else:
    print('NPZ_WRITTEN=False')
PY

exit "$rc"
