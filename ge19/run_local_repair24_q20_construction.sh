#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results

echo "=== GE19 Repair24 lock audit ==="

test "$(git rev-parse HEAD:docs/ge19_repair22_z20_certification_result_freeze.md)" = "fb4ef607d17b5545985edf557aa67d02bc4dff0f"
test "$(git rev-parse HEAD:docs/ge19_repair23_q20_normalized_bath_bridge_result_freeze.md)" = "5081fdf87e7e7f76849cf94e01f74c8df5dcca80"
test "$(git rev-parse HEAD:ge19/repair24_predata_q20_construction.json)" = "df2a197a87c426b2b45aca8ab95bbdbbbbc19fbf"
test "$(git rev-parse HEAD:ge19/repair24_q20_construction.py)" = "fc271987d1bddcd023cc9c057ddcad036b1d72fb"
test "$(git rev-parse HEAD:.github/workflows/ge19-repair24-prelock-audit.yml)" = "bc6bd4d441b7322a42f0f27094e0360370796a6f"
test "$(git rev-parse HEAD:docs/ge19_repair24_q20_construction_implementation_lock.md)" = "4ad007e9ac012f507019e7095ae7cf0bbe21f409"

for sha in   9174f2e622f42851474ed124b429bf07b2db3ac7   79597296185209e50ef133f680d7b3d3481bac86   e093edcb4fd81bec9f45f31c0c9be60937304c52   ac4814e24694ae01f5fc955d42ca92020b015687   6aead31bb9bdcb9ee384f37b84e73dfec8b82e6b   ca7b494616fffc0179486a731183af1e1d1728f2 \
  7218e049e5e3a1a413663f587d98f8100f22cfa4 \
  3027179251e227cf4285cc9ae75d2c20770a96b2 \
  18c80840855480130cc08345e097d487a6ed5991
do
  git merge-base --is-ancestor "$sha" HEAD
done

echo "GE19_REPAIR24_LOCK_PASS"

if [[ -z "${VIRTUAL_ENV:-}" ]]; then
  echo "GE19_REPAIR24_VENV_NOT_ACTIVE"
  echo "Run: source .venv/bin/activate"
  exit 5
fi

python3 -m py_compile ge19/repair24_q20_construction.py

echo "=== GE19 Repair24 frozen local GE19 inputs ==="
for f in   results/ge19_repair22_on_shell_parent_z20_certification.json   results/ge19_repair22_on_shell_parent_z20_certification.npz   results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.json   results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz   results/ge15_R1_dense_accepted_step_trace.dat   results/ge15_R1_cli_background.dat
do
  test -s "$f" || { echo "MISSING=$f"; exit 4; }
done

test "$(sha256sum results/ge19_repair22_on_shell_parent_z20_certification.json | awk '{print $1}')" =   "7d53b2458183c6b2cc326acdded70b2c3ce1fab959d8456e56d3b4f1f86ef374"
test "$(sha256sum results/ge19_repair22_on_shell_parent_z20_certification.npz | awk '{print $1}')" =   "3020e0d040f902ab2609e05705f4508d9919665b1344fa0e641644ea8fc41a16"
test "$(sha256sum results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.json | awk '{print $1}')" =   "ae3cc790ecffbd5498b5852273c72ae578d4615de29bbb616673c05cdb3e74b7"
test "$(sha256sum results/ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz | awk '{print $1}')" =   "011c0ae54fd21d70c0e2c695ce62e7b74a3c5529a07c9023c882a447d5b40ca3"

echo "GE19_REPAIR24_GE19_INPUTS_PASS"

echo "=== GE19 Repair24 frozen v0.77 artifact ==="
ARTROOT="$ROOT/frozen_v077_repair24"
TRACE="$(find "$ARTROOT" -type f -name v076_v077_base_trace.dat -print -quit 2>/dev/null || true)"

if [[ -z "$TRACE" ]]; then
  command -v gh >/dev/null 2>&1 || {
    echo "GE19_REPAIR24_GH_NOT_AVAILABLE"
    echo "Install/authenticate GitHub CLI or place artifact 10090367181 under $ARTROOT"
    exit 6
  }
  rm -rf "$ARTROOT"
  mkdir -p "$ARTROOT"
  gh run download 34315590099     --repo dvlahek/aest-memory-gravity     --name results_bundle_v077_native_state_tangent_affinity     --dir "$ARTROOT"
  TRACE="$(find "$ARTROOT" -type f -name v076_v077_base_trace.dat -print -quit)"
fi

test -n "$TRACE"
test -s "$TRACE"
test "$(sha256sum "$TRACE" | awk '{print $1}')" =   "98c8468e8ccdf902cad8d6e65f3852e863c6fd19df62ece61353ab725ac5a43e"
test "$(wc -c < "$TRACE" | tr -d ' ')" = "2657188"

echo "TRACE=$TRACE"
echo "GE19_REPAIR24_V077_INPUT_PASS"

rm -f   results/ge19_repair24_q20_construction.json   results/ge19_repair24_q20_construction.npz   results/ge19_repair24_q20_construction_FULL.log

echo "=== GE19 Repair24 q20 science execution ==="
set -o pipefail
python3 ge19/repair24_q20_construction.py   --results-dir results   --v077-trace "$TRACE"   --json-out results/ge19_repair24_q20_construction.json   --npz-out results/ge19_repair24_q20_construction.npz   2>&1 | tee results/ge19_repair24_q20_construction_FULL.log
SCIENCE_EXIT=${PIPESTATUS[0]}

echo "=== GE19 Repair24 summary ==="
if [[ -s results/ge19_repair24_q20_construction.json ]]; then
python3 - <<'PY'
import hashlib,json
from pathlib import Path

p=Path("results/ge19_repair24_q20_construction.json")
d=json.loads(p.read_text())
print("CLASSIFICATION =",d["classification"])
print("Q20_CONSTRUCTED =",d["q20_constructed"])
print("Q20_CERTIFIED_PROJECTION =",d["q20_certified_projection"])
print("Z21_LICENSED_AFTER_FREEZE =",d["Z21_licensed_after_freeze"])
print("FULL_HISTORY_BOUNDARY =",d["full_history_boundary"])
print("CONTROLS =",d["controls"])
print("GATES =",d["gates"])
print("CLAIM_BOUNDARY =",d["claim_boundary"])

for fn in [
  "results/ge19_repair24_q20_construction.json",
  "results/ge19_repair24_q20_construction.npz",
  "results/ge19_repair24_q20_construction_FULL.log",
]:
    q=Path(fn)
    if q.exists():
        print("SHA256",fn,hashlib.sha256(q.read_bytes()).hexdigest(),"BYTES",q.stat().st_size)
PY
fi

echo "GE19_REPAIR24_SCIENCE_EXIT=$SCIENCE_EXIT"
if [[ "$SCIENCE_EXIT" -eq 0 ]]; then
  echo "GE19_REPAIR24_EXECUTION_COMPLETE"
fi
exit "$SCIENCE_EXIT"
