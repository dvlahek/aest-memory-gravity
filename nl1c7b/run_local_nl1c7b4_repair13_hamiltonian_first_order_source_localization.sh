#!/usr/bin/env bash
set -euo pipefail

PREREG_COMMIT='f2bd2d3b693d41680e254d714aec1233502e3ce0'
IMPLEMENTATION_COMMIT='df3250a70c37303bde723688e87a071f42b2d380'
LOCK_COMMIT='49ce63ee685d7ef2c80270ca5881444de78b5fc4'
R12_FREEZE_COMMIT='167af8e7b6d610c307b67fed7890fe0547c27bfa'

PREREG_BLOB='20783a1dfdb17c5fe067171cef275a9bba32ea9f'
IMPLEMENTATION_BLOB='213d9fd22c5979ee1a47da653562dc43cb5c68cb'
LOCK_BLOB='57b5f1abdf570718f61eaca127393758a90654dc'
R12_FREEZE_BLOB='791015da17a25d2f75dbd8238bdbf04faa8dbaf0'
R12_BLOB='2199f8221bf341515301887de2f9fbf5a28b68a8'
R11_BLOB='72d324d94100ee4555698bf44acd45c6b612c927'
R10_BLOB='c72a85d6d42176fb8c6a5ebf5f8e101541272701'
R9_BLOB='0cd67cecfbd590cb8819ad37314dc5b49047bc93'
R1_BLOB='253a0ae2a19a597f06358704ea276c9005973af3'
B4_BLOB='8559120dc273be3174eca130ca313ed6ff5acb25'
R8_BLOB='94fb3f42a7c819b0525860f7344d5dbaff93da19'
REC_BLOB='ff383c1ddc2cb2a684e2b5dd11fde0ae811e4fac'

R8_JSON='results/nl1c7a_repair08_identity_preserving_scalar_representation.json'
R8_NPZ='results/nl1c7a_repair08_identity_preserving_primary_states.npz'
R10_JSON='results/nl1c7b4_repair10_raw_source_localization.json'
R11_JSON='results/nl1c7b4_repair11_esector_analytic_covariant_audit.json'
R12_JSON='results/nl1c7b4_repair12_full_constraint_order_audit.json'
TRACE='input/dense/nl1c7a_repair01_dense_trace.dat'
COVERAGE='input/dense/nl1c7a_repair01_dense_coverage.json'
OUT='results/nl1c7b4_repair13_hamiltonian_first_order_source_localization.json'
LOG='results/nl1c7b4_repair13_hamiltonian_first_order_source_localization.log'

R8_JSON_SHA='054851decab71e79a05aca2bc9fb287bb1239c8fb425989f40920004c3d88453'
R8_NPZ_SHA='4639f3b5c0afcddb2f98c8b9f6a9dbbf8661dac685b12d235c09075a106dafa7'
R10_JSON_SHA='f1fc1a86d2d488f5e88f0d32b0d3d1d5ce9dab22f52e51fa69801948aeb6de9d'
R11_JSON_SHA='48c8caf0c5758b089318bcd18885c87725bc244ed5a47862ac841b37b834742d'
R12_JSON_SHA='99c963dc65cca35c90c6b892fb4192bed1a8c03776664c9da532a5702c62767c'

for c in "$PREREG_COMMIT" "$IMPLEMENTATION_COMMIT" "$LOCK_COMMIT" "$R12_FREEZE_COMMIT"; do
  git merge-base --is-ancestor "$c" HEAD || { echo "LOCK ancestry failure: $c" >&2; exit 91; }
done

check_blob () {
  local p="$1" expected="$2"
  local got
  got="$(git rev-parse "HEAD:$p")"
  test "$got" = "$expected" || { echo "blob mismatch $p: $got != $expected" >&2; exit 92; }
}

check_blob docs/nl1c7b4_repair13_predata_hamiltonian_first_order_source_localization.md "$PREREG_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair13.py "$IMPLEMENTATION_BLOB"
check_blob docs/nl1c7b4_repair13_implementation_lock.md "$LOCK_BLOB"
check_blob docs/nl1c7b4_repair12_result_freeze.md "$R12_FREEZE_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair12.py "$R12_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair11.py "$R11_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair10.py "$R10_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair09.py "$R9_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair01.py "$R1_BLOB"
check_blob nl1c7b/initial_constraint_certification.py "$B4_BLOB"
check_blob nl1c7a/evaluate_identity_preserving_repair08.py "$R8_BLOB"
check_blob nl1c7a/a6_a10_spherical_reconstruction.py "$REC_BLOB"

for f in "$R8_JSON" "$R8_NPZ" "$R10_JSON" "$R11_JSON" "$R12_JSON" "$TRACE" "$COVERAGE"; do
  test -s "$f" || { echo "missing input: $f" >&2; exit 93; }
done

test "$(sha256sum "$R8_JSON" | awk '{print $1}')" = "$R8_JSON_SHA" || exit 94
test "$(sha256sum "$R8_NPZ" | awk '{print $1}')" = "$R8_NPZ_SHA" || exit 95
test "$(sha256sum "$R10_JSON" | awk '{print $1}')" = "$R10_JSON_SHA" || exit 96
test "$(sha256sum "$R11_JSON" | awk '{print $1}')" = "$R11_JSON_SHA" || exit 97
test "$(sha256sum "$R12_JSON" | awk '{print $1}')" = "$R12_JSON_SHA" || exit 98

echo 'NL1C7B4_REPAIR13_LOCK_PASS'
echo "HEAD=$(git rev-parse HEAD)"

mkdir -p results
set +e
PYTHONPATH="$PWD" python nl1c7b/initial_constraint_certification_repair13.py   --trace "$TRACE"   --coverage-json "$COVERAGE"   --repair08-json "$R8_JSON"   --repair08-npz "$R8_NPZ"   --repair10-json "$R10_JSON"   --repair11-json "$R11_JSON"   --repair12-json "$R12_JSON"   --out "$OUT"   2>&1 | tee "$LOG"
rc=$?
set -e

echo "SCIENCE_RC=$rc"
test "$rc" -eq 0 -o "$rc" -eq 2

python - <<'PY'
import json
p='results/nl1c7b4_repair13_hamiltonian_first_order_source_localization.json'
d=json.load(open(p))
print('CLASSIFICATION=', d['classification'])
print('gates=', d['gates'])
print('dominant_A_L2_source_counts=', d['summary']['dominant_A_L2_source_counts'])
print('per_source_order_label_counts=', d['summary']['per_source_order_label_counts'])
print('max_projection_sum_error=', d['summary']['max_projection_sum_error'])
print()
print('REPRESENTATIVE FIRST-ORDER LOCALIZATION (Simple, beta=1):')
for row in d['rows']:
    if row['Y_kind']=='Simple' and row['beta0']==1.0:
        print(
            'scale=',row['scale_hinv_Mpc'],'Nr=',row['Nr'],
            '| dominant=',row['dominant_A_L2_source'],
            '| second=',row['second_A_L2_source'],
            '| strongest_cancel=',row['strongest_cancelling_pair'],
            '| global_cancel=',row['global_cancellation_fraction']
        )
        coeffs=sorted(row['lambda_eighth_first_order_coefficients'], key=lambda x:x['A_L2'], reverse=True)
        for x in coeffs[:5]:
            print('   ',x['source'],'label=',x['order_label'],'A_L2=',x['A_L2'],'proj=',x['projection_fraction'],'cos=',x['cosine_with_total'])
PY

exit "$rc"
