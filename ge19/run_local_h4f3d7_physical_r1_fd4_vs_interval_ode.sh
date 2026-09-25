#!/usr/bin/env bash
# GE19 H4F3d7 PHYSICAL original-R1 interval ODE versus sampled FD4 audit.
# This runner does not execute manufactured inputs, certify bath on-shell,
# test full H4 Noether, solve Z21, or touch historical result files.
set -euo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ "$(git symbolic-ref --quiet --short HEAD)" != "physics-first-gravitational-elasticity" ]]; then
  echo GE19_H4F3D7_WRONG_BRANCH
  exit 4
fi
# Freeze exact committed implementations and protect against local worktree
# substitutions. Physical input bytes are checked separately below.
PINNED=(
  "ge19/h4f3d7_predata_bath_fd4_vs_original_r1_interval_ode.json:ccf3185b4f790d9d6068f80beb39a442b186158c"
  "ge19/h4f3d7_bath_fd4_vs_original_r1_interval_ode.py:b598a5cc49b3d87827b4758c55d3ce7f3a1198a8"
  "ge19/h4f3d6_actual_normalized_bath_parent_ward.py:0419145499f5f44e06ba0c96f779c2a604e84ce7"
  "ge19/h4f3b_actual_corrected_six_piece_source.py:0423cbc64f6cda3b2a9aeb67c734935ef3ae7f9c"
  "ge19/repair24_q20_construction.py:fc271987d1bddcd023cc9c057ddcad036b1d72fb"
  "ge19/repair37_cancellation_safe_fd8_h4_z21_reclosure.py:45d203a092f9ac71cc612b15df5f0c0c630f5898"
  "docs/ge19_h4f3d6_valid_local_actual_bath_parent_ward_subset_freeze.md:a78dee66657a1c9fddb952d29a1084a9f48ce3ea"
  "docs/ge19_h4f3d7_r1_fd4_compiler_valid_freeze.md:620cec44adce30fbaa8cd25c569872227af3831e"
  ".github/workflows/ge19-h4f3d7-r1-fd4-compiler.yml:ded2330eb9d9853bcaf1791a93a037261b04d98d"
)
for entry in "${PINNED[@]}"; do
  rel="${entry%%:*}"
  expected="${entry#*:}"
  [[ "$(git rev-parse "HEAD:$rel")" == "$expected" ]] || { echo "GE19_H4F3D7_CODE_BLOB_MISMATCH $rel"; exit 4; }
  git diff --quiet -- "$rel" || { echo "GE19_H4F3D7_DIRTY_CODE $rel"; exit 4; }
  git diff --cached --quiet -- "$rel" || { echo "GE19_H4F3D7_STAGED_CODE $rel"; exit 4; }
done
git diff --quiet -- ge19/run_local_h4f3d7_physical_r1_fd4_vs_interval_ode.sh
git diff --cached --quiet -- ge19/run_local_h4f3d7_physical_r1_fd4_vs_interval_ode.sh
echo "GE19_H4F3D7_PHYSICAL_LOCAL_LOCK_PASS"
echo "CODE_HEAD=$(git rev-parse HEAD)"
echo "RUNNER_BLOB=$(git rev-parse HEAD:ge19/run_local_h4f3d7_physical_r1_fd4_vs_interval_ode.sh)"

if [[ -z "${VIRTUAL_ENV:-}" ]]; then
  if [[ -f "$ROOT/.venv/bin/activate" ]]; then
    # Only the project's own local environment is activated automatically.
    source "$ROOT/.venv/bin/activate"
  else
    echo "GE19_H4F3D7_VENV_MISSING: source .venv/bin/activate"
    exit 5
  fi
fi
export PYTHONPATH="$ROOT"
export PYTHONDONTWRITEBYTECODE=1

