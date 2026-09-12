#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CLASS_SHA="e85808324f51fc694d12e3ed7439552a3c3f9540"
CLASS_ROOT="${CLASS_DENSE_ROOT:-$ROOT/.local/class_corrected_e8580832_densek64}"
PYTARGET="${PYTARGET_DENSE:-$ROOT/.local/classy_corrected_e8580832_densek64}"
ENVFILE="$ROOT/results/nl1c6d2n_corrected_class_densek64_env.sh"

mkdir -p "$ROOT/.local" "$ROOT/results"

if [[ ! -d "$CLASS_ROOT/.git" ]]; then
  rm -rf "$CLASS_ROOT"
  git clone https://github.com/lesgourg/class_public.git "$CLASS_ROOT"
fi

git -C "$CLASS_ROOT" fetch --quiet origin
git -C "$CLASS_ROOT" reset --hard "$CLASS_SHA"
git -C "$CLASS_ROOT" clean -xfd

# Identical corrected-AeST patch chain used by the certified D2C6 CLASS setup.
python "$ROOT/v019/apply_patch_v019.py" "$CLASS_ROOT"
python "$ROOT/v019i/apply_ic_patch.py" "$CLASS_ROOT"
python "$ROOT/v019j/apply_memory_patch.py" "$CLASS_ROOT"
python "$ROOT/v019w/apply_variational_forcing_patch.py" "$CLASS_ROOT"
python "$ROOT/v019y/apply_output_precision_patch.py" "$CLASS_ROOT"
python "$ROOT/v023/apply_source_grid_trace_patch.py" "$CLASS_ROOT"
python "$ROOT/nl1c6d2c6a/apply_aest_state_output_patch.py" "$CLASS_ROOT"

# Technical capacity repair only: K3 requests 41 perturbation-output histories.
python "$ROOT/fullj_weyl/apply_class_kfile_limit_patch.py" "$CLASS_ROOT"
grep -Eq '^#define[[:space:]]+_MAX_NUMBER_OF_K_FILES_[[:space:]]+64[[:space:]]*$' \
  "$CLASS_ROOT/include/perturbations.h"

echo "FULLJ_DENSE_RESIDUAL_R2_CLASS_KFILE_HEADER_PASS value=64"

rm -rf "$PYTARGET"
mkdir -p "$PYTARGET"
python -m pip install --no-deps --no-build-isolation --target "$PYTARGET" "$CLASS_ROOT"

PYTHONPATH="$PYTARGET${PYTHONPATH:+:$PYTHONPATH}" python - <<'PY'
from classy import Class
import classy
print('FULLJ_DENSE_RESIDUAL_R2_DENSE_CLASSY_IMPORT_PASS')
print('classy_module='+str(classy.__file__))
c=Class(); c.empty()
PY

cat > "$ENVFILE" <<EOF
export NL1C6D2N_CLASS_ROOT="$CLASS_ROOT"
export NL1C6D2N_PYTARGET="$PYTARGET"
export PYTHONPATH="$PYTARGET\${PYTHONPATH:+:\$PYTHONPATH}"
export FULLJ_DENSE_RESIDUAL_R2_CLASS_KFILE_LIMIT="64"
EOF

printf 'CLASS_ROOT=%s\nPYTARGET=%s\nENV_FILE=%s\n' "$CLASS_ROOT" "$PYTARGET" "$ENVFILE"
