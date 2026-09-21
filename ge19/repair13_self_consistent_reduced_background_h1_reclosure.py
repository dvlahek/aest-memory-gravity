#!/usr/bin/env python3
"""GE19 Repair13 self-consistent reduced-background H1 reclosure.

Uses the exact homogeneous AeST+dust+Lambda Friedmann solution for H(a)
on the same frozen x=ln(a) grids.  The AeST scalar charge/Exp branch,
dust C envelope, Lambda action, first-order equations, initial dynamic data,
canonical partition, Radau scheme, metrics and gates are unchanged.
H3/Z20 is not constructed.
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

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

TINY=1.0e-300
REPAIR12_SHA="e442e37dab7df97f890cc2b210d34446a204437650226f82a4887e1e2d0dc270"

LINEAR_MAX=1.0e-8
CONSTRAINT_MAX=1.0e-6
TIME_MAX=5.0e-3
INIT_MAX=1.0e-10
BG_FRIEDMANN_MAX=1.0e-12
BG_PRESSURE_MAX=1.0e-10


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


def stable_K_from_bg(r7,bg):
    """Recover K(Q) from the same stable Exp coordinates without exp overflow."""
    kq=np.asarray(bg["KQ_action"],float)
    z=np.asarray(bg["Z_action"],float)
    ex=kq/(4.0*r7.K2*r7.Z0*z)
    kval=2.0*r7.K2*r7.Z0*r7.Z0*(ex-1.0)
    if not np.all(np.isfinite(kval)):
        raise RuntimeError("nonfinite stable K")
    return kval


def reduced_background(r7,base_bg,tag,rho_lambda):
    """Exact homogeneous AeST+dust+Lambda background on the frozen a grid."""
    a=np.asarray(base_bg["a"],float)
    q=np.asarray(base_bg["Q_action"],float)
    kq=np.asarray(base_bg["KQ_action"],float)
    kqq=np.asarray(base_bg["KQQ_action"],float)
    rho_l=np.asarray(rho_lambda,float)
    if not (a.shape==q.shape==kq.shape==kqq.shape==rho_l.shape):
        raise RuntimeError("reduced background array-shape mismatch")

    kval=stable_K_from_bg(r7,base_bg)
    rho_aest=(q*kq-kval)/3.0
    rho_d=r7.C_VALUES[tag]/a**3
    H2=rho_aest+rho_d+rho_l
    if np.any(~np.isfinite(H2)) or np.any(H2<=0.0):
        raise RuntimeError(f"nonpositive/nonfinite reduced H^2 for {tag}")
    H=np.sqrt(H2)

    # Exact lapse/Friedmann identity:
    # 3H^2-(QKQ-K)-3(rho_d+rho_lambda)=0.
    fried=3.0*H2-(q*kq-kval)-3.0*(rho_d+rho_l)
    fried_scale=np.maximum(
        np.abs(3.0*H2)+np.abs(q*kq-kval)+3.0*np.abs(rho_d+rho_l),
        TINY,
    )
    fried_rel=float(np.linalg.norm(fried)/max(np.linalg.norm(fried_scale),TINY))

    # Exact reduced pressure identity.  Scalar conservation gives
    # d KQ/d ln a = -3 KQ and therefore
    # d[(QKQ-K)/3]/d ln a = -Q KQ.
    dH2_dx=-q*kq-3.0*rho_d
    p_required=-(kval/3.0+H2+dH2_dx/3.0)
    p_target=-rho_l
    pressure_rel=rel_l2(p_required,p_target)

    bg=dict(base_bg)
    bg["H_CLASS_full"]=np.asarray(base_bg["H"],float).copy()
    bg["H"]=H
    bg["K_action"]=kval
    bg["rho_AeST_action"]=rho_aest
    bg["rho_dust_action"]=rho_d
    bg["rho_lambda_action"]=rho_l

    diag={
        "C":tag,
        "friedmann_relative_L2":fried_rel,
        "pressure_identity_relative_L2":pressure_rel,
        "H_red_min":float(np.min(H)),
        "H_red_max":float(np.max(H)),
        "H_red_vs_CLASS_full_global_relative_L2":rel_l2(H,np.asarray(base_bg["H"],float)),
        "rho_AeST_min":float(np.min(rho_aest)),
        "rho_AeST_max":float(np.max(rho_aest)),
        "rho_dust_min":float(np.min(rho_d)),
        "rho_dust_max":float(np.max(rho_d)),
        "rho_lambda_min":float(np.min(rho_l)),
        "rho_lambda_max":float(np.max(rho_l)),
        "all_background_values_finite":bool(
            all(np.all(np.isfinite(x)) for x in (H,kval,rho_aest,rho_d,rho_l))
        ),
        "H_positive":bool(np.all(H>0.0)),
    }
    return bg,diag


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
        rd/"ge18_repair01_on_shell_matched_dust_first_order_bridge.json",
        rd/"ge18_repair01_on_shell_matched_dust_first_order_bridge.npz",
        rd/"ge19_repair12_remaining_standard_momentum_audit.json",
    ]
    missing=[str(p) for p in required if not p.exists()]
    if missing:
        raise RuntimeError("missing frozen local inputs: "+", ".join(missing))

    repair12_path=rd/"ge19_repair12_remaining_standard_momentum_audit.json"
    r12sha=sha256(repair12_path)
    if r12sha!=REPAIR12_SHA:
        raise RuntimeError(f"Repair12 result hash mismatch: {r12sha}")
    r12=json.loads(repair12_path.read_text())
    if r12.get("classification")!="GE19_REPAIR12_REMAINING_STANDARD_MOMENTUM_AUDIT_COMPLETE":
        raise RuntimeError("unexpected Repair12 classification")
    if r12.get("routing",{}).get("next_route")!="BACKGROUND_OR_REDUCED_DYNAMICS_REMAIN":
        raise RuntimeError("Repair12 did not license reduced-background reclosure")

    r7=load_module(
        ROOT/"ge19/repair07_window_retarded_reduced_h3_z20_particular.py",
        "ge19_repair07_for_repair13",
    )
    r11=load_module(
        ROOT/"ge19/repair11_lambda_inclusive_reduced_h1_reclosure.py",
        "ge19_repair11_for_repair13",
    )

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

    ge18_npz_path=rd/"ge18_repair01_on_shell_matched_dust_first_order_bridge.npz"
    ge18_npz_sha=sha256(ge18_npz_path)
    if ge18_npz_sha!=r7.GE18_NPZ_SHA:
        raise RuntimeError("GE18 NPZ hash mismatch")
    npz=np.load(ge18_npz_path)

    mod6_frozen=r7.load_frozen_generator(
        ROOT/"ge06/analytic_aest_directional_source_generator.py","ge19r13_ge06"
    )
    mod6=r7.build_stable_ge06_generator_v2(mod6_frozen)
    mod7=r7.load_frozen_generator(
        ROOT/"ge07/pressureless_matter_directional_source_generator.py","ge19r13_ge07"
    )

    base64,_,jets64=r7.build_ge15_reference(dense,r7.NT_PRIMARY)
    base32,_,jets32=r7.build_ge15_reference(dense,r7.NT_CONTROL)
    rho_l64=r11.interp_lambda(rd/"ge15_R1_cli_background.dat",base64["x"])
    rho_l32=r11.interp_lambda(rd/"ge15_R1_cli_background.dat",base32["x"])

    bg64={}; bg32={}; bgdiag=[]
    lambda_by_bg={}
    for tag in r7.C_TAGS:
        bg64[tag],d64=reduced_background(r7,base64,tag,rho_l64)
        bg32[tag],d32=reduced_background(r7,base32,tag,rho_l32)
        bgdiag.append({"C":tag,"primary":d64,"control":d32})
        lambda_by_bg[id(bg64[tag])]=rho_l64
        lambda_by_bg[id(bg32[tag])]=rho_l32

    # Install exactly the frozen Repair11 first-directional Lambda operator.
    lambda_diag=r11.install_lambda_operator(r7,lambda_by_bg)

    rows=[]; time_rows=[]; reference_rows=[]
    h1_64={}; h1_32={}; dot_64={}; dot_32={}
    sysmax=0.0; shiftmax=0.0; anisomax=0.0; initmax=0.0; timemax=0.0
    finite=True
    bg_fried_max=0.0; bg_pressure_max=0.0; bg_ok=True

    for q in bgdiag:
        for grid in ("primary","control"):
            b=q[grid]
            bg_fried_max=max(bg_fried_max,b["friedmann_relative_L2"])
            bg_pressure_max=max(bg_pressure_max,b["pressure_identity_relative_L2"])
            bg_ok=bool(bg_ok and b["all_background_values_finite"] and b["H_positive"])

    for tag in r7.C_TAGS:
        ref64,refdot64=r7.reference_reduced_mode_state(bg64[tag],jets64,npz,tag)
        ref32,refdot32=r7.reference_reduced_mode_state(bg32[tag],jets32,npz,tag)

        st64,dt64,c64=r7.solve_reduced_h1_case_canonical(
            mod6,mod7,bg64[tag],tag,ref64,refdot64
        )
        st32,dt32,c32=r7.solve_reduced_h1_case_canonical(
            mod6,mod7,bg32[tag],tag,ref32,refdot32
        )

        h1_64[tag]=st64; h1_32[tag]=st32
        dot_64[tag]=dt64; dot_32[tag]=dt32

        tc=r7.reduced_h1_time_control(
            bg64[tag]["x"],st64,bg32[tag]["x"],st32
        )
        cmp=r7.mixed_reference_comparison(st64,ref64)

        rows.append({"C":tag,"primary":c64,"control":c32})
        time_rows.append({"C":tag,**tc})
        reference_rows.append({"C":tag,**cmp})

        sysmax=max(sysmax,c64["linear_system_relative_L2_max"],c32["linear_system_relative_L2_max"])
        shiftmax=max(shiftmax,c64["shift_constraint_relative_L2_max"],c32["shift_constraint_relative_L2_max"])
        anisomax=max(anisomax,c64["anisotropy_constraint_relative_L2_max"],c32["anisotropy_constraint_relative_L2_max"])
        initmax=max(initmax,c64["initial_dynamic_match_abs_or_rel_max"],c32["initial_dynamic_match_abs_or_rel_max"])
        timemax=max(timemax,tc["max"])
        finite=bool(finite and c64["all_outputs_finite"] and c32["all_outputs_finite"])

    bg_gates={
        "friedmann_relative_L2_le_1e12":bool(bg_fried_max<=BG_FRIEDMANN_MAX),
        "pressure_identity_relative_L2_le_1e10":bool(bg_pressure_max<=BG_PRESSURE_MAX),
        "all_background_values_finite":bool(bg_ok),
        "H_positive":bool(bg_ok),
    }
    stage_gates={
        "linear_system_relative_L2_residual_le_1e8":bool(sysmax<=LINEAR_MAX),
        "shift_constraint_backward_error_le_1e6":bool(shiftmax<=CONSTRAINT_MAX),
        "anisotropy_constraint_backward_error_le_1e6":bool(anisomax<=CONSTRAINT_MAX),
        "primary64_vs_control32_state_global_relative_L2_le_5e3":bool(timemax<=TIME_MAX),
        "initial_dynamic_match_abs_or_rel_le_1e10":bool(initmax<=INIT_MAX),
        "all_outputs_finite":bool(finite),
    }
    passed=bool(all(bg_gates.values()) and all(stage_gates.values()))

    classification=(
        "GE19_REPAIR13_SELF_CONSISTENT_REDUCED_BACKGROUND_H1_RECLOSURE_PASS"
        if passed else
        "GE19_REPAIR13_SELF_CONSISTENT_REDUCED_BACKGROUND_H1_RECLOSURE_FAIL"
    )

    report={
        "classification":classification,
        "predata_classification":"GE19_REPAIR13_PREDATA_SELF_CONSISTENT_REDUCED_BACKGROUND_H1_RECLOSURE",
        "stage":"Stage_A_reduced_H1_reclosure_only",
        "repair12_result_sha256":r12sha,
        "background_definition":{
            "friedmann":"H_red^2=(Q K_Q-K)/3+C/a^3+rho_lambda",
            "scalar_charge":"a^3 K_Q = frozen GE15 I0",
            "same_x_grids":True,
            "same_Q_Z_branch":True,
            "same_C_values":True,
            "same_rho_lambda":True,
        },
        "background_controls":{
            "friedmann_relative_L2_max":bg_fried_max,
            "pressure_identity_relative_L2_max":bg_pressure_max,
            "rows":bgdiag,
            "gates":bg_gates,
        },
        "stage_A_controls":{
            "max_linear_system_relative_L2":sysmax,
            "max_shift_constraint_relative_L2":shiftmax,
            "max_anisotropy_constraint_relative_L2":anisomax,
            "max_initial_dynamic_match_abs_or_rel":initmax,
            "primary64_vs_control32_state_global_relative_L2_max":timemax,
            "all_outputs_finite":finite,
            "rows":rows,
            "time_control":time_rows,
            "mixed_reference_comparison":reference_rows,
            "gates":stage_gates,
        },
        "stage_A_pass":passed,
        "Z20_constructed":False,
        "next_step":(
            "Freeze Stage-A PASS and separately preregister Lambda second-directional source plus H3/Z20 on the same reduced background."
            if passed else
            "Do not construct H3/Z20. Freeze the failing gate and localize any remaining initial-surface or reduced-dynamics inconsistency."
        ),
        "provenance":{
            "GE15_dense_sha256":dense_sha,
            "GE15_dense_hash_exact":dense_sha==dense_expected,
            "GE18_npz_sha256":ge18_npz_sha,
            "GE18_npz_hash_exact":ge18_npz_sha==r7.GE18_NPZ_SHA,
            "Repair12_parent_route":r12["routing"]["next_route"],
        },
        "claim_boundary":"Self-consistent reduced-background H1 Stage-A result only. No H3/Z20, finite eta, finite physical-amplitude nonlinear evolution, collapse, lensing or observational claim."
    }

    out=Path(args.json_out)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2,allow_nan=False)+"\n")

    save={
        "x64":np.asarray(base64["x"],float),
        "x32":np.asarray(base32["x"],float),
        "rho_lambda64":rho_l64,
        "rho_lambda32":rho_l32,
    }
    for tag in r7.C_TAGS:
        save[f"{tag}_H_reduced_primary"]=np.asarray(bg64[tag]["H"],float)
        save[f"{tag}_H_reduced_control"]=np.asarray(bg32[tag]["H"],float)
        save[f"{tag}_Z10_reduced_primary"]=h1_64[tag]
        save[f"{tag}_Z10_reduced_control"]=h1_32[tag]
        save[f"{tag}_Z10_reduced_dot_primary"]=dot_64[tag]
        save[f"{tag}_Z10_reduced_dot_control"]=dot_32[tag]
    np.savez_compressed(args.npz_out,**save)

    print(json.dumps(report,indent=2,allow_nan=False))


if __name__=="__main__":
    main()
