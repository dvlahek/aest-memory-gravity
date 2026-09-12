#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fullj_weyl import evolving_flrw_weyl_bridge_r2 as r2
from nl1c6d2c6b import all27_physical_nonlinear_trajectories as d2b

m = r2.m
static = m.static

R2_RESULT_LOCK = "1f42f88e9724c58d2d242a65ca7266a207e4a0f8"
COV_RESULT_LOCK = "87434c21866241b1b35588ec88e93e99a6f5db1a"
PREDATA_LOCK = "ad0b42694183d71b3ea1cab1eb1775c6456268c6"

PASS = "FULLJ_EVOLVING_WEYL_GAUSSIAN_1D_ENSEMBLE_PASS"
FAIL = "FULLJ_EVOLVING_WEYL_GAUSSIAN_1D_ENSEMBLE_FAIL"
INCOMPLETE = "FULLJ_EVOLVING_WEYL_GAUSSIAN_1D_ENSEMBLE_INCOMPLETE"

SEED = 20260912
NREAL = 32
PREFIXES = (8, 16, 32)
REFERENCE_MEMBER = {"sigma": 0, "kind": "simple", "beta0": 1.0}
GAUSS_MEAN_MIN = 0.75
GAUSS_MEAN_MAX = 1.25
METRIC_GATE = 1.0e-8
CANONICAL_GATE = 1.0e-10
ALG_GATE = 1.0e-12
CONV_MED_GATE = 0.25
CONV_MAX_GATE = 0.50
BANDS = {
    "low": (1, 7),
    "mid": (8, 15),
    "high": (16, 32),
}


def git_head() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()


def is_ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0


def rel(a, b) -> float:
    aa = np.asarray(a)
    bb = np.asarray(b)
    return float(np.linalg.norm(aa - bb) / max(float(np.linalg.norm(aa)), float(np.linalg.norm(bb)), 1.0e-300))


def coefficient_draw():
    rng = np.random.default_rng(SEED)
    xy = rng.normal(size=(NREAL, len(m.K_MPC), 2))
    g = (xy[..., 0] + 1j * xy[..., 1]) / np.sqrt(2.0)
    digest = hashlib.sha256(np.ascontiguousarray(xy, dtype=np.float64).tobytes()).hexdigest()
    return xy, g, digest


def realization_basis(nx: int, gvec: np.ndarray) -> np.ndarray:
    gv = np.asarray(gvec, complex)
    if gv.shape != (len(m.K_MPC),):
        raise ValueError("Gaussian coefficient vector has wrong shape")
    x = np.arange(nx) * static.BOX / nx
    amp = static.MODE_AMP * np.abs(gv)
    phase = np.angle(gv)
    return amp[:, None] * np.cos(m.K_MPC[:, None] * x[None, :] + phase[:, None])


def output_modes(field, nmax=r2.NMAX):
    arr = np.asarray(field, float)
    ff = np.fft.rfft(arr) / arr.size
    out = np.zeros(nmax + 1, complex)
    n = min(out.size, ff.size)
    out[:n] = ff[:n]
    return out


def covariance_metrics(samples: np.ndarray):
    x = np.asarray(samples, complex)
    xc = x - np.mean(x, axis=0, keepdims=True)
    C = (xc.conj().T @ xc) / float(x.shape[0] - 1)
    herm = rel(C, C.conj().T)
    H = 0.5 * (C + C.conj().T)
    eig = np.linalg.eigvalsh(H)
    escale = max(float(np.max(np.abs(eig))), 1.0e-300)
    mineig = float(np.min(eig) / escale)
    trace = float(np.real(np.trace(H)))
    mse = float(np.sum(np.abs(xc) ** 2) / float(x.shape[0] - 1))
    trace_id = abs(trace - mse) / max(abs(trace), abs(mse), 1.0e-300)
    spec = np.real(np.diag(H))
    return C, {
        "hermiticity_relative_residual": herm,
        "min_eigenvalue_relative": mineig,
        "trace_identity_relative_residual": trace_id,
        "trace": trace,
        "spectrum": spec,
    }


def bandpowers(spec: np.ndarray):
    s = np.asarray(spec, float)
    out = {}
    for name, (lo, hi) in BANDS.items():
        out[name] = float(np.sum(s[lo:hi + 1]))
    return out


