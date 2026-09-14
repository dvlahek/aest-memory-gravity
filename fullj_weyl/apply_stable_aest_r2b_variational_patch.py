#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

MARKER = "FULLJ_STABLE_AEST_R2B_VARIATIONAL_V1"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("class_root")
    args = ap.parse_args()
    root = Path(args.class_root).resolve()
    repo = Path(__file__).resolve().parents[1]
    pc = root / "source" / "perturbations.c"
    if not pc.is_file():
        raise SystemExit("not a CLASS source root")
    text = pc.read_text()
    if MARKER in text:
        print("STABLE_AEST_R2B_VARIATIONAL_PATCH already=1")
        return 0
    if "FULLJ_AEST_STABLE_CHI_RESIDUAL_V1" not in text:
        raise RuntimeError("R2b variational patch requires the certified stable-residual source")

    old_patch = repo / "v019w" / "apply_variational_forcing_patch.py"
    if not old_patch.is_file():
        raise RuntimeError("missing historical v0.19w variational patch")
    subprocess.run([sys.executable, str(old_patch), str(root)], check=True)

    text = pc.read_text()
    old = '''    double Q_aest=pvecback[pba->index_bg_Q_aest];\n    double theta_aest=y[ppw->pv->index_pt_theta_cdm];\n    double alpha_aest=y[ppw->pv->index_pt_alpha_aest];\n    double chi_aest=Q_aest*(a*theta_aest/(k*k)+alpha_aest);\n    double Braw_aest=0.;\n'''
    new = '''    double Q_aest=pvecback[pba->index_bg_Q_aest];\n    /* FULLJ_STABLE_AEST_R2B_VARIATIONAL_V1: trace the eta derivative on\n       the certified residual coordinate, never reconstruct chi by subtraction. */\n    double s_aest=y[ppw->pv->index_pt_s_aest];\n    double chi_aest=Q_aest*s_aest;\n    double Braw_aest=0.;\n'''
    n = text.count(old)
    if n != 1:
        raise RuntimeError(f"stable variational trace replacement expected once, found {n}")
    text = text.replace(old, new, 1)
    pc.write_text(text)

    ptxt = pc.read_text()
    atxt = (root / "source" / "aest_memory.c").read_text()
    checks = {
        "stable_marker": "FULLJ_AEST_STABLE_CHI_RESIDUAL_V1" in ptxt,
        "r2b_marker": MARKER in ptxt,
        "trace_uses_s": "double s_aest=y[ppw->pv->index_pt_s_aest];" in ptxt,
        "trace_chi_Qs": "double chi_aest=Q_aest*s_aest;" in ptxt,
        "old_trace_subtraction_absent": "Q_aest*(a*theta_aest/(k*k)+alpha_aest)" not in ptxt,
        "external_force_hook": "dy[pv->index_pt_E_aest] += aest_tangent_external_force(k,tau);" in ptxt,
        "trace_hook": "aest_tangent_trace_force(k,tau,-0.5*a*Q_aest*Braw_aest/pba->aest_KB);" in ptxt,
        "runtime_force_file": "AEST_TANGENT_FORCE_FILE" in atxt,
        "runtime_lambda": "AEST_TANGENT_LAMBDA" in atxt,
        "physical_memory_closure_preserved": "E_rhs_aest -= 0.5*Q_aest*Bchi_aest" in ptxt,
        "stable_rhs_chi_count": ptxt.count("double chi_aest = Q_aest*s_aest;") == 2,
    }
    if not all(checks.values()):
        raise RuntimeError("R2b stable variational source audit failed: "+repr(checks))
    print("STABLE_AEST_R2B_VARIATIONAL_PATCH_PASS")
    for k, v in checks.items():
        print(f"{k}={v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
