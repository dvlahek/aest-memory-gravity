#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, os, subprocess, sys
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from fullj_weyl import stable_aest_growth_weyl_memory_r2 as r2

PREDATA_LOCK="6459fa6ceab26dfd56c4ba558613f3d1a4bd43c9"
R2B_POSTDATA_LOCK="35913eb794d7427431e5f5050f05a71ecfbccbbe"
R2B_JSON=ROOT/"results/stable_aest_growth_weyl_memory_r2b_variational.json"
R2_NPZ=ROOT/"results/stable_aest_growth_weyl_memory_r2.npz"
R1C_JSON=ROOT/"results/stable_aest_finite_memory_r1c.json"
HOST_JSON=ROOT/"results/fullj_aest_stable_chi_precision_floor.json"
ANCHORS=(0.09875,0.16125,0.19500)
SAMPLINGS=(0.02,0.005)
TAU=10.0; ORDER=20; TOL=3e-8
Z=np.asarray([6.,5.,4.,3.,2.,1.5,1.,0.5,0.2],float)

CLS_INCOMPLETE="STABLE_AEST_GROWTH_WEYL_MEMORY_R2C_INCOMPLETE"
CLS_DENSE_FAIL="STABLE_AEST_GROWTH_WEYL_MEMORY_R2C_DENSIFICATION_FAIL"
CLS_NEUTRAL_FAIL="STABLE_AEST_GROWTH_WEYL_MEMORY_R2C_PATCH_NEUTRALITY_FAIL"
CLS_TAN_FAIL="STABLE_AEST_GROWTH_WEYL_MEMORY_R2C_VARIATIONAL_TANGENT_FAIL"
CLS_GRID_FAIL="STABLE_AEST_GROWTH_WEYL_MEMORY_R2C_GRID_CONVERGENCE_FAIL"
CLS_NORM_PASS="STABLE_AEST_GROWTH_WEYL_MEMORY_R2C_ABSOLUTE_NORMALIZATION_CERTIFIED"
CLS_MISMATCH="STABLE_AEST_GROWTH_WEYL_MEMORY_R2C_GLOBAL_NORMALIZATION_MISMATCH_CERTIFIED"
CLS_UNRES="STABLE_AEST_GROWTH_WEYL_MEMORY_R2C_NORMALIZATION_UNRESOLVED"

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
def stag(s): return "s"+str(s).replace(".","p")

def source_ok():
    root=os.environ.get("AEST_STABLE_VAR_CLASS_ROOT","")
    if not root: return False
    root=Path(root); pc=root/"source/perturbations.c"; am=root/"source/aest_memory.c"
    if not pc.is_file() or not am.is_file(): return False
    p=pc.read_text(); a=am.read_text()
    req=("FULLJ_AEST_STABLE_CHI_RESIDUAL_V1","FULLJ_STABLE_AEST_R2B_VARIATIONAL_V1",
         "double s_aest=y[ppw->pv->index_pt_s_aest];","double chi_aest=Q_aest*s_aest;",
         "aest_tangent_trace_force(k,tau,-0.5*a*Q_aest*Braw_aest/pba->aest_KB);",
         "dy[pv->index_pt_E_aest] += aest_tangent_external_force(k,tau);",
         "E_rhs_aest -= 0.5*Q_aest*Bchi_aest","AEST_TANGENT_FORCE_FILE","AEST_TANGENT_LAMBDA")
    return all(x in p+a for x in req)

def run_transfer(kh,sampling):
    from classy import Class
    bits=r2.pc.bits_for_anchor(kh)
    p,pos=r2.amp.make_params(kh,int(bits))
    p["tol_perturbations_integration"]=float(TOL)
    p["perturb_sampling_stepsize"]=float(sampling)
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
        return {"D":D,"W":W,"h":float(h),"finite":finite,"basis_pass":basis,
                "bits":int(bits),"target_pos":int(pos)}
    finally:
        c.struct_cleanup(); c.empty()

def worker(args):
    v=run_transfer(float(args.kh),float(args.sampling))
    np.savez_compressed(args.out,D=v["D"],W=v["W"],redshifts=Z,h=np.asarray([v["h"]]),
                        finite=np.asarray([int(v["finite"])]),basis=np.asarray([int(v["basis_pass"])]))
    print(json.dumps({"k_h":float(args.kh),"sampling":float(args.sampling),
                      "h":v["h"],"finite":v["finite"],"basis_pass":v["basis_pass"]},sort_keys=True))
    return 0 if v["basis_pass"] else 2

