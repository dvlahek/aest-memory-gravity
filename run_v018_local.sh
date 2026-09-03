#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
WORK="$ROOT/_class_work"
SHA="e85808324f51fc694d12e3ed7439552a3c3f9540"
REPO="https://github.com/lesgourg/class_public.git"

rm -rf "$WORK"
mkdir -p "$WORK" "$ROOT/results"

git clone --no-checkout "$REPO" "$WORK/pristine"
git -C "$WORK/pristine" checkout "$SHA"
cp -a "$WORK/pristine" "$WORK/patched"

python3 "$ROOT/apply_patch.py" "$WORK/patched"

gcc -O2 -I"$ROOT/patch/include" "$ROOT/patch/source/aest_memory.c" "$ROOT/tests/test_aest_memory_module.c" -lm -o "$WORK/test_aest_memory_module"

"$WORK/test_aest_memory_module" | tee "$ROOT/results/module_selftest.txt"
STATUS="$(awk -F= '/^status=/{print $2}' "$ROOT/results/module_selftest.txt")"
MAXREL="$(awk -F= '/^max_relative_kernel_error=/{print $2}' "$ROOT/results/module_selftest.txt")"
python3 - "$STATUS" "$MAXREL" "$ROOT/results/module_selftest.json" <<'PY'
import json,sys
from pathlib import Path
status=int(sys.argv[1]); maxrel=float(sys.argv[2]); out=Path(sys.argv[3])
out.write_text(json.dumps({"status":status,"max_relative_kernel_error":maxrel,"gate_status":"PASS" if status==0 else "FAIL"},indent=2))
PY
test "$STATUS" = "0"

make -C "$WORK/pristine" -j2 class
make -C "$WORK/patched" -j2 class
nm "$WORK/patched/class" | grep aest_memory_module_version >/dev/null

mkdir -p "$WORK/pristine/output" "$WORK/patched/output"
(cd "$WORK/pristine" && ./class base_2018_plikHM_TTTEEE_lowl_lowE_lensing.ini)
(cd "$WORK/patched" && ./class base_2018_plikHM_TTTEEE_lowl_lowE_lensing.ini)

python3 "$ROOT/compare_class_outputs.py" "$WORK/pristine/output" "$WORK/patched/output" --json-out "$ROOT/results/off_baseline_compare.json"

python3 - "$ROOT/results/build_report.json" <<'PY'
import json,sys
from pathlib import Path
Path(sys.argv[1]).write_text(json.dumps({"pristine_build":"PASS","patched_build":"PASS","linked_symbol":"aest_memory_module_version"},indent=2))
PY

cd "$ROOT"
python3 make_v018_report.py
