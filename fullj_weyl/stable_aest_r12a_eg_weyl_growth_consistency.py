#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
from scipy.interpolate import CubicSpline, PchipInterpolator

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fullj_weyl import stable_aest_observable_projection_r5b_derivative_zero as r5b
from fullj_weyl import stable_aest_cosmic_memory_r8a_tau_amplitude_scan as r8a
from fullj_weyl import stable_aest_desi_dr1_r9b_shapefit_projection as r9b
from nl1c6d2a import baryon_matter_sector_audit as d2a

PREFIT_LOCK = "bb69d8ac1d83228ba879316c61141823c3e5c665"
R8A2_POSTDATA_LOCK = "590dbc69e2823f583b157af2297e357991103c47"
R10A_POSTDATA_LOCK = "b7da648f1810ea0c047b6e511e3f87211e830329"
R11A_R02_POSTDATA_LOCK = "d9e2e0e6da65126a81d02f32e65f83410bc8cc7c"

R8A2_JSON = ROOT / "results/stable_aest_cosmic_memory_r8a2_precision_qualified_tau_scan.json"
R8A2_NPZ = ROOT / "results/stable_aest_cosmic_memory_r8a2_precision_qualified_tau_scan.npz"
R11A_R02_JSON = ROOT / "results/stable_aest_ksz_r11a_dense_resolution_repair02.json"
R8A2_JSON_SHA256 = "2d6289c2fbd37bebcb904dade89f64c15a009e5c7454754b39d4dcc72924ca66"
R8A2_NPZ_SHA256 = "c81b2093a88719423e87ff5c180d790a56da6f396c0070858624879c90f26ee1"
R11A_R02_JSON_SHA256 = "f5166409be08edc93e739b2b901bd183a2a588325eb6c71eb0ad0e8a82d2b4a1"
R8A2_CLASS = "STABLE_AEST_COSMIC_MEMORY_R8A2_TAU_GENERALITY_CERTIFIED"
R11A_R02_CLASS = "STABLE_AEST_KSZ_R11A_REPAIR02_DENSE_RESOLUTION_CERTIFIED"

TAUS = (10.0, 5.0, 2.5, 1.25)
ETAS = (0.0, 0.025, -0.025, 0.05, -0.05)
EPS_PRIMARY = 0.025
EPS_CONTROL = 0.05
TOL = 3.0e-8
K_H = np.asarray([0.03, 0.05, 0.08, 0.10, 0.15, 0.20], float)
Z = np.asarray([
    0.29536404346937617,
    0.5096288678782911,
    0.7057956472488681,
    0.9185851971138159,
    1.3170658832980264,
    1.4905017757527006,
], float)
K_MATCH = 5.0e-12
NORM_GATE = 1.0e-12

GR_ID_E_GATE = 0.05
ETA0_E_GATE = 0.02
ETA0_C_GATE = 0.999
ETA0_TAU_POINT_GATE = 5.0e-6
TAN_E_GATE = 0.05
TAN_C_GATE = 0.995
DECOMP_E_GATE = 0.02
DECOMP_C_GATE = 0.999
LINEARITY_E_GATE = 0.10
LINEARITY_C_GATE = 0.99

CLS_PASS = "STABLE_AEST_R12A_EG_WEYL_GROWTH_CONSISTENCY_CERTIFIED"
CLS_PROV = "STABLE_AEST_R12A_PROVENANCE_SOURCE_FAIL"
CLS_COVER = "STABLE_AEST_R12A_MODE_HISTORY_COVERAGE_FAIL"
CLS_GR = "STABLE_AEST_R12A_GR_CONVENTION_FAIL"
CLS_ETA0 = "STABLE_AEST_R12A_ETA0_CLOSURE_FAIL"
CLS_INTERP = "STABLE_AEST_R12A_INTERPOLATION_CONTROL_FAIL"
CLS_EPS = "STABLE_AEST_R12A_EPSILON_CONSISTENCY_FAIL"
CLS_DECOMP = "STABLE_AEST_R12A_DIFFERENTIAL_DECOMPOSITION_FAIL"
CLS_LINEAR = "STABLE_AEST_R12A_LOCAL_LINEARITY_FAIL"
CLS_RUN = "STABLE_AEST_R12A_RUN_FAIL"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"], cwd=ROOT,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    ).returncode == 0


