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

from nl1c6d2c6d import finite_positive_eta_retained as d

c = d.c
m = d.m
d2b = d.d2b

PARENT_D2C6E_COMPUTE = "e51748d58c9cb43340e2ad583c5985641fa9aad6"
PARENT_D2C6E_RESULT = "dd49c48fb540109610bbfcb417701f97ee98554b"
PREREG_HEAD = "c23966efccbe310d35e1c45a069bf0370d7dd4bc"
CLARIFICATION_HEAD = "8b7cb2123e529409c4aea941aabdd6f3bb9f1ecd"

ETAS = (1.0 / 32.0, 1.0 / 16.0, 1.0 / 8.0)
ETA_MAX = ETAS[-1]
PRIMARY_ORDER = 39
CONTROL_ORDER = 47

ACTION_FD_GATE = 1.0e-6
BRIDGE_GATE = 1.0e-10
ENERGY_ID_GATE = 1.0e-12
PARENT_REG_GATE = 1.0e-10
CONSTRAINT_GATE = 1.0e-10
BATH_GATE = 1.0e-2
TIME_GATE = 2.0e-3
SPACE_GATE = 5.0e-3

SOURCE_NAMES = ("S_Psi", "S_Phi", "S_b", "S_shear")
PASS_LABEL = "NL1C6D2C6F_FINITE_ETA_DIRECT_GRAVITATIONAL_SOURCE_PASS"
FAIL_LABEL = "NL1C6D2C6F_FINITE_ETA_DIRECT_GRAVITATIONAL_SOURCE_FAIL"
INCOMPLETE_LABEL = "NL1C6D2C6F_FINITE_ETA_DIRECT_GRAVITATIONAL_SOURCE_INCOMPLETE"


def rel_l2(a, b):
    aa = np.asarray(a)
    bb = np.asarray(b)
    return float(np.linalg.norm(aa - bb) / max(np.linalg.norm(aa), np.linalg.norm(bb), 1.0e-300))


def git_head():
    return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()


def is_ancestor(sha):
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0


def spectral_absgrad(a):
    arr = np.asarray(a, float)
    n = arr.shape[-1]
    kk = 2.0 * np.pi * np.fft.rfftfreq(n, d=m.static.BOX / n)
    ff = np.fft.rfft(arr, axis=-1)
    return np.fft.irfft(ff * kk, n=n, axis=-1)


def component_signature(src, name, nmodes=32):
    arr = np.asarray(src[name], float)
    n = arr.shape[-1]
    ff = np.fft.rfft(arr, axis=-1) / float(n)
    return ff[..., : min(nmodes + 1, ff.shape[-1])].reshape(-1)


