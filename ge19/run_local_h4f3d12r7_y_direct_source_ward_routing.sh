#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

source .venv/bin/activate
export PYTHONUNBUFFERED=1
export PYTHONPATH="$PWD${PYTHONPATH:+:$PYTHONPATH}"

exec /usr/bin/time -v \
    python3 -m ge19.h4f3d12r7_y_direct_source_ward_routing_structural
