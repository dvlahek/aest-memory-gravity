#!/usr/bin/env python3
"""GE19 Repair20 shift near-null + time-resolution audit.

Diagnostic only. Repeats the projected-boundary H3 march on Nt=32,64,128
using one common frozen Repair13 Nt64 Z10/Z10dot parent interpolated with
PCHIP. Records full per-time shift telemetry and separates structurally
near-null rows from active rows with the preregistered machine-precision
scale rule.

No physics/source/boundary/threshold change. No Z20 certification.
"""
from __future__ import annotations

import argparse, hashlib, importlib.util, json, math, sys
from pathlib import Path

import numpy as np
from scipy.interpolate import PchipInterpolator

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

TINY=1e-300
EPS=float(np.finfo(float).eps)
SQRT_EPS=float(np.sqrt(EPS))

REPAIR13_JSON_SHA="ae3cc790ecffbd5498b5852273c72ae578d4615de29bbb616673c05cdb3e74b7"
REPAIR13_NPZ_SHA="011c0ae54fd21d70c0e2c695ce62e7b74a3c5529a07c9023c882a447d5b40ca3"
REPAIR18_JSON_SHA="d5603138c2f488413686323d1241613f6ef707b586116aa7fe865ae25ceb0edc"
REPAIR19_JSON_SHA="32837e04a9ea6c83642a0d465f0312cc17a02ddad168760764f3c7b999a0a14d"
REPAIR19_NPZ_SHA="d638c86e48dd5c912629068f56c3780d0a611ed26ff5c161cd792a14328f7215"

NTS=(32,64,128)
LINEAR_MAX=1e-8
ANISO_MAX=1e-6
SHIFT_GATE=1e-6
STATE_MAX=5e-3
ORDER_MIN=2.5
P_REPRO_MAX=1e-12
PARENT_IDENTITY_MAX=1e-14
SOURCE_REPRO_MAX=1e-12
NEAR_NULL_ABS_RATIO_MAX=1000.0*EPS


