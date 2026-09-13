#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ARG_BASE = 1024
ARG_TARGET = 4096
K_TARGET = 64

CYTHON_FIELDS = (
    "double k_output_values[30]",
    "int index_k_output_values[30]",
    "double * scalar_perturbations_data[30]",
    "double * vector_perturbations_data[30]",
    "double * tensor_perturbations_data[30]",
    "int size_scalar_perturbation_data[30]",
    "int size_vector_perturbation_data[30]",
    "int size_tensor_perturbation_data[30]",
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("class_root")
    args = ap.parse_args()
    root = Path(args.class_root).resolve()

    parser_h = root / "include/parser.h"
    perturb_h = root / "include/perturbations.h"
    pxd = root / "python/cclassy.pxd"
    for p in (parser_h, perturb_h, pxd):
        if not p.is_file():
            raise SystemExit(f"missing CLASS file: {p}")

    # The C-side k-output capacity must already be the previously locked 64.
    ptxt = perturb_h.read_text()
    km = re.search(r"^#define\s+_MAX_NUMBER_OF_K_FILES_\s+(\d+)\s*$", ptxt, re.MULTILINE)
    if km is None or int(km.group(1)) != K_TARGET:
        raise SystemExit(f"unexpected C k-output capacity: {None if km is None else km.group(1)}")

    # Expand only the in-memory CLASS argument-value capacity used by classy.
    text = parser_h.read_text()
    pat = re.compile(r"^(#define\s+_ARGUMENT_LENGTH_MAX_\s+)(\d+)(.*)$", re.MULTILINE)
    matches = list(pat.finditer(text))
    if len(matches) != 1:
        raise SystemExit(f"expected one _ARGUMENT_LENGTH_MAX_ definition, found {len(matches)}")
    current = int(matches[0].group(2))
    if current == ARG_BASE:
        text = pat.sub(lambda m: f"{m.group(1)}{ARG_TARGET}{m.group(3)}", text, count=1)
        parser_h.write_text(text)
        print(f"FULLJ_DIRECT_CLASS_CAPACITY_ARG_PATCH {ARG_BASE}->{ARG_TARGET}")
    elif current == ARG_TARGET:
        print(f"FULLJ_DIRECT_CLASS_CAPACITY_ARG_PATCH already={ARG_TARGET}")
    else:
        raise SystemExit(f"unexpected _ARGUMENT_LENGTH_MAX_={current}")

    # Keep Cython's view of all k-output history arrays consistent with C.
    ctext = pxd.read_text()
    changed = 0
    for old in CYTHON_FIELDS:
        new = old.replace("[30]", "[64]")
        n_old = ctext.count(old)
        n_new = ctext.count(new)
        if n_old == 1 and n_new == 0:
            ctext = ctext.replace(old, new, 1)
            changed += 1
        elif n_old == 0 and n_new == 1:
            continue
        else:
            raise SystemExit(f"unexpected Cython capacity anchor state for {old!r}: old={n_old} new={n_new}")
    pxd.write_text(ctext)

    # Exact verification.
    final_parser = parser_h.read_text()
    fm = pat.search(final_parser)
    if fm is None or int(fm.group(2)) != ARG_TARGET:
        raise SystemExit("argument-capacity repair verification failed")
    final_pxd = pxd.read_text()
    for old in CYTHON_FIELDS:
        new = old.replace("[30]", "[64]")
        if old in final_pxd or final_pxd.count(new) != 1:
            raise SystemExit(f"Cython capacity verification failed for {new!r}")

    print(
        "FULLJ_DIRECT_CLASS_CAPACITY_CYTHON_PATCH_PASS "
        f"arrays=8 changed_now={changed} target={K_TARGET}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
