#!/usr/bin/env python3
"""GE19 Repair17 full canonical initial-manifold audit.

Diagnostic only. For the exact frozen Repair14 H3 source, form the affine
lapse+shift constraints in canonical y=(q,p) at z=1.5 after the frozen
Noether-regularized algebraic reconstruction w= WY y + WR source.

Tests full y (2x8), q-only (2x4), and p-only (2x4). No time integration.
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
REPAIR15_JSON_SHA="a8c86b6056a3d6ab2f6f443850bef34881452b4a11b32bb6a66e2ac7920f1e50"
REPAIR16_JSON_SHA="768d5a2de7cd62059e7149a4765ab5a9663eef708fc29989c05192f607c5bf68"

FULL_RES_MAX=1e-8
CONSTRAINT_MAX=1e-6
ALG_MAX=1e-8
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


def backward_error(row,w,target):
    row=np.asarray(row,complex); w=np.asarray(w,complex); target=complex(target)
    lhs=complex(row@w); res=lhs-target
    scale=max(abs(lhs),abs(target),float(np.sum(np.abs(row*w))),TINY)
    return {
        "metric":float(abs(res)/scale),
        "absolute_residual":float(abs(res)),
        "scale":float(scale),
        "lhs_abs":float(abs(lhs)),
        "target_abs":float(abs(target)),
    }


def solve_subset(A,b,cols):
    A=np.asarray(A,complex)[:,np.asarray(cols,int)]
    b=np.asarray(b,complex)
    row_scale=np.maximum.reduce([
        np.max(np.abs(A),axis=1),
        np.abs(b),
        np.full(A.shape[0],TINY,float)
    ])
    As=A/row_scale[:,None]
    bs=b/row_scale
    x,resid,rank,s=np.linalg.lstsq(As,bs,rcond=None)
    rr=As@x-bs
    rel=float(np.linalg.norm(rr)/max(np.linalg.norm(As@x),np.linalg.norm(bs),TINY))
    aug=np.column_stack([As,bs])
    aug_rank=int(np.linalg.matrix_rank(aug))
    return x,{
        "relative_residual":rel,
        "coefficient_rank":int(rank),
        "augmented_rank":aug_rank,
        "singular_values":[float(v) for v in s],
        "row_scales":[float(v) for v in row_scale],
        "solution_L2":float(np.linalg.norm(x)),
    }


def evaluate_candidate(r7,Cmat,WY,WR,source,rr,rc,y):
    y=np.asarray(y,complex)
    w=WY@y+WR@source

    Calg=np.vstack([
        Cmat[0:4],
        Cmat[5:6],
        Cmat[12:13]+Cmat[13:14],
    ])
    target=np.concatenate([y[4:8],[rr[5],rc[1]]])
    lhs=Calg@w
    rs=(lhs-target)/np.maximum(np.max(np.abs(Calg),axis=1),TINY)
    ls=lhs/np.maximum(np.max(np.abs(Calg),axis=1),TINY)
    ts=target/np.maximum(np.max(np.abs(Calg),axis=1),TINY)
    alg=float(np.linalg.norm(rs)/max(np.linalg.norm(ls),np.linalg.norm(ts),TINY))

    lapse=backward_error(Cmat[4],w,rr[0])
    srow=Cmat[10]+Cmat[11]
    shift=backward_error(srow,w,rc[0])
    arow=Cmat[12]+Cmat[13]
    aniso=backward_error(arow,w,rc[1])

    return {
        "algebraic_relative_residual":alg,
        "lapse":lapse,
        "shift":shift,
        "anisotropy":aniso,
        "y_L2":float(np.linalg.norm(y)),
        "q_L2":float(np.linalg.norm(y[:4])),
        "p_L2":float(np.linalg.norm(y[4:])),
        "all_finite":bool(np.all(np.isfinite(y)) and np.all(np.isfinite(w))),
        "y":[[float(z.real),float(z.imag)] for z in y],
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--results-dir",default=str(ROOT/"results"))
    ap.add_argument("--json-out",required=True)
    args=ap.parse_args()
    rd=Path(args.results_dir)

    files={
        "trace":rd/"ge15_R1_dense_accepted_step_trace.dat",
        "bg":rd/"ge15_R1_cli_background.dat",
        "r13j":rd/"ge19_repair13_self_consistent_reduced_background_h1_reclosure.json",
        "r13n":rd/"ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz",
        "r14":rd/"ge19_repair14_self_consistent_reduced_h3_z20_particular.json",
        "r15":rd/"ge19_repair15_h3_initial_shift_noether_compatibility_audit.json",
        "r16":rd/"ge19_repair16_canonical_zero_initial_state_audit.json",
    }
    miss=[str(p) for p in files.values() if not p.exists()]
    if miss: raise RuntimeError("missing frozen inputs: "+", ".join(miss))

    expected={
        "r13j":REPAIR13_JSON_SHA,"r13n":REPAIR13_NPZ_SHA,"r14":REPAIR14_JSON_SHA,
        "r15":REPAIR15_JSON_SHA,"r16":REPAIR16_JSON_SHA,
    }
    for k,h in expected.items():
        got=sha256(files[k])
        if got!=h: raise RuntimeError(f"{k} hash mismatch: {got}")

    d13=json.loads(files["r13j"].read_text())
    d14=json.loads(files["r14"].read_text())
    d15=json.loads(files["r15"].read_text())
    d16=json.loads(files["r16"].read_text())
    if d13.get("stage_A_pass") is not True: raise RuntimeError("Repair13 Stage A not PASS")
    if d14.get("classification")!="GE19_REPAIR14_SELF_CONSISTENT_REDUCED_H3_Z20_PARTICULAR_FAIL":
        raise RuntimeError("Repair14 parent mismatch")
    if d15.get("routing",{}).get("next_route")!="INITIAL_SOURCE_INCOMPATIBILITY":
        raise RuntimeError("Repair15 route mismatch")
    if d16.get("routing",{}).get("next_route")!="QUADRATIC_SOURCE_NOETHER_INCOMPATIBILITY_REMAINS":
        raise RuntimeError("Repair16 route mismatch")

    r7=load_module(ROOT/"ge19/repair07_window_retarded_reduced_h3_z20_particular.py","r7r17")
    r11=load_module(ROOT/"ge19/repair11_lambda_inclusive_reduced_h1_reclosure.py","r11r17")
    r13=load_module(ROOT/"ge19/repair13_self_consistent_reduced_background_h1_reclosure.py","r13r17")
    r14=load_module(ROOT/"ge19/repair14_self_consistent_reduced_h3_z20_particular.py","r14r17")

    mod6_frozen=r7.load_frozen_generator(
        ROOT/"ge06/analytic_aest_directional_source_generator.py","ge06r17"
    )
    mod6=r7.build_stable_ge06_generator_v2(mod6_frozen)
    mod7=r7.load_frozen_generator(
        ROOT/"ge07/pressureless_matter_directional_source_generator.py","ge07r17"
    )

    base64,_,_=r7.build_ge15_reference(files["trace"],r7.NT_PRIMARY)
    base32,_,_=r7.build_ge15_reference(files["trace"],r7.NT_CONTROL)
    rho64=r11.interp_lambda(files["bg"],base64["x"])
    rho32=r11.interp_lambda(files["bg"],base32["x"])
    frozen=np.load(files["r13n"])

    bgs={}; rho_by_bg={}; sources={}
    for grid,base,rho,suffix in (
        ("primary",base64,rho64,"primary"),
        ("control",base32,rho32,"control"),
    ):
        for tag in r7.C_TAGS:
            bg,_=r13.reduced_background(r7,base,tag,rho)
            Hf=np.asarray(frozen[f"{tag}_H_reduced_{suffix}"],float)
            if np.linalg.norm(bg["H"]-Hf)>1e-14*max(np.linalg.norm(Hf),TINY):
                raise RuntimeError(f"H reproduction mismatch {grid} {tag}")
            bgs[(grid,tag)]=bg
            rho_by_bg[id(bg)]=rho

    r11.install_lambda_operator(r7,rho_by_bg)

    for grid,rho,suffix in (
        ("primary",rho64,"primary"),
        ("control",rho32,"control"),
    ):
        for tag in r7.C_TAGS:
            st=np.asarray(frozen[f"{tag}_Z10_reduced_{suffix}"],complex)
            dt=np.asarray(frozen[f"{tag}_Z10_reduced_dot_{suffix}"],complex)
            sources[(grid,tag)]=r14.source_bundle_reduced_lambda(
                r7,mod6,mod7,bgs[(grid,tag)],rho,tag,r7.NX_PRIMARY,st,dt
            )

    raw=[]; global_norm=0.0
    for grid in ("primary","control"):
        for tag in r7.C_TAGS:
            x0=float(bgs[(grid,tag)]["x"][0])
            for beta in r7.BETAS:
                src=sources[(grid,tag)][beta]
                for m in r7.M_SOLVE:
                    k=float(m*r7.g9.K_REQ[0]/r7.FOURIER_N[0])
                    rr=np.asarray(src["rhs"][:,0,m],complex)
                    rc=np.asarray(src["rhs_constraint"][:,0,m],complex)
                    s=np.concatenate([rr,rc])
                    sn=float(np.linalg.norm(s))
                    global_norm=max(global_norm,sn)
                    raw.append((grid,tag,float(beta),int(m),k,x0,rr,rc,s,sn))

    per=[]; material=[]
    for grid,tag,beta,m,k,x0,rr,rc,source,sn in raw:
        mat=bool(sn>=MATERIAL_FLOOR*max(global_norm,TINY))
        bg=bgs[(grid,tag)]
        M,F,ZY,ZR,WY,WR,Cmat,bp,opdiag=r7._canonical_operator_matrices(
            mod6,mod7,bg,tag,k,x0
        )
        woff=WR@source
        lapse_row=Cmat[4]
        shift_row=Cmat[10]+Cmat[11]
        A=np.vstack([lapse_row@WY,shift_row@WY])
        b=np.asarray([
            rr[0]-lapse_row@woff,
            rc[0]-shift_row@woff
        ],complex)

        candidates={}
        for name,cols in (
            ("full_y",range(8)),
            ("q_only",range(4)),
            ("p_only",range(4,8)),
        ):
            x,diag=solve_subset(A,b,list(cols))
            y=np.zeros(8,complex)
            y[np.asarray(list(cols),int)]=x
            ev=evaluate_candidate(r7,Cmat,WY,WR,source,rr,rc,y)
            candidates[name]={**diag,**ev}

        rec={
            "grid":grid,"C":tag,"beta0":beta,"m":m,"k_Mpc":k,
            "source_norm":sn,"material_source_case":mat,
            "canonical_constraint_map_rank_full":candidates["full_y"]["coefficient_rank"],
            "canonical_constraint_augmented_rank_full":candidates["full_y"]["augmented_rank"],
            "local_algebraic_scaled_condition_2":float(opdiag["algebraic_scaled_condition_2"]),
            "candidates":candidates,
        }
        per.append(rec)
        if mat: material.append(rec)

    if not material:
        route="IMPLEMENTATION_FAIL"
    else:
        def full_pass(q):
            c=q["candidates"]["full_y"]
            return (
                c["relative_residual"]<=FULL_RES_MAX
                and c["algebraic_relative_residual"]<=ALG_MAX
                and c["lapse"]["metric"]<=CONSTRAINT_MAX
                and c["shift"]["metric"]<=CONSTRAINT_MAX
                and c["all_finite"]
            )
        route=(
            "FINITE_WINDOW_ZERO_BOUNDARY_INADMISSIBLE_SOURCE_COMPATIBLE"
            if all(full_pass(q) for q in material)
            else "QUADRATIC_SOURCE_INITIAL_NOETHER_INCOMPATIBILITY_CONFIRMED"
        )

    def aggregate(name):
        cc=[q["candidates"][name] for q in material]
        return {
            "relative_residual_max":float(max((x["relative_residual"] for x in cc),default=np.inf)),
            "lapse_backward_error_max":float(max((x["lapse"]["metric"] for x in cc),default=np.inf)),
            "shift_backward_error_max":float(max((x["shift"]["metric"] for x in cc),default=np.inf)),
            "algebraic_relative_residual_max":float(max((x["algebraic_relative_residual"] for x in cc),default=np.inf)),
            "solution_L2_max":float(max((x["solution_L2"] for x in cc),default=np.inf)),
            "rank_min":int(min((x["coefficient_rank"] for x in cc),default=0)),
            "rank_max":int(max((x["coefficient_rank"] for x in cc),default=0)),
            "augmented_rank_max":int(max((x["augmented_rank"] for x in cc),default=0)),
            "all_finite":bool(all(x["all_finite"] for x in cc)),
            "pass_count":int(sum(
                x["relative_residual"]<=FULL_RES_MAX
                and x["algebraic_relative_residual"]<=ALG_MAX
                and x["lapse"]["metric"]<=CONSTRAINT_MAX
                and x["shift"]["metric"]<=CONSTRAINT_MAX
                and x["all_finite"] for x in cc
            )),
            "case_count":len(cc),
        }

    report={
        "classification":"GE19_REPAIR17_FULL_CANONICAL_INITIAL_MANIFOLD_AUDIT_COMPLETE",
        "predata_classification":"GE19_REPAIR17_PREDATA_FULL_CANONICAL_INITIAL_MANIFOLD_AUDIT",
        "diagnostic_only":True,
        "provenance":{
            "Repair13_JSON_sha256":sha256(files["r13j"]),
            "Repair13_NPZ_sha256":sha256(files["r13n"]),
            "Repair14_JSON_sha256":sha256(files["r14"]),
            "Repair15_JSON_sha256":sha256(files["r15"]),
            "Repair16_JSON_sha256":sha256(files["r16"]),
            "H1_recomputed":False,
            "Z20_trajectory_recomputed":False,
            "time_integration_performed":False
        },
        "thresholds":{
            "full_y_constraint_relative_residual_max":FULL_RES_MAX,
            "reconstructed_independent_constraint_backward_error_max":CONSTRAINT_MAX,
            "eliminated_algebraic_relative_residual_max":ALG_MAX,
            "material_source_floor_relative_to_global_initial_source_max":MATERIAL_FLOOR,
        },
        "global":{
            "initial_source_norm_max":global_norm,
            "material_case_count":len(material),
            "all_case_count":len(per),
            "full_y":aggregate("full_y"),
            "q_only":aggregate("q_only"),
            "p_only":aggregate("p_only"),
            "local_algebraic_scaled_condition_2_max":float(max(
                (q["local_algebraic_scaled_condition_2"] for q in material),default=np.inf
            )),
        },
        "routing":{"next_route":route},
        "per_case":per,
        "claim_boundary":"Initial constraint-manifold existence audit only. No propagation result and no Z20 certification.",
    }

    out=Path(args.json_out); out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2,allow_nan=False)+"\n")
    print(json.dumps(report,indent=2,allow_nan=False))


if __name__=="__main__":
    main()
