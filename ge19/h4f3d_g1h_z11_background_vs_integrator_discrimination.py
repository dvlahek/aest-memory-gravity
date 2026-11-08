#!/usr/bin/env python3
"""GE19 G1H — isolate offclock action background from integrator in Z11 IVP.

Two matched DOP853 solves on ONE frozen C_star/m20 case. Only the
background continuation changes: original Repair32B _bg_point PCHIP vs
source-identical D17 action-charge/Lambda function. Same original canonical
Cmat, same frozen Repair32B PCHIP GE05 source, same nodal initial data,
same numerical integrator and tolerances. Read-only original inputs.
A discrepancy is a numerical diagnostic, not a validated interval bound.
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

from ge19 import h4f3d_g1e_z11_original_action_euler_offclock as g1e
from ge19 import h4f3d17_actual_original_action_dense_canonical_H1 as d17
from ge19 import repair32b_factor2_corrected_reduced_h2_z11_reconstruction as r32b

ROOT=Path(__file__).resolve().parents[1]
MODES=g1e.MODES
TINY=1e-300
SOURCES={
  "ge19/h4f3d_g1g_independent_action_z11_ivp.py":
      "3575a11e5d4bbddbce5bc8a052129c6c0c553808",
  "ge19/h4f3d_g1e_z11_original_action_euler_offclock.py":
      "017ddec6b52434920f394a728a994f017af62dd9",
  "ge19/repair32b_factor2_corrected_reduced_h2_z11_reconstruction.py":
      "6ece578e8a30f48faaded8808687a9bd5c114608",
  "ge19/repair07_window_retarded_reduced_h3_z20_particular.py":
      "e34d28a2062c748f48bc82fa928844b02631de25",
}

def need(ok,msg):
    if not bool(ok):
        raise RuntimeError("GE19_G1H_"+msg)

def sha(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for b in iter(lambda:f.read(1048576),b""):
            h.update(b)
    return h.hexdigest()

def checked_sources():
    ret=g1e.pin_sources()
    for path,want in SOURCES.items():
        g=subprocess.check_output(["git","rev-parse","HEAD:"+path],cwd=ROOT,text=True).strip()
        f=subprocess.check_output(["git","hash-object",str(ROOT/path)],cwd=ROOT,text=True).strip()
        need(g==want and f==want,"SOURCE_PIN_"+path+"_"+g)
        ret[path]=want
    need(r32b.RAW_RESIDUAL_DICTIONARY_SCALE==2.,
         "ORIGINAL_M1_FACTOR_TWO_CHANGED")
    return ret

def comparison(a,b):
    a=np.asarray(a,complex);b=np.asarray(b,complex)
    need(a.shape==b.shape and a.size>0 and np.isfinite(a).all()
         and np.isfinite(b).all(),"INVALID_COMPARE")
    d=a-b
    return {
      "global_relative_L2":float(np.linalg.norm(d)/max(
          np.linalg.norm(a),np.linalg.norm(b),TINY)),
      "max_abs":float(np.max(np.abs(d))),
      "initial_max_abs":float(np.max(np.abs(d[...,0]))),
      "endpoint_max_abs":float(np.max(np.abs(d[...,-1]))),
      "per_physical_field_max_abs":[float(np.max(np.abs(d[i]))) for i in range(a.shape[0])]
         if a.ndim==2 else None
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--results-dir",type=Path,default=ROOT/"results")
    ap.add_argument("--tag",choices=g1e.TAGS,default="C_star")
    ap.add_argument("--grid",choices=g1e.GRIDS.keys(),default="primary")
    ap.add_argument("--mode",type=int,choices=MODES,default=20)
    ap.add_argument("--rtol",type=float,default=1e-11)
    ap.add_argument("--atol",type=float,default=1e-13)
    ap.add_argument("--max-step-factor",type=float,default=1.)
    ap.add_argument("--json-out",type=Path,required=True)
    a=ap.parse_args()
    need(not a.json_out.exists(),"REFUSE_OVERWRITE")
    need(math.isfinite(a.rtol) and 0<a.rtol<=1e-8
         and math.isfinite(a.atol) and 0<a.atol<=1e-10
         and math.isfinite(a.max_step_factor) and
         0<a.max_step_factor<=4,"TOLERANCE_OR_STEP_INVALID")
    pins=checked_sources()
    files=g1e.files(a.results_dir)
    d15=d17.d16r1.d15
    old=d15.d13.old
    r7=old.r7
    need(tuple(map(int,r7.FOURIER_N))==MODES,"FOURIER_MODES_CHANGED")
    nt=g1e.GRIDS[a.grid]
    ix=MODES.index(a.mode)
    k=float(a.mode*r7.g9.K_REQ[0]/r7.FOURIER_N[0])
    with np.load(files["r13"],allow_pickle=False) as z13,\
         np.load(files["z11"],allow_pickle=False) as data:
        bgs,_,mod6,mod7,_,_,_,_,_=old.build_context(a.results_dir,z13)
        bg=bgs[(nt,a.tag)]
        x=np.asarray(bg["x"],float)
        need(x.shape==(nt,) and np.array_equal(x,np.asarray(
             data["x_"+a.grid],float)) and
             np.all(np.diff(x)>0),"FROZEN_CLOCK_CHANGED")
        state_ref=np.asarray(data[f"{a.tag}_Z11_{a.grid}"],complex)[ix]
        dot_ref=np.asarray(data[f"{a.tag}_Z11dot_{a.grid}"],complex)[ix]
        B_all=np.asarray(data[f"{a.tag}_B10_{a.grid}"],complex)
        B=B_all[ix]
        all_rhs=np.asarray(data[f"{a.tag}_M1_rhs_{a.grid}"],complex)
        rhs_nodes=all_rhs[ix]
        need(state_ref.shape==(6,nt) and dot_ref.shape==(4,nt)
             and B.shape==(nt,) and rhs_nodes.shape==(6,nt),
             "FROZEN_PARENT_SHAPE_CHANGED")
        need(np.isfinite(state_ref).all() and
             np.isfinite(dot_ref).all() and
             np.isfinite(rhs_nodes).all(),"NONFINITE_FROZEN_PARENT")
        need(np.array_equal(rhs_nodes,r32b.source_from_B(bg,B_all)[ix]),
             "FROZEN_GE05_SOURCE_CHANGED")
        src_interp=g1e.cpchip(x,rhs_nodes)
        def force(t):
            out=np.zeros(8,complex)
            out[:6]=np.asarray(g1e.c_eval(src_interp,float(t)),complex)
            return out

        action_H,_=d15.clk.make_original_action_background(r7,bg,a.tag)
        action=d17.core.ActionBackground(r7,bg,action_H)
        original_callback=r7._bg_point
        original_cache=r7._CANONICAL_LOCAL_CACHE
        max_step=float(np.min(np.diff(x))*a.max_step_factor)
        outputs={}
        try:
            action.knot_check()
            for label,callback in (
                ("original_repair32b_background_PCHIP",original_callback),
                ("source_action_charge_background",lambda context,t:action(context,float(t))),
            ):
                r7._bg_point=callback
                r7._CANONICAL_LOCAL_CACHE={}
                q0=state_ref[[1,2,3,4],0]
                v0=dot_ref[:,0]
                y0,w0,idg=r7._initial_canonical_state(
                  mod6,mod7,bg,a.tag,k,float(x[0]),q0,v0,
                  force(float(x[0]))[:6])
                count=[0]
                def rhs(t,y):
                    M,F,*_ = r7._canonical_operator_matrices(
                        mod6,mod7,bg,a.tag,k,float(t))
                    count[0]+=1
                    return M@y+F@force(t)
                sol=solve_ivp(rhs,(float(x[0]),float(x[-1])),
                    np.asarray(y0,complex),method="DOP853",t_eval=x,
                    rtol=a.rtol,atol=a.atol,max_step=max_step)
                need(sol.success and sol.y.shape==(8,nt) and
                     np.isfinite(sol.y).all(),
                     "DOP853_"+label+"_"+str(sol.message))
                fields=np.empty((6,nt),complex)
                dots=np.empty((4,nt),complex)
                max_const=0.
                max_euler=0.
                for j,t in enumerate(x):
                    M,F,ZY,ZR,WY,WR,Cmat,bp,_=(
                        r7._canonical_operator_matrices(
                        mod6,mod7,bg,a.tag,k,float(t)))
                    src=force(t)
                    w=WY@sol.y[:,j]+WR@src
                    fields[:,j]=np.r_[w[0],sol.y[:4,j],w[1]]
                    dots[:,j]=w[6:10]
                    max_const=max(max_const,float(np.max(np.abs(
                        Cmat[0:4]@w-sol.y[4:8,j]))))
                    yp=M@sol.y[:,j]+F@src
                    residual=np.zeros(8,complex)
                    residual[0]=Cmat[4]@w-src[0]
                    residual[1:5]=Cmat[6:10]@w-bp["H"]*yp[4:8]-src[1:5]
                    residual[5]=Cmat[5]@w-src[5]
                    residual[6]=(Cmat[10]+Cmat[11])@w
                    residual[7]=(Cmat[12]+Cmat[13])@w
                    max_euler=max(max_euler,float(np.max(np.abs(residual))))
                outputs[label]={
                  "initial_canonical_y0":y0,
                  "canonical":sol.y,
                  "fields":fields,
                  "dots":dots,
                  "stats":{
                    "nfev":int(sol.nfev),"status":int(sol.status),
                    "initial_algebraic_scaled_residual":
                        float(idg["initial_algebraic_scaled_residual"]),
                    "max_reconstructed_nodal_constitutive_residual":max_const,
                    "max_reconstructed_nodal_euler_row_absolute":max_euler,
                    "Z11_fields_vs_frozen_Repair32B":comparison(fields,state_ref),
                    "Z11dot_vs_frozen_Repair32B":comparison(dots,dot_ref),
                  }
                }
                print("GE19_G1H "+label+" nfev="+str(sol.nfev)+
                  " frozen_Z11_rel="+format(
                    outputs[label]["stats"]["Z11_fields_vs_frozen_Repair32B"]["global_relative_L2"],".9g"),
                  flush=True)
            # Optional direct operator comparison at 3 fixed offclock points:
            probes=[]
            for step in (0,(nt-2)//2,nt-2):
                t=float(0.5*(x[step]+x[step+1]))
                r7._CANONICAL_LOCAL_CACHE={}
                r7._bg_point=original_callback
                M0,F0,*_=r7._canonical_operator_matrices(
                     mod6,mod7,bg,a.tag,k,t)
                r7._CANONICAL_LOCAL_CACHE={}
                r7._bg_point=lambda context,q:action(context,float(q))
                M1,F1,*_=r7._canonical_operator_matrices(
                     mod6,mod7,bg,a.tag,k,t)
                probes.append({
                   "coarse_interval":int(step),
                   "relative_M_matrix_change":
                       float(np.linalg.norm(M1-M0)/max(
                             np.linalg.norm(M1),np.linalg.norm(M0),TINY)),
                   "relative_F_map_change":
                       float(np.linalg.norm(F1-F0)/max(
                             np.linalg.norm(F1),np.linalg.norm(F0),TINY)),
                })
            p=outputs["original_repair32b_background_PCHIP"]
            q=outputs["source_action_charge_background"]
            report={
              "classification":
                "GE19_G1H_MATCHED_DOP853_Z11_BACKGROUND_DISCRIMINATION_COMPLETED_PHYSICAL_G1_OPEN",
              "scope":{"C":a.tag,"grid":a.grid,"Nt":nt,
                        "mode":a.mode,"k":k,
                        "integrator":"DOP853","rtol":a.rtol,
                        "atol":a.atol,"max_step":max_step,
                        "original_frozen_GE05_PCHIP_source_shared":True,
                        "original_initial_physical_data_shared":True},
              "inputs_sha256":{name:sha(path) for name,path in files.items()},
              "original_source_pins":pins,
              "initial_canonical_state_action_vs_PCHIP":comparison(
                   q["initial_canonical_y0"][:,None],
                   p["initial_canonical_y0"][:,None]),
              "PCHIP_background_DOP853":p["stats"],
              "ACTION_background_DOP853":q["stats"],
              "ACTION_vs_PCHIP_DOP853_canonical":comparison(
                    q["canonical"],p["canonical"]),
              "ACTION_vs_PCHIP_DOP853_fields":comparison(
                    q["fields"],p["fields"]),
              "ACTION_vs_PCHIP_DOP853_Z11dot":comparison(
                    q["dots"],p["dots"]),
              "offclock_operator_background_probes_sampled":probes,
              "true_continuous_Z11_error_enclosed":False,
              "physical_GE05_true_B10_error_certified":False,
              "G1_PHYSICAL_CLOSED":False,
              "G3_B_total_frozen":False,
              "full_H4_Ward_certified":False,
              "Z21_certified":False,
              "lensing_licensed":False,
              "interpretation_boundary":"Two DOP853 solves with same original GE06/GE07/Lambda Cmat, "
                "original frozen Repair32B M1 source PCHIP, initial physical fields, "
                "tolerances, and output clock. Only offclock background evaluation "
                "differs: original frozen PCHIP versus independent scalar charge/Lambda "
                "action continuation. This isolates a numerical background model "
                "difference from a cross-integrator discrepancy, but does not "
                "establish Radau or DOP853 true-error bounds or rigorous interval "
                "Euler enclosure. Original H4 science gates unchanged."
            }
        finally:
            r7._bg_point=original_callback
            r7._CANONICAL_LOCAL_CACHE=original_cache
    a.json_out.parent.mkdir(parents=True,exist_ok=True)
    a.json_out.write_text(json.dumps(report,indent=2,sort_keys=True,
                                     allow_nan=False)+"\n")
    print(report["classification"],flush=True)

if __name__=="__main__":
    main()
