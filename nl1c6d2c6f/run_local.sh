#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local
export PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}"

# Reuse the isolated Python environment created for D2C6E when possible.
BASE_PY=""
if command -v python3 >/dev/null 2>&1; then
  BASE_PY="$(command -v python3)"
elif command -v python >/dev/null 2>&1; then
  BASE_PY="$(command -v python)"
else
  echo "D2C6F: neither python3 nor python is installed" >&2
  exit 2
fi

VENV="$ROOT/.local/d2c6e_venv"
if [[ ! -x "$VENV/bin/python" ]]; then
  echo "D2C6F: creating isolated Python environment..."
  if ! "$BASE_PY" -m venv "$VENV"; then
    echo "D2C6F: Python venv support is missing. On Ubuntu/WSL run: sudo apt install python3-venv" >&2
    exit 2
  fi
fi

export PATH="$VENV/bin:$PATH"
python -m pip install --upgrade pip setuptools wheel
python -m pip install numpy scipy cython
python - <<'PY'
import Cython, numpy, scipy
print("D2C6F_PYTHON_ENV_PASS")
print("Cython=", Cython.__version__)
print("numpy=", numpy.__version__)
print("scipy=", scipy.__version__)
PY

# Reuse the already built zero-safe CLASS from D2C6E. Rebuild only if the
# machine-local absolute paths are absent or invalid.
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
  echo "D2C6F: building local zero-safe CLASS once..."
  bash nl1c6d2c6c_r5/setup_zero_safe_class.sh
  # shellcheck disable=SC1091
  source results/c3_r5_class_env.sh
else
  echo "D2C6F: reusing local zero-safe CLASS at ${C3_R5_CLASS_ROOT}"
fi

python -m py_compile nl1c6d2c6f/finite_eta_gravitational_source.py

LOG="results/nl1c6d2c6f_finite_eta_gravitational_source.log"
JSON="results/nl1c6d2c6f_finite_eta_gravitational_source.json"
ZIP="results/nl1c6d2c6f_local_bundle.zip"

rm -f "$LOG" "$JSON" "$ZIP"

set +e
python -u nl1c6d2c6f/finite_eta_gravitational_source.py --json-out "$JSON" 2>&1 | tee "$LOG"
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
    Path("docs/nl1c6d2c6f_finite_eta_gravitational_source_predata.md"),
    Path("docs/nl1c6d2c6f_predata_clarification.md"),
    Path("nl1c6d2c6f/finite_eta_gravitational_source.py"),
    Path("nl1c6d2c6f/run_local.sh"),
    Path("nl1c6d2c6f/README_LOCAL.md"),
    Path("docs/nl1c6d2c6e_larger_eta_result.md"),
    Path("docs/nl1c6d2c5_action_level_flrw_longitudinal_derivation.md"),
    Path("docs/nl1c3b_longitudinal_3plus1_memory_bridge_result.md"),
    Path("docs/d2c6c_d2c6d_resolution_postmortem_2026-09-10.md"),
]
with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
    for path in paths:
        if path.exists():
            zf.write(path, arcname=str(path))
print(f"D2C6F_BUNDLE={zip_path}")
PY

echo "D2C6F_EXIT=$code"
echo "D2C6F_LOG=$LOG"
echo "D2C6F_JSON=$JSON"
echo "D2C6F_ZIP=$ZIP"
exit "$code"
