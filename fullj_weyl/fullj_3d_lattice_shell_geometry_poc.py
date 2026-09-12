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
from nl1c6d2c6b import all27_physical_nonlinear_trajectories as d2b

m = r2.m
static = m.static

R2_RESULT_LOCK = "1f42f88e9724c58d2d242a65ca7266a207e4a0f8"
COV_RESULT_LOCK = "87434c21866241b1b35588ec88e93e99a6f5db1a"
GAUSS1D_RESULT_LOCK = "05e38b273f91eb04b7b4c8753731017d0ed839c1"
PREDATA_LOCK = "7cffa7213d1d9e40a014e4cd7eea6fa264f22877"

PASS = "FULLJ_3D_LATTICE_SHELL_GEOMETRY_POC_PASS"
FAIL = "FULLJ_3D_LATTICE_SHELL_GEOMETRY_POC_FAIL"
INCOMPLETE = "FULLJ_3D_LATTICE_SHELL_GEOMETRY_POC_INCOMPLETE"

REFERENCE_MEMBER = {"sigma": 0, "kind": "simple", "beta0": 1.0}
TARGET_Z = np.asarray([2.0, 0.5, 0.2], float)
SHELL_RADII = np.asarray([3, 5, 8, 10, 15, 20], int)
SHELL_HALF_WIDTH = 0.5
GRIDS = (64, 80)
NREAL = 8
SEED = 20260913
GEOM_M2_GATE = 1.0e-12
GEOM_M4_GATE = 1.0e-2
REDUCTION_GATE = 1.0e-12
ROTATION_GATE = 1.0e-12
CONV_MED_GATE = 0.15
CONV_MAX_GATE = 0.35
OUTPUT_ISO_GATE = 0.08


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


def shell_vectors(radius: int) -> np.ndarray:
    lim = int(math.ceil(radius + SHELL_HALF_WIDTH))
    vecs = []
    for ix in range(-lim, lim + 1):
        for iy in range(-lim, lim + 1):
            for iz in range(-lim, lim + 1):
                if ix == 0 and iy == 0 and iz == 0:
                    continue
                rr = math.sqrt(ix * ix + iy * iy + iz * iz)
                if abs(rr - float(radius)) <= SHELL_HALF_WIDTH + 1.0e-15:
                    vecs.append((ix, iy, iz))
    return np.asarray(sorted(set(vecs)), int)


def positive_half(v: np.ndarray) -> bool:
    for q in np.asarray(v, int):
        if q != 0:
            return bool(q > 0)
    return False


def shell_geometry(vecs: np.ndarray) -> dict:
    vv = np.asarray(vecs, float)
    uu = vv / np.linalg.norm(vv, axis=1)[:, None]
    m2 = (uu.T @ uu) / float(len(uu))
    m2_res = float(np.max(np.abs(m2 - np.eye(3) / 3.0)))
    ux4 = float(np.mean(uu[:, 0] ** 4))
    ux2uy2 = float(np.mean((uu[:, 0] ** 2) * (uu[:, 1] ** 2)))
    return {
        "count": int(len(uu)),
        "pair_count": int(sum(positive_half(v) for v in vecs)),
        "second_moment": m2.tolist(),
        "second_moment_max_residual": m2_res,
        "ux4": ux4,
        "ux2uy2": ux2uy2,
        "ux4_isotropic_error": abs(ux4 - 1.0 / 5.0),
        "ux2uy2_isotropic_error": abs(ux2uy2 - 1.0 / 15.0),
    }


def fft_mode_axis(N: int) -> np.ndarray:
    return np.rint(np.fft.fftfreq(N) * N).astype(int)


def spectral_arrays(N: int):
    mode = fft_mode_axis(N)
    kfund = 2.0 * np.pi / static.BOX
    k = kfund * mode.astype(float)
    kx = k[:, None, None]
    ky = k[None, :, None]
    kz = k[None, None, :]
    cutoff = float(N) / 3.0 + 1.0e-12
    mask1 = np.abs(mode) <= cutoff
    mask = mask1[:, None, None] & mask1[None, :, None] & mask1[None, None, :]
    return kx, ky, kz, mask


def normalized_hat_to_field(h: np.ndarray) -> np.ndarray:
    N = h.shape[0]
    return np.fft.ifftn(h * float(N ** 3)).real


