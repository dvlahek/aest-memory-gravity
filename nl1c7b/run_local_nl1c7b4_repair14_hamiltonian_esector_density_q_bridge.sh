#!/usr/bin/env bash
set -euo pipefail

PREREG_COMMIT='117d227737a1a78dfe5055878d703a90cbf74bd3'
IMPLEMENTATION_COMMIT='517535978defec9d8ca04e289315d79b4acbc981'
LOCK_COMMIT='c44dc7687050dc560a9071e540dc0d7058238e0f'
R13A_FREEZE_COMMIT='cb6440383eac99001369e976fae035d74adf30fc'

PREREG_BLOB='875aaef1b262811988b37f338119fc04fc0ad5ea'
IMPLEMENTATION_BLOB='c67aa9f8c64ba2dcb499216feb405a7a339b7b06'
LOCK_BLOB='d5d5fd4213fc3254922e31af771259ac877c8bd5'
R13A_FREEZE_BLOB='914a8aed85a87d45496c9bd05e03be4bc37bbeba'
R13A_BLOB='c6aa6f781b4a581db73b2dc4be38f0217dbb4a6b'
R12_BLOB='2199f8221bf341515301887de2f9fbf5a28b68a8'
R1_BLOB='253a0ae2a19a597f06358704ea276c9005973af3'
B4_BLOB='8559120dc273be3174eca130ca313ed6ff5acb25'
C7A_PREREG_BLOB='6d281c34c8545b3b4f2a3ab0864a684c2364ff67'
C7A_GAUGE_BLOB='dd9612552eed874fa4ab4b00091e5d46c22751be'
V019_PATCH_BLOB='c78484eb916bfee2730759c0bdc813a706bf9a68'
R8_BLOB='94fb3f42a7c819b0525860f7344d5dbaff93da19'
REC_BLOB='ff383c1ddc2cb2a684e2b5dd11fde0ae811e4fac'

R8_JSON='results/nl1c7a_repair08_identity_preserving_scalar_representation.json'
R8_NPZ='results/nl1c7a_repair08_identity_preserving_primary_states.npz'
R10_JSON='results/nl1c7b4_repair10_raw_source_localization.json'
R11_JSON='results/nl1c7b4_repair11_esector_analytic_covariant_audit.json'
R12_JSON='results/nl1c7b4_repair12_full_constraint_order_audit.json'
R13_JSON='results/nl1c7b4_repair13_hamiltonian_first_order_source_localization.json'
R13A_JSON='results/nl1c7b4_repair13a_roundoff_stable_source_localization.json'
TRACE='input/dense/nl1c7a_repair01_dense_trace.dat'
COVERAGE='input/dense/nl1c7a_repair01_dense_coverage.json'
OUT='results/nl1c7b4_repair14_hamiltonian_esector_density_q_bridge.json'
LOG='results/nl1c7b4_repair14_hamiltonian_esector_density_q_bridge.log'

R8_JSON_SHA='054851decab71e79a05aca2bc9fb287bb1239c8fb425989f40920004c3d88453'
R8_NPZ_SHA='4639f3b5c0afcddb2f98c8b9f6a9dbbf8661dac685b12d235c09075a106dafa7'
R10_JSON_SHA='f1fc1a86d2d488f5e88f0d32b0d3d1d5ce9dab22f52e51fa69801948aeb6de9d'
R11_JSON_SHA='48c8caf0c5758b089318bcd18885c87725bc244ed5a47862ac841b37b834742d'
R12_JSON_SHA='99c963dc65cca35c90c6b892fb4192bed1a8c03776664c9da532a5702c62767c'
R13_JSON_SHA='ef6791edd595a2bd8b44e52a703915385a1e2c4d98345ff4cc509a5d22a61a9b'
R13A_JSON_SHA='cad6cb2b49b3b20a0b6346390f8536fb90da8d5000ceed82ac0de86b912679b3'

for c in "$PREREG_COMMIT" "$IMPLEMENTATION_COMMIT" "$LOCK_COMMIT" "$R13A_FREEZE_COMMIT"; do
  git merge-base --is-ancestor "$c" HEAD || { echo "LOCK ancestry failure: $c" >&2; exit 91; }
done

check_blob () {
  local p="$1" expected="$2"
  local got
  got="$(git rev-parse "HEAD:$p")"
  test "$got" = "$expected" || { echo "blob mismatch $p: $got != $expected" >&2; exit 92; }
}

