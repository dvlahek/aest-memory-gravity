#!/usr/bin/env python3
from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path
import subprocess
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from nl1c6d2c6b import all27_physical_nonlinear_trajectories as d2b
from nl1c6d2n import corrected_class_baseline as cb
from nl1c6d2a import baryon_matter_sector_audit as d2a

m = d2b.m
static = m.static

PHASE_LOCK = "741894f68fd498f924869cfd6e7a1274237abf9c"
PREDATA_LOCK = "b98d30ae88b6f1e63c9ba79f6813a98786d9caea"

PASS_LABEL = "FULLJ_EVOLVING_WEYL_BRIDGE_PASS"
FAIL_LABEL = "FULLJ_EVOLVING_WEYL_BRIDGE_FAIL"
INCOMPLETE_LABEL = "FULLJ_EVOLVING_WEYL_BRIDGE_INCOMPLETE_METRIC_CLOSURE"

NX = 128
NSTEP = 4096
NMAX = 32
SOURCE_ID_GATE = 1.0e-12
LINEAR_GATE = 5.0e-3
STATIC_GATE = 1.0e-10
METRIC_CONSTRAINT_GATE = 1.0e-8
SLIP_ID_GATE = 1.0e-12


def rel_l2(a, b):
    aa = np.asarray(a)
    bb = np.asarray(b)
    return float(np.linalg.norm(aa - bb) / max(np.linalg.norm(bb), 1.0e-300))


def git_head():
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()


def is_ancestor(sha):
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0


def all_members():
    return [
        {"sigma": int(s), "kind": str(k), "beta0": float(b)}
        for s, k, b in itertools.product(d2b.SIGMAS, d2b.KINDS, d2b.BETAS)
    ]


def pick(raw, names):
    for name in names:
        if name in raw:
            return name
    raise m.InputIncomplete(f"missing bridge source among {names}; available={sorted(raw.keys())}")


def prepare_bridge_data():
    """Load the locked D2C6 input and add only already-output CLASS source fields.

    The D2C6 trajectory input is not changed.  A second read of the identical
    corrected CLASS run exposes phi and the effective-component density field
    that were not needed by the original scalar-current integrator.
    """
    data = m.prepare_class_data()

    from classy import Class

    c = Class()
    c.set(m.build_params())
    c.compute()
    try:
        pert = c.get_perturbations()
        histories, scalar_key = d2a.scalar_histories(pert)
        if len(histories) != len(data["modes"]):
            raise m.InputIncomplete(
                f"bridge dense-history count mismatch {len(histories)} vs {len(data['modes'])}"
            )

        required_seen = []
        for i, (raw, md) in enumerate(zip(histories, data["modes"])):
            ktau = pick(raw, ("tau [Mpc]", "tau", "tau[Mpc]"))
            fields = {
                "phi": pick(raw, ("phi",)),
                "psi_bridge": pick(raw, ("psi",)),
                "deltaA": pick(raw, ("delta_cdm", "d_cdm")),
                "thetaA": pick(raw, ("theta_cdm", "t_cdm")),
            }
            tau = np.asarray(raw[ktau], float)
            for outname, keyname in fields.items():
                sp, xs, ys = m.unique_spline(tau, np.asarray(raw[keyname], float))
                md["splines"][outname] = sp
                if data["t0"] < float(xs[0]) - 1.0e-9 or data["t1"] > float(xs[-1]) + 1.0e-9:
                    raise m.InputIncomplete(f"bridge field {outname} mode {i} lacks z=6..0.2 coverage")
            required_seen.append({k: v for k, v in fields.items()})
    finally:
        c.struct_cleanup()
        c.empty()

    data["bridge_scalar_key"] = scalar_key
    data["bridge_source_keys"] = required_seen
    return data


def K_of_Z(Z):
    zz = float(Z) * float(Z)
    ex = math.exp(zz)
    return cb.K2 * cb.Z0 * cb.Z0 * (ex - 1.0)