def metric(a, b) -> dict:
    aa = np.asarray(a, float).ravel(); bb = np.asarray(b, float).ravel()
    na = float(np.linalg.norm(aa)); nb = float(np.linalg.norm(bb))
    E = float(np.linalg.norm(aa-bb) / max(na, nb, 1e-300))
    C = float(np.dot(aa, bb) / max(na*nb, 1e-300))
    return {"E": E, "C": C, "norm_a": na, "norm_b": nb}


def tangent_pass(m: dict) -> bool:
    return bool(
        np.isfinite(m["E"]) and np.isfinite(m["C"])
        and m["E"] <= TAN_E_GATE and m["C"] >= TAN_C_GATE
        and m["norm_a"] > NORM_GATE and m["norm_b"] > NORM_GATE
    )


def _point_rel(a, b) -> float:
    aa=np.asarray(a,float); bb=np.asarray(b,float)
    return float(np.max(np.abs(aa-bb)/np.maximum(np.maximum(np.abs(aa),np.abs(bb)),1e-300)))


def _write(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True)+"\n")


def _h_from_params(p: dict) -> float:
    if "h" in p:
        return float(p["h"])
    if "H0" in p:
        return float(p["H0"])/100.0
    raise RuntimeError("parameter set has neither h nor H0")


def _build_params(eta: float, tau: float, pure_gr: bool) -> tuple[dict, int, int]:
    p,bits,pos=r5b.build_params(float(eta), TOL)
    h=_h_from_params(p)
    p["output"]="mTk,vTk"
    p["lensing"]="no"
    p["z_max_pk"]=max(2.2,float(np.max(Z))+0.25)
    p["P_k_max_h/Mpc"]=0.30
    p["k_output_values"] = ", ".join(f"{x*h:.17g}" for x in K_H)
    p["aest_tau_H0"]=float(tau)
    p.pop("non_linear",None); p.pop("l_max_scalars",None)
    if pure_gr:
        p["aest_enabled"]="no"
        p["aest_memory_enabled"]="no"
        p["aest_eta"]=0.0
    else:
        p["aest_enabled"]="yes"
        p["aest_memory_enabled"]="yes"
        p["aest_eta"]=float(eta)
    return p,int(bits),int(pos)


def _reported_kh(raw: dict, h: float) -> tuple[float,str]:
    candidates=(
        ("k (h/Mpc)",1.0),("k [h/Mpc]",1.0),("k[h/Mpc]",1.0),
        ("k (1/Mpc)",1.0/h),("k [1/Mpc]",1.0/h),("k[1/Mpc]",1.0/h),
    )
    for key,factor in candidates:
        if key in raw:
            q=np.asarray(raw[key],float).ravel(); q=q[np.isfinite(q)]
            if q.size==0: continue
            if np.max(np.abs(q-q[0])) > 1e-10*max(abs(float(q[0])),1.0):
                raise RuntimeError(f"history {key} is not constant")
            return float(q[0])*factor,key
    raise RuntimeError(f"history has no recognized k key: {sorted(raw.keys())}")


def _clean_xy(x,y):
    x=np.asarray(x,float); y=np.asarray(y,float)
    order=np.argsort(x); x=x[order]; y=y[order]
    good=np.isfinite(x)&np.isfinite(y); x=x[good]; y=y[good]
    keep=np.ones(x.size,dtype=bool)
    if x.size>1: keep[1:]=np.diff(x)>0
    x=x[keep]; y=y[keep]
    if x.size<8 or np.any(np.diff(x)<=0):
        raise RuntimeError("insufficient/nonmonotone history samples")
    return x,y


