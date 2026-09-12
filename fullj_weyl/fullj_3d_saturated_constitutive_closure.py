#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
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
from fullj_weyl import fullj_3d_lattice_shell_geometry_poc as geom
from nl1c6d2c6b import all27_physical_nonlinear_trajectories as d2b

m = r2.m
static = m.static

R2_RESULT_LOCK = "1f42f88e9724c58d2d242a65ca7266a207e4a0f8"
GAUSS1D_RESULT_LOCK = "05e38b273f91eb04b7b4c8753731017d0ed839c1"
GEOM_RESULT_LOCK = "ca6a102196055e27dc2b31379285bfc7aea1a35b"
PREDATA_LOCK = "1eeba0045304656ae73c3d2d7ae7e83796a47fe1"

PASS = "FULLJ_3D_SATURATED_CONSTITUTIVE_CLOSURE_PASS"
FAIL = "FULLJ_3D_SATURATED_CONSTITUTIVE_CLOSURE_FAIL"
INCOMPLETE = "FULLJ_3D_SATURATED_CONSTITUTIVE_CLOSURE_INCOMPLETE"

REFERENCE_MEMBER = {"sigma": 0, "kind": "simple", "beta0": 1.0}
TARGET_Z = np.asarray([6.0, 5.0, 4.0, 3.0, 2.0, 1.5, 1.0, 0.5, 0.2], float)
CONTROL_Z = np.asarray([6.0, 1.0, 0.2], float)
SHELL_RADII = np.asarray([3, 5, 8, 10, 15, 20], int)
PRIMARY_N = 64
CONTROL_N = 80
NREAL = 16
SEED = 20260914
FLUX_MED_GATE = 5.0e-3
FLUX_MAX_GATE = 2.0e-2
OP_MED_GATE = 5.0e-3
OP_MAX_GATE = 2.0e-2
SHELL_MED_GATE = 1.0e-2
SHELL_MAX_GATE = 5.0e-2
CONTROL_OP_GATE = 5.0e-3
CONTROL_SHELL_GATE = 1.0e-2


def git_head() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()


def is_ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"], cwd=ROOT,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    ).returncode == 0


def rel(a, b) -> float:
    aa = np.asarray(a)
    bb = np.asarray(b)
    return float(np.linalg.norm(aa - bb) / max(float(np.linalg.norm(aa)), float(np.linalg.norm(bb)), 1.0e-300))


def coefficient_draw(shell_halves: list[np.ndarray]):
    rng = np.random.default_rng(SEED)
    draws = []
    raw = []
    for half in shell_halves:
        xy = rng.normal(size=(NREAL, len(half), 2))
        g = (xy[..., 0] + 1j * xy[..., 1]) / np.sqrt(2.0)
        draws.append(g)
        raw.append(np.ascontiguousarray(xy, dtype=np.float64).tobytes())
    return draws, hashlib.sha256(b"".join(raw)).hexdigest()


def radial_seed(data):
    d2b.set_member(REFERENCE_MEMBER)
    run = r2.integrate_combined_r2(data, r2.NX, r2.NSTEP, True)
    if not run["finite"] or len(run["checkpoints"]) != len(data["tau_check"]):
        raise RuntimeError("locked central R2 trajectory unavailable")
    mode_num = np.asarray(static.MODE_NUM, int)
    out = {}
    for iz, z in enumerate(np.asarray(m.CHECK_Z, float)):
        cp = run["checkpoints"][iz]
        chi = np.asarray(cp["y"][1], float)
        fh = np.fft.fft(chi) / float(chi.size)
        c = np.asarray([fh[int(n)] for n in mode_num], complex)
        V = 2.0 * np.abs(c) ** 2
        a = float(m.bg_eval(data, float(cp["tau"]))[0])
        out[float(z)] = {
            "a": a,
            "tau": float(cp["tau"]),
            "V_chi": V,
            "canonical_constraint": float(cp["canonical_constraint"]),
        }
    return out


def shell_powers(h: np.ndarray, shell_vecs: list[np.ndarray]) -> np.ndarray:
    return np.asarray([geom.shell_power_and_m2_from_hat(h, vv)[0] for vv in shell_vecs], float)


