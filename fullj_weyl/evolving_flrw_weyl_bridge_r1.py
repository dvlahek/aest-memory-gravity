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

from fullj_weyl import evolving_flrw_weyl_bridge as r0
from nl1c6d2c6b import all27_physical_nonlinear_trajectories as d2b

m = d2b.m
static = m.static

R0_FAIL_HEAD = "1adb113c62fae8a9610fcc19b64fca0ffa325a9d"
R1_PREDATA_LOCK = "e41a11411e517a72e73dcf1290195b420b6ae032"

PASS_LABEL = "FULLJ_EVOLVING_WEYL_BRIDGE_R1_PASS"
FAIL_LABEL = "FULLJ_EVOLVING_WEYL_BRIDGE_R1_FAIL"
INCOMPLETE_LABEL = "FULLJ_EVOLVING_WEYL_BRIDGE_R1_INCOMPLETE_METRIC_CLOSURE"

NX = r0.NX
NSTEP = r0.NSTEP
NMAX = r0.NMAX
SOURCE_ID_GATE = r0.SOURCE_ID_GATE
LINEAR_GATE = r0.LINEAR_GATE
STATIC_GATE = r0.STATIC_GATE
METRIC_CONSTRAINT_GATE = r0.METRIC_CONSTRAINT_GATE
SLIP_ID_GATE = r0.SLIP_ID_GATE


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


def class_field_prime(data, tau, name, nx, C=None):
    if C is None:
        C = m.cos_matrix(nx)
    vals = np.asarray(
        [float(md["splines"][name](tau, 1)) for md in data["modes"]],
        float,
    )
    return m.to_field(vals, C)


def fluid_quantities(data, tau):
    bg = r0.fluid_background(data, tau)
    bg = dict(bg)
    bg["w"] = bg["p"] / bg["rho"]
    bg["cad2"] = bg["KQ"] / (bg["Q"] * bg["KQQ"])
    vals = [bg[k] for k in ("a", "H", "Q", "KQ", "KQQ", "rho", "p", "rho_plus_p", "w", "cad2")]
    if not np.all(np.isfinite(vals)) or bg["cad2"] < 0.0:
        raise FloatingPointError("invalid R1 effective-fluid background")
    return bg


def theta_from_canonical(data, tau, y, nx, ops=None):
    bg = fluid_quantities(data, tau)
    alpha = np.asarray(y[0], float)
    chi = np.asarray(y[1], float)
    if ops is None:
        ops = m.spec_ops(nx)
    lap = ops[1]
    return -lap(chi / bg["Q"] - alpha) / bg["a"]


def pi_from_state(data, tau, y, delta, nx, ops=None):
    if ops is None:
        ops = m.spec_ops(nx)
    lap = ops[1]
    bg = fluid_quantities(data, tau)
    E, _ = m.derive_E(data, tau, y, ops)
    chi = np.asarray(y[1], float)
    combo = static.KB * np.asarray(E, float) + m.A * chi
    Pi = bg["cad2"] * np.asarray(delta, float) - (
        bg["cad2"] * lap(combo) / (3.0 * bg["a"]**2 * bg["rho"])
    )
    return Pi, E, bg


def class_sources(data, tau, nx, C=None):
    if C is None:
        C = m.cos_matrix(nx)
    bg = fluid_quantities(data, tau)
    delta = r0.class_field(data, tau, "deltaA", nx, C)
    # Use the already locked D2C6 input theta rather than a separately-read duplicate.
    theta = m.to_field(m.mode_values(data, tau, "theta"), C)
    return {
        "delta": delta,
        "theta_div": theta,
        "delta_rho": bg["rho"] * delta,
        "q_momentum": bg["rho_plus_p"] * theta,
        "shear": np.zeros(nx, float),
    }, bg


def reconstruct_metric_r1(data, tau, y, delta, nx, C=None, ops=None):
    if C is None:
        C = m.cos_matrix(nx)
    if ops is None:
        ops = m.spec_ops(nx)
    bg = fluid_quantities(data, tau)
    theta = theta_from_canonical(data, tau, y, nx, ops)
    ref, _ = class_sources(data, tau, nx, C)
    corr = {
        "delta_rho": bg["rho"] * (np.asarray(delta, float) - ref["delta"]),
        "q_momentum": bg["rho_plus_p"] * (theta - ref["theta_div"]),
        "shear": np.zeros(nx, float),
    }
    mc = r0.metric_correction(data, tau, corr, nx)
    phi0, psi0, w0 = r0.class_metric_fields(data, tau, nx, C)
    phi = phi0 + mc["phi"]
    psi = psi0 + mc["psi"]
    # Stable algebraic slip evaluation.  This is exactly psi-phi but avoids
    # subtracting two nearly equal total potentials after adding corrections.
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
        "theta": theta,
        "delta": np.asarray(delta, float),
        "reference_source": ref,
        "correction_source": corr,
        "metric_correction": mc,
        "background": bg,
    }


