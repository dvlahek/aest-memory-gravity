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
from fullj_weyl import stable_aest_act_dr6_r6a_fixed_template_projection as r6a

PREFIT_LOCK = "4c46fd21df048553b577a1927d8404bc493f649e"
R6A_POSTDATA_LOCK = "540f8f85c618209abb509e3c9c7dc188698d8e25"
R8A2_POSTDATA_LOCK = "590dbc69e2823f583b157af2297e357991103c47"
R8A2_JSON = ROOT / "results/stable_aest_cosmic_memory_r8a2_precision_qualified_tau_scan.json"
R8A2_NPZ = ROOT / "results/stable_aest_cosmic_memory_r8a2_precision_qualified_tau_scan.npz"
R8A2_JSON_SHA256 = "2d6289c2fbd37bebcb904dade89f64c15a009e5c7454754b39d4dcc72924ca66"
R8A2_NPZ_SHA256 = "c81b2093a88719423e87ff5c180d790a56da6f396c0070858624879c90f26ee1"
R8A2_CLASS = "STABLE_AEST_COSMIC_MEMORY_R8A2_TAU_GENERALITY_CERTIFIED"

ACT_COMMIT = "b386ddbb5821c1216c709f051c9289292f174d30"
ACT_INTERNAL_VERSION = "1.2.0"
ACT_DATA_VERSION = "v1.2"
ACT_VARIANT = "act_baseline"
NSIMS_ACT = 796
TRIM_LMAX = 2998
CONTROL_CHI2 = 14.06
CONTROL_TOL = 0.10
SUPPORT_TOL = 1e-10
BASELINE_TAU_TOL = 1e-8
CENTRAL_E_TOL = 0.10
CENTRAL_C_TOL = 0.995
TAU_C_TOL = 0.98
ALG_TOL = 1e-10
GLS_TOL = 1e-10
TAUS = (10.0, 5.0, 2.5, 1.25)
ETA_GRID = (0.0, 0.01, 0.025, 0.05)

CLS_PARENT = "STABLE_AEST_ACT_DR6_R10A_PARENT_PROVENANCE_FAIL"
CLS_INTERFACE = "STABLE_AEST_ACT_DR6_R10A_OFFICIAL_INTERFACE_FAIL"
CLS_SUPPORT = "STABLE_AEST_ACT_DR6_R10A_SUPPORT_BASELINE_FAIL"
CLS_CENTRAL = "STABLE_AEST_ACT_DR6_R10A_LIVE_CENTRAL_DERIVATIVE_FAIL"
CLS_ALG = "STABLE_AEST_ACT_DR6_R10A_PROJECTION_ALGEBRA_FAIL"
CLS_GLS = "STABLE_AEST_ACT_DR6_R10A_MATCHED_FILTER_GLS_FAIL"
CLS_TAU = "STABLE_AEST_ACT_DR6_R10A_TAU_COHERENCE_FAIL"
CLS_PASS = "STABLE_AEST_ACT_DR6_R10A_LIVE_WEYL_MEMORY_PROJECTION_CERTIFIED"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"], cwd=ROOT,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    ).returncode == 0


def git_head(path: Path) -> str:
    return subprocess.check_output(["git", "-C", str(path), "rev-parse", "HEAD"], text=True).strip()


def tau_tag(tau: float) -> str:
    return str(float(tau)).replace(".", "p")


def rel(a, b) -> float:
    aa = np.asarray(a, float); bb = np.asarray(b, float)
    return float(np.linalg.norm(aa - bb) / max(float(np.linalg.norm(aa)), float(np.linalg.norm(bb)), 1e-300))


def cosine(a, b) -> float:
    aa = np.asarray(a, float); bb = np.asarray(b, float)
    na = float(np.linalg.norm(aa)); nb = float(np.linalg.norm(bb))
    if na <= 0.0 or nb <= 0.0:
        return float("nan")
    return float(np.dot(aa, bb) / (na * nb))


def qform(x, cinv) -> float:
    xx = np.asarray(x, float)
    return float(xx @ cinv @ xx)


