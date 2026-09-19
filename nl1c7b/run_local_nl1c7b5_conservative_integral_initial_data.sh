#!/usr/bin/env bash
set -euo pipefail

R19C4_FREEZE_COMMIT='4237da31c972fc961a2f7c961450a529652baa51'
PREREG_COMMIT='13a1e33cc170688441fe979a277c3826952de5e0'
IMPLEMENTATION_COMMIT='f166dadd74f6df8931707eeb9bdcf567d1f0d4bb'
LOCK_COMMIT='b0c03b610522be1c6b676eaa06c836e5e4c9f9a0'

R19C4_FREEZE_BLOB='cd36b4d3d457b22a63054b78b9930c02ca117a37'
PREREG_BLOB='f03e657c5f3ec3eebd4cffef65083dc789182103'
IMPLEMENTATION_BLOB='6f94be113ef8cabe7459a8a920d8005f5b212a6c'
LOCK_BLOB='75eb60344353929941886e270a453ce047c173bc'

R2_BLOB='eff076ec9a511f64bc693dc48b07b2ce26cfbaeb'
R19_BLOB='2532094b518dfc2990fa0d77d8123d793b0107b3'
R19A_BLOB='3322ed5cb6ed36471b5d700966d9a3fba646d2d8'
R19C_BLOB='f27ed8b39c1351e27d4f3b43b195ff4423e04c76'
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
R19C4_JSON='results/nl1c7b4_repair19c4_post_first_step_derivative_scale_diagnostic.json'

OUT='results/nl1c7b5_conservative_integral_initial_data.json'
STATE='results/nl1c7b5_conservative_integral_initial_states.npz'
LOG='results/nl1c7b5_conservative_integral_initial_data.log'

R15A_JSON_SHA='596c7b13c4683840bcf40f6850356e179e77f873c3a3b42ba0b54730ae80811d'
R15A_NPZ_SHA='997d0033eeed1f3e60c1907c7938a0ea87a1cf38de6ab860340bd003d18d6e6e'
R16_JSON_SHA='a225f435ef61eaf33a1b4466eea678b23d1a221a537589bd8e2b0717ed66335b'
R19C4_JSON_SHA='a5a7416cd93120f543dbe0f8a70ddc735e9704212d7db5266de87980fe768c18'

for c in "$R19C4_FREEZE_COMMIT" "$PREREG_COMMIT" "$IMPLEMENTATION_COMMIT" "$LOCK_COMMIT"; do
  git merge-base --is-ancestor "$c" HEAD || { echo "LOCK ancestry failure: $c" >&2; exit 91; }
done

check_blob () {
  local p="$1" expected="$2"
  local got
  got="$(git rev-parse "HEAD:$p")"
  test "$got" = "$expected" || { echo "blob mismatch $p: $got != $expected" >&2; exit 92; }
}

check_blob docs/nl1c7b4_repair19c4_result_freeze.md "$R19C4_FREEZE_BLOB"
check_blob docs/nl1c7b5_predata_conservative_integral_initial_data.md "$PREREG_BLOB"
check_blob nl1c7b/conservative_integral_initial_data_b5.py "$IMPLEMENTATION_BLOB"
check_blob docs/nl1c7b5_conservative_integral_initial_data_implementation_lock.md "$LOCK_BLOB"

check_blob nl1c7b/initial_constraint_certification_repair02.py "$R2_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair19.py "$R19_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair19a.py "$R19A_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair19c.py "$R19C_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair18a.py "$R18A_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair16.py "$R16_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair01.py "$R1_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair09.py "$R9_BLOB"
check_blob nl1c7b/initial_constraint_certification.py "$B4_BLOB"
check_blob nl1c7a/evaluate_identity_preserving_repair08.py "$R8_BLOB"
check_blob nl1c7a/a6_a10_spherical_reconstruction.py "$REC_BLOB"

for f in "$TRACE" "$COVERAGE" "$R15A_JSON" "$R15A_NPZ" "$R16_JSON" "$R19C4_JSON"; do
  test -s "$f" || { echo "missing input: $f" >&2; exit 93; }
done

test "$(sha256sum "$R15A_JSON" | awk '{print $1}')" = "$R15A_JSON_SHA" || exit 94
test "$(sha256sum "$R15A_NPZ" | awk '{print $1}')" = "$R15A_NPZ_SHA" || exit 95
test "$(sha256sum "$R16_JSON" | awk '{print $1}')" = "$R16_JSON_SHA" || exit 96
test "$(sha256sum "$R19C4_JSON" | awk '{print $1}')" = "$R19C4_JSON_SHA" || exit 97

echo 'NL1C7B5_CONSERVATIVE_INITIAL_DATA_LOCK_PASS'
echo "HEAD=$(git rev-parse HEAD)"
echo "REPAIR19C4_JSON_SHA256=$R19C4_JSON_SHA"

mkdir -p results
rm -f "$STATE"

set +e
PYTHONPATH="$PWD" python nl1c7b/conservative_integral_initial_data_b5.py   --trace "$TRACE"   --coverage-json "$COVERAGE"   --repair15a-json "$R15A_JSON"   --repair15a-npz "$R15A_NPZ"   --repair16-json "$R16_JSON"   --repair19c4-json "$R19C4_JSON"   --out "$OUT"   --state-npz "$STATE"   2>&1 | tee "$LOG"
rc=$?
set -e

echo "SCIENCE_RC=$rc"
test "$rc" -eq 0 -o "$rc" -eq 2

python - <<'PY'
import hashlib, json, pathlib
p=pathlib.Path('results/nl1c7b5_conservative_integral_initial_data.json')
d=json.loads(p.read_text())
print('CLASSIFICATION=',d['classification'])
print('GATES=',d['gates'])
print('SUMMARY=',d['summary'])
print('OUTPUT=',d['output'])
print('TWO_GRID=',d['two_grid_control'])
for r in d['case_rows']:
    print()
    print('scale=',r['scale_hinv_Mpc'],'Nr=',r['Nr'],
          '| attempted=',r.get('attempted'),
          '| solver_success=',r.get('solver',{}).get('success'),
          '| solver_status=',r.get('solver',{}).get('status'),
          '| nfev=',r.get('solver',{}).get('nfev'),
          '| safety=',r.get('safety_pass'),
          '| differential_pass=',r.get('differential_constraint_pass'))
    if 'exception' in r:
        print('  EXCEPTION=',r['exception'])
        continue
    print('  conservative_initial=',r['initial_conservative'])
    print('  conservative_final=',r['final_conservative'])
    print('  exact_H=',r['max_epsilon_H'],'exact_M=',r['max_epsilon_M'])
    print('  correction=',r['correction'])
    print('  gauge=',r['Y4_residual'],r['Qmean_residual'],
          'Qerr=',r['Q_target_max_normalized_error'],
          'freeze=',r['field_freeze_pass'])
print('JSON_SHA256=',hashlib.sha256(p.read_bytes()).hexdigest())
s=pathlib.Path('results/nl1c7b5_conservative_integral_initial_states.npz')
if s.exists():
    print('STATE_NPZ_BYTES=',s.stat().st_size)
    print('STATE_NPZ_SHA256=',hashlib.sha256(s.read_bytes()).hexdigest())
else:
    print('STATE_NPZ_ABSENT=1')
PY

exit "$rc"