def evaluate_one(N: int, z: float, ir: int, radial: dict, shell_vecs, shell_halves, draws):
    rr = radial[float(z)]
    V = np.asarray(rr["V_chi"], float)
    a = float(rr["a"])
    field = geom.build_field(N, shell_vecs, shell_halves, draws, V, ir)
    L3, lap, x, j = geom.operator3d(field, a)
    finite = bool(all(np.all(np.isfinite(v)) for v in (field, L3, lap, x, j)))

    gmag = np.asarray(x, float) * a / float(static.ACC_CONV)
    flux_num = float(np.linalg.norm((np.asarray(j, float) - 1.0) * gmag))
    flux_den = max(float(np.linalg.norm(2.0 * gmag)), 1.0e-300)
    eps_flux = flux_num / flux_den
    Lsat = 2.0 * np.asarray(lap, float)
    eps_op = rel(L3, Lsat)

    h3 = np.fft.fftn(L3) / float(N ** 3)
    h0 = np.fft.fftn(lap) / float(N ** 3)
    p3 = shell_powers(h3, shell_vecs)
    p0 = shell_powers(h0, shell_vecs)
    return {
        "finite": finite,
        "eps_flux": float(eps_flux),
        "eps_op": float(eps_op),
        "min_one_plus_j": float(np.min(1.0 + np.asarray(j, float))),
        "p3": p3,
        "p0": p0,
    }