def operator3d(field: np.ndarray, a: float):
    f = np.asarray(field, float)
    N = int(f.shape[0])
    if f.shape != (N, N, N):
        raise ValueError("3D field must be cubic")
    kx, ky, kz, mask = spectral_arrays(N)
    fh = np.fft.fftn(f)
    gx = np.fft.ifftn(1j * kx * fh).real
    gy = np.fft.ifftn(1j * ky * fh).real
    gz = np.fft.ifftn(1j * kz * fh).real
    gmag = np.sqrt(gx * gx + gy * gy + gz * gz)
    x = static.ACC_CONV * gmag / float(a)
    j, _ = static.j_and_prime(x, 1.0, "simple", saturated=False)
    onepj = 1.0 + j
    divh = (
        1j * kx * (np.fft.fftn(onepj * gx) * mask)
        + 1j * ky * (np.fft.fftn(onepj * gy) * mask)
        + 1j * kz * (np.fft.fftn(onepj * gz) * mask)
    )
    l3 = np.fft.ifftn(divh).real
    lap = np.fft.ifftn(-(kx * kx + ky * ky + kz * kz) * fh).real
    return l3, lap, x, j


def operator1d(field: np.ndarray, a: float):
    f = np.asarray(field, float)
    N = f.size
    mode = fft_mode_axis(N)
    k = (2.0 * np.pi / static.BOX) * mode.astype(float)
    mask = np.abs(mode) <= float(N) / 3.0 + 1.0e-12
    fh = np.fft.fft(f)
    g = np.fft.ifft(1j * k * fh).real
    x = static.ACC_CONV * np.abs(g) / float(a)
    j, _ = static.j_and_prime(x, 1.0, "simple", saturated=False)
    out = np.fft.ifft(1j * k * (np.fft.fft((1.0 + j) * g) * mask)).real
    return out


def shell_power_and_m2_from_hat(hn: np.ndarray, vecs: np.ndarray):
    N = hn.shape[0]
    weights = []
    units = []
    for v in np.asarray(vecs, int):
        idx = tuple(int(q) % N for q in v)
        weights.append(float(abs(hn[idx]) ** 2))
        vf = np.asarray(v, float)
        units.append(vf / np.linalg.norm(vf))
    w = np.asarray(weights, float)
    u = np.asarray(units, float)
    power = float(np.sum(w))
    if power <= 0.0:
        m2 = np.zeros((3, 3), float)
    else:
        m2 = np.einsum("n,ni,nj->ij", w, u, u) / power
    return power, m2


def central_r2_radial_seed(data):
    d2b.set_member(REFERENCE_MEMBER)
    run = r2.integrate_combined_r2(data, r2.NX, r2.NSTEP, True)
    if not run["finite"] or len(run["checkpoints"]) != len(data["tau_check"]):
        raise RuntimeError("central R2 trajectory unavailable")
    zall = np.asarray(m.CHECK_Z, float)
    mode_num = np.asarray(static.MODE_NUM, int)
    rows = {}
    coeffs = {}
    for z in TARGET_Z:
        ii = np.where(np.isclose(zall, z, rtol=0.0, atol=1.0e-12))[0]
        if len(ii) != 1:
            raise RuntimeError(f"missing checkpoint z={z:g}")
        cp = run["checkpoints"][int(ii[0])]
        chi = np.asarray(cp["y"][1], float)
        fh = np.fft.fft(chi) / float(chi.size)
        c = np.asarray([fh[int(n)] for n in mode_num], complex)
        V = 2.0 * np.abs(c) ** 2
        a = float(m.bg_eval(data, float(cp["tau"]))[0])
        rows[float(z)] = {
            "a": a,
            "tau": float(cp["tau"]),
            "V_chi": V.tolist(),
            "canonical_constraint": float(cp["canonical_constraint"]),
        }
        coeffs[float(z)] = c
    return rows, coeffs


def coefficient_draw(shell_halves: list[np.ndarray]):
    rng = np.random.default_rng(SEED)
    draws = []
    raw = []
    for half in shell_halves:
        xy = rng.normal(size=(NREAL, len(half), 2))
        g = (xy[..., 0] + 1j * xy[..., 1]) / np.sqrt(2.0)
        raw.append(np.ascontiguousarray(xy, dtype=np.float64).tobytes())
        draws.append(g)
    digest = hashlib.sha256(b"".join(raw)).hexdigest()
    return draws, digest


