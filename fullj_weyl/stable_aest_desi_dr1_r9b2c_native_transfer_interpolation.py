#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np
from scipy.interpolate import PchipInterpolator, interp1d

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from v063 import theory_response_map as v63
from fullj_weyl import stable_aest_desi_dr1_r9b_shapefit_projection as r9b
from fullj_weyl import stable_aest_observable_projection_r5b_derivative_zero as r5b

PREFIT_LOCK = "1e999d87c1158ee7be764e6055164d75a179b059"
POSTDATA_LOCK = "3101581468bc8a5b85eb2b34c33df22418f1ce88"
ADAPTER_LOCK = "f5484b4572b673dfcead51875e3aa790c698a18c"
V078_LOCK = "31c05c22b86e8ac01ce822306efecdcb03cff1d5"

R9B2B_JSON = ROOT / "results/stable_aest_desi_dr1_r9b2b_source_state_extraction.json"
ADAPTER_JSON = ROOT / "results/stable_aest_desi_dr1_r9b2_velocity_adapter_validation.json"
V078_NOTE = ROOT / "docs/v078_preserved_interpretation.md"

R9B2B_SHA256 = "bc0013a70a1e13ef925efc39b57f8810d7c5bab80091eed1ba4407bc1862314e"
ADAPTER_SHA256 = "c4d9281cd504785a9e4fb187b02db2860e24622bbe1ccf4a52e44446be0a119a"
R9B2B_CLASS = "STABLE_AEST_DESI_DR1_R9B2B_AEST_ETA0_CLOSURE_FAIL"
ADAPTER_CLASS = "STABLE_AEST_DESI_DR1_R9B2_VELOCITY_ADAPTER_VALIDATED"

ZEFF = np.asarray([
    0.29536404346937617,
    0.5096288678782911,
    0.7057956472488681,
    0.9185851971138159,
    1.3170658832980264,
    1.4905017757527006,
], dtype=float)
TAUS = (10.0, 5.0, 2.5, 1.25)
REL_GATE = 5.0e-3
MATERIAL_GATE = 5.0e-2
KH_MIN = 1.0e-4
KH_MAX = 5.0
TOL = 3.0e-8
KPIVOT = 0.05

CLS_PASS = "STABLE_AEST_DESI_DR1_R9B2C_OFFNATIVE_TRANSFER_INTERPOLATION_DEFECT_CERTIFIED"
CLS_PROV = "STABLE_AEST_DESI_DR1_R9B2C_PROVENANCE_FAIL"
CLS_COVER = "STABLE_AEST_DESI_DR1_R9B2C_NATIVE_STATE_COVERAGE_FAIL"
CLS_GR = "STABLE_AEST_DESI_DR1_R9B2C_GR_INTERPOLATION_BENCHMARK_FAIL"
CLS_NATIVE = "STABLE_AEST_DESI_DR1_R9B2C_NATIVE_AEST_STATE_FAIL"
CLS_PCHIP = "STABLE_AEST_DESI_DR1_R9B2C_PCHIP_TARGET_CLOSURE_FAIL"
CLS_LOCAL = "STABLE_AEST_DESI_DR1_R9B2C_ACCESSOR_DISCREPANCY_NOT_LOCALIZED"
CLS_ROBUST = "STABLE_AEST_DESI_DR1_R9B2C_INTERPOLATION_ROBUSTNESS_FAIL"
CLS_TAU = "STABLE_AEST_DESI_DR1_R9B2C_ETA0_TAU_INVARIANCE_FAIL"
CLS_RUN = "STABLE_AEST_DESI_DR1_R9B2C_RUN_FAIL"


def ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"], cwd=ROOT,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    ).returncode == 0


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(a: float, b: float) -> float:
    aa = float(a); bb = float(b)
    return float(abs(aa-bb) / max(abs(aa), abs(bb), 1e-300))


