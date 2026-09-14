#!/usr/bin/env python3
from __future__ import annotations

import argparse, json, os, re, subprocess, sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fullj_weyl import stable_aest_growth_weyl_memory_r2 as r2
from fullj_weyl import stable_aest_growth_weyl_memory_r2d_full_history as r2d

PREDATA_LOCK = "176b69261d61c9d43116a9bf82a99839fe328b43"
R2D_POSTDATA_LOCK = "d2589759cda81a590008c184cc2b061eada3ee28"
R2D_JSON = ROOT / "results/stable_aest_growth_weyl_memory_r2d_full_history.json"
R2D_NPZ = ROOT / "results/stable_aest_growth_weyl_memory_r2d_full_history.npz"
R2C_JSON = ROOT / "results/stable_aest_growth_weyl_memory_r2c_normalization.json"
R2B_JSON = ROOT / "results/stable_aest_growth_weyl_memory_r2b_variational.json"
R2_NPZ = ROOT / "results/stable_aest_growth_weyl_memory_r2.npz"
R1C_JSON = ROOT / "results/stable_aest_finite_memory_r1c.json"
HOST_JSON = ROOT / "results/fullj_aest_stable_chi_precision_floor.json"
R2D_WORK = ROOT / "results/stable_aest_growth_weyl_memory_r2d_work"

ANCHORS = (0.09875, 0.16125, 0.19500)
Z = np.asarray([6.,5.,4.,3.,2.,1.5,1.,0.5,0.2], float)
HOOK = "dy[pv->index_pt_E_aest] += aest_tangent_external_force(k,tau);"

CLS_INCOMPLETE = "STABLE_AEST_GROWTH_WEYL_MEMORY_R2E_INCOMPLETE"
CLS_SOURCE = "STABLE_AEST_GROWTH_WEYL_MEMORY_R2E_SINGLE_HOOK_SOURCE_FAIL"
CLS_NEUTRAL = "STABLE_AEST_GROWTH_WEYL_MEMORY_R2E_PATCH_NEUTRALITY_FAIL"
CLS_TANGENT = "STABLE_AEST_GROWTH_WEYL_MEMORY_R2E_VARIATIONAL_TANGENT_FAIL"
CLS_COMMON = "STABLE_AEST_GROWTH_WEYL_MEMORY_R2E_SINGLE_HOOK_ABSOLUTE_COMMON_MODE_CERTIFIED"
CLS_SEP = "STABLE_AEST_GROWTH_WEYL_MEMORY_R2E_SINGLE_HOOK_ABSOLUTE_SEPARATION_CERTIFIED"
CLS_NORM = "STABLE_AEST_GROWTH_WEYL_MEMORY_R2E_SINGLE_HOOK_NORMALIZATION_CERTIFIED"
CLS_UNRES = "STABLE_AEST_GROWTH_WEYL_MEMORY_R2E_SINGLE_HOOK_NORMALIZATION_UNRESOLVED"


