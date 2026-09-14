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

PREDATA_LOCK = "d728b9629866da83182f5324988dea659eb61f0d"
R5_POSTDATA_LOCK = "7e02d7789c7478f56c1c63b7fa94ca59192d4ac4"
R5_JSON = ROOT / "results/stable_aest_observable_projection_r5.json"
R5_CLASS = "STABLE_AEST_OBSERVABLE_PROJECTION_R5_ETA_SCALING_FAIL"

TAU = 10.0
ORDER = 20
ETA_SCAN = (0.0, 0.1, 0.25, 0.5)
TOL_NOMINAL = 3e-8
TOL_TIGHT = 1e-8
Z = np.asarray([0.2, 0.5, 1.0, 1.5, 2.0], float)
LMIN = 40
LMAX = 2000
CANON_KH = 0.165

CLS_INCOMPLETE = "STABLE_AEST_OBSERVABLE_PROJECTION_R5A_INCOMPLETE"
CLS_SOURCE = "STABLE_AEST_OBSERVABLE_PROJECTION_R5A_SOURCE_TOPOLOGY_FAIL"
CLS_RUN = "STABLE_AEST_OBSERVABLE_PROJECTION_R5A_RUN_FAIL"
CLS_PREC = "STABLE_AEST_OBSERVABLE_PROJECTION_R5A_PRECISION_UNRESOLVED"
CLS_ETA = "STABLE_AEST_OBSERVABLE_PROJECTION_R5A_LOCAL_ETA_SCALING_FAIL"
CLS_RESP = "STABLE_AEST_OBSERVABLE_PROJECTION_R5A_RESPONSE_UNRESOLVED"
CLS_PASS = "STABLE_AEST_OBSERVABLE_PROJECTION_R5A_LOCAL_TANGENT_CERTIFIED"


def ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0


def rel(a, b) -> float:
    aa = np.asarray(a, float)
    bb = np.asarray(b, float)
    return float(
        np.linalg.norm(aa - bb)
        / max(float(np.linalg.norm(aa)), float(np.linalg.norm(bb)), 1e-300)
    )


def cosine(a, b) -> float:
    aa = np.asarray(a, float)
    bb = np.asarray(b, float)
    na = float(np.linalg.norm(aa))
    nb = float(np.linalg.norm(bb))
    if na <= 0.0 or nb <= 0.0:
        return float("nan")
    return float(np.dot(aa, bb) / (na * nb))


def metric(a, b):
    return {"E": rel(a, b), "C": cosine(a, b)}


def tangent(x_eta, x0, eta: float):
    return (
        np.asarray(x_eta, float) - np.asarray(x0, float)
    ) / (float(eta) * np.asarray(x0, float))


def derivs_block(text: str) -> str:
    start = text.find("int perturbations_derivs(")
    if start < 0:
        return ""
    rest = text[start + 1 :]
    match = re.search(r"\nint\s+perturbations_[A-Za-z0-9_]+\s*\(", rest)
    if match is None:
        return text[start:]
    return text[start : start + 1 + match.start()]


def source_topology():
    root = os.environ.get("AEST_STABLE_CLASS_ROOT", "")
    if not root:
        return False, {"reason": "AEST_STABLE_CLASS_ROOT missing"}
    path = Path(root) / "source" / "perturbations.c"
    if not path.is_file():
        return False, {"reason": "perturbations.c missing"}

    text = path.read_text()
    body = derivs_block(text)
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
    meta = {
        "checks": checks,
        "eta_multiply_count": eta_mul,
        "closure_count": closure,
        "eta_reference_count_in_derivs": eta_refs,
        "external_force_count_in_derivs": external,
    }
    return bool(all(checks.values())), meta


def build_params(eta: float, tol: float):
    bits = pc.bits_for_anchor(float(CANON_KH))
    params, target_pos = amp.make_params(float(CANON_KH), int(bits))
    params["tol_perturbations_integration"] = float(tol)
    params["aest_memory_enabled"] = "yes"
    params["aest_memory_order"] = int(ORDER)
    params["aest_eta"] = float(eta)
    params["aest_tau_H0"] = float(TAU)
    params["output"] = "mPk,lCl"
    params["z_max_pk"] = 2.2
    params["P_k_max_h/Mpc"] = 5.0
    params["l_max_scalars"] = int(LMAX)
    # R5a is explicitly linear and must not inherit a nonlinear request.
    params.pop("non_linear", None)
    params.pop("lensing", None)
    return params, int(bits), int(target_pos)


