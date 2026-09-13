#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fullj_weyl import aest_ulp_initial_amplitude_localization as amp
from fullj_weyl import corrected_class_spectral_fringe_k_ulp_forensics as ulp

PREDATA_LOCK = "0c8dce2022626e194fa90aafe45242f2ed1fc8a7"
PARENT_JSON = ROOT / "results/fullj_aest_ulp_initial_amplitude_localization.json"
PARENT_NPZ = ROOT / "results/fullj_aest_ulp_initial_amplitude_localization.npz"
TRACE_DIR = ROOT / "results/fullj_aest_ulp_E_rhs_traces"

PAIRS = amp.PAIRS
TRACE_NAMES = (
    "k","tau","a","alpha","E","delta","theta","Q","KQ","H","cad2","w","rho",
    "chi","Pi","pi_delta","pi_E","pi_chi","T1","T2","T3","T4","E_rhs","D1","D2","dyE",
)
STATE_NAMES = ("alpha","delta","theta","Q","KQ","H","cad2","w")
TERM_NAMES = ("T1","T2","T3","T4")

INCOMPLETE = "FULLJ_AEST_ULP_E_RHS_AUDIT_INCOMPLETE"
NONNEUTRAL = "FULLJ_AEST_ULP_E_RHS_INSTRUMENTATION_NONNEUTRAL"
NOT_LOCAL = "FULLJ_AEST_ULP_E_RHS_SEED_NOT_LOCALIZED"
COMPONENT = "FULLJ_AEST_ULP_E_RHS_COMPONENT_DISCONTINUITY"
SMOOTH = "FULLJ_AEST_ULP_E_RHS_SMOOTH_NONCANCELLATION_SEED"
CANCEL = "FULLJ_AEST_ULP_E_RHS_CANCELLATION_SEED_CERTIFIED"


def is_ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"], cwd=ROOT,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    ).returncode == 0


def rel_l2(a, b) -> float:
    aa=np.asarray(a,float); bb=np.asarray(b,float)
    return float(np.linalg.norm(aa-bb)/max(float(np.linalg.norm(aa)),float(np.linalg.norm(bb)),1e-300))


def point_rel(a, b, floor=1e-300) -> float:
    return float(abs(float(a)-float(b))/max(abs(float(a)),abs(float(b)),floor))


def load_trace(path: Path):
    if not path.is_file():
        raise RuntimeError(f"missing trace {path}")
    arr=np.loadtxt(path, comments="#", dtype=float)
    if arr.ndim==1:
        arr=arr[None,:]
    if arr.shape[1] != len(TRACE_NAMES):
        raise RuntimeError(f"trace column mismatch {path}: {arr.shape}")
    if not np.all(np.isfinite(arr)):
        raise RuntimeError(f"nonfinite trace {path}")
    return {name:arr[:,i] for i,name in enumerate(TRACE_NAMES)}


def monotone_frontier(tr):
    a=np.asarray(tr["a"],float)
    keep=[]; mx=-np.inf
    for i,x in enumerate(a):
        if x > mx*(1.0+2e-14) if mx>0 else x>mx:
            keep.append(i); mx=x
    if len(keep)<8:
        # fallback: sort and unique by a
        order=np.argsort(a)
        av=a[order]
        mask=np.ones(len(order),dtype=bool)
        if len(order)>1: mask[1:]=np.diff(av)>0
        keep=list(order[mask])
    return {k:np.asarray(v)[keep] for k,v in tr.items()}


def common_interp(ta,tb,n=4096):
    A=monotone_frontier(ta); B=monotone_frontier(tb)
    lo=max(float(A["a"][0]),float(B["a"][0]))
    hi=min(float(A["a"][-1]),float(B["a"][-1]),3e-4)
    if not (0<lo<hi):
        raise RuntimeError("no common early trace interval")
    grid=np.exp(np.linspace(np.log(lo),np.log(hi),n))
    outA={}; outB={}
    xa=np.log(A["a"]); xb=np.log(B["a"]); xg=np.log(grid)
    for name in TRACE_NAMES:
        if name=="a":
            outA[name]=grid.copy(); outB[name]=grid.copy()
        else:
            outA[name]=np.interp(xg,xa,A[name])
            outB[name]=np.interp(xg,xb,B[name])
    return grid,outA,outB


def history_W_on_parent_grid(raw, grid):
    phi,_=amp.interp(raw,("phi",),grid)
    psi,_=amp.interp(raw,("psi",),grid)
    return phi+psi


