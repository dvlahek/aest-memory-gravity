#!/usr/bin/env bash
set -euo pipefail

R17_FREEZE_COMMIT='6a2cbd69218b63d8d7891e9deef43764365c47ff'
PREREG_COMMIT='ddec97d478bfd667666830fb0e2203b7334464f5'
IMPLEMENTATION_COMMIT='c59b0c5c770de137085ea647784ae835e384fe0b'
LOCK_COMMIT='10e4f3bd0ee4f1d578eb1c1382e8e3648e8e6f40'

R17_FREEZE_BLOB='c800a4e296fa23d3d7596e5730609d2f87e15a3c'
PREREG_BLOB='2ce19a30603e9d8ba5ade43a8c6d629464c171c5'
IMPLEMENTATION_BLOB='c0e589fe120a148148c2e21406219e197d2c16db'
LOCK_BLOB='3ab94751f72098f128068cc2e53057be6381c914'
R17_BLOB='c39d9e7bc20eef55fbd0bcea2bd19f42d8cfd8b5'
R16_BLOB='fbd7d24f748fc398638d4eea4b7707801161e52a'
R10_BLOB='c72a85d6d42176fb8c6a5ebf5f8e101541272701'
R9_BLOB='0cd67cecfbd590cb8819ad37314dc5b49047bc93'
R2_BLOB='eff076ec9a511f64bc693dc48b07b2ce26cfbaeb'
R1_BLOB='253a0ae2a19a597f06358704ea276c9005973af3'
B4_BLOB='8559120dc273be3174eca130ca313ed6ff5acb25'
R8_BLOB='94fb3f42a7c819b0525860f7344d5dbaff93da19'
REC_BLOB='ff383c1ddc2cb2a684e2b5dd11fde0ae811e4fac'

R15A_JSON='results/nl1c7b4_repair15a_density_q_completed_state.json'
R15A_NPZ='results/nl1c7b4_repair15a_density_q_completed_primary_states.npz'
R16_JSON='results/nl1c7b4_repair16_repair15a_exact_constraint_retest.json'
R17_JSON='results/nl1c7b4_repair17_repair16_source_localization.json'
TRACE='input/dense/nl1c7a_repair01_dense_trace.dat'
COVERAGE='input/dense/nl1c7a_repair01_dense_coverage.json'
OUT='results/nl1c7b4_repair18_minimal_nonlinear_projection_feasibility.json'
LOG='results/nl1c7b4_repair18_minimal_nonlinear_projection_feasibility.log'

R15A_JSON_SHA='596c7b13c4683840bcf40f6850356e179e77f873c3a3b42ba0b54730ae80811d'
R15A_NPZ_SHA='997d0033eeed1f3e60c1907c7938a0ea87a1cf38de6ab860340bd003d18d6e6e'
R16_JSON_SHA='a225f435ef61eaf33a1b4466eea678b23d1a221a537589bd8e2b0717ed66335b'
R17_JSON_SHA='09750aeb9fdce7bbbbe148c8478b9af5067a72ab20a1e48171f5a9e3a1d4b82e'

for c in "$R17_FREEZE_COMMIT" "$PREREG_COMMIT" "$IMPLEMENTATION_COMMIT" "$LOCK_COMMIT"; do
  git merge-base --is-ancestor "$c" HEAD || { echo "LOCK ancestry failure: $c" >&2; exit 91; }
done

check_blob () {
  local p="$1" expected="$2"
  local got
  got="$(git rev-parse "HEAD:$p")"
  test "$got" = "$expected" || { echo "blob mismatch $p: $got != $expected" >&2; exit 92; }
}

check_blob docs/nl1c7b4_repair17_result_freeze.md "$R17_FREEZE_BLOB"
check_blob docs/nl1c7b4_repair18_predata_minimal_nonlinear_projection_feasibility.md "$PREREG_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair18.py "$IMPLEMENTATION_BLOB"
check_blob docs/nl1c7b4_repair18_implementation_lock.md "$LOCK_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair17.py "$R17_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair16.py "$R16_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair10.py "$R10_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair09.py "$R9_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair02.py "$R2_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair01.py "$R1_BLOB"
check_blob nl1c7b/initial_constraint_certification.py "$B4_BLOB"
check_blob nl1c7a/evaluate_identity_preserving_repair08.py "$R8_BLOB"
check_blob nl1c7a/a6_a10_spherical_reconstruction.py "$REC_BLOB"

for f in "$R15A_JSON" "$R15A_NPZ" "$R16_JSON" "$R17_JSON" "$TRACE" "$COVERAGE"; do
  test -s "$f" || { echo "missing input: $f" >&2; exit 93; }
done

test "$(sha256sum "$R15A_JSON" | awk '{print $1}')" = "$R15A_JSON_SHA" || exit 94
test "$(sha256sum "$R15A_NPZ" | awk '{print $1}')" = "$R15A_NPZ_SHA" || exit 95
test "$(sha256sum "$R16_JSON" | awk '{print $1}')" = "$R16_JSON_SHA" || exit 96
test "$(sha256sum "$R17_JSON" | awk '{print $1}')" = "$R17_JSON_SHA" || exit 97

echo 'NL1C7B4_REPAIR18_LOCK_PASS'
echo "HEAD=$(git rev-parse HEAD)"
echo "REPAIR17_JSON_SHA256=$R17_JSON_SHA"

mkdir -p results
set +e
PYTHONPATH="$PWD" python nl1c7b/initial_constraint_certification_repair18.py   --trace "$TRACE"   --coverage-json "$COVERAGE"   --repair15a-json "$R15A_JSON"   --repair15a-npz "$R15A_NPZ"   --repair16-json "$R16_JSON"   --repair17-json "$R17_JSON"   --out "$OUT"   2>&1 | tee "$LOG"
rc=$?
set -e

echo "SCIENCE_RC=$rc"
test "$rc" -eq 0 -o "$rc" -eq 2

python - <<'PY'
import hashlib, json, pathlib
p=pathlib.Path('results/nl1c7b4_repair18_minimal_nonlinear_projection_feasibility.json')
d=json.loads(p.read_text())
print('CLASSIFICATION=',d['classification'])
print('gates=',d['gates'])
print('summary=',d['summary'])
print()
print('SCALING:')
for row in d['correction_scaling']:
    print(
      'scale=',row['scale_hinv_Mpc'],'Nr=',row['Nr'],
      '| norms=',row['combined_norms'],
      '| slopes=',row['adjacent_log2_slopes'],
      '| pass=',row['pass']
    )
print()
print('GRID CONTROL:')
for row in d['two_grid_correction_amplitude']:
    print(
      'scale=',row['scale_hinv_Mpc'],
      '| C256=',row['combined_norm_256'],
      '| C512=',row['combined_norm_512'],
      '| ratio=',row['symmetric_ratio'],
      '| pass=',row['pass']
    )
print()
print('LAMBDA=1 CANONICAL SOLVES:')
for row in d['solve_rows']:
    if row['lambda']==1.0:
        print(
          'scale=',row['scale_hinv_Mpc'],'Nr=',row['Nr'],
          '| success=',row['solver_success'],
          '| nfev=',row['nfev'],
          '| H=',row['canonical_projected_max_epsilon_H'],
          '| M=',row['canonical_projected_max_epsilon_M'],
          '| C=',row['correction']['combined_norm'],
          '| active=',row['active_mask_nonzero'],
          '| closure_pass=',row['solve_closure_pass']
        )
print('JSON_SHA256=',hashlib.sha256(p.read_bytes()).hexdigest())
PY

exit "$rc"
