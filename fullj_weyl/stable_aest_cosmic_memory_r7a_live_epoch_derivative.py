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

PREDATA_LOCK = "04c15f83032dd8a4a1baf2d26b576b00cc4c2681"
R7_POSTDATA_LOCK = "cf0132f7877160948e1ba4670eda19750d82159b"
R5B_POSTDATA_LOCK = "3242335ece23fbeb743f075a1df1aa70acaab211"
R7_JSON = ROOT / "results/stable_aest_cosmic_memory_r7_lookback_decomposition.json"
R5B_JSON = ROOT / "results/stable_aest_observable_projection_r5b_derivative_zero.json"
R5B_NPZ = ROOT / "results/stable_aest_observable_projection_r5b_derivative_zero.npz"
R5B_JSON_SHA256 = "26ce723e2b7b783fcd19765c9c7f01b6101992a3f09e6ee321299bf148259ca9"
R5B_NPZ_SHA256 = "a88f99254bc1a7393e40691d5dc539bb1e1648eae1b892e43b63f593f8e367e1"

R7_CLASS = "STABLE_AEST_COSMIC_MEMORY_R7_PHYSICAL_BRIDGE_FAIL"
R5B_CLASS = "STABLE_AEST_OBSERVABLE_PROJECTION_R5B_DERIVATIVE_ZERO_CERTIFIED"

EPS_PRIMARY = 0.025
EPS_CONTROL = 0.05
TOL = 3e-8
EPOCHS = ("ancient", "intermediate", "recent_structure", "late")
OBS = ("sigma8", "fsigma8", "ckk")

CLS_INCOMPLETE = "STABLE_AEST_COSMIC_MEMORY_R7A_INCOMPLETE"
CLS_PARENT = "STABLE_AEST_COSMIC_MEMORY_R7A_PARENT_PROVENANCE_FAIL"
CLS_SOURCE = "STABLE_AEST_COSMIC_MEMORY_R7A_SOURCE_TOPOLOGY_FAIL"
CLS_RUN = "STABLE_AEST_COSMIC_MEMORY_R7A_RUN_FAIL"
CLS_CENTRAL = "STABLE_AEST_COSMIC_MEMORY_R7A_CENTRAL_DERIVATIVE_FAIL"
CLS_BRIDGE = "STABLE_AEST_COSMIC_MEMORY_R7A_PHYSICAL_BRIDGE_FAIL"
CLS_RECON = "STABLE_AEST_COSMIC_MEMORY_R7A_EPOCH_RECONSTRUCTION_FAIL"
CLS_PASS = "STABLE_AEST_COSMIC_MEMORY_R7A_LIVE_LOOKBACK_DECOMPOSITION_CERTIFIED"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"],
        cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
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
    root = os.environ.get("AEST_STABLE_R7A_CLASS_ROOT", "")
    if not root:
        return False, {"reason": "AEST_STABLE_R7A_CLASS_ROOT missing"}
    root = Path(root)
    pc = root/"source"/"perturbations.c"
    am = root/"source"/"aest_memory.c"
    ah = root/"include"/"aest_memory.h"
    if not pc.is_file() or not am.is_file() or not ah.is_file():
        return False, {"reason": "R7a source files missing"}
    ptxt = pc.read_text(); atxt = am.read_text(); htxt = ah.read_text()
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