def _params_gr():
    p = dict(v63.class_params())
    p.update({
        "aest_enabled": "no",
        "aest_memory_enabled": "no",
        "aest_eta": 0.0,
        "output": "mPk,mTk,vTk",
        "z_max_pk": max(2.3, float(np.max(ZEFF))+0.25),
        "P_k_max_h/Mpc": KH_MAX,
    })
    p.pop("non_linear", None); p.pop("lensing", None)
    p.pop("l_max_scalars", None); p.pop("k_output_values", None)
    return p


def _params_aest(tau: float):
    p, _, _ = r5b.build_params(0.0, TOL)
    p["aest_tau_H0"] = float(tau)
    p["output"] = "mPk,mTk,vTk"
    p["z_max_pk"] = max(2.3, float(np.max(ZEFF))+0.25)
    p["P_k_max_h/Mpc"] = KH_MAX
    p.pop("non_linear", None); p.pop("lensing", None)
    p.pop("l_max_scalars", None); p.pop("k_output_values", None)
    return p


def _native_table(c):
    tab, k_mpc, z_native = c.get_transfer_and_k_and_z(output_format="class", h_units=False)
    required = ("d_b", "d_cdm", "t_b", "t_cdm")
    missing = [x for x in required if x not in tab]
    if missing:
        raise RuntimeError(f"native transfer fields missing: {missing}; keys={sorted(tab)}")

    k_mpc = np.asarray(k_mpc, float)
    z_native = np.asarray(z_native, float)
    arrays = {name: np.asarray(tab[name], float) for name in required}
    shape = (k_mpc.size, z_native.size)
    if any(arr.shape != shape for arr in arrays.values()):
        raise RuntimeError(f"native transfer orientation mismatch expected={shape} got=" +
                           str({k:v.shape for k,v in arrays.items()}))
    if not np.all(np.isfinite(k_mpc)) or not np.all(np.isfinite(z_native)):
        raise RuntimeError("nonfinite native coordinates")
    if any(not np.all(np.isfinite(arr)) for arr in arrays.values()):
        raise RuntimeError("nonfinite native state array")

    h = float(c.h())
    kh = k_mpc/h
    kmask = (kh >= KH_MIN) & (kh <= KH_MAX)
    if np.count_nonzero(kmask) < 32:
        raise RuntimeError("insufficient native k support")
    kh = kh[kmask]
    arrays = {name: arr[kmask, :] for name, arr in arrays.items()}
    korder = np.argsort(kh)
    kh = kh[korder]
    arrays = {name: arr[korder, :] for name, arr in arrays.items()}
    if kh[0] > 2.0e-4 or kh[-1] < 2.0 or np.any(np.diff(kh) <= 0.0):
        raise RuntimeError(f"native k support invalid {kh[0]}..{kh[-1]}")

    a = 1.0/(1.0+z_native)
    aorder = np.argsort(a)
    a = a[aorder]
    z_sorted = z_native[aorder]
    arrays = {name: arr[:, aorder] for name, arr in arrays.items()}
    au, idx = np.unique(a, return_index=True)
    if au.size < 4:
        raise RuntimeError("insufficient unique native time nodes")
    a = au
    z_sorted = z_sorted[idx]
    arrays = {name: arr[:, idx] for name, arr in arrays.items()}
    if np.any(np.diff(a) <= 0.0):
        raise RuntimeError("native scale-factor grid not strictly increasing")

    at = 1.0/(1.0+ZEFF)
    if float(np.min(at)) < float(a[0]) or float(np.max(at)) > float(a[-1]):
        raise RuntimeError(f"targets not bracketed by native a grid {a[0]}..{a[-1]}")

    return {"kh": kh, "a": a, "z": z_sorted, **arrays}


def _interp_states(native, method: str):
    at = 1.0/(1.0+ZEFF)
    out = {}
    for name in ("d_b", "d_cdm", "t_b", "t_cdm"):
        arr = native[name]
        if method == "pchip":
            f = PchipInterpolator(native["a"], arr, axis=1, extrapolate=False)
        elif method == "linear":
            f = interp1d(native["a"], arr, axis=1, kind="linear", bounds_error=True)
        else:
            raise ValueError(method)
        val = np.asarray(f(at), float)
        if val.shape != (native["kh"].size, ZEFF.size) or not np.all(np.isfinite(val)):
            raise RuntimeError(f"invalid {method} state interpolation for {name}")
        out[name] = val
    return out


