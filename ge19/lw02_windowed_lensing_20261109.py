#!/usr/bin/env python3
"""GE19 LW02: one prelocked *window-only* Born+Limber Weyl-lensing projection.

Consumes frozen LW01 native signed Weyl data; runs one unforced eta=0
original patched CLASS instance solely for background comoving distance.
No new perturbed CLASS run, no fitted parameters, no observed survey data.
Outside the locked k,z window the line-of-sight contribution is unknown:
never label these partial integrals as full-sky/full-sight lensing power.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from v063 import theory_response_map as v63

PRE = ROOT / "ge19/lw02_windowed_lensing_predata_20261109.json"
TINY = 1e-300


def sha256(p):
    h = hashlib.sha256()
    with Path(p).open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def require(ok, message):
    if not bool(ok):
        raise RuntimeError("GE19_LW02_" + message)


def signed_projection_on_chi(ell, chi, chi_s, k_native, w, dw, As, ns, log_k=True):
    """One ell; every input row is an original native redshift slice.

    Returns (Cphi, dCphi/deta, absolute derivative integral), all for the
    *provided slice only*. Expects strictly increasing chi and k_native.
    """
    chi = np.asarray(chi, float)
    k_native = np.asarray(k_native, float)
    w, dw = np.asarray(w, float), np.asarray(dw, float)
    require(chi.ndim == 1 and chi.size >= 2 and np.all(np.diff(chi) > 0),
            "CHI_NOT_INCREASING")
    require(np.all(chi > 0) and np.all(chi < chi_s), "CHI_SOURCE_ORDER")
    require(k_native.ndim == 1 and np.all(np.diff(k_native) > 0),
            "NATIVE_K_NOT_INCREASING")
    require(w.shape == dw.shape == (k_native.size, chi.size), "TRANSFER_SHAPE")
    k = (ell + 0.5) / chi
    require(np.all((k >= k_native[0]) & (k <= k_native[-1])), "K_EXTRAPOLATION")

    if log_k:
        lookup, targets = np.log(k_native), np.log(k)
    else:
        lookup, targets = k_native, k
    W = np.array([np.interp(targets[i], lookup, w[:, i])
                  for i in range(chi.size)])
    dW = np.array([np.interp(targets[i], lookup, dw[:, i])
                   for i in range(chi.size)])
    primordial_power = (2 * np.pi**2 / k**3) * As * (k / 0.05)**(ns-1)
    weight = 4 * ((chi_s - chi) / (chi_s * chi))**2 / chi**2
    integrand = weight * primordial_power * W**2
    derivative_integrand = weight * primordial_power * 2 * W * dW
    # Integrate strictly across the supplied *native* redshift slices.
    Cphi = float(np.trapz(integrand, chi))
    dCphi = float(np.trapz(derivative_integrand, chi))
    abs_dCphi = float(np.trapz(np.abs(derivative_integrand), chi))
    return Cphi, dCphi, abs_dCphi


def selftest():
    k = np.geomspace(0.01, 1., 500)
    chi = np.array([900., 1200., 1600., 2000., 2500.])
    w = np.ones((k.size, chi.size)) * 3.
    dw = np.ones_like(w) * 0.15
    c, d, _ = signed_projection_on_chi(100, chi, 3800., k, w, dw,
                                       2.1e-9, .966, True)
    require(c > 0 and abs(d/c - 0.1) < 1e-13, "SELFTEST_POWER_TANGENT")
    c2, d2, _ = signed_projection_on_chi(100, chi, 3800., k, w, -dw,
                                         2.1e-9, .966, False)
    require(abs(c2-c)/c < 1e-13 and abs(d2+d)/abs(d) < 1e-13,
            "SELFTEST_SIGN")
    print("GE19_LW02_SIGNED_PROJECTOR_SYNTHETIC_SELFTEST_PASS")


def load_parent(npz_path, json_path, pre):
    require(sha256(npz_path) == pre["parent"]["NPZ_SHA256"],
            "ORIGINAL_PARENT_NPZ_SHA_MISMATCH")
    require(sha256(json_path) == pre["parent"]["JSON_SHA256"],
            "ORIGINAL_PARENT_JSON_SHA_MISMATCH")
    report = json.loads(json_path.read_text())
    require(report["classification"] == pre["parent"]["classification"],
            "PARENT_NOT_NUMERICAL_PASS")
    require(all(bool(v) for v in report["gates"].values()),
            "PARENT_GATES_NOT_ALL_PASS")
    require(report["class_official_HEAD"] == pre["parent"]["original_CLASS_HEAD"],
            "PARENT_CLASS_PIN_MISMATCH")

    with np.load(npz_path, allow_pickle=False) as a:
        data = {k: np.asarray(a[k]).copy() for k in a.files}
    k, z, mask = (data[key] for key in ("k_native_h","z_native","primary_mask"))
    w, dw, t = (data[key] for key in ("weyl_base",
                                     "weyl_signed_mean","weyl_tangents"))
    lam = data["lambdas"]
    require(k.shape == (pre["parent"]["n_native_k"],) and
            z.shape == (pre["parent"]["n_native_z"],),
            "PARENT_NATIVE_SHAPE")
    require(mask.shape == w.shape == dw.shape == (k.size,z.size),
            "PARENT_GRID_SHAPE")
    require(np.count_nonzero(mask) == pre["parent"]["n_primary_nodes"],
            "PARENT_PRIMARY_NODES")
    require(np.array_equal(mask, (k[:,None] >= .03) & (k[:,None] <= .2) &
                                   (z[None,:] >= .2) & (z[None,:] <= 1.5)),
            "PARENT_MASK_CHANGED")
    require(np.all(np.diff(k)>0) and np.all(np.diff(z)<0),
            "PARENT_GRID_ORIENTATION")
    require(np.array_equal(lam, [10.,5.,2.5,1.25]), "PARENT_LAMBDAS")
    require(np.all(np.isfinite(w)) and np.all(np.isfinite(dw)),
            "PARENT_TRANSFER_NONFINITE")
    np.testing.assert_allclose(0.5*(data["phi_base"]+data["psi_base"]),
                               w,rtol=1e-13,atol=1e-15)
    np.testing.assert_allclose(
        0.5*(data["phi_signed_mean"]+data["psi_signed_mean"]),
        dw,rtol=1e-12,atol=1e-13)
    np.testing.assert_allclose(
        (data["weyl_plus"]-data["weyl_minus"])/(2*lam[:,None,None]),
        t, rtol=0,atol=0)
    np.testing.assert_allclose(t.mean(axis=0),dw,rtol=0,atol=0)
    return data


def get_geometry(class_root, z_query, source_z, expected_head):
    class_root = Path(class_root).resolve()
    require((class_root/"class").is_file(), "CLASS_EXECUTABLE_MISSING")
    head = subprocess.check_output(
        ["git","-C",str(class_root),"rev-parse","HEAD"],text=True).strip()
    require(head == expected_head,"CLASS_HEAD_CHANGED")
    from classy import Class
    keys = ("AEST_TANGENT_FORCE_FILE","AEST_TANGENT_LAMBDA",
            "AEST_OFFLINE_TRACE_FILE")
    saved = {k:os.environ.pop(k,None) for k in keys}
    c = None
    try:
        c = Class()
        pars = dict(v63.class_params())
        pars.update({"lensing":"no", "output":"mPk,mTk"})
        c.set(pars)
        c.compute()
        bg = c.get_background()
        require(all(k in bg for k in ("z","comov. dist.")),
                "CLASS_BACKGROUND_COLUMNS_MISSING")
        zb = np.asarray(bg["z"],float)
        chib = np.asarray(bg["comov. dist."],float)
        order = np.argsort(zb)
        zb, chib = zb[order], chib[order]
        # At enormous early-time redshifts comoving distances can round to
        # the same floating-point value. Only [0,z_source] is relevant here.
        local = (zb <= source_z)
        require(np.all(np.diff(zb)>0) and
                np.all(np.isfinite(chib)) and
                np.count_nonzero(local)>10 and
                np.all(np.diff(chib[local])>0),
                "CLASS_BACKGROUND_GEOMETRY")
        require(zb[0] <= min(z_query) and source_z <= zb[-1],
                "CLASS_BACKGROUND_REDSHIFT_COVERAGE")
        chi = np.interp(z_query,zb,chib)
        chis = float(np.interp(source_z,zb,chib))
        require(np.all(np.diff(chi)>0) and np.all(chi<chis),
                "CLASS_NATIVE_GEOMETRY_ORDER")
        return chi, chis, {"background_z_points":int(len(zb)),
                           "background_z_min":float(zb[0]),
                           "background_z_max":float(zb[-1]),
                           "comoving_distance_column":"comov. dist.",
                           "class_HEAD":head}
    finally:
        if c is not None:
            try:
                c.struct_cleanup()
                c.empty()
            except Exception:
                pass
        for k, v in saved.items():
            if v is not None:
                os.environ[k] = v


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--self-test",action="store_true")
    p.add_argument("--class-root",type=Path)
    p.add_argument("--parent-prefix",type=Path,
                   default=ROOT/"results/ge19_linear_weyl_native_tangent_20261109_kgridfix")
    p.add_argument("--json-out",type=Path,
                   default=ROOT/"results/ge19_lw02_windowed_lensing_20261109.json")
    args=p.parse_args()
    if args.self_test:
        selftest()
        return
    require(args.class_root is not None,"CLASS_ROOT_REQUIRED")
    pre=json.loads(PRE.read_text())
    require(pre["classification"] ==
            "GE19_LW02_WINDOW_RESTRICTED_LINEAR_WEYL_LENSING_PREDATA_LOCK_BEFORE_LW02_EXECUTION",
            "PREDATA_CHANGED")
    require(pre["locked_projection"]["ell"] == [100,150,200,300,500],
            "ELLS_CHANGED")
    out=args.json_out.resolve()
    require(out.parent.is_dir() and not out.exists(), "OUTPUT_PREEXISTS_OR_DIR_MISSING")
    prefix=args.parent_prefix.resolve()
    npz_path=Path(str(prefix)+".npz")
    json_path=Path(str(prefix)+".json")
    d=load_parent(npz_path,json_path,pre)
    k_h, zn=d["k_native_h"],d["z_native"]
    z_indices=np.where(np.any(d["primary_mask"],axis=0))[0][::-1]
    k_indices=np.where(np.any(d["primary_mask"],axis=1))[0]
    z=zn[z_indices]
    require(z.size==8 and len(k_indices)==322, "PARENT_WINDOW_CHANGING")
    model=pre["physical_model"]
    require(float(model["KB"]) == v63.KB and
            float(model["tauH0"]) == v63.TAUH0 and
            float(model["source_plane_redshift"])==2.0,
            "FROZEN_MODEL_CHANGED")
    source_z=float(model["source_plane_redshift"])
    chi, chis, geom=get_geometry(args.class_root,z,source_z,
                                pre["parent"]["original_CLASS_HEAD"])
    h=float(v63.START["H0"])/100
    kn=k_h[k_indices]*h # Physical wavenumbers [1/Mpc].
    W=d["weyl_base"][np.ix_(k_indices,z_indices)]
    TW=d["weyl_signed_mean"][np.ix_(k_indices,z_indices)]
    As=float(v63.START["A_s"]);ns=float(v63.START["n_s"])
    require(np.all(np.diff(kn)>0) and np.all(np.diff(chi)>0),
            "INVALID_NATIVE_WINDOW")
    results=[]
    for ell in pre["locked_projection"]["ell"]:
        kl=(float(ell)+.5)/chi
        used=(kl>=kn[0])&(kl<=kn[-1])
        idx=np.where(used)[0]
        if idx.size<pre["locked_projection"]["minimum_native_redshift_nodes_for_report"]:
            results.append({"ell":ell,"status":"INSUFFICIENT_NATIVE_Z_SUPPORT",
                            "native_z_nodes":int(idx.size),
                            "native_z_used":z[idx].tolist()})
            continue
        require(np.array_equal(idx,np.arange(idx[0],idx[-1]+1)),
                "ANGULAR_SUPPORT_NONCONTIGUOUS")
        kw=kn
        cw,cd,ad=signed_projection_on_chi(
            ell,chi[idx],chis,kw,W[:,idx],TW[:,idx],As,ns,True)
        aw,bd,ab=signed_projection_on_chi(
            ell,chi[idx],chis,kw,W[:,idx],TW[:,idx],As,ns,False)
        require(np.isfinite([cw,cd,ad,aw,bd,ab]).all() and cw>0,
                "NONFINITE_PROJECTED_RESPONSE")
        factor=(ell*(ell+1)/2)**2
        results.append({
            "ell":ell,"status":"WINDOW_RESTRICTED_PROJECTED_RESPONSE",
            "native_z_nodes":int(len(idx)),
            "native_z_used":[float(v) for v in z[idx]],
            "native_z_min":float(z[idx[0]]),
            "native_z_max":float(z[idx[-1]]),
            "sampled_k_h_per_Mpc_min":float(np.min(kl[idx])/h),
            "sampled_k_h_per_Mpc_max":float(np.max(kl[idx])/h),
            "C_ell_kappakappa_window":float(factor*cw),
            "dC_ell_kappakappa_window_deta":float(factor*cd),
            "fractional_derivative_per_unit_formal_eta":float(cd/cw),
            "log_vs_linear_k_interpolation_baseline_relative":
                float(abs(aw-cw)/max(abs(cw),TINY)),
            "log_vs_linear_k_interpolation_derivative_over_abs_integral":
                float(abs(bd-cd)/max(ad,TINY)),
            "absolute_signed_derivative_cancellation_fraction":
                float(abs(cd)/max(ad,TINY)),
            "geometry_warning":"Only the native and angularly supported k,z subwindow is integrated; it is not the full lensing line of sight."
        })
        print("GE19_LW02_ELL",ell,"Z_NODES",len(idx),
              "Ckappa_partial",factor*cw,"dC_deta_partial",factor*cd,
              "ratio",cd/cw,flush=True)
    result={
        "classification":"GE19_LW02_WINDOW_RESTRICTED_THEORY_ONLY_LENSING_RESPONSE_OBSERVATIONAL_OPEN",
        "parent_classification":pre["parent"]["classification"],
        "predata_classification":pre["classification"],
        "original_parent_sha256":{"npz":sha256(npz_path),
                                  "json":sha256(json_path)},
        "class_geometry":{"source_plane_z":source_z,
                          "source_plane_chi_Mpc":float(chis),
                          "window_native_z":z.tolist(),
                          "window_chi_Mpc":chi.tolist(),**geom},
        "primary_native_window":{"k_h_per_Mpc":[.03,.2],"z":[.2,1.5],
                                 "actual_native_z_min":float(z[0]),
                                 "actual_native_z_max":float(z[-1]),
                                 "n_native_z":int(len(z)),
                                 "n_native_k":int(len(kn))},
        "ell_results":results,
        "physical_scope":"Born+Limber signed eta=0 derivative in a STRICTLY WINDOWED fixed z_s=2 thin-source-plane projection; CLASS original model background; one geometry solve and no new perturbed solves.",
        "limitations":[
            "Not full lensing power: contributions outside parent 0.2<=z<=1.5 and 0.03<=k<=0.2 h/Mpc are unavailable.",
            "Only eight original native redshift nodes: no numerical z-integration convergence claim.",
            "Native-k interpolation is evaluated with two schemes; no new native-time interpolation.",
            "Thin source plane z=2 is an illustrative kernel, not a DES Y3 survey selection function.",
            "No measured sky comparison, likelihood, signal-to-noise, finite physical eta, or detection.",
            "No Z21/H4 certification; no nonlinear power or lensing."
        ],
        "full_lensing_spectrum_certified":False,
        "observational_detection":False,
        "H4_Z21_certified":False
    }
    out.write_text(json.dumps(result,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print("GE19_LW02_OUTPUT",str(out),flush=True)


if __name__=="__main__":
    main()
