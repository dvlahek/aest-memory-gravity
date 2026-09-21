#!/usr/bin/env python3
"""GE19 Repair09 dual-constraint partition audit.

Diagnostic only.  Reuses the frozen Repair07 continuum operator, initial
surface and Radau scheme.  The only diagnostic change is to use the shift
constraint, instead of anisotropy, as the sixth canonical algebraic row and
then monitor anisotropy independently.
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

import ge09.repair01_dense_accepted_step_local_jet_bridge as g9

TINY=1.0e-300
LINEAR_MAX=1.0e-8
CONSTRAINT_MAX=1.0e-6
TIME_MAX=5.0e-3
INIT_MAX=1.0e-10
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


def alt_operator_matrices(r7,mod6,mod7,bg,tag,k,xq):
    """Shift-enforced alternative to Repair07's anisotropy-enforced partition."""
    Cmat,bp,base_diag=r7._local_linear_matrix(mod6,mod7,bg,tag,k,xq)

    # Four canonical momentum definitions + dust density + shift.
    Calg=np.vstack([
        Cmat[0:4],
        Cmat[5:6],
        Cmat[10:11]+Cmat[11:12],
    ])
    Az=Calg[:,r7._ZIDX]
    Aq=Calg[:,r7._QIDX]

    Ry=np.zeros((6,8),complex)
    Ry[0:4,4:8]=np.eye(4)
    Ry[:,0:4]-=Aq

    # Source order:
    # lapse, isotropic, aether, scalar, dust-potential, dust-density,
    # shift, anisotropy.
    Rr=np.zeros((6,8),complex)
    Rr[4,5]=1.0
    Rr[5,6]=1.0

    ZY,d1=r7._dense_equilibrated_solve(Az,Ry)
    ZR,d2=r7._dense_equilibrated_solve(Az,Rr)

    WY=np.zeros((10,8),complex)
    WR=np.zeros((10,8),complex)
    WY[r7._QIDX,0:4]=np.eye(4)
    WY[r7._ZIDX,:]=ZY
    WR[r7._ZIDX,:]=ZR

    M=np.zeros((8,8),complex)
    F=np.zeros((8,8),complex)
    M[0:4,:]=ZY[2:6,:]/bp["H"]
    F[0:4,:]=ZR[2:6,:]/bp["H"]

    dyn_rhs=np.zeros((4,8),complex)
    dyn_rhs[0,1]=1.0
    dyn_rhs[1,2]=1.0
    dyn_rhs[2,3]=1.0
    dyn_rhs[3,4]=1.0
    M[4:8,:]=(Cmat[6:10]@WY)/bp["H"]
    F[4:8,:]=(Cmat[6:10]@WR-dyn_rhs)/bp["H"]

    return M,F,ZY,ZR,WY,WR,Cmat,bp,{
        **base_diag,
        "algebraic_scaled_condition_2":float(max(
            d1["scaled_condition_2"],d2["scaled_condition_2"]
        )),
        "algebraic_scaled_residual_max":float(max(
            d1["scaled_relative_L2_residual_max"],
            d2["scaled_relative_L2_residual_max"],
        )),
        "algebraic_unscaled_matrix_product_residual_max":float(max(
            d1["unscaled_matrix_product_relative_L2_residual_max"],
            d2["unscaled_matrix_product_relative_L2_residual_max"],
        )),
    }


