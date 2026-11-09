#!/usr/bin/env python3
"""GE19 LW05: frozen analytic full-LOS k,z feasibility audit.

No new CLASS runs, source evolution, interpolation, physics parameter fitting,
unmeasured tail estimate or observational inference. Uses SHA-pinned LW01-04.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/"ge19/lw05_line_of_sight_domain_audit_predata_20261109.json"
PRE_GIT_SHA="86081eaa14c781cf4c5eb8586ef0bf4486f9a242"
ELLS=(100,150,200,300,500)


def require(ok,label):
    if not bool(ok):
        raise RuntimeError("GE19_LW05_"+label)


def sha256(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):
            h.update(b)
    return h.hexdigest()


def supported_path(ell,chi_s,chi_min,chi_max,kmin,kmax,h):
    """Exact intersection of certified native z and k under Limber mapping."""
    require(chi_s>chi_max>chi_min>0 and 0<kmin<kmax and h>0
            and ell>=0,"INPUT_DOMAIN")
    lower_k=(ell+.5)/(h*kmax)
    upper_k=(ell+.5)/(h*kmin)
    left=max(chi_min,lower_k,0.)
    right=min(chi_max,upper_k,chi_s)
    span=max(0.,right-left)
    frac=span/chi_s
    return dict(
        limber_kmax_lower_chi_Mpc=float(lower_k),
        limber_kmin_upper_chi_Mpc=float(upper_k),
        chi_supported_lower_Mpc=float(left),
        chi_supported_upper_Mpc=float(right),
        chi_supported_span_Mpc=float(span),
        supported_unweighted_radial_fraction=float(frac),
        unsupported_unweighted_radial_fraction=float(1-frac),
        unsupported_low_chi_Mpc=float(min(left,chi_s)),
        unsupported_high_chi_Mpc=float(chi_s-min(chi_s,max(left,right))),
    )


def selftest():
    a=supported_path(10,1000,100,900,.01,.2,1.)
    b=supported_path(500,1000,100,900,.01,.2,1.)
    require(abs(a["supported_unweighted_radial_fraction"]-.8)<1e-14
            and b["supported_unweighted_radial_fraction"]==0.,
            "SELFTEST_INTERVAL")
    print("GE19_LW05_STRICT_LOS_DOMAIN_SYNTHETIC_SELFTEST_PASS",flush=True)


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--self-test",action="store_true")
    p.add_argument("--lw01-npz",type=Path,default=
                   ROOT/"results/ge19_linear_weyl_native_tangent_20261109_kgridfix.npz")
    p.add_argument("--lw02-json",type=Path,default=
                   ROOT/"results/ge19_lw02_windowed_lensing_20261109.json")
    p.add_argument("--lw03-json",type=Path,default=
                   ROOT/"results/ge19_lw03_source_time_closure_20261109_kprefixfix.json")
    p.add_argument("--lw04-json",type=Path,default=
                   ROOT/"results/ge19_lw04_source_grid_refinement_20261109_zunionfix.json")
    p.add_argument("--output",type=Path,default=
                   ROOT/"results/ge19_lw05_line_of_sight_domain_audit_20261109.json")
    args=p.parse_args()
    if args.self_test:
        selftest()
        return
    blob=subprocess.check_output(["git","hash-object",str(PRE)],
                                 text=True).strip()
    require(blob==PRE_GIT_SHA,"PREDATA_GIT_BLOB_CHANGED")
    pre=json.loads(PRE.read_text())
    require(pre["classification"]==
            "GE19_LW05_STRICT_LOS_KZ_DOMAIN_GEOMETRIC_AUDIT_PREDATA_LOCKED",
            "PREDATA_CHANGED")
    paths={
        "lw01_npz_sha256":args.lw01_npz,
        "lw02_json_sha256":args.lw02_json,
        "lw03_json_sha256":args.lw03_json,
        "lw04_json_sha256":args.lw04_json,
    }
    for key,path in paths.items():
        require(path.is_file() and sha256(path)==pre["frozen_parents"][key],
                "PARENT_HASH_"+key)
    lw02=json.loads(args.lw02_json.read_text())
    lw03=json.loads(args.lw03_json.read_text())
    lw04=json.loads(args.lw04_json.read_text())
    require(lw02["classification"]==
            "GE19_LW02_WINDOW_RESTRICTED_THEORY_ONLY_LENSING_RESPONSE_OBSERVATIONAL_OPEN",
            "LW02_PARENT_CHANGED")
    require(lw03["classification"]==
            "GE19_LW03_SOURCE_TIME_OPERATOR_OR_RADIAL_QUADRATURE_FAIL"
            and not lw03["gates"]["radial_quadrature"],"LW03_FAIL_NOT_PRESERVED")
    require(lw04["classification"]==
            "GE19_LW04_REFINED_SOURCE_GRID_AGREEMENT_PASS_LENSING_STILL_UNCERTIFIED"
            and all(lw04["gates"].values()),"LW04_PASS_NOT_PRESERVED")
    with np.load(args.lw01_npz,allow_pickle=False) as a:
        k=np.asarray(a["k_native_h"],float)
        z=np.asarray(a["z_native"],float)
        mask=np.asarray(a["primary_mask"],bool)
    require(mask.shape==(k.size,z.size) and np.all(np.diff(k)>0)
            and np.all(np.diff(z)<0),"ARCHIVED_NATIVE_SHAPE")
    ki=np.where(mask.any(axis=1))[0]
    zi=np.where(mask.any(axis=0))[0][::-1]
    g=pre["geometry"]
    gates=pre["preregistered_tests"]
    require(ki.size==gates["original_LW02_n_native_k"]
            and zi.size==gates["original_LW02_n_native_z"]
            and np.array_equal(g["native_ell"],list(ELLS)),
            "ARCHIVED_WINDOW_OR_ELL_CHANGED")
    kmin,kmax=float(k[ki[0]]),float(k[ki[-1]])
    require(kmin==.03 and kmax==.2,"K_WINDOW_CHANGED")
    geom=lw02["class_geometry"]
    zg=np.asarray(geom["window_native_z"],float)
    chi=np.asarray(geom["window_chi_Mpc"],float)
    require(np.array_equal(z[zi],zg) and np.all(np.diff(chi)>0)
            and chi.size==8,"LW02_CLASS_GEOMETRY_CHANGED")
    chi_s=float(geom["source_plane_chi_Mpc"])
    require(abs(chi_s-g["source_plane_chi_from_LW02_Mpc"])<=
            gates["source_chi_match_tolerance_Mpc"],
            "CHI_SOURCE_CHANGED")
    h=g["H0_km_s_Mpc"]/100.
    original={int(item["ell"]):item for item in lw02["ell_results"]}
    rows=[]
    for ell in ELLS:
        vals=supported_path(ell,chi_s,float(chi[0]),float(chi[-1]),
                            kmin,kmax,h)
        k_at_native=(ell+.5)/(h*chi)
        count=int(np.count_nonzero((k_at_native>=kmin)&
                                   (k_at_native<=kmax)))
        require(count==original[ell]["native_z_nodes"],
                "LW02_NATIVE_SUPPORT_"+str(ell))
        full=(abs(vals["supported_unweighted_radial_fraction"]-1.)<=
              gates["full_los_fraction_absolute_tolerance"])
        enough=count>=gates["native_z_node_count_min_for_projection"]
        rows.append(dict(ell=ell,**vals,
                         original_LW02_native_z_nodes=count,
                         native_node_count_sufficient=enough,
                         fully_supported_los=full))
        print("GE19_LW05_ELL",ell,
              "RADIAL_SUPPORT",vals["supported_unweighted_radial_fraction"],
              "NATIVE_Z_NODES",count,flush=True)
    ready=all(a["fully_supported_los"] and
              a["native_node_count_sufficient"] for a in rows)
    outcome=("full_support_ready" if ready else "full_support_blocked")
    result={
        "classification":pre["classifications"][outcome],
        "predata_git_blob_sha1":PRE_GIT_SHA,
        "inputs_sha256":{key:sha256(v) for key,v in paths.items()},
        "h":float(h),
        "source_plane_chi_Mpc":chi_s,
        "z_certified_min_max":[float(zg[0]),float(zg[-1])],
        "chi_certified_min_max_Mpc":[float(chi[0]),float(chi[-1])],
        "k_certified_min_max_h_per_Mpc":[kmin,kmax],
        "ell_results":rows,
        "full_los_geometric_domain_ready":ready,
        "LW01_native_Weyl_PASS_preserved":True,
        "LW03_radial_convergence_FAIL_preserved":True,
        "LW04_source_time_resolution_PASS_preserved":True,
        "full_lensing_spectrum_certified":False,
        "physical_lensing_sign_certified":False,
        "observational_likelihood_authorized":False,
        "observational_detection":False,
        "H4_Z21_certified":False,
        "interpretation":"Fractions are unweighted comoving radial distances, NOT lensing power/signal fractions. Contributions from uncertified k,z region cannot be bounded by these distances; do not zero-fill or extrapolate.",
        "scientific_decision":"BLOCK full-LOS cosmic shear or DES/ACT likelihood with current LW01 window; independently certify wider theory support or design a separately justified narrow-lens cross-probe.",
        "execution":"Read-only analytic domain test. No CLASS, forcing, observations, H4 or fitting."
    }
    out=args.output.resolve()
    require(out.parent.is_dir() and not out.exists(),
            "OUTPUT_PREEXISTS_OR_PARENT_MISSING")
    out.write_text(json.dumps(result,sort_keys=True,indent=2,
                              allow_nan=False)+"\n")
    print("GE19_LW05_CLASSIFICATION",result["classification"],flush=True)
    print("GE19_LW05_OUTPUT",str(out),flush=True)


if __name__=="__main__":
    main()
