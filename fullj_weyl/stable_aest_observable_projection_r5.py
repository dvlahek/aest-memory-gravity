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

from fullj_weyl import aest_ulp_initial_amplitude_localization as amp
from fullj_weyl import aest_stable_chi_precision_convergence as pc
from fullj_weyl import stable_aest_growth_weyl_memory_r4_common_mode_mechanism as r4

PREDATA_LOCK = "773ee8b0ab1d41dc1737eaf53f1961ea2f644bde"
R4_POSTDATA_LOCK = "c7c317be346371d0943e29b1b16016f9c36ef704"
R4_JSON = ROOT / "results/stable_aest_growth_weyl_memory_r4_common_mode_mechanism.json"
R4_CLASS = "STABLE_AEST_GROWTH_WEYL_MEMORY_R4_SINGLE_AMPLITUDE_MODE_CERTIFIED"

TAU = 10.0
ORDER = 20
ETA_NOMINAL = (0.0, 1.0, 10.0)
TOL_NOMINAL = 3e-8
TOL_TIGHT = 1e-8
Z = np.asarray([0.2, 0.5, 1.0, 1.5, 2.0], float)
LMIN = 40
LMAX = 2000
CANON_KH = 0.165

CLS_INCOMPLETE = "STABLE_AEST_OBSERVABLE_PROJECTION_R5_INCOMPLETE"
CLS_SOURCE = "STABLE_AEST_OBSERVABLE_PROJECTION_R5_SOURCE_TOPOLOGY_FAIL"
CLS_RUN = "STABLE_AEST_OBSERVABLE_PROJECTION_R5_RUN_FAIL"
CLS_ETA = "STABLE_AEST_OBSERVABLE_PROJECTION_R5_ETA_SCALING_FAIL"
CLS_PREC = "STABLE_AEST_OBSERVABLE_PROJECTION_R5_PRECISION_UNRESOLVED"
CLS_RESP = "STABLE_AEST_OBSERVABLE_PROJECTION_R5_RESPONSE_UNRESOLVED"
CLS_PASS = "STABLE_AEST_OBSERVABLE_PROJECTION_R5_CERTIFIED"


def ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"], cwd=ROOT,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    ).returncode == 0


def rel(a, b) -> float:
    a = np.asarray(a, float); b = np.asarray(b, float)
    return float(np.linalg.norm(a-b) / max(float(np.linalg.norm(a)), float(np.linalg.norm(b)), 1e-300))


def cosine(a, b) -> float:
    a = np.asarray(a, float); b = np.asarray(b, float)
    na = float(np.linalg.norm(a)); nb = float(np.linalg.norm(b))
    if na <= 0.0 or nb <= 0.0:
        return float("nan")
    return float(np.dot(a,b)/(na*nb))


def tangent(xe, x0, eta: float):
    return (np.asarray(xe,float)-np.asarray(x0,float))/(float(eta)*np.asarray(x0,float))


def build_params(eta: float, tol: float):
    bits = pc.bits_for_anchor(float(CANON_KH))
    p, pos = amp.make_params(float(CANON_KH), int(bits))
    p["tol_perturbations_integration"] = float(tol)
    p["aest_memory_enabled"] = "yes"
    p["aest_memory_order"] = int(ORDER)
    p["aest_eta"] = float(eta)
    p["aest_tau_H0"] = float(TAU)
    p["output"] = "mPk,lCl"
    p["z_max_pk"] = 2.2
    p["P_k_max_h/Mpc"] = 5.0
    p["l_max_scalars"] = int(LMAX)
    # R5 is explicitly linear. Remove any inherited nonlinear request.
    p.pop("non_linear", None)
    p.pop("lensing", None)
    return p, int(bits), int(pos)


