#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import subprocess
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from v063 import theory_response_map as v63

SCOPE_COMMIT = "e13f5a58004eb60ff59cc40c4db45ea2c91a9929"
H_EXECUTED_HEAD = "3bab93b3c697a0873bb95ded35044d47716829fc"
CLASS_SHA = "e85808324f51fc694d12e3ed7439552a3c3f9540"

ETA_GRID = np.asarray([0.0, 1.0/256.0, 1.0/128.0, 1.0/64.0, 1.0/32.0, 1.0/16.0, 1.0/8.0], float)
TAUH0 = 1.0
MEMORY_ORDER = 39
LMAX = 4000
TRIM_LMAX = 2998
ETA0_REG_GATE = 1.0e-8
LIKELIHOOD_VARIANT = "act_baseline"
LIKELIHOOD_VERSION = "v1.2"

COMPLETE_LABEL = "ACT_DR6_LENSING_EXPLORATORY_SCAN_COMPLETE"
INCOMPLETE_LABEL = "ACT_DR6_LENSING_EXPLORATORY_SCAN_INCOMPLETE"


def git_head() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()


def is_ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0


def rel_l2(a, b) -> float:
    aa = np.asarray(a, float)
    bb = np.asarray(b, float)
    return float(np.linalg.norm(aa-bb) / max(np.linalg.norm(aa), np.linalg.norm(bb), 1.0e-300))


def theory_params(memory_enabled: bool, eta: float) -> dict:
    p = dict(v63.class_params())
    p.update({
        "output": "lCl",
        "lensing": "yes",
        "l_max_scalars": LMAX,
        "P_k_max_h/Mpc": 20.0,
        "z_max_pk": 10.0,
        "non linear": "halofit",
        "aest_memory_enabled": "yes" if memory_enabled else "no",
        "aest_eta": float(eta),
        "aest_tau_H0": TAUH0,
        "aest_memory_order": MEMORY_ORDER,
    })
    return p


def compute_clpp(memory_enabled: bool, eta: float):
    from classy import Class

    c = Class()
    c.set(theory_params(memory_enabled, eta))
    c.compute()
    try:
        raw = c.raw_cl(LMAX)
        if "pp" not in raw:
            raise RuntimeError(f"CLASS raw_cl lacks pp; keys={sorted(raw)}")
        clpp = np.asarray(raw["pp"], float).copy()
        ell = np.arange(clpp.size, dtype=float)
        if clpp.size < TRIM_LMAX + 2:
            raise RuntimeError(f"CLASS pp length {clpp.size} is below likelihood requirement")
        if not np.all(np.isfinite(clpp)):
            raise FloatingPointError("nonfinite CLASS lensing-potential spectrum")
        return ell, clpp
    finally:
        c.struct_cleanup()
        c.empty()


def convergence_from_potential(alike, ell, clpp):
    clkk = np.asarray(alike.pp_to_kk(np.asarray(clpp, float), np.asarray(ell, float)), float)
    if not np.all(np.isfinite(clkk)):
        raise FloatingPointError("nonfinite C_L^kappakappa")
    return clkk


def likelihood(alike, data, ell, clkk):
    # In lens_only=True, like_corrections=False mode the primary-CMB spectra
    # are not used.  Generic likelihood still standardizes the supplied arrays,
    # so provide correctly shaped zeros rather than introducing irrelevant CMB output.
    z = np.zeros_like(clkk)
    lnlike, theory_binned = alike.generic_lnlike(
        data,
        ell, clkk,
        ell, z, z, z, z,
        trim_lmax=TRIM_LMAX,
        return_theory=True,
        do_norm_corr=False,
        act_calib=False,
        no_actlike_cmb_corrections=True,
    )
    lnlike = float(lnlike)
    theory_binned = np.asarray(theory_binned, float)
    if not math.isfinite(lnlike) or not np.all(np.isfinite(theory_binned)):
        raise FloatingPointError("nonfinite ACT DR6 likelihood result")
    return lnlike, theory_binned


