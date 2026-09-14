#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import subprocess
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PREDATA_LOCK = "05d338e1dde7719cc78b132cd146a408c6a90d62"
R5B_POSTDATA_LOCK = "3242335ece23fbeb743f075a1df1aa70acaab211"
R5B_JSON = ROOT / "results/stable_aest_observable_projection_r5b_derivative_zero.json"
R5B_NPZ = ROOT / "results/stable_aest_observable_projection_r5b_derivative_zero.npz"
R5B_JSON_SHA256 = "26ce723e2b7b783fcd19765c9c7f01b6101992a3f09e6ee321299bf148259ca9"
R5B_NPZ_SHA256 = "a88f99254bc1a7393e40691d5dc539bb1e1648eae1b892e43b63f593f8e367e1"
R5B_CLASS = "STABLE_AEST_OBSERVABLE_PROJECTION_R5B_DERIVATIVE_ZERO_CERTIFIED"

ACT_COMMIT = "b386ddbb5821c1216c709f051c9289292f174d30"
ACT_INTERNAL_VERSION = "1.2.0"
ACT_DATA_VERSION = "v1.2"
ACT_VARIANT = "act_baseline"
NSIMS_ACT = 796
TRIM_LMAX = 2998
ETA_GRID = (0.0, 0.01, 0.025, 0.05)
SUPPORT_TOL = 1e-10
CONTROL_CHI2 = 14.06
CONTROL_TOL = 0.10
GLS_TOL = 1e-10

CLS_INCOMPLETE = "STABLE_AEST_ACT_DR6_R6A_INCOMPLETE"
CLS_PARENT = "STABLE_AEST_ACT_DR6_R6A_PARENT_PROVENANCE_FAIL"
CLS_INTERFACE = "STABLE_AEST_ACT_DR6_R6A_OFFICIAL_INTERFACE_FAIL"
CLS_SUPPORT = "STABLE_AEST_ACT_DR6_R6A_TEMPLATE_SUPPORT_FAIL"
CLS_ALG = "STABLE_AEST_ACT_DR6_R6A_PROJECTION_ALGEBRA_FAIL"
CLS_GLS = "STABLE_AEST_ACT_DR6_R6A_MATCHED_FILTER_GLS_FAIL"
CLS_PASS = "STABLE_AEST_ACT_DR6_R6A_FIXED_TEMPLATE_PROJECTION_CERTIFIED"

CONSUMED_DATA = (
    "clkk_bandpowers_act.txt",
    "binning_matrix_act.txt",
    "covmat_act_cmbmarg.txt",
    "covmat_act.txt",
    "like_corrs/cosmo2017_10K_acc3_lensedCls.dat",
    "like_corrs/cosmo2017_10K_acc3_lenspotentialCls.dat",
)


def ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def git_head(path: Path) -> str:
    p = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "HEAD"],
        check=True,
        text=True,
        capture_output=True,
    )
    return p.stdout.strip()


def qform(x, cinv) -> float:
    xx = np.asarray(x, float)
    return float(xx @ cinv @ xx)


def dotc(a, b, cinv) -> float:
    return float(np.asarray(a, float) @ cinv @ np.asarray(b, float))


