#!/usr/bin/env python3
from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path
import subprocess

import numpy as np

from nl1c6d2c6d import finite_positive_eta_retained as d

c = d.c
m = d.m
d2b = d.d2b

PARENT_D2C6D_HEAD = "0e596eb342e56fae56287017876fb2ee07c4c2b4"
PARENT_D2C6D_RUN = 34507347610
PREREG_HEAD = "38d37b65447108a2e9ae39e991bfe3adf9f1682e"

ETAS = (1.0 / 32.0, 1.0 / 16.0, 1.0 / 8.0)
ETA_MAX = ETAS[-1]
PRIMARY_ORDER = 39
CONTROL_ORDER = 47

SOURCE_GATE = 1.0e-10
CONSTRAINT_GATE = 1.0e-10
BATH_GATE = 1.0e-2
TIME_GATE = 2.0e-3
SPACE_GATE = 5.0e-3

PASS_LABEL = "NL1C6D2C6E_LARGER_ETA_RETAINED_SCALAR_CURRENT_PASS"
FAIL_LABEL = "NL1C6D2C6E_LARGER_ETA_RETAINED_SCALAR_CURRENT_FAIL"
INCOMPLETE_LABEL = "NL1C6D2C6E_LARGER_ETA_RETAINED_SCALAR_CURRENT_INCOMPLETE"


def rel_l2(a, b):
    aa = np.asarray(a, float)
    bb = np.asarray(b, float)
    return float(np.linalg.norm(aa - bb) / max(np.linalg.norm(bb), 1.0e-300))


def git_head():
    return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()


def is_ancestor(sha):
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0


def source_identity_audit(data):
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


def member_health(run):
    return bool(
        run["finite"]
        and run["full_constraint_max"] <= CONSTRAINT_GATE
        and run["min_one_plus_j_eff"] > 0.0
    )


def field_arrays(run):
    return {
        "alpha": np.asarray(run["states"][:, 0], float),
        "E": np.asarray(run["E"], float),
        "chi": np.asarray(run["states"][:, 1], float),
    }


