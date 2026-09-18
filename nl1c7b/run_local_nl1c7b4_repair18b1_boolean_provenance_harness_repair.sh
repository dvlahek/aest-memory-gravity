#!/usr/bin/env bash
set -euo pipefail

R18B_FREEZE_COMMIT='3edf1b11992008d7be383692369f28614ef94d6b'
PREREG_COMMIT='df6968e904ec12c75276004cf4d5bd60486d91b0'
IMPLEMENTATION_COMMIT='6e5f826ebf60f817abc78ffaf0bb1a4b8341a5e3'
LOCK_COMMIT='f63429ad0910544203c8c99d22726dbe2cc4f9b9'

R18B_FREEZE_BLOB='ee240e5caac96c69630df6786439c3c541a96e1b'
PREREG_BLOB='7874fb1cc11867d732b5f41a034f9d9ae16c6f60'
IMPLEMENTATION_BLOB='1a312dea619c46aa300cbd4c30f141d7d4b2e624'
LOCK_BLOB='1dc6d2e769e67d02201ac0dc035a5f8f9fa77076'

R18B_BLOB='9beb762d33d4026a446a1a19363e79087b5a6525'
R18A_BLOB='767199e8ab620f5d6dabd50d0efde9828f22048b'
R16_BLOB='fbd7d24f748fc398638d4eea4b7707801161e52a'
R1_BLOB='253a0ae2a19a597f06358704ea276c9005973af3'
R9_BLOB='0cd67cecfbd590cb8819ad37314dc5b49047bc93'
B4_BLOB='8559120dc273be3174eca130ca313ed6ff5acb25'
R8_BLOB='94fb3f42a7c819b0525860f7344d5dbaff93da19'
REC_BLOB='ff383c1ddc2cb2a684e2b5dd11fde0ae811e4fac'

R15A_JSON='results/nl1c7b4_repair15a_density_q_completed_state.json'
R15A_NPZ='results/nl1c7b4_repair15a_density_q_completed_primary_states.npz'
R16_JSON='results/nl1c7b4_repair16_repair15a_exact_constraint_retest.json'
R17_JSON='results/nl1c7b4_repair17_repair16_source_localization.json'
R18_JSON='results/nl1c7b4_repair18_minimal_nonlinear_projection_feasibility.json'
R18A_JSON='results/nl1c7b4_repair18a_dimensionless_rt_coordinate_feasibility.json'
R18B_JSON='results/nl1c7b4_repair18b_jacobian_fidelity_diagnostic.json'
TRACE='input/dense/nl1c7a_repair01_dense_trace.dat'
COVERAGE='input/dense/nl1c7a_repair01_dense_coverage.json'

OUT='results/nl1c7b4_repair18b1_boolean_provenance_harness_repair.json'
LOG='results/nl1c7b4_repair18b1_boolean_provenance_harness_repair.log'

R15A_JSON_SHA='596c7b13c4683840bcf40f6850356e179e77f873c3a3b42ba0b54730ae80811d'
R15A_NPZ_SHA='997d0033eeed1f3e60c1907c7938a0ea87a1cf38de6ab860340bd003d18d6e6e'
R16_JSON_SHA='a225f435ef61eaf33a1b4466eea678b23d1a221a537589bd8e2b0717ed66335b'
R17_JSON_SHA='09750aeb9fdce7bbbbe148c8478b9af5067a72ab20a1e48171f5a9e3a1d4b82e'
R18_JSON_SHA='8f8b6ce1316bd5cad3442ebd0cba692e4d4c82060685da083517b990cac36922'
R18A_JSON_SHA='29a81013b42ebe22989ca1a00b48bb2bb33447677bb77db6aefee298c7159782'
R18B_JSON_SHA='cbb68157c2408d8d52c180586db0b7d6f007c584d48c5ffc8c8d272b74a6c855'

for c in "$R18B_FREEZE_COMMIT" "$PREREG_COMMIT" "$IMPLEMENTATION_COMMIT" "$LOCK_COMMIT"; do
  git merge-base --is-ancestor "$c" HEAD || { echo "LOCK ancestry failure: $c" >&2; exit 91; }
done

check_blob () {
  local p="$1" expected="$2"
  local got
  got="$(git rev-parse "HEAD:$p")"
  test "$got" = "$expected" || {
    echo "blob mismatch $p: $got != $expected" >&2
    exit 92
  }
}

