#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results .local
export PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}"

BASE_PY=""
if command -v python3 >/dev/null 2>&1; then
  BASE_PY="$(command -v python3)"
elif command -v python >/dev/null 2>&1; then
  BASE_PY="$(command -v python)"
else
  echo "D2C6F-R2: neither python3 nor python is installed" >&2
  exit 2
fi

VENV="$ROOT/.local/d2c6e_venv"
if [[ ! -x "$VENV/bin/python" ]]; then
  echo "D2C6F-R2: creating isolated Python environment..."
  if ! "$BASE_PY" -m venv "$VENV"; then
    echo "D2C6F-R2: Python venv support is missing. On Ubuntu/WSL run: sudo apt install python3-venv" >&2
    exit 2
  fi
fi
export PATH="$VENV/bin:$PATH"

if ! python - <<'PY'
import Cython, numpy, scipy
print("D2C6F_R2_PYTHON_ENV_PASS")
print("Cython=", Cython.__version__)
print("numpy=", numpy.__version__)
print("scipy=", scipy.__version__)
PY
then
  echo "D2C6F-R2: installing missing local Python dependencies..."
  python -m pip install --upgrade pip setuptools wheel
  python -m pip install numpy scipy cython
fi

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
  echo "D2C6F-R2: building local zero-safe CLASS once..."
  bash nl1c6d2c6c_r5/setup_zero_safe_class.sh
  # shellcheck disable=SC1091
  source results/c3_r5_class_env.sh
else
  echo "D2C6F-R2: reusing local zero-safe CLASS at ${C3_R5_CLASS_ROOT}"
fi

python -m py_compile nl1c6d2c6f_r2/vector_phase_direct_source.py

LOG="results/nl1c6d2c6f_r2_vector_phase_direct_source.log"
JSON="results/nl1c6d2c6f_r2_vector_phase_direct_source.json"
ZIP="results/nl1c6d2c6f_r2_local_bundle.zip"
rm -f "$LOG" "$JSON" "$ZIP"

set +e
python -u nl1c6d2c6f_r2/vector_phase_direct_source.py --json-out "$JSON" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

python - "$ZIP" "$LOG" "$JSON" <<'PY'
from pathlib import Path
import sys
import zipfile
zip_path=Path(sys.argv[1])
paths=[
    Path(sys.argv[2]), Path(sys.argv[3]),
    Path("docs/nl1c6d2c6f_r2_vector_phase_source_predata.md"),
    Path("docs/nl1c6d2c6f_r2_predata_diagnostic_scope.md"),
    Path("docs/nl1c6d2c6g_blocked_pending_r2.md"),
    Path("docs/nl1c6d2c6f_r1_direct_bath_source_convergence_result.md"),
    Path("docs/nl0b_covariant_memory_completion_result.md"),
    Path("nl1c6d2c6f_r2/vector_phase_direct_source.py"),
    Path("nl1c6d2c6f_r2/run_local.sh"),
    Path("nl1c6d2c6f_r2/README_LOCAL.md"),
    Path("nl1c6d2c6f/finite_eta_gravitational_source.py"),
    Path("nl1c6d2c6f_r1/direct_bath_source_convergence.py"),
]
with zipfile.ZipFile(zip_path,"w",compression=zipfile.ZIP_DEFLATED) as zf:
    for p in paths:
        if p.exists(): zf.write(p,arcname=str(p))
print(f"D2C6F_R2_BUNDLE={zip_path}")
PY

echo "D2C6F_R2_EXIT=$code"
echo "D2C6F_R2_LOG=$LOG"
echo "D2C6F_R2_JSON=$JSON"
echo "D2C6F_R2_ZIP=$ZIP"
exit "$code"
