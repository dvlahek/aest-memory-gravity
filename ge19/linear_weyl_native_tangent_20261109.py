#!/usr/bin/env python3
"""GE19 LW01: one preregistered native signed Weyl+matter eta tangent in CLASS.

Uses exactly frozen v077 physics, R4 k-sampling, original v075 forcing
recipe and four lambda values. One baseline + four +/- CLASS linear runs.
Does not run H4, change AeST action, fit to observations or overwrite
historical v077 files. --self-test is purely synthetic/no CLASS required.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from v063 import theory_response_map as v63

PRE = ROOT/"ge19/linear_weyl_native_tangent_predata_20261109.json"
SOURCE_BLOBS = {
    "v063/theory_response_map.py":"fb373c8118b755c5aa7d5572d910d6ca3684866e",
    "v075/fourier_k_resolution_closure.py":"6fb6a221bd2bab51c81348033f9cd1289a965fa3",
    "v076/native_node_power_closure.py":"72a2aadb4ee06deb080b5d9a45ffabcf6a43efe1",
    "v077/native_state_tangent_affinity.py":"65a20f40e609315904d179865df9a35da6f78aff",
    "v039/build_tau_forcing.py":"9c859d3131367892f9ee9d809786904a20796f91",
    "v019/ini/aest_exp.ini":"f9a2bde8921a148e063f9657a8ede0a51c6a629d",
}
CLASS_HEAD="e85808324f51fc694d12e3ed7439552a3c3f9540"
LAMBDAS=np.array([10.0,5.0,2.5,1.25],float)
R4={"label":"r4","k_per_decade_for_pk":80.0,"k_per_decade_for_bao":560.0}
REQ_KH=np.array([0.03,0.05,0.08,0.10,0.15,0.20])
H=float(v63.START["H0"])/100.0
AS=float(v63.START["A_s"])
NS=float(v63.START["n_s"])
K_PIVOT=0.05
TINY=1.0e-300


def require(ok,msg):
    if not bool(ok):
        raise RuntimeError("GE19_LW01_"+msg)

def sha256(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda:f.read(1<<20),b""):
            h.update(block)
    return h.hexdigest()

def git(args,cwd):
    return subprocess.check_output(["git",*args],cwd=cwd,text=True).strip()

def norm(x):
    return float(np.linalg.norm(np.asarray(x,dtype=float).reshape(-1)))

def signed_stats(base,plus,minus,lambdas,mask):
    base=np.asarray(base,float)
    plus=np.asarray(plus,float)
    minus=np.asarray(minus,float)
    mask=np.asarray(mask,bool)
    require(plus.shape==minus.shape and plus.shape[1:]==base.shape,
            "TANGENT_ARRAY_SHAPE")
    require(np.count_nonzero(mask)>0 and mask.shape==base.shape,"PRIMARY_MASK")
    t=(plus-minus)/(2*lambdas[:,None,None])
    vals=t[:,mask]
    ref=np.mean(vals,axis=0)
    den=norm(ref)
    affinity=np.array([norm(v-ref)/max(den,TINY) for v in vals])
    cosine=np.array([float(np.dot(v,ref)/max(norm(v)*den,TINY))
                     for v in vals])
    even=np.array([
        norm((plus[i]+minus[i]-2*base)[mask])/
        max(2*abs(lam)*den,TINY)
        for i,lam in enumerate(lambdas)])
    bnorm=norm(base[mask])
    relative=den/max(bnorm,TINY)
    return {
        "tangents":t,
        "mean_full":np.mean(t,axis=0),
        "affinity":affinity,"cosine":cosine,
        "even":even,"mean_norm":den,
        "baseline_norm":bnorm,
        "mean_to_baseline_norm_ratio":relative,
    }

def synthetic_selftest():
    nk,nz=4,3
    base=np.arange(nk*nz,dtype=float).reshape(nk,nz)/10+2
    delta=np.sin(np.arange(nk*nz).reshape(nk,nz)+0.1)*.002
    p=np.array([base+l*delta for l in LAMBDAS])
    m=np.array([base-l*delta for l in LAMBDAS])
    mask=np.ones_like(base,bool)
    stats=signed_stats(base,p,m,LAMBDAS,mask)
    require(np.max(stats["affinity"])<1e-11,"SELFTEST_ODD")
    require(np.max(stats["even"])<1e-11,"SELFTEST_EVEN")
    require(np.allclose(stats["mean_full"],delta,atol=1e-14,rtol=0),
            "SELFTEST_SIGN")
    p[1,0,0]+=.01
    require(float(np.max(signed_stats(base,p,m,LAMBDAS,mask)["affinity"]))>.005,
            "SELFTEST_NEGATIVE")
    print("GE19_LW01_SIGNED_NATIVE_SYNTHETIC_SELFTEST_PASS")

def preflight(class_root):
    require(PRE.is_file(),"PREDATA_MISSING")
    d=json.loads(PRE.read_text())
    require(d["classification"]==
      "GE19_LINEAR_WEYL_NATIVE_20261109_PREDATA_LOCK_BEFORE_EXECUTION",
      "PREDATA_CLASSIFICATION_CHANGED")
    require(d["created_before_result"] is True,"PREDATA_NOT_FROZEN")
    require(d["model"]["eta_tangent_amplifications"]==LAMBDAS.tolist(),
      "LAMBDA_CHANGED")
    require(d["model"]["CLASS_original_commit"]==CLASS_HEAD,"CLASS_PRE_PIN")
    require(d["primary_gates"]["Weyl_signed_additive_lambda_affinity_max"]==.005,
      "GATE_CHANGED")
    blobs={}
    for name,want in SOURCE_BLOBS.items():
        p=ROOT/name
        require(p.exists(),"PARENT_MISSING_"+name)
        head=git(["rev-parse","HEAD:"+name],ROOT)
        work=git(["hash-object",str(p)],ROOT)
        require(head==want and work==want,"PARENT_BLOB_CHANGED_"+name)
        blobs[name]=head
    require(class_root.is_dir(),"CLASS_ROOT_MISSING")
    require((class_root/"class").is_file(),"CLASS_EXE_MISSING")
    require(git(["rev-parse","HEAD"],class_root)==CLASS_HEAD,
            "OFFICIAL_CLASS_COMMIT_CHANGED")
    try:
        import classy
        require(hasattr(classy,"Class"),"PATCHED_CLASSY_UNAVAILABLE")
    except ImportError as e:
        raise RuntimeError(
            "GE19_LW01_CLASSY_MISSING: activate the v077 patched CLASS python environment") from e
    return d,blobs

def forcing_once(class_root,prefix):
    """Namespace-copy of original v075 forcing *recipe*; never touch v075 files."""
    root=ROOT/"results"
    trace=Path(str(prefix)+"_forcing_trace.dat")
    log=Path(str(prefix)+"_forcing_trace.log")
    ini=class_root/(prefix.name+"_forcing_trace.ini")
    summary=Path(str(prefix)+"_forcing_summary.json")
    force=Path(str(prefix)+"_forcing_force.dat")
    for p in (trace,log,ini,summary,force):
        require(not p.exists(),"OUTPUT_EXISTS_"+str(p))
    txt=v63.rewrite_ini(v63.BASE.read_text(),
                        "output/"+prefix.name+"_forcing_trace_")
    # The frozen v077 workflow explicitly uses lensing=no.
    if re.search(r"(?m)^\s*lensing\s*=",txt):
        txt=re.sub(r"(?m)^\s*lensing\s*=\s*\w+\s*$","lensing = no",txt)
    else:
        txt+="\nlensing = no\n"
    txt+="k_output_values = "+", ".join(f"{x:.17g}" for x in REQ_KH)+"\n"
    txt+=f"k_per_decade_for_pk = {R4['k_per_decade_for_pk']:.17g}\n"
    txt+=f"k_per_decade_for_bao = {R4['k_per_decade_for_bao']:.17g}\n"
    ini.write_text(txt)
    env=os.environ.copy()
    env["OMP_NUM_THREADS"]="1"
    env["AEST_OFFLINE_TRACE_FILE"]=str(trace.resolve())
    env.pop("AEST_TANGENT_FORCE_FILE",None)
    env.pop("AEST_TANGENT_LAMBDA",None)
    with log.open("w") as f:
        subprocess.run([str(class_root/"class"),ini.name,
                        str(ROOT/"v019p/pre/p3.pre")],
                       cwd=class_root,env=env,check=True,
                       stdout=f,stderr=subprocess.STDOUT)
    require(trace.is_file() and trace.stat().st_size>0,
            "ORIGINAL_FORCING_TRACE_MISSING")
    subprocess.run([
        sys.executable,str(ROOT/"v039/build_tau_forcing.py"),
        str(trace),"--KB",str(v63.KB),"--tauH0",str(v63.TAUH0),
        "--out-prefix",str(prefix)+"_forcing",
        "--control-order","512","--primary-order","1024",
        "--summary",str(summary)],check=True,cwd=ROOT)
    require(force.is_file() and force.stat().st_size>0 and summary.is_file(),
            "FORCING_OUTPUT_MISSING")
    j=json.loads(summary.read_text())
    return force,j,{"file_sha256":sha256(force),"summary_sha256":sha256(summary),
                    "trace_sha256":sha256(trace)}

def compute_run(force,lam):
    from classy import Class
    keys=("AEST_TANGENT_FORCE_FILE","AEST_TANGENT_LAMBDA")
    saved={k:os.environ.get(k) for k in keys}
    c=None
    try:
        if lam is None:
            for k in keys:os.environ.pop(k,None)
        else:
            os.environ["AEST_TANGENT_FORCE_FILE"]=str(force.resolve())
            os.environ["AEST_TANGENT_LAMBDA"]=str(float(lam))
        os.environ["OMP_NUM_THREADS"]="1"
        pars=dict(v63.class_params())
        pars.update({
            "output":"mPk,mTk","lensing":"no",
            "k_output_values":", ".join(f"{kh*H:.17g}" for kh in REQ_KH),
            "k_per_decade_for_pk":80.0,
            "k_per_decade_for_bao":560.0,
            "P_k_max_h/Mpc":2.0,"z_max_pk":5.0,
        })
        # v075/v077 use fixed requested k in 1/Mpc:
        pars["k_output_values"]=", ".join(f"{kh*H:.17g}" for kh in REQ_KH)
        c=Class()
        c.set(pars)
        c.compute()
        pk,kp,zp=c.get_pk_and_k_and_z(
            nonlinear=False,only_clustering_species=False,h_units=False)
        tk,kt,zt=c.get_transfer_and_k_and_z(
            output_format="class",h_units=False)
        wanted=("phi","psi")
        require(all(k in tk for k in wanted),
                "NO_NATIVE_PHI_PSI_TRANSFER_"+str(sorted(tk)))
        dkey="d_m" if "d_m" in tk else "delta_m"
        require(dkey in tk,"NO_NATIVE_MATTER_TRANSFER")
        kp,kt,zp,zt=map(lambda a:np.asarray(a,float),(kp,kt,zp,zt))
        dm,phi,psi=(np.asarray(tk[k],float).copy()
                    for k in (dkey,"phi","psi"))
        pp=np.asarray(pk,float)
        require(pp.shape==dm.shape==phi.shape==psi.shape==(kp.size,zp.size),
                "CLASS_TRANSFER_ORIENTATION")
        require(kp.shape==kt.shape and zp.shape==zt.shape,
                "NATIVE_KZ_SIZE_MISMATCH")
        gridk=float(np.max(np.abs(kp-kt)/np.maximum(np.abs(kp),TINY)))
        gridz=float(np.max(np.abs(zp-zt)))
        kphys=kt[:,None]
        primordial=AS*(kphys/K_PIVOT)**(NS-1)
        src_power=(2*math.pi**2/kphys**3)*primordial*dm**2
        require(np.isfinite(pp).all() and np.all(pp>0),
                "NATIVE_FOURIER_POWER_NONPOSITIVE")
        p_rel=float(np.max(np.abs(src_power-pp)/np.maximum(pp,TINY)))
        return dict(k=kt,z=zt,dm=dm,phi=phi,psi=psi,
                    weyl=(phi+psi)/2,grid_k_rel=gridk,
                    grid_z_abs=gridz,native_matter_power_rel=p_rel)
    finally:
        if c is not None:
            try:c.struct_cleanup();c.empty()
            except Exception:pass
        for k,v in saved.items():
            if v is None:os.environ.pop(k,None)
            else:os.environ[k]=v

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--self-test",action="store_true")
    ap.add_argument("--class-root",type=Path)
    ap.add_argument("--output-prefix",type=Path,
                    default=ROOT/"results/ge19_linear_weyl_native_tangent_20261109")
    args=ap.parse_args()
    if args.self_test:
        synthetic_selftest()
        return
    require(args.class_root is not None,"CLASS_ROOT_REQUIRED")
    prefix=args.output_prefix.resolve()
    require(prefix.parent.is_dir(),"OUTPUT_PARENT_DIR_MISSING")
    jout=Path(str(prefix)+".json")
    nout=Path(str(prefix)+".npz")
    require(not jout.exists() and not nout.exists(),"FINAL_OUTPUT_EXISTS")
    class_root=args.class_root.resolve()
    predata,blobs=preflight(class_root)
    force,fs,fdig=forcing_once(class_root,prefix)
    fg=predata["primary_gates"]
    fpass=bool(float(fs["relative_L2_control_vs_primary"])<=
                fg["forcing_relative_L2_max"]
               and float(fs["cosine"])>=fg["forcing_cosine_min"])
    print("GE19_LW01_FROZEN_FORCING",fpass,flush=True)
    # STOP if the forcing was not certified: no run of a perturbed state.
    require(fpass,"FROZEN_FORCING_CONTROL_FAIL")
    base=compute_run(force,None)
    pr=[]
    mr=[]
    for lam in LAMBDAS:
        print("GE19_LW01_CLASS_LINEAR_LAMBDA",float(lam),flush=True)
        p=compute_run(force,float(lam))
        m=compute_run(force,-float(lam))
        for z in (p,m):
            require(np.array_equal(z["k"],base["k"]) and
                    np.array_equal(z["z"],base["z"]),
                    "NATIVE_GRID_CHANGED_ACROSS_RUNS")
        pr.append(p)
        mr.append(m)
    k=base["k"]
    z=base["z"]
    mask=( (k[:,None]/H>=.03)&(k[:,None]/H<=.20) &
           (z[None,:]>=.2)&(z[None,:]<=1.5) )
    require(np.any(mask),"EMPTY_V077_NATIVE_WINDOW")
    result={}
    for field in ("dm","phi","psi","weyl"):
        plus=np.stack([r[field] for r in pr])
        minus=np.stack([r[field] for r in mr])
        result[field]=signed_stats(base[field],plus,minus,LAMBDAS,mask)
    gridk=max(r["grid_k_rel"] for r in [base]+pr+mr)
    gridz=max(r["grid_z_abs"] for r in [base]+pr+mr)
    pmax=max(r["native_matter_power_rel"] for r in [base]+pr+mr)
    finite=all(np.isfinite(a[field]).all() for a in [base]+pr+mr
               for field in ("dm","phi","psi","weyl"))
    epsw=float(np.max(result["weyl"]["affinity"]))
    evenw=float(np.max(result["weyl"]["even"]))
    epsm=float(np.max(result["dm"]["affinity"]))
    evenm=float(np.max(result["dm"]["even"]))
    nonzero=float(result["weyl"]["mean_to_baseline_norm_ratio"])>=fg["Weyl_tangent_global_mean_L2_vs_baseline_min"]
    gates=dict(
       forcing_pass=fpass,finite=finite,
       native_k_grid_pass=gridk<=fg["native_k_grid_relative_mismatch_max"],
       native_z_grid_pass=gridz<=fg["native_z_grid_absolute_mismatch_max"],
       matter_power_pass=pmax<=fg["native_source_matter_power_rel_max"],
       weyl_affinity_pass=epsw<=fg["Weyl_signed_additive_lambda_affinity_max"],
       weyl_even_pass=evenw<=fg["Weyl_signed_additive_even_residual_max"],
       matter_affinity_pass=epsm<=fg["matter_signed_additive_lambda_affinity_max"],
       matter_even_pass=evenm<=fg["matter_signed_additive_even_residual_max"],
       weyl_nonzero_numerically_resolved=nonzero)
    good=all(v for key,v in gates.items()
             if key!="weyl_nonzero_numerically_resolved")
    if not good:
        classification="GE19_LINEAR_WEYL_NATIVE_SIGNED_TANGENT_NUMERICAL_FAIL"
    elif not nonzero:
        classification="GE19_LINEAR_WEYL_NATIVE_TANGENT_UNRESOLVED"
    else:
        classification="GE19_LINEAR_WEYL_NATIVE_SIGNED_TANGENT_NUMERICAL_PASS_OBSERVATIONAL_OPEN"
    report={
      "classification":classification,
      "predata_classification":predata["classification"],
      "original_git_blob_locks":blobs,"class_official_HEAD":CLASS_HEAD,
      "forcing_sha256":fdig,
      "scope":{"regime":"linear eta-zero externally forced tangent",
               "native_k_h_per_Mpc_window":[.03,.20],
               "native_z_window":[.2,1.5],
               "n_native_nodes":int(np.count_nonzero(mask)),
               "lambdas":LAMBDAS.tolist(),
               "KB":v63.KB,"tauH0":v63.TAUH0,
               "signed_fields":["phi","psi","(phi+psi)/2","d_m"],
               "same_frozen_parent_class_as_v077":True},
      "diagnostics":{
        "forcing":fs,"k_grid_rel_max":gridk,"z_grid_abs_max":gridz,
        "native_matter_power_max_relative":pmax,
        "weyl_affinity_max":epsw,"weyl_even_max":evenw,
        "matter_affinity_max":epsm,"matter_even_max":evenm,
        "weyl_mean_to_baseline_L2_ratio":result["weyl"]["mean_to_baseline_norm_ratio"],
        "weyl_signed_mean_min":float(np.min(result["weyl"]["mean_full"][mask])),
        "weyl_signed_mean_max":float(np.max(result["weyl"]["mean_full"][mask])),
        "weyl_signed_mean_positive_fraction":
          float(np.mean(result["weyl"]["mean_full"][mask]>0)),
        "weyl_signed_mean_negative_fraction":
          float(np.mean(result["weyl"]["mean_full"][mask]<0)),
        "lambda_affinity_by_field":{f:result[f]["affinity"].tolist() for f in result},
        "even_residual_by_field":{f:result[f]["even"].tolist() for f in result},
      },
      "gates":gates,
      "all_original_v068_failure_unchanged":True,
      "H4_Ward_certified":False,"Z21_certified":False,
      "linear_lensing_prediction_certified":False,
      "observational_detection":False,
      "claim_boundary":"Signed, additive CLASS Newtonian-gauge native Weyl transfer tangent only; no inferred lensing spectrum, ISW, survey significance, or nonlinear solution. No local fractional division near transfer zeros."
    }
    np.savez_compressed(nout,
       k_native_h=k/H,z_native=z,primary_mask=mask,
       lambdas=LAMBDAS,
       weyl_base=base["weyl"],
       weyl_plus=np.stack([r["weyl"] for r in pr]),
       weyl_minus=np.stack([r["weyl"] for r in mr]),
       weyl_tangents=result["weyl"]["tangents"],
       weyl_signed_mean=result["weyl"]["mean_full"],
       matter_base=base["dm"],
       matter_tangents=result["dm"]["tangents"],
       matter_signed_mean=result["dm"]["mean_full"],
       phi_base=base["phi"],psi_base=base["psi"],
       phi_signed_mean=result["phi"]["mean_full"],
       psi_signed_mean=result["psi"]["mean_full"])
    jout.write_text(json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print("GE19_LW01_CLASSIFICATION",classification,flush=True)
    print("GE19_LW01_OUTPUT",jout,nout,flush=True)

if __name__=="__main__":
    main()