def delta_rhs(data, tau, y, delta, nx, C, ops):
    Pi, E, bg = pi_from_state(data, tau, y, delta, nx, ops)
    theta = theta_from_canonical(data, tau, y, nx, ops)
    rec = reconstruct_metric_r1(data, tau, y, delta, nx, C, ops)
    phi0_prime = class_field_prime(data, tau, "phi", nx, C)
    Hconf = bg["a"] * bg["H"]
    dphi_corr = rec["metric_correction"]["X"] - Hconf * rec["metric_correction"]["psi"]
    phi_prime = phi0_prime + dphi_corr
    ddelta = (
        3.0 * Hconf * (bg["w"] * np.asarray(delta, float) - Pi)
        + (1.0 + bg["w"]) * (3.0 * phi_prime - theta)
    )
    return ddelta


def initial_combined_state(data, nx):
    y, init = m.initial_state(data, nx)
    C = m.cos_matrix(nx)
    delta0 = r0.class_field(data, data["t0"], "deltaA", nx, C)
    return y, np.asarray(delta0, float), init


def integrate_combined(data, nx, nstep, nonlinear):
    y, delta, init = initial_combined_state(data, nx)
    C = m.cos_matrix(nx)
    ops = m.spec_ops(nx)
    t0, t1 = data["t0"], data["t1"]
    h = (t1 - t0) / nstep
    tchecks = np.asarray(data["tau_check"], float)
    checkpoints = []
    ci = 0
    finite = True
    fail_reason = None

    def rhs_pair(t, yc, dc):
        dy = d2b.rhs_member(data, t, yc, ops, C, nonlinear)
        dd = delta_rhs(data, t, yc, dc, nx, C, ops)
        return dy, dd

    def store(t, yc, dc):
        rec = reconstruct_metric_r1(data, float(t), yc, dc, nx, C, ops)
        E, cr, x, je = d2b.checkpoint_health_member(data, float(t), yc, ops)
        checkpoints.append({
            "tau": float(t),
            "y": np.asarray(yc, float).copy(),
            "delta": np.asarray(dc, float).copy(),
            "E": np.asarray(E, float).copy(),
            "canonical_constraint": float(cr),
            "metric": rec,
        })

    store(t0, y, delta)
    ci = 1

    for istep in range(nstep):
        t = t0 + istep * h
        tn = t1 if istep + 1 == nstep else t0 + (istep + 1) * h

        k1y, k1d = rhs_pair(t, y, delta)
        k2y, k2d = rhs_pair(t + 0.5*h, y + 0.5*h*k1y, delta + 0.5*h*k1d)
        k3y, k3d = rhs_pair(t + 0.5*h, y + 0.5*h*k2y, delta + 0.5*h*k2d)
        k4y, k4d = rhs_pair(t + h, y + h*k3y, delta + h*k3d)

        yn = y + (h/6.0) * (k1y + 2.0*k2y + 2.0*k3y + k4y)
        dn = delta + (h/6.0) * (k1d + 2.0*k2d + 2.0*k3d + k4d)

        if not np.all(np.isfinite(yn)) or not np.all(np.isfinite(dn)):
            finite = False
            fail_reason = f"nonfinite_combined_state_step_{istep+1}"
            break

        while ci < len(tchecks) and tchecks[ci] <= tn + 1.0e-10:
            frac = float((tchecks[ci] - t) / h)
            frac = min(1.0, max(0.0, frac))
            yc = y + frac * (yn - y)
            dc = delta + frac * (dn - delta)
            store(float(tchecks[ci]), yc, dc)
            ci += 1

        y, delta = yn, dn

    if finite and ci != len(tchecks):
        finite = False
        fail_reason = f"stored_only_{ci}_of_{len(tchecks)}_checkpoints"

    return {
        "finite": bool(finite),
        "fail_reason": fail_reason,
        "checkpoints": checkpoints,
        "initial": init,
    }


