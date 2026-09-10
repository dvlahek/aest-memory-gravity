#!/usr/bin/env python3
from __future__ import annotations

import argparse
import itertools
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from nl1c6d2c6ar1 import stable_canonical_integrator as r1

m = r1.m

SIGMAS = (-1, 0, 1)
KINDS = ("simple", "exponential", "sharp")
BETAS = (1.0, 0.5, 0.1)
EPS_MIX = 0.25

PASS_LABEL = "NL1C6D2C6B_ALL27_PHYSICAL_NONLINEAR_TRAJECTORIES_PASS"
FAIL_LABEL = "NL1C6D2C6B_ALL27_PHYSICAL_NONLINEAR_TRAJECTORIES_FAIL"
INCOMPLETE_LABEL = "NL1C6D2C6B_ALL27_PHYSICAL_NONLINEAR_TRAJECTORIES_INCOMPLETE"

_CURRENT_MEMBER = {"sigma": 0, "kind": "simple", "beta0": 1.0}


def member_tuple(member):
    return int(member["sigma"]), str(member["kind"]), float(member["beta0"])


def member_key(member):
    sigma, kind, beta = member_tuple(member)
    return f"sigma={sigma:+d}|kind={kind}|beta0={beta:g}"


def set_member(member):
    global _CURRENT_MEMBER
    _CURRENT_MEMBER = {
        "sigma": int(member["sigma"]),
        "kind": str(member["kind"]),
        "beta0": float(member["beta0"]),
    }


def j_eff(x, Z, member=None):
    if member is None:
        member = _CURRENT_MEMBER
    sigma, kind, beta = member_tuple(member)
    xx = np.asarray(x, float)
    j, _ = m.static.j_and_prime(xx, beta, kind, saturated=False)
    sx = xx**2 / (1.0 + xx**2)
    mix = 1.0 + sigma * EPS_MIX * sx * (np.tanh(float(Z)) ** 2)
    return j * mix


def rhs_member(data, tau, y, ops, C, nonlinear):
    E, b = r1.derive_E_stable(data, tau, y, ops)
    a, H, Q, KQ, KQQ, Z, Qdot = b
    alpha, chi, pchi, S = y
    grad, lap, _, div = ops

    U = pchi / (2.0 * a**3 * KQQ)
    psi = m.to_field(m.mode_values(data, tau, "psi"), C)

    if nonlinear:
        g = grad(chi)
        x = m.static.ACC_CONV * np.abs(g) / a
        je = j_eff(x, Z)
        nl = div((1.0 + je) * g)
    else:
        nl = lap(chi)

    dalpha = a * (E - psi)
    dchi = a * (U + Q * E + Qdot * alpha)
    dpchi = a * (
        -2.0 * m.A * a * lap(E)
        + 2.0 * m.A * a * nl
        - 2.0 * a * KQ * lap(alpha)
    )
    dS = a * (
        -2.0 * a * KQ * lap(chi)
        - 2.0 * m.A * a * Q * lap(E)
        + 2.0 * m.A * a * Q * nl
    )
    return np.stack([dalpha, dchi, dpchi, dS])


def checkpoint_health_member(data, tau, y, ops):
    E, b = r1.derive_E_stable(data, tau, y, ops)
    a, H, Q, KQ, KQQ, Z, Qdot = b
    alpha, chi, pchi, S = y
    grad, lap, _, _ = ops

    rhs0 = -2.0 * a * m.static.KB * lap(E) - 2.0 * m.A * a * lap(chi)
    cr = m.norm_residual(S - rhs0, S, rhs0)
    g = grad(chi)
    x = m.static.ACC_CONV * np.abs(g) / a
    je = j_eff(x, Z)
    return E, cr, x, je


# Keep the validated R1 stable variables/integrator. Only the D2C5-licensed
# projected nonlinear scalar-current constitutive factor is member-dependent.
m.initial_state = r1.initial_state_stable
m.derive_E = r1.derive_E_stable
m.rhs = rhs_member
m.checkpoint_health = checkpoint_health_member
m.integrate = r1.integrate_stable


