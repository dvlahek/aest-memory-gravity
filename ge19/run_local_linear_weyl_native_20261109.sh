#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
export PYTHONPATH="$PWD"
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1

mkdir -p results
echo "=== GE19 LINEAR NATIVE WEYL: FROZEN MODEL / SINGLE CAMPAIGN ==="

python3 -m py_compile ge19/linear_weyl_native_tangent_20261109.py
python3 -u -m ge19.linear_weyl_native_tangent_20261109 --self-test

if [[ -v CLASS_ROOT ]]; then
  ROOT_DIR="$CLASS_ROOT"
else
  ROOT_DIR=""
  for candidate in \
       "$PWD/class_v077" \
       "$HOME/class_v077" \
       "$PWD/class_public" \
       "$HOME/class_public" \
       "$PWD/class" \
       "$HOME/class"; do
    if [[ -f "$candidate/class" && -d "$candidate/.git" ]]; then
      ROOT_DIR="$candidate"
      break
    fi
  done
fi
if [[ -z "$ROOT_DIR" || ! -f "$ROOT_DIR/class" ]]; then
  echo "GE19_LW01_CLASS_ROOT_MISSING" >&2
  echo "Need original patched v077 official CLASS checkout HEAD e85808324f51fc694d12e3ed7439552a3c3f9540." >&2
  echo "Set CLASS_ROOT=/absolute/path/to/class_v077 and rerun. No CLASS numerical run was started." >&2
  exit 3
fi

echo "CLASS_ROOT=$ROOT_DIR"
echo "CLASS_HEAD=$(git -C "$ROOT_DIR" rev-parse HEAD)"
if python3 -u -m ge19.linear_weyl_native_tangent_20261109 \
   --class-root "$ROOT_DIR" \
   --output-prefix results/ge19_linear_weyl_native_tangent_20261109 \
  2>&1 | tee results/ge19_linear_weyl_native_tangent_20261109.log; then
  echo "EXIT=0"
else
  code=$?
  echo "EXIT=$code"
  exit "$code"
fi
