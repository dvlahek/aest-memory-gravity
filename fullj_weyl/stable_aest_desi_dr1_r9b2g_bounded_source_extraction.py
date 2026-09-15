#!/usr/bin/env python3
from __future__ import annotations

import inspect
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fullj_weyl import stable_aest_observable_projection_r5b_derivative_zero as r5b
from fullj_weyl import stable_aest_desi_dr1_r9b2f_full_grid_rogue_node as r9b2f

PREFIT_LOCK = "2ea44eb92319fc6c2a3273dc91254e14dc797e35"
R9B2F_POSTDATA_LOCK = "b569aebc41efc841755f5fcec63b91092c192ba3"
R9B2F_PREFIT_LOCK = "8413ed74450e387b3dee543ff67b39bf2cbb31bc"
R9B2F_IMPL_LOCK = "1c1cbbbdc2fcb43441c1659f7282ae40c3b18487"
R9B2E_POSTDATA_LOCK = "f1f2bfd032065360ec7a18c080403d6e39f54dc7"

ZEFF = np.asarray([
    0.29536404346937617,
    0.5096288678782911,
    0.7057956472488681,
    0.9185851971138159,
    1.3170658832980264,
    1.4905017757527006,
], float)
TAUS = (10.0, 5.0, 2.5, 1.25)
ETAS = (0.0, 0.025, -0.025, 0.05, -0.05)
EPS_PRIMARY = 0.025
EPS_CONTROL = 0.05
TOL = 3.0e-8
REL_GATE = 5.0e-3
E_GATE = 0.05
C_GATE = 0.995
NORM_GATE = 1.0e-12
KH_MAX = 5.0

PASS = "STABLE_AEST_DESI_DR1_R9B2G_BOUNDED_SOURCE_EXTRACTION_VALIDATED"
FAIL_G1 = "STABLE_AEST_DESI_DR1_R9B2G_PROVENANCE_OR_CONSTRUCTION_FAIL"
FAIL_G2 = "STABLE_AEST_DESI_DR1_R9B2G_FINITE_PHYSICALITY_FAIL"
FAIL_G3 = "STABLE_AEST_DESI_DR1_R9B2G_BOUNDED_INTEGRAL_CROSSCHECK_FAIL"
FAIL_G4 = "STABLE_AEST_DESI_DR1_R9B2G_ETA0_INTERNAL_CLOSURE_FAIL"
FAIL_G5 = "STABLE_AEST_DESI_DR1_R9B2G_ETA0_TAU_INVARIANCE_FAIL"
FAIL_G6 = "STABLE_AEST_DESI_DR1_R9B2G_CENTRAL_DERIVATIVE_FAIL"
FAIL_RUN = "STABLE_AEST_DESI_DR1_R9B2G_RUN_FAIL"