def run_endpoint(tag, kh, bits, endpoint, parent_npz):
    p,pos=amp.make_params(kh,bits)
    trace=TRACE_DIR/f"{tag}_{endpoint}.txt"
    if trace.exists(): trace.unlink()
    kval=ulp.bits_float(int(bits))
    old_file=os.environ.get("AEST_ERHS_TRACE_FILE")
    old_k=os.environ.get("AEST_ERHS_TRACE_K")
    os.environ["AEST_ERHS_TRACE_FILE"]=str(trace)
    os.environ["AEST_ERHS_TRACE_K"]=format(kval,".17g")
    try:
        raw,nh=amp.raw_target(p,pos,True)
    finally:
        if old_file is None: os.environ.pop("AEST_ERHS_TRACE_FILE",None)
        else: os.environ["AEST_ERHS_TRACE_FILE"]=old_file
        if old_k is None: os.environ.pop("AEST_ERHS_TRACE_K",None)
        else: os.environ["AEST_ERHS_TRACE_K"]=old_k
    tr=load_trace(trace)
    grid=np.asarray(parent_npz[f"a_{tag}"],float)
    W=history_W_on_parent_grid(raw,grid)
    Wref=np.asarray(parent_npz[f"W_{endpoint}_{tag}"],float)
    neutral=rel_l2(W,Wref)
    return tr,W,neutral,int(nh),int(pos),str(trace)


