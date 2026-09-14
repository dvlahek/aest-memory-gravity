#!/usr/bin/env python3
from __future__ import annotations

import argparse, json, os, subprocess, sys
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from fullj_weyl import stable_aest_growth_weyl_memory_r2 as r2

PREDATA_LOCK="246cc2a0059e88e9c89aa4de9d04aacc0f8302f8"
R2E_POSTDATA_LOCK="c0fe57f73a7785c21b1fecd7455f19148d5f812d"
R2E_JSON=ROOT/"results/stable_aest_growth_weyl_memory_r2e_single_hook.json"
R1C_JSON=ROOT/"results/stable_aest_finite_memory_r1c.json"
HOST_JSON=ROOT/"results/fullj_aest_stable_chi_precision_floor.json"

ANCHORS=(0.10000,0.10125,0.10250,0.10375,0.16500,0.19750,0.19875)
ETAS=(0.0,0.005,0.01)
Z=np.asarray([6.,5.,4.,3.,2.,1.5,1.,0.5,0.2],float)
EARLY=np.asarray([0,1,2],int)
LATE=np.asarray([6,7,8],int)

CLS_INCOMPLETE="STABLE_AEST_GROWTH_WEYL_MEMORY_R3_INCOMPLETE"
CLS_BASIS="STABLE_AEST_GROWTH_WEYL_MEMORY_R3_TRANSFER_BASIS_FAIL"
CLS_TAN="STABLE_AEST_GROWTH_WEYL_MEMORY_R3_TANGENT_GENERALITY_FAIL"
CLS_COMMON="STABLE_AEST_GROWTH_WEYL_MEMORY_R3_COMMON_MODE_GENERALITY_FAIL"
CLS_LATE="STABLE_AEST_GROWTH_WEYL_MEMORY_R3_LATE_RESPONSE_FAIL"
CLS_PASS="STABLE_AEST_GROWTH_WEYL_MEMORY_R3_SCALE_GENERALITY_CERTIFIED"