def official_control(alike, ddir: Path):
    d = alike.load_data(
        ACT_VARIANT,
        ddir=str(ddir),
        lens_only=True,
        apply_hartlap=True,
        like_corrections=False,
        nsims_act=NSIMS_ACT,
        trim_lmax=TRIM_LMAX,
        version=ACT_DATA_VERSION,
    )

    ell, cl_tt, cl_ee, cl_bb, cl_te = np.loadtxt(
        ddir / "like_corrs/cosmo2017_10K_acc3_lensedCls.dat",
        unpack=True,
    )
    raw = np.loadtxt(
        ddir / "like_corrs/cosmo2017_10K_acc3_lenspotentialCls.dat",
        unpack=True,
    )
    ellp = raw[0]
    cl_pp = raw[5]

    prefac = 2.0 * np.pi / ell / (ell + 1.0)
    cl_kk = cl_pp / 4.0 * 2.0 * np.pi
    cl_tt = cl_tt * prefac
    cl_ee = cl_ee * prefac
    cl_bb = cl_bb * prefac
    cl_te = cl_te * prefac

    lnlike = alike.generic_lnlike(
        d,
        ellp,
        cl_kk,
        ell,
        cl_tt,
        cl_ee,
        cl_te,
        cl_bb,
        trim_lmax=TRIM_LMAX,
    )
    return d, float(-2.0 * lnlike)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--json-out",
        default="results/stable_aest_act_dr6_r6a_fixed_template_projection.json",
    )
    ap.add_argument(
        "--npz-out",
        default="results/stable_aest_act_dr6_r6a_fixed_template_projection.npz",
    )
    args = ap.parse_args()

    print("STABLE_AEST_ACT_DR6_R6A_START", flush=True)

    parent_ok = R5B_JSON.is_file() and R5B_NPZ.is_file()
    parent_meta = {}
    if parent_ok:
        json_sha = sha256(R5B_JSON)
        npz_sha = sha256(R5B_NPZ)
        parent = json.loads(R5B_JSON.read_text())
        parent_meta = {
            "json_sha256": json_sha,
            "npz_sha256": npz_sha,
            "classification": parent.get("classification"),
        }
        g1 = bool(
            ancestor(PREDATA_LOCK)
            and ancestor(R5B_POSTDATA_LOCK)
            and json_sha == R5B_JSON_SHA256
            and npz_sha == R5B_NPZ_SHA256
            and parent.get("classification") == R5B_CLASS
            and parent.get("diagnostic_complete") is True
            and all(bool(v) for v in parent.get("gates", {}).values())
        )
    else:
        parent = {}
        g1 = False

    act_source = Path(os.environ.get("R6A_ACT_SOURCE_ROOT", ""))
    manifest = {}
    interface_meta = {}
    data_dict = None
    control_chi2 = float("nan")
    g2 = False
    g3 = False
    try:
        import act_dr6_lenslike as alike

        pkg_dir = Path(alike.__file__).resolve().parent
        ddir = pkg_dir / "data" / ACT_DATA_VERSION
        head = git_head(act_source) if act_source.is_dir() else ""
        module_path = pkg_dir / "act_dr6_lenslike.py"
        init_path = pkg_dir / "__init__.py"
        for rel in CONSUMED_DATA:
            p = ddir / rel
            if p.is_file():
                manifest[str(rel)] = {
                    "sha256": sha256(p),
                    "bytes": p.stat().st_size,
                }
        if module_path.is_file():
            manifest["PACKAGE/act_dr6_lenslike.py"] = {
                "sha256": sha256(module_path),
                "bytes": module_path.stat().st_size,
            }
        if init_path.is_file():
            manifest["PACKAGE/__init__.py"] = {
                "sha256": sha256(init_path),
                "bytes": init_path.stat().st_size,
            }

        internal_version = str(getattr(alike, "__version__", ""))
        complete_manifest = all(rel in manifest for rel in CONSUMED_DATA)
        g2 = bool(
            head == ACT_COMMIT
            and internal_version == ACT_INTERNAL_VERSION
            and ddir.is_dir()
            and complete_manifest
        )
        interface_meta = {
            "act_source_head": head,
            "internal_version": internal_version,
            "release_tag": "v1.2.1",
            "data_version": ACT_DATA_VERSION,
            "variant": ACT_VARIANT,
            "lens_only": True,
            "like_corrections": False,
            "apply_hartlap": True,
            "nsims_act": NSIMS_ACT,
            "trim_lmax": TRIM_LMAX,
            "data_dir": str(ddir),
            "manifest_complete": complete_manifest,
        }

        if g2:
            data_dict, control_chi2 = official_control(alike, ddir)
            g3 = bool(
                np.isfinite(control_chi2)
                and abs(control_chi2 - CONTROL_CHI2) <= CONTROL_TOL
            )
    except Exception as exc:
        interface_meta["error"] = repr(exc)

    print(
        "STABLE_AEST_ACT_DR6_R6A_INTERFACE "
        + json.dumps(
            {
                "g2": g2,
                "g3": g3,
                "control_chi2": control_chi2,
                **interface_meta,
            },
            sort_keys=True,
        ),
        flush=True,
    )

    support_meta = {}
    projection = {}
    overlap = {}
    arrays = {}
    g4 = g5 = g6 = False

    if g1 and g2 and g3 and data_dict is not None:
        q = np.load(R5B_NPZ)
        required = ("ell", "ckk_nominal_e0", "T_ckk_eta0p01")
        has_required = all(k in q.files for k in required)
        if has_required:
            ell = np.asarray(q["ell"], float)
            c0 = np.asarray(q["ckk_nominal_e0"], float)
            T = np.asarray(q["T_ckk_eta0p01"], float)

            exact_grid = bool(
                ell.shape == (1961,)
                and np.array_equal(ell, np.arange(40.0, 2001.0))
                and c0.shape == ell.shape
                and T.shape == ell.shape
            )
            parent_finite = bool(
                np.all(np.isfinite(c0))
                and np.all(c0 > 0.0)
                and np.all(np.isfinite(T))
            )

            B = np.asarray(data_dict["binmat_act"], float)
            nL = B.shape[1]
            Lfull = np.arange(nL, dtype=int)
            outside = (Lfull < 40) | (Lfull > 2000)
            abs_all = float(np.sum(np.abs(B)))
            abs_out = float(np.sum(np.abs(B[:, outside])))
            support_frac = abs_out / max(abs_all, 1e-300)
            row_den = np.sum(np.abs(B), axis=1)
            row_out = np.sum(np.abs(B[:, outside]), axis=1)
            row_frac = row_out / np.maximum(row_den, 1e-300)
            max_row_frac = float(np.max(row_frac))

            g4 = bool(
                exact_grid
                and parent_finite
                and nL == TRIM_LMAX + 2
                and np.all(np.isfinite(B))
                and support_frac <= SUPPORT_TOL
            )
            support_meta = {
                "exact_parent_grid": exact_grid,
                "parent_finite_positive": parent_finite,
                "binmat_shape": list(B.shape),
                "total_abs_outside_support_fraction": support_frac,
                "max_row_abs_outside_support_fraction": max_row_frac,
                "threshold": SUPPORT_TOL,
                "bcents_act": np.asarray(data_dict["bcents_act"], float).tolist(),
            }

            if g4:
                c0_full = np.zeros(nL, float)
                T_full = np.zeros(nL, float)
                idx = ell.astype(int)
                c0_full[idx] = c0
                T_full[idx] = T
                dC_full = c0_full * T_full

                b0 = B @ c0_full
                t = B @ dC_full
                data = np.asarray(data_dict["data_binned_clkk"], float)
                cov = np.asarray(data_dict["cov"], float)
                cinv = np.asarray(data_dict["cinv"], float)

                a = b0.copy()
                aa = dotc(a, a, cinv)
                at = dotc(a, t, cinv)
                tt = dotc(t, t, cinv)
                rho = at / math.sqrt(max(aa * tt, 1e-300))
                t_perp = t - a * (at / aa)
                F_perp = qform(t_perp, cinv)
                sigma_shape = 1.0 / math.sqrt(F_perp) if F_perp > 0 else float("inf")

                cov_sym = bool(np.allclose(cov, cov.T, rtol=1e-12, atol=1e-18))
                frozen_models = {}
                physical_positive = True
                for eta in ETA_GRID:
                    spec = c0 * (1.0 + eta * T)
                    physical_positive &= bool(np.all(np.isfinite(spec)) and np.all(spec > 0.0))
                    frozen_models[f"{eta:g}"] = b0 + eta * t

                finite_projection = bool(
                    np.all(np.isfinite(data))
                    and np.all(np.isfinite(cov))
                    and np.all(np.isfinite(cinv))
                    and np.all(np.isfinite(b0))
                    and np.all(np.isfinite(t))
                    and np.all(np.isfinite(t_perp))
                    and all(np.all(np.isfinite(v)) for v in frozen_models.values())
                )
                g5 = bool(
                    finite_projection
                    and cov_sym
                    and aa > 0.0
                    and tt > 0.0
                    and F_perp > 0.0
                    and physical_positive
                )

                projection = {
                    "nbins": int(data.size),
                    "F_raw": tt,
                    "F_perp": F_perp,
                    "rho_amplitude_memory": rho,
                    "sigma_eta_shape_fixed_baseline": sigma_shape,
                    "covariance_symmetric": cov_sym,
                    "physical_local_model_positive": physical_positive,
                }

                if g5:
                    r = data - b0
                    eta_hat = dotc(t_perp, r, cinv) / F_perp
                    sigma_hat = sigma_shape

                    try:
                        L = np.linalg.cholesky(cinv)
                        W = L.T
                        sa = math.sqrt(aa)
                        st = math.sqrt(tt)
                        Xs = np.column_stack([a / sa, t / st])
                        gamma, _, _, _ = np.linalg.lstsq(W @ Xs, W @ r, rcond=None)
                        deltaA_gls = float(gamma[0] / sa)
                        eta_gls = float(gamma[1] / st)
                        diff = abs(eta_hat - eta_gls)
                        scale = max(1.0, abs(eta_hat), abs(eta_gls))
                        gls_agree = bool(diff <= GLS_TOL * scale)
                    except Exception as exc:
                        deltaA_gls = eta_gls = float("nan")
                        diff = float("inf")
                        gls_agree = False
                        overlap["gls_error"] = repr(exc)

                    chi2_fixed = {}
                    chi2_profiled = {}
                    for eta in ETA_GRID:
                        rr = data - (b0 + eta * t)
                        chi2_fixed[f"{eta:g}"] = qform(rr, cinv)
                        deltaA = dotc(a, r - eta * t, cinv) / aa
                        rr_prof = r - deltaA * a - eta * t
                        chi2_profiled[f"{eta:g}"] = qform(rr_prof, cinv)

                    eta_phys = min(max(eta_hat, 0.0), 0.05)
                    deltaA_phys = dotc(a, r - eta_phys * t, cinv) / aa
                    rr_phys = r - deltaA_phys * a - eta_phys * t
                    chi2_phys_min = qform(rr_phys, cinv)

                    g6 = gls_agree
                    overlap.update(
                        {
                            "chi2_fixed_eta_grid": chi2_fixed,
                            "chi2_profiled_amplitude_eta_grid": chi2_profiled,
                            "eta_hat_signed_diagnostic": eta_hat,
                            "sigma_hat_fixed_baseline": sigma_hat,
                            "eta_hat_over_sigma": eta_hat / sigma_hat,
                            "gls_deltaA": deltaA_gls,
                            "gls_eta": eta_gls,
                            "matched_filter_gls_abs_diff": diff,
                            "matched_filter_gls_agree": gls_agree,
                            "physical_profile_eta_clipped": eta_phys,
                            "physical_profile_deltaA": deltaA_phys,
                            "physical_profile_chi2_min": chi2_phys_min,
                        }
                    )

                    arrays = {
                        "data_binned_clkk": data,
                        "bcents_act": np.asarray(data_dict["bcents_act"], float),
                        "b0": b0,
                        "memory_template": t,
                        "memory_template_perp": t_perp,
                        "cov": cov,
                        "cinv": cinv,
                        "ell_parent": ell,
                        "ckk_parent_eta0": c0,
                        "T_ckk_eta0p01": T,
                    }
                    for eta, bb in frozen_models.items():
                        arrays[f"bmodel_eta_{eta.replace('.', 'p')}"] = bb

    gates = {
        "R6A_G1_parent_provenance": g1,
        "R6A_G2_official_ACT_likelihood_provenance": g2,
        "R6A_G3_official_interface_control": g3,
        "R6A_G4_template_domain_support_validity": g4,
        "R6A_G5_bandpower_template_algebra": g5,
        "R6A_G6_matched_filter_GLS_agreement": g6,
    }

    if not parent_ok:
        cls = CLS_INCOMPLETE
    elif not g1:
        cls = CLS_PARENT
    elif not g2 or not g3:
        cls = CLS_INTERFACE
    elif not g4:
        cls = CLS_SUPPORT
    elif not g5:
        cls = CLS_ALG
    elif not g6:
        cls = CLS_GLS
    else:
        cls = CLS_PASS

    out = {
        "classification": cls,
        "diagnostic_complete": bool(parent_ok),
        "predata_lock": PREDATA_LOCK,
        "r5b_postdata_lock": R5B_POSTDATA_LOCK,
        "parent": parent_meta,
        "official_interface": {
            **interface_meta,
            "control_chi2": control_chi2,
            "control_target": CONTROL_CHI2,
            "control_tolerance": CONTROL_TOL,
        },
        "consumed_file_manifest": manifest,
        "support": support_meta,
        "projection": projection,
        "data_overlap": overlap,
        "settings": {
            "act_release_tag": "v1.2.1",
            "act_commit": ACT_COMMIT,
            "act_internal_version_expected": ACT_INTERNAL_VERSION,
            "data_version": ACT_DATA_VERSION,
            "variant": ACT_VARIANT,
            "lens_only": True,
            "like_corrections": False,
            "apply_hartlap": True,
            "nsims_act": NSIMS_ACT,
            "trim_lmax": TRIM_LMAX,
            "physical_eta_grid": list(ETA_GRID),
            "r5b_ell_min": 40,
            "r5b_ell_max": 2000,
            "nonlinear_halofit": False,
        },
        "gates": gates,
        "interpretation": {
            "fixed_template_projection_licensed": cls == CLS_PASS,
            "fixed_cosmology_data_overlap_licensed": cls == CLS_PASS,
            "cosmological_parameter_constraint_licensed": False,
            "observational_detection_claim_licensed": False,
            "likelihood_preference_claim_licensed": False,
            "negative_signed_eta_physical_interpretation_licensed": False,
            "positive_growth_weyl_separation_licensed": False,
        },
    }

    Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    if arrays:
        np.savez_compressed(args.npz_out, **arrays)
    else:
        np.savez_compressed(args.npz_out)

    print("STABLE_AEST_ACT_DR6_R6A_GATES=" + json.dumps(gates, sort_keys=True), flush=True)
    print(
        "STABLE_AEST_ACT_DR6_R6A_SUMMARY="
        + json.dumps(
            {
                "classification": cls,
                "control_chi2": control_chi2,
                "support": support_meta,
                "projection": projection,
                "data_overlap": overlap,
            },
            sort_keys=True,
        ),
        flush=True,
    )
    print("STABLE_AEST_ACT_DR6_R6A_CLASSIFICATION=" + cls, flush=True)
    return 0 if cls == CLS_PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