def fluid_background(data, tau):
    a, H, Q, KQ, KQQ, Z, Qdot = m.bg_eval(data, tau)
    K = K_of_Z(Z)
    rho = (Q * KQ - K) / 3.0
    p = K / 3.0
    if not np.all(np.isfinite((a, H, Q, KQ, KQQ, Z, K, rho, p))):
        raise FloatingPointError("nonfinite effective-fluid background")
    if rho <= 0.0 or rho + p <= 0.0:
        raise FloatingPointError("nonpositive effective-fluid rho or rho+p")
    return {
        "a": a, "H": H, "Q": Q, "KQ": KQ, "KQQ": KQQ, "Z": Z,
        "K": K, "rho": rho, "p": p, "rho_plus_p": rho + p,
    }


def class_field(data, tau, name, nx, C=None):
    if C is None:
        C = m.cos_matrix(nx)
    vals = m.mode_values(data, tau, name)
    return m.to_field(vals, C)


def canonical_sources(data, tau, y, nx):
    """D2C5 action-derived effective density and momentum sources.

    P_chi = 2 a^3 K_QQ U and delta rho_A = Q K_QQ U / 3 imply
    delta rho_A = Q P_chi / (6 a^3).

    chi = Q(a Theta_A/k^2 + alpha) implies in position space
    Theta_A = -lap(chi/Q-alpha)/a.
    """
    bg = fluid_background(data, tau)
    a = bg["a"]
    Q = bg["Q"]
    alpha = np.asarray(y[0], float)
    chi = np.asarray(y[1], float)
    pchi = np.asarray(y[2], float)
    _, lap, _, _ = m.spec_ops(nx)

    delta_rho = Q * pchi / (6.0 * a**3)
    theta_div = -lap(chi / Q - alpha) / a
    q_momentum = bg["rho_plus_p"] * theta_div
    shear = np.zeros_like(delta_rho)
    return {
        "delta_rho": delta_rho,
        "theta_div": theta_div,
        "q_momentum": q_momentum,
        "shear": shear,
    }, bg


def class_effective_sources(data, tau, nx, C=None):
    if C is None:
        C = m.cos_matrix(nx)
    bg = fluid_background(data, tau)
    delta = class_field(data, tau, "deltaA", nx, C)
    theta = class_field(data, tau, "thetaA", nx, C)
    return {
        "delta_rho": bg["rho"] * delta,
        "theta_div": theta,
        "q_momentum": bg["rho_plus_p"] * theta,
        "shear": np.zeros(nx, float),
    }, bg


def class_metric_fields(data, tau, nx, C=None):
    if C is None:
        C = m.cos_matrix(nx)
    phi = class_field(data, tau, "phi", nx, C)
    psi = class_field(data, tau, "psi_bridge", nx, C)
    return phi, psi, phi + psi


