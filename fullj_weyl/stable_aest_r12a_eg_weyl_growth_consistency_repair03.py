#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import numpy as np
from scipy.interpolate import PchipInterpolator

ROOT = Path(__file__).resolve().parents[1]

from fullj_weyl import stable_aest_r12a_eg_weyl_growth_consistency as base
from fullj_weyl import stable_aest_observable_projection_r5b_derivative_zero as r5b
from fullj_weyl import stable_aest_desi_dr1_r9b_shapefit_projection as r9b

PREFIT_R03 = "de7511bed7fc984bf0ba40d1afc70a63de88ebb2"
POSTDATA_R02 = "472ab501cfe564510b38e1c2831c4024ae012ecf"
R8A2_POSTDATA = "590dbc69e2823f583b157af2297e357991103c47"
R10A_POSTDATA = "b7da648f1810ea0c047b6e511e3f87211e830329"
R11A_R02_POSTDATA = "84c4ba550ce3b262c78c69054056ab2778014677"

TAUS = (10.0, 5.0, 2.5, 1.25)
ETAS = (0.0, 0.025, -0.025, 0.05, -0.05)
EPS_PRIMARY = 0.025
EPS_CONTROL = 0.05
K_H = np.asarray([0.03, 0.05, 0.08, 0.10, 0.15, 0.20], float)
Z = np.asarray([
    0.29536404346937617,
    0.5096288678782911,
    0.7057956472488681,
    0.9185851971138159,
    1.3170658832980264,
    1.4905017757527006,
], float)
GRID_RTOL = 1.0e-10
NORM_GATE = 1.0e-12

GR_E_GATE = 0.05
ETA0_E_GATE = 0.02
ETA0_C_GATE = 0.999
ETA0_TAU_POINT_GATE = 5.0e-6
TAN_E_GATE = 0.05
TAN_C_GATE = 0.995
DECOMP_E_GATE = 0.02
DECOMP_C_GATE = 0.999
LINEARITY_E_GATE = 0.10
LINEARITY_C_GATE = 0.99

