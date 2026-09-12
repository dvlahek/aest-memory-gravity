#!/usr/bin/env python3
from __future__ import annotations

import argparse
import inspect
import json
from pathlib import Path
import subprocess
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fullj_weyl import evolving_flrw_weyl_bridge as r0
from fullj_weyl import evolving_flrw_weyl_bridge_r1 as r1
from nl1c6d2c6b import all27_physical_nonlinear_trajectories as d2b

m = d2b.m

R1B_RESULT_LOCK = "6e3f8735712c3bb21eab5578e08c13f27d604ba0"
R2_PREDATA_LOCK = "d59529f429719ab29fdd24669e9a4f27dfa54388"

PASS_LABEL = "FULLJ_EVOLVING_WEYL_BRIDGE_R2_PASS"
FAIL_LABEL = "FULLJ_EVOLVING_WEYL_BRIDGE_R2_FAIL"
INCOMPLETE_LABEL = "FULLJ_EVOLVING_WEYL_BRIDGE_R2_INCOMPLETE_METRIC_CLOSURE"

NX = r0.NX
NSTEP = r0.NSTEP
NMAX = r0.NMAX
LINEAR_GATE = r0.LINEAR_GATE
STATIC_GATE = r0.STATIC_GATE
METRIC_CONSTRAINT_GATE = r0.METRIC_CONSTRAINT_GATE
SLIP_ID_GATE = r0.SLIP_ID_GATE
SOURCE_ID_GATE = r0.SOURCE_ID_GATE


def git_head():
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()


def is_ancestor(sha):
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0


def rel_l2(a, b):
    aa = np.asarray(a)
    bb = np.asarray(b)
    return float(np.linalg.norm(aa - bb) / max(np.linalg.norm(bb), 1.0e-300))


def class_theta_field(data, tau, nx, C=None):
    if C is None:
        C = m.cos_matrix(nx)
    return m.to_field(m.mode_values(data, tau, "theta"), C)


def reconstruct_metric_r2(data, tau, delta, theta, nx, C=None):
    if C is None:
        C = m.cos_matrix(nx)
    bg = r1.fluid_quantities(data, tau)
    ref, _ = r1.class_sources(data, tau, nx, C)
    corr = {
        "delta_rho": bg["rho"] * (np.asarray(delta, float) - ref["delta"]),
        "q_momentum": bg["rho_plus_p"] * (np.asarray(theta, float) - ref["theta_div"]),
        "shear": np.zeros(nx, float),
    }
    mc = r0.metric_correction(data, tau, corr, nx)
    phi0, psi0, w0 = r0.class_metric_fields(data, tau, nx, C)
    phi = phi0 + mc["phi"]
    psi = psi0 + mc["psi"]
    class_slip = psi0 - phi0
    slip = class_slip + (mc["psi"] - mc["phi"])
    return {
        "phi": phi,
        "psi": psi,
        "weyl": phi + psi,
        "slip": slip,
        "class_phi": phi0,
        "class_psi": psi0,
        "class_weyl": w0,
        "class_slip": class_slip,
        "delta": np.asarray(delta, float),
        "theta": np.asarray(theta, float),
        "reference_source": ref,
        "correction_source": corr,
        "metric_correction": mc,
        "background": bg,
    }


def fluid_rhs(data, tau, y, delta, theta, nx, C, ops):
    # IMPORTANT: Theta_A is a directly evolved state.  The ill-conditioned
    # algebraic reconstruction from chi/Q-alpha is intentionally absent here.
    Pi, E, bg = r1.pi_from_state(data, tau, y, delta, nx, ops)
    rec = reconstruct_metric_r2(data, tau, delta, theta, nx, C)
    Hconf = bg["a"] * bg["H"]
    phi0_prime = r1.class_field_prime(data, tau, "phi", nx, C)
    dphi_corr = rec["metric_correction"]["X"] - Hconf * rec["metric_correction"]["psi"]
    phi_prime = phi0_prime + dphi_corr

    ddelta = (
        3.0 * Hconf * (bg["w"] * np.asarray(delta, float) - Pi)
        + (1.0 + bg["w"]) * (3.0 * phi_prime - np.asarray(theta, float))
    )

    lap = ops[1]
    dtheta = (
        (3.0 * bg["cad2"] - 1.0) * Hconf * np.asarray(theta, float)
        - lap(Pi / (1.0 + bg["w"]) + rec["psi"])
    )
    return ddelta, dtheta, rec, Pi, E