def _eval_field(raw: dict, key: str, method: str) -> np.ndarray:
    akey=d2a.pick(raw,"a",("scale factor",))
    aa,yy=_clean_xy(raw[akey],raw[key])
    at=1.0/(1.0+Z)
    if float(np.min(at)) < float(aa[0])-1e-12 or float(np.max(at)) > float(aa[-1])+1e-12:
        raise RuntimeError(f"history {key} does not cover frozen z grid")
    if method=="cubic":
        out=CubicSpline(aa,yy,bc_type="not-a-knot")(at)
    elif method=="pchip":
        out=PchipInterpolator(aa,yy,extrapolate=False)(at)
    else:
        raise ValueError(method)
    out=np.asarray(out,float)
    if not np.all(np.isfinite(out)):
        raise RuntimeError(f"nonfinite {method} interpolation for {key}")
    return out


def _fields_for_mode(raw: dict, method: str, fb: float, fc: float, Hconf: np.ndarray,
                     kh: float, h: float, H0: float) -> dict:
    pk=d2a.pick(raw,"phi")
    sk=d2a.pick(raw,"psi")
    dbk=d2a.pick(raw,"delta_b",("d_b",))
    tbk=d2a.pick(raw,"theta_b",("t_b",))
    dck=d2a.pick(raw,"delta_cdm",("d_cdm",))
    tck=d2a.pick(raw,"theta_cdm",("t_cdm",))
    phi=_eval_field(raw,pk,method); psi=_eval_field(raw,sk,method)
    db=_eval_field(raw,dbk,method); tb=_eval_field(raw,tbk,method)
    dc=_eval_field(raw,dck,method); tc=_eval_field(raw,tck,method)
    W=phi+psi
    delta=fb*db+fc*dc
    theta=fb*tb+fc*tc
    fdelta=-theta/Hconf
    fcb=fdelta/delta
    kmpc=float(kh)*float(h)
    EG=-(kmpc*kmpc)*W/(3.0*H0*H0*(1.0+Z)*fdelta)
    vals=(W,delta,theta,fdelta,fcb,EG)
    if any(not np.all(np.isfinite(x)) for x in vals):
        raise RuntimeError("nonfinite derived transfer field")
    if np.any(np.abs(fdelta)<=1e-300) or np.any(np.abs(delta)<=1e-300) or np.any(np.abs(EG)<=1e-300):
        raise RuntimeError("zero derived transfer denominator")
    return {"W":W,"delta_cb":delta,"theta_cb":theta,"fdelta":fdelta,"fcb":fcb,"EG":EG}


