#!/usr/bin/env bash
set -euo pipefail

PREREG_COMMIT='02e1e7eaffd08aa289830810250057314594b9cf'
IMPLEMENTATION_COMMIT='95ba6dd33105ff0b4cada77e0df44ed819edf4a0'
LOCK_COMMIT='1de607cfffef8c0862ddb14f6f296a584f9e92f1'
R10_FREEZE_COMMIT='de03f563ee3e8700b3159be5a46b73633c85db8d'

PREREG_BLOB='e35181ff632bbc6461dc087d9800e63779000f18'
IMPLEMENTATION_BLOB='72d324d94100ee4555698bf44acd45c6b612c927'
LOCK_BLOB='a4a4b7fbfa33121a90880d7c00dfb5d03730d677'
R10_FREEZE_BLOB='86021d3ac9086585a2c01223a9700b6f67896f30'
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
TRACE='input/dense/nl1c7a_repair01_dense_trace.dat'
COVERAGE='input/dense/nl1c7a_repair01_dense_coverage.json'
OUT='results/nl1c7b4_repair11_esector_analytic_covariant_audit.json'
LOG='results/nl1c7b4_repair11_esector_analytic_covariant_audit.log'

R8_JSON_SHA='054851decab71e79a05aca2bc9fb287bb1239c8fb425989f40920004c3d88453'
R8_NPZ_SHA='4639f3b5c0afcddb2f98c8b9f6a9dbbf8661dac685b12d235c09075a106dafa7'
R10_JSON_SHA='f1fc1a86d2d488f5e88f0d32b0d3d1d5ce9dab22f52e51fa69801948aeb6de9d'

for c in "$PREREG_COMMIT" "$IMPLEMENTATION_COMMIT" "$LOCK_COMMIT" "$R10_FREEZE_COMMIT"; do
  git merge-base --is-ancestor "$c" HEAD || { echo "LOCK ancestry failure: $c" >&2; exit 91; }
done

check_blob () {
  local p="$1" expected="$2"
  local got
  got="$(git rev-parse "HEAD:$p")"
  test "$got" = "$expected" || { echo "blob mismatch $p: $got != $expected" >&2; exit 92; }
}

check_blob docs/nl1c7b4_repair11_predata_esector_analytic_covariant_audit.md "$PREREG_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair11.py "$IMPLEMENTATION_BLOB"
check_blob docs/nl1c7b4_repair11_implementation_lock.md "$LOCK_BLOB"
check_blob docs/nl1c7b4_repair10_result_freeze.md "$R10_FREEZE_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair10.py "$R10_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair09.py "$R9_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair01.py "$R1_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair02.py "$R2_BLOB"
check_blob nl1c7b/initial_constraint_certification.py "$B4_BLOB"
check_blob nl1c7a/evaluate_identity_preserving_repair08.py "$R8_BLOB"
check_blob nl1c7a/a6_a10_spherical_reconstruction.py "$REC_BLOB"

for f in "$R8_JSON" "$R8_NPZ" "$R10_JSON" "$TRACE" "$COVERAGE"; do
  test -s "$f" || { echo "missing input: $f" >&2; exit 93; }
done

test "$(sha256sum "$R8_JSON" | awk '{print $1}')" = "$R8_JSON_SHA" || { echo 'Repair08 JSON SHA mismatch' >&2; exit 94; }
test "$(sha256sum "$R8_NPZ" | awk '{print $1}')" = "$R8_NPZ_SHA" || { echo 'Repair08 NPZ SHA mismatch' >&2; exit 95; }
test "$(sha256sum "$R10_JSON" | awk '{print $1}')" = "$R10_JSON_SHA" || { echo 'Repair10 JSON SHA mismatch' >&2; exit 96; }

echo 'NL1C7B4_REPAIR11_LOCK_PASS'
echo "HEAD=$(git rev-parse HEAD)"
echo "REPAIR10_JSON_SHA256=$R10_JSON_SHA"

mkdir -p results
set +e
PYTHONPATH="$PWD" python nl1c7b/initial_constraint_certification_repair11.py   --trace "$TRACE"   --coverage-json "$COVERAGE"   --repair08-json "$R8_JSON"   --repair08-npz "$R8_NPZ"   --repair10-json "$R10_JSON"   --out "$OUT"   2>&1 | tee "$LOG"
rc=$?
set -e

echo "SCIENCE_RC=$rc"
test "$rc" -eq 0 -o "$rc" -eq 2

python - <<'PY'
import json
p='results/nl1c7b4_repair11_esector_analytic_covariant_audit.json'
d=json.load(open(p))
print('CLASSIFICATION=', d['classification'])
print('gates=', d['gates'])
print('first_order=', d['symbolic_audit']['first_order'])
print('quadratic=', d['symbolic_audit']['quadratic'])
print('implementation_equivalence_pass=', d['implementation_equivalence']['pass'])
print('hotspot_reproduction_pass=', d['repair10_hotspot_reproduction']['pass'])
print('scaling_min_slope=', d['amplitude_scaling']['min_slope'])
print('scaling_max_slope=', d['amplitude_scaling']['max_slope'])
print('fourier_consistency=', d['linear_fourier_consistency'])
print()
print('AMPLITUDE SLOPES:')
for row in d['amplitude_scaling']['rows']:
    print(
        'scale=',row['scale_hinv_Mpc'],'Nr=',row['Nr'],
        'E2=',row['AeST_E2_adjacent_log2_slopes'],
        'EX=',row['AeST_EX_adjacent_log2_slopes']
    )
PY

exit "$rc"