def _sigma_pair(c, kh, db, dc, tb, tc, z: float, As: float, ns: float):
    from cosmoprimo import PowerSpectrumInterpolator1D

    Om_b = r9b._omega(c, "Omega_b")
    Om_c = r9b._omega(c, "Omega_cdm")
    fb = Om_b/(Om_b+Om_c); fc = 1.0-fb
    dcb = fb*np.asarray(db,float) + fc*np.asarray(dc,float)
    theta = fb*np.asarray(tb,float) + fc*np.asarray(tc,float)
    Hconf = float(c.Hubble(float(z)))/(1.0+float(z))
    if not np.isfinite(Hconf) or Hconf <= 0.0:
        raise RuntimeError(f"invalid Hconf at z={z}")
    vcb = -theta/Hconf

    kh = np.asarray(kh,float)
    k_mpc = kh*float(c.h())
    primordial = float(As)*(k_mpc/KPIVOT)**(float(ns)-1.0)
    pref = (2.0*math.pi**2/k_mpc**3)*primordial
    pdd = pref*dcb**2*float(c.h())**3
    ptt = pref*vcb**2*float(c.h())**3
    if (not np.all(np.isfinite(pdd)) or not np.all(np.isfinite(ptt)) or
            not np.all(pdd > 0.0) or not np.all(ptt > 0.0)):
        raise RuntimeError(f"nonpositive/nonfinite source spectrum at z={z}")
    sdd = float(np.asarray(PowerSpectrumInterpolator1D(kh,pdd).sigma8()))
    stt = float(np.asarray(PowerSpectrumInterpolator1D(kh,ptt).sigma8()))
    return {"sigma8_dd": sdd, "sigma8_tt": stt, "f": stt/sdd}


def _target_rows_from_interp(c, native, states, params, internal=False):
    rows=[]; As=float(params.get("A_s",v63.START["A_s"])); ns=float(params.get("n_s",v63.START["n_s"]))
    for j,z in enumerate(ZEFF):
        q=_sigma_pair(c,native["kh"],states["d_b"][:,j],states["d_cdm"][:,j],
                      states["t_b"][:,j],states["t_cdm"][:,j],float(z),As,ns)
        q["z"]=float(z)
        if internal:
            si=float(c.sigma(8.0,float(z),h_units=True))
            fp=float(c.effective_f_sigma8(float(z),z_step=0.1))/si
            q.update({"sigma8_internal":si,"legacy_growth_proxy":fp,
                      "rel_sigma8_vs_internal":rel(q["sigma8_dd"],si),
                      "rel_f_vs_internal_proxy":rel(q["f"],fp)})
        rows.append(q)
    return rows


def _target_rows_direct(c, params):
    rows=[]; As=float(params.get("A_s",v63.START["A_s"])); ns=float(params.get("n_s",v63.START["n_s"]))
    for z in ZEFF:
        tr=c.get_transfer(float(z),output_format="class")
        required=("k (h/Mpc)","d_b","d_cdm","t_b","t_cdm")
        if any(x not in tr for x in required):
            raise RuntimeError(f"direct transfer missing field at z={z}")
        kh=np.asarray(tr["k (h/Mpc)"],float)
        mask=np.isfinite(kh)&(kh>=KH_MIN)&(kh<=KH_MAX)
        vals=[np.asarray(tr[x],float)[mask] for x in required[1:]]
        kh=kh[mask]
        order=np.argsort(kh); kh=kh[order]; vals=[v[order] for v in vals]
        keep=np.ones(kh.size,dtype=bool)
        if kh.size>1: keep[1:]=np.diff(kh)>0.0
        kh=kh[keep]; vals=[v[keep] for v in vals]
        q=_sigma_pair(c,kh,*vals,float(z),As,ns); q["z"]=float(z); rows.append(q)
    return rows


