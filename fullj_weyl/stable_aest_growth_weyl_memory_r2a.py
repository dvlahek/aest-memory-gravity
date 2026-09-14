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

from fullj_weyl import stable_aest_growth_weyl_memory_r2 as r2

PREDATA_LOCK = "4611d8b41f2c8a3293c34642a21eacb9b17f79a6"
R2_POSTDATA_LOCK = "938ca66087daed82c68ee8ff5aa56b98bb383254"
R2_JSON = ROOT / "results/stable_aest_growth_weyl_memory_r2.json"
R2_NPZ = ROOT / "results/stable_aest_growth_weyl_memory_r2.npz"
R1C_JSON = ROOT / "results/stable_aest_finite_memory_r1c.json"
HOST_JSON = ROOT / "results/fullj_aest_stable_chi_precision_floor.json"

R2_CLASS = "STABLE_AEST_GROWTH_WEYL_MEMORY_R2_TANGENT_FAIL"
R1C_CLASS = "STABLE_AEST_FINITE_MEMORY_R1C_LONG_RELAXATION_CERTIFIED"
HOST_CLASS = "FULLJ_AEST_STABLE_CHI_PRECISION_FLOOR_CERTIFIED"

ANCHORS = (0.09875, 0.16125, 0.19500)
PRIMARY_ETAS = (0.0, 0.01, 0.02, 0.04)
REUSED_ETAS = (0.0, 0.01)
NEW_PRIMARY_ETAS = (0.02, 0.04)
TAU = 10.0
ORDER = 20
PRIMARY_TOL = 3e-8
TIGHT_TOL = 1e-8
Z = np.asarray([6., 5., 4., 3., 2., 1.5, 1., 0.5, 0.2], float)

INCOMPLETE = "STABLE_AEST_GROWTH_WEYL_MEMORY_R2A_INCOMPLETE"
TRANSFER_FAIL = "STABLE_AEST_GROWTH_WEYL_MEMORY_R2A_TRANSFER_FAIL"
NONLINEAR = "STABLE_AEST_GROWTH_WEYL_MEMORY_R2A_INDIVIDUAL_NONLINEAR"
RESOLVED = "STABLE_AEST_GROWTH_WEYL_MEMORY_R2A_SEPARATION_RESOLVED"
FLOOR = "STABLE_AEST_GROWTH_WEYL_MEMORY_R2A_DIFFERENTIAL_FLOOR_SUPPORTED"
UNRESOLVED = "STABLE_AEST_GROWTH_WEYL_MEMORY_R2A_SEPARATION_UNRESOLVED"


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


def tag(kh: float) -> str:
    return r2.pc.tag_of(kh)


def etag(eta: float) -> str:
    return f"{eta:.3f}".replace(".", "p")


def run_case(kh: float, eta: float, tol: float):
    from classy import Class

    bits = r2.pc.bits_for_anchor(kh)
    p, pos = r2.amp.make_params(kh, int(bits))
    p["tol_perturbations_integration"] = float(tol)
    p["aest_memory_enabled"] = "yes"
    p["aest_memory_order"] = int(ORDER)
    p["aest_eta"] = float(eta)
    p["aest_tau_H0"] = float(TAU)
    p["output"] = "mTk,vTk"
    p["z_max_pk"] = max(float(p.get("z_max_pk", 0.0)), 6.5)

    c = Class(); c.set(p); c.compute()
    try:
        h = r2.classy_h(c)
        D = []; W = []; domains = []; keys = []
        for z in Z:
            tr = c.get_transfer(z=float(z), output_format="class")
            missing = [x for x in ("d_m", "phi", "psi") if x not in tr]
            if missing:
                raise RuntimeError(f"missing transfer fields {missing}; keys={sorted(tr.keys())}")
            kg, kkey = r2.k_h_from_transfer(tr, h)
            dm, klo, khi, nk = r2.interp_transfer_field(kg, tr["d_m"], kh)
            ph, _, _, _ = r2.interp_transfer_field(kg, tr["phi"], kh)
            ps, _, _, _ = r2.interp_transfer_field(kg, tr["psi"], kh)
            D.append(dm); W.append(ph+ps); domains.append((klo, khi, nk)); keys.append(kkey)
        D = np.asarray(D, float); W = np.asarray(W, float)
        finite = bool(np.all(np.isfinite(D)) and np.all(np.isfinite(W)))
        domains_ok = all(d[0] <= kh <= d[1] and d[2] >= 4 for d in domains)
        keys_ok = len(set(keys)) == 1
        return {
            "D": D, "W": W, "finite": finite, "basis_pass": bool(finite and domains_ok and keys_ok),
            "bits": int(bits), "target_pos": int(pos), "h": float(h),
            "k_key": keys[0] if keys else None,
            "min_k_h": float(min(d[0] for d in domains)),
            "max_k_h": float(max(d[1] for d in domains)),
            "min_k_count": int(min(d[2] for d in domains)),
        }
    finally:
        c.struct_cleanup(); c.empty()


