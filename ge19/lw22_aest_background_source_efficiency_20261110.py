#!/usr/bin/env python3
"""GE19 LW22: REAL DES Y3 NZ_SOURCE × frozen AeST CLASS chi(z) geometry.

One ORIGINAL patched CLASS background-only calculation, no perturbative
CLASS output, no new theory sweep, no DES observed GAMMAT or covariance.
This builds the physical geometric source efficiency g_s(z_L) on the
original MagLim lens redshift grid; it is not a full GGL observable.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from pathlib import Path

import numpy as np
from ge19 import lw21b_signed_source_geometry_sensitivity_20261110 as nzlib
from v063 import theory_response_map as v63

ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/"ge19/lw22_des_y3_source_lensing_efficiency_predata_20261110.json"
PRE_BLOB="b884ea402dc05ae486c6da008ebb7b19600d8dc2"
LW21B=ROOT/"results/ge19_lw21b_signed_source_geometry_sensitivity_20261110_r1.json"
LW21B_SHA="0223b698b13b1a36736274d6582889d66f7cf500ffe0b13eed40612fa4272de8"
LW02=ROOT/"results/ge19_lw02_windowed_lensing_20261109.json"
LW02_SHA="1aec3ddcbe84e473dbb5edb5640cf923ac1db4d9fb1fe37ab32424bd4d05f086"
SOURCES={
 "ge19/lw21b_signed_source_geometry_sensitivity_20261110.py":
    "1ba3d33a6a8ea892c5251f8bcde203e76436e3fd",
 "v063/theory_response_map.py":
    "fb373c8118b755c5aa7d5572d910d6ca3684866e",
}
ORIGINAL_CLASS_HEAD="e85808324f51fc694d12e3ed7439552a3c3f9540"
FITS_SHA="83efa43f6609ff07248b9c4e411b9ab386ec569cba402364fb21edff456e8b76"

def require(cond,tag):
    if not bool(cond):
        raise RuntimeError("GE19_LW22_"+tag)

def blob(p):
    return subprocess.check_output(["git","hash-object",str(p)],text=True).strip()

def sha(p):
    h=hashlib.sha256()
    with Path(p).open("rb") as f:
        for part in iter(lambda:f.read(1<<20),b""):
            h.update(part)
    return h.hexdigest()

def gaussian_source_efficiency(zlens,chilens,zs,raw_source,zbg,chibg,order):
    """g_s at each lens point; signed source weights kept intact.

    Integrates exact *linearized FITS* n(z) times (chi_s-chi_l)/chi_s.
    Background chi is linearly interpolated on the *original complete
    CLASS background* grid. Gauss 8 vs 16 checks integration stability,
    not the cosmology or survey model accuracy.
    """
    nodes,weights=np.polynomial.legendre.leggauss(order)
    zs=np.asarray(zs,float)
    y=np.asarray(raw_source,float)
    norm=float(np.trapezoid(y,zs))
    require(np.isfinite(norm) and norm>0,"SOURCE_SIGNED_TOTAL")
    require(np.all(np.diff(zs)>0) and
            zs[0]>=zbg[0] and zs[-1]<=zbg[-1],
            "SOURCE_OUTSIDE_CLASS_BACKGROUND")
    vals=np.empty_like(zlens,dtype=float)
    for i,(zL,chiL) in enumerate(zip(zlens,chilens)):
        lo=max(float(zL),float(zs[0]))
        if lo>=zs[-1]:
            vals[i]=0.
            continue
        knots=np.r_[lo,zs[(zs>lo)&(zs<zs[-1])],zs[-1]]
        left,right=knots[:-1],knots[1:]
        x=(left[:,None]+right[:,None])/2.+(right-left)[:,None]*nodes/2.
        chis=np.interp(x,zbg,chibg)
        require(np.all(chis>0) and np.isfinite(chis).all(),"CHI_SOURCE_NOT_POSITIVE")
        kern=(1.-chiL/chis)
        require(np.all(kern>=-1.e-10) and np.all(kern<=1.+1.e-10),
                "NONPHYSICAL_CHI_ORDER")
        ni=np.interp(x,zs,y)
        vals[i]=np.sum((right-left)[:,None]*weights*ni*kern/2.)/norm
    require(np.isfinite(vals).all(),"SOURCE_EFFICIENCY_NONFINITE")
    return vals

def synthetic_selftest():
    # Exact analytic illustration: chi(z)=z, lens z uniform [0,1],
    # sources z uniform [1,2]. Average source efficiency:
    # int dL (1-L ln2) = 1-.5 ln2.
    zbg=np.linspace(0.,2.,501);chibg=zbg.copy()
    zl=np.linspace(0.,1.,101);chil=zl.copy()
    zs=np.linspace(1.,2.,201);ns=np.ones_like(zs)
    g=gaussian_source_efficiency(zl,chil,zs,ns,zbg,chibg,16)
    ref=1.-0.5*np.log(2.)
    require(abs(float(np.trapezoid(g,zl))-ref)<2.e-7,
            "ANALYTIC_UNIFORM_GEOMETRY")
    near=gaussian_source_efficiency(
        np.array([1.5]),np.array([1.5]),
        np.linspace(0.,1.,101),np.ones(101),
        zbg,chibg,8)
    require(abs(float(near[0]))<1.e-14,"SOURCE_ALL_IN_FRONT")
    signed=ns.copy();signed[0]=-0.2
    audit=nzlib.audit(zs,signed,"SYNTHETIC_SIGNED_SOURCE")
    raw=gaussian_source_efficiency(zl,chil,zs,signed,zbg,chibg,16)
    pos=gaussian_source_efficiency(zl,chil,zs,np.maximum(signed,0),zbg,chibg,16)
    require(np.max(np.abs(raw-pos))<=
            audit["max_signed_vs_positive_normalized_event_discrepancy"]+1.e-10,
            "SIGNED_SOURCE_TV_BOUND")
    require(audit["exceeds_original_LW21_1e_minus4_limit"],
            "ORIGINAL_LW21_HARD_FAIL_PRESERVED")
    print("GE19_LW22_AEST_SOURCE_EFFICIENCY_SYNTHETIC_SELFTEST_PASS 4",flush=True)

def load_background(class_root):
    class_root=Path(class_root).expanduser().resolve()
    require((class_root/"class").is_file(),"CLASS_EXECUTABLE_MISSING")
    head=subprocess.check_output(["git","-C",str(class_root),"rev-parse","HEAD"],
                                 text=True).strip()
    require(head==ORIGINAL_CLASS_HEAD,"ORIGINAL_CLASS_HEAD_MISMATCH")
    from classy import Class
    pars=dict(v63.class_params())
    require(pars["aest_enabled"]=="yes"
            and pars["aest_memory_enabled"]=="no"
            and float(pars["aest_eta"])==0.0,
            "FROZEN_AEST_PARAMS_CHANGED")
    pars.pop("output",None)
    pars.pop("z_max_pk",None)
    pars.pop("P_k_max_h/Mpc",None)
    pars["lensing"]="no"
    keys=("AEST_TANGENT_FORCE_FILE","AEST_TANGENT_LAMBDA",
          "AEST_OFFLINE_TRACE_FILE")
    saved={k:os.environ.pop(k,None) for k in keys}
    c=None
    try:
        c=Class()
        c.set(pars)
        c.compute()
        bg=c.get_background()
        require("z" in bg and "comov. dist." in bg,
                "ORIGINAL_CLASS_BACKGROUND_MISSING")
        z=np.asarray(bg["z"],float)
        chi=np.asarray(bg["comov. dist."],float)
        ix=np.argsort(z)
        z,chi=z[ix],chi[ix]
        require(z.ndim==1 and z.size>100 and
                np.all(np.isfinite(z)) and np.all(np.isfinite(chi)) and
                np.all(np.diff(z)>0),"CLASS_BACKGROUND_GRID_INVALID")
        return z,chi,head
    finally:
        if c is not None:
            try:c.struct_cleanup();c.empty()
            except Exception:pass
        for k,v in saved.items():
            if v is not None:os.environ[k]=v

def integrated_lens_efficiency(zl,lens,eff,lower=None,upper=None):
    z=np.asarray(zl,float);y=np.asarray(lens,float)
    a=max(float(z[0]),float(lower)) if lower is not None else float(z[0])
    b=min(float(z[-1]),float(upper)) if upper is not None else float(z[-1])
    if b<=a:return 0.
    inner=z[(z>a)&(z<b)]
    x=np.r_[a,inner,b]
    val=np.interp(x,z,y)*np.interp(x,z,eff)
    return float(np.trapezoid(val,x)/np.trapezoid(y,z))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--self-test",action="store_true")
    ap.add_argument("--class-root",type=Path)
    ap.add_argument("--fits",type=Path)
    ap.add_argument("--out",type=Path,default=ROOT/
      "results/ge19_lw22_des_y3_source_efficiency_20261110_r1.json")
    arg=ap.parse_args()
    if arg.self_test:
        synthetic_selftest();return
    require(arg.class_root is not None,"CLASS_ROOT_REQUIRED")
    require(arg.fits is not None and arg.fits.is_file(),"ORIGINAL_DES_FITS_REQUIRED")
    require(blob(PRE)==PRE_BLOB,"PRELOCK_CHANGED")
    for f,expected in SOURCES.items():
        require(blob(ROOT/f)==expected,"SOURCE_BLOB_CHANGED_"+Path(f).name)
    require(LW21B.is_file() and sha(LW21B)==LW21B_SHA,
            "LW21B_RESEARCHER_SHA_CHANGED")
    # Cross-check the complete SHA-256 against the immutable pre-data freeze.
    frozen_lw02=json.loads(PRE.read_text())["exact_frozen_inputs"][
        "results/ge19_lw02_windowed_lensing_20261109.json_sha256"]
    require(len(LW02_SHA)==64 and LW02_SHA==frozen_lw02,
            "ORIGINAL_LW02_SHA_PRELOCK_MISMATCH")
    require(LW02.is_file(),"ORIGINAL_LW02_GEOMETRY_FILE_MISSING")
    actual_lw02_sha=sha(LW02)
    print("GE19_LW22_LW02_SHA256_AUDIT",json.dumps({
        "path":str(LW02),"expected":LW02_SHA,"actual":actual_lw02_sha
    },sort_keys=True),flush=True)
    require(actual_lw02_sha==LW02_SHA,
            "ORIGINAL_LW02_GEOMETRY_SHA_CHANGED")
    require(sha(arg.fits)==FITS_SHA,"ORIGINAL_FITS_SHA_CHANGED")
    pre=json.loads(PRE.read_text())
    require(pre["classification"]==
      "GE19_LW22_DES_MAGLIM4_SOURCE_LENSING_EFFICIENCY_GEOMETRY_FREEZE",
      "FROZEN_PRECLASS_CHANGED")
    target=arg.out.resolve()
    npz=target.with_suffix(".npz")
    require(target.parent.is_dir() and not target.exists() and
            not npz.exists(),"OUTPUT_PREEXISTS_OR_DIR_MISSING")
    data=nzlib.read_two_nz_hdus(arg.fits)
    zl,lenses=data["NZ_LENS"]
    zs,sources=data["NZ_SOURCE"]
    require(len(lenses)==6 and len(sources)==4,
            "DES_NZ_BIN_COUNTS_CHANGED")
    for binid,raw in lenses.items():
        nzlib.audit(zl,raw,"NZ_LENS_BIN"+str(binid),positive_only=True)
    for binid,raw in sources.items():
        nzlib.audit(zs,raw,"NZ_SOURCE_BIN"+str(binid))
    bgz,bgchi,head=load_background(arg.class_root)
    valid=((bgz<=max(float(zs[-1]),float(zl[-1]))))
    require(np.any(valid) and np.all(np.diff(bgchi[valid])>0)
            and min(float(zl[0]),float(zs[0]))>=bgz[0]
            and max(float(zl[-1]),float(zs[-1]))<=bgz[-1],
            "CLASS_CHI_NOT_MONOTONIC_OR_COVERED")
    native=json.loads(LW02.read_text())["class_geometry"]
    zn=np.asarray(native["window_native_z"],float)
    oldchi=np.asarray(native["window_chi_Mpc"],float)
    newchi=np.interp(zn,bgz,bgchi)
    rel=float(np.max(np.abs(newchi-oldchi)/np.maximum(oldchi,1.e-12)))
    require(rel<=1.e-4,"CLASS_BACKGROUND_MISMATCH_LW02")
    chil=np.interp(zl,bgz,bgchi)
    lw07=json.loads((ROOT/"results/ge19_lw07b_des_y3_nz_only_audit_20261109.json").read_text())
    bounds=[r for r in lw07["rows"] if
            r["sample"]=="MagLim" and r["bin_1based"]==4]
    require(len(bounds)==1,"ORIGINAL_LENS_BIN4_NOT_FOUND")
    byell={x["ell"]:x for x in bounds[0]["per_ell"]}
    gmap={}
    summaries=[]
    for sourcebin in sorted(sources):
        y=sources[sourcebin]
        audit=nzlib.audit(zs,y,"NZ_SOURCE_BIN"+str(sourcebin))
        gp=np.maximum(y,0.)
        g8=gaussian_source_efficiency(zl,chil,zs,y,bgz,bgchi,8)
        g16=gaussian_source_efficiency(zl,chil,zs,y,bgz,bgchi,16)
        pos16=gaussian_source_efficiency(zl,chil,zs,gp,bgz,bgchi,16)
        maxint=float(np.max(np.abs(g16-g8)))
        maxsigned=float(np.max(np.abs(g16-pos16)))
        bound=audit["max_signed_vs_positive_normalized_event_discrepancy"]
        require(maxint<=1.e-5,"SOURCE_GEOMETRY_QUAD_UNRESOLVED_BIN"+str(sourcebin))
        require(maxsigned<=bound+2.e-6,"SIGNEDNESS_BOUND_FAIL_BIN"+str(sourcebin))
        gmap["efficiency_source"+str(sourcebin)+"_signed"]=g16
        gmap["efficiency_source"+str(sourcebin)+"_positive_diagnostic"]=pos16
        full=integrated_lens_efficiency(zl,lenses[4],g16)
        nodes=[]
        for ell in (100,150,200,300):
            interval=byell[ell]
            lower,upper=interval["supported_z_lower"],interval["supported_z_upper"]
            part=integrated_lens_efficiency(zl,lenses[4],g16,lower,upper) if lower is not None else 0.
            nodes.append({"ell":ell,"lens_weighted_efficiency_native_interval":part,
                          "lens_weighted_efficiency_outside_interval":full-part,
                          "fraction_lens_weighted_efficiency_within_native_interval":
                              part/full if full>0 else None})
        summaries.append({
          "source_bin":sourcebin,
          "source_signedness_negative_ratio":audit["epsilon_B_over_A"],
          "source_signedness_TV_bound":bound,
          "max_lens_node_signed_vs_plus_efficiency_difference":maxsigned,
          "max_lens_node_Gauss8_vs_Gauss16_absolute_difference":maxint,
          "lens_weighted_full_source_efficiency":full,
          "per_ell":nodes,
        })
        print("GE19_LW22_SOURCE_EFFICIENCY",
              sourcebin,"FULL",f"{full:.9g}",
              "QUAD_DIFF",f"{maxint:.3g}",flush=True)
    np.savez_compressed(npz,lens_z=zl,lens_chi_Mpc=chil,
                        source_z=zs,**gmap)
    result={
      "classification":
        "GE19_LW22_AEST_BACKGROUND_SOURCE_EFFICIENCY_GEOMETRY_PASS_FULL_GGL_PHYSICAL_FORWARD_OPEN",
      "predata_git_blob_sha1":PRE_BLOB,
      "original_LW21B_WSL_SHA256":LW21B_SHA,
      "original_LW02_geometry_SHA256":LW02_SHA,
      "original_fits_SHA256":FITS_SHA,
      "original_patched_CLASS_HEAD":head,
      "max_relative_original_LW02_chi_difference":rel,
      "class_background_redshift_points":int(len(bgz)),
      "background_only_run_without_perturbation_output":True,
      "primary_lens_bin":4,
      "primary_source_bin":4,
      "source_bin_summaries":summaries,
      "npz_kernel_path":str(npz),
      "npz_kernel_SHA256":sha(npz),
      "full_GGL_gammat_prediction_calculated":False,
      "physical_P_deltaW_eta_response_certified":False,
      "source_signedness_LW21_hard_fail_preserved":True,
      "DES_gamma_t_and_covariance_read":False,
      "Asimov_forecast_and_detection":False,
      "LW05_cosmic_shear_LOS_BLOCK_preserved":True,
      "LW08_antisymmetric_response_UNRESOLVED":True,
      "H4_Z21_certified":False,
      "scientific_limit":"Aest original frozen chi(z) times calibrated DES NZ_SOURCE geometry only. Native k/z limit is not a bound on GGL signal because physical P_deltaW/bias/IA/angular windows remain absent.",
    }
    target.write_text(json.dumps(result,indent=2,sort_keys=True,
                                 allow_nan=False)+"\n")
    print("GE19_LW22_CLASSIFICATION",result["classification"],flush=True)
    print("GE19_LW22_PHYSICAL_GGL_FORWARD_READY",False,flush=True)
    print("GE19_LW22_OUTPUT",target,flush=True)

if __name__=="__main__":
    main()