def onset_analysis(grid,A,B):
    state_rel={name:np.asarray([point_rel(x,y) for x,y in zip(A[name],B[name])]) for name in STATE_NAMES}
    er=np.asarray([point_rel(x,y) for x,y in zip(A["E_rhs"],B["E_rhs"])])
    dr=np.asarray([point_rel(x,y) for x,y in zip(A["dyE"],B["dyE"])])
    material=(er>1e-3)|(dr>1e-3)
    onset=None
    for i in np.where(material)[0]:
        if max(float(state_rel[n][i]) for n in STATE_NAMES) <= 1e-8:
            onset=int(i); break
    first_state={n:float(state_rel[n][0]) for n in STATE_NAMES}
    first_cont=bool(max(first_state.values())<=1e-8)
    if onset is None:
        return {
            "first_state_rel":first_state,"first_state_continuous":first_cont,
            "seed_localized":False,"max_E_rhs_rel":float(np.max(er)),"max_dyE_rel":float(np.max(dr)),
        }
    i=onset
    sumA=sum(abs(float(A[n][i])) for n in TERM_NAMES)
    sumB=sum(abs(float(B[n][i])) for n in TERM_NAMES)
    kEA=sumA/max(abs(float(A["E_rhs"][i])),1e-300)
    kEB=sumB/max(abs(float(B["E_rhs"][i])),1e-300)
    kDA=(abs(float(A["D1"][i]))+abs(float(A["D2"][i])))/max(abs(float(A["dyE"][i])),1e-300)
    kDB=(abs(float(B["D1"][i]))+abs(float(B["D2"][i])))/max(abs(float(B["dyE"][i])),1e-300)
    term_rel={}
    scale=max(sumA,sumB,1e-300)
    for n in TERM_NAMES:
        den=max(abs(float(A[n][i])),abs(float(B[n][i])),scale*1e-15)
        term_rel[n]=float(abs(float(A[n][i])-float(B[n][i]))/den)
    component_cont=bool(max(term_rel.values())<=1e-5)
    cancellation=bool(max(kEA,kEB,kDA,kDB)>=1e6)
    return {
        "first_state_rel":first_state,"first_state_continuous":first_cont,
        "seed_localized":True,"onset_index":i,"onset_a":float(grid[i]),
        "onset_E_rhs_rel":float(er[i]),"onset_dyE_rel":float(dr[i]),
        "onset_state_rel":{n:float(state_rel[n][i]) for n in STATE_NAMES},
        "kappa_E_A":float(kEA),"kappa_E_B":float(kEB),
        "kappa_dy_A":float(kDA),"kappa_dy_B":float(kDB),
        "cancellation_at_onset":cancellation,
        "term_rel_at_onset":term_rel,"component_continuous":component_cont,
        "max_E_rhs_rel":float(np.max(er)),"max_dyE_rel":float(np.max(dr)),
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--json-out",default="results/fullj_aest_ulp_E_rhs_decomposition.json")
    ap.add_argument("--npz-out",default="results/fullj_aest_ulp_E_rhs_decomposition.npz")
    args=ap.parse_args()
    TRACE_DIR.mkdir(parents=True,exist_ok=True)
    print("FULLJ_AEST_ULP_E_RHS_START",flush=True)

    if not PARENT_JSON.exists() or not PARENT_NPZ.exists():
        out={"classification":INCOMPLETE,"diagnostic_complete":False,"reason":"missing parent amplitude-localization result"}
        Path(args.json_out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
        print("FULLJ_AEST_ULP_E_RHS_CLASSIFICATION="+INCOMPLETE,flush=True)
        return 3

    pj=json.loads(PARENT_JSON.read_text())
    pq=np.load(PARENT_NPZ)
    g1=bool(is_ancestor(PREDATA_LOCK) and pj.get("classification")=="FULLJ_AEST_ULP_LATE_EVOLUTION_DIVERGENCE" and pj.get("diagnostic_complete") is True)

    rows=[]; arrays={}; all_neutral=True
    first_cont_count=0; seed_count=0; cancel_count=0; component_all=True
    for tag,(kh,ba,bb) in PAIRS.items():
        trA,WA,nA,nhA,posA,pathA=run_endpoint(tag,kh,ba,"A",pq)
        trB,WB,nB,nhB,posB,pathB=run_endpoint(tag,kh,bb,"B",pq)
        if posA!=posB: raise RuntimeError("target positions differ")
        neutral=bool(nA<=2e-5 and nB<=2e-5)
        all_neutral &= neutral
        grid,A,B=common_interp(trA,trB,4096)
        an=onset_analysis(grid,A,B)
        first_cont_count += int(an["first_state_continuous"])
        seed_count += int(an["seed_localized"])
        if an["seed_localized"]:
            cancel_count += int(an["cancellation_at_onset"])
            component_all &= bool(an["component_continuous"])
        row={
            "tag":tag,"k_h":float(kh),"bits_A":int(ba),"bits_B":int(bb),"target_pos":int(posA),
            "trace_A":pathA,"trace_B":pathB,"n_histories_A":nhA,"n_histories_B":nhB,
            "instrumentation_neutral_A_relL2":float(nA),"instrumentation_neutral_B_relL2":float(nB),
            "instrumentation_neutral":neutral,**an,
        }
        rows.append(row)
        arrays[f"a_{tag}"]=grid
        for n in ("E_rhs","dyE","T1","T2","T3","T4","alpha","E","delta","theta","Q","KQ","H","cad2","w"):
            arrays[f"{n}_A_{tag}"]=A[n]; arrays[f"{n}_B_{tag}"]=B[n]
        print(
            f"FULLJ_AEST_ULP_E_RHS_PAIR k_h={kh:.5f} neutral={neutral} first_cont={an['first_state_continuous']} "
            f"seed={an['seed_localized']} onset_a={an.get('onset_a',float('nan')):.6e} "
            f"kappaE={max(an.get('kappa_E_A',0.),an.get('kappa_E_B',0.)):.3e} "
            f"kappaDy={max(an.get('kappa_dy_A',0.),an.get('kappa_dy_B',0.)):.3e} "
            f"component={an.get('component_continuous',False)}",flush=True
        )

    g2=bool(all_neutral)
    g3=bool(first_cont_count>=3)
    g4=bool(seed_count>=2)
    g5=bool(cancel_count>=2)
    g6=bool(g4 and component_all)
    gates={
        "ER_G1_provenance_and_parent_lock":g1,
        "ER_G2_instrumentation_neutrality":g2,
        "ER_G3_exact_initial_state_continuity":g3,
        "ER_G4_material_E_RHS_seeding":g4,
        "ER_G5_cancellation_localization":g5,
        "ER_G6_component_continuity":g6,
    }

    if not g1:
        classification=INCOMPLETE
    elif not g2:
        classification=NONNEUTRAL
    elif not g3 or not g4:
        classification=NOT_LOCAL
    elif not g6:
        classification=COMPONENT
    elif not g5:
        classification=SMOOTH
    else:
        classification=CANCEL

    summary={
        "classification":classification,"pair_count":len(rows),"first_continuous_pair_count":int(first_cont_count),
        "seed_localized_pair_count":int(seed_count),"cancellation_pair_count":int(cancel_count),
        "max_instrumentation_neutral_relL2":float(max(max(r["instrumentation_neutral_A_relL2"],r["instrumentation_neutral_B_relL2"]) for r in rows)),
        "max_onset_kappa_E":float(max(max(r.get("kappa_E_A",0.),r.get("kappa_E_B",0.)) for r in rows)),
        "max_onset_kappa_dy":float(max(max(r.get("kappa_dy_A",0.),r.get("kappa_dy_B",0.)) for r in rows)),
    }
    out={
        "classification":classification,"diagnostic_complete":True,"predata_lock":PREDATA_LOCK,
        "parent_classification":pj.get("classification"),"gates":gates,"summary":summary,"pairs":rows,
        "interpretation":{
            "historical_R3_reclassified":False,"new_physics_claim_licensed":False,"physical_instability_claim_licensed":False,
            "branch_index_audit_licensed":bool(classification==COMPONENT),
            "linear_mode_stability_audit_licensed":bool(classification==SMOOTH),
            "conditioning_mechanism_certified":bool(classification==CANCEL),
        },
    }
    Path(args.json_out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    np.savez_compressed(args.npz_out,**arrays)
    print("FULLJ_AEST_ULP_E_RHS_GATES="+json.dumps(gates,sort_keys=True),flush=True)
    print("FULLJ_AEST_ULP_E_RHS_SUMMARY="+json.dumps(summary,sort_keys=True),flush=True)
    print("FULLJ_AEST_ULP_E_RHS_CLASSIFICATION="+classification,flush=True)
    return 0 if classification in (CANCEL,COMPONENT,SMOOTH) else 1


if __name__=="__main__":
    raise SystemExit(main())
