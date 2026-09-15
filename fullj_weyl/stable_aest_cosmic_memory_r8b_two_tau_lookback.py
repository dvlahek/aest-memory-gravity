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

from fullj_weyl import stable_aest_cosmic_memory_r8a_tau_amplitude_scan as r8a
from fullj_weyl import stable_aest_cosmic_memory_r8a2_precision_qualified_tau_scan as r8a2

PREDATA_LOCK = "26ad0f310e0cc203c3350330a17e6822771515a0"
R7A_POSTDATA_LOCK = "86c03e6ba2ee9fcbf33a9d319d12ae778a747881"
R8A2_POSTDATA_LOCK = "590dbc69e2823f583b157af2297e357991103c47"

R7A_JSON = ROOT / "results/stable_aest_cosmic_memory_r7a_live_epoch_derivative.json"
R7A_NPZ = ROOT / "results/stable_aest_cosmic_memory_r7a_live_epoch_derivative.npz"
R8A2_JSON = ROOT / "results/stable_aest_cosmic_memory_r8a2_precision_qualified_tau_scan.json"
R8A2_NPZ = ROOT / "results/stable_aest_cosmic_memory_r8a2_precision_qualified_tau_scan.npz"

R7A_JSON_SHA256 = "94977acfe47f3f58337ce45dd8df982cd04ff6459434ed9780e229623bc92c0b"
R7A_NPZ_SHA256 = "cc3e9b70809c44c8154abfc4cd3961d5f785f5cd3b327def2666e39bec789771"
R8A2_JSON_SHA256 = "2d6289c2fbd37bebcb904dade89f64c15a009e5c7454754b39d4dcc72924ca66"
R8A2_NPZ_SHA256 = "c81b2093a88719423e87ff5c180d790a56da6f396c0070858624879c90f26ee1"

R7A_CLASS = "STABLE_AEST_COSMIC_MEMORY_R7A_LIVE_LOOKBACK_DECOMPOSITION_CERTIFIED"
R8A2_CLASS = "STABLE_AEST_COSMIC_MEMORY_R8A2_TAU_GENERALITY_CERTIFIED"

TAU = 1.25
EPS_PRIMARY = 0.025
EPS_CONTROL = 0.05
TOL = 3e-8
EPOCHS = ("ancient", "intermediate", "recent_structure", "late")
OBS = ("sigma8", "fsigma8", "ckk")

CLS_INCOMPLETE = "STABLE_AEST_COSMIC_MEMORY_R8B_INCOMPLETE"
CLS_PARENT = "STABLE_AEST_COSMIC_MEMORY_R8B_PARENT_PROVENANCE_FAIL"
CLS_SOURCE = "STABLE_AEST_COSMIC_MEMORY_R8B_SOURCE_TOPOLOGY_FAIL"
CLS_RUN = "STABLE_AEST_COSMIC_MEMORY_R8B_RUN_OR_BASELINE_FAIL"
CLS_CENTRAL = "STABLE_AEST_COSMIC_MEMORY_R8B_CENTRAL_DERIVATIVE_FAIL"
CLS_BRIDGE = "STABLE_AEST_COSMIC_MEMORY_R8B_R8A2_BRIDGE_FAIL"
CLS_RECON = "STABLE_AEST_COSMIC_MEMORY_R8B_EPOCH_RECONSTRUCTION_FAIL"
CLS_COMPONENT = "STABLE_AEST_COSMIC_MEMORY_R8B_EPOCH_COMPONENT_UNRESOLVED"
CLS_PASS = "STABLE_AEST_COSMIC_MEMORY_R8B_TWO_TAU_LOOKBACK_CERTIFIED"


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


def derivs_block(text: str) -> str:
    start = text.find("int perturbations_derivs(")
    if start < 0:
        return ""
    rest = text[start + 1:]
    m = re.search(r"\nint\s+perturbations_[A-Za-z0-9_]+\s*\(", rest)
    if m is None:
        return text[start:]
    return text[start:start + 1 + m.start()]


