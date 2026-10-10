#!/usr/bin/env bash
set -euo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
[[ "$(git symbolic-ref --quiet --short HEAD)" == "physics-first-gravitational-elasticity" ]] || { echo GE19_D25_WRONG_BRANCH; exit 4; }
if [[ -z "${VIRTUAL_ENV:-}" ]];then
  [[ -f "$ROOT/.venv/bin/activate" ]] || { echo GE19_D25_VENV_MISSING; exit 5; }
  source "$ROOT/.venv/bin/activate"
fi
export PYTHONPATH="$ROOT" PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS="${OPENBLAS_NUM_THREADS:-1}"
python3 -B - "$ROOT" <<'PY'
import hashlib,json,sys
from pathlib import Path
r=Path(sys.argv[1]);m=json.loads((r/'D25_SOURCE_MANIFEST.json').read_text())
assert m['classification']=='GE19_D25_FROZEN_THREE_CASE_H3_SHIFT_TRANSPORT_DECOMPOSITION_PACKAGE'
for rel,h in m['files_sha256'].items():
 p=r/rel
 assert p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==h,f'D25 source SHA mismatch: {p}'
print('GE19_D25_SOURCE_MANIFEST_AND_FROZEN_SCOPE_SHA_PASS',flush=True)
PY
python3 -B "$ROOT/ge19/h4f3d25_static_shift_transport_test.py"
mkdir -p "$ROOT/results"
PREFIX="$ROOT/results/ge19_h4f3d25_H3_first_step_shift_transport_decomposition"
J="${PREFIX}.json";N="${PREFIX}.npz";FULL="${PREFIX}_FULL.log"
for f in "$J" "$N" "$FULL";do
  [[ ! -e "$f" ]] || { echo "GE19_D25_NO_OVERWRITE $f";exit 7; }
done
TMP="$(mktemp -d)";trap 'rm -rf -- "$TMP"' EXIT
mkdir -p "$TMP/results"
cd "$TMP"
echo GE19_D25_THREE_CASE_H3_SHIFT_TRANSPORT_BEGIN
set +e
python3 -B -m ge19.h4f3d25_H3_first_step_shift_transport_decomposition \
  --results-dir "$ROOT/results" --json-out "$J" --npz-out "$N" \
  2>&1 | tee "$FULL"
rc="${PIPESTATUS[0]}"
set -e
for f in "$J" "$N" "$FULL";do
 if [[ -s "$f" ]];then sha256sum "$f";wc -c "$f";fi
done
if [[ "$rc" -ne 0 || ! -s "$J" || ! -s "$N" ]];then
 echo GE19_D25_DIAGNOSTIC_EXECUTION_FAIL
 [[ "$rc" -eq 0 ]] && exit 1 || exit "$rc"
fi
python3 -B - "$J" <<'PYCHECK'
import json,sys
r=json.load(open(sys.argv[1]));assert r['D22A_SCIENCE_FAIL_immutable'] is True
assert r['Z11_certified'] is False and r['Z20_certified'] is False
assert r['Z21_certified'] is False and r['full_H4_Ward_certified'] is False
assert r['q20_B20_recomputed'] is False and r['lensing_licensed'] is False
assert len(r['cases'])==3
print('GE19_D25_RESULT',r['classification'])
PYCHECK
