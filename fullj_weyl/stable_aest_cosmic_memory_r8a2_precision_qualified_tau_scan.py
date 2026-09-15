#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fullj_weyl import stable_aest_cosmic_memory_r8a_tau_amplitude_scan as r8a
from fullj_weyl import stable_aest_observable_projection_r5b_derivative_zero as r5b

PREDATA_LOCK = "e01db75882717b7f2e230d634ff8f930604d8011"
R7A_POSTDATA_LOCK = "86c03e6ba2ee9fcbf33a9d319d12ae778a747881"
R8A_POSTDATA_LOCK = "9b138cf04d3a8c323bbf3a82e3e747deea0393dc"
R7A_JSON = ROOT / "results/stable_aest_cosmic_memory_r7a_live_epoch_derivative.json"
R7A_NPZ = ROOT / "results/stable_aest_cosmic_memory_r7a_live_epoch_derivative.npz"
R8A_JSON = ROOT / "results/stable_aest_cosmic_memory_r8a_tau_amplitude_scan.json"

R7A_CLASS = "STABLE_AEST_COSMIC_MEMORY_R7A_LIVE_LOOKBACK_DECOMPOSITION_CERTIFIED"
R8A_CLASS = "STABLE_AEST_COSMIC_MEMORY_R8A_RUN_FAIL"

TAUS = (10.0, 5.0, 2.5, 1.25)
EPS_PRIMARY = 0.025
EPS_CONTROL = 0.05
TOL_NOMINAL = 3e-8
TOL_TIGHT = 1e-8
OBS = ("sigma8", "fsigma8", "ckk")

CLS_INCOMPLETE = "STABLE_AEST_COSMIC_MEMORY_R8A2_INCOMPLETE"
CLS_PARENT = "STABLE_AEST_COSMIC_MEMORY_R8A2_PARENT_PROVENANCE_FAIL"
CLS_SOURCE = "STABLE_AEST_COSMIC_MEMORY_R8A2_SOURCE_TOPOLOGY_FAIL"
CLS_RUNPREC = "STABLE_AEST_COSMIC_MEMORY_R8A2_RUN_OR_PRECISION_FAIL"
CLS_BRIDGE = "STABLE_AEST_COSMIC_MEMORY_R8A2_TAU10_BRIDGE_FAIL"
CLS_CENTRAL = "STABLE_AEST_COSMIC_MEMORY_R8A2_CENTRAL_DERIVATIVE_FAIL"
CLS_RESP = "STABLE_AEST_COSMIC_MEMORY_R8A2_RESPONSE_UNRESOLVED"
CLS_PASS = "STABLE_AEST_COSMIC_MEMORY_R8A2_TAU_GENERALITY_CERTIFIED"


def ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"], cwd=ROOT,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    ).returncode == 0


def run_case(eta: float, tau: float, tol: float):
    from classy import Class
    params, bits, pos = r5b.build_params(float(eta), float(tol))
    params["aest_tau_H0"] = float(tau)
    c = Class(); c.set(params); c.compute()
    try:
        sigma8 = np.asarray([float(c.sigma(8.0, float(z), h_units=True)) for z in r5b.Z], float)
        fsigma8 = np.asarray([float(c.effective_f_sigma8(float(z), z_step=0.1)) for z in r5b.Z], float)
        raw = c.raw_cl(lmax=int(r5b.LMAX))
        pp = np.asarray(raw["pp"], float)
        ell_all = np.arange(pp.size, dtype=float)
        sel = (ell_all >= r5b.LMIN) & (ell_all <= r5b.LMAX)
        ell = ell_all[sel]
        ckk = ((ell*(ell+1.0)/2.0)**2) * pp[sel]
        finite = bool(np.all(np.isfinite(sigma8)) and np.all(np.isfinite(fsigma8)) and np.all(np.isfinite(ckk)))
        positive = bool(np.all(sigma8 > 0.0) and np.all(ckk > 0.0))
        return {
            "sigma8": sigma8, "fsigma8": fsigma8, "ckk": ckk, "ell": ell,
            "finite": finite, "domain_positive": positive, "bits": int(bits),
            "target_pos": int(pos), "sigma8_z0_property": float(c.sigma8()),
        }
    finally:
        c.struct_cleanup(); c.empty()


def save_case(path: Path, v: dict):
    np.savez_compressed(
        path,
        sigma8=v["sigma8"], fsigma8=v["fsigma8"], ckk=v["ckk"], ell=v["ell"],
        finite=np.asarray([int(v["finite"])]), positive=np.asarray([int(v["domain_positive"])]),
        bits=np.asarray([v["bits"]]), target_pos=np.asarray([v["target_pos"]]),
        sigma8_z0_property=np.asarray([v["sigma8_z0_property"]]),
    )