def load_case(path):
    q=np.load(path)
    return {"D":np.asarray(q["D"],float),"W":np.asarray(q["W"],float),
            "h":float(q["h"][0]),"finite":bool(int(q["finite"][0])),
            "basis_pass":bool(int(q["basis"][0]))}

def force_stats(path,kh,h):
    rows=[]
    for line in path.read_text(errors="replace").splitlines():
        p=line.split()
        if len(p)!=3: continue
        try: k,t,f=map(float,p)
        except ValueError: continue
        if np.isfinite(k) and np.isfinite(t) and np.isfinite(f): rows.append((k,t,f))
    if not rows: return {"pass":False,"reason":"empty","target_k_samples":0}
    kvals=np.asarray(sorted({x[0] for x in rows}),float); kt=float(kh*h)
    kk=float(kvals[int(np.argmin(np.abs(kvals-kt)))])
    rr=abs(kk-kt)/max(abs(kt),1e-300)
    tr=[x for x in rows if x[0]==kk]
    taus=np.asarray([x[1] for x in tr],float); fs=np.asarray([x[2] for x in tr],float)
    good=bool(rr<=2e-10 and len(tr)>=8 and np.all(np.isfinite(fs)) and np.all(np.diff(taus)>0))
    return {"pass":good,"target_k_samples":len(tr),"relative_k_error":rr,
            "force_l2":float(np.linalg.norm(fs)),"force_max_abs":float(np.max(np.abs(fs)))}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--worker",action="store_true"); ap.add_argument("--kh",type=float)
    ap.add_argument("--sampling",type=float); ap.add_argument("--out")
    ap.add_argument("--json-out",default="results/stable_aest_growth_weyl_memory_r2c_normalization.json")
    ap.add_argument("--npz-out",default="results/stable_aest_growth_weyl_memory_r2c_normalization.npz")
    ap.add_argument("--workdir",default="results/stable_aest_growth_weyl_memory_r2c_work")
    args=ap.parse_args()
    if args.worker:
        if args.kh is None or args.sampling is None or not args.out:
            raise SystemExit("worker requires --kh --sampling --out")
        return worker(args)

    print("STABLE_AEST_GROWTH_WEYL_MEMORY_R2C_START",flush=True)
    req=(R2B_JSON,R2_NPZ,R1C_JSON,HOST_JSON)
    if any(not p.exists() for p in req):
        Path(args.json_out).write_text(json.dumps({"classification":CLS_INCOMPLETE,"diagnostic_complete":False},indent=2)+"\n")
        return 3
    r2b=json.loads(R2B_JSON.read_text()); r1c=json.loads(R1C_JSON.read_text()); host=json.loads(HOST_JSON.read_text())
    g1=bool(ancestor(PREDATA_LOCK) and ancestor(R2B_POSTDATA_LOCK) and source_ok()
            and r2b.get("classification")=="STABLE_AEST_GROWTH_WEYL_MEMORY_R2B_COMMON_MODE_BOUND_CERTIFIED"
            and r1c.get("classification")=="STABLE_AEST_FINITE_MEMORY_R1C_LONG_RELAXATION_CERTIFIED"
            and host.get("classification")=="FULLJ_AEST_STABLE_CHI_PRECISION_FLOOR_CERTIFIED")

    work=Path(args.workdir); work.mkdir(parents=True,exist_ok=True)
    py=sys.executable; mod="fullj_weyl.stable_aest_growth_weyl_memory_r2c_normalization"
    parent=np.load(R2_NPZ)
    baselines={}; cases={}; trace_rows=[]; arrays={"redshifts":Z}
    for s in SAMPLINGS:
        st=stag(s)
        for kh in ANCHORS:
            t=tag(kh); raw=work/f"force_{t}_{st}_raw.dat"; clean=work/f"force_{t}_{st}.dat"
            normjson=work/f"force_{t}_{st}.json"; trace_out=work/f"trace_{t}_{st}.npz"
            env=os.environ.copy()
            for key in ("AEST_TANGENT_FORCE_FILE","AEST_TANGENT_LAMBDA"): env.pop(key,None)
            env["AEST_TANGENT_TRACE_FILE"]=str(raw.resolve())
            subprocess.run([py,"-m",mod,"--worker","--kh",str(kh),"--sampling",str(s),"--out",str(trace_out)],
                           cwd=ROOT,env=env,check=True)
            base=load_case(trace_out); baselines[(s,kh)]=base
            subprocess.run([py,str(ROOT/"v019w"/"normalize_force_table.py"),str(raw),str(clean),
                            "--json-out",str(normjson)],cwd=ROOT,check=True)
            fs=force_stats(clean,kh,base["h"])
            trace_rows.append({"sampling":s,"k_h":kh,**fs})
            print(f"STABLE_AEST_GROWTH_WEYL_MEMORY_R2C_TRACE sampling={s:g} k_h={kh:.5f} "
                  f"pass={fs['pass']} samples={fs.get('target_k_samples',0)}",flush=True)
            arrays[f"D0_{t}_{st}"]=base["D"]; arrays[f"W0_{t}_{st}"]=base["W"]
            lambdas=(30.0,-30.0,10.0,-10.0) if s==SAMPLINGS[-1] else (30.0,-30.0)
            for lam in lambdas:
                lt=("p" if lam>0 else "m")+str(int(abs(lam))); out=work/f"case_{t}_{st}_{lt}.npz"
                env=os.environ.copy(); env.pop("AEST_TANGENT_TRACE_FILE",None)
                env["AEST_TANGENT_FORCE_FILE"]=str(clean.resolve()); env["AEST_TANGENT_LAMBDA"]=str(lam)
                subprocess.run([py,"-m",mod,"--worker","--kh",str(kh),"--sampling",str(s),"--out",str(out)],
                               cwd=ROOT,env=env,check=True)
                v=load_case(out); cases[(s,kh,lam)]=v
                arrays[f"D_{t}_{st}_{lt}"]=v["D"]; arrays[f"W_{t}_{st}_{lt}"]=v["W"]

    trace_map={(r["sampling"],r["k_h"]):r for r in trace_rows}; g2=True
    for kh in ANCHORS:
        a=trace_map[(SAMPLINGS[0],kh)]; b=trace_map[(SAMPLINGS[1],kh)]
        g2 &= bool(a["pass"] and b["pass"] and a["target_k_samples"]>26 and b["target_k_samples"]>a["target_k_samples"])

    neutral_rows=[]; g3=True
    for s in SAMPLINGS:
        for kh in ANCHORS:
            t=tag(kh); b=baselines[(s,kh)]
            ed=rel(b["D"],parent[f"D_{t}_e0p000"]); ew=rel(b["W"],parent[f"W_{t}_e0p000"])
            ok=bool(ed<=2e-5 and ew<=2e-5); g3 &= ok
            neutral_rows.append({"sampling":s,"k_h":kh,"D_relL2":ed,"W_relL2":ew,"pass":ok})

    rows=[]; grid_strict=0; grid_loose_all=True; norm_strict=0; norm_loose_all=True
    mismatch_all=True; lambda_all=True; avec=[]
    for kh in ANCHORS:
        t=tag(kh)
        refG=0.5*(np.asarray(parent[f"G005_{t}"],float)+np.asarray(parent[f"G010_{t}"],float))
        refL=0.5*(np.asarray(parent[f"L005_{t}"],float)+np.asarray(parent[f"L010_{t}"],float))
        dense={}
        for s in SAMPLINGS:
            st=stag(s); b=baselines[(s,kh)]
            p30=cases[(s,kh,30.0)]; m30=cases[(s,kh,-30.0)]
            G30=(p30["D"]-m30["D"])/(60.0*b["D"])
            L30=(p30["W"]-m30["W"])/(60.0*b["W"])
            dense[s]=(G30,L30); arrays[f"G30_{t}_{st}"]=G30; arrays[f"L30_{t}_{st}"]=L30
        G1,L1=dense[SAMPLINGS[0]]; G2v,L2v=dense[SAMPLINGS[1]]
        eg=rel(G1,G2v); el=rel(L1,L2v); cg=cosine(G1,G2v); cl=cosine(L1,L2v)
        gs=bool(eg<=.05 and el<=.05 and cg>=.999 and cl>=.999)
        gl=bool(eg<=.10 and el<=.10 and cg>=.995 and cl>=.995)
        grid_strict+=int(gs); grid_loose_all &= gl

        b=baselines[(SAMPLINGS[1],kh)]
        p10=cases[(SAMPLINGS[1],kh,10.0)]; m10=cases[(SAMPLINGS[1],kh,-10.0)]
        G10=(p10["D"]-m10["D"])/(20.0*b["D"]); L10=(p10["W"]-m10["W"])/(20.0*b["W"])
        egl=rel(G10,G2v); ell=rel(L10,L2v); cgl=cosine(G10,G2v); cll=cosine(L10,L2v)
        lok=bool(egl<=.02 and ell<=.02 and cgl>=.999 and cll>=.999); lambda_all &= lok

        eG=rel(G2v,refG); eL=rel(L2v,refL); cG=cosine(G2v,refG); cL=cosine(L2v,refL)
        aG=float(np.linalg.norm(refG)/max(float(np.linalg.norm(G2v)),1e-300))
        aL=float(np.linalg.norm(refL)/max(float(np.linalg.norm(L2v)),1e-300)); avec += [aG,aL]
        ns=bool(eG<=.05 and eL<=.05 and cG>=.999 and cL>=.999 and .95<=aG<=1.05 and .95<=aL<=1.05)
        nl=bool(eG<=.10 and eL<=.10 and cG>=.995 and cL>=.995 and .90<=aG<=1.10 and .90<=aL<=1.10)
        norm_strict+=int(ns); norm_loose_all &= nl
        amatch=abs(aG-aL)/max(abs(aG),abs(aL),1e-300)
        mm=bool(cG>=.999 and cL>=.999 and eG>.10 and eL>.10 and amatch<=.02); mismatch_all &= mm
        rows.append({"k_h":kh,"grid_E_G":eg,"grid_E_L":el,"grid_cos_G":cg,"grid_cos_L":cl,
                     "grid_strict":gs,"grid_loose":gl,"lambda_E_G":egl,"lambda_E_L":ell,
                     "lambda_cos_G":cgl,"lambda_cos_L":cll,"lambda_pass":lok,
                     "abs_E_G":eG,"abs_E_L":eL,"abs_cos_G":cG,"abs_cos_L":cL,
                     "A_G":aG,"A_L":aL,"norm_strict":ns,"norm_loose":nl,"coherent_mismatch":mm})
        arrays[f"Gref_{t}"]=refG; arrays[f"Lref_{t}"]=refL
        print("STABLE_AEST_GROWTH_WEYL_MEMORY_R2C_CELL "+json.dumps(rows[-1],sort_keys=True),flush=True)

    g4=bool(lambda_all); g5=bool(grid_strict>=2 and grid_loose_all)
    g6=bool(norm_strict>=2 and norm_loose_all)
    g7=bool(g2 and g3 and g4 and g5 and (not g6) and mismatch_all and max(avec)/max(min(avec),1e-300)<=1.10)
    gates={"R2C_G1_provenance_and_parent_lock":g1,"R2C_G2_source_grid_densification":g2,
           "R2C_G3_patch_neutrality":g3,"R2C_G4_dense_amplifier_consistency":g4,
           "R2C_G5_source_grid_convergence":g5,"R2C_G6_absolute_normalization":g6,
           "R2C_G7_coherent_normalization_mismatch":g7}
    if not g1: cls=CLS_INCOMPLETE
    elif not g2: cls=CLS_DENSE_FAIL
    elif not g3: cls=CLS_NEUTRAL_FAIL
    elif not g4: cls=CLS_TAN_FAIL
    elif not g5: cls=CLS_GRID_FAIL
    elif g6: cls=CLS_NORM_PASS
    elif g7: cls=CLS_MISMATCH
    else: cls=CLS_UNRES
    summary={"classification":cls,"trace_count":len(trace_rows),"grid_strict_count":grid_strict,
             "normalization_strict_count":norm_strict,"A_min":float(min(avec)),"A_max":float(max(avec))}
    out={"classification":cls,"diagnostic_complete":True,"predata_lock":PREDATA_LOCK,
         "r2b_parent_classification":r2b.get("classification"),"settings":{"samplings":SAMPLINGS,"anchors":ANCHORS,
         "tau_H0":TAU,"memory_order":ORDER,"physical_eta":0.0,"tol_perturbations_integration":TOL},
         "trace":trace_rows,"patch_neutrality":neutral_rows,"cells":rows,"gates":gates,"summary":summary,
         "interpretation":{"r2b_reclassified":False,"absolute_variational_tangent_licensed":cls==CLS_NORM_PASS,
         "global_normalization_mismatch_certified":cls==CLS_MISMATCH,
         "growth_Weyl_separation_certified":False,"observational_claim_licensed":False}}
    Path(args.json_out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    np.savez_compressed(args.npz_out,**arrays)
    print("STABLE_AEST_GROWTH_WEYL_MEMORY_R2C_GATES="+json.dumps(gates,sort_keys=True),flush=True)
    print("STABLE_AEST_GROWTH_WEYL_MEMORY_R2C_SUMMARY="+json.dumps(summary,sort_keys=True),flush=True)
    print("STABLE_AEST_GROWTH_WEYL_MEMORY_R2C_CLASSIFICATION="+cls,flush=True)
    return 0 if cls in (CLS_NORM_PASS,CLS_MISMATCH) else 1

if __name__=="__main__":
    raise SystemExit(main())