def spectrum_summary(ell, clpp, clkk):
    mask = (ell >= 40) & (ell <= 763)
    if not np.any(mask):
        raise RuntimeError("empty ACT baseline L summary range")
    return {
        "clpp_rms_L40_763": float(np.sqrt(np.mean(clpp[mask]**2))),
        "clkk_rms_L40_763": float(np.sqrt(np.mean(clkk[mask]**2))),
        "clkk_min_L40_763": float(np.min(clkk[mask])),
        "clkk_max_L40_763": float(np.max(clkk[mask])),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json-out", default="results/act_dr6_lensing_exploratory.json")
    ap.add_argument("--npz-out", default="results/act_dr6_lensing_exploratory.npz")
    args = ap.parse_args()
    jout = Path(args.json_out)
    nout = Path(args.npz_out)
    jout.parent.mkdir(parents=True, exist_ok=True)

    try:
        import act_dr6_lenslike as alike

        head = git_head()
        ancestry = {
            "exploratory_scope": is_ancestor(SCOPE_COMMIT),
            "D2C6H_executed_head": is_ancestor(H_EXECUTED_HEAD),
        }
        print("ACT_DR6_LENSING_EXPLORATORY_START", flush=True)
        print("HEAD=" + head, flush=True)
        print("ANCESTRY=" + json.dumps(ancestry, sort_keys=True), flush=True)
        print("ETA_GRID=" + ",".join(f"{x:.12e}" for x in ETA_GRID), flush=True)
        print(f"LIKELIHOOD variant={LIKELIHOOD_VARIANT} lens_only=True corrections=False data={LIKELIHOOD_VERSION}", flush=True)

        if not all(ancestry.values()):
            raise RuntimeError(f"required ancestry missing: {ancestry}")

        data = alike.load_data(
            LIKELIHOOD_VARIANT,
            lens_only=True,
            like_corrections=False,
            version=LIKELIHOOD_VERSION,
        )

        # Technical eta=0 regression only: physical memory bath enabled at zero
        # coupling must reproduce the memory-disabled AeST lensing spectrum.
        ell_off, pp_off = compute_clpp(False, 0.0)
        kk_off = convergence_from_potential(alike, ell_off, pp_off)
        ell_0, pp_0 = compute_clpp(True, 0.0)
        kk_0 = convergence_from_potential(alike, ell_0, pp_0)
        if not np.array_equal(ell_off, ell_0):
            raise RuntimeError("eta0 regression ell grids differ")
        reg_slice = (ell_0 >= 2) & (ell_0 <= TRIM_LMAX+1)
        eta0_reg = rel_l2(kk_off[reg_slice], kk_0[reg_slice])
        eta0_reg_pass = bool(eta0_reg <= ETA0_REG_GATE)
        print(f"ETA0_MEMORY_ON_OFF_CLKK_REL_L2={eta0_reg:.12e} pass={eta0_reg_pass}", flush=True)
        if not eta0_reg_pass:
            raise RuntimeError(f"eta0 memory on/off regression failed: {eta0_reg}")

        all_pp = []
        all_kk = []
        all_binned = []
        rows = []

        for i, eta in enumerate(ETA_GRID):
            if eta == 0.0:
                ell, clpp, clkk = ell_0, pp_0, kk_0
            else:
                ell, clpp = compute_clpp(True, float(eta))
                clkk = convergence_from_potential(alike, ell, clpp)
            lnlike, binned = likelihood(alike, data, ell, clkk)
            chi2 = -2.0 * lnlike
            row = {
                "index": int(i),
                "eta": float(eta),
                "lnlike": lnlike,
                "chi2": chi2,
                **spectrum_summary(ell, clpp, clkk),
            }
            rows.append(row)
            all_pp.append(clpp)
            all_kk.append(clkk)
            all_binned.append(binned)
            print(
                f"ACT_DR6_POINT {i+1:02d}/{len(ETA_GRID):02d} eta={eta:.12e} "
                f"lnL={lnlike:.12e} chi2={chi2:.12e}",
                flush=True,
            )

        chi0 = rows[0]["chi2"]
        for row in rows:
            row["delta_chi2_vs_eta0"] = float(row["chi2"] - chi0)
        best = min(rows, key=lambda r: r["chi2"])
        best_summary = {
            "eta": best["eta"],
            "chi2": best["chi2"],
            "delta_chi2_vs_eta0": best["delta_chi2_vs_eta0"],
            "grid_index": best["index"],
        }

        np.savez_compressed(
            nout,
            eta=ETA_GRID,
            ell=ell_0,
            clpp=np.stack(all_pp),
            clkk=np.stack(all_kk),
            binned_theory=np.stack(all_binned),
            data_binned_clkk=np.asarray(data["data_binned_clkk"], float),
            bcents_act=np.asarray(data["bcents_act"], float),
            chi2=np.asarray([r["chi2"] for r in rows], float),
            delta_chi2=np.asarray([r["delta_chi2_vs_eta0"] for r in rows], float),
        )

        result = {
            "classification": COMPLETE_LABEL,
            "exploratory": True,
            "historical_D2C6H_remains_formal_FAIL": True,
            "observational_claim_licensed": False,
            "head": head,
            "ancestry": ancestry,
            "scope_commit": SCOPE_COMMIT,
            "class_upstream_sha": CLASS_SHA,
            "likelihood": {
                "package": "act_dr6_lenslike",
                "package_version_frozen": "1.2.1",
                "data_version": LIKELIHOOD_VERSION,
                "variant": LIKELIHOOD_VARIANT,
                "lens_only": True,
                "like_corrections": False,
            },
            "theory": {
                "KB": 0.0665,
                "tauH0": TAUH0,
                "memory_order": MEMORY_ORDER,
                "lmax": LMAX,
                "nonlinear": "halofit exploratory; not AeST-specific calibration",
                "direct_R2_H_quadratic_metric_stress_in_linear_CLASS": False,
                "clpp_to_clkk": "[L(L+1)]^2/4",
            },
            "eta_grid": ETA_GRID.tolist(),
            "eta0_memory_on_off_clkk_rel_l2": eta0_reg,
            "eta0_regression_gate": ETA0_REG_GATE,
            "eta0_regression_pass": eta0_reg_pass,
            "points": rows,
            "best_grid_point_exploratory": best_summary,
            "interpretation_scope": (
                "Discrete fixed-cosmology ACT DR6 lensing likelihood scan. No parameter refit, posterior, "
                "detection significance or final bound is licensed; D2C6H remains a formal FAIL."
            ),
        }
        jout.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")

        print("BEST_GRID_POINT=" + json.dumps(best_summary, sort_keys=True), flush=True)
        print("CLASSIFICATION=" + COMPLETE_LABEL, flush=True)
        print("EXPLORATORY=True", flush=True)
        print("OBSERVATIONAL_CLAIM_LICENSED=False", flush=True)
        print("JSON=" + str(jout), flush=True)
        print("NPZ=" + str(nout), flush=True)
        print("ACT_DR6_LENSING_EXPLORATORY_END", flush=True)
        return 0

    except Exception as exc:
        result = {
            "classification": INCOMPLETE_LABEL,
            "exploratory": True,
            "historical_D2C6H_remains_formal_FAIL": True,
            "observational_claim_licensed": False,
            "error_type": type(exc).__name__,
            "error": str(exc),
        }
        jout.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print(f"ACT_DR6_ERROR {type(exc).__name__}: {exc}", flush=True)
        print("CLASSIFICATION=" + INCOMPLETE_LABEL, flush=True)
        print("OBSERVATIONAL_CLAIM_LICENSED=False", flush=True)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