def ancestor(sha):
    return subprocess.run(["git","merge-base","--is-ancestor",sha,"HEAD"],cwd=ROOT,
                          stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode==0

def rel(a,b): return r2.rel(a,b)
def cosine(a,b): return r2.cosine(a,b)
def rms(a):
    a=np.asarray(a,float)
    return float(np.sqrt(np.mean(a*a)))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--json-out",default="results/stable_aest_growth_weyl_memory_r3_scale_generality.json")
    ap.add_argument("--npz-out",default="results/stable_aest_growth_weyl_memory_r3_scale_generality.npz")
    args=ap.parse_args()
    print("STABLE_AEST_GROWTH_WEYL_MEMORY_R3_START",flush=True)

    req=(R2E_JSON,R1C_JSON,HOST_JSON)
    if any(not p.exists() for p in req):
        Path(args.json_out).write_text(json.dumps({"classification":CLS_INCOMPLETE,"diagnostic_complete":False},indent=2)+"\n")
        return 3
    r2e=json.loads(R2E_JSON.read_text()); r1c=json.loads(R1C_JSON.read_text()); host=json.loads(HOST_JSON.read_text())
    g1=bool(ancestor(PREDATA_LOCK) and ancestor(R2E_POSTDATA_LOCK) and r2.source_ok()
            and r2e.get("classification")=="STABLE_AEST_GROWTH_WEYL_MEMORY_R2E_SINGLE_HOOK_ABSOLUTE_COMMON_MODE_CERTIFIED"
            and r1c.get("classification")=="STABLE_AEST_FINITE_MEMORY_R1C_LONG_RELAXATION_CERTIFIED"
            and host.get("classification")=="FULLJ_AEST_STABLE_CHI_PRECISION_FLOOR_CERTIFIED")

    vals={}; runs=[]; arrays={"redshifts":Z,"anchors":np.asarray(ANCHORS,float)}; basis_ok=True
    for kh in ANCHORS:
        for eta in ETAS:
            try:
                v=r2.run_case(float(kh),float(eta)); vals[(kh,eta)]=v
                tag=r2.pc.tag_of(kh); et=f"{eta:.3f}".replace(".","p")
                arrays[f"D_{tag}_e{et}"]=v["D"]; arrays[f"W_{tag}_e{et}"]=v["W"]
                domains_ok=all(d[0]<=kh<=d[1] and d[2]>=4 for d in v["domains"])
                keys_ok=len(set(v["k_keys"]))==1
                this=bool(v["finite"] and domains_ok and keys_ok)
                basis_ok &= this
                runs.append({"k_h":kh,"eta":eta,"finite":v["finite"],"basis_pass":this,"h":v["h"],
                             "bits":v["bits"],"target_pos":v["target_pos"],
                             "min_k_h":float(min(d[0] for d in v["domains"])),
                             "max_k_h":float(max(d[1] for d in v["domains"])),
                             "min_k_count":int(min(d[2] for d in v["domains"]))})
                print(f"STABLE_AEST_GROWTH_WEYL_MEMORY_R3_RUN k_h={kh:.5f} eta={eta:.3g} finite={v['finite']} basis={this}",flush=True)
            except Exception as e:
                basis_ok=False; runs.append({"k_h":kh,"eta":eta,"finite":False,"basis_pass":False,"error":repr(e)})
                print(f"STABLE_AEST_GROWTH_WEYL_MEMORY_R3_RUN_FAIL k_h={kh:.5f} eta={eta:.3g} error={e!r}",flush=True)

    if len(vals)!=len(ANCHORS)*len(ETAS): basis_ok=False
    if basis_ok:
        for kh in ANCHORS:
            d0=vals[(kh,0.0)]["D"]; w0=vals[(kh,0.0)]["W"]
            basis_ok &= bool(np.all(np.isfinite(d0)) and np.all(np.isfinite(w0)) and np.all(np.abs(d0)>1e-300) and np.all(np.abs(w0)>1e-300))
    g2=bool(basis_ok)

    cells=[]; tan_strict=0; tan_loose_all=True; cm_strict=0; cm_loose_all=True; late_count=0; response_all=True
    if g2:
        for kh in ANCHORS:
            d0=vals[(kh,0.0)]["D"]; w0=vals[(kh,0.0)]["W"]
            d5=vals[(kh,0.005)]["D"]; w5=vals[(kh,0.005)]["W"]
            d1=vals[(kh,0.01)]["D"]; w1=vals[(kh,0.01)]["W"]
            G5=(d5-d0)/(0.005*d0); L5=(w5-w0)/(0.005*w0)
            G1=(d1-d0)/(0.01*d0); L1=(w1-w0)/(0.01*w0)
            EG=rel(G5,G1); EL=rel(L5,L1); CG=cosine(G5,G1); CL=cosine(L5,L1)
            ts=bool(EG<=.02 and EL<=.02 and CG>=.999 and CL>=.999)
            tl=bool(EG<=.05 and EL<=.05 and CG>=.995 and CL>=.995)
            tan_strict+=int(ts); tan_loose_all &= tl
            B1=float(np.linalg.norm(L1-G1)/max(float(np.linalg.norm(G1)),float(np.linalg.norm(L1)),1e-300))
            B5=float(np.linalg.norm(L5-G5)/max(float(np.linalg.norm(G5)),float(np.linalg.norm(L5)),1e-300))
            cs=bool(B1<=.01 and B5<=.01); cl=bool(B1<=.02 and B5<=.02)
            cm_strict+=int(cs); cm_loose_all &= cl
            nG=float(np.linalg.norm(G1)); nL=float(np.linalg.norm(L1)); nz=bool(np.isfinite(nG) and np.isfinite(nL) and nG>0 and nL>0)
            response_all &= nz
            fG=rms(np.abs(G1[LATE]))/max(rms(np.abs(G1[EARLY])),1e-300)
            fL=rms(np.abs(L1[LATE]))/max(rms(np.abs(L1[EARLY])),1e-300)
            lp=bool(fG>1 and fL>1); late_count+=int(lp)
            tag=r2.pc.tag_of(kh)
            for n,x in (("G005",G5),("L005",L5),("G010",G1),("L010",L1)):
                arrays[f"{n}_{tag}"]=x
            row={"k_h":kh,"E_G":EG,"E_L":EL,"C_G":CG,"C_L":CL,"tangent_strict":ts,"tangent_loose":tl,
                 "B_005":B5,"B_01":B1,"common_strict":cs,"common_loose":cl,
                 "norm_G01":nG,"norm_L01":nL,"F_late_G":fG,"F_late_L":fL,"late_pass":lp}
            cells.append(row)
            print("STABLE_AEST_GROWTH_WEYL_MEMORY_R3_CELL "+json.dumps(row,sort_keys=True),flush=True)

    g3=bool(g2 and tan_strict>=6 and tan_loose_all)
    g4=bool(g3 and cm_strict>=6 and cm_loose_all)
    g5=bool(g4 and response_all and late_count>=6)
    gates={"R3_G1_provenance_and_parent_lock":g1,"R3_G2_transfer_basis_and_finite_run_validity":g2,
           "R3_G3_individual_finite_eta_tangent_consistency":g3,"R3_G4_heldout_common_mode_generality":g4,
           "R3_G5_nonzero_late_time_physical_response":g5}
    if not g1: cls=CLS_INCOMPLETE
    elif not g2: cls=CLS_BASIS
    elif not g3: cls=CLS_TAN
    elif not g4: cls=CLS_COMMON
    elif not g5: cls=CLS_LATE
    else: cls=CLS_PASS
    summary={"classification":cls,"run_count":len(runs),"tangent_strict_count":tan_strict,
             "common_mode_strict_count":cm_strict,"late_pass_count":late_count,
             "max_B01":float(max((r["B_01"] for r in cells),default=float('nan'))),
             "max_B005":float(max((r["B_005"] for r in cells),default=float('nan')))}
    out={"classification":cls,"diagnostic_complete":True,"predata_lock":PREDATA_LOCK,
         "r2e_parent_classification":r2e.get("classification"),
         "settings":{"anchors":ANCHORS,"etas":ETAS,"tau_H0":10.0,"memory_order":20,
                     "tol_perturbations_integration":3e-8,"redshifts":Z.tolist(),
                     "science_method":"direct physical finite-eta; no diagnostic variational forcing"},
         "runs":runs,"cells":cells,"gates":gates,"summary":summary,
         "interpretation":{"scale_generality_licensed":cls==CLS_PASS,"observable_projection_licensed":cls==CLS_PASS,
                           "positive_separation_licensed":False,"observational_claim_licensed":False}}
    Path(args.json_out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    np.savez_compressed(args.npz_out,**arrays)
    print("STABLE_AEST_GROWTH_WEYL_MEMORY_R3_GATES="+json.dumps(gates,sort_keys=True),flush=True)
    print("STABLE_AEST_GROWTH_WEYL_MEMORY_R3_SUMMARY="+json.dumps(summary,sort_keys=True),flush=True)
    print("STABLE_AEST_GROWTH_WEYL_MEMORY_R3_CLASSIFICATION="+cls,flush=True)
    return 0 if cls==CLS_PASS else 1

if __name__=="__main__":
    raise SystemExit(main())
