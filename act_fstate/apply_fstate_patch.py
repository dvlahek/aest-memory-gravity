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
    if not ph.exists() or not pc.exists():
        raise SystemExit("Not a patched CLASS source root")

    # Rename the *single existing* closure slot. This is a coordinate change,
    # not an added degree of freedom.
    h = ph.read_text()
    c = pc.read_text()
    if "index_pt_F_aest" in h or "index_pt_F_aest" in c:
        raise RuntimeError("F state already present before nonredundant replacement")
    if "index_pt_E_aest" not in h or "index_pt_E_aest" not in c:
        raise RuntimeError("expected legacy E state is absent")
    ph.write_text(h.replace("index_pt_E_aest", "index_pt_F_aest"))
    pc.write_text(c.replace("index_pt_E_aest", "index_pt_F_aest"))

    # Header semantics and diagnostic output title now match the evolved state.
    replace_once(
        ph,
        "  int index_pt_F_aest;     /**< AeST scalar closure E=alpha_dot+Psi */\n",
        "  int index_pt_F_aest;     /**< AeST closure F=K_B E+(2-K_B) chi */\n",
        "F header semantics",
    )
    replace_once(
        pc,
        '      class_store_columntitle(ppt->scalar_titles,"E_aest",pba->aest_enabled);\n',
        '      class_store_columntitle(ppt->scalar_titles,"F_aest",pba->aest_enabled);\n',
        "F output title",
    )

    # Einstein stress: use the evolved cancellation-safe F directly.
    replace_once(
        pc,
        "          *(pba->aest_KB*y[ppw->pv->index_pt_F_aest]+(2.-pba->aest_KB)*chi_aest);\n",
        "          *y[ppw->pv->index_pt_F_aest];\n",
        "F Einstein stress",
    )

    # Dynamical closure: reconstruct E algebraically only where alpha' needs it;
    # pressure uses F directly. Keep E_rhs as a passive algebraic audit of the
    # unchanged original equation, but it is no longer an evolved state.
    old_block = (
        "        double E_aest = y[pv->index_pt_F_aest];\n"
        "        double chi_aest = Q_aest*(theta_potential_aest+alpha_aest);\n"
        "        double Pi_aest = cad2_aest*y[pv->index_pt_delta_cdm]\n"
        "          +cad2_aest*k2/(3.*a*a*rho_aest)\n"
        "          *(pba->aest_KB*E_aest+(2.-pba->aest_KB)*chi_aest);\n"
        "        double psi_aest = metric_euler/k2;\n"
        "        double H_aest = pvecback[pba->index_bg_H];\n"
        "        double E_rhs_aest;\n"
    )
    new_block = (
        "        double F_aest = y[pv->index_pt_F_aest];\n"
        "        double chi_aest = Q_aest*(theta_potential_aest+alpha_aest);\n"
        "        double B_aest = 2.-pba->aest_KB;\n"
        "        double E_aest = (F_aest-B_aest*chi_aest)/pba->aest_KB;\n"
        "        double Pi_aest = cad2_aest*y[pv->index_pt_delta_cdm]\n"
        "          +cad2_aest*k2/(3.*a*a*rho_aest)*F_aest;\n"
        "        double psi_aest = metric_euler/k2;\n"
        "        double H_aest = pvecback[pba->index_bg_H];\n"
        "        double E_rhs_aest;\n"
        "        double F_memory_force_aest = 0.;\n"
        "        double F_external_force_aest = 0.;\n"
    )
    replace_once(pc, old_block, new_block, "F dynamical pressure and E reconstruction")

    # Finite memory: KB times the original contribution to E' gives the exact
    # contribution to F'. The bath dynamics themselves are unchanged.
    replace_once(
        pc,
        "          E_rhs_aest -= 0.5*Q_aest*Bchi_aest;\n",
        "          E_rhs_aest -= 0.5*Q_aest*Bchi_aest;\n"
        "          F_memory_force_aest = -0.5*a*Q_aest*Bchi_aest;\n",
        "F finite-memory forcing",
    )

    # Replace the old evolved-E equation by the exact nonredundant F equation.
    # The external variational source was defined as an additive term in E', so
    # it enters F' multiplied by KB.
    old_rhs = (
        "        dy[pv->index_pt_F_aest] = a*E_rhs_aest/pba->aest_KB-a_prime_over_a*E_aest;\n"
        "        dy[pv->index_pt_F_aest] += aest_tangent_external_force(k,tau);\n"
    )
    new_rhs = (
        "        F_external_force_aest = aest_tangent_external_force(k,tau);\n"
        "        dy[pv->index_pt_F_aest] =\n"
        "          a*((B_aest*Q_aest/pba->aest_KB-H_aest)*F_aest\n"
        "             +(KQ_aest-2.*B_aest*Q_aest/pba->aest_KB)*chi_aest)\n"
        "          +F_memory_force_aest+pba->aest_KB*F_external_force_aest;\n"
    )
    replace_once(pc, old_rhs, new_rhs, "nonredundant F evolution")

    ht = ph.read_text()
    ct = pc.read_text()
    checks = {
        "legacy_E_index_absent_header": "index_pt_E_aest" not in ht,
        "legacy_E_index_absent_source": "index_pt_E_aest" not in ct,
        "single_F_index_declaration": ht.count("index_pt_F_aest") == 1,
        "single_F_state_allocation": ct.count("class_define_index(ppv->index_pt_F_aest") == 1,
        "F_output_title": '"F_aest",pba->aest_enabled' in ct,
        "E_reconstructed_algebraically": "E_aest = (F_aest-B_aest*chi_aest)/pba->aest_KB" in ct,
        "stress_uses_F": "*y[ppw->pv->index_pt_F_aest]" in ct,
        "rhs_pressure_uses_F": "cad2_aest*k2/(3.*a*a*rho_aest)*F_aest" in ct,
        "direct_F_equation": "KQ_aest-2.*B_aest*Q_aest/pba->aest_KB" in ct,
        "memory_transformed": "F_memory_force_aest = -0.5*a*Q_aest*Bchi_aest" in ct,
        "external_transformed": "pba->aest_KB*F_external_force_aest" in ct,
        "old_E_state_rhs_absent": "a*E_rhs_aest/pba->aest_KB-a_prime_over_a*E_aest" not in ct,
        "original_E_closure_audit_preserved": "E_rhs_aest -= 0.5*Q_aest*Bchi_aest" in ct,
        "no_redundant_F_state": "class_define_index(ppv->index_pt_E_aest" not in ct,
    }
    if not all(checks.values()):
        raise RuntimeError(f"nonredundant F-state audit failed: {checks}")

    report = {
        "classification": "AEST_NONREDUNDANT_F_STATE_PATCH_READY",
        "definition": "F=KB*E+(2-KB)*chi",
        "evolved_closure_state": "F_only",
        "E_reconstruction": "E=(F-(2-KB)*chi)/KB",
        "state_dimension_increase": 0,
        "new_free_parameters": 0,
        "physics_modified": False,
        "purpose": "remove both high-k cancellation loss and redundant off-constraint F/E mode",
        "checks": checks,
    }
    (repo / "results").mkdir(exist_ok=True)
    (repo / "results" / "act_fstate_apply_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(report, indent=2, sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
