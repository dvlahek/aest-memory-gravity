#!/usr/bin/env bash
set -euo pipefail

PREREG_COMMIT='271f6bbc4a21108d5d0c1beabb9764be56e280b3'
IMPLEMENTATION_COMMIT='6f934ef8d87084e04ce9422309aeea355b15821e'
LOCK_COMMIT='e36975d92547bc9acc825a3532db6784fdfa64b0'
R13_FREEZE_COMMIT='f3d25b37eddd322b4e1ed147c99af9b2dec0227f'

PREREG_BLOB='7b02b045ed9af2a71a9d8fc751dda3369e8af924'
IMPLEMENTATION_BLOB='c6aa6f781b4a581db73b2dc4be38f0217dbb4a6b'
LOCK_BLOB='ec451a5e0f612dcd30fb2411524ff55c0baca93a'
R13_FREEZE_BLOB='6297c1f4eb34a5493ec294bf635fa7c4a913f409'
R13_BLOB='213d9fd22c5979ee1a47da653562dc43cb5c68cb'
R12_BLOB='2199f8221bf341515301887de2f9fbf5a28b68a8'
R1_BLOB='253a0ae2a19a597f06358704ea276c9005973af3'
B4_BLOB='8559120dc273be3174eca130ca313ed6ff5acb25'
R8_BLOB='94fb3f42a7c819b0525860f7344d5dbaff93da19'
REC_BLOB='ff383c1ddc2cb2a684e2b5dd11fde0ae811e4fac'

R8_JSON='results/nl1c7a_repair08_identity_preserving_scalar_representation.json'
R8_NPZ='results/nl1c7a_repair08_identity_preserving_primary_states.npz'
R10_JSON='results/nl1c7b4_repair10_raw_source_localization.json'
R11_JSON='results/nl1c7b4_repair11_esector_analytic_covariant_audit.json'
R12_JSON='results/nl1c7b4_repair12_full_constraint_order_audit.json'
R13_JSON='results/nl1c7b4_repair13_hamiltonian_first_order_source_localization.json'
TRACE='input/dense/nl1c7a_repair01_dense_trace.dat'
COVERAGE='input/dense/nl1c7a_repair01_dense_coverage.json'
OUT='results/nl1c7b4_repair13a_roundoff_stable_source_localization.json'
LOG='results/nl1c7b4_repair13a_roundoff_stable_source_localization.log'

R8_JSON_SHA='054851decab71e79a05aca2bc9fb287bb1239c8fb425989f40920004c3d88453'
R8_NPZ_SHA='4639f3b5c0afcddb2f98c8b9f6a9dbbf8661dac685b12d235c09075a106dafa7'
R10_JSON_SHA='f1fc1a86d2d488f5e88f0d32b0d3d1d5ce9dab22f52e51fa69801948aeb6de9d'
R11_JSON_SHA='48c8caf0c5758b089318bcd18885c87725bc244ed5a47862ac841b37b834742d'
R12_JSON_SHA='99c963dc65cca35c90c6b892fb4192bed1a8c03776664c9da532a5702c62767c'
R13_JSON_SHA='ef6791edd595a2bd8b44e52a703915385a1e2c4d98345ff4cc509a5d22a61a9b'

for c in "$PREREG_COMMIT" "$IMPLEMENTATION_COMMIT" "$LOCK_COMMIT" "$R13_FREEZE_COMMIT"; do
  git merge-base --is-ancestor "$c" HEAD || { echo "LOCK ancestry failure: $c" >&2; exit 91; }
done

check_blob () {
  local p="$1" expected="$2"
  local got
  got="$(git rev-parse "HEAD:$p")"
  test "$got" = "$expected" || { echo "blob mismatch $p: $got != $expected" >&2; exit 92; }
}

