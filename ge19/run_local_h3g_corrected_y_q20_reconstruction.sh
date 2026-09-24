#!/usr/bin/env bash
# New corrected-Y q20 parent only; never overwrite frozen Repair27 artifacts.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results

test "$(git rev-parse HEAD:ge19/h3g_predata_corrected_y_q20_reconstruction.json)" = "09fc1bd7fc06459d90fc6f6ba37a84adba757d37"
test "$(git rev-parse HEAD:ge19/h3g_corrected_y_q20_core.py)" = "688920e840a0a13bc85a6f416c2573cf0472eaa3"
test "$(git rev-parse HEAD:ge19/h3g_corrected_y_q20_reconstruction.py)" = "de929ae025e3ce58e60e6d229682cf885e7b1007"
test "$(git rev-parse HEAD:docs/ge19_h3g_corrected_y_q20_implementation_lock.md)" = "8aaa263ef8a98bb88d514a0e311e4a128e45cfa0"
test "$(git rev-parse HEAD:.github/workflows/ge19-h3g-corrected-y-preexecution.yml)" = "a6a60064cb8d979ee2c466a8a05a656d80fc6b45"
test "$(git rev-parse HEAD:ge19/repair24_q20_construction.py)" = "fc271987d1bddcd023cc9c057ddcad036b1d72fb"
test "$(git rev-parse HEAD:ge19/repair27_cancellation_free_parent_q20_reconstruction.py)" = "adbab56e67f765ab5e2b37980abae42312a55b44"
test "$(git rev-parse HEAD:docs/ge19_h3f_corrected_y_z20_valid_local_science_result_freeze.md)" = "e69fd766a36c219ecf46aa7bbf547a38c244f482"

for file in \
  ge19/h3g_predata_corrected_y_q20_reconstruction.json \
  ge19/h3g_corrected_y_q20_core.py \
  ge19/h3g_corrected_y_q20_reconstruction.py \
  ge19/repair24_q20_construction.py \
  ge19/repair27_cancellation_free_parent_q20_reconstruction.py
do
  git diff --quiet -- "$file"
  git diff --cached --quiet -- "$file"
done
echo GE19_H3G_LOCK_PASS

if [[ -z "${VIRTUAL_ENV:-}" ]]; then
  echo GE19_H3G_VENV_NOT_ACTIVE
  echo "Run: source .venv/bin/activate"
  exit 5
fi

python3 -c 'import numpy, scipy, sympy'
python3 -m py_compile ge19/h3g_corrected_y_q20_core.py ge19/h3g_corrected_y_q20_reconstruction.py
python3 -m ge19.h3g_corrected_y_q20_reconstruction --help >/dev/null
python3 - <<'PY'
from pathlib import Path
import ge19.h3g_corrected_y_q20_reconstruction as h3g
h3g.audit_unchanged_physics()
h3g.verify_h3f_parent(Path("results"))
print("GE19_H3G_LOCAL_PREEXECUTION_AUDIT_PASS")
PY

python3 - <<'PY'
from pathlib import Path
import hashlib, json
def sha(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1<<20),b""):
            h.update(chunk)
    return h.hexdigest()
inputs={
    "ge19_h3f_corrected_y_z20_science_reclosure.json":"0616188d2bb7a6c09b2b56433a1f8a1860f360b2e54d2cb84e1ae214a407866b",
    "ge19_h3f_corrected_y_z20_science_reclosure.npz":"90840755fa9febb1d8cb84609d9e58f67dec2a0a01cd6bf8e47685b45caa4542",
    "ge19_repair13_self_consistent_reduced_background_h1_reclosure.json":"ae3cc790ecffbd5498b5852273c72ae578d4615de29bbb616673c05cdb3e74b7",
    "ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz":"011c0ae54fd21d70c0e2c695ce62e7b74a3c5529a07c9023c882a447d5b40ca3",
    "ge15_R1_dense_accepted_step_trace.dat":"7f57ab676f2a31cf0abf93ff0f8b0f1f2f80bb9a58d7cf1e47e10a158c57c69f",
}
for name,want in inputs.items():
    path=Path("results")/name
    if not path.is_file():
        raise RuntimeError(f"missing frozen H3G input: {path}")
    got=sha(path)
    if got!=want:
        raise RuntimeError(f"frozen H3G input hash mismatch: {path}: {got}")
