#!/usr/bin/env python3
from __future__ import annotations

import argparse
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

from fullj_weyl import aest_ulp_initial_amplitude_localization as amp
from fullj_weyl import aest_stable_chi_precision_convergence as pc

PREDATA_LOCK = "f6886b2b934330036e9239e3fb2d3678dee3c72f"
R5A_POSTDATA_LOCK = "118c680c3c05e7ca95bbc16700bd846e200a7ab6"
R5A_JSON = ROOT / "results/stable_aest_observable_projection_r5a_local_eta.json"
R5A_CLASS = "STABLE_AEST_OBSERVABLE_PROJECTION_R5A_LOCAL_ETA_SCALING_FAIL"

TAU = 10.0
ORDER = 20
ETA_CERT = (0.0, 0.01, 0.025, 0.05)
ETA_BRIDGE = 0.1
TOL_NOMINAL = 3e-8
TOL_TIGHT = 1e-8
Z = np.asarray([0.2, 0.5, 1.0, 1.5, 2.0], float)
LMIN = 40
LMAX = 2000
CANON_KH = 0.165

CLS_INCOMPLETE = "STABLE_AEST_OBSERVABLE_PROJECTION_R5B_INCOMPLETE"
CLS_SOURCE = "STABLE_AEST_OBSERVABLE_PROJECTION_R5B_SOURCE_TOPOLOGY_FAIL"
CLS_RUN = "STABLE_AEST_OBSERVABLE_PROJECTION_R5B_RUN_FAIL"
CLS_PREC = "STABLE_AEST_OBSERVABLE_PROJECTION_R5B_PRECISION_UNRESOLVED"
CLS_ETA = "STABLE_AEST_OBSERVABLE_PROJECTION_R5B_DERIVATIVE_SCALING_FAIL"
CLS_RESP = "STABLE_AEST_OBSERVABLE_PROJECTION_R5B_RESPONSE_UNRESOLVED"
CLS_PASS = "STABLE_AEST_OBSERVABLE_PROJECTION_R5B_DERIVATIVE_ZERO_CERTIFIED"


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


def tangent(x_eta, x0, eta: float):
    return (np.asarray(x_eta, float)-np.asarray(x0, float))/(float(eta)*np.asarray(x0, float))


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
    root = os.environ.get("AEST_STABLE_CLASS_ROOT", "")
    if not root:
        return False, {"reason": "AEST_STABLE_CLASS_ROOT missing"}
    p = Path(root)/"source"/"perturbations.c"
    if not p.is_file():
        return False, {"reason": "perturbations.c missing"}
    text = p.read_text(); body = derivs_block(text)
    eta_mul = body.count("Bchi_aest *= pba->aest_eta;")
    closure = body.count("E_rhs_aest -= 0.5*Q_aest*Bchi_aest;")
    eta_refs = body.count("pba->aest_eta")
    external = body.count("aest_tangent_external_force")
    checks = {
        "stable_marker": "FULLJ_AEST_STABLE_CHI_RESIDUAL_V1" in text,
        "stable_chi_rhs": "double chi_aest = Q_aest*s_aest;" in body,
        "alpha_rhs": "dy[pv->index_pt_alpha_aest] = a*(E_aest-psi_aest);" in body,
        "stable_s_rhs": "3.*cad2_aest*a_prime_over_a*(s_aest-alpha_aest)" in body,
        "physical_eta_multiply_once": eta_mul == 1,
        "physical_memory_closure_once": closure == 1,
        "physical_eta_rhs_reference_once": eta_refs == 1,
        "diagnostic_external_force_absent": external == 0,
    }
    meta = {"checks": checks, "eta_multiply_count": eta_mul, "closure_count": closure,
            "eta_reference_count_in_derivs": eta_refs, "external_force_count_in_derivs": external}
    return bool(all(checks.values())), meta


def build_params(eta: float, tol: float):
    bits = pc.bits_for_anchor(float(CANON_KH))
    params, pos = amp.make_params(float(CANON_KH), int(bits))
    params["tol_perturbations_integration"] = float(tol)
    params["aest_memory_enabled"] = "yes"
    params["aest_memory_order"] = int(ORDER)
    params["aest_eta"] = float(eta)
    params["aest_tau_H0"] = float(TAU)
    params["output"] = "mPk,lCl"
    params["z_max_pk"] = 2.2
    params["P_k_max_h/Mpc"] = 5.0
    params["l_max_scalars"] = int(LMAX)
    params.pop("non_linear", None)
    params.pop("lensing", None)
    return params, int(bits), int(pos)


