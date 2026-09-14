#!/usr/bin/env python3
from __future__ import annotations

import argparse, json, os, subprocess, sys
from collections import defaultdict
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from fullj_weyl import stable_aest_growth_weyl_memory_r2 as r2

PREDATA_LOCK="ee6ad94194802aed2622a314ac44df679fdee0f8"
R2C_POSTDATA_LOCK="23af2c6f1abbedfa63c7e41d4cb7fc0aaf36424c"
R2C_JSON=ROOT/"results/stable_aest_growth_weyl_memory_r2c_normalization.json"
R2B_JSON=ROOT/"results/stable_aest_growth_weyl_memory_r2b_variational.json"
R2_NPZ=ROOT/"results/stable_aest_growth_weyl_memory_r2.npz"
R1C_JSON=ROOT/"results/stable_aest_finite_memory_r1c.json"
HOST_JSON=ROOT/"results/fullj_aest_stable_chi_precision_floor.json"
R2C_WORK=ROOT/"results/stable_aest_growth_weyl_memory_r2c_work"

ANCHORS=(0.09875,0.16125,0.19500)
TAU=10.0; ORDER=20; TOL=3e-8
Z=np.asarray([6.,5.,4.,3.,2.,1.5,1.,0.5,0.2],float)
SOURCE_TAU_MIN=5174.717262978337
SOURCE_TAU_MAX=14151.626616283856

CLS_INCOMPLETE="STABLE_AEST_GROWTH_WEYL_MEMORY_R2D_INCOMPLETE"
CLS_COVER="STABLE_AEST_GROWTH_WEYL_MEMORY_R2D_HISTORY_COVERAGE_FAIL"
CLS_TRACE="STABLE_AEST_GROWTH_WEYL_MEMORY_R2D_TRACE_CONSISTENCY_FAIL"
CLS_TAN="STABLE_AEST_GROWTH_WEYL_MEMORY_R2D_VARIATIONAL_TANGENT_FAIL"
CLS_COMMON="STABLE_AEST_GROWTH_WEYL_MEMORY_R2D_FULL_HISTORY_COMMON_MODE_CERTIFIED"
CLS_SEP="STABLE_AEST_GROWTH_WEYL_MEMORY_R2D_FULL_HISTORY_SEPARATION_CERTIFIED"
CLS_MISMATCH="STABLE_AEST_GROWTH_WEYL_MEMORY_R2D_NON_HISTORY_NORMALIZATION_MISMATCH_CERTIFIED"
CLS_UNRES="STABLE_AEST_GROWTH_WEYL_MEMORY_R2D_FULL_HISTORY_UNRESOLVED"