PASS = "STABLE_AEST_R12A_REPAIR03_DIRECT_TRANSFER_CERTIFIED"
FAIL_PROV = "STABLE_AEST_R12A_REPAIR03_PROVENANCE_SOURCE_FAIL"
FAIL_IFACE = "STABLE_AEST_R12A_REPAIR03_DIRECT_TRANSFER_INTERFACE_FAIL"
FAIL_GRID = "STABLE_AEST_R12A_REPAIR03_NATIVE_K_GRID_FAIL"
FAIL_GR = "STABLE_AEST_R12A_REPAIR03_GR_CONVENTION_FAIL"
FAIL_ETA0 = "STABLE_AEST_R12A_REPAIR03_ETA0_CLOSURE_FAIL"
FAIL_INTERP = "STABLE_AEST_R12A_REPAIR03_K_INTERPOLATION_CONTROL_FAIL"
FAIL_EPS = "STABLE_AEST_R12A_REPAIR03_EPSILON_CONSISTENCY_FAIL"
FAIL_DECOMP = "STABLE_AEST_R12A_REPAIR03_DIFFERENTIAL_DECOMPOSITION_FAIL"
FAIL_LINEAR = "STABLE_AEST_R12A_REPAIR03_LOCAL_LINEARITY_FAIL"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ancestor(sha: str) -> bool:
    return subprocess.run(["git", "merge-base", "--is-ancestor", sha, "HEAD"], cwd=ROOT,
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0


def metric(a, b) -> dict:
    aa=np.asarray(a,float).ravel(); bb=np.asarray(b,float).ravel()
    na=float(np.linalg.norm(aa)); nb=float(np.linalg.norm(bb))
    E=float(np.linalg.norm(aa-bb)/max(na,nb,1e-300))
    C=float(np.dot(aa,bb)/max(na*nb,1e-300))
    return {"E":E,"C":C,"norm_a":na,"norm_b":nb}


def tangent_pass(m: dict) -> bool:
    return bool(np.isfinite(m["E"]) and np.isfinite(m["C"]) and
                m["E"] <= TAN_E_GATE and m["C"] >= TAN_C_GATE and
                m["norm_a"] > NORM_GATE and m["norm_b"] > NORM_GATE)


def _h_from_params(p: dict) -> float:
    if "h" in p: return float(p["h"])
    if "H0" in p: return float(p["H0"])/100.0
    raise RuntimeError("parameter set has neither h nor H0")


def _build_params(eta: float, tau: float, pure_gr: bool) -> tuple[dict,int,int]:
    p,bits,pos=r5b.build_params(float(eta), base.TOL)
    p["output"]="mTk,vTk"
    p["lensing"]="no"
    p["P_k_max_h/Mpc"]=0.30
    p["z_max_pk"]=max(2.2,float(np.max(Z))+0.25)
    p["z_pk"] = ", ".join(f"{x:.17g}" for x in Z)
    p.pop("k_output_values",None)
    p.pop("non_linear",None); p.pop("l_max_scalars",None)
    p["aest_tau_H0"]=float(tau)
    if pure_gr:
        p["aest_enabled"]="no"; p["aest_memory_enabled"]="no"; p["aest_eta"]=0.0
    else:
        p["aest_enabled"]="yes"; p["aest_memory_enabled"]="yes"; p["aest_eta"]=float(eta)
    return p,int(bits),int(pos)


def _pick(d: dict, *names: str) -> str:
    for n in names:
        if n in d: return n
    raise RuntimeError(f"missing transfer field among {names}; keys={sorted(d.keys())}")


def _extract_transfer(tk: dict, h: float, H0: float, Hconf: float, fb: float, fc: float, z: float) -> dict:
    if not isinstance(tk, dict):
        raise RuntimeError(f"get_transfer returned {type(tk)!r}, expected dict")
    kk=_pick(tk,"k (h/Mpc)","k [h/Mpc]","k[h/Mpc]","k","k (1/Mpc)","k [1/Mpc]","k[1/Mpc]")
    k=np.asarray(tk[kk],float).ravel()
    if "1/Mpc" in kk and "h/Mpc" not in kk:
        k=k/float(h)
    pk=_pick(tk,"phi")
    sk=_pick(tk,"psi")
    dbk=_pick(tk,"d_b","delta_b")
    dck=_pick(tk,"d_cdm","delta_cdm")
    tbk=_pick(tk,"t_b","theta_b")
    tck=_pick(tk,"t_cdm","theta_cdm")
    phi=np.asarray(tk[pk],float).ravel(); psi=np.asarray(tk[sk],float).ravel()
    db=np.asarray(tk[dbk],float).ravel(); dc=np.asarray(tk[dck],float).ravel()
    tb=np.asarray(tk[tbk],float).ravel(); tc=np.asarray(tk[tck],float).ravel()
    n=len(k)
    if any(len(x)!=n for x in (phi,psi,db,dc,tb,tc)):
        raise RuntimeError("transfer arrays have inconsistent lengths")
    good=np.isfinite(k)&np.isfinite(phi)&np.isfinite(psi)&np.isfinite(db)&np.isfinite(dc)&np.isfinite(tb)&np.isfinite(tc)&(k>0)
    k=k[good]; phi=phi[good]; psi=psi[good]; db=db[good]; dc=dc[good]; tb=tb[good]; tc=tc[good]
    if k.size < 16: raise RuntimeError("insufficient finite direct-transfer k nodes")
    order=np.argsort(k); k=k[order]; phi=phi[order]; psi=psi[order]; db=db[order]; dc=dc[order]; tb=tb[order]; tc=tc[order]
    keep=np.ones(k.size,dtype=bool); keep[1:]=np.diff(k)>0
    k=k[keep]; phi=phi[keep]; psi=psi[keep]; db=db[keep]; dc=dc[keep]; tb=tb[keep]; tc=tc[keep]
    if k[0] >= K_H.min() or k[-1] <= K_H.max():
        raise RuntimeError(f"target k grid not strictly inside transfer support [{k[0]}, {k[-1]}]")
    W=phi+psi
    delta=fb*db+fc*dc
    theta=fb*tb+fc*tc
    fdelta=-theta/float(Hconf)
    fcb=fdelta/delta
    kmpc=k*float(h)
    EG=-(kmpc*kmpc)*W/(3.0*H0*H0*(1.0+float(z))*fdelta)
    for name,x in (("W",W),("delta_cb",delta),("theta_cb",theta),("fdelta",fdelta),("fcb",fcb),("EG",EG)):
        if not np.all(np.isfinite(x)): raise RuntimeError(f"nonfinite derived direct-transfer field {name}")
    if np.any(np.abs(W)<=1e-300) or np.any(np.abs(fdelta)<=1e-300) or np.any(np.abs(delta)<=1e-300) or np.any(np.abs(EG)<=1e-300):
        raise RuntimeError("zero denominator in direct-transfer derived fields")
    return {"k":k,"W":W,"delta_cb":delta,"theta_cb":theta,"fdelta":fdelta,"fcb":fcb,"EG":EG,
            "keys":{"k":kk,"phi":pk,"psi":sk,"db":dbk,"dc":dck,"tb":tbk,"tc":tck}}


def run_case(eta: float, tau: float, pure_gr: bool) -> dict:
    from classy import Class
    p,bits,pos=_build_params(eta,tau,pure_gr)
    c=Class(); c.set(p); c.compute()
    try:
        h=float(c.h()); hreq=_h_from_params(p)
        if not np.isclose(h,hreq,rtol=1e-12,atol=1e-14): raise RuntimeError("CLASS h mismatch")
        ob=r9b._omega(c,"Omega_b"); oc=r9b._omega(c,"Omega_cdm"); onu=r9b._omega(c,"Omega_nu",0.0)
        try: om=float(c.Omega_m())
        except Exception: om=float(ob+oc+onu)
        if not (ob>0 and oc>0 and om>0): raise RuntimeError("invalid matter fractions")
        fb=float(ob/(ob+oc)); fc=float(oc/(ob+oc)); H0=float(c.Hubble(0.0))
        rows=[]
        if not hasattr(c,"get_transfer"): raise RuntimeError("frozen classy has no get_transfer method")
        for z in Z:
            Hconf=float(c.Hubble(float(z)))/(1.0+float(z))
            try:
                tk=c.get_transfer(float(z), output_format="class")
            except TypeError:
                tk=c.get_transfer(float(z))
            row=_extract_transfer(tk,h,H0,Hconf,fb,fc,float(z)); row["z"]=float(z); row["Hconf"]=Hconf
            rows.append(row)
        return {"pure_gr":bool(pure_gr),"tau_H0":float(tau),"eta":float(eta),"bits":bits,"target_pos":pos,
                "h":h,"H0":H0,"Omega_b":float(ob),"Omega_cdm":float(oc),"Omega_nu":float(onu),"Omega_m":float(om),
                "fb":fb,"fc":fc,"rows":rows}
    finally:
        c.struct_cleanup(); c.empty()


def _case_name(pure: bool,tau: float,eta: float) -> str:
    if pure: return "gr"
    s=(f"tau{tau:g}_eta{eta:+.3f}").replace("+","p").replace("-","m")
    return s


def save_case(path: Path, v: dict) -> None:
    path.parent.mkdir(parents=True,exist_ok=True)
    a={"schema":np.asarray([3]),"pure_gr":np.asarray([int(v["pure_gr"])]),"tau":np.asarray([v["tau_H0"]]),"eta":np.asarray([v["eta"]]),
       "h":np.asarray([v["h"]]),"H0":np.asarray([v["H0"]]),"Omega_b":np.asarray([v["Omega_b"]]),"Omega_cdm":np.asarray([v["Omega_cdm"]]),
       "Omega_nu":np.asarray([v["Omega_nu"]]),"Omega_m":np.asarray([v["Omega_m"]]),"fb":np.asarray([v["fb"]]),"fc":np.asarray([v["fc"]]),
       "bits":np.asarray([v["bits"]]),"target_pos":np.asarray([v["target_pos"]])}
    for iz,r in enumerate(v["rows"]):
        a[f"z{iz}_z"]=np.asarray([r["z"]]); a[f"z{iz}_Hconf"]=np.asarray([r["Hconf"]]); a[f"z{iz}_k"]=r["k"]
        for f in ("W","delta_cb","theta_cb","fdelta","fcb","EG"): a[f"z{iz}_{f}"]=r[f]
    np.savez_compressed(path,**a)


def load_case(path: Path,pure: bool,tau: float,eta: float) -> dict:
    q=np.load(path)
    if int(q["schema"][0])!=3: raise RuntimeError("schema mismatch")
    if bool(int(q["pure_gr"][0]))!=bool(pure): raise RuntimeError("pure_gr mismatch")
    if not np.isclose(float(q["tau"][0]),tau,rtol=0,atol=1e-14) or not np.isclose(float(q["eta"][0]),eta,rtol=0,atol=1e-14): raise RuntimeError("case key mismatch")
    rows=[]
    for iz,z in enumerate(Z):
        if not np.isclose(float(q[f"z{iz}_z"][0]),z,rtol=0,atol=1e-14): raise RuntimeError("z mismatch")
        r={"z":float(z),"Hconf":float(q[f"z{iz}_Hconf"][0]),"k":np.asarray(q[f"z{iz}_k"],float)}
        for f in ("W","delta_cb","theta_cb","fdelta","fcb","EG"): r[f]=np.asarray(q[f"z{iz}_{f}"],float)
        rows.append(r)
    return {"pure_gr":bool(pure),"tau_H0":float(tau),"eta":float(eta),"h":float(q["h"][0]),"H0":float(q["H0"][0]),
            "Omega_b":float(q["Omega_b"][0]),"Omega_cdm":float(q["Omega_cdm"][0]),"Omega_nu":float(q["Omega_nu"][0]),"Omega_m":float(q["Omega_m"][0]),
            "fb":float(q["fb"][0]),"fc":float(q["fc"][0]),"bits":int(q["bits"][0]),"target_pos":int(q["target_pos"][0]),"rows":rows}


def interp_response(k,y,method):
    k=np.asarray(k,float); y=np.asarray(y,float); x=np.log(k); xt=np.log(K_H)
    if K_H.min()<=k.min() or K_H.max()>=k.max(): raise RuntimeError("target k outside strict native support")
    if method=="pchip": out=PchipInterpolator(x,y,extrapolate=False)(xt)
    elif method=="linear": out=np.interp(xt,x,y)
    else: raise ValueError(method)
    out=np.asarray(out,float)
    if not np.all(np.isfinite(out)): raise RuntimeError("nonfinite k interpolation")
    return out


def grid_match(cases: dict) -> tuple[bool,float]:
    maxrel=0.0
    for tau in TAUS:
        for iz in range(len(Z)):
            ref=cases[(tau,0.0)]["rows"][iz]["k"]
            for eta in ETAS[1:]:
                k=cases[(tau,eta)]["rows"][iz]["k"]
                if k.shape!=ref.shape: return False,float("inf")
                rel=float(np.max(np.abs(k-ref)/np.maximum(np.maximum(np.abs(k),np.abs(ref)),1e-300)))
                maxrel=max(maxrel,rel)
                if rel>GRID_RTOL: return False,maxrel
    return True,maxrel


def build_target(cases: dict, tau: float, eps: float, field: str, method: str) -> np.ndarray:
    vals=[]
    for iz in range(len(Z)):
        c0=cases[(tau,0.0)]["rows"][iz]; cp=cases[(tau,+eps)]["rows"][iz]; cm=cases[(tau,-eps)]["rows"][iz]
        k=c0["k"]
        T=(cp[field]-cm[field])/(2.0*eps*c0[field])
        if not np.all(np.isfinite(T)): raise RuntimeError(f"nonfinite tangent {field}")
        vals.append(interp_response(k,T,method))
    return np.asarray(vals,float)


def build_baseline(case: dict, field: str, method: str) -> np.ndarray:
    return np.asarray([interp_response(r["k"],r[field],method) for r in case["rows"]],float)


def build_direct_shift(cases: dict,tau: float,method: str) -> np.ndarray:
    vals=[]
    for iz in range(len(Z)):
        c0=cases[(tau,0.0)]["rows"][iz]; cp=cases[(tau,0.05)]["rows"][iz]
        d=cp["EG"]/c0["EG"]-1.0
        vals.append(interp_response(c0["k"],d,method))
    return np.asarray(vals,float)


def write_json(path: Path,obj: dict):
    path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n")


def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--workdir",default="results/stable_aest_r12a_eg_work_repair03")
    ap.add_argument("--json-out",default="results/stable_aest_r12a_eg_weyl_growth_consistency_repair03.json")
    ap.add_argument("--npz-out",default="results/stable_aest_r12a_eg_weyl_growth_consistency_repair03.npz")
    args=ap.parse_args(); work=Path(args.workdir); work.mkdir(parents=True,exist_ok=True); jout=Path(args.json_out)

    locks=[PREFIT_R03,POSTDATA_R02,R8A2_POSTDATA,R10A_POSTDATA,R11A_R02_POSTDATA]
    g1=all(ancestor(x) for x in locks)
    if not g1:
        out={"classification":FAIL_PROV,"diagnostic_complete":True,"science_evaluated":False,"gates":{"G1_provenance":False}}
        write_json(jout,out); print("STABLE_AEST_R12A_R03_CLASSIFICATION="+FAIL_PROV); return 1

    specs=[("gr",True,10.0,0.0)]+[( _case_name(False,t,e),False,t,e) for t in TAUS for e in ETAS]
    cases={}; runs=[]
    print("STABLE_AEST_R12A_R03_START",flush=True)
    try:
        for name,pure,tau,eta in specs:
            p=work/f"{name}.npz"; reused=False
            if p.is_file():
                try: v=load_case(p,pure,tau,eta); reused=True
                except Exception: p.unlink(missing_ok=True); v=run_case(eta,tau,pure); save_case(p,v)
            else:
                v=run_case(eta,tau,pure); save_case(p,v)
            cases["gr" if pure else (tau,eta)]=v; runs.append({"name":name,"reused":reused,"pass":True})
            print(f"STABLE_AEST_R12A_R03_CASE name={name} reused={int(reused)}",flush=True)
    except Exception as exc:
        out={"classification":FAIL_IFACE,"diagnostic_complete":True,"science_evaluated":False,"gates":{"G1_provenance":True,"G2_direct_transfer_interface":False},"error":repr(exc),"runs":runs}
        write_json(jout,out); print(f"STABLE_AEST_R12A_R03_INTERFACE_FAIL error={exc!r}"); print("STABLE_AEST_R12A_R03_CLASSIFICATION="+FAIL_IFACE); return 1

    ggrid,maxgrid=grid_match(cases)
    if not ggrid:
        out={"classification":FAIL_GRID,"diagnostic_complete":True,"science_evaluated":False,"gates":{"G1_provenance":True,"G2_direct_transfer_interface":True,"G3_native_k_grid":False},"native_k_max_relative_difference":maxgrid,"runs":runs}
        write_json(jout,out); print("STABLE_AEST_R12A_R03_CLASSIFICATION="+FAIL_GRID); return 1

    methods=("pchip","linear")
    grctrl={}; eta0={}; tau0={}; tang={}; robust={"interpolation":{},"epsilon":{},"decomposition":{},"linearity":{}}
    try:
        for m in methods:
            eg=build_baseline(cases["gr"],"EG",m); fcb=build_baseline(cases["gr"],"fcb",m)
            ref=cases["gr"]["Omega_m"]/fcb
            mm=metric(eg,ref); mm["all_EG_positive"]=bool(np.all(eg>0)); mm["EG_min"]=float(np.min(eg)); mm["EG_max"]=float(np.max(eg)); mm["pass"]=bool(mm["E"]<=GR_E_GATE and mm["all_EG_positive"])
            grctrl[m]=mm
            eta0[m]={}
            ref0=eg
            for tau in TAUS:
                a0=build_baseline(cases[(tau,0.0)],"EG",m); q=metric(a0,ref0); q["pass"]=bool(q["E"]<=ETA0_E_GATE and q["C"]>=ETA0_C_GATE); eta0[m][str(tau)]=q
            base10=build_baseline(cases[(10.0,0.0)],"EG",m)
            tau0[m]={str(t):float(np.max(np.abs(build_baseline(cases[(t,0.0)],"EG",m)-base10)/np.maximum(np.maximum(np.abs(base10),np.abs(build_baseline(cases[(t,0.0)],"EG",m))),1e-300))) for t in TAUS}
        for tau in TAUS:
            robust["interpolation"][str(tau)]={}; robust["epsilon"][str(tau)]={}; robust["decomposition"][str(tau)]={}
            for eps in (EPS_PRIMARY,EPS_CONTROL):
                for m in methods:
                    for f in ("W","fdelta","EG"): tang[(tau,eps,m,f)]=build_target(cases,tau,eps,f,m)
                q=metric(tang[(tau,eps,"pchip","EG")],tang[(tau,eps,"linear","EG")]); q["pass"]=tangent_pass(q); robust["interpolation"][str(tau)][str(eps)]=q
            for m in methods:
                q=metric(tang[(tau,EPS_PRIMARY,m,"EG")],tang[(tau,EPS_CONTROL,m,"EG")]); q["pass"]=tangent_pass(q); robust["epsilon"][str(tau)][m]=q
                rhs=tang[(tau,EPS_PRIMARY,m,"W")]-tang[(tau,EPS_PRIMARY,m,"fdelta")]
                q=metric(tang[(tau,EPS_PRIMARY,m,"EG")],rhs); q["pass"]=bool(q["E"]<=DECOMP_E_GATE and q["C"]>=DECOMP_C_GATE); robust["decomposition"][str(tau)][m]=q
            direct=build_direct_shift(cases,tau,"pchip"); pred=0.05*tang[(tau,EPS_PRIMARY,"pchip","EG")]
            q=metric(direct,pred); q["pass"]=bool(q["E"]<=LINEARITY_E_GATE and q["C"]>=LINEARITY_C_GATE); robust["linearity"][str(tau)]=q
    except Exception as exc:
        out={"classification":FAIL_IFACE,"diagnostic_complete":True,"science_evaluated":False,"gates":{"G1_provenance":True,"G2_direct_transfer_interface":False,"G3_native_k_grid":True},"error":repr(exc)}
        write_json(jout,out); print(f"STABLE_AEST_R12A_R03_ANALYSIS_FAIL error={exc!r}"); return 1

    g4=all(x["pass"] for x in grctrl.values())
    g5=all(q["pass"] for d in eta0.values() for q in d.values()) and all(v<=ETA0_TAU_POINT_GATE for d in tau0.values() for v in d.values())
    g6=all(q["pass"] for d in robust["interpolation"].values() for q in d.values())
    g7=all(q["pass"] for d in robust["epsilon"].values() for q in d.values())
    g8=all(q["pass"] for d in robust["decomposition"].values() for q in d.values())
    g9=all(q["pass"] for q in robust["linearity"].values())
    gates={"G1_provenance":True,"G2_direct_transfer_interface":True,"G3_native_k_grid":True,"G4_GR_convention":g4,"G5_eta0_closure_tau_invariance":g5,"G6_k_interpolation_control":g6,"G7_epsilon_consistency":g7,"G8_differential_decomposition":g8,"G9_local_eta005_linearity":g9}
    if not g4: cls=FAIL_GR
    elif not g5: cls=FAIL_ETA0
    elif not g6: cls=FAIL_INTERP
    elif not g7: cls=FAIL_EPS
    elif not g8: cls=FAIL_DECOMP
    elif not g9: cls=FAIL_LINEAR
    else: cls=PASS

    science={}; taucoh={}
    if all(gates.values()):
        ref=tang[(10.0,EPS_PRIMARY,"pchip","EG")]
        for tau in TAUS:
            T=tang[(tau,EPS_PRIMARY,"pchip","EG")]; direct=build_direct_shift(cases,tau,"pchip"); TW=tang[(tau,EPS_PRIMARY,"pchip","W")]; TF=tang[(tau,EPS_PRIMARY,"pchip","fdelta")]
            idx=np.unravel_index(np.argmax(np.abs(direct)),direct.shape)
            science[str(tau)]={"tangent_norm":float(np.linalg.norm(T)),"physical_eta005_l2_fractional_shift":float(np.linalg.norm(direct)),"physical_eta005_max_abs_fractional_shift":float(np.max(np.abs(direct))),"physical_eta005_rms_fractional_shift":float(np.sqrt(np.mean(direct**2))),"max_location":{"z":float(Z[idx[0]]),"k_h_Mpc":float(K_H[idx[1]])},"A_ratio":float(np.linalg.norm(T)/max(np.linalg.norm(TW),np.linalg.norm(TF),1e-300))}
            taucoh[str(tau)]={"norm_ratio_to_tau10":float(np.linalg.norm(T)/np.linalg.norm(ref)),"cosine_to_tau10":float(np.dot(T.ravel(),ref.ravel())/(np.linalg.norm(T)*np.linalg.norm(ref)))}
    out={"classification":cls,"diagnostic_complete":True,"science_evaluated":bool(cls==PASS),"gates":gates,"settings":{"tau_H0":TAUS,"eta_values":ETAS,"epsilon_primary":EPS_PRIMARY,"epsilon_control":EPS_CONTROL,"k_h_Mpc":K_H.tolist(),"z":Z.tolist(),"time_interpolation_used":False,"primary_k_interpolation":"PCHIP in ln k after response formation","control_k_interpolation":"linear in ln k after response formation","EG_definition":"-k_phys^2(phi+psi)/(3 H0^2 (1+z) fdelta_cb)","fdelta_cb_definition":"-theta_cb/Hconf"},"native_k_max_relative_difference":maxgrid,"GR_control":grctrl,"eta0_closure":eta0,"eta0_tau_max_point_relative":tau0,"robustness":robust,"science":science,"tau_coherence":taucoh,"claim_scope":{"transfer_level_EG_response":bool(cls==PASS),"observational_EG_detection":False,"cross_correlation_likelihood":False,"eta_bound":False,"tau_bound":False,"nonlinear_claim":False,"galaxy_bias_cancellation_claim":False},"provenance":{"repair03_prefit_lock":PREFIT_R03,"repair02_postdata_lock":POSTDATA_R02,"r8a2":R8A2_POSTDATA,"r10a":R10A_POSTDATA,"r11a_r02":R11A_R02_POSTDATA}}
    write_json(jout,out)
    arrays={"k_h_Mpc":K_H,"z":Z,"EG_GR_pchip":build_baseline(cases["gr"],"EG","pchip")}
    if cls==PASS:
        for tau in TAUS:
            arrays[f"T_EG_tau{tau:g}"]=tang[(tau,EPS_PRIMARY,"pchip","EG")]; arrays[f"D_EG005_tau{tau:g}"]=build_direct_shift(cases,tau,"pchip")
    np.savez_compressed(args.npz_out,**arrays)
    print("STABLE_AEST_R12A_R03_GATES="+json.dumps(gates,sort_keys=True),flush=True)
    print("STABLE_AEST_R12A_R03_GR="+json.dumps(grctrl,sort_keys=True),flush=True)
    print("STABLE_AEST_R12A_R03_ROBUSTNESS="+json.dumps(robust,sort_keys=True),flush=True)
    if science: print("STABLE_AEST_R12A_R03_SCIENCE="+json.dumps(science,sort_keys=True),flush=True)
    print("STABLE_AEST_R12A_R03_CLASSIFICATION="+cls,flush=True)
    return 0 if cls==PASS else 1


if __name__=="__main__":
    raise SystemExit(main())
