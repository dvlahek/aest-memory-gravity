#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

REPAIR03_LOCK='d6b0b8341cad6ecf12d52a50e9f6b68cbb821d0b'
COBAYA_COMMIT='b76b6fed2a6c8c5594c6f92d5058bef10079746a'
git merge-base --is-ancestor "$REPAIR03_LOCK" HEAD

BASE_PY="$(command -v python3 || command -v python)"
[[ -n "$BASE_PY" ]] || { echo 'R9B_REPAIR03: python missing' >&2; exit 2; }
VENV="$ROOT/.local/fullj_weyl_bridge_venv"
if [[ ! -x "$VENV/bin/python" ]]; then "$BASE_PY" -m venv "$VENV"; fi
export PATH="$VENV/bin:$PATH"

python -m pip install -q "git+https://github.com/CobayaSampler/cobaya.git@$COBAYA_COMMIT"
python - <<'PY'
import cobaya
from cobaya.likelihood import Likelihood
print('STABLE_AEST_DESI_DR1_R9B_REPAIR03_COBAYA_IMPORT_PASS')
PY

exec bash fullj_weyl/run_local_stable_aest_desi_dr1_r9b_shapefit_projection_repair02.sh
