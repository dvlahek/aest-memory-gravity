#!/usr/bin/env python3
"""GE19 Repair29A — artifact-only localization of the frozen Repair28 even residual.

No CLASS execution is performed. The script verifies the frozen Repair28
artifact payload, reuses the exact Repair28 interpolation/formula definitions,
and localizes the sole failed Repair28 gate by field, lambda, k and ln(a).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

import ge19.repair28_cancellation_free_full_state_eta_tangent as r28

PARENT_JSON_SHA="1fd3a4310ea737f6da0d16fa37572c175c26005f6a3ee3f84e5e74f9c82b05a0"
PARENT_NPZ_SHA="101c38d91344d12071ecb343c35769326f80975e013b7d159f573aae73879705"
PARENT_FULL_SHA="694fda61ad3f460e79f32ea35ecf6fda0c2a5933f3230b766485518f82af8cc5"
FROZEN_LIMIT=5.0e-3
TINY=1.0e-300


def sha256(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1<<20),b""):
            h.update(block)
    return h.hexdigest()


def find_one(root:Path,name:str)->Path:
    hits=list(root.rglob(name))
    if len(hits)!=1:
        raise RuntimeError(f"expected one {name}, found {len(hits)}")
    return hits[0]


def tag(lam:float)->str:
    return str(float(lam)).replace(".","p")


def trace_name(level:str,kind:str,lam:float|None=None)->str:
    if kind=="base":
        return f"ge19_repair28_{level}_base_full_state_trace.dat"
    assert lam is not None
    return f"ge19_repair28_{level}_{kind}_{tag(lam)}_full_state_trace.dat"


def generated_key(level:str,kind:str,lam:float|None=None)->str:
    if kind=="base":
        return f"{level}_base_trace"
    assert lam is not None
    return f"{level}_{kind}_{tag(lam)}"


def verify_trace(path:Path,parent:dict,key:str):
    rec=parent["provenance"]["generated"][key]
    got_sha=sha256(path)
    got_bytes=path.stat().st_size
    if got_sha!=rec["trace_sha256"] or got_bytes!=rec["trace_bytes"]:
        raise RuntimeError(
            f"trace provenance mismatch {key}: "
            f"sha={got_sha}/{rec['trace_sha256']} bytes={got_bytes}/{rec['trace_bytes']}"
        )


def norm(x)->float:
    return float(np.linalg.norm(np.asarray(x,float)))


def even_metric(base,plus,minus,consensus,lam):
    ev=np.asarray(plus,float)+np.asarray(minus,float)-2.0*np.asarray(base,float)
    den=2.0*abs(float(lam))*max(norm(consensus),TINY)
    return ev,float(norm(ev)/den)


def localize_pair(ev,consensus,lam):
    ev=np.asarray(ev,float)
    cons=np.asarray(consensus,float)
    k=np.asarray(r28.g9.K_REQ,float)
    a=np.exp(np.asarray(r28.XGRID,float))

    per_mode=[]
    for ik in range(ev.shape[0]):
        den=2.0*abs(float(lam))*max(norm(cons[ik]),TINY)
        per_mode.append({
            "mode_index":int(ik),
            "k_Mpc":float(k[ik]),
            "global_over_time_normalized_even":float(norm(ev[ik])/den),
            "even_L2":norm(ev[ik]),
            "tangent_L2":norm(cons[ik]),
        })

    denom=np.maximum(2.0*abs(float(lam))*np.abs(cons),TINY)
    pt=np.abs(ev)/denom
    flat=int(np.nanargmax(pt))
    ik,it=np.unravel_index(flat,pt.shape)

    absflat=int(np.nanargmax(np.abs(ev)))
    ia,ita=np.unravel_index(absflat,ev.shape)

    return {
        "per_mode":per_mode,
        "worst_pointwise_normalized":{
            "mode_index":int(ik),
            "k_Mpc":float(k[ik]),
            "time_index":int(it),
            "a":float(a[it]),
            "z":float(1.0/a[it]-1.0),
            "metric":float(pt[ik,it]),
            "even_value":float(ev[ik,it]),
            "consensus_tangent_value":float(cons[ik,it]),
        },
        "largest_absolute_even_residual":{
            "mode_index":int(ia),
            "k_Mpc":float(k[ia]),
            "time_index":int(ita),
            "a":float(a[ita]),
            "z":float(1.0/a[ita]-1.0),
            "absolute_value":float(abs(ev[ia,ita])),
            "signed_value":float(ev[ia,ita]),
            "consensus_tangent_value":float(cons[ia,ita]),
        },
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--artifact-dir",required=True)
    ap.add_argument("--json-out",required=True)
    ap.add_argument("--npz-out",required=True)
    args=ap.parse_args()

    art=Path(args.artifact_dir).resolve()
    outj=Path(args.json_out)
    outn=Path(args.npz_out)
    outj.parent.mkdir(parents=True,exist_ok=True)

    pj=find_one(art,"ge19_repair28_cancellation_free_full_state_eta_tangent.json")
    pn=find_one(art,"ge19_repair28_cancellation_free_full_state_eta_tangent.npz")
    pl=find_one(art,"ge19_repair28_cancellation_free_full_state_eta_tangent_FULL.log")
    if sha256(pj)!=PARENT_JSON_SHA:
        raise RuntimeError("Repair28 JSON hash mismatch")
    if sha256(pn)!=PARENT_NPZ_SHA:
        raise RuntimeError("Repair28 NPZ hash mismatch")
    if sha256(pl)!=PARENT_FULL_SHA:
        raise RuntimeError("Repair28 FULL log hash mismatch")

    parent=json.loads(pj.read_text())
    if parent["classification"]!="GE19_REPAIR28_CANCELLATION_FREE_FULL_STATE_ETA_TANGENT_FAIL":
        raise RuntimeError("unexpected Repair28 classification")
    gates=parent["gates"]
    failed=[k for k,v in gates.items() if not bool(v)]
    if failed!=["R1_even_residual_global_normalized_le_5e3"]:
        raise RuntimeError(f"unexpected Repair28 failed-gate set: {failed}")

    levels={}
    raw_store={}
    for level in ("R1","R2"):
        bp=find_one(art,trace_name(level,"base"))
        verify_trace(bp,parent,generated_key(level,"base"))
        base,km=r28.interpolate_trace(bp)
        if km>r28.K_REL_MAX:
            raise RuntimeError(f"{level} base k mismatch")

        plus=[]; minus=[]
        for lam in r28.LAMBDAS:
            pp=find_one(art,trace_name(level,"plus",float(lam)))
            mp=find_one(art,trace_name(level,"minus",float(lam)))
            verify_trace(pp,parent,generated_key(level,"plus",float(lam)))
            verify_trace(mp,parent,generated_key(level,"minus",float(lam)))
            pd,kp=r28.interpolate_trace(pp)
            md,km2=r28.interpolate_trace(mp)
            if max(kp,km2)>r28.K_REL_MAX:
                raise RuntimeError(f"{level} lambda={lam}: k mismatch")
            plus.append(pd); minus.append(md)

        tangents=[
            r28.tangent_bundle(base,plus[i],minus[i],r28.LAMBDAS[i])
            for i in range(len(r28.LAMBDAS))
        ]
        consensus={
            name:np.mean(np.stack([q[name] for q in tangents],axis=0),axis=0)
            for name in r28.FIELDS
        }

        metrics={}
        ev_arrays={}
        for name in r28.PRIMARY_FIELDS:
            metrics[name]={}
            for i,lam in enumerate(r28.LAMBDAS):
                ev,m=even_metric(
                    base[name],plus[i][name],minus[i][name],
                    consensus[name],float(lam)
                )
                metrics[name][str(float(lam))]=float(m)
                ev_arrays[(name,float(lam))]=ev

        items=[
            (float(v),name,float(lam))
            for name,row in metrics.items()
            for lam,v in row.items()
        ]
        items.sort(reverse=True)
        worst_val,worst_field,worst_lam=items[0]
        worst_ev=ev_arrays[(worst_field,worst_lam)]

        levels[level]={
            "metrics":metrics,
            "worst":{
                "field":worst_field,
                "lambda":worst_lam,
                "global_normalized_even":worst_val,
                "exceeds_frozen_Repair28_limit":bool(worst_val>FROZEN_LIMIT),
                **localize_pair(worst_ev,consensus[worst_field],worst_lam),
            },
            "consensus":consensus,
            "ev_arrays":ev_arrays,
        }
        raw_store[level]={
            "consensus":consensus,
            "ev_arrays":ev_arrays,
        }

    ratios={}
    for name in r28.PRIMARY_FIELDS:
        ratios[name]={}
        for lam in r28.LAMBDAS:
            key=str(float(lam))
            v1=levels["R1"]["metrics"][name][key]
            v2=levels["R2"]["metrics"][name][key]
            ratios[name][key]={
                "R1":v1,
                "R2":v2,
                "R2_over_R1":float(v2/max(v1,TINY)),
                "R1_over_limit":float(v1/FROZEN_LIMIT),
                "R2_over_limit":float(v2/FROZEN_LIMIT),
            }

    target=set()
    target.add(float(levels["R1"]["worst"]["lambda"]))
    target.add(float(levels["R2"]["worst"]["lambda"]))
    for name,row in levels["R1"]["metrics"].items():
        for lam,v in row.items():
            if float(v)>FROZEN_LIMIT:
                target.add(float(lam))
    target_lambdas=sorted(target,reverse=True)

    r1_exceed=[
        {"field":name,"lambda":float(lam),"metric":float(v)}
        for name,row in levels["R1"]["metrics"].items()
        for lam,v in row.items()
        if float(v)>FROZEN_LIMIT
    ]
    r1_exceed.sort(key=lambda q:q["metric"],reverse=True)

    result={
        "classification":"GE19_REPAIR29A_REPAIR28_EVEN_RESIDUAL_LOCALIZATION_COMPLETE",
        "predata_classification":"GE19_REPAIR29A_PREDATA_REPAIR28_EVEN_RESIDUAL_LOCALIZATION",
        "uses_observational_data":False,
        "new_CLASS_runs_performed":False,
        "Repair28_relabelled":False,
        "Repair28_threshold_changed":False,
        "provenance":{
            "Repair28_workflow_run_id":35723905248,
            "Repair28_artifact_id":10692716361,
            "Repair28_artifact_digest":"sha256:0549f84dc1313c7a34c7d6002939bdc34692b195881145489aa89023e9b9c34d",
            "Repair28_JSON_sha256":PARENT_JSON_SHA,
            "Repair28_NPZ_sha256":PARENT_NPZ_SHA,
            "Repair28_FULL_sha256":PARENT_FULL_SHA,
            "all_raw_trace_hashes_verified_against_Repair28_JSON":True,
        },
        "frozen_formula":{
            "even":"plus + minus - 2 base",
            "normalization":"L2(even)/(2 |lambda| L2(consensus tangent for same field))",
            "frozen_Repair28_limit":FROZEN_LIMIT,
        },
        "R1":{
            "per_field_lambda_global_metrics":levels["R1"]["metrics"],
            "worst":levels["R1"]["worst"],
            "all_exceedances":r1_exceed,
        },
        "R2":{
            "per_field_lambda_global_metrics":levels["R2"]["metrics"],
            "worst":levels["R2"]["worst"],
        },
        "precision_scaling":ratios,
        "Repair29B_target_lambdas":target_lambdas,
        "Repair29B_selection_rule":"union of R1 global-worst lambda, R2 global-worst lambda, and every lambda with any R1 field above 0.005",
        "claim_boundary":"Repair29A is artifact-only localization of the frozen Repair28 FAIL. It performs no new physical tangent run, does not alter Repair28, and does not certify reduced Z11 or H4/Z21.",
    }
    outj.write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")

    save={
        "lambdas":np.asarray(r28.LAMBDAS,float),
        "k_Mpc":np.asarray(r28.g9.K_REQ,float),
        "a":np.exp(np.asarray(r28.XGRID,float)),
    }
    for level in ("R1","R2"):
        for name in r28.PRIMARY_FIELDS:
            save[f"{level}_{name}_consensus"]=raw_store[level]["consensus"][name]
            for lam in r28.LAMBDAS:
                save[f"{level}_{name}_lambda_{tag(float(lam))}_even"]=raw_store[level]["ev_arrays"][(name,float(lam))]
    np.savez_compressed(outn,**save)
    print(json.dumps(result,indent=2,allow_nan=False))


if __name__=="__main__":
    main()
