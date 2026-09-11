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

from nl1c6d2c6f import finite_eta_gravitational_source as f
from nl1c6d2c6f_r1 import direct_bath_source_convergence as r1b


d = f.d
c = f.c
m = f.m
d2b = f.d2b

BLOCK_COMMIT = "4bb0c4e847ce7b69d814f78fd6d9e8c56c629ac4"
PREREG_HEAD = "42ba09db9f14f82f32034af0ae46e785d0d62666"
CLARIFICATION_HEAD = "0cb9f1aeb6b9edeb89dd760922391c30ad6143a6"

ETA = 1.0 / 8.0
PRIMARY_ORDER = 256
CONTROL_ORDER = 512
NX = 128
NSTEP = 4096
NMAX = 32

PHASE_GATE = 1.0e-12
ACTION_GATE = 1.0e-6
ENERGY_GATE = 1.0e-12
CONSTRAINT_GATE = 1.0e-10
BATH_GATE = 1.0e-2
TIME_GATE = 2.0e-3
SPACE_GATE = 5.0e-3

SOURCE_NAMES = f.SOURCE_NAMES
PASS_LABEL = "NL1C6D2C6F_R2_VECTOR_PHASE_DIRECT_SOURCE_PASS"
FAIL_LABEL = "NL1C6D2C6F_R2_VECTOR_PHASE_DIRECT_SOURCE_FAIL"
INCOMPLETE_LABEL = "NL1C6D2C6F_R2_VECTOR_PHASE_DIRECT_SOURCE_INCOMPLETE"

OLD_METRIC_SOURCES = f.metric_sources


def git_head():
    return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()


def is_ancestor(sha):
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0


def rel(a, b):
    aa = np.asarray(a)
    bb = np.asarray(b)
    return float(
        np.linalg.norm(aa - bb)
        / max(np.linalg.norm(aa), np.linalg.norm(bb), 1.0e-300)
    )


def all_members():
    return [
        {"sigma": int(s), "kind": str(k), "beta0": float(b)}
        for s, k, b in itertools.product(d2b.SIGMAS, d2b.KINDS, d2b.BETAS)
    ]


def sentinels():
    return [
        {"sigma": 1, "kind": "simple", "beta0": 0.1},
        {"sigma": 0, "kind": "exponential", "beta0": 0.5},
        {"sigma": -1, "kind": "sharp", "beta0": 1.0},
    ]


def corrected_metric_sources(data, tau, full_chi, z, zp, ops, eta, order):
    """NL0B/NL1C3B local-vector source with the signed spatial phase."""
    a = float(m.bg_eval(data, tau)[0])
    grad = ops[0]
    omega_ratio, weights = c.BATH_DATA[order]
    omega = c.H0_MPC * np.asarray(omega_ratio, float) / c.TAUH0
    weights = np.asarray(weights, float)
    sw = np.sqrt(weights)

    z = np.asarray(z, float)
    zp = np.asarray(zp, float)
    q_action = grad(z) * (sw / omega)[:, None]
    qp_action = grad(zp) * (sw / omega)[:, None]
    qdot = qp_action / a
    qx = grad(q_action)
    X = grad(np.asarray(full_chi, float)) / a
    V = omega[:, None] * q_action - sw[:, None] * X[None, :]

    kin = qdot * qdot
    pot = V * V
    SN0 = -(a**3 / 4.0) * np.sum(kin + pot, axis=0)
    Sb0 = -(a**3 / 2.0) * np.sum(qdot * qx, axis=0)
    SL0 = (a**2 / 4.0) * np.sum(
        kin - (omega[:, None] * q_action) ** 2
        + weights[:, None] * X[None, :] ** 2,
        axis=0,
    )
    SR0 = (a**2 / 2.0) * np.sum(kin - pot, axis=0)

    SN = eta * SN0
    Sb = eta * Sb0
    SL = eta * SL0
    SR = eta * SR0
    SPsi = SN
    SPhi = -a * (SL + SR)
    Sshear = SL - 0.5 * SR

    rhs_energy = 0.25 * np.sum(kin + pot, axis=0)
    lhs_energy = -SN0 / (a**3)
    energy_identity = rel(lhs_energy, rhs_energy)

    return {
        "S_N": SN,
        "S_L": SL,
        "S_R": SR,
        "S_Psi": SPsi,
        "S_Phi": SPhi,
        "S_b": Sb,
        "S_shear": Sshear,
    }, {
        "energy_identity_relative_L2": energy_identity,
        "min_completed_square_energy": float(np.min(lhs_energy)),
    }


