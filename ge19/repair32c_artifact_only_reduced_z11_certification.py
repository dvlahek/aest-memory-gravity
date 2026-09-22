#!/usr/bin/env python3
"""GE19 Repair32C — artifact-only reduced Z11 certification.

No H2 integration is performed. This script certifies the already frozen
Repair32B corrected H2 state using global state precision, chi-parent closure,
and artifact-only reduced-operator/constraint diagnostics.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

import ge19.repair07_window_retarded_reduced_h3_z20_particular as r7
import ge19.repair31_repair30_h2_dictionary_monitor_audit as r31

R32B_JSON_SHA="226dd2a2a0e86ddccc39a62d833960bdf9d5a9af038ad3bf225bbbf69d0b95cf"
R32B_NPZ_SHA="5d4a0a72c08d09d096a8de0b428b3c8443fc33e8ad442ed6d997d6bf2bc6e327"
R32B_JSON_BYTES=68434
R32B_NPZ_BYTES=1082578

STATE_MAX=5e-3
CHI_MAX=5e-3
INIT_MAX=1e-8
OPERATOR_MAX=1e-4
CONSTRAINT_MAX=1e-6
C_ENVELOPE_MAX=5e-3
TINY=1e-300

SOURCE_FREE=("lapse","isotropic_spatial","dust_potential","dust_density")
DRIVEN=("aether_rapidity","scalar_phi")


def sha256(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):
            h.update(b)
    return h.hexdigest()


def rel_l2(a,b)->float:
    aa=np.asarray(a); bb=np.asarray(b)
    return float(np.linalg.norm(aa-bb)/max(np.linalg.norm(aa),np.linalg.norm(bb),TINY))


def c_envelope(z):
    star=np.asarray(z["C_star_chi11_primary"],complex)
    rows=[]
    mx=0.0
    for tag in ("C_min","C_max"):
        ch=np.asarray(z[f"{tag}_chi11_primary"],complex)
        e=rel_l2(ch,star)
        rows.append({"C":tag,"relative_L2_vs_C_star":e})
        mx=max(mx,e)
    return {"relative_L2_max":float(mx),"per_C":rows}


def source_free_global(operator_summary):
    eq=operator_summary["main_by_equation"]
    global_scale=math.sqrt(sum(max(float(v["global_lhs_L2"]),float(v["global_rhs_L2"]))**2 for v in eq.values()))
    rows={}
    mx=0.0
    for name in SOURCE_FREE:
        v=eq[name]
        q=float(v["global_absolute_L2"]/max(global_scale,TINY))
        rows[name]={
            "global_absolute_L2":float(v["global_absolute_L2"]),
            "absolute_over_global_main_operator_scale":q,
        }
        mx=max(mx,q)
    return {
        "global_main_operator_scale":float(global_scale),
        "max_absolute_over_global_main_operator_scale":float(mx),
        "per_equation":rows,
    }


def all_finite_obj(obj)->bool:
    if isinstance(obj,dict):
        return all(all_finite_obj(v) for v in obj.values())
    if isinstance(obj,(list,tuple)):
        return all(all_finite_obj(v) for v in obj)
    if isinstance(obj,(int,bool,str)) or obj is None:
        return True
    if isinstance(obj,float):
        return math.isfinite(obj)
    return True


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--results-dir",default=str(ROOT/"results"))
    ap.add_argument("--repair32b-json",required=True)
    ap.add_argument("--repair32b-npz",required=True)
    ap.add_argument("--json-out",required=True)
    args=ap.parse_args()

    j=Path(args.repair32b_json)
    n=Path(args.repair32b_npz)
    if not j.exists() or not n.exists():
        raise RuntimeError("missing frozen Repair32B artifacts")
    if sha256(j)!=R32B_JSON_SHA or j.stat().st_size!=R32B_JSON_BYTES:
        raise RuntimeError("Repair32B JSON provenance mismatch")
    if sha256(n)!=R32B_NPZ_SHA or n.stat().st_size!=R32B_NPZ_BYTES:
        raise RuntimeError("Repair32B NPZ provenance mismatch")

    d=json.loads(j.read_text())
    if d.get("classification")!="GE19_REPAIR32B_FACTOR2_CORRECTED_REDUCED_H2_Z11_RECONSTRUCTION_PASS":
        raise RuntimeError("Repair32B classification is not PASS")
    if d.get("corrected_H2_reconstruction_validated") is not True:
        raise RuntimeError("Repair32B corrected H2 reconstruction is not validated")
    if d.get("Z11_certified") is not False:
        raise RuntimeError("Repair32B must enter Repair32C uncertified")
    if d.get("routing",{}).get("H4_Z21_licensed") is not False:
        raise RuntimeError("Repair32B must not already license H4/Z21")
    dd=d.get("raw_residual_dictionary",{})
    if dd.get("GE05_M1_to_GE06_raw_residual_scale")!=2.0 or dd.get("fitted_normalization_used") is not False:
        raise RuntimeError("Repair32B dictionary provenance mismatch")
    if not all(bool(v) for v in d.get("validation_gates",{}).values()):
        raise RuntimeError("Repair32B reconstruction gates are not all PASS")

    z=np.load(n)
    bgs,bases,mod6,mod7,bgdiag=r31.build_operator_context(Path(args.results_dir))

    state=r31.state_precision(z)
    chi=r31.chi_audit(z)
    op=r31.operator_audit(z,bgs,mod6,mod7)
    sol=op["summary"]["solution"]
    eq=sol["main_by_equation"]
    sf=source_free_global(sol)
    ce=c_envelope(z)

    driven={
        name:{
            "global_relative_L2":float(eq[name]["global_relative_L2"]),
            "global_absolute_L2":float(eq[name]["global_absolute_L2"]),
            "global_lhs_L2":float(eq[name]["global_lhs_L2"]),
            "global_rhs_L2":float(eq[name]["global_rhs_L2"]),
        }
        for name in DRIVEN
    }
    driven_max=max(v["global_relative_L2"] for v in driven.values())
    shift=float(sol["constraints"]["shift"]["global_relative_to_operator_scale"])
    aniso=float(sol["constraints"]["anisotropy"]["global_relative_to_operator_scale"])

    gates={
        "Repair32B_hashes_exact":True,
        "Repair32B_reconstruction_PASS":True,
        "Repair32B_exact_dictionary_factor_2_no_fit":True,
        "Repair32B_reconstruction_validation_gates_all_PASS":True,
        "full_six_field_global_Nt128_vs_Nt64_relative_L2_le_5e3":bool(state["full_six_field_global_relative_L2_max"]<=STATE_MAX),
        "dynamic_global_Nt128_vs_Nt64_relative_L2_le_5e3":bool(state["dynamic_global_relative_L2_max"]<=STATE_MAX),
        "chi11_vs_R2_parent_relative_L2_le_5e3":bool(chi["relative_L2_max"]<=CHI_MAX),
        "chi11_initial_boundary_abs_or_rel_le_1e8":bool(chi["initial_abs_or_rel_max"]<=INIT_MAX),
        "driven_aether_scalar_operator_global_relative_L2_le_1e4":bool(driven_max<=OPERATOR_MAX),
        "source_free_main_rows_absolute_over_global_operator_scale_le_1e4":bool(sf["max_absolute_over_global_main_operator_scale"]<=OPERATOR_MAX),
        "shift_global_relative_to_operator_scale_le_1e6":bool(shift<=CONSTRAINT_MAX),
        "anisotropy_global_relative_to_operator_scale_le_1e6":bool(aniso<=CONSTRAINT_MAX),
        "chi11_C_envelope_relative_L2_le_5e3":bool(ce["relative_L2_max"]<=C_ENVELOPE_MAX),
    }

    diagnostics={
        "state_precision":state,
        "chi_parent":chi,
        "operator_solution_summary":sol,
        "driven_rows":driven,
        "driven_rows_global_relative_L2_max":float(driven_max),
        "source_free_rows":sf,
        "shift_global_relative_to_operator_scale":shift,
        "anisotropy_global_relative_to_operator_scale":aniso,
        "chi11_C_envelope":ce,
        "background_control":bgdiag,
    }
    finite=all_finite_obj(diagnostics)
    gates["all_artifact_diagnostics_finite"]=bool(finite)

    passed=bool(all(gates.values()))
    report={
        "classification":(
            "GE19_REPAIR32C_ARTIFACT_ONLY_REDUCED_Z11_CERTIFICATION_PASS"
            if passed else
            "GE19_REPAIR32C_ARTIFACT_ONLY_REDUCED_Z11_CERTIFICATION_FAIL"
        ),
        "predata_classification":"GE19_REPAIR32C_PREDATA_ARTIFACT_ONLY_REDUCED_Z11_CERTIFICATION",
        "uses_observational_data":False,
        "finite_physical_eta":False,
        "Repair32B_H2_reintegrated":False,
        "H4_Z21_solve_performed":False,
        "provenance":{
            "Repair32B_JSON_sha256":sha256(j),
            "Repair32B_JSON_bytes":j.stat().st_size,
            "Repair32B_NPZ_sha256":sha256(n),
            "Repair32B_NPZ_bytes":n.stat().st_size,
            "Repair32B_dictionary_scale":2.0,
            "fitted_normalization_used":False,
        },
        "thresholds":{
            "state_global_max":STATE_MAX,
            "chi_parent_max":CHI_MAX,
            "initial_boundary_max":INIT_MAX,
            "artifact_operator_max":OPERATOR_MAX,
            "global_constraint_max":CONSTRAINT_MAX,
            "C_envelope_max":C_ENVELOPE_MAX,
        },
        "diagnostics":diagnostics,
        "gates":gates,
        "Z11_certified":passed,
        "routing":{
            "next_route":(
                "REDUCED_Z11_CERTIFIED_PREREGISTER_H4_Z21"
                if passed else
                "ARTIFACT_ONLY_Z11_CERTIFICATION_FAIL_LOCALIZE_GATE"
            ),
            "H4_Z21_licensed":passed,
        },
        "claim_boundary":"Repair32C is artifact-only reduced-Z11 certification. It performs no H2 reintegration, no source change, no threshold fit, no H4/Z21 solve, no finite eta and no observational claim."
    }

    out=Path(args.json_out)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2,allow_nan=False)+"\n")
    print(json.dumps(report,indent=2,allow_nan=False))
    if not passed:
        raise SystemExit(2)


if __name__=="__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:
        print(json.dumps({
            "classification":"GE19_REPAIR32C_IMPLEMENTATION_FAIL",
            "error":repr(exc),
            "Repair32B_H2_reintegrated":False,
            "Z11_certified":False,
            "H4_Z21_solve_performed":False
        },indent=2))
        raise