def quotient_change(run_lo, eta_lo, run_hi, eta_hi):
    out = {}
    flo = field_arrays(run_lo)
    fhi = field_arrays(run_hi)
    for name in ("alpha", "E", "chi"):
        qlo = flo[name] / eta_lo
        qhi = fhi[name] / eta_hi
        out[name] = rel_l2(qlo, qhi)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--json-out",
        default="results/nl1c6d2c6e_larger_eta_retained.json",
    )
    args = ap.parse_args()

    try:
        head = git_head()
        parent_ok = is_ancestor(PARENT_D2C6D_HEAD)
        prereg_ok = is_ancestor(PREREG_HEAD)
        data = m.prepare_class_data()

        print("NL1C6D2C6E_LARGER_ETA_RETAINED_START", flush=True)
        print(f"D2C6E_HEAD={head}", flush=True)
        print(f"D2C6E_PARENT_ANCESTOR={parent_ok}", flush=True)
        print(f"D2C6E_PREREG_ANCESTOR={prereg_ok}", flush=True)
        print(
            "D2C6E_ETA_LADDER=" + ",".join(f"{x:.12e}" for x in ETAS),
            flush=True,
        )

        expected = [
            {"sigma": s, "kind": kind, "beta0": beta}
            for s, kind, beta in itertools.product(d2b.SIGMAS, d2b.KINDS, d2b.BETAS)
        ]
        coverage = len(expected) == 27 and len({d.member_key(q) for q in expected}) == 27

        source_audit = source_identity_audit(data)
        e2 = bool(
            source_audit["elliptic_relative_L2"] <= SOURCE_GATE
            and source_audit["increment_relative_L2"] <= SOURCE_GATE
        )
        print(
            "E2_SOURCE "
            f"elliptic={source_audit['elliptic_relative_L2']:.12e} "
            f"increment={source_audit['increment_relative_L2']:.12e} pass={e2}",
            flush=True,
        )

        # Full retarded finite-eta prehistories. These depend on eta/order/grid,
        # but not on the nonlinear completion member, so each frozen case is
        # computed once and reused across the 27-member ensemble.
        pre_primary = {
            eta: d.finite_prehistory(data, 128, 4096, eta, PRIMARY_ORDER)
            for eta in ETAS
        }
        pre_order47 = d.finite_prehistory(data, 128, 4096, ETA_MAX, CONTROL_ORDER)
        pre_time = d.finite_prehistory(data, 128, 8192, ETA_MAX, PRIMARY_ORDER)
        pre_space = d.finite_prehistory(data, 256, 4096, ETA_MAX, PRIMARY_ORDER)

        # Certified eta=0 tangent retained only as a non-gating diagnostic.
        tangent_pre = {PRIMARY_ORDER: c.prehistory(data, 128, 4096, PRIMARY_ORDER)}

        records = []
        primary_runs = {}
        tangent_runs = {}
        primary_health_fail = False
        tangent_remainder_by_eta = {eta: [] for eta in ETAS}

        for index, member in enumerate(expected, start=1):
            key = d.member_key(member)
            tangent = c.integrate(
                data,
                128,
                4096,
                member,
                orders=(PRIMARY_ORDER,),
                nonlinear=True,
                pre_cache=tangent_pre,
            )
            if not tangent["finite"]:
                raise RuntimeError(f"certified tangent reproduction nonfinite for {key}")
            tangent_runs[key] = tangent

            for eta in ETAS:
                run = d.integrate_finite(
                    data, 128, 4096, member, eta, PRIMARY_ORDER, pre_primary[eta]
                )
                primary_runs[(key, eta)] = run
                healthy = member_health(run)
                primary_health_fail = primary_health_fail or (not healthy)

                tc_fields, tc_momentum, tc_max = d.tangent_continuation(run, tangent, eta)
                tangent_remainder_by_eta[eta].append(float(tc_max))
                diag = d.displacement_diagnostics(run, tangent, eta)

                records.append(
                    {
                        "index": index,
                        "key": key,
                        "sigma": int(member["sigma"]),
                        "kind": str(member["kind"]),
                        "beta0": float(member["beta0"]),
                        "eta": float(eta),
                        "finite": bool(run["finite"]),
                        "health_pass": bool(healthy),
                        "full_constraint_max": float(run["full_constraint_max"]),
                        "min_one_plus_j_eff": float(run["min_one_plus_j_eff"]),
                        "tangent_remainder": tc_fields,
                        "tangent_momentum_diagnostic": tc_momentum,
                        "tangent_remainder_max": float(tc_max),
                        "diagnostics": diag,
                    }
                )
                print(
                    "D2C6E_MEMBER "
                    f"{index:02d}/27 eta={eta:.12e} {key} "
                    f"health={healthy} constraint={run['full_constraint_max']:.6e} "
                    f"min1p={run['min_one_plus_j_eff']:.6e} "
                    f"Rtan={tc_max:.6e} "
                    f"dalpha={diag['alpha']['displacement_norm']:.6e} "
                    f"dE={diag['E']['displacement_norm']:.6e} "
                    f"dchi={diag['chi']['displacement_norm']:.6e}",
                    flush=True,
                )

        control_records = []
        control_health_fail = False
        bath_max = 0.0
        time_max = 0.0
        space_max = 0.0

        for index, member in enumerate(expected, start=1):
            key = d.member_key(member)
            primary = primary_runs[(key, ETA_MAX)]
            order47 = d.integrate_finite(
                data, 128, 4096, member, ETA_MAX, CONTROL_ORDER, pre_order47
            )
            timectl = d.integrate_finite(
                data, 128, 8192, member, ETA_MAX, PRIMARY_ORDER, pre_time
            )
            spacectl = d.integrate_finite(
                data, 256, 4096, member, ETA_MAX, PRIMARY_ORDER, pre_space
            )

            bath_fields, bmax = d.compare_displacements(primary, order47, False)
            time_fields, tmax = d.compare_displacements(primary, timectl, False)
            space_fields, smax = d.compare_displacements(primary, spacectl, True)
            bath_max = max(bath_max, float(bmax))
            time_max = max(time_max, float(tmax))
            space_max = max(space_max, float(smax))

            control_health = all(member_health(r) for r in (order47, timectl, spacectl))
            control_health_fail = control_health_fail or (not control_health)
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
                "D2C6E_CONTROL "
                f"{index:02d}/27 {key} bath={bmax:.6e} "
                f"time={tmax:.6e} space={smax:.6e} health={control_health}",
                flush=True,
            )

        # Non-gating dyadic quotient changes and predeclared nonlinearity onset.
        quotient_records = []
        onset_records = []
        for member in expected:
            key = d.member_key(member)
            q12 = quotient_change(
                primary_runs[(key, ETAS[0])], ETAS[0],
                primary_runs[(key, ETAS[1])], ETAS[1],
            )
            q23 = quotient_change(
                primary_runs[(key, ETAS[1])], ETAS[1],
                primary_runs[(key, ETAS[2])], ETAS[2],
            )
            quotient_records.append({"key": key, "q_eta1_vs_eta2": q12, "q_eta2_vs_eta3": q23})

            by_eta = {
                float(rec["eta"]): rec
                for rec in records
                if rec["key"] == key
            }
            onset = {"key": key, "fields": {}}
            for field in ("alpha", "E", "chi"):
                vals = [
                    (eta, float(by_eta[eta]["tangent_remainder"][field]))
                    for eta in ETAS
                ]
                first1 = next((float(eta) for eta, value in vals if value > 0.01), None)
                first5 = next((float(eta) for eta, value in vals if value > 0.05), None)
                onset["fields"][field] = {
                    "first_eta_Rtan_gt_1pct": first1,
                    "first_eta_Rtan_gt_5pct": first5,
                    "Rtan_by_eta": {f"{eta:.12e}": value for eta, value in vals},
                }
            onset_records.append(onset)

        e1 = bool(parent_ok and prereg_ok and coverage and len(records) == 81)
        e3 = bool(
            not primary_health_fail
            and not control_health_fail
            and all(rec["health_pass"] for rec in records)
            and all(rec["control_health"] for rec in control_records)
        )
        e4 = bool(bath_max <= BATH_GATE)
        e5 = bool(time_max <= TIME_GATE)
        e6 = bool(space_max <= SPACE_GATE)
        e7 = True

        gates = {
            "E1_parent_prereg_and_exact_27x3_coverage": e1,
            "E2_finite_eta_source_identity_le_1e-10": e2,
            "E3_all_primary_and_control_health": e3,
            "E4_bath_order_displacement_convergence_le_1e-2": e4,
            "E5_time_displacement_convergence_le_2e-3": e5,
            "E6_space_displacement_convergence_le_5e-3": e6,
            "E7_scope_clean": e7,
        }
        passed = all(gates.values())
        classification = PASS_LABEL if passed else FAIL_LABEL

        max_rtan = {
            f"{eta:.12e}": float(max(tangent_remainder_by_eta[eta]))
            for eta in ETAS
        }
        visible_1pct = sum(
            1 for onset in onset_records for x in onset["fields"].values()
            if x["first_eta_Rtan_gt_1pct"] is not None
        )
        strong_5pct = sum(
            1 for onset in onset_records for x in onset["fields"].values()
            if x["first_eta_Rtan_gt_5pct"] is not None
        )

        out = {
            "classification": classification,
            "head": head,
            "parent_D2C6D": {"head": PARENT_D2C6D_HEAD, "run": PARENT_D2C6D_RUN},
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
            "gates": gates,
            "worst_bath_order": float(bath_max),
            "worst_time": float(time_max),
            "worst_space": float(space_max),
            "max_tangent_remainder_by_eta_non_gating": max_rtan,
            "visible_nonlinearity_field_count_gt_1pct_non_gating": int(visible_1pct),
            "strong_departure_field_count_gt_5pct_non_gating": int(strong_5pct),
            "primary_records": records,
            "control_records": control_records,
            "dyadic_quotient_change_non_gating": quotient_records,
            "nonlinearity_onset_non_gating": onset_records,
            "still_larger_retained_eta_step_licensed": bool(passed),
            "full_nonlinear_or_observational_step_licensed": False,
        }
        Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")

        print("D2C6E_MAX_RTAN_BY_ETA=" + json.dumps(max_rtan, sort_keys=True), flush=True)
        print(f"D2C6E_VISIBLE_1PCT_FIELD_COUNT={visible_1pct}", flush=True)
        print(f"D2C6E_STRONG_5PCT_FIELD_COUNT={strong_5pct}", flush=True)
        print(f"WORST_BATH_ORDER={bath_max:.12e}", flush=True)
        print(f"WORST_TIME={time_max:.12e}", flush=True)
        print(f"WORST_SPACE={space_max:.12e}", flush=True)
        print(f"GATES={json.dumps(gates, sort_keys=True)}", flush=True)
        print(f"CLASSIFICATION={classification}", flush=True)
        print(f"STILL_LARGER_RETAINED_ETA_STEP_LICENSED={passed}", flush=True)
        print("FULL_NONLINEAR_OR_OBSERVATIONAL_STEP_LICENSED=False", flush=True)
        print(f"JSON={args.json_out}", flush=True)
        print("NL1C6D2C6E_LARGER_ETA_RETAINED_END", flush=True)
        return 0 if passed else 2

    except m.InputIncomplete as exc:
        print(f"D2C6E_INCOMPLETE {type(exc).__name__}: {exc}", flush=True)
        print(f"CLASSIFICATION={INCOMPLETE_LABEL}", flush=True)
        return 3
    except Exception as exc:
        print(f"D2C6E_ERROR {type(exc).__name__}: {exc}", flush=True)
        print(f"CLASSIFICATION={INCOMPLETE_LABEL}", flush=True)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
