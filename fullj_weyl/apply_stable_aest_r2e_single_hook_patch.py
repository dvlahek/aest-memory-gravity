#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

HOOK = "        dy[pv->index_pt_E_aest] += aest_tangent_external_force(k,tau);"
MARKER = "FULLJ_STABLE_AEST_R2E_SINGLE_HOOK_V1"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("class_root")
    args = ap.parse_args()
    root = Path(args.class_root).resolve()
    pc = root / "source" / "perturbations.c"
    am = root / "source" / "aest_memory.c"
    if not pc.is_file() or not am.is_file():
        raise SystemExit("not an AeST CLASS source root")

    text = pc.read_text()
    if "FULLJ_AEST_STABLE_CHI_RESIDUAL_V1" not in text:
        raise RuntimeError("stable residual parent marker missing")
    if "FULLJ_STABLE_AEST_R2B_VARIATIONAL_V1" not in text:
        raise RuntimeError("R2b variational parent marker missing")

    n_before = text.count(HOOK)
    if n_before != 2:
        raise RuntimeError(f"R2e expected exactly two historical external-force hooks, found {n_before}")

    doubled = HOOK + "\n" + HOOK
    if text.count(doubled) != 1:
        raise RuntimeError("R2e expected one consecutive duplicate external-force pair")

    marker_line = "        /* FULLJ_STABLE_AEST_R2E_SINGLE_HOOK_V1: duplicate diagnostic hook removed. */"
    text = text.replace(doubled, marker_line + "\n" + HOOK, 1)
    pc.write_text(text)

    ptxt = pc.read_text()
    atxt = am.read_text()
    hook_count = ptxt.count(HOOK)
    helper_defs = len(re.findall(r"\bdouble\s+aest_tangent_external_force\s*\(", atxt))
    checks = {
        "marker": MARKER in ptxt,
        "external_force_hook_count_one": hook_count == 1,
        "runtime_external_helper_count_one": helper_defs == 1,
        "stable_chi_present": "double chi_aest = Q_aest*s_aest;" in ptxt or "double chi_aest=Q_aest*s_aest;" in ptxt,
        "physical_eta_multiply_once": ptxt.count("Bchi_aest *= pba->aest_eta;") == 1,
        "physical_closure_once": ptxt.count("E_rhs_aest -= 0.5*Q_aest*Bchi_aest;") == 1,
    }
    if not all(checks.values()):
        raise RuntimeError("R2e single-hook source audit failed: "+repr(checks))

    print("STABLE_AEST_R2E_SINGLE_HOOK_PATCH_PASS")
    print(f"historical_hook_count={n_before}")
    print(f"corrected_hook_count={hook_count}")
    for k,v in checks.items():
        print(f"{k}={v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