SOURCE_JSON="$ROOT/results/ge19_h4f3b_actual_corrected_six_piece_source.json"
SOURCE_NPZ="$ROOT/results/ge19_h4f3b_actual_corrected_six_piece_source.npz"
D6_JSON="$ROOT/results/ge19_h4f3d6_actual_normalized_bath_parent_ward.json"
D6_NPZ="$ROOT/results/ge19_h4f3d6_actual_normalized_bath_parent_ward.npz"
TRACE="${GE19_REPAIR26_R1_TRACE:-}"
if [[ -z "$TRACE" && -s "$ROOT/results/ge19_repair26_R1_full_history_trace.dat" ]]; then
  TRACE="$ROOT/results/ge19_repair26_R1_full_history_trace.dat"
fi
if [[ -z "$TRACE" && -d "$ROOT/frozen_repair26_repair27" ]]; then
  mapfile -d '' -t traces < <(find "$ROOT/frozen_repair26_repair27" -type f -name ge19_repair26_R1_full_history_trace.dat -print0)
  if [[ "${#traces[@]}" -eq 1 ]]; then TRACE="${traces[0]}"; fi
fi
if [[ -z "$TRACE" || ! -s "$TRACE" ]]; then
  echo "GE19_H4F3D7_MISSING_OR_AMBIGUOUS_ORIGINAL_R1_TRACE: set GE19_REPAIR26_R1_TRACE to its original file"
  exit 6
fi
TRACE="$(realpath "$TRACE")"
# Fail closed on changed or incomplete ORIGINAL certified physical files.
check_sha() {
  local path="$1" expected="$2" got
  [[ -s "$path" ]] || { echo "GE19_H4F3D7_MISSING_PHYSICAL_FILE $path"; exit 6; }
  got="$(sha256sum "$path" | awk '{print $1}')"
  [[ "$got" == "$expected" ]] || { echo "GE19_H4F3D7_SHA256_MISMATCH $path $got"; exit 6; }
}
check_sha "$SOURCE_JSON" 1ec88fd3fd6b81bf30614b0cb78d722a02dd4f745e1f22cb9b8f956a44bac6c1
check_sha "$SOURCE_NPZ" 787d5d177838b05078057aa932f379dd529449ce203f5664c36cf723acb0116b
check_sha "$D6_JSON" 4607edde17c6820c85f32c0bbd774d5a58148eb01bfd0c81ce592e8c1b907791
check_sha "$D6_NPZ" 17b50c6ee584b2a8886f7114a90ea9396a127172dd9e02976b0e6275fe2fedc0
check_sha "$TRACE" 608ee0b4c868a701db6976f756b9a551cd9ddffe1e8e4ab37c5cd2361405a6f8
[[ "$(wc -c < "$TRACE" | tr -d ' ')" == "26643162" ]] || { echo GE19_H4F3D7_REPAIR26_R1_LENGTH_MISMATCH; exit 6; }
echo GE19_H4F3D7_FROZEN_H4F3B_H4F3D6_R1_SHA256_PASS

JSON="$ROOT/results/ge19_h4f3d7_physical_r1_fd4_vs_interval_ode.json"
NPZ="$ROOT/results/ge19_h4f3d7_physical_r1_fd4_vs_interval_ode.npz"
FULL="$ROOT/results/ge19_h4f3d7_physical_r1_fd4_vs_interval_ode_FULL.log"
for out in "$JSON" "$NPZ" "$FULL"; do
  [[ ! -e "$out" ]] || { echo "GE19_H4F3D7_OUTPUT_ALREADY_EXISTS_NO_OVERWRITE $out"; exit 7; }
done