def _native_health(c, native, params):
    As=float(params.get("A_s",v63.START["A_s"])); ns=float(params.get("n_s",v63.START["n_s"]))
    zarr=native["z"]
    idx=np.where((zarr>=0.2)&(zarr<=1.6))[0]
    if idx.size == 0:
        raise RuntimeError("no native nodes in z=0.2..1.6")
    worst={"sigma8_dd_min":float("inf"),"sigma8_dd_max":0.0,"f_min":float("inf"),"f_max":0.0,
           "n_nodes":int(idx.size)}
    ok=True
    for j in idx:
        z=float(zarr[j])
        q=_sigma_pair(c,native["kh"],native["d_b"][:,j],native["d_cdm"][:,j],
                      native["t_b"][:,j],native["t_cdm"][:,j],z,As,ns)
        worst["sigma8_dd_min"]=min(worst["sigma8_dd_min"],q["sigma8_dd"])
        worst["sigma8_dd_max"]=max(worst["sigma8_dd_max"],q["sigma8_dd"])
        worst["f_min"]=min(worst["f_min"],q["f"])
        worst["f_max"]=max(worst["f_max"],q["f"])
        ok &= bool(0.1<q["sigma8_dd"]<2.0 and 0.05<q["f"]<2.0)
    worst["pass"]=bool(ok)
    return worst


def _run_model(params, need_direct=False, internal=False, native_health=False):
    from classy import Class
    c=Class(); c.set(params); c.compute()
    try:
        native=_native_table(c)
        pchip=_interp_states(native,"pchip")
        linear=_interp_states(native,"linear")
        out={
            "coverage": {"n_k":int(native["kh"].size),"n_z":int(native["a"].size),
                         "kh_min":float(native["kh"][0]),"kh_max":float(native["kh"][-1]),
                         "z_min":float(np.min(native["z"])),"z_max":float(np.max(native["z"]))},
            "pchip":_target_rows_from_interp(c,native,pchip,params,internal=internal),
            "linear":_target_rows_from_interp(c,native,linear,params,internal=False),
        }
        if need_direct: out["direct"]=_target_rows_direct(c,params)
        if native_health: out["native_health"]=_native_health(c,native,params)
        return out
    finally:
        c.struct_cleanup(); c.empty()


def _rowmap(rows): return {float(x["z"]):x for x in rows}


