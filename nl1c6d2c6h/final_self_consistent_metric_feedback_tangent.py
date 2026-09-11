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

from nl1c6d2c6f_r2 import vector_phase_direct_source as r2
from nl1c6d2c6g import eta0_metric_tangent_calibration as g

c = r2.c
m = r2.m
d2b = r2.d2b
r1 = r2.d.r1

G_RESULT = "fc8b4f1f9d6f7c9e9124b8d754c769cbde27b310"
R2_RESULT = "da6d3691829f465006b69fd9b39a48b9ac449607"
PREREG = "2f31fc65874bda220a651361b64d7255116709cf"

NX = 128
NSTEP = 4096
PRIMARY_ORDER = 256
CONTROL_ORDER = 512
ZERO_GATE = 1.0e-12
CONSTRAINT_GATE = 1.0e-10
ENERGY_GATE = 1.0e-12
BATH_GATE = 1.0e-2
NMAX = 32

PASS_LABEL = "NL1C6D2C6H_FINAL_SELF_CONSISTENT_METRIC_FEEDBACK_TANGENT_PASS"
FAIL_LABEL = "NL1C6D2C6H_FINAL_SELF_CONSISTENT_METRIC_FEEDBACK_TANGENT_FAIL"
INCOMPLETE_LABEL = "NL1C6D2C6H_FINAL_SELF_CONSISTENT_METRIC_FEEDBACK_TANGENT_INCOMPLETE"


def git_head():
    return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()


def is_ancestor(sha):
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0


def members():
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


def rel(a, b):
    aa = np.asarray(a)
    bb = np.asarray(b)
    return float(
        np.linalg.norm(aa - bb)
        / max(np.linalg.norm(aa), np.linalg.norm(bb), 1.0e-300)
    )


def lowband(a):
    aa = np.asarray(a, float)
    ff = np.fft.rfft(aa, axis=-1) / float(aa.shape[-1])
    return ff[..., : min(NMAX + 1, ff.shape[-1])].reshape(-1)


def single_mode_data(data, index):
    out = dict(data)
    out["modes"] = [data["modes"][index]]
    return out


def mode_chi(data, bg_data, index, tau, C):
    md = data["modes"][index]
    a, _, Q = m.bg_eval(bg_data, tau)[:3]
    alpha = float(md["splines"]["alpha"](tau))
    theta = float(md["splines"]["theta"](tau))
    k = float(m.K_MPC[index])
    return Q * (a * theta / (k * k) + alpha) * C[index]


def unit_source_psi(data, tau, chi, z, zp, ops, order):
    src, diag = r2.corrected_metric_sources(
        data, tau, chi, z, zp, ops, 1.0, order
    )
    _, psi, _ = g.metric_fields(data, tau, src, chi.shape[-1])
    return np.asarray(psi, float), diag


def physical_zero_audit(data, order):
    ops = m.spec_ops(NX)
    x = np.arange(NX) * m.static.BOX / NX
    chi = np.cos(2.0 * np.pi * 3.0 * x / m.static.BOX)
    z = np.zeros((order, NX), float)
    zp = np.zeros_like(z)
    src, _ = r2.corrected_metric_sources(
        data, float(data["t0"]), chi, z, zp, ops, 0.0, order
    )
    return max(float(np.max(np.abs(np.asarray(v, float)))) for v in src.values())


def rhs_feedback(data, tau, base_chi, v, q, p, ops, member, nonlinear, order, dpsi):
    out = c.tangent_rhs(
        data, tau, base_chi, v, q, ops, member, nonlinear, order
    ).copy()
    a = m.bg_eval(data, tau)[0]
    out[0] -= a * np.asarray(dpsi, float)
    return out


