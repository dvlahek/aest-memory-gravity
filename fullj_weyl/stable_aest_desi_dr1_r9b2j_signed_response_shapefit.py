#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import numpy as np
from scipy.integrate import simpson
from scipy.interpolate import PchipInterpolator

from fullj_weyl import stable_aest_desi_dr1_r9b2i_native_variance_response_shapefit as i
from fullj_weyl import stable_aest_desi_dr1_r9b_shapefit_projection as r9b
from fullj_weyl import stable_aest_desi_dr1_r9b2f_full_grid_rogue_node as r9b2f

ROOT = Path(__file__).resolve().parents[1]
PREFIT_LOCK = "dbf354f4ef3122fff44b1b389f1adc839e9e7f9d"
R9B2I_RUNNER_LOCK = "2264f6dace0e6da1c4e9966f01d446d0de7e68a0"
R9B2H_POSTDATA_LOCK = "ffd0a10892c65bf71f134c6d9e78dc9dc13f1a16"
R9B2I_JSON = ROOT / "results/stable_aest_desi_dr1_r9b2i_native_variance_response_shapefit.json"
R9B2I_SHA = "859d92d849c295d3a5219980a9caa82c283952f814e98df19a1b44ca5fe97164"
R9B2I_CLASS = "STABLE_AEST_DESI_DR1_R9B2I_CROSS_QUADRATURE_RESPONSE_FAIL"

ZEFF=i.ZEFF; TAUS=i.TAUS; ETAS=i.ETAS
EPS_PRIMARY=i.EPS_PRIMARY; EPS_CONTROL=i.EPS_CONTROL
REL_GATE=i.REL_GATE; E_GATE=i.E_GATE; C_GATE=i.C_GATE; NORM_GATE=i.NORM_GATE

PASS="STABLE_AEST_DESI_DR1_R9B2J_SIGNED_RESPONSE_SHAPEFIT_CERTIFIED"
FAIL_PROV="STABLE_AEST_DESI_DR1_R9B2J_PROVENANCE_FAIL"
FAIL_GRID="STABLE_AEST_DESI_DR1_R9B2J_GRID_FAIL"
FAIL_CLOSURE="STABLE_AEST_DESI_DR1_R9B2J_ETA0_CLOSURE_FAIL"
FAIL_RES="STABLE_AEST_DESI_DR1_R9B2J_RESPONSE_RESOLUTION_FAIL"
FAIL_EPS="STABLE_AEST_DESI_DR1_R9B2J_EPSILON_CONSISTENCY_FAIL"
FAIL_CROSS="STABLE_AEST_DESI_DR1_R9B2J_CROSS_OPERATOR_FAIL"
FAIL_DATA="STABLE_AEST_DESI_DR1_R9B2J_DESI_PROVENANCE_FAIL"
FAIL_VEC="STABLE_AEST_DESI_DR1_R9B2J_SHAPEFIT_VECTOR_FAIL"
FAIL_FULL="STABLE_AEST_DESI_DR1_R9B2J_FULL_TANGENT_FAIL"
FAIL_FULL_CROSS="STABLE_AEST_DESI_DR1_R9B2J_FULL_CROSS_OPERATOR_FAIL"
FAIL_PROJ="STABLE_AEST_DESI_DR1_R9B2J_NUISANCE_PROJECTION_FAIL"
FAIL_GLS="STABLE_AEST_DESI_DR1_R9B2J_MATCHED_FILTER_GLS_FAIL"
FAIL_RUN="STABLE_AEST_DESI_DR1_R9B2J_RUN_FAIL"


