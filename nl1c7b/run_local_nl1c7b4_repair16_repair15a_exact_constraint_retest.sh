#!/usr/bin/env bash
set -euo pipefail

R15A_FREEZE_COMMIT='045c5b28b74ff258dbc775057cf3e9387d47b37c'
PREREG_COMMIT='f39e797ab9c6df71fe4b026f783654eef45e3e2c'
IMPLEMENTATION_COMMIT='c31b740460f25ffd9d8cb4b60dea593ea7db8587'
LOCK_COMMIT='d3cce7fa101917828ea460858a7991cfba943d9b'

R15A_FREEZE_BLOB='2843173d5a024ad3e256b0f3eeda5f5bafae0242'
PREREG_BLOB='70f6edc9bb5e7847abc68b2947115c42757e88df'
IMPLEMENTATION_BLOB='fbd7d24f748fc398638d4eea4b7707801161e52a'
LOCK_BLOB='2e51a373ec353af4a67a5b48dac211774b28bbdc'
R9_BLOB='0cd67cecfbd590cb8819ad37314dc5b49047bc93'
R1_BLOB='253a0ae2a19a597f06358704ea276c9005973af3'
R2_BLOB='eff076ec9a511f64bc693dc48b07b2ce26cfbaeb'
B4_BLOB='8559120dc273be3174eca130ca313ed6ff5acb25'
R8_BLOB='94fb3f42a7c819b0525860f7344d5dbaff93da19'
REC_BLOB='ff383c1ddc2cb2a684e2b5dd11fde0ae811e4fac'

R15A_JSON='results/nl1c7b4_repair15a_density_q_completed_state.json'
R15A_NPZ='results/nl1c7b4_repair15a_density_q_completed_primary_states.npz'
TRACE='input/dense/nl1c7a_repair01_dense_trace.dat'
COVERAGE='input/dense/nl1c7a_repair01_dense_coverage.json'
OUT='results/nl1c7b4_repair16_repair15a_exact_constraint_retest.json'
LOG='results/nl1c7b4_repair16_repair15a_exact_constraint_retest.log'

R15A_JSON_SHA='596c7b13c4683840bcf40f6850356e179e77f873c3a3b42ba0b54730ae80811d'
R15A_NPZ_SHA='997d0033eeed1f3e60c1907c7938a0ea87a1cf38de6ab860340bd003d18d6e6e'

for c in "$R15A_FREEZE_COMMIT" "$PREREG_COMMIT" "$IMPLEMENTATION_COMMIT" "$LOCK_COMMIT"; do
  git merge-base --is-ancestor "$c" HEAD || { echo "LOCK ancestry failure: $c" >&2; exit 91; }
done

check_blob () {
  local p="$1" expected="$2"
  local got
  got="$(git rev-parse "HEAD:$p")"
  test "$got" = "$expected" || { echo "blob mismatch $p: $got != $expected" >&2; exit 92; }
}

check_blob docs/nl1c7b4_repair15a_result_freeze.md "$R15A_FREEZE_BLOB"
check_blob docs/nl1c7b4_repair16_predata_repair15a_exact_constraint_retest.md "$PREREG_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair16.py "$IMPLEMENTATION_BLOB"
check_blob docs/nl1c7b4_repair16_implementation_lock.md "$LOCK_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair09.py "$R9_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair01.py "$R1_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair02.py "$R2_BLOB"
check_blob nl1c7b/initial_constraint_certification.py "$B4_BLOB"
check_blob nl1c7a/evaluate_identity_preserving_repair08.py "$R8_BLOB"
check_blob nl1c7a/a6_a10_spherical_reconstruction.py "$REC_BLOB"

for f in "$R15A_JSON" "$R15A_NPZ" "$TRACE" "$COVERAGE"; do
  test -s "$f" || { echo "missing input: $f" >&2; exit 93; }
done

test "$(sha256sum "$R15A_JSON" | awk '{print $1}')" = "$R15A_JSON_SHA" || { echo "Repair15a JSON hash mismatch" >&2; exit 94; }
test "$(sha256sum "$R15A_NPZ" | awk '{print $1}')" = "$R15A_NPZ_SHA" || { echo "Repair15a NPZ hash mismatch" >&2; exit 95; }

echo 'NL1C7B4_REPAIR16_LOCK_PASS'
echo "HEAD=$(git rev-parse HEAD)"
echo "REPAIR15A_JSON_SHA256=$R15A_JSON_SHA"
echo "REPAIR15A_NPZ_SHA256=$R15A_NPZ_SHA"

mkdir -p results
set +e
PYTHONPATH="$PWD" python nl1c7b/initial_constraint_certification_repair16.py   --trace "$TRACE"   --coverage-json "$COVERAGE"   --repair15a-json "$R15A_JSON"   --repair15a-npz "$R15A_NPZ"   --out "$OUT"   2>&1 | tee "$LOG"
rc=$?
set -e

echo "SCIENCE_RC=$rc"
test "$rc" -eq 0 -o "$rc" -eq 2

python - <<'PY'
import hashlib, json, pathlib
p=pathlib.Path('results/nl1c7b4_repair16_repair15a_exact_constraint_retest.json')
d=json.loads(p.read_text())
print('CLASSIFICATION=', d['classification'])
print('gates=', d['gates'])
print('summary=', d['summary'])
print('state_anchor=', {
    'max_relative_L2': d['state_anchor']['max_relative_L2'],
    'scalar_identity': d['state_anchor']['scalar_canonical_vs_independent_at_ai_relative_L2'],
    'pass': d['state_anchor']['pass'],
})
print('dictionary=', {
    'symbolic_K_identity': d['symbolic_K_dictionary_identity'],
    'max_Q_target_error': d['summary']['max_Q_target_error'],
})
print()
print('REPRESENTATIVE CASES (Simple, beta=1):')
for row in d['constraint_rows']:
    if row['Y_kind']=='Simple' and row['beta0']==1.0:
        print(
            'scale=',row['scale_hinv_Mpc'],'Nr=',row['Nr'],
            '| maxH=',row['max_epsilon_H'],
            '| maxM=',row['max_epsilon_M'],
            '| rmsH=',row['rms_epsilon_H'],
            '| rmsM=',row['rms_epsilon_M'],
            '| pass=',row['constraint_pass']
        )
print()
print('GRID CONTROL (Simple, beta=1):')
for row in d['grid_control']:
    if row['Y_kind']=='Simple' and row['beta0']==1.0:
        print(
            'scale=',row['scale_hinv_Mpc'],
            '| H ratio=',row['rms_ratio_H'],
            '| M ratio=',row['rms_ratio_M'],
            '| pass=',row['pass']
        )
print('JSON_SHA256=', hashlib.sha256(p.read_bytes()).hexdigest())
PY

exit "$rc"
