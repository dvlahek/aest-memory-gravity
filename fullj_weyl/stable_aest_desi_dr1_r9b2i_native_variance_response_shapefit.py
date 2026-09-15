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
from scipy.integrate import simpson

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fullj_weyl import stable_aest_observable_projection_r5b_derivative_zero as r5b
from fullj_weyl import stable_aest_desi_dr1_r9b_shapefit_projection as r9b
from fullj_weyl import stable_aest_desi_dr1_r9b2f_full_grid_rogue_node as r9b2f

PREFIT_LOCK = "f7d05f034046388833b74f990c071e65b0ab2f14"
R9B2H_POSTDATA_LOCK = "ffd0a10892c65bf71f134c6d9e78dc9dc13f1a16"
R9B2H_PREFIT_LOCK = "e02eb97bf5675fb33a21f7545e0d7259ef5b97ce"
R9B2H_IMPL_LOCK = "ae5a3bbd3a535d01ceef06c4dd38776de2c6c6c6"
R9B2G_POSTDATA_LOCK = "68ca78bcea41a18af46ec4ccf6e30ddf78f64471"
R9B2F_POSTDATA_LOCK = "b569aebc41efc841755f5fcec63b91092c192ba3"
R9B2H_JSON = ROOT / "results/stable_aest_desi_dr1_r9b2h_derivative_stable_quadrature.json"
R9B2H_JSON_SHA = "7cdf0f17572c351acb118e858a8fc5c206484fa6af2cf8e66531b8cd5927eea2"
R9B2H_CLASS = "STABLE_AEST_DESI_DR1_R9B2H_CROSS_METHOD_DERIVATIVE_FAIL"

ZEFF = np.asarray([
    0.29536404346937617,
    0.5096288678782911,
    0.7057956472488681,
    0.9185851971138159,
    1.3170658832980264,
    1.4905017757527006,
], float)
TAUS = (10.0, 5.0, 2.5, 1.25)
ETAS = (0.0, 0.025, -0.025, 0.05, -0.05)
EPS_PRIMARY = 0.025
EPS_CONTROL = 0.05
TOL = 3.0e-8
REL_GATE = 5.0e-3
E_GATE = 0.05
C_GATE = 0.995
NORM_GATE = 1.0e-12
K_MATCH_RTOL = 1.0e-12
KH_MAX = 5.0

