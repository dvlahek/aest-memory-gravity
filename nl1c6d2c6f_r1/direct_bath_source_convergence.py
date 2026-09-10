#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from nl1c6d2c6f import finite_eta_gravitational_source as f
from v019s.stable_bath import tan_gl_nodes


d = f.d
c = f.c
m = f.m
d2b = f.d2b

PARENT_D2C6F_HEAD = "df953b9df86ee0b4d73d1691aa713535e27e57fa"
PARENT_FAIL_RECORD = "0b7213a3c3e568dc0854fb1c1a33a055b746cb65"
PREREG_HEAD = "c40a62b4679be161a5f0acbaf413a8336fcb7cd7"

ETA = 1.0 / 8.0
NX = 128
NSTEP = 4096
DIRECT_ORDERS = (128, 256, 512)
COMPRESSED_ORDERS = (39, 47)
SOURCE_GATE = 1.0e-2
STATE_GATE = 1.0e-2
CONSTRAINT_GATE = 1.0e-10
ENERGY_ID_GATE = 1.0e-12
WEIGHT_SUM_GATE = 1.0e-12

PASS_LABEL = "NL1C6D2C6F_R1_DIRECT_BATH_SOURCE_CONVERGENCE_PASS"
FAIL_LABEL = "NL1C6D2C6F_R1_DIRECT_BATH_SOURCE_CONVERGENCE_FAIL"
INCOMPLETE_LABEL = "NL1C6D2C6F_R1_DIRECT_BATH_SOURCE_CONVERGENCE_INCOMPLETE"


def git_head():
    return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()


def is_ancestor(sha):
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0


def target_members():
    out = []
    for sigma in (0, 1):
        for kind in d2b.KINDS:
            out.append({"sigma": sigma, "kind": kind, "beta0": 0.1})
    return out


def install_direct_baths():
    audit = {}
    for order in DIRECT_ORDERS:
        omega, weights = tan_gl_nodes(order)
        omega = np.asarray(omega, float)
        weights = np.asarray(weights, float)
        c.BATH_DATA[order] = (omega, weights)
        audit[str(order)] = {
            "count": int(len(omega)),
            "omega_finite_positive": bool(np.all(np.isfinite(omega)) and np.all(omega > 0.0)),
            "weights_finite_positive": bool(np.all(np.isfinite(weights)) and np.all(weights > 0.0)),
            "sum_weights": float(np.sum(weights)),
            "sum_weight_error": float(abs(np.sum(weights) - 1.0)),
            "omega_min": float(np.min(omega)),
            "omega_max": float(np.max(omega)),
        }
    return audit


def run_ok(run):
    return bool(
        f.run_health(run)
        and run["energy_identity_max"] <= ENERGY_ID_GATE
        and run["min_completed_square_energy"] >= -1.0e-14
    )


def state_compare(a, b):
    return {
        "state": f.rel_l2(a["states"], b["states"]),
        "E": f.rel_l2(a["E"], b["E"]),
    }


