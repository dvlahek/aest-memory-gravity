#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import numpy as np
from scipy.integrate import simpson
from scipy.interpolate import PchipInterpolator
from scipy.special import spherical_jn

from fullj_weyl import stable_aest_ksz_r11a_pairwise_velocity_response as r11a
from fullj_weyl import stable_aest_desi_dr1_r9b2k_native_k_density_convergence as k2

ROOT = Path(__file__).resolve().parents[1]

PREFIT_LOCK = "608851bff8d4fc8ab063cc338ec0cd102a9f74f8"
R11A_PREFIT_LOCK = "a34c4d13738383c670222472b3af8ab4e1802fdf"
R11A_IMPL_LOCK = "44a65aea8f671a0af7534447c31f415a6c9d314c"
R11A_RUNNER_LOCK = "8868dc344b83f69f7429b507e750450c724ddd63"
R11A_POSTDATA_LOCK = "94efaf95b4582a177bd80dd566d5d2c26b4e212c"
R9B2K_POSTDATA_LOCK = "dd3981b2fd838fb24a997af77f913c3d5dd8d07b"
REPAIR02_POSTDATA_LOCK = "d3fd6191d55f4e74aa8666f842dae64bd8aee09b"
R10A_POSTDATA_LOCK = "b7da648f1810ea0c047b6e511e3f87211e830329"

R11A_JSON = ROOT / "results/stable_aest_ksz_r11a_pairwise_velocity_response.json"
R11A_JSON_SHA256 = "a868dbbb6b5b08bf54139abf9d3a288d52bee501f23cc4b61f9422f9fb2d98ab"
R11A_CLASS = "STABLE_AEST_KSZ_R11A_NATIVE_DENSITY_FAIL"

TAUS = (10.0, 5.0, 2.5, 1.25)
ETAS = (0.0, 0.025, -0.025, 0.05, -0.05)
EPS_PRIMARY = 0.025
EPS_CONTROL = 0.05
R_MPC_H = np.arange(40.0, 201.0, 10.0)
Z = np.asarray(k2.ZEFF, float)
C_KMS = 299792.458
DEFAULT_NK = 108

RES_E_GATE = 0.01
RES_C_GATE = 0.999
TANGENT_E_GATE = 0.05
TANGENT_C_GATE = 0.995
LINEARITY_E_GATE = 0.10
LINEARITY_C_GATE = 0.99
NORM_GATE = 1.0e-12

CLS_PASS = "STABLE_AEST_KSZ_R11A_REPAIR01_RESPONSE_BEFORE_INTEGRATION_CERTIFIED"
CLS_PROV = "STABLE_AEST_KSZ_R11A_REPAIR01_PROVENANCE_FAIL"
CLS_SUPPORT = "STABLE_AEST_KSZ_R11A_REPAIR01_SUPPORT_BASELINE_FAIL"
CLS_RES = "STABLE_AEST_KSZ_R11A_REPAIR01_RESOLUTION_FAIL"
CLS_EPS = "STABLE_AEST_KSZ_R11A_REPAIR01_EPSILON_FAIL"
CLS_DENS = "STABLE_AEST_KSZ_R11A_REPAIR01_NATIVE_DENSITY_FAIL"
CLS_CROSS = "STABLE_AEST_KSZ_R11A_REPAIR01_CROSS_OPERATOR_FAIL"
CLS_LINEAR = "STABLE_AEST_KSZ_R11A_REPAIR01_LOCAL_LINEARITY_FAIL"
CLS_BG = "STABLE_AEST_KSZ_R11A_REPAIR01_BACKGROUND_AUDIT_FAIL"
CLS_RUN = "STABLE_AEST_KSZ_R11A_REPAIR01_RUN_FAIL"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"], cwd=ROOT,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    ).returncode == 0


def metric(a, b) -> dict:
    aa = np.asarray(a, float).ravel(); bb = np.asarray(b, float).ravel()
    na = float(np.linalg.norm(aa)); nb = float(np.linalg.norm(bb))
    E = float(np.linalg.norm(aa - bb) / max(na, nb, 1e-300))
    C = float(np.dot(aa, bb) / max(na * nb, 1e-300))
    return {"E": E, "C": C, "norm_a": na, "norm_b": nb}


