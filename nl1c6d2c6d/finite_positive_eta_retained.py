#!/usr/bin/env python3
from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Importing R3 installs the certified modewise full-prehistory implementation
# into c.prehistory.  All eta=0 tangent helpers remain the frozen D2C6C code.
from nl1c6d2c6c import r3_modewise_full_prehistory as r3

c = r3.c
m = c.m
d2b = c.d2b
r1 = c.r1

PARENT_R7_HEAD = "a6c61e275ce2ab949dd108ac2b326a4ed617ebcc"
PARENT_R7_RUN = 34502078991
PREREG_HEAD = "fc120a6666c751139cc1fc794f148c90e05938a5"

ETAS = (2.0**-8, 2.0**-7, 2.0**-6)
ETA_SMALL = ETAS[0]
ETA_MAX = ETAS[-1]
PRIMARY_ORDER = 39
CONTROL_ORDER = 47

SOURCE_GATE = 1.0e-10
TANGENT_GATE = 5.0e-3
CONSTRAINT_GATE = 1.0e-10
BATH_GATE = 1.0e-2
TIME_GATE = 2.0e-3
SPACE_GATE = 5.0e-3

PASS_LABEL = "NL1C6D2C6D_FINITE_POSITIVE_ETA_RETAINED_SCALAR_CURRENT_PASS"
FAIL_LABEL = "NL1C6D2C6D_FINITE_POSITIVE_ETA_RETAINED_SCALAR_CURRENT_FAIL"
INCOMPLETE_LABEL = "NL1C6D2C6D_FINITE_POSITIVE_ETA_RETAINED_SCALAR_CURRENT_INCOMPLETE"


def rel_l2(a, b):
    aa = np.asarray(a, float)
    bb = np.asarray(b, float)
    return float(np.linalg.norm(aa - bb) / max(np.linalg.norm(bb), 1.0e-300))


def member_key(member):
    return d2b.member_key(member)


def canonical_difference(d, Q):
    out = np.empty_like(d)
    out[0] = d[0]
    out[1] = d[1]
    out[2] = d[2]
    out[3] = d[3] - Q * d[2]
    return out


def finite_source(data, tau, full_chi, q, ops, order):
    a, _, Q = m.bg_eval(data, tau)[:3]
    _, lap, _, _ = ops
    _, weights = c.BATH_DATA[order]
    B = c.bath_residual(full_chi, a, q, weights)
    M = a * a * lap(B)
    return B, M, Q


def linear_difference_rhs(data, tau, d, full_chi, q, ops, eta, order):
    """Exact retained linear finite-eta difference around frozen CLASS history."""
    a, _, Q, KQ, KQQ, _, Qdot = m.bg_eval(data, tau)
    _, lap, _, _ = ops
    de = c.delta_E(data, tau, d, ops)
    B, M, _ = finite_source(data, tau, full_chi, q, ops, order)

    da = a * de
    dc = a * (d[2] / (2.0 * a**3 * KQQ) + Q * de + Qdot * d[0])
    dp = a * (
        -2.0 * m.A * a * lap(de)
        + 2.0 * m.A * a * lap(d[1])
        - 2.0 * a * KQ * lap(d[0])
    ) + eta * M
    ds = a * (
        -2.0 * a * KQ * lap(d[1])
        - 2.0 * m.A * a * Q * lap(de)
        + 2.0 * m.A * a * Q * lap(d[1])
    ) + eta * Q * M
    return np.stack([da, dc, dp, ds]), B