def postscan_health(data, run, nx):
    ops = m.spec_ops(nx)
    max_constraint = 0.0
    min_one_plus = np.inf
    finite = bool(run["stats"]["finite"])
    for cp in run["checkpoints"]:
        E, cr, x, je = checkpoint_health_member(data, float(cp["tau"]), cp["y"], ops)
        vals = (E, x, je, cp["y"])
        finite = finite and all(np.all(np.isfinite(v)) for v in vals) and np.isfinite(cr)
        max_constraint = max(max_constraint, float(cr))
        min_one_plus = min(min_one_plus, float(np.min(1.0 + je)))
    return {
        "finite": bool(finite),
        "max_constraint": float(max_constraint),
        "min_one_plus_j_eff": float(min_one_plus),
    }


def physical_field(run, name):
    if name == "alpha":
        return np.asarray(run["states"][:, 0, :], float)
    if name == "chi":
        return np.asarray(run["states"][:, 1, :], float)
    if name == "E":
        return np.stack([np.asarray(cp["E"], float) for cp in run["checkpoints"]])
    raise ValueError(name)


def summarize_response(records):
    out = {}
    for field in ("alpha", "E", "chi"):
        pairs = [(float(rec["response"][field]), rec["key"]) for rec in records]
        values = np.asarray([x[0] for x in pairs], float)
        imin = int(np.argmin(values))
        imax = int(np.argmax(values))
        out[field] = {
            "min": float(values[imin]),
            "min_member": pairs[imin][1],
            "median": float(np.median(values)),
            "max": float(values[imax]),
            "max_member": pairs[imax][1],
        }
    return out


