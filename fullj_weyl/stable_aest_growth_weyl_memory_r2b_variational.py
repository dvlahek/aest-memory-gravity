#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fullj_weyl import stable_aest_growth_weyl_memory_r2 as r2

PREDATA_LOCK = "fc118356ea77be3b81854a95992a89ff7a1630bc"
R2A_POSTDATA_LOCK = "bbcf1e8e88743fb63ebe9b7e8da1202b8d3438dc"
R2A_JSON = ROOT / "results/stable_aest_growth_weyl_memory_r2a.json"
R1C_JSON = ROOT / "results/stable_aest_finite_memory_r1c.json"
HOST_JSON = ROOT / "results/fullj_aest_stable_chi_precision_floor.json"
R2_NPZ = ROOT / "results/stable_aest_growth_weyl_memory_r2.npz"

R2A_CLASS = "STABLE_AEST_GROWTH_WEYL_MEMORY_R2A_SEPARATION_UNRESOLVED"
R1C_CLASS = "STABLE_AEST_FINITE_MEMORY_R1C_LONG_RELAXATION_CERTIFIED"
HOST_CLASS = "FULLJ_AEST_STABLE_CHI_PRECISION_FLOOR_CERTIFIED"

ANCHORS = (0.09875, 0.16125, 0.19500)
LAMBDAS = (0.0, 1.0, -1.0, 10.0, -10.0, 30.0, -30.0)
TAU = 10.0
ORDER = 20
TOL = 3e-8
Z = np.asarray([6.,5.,4.,3.,2.,1.5,1.,0.5,0.2], float)

INCOMPLETE = "STABLE_AEST_GROWTH_WEYL_MEMORY_R2B_INCOMPLETE"
FORCE_FAIL = "STABLE_AEST_GROWTH_WEYL_MEMORY_R2B_FORCE_TRACE_FAIL"
NEUTRAL_FAIL = "STABLE_AEST_GROWTH_WEYL_MEMORY_R2B_PATCH_NEUTRALITY_FAIL"
TANGENT_FAIL = "STABLE_AEST_GROWTH_WEYL_MEMORY_R2B_VARIATIONAL_TANGENT_FAIL"
SEP_PASS = "STABLE_AEST_GROWTH_WEYL_MEMORY_R2B_SEPARATION_CERTIFIED"
COMMON_PASS = "STABLE_AEST_GROWTH_WEYL_MEMORY_R2B_COMMON_MODE_BOUND_CERTIFIED"
UNRESOLVED = "STABLE_AEST_GROWTH_WEYL_MEMORY_R2B_SEPARATION_UNRESOLVED"


