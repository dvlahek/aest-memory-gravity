#!/usr/bin/env bash
set -euo pipefail

R14A_FREEZE_COMMIT='be1ad5287a22feb81e9fceef0483eefb17b1a800'
PREREG_COMMIT='fad9c5136d04de1618d3b94ef47a483529ba4d78'
IMPLEMENTATION_COMMIT='50644d7e4def48a2da80e854e1e9f0ac3c0f2720'
LOCK_COMMIT='fa986b353dcb0ab64c4fd5759cf8c6faaffcb7ad'

R14A_FREEZE_BLOB='ad041eef454a4d02675ee4f4df6afe506177a37f'
PREREG_BLOB='f2fa2983df554c1d9807c1e135ee17b0d1839c4e'
IMPLEMENTATION_BLOB='b455d72d768aec2ea2835e967418574de678be2d'
LOCK_BLOB='5e9d4df7067c8fc620848cda01186cf31ff4c787'
R8_BLOB='94fb3f42a7c819b0525860f7344d5dbaff93da19'
R9_BLOB='0cd67cecfbd590cb8819ad37314dc5b49047bc93'
B4_BLOB='8559120dc273be3174eca130ca313ed6ff5acb25'
REC_BLOB='ff383c1ddc2cb2a684e2b5dd11fde0ae811e4fac'

R8_JSON='results/nl1c7a_repair08_identity_preserving_scalar_representation.json'
R8_NPZ='results/nl1c7a_repair08_identity_preserving_primary_states.npz'
R14A_JSON='results/nl1c7b4_repair14a_decoded_static_semantics_parser.json'
TRACE='input/dense/nl1c7a_repair01_dense_trace.dat'
COVERAGE='input/dense/nl1c7a_repair01_dense_coverage.json'
OUT='results/nl1c7b4_repair15_density_q_completed_state.json'
STATE='results/nl1c7b4_repair15_density_q_completed_primary_states.npz'
LOG='results/nl1c7b4_repair15_density_q_completed_state.log'

R8_JSON_SHA='054851decab71e79a05aca2bc9fb287bb1239c8fb425989f40920004c3d88453'
R8_NPZ_SHA='4639f3b5c0afcddb2f98c8b9f6a9dbbf8661dac685b12d235c09075a106dafa7'
R14A_JSON_SHA='d60398e2804222df70e8cd3acda5fb397e9cfdd2068415b9256af4d65a5c64ca'

for c in "$R14A_FREEZE_COMMIT" "$PREREG_COMMIT" "$IMPLEMENTATION_COMMIT" "$LOCK_COMMIT"; do
  git merge-base --is-ancestor "$c" HEAD || { echo "LOCK ancestry failure: $c" >&2; exit 91; }
done

check_blob () {
  local p="$1" expected="$2"
  local got
  got="$(git rev-parse "HEAD:$p")"
  test "$got" = "$expected" || { echo "blob mismatch $p: $got != $expected" >&2; exit 92; }
}

check_blob docs/nl1c7b4_repair14a_result_freeze.md "$R14A_FREEZE_BLOB"
check_blob docs/nl1c7b4_repair15_predata_density_q_completed_state.md "$PREREG_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair15.py "$IMPLEMENTATION_BLOB"
check_blob docs/nl1c7b4_repair15_implementation_lock.md "$LOCK_BLOB"
check_blob nl1c7a/evaluate_identity_preserving_repair08.py "$R8_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair09.py "$R9_BLOB"
check_blob nl1c7b/initial_constraint_certification.py "$B4_BLOB"
check_blob nl1c7a/a6_a10_spherical_reconstruction.py "$REC_BLOB"

for f in "$R8_JSON" "$R8_NPZ" "$R14A_JSON" "$TRACE" "$COVERAGE"; do
  test -s "$f" || { echo "missing input: $f" >&2; exit 93; }
done

test "$(sha256sum "$R8_JSON" | awk '{print $1}')" = "$R8_JSON_SHA" || { echo "R8 JSON hash mismatch" >&2; exit 94; }
test "$(sha256sum "$R8_NPZ" | awk '{print $1}')" = "$R8_NPZ_SHA" || { echo "R8 NPZ hash mismatch" >&2; exit 95; }
test "$(sha256sum "$R14A_JSON" | awk '{print $1}')" = "$R14A_JSON_SHA" || { echo "R14a JSON hash mismatch" >&2; exit 96; }

echo 'NL1C7B4_REPAIR15_LOCK_PASS'
echo "HEAD=$(git rev-parse HEAD)"
echo "REPAIR14A_JSON_SHA256=$R14A_JSON_SHA"

mkdir -p results
rm -f "$STATE"

set +e
PYTHONPATH="$PWD" python nl1c7b/initial_constraint_certification_repair15.py   --trace "$TRACE"   --coverage-json "$COVERAGE"   --repair08-json "$R8_JSON"   --repair08-npz "$R8_NPZ"   --repair14a-json "$R14A_JSON"   --out "$OUT"   --state-npz "$STATE"   2>&1 | tee "$LOG"
rc=$?
set -e

echo "SCIENCE_RC=$rc"
test "$rc" -eq 0 -o "$rc" -eq 2

python - <<'PY'
import hashlib, json, pathlib
p=pathlib.Path('results/nl1c7b4_repair15_density_q_completed_state.json')
d=json.loads(p.read_text())
print('CLASSIFICATION=', d['classification'])
print('gates=', d['gates'])
print('summary=', d['summary'])
print('changes=', d['phidot_minus_Q_changes'])
print('output=', d['output'])
print('JSON_SHA256=', hashlib.sha256(p.read_bytes()).hexdigest())
npz=pathlib.Path('results/nl1c7b4_repair15_density_q_completed_primary_states.npz')
if npz.exists():
    print('NPZ_SHA256=', hashlib.sha256(npz.read_bytes()).hexdigest())
    print('NPZ_SIZE=', npz.stat().st_size)
PY

exit "$rc"
