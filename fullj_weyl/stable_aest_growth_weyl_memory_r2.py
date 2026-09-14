#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
from scipy.interpolate import PchipInterpolator

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fullj_weyl import aest_ulp_initial_amplitude_localization as amp
from fullj_weyl import aest_stable_chi_precision_convergence as pc

PREDATA_LOCK = "5fdb18b7fb40898ad6963fe4d4e5874c39bc0617"
R1C_POSTDATA_LOCK = "62d7649ebb5dd45a00be3272bf2ee8d5ab30a49a"
HISTORY_LOCK = "3fcbb4f610844f20d3e45045e829a9a8a69be87c"
R1C_JSON = ROOT / "results/stable_aest_finite_memory_r1c.json"
HOST_JSON = ROOT / "results/fullj_aest_stable_chi_precision_floor.json"
R1C_CLASS = "STABLE_AEST_FINITE_MEMORY_R1C_LONG_RELAXATION_CERTIFIED"
HOST_CLASS = "FULLJ_AEST_STABLE_CHI_PRECISION_FLOOR_CERTIFIED"

ANCHORS = (0.09875, 0.16125, 0.19500)
ETAS = (0.0, 0.005, 0.01)
TAU = 10.0
ORDER = 20
TOL = 3e-8
Z = np.asarray([6., 5., 4., 3., 2., 1.5, 1., 0.5, 0.2], float)
HI = np.asarray([0, 1, 2, 3], int)
LO = np.asarray([6, 7, 8], int)
LATE = np.asarray([4, 5, 6, 7, 8], int)

INCOMPLETE = "STABLE_AEST_GROWTH_WEYL_MEMORY_R2_INCOMPLETE"
BASIS_FAIL = "STABLE_AEST_GROWTH_WEYL_MEMORY_R2_TRANSFER_BASIS_FAIL"
TANGENT_FAIL = "STABLE_AEST_GROWTH_WEYL_MEMORY_R2_TANGENT_FAIL"
SEP_FAIL = "STABLE_AEST_GROWTH_WEYL_MEMORY_R2_SEPARATION_UNRESOLVED"
LATE_FAIL = "STABLE_AEST_GROWTH_WEYL_MEMORY_R2_LATE_ACTIVATION_FAIL"
COH_FAIL = "STABLE_AEST_GROWTH_WEYL_MEMORY_R2_CROSS_K_COHERENCE_FAIL"
PASS = "STABLE_AEST_GROWTH_WEYL_MEMORY_R2_SEPARATION_PASS"


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
    if na <= 0. or nb <= 0.:
        return float("nan")
    return float(np.dot(a, b)/(na*nb))


def rms(a) -> float:
    a = np.asarray(a, float)
    return float(np.sqrt(np.mean(a*a)))


def source_ok() -> bool:
    root = os.environ.get("AEST_STABLE_CLASS_ROOT", "")
    if not root:
        return False
    root = Path(root)
    paths = [root/"source/perturbations.c", root/"include/perturbations.h",
             root/"include/background.h", root/"source/aest_memory.c"]
    if not all(p.is_file() for p in paths):
        return False
    text = "\n".join(p.read_text() for p in paths)
    req = (
        "FULLJ_AEST_STABLE_CHI_RESIDUAL_V1",
        "double chi_aest = Q_aest*s_aest;",
        "aest_memory_enabled",
        "aest_memory_order",
        "E_rhs_aest -= 0.5*Q_aest*Bchi_aest",
        "if (order == 20)",
    )
    return all(x in text for x in req) and text.count("double chi_aest = Q_aest*s_aest;") >= 2


def k_h_from_transfer(tr, h):
    candidates = (
        ("k (h/Mpc)", 1.0), ("k [h/Mpc]", 1.0), ("k[h/Mpc]", 1.0),
        ("k (1/Mpc)", 1.0/h), ("k [1/Mpc]", 1.0/h), ("k[1/Mpc]", 1.0/h),
    )
    for key, fac in candidates:
        if key in tr:
            return np.asarray(tr[key], float)*fac, key
    raise RuntimeError("no recognized transfer-k key; keys=" + repr(sorted(tr.keys())))


def interp_transfer_field(kh_grid, values, target):
    k = np.asarray(kh_grid, float); y = np.asarray(values, float)
    good = np.isfinite(k) & np.isfinite(y) & (k > 0.)
    k = k[good]; y = y[good]
    order = np.argsort(k); k = k[order]; y = y[order]
    keep = np.ones(k.size, dtype=bool)
    if k.size > 1:
        keep[1:] = np.diff(k) > 0.
    k = k[keep]; y = y[keep]
    if k.size < 4 or not (k[0] <= target <= k[-1]):
        raise RuntimeError(f"target k={target} outside/undersampled transfer domain [{k[0] if k.size else np.nan},{k[-1] if k.size else np.nan}]")
    sp = PchipInterpolator(np.log(k), y, extrapolate=False)
    v = float(sp(np.log(float(target))))
    if not np.isfinite(v):
        raise RuntimeError("nonfinite transfer interpolation")
    return v, float(k[0]), float(k[-1]), int(k.size)


