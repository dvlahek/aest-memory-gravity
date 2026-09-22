#!/usr/bin/env python3
"""GE19 Repair31 — artifact-only audit of the frozen Repair30 H2 FAIL.

No H2 integration is performed. This script re-evaluates diagnostics on the
already frozen Repair30 states and mapped Repair29B R2 reference.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.interpolate import PchipInterpolator

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

import ge19.repair07_window_retarded_reduced_h3_z20_particular as r7
import ge19.repair11_lambda_inclusive_reduced_h1_reclosure as r11
import ge19.repair30_reduced_h2_z11_reclosure as r30

R30_JSON_SHA="de2d282eb0729b12f96e08be434b7bc0a320a606dd96d94057f1a2c94af22ce5"
R30_NPZ_SHA="02d7d9d52ca53f2495b84e5a339d396b3f63f9b03d05fd5416dcd4012c454429"
SQRT_EPS=math.sqrt(np.finfo(float).eps)
TINY=1e-300

EQ_NAMES=("lapse","isotropic_spatial","aether_rapidity","scalar_phi","dust_potential","dust_density")
FIELD_NAMES=("N","S","u","varphi","T","delta_varrho")
DYN_IDX=(1,2,3,4)


def sha256(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1<<20),b""):
            h.update(block)
    return h.hexdigest()


def rel_l2(a,b)->float:
    aa=np.asarray(a); bb=np.asarray(b)
    return float(np.linalg.norm(aa-bb)/max(np.linalg.norm(aa),np.linalg.norm(bb),TINY))


def aor(a,b)->float:
    aa=np.asarray(a); bb=np.asarray(b)
    ae=np.abs(aa-bb)
    re=ae/np.maximum(np.maximum(np.abs(aa),np.abs(bb)),TINY)
    return float(np.max(np.minimum(ae,re)))


def interp_complex(x0,y0,x):
    yy=np.asarray(y0,complex)
    re=PchipInterpolator(x0,yy.real,axis=-1,extrapolate=False)(x)
    im=PchipInterpolator(x0,yy.imag,axis=-1,extrapolate=False)(x)
    return np.asarray(re+1j*im,complex)


def build_operator_context(results:Path):
    dense=results/"ge15_R1_dense_accepted_step_trace.dat"
    r13n=results/"ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz"
    if not dense.exists() or not r13n.exists():
        raise RuntimeError("missing frozen GE15/Repair13 local parents required only to reconstruct the unchanged operator")
    if sha256(dense)!=r30.GE15_DENSE_SHA:
        raise RuntimeError("GE15 dense hash mismatch")
    if sha256(r13n)!=r30.R13_NPZ_SHA:
        raise RuntimeError("Repair13 NPZ hash mismatch")
    z13=np.load(r13n)
    bgs,bases,base_states,lambda_by_bg,bgdiag=r30.build_backgrounds(dense,z13)
    r11.install_lambda_operator(r7,lambda_by_bg)
    mod6f=r7.load_frozen_generator(ROOT/"ge06/analytic_aest_directional_source_generator.py","ge06r31")
    mod6=r7.build_stable_ge06_generator_v2(mod6f)
    mod7=r7.load_frozen_generator(ROOT/"ge07/pressureless_matter_directional_source_generator.py","ge07r31")
    return bgs,bases,mod6,mod7,bgdiag


def state_precision(z):
    xp=np.asarray(z["x_primary"],float)
    xc=np.asarray(z["x_control"],float)
    rows=[]
    global_max=0.0; dyn_max=0.0
    for tag in r7.C_TAGS:
        sp=np.asarray(z[f"{tag}_Z11_primary"],complex)
        sc=np.asarray(z[f"{tag}_Z11_control"],complex)
        si=interp_complex(xp,sp,xc)
        per={}
        for iv,name in enumerate(FIELD_NAMES):
            per[name]=rel_l2(si[:,iv],sc[:,iv])
        glob=rel_l2(si,sc)
        dyn=rel_l2(si[:,DYN_IDX],sc[:,DYN_IDX])
        dabs=float(np.linalg.norm(si[:,5]-sc[:,5]))
        dp=float(np.linalg.norm(si[:,5]))
        dc=float(np.linalg.norm(sc[:,5]))
        rows.append({
            "C":tag,
            "per_field_relative_L2":per,
            "full_six_field_global_relative_L2":glob,
            "dynamic_S_u_varphi_T_global_relative_L2":dyn,
            "delta_varrho_absolute_L2_difference":dabs,
            "delta_varrho_primary_interp_L2":dp,
            "delta_varrho_control_L2":dc,
        })
        global_max=max(global_max,glob)
        dyn_max=max(dyn_max,dyn)
    return {
        "per_C":rows,
        "full_six_field_global_relative_L2_max":global_max,
        "dynamic_global_relative_L2_max":dyn_max,
    }


def chi_audit(z):
    parent=np.asarray(z["R2_parent_chi11_positive"],complex)
    rows=[]; scales=[]; relmax=0.0; postmax=0.0; cosmin=1.0; initmax=0.0
    for tag in r7.C_TAGS:
        red=np.asarray(z[f"{tag}_chi11_primary"],complex)
        modes=[]
        for ik,k in enumerate(r7.g9.K_REQ):
            a=red[ik]; b=parent[ik]
            rr=rel_l2(a,b)
            den=np.vdot(a,a)
            c=(np.vdot(a,b)/den) if abs(den)>TINY else complex(np.nan,np.nan)
            fit=c*a
            post=float(np.linalg.norm(fit-b)/max(np.linalg.norm(b),TINY))
            cos=float(abs(np.vdot(a,b))/max(np.linalg.norm(a)*np.linalg.norm(b),TINY))
            ini=aor([a[0]],[b[0]])
            scales.append(c); relmax=max(relmax,rr); postmax=max(postmax,post); cosmin=min(cosmin,cos); initmax=max(initmax,ini)
            modes.append({
                "k_Mpc":float(k),
                "relative_L2":rr,
                "shape_cosine":cos,
                "best_complex_scale_reduced_to_parent":[float(c.real),float(c.imag)],
                "best_scale_magnitude":float(abs(c)),
                "best_scale_phase_rad":float(np.angle(c)),
                "postfit_relative_L2":post,
                "initial_abs_or_rel":ini,
            })
        rows.append({"C":tag,"per_mode":modes})
    mags=np.asarray([abs(q) for q in scales],float)
    return {
        "per_C":rows,
        "relative_L2_max":relmax,
        "shape_cosine_min":cosmin,
        "postfit_relative_L2_max":postmax,
        "initial_abs_or_rel_max":initmax,
        "best_scale_magnitude_mean":float(np.mean(mags)),
        "best_scale_magnitude_std":float(np.std(mags)),
        "best_scale_magnitude_relative_std":float(np.std(mags)/max(np.mean(mags),TINY)),
    }


def equation_metrics(main,rhs):
    out={}
    for ie,name in enumerate(EQ_NAMES):
        lhs=np.asarray(main[ie],complex)
        rr=np.asarray(rhs[ie],complex)
        res=lhs-rr
        out[name]={
            "relative_L2":float(np.linalg.norm(res)/max(np.linalg.norm(lhs),np.linalg.norm(rr),TINY)),
            "absolute_L2":float(np.linalg.norm(res)),
            "lhs_L2":float(np.linalg.norm(lhs)),
            "rhs_L2":float(np.linalg.norm(rr)),
        }
    return out


def operator_audit(z,bgs,mod6,mod7):
    rows=[]
    aggregate={"solution":{n:[] for n in EQ_NAMES},"reference":{n:[] for n in EQ_NAMES}}
    conagg={"solution":{"shift":[],"anisotropy":[]},"reference":{"shift":[],"anisotropy":[]}}

    for nt,label in ((128,"primary"),(64,"control")):
        for tag in r7.C_TAGS:
            bg=bgs[(nt,tag)]
            rhsall=np.asarray(z[f"{tag}_M1_rhs_{label}"],complex)
            for ik,m in enumerate(r7.FOURIER_N):
                k=float(m*r7.g9.K_REQ[0]/r7.FOURIER_N[0])
                one={"Nt":nt,"C":tag,"m":int(m)}
                for kind,key in (
                    ("solution",f"{tag}_Z11_{label}"),
                    ("reference",f"{tag}_Z11_reference_{label}"),
                ):
                    st=np.asarray(z[key],complex)[ik]
                    Y=st[:,:,None]
                    main,con=r7.linear_operator_batch(mod6,mod7,bg,tag,k,Y)
                    main=np.asarray(main[:,:,0],complex)
                    con=np.asarray(con[:,:,0],complex)
                    rhs=np.asarray(rhsall[ik],complex)
                    met=equation_metrics(main,rhs)
                    one[kind]={
                        "main":met,
                        "shift_relative_to_operator_scale":float(np.linalg.norm(con[0])/max(np.linalg.norm(main),np.linalg.norm(rhs),TINY)),
                        "anisotropy_relative_to_operator_scale":float(np.linalg.norm(con[1])/max(np.linalg.norm(main),np.linalg.norm(rhs),TINY)),
                        "shift_absolute_L2":float(np.linalg.norm(con[0])),
                        "anisotropy_absolute_L2":float(np.linalg.norm(con[1])),
                    }
                    for name in EQ_NAMES:
                        aggregate[kind][name].append((met[name]["absolute_L2"],met[name]["lhs_L2"],met[name]["rhs_L2"]))
                    conagg[kind]["shift"].append((float(np.linalg.norm(con[0])),float(np.linalg.norm(main)),float(np.linalg.norm(rhs))))
                    conagg[kind]["anisotropy"].append((float(np.linalg.norm(con[1])),float(np.linalg.norm(main)),float(np.linalg.norm(rhs))))
                rows.append(one)

    summary={}
    for kind in ("solution","reference"):
        eq={}
        for name in EQ_NAMES:
            vals=aggregate[kind][name]
            anum=math.sqrt(sum(v[0]**2 for v in vals))
            alhs=math.sqrt(sum(v[1]**2 for v in vals))
            arhs=math.sqrt(sum(v[2]**2 for v in vals))
            eq[name]={
                "global_relative_L2":float(anum/max(alhs,arhs,TINY)),
                "global_absolute_L2":float(anum),
                "global_lhs_L2":float(alhs),
                "global_rhs_L2":float(arhs),
            }
        cons={}
        for name in ("shift","anisotropy"):
            vals=conagg[kind][name]
            num=math.sqrt(sum(v[0]**2 for v in vals))
            den=math.sqrt(sum(max(v[1],v[2])**2 for v in vals))
            cons[name]={
                "global_relative_to_operator_scale":float(num/max(den,TINY)),
                "global_absolute_L2":float(num),
            }
        dominant=max(EQ_NAMES,key=lambda q:eq[q]["global_relative_L2"])
        summary[kind]={"main_by_equation":eq,"constraints":cons,"dominant_main_equation":dominant}
    return {"summary":summary,"per_case_mode":rows}


def shift_near_null_audit(z,bgs,mod6,mod7):
    samples={128:[],64:[]}
    for nt,label in ((128,"primary"),(64,"control")):
        for tag in r7.C_TAGS:
            bg=bgs[(nt,tag)]
            x=np.asarray(bg["x"],float)
            st=np.asarray(z[f"{tag}_Z11_{label}"],complex)
            dd=np.asarray(z[f"{tag}_Z11dot_{label}"],complex)
            for ik,m in enumerate(r7.FOURIER_N):
                k=float(m*r7.g9.K_REQ[0]/r7.FOURIER_N[0])
                for it,xq in enumerate(x):
                    w=np.asarray([
                        st[ik,0,it],st[ik,5,it],
                        st[ik,1,it],st[ik,2,it],st[ik,3,it],st[ik,4,it],
                        dd[ik,0,it],dd[ik,1,it],dd[ik,2,it],dd[ik,3,it],
                    ],complex)
                    Cmat,bp,diag=r7._local_linear_matrix(mod6,mod7,bg,tag,k,float(xq))
                    ga=Cmat[10]@w; ma=Cmat[11]@w
                    met=r7._constraint_backward_error(Cmat[10]+Cmat[11],w,0.0,ga,ma)
                    samples[nt].append({
                        "C":tag,"m":int(m),"time_index":int(it),"ln_a":float(xq),
                        "metric":float(met["metric"]),
                        "absolute_residual":float(met["absolute_residual"]),
                        "scale":float(met["scale"]),
                    })

    sref=max(q["scale"] for q in samples[128])
    thr=SQRT_EPS*sref
    active128=[q for q in samples[128] if q["scale"]>thr]
    null128=[q for q in samples[128] if q["scale"]<=thr]

    # Match Nt64 metric to Nt128 by C,m and PCHIP, then sample only the Nt128 active mask.
    m64map={}
    for tag in r7.C_TAGS:
        for m in r7.FOURIER_N:
            q=[r for r in samples[64] if r["C"]==tag and r["m"]==int(m)]
            q.sort(key=lambda z:z["ln_a"])
            xx=np.asarray([z["ln_a"] for z in q],float)
            yy=np.asarray([z["metric"] for z in q],float)
            m64map[(tag,int(m))]=PchipInterpolator(xx,yy,extrapolate=False)

    v128=[]; v64=[]
    for q in active128:
        v128.append(q["metric"])
        v64.append(float(m64map[(q["C"],q["m"])](q["ln_a"])))
    v128=np.asarray(v128,float); v64=np.asarray(v64,float)
    near_ratio=max((q["absolute_residual"] for q in null128),default=0.0)/max(sref,TINY)
    worst=max(active128,key=lambda q:q["metric"]) if active128 else None

    return {
        "S_ref_Nt128":float(sref),
        "near_null_scale_threshold":float(thr),
        "rule":"Nt128 scale <= sqrt(machine_epsilon)*S_ref",
        "active_sample_count":len(active128),
        "near_null_sample_count":len(null128),
        "Nt128_active_Linf":float(np.max(v128)) if len(v128) else None,
        "Nt128_active_L2":float(np.linalg.norm(v128)/math.sqrt(len(v128))) if len(v128) else None,
        "Nt64_interpolated_active_Linf":float(np.max(v64)) if len(v64) else None,
        "Nt64_interpolated_active_L2":float(np.linalg.norm(v64)/math.sqrt(len(v64))) if len(v64) else None,
        "near_null_absolute_residual_over_Sref_Nt128":float(near_ratio),
        "worst_Nt128_active_sample":worst,
        "raw_all_row_Nt128_Linf":float(max(q["metric"] for q in samples[128])),
        "raw_all_row_Nt64_Linf":float(max(q["metric"] for q in samples[64])),
    }


def source_identity():
    sym=r30.symbolic_m1_audit()
    sums={}
    for n in (1024,2048):
        om,w=r7.c4.tan_gl_nodes(n)
        sums[str(n)]={
            "weight_sum":float(np.sum(w)),
            "abs_weight_sum_minus_one":float(abs(np.sum(w)-1.0)),
            "all_weights_positive":bool(np.all(w>0)),
        }
    return {
        "GE05_symbolic_M1":sym,
        "Drude_quadrature":sums,
        "no_fitted_normalization_adopted":True,
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--results-dir",default=str(ROOT/"results"))
    ap.add_argument("--repair30-json",default=str(ROOT/"results/ge19_repair30_reduced_h2_z11_reclosure.json"))
    ap.add_argument("--repair30-npz",default=str(ROOT/"results/ge19_repair30_reduced_h2_z11_reclosure.npz"))
    ap.add_argument("--json-out",required=True)
    args=ap.parse_args()

    j=Path(args.repair30_json); n=Path(args.repair30_npz); rd=Path(args.results_dir)
    if sha256(j)!=R30_JSON_SHA:
        raise RuntimeError("Repair30 JSON hash mismatch")
    if sha256(n)!=R30_NPZ_SHA:
        raise RuntimeError("Repair30 NPZ hash mismatch")
    parent=json.loads(j.read_text())
    if parent.get("classification")!="GE19_REPAIR30_REDUCED_H2_Z11_RECLOSURE_FAIL":
        raise RuntimeError("unexpected Repair30 classification")

    z=np.load(n)
    bgs,bases,mod6,mod7,bgdiag=build_operator_context(rd)

    A=shift_near_null_audit(z,bgs,mod6,mod7)
    B=state_precision(z)
    C=chi_audit(z)
    D=operator_audit(z,bgs,mod6,mod7)
    E=source_identity()

    dom=D["summary"]["reference"]["dominant_main_equation"]
    if dom in ("aether_rapidity","scalar_phi"):
        route="REFERENCE_DEFECT_DOMINATED_BY_AETHER_OR_SCALAR_SOURCE_DICTIONARY_AUDIT_REQUIRED"
    elif dom in ("lapse","isotropic_spatial","dust_potential","dust_density"):
        route="REFERENCE_DEFECT_DOMINATED_BY_METRIC_OR_MATTER_REDUCTION_CLOSURE_AUDIT_REQUIRED"
    else:
        route="REFERENCE_DEFECT_ROUTE_UNRESOLVED"

    report={
        "classification":"GE19_REPAIR31_REPAIR30_H2_DICTIONARY_AND_MONITOR_AUDIT_COMPLETE",
        "predata_classification":"GE19_REPAIR31_PREDATA_REPAIR30_H2_DICTIONARY_AND_MONITOR_AUDIT",
        "uses_observational_data":False,
        "Repair30_relabelled":False,
        "Repair30_H2_reintegrated":False,
        "H4_Z21_solve_performed":False,
        "provenance":{
            "Repair30_JSON_sha256":sha256(j),
            "Repair30_NPZ_sha256":sha256(n),
        },
        "shift_monitor_audit":A,
        "state_precision_audit":B,
        "chi_parent_audit":C,
        "operator_residual_localization":D,
        "source_identity_audit":E,
        "routing":{
            "next_route":route,
            "H4_Z21_licensed":False,
        },
        "claim_boundary":"Artifact/operator audit only. Repair30 remains historical FAIL. No H2 reintegration, threshold change, fitted normalization, reduced-Z11 certification, H4/Z21, finite eta or observational claim.",
    }
    out=Path(args.json_out); out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2,allow_nan=False)+"\n")
    print(json.dumps(report,indent=2,allow_nan=False))


if __name__=="__main__":
    try:
        main()
    except Exception as exc:
        print(json.dumps({
            "classification":"GE19_REPAIR31_IMPLEMENTATION_FAIL",
            "error":repr(exc),
            "Repair30_relabelled":False,
            "Repair30_H2_reintegrated":False,
            "H4_Z21_solve_performed":False,
        },indent=2))
        raise
