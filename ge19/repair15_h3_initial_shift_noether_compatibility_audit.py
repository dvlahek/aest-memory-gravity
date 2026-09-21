#!/usr/bin/env python3
"""GE19 Repair15 H3 initial shift/Noether compatibility audit.

Diagnostic only.  Reconstructs the frozen Repair14 H3 source from the
certified Repair13 Z10 parent and tests the z=1.5 algebraic compatibility
of lapse, dust-density and shift equations under the frozen window-retarded
dynamic conditions q20=q20dot=0.

No Z20 trajectory is recomputed.
"""
from __future__ import annotations

import argparse, hashlib, importlib.util, json, sys
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

TINY=1e-300
REPAIR13_JSON_SHA="ae3cc790ecffbd5498b5852273c72ae578d4615de29bbb616673c05cdb3e74b7"
REPAIR13_NPZ_SHA="011c0ae54fd21d70c0e2c695ce62e7b74a3c5529a07c9023c882a447d5b40ca3"
REPAIR14_JSON_SHA="741da95a0aaffa31e27f2b05d42b8a7f011574013de8639812e453d7b130fe57"
COMPAT_MAX=1e-6
MATERIAL_FLOOR=1e-12


def sha256(p:Path)->str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load_module(path:Path,name:str):
    spec=importlib.util.spec_from_file_location(name,path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def row_metric(row,x,target):
    row=np.asarray(row,complex)
    x=np.asarray(x,complex)
    lhs=row@x
    residual=lhs-target
    scale=max(
        abs(lhs),abs(target),float(np.sum(np.abs(row*x))),TINY
    )
    return {
        "metric":float(abs(residual)/scale),
        "absolute_residual":float(abs(residual)),
        "scale":float(scale),
        "lhs_abs":float(abs(lhs)),
        "target_abs":float(abs(target)),
    }


def scaled_system(A,b):
    A=np.asarray(A,complex)
    b=np.asarray(b,complex)
    scales=np.maximum(
        np.maximum(np.max(np.abs(A),axis=1),np.abs(b)),
        TINY
    )
    return A/scales[:,None],b/scales,scales


def solve_pair(A,b,rows):
    Ap=np.asarray(A,complex)[list(rows)]
    bp=np.asarray(b,complex)[list(rows)]
    As,bs,_=scaled_system(Ap,bp)
    x,*_=np.linalg.lstsq(As,bs,rcond=None)
    return x


def compatibility(A,b):
    As,bs,scales=scaled_system(A,b)
    x,*_=np.linalg.lstsq(As,bs,rcond=None)
    resid=As@x-bs
    den=max(np.linalg.norm(As@x),np.linalg.norm(bs),TINY)
    ls=float(np.linalg.norm(resid)/den)

    U,S,Vh=np.linalg.svd(As,full_matrices=True)
    tol=max(As.shape)*np.finfo(float).eps*(S[0] if len(S) else 0.0)
    rank=int(np.sum(S>tol))
    null_cols=U[:,rank:]
    if null_cols.size:
        proj=null_cols.conj().T@bs
        left=float(np.linalg.norm(proj)/max(np.linalg.norm(bs),TINY))
    else:
        left=0.0

    aug=np.column_stack([As,bs])
    arank=int(np.linalg.matrix_rank(aug))
    return {
        "least_squares_relative_residual":ls,
        "left_null_compatibility_residual":left,
        "coefficient_rank":rank,
        "augmented_rank":arank,
        "singular_values":[float(v) for v in S],
        "solution_N_dr":[[float(v.real),float(v.imag)] for v in x],
        "row_scales":[float(v) for v in scales],
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
      rd/"ge19_repair13_self_consistent_reduced_background_h1_reclosure.json",
      rd/"ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz",
      rd/"ge19_repair14_self_consistent_reduced_h3_z20_particular.json",
    ]
    miss=[str(p) for p in required if not p.exists()]
    if miss:
        raise RuntimeError("missing frozen inputs: "+", ".join(miss))

    p13j=rd/"ge19_repair13_self_consistent_reduced_background_h1_reclosure.json"
    p13n=rd/"ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz"
    p14j=rd/"ge19_repair14_self_consistent_reduced_h3_z20_particular.json"
    if sha256(p13j)!=REPAIR13_JSON_SHA: raise RuntimeError("Repair13 JSON hash mismatch")
    if sha256(p13n)!=REPAIR13_NPZ_SHA: raise RuntimeError("Repair13 NPZ hash mismatch")
    if sha256(p14j)!=REPAIR14_JSON_SHA: raise RuntimeError("Repair14 JSON hash mismatch")

    parent14=json.loads(p14j.read_text())
    if parent14.get("classification")!="GE19_REPAIR14_SELF_CONSISTENT_REDUCED_H3_Z20_PARTICULAR_FAIL":
        raise RuntimeError("Repair14 parent classification mismatch")

    r7=load_module(ROOT/"ge19/repair07_window_retarded_reduced_h3_z20_particular.py","r7r15")
    r11=load_module(ROOT/"ge19/repair11_lambda_inclusive_reduced_h1_reclosure.py","r11r15")
    r13=load_module(ROOT/"ge19/repair13_self_consistent_reduced_background_h1_reclosure.py","r13r15")
    r14=load_module(ROOT/"ge19/repair14_self_consistent_reduced_h3_z20_particular.py","r14r15")

    mod6_frozen=r7.load_frozen_generator(
        ROOT/"ge06/analytic_aest_directional_source_generator.py","ge06r15"
    )
    mod6=r7.build_stable_ge06_generator_v2(mod6_frozen)
    mod7=r7.load_frozen_generator(
        ROOT/"ge07/pressureless_matter_directional_source_generator.py","ge07r15"
    )

    dense=rd/"ge15_R1_dense_accepted_step_trace.dat"
    base64,_,_=r7.build_ge15_reference(dense,r7.NT_PRIMARY)
    base32,_,_=r7.build_ge15_reference(dense,r7.NT_CONTROL)
    rho64=r11.interp_lambda(rd/"ge15_R1_cli_background.dat",base64["x"])
    rho32=r11.interp_lambda(rd/"ge15_R1_cli_background.dat",base32["x"])
    frozen=np.load(p13n)

    bgs={}
    sources={}
    lambda_by_bg={}

    for grid,base,rho,suffix,nx in (
        ("primary",base64,rho64,"primary",r7.NX_PRIMARY),
        ("control",base32,rho32,"control",r7.NX_PRIMARY),
    ):
        for tag in r7.C_TAGS:
            bg,_=r13.reduced_background(r7,base,tag,rho)
            Hf=np.asarray(frozen[f"{tag}_H_reduced_{suffix}"],float)
            if np.linalg.norm(bg["H"]-Hf)>1e-14*max(np.linalg.norm(Hf),TINY):
                raise RuntimeError(f"H reproduction mismatch {grid} {tag}")
            bgs[(grid,tag)]=bg
            lambda_by_bg[id(bg)]=rho

    r11.install_lambda_operator(r7,lambda_by_bg)

    for grid,rho,suffix,nx in (
        ("primary",rho64,"primary",r7.NX_PRIMARY),
        ("control",rho32,"control",r7.NX_PRIMARY),
    ):
        for tag in r7.C_TAGS:
            state=np.asarray(frozen[f"{tag}_Z10_reduced_{suffix}"],complex)
            dot=np.asarray(frozen[f"{tag}_Z10_reduced_dot_{suffix}"],complex)
            sources[(grid,tag)]=r14.source_bundle_reduced_lambda(
                r7,mod6,mod7,bgs[(grid,tag)],rho,tag,nx,state,dot
            )

    # First pass: collect target norms for material-source classification.
    raw=[]
    global_target_max=0.0
    for grid in ("primary","control"):
      for tag in r7.C_TAGS:
        bg=bgs[(grid,tag)]
        x0=float(bg["x"][0])
        for beta in r7.BETAS:
          src=sources[(grid,tag)][beta]
          for m in r7.M_SOLVE:
            k=float(m*r7.g9.K_REQ[0]/r7.FOURIER_N[0])
            rhs=np.asarray(src["rhs"][:,0,m],complex)
            rc=np.asarray(src["rhs_constraint"][:,0,m],complex)
            Cmat,bp,_=r7._local_linear_matrix(mod6,mod7,bg,tag,k,x0)
            A=np.vstack([
                Cmat[4,[0,1]],
                Cmat[5,[0,1]],
                (Cmat[10]+Cmat[11])[[0,1]],
            ])
            b=np.asarray([rhs[0],rhs[5],rc[0]],complex)
            tnorm=float(np.linalg.norm(b))
            global_target_max=max(global_target_max,tnorm)
            raw.append((grid,tag,beta,int(m),k,rhs,rc,Cmat,A,b,tnorm))

    rows=[]
    material=[]
    current_shift_max=0.0
    current_aniso_max=0.0
    ls_max=0.0
    left_max=0.0
    pair_best_third_max=0.0

    for grid,tag,beta,m,k,rhs,rc,Cmat,A,b,tnorm in raw:
        mat=bool(tnorm>=MATERIAL_FLOOR*max(global_target_max,TINY))

        # Exact current Repair14 initialization: q=v=0, solve lapse+density.
        y0,wcur,idiag=r7._initial_canonical_state(
            mod6,mod7,bgs[(grid,tag)],tag,k,
            float(bgs[(grid,tag)]["x"][0]),
            np.zeros(4,complex),np.zeros(4,complex),rhs
        )
        smet=r7._constraint_backward_error(
            Cmat[10]+Cmat[11],wcur,rc[0],
            Cmat[10]@wcur,Cmat[11]@wcur
        )
        amet=r7._constraint_backward_error(
            Cmat[12]+Cmat[13],wcur,rc[1],
            Cmat[12]@wcur,Cmat[13]@wcur
        )
        current_shift_max=max(current_shift_max,smet["metric"])
        current_aniso_max=max(current_aniso_max,amet["metric"])

        comp=compatibility(A,b)
        if mat:
            ls_max=max(ls_max,comp["least_squares_relative_residual"])
            left_max=max(left_max,comp["left_null_compatibility_residual"])

        pair={}
        # local x=(N,dr); dynamic q/v frozen zero.
        for name,pr in (("lapse_density",(0,1)),("density_shift",(1,2)),("lapse_shift",(0,2))):
            x=solve_pair(A,b,pr)
            mets=[row_metric(A[i],x,b[i]) for i in range(3)]
            third=max(mets[i]["metric"] for i in range(3) if i not in pr)
            pair[name]={
                "solution_N_dr":[[float(v.real),float(v.imag)] for v in x],
                "equation_metrics":mets,
                "unfitted_equation_metric_max":float(third),
            }
        best_third=min(v["unfitted_equation_metric_max"] for v in pair.values())
        if mat:
            pair_best_third_max=max(pair_best_third_max,best_third)

        rec={
            "grid":grid,"C":tag,"beta0":float(beta),"m":m,"k_Mpc":k,
            "target_norm":tnorm,"material_source_case":mat,
            "current_initial":{
                "initial_algebraic_scaled_residual":idiag["initial_algebraic_scaled_residual"],
                "shift_metric":smet["metric"],
                "shift_absolute_residual":smet["absolute_residual"],
                "shift_scale":smet["scale"],
                "anisotropy_metric":amet["metric"],
            },
            "compatibility_3x2":comp,
            "pairwise":pair,
            "best_pair_unfitted_equation_metric":float(best_third),
        }
        rows.append(rec)
        if mat: material.append(rec)

    # Routing is based only on material-source cases.
    if not material:
        route="REPAIR15_IMPLEMENTATION_NO_MATERIAL_CASES"
    elif ls_max>COMPAT_MAX or left_max>COMPAT_MAX:
        route="INITIAL_SOURCE_INCOMPATIBILITY"
    elif current_shift_max>COMPAT_MAX:
        route="CURRENT_INITIAL_PARTITION_ONLY"
    else:
        route="INITIAL_SURFACE_CLOSE_PROPAGATION_DEFECT_REMAINS"

    report={
      "classification":"GE19_REPAIR15_H3_INITIAL_SHIFT_NOETHER_COMPATIBILITY_AUDIT_COMPLETE",
      "predata_classification":"GE19_REPAIR15_PREDATA_H3_INITIAL_SHIFT_NOETHER_COMPATIBILITY_AUDIT",
      "diagnostic_only":True,
      "provenance":{
        "Repair13_JSON_sha256":sha256(p13j),
        "Repair13_NPZ_sha256":sha256(p13n),
        "Repair14_JSON_sha256":sha256(p14j),
        "Repair14_parent_FAIL":True,
        "Z20_trajectory_recomputed":False
      },
      "thresholds":{
        "compatibility_relative_residual_max":COMPAT_MAX,
        "material_source_floor_relative_to_global_initial_target_max":MATERIAL_FLOOR
      },
      "global":{
        "initial_target_norm_max":global_target_max,
        "material_case_count":len(material),
        "all_case_count":len(rows),
        "current_initial_shift_metric_max":current_shift_max,
        "current_initial_anisotropy_metric_max":current_aniso_max,
        "material_3x2_least_squares_relative_residual_max":ls_max,
        "material_left_null_compatibility_residual_max":left_max,
        "material_best_pair_unfitted_equation_metric_max":pair_best_third_max
      },
      "routing":{"next_route":route},
      "per_case":rows,
      "claim_boundary":"Initial-surface H3 algebraic/source compatibility audit only. No Repair14 trajectory is modified or recertified; q20 and H4/Z21 remain unlicensed."
    }

    out=Path(args.json_out)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2,allow_nan=False)+"\n")
    print(json.dumps(report,indent=2,allow_nan=False))


if __name__=="__main__":
    main()
