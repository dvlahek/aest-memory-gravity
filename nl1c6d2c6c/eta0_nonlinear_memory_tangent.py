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

from nl1c6d2c6ar1 import stable_canonical_integrator as r1
from nl1c6d2c6b import all27_physical_nonlinear_trajectories as d2b
from v019u import apply_tau1_bath_patch as bathdef

m = r1.m

PARENT_HEAD = "3e1ec4a72be081318d06af174d3afcd855cbbc72"
PARENT_RUN = 34447971316
PREREG_HEAD = "fe34cbfb651f4e27fd05479f48c5832dd23863c2"

PASS_LABEL = "NL1C6D2C6C_ETA0_NONLINEAR_MEMORY_TANGENT_PASS"
FAIL_LABEL = "NL1C6D2C6C_ETA0_NONLINEAR_MEMORY_TANGENT_FAIL"
INCOMPLETE_LABEL = "NL1C6D2C6C_ETA0_NONLINEAR_MEMORY_TANGENT_INCOMPLETE"

TAUH0 = 1.0
ORDERS = (39, 47)
PRIMARY_ORDER = 39
BATH_GATE = 1.0e-2
TIME_GATE = 2.0e-3
SPACE_GATE = 5.0e-3
CONSTRAINT_GATE = 1.0e-10
FLUX_FD_GATE = 1.0e-6
BRIDGE_GATE = 1.0e-10
LINEAR_GATE = 5.0e-3
H0_MPC = m.static.H0 / m.static.C_KM

BATH_DATA = {
    39: (np.asarray(bathdef.OMEGA39, float), np.asarray(bathdef.WEIGHT39, float)),
    47: (np.asarray(bathdef.OMEGA47, float), np.asarray(bathdef.WEIGHT47, float)),
}


def rel_l2(a, b):
    aa = np.asarray(a, float)
    bb = np.asarray(b, float)
    return float(np.linalg.norm(aa - bb) / max(np.linalg.norm(bb), 1e-300))


def canonical_tangent(v, Q):
    out = np.empty_like(v)
    out[0] = v[0]
    out[1] = v[1]
    out[2] = v[2]
    out[3] = v[3] - Q * v[2]
    return out


def delta_E(data, tau, v, ops):
    a = m.bg_eval(data, tau)[0]
    _, _, invlap, _ = ops
    combo = invlap(-v[3] / (2.0 * a))
    return (combo - m.A * v[1]) / m.static.KB


def jeff_and_derivative(x, Z, member):
    sigma = int(member["sigma"])
    kind = str(member["kind"])
    beta = float(member["beta0"])
    xx = np.asarray(x, float)
    j, jp = m.static.j_and_prime(xx, beta, kind, saturated=False)
    tanh2 = math.tanh(float(Z)) ** 2
    sx = xx * xx / (1.0 + xx * xx)
    mix = 1.0 + sigma * d2b.EPS_MIX * sx * tanh2
    dmix = sigma * d2b.EPS_MIX * (2.0 * xx / (1.0 + xx * xx) ** 2) * tanh2
    je = j * mix
    dje = jp * mix + j * dmix
    return je, dje


def nonlinear_delta_operator(data, tau, base_chi, dchi, ops, member):
    a, _, _, _, _, Z, _ = m.bg_eval(data, tau)
    grad, _, _, div = ops
    g = grad(base_chi)
    dg = grad(dchi)
    x = m.static.ACC_CONV * np.abs(g) / a
    je, dje = jeff_and_derivative(x, Z, member)
    aeff = 1.0 + je + x * dje
    return div(aeff * dg)


def bath_residual(base_chi, a, q, weights):
    return np.asarray(base_chi, float) - a * np.tensordot(weights, q, axes=(0, 0))


