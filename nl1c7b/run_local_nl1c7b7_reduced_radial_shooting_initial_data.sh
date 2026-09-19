#!/usr/bin/env bash
set -euo pipefail

B6_FREEZE_COMMIT='70c9fc2aa58b76bf3579260e54c6d85097769160'
B7_PREREG_COMMIT='3d77dd915b1fe1f5b26d102e8c7d9f90ec508fca'
B7_IMPLEMENTATION_COMMIT='edbda966c50bf1c2b5814f28ffd9db3a889cd474'
B7_LOCK_COMMIT='09bf77d7cb06ce4829ffc553370ba69c818c029c'

B6_FREEZE_BLOB='2d2b64f15c581f750d7553af2bb101a54b8cf991'
B7_PREREG_BLOB='f14c8bd97ebaf8817d0939b9ded54cd0c9e43166'
B7_IMPLEMENTATION_BLOB='adf268f4e49c1b8118d9bb40756269f959472b5a'
B7_LOCK_BLOB='050cab9d91b6b03e2ef292c72374d683b6b81404'

B4_BLOB='8559120dc273be3174eca130ca313ed6ff5acb25'
R1_BLOB='253a0ae2a19a597f06358704ea276c9005973af3'
R9_BLOB='0cd67cecfbd590cb8819ad37314dc5b49047bc93'
R16_BLOB='fbd7d24f748fc398638d4eea4b7707801161e52a'
R18A_BLOB='767199e8ab620f5d6dabd50d0efde9828f22048b'
R19_BLOB='2532094b518dfc2990fa0d77d8123d793b0107b3'
R19C_BLOB='f27ed8b39c1351e27d4f3b43b195ff4423e04c76'
R8_BLOB='94fb3f42a7c819b0525860f7344d5dbaff93da19'
REC_BLOB='ff383c1ddc2cb2a684e2b5dd11fde0ae811e4fac'

TRACE='input/dense/nl1c7a_repair01_dense_trace.dat'
COVERAGE='input/dense/nl1c7a_repair01_dense_coverage.json'
R15A_JSON='results/nl1c7b4_repair15a_density_q_completed_state.json'
R15A_NPZ='results/nl1c7b4_repair15a_density_q_completed_primary_states.npz'
R16_JSON='results/nl1c7b4_repair16_repair15a_exact_constraint_retest.json'
B6_JSON='results/nl1c7b6_symbolic_radial_reduction_audit.json'

OUT='results/nl1c7b7_reduced_radial_shooting_initial_data.json'
STATE='results/nl1c7b7_reduced_radial_initial_states.npz'
LOG='results/nl1c7b7_reduced_radial_shooting_initial_data.log'

R15A_JSON_SHA='596c7b13c4683840bcf40f6850356e179e77f873c3a3b42ba0b54730ae80811d'
R15A_NPZ_SHA='997d0033eeed1f3e60c1907c7938a0ea87a1cf38de6ab860340bd003d18d6e6e'
R16_JSON_SHA='a225f435ef61eaf33a1b4466eea678b23d1a221a537589bd8e2b0717ed66335b'
B6_JSON_SHA='ed1efdac5dee72d8c57cbda23d074213babd15fdf3bc7adc18e61789f862e635'

for c in "$B6_FREEZE_COMMIT" "$B7_PREREG_COMMIT" "$B7_IMPLEMENTATION_COMMIT" "$B7_LOCK_COMMIT"; do
  git merge-base --is-ancestor "$c" HEAD || { echo "LOCK ancestry failure: $c" >&2; exit 91; }
done

check_blob () {
  local p="$1" expected="$2"
  local got
  got="$(git rev-parse "HEAD:$p")"
  test "$got" = "$expected" || { echo "blob mismatch $p: $got != $expected" >&2; exit 92; }
}

check_blob docs/nl1c7b6_symbolic_radial_reduction_result_freeze.md "$B6_FREEZE_BLOB"
check_blob docs/nl1c7b7_predata_reduced_radial_shooting_initial_data.md "$B7_PREREG_BLOB"
check_blob nl1c7b/reduced_radial_initial_data_b7.py "$B7_IMPLEMENTATION_BLOB"
check_blob docs/nl1c7b7_reduced_radial_shooting_implementation_lock.md "$B7_LOCK_BLOB"