def ancestor(sha: str) -> bool:
    return subprocess.run(["git","merge-base","--is-ancestor",sha,"HEAD"], cwd=ROOT,
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0


def rel(a,b) -> float:
    a=np.asarray(a,float); b=np.asarray(b,float)
    return float(np.linalg.norm(a-b)/max(float(np.linalg.norm(a)),float(np.linalg.norm(b)),1e-300))


def cosine(a,b) -> float:
    a=np.asarray(a,float); b=np.asarray(b,float)
    na=float(np.linalg.norm(a)); nb=float(np.linalg.norm(b))
    if na<=0 or nb<=0: return float("nan")
    return float(np.dot(a,b)/(na*nb))


def tag(kh: float) -> str:
    return r2.pc.tag_of(kh)


def ltag(lam: float) -> str:
    if lam == 0: return "0"
    return ("p" if lam>0 else "m") + str(int(abs(lam)))


def source_ok() -> bool:
    root=os.environ.get("AEST_STABLE_VAR_CLASS_ROOT","")
    if not root: return False
    root=Path(root)
    pc=(root/"source"/"perturbations.c")
    am=(root/"source"/"aest_memory.c")
    if not pc.is_file() or not am.is_file(): return False
    p=pc.read_text(); a=am.read_text()
    req=(
        "FULLJ_AEST_STABLE_CHI_RESIDUAL_V1",
        "FULLJ_STABLE_AEST_R2B_VARIATIONAL_V1",
        "double s_aest=y[ppw->pv->index_pt_s_aest];",
        "double chi_aest=Q_aest*s_aest;",
        "aest_tangent_trace_force(k,tau,-0.5*a*Q_aest*Braw_aest/pba->aest_KB);",
        "dy[pv->index_pt_E_aest] += aest_tangent_external_force(k,tau);",
        "E_rhs_aest -= 0.5*Q_aest*Bchi_aest",
        "AEST_TANGENT_FORCE_FILE",
        "AEST_TANGENT_LAMBDA",
    )
    return all(x in (p+a) for x in req) and "Q_aest*(a*theta_aest/(k*k)+alpha_aest)" not in p


def run_transfer(kh: float):
    from classy import Class
    bits=r2.pc.bits_for_anchor(kh)
    p,pos=r2.amp.make_params(kh,int(bits))
    p["tol_perturbations_integration"]=float(TOL)
    p["aest_memory_enabled"]="yes"
    p["aest_memory_order"]=int(ORDER)
    p["aest_eta"]=0.0
    p["aest_tau_H0"]=float(TAU)
    p["output"]="mTk,vTk"
    p["z_max_pk"]=max(float(p.get("z_max_pk",0.0)),6.5)
    c=Class(); c.set(p); c.compute()
    try:
        h=r2.classy_h(c); D=[]; W=[]; domains=[]; keys=[]
        for z in Z:
            tr=c.get_transfer(z=float(z),output_format="class")
            missing=[x for x in ("d_m","phi","psi") if x not in tr]
            if missing: raise RuntimeError(f"missing transfer fields {missing}")
            kg,kkey=r2.k_h_from_transfer(tr,h)
            dm,klo,khi,nk=r2.interp_transfer_field(kg,tr["d_m"],kh)
            ph,_,_,_=r2.interp_transfer_field(kg,tr["phi"],kh)
            ps,_,_,_=r2.interp_transfer_field(kg,tr["psi"],kh)
            D.append(dm); W.append(ph+ps); domains.append((klo,khi,nk)); keys.append(kkey)
        D=np.asarray(D,float); W=np.asarray(W,float)
        finite=bool(np.all(np.isfinite(D)) and np.all(np.isfinite(W)))
        basis=bool(finite and all(x[0]<=kh<=x[1] and x[2]>=4 for x in domains) and len(set(keys))==1)
        return {"D":D,"W":W,"h":float(h),"finite":finite,"basis_pass":basis,
                "bits":int(bits),"target_pos":int(pos),"k_key":keys[0] if keys else None}
    finally:
        c.struct_cleanup(); c.empty()


def worker(args) -> int:
    v=run_transfer(float(args.kh))
    np.savez_compressed(args.out,D=v["D"],W=v["W"],redshifts=Z,h=np.asarray([v["h"]]),
                        finite=np.asarray([int(v["finite"])]),basis=np.asarray([int(v["basis_pass"])]),
                        bits=np.asarray([v["bits"]],dtype=np.int64),target_pos=np.asarray([v["target_pos"]],dtype=np.int64))
    print(json.dumps({"k_h":float(args.kh),"h":v["h"],"finite":v["finite"],"basis_pass":v["basis_pass"]},sort_keys=True))
    return 0 if v["basis_pass"] else 2


def load_case(path: Path):
    q=np.load(path)
    return {"D":np.asarray(q["D"],float),"W":np.asarray(q["W"],float),"h":float(q["h"][0]),
            "finite":bool(int(q["finite"][0])),"basis_pass":bool(int(q["basis"][0]))}


def target_force_stats(path: Path, kh: float, h: float):
    rows=[]
    for line in path.read_text(errors="replace").splitlines():
        p=line.split()
        if len(p)!=3: continue
        try: k,t,f=map(float,p)
        except ValueError: continue
        if np.isfinite(k) and np.isfinite(t) and np.isfinite(f): rows.append((k,t,f))
    if not rows: return {"pass":False,"reason":"empty"}
    kvals=np.asarray(sorted({x[0] for x in rows}),float)
    kt=float(kh*h)
    j=int(np.argmin(np.abs(kvals-kt))); kk=float(kvals[j]); rr=abs(kk-kt)/max(abs(kt),1e-300)
    tr=[x for x in rows if x[0]==kk]
    taus=np.asarray([x[1] for x in tr],float); fs=np.asarray([x[2] for x in tr],float)
    good=bool(rr<=2e-10 and len(tr)>=8 and np.all(np.isfinite(fs)) and np.all(np.diff(taus)>0))
    return {"pass":good,"target_k_internal":kt,"matched_k_internal":kk,"relative_k_error":rr,
            "target_k_samples":len(tr),"force_l2":float(np.linalg.norm(fs)),"force_max_abs":float(np.max(np.abs(fs)))}


def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--worker",action="store_true")
    ap.add_argument("--kh",type=float)
    ap.add_argument("--out")
    ap.add_argument("--json-out",default="results/stable_aest_growth_weyl_memory_r2b_variational.json")
    ap.add_argument("--npz-out",default="results/stable_aest_growth_weyl_memory_r2b_variational.npz")
    ap.add_argument("--workdir",default="results/stable_aest_growth_weyl_memory_r2b_work")
    args=ap.parse_args()
    if args.worker:
        if args.kh is None or not args.out: raise SystemExit("worker requires --kh and --out")
        return worker(args)

    print("STABLE_AEST_GROWTH_WEYL_MEMORY_R2B_START",flush=True)
    for p in (R2A_JSON,R1C_JSON,HOST_JSON,R2_NPZ):
        if not p.exists():
            Path(args.json_out).write_text(json.dumps({"classification":INCOMPLETE,"diagnostic_complete":False,"reason":f"missing {p}"},indent=2)+"\n")
            return 3
    r2a=json.loads(R2A_JSON.read_text()); r1c=json.loads(R1C_JSON.read_text()); host=json.loads(HOST_JSON.read_text())
    g1=bool(ancestor(PREDATA_LOCK) and ancestor(R2A_POSTDATA_LOCK)
            and r2a.get("classification")==R2A_CLASS and r1c.get("classification")==R1C_CLASS
            and host.get("classification")==HOST_CLASS and source_ok())

    work=Path(args.workdir); work.mkdir(parents=True,exist_ok=True)
    py=sys.executable; mod="fullj_weyl.stable_aest_growth_weyl_memory_r2b_variational"
    cases={}; trace_rows=[]; force_ok=True; basis_ok=True
    arrays={"redshifts":Z}

    for kh in ANCHORS:
        t=tag(kh); raw=work/f"force_{t}_raw.dat"; clean=work/f"force_{t}.dat"; stats=work/f"force_{t}.json"
        trace_out=work/f"trace_{t}.npz"
        env=os.environ.copy(); env.pop("AEST_TANGENT_FORCE_FILE",None); env.pop("AEST_TANGENT_LAMBDA",None)
        env["AEST_TANGENT_TRACE_FILE"]=str(raw.resolve())
        subprocess.run([py,"-m",mod,"--worker","--kh",str(kh),"--out",str(trace_out)],cwd=ROOT,env=env,check=True)
        tv=load_case(trace_out); basis_ok &= tv["basis_pass"]
        subprocess.run([py,str(ROOT/"v019w"/"normalize_force_table.py"),str(raw),str(clean),"--json-out",str(stats)],cwd=ROOT,check=True)
        fs=target_force_stats(clean,kh,tv["h"]); force_ok &= fs["pass"]
        trace_rows.append({"k_h":kh,**fs})
        print(f"STABLE_AEST_GROWTH_WEYL_MEMORY_R2B_TRACE k_h={kh:.5f} pass={fs['pass']} samples={fs.get('target_k_samples',0)} force_l2={fs.get('force_l2',float('nan')):.3e}",flush=True)

        for lam in LAMBDAS:
            out=work/f"case_{t}_{ltag(lam)}.npz"
            env=os.environ.copy(); env.pop("AEST_TANGENT_TRACE_FILE",None)
            env["AEST_TANGENT_FORCE_FILE"]=str(clean.resolve()); env["AEST_TANGENT_LAMBDA"]=str(lam)
            subprocess.run([py,"-m",mod,"--worker","--kh",str(kh),"--out",str(out)],cwd=ROOT,env=env,check=True)
            v=load_case(out); cases[(kh,lam)]=v; basis_ok &= v["basis_pass"]
            arrays[f"D_{t}_{ltag(lam)}"]=v["D"]; arrays[f"W_{t}_{ltag(lam)}"]=v["W"]
            print(f"STABLE_AEST_GROWTH_WEYL_MEMORY_R2B_RUN k_h={kh:.5f} lambda={lam:g} basis={v['basis_pass']}",flush=True)

    # Patch neutrality against frozen R2 eta=0 arrays.
    parent=np.load(R2_NPZ); neutral_rows=[]; neutral_ok=True
    for kh in ANCHORS:
        t=tag(kh); v0=cases[(kh,0.0)]
        pd=np.asarray(parent[f"D_{t}_e0p000"],float); pw=np.asarray(parent[f"W_{t}_e0p000"],float)
        ed=rel(v0["D"],pd); ew=rel(v0["W"],pw); ok=bool(ed<=2e-5 and ew<=2e-5)
        neutral_ok &= ok; neutral_rows.append({"k_h":kh,"D_relL2":ed,"W_relL2":ew,"pass":ok})
        print(f"STABLE_AEST_GROWTH_WEYL_MEMORY_R2B_NEUTRAL k_h={kh:.5f} D={ed:.3e} W={ew:.3e} pass={ok}",flush=True)

    tangent_rows=[]; sep_count=0; common_count=0; strict_count=0; loose_all=True
    if basis_ok and force_ok and neutral_ok:
        for kh in ANCHORS:
            v0=cases[(kh,0.0)]; D0=v0["D"]; W0=v0["W"]
            tang={}
            for lam in (1.0,10.0,30.0):
                vp=cases[(kh,lam)]; vm=cases[(kh,-lam)]
                TD=(vp["D"]-vm["D"])/(2.*lam); TW=(vp["W"]-vm["W"])/(2.*lam)
                G=TD/D0; L=TW/W0; R=L-G; tang[lam]=(G,L,R)
                t=tag(kh); lt=f"l{int(lam)}"
                arrays[f"G_{t}_{lt}"]=G; arrays[f"L_{t}_{lt}"]=L; arrays[f"R_{t}_{lt}"]=R
            G1,L1,R1=tang[1.0]; G10,L10,R10=tang[10.0]; G30,L30,R30=tang[30.0]
            eg=rel(G10,G30); el=rel(L10,L30); strict=bool(max(eg,el)<=0.02); loose=bool(max(eg,el)<=0.05)
            strict_count += int(strict); loose_all &= loose
            er=rel(R10,R30); cr=cosine(R10,R30); qr=float(np.linalg.norm(R30)/max(float(np.linalg.norm(R10-R30)),1e-300))
            sep=bool(er<=0.20 and cr>=0.95 and qr>=3.0); sep_count += int(sep)
            b30=float(np.linalg.norm(R30)/max(float(np.linalg.norm(G30)),float(np.linalg.norm(L30)),1e-300)); common=bool(b30<=0.01); common_count += int(common)
            row={"k_h":kh,"E_G_10_30":eg,"E_L_10_30":el,"E_G_1_10":rel(G1,G10),"E_L_1_10":rel(L1,L10),
                 "strict_individual":strict,"loose_individual":loose,"E_R_10_30":er,"cos_R_10_30":cr,"Q_R":qr,
                 "separation_resolved":sep,"B_30":b30,"common_mode_1pct":common}
            tangent_rows.append(row)
            print(f"STABLE_AEST_GROWTH_WEYL_MEMORY_R2B_TANGENT k_h={kh:.5f} EG={eg:.3e} EL={el:.3e} ER={er:.3e} cos={cr:.6f} Q={qr:.3e} B={b30:.3e} sep={sep} common={common}",flush=True)

    g2=bool(force_ok and basis_ok); g3=bool(neutral_ok); g4=bool(loose_all and strict_count>=2)
    gates={"R2B_G1_provenance_and_parent_lock":g1,"R2B_G2_forcing_trace_validity":g2,
           "R2B_G3_patch_neutrality":g3,"R2B_G4_amplified_individual_tangent_consistency":g4,
           "R2B_G5_resolved_separation_count_ge2":bool(sep_count>=2),"R2B_G6_common_mode_bound_all3":bool(common_count==3)}
    if not g1: cl=INCOMPLETE
    elif not g2: cl=FORCE_FAIL
    elif not g3: cl=NEUTRAL_FAIL
    elif not g4: cl=TANGENT_FAIL
    elif sep_count>=2: cl=SEP_PASS
    elif common_count==3: cl=COMMON_PASS
    else: cl=UNRESOLVED
    summary={"classification":cl,"trace_pass_count":sum(int(x["pass"]) for x in trace_rows),"neutral_pass_count":sum(int(x["pass"]) for x in neutral_rows),
             "individual_strict_pass_count":strict_count,"separation_resolved_count":sep_count,"common_mode_1pct_count":common_count,
             "max_B_30":float(max((x["B_30"] for x in tangent_rows),default=float("nan"))),
             "max_E_R_10_30":float(max((x["E_R_10_30"] for x in tangent_rows),default=float("nan"))),
             "min_Q_R":float(min((x["Q_R"] for x in tangent_rows),default=float("nan")))}
    out={"classification":cl,"diagnostic_complete":True,"predata_lock":PREDATA_LOCK,"r2a_parent_classification":r2a.get("classification"),
         "r1c_parent_classification":r1c.get("classification"),"host_parent_classification":host.get("classification"),
         "settings":{"anchors":list(ANCHORS),"lambdas":list(LAMBDAS),"physical_eta":0.0,"tau_H0":TAU,"memory_order":ORDER,"tol_perturbations_integration":TOL,
                     "growth_observable":"CLASS d_m","weyl_observable":"CLASS phi+psi","redshifts":Z.tolist()},
         "force_trace":trace_rows,"patch_neutrality":neutral_rows,"variational_tangent":tangent_rows,"gates":gates,"summary":summary,
         "interpretation":{"historical_R2_reclassified":False,"historical_R2a_reclassified":False,
                           "growth_Weyl_separation_certified":cl==SEP_PASS,"common_mode_bound_certified":cl==COMMON_PASS,
                           "MCMG_bridge_followup_licensed":cl==SEP_PASS,"observational_claim_licensed":False,"new_physics_claim_licensed":False}}
    Path(args.json_out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    np.savez_compressed(args.npz_out,**arrays)
    print("STABLE_AEST_GROWTH_WEYL_MEMORY_R2B_GATES="+json.dumps(gates,sort_keys=True),flush=True)
    print("STABLE_AEST_GROWTH_WEYL_MEMORY_R2B_SUMMARY="+json.dumps(summary,sort_keys=True),flush=True)
    print("STABLE_AEST_GROWTH_WEYL_MEMORY_R2B_CLASSIFICATION="+cl,flush=True)
    return 0 if cl in (SEP_PASS,COMMON_PASS) else 1


if __name__ == "__main__":
    raise SystemExit(main())
