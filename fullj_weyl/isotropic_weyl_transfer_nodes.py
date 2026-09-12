#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
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
GAUSS1D_RESULT_LOCK = "05e38b273f91eb04b7b4c8753731017d0ed839c1"
GEOM_RESULT_LOCK = "ca6a102196055e27dc2b31379285bfc7aea1a35b"
SAT_RESULT_LOCK = "f6eb7099cffc9ae6f4fe11ddef1794f0e6dd6e4f"
PREDATA_LOCK = "b02960733256e27d4c1883a30031392c68a5cf74"

PASS = "FULLJ_ISOTROPIC_WEYL_TRANSFER_NODES_PASS"
FAIL = "FULLJ_ISOTROPIC_WEYL_TRANSFER_NODES_FAIL"
INCOMPLETE = "FULLJ_ISOTROPIC_WEYL_TRANSFER_NODES_INCOMPLETE"

REFERENCE_MEMBER = {"sigma": 0, "kind": "simple", "beta0": 1.0}
ANCHOR_IDX = (0, 3, 5)  # n = 3,10,20
AMP_SCALES = (0.5, 2.0)
MODE_NUM = np.asarray(static.MODE_NUM, int)
K_MPC = np.asarray(m.K_MPC, float)
CHECK_Z = np.asarray(m.CHECK_Z, float)
NX = r2.NX
NSTEP = r2.NSTEP
NMAX = r2.NMAX

CANONICAL_GATE = 1.0e-10
METRIC_GATE = 1.0e-8
INITIAL_CLASS_GATE = 5.0e-3
PHASE_GATE = 1.0e-8
SEP_MED_GATE = 5.0e-4
SEP_MAX_GATE = 5.0e-3
LEAK_GATE = 5.0e-3
HOM_MED_GATE = 5.0e-4
HOM_MAX_GATE = 5.0e-3
GAUSS_MED_GATE = 5.0e-3
GAUSS_MAX_GATE = 2.0e-2
ALG_GATE = 1.0e-12
GAUSS_JSON = ROOT / "results/fullj_evolving_weyl_gaussian_1d_ensemble.json"


def git_head() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()


def is_ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0


def rel_scalar(a, b) -> float:
    aa = complex(a)
    bb = complex(b)
    return float(abs(aa - bb) / max(abs(aa), abs(bb), 1.0e-300))


def basis_matrix(nx: int, scales: np.ndarray) -> np.ndarray:
    s = np.asarray(scales, float)
    if s.shape != (len(MODE_NUM),):
        raise ValueError("basis scale vector has wrong shape")
    x = np.arange(nx) * static.BOX / nx
    return (
        (static.MODE_AMP * s)[:, None]
        * np.cos(K_MPC[:, None] * x[None, :] + static.PHASE[:, None])
    )


def transfer_from_field(field: np.ndarray, scales: np.ndarray) -> np.ndarray:
    arr = np.asarray(field, float)
    fh = np.fft.fft(arr) / float(arr.size)
    out = np.full(len(MODE_NUM), np.nan + 1j * np.nan, complex)
    for j, n in enumerate(MODE_NUM):
        amp = float(static.MODE_AMP[j] * scales[j])
        if amp == 0.0:
            continue
        out[j] = 2.0 * fh[int(n)] * np.exp(-1j * float(static.PHASE[j])) / amp
    return out


def positive_mode_leakage(field: np.ndarray, target_n: int) -> float:
    arr = np.asarray(field, float)
    fh = np.fft.rfft(arr) / float(arr.size)
    hi = min(int(NMAX), fh.size - 1)
    p = np.abs(fh[1:hi + 1]) ** 2
    total = float(np.sum(p))
    if total <= 1.0e-300:
        return 0.0
    idx = int(target_n) - 1
    target = float(p[idx]) if 0 <= idx < p.size else 0.0
    return float(max(total - target, 0.0) / total)


def run_with_scales(data, scales: np.ndarray):
    original = m.cos_matrix
    s = np.asarray(scales, float).copy()

    def custom_cos_matrix(nx):
        return basis_matrix(nx, s)

    d2b.set_member(REFERENCE_MEMBER)
    m.cos_matrix = custom_cos_matrix
    try:
        run = r2.integrate_combined_r2(data, NX, NSTEP, True)
    finally:
        m.cos_matrix = original

    return run


