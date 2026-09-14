#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fullj_weyl import aest_ulp_initial_amplitude_localization as amp
from fullj_weyl import aest_stable_chi_precision_convergence as pc

PREDATA_LOCK = "a7b10d1a9195ad41ea1ce456c259bd88351a951a"
PARENT_JSON = ROOT / "results/fullj_aest_stable_chi_precision_floor.json"
PARENT_CLASS = "FULLJ_AEST_STABLE_CHI_PRECISION_FLOOR_CERTIFIED"

Z = np.asarray([6., 5., 4., 3., 2., 1.5, 1., 0.5, 0.2], float)
ANCHORS = (0.10000, 0.16500, 0.19750)
ETAS = (0.0025, 0.005, 0.01)
TAUS = (1.0, 10.0)
TOL = 1e-7
ORDER = 16

INCOMPLETE = "STABLE_AEST_FINITE_MEMORY_R1_INCOMPLETE"
ZERO_FAIL = "STABLE_AEST_FINITE_MEMORY_R1_ZERO_REGRESSION_FAIL"
REGULARITY_FAIL = "STABLE_AEST_FINITE_MEMORY_R1_NUMERICAL_REGULARITY_FAIL"
SMOOTH_FAIL = "STABLE_AEST_FINITE_MEMORY_R1_ETA_SMOOTHNESS_FAIL"
SMALL_FAIL = "STABLE_AEST_FINITE_MEMORY_R1_RESPONSE_TOO_SMALL"
TAU_FAIL = "STABLE_AEST_FINITE_MEMORY_R1_RELAXATION_TIME_FAIL"
PASS = "STABLE_AEST_FINITE_MEMORY_R1_PASS"


def is_ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"], cwd=ROOT,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    ).returncode == 0


def rel(a, b) -> float:
    aa = np.asarray(a, float)
    bb = np.asarray(b, float)
    return float(np.linalg.norm(aa-bb) / max(float(np.linalg.norm(aa)), float(np.linalg.norm(bb)), 1e-300))


def amp_rel(delta, base) -> float:
    dd = np.asarray(delta, float)
    bb = np.asarray(base, float)
    return float(np.linalg.norm(dd) / max(float(np.linalg.norm(bb)), 1e-300))


def linerr(big, small) -> float:
    aa = np.asarray(big, float)
    bb = np.asarray(small, float)
    return float(np.linalg.norm(aa-2.*bb) /
                 max(float(np.linalg.norm(aa)), 2.*float(np.linalg.norm(bb)), 1e-300))


def source_audit_ok() -> bool:
    root = os.environ.get("AEST_STABLE_CLASS_ROOT", "")
    if not root:
        return False
    root = Path(root)
    ph = root / "include" / "perturbations.h"
    bh = root / "include" / "background.h"
    pcsrc = root / "source" / "perturbations.c"
    if not ph.is_file() or not bh.is_file() or not pcsrc.is_file():
        return False
    text = ph.read_text() + "\n" + bh.read_text() + "\n" + pcsrc.read_text()
    required = (
        "FULLJ_AEST_STABLE_CHI_RESIDUAL_V1",
        "index_pt_s_aest",
        "double chi_aest = Q_aest*s_aest;",
        "aest_memory_enabled",
        "aest_eta",
        "aest_tau_H0",
        "aest_memory_order",
        "index_pt_mem_q_aest",
        "index_pt_mem_p_aest",
        "E_rhs_aest -= 0.5*Q_aest*Bchi_aest",
    )
    return all(x in text for x in required) and text.count("double chi_aest = Q_aest*s_aest;") >= 2


def field_at_z(raw, names):
    return pc.field_at_z(raw, names)


def extract(raw):
    out = {
        "delta": field_at_z(raw, ("delta_cdm",)),
        "alpha": field_at_z(raw, ("alpha_aest", "alpha")),
        "E": field_at_z(raw, ("E_aest", "E")),
        "s": field_at_z(raw, ("s_aest",)),
    }
    phi = field_at_z(raw, ("phi",))
    psi = field_at_z(raw, ("psi",))
    out["phi"] = phi
    out["psi"] = psi
    out["W"] = phi + psi
    return out


def run_case(kh: float, memory_enabled: bool, eta: float, tau: float):
    bits = pc.bits_for_anchor(kh)
    p, pos = amp.make_params(kh, int(bits))
    p["tol_perturbations_integration"] = float(TOL)
    p["aest_memory_enabled"] = "yes" if memory_enabled else "no"
    p["aest_eta"] = float(eta)
    p["aest_tau_H0"] = float(tau)
    p["aest_memory_order"] = int(ORDER)
    raw, nh = amp.raw_target(p, pos, True)
    vals = extract(raw)
    finite = all(np.all(np.isfinite(v)) for v in vals.values())
    return vals, int(nh), int(pos), int(bits), bool(finite)


def key_eta(x: float) -> str:
    return f"{x:.4f}".replace(".", "p")