def integrate_alt(r7,mod6,mod7,bg,tag,k,y0,rhsfun,conrhsfun):
    x=np.asarray(bg["x"],float)
    Y0=np.asarray(y0,complex)
    if Y0.ndim==1:
        Y0=Y0[:,None]
    ncol=Y0.shape[1]
    Y=np.empty((ncol,8,len(x)),complex)
    Y[:,:,0]=Y0.T

    step_res=[]
    step_cond=[]
    local_cond=[]
    local_zero=[]

    a11=5.0/12.0; a12=-1.0/12.0
    a21=3.0/4.0; a22=1.0/4.0
    b1=3.0/4.0; b2=1.0/4.0
    c1=1.0/3.0

    cur=Y0.copy()
    I=np.eye(8,dtype=complex)

    for i in range(len(x)-1):
        h=float(x[i+1]-x[i])
        x1=float(x[i]+c1*h)
        x2=float(x[i+1])

        M1,Fmap1,*rest1=alt_operator_matrices(r7,mod6,mod7,bg,tag,k,x1)
        M2,Fmap2,*rest2=alt_operator_matrices(r7,mod6,mod7,bg,tag,k,x2)
        d1=rest1[-1]; d2=rest2[-1]
        local_cond.extend([d1["algebraic_scaled_condition_2"],d2["algebraic_scaled_condition_2"]])
        local_zero.extend([d1["raw_zero_output_abs_max"],d2["raw_zero_output_abs_max"]])

        R1=np.asarray(rhsfun(x1),complex)
        R2=np.asarray(rhsfun(x2),complex)
        C1=np.asarray(conrhsfun(x1),complex)
        C2=np.asarray(conrhsfun(x2),complex)
        if R1.ndim==1: R1=R1[:,None]
        if R2.ndim==1: R2=R2[:,None]
        if C1.ndim==1: C1=C1[:,None]
        if C2.ndim==1: C2=C2[:,None]
        S1=np.vstack([R1,C1])
        S2=np.vstack([R2,C2])
        F1=Fmap1@S1
        F2=Fmap2@S2

        K=np.block([
            [I-h*a11*M1, -h*a12*M2],
            [-h*a21*M1, I-h*a22*M2],
        ])
        RHS=np.vstack([
            cur+h*(a11*F1+a12*F2),
            cur+h*(a21*F1+a22*F2),
        ])
        stages,diag=r7._dense_equilibrated_solve(K,RHS)
        Y1=stages[:8]
        Y2=stages[8:]
        G1=M1@Y1+F1
        G2=M2@Y2+F2
        cur=cur+h*(b1*G1+b2*G2)
        Y[:,:,i+1]=cur.T

        step_res.append(diag["scaled_relative_L2_residual_max"])
        step_cond.append(diag["scaled_condition_2"])

    return Y,{
        "radau_block_scaled_relative_L2_residual_max":float(max(step_res,default=0.0)),
        "radau_scaled_condition_2_max":float(max(step_cond,default=0.0)),
        "local_algebraic_scaled_condition_2_max":float(max(local_cond,default=0.0)),
        "raw_zero_output_abs_max":float(max(local_zero,default=0.0)),
    }