PASS = "STABLE_AEST_DESI_DR1_R9B2I_NATIVE_VARIANCE_RESPONSE_SHAPEFIT_CERTIFIED"
FAIL_PROV = "STABLE_AEST_DESI_DR1_R9B2I_PROVENANCE_FAIL"
FAIL_GRID = "STABLE_AEST_DESI_DR1_R9B2I_NATIVE_GRID_FAIL"
FAIL_CLOSURE = "STABLE_AEST_DESI_DR1_R9B2I_ETA0_CLOSURE_FAIL"
FAIL_TAU = "STABLE_AEST_DESI_DR1_R9B2I_ETA0_TAU_INVARIANCE_FAIL"
FAIL_SIMP = "STABLE_AEST_DESI_DR1_R9B2I_SIMPSON_RESPONSE_FAIL"
FAIL_TRAP = "STABLE_AEST_DESI_DR1_R9B2I_TRAPEZOID_RESPONSE_FAIL"
FAIL_CROSS = "STABLE_AEST_DESI_DR1_R9B2I_CROSS_QUADRATURE_RESPONSE_FAIL"
FAIL_DATA = "STABLE_AEST_DESI_DR1_R9B2I_DESI_PROVENANCE_FAIL"
FAIL_VEC = "STABLE_AEST_DESI_DR1_R9B2I_CORRECTED_VECTOR_FAIL"
FAIL_FULL = "STABLE_AEST_DESI_DR1_R9B2I_FULL_TANGENT_FAIL"
FAIL_FULL_CROSS = "STABLE_AEST_DESI_DR1_R9B2I_FULL_CROSS_QUADRATURE_FAIL"
FAIL_PROJ = "STABLE_AEST_DESI_DR1_R9B2I_NUISANCE_PROJECTION_FAIL"
FAIL_GLS = "STABLE_AEST_DESI_DR1_R9B2I_MATCHED_FILTER_GLS_FAIL"
FAIL_RUN = "STABLE_AEST_DESI_DR1_R9B2I_RUN_FAIL"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ancestor(sha: str) -> bool:
    return subprocess.run(["git", "merge-base", "--is-ancestor", sha, "HEAD"], cwd=ROOT,
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0


def rel(a, b) -> float:
    a = np.asarray(a, float); b = np.asarray(b, float)
    if not np.all(np.isfinite(a)) or not np.all(np.isfinite(b)):
        return float("inf")
    return float(np.linalg.norm(a-b)/max(np.linalg.norm(a), np.linalg.norm(b), 1e-300))


def cosine(a, b) -> float:
    a = np.asarray(a, float); b = np.asarray(b, float)
    na = float(np.linalg.norm(a)); nb = float(np.linalg.norm(b))
    if na <= 0.0 or nb <= 0.0:
        return float("nan")
    return float(np.dot(a, b)/(na*nb))


def metrics(a, b) -> dict:
    a = np.asarray(a, float); b = np.asarray(b, float)
    return {"E": rel(a,b), "C": cosine(a,b),
            "norm_a": float(np.linalg.norm(a)), "norm_b": float(np.linalg.norm(b))}


def metric_pass(m: dict) -> bool:
    return bool(np.isfinite(m["E"]) and np.isfinite(m["C"])
                and m["E"] <= E_GATE and m["C"] >= C_GATE
                and m["norm_a"] > NORM_GATE and m["norm_b"] > NORM_GATE)


def _key(tau: float, eta: float) -> str:
    return f"tau{tau:g}_eta{eta:+.3f}"


def _params(eta: float, tau: float):
    p, bits, pos = r5b.build_params(float(eta), TOL)
    p["aest_tau_H0"] = float(tau)
    p["output"] = "mPk,mTk,vTk"
    p["z_max_pk"] = max(2.3, float(np.max(ZEFF))+0.25)
    p["P_k_max_h/Mpc"] = KH_MAX
    for key in ("non_linear", "lensing", "l_max_scalars", "k_output_values",
                "k_per_decade_for_pk", "k_per_decade_for_bao"):
        p.pop(key, None)
    return p, int(bits), int(pos)


def _variance(kh, pk, method: str) -> float:
    kh = np.asarray(kh, float); pk = np.asarray(pk, float)
    if kh.ndim != 1 or pk.shape != kh.shape or kh.size < 8:
        raise RuntimeError("invalid native variance arrays")
    x = np.log(kh)
    y = kh**3 * pk * r9b2f._w2(8.0*kh) / (2.0*np.pi**2)
    if not np.all(np.isfinite(y)):
        raise RuntimeError("non-finite native variance integrand")
    if method == "simpson":
        return float(simpson(y, x=x))
    if method == "trapezoid":
        return float(np.trapezoid(y, x=x))
    raise ValueError(method)


def _same_k(*states) -> bool:
    k0 = np.asarray(states[0]["kh"], float)
    for st in states[1:]:
        k = np.asarray(st["kh"], float)
        if k.shape != k0.shape or not np.allclose(k, k0, rtol=K_MATCH_RTOL, atol=0.0):
            return False
    return True


def _shape_scalars(c, z: float, fid, fcache) -> dict:
    sf = r9b._model_shapefit_at_z(c, float(z), fid, fcache)
    apar, aper = r9b._geometry(c, float(z), fid)
    fz = fcache[float(z)]
    return {"m": float(sf["m"]), "Ap": float(sf["Ap"]),
            "apar": float(apar), "aper": float(aper),
            "fid_m": float(fz["m"]), "fid_f_sqrt_Ap": float(fz["f_sqrt_Ap"])}


def _run_case(eta: float, tau: float) -> dict:
    from classy import Class
    p, bits, pos = _params(eta, tau)
    c = Class(); c.set(p); c.compute()
    try:
        fid, fcache = r9b._get_fiducial_cache(ZEFF)
        As = float(p["A_s"]); ns = float(p["n_s"])
        rows = []
        for z in ZEFF:
            st = r9b2f._state_at_z(c, float(z), As, ns)
            si = float(c.sigma(8.0, float(z), h_units=True))
            proxy = float(c.effective_f_sigma8(float(z), z_step=0.1))/si
            shape = _shape_scalars(c, float(z), fid, fcache)
            rows.append({"z": float(z), "state": st, "sigma_internal": si,
                         "growth_proxy": proxy, "shape": shape})
        return {"rows": rows, "bits": bits, "target_pos": pos}
    finally:
        c.struct_cleanup(); c.empty()


def _row(case: dict, iz: int) -> dict:
    return case["rows"][iz]


def _baseline(case: dict, method: str) -> dict:
    sdd=[]; stt=[]; ff=[]
    for row in case["rows"]:
        st=row["state"]
        vd=_variance(st["kh"],st["pdd"],method)
        vt=_variance(st["kh"],st["ptt"],method)
        if not (np.isfinite(vd) and np.isfinite(vt) and vd>0.0 and vt>0.0):
            raise RuntimeError("non-positive eta0 native variance")
        sd=float(np.sqrt(vd)); stt0=float(np.sqrt(vt))
        sdd.append(sd); stt.append(stt0); ff.append(stt0/sd)
    return {"sigma8_dd":np.asarray(sdd), "sigma8_tt":np.asarray(stt), "f":np.asarray(ff)}


def _response(zero: dict, plus: dict, minus: dict, eps: float, method: str) -> dict:
    df=[]; dsd=[]; dst=[]; dvd=[]; dvt=[]
    for iz in range(len(ZEFF)):
        rz=_row(zero,iz); rp=_row(plus,iz); rm=_row(minus,iz)
        sz=rz["state"]; sp=rp["state"]; sm=rm["state"]
        if not _same_k(sz,sp,sm):
            raise RuntimeError(f"central-pair k-grid mismatch z={ZEFF[iz]} eps={eps}")
        kh=np.asarray(sz["kh"],float)
        vd0=_variance(kh,sz["pdd"],method); vt0=_variance(kh,sz["ptt"],method)
        if vd0<=0.0 or vt0<=0.0:
            raise RuntimeError("invalid baseline variance")
        Dd=(np.asarray(sp["pdd"])-np.asarray(sm["pdd"]))/(2.0*eps)
        Dt=(np.asarray(sp["ptt"])-np.asarray(sm["ptt"]))/(2.0*eps)
        dVd=_variance(kh,Dd,method); dVt=_variance(kh,Dt,method)
        sd=float(np.sqrt(vd0)); st=float(np.sqrt(vt0))
        dSd=dVd/(2.0*sd); dSt=dVt/(2.0*st)
        dF=dSt/sd-st*dSd/(sd*sd)
        dvd.append(dVd); dvt.append(dVt); dsd.append(dSd); dst.append(dSt); df.append(dF)
    return {"df":np.asarray(df), "d_sigma8_dd":np.asarray(dsd), "d_sigma8_tt":np.asarray(dst),
            "dVdd":np.asarray(dvd), "dVtt":np.asarray(dvt)}


def _q(shape: dict, param: str) -> float:
    apar=float(shape["apar"]); aper=float(shape["aper"])
    if param in ("qpar","qper","qiso","qap"):
        suffix=param[1:]
        a,b={"iso":(1./3.,2./3.),"par":(1.,0.),"per":(0.,1.),"ap":(1.,-1.)}[suffix]
        return float(apar**a*aper**b)
    raise ValueError(param)


def _assemble_baseline(case0: dict, f0: np.ndarray, bins) -> np.ndarray:
    out=[]
    for iz,b in enumerate(bins):
        sh=_row(case0,iz)["shape"]
        for p in b["parameters"]:
            if p in ("qpar","qper","qiso","qap"):
                v=_q(sh,p)
            elif p=="df":
                v=float(f0[iz]*np.sqrt(sh["Ap"])/sh["fid_f_sqrt_Ap"])
            elif p=="dm":
                v=float(sh["m"]-sh["fid_m"])
            else:
                raise RuntimeError(f"unsupported ShapeFit parameter {p}")
            out.append(v)
    return np.asarray(out,float)


def _assemble_tangent(zero: dict, plus: dict, minus: dict, source_resp: dict,
                      eps: float, baseline: dict, bins) -> np.ndarray:
    out=[]
    f0=np.asarray(baseline["f"],float); df=np.asarray(source_resp["df"],float)
    for iz,b in enumerate(bins):
        sh0=_row(zero,iz)["shape"]; shp=_row(plus,iz)["shape"]; shm=_row(minus,iz)["shape"]
        dAp=(float(shp["Ap"])-float(shm["Ap"]))/(2.0*eps)
        dS=np.sqrt(sh0["Ap"])*df[iz] + f0[iz]*dAp/(2.0*np.sqrt(sh0["Ap"]))
        for p in b["parameters"]:
            if p in ("qpar","qper","qiso","qap"):
                v=(_q(shp,p)-_q(shm,p))/(2.0*eps)
            elif p=="df":
                v=float(dS/sh0["fid_f_sqrt_Ap"])
            elif p=="dm":
                v=(float(shp["m"])-float(shm["m"]))/(2.0*eps)
            else:
                raise RuntimeError(f"unsupported ShapeFit parameter {p}")
            out.append(v)
    return np.asarray(out,float)


def _provenance() -> tuple[bool,dict]:
    meta={}
    try:
        meta["r9b2h_json_exists"]=R9B2H_JSON.is_file()
        meta["r9b2h_json_sha256"]=sha256(R9B2H_JSON) if R9B2H_JSON.is_file() else None
        old=json.loads(R9B2H_JSON.read_text()) if R9B2H_JSON.is_file() else {}
        meta["r9b2h_classification"]=old.get("classification")
        locks=(PREFIT_LOCK,R9B2H_POSTDATA_LOCK,R9B2H_PREFIT_LOCK,R9B2H_IMPL_LOCK,R9B2G_POSTDATA_LOCK,R9B2F_POSTDATA_LOCK)
        meta["ancestor_locks"]={x:ancestor(x) for x in locks}
        source_ok, source_meta=r9b.r8a.source_topology(); meta["source_topology"]=source_meta
        ok=bool(all(meta["ancestor_locks"].values()) and meta["r9b2h_json_sha256"]==R9B2H_JSON_SHA
                and old.get("classification")==R9B2H_CLASS and old.get("diagnostic_complete") is True
                and source_ok)
        return ok,meta
    except Exception as exc:
        meta["error"]=repr(exc); return False,meta


def _write(path: Path, out: dict):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")


def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--data-dir",default=os.environ.get("AEST_R9B_DESI_DATA_DIR",""))
    ap.add_argument("--official-repo",default=os.environ.get("AEST_R9B_DESI_REPO",""))
    ap.add_argument("--json-out",default="results/stable_aest_desi_dr1_r9b2i_native_variance_response_shapefit.json")
    ap.add_argument("--npz-out",default="results/stable_aest_desi_dr1_r9b2i_native_variance_response_shapefit.npz")
    args=ap.parse_args(); outpath=Path(args.json_out)
    print("STABLE_AEST_DESI_DR1_R9B2I_START",flush=True)

    gA1,prov=_provenance()
    if not gA1:
        out={"classification":FAIL_PROV,"diagnostic_complete":False,"science_evaluated":False,
             "desi_data_loaded":False,"provenance":prov,"gates":{"R9B2I_A1_provenance":False}}
        _write(outpath,out); print("STABLE_AEST_DESI_DR1_R9B2I_CLASSIFICATION="+FAIL_PROV,flush=True); return 3

    vals={}; runs=[]
    try:
        for tau in TAUS:
            for eta in ETAS:
                print(f"STABLE_AEST_DESI_DR1_R9B2I_RUN tau={tau:g} eta={eta:+.3f}",flush=True)
                vals[_key(tau,eta)]=_run_case(eta,tau); runs.append({"tau_H0":tau,"eta":eta,"ok":True})
    except Exception as exc:
        out={"classification":FAIL_RUN,"diagnostic_complete":False,"science_evaluated":False,"desi_data_loaded":False,
             "error":repr(exc),"runs":runs,"provenance":prov}
        _write(outpath,out); print(f"STABLE_AEST_DESI_DR1_R9B2I_RUN_FAIL error={exc!r}",flush=True); return 2

    # A2: native-grid identity and finite/physical eta0 state.
    gA2=True; grid_meta=[]
    for tau in TAUS:
        zc=vals[_key(tau,0.0)]
        for eps in (EPS_PRIMARY,EPS_CONTROL):
            pp=vals[_key(tau,+eps)]; mm=vals[_key(tau,-eps)]
            for iz,z in enumerate(ZEFF):
                ss=[_row(x,iz)["state"] for x in (zc,pp,mm)]
                same=_same_k(*ss); gA2 &= same
                st=ss[0]
                physical=bool(np.all(np.isfinite(st["pdd"])) and np.all(np.isfinite(st["ptt"]))
                              and np.all(np.asarray(st["pdd"])>0) and np.all(np.asarray(st["ptt"])>0))
                gA2 &= physical
                grid_meta.append({"tau_H0":tau,"epsilon":eps,"z":float(z),"same_k":same,
                                  "n_k":int(len(st["kh"])),"kh_min":float(st["kh"][0]),"kh_max":float(st["kh"][-1])})

    baselines={m:{} for m in ("simpson","trapezoid")}
    responses={m:{} for m in ("simpson","trapezoid")}
    try:
        for method in baselines:
            for tau in TAUS:
                zc=vals[_key(tau,0.0)]
                baselines[method][str(tau)]=_baseline(zc,method)
                responses[method][str(tau)]={}
                for eps in (EPS_PRIMARY,EPS_CONTROL):
                    responses[method][str(tau)][str(eps)]=_response(
                        zc,vals[_key(tau,+eps)],vals[_key(tau,-eps)],eps,method)
    except Exception as exc:
        out={"classification":FAIL_RUN,"diagnostic_complete":False,"science_evaluated":False,"desi_data_loaded":False,
             "error":repr(exc),"runs":runs,"provenance":prov}
        _write(outpath,out); print(f"STABLE_AEST_DESI_DR1_R9B2I_RESPONSE_FAIL error={exc!r}",flush=True); return 2

    closure={"sigma8_dd":0.0,"f":0.0}; gA3=True
    for tau in TAUS:
        b=baselines["simpson"][str(tau)]; case=vals[_key(tau,0.0)]
        for iz in range(len(ZEFF)):
            si=_row(case,iz)["sigma_internal"]; gp=_row(case,iz)["growth_proxy"]
            rd=abs(b["sigma8_dd"][iz]-si)/max(abs(b["sigma8_dd"][iz]),abs(si),1e-300)
            rf=abs(b["f"][iz]-gp)/max(abs(b["f"][iz]),abs(gp),1e-300)
            closure["sigma8_dd"]=max(closure["sigma8_dd"],rd); closure["f"]=max(closure["f"],rf)
            gA3 &= bool(rd<=REL_GATE and rf<=REL_GATE)

    tauvar={q:0.0 for q in ("sigma8_dd","sigma8_tt","f")}; gA4=True
    for iz in range(len(ZEFF)):
        for q in tauvar:
            a=np.asarray([baselines["simpson"][str(t)][q][iz] for t in TAUS],float)
            r=(float(np.max(a))-float(np.min(a)))/max(float(np.max(np.abs(a))),1e-300)
            tauvar[q]=max(tauvar[q],r); gA4 &= r<=REL_GATE

    response_metrics={"simpson":{},"trapezoid":{},"cross":{}}; gA5=True; gA6=True; gA7=True
    for tau in TAUS:
        s=str(tau)
        for method in ("simpson","trapezoid"):
            p=responses[method][s][str(EPS_PRIMARY)]["df"]
            c=responses[method][s][str(EPS_CONTROL)]["df"]
            m=metrics(p,c); response_metrics[method][s]=m
            if method=="simpson": gA5 &= metric_pass(m)
            else: gA6 &= metric_pass(m)
        response_metrics["cross"][s]={}
        for eps in (EPS_PRIMARY,EPS_CONTROL):
            a=responses["simpson"][s][str(eps)]["df"]
            b=responses["trapezoid"][s][str(eps)]["df"]
            m=metrics(a,b); response_metrics["cross"][s][str(eps)]=m; gA7 &= metric_pass(m)

    gates={"R9B2I_A1_provenance":True,"R9B2I_A2_native_grid":bool(gA2),
           "R9B2I_A3_eta0_closure":bool(gA3),"R9B2I_A4_eta0_tau_invariance":bool(gA4),
           "R9B2I_A5_simpson_response":bool(gA5),"R9B2I_A6_trapezoid_response":bool(gA6),
           "R9B2I_A7_cross_quadrature_response":bool(gA7)}
    stageA={"closure_max_rel":closure,"tau_variation_max_rel":tauvar,"response_metrics":response_metrics,
            "grid":grid_meta}
    if not gA2: fail=FAIL_GRID
    elif not gA3: fail=FAIL_CLOSURE
    elif not gA4: fail=FAIL_TAU
    elif not gA5: fail=FAIL_SIMP
    elif not gA6: fail=FAIL_TRAP
    elif not gA7: fail=FAIL_CROSS
    else: fail=None
    print("STABLE_AEST_DESI_DR1_R9B2I_STAGE_A_GATES="+json.dumps(gates,sort_keys=True),flush=True)
    print("STABLE_AEST_DESI_DR1_R9B2I_STAGE_A_METRICS="+json.dumps({"closure":closure,"tauvar":tauvar,"response":response_metrics},sort_keys=True),flush=True)
    if fail:
        out={"classification":fail,"diagnostic_complete":True,"science_evaluated":False,"desi_data_loaded":False,
             "gates":gates,"stageA":stageA,"provenance":prov,"runs":runs,
             "interpretation":{"historical_failures_reclassified":False,"observational_detection_claim_licensed":False}}
        _write(outpath,out); print("STABLE_AEST_DESI_DR1_R9B2I_CLASSIFICATION="+fail,flush=True); return 1

    # Stage B: only now touch official DESI files/repository.
    print("STABLE_AEST_DESI_DR1_R9B2I_STAGE_A_PASS_LOADING_DESI",flush=True)
    data_dir=Path(args.data_dir).resolve() if args.data_dir else None
    official_repo=Path(args.official_repo).resolve() if args.official_repo else None
    data_loaded=False
    try:
        if data_dir is None or official_repo is None or not data_dir.is_dir() or not official_repo.is_dir():
            raise RuntimeError("missing DESI data/repository path")
        bins,d,C,offsets,data_hashes,_=r9b.load_desi(data_dir,official_repo); data_loaded=True
        repo_head=subprocess.check_output(["git","-C",str(official_repo),"rev-parse","HEAD"],text=True).strip()
        eig=np.linalg.eigvalsh(C)
        ze=np.asarray([float(b["zeff"]) for b in bins],float)
        gB1=bool(repo_head==r9b.DESI_REPO_COMMIT and len(bins)==6 and len(d)==24
                 and np.allclose(ze,ZEFF,rtol=0,atol=1e-12) and np.all(np.isfinite(d)) and np.all(np.isfinite(C))
                 and np.allclose(C,C.T,rtol=0,atol=1e-12) and np.all(eig>0.0))
        data_meta={"repo_head":repo_head,"files_sha256":data_hashes,"dimension":int(len(d)),
                   "min_cov_eigenvalue":float(eig.min()),"bins":[{"namespace":b["namespace"],"zeff":b["zeff"],"parameters":b["parameters"]} for b in bins]}
    except Exception as exc:
        gB1=False; bins=[]; d=C=offsets=None; data_meta={"error":repr(exc)}
    gates["R9B2I_B1_desi_provenance"]=bool(gB1)
    if not gB1:
        out={"classification":FAIL_DATA,"diagnostic_complete":True,"science_evaluated":False,
             "desi_data_loaded":data_loaded,"gates":gates,"stageA":stageA,"data":data_meta,"provenance":prov,"runs":runs}
        _write(outpath,out); print("STABLE_AEST_DESI_DR1_R9B2I_CLASSIFICATION="+FAIL_DATA,flush=True); return 1

    full={"simpson":{},"trapezoid":{}}; full_metrics={"within_simpson":{},"cross":{}}
    baseline_simpson=_assemble_baseline(vals[_key(10.0,0.0)],baselines["simpson"]["10.0"]["f"],bins)
    gB2=bool(np.all(np.isfinite(baseline_simpson)))
    for tau in TAUS:
        s=str(tau); full["simpson"][s]={}; full["trapezoid"][s]={}
        zc=vals[_key(tau,0.0)]
        for eps in (EPS_PRIMARY,EPS_CONTROL):
            pp=vals[_key(tau,+eps)]; mm=vals[_key(tau,-eps)]
            for method in ("simpson","trapezoid"):
                t=_assemble_tangent(zc,pp,mm,responses[method][s][str(eps)],eps,baselines[method][s],bins)
                full[method][s][str(eps)]=t; gB2 &= bool(np.all(np.isfinite(t)))
    gates["R9B2I_B2_corrected_vector"]=bool(gB2)

    gB3=True; gB4=True
    for tau in TAUS:
        s=str(tau)
        m=metrics(full["simpson"][s][str(EPS_PRIMARY)],full["simpson"][s][str(EPS_CONTROL)])
        full_metrics["within_simpson"][s]=m; gB3 &= metric_pass(m)
        full_metrics["cross"][s]={}
        for eps in (EPS_PRIMARY,EPS_CONTROL):
            mc=metrics(full["simpson"][s][str(eps)],full["trapezoid"][s][str(eps)])
            full_metrics["cross"][s][str(eps)]=mc; gB4 &= metric_pass(mc)
    gates["R9B2I_B3_full_tangent"]=bool(gB3)
    gates["R9B2I_B4_full_cross_quadrature"]=bool(gB4)

    projection={}; gB5=bool(gB2 and gB3 and gB4); gB6=bool(gB5)
    if gB5:
        for tau in TAUS:
            try:
                t=full["simpson"][str(tau)][str(EPS_PRIMARY)]
                p=r9b.projection_summary(d,C,baseline_simpson,t,bins,offsets); projection[str(tau)]=p
                gB5 &= bool(np.isfinite(p["F_perp"]) and p["F_perp"]>0.0 and p["projection_idempotence_metric"]<=1e-8)
                a=p["eta_hat_signed_matched_filter"]; b=p["eta_hat_signed_gls"]
                gB6 &= abs(a-b)<=max(1e-10,1e-8*max(abs(a),abs(b),1.0))
            except Exception as exc:
                projection[str(tau)]={"error":repr(exc)}; gB5=False; gB6=False
    gates["R9B2I_B5_nuisance_projection"]=bool(gB5)
    gates["R9B2I_B6_matched_filter_gls"]=bool(gB6)

    if not gB2: classification=FAIL_VEC
    elif not gB3: classification=FAIL_FULL
    elif not gB4: classification=FAIL_FULL_CROSS
    elif not gB5: classification=FAIL_PROJ
    elif not gB6: classification=FAIL_GLS
    else: classification=PASS

    result={"classification":classification,"diagnostic_complete":True,"science_evaluated":True,
            "desi_data_loaded":True,"gates":gates,"stageA":stageA,"stageB":{"full_tangent_metrics":full_metrics,"tau_likelihood":projection},
            "data":data_meta,"provenance":prov,"runs":runs,
            "settings":{"tau_H0_grid":list(TAUS),"eta_grid":list(ETAS),"epsilon_primary":EPS_PRIMARY,
                        "epsilon_control":EPS_CONTROL,"E_gate":E_GATE,"C_gate":C_GATE,"rel_gate":REL_GATE,
                        "variance_response":"central difference spectrum integrated on native CLASS log-k nodes",
                        "primary_quadrature":"Simpson native nodes","control_quadrature":"trapezoid native nodes",
                        "eta_physical_interval":[r9b.ETA_PHYS_MIN,r9b.ETA_PHYS_MAX]},
            "interpretation":{"historical_failures_reclassified":False,
                              "compressed_full_shape_corrected_projection_reportable":classification==PASS,
                              "observational_detection_claim_licensed":False,
                              "full_EFT_modified_gravity_claim_licensed":False,"tau_bound_claim_licensed":False}}
    _write(outpath,result)
    if data_loaded:
        arrays={"data":d,"covariance":C,"baseline":baseline_simpson}
        for tau in TAUS:
            arrays[f"tangent_tau{tau:g}"]=full["simpson"][str(tau)][str(EPS_PRIMARY)]
            arrays[f"source_df_response_tau{tau:g}"]=responses["simpson"][str(tau)][str(EPS_PRIMARY)]["df"]
        np.savez_compressed(args.npz_out,**arrays)
    print("STABLE_AEST_DESI_DR1_R9B2I_GATES="+json.dumps(gates,sort_keys=True),flush=True)
    print("STABLE_AEST_DESI_DR1_R9B2I_PROJECTION="+json.dumps(projection,sort_keys=True),flush=True)
    print("STABLE_AEST_DESI_DR1_R9B2I_CLASSIFICATION="+classification,flush=True)
    return 0 if classification==PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