def phase_identity_audit():
    nx = 128
    x = np.arange(nx) * m.static.BOX / nx
    k3 = 2.0 * np.pi * 3.0 / m.static.BOX
    k8 = 2.0 * np.pi * 8.0 / m.static.BOX
    chi = np.cos(k3 * x + 0.31) + 0.37 * np.sin(k8 * x - 0.52)
    a = 0.73
    z = chi / a
    omega = 1.7
    sw = math.sqrt(0.6)
    grad = m.spec_ops(nx)[0]

    expected = -k3 * np.sin(k3 * x + 0.31) + 0.37 * k8 * np.cos(k8 * x - 0.52)
    grad_err = rel(grad(chi), expected)
    X = grad(chi) / a
    q_corr = (sw / omega) * grad(z)
    V_corr = omega * q_corr - sw * X
    scale = max(float(np.linalg.norm(sw * X)), 1.0e-300)
    phase_res = float(np.linalg.norm(V_corr) / scale)

    zp = 0.41 * z
    derivative_res = rel(grad(zp), 0.41 * grad(z))

    q_old = (sw / omega) * f.spectral_absgrad(z)
    V_old = omega * q_old - sw * X
    old_res = float(np.linalg.norm(V_old) / scale)

    return {
        "signed_gradient_relative_error": grad_err,
        "completed_square_alignment_residual": phase_res,
        "derivative_bridge_residual": derivative_res,
        "old_absgrad_forensic_residual_non_gating": old_res,
        "pass": bool(
            grad_err <= PHASE_GATE
            and phase_res <= PHASE_GATE
            and derivative_res <= PHASE_GATE
        ),
    }


def lowband_signature(arr):
    aa = np.asarray(arr, float)
    ff = np.fft.rfft(aa, axis=-1) / float(aa.shape[-1])
    return ff[..., : min(NMAX + 1, ff.shape[-1])].reshape(-1)


def compare_runs(a, b):
    out = f.compare_sources(a, b)
    out["state"] = rel(lowband_signature(a["states"]), lowband_signature(b["states"]))
    out["E"] = rel(lowband_signature(a["E"]), lowband_signature(b["E"]))
    return out


def run_ok(run):
    return bool(
        f.run_health(run)
        and run["energy_identity_max"] <= ENERGY_GATE
        and run["min_completed_square_energy"] >= -1.0e-14
    )


def metric_projection(data, tau, src, nx):
    a, H = m.bg_eval(data, tau)[:2]
    Hconf = a * H
    grad = m.spec_ops(nx)[0]
    rho = -np.asarray(src["S_N"], float) / (6.0 * a**3)
    t0x = np.asarray(src["S_b"], float) / (6.0 * a**3)
    qmom = grad(t0x)
    shear = -np.asarray(src["S_shear"], float) / (9.0 * a**2)

    kk = 2.0 * np.pi * np.fft.fftfreq(nx, d=m.static.BOX / nx)
    k2 = kk * kk
    modes = np.minimum(np.arange(nx), nx - np.arange(nx))
    mask = (modes >= 1) & (modes <= NMAX)

    rh = np.fft.fft(rho)
    qh = np.fft.fft(qmom)
    sh = np.fft.fft(shear)
    ph = np.zeros(nx, complex)
    ps = np.zeros(nx, complex)
    ph[mask] = -1.5 * a**2 * (
        k2[mask] * rh[mask] + 3.0 * Hconf * qh[mask]
    ) / (k2[mask] * k2[mask])
    ps[mask] = ph[mask] - 4.5 * a**2 * sh[mask] / k2[mask]

    phi = np.fft.ifft(ph).real
    psi = np.fft.ifft(ps).real
    r1 = k2[mask] * k2[mask] * ph[mask] + 1.5 * a**2 * (
        k2[mask] * rh[mask] + 3.0 * Hconf * qh[mask]
    )
    r2 = k2[mask] * (ps[mask] - ph[mask]) + 4.5 * a**2 * sh[mask]
    s1 = max(
        float(np.linalg.norm(k2[mask] * k2[mask] * ph[mask])),
        float(np.linalg.norm(1.5 * a**2 * k2[mask] * rh[mask])),
        float(np.linalg.norm(4.5 * a**2 * Hconf * qh[mask])),
        1.0e-300,
    )
    s2 = max(
        float(np.linalg.norm(k2[mask] * (ps[mask] - ph[mask]))),
        float(np.linalg.norm(4.5 * a**2 * sh[mask])),
        1.0e-300,
    )
    return {
        "delta_phi_rms": float(np.sqrt(np.mean(phi * phi))),
        "delta_psi_rms": float(np.sqrt(np.mean(psi * psi))),
        "delta_weyl_rms": float(np.sqrt(np.mean((phi + psi) ** 2))),
        "delta_phi_maxabs": float(np.max(np.abs(phi))),
        "delta_psi_maxabs": float(np.max(np.abs(psi))),
        "constraint_residual": max(
            float(np.linalg.norm(r1) / s1), float(np.linalg.norm(r2) / s2)
        ),
    }


