#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fullj_weyl import stable_aest_observable_projection_r5b_derivative_zero as r5b

PREDATA_LOCK = "01e6a0adaee514bf859b7730f2784eb3832e02b1"
R7A_POSTDATA_LOCK = "86c03e6ba2ee9fcbf33a9d319d12ae778a747881"
R7A_JSON = ROOT / "results/stable_aest_cosmic_memory_r7a_live_epoch_derivative.json"
R7A_NPZ = ROOT / "results/stable_aest_cosmic_memory_r7a_live_epoch_derivative.npz"
R7A_JSON_SHA256 = "94977acfe47f3f58337ce45dd8df982cd04ff6459434ed9780e229623bc92c0b"
R7A_NPZ_SHA256 = "cc3e9b70809c44c8154abfc4cd3961d5f785f5cd3b327def2666e39bec789771"
R7A_CLASS = "STABLE_AEST_COSMIC_MEMORY_R7A_LIVE_LOOKBACK_DECOMPOSITION_CERTIFIED"

TAUS = (10.0, 5.0, 2.5, 1.25)
EPS_PRIMARY = 0.025
EPS_CONTROL = 0.05
TOL = 3e-8
OBS = ("sigma8", "fsigma8", "ckk")

CLS_INCOMPLETE = "STABLE_AEST_COSMIC_MEMORY_R8A_INCOMPLETE"
CLS_PARENT = "STABLE_AEST_COSMIC_MEMORY_R8A_PARENT_PROVENANCE_FAIL"
CLS_SOURCE = "STABLE_AEST_COSMIC_MEMORY_R8A_SOURCE_TOPOLOGY_FAIL"
CLS_RUN = "STABLE_AEST_COSMIC_MEMORY_R8A_RUN_FAIL"
CLS_BRIDGE = "STABLE_AEST_COSMIC_MEMORY_R8A_TAU10_BRIDGE_FAIL"
CLS_CENTRAL = "STABLE_AEST_COSMIC_MEMORY_R8A_CENTRAL_DERIVATIVE_FAIL"
CLS_RESP = "STABLE_AEST_COSMIC_MEMORY_R8A_RESPONSE_UNRESOLVED"
CLS_PASS = "STABLE_AEST_COSMIC_MEMORY_R8A_TAU_GENERALITY_CERTIFIED"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"], cwd=ROOT,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    ).returncode == 0


def rel(a, b) -> float:
    aa = np.asarray(a, float); bb = np.asarray(b, float)
    return float(np.linalg.norm(aa-bb) / max(float(np.linalg.norm(aa)), float(np.linalg.norm(bb)), 1e-300))


def cosine(a, b) -> float:
    aa = np.asarray(a, float); bb = np.asarray(b, float)
    na = float(np.linalg.norm(aa)); nb = float(np.linalg.norm(bb))
    if na <= 0.0 or nb <= 0.0:
        return float("nan")
    return float(np.dot(aa, bb)/(na*nb))


def metric(a, b):
    return {"E": rel(a, b), "C": cosine(a, b)}


def central(p, m, x0, eps: float):
    return (np.asarray(p, float)-np.asarray(m, float))/(2.0*float(eps)*np.asarray(x0, float))


def derivs_block(text: str) -> str:
    start = text.find("int perturbations_derivs(")
    if start < 0:
        return ""
    rest = text[start+1:]
    m = re.search(r"\nint\s+perturbations_[A-Za-z0-9_]+\s*\(", rest)
    if m is None:
        return text[start:]
    return text[start:start+1+m.start()]