def build_field(N: int, shell_vecs: list[np.ndarray], shell_halves: list[np.ndarray], draws, V: np.ndarray, ir: int):
    h = np.zeros((N, N, N), complex)
    for js, (_vecs, half) in enumerate(zip(shell_vecs, shell_halves)):
        pair_count = len(half)
        scale = math.sqrt(max(float(V[js]), 0.0)) / math.sqrt(2.0 * float(pair_count))
        gv = draws[js][ir]
        for ip, v in enumerate(half):
            c = scale * gv[ip]
            idx = tuple(int(q) % N for q in v)
            midx = tuple(int(-q) % N for q in v)
            h[idx] = c
            h[midx] = np.conj(c)
    return normalized_hat_to_field(h)


def axial_reduction(coeffs_z: np.ndarray, a: float):
    N = GRIDS[0]
    h1 = np.zeros(N, complex)
    for c, n in zip(np.asarray(coeffs_z, complex), np.asarray(static.MODE_NUM, int)):
        h1[int(n) % N] = c
        h1[int(-n) % N] = np.conj(c)
    f1 = np.fft.ifft(h1 * float(N)).real
    out1 = operator1d(f1, a)
    f3 = np.broadcast_to(f1[:, None, None], (N, N, N)).copy()
    out3, _, _, _ = operator3d(f3, a)
    return rel(out3[:, 0, 0], out1)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json-out", default="results/fullj_3d_lattice_shell_geometry_poc.json")
    ap.add_argument("--npz-out", default="results/fullj_3d_lattice_shell_geometry_poc.npz")
    args = ap.parse_args()

    ancestry = {
        "r2_result_lock": is_ancestor(R2_RESULT_LOCK),
        "covariance_result_lock": is_ancestor(COV_RESULT_LOCK),
        "gaussian_1d_result_lock": is_ancestor(GAUSS1D_RESULT_LOCK),
        "predata_lock": is_ancestor(PREDATA_LOCK),
    }
    if not all(ancestry.values()):
        result = {"classification": INCOMPLETE, "diagnostic_complete": False, "ancestry": ancestry}
        Path(args.json_out).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print("FULLJ_3D_SHELL_CLASSIFICATION=" + INCOMPLETE, flush=True)
        return 2

    print("FULLJ_3D_SHELL_START", flush=True)
    print("FULLJ_3D_SHELL_ANCESTRY=" + json.dumps(ancestry, sort_keys=True), flush=True)

    shell_vecs = [shell_vectors(int(n)) for n in SHELL_RADII]
    shell_halves = [np.asarray([v for v in vv if positive_half(v)], int) for vv in shell_vecs]
    geom = [shell_geometry(vv) for vv in shell_vecs]
    for n, g in zip(SHELL_RADII, geom):
        print(
            f"FULLJ_3D_SHELL_GEOM n={int(n)} count={g['count']} pairs={g['pair_count']} "
            f"m2={g['second_moment_max_residual']:.3e} "
            f"m4a={g['ux4_isotropic_error']:.3e} m4b={g['ux2uy2_isotropic_error']:.3e}",
            flush=True,
        )

    data = r2.r0.prepare_bridge_data()
    radial, radial_coeff = central_r2_radial_seed(data)
    draws, coeff_hash = coefficient_draw(shell_halves)
    print(f"FULLJ_3D_SHELL_COEFFICIENTS seed={SEED} nreal={NREAL} sha256={coeff_hash}", flush=True)

    z02 = float(TARGET_Z[-1])
    reduction = axial_reduction(radial_coeff[z02], float(radial[z02]["a"]))
    print(f"FULLJ_3D_SHELL_AXIAL_REDUCTION relL2={reduction:.12e}", flush=True)

    frot = build_field(GRIDS[0], shell_vecs, shell_halves, draws, np.asarray(radial[z02]["V_chi"], float), 0)
    out0, _, _, _ = operator3d(frot, float(radial[z02]["a"]))
    perm = (1, 2, 0)
    invperm = tuple(np.argsort(perm))
    fr = np.transpose(frot, perm)
    outr, _, _, _ = operator3d(fr, float(radial[z02]["a"]))
    rotation = rel(np.transpose(outr, invperm), out0)
    print(f"FULLJ_3D_SHELL_ROTATION relL2={rotation:.12e}", flush=True)

    powers = {N: np.zeros((len(TARGET_Z), len(SHELL_RADII), NREAL), float) for N in GRIDS}
    linear_powers = {N: np.zeros_like(powers[N]) for N in GRIDS}
    excess_powers = {N: np.zeros_like(powers[N]) for N in GRIDS}
    m2_num = np.zeros((len(TARGET_Z), len(SHELL_RADII), 3, 3), float)
    m2_den = np.zeros((len(TARGET_Z), len(SHELL_RADII)), float)
    finite_all = True
    min_onepj = math.inf

    for N in GRIDS:
        for iz, z in enumerate(TARGET_Z):
            V = np.asarray(radial[float(z)]["V_chi"], float)
            a = float(radial[float(z)]["a"])
            for ir in range(NREAL):
                field = build_field(N, shell_vecs, shell_halves, draws, V, ir)
                l3, l0, x, j = operator3d(field, a)
                finite = bool(all(np.all(np.isfinite(v)) for v in (field, l3, l0, x, j)))
                finite_all = finite_all and finite
                min_onepj = min(min_onepj, float(np.min(1.0 + j)))
                h3 = np.fft.fftn(l3) / float(N ** 3)
                h0 = np.fft.fftn(l0) / float(N ** 3)
                he = np.fft.fftn(l3 - l0) / float(N ** 3)
                for js, vv in enumerate(shell_vecs):
                    p3, M = shell_power_and_m2_from_hat(h3, vv)
                    p0, _ = shell_power_and_m2_from_hat(h0, vv)
                    pe, _ = shell_power_and_m2_from_hat(he, vv)
                    powers[N][iz, js, ir] = p3
                    linear_powers[N][iz, js, ir] = p0
                    excess_powers[N][iz, js, ir] = pe
                    if N == GRIDS[-1]:
                        m2_num[iz, js] += M * p3
                        m2_den[iz, js] += p3
                print(
                    f"FULLJ_3D_SHELL_EVAL N={N} z={float(z):g} realization={ir+1:02d}/{NREAL} "
                    f"finite={finite} min1pj={float(np.min(1.0+j)):.6e}",
                    flush=True,
                )

    rows = []
    conv = []
    iso = []
    for iz, z in enumerate(TARGET_Z):
        for js, n in enumerate(SHELL_RADII):
            p64 = float(np.mean(powers[GRIDS[0]][iz, js]))
            p80 = float(np.mean(powers[GRIDS[1]][iz, js]))
            q = abs(p80 - p64) / max(abs(p80), abs(p64), 1.0e-300)
            conv.append(q)
            M = m2_num[iz, js] / max(m2_den[iz, js], 1.0e-300)
            ires = float(np.max(np.abs(M - np.eye(3) / 3.0)))
            iso.append(ires)
            p0 = float(np.mean(linear_powers[GRIDS[1]][iz, js]))
            pe = float(np.mean(excess_powers[GRIDS[1]][iz, js]))
            rows.append({
                "z": float(z), "shell_n": int(n),
                "P_L3_N64": p64, "P_L3_N80": p80,
                "d64_80": float(q),
                "P_L0_N80": p0,
                "P_excess_N80": pe,
                "P_L3_to_L0_N80": float(p80 / max(p0, 1.0e-300)),
                "output_M2": M.tolist(),
                "output_isotropy_max_residual": ires,
            })

    conv_med = float(np.median(conv))
    conv_max = float(np.max(conv))
    iso_max = float(np.max(iso))
    g1 = bool(
        all(ancestry.values())
        and REFERENCE_MEMBER == {"sigma": 0, "kind": "simple", "beta0": 1.0}
        and np.array_equal(TARGET_Z, np.asarray([2.0, 0.5, 0.2]))
        and np.array_equal(SHELL_RADII, np.asarray([3, 5, 8, 10, 15, 20]))
        and GRIDS == (64, 80) and NREAL == 8 and SEED == 20260913
    )
    g2 = bool(all(
        q["second_moment_max_residual"] <= GEOM_M2_GATE
        and q["ux4_isotropic_error"] <= GEOM_M4_GATE
        and q["ux2uy2_isotropic_error"] <= GEOM_M4_GATE
        for q in geom
    ))
    g3 = bool(reduction <= REDUCTION_GATE)
    g4 = bool(rotation <= ROTATION_GATE)
    g5 = bool(finite_all and np.isfinite(min_onepj) and min_onepj > 0.0)
    g6 = bool(conv_med <= CONV_MED_GATE and conv_max <= CONV_MAX_GATE)
    g7 = bool(iso_max <= OUTPUT_ISO_GATE)
    gates = {
        "G1_provenance_and_frozen_setup": g1,
        "G2_shell_geometry_isotropy": g2,
        "G3_axial_3D_to_1D_reduction": g3,
        "G4_cubic_rotation_equivariance": g4,
        "G5_finite_healthy_3D_operator": g5,
        "G6_N64_to_N80_shell_power_convergence": g6,
        "G7_output_angular_isotropy": g7,
    }
    classification = PASS if all(gates.values()) else FAIL
    summary = {
        "coefficient_sha256": coeff_hash,
        "axial_reduction_relL2": reduction,
        "rotation_equivariance_relL2": rotation,
        "min_one_plus_j": min_onepj,
        "d64_80_median": conv_med,
        "d64_80_max": conv_max,
        "output_isotropy_max_residual": iso_max,
        "finite_all": bool(finite_all),
    }
    result = {
        "classification": classification,
        "diagnostic_complete": True,
        "git_head": git_head(),
        "ancestry": ancestry,
        "reference_member": REFERENCE_MEMBER,
        "target_z": TARGET_Z.tolist(),
        "shell_radii": SHELL_RADII.tolist(),
        "shell_half_width": SHELL_HALF_WIDTH,
        "grids": list(GRIDS),
        "Nreal": NREAL,
        "seed": SEED,
        "shell_geometry": geom,
        "radial_seed": radial,
        "gates": gates,
        "summary": summary,
        "rows": rows,
        "THREE_D_LATTICE_SHELL_GEOMETRY_TESTED": True,
        "THREE_D_EVOLVING_STOCHASTIC_ENSEMBLE_LICENSED": bool(classification == PASS),
        "THREE_D_ISOTROPIC_WEYL_POWER_LICENSED": False,
        "EVOLVING_WEYL_POWER_LICENSED": False,
        "ACT_LIKELIHOOD_LICENSED": False,
        "OBSERVATIONAL_CLAIM_LICENSED": False,
        "scope": "3D lattice-shell nonlinear scalar-current geometry POC seeded by six radial chi variances from the locked central 1D R2 trajectory; not a full 3D time evolution",
    }

    jout = Path(args.json_out)
    nout = Path(args.npz_out)
    jout.parent.mkdir(parents=True, exist_ok=True)
    jout.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    np.savez_compressed(
        nout,
        target_z=TARGET_Z,
        shell_radii=SHELL_RADII,
        P_L3_N64=np.mean(powers[GRIDS[0]], axis=2),
        P_L3_N80=np.mean(powers[GRIDS[1]], axis=2),
        P_L0_N80=np.mean(linear_powers[GRIDS[1]], axis=2),
        P_excess_N80=np.mean(excess_powers[GRIDS[1]], axis=2),
        d64_80=np.asarray(conv, float).reshape(len(TARGET_Z), len(SHELL_RADII)),
        output_isotropy=np.asarray(iso, float).reshape(len(TARGET_Z), len(SHELL_RADII)),
    )

    print("FULLJ_3D_SHELL_SUMMARY=" + json.dumps(summary, sort_keys=True), flush=True)
    print("FULLJ_3D_SHELL_GATES=" + json.dumps(gates, sort_keys=True), flush=True)
    print("FULLJ_3D_SHELL_CLASSIFICATION=" + classification, flush=True)
    print("THREE_D_LATTICE_SHELL_GEOMETRY_TESTED=True", flush=True)
    print("THREE_D_EVOLVING_STOCHASTIC_ENSEMBLE_LICENSED=" + str(bool(classification == PASS)), flush=True)
    print("THREE_D_ISOTROPIC_WEYL_POWER_LICENSED=False", flush=True)
    print("EVOLVING_WEYL_POWER_LICENSED=False", flush=True)
    print("ACT_LIKELIHOOD_LICENSED=False", flush=True)
    print("OBSERVATIONAL_CLAIM_LICENSED=False", flush=True)
    print("FULLJ_3D_SHELL_JSON=" + str(jout), flush=True)
    print("FULLJ_3D_SHELL_NPZ=" + str(nout), flush=True)
    return 0 if classification == PASS else 2


if __name__ == "__main__":
    raise SystemExit(main())
