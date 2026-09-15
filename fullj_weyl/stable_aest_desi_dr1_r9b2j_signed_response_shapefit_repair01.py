#!/usr/bin/env python3
from __future__ import annotations

import argparse
import gc
import json
import os
import pickle
import subprocess
import sys
from pathlib import Path

import numpy as np

from fullj_weyl import stable_aest_desi_dr1_r9b2j_signed_response_shapefit as j
from fullj_weyl import stable_aest_desi_dr1_r9b2i_native_variance_response_shapefit as i
from fullj_weyl import stable_aest_desi_dr1_r9b_shapefit_projection as r9b
from fullj_weyl import stable_aest_desi_dr1_r9b2f_full_grid_rogue_node as r9b2f

ROOT = Path(__file__).resolve().parents[1]
REPAIR_PREFIT_LOCK = "040d169407d4bdde0f59f9b15380c3623a5abfe8"
ORIGINAL_PREFIT_LOCK = "dbf354f4ef3122fff44b1b389f1adc839e9e7f9d"
ORIGINAL_IMPL_LOCK = "342ab7d85366e4f4521a7e3e2d19741e878aec3a"
ORIGINAL_RUNNER_LOCK = "2e3bf71cb403e9c31782d2afd142a2c87fe01e79"

ZEFF=j.ZEFF; TAUS=j.TAUS; ETAS=j.ETAS
EPS_PRIMARY=j.EPS_PRIMARY; EPS_CONTROL=j.EPS_CONTROL
REL_GATE=j.REL_GATE; E_GATE=j.E_GATE; C_GATE=j.C_GATE
PASS=j.PASS


def _ckey(tau: float, eta: float) -> str:
    return f"tau{tau:g}_eta{eta:+.3f}"


def _checkpoint_ok(case: dict, tau: float, eta: float) -> bool:
    try:
        if float(case["tau_H0"]) != float(tau) or float(case["eta"]) != float(eta): return False
        rows=case["rows"]
        if len(rows)!=len(ZEFF): return False
        for z,row in zip(ZEFF,rows):
            if abs(float(row["z"])-float(z))>1e-13: return False
            st=row["state"]
            for q in ("kh","pdd","ptt"):
                a=np.asarray(st[q],float)
                if a.ndim!=1 or a.size<32 or not np.all(np.isfinite(a)): return False
            if not (np.all(np.asarray(st["pdd"])>0) and np.all(np.asarray(st["ptt"])>0)): return False
        return True
    except Exception:
        return False


def run_light_case(eta: float, tau: float) -> dict:
    from classy import Class
    p,bits,pos=i._params(float(eta),float(tau)); c=Class(); c.set(p); c.compute()
    try:
        As=float(p["A_s"]); ns=float(p["n_s"])
        meta0={
            "h":float(c.h()), "rdrag":float(c.rs_drag()), "Omega_b":r9b._omega(c,"Omega_b"),
            "Omega_cdm":r9b._omega(c,"Omega_cdm"), "Omega_nu":r9b._omega(c,"Omega_nu",0.0),
            "n_s":float(c.n_s()),
        }
        rows=[]
        for z in ZEFF:
            z=float(z); st=r9b2f._state_at_z(c,z,As,ns)
            si=float(c.sigma(8.0,z,h_units=True)); proxy=float(c.effective_f_sigma8(z,z_step=0.1))/si
            bg=dict(meta0)
            bg.update({"Hubble_Mpc_inv":float(c.Hubble(z)),"angular_distance_Mpc":float(c.angular_distance(z))})
            rows.append({"z":z,"state":st,"sigma_internal":si,"growth_proxy":proxy,"background":bg})
        return {"tau_H0":float(tau),"eta":float(eta),"rows":rows,"bits":int(bits),"target_pos":int(pos)}
    finally:
        c.struct_cleanup(); c.empty()


