#!/usr/bin/env python3
"""GE09 dense accepted-step local-jet bridge.

Theory-only. Builds a common ln(a) representation of the complete local
first-order jet required by GE06 from successful NDF15 endpoints carrying
fresh physical RHS derivatives.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import os
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
from scipy.interpolate import CubicHermiteSpline, PchipInterpolator

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

import v063.theory_response_map as v63
import nl1c4.expanding_memory_source_trajectory as c4

KB=float(v63.KB)
H0_CLASS=float(v63.START["H0"])/299792.458
K_H=np.asarray([0.03,0.05,0.08,0.10,0.15,0.20],float)
K_REQ=K_H*(float(v63.START["H0"])/100.0)
AMIN=1.0/(1.0+1.5)
AMAX=1.0/(1.0+0.2)
NCOMMON=64
TINY=1e-300

TRACE_CLASS_MAX=1e-12
SOURCE_MAX=1e-4
CONTROL_GL2_MAX=5e-4
CONTROL_POINT_MAX=2e-3
PT_ID_MAX=1e-12
MIN_ACCEPTED=16

HERMITE={
    "phi":"phi_prime",
    "delta_dark":"delta_dark_prime",
    "theta_dark":"theta_dark_prime",
    "alpha_aest":"alpha_prime",
    "E_aest":"E_aest_prime",
}
ALGEBRAIC=("psi","Q","H_over_H0","rho_dark","p_dark","cad2_dark")
JET_NAMES=("N","L","R","b","u","Lt","Lx","Rt","Rx","bx","ut","ux","pt","px","Nx")


def read_table(path:Path):
    with path.open(newline="") as f:
        rd=csv.DictReader(f,delimiter=" ",skipinitialspace=True)
        if rd.fieldnames is None:
            raise RuntimeError(f"missing header: {path}")
        out=[]
        for rr in rd:
            try:
                q={k:float(rr[k]) for k in rd.fieldnames}
            except Exception:
                continue
            if all(math.isfinite(v) for v in q.values()):
                out.append(q)
    if not out:
        raise RuntimeError(f"empty trace {path}")
    return out


def aor(a,b):
    aa=np.asarray(a,float); bb=np.asarray(b,float)
    ae=np.abs(aa-bb)
    re=ae/np.maximum(np.maximum(np.abs(aa),np.abs(bb)),TINY)
    return float(np.max(np.minimum(ae,re)))


def rel_l2(a,b):
    aa=np.asarray(a,float); bb=np.asarray(b,float)
    return float(np.linalg.norm(aa-bb)/max(np.linalg.norm(aa),np.linalg.norm(bb),TINY))


def nearest_k(k,grid=K_REQ):
    i=int(np.argmin(np.abs(grid-float(k))))
    e=float(abs(grid[i]-float(k))/max(abs(float(k)),TINY))
    return i,e


def dedup_rows(rows):
    rows=sorted(rows,key=lambda r:r["a"])
    groups=[]
    cur=[]
    center=None
    for r in rows:
        x=math.log(r["a"])
        if center is None or abs(x-center)<=1e-13*max(1.0,abs(x),abs(center)):
            cur.append(r)
            center=float(np.median([math.log(z["a"]) for z in cur]))
        else:
            groups.append(cur); cur=[r]; center=x
    if cur: groups.append(cur)
    keys=rows[0].keys()
    return [{k:float(np.median([r[k] for r in g])) for k in keys} for g in groups]


def group_modes(rows):
    modes=[[] for _ in K_REQ]
    kmiss=0.0
    for r in rows:
        i,e=nearest_k(r["k"])
        if e<=1e-12:
            modes[i].append(r)
            kmiss=max(kmiss,e)
    modes=[dedup_rows(m) for m in modes]
    if any(len(m)==0 for m in modes):
        raise RuntimeError("one or more requested k modes absent from dense trace")
    return modes,kmiss


def decimate(rows):
    if len(rows)<=2:
        return list(rows)
    idx=list(range(0,len(rows),2))
    if idx[-1]!=len(rows)-1: idx.append(len(rows)-1)
    return [rows[i] for i in idx]


def build_interps(rows):
    x=np.log(np.asarray([r["a"] for r in rows],float))
    if np.any(np.diff(x)<=0):
        raise RuntimeError("accepted-step a grid not strictly increasing after dedup")
    H=np.asarray([r["H_over_H0"]*H0_CLASS for r in rows],float)
    calH=np.asarray([r["a"] for r in rows],float)*H
    if np.any(calH<=0):
        raise RuntimeError("non-positive conformal H in dense trace")

    out={}
    for field,prime in HERMITE.items():
        y=np.asarray([r[field] for r in rows],float)
        yp=np.asarray([r[prime] for r in rows],float)/calH
        out[field]=CubicHermiteSpline(x,y,yp,extrapolate=False)
    for field in ALGEBRAIC:
        y=np.asarray([r[field] for r in rows],float)
        out[field]=PchipInterpolator(x,y,extrapolate=False)
    return out


def eval_state(interps,x):
    d={k:np.asarray(fn(x),float) for k,fn in interps.items()}
    # Hermite derivative wrt ln(a), converted to conformal prime.
    H=d["H_over_H0"]*H0_CLASS
    a=np.exp(np.asarray(x,float))
    calH=a*H
    for field in HERMITE:
        d[field+"_prime_interp"]=np.asarray(interps[field].derivative()(x),float)*calH
    return d


def jet_from_state(state,a,k):
    H=state["H_over_H0"]*H0_CLASS
    Q=state["Q"]
    phi=state["phi"]
    psi=state["psi"]
    delta=state["delta_dark"]
    theta=state["theta_dark"]
    alpha=state["alpha_aest"]
    E=state["E_aest"]
    rho=state["rho_dark"]
    p=state["p_dark"]
    c2=state["cad2_dark"]
    phi_p=state["phi_prime_interp"]

    w=p/rho
    chi=Q*(a*theta/(k*k)+alpha)
    Pi=c2*delta+c2*k*k/(3.0*a*a*rho)*(KB*E+(2.0-KB)*chi)
    varphi=Q*a*theta/(k*k)
    pt=Q*(psi+Pi/(1.0+w))

    # Each entry is represented by coefficients multiplying cos(phase) and
    # sin(phase) for a single Fourier mode. Spatial derivatives are analytic.
    z=np.zeros_like(a)
    cos={
        "N":psi,
        "L":-a*phi,
        "R":-a*phi,
        "b":z,
        "u":z,
        "Lt":-a*H*phi-phi_p,
        "Lx":z,
        "Rt":-a*H*phi-phi_p,
        "Rx":z,
        "bx":z,
        "ut":z,
        "ux":-(k*k/a)*alpha,
        "pt":pt,
        "px":z,
        "Nx":z,
    }
    sin={
        "N":z,
        "L":z,
        "R":z,
        "b":z,
        "u":-(k/a)*alpha,
        "Lt":z,
        "Lx":a*k*phi,
        "Rt":z,
        "Rx":a*k*phi,
        "bx":z,
        "ut":(k/a)*(H*alpha-E+psi),
        "ux":z,
        "pt":z,
        "px":-k*varphi,
        "Nx":-k*psi,
    }
    return cos,sin,{"chi":chi,"Pi":Pi,"varphi":varphi,"w":w,"pt":pt}


def accepted_pt_identity(rows):
    aa=[]; bb=[]
    for r in rows:
        if not (AMIN-1e-14<=r["a"]<=AMAX+1e-14):
            continue
        a=r["a"]; H=r["H_over_H0"]*H0_CLASS; k=r["k"]
        Q=r["Q"]; rho=r["rho_dark"]; p=r["p_dark"]; c2=r["cad2_dark"]
        theta=r["theta_dark"]; psi=r["psi"]; E=r["E_aest"]; alpha=r["alpha_aest"]
        chi=Q*(a*theta/(k*k)+alpha)
        Pi=c2*r["delta_dark"]+c2*k*k/(3*a*a*rho)*(KB*E+(2-KB)*chi)
        closed=Q*(psi+Pi/(1+p/rho))
        Qdot=-3.0*H*Q*c2
        product=Qdot*(a*theta/(k*k))+Q*(a*H*theta+r["theta_dark_prime"])/(k*k)
        aa.append(closed); bb.append(product)
    if not aa:
        raise RuntimeError("no accepted endpoints in window for pt identity")
    return aor(aa,bb)


def read_class_perturbation(path):
    path=Path(path)
    lines=path.read_text().splitlines()
    kline=next((x for x in lines if x.startswith("#scalar perturbations for mode k")),None)
    if kline is None:
        raise RuntimeError(f"missing scalar-mode k header in {path}")
    mm=re.search(r"k\s*=\s*([0-9eE+\-.]+)",kline)
    if mm is None:
        raise RuntimeError(f"cannot parse scalar-mode k header in {path}")
    kval=float(mm.group(1))
    hline=next((x for x in lines if x.startswith("#") and "1:tau" in x and "2:a" in x),None)
    if hline is None:
        raise RuntimeError(f"missing numbered perturbation header in {path}")
    pairs=re.findall(r"(\d+):(.+?)(?=\s+\d+:|$)",hline.lstrip("#").strip())
    names={title.strip():int(num)-1 for num,title in pairs}
    data=np.loadtxt(path,comments="#",ndmin=2)
    required=("tau [Mpc]","a","phi","psi","delta_cdm","theta_cdm")
    missing=[x for x in required if x not in names]
    if missing:
        raise RuntimeError(f"missing CLASS perturbation columns {missing}; parsed={list(names)}")
    out={x:np.asarray(data[:,names[x]],float) for x in required}
    out["k"]=kval
    return out


def class_trace_control(modes,pt):
    errs=[]
    counts=[]
    fields=(("a","a"),("phi","phi"),("psi","psi"),
            ("delta_dark","delta_cdm"),("theta_dark","theta_cdm"))
    if len(pt)!=len(modes):
        raise RuntimeError(f"CLASS perturbation mode count {len(pt)} != {len(modes)}")
    for rows,mode in zip(modes,pt):
        taukey="tau [Mpc]"
        if taukey not in mode:
            raise RuntimeError(f"CLASS mode missing {taukey}; keys={sorted(mode)}")
        mt=np.asarray(mode[taukey],float)
        counts.append((len(rows),len(mt)))
        for r in rows:
            j=int(np.argmin(np.abs(mt-r["tau"])))
            if abs(mt[j]-r["tau"])>1e-11*max(1.0,abs(r["tau"])):
                raise RuntimeError("dense trace tau not found in CLASS get_perturbations")
            for rf,mf in fields:
                if mf not in mode:
                    raise RuntimeError(f"CLASS mode missing {mf}")
                errs.append(aor([r[rf]],[np.asarray(mode[mf],float)[j]]))
    return float(max(errs,default=math.inf)),counts


def source_validation(source_rows,primary):
    byfield={k:[] for k in (
        "phi","psi","delta_dark","theta_dark","alpha_aest","E_aest",
        "Q","H_over_H0","rho_dark","p_dark","cad2_dark"
    )}
    srcmap={
        "phi":"phi_newtonian","psi":"psi_newtonian",
        "delta_dark":"delta_dark","theta_dark":"theta_dark",
        "alpha_aest":"alpha_aest","E_aest":"E_aest",
        "Q":"Q","H_over_H0":"H_over_H0",
        "rho_dark":"rho_dark","p_dark":"p_dark","cad2_dark":"cad2_dark",
    }
    used=0
    for r in source_rows:
        if not (AMIN-1e-12<=r["a"]<=AMAX+1e-12):
            continue
        ik,e=nearest_k(r["k"])
        if e>1e-12: continue
        x=math.log(r["a"])
        st=eval_state(primary[ik],np.asarray([x]))
        for f,sf in srcmap.items():
            byfield[f].append((float(st[f][0]),float(r[sf])))
        used+=1
    if used<8*len(K_REQ):
        raise RuntimeError(f"only {used} source-validation rows; expected at least {8*len(K_REQ)}")
    errors={f:aor([x for x,_ in v],[y for _,y in v]) for f,v in byfield.items()}
    return errors,used


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--class-root",required=True)
    ap.add_argument("--json-out",required=True)
    ap.add_argument("--npz-out",required=True)
    args=ap.parse_args()
    outj=Path(args.json_out); outn=Path(args.npz_out)
    outj.parent.mkdir(parents=True,exist_ok=True)

    dense=ROOT/"results"/"ge09_dense_accepted_step_trace.dat"
    source=ROOT/"results"/"ge09_source_state_trace.dat"
    for p in (dense,source):
        if p.exists(): p.unlink()

    class_root=Path(args.class_root).resolve()
    prefix=ROOT/"results"/"ge09_cli_"
    for i in range(len(K_REQ)):
        p=Path(str(prefix)+f"perturbations_k{i}_s.dat")
        if p.exists(): p.unlink()
    ini=class_root/"ge09_repair01_cli.ini"
    text=v63.rewrite_ini(v63.BASE.read_text(),str(prefix))
    text=text.replace("lensing = yes","lensing = no")
    text += "k_output_values = " + ", ".join(f"{k:.17g}" for k in K_REQ) + "\n"
    ini.write_text(text)

    env=os.environ.copy()
    env["AEST_DENSE_JET_TRACE_FILE"]=str(dense.resolve())
    env["AEST_FULL_STATE_TRACE_FILE"]=str(source.resolve())
    env.pop("AEST_OFFLINE_TRACE_FILE",None)
    env.pop("AEST_TANGENT_FORCE_FILE",None)
    env.pop("AEST_TANGENT_LAMBDA",None)
    env["OMP_NUM_THREADS"]="1"

    class_log=ROOT/"results"/"ge09_repair01_cli_class.log"
    with class_log.open("w") as fh:
        subprocess.run(
            [str(class_root/"class"),ini.name,str(ROOT/"v019p/pre/p3.pre")],
            cwd=class_root,
            env=env,
            stdout=fh,
            stderr=subprocess.STDOUT,
            check=True,
        )

    pt=[read_class_perturbation(Path(str(prefix)+f"perturbations_k{i}_s.dat"))
        for i in range(len(K_REQ))]

    dense_rows=read_table(dense)
    source_rows=read_table(source)
    modes,kmiss=group_modes(dense_rows)

    class_err,class_counts=class_trace_control(modes,pt)

    nwin=[]
    max_gap=[]
    primary=[]; control=[]
    for m in modes:
        inwin=[r for r in m if AMIN-1e-14<=r["a"]<=AMAX+1e-14]
        nwin.append(len(inwin))
        xx=np.log(np.asarray([r["a"] for r in inwin],float))
        max_gap.append(float(np.max(np.diff(xx))) if len(xx)>1 else math.inf)
        if m[0]["a"]>AMIN or m[-1]["a"]<AMAX:
            raise RuntimeError("dense accepted trace does not bracket frozen common window")
        primary.append(build_interps(m))
        control.append(build_interps(decimate(m)))

    xcommon=np.linspace(math.log(AMIN),math.log(AMAX),NCOMMON)
    acommon=np.exp(xcommon)

    source_errs,source_used=source_validation(source_rows,primary)

    jet_primary={name:[] for name in JET_NAMES}
    jet_control={name:[] for name in JET_NAMES}
    jet_primary_sin={name:[] for name in JET_NAMES}
    jet_control_sin={name:[] for name in JET_NAMES}
    state_primary=[]
    state_control=[]
    all_finite=True

    for ik,k in enumerate(K_REQ):
        sp=eval_state(primary[ik],xcommon)
        sc=eval_state(control[ik],xcommon)
        cp,ss_p,diagp=jet_from_state(sp,acommon,k)
        cc,ss_c,diagc=jet_from_state(sc,acommon,k)
        state_primary.append(sp); state_control.append(sc)
        for name in JET_NAMES:
            jet_primary[name].append(cp[name])
            jet_control[name].append(cc[name])
            jet_primary_sin[name].append(ss_p[name])
            jet_control_sin[name].append(ss_c[name])
            all_finite=bool(
                all_finite
                and np.all(np.isfinite(cp[name])) and np.all(np.isfinite(cc[name]))
                and np.all(np.isfinite(ss_p[name])) and np.all(np.isfinite(ss_c[name]))
            )

    # Stack mode,time.
    for d in (jet_primary,jet_control,jet_primary_sin,jet_control_sin):
        for name in d:
            d[name]=np.asarray(d[name],float)

    control_errors={}
    gl2max=0.0; pmax=0.0
    for name in JET_NAMES:
        vp=np.concatenate([jet_primary[name].ravel(),jet_primary_sin[name].ravel()])
        vc=np.concatenate([jet_control[name].ravel(),jet_control_sin[name].ravel()])
        gl=rel_l2(vp,vc)
        pp=aor(vp,vc)
        control_errors[name]={"global_relative_L2":gl,"pointwise_abs_or_rel_max":pp}
        gl2max=max(gl2max,gl); pmax=max(pmax,pp)

    pt_err=accepted_pt_identity(dense_rows)

    gates={
        "successful_step_lifecycle_static_identity":True,
        "dense_trace_vs_CLASS_cli_perturbation_abs_or_rel_le_1e12":bool(class_err<=TRACE_CLASS_MAX),
        "minimum_accepted_points_per_k_in_window_ge_16":bool(min(nwin)>=MIN_ACCEPTED),
        "common_grid_nodes_exact_64":bool(len(xcommon)==NCOMMON),
        "source_grid_state_validation_abs_or_rel_le_1e4":bool(max(source_errs.values())<=SOURCE_MAX),
        "primary_vs_decimated_global_relative_L2_le_5e4":bool(gl2max<=CONTROL_GL2_MAX),
        "primary_vs_decimated_pointwise_abs_or_rel_le_2e3":bool(pmax<=CONTROL_POINT_MAX),
        "pt_closed_vs_product_rule_abs_or_rel_le_1e12":bool(pt_err<=PT_ID_MAX),
        "all_complete_jet_entries_finite":bool(all_finite),
    }
    passed=bool(all(gates.values()))
    classification="GE09_DENSE_ACCEPTED_STEP_LOCAL_JET_BRIDGE_PASS" if passed else "GE09_DENSE_ACCEPTED_STEP_LOCAL_JET_BRIDGE_FAIL"

    result={
        "classification":classification,
        "predata_classification":"GE09_REPAIR01_PREDATA_NATIVE_CLASS_CLI_PRECISION_EXECUTION",
        "scope":"GE09 Repair01 native-CLI p3 execution of the unchanged dense successful-step local-jet representation for GE06; matter closure and Z20 remain separate.",
        "trace":{
            "dense_rows":len(dense_rows),
            "source_rows":len(source_rows),
            "accepted_points_per_k_in_window":nwin,
            "max_ln_a_gap_per_k_in_window":max_gap,
            "requested_k_relative_miss_max":kmiss,
            "trace_vs_CLASS_cli_perturbation_abs_or_rel_max":class_err,
            "trace_vs_CLASS_counts":class_counts,
        },
        "common_time_representation":{
            "variable":"ln(a)",
            "nodes":NCOMMON,
            "a_min":AMIN,"a_max":AMAX,
            "primary":"all successful endpoints",
            "control":"every second endpoint, first/last retained",
            "derivative_aware":"CubicHermiteSpline using fresh physical RHS / (aH)",
            "algebraic":"PchipInterpolator",
        },
        "source_grid_validation":{
            "rows_used":source_used,
            "abs_or_rel_max_by_field":source_errs,
            "abs_or_rel_max":max(source_errs.values()),
            "limit":SOURCE_MAX,
        },
        "jet_control":{
            "by_entry":control_errors,
            "global_relative_L2_max":gl2max,
            "pointwise_abs_or_rel_max":pmax,
            "limits":{"global_relative_L2":CONTROL_GL2_MAX,"pointwise_abs_or_rel":CONTROL_POINT_MAX},
        },
        "exact_internal_controls":{
            "pt_closed_vs_product_rule_abs_or_rel_max":pt_err,
            "limit":PT_ID_MAX,
            "Qdot_identity":"Qdot=-3 H Q cad2",
        },
        "jet_dictionary":{
            "entries":list(JET_NAMES),
            "representation":"per Fourier mode cosine/sine coefficients at 64 common ln(a) nodes",
            "spatial_derivatives":"analytic Fourier multipliers",
            "future_spatial_primary_N":1024,
            "future_spatial_control_N":2048,
        },
        "gates":gates,
        "project_boundary":{
            "complete_GE06_local_jet_certified":passed,
            "standard_matter_closure_certified":False,
            "Z20_solve_licensed":False,
            "finite_eta_licensed":False,
        },
        "claim_boundary":"PASS certifies only the complete first-order local jet representation needed to evaluate the GE06 Q source. GE08 Repair01 matter incompleteness remains and Z20 is not licensed.",
    }
    outj.write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")

    save={
        "k_Mpc":K_REQ,
        "k_h_Mpc":K_H,
        "ln_a":xcommon,
        "a":acommon,
    }
    for name in JET_NAMES:
        save["cos_"+name]=jet_primary[name]
        save["sin_"+name]=jet_primary_sin[name]
        save["control_cos_"+name]=jet_control[name]
        save["control_sin_"+name]=jet_control_sin[name]
    np.savez_compressed(outn,**save)

    print(json.dumps(result,indent=2,allow_nan=False))
    if not passed:
        raise SystemExit(2)


if __name__=="__main__":
    main()