def initial_combined_state(data, nx):
    y, init = m.initial_state(data, nx)
    C = m.cos_matrix(nx)
    t0 = data["t0"]
    delta0 = r0.class_field(data, t0, "deltaA", nx, C)
    theta0 = class_theta_field(data, t0, nx, C)
    return y, np.asarray(delta0, float), np.asarray(theta0, float), init


def integrate_combined_r2(data, nx, nstep, nonlinear):
    y, delta, theta, init = initial_combined_state(data, nx)
    C = m.cos_matrix(nx)
    ops = m.spec_ops(nx)
    t0, t1 = data["t0"], data["t1"]
    h = (t1 - t0) / nstep
    tchecks = np.asarray(data["tau_check"], float)
    checkpoints = []
    ci = 0
    finite = True
    fail_reason = None

    def rhs_all(t, yc, dc, tc):
        dy = d2b.rhs_member(data, t, yc, ops, C, nonlinear)
        dd, dt, rec, Pi, E = fluid_rhs(data, t, yc, dc, tc, nx, C, ops)
        return dy, dd, dt

    def store(t, yc, dc, tc):
        rec = reconstruct_metric_r2(data, float(t), dc, tc, nx, C)
        E, cr, x, je = d2b.checkpoint_health_member(data, float(t), yc, ops)
        checkpoints.append({
            "tau": float(t),
            "y": np.asarray(yc, float).copy(),
            "delta": np.asarray(dc, float).copy(),
            "theta": np.asarray(tc, float).copy(),
            "E": np.asarray(E, float).copy(),
            "canonical_constraint": float(cr),
            "metric": rec,
        })

    store(t0, y, delta, theta)
    ci = 1

    for istep in range(nstep):
        t = t0 + istep * h
        tn = t1 if istep + 1 == nstep else t0 + (istep + 1) * h

        k1y, k1d, k1t = rhs_all(t, y, delta, theta)
        k2y, k2d, k2t = rhs_all(
            t + 0.5*h,
            y + 0.5*h*k1y,
            delta + 0.5*h*k1d,
            theta + 0.5*h*k1t,
        )
        k3y, k3d, k3t = rhs_all(
            t + 0.5*h,
            y + 0.5*h*k2y,
            delta + 0.5*h*k2d,
            theta + 0.5*h*k2t,
        )
        k4y, k4d, k4t = rhs_all(
            t + h,
            y + h*k3y,
            delta + h*k3d,
            theta + h*k3t,
        )

        yn = y + (h/6.0) * (k1y + 2.0*k2y + 2.0*k3y + k4y)
        dn = delta + (h/6.0) * (k1d + 2.0*k2d + 2.0*k3d + k4d)
        qn = theta + (h/6.0) * (k1t + 2.0*k2t + 2.0*k3t + k4t)

        if not np.all(np.isfinite(yn)) or not np.all(np.isfinite(dn)) or not np.all(np.isfinite(qn)):
            finite = False
            fail_reason = f"nonfinite_r2_state_step_{istep+1}"
            break

        while ci < len(tchecks) and tchecks[ci] <= tn + 1.0e-10:
            frac = float((tchecks[ci] - t) / h)
            frac = min(1.0, max(0.0, frac))
            yc = y + frac * (yn - y)
            dc = delta + frac * (dn - delta)
            tc = theta + frac * (qn - theta)
            store(float(tchecks[ci]), yc, dc, tc)
            ci += 1

        y, delta, theta = yn, dn, qn

    if finite and ci != len(tchecks):
        finite = False
        fail_reason = f"stored_only_{ci}_of_{len(tchecks)}_checkpoints"

    return {
        "finite": bool(finite),
        "fail_reason": fail_reason,
        "checkpoints": checkpoints,
        "initial": init,
    }


