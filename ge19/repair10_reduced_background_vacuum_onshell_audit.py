#!/usr/bin/env python3
"""GE19 Repair10 reduced-background vacuum on-shell audit.

Diagnostic only.  Evaluates the homogeneous GE06 Einstein+AeST equations on
the frozen GE15 late-time CLASS background and compares the non-AeST density
and pressure required by those equations with:
  (i) the current matched conserved dust,
  (ii) that dust plus the frozen CLASS cosmological constant,
  (iii) the full known non-AeST CLASS background sector.
No linear operator or trajectory is changed.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.interpolate import PchipInterpolator

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

import ge09.repair01_dense_accepted_step_local_jet_bridge as g9
import ge18.repair01_on_shell_matched_dust_first_order_bridge as g18

C_VALUES={
    "C_min":2.566238549760586e-9,
    "C_star":2.568543329983919e-9,
    "C_max":2.5714842087496506e-9,
}
TINY=1.0e-300
DENSITY_FULL_MAX=5.0e-5
PRESSURE_FULL_MAX=5.0e-3
LAMBDA_IMPROVEMENT_REFERENCE=10.0
REPAIR08_SHA="8402a9f3ede227ca4c0c762976c8de247dd07161b41f504c438c6f248361d7d0"


def sha256(path:Path)->str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module(path:Path,name:str):
    spec=importlib.util.spec_from_file_location(name,path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def rel_l2(a,b):
    aa=np.asarray(a,float)
    bb=np.asarray(b,float)
    return float(np.linalg.norm(aa-bb)/max(np.linalg.norm(aa),np.linalg.norm(bb),TINY))


def residual_rel(target,model):
    t=np.asarray(target,float)
    m=np.asarray(model,float)
    return float(np.linalg.norm(t-m)/max(np.linalg.norm(t),np.linalg.norm(m),TINY))


def interp_background(path:Path,x):
    names,data=g18.parse_numbered_table(path)
    required=(
        "z","H [1/Mpc]","(.)rho_g","(.)rho_b","(.)rho_cdm",
        "(.)rho_ncdm[0]","(.)p_ncdm[0]","(.)rho_lambda",
        "(.)rho_ur","(.)rho_tot","(.)p_tot"
    )
    missing=[q for q in required if q not in names]
    if missing:
        raise RuntimeError(f"background missing {missing}; keys={sorted(names)}")

    z=np.asarray(data[:,names["z"]],float)
    a=1.0/(1.0+z)
    order=np.argsort(a)
    xa=np.log(a[order])
    if np.any(np.diff(xa)<=0):
        raise RuntimeError("background ln(a) is not strictly increasing")

    out={}
    for key in required:
        if key=="z":
            continue
        vals=np.asarray(data[:,names[key]],float)[order]
        out[key]=np.asarray(PchipInterpolator(xa,vals,extrapolate=False)(x),float)
    return out


def native_H_and_derivative(dense_path:Path,x):
    rows=g9.read_table(dense_path)
    modes,_=g9.group_modes(rows)
    ip=g9.build_interps(modes[0])
    H=np.asarray(ip["H_over_H0"](x),float)*g9.H0_CLASS
    dHdx=np.asarray(ip["H_over_H0"].derivative()(x),float)*g9.H0_CLASS
    return H,dHdx,modes


def summary_residual(target,current,plus_lambda):
    rc=residual_rel(target,current)
    rl=residual_rel(target,plus_lambda)
    return {
        "current_reduced_relative_L2":rc,
        "reduced_plus_lambda_relative_L2":rl,
        "lambda_improvement_factor":float(rc/max(rl,TINY)),
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--results-dir",default=str(ROOT/"results"))
    ap.add_argument("--json-out",required=True)
    args=ap.parse_args()
    rd=Path(args.results_dir)

    required=[
        rd/"ge15_R1_dense_accepted_step_trace.dat",
        rd/"ge15_R1_cli_background.dat",
        rd/"ge15_cancellation_free_s_state_precision_closure.json",
        rd/"ge19_repair08_shift_constraint_localization_audit.json",
    ]
    missing=[str(p) for p in required if not p.exists()]
    if missing:
        raise RuntimeError("missing frozen local inputs: "+", ".join(missing))

    r8path=rd/"ge19_repair08_shift_constraint_localization_audit.json"
    r8sha=sha256(r8path)
    if r8sha!=REPAIR08_SHA:
        raise RuntimeError(f"Repair08 result hash mismatch: {r8sha}")
    r8=json.loads(r8path.read_text())
    if r8.get("classification")!="GE19_REPAIR08_SHIFT_CONSTRAINT_LOCALIZATION_AUDIT_COMPLETE":
        raise RuntimeError("Repair08 parent classification mismatch")

    ge15=json.loads((rd/"ge15_cancellation_free_s_state_precision_closure.json").read_text())
    if ge15.get("classification")!="GE15_CANCELLATION_FREE_S_STATE_PRECISION_CLOSURE_PASS":
        raise RuntimeError("GE15 parent is not PASS")

    dense=rd/"ge15_R1_dense_accepted_step_trace.dat"
    dense_sha=sha256(dense)
    dense_expected=ge15["precision_binding"]["dense_trace_sha256"]["R1"]
    if dense_sha!=dense_expected:
        raise RuntimeError("GE15 dense hash mismatch")

    r7=load_module(
        ROOT/"ge19/repair07_window_retarded_reduced_h3_z20_particular.py",
        "ge19_repair07_for_repair10",
    )

    x=np.linspace(math.log(g9.AMIN),math.log(g9.AMAX),64)
    a=np.exp(x)
    H,dHdx,modes=native_H_and_derivative(dense,x)
    stable,native_diag,native_gates=r7.stable_exp_background_from_native(modes,a)

    # Cosmic-time derivatives for the homogeneous GE06 action.
    adot=a*H
    addot=a*H*(H+dHdx)

    Q=np.asarray(stable["Q"],float)
    KQ=np.asarray(stable["KQ"],float)
    K=np.asarray(stable["K"],float)

    # Exact homogeneous GE06 identities.
    E_N_ga=2.0*a**3*(3.0*H**2-(Q*KQ-K))
    E_L_ga=2.0*a**2*K+2.0*adot**2+4.0*a*addot

    rho_req=(3.0*H**2-(Q*KQ-K))/3.0
    p_req=-E_L_ga/(6.0*a**2)

    cbg=interp_background(rd/"ge15_R1_cli_background.dat",x)
    rho_g=cbg["(.)rho_g"]
    rho_b=cbg["(.)rho_b"]
    rho_aest_class=cbg["(.)rho_cdm"]
    rho_n=cbg["(.)rho_ncdm[0]"]
    p_n=cbg["(.)p_ncdm[0]"]
    rho_l=cbg["(.)rho_lambda"]
    rho_ur=cbg["(.)rho_ur"]
    p_tot=cbg["(.)p_tot"]
    H_bg=cbg["H [1/Mpc]"]

    rho_std=rho_b+rho_g+rho_ur+rho_n
    p_std=rho_g/3.0+rho_ur/3.0+p_n
    rho_full_nonA=rho_std+rho_l
    p_full_nonA=p_std-rho_l

    rho_aest_stable=(Q*KQ-K)/3.0
    p_aest_stable=K/3.0

    full_density_rel=residual_rel(rho_req,rho_full_nonA)
    full_pressure_rel=residual_rel(p_req,p_full_nonA)

    # Independent background-table identities, descriptive controls.
    H_trace_vs_bg_rel=rel_l2(H,H_bg)
    aest_density_rel=rel_l2(rho_aest_stable,rho_aest_class)
    p_req_vs_p_tot_minus_aest_rel=rel_l2(p_req,p_tot-p_aest_stable)

    per_C={}
    lambda_density_improvements=[]
    lambda_pressure_improvements=[]
    for tag,C in C_VALUES.items():
        rho_d=C/a**3
        p_d=np.zeros_like(a)

        ds=summary_residual(rho_req,rho_d,rho_d+rho_l)
        ps=summary_residual(p_req,p_d,p_d-rho_l)
        lambda_density_improvements.append(ds["lambda_improvement_factor"])
        lambda_pressure_improvements.append(ps["lambda_improvement_factor"])

        per_C[tag]={
            "density":ds,
            "pressure":ps,
            "dust_vs_full_standard_density_relative_L2":rel_l2(rho_d,rho_std),
            "dust_plus_lambda_vs_full_known_density_relative_L2":rel_l2(rho_d+rho_l,rho_full_nonA),
            "minus_lambda_vs_full_known_pressure_relative_L2":rel_l2(-rho_l,p_full_nonA),
        }

    finite=bool(all(np.all(np.isfinite(v)) for v in (
        a,H,dHdx,Q,KQ,K,E_N_ga,E_L_ga,rho_req,p_req,
        rho_std,p_std,rho_l,rho_full_nonA,p_full_nonA,
        rho_aest_stable,p_aest_stable
    )))
    stable_ok=bool(all(native_gates.values()))
    full_density_ok=bool(full_density_rel<=DENSITY_FULL_MAX)
    full_pressure_ok=bool(full_pressure_rel<=PRESSURE_FULL_MAX)
    density_lambda_dominant=bool(min(lambda_density_improvements)>=LAMBDA_IMPROVEMENT_REFERENCE)
    pressure_lambda_dominant=bool(min(lambda_pressure_improvements)>=LAMBDA_IMPROVEMENT_REFERENCE)

    if full_density_ok and full_pressure_ok and density_lambda_dominant and pressure_lambda_dominant:
        route="OMITTED_LAMBDA_DOMINANT_OFFSHELL_MECHANISM"
    elif full_density_ok and full_pressure_ok and (density_lambda_dominant or pressure_lambda_dominant):
        route="LAMBDA_REAL_BUT_NONVACUUM_REDUCTION_ALSO_MATERIAL"
    elif not (full_density_ok and full_pressure_ok):
        route="BACKGROUND_NORMALIZATION_OR_INTERPOLATION_UNRESOLVED"
    else:
        route="VACUUM_OMISSION_NOT_DOMINANT"

    report={
        "classification":"GE19_REPAIR10_REDUCED_BACKGROUND_VACUUM_ONSHELL_AUDIT_COMPLETE",
        "predata_classification":"GE19_REPAIR10_PREDATA_REDUCED_BACKGROUND_VACUUM_ONSHELL_AUDIT",
        "diagnostic_only":True,
        "repair08_result_sha256":r8sha,
        "provenance":{
            "GE15_parent_PASS":True,
            "GE15_dense_sha256":dense_sha,
            "GE15_dense_hash_exact":True,
            "stable_exp_native_diagnostic":native_diag,
            "stable_exp_native_gates":native_gates,
        },
        "equation_convention":{
            "GE06_lapse":"E_N/(2a^3)=3H^2-(QKQ-K)",
            "rho_required_nonAeST_CLASS":"[3H^2-(QKQ-K)]/3",
            "GE06_longitudinal_scale":"E_L=2a^2 K+2 adot^2+4a addot",
            "p_required_nonAeST_CLASS":"-E_L/(6a^2)",
            "lambda_action":"-6 rho_lambda N L R^2",
            "lambda_pressure":"-rho_lambda",
        },
        "full_known_background_closure":{
            "density_required_vs_rho_std_plus_lambda_global_relative_L2":full_density_rel,
            "pressure_required_vs_p_std_minus_lambda_global_relative_L2":full_pressure_rel,
            "limits":{
                "density":DENSITY_FULL_MAX,
                "pressure":PRESSURE_FULL_MAX,
            },
        },
        "independent_diagnostics":{
            "dense_trace_H_vs_CLASS_background_H_global_relative_L2":H_trace_vs_bg_rel,
            "stable_AeST_density_vs_CLASS_cdm_slot_global_relative_L2":aest_density_rel,
            "action_required_pressure_vs_CLASS_p_tot_minus_stable_AeST_pressure_global_relative_L2":p_req_vs_p_tot_minus_aest_rel,
            "rho_lambda_min":float(np.min(rho_l)),
            "rho_lambda_max":float(np.max(rho_l)),
            "p_std_over_rho_std_global_L2":float(np.linalg.norm(p_std)/max(np.linalg.norm(rho_std),TINY)),
        },
        "per_C":per_C,
        "global_lambda_improvement":{
            "density_min_across_C":float(min(lambda_density_improvements)),
            "density_max_across_C":float(max(lambda_density_improvements)),
            "pressure_min_across_C":float(min(lambda_pressure_improvements)),
            "pressure_max_across_C":float(max(lambda_pressure_improvements)),
            "reference_factor":LAMBDA_IMPROVEMENT_REFERENCE,
        },
        "controls":{
            "stable_AeST_native_reconstruction_PASS":stable_ok,
            "full_known_density_closure_PASS":full_density_ok,
            "full_known_pressure_closure_PASS":full_pressure_ok,
            "all_outputs_finite":finite,
        },
        "routing":{
            "lambda_density_dominant":density_lambda_dominant,
            "lambda_pressure_dominant":pressure_lambda_dominant,
            "next_route":route,
        },
        "claim_boundary":"Background/action audit only. No Lambda term has been added to the GE19 linear operator; no H1/H3/Z20 evolution is licensed."
    }

    out=Path(args.json_out)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2,allow_nan=False)+"\n")
    print(json.dumps(report,indent=2,allow_nan=False))


if __name__=="__main__":
    main()
