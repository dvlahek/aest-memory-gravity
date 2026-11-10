#!/usr/bin/env python3
"""GE19 LW21B: signed DES Y3 source n(z) response sensitivity diagnostic.

Reports side-by-side event integrals with the original signed source
weight and a positive-part comparison, plus an exact total-variation
upper bound. DOES NOT change the frozen LW21 <=1e-4 positivity gate,
relabel its failed WSL run PASS, read DES shear/covariance, or produce
a lensing observable/detection. Source arrays can be signed response
estimates, not literal probability densities.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/"ge19/lw21b_signed_source_sensitivity_predata_20261110.json"
PRE_BLOB="7537ac59c928dacc368f2c46c359721449d99cc4"
LW07=ROOT/"results/ge19_lw07b_des_y3_nz_only_audit_20261109.json"
LW07_BLOB="5323b8457cbe7e7426c3e6eb4345183c3660cbff"
LW20=ROOT/"results/ge19_lw20_ggl_preforecast_support_20261110_r1.json"
LW20_SHA="ab0b0147b4edf1a12d182628f81476e2d23443e347fe636243d51007eca962a4"
ORIG_LW21=ROOT/"ge19/lw21_des_y3_maglim4_source_behind_20261110.py"
ORIG_LW21_BLOB="cbaf749fba53be7ae612c46f8e97488d1864d4cc"
POLICY=ROOT/"ge19/lw21_nz_signedness_handling_erratum_20261110.json"
POLICY_BLOB="4cd19e0ed232a0c7fe8c5673cafdc7d4c7ff4cf4"
GAUSS_X,GAUSS_W=np.polynomial.legendre.leggauss(4)

def need(ok,label):
    if not bool(ok):
        raise RuntimeError("GE19_LW21B_"+label)

def gitblob(p):
    return subprocess.check_output(["git","hash-object",str(p)],text=True).strip()

def sha256(p):
    h=hashlib.sha256()
    with Path(p).open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):
            h.update(b)
    return h.hexdigest()

def audit(z,y,label,positive_only=False):
    z=np.asarray(z,float)
    y=np.asarray(y,float)
    need(z.ndim==1 and z.size>=6 and y.shape==z.shape,"BAD_ARRAY_"+label)
    need(np.isfinite(z).all() and np.isfinite(y).all() and
         np.all(np.diff(z)>0),"BAD_VALUES_"+label)
    A=float(np.trapezoid(np.maximum(y,0.),z))
    B=float(np.trapezoid(np.maximum(-y,0.),z))
    signed=float(np.trapezoid(y,z))
    need(np.isfinite(A+B+signed) and A>B>=0 and signed>0,
         "UNNORMALIZABLE_"+label)
    if positive_only:
        need(B==0,"LENS_DISTRIBUTION_SIGNED_"+label)
    e=B/A
    return {
        "label":label,
        "samples":int(y.size),
        "min":float(y.min()),
        "negative_values":int(np.count_nonzero(y<0)),
        "positive_area":A,
        "negative_area":B,
        "signed_area":signed,
        "epsilon_B_over_A":e,
        "max_signed_vs_positive_normalized_event_discrepancy":e/(1.-e),
        "exceeds_original_LW21_1e_minus4_limit":bool(e>1.e-4),
    }

def survival_signed(q,z,y):
    """Original signed n(z) survival. No clipping to [0,1]."""
    z=np.asarray(z,float);y=np.asarray(y,float);q=np.asarray(q,float)
    span=np.diff(z)
    integ=np.r_[0.,np.cumsum(span*(y[:-1]+y[1:])/2.)]
    norm=integ[-1]
    need(norm>0,"NEGATIVE_SIGNED_TOTAL")
    ix=np.clip(np.searchsorted(z,q,side="right")-1,0,len(z)-2)
    u=q-z[ix]
    slope=(y[ix+1]-y[ix])/span[ix]
    cumul=(integ[ix]+y[ix]*u+0.5*slope*u*u)/norm
    return np.where(q<=z[0],1.,np.where(q>=z[-1],0.,1.-cumul))

def pair_integral(zl,nl,zs,ns,left=None,right=None):
    """Exact for piecewise-linear input densities, including signed source."""
    zl=np.asarray(zl,float);nl=np.asarray(nl,float)
    zs=np.asarray(zs,float);ns=np.asarray(ns,float)
    lo=max(float(zl[0]),float(left) if left is not None else float(zl[0]))
    hi=min(float(zl[-1]),float(right) if right is not None else float(zl[-1]))
    if lo>=hi: return 0.
    knots=np.unique(np.r_[
        lo,zl[(zl>lo)&(zl<hi)],zs[(zs>lo)&(zs<hi)],hi
    ])
    a,b=knots[:-1],knots[1:]
    grid=(a[:,None]+b[:,None])/2.+(b-a)[:,None]*GAUSS_X/2.
    v=np.interp(grid,zl,nl)*survival_signed(grid,zs,ns)
    result=float(np.sum((b-a)[:,None]*GAUSS_W*v/2.)/
                 np.trapezoid(nl,zl))
    need(np.isfinite(result),"NONFINITE_PAIR_INTEGRAL")
    return result

def synthetic_tests():
    z=np.linspace(0.,1.,41)
    v=np.ones_like(z)
    need(abs(pair_integral(z,v,z,v)-0.5)<1.e-12,"HALF")
    need(abs(pair_integral(z,v,z,v,.25,.75)-.25)<1.e-12,
         "SUBINTERVAL")
    s=np.linspace(0.,1.,41)
    src=np.ones_like(s)
    src[0]=-0.0166 # a deliberate signed source-response ordinate
    out=audit(s,src,"SYNTHETIC_SOURCE")
    raw=pair_integral(z,v,s,src)
    clipped=pair_integral(z,v,s,np.maximum(src,0.))
    need(abs(raw-clipped)<=out[
        "max_signed_vs_positive_normalized_event_discrepancy"]+1.e-12,
        "SIGNED_TV_BOUND")
    need(out["exceeds_original_LW21_1e_minus4_limit"],
         "ORIGINAL_LW21_FAILURE_PRESERVED")
    print("GE19_LW21B_SIGNED_SOURCE_SENSITIVITY_SELFTEST_PASS 4",flush=True)

def read_two_nz_hdus(p):
    try:
        from astropy.io import fits
    except ImportError as ex:
        raise RuntimeError("GE19_LW21B_ASTROPY_REQUIRED") from ex
    output={}
    with fits.open(p,memmap=True) as hdus:
        for name in ("NZ_LENS","NZ_SOURCE"):
            found=[h for h in hdus if h.name.upper()==name]
            need(len(found)==1,"HDU_"+name+"_NOT_UNIQUE")
            tab=found[0].data
            need(tab is not None,"HDU_"+name+"_EMPTY")
            col={x.upper():x for x in tab.names}
            need("Z_MID" in col,"NO_Z_MID_"+name)
            bins=sorted((x for x in col if x.startswith("BIN") and
                         x[3:].isdigit()),key=lambda x:int(x[3:]))
            need([int(x[3:]) for x in bins]==list(range(1,len(bins)+1)),
                 "BIN_SEQUENCE_"+name)
            z=np.asarray(tab[col["Z_MID"]],float).copy()
            ys={int(x[3:]):np.asarray(tab[col[x]],float).copy()
                for x in bins}
            output[name]=(z,ys)
    return output

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--self-test",action="store_true")
    ap.add_argument("--fits",type=Path)
    ap.add_argument("--out",type=Path,default=ROOT/
      "results/ge19_lw21b_signed_source_geometry_sensitivity_20261110_r1.json")
    arg=ap.parse_args()
    if arg.self_test:
        synthetic_tests();return
    for f,want in ((PRE,PRE_BLOB),(LW07,LW07_BLOB),
                   (ORIG_LW21,ORIG_LW21_BLOB),(POLICY,POLICY_BLOB)):
        need(gitblob(f)==want,"FROZEN_SOURCE_CHANGED_"+f.name)
    need(LW20.is_file() and sha256(LW20)==LW20_SHA,
         "LW20_WSL_PARENT_CHANGED")
    pre=json.loads(PRE.read_text())
    policy=json.loads(POLICY.read_text())
    need(pre["classification"]==
       "GE19_LW21B_ORIGINAL_SIGNED_SOURCE_NZ_VS_NONNEGATIVE_DIAGNOSTIC_LOCK",
       "PRECLASS_CHANGED")
    need(policy["fixed_threshold_relative_negative_area"]==1.e-4,
         "ORIGINAL_LW21_SIGNEDNESS_POLICY_CHANGED")
    need(arg.fits is not None and arg.fits.is_file(),"ORIGINAL_FITS_REQUIRED")
    path=arg.fits.resolve()
    need(path.name==pre["input"]["fits_name"],"FITS_NAME_CHANGED")
    seven=json.loads(LW07.read_text())
    locked=[s for s in seven["source_files"] if s["sample"]=="MagLim"]
    filehash=sha256(path)
    need(len(locked)==1 and locked[0]["file"]==path.name and
         locked[0]["sha256"]==filehash,"DES_FITS_SHA_MISMATCH")
    hdus=read_two_nz_hdus(path)
    zl,lenses=hdus["NZ_LENS"]
    zs,sources=hdus["NZ_SOURCE"]
    need(len(lenses)==6 and len(sources)==4,"DES_NZ_BIN_COUNTS")
    lens_audits=[audit(zl,v,"NZ_LENS_BIN"+str(k),positive_only=True)
                 for k,v in sorted(lenses.items())]
    source_audits=[audit(zs,v,"NZ_SOURCE_BIN"+str(k))
                   for k,v in sorted(sources.items())]
    for d in lens_audits+source_audits:
        print("GE19_LW21B_NZ_SIGNED_AUDIT",json.dumps(d,sort_keys=True),
              flush=True)
    lens4=lenses[4]
    rows=[r for r in seven["rows"] if r["sample"]=="MagLim" and
          r["bin_1based"]==4]
    need(len(rows)==1,"MAGLIM4_ROW_CHANGED")
    support={x["ell"]:x for x in rows[0]["per_ell"]}
    ellipse=[100,150,200,300]
    need(all(e in support for e in ellipse),"ELL_OR_SUPPORT_MISSING")
    output=[]
    for i in sorted(sources):
        original=sources[i]
        plus=np.maximum(original,0.)
        diag=source_audits[i-1]
        limit=diag["max_signed_vs_positive_normalized_event_discrepancy"]
        comparisons=[]
        for ell in ["all"]+ellipse:
            bounds={} if ell=="all" else {
                "left":support[ell]["supported_z_lower"],
                "right":support[ell]["supported_z_upper"]
            }
            if ell!="all" and bounds["left"] is None:
                signed=clipped=0.
            else:
                signed=pair_integral(zl,lens4,zs,original,**bounds)
                clipped=pair_integral(zl,lens4,zs,plus,**bounds)
            dif=abs(signed-clipped)
            need(dif<=limit+2.e-10,"TOTAL_VARIATION_BOUND_FAILED")
            comparisons.append({
                "ell":ell,
                "source_behind_integral_from_original_signed_kernel":
                    signed,
                "source_behind_integral_from_positive_part_diagnostic":
                    clipped,
                "absolute_signed_vs_positive_part_difference":dif,
                "provable_absolute_difference_upper_bound":limit,
                "no_physical_probability_certification":True
            })
        output.append({
            "source_bin":i,
            "raw_diagnostic":diag,
            "paired_lens4_redshift_event_integrals":comparisons
        })
    result={
      "classification":
       "GE19_LW21B_DES_SIGNED_SOURCE_GEOMETRY_SENSITIVITY_REPORTED_NOT_GGL_FORWARD",
      "original_failed_LW21_nz_sign_policy_threshold_preserved":1.e-4,
      "original_LW21_real_WSL_PASS":False,
      "predata_git_blob_sha1":PRE_BLOB,
      "original_fits_sha256":filehash,
      "original_LW20_WSL_SHA256":LW20_SHA,
      "lens_nz_audit":lens_audits,
      "source_bin_comparisons":output,
      "positive_part_used_only_for_diagnostic_comparison":True,
      "negative_source_weight_is_not_literal_probability":True,
      "uncertainty_is_signedness_method_sensitivity_not_DES_photoz_error":True,
      "physical_source_lensing_efficiency_computed":False,
      "physical_eta_matter_Weyl_transfer_certified":False,
      "galaxy_shear_observed_or_covariance_read":False,
      "Asimov_forecast_or_detection":False,
      "full_DES_GGL_forward_certified":False,
      "LW05_cosmic_shear_LOS_BLOCK_preserved":True,
      "LW08_antisymmetric_Weyl_response_UNRESOLVED":True,
      "H4_Z21_certified":False
    }
    target=arg.out.resolve()
    need(target.parent.is_dir() and not target.exists(),
         "OUTPUT_EXISTS_OR_PARENT_MISSING")
    target.write_text(json.dumps(result,indent=2,sort_keys=True,
                                 allow_nan=False)+"\n")
    print("GE19_LW21B_CLASSIFICATION",result["classification"],flush=True)
    print("GE19_LW21B_SOURCE_BINS_AUDITED",len(output),flush=True)
    print("GE19_LW21B_PHYSICAL_GGL_OBSERVER_READY",False,flush=True)
    print("GE19_LW21B_OUTPUT",target,flush=True)

if __name__=="__main__":
    main()
