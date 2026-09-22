#!/usr/bin/env python3
"""GE19 Repair28 — cancellation-free complete first-order eta tangent audit.

Build the retarded eta=0 memory forcing from the frozen Repair26 R1
cancellation-free history. Run signed-lambda GE15 cancellation-free CLASS
trajectories at R1/R2 precision and certify the complete accepted-source-grid
state tangent needed as the future H2/Z11 parent.

No reduced Z11 solve and no H4/Z21 solve are performed here.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
from scipy.interpolate import PchipInterpolator

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

import v063.theory_response_map as v63
import ge09.repair01_dense_accepted_step_local_jet_bridge as g9

LAMBDAS=np.asarray([10.0,5.0,2.5,1.25],float)
LEVELS={
    "R1":ROOT/"ge11"/"pre"/"R1_repair01.pre",
    "R2":ROOT/"ge11"/"pre"/"R2_repair01.pre",
}
A0=0.4
A1=1.0/(1.0+0.2)
NT=128
XGRID=np.linspace(math.log(A0),math.log(A1),NT)
FIELDS=(
    "phi_newtonian","psi_newtonian","phi_prime_conformal",
    "delta_dark","theta_dark","alpha_aest","E_aest","alpha_prime_dy",
    "delta_b","theta_b","delta_m_native","theta_m_native",
    "total_delta_rho","total_rho_plus_p_theta",
    "total_delta_p","total_rho_plus_p_shear",
)
BGFIELDS=("H_over_H0","Q","rho_dark","p_dark","cad2_dark","rho_b")
PRIMARY_FIELDS=(
    "phi_newtonian","psi_newtonian",
    "delta_dark","theta_dark","alpha_aest","E_aest",
    "delta_m_native","theta_m_native",
    "total_delta_rho","total_rho_plus_p_theta",
)
TINY=1e-300

REPAIR26_TRACE_SHA="608ee0b4c868a701db6976f756b9a551cd9ddffe1e8e4ab37c5cd2361405a6f8"
REPAIR26_TRACE_BYTES=26643162

FORCE_REL_MAX=1e-2
FORCE_COS_MIN=0.9999
K_REL_MAX=1e-12
BG_REL_MAX=1e-12
AFFINITY_MAX=5e-3
COS_MIN=0.9999
EVEN_MAX=5e-3
PRECISION_MAX=5e-3
CHI_PRECISION_MAX=5e-3
A0_POINT_MAX=5e-3


def sha256(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1<<20),b""):
            h.update(block)
    return h.hexdigest()


def norm(x)->float:
    return float(np.linalg.norm(np.asarray(x)))


def rel_l2(a,b)->float:
    aa=np.asarray(a,float); bb=np.asarray(b,float)
    return float(np.linalg.norm(aa-bb)/max(np.linalg.norm(aa),np.linalg.norm(bb),TINY))


def cosine(a,b)->float:
    aa=np.asarray(a,float).ravel(); bb=np.asarray(b,float).ravel()
    return float(np.dot(aa,bb)/max(np.linalg.norm(aa)*np.linalg.norm(bb),TINY))


def aor(a,b)->float:
    aa=np.asarray(a,float); bb=np.asarray(b,float)
    ae=np.abs(aa-bb)
    re=ae/np.maximum(np.maximum(np.abs(aa),np.abs(bb)),TINY)
    return float(np.max(np.minimum(ae,re)))


def read_table(path:Path):
    with path.open(newline="") as f:
        rd=csv.DictReader(f,delimiter=" ",skipinitialspace=True)
        if rd.fieldnames is None:
            raise RuntimeError(f"missing trace header: {path}")
        rows=[]
        for rr in rd:
            try:
                q={k:float(rr[k]) for k in rd.fieldnames}
            except Exception:
                continue
            if all(math.isfinite(v) for v in q.values()):
                rows.append(q)
    if not rows:
        raise RuntimeError(f"empty trace: {path}")
    return rows


def dedup(rows):
    rr=sorted(rows,key=lambda q:q["a"])
    groups=[]; cur=[]; center=None
    for q in rr:
        x=math.log(q["a"])
        if center is None or abs(x-center)<=1e-13*max(1.0,abs(x),abs(center)):
            cur.append(q)
            center=float(np.median([math.log(z["a"]) for z in cur]))
        else:
            groups.append(cur); cur=[q]; center=x
    if cur: groups.append(cur)
    keys=rr[0].keys()
    return [{k:float(np.median([q[k] for q in g])) for k in keys} for g in groups]


def group_modes(rows):
    modes=[[] for _ in g9.K_REQ]
    kmiss=0.0
    for q in rows:
        k=float(q["k"])
        i=int(np.argmin(np.abs(g9.K_REQ-k)))
        e=abs(float(g9.K_REQ[i])-k)/max(abs(k),TINY)
        if e<=K_REL_MAX:
            modes[i].append(q); kmiss=max(kmiss,e)
    modes=[dedup(m) for m in modes]
    if any(len(m)<2 for m in modes):
        raise RuntimeError("one or more requested k histories are absent")
    return modes,float(kmiss)


def interpolate_trace(path:Path):
    rows=read_table(path)
    modes,kmiss=group_modes(rows)
    out={name:np.empty((len(g9.K_REQ),NT),float) for name in (*FIELDS,*BGFIELDS)}
    range_miss=0.0
    for im,m in enumerate(modes):
        x=np.log(np.asarray([q["a"] for q in m],float))
        if XGRID[0] < x[0]-1e-13 or XGRID[-1] > x[-1]+1e-13:
            raise RuntimeError(f"trace does not cover frozen window: {path} mode={im}")
        for name in out:
            y=np.asarray([q[name] for q in m],float)
            out[name][im]=PchipInterpolator(x,y,extrapolate=False)(XGRID)
            if not np.all(np.isfinite(out[name][im])):
                raise RuntimeError(f"nonfinite interpolation {name}: {path}")
    return out,kmiss


def run_class(class_root:Path,results:Path,level:str,lam,force:Path):
    tag="base" if lam is None else ("plus" if lam>0 else "minus")+"_"+str(abs(float(lam))).replace(".","p")
    trace=results/f"ge19_repair28_{level}_{tag}_full_state_trace.dat"
    log=results/f"ge19_repair28_{level}_{tag}_class.log"
    for p in (trace,log):
        if p.exists(): p.unlink()

    ini=class_root/f"ge19_repair28_{level}_{tag}.ini"
    txt=v63.rewrite_ini(v63.BASE.read_text(),str(results/f"ge19_repair28_{level}_{tag}_"))
    txt=txt.replace("lensing = yes","lensing = no")
    txt += "k_output_values = "+", ".join(f"{k:.17g}" for k in g9.K_REQ)+"\n"
    ini.write_text(txt)

    env=os.environ.copy()
    env["OMP_NUM_THREADS"]="1"
    env["AEST_FULL_STATE_TRACE_FILE"]=str(trace.resolve())
    env.pop("AEST_DENSE_JET_TRACE_FILE",None)
    env.pop("AEST_OFFLINE_TRACE_FILE",None)
    if lam is None:
        env.pop("AEST_TANGENT_FORCE_FILE",None)
        env.pop("AEST_TANGENT_LAMBDA",None)
    else:
        env["AEST_TANGENT_FORCE_FILE"]=str(force.resolve())
        env["AEST_TANGENT_LAMBDA"]=str(float(lam))

    with log.open("w") as fh:
        subprocess.run(
            [str(class_root/"class"),ini.name,str(LEVELS[level].resolve())],
            cwd=class_root,env=env,stdout=fh,stderr=subprocess.STDOUT,check=True,
        )
    if not trace.exists() or trace.stat().st_size==0:
        raise RuntimeError(f"{level} {tag}: full-state trace not produced")
    return trace,log


def build_force(trace:Path,results:Path):
    prefix=results/"ge19_repair28_repair26_forcing"
    summary=results/"ge19_repair28_repair26_forcing_summary.json"
    force=Path(str(prefix)+"_force.dat")
    for p in (summary,force):
        if p.exists(): p.unlink()
    subprocess.run([
        sys.executable,str(ROOT/"v039"/"build_tau_forcing.py"),str(trace),
        "--KB",str(v63.KB),"--tauH0",str(v63.TAUH0),
        "--out-prefix",str(prefix),
        "--control-order","1024","--primary-order","2048",
        "--summary",str(summary),
    ],check=True)
    if not force.exists() or not summary.exists():
        raise RuntimeError("Repair28 forcing builder did not produce outputs")
    d=json.loads(summary.read_text())
    return force,summary,d


def tangent_bundle(base,plus,minus,lam):
    return {name:(plus[name]-minus[name])/(2.0*float(lam)) for name in FIELDS}


def derived(tan,base):
    a=np.exp(XGRID)[None,:]
    k=np.asarray(g9.K_REQ,float)[:,None]
    Q=np.asarray(base["Q"],float)
    rho=np.asarray(base["rho_dark"],float)
    p=np.asarray(base["p_dark"],float)
    chi=Q*(a*tan["theta_dark"]/(k*k)+tan["alpha_aest"])
    std_dr=tan["total_delta_rho"]-rho*tan["delta_dark"]
    std_mom=tan["total_rho_plus_p_theta"]-(rho+p)*tan["theta_dark"]
    return {
        "chi11":chi,
        "standard_sector_delta_rho11":std_dr,
        "standard_sector_momentum11":std_mom,
    }


def field_affinity(tangents):
    rows={}
    mx=0.0; cmin=1.0
    for name in PRIMARY_FIELDS:
        arr=np.stack([q[name] for q in tangents],axis=0)
        mean=np.mean(arr,axis=0)
        den=max(norm(mean),TINY)
        rels=[norm(arr[i]-mean)/den for i in range(len(arr))]
        coss=[cosine(arr[i],mean) for i in range(len(arr))]
        rows[name]={
            "relative_L2_by_lambda":{str(float(LAMBDAS[i])):float(rels[i]) for i in range(len(LAMBDAS))},
            "relative_L2_max":float(max(rels)),
            "cosine_min":float(min(coss)),
        }
        mx=max(mx,max(rels)); cmin=min(cmin,min(coss))
    return rows,float(mx),float(cmin)


def even_control(base,plus,minus,tangent_mean,lam):
    vals=[]
    for name in PRIMARY_FIELDS:
        ev=plus[name]+minus[name]-2.0*base[name]
        den=max(2.0*abs(float(lam))*norm(tangent_mean[name]),TINY)
        vals.append(norm(ev)/den)
    return float(max(vals))


def bg_mismatch(runs):
    ref=runs[0]
    mx=0.0
    for cur in runs[1:]:
        for name in BGFIELDS:
            mx=max(mx,rel_l2(cur[name],ref[name]))
    return float(mx)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--class-root",required=True)
    ap.add_argument("--repair26-trace",required=True)
    ap.add_argument("--results-dir",default=str(ROOT/"results"))
    ap.add_argument("--json-out",required=True)
    ap.add_argument("--npz-out",required=True)
    args=ap.parse_args()

    class_root=Path(args.class_root).resolve()
    trace26=Path(args.repair26_trace).resolve()
    results=Path(args.results_dir).resolve(); results.mkdir(parents=True,exist_ok=True)
    outj=Path(args.json_out); outn=Path(args.npz_out); outj.parent.mkdir(parents=True,exist_ok=True)

    if sha256(trace26)!=REPAIR26_TRACE_SHA or trace26.stat().st_size!=REPAIR26_TRACE_BYTES:
        raise RuntimeError("Repair26 R1 trace provenance mismatch")

    patch=results/"ge15_s_state_patch.json"
    if not patch.exists():
        raise RuntimeError("missing GE15 patch report")
    pd=json.loads(patch.read_text())
    if not (
        pd.get("classification")=="GE15_CANCELLATION_FREE_S_STATE_PATCH_PASS"
        and pd.get("physics_modified") is False
        and pd.get("state_dimension_modified") is False
        and pd.get("initial_s")==0.0
        and all(pd.get("checks",{}).values())
    ):
        raise RuntimeError("GE15 patch audit not PASS")

    force,force_summary,fd=build_force(trace26,results)
    force_rel=float(fd["relative_L2_control_vs_primary"])
    force_cos=float(fd["cosine"])

    level_data={}
    generated={}
    kmiss=0.0
    background_mismatch=0.0

    for level in ("R1","R2"):
        tr0,lg0=run_class(class_root,results,level,None,force)
        base,km=interpolate_trace(tr0); kmiss=max(kmiss,km)
        plus=[]; minus=[]; traces=[base]
        generated[f"{level}_base_trace"]=(tr0,lg0)
        for lam in LAMBDAS:
            tp,lp=run_class(class_root,results,level,+float(lam),force)
            tm,lm=run_class(class_root,results,level,-float(lam),force)
            pp,kp=interpolate_trace(tp); mm,km2=interpolate_trace(tm)
            kmiss=max(kmiss,kp,km2)
            plus.append(pp); minus.append(mm); traces.extend([pp,mm])
            stag=str(float(lam)).replace(".","p")
            generated[f"{level}_plus_{stag}"]=(tp,lp)
            generated[f"{level}_minus_{stag}"]=(tm,lm)

        background_mismatch=max(background_mismatch,bg_mismatch(traces))
        tangents=[tangent_bundle(base,plus[i],minus[i],LAMBDAS[i]) for i in range(len(LAMBDAS))]
        consensus={name:np.mean(np.stack([q[name] for q in tangents],axis=0),axis=0) for name in FIELDS}
        affinity,affmax,cosmin=field_affinity(tangents)
        even=max(even_control(base,plus[i],minus[i],consensus,LAMBDAS[i]) for i in range(len(LAMBDAS)))
        der=derived(consensus,base)
        level_data[level]={
            "base":base,"plus":plus,"minus":minus,"tangents":tangents,
            "consensus":consensus,"derived":der,
            "affinity":affinity,"affinity_max":affmax,"cosine_min":cosmin,
            "even_max":float(even),
        }

    field_precision={}
    precision_max=0.0
    a0_max=0.0
    for name in PRIMARY_FIELDS:
        e=rel_l2(level_data["R1"]["consensus"][name],level_data["R2"]["consensus"][name])
        e0=aor(level_data["R1"]["consensus"][name][:,0],level_data["R2"]["consensus"][name][:,0])
        field_precision[name]={"R1_R2_relative_L2":e,"a0_abs_or_rel_max":e0}
        precision_max=max(precision_max,e)
        a0_max=max(a0_max,e0)

    chi_precision=rel_l2(level_data["R1"]["derived"]["chi11"],level_data["R2"]["derived"]["chi11"])

    all_finite=True
    for lev in level_data.values():
        for q in list(lev["consensus"].values())+list(lev["derived"].values()):
            all_finite=bool(all_finite and np.all(np.isfinite(q)))

    gates={
        "GE15_patch_report_pass":True,
        "forcing_control_relative_L2_le_1e2":bool(force_rel<=FORCE_REL_MAX),
        "forcing_control_cosine_ge_0p9999":bool(force_cos>=FORCE_COS_MIN),
        "requested_k_relative_miss_le_1e12":bool(kmiss<=K_REL_MAX),
        "common_background_grid_relative_mismatch_le_1e12":bool(background_mismatch<=BG_REL_MAX),
        "R1_lambda_affinity_global_relative_L2_le_5e3":bool(level_data["R1"]["affinity_max"]<=AFFINITY_MAX),
        "R2_lambda_affinity_global_relative_L2_le_5e3":bool(level_data["R2"]["affinity_max"]<=AFFINITY_MAX),
        "R1_lambda_cosine_ge_0p9999":bool(level_data["R1"]["cosine_min"]>=COS_MIN),
        "R2_lambda_cosine_ge_0p9999":bool(level_data["R2"]["cosine_min"]>=COS_MIN),
        "R1_even_residual_global_normalized_le_5e3":bool(level_data["R1"]["even_max"]<=EVEN_MAX),
        "R2_even_residual_global_normalized_le_5e3":bool(level_data["R2"]["even_max"]<=EVEN_MAX),
        "R1_R2_consensus_state_global_relative_L2_le_5e3":bool(precision_max<=PRECISION_MAX),
        "R1_R2_chi11_global_relative_L2_le_5e3":bool(chi_precision<=CHI_PRECISION_MAX),
        "a0_R1_R2_state_abs_or_rel_le_5e3":bool(a0_max<=A0_POINT_MAX),
        "all_outputs_finite":bool(all_finite),
    }
    passed=bool(all(gates.values()))

    files={}
    for key,(tp,lp) in generated.items():
        files[key]={
            "trace_sha256":sha256(tp),"trace_bytes":tp.stat().st_size,
            "log_sha256":sha256(lp),"log_bytes":lp.stat().st_size,
        }

    result={
        "classification":(
            "GE19_REPAIR28_CANCELLATION_FREE_FULL_STATE_ETA_TANGENT_PASS"
            if passed else
            "GE19_REPAIR28_CANCELLATION_FREE_FULL_STATE_ETA_TANGENT_FAIL"
        ),
        "predata_classification":"GE19_REPAIR28_PREDATA_CANCELLATION_FREE_FULL_STATE_ETA_TANGENT",
        "uses_observational_data":False,
        "finite_physical_eta":False,
        "reduced_Z11_solve_performed":False,
        "H4_Z21_solve_performed":False,
        "provenance":{
            "Repair26_R1_trace_sha256":REPAIR26_TRACE_SHA,
            "Repair26_R1_trace_bytes":REPAIR26_TRACE_BYTES,
            "GE15_patch_report":pd,
            "forcing_summary_sha256":sha256(force_summary),
            "forcing_file_sha256":sha256(force),
            "generated":files,
        },
        "forcing_control":{
            "relative_L2_control_vs_primary":force_rel,
            "cosine":force_cos,
            "primary_order":2048,
            "control_order":1024,
        },
        "grid":{
            "a_min":A0,"a_max":A1,"common_nodes":NT,
            "requested_k_relative_miss_max":kmiss,
            "common_background_grid_relative_mismatch_max":background_mismatch,
        },
        "R1":{
            "lambda_affinity":level_data["R1"]["affinity"],
            "lambda_affinity_global_max":level_data["R1"]["affinity_max"],
            "lambda_cosine_min":level_data["R1"]["cosine_min"],
            "even_residual_global_normalized_max":level_data["R1"]["even_max"],
        },
        "R2":{
            "lambda_affinity":level_data["R2"]["affinity"],
            "lambda_affinity_global_max":level_data["R2"]["affinity_max"],
            "lambda_cosine_min":level_data["R2"]["cosine_min"],
            "even_residual_global_normalized_max":level_data["R2"]["even_max"],
        },
        "precision_control":{
            "per_field":field_precision,
            "state_relative_L2_max":precision_max,
            "a0_state_abs_or_rel_max":a0_max,
            "chi11_relative_L2":chi_precision,
        },
        "gates":gates,
        "next_step":(
            "Separately preregister a reduced H2/Z11 reclosure using the Repair28 consensus tangent as its reference/boundary parent."
            if passed else
            "Do not construct reduced Z11; localize the failing full-state tangent gate."
        ),
        "claim_boundary":"Repair28 certifies only the complete cancellation-free first-order eta tangent trace/reference. It does not solve reduced Z11, H4/Z21, introduce finite eta, or make observational claims.",
    }

    outj.write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
    save={"ln_a":XGRID,"a":np.exp(XGRID),"k_Mpc":np.asarray(g9.K_REQ,float)}
    for level in ("R1","R2"):
        for name in FIELDS:
            save[f"{level}_{name}_tangent_consensus"]=level_data[level]["consensus"][name]
        for name,val in level_data[level]["derived"].items():
            save[f"{level}_{name}"]=val
        for i,lam in enumerate(LAMBDAS):
            tag=str(float(lam)).replace(".","p")
            for name in PRIMARY_FIELDS:
                save[f"{level}_lambda_{tag}_{name}_tangent"]=level_data[level]["tangents"][i][name]
    np.savez_compressed(outn,**save)

    print(json.dumps(result,indent=2,allow_nan=False))
    if not passed:
        raise SystemExit(2)


if __name__=="__main__":
    try:
        main()
    except Exception as exc:
        print(json.dumps({
            "classification":"GE19_REPAIR28_IMPLEMENTATION_FAIL",
            "error":repr(exc),
            "reduced_Z11_solve_performed":False,
            "H4_Z21_solve_performed":False,
        },indent=2))
        raise