def response_pass(m: dict, resolution: bool = False) -> bool:
    eg = RES_E_GATE if resolution else TANGENT_E_GATE
    cg = RES_C_GATE if resolution else TANGENT_C_GATE
    return bool(
        np.isfinite(m["E"]) and np.isfinite(m["C"])
        and m["E"] <= eg and m["C"] >= cg
        and m["norm_a"] > NORM_GATE and m["norm_b"] > NORM_GATE
    )


def _write(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")


def _pdf(row: dict) -> np.ndarray:
    st = row["state"]
    pdd = np.asarray(st["pdd"], float)
    ptt = np.asarray(st["ptt"], float)
    dcb = np.asarray(st["dcb"], float)
    tcb = np.asarray(st["tcb"], float)
    Hconf = float(st["Hconf"])
    if not np.isfinite(Hconf) or Hconf == 0.0:
        raise RuntimeError("invalid Hconf")
    vcb = -tcb / Hconf
    out = np.sign(dcb * vcb) * np.sqrt(pdd * ptt)
    if np.any(~np.isfinite(out)):
        raise RuntimeError("non-finite P_df")
    return out


def _A(row: dict) -> float:
    bg = row["background"]
    h = float(bg["h"]); H = float(bg["Hubble_Mpc_inv"])
    if not np.isfinite(h) or h <= 0.0 or not np.isfinite(H) or H <= 0.0:
        raise RuntimeError("invalid background")
    return C_KMS * H / h


def _interp(logk: np.ndarray, y: np.ndarray, grid: np.ndarray, mode: str, positive: bool) -> np.ndarray:
    logk = np.asarray(logk, float); y = np.asarray(y, float); grid = np.asarray(grid, float)
    if positive:
        if np.any(~np.isfinite(y)) or np.any(y <= 0.0):
            raise RuntimeError("positive interpolation received non-positive input")
        src = np.log(y)
        if mode == "linear": val = np.interp(grid, logk, src)
        elif mode == "pchip": val = PchipInterpolator(logk, src, extrapolate=False)(grid)
        else: raise ValueError(mode)
        out = np.exp(val)
    else:
        if np.any(~np.isfinite(y)):
            raise RuntimeError("signed interpolation received non-finite input")
        if mode == "linear": out = np.interp(grid, logk, y)
        elif mode == "pchip": out = PchipInterpolator(logk, y, extrapolate=False)(grid)
        else: raise ValueError(mode)
    out = np.asarray(out, float)
    if np.any(~np.isfinite(out)):
        raise RuntimeError("non-finite dense interpolation")
    return out


def _same_grid(*rows: dict) -> tuple[np.ndarray, bool]:
    ks = [np.asarray(r["state"]["kh"], float) for r in rows]
    ref = ks[0]
    ok = all(k.shape == ref.shape and np.allclose(k, ref, rtol=0.0, atol=1e-14) for k in ks[1:])
    return ref, bool(ok)


def _dense_baseline(row: dict, support: tuple[float, float], mode: str, n: int) -> dict:
    st = row["state"]
    kh = np.asarray(st["kh"], float); pdd = np.asarray(st["pdd"], float); pdf = _pdf(row)
    lo, hi = map(float, support)
    grid = np.linspace(np.log(lo), np.log(hi), int(n)); kg = np.exp(grid)
    pddg = _interp(np.log(kh), pdd, grid, mode, True)
    pdfg = _interp(np.log(kh), pdf, grid, mode, False)
    z = float(row["z"]); a = 1.0 / (1.0 + z); A0 = _A(row)
    xi = np.empty(R_MPC_H.size, float); Ii = np.empty_like(xi)
    for ir, r in enumerate(R_MPC_H):
        x = kg * float(r)
        xi[ir] = float(simpson(kg**3 * pddg * spherical_jn(0, x) / (2.0*np.pi**2), x=grid))
        Ii[ir] = float(simpson(kg**2 * pdfg * spherical_jn(1, x) / (2.0*np.pi**2), x=grid))
    den = 1.0 + xi
    if np.any(~np.isfinite(xi)) or np.any(~np.isfinite(Ii)) or np.any(den <= 0.0) or np.any(np.abs(Ii) <= 1e-12):
        raise RuntimeError("invalid dense baseline integrals")
    v = -2.0 * a * A0 * Ii / den
    if np.any(~np.isfinite(v)) or np.any(np.abs(v) <= 1e-6):
        raise RuntimeError("invalid dense baseline velocity")
    return {"xi": xi, "I": Ii, "v": v, "A": A0}


def _dense_tangent(row0: dict, rowp: dict, rowm: dict, eps: float,
                   support: tuple[float, float], mode: str, n: int) -> dict:
    kh, same = _same_grid(row0, rowp, rowm)
    if not same:
        raise RuntimeError("eta stencil native k grids differ")
    p0 = np.asarray(row0["state"]["pdd"], float)
    pp = np.asarray(rowp["state"]["pdd"], float)
    pm = np.asarray(rowm["state"]["pdd"], float)
    f0 = _pdf(row0); fp = _pdf(rowp); fm = _pdf(rowm)
    Dp = (pp - pm) / (2.0 * float(eps))
    Df = (fp - fm) / (2.0 * float(eps))

    lo, hi = map(float, support)
    grid = np.linspace(np.log(lo), np.log(hi), int(n)); kg = np.exp(grid); lk = np.log(kh)
    p0g = _interp(lk, p0, grid, mode, True)
    f0g = _interp(lk, f0, grid, mode, False)
    Dpg = _interp(lk, Dp, grid, mode, False)
    Dfg = _interp(lk, Df, grid, mode, False)

    A0 = _A(row0); Ap = _A(rowp); Am = _A(rowm)
    DlnA = (Ap - Am) / (2.0 * float(eps) * A0)
    if not np.isfinite(DlnA):
        raise RuntimeError("non-finite background response")

    xi0 = np.empty(R_MPC_H.size, float); I0 = np.empty_like(xi0)
    Dxi = np.empty_like(xi0); DI = np.empty_like(xi0)
    for ir, r in enumerate(R_MPC_H):
        x = kg * float(r); j0 = spherical_jn(0, x); j1 = spherical_jn(1, x)
        xi0[ir] = float(simpson(kg**3 * p0g * j0 / (2.0*np.pi**2), x=grid))
        I0[ir] = float(simpson(kg**2 * f0g * j1 / (2.0*np.pi**2), x=grid))
        Dxi[ir] = float(simpson(kg**3 * Dpg * j0 / (2.0*np.pi**2), x=grid))
        DI[ir] = float(simpson(kg**2 * Dfg * j1 / (2.0*np.pi**2), x=grid))
    if np.any(~np.isfinite(xi0)) or np.any(~np.isfinite(I0)) or np.any(~np.isfinite(Dxi)) or np.any(~np.isfinite(DI)):
        raise RuntimeError("non-finite response integrals")
    if np.any(1.0 + xi0 <= 0.0) or np.any(np.abs(I0) <= 1e-12):
        raise RuntimeError("invalid response denominator")
    T = DlnA + DI / I0 - Dxi / (1.0 + xi0)
    if np.any(~np.isfinite(T)):
        raise RuntimeError("non-finite fractional tangent")
    return {"T": T, "DlnA": float(DlnA), "Dxi": Dxi, "DI": DI, "xi0": xi0, "I0": I0}


def _case_rows(case: dict) -> list[dict]:
    return list(case["rows"])


def _stack_tangent(cases: dict, tier: str, tau: float, eps: float, supports,
                   mode: str, n: int) -> tuple[np.ndarray, list[float]]:
    zc = cases[(tier, float(tau), 0.0)]
    pp = cases[(tier, float(tau), +float(eps))]
    mm = cases[(tier, float(tau), -float(eps))]
    arr = []; bg = []
    for iz in range(len(Z)):
        q = _dense_tangent(zc["rows"][iz], pp["rows"][iz], mm["rows"][iz], eps, supports[iz], mode, n)
        arr.append(q["T"]); bg.append(q["DlnA"])
    return np.stack(arr, axis=0), bg


def _stack_direct_shift(cases: dict, tier: str, tau: float, supports, mode: str, n: int) -> np.ndarray:
    zc = cases[(tier, float(tau), 0.0)]; pp = cases[(tier, float(tau), 0.05)]
    out = []
    for iz in range(len(Z)):
        b0 = _dense_baseline(zc["rows"][iz], supports[iz], mode, n)
        bp = _dense_baseline(pp["rows"][iz], supports[iz], mode, n)
        out.append((bp["v"] - b0["v"]) / b0["v"])
    return np.stack(out, axis=0)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workdir", default="results/stable_aest_desi_dr1_r9b2k_work")
    ap.add_argument("--json-out", default="results/stable_aest_ksz_r11a_response_before_integration_repair01.json")
    ap.add_argument("--npz-out", default="results/stable_aest_ksz_r11a_response_before_integration_repair01.npz")
    args = ap.parse_args()
    out = Path(args.json_out); work = Path(args.workdir)
    print("STABLE_AEST_KSZ_R11A_REPAIR01_START", flush=True)

    prov = {"prefit_lock": PREFIT_LOCK, "r11a_postdata_lock": R11A_POSTDATA_LOCK, "r11a_json_sha256_expected": R11A_JSON_SHA256}
    try:
        locks = (PREFIT_LOCK, R11A_PREFIT_LOCK, R11A_IMPL_LOCK, R11A_RUNNER_LOCK, R11A_POSTDATA_LOCK,
                 R9B2K_POSTDATA_LOCK, REPAIR02_POSTDATA_LOCK, R10A_POSTDATA_LOCK)
        prov["ancestor_locks"] = {x: ancestor(x) for x in locks}
        old = json.loads(R11A_JSON.read_text())
        prov["r11a_json_sha256"] = sha256(R11A_JSON)
        prov["r11a_classification"] = old.get("classification")
        og = old.get("gates", {})
        g1 = bool(
            all(prov["ancestor_locks"].values())
            and prov["r11a_json_sha256"] == R11A_JSON_SHA256
            and old.get("classification") == R11A_CLASS
            and old.get("diagnostic_complete") is True
            and og.get("R11A_G1_provenance_checkpoints") is True
            and og.get("R11A_G2_baseline_physicality_tau_invariance") is True
            and og.get("R11A_G3_baseline_quadrature") is True
            and og.get("R11A_G4_epsilon_consistency") is True
            and og.get("R11A_G5_native_density_convergence") is False
            and og.get("R11A_G6_cross_quadrature_tangent") is False
            and og.get("R11A_G7_local_eta005_linearity") is True
        )
    except Exception as exc:
        prov["error"] = repr(exc); g1 = False

    cases = {}; checkpoints = []
    if g1:
        try:
            specs = [("D1", 10.0, eta) for eta in ETAS] + [("D2", tau, eta) for tau in TAUS for eta in ETAS]
            for tier, tau, eta in specs:
                case = r11a._load_checkpoint(work, tier, tau, eta)
                cases[(tier, float(tau), float(eta))] = case
                nk = [len(r["state"]["kh"]) for r in case["rows"]]
                checkpoints.append({"tier": tier, "tau_H0": tau, "eta": eta, "n_k_min": int(min(nk)), "n_k_max": int(max(nk))})
        except Exception as exc:
            prov["checkpoint_error"] = repr(exc); g1 = False

    refinement = []
    if g1:
        for iz, z in enumerate(Z):
            n1 = len(cases[("D1",10.0,0.0)]["rows"][iz]["state"]["kh"])
            n2 = len(cases[("D2",10.0,0.0)]["rows"][iz]["state"]["kh"])
            ok = bool(n2 > n1 > DEFAULT_NK); g1 &= ok
            refinement.append({"z": float(z), "n_default": DEFAULT_NK, "n_D1": int(n1), "n_D2": int(n2), "pass": ok})

    if not g1:
        result = {"classification": CLS_PROV, "diagnostic_complete": False, "science_evaluated": False,
                  "gates": {"R11A_R01_G1_provenance_checkpoints": False}, "provenance": prov, "native_refinement": refinement}
        _write(out, result); print("STABLE_AEST_KSZ_R11A_REPAIR01_CLASSIFICATION="+CLS_PROV, flush=True); return 3
    print(f"STABLE_AEST_KSZ_R11A_REPAIR01_CHECKPOINT_PASS count={len(checkpoints)}", flush=True)

    # One common bounded support per redshift across all 25 cases.
    supports = []; support_meta = []; g2 = True
    try:
        for iz, z in enumerate(Z):
            lows=[]; highs=[]
            for case in cases.values():
                kh=np.asarray(case["rows"][iz]["state"]["kh"],float)
                lows.append(float(kh[0])); highs.append(float(kh[-1]))
            lo=max(lows); hi=min(highs)
            ok=bool(np.isfinite(lo) and np.isfinite(hi) and 0.0<lo<hi and lo<=2e-4 and hi>=2.0)
            g2 &= ok; supports.append((lo,hi)); support_meta.append({"z":float(z),"kmin_h_Mpc":lo,"kmax_h_Mpc":hi,"pass":ok})
        # Dense baseline physicality for both operators at all D2 tau values.
        baseline_meta=[]
        for tau in TAUS:
            for mode in ("linear","pchip"):
                vv=[]
                for iz in range(len(Z)):
                    b=_dense_baseline(cases[("D2",tau,0.0)]["rows"][iz],supports[iz],mode,8192)
                    vv.append(b["v"])
                v=np.stack(vv,axis=0)
                ok=bool(np.all(np.isfinite(v)) and np.all(np.abs(v)>1e-6)); g2 &= ok
                baseline_meta.append({"tau_H0":tau,"operator":mode,"pass":ok,"v_min_kms":float(v.min()),"v_max_kms":float(v.max())})
    except Exception as exc:
        support_meta.append({"error":repr(exc)}); baseline_meta=[]; g2=False

    # Build all tangents needed by frozen gates.
    tangent_cache={}; bg_values=[]
    try:
        for tau in TAUS:
            for eps in (EPS_PRIMARY,EPS_CONTROL):
                for n in (4096,8192,16384):
                    T,bg=_stack_tangent(cases,"D2",tau,eps,supports,"linear",n)
                    tangent_cache[("D2",tau,eps,"linear",n)]=T; bg_values.extend(bg)
                T,bg=_stack_tangent(cases,"D2",tau,eps,supports,"pchip",8192)
                tangent_cache[("D2",tau,eps,"pchip",8192)]=T; bg_values.extend(bg)
        for eps in (EPS_PRIMARY,EPS_CONTROL):
            for mode in ("linear","pchip"):
                T,bg=_stack_tangent(cases,"D1",10.0,eps,supports,mode,8192)
                tangent_cache[("D1",10.0,eps,mode,8192)]=T; bg_values.extend(bg)
    except Exception as exc:
        result={"classification":CLS_RUN,"diagnostic_complete":False,"science_evaluated":False,
                "gates":{"R11A_R01_G1_provenance_checkpoints":True,"R11A_R01_G2_support_baseline":bool(g2)},
                "error":repr(exc),"support":support_meta,"provenance":prov}
        _write(out,result); print(f"STABLE_AEST_KSZ_R11A_REPAIR01_RUN_FAIL error={exc!r}",flush=True); return 2

    # G3: dense resolution.
    res_metrics={}; g3=True
    for tau in TAUS:
        res_metrics[str(tau)]={}
        for eps in (EPS_PRIMARY,EPS_CONTROL):
            a=tangent_cache[("D2",tau,eps,"linear",4096)]
            b=tangent_cache[("D2",tau,eps,"linear",8192)]
            c=tangent_cache[("D2",tau,eps,"linear",16384)]
            m1=metric(a,b); m2=metric(b,c)
            res_metrics[str(tau)][str(eps)]={"4096_vs_8192":m1,"8192_vs_16384":m2}
            g3 &= response_pass(m1,True) and response_pass(m2,True)

    # G4: epsilon consistency.
    eps_metrics={}; g4=True
    for tau in TAUS:
        eps_metrics[str(tau)]={}
        for mode in ("linear","pchip"):
            m=metric(tangent_cache[("D2",tau,EPS_PRIMARY,mode,8192)],tangent_cache[("D2",tau,EPS_CONTROL,mode,8192)])
            eps_metrics[str(tau)][mode]=m; g4 &= response_pass(m,False)

    # G5: D1 -> D2 density convergence at tau10.
    density_metrics={}; g5=True
    for mode in ("linear","pchip"):
        density_metrics[mode]={}
        for eps in (EPS_PRIMARY,EPS_CONTROL):
            m=metric(tangent_cache[("D1",10.0,eps,mode,8192)],tangent_cache[("D2",10.0,eps,mode,8192)])
            density_metrics[mode][str(eps)]=m; g5 &= response_pass(m,False)

    # G6: linear vs PCHIP at D2.
    cross_metrics={}; g6=True
    for tau in TAUS:
        cross_metrics[str(tau)]={}
        for eps in (EPS_PRIMARY,EPS_CONTROL):
            m=metric(tangent_cache[("D2",tau,eps,"linear",8192)],tangent_cache[("D2",tau,eps,"pchip",8192)])
            cross_metrics[str(tau)][str(eps)]=m; g6 &= response_pass(m,False)

    # G7: direct eta=0.05 dense shift vs local primary linear response.
    linearity={}; direct_shifts={}; g7=True
    for tau in TAUS:
        direct=_stack_direct_shift(cases,"D2",tau,supports,"linear",8192)
        pred=0.05*tangent_cache[("D2",tau,EPS_PRIMARY,"linear",8192)]
        m=metric(direct,pred)
        ok=bool(np.isfinite(m["E"]) and np.isfinite(m["C"]) and m["E"]<=LINEARITY_E_GATE and m["C"]>=LINEARITY_C_GATE)
        linearity[str(tau)]={**m,"pass":ok}; direct_shifts[str(tau)]=direct; g7 &= ok

    # G8: finite background response, not required to be zero.
    bg=np.asarray(bg_values,float); g8=bool(bg.size>0 and np.all(np.isfinite(bg)))
    bg_max=float(np.max(np.abs(bg))) if bg.size else float("nan")

    gates={
        "R11A_R01_G1_provenance_checkpoints":True,
        "R11A_R01_G2_support_baseline":bool(g2),
        "R11A_R01_G3_dense_resolution":bool(g3),
        "R11A_R01_G4_epsilon_consistency":bool(g4),
        "R11A_R01_G5_native_density_convergence":bool(g5),
        "R11A_R01_G6_cross_operator":bool(g6),
        "R11A_R01_G7_local_eta005_linearity":bool(g7),
        "R11A_R01_G8_background_prefactor_audit":bool(g8),
    }

    if not g2: classification=CLS_SUPPORT
    elif not g3: classification=CLS_RES
    elif not g4: classification=CLS_EPS
    elif not g5: classification=CLS_DENS
    elif not g6: classification=CLS_CROSS
    elif not g7: classification=CLS_LINEAR
    elif not g8: classification=CLS_BG
    else: classification=CLS_PASS

    physical={}; tau_coherence={}
    if classification==CLS_PASS:
        tref=tangent_cache[("D2",10.0,EPS_PRIMARY,"linear",8192)]
        for tau in TAUS:
            T=tangent_cache[("D2",tau,EPS_PRIMARY,"linear",8192)]
            ds=direct_shifts[str(tau)]
            # Direct dense absolute velocity difference for eta=0.05.
            dv=[]
            for iz in range(len(Z)):
                b0=_dense_baseline(cases[("D2",tau,0.0)]["rows"][iz],supports[iz],"linear",8192)
                bp=_dense_baseline(cases[("D2",tau,0.05)]["rows"][iz],supports[iz],"linear",8192)
                dv.append(bp["v"]-b0["v"])
            dv=np.stack(dv,axis=0)
            idx=np.unravel_index(int(np.argmax(np.abs(ds))),ds.shape)
            physical[str(tau)]={
                "max_abs_T_per_eta":float(np.max(np.abs(T))),
                "rms_T_per_eta":float(np.sqrt(np.mean(T*T))),
                "max_abs_fractional_shift_eta005":float(np.max(np.abs(ds))),
                "rms_fractional_shift_eta005":float(np.sqrt(np.mean(ds*ds))),
                "max_abs_velocity_shift_kms_eta005":float(np.max(np.abs(dv))),
                "largest_fractional_shift":{"z":float(Z[idx[0]]),"r_Mpc_h":float(R_MPC_H[idx[1]]),"fractional_shift":float(ds[idx]),"T_per_eta":float(T[idx]),"delta_v12_kms":float(dv[idx])},
                "linearity":linearity[str(tau)],
            }
            tau_coherence[str(tau)]=metric(tref,T)

    result={
        "classification":classification,"diagnostic_complete":True,"science_evaluated":classification==CLS_PASS,
        "gates":gates,"provenance":prov,"checkpoints":checkpoints,"native_refinement":refinement,
        "support":{"common_per_redshift":support_meta,"baseline":baseline_meta},
        "robustness":{"resolution":res_metrics,"epsilon":eps_metrics,"density":density_metrics,"cross_operator":cross_metrics,"eta005_linearity":linearity,"max_abs_DlnA_per_eta":bg_max},
        "physical_response":physical,"tau_coherence":tau_coherence,
        "settings":{"tau_H0":list(TAUS),"eta_values":list(ETAS),"epsilon_primary":EPS_PRIMARY,"epsilon_control":EPS_CONTROL,"r_Mpc_h":R_MPC_H.tolist(),"common_bounded_support":True,"primary":"LINEAR8192 signed response before Simpson integration","resolution_controls":[4096,16384],"shape_control":"PCHIP8192 signed response before Simpson integration","no_extrapolation":True,"no_smoothing":True,"no_clipping":True},
        "claim_scope":{"theory_only_pairwise_velocity_response":classification==CLS_PASS,"ksz_detection":False,"ksz_likelihood":False,"eta_bound":False,"tau_bound":False,"optical_depth_inference":False,"galaxy_halo_prediction":False,"nonlinear_small_scale_claim":False},
    }
    _write(out,result)

    arrays={"z":Z,"r_Mpc_h":R_MPC_H}
    for tau in TAUS:
        arrays[f"T_tau{tau:g}"]=tangent_cache[("D2",tau,EPS_PRIMARY,"linear",8192)]
        arrays[f"direct_shift_eta005_tau{tau:g}"]=direct_shifts[str(tau)]
    np.savez_compressed(args.npz_out,**arrays)

    print("STABLE_AEST_KSZ_R11A_REPAIR01_GATES="+json.dumps(gates,sort_keys=True),flush=True)
    print("STABLE_AEST_KSZ_R11A_REPAIR01_ROBUSTNESS="+json.dumps({"resolution":res_metrics,"epsilon":eps_metrics,"density":density_metrics,"cross_operator":cross_metrics,"linearity":linearity,"max_abs_DlnA_per_eta":bg_max},sort_keys=True),flush=True)
    if classification==CLS_PASS:
        print("STABLE_AEST_KSZ_R11A_REPAIR01_PHYSICAL="+json.dumps(physical,sort_keys=True),flush=True)
        print("STABLE_AEST_KSZ_R11A_REPAIR01_TAU="+json.dumps(tau_coherence,sort_keys=True),flush=True)
    print("STABLE_AEST_KSZ_R11A_REPAIR01_CLASSIFICATION="+classification,flush=True)
    return 0 if classification==CLS_PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
