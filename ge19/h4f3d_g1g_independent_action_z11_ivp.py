#!/usr/bin/env python3
"""GE19 G1G: independent DOP853 original-action forced canonical Z11 IVP.

Solve a NEW eight-dimensional canonical first-order Z11 IVP for a chosen
frozen Fourier mode with the *unchanged* Repair32B GE05 M1 PCHIP source,
the original Repair13 action background from D17, and exactly the frozen
GE06+GE07+Lambda canonical action matrices. Compare against frozen
Repair32B's Radau state on the original time nodes. One physically useful
cross-integrator check, NOT a validated-interval certification, NOT a
replacement for an original frozen result and NOT an H4 Ward evaluation.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import subprocess
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp

from ge19 import h4f3d17_actual_original_action_dense_canonical_H1 as d17
from ge19 import h4f3d_g1e_z11_original_action_euler_offclock as g1e
from ge19 import repair32b_factor2_corrected_reduced_h2_z11_reconstruction as r32b

ROOT=Path(__file__).resolve().parents[1]
TINY=1e-300
PINS={
 "ge19/h4f3d17_actual_original_action_dense_canonical_H1.py":
    "813c350d1d1860515997ce43f223b9b6bc2091e9",
 "ge19/h4f3d17_original_action_dense_H1_core.py":
    "6074d31050450440654bdc55980a13584d5ce5ee",
 "ge19/repair32b_factor2_corrected_reduced_h2_z11_reconstruction.py":
    "6ece578e8a30f48faaded8808687a9bd5c114608",
 "ge19/repair07_window_retarded_reduced_h3_z20_particular.py":
    "e34d28a2062c748f48bc82fa928844b02631de25",
 "ge19/h4f3d_g1e_z11_original_action_euler_offclock.py":
    "017ddec6b52434920f394a728a994f017af62dd9",
}

def require(test,msg):
    if not bool(test):raise RuntimeError("GE19_G1G_"+msg)

def sha(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda:f.read(1<<20),b""):h.update(block)
    return h.hexdigest()

def locks():
    out=g1e.pin_sources()
    for path,want in PINS.items():
        commit=subprocess.check_output(["git","rev-parse","HEAD:"+path],
                                       cwd=ROOT,text=True).strip()
        work=subprocess.check_output(["git","hash-object",str(ROOT/path)],
                                     cwd=ROOT,text=True).strip()
        require(commit==work==want,"SOURCE_PIN_CHANGED_"+path)
        out[path]=want
    require(r32b.RAW_RESIDUAL_DICTIONARY_SCALE==2.0,
            "GE05_FACTOR_TWO_CHANGED")
    return out

def metric(a,b):
    a=np.asarray(a,complex);b=np.asarray(b,complex)
    require(a.shape==b.shape,"SHAPE_MISMATCH")
    require(np.isfinite(a).all() and np.isfinite(b).all(),
            "NONFINITE_COMPARE")
    d=a-b
    return {"global_relative_L2":float(
                np.linalg.norm(d)/max(np.linalg.norm(a),np.linalg.norm(b),TINY)),
            "max_abs":float(np.max(np.abs(d))),
            "endpoint_max_abs":float(np.max(np.abs(d[..., -1]))),
            "initial_max_abs":float(np.max(np.abs(d[..., 0])))}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--results-dir",type=Path,default=ROOT/"results")
    ap.add_argument("--tag",choices=g1e.TAGS,default="C_star")
    ap.add_argument("--grid",choices=g1e.GRIDS.keys(),default="primary")
    ap.add_argument("--mode",type=int,choices=g1e.MODES,default=20)
    ap.add_argument("--rtol",type=float,default=1e-11)
    ap.add_argument("--atol",type=float,default=1e-13)
    ap.add_argument("--max-step-factor",type=float,default=1.0)
    ap.add_argument("--json-out",required=True,type=Path)
    args=ap.parse_args()
    require(not args.json_out.exists(),"REFUSE_OVERWRITE")
    require(math.isfinite(args.rtol) and 0<args.rtol<=1e-8 and
            math.isfinite(args.atol) and 0<args.atol<=1e-10,
            "INVALID_PREDECLARED_NUMERIC_TOLERANCES")
    require(math.isfinite(args.max_step_factor) and
            0<args.max_step_factor<=4,
            "INVALID_MAX_STEP_FACTOR")
    pins=locks()
    paths=g1e.files(args.results_dir)
    nt=g1e.GRIDS[args.grid]
    d15=d17.d16r1.d15
    old=d15.d13.old
    r7=old.r7
    require(tuple(map(int,r7.FOURIER_N))==g1e.MODES,
            "FOURIER_MODE_SET_CHANGED")
    im=g1e.MODES.index(args.mode)
    k=float(args.mode*r7.g9.K_REQ[0]/r7.FOURIER_N[0])
    with np.load(paths["r13"],allow_pickle=False) as r13,\
         np.load(paths["z11"],allow_pickle=False) as z:
        bgs,_,mod6,mod7,_,_,_,_,_=old.build_context(
            args.results_dir,r13)
        bg=bgs[(nt,args.tag)]
        x=np.asarray(bg["x"],float)
        require(x.shape==(nt,) and np.all(np.diff(x)>0),
                "NONMONOTONE_CLOCK")
        require(np.array_equal(x,np.asarray(z["x_"+args.grid],float)),
                "FROZEN_Z11_CLOCK_MISMATCH")
        saved=np.asarray(z[f"{args.tag}_Z11_{args.grid}"],complex)[im]
        saved_dot=np.asarray(z[f"{args.tag}_Z11dot_{args.grid}"],complex)[im]
        B=np.asarray(z[f"{args.tag}_B10_{args.grid}"],complex)[im]
        raw=np.asarray(z[f"{args.tag}_M1_rhs_{args.grid}"],complex)[im]
        require(saved.shape==(6,nt) and saved_dot.shape==(4,nt)
                and B.shape==(nt,) and raw.shape==(6,nt),
                "ORIGINAL_Z11_SOURCE_SHAPES_CHANGED")
        require(all(np.isfinite(v).all() for v in
                    (saved,saved_dot,B,raw)),"NONFINITE_ORIGINAL_Z11")
        # Frozen exact factor-two source identity at saved knots:
        actual=r32b.source_from_B(bg,
            np.asarray(z[f"{args.tag}_B10_{args.grid}"],complex))[im]
        source_exact=metric(raw,actual)
        require(source_exact["max_abs"]==0.,
                "ORIGINAL_RAW_GE05_SOURCE_CHANGED")
        rinterp=g1e.cpchip(x,raw)
        binterp=g1e.cpchip(x,B)

        def raw_rhs(t):
            v=np.asarray(g1e.c_eval(rinterp,t),complex)
            require(v.shape==(6,),"SOURCE_INTERPOLANT_SHAPE")
            return v

        # Original D17 shared action: Q,KQ,Z from scalar charge and H from
        # independently source-derived GE15/Repair13 Lambda continuation.
        h_eval,_=d15.clk.make_original_action_background(
            r7,bg,args.tag)
        action=d17.core.ActionBackground(r7,bg,h_eval)
        orig_bgpoint=r7._bg_point
        orig_cache=r7._CANONICAL_LOCAL_CACHE
        r7._CANONICAL_LOCAL_CACHE={}
        r7._bg_point=lambda background,t:action(background,float(t))
        try:
            action.knot_check()
            q0=np.asarray(saved[[1,2,3,4],0],complex)
            v0=np.asarray(saved_dot[:,0],complex)
            y0,w0,initial=r7._initial_canonical_state(
                mod6,mod7,bg,args.tag,k,float(x[0]),q0,v0,
                raw_rhs(float(x[0])))
            rhs_guard={"n":0,"max_local_cmat_offset_abs":0.,
                       "max_operator_cond_report_only":0.,
                       "max_force_representation_relative_sampled":0.,
                       "max_force_representation_absolute_sampled":0.}

            def evaluate(t,yy):
                M,F,ZY,ZR,WY,WR,Cmat,bp,diag=(
                    r7._canonical_operator_matrices(
                    mod6,mod7,bg,args.tag,k,float(t)))
                source=np.zeros(8,complex)
                source[:6]=raw_rhs(float(t))
                rhs_guard["n"]+=1
                rhs_guard["max_local_cmat_offset_abs"]=max(
                    rhs_guard["max_local_cmat_offset_abs"],
                    float(diag["raw_zero_output_abs_max"]))
                rhs_guard["max_operator_cond_report_only"]=max(
                    rhs_guard["max_operator_cond_report_only"],
                    float(diag["algebraic_scaled_condition_2"]))
                native=source[:6]
                Bq=complex(g1e.c_eval(binterp,float(t)))
                action_src=np.zeros(6,complex)
                action_src[2]=bp["a"]**3*bp["Q_action"]*Bq
                action_src[3]=-1j*k*bp["a"]**2*Bq
                gap=float(np.linalg.norm(native-action_src))
                scale=max(np.linalg.norm(native),
                          np.linalg.norm(action_src),TINY)
                rhs_guard["max_force_representation_relative_sampled"]=max(
                    rhs_guard["max_force_representation_relative_sampled"],
                    gap/scale)
                rhs_guard["max_force_representation_absolute_sampled"]=max(
                    rhs_guard["max_force_representation_absolute_sampled"],
                    gap)
                return M@yy+F@source

            max_step=float(np.min(np.diff(x))*args.max_step_factor)
            solution=solve_ivp(
                evaluate,(float(x[0]),float(x[-1])),
                np.asarray(y0,complex),method="DOP853",
                t_eval=x,rtol=args.rtol,atol=args.atol,
                max_step=max_step,dense_output=False)
            require(solution.success,
                    "DOP853_FAILED_"+str(solution.message))
            require(solution.y.shape==(8,nt) and
                    np.isfinite(solution.y).all(),
                    "NONFINITE_INDEPENDENT_IVP")
            state=np.empty((6,nt),complex)
            dot=np.empty((4,nt),complex)
            mainres=np.zeros((8,nt),complex)
            momdiff=np.empty((nt,),float)
            for j,t in enumerate(x):
                M,F,ZY,ZR,WY,WR,Cmat,bp,_=(
                  r7._canonical_operator_matrices(
                  mod6,mod7,bg,args.tag,k,float(t)))
                source=np.zeros(8,complex)
                source[:6]=raw_rhs(float(t))
                y=solution.y[:,j]
                w=WY@y+WR@source
                state[:,j]=np.r_[w[0],y[:4],w[1]]
                dot[:,j]=w[6:10]
                momdiff[j]=float(np.linalg.norm(
                    Cmat[0:4]@w-y[4:8]))
                momx=(M@y+F@source)[4:8]
                mainres[0,j]=Cmat[4]@w-source[0]
                mainres[1:5,j]=Cmat[6:10]@w-bp["H"]*momx-source[1:5]
                mainres[5,j]=Cmat[5]@w-source[5]
                mainres[6,j]=(Cmat[10]+Cmat[11])@w
                mainres[7,j]=(Cmat[12]+Cmat[13])@w
            report={
               "classification":
                  "GE19_G1G_DOP853_ORIGINAL_ACTION_FORCED_Z11_INDEPENDENT_IVP_COMPLETED_CONTINUOUS_G1_OPEN",
               "scope":{"tag":args.tag,"grid":args.grid,"Nt":nt,
                  "mode":args.mode,"k":k,
                  "canonical_IVP":"8D original GE06+GE07+Lambda with frozen Repair32B M1 PCHIP source",
                  "action_background":
                      "exact scalar charge/Exp branch and original Lambda H from D15a",
                  "independent_integrator":"scipy.integrate.solve_ivp(DOP853)",
                  "rtol":args.rtol,"atol":args.atol,
                  "max_step":max_step,
                  "no_source_or_parent_replacement":True},
               "original_source_pins":pins,
               "frozen_inputs_sha256":{key:sha(p) for key,p in paths.items()},
               "frozen_Z11_M1_source_exact_at_knots":source_exact,
               "integration":{"nfev":int(solution.nfev),
                  "n_step_nodes":nt,"success":bool(solution.success),
                  "status":int(solution.status),
                  "message":str(solution.message),
                  "initial_algebraic_scaled_residual":
                      initial["initial_algebraic_scaled_residual"],
                  **rhs_guard},
               "DOP853_vs_frozen_Repair32B_Z11_fields":metric(state,saved),
               "DOP853_vs_frozen_Repair32B_Z11_time_derivatives":
                  metric(dot,saved_dot),
               "DOP853_vs_frozen_dynamic_fields":
                  metric(state[[1,2,3,4],:],saved[[1,2,3,4],:]),
               "DOP853_vs_frozen_lapse_dust":
                  metric(state[[0,5],:],saved[[0,5],:]),
               "DOP853_original_action_8_row_max_abs_at_original_knots":
                  float(np.max(np.abs(mainres))),
               "DOP853_original_action_8_row_L2_max_at_original_knots":
                  float(np.max(np.linalg.norm(mainres,axis=0))),
               "DOP853_canonical_momentum_relation_max_abs_at_knots":
                  float(np.max(momdiff)),
               "DOP853_true_solution_error_certified":False,
               "physical_GE05_B10_source_error_certified":False,
               "original_Z11_continuous_Euler_enclosed":False,
               "G1_PHYSICAL_CLOSED":False,
               "G3_B_total_frozen":False,
               "full_H4_Ward_certified":False,
               "Z21_certified":False,
               "lensing_licensed":False,
               "claim_boundary":"Independent higher-order approximate IVP with original action coefficient and unchanged frozen PCHIP GE05 source compared to original frozen Repair32B Radau solution. DOP853 solver local rtol/atol and small Cmat backward errors are NOT interval or theorem bounds for the full Euler DAE; both solvers use same original operator model, while background offclock continuation differs. Reconstructed canonical equation checks at solver knots are algebraic by construction, not independent exact-solution evidence. Missing historical D47 m20 remains missing. No H4 Ward, no Z21 and no observational tuning."
            }
        finally:
            r7._bg_point=orig_bgpoint
            r7._CANONICAL_LOCAL_CACHE=orig_cache
    args.json_out.parent.mkdir(parents=True,exist_ok=True)
    args.json_out.write_text(json.dumps(report,sort_keys=True,
                                    indent=2,allow_nan=False)+"\n")
    print(f"GE19_G1G m={args.mode} IVP nfev={solution.nfev} "
          f"Z11_rel={report['DOP853_vs_frozen_Repair32B_Z11_fields']['global_relative_L2']:.9g} "
          f"Z11_abs_max={report['DOP853_vs_frozen_Repair32B_Z11_fields']['max_abs']:.9g}",
          flush=True)
    print(report["classification"],flush=True)

if __name__=="__main__":
    main()