def health(run) -> dict:
    out = {
        "finite": bool(run.get("finite", False)),
        "canonical_max": float("inf"),
        "metric_max": {"hamiltonian": float("inf"), "momentum": float("inf"), "shear": float("inf")},
    }
    cps = run.get("checkpoints", [])
    if not out["finite"] or len(cps) != len(CHECK_Z):
        return out
    out["canonical_max"] = max(float(cp["canonical_constraint"]) for cp in cps)
    mm = {"hamiltonian": 0.0, "momentum": 0.0, "shear": 0.0}
    for cp in cps:
        cc = cp["metric"]["metric_correction"]["constraint"]
        for key in mm:
            mm[key] = max(mm[key], float(cc[key]))
    out["metric_max"] = mm
    return out


def extract_transfer_grid(run, scales: np.ndarray) -> np.ndarray:
    cps = run["checkpoints"]
    return np.asarray(
        [transfer_from_field(cp["metric"]["weyl"], scales) for cp in cps],
        complex,
    )


def class_transfer_grid(data) -> np.ndarray:
    rows = []
    for tau in np.asarray(data["tau_check"], float):
        phi = m.mode_values(data, float(tau), "phi")
        psi = m.mode_values(data, float(tau), "psi_bridge")
        rows.append(np.asarray(phi + psi, float))
    return np.asarray(rows, float)


def load_recorded_gaussian_ratios() -> dict:
    if not GAUSS_JSON.exists():
        raise FileNotFoundError(str(GAUSS_JSON))
    raw = json.loads(GAUSS_JSON.read_text())
    if raw.get("classification") != "FULLJ_EVOLVING_WEYL_GAUSSIAN_1D_ENSEMBLE_PASS":
        raise RuntimeError("local Gaussian 1D result is not the locked PASS classification")
    out = {}
    for row in raw.get("prefix_rows", []):
        if int(row.get("N", -1)) != 32:
            continue
        z = float(row["z"])
        out[z] = {k: float(v) for k, v in row["nonlinear_to_class_band_ratio"].items()}
    if len(out) != len(CHECK_Z):
        raise RuntimeError("local Gaussian 1D result lacks all N=32 redshift rows")
    return out


def gaussian_sample_variance() -> np.ndarray:
    rng = np.random.default_rng(20260912)
    xy = rng.normal(size=(32, len(MODE_NUM), 2))
    g = (xy[..., 0] + 1j * xy[..., 1]) / np.sqrt(2.0)
    gc = g - np.mean(g, axis=0, keepdims=True)
    return np.sum(np.abs(gc) ** 2, axis=0) / float(g.shape[0] - 1)


