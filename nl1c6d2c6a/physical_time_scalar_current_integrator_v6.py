#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from nl1c6d2c6a import physical_time_scalar_current_integrator_v5 as v5

m = v5.m


def integrate_fixed_grid(data, nx, nstep, nonlinear, collect_stats=False):
    """Same preregistered RK4 integrator with exact fixed-grid time labels.

    The only change relative to the original D2C6A implementation is endpoint
    bookkeeping: t_n is formed from t0+n*h and the final label is exactly t1,
    preventing accumulated floating-point addition from dropping z=0.2.
    """
    y, init = m.initial_state(data, nx)
    C = m.cos_matrix(nx)
    ops = m.spec_ops(nx)
    t0, t1 = data["t0"], data["t1"]
    h = (t1 - t0) / nstep
    tchecks = data["tau_check"]
    ck = []
    ci = 0
    stats_x = []
    jmax = -np.inf
    onejmin = np.inf
    max_constraint = 0.0

    def store(t, ycur):
        nonlocal jmax, onejmin, max_constraint
        E, cr, x, j = m.checkpoint_health(data, t, ycur, ops)
        max_constraint = max(max_constraint, cr)
        ck.append({"tau": float(t), "y": ycur.copy(), "E": E.copy(), "constraint": cr})

    store(t0, y)
    ci = 1
    if collect_stats:
        _, _, x, j = m.checkpoint_health(data, t0, y, ops)
        stats_x.append(x.copy())
        jmax = max(jmax, float(np.max(j)))
        onejmin = min(onejmin, float(np.min(1 + j)))

    finite = True
    fail_reason = None
    for istep in range(nstep):
        t = t0 + istep * h
        tn = t1 if (istep + 1) == nstep else (t0 + (istep + 1) * h)

        k1 = m.rhs(data, t, y, ops, C, nonlinear)
        k2 = m.rhs(data, t + 0.5 * h, y + 0.5 * h * k1, ops, C, nonlinear)
        k3 = m.rhs(data, t + 0.5 * h, y + 0.5 * h * k2, ops, C, nonlinear)
        k4 = m.rhs(data, t + h, y + h * k3, ops, C, nonlinear)
        yn = y + (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)

        if not np.all(np.isfinite(yn)):
            finite = False
            fail_reason = f"nonfinite_state_step_{istep + 1}"
            break

        while ci < len(tchecks) and tchecks[ci] <= tn + 1e-10:
            frac = float((tchecks[ci] - t) / h)
            frac = min(1.0, max(0.0, frac))
            yc = y + frac * (yn - y)
            store(float(tchecks[ci]), yc)
            ci += 1

        y = yn
        if collect_stats and (istep + 1) % 8 == 0:
            _, _, x, j = m.checkpoint_health(data, tn, y, ops)
            stats_x.append(x.copy())
            jmax = max(jmax, float(np.max(j)))
            onejmin = min(onejmin, float(np.min(1 + j)))

    if finite and ci != len(tchecks):
        finite = False
        fail_reason = f"stored_only_{ci}_of_{len(tchecks)}_checkpoints"

    arr = None
    if ck:
        arr = np.stack([q["y"] for q in ck])

    stats = {
        "finite": finite,
        "fail_reason": fail_reason,
        "max_constraint": float(max_constraint),
        "init": init,
    }
    if collect_stats and stats_x:
        xx = np.concatenate(stats_x)
        stats.update({
            "x_max": float(np.max(xx)),
            "x_p01": float(np.percentile(xx, 1)),
            "x_p50": float(np.percentile(xx, 50)),
            "x_p99": float(np.percentile(xx, 99)),
            "x_frac_lt1": float(np.mean(xx < 1)),
            "x_frac_1_10": float(np.mean((xx >= 1) & (xx < 10))),
            "x_frac_ge10": float(np.mean(xx >= 10)),
            "j_max": float(jmax),
            "one_plus_j_min": float(onejmin),
            "n_x_samples": int(xx.size),
        })
    return {"states": arr, "checkpoints": ck, "stats": stats}


m.integrate = integrate_fixed_grid

if __name__ == "__main__":
    raise SystemExit(m.main())