def reconstruct_alt(r7,mod6,mod7,bg,tag,k,Y,rhsfun,conrhsfun):
    ncol,_,nt=Y.shape
    state=np.empty((ncol,6,nt),complex)
    dots=np.empty((ncol,4,nt),complex)

    alg_res=np.zeros(ncol,float)
    lapse_res=np.zeros(ncol,float)
    shift=np.zeros(ncol,float)
    aniso=np.zeros(ncol,float)
    shift_abs=np.zeros(ncol,float)
    aniso_abs=np.zeros(ncol,float)
    shift_scale=np.zeros(ncol,float)
    aniso_scale=np.zeros(ncol,float)
    local_cond=0.0

    for it,xq in enumerate(bg["x"]):
        rr=np.asarray(rhsfun(float(xq)),complex)
        rc=np.asarray(conrhsfun(float(xq)),complex)
        if rr.ndim==1: rr=rr[:,None]
        if rc.ndim==1: rc=rc[:,None]

        M,F,ZY,ZR,WY,WR,Cmat,bp,opdiag=alt_operator_matrices(
            r7,mod6,mod7,bg,tag,k,float(xq)
        )
        local_cond=max(local_cond,opdiag["algebraic_scaled_condition_2"])

        for j in range(ncol):
            y=Y[j,:,it]
            src=np.concatenate([rr[:,j],rc[:,j]])
            w=WY@y+WR@src
            z=w[r7._ZIDX]
            N,dr,Sdot,udot,phidot,Tdot=z
            S,u,phi,T=y[:4]
            state[j,:,it]=np.asarray([N,S,u,phi,T,dr],complex)
            dots[j,:,it]=np.asarray([Sdot,udot,phidot,Tdot],complex)

            Calg=np.vstack([
                Cmat[0:4],
                Cmat[5:6],
                Cmat[10:11]+Cmat[11:12],
            ])
            target=np.concatenate([y[4:8],[rr[5,j],rc[0,j]]])
            lhs=Calg@w
            rows=np.max(np.abs(Calg),axis=1)
            rs=(lhs-target)/np.maximum(rows,TINY)
            ls=lhs/np.maximum(rows,TINY)
            ts=target/np.maximum(rows,TINY)
            alg_res[j]=max(
                alg_res[j],
                float(np.linalg.norm(rs)/max(np.linalg.norm(ls),np.linalg.norm(ts),TINY))
            )

            lapse_lhs=Cmat[4]@w
            lapse_parts=max(
                abs(lapse_lhs),
                abs(rr[0,j]),
                np.max(np.abs(Cmat[4]))*max(np.max(np.abs(w)),TINY),
                TINY,
            )
            lapse_res[j]=max(
                lapse_res[j],
                float(abs(lapse_lhs-rr[0,j])/lapse_parts)
            )

            sga=Cmat[10]@w
            sm=Cmat[11]@w
            smet=r7._constraint_backward_error(
                Cmat[10]+Cmat[11],w,rc[0,j],sga,sm
            )
            shift[j]=max(shift[j],smet["metric"])
            shift_abs[j]=max(shift_abs[j],smet["absolute_residual"])
            shift_scale[j]=max(shift_scale[j],smet["scale"])

            aga=Cmat[12]@w
            am=Cmat[13]@w
            amet=r7._constraint_backward_error(
                Cmat[12]+Cmat[13],w,rc[1,j],aga,am
            )
            aniso[j]=max(aniso[j],amet["metric"])
            aniso_abs[j]=max(aniso_abs[j],amet["absolute_residual"])
            aniso_scale[j]=max(aniso_scale[j],amet["scale"])

    return state,dots,{
        "algebraic_scaled_relative_L2_residual_max":float(np.max(alg_res)),
        "lapse_noether_row_relative_residual_max":float(np.max(lapse_res)),
        "local_algebraic_scaled_condition_2_max":float(local_cond),
        "shift_constraint_relative_L2_max":float(np.max(shift)),
        "anisotropy_constraint_relative_L2_max":float(np.max(aniso)),
        "shift_constraint_absolute_residual_max":float(np.max(shift_abs)),
        "anisotropy_constraint_absolute_residual_max":float(np.max(aniso_abs)),
        "shift_constraint_row_scale_max":float(np.max(shift_scale)),
        "anisotropy_constraint_row_scale_max":float(np.max(aniso_scale)),
        "constraint_monitor_normalization":"componentwise_backward_error",
        "all_outputs_finite":bool(np.all(np.isfinite(state)) and np.all(np.isfinite(dots))),
    }