def source_topology():
    root = os.environ.get("AEST_STABLE_R8A_CLASS_ROOT", "")
    if not root:
        return False, {"reason": "AEST_STABLE_R8A_CLASS_ROOT missing"}
    root = Path(root)
    pc = root/"source"/"perturbations.c"
    am = root/"source"/"aest_memory.c"
    ah = root/"include"/"aest_memory.h"
    inp = root/"source"/"input.c"
    if not all(p.is_file() for p in (pc, am, ah, inp)):
        return False, {"reason": "R8a source files missing"}
    ptxt = pc.read_text(); atxt = am.read_text(); htxt = ah.read_text(); itxt = inp.read_text()
    body = derivs_block(ptxt)
    new_mul = "Bchi_aest *= pba->aest_eta*aest_r7a_epoch_weight(a);"
    closure = "E_rhs_aest -= 0.5*Q_aest*Bchi_aest;"
    external_hook = "dy[pv->index_pt_E_aest] += aest_tangent_external_force(k,tau);"
    r2d_hook = "aest_r2d_trace_force(k,pba->h,tau"
    checks = {
        "stable_marker": "FULLJ_AEST_STABLE_CHI_RESIDUAL_V1" in ptxt,
        "stable_chi_rhs": "double chi_aest = Q_aest*s_aest;" in body,
        "r7a_marker": "FULLJ_STABLE_AEST_R7A_LIVE_EPOCH_V1" in ptxt and "FULLJ_STABLE_AEST_R7A_LIVE_EPOCH_V1" in atxt,
        "windowed_eta_multiplier_once": body.count(new_mul) == 1,
        "plain_eta_multiplier_absent": body.count("Bchi_aest *= pba->aest_eta;") == 0,
        "physical_closure_once": body.count(closure) == 1,
        "external_replay_hook_absent": body.count(external_hook) == 0,
        "r2d_trace_hook_absent": body.count(r2d_hook) == 0,
        "epoch_helper_once": len(re.findall(r"\bdouble\s+aest_r7a_epoch_weight\s*\(", atxt)) == 1,
        "epoch_mode_env": "AEST_R7A_EPOCH_MODE" in atxt,
        "epoch_prototype": "double aest_r7a_epoch_weight(double a);" in htxt,
        "signed_eta_guard_absent": "pba->aest_eta < 0." not in itxt,
    }
    meta = {
        "checks": checks,
        "windowed_multiplier_count": body.count(new_mul),
        "closure_count": body.count(closure),
        "external_replay_hook_count": body.count(external_hook),
        "r2d_trace_hook_count": body.count(r2d_hook),
        "epoch_helper_defs": len(re.findall(r"\bdouble\s+aest_r7a_epoch_weight\s*\(", atxt)),
    }
    return bool(all(checks.values())), meta


def run_case(eta: float, tau: float):
    from classy import Class
    params, bits, pos = r5b.build_params(float(eta), TOL)
    params["aest_tau_H0"] = float(tau)
    c = Class(); c.set(params); c.compute()
    try:
        sigma8 = np.asarray([float(c.sigma(8.0, float(z), h_units=True)) for z in r5b.Z], float)
        fsigma8 = np.asarray([float(c.effective_f_sigma8(float(z), z_step=0.1)) for z in r5b.Z], float)
        raw = c.raw_cl(lmax=int(r5b.LMAX))
        if "pp" not in raw:
            raise RuntimeError("CLASS raw_cl has no pp")
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
        "sigma8": np.asarray(q["sigma8"], float), "fsigma8": np.asarray(q["fsigma8"], float),
        "ckk": np.asarray(q["ckk"], float), "ell": np.asarray(q["ell"], float),
        "finite": bool(int(q["finite"][0])), "domain_positive": bool(int(q["positive"][0])),
        "bits": int(q["bits"][0]), "target_pos": int(q["target_pos"][0]),
        "sigma8_z0_property": float(q["sigma8_z0_property"][0]),
    }


def worker(args) -> int:
    got = os.environ.get("AEST_R7A_EPOCH_MODE")
    if got != "full":
        raise SystemExit(f"R8a requires AEST_R7A_EPOCH_MODE='full', got {got!r}")
    v = run_case(float(args.eta), float(args.tau))
    save_case(Path(args.out), v)
    print(json.dumps({
        "tau_H0": float(args.tau), "eta": float(args.eta), "finite": v["finite"],
        "positive": v["domain_positive"], "bits": v["bits"], "target_pos": v["target_pos"]
    }, sort_keys=True), flush=True)
    return 0 if v["finite"] and v["domain_positive"] else 2