check_blob docs/nl1c7b4_repair14_predata_hamiltonian_esector_density_q_bridge.md "$PREREG_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair14.py "$IMPLEMENTATION_BLOB"
check_blob docs/nl1c7b4_repair14_implementation_lock.md "$LOCK_BLOB"
check_blob docs/nl1c7b4_repair13a_result_freeze.md "$R13A_FREEZE_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair13a.py "$R13A_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair12.py "$R12_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair01.py "$R1_BLOB"
check_blob nl1c7b/initial_constraint_certification.py "$B4_BLOB"
check_blob docs/nl1c7a_predata_growing_mode_bridge.md "$C7A_PREREG_BLOB"
check_blob nl1c7a/gauge_bridge_audit.py "$C7A_GAUGE_BLOB"
check_blob v019/apply_patch_v019.py "$V019_PATCH_BLOB"
check_blob nl1c7a/evaluate_identity_preserving_repair08.py "$R8_BLOB"
check_blob nl1c7a/a6_a10_spherical_reconstruction.py "$REC_BLOB"

for f in "$R8_JSON" "$R8_NPZ" "$R10_JSON" "$R11_JSON" "$R12_JSON" "$R13_JSON" "$R13A_JSON" "$TRACE" "$COVERAGE"; do
  test -s "$f" || { echo "missing input: $f" >&2; exit 93; }
done

test "$(sha256sum "$R8_JSON" | awk '{print $1}')" = "$R8_JSON_SHA" || exit 94
test "$(sha256sum "$R8_NPZ" | awk '{print $1}')" = "$R8_NPZ_SHA" || exit 95
test "$(sha256sum "$R10_JSON" | awk '{print $1}')" = "$R10_JSON_SHA" || exit 96
test "$(sha256sum "$R11_JSON" | awk '{print $1}')" = "$R11_JSON_SHA" || exit 97
test "$(sha256sum "$R12_JSON" | awk '{print $1}')" = "$R12_JSON_SHA" || exit 98
test "$(sha256sum "$R13_JSON" | awk '{print $1}')" = "$R13_JSON_SHA" || exit 99
test "$(sha256sum "$R13A_JSON" | awk '{print $1}')" = "$R13A_JSON_SHA" || exit 100

echo 'NL1C7B4_REPAIR14_LOCK_PASS'
echo "HEAD=$(git rev-parse HEAD)"
echo "REPAIR13A_JSON_SHA256=$R13A_JSON_SHA"

mkdir -p results
set +e
PYTHONPATH="$PWD" python nl1c7b/initial_constraint_certification_repair14.py   --trace "$TRACE"   --coverage-json "$COVERAGE"   --repair08-json "$R8_JSON"   --repair08-npz "$R8_NPZ"   --repair10-json "$R10_JSON"   --repair11-json "$R11_JSON"   --repair12-json "$R12_JSON"   --repair13-json "$R13_JSON"   --repair13a-json "$R13A_JSON"   --out "$OUT"   2>&1 | tee "$LOG"
rc=$?
set -e

echo "SCIENCE_RC=$rc"
test "$rc" -eq 0 -o "$rc" -eq 2

python - <<'PY'
import json
p='results/nl1c7b4_repair14_hamiltonian_esector_density_q_bridge.json'
d=json.load(open(p))
print('CLASSIFICATION=', d['classification'])
print('gates=', d['gates'])
print('symbolic=', d['symbolic_audit'])
print('static_bridge_semantics=', d['static_bridge_semantics'])
print('summary=', d['summary'])
print()
print('ANALYTIC PROFILE PAIRS:')
for row in d['analytic_profile_rows']:
    print(
        'scale=',row['scale_hinv_Mpc'],'Nr=',row['Nr'],
        '| E2=',row['E2_A_L2'],
        '| EX=',row['EX_A_L2'],
        '| Kcorr+E rel=',row['Kcorr_plus_E_relative_L2'],
        '| DeltaQ L2=',row['Delta_deltaQ_L2']
    )
print()
print('CORRECTED ORDER (Simple, beta=1):')
for row in d['corrected_diagnostic_order_rows']:
    if row['Y_kind']=='Simple' and row['beta0']==1.0:
        print(
            'scale=',row['scale_hinv_Mpc'],'Nr=',row['Nr'],
            '| H=',row['H_L2_adjacent_log2_slopes'],
            '| M=',row['M_L2_adjacent_log2_slopes'],
            '| Hgate=',row['H_gated_pass'],
            '| Mgate=',row['M_gated_pass']
        )
PY

exit "$rc"