def run_case(eta: float, tol: float):
    from classy import Class
    params, bits, pos = build_params(eta, tol)
    c = Class(); c.set(params); c.compute()
    try:
        sigma8 = np.asarray([float(c.sigma(8.0, float(z), h_units=True)) for z in Z], float)
        fsigma8 = np.asarray([float(c.effective_f_sigma8(float(z), z_step=0.1)) for z in Z], float)
        raw = c.raw_cl(lmax=int(LMAX))
        if "pp" not in raw:
            raise RuntimeError("CLASS raw_cl has no pp lensing-potential spectrum")
        pp = np.asarray(raw["pp"], float)
        ell = np.arange(pp.size, dtype=float)
        if pp.size <= LMAX:
            raise RuntimeError(f"pp length {pp.size} <= requested LMAX {LMAX}")
        sel = (ell >= LMIN) & (ell <= LMAX)
        le = ell[sel]
        ckk = ((le*(le+1.0)/2.0)**2) * pp[sel]
        finite = bool(np.all(np.isfinite(sigma8)) and np.all(np.isfinite(fsigma8)) and np.all(np.isfinite(ckk)))
        positive = bool(np.all(sigma8 > 0.0) and np.all(ckk > 0.0))
        return {"sigma8": sigma8, "fsigma8": fsigma8, "ckk": ckk, "ell": le,
                "finite": finite, "domain_positive": positive, "bits": bits,
                "target_pos": pos, "sigma8_z0_property": float(c.sigma8())}
    finally:
        c.struct_cleanup(); c.empty()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json-out", default="results/stable_aest_observable_projection_r5b_derivative_zero.json")
    ap.add_argument("--npz-out", default="results/stable_aest_observable_projection_r5b_derivative_zero.npz")
    args = ap.parse_args()
    print("STABLE_AEST_OBSERVABLE_PROJECTION_R5B_START", flush=True)

    if not R5A_JSON.exists():
        out = {"classification": CLS_INCOMPLETE, "diagnostic_complete": False, "reason": "missing R5a JSON"}
        Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True)+"\n")
        print("STABLE_AEST_OBSERVABLE_PROJECTION_R5B_CLASSIFICATION="+CLS_INCOMPLETE, flush=True)
        return 3

    parent = json.loads(R5A_JSON.read_text())
    g1 = bool(ancestor(PREDATA_LOCK) and ancestor(R5A_POSTDATA_LOCK)
              and parent.get("classification") == R5A_CLASS
              and parent.get("diagnostic_complete") is True)
    g2, source_meta = source_topology()
    print("STABLE_AEST_OBSERVABLE_PROJECTION_R5B_SOURCE "+json.dumps(source_meta, sort_keys=True), flush=True)

    specs = [
        ("nominal_e0", 0.0, TOL_NOMINAL),
        ("nominal_e0p01", 0.01, TOL_NOMINAL),
        ("nominal_e0p025", 0.025, TOL_NOMINAL),
        ("nominal_e0p05", 0.05, TOL_NOMINAL),
        ("bridge_e0p1", 0.1, TOL_NOMINAL),
        ("tight_e0", 0.0, TOL_TIGHT),
        ("tight_e0p01", 0.01, TOL_TIGHT),
    ]
    vals = {}; runs = []; arrays = {"z": Z}; all_runs = True
    for name, eta, tol in specs:
        try:
            v = run_case(eta, tol); vals[name] = v
            ok = bool(v["finite"] and v["domain_positive"]); all_runs &= ok
            runs.append({"name": name, "eta": eta, "tol": tol, "finite": v["finite"],
                         "domain_positive": v["domain_positive"], "bits": v["bits"],
                         "target_pos": v["target_pos"], "sigma8_z0_property": v["sigma8_z0_property"]})
            for key in ("sigma8", "fsigma8", "ckk"):
                arrays[f"{key}_{name}"] = v[key]
            arrays["ell"] = v["ell"]
            print(f"STABLE_AEST_OBSERVABLE_PROJECTION_R5B_RUN name={name} eta={eta:g} tol={tol:.1e} finite={v['finite']} domain_positive={v['domain_positive']}", flush=True)
        except Exception as exc:
            all_runs = False
            runs.append({"name": name, "eta": eta, "tol": tol, "finite": False, "domain_positive": False, "error": repr(exc)})
            print(f"STABLE_AEST_OBSERVABLE_PROJECTION_R5B_RUN_FAIL name={name} eta={eta:g} tol={tol:.1e} error={exc!r}", flush=True)

    g3 = bool(all_runs and len(vals) == len(specs))
    precision_metrics = {}; derivative_metrics = {}; bridge_metrics = {}; response = {}
    g4 = g5 = g6 = False

    if g3:
        n0 = vals["nominal_e0"]; n01 = vals["nominal_e0p01"]
        n025 = vals["nominal_e0p025"]; n05 = vals["nominal_e0p05"]
        nb = vals["bridge_e0p1"]; t0 = vals["tight_e0"]; t01 = vals["tight_e0p01"]
        precision_all = True; derivative_all = True; resolved_all = True
        for key in ("sigma8", "fsigma8", "ckk"):
            T01 = tangent(n01[key], n0[key], 0.01)
            T025 = tangent(n025[key], n0[key], 0.025)
            T05 = tangent(n05[key], n0[key], 0.05)
            T10 = tangent(nb[key], n0[key], 0.1)
            TT01 = tangent(t01[key], t0[key], 0.01)
            arrays[f"T_{key}_eta0p01"] = T01
            arrays[f"T_{key}_eta0p025"] = T025
            arrays[f"T_{key}_eta0p05"] = T05
            arrays[f"T_{key}_eta0p1_bridge"] = T10
            arrays[f"T_{key}_eta0p01_tight"] = TT01

            pm = metric(T01, TT01)
            m01_025 = metric(T01, T025)
            m025_05 = metric(T025, T05)
            bm = metric(T05, T10)
            precision_metrics[key] = pm
            derivative_metrics[key] = {"eta0p01_vs_eta0p025": m01_025,
                                       "eta0p025_vs_eta0p05": m025_05}
            bridge_metrics[key] = {"eta0p05_vs_eta0p1": bm}
            precision_pass = bool(pm["E"] <= 0.10 and pm["C"] >= 0.995)
            derivative_pass = bool(m01_025["E"] <= 0.10 and m01_025["C"] >= 0.995
                                   and m025_05["E"] <= 0.10 and m025_05["C"] >= 0.995)
            precision_all &= precision_pass; derivative_all &= derivative_pass
            nrm = float(np.linalg.norm(T01)); resolved = bool(np.isfinite(nrm) and nrm > 0.0)
            resolved_all &= resolved
            response[key] = {"norm_eta0p01": nrm, "min_eta0p01": float(np.min(T01)),
                             "max_eta0p01": float(np.max(T01)), "precision_pass": precision_pass,
                             "derivative_pass": derivative_pass, "resolved": resolved}
            print("STABLE_AEST_OBSERVABLE_PROJECTION_R5B_OBS "+json.dumps(
                {"observable": key, "precision": pm, "derivative": derivative_metrics[key],
                 "bridge": bridge_metrics[key], "response": response[key]}, sort_keys=True), flush=True)
        g4 = bool(precision_all)
        g5 = bool(derivative_all)
        g6 = bool(g4 and g5 and resolved_all)

    gates = {
        "R5B_G1_provenance_and_parent_lock": g1,
        "R5B_G2_single_channel_source_topology": g2,
        "R5B_G3_finite_observable_runs": g3,
        "R5B_G4_smallest_eta_precision_stability": g4,
        "R5B_G5_derivative_zero_eta_consistency": g5,
        "R5B_G6_resolved_derivative_zero_response": g6,
    }
    if not g1: cls = CLS_INCOMPLETE
    elif not g2: cls = CLS_SOURCE
    elif not g3: cls = CLS_RUN
    elif not g4: cls = CLS_PREC
    elif not g5: cls = CLS_ETA
    elif not g6: cls = CLS_RESP
    else: cls = CLS_PASS

    summary = {"classification": cls, "run_count": len(runs), "precision_metrics": precision_metrics,
               "derivative_metrics": derivative_metrics, "bridge_metrics": bridge_metrics,
               "response": response}
    out = {
        "classification": cls, "diagnostic_complete": True, "predata_lock": PREDATA_LOCK,
        "r5a_parent_classification": parent.get("classification"),
        "r5a_postdata_lock": R5A_POSTDATA_LOCK,
        "source_topology": source_meta,
        "settings": {"tau_H0": TAU, "memory_order": ORDER,
                     "eta_certification": list(ETA_CERT), "eta_bridge": ETA_BRIDGE,
                     "eta_tight": [0.0, 0.01], "tol_nominal": TOL_NOMINAL,
                     "tol_tight": TOL_TIGHT, "redshifts": Z.tolist(), "L_min": LMIN,
                     "L_max": LMAX, "canonical_k_output_seed": CANON_KH,
                     "P_k_max_h/Mpc": 5.0, "non_linear": False,
                     "science_method": "direct physical derivative-at-zero eta; eta=0.1 bridge is non-gating"},
        "runs": runs, "gates": gates, "summary": summary,
        "interpretation": {"derivative_zero_observable_tangent_licensed": cls == CLS_PASS,
                           "eta0p1_bridge_is_gating": False,
                           "observational_claim_licensed": False,
                           "likelihood_claim_licensed": False,
                           "positive_growth_weyl_separation_licensed": False,
                           "r5a_reclassified": False},
    }
    Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True)+"\n")
    np.savez_compressed(args.npz_out, **arrays)
    print("STABLE_AEST_OBSERVABLE_PROJECTION_R5B_GATES="+json.dumps(gates, sort_keys=True), flush=True)
    print("STABLE_AEST_OBSERVABLE_PROJECTION_R5B_SUMMARY="+json.dumps(summary, sort_keys=True), flush=True)
    print("STABLE_AEST_OBSERVABLE_PROJECTION_R5B_CLASSIFICATION="+cls, flush=True)
    return 0 if cls == CLS_PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