def run_case(eta: float, tau: float, pure_gr: bool) -> dict:
    from classy import Class
    p,bits,pos=_build_params(eta,tau,pure_gr)
    c=Class(); c.set(p); c.compute()
    try:
        h=float(c.h()); hp=_h_from_params(p)
        if abs(h-hp)>1e-12*max(abs(h),1.0):
            raise RuntimeError("CLASS h differs from requested h")
        ob=r9b._omega(c,"Omega_b"); oc=r9b._omega(c,"Omega_cdm")
        onu=r9b._omega(c,"Omega_nu",0.0)
        try: om=float(c.Omega_m())
        except Exception: om=float(ob+oc+onu)
        if not (ob>0 and oc>0 and om>0):
            raise RuntimeError("invalid matter density fractions")
        fb=ob/(ob+oc); fc=oc/(ob+oc)
        H0=float(c.Hubble(0.0)); Hconf=np.asarray([float(c.Hubble(float(z)))/(1.0+float(z)) for z in Z],float)
        if not (np.isfinite(H0) and H0>0 and np.all(np.isfinite(Hconf)) and np.all(Hconf>0)):
            raise RuntimeError("invalid Hubble values")
        pert=c.get_perturbations(); histories,_=d2a.scalar_histories(pert)
        rows=[]; used=set(); maxerr=0.0
        for target in K_H:
            candidates=[]
            for ih,raw in enumerate(histories):
                kh,key=_reported_kh(raw,h)
                candidates.append((abs(kh-float(target)),ih,kh,key))
            candidates.sort(key=lambda x:x[0]); err,ih,kh,key=candidates[0]
            if err>K_MATCH or ih in used:
                raise RuntimeError(f"no unique history for k={target}; best err={err}")
            used.add(ih); maxerr=max(maxerr,float(err)); raw=histories[ih]
            out={"requested_k_h_Mpc":float(target),"reported_k_h_Mpc":float(kh),"reported_k_key":key}
            for method in ("cubic","pchip"):
                out[method]=_fields_for_mode(raw,method,fb,fc,Hconf,kh,h,H0)
            rows.append(out)
        if len(used)!=len(K_H):
            raise RuntimeError("returned history mapping is not one-to-one")
        return {
            "pure_gr":bool(pure_gr),"tau_H0":float(tau),"eta":float(eta),
            "bits":bits,"target_pos":pos,"h":h,"H0_Mpc_inv":H0,
            "Omega_b":float(ob),"Omega_cdm":float(oc),"Omega_nu":float(onu),"Omega_m":float(om),
            "fb":float(fb),"fc":float(fc),"max_k_match_error_h_Mpc":float(maxerr),"rows":rows,
        }
    finally:
        c.struct_cleanup(); c.empty()


def _save_case(path: Path, v: dict) -> None:
    arrays={
        "schema":np.asarray([1]),"pure_gr":np.asarray([int(v["pure_gr"])]),
        "tau_H0":np.asarray([v["tau_H0"]]),"eta":np.asarray([v["eta"]]),
        "h":np.asarray([v["h"]]),"H0_Mpc_inv":np.asarray([v["H0_Mpc_inv"]]),
        "Omega_m":np.asarray([v["Omega_m"]]),"Omega_b":np.asarray([v["Omega_b"]]),
        "Omega_cdm":np.asarray([v["Omega_cdm"]]),"Omega_nu":np.asarray([v["Omega_nu"]]),
        "fb":np.asarray([v["fb"]]),"fc":np.asarray([v["fc"]]),
        "max_k_match_error_h_Mpc":np.asarray([v["max_k_match_error_h_Mpc"]]),
        "k_h_Mpc":K_H,"z":Z,
    }
    for method in ("cubic","pchip"):
        for field in ("W","delta_cb","theta_cb","fdelta","fcb","EG"):
            arrays[f"{method}_{field}"]=np.stack([r[method][field] for r in v["rows"]],axis=0)
    np.savez_compressed(path,**arrays)


def _load_case(path: Path, pure_gr: bool, tau: float, eta: float) -> dict:
    q=np.load(path)
    if int(q["schema"][0])!=1 or bool(int(q["pure_gr"][0]))!=bool(pure_gr): raise RuntimeError("checkpoint schema/mode mismatch")
    if abs(float(q["tau_H0"][0])-float(tau))>1e-13 or abs(float(q["eta"][0])-float(eta))>1e-13: raise RuntimeError("checkpoint parameter mismatch")
    if not np.array_equal(np.asarray(q["k_h_Mpc"],float),K_H) or not np.array_equal(np.asarray(q["z"],float),Z): raise RuntimeError("checkpoint grid mismatch")
    out={"pure_gr":pure_gr,"tau_H0":tau,"eta":eta,"h":float(q["h"][0]),"H0_Mpc_inv":float(q["H0_Mpc_inv"][0]),"Omega_m":float(q["Omega_m"][0]),"max_k_match_error_h_Mpc":float(q["max_k_match_error_h_Mpc"][0])}
    for method in ("cubic","pchip"):
        out[method]={field:np.asarray(q[f"{method}_{field}"],float) for field in ("W","delta_cb","theta_cb","fdelta","fcb","EG")}
        if any(a.shape!=(len(K_H),len(Z)) or not np.all(np.isfinite(a)) for a in out[method].values()): raise RuntimeError("invalid checkpoint field array")
    return out