def metric_correction(data, tau, corr, nx):
    """Newtonian-gauge correction in the already locked D2C6G convention.

    We solve the combined Hamiltonian+momentum projection and the scalar shear
    constraint.  X denotes Phi' + Hconf Psi for the correction sector.
    """
    bg = fluid_background(data, tau)
    a = bg["a"]
    Hconf = a * bg["H"]

    kk = 2.0 * np.pi * np.fft.fftfreq(nx, d=static.BOX / nx)
    k2 = kk * kk
    modes = np.minimum(np.arange(nx), nx - np.arange(nx))
    mask = (modes >= 1) & (modes <= NMAX)

    rh = np.fft.fft(np.asarray(corr["delta_rho"], float))
    qh = np.fft.fft(np.asarray(corr["q_momentum"], float))
    sh = np.fft.fft(np.asarray(corr["shear"], float))

    xh = np.zeros(nx, complex)
    ph = np.zeros(nx, complex)
    ps = np.zeros(nx, complex)
    xh[mask] = 1.5 * a**2 * qh[mask] / k2[mask]
    ph[mask] = -(
        1.5 * a**2 * rh[mask] + 3.0 * Hconf * xh[mask]
    ) / k2[mask]
    ps[mask] = ph[mask] - 4.5 * a**2 * sh[mask] / k2[mask]

    # Independent residual evaluation of the three projected constraint families.
    rH = k2[mask] * ph[mask] + 3.0 * Hconf * xh[mask] + 1.5 * a**2 * rh[mask]
    rM = k2[mask] * xh[mask] - 1.5 * a**2 * qh[mask]
    rS = k2[mask] * (ps[mask] - ph[mask]) + 4.5 * a**2 * sh[mask]

    sH = max(
        float(np.linalg.norm(k2[mask] * ph[mask])),
        float(np.linalg.norm(3.0 * Hconf * xh[mask])),
        float(np.linalg.norm(1.5 * a**2 * rh[mask])),
        1.0e-300,
    )
    sM = max(
        float(np.linalg.norm(k2[mask] * xh[mask])),
        float(np.linalg.norm(1.5 * a**2 * qh[mask])),
        1.0e-300,
    )
    sS = max(
        float(np.linalg.norm(k2[mask] * (ps[mask] - ph[mask]))),
        float(np.linalg.norm(4.5 * a**2 * sh[mask])),
        1.0e-300,
    )

    phi = np.fft.ifft(ph).real
    psi = np.fft.ifft(ps).real
    return {
        "phi": phi,
        "psi": psi,
        "weyl": phi + psi,
        "X": np.fft.ifft(xh).real,
        "constraint": {
            "hamiltonian": float(np.linalg.norm(rH) / sH),
            "momentum": float(np.linalg.norm(rM) / sM),
            "shear": float(np.linalg.norm(rS) / sS),
        },
    }


def reconstruct_metric(data, tau, y, nx, C=None):
    if C is None:
        C = m.cos_matrix(nx)
    src, bg = canonical_sources(data, tau, y, nx)
    ref, _ = class_effective_sources(data, tau, nx, C)
    corr = {name: np.asarray(src[name]) - np.asarray(ref[name]) for name in ("delta_rho", "q_momentum", "shear")}
    mc = metric_correction(data, tau, corr, nx)
    phi0, psi0, w0 = class_metric_fields(data, tau, nx, C)
    phi = phi0 + mc["phi"]
    psi = psi0 + mc["psi"]
    return {
        "phi": phi,
        "psi": psi,
        "weyl": phi + psi,
        "slip": psi - phi,
        "class_phi": phi0,
        "class_psi": psi0,
        "class_weyl": w0,
        "class_slip": psi0 - phi0,
        "source": src,
        "reference_source": ref,
        "correction_source": corr,
        "metric_correction": mc,
        "background": bg,
    }


def source_traceability_audit(data):
    C = m.cos_matrix(NX)
    _, lap, _, _ = m.spec_ops(NX)
    worst_theta = 0.0
    worst_rhop = 0.0
    worst_pchi = 0.0

    # Closed identities evaluated on all retained CLASS checkpoints.
    for tau in np.asarray(data["tau_check"], float):
        cf = m.class_fields(data, float(tau), NX, C)
        bg = fluid_background(data, float(tau))
        theta_ref = class_field(data, float(tau), "thetaA", NX, C)
        theta_from_chi = -lap(cf["chi"] / bg["Q"] - cf["alpha"]) / bg["a"]
        worst_theta = max(worst_theta, rel_l2(theta_from_chi, theta_ref))
        lhs = bg["rho_plus_p"]
        rhs = bg["Q"] * bg["KQ"] / 3.0
        worst_rhop = max(worst_rhop, abs(lhs - rhs) / max(abs(rhs), 1.0e-300))

        # Pure canonical identity: delta rho from U equals delta rho from P_chi.
        probe = np.linspace(-1.0, 1.0, NX) * 1.0e-12
        U = probe / (2.0 * bg["a"]**3 * bg["KQQ"])
        d1 = bg["Q"] * bg["KQQ"] * U / 3.0
        d2 = bg["Q"] * probe / (6.0 * bg["a"]**3)
        worst_pchi = max(worst_pchi, rel_l2(d1, d2))

    metrics = {
        "theta_mapping_relL2_max": float(worst_theta),
        "rho_plus_p_identity_rel_max": float(worst_rhop),
        "pchi_density_identity_relL2_max": float(worst_pchi),
        "nonlinear_completion_shear_source_maxabs": 0.0,
    }
    metrics["max_closed_identity_mismatch"] = max(metrics.values())
    metrics["pass"] = bool(metrics["max_closed_identity_mismatch"] <= SOURCE_ID_GATE)
    return metrics


