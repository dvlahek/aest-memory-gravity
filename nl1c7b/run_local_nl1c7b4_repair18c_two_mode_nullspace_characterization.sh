#!/usr/bin/env bash
set -euo pipefail

R18B1_FREEZE_COMMIT='77090aef851f217f194c0b977afd361bbf016682'
PREREG_COMMIT='43ddb5e99ca4289663cdbcc614389e2958810f96'
IMPLEMENTATION_COMMIT='3ac5f77991565019ac1fe216fe66b877a375579e'
LOCK_COMMIT='8eb954dde99430818cf240c31d902865224e16ec'

R18B1_FREEZE_BLOB='6ea7f986a441cfbf8256ef1bb77c52e57008d94c'
PREREG_BLOB='bf33fefaa075694f2486d01ce4c993cf6ea84da4'
IMPLEMENTATION_BLOB='719a4cff1aa793bf97443d4c5fa4ae5849d3f81c'
LOCK_BLOB='930434f76ff6bdc1ca3a2d96d3645f49a88f264a'

R18B1_BLOB='1a312dea619c46aa300cbd4c30f141d7d4b2e624'
R18A_BLOB='767199e8ab620f5d6dabd50d0efde9828f22048b'
R16_BLOB='fbd7d24f748fc398638d4eea4b7707801161e52a'
R1_BLOB='253a0ae2a19a597f06358704ea276c9005973af3'
R9_BLOB='0cd67cecfbd590cb8819ad37314dc5b49047bc93'
B4_BLOB='8559120dc273be3174eca130ca313ed6ff5acb25'
R8_BLOB='94fb3f42a7c819b0525860f7344d5dbaff93da19'
REC_BLOB='ff383c1ddc2cb2a684e2b5dd11fde0ae811e4fac'

R15A_JSON='results/nl1c7b4_repair15a_density_q_completed_state.json'
R15A_NPZ='results/nl1c7b4_repair15a_density_q_completed_primary_states.npz'
R16_JSON='results/nl1c7b4_repair16_repair15a_exact_constraint_retest.json'
R17_JSON='results/nl1c7b4_repair17_repair16_source_localization.json'
R18_JSON='results/nl1c7b4_repair18_minimal_nonlinear_projection_feasibility.json'
R18A_JSON='results/nl1c7b4_repair18a_dimensionless_rt_coordinate_feasibility.json'
R18B_JSON='results/nl1c7b4_repair18b_jacobian_fidelity_diagnostic.json'
R18B1_JSON='results/nl1c7b4_repair18b1_boolean_provenance_harness_repair.json'
TRACE='input/dense/nl1c7a_repair01_dense_trace.dat'
COVERAGE='input/dense/nl1c7a_repair01_dense_coverage.json'
OUT='results/nl1c7b4_repair18c_two_mode_nullspace_characterization.json'
LOG='results/nl1c7b4_repair18c_two_mode_nullspace_characterization.log'

R15A_JSON_SHA='596c7b13c4683840bcf40f6850356e179e77f873c3a3b42ba0b54730ae80811d'
R15A_NPZ_SHA='997d0033eeed1f3e60c1907c7938a0ea87a1cf38de6ab860340bd003d18d6e6e'
R16_JSON_SHA='a225f435ef61eaf33a1b4466eea678b23d1a221a537589bd8e2b0717ed66335b'
R17_JSON_SHA='09750aeb9fdce7bbbbe148c8478b9af5067a72ab20a1e48171f5a9e3a1d4b82e'
R18_JSON_SHA='8f8b6ce1316bd5cad3442ebd0cba692e4d4c82060685da083517b990cac36922'
R18A_JSON_SHA='29a81013b42ebe22989ca1a00b48bb2bb33447677bb77db6aefee298c7159782'
R18B_JSON_SHA='cbb68157c2408d8d52c180586db0b7d6f007c584d48c5ffc8c8d272b74a6c855'
R18B1_JSON_SHA='8e0d796e0368372d0b4cf75a075fba12ebde154b651d74929e745118c1ca6dab'

