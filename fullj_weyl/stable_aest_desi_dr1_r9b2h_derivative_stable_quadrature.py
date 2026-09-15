#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import simpson
from scipy.interpolate import PchipInterpolator

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fullj_weyl import stable_aest_observable_projection_r5b_derivative_zero as r5b
from fullj_weyl import stable_aest_desi_dr1_r9b2f_full_grid_rogue_node as r9b2f

PREFIT_LOCK = "e02eb97bf5675fb33a21f7545e0d7259ef5b97ce"
R9B2G_POSTDATA_LOCK = "68ca78bcea41a18af46ec4ccf6e30ddf78f64471"
R9B2G_PREFIT_LOCK = "2ea44eb92319fc6c2a3273dc91254e14dc797e35"
R9B2G_IMPL_LOCK = "ca8b788a40bc5de1649f53ff4cfe7ace5aa1500b"
R9B2F_POSTDATA_LOCK = "b569aebc41efc841755f5fcec63b91092c192ba3"

R9B2G_JSON = ROOT / "results/stable_aest_desi_dr1_r9b2g_bounded_source_extraction.json"
R9B2G_SHA256 = "2e2be7821088b8bbe2f152d8ee03cc950d3d4270d4725286dd0e976a522f4d34"
R9B2G_CLASS = "STABLE_AEST_DESI_DR1_R9B2G_CENTRAL_DERIVATIVE_FAIL"

ZEFF = np.asarray([
    0.29536404346937617, 0.5096288678782911, 0.7057956472488681,
    0.9185851971138159, 1.3170658832980264, 1.4905017757527006,
], float)
TAUS = (10.0, 5.0, 2.5, 1.25)
ETAS = (0.0, 0.025, -0.025, 0.05, -0.05)
EPS_PRIMARY = 0.025
EPS_CONTROL = 0.05
TOL = 3.0e-8
REL_GATE = 5.0e-3
RES_GATE = 1.0e-4
E_GATE = 0.05
C_GATE = 0.995
NORM_GATE = 1.0e-12
KMAX_PRIMARY = 5.0
KMAX_CONTROLS = (10.0, 20.0)
NGRID = (4096, 8192, 16384)

PASS = "STABLE_AEST_DESI_DR1_R9B2H_DERIVATIVE_STABLE_BOUNDED_QUADRATURE_VALIDATED"
FAIL_G1 = "STABLE_AEST_DESI_DR1_R9B2H_PROVENANCE_OR_CONSTRUCTION_FAIL"
FAIL_G2 = "STABLE_AEST_DESI_DR1_R9B2H_FINITE_PHYSICALITY_FAIL"
FAIL_G3 = "STABLE_AEST_DESI_DR1_R9B2H_RESOLUTION_CONVERGENCE_FAIL"
FAIL_G4 = "STABLE_AEST_DESI_DR1_R9B2H_QUADRATURE_AGREEMENT_FAIL"
FAIL_G5 = "STABLE_AEST_DESI_DR1_R9B2H_WITHIN_METHOD_DERIVATIVE_FAIL"
FAIL_G6 = "STABLE_AEST_DESI_DR1_R9B2H_CROSS_METHOD_DERIVATIVE_FAIL"
FAIL_G7 = "STABLE_AEST_DESI_DR1_R9B2H_KSUPPORT_CONVERGENCE_FAIL"
FAIL_RUN = "STABLE_AEST_DESI_DR1_R9B2H_RUN_FAIL"