def completion_diagnostics(records, primary_runs):
    by_tuple = {
        (rec["sigma"], rec["kind"], rec["beta0"]): rec
        for rec in records
    }
    out = []
    for kind in KINDS:
        for beta in BETAS:
            block = [by_tuple[(sigma, kind, beta)] for sigma in SIGMAS]
            nblock = max(
                max(float(rec["time_convergence"]["max"]), float(rec["spatial_convergence"]["max"]))
                for rec in block
            )
            ref_rec = by_tuple[(0, kind, beta)]
            ref_run = primary_runs[ref_rec["key"]]
            entry = {
                "kind": kind,
                "beta0": float(beta),
                "N_block": float(nblock),
                "sigma_displacements": {},
            }
            for sigma in (-1, 1):
                rec = by_tuple[(sigma, kind, beta)]
                run = primary_runs[rec["key"]]
                vals = {}
                for field in ("alpha", "E", "chi"):
                    c = m.rel_l2(physical_field(run, field), physical_field(ref_run, field))
                    vals[field] = {
                        "C": float(c),
                        "resolved_gt_10N_block": bool(c > 10.0 * nblock),
                    }
                entry["sigma_displacements"][str(sigma)] = vals
            out.append(entry)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--json-out",
        default="results/nl1c6d2c6b_all27_physical_nonlinear_trajectories.json",
    )
    args = ap.parse_args()

    try:
        data = m.prepare_class_data()
        print("NL1C6D2C6B_ALL27_PHYSICAL_NONLINEAR_TRAJECTORIES_START", flush=True)

        expected = [
            {"sigma": s, "kind": k, "beta0": b}
            for s, k, b in itertools.product(SIGMAS, KINDS, BETAS)
        ]
        coverage = len(expected) == 27 and len({member_key(q) for q in expected}) == 27

        set_member({"sigma": 0, "kind": "simple", "beta0": 1.0})
        _, init = m.initial_state(data, 128)
        i2 = max(
            float(init["elliptic_residual"]),
            float(init["pchi_definition_residual"]),
            max(float(v) for v in init["zero_mode_relative"].values()),
        )
        initial_pass = bool(i2 <= m.INITIAL_GATE and init["all_finite"])

        linear = m.integrate(data, 128, 4096, False, collect_stats=False)
        linear_err = m.linear_class_compare(data, linear, 128)
        linear_pass = bool(
            linear["stats"]["finite"]
            and linear_err["alpha"] <= m.LINEAR_GATE
            and linear_err["E"] <= m.LINEAR_GATE
            and linear_err["chi"] <= m.LINEAR_GATE
        )
        print(
            f"B2_SHARED initial={i2:.12e} initial_pass={initial_pass} "
            f"linear_alpha={linear_err['alpha']:.12e} "
            f"linear_E={linear_err['E']:.12e} "
            f"linear_chi={linear_err['chi']:.12e} linear_pass={linear_pass}",
            flush=True,
        )

        records = []
        primary_runs = {}
        for index, member in enumerate(expected, start=1):
            set_member(member)
            key = member_key(member)

            primary = m.integrate(data, 128, 4096, True, collect_stats=True)
            timectl = m.integrate(data, 128, 8192, True, collect_stats=False)
            spacectl = m.integrate(data, 256, 4096, True, collect_stats=False)

            time_fields, time_max = m.compare_state_runs(primary, timectl, False)
            space_fields, space_max = m.compare_state_runs(primary, spacectl, True)
            response = m.nonlinear_linear_diag(primary, linear)

            hp = postscan_health(data, primary, 128)
            ht = postscan_health(data, timectl, 128)
            hs = postscan_health(data, spacectl, 256)
            health = {
                "finite": bool(hp["finite"] and ht["finite"] and hs["finite"]),
                "max_constraint": float(
                    max(hp["max_constraint"], ht["max_constraint"], hs["max_constraint"])
                ),
                "min_one_plus_j_eff": float(
                    min(
                        hp["min_one_plus_j_eff"],
                        ht["min_one_plus_j_eff"],
                        hs["min_one_plus_j_eff"],
                    )
                ),
            }
            health_pass = bool(
                health["finite"]
                and health["max_constraint"] <= m.CONSTRAINT_GATE
                and health["min_one_plus_j_eff"] > 0.0
            )
            time_pass = bool(time_max <= m.TIME_GATE)
            space_pass = bool(space_max <= m.SPACE_GATE)
            member_pass = bool(health_pass and time_pass and space_pass)

            stats = primary["stats"]
            rec = {
                "index": index,
                "key": key,
                "sigma": int(member["sigma"]),
                "kind": str(member["kind"]),
                "beta0": float(member["beta0"]),
                "health": health,
                "health_pass": health_pass,
                "time_convergence": {"fields": time_fields, "max": float(time_max)},
                "time_pass": time_pass,
                "spatial_convergence": {"fields": space_fields, "max": float(space_max)},
                "space_pass": space_pass,
                "response": {k: float(v) for k, v in response.items()},
                "gradient_diagnostics": {
                    "x_max": float(stats.get("x_max", np.nan)),
                    "x_p01": float(stats.get("x_p01", np.nan)),
                    "x_p50": float(stats.get("x_p50", np.nan)),
                    "x_p99": float(stats.get("x_p99", np.nan)),
                    "x_frac_lt1": float(stats.get("x_frac_lt1", np.nan)),
                    "x_frac_1_10": float(stats.get("x_frac_1_10", np.nan)),
                    "x_frac_ge10": float(stats.get("x_frac_ge10", np.nan)),
                    "j_eff_max": float(stats.get("j_max", np.nan)),
                    "min_one_plus_j_eff_dense": float(stats.get("one_plus_j_min", np.nan)),
                    "n_x_samples": int(stats.get("n_x_samples", 0)),
                },
                "pass": member_pass,
            }
            records.append(rec)
            primary_runs[key] = primary

            print(
                f"MEMBER {index:02d}/27 sigma={member['sigma']:+d} "
                f"kind={member['kind']} beta0={member['beta0']:g} "
                f"health={health_pass} constraint={health['max_constraint']:.6e} "
                f"min1pjeff={health['min_one_plus_j_eff']:.6e} "
                f"time={time_max:.6e} time_pass={time_pass} "
                f"space={space_max:.6e} space_pass={space_pass} "
                f"Ralpha={response['alpha']:.6e} RE={response['E']:.6e} "
                f"Rchi={response['chi']:.6e}",
                flush=True,
            )

        response_summary = summarize_response(records)
        completion = completion_diagnostics(records, primary_runs)

        b1 = bool(coverage and data["provenance"].get("pass", False))
        b2 = bool(initial_pass and linear_pass)
        b3 = all(rec["health_pass"] for rec in records)
        b4 = all(rec["time_pass"] for rec in records)
        b5 = all(rec["space_pass"] for rec in records)
        b6 = True
        gates = {
            "B1_provenance_and_exact_27_coverage": b1,
            "B2_shared_initial_and_linear_regression": b2,
            "B3_all27_trajectory_health": b3,
            "B4_all27_timestep_convergence_le_2e-3": b4,
            "B5_all27_spatial_convergence_le_5e-3": b5,
            "B6_scope_clean": b6,
        }
        passed = all(gates.values())
        classification = PASS_LABEL if passed else FAIL_LABEL

        worst_time = max(records, key=lambda r: r["time_convergence"]["max"])
        worst_space = max(records, key=lambda r: r["spatial_convergence"]["max"])
        worst_constraint = max(records, key=lambda r: r["health"]["max_constraint"])

        out = {
            "classification": classification,
            "predata_commits": [
                "401091aecf602e31e4de0e0f779133fd6fe14112",
                "908bdf00953506d85e41b2fdb753268134332871",
            ],
            "license": {
                "D2C6AR1_run": 34445918519,
                "D2C6AR1_head": "6f9defb69566c33b2190c0765ef50df5e787d4d7",
                "historical_D2C6A_remains_FAIL": True,
            },
            "family": {
                "sigma": list(SIGMAS),
                "kind": list(KINDS),
                "beta0": list(BETAS),
                "epsilon_mix": EPS_MIX,
                "member_count": len(records),
            },
            "shared_initial": {
                "max_gate_metric": float(i2),
                "elliptic_residual": float(init["elliptic_residual"]),
                "pchi_definition_residual": float(init["pchi_definition_residual"]),
                "zero_mode_relative": {
                    k: float(v) for k, v in init["zero_mode_relative"].items()
                },
                "cancellation_ratio": float(init.get("cancellation_ratio", np.nan)),
            },
            "shared_linear_control_relative_L2": {
                k: float(v) for k, v in linear_err.items()
            },
            "discretization": {
                "primary": {"Nx": 128, "Nstep": 4096},
                "time_control": {"Nx": 128, "Nstep": 8192},
                "spatial_control": {"Nx": 256, "Nstep": 4096},
                "integrator": "fixed-step classical RK4",
                "convergence_states": ["alpha", "chi", "P_chi", "P_alpha"],
            },
            "members": records,
            "response_summary": response_summary,
            "completion_diagnostics": completion,
            "worst_cases": {
                "time": {
                    "member": worst_time["key"],
                    "max": float(worst_time["time_convergence"]["max"]),
                },
                "space": {
                    "member": worst_space["key"],
                    "max": float(worst_space["spatial_convergence"]["max"]),
                },
                "constraint": {
                    "member": worst_constraint["key"],
                    "max": float(worst_constraint["health"]["max_constraint"]),
                },
            },
            "gates": gates,
            "scope": {
                "memory_or_finite_eta": False,
                "likelihood": False,
                "refit": False,
                "nonlinear_matter_evolved": False,
                "completion_selection": False,
            },
            "next_nonlinear_memory_step_licensed": bool(passed),
        }

        p = Path(args.json_out)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")

        for field in ("alpha", "E", "chi"):
            s = response_summary[field]
            print(
                f"RESPONSE_SUMMARY field={field} min={s['min']:.12e} "
                f"median={s['median']:.12e} max={s['max']:.12e} "
                f"min_member={s['min_member']} max_member={s['max_member']}",
                flush=True,
            )
        print(
            f"WORST_TIME member={worst_time['key']} "
            f"max={worst_time['time_convergence']['max']:.12e}",
            flush=True,
        )
        print(
            f"WORST_SPACE member={worst_space['key']} "
            f"max={worst_space['spatial_convergence']['max']:.12e}",
            flush=True,
        )
        print(
            f"WORST_CONSTRAINT member={worst_constraint['key']} "
            f"max={worst_constraint['health']['max_constraint']:.12e}",
            flush=True,
        )
        print(f"GATES={json.dumps(gates, sort_keys=True)}", flush=True)
        print(f"CLASSIFICATION={classification}", flush=True)
        print(f"NEXT_NONLINEAR_MEMORY_STEP_LICENSED={passed}", flush=True)
        print(f"JSON={args.json_out}", flush=True)
        print("NL1C6D2C6B_ALL27_PHYSICAL_NONLINEAR_TRAJECTORIES_END", flush=True)
        return 0 if passed else 2

    except m.InputIncomplete as exc:
        print(f"CLASSIFICATION={INCOMPLETE_LABEL}", flush=True)
        print(f"INCOMPLETE_REASON={exc}", flush=True)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