def compact_source_summary(run):
    return f.source_summary(run)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--json-out",
        default="results/nl1c6d2c6f_r1_direct_bath_source_convergence.json",
    )
    args = ap.parse_args()
    outpath = Path(args.json_out)
    outpath.parent.mkdir(parents=True, exist_ok=True)

    try:
        head = git_head()
        parent_ok = is_ancestor(PARENT_D2C6F_HEAD)
        fail_record_ok = is_ancestor(PARENT_FAIL_RECORD)
        prereg_ok = is_ancestor(PREREG_HEAD)

        print("NL1C6D2C6F_R1_DIRECT_BATH_SOURCE_CONVERGENCE_START", flush=True)
        print(f"R1_HEAD={head}", flush=True)
        print(f"R1_PARENT_D2C6F_ANCESTOR={parent_ok}", flush=True)
        print(f"R1_FAIL_RECORD_ANCESTOR={fail_record_ok}", flush=True)
        print(f"R1_PREREG_ANCESTOR={prereg_ok}", flush=True)
        print(f"R1_ETA={ETA:.12e}", flush=True)
        print("R1_DIRECT_ORDERS=" + ",".join(str(x) for x in DIRECT_ORDERS), flush=True)

        members = target_members()
        keys = [d.member_key(x) for x in members]
        exact_coverage = bool(
            len(members) == 6
            and len(set(keys)) == 6
            and all(float(x["beta0"]) == 0.1 for x in members)
            and {int(x["sigma"]) for x in members} == {0, 1}
            and set(str(x["kind"]) for x in members) == set(d2b.KINDS)
        )

        quadrature = install_direct_baths()
        quadrature_ok = all(
            q["count"] == int(order)
            and q["omega_finite_positive"]
            and q["weights_finite_positive"]
            and q["sum_weight_error"] <= WEIGHT_SUM_GATE
            for order, q in ((int(k), v) for k, v in quadrature.items())
        )
        for order in DIRECT_ORDERS:
            q = quadrature[str(order)]
            print(
                f"R1_QUADRATURE order={order} sumerr={q['sum_weight_error']:.3e} "
                f"omin={q['omega_min']:.6e} omax={q['omega_max']:.6e} pass="
                f"{q['omega_finite_positive'] and q['weights_finite_positive'] and q['sum_weight_error'] <= WEIGHT_SUM_GATE}",
                flush=True,
            )

        data = m.prepare_class_data()

        pre = {}
        for order in (*COMPRESSED_ORDERS, *DIRECT_ORDERS):
            print(f"R1_PREHISTORY_BEGIN order={order}", flush=True)
            pre[order] = d.finite_prehistory(data, NX, NSTEP, ETA, order)
            print(f"R1_PREHISTORY_END order={order}", flush=True)

        direct_runs = {}
        direct_records = []
        health_ok = True

        for idx, member in enumerate(members, start=1):
            key = d.member_key(member)
            for order in DIRECT_ORDERS:
                run = f.integrate_with_sources(
                    data, NX, NSTEP, member, ETA, order, pre[order]
                )
                direct_runs[(key, order)] = run
                ok = run_ok(run)
                health_ok = health_ok and ok
                summ = compact_source_summary(run)
                direct_records.append(
                    {
                        "index": idx,
                        "key": key,
                        "order": order,
                        "health_pass": ok,
                        "finite": run["finite"],
                        "source_finite": run["source_finite"],
                        "full_constraint_max": run["full_constraint_max"],
                        "min_one_plus_j_eff": run["min_one_plus_j_eff"],
                        "energy_identity_max": run["energy_identity_max"],
                        "min_completed_square_energy": run["min_completed_square_energy"],
                        "source_summary": summ,
                    }
                )
                print(
                    f"R1_DIRECT {idx:02d}/06 order={order} {key} health={ok} "
                    f"constraint={run['full_constraint_max']:.6e} "
                    f"min1p={run['min_one_plus_j_eff']:.6e} "
                    f"energy_id={run['energy_identity_max']:.3e}",
                    flush=True,
                )

        direct_convergence = []
        worst_source_256_512 = -1.0
        worst_source_event = None
        worst_state_256_512 = 0.0
        direct_source_ok = True
        direct_state_ok = True

        for idx, member in enumerate(members, start=1):
            key = d.member_key(member)
            r128 = direct_runs[(key, 128)]
            r256 = direct_runs[(key, 256)]
            r512 = direct_runs[(key, 512)]

            s128_256 = f.compare_sources(r128, r256)
            s256_512 = f.compare_sources(r256, r512)
            y128_256 = state_compare(r128, r256)
            y256_512 = state_compare(r256, r512)

            member_source_max = max(s256_512.values())
            member_state_max = max(y256_512.values())
            direct_source_ok = direct_source_ok and member_source_max <= SOURCE_GATE
            direct_state_ok = direct_state_ok and member_state_max <= STATE_GATE
            worst_state_256_512 = max(worst_state_256_512, member_state_max)

            for name, value in s256_512.items():
                if value > worst_source_256_512:
                    worst_source_256_512 = float(value)
                    worst_source_event = {
                        "key": key,
                        "source": name,
                        "relative_L2_256_to_512": float(value),
                    }

            improvement = {
                name: bool(s256_512[name] <= s128_256[name])
                for name in f.SOURCE_NAMES
            }
            direct_convergence.append(
                {
                    "index": idx,
                    "key": key,
                    "source_128_to_256": s128_256,
                    "source_256_to_512": s256_512,
                    "state_128_to_256": y128_256,
                    "state_256_to_512": y256_512,
                    "source_improves_256_to_512_non_gating": improvement,
                    "direct512_source_summary": compact_source_summary(r512),
                }
            )
            print(
                f"R1_CONVERGENCE {idx:02d}/06 {key} "
                f"source128_256={max(s128_256.values()):.6e} "
                f"source256_512={member_source_max:.6e} "
                f"state256_512={member_state_max:.6e}",
                flush=True,
            )

        compressed_records = []
        for idx, member in enumerate(members, start=1):
            key = d.member_key(member)
            ref = direct_runs[(key, 512)]
            row = {"index": idx, "key": key}
            for order in COMPRESSED_ORDERS:
                run = f.integrate_with_sources(
                    data, NX, NSTEP, member, ETA, order, pre[order]
                )
                src = f.compare_sources(run, ref)
                st = state_compare(run, ref)
                row[f"compressed_{order}_to_direct512_source"] = src
                row[f"compressed_{order}_to_direct512_state"] = st
                row[f"compressed_{order}_health"] = run_ok(run)
                print(
                    f"R1_COMPRESSED_DIAG {idx:02d}/06 order={order} {key} "
                    f"source_to_512={max(src.values()):.6e} state_to_512={max(st.values()):.6e}",
                    flush=True,
                )
            compressed_records.append(row)

        g1 = bool(parent_ok and fail_record_ok and prereg_ok and exact_coverage and DIRECT_ORDERS == (128, 256, 512))
        g2 = bool(quadrature_ok)
        g3 = bool(health_ok)
        g4 = bool(direct_source_ok)
        g5 = bool(direct_state_ok)
        g6 = True

        gates = {
            "R1_parent_fail_prereg_exact_six_coverage": g1,
            "R2_direct_quadrature_positive_normalized": g2,
            "R3_all_direct_trajectory_health_and_energy_identity": g3,
            "R4_direct256_to_direct512_source_convergence_le_1e-2": g4,
            "R5_direct256_to_direct512_state_E_convergence_le_1e-2": g5,
            "R6_scope_clean_no_amplitude_sign_observation_gate": g6,
        }
        classification = PASS_LABEL if all(gates.values()) else FAIL_LABEL
        feedback_licensed = bool(all(gates.values()))

        result = {
            "classification": classification,
            "head": head,
            "parent_D2C6F_head": PARENT_D2C6F_HEAD,
            "parent_D2C6F_fail_record": PARENT_FAIL_RECORD,
            "predata_commit": PREREG_HEAD,
            "eta": ETA,
            "nx": NX,
            "nstep": NSTEP,
            "target_members": keys,
            "direct_orders": list(DIRECT_ORDERS),
            "compressed_orders_diagnostic_only": list(COMPRESSED_ORDERS),
            "quadrature_audit": quadrature,
            "direct_records": direct_records,
            "direct_convergence": direct_convergence,
            "compressed_to_direct512_diagnostics": compressed_records,
            "worst_direct256_to_direct512_source_convergence": float(worst_source_256_512),
            "worst_direct256_to_direct512_source_event": worst_source_event,
            "worst_direct256_to_direct512_state_E_convergence": float(worst_state_256_512),
            "gates": gates,
            "historical_D2C6F_fail_unchanged": True,
            "self_consistent_weakfield_feedback_step_licensed": feedback_licensed,
            "licensed_feedback_primary_bath_if_pass": 256 if feedback_licensed else None,
            "licensed_feedback_control_bath_if_pass": 512 if feedback_licensed else None,
            "observational_step_licensed": False,
            "full_arbitrary_amplitude_nonlinear_gr_aest_licensed": False,
            "interpretation": (
                "PASS means the previously unresolved direct metric-stress source is converged under an independent, non-fitted direct tan-Gauss-Legendre Drude quadrature on the six original F6 failures. The historical D2C6F 39/47 FAIL remains unchanged. PASS licenses only a separately preregistered self-consistent weak-field feedback stage using direct N=256 primary and N=512 control."
            ),
        }

        outpath.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print("WORST_DIRECT_256_512_SOURCE=" + f"{worst_source_256_512:.12e}", flush=True)
        print("WORST_DIRECT_256_512_STATE_E=" + f"{worst_state_256_512:.12e}", flush=True)
        print("GATES=" + json.dumps(gates, sort_keys=True), flush=True)
        print("CLASSIFICATION=" + classification, flush=True)
        print("HISTORICAL_D2C6F_FAIL_UNCHANGED=True", flush=True)
        print("SELF_CONSISTENT_WEAKFIELD_FEEDBACK_STEP_LICENSED=" + str(feedback_licensed), flush=True)
        print("OBSERVATIONAL_STEP_LICENSED=False", flush=True)
        print("JSON=" + str(outpath), flush=True)
        print("NL1C6D2C6F_R1_DIRECT_BATH_SOURCE_CONVERGENCE_END", flush=True)
        raise SystemExit(0 if all(gates.values()) else 1)

    except SystemExit:
        raise
    except Exception as exc:
        result = {
            "classification": INCOMPLETE_LABEL,
            "error_type": type(exc).__name__,
            "error": str(exc),
            "historical_D2C6F_fail_unchanged": True,
            "self_consistent_weakfield_feedback_step_licensed": False,
            "observational_step_licensed": False,
        }
        outpath.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print("CLASSIFICATION=" + INCOMPLETE_LABEL, flush=True)
        print(f"ERROR={type(exc).__name__}: {exc}", flush=True)
        print("SELF_CONSISTENT_WEAKFIELD_FEEDBACK_STEP_LICENSED=False", flush=True)
        print("OBSERVATIONAL_STEP_LICENSED=False", flush=True)
        print("JSON=" + str(outpath), flush=True)
        raise SystemExit(2)


if __name__ == "__main__":
    main()