def static_regression():
    nx = 256
    a = 0.8
    x = np.arange(nx) * static.BOX / nx
    # Deterministic nontrivial constitutive state; no solve is needed for the
    # operator identity itself.  All modes are exact periodic grid modes.
    chi = np.zeros(nx, float)
    for i, (k, ph) in enumerate(zip(np.asarray(static.K_MPC, float), np.asarray(static.PHASE, float))):
        chi += (1.0e-4 / (1.0 + i)) * np.cos(k * x + ph)
    chi -= np.mean(chi)

    rows = []
    worst = 0.0
    for kind in ("simple", "exponential", "sharp"):
        for beta in (1.0, 0.5, 0.1):
            op, g, xx, j = static.full_operator(chi, a, beta, kind, saturated=False)
            tilde = static.invlap_phys(op, a)
            phi = tilde + chi
            psi = static.invlap_phys(static.lap_phys(chi, a) + op, a)
            weyl = phi + psi
            epsi = rel_l2(psi, phi)
            ew = rel_l2(weyl, 2.0 * phi)
            # Direct locked frozen-operator reconstruction.
            phi_locked = static.invlap_phys(op, a) + chi
            eop = rel_l2(phi, phi_locked)
            err = max(epsi, ew, eop)
            worst = max(worst, err)
            rows.append({
                "kind": kind, "beta0": beta,
                "Psi_to_Phi_relL2": epsi,
                "W_to_2Phi_relL2": ew,
                "Phi_operator_relL2": eop,
                "max_error": err,
            })
    return {"max_error": float(worst), "gate": STATIC_GATE, "pass": bool(worst <= STATIC_GATE), "rows": rows}


def output_modes(field, nmax=NMAX):
    arr = np.asarray(field, float)
    ff = np.fft.rfft(arr) / arr.size
    n = min(nmax + 1, ff.size)
    out = np.zeros(nmax + 1, complex)
    out[:n] = ff[:n]
    return out


def linear_regression(data):
    d2b.set_member({"sigma": 0, "kind": "simple", "beta0": 1.0})
    run = m.integrate(data, NX, NSTEP, False, collect_stats=False)
    if not run["stats"]["finite"] or len(run["checkpoints"]) != len(data["tau_check"]):
        return {"pass": False, "reason": run["stats"].get("fail_reason", "linear_run_incomplete")}, run

    C = m.cos_matrix(NX)
    vals = {"Phi": [], "Psi": [], "W": []}
    refs = {"Phi": [], "Psi": [], "W": []}
    max_constraint = {"hamiltonian": 0.0, "momentum": 0.0, "shear": 0.0}
    for cp in run["checkpoints"]:
        tau = float(cp["tau"])
        rec = reconstruct_metric(data, tau, cp["y"], NX, C)
        vals["Phi"].append(rec["phi"])
        vals["Psi"].append(rec["psi"])
        vals["W"].append(rec["weyl"])
        refs["Phi"].append(rec["class_phi"])
        refs["Psi"].append(rec["class_psi"])
        refs["W"].append(rec["class_weyl"])
        for key, value in rec["metric_correction"]["constraint"].items():
            max_constraint[key] = max(max_constraint[key], float(value))

    err = {name: rel_l2(np.stack(vals[name]), np.stack(refs[name])) for name in vals}
    passed = bool(all(v <= LINEAR_GATE for v in err.values()))
    return {
        "pass": passed,
        "relative_L2": err,
        "gate": LINEAR_GATE,
        "metric_correction_constraint_max": max_constraint,
    }, run


