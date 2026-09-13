#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CLASS_SHA="e85808324f51fc694d12e3ed7439552a3c3f9540"
CLASS_ROOT="${CLASS_DENSE_LONGARG_ROOT:-$ROOT/.local/class_corrected_e8580832_densek64_longarg4096}"
PYTARGET="${PYTARGET_DENSE_LONGARG:-$ROOT/.local/classy_corrected_e8580832_densek64_longarg4096}"
ENVFILE="$ROOT/results/fullj_corrected_class_densek64_longarg4096_env.sh"

mkdir -p "$ROOT/.local" "$ROOT/results"

if [[ ! -d "$CLASS_ROOT/.git" ]]; then
  rm -rf "$CLASS_ROOT"
  git clone https://github.com/lesgourg/class_public.git "$CLASS_ROOT"
fi

git -C "$CLASS_ROOT" fetch --quiet origin
git -C "$CLASS_ROOT" reset --hard "$CLASS_SHA"
git -C "$CLASS_ROOT" clean -xfd

# Exact corrected-AeST patch chain already used by the certified dense-k64 runtime.
python "$ROOT/v019/apply_patch_v019.py" "$CLASS_ROOT"
python "$ROOT/v019i/apply_ic_patch.py" "$CLASS_ROOT"
python "$ROOT/v019j/apply_memory_patch.py" "$CLASS_ROOT"
python "$ROOT/v019w/apply_variational_forcing_patch.py" "$CLASS_ROOT"
python "$ROOT/v019y/apply_output_precision_patch.py" "$CLASS_ROOT"
python "$ROOT/v023/apply_source_grid_trace_patch.py" "$CLASS_ROOT"
python "$ROOT/nl1c6d2c6a/apply_aest_state_output_patch.py" "$CLASS_ROOT"

# Previously preregistered C-side history capacity, followed by the R3
# parser/Cython capacity-only repair. No physics source is changed here.
python "$ROOT/fullj_weyl/apply_class_kfile_limit_patch.py" "$CLASS_ROOT"
python "$ROOT/fullj_weyl/apply_direct_class_capacity_patch.py" "$CLASS_ROOT"

grep -Eq '^#define[[:space:]]+_MAX_NUMBER_OF_K_FILES_[[:space:]]+64[[:space:]]*$' \
  "$CLASS_ROOT/include/perturbations.h"
grep -Eq '^#define[[:space:]]+_ARGUMENT_LENGTH_MAX_[[:space:]]+4096([[:space:]]|/|$)' \
  "$CLASS_ROOT/include/parser.h"

echo "FULLJ_DIRECT_CLASS_CAPACITY_HEADER_PASS kfile_limit=64 argument_limit=4096"

rm -rf "$PYTARGET"
mkdir -p "$PYTARGET"
python -m pip install --no-deps --no-build-isolation --target "$PYTARGET" "$CLASS_ROOT"

PYTHONPATH="$PYTARGET${PYTHONPATH:+:$PYTHONPATH}" python - <<'PY'
from classy import Class
import classy
print('FULLJ_DIRECT_CLASS_CAPACITY_CLASSY_IMPORT_PASS')
print('classy_module='+str(classy.__file__))
c=Class(); c.empty()
PY

cat > "$ENVFILE" <<EOF
export NL1C6D2N_CLASS_ROOT="$CLASS_ROOT"
export NL1C6D2N_PYTARGET="$PYTARGET"
export PYTHONPATH="$PYTARGET\${PYTHONPATH:+:\$PYTHONPATH}"
export FULLJ_DENSE_RESIDUAL_R2_CLASS_KFILE_LIMIT="64"
export FULLJ_DIRECT_CLASS_ARGUMENT_LIMIT="4096"
export FULLJ_DIRECT_CLASS_CYTHON_KFILE_LIMIT="64"
EOF

printf 'CLASS_ROOT=%s\nPYTARGET=%s\nENV_FILE=%s\n' "$CLASS_ROOT" "$PYTARGET" "$ENVFILE"