def gaussian_ratio_prediction(T: np.ndarray, Tc: np.ndarray) -> dict:
    svar = gaussian_sample_variance()
    weight = (np.asarray(static.MODE_AMP, float) / 2.0) ** 2 * svar
    band_members = {
        "low": [j for j, n in enumerate(MODE_NUM) if 1 <= n <= 7],
        "mid": [j for j, n in enumerate(MODE_NUM) if 8 <= n <= 15],
        "high": [j for j, n in enumerate(MODE_NUM) if 16 <= n <= 32],
    }
    out = {}
    for iz, z in enumerate(CHECK_Z):
        out[float(z)] = {}
        for band, inds in band_members.items():
            num = float(sum(weight[j] * abs(T[iz, j]) ** 2 for j in inds))
            den = float(sum(weight[j] * abs(Tc[iz, j]) ** 2 for j in inds))
            out[float(z)][band] = num / max(den, 1.0e-300)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json-out", default="results/fullj_isotropic_weyl_transfer_nodes.json")
    ap.add_argument("--npz-out", default="results/fullj_isotropic_weyl_transfer_nodes.npz")
    args = ap.parse_args()

    ancestry = {
        "r2_result_lock": is_ancestor(R2_RESULT_LOCK),
        "gaussian_1d_result_lock": is_ancestor(GAUSS1D_RESULT_LOCK),
        "geometry_result_lock": is_ancestor(GEOM_RESULT_LOCK),
        "saturated_closure_result_lock": is_ancestor(SAT_RESULT_LOCK),
        "predata_lock": is_ancestor(PREDATA_LOCK),
    }
    if not all(ancestry.values()):
        result = {"classification": INCOMPLETE, "diagnostic_complete": False, "ancestry": ancestry, "reason": "missing locked ancestry"}
        Path(args.json_out).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print("FULLJ_ISO_TRANSFER_CLASSIFICATION=" + INCOMPLETE, flush=True)
        return 3
    if not GAUSS_JSON.exists():
        result = {"classification": INCOMPLETE, "diagnostic_complete": False, "ancestry": ancestry, "reason": f"missing local {GAUSS_JSON.relative_to(ROOT)}"}
        Path(args.json_out).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print("FULLJ_ISO_TRANSFER_CLASSIFICATION=" + INCOMPLETE, flush=True)
        return 3

    print("FULLJ_ISO_TRANSFER_START", flush=True)
    print("FULLJ_ISO_TRANSFER_ANCESTRY=" + json.dumps(ancestry, sort_keys=True), flush=True)
    data = r2.r0.prepare_bridge_data()
    Tc = class_transfer_grid(data)

    scales_full = np.ones(len(MODE_NUM), float)
    multi = run_with_scales(data, scales_full)
    h_multi = health(multi)
    if not h_multi["finite"]:
        raise RuntimeError("central six-mode R2 run did not complete")
    Tmulti = extract_transfer_grid(multi, scales_full)
    print(
        "FULLJ_ISO_TRANSFER_MULTI "
        f"canonical={h_multi['canonical_max']:.3e} "
        + " ".join(f"{k}={v:.3e}" for k, v in h_multi["metric_max"].items()),
        flush=True,
    )

    single_runs = []
    Tsingle = np.full_like(Tmulti, np.nan + 1j * np.nan)
    leak = []
    health_rows = [{"scope": "multi", **h_multi}]
    for j, n in enumerate(MODE_NUM):
        s = np.zeros(len(MODE_NUM), float)
        s[j] = 1.0
        run = run_with_scales(data, s)
        hh = health(run)
        health_rows.append({"scope": f"single_n{int(n)}", **hh})
        if not hh["finite"]:
            raise RuntimeError(f"single-mode run n={int(n)} incomplete")
        TT = extract_transfer_grid(run, s)
        Tsingle[:, j] = TT[:, j]
        lj = [positive_mode_leakage(cp["metric"]["weyl"], int(n)) for cp in run["checkpoints"]]
        leak.extend(lj)
        single_runs.append(run)
        print(
            f"FULLJ_ISO_TRANSFER_SINGLE n={int(n)} leakMax={max(lj):.3e} canonical={hh['canonical_max']:.3e}",
            flush=True,
        )

    hom = []
    control_rows = []
    for j in ANCHOR_IDX:
        n = int(MODE_NUM[j])
        for fac in AMP_SCALES:
            s = np.zeros(len(MODE_NUM), float)
            s[j] = float(fac)
            run = run_with_scales(data, s)
            hh = health(run)
            health_rows.append({"scope": f"amp_n{n}_x{fac:g}", **hh})
            if not hh["finite"]:
                raise RuntimeError(f"amplitude control n={n} scale={fac:g} incomplete")
            TT = extract_transfer_grid(run, s)[:, j]
            diffs = [rel_scalar(TT[iz], Tsingle[iz, j]) for iz in range(len(CHECK_Z))]
            hom.extend(diffs)
            control_rows.append({"mode_n": n, "scale": float(fac), "relative_transfer_difference": [float(x) for x in diffs], "max": float(max(diffs))})
            print(f"FULLJ_ISO_TRANSFER_AMP n={n} scale={fac:g} maxRel={max(diffs):.3e}", flush=True)

    sep = np.asarray([[rel_scalar(Tsingle[iz, j], Tmulti[iz, j]) for j in range(len(MODE_NUM))] for iz in range(len(CHECK_Z))], float)
    phase_res = np.abs(np.imag(Tmulti)) / np.maximum(np.abs(Tmulti), 1.0e-300)
    initial = np.abs(Tmulti[0] - Tc[0]) / np.maximum(np.abs(Tc[0]), 1.0e-300)

    recorded = load_recorded_gaussian_ratios()
    predicted = gaussian_ratio_prediction(Tmulti, Tc)
    gauss_rows = []
    gauss_diff = []
    for z in CHECK_Z:
        for band in ("low", "mid", "high"):
            p = float(predicted[float(z)][band])
            r = float(recorded[float(z)][band])
            q = abs(p - r) / max(abs(p), abs(r), 1.0e-300)
            gauss_diff.append(q)
            gauss_rows.append({"z": float(z), "band": band, "predicted_ratio": p, "recorded_ratio": r, "relative_difference": float(q)})

    delta2 = np.asarray(static.PR, float)[None, :] * np.abs(Tmulti) ** 2
    p3d = (2.0 * np.pi**2 / (K_MPC[None, :] ** 3)) * delta2
    delta2_check = np.asarray(static.PR, float)[None, :] * (np.real(Tmulti) ** 2 + np.imag(Tmulti) ** 2)
    alg_res = float(np.linalg.norm(delta2 - delta2_check) / max(float(np.linalg.norm(delta2)), 1.0e-300))

    all_health = all(
        bool(q["finite"])
        and float(q["canonical_max"]) <= CANONICAL_GATE
        and all(float(v) <= METRIC_GATE for v in q["metric_max"].values())
        for q in health_rows
    )

    sep_med = float(np.median(sep))
    sep_max = float(np.max(sep))
    leak_max = float(np.max(leak))
    hom_med = float(np.median(hom))
    hom_max = float(np.max(hom))
    gd_med = float(np.median(gauss_diff))
    gd_max = float(np.max(gauss_diff))
    phase_max = float(np.max(phase_res))
    init_max = float(np.max(initial))

    g1 = bool(
        all(ancestry.values())
        and REFERENCE_MEMBER == {"sigma": 0, "kind": "simple", "beta0": 1.0}
        and np.array_equal(MODE_NUM, np.asarray([3, 5, 8, 10, 15, 20]))
        and np.array_equal(CHECK_Z, np.asarray([6.0, 5.0, 4.0, 3.0, 2.0, 1.5, 1.0, 0.5, 0.2]))
        and NX == 128 and NSTEP == 4096
    )
    g2 = bool(all_health)
    g3 = bool(init_max <= INITIAL_CLASS_GATE)
    g4 = bool(phase_max <= PHASE_GATE)
    g5 = bool(sep_med <= SEP_MED_GATE and sep_max <= SEP_MAX_GATE)
    g6 = bool(leak_max <= LEAK_GATE)
    g7 = bool(hom_med <= HOM_MED_GATE and hom_max <= HOM_MAX_GATE)
    g8 = bool(gd_med <= GAUSS_MED_GATE and gd_max <= GAUSS_MAX_GATE)
    g9 = bool(
        np.all(np.isfinite(delta2)) and np.all(delta2 >= 0.0)
        and np.all(np.isfinite(p3d)) and np.all(p3d >= 0.0)
        and alg_res <= ALG_GATE
    )
    gates = {
        "G1_provenance_setup": g1,
        "G2_finite_constraint_health": g2,
        "G3_initial_CLASS_normalization": g3,
        "G4_transfer_phase_consistency": g4,
        "G5_single_mode_separability": g5,
        "G6_off_target_leakage": g6,
        "G7_amplitude_homogeneity": g7,
        "G8_gaussian_ensemble_reconstruction": g8,
        "G9_discrete_power_node_sanity": g9,
    }
    classification = PASS if all(gates.values()) else FAIL

    summary = {
        "initial_CLASS_max_relative_error": init_max,
        "phase_max_relative_imaginary": phase_max,
        "separability_median": sep_med,
        "separability_max": sep_max,
        "off_target_leakage_max": leak_max,
        "amplitude_homogeneity_median": hom_med,
        "amplitude_homogeneity_max": hom_max,
        "gaussian_ratio_reconstruction_median": gd_med,
        "gaussian_ratio_reconstruction_max": gd_max,
        "power_identity_relative_residual": alg_res,
    }

    transfer_rows = []
    for iz, z in enumerate(CHECK_Z):
        for j, n in enumerate(MODE_NUM):
            transfer_rows.append({
                "z": float(z),
                "mode_n": int(n),
                "k_Mpc_inv": float(K_MPC[j]),
                "k_h_Mpc_inv": float(static.K_H[j]),
                "T_W_R2_real": float(np.real(Tmulti[iz, j])),
                "T_W_R2_imag": float(np.imag(Tmulti[iz, j])),
                "T_W_CLASS": float(Tc[iz, j]),
                "single_mode_T_real": float(np.real(Tsingle[iz, j])),
                "single_mode_T_imag": float(np.imag(Tsingle[iz, j])),
                "single_vs_multi_relative": float(sep[iz, j]),
                "Delta_W2": float(delta2[iz, j]),
                "P_W_Mpc3": float(p3d[iz, j]),
            })

    result = {
        "classification": classification,
        "diagnostic_complete": True,
        "git_head": git_head(),
        "ancestry": ancestry,
        "reference_member": REFERENCE_MEMBER,
        "mode_numbers": MODE_NUM.tolist(),
        "k_Mpc_inv": K_MPC.tolist(),
        "k_h_Mpc_inv": np.asarray(static.K_H, float).tolist(),
        "redshifts": CHECK_Z.tolist(),
        "health": health_rows,
        "amplitude_controls": control_rows,
        "gaussian_crosscheck": gauss_rows,
        "transfer_nodes": transfer_rows,
        "gates": gates,
        "summary": summary,
        "THREE_D_ISOTROPIC_WEYL_TRANSFER_NODES_LICENSED": bool(classification == PASS),
        "THREE_D_ISOTROPIC_WEYL_POWER_NODES_LICENSED": bool(classification == PASS),
        "THREE_D_CONTINUOUS_WEYL_POWER_LICENSED": False,
        "EVOLVING_WEYL_POWER_LICENSED": False,
        "ACT_LIKELIHOOD_LICENSED": False,
        "OBSERVATIONAL_CLAIM_LICENSED": False,
        "scope": "six discrete isotropic Weyl transfer/power nodes on the locked central saturated branch; no dense-k interpolation or lensing",
    }

    jout = Path(args.json_out)
    nout = Path(args.npz_out)
    jout.parent.mkdir(parents=True, exist_ok=True)
    jout.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    np.savez_compressed(
        nout,
        z=CHECK_Z,
        mode_n=MODE_NUM,
        k_Mpc_inv=K_MPC,
        k_h_Mpc_inv=np.asarray(static.K_H, float),
        T_W_R2=Tmulti,
        T_W_single=Tsingle,
        T_W_CLASS=Tc,
        Delta_W2=delta2,
        P_W_Mpc3=p3d,
        separability=sep,
        phase_residual=phase_res,
        initial_class_relative_error=initial,
        gaussian_ratio_relative_difference=np.asarray(gauss_diff, float).reshape(len(CHECK_Z), 3),
    )

    print("FULLJ_ISO_TRANSFER_SUMMARY=" + json.dumps(summary, sort_keys=True), flush=True)
    print("FULLJ_ISO_TRANSFER_GATES=" + json.dumps(gates, sort_keys=True), flush=True)
    print("FULLJ_ISO_TRANSFER_CLASSIFICATION=" + classification, flush=True)
    print("THREE_D_ISOTROPIC_WEYL_TRANSFER_NODES_LICENSED=" + str(bool(classification == PASS)), flush=True)
    print("THREE_D_ISOTROPIC_WEYL_POWER_NODES_LICENSED=" + str(bool(classification == PASS)), flush=True)
    print("THREE_D_CONTINUOUS_WEYL_POWER_LICENSED=False", flush=True)
    print("EVOLVING_WEYL_POWER_LICENSED=False", flush=True)
    print("ACT_LIKELIHOOD_LICENSED=False", flush=True)
    print("OBSERVATIONAL_CLAIM_LICENSED=False", flush=True)
    print("FULLJ_ISO_TRANSFER_JSON=" + str(jout), flush=True)
    print("FULLJ_ISO_TRANSFER_NPZ=" + str(nout), flush=True)
    return 0 if classification == PASS else 2


if __name__ == "__main__":
    raise SystemExit(main())