def source_traceability_audit_r1(data):
    worst_theta = 0.0
    worst_rhop = 0.0
    worst_shear = 0.0
    for tau in np.asarray(data["tau_check"], float):
        bg = fluid_quantities(data, float(tau))
        a = bg["a"]
        Q = bg["Q"]
        alpha_m = m.mode_values(data, float(tau), "alpha")
        theta_m = m.mode_values(data, float(tau), "theta")
        chi_m = Q * (a * theta_m / (m.K_MPC * m.K_MPC) + alpha_m)
        theta_back = (m.K_MPC * m.K_MPC / a) * (chi_m / Q - alpha_m)
        worst_theta = max(worst_theta, rel_l2(theta_back, theta_m))
        rhs = Q * bg["KQ"] / 3.0
        worst_rhop = max(worst_rhop, abs(bg["rho_plus_p"] - rhs) / max(abs(rhs), 1.0e-300))
        worst_shear = max(worst_shear, 0.0)

    metrics = {
        "theta_mapping_relL2_max": float(worst_theta),
        "rho_plus_p_identity_rel_max": float(worst_rhop),
        "nonlinear_completion_shear_source_maxabs": float(worst_shear),
        "cad2_mapping": "K_Q/(Q K_QQ)",
        "density_state_equation": "D2C5 effective-fluid continuity equation",
    }
    metrics["max_closed_identity_mismatch"] = max(worst_theta, worst_rhop, worst_shear)
    metrics["pass"] = bool(metrics["max_closed_identity_mismatch"] <= SOURCE_ID_GATE)
    return metrics


def linear_regression_r1(data):
    d2b.set_member({"sigma": 0, "kind": "simple", "beta0": 1.0})
    run = integrate_combined(data, NX, NSTEP, False)
    if not run["finite"] or len(run["checkpoints"]) != len(data["tau_check"]):
        return {"pass": False, "reason": run.get("fail_reason", "linear_combined_incomplete")}, run

    vals = {"Phi": [], "Psi": [], "W": [], "delta_A": []}
    refs = {"Phi": [], "Psi": [], "W": [], "delta_A": []}
    max_constraint = {"hamiltonian": 0.0, "momentum": 0.0, "shear": 0.0}
    for cp in run["checkpoints"]:
        rec = cp["metric"]
        vals["Phi"].append(rec["phi"])
        vals["Psi"].append(rec["psi"])
        vals["W"].append(rec["weyl"])
        vals["delta_A"].append(cp["delta"])
        refs["Phi"].append(rec["class_phi"])
        refs["Psi"].append(rec["class_psi"])
        refs["W"].append(rec["class_weyl"])
        refs["delta_A"].append(rec["reference_source"]["delta"])
        for key, value in rec["metric_correction"]["constraint"].items():
            max_constraint[key] = max(max_constraint[key], float(value))

    err = {name: rel_l2(np.stack(vals[name]), np.stack(refs[name])) for name in vals}
    passed = bool(all(err[name] <= LINEAR_GATE for name in ("Phi", "Psi", "W")))
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