def sha256(p:Path)->str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load_module(path:Path,name:str):
    spec=importlib.util.spec_from_file_location(name,path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def rel_l2(a,b):
    aa=np.asarray(a,complex)
    bb=np.asarray(b,complex)
    return float(np.linalg.norm(aa-bb)/max(np.linalg.norm(aa),np.linalg.norm(bb),TINY))


def complex_vec(pairs):
    return np.asarray([complex(float(z[0]),float(z[1])) for z in pairs],complex)


def pchip_complex(x,y,xnew):
    y=np.asarray(y,complex)
    re=PchipInterpolator(x,y.real,axis=-1,extrapolate=False)(xnew)
    im=PchipInterpolator(x,y.imag,axis=-1,extrapolate=False)(xnew)
    return np.asarray(re+1j*im,complex)


def state_grid_rel(xc,sc,xf,sf):
    interp=pchip_complex(np.asarray(xc,float),np.asarray(sc,complex),np.asarray(xf,float))
    return rel_l2(interp,sf)


def observed_order(e_coarse,e_fine,h_coarse,h_fine):
    if not all(np.isfinite(v) and v>0 for v in (e_coarse,e_fine,h_coarse,h_fine)):
        return float("nan")
    return float(math.log(e_coarse/e_fine)/math.log(h_coarse/h_fine))


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--results-dir",default=str(ROOT/"results"))
    ap.add_argument("--json-out",required=True)
    ap.add_argument("--npz-out",required=True)
    args=ap.parse_args()
    rd=Path(args.results_dir)

    files={
        "trace":rd/"ge15_R1_dense_accepted_step_trace.dat",
        "lambda":rd/"ge15_R1_cli_background.dat",
        "r13j":rd/"ge19_repair13_self_consistent_reduced_background_h1_reclosure.json",
        "r13n":rd/"ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz",
        "r18":rd/"ge19_repair18_zero_coordinate_constraint_projected_momentum_boundary.json",
        "r19j":rd/"ge19_repair19_projected_boundary_reduced_h3_z20_propagation.json",
        "r19n":rd/"ge19_repair19_projected_boundary_reduced_h3_z20_propagation.npz",
    }
    missing=[str(p) for p in files.values() if not p.exists()]
    if missing:
        raise RuntimeError("missing frozen inputs: "+", ".join(missing))

    expected={
        "r13j":REPAIR13_JSON_SHA,
        "r13n":REPAIR13_NPZ_SHA,
        "r18":REPAIR18_JSON_SHA,
        "r19j":REPAIR19_JSON_SHA,
        "r19n":REPAIR19_NPZ_SHA,
    }
    for key,h in expected.items():
        got=sha256(files[key])
        if got!=h:
            raise RuntimeError(f"{key} hash mismatch: {got}")

    d13=json.loads(files["r13j"].read_text())
    d18=json.loads(files["r18"].read_text())
    d19=json.loads(files["r19j"].read_text())
    if d13.get("stage_A_pass") is not True:
        raise RuntimeError("Repair13 Stage A not PASS")
    if d18.get("routing",{}).get("next_route")!="ZERO_COORDINATE_CONSTRAINT_PROJECTED_MOMENTUM_BOUNDARY_CERTIFIED":
        raise RuntimeError("Repair18 boundary not certified")
    if d19.get("classification")!="GE19_REPAIR19_PROJECTED_BOUNDARY_REDUCED_H3_Z20_PROPAGATION_FAIL":
        raise RuntimeError("Repair19 parent is not frozen FAIL")
    if d19.get("gates",{}).get("shift_constraint_backward_error_le_1e6") is not False:
        raise RuntimeError("Repair19 did not fail the frozen shift gate")

    r7=load_module(ROOT/"ge19/repair07_window_retarded_reduced_h3_z20_particular.py","r7r20")
    r11=load_module(ROOT/"ge19/repair11_lambda_inclusive_reduced_h1_reclosure.py","r11r20")
    r13=load_module(ROOT/"ge19/repair13_self_consistent_reduced_background_h1_reclosure.py","r13r20")
    r14=load_module(ROOT/"ge19/repair14_self_consistent_reduced_h3_z20_particular.py","r14r20")
    r18=load_module(ROOT/"ge19/repair18_zero_coordinate_constraint_projected_momentum_boundary.py","r18r20")

    mod6_frozen=r7.load_frozen_generator(
        ROOT/"ge06/analytic_aest_directional_source_generator.py","ge06r20"
    )
    mod6=r7.build_stable_ge06_generator_v2(mod6_frozen)
    mod7=r7.load_frozen_generator(
        ROOT/"ge07/pressureless_matter_directional_source_generator.py","ge07r20"
    )

    z13=np.load(files["r13n"])
    z19=np.load(files["r19n"])
    x_parent=np.asarray(z13["ln_a_primary"],float)

    # Frozen Repair18 reference p0, using primary rows only.
    p18={}
    for q in d18["per_case"]:
        if q["grid"]=="primary":
            p18[(q["C"],float(q["beta0"]),int(q["m"]))]=complex_vec(q["boundary"]["p"])

    # Build all backgrounds first, then install the exact frozen Lambda c1 operator.
    bases={}; rhos={}; bgs={}
    lambda_by_bg={}
    for nt in NTS:
        base,_,_=r7.build_ge15_reference(files["trace"],nt)
        rho=r11.interp_lambda(files["lambda"],base["x"])
        bases[nt]=base; rhos[nt]=rho
        for tag in r7.C_TAGS:
            bg,_=r13.reduced_background(r7,base,tag,rho)
            bgs[(nt,tag)]=bg
            lambda_by_bg[id(bg)]=rho
    r11.install_lambda_operator(r7,lambda_by_bg)

    # Common frozen H1 parent interpolation and source construction.
    parent_identity=0.0
    sources={}
    h1_interp={}
    for nt in NTS:
        xt=np.asarray(bases[nt]["x"],float)
        for tag in r7.C_TAGS:
            st0=np.asarray(z13[f"{tag}_Z10_reduced_primary"],complex)
            dt0=np.asarray(z13[f"{tag}_Z10_reduced_dot_primary"],complex)
            st=pchip_complex(x_parent,st0,xt)
            dt=pchip_complex(x_parent,dt0,xt)
            if nt==64:
                parent_identity=max(parent_identity,rel_l2(st,st0),rel_l2(dt,dt0))
            h1_interp[(nt,tag)]=(st,dt)
            sources[(nt,tag)]=r14.source_bundle_reduced_lambda(
                r7,mod6,mod7,bgs[(nt,tag)],rhos[nt],tag,r7.NX_PRIMARY,st,dt
            )

    if parent_identity>PARENT_IDENTITY_MAX:
        raise RuntimeError(f"Nt64 common-parent interpolation identity failed: {parent_identity}")

    # Reproduce frozen Repair19 Nt64 main RHS as an additional source-wiring control.
    source_repro=0.0
    beta_key={1.0:"beta1p0",0.5:"beta0p5",0.1:"beta0p1"}
    for tag in r7.C_TAGS:
        for beta in r7.BETAS:
            new=np.asarray(sources[(64,tag)][beta]["rhs"],complex)
            old=np.asarray(z19[f"{tag}_{beta_key[float(beta)]}_rhs_primary_m0_40"],complex)
            source_repro=max(source_repro,rel_l2(new,old))
    if source_repro>SOURCE_REPRO_MAX:
        raise RuntimeError(f"Repair19 Nt64 RHS reproduction failed: {source_repro}")

    arrays={}
    grid_reports={}
    all_finite=True
    boundary_repro_max=0.0

    for nt in NTS:
        x=np.asarray(bases[nt]["x"],float)
        h=float(abs(x[-1]-x[0])/(len(x)-1))
        grid_linear=0.0
        grid_aniso=0.0
        grid_lapse=0.0
        grid_all_shift=0.0
        grid_boundary_shift=0.0
        grid_boundary_alg=0.0
        grid_boundary_scaled=0.0
        grid_rank_min=99
        grid_rank_max=0

        for tag in r7.C_TAGS:
            nb=len(r7.BETAS); nm=len(r7.M_SOLVE)
            states=np.empty((nb,nm,6,nt),complex)
            metrics=np.empty((nb,nm,nt),float)
            absres=np.empty((nb,nm,nt),float)
            scales=np.empty((nb,nm,nt),float)
            lhsabs=np.empty((nb,nm,nt),float)
            srcabs=np.empty((nb,nm,nt),float)
            contrib=np.empty((nb,nm,nt),float)
            p0arr=np.empty((nb,nm,4),complex)

            for jm,m in enumerate(r7.M_SOLVE):
                k=float(m*r7.g9.K_REQ[0]/r7.FOURIER_N[0])
                rhsfun,confun=r7._source_interp(x,sources[(nt,tag)],m)
                r0=np.asarray(rhsfun(float(x[0])),complex)
                c0=np.asarray(confun(float(x[0])),complex)
                if r0.ndim==1: r0=r0[:,None]
                if c0.ndim==1: c0=c0[:,None]

                M,F,ZY,ZR,WY,WR,Cmat,bp,opdiag=r7._canonical_operator_matrices(
                    mod6,mod7,bgs[(nt,tag)],tag,k,float(x[0])
                )
                y0=np.zeros((8,nb),complex)

                for ib,beta in enumerate(r7.BETAS):
                    source0=np.concatenate([r0[:,ib],c0[:,ib]])
                    woff=WR@source0
                    lr=Cmat[4]; sr=Cmat[10]+Cmat[11]
                    Afull=np.vstack([lr@WY,sr@WY])
                    A=Afull[:,4:8]
                    b=np.asarray([r0[0,ib]-lr@woff,c0[0,ib]-sr@woff],complex)
                    p,sd=r18.projected_momentum_solve(A,b)
                    y0[4:8,ib]=p
                    p0arr[ib,jm]=p
                    ev=r18.evaluate_candidate(Cmat,WY,WR,source0,r0[:,ib],c0[:,ib],p)
                    pref=p18[(tag,float(beta),int(m))]
                    boundary_repro_max=max(boundary_repro_max,rel_l2(p,pref))
                    grid_boundary_shift=max(grid_boundary_shift,float(ev["shift"]["metric"]))
                    grid_boundary_alg=max(grid_boundary_alg,float(ev["algebraic_relative_residual"]))
                    grid_boundary_scaled=max(grid_boundary_scaled,float(sd["scaled_relative_residual_final"]))
                    grid_rank_min=min(grid_rank_min,int(sd["rank"]))
                    grid_rank_max=max(grid_rank_max,int(sd["rank"]))

                Y,rdiag=r7._radau2_integrate_canonical(
                    mod6,mod7,bgs[(nt,tag)],tag,k,y0,rhsfun,confun
                )
                st,dd,odiag=r7._reconstruct_canonical_solution(
                    mod6,mod7,bgs[(nt,tag)],tag,k,Y,rhsfun,confun
                )
                states[:,jm]=st
                grid_linear=max(
                    grid_linear,
                    float(rdiag["radau_block_scaled_relative_L2_residual_max"]),
                    float(odiag["algebraic_scaled_relative_L2_residual_max"]),
                    float(odiag["lapse_noether_row_relative_residual_max"]),
                )
                grid_aniso=max(grid_aniso,float(odiag["anisotropy_constraint_relative_L2_max"]))
                grid_lapse=max(grid_lapse,float(odiag["lapse_noether_row_relative_residual_max"]))
                grid_all_shift=max(grid_all_shift,float(odiag["shift_constraint_relative_L2_max"]))
                all_finite=bool(all_finite and odiag["all_outputs_finite"] and np.all(np.isfinite(Y)))

                # Per-time shift telemetry under the unchanged Repair07 definition.
                for it,xq in enumerate(x):
                    rr=np.asarray(rhsfun(float(xq)),complex)
                    rc=np.asarray(confun(float(xq)),complex)
                    if rr.ndim==1: rr=rr[:,None]
                    if rc.ndim==1: rc=rc[:,None]
                    MM,FF,ZZY,ZZR,WWY,WWR,CC,bbp,ddiag=r7._canonical_operator_matrices(
                        mod6,mod7,bgs[(nt,tag)],tag,k,float(xq)
                    )
                    for ib in range(nb):
                        y=Y[ib,:,it]
                        src=np.concatenate([rr[:,ib],rc[:,ib]])
                        w=WWY@y+WWR@src
                        smet=r7._constraint_backward_error(
                            CC[10]+CC[11],w,rc[0,ib],CC[10]@w,CC[11]@w
                        )
                        metrics[ib,jm,it]=smet["metric"]
                        absres[ib,jm,it]=smet["absolute_residual"]
                        scales[ib,jm,it]=smet["scale"]
                        lhsabs[ib,jm,it]=smet["lhs_abs"]
                        srcabs[ib,jm,it]=smet["source_abs"]
                        contrib[ib,jm,it]=smet["contribution_scale"]

            arrays[f"Nt{nt}_{tag}_state"]=states
            arrays[f"Nt{nt}_{tag}_shift_metric"]=metrics
            arrays[f"Nt{nt}_{tag}_shift_abs"]=absres
            arrays[f"Nt{nt}_{tag}_shift_scale"]=scales
            arrays[f"Nt{nt}_{tag}_shift_lhs_abs"]=lhsabs
            arrays[f"Nt{nt}_{tag}_shift_source_abs"]=srcabs
            arrays[f"Nt{nt}_{tag}_shift_contribution_scale"]=contrib
            arrays[f"Nt{nt}_{tag}_projected_p0"]=p0arr

        grid_reports[nt]={
            "Nt":nt,
            "h_ln_a":h,
            "linear_system_relative_L2_residual_max":grid_linear,
            "anisotropy_backward_error_max":grid_aniso,
            "lapse_noether_relative_residual_max":grid_lapse,
            "original_all_row_shift_backward_error_max":grid_all_shift,
            "boundary_shift_backward_error_max":grid_boundary_shift,
            "boundary_algebraic_relative_residual_max":grid_boundary_alg,
            "boundary_scaled_constraint_relative_residual_max":grid_boundary_scaled,
            "boundary_rank_min":int(grid_rank_min),
            "boundary_rank_max":int(grid_rank_max),
        }

    # Global Nt128 scale reference and frozen near-null classification.
    sref=max(float(np.max(arrays[f"Nt128_{tag}_shift_scale"])) for tag in r7.C_TAGS)
    null_threshold=SQRT_EPS*sref

    active_max={}; active_abs_max={}; near_abs_max={}
    active_count={}; null_count={}
    active_scale_min={}; active_scale_max={}
    worst_active={}; worst_all={}

    for nt in NTS:
        amax=-1.0; aa=-1.0; na=-1.0
        ac=0; nc=0
        smin=float("inf"); smax=0.0
        wa=None; wall=None; wallv=-1.0
        for tag in r7.C_TAGS:
            met=arrays[f"Nt{nt}_{tag}_shift_metric"]
            ab=arrays[f"Nt{nt}_{tag}_shift_abs"]
            sc=arrays[f"Nt{nt}_{tag}_shift_scale"]
            for ib,beta in enumerate(r7.BETAS):
                for jm,m in enumerate(r7.M_SOLVE):
                    for it,xq in enumerate(bases[nt]["x"]):
                        v=float(met[ib,jm,it]); av=float(ab[ib,jm,it]); sv=float(sc[ib,jm,it])
                        if v>wallv:
                            wallv=v
                            wall={"C":tag,"beta0":float(beta),"m":int(m),"time_index":int(it),"ln_a":float(xq),"metric":v,"absolute_residual":av,"scale":sv}
                        if sv<=null_threshold:
                            nc+=1; na=max(na,av)
                        else:
                            ac+=1
                            if v>amax:
                                amax=v
                                wa={"C":tag,"beta0":float(beta),"m":int(m),"time_index":int(it),"ln_a":float(xq),"metric":v,"absolute_residual":av,"scale":sv}
                            aa=max(aa,av); smin=min(smin,sv); smax=max(smax,sv)
        active_max[nt]=float(amax)
        active_abs_max[nt]=float(aa)
        near_abs_max[nt]=float(na)
        active_count[nt]=int(ac); null_count[nt]=int(nc)
        active_scale_min[nt]=float(smin)
        active_scale_max[nt]=float(smax)
        worst_active[nt]=wa; worst_all[nt]=wall

    # State convergence using common-parent ladder states.
    def all_state(nt):
        return np.concatenate([arrays[f"Nt{nt}_{tag}_state"].reshape(-1,nt) for tag in r7.C_TAGS],axis=0)
    s32=all_state(32); s64=all_state(64); s128=all_state(128)
    state_32_64=state_grid_rel(bases[32]["x"],s32,bases[64]["x"],s64)
    state_64_128=state_grid_rel(bases[64]["x"],s64,bases[128]["x"],s128)

    h32=grid_reports[32]["h_ln_a"]; h64=grid_reports[64]["h_ln_a"]; h128=grid_reports[128]["h_ln_a"]
    p3264=observed_order(active_max[32],active_max[64],h32,h64)
    p64128=observed_order(active_max[64],active_max[128],h64,h128)

    near_ratio_128=float(near_abs_max[128]/max(sref,TINY))

    controls={
        "Repair13_common_parent_Nt64_interpolation_identity_relative_L2_max":float(parent_identity),
        "Repair19_Nt64_main_RHS_reproduction_relative_L2_max":float(source_repro),
        "Repair18_projected_p0_reproduction_relative_L2_max":float(boundary_repro_max),
        "near_null_absolute_residual_over_Sref_Nt128":near_ratio_128,
        "active_Nt128_shift_relative_max":active_max[128],
        "active_observed_order_32_to_64":p3264,
        "active_observed_order_64_to_128":p64128,
        "state_relative_L2_32_to_64":state_32_64,
        "state_relative_L2_64_to_128":state_64_128,
        "linear_system_relative_L2_residual_max":float(max(grid_reports[n]["linear_system_relative_L2_residual_max"] for n in NTS)),
        "anisotropy_backward_error_max":float(max(grid_reports[n]["anisotropy_backward_error_max"] for n in NTS)),
        "all_outputs_finite":bool(all_finite),
    }

    gates={
        "common_parent_Nt64_identity_le_1e14":bool(parent_identity<=PARENT_IDENTITY_MAX),
        "Repair19_Nt64_RHS_reproduction_le_1e12":bool(source_repro<=SOURCE_REPRO_MAX),
        "Repair18_projected_p0_reproduction_le_1e12":bool(boundary_repro_max<=P_REPRO_MAX),
        "near_null_absolute_residual_over_Sref_le_1000eps":bool(near_ratio_128<=NEAR_NULL_ABS_RATIO_MAX),
        "active_Nt128_shift_relative_max_le_1e6":bool(active_max[128]<=SHIFT_GATE),
        "active_order_64_to_128_ge_2p5":bool(np.isfinite(p64128) and p64128>=ORDER_MIN),
        "state_64_to_128_relative_L2_le_5e3":bool(state_64_128<=STATE_MAX),
        "linear_system_relative_L2_residual_le_1e8":bool(controls["linear_system_relative_L2_residual_max"]<=LINEAR_MAX),
        "anisotropy_backward_error_le_1e6":bool(controls["anisotropy_backward_error_max"]<=ANISO_MAX),
        "all_outputs_finite":bool(all_finite),
    }

    route=(
        "NEAR_NULL_MONITOR_PLUS_TIME_TRUNCATION_CONFIRMED"
        if all(gates.values())
        else "ACTIVE_SHIFT_PROPAGATION_ISSUE_REMAINS"
    )

    report={
        "classification":"GE19_REPAIR20_SHIFT_NEAR_NULL_TIME_RESOLUTION_AUDIT_COMPLETE",
        "predata_classification":"GE19_REPAIR20_PREDATA_SHIFT_NEAR_NULL_TIME_RESOLUTION_AUDIT",
        "diagnostic_only":True,
        "provenance":{
            "Repair13_JSON_sha256":sha256(files["r13j"]),
            "Repair13_NPZ_sha256":sha256(files["r13n"]),
            "Repair18_JSON_sha256":sha256(files["r18"]),
            "Repair19_JSON_sha256":sha256(files["r19j"]),
            "Repair19_NPZ_sha256":sha256(files["r19n"]),
            "H1_recomputed":False,
            "physics_or_source_formula_edited":False,
            "shift_metric_definition_edited":False,
            "shift_threshold_relaxed":False,
        },
        "ladder":{
            "Nt":list(NTS),
            "Nx":int(r7.NX_PRIMARY),
            "common_parent":"Repair13 frozen Nt64 Z10/Z10dot with PCHIP real/imag interpolation",
            "expected_integrator_global_order":3,
        },
        "near_null_definition":{
            "machine_epsilon_float64":EPS,
            "sqrt_machine_epsilon":SQRT_EPS,
            "S_ref_Nt128":float(sref),
            "near_null_scale_threshold":float(null_threshold),
            "rule":"scale <= sqrt(eps)*S_ref_Nt128",
        },
        "per_grid":{
            str(nt):{
                **grid_reports[nt],
                "active_shift_relative_max":active_max[nt],
                "active_shift_absolute_residual_max":active_abs_max[nt],
                "near_null_shift_absolute_residual_max":near_abs_max[nt],
                "active_sample_count":active_count[nt],
                "near_null_sample_count":null_count[nt],
                "active_scale_min":active_scale_min[nt],
                "active_scale_max":active_scale_max[nt],
                "worst_active_sample":worst_active[nt],
                "worst_all_row_sample":worst_all[nt],
            } for nt in NTS
        },
        "controls":controls,
        "gates":gates,
        "routing":{"next_route":route},
        "interpretation_boundary":"Diagnostic only. A positive route does not relabel Repair19 or certify Z20; it only licenses a separately preregistered monitor/certification repair.",
        "claim_boundary":"No q20, H4/Z21, finite-eta, lensing or observational claim.",
    }

    outj=Path(args.json_out); outn=Path(args.npz_out)
    outj.parent.mkdir(parents=True,exist_ok=True); outn.parent.mkdir(parents=True,exist_ok=True)
    outj.write_text(json.dumps(report,indent=2,allow_nan=False)+"\n")
    arrays["x_Nt32"]=np.asarray(bases[32]["x"],float)
    arrays["x_Nt64"]=np.asarray(bases[64]["x"],float)
    arrays["x_Nt128"]=np.asarray(bases[128]["x"],float)
    np.savez_compressed(outn,**arrays)

    print(json.dumps(report,indent=2,allow_nan=False))


if __name__=="__main__":
    try:
        main()
    except Exception as exc:
        print(json.dumps({
            "classification":"GE19_REPAIR20_SHIFT_NEAR_NULL_TIME_RESOLUTION_AUDIT_IMPLEMENTATION_FAIL",
            "error":repr(exc),
        },indent=2))
        raise
