#!/usr/bin/env python3
from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path
import subprocess
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from nl1c6d2c6f_r2 import vector_phase_direct_source as r2

f = r2.f
d = r2.d
m = r2.m
d2b = r2.d2b
r1b = r2.r1b

R2_PREREG = "42ba09db9f14f82f32034af0ae46e785d0d62666"
R2_IMPLEMENTATION = "d74f152944c9409580ff46cc4c4f9bc934d8942c"
R2_RESULT = "da6d3691829f465006b69fd9b39a48b9ac449607"
PREREG_HEAD = "43b8e2dc9150f03f77a5b724ce14d4d96ab99489"

ETA_TRAJECTORY = 0.0
PRIMARY_ORDER = 256
CONTROL_ORDER = 512
NX = 128
NSTEP = 4096
NMAX = 32
CONSTRAINT_GATE = 1.0e-10
ENERGY_GATE = 1.0e-12
ZERO_GATE = 1.0e-12
BATH_GATE = 1.0e-2

PASS_LABEL = "NL1C6D2C6G_ETA0_DIRECT_METRIC_TANGENT_CALIBRATION_PASS"
FAIL_LABEL = "NL1C6D2C6G_ETA0_DIRECT_METRIC_TANGENT_CALIBRATION_FAIL"
INCOMPLETE_LABEL = "NL1C6D2C6G_ETA0_DIRECT_METRIC_TANGENT_CALIBRATION_INCOMPLETE"


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


def unit_metric_sources(data, tau, full_chi, z, zp, ops, eta, order):
    # D2C6G evolves the physical trajectory at eta=0 but stores the exact
    # coefficient dS_mem/deta|0 by evaluating the explicit R2 stress prefactor
    # at unit eta on the same eta=0 state.
    return r2.corrected_metric_sources(
        data, tau, full_chi, z, zp, ops, 1.0, order
    )


def baseline_psi(data, tau, nx):
    C = m.cos_matrix(nx)
    vals = m.mode_values(data, tau, "psi")
    return m.to_field(vals, C)


def metric_fields(data, tau, src, nx):
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
    return phi, psi, phi + psi


def lowband_signature(field):
    arr = np.asarray(field, float)
    ff = np.fft.rfft(arr, axis=-1) / float(arr.shape[-1])
    return ff[..., : min(NMAX + 1, ff.shape[-1])].reshape(-1)


def metric_tangent_signature(data, run):
    phis = []
    psis = []
    weyls = []
    for i, tau in enumerate(np.asarray(data["tau_check"], float)):
        src = {name: run["sources"][name][i] for name in run["sources"]}
        phi, psi, weyl = metric_fields(data, float(tau), src, NX)
        phis.append(phi)
        psis.append(psi)
        weyls.append(weyl)
    return {
        "Phi_hat": lowband_signature(np.stack(phis)),
        "Psi_hat": lowband_signature(np.stack(psis)),
        "Weyl_hat": lowband_signature(np.stack(weyls)),
    }


def compare_unit_runs(data, a, b):
    out = f.compare_sources(a, b)
    sa = metric_tangent_signature(data, a)
    sb = metric_tangent_signature(data, b)
    for name in sa:
        out[name] = rel(sa[name], sb[name])
    out["state"] = rel(lowband_signature(a["states"]), lowband_signature(b["states"]))
    out["E"] = rel(lowband_signature(a["E"]), lowband_signature(b["E"]))
    return out


def run_ok(run):
    return bool(
        run["finite"]
        and run["source_finite"]
        and run["full_constraint_max"] <= CONSTRAINT_GATE
        and run["min_one_plus_j_eff"] > 0.0
        and run["energy_identity_max"] <= ENERGY_GATE
        and run["min_completed_square_energy"] >= -1.0e-14
    )


