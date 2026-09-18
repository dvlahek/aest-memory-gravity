#!/usr/bin/env bash
set -euo pipefail

R16_FREEZE_COMMIT='af47a7c33c0f09744b98828e0727279b1c3d6475'
PREREG_COMMIT='ef7e23770590ab70691feb701e33a4a6624e7ad8'
IMPLEMENTATION_COMMIT='9bb8afef7ca657d35b2e8737020c508982dde551'
LOCK_COMMIT='f5e9aed806861d22ee83e7c079a3e6b36263c5ad'

R16_FREEZE_BLOB='c5456a8947e33d5625a29ddeb600ca3c9236bfda'
PREREG_BLOB='3a7471d6c5b9704656880b7e8578e403bedc60cb'
IMPLEMENTATION_BLOB='c39d9e7bc20eef55fbd0bcea2bd19f42d8cfd8b5'
LOCK_BLOB='d8c16933a70ecf420d50a816bb3657486921f5dd'
R16_BLOB='fbd7d24f748fc398638d4eea4b7707801161e52a'
R10_BLOB='c72a85d6d42176fb8c6a5ebf5f8e101541272701'
R9_BLOB='0cd67cecfbd590cb8819ad37314dc5b49047bc93'
R1_BLOB='253a0ae2a19a597f06358704ea276c9005973af3'
B4_BLOB='8559120dc273be3174eca130ca313ed6ff5acb25'
R8_BLOB='94fb3f42a7c819b0525860f7344d5dbaff93da19'
REC_BLOB='ff383c1ddc2cb2a684e2b5dd11fde0ae811e4fac'

R15A_JSON='results/nl1c7b4_repair15a_density_q_completed_state.json'
R15A_NPZ='results/nl1c7b4_repair15a_density_q_completed_primary_states.npz'
R16_JSON='results/nl1c7b4_repair16_repair15a_exact_constraint_retest.json'
TRACE='input/dense/nl1c7a_repair01_dense_trace.dat'
COVERAGE='input/dense/nl1c7a_repair01_dense_coverage.json'
OUT='results/nl1c7b4_repair17_repair16_source_localization.json'
LOG='results/nl1c7b4_repair17_repair16_source_localization.log'

R15A_JSON_SHA='596c7b13c4683840bcf40f6850356e179e77f873c3a3b42ba0b54730ae80811d'
R15A_NPZ_SHA='997d0033eeed1f3e60c1907c7938a0ea87a1cf38de6ab860340bd003d18d6e6e'
R16_JSON_SHA='a225f435ef61eaf33a1b4466eea678b23d1a221a537589bd8e2b0717ed66335b'

for c in "$R16_FREEZE_COMMIT" "$PREREG_COMMIT" "$IMPLEMENTATION_COMMIT" "$LOCK_COMMIT"; do
  git merge-base --is-ancestor "$c" HEAD || { echo "LOCK ancestry failure: $c" >&2; exit 91; }
done

check_blob () {
  local p="$1" expected="$2"
  local got
  got="$(git rev-parse "HEAD:$p")"
  test "$got" = "$expected" || { echo "blob mismatch $p: $got != $expected" >&2; exit 92; }
}

check_blob docs/nl1c7b4_repair16_result_freeze.md "$R16_FREEZE_BLOB"
check_blob docs/nl1c7b4_repair17_predata_repair16_source_localization.md "$PREREG_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair17.py "$IMPLEMENTATION_BLOB"
check_blob docs/nl1c7b4_repair17_implementation_lock.md "$LOCK_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair16.py "$R16_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair10.py "$R10_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair09.py "$R9_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair01.py "$R1_BLOB"
check_blob nl1c7b/initial_constraint_certification.py "$B4_BLOB"
check_blob nl1c7a/evaluate_identity_preserving_repair08.py "$R8_BLOB"
check_blob nl1c7a/a6_a10_spherical_reconstruction.py "$REC_BLOB"

for f in "$R15A_JSON" "$R15A_NPZ" "$R16_JSON" "$TRACE" "$COVERAGE"; do
  test -s "$f" || { echo "missing input: $f" >&2; exit 93; }
done

test "$(sha256sum "$R15A_JSON" | awk '{print $1}')" = "$R15A_JSON_SHA" || exit 94
test "$(sha256sum "$R15A_NPZ" | awk '{print $1}')" = "$R15A_NPZ_SHA" || exit 95
test "$(sha256sum "$R16_JSON" | awk '{print $1}')" = "$R16_JSON_SHA" || exit 96

echo 'NL1C7B4_REPAIR17_LOCK_PASS'
echo "HEAD=$(git rev-parse HEAD)"
echo "REPAIR16_JSON_SHA256=$R16_JSON_SHA"

mkdir -p results
set +e
PYTHONPATH="$PWD" python nl1c7b/initial_constraint_certification_repair17.py   --trace "$TRACE"   --coverage-json "$COVERAGE"   --repair15a-json "$R15A_JSON"   --repair15a-npz "$R15A_NPZ"   --repair16-json "$R16_JSON"   --out "$OUT"   2>&1 | tee "$LOG"
rc=$?
set -e

echo "SCIENCE_RC=$rc"
test "$rc" -eq 0 -o "$rc" -eq 2

python - <<'PY'
import hashlib, json, pathlib
p=pathlib.Path('results/nl1c7b4_repair17_repair16_source_localization.json')
d=json.loads(p.read_text())
print('CLASSIFICATION=',d['classification'])
print('gates=',d['gates'])
print('closure=',d['decomposition_closure'])
print('summary=',d['summary'])
print()
print('REPRESENTATIVE HOTSPOTS (Simple, beta=1):')
for row in d['localization_rows']:
    if row['Y_kind']=='Simple' and row['beta0']==1.0:
        print(
            'scale=',row['scale_hinv_Mpc'],'Nr=',row['Nr'],
            '| H=',row['H_hotspot']['dominant_label'],
            '/',row['H_hotspot']['second_label'],
            'eps=',row['max_epsilon_H'],
            'r=',row['H_hotspot']['r_Mpc'],
            '| M=',row['M_hotspot']['dominant_label'],
            '/',row['M_hotspot']['second_label'],
            'eps=',row['max_epsilon_M'],
            'r=',row['M_hotspot']['r_Mpc']
        )
print('JSON_SHA256=',hashlib.sha256(p.read_bytes()).hexdigest())
PY

exit "$rc"