def main() -> int:
    outpath=ROOT/"results/stable_aest_desi_dr1_r9b2c_native_transfer_interpolation.json"
    print("STABLE_AEST_DESI_DR1_R9B2C_START",flush=True)

    try:
        parent=json.loads(R9B2B_JSON.read_text()); adapter=json.loads(ADAPTER_JSON.read_text()); note=V078_NOTE.read_text()
        g=parent.get("gates",{})
        c1=bool(
            ancestor(PREFIT_LOCK) and ancestor(POSTDATA_LOCK) and ancestor(ADAPTER_LOCK) and ancestor(V078_LOCK)
            and sha256(R9B2B_JSON)==R9B2B_SHA256 and sha256(ADAPTER_JSON)==ADAPTER_SHA256
            and parent.get("classification")==R9B2B_CLASS and parent.get("diagnostic_complete") is True
            and parent.get("science_evaluated") is False
            and g.get("R9B2B_B1_provenance_and_historical_lock") is True
            and g.get("R9B2B_B2_source_state_construction") is True
            and g.get("R9B2B_B3_pure_GR_benchmark") is True
            and g.get("R9B2B_B4_AeST_eta0_source_internal_consistency") is False
            and g.get("R9B2B_B5_eta0_tau_invariance") is True
            and g.get("R9B2B_B6_pathological_point_removal") is False
            and adapter.get("classification")==ADAPTER_CLASS and adapter.get("diagnostic_complete") is True
            and "V078_TIME_INTERPOLATION_OPERATOR_CLOSURE_PASS" in note
            and "V078_TIME_INTERPOLATION_OPERATOR_DISCREPANCY_LOCALIZED" in note
        )
    except Exception as exc:
        c1=False; adapter={}; parent={}; prov_error=repr(exc)
    else:
        prov_error=None
    if not c1:
        out={"classification":CLS_PROV,"diagnostic_complete":False,"science_evaluated":False,"error":prov_error}
        outpath.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
        print("STABLE_AEST_DESI_DR1_R9B2C_CLASSIFICATION="+CLS_PROV,flush=True); return 3

    try:
        gr=_run_model(_params_gr(),need_direct=False,internal=False,native_health=False)
        aest={}
        for tau in TAUS:
            print(f"STABLE_AEST_DESI_DR1_R9B2C_AEST_TAU tau_H0={tau:g}",flush=True)
            aest[str(tau)]=_run_model(_params_aest(tau),need_direct=(tau==10.0),internal=(tau==10.0),native_health=(tau==10.0))
    except Exception as exc:
        out={"classification":CLS_RUN,"diagnostic_complete":False,"science_evaluated":False,"error":repr(exc)}
        outpath.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
        print(f"STABLE_AEST_DESI_DR1_R9B2C_RUN_FAIL error={exc!r}",flush=True)
        print("STABLE_AEST_DESI_DR1_R9B2C_CLASSIFICATION="+CLS_RUN,flush=True); return 2

    c2=True
    for rr in [gr,*aest.values()]:
        cv=rr["coverage"]
        c2 &= bool(cv["n_k"]>=32 and cv["kh_min"]<=2e-4 and cv["kh_max"]>=2.0)

    locked=_rowmap(adapter["rows"]); gr_cmp=[]; c3=True
    for rr in gr["pchip"]:
        aa=locked[float(rr["z"])]
        x={"z":rr["z"],
           "rel_sigma8_dd_vs_locked_class":rel(rr["sigma8_dd"],aa["class_sigma8_dd"]),
           "rel_sigma8_tt_vs_locked_class":rel(rr["sigma8_tt"],aa["class_sigma8_tt"]),
           "rel_f_vs_locked_class":rel(rr["f"],aa["class_f"]),
           "rel_f_vs_locked_camb":rel(rr["f"],aa["camb_f"])}
        x["pass"]=bool(max(v for k,v in x.items() if k.startswith("rel_"))<=REL_GATE); c3 &= x["pass"]; gr_cmp.append(x)

    a10=aest["10.0"]; c4=bool(a10["native_health"]["pass"])
    c5=True
    for rr in a10["pchip"]:
        rr["closure_pass"]=bool(0.1<rr["sigma8_dd"]<2.0 and 0.05<rr["f"]<2.0
                                and rr["rel_sigma8_vs_internal"]<=REL_GATE
                                and rr["rel_f_vs_internal_proxy"]<=REL_GATE)
        c5 &= rr["closure_pass"]

    pmap=_rowmap(a10["pchip"]); dmap=_rowmap(a10["direct"])
    accessor_max=0.0; accessor_rows=[]
    for z in pmap:
        ds=rel(dmap[z]["sigma8_dd"],pmap[z]["sigma8_dd"]); df=rel(dmap[z]["f"],pmap[z]["f"])
        accessor_max=max(accessor_max,ds,df); accessor_rows.append({"z":z,"rel_sigma8_dd_direct_vs_pchip":ds,"rel_f_direct_vs_pchip":df})
    c6=bool(c4 and c5 and accessor_max>=MATERIAL_GATE)

    lmap=_rowmap(a10["linear"])
    robust={"max_rel_sigma8_dd":0.0,"max_rel_sigma8_tt":0.0,"max_rel_f":0.0}
    for z in pmap:
        robust["max_rel_sigma8_dd"]=max(robust["max_rel_sigma8_dd"],rel(lmap[z]["sigma8_dd"],pmap[z]["sigma8_dd"]))
        robust["max_rel_sigma8_tt"]=max(robust["max_rel_sigma8_tt"],rel(lmap[z]["sigma8_tt"],pmap[z]["sigma8_tt"]))
        robust["max_rel_f"]=max(robust["max_rel_f"],rel(lmap[z]["f"],pmap[z]["f"]))
    c7=bool(max(robust.values())<=REL_GATE)

    tau_metrics={"max_rel_sigma8_dd":0.0,"max_rel_sigma8_tt":0.0,"max_rel_f":0.0}
    for key,rr in aest.items():
        if key=="10.0": continue
        mm=_rowmap(rr["pchip"])
        for z in pmap:
            tau_metrics["max_rel_sigma8_dd"]=max(tau_metrics["max_rel_sigma8_dd"],rel(mm[z]["sigma8_dd"],pmap[z]["sigma8_dd"]))
            tau_metrics["max_rel_sigma8_tt"]=max(tau_metrics["max_rel_sigma8_tt"],rel(mm[z]["sigma8_tt"],pmap[z]["sigma8_tt"]))
            tau_metrics["max_rel_f"]=max(tau_metrics["max_rel_f"],rel(mm[z]["f"],pmap[z]["f"]))
    c8=bool(max(tau_metrics.values())<=REL_GATE)

    gates={
        "R9B2C_C1_provenance_and_historical_lock":bool(c1),
        "R9B2C_C2_native_state_coverage_and_finiteness":bool(c2),
        "R9B2C_C3_pure_GR_custom_interpolation_benchmark":bool(c3),
        "R9B2C_C4_AeST_native_state_sanity":bool(c4),
        "R9B2C_C5_AeST_PCHIP_target_closure":bool(c5),
        "R9B2C_C6_accessor_discrepancy_localization":bool(c6),
        "R9B2C_C7_external_interpolation_robustness":bool(c7),
        "R9B2C_C8_eta0_tau_invariance":bool(c8),
    }
    if not c2: classification=CLS_COVER
    elif not c3: classification=CLS_GR
    elif not c4: classification=CLS_NATIVE
    elif not c5: classification=CLS_PCHIP
    elif not c6: classification=CLS_LOCAL
    elif not c7: classification=CLS_ROBUST
    elif not c8: classification=CLS_TAU
    else: classification=CLS_PASS

    metrics={
        "rel_gate":REL_GATE,"material_gate":MATERIAL_GATE,
        "GR_max_rel_sigma8_dd_vs_locked_class":max(x["rel_sigma8_dd_vs_locked_class"] for x in gr_cmp),
        "GR_max_rel_sigma8_tt_vs_locked_class":max(x["rel_sigma8_tt_vs_locked_class"] for x in gr_cmp),
        "GR_max_rel_f_vs_locked_class":max(x["rel_f_vs_locked_class"] for x in gr_cmp),
        "GR_max_rel_f_vs_locked_camb":max(x["rel_f_vs_locked_camb"] for x in gr_cmp),
        "AeST_PCHIP_max_rel_sigma8_vs_internal":max(x["rel_sigma8_vs_internal"] for x in a10["pchip"]),
        "AeST_PCHIP_max_rel_f_vs_internal_proxy":max(x["rel_f_vs_internal_proxy"] for x in a10["pchip"]),
        "accessor_max_material_discrepancy":accessor_max,
        "PCHIP_vs_linear":robust,
        "tau_invariance":tau_metrics,
    }
    out={
        "classification":classification,"diagnostic_complete":True,"science_evaluated":False,"desi_data_loaded":False,
        "gates":gates,"metrics":metrics,"GR":gr,"GR_comparison_to_locked_adapter":gr_cmp,
        "AeST_by_tau":aest,"accessor_comparison_tau10":accessor_rows,
        "interpretation":{"historical_failures_reclassified":False,"desi_detection_claim_licensed":False,
                          "eta_or_tau_constraint_licensed":False,
                          "native_state_DESI_followup_licensed":classification==CLS_PASS},
    }
    outpath.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print("STABLE_AEST_DESI_DR1_R9B2C_GATES="+json.dumps(gates,sort_keys=True),flush=True)
    print("STABLE_AEST_DESI_DR1_R9B2C_METRICS="+json.dumps(metrics,sort_keys=True),flush=True)
    print("STABLE_AEST_DESI_DR1_R9B2C_CLASSIFICATION="+classification,flush=True)
    return 0 if classification==CLS_PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
