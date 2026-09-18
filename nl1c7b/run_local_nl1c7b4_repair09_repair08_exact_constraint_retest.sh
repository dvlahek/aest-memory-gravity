#!/usr/bin/env bash
set -euo pipefail

PREREG_COMMIT='ee97aec340b9b8dcc508d092730b795f01eb65bd'
ATTEMPT01_FREEZE_COMMIT='31245e697143304e37440d2dd939bd3965d50fc3'
CORRECTION_COMMIT='555bc34a98eb918730aebe6f46bbb9f7a1497fc6'
IMPLEMENTATION_COMMIT='8f04b382aaa44960df18f662c2fa8330665e82c2'
LOCK_COMMIT='14b2a05000a8ea73105ede6c4188013df11be88a'

PREREG_BLOB='3e4f6ed8cf8a70a791f0ffef68c9b780ba7552c6'
IMPLEMENTATION_BLOB='0cd67cecfbd590cb8819ad37314dc5b49047bc93'
LOCK_BLOB='d36b8238d83fdb13199d5e7709c8fbccafaf7df7'
ATTEMPT01_FREEZE_BLOB='5381609f7df27f578ef8a514777457f0aeaf51d7'
CORRECTION_BLOB='03a49c08d7d7337dc6f728c6ce274ef95cf22886'
B4_BLOB='8559120dc273be3174eca130ca313ed6ff5acb25'
R1_BLOB='253a0ae2a19a597f06358704ea276c9005973af3'
R2_BLOB='eff076ec9a511f64bc693dc48b07b2ce26cfbaeb'
C7A_REC_BLOB='ff383c1ddc2cb2a684e2b5dd11fde0ae811e4fac'
R8_EVAL_BLOB='94fb3f42a7c819b0525860f7344d5dbaff93da19'

R8_JSON='results/nl1c7a_repair08_identity_preserving_scalar_representation.json'
R8_NPZ='results/nl1c7a_repair08_identity_preserving_primary_states.npz'
TRACE='input/dense/nl1c7a_repair01_dense_trace.dat'
COVERAGE='input/dense/nl1c7a_repair01_dense_coverage.json'
OUT='results/nl1c7b4_repair09_repair08_exact_constraint_retest.json'
LOG='results/nl1c7b4_repair09_repair08_exact_constraint_retest.log'

R8_JSON_SHA='054851decab71e79a05aca2bc9fb287bb1239c8fb425989f40920004c3d88453'
R8_NPZ_SHA='4639f3b5c0afcddb2f98c8b9f6a9dbbf8661dac685b12d235c09075a106dafa7'

for c in "$PREREG_COMMIT" "$IMPLEMENTATION_COMMIT" "$LOCK_COMMIT" "$ATTEMPT01_FREEZE_COMMIT" "$CORRECTION_COMMIT"; do
  git merge-base --is-ancestor "$c" HEAD || { echo "LOCK ancestry failure: $c" >&2; exit 91; }
done

check_blob () {
  local path="$1" expected="$2"
  local got
  got="$(git rev-parse "HEAD:${path}")"
  test "$got" = "$expected" || { echo "blob mismatch ${path}: ${got} != ${expected}" >&2; exit 92; }
}

check_blob docs/nl1c7b4_repair09_predata_repair08_exact_constraint_retest.md "$PREREG_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair09.py "$IMPLEMENTATION_BLOB"
check_blob docs/nl1c7b4_repair09_implementation_lock.md "$LOCK_BLOB"
check_blob docs/nl1c7b4_repair09_attempt01_harness_failure_freeze.md "$ATTEMPT01_FREEZE_BLOB"
check_blob docs/nl1c7b4_repair09_provenance_lock_correction.md "$CORRECTION_BLOB"
check_blob nl1c7b/initial_constraint_certification.py "$B4_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair01.py "$R1_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair02.py "$R2_BLOB"
check_blob nl1c7a/a6_a10_spherical_reconstruction.py "$C7A_REC_BLOB"
check_blob nl1c7a/evaluate_identity_preserving_repair08.py "$R8_EVAL_BLOB"

test -s "$R8_JSON"
test -s "$R8_NPZ"
test -s "$TRACE"
test -s "$COVERAGE"

test "$(sha256sum "$R8_JSON" | awk '{print $1}')" = "$R8_JSON_SHA" || { echo 'Repair08 JSON SHA256 mismatch' >&2; exit 93; }
test "$(sha256sum "$R8_NPZ" | awk '{print $1}')" = "$R8_NPZ_SHA" || { echo 'Repair08 NPZ SHA256 mismatch' >&2; exit 94; }
test "$(stat -c %s "$R8_NPZ")" = '103024' || { echo 'Repair08 NPZ size mismatch' >&2; exit 95; }

echo 'NL1C7B4_REPAIR09_LOCK_PASS'
echo "HEAD=$(git rev-parse HEAD)"
echo "REPAIR08_NPZ_SHA256=$R8_NPZ_SHA"

mkdir -p results
set +e
PYTHONPATH="$PWD" python nl1c7b/initial_constraint_certification_repair09.py \
  --trace "$TRACE" \
  --coverage-json "$COVERAGE" \
  --repair08-json "$R8_JSON" \
  --repair08-npz "$R8_NPZ" \
  --out "$OUT" \
  2>&1 | tee "$LOG"
rc=${PIPESTATUS[0]}
set -e

echo "SCIENCE_RC=${rc}"
test "$rc" -eq 0 -o "$rc" -eq 2

python - <<'PY'
import json
p='results/nl1c7b4_repair09_repair08_exact_constraint_retest.json'
d=json.load(open(p))
print('CLASSIFICATION=', d['classification'])
print('gates=', d['gates'])
print('state_anchor=', {k:v for k,v in d['state_anchor'].items() if k!='rows'})
print('dictionary_max_Q_error=', d['summary']['max_Q_target_error'])
print('n_constraint_pass=', d['summary']['n_constraint_pass'], '/', d['summary']['n_constraint_cases'])
print('max_epsilon_H=', d['summary']['max_epsilon_H'])
print('max_epsilon_M=', d['summary']['max_epsilon_M'])
print('min_max_epsilon_H=', d['summary']['min_max_epsilon_H'])
print('min_max_epsilon_M=', d['summary']['min_max_epsilon_M'])
print('constraint_limit=', d['summary']['constraint_limit'])
print('grid_pass=', d['gates']['R9_G5_two_grid_control'])
print('grid_ratio_max_H=', max(x['rms_ratio_H'] for x in d['grid_control']))
print('grid_ratio_max_M=', max(x['rms_ratio_M'] for x in d['grid_control']))
PY

exit "$rc"