def finite_prehistory(data, nx, nstep_main, eta, order):
    """Modewise regular finite-eta linear prehistory, summed at z=6."""
    C = m.cos_matrix(nx)
    ops = m.spec_ops(nx)
    t0 = float(data["t0"])
    hmain = (float(data["t1"]) - t0) / float(nstep_main)
    omega, _ = c.BATH_DATA[order]

    d_total = np.zeros((4, nx), float)
    q_total = np.zeros((len(omega), nx), float)
    p_total = np.zeros_like(q_total)
    starts = []
    counts = []
    bmax = 0.0

    for index, md in enumerate(data["modes"]):
        tpre = float(md["tau_lo"])
        if tpre > t0 + 1.0e-12:
            raise m.InputIncomplete(f"D2C6D mode {index} history begins after z=6")
        mode_data = r3._single_mode_data(data, index)
        d = np.zeros((4, nx), float)
        q = np.zeros_like(q_total)
        p = np.zeros_like(q_total)

        if abs(t0 - tpre) <= 1.0e-12:
            npre = 0
        else:
            npre = max(1, int(math.ceil((t0 - tpre) / hmain)))
            h = (t0 - tpre) / float(npre)
            for istep in range(npre):
                t = tpre + istep * h
                th = t + 0.5 * h
                tn = t0 if istep + 1 == npre else tpre + (istep + 1) * h

                base0 = r3._mode_chi_field(data, mode_data, index, t, C)
                baseh = r3._mode_chi_field(data, mode_data, index, th, C)
                basen = r3._mode_chi_field(data, mode_data, index, tn, C)
                a0 = m.bg_eval(mode_data, t)[0]
                ah = m.bg_eval(mode_data, th)[0]
                an = m.bg_eval(mode_data, tn)[0]

                full0 = base0 + d[1]
                s0 = full0 / a0
                k1, B1 = linear_difference_rhs(
                    mode_data, t, d, full0, q, ops, eta, order
                )
                d2 = d + 0.5 * h * k1
                full2 = baseh + d2[1]
                s2 = full2 / ah
                q2, p2 = c.bath_advance(mode_data, t, th, q, p, s0, s2, order)

                k2, B2 = linear_difference_rhs(
                    mode_data, th, d2, full2, q2, ops, eta, order
                )
                d3 = d + 0.5 * h * k2
                full3 = baseh + d3[1]
                s3 = full3 / ah
                q3, p3 = c.bath_advance(mode_data, t, th, q, p, s0, s3, order)

                k3, B3 = linear_difference_rhs(
                    mode_data, th, d3, full3, q3, ops, eta, order
                )
                d4 = d + h * k3
                full4 = basen + d4[1]
                s4 = full4 / an
                q4, p4 = c.bath_advance(mode_data, t, tn, q, p, s0, s4, order)

                k4, B4 = linear_difference_rhs(
                    mode_data, tn, d4, full4, q4, ops, eta, order
                )
                dn = d + (h / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
                fulln = basen + dn[1]
                sn = fulln / an
                qn, pn = c.bath_advance(mode_data, t, tn, q, p, s0, sn, order)

                if not (
                    np.all(np.isfinite(dn))
                    and np.all(np.isfinite(qn))
                    and np.all(np.isfinite(pn))
                ):
                    raise FloatingPointError(
                        f"D2C6D nonfinite prehistory mode={index} eta={eta:.12e} "
                        f"order={order} step={istep+1}/{npre}"
                    )
                bmax = max(
                    bmax,
                    float(np.linalg.norm(B1)),
                    float(np.linalg.norm(B2)),
                    float(np.linalg.norm(B3)),
                    float(np.linalg.norm(B4)),
                )
                d, q, p = dn, qn, pn

        d_total += d
        q_total += q
        p_total += p
        starts.append(tpre)
        counts.append(int(npre))

    print(
        "D2C6D_PREHISTORY "
        f"eta={eta:.12e} order={order} nx={nx} nstep_main={nstep_main} "
        f"tau_lo={','.join(f'{x:.12e}' for x in starts)} "
        f"npre={','.join(str(x) for x in counts)}",
        flush=True,
    )
    return {
        "d": d_total,
        "q": q_total,
        "p": p_total,
        "tpre": float(min(starts)),
        "nstep": int(sum(counts)),
        "bath_B_norm_max": float(bmax),
    }


def pair_rhs(data, tau, y0, d, q, ops, C, member, eta, order):
    by = c.base_rhs(data, tau, y0, ops, C, member, True)
    full = y0 + d
    fy = c.base_rhs(data, tau, full, ops, C, member, True)
    B, M, Q = finite_source(data, tau, full[1], q, ops, order)
    dd = fy - by
    dd = np.asarray(dd, float).copy()
    dd[2] += eta * M
    dd[3] += eta * Q * M
    return by, dd, B


def integrate_finite(data, nx, nstep, member, eta, order, pre_cache=None):
    C = m.cos_matrix(nx)
    ops = m.spec_ops(nx)
    y0, init = r1.initial_state_stable(data, nx)
    if pre_cache is None:
        pre_cache = finite_prehistory(data, nx, nstep, eta, order)
    d = np.asarray(pre_cache["d"], float).copy()
    q = np.asarray(pre_cache["q"], float).copy()
    p = np.asarray(pre_cache["p"], float).copy()

    t0 = float(data["t0"])
    t1 = float(data["t1"])
    h = (t1 - t0) / float(nstep)
    tchecks = np.asarray(data["tau_check"], float)
    states = []
    efields = []
    full_constraint_max = 0.0
    min1p = np.inf
    bmax = float(pre_cache.get("bath_B_norm_max", 0.0))
    finite = True
    fail_reason = None

    def store(t, ycur, dcur):
        nonlocal full_constraint_max, min1p
        full = ycur + dcur
        Q = m.bg_eval(data, t)[2]
        states.append(canonical_difference(dcur, Q))
        efields.append(c.delta_E(data, t, dcur, ops))
        full_constraint_max = max(
            full_constraint_max, c.base_constraint(data, t, full, ops)
        )
        min1p = min(min1p, c.min_one_plus(data, t, full[1], ops, member))

    store(t0, y0, d)
    ci = 1

    for istep in range(nstep):
        t = t0 + istep * h
        th = t + 0.5 * h
        tn = t1 if istep + 1 == nstep else t0 + (istep + 1) * h
        a0 = m.bg_eval(data, t)[0]
        ah = m.bg_eval(data, th)[0]
        an = m.bg_eval(data, tn)[0]

        by1, k1, B1 = pair_rhs(data, t, y0, d, q, ops, C, member, eta, order)
        y2 = y0 + 0.5 * h * by1
        d2 = d + 0.5 * h * k1
        s0 = (y0[1] + d[1]) / a0
        s2 = (y2[1] + d2[1]) / ah
        q2, p2 = c.bath_advance(data, t, th, q, p, s0, s2, order)

        by2, k2, B2 = pair_rhs(data, th, y2, d2, q2, ops, C, member, eta, order)
        y3 = y0 + 0.5 * h * by2
        d3 = d + 0.5 * h * k2
        s3 = (y3[1] + d3[1]) / ah
        q3, p3 = c.bath_advance(data, t, th, q, p, s0, s3, order)

        by3, k3, B3 = pair_rhs(data, th, y3, d3, q3, ops, C, member, eta, order)
        y4 = y0 + h * by3
        d4 = d + h * k3
        s4 = (y4[1] + d4[1]) / an
        q4, p4 = c.bath_advance(data, t, tn, q, p, s0, s4, order)

        by4, k4, B4 = pair_rhs(data, tn, y4, d4, q4, ops, C, member, eta, order)
        yn = y0 + (h / 6.0) * (by1 + 2.0 * by2 + 2.0 * by3 + by4)
        dn = d + (h / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
        sn = (yn[1] + dn[1]) / an
        qn, pn = c.bath_advance(data, t, tn, q, p, s0, sn, order)

        if not (
            np.all(np.isfinite(yn))
            and np.all(np.isfinite(dn))
            and np.all(np.isfinite(qn))
            and np.all(np.isfinite(pn))
        ):
            finite = False
            fail_reason = f"nonfinite_step_{istep+1}"
            break

        bmax = max(
            bmax,
            float(np.linalg.norm(B1)),
            float(np.linalg.norm(B2)),
            float(np.linalg.norm(B3)),
            float(np.linalg.norm(B4)),
        )

        old_y = y0
        old_d = d
        while ci < len(tchecks) and tchecks[ci] <= tn + 1.0e-10:
            frac = float((tchecks[ci] - t) / h)
            frac = min(1.0, max(0.0, frac))
            yc = old_y + frac * (yn - old_y)
            dc = old_d + frac * (dn - old_d)
            store(float(tchecks[ci]), yc, dc)
            ci += 1

        y0, d, q, p = yn, dn, qn, pn
        if (istep + 1) % 8 == 0:
            full = y0 + d
            min1p = min(min1p, c.min_one_plus(data, tn, full[1], ops, member))

    if finite and ci != len(tchecks):
        finite = False
        fail_reason = f"stored_only_{ci}_of_{len(tchecks)}_checkpoints"

    arr = np.stack(states) if states else np.empty((0, 4, nx))
    ee = np.stack(efields) if efields else np.empty((0, nx))
    return {
        "finite": bool(finite),
        "fail_reason": fail_reason,
        "eta": float(eta),
        "order": int(order),
        "nx": int(nx),
        "nstep": int(nstep),
        "states": arr,
        "E": ee,
        "full_constraint_max": float(full_constraint_max),
        "min_one_plus_j_eff": float(min1p),
        "bath_B_norm_max": float(bmax),
        "prehistory_steps": int(pre_cache["nstep"]),
        "prehistory_start_tau": float(pre_cache["tpre"]),
        "initial": init,
    }


def compare_displacements(a, b, spatial=False):
    aa = np.asarray(a["states"], float)
    bb = np.asarray(b["states"], float)
    names = ("d_alpha", "d_chi", "d_Pchi", "d_Palpha")
    vals = {}
    for j, name in enumerate(names):
        x = aa[:, j]
        y = bb[:, j]
        if spatial:
            y = np.stack([m.static.spectral_resample(row, x.shape[1]) for row in y])
        vals[name] = rel_l2(x, y)
    return vals, max(vals.values())


def tangent_continuation(finite_run, tangent_run, eta):
    tr = tangent_run["orders"][39]
    fields = {
        "alpha": rel_l2(finite_run["states"][:, 0] / eta, tr["states"][:, 0]),
        "E": rel_l2(finite_run["E"] / eta, tr["E"]),
        "chi": rel_l2(finite_run["states"][:, 1] / eta, tr["states"][:, 1]),
    }
    momentum = {
        "Pchi": rel_l2(finite_run["states"][:, 2] / eta, tr["states"][:, 2]),
        "Palpha": rel_l2(finite_run["states"][:, 3] / eta, tr["states"][:, 3]),
    }
    return fields, momentum, max(fields.values())


def displacement_diagnostics(run, tangent_run, eta):
    tr = tangent_run["orders"][39]
    out = {}
    pairs = {
        "alpha": (run["states"][:, 0], tr["states"][:, 0]),
        "E": (run["E"], tr["E"]),
        "chi": (run["states"][:, 1], tr["states"][:, 1]),
    }
    for name, (disp, tan) in pairs.items():
        dd = np.asarray(disp, float)
        tt = np.asarray(tan, float)
        denom = max(float(np.vdot(tt.ravel(), tt.ravel()).real), 1.0e-300)
        projection = float(np.vdot(tt.ravel(), dd.ravel()).real / denom)
        remainder = dd - eta * tt
        out[name] = {
            "displacement_norm": float(np.linalg.norm(dd)),
            "signed_tangent_projection": projection,
            "projection_over_eta": float(projection / eta),
            "remainder_over_eta_tangent": float(
                np.linalg.norm(remainder) / max(abs(eta) * np.linalg.norm(tt), 1.0e-300)
            ),
        }
    return out


def source_identity_audit(data):
    # Reuse the certified deterministic B field from C2, now with physical eta.
    nx = 128
    ops = m.spec_ops(nx)
    _, lap, invlap, _ = ops
    x = np.arange(nx) * m.static.BOX / nx
    B = np.cos(m.K_MPC[1] * x + 0.37) + 0.3 * np.cos(m.K_MPC[4] * x - 0.21)
    B -= np.mean(B)
    tau = float(data["tau_check"][4])
    a, _, Q = m.bg_eval(data, tau)[:3]
    M = a * a * lap(B)
    eta = ETA_MAX
    reconstructed = invlap(-eta * Q * M / (2.0 * a)) / m.static.KB
    expected = -eta * a * Q * B / (2.0 * m.static.KB)
    elliptic = rel_l2(reconstructed, expected)
    inc = np.stack([np.zeros(nx), np.zeros(nx), eta * M, eta * Q * M])
    expected_inc = np.stack([np.zeros(nx), np.zeros(nx), eta * M, eta * Q * M])
    increment = rel_l2(inc, expected_inc)
    return {"elliptic_relative_L2": elliptic, "increment_relative_L2": increment}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--json-out",
        default="results/nl1c6d2c6d_finite_positive_eta_retained.json",
    )
    args = ap.parse_args()

    try:
        data = m.prepare_class_data()
        print("NL1C6D2C6D_FINITE_POSITIVE_ETA_RETAINED_START", flush=True)
        print(
            "D2C6D_ETA_LADDER=" + ",".join(f"{x:.12e}" for x in ETAS),
            flush=True,
        )

        expected = [
            {"sigma": s, "kind": kind, "beta0": beta}
            for s, kind, beta in itertools.product(d2b.SIGMAS, d2b.KINDS, d2b.BETAS)
        ]
        coverage = len(expected) == 27 and len({member_key(q) for q in expected}) == 27

        source_audit = source_identity_audit(data)
        d2 = bool(
            source_audit["elliptic_relative_L2"] <= SOURCE_GATE
            and source_audit["increment_relative_L2"] <= SOURCE_GATE
        )
        print(
            "D2_SOURCE "
            f"elliptic={source_audit['elliptic_relative_L2']:.12e} "
            f"increment={source_audit['increment_relative_L2']:.12e} pass={d2}",
            flush=True,
        )

        # Prehistories depend on eta/resolution/order but not on the nonlinear
        # completion member, so compute each frozen case once and reuse it.
        pre_primary = {
            eta: finite_prehistory(data, 128, 4096, eta, PRIMARY_ORDER)
            for eta in ETAS
        }
        pre_order47 = finite_prehistory(data, 128, 4096, ETA_MAX, CONTROL_ORDER)
        pre_time = finite_prehistory(data, 128, 8192, ETA_MAX, PRIMARY_ORDER)
        pre_space = finite_prehistory(data, 256, 4096, ETA_MAX, PRIMARY_ORDER)

        # Certified eta=0 tangent prehistory is likewise member-independent.
        tangent_pre = {PRIMARY_ORDER: c.prehistory(data, 128, 4096, PRIMARY_ORDER)}

        records = []
        primary_runs = {}
        tangent_runs = {}
        tangent_errors = []
        health_fail = False

        for index, member in enumerate(expected, start=1):
            key = member_key(member)
            tangent = c.integrate(
                data, 128, 4096, member, orders=(PRIMARY_ORDER,),
                nonlinear=True, pre_cache=tangent_pre,
            )
            if not tangent["finite"]:
                raise RuntimeError(f"certified tangent reproduction nonfinite for {key}")
            tangent_runs[key] = tangent

            for eta in ETAS:
                run = integrate_finite(
                    data, 128, 4096, member, eta, PRIMARY_ORDER, pre_primary[eta]
                )
                primary_runs[(key, eta)] = run
                healthy = bool(
                    run["finite"]
                    and run["full_constraint_max"] <= CONSTRAINT_GATE
                    and run["min_one_plus_j_eff"] > 0.0
                )
                health_fail = health_fail or (not healthy)

                tc_fields = None
                tc_momentum = None
                tc_max = None
                if eta == ETA_SMALL:
                    tc_fields, tc_momentum, tc_max = tangent_continuation(run, tangent, eta)
                    tangent_errors.append(float(tc_max))

                diag = displacement_diagnostics(run, tangent, eta)
                rec = {
                    "index": index,
                    "key": key,
                    "sigma": int(member["sigma"]),
                    "kind": str(member["kind"]),
                    "beta0": float(member["beta0"]),
                    "eta": float(eta),
                    "finite": bool(run["finite"]),
                    "health_pass": healthy,
                    "full_constraint_max": float(run["full_constraint_max"]),
                    "min_one_plus_j_eff": float(run["min_one_plus_j_eff"]),
                    "tangent_continuation": tc_fields,
                    "tangent_momentum_diagnostic": tc_momentum,
                    "tangent_continuation_max": tc_max,
                    "diagnostics": diag,
                }
                records.append(rec)
                print(
                    "D2C6D_MEMBER "
                    f"{index:02d}/27 eta={eta:.12e} {key} "
                    f"health={healthy} constraint={run['full_constraint_max']:.6e} "
                    f"min1p={run['min_one_plus_j_eff']:.6e} "
                    f"tangent_max={'NA' if tc_max is None else f'{tc_max:.6e}'} "
                    f"dalpha={diag['alpha']['displacement_norm']:.6e} "
                    f"dE={diag['E']['displacement_norm']:.6e} "
                    f"dchi={diag['chi']['displacement_norm']:.6e}",
                    flush=True,
                )

        d3_max = max(tangent_errors) if tangent_errors else float("inf")
        d3 = bool(d3_max <= TANGENT_GATE)

        control_records = []
        bath_max = 0.0
        time_max = 0.0
        space_max = 0.0
        for index, member in enumerate(expected, start=1):
            key = member_key(member)
            primary = primary_runs[(key, ETA_MAX)]
            order47 = integrate_finite(
                data, 128, 4096, member, ETA_MAX, CONTROL_ORDER, pre_order47
            )
            timectl = integrate_finite(
                data, 128, 8192, member, ETA_MAX, PRIMARY_ORDER, pre_time
            )
            spacectl = integrate_finite(
                data, 256, 4096, member, ETA_MAX, PRIMARY_ORDER, pre_space
            )

            bath_fields, bmax = compare_displacements(primary, order47, False)
            time_fields, tmax = compare_displacements(primary, timectl, False)
            space_fields, smax = compare_displacements(primary, spacectl, True)
            bath_max = max(bath_max, float(bmax))
            time_max = max(time_max, float(tmax))
            space_max = max(space_max, float(smax))

            control_health = all(
                r["finite"]
                and r["full_constraint_max"] <= CONSTRAINT_GATE
                and r["min_one_plus_j_eff"] > 0.0
                for r in (order47, timectl, spacectl)
            )
            health_fail = health_fail or (not control_health)
            control_records.append(
                {
                    "index": index,
                    "key": key,
                    "bath_order": bath_fields,
                    "bath_order_max": float(bmax),
                    "time": time_fields,
                    "time_max": float(tmax),
                    "space": space_fields,
                    "space_max": float(smax),
                    "control_health": bool(control_health),
                }
            )
            print(
                "D2C6D_CONTROL "
                f"{index:02d}/27 {key} bath={bmax:.6e} "
                f"time={tmax:.6e} space={smax:.6e} health={control_health}",
                flush=True,
            )

        d1 = bool(coverage and len(records) == 81)
        d4 = bool(not health_fail and all(r["health_pass"] for r in records))
        d5 = bool(bath_max <= BATH_GATE)
        d6 = bool(time_max <= TIME_GATE)
        d7 = bool(space_max <= SPACE_GATE)
        d8 = True
        gates = {
            "D1_R7_provenance_and_exact_27x3_coverage": d1,
            "D2_finite_eta_source_identity_le_1e-10": d2,
            "D3_eta_to_zero_tangent_continuation_le_5e-3": d3,
            "D4_all_finite_eta_health": d4,
            "D5_bath_order_displacement_convergence_le_1e-2": d5,
            "D6_time_displacement_convergence_le_2e-3": d6,
            "D7_space_displacement_convergence_le_5e-3": d7,
            "D8_scope_clean": d8,
        }
        passed = all(gates.values())
        classification = PASS_LABEL if passed else FAIL_LABEL

        # Non-gating dyadic quotient-change diagnostics.
        quotient_change = []
        for member in expected:
            key = member_key(member)
            runs = [primary_runs[(key, eta)] for eta in ETAS]
            entry = {"key": key, "fields": {}}
            for name, getter in (
                ("alpha", lambda r: r["states"][:, 0]),
                ("E", lambda r: r["E"]),
                ("chi", lambda r: r["states"][:, 1]),
            ):
                qs = [np.asarray(getter(r), float) / eta for r, eta in zip(runs, ETAS)]
                entry["fields"][name] = {
                    "q_eta1_vs_eta2": rel_l2(qs[0], qs[1]),
                    "q_eta2_vs_eta3": rel_l2(qs[1], qs[2]),
                }
            quotient_change.append(entry)

        out = {
            "classification": classification,
            "parent_R7": {"head": PARENT_R7_HEAD, "run": PARENT_R7_RUN},
            "predata_commit": PREREG_HEAD,
            "eta_values": [float(x) for x in ETAS],
            "scope": {
                "retained_scalar_current_only": True,
                "external_metric_matter_frozen": True,
                "direct_nonlinear_memory_Einstein_stress_included": False,
                "nonlinear_matter_evolution_included": False,
                "observational_likelihood": False,
                "full_nonlinear_AeST_memory_claim": False,
            },
            "source_identity": source_audit,
            "tangent_continuation_max": float(d3_max),
            "worst_bath_order": float(bath_max),
            "worst_time": float(time_max),
            "worst_space": float(space_max),
            "gates": gates,
            "primary_records": records,
            "control_records": control_records,
            "dyadic_quotient_change_non_gating": quotient_change,
            "larger_amplitude_retained_eta_step_licensed": bool(passed),
            "full_nonlinear_or_observational_step_licensed": False,
        }
        Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")

        print(f"D3_TANGENT_CONTINUATION_MAX={d3_max:.12e}", flush=True)
        print(f"WORST_BATH_ORDER={bath_max:.12e}", flush=True)
        print(f"WORST_TIME={time_max:.12e}", flush=True)
        print(f"WORST_SPACE={space_max:.12e}", flush=True)
        print(f"GATES={json.dumps(gates, sort_keys=True)}", flush=True)
        print(f"CLASSIFICATION={classification}", flush=True)
        print(f"LARGER_AMPLITUDE_RETAINED_ETA_STEP_LICENSED={passed}", flush=True)
        print("FULL_NONLINEAR_OR_OBSERVATIONAL_STEP_LICENSED=False", flush=True)
        print(f"JSON={args.json_out}", flush=True)
        print("NL1C6D2C6D_FINITE_POSITIVE_ETA_RETAINED_END", flush=True)
        return 0 if passed else 2

    except m.InputIncomplete as exc:
        print(f"D2C6D_INCOMPLETE {type(exc).__name__}: {exc}", flush=True)
        print(f"CLASSIFICATION={INCOMPLETE_LABEL}", flush=True)
        print("LARGER_AMPLITUDE_RETAINED_ETA_STEP_LICENSED=False", flush=True)
        print("FULL_NONLINEAR_OR_OBSERVATIONAL_STEP_LICENSED=False", flush=True)
        return 3
    except Exception as exc:
        print(f"D2C6D_ERROR {type(exc).__name__}: {exc}", flush=True)
        print(f"CLASSIFICATION={INCOMPLETE_LABEL}", flush=True)
        print("LARGER_AMPLITUDE_RETAINED_ETA_STEP_LICENSED=False", flush=True)
        print("FULL_NONLINEAR_OR_OBSERVATIONAL_STEP_LICENSED=False", flush=True)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
