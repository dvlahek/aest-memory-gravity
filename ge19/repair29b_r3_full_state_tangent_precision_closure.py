#!/usr/bin/env python3
"""GE19 Repair29B — targeted R3 precision closure for the complete eta tangent.

Target lambda values and tracked field/lambda pairs are not chosen here.
They are read from the frozen Repair29A deterministic selector. R3 is the
preregistered exact factor-2 refinement of Repair28 R2. The historical
Repair28 classification and threshold remain unchanged.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

import ge19.repair28_cancellation_free_full_state_eta_tangent as r28

R3_PRE=ROOT/"ge19"/"pre"/"R3_repair29b.pre"
REPAIR26_TRACE_SHA=r28.REPAIR26_TRACE_SHA
REPAIR26_TRACE_BYTES=r28.REPAIR26_TRACE_BYTES
REPAIR28_NPZ_SHA="101c38d91344d12071ecb343c35769326f80975e013b7d159f573aae73879705"
FORCE_REL_MAX=1.0e-2
FORCE_COS_MIN=0.9999
K_REL_MAX=1.0e-12
BG_REL_MAX=1.0e-12
TANGENT_PRECISION_MAX=5.0e-3
EVEN_MAX=5.0e-3
TINY=1.0e-300


def sha256(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1<<20),b""):
            h.update(block)
    return h.hexdigest()


def norm(x)->float:
    return float(np.linalg.norm(np.asarray(x,float)))


def rel_l2(a,b)->float:
    aa=np.asarray(a,float); bb=np.asarray(b,float)
    return float(np.linalg.norm(aa-bb)/max(np.linalg.norm(aa),np.linalg.norm(bb),TINY))


def ltag(lam:float)->str:
    return str(float(lam)).replace(".","p")


def run_class(class_root:Path,results:Path,kind:str,lam:float|None,force:Path):
    if kind=="base":
        label="base"
    else:
        assert lam is not None
        label=f"{kind}_{ltag(abs(float(lam)))}"
    trace=results/f"ge19_repair29b_R3_{label}_full_state_trace.dat"
    log=results/f"ge19_repair29b_R3_{label}_class.log"
    for p in (trace,log):
        if p.exists(): p.unlink()

    ini=class_root/f"ge19_repair29b_R3_{label}.ini"
    txt=r28.v63.rewrite_ini(
        r28.v63.BASE.read_text(),
        str(results/f"ge19_repair29b_R3_{label}_")
    )
    txt=txt.replace("lensing = yes","lensing = no")
    txt += "k_output_values = "+", ".join(f"{k:.17g}" for k in r28.g9.K_REQ)+"\n"
    ini.write_text(txt)

    env=os.environ.copy()
    env["OMP_NUM_THREADS"]="1"
    env["AEST_FULL_STATE_TRACE_FILE"]=str(trace.resolve())
    env.pop("AEST_DENSE_JET_TRACE_FILE",None)
    env.pop("AEST_OFFLINE_TRACE_FILE",None)
    if kind=="base":
        env.pop("AEST_TANGENT_FORCE_FILE",None)
        env.pop("AEST_TANGENT_LAMBDA",None)
    else:
        env["AEST_TANGENT_FORCE_FILE"]=str(force.resolve())
        env["AEST_TANGENT_LAMBDA"]=str(float(lam))

    with log.open("w") as fh:
        subprocess.run(
            [str(class_root/"class"),ini.name,str(R3_PRE.resolve())],
            cwd=class_root,env=env,stdout=fh,stderr=subprocess.STDOUT,check=True,
        )
    if not trace.exists() or trace.stat().st_size==0:
        raise RuntimeError(f"R3 {label}: full-state trace not produced")
    return trace,log


def build_force(trace:Path,results:Path):
    prefix=results/"ge19_repair29b_repair26_forcing"
    summary=results/"ge19_repair29b_repair26_forcing_summary.json"
    force=Path(str(prefix)+"_force.dat")
    for p in (summary,force):
        if p.exists(): p.unlink()
    subprocess.run([
        sys.executable,str(ROOT/"v039"/"build_tau_forcing.py"),str(trace),
        "--KB",str(r28.v63.KB),"--tauH0",str(r28.v63.TAUH0),
        "--out-prefix",str(prefix),
        "--control-order","1024","--primary-order","2048",
        "--summary",str(summary),
    ],check=True)
    d=json.loads(summary.read_text())
    return force,summary,d


def parse_selector(d:dict):
    if d.get("classification")!="GE19_REPAIR29A_REPAIR28_EVEN_RESIDUAL_LOCALIZATION_COMPLETE":
        raise RuntimeError("Repair29A classification mismatch")
    if d.get("new_CLASS_runs_performed") is not False:
        raise RuntimeError("Repair29A was not artifact-only")
    if d.get("Repair28_relabelled") is not False or d.get("Repair28_threshold_changed") is not False:
        raise RuntimeError("Repair29A parent policy mismatch")

    tracked=set()
    w1=d["R1"]["worst"]; w2=d["R2"]["worst"]
    tracked.add((str(w1["field"]),float(w1["lambda"])))
    tracked.add((str(w2["field"]),float(w2["lambda"])))
    for q in d["R1"]["all_exceedances"]:
        tracked.add((str(q["field"]),float(q["lambda"])))

    target=sorted({lam for _,lam in tracked},reverse=True)
    declared=[float(x) for x in d["Repair29B_target_lambdas"]]
    if target!=declared:
        raise RuntimeError(f"Repair29A selector mismatch: recomputed={target} declared={declared}")
    return target,sorted(tracked,key=lambda q:(-q[1],q[0]))


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--class-root",required=True)
    ap.add_argument("--repair26-trace",required=True)
    ap.add_argument("--repair29a-json",required=True)
    ap.add_argument("--repair28-npz",required=True)
    ap.add_argument("--results-dir",default=str(ROOT/"results"))
    ap.add_argument("--json-out",required=True)
    ap.add_argument("--npz-out",required=True)
    args=ap.parse_args()

    class_root=Path(args.class_root).resolve()
    trace26=Path(args.repair26_trace).resolve()
    r29aj=Path(args.repair29a_json).resolve()
    r28npz=Path(args.repair28_npz).resolve()
    results=Path(args.results_dir).resolve(); results.mkdir(parents=True,exist_ok=True)
    outj=Path(args.json_out); outn=Path(args.npz_out); outj.parent.mkdir(parents=True,exist_ok=True)

    if sha256(trace26)!=REPAIR26_TRACE_SHA or trace26.stat().st_size!=REPAIR26_TRACE_BYTES:
        raise RuntimeError("Repair26 trace provenance mismatch")
    if sha256(r28npz)!=REPAIR28_NPZ_SHA:
        raise RuntimeError("Repair28 NPZ provenance mismatch")

    selector=json.loads(r29aj.read_text())
    target_lambdas,tracked_pairs=parse_selector(selector)

    ref=np.load(r28npz)
    if not np.allclose(np.asarray(ref["ln_a"],float),r28.XGRID,rtol=0,atol=0):
        raise RuntimeError("Repair28 NPZ ln(a) grid mismatch")
    if not np.allclose(np.asarray(ref["k_Mpc"],float),r28.g9.K_REQ,rtol=0,atol=0):
        raise RuntimeError("Repair28 NPZ k grid mismatch")

    force,force_summary,fd=build_force(trace26,results)
    force_rel=float(fd["relative_L2_control_vs_primary"])
    force_cos=float(fd["cosine"])

    generated={}
    tb,lb=run_class(class_root,results,"base",None,force)
    base,km=r28.interpolate_trace(tb)
    generated["base"]=(tb,lb)
    kmiss=float(km)

    plus={}; minus={}; bg_runs=[base]
    for lam in target_lambdas:
        tp,lp=run_class(class_root,results,"plus",+float(lam),force)
        tm,lm=run_class(class_root,results,"minus",-float(lam),force)
        pp,kp=r28.interpolate_trace(tp)
        mm,km2=r28.interpolate_trace(tm)
        kmiss=max(kmiss,float(kp),float(km2))
        plus[lam]=pp; minus[lam]=mm; bg_runs.extend([pp,mm])
        generated[f"plus_{ltag(lam)}"]=(tp,lp)
        generated[f"minus_{ltag(lam)}"]=(tm,lm)

    bg_mismatch=r28.bg_mismatch(bg_runs)

    per_lambda={}
    tangent_precision_max=0.0
    all_finite=True
    r3_tangents={}
    r3_even={}
    for lam in target_lambdas:
        per_field={}
        for name in r28.PRIMARY_FIELDS:
            t=(plus[lam][name]-minus[lam][name])/(2.0*float(lam))
            e=plus[lam][name]+minus[lam][name]-2.0*base[name]
            r2_cons=np.asarray(ref[f"R2_{name}_tangent_consensus"],float)
            r2_same=np.asarray(ref[f"R2_lambda_{ltag(lam)}_{name}_tangent"],float)
            em=float(norm(e)/(2.0*abs(float(lam))*max(norm(r2_cons),TINY)))
            tp=rel_l2(t,r2_same)
            tangent_precision_max=max(tangent_precision_max,tp)
            all_finite=bool(all_finite and np.all(np.isfinite(t)) and np.all(np.isfinite(e)))
            per_field[name]={
                "R3_even_normalized_to_frozen_R2_consensus":em,
                "R3_vs_R2_same_lambda_tangent_relative_L2":tp,
            }
            r3_tangents[(name,lam)]=t
            r3_even[(name,lam)]=e
        per_lambda[str(float(lam))]=per_field

    tracked=[]
    tracked_even_max=0.0
    monotone=True
    for name,lam in tracked_pairs:
        key=str(float(lam))
        r1=float(selector["R1"]["per_field_lambda_global_metrics"][name][key])
        r2=float(selector["R2"]["per_field_lambda_global_metrics"][name][key])
        r3=float(per_lambda[key][name]["R3_even_normalized_to_frozen_R2_consensus"])
        tracked_even_max=max(tracked_even_max,r3)
        mono=bool(r3<=r2)
        monotone=bool(monotone and mono)
        p12=(math.log(r1/r2)/math.log(2.0)) if r1>0 and r2>0 else None
        p23=(math.log(r2/r3)/math.log(2.0)) if r2>0 and r3>0 else None
        tracked.append({
            "field":name,"lambda":lam,
            "R1_even":r1,"R2_even":r2,"R3_even":r3,
            "R2_over_R1":float(r2/max(r1,TINY)),
            "R3_over_R2":float(r3/max(r2,TINY)),
            "R3_le_R2":mono,
            "empirical_order_R1_R2":p12,
            "empirical_order_R2_R3":p23,
            "R3_passes_frozen_Repair28_limit":bool(r3<=EVEN_MAX),
            "R3_vs_R2_same_lambda_tangent_relative_L2":float(
                per_lambda[key][name]["R3_vs_R2_same_lambda_tangent_relative_L2"]
            ),
        })

    gates={
        "Repair29A_provenance_and_selector_exact":True,
        "forcing_control_relative_L2_le_1e2":bool(force_rel<=FORCE_REL_MAX),
        "forcing_control_cosine_ge_0p9999":bool(force_cos>=FORCE_COS_MIN),
        "requested_k_relative_miss_le_1e12":bool(kmiss<=K_REL_MAX),
        "background_grid_relative_mismatch_le_1e12":bool(bg_mismatch<=BG_REL_MAX),
        "R3_vs_R2_same_lambda_tangent_relative_L2_le_5e3":bool(tangent_precision_max<=TANGENT_PRECISION_MAX),
        "tracked_R3_even_residual_le_5e3":bool(tracked_even_max<=EVEN_MAX),
        "tracked_R3_even_not_greater_than_R2":bool(monotone),
        "all_outputs_finite":bool(all_finite),
    }
    passed=bool(all(gates.values()))

    provenance={}
    for key,(tp,lp) in generated.items():
        provenance[key]={
            "trace_sha256":sha256(tp),"trace_bytes":tp.stat().st_size,
            "log_sha256":sha256(lp),"log_bytes":lp.stat().st_size,
        }

    result={
        "classification":(
            "GE19_REPAIR29B_R2_PRIMARY_R3_CONTROL_FULL_STATE_ETA_TANGENT_PASS"
            if passed else
            "GE19_REPAIR29B_R3_FULL_STATE_TANGENT_PRECISION_CLOSURE_FAIL"
        ),
        "predata_classification":"GE19_REPAIR29B_PREDATA_R3_FULL_STATE_TANGENT_PRECISION_CLOSURE",
        "uses_observational_data":False,
        "finite_physical_eta":False,
        "Repair28_relabelled":False,
        "Repair28_threshold_changed":False,
        "reduced_Z11_solve_performed":False,
        "H4_Z21_solve_performed":False,
        "selector":{
            "target_lambdas":target_lambdas,
            "tracked_pairs":[{"field":f,"lambda":l} for f,l in tracked_pairs],
            "source_classification":selector["classification"],
        },
        "R3_precision":{
            "tol_perturbations_integration":6.25e-9,
            "perturbations_sampling_stepsize":0.0003125,
            "factor_two_refinement_from_R2":True,
        },
        "forcing_control":{
            "relative_L2_control_vs_primary":force_rel,
            "cosine":force_cos,
            "primary_order":2048,
            "control_order":1024,
            "summary_sha256":sha256(force_summary),
            "force_sha256":sha256(force),
        },
        "grid_controls":{
            "requested_k_relative_miss_max":kmiss,
            "background_grid_relative_mismatch_max":bg_mismatch,
        },
        "per_target_lambda":per_lambda,
        "tracked_precision_ladder":tracked,
        "summary":{
            "R3_vs_R2_same_lambda_tangent_relative_L2_max":tangent_precision_max,
            "tracked_R3_even_residual_max":tracked_even_max,
            "all_tracked_R3_even_not_greater_than_R2":monotone,
        },
        "R3_generated_provenance":provenance,
        "gates":gates,
        "next_step":(
            "Separately preregister reduced H2/Z11 reclosure using Repair29B-certified R2 primary tangent representation."
            if passed else
            "Do not construct reduced Z11; localize the failed Repair29B precision gate."
        ),
        "claim_boundary":"Repair29B can certify R2 as the complete eta-tangent primary representation with targeted R3 numerical control. It does not relabel Repair28, solve reduced Z11, solve H4/Z21, introduce finite eta, or make observational claims.",
    }

    outj.write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
    save={
        "target_lambdas":np.asarray(target_lambdas,float),
        "k_Mpc":np.asarray(r28.g9.K_REQ,float),
        "ln_a":np.asarray(r28.XGRID,float),
        "a":np.exp(np.asarray(r28.XGRID,float)),
    }
    for lam in target_lambdas:
        for name in r28.PRIMARY_FIELDS:
            save[f"R3_lambda_{ltag(lam)}_{name}_tangent"]=r3_tangents[(name,lam)]
            save[f"R3_lambda_{ltag(lam)}_{name}_even"]=r3_even[(name,lam)]
    np.savez_compressed(outn,**save)
    print(json.dumps(result,indent=2,allow_nan=False))
    if not passed:
        raise SystemExit(2)


if __name__=="__main__":
    try:
        main()
    except Exception as exc:
        print(json.dumps({
            "classification":"GE19_REPAIR29B_IMPLEMENTATION_FAIL",
            "error":repr(exc),
            "Repair28_relabelled":False,
            "reduced_Z11_solve_performed":False,
            "H4_Z21_solve_performed":False,
        },indent=2))
        raise
