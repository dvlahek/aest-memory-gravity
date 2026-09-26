#!/usr/bin/env bash
# GE19 H4F3d12r1: reproduce exact ORIGINAL D11-derived restricted D12 archive.
# No actual F21, full GE05 bath, full H4 Ward or Z21 certification.
set -euo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
[[ "$(git symbolic-ref --quiet --short HEAD)" == "physics-first-gravitational-elasticity" ]] || {
  echo GE19_H4F3D12R1_WRONG_BRANCH; exit 4;
}
PINS=(
 "ge19/h4f3d12_predata_restricted_background_and_f21_bound.json:97b513c176f9de6e1ee55cc21d87cb23103fc707"
 "ge19/h4f3d12_restricted_background_and_conditional_f21_bound.py:d5f3184f069738679ce7fe738836ef712f60b867"
 "ge19/h4f3d12r1_restricted_background_and_conditional_f21_bound.py:794df05d6c2c7572a435ba617b0c22649a28b318"
 "ge19/h4f3d12_actual_d11_conditional_f21_bound.json.gz:30cae15e4c2992484d96d3ba0f3f02e8ea8969b1"
 "ge19/h4f3d12_freeze_manifest.json:b7b8a97ea9e27e6f31a85e7724532bb4dfc4fc4b"
 "docs/ge19_h4f3d12_restricted_background_freeze_report.md:ec2a6ab2758777d6373623dd2d869a206080e84c"
 "ge19/h4f3d11_actual_original_background_e00_independent_archive_audit.json:c3f238c2914ff18e43030ec31a3debb0edab81f1"
 "ge06/analytic_aest_directional_source_generator.py:a7afe0035054a9dca55d74a6497c081422114b4c"
 "ge07/pressureless_matter_directional_source_generator.py:cde8da77a80799cef00fc7c09c3633310fc9e3d4"
)
for entry in "${PINS[@]}"; do
  rel="${entry%%:*}"; want="${entry#*:}"
  [[ "$(git rev-parse "HEAD:$rel")" == "$want" ]] || { echo "GE19_H4F3D12R1_BLOB_MISMATCH $rel"; exit 4; }
  [[ "$(git hash-object "$ROOT/$rel")" == "$want" ]] || { echo "GE19_H4F3D12R1_WORKTREE_MISMATCH $rel"; exit 4; }
done
git diff --quiet -- ge19/run_local_h4f3d12r1_restricted_background_and_f21_bound.sh
git diff --cached --quiet -- ge19/run_local_h4f3d12r1_restricted_background_and_f21_bound.sh
echo GE19_H4F3D12R1_EXACT_FROZEN_CODE_PASS

if [[ -z "${VIRTUAL_ENV:-}" ]]; then
  [[ -f "$ROOT/.venv/bin/activate" ]] || { echo GE19_H4F3D12R1_VENV_MISSING; exit 5; }
  source "$ROOT/.venv/bin/activate"
fi
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH="$ROOT"
check() {
 local file="$1" want="$2" got
 [[ -s "$file" ]] || { echo "GE19_H4F3D12R1_MISSING $file"; exit 6; }
 got="$(sha256sum "$file" | awk '{print $1}')"
 [[ "$got" == "$want" ]] || { echo "GE19_H4F3D12R1_PARENT_SHA_MISMATCH $file $got"; exit 6; }
}
check "$ROOT/ge19/h4f3d12_predata_restricted_background_and_f21_bound.json" d704bd35c71f80133c7e5b3bb7b71423366f4a692be48fb5797526c2f31db183
check "$ROOT/ge19/h4f3d12r1_restricted_background_and_conditional_f21_bound.py" cc637acbe41941247bdf0382dfd1d517790795ba5e7c1562482e0ac0ca757017
check "$ROOT/ge19/h4f3d12_actual_d11_conditional_f21_bound.json.gz" 7f011e1f56e1e44708d4515b3593e8ad2f65921ef2cac56bdc0871e867530ef0
check "$ROOT/results/ge19_h4f3d11_actual_original_action_background_e00.json" d62436b12bb5e5d9b7cbf1ea24abd0e6c06ac3ff1bfd43a41556aef284e3d3df
check "$ROOT/results/ge19_h4f3d11_actual_original_action_background_e00.npz" 7679dc6765b87c0b1294b3915d0d1305e4fa59ac86a18d75621d5bf85c616229
check "$ROOT/results/ge19_h4f3d10r1_lossless_fourier_known_boundary.json" 69eabf101a6ec1939b32323e25b207dc419fad57eb5b2cef0858874a50cfa1d2
check "$ROOT/results/ge19_h4f3d10r1_lossless_fourier_known_boundary.npz" 85c0fbd8b56037aae98615926b70bd60739a1af2fa1ff666ffc2e95485c2749b
echo GE19_H4F3D12R1_FROZEN_ACTUAL_D11_AND_D10R1_INPUT_SHA_PASS

JSON="$ROOT/results/ge19_h4f3d12r1_LOCAL_reproduced_actual_d11_conditional_f21_bound.json"
FULL="$ROOT/results/ge19_h4f3d12r1_LOCAL_reproduced_actual_d11_conditional_f21_bound_FULL.log"
for out in "$JSON" "$FULL"; do
  [[ ! -e "$out" ]] || { echo "GE19_H4F3D12R1_NO_OVERWRITE $out"; exit 7; }
done
TMP="$(mktemp -d)"
trap 'rm -rf -- "$TMP"' EXIT
gzip -t "$ROOT/ge19/h4f3d12_actual_d11_conditional_f21_bound.json.gz"
gzip -dc "$ROOT/ge19/h4f3d12_actual_d11_conditional_f21_bound.json.gz" > "$TMP/frozen.json"
check "$TMP/frozen.json" 5d94ac19e3176e8e6d2948260b957718eba9620ea9fced2981fe2e6df2c5837e
python3 -B -c 'import numpy,sympy'
cd "$TMP"
set +e
python3 -B "$ROOT/ge19/h4f3d12r1_restricted_background_and_conditional_f21_bound.py" \
 --predata "$ROOT/ge19/h4f3d12_predata_restricted_background_and_f21_bound.json" \
 --d11-json "$ROOT/results/ge19_h4f3d11_actual_original_action_background_e00.json" \
 --d11-npz "$ROOT/results/ge19_h4f3d11_actual_original_action_background_e00.npz" \
 --json-out "$JSON" 2>&1 | tee "$FULL"
rc="${PIPESTATUS[0]}"
set -e
if [[ "$rc" -eq 0 && -s "$JSON" ]] && cmp -s "$JSON" "$TMP/frozen.json"; then
  check "$JSON" 5d94ac19e3176e8e6d2948260b957718eba9620ea9fced2981fe2e6df2c5837e
  sha256sum "$JSON" "$FULL"
  echo GE19_H4F3D12R1_ACTUAL_D11_BYTE_IDENTICAL_REPLAY_PASS_F21_OPEN
else
  echo GE19_H4F3D12R1_ACTUAL_REPLAY_OR_ARCHIVED_SHA_FAIL
  exit 8
fi