def source_topology():
    root = os.environ.get("AEST_STABLE_R8B_CLASS_ROOT", "")
    if not root:
        return False, {"reason": "AEST_STABLE_R8B_CLASS_ROOT missing"}
    root = Path(root)
    pc = root / "source" / "perturbations.c"
    am = root / "source" / "aest_memory.c"
    ah = root / "include" / "aest_memory.h"
    inp = root / "source" / "input.c"
    if not all(p.is_file() for p in (pc, am, ah, inp)):
        return False, {"reason": "R8b source files missing"}
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
        "signed_eta_marker_once": itxt.count("FULLJ_STABLE_AEST_R7A_SIGNED_ETA_DIAGNOSTIC_V1") == 1,
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


def worker(args) -> int:
    mode = str(args.mode)
    if mode not in ("full",) + EPOCHS:
        raise SystemExit(f"unknown R8b mode {mode}")
    got = os.environ.get("AEST_R7A_EPOCH_MODE")
    if got != mode:
        raise SystemExit(f"AEST_R7A_EPOCH_MODE mismatch env={got!r} arg={mode!r}")
    v = r8a2.run_case(float(args.eta), TAU, TOL)
    r8a2.save_case(Path(args.out), v)
    print(json.dumps({
        "mode": mode, "tau_H0": TAU, "eta": float(args.eta),
        "finite": v["finite"], "positive": v["domain_positive"],
        "bits": v["bits"], "target_pos": v["target_pos"],
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
            "signed_projection_fraction": float(np.dot(v, f) / f2) if f2 > 0.0 else float("nan"),
            "norm_share": norms[e] / norm_sum,
            "cosine_with_full": r8a.cosine(v, f),
            "tangent_norm": norms[e],
        }
    out["sum_signed_projection_fraction"] = float(sum(out[e]["signed_projection_fraction"] for e in EPOCHS))
    out["early_signed_projection_fraction"] = float(out["ancient"]["signed_projection_fraction"] + out["intermediate"]["signed_projection_fraction"])
    out["late_signed_projection_fraction"] = float(out["recent_structure"]["signed_projection_fraction"] + out["late"]["signed_projection_fraction"])
    out["early_norm_share"] = float(out["ancient"]["norm_share"] + out["intermediate"]["norm_share"])
    out["late_norm_share"] = float(out["recent_structure"]["norm_share"] + out["late"]["norm_share"])
    return out


def zero_crossings(ell: np.ndarray, y: np.ndarray):
    x = np.asarray(ell, float); v = np.asarray(y, float)
    out = []
    for i in range(len(v) - 1):
        y0 = float(v[i]); y1 = float(v[i + 1])
        if not np.isfinite(y0) or not np.isfinite(y1):
            continue
        if y0 == 0.0:
            out.append(float(x[i]))
        elif y0 * y1 < 0.0:
            frac = -y0 / (y1 - y0)
            out.append(float(x[i] + frac * (x[i + 1] - x[i])))
    if len(v) and float(v[-1]) == 0.0:
        out.append(float(x[-1]))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--worker", action="store_true")
    ap.add_argument("--mode")
    ap.add_argument("--eta", type=float)
    ap.add_argument("--out")
    ap.add_argument("--json-out", default="results/stable_aest_cosmic_memory_r8b_two_tau_lookback.json")
    ap.add_argument("--npz-out", default="results/stable_aest_cosmic_memory_r8b_two_tau_lookback.npz")
    ap.add_argument("--workdir", default="results/stable_aest_cosmic_memory_r8b_work")
    args = ap.parse_args()
    if args.worker:
        if args.mode is None or args.eta is None or args.out is None:
            raise SystemExit("worker requires --mode --eta --out")
        return worker(args)

    print("STABLE_AEST_COSMIC_MEMORY_R8B_START", flush=True)
    req = (R7A_JSON, R7A_NPZ, R8A2_JSON, R8A2_NPZ)
    if any(not p.exists() for p in req):
        out = {"classification": CLS_INCOMPLETE, "diagnostic_complete": False, "reason": "missing frozen parent result"}
        Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
        print("STABLE_AEST_COSMIC_MEMORY_R8B_CLASSIFICATION=" + CLS_INCOMPLETE, flush=True)
        return 3

    r7j = json.loads(R7A_JSON.read_text()); r7q = np.load(R7A_NPZ)
    r8j = json.loads(R8A2_JSON.read_text()); r8q = np.load(R8A2_NPZ)
    g1 = bool(
        ancestor(PREDATA_LOCK) and ancestor(R7A_POSTDATA_LOCK) and ancestor(R8A2_POSTDATA_LOCK)
        and sha256(R7A_JSON) == R7A_JSON_SHA256
        and sha256(R7A_NPZ) == R7A_NPZ_SHA256
        and sha256(R8A2_JSON) == R8A2_JSON_SHA256
        and sha256(R8A2_NPZ) == R8A2_NPZ_SHA256
        and r7j.get("classification") == R7A_CLASS
        and r7j.get("diagnostic_complete") is True
        and r7j.get("gates") and all(bool(v) for v in r7j["gates"].values())
        and r8j.get("classification") == R8A2_CLASS
        and r8j.get("diagnostic_complete") is True
        and r8j.get("gates") and all(bool(v) for v in r8j["gates"].values())
    )
    g2, source_meta = source_topology()
    print("STABLE_AEST_COSMIC_MEMORY_R8B_SOURCE " + json.dumps(source_meta, sort_keys=True), flush=True)

    work = Path(args.workdir); work.mkdir(parents=True, exist_ok=True)
    py = sys.executable
    mod = "fullj_weyl.stable_aest_cosmic_memory_r8b_two_tau_lookback"
    specs = [("baseline", "full", 0.0)]
    for eps, tag in ((EPS_PRIMARY, "e0p025"), (EPS_CONTROL, "e0p05")):
        specs += [(f"full_p_{tag}", "full", +eps), (f"full_m_{tag}", "full", -eps)]
    for e in EPOCHS:
        specs += [(f"{e}_p", e, +EPS_PRIMARY), (f"{e}_m", e, -EPS_PRIMARY)]

    vals = {}; runs = []; all_runs = True
    for name, mode, eta in specs:
        outp = work / f"{name}.npz"
        env = os.environ.copy(); env["AEST_R7A_EPOCH_MODE"] = mode
        for key in (
            "AEST_TANGENT_FORCE_FILE", "AEST_TANGENT_LAMBDA", "AEST_TANGENT_TRACE_FILE",
            "AEST_R2D_TRACE_FILE", "AEST_R2D_TRACE_KH", "AEST_R2D_TRACE_ALL_K",
            "AEST_TANGENT_ALLOW_K_MISS", "AEST_ERHS_TRACE_FILE", "AEST_ERHS_TRACE_K",
        ):
            env.pop(key, None)
        try:
            subprocess.run(
                [py, "-m", mod, "--worker", "--mode", mode, "--eta", str(eta), "--out", str(outp)],
                cwd=ROOT, env=env, check=True,
            )
            v = r8a2.load_case(outp); vals[name] = v
            ok = bool(v["finite"] and v["domain_positive"]); all_runs &= ok
            runs.append({
                "name": name, "mode": mode, "tau_H0": TAU, "eta": eta,
                "finite": v["finite"], "domain_positive": v["domain_positive"],
                "bits": v["bits"], "target_pos": v["target_pos"],
                "sigma8_z0_property": v["sigma8_z0_property"],
            })
            print(f"STABLE_AEST_COSMIC_MEMORY_R8B_RUN name={name} mode={mode} tau={TAU:g} eta={eta:g} finite={v['finite']} positive={v['domain_positive']}", flush=True)
        except Exception as exc:
            all_runs = False
            runs.append({"name": name, "mode": mode, "tau_H0": TAU, "eta": eta, "finite": False, "domain_positive": False, "error": repr(exc)})
            print(f"STABLE_AEST_COSMIC_MEMORY_R8B_RUN_FAIL name={name} mode={mode} eta={eta:g} error={exc!r}", flush=True)

    arrays = {"z": np.asarray(r7q["z"], float), "ell": np.asarray(r7q["ell"], float)}
    baseline_metrics = {}; central_metrics = {}; bridge_metrics = {}; recon_metrics = {}
    contributions_125 = {}; contributions_10 = {}; comparison = {}; late_z0p2 = {}
    zero_cross = {}

    g3 = bool(all_runs and len(vals) == len(specs))
    if g3:
        b = vals["baseline"]
        base_ok = True
        for obs in OBS:
            parent0 = np.asarray(r8q[f"baseline_tau1p25_{obs}"], float)
            bm = r8a.metric(b[obs], parent0)
            baseline_metrics[obs] = bm
            base_ok &= bool(bm["E"] <= 1e-7 and bm["C"] >= 0.99999999)
            arrays[f"baseline_tau1p25_{obs}"] = b[obs]
            arrays[f"parent_baseline_tau1p25_{obs}"] = parent0
        g3 = bool(g3 and base_ok)

    g4 = g5 = g6 = g7 = False
    if g3:
        b = vals["baseline"]
        c_ok = bridge_ok = recon_ok = component_ok = True
        for obs in OBS:
            tf25 = r8a.central(vals["full_p_e0p025"][obs], vals["full_m_e0p025"][obs], b[obs], EPS_PRIMARY)
            tf50 = r8a.central(vals["full_p_e0p05"][obs], vals["full_m_e0p05"][obs], b[obs], EPS_CONTROL)
            cm = r8a.metric(tf25, tf50)
            central_metrics[obs] = cm
            c_ok &= bool(cm["E"] <= 0.05 and cm["C"] >= 0.995)

            parent125 = np.asarray(r8q[f"T_tau1p25_{obs}_eps025"], float)
            bm = r8a.metric(tf25, parent125)
            bridge_metrics[obs] = bm
            bridge_ok &= bool(bm["E"] <= 0.02 and bm["C"] >= 0.999)

            parts125 = {}
            for e in EPOCHS:
                part = r8a.central(vals[f"{e}_p"][obs], vals[f"{e}_m"][obs], b[obs], EPS_PRIMARY)
                parts125[e] = part
                arrays[f"T_tau1p25_{e}_{obs}"] = part
                component_ok &= bool(np.all(np.isfinite(part)) and np.linalg.norm(part) > 0.0)
            tsum = sum((parts125[e] for e in EPOCHS), np.zeros_like(tf25))
            rm = r8a.metric(tsum, tf25)
            recon_metrics[obs] = rm
            recon_ok &= bool(rm["E"] <= 0.02 and rm["C"] >= 0.999)

            full10 = np.asarray(r7q[f"T_full025_{obs}"], float)
            parts10 = {e: np.asarray(r7q[f"T_{e}_{obs}"], float) for e in EPOCHS}
            m125 = contribution_metrics(parts125, tf25)
            m10 = contribution_metrics(parts10, full10)
            contributions_125[obs] = m125
            contributions_10[obs] = m10

            comp = {}
            for e in EPOCHS:
                n10 = max(float(np.linalg.norm(parts10[e])), 1e-300)
                comp[e] = {
                    "delta_signed_projection_fraction": float(m125[e]["signed_projection_fraction"] - m10[e]["signed_projection_fraction"]),
                    "delta_norm_share": float(m125[e]["norm_share"] - m10[e]["norm_share"]),
                    "cross_tau_epoch_cosine": r8a.cosine(parts125[e], parts10[e]),
                    "epoch_amplitude_ratio_tau1p25_to_tau10": float(np.linalg.norm(parts125[e]) / n10),
                }
            comp["aggregate"] = {
                "delta_early_signed_projection_fraction": float(m125["early_signed_projection_fraction"] - m10["early_signed_projection_fraction"]),
                "delta_late_signed_projection_fraction": float(m125["late_signed_projection_fraction"] - m10["late_signed_projection_fraction"]),
                "delta_early_norm_share": float(m125["early_norm_share"] - m10["early_norm_share"]),
                "delta_late_norm_share": float(m125["late_norm_share"] - m10["late_norm_share"]),
            }
            comparison[obs] = comp

            arrays[f"T_tau1p25_full025_{obs}"] = tf25
            arrays[f"T_tau1p25_full05_{obs}"] = tf50
            arrays[f"T_tau1p25_sum_{obs}"] = tsum
            arrays[f"T_parent_r8a2_tau1p25_{obs}"] = parent125
            arrays[f"T_tau10_full_{obs}"] = full10
            for e in EPOCHS:
                arrays[f"T_tau10_{e}_{obs}"] = parts10[e]

            if obs in ("sigma8", "fsigma8"):
                d125 = float(tf25[0]); d10 = float(full10[0])
                late_z0p2[obs] = {
                    "tau1p25": {e: (float(parts125[e][0] / d125) if d125 != 0.0 else float("nan")) for e in EPOCHS},
                    "tau10": {e: (float(parts10[e][0] / d10) if d10 != 0.0 else float("nan")) for e in EPOCHS},
                }
                for label in ("tau1p25", "tau10"):
                    late_z0p2[obs][label]["sum"] = float(sum(late_z0p2[obs][label][e] for e in EPOCHS))
                late_z0p2[obs]["delta"] = {e: float(late_z0p2[obs]["tau1p25"][e] - late_z0p2[obs]["tau10"][e]) for e in EPOCHS}

            if obs == "ckk":
                ell = np.asarray(r7q["ell"], float)
                zero_cross = {
                    "tau1p25": zero_crossings(ell, tf25),
                    "tau10": zero_crossings(ell, full10),
                }

        g4 = bool(c_ok); g5 = bool(bridge_ok); g6 = bool(recon_ok); g7 = bool(component_ok)

    gates = {
        "R8B_G1_provenance_and_parent_lock": g1,
        "R8B_G2_direct_physical_source_topology": g2,
        "R8B_G3_finite_runs_and_tau1p25_baseline_bridge": g3,
        "R8B_G4_tau1p25_full_central_derivative_consistency": g4,
        "R8B_G5_tau1p25_full_bridge_to_r8a2": g5,
        "R8B_G6_live_epoch_reconstruction_tau1p25": g6,
        "R8B_G7_resolved_epoch_components": g7,
    }
    if not g1: cls = CLS_PARENT
    elif not g2: cls = CLS_SOURCE
    elif not g3: cls = CLS_RUN
    elif not g4: cls = CLS_CENTRAL
    elif not g5: cls = CLS_BRIDGE
    elif not g6: cls = CLS_RECON
    elif not g7: cls = CLS_COMPONENT
    else: cls = CLS_PASS

    reportable = bool(cls == CLS_PASS)
    summary = {
        "classification": cls,
        "baseline_bridge_tau1p25": baseline_metrics,
        "central_derivative_metrics_tau1p25": central_metrics,
        "r8a2_full_bridge_tau1p25": bridge_metrics,
        "epoch_reconstruction_tau1p25": recon_metrics,
        "epoch_contributions_tau1p25": contributions_125,
        "epoch_contributions_tau10_parent": contributions_10,
        "two_tau_epoch_comparison": comparison,
        "late_z0p2_signed_epoch_fractions": late_z0p2,
        "ckk_zero_crossings": zero_cross,
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
            "r8a2_postdata_lock": R8A2_POSTDATA_LOCK,
            "r8a2_classification": r8j.get("classification"),
            "r8a2_json_sha256": sha256(R8A2_JSON),
            "r8a2_npz_sha256": sha256(R8A2_NPZ),
        },
        "settings": {
            "tau_H0_new": TAU,
            "tau_H0_reference": 10.0,
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
            "construction": "live physical epoch mask at tau1.25 compared with frozen R7a tau10 parent",
            "nonlinear_halofit": False,
        },
        "source_topology": source_meta,
        "runs": runs,
        "baseline_bridge_tau1p25": baseline_metrics,
        "central_derivative_metrics_tau1p25": central_metrics,
        "r8a2_full_bridge_tau1p25": bridge_metrics,
        "epoch_reconstruction_tau1p25": recon_metrics,
        "epoch_contributions_tau1p25": contributions_125,
        "epoch_contributions_tau10_parent": contributions_10,
        "two_tau_epoch_comparison": comparison,
        "late_z0p2_signed_epoch_fractions": late_z0p2,
        "ckk_zero_crossings": zero_cross,
        "gates": gates,
        "interpretation": {
            "two_tau_lookback_comparison_reportable": reportable,
            "tau1p25_epoch_fractions_reportable": reportable,
            "continuous_tau_kernel_claim_licensed": False,
            "tau_below_1p25_claim_licensed": False,
            "observational_detection_claim_licensed": False,
            "signed_fractions_are_probabilities": False,
        },
        "summary": summary,
    }
    Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    np.savez_compressed(args.npz_out, **arrays)

    print("STABLE_AEST_COSMIC_MEMORY_R8B_GATES=" + json.dumps(gates, sort_keys=True), flush=True)
    print("STABLE_AEST_COSMIC_MEMORY_R8B_SUMMARY=" + json.dumps(summary, sort_keys=True), flush=True)
    print("STABLE_AEST_COSMIC_MEMORY_R8B_CLASSIFICATION=" + cls, flush=True)
    return 0 if cls == CLS_PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