def cell_shell_ratio(p3: np.ndarray, p0: np.ndarray) -> np.ndarray:
    a = np.mean(np.asarray(p3, float), axis=0)
    b = np.mean(np.asarray(p0, float), axis=0)
    return a / np.maximum(4.0 * b, 1.0e-300)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json-out", default="results/fullj_3d_saturated_constitutive_closure.json")
    ap.add_argument("--npz-out", default="results/fullj_3d_saturated_constitutive_closure.npz")
    args = ap.parse_args()

    ancestry = {
        "r2_result_lock": is_ancestor(R2_RESULT_LOCK),
        "gaussian_1d_result_lock": is_ancestor(GAUSS1D_RESULT_LOCK),
        "geometry_result_lock": is_ancestor(GEOM_RESULT_LOCK),
        "predata_lock": is_ancestor(PREDATA_LOCK),
    }
    if not all(ancestry.values()):
        result = {"classification": INCOMPLETE, "diagnostic_complete": False, "ancestry": ancestry}
        Path(args.json_out).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print("FULLJ_3D_SAT_CLASSIFICATION=" + INCOMPLETE, flush=True)
        return 2

    print("FULLJ_3D_SAT_START", flush=True)
    print("FULLJ_3D_SAT_ANCESTRY=" + json.dumps(ancestry, sort_keys=True), flush=True)
    print("FULLJ_3D_SAT_MEMBER=" + d2b.member_key(REFERENCE_MEMBER), flush=True)

    shell_vecs = [geom.shell_vectors(int(n)) for n in SHELL_RADII]
    shell_halves = [np.asarray([v for v in vv if geom.positive_half(v)], int) for vv in shell_vecs]
    draws, coeff_hash = coefficient_draw(shell_halves)
    print(f"FULLJ_3D_SAT_COEFFICIENTS seed={SEED} nreal={NREAL} sha256={coeff_hash}", flush=True)

    data = r2.r0.prepare_bridge_data()
    radial = radial_seed(data)
    if set(round(float(k), 12) for k in radial) != set(round(float(z), 12) for z in TARGET_Z):
        raise RuntimeError("radial seed redshift set mismatch")

    primary_eps_flux = []
    primary_eps_op = []
    min_one_plus_j = math.inf
    finite_all = True
    p3_primary = np.zeros((len(TARGET_Z), NREAL, len(SHELL_RADII)), float)
    p0_primary = np.zeros_like(p3_primary)
    rows = []

    for iz, z in enumerate(TARGET_Z):
        for ir in range(NREAL):
            q = evaluate_one(PRIMARY_N, float(z), ir, radial, shell_vecs, shell_halves, draws)
            finite_all = finite_all and bool(q["finite"])
            min_one_plus_j = min(min_one_plus_j, float(q["min_one_plus_j"]))
            primary_eps_flux.append(float(q["eps_flux"]))
            primary_eps_op.append(float(q["eps_op"]))
            p3_primary[iz, ir] = q["p3"]
            p0_primary[iz, ir] = q["p0"]
            print(
                f"FULLJ_3D_SAT_EVAL N={PRIMARY_N} z={float(z):g} realization={ir+1:02d}/{NREAL} "
                f"finite={q['finite']} epsFlux={q['eps_flux']:.6e} epsOp={q['eps_op']:.6e} "
                f"min1pj={q['min_one_plus_j']:.6e}", flush=True,
            )

    shell_ratio_primary = np.zeros((len(TARGET_Z), len(SHELL_RADII)), float)
    shell_dev = []
    for iz, z in enumerate(TARGET_Z):
        rr = cell_shell_ratio(p3_primary[iz], p0_primary[iz])
        shell_ratio_primary[iz] = rr
        for js, n in enumerate(SHELL_RADII):
            dev = abs(float(rr[js]) - 1.0)
            shell_dev.append(dev)
            rows.append({
                "scope": "primary64", "z": float(z), "shell_n": int(n),
                "R_shell": float(rr[js]), "abs_R_minus_1": float(dev),
            })

    control_op_delta = []
    control_shell_delta = []
    control_rows = []
    p3_control = np.zeros((len(CONTROL_Z), NREAL, len(SHELL_RADII)), float)
    p0_control = np.zeros_like(p3_control)
    epsop80 = np.zeros((len(CONTROL_Z), NREAL), float)
    epsop64 = np.zeros_like(epsop80)

    z_to_primary = {round(float(z), 12): i for i, z in enumerate(TARGET_Z)}
    for ic, z in enumerate(CONTROL_Z):
        ip = z_to_primary[round(float(z), 12)]
        for ir in range(NREAL):
            # Re-evaluate N=64 for exactly matched per-realization control bookkeeping.
            q64 = evaluate_one(PRIMARY_N, float(z), ir, radial, shell_vecs, shell_halves, draws)
            q80 = evaluate_one(CONTROL_N, float(z), ir, radial, shell_vecs, shell_halves, draws)
            finite_all = finite_all and bool(q64["finite"]) and bool(q80["finite"])
            min_one_plus_j = min(min_one_plus_j, float(q64["min_one_plus_j"]), float(q80["min_one_plus_j"]))
            epsop64[ic, ir] = q64["eps_op"]
            epsop80[ic, ir] = q80["eps_op"]
            p3_control[ic, ir] = q80["p3"]
            p0_control[ic, ir] = q80["p0"]
            print(
                f"FULLJ_3D_SAT_CONTROL N={CONTROL_N} z={float(z):g} realization={ir+1:02d}/{NREAL} "
                f"finite={q80['finite']} epsOp={q80['eps_op']:.6e} min1pj={q80['min_one_plus_j']:.6e}",
                flush=True,
            )

        d_op = abs(float(np.mean(epsop80[ic])) - float(np.mean(epsop64[ic])))
        control_op_delta.append(d_op)
        rr80 = cell_shell_ratio(p3_control[ic], p0_control[ic])
        rr64 = shell_ratio_primary[ip]
        for js, n in enumerate(SHELL_RADII):
            d_shell = abs(float(rr80[js]) - float(rr64[js]))
            control_shell_delta.append(d_shell)
            control_rows.append({
                "scope": "control80", "z": float(z), "shell_n": int(n),
                "R_shell_64": float(rr64[js]), "R_shell_80": float(rr80[js]),
                "abs_delta_R": float(d_shell), "mean_eps_op_64": float(np.mean(epsop64[ic])),
                "mean_eps_op_80": float(np.mean(epsop80[ic])), "abs_delta_eps_op": float(d_op),
            })
    rows.extend(control_rows)

    flux_med = float(np.median(primary_eps_flux))
    flux_max = float(np.max(primary_eps_flux))
    op_med = float(np.median(primary_eps_op))
    op_max = float(np.max(primary_eps_op))
    shell_med = float(np.median(shell_dev))
    shell_max = float(np.max(shell_dev))
    ctrl_op_max = float(np.max(control_op_delta))
    ctrl_shell_max = float(np.max(control_shell_delta))

    g1 = bool(
        all(ancestry.values()) and REFERENCE_MEMBER == {"sigma": 0, "kind": "simple", "beta0": 1.0}
        and np.array_equal(TARGET_Z, np.asarray([6.0,5.0,4.0,3.0,2.0,1.5,1.0,0.5,0.2]))
        and np.array_equal(CONTROL_Z, np.asarray([6.0,1.0,0.2]))
        and np.array_equal(SHELL_RADII, np.asarray([3,5,8,10,15,20]))
        and PRIMARY_N == 64 and CONTROL_N == 80 and NREAL == 16 and SEED == 20260914
    )
    g2 = bool(finite_all and np.isfinite(min_one_plus_j) and min_one_plus_j > 0.0)
    g3 = bool(flux_med <= FLUX_MED_GATE and flux_max <= FLUX_MAX_GATE)
    g4 = bool(op_med <= OP_MED_GATE and op_max <= OP_MAX_GATE)
    g5 = bool(shell_med <= SHELL_MED_GATE and shell_max <= SHELL_MAX_GATE)
    g6 = bool(ctrl_op_max <= CONTROL_OP_GATE and ctrl_shell_max <= CONTROL_SHELL_GATE)
    g7 = bool(d2b.member_key(REFERENCE_MEMBER) == "sigma=+0|kind=simple|beta0=1")
    gates = {
        "G1_locked_provenance_setup": g1,
        "G2_finite_healthy_operator": g2,
        "G3_weighted_flux_saturation": g3,
        "G4_full_operator_saturation": g4,
        "G5_shell_power_saturation": g5,
        "G6_resolution_control_consistency": g6,
        "G7_no_deterministic_theory_mixing": g7,
    }
    classification = PASS if all(gates.values()) else FAIL
    summary = {
        "coefficient_sha256": coeff_hash,
        "finite_all": bool(finite_all),
        "min_one_plus_j": float(min_one_plus_j),
        "eps_flux_median": flux_med, "eps_flux_max": flux_max,
        "eps_op_median": op_med, "eps_op_max": op_max,
        "shell_abs_R_minus_1_median": shell_med, "shell_abs_R_minus_1_max": shell_max,
        "control_abs_delta_eps_op_max": ctrl_op_max,
        "control_abs_delta_R_shell_max": ctrl_shell_max,
    }
    result = {
        "classification": classification,
        "diagnostic_complete": True,
        "git_head": git_head(),
        "ancestry": ancestry,
        "reference_member": REFERENCE_MEMBER,
        "target_z": TARGET_Z.tolist(), "control_z": CONTROL_Z.tolist(),
        "shell_radii": SHELL_RADII.tolist(), "Nreal": NREAL, "seed": SEED,
        "primary_grid": PRIMARY_N, "control_grid": CONTROL_N,
        "gates": gates, "summary": summary, "rows": rows,
        "radial_seed": {
            str(z): {"a": float(radial[z]["a"]), "tau": float(radial[z]["tau"]),
                     "V_chi": np.asarray(radial[z]["V_chi"], float).tolist(),
                     "canonical_constraint": float(radial[z]["canonical_constraint"])}
            for z in sorted(radial)
        },
        "THREE_D_SATURATED_LAPLACIAN_CLOSURE_LICENSED": bool(classification == PASS),
        "THREE_D_ISOTROPIC_TRANSFER_CONSTRUCTION_LICENSED": bool(classification == PASS),
        "THREE_D_ISOTROPIC_WEYL_POWER_LICENSED": False,
        "EVOLVING_WEYL_POWER_LICENSED": False,
        "ACT_LIKELIHOOD_LICENSED": False,
        "OBSERVATIONAL_CLAIM_LICENSED": False,
        "scope": "3D stochastic lattice-shell audit of saturated constitutive closure on locked central R2 radial amplitudes; not a full 3D time evolution",
    }

    jout = Path(args.json_out); nout = Path(args.npz_out)
    jout.parent.mkdir(parents=True, exist_ok=True)
    jout.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    np.savez_compressed(
        nout,
        target_z=TARGET_Z, control_z=CONTROL_Z, shell_radii=SHELL_RADII,
        shell_ratio_primary=shell_ratio_primary,
        eps_flux_primary=np.asarray(primary_eps_flux, float).reshape(len(TARGET_Z), NREAL),
        eps_op_primary=np.asarray(primary_eps_op, float).reshape(len(TARGET_Z), NREAL),
        eps_op_control_64=epsop64, eps_op_control_80=epsop80,
    )

    print("FULLJ_3D_SAT_SUMMARY=" + json.dumps(summary, sort_keys=True), flush=True)
    print("FULLJ_3D_SAT_GATES=" + json.dumps(gates, sort_keys=True), flush=True)
    print("FULLJ_3D_SAT_CLASSIFICATION=" + classification, flush=True)
    print("THREE_D_SATURATED_LAPLACIAN_CLOSURE_LICENSED=" + str(bool(classification == PASS)), flush=True)
    print("THREE_D_ISOTROPIC_TRANSFER_CONSTRUCTION_LICENSED=" + str(bool(classification == PASS)), flush=True)
    print("THREE_D_ISOTROPIC_WEYL_POWER_LICENSED=False", flush=True)
    print("EVOLVING_WEYL_POWER_LICENSED=False", flush=True)
    print("ACT_LIKELIHOOD_LICENSED=False", flush=True)
    print("OBSERVATIONAL_CLAIM_LICENSED=False", flush=True)
    print("FULLJ_3D_SAT_JSON=" + str(jout), flush=True)
    print("FULLJ_3D_SAT_NPZ=" + str(nout), flush=True)
    return 0 if classification == PASS else 2


if __name__ == "__main__":
    raise SystemExit(main())