def worker(args) -> int:
    case=run_light_case(args.eta,args.tau)
    p=Path(args.out); p.parent.mkdir(parents=True,exist_ok=True)
    tmp=p.with_suffix(p.suffix+".tmp")
    with tmp.open("wb") as f: pickle.dump(case,f,protocol=pickle.HIGHEST_PROTOCOL)
    tmp.replace(p)
    print(f"STABLE_AEST_DESI_DR1_R9B2J_REPAIR01_WORKER_PASS tau={args.tau:g} eta={args.eta:+.3f}",flush=True)
    return 0


def source_shape_saved(row: dict, fid, fcache) -> dict:
    from cosmoprimo import Cosmology, PowerSpectrumInterpolator1D
    z=float(row["z"]); st=row["state"]; m0=row["background"]
    h=float(m0["h"]); rdrag=float(m0["rdrag"])
    cosmo=Cosmology(H0=100.*h,Omega_b=float(m0["Omega_b"]),Omega_cdm=float(m0["Omega_cdm"]),
                    Omega_ncdm=float(m0["Omega_nu"]),n_s=float(m0["n_s"]))
    try: cosmo.rs_drag=rdrag*h
    except Exception: pass
    kh=np.asarray(st["kh"],float); pdd=np.asarray(st["pdd"],float)
    pkdd=PowerSpectrumInterpolator1D(kh,pdd,extrap_kmin=float(kh[0]),extrap_kmax=float(kh[-1]))
    filt=fcache[z]["filter"]; filt(pkdd,cosmo=cosmo); pknow=filt.smooth_pk_interpolator()
    s=(rdrag*h)/float(fid.rs_drag); kp=0.03/s; dk=1e-2; kk=kp*np.asarray([1.-dk,1.+dk])
    if kk[0]<=kh[0] or kk[-1]>=kh[-1]: raise RuntimeError(f"ShapeFit pivot outside bounded source support z={z}")
    mm=float(np.diff(np.log(np.asarray(pknow(kk),float)))[0]/np.diff(np.log(kk))[0])
    Ap=float((1./s**3)*np.asarray(pkdd(kp)))
    Hz=float(m0["Hubble_Mpc_inv"])*r9b.C_KM_S; da=float(m0["angular_distance_Mpc"])
    apar=(1.0/(Hz/100.0)/rdrag)/(1.0/float(fid.efunc(z))/float(fid.rs_drag))
    aper=(da/rdrag)/(float(fid.angular_diameter_distance(z))/float(fid.rs_drag))
    fz=fcache[z]
    return {"m":mm,"Ap":Ap,"apar":float(apar),"aper":float(aper),"fid_m":float(fz["m"]),
            "fid_f_sqrt_Ap":float(fz["f_sqrt_Ap"])}


def _write(path: Path,obj: dict):
    path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n")


