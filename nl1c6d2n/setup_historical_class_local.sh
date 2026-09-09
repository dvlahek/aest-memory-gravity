#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CLASS_SHA="e85808324f51fc694d12e3ed7439552a3c3f9540"
CLASS_ROOT="${HIST_CLASS_ROOT:-$ROOT/.local/class_historical_exp_e8580832}"
PYTARGET="${HIST_PYTARGET:-$ROOT/.local/classy_historical_exp_e8580832}"

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
python "$ROOT/v019w/apply_variational_forcing_patch.py" "$CLASS_ROOT"
python "$ROOT/v019y/apply_output_precision_patch.py" "$CLASS_ROOT"
python "$ROOT/v023/apply_source_grid_trace_patch.py" "$CLASS_ROOT"

# Restore only the Exp branch to the historical factor-2 normalization.
# Use whole-block anchors so the identical Cosh inverse denominator is never touched.
python - "$CLASS_ROOT/source/aest_memory.c" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1])
s=p.read_text()

old_exp='''  else if (model==_AEST_MODEL_EXP_) {
    double zz=Z*Z;
    double ex=exp(zz);
    if (!isfinite(ex)) return 3;
    k=K2*Z0*Z0*(ex-1.);
    kq=2.*K2*Z0*Z*ex;
    kqq=2.*K2*ex*(1.+2.*zz);
  }
'''
new_exp='''  else if (model==_AEST_MODEL_EXP_) {
    double zz=Z*Z;
    double ex=exp(zz);
    if (!isfinite(ex)) return 3;
    k=2.*K2*Z0*Z0*(ex-1.);
    kq=4.*K2*Z0*Z*ex;
    kqq=4.*K2*ex*(1.+2.*zz);
  }
'''
old_inv='''  else if (model==_AEST_MODEL_EXP_) {
    double x=kq/(2.*K2*Z0);
    if (aest_exp_Z_from_x(x,&Z)) return 3;
  }
'''
new_inv='''  else if (model==_AEST_MODEL_EXP_) {
    double x=kq/(4.*K2*Z0);
    if (aest_exp_Z_from_x(x,&Z)) return 3;
  }
'''

for label, old, new in (
    ('Exp evaluator', old_exp, new_exp),
    ('Exp inverse', old_inv, new_inv),
):
    n=s.count(old)
    if n != 1:
        raise RuntimeError(f'historical {label} block: expected exactly 1 corrected block, found {n}')
    s=s.replace(old,new,1)

checks={
    'historical_K':'k=2.*K2*Z0*Z0*(ex-1.);' in s,
    'historical_KQ':'kq=4.*K2*Z0*Z*ex;' in s,
    'historical_KQQ':'kqq=4.*K2*ex*(1.+2.*zz);' in s,
    'historical_inverse':'else if (model==_AEST_MODEL_EXP_) {\n    double x=kq/(4.*K2*Z0);' in s,
    'cosh_inverse_preserved':'if (model==_AEST_MODEL_COSH_) {\n    double x=kq/(2.*K2*Z0);' in s,
}
if not all(checks.values()):
    raise RuntimeError('historical Exp restoration source audit failed: '+repr(checks))

p.write_text(s)
print('HISTORICAL_EXP_NORMALIZATION_RESTORED', checks)
PY

rm -rf "$PYTARGET"
mkdir -p "$PYTARGET"
python -m pip install --no-deps --no-build-isolation --target "$PYTARGET" "$CLASS_ROOT"

PYTHONPATH="$PYTARGET${PYTHONPATH:+:$PYTHONPATH}" python - <<'PY'
from classy import Class
import classy
print('HISTORICAL_CLASSY_IMPORT_PASS')
print('classy_module=', classy.__file__)
c=Class(); c.empty()
PY

cat > "$ROOT/results/nl1c6d2n_historical_class_env.sh" <<EOF
export NL1C6D2N_HIST_CLASS_ROOT="$CLASS_ROOT"
export NL1C6D2N_HIST_PYTARGET="$PYTARGET"
export PYTHONPATH="$PYTARGET\${PYTHONPATH:+:\$PYTHONPATH}"
EOF

printf 'HIST_CLASS_ROOT=%s\nHIST_PYTARGET=%s\n' "$CLASS_ROOT" "$PYTARGET"
printf 'ENV_FILE=%s\n' "$ROOT/results/nl1c6d2n_historical_class_env.sh"