for c in "$R18B1_FREEZE_COMMIT" "$PREREG_COMMIT" "$IMPLEMENTATION_COMMIT" "$LOCK_COMMIT"; do
  git merge-base --is-ancestor "$c" HEAD || { echo "LOCK ancestry failure: $c" >&2; exit 91; }
done

check_blob () {
  local p="$1" expected="$2"
  local got
  got="$(git rev-parse "HEAD:$p")"
  test "$got" = "$expected" || { echo "blob mismatch $p: $got != $expected" >&2; exit 92; }
}

check_blob docs/nl1c7b4_repair18b1_result_freeze.md "$R18B1_FREEZE_BLOB"
check_blob docs/nl1c7b4_repair18c_predata_two_mode_nullspace_characterization.md "$PREREG_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair18c.py "$IMPLEMENTATION_BLOB"
check_blob docs/nl1c7b4_repair18c_implementation_lock.md "$LOCK_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair18b1.py "$R18B1_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair18a.py "$R18A_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair16.py "$R16_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair01.py "$R1_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair09.py "$R9_BLOB"
check_blob nl1c7b/initial_constraint_certification.py "$B4_BLOB"
check_blob nl1c7a/evaluate_identity_preserving_repair08.py "$R8_BLOB"
check_blob nl1c7a/a6_a10_spherical_reconstruction.py "$REC_BLOB"

for f in "$R15A_JSON" "$R15A_NPZ" "$R16_JSON" "$R17_JSON" "$R18_JSON" "$R18A_JSON" "$R18B_JSON" "$R18B1_JSON" "$TRACE" "$COVERAGE"; do
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

echo 'NL1C7B4_REPAIR18C_LOCK_PASS'
echo "HEAD=$(git rev-parse HEAD)"
echo "REPAIR18B1_JSON_SHA256=$R18B1_JSON_SHA"

mkdir -p results
set +e
PYTHONPATH="$PWD" python nl1c7b/initial_constraint_certification_repair18c.py   --trace "$TRACE"   --coverage-json "$COVERAGE"   --repair15a-json "$R15A_JSON"   --repair15a-npz "$R15A_NPZ"   --repair16-json "$R16_JSON"   --repair17-json "$R17_JSON"   --repair18-json "$R18_JSON"   --repair18a-json "$R18A_JSON"   --repair18b-json "$R18B_JSON"   --repair18b1-json "$R18B1_JSON"   --out "$OUT"   2>&1 | tee "$LOG"
rc=$?
set -e

echo "SCIENCE_RC=$rc"
test "$rc" -eq 0 -o "$rc" -eq 2

python - <<'PY'
import hashlib, json, pathlib
p=pathlib.Path('results/nl1c7b4_repair18c_two_mode_nullspace_characterization.json')
d=json.loads(p.read_text())
print('CLASSIFICATION=',d['classification'])
print('GATES=',d['gates'])
print('SUMMARY=',d['summary'])
for row in d['rows']:
    nl=row['null_leverage']
    print()
    print(
      'scale=',row['scale_hinv_Mpc'],
      '| rank=',row['rank'],'/',row['n_unknowns'],
      '| deficiency=',row['deficient_dimension'],
      '| yL_frac=',nl['yL_fraction_of_trace2'],
      '| qRt_frac=',nl['qRt_fraction_of_trace2'],
      '| max=',nl['max_coordinate'],
      '| left_compat=',row['left_null_compatibility']['relative_L2']
    )
    print('candidate_capture=',row['candidate_capture_fractions'])
    print('boundary_windows=',nl['boundary_windows'])
print()
print('PRINCIPAL ANGLES:')
for row in d['cross_scale_right_null_subspace']:
    print(row)
print('JSON_SHA256=',hashlib.sha256(p.read_bytes()).hexdigest())
PY

exit "$rc"