check_blob docs/nl1c7b4_repair13a_predata_roundoff_stable_source_localization.md "$PREREG_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair13a.py "$IMPLEMENTATION_BLOB"
check_blob docs/nl1c7b4_repair13a_implementation_lock.md "$LOCK_BLOB"
check_blob docs/nl1c7b4_repair13_result_freeze.md "$R13_FREEZE_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair13.py "$R13_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair12.py "$R12_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair01.py "$R1_BLOB"
check_blob nl1c7b/initial_constraint_certification.py "$B4_BLOB"
check_blob nl1c7a/evaluate_identity_preserving_repair08.py "$R8_BLOB"
check_blob nl1c7a/a6_a10_spherical_reconstruction.py "$REC_BLOB"

for f in "$R8_JSON" "$R8_NPZ" "$R10_JSON" "$R11_JSON" "$R12_JSON" "$R13_JSON" "$TRACE" "$COVERAGE"; do
  test -s "$f" || { echo "missing input: $f" >&2; exit 93; }
done

test "$(sha256sum "$R8_JSON" | awk '{print $1}')" = "$R8_JSON_SHA" || exit 94
test "$(sha256sum "$R8_NPZ" | awk '{print $1}')" = "$R8_NPZ_SHA" || exit 95
test "$(sha256sum "$R10_JSON" | awk '{print $1}')" = "$R10_JSON_SHA" || exit 96
test "$(sha256sum "$R11_JSON" | awk '{print $1}')" = "$R11_JSON_SHA" || exit 97
test "$(sha256sum "$R12_JSON" | awk '{print $1}')" = "$R12_JSON_SHA" || exit 98
test "$(sha256sum "$R13_JSON" | awk '{print $1}')" = "$R13_JSON_SHA" || exit 99

echo 'NL1C7B4_REPAIR13A_LOCK_PASS'
echo "HEAD=$(git rev-parse HEAD)"
echo "REPAIR13_JSON_SHA256=$R13_JSON_SHA"

mkdir -p results
set +e
PYTHONPATH="$PWD" python nl1c7b/initial_constraint_certification_repair13a.py   --trace "$TRACE"   --coverage-json "$COVERAGE"   --repair08-json "$R8_JSON"   --repair08-npz "$R8_NPZ"   --repair10-json "$R10_JSON"   --repair11-json "$R11_JSON"   --repair12-json "$R12_JSON"   --repair13-json "$R13_JSON"   --out "$OUT"   2>&1 | tee "$LOG"
rc=$?
set -e

echo "SCIENCE_RC=$rc"
test "$rc" -eq 0 -o "$rc" -eq 2

python - <<'PY'
import json
p='results/nl1c7b4_repair13a_roundoff_stable_source_localization.json'
d=json.load(open(p))
print('CLASSIFICATION=', d['classification'])
print('gates=', d['gates'])
print('roundoff=', {
    'max_G3_error_over_bound': d['roundoff_certification']['max_G3_error_over_bound'],
    'max_G4_error_over_bound': d['roundoff_certification']['max_G4_error_over_bound'],
    'max_G5_error_over_bound': d['roundoff_certification']['max_G5_error_over_bound'],
})
print('historical_Repair13=', d['historical_Repair13'])
print('frozen_localization_summary=', d['frozen_localization_summary'])
print()
print('REPRESENTATIVE ROUNDOFF ROWS (Simple, beta=1):')
for row in d['roundoff_certification']['rows']:
    if row['Y_kind']=='Simple' and row['beta0']==1.0:
        print(
            'scale=',row['scale_hinv_Mpc'],'Nr=',row['Nr'],
            '| dominant=',row['frozen_dominant_A_L2_source'],
            '| second=',row['frozen_second_A_L2_source'],
            '| G3 ratios=',[x['G3_max_error_over_bound'] for x in row['lambda_closure']],
            '| G4 ratios=',[x['G4_max_error_over_bound'] for x in row['lambda_closure']],
            '| G5 ratio=',row['projection_identity']['error_over_bound']
        )
PY

exit "$rc"