def ancestor(sha: str) -> bool:
    return subprocess.run(["git","merge-base","--is-ancestor",sha,"HEAD"],cwd=ROOT,
                          stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode == 0


def rel(a: float, b: float) -> float:
    aa=float(a); bb=float(b)
    if not np.isfinite(aa) or not np.isfinite(bb): return float("inf")
    return abs(aa-bb)/max(abs(aa),abs(bb),1e-300)


def cosine(a,b):
    a=np.asarray(a,float); b=np.asarray(b,float)
    na=float(np.linalg.norm(a)); nb=float(np.linalg.norm(b))
    if na<=0 or nb<=0: return float("nan")
    return float(np.dot(a,b)/(na*nb))


def _params(eta: float, tau: float):
    p, _, _ = r5b.build_params(float(eta), TOL)
    p["aest_tau_H0"] = float(tau)
    p["output"] = "mPk,mTk,vTk"
    p["z_max_pk"] = max(2.3, float(np.max(ZEFF))+0.25)
    p["P_k_max_h/Mpc"] = KH_MAX
    for key in ("non_linear","lensing","l_max_scalars","k_output_values",
                "k_per_decade_for_pk","k_per_decade_for_bao"):
        p.pop(key, None)
    return p


def _construction_gate():
    p=_params(0.0,10.0)
    absent=all(k not in p for k in ("k_output_values","k_per_decade_for_pk","k_per_decade_for_bao"))
    src_state=inspect.getsource(r9b2f._state_at_z)
    src_cosmo=inspect.getsource(r9b2f._cosmo_sigma8)
    src_linear=inspect.getsource(r9b2f._loglinear_sigma8)
    return bool(absent and "pdd=pref*dcb**2" in src_state and "ptt=pref*vcb**2" in src_state
                and "pk_lin" not in src_state and "pk_cb_lin" not in src_state
                and "extrap_kmin=float(kh[0])" in src_cosmo and "extrap_kmax=float(kh[-1])" in src_cosmo
                and "grid=np.linspace(logk[0],logk[-1],NLOG)" in src_linear)


def _run_case(eta: float, tau: float):
    from classy import Class
    p=_params(eta,tau); c=Class(); c.set(p); c.compute()
    try:
        As=float(p["A_s"]); ns=float(p["n_s"])
        rows=[]
        for z in ZEFF:
            st=r9b2f._state_at_z(c,float(z),As,ns)
            kh=st["kh"]
            cb_dd=r9b2f._cosmo_sigma8(kh,st["pdd"],True)
            cb_tt=r9b2f._cosmo_sigma8(kh,st["ptt"],True)
            ll_dd=r9b2f._loglinear_sigma8(kh,st["pdd"])
            ll_tt=r9b2f._loglinear_sigma8(kh,st["ptt"])
            cb_f=cb_tt/cb_dd; ll_f=ll_tt/ll_dd
            si=float(c.sigma(8.0,float(z),h_units=True))
            proxy=float(c.effective_f_sigma8(float(z),z_step=0.1))/si
            row={
                "z":float(z),"n_k":int(kh.size),"kh_min":float(kh[0]),"kh_max":float(kh[-1]),
                "bounded_cosmo":{"sigma8_dd":cb_dd,"sigma8_tt":cb_tt,"f":cb_f},
                "bounded_loglinear":{"sigma8_dd":ll_dd,"sigma8_tt":ll_tt,"f":ll_f},
                "cross_rel":{"sigma8_dd":rel(cb_dd,ll_dd),"sigma8_tt":rel(cb_tt,ll_tt),"f":rel(cb_f,ll_f)},
                "internal":{"sigma8":si,"growth_proxy":proxy,
                            "rel_sigma8":rel(cb_dd,si),"rel_f":rel(cb_f,proxy)},
            }
            rows.append(row)
        return rows
    finally:
        c.struct_cleanup(); c.empty()


def _key(tau,eta): return f"tau{tau:g}_eta{eta:+.3f}"


def _rowmap(rows): return {float(r["z"]):r for r in rows}


def main() -> int:
    outpath=ROOT/"results/stable_aest_desi_dr1_r9b2g_bounded_source_extraction.json"
    print("STABLE_AEST_DESI_DR1_R9B2G_START",flush=True)
    g1=bool(all(ancestor(x) for x in (PREFIT_LOCK,R9B2F_POSTDATA_LOCK,R9B2F_PREFIT_LOCK,R9B2F_IMPL_LOCK,R9B2E_POSTDATA_LOCK))
            and _construction_gate())
    if not g1:
        out={"classification":FAIL_G1,"diagnostic_complete":False,"science_evaluated":False,
             "gates":{"R9B2G_G1_provenance_and_construction":False}}
        outpath.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
        print("STABLE_AEST_DESI_DR1_R9B2G_CLASSIFICATION="+FAIL_G1,flush=True); return 3

    vals={}; runs=[]
    try:
        for tau in TAUS:
            for eta in ETAS:
                key=_key(tau,eta)
                print(f"STABLE_AEST_DESI_DR1_R9B2G_RUN tau={tau:g} eta={eta:+.3f}",flush=True)
                rows=_run_case(eta,tau); vals[key]=rows
                runs.append({"tau_H0":tau,"eta":eta,"ok":True})
    except Exception as exc:
        out={"classification":FAIL_RUN,"diagnostic_complete":False,"science_evaluated":False,
             "error":repr(exc),"runs":runs}
        outpath.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
        print(f"STABLE_AEST_DESI_DR1_R9B2G_RUN_FAIL error={exc!r}",flush=True)
        print("STABLE_AEST_DESI_DR1_R9B2G_CLASSIFICATION="+FAIL_RUN,flush=True); return 2

    g2=True; cross={"sigma8_dd":0.0,"sigma8_tt":0.0,"f":0.0}
    for rows in vals.values():
        for r in rows:
            for method in ("bounded_cosmo","bounded_loglinear"):
                x=r[method]
                g2 &= bool(np.isfinite(x["sigma8_dd"]) and np.isfinite(x["sigma8_tt"]) and np.isfinite(x["f"])
                           and 0.1<x["sigma8_dd"]<2.0 and 0.05<x["f"]<2.0)
            for q in cross: cross[q]=max(cross[q],r["cross_rel"][q])
    g3=bool(max(cross.values())<=REL_GATE)

    eta0_internal={"sigma8":0.0,"f":0.0}; g4=True
    for tau in TAUS:
        for r in vals[_key(tau,0.0)]:
            eta0_internal["sigma8"]=max(eta0_internal["sigma8"],r["internal"]["rel_sigma8"])
            eta0_internal["f"]=max(eta0_internal["f"],r["internal"]["rel_f"])
            g4 &= bool(r["internal"]["rel_sigma8"]<=REL_GATE and r["internal"]["rel_f"]<=REL_GATE)

    tauvar={"sigma8_dd":0.0,"sigma8_tt":0.0,"f":0.0}
    for z in ZEFF:
        samples=[]
        for tau in TAUS:
            rm=_rowmap(vals[_key(tau,0.0)])
            samples.append(rm[float(z)]["bounded_cosmo"])
        for q in tauvar:
            arr=[x[q] for x in samples]
            tauvar[q]=max(tauvar[q],(max(arr)-min(arr))/max(max(map(abs,arr)),1e-300))
    g5=bool(max(tauvar.values())<=REL_GATE)

    central={}; g6=True
    for tau in TAUS:
        fp=np.asarray([r["bounded_cosmo"]["f"] for r in vals[_key(tau,+EPS_PRIMARY)]],float)
        fm=np.asarray([r["bounded_cosmo"]["f"] for r in vals[_key(tau,-EPS_PRIMARY)]],float)
        cp=np.asarray([r["bounded_cosmo"]["f"] for r in vals[_key(tau,+EPS_CONTROL)]],float)
        cm=np.asarray([r["bounded_cosmo"]["f"] for r in vals[_key(tau,-EPS_CONTROL)]],float)
        t1=(fp-fm)/(2*EPS_PRIMARY); t2=(cp-cm)/(2*EPS_CONTROL)
        n1=float(np.linalg.norm(t1)); n2=float(np.linalg.norm(t2)); E=float(np.linalg.norm(t1-t2)/max(n1,n2,1e-300)); C=cosine(t1,t2)
        central[str(tau)]={"E":E,"C":C,"norm_primary":n1,"norm_control":n2,
                           "tangent_primary":t1.tolist(),"tangent_control":t2.tolist()}
        g6 &= bool(np.isfinite(E) and np.isfinite(C) and E<=E_GATE and C>=C_GATE and n1>NORM_GATE)

    gates={
        "R9B2G_G1_provenance_and_construction":g1,
        "R9B2G_G2_full_grid_finite_physical":bool(g2),
        "R9B2G_G3_independent_bounded_integral_agreement":g3,
        "R9B2G_G4_eta0_internal_closure":bool(g4),
        "R9B2G_G5_eta0_tau_invariance":g5,
        "R9B2G_G6_central_derivative_consistency":bool(g6),
    }
    if not g2: classification=FAIL_G2
    elif not g3: classification=FAIL_G3
    elif not g4: classification=FAIL_G4
    elif not g5: classification=FAIL_G5
    elif not g6: classification=FAIL_G6
    else: classification=PASS

    metrics={"rel_gate":REL_GATE,"E_gate":E_GATE,"C_gate":C_GATE,
             "max_bounded_cosmo_vs_loglinear":cross,"max_eta0_internal_rel":eta0_internal,
             "max_eta0_tau_variation":tauvar,"central_derivative":central}
    out={"classification":classification,"diagnostic_complete":True,"science_evaluated":False,"desi_data_loaded":False,
         "gates":gates,"metrics":metrics,"runs":runs,"cases":vals,
         "settings":{"tau_H0_grid":list(TAUS),"eta_grid":list(ETAS),"zeff":ZEFF.tolist(),
                     "default_k_sampling":True,"bounded_support_only":True},
         "interpretation":{"historical_failures_reclassified":False,
                           "corrected_shapeFit_projection_licensed":classification==PASS,
                           "observational_claim_licensed":False}}
    outpath.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print("STABLE_AEST_DESI_DR1_R9B2G_GATES="+json.dumps(gates,sort_keys=True),flush=True)
    print("STABLE_AEST_DESI_DR1_R9B2G_METRICS="+json.dumps(metrics,sort_keys=True),flush=True)
    print("STABLE_AEST_DESI_DR1_R9B2G_CLASSIFICATION="+classification,flush=True)
    return 0 if classification==PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