def run_one(data, gvec: np.ndarray, original_cos_matrix):
    def custom_cos_matrix(nx):
        return realization_basis(nx, gvec)

    m.cos_matrix = custom_cos_matrix
    d2b.set_member(REFERENCE_MEMBER)
    try:
        run = r2.integrate_combined_r2(data, r2.NX, r2.NSTEP, True)
        if not run["finite"] or len(run["checkpoints"]) != len(data["tau_check"]):
            return {
                "finite": False,
                "reason": run.get("fail_reason", "incomplete_realization"),
            }, None, None

        C = custom_cos_matrix(r2.NX)
        W = []
        Wclass = []
        metric_max = {"hamiltonian": 0.0, "momentum": 0.0, "shear": 0.0}
        canonical_max = 0.0
        finite = True
        for cp in run["checkpoints"]:
            rec = cp["metric"]
            w = np.asarray(rec["weyl"], float)
            finite = finite and np.all(np.isfinite(w))
            W.append(output_modes(w))
            _, _, wc = r2.r0.class_metric_fields(data, float(cp["tau"]), r2.NX, C)
            Wclass.append(output_modes(wc))
            canonical_max = max(canonical_max, float(cp["canonical_constraint"]))
            for key, value in rec["metric_correction"]["constraint"].items():
                metric_max[key] = max(metric_max[key], float(value))

        record = {
            "finite": bool(finite),
            "canonical_constraint_max": float(canonical_max),
            "metric_constraint_max": metric_max,
        }
        return record, np.asarray(W, complex), np.asarray(Wclass, complex)
    finally:
        m.cos_matrix = original_cos_matrix


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json-out", default="results/fullj_evolving_weyl_gaussian_1d_ensemble.json")
    ap.add_argument("--npz-out", default="results/fullj_evolving_weyl_gaussian_1d_ensemble.npz")
    args = ap.parse_args()

    ancestry = {
        "r2_result_lock": is_ancestor(R2_RESULT_LOCK),
        "covariance_result_lock": is_ancestor(COV_RESULT_LOCK),
        "predata_lock": is_ancestor(PREDATA_LOCK),
    }
    if not all(ancestry.values()):
        result = {
            "classification": INCOMPLETE,
            "diagnostic_complete": False,
            "ancestry": ancestry,
            "reason": "missing required locked ancestry",
        }
        Path(args.json_out).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print("FULLJ_GAUSS1D_CLASSIFICATION=" + INCOMPLETE, flush=True)
        return 2

    print("FULLJ_GAUSS1D_START", flush=True)
    print("FULLJ_GAUSS1D_ANCESTRY=" + json.dumps(ancestry, sort_keys=True), flush=True)
    print("FULLJ_GAUSS1D_MEMBER=" + d2b.member_key(REFERENCE_MEMBER), flush=True)

    data = r2.r0.prepare_bridge_data()
    xy, g, coeff_hash = coefficient_draw()
    mean_abs2 = float(np.mean(np.abs(g) ** 2))
    print(
        f"FULLJ_GAUSS1D_COEFFICIENTS seed={SEED} nreal={NREAL} modes={g.shape[1]} "
        f"mean_abs2={mean_abs2:.12e} sha256={coeff_hash}",
        flush=True,
    )

    original_cos_matrix = m.cos_matrix
    records = []
    W_all = []
    Wclass_all = []
    metric_global = {"hamiltonian": 0.0, "momentum": 0.0, "shear": 0.0}
    canonical_global = 0.0

    for ir in range(NREAL):
        rec, W, Wclass = run_one(data, g[ir], original_cos_matrix)
        rec["realization"] = int(ir)
        rec["g_abs2_mean"] = float(np.mean(np.abs(g[ir]) ** 2))
        records.append(rec)
        if W is not None:
            W_all.append(W)
            Wclass_all.append(Wclass)
            canonical_global = max(canonical_global, float(rec["canonical_constraint_max"]))
            for key, value in rec["metric_constraint_max"].items():
                metric_global[key] = max(metric_global[key], float(value))
        print(
            f"FULLJ_GAUSS1D_REALIZATION {ir+1:02d}/{NREAL} finite={rec['finite']} "
            + (
                f"canonical={rec['canonical_constraint_max']:.3e} "
                + " ".join(f"{k}={v:.3e}" for k, v in rec["metric_constraint_max"].items())
                if rec.get("finite") else f"reason={rec.get('reason','unknown')}"
            ),
            flush=True,
        )

    all_finite = len(W_all) == NREAL and all(bool(r.get("finite", False)) for r in records)
    if all_finite:
        W_all = np.asarray(W_all, complex)  # realization,z,mode
        Wclass_all = np.asarray(Wclass_all, complex)
    else:
        W_all = np.asarray(W_all, complex) if W_all else np.empty((0, 9, r2.NMAX + 1), complex)
        Wclass_all = np.asarray(Wclass_all, complex) if Wclass_all else np.empty_like(W_all)

    cov_store = []
    ref_cov_store = []
    prefix_rows = []
    alg_herm = []
    alg_mineig = []
    alg_traceid = []
    bands_by_prefix = {}

    if all_finite:
        for N in PREFIXES:
            perz = []
            perz_ref = []
            band_rows = []
            for iz, z in enumerate(np.asarray(m.CHECK_Z, float)):
                C, mm = covariance_metrics(W_all[:N, iz, :])
                Cr, mr = covariance_metrics(Wclass_all[:N, iz, :])
                perz.append(C)
                perz_ref.append(Cr)
                alg_herm.append(mm["hermiticity_relative_residual"])
                alg_mineig.append(mm["min_eigenvalue_relative"])
                alg_traceid.append(mm["trace_identity_relative_residual"])
                bp = bandpowers(mm["spectrum"])
                bpr = bandpowers(mr["spectrum"])
                band_rows.append(bp)
                prefix_rows.append({
                    "N": int(N),
                    "z": float(z),
                    "trace": float(mm["trace"]),
                    "hermiticity_relative_residual": float(mm["hermiticity_relative_residual"]),
                    "min_eigenvalue_relative": float(mm["min_eigenvalue_relative"]),
                    "trace_identity_relative_residual": float(mm["trace_identity_relative_residual"]),
                    "bandpower": bp,
                    "class_bandpower": bpr,
                    "nonlinear_to_class_band_ratio": {
                        k: float(bp[k] / max(bpr[k], 1.0e-300)) for k in BANDS
                    },
                })
            cov_store.append(perz)
            ref_cov_store.append(perz_ref)
            bands_by_prefix[N] = band_rows

    d16_32 = []
    d8_16 = []
    conv_rows = []
    if all_finite:
        for iz, z in enumerate(np.asarray(m.CHECK_Z, float)):
            for band in BANDS:
                b8 = float(bands_by_prefix[8][iz][band])
                b16 = float(bands_by_prefix[16][iz][band])
                b32 = float(bands_by_prefix[32][iz][band])
                q816 = abs(b16 - b8) / max(abs(b16), abs(b8), 1.0e-300)
                q1632 = abs(b32 - b16) / max(abs(b32), abs(b16), 1.0e-300)
                d8_16.append(q816)
                d16_32.append(q1632)
                conv_rows.append({
                    "z": float(z), "band": band,
                    "B8": b8, "B16": b16, "B32": b32,
                    "d8_16": float(q816), "d16_32": float(q1632),
                })

    conv_med = float(np.median(d16_32)) if d16_32 else float("inf")
    conv_max = float(np.max(d16_32)) if d16_32 else float("inf")
    g1 = bool(all(ancestry.values()) and NREAL == 32 and SEED == 20260912 and REFERENCE_MEMBER == {"sigma": 0, "kind": "simple", "beta0": 1.0})
    g2 = bool(GAUSS_MEAN_MIN <= mean_abs2 <= GAUSS_MEAN_MAX)
    g3 = bool(all_finite)
    g4 = bool(
        all_finite
        and canonical_global <= CANONICAL_GATE
        and all(v <= METRIC_GATE for v in metric_global.values())
    )
    g5 = bool(
        all_finite
        and alg_herm and max(alg_herm) <= ALG_GATE
        and min(alg_mineig) >= -ALG_GATE
        and max(alg_traceid) <= ALG_GATE
    )
    g6 = bool(all_finite and conv_med <= CONV_MED_GATE and conv_max <= CONV_MAX_GATE)
    g7 = bool(d2b.member_key(REFERENCE_MEMBER) == "sigma=+0|kind=simple|beta0=1")
    gates = {
        "G1_provenance_and_ensemble_identity": g1,
        "G2_Gaussian_coefficient_normalization": g2,
        "G3_finite_nonlinear_evolution_32of32": g3,
        "G4_metric_and_canonical_health": g4,
        "G5_stochastic_covariance_algebra": g5,
        "G6_prefix_bandpower_convergence": g6,
        "G7_no_deterministic_theory_mixing": g7,
    }
    classification = PASS if all(gates.values()) else FAIL

    summary = {
        "seed": SEED,
        "coefficient_sha256": coeff_hash,
        "mean_abs_g_squared": mean_abs2,
        "finite_realizations": int(sum(bool(r.get("finite", False)) for r in records)),
        "expected_realizations": NREAL,
        "canonical_constraint_max": float(canonical_global),
        "metric_constraint_max": metric_global,
        "covariance_hermiticity_max": float(max(alg_herm)) if alg_herm else float("nan"),
        "covariance_min_eigenvalue_relative": float(min(alg_mineig)) if alg_mineig else float("nan"),
        "covariance_trace_identity_max": float(max(alg_traceid)) if alg_traceid else float("nan"),
        "d16_32_median": conv_med,
        "d16_32_max": conv_max,
        "d8_16_median": float(np.median(d8_16)) if d8_16 else float("nan"),
        "d8_16_max": float(np.max(d8_16)) if d8_16 else float("nan"),
    }

    result = {
        "classification": classification,
        "diagnostic_complete": True,
        "git_head": git_head(),
        "ancestry": ancestry,
        "scope": "32-realization Gaussian stochastic diagnostic on the 1D periodic R2 embedding; fixed theory branch sigma=0,simple,beta0=1",
        "reference_member": REFERENCE_MEMBER,
        "rng": {"generator": "numpy.random.default_rng", "seed": SEED, "N": NREAL},
        "coefficient_definition": "g=(X+iY)/sqrt(2), X,Y iid N(0,1); basis amplitude MODE_AMP*abs(g), phase arg(g)",
        "coefficient_sha256": coeff_hash,
        "gates": gates,
        "summary": summary,
        "records": records,
        "prefix_rows": prefix_rows,
        "convergence_rows": conv_rows,
        "ONE_D_GAUSSIAN_WEYL_ENSEMBLE_TESTED": True,
        "THREE_D_ISOTROPIC_WEYL_POWER_LICENSED": False,
        "EVOLVING_WEYL_POWER_LICENSED": False,
        "ACT_LIKELIHOOD_LICENSED": False,
        "OBSERVATIONAL_CLAIM_LICENSED": False,
    }

    jout = Path(args.json_out)
    nout = Path(args.npz_out)
    jout.parent.mkdir(parents=True, exist_ok=True)
    jout.write_text(json.dumps(result, indent=2, sort_keys=True, allow_nan=True) + "\n")

    if all_finite:
        cov_arr = np.asarray(cov_store, complex)  # prefix,z,mode,mode
        ref_cov_arr = np.asarray(ref_cov_store, complex)
        k_out = np.arange(r2.NMAX + 1, dtype=float) * (2.0 * np.pi / static.BOX)
        np.savez_compressed(
            nout,
            X_Y=xy,
            g_real=g.real,
            g_imag=g.imag,
            z=np.asarray(m.CHECK_Z, float),
            mode_number=np.arange(r2.NMAX + 1, dtype=int),
            k_Mpc=k_out,
            W=W_all,
            W_CLASS=Wclass_all,
            prefixes=np.asarray(PREFIXES, int),
            C_real=cov_arr.real,
            C_imag=cov_arr.imag,
            C_CLASS_real=ref_cov_arr.real,
            C_CLASS_imag=ref_cov_arr.imag,
        )

    print("FULLJ_GAUSS1D_SUMMARY=" + json.dumps(summary, sort_keys=True), flush=True)
    print("FULLJ_GAUSS1D_GATES=" + json.dumps(gates, sort_keys=True), flush=True)
    print("FULLJ_GAUSS1D_CLASSIFICATION=" + classification, flush=True)
    print("ONE_D_GAUSSIAN_WEYL_ENSEMBLE_TESTED=True", flush=True)
    print("THREE_D_ISOTROPIC_WEYL_POWER_LICENSED=False", flush=True)
    print("EVOLVING_WEYL_POWER_LICENSED=False", flush=True)
    print("ACT_LIKELIHOOD_LICENSED=False", flush=True)
    print("OBSERVATIONAL_CLAIM_LICENSED=False", flush=True)
    print("FULLJ_GAUSS1D_JSON=" + str(jout), flush=True)
    print("FULLJ_GAUSS1D_NPZ=" + str(nout), flush=True)
    return 0 if classification == PASS else 2


if __name__ == "__main__":
    raise SystemExit(main())
