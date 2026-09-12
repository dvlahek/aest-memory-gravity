#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p results

PY=""
if command -v python3 >/dev/null 2>&1; then
  PY="$(command -v python3)"
elif command -v python >/dev/null 2>&1; then
  PY="$(command -v python)"
else
  echo "FULLJ_ISO_TRANSFER_R1_PHASE: python missing" >&2
  exit 2
fi

"$PY" -m py_compile fullj_weyl/isotropic_weyl_transfer_nodes_r1_phase_audit.py

echo "FULLJ_ISO_TRANSFER_R1_PHASE_IMPORT_PASS"

IN="results/fullj_isotropic_weyl_transfer_nodes.json"
JSON="results/fullj_isotropic_weyl_transfer_nodes_r1_phase_audit.json"
CSV="results/fullj_isotropic_weyl_transfer_nodes_r1_phase_audit.csv"
LOG="results/fullj_isotropic_weyl_transfer_nodes_r1_phase_audit.log"
ZIP="results/fullj_isotropic_weyl_transfer_nodes_r1_phase_audit_bundle.zip"
rm -f "$JSON" "$CSV" "$LOG" "$ZIP"

set +e
"$PY" -u fullj_weyl/isotropic_weyl_transfer_nodes_r1_phase_audit.py \
  --input-json "$IN" \
  --json-out "$JSON" \
  --csv-out "$CSV" 2>&1 | tee "$LOG"
code=${PIPESTATUS[0]}
set -e

"$PY" - "$ZIP" "$LOG" "$JSON" "$CSV" <<'PY'
from pathlib import Path
import sys, zipfile
zp=Path(sys.argv[1])
paths=[Path(x) for x in sys.argv[2:]] + [
    Path('results/fullj_isotropic_weyl_transfer_nodes.json'),
    Path('docs/fullj_isotropic_weyl_transfer_nodes_result.md'),
    Path('docs/fullj_isotropic_weyl_transfer_nodes_r1_phase_audit_predata.md'),
    Path('fullj_weyl/isotropic_weyl_transfer_nodes_r1_phase_audit.py'),
    Path('fullj_weyl/run_local_isotropic_weyl_transfer_nodes_r1_phase_audit.sh'),
]
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED) as zf:
    seen=set()
    for p in paths:
        if p.exists() and p not in seen:
            zf.write(p,arcname=str(p)); seen.add(p)
print('FULLJ_ISO_TRANSFER_R1_PHASE_BUNDLE='+str(zp))
PY

echo "FULLJ_ISO_TRANSFER_R1_PHASE_EXIT=$code"
echo "FULLJ_ISO_TRANSFER_R1_PHASE_LOG=$LOG"
echo "FULLJ_ISO_TRANSFER_R1_PHASE_JSON=$JSON"
echo "FULLJ_ISO_TRANSFER_R1_PHASE_CSV=$CSV"
echo "FULLJ_ISO_TRANSFER_R1_PHASE_ZIP=$ZIP"
exit "$code"