def ancestor(sha: str) -> bool:
    return subprocess.run(["git","merge-base","--is-ancestor",sha,"HEAD"],cwd=ROOT,
                          stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode == 0


def rel(a,b):
    a=np.asarray(a,float); b=np.asarray(b,float)
    return float(np.linalg.norm(a-b)/max(float(np.linalg.norm(a)),float(np.linalg.norm(b)),1e-300))


def cosine(a,b):
    a=np.asarray(a,float); b=np.asarray(b,float)
    na=float(np.linalg.norm(a)); nb=float(np.linalg.norm(b))
    return float(np.dot(a,b)/(na*nb)) if na>0. and nb>0. else float("nan")


def source_audit():
    root=os.environ.get("AEST_STABLE_R2E_CLASS_ROOT","")
    if not root:
        return {"pass":False,"reason":"missing AEST_STABLE_R2E_CLASS_ROOT"}
    root=Path(root); pc=root/"source/perturbations.c"; am=root/"source/aest_memory.c"
    if not pc.is_file() or not am.is_file():
        return {"pass":False,"reason":"missing source files"}
    p=pc.read_text(); a=am.read_text()
    hook_count=p.count(HOOK)
    helper_defs=len(re.findall(r"\bdouble\s+aest_tangent_external_force\s*\(",a))
    checks={
        "r2e_marker":"FULLJ_STABLE_AEST_R2E_SINGLE_HOOK_V1" in p,
        "external_force_hook_count_one":hook_count==1,
        "runtime_external_helper_count_one":helper_defs==1,
        "stable_chi_present":("double chi_aest = Q_aest*s_aest;" in p or "double chi_aest=Q_aest*s_aest;" in p),
        "physical_eta_multiply_once":p.count("Bchi_aest *= pba->aest_eta;")==1,
        "physical_closure_once":p.count("E_rhs_aest -= 0.5*Q_aest*Bchi_aest;")==1,
    }
    return {"pass":bool(all(checks.values())),"hook_count":hook_count,"helper_defs":helper_defs,"checks":checks}


def worker(args):
    v=r2d.run_transfer(float(args.kh))
    np.savez_compressed(args.out,D=v["D"],W=v["W"],redshifts=Z,h=np.asarray([v["h"]]),
                        finite=np.asarray([int(v["finite"])]),basis=np.asarray([int(v["basis_pass"])]))
    print(json.dumps({"k_h":float(args.kh),"h":v["h"],"finite":v["finite"],"basis_pass":v["basis_pass"]},sort_keys=True))
    return 0 if v["basis_pass"] else 2


def load_case(path):
    q=np.load(path)
    return {"D":np.asarray(q["D"],float),"W":np.asarray(q["W"],float),"h":float(q["h"][0]),
            "finite":bool(int(q["finite"][0])),"basis_pass":bool(int(q["basis"][0]))}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--worker",action="store_true")
    ap.add_argument("--kh",type=float)
    ap.add_argument("--out")
    ap.add_argument("--json-out",default="results/stable_aest_growth_weyl_memory_r2e_single_hook.json")
    ap.add_argument("--npz-out",default="results/stable_aest_growth_weyl_memory_r2e_single_hook.npz")
    ap.add_argument("--workdir",default="results/stable_aest_growth_weyl_memory_r2e_work")
    args=ap.parse_args()
    if args.worker:
        if args.kh is None or not args.out:
            raise SystemExit("worker requires --kh --out")
        return worker(args)

    print("STABLE_AEST_GROWTH_WEYL_MEMORY_R2E_START",flush=True)
    req=(R2D_JSON,R2D_NPZ,R2C_JSON,R2B_JSON,R2_NPZ,R1C_JSON,HOST_JSON)
    force_paths={kh:R2D_WORK/f"rhs_force_{r2d.tag(kh)}.dat" for kh in ANCHORS}
    if any(not p.exists() for p in req) or any(not p.exists() for p in force_paths.values()):
        out={"classification":CLS_INCOMPLETE,"diagnostic_complete":False,"reason":"missing parent result or frozen R2d force table"}
        Path(args.json_out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
        print("STABLE_AEST_GROWTH_WEYL_MEMORY_R2E_CLASSIFICATION="+CLS_INCOMPLETE,flush=True)
        return 3

    r2dj=json.loads(R2D_JSON.read_text()); r2cj=json.loads(R2C_JSON.read_text()); r2bj=json.loads(R2B_JSON.read_text())
    r1cj=json.loads(R1C_JSON.read_text()); host=json.loads(HOST_JSON.read_text())
    g1=bool(ancestor(PREDATA_LOCK) and ancestor(R2D_POSTDATA_LOCK)
            and r2dj.get("classification")=="STABLE_AEST_GROWTH_WEYL_MEMORY_R2D_NON_HISTORY_NORMALIZATION_MISMATCH_CERTIFIED"
            and r2cj.get("classification")=="STABLE_AEST_GROWTH_WEYL_MEMORY_R2C_GLOBAL_NORMALIZATION_MISMATCH_CERTIFIED"
            and r2bj.get("classification")=="STABLE_AEST_GROWTH_WEYL_MEMORY_R2B_COMMON_MODE_BOUND_CERTIFIED"
            and r1cj.get("classification")=="STABLE_AEST_FINITE_MEMORY_R1C_LONG_RELAXATION_CERTIFIED"
            and host.get("classification")=="FULLJ_AEST_STABLE_CHI_PRECISION_FLOOR_CERTIFIED")
    sa=source_audit(); g2=bool(sa.get("pass"))

    work=Path(args.workdir); work.mkdir(parents=True,exist_ok=True)
    py=sys.executable; mod="fullj_weyl.stable_aest_growth_weyl_memory_r2e_single_hook"
    parent=np.load(R2_NPZ); old=np.load(R2D_NPZ)
    baselines={}; cases={}; neutral=[]; arrays={"redshifts":Z}

    for kh in ANCHORS:
        t=r2d.tag(kh); base_out=work/f"baseline_{t}.npz"
        env=os.environ.copy()
        for key in ("AEST_TANGENT_FORCE_FILE","AEST_TANGENT_LAMBDA","AEST_TANGENT_TRACE_FILE",
                    "AEST_R2D_TRACE_FILE","AEST_R2D_TRACE_KH","AEST_R2D_TRACE_ALL_K"):
            env.pop(key,None)
        subprocess.run([py,"-m",mod,"--worker","--kh",str(kh),"--out",str(base_out)],cwd=ROOT,env=env,check=True)
        b=load_case(base_out); baselines[kh]=b
        d0=np.asarray(parent[f"D_{t}_e0p000"],float); w0=np.asarray(parent[f"W_{t}_e0p000"],float)
        ed=rel(b["D"],d0); ew=rel(b["W"],w0); ok=bool(ed<=2e-5 and ew<=2e-5)
        neutral.append({"k_h":kh,"D_relL2":ed,"W_relL2":ew,"pass":ok})
        arrays[f"D0_{t}"]=b["D"]; arrays[f"W0_{t}"]=b["W"]
        print(f"STABLE_AEST_GROWTH_WEYL_MEMORY_R2E_BASELINE k_h={kh:.5f} D={ed:.3e} W={ew:.3e} pass={ok}",flush=True)

        for lam in (30.0,-30.0,10.0,-10.0):
            lt=("p" if lam>0 else "m")+str(int(abs(lam))); out=work/f"case_{t}_{lt}.npz"
            env=os.environ.copy()
            for key in ("AEST_TANGENT_TRACE_FILE","AEST_R2D_TRACE_FILE","AEST_R2D_TRACE_KH","AEST_R2D_TRACE_ALL_K"):
                env.pop(key,None)
            env["AEST_TANGENT_FORCE_FILE"]=str(force_paths[kh].resolve())
            env["AEST_TANGENT_LAMBDA"]=str(lam)
            subprocess.run([py,"-m",mod,"--worker","--kh",str(kh),"--out",str(out)],cwd=ROOT,env=env,check=True)
            v=load_case(out); cases[(kh,lam)]=v
            arrays[f"D_{t}_{lt}"]=v["D"]; arrays[f"W_{t}_{lt}"]=v["W"]

    g3=all(x["pass"] for x in neutral)
    rows=[]; amp_all=True; strict_count=0; loose_all=True; common_all=True; sep_count=0

    for kh in ANCHORS:
        t=r2d.tag(kh); b=baselines[kh]
        p30,m30=cases[(kh,30.0)],cases[(kh,-30.0)]; p10,m10=cases[(kh,10.0)],cases[(kh,-10.0)]
        G30=(p30["D"]-m30["D"])/(60.0*b["D"]); L30=(p30["W"]-m30["W"])/(60.0*b["W"])
        G10=(p10["D"]-m10["D"])/(20.0*b["D"]); L10=(p10["W"]-m10["W"])/(20.0*b["W"])
        R30=L30-G30; R10=L10-G10
        refG=.5*(np.asarray(parent[f"G005_{t}"],float)+np.asarray(parent[f"G010_{t}"],float))
        refL=.5*(np.asarray(parent[f"L005_{t}"],float)+np.asarray(parent[f"L010_{t}"],float))
        oldG=np.asarray(old[f"G30_{t}"],float); oldL=np.asarray(old[f"L30_{t}"],float)

        elG=rel(G10,G30); elL=rel(L10,L30); clG=cosine(G10,G30); clL=cosine(L10,L30)
        amp=bool(elG<=.02 and elL<=.02 and clG>=.999 and clL>=.999); amp_all &= amp
        eG=rel(G30,refG); eL=rel(L30,refL); cG=cosine(G30,refG); cL=cosine(L30,refL)
        aG=float(np.linalg.norm(refG)/max(float(np.linalg.norm(G30)),1e-300)); aL=float(np.linalg.norm(refL)/max(float(np.linalg.norm(L30)),1e-300))
        sG=float(np.linalg.norm(oldG)/max(float(np.linalg.norm(G30)),1e-300)); sL=float(np.linalg.norm(oldL)/max(float(np.linalg.norm(L30)),1e-300))
        coG=cosine(oldG,G30); coL=cosine(oldL,L30)
        strict=bool(eG<=.05 and eL<=.05 and cG>=.999 and cL>=.999 and .95<=aG<=1.05 and .95<=aL<=1.05
                    and 1.95<=sG<=2.05 and 1.95<=sL<=2.05 and coG>=.999 and coL>=.999)
        loose=bool(eG<=.10 and eL<=.10 and cG>=.995 and cL>=.995 and .90<=aG<=1.10 and .90<=aL<=1.10
                   and 1.90<=sG<=2.10 and 1.90<=sL<=2.10 and coG>=.995 and coL>=.995)
        strict_count += int(strict); loose_all &= loose
        B=float(np.linalg.norm(R30)/max(float(np.linalg.norm(G30)),float(np.linalg.norm(L30)),1e-300))
        cm=bool(B<=.01); common_all &= cm
        eR=rel(R10,R30); cR=cosine(R10,R30); sep=bool(B>.01 and eR<=.20 and cR>=.95); sep_count += int(sep)
        row={"k_h":kh,"lambda_E_G":elG,"lambda_E_L":elL,"lambda_cos_G":clG,"lambda_cos_L":clL,
             "lambda_pass":amp,"abs_E_G":eG,"abs_E_L":eL,"abs_cos_G":cG,"abs_cos_L":cL,
             "A_G":aG,"A_L":aL,"S_G_old_over_new":sG,"S_L_old_over_new":sL,
             "old_new_cos_G":coG,"old_new_cos_L":coL,"causal_strict":strict,"causal_loose":loose,
             "B_30":B,"common_mode_pass":cm,"E_R":eR,"C_R":cR,"resolved_separation":sep}
        rows.append(row)
        arrays[f"G30_{t}"]=G30; arrays[f"L30_{t}"]=L30; arrays[f"R30_{t}"]=R30
        arrays[f"G10_{t}"]=G10; arrays[f"L10_{t}"]=L10; arrays[f"R10_{t}"]=R10
        arrays[f"Gref_{t}"]=refG; arrays[f"Lref_{t}"]=refL
        print("STABLE_AEST_GROWTH_WEYL_MEMORY_R2E_CELL "+json.dumps(row,sort_keys=True),flush=True)

    g4=bool(amp_all); g5=bool(strict_count>=2 and loose_all); g6=bool(common_all); g7=bool(g5 and (not g6) and sep_count>=2)
    gates={"R2E_G1_provenance_and_parent_lock":g1,"R2E_G2_single_hook_source_correction":g2,
           "R2E_G3_patch_neutrality":g3,"R2E_G4_corrected_amplifier_consistency":g4,
           "R2E_G5_duplicate_hook_causal_normalization":g5,"R2E_G6_corrected_common_mode_bound":g6,
           "R2E_G7_resolved_corrected_separation":g7}
    if not g1: cls=CLS_INCOMPLETE
    elif not g2: cls=CLS_SOURCE
    elif not g3: cls=CLS_NEUTRAL
    elif not g4: cls=CLS_TANGENT
    elif g5 and g6: cls=CLS_COMMON
    elif g5 and (not g6) and g7: cls=CLS_SEP
    elif g5: cls=CLS_NORM
    else: cls=CLS_UNRES

    summary={"classification":cls,"causal_strict_count":strict_count,"resolved_separation_count":sep_count,
             "max_B30":float(max(r["B_30"] for r in rows)),
             "A_min":float(min(min(r["A_G"],r["A_L"]) for r in rows)),
             "A_max":float(max(max(r["A_G"],r["A_L"]) for r in rows)),
             "S_min":float(min(min(r["S_G_old_over_new"],r["S_L_old_over_new"]) for r in rows)),
             "S_max":float(max(max(r["S_G_old_over_new"],r["S_L_old_over_new"]) for r in rows))}
    out={"classification":cls,"diagnostic_complete":True,"predata_lock":PREDATA_LOCK,
         "r2d_parent_classification":r2dj.get("classification"),"source_audit":sa,
         "patch_neutrality":neutral,"cells":rows,"gates":gates,"summary":summary,
         "settings":{"anchors":ANCHORS,"tau_H0":10.0,"memory_order":20,"physical_eta":0.0,
                     "tol_perturbations_integration":3e-8,"lambda":[-30,-10,10,30],
                     "forcing":"frozen completed R2d full-history full-k tables"},
         "interpretation":{"historical_results_reclassified":False,
             "duplicate_hook_cause_certified":bool(g5),
             "absolute_single_hook_tangent_licensed":cls in (CLS_COMMON,CLS_SEP,CLS_NORM),
             "corrected_common_mode_licensed":cls==CLS_COMMON,
             "corrected_separation_licensed":cls==CLS_SEP,
             "observational_claim_licensed":False}}
    Path(args.json_out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    np.savez_compressed(args.npz_out,**arrays)
    print("STABLE_AEST_GROWTH_WEYL_MEMORY_R2E_GATES="+json.dumps(gates,sort_keys=True),flush=True)
    print("STABLE_AEST_GROWTH_WEYL_MEMORY_R2E_SUMMARY="+json.dumps(summary,sort_keys=True),flush=True)
    print("STABLE_AEST_GROWTH_WEYL_MEMORY_R2E_CLASSIFICATION="+cls,flush=True)
    return 0 if cls in (CLS_COMMON,CLS_SEP,CLS_NORM) else 1


if __name__ == "__main__":
    raise SystemExit(main())