def ancestor(sha: str) -> bool:
    return subprocess.run(["git","merge-base","--is-ancestor",sha,"HEAD"],cwd=ROOT,
                          stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode == 0


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(a: float, b: float) -> float:
    aa=float(a); bb=float(b)
    if not np.isfinite(aa) or not np.isfinite(bb): return float("inf")
    return abs(aa-bb)/max(abs(aa),abs(bb),1e-300)


def cosine(a,b):
    a=np.asarray(a,float); b=np.asarray(b,float)
    na=float(np.linalg.norm(a)); nb=float(np.linalg.norm(b))
    if na<=0 or nb<=0: return float("nan")
    return float(np.dot(a,b)/(na*nb))


def vec_metrics(a,b):
    a=np.asarray(a,float); b=np.asarray(b,float)
    na=float(np.linalg.norm(a)); nb=float(np.linalg.norm(b))
    return {"E":float(np.linalg.norm(a-b)/max(na,nb,1e-300)),"C":cosine(a,b),
            "norm_a":na,"norm_b":nb}


def _params(eta: float, tau: float, kmax: float):
    p, _, _ = r5b.build_params(float(eta), TOL)
    p["aest_tau_H0"] = float(tau)
    p["output"] = "mPk,mTk,vTk"
    p["z_max_pk"] = max(2.3, float(np.max(ZEFF))+0.25)
    p["P_k_max_h/Mpc"] = float(kmax)
    for key in ("non_linear","lensing","l_max_scalars","k_output_values",
                "k_per_decade_for_pk","k_per_decade_for_bao"):
        p.pop(key, None)
    return p


def _variance(kh, pk, mode: str, n: int = 8192):
    kh=np.asarray(kh,float); pk=np.asarray(pk,float)
    if kh.ndim!=1 or pk.shape!=kh.shape or kh.size<32 or np.any(~np.isfinite(kh)) or np.any(~np.isfinite(pk)) or np.any(pk<=0):
        raise RuntimeError("invalid bounded quadrature inputs")
    lk=np.log(kh); lp=np.log(pk); grid=np.linspace(lk[0],lk[-1],int(n)); kg=np.exp(grid)
    if mode=="loglinear":
        lpg=np.interp(grid,lk,lp)
    elif mode=="pchip":
        lpg=np.asarray(PchipInterpolator(lk,lp,extrapolate=False)(grid),float)
    else:
        raise ValueError(mode)
    if np.any(~np.isfinite(lpg)): raise RuntimeError(f"nonfinite {mode} interpolation")
    pg=np.exp(lpg)
    integ=kg**3*pg*r9b2f._w2(8.0*kg)
    var=float(simpson(integ,x=grid)/(2.0*np.pi**2))
    if not np.isfinite(var) or var<=0: raise RuntimeError(f"invalid {mode} variance {var}")
    return math.sqrt(var)


def _extract(st):
    kh=st["kh"]
    out={"n_k":int(kh.size),"kh_min":float(kh[0]),"kh_max":float(kh[-1])}
    for label,n in (("LL4096",4096),("LL8192",8192),("LL16384",16384)):
        sdd=_variance(kh,st["pdd"],"loglinear",n); stt=_variance(kh,st["ptt"],"loglinear",n)
        out[label]={"sigma8_dd":sdd,"sigma8_tt":stt,"f":stt/sdd}
    sdd=_variance(kh,st["pdd"],"pchip",8192); stt=_variance(kh,st["ptt"],"pchip",8192)
    out["PCHIP8192"]={"sigma8_dd":sdd,"sigma8_tt":stt,"f":stt/sdd}
    return out


def _run_case(eta: float, tau: float, kmax: float):
    from classy import Class
    p=_params(eta,tau,kmax); c=Class(); c.set(p); c.compute()
    try:
        As=float(p["A_s"]); ns=float(p["n_s"]); rows=[]
        for z in ZEFF:
            st=r9b2f._state_at_z(c,float(z),As,ns); row=_extract(st); row["z"]=float(z)
            rows.append(row)
        return rows
    finally:
        c.struct_cleanup(); c.empty()


def _key(tau,eta,kmax=KMAX_PRIMARY): return f"k{kmax:g}_tau{tau:g}_eta{eta:+.3f}"


def _fvec(vals,tau,eta,method,kmax=KMAX_PRIMARY):
    return np.asarray([r[method]["f"] for r in vals[_key(tau,eta,kmax)]],float)


def _tangents(vals,tau,method,kmax=KMAX_PRIMARY):
    p=(_fvec(vals,tau,+EPS_PRIMARY,method,kmax)-_fvec(vals,tau,-EPS_PRIMARY,method,kmax))/(2*EPS_PRIMARY)
    c=(_fvec(vals,tau,+EPS_CONTROL,method,kmax)-_fvec(vals,tau,-EPS_CONTROL,method,kmax))/(2*EPS_CONTROL)
    return p,c


def _derivative_summary(vals,tau,method,kmax=KMAX_PRIMARY):
    p,c=_tangents(vals,tau,method,kmax); m=vec_metrics(p,c)
    return {**m,"tangent_primary":p.tolist(),"tangent_control":c.tolist()}


def main() -> int:
    outpath=ROOT/"results/stable_aest_desi_dr1_r9b2h_derivative_stable_quadrature.json"
    print("STABLE_AEST_DESI_DR1_R9B2H_START",flush=True)
    try:
        parent=json.loads(R9B2G_JSON.read_text())
        g1=bool(all(ancestor(x) for x in (PREFIT_LOCK,R9B2G_POSTDATA_LOCK,R9B2G_PREFIT_LOCK,R9B2G_IMPL_LOCK,R9B2F_POSTDATA_LOCK))
                and sha256(R9B2G_JSON)==R9B2G_SHA256
                and parent.get("classification")==R9B2G_CLASS
                and parent.get("diagnostic_complete") is True
                and parent.get("science_evaluated") is False)
    except Exception:
        g1=False
    if not g1:
        out={"classification":FAIL_G1,"diagnostic_complete":False,"science_evaluated":False,
             "gates":{"R9B2H_H1_provenance_and_construction":False}}
        outpath.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
        print("STABLE_AEST_DESI_DR1_R9B2H_CLASSIFICATION="+FAIL_G1,flush=True); return 3

    vals={}; runs=[]
    try:
        for tau in TAUS:
            for eta in ETAS:
                print(f"STABLE_AEST_DESI_DR1_R9B2H_RUN kmax=5 tau={tau:g} eta={eta:+.3f}",flush=True)
                vals[_key(tau,eta,5.0)]=_run_case(eta,tau,5.0); runs.append({"kmax":5.0,"tau":tau,"eta":eta,"ok":True})
        for kmax in KMAX_CONTROLS:
            for eta in ETAS:
                print(f"STABLE_AEST_DESI_DR1_R9B2H_RUN kmax={kmax:g} tau=10 eta={eta:+.3f}",flush=True)
                vals[_key(10.0,eta,kmax)]=_run_case(eta,10.0,kmax); runs.append({"kmax":kmax,"tau":10.0,"eta":eta,"ok":True})
    except Exception as exc:
        out={"classification":FAIL_RUN,"diagnostic_complete":False,"science_evaluated":False,"error":repr(exc),"runs":runs}
        outpath.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
        print(f"STABLE_AEST_DESI_DR1_R9B2H_RUN_FAIL error={exc!r}",flush=True)
        print("STABLE_AEST_DESI_DR1_R9B2H_CLASSIFICATION="+FAIL_RUN,flush=True); return 2

    methods=("LL4096","LL8192","LL16384","PCHIP8192")
    g2=True
    for rows in vals.values():
        for r in rows:
            for method in methods:
                x=r[method]; g2 &= bool(np.isfinite(x["sigma8_dd"]) and np.isfinite(x["sigma8_tt"]) and np.isfinite(x["f"])
                    and 0.1<x["sigma8_dd"]<2.0 and 0.05<x["f"]<2.0)

    res12={q:0.0 for q in ("sigma8_dd","sigma8_tt","f")}; res23={q:0.0 for q in res12}; cross={q:0.0 for q in res12}
    for tau in TAUS:
        for eta in ETAS:
            for r in vals[_key(tau,eta,5.0)]:
                for q in res12:
                    res12[q]=max(res12[q],rel(r["LL4096"][q],r["LL8192"][q]))
                    res23[q]=max(res23[q],rel(r["LL8192"][q],r["LL16384"][q]))
                    cross[q]=max(cross[q],rel(r["LL8192"][q],r["PCHIP8192"][q]))
    g3=bool(max(res12.values())<=RES_GATE and max(res23.values())<=RES_GATE)
    g4=bool(max(cross.values())<=REL_GATE)

    deriv={}; g5=True; cross_tan={}; g6=True
    for tau in TAUS:
        deriv[str(tau)]={}
        for method in ("LL8192","PCHIP8192"):
            s=_derivative_summary(vals,tau,method,5.0); deriv[str(tau)][method]=s
            g5 &= bool(np.isfinite(s["E"]) and np.isfinite(s["C"]) and s["E"]<=E_GATE and s["C"]>=C_GATE and s["norm_a"]>NORM_GATE)
        llp,llc=_tangents(vals,tau,"LL8192",5.0); php,phc=_tangents(vals,tau,"PCHIP8192",5.0)
        mp=vec_metrics(llp,php); mc=vec_metrics(llc,phc); cross_tan[str(tau)]={"primary":mp,"control":mc}
        for m in (mp,mc): g6 &= bool(np.isfinite(m["E"]) and np.isfinite(m["C"]) and m["E"]<=E_GATE and m["C"]>=C_GATE)

    support={"k5_vs_k20":{q:0.0 for q in res12},"k10_vs_k20":{q:0.0 for q in res12}}
    for eta in ETAS:
        a=vals[_key(10.0,eta,5.0)]; b=vals[_key(10.0,eta,10.0)]; c=vals[_key(10.0,eta,20.0)]
        for ia in range(len(ZEFF)):
            for q in res12:
                support["k5_vs_k20"][q]=max(support["k5_vs_k20"][q],rel(a[ia]["LL8192"][q],c[ia]["LL8192"][q]))
                support["k10_vs_k20"][q]=max(support["k10_vs_k20"][q],rel(b[ia]["LL8192"][q],c[ia]["LL8192"][q]))
    support_deriv={}
    g7=bool(max(support["k5_vs_k20"].values())<=REL_GATE and max(support["k10_vs_k20"].values())<=REL_GATE)
    for kmax in (10.0,20.0):
        s=_derivative_summary(vals,10.0,"LL8192",kmax); support_deriv[f"k{kmax:g}"]=s
        g7 &= bool(s["E"]<=E_GATE and s["C"]>=C_GATE and s["norm_a"]>NORM_GATE)
    p5,c5=_tangents(vals,10.0,"LL8192",5.0); p20,c20=_tangents(vals,10.0,"LL8192",20.0)
    support_deriv["k5_vs_k20_primary"]=vec_metrics(p5,p20); support_deriv["k5_vs_k20_control"]=vec_metrics(c5,c20)
    for name in ("k5_vs_k20_primary","k5_vs_k20_control"):
        m=support_deriv[name]; g7 &= bool(m["E"]<=E_GATE and m["C"]>=C_GATE)

    gates={
        "R9B2H_H1_provenance_and_construction":True,
        "R9B2H_H2_finite_physicality":bool(g2),
        "R9B2H_H3_loglinear_resolution_convergence":bool(g3),
        "R9B2H_H4_shape_preserving_quadrature_agreement":bool(g4),
        "R9B2H_H5_within_method_derivative_consistency":bool(g5),
        "R9B2H_H6_cross_method_tangent_agreement":bool(g6),
        "R9B2H_H7_actual_k_support_convergence":bool(g7),
    }
    if not g2: classification=FAIL_G2
    elif not g3: classification=FAIL_G3
    elif not g4: classification=FAIL_G4
    elif not g5: classification=FAIL_G5
    elif not g6: classification=FAIL_G6
    elif not g7: classification=FAIL_G7
    else: classification=PASS

    metrics={"rel_gate":REL_GATE,"resolution_gate":RES_GATE,"E_gate":E_GATE,"C_gate":C_GATE,
             "resolution_LL4096_vs_LL8192":res12,"resolution_LL8192_vs_LL16384":res23,
             "LL8192_vs_PCHIP8192":cross,"derivative":deriv,"cross_method_tangent":cross_tan,
             "support_value_convergence":support,"support_derivative":support_deriv}
    out={"classification":classification,"diagnostic_complete":True,"science_evaluated":False,"desi_data_loaded":False,
         "gates":gates,"metrics":metrics,"runs":runs,"cases":vals,
         "settings":{"tau_H0_grid":list(TAUS),"eta_grid":list(ETAS),"zeff":ZEFF.tolist(),
                     "kmax_primary":KMAX_PRIMARY,"kmax_controls":list(KMAX_CONTROLS),
                     "quadratures":{"Q1":"loglinear4096","Q2":"loglinear8192","Q3":"loglinear16384","Q4":"logP_PCHIP8192"}},
         "interpretation":{"historical_failures_reclassified":False,
                           "corrected_shapeFit_theory_extraction_licensed":classification==PASS,
                           "licensed_primary_extraction":"bounded_loglinear_8192" if classification==PASS else None,
                           "observational_claim_licensed":False}}
    outpath.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print("STABLE_AEST_DESI_DR1_R9B2H_GATES="+json.dumps(gates,sort_keys=True),flush=True)
    print("STABLE_AEST_DESI_DR1_R9B2H_METRICS="+json.dumps(metrics,sort_keys=True),flush=True)
    print("STABLE_AEST_DESI_DR1_R9B2H_CLASSIFICATION="+classification,flush=True)
    return 0 if classification==PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