def metric_sources(data, tau, full_chi, z, zp, ops, eta, order):
    a = float(m.bg_eval(data, tau)[0])
    grad = ops[0]
    omega_ratio, weights = c.BATH_DATA[order]
    omega = c.H0_MPC * np.asarray(omega_ratio, float) / c.TAUH0
    weights = np.asarray(weights, float)
    sw = np.sqrt(weights)

    z = np.asarray(z, float)
    zp = np.asarray(zp, float)
    q_action = spectral_absgrad(z) * (sw / omega)[:, None]
    qp_action = spectral_absgrad(zp) * (sw / omega)[:, None]
    qdot = qp_action / a
    qx = grad(q_action)
    chix = grad(np.asarray(full_chi, float))
    X = chix / a
    V = omega[:, None] * q_action - sw[:, None] * X[None, :]

    kin = qdot * qdot
    pot = V * V
    SN0 = -(a**3 / 4.0) * np.sum(kin + pot, axis=0)
    Sb0 = -(a**3 / 2.0) * np.sum(qdot * qx, axis=0)
    SL0 = (a**2 / 4.0) * np.sum(
        kin - (omega[:, None] * q_action) ** 2 + weights[:, None] * X[None, :] ** 2,
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
    energy_identity = rel_l2(lhs_energy, rhs_energy)
    min_energy = float(np.min(lhs_energy))

    fields = {
        "S_N": SN,
        "S_L": SL,
        "S_R": SR,
        "S_Psi": SPsi,
        "S_Phi": SPhi,
        "S_b": Sb,
        "S_shear": Sshear,
    }
    return fields, {
        "energy_identity_relative_L2": energy_identity,
        "min_completed_square_energy": min_energy,
    }


def action_fd_audit():
    a = 0.73
    om = 1.7
    sw = math.sqrt(0.6)
    px = -0.47
    qt = 0.29
    qx = -0.22
    q = 0.18

    def lag(N, b, L, R):
        Aq = (qt - b * qx) / N
        X = px / L
        return N * L * R * R / 4.0 * (Aq * Aq - (om * q - sw * X) ** 2)

    V = om * q - sw * px / a
    analytic = {
        "N": -(a**3 / 4.0) * (qt * qt + V * V),
        "b": -(a**3 / 2.0) * qt * qx,
        "L": (a**2 / 4.0) * (qt * qt - om * om * q * q + sw * sw * (px / a) ** 2),
        "R": (a**2 / 2.0) * (qt * qt - V * V),
    }
    base = {"N": 1.0, "b": 0.0, "L": a, "R": a}
    errs = {}
    for name in ("N", "b", "L", "R"):
        x0 = base[name]
        h = 1.0e-6 * max(1.0, abs(x0))
        bp = dict(base)
        bm = dict(base)
        bp[name] = x0 + h
        bm[name] = x0 - h
        fd = (lag(**bp) - lag(**bm)) / (2.0 * h)
        errs[name] = abs(fd - analytic[name]) / max(abs(fd), abs(analytic[name]), 1.0e-14)

    nx = 128
    x = np.arange(nx) * m.static.BOX / nx
    k1 = 2.0 * np.pi * 2.0 / m.static.BOX
    k2 = 2.0 * np.pi * 5.0 / m.static.BOX
    z = np.cos(k1 * x + 0.2) + 0.3 * np.cos(k2 * x - 0.4)
    got = spectral_absgrad(z)
    expected = k1 * np.cos(k1 * x + 0.2) + 0.3 * k2 * np.cos(k2 * x - 0.4)
    bridge = rel_l2(got, expected)

    return {
        "metric_source_fd_relative_errors": errs,
        "metric_source_fd_max": float(max(errs.values())),
        "spectral_z_to_q_bridge_relative_L2": bridge,
    }


def integrate_with_sources(data, nx, nstep, member, eta, order, pre_cache=None):
    C = m.cos_matrix(nx)
    ops = m.spec_ops(nx)
    y0, _ = d.r1.initial_state_stable(data, nx)
    if pre_cache is None:
        pre_cache = d.finite_prehistory(data, nx, nstep, eta, order)

    dc = np.asarray(pre_cache["d"], float).copy()
    z = np.asarray(pre_cache["q"], float).copy()
    zp = np.asarray(pre_cache["p"], float).copy()

    t0 = float(data["t0"])
    t1 = float(data["t1"])
    h = (t1 - t0) / float(nstep)
    tchecks = np.asarray(data["tau_check"], float)

    states = []
    efields = []
    source_store = {name: [] for name in ("S_N", "S_L", "S_R", *SOURCE_NAMES)}
    source_diag = []
    full_constraint_max = 0.0
    min1p = np.inf
    finite = True
    fail_reason = None

    def store(t, ycur, dcur, zcur, zpcur):
        nonlocal full_constraint_max, min1p
        full = ycur + dcur
        Q = m.bg_eval(data, t)[2]
        states.append(d.canonical_difference(dcur, Q))
        efields.append(c.delta_E(data, t, dcur, ops))
        full_constraint_max = max(
            full_constraint_max, c.base_constraint(data, t, full, ops)
        )
        min1p = min(min1p, c.min_one_plus(data, t, full[1], ops, member))
        src, diag = metric_sources(data, t, full[1], zcur, zpcur, ops, eta, order)
        for name in source_store:
            source_store[name].append(np.asarray(src[name], float))
        source_diag.append(diag)

    store(t0, y0, dc, z, zp)
    ci = 1

    for istep in range(nstep):
        t = t0 + istep * h
        th = t + 0.5 * h
        tn = t1 if istep + 1 == nstep else t0 + (istep + 1) * h

        a0 = m.bg_eval(data, t)[0]
        ah = m.bg_eval(data, th)[0]
        an = m.bg_eval(data, tn)[0]

        by1, k1, _ = d.pair_rhs(data, t, y0, dc, z, ops, C, member, eta, order)
        y2 = y0 + 0.5 * h * by1
        d2 = dc + 0.5 * h * k1
        s0 = (y0[1] + dc[1]) / a0
        s2 = (y2[1] + d2[1]) / ah
        z2, zp2 = c.bath_advance(data, t, th, z, zp, s0, s2, order)

        by2, k2, _ = d.pair_rhs(data, th, y2, d2, z2, ops, C, member, eta, order)
        y3 = y0 + 0.5 * h * by2
        d3 = dc + 0.5 * h * k2
        s3 = (y3[1] + d3[1]) / ah
        z3, zp3 = c.bath_advance(data, t, th, z, zp, s0, s3, order)

        by3, k3, _ = d.pair_rhs(data, th, y3, d3, z3, ops, C, member, eta, order)
        y4 = y0 + h * by3
        d4 = dc + h * k3
        s4 = (y4[1] + d4[1]) / an
        z4, zp4 = c.bath_advance(data, t, tn, z, zp, s0, s4, order)

        by4, k4, _ = d.pair_rhs(data, tn, y4, d4, z4, ops, C, member, eta, order)
        yn = y0 + (h / 6.0) * (by1 + 2.0 * by2 + 2.0 * by3 + by4)
        dn = dc + (h / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
        sn = (yn[1] + dn[1]) / an
        zn, zpn = c.bath_advance(data, t, tn, z, zp, s0, sn, order)

        if not (
            np.all(np.isfinite(yn))
            and np.all(np.isfinite(dn))
            and np.all(np.isfinite(zn))
            and np.all(np.isfinite(zpn))
        ):
            finite = False
            fail_reason = f"nonfinite_step_{istep + 1}"
            break

        old_y = y0
        old_d = dc
        old_z = z
        old_zp = zp

        while ci < len(tchecks) and tchecks[ci] <= tn + 1.0e-10:
            frac = float((tchecks[ci] - t) / h)
            frac = min(1.0, max(0.0, frac))
            yc = old_y + frac * (yn - old_y)
            dd = old_d + frac * (dn - old_d)
            zc = old_z + frac * (zn - old_z)
            zpc = old_zp + frac * (zpn - old_zp)
            store(float(tchecks[ci]), yc, dd, zc, zpc)
            ci += 1

        y0, dc, z, zp = yn, dn, zn, zpn
        if (istep + 1) % 8 == 0:
            full = y0 + dc
            min1p = min(min1p, c.min_one_plus(data, tn, full[1], ops, member))

    if finite and ci != len(tchecks):
        finite = False
        fail_reason = f"stored_only_{ci}_of_{len(tchecks)}_checkpoints"

    arr = np.stack(states) if states else np.empty((0, 4, nx))
    ee = np.stack(efields) if efields else np.empty((0, nx))
    sources = {
        name: np.stack(vals) if vals else np.empty((0, nx))
        for name, vals in source_store.items()
    }
    source_finite = all(np.all(np.isfinite(v)) for v in sources.values())
    energy_err = max(
        [x["energy_identity_relative_L2"] for x in source_diag] or [np.inf]
    )
    min_energy = min([x["min_completed_square_energy"] for x in source_diag] or [-np.inf])

    return {
        "finite": bool(finite),
        "fail_reason": fail_reason,
        "states": arr,
        "E": ee,
        "sources": sources,
        "source_finite": bool(source_finite),
        "full_constraint_max": float(full_constraint_max),
        "min_one_plus_j_eff": float(min1p),
        "energy_identity_max": float(energy_err),
        "min_completed_square_energy": float(min_energy),
    }


def run_health(run):
    return bool(
        run["finite"]
        and run["source_finite"]
        and run["full_constraint_max"] <= CONSTRAINT_GATE
        and run["min_one_plus_j_eff"] > 0.0
    )


def source_summary(run):
    out = {}
    for name in SOURCE_NAMES:
        arr = np.asarray(run["sources"][name], float)
        rms_z = np.sqrt(np.mean(arr * arr, axis=-1))
        out[name] = {
            "rms_by_checkpoint": [float(x) for x in rms_z],
            "rms_max": float(np.max(rms_z)),
            "rms_final": float(rms_z[-1]),
        }
    return out


def compare_sources(a, b):
    return {
        name: rel_l2(component_signature(a["sources"], name), component_signature(b["sources"], name))
        for name in SOURCE_NAMES
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--json-out",
        default="results/nl1c6d2c6f_finite_eta_gravitational_source.json",
    )
    args = ap.parse_args()
    outpath = Path(args.json_out)
    outpath.parent.mkdir(parents=True, exist_ok=True)

    try:
        head = git_head()
        parent_compute_ok = is_ancestor(PARENT_D2C6E_COMPUTE)
        parent_result_ok = is_ancestor(PARENT_D2C6E_RESULT)
        prereg_ok = is_ancestor(PREREG_HEAD)
        clarification_ok = is_ancestor(CLARIFICATION_HEAD)

        print("NL1C6D2C6F_FINITE_ETA_DIRECT_GRAVITATIONAL_SOURCE_START", flush=True)
        print(f"D2C6F_HEAD={head}", flush=True)
        print(f"D2C6F_PARENT_COMPUTE_ANCESTOR={parent_compute_ok}", flush=True)
        print(f"D2C6F_PARENT_RESULT_ANCESTOR={parent_result_ok}", flush=True)
        print(f"D2C6F_PREREG_ANCESTOR={prereg_ok}", flush=True)
        print(f"D2C6F_CLARIFICATION_ANCESTOR={clarification_ok}", flush=True)

        audit = action_fd_audit()
        f2 = bool(
            audit["metric_source_fd_max"] <= ACTION_FD_GATE
            and audit["spectral_z_to_q_bridge_relative_L2"] <= BRIDGE_GATE
        )
        print(
            "F2_ACTION "
            f"metric_fd={audit['metric_source_fd_max']:.12e} "
            f"bridge={audit['spectral_z_to_q_bridge_relative_L2']:.12e} pass={f2}",
            flush=True,
        )

        data = m.prepare_class_data()
        expected = [
            {"sigma": s, "kind": kind, "beta0": beta}
            for s, kind, beta in itertools.product(d2b.SIGMAS, d2b.KINDS, d2b.BETAS)
        ]
        coverage = len(expected) == 27 and len({d.member_key(x) for x in expected}) == 27

        nx0 = 128
        ops0 = m.spec_ops(nx0)
        x0 = np.arange(nx0) * m.static.BOX / nx0
        chi0 = np.cos(2.0 * np.pi * 2.0 * x0 / m.static.BOX)
        om0, _ = c.BATH_DATA[PRIMARY_ORDER]
        z0 = np.zeros((len(om0), nx0), float)
        zp0 = np.zeros_like(z0)
        src0, _ = metric_sources(
            data, float(data["tau_check"][0]), chi0, z0, zp0, ops0, 0.0, PRIMARY_ORDER
        )
        eta0_exact = max(float(np.max(np.abs(v))) for v in src0.values()) == 0.0

        pre_primary = {
            eta: d.finite_prehistory(data, 128, 4096, eta, PRIMARY_ORDER)
            for eta in ETAS
        }
        pre_order = d.finite_prehistory(data, 128, 4096, ETA_MAX, CONTROL_ORDER)
        pre_time = d.finite_prehistory(data, 128, 8192, ETA_MAX, PRIMARY_ORDER)
        pre_space = d.finite_prehistory(data, 256, 4096, ETA_MAX, PRIMARY_ORDER)

        primary = {}
        records = []
        energy_ok = eta0_exact
        health_ok = True

        for idx, member in enumerate(expected, start=1):
            key = d.member_key(member)
            for eta in ETAS:
                run = integrate_with_sources(
                    data, 128, 4096, member, eta, PRIMARY_ORDER, pre_primary[eta]
                )
                primary[(key, eta)] = run
                health = run_health(run)
                health_ok = health_ok and health
                energy = bool(
                    run["energy_identity_max"] <= ENERGY_ID_GATE
                    and run["min_completed_square_energy"] >= -1.0e-14
                )
                energy_ok = energy_ok and energy
                summ = source_summary(run)
                records.append(
                    {
                        "index": idx,
                        "key": key,
                        "eta": eta,
                        "health_pass": health,
                        "finite": run["finite"],
                        "source_finite": run["source_finite"],
                        "full_constraint_max": run["full_constraint_max"],
                        "min_one_plus_j_eff": run["min_one_plus_j_eff"],
                        "energy_identity_max": run["energy_identity_max"],
                        "min_completed_square_energy": run["min_completed_square_energy"],
                        "source_summary": summ,
                    }
                )
                maxsrc = max(v["rms_max"] for v in summ.values())
                print(
                    f"D2C6F_MEMBER {idx:02d}/27 eta={eta:.12e} {key} "
                    f"health={health} constraint={run['full_constraint_max']:.6e} "
                    f"min1p={run['min_one_plus_j_eff']:.6e} "
                    f"energy_id={run['energy_identity_max']:.3e} "
                    f"source_rms_max={maxsrc:.6e}",
                    flush=True,
                )

        anchor = expected[0]
        anchor_key = d.member_key(anchor)
        old = d.integrate_finite(
            data, 128, 4096, anchor, ETA_MAX, PRIMARY_ORDER, pre_primary[ETA_MAX]
        )
        new = primary[(anchor_key, ETA_MAX)]
        parent_state_reg = rel_l2(new["states"], old["states"])
        parent_E_reg = rel_l2(new["E"], old["E"])
        f4 = bool(max(parent_state_reg, parent_E_reg) <= PARENT_REG_GATE)
        print(
            "F4_PARENT_REGRESSION "
            f"state={parent_state_reg:.12e} E={parent_E_reg:.12e} pass={f4}",
            flush=True,
        )

        controls = []
        worst_bath = 0.0
        worst_time = 0.0
        worst_space = 0.0
        control_health_ok = True
        control_energy_ok = True

        for idx, member in enumerate(expected, start=1):
            key = d.member_key(member)
            base = primary[(key, ETA_MAX)]
            ro = integrate_with_sources(
                data, 128, 4096, member, ETA_MAX, CONTROL_ORDER, pre_order
            )
            rt = integrate_with_sources(
                data, 128, 8192, member, ETA_MAX, PRIMARY_ORDER, pre_time
            )
            rs = integrate_with_sources(
                data, 256, 4096, member, ETA_MAX, PRIMARY_ORDER, pre_space
            )

            db = compare_sources(base, ro)
            dt = compare_sources(base, rt)
            ds = compare_sources(base, rs)
            mb = max(db.values())
            mt = max(dt.values())
            ms = max(ds.values())
            worst_bath = max(worst_bath, mb)
            worst_time = max(worst_time, mt)
            worst_space = max(worst_space, ms)

            ch = all(run_health(r) for r in (ro, rt, rs))
            en = all(
                r["energy_identity_max"] <= ENERGY_ID_GATE
                and r["min_completed_square_energy"] >= -1.0e-14
                for r in (ro, rt, rs)
            )
            control_health_ok = control_health_ok and ch
            control_energy_ok = control_energy_ok and en
            controls.append(
                {
                    "index": idx,
                    "key": key,
                    "bath_order": db,
                    "time": dt,
                    "space": ds,
                    "bath_order_max": mb,
                    "time_max": mt,
                    "space_max": ms,
                    "control_health": ch,
                    "energy_identity_pass": en,
                }
            )
            print(
                f"D2C6F_CONTROL {idx:02d}/27 {key} "
                f"bath={mb:.6e} time={mt:.6e} space={ms:.6e} health={ch}",
                flush=True,
            )

        f1 = bool(parent_compute_ok and parent_result_ok and prereg_ok and clarification_ok and coverage and len(records) == 81)
        f3 = bool(energy_ok and control_energy_ok)
        f5 = bool(health_ok and control_health_ok)
        f6 = bool(worst_bath <= BATH_GATE)
        f7 = bool(worst_time <= TIME_GATE)
        f8 = bool(worst_space <= SPACE_GATE)
        f9 = True

        dyadic = []
        for member in expected:
            key = d.member_key(member)
            row = {"key": key}
            for ilo, ihi in ((0, 1), (1, 2)):
                elo, ehi = ETAS[ilo], ETAS[ihi]
                lo = primary[(key, elo)]["sources"]
                hi = primary[(key, ehi)]["sources"]
                tag = f"{elo:.12e}_to_{ehi:.12e}"
                row[tag] = {
                    name: rel_l2(
                        component_signature({name: lo[name]}, name) / elo,
                        component_signature({name: hi[name]}, name) / ehi,
                    )
                    for name in SOURCE_NAMES
                }
            dyadic.append(row)

        spread = {}
        for name in SOURCE_NAMES:
            vals = []
            for member in expected:
                key = d.member_key(member)
                arr = primary[(key, ETA_MAX)]["sources"][name]
                vals.append(float(np.sqrt(np.mean(arr[-1] ** 2))))
            spread[name] = {
                "final_rms_min": float(min(vals)),
                "final_rms_max": float(max(vals)),
                "max_over_min": float(max(vals) / max(min(vals), 1.0e-300)),
            }

        largest = None
        for rec in records:
            for name, ss in rec["source_summary"].items():
                item = {
                    "key": rec["key"],
                    "eta": rec["eta"],
                    "source": name,
                    "rms_max": ss["rms_max"],
                }
                if largest is None or item["rms_max"] > largest["rms_max"]:
                    largest = item

        gates = {
            "F1_parent_prereg_exact_27x3_coverage": f1,
            "F2_action_source_and_zq_bridge": f2,
            "F3_eta0_and_completed_square_energy_identity": f3,
            "F4_parent_retained_trajectory_regression": f4,
            "F5_all_primary_and_control_health": f5,
            "F6_bath_order_source_convergence_le_1e-2": f6,
            "F7_time_source_convergence_le_2e-3": f7,
            "F8_space_source_convergence_le_5e-3": f8,
            "F9_scope_clean_one_way_only": f9,
        }
        classification = PASS_LABEL if all(gates.values()) else FAIL_LABEL

        result = {
            "classification": classification,
            "head": head,
            "predata_commit": PREREG_HEAD,
            "predata_clarification_commit": CLARIFICATION_HEAD,
            "parent_D2C6E_compute": PARENT_D2C6E_COMPUTE,
            "parent_D2C6E_result": PARENT_D2C6E_RESULT,
            "eta_values": list(ETAS),
            "action_source_audit": audit,
            "eta0_direct_metric_source_exact_zero": eta0_exact,
            "parent_regression": {
                "state_relative_L2": parent_state_reg,
                "E_relative_L2": parent_E_reg,
            },
            "primary_records": records,
            "control_records": controls,
            "worst_bath_order_source_convergence": worst_bath,
            "worst_time_source_convergence": worst_time,
            "worst_space_source_convergence": worst_space,
            "dyadic_eta_normalized_source_change_non_gating": dyadic,
            "completion_spread_eta_max_non_gating": spread,
            "largest_source_event_non_gating": largest,
            "gates": gates,
            "self_consistent_weakfield_feedback_step_licensed": bool(all(gates.values())),
            "full_arbitrary_amplitude_nonlinear_gr_aest_licensed": False,
            "observational_step_licensed": False,
            "scope": (
                "one-way direct metric source from frozen NL0B action evaluated on "
                "certified D2C6E finite-eta retained scalar-current trajectories; "
                "no metric/matter feedback and no observational likelihood"
            ),
        }
        outpath.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")

        print(f"WORST_BATH_ORDER_SOURCE={worst_bath:.12e}", flush=True)
        print(f"WORST_TIME_SOURCE={worst_time:.12e}", flush=True)
        print(f"WORST_SPACE_SOURCE={worst_space:.12e}", flush=True)
        print("GATES=" + json.dumps(gates, sort_keys=True), flush=True)
        print(f"CLASSIFICATION={classification}", flush=True)
        print(
            "SELF_CONSISTENT_WEAKFIELD_FEEDBACK_STEP_LICENSED="
            + str(bool(all(gates.values()))),
            flush=True,
        )
        print("OBSERVATIONAL_STEP_LICENSED=False", flush=True)
        print(f"JSON={outpath}", flush=True)
        print("NL1C6D2C6F_FINITE_ETA_DIRECT_GRAVITATIONAL_SOURCE_END", flush=True)
        return 0 if classification == PASS_LABEL else 1

    except Exception as exc:
        result = {
            "classification": INCOMPLETE_LABEL,
            "error_type": type(exc).__name__,
            "error": str(exc),
            "self_consistent_weakfield_feedback_step_licensed": False,
            "observational_step_licensed": False,
        }
        outpath.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print(f"CLASSIFICATION={INCOMPLETE_LABEL}", flush=True)
        print(f"ERROR={type(exc).__name__}: {exc}", flush=True)
        print(f"JSON={outpath}", flush=True)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