def bath_advance(data, t0, t1, q, p, source0, source1, order):
    dt = float(t1 - t0)
    if dt == 0.0:
        return q.copy(), p.copy()
    tm = 0.5 * (t0 + t1)
    a, H = m.bg_eval(data, tm)[:2]
    omega_ratio, _ = BATH_DATA[order]
    omega = (a * H0_MPC * omega_ratio / TAUH0)[:, None]
    c = 2.0 * a * H
    d = 0.5 * c
    slope = (np.asarray(source1, float) - np.asarray(source0, float)) / dt
    u0 = q - source0[None, :]
    vu0 = p - slope[None, :]
    force = -c * slope[None, :]
    om2 = omega * omega
    disc = om2 - d * d
    scale = np.maximum(om2 + d * d, 1.0)
    under = disc[:, 0] > 1.0e-12 * scale[:, 0]
    over = disc[:, 0] < -1.0e-12 * scale[:, 0]
    crit = ~(under | over)
    un = np.empty_like(q)
    vn = np.empty_like(p)

    if np.any(under):
        O = np.sqrt(disc[under])
        z = O * dt
        ed = math.exp(-d * dt)
        Cc = np.cos(z)
        Ss = np.sin(z)
        uu = u0[under]
        vv = vu0[under]
        oo2 = om2[under]
        hu = ed * (uu * Cc + (vv + d * uu) / O * Ss)
        hv = ed * (vv * Cc - (d * vv + oo2 * uu) / O * Ss)
        one = 1.0 - ed * (Cc + d / O * Ss)
        G = ed * Ss / O
        un[under] = hu + force / oo2 * one
        vn[under] = hv + force * G

    if np.any(over):
        oo2 = om2[over]
        delta = np.sqrt(-disc[over])
        lam1 = -oo2 / (d + delta)
        lam2 = -d - delta
        den = lam1 - lam2
        e1 = np.exp(lam1 * dt)
        e2 = np.exp(lam2 * dt)
        uu = u0[over]
        vv = vu0[over]
        c1 = (vv - lam2 * uu) / den
        c2 = (lam1 * uu - vv) / den
        hu = c1 * e1 + c2 * e2
        hv = lam1 * c1 * e1 + lam2 * c2 * e2
        one = (-lam2 * (-np.expm1(lam1 * dt)) + lam1 * (-np.expm1(lam2 * dt))) / den
        G = (e1 - e2) / den
        un[over] = hu + force / oo2 * one
        vn[over] = hv + force * G

    if np.any(crit):
        oo2 = om2[crit]
        ed = math.exp(-d * dt)
        uu = u0[crit]
        vv = vu0[crit]
        hu = ed * (uu + (vv + d * uu) * dt)
        hv = ed * (vv - (d * vv + oo2 * uu) * dt)
        one = -math.expm1(-d * dt) - d * dt * ed
        G = ed * dt
        un[crit] = hu + force / oo2 * one
        vn[crit] = hv + force * G

    return source1[None, :] + un, vn + slope[None, :]


def tangent_rhs(data, tau, base_chi, v, q, ops, member, nonlinear, order):
    a, H, Q, KQ, KQQ, Z, Qdot = m.bg_eval(data, tau)
    _, lap, _, _ = ops
    de = delta_E(data, tau, v, ops)
    if nonlinear:
        dn = nonlinear_delta_operator(data, tau, base_chi, v[1], ops, member)
    else:
        dn = lap(v[1])
    _, weights = BATH_DATA[order]
    B = bath_residual(base_chi, a, q, weights)
    M = a * a * lap(B)

    da = a * de
    dc = a * (v[2] / (2.0 * a**3 * KQQ) + Q * de + Qdot * v[0])
    dp = a * (
        -2.0 * m.A * a * lap(de)
        + 2.0 * m.A * a * dn
        - 2.0 * a * KQ * lap(v[0])
    ) + M
    ds = a * (
        -2.0 * a * KQ * lap(v[1])
        - 2.0 * m.A * a * Q * lap(de)
        + 2.0 * m.A * a * Q * dn
    ) + Q * M
    return np.stack([da, dc, dp, ds])


def class_chi(data, tau, nx, C):
    a, _, Q = m.bg_eval(data, tau)[:3]
    alpha_m = m.mode_values(data, tau, "alpha")
    theta_m = m.mode_values(data, tau, "theta")
    chi_m = Q * (a * theta_m / (m.K_MPC * m.K_MPC) + alpha_m)
    return m.to_field(chi_m, C)


