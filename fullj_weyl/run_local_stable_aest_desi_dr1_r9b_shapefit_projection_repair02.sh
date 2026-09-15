#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

REPAIR02_LOCK='94cc4ddc2fe06b7d5b951e7dea6f63698177f16c'
git merge-base --is-ancestor "$REPAIR02_LOCK" HEAD

SRC='fullj_weyl/run_local_stable_aest_desi_dr1_r9b_shapefit_projection.sh'
TMP='.local/run_local_stable_aest_desi_dr1_r9b_shapefit_projection_repair02_exec.sh'
mkdir -p .local

python3 - "$SRC" "$TMP" <<'PY'
from pathlib import Path
import sys
src=Path(sys.argv[1]); dst=Path(sys.argv[2])
s=src.read_text()
marker='python "$DESI_REPO/dr1/cobaya/download.py" --data-dir "$DESI_DATA"\n'
if s.count(marker) != 1:
    raise SystemExit(f'R9B_REPAIR02_MARKER_COUNT_FAIL count={s.count(marker)}')
patch=r'''python - "$DESI_DATA" <<'PY_R9B_REPAIR02'
from pathlib import Path
import sys
root=Path(sys.argv[1])
renamed=[]
for p in sorted(root.glob('*%2B*')):
    q=p.with_name(p.name.replace('%2B','+'))
    if q.exists():
        raise SystemExit(f'R9B_REPAIR02_DEST_EXISTS src={p.name} dst={q.name}')
    p.rename(q)
    renamed.append((p.name,q.name))
print(f'STABLE_AEST_DESI_DR1_R9B_REPAIR02_FILENAME_CANONICALIZATION_PASS count={len(renamed)}')
for a,b in renamed:
    print(f'R9B_REPAIR02_RENAME {a} -> {b}')
if len(renamed) < 6:
    raise SystemExit(f'R9B_REPAIR02_TOO_FEW_RENAMES count={len(renamed)}')
PY_R9B_REPAIR02
'''
s=s.replace(marker, marker+patch, 1)
dst.write_text(s)
print('STABLE_AEST_DESI_DR1_R9B_REPAIR02_TEMP_RUNNER_PASS')
PY

chmod +x "$TMP"
exec bash "$TMP"