def run_case(eta: float, tol: float):
    from classy import Class

    p, bits, pos = build_params(eta, tol)
    c = Class(); c.set(p); c.compute()
    try:
        sigma8 = np.asarray([float(c.sigma(8.0, float(z), h_units=True)) for z in Z], float)
        fs8 = np.asarray([float(c.effective_f_sigma8(float(z), z_step=0.1)) for z in Z], float)
        cl = c.raw_cl(lmax=int(LMAX))
        if "pp" not in cl:
            raise RuntimeError("CLASS raw_cl has no pp lensing-potential spectrum")
        pp = np.asarray(cl["pp"], float)
        ell = np.arange(pp.size, dtype=float)
        if pp.size <= LMAX:
            raise RuntimeError(f"pp length {pp.size} <= requested LMAX {LMAX}")
        sel = (ell >= LMIN) & (ell <= LMAX)
        lsel = ell[sel]
        ckk = ((lsel*(lsel+1.0)/2.0)**2) * pp[sel]
        finite = bool(np.all(np.isfinite(sigma8)) and np.all(np.isfinite(fs8)) and np.all(np.isfinite(ckk)))
        positive = bool(np.all(sigma8 > 0.0) and np.all(ckk > 0.0))
        return {
            "sigma8": sigma8,
            "fsigma8": fs8,
            "ckk": ckk,
            "ell": lsel,
            "finite": finite,
            "positive": positive,
            "bits": bits,
            "target_pos": pos,
            "sigma8_z0_property": float(c.sigma8()),
        }
    finally:
        c.struct_cleanup(); c.empty()