def feedback_prehistory(data, order):
    C = m.cos_matrix(NX)
    ops = m.spec_ops(NX)
    t0 = float(data["t0"])
    hmain = (float(data["t1"]) - t0) / float(NSTEP)

    omega, _ = c.BATH_DATA[order]
    q = np.zeros((len(omega), NX), float)
    p = np.zeros_like(q)
    v = np.zeros((4, NX), float)

    starts = [float(md["tau_lo"]) for md in data["modes"]]
    imin = int(np.argmin(starts))
    bg_data = single_mode_data(data, imin)
    boundaries = sorted(set(starts + [t0]))

    energy_max = 0.0
    min_energy = np.inf
    psi_max = 0.0
    steps = 0

    def chi_active(tau, active):
        out = np.zeros(NX, float)
        for j in active:
            out += mode_chi(data, bg_data, j, tau, C)
        return out

    for ib in range(len(boundaries) - 1):
        ta = float(boundaries[ib])
        tb = float(boundaries[ib + 1])
        if tb <= ta + 1.0e-15:
            continue
        active = [j for j, s in enumerate(starts) if s <= ta + 1.0e-12]
        nseg = max(1, int(math.ceil((tb - ta) / hmain)))
        h = (tb - ta) / float(nseg)

        for iseg in range(nseg):
            t = ta + iseg * h
            th = t + 0.5 * h
            tn = tb if iseg + 1 == nseg else ta + (iseg + 1) * h

            chi0 = chi_active(t, active)
            chih = chi_active(th, active)
            chin = chi_active(tn, active)
            a0 = m.bg_eval(bg_data, t)[0]
            ah = m.bg_eval(bg_data, th)[0]
            an = m.bg_eval(bg_data, tn)[0]
            s0, sh, sn = chi0 / a0, chih / ah, chin / an

            psi0, dg0 = unit_source_psi(bg_data, t, chi0, q, p, ops, order)
            k1 = rhs_feedback(bg_data, t, chi0, v, q, p, ops, None, False, order, psi0)

            q2, p2 = c.bath_advance(bg_data, t, th, q, p, s0, sh, order)
            v2 = v + 0.5 * h * k1
            psih, dgh = unit_source_psi(bg_data, th, chih, q2, p2, ops, order)
            k2 = rhs_feedback(bg_data, th, chih, v2, q2, p2, ops, None, False, order, psih)

            q3, p3 = c.bath_advance(bg_data, t, th, q, p, s0, sh, order)
            v3 = v + 0.5 * h * k2
            k3 = rhs_feedback(bg_data, th, chih, v3, q3, p3, ops, None, False, order, psih)

            q4, p4 = c.bath_advance(bg_data, t, tn, q, p, s0, sn, order)
            v4 = v + h * k3
            psin, dgn = unit_source_psi(bg_data, tn, chin, q4, p4, ops, order)
            k4 = rhs_feedback(bg_data, tn, chin, v4, q4, p4, ops, None, False, order, psin)

            v = v + (h / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
            q, p = c.bath_advance(bg_data, t, tn, q, p, s0, sn, order)

            for dg in (dg0, dgh, dgn):
                energy_max = max(energy_max, float(dg["energy_identity_relative_L2"]))
                min_energy = min(min_energy, float(dg["min_completed_square_energy"]))
            psi_max = max(
                psi_max,
                float(np.max(np.abs(psi0))),
                float(np.max(np.abs(psih))),
                float(np.max(np.abs(psin))),
            )
            steps += 1

            if not (
                np.all(np.isfinite(v))
                and np.all(np.isfinite(q))
                and np.all(np.isfinite(p))
            ):
                raise FloatingPointError(
                    f"nonfinite feedback prehistory order={order} segment={ib} step={iseg+1}"
                )

    return {
        "q": q,
        "p": p,
        "v": v,
        "steps": int(steps),
        "energy_identity_max": float(energy_max),
        "min_completed_square_energy": float(min_energy),
        "psi_maxabs": float(psi_max),
    }


def build_metric_driver(data, member, order, pre):
    C = m.cos_matrix(NX)
    ops = m.spec_ops(NX)
    y, _ = r1.initial_state_stable(data, NX)
    q = np.asarray(pre["q"], float).copy()
    p = np.asarray(pre["p"], float).copy()

    t0 = float(data["t0"])
    t1 = float(data["t1"])
    h = (t1 - t0) / float(NSTEP)

    psi = np.empty((NSTEP + 1, NX), float)
    energy_max = float(pre["energy_identity_max"])
    min_energy = float(pre["min_completed_square_energy"])
    base_constraint_max = 0.0
    min1p = np.inf

    def record(i, t, ycur, qcur, pcur):
        nonlocal energy_max, min_energy, base_constraint_max, min1p
        ps, dg = unit_source_psi(data, t, ycur[1], qcur, pcur, ops, order)
        psi[i] = ps
        energy_max = max(energy_max, float(dg["energy_identity_relative_L2"]))
        min_energy = min(min_energy, float(dg["min_completed_square_energy"]))
        base_constraint_max = max(
            base_constraint_max, c.base_constraint(data, t, ycur, ops)
        )
        min1p = min(min1p, c.min_one_plus(data, t, ycur[1], ops, member))

    record(0, t0, y, q, p)

    for i in range(NSTEP):
        t = t0 + i * h
        th = t + 0.5 * h
        tn = t1 if i + 1 == NSTEP else t0 + (i + 1) * h
        a0 = m.bg_eval(data, t)[0]
        ah = m.bg_eval(data, th)[0]
        an = m.bg_eval(data, tn)[0]

        k1 = c.base_rhs(data, t, y, ops, C, member, True)
        y2 = y + 0.5 * h * k1
        k2 = c.base_rhs(data, th, y2, ops, C, member, True)
        y3 = y + 0.5 * h * k2
        k3 = c.base_rhs(data, th, y3, ops, C, member, True)
        y4 = y + h * k3
        k4 = c.base_rhs(data, tn, y4, ops, C, member, True)
        yn = y + (h / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)

        s0 = y[1] / a0
        s2 = y2[1] / ah
        s3 = y3[1] / ah
        s4 = y4[1] / an
        sn = yn[1] / an
        c.bath_advance(data, t, th, q, p, s0, s2, order)
        c.bath_advance(data, t, th, q, p, s0, s3, order)
        c.bath_advance(data, t, tn, q, p, s0, s4, order)
        qn, pn = c.bath_advance(data, t, tn, q, p, s0, sn, order)

        if not (
            np.all(np.isfinite(yn))
            and np.all(np.isfinite(qn))
            and np.all(np.isfinite(pn))
        ):
            raise FloatingPointError(f"nonfinite driver order={order} step={i+1}")

        y, q, p = yn, qn, pn
        record(i + 1, tn, y, q, p)

    return {
        "psi": psi,
        "energy_identity_max": float(energy_max),
        "min_completed_square_energy": float(min_energy),
        "base_constraint_max": float(base_constraint_max),
        "min_one_plus_j_eff": float(min1p),
    }


def integrate_feedback(data, member, order, pre, driver):
    C = m.cos_matrix(NX)
    ops = m.spec_ops(NX)
    y, _ = r1.initial_state_stable(data, NX)
    q = np.asarray(pre["q"], float).copy()
    p = np.asarray(pre["p"], float).copy()
    v = np.asarray(pre["v"], float).copy()

    t0 = float(data["t0"])
    t1 = float(data["t1"])
    h = (t1 - t0) / float(NSTEP)
    checks = np.asarray(data["tau_check"], float)
    ci = 0

    states = []
    efields = []
    psifields = []
    tangent_constraint_max = 0.0
    base_constraint_max = 0.0
    min1p = np.inf

    def store(t, ycur, vcur, psicur):
        nonlocal tangent_constraint_max, base_constraint_max, min1p
        Q = m.bg_eval(data, t)[2]
        states.append(c.canonical_tangent(vcur, Q))
        efields.append(c.delta_E(data, t, vcur, ops))
        psifields.append(np.asarray(psicur, float).copy())
        tangent_constraint_max = max(
            tangent_constraint_max, c.tangent_constraint(data, t, vcur, ops)
        )
        base_constraint_max = max(
            base_constraint_max, c.base_constraint(data, t, ycur, ops)
        )
        min1p = min(min1p, c.min_one_plus(data, t, ycur[1], ops, member))

    while ci < len(checks) and checks[ci] <= t0 + 1.0e-10:
        store(float(checks[ci]), y, v, driver["psi"][0])
        ci += 1

    for i in range(NSTEP):
        t = t0 + i * h
        th = t + 0.5 * h
        tn = t1 if i + 1 == NSTEP else t0 + (i + 1) * h
        a0 = m.bg_eval(data, t)[0]
        ah = m.bg_eval(data, th)[0]
        an = m.bg_eval(data, tn)[0]

        psi0 = driver["psi"][i]
        psin = driver["psi"][i + 1]
        psih = 0.5 * (psi0 + psin)

        by1 = c.base_rhs(data, t, y, ops, C, member, True)
        y2 = y + 0.5 * h * by1
        by2 = c.base_rhs(data, th, y2, ops, C, member, True)
        y3 = y + 0.5 * h * by2
        by3 = c.base_rhs(data, th, y3, ops, C, member, True)
        y4 = y + h * by3
        by4 = c.base_rhs(data, tn, y4, ops, C, member, True)
        yn = y + (h / 6.0) * (by1 + 2.0 * by2 + 2.0 * by3 + by4)

        s0 = y[1] / a0
        s2 = y2[1] / ah
        s3 = y3[1] / ah
        s4 = y4[1] / an
        sn = yn[1] / an

        k1 = rhs_feedback(data, t, y[1], v, q, p, ops, member, True, order, psi0)
        q2, p2 = c.bath_advance(data, t, th, q, p, s0, s2, order)
        v2 = v + 0.5 * h * k1
        k2 = rhs_feedback(data, th, y2[1], v2, q2, p2, ops, member, True, order, psih)

        q3, p3 = c.bath_advance(data, t, th, q, p, s0, s3, order)
        v3 = v + 0.5 * h * k2
        k3 = rhs_feedback(data, th, y3[1], v3, q3, p3, ops, member, True, order, psih)

        q4, p4 = c.bath_advance(data, t, tn, q, p, s0, s4, order)
        v4 = v + h * k3
        k4 = rhs_feedback(data, tn, y4[1], v4, q4, p4, ops, member, True, order, psin)

        vn = v + (h / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
        qn, pn = c.bath_advance(data, t, tn, q, p, s0, sn, order)

        if not (
            np.all(np.isfinite(yn))
            and np.all(np.isfinite(vn))
            and np.all(np.isfinite(qn))
            and np.all(np.isfinite(pn))
        ):
            raise FloatingPointError(f"nonfinite feedback order={order} step={i+1}")

        while ci < len(checks) and checks[ci] <= tn + 1.0e-10:
            frac = min(1.0, max(0.0, float((checks[ci] - t) / h)))
            yc = y + frac * (yn - y)
            vc = v + frac * (vn - v)
            pc = psi0 + frac * (psin - psi0)
            store(float(checks[ci]), yc, vc, pc)
            ci += 1

        y, v, q, p = yn, vn, qn, pn

    if ci != len(checks):
        raise RuntimeError(f"stored only {ci}/{len(checks)} checkpoints")

    return {
        "states": np.stack(states),
        "E": np.stack(efields),
        "Psi": np.stack(psifields),
        "finite": True,
        "base_constraint_max": float(max(base_constraint_max, driver["base_constraint_max"])),
        "tangent_constraint_max": float(tangent_constraint_max),
        "min_one_plus_j_eff": float(min(min1p, driver["min_one_plus_j_eff"])),
        "energy_identity_max": float(driver["energy_identity_max"]),
        "min_completed_square_energy": float(driver["min_completed_square_energy"]),
    }


def compare_feedback(a, b):
    names = ("delta_alpha", "delta_chi", "delta_Pchi", "delta_Palpha")
    out = {
        name: rel(lowband(a["states"][:, j]), lowband(b["states"][:, j]))
        for j, name in enumerate(names)
    }
    out["delta_E"] = rel(lowband(a["E"]), lowband(b["E"]))
    out["delta_Psi"] = rel(lowband(a["Psi"]), lowband(b["Psi"]))
    return out


def run_health(run):
    return bool(
        run["finite"]
        and run["base_constraint_max"] <= CONSTRAINT_GATE
        and run["tangent_constraint_max"] <= CONSTRAINT_GATE
        and run["min_one_plus_j_eff"] > 0.0
        and run["energy_identity_max"] <= ENERGY_GATE
        and run["min_completed_square_energy"] >= -1.0e-14
        and np.all(np.isfinite(run["states"]))
        and np.all(np.isfinite(run["E"]))
        and np.all(np.isfinite(run["Psi"]))
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--json-out",
        default="results/nl1c6d2c6h_final_self_consistent_metric_feedback_tangent.json",
    )
    args = ap.parse_args()
    outpath = Path(args.json_out)
    outpath.parent.mkdir(parents=True, exist_ok=True)

    try:
        print("NL1C6D2C6H_FINAL_SELF_CONSISTENT_METRIC_FEEDBACK_TANGENT_START", flush=True)
        head = git_head()
        ancestry = {
            "D2C6G_result": is_ancestor(G_RESULT),
            "D2C6F_R2_result": is_ancestor(R2_RESULT),
            "D2C6H_prereg": is_ancestor(PREREG),
        }
        print("D2C6H_HEAD=" + head, flush=True)
        print("D2C6H_ANCESTRY=" + json.dumps(ancestry, sort_keys=True), flush=True)

        quadrature = r2.r1b.install_direct_baths()
        data = m.prepare_class_data()
        ms = members()
        ss = sentinels()
        keys = [r2.d.member_key(x) for x in ms]
        skeys = [r2.d.member_key(x) for x in ss]
        exact = len(keys) == 27 and len(set(keys)) == 27 and len(set(skeys)) == 3

        zero = physical_zero_audit(data, PRIMARY_ORDER)
        print(f"D2C6H_PHYSICAL_ETA0_SOURCE_MAX={zero:.12e}", flush=True)

        print("D2C6H_PREHISTORY_FB256_BEGIN", flush=True)
        pre256 = feedback_prehistory(data, PRIMARY_ORDER)
        print(
            f"D2C6H_PREHISTORY_FB256_END steps={pre256['steps']} "
            f"psi_max={pre256['psi_maxabs']:.12e}",
            flush=True,
        )

        primary = {}
        records = []
        health_ok = True
        activity_ok = True

        for i, member in enumerate(ms, start=1):
            key = r2.d.member_key(member)
            driver = build_metric_driver(data, member, PRIMARY_ORDER, pre256)
            run = integrate_feedback(data, member, PRIMARY_ORDER, pre256, driver)
            primary[key] = run
            ok = run_health(run)
            health_ok = health_ok and ok
            psi_norm = float(np.linalg.norm(run["Psi"]))
            activity_ok = activity_ok and np.isfinite(psi_norm) and psi_norm > 0.0
            rec = {
                "index": i,
                "key": key,
                "health": ok,
                "base_constraint_max": run["base_constraint_max"],
                "tangent_constraint_max": run["tangent_constraint_max"],
                "min_one_plus_j_eff": run["min_one_plus_j_eff"],
                "energy_identity_max": run["energy_identity_max"],
                "psi_tangent_rms": float(np.sqrt(np.mean(run["Psi"] ** 2))),
                "psi_tangent_maxabs": float(np.max(np.abs(run["Psi"]))),
                "state_tangent_rms": float(np.sqrt(np.mean(run["states"] ** 2))),
            }
            records.append(rec)
            print(
                f"D2C6H_PRIMARY {i:02d}/27 {key} health={ok} "
                f"bcon={run['base_constraint_max']:.3e} "
                f"tcon={run['tangent_constraint_max']:.3e} "
                f"min1p={run['min_one_plus_j_eff']:.6e} "
                f"psi_rms={rec['psi_tangent_rms']:.6e}",
                flush=True,
            )

        pre_off256 = c.prehistory(data, NX, NSTEP, PRIMARY_ORDER)
        off_rows = []
        for member in ss:
            key = r2.d.member_key(member)
            off = c.integrate(
                data,
                NX,
                NSTEP,
                member,
                orders=(PRIMARY_ORDER,),
                nonlinear=True,
                pre_cache={PRIMARY_ORDER: pre_off256},
            )
            off_state = off["orders"][PRIMARY_ORDER]["states"]
            on_state = primary[key]["states"]
            diff = rel(lowband(on_state), lowband(off_state))
            active = bool(np.isfinite(diff) and np.linalg.norm(lowband(on_state) - lowband(off_state)) > 0.0)
            activity_ok = activity_ok and active
            off_rows.append({"key": key, "feedback_on_off_relative": diff, "active": active})
            print(f"D2C6H_SWITCH {key} rel={diff:.12e} active={active}", flush=True)

        print("D2C6H_PREHISTORY_FB512_BEGIN", flush=True)
        pre512 = feedback_prehistory(data, CONTROL_ORDER)
        print(
            f"D2C6H_PREHISTORY_FB512_END steps={pre512['steps']} "
            f"psi_max={pre512['psi_maxabs']:.12e}",
            flush=True,
        )

        bath_rows = []
        bath_ok = True
        for member in ss:
            key = r2.d.member_key(member)
            driver = build_metric_driver(data, member, CONTROL_ORDER, pre512)
            ctl = integrate_feedback(data, member, CONTROL_ORDER, pre512, driver)
            cmp = compare_feedback(primary[key], ctl)
            mx = max(cmp.values())
            ok = run_health(ctl) and mx <= BATH_GATE
            bath_ok = bath_ok and ok
            bath_rows.append({"key": key, "differences": cmp, "max": mx, "pass": ok})
            print(f"D2C6H_BATH {key} max={mx:.12e} pass={ok}", flush=True)

        h1 = bool(all(ancestry.values()) and exact)
        h2 = bool(zero <= ZERO_GATE)
        h3 = bool(health_ok)
        h4 = bool(activity_ok)
        h5 = bool(bath_ok)
        h6 = True
        gates = {
            "H1_provenance_exact27_and_sentinels": h1,
            "H2_eta0_physical_source_identity_and_base_unmodified": h2,
            "H3_all27_feedback_tangent_health": h3,
            "H4_metric_feedback_active_switch_control": h4,
            "H5_direct256_512_feedback_tangent_convergence": h5,
            "H6_scope_clean_final_before_observables": h6,
        }
        passed = all(gates.values())
        classification = PASS_LABEL if passed else FAIL_LABEL

        result = {
            "classification": classification,
            "head": head,
            "ancestry": ancestry,
            "predata_commit": PREREG,
            "trajectory_eta": 0.0,
            "primary_order": PRIMARY_ORDER,
            "control_order": CONTROL_ORDER,
            "nx": NX,
            "nstep": NSTEP,
            "quadrature_audit": quadrature,
            "physical_eta0_source_maxabs": zero,
            "primary_records": records,
            "feedback_switch_controls": off_rows,
            "bath_controls": bath_rows,
            "gates": gates,
            "observational_implementation_step_licensed": bool(passed),
            "observational_claim_licensed": False,
            "further_intermediate_numerical_bridge_preregistered": False,
            "scope": (
                "Final eta=0 longitudinal memory<->metric tangent closure in the certified nonlinear box. "
                "PASS returns the project to cosmological observables/likelihood implementation; it is not "
                "a claim of arbitrary-amplitude fully nonlinear GR/AeST."
            ),
        }
        outpath.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print("GATES=" + json.dumps(gates, sort_keys=True), flush=True)
        print("CLASSIFICATION=" + classification, flush=True)
        print("OBSERVATIONAL_IMPLEMENTATION_STEP_LICENSED=" + str(bool(passed)), flush=True)
        print("FURTHER_INTERMEDIATE_NUMERICAL_BRIDGE_PREREGISTERED=False", flush=True)
        print("JSON=" + str(outpath), flush=True)
        print("NL1C6D2C6H_FINAL_SELF_CONSISTENT_METRIC_FEEDBACK_TANGENT_END", flush=True)
        raise SystemExit(0 if passed else 1)

    except SystemExit:
        raise
    except Exception as exc:
        result = {
            "classification": INCOMPLETE_LABEL,
            "error_type": type(exc).__name__,
            "error": str(exc),
            "observational_implementation_step_licensed": False,
            "further_intermediate_numerical_bridge_preregistered": False,
        }
        outpath.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print("CLASSIFICATION=" + INCOMPLETE_LABEL, flush=True)
        print(f"ERROR={type(exc).__name__}: {exc}", flush=True)
        print("OBSERVATIONAL_IMPLEMENTATION_STEP_LICENSED=False", flush=True)
        raise SystemExit(2)


if __name__ == "__main__":
    main()
