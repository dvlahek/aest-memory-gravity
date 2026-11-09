#!/usr/bin/env bash
# GE19 LW01: locally reconstruct the exact original v077 CLASS environment,
# then run ONE preregistered linear Weyl campaign. No H4 or GitHub Actions.
set -euo pipefail
cd "$(dirname "$0")/.."
ROOT="$PWD"

if [[ -f .venv/bin/activate ]]; then
  source .venv/bin/activate
fi
command -v python3 >/dev/null
command -v git >/dev/null || { echo "Missing git" >&2; exit 2; }
command -v make >/dev/null || { echo "Missing make" >&2; exit 2; }
command -v gcc >/dev/null || { echo "Missing gcc" >&2; exit 2; }
command -v g++ >/dev/null || { echo "Missing g++" >&2; exit 2; }

PIN="e85808324f51fc694d12e3ed7439552a3c3f9540"
if [[ ! -v CLASS_ROOT ]]; then CLASS_ROOT="$ROOT/class_v077"; fi
mkdir -p results
LOG="$ROOT/results/ge19_lw01_class_bootstrap_20261109.log"
echo "GE19_LW01_CLASS_BOOTSTRAP_START" | tee -a "$LOG"
echo "CLASS_ROOT=$CLASS_ROOT" | tee -a "$LOG"

if [[ ! -e "$CLASS_ROOT" ]]; then
  echo "CHECKOUT_OFFICIAL_CLASS_PIN" | tee -a "$LOG"
  git init "$CLASS_ROOT" 2>&1 | tee -a "$LOG"
  git -C "$CLASS_ROOT" remote add origin https://github.com/lesgourg/class_public.git
  git -C "$CLASS_ROOT" fetch --depth=1 origin "$PIN" 2>&1 | tee -a "$LOG"
  git -C "$CLASS_ROOT" -c advice.detachedHead=false checkout --detach FETCH_HEAD 2>&1 | tee -a "$LOG"
fi
if [[ ! -d "$CLASS_ROOT/.git" ]]; then
  echo "Existing CLASS_ROOT is not a Git checkout; stop without modifying it." >&2
  exit 3
fi
ACTUAL="$(git -C "$CLASS_ROOT" rev-parse HEAD)"
if [[ "$ACTUAL" != "$PIN" ]]; then
  echo "CLASS_COMMIT_MISMATCH expected=$PIN got=$ACTUAL; refusing to patch." >&2
  exit 3
fi
if [[ ! -f "$CLASS_ROOT/include/common.h" ]]; then
  echo "Pinned CLASS source is incomplete; check git checkout." >&2
  exit 3
fi

# Detect complete original v077 patch signatures. Do not reapply patches
# to a dirty or partially modified checkout.
MARK="$CLASS_ROOT/.ge19_lw01_v077_patch_complete"
if [[ ! -f "$MARK" ]]; then
  if grep -Fq 'v0.75 technical runtime fix' "$CLASS_ROOT/source/aest_memory.c" 2>/dev/null &&
     grep -Fq 'v0.63 technical runtime fix' "$CLASS_ROOT/source/aest_memory.c" 2>/dev/null &&
     grep -Fq 'aest_offline_trace_state' "$CLASS_ROOT/source/aest_memory.c" 2>/dev/null; then
    echo "Existing full v077-style AeST patch signatures found; no reapplication." | tee -a "$LOG"
    printf '%s\n' "$PIN" > "$MARK"
  else
    if [[ -n "$(git -C "$CLASS_ROOT" status --porcelain)" ]]; then
      echo "CLASS checkout already modified but patch set unverified; stop without overwriting." >&2
      echo "Use a new CLASS_ROOT for a clean pinned checkout." >&2
      exit 3
    fi
    echo "APPLY_FROZEN_V077_PATCH_SEQUENCE" | tee -a "$LOG"
    for patch in \
      v019/apply_patch_v019.py \
      v019i/apply_ic_patch.py \
      v019j/apply_memory_patch.py \
      v019w/apply_variational_forcing_patch.py \
      v019y/apply_output_precision_patch.py \
      v023/apply_source_grid_trace_patch.py \
      tools/apply_v072_offline_trace_runtime_reload_patch.py \
      tools/apply_v063_classy_runtime_reload_patch.py \
      tools/apply_v075_force_path_reload_patch.py; do
        echo "PATCH $patch" | tee -a "$LOG"
        python3 "$patch" "$CLASS_ROOT" 2>&1 | tee -a "$LOG"
    done
    printf '%s\n' "$PIN" > "$MARK"
  fi
fi

if ! python3 - <<'PY'
import numpy, scipy, Cython, setuptools, wheel
PY
then
  echo "Installing v077 Python build prerequisites into active Python environment." | tee -a "$LOG"
  python3 -m pip install numpy scipy cython setuptools wheel 2>&1 | tee -a "$LOG"
fi

echo "BUILD_PINNED_PATCHED_CLASS_AND_CLASSY" | tee -a "$LOG"
PYTHON_BIN="$(command -v python3)"
make -C "$CLASS_ROOT" -j2 PYTHON="$PYTHON_BIN" class 2>&1 | tee -a "$LOG"
make -C "$CLASS_ROOT" -j2 PYTHON="$PYTHON_BIN" classy 2>&1 | tee -a "$LOG"
python3 - <<'PY'
from classy import Class
print("GE19_LW01_PATCHED_CLASSY_IMPORT_OK",Class.__module__)
PY

echo "GE19_LW01_BUILD_SUCCESS_START_ONE_PREREGISTERED_LINEAR_RUN" | tee -a "$LOG"
export CLASS_ROOT
bash ge19/run_local_linear_weyl_native_20261109.sh
