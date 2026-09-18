#!/usr/bin/env bash
set -euo pipefail

PREREG_COMMIT='c43c3147da0ac7d9990d6badd422095b2b737ff9'
IMPLEMENTATION_COMMIT='29ec99242e456a1780176e0cb85ee35614f02486'
LOCK_COMMIT='490ab43db80a496c6d883ce09ea953a48c21080f'
R09_FREEZE_COMMIT='04d85232092cdc747cf317f2937f1c33a1c0dddc'

PREREG_BLOB='b9f4235bd6b62b8e7b79beecbe20a6d2178197b4'
IMPLEMENTATION_BLOB='c72a85d6d42176fb8c6a5ebf5f8e101541272701'
LOCK_BLOB='8a340fe360c670c7ead222495a3d5149677e0ee2'
R09_FREEZE_BLOB='09debcf9c89248f0f158b25d27fb39bdf38cefaf'
R09_BLOB='0cd67cecfbd590cb8819ad37314dc5b49047bc93'
R1_BLOB='253a0ae2a19a597f06358704ea276c9005973af3'
R2_BLOB='eff076ec9a511f64bc693dc48b07b2ce26cfbaeb'
B4_BLOB='8559120dc273be3174eca130ca313ed6ff5acb25'
R8_BLOB='94fb3f42a7c819b0525860f7344d5dbaff93da19'

R8_JSON='results/nl1c7a_repair08_identity_preserving_scalar_representation.json'
R8_NPZ='results/nl1c7a_repair08_identity_preserving_primary_states.npz'
R9_JSON='results/nl1c7b4_repair09_repair08_exact_constraint_retest.json'
TRACE='input/dense/nl1c7a_repair01_dense_trace.dat'
COVERAGE='input/dense/nl1c7a_repair01_dense_coverage.json'
OUT='results/nl1c7b4_repair10_raw_source_localization.json'
LOG='results/nl1c7b4_repair10_raw_source_localization.log'

R8_JSON_SHA='054851decab71e79a05aca2bc9fb287bb1239c8fb425989f40920004c3d88453'
R8_NPZ_SHA='4639f3b5c0afcddb2f98c8b9f6a9dbbf8661dac685b12d235c09075a106dafa7'
R9_JSON_SHA='be8b54823690ffefb62470c34ee3d7addeef45e2db81e40b10cce4b833376ffc'

for c in "$PREREG_COMMIT" "$IMPLEMENTATION_COMMIT" "$LOCK_COMMIT" "$R09_FREEZE_COMMIT"; do
  git merge-base --is-ancestor "$c" HEAD || { echo "LOCK ancestry failure: $c" >&2; exit 91; }
done

check_blob () {
  local p="$1" expected="$2"
  local got
  got="$(git rev-parse "HEAD:$p")"
  test "$got" = "$expected" || { echo "blob mismatch $p: $got != $expected" >&2; exit 92; }
}

check_blob docs/nl1c7b4_repair10_predata_raw_source_localization.md "$PREREG_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair10.py "$IMPLEMENTATION_BLOB"
check_blob docs/nl1c7b4_repair10_implementation_lock.md "$LOCK_BLOB"
check_blob docs/nl1c7b4_repair09_result_freeze.md "$R09_FREEZE_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair09.py "$R09_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair01.py "$R1_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair02.py "$R2_BLOB"
check_blob nl1c7b/initial_constraint_certification.py "$B4_BLOB"
check_blob nl1c7a/evaluate_identity_preserving_repair08.py "$R8_BLOB"

for f in "$R8_JSON" "$R8_NPZ" "$R9_JSON" "$TRACE" "$COVERAGE"; do
  test -s "$f" || { echo "missing input: $f" >&2; exit 93; }
done

test "$(sha256sum "$R8_JSON" | awk '{print $1}')" = "$R8_JSON_SHA" || { echo 'Repair08 JSON SHA mismatch' >&2; exit 94; }
test "$(sha256sum "$R8_NPZ" | awk '{print $1}')" = "$R8_NPZ_SHA" || { echo 'Repair08 NPZ SHA mismatch' >&2; exit 95; }
test "$(sha256sum "$R9_JSON" | awk '{print $1}')" = "$R9_JSON_SHA" || { echo 'Repair09 JSON SHA mismatch' >&2; exit 96; }

echo 'NL1C7B4_REPAIR10_LOCK_PASS'
echo "HEAD=$(git rev-parse HEAD)"
echo "REPAIR09_JSON_SHA256=$R9_JSON_SHA"

mkdir -p results
set +e
PYTHONPATH="$PWD" python nl1c7b/initial_constraint_certification_repair10.py   --trace "$TRACE"   --coverage-json "$COVERAGE"   --repair08-json "$R8_JSON"   --repair08-npz "$R8_NPZ"   --repair09-json "$R9_JSON"   --out "$OUT"   2>&1 | tee "$LOG"
rc=$?
set -e

echo "SCIENCE_RC=$rc"
test "$rc" -eq 0 -o "$rc" -eq 2

python - <<'PY'
import json
p='results/nl1c7b4_repair10_raw_source_localization.json'
d=json.load(open(p))
print('CLASSIFICATION=', d['classification'])
print('gates=', d['gates'])
print('closure=', d['decomposition_closure'])
print('H_dominant_counts=', d['summary']['H_dominant_label_counts'])
print('M_dominant_counts=', d['summary']['M_dominant_label_counts'])
print('H_second_counts=', d['summary']['H_second_label_counts'])
print('M_second_counts=', d['summary']['M_second_label_counts'])
print()
print('REPRESENTATIVE HOTSPOTS (Simple, beta=1):')
for row in d['localization_rows']:
    if row['Y_kind']=='Simple' and row['beta0']==1.0:
        h=row['H_hotspot']; m=row['M_hotspot']
        print(
            'scale=',row['scale_hinv_Mpc'],'Nr=',row['Nr'],
            '| H eps=',row['max_epsilon_H'],'r=',h['r_Mpc'],
            'dom=',h['dominant_label'],'second=',h['second_label'],
            '| M eps=',row['max_epsilon_M'],'r=',m['r_Mpc'],
            'dom=',m['dominant_label'],'second=',m['second_label'],
            'Mdom/rest=',m['dominant_to_opposing_rest_ratio']
        )
PY

exit "$rc"
