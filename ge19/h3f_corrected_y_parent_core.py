#!/usr/bin/env python3
"""GE19 H3F action-completed Y on-shell H1 parent / Z20 propagation core.

New, separately versioned source-corrected H3/Z20 core. Use exact frozen
non-Y GE06+GE07+Lambda sources and the complete Stage E Y aether+scalar
raw RHS rows. Recompute initial projected p0 from the new source with the
unchanged Repair18 algorithm. A legacy-Y control mode reproduces the
original unmodified Repair21 pipeline for comparison. No q20/H4 solve.
"""
from __future__ import annotations

import argparse, hashlib, importlib.util, json, math, sys
from pathlib import Path

import numpy as np
from scipy.interpolate import PchipInterpolator

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

import ge19.h3f_corrected_y_source_adapter as h3f_adapter

TINY=1e-300
EPS=float(np.finfo(float).eps)
SQRT_EPS=float(np.sqrt(EPS))

REPAIR13_JSON_SHA="ae3cc790ecffbd5498b5852273c72ae578d4615de29bbb616673c05cdb3e74b7"
REPAIR13_NPZ_SHA="011c0ae54fd21d70c0e2c695ce62e7b74a3c5529a07c9023c882a447d5b40ca3"
REPAIR18_JSON_SHA="d5603138c2f488413686323d1241613f6ef707b586116aa7fe865ae25ceb0edc"
REPAIR19_JSON_SHA="32837e04a9ea6c83642a0d465f0312cc17a02ddad168760764f3c7b999a0a14d"
REPAIR20_JSON_SHA="5f1dc8e48963c6403f142958c8ce34ab1457953b47868d1a65317655cd0644eb"
REPAIR20_NPZ_SHA="99937112b889bc556ada756bc7b4e834991a6019596fdbc353a40294ad3968a6"

NTS=(64,128)
H1_REPRO_MAX=1e-12
LINEAR_MAX=1e-8
SHIFT_MAX=1e-6
ANISO_MAX=1e-6
INIT_MAX=1e-10
STATE_MAX=5e-3
ORDER_MIN=2.5
BOUNDARY_REPRO_MAX=1e-12
NEAR_NULL_RATIO_MAX=1000.0*EPS


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