def calibration_record(data, run, key):
    rows = []
    min_eta_1pct = np.inf
    min_row = None
    for i, tau in enumerate(np.asarray(data["tau_check"], float)):
        src = {name: run["sources"][name][i] for name in run["sources"]}
        phi, psi, weyl = metric_fields(data, float(tau), src, NX)
        base = baseline_psi(data, float(tau), NX)
        base_rms = float(np.sqrt(np.mean(base * base)))
        base_max = float(np.max(np.abs(base)))
        phi_rms = float(np.sqrt(np.mean(phi * phi)))
        psi_rms = float(np.sqrt(np.mean(psi * psi)))
        weyl_rms = float(np.sqrt(np.mean(weyl * weyl)))
        phi_max = float(np.max(np.abs(phi)))
        psi_max = float(np.max(np.abs(psi)))
        weyl_max = float(np.max(np.abs(weyl)))

        if psi_rms <= 0.0 or psi_max <= 0.0 or base_rms <= 0.0:
            eta1 = eta10 = eta100 = np.inf
            ea2 = ea1 = ea0 = np.inf
        else:
            eta1 = 0.01 * base_rms / psi_rms
            eta10 = 0.10 * base_rms / psi_rms
            eta100 = base_rms / psi_rms
            ea2 = 1.0e-2 / psi_max
            ea1 = 1.0e-1 / psi_max
            ea0 = 1.0 / psi_max

        row = {
            "checkpoint_index": i,
            "z": float(m.CHECK_Z[i]),
            "psi_base_rms": base_rms,
            "psi_base_maxabs": base_max,
            "Phi_hat_rms_per_eta": phi_rms,
            "Psi_hat_rms_per_eta": psi_rms,
            "Weyl_hat_rms_per_eta": weyl_rms,
            "Phi_hat_maxabs_per_eta": phi_max,
            "Psi_hat_maxabs_per_eta": psi_max,
            "Weyl_hat_maxabs_per_eta": weyl_max,
            "eta_for_1pct_base_psi_rms": float(eta1),
            "eta_for_10pct_base_psi_rms": float(eta10),
            "eta_for_100pct_base_psi_rms": float(eta100),
            "eta_for_abs_Psi_max_1e-2": float(ea2),
            "eta_for_abs_Psi_max_1e-1": float(ea1),
            "eta_for_abs_Psi_max_1": float(ea0),
        }
        rows.append(row)
        if np.isfinite(eta1) and eta1 < min_eta_1pct:
            min_eta_1pct = float(eta1)
            min_row = dict(row)
    return {
        "key": key,
        "health_pass": run_ok(run),
        "full_constraint_max": float(run["full_constraint_max"]),
        "min_one_plus_j_eff": float(run["min_one_plus_j_eff"]),
        "energy_identity_max": float(run["energy_identity_max"]),
        "eta0_difference_state_maxabs": float(np.max(np.abs(run["states"]))),
        "eta0_difference_E_maxabs": float(np.max(np.abs(run["E"]))),
        "calibration_by_checkpoint": rows,
        "member_min_eta_1pct": float(min_eta_1pct),
        "member_limiting_checkpoint": min_row,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--json-out",
        default="results/nl1c6d2c6g_eta0_metric_tangent_calibration.json",
    )
    args = ap.parse_args()
    outpath = Path(args.json_out)
    outpath.parent.mkdir(parents=True, exist_ok=True)

    try:
        head = git_head()
        ancestry = {
            "R2_prereg": is_ancestor(R2_PREREG),
            "R2_implementation": is_ancestor(R2_IMPLEMENTATION),
            "R2_result": is_ancestor(R2_RESULT),
            "D2C6G_prereg": is_ancestor(PREREG_HEAD),
        }
        print("NL1C6D2C6G_ETA0_DIRECT_METRIC_TANGENT_START", flush=True)
        print("D2C6G_HEAD=" + head, flush=True)
        print("D2C6G_ANCESTRY=" + json.dumps(ancestry, sort_keys=True), flush=True)

        quadrature = r1b.install_direct_baths()
        data = m.prepare_class_data()
        members = all_members()
        keys = [d.member_key(x) for x in members]
        controls = sentinels()
        control_keys = [d.member_key(x) for x in controls]
        exact_coverage = len(keys) == 27 and len(set(keys)) == 27

        # Structural eta=0 source identity on deterministic fields.
        ops = m.spec_ops(NX)
        x = np.arange(NX) * m.static.BOX / NX
        chi = np.cos(2.0 * np.pi * 3.0 * x / m.static.BOX)
        z = np.zeros((PRIMARY_ORDER, NX), float)
        zp = np.zeros_like(z)
        physical_zero_src, _ = r2.corrected_metric_sources(
            data, float(data["t0"]), chi, z, zp, ops, 0.0, PRIMARY_ORDER
        )
        physical_zero_max = max(
            float(np.max(np.abs(np.asarray(v, float))))
            for v in physical_zero_src.values()
        )
        print(f"D2C6G_PHYSICAL_ETA0_SOURCE_MAX={physical_zero_max:.12e}", flush=True)

        old_metric_sources = f.metric_sources
        f.metric_sources = unit_metric_sources

        print("D2C6G_PREHISTORY direct256 eta0 begin", flush=True)
        pre256 = d.finite_prehistory(data, NX, NSTEP, 0.0, PRIMARY_ORDER)
        print("D2C6G_PREHISTORY direct256 eta0 end", flush=True)

        primary = {}
        records = []
        health_ok = True
        eta0_identity_ok = physical_zero_max <= ZERO_GATE
        baseline_ok = True
        global_cap = np.inf
        limiting = None

        for i, member in enumerate(members, start=1):
            key = d.member_key(member)
            run = f.integrate_with_sources(
                data, NX, NSTEP, member, 0.0, PRIMARY_ORDER, pre256
            )
            primary[key] = run
            rec = calibration_record(data, run, key)
            rec["index"] = i
            records.append(rec)
            health_ok = health_ok and rec["health_pass"]
            eta0_identity_ok = eta0_identity_ok and (
                rec["eta0_difference_state_maxabs"] <= ZERO_GATE
                and rec["eta0_difference_E_maxabs"] <= ZERO_GATE
            )
            for row in rec["calibration_by_checkpoint"]:
                vals = [
                    row["psi_base_rms"],
                    row["psi_base_maxabs"],
                    row["Psi_hat_rms_per_eta"],
                    row["Psi_hat_maxabs_per_eta"],
                    row["eta_for_1pct_base_psi_rms"],
                    row["eta_for_10pct_base_psi_rms"],
                    row["eta_for_100pct_base_psi_rms"],
                    row["eta_for_abs_Psi_max_1e-2"],
                    row["eta_for_abs_Psi_max_1e-1"],
                    row["eta_for_abs_Psi_max_1"],
                ]
                baseline_ok = baseline_ok and all(np.isfinite(vals)) and all(v > 0.0 for v in vals)
                eta1 = row["eta_for_1pct_base_psi_rms"]
                if np.isfinite(eta1) and eta1 < global_cap:
                    global_cap = float(eta1)
                    limiting = {"key": key, **row}
            print(
                f"D2C6G_PRIMARY {i:02d}/27 {key} health={rec['health_pass']} "
                f"dstate0={rec['eta0_difference_state_maxabs']:.3e} "
                f"dE0={rec['eta0_difference_E_maxabs']:.3e} "
                f"member_eta1pct={rec['member_min_eta_1pct']:.12e}",
                flush=True,
            )

        print("D2C6G_PREHISTORY direct512 eta0 begin", flush=True)
        pre512 = d.finite_prehistory(data, NX, NSTEP, 0.0, CONTROL_ORDER)
        print("D2C6G_PREHISTORY direct512 eta0 end", flush=True)
        control_rows = []
        bath_ok = True
        for member in controls:
            key = d.member_key(member)
            ctl = f.integrate_with_sources(
                data, NX, NSTEP, member, 0.0, CONTROL_ORDER, pre512
            )
            cmp = compare_unit_runs(data, primary[key], ctl)
            mx = max(cmp.values())
            ok = run_ok(ctl) and mx <= BATH_GATE
            bath_ok = bath_ok and ok
            control_rows.append({"key": key, "differences": cmp, "max": mx, "pass": ok})
            print(f"D2C6G_BATH {key} max={mx:.12e} pass={ok}", flush=True)

        f.metric_sources = old_metric_sources

        feedback_ladder = [
            float(global_cap / 4.0),
            float(global_cap / 2.0),
            float(global_cap),
        ] if np.isfinite(global_cap) and global_cap > 0.0 else []

        g1 = bool(
            all(ancestry.values())
            and exact_coverage
            and ETA_TRAJECTORY == 0.0
            and PRIMARY_ORDER == 256
            and CONTROL_ORDER == 512
        )
        g2 = bool(eta0_identity_ok)
        g3 = bool(health_ok)
        g4 = bool(bath_ok)
        g5 = bool(baseline_ok and np.isfinite(global_cap) and global_cap > 0.0)
        g6 = True
        gates = {
            "G1_provenance_exact27_eta0_direct256_512": g1,
            "G2_eta0_physical_source_and_trajectory_identity": g2,
            "G3_all27_eta0_health": g3,
            "G4_direct256_512_metric_tangent_convergence": g4,
            "G5_baseline_metric_calibration_finite_positive": g5,
            "G6_scope_clean": g6,
        }
        classification = PASS_LABEL if all(gates.values()) else FAIL_LABEL
        licensed = bool(all(gates.values()))

        result = {
            "classification": classification,
            "head": head,
            "ancestry": ancestry,
            "predata_commit": PREREG_HEAD,
            "trajectory_eta": ETA_TRAJECTORY,
            "primary_order": PRIMARY_ORDER,
            "control_order": CONTROL_ORDER,
            "quadrature_audit": quadrature,
            "physical_eta0_source_maxabs": physical_zero_max,
            "primary_records": records,
            "sentinel_keys": control_keys,
            "bath_metric_tangent_controls": control_rows,
            "feedback_eta_cap_1pct_base_psi_rms": None if not np.isfinite(global_cap) else float(global_cap),
            "feedback_eta_ladder_if_pass": feedback_ladder,
            "limiting_member_checkpoint": limiting,
            "gates": gates,
            "self_consistent_feedback_ladder_licensed": licensed,
            "observational_step_licensed": False,
            "interpretation": (
                "PASS calibrates the corrected direct-memory metric tangent on the certified eta=0 "
                "nonlinear trajectories. The first feedback amplitudes are fixed by predata to "
                "{cap/4, cap/2, cap}, where cap is the global eta at which the one-way Psi tangent "
                "reaches 1% of the frozen baseline CLASS Psi RMS."
            ),
        }
        outpath.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print("FEEDBACK_ETA_CAP_1PCT_BASE_PSI=" + (f"{global_cap:.12e}" if np.isfinite(global_cap) else "nan"), flush=True)
        print("FEEDBACK_ETA_LADDER=" + ",".join(f"{x:.12e}" for x in feedback_ladder), flush=True)
        print("LIMITING=" + json.dumps(limiting, sort_keys=True), flush=True)
        print("GATES=" + json.dumps(gates, sort_keys=True), flush=True)
        print("CLASSIFICATION=" + classification, flush=True)
        print("SELF_CONSISTENT_FEEDBACK_LADDER_LICENSED=" + str(licensed), flush=True)
        print("OBSERVATIONAL_STEP_LICENSED=False", flush=True)
        print("JSON=" + str(outpath), flush=True)
        print("NL1C6D2C6G_ETA0_DIRECT_METRIC_TANGENT_END", flush=True)
        raise SystemExit(0 if all(gates.values()) else 1)

    except SystemExit:
        raise
    except Exception as exc:
        try:
            f.metric_sources = r2.OLD_METRIC_SOURCES
        except Exception:
            pass
        result = {
            "classification": INCOMPLETE_LABEL,
            "error_type": type(exc).__name__,
            "error": str(exc),
            "self_consistent_feedback_ladder_licensed": False,
            "observational_step_licensed": False,
        }
        outpath.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print("CLASSIFICATION=" + INCOMPLETE_LABEL, flush=True)
        print(f"ERROR={type(exc).__name__}: {exc}", flush=True)
        print("SELF_CONSISTENT_FEEDBACK_LADDER_LICENSED=False", flush=True)
        print("OBSERVATIONAL_STEP_LICENSED=False", flush=True)
        raise SystemExit(2)


if __name__ == "__main__":
    main()
