#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p .local results

REPAIR01_PREFIT_LOCK='3a933f706f390bb49d4f70c6751038dafef45fbb'
REPAIR02_PREFIT_LOCK='9d246fd780d3bc62a4c9cda054946c9bd121cbd7'
BASE_IMPLEMENTATION_LOCK='c10d18549ff1ab2ca6f948f7786dfdbc5225ab73'
BASE_RUNNER_LOCK='420592d970acb7684aa55ad017862394c18d62a7'

git merge-base --is-ancestor "$REPAIR01_PREFIT_LOCK" HEAD
git merge-base --is-ancestor "$REPAIR02_PREFIT_LOCK" HEAD
git merge-base --is-ancestor "$BASE_IMPLEMENTATION_LOCK" HEAD
git merge-base --is-ancestor "$BASE_RUNNER_LOCK" HEAD

TARGET='fullj_weyl/stable_aest_desi_dr1_r9b2_direct_velocity_shapefit_projection.py'
BACKUP='.local/r9b2_direct_velocity_repair01_source_backup.py'
cp "$TARGET" "$BACKUP"
restore_source() {
  cp "$BACKUP" "$TARGET" 2>/dev/null || true
  rm -f "$BACKUP" 2>/dev/null || true
}
trap restore_source EXIT INT TERM

if [[ -x "$ROOT/.local/fullj_weyl_bridge_venv/bin/python" ]]; then
  PATCH_PY="$ROOT/.local/fullj_weyl_bridge_venv/bin/python"
else
  PATCH_PY="$(command -v python3 || command -v python || true)"
fi
[[ -n "$PATCH_PY" ]] || { echo 'R9B2_REPAIR02: no Python interpreter available for deterministic pre-run patch' >&2; exit 2; }
echo "STABLE_AEST_DESI_DR1_R9B2_REPAIR02_PATCH_PY=$PATCH_PY"

"$PATCH_PY" - "$TARGET" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1])
s=p.read_text()
old='''    old_sigma8 = float(c.sigma(8.0, float(z), h_units=True))\n    old_fsigma8 = float(c.effective_f_sigma8(float(z), z_step=0.1))\n    old_proxy = old_fsigma8/old_sigma8\n'''
new='''    try:\n        old_sigma8 = float(c.sigma(8.0, float(z), h_units=True))\n        old_fsigma8 = float(c.effective_f_sigma8(float(z), z_step=0.1))\n        old_proxy = old_fsigma8/old_sigma8\n    except Exception:\n        old_proxy = float("nan")\n'''
if s.count(old) != 1:
    raise SystemExit(f'R9B2_REPAIR01_MARKER_COUNT_FAIL count={s.count(old)}')
s=s.replace(old,new,1)
p.write_text(s)
print('STABLE_AEST_DESI_DR1_R9B2_REPAIR01_LEGACY_PROXY_NON_GATING_PASS')
PY

"$PATCH_PY" -m py_compile "$TARGET"

echo 'STABLE_AEST_DESI_DR1_R9B2_REPAIR02_LAUNCHER_PASS'

set +e
bash fullj_weyl/run_local_stable_aest_desi_dr1_r9b2_direct_velocity_shapefit_projection.sh
code=$?
set -e

echo "STABLE_AEST_DESI_DR1_R9B2_REPAIR01_EXIT=$code"
exit "$code"
