#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

MACRO = "_MAX_NUMBER_OF_K_FILES_"
EXPECTED_BASE = 30
TARGET = 64


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("class_root")
    args = ap.parse_args()

    header = Path(args.class_root) / "include" / "perturbations.h"
    if not header.is_file():
        raise SystemExit(f"missing CLASS header: {header}")

    text = header.read_text()
    pat = re.compile(r"^(#define\s+_MAX_NUMBER_OF_K_FILES_\s+)(\d+)(\s*)$", re.MULTILINE)
    matches = list(pat.finditer(text))
    if len(matches) != 1:
        raise SystemExit(f"expected exactly one {MACRO} definition, found {len(matches)}")

    current = int(matches[0].group(2))
    if current == TARGET:
        print(f"FULLJ_DENSE_RESIDUAL_R2_CLASS_KFILE_PATCH already={TARGET}")
        return 0
    if current != EXPECTED_BASE:
        raise SystemExit(f"unexpected {MACRO}={current}; expected {EXPECTED_BASE} before repair")

    text2 = pat.sub(lambda m: f"{m.group(1)}{TARGET}{m.group(3)}", text, count=1)
    header.write_text(text2)

    verify = pat.search(header.read_text())
    if verify is None or int(verify.group(2)) != TARGET:
        raise SystemExit("CLASS k-output capacity repair did not verify")
    print(f"FULLJ_DENSE_RESIDUAL_R2_CLASS_KFILE_PATCH {EXPECTED_BASE}->{TARGET}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