def sha256(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def ancestor(sha):
    return subprocess.run(["git","merge-base","--is-ancestor",sha,"HEAD"],cwd=ROOT,
                          stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode==0

def metric_pass(m):
    return bool(np.isfinite(m["E"]) and np.isfinite(m["C"]) and m["E"]<=E_GATE and m["C"]>=C_GATE
                and m["norm_a"]>NORM_GATE and m["norm_b"]>NORM_GATE)

def write_json(path,obj):
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n")


def source_shape(c,state,z,fid,fcache):
    from cosmoprimo import Cosmology, PowerSpectrumInterpolator1D
    h=float(c.h()); rdrag=float(c.rs_drag())
    cosmo=Cosmology(H0=100.*h,Omega_b=r9b._omega(c,"Omega_b"),Omega_cdm=r9b._omega(c,"Omega_cdm"),
                    Omega_ncdm=r9b._omega(c,"Omega_nu",0.0),n_s=float(c.n_s()))
    try: cosmo.rs_drag=rdrag*h
    except Exception: pass
    kh=np.asarray(state["kh"],float); pdd=np.asarray(state["pdd"],float)
    pkdd=PowerSpectrumInterpolator1D(kh,pdd,extrap_kmin=float(kh[0]),extrap_kmax=float(kh[-1]))
    filt=fcache[float(z)]["filter"]
    filt(pkdd,cosmo=cosmo); pknow=filt.smooth_pk_interpolator()
    s=(rdrag*h)/float(fid.rs_drag); kp=0.03/s; dk=1e-2
    kk=kp*np.asarray([1.-dk,1.+dk])
    if kk[0]<=kh[0] or kk[-1]>=kh[-1]: raise RuntimeError(f"ShapeFit pivot outside bounded source support z={z}")
    m=float(np.diff(np.log(np.asarray(pknow(kk),float)))[0]/np.diff(np.log(kk))[0])
    Ap=float((1./s**3)*np.asarray(pkdd(kp)))
    apar,aper=r9b._geometry(c,float(z),fid); fz=fcache[float(z)]
    return {"m":m,"Ap":Ap,"apar":float(apar),"aper":float(aper),"fid_m":float(fz["m"]),
            "fid_f_sqrt_Ap":float(fz["f_sqrt_Ap"])}


def run_case(eta,tau):
    from classy import Class
    p,bits,pos=i._params(float(eta),float(tau)); c=Class(); c.set(p); c.compute()
    try:
        fid,fcache=r9b._get_fiducial_cache(ZEFF); As=float(p["A_s"]); ns=float(p["n_s"]); rows=[]
        for z in ZEFF:
            st=r9b2f._state_at_z(c,float(z),As,ns)
            si=float(c.sigma(8.0,float(z),h_units=True)); proxy=float(c.effective_f_sigma8(float(z),z_step=0.1))/si
            rows.append({"z":float(z),"state":st,"sigma_internal":si,"growth_proxy":proxy,
                         "shape":source_shape(c,st,float(z),fid,fcache)})
        return {"rows":rows,"bits":int(bits),"target_pos":int(pos)}
    finally:
        c.struct_cleanup(); c.empty()


def positive_variance(kh,pk,mode,n):
    kh=np.asarray(kh,float); pk=np.asarray(pk,float)
    if kh.ndim!=1 or pk.shape!=kh.shape or kh.size<32 or np.any(~np.isfinite(pk)) or np.any(pk<=0):
        raise RuntimeError("invalid positive variance input")
    x=np.log(kh); xg=np.linspace(x[0],x[-1],int(n))
    if mode=="linear": lpg=np.interp(xg,x,np.log(pk))
    elif mode=="pchip": lpg=np.asarray(PchipInterpolator(x,np.log(pk),extrapolate=False)(xg),float)
    else: raise ValueError(mode)
    kg=np.exp(xg); y=kg**3*np.exp(lpg)*r9b2f._w2(8.*kg)/(2.*np.pi**2)
    v=float(simpson(y,x=xg))
    if not np.isfinite(v) or v<=0: raise RuntimeError(f"invalid baseline variance {mode}/{n}: {v}")
    return v


def signed_response_integral(kh,dpk,mode,n):
    kh=np.asarray(kh,float); dpk=np.asarray(dpk,float)
    if kh.ndim!=1 or dpk.shape!=kh.shape or kh.size<32 or np.any(~np.isfinite(dpk)):
        raise RuntimeError("invalid signed response input")
    x=np.log(kh); xg=np.linspace(x[0],x[-1],int(n))
    if mode=="linear": dg=np.interp(xg,x,dpk)
    elif mode=="pchip": dg=np.asarray(PchipInterpolator(x,dpk,extrapolate=False)(xg),float)
    else: raise ValueError(mode)
    kg=np.exp(xg); y=kg**3*dg*r9b2f._w2(8.*kg)/(2.*np.pi**2)
    v=float(simpson(y,x=xg))
    if not np.isfinite(v): raise RuntimeError(f"invalid signed response integral {mode}/{n}")
    return v


def baseline(case,mode,n):
    out={"sigma8_dd":[],"sigma8_tt":[],"f":[]}
    for row in case["rows"]:
        st=row["state"]; vd=positive_variance(st["kh"],st["pdd"],mode,n); vt=positive_variance(st["kh"],st["ptt"],mode,n)
        sd=float(np.sqrt(vd)); stt=float(np.sqrt(vt))
        out["sigma8_dd"].append(sd); out["sigma8_tt"].append(stt); out["f"].append(stt/sd)
    return {k:np.asarray(v,float) for k,v in out.items()}


def response(zero,plus,minus,eps,mode,n):
    out={"df":[],"d_sigma8_dd":[],"d_sigma8_tt":[],"dVdd":[],"dVtt":[]}
    for iz in range(len(ZEFF)):
        rz=i._row(zero,iz); rp=i._row(plus,iz); rm=i._row(minus,iz)
        sz,sp,sm=rz["state"],rp["state"],rm["state"]
        if not i._same_k(sz,sp,sm): raise RuntimeError(f"central k-grid mismatch z={ZEFF[iz]} eps={eps}")
        kh=np.asarray(sz["kh"],float); vd0=positive_variance(kh,sz["pdd"],mode,n); vt0=positive_variance(kh,sz["ptt"],mode,n)
        Dd=(np.asarray(sp["pdd"],float)-np.asarray(sm["pdd"],float))/(2.*eps)
        Dt=(np.asarray(sp["ptt"],float)-np.asarray(sm["ptt"],float))/(2.*eps)
        dVd=signed_response_integral(kh,Dd,mode,n); dVt=signed_response_integral(kh,Dt,mode,n)
        sd=float(np.sqrt(vd0)); st=float(np.sqrt(vt0)); dSd=dVd/(2.*sd); dSt=dVt/(2.*st)
        out["dVdd"].append(dVd); out["dVtt"].append(dVt); out["d_sigma8_dd"].append(dSd); out["d_sigma8_tt"].append(dSt)
        out["df"].append(dSt/sd-st*dSd/(sd*sd))
    return {k:np.asarray(v,float) for k,v in out.items()}


def provenance():
    meta={}
    try:
        old=json.loads(R9B2I_JSON.read_text()) if R9B2I_JSON.is_file() else {}; gates=old.get("gates",{})
        meta["r9b2i_json_exists"]=R9B2I_JSON.is_file(); meta["r9b2i_json_sha256"]=sha256(R9B2I_JSON) if R9B2I_JSON.is_file() else None
        meta["r9b2i_classification"]=old.get("classification"); meta["r9b2i_gates"]=gates
        locks=(PREFIT_LOCK,R9B2I_RUNNER_LOCK,R9B2H_POSTDATA_LOCK); meta["ancestor_locks"]={x:ancestor(x) for x in locks}
        source_ok,source_meta=r9b.r8a.source_topology(); meta["source_topology"]=source_meta
        expected=("R9B2I_A1_provenance","R9B2I_A2_native_grid","R9B2I_A3_eta0_closure","R9B2I_A4_eta0_tau_invariance",
                  "R9B2I_A5_simpson_response","R9B2I_A6_trapezoid_response")
        ok=bool(all(meta["ancestor_locks"].values()) and meta["r9b2i_json_sha256"]==R9B2I_SHA and old.get("classification")==R9B2I_CLASS
                and old.get("diagnostic_complete") is True and all(gates.get(x) is True for x in expected)
                and gates.get("R9B2I_A7_cross_quadrature_response") is False and source_ok)
        return ok,meta
    except Exception as exc:
        meta["error"]=repr(exc); return False,meta


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--data-dir",default=""); ap.add_argument("--official-repo",default="")
    ap.add_argument("--json-out",default="results/stable_aest_desi_dr1_r9b2j_signed_response_shapefit.json")
    ap.add_argument("--npz-out",default="results/stable_aest_desi_dr1_r9b2j_signed_response_shapefit.npz")
    args=ap.parse_args(); outpath=Path(args.json_out)
    print("STABLE_AEST_DESI_DR1_R9B2J_START",flush=True)
    g1,prov=provenance()
    if not g1:
        write_json(outpath,{"classification":FAIL_PROV,"diagnostic_complete":False,"science_evaluated":False,"desi_data_loaded":False,
                            "provenance":prov,"gates":{"R9B2J_J1_provenance":False}})
        print("STABLE_AEST_DESI_DR1_R9B2J_CLASSIFICATION="+FAIL_PROV,flush=True); return 3

    vals={}; runs=[]
    try:
        for tau in TAUS:
            for eta in ETAS:
                print(f"STABLE_AEST_DESI_DR1_R9B2J_RUN tau={tau:g} eta={eta:+.3f}",flush=True)
                vals[i._key(tau,eta)]=run_case(eta,tau); runs.append({"tau_H0":tau,"eta":eta,"ok":True})
    except Exception as exc:
        write_json(outpath,{"classification":FAIL_RUN,"diagnostic_complete":False,"science_evaluated":False,"desi_data_loaded":False,
                            "error":repr(exc),"runs":runs,"provenance":prov})
        print(f"STABLE_AEST_DESI_DR1_R9B2J_RUN_FAIL error={exc!r}",flush=True); return 2

    g2=True; grid=[]
    for tau in TAUS:
        zc=vals[i._key(tau,0.)]
        for eps in (EPS_PRIMARY,EPS_CONTROL):
            pp,mm=vals[i._key(tau,+eps)],vals[i._key(tau,-eps)]
            for iz,z in enumerate(ZEFF):
                ss=[i._row(x,iz)["state"] for x in (zc,pp,mm)]; same=i._same_k(*ss); st=ss[0]; kh=np.asarray(st["kh"],float)
                healthy=bool(same and kh.size>=32 and np.all(np.isfinite(kh)) and kh[0]<=2e-4 and kh[-1]>=2.
                             and np.all(np.isfinite(st["pdd"])) and np.all(np.asarray(st["pdd"])>0)
                             and np.all(np.isfinite(st["ptt"])) and np.all(np.asarray(st["ptt"])>0))
                g2 &= healthy; grid.append({"tau_H0":tau,"epsilon":eps,"z":float(z),"same_k":same,"healthy":healthy,
                                            "n_k":int(kh.size),"kh_min":float(kh[0]),"kh_max":float(kh[-1])})

    baselines={"linear8192":{},"pchip8192":{}}; responses={x:{} for x in ("linear4096","linear8192","linear16384","pchip8192")}
    try:
        for tau in TAUS:
            s=str(tau); zc=vals[i._key(tau,0.)]
            baselines["linear8192"][s]=baseline(zc,"linear",8192); baselines["pchip8192"][s]=baseline(zc,"pchip",8192)
            for name,mode,n in (("linear4096","linear",4096),("linear8192","linear",8192),("linear16384","linear",16384),("pchip8192","pchip",8192)):
                responses[name][s]={}
                for eps in (EPS_PRIMARY,EPS_CONTROL): responses[name][s][str(eps)]=response(zc,vals[i._key(tau,+eps)],vals[i._key(tau,-eps)],eps,mode,n)
    except Exception as exc:
        write_json(outpath,{"classification":FAIL_RUN,"diagnostic_complete":False,"science_evaluated":False,"desi_data_loaded":False,
                            "error":repr(exc),"runs":runs,"provenance":prov})
        print(f"STABLE_AEST_DESI_DR1_R9B2J_RESPONSE_FAIL error={exc!r}",flush=True); return 2

    closure={"sigma8_dd":0.,"f":0.}; tauvar={q:0. for q in ("sigma8_dd","sigma8_tt","f")}; g3=True
    for tau in TAUS:
        s=str(tau); b=baselines["linear8192"][s]; case=vals[i._key(tau,0.)]
        for iz in range(len(ZEFF)):
            si=i._row(case,iz)["sigma_internal"]; gp=i._row(case,iz)["growth_proxy"]
            rd=abs(b["sigma8_dd"][iz]-si)/max(abs(b["sigma8_dd"][iz]),abs(si),1e-300); rf=abs(b["f"][iz]-gp)/max(abs(b["f"][iz]),abs(gp),1e-300)
            closure["sigma8_dd"]=max(closure["sigma8_dd"],rd); closure["f"]=max(closure["f"],rf); g3 &= rd<=REL_GATE and rf<=REL_GATE
    for iz in range(len(ZEFF)):
        for q in tauvar:
            a=np.asarray([baselines["linear8192"][str(t)][q][iz] for t in TAUS],float); rv=(float(np.max(a))-float(np.min(a)))/max(float(np.max(np.abs(a))),1e-300)
            tauvar[q]=max(tauvar[q],rv); g3 &= rv<=REL_GATE

    resolution={}; g4=True
    for tau in TAUS:
        s=str(tau); resolution[s]={}
        for eps in (EPS_PRIMARY,EPS_CONTROL):
            m12=i.metrics(responses["linear4096"][s][str(eps)]["df"],responses["linear8192"][s][str(eps)]["df"])
            m23=i.metrics(responses["linear8192"][s][str(eps)]["df"],responses["linear16384"][s][str(eps)]["df"])
            resolution[s][str(eps)]={"4096_vs_8192":m12,"8192_vs_16384":m23}; g4 &= metric_pass(m12) and metric_pass(m23)

    epsm={"linear8192":{},"pchip8192":{}}; g5=True
    for tau in TAUS:
        s=str(tau)
        for name in epsm:
            m=i.metrics(responses[name][s][str(EPS_PRIMARY)]["df"],responses[name][s][str(EPS_CONTROL)]["df"]); epsm[name][s]=m; g5 &= metric_pass(m)

    cross={}; g6=True
    for tau in TAUS:
        s=str(tau); cross[s]={}
        for eps in (EPS_PRIMARY,EPS_CONTROL):
            m=i.metrics(responses["linear8192"][s][str(eps)]["df"],responses["pchip8192"][s][str(eps)]["df"]); cross[s][str(eps)]=m; g6 &= metric_pass(m)

    gates={"R9B2J_J1_provenance":True,"R9B2J_J2_common_bounded_grid":bool(g2),"R9B2J_J3_eta0_closure_tau_invariance":bool(g3),
           "R9B2J_J4_response_resolution":bool(g4),"R9B2J_J5_epsilon_consistency":bool(g5),"R9B2J_J6_cross_operator":bool(g6)}
    stageA={"closure_max_rel":closure,"tau_variation_max_rel":tauvar,"resolution_metrics":resolution,"epsilon_metrics":epsm,"cross_operator_metrics":cross,"grid":grid}
    print("STABLE_AEST_DESI_DR1_R9B2J_STAGE_A_GATES="+json.dumps(gates,sort_keys=True),flush=True)
    print("STABLE_AEST_DESI_DR1_R9B2J_STAGE_A_METRICS="+json.dumps({"closure":closure,"tauvar":tauvar,"resolution":resolution,"epsilon":epsm,"cross":cross},sort_keys=True),flush=True)
    fail=None
    if not g2: fail=FAIL_GRID
    elif not g3: fail=FAIL_CLOSURE
    elif not g4: fail=FAIL_RES
    elif not g5: fail=FAIL_EPS
    elif not g6: fail=FAIL_CROSS
    if fail:
        write_json(outpath,{"classification":fail,"diagnostic_complete":True,"science_evaluated":False,"desi_data_loaded":False,"gates":gates,"stageA":stageA,
                            "provenance":prov,"runs":runs,"interpretation":{"historical_failures_reclassified":False,"observational_detection_claim_licensed":False}})
        print("STABLE_AEST_DESI_DR1_R9B2J_CLASSIFICATION="+fail,flush=True); return 1

    print("STABLE_AEST_DESI_DR1_R9B2J_STAGE_A_PASS_LOADING_DESI",flush=True)
    data_loaded=False
    try:
        data_dir=Path(args.data_dir).resolve(); official_repo=Path(args.official_repo).resolve()
        if not data_dir.is_dir() or not official_repo.is_dir(): raise RuntimeError("missing DESI data/repository path")
        bins,d,C,offsets,data_hashes,_=r9b.load_desi(data_dir,official_repo); data_loaded=True
        repo_head=subprocess.check_output(["git","-C",str(official_repo),"rev-parse","HEAD"],text=True).strip(); eig=np.linalg.eigvalsh(C)
        ze=np.asarray([float(b["zeff"]) for b in bins],float)
        k1=bool(repo_head==r9b.DESI_REPO_COMMIT and len(bins)==6 and len(d)==24 and np.allclose(ze,ZEFF,rtol=0,atol=1e-12)
                and np.all(np.isfinite(d)) and np.all(np.isfinite(C)) and np.allclose(C,C.T,rtol=0,atol=1e-12) and np.all(eig>0))
        data_meta={"repo_head":repo_head,"files_sha256":data_hashes,"dimension":int(len(d)),"min_cov_eigenvalue":float(eig.min()),
                   "bins":[{"namespace":b["namespace"],"zeff":b["zeff"],"parameters":b["parameters"]} for b in bins]}
    except Exception as exc:
        k1=False; bins=[]; d=C=offsets=None; data_meta={"error":repr(exc)}
    gates["R9B2J_K1_desi_provenance"]=bool(k1)
    if not k1:
        write_json(outpath,{"classification":FAIL_DATA,"diagnostic_complete":True,"science_evaluated":False,"desi_data_loaded":data_loaded,"gates":gates,
                            "stageA":stageA,"data":data_meta,"provenance":prov,"runs":runs})
        print("STABLE_AEST_DESI_DR1_R9B2J_CLASSIFICATION="+FAIL_DATA,flush=True); return 1

    full={"linear8192":{},"pchip8192":{}}; fullm={"epsilon":{},"cross":{}}
    basevec=i._assemble_baseline(vals[i._key(10.,0.)],baselines["linear8192"]["10.0"]["f"],bins); k2=bool(np.all(np.isfinite(basevec)))
    for tau in TAUS:
        s=str(tau); zc=vals[i._key(tau,0.)]; full["linear8192"][s]={}; full["pchip8192"][s]={}
        for eps in (EPS_PRIMARY,EPS_CONTROL):
            pp,mm=vals[i._key(tau,+eps)],vals[i._key(tau,-eps)]
            for name in ("linear8192","pchip8192"):
                t=i._assemble_tangent(zc,pp,mm,responses[name][s][str(eps)],eps,baselines[name][s],bins); full[name][s][str(eps)]=t; k2 &= np.all(np.isfinite(t))
    gates["R9B2J_K2_source_state_shapefit_vector"]=bool(k2)

    k3=True; k4=True
    for tau in TAUS:
        s=str(tau); m=i.metrics(full["linear8192"][s][str(EPS_PRIMARY)],full["linear8192"][s][str(EPS_CONTROL)]); fullm["epsilon"][s]=m; k3 &= metric_pass(m); fullm["cross"][s]={}
        for eps in (EPS_PRIMARY,EPS_CONTROL):
            mc=i.metrics(full["linear8192"][s][str(eps)],full["pchip8192"][s][str(eps)]); fullm["cross"][s][str(eps)]=mc; k4 &= metric_pass(mc)
    gates["R9B2J_K3_full_tangent_epsilon"]=bool(k3); gates["R9B2J_K4_full_cross_operator"]=bool(k4)

    projection={}; k5=bool(k2 and k3 and k4); k6=bool(k5)
    if k5:
        for tau in TAUS:
            try:
                t=full["linear8192"][str(tau)][str(EPS_PRIMARY)]; p=r9b.projection_summary(d,C,basevec,t,bins,offsets); projection[str(tau)]=p
                k5 &= bool(np.isfinite(p["F_perp"]) and p["F_perp"]>0 and p["projection_idempotence_metric"]<=1e-8)
                a=p["eta_hat_signed_matched_filter"]; b=p["eta_hat_signed_gls"]; k6 &= abs(a-b)<=max(1e-10,1e-8*max(abs(a),abs(b),1.))
            except Exception as exc:
                projection[str(tau)]={"error":repr(exc)}; k5=False; k6=False
    gates["R9B2J_K5_nuisance_projection"]=bool(k5); gates["R9B2J_K6_matched_filter_gls"]=bool(k6)
    if not k2: cls=FAIL_VEC
    elif not k3: cls=FAIL_FULL
    elif not k4: cls=FAIL_FULL_CROSS
    elif not k5: cls=FAIL_PROJ
    elif not k6: cls=FAIL_GLS
    else: cls=PASS

    result={"classification":cls,"diagnostic_complete":True,"science_evaluated":True,"desi_data_loaded":True,"gates":gates,"stageA":stageA,
            "stageB":{"full_tangent_metrics":fullm,"tau_likelihood":projection},"data":data_meta,"provenance":prov,"runs":runs,
            "settings":{"tau_H0_grid":list(TAUS),"eta_grid":list(ETAS),"epsilon_primary":EPS_PRIMARY,"epsilon_control":EPS_CONTROL,"E_gate":E_GATE,"C_gate":C_GATE,
                        "rel_gate":REL_GATE,"primary_response":"signed dP/deta linear in ln(k), 8192 nodes, Simpson","resolution_controls":[4096,16384],
                        "control_response":"signed dP/deta PCHIP in ln(k), 8192 nodes, Simpson","shapefit_power_source":"bounded source-state Pdd; no CLASS pk_cb_lin in R9b2j path",
                        "eta_physical_interval":[r9b.ETA_PHYS_MIN,r9b.ETA_PHYS_MAX]},
            "interpretation":{"historical_failures_reclassified":False,"compressed_full_shape_corrected_projection_reportable":cls==PASS,
                              "observational_detection_claim_licensed":False,"full_EFT_modified_gravity_claim_licensed":False,"tau_bound_claim_licensed":False}}
    write_json(outpath,result)
    arrays={"data":d,"covariance":C,"baseline":basevec}
    for tau in TAUS:
        arrays[f"tangent_tau{tau:g}"]=full["linear8192"][str(tau)][str(EPS_PRIMARY)]; arrays[f"source_df_response_tau{tau:g}"]=responses["linear8192"][str(tau)][str(EPS_PRIMARY)]["df"]
    np.savez_compressed(args.npz_out,**arrays)
    print("STABLE_AEST_DESI_DR1_R9B2J_GATES="+json.dumps(gates,sort_keys=True),flush=True)
    print("STABLE_AEST_DESI_DR1_R9B2J_PROJECTION="+json.dumps(projection,sort_keys=True),flush=True)
    print("STABLE_AEST_DESI_DR1_R9B2J_CLASSIFICATION="+cls,flush=True)
    return 0 if cls==PASS else 1

if __name__=="__main__": raise SystemExit(main())
