#!/usr/bin/env python3
"""GE19 G1E: original-action Z11 Euler off-clock physical residual diagnostic.

Read frozen Repair32B Z11/Z11dot/B10/M1_rhs and Repair13 action background.
Use original GE06+GE07+Lambda local Cmat and original GE05 factor-two
raw Euler source dictionary. Construct explicit *surrogate* field/momentum
interpolants, evaluate all six original main Euler + shift/anisotropy rows,
and report the original PCHIP M1 drive versus action background*PCHIP B10.

This is NOT interval arithmetic, not a physical Euler supremum enclosure,
not G1 PASS, not original FD4/FD8 prelocked B_total, and never evaluates
the mixed H4 Ward, Z21, or observations. Original inputs are not changed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
from pathlib import Path

import numpy as np
from scipy.interpolate import PchipInterpolator

from ge19 import h4f3d17_actual_original_action_dense_canonical_H1 as d17
from ge19 import repair32b_factor2_corrected_reduced_h2_z11_reconstruction as r32b

ROOT=Path(__file__).resolve().parents[1]
TINY=1.e-300
MODES=(3,5,8,10,15,20)
TAGS=("C_min","C_star","C_max")
GRIDS={"primary":128,"control":64}
EXPECTED_BLOBS={
    "ge19/repair07_window_retarded_reduced_h3_z20_particular.py":
        "e34d28a2062c748f48bc82fa928844b02631de25",
    "ge19/repair11_lambda_inclusive_reduced_h1_reclosure.py":
        "dbfa43ae11dbd3cfeeb1994a30237e9374dbb3e7",
    "ge19/repair13_self_consistent_reduced_background_h1_reclosure.py":
        "362d63d03d7b850fceae393f535353ded79aeea7",
    "ge19/repair32b_factor2_corrected_reduced_h2_z11_reconstruction.py":
        "6ece578e8a30f48faaded8808687a9bd5c114608",
    "ge19/h4f3d17_actual_original_action_dense_canonical_H1.py":
        "813c350d1d1860515997ce43f223b9b6bc2091e9",
    "ge19/h4f3d17_original_action_dense_H1_core.py":
        "6074d31050450440654bdc55980a13584d5ce5ee",
    "ge19/h4f3b_actual_corrected_six_piece_source.py":
        "0423cbc64f6cda3b2a9aeb67c734935ef3ae7f9c",
}
LOCKED_NPZ={
    "r13":("ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz",
           "011c0ae54fd21d70c0e2c695ce62e7b74a3c5529a07c9023c882a447d5b40ca3"),
    "z11":("ge19_repair32b_factor2_corrected_reduced_h2_z11_reconstruction.npz",
           "5d4a0a72c08d09d096a8de0b428b3c8443fc33e8ad442ed6d997d6bf2bc6e327"),
}
GE15_NAME="ge15_R1_dense_accepted_step_trace.dat"
GE15_SHA="7f57ab676f2a31cf0abf93ff0f8b0f1f2f80bb9a58d7cf1e47e10a158c57c69f"
REQUIRED_ROWS=("lapse","isotropic","aether","scalar","dust_potential","dust_density","shift","anisotropy")

def require(ok,msg):
    if not bool(ok):raise RuntimeError("GE19_G1E_"+msg)

def sha256(p):
    h=hashlib.sha256()
    with Path(p).open("rb") as stream:
        for block in iter(lambda:stream.read(1048576),b""):
            h.update(block)
    return h.hexdigest()

def pin_sources():
    out={}
    for p,want in EXPECTED_BLOBS.items():
        got=subprocess.check_output(
            ["git","rev-parse","HEAD:"+p],cwd=ROOT,text=True).strip()
        working=subprocess.check_output(
            ["git","hash-object",str(ROOT/p)],cwd=ROOT,text=True).strip()
        require(got==want and working==want,"SOURCE_CHANGED_"+p)
        out[p]=want
    require(r32b.RAW_RESIDUAL_DICTIONARY_SCALE==2.0,
            "GE05_M1_FACTOR_TWO_CHANGED")
    return out

def files(rd):
    o={}
    for k,(name,want) in LOCKED_NPZ.items():
        p=rd/name
        require(p.is_file(),"MISSING_"+k+"_"+str(p))
        got=sha256(p)
        require(got==want,"FROZEN_NPZ_SHA_CHANGED_"+k)
        o[k]=p
    dense=rd/GE15_NAME
    require(dense.is_file() and sha256(dense)==GE15_SHA,
            "GE15_ORIGINAL_BACKGROUND_MISSING_OR_CHANGED")
    o["dense"]=dense
    return o

def cpchip(x,arr):
    v=np.asarray(arr,complex)
    require(v.shape[-1]==len(x),"PCHIP_INPUT_CLOCK_MISMATCH")
    return (PchipInterpolator(x,v.real,axis=-1,extrapolate=False),
            PchipInterpolator(x,v.imag,axis=-1,extrapolate=False))

def c_eval(interp,t,derivative=False):
    r,i=interp
    if derivative:
        return r.derivative()(t)+1j*i.derivative()(t)
    return r(t)+1j*i(t)

def hermite_value_and_dx(q0,q1,v0,v1,h,u):
    # q'(x)=qdot/H, from original Z11dot physical-time endpoints.
    u2=u*u;u3=u2*u
    value=((2*u3-3*u2+1)*q0+(u3-2*u2+u)*h*v0
           +(-2*u3+3*u2)*q1+(u3-u2)*h*v1)
    dx=((6*u2-6*u)*q0/h+(3*u2-4*u+1)*v0
        +(-6*u2+6*u)*q1/h+(3*u2-2*u)*v1)
    return value,dx

def safe_l2(v):
    z=float(np.linalg.norm(np.asarray(v,complex)))
    require(math.isfinite(z),"NONFINITE_METRIC")
    return z

def physical_rows(C,w,dpdx,H,source):
    out=np.empty(8,complex)
    out[0]=C[4]@w-source[0]
    out[1:5]=C[6:10]@w-H*dpdx-source[1:5]
    out[5]=C[5]@w-source[5]
    out[6]=(C[10]+C[11])@w
    out[7]=(C[12]+C[13])@w
    # No GE05 shift/anisotropy source; both zero by original dictionary.
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--results-dir",type=Path,default=ROOT/"results")
    ap.add_argument("--tag",choices=TAGS,default="C_star")
    ap.add_argument("--grid",choices=GRIDS.keys(),default="primary")
    ap.add_argument("--interval-stride",type=int,default=4)
    ap.add_argument("--json-out",type=Path,required=True)
    args=ap.parse_args()
    require(args.interval_stride>=1,"BAD_INTERVAL_STRIDE")
    require(not args.json_out.exists(),"REFUSE_OVERWRITE")
    pins=pin_sources()
    p=files(args.results_dir)
    nt=GRIDS[args.grid];tag=args.tag
    # Import via original frozen production dependency chain. D17 and R32B
    # do not run their main functions or numerical integrators here.
    d15=d17.d16r1.d15
    old=d15.d13.old
    r7=old.r7
    require(tuple(map(int,r7.FOURIER_N))==MODES,"FOURIER_MODE_SET_CHANGED")

    with np.load(p["r13"],allow_pickle=False) as z13,\
         np.load(p["z11"],allow_pickle=False) as z11:
        bgs,_,mod6,mod7,_,_,_,_,_=old.build_context(args.results_dir,z13)
        bg=bgs[(nt,tag)]
        x=np.asarray(bg["x"],float)
        require(x.shape==(nt,) and np.all(np.diff(x)>0),"BAD_ORIGINAL_CLOCK")
        require(np.array_equal(x,np.asarray(z11["x_"+args.grid],float)),
                "H4_Z11_SOURCE_CLOCK_MISMATCH")
        st=np.asarray(z11[f"{tag}_Z11_{args.grid}"],complex)
        dt=np.asarray(z11[f"{tag}_Z11dot_{args.grid}"],complex)
        B=np.asarray(z11[f"{tag}_B10_{args.grid}"],complex)
        rhs=np.asarray(z11[f"{tag}_M1_rhs_{args.grid}"],complex)
        require(st.shape==(6,6,nt) and dt.shape==(6,4,nt) and
                B.shape==(6,nt) and rhs.shape==(6,6,nt),
                "ORIGINAL_PARENT_SHAPE_CHANGED")
        require(all(np.isfinite(v).all() for v in (st,dt,B,rhs)),
                "NONFINITE_FROZEN_Z11")

        rebuilt=r32b.source_from_B(bg,B)
        source_input_mismatch=safe_l2(rebuilt-rhs)/max(
            safe_l2(rebuilt),safe_l2(rhs),TINY)
        require(source_input_mismatch<1e-10,
                "REPAIR32B_M1_DICTIONARY_NOT_REPRODUCED")
        src_sha=sha256(p["z11"])
        actionH,_=d15.clk.make_original_action_background(r7,bg,tag)
        ctx=d17.core.ActionBackground(r7,bg,actionH)
        orig_point=r7._bg_point
        orig_cache=r7._CANONICAL_LOCAL_CACHE
        r7._CANONICAL_LOCAL_CACHE={}
        r7._bg_point=lambda original_bg,xq:ctx(original_bg,float(xq))
        modes=[]
        try:
            ctx.knot_check()
            checked_intervals=list(range(0,nt-1,args.interval_stride))
            if nt-2 not in checked_intervals:
                checked_intervals.append(nt-2)
            for im,m in enumerate(MODES):
                k=float(m*r7.g9.K_REQ[0]/r7.FOURIER_N[0])
                w_nodes=np.empty((nt,10),complex)
                w_nodes[:,0]=st[im,0]
                w_nodes[:,1]=st[im,5]
                w_nodes[:,2:6]=st[im,[1,2,3,4],:].T
                w_nodes[:,6:10]=dt[im].T
                pnodes=np.empty((4,nt),complex)
                for j in range(nt):
                    C,bp,_=r7._local_linear_matrix(
                        mod6,mod7,bg,tag,k,float(x[j]))
                    pnodes[:,j]=C[0:4]@w_nodes[j]
                pn_inter=cpchip(x,pnodes)
                N_inter=cpchip(x,st[im,0])
                rho_inter=cpchip(x,st[im,5])
                B_inter=cpchip(x,B[im])
                src_inter=cpchip(x,rhs[im])
                q=st[im,[1,2,3,4],:]
                v=dt[im]/np.asarray(bg["H"],float)[None,:]
                stats={
                  "mode":m,"intervals_scanned":len(checked_intervals),
                  "x_fraction_samples":(0.25,0.5,0.75),
                  "max_main_Euler_residual_absolute_L2_sampled":0.,
                  "max_eight_row_Euler_residual_absolute_L2_sampled":0.,
                  "max_eight_row_relative_backward_error_sampled":0.,
                  "max_shift_absolute_sampled":0.,
                  "max_anisotropy_absolute_sampled":0.,
                  "max_nodal_momentum_relation_discrepancy_sampled":0.,
                  "max_frozen_PCHIP_M1_vs_action_B_source_absolute_L2_sampled":0.,
                  "max_frozen_PCHIP_M1_vs_action_B_source_relative_L2_sampled":0.,
                  "source_rows_L2_max_sampled":0.,
                  "max_frozen_cmat_zero_offset_sampled":0.,
                  "dominant_residual_interval":None,
                  "dominant_residual_fraction":None,
                  "per_euler_row_absolute_max_sampled":{row:0. for row in REQUIRED_ROWS},
                }
                for interval in checked_intervals:
                    a=float(x[interval]);b=float(x[interval+1]);h=b-a
                    for fraction in stats["x_fraction_samples"]:
                        t=a+fraction*h
                        C,bp,diag=r7._local_linear_matrix(
                            mod6,mod7,bg,tag,k,t)
                        h_action=float(bp["H"])
                        dyn,dyn_x=hermite_value_and_dx(
                            q[:,interval],q[:,interval+1],
                            v[:,interval],v[:,interval+1],h,
                            fraction)
                        w=np.empty(10,complex)
                        w[0]=c_eval(N_inter,t)
                        w[1]=c_eval(rho_inter,t)
                        w[2:6]=dyn
                        w[6:10]=h_action*dyn_x
                        pp=np.asarray(c_eval(pn_inter,t),complex)
                        pp_x=np.asarray(c_eval(pn_inter,t,True),complex)
                        source=np.asarray(c_eval(src_inter,t),complex)
                        Bx=complex(c_eval(B_inter,t))
                        action_source=np.zeros(6,complex)
                        action_source[2]=bp["a"]**3*bp["Q_action"]*Bx
                        action_source[3]=-1j*k*bp["a"]**2*Bx
                        physical=physical_rows(C,w,pp_x,h_action,source)
                        absolute=safe_l2(physical)
                        relative=absolute/max(
                            safe_l2(C[4:10]@w),safe_l2(source),
                            abs(h_action)*safe_l2(pp_x),
                            safe_l2((C[10]+C[11])@w),
                            safe_l2((C[12]+C[13])@w),TINY)
                        diff=safe_l2(source-action_source)
                        diffrel=diff/max(safe_l2(source),
                                        safe_l2(action_source),TINY)
                        const=safe_l2(pp-C[0:4]@w)
                        stats["max_eight_row_Euler_residual_absolute_L2_sampled"]=max(
                            stats["max_eight_row_Euler_residual_absolute_L2_sampled"],absolute)
                        stats["max_main_Euler_residual_absolute_L2_sampled"]=max(
                            stats["max_main_Euler_residual_absolute_L2_sampled"],
                            safe_l2(physical[:6]))
                        if relative>stats["max_eight_row_relative_backward_error_sampled"]:
                            stats["max_eight_row_relative_backward_error_sampled"]=relative
                            stats["dominant_residual_interval"]=interval
                            stats["dominant_residual_fraction"]=fraction
                        stats["max_shift_absolute_sampled"]=max(
                            stats["max_shift_absolute_sampled"],abs(physical[6]))
                        stats["max_anisotropy_absolute_sampled"]=max(
                            stats["max_anisotropy_absolute_sampled"],abs(physical[7]))
                        stats["max_nodal_momentum_relation_discrepancy_sampled"]=max(
                            stats["max_nodal_momentum_relation_discrepancy_sampled"],const)
                        stats["max_frozen_PCHIP_M1_vs_action_B_source_absolute_L2_sampled"]=max(
                            stats["max_frozen_PCHIP_M1_vs_action_B_source_absolute_L2_sampled"],diff)
                        stats["max_frozen_PCHIP_M1_vs_action_B_source_relative_L2_sampled"]=max(
                            stats["max_frozen_PCHIP_M1_vs_action_B_source_relative_L2_sampled"],diffrel)
                        stats["source_rows_L2_max_sampled"]=max(
                            stats["source_rows_L2_max_sampled"],safe_l2(source))
                        stats["max_frozen_cmat_zero_offset_sampled"]=max(
                            stats["max_frozen_cmat_zero_offset_sampled"],
                            float(diag["raw_zero_output_abs_max"]))
                        for ii,name in enumerate(REQUIRED_ROWS):
                            stats["per_euler_row_absolute_max_sampled"][name]=max(
                                stats["per_euler_row_absolute_max_sampled"][name],
                                float(abs(physical[ii])))
                modes.append(stats)
                print(f"GE19_G1E_Z11_ACTION_EULER m={m} "
                      f"euler8_rel_sampled={stats['max_eight_row_relative_backward_error_sampled']:.8g} "
                      f"source_native_rel_sampled={stats['max_frozen_PCHIP_M1_vs_action_B_source_relative_L2_sampled']:.8g}",
                      flush=True)
                r7._CANONICAL_LOCAL_CACHE.clear()
        finally:
            r7._bg_point=orig_point
            r7._CANONICAL_LOCAL_CACHE=orig_cache
        report={
          "classification":"GE19_G1E_ORIGINAL_ACTION_Z11_EULER_AND_GE05_SOURCE_OFFCLOCK_SAMPLED_DIAGNOSTIC_COMPLETED_G1_OPEN",
          "scope":{"C":tag,"Nt":nt,"grid":args.grid,"modes":list(MODES),
                   "interval_stride":args.interval_stride,
                   "intervals_per_mode":len(checked_intervals),
                   "fractions_per_interval":[0.25,0.5,0.75],
                   "original_action_background":True,
                   "original_H4F3B_frozen_Z11_array":True,
                   "Z11_reconstruction":"dynamic S,u,phi,T cubic Hermite in ln(a) using physical Z11dot / original action H; lapse/dust density PCHIP",
                   "canonical_momenta":"p_j = Cmat(t_j)[0:4] w_j at 128/64 frozen original nodes; interpolated PCHIP",
                   "momentum_derivative":"d/dln(a) of that explicitly interpolated PCHIP canonical momentum, NOT physical Z11dot",
                   "GE05_source":"original saved Repair32B GE05 M1_rhs PCHIP, compared separately with original action background times B10 PCHIP"},
          "original_source_locks":pins,
          "input_SHA256":{k:sha256(path) for k,path in p.items()},
          "frozen_GE05_M1_factor_two_exact":True,
          "recomputed_frozen_source_relative_L2":source_input_mismatch,
          "per_mode":modes,
          "G1_true_Euler_supremum_certified":False,
          "G1_Z11_original_action_continuous_error_enclosed":False,
          "G1_GE05_true_B10_error_enclosed":False,
          "G1_PHYSICAL_CLOSED":False,
          "G3_B_total_frozen":False,
          "full_H4_Ward_certified":False,
          "Z21_certified":False,"lensing_licensed":False,
          "claim_boundary":"Source-action Cmat with frozen Repair13 exact-charge/Lambda background and correct GE05 M1 factor-two source applied to explicit frozen Z11 surrogate. Residual sampled at three fractions of selected coarse intervals. PCHIP/Hermite is a chosen off-clock reconstruction, not a certified continuous representation of the original numerical integrator. This report is a physical-action residual DIAGNOSTIC, NOT a rigorous interval upper bound, not a strong FD4/FD8 error budget and not an integrated H4 Ward test. All old failures and science thresholds remain intact."
        }
        args.json_out.parent.mkdir(parents=True,exist_ok=True)
        args.json_out.write_text(
            json.dumps(report,sort_keys=True,indent=2,allow_nan=False)+"\n")
        print(report["classification"],flush=True)

if __name__=="__main__":
    main()
