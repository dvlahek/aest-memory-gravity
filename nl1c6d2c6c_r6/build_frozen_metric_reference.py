#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from nl1c6d2c6c import r3_modewise_full_prehistory as r3
from nl1c6d2c6c_r5 import build_zero_safe_reference as r5ref
from nl1c6d2n import exp_normalization_audit as norm

c = r3.c
m = c.m
KB = float(m.static.KB)
A = 2.0 - KB
ORDER = 39
TAUH0 = 1.0


def load_force_table(path: Path):
    rows = []
    for line in path.read_text().splitlines():
        p = line.split()
        if len(p) != 3:
            continue
        k, tau, f = map(float, p)
        if math.isfinite(k) and math.isfinite(tau) and math.isfinite(f):
            rows.append((k, tau, f))
    if not rows:
        raise RuntimeError("R6 force table is empty")

    grouped = []
    for target in np.asarray(m.K_MPC, float):
        hit = [(t, f) for k, t, f in rows if abs(k-target) <= 2e-12*max(abs(target), 1.0)]
        if len(hit) < 8:
            raise RuntimeError(f"insufficient force rows for k={target:.17g}: {len(hit)}")
        hit.sort()
        tt = np.asarray([q[0] for q in hit], float)
        ff = np.asarray([q[1] for q in hit], float)
        keep = np.ones(tt.size, dtype=bool)
        keep[1:] = np.diff(tt) > 0.0
        tt, ff = tt[keep], ff[keep]
        if tt.size < 8 or not np.all(np.diff(tt) > 0.0):
            raise RuntimeError(f"invalid force time grid for k={target:.17g}")
        grouped.append((tt, ff))
    return grouped


def fluid_background(data, tau: float):
    a, H, Q, KQ, KQQ, Z, _ = m.bg_eval(data, float(tau))
    q2, K, kq2, kqq2 = norm.exp_eval(float(Z))
    checks = (
        abs(q2-Q) / max(abs(Q), 1e-300),
        abs(kq2-KQ) / max(abs(KQ), 1e-300),
        abs(kqq2-KQQ) / max(abs(KQQ), 1e-300),
    )
    if max(checks) > 2e-10:
        raise RuntimeError(f"corrected Exp background mismatch at tau={tau}: {checks}")
    rho = (Q*KQ-K) / 3.0
    p = K / 3.0
    w = p / rho
    cad2 = KQ / (Q*KQQ)
    vals = (a, H, Q, KQ, KQQ, K, rho, p, w, cad2)
    if not np.all(np.isfinite(vals)) or a <= 0.0 or rho <= 0.0 or (1.0+w) <= 0.0:
        raise FloatingPointError(f"invalid frozen background at tau={tau}")
    return a, H, Q, KQ, rho, w, cad2


def force_at(tau: float, tt: np.ndarray, ff: np.ndarray):
    if tau <= tt[0]:
        return 0.0 if tau < tt[0]-1e-12 else float(ff[0])
    if tau >= tt[-1]:
        return float(ff[-1])
    j = int(np.searchsorted(tt, tau, side="right") - 1)
    j = max(0, min(j, tt.size-2))
    x = (tau-tt[j])/(tt[j+1]-tt[j])
    return float(ff[j] + x*(ff[j+1]-ff[j]))


def rhs(data, tau: float, u: np.ndarray, k: float, tt: np.ndarray, ff: np.ndarray):
    ddelta, dtheta, dalpha, dE = [float(x) for x in u]
    a, H, Q, KQ, rho, w, cad2 = fluid_background(data, tau)
    k2 = k*k
    dchi = Q*(a*dtheta/k2 + dalpha)
    dPi = cad2*ddelta + cad2*k2/(3.0*a*a*rho)*(KB*dE + A*dchi)
    ah = a*H

    out = np.empty(4, float)
    out[0] = 3.0*ah*(w*ddelta-dPi) - (1.0+w)*dtheta
    out[1] = (3.0*cad2-1.0)*ah*dtheta + k2*dPi/(1.0+w)
    out[2] = a*dE
    Erhs = KQ*dchi - A*(
        Q*dPi/(1.0+w)
        + (H+Q)*dchi
        - 3.0*cad2*H*Q*dalpha
    )
    out[3] = a*Erhs/KB - ah*dE + force_at(tau, tt, ff)
    if not np.all(np.isfinite(out)):
        raise FloatingPointError(f"nonfinite R6 tangent RHS at tau={tau}, k={k}")
    return out


def rk4_step(data, t: float, u: np.ndarray, h: float, k: float, tt, ff):
    k1 = rhs(data, t, u, k, tt, ff)
    k2 = rhs(data, t+0.5*h, u+0.5*h*k1, k, tt, ff)
    k3 = rhs(data, t+0.5*h, u+0.5*h*k2, k, tt, ff)
    k4 = rhs(data, t+h, u+h*k3, k, tt, ff)
    return u + (h/6.0)*(k1+2.0*k2+2.0*k3+k4)