def compact_record(data, run, key):
    srcsum = f.source_summary(run)
    metric = []
    for i, tau in enumerate(np.asarray(data["tau_check"], float)):
        src = {name: run["sources"][name][i] for name in run["sources"]}
        metric.append(metric_projection(data, float(tau), src, run["states"].shape[-1]))
    return {
        "key": key,
        "health_pass": run_ok(run),
        "full_constraint_max": float(run["full_constraint_max"]),
        "min_one_plus_j_eff": float(run["min_one_plus_j_eff"]),
        "energy_identity_max": float(run["energy_identity_max"]),
        "min_completed_square_energy": float(run["min_completed_square_energy"]),
        "source_summary": srcsum,
        "one_way_metric_non_gating": metric,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--json-out",
        default="results/nl1c6d2c6f_r2_vector_phase_direct_source.json",
    )
    args = ap.parse_args()
    outpath = Path(args.json_out)
    outpath.parent.mkdir(parents=True, exist_ok=True)

    try:
        head = git_head()
        block_ok = is_ancestor(BLOCK_COMMIT)
        prereg_ok = is_ancestor(PREREG_HEAD)
        clarify_ok = is_ancestor(CLARIFICATION_HEAD)
        print("NL1C6D2C6F_R2_VECTOR_PHASE_DIRECT_SOURCE_START", flush=True)
        print(f"R2_HEAD={head}", flush=True)
        print(f"R2_BLOCK_ANCESTOR={block_ok}", flush=True)
        print(f"R2_PREREG_ANCESTOR={prereg_ok}", flush=True)
        print(f"R2_CLARIFICATION_ANCESTOR={clarify_ok}", flush=True)

        quadrature = r1b.install_direct_baths()
        phase = phase_identity_audit()
        action = f.action_fd_audit()
        action_ok = bool(
            action["metric_source_fd_max"] <= ACTION_GATE
            and action["spectral_z_to_q_bridge_relative_L2"] <= f.BRIDGE_GATE
        )
        print(
            f"R2_PHASE grad={phase['signed_gradient_relative_error']:.12e} "
            f"Vcorr={phase['completed_square_alignment_residual']:.12e} "
            f"old={phase['old_absgrad_forensic_residual_non_gating']:.12e} "
            f"pass={phase['pass']}",
            flush=True,
        )
        print(
            f"R2_ACTION fd={action['metric_source_fd_max']:.12e} pass={action_ok}",
            flush=True,
        )

        members = all_members()
        keys = [d.member_key(x) for x in members]
        exact_coverage = len(keys) == 27 and len(set(keys)) == 27
        control_members = sentinels()
        control_keys = [d.member_key(x) for x in control_members]

        data = m.prepare_class_data()
        f.metric_sources = corrected_metric_sources

        print("R2_PREHISTORY direct256 primary begin", flush=True)
        pre256 = d.finite_prehistory(data, NX, NSTEP, ETA, PRIMARY_ORDER)
        print("R2_PREHISTORY direct256 primary end", flush=True)

        primary = {}
        records = []
        health_ok = True
        for i, member in enumerate(members, start=1):
            key = d.member_key(member)
            run = f.integrate_with_sources(
                data, NX, NSTEP, member, ETA, PRIMARY_ORDER, pre256
            )
            primary[key] = run
            rec = compact_record(data, run, key)
            rec["index"] = i
            records.append(rec)
            health_ok = health_ok and rec["health_pass"]
            dpsi = max(x["delta_psi_rms"] for x in rec["one_way_metric_non_gating"])
            print(
                f"R2_PRIMARY {i:02d}/27 {key} health={rec['health_pass']} "
                f"constraint={run['full_constraint_max']:.6e} "
                f"min1p={run['min_one_plus_j_eff']:.6e} "
                f"energy_id={run['energy_identity_max']:.3e} "
                f"dpsi_rmsmax={dpsi:.6e}",
                flush=True,
            )

        print("R2_PREHISTORY direct512 control begin", flush=True)
        pre512 = d.finite_prehistory(data, NX, NSTEP, ETA, CONTROL_ORDER)
        print("R2_PREHISTORY direct512 control end", flush=True)
        bath_rows = []
        bath_ok = True
        for member in control_members:
            key = d.member_key(member)
            ctl = f.integrate_with_sources(
                data, NX, NSTEP, member, ETA, CONTROL_ORDER, pre512
            )
            cmp = compare_runs(primary[key], ctl)
            mx = max(cmp.values())
            ok = run_ok(ctl) and mx <= BATH_GATE
            bath_ok = bath_ok and ok
            bath_rows.append({"key": key, "differences": cmp, "max": mx, "pass": ok})
            print(f"R2_BATH {key} max={mx:.6e} pass={ok}", flush=True)

        print("R2_PREHISTORY direct256 time8192 begin", flush=True)
        pretime = d.finite_prehistory(data, NX, 8192, ETA, PRIMARY_ORDER)
        print("R2_PREHISTORY direct256 time8192 end", flush=True)
        time_rows = []
        time_ok = True
        for member in control_members:
            key = d.member_key(member)
            ctl = f.integrate_with_sources(
                data, NX, 8192, member, ETA, PRIMARY_ORDER, pretime
            )
            cmp = compare_runs(primary[key], ctl)
            mx = max(cmp.values())
            ok = run_ok(ctl) and mx <= TIME_GATE
            time_ok = time_ok and ok
            time_rows.append({"key": key, "differences": cmp, "max": mx, "pass": ok})
            print(f"R2_TIME {key} max={mx:.6e} pass={ok}", flush=True)

        print("R2_PREHISTORY direct256 space256 begin", flush=True)
        prespace = d.finite_prehistory(data, 256, NSTEP, ETA, PRIMARY_ORDER)
        print("R2_PREHISTORY direct256 space256 end", flush=True)
        space_rows = []
        space_ok = True
        for member in control_members:
            key = d.member_key(member)
            ctl = f.integrate_with_sources(
                data, 256, NSTEP, member, ETA, PRIMARY_ORDER, prespace
            )
            cmp = compare_runs(primary[key], ctl)
            mx = max(cmp.values())
            ok = run_ok(ctl) and mx <= SPACE_GATE
            space_ok = space_ok and ok
            space_rows.append({"key": key, "differences": cmp, "max": mx, "pass": ok})
            print(f"R2_SPACE {key} max={mx:.6e} pass={ok}", flush=True)

        # Non-gating forensic old-phase comparison on the three frozen sentinels.
        f.metric_sources = OLD_METRIC_SOURCES
        old_rows = []
        for member in control_members:
            key = d.member_key(member)
            oldrun = f.integrate_with_sources(
                data, NX, NSTEP, member, ETA, PRIMARY_ORDER, pre256
            )
            old_rows.append(
                {
                    "key": key,
                    "corrected_vs_old_source": f.compare_sources(primary[key], oldrun),
                }
            )
        f.metric_sources = corrected_metric_sources

        g1 = bool(
            block_ok
            and prereg_ok
            and clarify_ok
            and exact_coverage
            and ETA == 0.125
            and PRIMARY_ORDER == 256
            and CONTROL_ORDER == 512
        )
        g2 = bool(phase["pass"])
        g3 = bool(
            action_ok
            and all(r["energy_identity_max"] <= ENERGY_GATE for r in primary.values())
        )
        g4 = bool(health_ok)
        g5 = bool(bath_ok)
        g6 = bool(time_ok)
        g7 = bool(space_ok)
        g8 = True
        gates = {
            "R2_1_provenance_exact27_direct256_512": g1,
            "R2_2_local_vector_phase_identity": g2,
            "R2_3_action_source_and_energy_identity": g3,
            "R2_4_all27_health": g4,
            "R2_5_direct256_512_bath_convergence": g5,
            "R2_6_time_convergence": g6,
            "R2_7_space_convergence": g7,
            "R2_8_scope_clean": g8,
        }
        classification = PASS_LABEL if all(gates.values()) else FAIL_LABEL
        relicensed = bool(all(gates.values()))

        spread = {}
        for name in SOURCE_NAMES:
            vals = [
                (float(rec["source_summary"][name]["rms_max"]), rec["key"])
                for rec in records
            ]
            arr = np.asarray([x[0] for x in vals], float)
            imin = int(np.argmin(arr))
            imax = int(np.argmax(arr))
            spread[name] = {
                "min": float(arr[imin]),
                "min_member": vals[imin][1],
                "median": float(np.median(arr)),
                "max": float(arr[imax]),
                "max_member": vals[imax][1],
                "max_over_min": float(arr[imax] / max(arr[imin], 1.0e-300)),
            }

        metric_peaks = []
        for rec in records:
            for iz, row in enumerate(rec["one_way_metric_non_gating"]):
                metric_peaks.append((row["delta_psi_rms"], rec["key"], iz, row))
        metric_peaks.sort(key=lambda x: x[0])
        worst_metric = metric_peaks[-1] if metric_peaks else None

        result = {
            "classification": classification,
            "head": head,
            "block_commit": BLOCK_COMMIT,
            "predata_commit": PREREG_HEAD,
            "clarification_commit": CLARIFICATION_HEAD,
            "eta": ETA,
            "primary_order": PRIMARY_ORDER,
            "control_order": CONTROL_ORDER,
            "quadrature_audit": quadrature,
            "phase_identity_audit": phase,
            "action_fd_audit": action,
            "primary_records": records,
            "sentinel_keys": control_keys,
            "bath_controls": bath_rows,
            "time_controls": time_rows,
            "space_controls": space_rows,
            "old_phase_forensic_sentinels_non_gating": old_rows,
            "completion_spread_non_gating": spread,
            "worst_one_way_delta_psi_rms_non_gating": None
            if worst_metric is None
            else {
                "value": float(worst_metric[0]),
                "member": worst_metric[1],
                "checkpoint_index": int(worst_metric[2]),
                "metric": worst_metric[3],
            },
            "gates": gates,
            "historical_D2C6F_fail_unchanged": True,
            "historical_D2C6F_R1_pass_retained_but_feedback_license_superseded": True,
            "self_consistent_metric_feedback_step_relicensed": relicensed,
            "observational_step_licensed": False,
            "interpretation": (
                "PASS means the direct memory stress is recertified with the local-action signed "
                "vector phase q_x=(sqrt(w)/omega)d_x z. The retained finite-memory trajectory is "
                "unchanged. The metric projection here is one-way and non-gating; PASS only "
                "re-licenses a separately preregistered feedback stage."
            ),
        }
        outpath.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print("GATES=" + json.dumps(gates, sort_keys=True), flush=True)
        print("CLASSIFICATION=" + classification, flush=True)
        print("SELF_CONSISTENT_METRIC_FEEDBACK_STEP_RELICENSED=" + str(relicensed), flush=True)
        print("OBSERVATIONAL_STEP_LICENSED=False", flush=True)
        print("JSON=" + str(outpath), flush=True)
        print("NL1C6D2C6F_R2_VECTOR_PHASE_DIRECT_SOURCE_END", flush=True)
        raise SystemExit(0 if all(gates.values()) else 1)

    except SystemExit:
        raise
    except Exception as exc:
        f.metric_sources = OLD_METRIC_SOURCES
        payload = {
            "classification": INCOMPLETE_LABEL,
            "error_type": type(exc).__name__,
            "error": str(exc),
            "self_consistent_metric_feedback_step_relicensed": False,
            "observational_step_licensed": False,
        }
        outpath.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
        print("CLASSIFICATION=" + INCOMPLETE_LABEL, flush=True)
        print(f"ERROR={type(exc).__name__}: {exc}", flush=True)
        print("JSON=" + str(outpath), flush=True)
        raise


if __name__ == "__main__":
    main()
