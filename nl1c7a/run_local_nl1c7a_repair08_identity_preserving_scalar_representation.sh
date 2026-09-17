#!/usr/bin/env bash
set -euo pipefail

# NL1C7A Repair08 local runner. Uses only retained frozen inputs already present
# under input/dense and input/final. It never overwrites the historical C7A NPZ.

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

# Locked history / implementation provenance.
git merge-base --is-ancestor c32c77940b5a338fd6ca42f7251b3a1b57927fb7 HEAD
git merge-base --is-ancestor 93807f46ea532849aaf3d4dc8efdd7f25d985bd2 HEAD
git merge-base --is-ancestor b99954cace654d7edac9d202b1db8537788dc92b HEAD
git merge-base --is-ancestor d2bc5fcbf6559ecd1f80be46909a010bbd8a12c0 HEAD

test "$(git rev-parse HEAD:docs/nl1c7b4_repair07b_result_freeze.md)" = "fa0d38dcce6902b224c8d5055a883ad163dab5bd"
test "$(git rev-parse HEAD:docs/nl1c7a_repair08_identity_preserving_scalar_representation.md)" = "258c74068d0f6bfb33867e07057b1977344c022c"
test "$(git rev-parse HEAD:docs/nl1c7a_repair08_implementation_lock.md)" = "53773587917529c5d3caa318b45e4c640ddd29a9"
test "$(git rev-parse HEAD:nl1c7a/evaluate_identity_preserving_repair08.py)" = "94fb3f42a7c819b0525860f7344d5dbaff93da19"

test "$(git rev-parse HEAD:nl1c7a/a5_denominator_audit.py)" = "47b486ca2defbd1db029df003b37909a9d4d170d"
test "$(git rev-parse HEAD:nl1c7a/a6_a10_spherical_reconstruction.py)" = "ff383c1ddc2cb2a684e2b5dd11fde0ae811e4fac"
test "$(git rev-parse HEAD:nl1c7a/evaluate_dense_time_repair01.py)" = "aa84b4892586a59455ec93b6dfdc0057adc20d38"
test "$(git rev-parse HEAD:nl1c7a/make_repair01_coverage_compat.py)" = "db52f94e1b896b2d277bb306a9eb4a63ea412ead"
test "$(git rev-parse HEAD:.github/workflows/nl1c7a-repair01-evalfix.yml)" = "3e784644e92aea67c8adbc36139d72694052e5ae"

echo NL1C7A_REPAIR08_LOCK_PASS

TRACE="input/dense/nl1c7a_repair01_dense_trace.dat"
COVERAGE_RAW="input/dense/nl1c7a_repair01_dense_coverage.json"
OFFICIAL="input/final/nl1c7a_repair01_evalfix_primary_states.npz"

for f in "$TRACE" "$COVERAGE_RAW" "$OFFICIAL"; do
  test -s "$f" || { echo "MISSING_INPUT=$f" >&2; exit 3; }
done

mkdir -p results
COMPAT="results/nl1c7a_repair08_dense_coverage_compat.json"
A5="results/nl1c7a_repair08_a5.json"
OUT="results/nl1c7a_repair08_identity_preserving_scalar_representation.json"
STATE="results/nl1c7a_repair08_identity_preserving_primary_states.npz"

rm -f "$STATE"

python nl1c7a/make_repair01_coverage_compat.py \
  --input "$COVERAGE_RAW" \
  --output "$COMPAT" \
  2>&1 | tee results/nl1c7a_repair08_coverage_compat.log

set +e
set -o pipefail
python nl1c7a/a5_denominator_audit.py \
  --trace "$TRACE" \
  --coverage-json "$COMPAT" \
  --out "$A5" \
  2>&1 | tee results/nl1c7a_repair08_a5.log
A5_RC=${PIPESTATUS[0]}
set -e
if [[ "$A5_RC" -ne 0 && "$A5_RC" -ne 1 ]]; then
  echo "A5_TECHNICAL_RC=$A5_RC" >&2
  exit "$A5_RC"
fi

echo "A5_SCIENCE_RC=$A5_RC"
test -s "$A5"

set +e
set -o pipefail
PYTHONPATH="$PWD" python nl1c7a/evaluate_identity_preserving_repair08.py \
  --trace "$TRACE" \
  --coverage-json "$COMPAT" \
  --a5-json "$A5" \
  --official-npz "$OFFICIAL" \
  --out "$OUT" \
  --state-npz "$STATE" \
  2>&1 | tee results/nl1c7a_repair08_identity_preserving_scalar_representation.log
SCIENCE_RC=${PIPESTATUS[0]}
set -e

if [[ "$SCIENCE_RC" -ne 0 && "$SCIENCE_RC" -ne 2 ]]; then
  echo "UNEXPECTED_TECHNICAL_RC=$SCIENCE_RC" >&2
  exit "$SCIENCE_RC"
fi

echo "SCIENCE_RC=$SCIENCE_RC"
test -s "$OUT"

python - <<'PY'
import json, os
p='results/nl1c7a_repair08_identity_preserving_scalar_representation.json'
d=json.load(open(p))
print('CLASSIFICATION=', d['classification'])
print('gates=', d['gates'])
print('scalar_identity=', d['scalar_identity'])
print('A6_max=', d['A6']['max_active_relative_difference'], 'pass=', d['A6']['pass'])
print('A7_max=', d['A7']['max_active_relative_difference'], 'pass=', d['A7']['pass'])
print('A8_max=', d['A8']['max_error_or_mismatch'], 'pass=', d['A8']['pass'])
print('A9_max=', d['A9']['max_bridge_relative_error'], 'pass=', d['A9']['pass'])
print('regression_max=', d['unchanged_state_regression']['max_relative_L2'], 'pass=', d['unchanged_state_regression']['pass'])
print('allowed_scalar_changes=', d['unchanged_state_regression']['allowed_scalar_changes'])
print('new_state_npz_written=', d['new_state_npz_written'])
if d['new_state_npz_written']:
    q='results/nl1c7a_repair08_identity_preserving_primary_states.npz'
    print('new_state_npz_size=', os.path.getsize(q))
PY

exit "$SCIENCE_RC"