def classy_h(c) -> float:
    x = c.h
    try:
        return float(x())
    except TypeError:
        return float(x)


def run_case(kh: float, eta: float):
    from classy import Class

    bits = pc.bits_for_anchor(kh)
    p, pos = amp.make_params(kh, int(bits))
    p["tol_perturbations_integration"] = float(TOL)
    p["aest_memory_enabled"] = "yes"
    p["aest_memory_order"] = int(ORDER)
    p["aest_eta"] = float(eta)
    p["aest_tau_H0"] = float(TAU)
    p["output"] = "mTk,vTk"
    p["z_max_pk"] = max(float(p.get("z_max_pk", 0.0)), 6.5)

    c = Class(); c.set(p); c.compute()
    rows = []
    try:
        h = classy_h(c)
        D = []; W = []; domains = []; keys = []
        for z in Z:
            tr = c.get_transfer(z=float(z), output_format="class")
            missing = [x for x in ("d_m", "phi", "psi") if x not in tr]
            if missing:
                raise RuntimeError(f"missing transfer fields {missing}; keys={sorted(tr.keys())}")
            kg, kkey = k_h_from_transfer(tr, h)
            dm, klo, khi, nk = interp_transfer_field(kg, tr["d_m"], kh)
            ph, _, _, _ = interp_transfer_field(kg, tr["phi"], kh)
            ps, _, _, _ = interp_transfer_field(kg, tr["psi"], kh)
            D.append(dm); W.append(ph+ps); domains.append((klo, khi, nk)); keys.append(kkey)
        D = np.asarray(D, float); W = np.asarray(W, float)
        finite = bool(np.all(np.isfinite(D)) and np.all(np.isfinite(W)))
        return {
            "D": D, "W": W, "finite": finite, "bits": int(bits), "target_pos": int(pos),
            "k_keys": keys, "domains": domains, "h": float(h),
        }
    finally:
        c.struct_cleanup(); c.empty()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json-out", default="results/stable_aest_growth_weyl_memory_r2.json")
    ap.add_argument("--npz-out", default="results/stable_aest_growth_weyl_memory_r2.npz")
    args = ap.parse_args()

    print("STABLE_AEST_GROWTH_WEYL_MEMORY_R2_START", flush=True)

    if not R1C_JSON.exists() or not HOST_JSON.exists():
        out = {"classification": INCOMPLETE, "diagnostic_complete": False, "reason": "missing parent json"}
        Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True)+"\n")
        print("STABLE_AEST_GROWTH_WEYL_MEMORY_R2_CLASSIFICATION="+INCOMPLETE, flush=True)
        return 3

    r1c = json.loads(R1C_JSON.read_text()); host = json.loads(HOST_JSON.read_text())
    g1 = bool(
        ancestor(PREDATA_LOCK) and ancestor(R1C_POSTDATA_LOCK) and ancestor(HISTORY_LOCK)
        and r1c.get("classification") == R1C_CLASS
        and r1c.get("interpretation", {}).get("long_relaxation_growth_Weyl_followup_licensed") is True
        and host.get("classification") == HOST_CLASS
        and source_ok()
    )

    arrays = {"redshifts": Z}
    vals = {}; run_rows = []; basis_ok = True
    for kh in ANCHORS:
        for eta in ETAS:
            tag = pc.tag_of(kh); et = f"{eta:.3f}".replace(".", "p")
            try:
                v = run_case(kh, eta)
                vals[(kh, eta)] = v
                arrays[f"D_{tag}_e{et}"] = v["D"]
                arrays[f"W_{tag}_e{et}"] = v["W"]
                domains_ok = all(d[0] <= kh <= d[1] and d[2] >= 4 for d in v["domains"])
                keys_ok = len(set(v["k_keys"])) == 1
                this = bool(v["finite"] and domains_ok and keys_ok)
                basis_ok &= this
                run_rows.append({"k_h": kh, "eta": eta, "finite": v["finite"], "basis_pass": this,
                                 "bits": v["bits"], "target_pos": v["target_pos"], "h": v["h"],
                                 "k_key": v["k_keys"][0] if v["k_keys"] else None,
                                 "min_k_h": float(min(d[0] for d in v["domains"])),
                                 "max_k_h": float(max(d[1] for d in v["domains"])),
                                 "min_k_count": int(min(d[2] for d in v["domains"]))})
                print(f"STABLE_AEST_GROWTH_WEYL_MEMORY_R2_RUN k_h={kh:.5f} eta={eta:.3g} finite={v['finite']} basis={this}", flush=True)
            except Exception as e:
                basis_ok = False
                run_rows.append({"k_h": kh, "eta": eta, "finite": False, "basis_pass": False, "error": repr(e)})
                print(f"STABLE_AEST_GROWTH_WEYL_MEMORY_R2_RUN_FAIL k_h={kh:.5f} eta={eta:.3g} error={e!r}", flush=True)

    # Denominator validity is part of the transfer-basis gate.
    if len(vals) == len(ANCHORS)*len(ETAS):
        for kh in ANCHORS:
            d0 = vals[(kh, 0.0)]["D"]; w0 = vals[(kh, 0.0)]["W"]
            basis_ok &= bool(np.all(np.isfinite(d0)) and np.all(np.isfinite(w0))
                             and np.all(np.abs(d0) > 1e-300) and np.all(np.abs(w0) > 1e-300))
    else:
        basis_ok = False

    tangent_rows = []; sep_rows = []; late_rows = []
    tangent_strict = 0; tangent_loose_all = True
    sep_ge3 = 0; sep_ge1_all = True
    late_ge2 = 0; late_ge1_all = True
    R10 = {}

    if basis_ok:
        for kh in ANCHORS:
            d0 = vals[(kh,0.0)]["D"]; w0 = vals[(kh,0.0)]["W"]
            D5 = vals[(kh,0.005)]["D"]; W5 = vals[(kh,0.005)]["W"]
            D10 = vals[(kh,0.01)]["D"]; W10 = vals[(kh,0.01)]["W"]
            G5 = (D5-d0)/(0.005*d0); G10 = (D10-d0)/(0.01*d0)
            L5 = (W5-w0)/(0.005*w0); L10 = (W10-w0)/(0.01*w0)
            R5 = L5-G5; R = L10-G10; R10[kh] = R
            tag = pc.tag_of(kh)
            for n,x in (("G005",G5),("G010",G10),("L005",L5),("L010",L10),("R005",R5),("R010",R)):
                arrays[f"{n}_{tag}"] = x

            eG = rel(G5,G10); eL = rel(L5,L10); eR = rel(R5,R)
            strict = bool(eG <= 0.10 and eL <= 0.10 and eR <= 0.15)
            loose = bool(eG <= 0.25 and eL <= 0.25 and eR <= 0.30)
            tangent_strict += int(strict); tangent_loose_all &= loose
            tangent_rows.append({"k_h":kh,"E_G":eG,"E_L":eL,"E_R":eR,"strict_pass":strict,"loose_pass":loose})
            print(f"STABLE_AEST_GROWTH_WEYL_MEMORY_R2_TANGENT k_h={kh:.5f} EG={eG:.3e} EL={eL:.3e} ER={eR:.3e} strict={strict}", flush=True)

            sR = float(np.linalg.norm(R)); nR = float(np.linalg.norm(R5-R)); q = sR/max(nR,1e-300)
            nonzero = bool(np.isfinite(sR) and sR > 0.)
            p3 = bool(nonzero and q >= 3.); p1 = bool(nonzero and q >= 1.)
            sep_ge3 += int(p3); sep_ge1_all &= p1
            sep_rows.append({"k_h":kh,"S_R":sR,"N_R":nR,"Q_sep":q,"pass_ge3":p3,"pass_ge1":p1})
            print(f"STABLE_AEST_GROWTH_WEYL_MEMORY_R2_SEP k_h={kh:.5f} S={sR:.3e} N={nR:.3e} Q={q:.3e}", flush=True)

            ahi = rms(np.abs(R[HI])); alo = rms(np.abs(R[LO])); fl = alo/max(ahi,1e-300)
            p2 = bool(np.isfinite(fl) and fl >= 2.); p1late = bool(np.isfinite(fl) and fl >= 1.)
            late_ge2 += int(p2); late_ge1_all &= p1late
            late_rows.append({"k_h":kh,"A_hi":ahi,"A_lo":alo,"F_late":fl,"pass_ge2":p2,"pass_ge1":p1late,
                              "R_z0p2":float(R[-1])})
            print(f"STABLE_AEST_GROWTH_WEYL_MEMORY_R2_LATE k_h={kh:.5f} Ahi={ahi:.3e} Alo={alo:.3e} F={fl:.3e} Rz02={R[-1]:.3e}", flush=True)

    coherence_rows = []; coherence_ok = False; min_cos = float("nan")
    if basis_ok and len(R10) == len(ANCHORS):
        aligned = {}
        valid = True
        for kh in ANCHORS:
            r = np.asarray(R10[kh][LATE], float)
            s = float(R10[kh][-1])
            nr = float(np.linalg.norm(r))
            if not np.all(np.isfinite(r)) or s == 0. or nr <= 0.:
                valid = False; break
            aligned[kh] = np.sign(s)*r/nr
        if valid:
            cs = []
            for i in range(len(ANCHORS)):
                for j in range(i+1,len(ANCHORS)):
                    c = cosine(aligned[ANCHORS[i]], aligned[ANCHORS[j]])
                    cs.append(c); coherence_rows.append({"k_h_a":ANCHORS[i],"k_h_b":ANCHORS[j],"cosine":c})
            min_cos = float(min(cs)); coherence_ok = bool(np.isfinite(min_cos) and min_cos >= 0.75)
            print(f"STABLE_AEST_GROWTH_WEYL_MEMORY_R2_COHERENCE min_cos={min_cos:.9f} pass={coherence_ok}", flush=True)

    g2 = bool(basis_ok)
    g3 = bool(g2 and tangent_loose_all and tangent_strict >= 2)
    g4 = bool(g2 and sep_ge1_all and sep_ge3 >= 2)
    g5 = bool(g2 and late_ge1_all and late_ge2 >= 2)
    g6 = bool(g2 and coherence_ok)

    gates = {
        "R2_G1_provenance_and_certified_parent_lock": g1,
        "R2_G2_transfer_basis_validity": g2,
        "R2_G3_matched_tangent_reproducibility": g3,
        "R2_G4_resolved_growth_Weyl_separation": g4,
        "R2_G5_late_time_activation": g5,
        "R2_G6_cross_k_temporal_coherence": g6,
    }

    if not g1: classification = INCOMPLETE
    elif not g2: classification = BASIS_FAIL
    elif not g3: classification = TANGENT_FAIL
    elif not g4: classification = SEP_FAIL
    elif not g5: classification = LATE_FAIL
    elif not g6: classification = COH_FAIL
    else: classification = PASS

    summary = {
        "classification": classification,
        "run_count": len(run_rows),
        "basis_pass_count": int(sum(bool(r.get("basis_pass",False)) for r in run_rows)),
        "tangent_strict_pass_count": int(tangent_strict),
        "separation_Q_ge3_count": int(sep_ge3),
        "late_F_ge2_count": int(late_ge2),
        "min_cross_k_cosine": min_cos,
        "min_Q_sep": float(min((r["Q_sep"] for r in sep_rows), default=np.nan)),
        "min_F_late": float(min((r["F_late"] for r in late_rows), default=np.nan)),
        "max_E_G": float(max((r["E_G"] for r in tangent_rows), default=np.nan)),
        "max_E_L": float(max((r["E_L"] for r in tangent_rows), default=np.nan)),
        "max_E_R": float(max((r["E_R"] for r in tangent_rows), default=np.nan)),
    }

    out = {
        "classification": classification,
        "diagnostic_complete": True,
        "predata_lock": PREDATA_LOCK,
        "r1c_parent_classification": r1c.get("classification"),
        "host_parent_classification": host.get("classification"),
        "settings": {"anchors":list(ANCHORS),"etas":list(ETAS),"tau_H0":TAU,"memory_order":ORDER,
                     "tol_perturbations_integration":TOL,"redshifts":Z.tolist(),"growth_observable":"CLASS d_m",
                     "weyl_observable":"CLASS phi+psi","k_interpolation":"PCHIP in log(k_h), no extrapolation"},
        "gates": gates,
        "summary": summary,
        "runs": run_rows,
        "tangent": tangent_rows,
        "separation": sep_rows,
        "late_activation": late_rows,
        "cross_k_coherence": coherence_rows,
        "interpretation": {
            "historical_results_reclassified": False,
            "tau1_certified": False,
            "MCMG_first_moment_relation_certified": False,
            "observational_claim_licensed": False,
            "new_physics_claim_licensed": False,
            "growth_Weyl_separation_certified": classification == PASS,
            "MCMG_bridge_followup_licensed": classification == PASS,
        },
    }

    Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True)+"\n")
    np.savez_compressed(args.npz_out, **arrays)
    print("STABLE_AEST_GROWTH_WEYL_MEMORY_R2_GATES="+json.dumps(gates,sort_keys=True), flush=True)
    print("STABLE_AEST_GROWTH_WEYL_MEMORY_R2_SUMMARY="+json.dumps(summary,sort_keys=True), flush=True)
    print("STABLE_AEST_GROWTH_WEYL_MEMORY_R2_CLASSIFICATION="+classification, flush=True)
    return 0 if classification == PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