# Importing historical generators may write OLD relative result names.
# Both the preflight import and the actual execution happen ONLY inside
# this disposable isolated directory, with absolute certified input/output.
TMP="$(mktemp -d)"
trap 'rm -rf -- "$TMP"' EXIT
mkdir -p "$TMP/results"
cd "$TMP"
python3 -B -c 'import numpy, scipy, sympy'
python3 -B - "$ROOT/results" "$TRACE" "$SOURCE_JSON" "$SOURCE_NPZ" "$D6_JSON" "$D6_NPZ" <<'PY'
import json
import sys
from pathlib import Path
from ge19 import h4f3d7_bath_fd4_vs_original_r1_interval_ode as d7
from ge19 import h4f3b_actual_corrected_six_piece_source as s
rd, trace, sj, sn, dj, dn = map(Path, sys.argv[1:])
assert all(v["exact"] for v in d7.exact_code_lock().values())
assert d7.stepper_ast_exact() is True
assert all(v["exact"] for v in s.code_lock().values())
files, parents = s.frozen_inputs(rd, trace)
assert all(parents[k]["exact"] for k in s.REQUIRED)
for path, expected in ((sj, d7.SOURCE_JSON_SHA), (sn, d7.SOURCE_NPZ_SHA),
                       (dj, d7.D6_JSON_SHA), (dn, d7.D6_NPZ_SHA)):
    assert d7.sha256(path) == expected, str(path)
source = json.loads(sj.read_text())
bath = json.loads(dj.read_text())
assert source["classification"] == "GE19_H4F3B_ACTUAL_CORRECTED_SIX_SOURCE_PASS_FULL_WARD_OPEN"
assert bath["classification"] == "GE19_H4F3D6_ACTUAL_BATH_PARENT_WARD_SUBSET_PASS_FULL_OPEN"
assert len(bath["cases"]) == 18
assert all(v is True for v in source["gates"].values())
assert all(v is True for v in bath["gates"].values())
print("GE19_H4F3D7_PHYSICAL_ORIGINAL_ALL_PARENT_INPUT_PASS")
print("CERTIFIED_Z11 =", files["z11"])
print("REPAIR13 =", files["r13"])
print("H3F =", files["h3fn"])
print("H3G =", files["h3gn"])
PY
echo GE19_H4F3D7_PHYSICAL_LOCAL_PREEXECUTION_PASS

set +e
python3 -B -m ge19.h4f3d7_bath_fd4_vs_original_r1_interval_ode --results-dir "$ROOT/results" --repair26-trace "$TRACE" --source-json "$SOURCE_JSON" --source-npz "$SOURCE_NPZ" --d6-json "$D6_JSON" --d6-npz "$D6_NPZ" --json-out "$JSON" --npz-out "$NPZ" 2>&1 | tee "$FULL" | tail -n 48
rc=${PIPESTATUS[0]}
set -e

if [[ -s "$JSON" ]]; then
  python3 -B - "$JSON" <<'PY'
import json
import sys
d = json.load(open(sys.argv[1]))
print("CLASSIFICATION =", d["classification"])
print("SIX_ORIGINAL_C_NT_COHORTS =", len(d["cases"]))
print("ORIGINAL_FD4_R1_ODE_UNCHANGED =", d["original_FD4_and_R1_ODE_unchanged"])
print("BATH_ON_SHELL_SMALLNESS_GATE_INTRODUCED =", d["new_bath_on_shell_smallness_gate_introduced"])
print("FULL_NOETHER_CERTIFIED =", d["full_all_sector_H4_Noether_certified"])
print("Z21_CERTIFIED =", d["Z21_certified"])
PY
fi
for p in "$JSON" "$NPZ" "$FULL"; do
  if [[ -s "$p" ]]; then sha256sum "$p"; wc -c "$p"; fi
done
if [[ "$rc" -eq 0 && -s "$JSON" && -s "$NPZ" ]]; then
  echo GE19_H4F3D7_PHYSICAL_DECOMPOSITION_PASS_FULL_NOETHER_OPEN
elif [[ "$rc" -eq 2 && -s "$JSON" && -s "$NPZ" ]]; then
  echo GE19_H4F3D7_PHYSICAL_DIAGNOSTIC_FAIL
else
  echo GE19_H4F3D7_PHYSICAL_IMPLEMENTATION_OR_INPUT_FAIL
fi
exit "$rc"
