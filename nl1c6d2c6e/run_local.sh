#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results
export PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}"

# Reuse a valid local zero-safe CLASS build when available. The generated
# environment file contains absolute paths, so a file copied from another
# machine is deliberately treated as invalid.
need_setup=0
if [[ ! -f results/c3_r5_class_env.sh ]]; then
  need_setup=1
else
  # shellcheck disable=SC1091
  source results/c3_r5_class_env.sh
  if [[ -z "${PYTARGET:-}" || ! -d "${PYTARGET}" || -z "${CLASS_ROOT:-}" || ! -d "${CLASS_ROOT}" ]]; then
    need_setup=1
  fi
fi

if [[ "$need_setup" -eq 1 ]]; then
  echo "D2C6E: building local zero-safe CLASS once..."
  bash nl1c6d2c6c_r5/setup_zero_safe_class.sh
  # shellcheck disable=SC1091
  source results/c3_r5_class_env.sh
else
  echo "D2C6E: reusing local zero-safe CLASS at ${CLASS_ROOT}"
fi

python -m py_compile nl1c6d2c6e/larger_eta_retained.py

LOG="results/nl1c6d2c6e_larger_eta_retained.log"
JSON="results/nl1c6d2c6e_larger_eta_retained.json"
ZIP="results/nl1c6d2c6e_local_bundle.zip"

rm -f "$LOG" "$JSON" "$ZIP"

set +e
python -u nl1c6d2c6e/larger_eta_retained.py --json-out "$JSON" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

python - "$ZIP" "$LOG" "$JSON" <<'PY'
from pathlib import Path
import sys
import zipfile

zip_path = Path(sys.argv[1])
paths = [
    Path(sys.argv[2]),
    Path(sys.argv[3]),
    Path("docs/nl1c6d2c6e_larger_eta_predata.md"),
    Path("nl1c6d2c6e/larger_eta_retained.py"),
    Path("nl1c6d2c6e/run_local.sh"),
    Path("docs/d2c6c_d2c6d_resolution_postmortem_2026-09-10.md"),
]
with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
    for path in paths:
        if path.exists():
            zf.write(path, arcname=str(path))
print(f"D2C6E_BUNDLE={zip_path}")
PY

echo "D2C6E_EXIT=$code"
echo "D2C6E_LOG=$LOG"
echo "D2C6E_JSON=$JSON"
echo "D2C6E_ZIP=$ZIP"
exit "$code"
