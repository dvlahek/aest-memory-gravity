#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import numpy as np

from fullj_weyl import stable_aest_ksz_r11a_response_before_integration_repair01 as r01
from fullj_weyl import stable_aest_ksz_r11a_pairwise_velocity_response as r11a

ROOT = Path(__file__).resolve().parents[1]

PREFIT_LOCK = "f7dfff4cb6c4fc43fdd99a9a5679d509afa01714"
R11A_POSTDATA_LOCK = "94efaf95b4582a177bd80dd566d5d2c26b4e212c"
R01_PREFIT_LOCK = "608851bff8d4fc8ab063cc338ec0cd102a9f74f8"
R01_IMPL_LOCK = "11f51614a5c5ddecdcb24e898011d0d47df2b7ea"
R01_RUNNER_LOCK = "d2c1b9d811cdc7344039a015210a675ec7361360"
R01_POSTDATA_LOCK = "43ce2d7cd772438efe34edabc25572c7b7516bee"
R01_JSON = ROOT / "results/stable_aest_ksz_r11a_response_before_integration_repair01.json"
R01_JSON_SHA256 = "4fc3612674ae5ae6b2093e9642a3984bf4c7a3dbcd72b6b9eba6d9e664caa239"
R01_CLASS = "STABLE_AEST_KSZ_R11A_REPAIR01_RESOLUTION_FAIL"

TAUS = r01.TAUS
ETAS = r01.ETAS
EPS_PRIMARY = r01.EPS_PRIMARY
EPS_CONTROL = r01.EPS_CONTROL
R_MPC_H = r01.R_MPC_H
Z = r01.Z
DEFAULT_NK = r01.DEFAULT_NK

RES_E_GATE = 0.01
RES_C_GATE = 0.999
TANGENT_E_GATE = 0.05
TANGENT_C_GATE = 0.995
LINEARITY_E_GATE = 0.10
LINEARITY_C_GATE = 0.99
NORM_GATE = 1e-12

