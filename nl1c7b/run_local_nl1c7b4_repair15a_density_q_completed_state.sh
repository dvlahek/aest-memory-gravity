#!/usr/bin/env bash
set -euo pipefail

ATTEMPT01_FREEZE_COMMIT='1a1bd3716af19d5ba3b1a76c04f68c00ae730b1f'
PREREG_COMMIT='893d42f083123f08b52df1225d0e01e49b687c61'
IMPLEMENTATION_COMMIT='52505918435b6a713046eb982141ad9d6b12ca43'
LOCK_COMMIT='c00c07e23cf8c7e9be6242b6eea70eb670bf71bf'

ATTEMPT01_FREEZE_BLOB='cb665f9c07f3b068cbd704d51bf2182a927763bf'
PREREG_BLOB='dd0f9a930cf835640f9f045b6dc17b84f78f710a'
IMPLEMENTATION_BLOB='d30b74e1b8a17d4f058896e052ec4e1f6efa25e9'
LOCK_BLOB='58f9bced33e4d958aeeb2677c7d39baefce625c0'
R15_BLOB='b455d72d768aec2ea2835e967418574de678be2d'
B4_BLOB='8559120dc273be3174eca130ca313ed6ff5acb25'
REC_BLOB='ff383c1ddc2cb2a684e2b5dd11fde0ae811e4fac'

R8_JSON='results/nl1c7a_repair08_identity_preserving_scalar_representation.json'
R8_NPZ='results/nl1c7a_repair08_identity_preserving_primary_states.npz'
R14A_JSON='results/nl1c7b4_repair14a_decoded_static_semantics_parser.json'
TRACE='input/dense/nl1c7a_repair01_dense_trace.dat'
COVERAGE='input/dense/nl1c7a_repair01_dense_coverage.json'
OUT='results/nl1c7b4_repair15a_density_q_completed_state.json'
STATE='results/nl1c7b4_repair15a_density_q_completed_primary_states.npz'
LOG='results/nl1c7b4_repair15a_density_q_completed_state.log'

R8_JSON_SHA='054851decab71e79a05aca2bc9fb287bb1239c8fb425989f40920004c3d88453'
R8_NPZ_SHA='4639f3b5c0afcddb2f98c8b9f6a9dbbf8661dac685b12d235c09075a106dafa7'
R14A_JSON_SHA='d60398e2804222df70e8cd3acda5fb397e9cfdd2068415b9256af4d65a5c64ca'

for c in "$ATTEMPT01_FREEZE_COMMIT" "$PREREG_COMMIT" "$IMPLEMENTATION_COMMIT" "$LOCK_COMMIT"; do
  git merge-base --is-ancestor "$c" HEAD || { echo "LOCK ancestry failure: $c" >&2; exit 91; }
done

check_blob () {
  local p="$1" expected="$2"
  local got
  got="$(git rev-parse "HEAD:$p")"
  test "$got" = "$expected" || { echo "blob mismatch $p: $got != $expected" >&2; exit 92; }
}

check_blob docs/nl1c7b4_repair15_attempt01_harness_failure_freeze.md "$ATTEMPT01_FREEZE_BLOB"
check_blob docs/nl1c7b4_repair15a_predata_kq_background_accessor_repair.md "$PREREG_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair15a.py "$IMPLEMENTATION_BLOB"
check_blob docs/nl1c7b4_repair15a_implementation_lock.md "$LOCK_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair15.py "$R15_BLOB"
check_blob nl1c7b/initial_constraint_certification.py "$B4_BLOB"
check_blob nl1c7a/a6_a10_spherical_reconstruction.py "$REC_BLOB"

for f in "$R8_JSON" "$R8_NPZ" "$R14A_JSON" "$TRACE" "$COVERAGE"; do
  test -s "$f" || { echo "missing input: $f" >&2; exit 93; }
done

test "$(sha256sum "$R8_JSON" | awk '{print $1}')" = "$R8_JSON_SHA" || { echo "R8 JSON hash mismatch" >&2; exit 94; }
test "$(sha256sum "$R8_NPZ" | awk '{print $1}')" = "$R8_NPZ_SHA" || { echo "R8 NPZ hash mismatch" >&2; exit 95; }
test "$(sha256sum "$R14A_JSON" | awk '{print $1}')" = "$R14A_JSON_SHA" || { echo "R14a JSON hash mismatch" >&2; exit 96; }

echo 'NL1C7B4_REPAIR15A_LOCK_PASS'
echo "HEAD=$(git rev-parse HEAD)"
echo "REPAIR14A_JSON_SHA256=$R14A_JSON_SHA"

mkdir -p results
rm -f "$OUT" "$STATE"

set +e
PYTHONPATH="$PWD" python nl1c7b/initial_constraint_certification_repair15a.py   --trace "$TRACE"   --coverage-json "$COVERAGE"   --repair08-json "$R8_JSON"   --repair08-npz "$R8_NPZ"   --repair14a-json "$R14A_JSON"   --out "$OUT"   --state-npz "$STATE"   2>&1 | tee "$LOG"
rc=$?
set -e

echo "SCIENCE_RC=$rc"
test "$rc" -eq 0 -o "$rc" -eq 2

python - <<'PY'
import hashlib, json, pathlib
p=pathlib.Path('results/nl1c7b4_repair15a_density_q_completed_state.json')
d=json.loads(p.read_text())
print('CLASSIFICATION=', d['classification'])
print('gates=', d['gates'])
print('inherited_Repair15_gates=', d['inherited_Repair15_gates'])
print('accessor=', d['repair15a_accessor_repair'])
print('summary=', d['summary'])
print('changes=', d['phidot_minus_Q_changes'])
print('output=', d['output'])
print('JSON_SHA256=', hashlib.sha256(p.read_bytes()).hexdigest())
npz=pathlib.Path('results/nl1c7b4_repair15a_density_q_completed_primary_states.npz')
if npz.exists():
    print('NPZ_SHA256=', hashlib.sha256(npz.read_bytes()).hexdigest())
    print('NPZ_SIZE=', npz.stat().st_size)
PY

exit "$rc"