def main(args) -> int:
    outpath=Path(args.json_out); work=Path(args.workdir); work.mkdir(parents=True,exist_ok=True)
    print("STABLE_AEST_DESI_DR1_R9B2J_REPAIR01_START",flush=True)
    # Exact same provenance and frozen science gates as original R9b2j, plus repair lock.
    g1,prov=j.provenance()
    repair_locks={x:j.ancestor(x) for x in (REPAIR_PREFIT_LOCK,ORIGINAL_PREFIT_LOCK,ORIGINAL_IMPL_LOCK,ORIGINAL_RUNNER_LOCK)}
    g1=bool(g1 and all(repair_locks.values())); prov["repair01_ancestor_locks"]=repair_locks
    if not g1:
        _write(outpath,{"classification":j.FAIL_PROV,"diagnostic_complete":False,"science_evaluated":False,"gates":{"R9B2J_J1_provenance":False},"provenance":prov})
        return 3

    vals={}; runs=[]; mod="fullj_weyl.stable_aest_desi_dr1_r9b2j_signed_response_shapefit_repair01"
    for tau in TAUS:
        for eta in ETAS:
            key=i._key(tau,eta); cp=work/f"{_ckey(tau,eta)}.pkl"
            reused=False
            if cp.is_file():
                try:
                    with cp.open("rb") as f: case=pickle.load(f)
                    if _checkpoint_ok(case,tau,eta): vals[key]=case; reused=True
                except Exception: reused=False
            if not reused:
                print(f"STABLE_AEST_DESI_DR1_R9B2J_REPAIR01_RUN tau={tau:g} eta={eta:+.3f}",flush=True)
                cmd=[sys.executable,"-u","-m",mod,"--worker","--tau",str(tau),"--eta",str(eta),"--out",str(cp)]
                rc=subprocess.run(cmd,env=os.environ.copy()).returncode
                if rc!=0:
                    _write(outpath,{"classification":j.FAIL_RUN,"diagnostic_complete":False,"science_evaluated":False,"error":f"worker exit {rc}","runs":runs,"provenance":prov})
                    return 2
                with cp.open("rb") as f: case=pickle.load(f)
                if not _checkpoint_ok(case,tau,eta):
                    _write(outpath,{"classification":j.FAIL_RUN,"diagnostic_complete":False,"science_evaluated":False,"error":"invalid worker checkpoint","runs":runs,"provenance":prov})
                    return 2
                vals[key]=case
            print(f"STABLE_AEST_DESI_DR1_R9B2J_REPAIR01_CASE_READY tau={tau:g} eta={eta:+.3f} reused={str(reused).lower()}",flush=True)
            runs.append({"tau_H0":tau,"eta":eta,"ok":True,"checkpoint_reused":reused})

    # Stage A is byte-for-byte equivalent in mathematical construction to original R9b2j.
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
                g2 &= healthy; grid.append({"tau_H0":tau,"epsilon":eps,"z":float(z),"same_k":same,"healthy":healthy,"n_k":int(kh.size),"kh_min":float(kh[0]),"kh_max":float(kh[-1])})

    baselines={"linear8192":{},"pchip8192":{}}; responses={x:{} for x in ("linear4096","linear8192","linear16384","pchip8192")}
    for tau in TAUS:
        s=str(tau); zc=vals[i._key(tau,0.)]
        baselines["linear8192"][s]=j.baseline(zc,"linear",8192); baselines["pchip8192"][s]=j.baseline(zc,"pchip",8192)
        for name,mode,n in (("linear4096","linear",4096),("linear8192","linear",8192),("linear16384","linear",16384),("pchip8192","pchip",8192)):
            responses[name][s]={}
            for eps in (EPS_PRIMARY,EPS_CONTROL): responses[name][s][str(eps)]=j.response(zc,vals[i._key(tau,+eps)],vals[i._key(tau,-eps)],eps,mode,n)

    closure={"sigma8_dd":0.,"f":0.}; tauvar={q:0. for q in ("sigma8_dd","sigma8_tt","f")}; g3=True
    for tau in TAUS:
        s=str(tau); b=baselines["linear8192"][s]; case=vals[i._key(tau,0.)]
        for iz in range(len(ZEFF)):
            si=i._row(case,iz)["sigma_internal"]; gp=i._row(case,iz)["growth_proxy"]
            rd=abs(b["sigma8_dd"][iz]-si)/max(abs(b["sigma8_dd"][iz]),abs(si),1e-300); rf=abs(b["f"][iz]-gp)/max(abs(b["f"][iz]),abs(gp),1e-300)
            closure["sigma8_dd"]=max(closure["sigma8_dd"],rd); closure["f"]=max(closure["f"],rf); g3 &= rd<=REL_GATE and rf<=REL_GATE
    for iz in range(len(ZEFF)):
        for q in tauvar:
            a=np.asarray([baselines["linear8192"][str(t)][q][iz] for t in TAUS]); rv=(float(np.max(a))-float(np.min(a)))/max(float(np.max(np.abs(a))),1e-300)
            tauvar[q]=max(tauvar[q],rv); g3 &= rv<=REL_GATE

    resolution={}; g4=True
    for tau in TAUS:
        s=str(tau); resolution[s]={}
        for eps in (EPS_PRIMARY,EPS_CONTROL):
            m12=i.metrics(responses["linear4096"][s][str(eps)]["df"],responses["linear8192"][s][str(eps)]["df"])
            m23=i.metrics(responses["linear8192"][s][str(eps)]["df"],responses["linear16384"][s][str(eps)]["df"])
            resolution[s][str(eps)]={"4096_vs_8192":m12,"8192_vs_16384":m23}; g4 &= j.metric_pass(m12) and j.metric_pass(m23)
    epsm={"linear8192":{},"pchip8192":{}}; g5=True
    for tau in TAUS:
        s=str(tau)
        for name in epsm:
            m=i.metrics(responses[name][s][str(EPS_PRIMARY)]["df"],responses[name][s][str(EPS_CONTROL)]["df"]); epsm[name][s]=m; g5 &= j.metric_pass(m)
    cross={}; g6=True
    for tau in TAUS:
        s=str(tau); cross[s]={}
        for eps in (EPS_PRIMARY,EPS_CONTROL):
            m=i.metrics(responses["linear8192"][s][str(eps)]["df"],responses["pchip8192"][s][str(eps)]["df"]); cross[s][str(eps)]=m; g6 &= j.metric_pass(m)

    gates={"R9B2J_J1_provenance":True,"R9B2J_J2_common_bounded_grid":bool(g2),"R9B2J_J3_eta0_closure_tau_invariance":bool(g3),"R9B2J_J4_response_resolution":bool(g4),"R9B2J_J5_epsilon_consistency":bool(g5),"R9B2J_J6_cross_operator":bool(g6)}
    stageA={"closure_max_rel":closure,"tau_variation_max_rel":tauvar,"resolution_metrics":resolution,"epsilon_metrics":epsm,"cross_operator_metrics":cross,"grid":grid}
    print("STABLE_AEST_DESI_DR1_R9B2J_REPAIR01_STAGE_A_GATES="+json.dumps(gates,sort_keys=True),flush=True)
    fail=None
    if not g2: fail=j.FAIL_GRID
    elif not g3: fail=j.FAIL_CLOSURE
    elif not g4: fail=j.FAIL_RES
    elif not g5: fail=j.FAIL_EPS
    elif not g6: fail=j.FAIL_CROSS
    if fail:
        _write(outpath,{"classification":fail,"diagnostic_complete":True,"science_evaluated":False,"desi_data_loaded":False,"gates":gates,"stageA":stageA,"provenance":prov,"runs":runs,"repair01":True})
        print("STABLE_AEST_DESI_DR1_R9B2J_REPAIR01_CLASSIFICATION="+fail,flush=True); return 1

    print("STABLE_AEST_DESI_DR1_R9B2J_REPAIR01_STAGE_A_PASS_LOADING_DESI",flush=True)
    try:
        data_dir=Path(args.data_dir).resolve(); official_repo=Path(args.official_repo).resolve()
        bins,d,C,offsets,data_hashes,_=r9b.load_desi(data_dir,official_repo)
        repo_head=subprocess.check_output(["git","-C",str(official_repo),"rev-parse","HEAD"],text=True).strip(); eig=np.linalg.eigvalsh(C)
        ze=np.asarray([float(b["zeff"]) for b in bins],float)
        k1=bool(repo_head==r9b.DESI_REPO_COMMIT and len(bins)==6 and len(d)==24 and np.allclose(ze,ZEFF,rtol=0,atol=1e-12)
                and np.all(np.isfinite(d)) and np.all(np.isfinite(C)) and np.allclose(C,C.T,rtol=0,atol=1e-12) and np.all(eig>0))
        data_meta={"repo_head":repo_head,"files_sha256":data_hashes,"dimension":int(len(d)),"min_cov_eigenvalue":float(eig.min())}
    except Exception as exc:
        k1=False; data_meta={"error":repr(exc)}
    gates["R9B2J_K1_desi_provenance"]=k1
    if not k1:
        _write(outpath,{"classification":j.FAIL_DATA,"diagnostic_complete":True,"science_evaluated":False,"gates":gates,"stageA":stageA,"data":data_meta,"runs":runs,"repair01":True}); return 1

    # Construct fiducial/CAMB cache once, after every CLASS worker has exited.
    fid,fcache=r9b._get_fiducial_cache(ZEFF)
    for case in vals.values():
        for row in case["rows"]: row["shape"]=source_shape_saved(row,fid,fcache)
        gc.collect()

    full={"linear8192":{},"pchip8192":{}}; fullm={"epsilon":{},"cross":{}}
    basevec=i._assemble_baseline(vals[i._key(10.,0.)],baselines["linear8192"]["10.0"]["f"],bins); k2=bool(np.all(np.isfinite(basevec)))
    for tau in TAUS:
        s=str(tau); zc=vals[i._key(tau,0.)]; full["linear8192"][s]={}; full["pchip8192"][s]={}
        for eps in (EPS_PRIMARY,EPS_CONTROL):
            pp,mm=vals[i._key(tau,+eps)],vals[i._key(tau,-eps)]
            for name in ("linear8192","pchip8192"):
                t=i._assemble_tangent(zc,pp,mm,responses[name][s][str(eps)],eps,baselines[name][s],bins); full[name][s][str(eps)]=t; k2 &= bool(np.all(np.isfinite(t)))
    gates["R9B2J_K2_source_state_shapefit_vector"]=k2
    k3=True; k4=True
    for tau in TAUS:
        s=str(tau); m=i.metrics(full["linear8192"][s][str(EPS_PRIMARY)],full["linear8192"][s][str(EPS_CONTROL)]); fullm["epsilon"][s]=m; k3 &= j.metric_pass(m); fullm["cross"][s]={}
        for eps in (EPS_PRIMARY,EPS_CONTROL):
            mc=i.metrics(full["linear8192"][s][str(eps)],full["pchip8192"][s][str(eps)]); fullm["cross"][s][str(eps)]=mc; k4 &= j.metric_pass(mc)
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
    if not k2: cls=j.FAIL_VEC
    elif not k3: cls=j.FAIL_FULL
    elif not k4: cls=j.FAIL_FULL_CROSS
    elif not k5: cls=j.FAIL_PROJ
    elif not k6: cls=j.FAIL_GLS
    else: cls=PASS

    result={"classification":cls,"diagnostic_complete":True,"science_evaluated":True,"desi_data_loaded":True,"gates":gates,"stageA":stageA,
            "stageB":{"full_tangent_metrics":fullm,"tau_likelihood":projection},"data":data_meta,"provenance":prov,"runs":runs,"repair01":True,
            "settings":{"process_isolation":"one CLASS subprocess per tau/eta with resumable checkpoints","shape_cache":"single post-Stage-A fiducial/CAMB cache",
                        "science_definition":"unchanged from R9b2j preregistration"},
            "interpretation":{"historical_failures_reclassified":False,"compressed_full_shape_corrected_projection_reportable":cls==PASS,"observational_detection_claim_licensed":False}}
    _write(outpath,result)
    arrays={"data":d,"covariance":C,"baseline":basevec}
    for tau in TAUS:
        arrays[f"tangent_tau{tau:g}"]=full["linear8192"][str(tau)][str(EPS_PRIMARY)]
    np.savez_compressed(args.npz_out,**arrays)
    print("STABLE_AEST_DESI_DR1_R9B2J_REPAIR01_GATES="+json.dumps(gates,sort_keys=True),flush=True)
    print("STABLE_AEST_DESI_DR1_R9B2J_REPAIR01_PROJECTION="+json.dumps(projection,sort_keys=True),flush=True)
    print("STABLE_AEST_DESI_DR1_R9B2J_REPAIR01_CLASSIFICATION="+cls,flush=True)
    return 0 if cls==PASS else 1


if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--worker",action="store_true"); ap.add_argument("--tau",type=float); ap.add_argument("--eta",type=float); ap.add_argument("--out")
    ap.add_argument("--data-dir",default=""); ap.add_argument("--official-repo",default=""); ap.add_argument("--json-out",default="results/stable_aest_desi_dr1_r9b2j_signed_response_shapefit_repair01.json")
    ap.add_argument("--npz-out",default="results/stable_aest_desi_dr1_r9b2j_signed_response_shapefit_repair01.npz"); ap.add_argument("--workdir",default="results/stable_aest_desi_dr1_r9b2j_repair01_work")
    args=ap.parse_args()
    if args.worker:
        if args.tau is None or args.eta is None or not args.out: raise SystemExit("worker requires --tau --eta --out")
        raise SystemExit(worker(args))
    raise SystemExit(main(args))