#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results
export PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}"

# WSL/Ubuntu often ships python3 without a `python` command. The shared CLASS
# setup script intentionally remains untouched; provide a local shim only for
# this D2C6E runner so no historical GitHub workflow path is modified.
if ! command -v python >/dev/null 2>&1; then
  if command -v python3 >/dev/null 2>&1; then
    PYSHIM="$ROOT/.local/d2c6e_python_shim"
    mkdir -p "$PYSHIM"
    ln -sf "$(command -v python3)" "$PYSHIM/python"
    export PATH="$PYSHIM:$PATH"
    echo "D2C6E: using python3 via local python shim ($(command -v python3))"
  else
    echo "D2C6E: neither python nor python3 is installed" >&2
    exit 2
  fi
fi

if ! python -m pip --version >/dev/null 2>&1; then
  echo "D2C6E: Python is available but pip is missing. Install python3-pip and rerun." >&2
  exit 2
fi

# Reuse a valid local zero-safe CLASS build when available. The generated
# environment file contains absolute paths, so a file copied from another
# machine is deliberately treated as invalid.
need_setup=0
if [[ ! -f results/c3_r5_class_env.sh ]]; then
  need_setup=1
else
  # shellcheck disable=SC1091
  source results/c3_r5_class_env.sh
  if [[ -z "${C3_R5_PYTARGET:-}" || ! -d "${C3_R5_PYTARGET}" || -z "${C3_R5_CLASS_ROOT:-}" || ! -d "${C3_R5_CLASS_ROOT}" ]]; then
    need_setup=1
  fi
fi

if [[ "$need_setup" -eq 1 ]]; then
  echo "D2C6E: building local zero-safe CLASS once..."
  bash nl1c6d2c6c_r5/setup_zero_safe_class.sh
  # shellcheck disable=SC1091
  source results/c3_r5_class_env.sh
else
  echo "D2C6E: reusing local zero-safe CLASS at ${C3_R5_CLASS_ROOT}"
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
