#!/usr/bin/env bash
set -euo pipefail

B5_FREEZE_COMMIT='2a2739db609ffb58e899baa7308199fd8dbc528b'
B6_PREREG_COMMIT='571d5bacee7a18f8c853a95769e2963c045e3e69'
B6_IMPLEMENTATION_COMMIT='2082832d6c1c838ec2093bc82068eae1f9757857'
B6_LOCK_COMMIT='5a8ac617ce9bfd0e3a48447689e742e0079a5aed'

B5_FREEZE_BLOB='05057f742b2fb5c2c9bb5cf316a047deecfd79bb'
B6_PREREG_BLOB='12ea9757ed08b9533f2877cdd186b7b07c25b7cd'
B6_IMPLEMENTATION_BLOB='4758345861dffe89baac2a1c90d5672a4ff2a7df'
B6_LOCK_BLOB='bdb1b40dd6cb12e9f0ba9f699ac6e68ca97349a9'

B4_BLOB='8559120dc273be3174eca130ca313ed6ff5acb25'
R1_BLOB='253a0ae2a19a597f06358704ea276c9005973af3'
R9_BLOB='0cd67cecfbd590cb8819ad37314dc5b49047bc93'
R16_BLOB='fbd7d24f748fc398638d4eea4b7707801161e52a'
R18A_BLOB='767199e8ab620f5d6dabd50d0efde9828f22048b'
R19C_BLOB='f27ed8b39c1351e27d4f3b43b195ff4423e04c76'
R8_BLOB='94fb3f42a7c819b0525860f7344d5dbaff93da19'
REC_BLOB='ff383c1ddc2cb2a684e2b5dd11fde0ae811e4fac'

TRACE='input/dense/nl1c7a_repair01_dense_trace.dat'
COVERAGE='input/dense/nl1c7a_repair01_dense_coverage.json'
R15A_JSON='results/nl1c7b4_repair15a_density_q_completed_state.json'
R15A_NPZ='results/nl1c7b4_repair15a_density_q_completed_primary_states.npz'
R16_JSON='results/nl1c7b4_repair16_repair15a_exact_constraint_retest.json'
B5_JSON='results/nl1c7b5_repair01_regular_center_source_limit.json'

OUT='results/nl1c7b6_symbolic_radial_reduction_audit.json'
LOG='results/nl1c7b6_symbolic_radial_reduction_audit.log'

R15A_JSON_SHA='596c7b13c4683840bcf40f6850356e179e77f873c3a3b42ba0b54730ae80811d'
R15A_NPZ_SHA='997d0033eeed1f3e60c1907c7938a0ea87a1cf38de6ab860340bd003d18d6e6e'
R16_JSON_SHA='a225f435ef61eaf33a1b4466eea678b23d1a221a537589bd8e2b0717ed66335b'
B5_JSON_SHA='bfeae8019b69f23e0fa659c6c3e0134353b85e0dcd67f0337c14d6f50b887c8d'

for c in "$B5_FREEZE_COMMIT" "$B6_PREREG_COMMIT" "$B6_IMPLEMENTATION_COMMIT" "$B6_LOCK_COMMIT"; do
  git merge-base --is-ancestor "$c" HEAD || { echo "LOCK ancestry failure: $c" >&2; exit 91; }
done

check_blob () {
  local p="$1" expected="$2"
  local got
  got="$(git rev-parse "HEAD:$p")"
  test "$got" = "$expected" || { echo "blob mismatch $p: $got != $expected" >&2; exit 92; }
}

check_blob docs/nl1c7b5_repair01_result_freeze.md "$B5_FREEZE_BLOB"
check_blob docs/nl1c7b6_predata_symbolic_radial_reduction_audit.md "$B6_PREREG_BLOB"
check_blob nl1c7b/symbolic_radial_reduction_b6.py "$B6_IMPLEMENTATION_BLOB"
check_blob docs/nl1c7b6_symbolic_radial_reduction_implementation_lock.md "$B6_LOCK_BLOB"

check_blob nl1c7b/initial_constraint_certification.py "$B4_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair01.py "$R1_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair09.py "$R9_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair16.py "$R16_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair18a.py "$R18A_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair19c.py "$R19C_BLOB"
check_blob nl1c7a/evaluate_identity_preserving_repair08.py "$R8_BLOB"
check_blob nl1c7a/a6_a10_spherical_reconstruction.py "$REC_BLOB"

for f in "$TRACE" "$COVERAGE" "$R15A_JSON" "$R15A_NPZ" "$R16_JSON" "$B5_JSON"; do
  test -s "$f" || { echo "missing input: $f" >&2; exit 93; }
done

test "$(sha256sum "$R15A_JSON" | awk '{print $1}')" = "$R15A_JSON_SHA" || exit 94
test "$(sha256sum "$R15A_NPZ" | awk '{print $1}')" = "$R15A_NPZ_SHA" || exit 95
test "$(sha256sum "$R16_JSON" | awk '{print $1}')" = "$R16_JSON_SHA" || exit 96
test "$(sha256sum "$B5_JSON" | awk '{print $1}')" = "$B5_JSON_SHA" || exit 97

echo 'NL1C7B6_SYMBOLIC_RADIAL_REDUCTION_LOCK_PASS'
echo "HEAD=$(git rev-parse HEAD)"
echo "B5_REPAIR01_JSON_SHA256=$B5_JSON_SHA"

mkdir -p results

set +e
PYTHONPATH="$PWD" python nl1c7b/symbolic_radial_reduction_b6.py   --trace "$TRACE"   --coverage-json "$COVERAGE"   --repair15a-json "$R15A_JSON"   --repair15a-npz "$R15A_NPZ"   --repair16-json "$R16_JSON"   --b5-repair01-json "$B5_JSON"   --out "$OUT"   2>&1 | tee "$LOG"
rc=$?
set -e

echo "SCIENCE_RC=$rc"
test "$rc" -eq 0 -o "$rc" -eq 2

python - <<'PY'
import hashlib, json, pathlib
p=pathlib.Path('results/nl1c7b6_symbolic_radial_reduction_audit.json')
d=json.loads(p.read_text())
print('CLASSIFICATION=',d['classification'])
print('GATES=',d['gates'])
print('SYMBOLIC_CHECKS=',d['symbolic']['checks'])
print('FORMS=',d['symbolic']['forms'])
print('PROJECT_BOUNDARY=',d['project_boundary'])
for r in d['coefficient_rows']:
    print()
    print('scale=',r['scale_hinv_Mpc'],'Nr=',r['Nr'],'pass=',r['pass'])
    print('  A_H=',r['A_H'])
    print('  A_M_4LR=',r['A_M_4LR'])
    print('  center A_H/r min,max=',
          r['center_structure']['A_H_over_r']['min'],
          r['center_structure']['A_H_over_r']['max'])
    print('  center A_M/r min,max=',
          r['center_structure']['A_M_over_r']['min'],
          r['center_structure']['A_M_over_r']['max'])
print('JSON_SHA256=',hashlib.sha256(p.read_bytes()).hexdigest())
PY

exit "$rc"
