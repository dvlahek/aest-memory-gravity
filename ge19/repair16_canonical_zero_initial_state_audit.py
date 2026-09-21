#!/usr/bin/env python3
"""GE19 Repair16 canonical-zero initial-state audit.

Diagnostic only. Reconstructs the frozen Repair14 H3 source and tests the
natural canonical boundary y0=(q0,p0)=0. The frozen Noether-regularized
algebraic map then determines N20, delta_varrho20 and qdot20 locally.

No H1 or Z20 trajectory is recomputed.
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

ALG_MAX=1e-8
LAPSE_MAX=1e-6
SHIFT_MAX=1e-6
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


def row_backward_error(row,w,target):
    row=np.asarray(row,complex)
    w=np.asarray(w,complex)
    lhs=complex(row@w)
    target=complex(target)
    residual=lhs-target
    scale=max(abs(lhs),abs(target),float(np.sum(np.abs(row*w))),TINY)
    return {
        "metric":float(abs(residual)/scale),
        "absolute_residual":float(abs(residual)),
        "scale":float(scale),
        "lhs_abs":float(abs(lhs)),
        "target_abs":float(abs(target)),
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
        rd/"ge19_repair15_h3_initial_shift_noether_compatibility_audit.json",
    ]
    miss=[str(p) for p in required if not p.exists()]
    if miss:
        raise RuntimeError("missing frozen inputs: "+", ".join(miss))

    p13j=required[2]; p13n=required[3]; p14j=required[4]; p15j=required[5]
    if sha256(p13j)!=REPAIR13_JSON_SHA: raise RuntimeError("Repair13 JSON hash mismatch")
    if sha256(p13n)!=REPAIR13_NPZ_SHA: raise RuntimeError("Repair13 NPZ hash mismatch")
    if sha256(p14j)!=REPAIR14_JSON_SHA: raise RuntimeError("Repair14 JSON hash mismatch")
    if sha256(p15j)!=REPAIR15_JSON_SHA: raise RuntimeError("Repair15 JSON hash mismatch")

    d13=json.loads(p13j.read_text())
    d14=json.loads(p14j.read_text())
    d15=json.loads(p15j.read_text())
    if d13.get("stage_A_pass") is not True:
        raise RuntimeError("Repair13 parent Stage A not PASS")
    if d14.get("classification")!="GE19_REPAIR14_SELF_CONSISTENT_REDUCED_H3_Z20_PARTICULAR_FAIL":
        raise RuntimeError("Repair14 parent mismatch")
    if d15.get("routing",{}).get("next_route")!="INITIAL_SOURCE_INCOMPATIBILITY":
        raise RuntimeError("Repair15 did not license Repair16")

    r7=load_module(ROOT/"ge19/repair07_window_retarded_reduced_h3_z20_particular.py","r7r16")
    r11=load_module(ROOT/"ge19/repair11_lambda_inclusive_reduced_h1_reclosure.py","r11r16")
    r13=load_module(ROOT/"ge19/repair13_self_consistent_reduced_background_h1_reclosure.py","r13r16")
    r14=load_module(ROOT/"ge19/repair14_self_consistent_reduced_h3_z20_particular.py","r14r16")

    mod6_frozen=r7.load_frozen_generator(
        ROOT/"ge06/analytic_aest_directional_source_generator.py","ge06r16"
    )
    mod6=r7.build_stable_ge06_generator_v2(mod6_frozen)
    mod7=r7.load_frozen_generator(
        ROOT/"ge07/pressureless_matter_directional_source_generator.py","ge07r16"
    )

    dense=rd/"ge15_R1_dense_accepted_step_trace.dat"
    base64,_,_=r7.build_ge15_reference(dense,r7.NT_PRIMARY)
    base32,_,_=r7.build_ge15_reference(dense,r7.NT_CONTROL)
    rho64=r11.interp_lambda(rd/"ge15_R1_cli_background.dat",base64["x"])
    rho32=r11.interp_lambda(rd/"ge15_R1_cli_background.dat",base32["x"])
    frozen=np.load(p13n)

    bgs={}; sources={}; lambda_by_bg={}
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
            lambda_by_bg[id(bg)]=rho

    r11.install_lambda_operator(r7,lambda_by_bg)

    for grid,rho,suffix in (
        ("primary",rho64,"primary"),
        ("control",rho32,"control"),
    ):
        for tag in r7.C_TAGS:
            state=np.asarray(frozen[f"{tag}_Z10_reduced_{suffix}"],complex)
            dot=np.asarray(frozen[f"{tag}_Z10_reduced_dot_{suffix}"],complex)
            sources[(grid,tag)]=r14.source_bundle_reduced_lambda(
                r7,mod6,mod7,bgs[(grid,tag)],rho,tag,r7.NX_PRIMARY,state,dot
            )

    # Material-source normalization from the full initial source vector.
    raw=[]
    global_src_norm=0.0
    for grid in ("primary","control"):
        for tag in r7.C_TAGS:
            bg=bgs[(grid,tag)]
            x0=float(bg["x"][0])
            for beta in r7.BETAS:
                src=sources[(grid,tag)][beta]
                for m in r7.M_SOLVE:
                    k=float(m*r7.g9.K_REQ[0]/r7.FOURIER_N[0])
                    rr=np.asarray(src["rhs"][:,0,m],complex)
                    rc=np.asarray(src["rhs_constraint"][:,0,m],complex)
                    sv=np.concatenate([rr,rc])
                    sn=float(np.linalg.norm(sv))
                    global_src_norm=max(global_src_norm,sn)
                    raw.append((grid,tag,float(beta),int(m),k,x0,rr,rc,sn))

    rows=[]; material=[]
    algmax=0.0; lapsemax=0.0; shiftmax=0.0; anisomax=0.0
    qdotnormmax=0.0; condmax=0.0; finite=True

    for grid,tag,beta,m,k,x0,rr,rc,sn in raw:
        mat=bool(sn>=MATERIAL_FLOOR*max(global_src_norm,TINY))
        bg=bgs[(grid,tag)]
        M,F,ZY,ZR,WY,WR,Cmat,bp,opdiag=r7._canonical_operator_matrices(
            mod6,mod7,bg,tag,k,x0
        )
        y0=np.zeros(8,complex)
        source=np.concatenate([rr,rc])
        w=WY@y0+WR@source

        # Frozen algebraic partition: pS..pT, dust density, anisotropy.
        Calg=np.vstack([
            Cmat[0:4],
            Cmat[5:6],
            Cmat[12:13]+Cmat[13:14],
        ])
        target=np.concatenate([np.zeros(4,complex),[rr[5],rc[1]]])
        lhs=Calg@w
        rownorm=np.maximum(np.max(np.abs(Calg),axis=1),TINY)
        rs=(lhs-target)/rownorm
        ls=lhs/rownorm
        ts=target/rownorm
        alg=float(np.linalg.norm(rs)/max(np.linalg.norm(ls),np.linalg.norm(ts),TINY))

        lapse=row_backward_error(Cmat[4],w,rr[0])
        shift=r7._constraint_backward_error(
            Cmat[10]+Cmat[11],w,rc[0],Cmat[10]@w,Cmat[11]@w
        )
        aniso=r7._constraint_backward_error(
            Cmat[12]+Cmat[13],w,rc[1],Cmat[12]@w,Cmat[13]@w
        )

        qdot=np.asarray(w[[6,7,8,9]],complex)
        qdotnorm=float(np.linalg.norm(qdot))
        allfin=bool(np.all(np.isfinite(w)) and np.all(np.isfinite(qdot)))

        if mat:
            algmax=max(algmax,alg)
            lapsemax=max(lapsemax,lapse["metric"])
            shiftmax=max(shiftmax,shift["metric"])
            anisomax=max(anisomax,aniso["metric"])
            qdotnormmax=max(qdotnormmax,qdotnorm)
            condmax=max(condmax,float(opdiag["algebraic_scaled_condition_2"]))
            finite=bool(finite and allfin)

        rec={
            "grid":grid,"C":tag,"beta0":beta,"m":m,"k_Mpc":k,
            "source_norm":sn,"material_source_case":mat,
            "canonical_y0_zero":True,
            "algebraic_relative_residual":alg,
            "lapse":lapse,
            "shift":shift,
            "anisotropy":aniso,
            "determined_N_dr":[[float(w[i].real),float(w[i].imag)] for i in (0,1)],
            "determined_qdot":[[float(v.real),float(v.imag)] for v in qdot],
            "determined_qdot_L2":qdotnorm,
            "algebraic_scaled_condition_2":float(opdiag["algebraic_scaled_condition_2"]),
            "all_finite":allfin,
        }
        rows.append(rec)
        if mat: material.append(rec)

    if not material:
        route="IMPLEMENTATION_FAIL"
    elif algmax<=ALG_MAX and lapsemax<=LAPSE_MAX and shiftmax<=SHIFT_MAX and finite:
        route="CANONICAL_ZERO_INITIAL_STATE_CLOSES_CONSTRAINTS"
    else:
        route="QUADRATIC_SOURCE_NOETHER_INCOMPATIBILITY_REMAINS"

    report={
        "classification":"GE19_REPAIR16_CANONICAL_ZERO_INITIAL_STATE_AUDIT_COMPLETE",
        "predata_classification":"GE19_REPAIR16_PREDATA_CANONICAL_ZERO_INITIAL_STATE_AUDIT",
        "diagnostic_only":True,
        "provenance":{
            "Repair13_JSON_sha256":sha256(p13j),
            "Repair13_NPZ_sha256":sha256(p13n),
            "Repair14_JSON_sha256":sha256(p14j),
            "Repair15_JSON_sha256":sha256(p15j),
            "H1_recomputed":False,
            "Z20_trajectory_recomputed":False
        },
        "thresholds":{
            "algebraic_relative_residual_max":ALG_MAX,
            "independent_lapse_backward_error_max":LAPSE_MAX,
            "independent_shift_backward_error_max":SHIFT_MAX,
            "material_source_floor_relative_to_global_initial_source_max":MATERIAL_FLOOR
        },
        "global":{
            "initial_source_norm_max":global_src_norm,
            "material_case_count":len(material),
            "all_case_count":len(rows),
            "material_algebraic_relative_residual_max":algmax,
            "material_independent_lapse_backward_error_max":lapsemax,
            "material_independent_shift_backward_error_max":shiftmax,
            "material_anisotropy_backward_error_max":anisomax,
            "material_determined_qdot_L2_max":qdotnormmax,
            "material_local_algebraic_scaled_condition_2_max":condmax,
            "all_material_outputs_finite":finite
        },
        "routing":{"next_route":route},
        "per_case":rows,
        "claim_boundary":"Canonical-zero initial-surface audit only. No Repair14 trajectory is modified or recertified; q20 and H4/Z21 remain unlicensed."
    }

    out=Path(args.json_out)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2,allow_nan=False)+"\n")
    print(json.dumps(report,indent=2,allow_nan=False))


if __name__=="__main__":
    main()