def solve_h1_alt(r7,mod6,mod7,bg,tag,reference,reference_dot):
    nt=len(bg["x"])
    state=np.empty((len(r7.FOURIER_N),6,nt),complex)
    dots=np.empty((len(r7.FOURIER_N),4,nt),complex)
    lin=[]; shift=[]; aniso=[]; init=[]; march=[]
    rhsfun,confun=r7._zero_source_interp(1)

    for ik,m in enumerate(r7.FOURIER_N):
        k=float(m*g9.K_REQ[0]/r7.FOURIER_N[0])
        q0=np.asarray(reference[ik,[1,2,3,4],0],complex)
        v0=np.asarray(reference_dot[ik,:,0],complex)

        # Initial surface remains exactly the frozen Repair07 construction:
        # lapse+dust-density determine N,dr before momenta are defined.
        y0,w0,idiag=r7._initial_canonical_state(
            mod6,mod7,bg,tag,k,float(bg["x"][0]),q0,v0,np.zeros(6,complex)
        )

        Y,rdiag=integrate_alt(
            r7,mod6,mod7,bg,tag,k,y0[:,None],rhsfun,confun
        )
        st,dd,odiag=reconstruct_alt(
            r7,mod6,mod7,bg,tag,k,Y,rhsfun,confun
        )
        state[ik]=st[0]
        dots[ik]=dd[0]

        lin.append(max(
            idiag["initial_algebraic_scaled_residual"],
            rdiag["radau_block_scaled_relative_L2_residual_max"],
            odiag["algebraic_scaled_relative_L2_residual_max"],
            odiag["lapse_noether_row_relative_residual_max"],
        ))
        shift.append(odiag["shift_constraint_relative_L2_max"])
        aniso.append(odiag["anisotropy_constraint_relative_L2_max"])

        for j in range(4):
            init.append(r7.aor([state[ik,j+1,0]],[q0[j]]))
            init.append(r7.aor([dots[ik,j,0]],[v0[j]]))

        march.append({"m":int(m),**idiag,**rdiag,**odiag})

    return state,dots,{
        "linear_system_relative_L2_max":float(max(lin,default=math.inf)),
        "shift_constraint_relative_L2_max":float(max(shift,default=math.inf)),
        "anisotropy_constraint_relative_L2_max":float(max(aniso,default=math.inf)),
        "initial_dynamic_match_abs_or_rel_max":float(max(init,default=math.inf)),
        "all_outputs_finite":bool(np.all(np.isfinite(state)) and np.all(np.isfinite(dots))),
        "canonical_march_diagnostics":march,
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--results-dir",default=str(ROOT/"results"))
    ap.add_argument("--json-out",required=True)
    args=ap.parse_args()
    rd=Path(args.results_dir)

    required=[
        rd/"ge15_R1_dense_accepted_step_trace.dat",
        rd/"ge15_cancellation_free_s_state_precision_closure.json",
        rd/"ge18_repair01_on_shell_matched_dust_first_order_bridge.json",
        rd/"ge18_repair01_on_shell_matched_dust_first_order_bridge.npz",
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

    r7=load_module(
        ROOT/"ge19/repair07_window_retarded_reduced_h3_z20_particular.py",
        "ge19_repair07_for_repair09",
    )

    ge15=json.loads((rd/"ge15_cancellation_free_s_state_precision_closure.json").read_text())
    ge18=json.loads((rd/"ge18_repair01_on_shell_matched_dust_first_order_bridge.json").read_text())
    if ge15.get("classification")!="GE15_CANCELLATION_FREE_S_STATE_PRECISION_CLOSURE_PASS":
        raise RuntimeError("GE15 parent is not PASS")
    if ge18.get("classification")!="GE18_REPAIR01_ON_SHELL_MATCHED_DUST_FIRST_ORDER_BRIDGE_PASS":
        raise RuntimeError("GE18 Repair01 parent is not PASS")

    dense=rd/"ge15_R1_dense_accepted_step_trace.dat"
    if sha256(dense)!=ge15["precision_binding"]["dense_trace_sha256"]["R1"]:
        raise RuntimeError("GE15 dense hash mismatch")

    npz_path=rd/"ge18_repair01_on_shell_matched_dust_first_order_bridge.npz"
    if sha256(npz_path)!=r7.GE18_NPZ_SHA:
        raise RuntimeError("GE18 NPZ hash mismatch")
    npz=np.load(npz_path)

    mod6_frozen=r7.load_frozen_generator(
        ROOT/"ge06/analytic_aest_directional_source_generator.py",
        "ge19r9_ge06",
    )
    mod6=r7.build_stable_ge06_generator_v2(mod6_frozen)
    mod7=r7.load_frozen_generator(
        ROOT/"ge07/pressureless_matter_directional_source_generator.py",
        "ge19r9_ge07",
    )

    bg64,_,jets64=r7.build_ge15_reference(dense,r7.NT_PRIMARY)
    bg32,_,jets32=r7.build_ge15_reference(dense,r7.NT_CONTROL)

    rows=[]
    time_rows=[]
    sysmax=0.0
    shiftmax=0.0
    anisomax=0.0
    initmax=0.0
    timemax=0.0
    finite=True

    for tag in r7.C_TAGS:
        ref64,dref64=r7.reference_reduced_mode_state(bg64,jets64,npz,tag)
        ref32,dref32=r7.reference_reduced_mode_state(bg32,jets32,npz,tag)

        st64,dot64,c64=solve_h1_alt(
            r7,mod6,mod7,bg64,tag,ref64,dref64
        )
        st32,dot32,c32=solve_h1_alt(
            r7,mod6,mod7,bg32,tag,ref32,dref32
        )
        tc=r7.reduced_h1_time_control(bg64["x"],st64,bg32["x"],st32)

        rows.append({"C":tag,"primary":c64,"control":c32})
        time_rows.append({"C":tag,**tc})

        sysmax=max(sysmax,c64["linear_system_relative_L2_max"],c32["linear_system_relative_L2_max"])
        shiftmax=max(shiftmax,c64["shift_constraint_relative_L2_max"],c32["shift_constraint_relative_L2_max"])
        anisomax=max(anisomax,c64["anisotropy_constraint_relative_L2_max"],c32["anisotropy_constraint_relative_L2_max"])
        initmax=max(initmax,c64["initial_dynamic_match_abs_or_rel_max"],c32["initial_dynamic_match_abs_or_rel_max"])
        timemax=max(timemax,tc["max"])
        finite=bool(finite and c64["all_outputs_finite"] and c32["all_outputs_finite"])

    numerical_healthy=bool(
        sysmax<=LINEAR_MAX
        and timemax<=TIME_MAX
        and initmax<=INIT_MAX
        and finite
    )

    if numerical_healthy and shiftmax<=CONSTRAINT_MAX and anisomax<=CONSTRAINT_MAX:
        route="DAE_PARTITION_DEFECT_LOCALIZED"
    elif numerical_healthy and shiftmax<=CONSTRAINT_MAX and anisomax>CONSTRAINT_MAX:
        route="REDUCED_BACKGROUND_CONSTRAINT_INCOMPATIBILITY_CONFIRMED"
    elif not numerical_healthy or shiftmax>CONSTRAINT_MAX:
        route="ALTERNATE_PARTITION_NUMERICAL_FAIL"
    else:
        route="DUAL_PARTITION_RESULT_AMBIGUOUS"

    report={
        "classification":"GE19_REPAIR09_DUAL_CONSTRAINT_PARTITION_AUDIT_COMPLETE",
        "predata_classification":"GE19_REPAIR09_PREDATA_DUAL_CONSTRAINT_PARTITION_AUDIT",
        "diagnostic_only":True,
        "repair08_result_sha256":r8sha,
        "historical_repair07_shift_max":r8["global"]["canonical_repair07_shift_backward_error_max"],
        "alternative_partition":"canonical momentum definitions + dust density + shift; anisotropy independently monitored",
        "global":{
            "linear_system_relative_L2_max":sysmax,
            "shift_constraint_backward_error_max":shiftmax,
            "anisotropy_constraint_backward_error_max":anisomax,
            "initial_dynamic_match_abs_or_rel_max":initmax,
            "primary64_vs_control32_state_global_relative_L2_max":timemax,
            "all_outputs_finite":finite,
        },
        "reference_thresholds":{
            "linear_system_relative_L2_residual_max":LINEAR_MAX,
            "shift_constraint_backward_error_max":CONSTRAINT_MAX,
            "anisotropy_constraint_backward_error_max":CONSTRAINT_MAX,
            "primary64_vs_control32_state_global_relative_L2_max":TIME_MAX,
            "initial_dynamic_match_abs_or_rel_max":INIT_MAX,
        },
        "routing":{
            "numerical_controls_healthy":numerical_healthy,
            "next_route":route,
        },
        "rows":rows,
        "time_control":time_rows,
        "claim_boundary":"Diagnostic reduced-H1 partition audit only. No equation, sign, threshold, background, reduced-matter model or H3/Z20 result is changed or licensed."
    }

    out=Path(args.json_out)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2,allow_nan=False)+"\n")
    print(json.dumps(report,indent=2,allow_nan=False))


if __name__=="__main__":
    main()
