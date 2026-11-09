#!/usr/bin/env python3
"""GE19 LW07b: inspect only DES Y3 FITS NZ_LENS kernels, never shear values.

No CLASS, no gamma_t, no covariance/likelihood or residuals are read.
All results are informational fractions of true calibrated lens n(z)
lying inside the SHA-frozen native finite k,z window, for fixed ell.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/"ge19/lw07b_des_y3_nz_only_predata_20261109.json"
PRE_BLOB="a3b34e070eef54c18bd0355d37209f6c9e08d92c"
TINY=1e-300


def require(test,name):
    if not bool(test):
        raise RuntimeError("GE19_LW07B_"+name)


def sha256(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as handle:
        for b in iter(lambda:handle.read(1<<20),b""):
            h.update(b)
    return h.hexdigest()


def enclosed_mass(z,n,lo,hi):
    """Piecewise-linear positive n(z) integration with exact interval ends."""
    z=np.asarray(z,float)
    n=np.asarray(n,float)
    require(z.ndim==1 and n.shape==z.shape and z.size>3 and
            np.all(np.diff(z)>0) and
            np.isfinite(n).all() and np.all(n>=0.),"INVALID_NZ")
    norm=float(np.trapezoid(n,z))
    require(norm>0 and np.isfinite(norm),"ZERO_NZ_MASS")
    l=max(lo,float(z[0]))
    r=min(hi,float(z[-1]))
    if l>=r:
        return 0.
    mid=(z>l)&(z<r)
    zz=np.concatenate(([l],z[mid],[r]))
    nn=np.interp(zz,z,n)
    m=float(np.trapezoid(nn,zz)/norm)
    require(-1e-12<=m<=1+1e-12,"NZ_NORMALIZATION_BROKEN")
    return max(0.,min(1.,m))


def selftest():
    z=np.linspace(0.,2.,201)
    n=z*0+1.
    require(abs(enclosed_mass(z,n,.5,1.)-.25)<1e-13,
            "SELFTEST_INTERIOR")
    require(abs(enclosed_mass(z,n,-1.,3.)-1.)<1e-13,
            "SELFTEST_FULL")
    require(enclosed_mass(z,n,2.1,3.)==0.,
            "SELFTEST_OUTSIDE")
    print("GE19_LW07B_NZ_METADATA_SYNTHETIC_SELFTEST_PASS",flush=True)


def parse_fits_kernel(path):
    try:
        from astropy.io import fits
    except ImportError as exc:
        raise RuntimeError("GE19_LW07B_ASTROPY_REQUIRED: python -m pip install astropy") from exc
    # Open the 2pt FITS container, but read ONLY the explicitly named
    # redshift-distribution extension, never observational correlation
    # rows or covariance matrix.
    with fits.open(path,memmap=True) as hdu:
        valid=[i for i,x in enumerate(hdu) if x.name.upper()=="NZ_LENS"]
        require(len(valid)==1,"NO_UNIQUE_NZ_LENS_EXTENSION")
        table=hdu[valid[0]].data
        require(table is not None,"EMPTY_NZ_LENS")
        name_map={x.upper():x for x in table.names}
        require("Z_MID" in name_map,"NZ_Z_MID_MISSING")
        z=np.asarray(table[name_map["Z_MID"]],float).copy()
        require(z.size>=8 and np.isfinite(z).all() and
                np.all(np.diff(z)>0),"NZ_Z_MID_INVALID")
        cols=sorted([x for x in name_map if x.startswith("BIN") and
                     x[3:].isdigit()],key=lambda x:int(x[3:]))
        require(len(cols)>0,"NZ_BIN_COLUMNS_MISSING")
        require([int(x[3:]) for x in cols]==list(range(1,len(cols)+1)),
                "NZ_BIN_NUMBERING")
        arr={int(x[3:]):np.asarray(table[name_map[x]],float).copy()
             for x in cols}
    return z,arr


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--self-test",action="store_true")
    ap.add_argument("--maglim-fits",type=Path)
    ap.add_argument("--redmagic-fits",type=Path)
    ap.add_argument("--lw02-json",type=Path,default=
                    ROOT/"results/ge19_lw02_windowed_lensing_20261109.json")
    ap.add_argument("--output",type=Path,default=
                    ROOT/"results/ge19_lw07b_des_y3_nz_only_audit_20261109.json")
    args=ap.parse_args()
    if args.self_test:
        selftest()
        return
    prehash=subprocess.check_output(
        ["git","hash-object",str(PRE)],text=True).strip()
    require(prehash==PRE_BLOB,"PREDATA_GIT_BLOB_CHANGED")
    pre=json.loads(PRE.read_text())
    require(pre["classification"]==
            "GE19_LW07B_CALIBRATED_DESY3_LENS_NZ_METADATA_PREEXECUTION_LOCK",
            "PREDATA_STATUS_CHANGED")
    require(args.maglim_fits is not None and args.redmagic_fits is not None,
            "BOTH_FITS_PATHS_REQUIRED")
    for sample,filepath,key in (
        ("MagLim",args.maglim_fits,"official_maglim_file"),
        ("redMaGiC",args.redmagic_fits,"official_redmagic_file")):
        require(filepath.is_file() and filepath.name==pre[key],
                "REQUIRED_FITS_FILE_"+sample)
    oldpath=args.lw02_json.resolve()
    require(oldpath.is_file() and sha256(oldpath)==pre[
            "parent_lw02_json_sha256"],"LW02_PARENT_HASH")
    old=json.loads(oldpath.read_text())
    g=old["class_geometry"]
    zg=np.asarray(g["window_native_z"],float)
    chi=np.asarray(g["window_chi_Mpc"],float)
    require(zg.shape==chi.shape==(8,) and
            np.all(np.diff(zg)>0) and np.all(np.diff(chi)>0),
            "ARCHIVED_GEOMETRY")
    h=float(pre["h"])
    kmn,kmx=pre["native_k_h"]
    rows=[]
    source_files=[]
    for label,file,expected_nbin in (
        ("MagLim",args.maglim_fits,6),
        ("redMaGiC",args.redmagic_fits,5)):
        z,nzs=parse_fits_kernel(file)
        require(len(nzs)==expected_nbin,
                "LENS_NZ_BIN_COUNT_"+label)
        source_files.append({"sample":label,"file":file.name,
                             "sha256":sha256(file),
                             "NZ_LENS_bin_count":len(nzs),
                             "NZ_LENS_z_min_max":[float(z[0]),float(z[-1])]})
        for binid,vals in nzs.items():
            m_z=enclosed_mass(z,vals,float(zg[0]),float(zg[-1]))
            ells=[]
            for ell in pre["eval_multipoles"]:
                chi_lo=max(float(chi[0]),(ell+.5)/(h*kmx))
                chi_hi=min(float(chi[-1]),(ell+.5)/(h*kmn))
                if chi_lo>=chi_hi:
                    frac=0.
                    zlo=zhi=None
                else:
                    zlo=float(np.interp(chi_lo,chi,zg))
                    zhi=float(np.interp(chi_hi,chi,zg))
                    frac=enclosed_mass(z,vals,zlo,zhi)
                ells.append({
                    "ell":int(ell),
                    "supported_z_lower":zlo,
                    "supported_z_upper":zhi,
                    "fraction_of_calibrated_nz_mass_inside_kz_domain":frac,
                    "informational_fraction_ge_0p99":
                        bool(frac>=pre["true_nz_mass_in_domain_informational_threshold"]),
                })
            rows.append({
                "sample":label,"bin_1based":int(binid),
                "fraction_of_calibrated_nz_mass_in_native_z_window":m_z,
                "per_ell":ells,
                "calibrated_nz_tails_zeroed":False,
                "ell_angular_window_validated":False,
                "survey_likelihood_eligible":False,
            })
            print("GE19_LW07B_NZ",label,"BIN",binid,
                  "Z_FRAC",m_z,
                  "ELL_FRACS",[(v["ell"],round(v[
                      "fraction_of_calibrated_nz_mass_inside_kz_domain"],6))
                      for v in ells],flush=True)
    result={
        "classification":"GE19_LW07B_TRUE_NZ_SUPPORT_MEASURED_OBSERVATION_STILL_BLOCKED",
        "predata_git_blob_sha1":PRE_BLOB,
        "LW02_json_sha256":sha256(oldpath),
        "source_files":source_files,
        "rows":rows,
        "native_z_window":[float(zg[0]),float(zg[-1])],
        "native_k_h_window":[kmn,kmx],
        "observed_shear_or_covariance_read":False,
        "full_angular_window_forward_model_certified":False,
        "physical_eta_calibrated":False,
        "galaxy_source_gauge_and_bias_certified":False,
        "observational_likelihood_authorized":False,
        "observational_detection":False,
        "note":"Fractions refer to calibrated lens n(z) only; geometry plus finite k,z native transfer. They are not fractions of GGL amplitude or angular bandpower. 1% tails cannot be silently discarded."
    }
    out=args.output.resolve()
    require(out.parent.is_dir() and not out.exists(),
            "OUTPUT_EXISTS_OR_PARENT_MISSING")
    out.write_text(json.dumps(result,indent=2,sort_keys=True,
                              allow_nan=False)+"\n")
    print("GE19_LW07B_CLASSIFICATION",result["classification"],flush=True)
    print("GE19_LW07B_OUTPUT",str(out),flush=True)


if __name__=="__main__":
    main()