def key_tau(x: float) -> str:
    return f"{x:.0f}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json-out", default="results/stable_aest_finite_memory_r1.json")
    ap.add_argument("--npz-out", default="results/stable_aest_finite_memory_r1.npz")
    args = ap.parse_args()

    print("STABLE_AEST_FINITE_MEMORY_R1_START", flush=True)

    if not PARENT_JSON.exists():
        out = {"classification": INCOMPLETE, "diagnostic_complete": False,
               "reason": "missing stable-AeST precision-floor parent"}
        Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True)+"\n")
        print("STABLE_AEST_FINITE_MEMORY_R1_CLASSIFICATION="+INCOMPLETE, flush=True)
        return 3

    parent = json.loads(PARENT_JSON.read_text())
    g1 = bool(
        is_ancestor(PREDATA_LOCK)
        and parent.get("classification") == PARENT_CLASS
        and parent.get("diagnostic_complete") is True
        and parent.get("interpretation", {}).get("stable_AeST_host_followup_licensed") is True
        and source_audit_ok()
    )

    arrays = {"redshifts": Z}
    base = {}
    zero = {}
    finite = {}
    zero_rows = []
    regular_rows = []

    # A. Memory-off stable baseline.
    for kh in ANCHORS:
        vals, nh, pos, bits, ok = run_case(kh, False, 0.0, 10.0)
        base[kh] = vals
        tag = pc.tag_of(kh)
        for name, v in vals.items():
            arrays[f"base_{name}_{tag}"] = v
        print(f"STABLE_AEST_FINITE_MEMORY_R1_BASE k_h={kh:.5f} finite={ok} histories={nh} pos={pos}", flush=True)

    # B. Memory enabled with eta=0.
    zero_ok = True
    for kh in ANCHORS:
        vals, nh, pos, bits, ok = run_case(kh, True, 0.0, 10.0)
        zero[kh] = vals
        tag = pc.tag_of(kh)
        for name, v in vals.items():
            arrays[f"eta0_{name}_{tag}"] = v
        rr = {name: rel(vals[name], base[kh][name]) for name in ("W", "delta", "alpha", "E", "s")}
        this = bool(ok and rr["W"] <= 1e-5 and rr["delta"] <= 1e-5
                    and rr["alpha"] <= 5e-5 and rr["E"] <= 5e-5 and rr["s"] <= 5e-5)
        zero_ok &= this
        row = {"k_h": kh, "finite": ok, "pass": this, **{f"{k}_relL2": v for k, v in rr.items()}}
        zero_rows.append(row)
        print("STABLE_AEST_FINITE_MEMORY_R1_ZERO "
              f"k_h={kh:.5f} W={rr['W']:.3e} delta={rr['delta']:.3e} "
              f"alpha={rr['alpha']:.3e} E={rr['E']:.3e} s={rr['s']:.3e} pass={this}", flush=True)

    # C. Finite-memory scan.
    all_regular = True
    for tau in TAUS:
        for eta in ETAS:
            for kh in ANCHORS:
                vals, nh, pos, bits, ok = run_case(kh, True, eta, tau)
                finite[(kh, eta, tau)] = vals
                tag = pc.tag_of(kh)
                ek = key_eta(eta); tk = key_tau(tau)
                for name, v in vals.items():
                    arrays[f"mem_{name}_e{ek}_t{tk}_{tag}"] = v
                dW = vals["W"] - base[kh]["W"]
                dd = vals["delta"] - base[kh]["delta"]
                Aw = amp_rel(dW, base[kh]["W"])
                Ad = amp_rel(dd, base[kh]["delta"])
                this = bool(ok and Aw <= 0.25 and Ad <= 0.25)
                all_regular &= this
                regular_rows.append({"k_h": kh, "eta": eta, "tau_H0": tau,
                                     "finite": ok, "A_W": Aw, "A_delta": Ad, "pass": this})
                print(f"STABLE_AEST_FINITE_MEMORY_R1_MEM k_h={kh:.5f} eta={eta:.4g} tau={tau:.0f} "
                      f"A_W={Aw:.3e} A_delta={Ad:.3e} finite={ok} pass={this}", flush=True)

    # D. eta smoothness.
    smooth_rows = []
    smooth_pass = 0
    smooth_all_loose = True
    for tau in TAUS:
        for kh in ANCHORS:
            d1 = finite[(kh, 0.0025, tau)]["W"] - base[kh]["W"]
            d2 = finite[(kh, 0.005, tau)]["W"] - base[kh]["W"]
            d3 = finite[(kh, 0.01, tau)]["W"] - base[kh]["W"]
            L1 = linerr(d2, d1)
            L2 = linerr(d3, d2)
            mx = max(L1, L2)
            strict = bool(mx <= 0.10)
            loose = bool(mx <= 0.25)
            smooth_pass += int(strict)
            smooth_all_loose &= loose
            smooth_rows.append({"k_h": kh, "tau_H0": tau, "L1": L1, "L2": L2,
                                "max_L": mx, "strict_pass": strict, "loose_pass": loose})
            print(f"STABLE_AEST_FINITE_MEMORY_R1_SMOOTH k_h={kh:.5f} tau={tau:.0f} "
                  f"L1={L1:.3e} L2={L2:.3e} strict={strict}", flush=True)

    # E. material response and tau dependence at eta=0.01.
    response_rows = []
    material_count = 0
    tau_count = 0
    for kh in ANCHORS:
        d10 = finite[(kh, 0.01, 10.0)]["W"] - base[kh]["W"]
        d1 = finite[(kh, 0.01, 1.0)]["W"] - base[kh]["W"]
        Aw10 = amp_rel(d10, base[kh]["W"])
        Ttau = rel(d10, d1)
        material = bool(Aw10 >= 1e-8)
        taupass = bool(Ttau >= 0.01)
        material_count += int(material)
        tau_count += int(taupass)
        response_rows.append({"k_h": kh, "A_W_eta001_tau10": Aw10,
                              "T_tau": Ttau, "material_pass": material,
                              "tau_dependence_pass": taupass})
        print(f"STABLE_AEST_FINITE_MEMORY_R1_RESPONSE k_h={kh:.5f} A_W={Aw10:.3e} "
              f"T_tau={Ttau:.3e} material={material} taupass={taupass}", flush=True)

    g2 = bool(zero_ok)
    g3 = bool(all_regular)
    g4 = bool(smooth_pass >= 5 and smooth_all_loose)
    g5 = bool(material_count >= 2)
    g6 = bool(tau_count >= 2)

    gates = {
        "FM_G1_provenance_and_stable_host_lock": g1,
        "FM_G2_zero_coupling_memory_regression": g2,
        "FM_G3_finite_memory_numerical_regularity": g3,
        "FM_G4_small_eta_smoothness": g4,
        "FM_G5_material_memory_response": g5,
        "FM_G6_relaxation_time_dependence": g6,
    }

    if not g1:
        classification = INCOMPLETE
    elif not g2:
        classification = ZERO_FAIL
    elif not g3:
        classification = REGULARITY_FAIL
    elif not g4:
        classification = SMOOTH_FAIL
    elif not g5:
        classification = SMALL_FAIL
    elif not g6:
        classification = TAU_FAIL
    else:
        classification = PASS

    summary = {
        "classification": classification,
        "anchor_count": len(ANCHORS),
        "finite_run_count": len(regular_rows),
        "zero_regression_pass_count": int(sum(r["pass"] for r in zero_rows)),
        "regularity_pass_count": int(sum(r["pass"] for r in regular_rows)),
        "smooth_strict_pass_count": int(smooth_pass),
        "smooth_cell_count": len(smooth_rows),
        "material_response_pass_count": int(material_count),
        "tau_dependence_pass_count": int(tau_count),
        "max_zero_W_relL2": float(max(r["W_relL2"] for r in zero_rows)),
        "max_A_W": float(max(r["A_W"] for r in regular_rows)),
        "max_A_delta": float(max(r["A_delta"] for r in regular_rows)),
        "max_smoothness_error": float(max(r["max_L"] for r in smooth_rows)),
        "min_material_A_W_eta001_tau10": float(min(r["A_W_eta001_tau10"] for r in response_rows)),
        "min_T_tau": float(min(r["T_tau"] for r in response_rows)),
    }

    out = {
        "classification": classification,
        "diagnostic_complete": True,
        "predata_lock": PREDATA_LOCK,
        "parent_classification": parent.get("classification"),
        "settings": {"anchors": list(ANCHORS), "etas": list(ETAS), "taus_H0": list(TAUS),
                     "memory_order": ORDER, "tol_perturbations_integration": TOL,
                     "redshifts": Z.tolist()},
        "gates": gates,
        "summary": summary,
        "zero_regression": zero_rows,
        "finite_runs": regular_rows,
        "eta_smoothness": smooth_rows,
        "response_and_tau": response_rows,
        "interpretation": {
            "historical_results_reclassified": False,
            "observational_claim_licensed": False,
            "new_physics_claim_licensed": False,
            "permanent_elasticity_loss_claim_licensed": False,
            "stable_AeST_growth_Weyl_memory_followup_licensed": classification == PASS,
        },
    }

    Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True)+"\n")
    np.savez_compressed(args.npz_out, **arrays)
    print("STABLE_AEST_FINITE_MEMORY_R1_GATES="+json.dumps(gates, sort_keys=True), flush=True)
    print("STABLE_AEST_FINITE_MEMORY_R1_SUMMARY="+json.dumps(summary, sort_keys=True), flush=True)
    print("STABLE_AEST_FINITE_MEMORY_R1_CLASSIFICATION="+classification, flush=True)
    return 0 if classification == PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
