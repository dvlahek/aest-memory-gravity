#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CLASS_SHA="e85808324f51fc694d12e3ed7439552a3c3f9540"
CLASS_ROOT="${CLASS_ROOT:-$ROOT/.local/class_fstate_e8580832}"
PYTARGET="${PYTARGET:-$ROOT/.local/classy_fstate_e8580832}"

mkdir -p "$ROOT/.local" "$ROOT/results"
if [[ ! -d "$CLASS_ROOT/.git" ]]; then
  rm -rf "$CLASS_ROOT"
  git clone https://github.com/lesgourg/class_public.git "$CLASS_ROOT"
fi

git -C "$CLASS_ROOT" fetch --quiet origin
git -C "$CLASS_ROOT" reset --hard "$CLASS_SHA"
git -C "$CLASS_ROOT" clean -xfd

# Reconstruct the exact R9 physical patch stack, then perform only the
# nonredundant E->F coordinate replacement. The failed redundant F-balance
# patch is deliberately NOT applied.
python "$ROOT/v019/apply_patch_v019.py" "$CLASS_ROOT"
python "$ROOT/v019i/apply_ic_patch.py" "$CLASS_ROOT"
python "$ROOT/v019j/apply_memory_patch.py" "$CLASS_ROOT"
python "$ROOT/v019u/apply_tau1_bath_patch.py" "$CLASS_ROOT"
sed -i 's/pba->aest_memory_order = 16;/pba->aest_memory_order = 39;/' "$CLASS_ROOT/source/input.c"
python "$ROOT/v019w/apply_variational_forcing_patch.py" "$CLASS_ROOT"
python "$ROOT/v019y/apply_output_precision_patch.py" "$CLASS_ROOT"
python "$ROOT/v023/apply_source_grid_trace_patch.py" "$CLASS_ROOT"
python "$ROOT/nl1c6d2c6a/apply_aest_state_output_patch.py" "$CLASS_ROOT"
python "$ROOT/nl1c6d2c6c_r5/apply_eta0_passive_bath_decoupling.py" "$CLASS_ROOT"
python "$ROOT/nl1c6d2c6c_r5/apply_sparse_k_force_patch.py" "$CLASS_ROOT"
python "$ROOT/act_fstate/apply_fstate_patch.py" "$CLASS_ROOT"

# Literal post-patch audit: one closure state F, no closure state E.
grep -Fq 'index_pt_F_aest' "$CLASS_ROOT/include/perturbations.h"
! grep -Fq 'index_pt_E_aest' "$CLASS_ROOT/include/perturbations.h"
! grep -Fq 'index_pt_E_aest' "$CLASS_ROOT/source/perturbations.c"
grep -Fq 'E_aest = (F_aest-B_aest*chi_aest)/pba->aest_KB' "$CLASS_ROOT/source/perturbations.c"
grep -Fq 'cad2_aest*k2/(3.*a*a*rho_aest)*F_aest' "$CLASS_ROOT/source/perturbations.c"
grep -Fq 'F_memory_force_aest = -0.5*a*Q_aest*Bchi_aest' "$CLASS_ROOT/source/perturbations.c"
grep -Fq 'pba->aest_KB*F_external_force_aest' "$CLASS_ROOT/source/perturbations.c"
echo 'FSTATE_SOURCE_AUDIT_PASS'

make -C "$CLASS_ROOT" -j2 class

test -x "$CLASS_ROOT/class"

rm -rf "$PYTARGET"
mkdir -p "$PYTARGET"
python -m pip install --no-deps --no-build-isolation --target "$PYTARGET" "$CLASS_ROOT" >/dev/null

PYTHONPATH="$PYTARGET${PYTHONPATH:+:$PYTHONPATH}" python - <<'PY'
from classy import Class
import classy
print('FSTATE_CLASSY_IMPORT_PASS')
print('classy_module=', classy.__file__)
c=Class(); c.empty()
PY

cat > "$ROOT/results/act_fstate_class_env.sh" <<EOF
export FSTATE_CLASS_ROOT="$CLASS_ROOT"
export FSTATE_PYTARGET="$PYTARGET"
export PYTHONPATH="$PYTARGET\${PYTHONPATH:+:\$PYTHONPATH}"
EOF

printf 'FSTATE_CLASS_ROOT=%s\nFSTATE_PYTARGET=%s\n' "$CLASS_ROOT" "$PYTARGET"
printf 'FSTATE_ENV=%s\n' "$ROOT/results/act_fstate_class_env.sh"