def metric(a, b):
    return {"E": rel(a,b), "C": cosine(a,b)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json-out", default="results/stable_aest_observable_projection_r5.json")
    ap.add_argument("--npz-out", default="results/stable_aest_observable_projection_r5.npz")
    args = ap.parse_args()

    print("STABLE_AEST_OBSERVABLE_PROJECTION_R5_START", flush=True)

    if not R4_JSON.exists():
        out={"classification":CLS_INCOMPLETE,"diagnostic_complete":False,"reason":"missing R4 JSON"}
        Path(args.json_out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
        print("STABLE_AEST_OBSERVABLE_PROJECTION_R5_CLASSIFICATION="+CLS_INCOMPLETE,flush=True)
        return 3

    r4j=json.loads(R4_JSON.read_text())
    g1=bool(ancestor(PREDATA_LOCK) and ancestor(R4_POSTDATA_LOCK)
            and r4j.get("classification")==R4_CLASS)
    g2, source_meta = r4.source_topology()
    print("STABLE_AEST_OBSERVABLE_PROJECTION_R5_SOURCE "+json.dumps(source_meta,sort_keys=True),flush=True)

    specs=[("nominal_e0",0.0,TOL_NOMINAL),("nominal_e1",1.0,TOL_NOMINAL),
           ("nominal_e10",10.0,TOL_NOMINAL),("tight_e0",0.0,TOL_TIGHT),
           ("tight_e10",10.0,TOL_TIGHT)]
    vals={}; runs=[]; arrays={"z":Z}
    all_runs=True
    for name,eta,tol in specs:
        try:
            v=run_case(eta,tol); vals[name]=v
            ok=bool(v["finite"] and v["positive"])
            all_runs &= ok
            runs.append({"name":name,"eta":eta,"tol":tol,"finite":v["finite"],"positive":v["positive"],
                         "bits":v["bits"],"target_pos":v["target_pos"],
                         "sigma8_z0_property":v["sigma8_z0_property"]})
            arrays[f"sigma8_{name}"]=v["sigma8"]
            arrays[f"fsigma8_{name}"]=v["fsigma8"]
            arrays[f"ckk_{name}"]=v["ckk"]
            arrays["ell"]=v["ell"]
            print(f"STABLE_AEST_OBSERVABLE_PROJECTION_R5_RUN name={name} eta={eta:g} tol={tol:.1e} finite={v['finite']} positive={v['positive']}",flush=True)
        except Exception as e:
            all_runs=False
            runs.append({"name":name,"eta":eta,"tol":tol,"finite":False,"positive":False,"error":repr(e)})
            print(f"STABLE_AEST_OBSERVABLE_PROJECTION_R5_RUN_FAIL name={name} eta={eta:g} tol={tol:.1e} error={e!r}",flush=True)

    g3=bool(all_runs and len(vals)==len(specs))
    eta_metrics={}; prec_metrics={}; response={}
    g4=g5=g6=False

    if g3:
        n0=vals["nominal_e0"]; n1=vals["nominal_e1"]; n10=vals["nominal_e10"]
        t0=vals["tight_e0"]; t10=vals["tight_e10"]
        strict_eta=True; strict_prec=True; resolved=True
        for key in ("sigma8","fsigma8","ckk"):
            T1=tangent(n1[key],n0[key],1.0)
            T10=tangent(n10[key],n0[key],10.0)
            TT10=tangent(t10[key],t0[key],10.0)
            arrays[f"T_{key}_eta1"]=T1
            arrays[f"T_{key}_eta10"]=T10
            arrays[f"T_{key}_eta10_tight"]=TT10
            em=metric(T1,T10); pm=metric(T10,TT10)
            eta_metrics[key]=em; prec_metrics[key]=pm
            nrm=float(np.linalg.norm(T10))
            response[key]={"norm_eta10":nrm,"min":float(np.min(T10)),"max":float(np.max(T10))}
            strict_eta &= bool(em["E"]<=0.05 and em["C"]>=0.999)
            strict_prec &= bool(pm["E"]<=0.10 and pm["C"]>=0.995)
            resolved &= bool(np.isfinite(nrm) and nrm>0.0)
            print("STABLE_AEST_OBSERVABLE_PROJECTION_R5_OBS "+json.dumps({"observable":key,"eta":em,"precision":pm,"response":response[key]},sort_keys=True),flush=True)
        g4=bool(strict_eta)
        g5=bool(g4 and strict_prec)
        g6=bool(g5 and resolved)

    gates={
        "R5_G1_provenance_and_parent_lock":g1,
        "R5_G2_single_channel_source_topology":g2,
        "R5_G3_finite_observable_runs":g3,
        "R5_G4_physical_eta_tangent_consistency":g4,
        "R5_G5_precision_stability":g5,
        "R5_G6_resolved_observable_response":g6,
    }
    if not g1: cls=CLS_INCOMPLETE
    elif not g2: cls=CLS_SOURCE
    elif not g3: cls=CLS_RUN
    elif not g4: cls=CLS_ETA
    elif not g5: cls=CLS_PREC
    elif not g6: cls=CLS_RESP
    else: cls=CLS_PASS

    summary={"classification":cls,"run_count":len(runs),"eta_metrics":eta_metrics,
             "precision_metrics":prec_metrics,"response":response}
    out={
        "classification":cls,"diagnostic_complete":True,"predata_lock":PREDATA_LOCK,
        "r4_parent_classification":r4j.get("classification"),"source_topology":source_meta,
        "settings":{"tau_H0":TAU,"memory_order":ORDER,"eta_nominal":ETA_NOMINAL,
                    "tol_nominal":TOL_NOMINAL,"tol_tight":TOL_TIGHT,"redshifts":Z.tolist(),
                    "L_min":LMIN,"L_max":LMAX,"canonical_k_output_seed":CANON_KH,
                    "P_k_max_h/Mpc":5.0,"non_linear":False,
                    "science_method":"direct physical eta; CLASS sigma/effective_f_sigma8/raw C_L^phiphi"},
        "runs":runs,"gates":gates,"summary":summary,
        "interpretation":{"observable_projection_licensed":cls==CLS_PASS,
                          "observational_claim_licensed":False,
                          "likelihood_claim_licensed":False,
                          "positive_growth_weyl_separation_licensed":False},
    }
    Path(args.json_out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    np.savez_compressed(args.npz_out,**arrays)
    print("STABLE_AEST_OBSERVABLE_PROJECTION_R5_GATES="+json.dumps(gates,sort_keys=True),flush=True)
    print("STABLE_AEST_OBSERVABLE_PROJECTION_R5_SUMMARY="+json.dumps(summary,sort_keys=True),flush=True)
    print("STABLE_AEST_OBSERVABLE_PROJECTION_R5_CLASSIFICATION="+cls,flush=True)
    return 0 if cls==CLS_PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
