#!/usr/bin/env bash
# GE19 experimental full-CLASS eta tangent. A SINGLE frozen 5-pass local campaign.
# Preserves historical CLASS: always patches a SEPARATE isolated checkout.
# Stages: prepare (source checkout+patch+build); run (fixed experiment).
set -euo pipefail

PROJECT="${GE19_PROJECT_ROOT:-$HOME/aest-memory-gravity}"
CLASS="${GE19_TANGENT_CLASS_ROOT:-$HOME/GE19_CLASS_TANGENT_v077}"
OUT="${GE19_TANGENT_OUT_DIR:-$PROJECT/results/ge19_full_class_direct_tangent_20261112}"
PIN="e85808324f51fc694d12e3ed7439552a3c3f9540"
MODE="${1:-prepare}"

cd "$PROJECT"
if [[ "$(git branch --show-current)" != "physics-first-gravitational-elasticity" ]]; then
    echo "GE19_WRONG_PROJECT_BRANCH"; exit 2
fi
source .venv/bin/activate
if [[ "$CLASS" != "$HOME/GE19_CLASS_TANGENT_v077" && "${GE19_ACK_ISOLATED_CLASS:-}" != "yes" ]]; then
    echo "GE19_REFUSE_UNACKNOWLEDGED_CLASS_ROOT: use the default isolated directory"
    echo "or set GE19_ACK_ISOLATED_CLASS=yes after making a separate copy"
    exit 3
fi
case "$MODE" in
  prepare)
    if [[ ! -d "$CLASS" ]]; then
      echo "GE19_CLONE_LOCAL_ISOLATED_CLASS"
      git clone https://github.com/lesgourg/class_public.git "$CLASS"
      git -C "$CLASS" checkout --detach "$PIN"
    fi
    if [[ ! -f "$CLASS/include/common.h" ]]; then
      echo "GE19_CLASS_ROOT_INVALID"; exit 4
    fi
    if [[ ! -e "$CLASS/ge19_tangent_patch_manifest.json" ]]; then
      if [[ "$(git -C "$CLASS" rev-parse HEAD)" != "$PIN" ]]; then
        echo "GE19_CLASS_NOT_AT_PINNED_HEAD";exit 5
      fi
      if ! grep -q 'aest_enabled' "$CLASS/include/background.h"; then
        python3 v019/apply_patch_v019.py "$CLASS"
      fi
      if ! grep -q 'aest_memory_enabled' "$CLASS/include/background.h"; then
        python3 v019j/apply_memory_patch.py "$CLASS"
      fi
      python3 ge19/physics_gate/patch_full_class_tangent_two_pass_20261112.py \
        --class-root "$CLASS" --check-only
      python3 ge19/physics_gate/patch_full_class_tangent_two_pass_20261112.py \
        --class-root "$CLASS"
    fi
    make -C "$CLASS" -j2
    python3 ge19/physics_gate/run_full_class_two_pass_tangent_20261112.py \
      --class-root "$CLASS" \
      --original-ini "$PROJECT/v019/ini/aest_exp.ini" \
      --out-dir "$OUT"
    echo "GE19_FULL_CLASS_PATCH_COMPILE_PREFLIGHT_COMPLETE_NOT_PHYSICS_GO"
    echo "GE19_NEXT: bash ge19/run_local_full_class_direct_tangent_20261112.sh run"
    ;;
  run)
    python3 ge19/physics_gate/run_full_class_two_pass_tangent_20261112.py \
      --class-root "$CLASS" \
      --original-ini "$PROJECT/v019/ini/aest_exp.ini" \
      --out-dir "$OUT" --run \
      2>&1 | tee "$PROJECT/results/ge19_full_class_direct_tangent_20261112_runner.log"
    ;;
  *)
    echo "Usage: bash ge19/run_local_full_class_direct_tangent_20261112.sh prepare|run"
    exit 2
    ;;
esac