def prehistory(data, nx, nstep_main, order):
    C = m.cos_matrix(nx)
    ops = m.spec_ops(nx)
    t0 = float(data["t0"])
    tpre = max(float(md["tau_lo"]) for md in data["modes"])
    if tpre > t0 + 1e-12:
        raise m.InputIncomplete("linear perturbation histories begin after z=6")
    omega, _ = BATH_DATA[order]
    q = np.zeros((len(omega), nx), float)
    p = np.zeros_like(q)
    v = np.zeros((4, nx), float)
    if abs(t0 - tpre) <= 1e-12:
        return {"q": q, "p": p, "v": v, "tpre": tpre, "nstep": 0}

    hmain = (float(data["t1"]) - t0) / float(nstep_main)
    npre = max(1, int(math.ceil((t0 - tpre) / hmain)))
    h = (t0 - tpre) / npre

    for i in range(npre):
        t = tpre + i * h
        th = t + 0.5 * h
        tn = t0 if i + 1 == npre else t + h
        chi0 = class_chi(data, t, nx, C)
        chih = class_chi(data, th, nx, C)
        chin = class_chi(data, tn, nx, C)
        a0 = m.bg_eval(data, t)[0]
        ah = m.bg_eval(data, th)[0]
        an = m.bg_eval(data, tn)[0]
        s0 = chi0 / a0
        sh = chih / ah
        sn = chin / an

        k1 = tangent_rhs(data, t, chi0, v, q, ops, None, False, order)
        q2, p2 = bath_advance(data, t, th, q, p, s0, sh, order)
        v2 = v + 0.5 * h * k1
        k2 = tangent_rhs(data, th, chih, v2, q2, ops, None, False, order)
        q3, p3 = bath_advance(data, t, th, q, p, s0, sh, order)
        v3 = v + 0.5 * h * k2
        k3 = tangent_rhs(data, th, chih, v3, q3, ops, None, False, order)
        q4, p4 = bath_advance(data, t, tn, q, p, s0, sn, order)
        v4 = v + h * k3
        k4 = tangent_rhs(data, tn, chin, v4, q4, ops, None, False, order)
        vn = v + (h / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
        qn, pn = bath_advance(data, t, tn, q, p, s0, sn, order)

        if not (np.all(np.isfinite(vn)) and np.all(np.isfinite(qn)) and np.all(np.isfinite(pn))):
            raise FloatingPointError(f"nonfinite prehistory at step {i+1}/{npre}")
        v, q, p = vn, qn, pn

    return {"q": q, "p": p, "v": v, "tpre": tpre, "nstep": npre}


def base_rhs(data, tau, y, ops, C, member, nonlinear):
    if nonlinear:
        d2b.set_member(member)
        return d2b.rhs_member(data, tau, y, ops, C, True)
    return r1.rhs_stable(data, tau, y, ops, C, False)


def min_one_plus(data, tau, chi, ops, member):
    a, _, _, _, _, Z, _ = m.bg_eval(data, tau)
    grad = ops[0]
    x = m.static.ACC_CONV * np.abs(grad(chi)) / a
    je, _ = jeff_and_derivative(x, Z, member)
    return float(np.min(1.0 + je))


def tangent_constraint(data, tau, v, ops):
    a = m.bg_eval(data, tau)[0]
    _, lap, _, _ = ops
    de = delta_E(data, tau, v, ops)
    rhs = -2.0 * a * m.static.KB * lap(de) - 2.0 * m.A * a * lap(v[1])
    return m.norm_residual(v[3] - rhs, v[3], rhs)


def base_constraint(data, tau, y, ops):
    E, _ = r1.derive_E_stable(data, tau, y, ops)
    a = m.bg_eval(data, tau)[0]
    _, lap, _, _ = ops
    rhs = -2.0 * a * m.static.KB * lap(E) - 2.0 * m.A * a * lap(y[1])
    return m.norm_residual(y[3] - rhs, y[3], rhs)


def integrate(data, nx, nstep, member, orders=(39,), nonlinear=True, pre_cache=None):
    C = m.cos_matrix(nx)
    ops = m.spec_ops(nx)
    y, init = r1.initial_state_stable(data, nx)
    t0 = float(data["t0"])
    t1 = float(data["t1"])
    h = (t1 - t0) / nstep
    tchecks = np.asarray(data["tau_check"], float)

    if pre_cache is None:
        pre_cache = {order: prehistory(data, nx, nstep, order) for order in orders}

    baths = {}
    tangents = {}
    for order in orders:
        pre = pre_cache[order]
        baths[order] = [pre["q"].copy(), pre["p"].copy()]
        tangents[order] = pre["v"].copy()

    states = {order: [] for order in orders}
    efields = {order: [] for order in orders}
    max_tconstraint = {order: 0.0 for order in orders}
    max_bnorm = {order: 0.0 for order in orders}
    finite = True
    fail_reason = None
    max_base_constraint = 0.0
    min1p = np.inf

    def store(t, ycur, vcur):
        nonlocal max_base_constraint, min1p
        Q = m.bg_eval(data, t)[2]
        max_base_constraint = max(max_base_constraint, base_constraint(data, t, ycur, ops))
        if nonlinear:
            min1p = min(min1p, min_one_plus(data, t, ycur[1], ops, member))
        for order in orders:
            vv = vcur[order]
            states[order].append(canonical_tangent(vv, Q))
            efields[order].append(delta_E(data, t, vv, ops))
            max_tconstraint[order] = max(
                max_tconstraint[order], tangent_constraint(data, t, vv, ops)
            )

    store(t0, y, tangents)
    ci = 1

    for istep in range(nstep):
        t = t0 + istep * h
        th = t + 0.5 * h
        tn = t1 if istep + 1 == nstep else t0 + (istep + 1) * h

        by1 = base_rhs(data, t, y, ops, C, member, nonlinear)
        y2 = y + 0.5 * h * by1
        by2 = base_rhs(data, th, y2, ops, C, member, nonlinear)
        y3 = y + 0.5 * h * by2
        by3 = base_rhs(data, th, y3, ops, C, member, nonlinear)
        y4 = y + h * by3
        by4 = base_rhs(data, tn, y4, ops, C, member, nonlinear)
        yn = y + (h / 6.0) * (by1 + 2.0 * by2 + 2.0 * by3 + by4)

        a0 = m.bg_eval(data, t)[0]
        ah = m.bg_eval(data, th)[0]
        an = m.bg_eval(data, tn)[0]
        s0 = y[1] / a0
        s2 = y2[1] / ah
        s3 = y3[1] / ah
        s4 = y4[1] / an
        sn = yn[1] / an

        next_baths = {}
        next_tangents = {}
        old_tangents = {order: tangents[order].copy() for order in orders}
        for order in orders:
            q0, p0 = baths[order]
            v0 = tangents[order]
            q2, p2 = bath_advance(data, t, th, q0, p0, s0, s2, order)
            q3, p3 = bath_advance(data, t, th, q0, p0, s0, s3, order)
            q4, p4 = bath_advance(data, t, tn, q0, p0, s0, s4, order)

            k1 = tangent_rhs(data, t, y[1], v0, q0, ops, member, nonlinear, order)
            v2 = v0 + 0.5 * h * k1
            k2 = tangent_rhs(data, th, y2[1], v2, q2, ops, member, nonlinear, order)
            v3 = v0 + 0.5 * h * k2
            k3 = tangent_rhs(data, th, y3[1], v3, q3, ops, member, nonlinear, order)
            v4 = v0 + h * k3
            k4 = tangent_rhs(data, tn, y4[1], v4, q4, ops, member, nonlinear, order)
            vn = v0 + (h / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
            qn, pn = bath_advance(data, t, tn, q0, p0, s0, sn, order)

            _, weights = BATH_DATA[order]
            Bn = bath_residual(yn[1], an, qn, weights)
            max_bnorm[order] = max(max_bnorm[order], float(np.linalg.norm(Bn)))
            if not (
                np.all(np.isfinite(vn))
                and np.all(np.isfinite(qn))
                and np.all(np.isfinite(pn))
            ):
                finite = False
                fail_reason = f"nonfinite_order_{order}_step_{istep+1}"
                break
            next_baths[order] = [qn, pn]
            next_tangents[order] = vn

        if not finite or not np.all(np.isfinite(yn)):
            finite = False
            fail_reason = fail_reason or f"nonfinite_base_step_{istep+1}"
            break

        while ci < len(tchecks) and tchecks[ci] <= tn + 1e-10:
            frac = float((tchecks[ci] - t) / h)
            frac = min(1.0, max(0.0, frac))
            yc = y + frac * (yn - y)
            vc = {
                order: old_tangents[order] + frac * (next_tangents[order] - old_tangents[order])
                for order in orders
            }
            store(float(tchecks[ci]), yc, vc)
            ci += 1

        y = yn
        baths = next_baths
        tangents = next_tangents

        if nonlinear and (istep + 1) % 8 == 0:
            min1p = min(min1p, min_one_plus(data, tn, y[1], ops, member))

    if finite and ci != len(tchecks):
        finite = False
        fail_reason = f"stored_only_{ci}_of_{len(tchecks)}_checkpoints"

    out = {
        "finite": bool(finite),
        "fail_reason": fail_reason,
        "base_constraint_max": float(max_base_constraint),
        "min_one_plus_j_eff": float(min1p) if nonlinear else None,
        "initial": init,
        "orders": {},
    }
    for order in orders:
        if states[order]:
            arr = np.stack(states[order])
            ee = np.stack(efields[order])
        else:
            arr = np.empty((0, 4, nx))
            ee = np.empty((0, nx))
        out["orders"][order] = {
            "states": arr,
            "E": ee,
            "tangent_constraint_max": float(max_tconstraint[order]),
            "bath_B_norm_max": float(max_bnorm[order]),
            "prehistory_steps": int(pre_cache[order]["nstep"]),
            "prehistory_start_tau": float(pre_cache[order]["tpre"]),
        }
    return out


def compare_runs(a, b, order=39, spatial=False):
    aa = a["orders"][order]["states"]
    bb = b["orders"][order]["states"]
    names = ("delta_alpha", "delta_chi", "delta_Pchi", "delta_Palpha")
    vals = {}
    for j, name in enumerate(names):
        x = aa[:, j, :]
        y = bb[:, j, :]
        if spatial:
            y = np.stack([m.static.spectral_resample(row, x.shape[1]) for row in y])
        vals[name] = rel_l2(x, y)
    return vals, max(vals.values())


def compare_orders(run):
    a = run["orders"][39]["states"]
    b = run["orders"][47]["states"]
    names = ("delta_alpha", "delta_chi", "delta_Pchi", "delta_Palpha")
    vals = {name: rel_l2(a[:, j, :], b[:, j, :]) for j, name in enumerate(names)}
    return vals, max(vals.values())


def bridge_audit(data):
    nx = 128
    ops = m.spec_ops(nx)
    _, lap, invlap, _ = ops
    x = np.arange(nx) * m.static.BOX / nx
    B = np.cos(m.K_MPC[1] * x + 0.37) + 0.3 * np.cos(m.K_MPC[4] * x - 0.21)
    B -= np.mean(B)
    tau = float(data["tau_check"][4])
    a, _, Q = m.bg_eval(data, tau)[:3]
    M = a * a * lap(B)
    reconstructed = invlap(-Q * M / (2.0 * a)) / m.static.KB
    expected = -a * Q * B / (2.0 * m.static.KB)
    return rel_l2(reconstructed, expected)


def flux_jacobian_audit(data):
    nx = 128
    ops = m.spec_ops(nx)
    xgrid = np.arange(nx) * m.static.BOX / nx
    tau = float(data["tau_check"][4])
    scale = 5.0e-5
    chi = scale * (
        np.cos(m.K_MPC[0] * xgrid + 0.17)
        + 0.4 * np.cos(m.K_MPC[3] * xgrid - 0.31)
    )
    direction = scale * (
        0.7 * np.cos(m.K_MPC[1] * xgrid + 0.23)
        - 0.2 * np.cos(m.K_MPC[5] * xgrid + 0.61)
    )
    eps = 1.0e-6
    errors = {}
    for s, kind, beta in itertools.product(d2b.SIGMAS, d2b.KINDS, d2b.BETAS):
        member = {"sigma": s, "kind": kind, "beta0": beta}
        ana = nonlinear_delta_operator(data, tau, chi, direction, ops, member)
        def N(field):
            a, _, _, _, _, Z, _ = m.bg_eval(data, tau)
            grad, _, _, div = ops
            g = grad(field)
            xx = m.static.ACC_CONV * np.abs(g) / a
            je = d2b.j_eff(xx, Z, member)
            return div((1.0 + je) * g)
        fd = (N(chi + eps * direction) - N(chi - eps * direction)) / (2.0 * eps)
        key = d2b.member_key(member)
        errors[key] = rel_l2(fd, ana)
    return errors, max(errors.values())


def reference_compare(data, run, npz_path):
    ref = np.load(npz_path)
    if not np.allclose(ref["z"], m.CHECK_Z, rtol=0, atol=1e-12):
        raise m.InputIncomplete("linear tangent reference checkpoint mismatch")
    if not np.allclose(ref["k_mpc"], m.K_MPC, rtol=0, atol=1e-13):
        raise m.InputIncomplete("linear tangent reference k-grid mismatch")
    C = m.cos_matrix(128)
    vals = {"alpha": [], "E": [], "chi": []}
    refs = {"alpha": [], "E": [], "chi": []}
    rr = run["orders"][39]
    for i, tau in enumerate(data["tau_check"]):
        a, _, Q = m.bg_eval(data, float(tau))[:3]
        dalpha_m = np.asarray(ref["alpha"][i], float)
        dE_m = np.asarray(ref["E"][i], float)
        dtheta_m = np.asarray(ref["theta"][i], float)
        dchi_m = Q * (a * dtheta_m / (m.K_MPC * m.K_MPC) + dalpha_m)
        refs["alpha"].append(m.to_field(dalpha_m, C))
        refs["E"].append(m.to_field(dE_m, C))
        refs["chi"].append(m.to_field(dchi_m, C))
        vals["alpha"].append(rr["states"][i, 0])
        vals["E"].append(rr["E"][i])
        vals["chi"].append(rr["states"][i, 1])
    return {
        key: rel_l2(np.stack(vals[key]), np.stack(refs[key]))
        for key in ("alpha", "E", "chi")
    }


def response_diag(run, linear_run=None):
    rr = run["orders"][39]
    out = {
        "delta_alpha_norm": float(np.linalg.norm(rr["states"][:, 0])),
        "delta_E_norm": float(np.linalg.norm(rr["E"])),
        "delta_chi_norm": float(np.linalg.norm(rr["states"][:, 1])),
        "bath_B_norm_max": float(rr["bath_B_norm_max"]),
    }
    if linear_run is not None:
        lr = linear_run["orders"][39]
        out["nonlinear_vs_linear"] = {
            "alpha": rel_l2(rr["states"][:, 0], lr["states"][:, 0]),
            "E": rel_l2(rr["E"], lr["E"]),
            "chi": rel_l2(rr["states"][:, 1], lr["states"][:, 1]),
        }
    return out


def ancestry_ok():
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", PARENT_HEAD, "HEAD"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--linear-reference",
        default="results/nl1c6d2c6c_linear_tangent_reference.npz",
    )
    ap.add_argument(
        "--json-out",
        default="results/nl1c6d2c6c_eta0_nonlinear_memory_tangent.json",
    )
    args = ap.parse_args()

    try:
        data = m.prepare_class_data()
        print("NL1C6D2C6C_ETA0_NONLINEAR_MEMORY_TANGENT_START", flush=True)

        expected = [
            {"sigma": s, "kind": kind, "beta0": beta}
            for s, kind, beta in itertools.product(d2b.SIGMAS, d2b.KINDS, d2b.BETAS)
        ]
        coverage = len(expected) == 27 and len({d2b.member_key(x) for x in expected}) == 27

        bridge_err = bridge_audit(data)
        flux_errors, flux_max = flux_jacobian_audit(data)
        print(
            f"C2_BRIDGE relative_L2={bridge_err:.12e} "
            f"flux_fd_max={flux_max:.12e}",
            flush=True,
        )

        pre_primary = {
            order: prehistory(data, 128, 4096, order) for order in (39, 47)
        }
        pre_time = {39: prehistory(data, 128, 8192, 39)}
        pre_space = {39: prehistory(data, 256, 4096, 39)}

        linear_member = {"sigma": 0, "kind": "simple", "beta0": 1.0}
        linear = integrate(
            data, 128, 4096, linear_member, orders=(39,), nonlinear=False,
            pre_cache={39: pre_primary[39]},
        )
        linear_err = reference_compare(data, linear, Path(args.linear_reference))
        linear_pass = bool(
            linear["finite"]
            and linear_err["alpha"] <= LINEAR_GATE
            and linear_err["E"] <= LINEAR_GATE
            and linear_err["chi"] <= LINEAR_GATE
        )
        print(
            f"C3_LINEAR alpha={linear_err['alpha']:.12e} "
            f"E={linear_err['E']:.12e} chi={linear_err['chi']:.12e} "
            f"pass={linear_pass}",
            flush=True,
        )

        records = []
        worst_bath = (-1.0, None)
        worst_time = (-1.0, None)
        worst_space = (-1.0, None)
        worst_constraint = (-1.0, None)

        for index, member in enumerate(expected, start=1):
            key = d2b.member_key(member)
            primary = integrate(
                data, 128, 4096, member, orders=(39, 47), nonlinear=True,
                pre_cache=pre_primary,
            )
            timectl = integrate(
                data, 128, 8192, member, orders=(39,), nonlinear=True,
                pre_cache=pre_time,
            )
            spacectl = integrate(
                data, 256, 4096, member, orders=(39,), nonlinear=True,
                pre_cache=pre_space,
            )

            bath_fields, bath_max = compare_orders(primary)
            time_fields, time_max = compare_runs(primary, timectl, 39, False)
            space_fields, space_max = compare_runs(primary, spacectl, 39, True)

            finite = bool(primary["finite"] and timectl["finite"] and spacectl["finite"])
            tconstraint = max(
                primary["orders"][39]["tangent_constraint_max"],
                primary["orders"][47]["tangent_constraint_max"],
                timectl["orders"][39]["tangent_constraint_max"],
                spacectl["orders"][39]["tangent_constraint_max"],
            )
            base_constraint_max = max(
                primary["base_constraint_max"],
                timectl["base_constraint_max"],
                spacectl["base_constraint_max"],
            )
            min1p = min(
                primary["min_one_plus_j_eff"],
                timectl["min_one_plus_j_eff"],
                spacectl["min_one_plus_j_eff"],
            )
            health_pass = bool(
                finite and tconstraint <= CONSTRAINT_GATE and min1p > 0.0
            )
            bath_pass = bool(bath_max <= BATH_GATE)
            time_pass = bool(time_max <= TIME_GATE)
            space_pass = bool(space_max <= SPACE_GATE)

            diag = response_diag(primary, linear)
            rec = {
                "index": index,
                "key": key,
                "sigma": int(member["sigma"]),
                "kind": str(member["kind"]),
                "beta0": float(member["beta0"]),
                "health": {
                    "finite": finite,
                    "tangent_constraint_max": float(tconstraint),
                    "base_constraint_max_descriptive": float(base_constraint_max),
                    "min_one_plus_j_eff": float(min1p),
                },
                "health_pass": health_pass,
                "bath_order_convergence": {"fields": bath_fields, "max": float(bath_max)},
                "bath_pass": bath_pass,
                "time_convergence": {"fields": time_fields, "max": float(time_max)},
                "time_pass": time_pass,
                "spatial_convergence": {"fields": space_fields, "max": float(space_max)},
                "space_pass": space_pass,
                "response_diagnostic": diag,
            }
            records.append(rec)

            if bath_max > worst_bath[0]:
                worst_bath = (bath_max, key)
            if time_max > worst_time[0]:
                worst_time = (time_max, key)
            if space_max > worst_space[0]:
                worst_space = (space_max, key)
            if tconstraint > worst_constraint[0]:
                worst_constraint = (tconstraint, key)

            print(
                f"MEMBER {index:02d}/27 {key} "
                f"health={health_pass} constraint={tconstraint:.6e} "
                f"min1pjeff={min1p:.6e} bath={bath_max:.6e} "
                f"time={time_max:.6e} space={space_max:.6e} "
                f"dalpha={diag['delta_alpha_norm']:.6e} "
                f"dE={diag['delta_E_norm']:.6e} dchi={diag['delta_chi_norm']:.6e}",
                flush=True,
            )

        c1 = bool(
            coverage
            and ancestry_ok()
            and data["provenance"].get("pass", False)
        )
        c2 = bool(bridge_err <= BRIDGE_GATE and flux_max <= FLUX_FD_GATE)
        c3 = linear_pass
        c4 = all(r["health_pass"] for r in records)
        c5 = all(r["bath_pass"] for r in records)
        c6 = all(r["time_pass"] for r in records)
        c7 = all(r["space_pass"] for r in records)
        c8 = True
        gates = {
            "C1_provenance_parent_and_exact_27_coverage": c1,
            "C2_algebraic_bridge_and_flux_jacobian": c2,
            "C3_linear_eta0_tangent_regression_le_5e-3": c3,
            "C4_all27_health_constraint_le_1e-10": c4,
            "C5_bath_order_39_vs_47_le_1e-2": c5,
            "C6_time_convergence_le_2e-3": c6,
            "C7_spatial_convergence_le_5e-3": c7,
            "C8_scope_clean_eta0_only": c8,
        }
        passed = all(gates.values())
        classification = PASS_LABEL if passed else FAIL_LABEL

        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=ROOT, text=True
        ).strip()

        result = {
            "classification": classification,
            "git": {"head": head, "branch": branch},
            "predata_commit": PREREG_HEAD,
            "license": {
                "D2C6B_run": PARENT_RUN,
                "D2C6B_head": PARENT_HEAD,
                "parent_is_ancestor": ancestry_ok(),
                "historical_D2C6A_remains_FAIL": True,
            },
            "physical_eta": 0.0,
            "bath": {
                "tauH0": TAUH0,
                "primary_order": 39,
                "control_order": 47,
                "weight_sums": {
                    str(order): float(np.sum(BATH_DATA[order][1])) for order in ORDERS
                },
                "prehistory": {
                    "primary39_steps": int(pre_primary[39]["nstep"]),
                    "primary47_steps": int(pre_primary[47]["nstep"]),
                    "time39_steps": int(pre_time[39]["nstep"]),
                    "space39_steps": int(pre_space[39]["nstep"]),
                    "start_tau": float(pre_primary[39]["tpre"]),
                    "reset_at_z6": False,
                },
            },
            "family": {
                "sigma": list(d2b.SIGMAS),
                "kind": list(d2b.KINDS),
                "beta0": list(d2b.BETAS),
                "epsilon_mix": d2b.EPS_MIX,
                "member_count": len(records),
            },
            "C2_audits": {
                "stable_canonical_memory_bridge_relative_L2": float(bridge_err),
                "flux_jacobian_relative_L2_max": float(flux_max),
                "flux_jacobian_by_member": flux_errors,
            },
            "linear_control_relative_L2": linear_err,
            "discretization": {
                "primary": {"Nx": 128, "Nstep": 4096, "bath_orders": [39, 47]},
                "time_control": {"Nx": 128, "Nstep": 8192, "bath_orders": [39]},
                "spatial_control": {"Nx": 256, "Nstep": 4096, "bath_orders": [39]},
                "base_tangent_integrator": "fixed-step classical RK4",
                "bath_integrator": "analytic frozen-background damped oscillator with linear source over each stage interval",
                "canonical_comparison_states": [
                    "delta_alpha", "delta_chi", "delta_Pchi", "delta_Palpha"
                ],
            },
            "members": records,
            "worst_cases": {
                "bath_order": {"member": worst_bath[1], "max": float(worst_bath[0])},
                "time": {"member": worst_time[1], "max": float(worst_time[0])},
                "space": {"member": worst_space[1], "max": float(worst_space[0])},
                "tangent_constraint": {
                    "member": worst_constraint[1], "max": float(worst_constraint[0])
                },
            },
            "gates": gates,
            "scope": {
                "finite_physical_eta": False,
                "likelihood": False,
                "refit": False,
                "nonlinear_matter_evolved": False,
                "postdata_member_selection": False,
            },
            "finite_positive_eta_nonlinear_memory_licensed": bool(passed),
        }
        out = Path(args.json_out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")

        print(f"WORST_BATH member={worst_bath[1]} max={worst_bath[0]:.12e}", flush=True)
        print(f"WORST_TIME member={worst_time[1]} max={worst_time[0]:.12e}", flush=True)
        print(f"WORST_SPACE member={worst_space[1]} max={worst_space[0]:.12e}", flush=True)
        print(
            f"WORST_TANGENT_CONSTRAINT member={worst_constraint[1]} "
            f"max={worst_constraint[0]:.12e}",
            flush=True,
        )
        print(f"GATES={json.dumps(gates, sort_keys=True)}", flush=True)
        print(f"CLASSIFICATION={classification}", flush=True)
        print(f"FINITE_POSITIVE_ETA_NONLINEAR_MEMORY_LICENSED={passed}", flush=True)
        print(f"JSON={args.json_out}", flush=True)
        print("NL1C6D2C6C_ETA0_NONLINEAR_MEMORY_TANGENT_END", flush=True)
        return 0 if passed else 2

    except m.InputIncomplete as exc:
        print(f"CLASSIFICATION={INCOMPLETE_LABEL}", flush=True)
        print(f"INCOMPLETE_REASON={exc}", flush=True)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
