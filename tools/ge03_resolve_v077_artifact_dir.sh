#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-frozen_v077}"

mapfile -t BASES < <(find "$ROOT" -type f -name 'v076_v077_base_trace.dat' -print | sort)

if [ "${#BASES[@]}" -ne 1 ]; then
  echo "GE03 artifact resolution failure: expected exactly one base trace under $ROOT, found ${#BASES[@]}" >&2
  printf '%s\n' "${BASES[@]}" >&2 || true
  exit 41
fi

DIR="$(dirname "${BASES[0]}")"

for tag in 10p0 5p0 2p5 1p25; do
  for sign in plus minus; do
    f="$DIR/v076_v077_${sign}_${tag}_trace.dat"
    test -s "$f" || {
      echo "GE03 artifact resolution failure: missing required trace $f" >&2
      exit 42
    }
  done
done

printf '%s\n' "$DIR"
