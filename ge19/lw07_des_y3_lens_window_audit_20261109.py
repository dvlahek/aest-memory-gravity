#!/usr/bin/env python3
"""GE19 LW07: metadata-only DES Y3 photo-z geometry screen, no observed data.

The input DES *photometric selection edges* are not true n(z) supports,
nor do finite ell ranges validate an observed gamma_t(theta) bin.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
from pathlib import Path

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/"ge19/lw07_des_y3_lens_window_predata_20261109.json"
PRE_BLOB="d455ba3db31ea02ba02511735be4bec34cc7e040"


def require(condition, label):
    if not bool(condition):
        raise RuntimeError("GE19_LW07_"+label)


def sha256(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda:handle.read(1<<20),b""):
            h.update(block)
    return h.hexdigest()


def nominal_bin_window(zlo,zhi,z_native,chi_native,klo,khi,h):
    """Support for all nominal photo-z values; NOT calibrated n(z)."""
    if zlo < z_native[0] or zhi > z_native[-1]:
        return {"status":"PHOTOMETRIC_BIN_EXTENDS_BEYOND_NATIVE_CERTIFIED_Z",
                "nominal_bin_completely_inside_native_z":False,
                "ell_lower":None,"ell_upper":None,
                "ell_span_integer_count":0,"chi_Mpc_lower":None,
                "chi_Mpc_upper":None}
    x0=float(np.interp(zlo,z_native,chi_native))
    x1=float(np.interp(zhi,z_native,chi_native))
    ell_min=math.ceil(klo*h*x1-.5)
    ell_max=math.floor(khi*h*x0-.5)
    ok=ell_min<=ell_max
    return {
        "status":("METADATA_ONLY_NOMINAL_BIN_KZ_SUPPORT_CANDIDATE"
                  if ok else "NOMINAL_BIN_HAS_NO_COMMON_ELL_INTERVAL"),
        "nominal_bin_completely_inside_native_z":True,
        "ell_lower":int(ell_min) if ok else None,
        "ell_upper":int(ell_max) if ok else None,
        "ell_span_integer_count":int(ell_max-ell_min+1) if ok else 0,
        "chi_Mpc_lower":x0,"chi_Mpc_upper":x1,
    }


def selftest():
    z=np.array([.2,.4,.7,1.]);chi=np.array([800.,1500.,2450.,3400.])
    a=nominal_bin_window(.4,.7,z,chi,.03,.2,.673)
    require(a["status"]=="METADATA_ONLY_NOMINAL_BIN_KZ_SUPPORT_CANDIDATE",
            "SELFTEST_CANDIDATE")
    require(a["ell_lower"]==50 and a["ell_upper"]==201,"SELFTEST_ELL")
    b=nominal_bin_window(.1,.4,z,chi,.03,.2,.673)
    require(b["ell_lower"] is None,"SELFTEST_OUT_OF_DOMAIN")
    print("GE19_LW07_PHOTOZ_BIN_GEOMETRY_SELFTEST_PASS",flush=True)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--self-test",action="store_true")
    parser.add_argument("--lw02-json",type=Path,default=ROOT/
        "results/ge19_lw02_windowed_lensing_20261109.json")
    parser.add_argument("--out",type=Path,default=ROOT/
        "results/ge19_lw07_des_y3_lens_window_audit_20261109.json")
    a=parser.parse_args()
    if a.self_test:
        selftest()
        return

    gitblob=subprocess.check_output(["git","hash-object",str(PRE)],
                                    text=True).strip()
    require(gitblob==PRE_BLOB,"PREDATA_LOCK_CHANGED")
    pre=json.loads(PRE.read_text())
    require(pre["classification"]==
            "GE19_LW07_DESY3_PUBLISHED_PHOTOZ_WINDOW_METADATA_PREDATA_LOCK",
            "PREDATA_STATUS_CHANGED")
    src=a.lw02_json.resolve()
    require(src.is_file() and sha256(src)==pre["archived_model_lock"][
            "lw02_json_sha256"],"LW02_PARENT_HASH")
    old=json.loads(src.read_text())
    assert old["classification"] == (
        "GE19_LW02_WINDOW_RESTRICTED_THEORY_ONLY_LENSING_RESPONSE_OBSERVATIONAL_OPEN"
    ), "Frozen LW02 parent classification changed"
    geom=old["class_geometry"]
    z=np.asarray(geom["window_native_z"],float)
    chi=np.asarray(geom["window_chi_Mpc"],float)
    require(z.shape==chi.shape==(8,) and
            np.isfinite(z).all() and np.isfinite(chi).all() and
            np.all(np.diff(z)>0) and np.all(np.diff(chi)>0),
            "ARCHIVED_CLASS_GEOMETRY")
    h=pre["archived_model_lock"]["H0_km_s_Mpc"]/100.
    kmin=pre["archived_model_lock"]["lw01_native_k_h_min"]
    kmax=pre["archived_model_lock"]["lw01_native_k_h_max"]
    require(kmin==.03 and kmax==.2,"NATIVE_K_BOUNDS")

    rows=[]
    for sample,edges in pre["DES_Y3_published_photoz_bins"].items():
        for i,(lo,hi) in enumerate(edges,1):
            assert lo<hi
            item=nominal_bin_window(lo,hi,z,chi,kmin,kmax,h)
            rows.append({
                "sample":sample,"bin_1based":i,
                "photometric_selection_z_min":lo,
                "photometric_selection_z_max":hi,
                **item,
                "calibrated_true_lens_nz_checked":False,
                "angular_bandpower_window_checked":False,
                "gamma_t_observable_certified":False,
            })
            print("GE19_LW07",sample,"BIN",i,item["status"],
                  "ELL",item["ell_lower"],item["ell_upper"],flush=True)
    require(len(rows)==11,"BIN_COUNT")
    candidates=[r for r in rows if r["status"]==
                "METADATA_ONLY_NOMINAL_BIN_KZ_SUPPORT_CANDIDATE"]
    # Deliberate STOP: photo-z bounds do not truncate true n(z), and
    # real-space gamma_t carries a broad Bessel ell response.
    output={
        "classification":pre["evaluation_policy"]["classification"],
        "predata_git_blob_sha1":PRE_BLOB,
        "LW02_json_sha256":sha256(src),
        "h":float(h),
        "LW01_original_native_k_h_min_max":[kmin,kmax],
        "LW01_actual_native_z_min_max":[float(z[0]),float(z[-1])],
        "n_published_photoz_bins":len(rows),
        "n_nominal_geometric_candidates":len(candidates),
        "rows":rows,
        "actual_calibrated_true_lens_nz_accessed":False,
        "observed_gamma_t_accessed":False,
        "observed_covariance_or_residuals_accessed":False,
        "survey_window_functions_accessed":False,
        "physical_galaxy_Weyl_cross_power_certified":False,
        "gauge_consistent_galaxy_density_certified":False,
        "finite_eta_calibrated":False,
        "galaxy_lensing_forward_model_certified":False,
        "DES_Y3_likelihood_authorized":False,
        "physical_observation_or_detection":False,
        "LW03_radial_fail_preserved":True,
        "LW04_source_time_pass_preserved":True,
        "LW05_full_los_block_preserved":True,
        "LW06_native_matter_Weyl_pass_preserved":True,
        "interpretation":"Nominal photo-z selection bin ranges and CLASS chi(z) yield bounded ell feasibility only. Actual true n(z) tails and real-space angular windows are NOT tested. Do not interpret as observed lens-bin eligibility.",
        "next_evidence_required":[
          "Official DES 3x2pt calibrated NZ_LENS distribution and photo-z nuisance variations",
          "Actual source n(z) and survey selection/galaxy-bias model",
          "Validated angular bandpower window or full real-space J2 transform and out-of-window contribution bound",
          "Gauge-consistent galaxy-matter-Weyl forward model and physical eta normalization",
          "Covariance-aware Asimov discriminability against restricted instant-gravity and nuisance templates, before observed residuals"
        ]
    }
    out=a.out.resolve()
    require(out.parent.is_dir() and not out.exists(),"OUTPUT_PREEXISTS_OR_DIR")
    out.write_text(json.dumps(output,indent=2,sort_keys=True,
                              allow_nan=False)+"\n")
    print("GE19_LW07_CLASSIFICATION",output["classification"],flush=True)
    print("GE19_LW07_OUTPUT",out,flush=True)


if __name__=="__main__":
    main()