lambda_bg=Path("results/ge15_R1_cli_background.dat")
if not lambda_bg.is_file() or not lambda_bg.stat().st_size:
    raise RuntimeError("missing GE15 frozen Lambda background")
p=json.load(open("results/ge19_h3f_corrected_y_z20_science_reclosure.json"))
if p["classification"]!="GE19_H3F_CORRECTED_Y_H3_Z20_CERTIFIED":
    raise RuntimeError("H3F parent classification changed")
print("GE19_H3G_H3F_FROZEN_PARENT_PASS")
PY

ARTROOT="$ROOT/frozen_repair26_repair27"
TRACE="$(find "$ARTROOT" -type f -name ge19_repair26_R1_full_history_trace.dat -print -quit 2>/dev/null || true)"
if [[ -z "$TRACE" ]]; then
  command -v gh >/dev/null 2>&1 || {
    echo GE19_H3G_GH_NOT_AVAILABLE
    echo "Install/authenticate GitHub CLI or restore frozen Repair26 artifact 10690709843 under $ARTROOT"
    exit 6
  }
  rm -rf "$ARTROOT"
  mkdir -p "$ARTROOT"
  gh run download 35721220889 \
    --repo dvlahek/aest-memory-gravity \
    --name results_bundle_ge19_repair26_cancellation_free_full_history_bath_boundary \
    --dir "$ARTROOT"
  TRACE="$(find "$ARTROOT" -type f -name ge19_repair26_R1_full_history_trace.dat -print -quit)"
fi
test -n "$TRACE"
test -s "$TRACE"
test "$(sha256sum "$TRACE" | awk '{print $1}')" = "608ee0b4c868a701db6976f756b9a551cd9ddffe1e8e4ab37c5cd2361405a6f8"
test "$(wc -c < "$TRACE" | tr -d ' ')" = "26643162"
echo "TRACE=$TRACE"
echo GE19_H3G_REPAIR26_R1_PARENT_PASS

JSON=results/ge19_h3g_corrected_y_q20_reconstruction.json
NPZ=results/ge19_h3g_corrected_y_q20_reconstruction.npz
FULL=results/ge19_h3g_corrected_y_q20_reconstruction_FULL.log
rm -f "$JSON" "$NPZ" "$FULL"

set +e
set -o pipefail
python3 -m ge19.h3g_corrected_y_q20_reconstruction \
  --results-dir results \
  --repair26-trace "$TRACE" \
  --json-out "$JSON" \
  --npz-out "$NPZ" \
  2>&1 | tee "$FULL" | tail -n 85
rc=${PIPESTATUS[0]}
set -e

if [[ -s "$JSON" ]]; then
python3 - <<'PY'
import json
p="results/ge19_h3g_corrected_y_q20_reconstruction.json"
d=json.load(open(p))
print("CLASSIFICATION =",d["classification"])
print("ROUTE =",d["routing"]["next_route"])
print("Q20_CONSTRUCTED =",d["q20_constructed"])
print("Q20_CERTIFIED_PROJECTION =",d["q20_certified_projection"])
print("CONTROLS =",d["controls"])
print("GATES =",d["gates"])
print("FAILED_GATES =",[k for k,v in d["gates"].items() if not v])
print("PARENT_CHANGE =",d["parent_change"])
print("OLD_REPAIR27_REPORT_ONLY =",d["old_Repair27_comparator"])
print("FULL_H4_NOETHER_DERIVED =",d["full_all_sector_H4_Noether_derived"])
print("Z21_LICENSED =",d["Z21_licensed_after_freeze"])
PY
fi
for path in "$JSON" "$NPZ" "$FULL"; do
  if [[ -s "$path" ]]; then
    sha256sum "$path"
    wc -c "$path"
  fi
done
if [[ "$rc" -eq 0 && -s "$JSON" && -s "$NPZ" ]]; then
  echo GE19_H3G_CORRECTED_Y_Q20_SCIENCE_PASS
elif [[ "$rc" -eq 2 && -s "$JSON" && -s "$NPZ" ]]; then
  echo GE19_H3G_CORRECTED_Y_Q20_SCIENCE_FAIL
else
  echo GE19_H3G_IMPLEMENTATION_OR_EXECUTION_FAIL
fi
exit "$rc"