def _key(tau: float, eta: float) -> str:
    return f"tau{tau:g}_eta{eta:+.3f}"


def _central(vals: dict, tau: float, eps: float, method: str, field: str) -> np.ndarray:
    z=vals[_key(tau,0.0)][method][field]
    p=vals[_key(tau,+eps)][method][field]
    m=vals[_key(tau,-eps)][method][field]
    if np.any(np.abs(z)<=1e-300): raise RuntimeError(f"zero baseline {field}")
    return (p-m)/(2.0*eps*z)


def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--worker",action="store_true")
    ap.add_argument("--pure-gr",action="store_true")
    ap.add_argument("--tau",type=float,default=10.0)
    ap.add_argument("--eta",type=float,default=0.0)
    ap.add_argument("--out")
    ap.add_argument("--workdir",default="results/stable_aest_r12a_eg_work")
    ap.add_argument("--json-out",default="results/stable_aest_r12a_eg_weyl_growth_consistency.json")
    ap.add_argument("--npz-out",default="results/stable_aest_r12a_eg_weyl_growth_consistency.npz")
    args=ap.parse_args()
    if args.worker:
        if not args.out: raise SystemExit("worker requires --out")
        v=run_case(float(args.eta),float(args.tau),bool(args.pure_gr)); _save_case(Path(args.out),v)
        print(json.dumps({"pure_gr":bool(args.pure_gr),"tau_H0":float(args.tau),"eta":float(args.eta),"max_k_error":v["max_k_match_error_h_Mpc"]},sort_keys=True),flush=True)
        return 0

    print("STABLE_AEST_R12A_START",flush=True)
    prov={}; g1=False
    try:
        r8j=json.loads(R8A2_JSON.read_text()); r11j=json.loads(R11A_R02_JSON.read_text())
        locks=(PREFIT_LOCK,R8A2_POSTDATA_LOCK,R10A_POSTDATA_LOCK,R11A_R02_POSTDATA_LOCK)
        source_ok,source_meta=r8a.source_topology()
        prov={
            "ancestor_locks":{x:ancestor(x) for x in locks},"source_topology":source_meta,
            "r8a2_json_sha256":sha256(R8A2_JSON),"r8a2_npz_sha256":sha256(R8A2_NPZ),
            "r8a2_classification":r8j.get("classification"),"r11a_r02_json_sha256":sha256(R11A_R02_JSON),
            "r11a_r02_classification":r11j.get("classification"),
        }
        g1=bool(all(prov["ancestor_locks"].values()) and source_ok
                and prov["r8a2_json_sha256"]==R8A2_JSON_SHA256 and prov["r8a2_npz_sha256"]==R8A2_NPZ_SHA256
                and r8j.get("classification")==R8A2_CLASS and r8j.get("diagnostic_complete") is True and all(r8j.get("gates",{}).values())
                and prov["r11a_r02_json_sha256"]==R11A_R02_JSON_SHA256 and r11j.get("classification")==R11A_R02_CLASS
                and r11j.get("diagnostic_complete") is True and all(r11j.get("gates",{}).values()))
    except Exception as exc:
        prov={"error":repr(exc)}; g1=False
    if not g1:
        result={"classification":CLS_PROV,"diagnostic_complete":False,"science_evaluated":False,"gates":{"R12A_G1_provenance_source":False},"provenance":prov}
        _write(Path(args.json_out),result); print("STABLE_AEST_R12A_CLASSIFICATION="+CLS_PROV,flush=True); return 3

    work=Path(args.workdir); work.mkdir(parents=True,exist_ok=True)
    py=sys.executable; mod="fullj_weyl.stable_aest_r12a_eg_weyl_growth_consistency"
    specs=[("gr",True,10.0,0.0)]+[( _key(tau,eta),False,tau,eta) for tau in TAUS for eta in ETAS]
    vals={}; runs=[]; all_runs=True
    for name,pure,tau,eta in specs:
        p=work/f"{name}.npz"
        try:
            reuse=False
            if p.is_file():
                try: v=_load_case(p,pure,tau,eta); reuse=True
                except Exception: p.unlink(missing_ok=True)
            if not reuse:
                cmd=[py,"-m",mod,"--worker","--tau",str(tau),"--eta",str(eta),"--out",str(p)]
                if pure: cmd.append("--pure-gr")
                env=os.environ.copy(); env["AEST_R7A_EPOCH_MODE"]="full"
                for x in ("AEST_TANGENT_FORCE_FILE","AEST_TANGENT_LAMBDA","AEST_TANGENT_TRACE_FILE","AEST_R2D_TRACE_FILE","AEST_R2D_TRACE_KH","AEST_R2D_TRACE_ALL_K","AEST_TANGENT_ALLOW_K_MISS","AEST_ERHS_TRACE_FILE","AEST_ERHS_TRACE_K"):
                    env.pop(x,None)
                subprocess.run(cmd,cwd=ROOT,env=env,check=True)
                v=_load_case(p,pure,tau,eta)
            vals[name]=v
            ok=bool(v["max_k_match_error_h_Mpc"]<=K_MATCH); all_runs &= ok
            runs.append({"name":name,"pure_gr":pure,"tau_H0":tau,"eta":eta,"reused":reuse,"max_k_match_error_h_Mpc":v["max_k_match_error_h_Mpc"],"pass":ok})
            print(f"STABLE_AEST_R12A_CASE name={name} reused={int(reuse)} kerr={v['max_k_match_error_h_Mpc']:.3e}",flush=True)
        except Exception as exc:
            all_runs=False; runs.append({"name":name,"pure_gr":pure,"tau_H0":tau,"eta":eta,"pass":False,"error":repr(exc)})
            print(f"STABLE_AEST_R12A_CASE_FAIL name={name} error={exc!r}",flush=True)
    g2=bool(all_runs and len(vals)==len(specs))
    if not g2:
        result={"classification":CLS_COVER,"diagnostic_complete":True,"science_evaluated":False,"gates":{"R12A_G1_provenance_source":True,"R12A_G2_mode_history_coverage":False},"provenance":prov,"runs":runs}
        _write(Path(args.json_out),result); print("STABLE_AEST_R12A_CLASSIFICATION="+CLS_COVER,flush=True); return 1

    # G3: pure-GR sign/unit/normalization control.
    gr=vals["gr"]; gr_metrics={}; g3=True
    for method in ("cubic","pchip"):
        eg=gr[method]["EG"]; fcb=gr[method]["fcb"]; expected=gr["Omega_m"]/fcb
        m=metric(eg,expected); positive=bool(np.all(eg>0) and np.all(np.isfinite(eg)) and np.all(np.abs(gr[method]["fdelta"])>1e-300))
        ok=bool(positive and m["E"]<=GR_ID_E_GATE); g3 &= ok
        gr_metrics[method]={**m,"all_EG_positive":positive,"pass":ok,"EG_min":float(np.min(eg)),"EG_max":float(np.max(eg))}

    # G4: eta0 AeST closure to GR and exact tau invariance.
    eta0_metrics={}; tau_point={}; g4=True
    for method in ("cubic","pchip"):
        ref=vals[_key(10.0,0.0)][method]["EG"]
        eta0_metrics[method]={}; tau_point[method]={}
        for tau in TAUS:
            eg=vals[_key(tau,0.0)][method]["EG"]
            mg=metric(eg,gr[method]["EG"]); pt=_point_rel(eg,ref)
            ok=bool(mg["E"]<=ETA0_E_GATE and mg["C"]>=ETA0_C_GATE and pt<=ETA0_TAU_POINT_GATE)
            g4 &= ok; eta0_metrics[method][str(tau)]={**mg,"pass":ok}; tau_point[method][str(tau)]=pt

    tangents={}; interp_metrics={}; eps_metrics={}; decomp_metrics={}; linearity={}
    g5=g6=g7=g8=True
    for tau in TAUS:
        interp_metrics[str(tau)]={}; eps_metrics[str(tau)]={}; decomp_metrics[str(tau)]={}
        for eps in (EPS_PRIMARY,EPS_CONTROL):
            for method in ("cubic","pchip"):
                for field in ("EG","W","fdelta"):
                    tangents[(tau,eps,method,field)]=_central(vals,tau,eps,method,field)
            mi=metric(tangents[(tau,eps,"cubic","EG")],tangents[(tau,eps,"pchip","EG")])
            ok=tangent_pass(mi); g5 &= ok; interp_metrics[str(tau)][str(eps)]={**mi,"pass":ok}
        for method in ("cubic","pchip"):
            me=metric(tangents[(tau,EPS_PRIMARY,method,"EG")],tangents[(tau,EPS_CONTROL,method,"EG")])
            ok=tangent_pass(me); g6 &= ok; eps_metrics[str(tau)][method]={**me,"pass":ok}
            rhs=tangents[(tau,EPS_PRIMARY,method,"W")]-tangents[(tau,EPS_PRIMARY,method,"fdelta")]
            md=metric(tangents[(tau,EPS_PRIMARY,method,"EG")],rhs)
            okd=bool(md["E"]<=DECOMP_E_GATE and md["C"]>=DECOMP_C_GATE); g7 &= okd
            decomp_metrics[str(tau)][method]={**md,"pass":okd}
        base=vals[_key(tau,0.0)]["cubic"]["EG"]; plus=vals[_key(tau,0.05)]["cubic"]["EG"]
        direct=(plus-base)/base; pred=0.05*tangents[(tau,EPS_PRIMARY,"cubic","EG")]
        ml=metric(direct,pred); okl=bool(ml["E"]<=LINEARITY_E_GATE and ml["C"]>=LINEARITY_C_GATE); g8 &= okl
        linearity[str(tau)]={**ml,"pass":okl}

    gates={
        "R12A_G1_provenance_source":True,"R12A_G2_mode_history_coverage":True,
        "R12A_G3_GR_convention":bool(g3),"R12A_G4_eta0_closure_tau_invariance":bool(g4),
        "R12A_G5_interpolation_control":bool(g5),"R12A_G6_epsilon_consistency":bool(g6),
        "R12A_G7_differential_decomposition":bool(g7),"R12A_G8_local_eta005_linearity":bool(g8),
    }
    if not g3: classification=CLS_GR
    elif not g4: classification=CLS_ETA0
    elif not g5: classification=CLS_INTERP
    elif not g6: classification=CLS_EPS
    elif not g7: classification=CLS_DECOMP
    elif not g8: classification=CLS_LINEAR
    else: classification=CLS_PASS

    science={}; tau_coherence={}; arrays={"k_h_Mpc":K_H,"z":Z,"EG_GR_cubic":gr["cubic"]["EG"]}
    if classification==CLS_PASS:
        tref=tangents[(10.0,EPS_PRIMARY,"cubic","EG")]
        for tau in TAUS:
            T=tangents[(tau,EPS_PRIMARY,"cubic","EG")]; TW=tangents[(tau,EPS_PRIMARY,"cubic","W")]; TF=tangents[(tau,EPS_PRIMARY,"cubic","fdelta")]
            base=vals[_key(tau,0.0)]["cubic"]["EG"]; plus=vals[_key(tau,0.05)]["cubic"]["EG"]; shift=(plus-base)/base
            idx=np.unravel_index(int(np.argmax(np.abs(shift))),shift.shape)
            nw=float(np.linalg.norm(TW)); nf=float(np.linalg.norm(TF)); ne=float(np.linalg.norm(T))
            science[str(tau)]={
                "EG_baseline_min":float(np.min(base)),"EG_baseline_max":float(np.max(base)),
                "max_abs_T_EG_per_eta":float(np.max(np.abs(T))),"rms_T_EG_per_eta":float(np.sqrt(np.mean(T*T))),
                "max_abs_fractional_shift_eta005":float(np.max(np.abs(shift))),"rms_fractional_shift_eta005":float(np.sqrt(np.mean(shift*shift))),
                "largest_fractional_shift":{"k_h_Mpc":float(K_H[idx[0]]),"z":float(Z[idx[1]]),"fractional_shift":float(shift[idx]),"T_EG_per_eta":float(T[idx])},
                "norm_T_W":nw,"norm_T_fdelta":nf,"norm_T_EG":ne,
                "A_ratio":ne/max(nw,nf,1e-300),"linearity":linearity[str(tau)],
            }
            tau_coherence[str(tau)]=metric(tref,T)
            arrays[f"EG0_tau{tau:g}"]=base; arrays[f"T_EG_tau{tau:g}"]=T; arrays[f"T_W_tau{tau:g}"]=TW; arrays[f"T_fdelta_tau{tau:g}"]=TF; arrays[f"shift_eta005_tau{tau:g}"]=shift

    result={
        "classification":classification,"diagnostic_complete":True,"science_evaluated":classification==CLS_PASS,
        "gates":gates,"provenance":prov,"runs":runs,
        "GR_control":gr_metrics,"eta0_closure":eta0_metrics,"eta0_tau_max_point_relative":tau_point,
        "robustness":{"interpolation":interp_metrics,"epsilon":eps_metrics,"decomposition":decomp_metrics,"linearity":linearity},
        "science":science,"tau_coherence":tau_coherence,
        "settings":{"tau_H0":list(TAUS),"eta_values":list(ETAS),"epsilon_primary":EPS_PRIMARY,"epsilon_control":EPS_CONTROL,"k_h_Mpc":K_H.tolist(),"z":Z.tolist(),"primary_time_interpolation":"cubic spline in scale factor","control_time_interpolation":"PCHIP in scale factor","EG_definition":"-k_phys^2(phi+psi)/(3 H0^2 (1+z) fdelta_cb)","fdelta_cb_definition":"-theta_cb/Hconf","no_extrapolation":True,"no_smoothing":True,"no_clipping":True},
        "claim_scope":{"transfer_level_EG_response":classification==CLS_PASS,"observational_EG_detection":False,"galaxy_bias_cancellation_claim":False,"eta_bound":False,"tau_bound":False,"nonlinear_claim":False,"cross_correlation_likelihood":False},
    }
    _write(Path(args.json_out),result)
    np.savez_compressed(args.npz_out,**arrays)
    print("STABLE_AEST_R12A_GATES="+json.dumps(gates,sort_keys=True),flush=True)
    print("STABLE_AEST_R12A_GR="+json.dumps(gr_metrics,sort_keys=True),flush=True)
    print("STABLE_AEST_R12A_ROBUSTNESS="+json.dumps(result["robustness"],sort_keys=True),flush=True)
    if classification==CLS_PASS:
        print("STABLE_AEST_R12A_SCIENCE="+json.dumps(science,sort_keys=True),flush=True)
        print("STABLE_AEST_R12A_TAU="+json.dumps(tau_coherence,sort_keys=True),flush=True)
    print("STABLE_AEST_R12A_CLASSIFICATION="+classification,flush=True)
    return 0 if classification==CLS_PASS else 1


if __name__=="__main__":
    raise SystemExit(main())