def source_traceability_audit_r2(data):
    worst_rhop = 0.0
    for tau in np.asarray(data["tau_check"], float):
        bg = r1.fluid_quantities(data, float(tau))
        rhs = bg["Q"] * bg["KQ"] / 3.0
        worst_rhop = max(
            worst_rhop,
            abs(bg["rho_plus_p"] - rhs) / max(abs(rhs), 1.0e-300),
        )

    src = inspect.getsource(fluid_rhs)
    direct_theta = ("theta_from_canonical" not in src) and ("chi / bg" not in src) and ("chi/bg" not in src)
    metrics = {
        "rho_plus_p_identity_rel_max": float(worst_rhop),
        "nonlinear_completion_shear_source_maxabs": 0.0,
        "continuity_identity_certified_by_R1A": True,
        "euler_identity_certified_by_R1B": True,
        "ill_conditioned_theta_reconstruction_used_in_RHS": not direct_theta,
        "pass": bool(worst_rhop <= SOURCE_ID_GATE and direct_theta),
    }
    return metrics


def linear_regression_r2(data):
    d2b.set_member({"sigma": 0, "kind": "simple", "beta0": 1.0})
    run = integrate_combined_r2(data, NX, NSTEP, False)
    if not run["finite"] or len(run["checkpoints"]) != len(data["tau_check"]):
        return {"pass": False, "reason": run.get("fail_reason", "linear_r2_incomplete")}, run

    vals = {"Phi": [], "Psi": [], "W": [], "delta_A": [], "Theta_A": []}
    refs = {"Phi": [], "Psi": [], "W": [], "delta_A": [], "Theta_A": []}
    max_constraint = {"hamiltonian": 0.0, "momentum": 0.0, "shear": 0.0}
    C = m.cos_matrix(NX)

    for cp in run["checkpoints"]:
        rec = cp["metric"]
        vals["Phi"].append(rec["phi"])
        vals["Psi"].append(rec["psi"])
        vals["W"].append(rec["weyl"])
        vals["delta_A"].append(cp["delta"])
        vals["Theta_A"].append(cp["theta"])
        refs["Phi"].append(rec["class_phi"])
        refs["Psi"].append(rec["class_psi"])
        refs["W"].append(rec["class_weyl"])
        refs["delta_A"].append(rec["reference_source"]["delta"])
        refs["Theta_A"].append(rec["reference_source"]["theta_div"])
        for key, value in rec["metric_correction"]["constraint"].items():
            max_constraint[key] = max(max_constraint[key], float(value))

    err = {name: rel_l2(np.stack(vals[name]), np.stack(refs[name])) for name in vals}
    passed = bool(all(err[name] <= LINEAR_GATE for name in ("Phi", "Psi", "W", "delta_A", "Theta_A")))
    return {
        "pass": passed,
        "relative_L2": err,
        "gate": LINEAR_GATE,
        "metric_correction_constraint_max": max_constraint,
    }, run


def output_modes(field, nmax=NMAX):
    arr = np.asarray(field, float)
    ff = np.fft.rfft(arr) / arr.size
    out = np.zeros(nmax + 1, complex)
    n = min(out.size, ff.size)
    out[:n] = ff[:n]
    return out


