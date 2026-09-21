#!/usr/bin/env python3
"""GE19 Repair11 Lambda-inclusive reduced-H1 reclosure.

Adds only the exact first directional metric coefficients of
    L_lambda = -6 rho_lambda N L R^2
to the frozen Repair07 canonical reduced-H1 operator.  All initial data,
pressureless-dust C values, Noether partition, Radau scheme, constraint
metrics and Stage-A thresholds remain unchanged.  H3/Z20 is not constructed.
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

TINY=1.0e-300
REPAIR10_SHA="0903363695f071e635f91875903893041bfe728d9ff6c85b424604b933c8baa5"

LINEAR_MAX=1.0e-8
CONSTRAINT_MAX=1.0e-6
TIME_MAX=5.0e-3
INIT_MAX=1.0e-10


def sha256(path:Path)->str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module(path:Path,name:str):
    spec=importlib.util.spec_from_file_location(name,path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def interp_lambda(path:Path,x):
    names,data=g18.parse_numbered_table(path)
    for q in ("z","(.)rho_lambda"):
        if q not in names:
            raise RuntimeError(f"background missing {q}; keys={sorted(names)}")
    z=np.asarray(data[:,names["z"]],float)
    a=1.0/(1.0+z)
    order=np.argsort(a)
    xx=np.log(a[order])
    rr=np.asarray(data[:,names["(.)rho_lambda"]],float)[order]
    if np.any(np.diff(xx)<=0):
        raise RuntimeError("background ln(a) is not strictly increasing")
    out=np.asarray(PchipInterpolator(xx,rr,extrapolate=False)(np.asarray(x,float)),float)
    if not np.all(np.isfinite(out)):
        raise RuntimeError("nonfinite rho_lambda interpolation")
    return out


def lambda_c1_matrix(a,rho_lambda):
    """Gauge-fixed first directional local matrix for L_lambda.

    Local Repair07 w order:
      (N,dr,S,u,phi,T,Sdot,udot,phidot,Tdot)
    C row order:
      pS,pu,pphi,pT,lapse,dust-density,
      isotropic,aether,scalar,dust-potential,
      shift_ga,shift_m,anisotropy_ga,anisotropy_m,pLt,pRt.
    """
    a=float(a); rho=float(rho_lambda)
    C=np.zeros((16,10),complex)

    # delta E_N^lambda = -18 rho a^2 S
    C[4,2]=-18.0*rho*a*a

    # delta(E_L+E_R)^lambda
    #   = -18 rho a^2 N -36 rho a S
    C[6,0]=-18.0*rho*a*a
    C[6,2]=-36.0*rho*a

    # Shift and anisotropy vanish identically for a homogeneous vacuum action.
    return C


def install_lambda_operator(r7,lambda_by_bg):
    base_local=r7._local_linear_matrix
    lambda_diag={}

    def local_with_lambda(mod6,mod7,bg,tag,k,xq):
        C,bp,diag=base_local(mod6,mod7,bg,tag,k,xq)
        xx=np.asarray(bg["x"],float)
        rr=np.asarray(lambda_by_bg[id(bg)],float)
        rho=float(PchipInterpolator(xx,rr,extrapolate=False)(float(xq)))
        if not np.isfinite(rho):
            raise RuntimeError("nonfinite rho_lambda at canonical stage")
        Cl=lambda_c1_matrix(bp["a"],rho)
        out=np.asarray(C,complex).copy()+Cl
        key=(id(bg),round(float(xq),15))
        lambda_diag[key]={
            "x":float(xq),
            "a":float(bp["a"]),
            "rho_lambda":rho,
            "lambda_lapse_S_coefficient":float(np.real(Cl[4,2])),
            "lambda_isotropic_N_coefficient":float(np.real(Cl[6,0])),
            "lambda_isotropic_S_coefficient":float(np.real(Cl[6,2])),
            "lambda_shift_abs_max":float(np.max(np.abs(Cl[10:12]))),
            "lambda_anisotropy_abs_max":float(np.max(np.abs(Cl[12:14]))),
        }
        dd=dict(diag)
        dd.update({
            "lambda_inclusive":True,
            "rho_lambda":rho,
            "lambda_shift_abs_max":lambda_diag[key]["lambda_shift_abs_max"],
            "lambda_anisotropy_abs_max":lambda_diag[key]["lambda_anisotropy_abs_max"],
        })
        return out,bp,dd

    r7._local_linear_matrix=local_with_lambda
    return lambda_diag


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--results-dir",default=str(ROOT/"results"))
    ap.add_argument("--json-out",required=True)
    ap.add_argument("--npz-out",required=True)
    args=ap.parse_args()
    rd=Path(args.results_dir)

    required=[
        rd/"ge15_R1_dense_accepted_step_trace.dat",
        rd/"ge15_R1_cli_background.dat",
        rd/"ge15_cancellation_free_s_state_precision_closure.json",
        rd/"ge15_cancellation_free_s_state_precision_closure.npz",
        rd/"ge18_repair01_on_shell_matched_dust_first_order_bridge.json",
        rd/"ge18_repair01_on_shell_matched_dust_first_order_bridge.npz",
        rd/"ge19_repair10_reduced_background_vacuum_onshell_audit.json",
    ]
    missing=[str(p) for p in required if not p.exists()]
    if missing:
        raise RuntimeError("missing frozen local inputs: "+", ".join(missing))

    repair10_path=rd/"ge19_repair10_reduced_background_vacuum_onshell_audit.json"
    repair10_sha=sha256(repair10_path)
    if repair10_sha!=REPAIR10_SHA:
        raise RuntimeError(f"Repair10 result hash mismatch: {repair10_sha}")
    repair10=json.loads(repair10_path.read_text())
    if repair10.get("classification")!="GE19_REPAIR10_REDUCED_BACKGROUND_VACUUM_ONSHELL_AUDIT_COMPLETE":
        raise RuntimeError("Repair10 parent classification mismatch")
    if repair10.get("routing",{}).get("next_route")!="OMITTED_LAMBDA_DOMINANT_OFFSHELL_MECHANISM":
        raise RuntimeError("Repair10 did not license Lambda-inclusive reclosure")

    ge15=json.loads((rd/"ge15_cancellation_free_s_state_precision_closure.json").read_text())
    ge18=json.loads((rd/"ge18_repair01_on_shell_matched_dust_first_order_bridge.json").read_text())
    if ge15.get("classification")!="GE15_CANCELLATION_FREE_S_STATE_PRECISION_CLOSURE_PASS":
        raise RuntimeError("GE15 parent is not PASS")
    if ge18.get("classification")!="GE18_REPAIR01_ON_SHELL_MATCHED_DUST_FIRST_ORDER_BRIDGE_PASS":
        raise RuntimeError("GE18 Repair01 parent is not PASS")

    dense=rd/"ge15_R1_dense_accepted_step_trace.dat"
    dense_sha=sha256(dense)
    dense_expected=ge15["precision_binding"]["dense_trace_sha256"]["R1"]
    if dense_sha!=dense_expected:
        raise RuntimeError("GE15 dense hash mismatch")

    r7=load_module(
        ROOT/"ge19/repair07_window_retarded_reduced_h3_z20_particular.py",
        "ge19_repair07_for_repair11",
    )

    ge18_npz_path=rd/"ge18_repair01_on_shell_matched_dust_first_order_bridge.npz"
    ge18_npz_sha=sha256(ge18_npz_path)
    if ge18_npz_sha!=r7.GE18_NPZ_SHA:
        raise RuntimeError("GE18 NPZ hash mismatch")
    npz=np.load(ge18_npz_path)

    mod6_frozen=r7.load_frozen_generator(
        ROOT/"ge06/analytic_aest_directional_source_generator.py","ge19r11_ge06"
    )
    mod6=r7.build_stable_ge06_generator_v2(mod6_frozen)
    mod7=r7.load_frozen_generator(
        ROOT/"ge07/pressureless_matter_directional_source_generator.py","ge19r11_ge07"
    )

    bg64,_,jets64=r7.build_ge15_reference(dense,r7.NT_PRIMARY)
    bg32,_,jets32=r7.build_ge15_reference(dense,r7.NT_CONTROL)

    rho_l64=interp_lambda(rd/"ge15_R1_cli_background.dat",bg64["x"])
    rho_l32=interp_lambda(rd/"ge15_R1_cli_background.dat",bg32["x"])
    lambda_by_bg={id(bg64):rho_l64,id(bg32):rho_l32}
    lambda_diag=install_lambda_operator(r7,lambda_by_bg)

    ref64={}; refdot64={}; ref32={}; refdot32={}
    h1_64={}; h1_32={}; h1_dot64={}; h1_dot32={}
    rows=[]; time_rows=[]; reference_rows=[]
    sysmax=0.0; shiftmax=0.0; anisomax=0.0; initmax=0.0; timemax=0.0
    finite=True

    for tag in r7.C_TAGS:
        ref64[tag],refdot64[tag]=r7.reference_reduced_mode_state(bg64,jets64,npz,tag)
        ref32[tag],refdot32[tag]=r7.reference_reduced_mode_state(bg32,jets32,npz,tag)

        st64,dot64,c64=r7.solve_reduced_h1_case_canonical(
            mod6,mod7,bg64,tag,ref64[tag],refdot64[tag]
        )
        st32,dot32,c32=r7.solve_reduced_h1_case_canonical(
            mod6,mod7,bg32,tag,ref32[tag],refdot32[tag]
        )
        h1_64[tag]=st64; h1_32[tag]=st32
        h1_dot64[tag]=dot64; h1_dot32[tag]=dot32

        tc=r7.reduced_h1_time_control(bg64["x"],st64,bg32["x"],st32)
        cmp=r7.mixed_reference_comparison(st64,ref64[tag])

        rows.append({"C":tag,"primary":c64,"control":c32})
        time_rows.append({"C":tag,**tc})
        reference_rows.append({"C":tag,**cmp})

        sysmax=max(sysmax,c64["linear_system_relative_L2_max"],c32["linear_system_relative_L2_max"])
        shiftmax=max(shiftmax,c64["shift_constraint_relative_L2_max"],c32["shift_constraint_relative_L2_max"])
        anisomax=max(anisomax,c64["anisotropy_constraint_relative_L2_max"],c32["anisotropy_constraint_relative_L2_max"])
        initmax=max(initmax,c64["initial_dynamic_match_abs_or_rel_max"],c32["initial_dynamic_match_abs_or_rel_max"])
        timemax=max(timemax,tc["max"])
        finite=bool(finite and c64["all_outputs_finite"] and c32["all_outputs_finite"])

    gates={
        "linear_system_relative_L2_residual_le_1e8":bool(sysmax<=LINEAR_MAX),
        "shift_constraint_backward_error_le_1e6":bool(shiftmax<=CONSTRAINT_MAX),
        "anisotropy_constraint_backward_error_le_1e6":bool(anisomax<=CONSTRAINT_MAX),
        "primary64_vs_control32_state_global_relative_L2_le_5e3":bool(timemax<=TIME_MAX),
        "initial_dynamic_match_abs_or_rel_le_1e10":bool(initmax<=INIT_MAX),
        "all_outputs_finite":bool(finite),
    }
    passed=bool(all(gates.values()))

    ldiag=list(lambda_diag.values())
    if not ldiag:
        raise RuntimeError("no Lambda local-matrix diagnostics were recorded")
    lambda_summary={
        "rho_lambda_min":float(min(q["rho_lambda"] for q in ldiag)),
        "rho_lambda_max":float(max(q["rho_lambda"] for q in ldiag)),
        "lambda_lapse_S_coefficient_abs_max":float(max(abs(q["lambda_lapse_S_coefficient"]) for q in ldiag)),
        "lambda_isotropic_N_coefficient_abs_max":float(max(abs(q["lambda_isotropic_N_coefficient"]) for q in ldiag)),
        "lambda_isotropic_S_coefficient_abs_max":float(max(abs(q["lambda_isotropic_S_coefficient"]) for q in ldiag)),
        "lambda_shift_abs_max":float(max(q["lambda_shift_abs_max"] for q in ldiag)),
        "lambda_anisotropy_abs_max":float(max(q["lambda_anisotropy_abs_max"] for q in ldiag)),
        "n_local_points":int(len(ldiag)),
    }

    classification=(
        "GE19_REPAIR11_LAMBDA_INCLUSIVE_REDUCED_H1_RECLOSURE_PASS"
        if passed else
        "GE19_REPAIR11_LAMBDA_INCLUSIVE_REDUCED_H1_RECLOSURE_FAIL"
    )

    report={
        "classification":classification,
        "predata_classification":"GE19_REPAIR11_PREDATA_LAMBDA_INCLUSIVE_REDUCED_H1_RECLOSURE",
        "stage":"Stage_A_reduced_H1_reclosure_only",
        "repair10_result_sha256":repair10_sha,
        "lambda_action":"-6 rho_lambda N L R^2",
        "lambda_background_source":"frozen GE15 CLASS rho_lambda",
        "lambda_first_directional_matrix_summary":lambda_summary,
        "controls":{
            "max_linear_system_relative_L2":sysmax,
            "max_shift_constraint_relative_L2":shiftmax,
            "max_anisotropy_constraint_relative_L2":anisomax,
            "max_initial_dynamic_match_abs_or_rel":initmax,
            "primary64_vs_control32_state_global_relative_L2_max":timemax,
            "all_outputs_finite":finite,
            "rows":rows,
            "time_control":time_rows,
            "mixed_reference_comparison":reference_rows,
        },
        "gates":gates,
        "stage_A_pass":passed,
        "Z20_constructed":False,
        "next_step":(
            "Preregister Lambda second-directional metric source and H3/Z20 particular solve."
            if passed else
            "Do not construct H3/Z20. Localize the remaining Stage-A failing gate without threshold relaxation."
        ),
        "provenance":{
            "GE15_dense_sha256":dense_sha,
            "GE15_dense_hash_exact":dense_sha==dense_expected,
            "GE18_npz_sha256":ge18_npz_sha,
            "GE18_npz_hash_exact":ge18_npz_sha==r7.GE18_NPZ_SHA,
            "Repair10_parent_route":repair10["routing"]["next_route"],
            "rho_lambda_table":"results/ge15_R1_cli_background.dat",
        },
        "claim_boundary":"Lambda-inclusive reduced-H1 Stage-A result only. No H3/Z20, finite eta, finite physical-amplitude nonlinear evolution, collapse, lensing or observational claim."
    }

    out=Path(args.json_out)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2,allow_nan=False)+"\n")

    save={
        "x64":np.asarray(bg64["x"],float),
        "x32":np.asarray(bg32["x"],float),
        "rho_lambda64":rho_l64,
        "rho_lambda32":rho_l32,
    }
    for tag in r7.C_TAGS:
        save[f"{tag}_Z10_lambda_primary"]=h1_64[tag]
        save[f"{tag}_Z10_lambda_control"]=h1_32[tag]
        save[f"{tag}_Z10_lambda_dot_primary"]=h1_dot64[tag]
        save[f"{tag}_Z10_lambda_dot_control"]=h1_dot32[tag]
    np.savez_compressed(args.npz_out,**save)

    print(json.dumps(report,indent=2,allow_nan=False))


if __name__=="__main__":
    main()