check_blob nl1c7b/initial_constraint_certification.py "$B4_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair01.py "$R1_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair09.py "$R9_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair16.py "$R16_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair18a.py "$R18A_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair19.py "$R19_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair19c.py "$R19C_BLOB"
check_blob nl1c7a/evaluate_identity_preserving_repair08.py "$R8_BLOB"
check_blob nl1c7a/a6_a10_spherical_reconstruction.py "$REC_BLOB"

for f in "$TRACE" "$COVERAGE" "$R15A_JSON" "$R15A_NPZ" "$R16_JSON" "$B6_JSON"; do
  test -s "$f" || { echo "missing input: $f" >&2; exit 93; }
done

test "$(sha256sum "$R15A_JSON" | awk '{print $1}')" = "$R15A_JSON_SHA" || exit 94
test "$(sha256sum "$R15A_NPZ" | awk '{print $1}')" = "$R15A_NPZ_SHA" || exit 95
test "$(sha256sum "$R16_JSON" | awk '{print $1}')" = "$R16_JSON_SHA" || exit 96
test "$(sha256sum "$B6_JSON" | awk '{print $1}')" = "$B6_JSON_SHA" || exit 97

echo 'NL1C7B7_REDUCED_RADIAL_SHOOTING_LOCK_PASS'
echo "HEAD=$(git rev-parse HEAD)"
echo "B6_JSON_SHA256=$B6_JSON_SHA"

mkdir -p results
rm -f "$STATE"

set +e
PYTHONPATH="$PWD" python nl1c7b/reduced_radial_initial_data_b7.py   --trace "$TRACE"   --coverage-json "$COVERAGE"   --repair15a-json "$R15A_JSON"   --repair15a-npz "$R15A_NPZ"   --repair16-json "$R16_JSON"   --b6-json "$B6_JSON"   --out "$OUT"   --state-npz "$STATE"   2>&1 | tee "$LOG"
rc=$?
set -e

echo "SCIENCE_RC=$rc"
test "$rc" -eq 0 -o "$rc" -eq 2

python - <<'PY'
import hashlib, json, pathlib
p=pathlib.Path('results/nl1c7b7_reduced_radial_shooting_initial_data.json')
d=json.loads(p.read_text())
print('CLASSIFICATION=',d['classification'])
print('GATES=',d['gates'])
print('SUMMARY=',d['summary'])
print('OUTPUT=',d['output'])
print('RHS_AUDIT=',d['rhs_audit'])
print('TWO_GRID=',d['two_grid_control'])
for r in d['case_rows']:
    print()
    print('scale=',r['scale_hinv_Mpc'],'Nr=',r['Nr'],
          '| construction=',r.get('construction_pass'),
          '| center=',r.get('center_control',{}).get('pass'),
          '| outer=',r.get('outer_Rt_compatibility',{}).get('pass'),
          '| safety=',r.get('safety_pass'),
          '| differential=',r.get('differential_constraint_pass'))
    print('  primary=',r.get('primary_launch'))
    print('  control=',r.get('control_launch'))
    if 'center_control' in r:
        print('  center_control=',r['center_control'])
    if 'outer_Rt_compatibility' in r:
        print('  outer_Rt=',r['outer_Rt_compatibility'])
    if r.get('max_epsilon_H') is not None:
        print('  exact_H=',r['max_epsilon_H'],'exact_M=',r['max_epsilon_M'])
        print('  correction=',r['correction'])
        print('  bounds=',r['max_abs_log_L_over_parent'],r['max_abs_qRt_correction'])
        print('  gauges_descriptive=',r['Y4_descriptive'],r['Qmean_descriptive'])
print('JSON_SHA256=',hashlib.sha256(p.read_bytes()).hexdigest())
s=pathlib.Path('results/nl1c7b7_reduced_radial_initial_states.npz')
if s.exists():
    print('STATE_NPZ_BYTES=',s.stat().st_size)
    print('STATE_NPZ_SHA256=',hashlib.sha256(s.read_bytes()).hexdigest())
else:
    print('STATE_NPZ_ABSENT=1')
PY

exit "$rc"
