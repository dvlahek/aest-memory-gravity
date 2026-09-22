#!/usr/bin/env python3
"""GE19 Repair32A — exact GE06/GE05 raw-residual normalization dictionary audit.

No H2 integration is performed. The exact dictionary factor is derived
symbolically and only then checked against frozen Repair31 driven-row ratios.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
R31_SHA="569ad9b16a26989fd8a9c9c02d83b77eb4afe23d9962fa56b87166d78d0ea33a"
EMP_TOL=1.0e-3

def sha256(p:Path)->str:
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):
            h.update(b)
    return h.hexdigest()

def require_text(path:Path,needle:str):
    txt=path.read_text()
    return needle in txt

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--repair31-json",required=True)
    ap.add_argument("--json-out",required=True)
    args=ap.parse_args()

    r31=Path(args.repair31_json)
    if sha256(r31)!=R31_SHA:
        raise RuntimeError("Repair31 JSON hash mismatch")
    d31=json.loads(r31.read_text())
    if d31.get("classification")!="GE19_REPAIR31_REPAIR30_H2_DICTIONARY_AND_MONITOR_AUDIT_COMPLETE":
        raise RuntimeError("unexpected Repair31 classification")

    a,KB,Q,B,Edot=sp.symbols("a KB Q B Edot", positive=True, nonzero=True)
    E=sp.symbols("E")
    # Isolated coefficient audit: GE06 contains a^3 KB E^2.
    L6=a**3*KB*E**2
    pE=sp.diff(L6,E)
    class_mem_Edot=-Q*B/(2*KB)
    # GE06 residual convention contains -d/dt(dL/dudot);
    # source placed on RHS is therefore -R_mem = +2 a^3 KB*(-Edot_mem)
    ge06_rhs=sp.simplify(-2*a**3*KB*class_mem_Edot)
    ge05_M1=-a**3*Q*B/2
    repair30_rhs=sp.simplify(-ge05_M1)
    ratio=sp.simplify(ge06_rhs/repair30_rhs)

    sol=d31["operator_residual_localization"]["summary"]["solution"]["main_by_equation"]
    ref=d31["operator_residual_localization"]["summary"]["reference"]["main_by_equation"]
    ar=float(ref["aether_rapidity"]["global_lhs_L2"]/ref["aether_rapidity"]["global_rhs_L2"])
    sr=float(ref["scalar_phi"]["global_lhs_L2"]/ref["scalar_phi"]["global_rhs_L2"])
    sol_ar=float(sol["aether_rapidity"]["global_lhs_L2"]/sol["aether_rapidity"]["global_rhs_L2"])
    sol_sr=float(sol["scalar_phi"]["global_lhs_L2"]/sol["scalar_phi"]["global_rhs_L2"])

    impl={
        "GE06_a3_KB_E2":require_text(ROOT/"ge06/analytic_aest_directional_source_generator.py","KB*E**2"),
        "GE05_quarter_completed_square":require_text(ROOT/"ge05/memory_directional_source_generator.py","sp.Rational(1,4)"),
        "v039_force_half":require_text(ROOT/"v039/build_tau_forcing.py","fc=-0.5*aa*aa*Q*yc/a.KB"),
        "v019w_runtime_half":require_text(ROOT/"v019w/apply_variational_forcing_patch.py","dEprime/deta|0 = -a Q Bchi_raw/(2 KB)"),
        "NL0B_factor_half_frozen":require_text(ROOT/"docs/nl0b_covariant_memory_completion_result.md","The factor \\(1/2\\) is fixed by the preregistered action normalization"),
    }

    exact={
        "GE06_isolated_L":str(L6),
        "dL_dE":str(pE),
        "CLASS_memory_Edot":str(class_mem_Edot),
        "GE06_raw_rhs_implied_by_CLASS":str(ge06_rhs),
        "GE05_M1_aether":str(ge05_M1),
        "Repair30_minus_M1_rhs":str(repair30_rhs),
        "exact_dictionary_ratio":str(ratio),
        "ratio_equals_2":bool(sp.simplify(ratio-2)==0),
    }

    empirical={
        "Repair30_solution_aether_LHS_over_RHS":sol_ar,
        "Repair30_solution_scalar_LHS_over_RHS":sol_sr,
        "R2_reference_aether_LHS_over_Repair30_RHS":ar,
        "R2_reference_scalar_LHS_over_Repair30_RHS":sr,
        "aether_abs_deviation_from_2":abs(ar-2.0),
        "scalar_abs_deviation_from_2":abs(sr-2.0),
        "both_within_1e3":bool(abs(ar-2.0)<=EMP_TOL and abs(sr-2.0)<=EMP_TOL),
    }

    gates={
        "exact_dictionary_ratio_eq_2":exact["ratio_equals_2"],
        "all_implementation_conventions_found":bool(all(impl.values())),
        "Repair31_aether_scalar_ratios_within_1e3_of_2":empirical["both_within_1e3"],
        "Repair30_solution_still_solves_its_frozen_rhs":bool(abs(sol_ar-1.0)<=1e-3 and abs(sol_sr-1.0)<=1e-3),
    }
    passed=all(gates.values())

    out={
        "classification":(
            "GE19_REPAIR32A_GE06_GE05_RAW_RESIDUAL_NORMALIZATION_DICTIONARY_PASS"
            if passed else
            "GE19_REPAIR32A_GE06_GE05_RAW_RESIDUAL_NORMALIZATION_DICTIONARY_FAIL"
        ),
        "predata_classification":"GE19_REPAIR32A_PREDATA_GE06_GE05_RAW_RESIDUAL_NORMALIZATION_DICTIONARY_AUDIT",
        "uses_observational_data":False,
        "Repair30_relabelled":False,
        "Repair31_relabelled":False,
        "H2_reintegration":False,
        "H4_Z21_solve":False,
        "provenance":{"Repair31_JSON_sha256":sha256(r31)},
        "exact_symbolic_dictionary":exact,
        "implementation_convention_audit":impl,
        "Repair31_empirical_consistency":empirical,
        "gates":gates,
        "derived_dictionary":{
            "GE05_M1_to_GE06_raw_residual_scale":2 if passed else None,
            "fitted_normalization_used":False,
        },
        "routing":{
            "next_route":(
                "PREREGISTER_REPAIR32B_FACTOR2_CORRECTED_REDUCED_H2_Z11_RECLOSURE"
                if passed else
                "RAW_RESIDUAL_NORMALIZATION_DICTIONARY_UNRESOLVED"
            ),
            "H4_Z21_licensed":False,
        },
        "claim_boundary":"Exact normalization-dictionary audit only. No H2 reintegration, Repair30 relabel, fitted normalization, H4/Z21, finite eta, or observational claim."
    }
    p=Path(args.json_out); p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(out,indent=2,allow_nan=False)+"\n")
    print(json.dumps(out,indent=2,allow_nan=False))
    if not passed:
        raise SystemExit(2)

if __name__=="__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:
        print(json.dumps({
            "classification":"GE19_REPAIR32A_IMPLEMENTATION_FAIL",
            "error":repr(exc),
            "H2_reintegration":False,
            "H4_Z21_solve":False
        },indent=2))
        raise