def integrate_mode(data, j: int, tt: np.ndarray, ff: np.ndarray, hmax: float):
    k = float(m.K_MPC[j])
    t = float(data["modes"][j]["tau_lo"])
    targets = np.asarray(data["tau_check"], float)
    if not (tt[0] <= t + 1e-9 and t < targets[0] and tt[-1] >= targets[-1]-1e-9):
        raise RuntimeError(
            f"mode {j} history/force coverage invalid: t={t}, force={tt[0]}..{tt[-1]}, checkpoints={targets[0]}..{targets[-1]}"
        )
    u = np.zeros(4, float)
    saved = []
    total_steps = 0
    for target in targets:
        target = float(target)
        span = target-t
        if span < -1e-10:
            raise RuntimeError(f"mode {j} checkpoint ordering failure")
        if span > 1e-13:
            n = max(1, int(math.ceil(span/hmax)))
            h = span/n
            for _ in range(n):
                u = rk4_step(data, t, u, h, k, tt, ff)
                t += h
                total_steps += 1
            t = target
        saved.append(u.copy())
    arr = np.stack(saved)
    print(
        f"R6_MODE mode={j} k_mpc={k:.12e} start_tau={data['modes'][j]['tau_lo']:.12e} "
        f"steps={total_steps} alpha_end={arr[-1,2]:.12e} E_end={arr[-1,3]:.12e} theta_end={arr[-1,1]:.12e}",
        flush=True,
    )
    return arr, total_steps


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="results/c3_r6_frozen_metric_reference.npz")
    ap.add_argument("--meta-out", default="results/c3_r6_frozen_metric_reference.json")
    ap.add_argument("--force-out", default="results/c3_r6_eta0_force39.dat")
    args = ap.parse_args()

    try:
        out = Path(args.out)
        meta = Path(args.meta_out)
        force_path = Path(args.force_out)
        out.parent.mkdir(parents=True, exist_ok=True)

        data = m.prepare_class_data()
        mode_stats, bath_audits = r5ref.make_force_table(data, force_path)
        forces = load_force_table(force_path)
        hmax = (float(data["t1"])-float(data["t0"]))/4096.0
        if not (math.isfinite(hmax) and hmax > 0.0):
            raise RuntimeError("invalid frozen D2C6C main step")

        # Directly audit the corrected background coefficients used in the
        # frozen-metric CLASS-variable variational equations.
        bg_rel_max = 0.0
        for tau in np.linspace(float(data["t0"]), float(data["t1"]), 17):
            a, H, Q, KQ, KQQ, Z, _ = m.bg_eval(data, float(tau))
            q2, _, kq2, kqq2 = norm.exp_eval(float(Z))
            bg_rel_max = max(
                bg_rel_max,
                abs(q2-Q)/max(abs(Q),1e-300),
                abs(kq2-KQ)/max(abs(KQ),1e-300),
                abs(kqq2-KQQ)/max(abs(KQQ),1e-300),
            )
            fluid_background(data, float(tau))

        states = []
        steps = []
        for j, (tt, ff) in enumerate(forces):
            arr, ns = integrate_mode(data, j, tt, ff, hmax)
            states.append(arr)
            steps.append(ns)
        # [mode, checkpoint, state] -> [checkpoint, mode]
        U = np.stack(states, axis=0)
        alpha = U[:,:,2].T
        E = U[:,:,3].T
        theta = U[:,:,1].T
        if not (np.all(np.isfinite(alpha)) and np.all(np.isfinite(E)) and np.all(np.isfinite(theta))):
            raise FloatingPointError("nonfinite R6 reference arrays")

        np.savez_compressed(
            out,
            z=np.asarray(m.CHECK_Z, float),
            a=1.0/(1.0+np.asarray(m.CHECK_Z, float)),
            k_mpc=np.asarray(m.K_MPC, float),
            alpha=alpha,
            E=E,
            theta=theta,
        )
        report = {
            "classification": "C3_R6_FROZEN_METRIC_CLASS_VARIABLE_REFERENCE_READY",
            "historical_R2_R3_R4_R5_remain_fail": True,
            "finite_positive_eta_licensed": False,
            "physical_eta": 0.0,
            "tauH0": TAUH0,
            "bath_order": ORDER,
            "external_metric_tangent_frozen": True,
            "full_CLASS_Einstein_feedback": False,
            "initial_tangent": "zero at each mode earliest retained CLASS history time",
            "integrator": "independent per-mode RK4, exact checkpoint endpoints",
            "hmax": float(hmax),
            "steps_per_mode": [int(x) for x in steps],
            "background_exp_rel_max": float(bg_rel_max),
            "bath_force_audits": bath_audits,
            "bath_force_mode_stats": mode_stats,
            "equations": "direct variational form of patched CLASS AeST delta/theta/alpha/E block with metric tangent terms set to zero",
        }
        meta.write_text(json.dumps(report, indent=2, sort_keys=True)+"\n")
        print(f"R6_BACKGROUND_EXP_REL_MAX={bg_rel_max:.12e}", flush=True)
        print("CLASSIFICATION=C3_R6_FROZEN_METRIC_CLASS_VARIABLE_REFERENCE_READY", flush=True)
        print("FINITE_POSITIVE_ETA_NONLINEAR_MEMORY_LICENSED=False", flush=True)
        return 0
    except Exception as exc:
        print(f"C3_R6_REFERENCE_ERROR {type(exc).__name__}: {exc}", flush=True)
        print("CLASSIFICATION=C3_R6_FROZEN_METRIC_REFERENCE_INCOMPLETE", flush=True)
        print("FINITE_POSITIVE_ETA_NONLINEAR_MEMORY_LICENSED=False", flush=True)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
