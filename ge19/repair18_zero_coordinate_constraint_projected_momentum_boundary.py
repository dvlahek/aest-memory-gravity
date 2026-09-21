#!/usr/bin/env python3
"""GE19 Repair18 zero-coordinate constraint-projected momentum boundary audit.

Diagnostic only. For the exact frozen Repair14 H3 source, keep the second-order
canonical coordinates q0=(S,u,phi,T)=0 at z=1.5 and determine only the
canonical momenta p0=(pS,pu,pphi,pT) from the independent lapse+shift
constraints using the preregistered doubly equilibrated minimum-norm rule
with exactly four iterative-refinement sweeps.

No H1 or Z20 trajectory is recomputed and no time integration is performed.
"""
from __future__ import annotations

import argparse, hashlib, importlib.util, json, sys
from pathlib import Path
import numpy as np
from scipy import linalg as sla

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

TINY=1e-300
REPAIR13_JSON_SHA="ae3cc790ecffbd5498b5852273c72ae578d4615de29bbb616673c05cdb3e74b7"
REPAIR13_NPZ_SHA="011c0ae54fd21d70c0e2c695ce62e7b74a3c5529a07c9023c882a447d5b40ca3"
REPAIR14_JSON_SHA="741da95a0aaffa31e27f2b05d42b8a7f011574013de8639812e453d7b130fe57"
REPAIR15_JSON_SHA="a8c86b6056a3d6ab2f6f443850bef34881452b4a11b32bb6a66e2ac7920f1e50"
REPAIR16_JSON_SHA="768d5a2de7cd62059e7149a4765ab5a9663eef708fc29989c05192f607c5bf68"
REPAIR17_JSON_SHA="f81ad8ef52eb3a7ff4d4286670a62c830f17872459f43812b059447f85e14184"

CONSTRAINT_RES_MAX=1e-8
CONSTRAINT_BE_MAX=1e-6
ALG_MAX=1e-8
MATERIAL_FLOOR=1e-12
REFINEMENT_SWEEPS=4


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


def projected_momentum_solve(A,b):
    """Frozen Repair18 2x4 doubly equilibrated min-norm solve + 4 refinements."""
    A=np.asarray(A,complex)
    b=np.asarray(b,complex)
    if A.shape!=(2,4) or b.shape!=(2,):
        raise ValueError(f"expected A=(2,4), b=(2,), got {A.shape}, {b.shape}")

    row_scale=np.maximum.reduce([
        np.max(np.abs(A),axis=1),
        np.abs(b),
        np.full(2,TINY,float),
    ])
    Ar=A/row_scale[:,None]
    br=b/row_scale

    col_scale=np.max(np.abs(Ar),axis=0)
    if np.any(~np.isfinite(col_scale)) or np.any(col_scale<=0.0):
        raise RuntimeError("zero/nonfinite Repair18 momentum column scale")
    As=Ar/col_scale[None,:]

    z,resid,rank,s=sla.lstsq(
        As,br,cond=None,lapack_driver="gelsd",check_finite=True
    )
    p=z/col_scale

    initial_scaled_residual=Ar@p-br
    refinement=[]
    for sweep in range(REFINEMENT_SWEEPS):
        r=b-A@p
        rr=r/row_scale
        dz,_,rank_i,s_i=sla.lstsq(
            As,rr,cond=None,lapack_driver="gelsd",check_finite=True
        )
        dp=dz/col_scale
        p=p+dp
        sr=Ar@p-br
        rel=float(np.linalg.norm(sr)/max(np.linalg.norm(Ar@p),np.linalg.norm(br),TINY))
        refinement.append({
            "sweep":int(sweep+1),
            "correction_scaled_L2":float(np.linalg.norm(dz)),
            "correction_p_L2":float(np.linalg.norm(dp)),
            "scaled_relative_residual":rel,
            "rank":int(rank_i),
            "singular_values":[float(v) for v in s_i],
        })

    final_scaled_residual=Ar@p-br
    final_rel=float(np.linalg.norm(final_scaled_residual)/max(
        np.linalg.norm(Ar@p),np.linalg.norm(br),TINY
    ))
    aug=np.column_stack([As,br])
    return p,{
        "scaled_relative_residual_initial":float(
            np.linalg.norm(initial_scaled_residual)/max(
                np.linalg.norm(Ar@(z/col_scale)),np.linalg.norm(br),TINY
            )
        ),
        "scaled_relative_residual_final":final_rel,
        "row_scales":[float(v) for v in row_scale],
        "column_scales":[float(v) for v in col_scale],
        "scaled_solution_L2":float(np.linalg.norm(col_scale*p)),
        "momentum_L2":float(np.linalg.norm(p)),
        "rank":int(rank),
        "augmented_rank":int(np.linalg.matrix_rank(aug)),
        "singular_values":[float(v) for v in s],
        "scaled_condition_nonzero":float(s[0]/s[-1]) if len(s)>=2 and s[-1]>0 else float("inf"),
        "refinement":refinement,
    }


