#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

MARKER = "FULLJ_AEST_STABLE_CHI_RESIDUAL_V1"


def replace_once(path: Path, old: str, new: str, label: str) -> None:
    text = path.read_text()
    n = text.count(old)
    if n != 1:
        raise RuntimeError(f"{label}: expected exactly one anchor, found {n} in {path}")
    path.write_text(text.replace(old, new, 1))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("class_root")
    args = ap.parse_args()
    root = Path(args.class_root).resolve()
    ph = root / "include" / "perturbations.h"
    pc = root / "source" / "perturbations.c"
    if not ph.is_file() or not pc.is_file():
        raise SystemExit("not a patched CLASS/AeST source root")
    if MARKER in pc.read_text():
        print("FULLJ_AEST_STABLE_CHI_PATCH already=1")
        return 0

    # One redundant residual state s = a theta/k^2 + alpha.
    replace_once(
        ph,
        '''  int index_pt_E_aest;     /**< AeST scalar closure E=alpha_dot+Psi */\n  int index_pt_mem_q_aest; /**< first normalized finite-bath coordinate */\n''',
        '''  int index_pt_E_aest;     /**< AeST scalar closure E=alpha_dot+Psi */\n  int index_pt_s_aest;     /**< stable residual s=a theta/k^2+alpha */\n  int index_pt_mem_q_aest; /**< first normalized finite-bath coordinate */\n''',
        "stable residual perturbation index",
    )

    replace_once(
        pc,
        '''    class_define_index(ppv->index_pt_alpha_aest,pba->aest_enabled && (ppt->gauge == newtonian),index_pt,1);\n    class_define_index(ppv->index_pt_E_aest,pba->aest_enabled && (ppt->gauge == newtonian),index_pt,1);\n    class_define_index(ppv->index_pt_mem_q_aest,pba->aest_enabled && pba->aest_memory_enabled && (ppt->gauge == newtonian),index_pt,aest_memory_active_count(pba->aest_memory_order));\n''',
        '''    class_define_index(ppv->index_pt_alpha_aest,pba->aest_enabled && (ppt->gauge == newtonian),index_pt,1);\n    class_define_index(ppv->index_pt_E_aest,pba->aest_enabled && (ppt->gauge == newtonian),index_pt,1);\n    class_define_index(ppv->index_pt_s_aest,pba->aest_enabled && (ppt->gauge == newtonian),index_pt,1);\n    class_define_index(ppv->index_pt_mem_q_aest,pba->aest_enabled && pba->aest_memory_enabled && (ppt->gauge == newtonian),index_pt,aest_memory_active_count(pba->aest_memory_order));\n''',
        "stable residual vector allocation",
    )

    replace_once(
        pc,
        '''            ppv->y[ppv->index_pt_alpha_aest] = ppw->pv->y[ppw->pv->index_pt_alpha_aest];\n            ppv->y[ppv->index_pt_E_aest] = ppw->pv->y[ppw->pv->index_pt_E_aest];\n            if (pba->aest_memory_enabled == _TRUE_) {\n''',
        '''            ppv->y[ppv->index_pt_alpha_aest] = ppw->pv->y[ppw->pv->index_pt_alpha_aest];\n            ppv->y[ppv->index_pt_E_aest] = ppw->pv->y[ppw->pv->index_pt_E_aest];\n            ppv->y[ppv->index_pt_s_aest] = ppw->pv->y[ppw->pv->index_pt_s_aest];\n            if (pba->aest_memory_enabled == _TRUE_) {\n''',
        "stable residual approximation-switch copy",
    )

    replace_once(
        pc,
        '''      ppw->pv->y[ppw->pv->index_pt_E_aest] = 0.;\n      if (pba->aest_memory_enabled == _TRUE_) {\n''',
        '''      ppw->pv->y[ppw->pv->index_pt_E_aest] = 0.;\n      /* FULLJ_AEST_STABLE_CHI_RESIDUAL_V1: exact leading-mode residual. */\n      ppw->pv->y[ppw->pv->index_pt_s_aest] = 0.;\n      if (pba->aest_memory_enabled == _TRUE_) {\n''',
        "stable residual initial condition",
    )

    # Metric/source block: use the directly evolved residual.
    replace_once(
        pc,
        '''        double theta_potential = a*y[ppw->pv->index_pt_theta_cdm]/k2;\n        double chi_aest = Q_aest*(theta_potential+y[ppw->pv->index_pt_alpha_aest]);\n''',
        '''        double s_aest = y[ppw->pv->index_pt_s_aest];\n        double chi_aest = Q_aest*s_aest;\n''',
        "stable residual metric-source chi",
    )

    # Perturbation RHS block: same replacement plus exact redundant-state ODE.
    replace_once(
        pc,
        '''        double theta_div_aest = y[pv->index_pt_theta_cdm];\n        double theta_potential_aest = a*theta_div_aest/k2;\n        double alpha_aest = y[pv->index_pt_alpha_aest];\n        double E_aest = y[pv->index_pt_E_aest];\n        double chi_aest = Q_aest*(theta_potential_aest+alpha_aest);\n''',
        '''        double theta_div_aest = y[pv->index_pt_theta_cdm];\n        double alpha_aest = y[pv->index_pt_alpha_aest];\n        double E_aest = y[pv->index_pt_E_aest];\n        double s_aest = y[pv->index_pt_s_aest];\n        double chi_aest = Q_aest*s_aest;\n''',
        "stable residual RHS chi",
    )

    replace_once(
        pc,
        '''        dy[pv->index_pt_alpha_aest] = a*(E_aest-psi_aest);\n\n        E_rhs_aest = KQ_aest*chi_aest\n''',
        '''        dy[pv->index_pt_alpha_aest] = a*(E_aest-psi_aest);\n\n        /* Exact identity for s=a*theta/k^2+alpha.  The metric_euler/k^2\n           contribution from theta' cancels psi analytically. */\n        dy[pv->index_pt_s_aest] =\n          3.*cad2_aest*a_prime_over_a*(s_aest-alpha_aest)\n          +a*(Pi_aest/(1.+w_aest)+E_aest);\n\n        E_rhs_aest = KQ_aest*chi_aest\n''',
        "stable residual ODE",
    )

    # Expose s in the existing read-only state output.
    replace_once(
        pc,
        '''      class_store_columntitle(ppt->scalar_titles,"alpha_aest",pba->aest_enabled);\n      class_store_columntitle(ppt->scalar_titles,"E_aest",pba->aest_enabled);\n''',
        '''      class_store_columntitle(ppt->scalar_titles,"alpha_aest",pba->aest_enabled);\n      class_store_columntitle(ppt->scalar_titles,"E_aest",pba->aest_enabled);\n      class_store_columntitle(ppt->scalar_titles,"s_aest",pba->aest_enabled);\n''',
        "stable residual output title",
    )

    replace_once(
        pc,
        '''    class_store_double(dataptr,\n                       pba->aest_enabled ? y[ppw->pv->index_pt_E_aest] : 0.,\n                       pba->aest_enabled,\n                       storeidx);\n''',
        '''    class_store_double(dataptr,\n                       pba->aest_enabled ? y[ppw->pv->index_pt_E_aest] : 0.,\n                       pba->aest_enabled,\n                       storeidx);\n    class_store_double(dataptr,\n                       pba->aest_enabled ? y[ppw->pv->index_pt_s_aest] : 0.,\n                       pba->aest_enabled,\n                       storeidx);\n''',
        "stable residual output data",
    )

    ptxt = pc.read_text()
    htxt = ph.read_text()
    checks = {
        "marker": MARKER in ptxt,
        "state_index": "index_pt_s_aest" in htxt,
        "state_allocation": "class_define_index(ppv->index_pt_s_aest" in ptxt,
        "state_copy": "ppv->y[ppv->index_pt_s_aest] = ppw->pv->y[ppw->pv->index_pt_s_aest]" in ptxt,
        "state_ic_zero": "ppw->pv->y[ppw->pv->index_pt_s_aest] = 0.;" in ptxt,
        "rhs_identity": "3.*cad2_aest*a_prime_over_a*(s_aest-alpha_aest)" in ptxt,
        "chi_from_s_count": ptxt.count("double chi_aest = Q_aest*s_aest;") == 2,
        "old_rhs_subtraction_absent": "Q_aest*(theta_potential_aest+alpha_aest)" not in ptxt,
        "old_metric_subtraction_absent": "Q_aest*(theta_potential+y[ppw->pv->index_pt_alpha_aest])" not in ptxt,
        "s_output": '"s_aest",pba->aest_enabled' in ptxt,
        "original_alpha_rhs": "dy[pv->index_pt_alpha_aest] = a*(E_aest-psi_aest);" in ptxt,
        "original_E_rhs": "dy[pv->index_pt_E_aest] = a*E_rhs_aest/pba->aest_KB-a_prime_over_a*E_aest;" in ptxt,
    }
    if not all(checks.values()):
        raise RuntimeError("stable chi residual source audit failed: "+repr(checks))
    print("FULLJ_AEST_STABLE_CHI_PATCH_PASS")
    for k,v in checks.items():
        print(f"{k}={v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