def save_case(path: Path, v: dict):
    np.savez_compressed(
        path,
        sigma8=np.asarray(v["sigma8"], float),
        fsigma8=np.asarray(v["fsigma8"], float),
        ckk=np.asarray(v["ckk"], float),
        ell=np.asarray(v["ell"], float),
        finite=np.asarray([int(v["finite"])]),
        positive=np.asarray([int(v["domain_positive"])]),
        bits=np.asarray([int(v["bits"])]),
        target_pos=np.asarray([int(v["target_pos"])]),
        sigma8_z0_property=np.asarray([float(v["sigma8_z0_property"])]),
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
    mode = str(args.mode)
    if mode not in ("full",) + EPOCHS:
        raise SystemExit(f"unknown R7a worker mode {mode}")
    got = os.environ.get("AEST_R7A_EPOCH_MODE")
    if got != mode:
        raise SystemExit(f"AEST_R7A_EPOCH_MODE mismatch env={got!r} arg={mode!r}")
    v = r5b.run_case(float(args.eta), TOL)
    save_case(Path(args.out), v)
    print(json.dumps({
        "mode": mode, "eta": float(args.eta), "finite": v["finite"],
        "positive": v["domain_positive"], "bits": v["bits"],
        "target_pos": v["target_pos"]
    }, sort_keys=True), flush=True)
    return 0 if v["finite"] and v["domain_positive"] else 2


def contribution_metrics(parts: dict[str, np.ndarray], full: np.ndarray):
    f = np.asarray(full, float)
    f2 = float(np.dot(f, f))
    norms = {e: float(np.linalg.norm(np.asarray(parts[e], float))) for e in EPOCHS}
    norm_sum = max(sum(norms.values()), 1e-300)
    out = {}
    for e in EPOCHS:
        v = np.asarray(parts[e], float)
        out[e] = {
            "signed_projection_fraction": float(np.dot(v, f)/f2) if f2 > 0.0 else float("nan"),
            "norm_share": norms[e]/norm_sum,
            "cosine_with_full": cosine(v, f),
            "tangent_norm": norms[e],
        }
    out["sum_signed_projection_fraction"] = float(sum(out[e]["signed_projection_fraction"] for e in EPOCHS))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--worker", action="store_true")
    ap.add_argument("--mode")
    ap.add_argument("--eta", type=float)
    ap.add_argument("--out")
    ap.add_argument("--json-out", default="results/stable_aest_cosmic_memory_r7a_live_epoch_derivative.json")
    ap.add_argument("--npz-out", default="results/stable_aest_cosmic_memory_r7a_live_epoch_derivative.npz")
    ap.add_argument("--workdir", default="results/stable_aest_cosmic_memory_r7a_work")
    args = ap.parse_args()
    if args.worker:
        if args.mode is None or args.eta is None or args.out is None:
            raise SystemExit("worker requires --mode --eta --out")
        return worker(args)

    print("STABLE_AEST_COSMIC_MEMORY_R7A_START", flush=True)

    req = (R7_JSON, R5B_JSON, R5B_NPZ)
    if any(not p.exists() for p in req):
        out = {"classification": CLS_INCOMPLETE, "diagnostic_complete": False, "reason": "missing R7/R5b parent file"}
        Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True)+"\n")
        print("STABLE_AEST_COSMIC_MEMORY_R7A_CLASSIFICATION="+CLS_INCOMPLETE, flush=True)
        return 3

    r7 = json.loads(R7_JSON.read_text())
    r5j = json.loads(R5B_JSON.read_text())
    r5q = np.load(R5B_NPZ)
    r5_gates = r5j.get("gates", {})
    g1 = bool(
        ancestor(PREDATA_LOCK) and ancestor(R7_POSTDATA_LOCK) and ancestor(R5B_POSTDATA_LOCK)
        and r7.get("classification") == R7_CLASS
        and r7.get("diagnostic_complete") is True
        and sha256(R5B_JSON) == R5B_JSON_SHA256
        and sha256(R5B_NPZ) == R5B_NPZ_SHA256
        and r5j.get("classification") == R5B_CLASS
        and r5j.get("diagnostic_complete") is True
        and r5_gates and all(bool(v) for v in r5_gates.values())
    )
    g2, source_meta = source_topology()
    print("STABLE_AEST_COSMIC_MEMORY_R7A_SOURCE "+json.dumps(source_meta, sort_keys=True), flush=True)

    work = Path(args.workdir); work.mkdir(parents=True, exist_ok=True)
    py = sys.executable
    mod = "fullj_weyl.stable_aest_cosmic_memory_r7a_live_epoch_derivative"

    specs = [("baseline", "full", 0.0)]
    for eps, tag in ((EPS_PRIMARY, "e0p025"), (EPS_CONTROL, "e0p05")):
        specs += [(f"full_p_{tag}", "full", +eps), (f"full_m_{tag}", "full", -eps)]
    for e in EPOCHS:
        specs += [(f"{e}_p", e, +EPS_PRIMARY), (f"{e}_m", e, -EPS_PRIMARY)]

    vals = {}
    runs = []
    all_runs = True
    for name, mode, eta in specs:
        outp = work/f"{name}.npz"
        env = os.environ.copy()
        env["AEST_R7A_EPOCH_MODE"] = mode
        for key in (
            "AEST_TANGENT_FORCE_FILE", "AEST_TANGENT_LAMBDA", "AEST_TANGENT_TRACE_FILE",
            "AEST_R2D_TRACE_FILE", "AEST_R2D_TRACE_KH", "AEST_R2D_TRACE_ALL_K",
            "AEST_TANGENT_ALLOW_K_MISS", "AEST_ERHS_TRACE_FILE", "AEST_ERHS_TRACE_K"
        ):
            env.pop(key, None)
        try:
            subprocess.run(
                [py, "-m", mod, "--worker", "--mode", mode, "--eta", str(eta), "--out", str(outp)],
                cwd=ROOT, env=env, check=True
            )
            v = load_case(outp); vals[name] = v
            ok = bool(v["finite"] and v["domain_positive"]); all_runs &= ok
            runs.append({
                "name": name, "mode": mode, "eta": eta, "finite": v["finite"],
                "domain_positive": v["domain_positive"], "bits": v["bits"],
                "target_pos": v["target_pos"], "sigma8_z0_property": v["sigma8_z0_property"]
            })
            print(f"STABLE_AEST_COSMIC_MEMORY_R7A_RUN name={name} mode={mode} eta={eta:g} finite={v['finite']} positive={v['domain_positive']}", flush=True)
        except Exception as exc:
            all_runs = False
            runs.append({"name": name, "mode": mode, "eta": eta, "finite": False, "domain_positive": False, "error": repr(exc)})
            print(f"STABLE_AEST_COSMIC_MEMORY_R7A_RUN_FAIL name={name} mode={mode} eta={eta:g} error={exc!r}", flush=True)

    arrays = {"z": np.asarray(r5q["z"], float), "ell": np.asarray(r5q["ell"], float)}
    baseline_metrics = {}
    g3 = bool(all_runs and len(vals) == len(specs))
    if g3:
        b = vals["baseline"]
        base_ok = True
        for obs in OBS:
            parent0 = np.asarray(r5q[f"{obs}_nominal_e0"], float)
            bm = metric(b[obs], parent0)
            baseline_metrics[obs] = bm
            base_ok &= bool(bm["E"] <= 1e-10 and bm["C"] >= 0.999999999)
            arrays[f"baseline_{obs}"] = b[obs]
        g3 = bool(g3 and base_ok)

    central_metrics = {}
    bridge_metrics = {}
    recon_metrics = {}
    contributions = {}
    late_z0p2 = {}
    g4 = g5 = g6 = False

    if g3:
        b = vals["baseline"]
        g4_all = g5_all = g6_all = True
        for obs in OBS:
            tf25 = central(vals["full_p_e0p025"][obs], vals["full_m_e0p025"][obs], b[obs], EPS_PRIMARY)
            tf50 = central(vals["full_p_e0p05"][obs], vals["full_m_e0p05"][obs], b[obs], EPS_CONTROL)
            parent = np.asarray(r5q[f"T_{obs}_eta0p01"], float)
            cm = metric(tf25, tf50)
            bm = metric(tf25, parent)
            central_metrics[obs] = cm
            bridge_metrics[obs] = bm
            g4_all &= bool(cm["E"] <= 0.05 and cm["C"] >= 0.995)
            g5_all &= bool(bm["E"] <= 0.10 and bm["C"] >= 0.995)

            parts = {}
            for e in EPOCHS:
                parts[e] = central(vals[f"{e}_p"][obs], vals[f"{e}_m"][obs], b[obs], EPS_PRIMARY)
                arrays[f"T_{e}_{obs}"] = parts[e]
            tsum = sum((parts[e] for e in EPOCHS), np.zeros_like(tf25))
            rm = metric(tsum, tf25)
            recon_metrics[obs] = rm
            g6_all &= bool(rm["E"] <= 0.02 and rm["C"] >= 0.999)

            arrays[f"T_full025_{obs}"] = tf25
            arrays[f"T_full05_{obs}"] = tf50
            arrays[f"T_parent_r5b_{obs}"] = parent
            arrays[f"T_sum_{obs}"] = tsum
            contributions[obs] = contribution_metrics(parts, tf25)

            if obs in ("sigma8", "fsigma8"):
                denom = float(tf25[0])
                late_z0p2[obs] = {e: (float(parts[e][0]/denom) if denom != 0.0 else float("nan")) for e in EPOCHS}
                late_z0p2[obs]["sum"] = float(sum(late_z0p2[obs][e] for e in EPOCHS))

        g4 = bool(g4_all)
        g5 = bool(g5_all)
        g6 = bool(g6_all)

    gates = {
        "R7A_G1_provenance_and_parent_lock": g1,
        "R7A_G2_live_physical_source_topology": g2,
        "R7A_G3_finite_runs_and_baseline_identity": g3,
        "R7A_G4_full_central_derivative_amplitude_consistency": g4,
        "R7A_G5_direct_physical_bridge_to_r5b": g5,
        "R7A_G6_live_epoch_reconstruction": g6,
    }

    if not g1: cls = CLS_PARENT
    elif not g2: cls = CLS_SOURCE
    elif not g3: cls = CLS_RUN
    elif not g4: cls = CLS_CENTRAL
    elif not g5: cls = CLS_BRIDGE
    elif not g6: cls = CLS_RECON
    else: cls = CLS_PASS

    reportable = bool(cls == CLS_PASS)
    summary = {
        "classification": cls,
        "baseline_vs_r5b": baseline_metrics,
        "central_derivative_metrics": central_metrics,
        "physical_r5b_bridge_metrics": bridge_metrics,
        "epoch_reconstruction_metrics": recon_metrics,
        "epoch_contributions": contributions,
        "late_z0p2_signed_epoch_fractions": late_z0p2,
        "gates": gates,
    }
    out = {
        "classification": cls,
        "diagnostic_complete": bool(len(vals) == len(specs)),
        "predata_lock": PREDATA_LOCK,
        "parents": {
            "r7_postdata_lock": R7_POSTDATA_LOCK,
            "r7_classification": r7.get("classification"),
            "r5b_postdata_lock": R5B_POSTDATA_LOCK,
            "r5b_classification": r5j.get("classification"),
            "r5b_json_sha256": sha256(R5B_JSON),
            "r5b_npz_sha256": sha256(R5B_NPZ),
        },
        "settings": {
            "tau_H0": 10.0,
            "memory_order": 20,
            "tol": TOL,
            "epsilon_primary": EPS_PRIMARY,
            "epsilon_control": EPS_CONTROL,
            "epochs": {
                "ancient": "z >= 10",
                "intermediate": "2 <= z < 10",
                "recent_structure": "0.5 <= z < 2",
                "late": "z < 0.5",
            },
            "observable_redshifts": [float(x) for x in r5b.Z],
            "L_min": int(r5b.LMIN),
            "L_max": int(r5b.LMAX),
            "nonlinear_halofit": False,
            "construction": "live physical epoch mask; no force table or external replay hook",
        },
        "source_topology": source_meta,
        "runs": runs,
        "baseline_vs_r5b": baseline_metrics,
        "central_derivative_metrics": central_metrics,
        "physical_r5b_bridge_metrics": bridge_metrics,
        "epoch_reconstruction_metrics": recon_metrics,
        "epoch_contributions": contributions,
        "late_z0p2_signed_epoch_fractions": late_z0p2,
        "gates": gates,
        "interpretation": {
            "lookback_decomposition_licensed": reportable,
            "epoch_fractions_reportable": reportable,
            "observational_detection_claim_licensed": False,
            "tau_generality_claim_licensed": False,
            "universal_entire_universe_memory_claim_licensed": False,
            "r7_reclassified": False,
        },
        "summary": summary,
    }

    Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True)+"\n")
    np.savez_compressed(args.npz_out, **arrays)

    print("STABLE_AEST_COSMIC_MEMORY_R7A_GATES="+json.dumps(gates, sort_keys=True), flush=True)
    print("STABLE_AEST_COSMIC_MEMORY_R7A_SUMMARY="+json.dumps(summary, sort_keys=True), flush=True)
    print("STABLE_AEST_COSMIC_MEMORY_R7A_CLASSIFICATION="+cls, flush=True)
    return 0 if cls == CLS_PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