CLS_PASS = "STABLE_AEST_KSZ_R11A_REPAIR02_DENSE_RESOLUTION_CERTIFIED"
CLS_PROV = "STABLE_AEST_KSZ_R11A_REPAIR02_PROVENANCE_FAIL"
CLS_SUPPORT = "STABLE_AEST_KSZ_R11A_REPAIR02_SUPPORT_FAIL"
CLS_RES = "STABLE_AEST_KSZ_R11A_REPAIR02_RESOLUTION_FAIL"
CLS_EPS = "STABLE_AEST_KSZ_R11A_REPAIR02_EPSILON_FAIL"
CLS_DENS = "STABLE_AEST_KSZ_R11A_REPAIR02_NATIVE_DENSITY_FAIL"
CLS_CROSS = "STABLE_AEST_KSZ_R11A_REPAIR02_CROSS_OPERATOR_FAIL"
CLS_LINEAR = "STABLE_AEST_KSZ_R11A_REPAIR02_LOCAL_LINEARITY_FAIL"
CLS_BG = "STABLE_AEST_KSZ_R11A_REPAIR02_BACKGROUND_FAIL"
CLS_SHIFT = "STABLE_AEST_KSZ_R11A_REPAIR02_PHYSICAL_SHIFT_RESOLUTION_FAIL"
CLS_RUN = "STABLE_AEST_KSZ_R11A_REPAIR02_RUN_FAIL"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ancestor(sha: str) -> bool:
    return subprocess.run(["git", "merge-base", "--is-ancestor", sha, "HEAD"], cwd=ROOT,
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0


def metric(a, b):
    return r01.metric(a, b)


def pass_metric(m, resolution=False):
    eg = RES_E_GATE if resolution else TANGENT_E_GATE
    cg = RES_C_GATE if resolution else TANGENT_C_GATE
    return bool(np.isfinite(m["E"]) and np.isfinite(m["C"]) and m["E"] <= eg and m["C"] >= cg
                and m["norm_a"] > NORM_GATE and m["norm_b"] > NORM_GATE)


def write(path: Path, obj: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workdir", default="results/stable_aest_desi_dr1_r9b2k_work")
    ap.add_argument("--json-out", default="results/stable_aest_ksz_r11a_dense_resolution_repair02.json")
    ap.add_argument("--npz-out", default="results/stable_aest_ksz_r11a_dense_resolution_repair02.npz")
    args = ap.parse_args()
    work = Path(args.workdir); out = Path(args.json_out)
    print("STABLE_AEST_KSZ_R11A_REPAIR02_START", flush=True)

    prov = {"prefit_lock": PREFIT_LOCK, "repair01_json_sha256_expected": R01_JSON_SHA256}
    try:
        locks = (PREFIT_LOCK, R11A_POSTDATA_LOCK, R01_PREFIT_LOCK, R01_IMPL_LOCK, R01_RUNNER_LOCK, R01_POSTDATA_LOCK)
        prov["ancestor_locks"] = {x: ancestor(x) for x in locks}
        old = json.loads(R01_JSON.read_text())
        prov["repair01_json_sha256"] = sha256(R01_JSON)
        prov["repair01_classification"] = old.get("classification")
        og = old.get("gates", {})
        g1 = bool(all(prov["ancestor_locks"].values())
                  and prov["repair01_json_sha256"] == R01_JSON_SHA256
                  and old.get("classification") == R01_CLASS
                  and old.get("diagnostic_complete") is True
                  and og.get("R11A_R01_G1_provenance_checkpoints") is True
                  and og.get("R11A_R01_G2_support_baseline") is True
                  and og.get("R11A_R01_G3_dense_resolution") is False
                  and og.get("R11A_R01_G4_epsilon_consistency") is True
                  and og.get("R11A_R01_G5_native_density_convergence") is True
                  and og.get("R11A_R01_G6_cross_operator") is True
                  and og.get("R11A_R01_G7_local_eta005_linearity") is True
                  and og.get("R11A_R01_G8_background_prefactor_audit") is True)
    except Exception as exc:
        prov["error"] = repr(exc); g1 = False

    cases = {}; checkpoints = []
    if g1:
        try:
            specs = [("D1", 10.0, eta) for eta in ETAS] + [("D2", tau, eta) for tau in TAUS for eta in ETAS]
            for tier, tau, eta in specs:
                case = r11a._load_checkpoint(work, tier, tau, eta)
                cases[(tier, float(tau), float(eta))] = case
                nk = [len(row["state"]["kh"]) for row in case["rows"]]
                checkpoints.append({"tier": tier, "tau_H0": tau, "eta": eta,
                                    "n_k_min": int(min(nk)), "n_k_max": int(max(nk))})
        except Exception as exc:
            prov["checkpoint_error"] = repr(exc); g1 = False

    refinement = []
    if g1:
        for iz, z in enumerate(Z):
            n1 = len(cases[("D1", 10.0, 0.0)]["rows"][iz]["state"]["kh"])
            n2 = len(cases[("D2", 10.0, 0.0)]["rows"][iz]["state"]["kh"])
            ok = bool(n2 > n1 > DEFAULT_NK); g1 &= ok
            refinement.append({"z": float(z), "n_default": DEFAULT_NK, "n_D1": int(n1), "n_D2": int(n2), "pass": ok})

    if not g1:
        result = {"classification": CLS_PROV, "diagnostic_complete": False, "science_evaluated": False,
                  "gates": {"R11A_R02_G1_provenance_checkpoints": False}, "provenance": prov}
        write(out, result); print("STABLE_AEST_KSZ_R11A_REPAIR02_CLASSIFICATION=" + CLS_PROV, flush=True); return 3
    print(f"STABLE_AEST_KSZ_R11A_REPAIR02_CHECKPOINT_PASS count={len(checkpoints)}", flush=True)

    supports = []; support_meta = []; g2 = True
    try:
        for iz, z in enumerate(Z):
            lows=[]; highs=[]
            for case in cases.values():
                kh=np.asarray(case["rows"][iz]["state"]["kh"], float)
                lows.append(float(kh[0])); highs.append(float(kh[-1]))
            lo=max(lows); hi=min(highs)
            ok=bool(np.isfinite(lo) and np.isfinite(hi) and 0 < lo < hi and lo <= 2e-4 and hi >= 2.0)
            g2 &= ok; supports.append((lo,hi)); support_meta.append({"z":float(z),"kmin_h_Mpc":lo,"kmax_h_Mpc":hi,"pass":ok})
        baseline_meta=[]
        for tau in TAUS:
            for mode in ("linear","pchip"):
                vv=[]
                for iz in range(len(Z)):
                    b=r01._dense_baseline(cases[("D2",tau,0.0)]["rows"][iz],supports[iz],mode,32768)
                    vv.append(b["v"])
                v=np.stack(vv); ok=bool(np.all(np.isfinite(v)) and np.all(np.abs(v)>1e-6)); g2 &= ok
                baseline_meta.append({"tau_H0":tau,"operator":mode,"pass":ok,
                                      "v_min_kms":float(v.min()),"v_max_kms":float(v.max())})
    except Exception as exc:
        support_meta.append({"error":repr(exc)}); baseline_meta=[]; g2=False

    cache={}; bg_values=[]
    try:
        for tau in TAUS:
            for eps in (EPS_PRIMARY, EPS_CONTROL):
                for n in (16384,32768,65536):
                    T,bg=r01._stack_tangent(cases,"D2",tau,eps,supports,"linear",n)
                    cache[("D2",tau,eps,"linear",n)]=T; bg_values.extend(bg)
                T,bg=r01._stack_tangent(cases,"D2",tau,eps,supports,"pchip",32768)
                cache[("D2",tau,eps,"pchip",32768)]=T; bg_values.extend(bg)
        for eps in (EPS_PRIMARY, EPS_CONTROL):
            for mode in ("linear","pchip"):
                T,bg=r01._stack_tangent(cases,"D1",10.0,eps,supports,mode,32768)
                cache[("D1",10.0,eps,mode,32768)]=T; bg_values.extend(bg)
    except Exception as exc:
        result={"classification":CLS_RUN,"diagnostic_complete":False,"science_evaluated":False,
                "gates":{"R11A_R02_G1_provenance_checkpoints":True,"R11A_R02_G2_support_baseline":bool(g2)},
                "error":repr(exc),"provenance":prov,"support":support_meta}
        write(out,result); print(f"STABLE_AEST_KSZ_R11A_REPAIR02_RUN_FAIL error={exc!r}",flush=True); return 2

    res_metrics={}; g3=True
    for tau in TAUS:
        res_metrics[str(tau)]={}
        for eps in (EPS_PRIMARY,EPS_CONTROL):
            m1=metric(cache[("D2",tau,eps,"linear",16384)],cache[("D2",tau,eps,"linear",32768)])
            m2=metric(cache[("D2",tau,eps,"linear",32768)],cache[("D2",tau,eps,"linear",65536)])
            res_metrics[str(tau)][str(eps)]={"16384_vs_32768":m1,"32768_vs_65536":m2}
            g3 &= pass_metric(m1,True) and pass_metric(m2,True)

    eps_metrics={}; g4=True
    for tau in TAUS:
        eps_metrics[str(tau)]={}
        for mode in ("linear","pchip"):
            m=metric(cache[("D2",tau,EPS_PRIMARY,mode,32768)],cache[("D2",tau,EPS_CONTROL,mode,32768)])
            eps_metrics[str(tau)][mode]=m; g4 &= pass_metric(m)

    density_metrics={}; g5=True
    for mode in ("linear","pchip"):
        density_metrics[mode]={}
        for eps in (EPS_PRIMARY,EPS_CONTROL):
            m=metric(cache[("D1",10.0,eps,mode,32768)],cache[("D2",10.0,eps,mode,32768)])
            density_metrics[mode][str(eps)]=m; g5 &= pass_metric(m)

    cross_metrics={}; g6=True
    for tau in TAUS:
        cross_metrics[str(tau)]={}
        for eps in (EPS_PRIMARY,EPS_CONTROL):
            m=metric(cache[("D2",tau,eps,"linear",32768)],cache[("D2",tau,eps,"pchip",32768)])
            cross_metrics[str(tau)][str(eps)]=m; g6 &= pass_metric(m)

    direct32768={}; direct65536={}; linearity={}; shift_resolution={}; g7=True; g9=True
    for tau in TAUS:
        d32=r01._stack_direct_shift(cases,"D2",tau,supports,"linear",32768)
        d65=r01._stack_direct_shift(cases,"D2",tau,supports,"linear",65536)
        direct32768[str(tau)]=d32; direct65536[str(tau)]=d65
        pred=0.05*cache[("D2",tau,EPS_PRIMARY,"linear",32768)]
        ml=metric(d32,pred)
        ok=bool(np.isfinite(ml["E"]) and np.isfinite(ml["C"]) and ml["E"]<=LINEARITY_E_GATE and ml["C"]>=LINEARITY_C_GATE)
        linearity[str(tau)]={**ml,"pass":ok}; g7 &= ok
        ms=metric(d32,d65); shift_resolution[str(tau)]={**ms,"pass":pass_metric(ms,True)}; g9 &= pass_metric(ms,True)

    bg=np.asarray(bg_values,float); g8=bool(bg.size and np.all(np.isfinite(bg)))
    bg_max=float(np.max(np.abs(bg))) if bg.size else float("nan")

    gates={
        "R11A_R02_G1_provenance_checkpoints":True,
        "R11A_R02_G2_support_baseline":bool(g2),
        "R11A_R02_G3_asymptotic_dense_resolution":bool(g3),
        "R11A_R02_G4_epsilon_consistency":bool(g4),
        "R11A_R02_G5_native_density_convergence":bool(g5),
        "R11A_R02_G6_cross_operator":bool(g6),
        "R11A_R02_G7_local_eta005_linearity":bool(g7),
        "R11A_R02_G8_background_audit":bool(g8),
        "R11A_R02_G9_physical_shift_resolution":bool(g9),
    }
    if not g2: classification=CLS_SUPPORT
    elif not g3: classification=CLS_RES
    elif not g4: classification=CLS_EPS
    elif not g5: classification=CLS_DENS
    elif not g6: classification=CLS_CROSS
    elif not g7: classification=CLS_LINEAR
    elif not g8: classification=CLS_BG
    elif not g9: classification=CLS_SHIFT
    else: classification=CLS_PASS

    physical={}; tau_coherence={}
    if classification==CLS_PASS:
        tref=cache[("D2",10.0,EPS_PRIMARY,"linear",32768)]
        for tau in TAUS:
            T=cache[("D2",tau,EPS_PRIMARY,"linear",32768)]
            ds=direct32768[str(tau)]; dv=[]
            for iz in range(len(Z)):
                b0=r01._dense_baseline(cases[("D2",tau,0.0)]["rows"][iz],supports[iz],"linear",32768)
                bp=r01._dense_baseline(cases[("D2",tau,0.05)]["rows"][iz],supports[iz],"linear",32768)
                dv.append(bp["v"]-b0["v"])
            dv=np.stack(dv); idx=np.unravel_index(int(np.argmax(np.abs(ds))),ds.shape)
            physical[str(tau)]={
                "max_abs_T_per_eta":float(np.max(np.abs(T))),
                "rms_T_per_eta":float(np.sqrt(np.mean(T*T))),
                "max_abs_fractional_shift_eta005":float(np.max(np.abs(ds))),
                "rms_fractional_shift_eta005":float(np.sqrt(np.mean(ds*ds))),
                "max_abs_velocity_shift_kms_eta005":float(np.max(np.abs(dv))),
                "largest_fractional_shift":{"z":float(Z[idx[0]]),"r_Mpc_h":float(R_MPC_H[idx[1]]),
                                              "fractional_shift":float(ds[idx]),"T_per_eta":float(T[idx]),
                                              "delta_v12_kms":float(dv[idx])},
                "linearity":linearity[str(tau)],"shift_resolution_32768_vs_65536":shift_resolution[str(tau)],
            }
            tau_coherence[str(tau)]=metric(tref,T)

    result={"classification":classification,"diagnostic_complete":True,"science_evaluated":classification==CLS_PASS,
            "gates":gates,"provenance":prov,"checkpoints":checkpoints,"native_refinement":refinement,
            "support":{"common_per_redshift":support_meta,"baseline":baseline_meta},
            "robustness":{"resolution":res_metrics,"epsilon":eps_metrics,"density":density_metrics,
                          "cross_operator":cross_metrics,"eta005_linearity":linearity,
                          "eta005_shift_resolution":shift_resolution,"max_abs_DlnA_per_eta":bg_max},
            "physical_response":physical,"tau_coherence":tau_coherence,
            "settings":{"primary_dense_nodes":32768,"resolution_nodes":[16384,32768,65536],
                        "resolution_E_gate":RES_E_GATE,"resolution_C_gate":RES_C_GATE,
                        "tau_H0":list(TAUS),"eta_values":list(ETAS),"epsilon_primary":EPS_PRIMARY,
                        "epsilon_control":EPS_CONTROL,"r_Mpc_h":R_MPC_H.tolist(),"no_extrapolation":True,
                        "no_smoothing":True,"no_clipping":True,"response_before_integration":True},
            "claim_scope":{"theory_only_pairwise_velocity_response":classification==CLS_PASS,"ksz_detection":False,
                           "ksz_likelihood":False,"eta_bound":False,"tau_bound":False,"optical_depth_inference":False,
                           "galaxy_halo_prediction":False,"nonlinear_small_scale_claim":False}}
    write(out,result)
    arrays={"z":Z,"r_Mpc_h":R_MPC_H}
    for tau in TAUS:
        arrays[f"T_tau{tau:g}"]=cache[("D2",tau,EPS_PRIMARY,"linear",32768)]
        arrays[f"direct_shift_eta005_tau{tau:g}"]=direct32768[str(tau)]
    np.savez_compressed(args.npz_out,**arrays)

    print("STABLE_AEST_KSZ_R11A_REPAIR02_GATES="+json.dumps(gates,sort_keys=True),flush=True)
    print("STABLE_AEST_KSZ_R11A_REPAIR02_ROBUSTNESS="+json.dumps({"resolution":res_metrics,"epsilon":eps_metrics,"density":density_metrics,"cross_operator":cross_metrics,"linearity":linearity,"shift_resolution":shift_resolution,"max_abs_DlnA_per_eta":bg_max},sort_keys=True),flush=True)
    if classification==CLS_PASS:
        print("STABLE_AEST_KSZ_R11A_REPAIR02_PHYSICAL="+json.dumps(physical,sort_keys=True),flush=True)
        print("STABLE_AEST_KSZ_R11A_REPAIR02_TAU="+json.dumps(tau_coherence,sort_keys=True),flush=True)
    print("STABLE_AEST_KSZ_R11A_REPAIR02_CLASSIFICATION="+classification,flush=True)
    return 0 if classification==CLS_PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
