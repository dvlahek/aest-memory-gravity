#!/usr/bin/env bash
set -euo pipefail

ATTEMPT01_FREEZE_COMMIT='381bc30d6266b12c3590b9138c9f1a7bc07de9cc'
PREREG_COMMIT='f8eed7308018bc8f7e626128d9a375c6fc90b374'
IMPLEMENTATION_COMMIT='c73ebe709b41cfe8d8d346efb24a92f3eda25cad'
LOCK_COMMIT='0dc564fa16b4d2fbd04f2c9f34bd5fcb2ee503b1'

ATTEMPT01_FREEZE_BLOB='8e19263ac71597a006509d43b5b0606fab349e7e'
PREREG_BLOB='870fc95eef7335049e4d0785c4acc8a14509864a'
IMPLEMENTATION_BLOB='1bf9ea6b9ed813574a7ed20ce723228347e9f737'
LOCK_BLOB='ba442ff0fb27ce7a132ccc1dad30fd307d6ddf9c'
R14_BLOB='c67aa9f8c64ba2dcb499216feb405a7a339b7b06'
V019_PATCH_BLOB='c78484eb916bfee2730759c0bdc813a706bf9a68'

R8_JSON='results/nl1c7a_repair08_identity_preserving_scalar_representation.json'
R8_NPZ='results/nl1c7a_repair08_identity_preserving_primary_states.npz'
R10_JSON='results/nl1c7b4_repair10_raw_source_localization.json'
R11_JSON='results/nl1c7b4_repair11_esector_analytic_covariant_audit.json'
R12_JSON='results/nl1c7b4_repair12_full_constraint_order_audit.json'
R13_JSON='results/nl1c7b4_repair13_hamiltonian_first_order_source_localization.json'
R13A_JSON='results/nl1c7b4_repair13a_roundoff_stable_source_localization.json'
R14_JSON='results/nl1c7b4_repair14_hamiltonian_esector_density_q_bridge.json'
TRACE='input/dense/nl1c7a_repair01_dense_trace.dat'
COVERAGE='input/dense/nl1c7a_repair01_dense_coverage.json'
OUT='results/nl1c7b4_repair14a_decoded_static_semantics_parser.json'
LOG='results/nl1c7b4_repair14a_decoded_static_semantics_parser.log'

R14_JSON_SHA='ea4f1d28330b22d6d3d64f5f6f6d27b3646a889fbee9cffc37c4e789282f0966'

for c in "$ATTEMPT01_FREEZE_COMMIT" "$PREREG_COMMIT" "$IMPLEMENTATION_COMMIT" "$LOCK_COMMIT"; do
  git merge-base --is-ancestor "$c" HEAD || { echo "LOCK ancestry failure: $c" >&2; exit 91; }
done

check_blob () {
  local p="$1" expected="$2"
  local got
  got="$(git rev-parse "HEAD:$p")"
  test "$got" = "$expected" || { echo "blob mismatch $p: $got != $expected" >&2; exit 92; }
}

check_blob docs/nl1c7b4_repair14_attempt01_implementation_failure_freeze.md "$ATTEMPT01_FREEZE_BLOB"
check_blob docs/nl1c7b4_repair14a_predata_decoded_static_semantics_parser.md "$PREREG_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair14a.py "$IMPLEMENTATION_BLOB"
check_blob docs/nl1c7b4_repair14a_implementation_lock.md "$LOCK_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair14.py "$R14_BLOB"
check_blob v019/apply_patch_v019.py "$V019_PATCH_BLOB"

for f in "$R8_JSON" "$R8_NPZ" "$R10_JSON" "$R11_JSON" "$R12_JSON" "$R13_JSON" "$R13A_JSON" "$R14_JSON" "$TRACE" "$COVERAGE"; do
  test -s "$f" || { echo "missing input: $f" >&2; exit 93; }
done

test "$(sha256sum "$R14_JSON" | awk '{print $1}')" = "$R14_JSON_SHA" || {
  echo "Repair14 attempt01 JSON hash mismatch" >&2
  exit 94
}

echo 'NL1C7B4_REPAIR14A_LOCK_PASS'
echo "HEAD=$(git rev-parse HEAD)"
echo "REPAIR14_ATTEMPT01_JSON_SHA256=$R14_JSON_SHA"

mkdir -p results
set +e
PYTHONPATH="$PWD" python nl1c7b/initial_constraint_certification_repair14a.py   --trace "$TRACE"   --coverage-json "$COVERAGE"   --repair08-json "$R8_JSON"   --repair08-npz "$R8_NPZ"   --repair10-json "$R10_JSON"   --repair11-json "$R11_JSON"   --repair12-json "$R12_JSON"   --repair13-json "$R13_JSON"   --repair13a-json "$R13A_JSON"   --repair14-json "$R14_JSON"   --out "$OUT"   2>&1 | tee "$LOG"
rc=$?
set -e

echo "SCIENCE_RC=$rc"
test "$rc" -eq 0 -o "$rc" -eq 2

python - <<'PY'
import json
p='results/nl1c7b4_repair14a_decoded_static_semantics_parser.json'
d=json.load(open(p))
print('CLASSIFICATION=', d['classification'])
print('gates=', d['gates'])
print('inherited_Repair14_gates=', d['inherited_Repair14_gates'])
print('decoded_static=', d['repair14a_parser_repair']['decoded_static_semantics'])
print('payload_exact=', d['repair14a_parser_repair']['science_payload_exactly_reproduced_vs_attempt01'])
print('summary=', d['summary'])
PY

exit "$rc"
