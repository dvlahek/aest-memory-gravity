#!/usr/bin/env python3
from pathlib import Path
import argparse
import json


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
    pc = root / "source" / "perturbations.c"
    ac = root / "source" / "aest_memory.c"
    if not pc.exists() or not ac.exists():
        raise SystemExit("Not a patched CLASS source root")

    # Expose the exact eta=0 inhomogeneous forcing computed from the already
    # evolved CLASS bath state on each dense k_output perturbation history.
    replace_once(
        pc,
        '      class_store_columntitle(ppt->scalar_titles,"E_aest",pba->aest_enabled);\n',
        '      class_store_columntitle(ppt->scalar_titles,"E_aest",pba->aest_enabled);\n'
        '      class_store_columntitle(ppt->scalar_titles,"eta0_tangent_force_aest",pba->aest_enabled && pba->aest_memory_enabled);\n',
        "R4 dense force output title",
    )

    old_data = '''    class_store_double(dataptr,\n                       pba->aest_enabled ? y[ppw->pv->index_pt_E_aest] : 0.,\n                       pba->aest_enabled,\n                       storeidx);\n'''
    new_data = old_data + '''    /* C3-R4 instrumentation only. Physical eta remains zero in Stage A. */\n    {\n      double eta0_tangent_force_aest = 0.;\n      if ((pba->aest_enabled == _TRUE_) && (pba->aest_memory_enabled == _TRUE_)) {\n        int jm,nm=aest_memory_active_count(pba->aest_memory_order);\n        double a_r4=ppw->pvecback[pba->index_bg_a];\n        double Q_r4=ppw->pvecback[pba->index_bg_Q_aest];\n        double alpha_r4=y[ppw->pv->index_pt_alpha_aest];\n        double chi_r4=Q_r4*(a_r4*theta_cdm/(k*k)+alpha_r4);\n        double Braw_r4=0.;\n        for (jm=0;jm<nm;jm++) {\n          double rj=aest_memory_node_order(pba->aest_memory_order,jm);\n          double wj=aest_memory_weight_order(pba->aest_memory_order,jm);\n          double omega_j=rj*pba->H0/pba->aest_tau_H0;\n          double qj=y[ppw->pv->index_pt_mem_q_aest+jm];\n          Braw_r4 += wj*chi_r4-sqrt(wj)*(a_r4*omega_j/k)*qj;\n        }\n        eta0_tangent_force_aest = -0.5*a_r4*Q_r4*Braw_r4/pba->aest_KB;\n      }\n      class_store_double(dataptr,\n                         eta0_tangent_force_aest,\n                         pba->aest_enabled && pba->aest_memory_enabled,\n                         storeidx);\n    }\n'''
    replace_once(pc, old_data, new_data, "R4 dense force output data")

    # Reference-only sparse-k forcing: exact six frozen k modes are forced;
    # unrelated transfer-grid k values receive zero instead of aborting.
    old_miss = '''  if (rel > 2.e-10) {\n    fprintf(stderr,"AEST_TANGENT_FORCE_K_MISS query=%.17g nearest=%.17g rel=%.3e\\n",\n            k,_aest_tf_cache_k,rel);\n    return 0;\n  }\n'''
    new_miss = '''  if (rel > 2.e-10) {\n    const char *allow_sparse = getenv("AEST_TANGENT_ALLOW_K_MISS");\n    if (allow_sparse != NULL && strcmp(allow_sparse,"1") == 0) return 0;\n    fprintf(stderr,"AEST_TANGENT_FORCE_K_MISS query=%.17g nearest=%.17g rel=%.3e\\n",\n            k,_aest_tf_cache_k,rel);\n    return 0;\n  }\n'''
    replace_once(ac, old_miss, new_miss, "R4 sparse-k miss suppression")

    replace_once(
        ac,
        '  if (!_aest_tangent_select_k(k)) exit(94);\n',
        '  if (!_aest_tangent_select_k(k)) {\n'
        '    const char *allow_sparse = getenv("AEST_TANGENT_ALLOW_K_MISS");\n'
        '    if (allow_sparse != NULL && strcmp(allow_sparse,"1") == 0) return 0.;\n'
        '    exit(94);\n'
        '  }\n',
        "R4 sparse-k zero forcing",
    )

    ptxt = pc.read_text()
    atxt = ac.read_text()
    checks = {
        "dense_force_title": '"eta0_tangent_force_aest",pba->aest_enabled && pba->aest_memory_enabled' in ptxt,
        "dense_force_from_live_q": 'Braw_r4 += wj*chi_r4-sqrt(wj)*(a_r4*omega_j/k)*qj' in ptxt,
        "dense_force_formula": 'eta0_tangent_force_aest = -0.5*a_r4*Q_r4*Braw_r4/pba->aest_KB' in ptxt,
        "physical_eta_closure_unchanged": 'Bchi_aest *= pba->aest_eta' in ptxt,
        "sparse_k_env": 'AEST_TANGENT_ALLOW_K_MISS' in atxt,
        "exact_interpolation_unchanged": 'return _aest_tf_lambda*(f0 + x*(f1-f0));' in atxt,
    }
    if not all(checks.values()):
        raise RuntimeError(f"R4 patch audit failed: {checks}")
    report = {
        "classification": "C3_R4_DENSE_FORCE_OUTPUT_PATCH_READY",
        "physics_modified": False,
        "checks": checks,
    }
    repo = Path(__file__).resolve().parents[1]
    (repo / "results").mkdir(exist_ok=True)
    (repo / "results" / "c3_r4_patch_report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