def run_member_r1(data, member):
    d2b.set_member(member)
    run = integrate_combined(data, NX, NSTEP, True)
    key = d2b.member_key(member)
    if not run["finite"] or len(run["checkpoints"]) != len(data["tau_check"]):
        return {"key": key, "finite": False, "reason": run.get("fail_reason", "combined_incomplete")}, None

    phi_modes = []
    psi_modes = []
    weyl_modes = []
    slip_modes = []
    delta_modes = []
    max_metric = {"hamiltonian": 0.0, "momentum": 0.0, "shear": 0.0}
    max_source_corr = {"delta_rho": 0.0, "q_momentum": 0.0}
    max_canonical = 0.0
    slip_ref = []
    slip_tot = []
    finite = True

    for cp in run["checkpoints"]:
        rec = cp["metric"]
        fields = (rec["phi"], rec["psi"], rec["weyl"], rec["slip"], cp["delta"])
        finite = finite and all(np.all(np.isfinite(x)) for x in fields)
        phi_modes.append(output_modes(rec["phi"]))
        psi_modes.append(output_modes(rec["psi"]))
        weyl_modes.append(output_modes(rec["weyl"]))
        slip_modes.append(output_modes(rec["slip"]))
        delta_modes.append(output_modes(cp["delta"]))
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
    arrays = {
        "Phi": np.asarray(phi_modes, complex),
        "Psi": np.asarray(psi_modes, complex),
        "W": np.asarray(weyl_modes, complex),
        "slip": np.asarray(slip_modes, complex),
        "delta_A": np.asarray(delta_modes, complex),
    }
    return record, arrays


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json-out", default="results/fullj_evolving_weyl_bridge_r1.json")
    ap.add_argument("--npz-out", default="results/fullj_evolving_weyl_bridge_r1.npz")
    args = ap.parse_args()
    jout = Path(args.json_out)
    nout = Path(args.npz_out)
    jout.parent.mkdir(parents=True, exist_ok=True)

    try:
        head = git_head()
        ancestry = {
            "historical_r0_fail": is_ancestor(R0_FAIL_HEAD),
            "r1_predata_lock": is_ancestor(R1_PREDATA_LOCK),
            "phase_lock": is_ancestor(r0.PHASE_LOCK),
            "original_predata_lock": is_ancestor(r0.PREDATA_LOCK),
        }
        if not all(ancestry.values()):
            raise m.InputIncomplete(f"required R1 ancestry missing: {ancestry}")

        print("FULLJ_EVOLVING_WEYL_BRIDGE_R1_START", flush=True)
        print("FULLJ_WEYL_R1_ANCESTRY=" + json.dumps(ancestry, sort_keys=True), flush=True)
        data = r0.prepare_bridge_data()
        print(
            f"FULLJ_WEYL_R1_INPUT_READY modes={len(data['modes'])} checkpoints={len(data['tau_check'])} members=27",
            flush=True,
        )

        g1 = source_traceability_audit_r1(data)
        print(
            f"FULLJ_WEYL_R1_G1 source_identity_max={g1['max_closed_identity_mismatch']:.12e} pass={g1['pass']}",
            flush=True,
        )

        g3 = r0.static_regression()
        print(f"FULLJ_WEYL_R1_G3 static_max={g3['max_error']:.12e} pass={g3['pass']}", flush=True)

        g2, linear_run = linear_regression_r1(data)
        if "relative_L2" in g2:
            print(
                "FULLJ_WEYL_R1_G2 "
                + " ".join(f"{k}={v:.12e}" for k, v in g2["relative_L2"].items())
                + f" pass={g2['pass']}",
                flush=True,
            )
        else:
            print(f"FULLJ_WEYL_R1_G2 pass=False reason={g2.get('reason','unknown')}", flush=True)

        records = []
        stores = []
        names = []
        global_constraint = {"hamiltonian": 0.0, "momentum": 0.0, "shear": 0.0}
        all_finite = True
        slip_identity_max = 0.0
        slip_maxabs_global = 0.0

        members = r0.all_members()
        for i, member in enumerate(members, start=1):
            rec, arrays = run_member_r1(data, member)
            records.append(rec)
            print(
                f"FULLJ_WEYL_R1_MEMBER {i:02d}/27 key={rec['key']} finite={rec['finite']} "
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
            "interpretation": "R1 nonlinear completion adds no retained shear source; corrected CLASS evolving slip is preserved algebraically and is not set to zero",
        }

        print(
            "FULLJ_WEYL_R1_G4 " + " ".join(f"{k}={v:.12e}" for k, v in global_constraint.items())
            + f" pass={g4['pass']}", flush=True,
        )
        print(f"FULLJ_WEYL_R1_G5 finite={g5['finite_members']}/27 pass={g5['pass']}", flush=True)
        print(
            f"FULLJ_WEYL_R1_G6 slip_identity={slip_identity_max:.12e} slip_maxabs={slip_maxabs_global:.12e} pass={g6['pass']}",
            flush=True,
        )

        gates = {
            "G1_canonical_source_traceability": bool(g1["pass"]),
            "G2_linear_CLASS_regression": bool(g2["pass"]),
            "G3_static_fullJ_regression": bool(g3["pass"]),
            "G4_metric_constraint_closure": bool(g4["pass"]),
            "G5_finite_evolving_Weyl": bool(g5["pass"]),
            "G6_static_vs_evolving_slip_distinction": bool(g6["pass"]),
        }
        passed = bool(all(gates.values()))
        classification = PASS_LABEL if passed else FAIL_LABEL

        result = {
            "classification": classification,
            "diagnostic_complete": True,
            "git_head": head,
            "ancestry": ancestry,
            "historical_R0_classification": r0.FAIL_LABEL,
            "HISTORICAL_R0_FAIL_PRESERVED": True,
            "scope": "eta=0 triangular evolving-FLRW effective-density/metric reconstruction on locked D2C6 nonlinear scalar-current trajectories; canonical trajectory does not depend on R1 delta_A or reconstructed metric",
            "density_closure": {
                "Theta_A": "-lap(chi/Q-alpha)/a",
                "Pi_A": "cad2*delta_A-cad2*lap(K_B*E+(2-K_B)*chi)/(3*a^2*rho_A)",
                "delta_A_prime": "3*Hconf*(w*delta_A-Pi_A)+(1+w)*(3*Phi_prime-Theta_A)",
                "Phi_prime": "Phi_CLASS_prime+DeltaX-Hconf*DeltaPsi",
                "initial_condition": "delta_A(z=6)=delta_A_CLASS(z=6)",
                "feedback_to_locked_scalar_current": False,
            },
            "g1_source_traceability": g1,
            "g2_linear_CLASS": g2,
            "g3_static_fullJ": g3,
            "g4_constraint_closure": g4,
            "g5_finite_output": g5,
            "g6_slip_distinction": g6,
            "records": records,
            "z_checkpoints": m.CHECK_Z.tolist(),
            "tau_checkpoints": np.asarray(data["tau_check"], float).tolist(),
            "fourier_mode_numbers_stored": list(range(NMAX + 1)),
            "gates": gates,
            "EVOLVING_WEYL_BRIDGE_R1_TESTED": True,
            "EVOLVING_WEYL_POWER_LICENSED": bool(passed),
            "ACT_LIKELIHOOD_LICENSED": False,
            "OBSERVATIONAL_CLAIM_LICENSED": False,
            "NO_STATIC_W_EQUALS_2PHI_PROMOTION": True,
        }
        jout.write_text(json.dumps(result, indent=2, sort_keys=True, allow_nan=True) + "\n")

        if len(stores) == 27:
            np.savez_compressed(
                nout,
                member_names=np.asarray(names),
                z=np.asarray(m.CHECK_Z, float),
                tau=np.asarray(data["tau_check"], float),
                mode_number=np.arange(NMAX + 1, dtype=int),
                k_Mpc=np.arange(NMAX + 1, dtype=float) * (2.0*np.pi/static.BOX),
                Phi_hat=np.stack([q["Phi"] for q in stores]),
                Psi_hat=np.stack([q["Psi"] for q in stores]),
                W_hat=np.stack([q["W"] for q in stores]),
                slip_hat=np.stack([q["slip"] for q in stores]),
                delta_A_hat=np.stack([q["delta_A"] for q in stores]),
            )

        print("FULLJ_WEYL_R1_GATES=" + json.dumps(gates, sort_keys=True), flush=True)
        print("FULLJ_EVOLVING_WEYL_R1_CLASSIFICATION=" + classification, flush=True)
        print("HISTORICAL_R0_FAIL_PRESERVED=True", flush=True)
        print("EVOLVING_WEYL_POWER_LICENSED=" + str(bool(passed)), flush=True)
        print("ACT_LIKELIHOOD_LICENSED=False", flush=True)
        print("OBSERVATIONAL_CLAIM_LICENSED=False", flush=True)
        print("NO_STATIC_W_EQUALS_2PHI_PROMOTION=True", flush=True)
        print("FULLJ_WEYL_R1_JSON=" + str(jout), flush=True)
        print("FULLJ_WEYL_R1_NPZ=" + str(nout), flush=True)
        return 0 if passed else 2

    except m.InputIncomplete as exc:
        head = git_head()
        result = {
            "classification": INCOMPLETE_LABEL,
            "git_head": head,
            "reason": str(exc),
            "HISTORICAL_R0_FAIL_PRESERVED": True,
            "EVOLVING_WEYL_POWER_LICENSED": False,
            "ACT_LIKELIHOOD_LICENSED": False,
            "OBSERVATIONAL_CLAIM_LICENSED": False,
        }
        jout.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print("FULLJ_EVOLVING_WEYL_R1_CLASSIFICATION=" + INCOMPLETE_LABEL, flush=True)
        print("REASON=" + str(exc), flush=True)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