def tau_tag(tau: float) -> str:
    return str(tau).replace(".", "p")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--worker", action="store_true")
    ap.add_argument("--tau", type=float)
    ap.add_argument("--eta", type=float)
    ap.add_argument("--out")
    ap.add_argument("--json-out", default="results/stable_aest_cosmic_memory_r8a_tau_amplitude_scan.json")
    ap.add_argument("--npz-out", default="results/stable_aest_cosmic_memory_r8a_tau_amplitude_scan.npz")
    ap.add_argument("--workdir", default="results/stable_aest_cosmic_memory_r8a_tau_amplitude_work")
    args = ap.parse_args()
    if args.worker:
        if args.tau is None or args.eta is None or args.out is None:
            raise SystemExit("worker requires --tau --eta --out")
        return worker(args)

    print("STABLE_AEST_COSMIC_MEMORY_R8A_START", flush=True)
    if not R7A_JSON.exists() or not R7A_NPZ.exists():
        out = {"classification": CLS_INCOMPLETE, "diagnostic_complete": False, "reason": "missing frozen R7a parent"}
        Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True)+"\n")
        print("STABLE_AEST_COSMIC_MEMORY_R8A_CLASSIFICATION="+CLS_INCOMPLETE, flush=True)
        return 3

    r7j = json.loads(R7A_JSON.read_text())
    r7q = np.load(R7A_NPZ)
    g1 = bool(
        ancestor(PREDATA_LOCK) and ancestor(R7A_POSTDATA_LOCK)
        and sha256(R7A_JSON) == R7A_JSON_SHA256
        and sha256(R7A_NPZ) == R7A_NPZ_SHA256
        and r7j.get("classification") == R7A_CLASS
        and r7j.get("diagnostic_complete") is True
        and all(bool(v) for v in r7j.get("gates", {}).values())
    )
    g2, source_meta = source_topology()
    print("STABLE_AEST_COSMIC_MEMORY_R8A_SOURCE "+json.dumps(source_meta, sort_keys=True), flush=True)

    work = Path(args.workdir); work.mkdir(parents=True, exist_ok=True)
    py = sys.executable
    mod = "fullj_weyl.stable_aest_cosmic_memory_r8a_tau_amplitude_scan"
    specs = []
    for tau in TAUS:
        specs.append((tau, 0.0, "e0"))
        specs.append((tau, +EPS_PRIMARY, "p025"))
        specs.append((tau, -EPS_PRIMARY, "m025"))
        specs.append((tau, +EPS_CONTROL, "p05"))
        specs.append((tau, -EPS_CONTROL, "m05"))

    vals = {}; runs = []; all_runs = True
    for tau, eta, etag in specs:
        key = f"tau{tau_tag(tau)}_{etag}"
        outp = work/f"{key}.npz"
        env = os.environ.copy(); env["AEST_R7A_EPOCH_MODE"] = "full"
        for x in (
            "AEST_TANGENT_FORCE_FILE", "AEST_TANGENT_LAMBDA", "AEST_TANGENT_TRACE_FILE",
            "AEST_R2D_TRACE_FILE", "AEST_R2D_TRACE_KH", "AEST_R2D_TRACE_ALL_K",
            "AEST_TANGENT_ALLOW_K_MISS", "AEST_ERHS_TRACE_FILE", "AEST_ERHS_TRACE_K"
        ):
            env.pop(x, None)
        try:
            subprocess.run([py, "-m", mod, "--worker", "--tau", str(tau), "--eta", str(eta), "--out", str(outp)],
                           cwd=ROOT, env=env, check=True)
            v = load_case(outp); vals[key] = v
            ok = bool(v["finite"] and v["domain_positive"]); all_runs &= ok
            runs.append({"name": key, "tau_H0": tau, "eta": eta, "finite": v["finite"],
                         "domain_positive": v["domain_positive"], "bits": v["bits"],
                         "target_pos": v["target_pos"], "sigma8_z0_property": v["sigma8_z0_property"]})
            print(f"STABLE_AEST_COSMIC_MEMORY_R8A_RUN name={key} tau={tau:g} eta={eta:g} finite={v['finite']} positive={v['domain_positive']}", flush=True)
        except Exception as exc:
            all_runs = False
            runs.append({"name": key, "tau_H0": tau, "eta": eta, "finite": False, "domain_positive": False, "error": repr(exc)})
            print(f"STABLE_AEST_COSMIC_MEMORY_R8A_RUN_FAIL name={key} tau={tau:g} eta={eta:g} error={exc!r}", flush=True)

    arrays = {"z": np.asarray(r7q["z"], float), "ell": np.asarray(r7q["ell"], float), "tau_grid": np.asarray(TAUS, float)}
    baseline_metrics = {}
    g3 = bool(all_runs and len(vals) == len(specs))
    if g3:
        ref = vals[f"tau{tau_tag(10.0)}_e0"]
        base_all = True
        for tau in TAUS:
            key = f"tau{tau_tag(tau)}_e0"
            baseline_metrics[str(tau)] = {}
            for obs in OBS:
                bm = metric(vals[key][obs], ref[obs])
                baseline_metrics[str(tau)][obs] = bm
                base_all &= bool(bm["E"] <= 1e-10 and bm["C"] >= 0.9999999999)
                arrays[f"baseline_tau{tau_tag(tau)}_{obs}"] = vals[key][obs]
        g3 = bool(g3 and base_all)

    central_metrics = {}; tau10_bridge = {}; tau_response = {}
    g4 = g5 = g6 = False
    if g3:
        g4_all = g5_all = g6_all = True
        tau10_tangents = {}
        for tau in TAUS:
            tag = tau_tag(tau)
            b = vals[f"tau{tag}_e0"]
            central_metrics[str(tau)] = {}
            tau_response[str(tau)] = {}
            for obs in OBS:
                t25 = central(vals[f"tau{tag}_p025"][obs], vals[f"tau{tag}_m025"][obs], b[obs], EPS_PRIMARY)
                t50 = central(vals[f"tau{tag}_p05"][obs], vals[f"tau{tag}_m05"][obs], b[obs], EPS_CONTROL)
                cm = metric(t25, t50)
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
            bm = metric(tau10_tangents[obs], parent)
            tau10_bridge[obs] = bm
            g4_all &= bool(bm["E"] <= 0.02 and bm["C"] >= 0.999)
            arrays[f"T_parent_r7a_tau10_{obs}"] = parent

        for tau in TAUS:
            tag = tau_tag(tau)
            for obs in OBS:
                t = arrays[f"T_tau{tag}_{obs}_eps025"]
                tref = tau10_tangents[obs]
                tau_response[str(tau)][obs]["amplitude_ratio_to_tau10"] = float(np.linalg.norm(t)/max(np.linalg.norm(tref), 1e-300))
                tau_response[str(tau)][obs]["cosine_to_tau10"] = cosine(t, tref)

        g4 = bool(g4_all); g5 = bool(g5_all); g6 = bool(g6_all)

    gates = {
        "R8A_G1_provenance_and_parent_lock": g1,
        "R8A_G2_direct_physical_source_topology": g2,
        "R8A_G3_finite_tau_grid_runs_and_eta0_identity": g3,
        "R8A_G4_tau10_parent_derivative_bridge": g4,
        "R8A_G5_central_derivative_consistency_across_tau": g5,
        "R8A_G6_resolved_response_across_tau": g6,
    }
    if not g1: cls = CLS_PARENT
    elif not g2: cls = CLS_SOURCE
    elif not g3: cls = CLS_RUN
    elif not g4: cls = CLS_BRIDGE
    elif not g5: cls = CLS_CENTRAL
    elif not g6: cls = CLS_RESP
    else: cls = CLS_PASS

    reportable = bool(cls == CLS_PASS)
    summary = {
        "classification": cls,
        "baseline_metrics": baseline_metrics,
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
            "r7a_json_sha256": sha256(R7A_JSON),
            "r7a_npz_sha256": sha256(R7A_NPZ),
        },
        "settings": {
            "tau_H0_grid": list(TAUS), "memory_order": 20, "tol": TOL,
            "epsilon_primary": EPS_PRIMARY, "epsilon_control": EPS_CONTROL,
            "epoch_mode": "full", "observable_redshifts": [float(x) for x in r5b.Z],
            "L_min": int(r5b.LMIN), "L_max": int(r5b.LMAX), "nonlinear_halofit": False,
            "construction": "direct physical full-memory central derivative; R7a live source; no replay",
        },
        "source_topology": source_meta,
        "runs": runs,
        "baseline_metrics": baseline_metrics,
        "tau10_parent_bridge": tau10_bridge,
        "central_derivative_metrics": central_metrics,
        "tau_response": tau_response,
        "gates": gates,
        "interpretation": {
            "tau_generality_reportable": reportable,
            "tau_amplitude_shape_reportable": reportable,
            "lookback_at_new_tau_licensed": False,
            "observational_detection_claim_licensed": False,
            "tau_below_1p25_claim_licensed": False,
            "monotonic_extrapolation_licensed": False,
        },
        "summary": summary,
    }
    Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True)+"\n")
    np.savez_compressed(args.npz_out, **arrays)
    print("STABLE_AEST_COSMIC_MEMORY_R8A_GATES="+json.dumps(gates, sort_keys=True), flush=True)
    print("STABLE_AEST_COSMIC_MEMORY_R8A_SUMMARY="+json.dumps(summary, sort_keys=True), flush=True)
    print("STABLE_AEST_COSMIC_MEMORY_R8A_CLASSIFICATION="+cls, flush=True)
    return 0 if cls == CLS_PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
