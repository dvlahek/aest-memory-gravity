#!/usr/bin/env python3
"""GE19 LW04: one frozen, independently finer CLASS source-time grid.

Reference: successful three-run LW03 CLASS get_transfer(z) output, saved at
fixed 65 chi points for ell 100,150,200,300. New: only baseline, +2.5,
-2.5 CLASS solves with perturbations_sampling_stepsize=0.025 rather than
the standard 0.1. All physical parameters and signed external forcing
are original and SHA-locked. This test does NOT certify full lensing or
reopen the already failed LW03 radial quadrature gate.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from pathlib import Path

import numpy as np

from v063 import theory_response_map as v63
from ge19 import lw03_source_time_closure_20261109 as lw03
from ge19 import lw02_windowed_lensing_20261109 as lw02

ROOT = Path(__file__).resolve().parents[1]
PRE = ROOT / "ge19/lw04_source_grid_refinement_predata_20261109.json"
PREDATA_GIT_BLOB = "59e43bb536bd899b74620056942f711fe842cbc1"
ELLS = (100, 150, 200, 300)
TINY = 1.e-300


def require(ok, label):
    if not bool(ok):
        raise RuntimeError("GE19_LW04_" + label)


def sha256(path):
    dig = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            dig.update(block)
    return dig.hexdigest()


def l2rel(new, old):
    return float(np.linalg.norm(new-old) / max(np.linalg.norm(old), TINY))


def selftest():
    k = np.geomspace(.01, 1., 120)
    chi = np.linspace(900., 2500., 65)
    w = np.ones((120,65)) * 3
    dw = np.ones_like(w) * .15
    cf, df, af = lw02.signed_projection_on_chi(
        100, chi, 3800., k, w, dw*1.001, 2.1e-9, .966, True)
    cc, dc, ac = lw02.signed_projection_on_chi(
        100, chi, 3800., k, w, dw, 2.1e-9, .966, True)
    require(l2rel(dw*1.001, dw)<.002, "SELFTEST_L2")
    require(abs((df-dc)/dc-.001)<1e-11, "SELFTEST_DERIVATIVE")
    require(abs(cf-cc)<1e-14*cc, "SELFTEST_BASELINE")
    require(abs(df-dc)/ac <.05 and af>0., "SELFTEST_ABSOLUTE_GATE")
    print("GE19_LW04_SOURCE_GRID_SYNTHETIC_SELFTEST_PASS",flush=True)


def class_run(label, lam, force, class_params, query_z, full_kh, selected_k):
    from classy import Class
    envnames=("AEST_TANGENT_FORCE_FILE","AEST_TANGENT_LAMBDA",
              "AEST_OFFLINE_TRACE_FILE","OMP_NUM_THREADS")
    saved={name:os.environ.get(name) for name in envnames}
    c=None
    try:
        os.environ.pop("AEST_OFFLINE_TRACE_FILE",None)
        os.environ["OMP_NUM_THREADS"]="1"
        if lam is None:
            os.environ.pop("AEST_TANGENT_FORCE_FILE",None)
            os.environ.pop("AEST_TANGENT_LAMBDA",None)
        else:
            os.environ["AEST_TANGENT_FORCE_FILE"]=str(force)
            os.environ["AEST_TANGENT_LAMBDA"]=str(float(lam))
        print("GE19_LW04_CLASS_RUN",label,flush=True)
        c=Class()
        c.set(class_params)
        c.compute()

        # Return the actual source time grid length: this must grow.
        if lam is None:
            t,k_phys,native_z=c.get_transfer_and_k_and_z(
                output_format="class",h_units=False)
            native_z=np.asarray(native_z,float)
            require(all(q in t for q in ("phi","psi")),
                    "REFINED_NATIVE_WEYL_NOT_PRESENT")
            ntime=int(native_z.size)
            require(np.all(np.isfinite(native_z)),
                    "REFINED_NATIVE_Z_NONFINITE")
            kphys=np.asarray(k_phys,float)
            h=float(v63.START["H0"])/100.
            require(kphys.shape==full_kh.shape and
                    np.max(abs(kphys/h-full_kh)/
                           np.maximum(abs(full_kh),TINY))<=1e-10,
                    "REFINED_NATIVE_K_MISMATCH")
            bg=c.get_background()
            zbg=np.asarray(bg["z"],float)
            chibg=np.asarray(bg["comov. dist."],float)
            order=np.argsort(zbg)
            zbg,chibg=zbg[order],chibg[order]
            require(np.all(np.diff(zbg)>0), "BACKGROUND_Z_GRID")
        else:
            ntime=None
            zbg=chibg=None

        out=np.empty((len(query_z),len(selected_k)),float)
        max_kerr=0.
        for i, z in enumerate(query_z):
            value,kerr=lw03.native_source_weyl(
                c.get_transfer(float(z),output_format="class"),
                full_kh)
            out[i,:]=value[selected_k]
            max_kerr=max(kerr,max_kerr)
        require(np.isfinite(out).all(), "SOURCE_W_NONFINITE")
        return out, max_kerr, ntime, zbg, chibg
    finally:
        if c is not None:
            try:
                c.struct_cleanup()
                c.empty()
            except Exception:
                pass
        for key,val in saved.items():
            if val is None:
                os.environ.pop(key,None)
            else:
                os.environ[key]=val


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--self-test",action="store_true")
    ap.add_argument("--class-root",type=Path)
    ap.add_argument("--lw01-prefix",type=Path,default=
                    ROOT/"results/ge19_linear_weyl_native_tangent_20261109_kgridfix")
    ap.add_argument("--lw03-prefix",type=Path,default=
                    ROOT/"results/ge19_lw03_source_time_closure_20261109_kprefixfix")
    ap.add_argument("--output-prefix",type=Path,default=
                    ROOT/"results/ge19_lw04_source_grid_refinement_20261109")
    args=ap.parse_args()
    if args.self_test:
        selftest()
        return

    pre=json.loads(PRE.read_text())
    obj=subprocess.check_output(["git","hash-object",str(PRE)],
                                 text=True).strip()
    require(obj==PREDATA_GIT_BLOB,"PREDATA_CHANGED")
    require(pre["protocol_classification"]==
            "GE19_LW04_FIXED_MODEL_INDEPENDENT_SOURCE_TIME_GRID_PREDATA_LOCK",
            "PREDATA_PROTOCOL")
    cfg=pre["experiment"]
    require(cfg["refined_class_runs"]==3 and
            cfg["refined_value"]==.025 and
            cfg["original_default_value"]==.1 and
            cfg["identical_ell_windows"]==list(ELLS),
            "EXPERIMENT_CHANGED")

    require(args.class_root is not None,"CLASS_ROOT_REQUIRED")
    class_root=args.class_root.resolve()
    require((class_root/"class").is_file(),"CLASS_EXECUTABLE_MISSING")
    head=subprocess.check_output(["git","-C",str(class_root),
                                  "rev-parse","HEAD"],text=True).strip()
    require(head==pre["frozen_parent"]["pinned_class_head"],
            "CLASS_HEAD_NOT_PINNED")
    require(v63.KB==pre["frozen_physics"]["KB"] and
            v63.TAUH0==pre["frozen_physics"]["tauH0"],
            "PHYSICAL_MODEL_CHANGED")

    p1,p3=args.lw01_prefix.resolve(),args.lw03_prefix.resolve()
    f1=pre["frozen_parent"]
    first_json=Path(str(p1)+".json")
    first_npz=Path(str(p1)+".npz")
    source_force=Path(str(p1)+"_forcing_force.dat")
    prior_json=Path(str(p3)+".json")
    prior_npz=Path(str(p3)+".npz")
    for path,wanted in (
        (first_json,f1["lw01_json_sha256"]),
        (first_npz,f1["lw01_npz_sha256"]),
        (source_force,f1["original_drude_forcing_sha256"]),
        (prior_json,f1["lw03_json_sha256"]),
        (prior_npz,f1["lw03_npz_sha256"])):
        require(path.is_file() and sha256(path)==wanted,
                "FROZEN_FILE_HASH_"+path.name)
    result1=json.loads(first_json.read_text())
    result3=json.loads(prior_json.read_text())
    require(result1["classification"]==
            "GE19_LINEAR_WEYL_NATIVE_SIGNED_TANGENT_NUMERICAL_PASS_OBSERVATIONAL_OPEN"
            and all(result1["gates"].values()),"LW01_NOT_PASS")
    require(result3["classification"]==
            "GE19_LW03_SOURCE_TIME_OPERATOR_OR_RADIAL_QUADRATURE_FAIL"
            and result3["gates"]["class_native_baseline"]
            and result3["gates"]["class_native_signed"]
            and not result3["gates"]["radial_quadrature"],"LW03_EVIDENCE_CHANGED")

    dest=args.output_prefix.resolve()
    dest_j=Path(str(dest)+".json")
    dest_n=Path(str(dest)+".npz")
    require(dest.parent.is_dir() and
            not dest_j.exists() and not dest_n.exists(),
            "OUTPUT_PREEXISTS_OR_PARENT_MISSING")

    with np.load(first_npz,allow_pickle=False) as file:
        kh_full=np.asarray(file["k_native_h"],float)
        mask=np.asarray(file["primary_mask"],bool)
        n_native_time_initial=len(file["z_native"])
    indices=np.where(mask.any(axis=1))[0]
    require(len(indices)==322 and n_native_time_initial==24,
            "FROZEN_PARENT_GRID")
    kh=kh_full[indices]
    with np.load(prior_npz,allow_pickle=False) as file:
        reference={k:file[k].copy() for k in file.files}
    for ell in ELLS:
        for key in ("chi","z","W","TW"):
            require(f"{key}_ell_{ell}" in reference,"LW03_FIELD_MISSING")

    # LW03 evaluated 262 redshifts = 257 from its four stored 65-point
    # projection paths plus five native-z control points. Its NPZ stores
    # ONLY the projection paths. LW04 intentionally replays those paths,
    # and must not require the five additional unarchived control nodes.
    for ell in ELLS:
        zz=np.asarray(reference[f"z_ell_{ell}"],float)
        require(zz.shape==(65,) and np.isfinite(zz).all() and
                np.all(np.diff(zz)>0),"LW03_Z_PATH_INVALID")
    query_z=np.unique(np.concatenate([reference[f"z_ell_{e}"]
                                       for e in ELLS]))
    require(query_z.size==257,"LW03_PROJECTED_REFERENCE_QUERY_Z_CHANGED")
    h=float(v63.START["H0"])/100.
    model=dict(v63.class_params())
    model.update({
        "output":"mPk,mTk",
        "lensing":"no",
        "k_per_decade_for_pk":80.,
        "k_per_decade_for_bao":560.,
        "P_k_max_h/Mpc":2.,
        "z_max_pk":5.,
        "k_output_values":", ".join(
            f"{k*h:.17g}" for k in
            pre["frozen_physics"]["k_output_values_h_per_Mpc"]),
        "perturbations_sampling_stepsize":cfg["refined_value"],
    })
    # Exactly three new CLASS solves, no coarse reruns.
    W0,k0,n_time,zbg,chibg=class_run(
        "baseline_fine",None,source_force,model,query_z,kh_full,indices)
    WP,kp,_,_,_=class_run(
        "plus_2p5_fine",+2.5,source_force,model,query_z,kh_full,indices)
    WM,km,_,_,_=class_run(
        "minus_2p5_fine",-2.5,source_force,model,query_z,kh_full,indices)
    TW=(WP-WM)/(2*pre["frozen_physics"]["signed_amplification_lambda"])
    require(np.isfinite(TW).all(),"REFINED_SIGNED_NONFINITE")

    chi_s_orig=float(result3["numerical_diagnostics"][
                        "class_source_plane_chi_Mpc"])
    chi_s_fine=float(np.interp(2.,zbg,chibg))
    max_geo=abs(chi_s_fine-chi_s_orig)/max(abs(chi_s_orig),TINY)
    g=pre["preregistered_checks"]
    checks={
        "source_time_grid_increased":
            n_time >= g["minimum_refined_native_time_nodes_relative_to_lw01"]
                      * n_native_time_initial,
        "class_k_exact_prefix":
            max(k0,kp,km)<=g["class_get_transfer_native_k_prefix_rel_max"],
        "source_chi_geometry":
            max_geo<=g["background_source_chi_relative_max"],
        "fine_transfer_finite":
            all(np.isfinite(x).all() for x in (W0,WP,WM,TW))
    }
    arrays={}
    rows=[]
    for ell in ELLS:
        chi=reference[f"chi_ell_{ell}"]
        z=reference[f"z_ell_{ell}"]
        old_W=reference[f"W_ell_{ell}"]
        old_TW=reference[f"TW_ell_{ell}"]
        idx=np.searchsorted(query_z,z)
        require(np.array_equal(query_z[idx],z),"EXACT_REDSHIFT_INDEX")
        new_W=W0[idx,:].T
        new_TW=TW[idx,:].T
        require(new_W.shape==old_W.shape==new_TW.shape==old_TW.shape
                and old_W.shape==(322,65),"LW03_SHAPE_CHANGED")
        werr=l2rel(new_W,old_W)
        twerr=l2rel(new_TW,old_TW)
        local_chi=np.interp(z,zbg,chibg)
        geo=float(np.max(abs(local_chi-chi)/np.maximum(abs(chi),TINY)))
        max_geo=max(max_geo,geo)
        c0,d0,a0=lw02.signed_projection_on_chi(
            ell,chi,chi_s_orig,kh*h,old_W,old_TW,
            float(v63.START["A_s"]),float(v63.START["n_s"]),True)
        c1,d1,a1=lw02.signed_projection_on_chi(
            ell,chi,chi_s_fine,kh*h,new_W,new_TW,
            float(v63.START["A_s"]),float(v63.START["n_s"]),True)
        relative_integral_change=float(abs(d1-d0)/max(a0,TINY))
        row_gates={
            "W_source_time_resolution":werr<=g["relative_L2_fine_vs_coarse_W_per_ell_max"],
            "signed_W_source_time_resolution":
                twerr<=g["relative_L2_fine_vs_coarse_signed_W_per_ell_max"],
            "integrated_signed_response_resolution":
                relative_integral_change<=g[
                    "absolute_signed_integral_change_normalized_by_original_integral_abs_per_ell_max"],
            "geometry":geo<=g["background_source_chi_relative_max"],
        }
        entry={
            "ell":ell,
            "n_chi":len(chi),
            "relative_L2_W_new_vs_LW03":werr,
            "relative_L2_signed_W_new_vs_LW03":twerr,
            "relative_chi_mismatch":geo,
            "coarse_LW03_signed_window_ratio":float(d0/c0),
            "refined_signed_window_ratio":float(d1/c1),
            "absolute_signed_integral_change_over_LW03_abs_integral":
                relative_integral_change,
            "radial_quadrature_already_failed_in_LW03":True,
            "gates":row_gates
        }
        rows.append(entry)
        arrays[f"W_refined_ell_{ell}"]=new_W
        arrays[f"TW_refined_ell_{ell}"]=new_TW
        print("GE19_LW04_ELL",ell,"W_L2",werr,"TW_L2",twerr,
              "DELTA_INT_ABS",relative_integral_change,
              "CHECKS",row_gates,flush=True)
    checks["all_ell_source_resolution_checks"]=all(
        all(entry["gates"].values()) for entry in rows)
    checks["all_ell_geometry"]=max_geo<=g["background_source_chi_relative_max"]

    passed=all(checks.values())
    outcome=(pre["outcomes"]["time_source_stability_pass"]
             if passed else pre["outcomes"]["time_source_stability_fail"])
    final={
        "classification":outcome,
        "predata_git_blob_sha1":PREDATA_GIT_BLOB,
        "frozen_parent_hashes":f1,
        "class_head":head,
        "sampling_stepsize_original":.1,
        "sampling_stepsize_fine":.025,
        "native_stored_time_points_original":n_native_time_initial,
        "native_stored_time_points_fine":n_time,
        "unique_z_queries":len(query_z),
        "class_k_prefix_relative_error_max":max(k0,kp,km),
        "class_source_chi_Mpc_coarse":chi_s_orig,
        "class_source_chi_Mpc_fine":chi_s_fine,
        "geometry_relative_error_max":max_geo,
        "gates":checks,
        "ell_results":rows,
        "scope":"One independent CLASS source-time SAMPLING change; no integrator tolerance change, no new physical coupling, no complete line of sight.",
        "LW01_native_signed_Weyl_numerical_PASS":True,
        "LW03_radial_quadrature_FAIL_preserved":True,
        "full_lensing_spectrum_certified":False,
        "physical_lensing_sign_certified":False,
        "observational_detection":False,
        "H4_Z21_certified":False,
    }
    dest_j.write_text(json.dumps(final,indent=2,sort_keys=True,
                                 allow_nan=False)+"\n")
    np.savez_compressed(dest_n,**arrays)
    print("GE19_LW04_CLASSIFICATION",outcome,flush=True)
    print("GE19_LW04_OUTPUT",str(dest_j),str(dest_n),flush=True)


if __name__=="__main__":
    main()