def evaluate_candidate(Cmat,WY,WR,source,rr,rc,p):
    y=np.zeros(8,complex)
    y[4:8]=np.asarray(p,complex)
    w=WY@y+WR@source

    Calg=np.vstack([
        Cmat[0:4],
        Cmat[5:6],
        Cmat[12:13]+Cmat[13:14],
    ])
    target=np.concatenate([y[4:8],[rr[5],rc[1]]])
    lhs=Calg@w
    rownorm=np.maximum(np.max(np.abs(Calg),axis=1),TINY)
    rs=(lhs-target)/rownorm
    ls=lhs/rownorm
    ts=target/rownorm
    alg=float(np.linalg.norm(rs)/max(np.linalg.norm(ls),np.linalg.norm(ts),TINY))

    lapse=backward_error(Cmat[4],w,rr[0])
    shift=backward_error(Cmat[10]+Cmat[11],w,rc[0])
    aniso=backward_error(Cmat[12]+Cmat[13],w,rc[1])

    return {
        "algebraic_relative_residual":alg,
        "lapse":lapse,
        "shift":shift,
        "anisotropy":aniso,
        "q_L2":0.0,
        "p_L2":float(np.linalg.norm(p)),
        "all_finite":bool(np.all(np.isfinite(y)) and np.all(np.isfinite(w))),
        "p":[[float(z.real),float(z.imag)] for z in p],
        "determined_qdot":[[float(w[i].real),float(w[i].imag)] for i in (6,7,8,9)],
        "determined_qdot_L2":float(np.linalg.norm(w[[6,7,8,9]])),
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
        "r17":rd/"ge19_repair17_full_canonical_initial_manifold_audit.json",
    }
    miss=[str(p) for p in files.values() if not p.exists()]
    if miss: raise RuntimeError("missing frozen inputs: "+", ".join(miss))

    expected={
        "r13j":REPAIR13_JSON_SHA,"r13n":REPAIR13_NPZ_SHA,
        "r14":REPAIR14_JSON_SHA,"r15":REPAIR15_JSON_SHA,
        "r16":REPAIR16_JSON_SHA,"r17":REPAIR17_JSON_SHA,
    }
    for k,h in expected.items():
        got=sha256(files[k])
        if got!=h: raise RuntimeError(f"{k} hash mismatch: {got}")

    d13=json.loads(files["r13j"].read_text())
    d14=json.loads(files["r14"].read_text())
    d17=json.loads(files["r17"].read_text())
    if d13.get("stage_A_pass") is not True: raise RuntimeError("Repair13 Stage A not PASS")
    if d14.get("classification")!="GE19_REPAIR14_SELF_CONSISTENT_REDUCED_H3_Z20_PARTICULAR_FAIL":
        raise RuntimeError("Repair14 parent mismatch")
    if d17.get("classification")!="GE19_REPAIR17_FULL_CANONICAL_INITIAL_MANIFOLD_AUDIT_COMPLETE":
        raise RuntimeError("Repair17 classification mismatch")
    if d17.get("routing",{}).get("next_route")!="FINITE_WINDOW_ZERO_BOUNDARY_INADMISSIBLE_SOURCE_COMPATIBLE":
        raise RuntimeError("Repair17 route does not license Repair18")
    if d17.get("global",{}).get("full_y",{}).get("pass_count")!=714:
        raise RuntimeError("Repair17 full-y pass count mismatch")

    r7=load_module(ROOT/"ge19/repair07_window_retarded_reduced_h3_z20_particular.py","r7r18")
    r11=load_module(ROOT/"ge19/repair11_lambda_inclusive_reduced_h1_reclosure.py","r11r18")
    r13=load_module(ROOT/"ge19/repair13_self_consistent_reduced_background_h1_reclosure.py","r13r18")
    r14=load_module(ROOT/"ge19/repair14_self_consistent_reduced_h3_z20_particular.py","r14r18")

    mod6_frozen=r7.load_frozen_generator(
        ROOT/"ge06/analytic_aest_directional_source_generator.py","ge06r18"
    )
    mod6=r7.build_stable_ge06_generator_v2(mod6_frozen)
    mod7=r7.load_frozen_generator(
        ROOT/"ge07/pressureless_matter_directional_source_generator.py","ge07r18"
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
                    source=np.concatenate([rr,rc])
                    sn=float(np.linalg.norm(source))
                    global_norm=max(global_norm,sn)
                    raw.append((grid,tag,float(beta),int(m),k,x0,rr,rc,source,sn))

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

        # q=0, solve only p columns y[4:8].
        A_full=np.vstack([lapse_row@WY,shift_row@WY])
        A=A_full[:,4:8]
        b=np.asarray([
            rr[0]-lapse_row@woff,
            rc[0]-shift_row@woff,
        ],complex)

        p,diag=projected_momentum_solve(A,b)
        ev=evaluate_candidate(Cmat,WY,WR,source,rr,rc,p)

        # Descriptive comparison to the frozen Repair17 p-only witness.
        oldcase=None
        # keyed lookup is intentionally local and exact, avoiding assumptions
        # about per_case ordering in the frozen Repair17 file.
        for q in d17["per_case"]:
            if (
                q["grid"]==grid and q["C"]==tag
                and float(q["beta0"])==beta and int(q["m"])==m
            ):
                oldcase=q["candidates"]["p_only"]
                break
        if oldcase is None:
            raise RuntimeError(f"Repair17 p-only witness missing for {grid} {tag} beta={beta} m={m}")

        rec={
            "grid":grid,"C":tag,"beta0":beta,"m":m,"k_Mpc":k,
            "source_norm":sn,"material_source_case":mat,
            "boundary":{
                "q_exact_zero":True,
                "solver":diag,
                **ev,
            },
            "repair17_p_only_comparison":{
                "old_shift_metric":float(oldcase["shift"]["metric"]),
                "old_constraint_relative_residual":float(oldcase["relative_residual"]),
                "old_p_L2":float(oldcase["p_L2"]),
                "new_to_old_p_L2_ratio":float(ev["p_L2"]/max(float(oldcase["p_L2"]),TINY)),
            },
            "local_algebraic_scaled_condition_2":float(opdiag["algebraic_scaled_condition_2"]),
        }
        per.append(rec)
        if mat: material.append(rec)

    if not material:
        route="IMPLEMENTATION_FAIL"
    else:
        def ok(q):
            c=q["boundary"]
            return (
                c["solver"]["scaled_relative_residual_final"]<=CONSTRAINT_RES_MAX
                and c["lapse"]["metric"]<=CONSTRAINT_BE_MAX
                and c["shift"]["metric"]<=CONSTRAINT_BE_MAX
                and c["algebraic_relative_residual"]<=ALG_MAX
                and c["solver"]["rank"]==2
                and c["all_finite"]
            )
        if all(ok(q) for q in material):
            route="ZERO_COORDINATE_CONSTRAINT_PROJECTED_MOMENTUM_BOUNDARY_CERTIFIED"
        else:
            route="ZERO_COORDINATE_BOUNDARY_NUMERICALLY_UNRESOLVED"

    def mx(path):
        vals=[]
        for q in material:
            x=q
            for key in path: x=x[key]
            vals.append(float(x))
        return float(max(vals,default=np.inf))

    report={
        "classification":"GE19_REPAIR18_ZERO_COORDINATE_CONSTRAINT_PROJECTED_MOMENTUM_BOUNDARY_AUDIT_COMPLETE",
        "predata_classification":"GE19_REPAIR18_PREDATA_ZERO_COORDINATE_CONSTRAINT_PROJECTED_MOMENTUM_BOUNDARY",
        "diagnostic_only":True,
        "provenance":{
            "Repair13_JSON_sha256":sha256(files["r13j"]),
            "Repair13_NPZ_sha256":sha256(files["r13n"]),
            "Repair14_JSON_sha256":sha256(files["r14"]),
            "Repair15_JSON_sha256":sha256(files["r15"]),
            "Repair16_JSON_sha256":sha256(files["r16"]),
            "Repair17_JSON_sha256":sha256(files["r17"]),
            "H1_recomputed":False,
            "Z20_trajectory_recomputed":False,
            "time_integration_performed":False,
        },
        "boundary_rule":{
            "q0":"exactly zero",
            "p0":"doubly equilibrated minimum-norm 2x4 lapse+shift solve",
            "lapack_driver":"gelsd",
            "iterative_refinement_sweeps":REFINEMENT_SWEEPS,
        },
        "thresholds":{
            "constraint_scaled_relative_residual_max":CONSTRAINT_RES_MAX,
            "independent_lapse_backward_error_max":CONSTRAINT_BE_MAX,
            "independent_shift_backward_error_max":CONSTRAINT_BE_MAX,
            "eliminated_algebraic_relative_residual_max":ALG_MAX,
            "rank_required":2,
            "material_source_floor_relative_to_global_initial_source_max":MATERIAL_FLOOR,
        },
        "global":{
            "initial_source_norm_max":global_norm,
            "material_case_count":len(material),
            "all_case_count":len(per),
            "constraint_scaled_relative_residual_max":mx(["boundary","solver","scaled_relative_residual_final"]),
            "lapse_backward_error_max":mx(["boundary","lapse","metric"]),
            "shift_backward_error_max":mx(["boundary","shift","metric"]),
            "algebraic_relative_residual_max":mx(["boundary","algebraic_relative_residual"]),
            "anisotropy_backward_error_max":mx(["boundary","anisotropy","metric"]),
            "p_L2_max":mx(["boundary","p_L2"]),
            "determined_qdot_L2_max":mx(["boundary","determined_qdot_L2"]),
            "scaled_solution_L2_max":mx(["boundary","solver","scaled_solution_L2"]),
            "rank_min":int(min((q["boundary"]["solver"]["rank"] for q in material),default=0)),
            "rank_max":int(max((q["boundary"]["solver"]["rank"] for q in material),default=0)),
            "augmented_rank_max":int(max((q["boundary"]["solver"]["augmented_rank"] for q in material),default=0)),
            "all_material_outputs_finite":bool(all(q["boundary"]["all_finite"] for q in material)),
            "pass_count":int(sum(
                q["boundary"]["solver"]["scaled_relative_residual_final"]<=CONSTRAINT_RES_MAX
                and q["boundary"]["lapse"]["metric"]<=CONSTRAINT_BE_MAX
                and q["boundary"]["shift"]["metric"]<=CONSTRAINT_BE_MAX
                and q["boundary"]["algebraic_relative_residual"]<=ALG_MAX
                and q["boundary"]["solver"]["rank"]==2
                and q["boundary"]["all_finite"]
                for q in material
            )),
        },
        "routing":{"next_route":route},
        "per_case":per,
        "claim_boundary":"Finite-window initial-boundary certification only. No H3 propagation, Z20 certification, q20, H4/Z21 or observable claim.",
    }

    out=Path(args.json_out); out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2,allow_nan=False)+"\n")
    print(json.dumps(report,indent=2,allow_nan=False))


if __name__=="__main__":
    main()
