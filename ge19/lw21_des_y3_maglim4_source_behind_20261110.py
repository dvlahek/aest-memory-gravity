#!/usr/bin/env python3
"""GE19 LW21: source-redshift geometry from original DES Y3 MagLim FITS.

Read ONLY NZ_LENS and NZ_SOURCE in the already published DES Y3 2-point
FITS, never observed GAMMAT/COVMAT/other data vectors. Compute exact
piecewise-linear model probabilities P(z_source>z_lens) and which parts
of that probability have lens z inside original LW07b native k,z
support, for three frozen ell candidate nodes.

This is NOT lensing efficiency or DES likelihood or Weyl detection.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/"ge19/lw21_des_y3_maglim4_source_behind_predata_20261110.json"
PRE_BLOB="2b00093ef9621ed19c17ed5599feaa0e58d004d4"
SIGNEDNESS=ROOT/"ge19/lw21_nz_signedness_handling_erratum_20261110.json"
SIGNEDNESS_BLOB="4cd19e0ed232a0c7fe8c5673cafdc7d4c7ff4cf4"
MAX_NEGATIVE_MASS_RATIO=1.e-4
OLD7=ROOT/"results/ge19_lw07b_des_y3_nz_only_audit_20261109.json"
OLD7_BLOB="5323b8457cbe7e7426c3e6eb4345183c3660cbff"
OLD20=ROOT/"results/ge19_lw20_ggl_preforecast_support_20261110_r1.json"
OLD20_SHA256="ab0b0147b4edf1a12d182628f81476e2d23443e347fe636243d51007eca962a4"

def require(ok,tag):
    if not bool(ok):
        raise RuntimeError("GE19_LW21_"+tag)

def sha256(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda:f.read(1<<20),b""):
            h.update(block)
    return h.hexdigest()

def gitblob(path):
    return subprocess.check_output(["git","hash-object",str(path)],text=True).strip()

def normalized_cdf(z,y):
    z=np.asarray(z,float);y=np.asarray(y,float)
    require(z.ndim==1 and z.size>5 and y.shape==z.shape,
            "NZ_SHAPE")
    require(np.isfinite(z).all() and np.isfinite(y).all()
            and np.all(np.diff(z)>0) and np.all(y>=0),
            "NZ_VALUES_INVALID")
    spans=np.diff(z)
    cumulative=np.r_[0.,np.cumsum(spans*(y[:-1]+y[1:])/2.)]
    total=float(cumulative[-1])
    require(np.isfinite(total) and total>0,"NZ_ZERO_MASS")
    return cumulative/total,total


def audited_working_nz(z,values,label):
    """Raw FITS untouched; diagnose signedness before any conditional clipping.

    epsilon = integral(max(-n,0))/integral(max(n,0)), with trapezoidal
    areas on the original z grid. Only numerical-sign undershoots
    epsilon<=1e-4 are clipped on a working copy, with full audit record.
    Larger or nonfinite anomalies fail closed after printing statistics.
    """
    z=np.asarray(z,float)
    y=np.asarray(values,float)
    shape_ok=z.ndim==1 and z.size>5 and y.shape==z.shape
    audit={
        "bin":label,
        "z_points":int(z.size),
        "raw_values_count":int(y.size),
        "array_shape_ok":bool(shape_ok),
        "z_nonfinite_count":int(np.count_nonzero(~np.isfinite(z))),
        "nz_nonfinite_count":int(np.count_nonzero(~np.isfinite(y))),
        "nz_negative_sample_count":int(np.count_nonzero(y<0)),
        "nz_min":float(np.min(y[np.isfinite(y)])) if np.isfinite(y).any() else None,
        "nz_max":float(np.max(y[np.isfinite(y)])) if np.isfinite(y).any() else None,
        "integrated_positive_area":None,
        "integrated_negative_area":None,
        "negative_to_positive_area":None,
        "normalized_signed_vs_clipped_TV_bound":None,
        "corrected_on_working_copy":False,
    }
    valid=shape_ok and np.isfinite(z).all() and np.isfinite(y).all() and np.all(np.diff(z)>0)
    if valid:
        positive=np.maximum(y,0.)
        negative=np.maximum(-y,0.)
        pa=float(np.trapezoid(positive,z))
        na=float(np.trapezoid(negative,z))
        audit["integrated_positive_area"]=pa
        audit["integrated_negative_area"]=na
        if np.isfinite(pa) and pa>na>=0:
            eps=na/pa
            audit["negative_to_positive_area"]=eps
            audit["normalized_signed_vs_clipped_TV_bound"]=eps/(1.-eps)
            valid=eps<=MAX_NEGATIVE_MASS_RATIO
        else:
            valid=False
    print("GE19_LW21_RAW_NZ_SIGN_AUDIT",json.dumps(audit,sort_keys=True),flush=True)
    require(valid,"NZ_SIGNEDNESS_SOURCE_REVIEW_REQUIRED_"+label)
    used=np.maximum(y,0.)
    audit["corrected_on_working_copy"]=bool(audit["nz_negative_sample_count"]>0)
    normalized_cdf(z,used)
    return used,audit

def survival(zquery,z,values):
    """Exact piecewise-quadratic survival of piecewise-linear source n(z)."""
    q=np.asarray(zquery,dtype=float)
    cum,total=normalized_cdf(z,values)
    index=np.clip(np.searchsorted(z,q,side="right")-1,0,len(z)-2)
    delta=q-z[index]
    width=z[index+1]-z[index]
    slope=(values[index+1]-values[index])/width
    prob_below=cum[index]+(values[index]*delta+slope*delta**2/2.)/total
    result=np.where(q<=z[0],1.,np.where(q>=z[-1],0.,1.-prob_below))
    return np.clip(result,0.,1.)

# Four-point Gauss-Legendre is exact for this model on each union-knot
# interval: piecewise-linear lens density times piecewise-quadratic
# source survival = piecewise cubic.
G_NODES=np.array([-0.8611363115940526,-0.3399810435848563,
                   0.3399810435848563,0.8611363115940526])
G_WEIGHTS=np.array([0.3478548451374539,0.6521451548625461,
                    0.6521451548625461,0.3478548451374539])

def pair_probability(zl,nl,zs,ns,lower=None,upper=None):
    zl=np.asarray(zl,float);nl=np.asarray(nl,float)
    zs=np.asarray(zs,float);ns=np.asarray(ns,float)
    _,norm_l=normalized_cdf(zl,nl)
    normalized_cdf(zs,ns)
    lo=max(float(zl[0]),float(lower) if lower is not None else float(zl[0]))
    hi=min(float(zl[-1]),float(upper) if upper is not None else float(zl[-1]))
    if lo>=hi:
        return 0.
    internal=np.r_[zl[(zl>lo)&(zl<hi)],
                   zs[(zs>lo)&(zs<hi)]]
    mesh=np.unique(np.r_[lo,internal,hi])
    starts,ends=mesh[:-1],mesh[1:]
    midpoint=(starts+ends)/2.
    halfwidth=(ends-starts)/2.
    quadx=midpoint[:,None]+halfwidth[:,None]*G_NODES[None,:]
    lens=np.interp(quadx,zl,nl)
    behind=survival(quadx,zs,ns)
    p=float(np.sum(halfwidth[:,None]*G_WEIGHTS[None,:]*lens*behind)/norm_l)
    require(np.isfinite(p) and -1.e-12<=p<=1.+1.e-12,
            "PAIR_PROBABILITY_BOUND")
    return float(np.clip(p,0.,1.))

def synthetic_selftest():
    z=np.linspace(0,1,31);one=np.ones_like(z)
    p=pair_probability(z,one,z,one)
    require(abs(p-.5)<1.e-12,"UNIFORM_HALF")
    require(abs(pair_probability(z,one,z,one,.25,.75)-.25)<1.e-12,
            "UNIFORM_HALF_INTERVAL")
    a=np.linspace(.4,.6,21)
    behind=np.linspace(.8,1.,21)
    front=np.linspace(0,.2,21)
    require(abs(pair_probability(a,np.ones_like(a),
           behind,np.ones_like(behind))-1.)<1.e-12,"ALL_SOURCE_BEHIND")
    require(pair_probability(a,np.ones_like(a),
           front,np.ones_like(front))<1.e-12,"ALL_SOURCE_IN_FRONT")
    # Mathematically tiny signedness is permitted only on a working copy.
    small=np.ones_like(z)
    small[0]=-1.e-6
    fixed, audit=audited_working_nz(z,small,"SYNTHETIC_TINY")
    require(audit["corrected_on_working_copy"] and
            audit["negative_to_positive_area"]<MAX_NEGATIVE_MASS_RATIO and
            (fixed>=0).all(),"TINY_SIGNEDNESS_NOT_HANDLED")
    bad=np.ones_like(z)
    bad[0]=-1.
    blocked=False
    try:
        audited_working_nz(z,bad,"SYNTHETIC_BIG")
    except RuntimeError as err:
        blocked="NZ_SIGNEDNESS_SOURCE_REVIEW_REQUIRED" in str(err)
    require(blocked,"BIG_SIGNEDNESS_NOT_REJECTED")
    print("GE19_LW21_SOURCE_BEHIND_SYNTHETIC_SELFTEST_PASS 6",flush=True)

def read_nz_only(fitsfile):
    try:
        from astropy.io import fits
    except ImportError as e:
        raise RuntimeError("GE19_LW21_ASTROPY_REQUIRED") from e
    obj={}
    signedness_audit=[]
    # Only access named n(z) HDU data; other HDUs remain uninspected.
    with fits.open(fitsfile,memmap=True) as hdus:
        for hname in ("NZ_LENS","NZ_SOURCE"):
            matching=[h for h in hdus if h.name.upper()==hname]
            require(len(matching)==1,"HDU_"+hname+"_NOT_UNIQUE")
            table=matching[0].data
            require(table is not None,"HDU_"+hname+"_EMPTY")
            names={n.upper():n for n in table.names}
            require("Z_MID" in names,"Z_MID_MISSING_"+hname)
            bins=sorted([key for key in names if key.startswith("BIN")
                         and key[3:].isdigit()],key=lambda k:int(k[3:]))
            require([int(k[3:]) for k in bins]==
                    list(range(1,len(bins)+1)),"BIN_SEQUENCE_"+hname)
            z=np.asarray(table[names["Z_MID"]],float).copy()
            dist={}
            for col in bins:
                dist[int(col[3:])]=np.asarray(table[names[col]],float).copy()
            for binid in sorted(dist):
                dist[binid],audit=audited_working_nz(
                    z,dist[binid],hname+"_BIN"+str(binid))
                signedness_audit.append(audit)
            obj[hname]=(z,dist)
    return obj,signedness_audit

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--self-test",action="store_true")
    ap.add_argument("--fits",type=Path)
    ap.add_argument("--out",type=Path,default=ROOT/
      "results/ge19_lw21_des_y3_maglim4_source_behind_20261110_r1.json")
    args=ap.parse_args()
    if args.self_test:
        synthetic_selftest()
        return
    require(args.fits is not None and args.fits.is_file(),"MAGLIM_FITS_REQUIRED")
    require(gitblob(PRE)==PRE_BLOB,"PRELOCK_CHANGED")
    require(gitblob(SIGNEDNESS)==SIGNEDNESS_BLOB,
            "SIGNEDNESS_POLICY_LOCK_CHANGED")
    policy=json.loads(SIGNEDNESS.read_text())
    require(policy["classification"]==
      "GE19_LW21_NZ_FITS_SIGNEDNESS_PREVALUE_REPAIR_POLICY"
      and policy["fixed_threshold_relative_negative_area"]==
      MAX_NEGATIVE_MASS_RATIO,"SIGNEDNESS_POLICY_CHANGED")
    require(gitblob(OLD7)==OLD7_BLOB,"ORIGINAL_LW07B_CHANGED")
    require(OLD20.is_file() and sha256(OLD20)==OLD20_SHA256,
            "ORIGINAL_LW20_WSL_CHANGED")
    pre=json.loads(PRE.read_text())
    seven=json.loads(OLD7.read_text())
    twenty=json.loads(OLD20.read_text())
    require(pre["classification"]==
       "GE19_LW21_DES_Y3_MAGLIM4_SOURCE_BEHIND_GEOMETRY_PREDATA",
       "CLASSIFICATION_PRE_CHANGED")
    require(seven["classification"]==
       "GE19_LW07B_TRUE_NZ_SUPPORT_MEASURED_OBSERVATION_STILL_BLOCKED",
       "LW07B_NOT_FROZEN")
    require(twenty["classification"]==
       "GE19_LW20_MAGLIM4_LENS_ONLY_SUPPORT_SCREEN_PASS_GGL_FORWARD_AND_FORECAST_BLOCKED",
       "LW20_NOT_FROZEN")
    fitsfile=args.fits.resolve()
    require(fitsfile.name==pre["input_public_fits"],"FITS_FILENAME_MISMATCH")
    actual_sha=sha256(fitsfile)
    original=[s for s in seven["source_files"] if s["sample"]=="MagLim"]
    require(len(original)==1 and
            original[0]["file"]==fitsfile.name and
            original[0]["sha256"]==actual_sha,"FITS_HASH_NOT_ORIGINAL")
    data,signedness_audit=read_nz_only(fitsfile)
    zl,lens=data["NZ_LENS"]
    zs,sources=data["NZ_SOURCE"]
    require(len(lens)==6 and len(sources)==4,"REDSHIFT_BIN_COUNT")
    lens_id=4
    oldrows=[r for r in seven["rows"] if
        r["sample"]=="MagLim" and r["bin_1based"]==lens_id]
    require(len(oldrows)==1,"FROZEN_LENS_ROW_NOT_UNIQUE")
    bounds={r["ell"]:r for r in oldrows[0]["per_ell"]}
    ell=pre["candidate_ell"]
    require(ell==[100,150,200] and 300 in bounds,
            "ELL_PRELOCK_CHANGED")
    outrows=[]
    for source_bin in sorted(sources):
        s=sources[source_bin]
        full=pair_probability(zl,lens[lens_id],zs,s)
        covered=[]
        for multipole in ell+[300]:
            original=bounds[multipole]
            left=original["supported_z_lower"]
            right=original["supported_z_upper"]
            constrained=(pair_probability(zl,lens[lens_id],zs,s,
                           left,right) if left is not None else 0.)
            tail=full-constrained
            require(constrained<=full+1.e-12 and tail>=-1.e-12,
                    "GEOMETRIC_PAIR_MASS_CONSISTENCY")
            covered.append({
                "ell":multipole,
                "total_probability_lens_in_native_and_source_behind":
                    constrained,
                "total_probability_lens_outside_native_and_source_behind":
                    max(0.,tail),
                "fraction_of_behind_pairs_with_lens_native":
                    constrained/full if full>0 else None,
            })
        outrows.append({"source_bin_1based":source_bin,
                        "p_source_redshift_greater_than_lens_redshift":full,
                        "per_ell":covered})
    report={
       "classification":
         "GE19_LW21_SOURCE_BEHIND_LENS_REDSHIFT_GEOMETRY_PASS_GGL_PHYSICAL_FORWARD_OPEN",
       "protocol_git_blob_sha1":PRE_BLOB,
       "signedness_policy_git_blob_sha1":SIGNEDNESS_BLOB,
       "negative_area_threshold":MAX_NEGATIVE_MASS_RATIO,
       "raw_nz_sign_diagnostics":signedness_audit,
       "raw_FITS_bytes_modified":False,
       "maximum_pair_event_signed_to_clipped_bound":
           max(a["normalized_signed_vs_clipped_TV_bound"]
               for a in signedness_audit if a["bin"].startswith("NZ_LENS"))+
           max(a["normalized_signed_vs_clipped_TV_bound"]
               for a in signedness_audit if a["bin"].startswith("NZ_SOURCE")),
       "official_maglim_fits_name":fitsfile.name,
       "official_maglim_fits_sha256":actual_sha,
       "original_LW20_WSL_SHA256":OLD20_SHA256,
       "lens_sample":"DES Y3 MagLim","lens_bin_1based":lens_id,
       "source_sample":"DES Y3 NZ_SOURCE calibrated distributions",
       "source_bin_count":len(sources),
       "source_bins":outrows,
       "lens_and_source_nz_only":True,
       "source_behind_probability_is_not_lensing_efficiency":True,
       "actual_source_lensing_efficiency_computed":False,
       "lens_kz_and_angular_forward_certified":False,
       "original_action_to_CLASS_map_certified":False,
       "physical_eta_GGL_response_computed":False,
       "covariance_or_observed_shear_read":False,
       "Asimov_forecast_computed":False,
       "observational_detection":False,
       "LW05_cosmic_shear_LOS_BLOCK_preserved":True,
       "LW08_antisymmetric_Weyl_tangent_UNRESOLVED_preserved":True,
       "H4_Z21_certified":False,
       "science_stop":"Redshift ordering P(z_s>z_l) is NOT the shear efficiency g_s(chi), measured source galaxy response, full n(z) kernel or memory detection. A full background chi(z), physical P_deltaW eta tangent and angular/covariance model are still needed."
    }
    target=args.out.resolve()
    require(target.parent.is_dir() and not target.exists(),
            "OUTPUT_EXISTS_OR_PARENT_MISSING")
    target.write_text(json.dumps(report,indent=2,sort_keys=True,
                                 allow_nan=False)+"\n")
    print("GE19_LW21_CLASSIFICATION",report["classification"],flush=True)
    for r in outrows:
        print("GE19_LW21_SOURCE_BEHIND",
              r["source_bin_1based"],
              f'{r["p_source_redshift_greater_than_lens_redshift"]:.9g}',
              flush=True)
    print("GE19_LW21_PHYSICAL_FORECAST_READY",False,flush=True)
    print("GE19_LW21_OUTPUT",target,flush=True)

if __name__=="__main__":
    main()