check_blob docs/nl1c7b4_repair18b_result_freeze.md "$R18B_FREEZE_BLOB"
check_blob docs/nl1c7b4_repair18b1_predata_boolean_provenance_harness_repair.md "$PREREG_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair18b1.py "$IMPLEMENTATION_BLOB"
check_blob docs/nl1c7b4_repair18b1_implementation_lock.md "$LOCK_BLOB"

check_blob nl1c7b/initial_constraint_certification_repair18b.py "$R18B_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair18a.py "$R18A_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair16.py "$R16_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair01.py "$R1_BLOB"
check_blob nl1c7b/initial_constraint_certification_repair09.py "$R9_BLOB"
check_blob nl1c7b/initial_constraint_certification.py "$B4_BLOB"
check_blob nl1c7a/evaluate_identity_preserving_repair08.py "$R8_BLOB"
check_blob nl1c7a/a6_a10_spherical_reconstruction.py "$REC_BLOB"

for f in "$R15A_JSON" "$R15A_NPZ" "$R16_JSON" "$R17_JSON" "$R18_JSON" "$R18A_JSON" "$R18B_JSON" "$TRACE" "$COVERAGE"; do
  test -s "$f" || { echo "missing input: $f" >&2; exit 93; }
done

test "$(sha256sum "$R15A_JSON" | awk '{print $1}')" = "$R15A_JSON_SHA" || exit 94
test "$(sha256sum "$R15A_NPZ" | awk '{print $1}')" = "$R15A_NPZ_SHA" || exit 95
test "$(sha256sum "$R16_JSON" | awk '{print $1}')" = "$R16_JSON_SHA" || exit 96
test "$(sha256sum "$R17_JSON" | awk '{print $1}')" = "$R17_JSON_SHA" || exit 97
test "$(sha256sum "$R18_JSON" | awk '{print $1}')" = "$R18_JSON_SHA" || exit 98
test "$(sha256sum "$R18A_JSON" | awk '{print $1}')" = "$R18A_JSON_SHA" || exit 99
test "$(sha256sum "$R18B_JSON" | awk '{print $1}')" = "$R18B_JSON_SHA" || exit 100

echo 'NL1C7B4_REPAIR18B1_LOCK_PASS'
echo "HEAD=$(git rev-parse HEAD)"
echo "REPAIR18B_JSON_SHA256=$R18B_JSON_SHA"

mkdir -p results
set +e
PYTHONPATH="$PWD" python nl1c7b/initial_constraint_certification_repair18b1.py   --trace "$TRACE"   --coverage-json "$COVERAGE"   --repair15a-json "$R15A_JSON"   --repair15a-npz "$R15A_NPZ"   --repair16-json "$R16_JSON"   --repair17-json "$R17_JSON"   --repair18-json "$R18_JSON"   --repair18a-json "$R18A_JSON"   --repair18b-json "$R18B_JSON"   --out "$OUT"   2>&1 | tee "$LOG"
rc=$?
set -e

echo "SCIENCE_RC=$rc"
test "$rc" -eq 0 -o "$rc" -eq 2

python - <<'PY'
import hashlib, json, pathlib
p=pathlib.Path('results/nl1c7b4_repair18b1_boolean_provenance_harness_repair.json')
d=json.loads(p.read_text())
print('CLASSIFICATION=',d['classification'])
print('GATES=',d['gates'])
print('PAYLOAD_REPRODUCTION=',d['payload_reproduction'])
print('SUMMARY=',d['summary'])
for row in d['rows']:
    print()
    print(
      'scale=',row['scale_hinv_Mpc'],
      '| frob=',row['relative_Frobenius_sparse_vs_dense'],
      '| match=',row['jacobian_structure_match'],
      '| rank=',row['dense_numerical_rank'],'/',row['n_unknowns'],
      '| sigma_ratio=',row['dense_sigma_min_over_sigma_max'],
      '| linear_success=',row['linear_lsq_success'],
      '| dxmax=',row['linear_lsq_max_abs_coordinate']
    )
    print('operator_action=',row['deterministic_operator_action_relative_differences'])
    for q in row['exact_nonlinear_alpha_probes']:
        print(
          ' alpha=',q['alpha'],
          '| H=',q['max_epsilon_H'],
          '| M=',q['max_epsilon_M'],
          '| F_L2=',q['frozen_parent_normalized_residual_l2'],
          '| C=',q['correction']['combined_norm'],
          '| bound=',q['within_bounds']
        )
print('JSON_SHA256=',hashlib.sha256(p.read_bytes()).hexdigest())
PY

exit "$rc"
