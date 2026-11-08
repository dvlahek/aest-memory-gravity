#!/usr/bin/env python3
"""GE19 G1F: isolate canonical momentum reconstruction in G1E original-action Euler.

Compare three precisely defined offclock Z11 surrogates without integrating
Z11 or altering its frozen source: original PCHIP(p)+PCHIP(M1), nodal-Euler
Hermite(p)+PCHIP(M1), nodal-Euler Hermite(p)+action(B10).

This is a sampled physical first-order Euler diagnostic. The Hermite endpoint
derivative is constrained by the frozen nodal Euler RHS by construction:
zero or small endpoint defects MUST NOT be presented as independent evidence
of an exact action solution or as a rigorous interval certificate.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
from pathlib import Path

import numpy as np

from ge19 import h4f3d_g1e_z11_original_action_euler_offclock as g1e
from ge19 import h4f3d17_actual_original_action_dense_canonical_H1 as d17
from ge19 import repair32b_factor2_corrected_reduced_h2_z11_reconstruction as r32b

ROOT=Path(__file__).resolve().parents[1]
MODES=g1e.MODES
TAGS=g1e.TAGS
GRIDS=g1e.GRIDS
EPS=1e-300
FRACTIONS=(0.25,0.5,0.75)
PINNED={
 "ge19/h4f3d_g1e_z11_original_action_euler_offclock.py":
   "017ddec6b52434920f394a728a994f017af62dd9",
 "ge19/repair32b_factor2_corrected_reduced_h2_z11_reconstruction.py":
   "6ece578e8a30f48faaded8808687a9bd5c114608",
 "ge19/repair07_window_retarded_reduced_h3_z20_particular.py":
   "e34d28a2062c748f48bc82fa928844b02631de25",
 "ge19/h4f3d17_actual_original_action_dense_canonical_H1.py":
   "813c350d1d1860515997ce43f223b9b6bc2091e9",
}
VARIANTS=("pchip_saved","euler_hermite_saved","euler_hermite_actionB")

def check(ok,msg):
    if not bool(ok):raise RuntimeError("GE19_G1F_"+msg)

def sha(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda:f.read(1<<20),b""):
            h.update(block)
    return h.hexdigest()

def check_pins():
    d={}
    for path,want in PINNED.items():
        committed=subprocess.check_output(
          ["git","rev-parse","HEAD:"+path],cwd=ROOT,text=True).strip()
        working=subprocess.check_output(
          ["git","hash-object",str(ROOT/path)],cwd=ROOT,text=True).strip()
        check(committed==want and working==want,"SOURCE_PIN_"+path)
        d[path]=want
    return d

def make_accumulator():
    return {
      "max_main_six_Euler_absolute_L2_sampled":0.,
      "max_full_eight_Euler_absolute_L2_sampled":0.,
      "max_full_eight_Euler_relative_backward_error_sampled":0.,
      "max_scalar_Euler_absolute_sampled":0.,
      "max_aether_Euler_absolute_sampled":0.,
      "max_momentum_constitutive_absolute_L2_sampled":0.,
      "max_shift_absolute_sampled":0.,
      "max_anisotropy_absolute_sampled":0.,
      "dominant_relative_error_position":None,
      "dominant_scalar_error_position":None,
      "first_interval_half_Euler_relative_backward_error":None,
      "first_interval_half_scalar_Euler_absolute":None,
    }

def update(stats,rows,const,C,w,pp_x,H,source,interval,fraction):
    absol=g1e.safe_l2(rows)
    main=g1e.safe_l2(rows[:6])
    rel=absol/max(
      g1e.safe_l2(C[4:10]@w),g1e.safe_l2(source),
      abs(H)*g1e.safe_l2(pp_x),
      g1e.safe_l2((C[10]+C[11])@w),
      g1e.safe_l2((C[12]+C[13])@w),EPS)
    stats["max_full_eight_Euler_absolute_L2_sampled"]=max(
        stats["max_full_eight_Euler_absolute_L2_sampled"],absol)
    stats["max_main_six_Euler_absolute_L2_sampled"]=max(
        stats["max_main_six_Euler_absolute_L2_sampled"],main)
    if rel>stats["max_full_eight_Euler_relative_backward_error_sampled"]:
        stats["max_full_eight_Euler_relative_backward_error_sampled"]=rel
        stats["dominant_relative_error_position"]={
            "interval":int(interval),"fraction":float(fraction)}
    if abs(rows[3])>stats["max_scalar_Euler_absolute_sampled"]:
        stats["max_scalar_Euler_absolute_sampled"]=float(abs(rows[3]))
        stats["dominant_scalar_error_position"]={
            "interval":int(interval),"fraction":float(fraction)}
    stats["max_aether_Euler_absolute_sampled"]=max(
        stats["max_aether_Euler_absolute_sampled"],float(abs(rows[2])))
    stats["max_momentum_constitutive_absolute_L2_sampled"]=max(
        stats["max_momentum_constitutive_absolute_L2_sampled"],const)
    stats["max_shift_absolute_sampled"]=max(
        stats["max_shift_absolute_sampled"],float(abs(rows[6])))
    stats["max_anisotropy_absolute_sampled"]=max(
        stats["max_anisotropy_absolute_sampled"],float(abs(rows[7])))
    if interval==0 and fraction==0.5:
        stats["first_interval_half_Euler_relative_backward_error"]=rel
        stats["first_interval_half_scalar_Euler_absolute"]=float(abs(rows[3]))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--results-dir",type=Path,default=ROOT/"results")
    ap.add_argument("--tag",choices=TAGS,default="C_star")
    ap.add_argument("--grid",choices=GRIDS.keys(),default="primary")
    ap.add_argument("--interval-stride",type=int,default=4)
    ap.add_argument("--json-out",type=Path,required=True)
    args=ap.parse_args()
    check(args.interval_stride>=1,"BAD_INTERVAL_STRIDE")
    check(not args.json_out.exists(),"REFUSE_OVERWRITE")
    pins=check_pins()
    g1epins=g1e.pin_sources()
    files=g1e.files(args.results_dir)
    old=d17.d16r1.d15.d13.old
    d15=d17.d16r1.d15
    r7=old.r7
    nt=GRIDS[args.grid]
    check(tuple(map(int,r7.FOURIER_N))==MODES,"FROZEN_MODE_SET_CHANGED")
    outcome=[]
    with np.load(files["r13"],allow_pickle=False) as r13,\
         np.load(files["z11"],allow_pickle=False) as z:
        bgs,_,mod6,mod7,_,_,_,_,_=old.build_context(args.results_dir,r13)
        bg=bgs[(nt,args.tag)]
        x=np.asarray(bg["x"],float)
        check(np.array_equal(x,np.asarray(z["x_"+args.grid],float)),
              "ORIGINAL_CLOCK_MISMATCH")
        st=np.asarray(z[f"{args.tag}_Z11_{args.grid}"],complex)
        dt=np.asarray(z[f"{args.tag}_Z11dot_{args.grid}"],complex)
        B=np.asarray(z[f"{args.tag}_B10_{args.grid}"],complex)
        sourceall=np.asarray(z[f"{args.tag}_M1_rhs_{args.grid}"],complex)
        check(st.shape==(6,6,nt) and dt.shape==(6,4,nt) and
              B.shape==(6,nt) and sourceall.shape==(6,6,nt),
              "ORIGINAL_Z11_SHAPES_CHANGED")
        check(np.isfinite(st).all() and np.isfinite(dt).all()
              and np.isfinite(B).all() and np.isfinite(sourceall).all(),
              "NONFINITE_INPUT")
        real_source=r32b.source_from_B(bg,B)
        source_match=g1e.safe_l2(real_source-sourceall)/max(
            g1e.safe_l2(real_source),g1e.safe_l2(sourceall),EPS)
        check(source_match<1e-10,"FROZEN_M1_SOURCE_DICTIONARY_MISMATCH")

        get_H,_=d15.clk.make_original_action_background(r7,bg,args.tag)
        action=d17.core.ActionBackground(r7,bg,get_H)
        original_point=r7._bg_point
        original_cache=r7._CANONICAL_LOCAL_CACHE
        r7._CANONICAL_LOCAL_CACHE={}
        r7._bg_point=lambda background,at:action(background,float(at))
        index=list(range(0,nt-1,args.interval_stride))
        if nt-2 not in index:index.append(nt-2)
        try:
            action.knot_check()
            for im,m in enumerate(MODES):
                k=float(m*r7.g9.K_REQ[0]/r7.FOURIER_N[0])
                w_nodes=np.empty((nt,10),complex)
                w_nodes[:,0]=st[im,0]
                w_nodes[:,1]=st[im,5]
                w_nodes[:,2:6]=st[im,[1,2,3,4],:].T
                w_nodes[:,6:10]=dt[im].T
                pnodes=np.empty((4,nt),complex)
                pdx_nodes=np.empty((4,nt),complex)
                for j in range(nt):
                    C,bp,_=r7._local_linear_matrix(
                        mod6,mod7,bg,args.tag,k,float(x[j]))
                    pnodes[:,j]=C[0:4]@w_nodes[j]
                    pdx_nodes[:,j]=(C[6:10]@w_nodes[j]-sourceall[im,1:5,j])/float(bp["H"])
                check(np.isfinite(pnodes).all() and np.isfinite(pdx_nodes).all(),
                      "NONFINITE_CANONICAL_DATA")
                mompchip=g1e.cpchip(x,pnodes)
                Npchip=g1e.cpchip(x,st[im,0])
                rhopchip=g1e.cpchip(x,st[im,5])
                Bpchip=g1e.cpchip(x,B[im])
                sourcepchip=g1e.cpchip(x,sourceall[im])
                q=st[im,[1,2,3,4],:]
                vx=dt[im]/np.asarray(bg["H"],float)[None,:]
                variant={v:make_accumulator() for v in VARIANTS}
                forcing_gap={"max_source_L2_absolute_sampled":0.,
                             "max_source_L2_relative_sampled":0.}
                for j in index:
                    a=float(x[j]);b=float(x[j+1]);h=b-a
                    for u in FRACTIONS:
                        t=a+u*h
                        C,bp,_=r7._local_linear_matrix(
                            mod6,mod7,bg,args.tag,k,t)
                        H=float(bp["H"])
                        qh,qdx=g1e.hermite_value_and_dx(
                            q[:,j],q[:,j+1],vx[:,j],vx[:,j+1],h,u)
                        w=np.empty(10,complex)
                        w[0]=g1e.c_eval(Npchip,t)
                        w[1]=g1e.c_eval(rhopchip,t)
                        w[2:6]=qh
                        w[6:10]=H*qdx
                        psaved=g1e.c_eval(mompchip,t)
                        psaved_x=g1e.c_eval(mompchip,t,True)
                        ph,ph_x=g1e.hermite_value_and_dx(
                            pnodes[:,j],pnodes[:,j+1],
                            pdx_nodes[:,j],pdx_nodes[:,j+1],h,u)
                        saved=np.asarray(g1e.c_eval(sourcepchip,t),complex)
                        Boff=complex(g1e.c_eval(Bpchip,t))
                        action_source=np.zeros(6,complex)
                        action_source[2]=bp["a"]**3*bp["Q_action"]*Boff
                        action_source[3]=-1j*k*bp["a"]**2*Boff
                        gap=g1e.safe_l2(saved-action_source)
                        gap_rel=gap/max(g1e.safe_l2(saved),
                                        g1e.safe_l2(action_source),EPS)
                        forcing_gap["max_source_L2_absolute_sampled"]=max(
                            forcing_gap["max_source_L2_absolute_sampled"],gap)
                        forcing_gap["max_source_L2_relative_sampled"]=max(
                            forcing_gap["max_source_L2_relative_sampled"],gap_rel)
                        for name,p,px,s in (
                            ("pchip_saved",psaved,psaved_x,saved),
                            ("euler_hermite_saved",ph,ph_x,saved),
                            ("euler_hermite_actionB",ph,ph_x,action_source),
                        ):
                            rows=g1e.physical_rows(C,w,px,H,s)
                            const=g1e.safe_l2(p-C[0:4]@w)
                            update(variant[name],rows,const,C,w,px,H,s,j,u)
                base=variant["pchip_saved"]["max_full_eight_Euler_relative_backward_error_sampled"]
                hnew=variant["euler_hermite_saved"]["max_full_eight_Euler_relative_backward_error_sampled"]
                improvement=base/max(hnew,EPS)
                outcome.append({
                  "mode":int(m),"variants":variant,
                  "forcing_gap":forcing_gap,
                  "PCHIP_to_EulerHermite_max_relative_error_ratio":
                      float(improvement),
                  "improvement_interpretation":
                      "empirical sampled maximum ratio, NOT a convergence rate or certified bound",
                })
                print("GE19_G1F m=%s PCHIP=%0.9g EULER_HERMITE=%0.9g ACTIONB=%0.9g ratio=%0.6g"%(
                    m,base,hnew,
                    variant["euler_hermite_actionB"]["max_full_eight_Euler_relative_backward_error_sampled"],
                    improvement),flush=True)
                r7._CANONICAL_LOCAL_CACHE.clear()
        finally:
            r7._bg_point=original_point
            r7._CANONICAL_LOCAL_CACHE=original_cache
    report={
      "classification":"GE19_G1F_Z11_CANONICAL_MOMENTUM_INTERPOLATION_PHYSICAL_EULER_COMPARISON_COMPLETED_G1_OPEN",
      "scope":{"tag":args.tag,"grid":args.grid,"Nt":nt,
               "original_modes":list(MODES),"interval_stride":args.interval_stride,
               "intervals_per_mode":len(index),
               "fractions_per_interval":list(FRACTIONS)},
      "original_action_source_pins":g1epins,
      "G1F_source_pins":pins,
      "input_sha256":{k:sha(path) for k,path in files.items()},
      "original_repair32b_GE05_factor_two":2.0,
      "frozen_source_dictionary_global_relative_L2":source_match,
      "per_mode":outcome,
      "surrogate_comparison":{
          "pchip_saved":"original G1E: Z11 physical field Hermite, N/dr PCHIP, p PCHIP from nodal Cmat and M1_rhs PCHIP",
          "euler_hermite_saved":"same Z11 physical field surrogate and frozen saved M1 PCHIP, but p cubic Hermite from frozen nodal p and nodal original-action Euler p_x",
          "euler_hermite_actionB":"same p Hermite, with action a^3Q B, -ik a^2 B using PCHIP(B10) rather than original PCHIP(M1_rhs)",
          "nodal_hermite_derivatives":"p_x at endpoints determined from original GE06/GE07/Lambda dynamic Euler Cmat[6:10]w minus frozen source divided by original H; resulting endpoint Euler identity is BUILT IN",
          "measure_type":"offclock sampled actual original-action Euler defects of declared reconstructions, NOT true physical continuous suprema"
      },
      "G1_true_Z11_action_Euler_interval_enclosed":False,
      "G1_GE05_true_source_error_enclosed":False,
      "G1_PHYSICAL_CLOSED":False,
      "G3_B_total_frozen":False,
      "full_H4_Ward_certified":False,
      "Z21_certified":False,
      "lensing_licensed":False,
      "claim_boundary":"Source-locked unchanged real physical action Cmat and frozen Z11+GE05 arrays. No new Z11 integration. The alternative cubic-Hermite p derivative is imposed at endpoints from the Euler equation, so any apparent reduction of sampled midpoint defect is about offclock polynomial reconstruction only and is not independent proof of physical ODE or interval error. Original G1E metrics and science gates remain immutable."
    }
    args.json_out.parent.mkdir(parents=True,exist_ok=True)
    args.json_out.write_text(json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print(report["classification"],flush=True)

if __name__=="__main__":
    main()