def load_case(path: Path):
    q = np.load(path)
    return {
        "sigma8": np.asarray(q["sigma8"], float),
        "fsigma8": np.asarray(q["fsigma8"], float),
        "ckk": np.asarray(q["ckk"], float),
        "ell": np.asarray(q["ell"], float),
        "finite": bool(int(q["finite"][0])),
        "domain_positive": bool(int(q["positive"][0])),
        "bits": int(q["bits"][0]),
        "target_pos": int(q["target_pos"][0]),
        "sigma8_z0_property": float(q["sigma8_z0_property"][0]),
    }


def worker(args) -> int:
    if os.environ.get("AEST_R7A_EPOCH_MODE") != "full":
        raise SystemExit("R8a2 requires AEST_R7A_EPOCH_MODE=full")
    v = run_case(float(args.eta), float(args.tau), float(args.tol))
    save_case(Path(args.out), v)
    print(json.dumps({
        "tau_H0": float(args.tau), "eta": float(args.eta), "tol": float(args.tol),
        "finite": v["finite"], "positive": v["domain_positive"],
        "bits": v["bits"], "target_pos": v["target_pos"],
    }, sort_keys=True), flush=True)
    return 0 if v["finite"] and v["domain_positive"] else 2


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--worker", action="store_true")
    ap.add_argument("--tau", type=float)
    ap.add_argument("--eta", type=float)
    ap.add_argument("--tol", type=float)
    ap.add_argument("--out")
    ap.add_argument("--json-out", default="results/stable_aest_cosmic_memory_r8a2_precision_qualified_tau_scan.json")
    ap.add_argument("--npz-out", default="results/stable_aest_cosmic_memory_r8a2_precision_qualified_tau_scan.npz")
    ap.add_argument("--workdir", default="results/stable_aest_cosmic_memory_r8a2_work")
    args = ap.parse_args()
    if args.worker:
        if None in (args.tau, args.eta, args.tol, args.out):
            raise SystemExit("worker requires --tau --eta --tol --out")
        return worker(args)

    print("STABLE_AEST_COSMIC_MEMORY_R8A2_START", flush=True)
    if not (R7A_JSON.exists() and R7A_NPZ.exists() and R8A_JSON.exists()):
        out = {"classification": CLS_INCOMPLETE, "diagnostic_complete": False, "reason": "missing parent result"}
        Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True)+"\n")
        print("STABLE_AEST_COSMIC_MEMORY_R8A2_CLASSIFICATION="+CLS_INCOMPLETE, flush=True)
        return 3

    r7j = json.loads(R7A_JSON.read_text())
    r7q = np.load(R7A_NPZ)
    r8j = json.loads(R8A_JSON.read_text())
    g1 = bool(
        ancestor(PREDATA_LOCK) and ancestor(R7A_POSTDATA_LOCK) and ancestor(R8A_POSTDATA_LOCK)
        and r7j.get("classification") == R7A_CLASS
        and r7j.get("diagnostic_complete") is True
        and all(bool(v) for v in r7j.get("gates", {}).values())
        and r8j.get("classification") == R8A_CLASS
        and r8j.get("diagnostic_complete") is True
    )
    g2, source_meta = r8a.source_topology()
    print("STABLE_AEST_COSMIC_MEMORY_R8A2_SOURCE "+json.dumps(source_meta, sort_keys=True), flush=True)

    work = Path(args.workdir); work.mkdir(parents=True, exist_ok=True)
    py = sys.executable
    mod = "fullj_weyl.stable_aest_cosmic_memory_r8a2_precision_qualified_tau_scan"
    specs = []
    for tau in TAUS:
        specs += [
            (tau, 0.0, TOL_NOMINAL, "e0"),
            (tau, +EPS_PRIMARY, TOL_NOMINAL, "p025"),
            (tau, -EPS_PRIMARY, TOL_NOMINAL, "m025"),
            (tau, +EPS_CONTROL, TOL_NOMINAL, "p05"),
            (tau, -EPS_CONTROL, TOL_NOMINAL, "m05"),
            (tau, 0.0, TOL_TIGHT, "e0_tight"),
        ]

    vals = {}; runs = []; all_runs = True
    for tau, eta, tol, tag in specs:
        key = f"tau{r8a.tau_tag(tau)}_{tag}"
        outp = work/f"{key}.npz"
        env = os.environ.copy(); env["AEST_R7A_EPOCH_MODE"] = "full"
        for x in (
            "AEST_TANGENT_FORCE_FILE", "AEST_TANGENT_LAMBDA", "AEST_TANGENT_TRACE_FILE",
            "AEST_R2D_TRACE_FILE", "AEST_R2D_TRACE_KH", "AEST_R2D_TRACE_ALL_K",
            "AEST_TANGENT_ALLOW_K_MISS", "AEST_ERHS_TRACE_FILE", "AEST_ERHS_TRACE_K"
        ):
            env.pop(x, None)
        try:
            subprocess.run(
                [py, "-m", mod, "--worker", "--tau", str(tau), "--eta", str(eta),
                 "--tol", str(tol), "--out", str(outp)], cwd=ROOT, env=env, check=True
            )
            v = load_case(outp); vals[key] = v
            ok = bool(v["finite"] and v["domain_positive"]); all_runs &= ok
            runs.append({"name": key, "tau_H0": tau, "eta": eta, "tol": tol,
                         "finite": v["finite"], "domain_positive": v["domain_positive"],
                         "bits": v["bits"], "target_pos": v["target_pos"],
                         "sigma8_z0_property": v["sigma8_z0_property"]})
            print(f"STABLE_AEST_COSMIC_MEMORY_R8A2_RUN name={key} tau={tau:g} eta={eta:g} tol={tol:.1e} finite={v['finite']} positive={v['domain_positive']}", flush=True)
        except Exception as exc:
            all_runs = False
            runs.append({"name": key, "tau_H0": tau, "eta": eta, "tol": tol,
                         "finite": False, "domain_positive": False, "error": repr(exc)})
            print(f"STABLE_AEST_COSMIC_MEMORY_R8A2_RUN_FAIL name={key} error={exc!r}", flush=True)

    arrays = {"z": np.asarray(r7q["z"], float), "ell": np.asarray(r7q["ell"], float), "tau_grid": np.asarray(TAUS, float)}
    baseline_precision = {}; cross_tau_baseline = {}
    g3 = bool(all_runs and len(vals) == len(specs))
    if g3:
        prec_all = True
        ref = vals[f"tau{r8a.tau_tag(10.0)}_e0"]
        for tau in TAUS:
            tag = r8a.tau_tag(tau)
            b = vals[f"tau{tag}_e0"]
            bt = vals[f"tau{tag}_e0_tight"]
            baseline_precision[str(tau)] = {}
            cross_tau_baseline[str(tau)] = {}
            for obs in OBS:
                pm = r8a.metric(b[obs], bt[obs])
                dm = r8a.metric(b[obs], ref[obs])
                baseline_precision[str(tau)][obs] = pm
                cross_tau_baseline[str(tau)][obs] = dm
                prec_all &= bool(pm["E"] <= 1e-7 and pm["C"] >= 0.99999999)
                arrays[f"baseline_tau{tag}_{obs}"] = b[obs]
                arrays[f"baseline_tight_tau{tag}_{obs}"] = bt[obs]
        g3 = bool(g3 and prec_all)

    central_metrics = {}; tau10_bridge = {}; tau_response = {}
    g4 = g5 = g6 = False
    if g3:
        g4_all = g5_all = g6_all = True
        tau10_tangents = {}
        for tau in TAUS:
            tag = r8a.tau_tag(tau)
            b = vals[f"tau{tag}_e0"]
            central_metrics[str(tau)] = {}
            tau_response[str(tau)] = {}
            for obs in OBS:
                t25 = r8a.central(vals[f"tau{tag}_p025"][obs], vals[f"tau{tag}_m025"][obs], b[obs], EPS_PRIMARY)
                t50 = r8a.central(vals[f"tau{tag}_p05"][obs], vals[f"tau{tag}_m05"][obs], b[obs], EPS_CONTROL)
                cm = r8a.metric(t25, t50)
                central_metrics[str(tau)][obs] = cm
                g5_all &= bool(cm["E"] <= 0.10 and cm["C"] >= 0.995)
                nrm = float(np.linalg.norm(t25))
                g6_all &= bool(np.isfinite(nrm) and nrm > 0.0)
                arrays[f"T_tau{tag}_{obs}_eps025"] = t25
                arrays[f"T_tau{tag}_{obs}_eps05"] = t50
                tau_response[str(tau)][obs] = {
                    "norm_primary": nrm,
                    "min_primary": float(np.min(t25)),
                    "max_primary": float(np.max(t25)),
                }
                if tau == 10.0:
                    tau10_tangents[obs] = t25

        for obs in OBS:
            parent = np.asarray(r7q[f"T_full025_{obs}"], float)
            bm = r8a.metric(tau10_tangents[obs], parent)
            tau10_bridge[obs] = bm
            g4_all &= bool(bm["E"] <= 0.02 and bm["C"] >= 0.999)
            arrays[f"T_parent_r7a_tau10_{obs}"] = parent

        for tau in TAUS:
            tag = r8a.tau_tag(tau)
            for obs in OBS:
                t = arrays[f"T_tau{tag}_{obs}_eps025"]
                tref = tau10_tangents[obs]
                tau_response[str(tau)][obs]["amplitude_ratio_to_tau10"] = float(np.linalg.norm(t)/max(np.linalg.norm(tref), 1e-300))
                tau_response[str(tau)][obs]["cosine_to_tau10"] = r8a.cosine(t, tref)

        g4 = bool(g4_all); g5 = bool(g5_all); g6 = bool(g6_all)

    gates = {
        "R8A2_G1_provenance_and_parent_lock": g1,
        "R8A2_G2_direct_physical_source_topology": g2,
        "R8A2_G3_finite_runs_and_same_tau_eta0_precision": g3,
        "R8A2_G4_tau10_parent_derivative_bridge": g4,
        "R8A2_G5_central_derivative_consistency_across_tau": g5,
        "R8A2_G6_resolved_response_across_tau": g6,
    }
    if not g1: cls = CLS_PARENT
    elif not g2: cls = CLS_SOURCE
    elif not g3: cls = CLS_RUNPREC
    elif not g4: cls = CLS_BRIDGE
    elif not g5: cls = CLS_CENTRAL
    elif not g6: cls = CLS_RESP
    else: cls = CLS_PASS

    reportable = bool(cls == CLS_PASS)
    summary = {
        "classification": cls,
        "baseline_precision_metrics": baseline_precision,
        "cross_tau_eta0_diagnostic": cross_tau_baseline,
        "tau10_parent_bridge": tau10_bridge,
        "central_derivative_metrics": central_metrics,
        "tau_response": tau_response,
        "gates": gates,
    }
    out = {
        "classification": cls,
        "diagnostic_complete": bool(len(vals) == len(specs)),
        "predata_lock": PREDATA_LOCK,
        "parents": {
            "r7a_postdata_lock": R7A_POSTDATA_LOCK,
            "r7a_classification": r7j.get("classification"),
            "r8a_postdata_lock": R8A_POSTDATA_LOCK,
            "r8a_classification": r8j.get("classification"),
        },
        "settings": {
            "tau_H0_grid": list(TAUS), "memory_order": 20,
            "tol_nominal": TOL_NOMINAL, "tol_tight_eta0": TOL_TIGHT,
            "epsilon_primary": EPS_PRIMARY, "epsilon_control": EPS_CONTROL,
            "epoch_mode": "full", "nonlinear_halofit": False,
            "observable_redshifts": [float(x) for x in r5b.Z],
            "L_min": int(r5b.LMIN), "L_max": int(r5b.LMAX),
            "cross_tau_eta0_is_gating": False,
            "construction": "direct physical same-tau central derivative with tight eta-zero precision controls",
        },
        "source_topology": source_meta,
        "runs": runs,
        "baseline_precision_metrics": baseline_precision,
        "cross_tau_eta0_diagnostic": cross_tau_baseline,
        "tau10_parent_bridge": tau10_bridge,
        "central_derivative_metrics": central_metrics,
        "tau_response": tau_response,
        "gates": gates,
        "interpretation": {
            "tau_amplitude_shape_reportable": reportable,
            "tau_generality_reportable": reportable,
            "lookback_at_new_tau_licensed": False,
            "monotonic_extrapolation_licensed": False,
            "tau_below_1p25_claim_licensed": False,
            "observational_detection_claim_licensed": False,
            "r8a_reclassified": False,
        },
        "summary": summary,
    }
    Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True)+"\n")
    np.savez_compressed(args.npz_out, **arrays)
    print("STABLE_AEST_COSMIC_MEMORY_R8A2_GATES="+json.dumps(gates, sort_keys=True), flush=True)
    print("STABLE_AEST_COSMIC_MEMORY_R8A2_SUMMARY="+json.dumps(summary, sort_keys=True), flush=True)
    print("STABLE_AEST_COSMIC_MEMORY_R8A2_CLASSIFICATION="+cls, flush=True)
    return 0 if cls == CLS_PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
