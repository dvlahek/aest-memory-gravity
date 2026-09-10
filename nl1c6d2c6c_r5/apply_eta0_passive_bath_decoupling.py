#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def replace_once(path: Path, old: str, new: str, label: str) -> None:
    text = path.read_text()
    n = text.count(old)
    if n != 1:
        raise RuntimeError(f"{label}: expected exactly one anchor, found {n}")
    path.write_text(text.replace(old, new, 1))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("class_root")
    args = ap.parse_args()
    root = Path(args.class_root).resolve()
    repo = Path(__file__).resolve().parents[1]
    pc = root / "source" / "perturbations.c"

    # A passive eta=0 bath must not enlarge the NDF15 system.  The finite-eta
    # path is unchanged: bath states are allocated exactly as before for eta>0.
    replace_once(
        pc,
        """    class_define_index(ppv->index_pt_mem_q_aest,pba->aest_enabled && pba->aest_memory_enabled && (ppt->gauge == newtonian),index_pt,aest_memory_active_count(pba->aest_memory_order));\n    class_define_index(ppv->index_pt_mem_p_aest,pba->aest_enabled && pba->aest_memory_enabled && (ppt->gauge == newtonian),index_pt,aest_memory_active_count(pba->aest_memory_order));\n""",
        """    class_define_index(ppv->index_pt_mem_q_aest,pba->aest_enabled && pba->aest_memory_enabled && (pba->aest_eta != 0.) && (ppt->gauge == newtonian),index_pt,aest_memory_active_count(pba->aest_memory_order));\n    class_define_index(ppv->index_pt_mem_p_aest,pba->aest_enabled && pba->aest_memory_enabled && (pba->aest_eta != 0.) && (ppt->gauge == newtonian),index_pt,aest_memory_active_count(pba->aest_memory_order));\n""",
        "eta0 bath allocation",
    )

    replace_once(
        pc,
        """            if (pba->aest_memory_enabled == _TRUE_) {\n              int nm=aest_memory_active_count(pba->aest_memory_order);\n""",
        """            if ((pba->aest_memory_enabled == _TRUE_) && (pba->aest_eta != 0.)) {\n              int nm=aest_memory_active_count(pba->aest_memory_order);\n""",
        "eta0 approximation-switch bath copy",
    )

    replace_once(
        pc,
        """      if (pba->aest_memory_enabled == _TRUE_) {\n        int jm,nm=aest_memory_active_count(pba->aest_memory_order);\n""",
        """      if ((pba->aest_memory_enabled == _TRUE_) && (pba->aest_eta != 0.)) {\n        int jm,nm=aest_memory_active_count(pba->aest_memory_order);\n""",
        "eta0 bath initial conditions",
    )

    replace_once(
        pc,
        """        if (pba->aest_memory_enabled == _TRUE_) {\n          int jm,nm=aest_memory_active_count(pba->aest_memory_order);\n          double Bchi_aest=0.;\n""",
        """        if ((pba->aest_memory_enabled == _TRUE_) && (pba->aest_eta != 0.)) {\n          int jm,nm=aest_memory_active_count(pba->aest_memory_order);\n          double Bchi_aest=0.;\n""",
        "eta0 bath dynamics and closure",
    )

    # v0.19w traces live q_j only when those states exist.  At eta=0 the R5
    # bath is reconstructed outside CLASS from the memory-off core trajectory.
    replace_once(
        pc,
        """  if ((pba->aest_enabled == _TRUE_) &&\n      (pba->aest_memory_enabled == _TRUE_) &&\n      (index_md == ppt->index_md_scalars)) {\n""",
        """  if ((pba->aest_enabled == _TRUE_) &&\n      (pba->aest_memory_enabled == _TRUE_) &&\n      (pba->aest_eta != 0.) &&\n      (index_md == ppt->index_md_scalars)) {\n""",
        "eta0 live-bath tangent trace",
    )

    text = pc.read_text()
    checks = {
        "eta0_q_allocation_disabled": "pba->aest_memory_enabled && (pba->aest_eta != 0.) && (ppt->gauge == newtonian)" in text,
        "eta0_switch_copy_disabled": "if ((pba->aest_memory_enabled == _TRUE_) && (pba->aest_eta != 0.))" in text,
        "eta0_live_bath_trace_disabled": "(pba->aest_eta != 0.) &&\n      (index_md == ppt->index_md_scalars)" in text,
        "finite_eta_closure_preserved": "E_rhs_aest -= 0.5*Q_aest*Bchi_aest" in text,
        "external_tangent_force_preserved": "dy[pv->index_pt_E_aest] += aest_tangent_external_force(k,tau)" in text,
        "core_chi_trace_preserved": "aest_offline_trace_state(k,tau,a,pvecback[pba->index_bg_H],pba->H0" in text,
    }
    if not all(checks.values()):
        raise RuntimeError(f"R5 eta0 decoupling audit failed: {checks}")

    report = {
        "classification": "C3_R5_ETA0_PASSIVE_BATH_DECOUPLING_PATCH_READY",
        "physics_modified_for_positive_eta": False,
        "eta0_passive_states_in_class": False,
        "checks": checks,
    }
    (repo / "results").mkdir(exist_ok=True)
    (repo / "results" / "c3_r5_eta0_decoupling_patch.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(report, indent=2, sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
