#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


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
    repo = Path(__file__).resolve().parents[1]
    ph = root / "include" / "perturbations.h"
    pc = root / "source" / "perturbations.c"

    # 1) Add the redundant cancellation-safe state F = KB E + (2-KB) chi.
    replace_once(
        ph,
        "  int index_pt_E_aest;     /**< AeST scalar closure E=alpha_dot+Psi */\n",
        "  int index_pt_E_aest;     /**< AeST scalar closure E=alpha_dot+Psi */\n"
        "  int index_pt_F_aest;     /**< cancellation-safe F=KB E+(2-KB) chi */\n",
        "F index",
    )

    replace_once(
        pc,
        "    class_define_index(ppv->index_pt_E_aest,pba->aest_enabled && (ppt->gauge == newtonian),index_pt,1);\n",
        "    class_define_index(ppv->index_pt_E_aest,pba->aest_enabled && (ppt->gauge == newtonian),index_pt,1);\n"
        "    class_define_index(ppv->index_pt_F_aest,pba->aest_enabled && (ppt->gauge == newtonian),index_pt,1);\n",
        "F vector allocation",
    )

    # 2) Preserve F across CLASS approximation-vector rebuilds.
    replace_once(
        pc,
        "            ppv->y[ppv->index_pt_alpha_aest] = ppw->pv->y[ppw->pv->index_pt_alpha_aest];\n"
        "            ppv->y[ppv->index_pt_E_aest] = ppw->pv->y[ppw->pv->index_pt_E_aest];\n",
        "            ppv->y[ppv->index_pt_alpha_aest] = ppw->pv->y[ppw->pv->index_pt_alpha_aest];\n"
        "            ppv->y[ppv->index_pt_E_aest] = ppw->pv->y[ppw->pv->index_pt_E_aest];\n"
        "            ppv->y[ppv->index_pt_F_aest] = ppw->pv->y[ppw->pv->index_pt_F_aest];\n",
        "F approximation-switch copy",
    )

    # 3) Regular adiabatic IC: the existing leading mode has E=chi=0, hence F=0.
    replace_once(
        pc,
        "      ppw->pv->y[ppw->pv->index_pt_E_aest] = 0.;\n",
        "      ppw->pv->y[ppw->pv->index_pt_E_aest] = 0.;\n"
        "      ppw->pv->y[ppw->pv->index_pt_F_aest] = 0.;\n",
        "F adiabatic initial condition",
    )

    # 4) Einstein-stress path: use directly evolved F instead of reconstructing
    #    KB*E+(2-KB)*chi in floating point.
    replace_once(
        pc,
        "        Pi_aest = cad2_aest*y[ppw->pv->index_pt_delta_cdm]\n"
        "          +cad2_aest*k2/(3.*a2*rho_dark)\n"
        "          *(pba->aest_KB*y[ppw->pv->index_pt_E_aest]+(2.-pba->aest_KB)*chi_aest);\n",
        "        Pi_aest = cad2_aest*y[ppw->pv->index_pt_delta_cdm]\n"
        "          +cad2_aest*k2/(3.*a2*rho_dark)\n"
        "          *y[ppw->pv->index_pt_F_aest];\n",
        "F Einstein stress",
    )

    # 5) Dynamical RHS: Pi uses F. E is still evolved unchanged.
    replace_once(
        pc,
        "        double E_aest = y[pv->index_pt_E_aest];\n"
        "        double chi_aest = Q_aest*(theta_potential_aest+alpha_aest);\n"
        "        double Pi_aest = cad2_aest*y[pv->index_pt_delta_cdm]\n"
        "          +cad2_aest*k2/(3.*a*a*rho_aest)\n"
        "          *(pba->aest_KB*E_aest+(2.-pba->aest_KB)*chi_aest);\n"
        "        double psi_aest = metric_euler/k2;\n"
        "        double H_aest = pvecback[pba->index_bg_H];\n"
        "        double E_rhs_aest;\n",
        "        double E_aest = y[pv->index_pt_E_aest];\n"
        "        double F_aest = y[pv->index_pt_F_aest];\n"
        "        double chi_aest = Q_aest*(theta_potential_aest+alpha_aest);\n"
        "        double Pi_aest = cad2_aest*y[pv->index_pt_delta_cdm]\n"
        "          +cad2_aest*k2/(3.*a*a*rho_aest)*F_aest;\n"
        "        double psi_aest = metric_euler/k2;\n"
        "        double H_aest = pvecback[pba->index_bg_H];\n"
        "        double E_rhs_aest;\n"
        "        double F_memory_force_aest = 0.;\n"
        "        double F_external_force_aest = 0.;\n",
        "F dynamical pressure",
    )

    # Finite-memory contribution to F' is KB times its contribution to E'.
    replace_once(
        pc,
        "          E_rhs_aest -= 0.5*Q_aest*Bchi_aest;\n",
        "          E_rhs_aest -= 0.5*Q_aest*Bchi_aest;\n"
        "          F_memory_force_aest = -0.5*a*Q_aest*Bchi_aest;\n",
        "F finite-memory forcing",
    )

    # External variational forcing is likewise inherited exactly as KB*f_ext.
    # The analytic F equation follows from the unchanged theta, alpha and E
    # equations plus Q'/Q=-3(aH)c_ad^2. The large Pi terms cancel before
    # floating-point evaluation.
    replace_once(
        pc,
        "        dy[pv->index_pt_E_aest] = a*E_rhs_aest/pba->aest_KB-a_prime_over_a*E_aest;\n"
        "        dy[pv->index_pt_E_aest] += aest_tangent_external_force(k,tau);\n",
        "        dy[pv->index_pt_E_aest] = a*E_rhs_aest/pba->aest_KB-a_prime_over_a*E_aest;\n"
        "        F_external_force_aest = aest_tangent_external_force(k,tau);\n"
        "        dy[pv->index_pt_E_aest] += F_external_force_aest;\n"
        "        {\n"
        "          double B_aest = 2.-pba->aest_KB;\n"
        "          dy[pv->index_pt_F_aest] =\n"
        "            a*((B_aest*Q_aest/pba->aest_KB-H_aest)*F_aest\n"
        "               +(KQ_aest-2.*B_aest*Q_aest/pba->aest_KB)*chi_aest)\n"
        "            +F_memory_force_aest+pba->aest_KB*F_external_force_aest;\n"
        "        }\n",
        "direct F evolution",
    )

    text = pc.read_text()
    checks = {
        "F_index_allocated": "index_pt_F_aest" in text,
        "stress_uses_F": "*y[ppw->pv->index_pt_F_aest]" in text,
        "rhs_uses_F": "cad2_aest*k2/(3.*a*a*rho_aest)*F_aest" in text,
        "direct_F_equation": "KQ_aest-2.*B_aest*Q_aest/pba->aest_KB" in text,
        "memory_inherited": "F_memory_force_aest = -0.5*a*Q_aest*Bchi_aest" in text,
        "external_inherited": "pba->aest_KB*F_external_force_aest" in text,
        "E_equation_preserved": "dy[pv->index_pt_E_aest] = a*E_rhs_aest/pba->aest_KB-a_prime_over_a*E_aest" in text,
        "memory_closure_preserved": "E_rhs_aest -= 0.5*Q_aest*Bchi_aest" in text,
    }
    if not all(checks.values()):
        raise RuntimeError(f"F-balance source audit failed: {checks}")

    report = {
        "classification": "AEST_F_BALANCE_PRODUCTION_PATCH_READY",
        "physics_modified": False,
        "new_free_parameters": 0,
        "definition": "F=KB*E+(2-KB)*chi",
        "purpose": "avoid high-k cancellation loss before k^2 pressure amplification",
        "checks": checks,
    }
    (repo / "results").mkdir(exist_ok=True)
    (repo / "results" / "act_fbalance_apply_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(report, indent=2, sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