def run_case(eta: float, tol: float):
    from classy import Class

    params, bits, target_pos = build_params(eta, tol)
    cosmo = Class()
    cosmo.set(params)
    cosmo.compute()
    try:
        sigma8 = np.asarray(
            [float(cosmo.sigma(8.0, float(z), h_units=True)) for z in Z], float
        )
        fsigma8 = np.asarray(
            [float(cosmo.effective_f_sigma8(float(z), z_step=0.1)) for z in Z],
            float,
        )
        raw = cosmo.raw_cl(lmax=int(LMAX))
        if "pp" not in raw:
            raise RuntimeError("CLASS raw_cl has no pp lensing-potential spectrum")
        pp = np.asarray(raw["pp"], float)
        ell = np.arange(pp.size, dtype=float)
        if pp.size <= LMAX:
            raise RuntimeError(f"pp length {pp.size} <= requested LMAX {LMAX}")
        select = (ell >= LMIN) & (ell <= LMAX)
        ell_science = ell[select]
        ckk = ((ell_science * (ell_science + 1.0) / 2.0) ** 2) * pp[select]

        finite = bool(
            np.all(np.isfinite(sigma8))
            and np.all(np.isfinite(fsigma8))
            and np.all(np.isfinite(ckk))
        )
        domain_positive = bool(np.all(sigma8 > 0.0) and np.all(ckk > 0.0))
        return {
            "sigma8": sigma8,
            "fsigma8": fsigma8,
            "ckk": ckk,
            "ell": ell_science,
            "finite": finite,
            "domain_positive": domain_positive,
            "bits": bits,
            "target_pos": target_pos,
            "sigma8_z0_property": float(cosmo.sigma8()),
        }
    finally:
        cosmo.struct_cleanup()
        cosmo.empty()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--json-out",
        default="results/stable_aest_observable_projection_r5a_local_eta.json",
    )
    parser.add_argument(
        "--npz-out",
        default="results/stable_aest_observable_projection_r5a_local_eta.npz",
    )
    args = parser.parse_args()

    print("STABLE_AEST_OBSERVABLE_PROJECTION_R5A_START", flush=True)

    if not R5_JSON.exists():
        out = {
            "classification": CLS_INCOMPLETE,
            "diagnostic_complete": False,
            "reason": "missing R5 JSON",
        }
        Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
        print(
            "STABLE_AEST_OBSERVABLE_PROJECTION_R5A_CLASSIFICATION=" + CLS_INCOMPLETE,
            flush=True,
        )
        return 3

    r5 = json.loads(R5_JSON.read_text())
    g1 = bool(
        ancestor(PREDATA_LOCK)
        and ancestor(R5_POSTDATA_LOCK)
        and r5.get("classification") == R5_CLASS
        and r5.get("diagnostic_complete") is True
    )
    g2, source_meta = source_topology()
    print(
        "STABLE_AEST_OBSERVABLE_PROJECTION_R5A_SOURCE "
        + json.dumps(source_meta, sort_keys=True),
        flush=True,
    )

    specs = [
        ("nominal_e0", 0.0, TOL_NOMINAL),
        ("nominal_e0p1", 0.1, TOL_NOMINAL),
        ("nominal_e0p25", 0.25, TOL_NOMINAL),
        ("nominal_e0p5", 0.5, TOL_NOMINAL),
        ("tight_e0", 0.0, TOL_TIGHT),
        ("tight_e0p1", 0.1, TOL_TIGHT),
    ]

    vals = {}
    runs = []
    arrays = {"z": Z}
    all_runs = True
    for name, eta, tol in specs:
        try:
            value = run_case(eta, tol)
            vals[name] = value
            ok = bool(value["finite"] and value["domain_positive"])
            all_runs &= ok
            runs.append(
                {
                    "name": name,
                    "eta": eta,
                    "tol": tol,
                    "finite": value["finite"],
                    "domain_positive": value["domain_positive"],
                    "bits": value["bits"],
                    "target_pos": value["target_pos"],
                    "sigma8_z0_property": value["sigma8_z0_property"],
                }
            )
            for key in ("sigma8", "fsigma8", "ckk"):
                arrays[f"{key}_{name}"] = value[key]
            arrays["ell"] = value["ell"]
            print(
                f"STABLE_AEST_OBSERVABLE_PROJECTION_R5A_RUN name={name} "
                f"eta={eta:g} tol={tol:.1e} finite={value['finite']} "
                f"domain_positive={value['domain_positive']}",
                flush=True,
            )
        except Exception as exc:
            all_runs = False
            runs.append(
                {
                    "name": name,
                    "eta": eta,
                    "tol": tol,
                    "finite": False,
                    "domain_positive": False,
                    "error": repr(exc),
                }
            )
            print(
                f"STABLE_AEST_OBSERVABLE_PROJECTION_R5A_RUN_FAIL name={name} "
                f"eta={eta:g} tol={tol:.1e} error={exc!r}",
                flush=True,
            )

    g3 = bool(all_runs and len(vals) == len(specs))
    precision_metrics = {}
    local_metrics = {}
    response = {}
    g4 = g5 = g6 = False

    if g3:
        n0 = vals["nominal_e0"]
        n01 = vals["nominal_e0p1"]
        n025 = vals["nominal_e0p25"]
        n05 = vals["nominal_e0p5"]
        t0 = vals["tight_e0"]
        t01 = vals["tight_e0p1"]

        precision_all = True
        local_all = True
        resolved_all = True
        for key in ("sigma8", "fsigma8", "ckk"):
            T01 = tangent(n01[key], n0[key], 0.1)
            T025 = tangent(n025[key], n0[key], 0.25)
            T05 = tangent(n05[key], n0[key], 0.5)
            TT01 = tangent(t01[key], t0[key], 0.1)

            arrays[f"T_{key}_eta0p1"] = T01
            arrays[f"T_{key}_eta0p25"] = T025
            arrays[f"T_{key}_eta0p5"] = T05
            arrays[f"T_{key}_eta0p1_tight"] = TT01

            pm = metric(T01, TT01)
            m01_025 = metric(T01, T025)
            m025_05 = metric(T025, T05)
            precision_metrics[key] = pm
            local_metrics[key] = {
                "eta0p1_vs_eta0p25": m01_025,
                "eta0p25_vs_eta0p5": m025_05,
            }

            precision_pass = bool(pm["E"] <= 0.10 and pm["C"] >= 0.995)
            local_pass = bool(
                m01_025["E"] <= 0.10
                and m01_025["C"] >= 0.995
                and m025_05["E"] <= 0.10
                and m025_05["C"] >= 0.995
            )
            precision_all &= precision_pass
            local_all &= local_pass

            norm01 = float(np.linalg.norm(T01))
            resolved = bool(np.isfinite(norm01) and norm01 > 0.0)
            resolved_all &= resolved
            response[key] = {
                "norm_eta0p1": norm01,
                "min_eta0p1": float(np.min(T01)),
                "max_eta0p1": float(np.max(T01)),
                "precision_pass": precision_pass,
                "local_eta_pass": local_pass,
                "resolved": resolved,
            }
            print(
                "STABLE_AEST_OBSERVABLE_PROJECTION_R5A_OBS "
                + json.dumps(
                    {
                        "observable": key,
                        "precision": pm,
                        "local": local_metrics[key],
                        "response": response[key],
                    },
                    sort_keys=True,
                ),
                flush=True,
            )

        g4 = bool(precision_all)
        g5 = bool(local_all)
        g6 = bool(g4 and g5 and resolved_all)

    gates = {
        "R5A_G1_provenance_and_parent_lock": g1,
        "R5A_G2_single_channel_source_topology": g2,
        "R5A_G3_finite_observable_runs": g3,
        "R5A_G4_smallest_eta_precision_stability": g4,
        "R5A_G5_local_eta_tangent_consistency": g5,
        "R5A_G6_resolved_local_response": g6,
    }

    if not g1:
        classification = CLS_INCOMPLETE
    elif not g2:
        classification = CLS_SOURCE
    elif not g3:
        classification = CLS_RUN
    elif not g4:
        classification = CLS_PREC
    elif not g5:
        classification = CLS_ETA
    elif not g6:
        classification = CLS_RESP
    else:
        classification = CLS_PASS

    summary = {
        "classification": classification,
        "run_count": len(runs),
        "precision_metrics": precision_metrics,
        "local_eta_metrics": local_metrics,
        "response": response,
    }
    out = {
        "classification": classification,
        "diagnostic_complete": True,
        "predata_lock": PREDATA_LOCK,
        "r5_postdata_lock": R5_POSTDATA_LOCK,
        "r5_parent_classification": r5.get("classification"),
        "source_topology": source_meta,
        "settings": {
            "tau_H0": TAU,
            "memory_order": ORDER,
            "eta_nominal": ETA_SCAN,
            "eta_tight": [0.0, 0.1],
            "tol_nominal": TOL_NOMINAL,
            "tol_tight": TOL_TIGHT,
            "redshifts": Z.tolist(),
            "L_min": LMIN,
            "L_max": LMAX,
            "canonical_k_output_seed": CANON_KH,
            "P_k_max_h/Mpc": 5.0,
            "non_linear": False,
            "science_method": (
                "direct physical small eta; CLASS sigma/effective_f_sigma8/raw C_L^phiphi"
            ),
        },
        "runs": runs,
        "gates": gates,
        "summary": summary,
        "interpretation": {
            "local_observable_tangent_licensed": classification == CLS_PASS,
            "r5_reclassified": False,
            "observational_claim_licensed": False,
            "likelihood_claim_licensed": False,
            "positive_growth_weyl_separation_licensed": False,
        },
    }

    Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    np.savez_compressed(args.npz_out, **arrays)
    print(
        "STABLE_AEST_OBSERVABLE_PROJECTION_R5A_GATES="
        + json.dumps(gates, sort_keys=True),
        flush=True,
    )
    print(
        "STABLE_AEST_OBSERVABLE_PROJECTION_R5A_SUMMARY="
        + json.dumps(summary, sort_keys=True),
        flush=True,
    )
    print(
        "STABLE_AEST_OBSERVABLE_PROJECTION_R5A_CLASSIFICATION=" + classification,
        flush=True,
    )
    return 0 if classification == CLS_PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