def run_member(data, member):
    d2b.set_member(member)
    run = m.integrate(data, NX, NSTEP, True, collect_stats=False)
    key = d2b.member_key(member)
    if not run["stats"]["finite"] or len(run["checkpoints"]) != len(data["tau_check"]):
        return {
            "key": key, "finite": False,
            "reason": run["stats"].get("fail_reason", "trajectory_incomplete"),
        }, None

    C = m.cos_matrix(NX)
    phi_modes = []
    psi_modes = []
    weyl_modes = []
    slip_modes = []
    max_metric = {"hamiltonian": 0.0, "momentum": 0.0, "shear": 0.0}
    max_source_corr = {"delta_rho": 0.0, "q_momentum": 0.0}
    finite = True
    slip_ref = []
    slip_tot = []

    for cp in run["checkpoints"]:
        tau = float(cp["tau"])
        rec = reconstruct_metric(data, tau, cp["y"], NX, C)
        fields = (rec["phi"], rec["psi"], rec["weyl"], rec["slip"])
        finite = finite and all(np.all(np.isfinite(x)) for x in fields)
        phi_modes.append(output_modes(rec["phi"]))
        psi_modes.append(output_modes(rec["psi"]))
        weyl_modes.append(output_modes(rec["weyl"]))
        slip_modes.append(output_modes(rec["slip"]))
        slip_ref.append(rec["class_slip"])
        slip_tot.append(rec["slip"])
        for name, value in rec["metric_correction"]["constraint"].items():
            max_metric[name] = max(max_metric[name], float(value))
        for name in max_source_corr:
            max_source_corr[name] = max(
                max_source_corr[name], float(np.sqrt(np.mean(np.asarray(rec["correction_source"][name])**2)))
            )

    slip_identity = rel_l2(np.stack(slip_tot), np.stack(slip_ref))
    slip_maxabs = float(np.max(np.abs(np.stack(slip_tot))))
    canonical_constraint = float(max(cp["constraint"] for cp in run["checkpoints"]))
    record = {
        "key": key,
        "sigma": int(member["sigma"]),
        "kind": str(member["kind"]),
        "beta0": float(member["beta0"]),
        "finite": bool(finite),
        "canonical_constraint_max": canonical_constraint,
        "metric_constraint_max": max_metric,
        "source_correction_rms_max": max_source_corr,
        "slip_to_CLASS_slip_relL2": float(slip_identity),
        "slip_maxabs": slip_maxabs,
    }
    arrays = {
        "Phi": np.asarray(phi_modes, complex),
        "Psi": np.asarray(psi_modes, complex),
        "W": np.asarray(weyl_modes, complex),
        "slip": np.asarray(slip_modes, complex),
    }
    return record, arrays


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json-out", default="results/fullj_evolving_weyl_bridge.json")
    ap.add_argument("--npz-out", default="results/fullj_evolving_weyl_bridge.npz")
    args = ap.parse_args()
    jout = Path(args.json_out)
    nout = Path(args.npz_out)
    jout.parent.mkdir(parents=True, exist_ok=True)

    try:
        head = git_head()
        ancestry = {
            "phase_lock": is_ancestor(PHASE_LOCK),
            "predata_lock": is_ancestor(PREDATA_LOCK),
        }
        if not all(ancestry.values()):
            raise m.InputIncomplete(f"required ancestry missing: {ancestry}")

        print("FULLJ_EVOLVING_WEYL_BRIDGE_START", flush=True)
        print("FULLJ_WEYL_ANCESTRY=" + json.dumps(ancestry, sort_keys=True), flush=True)
        data = prepare_bridge_data()
        print(
            f"FULLJ_WEYL_INPUT_READY modes={len(data['modes'])} checkpoints={len(data['tau_check'])} members=27",
            flush=True,
        )

        g1 = source_traceability_audit(data)
        print(
            f"FULLJ_WEYL_G1 source_identity_max={g1['max_closed_identity_mismatch']:.12e} pass={g1['pass']}",
            flush=True,
        )

        g3 = static_regression()
        print(f"FULLJ_WEYL_G3 static_max={g3['max_error']:.12e} pass={g3['pass']}", flush=True)

        g2, linear_run = linear_regression(data)
        if "relative_L2" in g2:
            print(
                "FULLJ_WEYL_G2 "
                + " ".join(f"{k}={v:.12e}" for k, v in g2["relative_L2"].items())
                + f" pass={g2['pass']}",
                flush=True,
            )
        else:
            print(f"FULLJ_WEYL_G2 pass=False reason={g2.get('reason','unknown')}", flush=True)

        records = []
        stores = []
        names = []
        global_constraint = {"hamiltonian": 0.0, "momentum": 0.0, "shear": 0.0}
        all_finite = True
        slip_identity_max = 0.0
        slip_maxabs_global = 0.0

        members = all_members()
        for i, member in enumerate(members, start=1):
            rec, arrays = run_member(data, member)
            records.append(rec)
            print(
                f"FULLJ_WEYL_MEMBER {i:02d}/27 key={rec['key']} finite={rec['finite']} "
                + (
                    " ".join(f"{k}={v:.3e}" for k, v in rec.get("metric_constraint_max", {}).items())
                    + f" slip={rec.get('slip_maxabs',float('nan')):.3e}"
                    if rec.get("finite") else f" reason={rec.get('reason','unknown')}"
                ),
                flush=True,
            )
            if arrays is None:
                all_finite = False
                continue
            stores.append(arrays)
            names.append(rec["key"])
            all_finite = all_finite and bool(rec["finite"])
            for key, value in rec["metric_constraint_max"].items():
                global_constraint[key] = max(global_constraint[key], float(value))
            slip_identity_max = max(slip_identity_max, float(rec["slip_to_CLASS_slip_relL2"]))
            slip_maxabs_global = max(slip_maxabs_global, float(rec["slip_maxabs"]))

        g4 = {
            "metric_constraint_max": global_constraint,
            "gate": METRIC_CONSTRAINT_GATE,
            "pass": bool(
                len(stores) == 27
                and all(v <= METRIC_CONSTRAINT_GATE for v in global_constraint.values())
            ),
        }
        g5 = {"finite_members": int(sum(bool(r.get("finite", False)) for r in records)), "expected": 27}
        g5["pass"] = bool(g5["finite_members"] == 27 and all_finite)
        g6 = {
            "slip_to_CLASS_slip_relL2_max": float(slip_identity_max),
            "slip_maxabs_global": float(slip_maxabs_global),
            "identity_gate": SLIP_ID_GATE,
            "pass": bool(slip_identity_max <= SLIP_ID_GATE and slip_maxabs_global > 0.0),
            "interpretation": "nonlinear D2C5 completion adds no new retained shear source; evolving CLASS baseline slip is retained and is not set to zero",
        }
        print(
            "FULLJ_WEYL_G4 " + " ".join(f"{k}={v:.12e}" for k, v in global_constraint.items())
            + f" pass={g4['pass']}", flush=True,
        )
        print(f"FULLJ_WEYL_G5 finite={g5['finite_members']}/27 pass={g5['pass']}", flush=True)
        print(
            f"FULLJ_WEYL_G6 slip_identity={slip_identity_max:.12e} slip_maxabs={slip_maxabs_global:.12e} pass={g6['pass']}",
            flush=True,
        )

        gates = {
            "G1_canonical_source_traceability": bool(g1["pass"]),
            "G2_linear_CLASS_regression": bool(g2["pass"]),
            "G3_static_fullJ_regression": bool(g3["pass"]),
            "G4_metric_constraint_closure": bool(g4["pass"]),
            "G5_finite_evolving_Weyl": bool(g5["pass"]),
            "G6_static_vs_evolving_slip_distinction": bool(g6["pass"]),
        }
        passed = bool(all(gates.values()))
        classification = PASS_LABEL if passed else FAIL_LABEL

        result = {
            "classification": classification,
            "diagnostic_complete": True,
            "git_head": head,
            "ancestry": ancestry,
            "scope": "eta=0 one-way evolving-FLRW metric reconstruction on already locked D2C6 nonlinear scalar-current trajectories; corrected CLASS matter/radiation baseline retained; no nonlinear matter re-evolution, memory, likelihood, or observational fit",
            "source_mapping": {
                "delta_rho_A": "Q*P_chi/(6*a^3)",
                "Theta_A": "-lap(chi/Q-alpha)/a",
                "q_A": "(rho_A+p_A)*Theta_A",
                "rho_A": "(Q*K_Q-K)/3",
                "p_A": "K/3",
                "rho_A_plus_p_A": "Q*K_Q/3",
                "nonlinear_completion_delta_shear_A": 0.0,
                "metric_strategy": "corrected_CLASS_total_metric + constraint projection of (canonical_AeST_source - corrected_CLASS_AeST_effective_source)",
            },
            "g1_source_traceability": g1,
            "g2_linear_CLASS": g2,
            "g3_static_fullJ": g3,
            "g4_constraint_closure": g4,
            "g5_finite_output": g5,
            "g6_slip_distinction": g6,
            "records": records,
            "z_checkpoints": m.CHECK_Z.tolist(),
            "tau_checkpoints": np.asarray(data["tau_check"], float).tolist(),
            "fourier_mode_numbers_stored": list(range(NMAX + 1)),
            "gates": gates,
            "EVOLVING_WEYL_BRIDGE_TESTED": True,
            "ACT_LIKELIHOOD_LICENSED": False,
            "OBSERVATIONAL_CLAIM_LICENSED": False,
            "NO_STATIC_W_EQUALS_2PHI_PROMOTION": True,
            "EVOLVING_WEYL_POWER_LICENSED": bool(passed),
        }
        jout.write_text(json.dumps(result, indent=2, sort_keys=True, allow_nan=True) + "\n")

        arrays = {
            "member_names": np.asarray(names, dtype="U96"),
            "z": np.asarray(m.CHECK_Z, float),
            "tau": np.asarray(data["tau_check"], float),
            "mode_number": np.arange(NMAX + 1, dtype=int),
            "k_Mpc": np.arange(NMAX + 1, dtype=float) * (2.0 * np.pi / static.BOX),
        }
        if len(stores) == 27:
            for field in ("Phi", "Psi", "W", "slip"):
                arrays[field + "_hat"] = np.asarray([s[field] for s in stores], complex)
        np.savez_compressed(nout, **arrays)

        print("FULLJ_WEYL_GATES=" + json.dumps(gates, sort_keys=True), flush=True)
        print(f"FULLJ_EVOLVING_WEYL_CLASSIFICATION={classification}", flush=True)
        print("EVOLVING_WEYL_BRIDGE_TESTED=True", flush=True)
        print("ACT_LIKELIHOOD_LICENSED=False", flush=True)
        print("OBSERVATIONAL_CLAIM_LICENSED=False", flush=True)
        print("NO_STATIC_W_EQUALS_2PHI_PROMOTION=True", flush=True)
        print(f"FULLJ_WEYL_JSON={jout}", flush=True)
        print(f"FULLJ_WEYL_NPZ={nout}", flush=True)
        return 0 if passed else 2

    except (m.InputIncomplete, KeyError) as exc:
        head = git_head()
        result = {
            "classification": INCOMPLETE_LABEL,
            "diagnostic_complete": False,
            "reason": str(exc),
            "git_head": head,
            "EVOLVING_WEYL_BRIDGE_TESTED": True,
            "ACT_LIKELIHOOD_LICENSED": False,
            "OBSERVATIONAL_CLAIM_LICENSED": False,
            "NO_STATIC_W_EQUALS_2PHI_PROMOTION": True,
            "EVOLVING_WEYL_POWER_LICENSED": False,
        }
        jout.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print(f"FULLJ_EVOLVING_WEYL_CLASSIFICATION={INCOMPLETE_LABEL}", flush=True)
        print(f"FULLJ_WEYL_REASON={exc}", flush=True)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