def matched_tangents(v0, ve, eta: float):
    D0 = np.asarray(v0["D"], float); W0 = np.asarray(v0["W"], float)
    D = np.asarray(ve["D"], float); W = np.asarray(ve["W"], float)
    G = (D-D0)/(float(eta)*D0)
    L = (W-W0)/(float(eta)*W0)
    R = L-G
    P = float(eta)*R
    return G, L, R, P


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json-out", default="results/stable_aest_growth_weyl_memory_r2a.json")
    ap.add_argument("--npz-out", default="results/stable_aest_growth_weyl_memory_r2a.npz")
    args = ap.parse_args()

    print("STABLE_AEST_GROWTH_WEYL_MEMORY_R2A_START", flush=True)

    required = (R2_JSON, R2_NPZ, R1C_JSON, HOST_JSON)
    if not all(p.exists() for p in required):
        out = {"classification": INCOMPLETE, "diagnostic_complete": False, "reason": "missing parent result"}
        Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True)+"\n")
        print("STABLE_AEST_GROWTH_WEYL_MEMORY_R2A_CLASSIFICATION="+INCOMPLETE, flush=True)
        return 3

    r2j = json.loads(R2_JSON.read_text())
    r1c = json.loads(R1C_JSON.read_text())
    host = json.loads(HOST_JSON.read_text())
    parent_npz = np.load(R2_NPZ)

    settings = r2j.get("settings", {})
    parent_settings_ok = bool(
        r2j.get("classification") == R2_CLASS
        and settings.get("growth_observable") == "CLASS d_m"
        and settings.get("weyl_observable") == "CLASS phi+psi"
        and abs(float(settings.get("tau_H0", -1))-TAU) < 1e-15
        and int(settings.get("memory_order", -1)) == ORDER
        and abs(float(settings.get("tol_perturbations_integration", -1))-PRIMARY_TOL) < 1e-20
        and np.allclose(np.asarray(settings.get("anchors", []), float), np.asarray(ANCHORS), rtol=0, atol=5e-13)
    )
    parent_arrays_ok = True
    for kh in ANCHORS:
        t = tag(kh)
        for eta in REUSED_ETAS:
            e = etag(eta)
            parent_arrays_ok &= (f"D_{t}_e{e}" in parent_npz.files and f"W_{t}_e{e}" in parent_npz.files)

    g1 = bool(
        ancestor(PREDATA_LOCK) and ancestor(R2_POSTDATA_LOCK)
        and parent_settings_ok and parent_arrays_ok
        and r1c.get("classification") == R1C_CLASS
        and host.get("classification") == HOST_CLASS
        and r2.source_ok()
    )

    arrays = {"redshifts": Z}
    primary = {}; tight = {}; run_rows = []; basis_ok = bool(parent_arrays_ok)

    # Reuse exact R2 primary eta=0 and eta=0.01 arrays.
    for kh in ANCHORS:
        t = tag(kh)
        for eta in REUSED_ETAS:
            e = etag(eta)
            D = np.asarray(parent_npz[f"D_{t}_e{e}"], float).copy()
            W = np.asarray(parent_npz[f"W_{t}_e{e}"], float).copy()
            ok = bool(D.shape == Z.shape and W.shape == Z.shape and np.all(np.isfinite(D)) and np.all(np.isfinite(W)))
            primary[(kh,eta)] = {"D":D,"W":W,"finite":ok,"basis_pass":ok,"reused":True}
            arrays[f"P_D_{t}_e{e}"] = D; arrays[f"P_W_{t}_e{e}"] = W
            basis_ok &= ok
            run_rows.append({"k_h":kh,"eta":eta,"tol":PRIMARY_TOL,"reused":True,"basis_pass":ok})
            print(f"STABLE_AEST_GROWTH_WEYL_MEMORY_R2A_REUSE k_h={kh:.5f} eta={eta:.3g} basis={ok}", flush=True)

    # New primary leverage runs at eta=.02,.04.
    for kh in ANCHORS:
        for eta in NEW_PRIMARY_ETAS:
            try:
                v = run_case(kh, eta, PRIMARY_TOL); primary[(kh,eta)] = v
                t = tag(kh); e = etag(eta)
                arrays[f"P_D_{t}_e{e}"] = v["D"]; arrays[f"P_W_{t}_e{e}"] = v["W"]
                basis_ok &= bool(v["basis_pass"])
                run_rows.append({"k_h":kh,"eta":eta,"tol":PRIMARY_TOL,"reused":False,"basis_pass":v["basis_pass"],
                                 "bits":v["bits"],"target_pos":v["target_pos"],"h":v["h"],"k_key":v["k_key"],
                                 "min_k_h":v["min_k_h"],"max_k_h":v["max_k_h"],"min_k_count":v["min_k_count"]})
                print(f"STABLE_AEST_GROWTH_WEYL_MEMORY_R2A_PRIMARY k_h={kh:.5f} eta={eta:.3g} basis={v['basis_pass']}", flush=True)
            except Exception as ex:
                basis_ok = False
                run_rows.append({"k_h":kh,"eta":eta,"tol":PRIMARY_TOL,"reused":False,"basis_pass":False,"error":repr(ex)})
                print(f"STABLE_AEST_GROWTH_WEYL_MEMORY_R2A_PRIMARY_FAIL k_h={kh:.5f} eta={eta:.3g} error={ex!r}", flush=True)

    # Tight eta=0,.04 runs.
    for kh in ANCHORS:
        for eta in (0.0,0.04):
            try:
                v = run_case(kh, eta, TIGHT_TOL); tight[(kh,eta)] = v
                t = tag(kh); e = etag(eta)
                arrays[f"T_D_{t}_e{e}"] = v["D"]; arrays[f"T_W_{t}_e{e}"] = v["W"]
                basis_ok &= bool(v["basis_pass"])
                run_rows.append({"k_h":kh,"eta":eta,"tol":TIGHT_TOL,"reused":False,"basis_pass":v["basis_pass"],
                                 "bits":v["bits"],"target_pos":v["target_pos"],"h":v["h"],"k_key":v["k_key"],
                                 "min_k_h":v["min_k_h"],"max_k_h":v["max_k_h"],"min_k_count":v["min_k_count"]})
                print(f"STABLE_AEST_GROWTH_WEYL_MEMORY_R2A_TIGHT k_h={kh:.5f} eta={eta:.3g} basis={v['basis_pass']}", flush=True)
            except Exception as ex:
                basis_ok = False
                run_rows.append({"k_h":kh,"eta":eta,"tol":TIGHT_TOL,"reused":False,"basis_pass":False,"error":repr(ex)})
                print(f"STABLE_AEST_GROWTH_WEYL_MEMORY_R2A_TIGHT_FAIL k_h={kh:.5f} eta={eta:.3g} error={ex!r}", flush=True)

    # Denominator validity.
    if len(primary) == len(ANCHORS)*len(PRIMARY_ETAS) and len(tight) == len(ANCHORS)*2:
        for kh in ANCHORS:
            for dct, tol in ((primary,PRIMARY_TOL),(tight,TIGHT_TOL)):
                D0 = np.asarray(dct[(kh,0.0)]["D"],float); W0=np.asarray(dct[(kh,0.0)]["W"],float)
                basis_ok &= bool(np.all(np.abs(D0)>1e-300) and np.all(np.abs(W0)>1e-300))
    else:
        basis_ok = False

    linear_rows=[]; sep_rows=[]; floor_rows=[]; tol_rows=[]
    strict_linear=0; loose_linear_all=True
    resolved_hi=0; loose_hi_all=True
    floor_count=0
    tight_individual_all=True; tight_sep_count=0; tight_sep_finite=True

    if basis_ok:
        for kh in ANCHORS:
            G={}; L={}; R={}; P={}
            for eta in (0.01,0.02,0.04):
                G[eta],L[eta],R[eta],P[eta]=matched_tangents(primary[(kh,0.0)],primary[(kh,eta)],eta)
                t=tag(kh); e=etag(eta)
                for n,x in (("G",G[eta]),("L",L[eta]),("R",R[eta]),("SEP",P[eta])):
                    arrays[f"{n}_{t}_e{e}"]=x

            eG12=rel(G[0.01],G[0.02]); eG24=rel(G[0.02],G[0.04])
            eL12=rel(L[0.01],L[0.02]); eL24=rel(L[0.02],L[0.04])
            mx=max(eG12,eG24,eL12,eL24); strict=bool(mx<=0.05); loose=bool(mx<=0.10)
            strict_linear += int(strict); loose_linear_all &= loose
            linear_rows.append({"k_h":kh,"E_G_12":eG12,"E_G_24":eG24,"E_L_12":eL12,"E_L_24":eL24,"max_E":mx,"strict_pass":strict,"loose_pass":loose})
            print(f"STABLE_AEST_GROWTH_WEYL_MEMORY_R2A_LINEAR k_h={kh:.5f} maxE={mx:.3e} strict={strict}",flush=True)

            eR=rel(R[0.02],R[0.04]); qhi=float(np.linalg.norm(R[0.04])/max(float(np.linalg.norm(R[0.02]-R[0.04])),1e-300))
            strictR=bool(eR<=0.20 and qhi>=3.0); looseR=bool(eR<=0.35 and qhi>=1.0)
            resolved_hi += int(strictR); loose_hi_all &= looseR
            sep_rows.append({"k_h":kh,"E_R_hi":eR,"Q_hi":qhi,"strict_pass":strictR,"loose_pass":looseR,
                             "norm_R_001":float(np.linalg.norm(R[0.01])),"norm_R_002":float(np.linalg.norm(R[0.02])),"norm_R_004":float(np.linalg.norm(R[0.04]))})
            print(f"STABLE_AEST_GROWTH_WEYL_MEMORY_R2A_SEP k_h={kh:.5f} ER={eR:.3e} Q={qhi:.3e} strict={strictR}",flush=True)

            cp12=rel(P[0.01],P[0.02]); cp24=rel(P[0.02],P[0.04]); c12=cosine(P[0.01],P[0.02]); c24=cosine(P[0.02],P[0.04])
            floor_like=bool(max(cp12,cp24)<=0.20 and c12>=0.95 and c24>=0.95)
            floor_count += int(floor_like)
            floor_rows.append({"k_h":kh,"C_P_12":cp12,"C_P_24":cp24,"cos_P_12":c12,"cos_P_24":c24,"floor_like":floor_like})
            print(f"STABLE_AEST_GROWTH_WEYL_MEMORY_R2A_FLOOR k_h={kh:.5f} CP12={cp12:.3e} CP24={cp24:.3e} cos12={c12:.6f} cos24={c24:.6f} floor={floor_like}",flush=True)

            Gp,Lp,Rp,Pp = G[0.04],L[0.04],R[0.04],P[0.04]
            Gt,Lt,Rt,Pt = matched_tangents(tight[(kh,0.0)],tight[(kh,0.04)],0.04)
            t=tag(kh)
            arrays[f"TG_{t}_e0p040"]=Gt; arrays[f"TL_{t}_e0p040"]=Lt; arrays[f"TR_{t}_e0p040"]=Rt; arrays[f"TSEP_{t}_e0p040"]=Pt
            cG=rel(Gp,Gt); cL=rel(Lp,Lt); cR=rel(Rp,Rt); cosR=cosine(Rp,Rt)
            ind=bool(cG<=0.05 and cL<=0.05); sepfin=bool(np.all(np.isfinite(Rt)) and np.linalg.norm(Rt)>0)
            sepres=bool(sepfin and cR<=0.25 and cosR>=0.95)
            tight_individual_all &= ind; tight_sep_finite &= sepfin; tight_sep_count += int(sepres)
            tol_rows.append({"k_h":kh,"C_G_tol":cG,"C_L_tol":cL,"C_R_tol":cR,"cos_R_tol":cosR,
                             "individual_pass":ind,"separation_pass":sepres})
            print(f"STABLE_AEST_GROWTH_WEYL_MEMORY_R2A_TOL k_h={kh:.5f} CG={cG:.3e} CL={cL:.3e} CR={cR:.3e} cosR={cosR:.6f} sep={sepres}",flush=True)

    g2=bool(basis_ok)
    g3=bool(g2 and strict_linear>=2 and loose_linear_all)
    g4=bool(g2 and resolved_hi>=2 and loose_hi_all)
    g5=bool(g2 and tight_individual_all)
    g6=bool(g2 and tight_sep_finite and tight_sep_count>=2)
    d1=int(floor_count)

    gates={
        "R2A_G1_provenance_and_parent_lock":g1,
        "R2A_G2_transfer_basis_and_numerical_regularity":g2,
        "R2A_G3_extended_G_L_linearity":g3,
        "R2A_G4_high_leverage_separation_resolution":g4,
        "R2A_G5_tight_individual_response_reproducibility":g5,
        "R2A_G6_tight_separation_reproducibility":g6,
    }

    if not g1: classification=INCOMPLETE
    elif not g2: classification=TRANSFER_FAIL
    elif not g3: classification=NONLINEAR
    elif g4 and g5 and g6: classification=RESOLVED
    elif g5 and (not g4 or not g6) and d1>=2: classification=FLOOR
    else: classification=UNRESOLVED

    summary={
        "classification":classification,
        "new_run_count":int(sum(not bool(r.get("reused",False)) for r in run_rows)),
        "reused_run_count":int(sum(bool(r.get("reused",False)) for r in run_rows)),
        "linear_strict_pass_count":int(strict_linear),
        "high_leverage_resolved_count":int(resolved_hi),
        "floor_like_count":int(floor_count),
        "tight_separation_pass_count":int(tight_sep_count),
        "max_individual_linearity_error":float(max((r["max_E"] for r in linear_rows),default=np.nan)),
        "max_E_R_hi":float(max((r["E_R_hi"] for r in sep_rows),default=np.nan)),
        "min_Q_hi":float(min((r["Q_hi"] for r in sep_rows),default=np.nan)),
        "max_C_R_tol":float(max((r["C_R_tol"] for r in tol_rows),default=np.nan)),
    }

    out={
        "classification":classification,"diagnostic_complete":True,"predata_lock":PREDATA_LOCK,
        "r2_parent_classification":r2j.get("classification"),"r1c_parent_classification":r1c.get("classification"),
        "host_parent_classification":host.get("classification"),
        "settings":{"anchors":list(ANCHORS),"primary_etas":list(PRIMARY_ETAS),"tau_H0":TAU,"memory_order":ORDER,
                    "primary_tol":PRIMARY_TOL,"tight_tol":TIGHT_TOL,"redshifts":Z.tolist(),
                    "growth_observable":"CLASS d_m","weyl_observable":"CLASS phi+psi"},
        "gates":gates,"floor_diagnostic_count":d1,"summary":summary,"runs":run_rows,
        "individual_linearity":linear_rows,"high_leverage_separation":sep_rows,
        "floor_scaling":floor_rows,"tolerance_confirmation":tol_rows,
        "interpretation":{"historical_R2_reclassified":False,"MCMG_bridge_followup_licensed":classification==RESOLVED,
                          "growth_Weyl_separation_certified":classification==RESOLVED,
                          "differential_floor_supported":classification==FLOOR,
                          "common_mode_to_current_bound":classification==FLOOR,
                          "observational_claim_licensed":False,"new_physics_claim_licensed":False},
    }
    Path(args.json_out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    np.savez_compressed(args.npz_out,**arrays)
    print("STABLE_AEST_GROWTH_WEYL_MEMORY_R2A_GATES="+json.dumps(gates,sort_keys=True),flush=True)
    print("STABLE_AEST_GROWTH_WEYL_MEMORY_R2A_SUMMARY="+json.dumps(summary,sort_keys=True),flush=True)
    print("STABLE_AEST_GROWTH_WEYL_MEMORY_R2A_CLASSIFICATION="+classification,flush=True)
    return 0 if classification in (RESOLVED,FLOOR) else 1


if __name__ == "__main__":
    raise SystemExit(main())
