#!/usr/bin/env python3
from __future__ import annotations

# D2C6C-R3: restore the originally preregistered full retarded prehistory.
# Each frozen CLASS mode is propagated independently from its own valid tau_lo
# to the common z=6 time, then the linear bath/tangent contributions are summed.
# Post-z=6 equations, gates, bath orders, physical eta and discretizations are
# unchanged. R1 parser compatibility is inherited unchanged.

import math
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from nl1c6d2c6c import r1_tau1_parser_compat as r1compat

c = r1compat.c


def _single_mode_data(data, index):
    """Shallow data view whose background a(tau) is evaluated from mode index."""
    out = dict(data)
    out["modes"] = [data["modes"][index]]
    return out


def _mode_chi_field(data, mode_data, index, tau, C):
    """One frozen CLASS mode's contribution to chi in the real-space box."""
    md = data["modes"][index]
    a, _, Q = c.m.bg_eval(mode_data, tau)[:3]
    alpha = float(md["splines"]["alpha"](tau))
    theta = float(md["splines"]["theta"](tau))
    k = float(c.m.K_MPC[index])
    chi_mode = Q * (a * theta / (k * k) + alpha)
    return chi_mode * C[index]


def prehistory_modewise(data, nx, nstep_main, order):
    C = c.m.cos_matrix(nx)
    ops = c.m.spec_ops(nx)
    t0 = float(data["t0"])
    hmain = (float(data["t1"]) - t0) / float(nstep_main)

    omega, _ = c.BATH_DATA[order]
    q_total = np.zeros((len(omega), nx), float)
    p_total = np.zeros_like(q_total)
    v_total = np.zeros((4, nx), float)

    starts = []
    step_counts = []

    for index, md in enumerate(data["modes"]):
        tpre = float(md["tau_lo"])
        if tpre > t0 + 1.0e-12:
            raise c.m.InputIncomplete(
                f"R3 mode {index} linear history begins after z=6"
            )

        mode_data = _single_mode_data(data, index)
        q = np.zeros_like(q_total)
        p = np.zeros_like(p_total)
        v = np.zeros_like(v_total)

        if abs(t0 - tpre) <= 1.0e-12:
            npre = 0
        else:
            npre = max(1, int(math.ceil((t0 - tpre) / hmain)))
            h = (t0 - tpre) / float(npre)

            for istep in range(npre):
                t = tpre + istep * h
                th = t + 0.5 * h
                tn = t0 if istep + 1 == npre else tpre + (istep + 1) * h

                chi0 = _mode_chi_field(data, mode_data, index, t, C)
                chih = _mode_chi_field(data, mode_data, index, th, C)
                chin = _mode_chi_field(data, mode_data, index, tn, C)

                a0 = c.m.bg_eval(mode_data, t)[0]
                ah = c.m.bg_eval(mode_data, th)[0]
                an = c.m.bg_eval(mode_data, tn)[0]
                s0 = chi0 / a0
                sh = chih / ah
                sn = chin / an

                k1 = c.tangent_rhs(
                    mode_data, t, chi0, v, q, ops, None, False, order
                )
                q2, p2 = c.bath_advance(
                    mode_data, t, th, q, p, s0, sh, order
                )
                v2 = v + 0.5 * h * k1

                k2 = c.tangent_rhs(
                    mode_data, th, chih, v2, q2, ops, None, False, order
                )
                q3, p3 = c.bath_advance(
                    mode_data, t, th, q, p, s0, sh, order
                )
                v3 = v + 0.5 * h * k2

                k3 = c.tangent_rhs(
                    mode_data, th, chih, v3, q3, ops, None, False, order
                )
                q4, p4 = c.bath_advance(
                    mode_data, t, tn, q, p, s0, sn, order
                )
                v4 = v + h * k3

                k4 = c.tangent_rhs(
                    mode_data, tn, chin, v4, q4, ops, None, False, order
                )
                vn = v + (h / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
                qn, pn = c.bath_advance(
                    mode_data, t, tn, q, p, s0, sn, order
                )

                if not (
                    np.all(np.isfinite(vn))
                    and np.all(np.isfinite(qn))
                    and np.all(np.isfinite(pn))
                ):
                    raise FloatingPointError(
                        f"R3 nonfinite prehistory mode={index} "
                        f"step={istep + 1}/{npre}"
                    )

                v, q, p = vn, qn, pn

        q_total += q
        p_total += p
        v_total += v
        starts.append(tpre)
        step_counts.append(int(npre))

    print(
        "R3_MODEWISE_PREHISTORY "
        f"order={order} nx={nx} nstep_main={nstep_main} "
        f"tau_lo={','.join(f'{x:.12e}' for x in starts)} "
        f"npre={','.join(str(x) for x in step_counts)}",
        flush=True,
    )

    return {
        "q": q_total,
        "p": p_total,
        "v": v_total,
        "tpre": float(min(starts)),
        "nstep": int(sum(step_counts)),
        "mode_tau_lo": starts,
        "mode_nstep": step_counts,
    }


c.prehistory = prehistory_modewise

if __name__ == "__main__":
    raise SystemExit(c.main())
