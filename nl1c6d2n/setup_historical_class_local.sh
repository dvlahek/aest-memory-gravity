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

python - "$CLASS_ROOT/source/aest_memory.c" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1])
s=p.read_text()
repl=[
('k=K2*Z0*Z0*(ex-1.);','k=2.*K2*Z0*Z0*(ex-1.);'),
('kq=2.*K2*Z0*Z*ex;','kq=4.*K2*Z0*Z*ex;'),
('kqq=2.*K2*ex*(1.+2.*zz);','kqq=4.*K2*ex*(1.+2.*zz);'),
('double x=kq/(2.*K2*Z0);','double x=kq/(4.*K2*Z0);'),
]
for old,new in repl:
    n=s.count(old)
    if n != 1:
        raise RuntimeError(f'historical normalization anchor {old!r}: expected 1, found {n}')
    s=s.replace(old,new,1)
for old,_ in repl:
    if old in s:
        raise RuntimeError(f'corrected anchor remains after historical restoration: {old}')
p.write_text(s)
print('HISTORICAL_EXP_NORMALIZATION_RESTORED')
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