def dotc(a, b, cinv) -> float:
    return float(np.asarray(a, float) @ cinv @ np.asarray(b, float))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json-out", default="results/stable_aest_act_dr6_r10a_live_weyl_memory_projection.json")
    ap.add_argument("--npz-out", default="results/stable_aest_act_dr6_r10a_live_weyl_memory_projection.npz")
    args = ap.parse_args()
    print("STABLE_AEST_ACT_DR6_R10A_START", flush=True)

    parent_meta = {}
    q = None
    g1 = False
    if R8A2_JSON.is_file() and R8A2_NPZ.is_file():
        jsha = sha256(R8A2_JSON); nsha = sha256(R8A2_NPZ)
        r8j = json.loads(R8A2_JSON.read_text())
        constants_ok = bool(
            r6a.ACT_COMMIT == ACT_COMMIT
            and r6a.ACT_INTERNAL_VERSION == ACT_INTERNAL_VERSION
            and r6a.ACT_DATA_VERSION == ACT_DATA_VERSION
            and r6a.ACT_VARIANT == ACT_VARIANT
            and r6a.NSIMS_ACT == NSIMS_ACT
            and r6a.TRIM_LMAX == TRIM_LMAX
        )
        g1 = bool(
            ancestor(PREFIT_LOCK) and ancestor(R6A_POSTDATA_LOCK) and ancestor(R8A2_POSTDATA_LOCK)
            and jsha == R8A2_JSON_SHA256 and nsha == R8A2_NPZ_SHA256
            and r8j.get("classification") == R8A2_CLASS
            and r8j.get("diagnostic_complete") is True
            and all(bool(v) for v in r8j.get("gates", {}).values())
            and constants_ok
        )
        if g1:
            q = np.load(R8A2_NPZ)
        parent_meta = {
            "r6a_postdata_lock": R6A_POSTDATA_LOCK,
            "r8a2_postdata_lock": R8A2_POSTDATA_LOCK,
            "r8a2_json_sha256": jsha,
            "r8a2_npz_sha256": nsha,
            "r8a2_classification": r8j.get("classification"),
            "r6a_interface_constants_match": constants_ok,
        }
    else:
        parent_meta = {"missing_r8a2_json": not R8A2_JSON.is_file(), "missing_r8a2_npz": not R8A2_NPZ.is_file()}
    print("STABLE_AEST_ACT_DR6_R10A_PARENT " + json.dumps({"g1": g1, **parent_meta}, sort_keys=True), flush=True)

    interface_meta = {}; data_dict = None; control_chi2 = float("nan"); g2 = False
    if g1:
        try:
            import act_dr6_lenslike as alike
            src = Path(os.environ.get("R10A_ACT_SOURCE_ROOT", ""))
            pkg_dir = Path(alike.__file__).resolve().parent
            ddir = pkg_dir / "data" / ACT_DATA_VERSION
            source_head = git_head(src) if src.is_dir() else ""
            internal_version = str(getattr(alike, "__version__", ""))
            module_in_source = bool(src.is_dir() and pkg_dir.is_relative_to(src.resolve()))
            manifest = {}
            for relp in r6a.CONSUMED_DATA:
                p = ddir / relp
                if p.is_file():
                    manifest[str(relp)] = {"sha256": sha256(p), "bytes": p.stat().st_size}
            complete_manifest = all(relp in manifest for relp in r6a.CONSUMED_DATA)
            source_ok = bool(
                source_head == ACT_COMMIT and internal_version == ACT_INTERNAL_VERSION
                and module_in_source and ddir.is_dir() and complete_manifest
            )
            if source_ok:
                data_dict, control_chi2 = r6a.official_control(alike, ddir)
            g2 = bool(source_ok and np.isfinite(control_chi2) and abs(control_chi2 - CONTROL_CHI2) <= CONTROL_TOL)
            interface_meta = {
                "act_source_head": source_head, "act_internal_version": internal_version,
                "act_module": str(Path(alike.__file__).resolve()), "module_in_source": module_in_source,
                "data_dir": str(ddir), "manifest_complete": complete_manifest, "manifest": manifest,
                "control_chi2": control_chi2, "control_target": CONTROL_CHI2,
                "control_tolerance": CONTROL_TOL,
            }
        except Exception as exc:
            interface_meta = {"error": repr(exc), "control_chi2": control_chi2}
    print("STABLE_AEST_ACT_DR6_R10A_INTERFACE " + json.dumps({"g2": g2, **interface_meta}, sort_keys=True), flush=True)

    arrays = {}; support_meta = {}; central_metrics = {}; projections = {}; tau_coherence = {}; live = {}
    g3 = g4 = g5 = g6 = g7 = False

    if g2 and q is not None and data_dict is not None:
        ell = np.asarray(q["ell"], float)
        expected_ell = np.arange(40.0, 2001.0)
        exact_ell = bool(ell.shape == expected_ell.shape and np.array_equal(ell, expected_ell))
        B = np.asarray(data_dict["binmat_act"], float)
        nL = int(B.shape[1]); Lfull = np.arange(nL, dtype=int)
        outside = (Lfull < 40) | (Lfull > 2000)
        support_frac = float(np.sum(np.abs(B[:, outside]))) / max(float(np.sum(np.abs(B))), 1e-300)

        baseline_ref = None; baseline_errors = {}; finite_positive = True; required_arrays = True
        for tau in TAUS:
            tag = tau_tag(tau)
            kc = f"baseline_tau{tag}_ckk"; k25 = f"T_tau{tag}_ckk_eps025"; k50 = f"T_tau{tag}_ckk_eps05"
            if not all(k in q.files for k in (kc, k25, k50)):
                required_arrays = False
                continue
            c0 = np.asarray(q[kc], float); T25 = np.asarray(q[k25], float); T50 = np.asarray(q[k50], float)
            shape_ok = bool(c0.shape == ell.shape and T25.shape == ell.shape and T50.shape == ell.shape)
            finite_positive &= bool(
                shape_ok and np.all(np.isfinite(c0)) and np.all(c0 > 0.0)
                and np.all(np.isfinite(T25)) and np.all(np.isfinite(T50))
            )
            if baseline_ref is None and shape_ok:
                baseline_ref = c0.copy()
            berr = (
                float(np.max(np.abs(c0 - baseline_ref) / np.maximum(np.abs(baseline_ref), 1e-300)))
                if baseline_ref is not None and c0.shape == baseline_ref.shape else float("inf")
            )
            baseline_errors[str(tau)] = berr
            live[tau] = {"c0": c0, "T25": T25, "T50": T50}
        max_baseline_error = max(baseline_errors.values(), default=float("inf"))
        g3 = bool(
            exact_ell and required_arrays and len(live) == len(TAUS) and finite_positive
            and nL == TRIM_LMAX + 2 and np.all(np.isfinite(B))
            and support_frac <= SUPPORT_TOL and max_baseline_error <= BASELINE_TAU_TOL
        )
        support_meta = {
            "exact_ell_40_2000": exact_ell, "required_arrays_present": required_arrays,
            "live_arrays_finite_baseline_positive": finite_positive, "binmat_shape": list(B.shape),
            "support_fraction_outside_40_2000": support_frac, "support_threshold": SUPPORT_TOL,
            "baseline_tau_max_relative_errors_vs_tau10": baseline_errors,
            "baseline_tau_max_relative_error": max_baseline_error, "baseline_tau_threshold": BASELINE_TAU_TOL,
            "bcents_act": np.asarray(data_dict["bcents_act"], float).tolist(),
        }
        arrays["ell"] = ell

        if g3:
            central_all = True; idx = ell.astype(int)
            for tau in TAUS:
                tag = tau_tag(tau)
                c0 = live[tau]["c0"]; T25 = live[tau]["T25"]; T50 = live[tau]["T50"]
                c0_full = np.zeros(nL, float); d25_full = np.zeros(nL, float); d50_full = np.zeros(nL, float)
                c0_full[idx] = c0; d25_full[idx] = c0 * T25; d50_full[idx] = c0 * T50
                b0 = B @ c0_full; t25 = B @ d25_full; t50 = B @ d50_full
                E = rel(t25, t50); C = cosine(t25, t50); norm25 = float(np.linalg.norm(t25))
                ok = bool(
                    np.all(np.isfinite(b0)) and np.all(np.isfinite(t25)) and np.all(np.isfinite(t50))
                    and E <= CENTRAL_E_TOL and C >= CENTRAL_C_TOL and norm25 > 1e-20
                )
                central_all &= ok
                central_metrics[str(tau)] = {"E_eps025_vs_eps05": E, "C_eps025_vs_eps05": C, "norm_eps025": norm25, "pass": ok}
                live[tau].update({"b0": b0, "t25": t25, "t50": t50})
                arrays[f"baseline_tau{tag}_ckk"] = c0
                arrays[f"T_tau{tag}_ckk_eps025"] = T25
                arrays[f"T_tau{tag}_ckk_eps05"] = T50
                arrays[f"act_b0_tau{tag}"] = b0
                arrays[f"act_t25_tau{tag}"] = t25
                arrays[f"act_t50_tau{tag}"] = t50
            g4 = bool(central_all)

        if g4:
            data = np.asarray(data_dict["data_binned_clkk"], float)
            cov = np.asarray(data_dict["cov"], float); cinv = np.asarray(data_dict["cinv"], float)
            cov_sym = bool(np.allclose(cov, cov.T, rtol=1e-12, atol=1e-18))
            algebra_all = bool(np.all(np.isfinite(data)) and np.all(np.isfinite(cov)) and np.all(np.isfinite(cinv)) and cov_sym)
            for tau in TAUS:
                tag = tau_tag(tau); c0 = live[tau]["c0"]; T25 = live[tau]["T25"]
                b0 = live[tau]["b0"]; t25 = live[tau]["t25"]; a = b0.copy()
                aa = dotc(a, a, cinv); at = dotc(a, t25, cinv); tt = dotc(t25, t25, cinv)
                tperp = t25 - a * (at / aa) if aa > 0.0 else np.full_like(t25, np.nan)
                Fperp = qform(tperp, cinv) if np.all(np.isfinite(tperp)) else float("nan")
                orth = abs(dotc(a, tperp, cinv)) / math.sqrt(aa * Fperp) if aa > 0.0 and Fperp > 0.0 else float("inf")
                physical_positive = all(
                    bool(np.all(np.isfinite(c0 * (1.0 + eta * T25))) and np.all(c0 * (1.0 + eta * T25) > 0.0))
                    for eta in ETA_GRID
                )
                ok = bool(
                    np.all(np.isfinite(b0)) and np.all(np.isfinite(t25)) and aa > 0.0 and tt > 0.0
                    and np.isfinite(Fperp) and Fperp > 0.0 and np.isfinite(orth) and orth <= ALG_TOL
                    and physical_positive
                )
                algebra_all &= ok
                live[tau].update({"a": a, "aa": aa, "tt": tt, "tperp": tperp, "Fperp": Fperp})
                projections[str(tau)] = {
                    "F_raw": tt, "F_perp": Fperp,
                    "F_perp_over_F_raw": Fperp / tt if tt > 0.0 else float("nan"),
                    "rho_amplitude_memory": at / math.sqrt(aa * tt) if aa > 0.0 and tt > 0.0 else float("nan"),
                    "sigma_eta_shape": 1.0 / math.sqrt(Fperp) if Fperp > 0.0 else float("inf"),
                    "amplitude_projection_orthogonality": orth,
                    "physical_local_model_positive": physical_positive, "projection_algebra_pass": ok,
                }
                arrays[f"act_tperp_tau{tag}"] = tperp
            g5 = bool(algebra_all)

        if g5:
            data = np.asarray(data_dict["data_binned_clkk"], float); cinv = np.asarray(data_dict["cinv"], float)
            gls_all = True
            for tau in TAUS:
                b0 = live[tau]["b0"]; t25 = live[tau]["t25"]; a = live[tau]["a"]
                aa = live[tau]["aa"]; tt = live[tau]["tt"]; tperp = live[tau]["tperp"]; Fperp = live[tau]["Fperp"]
                r = data - b0
                eta_hat = dotc(tperp, r, cinv) / Fperp
                sigma_eta = 1.0 / math.sqrt(Fperp); signed_sn = eta_hat / sigma_eta
                try:
                    L = np.linalg.cholesky(cinv); W = L.T
                    sa = math.sqrt(aa); st = math.sqrt(tt); Xs = np.column_stack([a / sa, t25 / st])
                    gamma, _, _, _ = np.linalg.lstsq(W @ Xs, W @ r, rcond=None)
                    deltaA_gls = float(gamma[0] / sa); eta_gls = float(gamma[1] / st)
                    diff = abs(eta_hat - eta_gls); scale = max(1.0, abs(eta_hat), abs(eta_gls))
                    gls_ok = bool(diff <= GLS_TOL * scale)
                except Exception as exc:
                    deltaA_gls = eta_gls = float("nan"); diff = float("inf"); gls_ok = False
                    projections[str(tau)]["gls_error"] = repr(exc)
                gls_all &= gls_ok
                chi2_fixed = {}; chi2_profiled = {}
                for eta in ETA_GRID:
                    rr = data - (b0 + eta * t25); chi2_fixed[f"{eta:g}"] = qform(rr, cinv)
                    deltaA = dotc(a, r - eta * t25, cinv) / aa
                    rr_prof = r - deltaA * a - eta * t25; chi2_profiled[f"{eta:g}"] = qform(rr_prof, cinv)
                eta_phys = min(max(eta_hat, 0.0), 0.05)
                deltaA_phys = dotc(a, r - eta_phys * t25, cinv) / aa
                rr_phys = r - deltaA_phys * a - eta_phys * t25
                chi2_phys = qform(rr_phys, cinv); delta_chi2_phys = chi2_profiled["0"] - chi2_phys
                projections[str(tau)].update({
                    "eta_hat_signed": eta_hat, "sigma_eta": sigma_eta, "signed_template_sn": signed_sn,
                    "eta_gls": eta_gls, "deltaA_gls": deltaA_gls, "matched_filter_gls_abs_diff": diff,
                    "matched_filter_gls_pass": gls_ok, "eta_physical_clipped": eta_phys,
                    "delta_chi2_physical": delta_chi2_phys, "chi2_fixed": chi2_fixed, "chi2_profiled": chi2_profiled,
                })
            g6 = bool(gls_all)

        if g6:
            ref = live[10.0]["tperp"]; ref_norm = float(np.linalg.norm(ref)); tau_all = True
            for tau in TAUS:
                x = live[tau]["tperp"]; n = float(np.linalg.norm(x)); C = cosine(x, ref)
                ratio = n / max(ref_norm, 1e-300)
                ok = bool(np.isfinite(n) and n > 0.0 and np.isfinite(C) and C >= TAU_C_TOL)
                tau_all &= ok
                tau_coherence[str(tau)] = {"cosine_to_tau10": C, "norm_ratio_to_tau10": ratio, "pass": ok}
            g7 = bool(tau_all)

    gates = {
        "R10A_G1_parent_provenance": g1,
        "R10A_G2_official_ACT_interface_control": g2,
        "R10A_G3_support_and_live_baseline": g3,
        "R10A_G4_live_central_derivative_ACT_space": g4,
        "R10A_G5_projection_algebra_and_physical_local_model": g5,
        "R10A_G6_matched_filter_GLS_identity": g6,
        "R10A_G7_ACT_space_tau_coherence": g7,
    }
    if not g1: classification = CLS_PARENT
    elif not g2: classification = CLS_INTERFACE
    elif not g3: classification = CLS_SUPPORT
    elif not g4: classification = CLS_CENTRAL
    elif not g5: classification = CLS_ALG
    elif not g6: classification = CLS_GLS
    elif not g7: classification = CLS_TAU
    else: classification = CLS_PASS

    out = {
        "classification": classification, "diagnostic_complete": True,
        "science_evaluated": bool(g1 and g2 and g3 and g4 and g5 and g6),
        "claim_scope": {
            "compressed_ACT_DR6_lensing_only_projection": classification == CLS_PASS,
            "live_AeST_linear_response": classification == CLS_PASS,
            "detection_claim": False,
            "physical_eta_estimate_from_unconstrained_signed_coefficient": False,
            "tau_bound": False, "full_cosmological_inference": False,
            "full_ACT_primary_CMB_likelihood": False, "nonlinear_lensing_claim": False,
        },
        "frozen": {
            "prefit_lock": PREFIT_LOCK, "r6a_postdata_lock": R6A_POSTDATA_LOCK,
            "r8a2_postdata_lock": R8A2_POSTDATA_LOCK, "tau_H0": list(TAUS),
            "eta_grid": list(ETA_GRID), "physical_eta_interval": [0.0, 0.05],
            "primary_epsilon": 0.025, "control_epsilon": 0.05,
            "act_commit": ACT_COMMIT, "act_data_version": ACT_DATA_VERSION,
            "act_variant": ACT_VARIANT, "lens_only": True, "like_corrections": False,
            "apply_hartlap": True, "nsims_act": NSIMS_ACT, "trim_lmax": TRIM_LMAX,
        },
        "gates": gates, "parent": parent_meta, "interface": interface_meta,
        "support": support_meta, "central_derivative_ACT_space": central_metrics,
        "projection": projections, "tau_coherence_ACT_space": tau_coherence,
    }
    Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    if arrays:
        np.savez_compressed(args.npz_out, **arrays)

    print("STABLE_AEST_ACT_DR6_R10A_GATES " + json.dumps(gates, sort_keys=True), flush=True)
    if projections:
        summary = {
            tau: {k: projections[tau].get(k) for k in (
                "eta_hat_signed", "sigma_eta", "signed_template_sn",
                "eta_physical_clipped", "delta_chi2_physical", "F_perp_over_F_raw")}
            for tau in projections
        }
        print("STABLE_AEST_ACT_DR6_R10A_PROJECTION " + json.dumps(summary, sort_keys=True), flush=True)
    if tau_coherence:
        print("STABLE_AEST_ACT_DR6_R10A_TAU " + json.dumps(tau_coherence, sort_keys=True), flush=True)
    print("STABLE_AEST_ACT_DR6_R10A_CLASSIFICATION=" + classification, flush=True)
    return 0 if classification == CLS_PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