def ancestor(sha):
    return subprocess.run(["git","merge-base","--is-ancestor",sha,"HEAD"],cwd=ROOT,
                          stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode==0

def rel(a,b):
    a=np.asarray(a,float); b=np.asarray(b,float)
    return float(np.linalg.norm(a-b)/max(float(np.linalg.norm(a)),float(np.linalg.norm(b)),1e-300))

def cosine(a,b):
    a=np.asarray(a,float); b=np.asarray(b,float)
    na=float(np.linalg.norm(a)); nb=float(np.linalg.norm(b))
    return float(np.dot(a,b)/(na*nb)) if na>0 and nb>0 else float("nan")

def tag(kh): return r2.pc.tag_of(kh)

def source_ok():
    root=os.environ.get("AEST_STABLE_R2D_CLASS_ROOT","")
    if not root: return False
    root=Path(root); pc=root/"source/perturbations.c"; am=root/"source/aest_memory.c"
    if not pc.is_file() or not am.is_file(): return False
    p=pc.read_text(); a=am.read_text()
    req=("FULLJ_AEST_STABLE_CHI_RESIDUAL_V1","FULLJ_STABLE_AEST_R2B_VARIATIONAL_V1",
         "FULLJ_STABLE_AEST_R2D_FULL_HISTORY_V1",
         "aest_r2d_trace_force(k,pba->h,tau,-0.5*a*Q_aest*Bchi_aest/pba->aest_KB);",
         "Bchi_aest *= pba->aest_eta;","E_rhs_aest -= 0.5*Q_aest*Bchi_aest;",
         "AEST_R2D_TRACE_FILE","AEST_R2D_TRACE_KH","AEST_TANGENT_FORCE_FILE","AEST_TANGENT_LAMBDA")
    return all(x in p+a for x in req)

def run_transfer(kh):
    from classy import Class
    bits=r2.pc.bits_for_anchor(kh)
    p,pos=r2.amp.make_params(kh,int(bits))
    p["tol_perturbations_integration"]=float(TOL)
    p["aest_memory_enabled"]="yes"; p["aest_memory_order"]=int(ORDER)
    p["aest_eta"]=0.0; p["aest_tau_H0"]=float(TAU)
    p["output"]="mTk,vTk"; p["z_max_pk"]=max(float(p.get("z_max_pk",0.0)),6.5)
    c=Class(); c.set(p); c.compute()
    try:
        h=r2.classy_h(c); D=[]; W=[]; domains=[]; keys=[]
        for z in Z:
            tr=c.get_transfer(z=float(z),output_format="class")
            miss=[x for x in ("d_m","phi","psi") if x not in tr]
            if miss: raise RuntimeError(f"missing transfer fields {miss}")
            kg,kkey=r2.k_h_from_transfer(tr,h)
            dm,klo,khi,nk=r2.interp_transfer_field(kg,tr["d_m"],kh)
            ph,_,_,_=r2.interp_transfer_field(kg,tr["phi"],kh)
            ps,_,_,_=r2.interp_transfer_field(kg,tr["psi"],kh)
            D.append(dm); W.append(ph+ps); domains.append((klo,khi,nk)); keys.append(kkey)
        D=np.asarray(D,float); W=np.asarray(W,float)
        finite=bool(np.all(np.isfinite(D)) and np.all(np.isfinite(W)))
        basis=bool(finite and all(q[0]<=kh<=q[1] and q[2]>=4 for q in domains) and len(set(keys))==1)
        return {"D":D,"W":W,"h":float(h),"finite":finite,"basis_pass":basis}
    finally:
        c.struct_cleanup(); c.empty()

def worker(args):
    v=run_transfer(float(args.kh))
    np.savez_compressed(args.out,D=v["D"],W=v["W"],redshifts=Z,h=np.asarray([v["h"]]),
                        finite=np.asarray([int(v["finite"])]),basis=np.asarray([int(v["basis_pass"])]))
    print(json.dumps({"k_h":float(args.kh),"h":v["h"],"finite":v["finite"],"basis_pass":v["basis_pass"]},sort_keys=True))
    return 0 if v["basis_pass"] else 2

def load_case(path):
    q=np.load(path)
    return {"D":np.asarray(q["D"],float),"W":np.asarray(q["W"],float),"h":float(q["h"][0]),
            "finite":bool(int(q["finite"][0])),"basis_pass":bool(int(q["basis"][0]))}

def read_force(path):
    rows=[]
    for line in Path(path).read_text(errors="replace").splitlines():
        p=line.split()
        if len(p)!=3: continue
        try: k,t,f=map(float,p)
        except ValueError: continue
        if np.isfinite(k) and np.isfinite(t) and np.isfinite(f): rows.append((k,t,f))
    return rows

def normalize_rhs(raw,out):
    rows=read_force(raw)
    if not rows: raise RuntimeError(f"no valid RHS trace rows in {raw}")
    acc=defaultdict(list)
    for k,t,f in rows: acc[(k,t)].append(f)
    clean=[]; max_dup_rel=0.0
    for (k,t),vals in acc.items():
        v=np.asarray(vals,float); mean=float(np.mean(v))
        spread=float(np.max(np.abs(v-mean))/max(abs(mean),float(np.max(np.abs(v))),1e-300))
        max_dup_rel=max(max_dup_rel,spread); clean.append((k,t,mean))
    clean.sort(key=lambda x:(x[0],x[1]))
    Path(out).parent.mkdir(parents=True,exist_ok=True)
    with open(out,"w") as fp:
        for k,t,f in clean: fp.write(f"{k:.17g} {t:.17g} {f:.17g}\n")
    taus=np.asarray([x[1] for x in clean],float); fs=np.asarray([x[2] for x in clean],float)
    return {"raw_rows":len(rows),"unique_rows":len(clean),"tau_min":float(np.min(taus)),
            "tau_max":float(np.max(taus)),"force_l2":float(np.linalg.norm(fs)),
            "force_max_abs":float(np.max(np.abs(fs))),"max_duplicate_relative_spread":max_dup_rel}

def overlap_metrics(rhs_path,src_path):
    rr=read_force(rhs_path); ss=read_force(src_path)
    if not rr or not ss: return {"pass":False,"E_force":float("inf"),"C_force":float("nan")}
    # R2d RHS trace is target-k only; R2c source-grid tables contain all k modes.
    # Select the R2c physical-k block nearest to the unique R2d target k before
    # comparing the forcing on their common tau interval.
    kr=float(np.median([x[0] for x in rr]))
    sk=np.asarray(sorted({x[0] for x in ss}),float)
    ks=float(sk[int(np.argmin(np.abs(sk-kr)))])
    krel=abs(ks-kr)/max(abs(kr),1e-300)
    if krel>2e-10:
        return {"pass":False,"E_force":float("inf"),"C_force":float("nan"),"relative_k_error":krel}
    rr=[x for x in rr if abs(x[0]-kr)<=2e-13*(1.+abs(kr))]
    ss=[x for x in ss if x[0]==ks]
    tr=np.asarray([x[1] for x in rr],float); fr=np.asarray([x[2] for x in rr],float)
    ts=np.asarray([x[1] for x in ss],float); fs=np.asarray([x[2] for x in ss],float)
    order=np.argsort(tr); tr=tr[order]; fr=fr[order]
    keep=np.ones(len(tr),bool)
    if len(tr)>1: keep[1:]=np.diff(tr)>0
    tr=tr[keep]; fr=fr[keep]
    good=(ts>=tr[0])&(ts<=tr[-1])
    if np.count_nonzero(good)<8:
        return {"pass":False,"E_force":float("inf"),"C_force":float("nan"),"relative_k_error":krel}
    fi=np.interp(ts[good],tr,fr); fsrc=fs[good]
    e=rel(fi,fsrc); c=cosine(fi,fsrc)
    return {"pass":bool(e<=.02 and c>=.999),"E_force":e,"C_force":c,
            "overlap_points":int(np.count_nonzero(good)),"relative_k_error":krel}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--worker",action="store_true"); ap.add_argument("--kh",type=float); ap.add_argument("--out")
    ap.add_argument("--json-out",default="results/stable_aest_growth_weyl_memory_r2d_full_history.json")
    ap.add_argument("--npz-out",default="results/stable_aest_growth_weyl_memory_r2d_full_history.npz")
    ap.add_argument("--workdir",default="results/stable_aest_growth_weyl_memory_r2d_work")
    args=ap.parse_args()
    if args.worker:
        if args.kh is None or not args.out: raise SystemExit("worker requires --kh --out")
        return worker(args)

    print("STABLE_AEST_GROWTH_WEYL_MEMORY_R2D_START",flush=True)
    req=(R2C_JSON,R2B_JSON,R2_NPZ,R1C_JSON,HOST_JSON)
    if any(not p.exists() for p in req):
        Path(args.json_out).write_text(json.dumps({"classification":CLS_INCOMPLETE,"diagnostic_complete":False},indent=2)+"\n")
        return 3

    r2c=json.loads(R2C_JSON.read_text()); r2b=json.loads(R2B_JSON.read_text())
    r1c=json.loads(R1C_JSON.read_text()); host=json.loads(HOST_JSON.read_text())
    g1=bool(ancestor(PREDATA_LOCK) and ancestor(R2C_POSTDATA_LOCK) and source_ok()
            and r2c.get("classification")=="STABLE_AEST_GROWTH_WEYL_MEMORY_R2C_GLOBAL_NORMALIZATION_MISMATCH_CERTIFIED"
            and r2b.get("classification")=="STABLE_AEST_GROWTH_WEYL_MEMORY_R2B_COMMON_MODE_BOUND_CERTIFIED"
            and r1c.get("classification")=="STABLE_AEST_FINITE_MEMORY_R1C_LONG_RELAXATION_CERTIFIED"
            and host.get("classification")=="FULLJ_AEST_STABLE_CHI_PRECISION_FLOOR_CERTIFIED")

    work=Path(args.workdir); work.mkdir(parents=True,exist_ok=True)
    py=sys.executable; mod="fullj_weyl.stable_aest_growth_weyl_memory_r2d_full_history"
    parent=np.load(R2_NPZ)
    baselines={}; cases={}; trace_rows=[]; overlap_rows=[]; neutral_rows=[]; arrays={"redshifts":Z}

    for kh in ANCHORS:
        t=tag(kh); raw=work/f"rhs_force_{t}_raw.dat"; clean=work/f"rhs_force_{t}.dat"; trace_out=work/f"trace_{t}.npz"
        env=os.environ.copy()
        for key in ("AEST_TANGENT_FORCE_FILE","AEST_TANGENT_LAMBDA","AEST_TANGENT_TRACE_FILE"): env.pop(key,None)
        env["AEST_R2D_TRACE_FILE"]=str(raw.resolve()); env["AEST_R2D_TRACE_KH"]=str(kh)
        subprocess.run([py,"-m",mod,"--worker","--kh",str(kh),"--out",str(trace_out)],cwd=ROOT,env=env,check=True)
        base=load_case(trace_out); baselines[kh]=base
        fs=normalize_rhs(raw,clean)
        coverage=bool(fs["tau_min"]<=.25*SOURCE_TAU_MIN and fs["tau_max"]>=.995*SOURCE_TAU_MAX
                      and fs["unique_rows"]>489 and np.isfinite(fs["force_l2"]))
        trace_rows.append({"k_h":kh,**fs,"coverage_pass":coverage})
        print(f"STABLE_AEST_GROWTH_WEYL_MEMORY_R2D_TRACE k_h={kh:.5f} pass={coverage} n={fs['unique_rows']} tau=[{fs['tau_min']:.6g},{fs['tau_max']:.6g}]",flush=True)

        src=R2C_WORK/f"force_{t}_s0p005.dat"
        ov=overlap_metrics(clean,src) if src.exists() else {"pass":False,"E_force":float("inf"),"C_force":float("nan")}
        overlap_rows.append({"k_h":kh,**ov})
        print("STABLE_AEST_GROWTH_WEYL_MEMORY_R2D_OVERLAP "+json.dumps(overlap_rows[-1],sort_keys=True),flush=True)

        d0=np.asarray(parent[f"D_{t}_e0p000"],float); w0=np.asarray(parent[f"W_{t}_e0p000"],float)
        ed=rel(base["D"],d0); ew=rel(base["W"],w0); neutral=bool(ed<=2e-5 and ew<=2e-5)
        neutral_rows.append({"k_h":kh,"D_relL2":ed,"W_relL2":ew,"pass":neutral})
        arrays[f"D0_{t}"]=base["D"]; arrays[f"W0_{t}"]=base["W"]

        for lam in (30.0,-30.0,10.0,-10.0):
            lt=("p" if lam>0 else "m")+str(int(abs(lam))); out=work/f"case_{t}_{lt}.npz"
            env=os.environ.copy()
            for key in ("AEST_R2D_TRACE_FILE","AEST_R2D_TRACE_KH","AEST_TANGENT_TRACE_FILE"): env.pop(key,None)
            env["AEST_TANGENT_FORCE_FILE"]=str(clean.resolve()); env["AEST_TANGENT_LAMBDA"]=str(lam)
            subprocess.run([py,"-m",mod,"--worker","--kh",str(kh),"--out",str(out)],cwd=ROOT,env=env,check=True)
            v=load_case(out); cases[(kh,lam)]=v
            arrays[f"D_{t}_{lt}"]=v["D"]; arrays[f"W_{t}_{lt}"]=v["W"]

    g2=all(r["coverage_pass"] for r in trace_rows)
    g3=all(r["pass"] for r in overlap_rows) and all(r["pass"] for r in neutral_rows)

    rows=[]; lambda_all=True; norm_strict=0; norm_loose_all=True; common_all=True; sep_count=0; mismatch_all=True; avec=[]
    for kh in ANCHORS:
        t=tag(kh); b=baselines[kh]
        p30,m30=cases[(kh,30.0)],cases[(kh,-30.0)]; p10,m10=cases[(kh,10.0)],cases[(kh,-10.0)]
        G30=(p30["D"]-m30["D"])/(60.0*b["D"]); L30=(p30["W"]-m30["W"])/(60.0*b["W"])
        G10=(p10["D"]-m10["D"])/(20.0*b["D"]); L10=(p10["W"]-m10["W"])/(20.0*b["W"])
        R30=L30-G30; R10=L10-G10
        refG=.5*(np.asarray(parent[f"G005_{t}"],float)+np.asarray(parent[f"G010_{t}"],float))
        refL=.5*(np.asarray(parent[f"L005_{t}"],float)+np.asarray(parent[f"L010_{t}"],float))

        elG=rel(G10,G30); elL=rel(L10,L30); clG=cosine(G10,G30); clL=cosine(L10,L30)
        lp=bool(elG<=.02 and elL<=.02 and clG>=.999 and clL>=.999); lambda_all &= lp
        eG=rel(G30,refG); eL=rel(L30,refL); cG=cosine(G30,refG); cL=cosine(L30,refL)
        aG=float(np.linalg.norm(refG)/max(float(np.linalg.norm(G30)),1e-300)); aL=float(np.linalg.norm(refL)/max(float(np.linalg.norm(L30)),1e-300)); avec += [aG,aL]
        ns=bool(eG<=.05 and eL<=.05 and cG>=.999 and cL>=.999 and .95<=aG<=1.05 and .95<=aL<=1.05)
        nl=bool(eG<=.10 and eL<=.10 and cG>=.995 and cL>=.995 and .90<=aG<=1.10 and .90<=aL<=1.10)
        norm_strict+=int(ns); norm_loose_all &= nl
        B=float(np.linalg.norm(R30)/max(float(np.linalg.norm(G30)),float(np.linalg.norm(L30)),1e-300))
        cm=bool(B<=.01); common_all &= cm
        eR=rel(R10,R30); cR=cosine(R10,R30); sep=bool(B>.01 and eR<=.20 and cR>=.95); sep_count+=int(sep)
        amatch=abs(aG-aL)/max(abs(aG),abs(aL),1e-300); mm=bool(cG>=.999 and cL>=.999 and eG>.10 and eL>.10 and amatch<=.02); mismatch_all &= mm

        row={"k_h":kh,"lambda_E_G":elG,"lambda_E_L":elL,"lambda_cos_G":clG,"lambda_cos_L":clL,
             "lambda_pass":lp,"abs_E_G":eG,"abs_E_L":eL,"abs_cos_G":cG,"abs_cos_L":cL,
             "A_G":aG,"A_L":aL,"norm_strict":ns,"norm_loose":nl,"B_30":B,
             "common_mode_pass":cm,"E_R":eR,"C_R":cR,"resolved_separation":sep,"coherent_mismatch":mm}
        rows.append(row)
        arrays[f"G30_{t}"]=G30; arrays[f"L30_{t}"]=L30; arrays[f"R30_{t}"]=R30
        arrays[f"G10_{t}"]=G10; arrays[f"L10_{t}"]=L10; arrays[f"R10_{t}"]=R10
        arrays[f"Gref_{t}"]=refG; arrays[f"Lref_{t}"]=refL
        print("STABLE_AEST_GROWTH_WEYL_MEMORY_R2D_CELL "+json.dumps(row,sort_keys=True),flush=True)

    g4=bool(lambda_all); g5=bool(norm_strict>=2 and norm_loose_all); g6=bool(common_all)
    g7=bool(g5 and (not g6) and sep_count>=2)
    g8=bool(g2 and g3 and g4 and (not g5) and mismatch_all and max(avec)/max(min(avec),1e-300)<=1.10)
    gates={"R2D_G1_provenance_and_parent_lock":g1,"R2D_G2_full_history_coverage":g2,
           "R2D_G3_overlap_trace_consistency_and_patch_neutrality":g3,
           "R2D_G4_full_history_amplifier_consistency":g4,"R2D_G5_absolute_normalization":g5,
           "R2D_G6_full_history_common_mode_bound":g6,"R2D_G7_resolved_full_history_separation":g7,
           "R2D_G8_persistent_coherent_normalization_mismatch":g8}
    if not g1: cls=CLS_INCOMPLETE
    elif not g2: cls=CLS_COVER
    elif not g3: cls=CLS_TRACE
    elif not g4: cls=CLS_TAN
    elif g5 and g6: cls=CLS_COMMON
    elif g5 and (not g6) and g7: cls=CLS_SEP
    elif (not g5) and g8: cls=CLS_MISMATCH
    else: cls=CLS_UNRES

    summary={"classification":cls,"trace_count":len(trace_rows),"normalization_strict_count":norm_strict,
             "resolved_separation_count":sep_count,"A_min":float(min(avec)),"A_max":float(max(avec)),
             "max_B30":float(max(r["B_30"] for r in rows))}
    out={"classification":cls,"diagnostic_complete":True,"predata_lock":PREDATA_LOCK,
         "r2c_parent_classification":r2c.get("classification"),"settings":{"anchors":ANCHORS,"tau_H0":TAU,
         "memory_order":ORDER,"physical_eta":0.0,"tol_perturbations_integration":TOL,
         "source_tau_min_reference":SOURCE_TAU_MIN,"source_tau_max_reference":SOURCE_TAU_MAX},
         "trace":trace_rows,"overlap":overlap_rows,"patch_neutrality":neutral_rows,"cells":rows,
         "gates":gates,"summary":summary,
         "interpretation":{"r2b_reclassified":False,"r2c_reclassified":False,
             "absolute_full_history_tangent_licensed":cls in (CLS_COMMON,CLS_SEP),
             "full_history_common_mode_licensed":cls==CLS_COMMON,
             "full_history_separation_licensed":cls==CLS_SEP,
             "missing_history_explanation_rejected":cls==CLS_MISMATCH,
             "observational_claim_licensed":False}}
    Path(args.json_out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    np.savez_compressed(args.npz_out,**arrays)
    print("STABLE_AEST_GROWTH_WEYL_MEMORY_R2D_GATES="+json.dumps(gates,sort_keys=True),flush=True)
    print("STABLE_AEST_GROWTH_WEYL_MEMORY_R2D_SUMMARY="+json.dumps(summary,sort_keys=True),flush=True)
    print("STABLE_AEST_GROWTH_WEYL_MEMORY_R2D_CLASSIFICATION="+cls,flush=True)
    return 0 if cls in (CLS_COMMON,CLS_SEP,CLS_MISMATCH) else 1

if __name__=="__main__":
    raise SystemExit(main())