def run_member_r2(data, member):
    d2b.set_member(member)
    run = integrate_combined_r2(data, NX, NSTEP, True)
    key = d2b.member_key(member)
    if not run["finite"] or len(run["checkpoints"]) != len(data["tau_check"]):
        return {"key": key, "finite": False, "reason": run.get("fail_reason", "r2_incomplete")}, None

    stores = {"Phi": [], "Psi": [], "W": [], "slip": [], "delta_A": [], "Theta_A": []}
    max_metric = {"hamiltonian": 0.0, "momentum": 0.0, "shear": 0.0}
    max_source_corr = {"delta_rho": 0.0, "q_momentum": 0.0}
    max_canonical = 0.0
    slip_ref = []
    slip_tot = []
    finite = True

    for cp in run["checkpoints"]:
        rec = cp["metric"]
        fields = (rec["phi"], rec["psi"], rec["weyl"], rec["slip"], cp["delta"], cp["theta"])
        finite = finite and all(np.all(np.isfinite(x)) for x in fields)
        stores["Phi"].append(output_modes(rec["phi"]))
        stores["Psi"].append(output_modes(rec["psi"]))
        stores["W"].append(output_modes(rec["weyl"]))
        stores["slip"].append(output_modes(rec["slip"]))
        stores["delta_A"].append(output_modes(cp["delta"]))
        stores["Theta_A"].append(output_modes(cp["theta"]))
        slip_ref.append(rec["class_slip"])
        slip_tot.append(rec["slip"])
        max_canonical = max(max_canonical, float(cp["canonical_constraint"]))
        for name, value in rec["metric_correction"]["constraint"].items():
            max_metric[name] = max(max_metric[name], float(value))
        for name in max_source_corr:
            max_source_corr[name] = max(
                max_source_corr[name],
                float(np.sqrt(np.mean(np.asarray(rec["correction_source"][name], float)**2))),
            )

    slip_identity = rel_l2(np.stack(slip_tot), np.stack(slip_ref))
    slip_maxabs = float(np.max(np.abs(np.stack(slip_tot))))
    record = {
        "key": key,
        "sigma": int(member["sigma"]),
        "kind": str(member["kind"]),
        "beta0": float(member["beta0"]),
        "finite": bool(finite),
        "canonical_constraint_max": float(max_canonical),
        "metric_constraint_max": max_metric,
        "source_correction_rms_max": max_source_corr,
        "slip_to_CLASS_slip_relL2": float(slip_identity),
        "slip_maxabs": slip_maxabs,
    }
    arrays = {k: np.asarray(v, complex) for k, v in stores.items()}
    return record, arrays


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json-out", default="results/fullj_evolving_weyl_bridge_r2.json")
    ap.add_argument("--npz-out", default="results/fullj_evolving_weyl_bridge_r2.npz")
    args = ap.parse_args()
    jout = Path(args.json_out)
    nout = Path(args.npz_out)
    jout.parent.mkdir(parents=True, exist_ok=True)

    try:
        ancestry = {
            "phase_lock": is_ancestor(r0.PHASE_LOCK),
            "original_predata_lock": is_ancestor(r0.PREDATA_LOCK),
            "r1b_result_lock": is_ancestor(R1B_RESULT_LOCK),
            "r2_predata_lock": is_ancestor(R2_PREDATA_LOCK),
        }
        if not all(ancestry.values()):
            raise m.InputIncomplete(f"required R2 ancestry missing: {ancestry}")

        print("FULLJ_EVOLVING_WEYL_BRIDGE_R2_START", flush=True)
        print("FULLJ_WEYL_R2_ANCESTRY=" + json.dumps(ancestry, sort_keys=True), flush=True)
        data = r0.prepare_bridge_data()
        print(
            f"FULLJ_WEYL_R2_INPUT_READY modes={len(data['modes'])} checkpoints={len(data['tau_check'])} members=27",
            flush=True,
        )

        g1 = source_traceability_audit_r2(data)
        print(
            f"FULLJ_WEYL_R2_G1 rho+p={g1['rho_plus_p_identity_rel_max']:.12e} "
            f"illThetaRHS={g1['ill_conditioned_theta_reconstruction_used_in_RHS']} pass={g1['pass']}",
            flush=True,
        )

        g3 = r0.static_regression()
        print(f"FULLJ_WEYL_R2_G3 static_max={g3['max_error']:.12e} pass={g3['pass']}", flush=True)

        g2, linear_run = linear_regression_r2(data)
        if "relative_L2" in g2:
            print(
                "FULLJ_WEYL_R2_G2 "
                + " ".join(f"{k}={v:.12e}" for k, v in g2["relative_L2"].items())
                + f" pass={g2['pass']}",
                flush=True,
            )
        else:
            print(f"FULLJ_WEYL_R2_G2 pass=False reason={g2.get('reason','unknown')}", flush=True)

        records = []
        stores = []
        names = []
        global_constraint = {"hamiltonian": 0.0, "momentum": 0.0, "shear": 0.0}
        all_finite = True
        slip_identity_max = 0.0
        slip_maxabs_global = 0.0

        for i, member in enumerate(r0.all_members(), start=1):
            rec, arrays = run_member_r2(data, member)
            records.append(rec)
            print(
                f"FULLJ_WEYL_R2_MEMBER {i:02d}/27 key={rec['key']} finite={rec['finite']} "
                + (
                    " ".join(f"{k}={v:.3e}" for k, v in rec.get("metric_constraint_max", {}).items())
                    + f" slip={rec.get('slip_maxabs',float('nan')):.3e}"
                    if rec.get("finite") else f" reason={rec.get('reason','unknown')}"
                ),
                flush=True,
            )
            if arrays is None:
                all_finite = False
                continue
            stores.append(arrays)
            names.append(rec["key"])
            all_finite = all_finite and bool(rec["finite"])
            for k, v in rec["metric_constraint_max"].items():
                global_constraint[k] = max(global_constraint[k], float(v))
            slip_identity_max = max(slip_identity_max, float(rec["slip_to_CLASS_slip_relL2"]))
            slip_maxabs_global = max(slip_maxabs_global, float(rec["slip_maxabs"]))

        g4 = {
            "metric_constraint_max": global_constraint,
            "gate": METRIC_CONSTRAINT_GATE,
            "pass": bool(len(stores) == 27 and all(v <= METRIC_CONSTRAINT_GATE for v in global_constraint.values())),
        }
        g5 = {"finite_members": int(sum(bool(r.get("finite", False)) for r in records)), "expected": 27}
        g5["pass"] = bool(g5["finite_members"] == 27 and all_finite)
        g6 = {
            "slip_to_CLASS_slip_relL2_max": float(slip_identity_max),
            "slip_maxabs_global": float(slip_maxabs_global),
            "identity_gate": SLIP_ID_GATE,
            "pass": bool(slip_identity_max <= SLIP_ID_GATE and slip_maxabs_global > 0.0),
        }
        g7 = {
            "directly_evolved_Theta_A": bool(not g1["ill_conditioned_theta_reconstruction_used_in_RHS"]),
            "pass": bool(not g1["ill_conditioned_theta_reconstruction_used_in_RHS"]),
        }

        print(
            "FULLJ_WEYL_R2_G4 " + " ".join(f"{k}={v:.12e}" for k, v in global_constraint.items())
            + f" pass={g4['pass']}", flush=True,
        )
        print(f"FULLJ_WEYL_R2_G5 finite={g5['finite_members']}/27 pass={g5['pass']}", flush=True)
        print(
            f"FULLJ_WEYL_R2_G6 slip_identity={slip_identity_max:.12e} "
            f"slip_maxabs={slip_maxabs_global:.12e} pass={g6['pass']}", flush=True,
        )
        print(f"FULLJ_WEYL_R2_G7 directTheta={g7['directly_evolved_Theta_A']} pass={g7['pass']}", flush=True)

        gates = {
            "G1_source_equation_provenance": bool(g1["pass"]),
            "G2_linear_CLASS_regression": bool(g2["pass"]),
            "G3_static_fullJ_regression": bool(g3["pass"]),
            "G4_metric_constraint_closure": bool(g4["pass"]),
            "G5_finite_evolving_Weyl": bool(g5["pass"]),
            "G6_static_vs_evolving_slip_distinction": bool(g6["pass"]),
            "G7_no_ill_conditioned_Theta_RHS": bool(g7["pass"]),
        }
        classification = PASS_LABEL if all(gates.values()) else FAIL_LABEL

        result = {
            "classification": classification,
            "diagnostic_complete": True,
            "git_head": git_head(),
            "ancestry": ancestry,
            "scope": "eta=0 triangular evolving-FLRW Weyl bridge on locked D2C6 canonical trajectories with directly evolved effective-fluid pair (delta_A,Theta_A)",
            "g1_source_equation_provenance": g1,
            "g2_linear_CLASS": g2,
            "g3_static_fullJ": g3,
            "g4_constraint_closure": g4,
            "g5_finite_output": g5,
            "g6_slip_distinction": g6,
            "g7_direct_Theta_state": g7,
            "gates": gates,
            "records": records,
            "tau_checkpoints": [float(x) for x in data["tau_check"]],
            "z_checkpoints": [float(x) for x in m.CHECK_Z],
            "HISTORICAL_R0_FAIL_PRESERVED": True,
            "HISTORICAL_R1_FAIL_PRESERVED": True,
            "EVOLVING_WEYL_COVARIANCE_DIAGNOSTIC_LICENSED": bool(classification == PASS_LABEL),
            "EVOLVING_WEYL_POWER_LICENSED": False,
            "ACT_LIKELIHOOD_LICENSED": False,
            "OBSERVATIONAL_CLAIM_LICENSED": False,
            "NO_STATIC_W_EQUALS_2PHI_PROMOTION": True,
            "CANONICAL_TRAJECTORY_METRIC_FEEDBACK_ENABLED": False,
        }
        jout.write_text(json.dumps(result, indent=2, sort_keys=True, allow_nan=True) + "\n")

        if len(stores) == 27:
            payload = {
                "member_names": np.asarray(names, dtype="U96"),
                "tau": np.asarray(data["tau_check"], float),
                "z": np.asarray(m.CHECK_Z, float),
                "mode_number": np.arange(NMAX + 1, dtype=int),
            }
            for key in ("Phi", "Psi", "W", "slip", "delta_A", "Theta_A"):
                payload[key] = np.stack([x[key] for x in stores], axis=0)
            np.savez_compressed(nout, **payload)

        print("FULLJ_WEYL_R2_GATES=" + json.dumps(gates, sort_keys=True), flush=True)
        print(f"FULLJ_EVOLVING_WEYL_R2_CLASSIFICATION={classification}", flush=True)
        print("HISTORICAL_R0_FAIL_PRESERVED=True", flush=True)
        print("HISTORICAL_R1_FAIL_PRESERVED=True", flush=True)
        print(f"EVOLVING_WEYL_COVARIANCE_DIAGNOSTIC_LICENSED={classification == PASS_LABEL}", flush=True)
        print("EVOLVING_WEYL_POWER_LICENSED=False", flush=True)
        print("ACT_LIKELIHOOD_LICENSED=False", flush=True)
        print("OBSERVATIONAL_CLAIM_LICENSED=False", flush=True)
        print("CANONICAL_TRAJECTORY_METRIC_FEEDBACK_ENABLED=False", flush=True)
        print(f"FULLJ_WEYL_R2_JSON={jout}", flush=True)
        print(f"FULLJ_WEYL_R2_NPZ={nout}", flush=True)
        return 0 if classification == PASS_LABEL else 2

    except m.InputIncomplete as exc:
        result = {
            "classification": INCOMPLETE_LABEL,
            "diagnostic_complete": False,
            "reason": str(exc),
            "git_head": git_head(),
            "ACT_LIKELIHOOD_LICENSED": False,
            "OBSERVATIONAL_CLAIM_LICENSED": False,
        }
        jout.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print(f"FULLJ_EVOLVING_WEYL_R2_CLASSIFICATION={INCOMPLETE_LABEL}", flush=True)
        print("FULLJ_WEYL_R2_REASON=" + str(exc), flush=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
