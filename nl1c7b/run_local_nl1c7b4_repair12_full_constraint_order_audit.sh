#!/usr/bin/env bash
set -euo pipefail

PREREG_COMMIT='d1b5c5f3aab13b3929f8c91eeea216724951c5f3'
IMPLEMENTATION_COMMIT='85b9120781b29854f7508f1a18a77f8b42c814f2'
LOCK_COMMIT='ccba3e6d6b19a77032145ec65d5209710699a4fb'
R11_FREEZE_COMMIT='559650a2de9bf57a344401ba459adf2268212b81'

PREREG_BLOB='f10574705665d31dc88efb0cd34867ad2ed2de07'
IMPLEMENTATION_BLOB='2199f8221bf341515301887de2f9fbf5a28b68a8'
LOCK_BLOB='d5aa1277639df4638dd9f5b63962b0e2db0966ab'
R11_FREEZE_BLOB='5aade75b3c9f66427dba3ce6192d2500d4d604ee'
R11_BLOB='72d324d94100ee4555698bf44acd45c6b612c927'
R10_BLOB='c72a85d6d42176fb8c6a5ebf5f8e101541272701'
R9_BLOB='0cd67cecfbd590cb8819ad37314dc5b49047bc93'
R1_BLOB='253a0ae2a19a597f06358704ea276c9005973af3'
R2_BLOB='eff076ec9a511f64bc693dc48b07b2ce26cfbaeb'
B4_BLOB='8559120dc273be3174eca130ca313ed6ff5acb25'
R8_BLOB='94fb3f42a7c819b0525860f7344d5dbaff93da19'
REC_BLOB='ff383c1ddc2cb2a684e2b5dd11fde0ae811e4fac'

R8_JSON='results/nl1c7a_repair08_identity_preserving_scalar_representation.json'
R8_NPZ='results/nl1c7a_repair08_identity_preserving_primary_states.npz'
R10_JSON='results/nl1c7b4_repair10_raw_source_localization.json'
R11_JSON='results/nl1c7b4_repair11_esector_analytic_covariant_audit.json'
TRACE='input/dense/nl1c7a_repair01_dense_trace.dat'
COVERAGE='input/dense/nl1c7a_repair01_dense_coverage.json'
OUT='results/nl1c7b4_repair12_full_constraint_order_audit.json'
LOG='results/nl1c7b4_repair12_full_constraint_order_audit.log'

R8_JSON_SHA='054851decab71e79a05aca2bc9fb287bb1239c8fb425989f40920004c3d88453'
R8_NPZ_SHA='4639f3b5c0afcddb2f98c8b9f6a9dbbf8661dac685b12d235c09075a106dafa7'
R10_JSON_SHA='f1fc1a86d2d488f5e88f0d32b0d3d1d5ce9dab22f52e51fa69801948aeb6de9d'
R11_JSON_SHA='48c8caf0c5758b089318bcd18885c87725bc244ed5a47862ac841b37b834742d'

for c in "$PREREG_COMMIT" "$IMPLEMENTATION_COMMIT" "$LOCK_COMMIT" "$R11_FREEZE_COMMIT"; do
  git merge-base --is-ancestor "$c" HEAD || { echo "LOCK ancestry failure: $c" >&2; exit 91; }
done

check_blob () {
  local p="$1" expected="$2"
  local got
  got="$(git rev-parse "HEAD:$p")"
  test "$got" = "$expected" || { echo "blob mismatch $p: $got != $expected" >&2; exit 92; }
}

check_blob docs/nl1c7b4_repair12_predata_full_constraint_order_audit.md "$PREREG_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair12.py "$IMPLEMENTATION_BLOB"
check_blob docs/nl1c7b4_repair12_implementation_lock.md "$LOCK_BLOB"
check_blob docs/nl1c7b4_repair11_result_freeze.md "$R11_FREEZE_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair11.py "$R11_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair10.py "$R10_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair09.py "$R9_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair01.py "$R1_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair02.py "$R2_BLOB"
check_blob nl1c7b/initial_constraint_certification.py "$B4_BLOB"
check_blob nl1c7a/evaluate_identity_preserving_repair08.py "$R8_BLOB"
check_blob nl1c7a/a6_a10_spherical_reconstruction.py "$REC_BLOB"

for f in "$R8_JSON" "$R8_NPZ" "$R10_JSON" "$R11_JSON" "$TRACE" "$COVERAGE"; do
  test -s "$f" || { echo "missing input: $f" >&2; exit 93; }
done

test "$(sha256sum "$R8_JSON" | awk '{print $1}')" = "$R8_JSON_SHA" || { echo 'Repair08 JSON SHA mismatch' >&2; exit 94; }
test "$(sha256sum "$R8_NPZ" | awk '{print $1}')" = "$R8_NPZ_SHA" || { echo 'Repair08 NPZ SHA mismatch' >&2; exit 95; }
test "$(sha256sum "$R10_JSON" | awk '{print $1}')" = "$R10_JSON_SHA" || { echo 'Repair10 JSON SHA mismatch' >&2; exit 96; }
test "$(sha256sum "$R11_JSON" | awk '{print $1}')" = "$R11_JSON_SHA" || { echo 'Repair11 JSON SHA mismatch' >&2; exit 97; }

echo 'NL1C7B4_REPAIR12_LOCK_PASS'
echo "HEAD=$(git rev-parse HEAD)"
echo "REPAIR11_JSON_SHA256=$R11_JSON_SHA"

mkdir -p results
set +e
PYTHONPATH="$PWD" python nl1c7b/initial_constraint_certification_repair12.py   --trace "$TRACE"   --coverage-json "$COVERAGE"   --repair08-json "$R8_JSON"   --repair08-npz "$R8_NPZ"   --repair10-json "$R10_JSON"   --repair11-json "$R11_JSON"   --out "$OUT"   2>&1 | tee "$LOG"
rc=$?
set -e

echo "SCIENCE_RC=$rc"
test "$rc" -eq 0 -o "$rc" -eq 2

python - <<'PY'
import json
p='results/nl1c7b4_repair12_full_constraint_order_audit.json'
d=json.load(open(p))
print('CLASSIFICATION=', d['classification'])
print('gates=', d['gates'])
print('closure=', d['bookkeeping_closure'])
print('summary=', d['summary'])
print()
print('REPRESENTATIVE ORDER ROWS (Simple, beta=1):')
for row in d['order_audit_rows']:
    if row['Y_kind']=='Simple' and row['beta0']==1.0:
        print(
            'scale=',row['scale_hinv_Mpc'],'Nr=',row['Nr'],
            '| H L2 slopes=',row['H_L2_adjacent_log2_slopes'],
            '| M L2 slopes=',row['M_L2_adjacent_log2_slopes'],
            '| H gate=',row['H_gated_pass'],
            '| M gate=',row['M_gated_pass'],
            '| baseline H/M L2=',row['baseline']['N_H_L2'],row['baseline']['N_M_L2']
        )
PY

exit "$rc"
