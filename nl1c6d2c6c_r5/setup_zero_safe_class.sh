#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CLASS_SHA="e85808324f51fc694d12e3ed7439552a3c3f9540"
CLASS_ROOT="${CLASS_ROOT:-$ROOT/.local/class_c3_r5_zero_safe_e8580832}"
PYTARGET="${PYTARGET:-$ROOT/.local/classy_c3_r5_zero_safe_e8580832}"

mkdir -p "$ROOT/.local" "$ROOT/results"
if [[ ! -d "$CLASS_ROOT/.git" ]]; then
  rm -rf "$CLASS_ROOT"
  git clone https://github.com/lesgourg/class_public.git "$CLASS_ROOT"
fi

git -C "$CLASS_ROOT" fetch --quiet origin
git -C "$CLASS_ROOT" reset --hard "$CLASS_SHA"
git -C "$CLASS_ROOT" clean -xfd

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

grep -q 'pba->aest_memory_enabled && (pba->aest_eta != 0.)' "$CLASS_ROOT/source/perturbations.c"
grep -q 'dy\[pv->index_pt_E_aest\] += aest_tangent_external_force(k,tau)' "$CLASS_ROOT/source/perturbations.c"
grep -q 'E_rhs_aest -= 0.5\*Q_aest\*Bchi_aest' "$CLASS_ROOT/source/perturbations.c"
grep -q 'AEST_TANGENT_ALLOW_K_MISS' "$CLASS_ROOT/source/aest_memory.c"

rm -rf "$PYTARGET"
mkdir -p "$PYTARGET"
python -m pip install --no-deps --no-build-isolation --target "$PYTARGET" "$CLASS_ROOT"

PYTHONPATH="$PYTARGET${PYTHONPATH:+:$PYTHONPATH}" python - <<'PY'
from classy import Class
import classy
print("C3_R5_ZERO_SAFE_CLASSY_IMPORT_PASS")
print("classy_module=", classy.__file__)
c=Class(); c.empty()
PY

cat > "$ROOT/results/c3_r5_class_env.sh" <<EOF
export NL1C6D2N_CLASS_ROOT="$CLASS_ROOT"
export C3_R5_CLASS_ROOT="$CLASS_ROOT"
export C3_R5_PYTARGET="$PYTARGET"
export PYTHONPATH="$PYTARGET\${PYTHONPATH:+:\$PYTHONPATH}"
EOF

printf 'CLASS_ROOT=%s\nPYTARGET=%s\n' "$CLASS_ROOT" "$PYTARGET"
printf 'ENV_FILE=%s\n' "$ROOT/results/c3_r5_class_env.sh"
