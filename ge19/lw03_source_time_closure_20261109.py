#!/usr/bin/env python3
"""GE19 LW03: one prelocked source-time interpolation replay after LW02.

Three original CLASS linear solves (baseline, +2.5, -2.5), the exact LW01
external Drude forcing, and no new physics parameters, H4 or observed data.
CLASS.get_transfer(z) is a source-time INTERPOLATION OPERATOR, not fresh
independent evolution at every z. Converged quadrature of that operator
never certifies the physical sign or full lensing spectrum by itself.
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
from ge19 import lw02_windowed_lensing_20261109 as lw2

ROOT = Path(__file__).resolve().parents[1]
PRE = ROOT / "ge19/lw03_source_time_closure_predata_20261109.json"
TINY = 1.e-300


def require(test, msg):
    if not bool(test):
        raise RuntimeError("GE19_LW03_" + msg)


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def rel_l2(data, reference):
    return float(np.linalg.norm(data-reference) /
                 max(np.linalg.norm(reference), TINY))


def native_source_weyl(transfer, archived_k_h):
    kkey = next((s for s in ("k (h/Mpc)", "k [h/Mpc]", "k")
                 if s in transfer), None)
    require(kkey is not None and "phi" in transfer and "psi" in transfer,
            "CLASS_TRANSFER_KEYS")
    # classy.get_transfer(z) exposes pt.k_size[scalars] (the full scalar
    # perturbation k array), but get_transfer_and_k_and_z() and the
    # archived LW01 Fourier transfer use pt.k_size_pk (its INITIAL prefix).
    # The trailing scalar modes are not LW01 Fourier nodes; never
    # interpolate, truncate without a check, or relax k-match tolerance.
    kh_full = np.asarray(transfer[kkey], float)
    n_archive = archived_k_h.size
    require(kh_full.ndim == 1 and archived_k_h.ndim == 1 and
            kh_full.size >= n_archive, "CLASS_K_GRID_TOO_SHORT")
    kh = kh_full[:n_archive]
    kerr = float(np.max(abs(kh-archived_k_h) /
                        np.maximum(abs(archived_k_h), TINY)))
    require(kerr <= 1.0e-10, "CLASS_NATIVE_K_PREFIX_MISMATCH")
    phi = np.asarray(transfer["phi"], float)
    psi = np.asarray(transfer["psi"], float)
    require(phi.shape == psi.shape == kh_full.shape,
            "CLASS_FULL_WEYL_TRANSFER_SHAPE")
    W = .5*(phi[:n_archive] + psi[:n_archive])
    require(np.all(np.isfinite(W)), "WEYL_TRANSFER_NONFINITE")
    return W, kerr


def background_geometry(c, native_z, archived_chi):
    b = c.get_background()
    require("z" in b and "comov. dist." in b, "BACKGROUND_KEYS")
    z = np.asarray(b["z"], float)
    chi = np.asarray(b["comov. dist."], float)
    order = np.argsort(z)
    z, chi = z[order], chi[order]
    # Preserve one tabulated point above z_s=2 for an interpolation
    # bracket; CLASS does not necessarily store z=2 as an exact node.
    end = int(np.searchsorted(z, 2.0, side="right"))
    require(end < len(z), "BACKGROUND_SOURCE_COVERAGE")
    z, chi = z[:end+1], chi[:end+1]
    require(len(z) >= 20 and np.all(np.diff(z) > 0) and
            np.all(np.diff(chi) > 0), "BACKGROUND_MONOTONICITY")
    require(z[0] <= native_z[0] and z[-1] >= 2.0,
            "BACKGROUND_SOURCE_COVERAGE")
    chint = np.interp(native_z, z, chi)
    chi_source = float(np.interp(2.0, z, chi))
    geometry_err = float(np.max(abs(chint-archived_chi) /
                                np.maximum(abs(archived_chi), TINY)))
    return z, chi, chi_source, geometry_err


def source_run(lam, force, class_params, query_z, frozen_k_h,
               native_z=None, archived_chi=None):
    from classy import Class
    keys = ("AEST_TANGENT_FORCE_FILE", "AEST_TANGENT_LAMBDA",
            "AEST_OFFLINE_TRACE_FILE")
    saved = {x:os.environ.get(x) for x in keys}
    c = None
    try:
        os.environ.pop("AEST_OFFLINE_TRACE_FILE", None)
        if lam is None:
            os.environ.pop("AEST_TANGENT_FORCE_FILE", None)
            os.environ.pop("AEST_TANGENT_LAMBDA", None)
        else:
            os.environ["AEST_TANGENT_FORCE_FILE"] = str(force.resolve())
            os.environ["AEST_TANGENT_LAMBDA"] = str(float(lam))
        os.environ["OMP_NUM_THREADS"] = "1"
        c = Class()
        c.set(class_params)
        c.compute()
        geo = None
        if lam is None and native_z is not None:
            geo = background_geometry(c, native_z, archived_chi)
        if query_z is None:
            return None, None, geo
        arr = np.empty((len(query_z),len(frozen_k_h)))
        kerr = 0.
        for i, zi in enumerate(query_z):
            arr[i], err = native_source_weyl(
                c.get_transfer(float(zi), output_format="class"), frozen_k_h)
            kerr = max(kerr,err)
        return arr, kerr, geo
    finally:
        if c is not None:
            try:
                c.struct_cleanup()
                c.empty()
            except Exception:
                pass
        for k, v in saved.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v


def quadrature_levels(ell, chi, chi_s, kn, w, tw, As, ns):
    require(len(chi) == 65 and w.shape == tw.shape == (len(kn),65),
            "QUADRATURE_INPUT_SHAPE")
    out = {}
    for n, step in ((17,4),(33,2),(65,1)):
        out[n] = lw2.signed_projection_on_chi(
            ell, chi[::step],chi_s,kn,w[:,::step],tw[:,::step],As,ns,True)
    def rel(a,b):
        return abs(out[a][1]-out[b][1])/max(out[b][2],TINY)
    signs = [int(np.sign(out[n][1])) for n in (17,33,65)]
    return out,rel(17,33),rel(33,65),len(set(signs))==1 and signs[0]!=0


def selftest():
    chi = np.linspace(900.,2500.,65)
    k = np.geomspace(.01,1.,128)
    W = np.full((128,65),3.)
    TW = np.full_like(W,.15)
    levels,r1,r2,same = quadrature_levels(
        100,chi,3800.,k,W,TW,2.1e-9,.966)
    require(all(abs(levels[n][1]/levels[n][0]-.1)<1e-13
                for n in (17,33,65)), "SELFTEST_SIGNED_DERIVATIVE")
    require(same and r2<.005, "SELFTEST_NUMERICAL_QUADRATURE")
    levels2,_,_,same2=quadrature_levels(
        100,chi,3800.,k,W,-TW,2.1e-9,.966)
    require(same2 and levels2[65][1]<0,"SELFTEST_NEGATIVE_TANGENT")
    # A CLASS scalar transfer may have more k modes than the archived
    # native Fourier window. Test exact validated-prefix selection.
    karchive = np.geomspace(0.001, 0.2, 12)
    extra = np.array([0.21, 0.25, 0.35])
    full = np.concatenate((karchive, extra))
    mock = {"k (h/Mpc)":full, "phi":np.arange(15.,dtype=float),
            "psi":np.arange(15.,dtype=float)*2.0}
    w0, ke = native_source_weyl(mock,karchive)
    require(w0.size==12 and ke==0 and
            np.array_equal(w0,1.5*np.arange(12)),
            "SELFTEST_PREFIX_EXTRA_K")
    bad = dict(mock)
    bad["k (h/Mpc)"] = full.copy()
    bad["k (h/Mpc)"][4] *= 1.00001
    try:
        native_source_weyl(bad,karchive)
    except RuntimeError as exc:
        require("CLASS_NATIVE_K_PREFIX_MISMATCH" in str(exc),
                "SELFTEST_WRONG_K_REJECTION")
    else:
        raise RuntimeError("GE19_LW03_SELFTEST_BAD_K_ACCEPTED")
    print("GE19_LW03_SOURCE_TIME_SYNTHETIC_SELFTEST_PASS",flush=True)


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--self-test",action="store_true")
    a.add_argument("--class-root",type=Path)
    a.add_argument("--parent-prefix",type=Path,default=
                   ROOT/"results/ge19_linear_weyl_native_tangent_20261109_kgridfix")
    a.add_argument("--lw02-json",type=Path,default=
                   ROOT/"results/ge19_lw02_windowed_lensing_20261109.json")
    a.add_argument("--output-prefix",type=Path,default=
                   ROOT/"results/ge19_lw03_source_time_closure_20261109")
    args = a.parse_args()
    if args.self_test:
        selftest()
        return
    require(args.class_root is not None,"CLASS_ROOT_REQUIRED")
    pre = json.loads(PRE.read_text())
    # Frozen JSON uses "classification" for its outcome-label mapping.
    # The originally intended protocol label is not the value of that
    # field. Lock the Git blob and the actual outcome labels instead;
    # do not edit or re-freeze the already committed predata.
    predata_blob = subprocess.check_output(
        ["git", "hash-object", str(PRE)], text=True).strip()
    require(predata_blob == "f66323370f526faa3e4587795d91e72d4bd68c0b",
            "PREDATA_BLOB_CHANGED")
    outcomes = pre.get("classification")
    require(isinstance(outcomes, dict) and
            outcomes.get("pass") ==
              "GE19_LW03_CLASS_SOURCE_TIME_OPERATOR_CONSISTENT_WINDOW_QUADRATURE_PASS_FULL_LOS_OPEN" and
            outcomes.get("fail") ==
              "GE19_LW03_SOURCE_TIME_OPERATOR_OR_RADIAL_QUADRATURE_FAIL" and
            outcomes.get("implementation") ==
              "GE19_LW03_IMPLEMENTATION_BLOCKED",
            "PREDATA_NOT_LOCKED")
    require(pre["projection"]["ells"]==[100,150,200,300,500] and
            pre["projection"]["chi_sampling_nested"]==[17,33,65],
            "FROZEN_SAMPLING_CHANGED")
    require(v63.KB==.0665 and v63.TAUH0==10. and
            pre["frozen_model"]["signed_amplification_lambda"]==2.5,
            "FROZEN_MODEL_CHANGED")
    class_root = args.class_root.resolve()
    require((class_root/"class").is_file(), "CLASS_MISSING")
    head = subprocess.check_output(
        ["git","-C",str(class_root),"rev-parse","HEAD"],text=True).strip()
    require(head==pre["parent"]["class_head"],"CLASS_PIN_CHANGED")
    pp = args.parent_prefix.resolve()
    j1,p1,force = (Path(str(pp)+suffix) for suffix in
                   (".json",".npz","_forcing_force.dat"))
    j2 = args.lw02_json.resolve()
    for path,expected in (
        (j1,pre["parent"]["lw01_json_sha256"]),
        (p1,pre["parent"]["lw01_npz_sha256"]),
        (j2,pre["parent"]["lw02_json_sha256"]),
        (force,pre["parent"]["lw01_forcing_file_sha256"])):
        require(path.is_file() and sha256(path)==expected,
                "ORIGINAL_PARENT_HASH_"+path.name)
    j = json.loads(j1.read_text())
    require(j["classification"]==
            "GE19_LINEAR_WEYL_NATIVE_SIGNED_TANGENT_NUMERICAL_PASS_OBSERVATIONAL_OPEN"
            and all(j["gates"].values()), "LW01_NOT_CERTIFIED")
    lw2j = json.loads(j2.read_text())
    require(lw2j["classification"]==
            "GE19_LW02_WINDOW_RESTRICTED_THEORY_ONLY_LENSING_RESPONSE_OBSERVATIONAL_OPEN",
            "LW02_NOT_FROZEN")
    out = args.output_prefix.resolve()
    outj,outn = Path(str(out)+".json"),Path(str(out)+".npz")
    require(out.parent.is_dir() and not outj.exists() and not outn.exists(),
            "OUTPUT_ALREADY_EXISTS_OR_PARENT_MISSING")
    with np.load(p1,allow_pickle=False) as aa:
        d = {key:aa[key].copy() for key in aa.files}
    kh_all,zall,mask=d["k_native_h"],d["z_native"],d["primary_mask"]
    ii=np.where(mask.any(axis=1))[0]
    jj=np.where(mask.any(axis=0))[0][::-1]
    kh=kh_all[ii]
    native_z=zall[jj]
    native_chi=np.array(lw2j["class_geometry"]["window_chi_Mpc"],float)
    require(len(ii)==322 and len(jj)==8 and
            np.array_equal(native_z,np.array(lw2j["class_geometry"]["window_native_z"])),
            "NATIVE_PARENT_WINDOW_CHANGED")

    h=float(v63.START["H0"])/100.
    params=dict(v63.class_params())
    params.update({"output":"mPk,mTk","lensing":"no",
                   "k_per_decade_for_pk":80.,"k_per_decade_for_bao":560.,
                   "P_k_max_h/Mpc":2.,"z_max_pk":5.,
                   "k_output_values":", ".join(
                       f"{kh0*h:.17g}" for kh0 in
                       pre["frozen_model"]["k_output_values_h_per_Mpc"])})
    # Open the original baseline CLASS once, obtain its geometry, and use
    # the *same instance* to query all off-native redshifts. No fourth solve.
    from classy import Class
    keys=("AEST_TANGENT_FORCE_FILE","AEST_TANGENT_LAMBDA",
          "AEST_OFFLINE_TRACE_FILE")
    saved={k:os.environ.pop(k,None) for k in keys}
    c=None
    try:
        c=Class()
        c.set(params)
        c.compute()
        zb,chib,chi_s,geometry_err=background_geometry(
            c,native_z,native_chi)
        source_chi_parent=float(lw2j["class_geometry"]["source_plane_chi_Mpc"])
        require(abs(chi_s-source_chi_parent)/chi_s<1.e-8,
                "SOURCE_PLANE_GEOMETRY_CHANGED")
        plans=[]
        for e in lw2j["ell_results"]:
            if e["status"]=="INSUFFICIENT_NATIVE_Z_SUPPORT":
                plans.append({"ell":e["ell"],"support":False,
                              "native_nodes":e["native_z_nodes"]})
                continue
            z_used=np.array(e["native_z_used"],float)
            idx=np.array([np.argmin(abs(native_z-z)) for z in z_used])
            require(len(idx)>=4 and np.all(np.diff(idx)>0) and
                    np.all(abs(native_z[idx]-z_used)<1.e-13),
                    "ORIGINAL_ELL_SUPPORT_CHANGED")
            chi=np.linspace(native_chi[idx[0]],native_chi[idx[-1]],65)
            z=np.interp(chi,chib,zb)
            require(np.all(np.diff(z)>0),"DENSE_CHI_TO_Z")
            plans.append({"ell":e["ell"],"support":True,"chi":chi,"z":z,
                          "native_nodes":len(idx),"old_ratio":
                          e["fractional_derivative_per_unit_formal_eta"]})
        query_z=np.unique(np.concatenate(
            [native_z]+[e["z"] for e in plans if e["support"]]))
        print("GE19_LW03_CLASS_RUN baseline; query_z_count=",len(query_z),
              flush=True)
        W0=np.empty((len(query_z),len(kh_all)),float)
        ke0=0.
        for i,z in enumerate(query_z):
            W0[i],err=native_source_weyl(
                c.get_transfer(float(z),output_format="class"),kh_all)
            ke0=max(ke0,err)
    finally:
        if c is not None:
            try:
                c.struct_cleanup()
                c.empty()
            except Exception:
                pass
        for k,v in saved.items():
            if v is not None:
                os.environ[k]=v

    print("GE19_LW03_CLASS_RUN +2.5",flush=True)
    WP,keP,_=source_run(+2.5,force,params,query_z,kh_all)
    print("GE19_LW03_CLASS_RUN -2.5",flush=True)
    WM,keM,_=source_run(-2.5,force,params,query_z,kh_all)
    TW=(WP-WM)/5.
    native_indices=np.searchsorted(query_z,native_z)
    require(np.array_equal(query_z[native_indices],native_z),
            "NATIVE_TIME_INDEXING")
    archived_w=d["weyl_base"][np.ix_(ii,jj)].T
    archived_tw=d["weyl_tangents"][2][np.ix_(ii,jj)].T
    base_rel=rel_l2(W0[native_indices][:,ii],archived_w)
    tangent_rel=rel_l2(TW[native_indices][:,ii],archived_tw)
    k_err=max(ke0,keP,keM)
    g=pre["gates"]
    checks={
        "class_k_grid":k_err<=g["class_native_k_matching_relative_max"],
        "class_native_baseline":base_rel<=g["native_operator_baseline_W_relative_L2_max"],
        "class_native_signed":tangent_rel<=g["native_operator_signed_W_derivative_relative_L2_max"],
        "background_geometry":geometry_err<=g["geometry_chi_native_relative_max"],
        "finite_transfer":all(np.all(np.isfinite(x)) for x in (W0,WP,WM,TW))}
    report=[]
    npz={}
    for item in plans:
        ell=item["ell"]
        if not item["support"]:
            report.append({"ell":ell,"status":"UNCHANGED_INSUFFICIENT_NATIVE_SUPPORT",
                           "native_z_nodes":item["native_nodes"]})
            continue
        chi,z=item["chi"],item["z"]
        select=np.searchsorted(query_z,z)
        require(np.array_equal(query_z[select],z),"QUERY_Z_LOOKUP")
        w=W0[select][:,ii].T
        tw=TW[select][:,ii].T
        out17_33_65,coarse,fine,sign_ok=quadrature_levels(
            ell,chi,chi_s,kh*h,w,tw,
            float(v63.START["A_s"]),float(v63.START["n_s"]))
        c65,dc65,absdc=out17_33_65[65]
        qpass=bool(coarse<=g["radial_coarse_17_to_33_relative_over_abs_signed_integral_max"]
                   and fine<=g["radial_33_to_65_relative_over_abs_signed_integral_max"]
                   and sign_ok and c65>0)
        rr={"ell":ell,"status":"CLASS_SOURCE_TIME_WINDOW_REPLAY",
            "native_z_nodes":item["native_nodes"],"class_source_z_queries":65,
            "z_min":float(z[0]),"z_max":float(z[-1]),
            "original_LW02_ratio":float(item["old_ratio"]),
            "Ckappa_window":float((ell*(ell+1)/2)**2*c65),
            "dCkappa_window_deta":float((ell*(ell+1)/2)**2*dc65),
            "ratio_per_formal_eta":float(dc65/c65),
            "ratios_by_n":{str(n):float(out17_33_65[n][1]/out17_33_65[n][0])
                            for n in (17,33,65)},
            "signed_derivative_quadrature_error_17_33_over_abs":float(coarse),
            "signed_derivative_quadrature_error_33_65_over_abs":float(fine),
            "sign_17_33_65_consistent":bool(sign_ok),
            "quadrature_gate":qpass}
        report.append(rr)
        for name,arr in (("chi",chi),("z",z),("W",w),("TW",tw)):
            npz[name+"_ell_"+str(ell)]=arr
        print("GE19_LW03_ELL",ell,"RATIO",rr["ratio_per_formal_eta"],
              "17to33",coarse,"33to65",fine,"PASS",qpass,flush=True)
    checks["radial_quadrature"]=all(r["quadrature_gate"] for r in report
                                    if r["status"]=="CLASS_SOURCE_TIME_WINDOW_REPLAY")
    passed=all(checks.values())
    classification=("GE19_LW03_CLASS_SOURCE_TIME_OPERATOR_CONSISTENT_WINDOW_QUADRATURE_PASS_FULL_LOS_OPEN"
                    if passed else
                    "GE19_LW03_SOURCE_TIME_OPERATOR_OR_RADIAL_QUADRATURE_FAIL")
    final={
        "classification":classification,
        "predata_protocol":"GE19_LW03_OFFNATIVE_SOURCE_TIME_REPLAY_PREDATA_LOCKED",
        "predata_outcome_labels":pre["classification"],
        "predata_git_blob_sha1":predata_blob,
        "parent_sha256":{"lw01_json":sha256(j1),"lw01_npz":sha256(p1),
                         "lw02_json":sha256(j2),"forcing":sha256(force)},
        "numerical_diagnostics":{"source_time_native_baseline_relative_L2":base_rel,
            "source_time_native_lambda2p5_relative_L2":tangent_rel,
            "class_k_grid_relative_mismatch":k_err,
            "geometry_relative_mismatch":geometry_err,
            "class_source_plane_chi_Mpc":chi_s,
            "unique_offnative_source_redshift_queries":len(query_z)},
        "gates":checks,"ell_results":report,
        "scientific_scope":"One 3-solve CLASS get_transfer(z) source-time interpolation vs original LW01 native-time 8-z window; nested 17/33/65 radial quadrature.",
        "limitations":[
            "get_transfer(z) is CLASS source-time interpolation, NOT independent native-time evolution.",
            "Quadrature stability within this operator does NOT certify physical lensing sign.",
            "Different ell have different truncated redshift support.",
            "No full line of sight, no DES Y3 or other observational likelihood, no finite eta, no H4 Z21."],
        "physical_lensing_sign_certified":False,
        "full_lensing_spectrum_certified":False,
        "observational_detection":False,
        "H4_Z21_certified":False}
    outj.write_text(json.dumps(final,indent=2,sort_keys=True,allow_nan=False)+"\n")
    np.savez_compressed(outn,**npz)
    print("GE19_LW03_CLASSIFICATION",classification,flush=True)
    print("GE19_LW03_OUTPUT",str(outj),str(outn),flush=True)


if __name__=="__main__":
    main()