def observed_order(e64,e128,h64,h128):
    if not all(np.isfinite(v) and v>0 for v in (e64,e128,h64,h128)):
        return float("nan")
    return float(math.log(e64/e128)/math.log(h64/h128))


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--results-dir",default=str(ROOT/"results"))
    ap.add_argument("--json-out",required=True)
    ap.add_argument("--npz-out",required=True)
    ap.add_argument("--legacy-y-control",action="store_true")
    args=ap.parse_args()
    rd=Path(args.results_dir)

    files={
        "trace":rd/"ge15_R1_dense_accepted_step_trace.dat",
        "lambda":rd/"ge15_R1_cli_background.dat",
        "ge18n":rd/"ge18_repair01_on_shell_matched_dust_first_order_bridge.npz",
        "r13j":rd/"ge19_repair13_self_consistent_reduced_background_h1_reclosure.json",
        "r13n":rd/"ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz",
        "r18":rd/"ge19_repair18_zero_coordinate_constraint_projected_momentum_boundary.json",
        "r19":rd/"ge19_repair19_projected_boundary_reduced_h3_z20_propagation.json",
        "r20j":rd/"ge19_repair20_shift_near_null_time_resolution_audit.json",
        "r20n":rd/"ge19_repair20_shift_near_null_time_resolution_audit.npz",
    }
    missing=[str(p) for p in files.values() if not p.exists()]
    if missing:
        raise RuntimeError("missing frozen inputs: "+", ".join(missing))

    expected={
        "r13j":REPAIR13_JSON_SHA,
        "r13n":REPAIR13_NPZ_SHA,
        "r18":REPAIR18_JSON_SHA,
        "r19":REPAIR19_JSON_SHA,
        "r20j":REPAIR20_JSON_SHA,
        "r20n":REPAIR20_NPZ_SHA,
    }
    for key,h in expected.items():
        got=sha256(files[key])
        if got!=h:
            raise RuntimeError(f"{key} hash mismatch: {got}")

    d13=json.loads(files["r13j"].read_text())
    d18=json.loads(files["r18"].read_text())
    d19=json.loads(files["r19"].read_text())
    d20=json.loads(files["r20j"].read_text())
    if d13.get("stage_A_pass") is not True:
        raise RuntimeError("Repair13 parent not PASS")
    if d18.get("routing",{}).get("next_route")!="ZERO_COORDINATE_CONSTRAINT_PROJECTED_MOMENTUM_BOUNDARY_CERTIFIED":
        raise RuntimeError("Repair18 boundary not certified")
    if d19.get("classification")!="GE19_REPAIR19_PROJECTED_BOUNDARY_REDUCED_H3_Z20_PROPAGATION_FAIL":
        raise RuntimeError("Repair19 parent mismatch")
    if d20.get("routing",{}).get("next_route")!="ACTIVE_SHIFT_PROPAGATION_ISSUE_REMAINS":
        raise RuntimeError("Repair20 did not license Repair21")

    r7=load_module(ROOT/"ge19/repair07_window_retarded_reduced_h3_z20_particular.py","r7r21")
    r11=load_module(ROOT/"ge19/repair11_lambda_inclusive_reduced_h1_reclosure.py","r11r21")
    r13=load_module(ROOT/"ge19/repair13_self_consistent_reduced_background_h1_reclosure.py","r13r21")
    r14=load_module(ROOT/"ge19/repair14_self_consistent_reduced_h3_z20_particular.py","r14r21")
    r18=load_module(ROOT/"ge19/repair18_zero_coordinate_constraint_projected_momentum_boundary.py","r18r21")

    def h3f_bundle_local(r7arg,mod6arg,mod7arg,bg,rho_lambda,tag,nx,state,dot):
        if args.legacy_y_control:
            return r14.source_bundle_reduced_lambda(
                r7arg,mod6arg,mod7arg,bg,rho_lambda,tag,nx,state,dot
            )
        return h3f_adapter.source_bundle_reduced_lambda(
            r7arg,r14,mod6arg,mod7arg,bg,rho_lambda,tag,nx,state,dot
        )

    if sha256(files["ge18n"])!=r7.GE18_NPZ_SHA:
        raise RuntimeError("GE18 NPZ hash mismatch")
    if sha256(files["trace"])!=d13["provenance"]["GE15_dense_sha256"]:
        raise RuntimeError("GE15 dense trace hash mismatch")

    mod6_frozen=r7.load_frozen_generator(
        ROOT/"ge06/analytic_aest_directional_source_generator.py","ge06r21"
    )
    mod6=r7.build_stable_ge06_generator_v2(mod6_frozen)
    mod7=r7.load_frozen_generator(
        ROOT/"ge07/pressureless_matter_directional_source_generator.py","ge07r21"
    )
    ge18=np.load(files["ge18n"])
    z13=np.load(files["r13n"])

    # Frozen Repair18 primary projected momenta.
    p18={}
    for q in d18["per_case"]:
        if q["grid"]=="primary":
            p18[(q["C"],float(q["beta0"]),int(q["m"]))]=complex_vec(q["boundary"]["p"])

    bases={}; jets={}; rhos={}; bgs={}; lambda_by_bg={}
    for nt in NTS:
        base,_,j=r7.build_ge15_reference(files["trace"],nt)
        rho=r11.interp_lambda(files["lambda"],base["x"])
        bases[nt]=base; jets[nt]=j; rhos[nt]=rho
        for tag in r7.C_TAGS:
            bg,_=r13.reduced_background(r7,base,tag,rho)
            bgs[(nt,tag)]=bg
            lambda_by_bg[id(bg)]=rho
    r11.install_lambda_operator(r7,lambda_by_bg)

    # Genuine on-shell H1 solve on both grids.
    h1={}; h1dot={}; h1diag={}
    h1_linear=0.0; h1_shift=0.0; h1_aniso=0.0; h1_init=0.0; h1_finite=True
    repro_st=0.0; repro_dt=0.0

    for nt in NTS:
        for tag in r7.C_TAGS:
            ref,refdot=r7.reference_reduced_mode_state(
                bgs[(nt,tag)],jets[nt],ge18,tag
            )
            st,dt,diag=r7.solve_reduced_h1_case_canonical(
                mod6,mod7,bgs[(nt,tag)],tag,ref,refdot
            )
            h1[(nt,tag)]=st
            h1dot[(nt,tag)]=dt
            h1diag[(nt,tag)]=diag
            h1_linear=max(h1_linear,float(diag["linear_system_relative_L2_max"]))
            h1_shift=max(h1_shift,float(diag["shift_constraint_relative_L2_max"]))
            h1_aniso=max(h1_aniso,float(diag["anisotropy_constraint_relative_L2_max"]))
            h1_init=max(h1_init,float(diag["initial_dynamic_match_abs_or_rel_max"]))
            h1_finite=bool(h1_finite and diag["all_outputs_finite"])
            if nt==64:
                repro_st=max(repro_st,rel_l2(st,np.asarray(z13[f"{tag}_Z10_reduced_primary"],complex)))
                repro_dt=max(repro_dt,rel_l2(dt,np.asarray(z13[f"{tag}_Z10_reduced_dot_primary"],complex)))

    h1_state_conv=max(
        r7.reduced_h1_time_control(
            bgs[(128,tag)]["x"],h1[(128,tag)],
            bgs[(64,tag)]["x"],h1[(64,tag)]
        )["max"]
        for tag in r7.C_TAGS
    )

    # Counterfactual Repair20 interpolated Nt128 parent and source mismatch.
    x64=np.asarray(z13["x64"],float)
    x128=np.asarray(bases[128]["x"],float)
    interp_state_diff=0.0; interp_dot_diff=0.0
    interp_h1={}; interp_h1dot={}
    for tag in r7.C_TAGS:
        st0=np.asarray(z13[f"{tag}_Z10_reduced_primary"],complex)
        dt0=np.asarray(z13[f"{tag}_Z10_reduced_dot_primary"],complex)
        si=pchip_complex(x64,st0,x128)
        di=pchip_complex(x64,dt0,x128)
        interp_h1[tag]=si; interp_h1dot[tag]=di
        interp_state_diff=max(interp_state_diff,rel_l2(si,h1[(128,tag)]))
        interp_dot_diff=max(interp_dot_diff,rel_l2(di,h1dot[(128,tag)]))

    sources={}; interp_sources={}
    source_counterfactual_diff=0.0
    for nt in NTS:
        for tag in r7.C_TAGS:
            sources[(nt,tag)]=h3f_bundle_local(
                r7,mod6,mod7,bgs[(nt,tag)],rhos[nt],tag,r7.NX_PRIMARY,
                h1[(nt,tag)],h1dot[(nt,tag)]
            )
    for tag in r7.C_TAGS:
        interp_sources[tag]=h3f_bundle_local(
            r7,mod6,mod7,bgs[(128,tag)],rhos[128],tag,r7.NX_PRIMARY,
            interp_h1[tag],interp_h1dot[tag]
        )
        for beta in r7.BETAS:
            source_counterfactual_diff=max(
                source_counterfactual_diff,
                rel_l2(
                    interp_sources[tag][beta]["rhs"],
                    sources[(128,tag)][beta]["rhs"],
                ),
            )

    arrays={}; grid_report={}
    boundary_repro=0.0
    h3_linear=0.0; h3_aniso=0.0; h3_finite=True

    for nt in NTS:
        x=np.asarray(bases[nt]["x"],float)
        h=float(abs(x[-1]-x[0])/(len(x)-1))
        glin=0.0; gani=0.0; gallshift=0.0
        bshift=0.0; balg=0.0; bscaled=0.0
        for tag in r7.C_TAGS:
            nb=len(r7.BETAS); nm=len(r7.M_SOLVE)
            states=np.empty((nb,nm,6,nt),complex)
            metrics=np.empty((nb,nm,nt),float)
            absres=np.empty((nb,nm,nt),float)
            scales=np.empty((nb,nm,nt),float)
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
                    boundary_repro=max(
                        boundary_repro,
                        rel_l2(p,p18[(tag,float(beta),int(m))])
                    )
                    bshift=max(bshift,float(ev["shift"]["metric"]))
                    balg=max(balg,float(ev["algebraic_relative_residual"]))
                    bscaled=max(bscaled,float(sd["scaled_relative_residual_final"]))

                Y,rdiag=r7._radau2_integrate_canonical(
                    mod6,mod7,bgs[(nt,tag)],tag,k,y0,rhsfun,confun
                )
                st,dd,odiag=r7._reconstruct_canonical_solution(
                    mod6,mod7,bgs[(nt,tag)],tag,k,Y,rhsfun,confun
                )
                states[:,jm]=st
                glin=max(
                    glin,
                    float(rdiag["radau_block_scaled_relative_L2_residual_max"]),
                    float(odiag["algebraic_scaled_relative_L2_residual_max"]),
                    float(odiag["lapse_noether_row_relative_residual_max"]),
                )
                gani=max(gani,float(odiag["anisotropy_constraint_relative_L2_max"]))
                gallshift=max(gallshift,float(odiag["shift_constraint_relative_L2_max"]))
                h3_finite=bool(h3_finite and odiag["all_outputs_finite"] and np.all(np.isfinite(Y)))

                for it,xq in enumerate(x):
                    rr=np.asarray(rhsfun(float(xq)),complex)
                    rc=np.asarray(confun(float(xq)),complex)
                    if rr.ndim==1: rr=rr[:,None]
                    if rc.ndim==1: rc=rc[:,None]
                    MM,FF,ZZY,ZZR,WWY,WWR,CC,bbp,ddiag=r7._canonical_operator_matrices(
                        mod6,mod7,bgs[(nt,tag)],tag,k,float(xq)
                    )
                    for ib in range(nb):
                        src=np.concatenate([rr[:,ib],rc[:,ib]])
                        w=WWY@Y[ib,:,it]+WWR@src
                        sm=r7._constraint_backward_error(
                            CC[10]+CC[11],w,rc[0,ib],CC[10]@w,CC[11]@w
                        )
                        metrics[ib,jm,it]=sm["metric"]
                        absres[ib,jm,it]=sm["absolute_residual"]
                        scales[ib,jm,it]=sm["scale"]

            arrays[f"Nt{nt}_{tag}_state"]=states
            arrays[f"Nt{nt}_{tag}_shift_metric"]=metrics
            arrays[f"Nt{nt}_{tag}_shift_abs"]=absres
            arrays[f"Nt{nt}_{tag}_shift_scale"]=scales
            arrays[f"Nt{nt}_{tag}_projected_p0"]=p0arr

        grid_report[nt]={
            "Nt":nt,
            "h_ln_a":h,
            "linear_system_relative_L2_residual_max":glin,
            "anisotropy_backward_error_max":gani,
            "original_all_row_shift_backward_error_max":gallshift,
            "boundary_shift_backward_error_max":bshift,
            "boundary_algebraic_relative_residual_max":balg,
            "boundary_scaled_constraint_relative_residual_max":bscaled,
        }
        h3_linear=max(h3_linear,glin)
        h3_aniso=max(h3_aniso,gani)

    # On-shell Nt128 near-null rule.
    sref=max(float(np.max(arrays[f"Nt128_{tag}_shift_scale"])) for tag in r7.C_TAGS)
    null_thr=SQRT_EPS*sref

    # Matched Nt128 common-grid metric fields.
    matched64=[]; matched128=[]
    near_abs=[]
    active_count=0; null_count=0
    worst128=None; worst128v=-1.0

    for tag in r7.C_TAGS:
        m64=arrays[f"Nt64_{tag}_shift_metric"]
        m128=arrays[f"Nt128_{tag}_shift_metric"]
        a128=arrays[f"Nt128_{tag}_shift_abs"]
        s128=arrays[f"Nt128_{tag}_shift_scale"]
        x64g=np.asarray(bases[64]["x"],float)
        x128g=np.asarray(bases[128]["x"],float)

        for ib,beta in enumerate(r7.BETAS):
            for jm,m in enumerate(r7.M_SOLVE):
                c64=PchipInterpolator(x64g,m64[ib,jm],extrapolate=False)(x128g)
                mask=s128[ib,jm]>null_thr
                nmask=~mask
                if np.any(mask):
                    matched64.extend(np.asarray(c64[mask],float).tolist())
                    matched128.extend(np.asarray(m128[ib,jm,mask],float).tolist())
                    active_count+=int(np.count_nonzero(mask))
                    loc=np.argmax(np.where(mask,m128[ib,jm],-np.inf))
                    v=float(m128[ib,jm,loc])
                    if v>worst128v:
                        worst128v=v
                        worst128={
                            "C":tag,"beta0":float(beta),"m":int(m),
                            "time_index":int(loc),"ln_a":float(x128g[loc]),
                            "metric":v,
                            "absolute_residual":float(a128[ib,jm,loc]),
                            "scale":float(s128[ib,jm,loc]),
                        }
                if np.any(nmask):
                    near_abs.extend(np.asarray(a128[ib,jm,nmask],float).tolist())
                    null_count+=int(np.count_nonzero(nmask))

    matched64=np.asarray(matched64,float)
    matched128=np.asarray(matched128,float)
    e64_inf=float(np.max(matched64))
    e128_inf=float(np.max(matched128))
    e64_l2=float(np.sqrt(np.mean(matched64**2)))
    e128_l2=float(np.sqrt(np.mean(matched128**2)))
    h64=grid_report[64]["h_ln_a"]; h128=grid_report[128]["h_ln_a"]
    p_inf=observed_order(e64_inf,e128_inf,h64,h128)
    p_l2=observed_order(e64_l2,e128_l2,h64,h128)
    near_ratio=float(max(near_abs,default=0.0)/max(sref,TINY))

    # H3 state convergence on on-shell-parent runs.
    def all_state(nt):
        return np.concatenate([
            arrays[f"Nt{nt}_{tag}_state"].reshape(-1,nt)
            for tag in r7.C_TAGS
        ],axis=0)
    h3_state_conv=state_grid_rel(
        bases[64]["x"],all_state(64),
        bases[128]["x"],all_state(128)
    )

    h1_gates={
        "Nt64_Z10_reproduction_le_1e12":bool(repro_st<=H1_REPRO_MAX),
        "Nt64_Z10dot_reproduction_le_1e12":bool(repro_dt<=H1_REPRO_MAX),
        "linear_system_relative_L2_residual_le_1e8":bool(h1_linear<=LINEAR_MAX),
        "shift_constraint_backward_error_le_1e6":bool(h1_shift<=SHIFT_MAX),
        "anisotropy_constraint_backward_error_le_1e6":bool(h1_aniso<=ANISO_MAX),
        "initial_dynamic_match_le_1e10":bool(h1_init<=INIT_MAX),
        "Nt64_vs_Nt128_state_relative_L2_le_5e3":bool(h1_state_conv<=STATE_MAX),
        "all_outputs_finite":bool(h1_finite),
    }

    diag_gates={
        "near_null_absolute_residual_over_Sref_le_1000eps":bool(near_ratio<=NEAR_NULL_RATIO_MAX),
        "active_Nt128_shift_Linf_le_1e6":bool(e128_inf<=SHIFT_MAX),
        "matched_active_Linf_order_ge_2p5":bool(np.isfinite(p_inf) and p_inf>=ORDER_MIN),
        "matched_active_L2_order_ge_2p5":bool(np.isfinite(p_l2) and p_l2>=ORDER_MIN),
        "H3_state_Nt64_vs_Nt128_relative_L2_le_5e3":bool(h3_state_conv<=STATE_MAX),
        "H3_linear_system_relative_L2_residual_le_1e8":bool(h3_linear<=LINEAR_MAX),
        "H3_anisotropy_backward_error_le_1e6":bool(h3_aniso<=ANISO_MAX),
        "source_aware_boundary_shift_le_1e6":bool(bshift<=SHIFT_MAX),
        "source_aware_boundary_scaled_constraint_le_1e8":bool(bscaled<=LINEAR_MAX),
        "source_aware_boundary_algebraic_le_1e8":bool(balg<=LINEAR_MAX),
        "all_outputs_finite":bool(h3_finite),
    }

    if not all(h1_gates.values()):
        route="IMPLEMENTATION_FAIL"
    elif all(diag_gates.values()):
        route=("H3F_LEGACY_Y_CONTROL_PASS" if args.legacy_y_control
               else "H3F_CORRECTED_SOURCE_DIAGNOSTIC_GATES_PASS")
    else:
        route=("H3F_LEGACY_Y_CONTROL_FAIL" if args.legacy_y_control
               else "H3F_CORRECTED_SOURCE_SCIENCE_GATE_FAIL")

    report={
        "classification":("GE19_H3F_LEGACY_Y_CONTROL_COMPLETE" if args.legacy_y_control
                          else "GE19_H3F_CORRECTED_Y_PARENT_CORE_COMPLETE"),
        "predata_classification":"GE19_H3F_PREDATA_ACTION_COMPLETED_Y_Z20_PARENT_RECLOSURE",
        "diagnostic_only":True,
        "provenance":{
            "Repair13_JSON_sha256":sha256(files["r13j"]),
            "Repair13_NPZ_sha256":sha256(files["r13n"]),
            "Repair18_JSON_sha256":sha256(files["r18"]),
            "Repair19_JSON_sha256":sha256(files["r19"]),
            "Repair20_JSON_sha256":sha256(files["r20j"]),
            "Repair20_NPZ_sha256":sha256(files["r20n"]),
            "H1_recomputed_at_target_resolutions":True,
            "historical_physics_modules_edited":False,
            "StageE_Y_source_used":bool(not args.legacy_y_control),
            "legacy_Y_control":bool(args.legacy_y_control),
            "shift_metric_definition_edited":False,
            "shift_threshold_relaxed":False,
        },
        "H1_on_shell_controls":{
            "Nt64_Z10_reproduction_relative_L2_max":repro_st,
            "Nt64_Z10dot_reproduction_relative_L2_max":repro_dt,
            "linear_system_relative_L2_residual_max":h1_linear,
            "shift_constraint_backward_error_max":h1_shift,
            "anisotropy_constraint_backward_error_max":h1_aniso,
            "initial_dynamic_match_abs_or_rel_max":h1_init,
            "Nt64_vs_Nt128_state_relative_L2_max":h1_state_conv,
            "all_outputs_finite":h1_finite,
            "gates":h1_gates,
        },
        "Repair20_interpolated_parent_counterfactual":{
            "Nt128_Z10_relative_L2_vs_on_shell_max":interp_state_diff,
            "Nt128_Z10dot_relative_L2_vs_on_shell_max":interp_dot_diff,
            "Nt128_H3_main_RHS_relative_L2_vs_on_shell_max":source_counterfactual_diff,
        },
        "near_null_definition":{
            "machine_epsilon_float64":EPS,
            "sqrt_machine_epsilon":SQRT_EPS,
            "S_ref_Nt128":sref,
            "near_null_scale_threshold":null_thr,
            "rule":"Nt128 on-shell scale <= sqrt(eps)*S_ref_Nt128",
        },
        "per_grid":{str(nt):grid_report[nt] for nt in NTS},
        "matched_shift":{
            "common_grid":"Nt128",
            "active_sample_count":active_count,
            "near_null_sample_count":null_count,
            "Nt64_interpolated_active_Linf":e64_inf,
            "Nt128_active_Linf":e128_inf,
            "Nt64_interpolated_active_L2":e64_l2,
            "Nt128_active_L2":e128_l2,
            "observed_order_Linf":p_inf,
            "observed_order_L2":p_l2,
            "near_null_absolute_residual_over_Sref_Nt128":near_ratio,
            "worst_Nt128_active_sample":worst128,
        },
        "H3_controls":{
            "state_Nt64_vs_Nt128_relative_L2":h3_state_conv,
            "linear_system_relative_L2_residual_max":h3_linear,
            "anisotropy_backward_error_max":h3_aniso,
            "historical_Repair18_p0_difference_report_only":boundary_repro,
            "all_outputs_finite":h3_finite,
            "gates":diag_gates,
        },
        "routing":{"next_route":route},
        "interpretation_boundary":"H3F source-corrected core/legacy control only. New Z20 is not certified until the separate preregistered H3F source/boundary/science certification gates pass.",
        "claim_boundary":"No q20, H4/Z21, finite eta, lensing or observational claim.",
    }

    outj=Path(args.json_out); outn=Path(args.npz_out)
    outj.parent.mkdir(parents=True,exist_ok=True); outn.parent.mkdir(parents=True,exist_ok=True)
    outj.write_text(json.dumps(report,indent=2,allow_nan=False)+"\n")

    arrays["x_Nt64"]=np.asarray(bases[64]["x"],float)
    arrays["x_Nt128"]=np.asarray(bases[128]["x"],float)
    for nt in NTS:
        for tag in r7.C_TAGS:
            arrays[f"Nt{nt}_{tag}_H1_state"]=h1[(nt,tag)]
            arrays[f"Nt{nt}_{tag}_H1_dot"]=h1dot[(nt,tag)]
    np.savez_compressed(outn,**arrays)

    print(json.dumps(report,indent=2,allow_nan=False))


if __name__=="__main__":
    try:
        main()
    except Exception as exc:
        print(json.dumps({
            "classification":"GE19_H3F_CORRECTED_Y_PARENT_CORE_IMPLEMENTATION_FAIL",
            "error":repr(exc),
        },indent=2))
        raise
