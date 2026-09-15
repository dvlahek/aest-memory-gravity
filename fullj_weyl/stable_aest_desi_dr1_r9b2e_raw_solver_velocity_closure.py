#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np
from scipy.interpolate import CubicSpline, PchipInterpolator

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fullj_weyl import stable_aest_observable_projection_r5b_derivative_zero as r5b
from nl1c6d2a import baryon_matter_sector_audit as d2a

PREFIT_LOCK = "756eb268bdc4d0c3ba8dc6bfa94ba74eb11bdab1"
R9B2D_POSTDATA_LOCK = "6b26243f78b477f7d4040c6499085faf05e8ffac"
R9B2D_PREFIT_LOCK = "bb15759f23246d3b7af734ff7f7cb2052f44d651"
R9B2D_IMPL_LOCK = "a18020d3b307294b742614edc75a5ed28d7a91e8"
R9B2C_POSTDATA_LOCK = "7c4cc8a0a9f2a59a91cbb288a157f880d630f309"

R9B2D_JSON = ROOT / "results/stable_aest_desi_dr1_r9b2d_kgrid_inheritance.json"
R9B2D_SHA256 = "54db5acc49d4099d1173aa029a58e02cdac0e844c03aa72d95fa08b86a6f70df"
R9B2D_CLASS = "STABLE_AEST_DESI_DR1_R9B2D_DEFAULT_GRID_AEST_UNRESOLVED"

ZEFF = np.asarray([
    0.29536404346937617,
    0.5096288678782911,
    0.7057956472488681,
    0.9185851971138159,
    1.3170658832980264,
    1.4905017757527006,
], float)
K_H = np.geomspace(0.02, 2.0, 24)
TOL = 3.0e-8
TAU = 10.0
K_MATCH_GATE = 1.0e-12
INTERNAL_GATE = 5.0e-3
PRIMARY_CLOSURE_GATE = 2.0e-4
PCHIP_CLOSURE_GATE = 5.0e-4
CONTINUITY_GATE = 2.0e-3
MATERIAL_GLOBAL_GATE = 5.0e-2
MATERIAL_POINT_GATE = 5.0e-1
RAW_INTERP_GATE = 5.0e-3
Z_CONT_MIN = 0.2
Z_CONT_MAX = 1.6
EDGE_DROP = 2
MIN_INTERIOR = 20

PASS = "STABLE_AEST_DESI_DR1_R9B2E_TRANSFER_VELOCITY_MAPPING_DEFECT_CERTIFIED"
PROV_FAIL = "STABLE_AEST_DESI_DR1_R9B2E_PROVENANCE_OR_MODE_IDENTITY_FAIL"
KOUT_FAIL = "STABLE_AEST_DESI_DR1_R9B2E_KOUTPUT_INTERNAL_INVARIANCE_FAIL"
GR_FAIL = "STABLE_AEST_DESI_DR1_R9B2E_GR_RAW_TRANSFER_CLOSURE_FAIL"
RAW_FAIL = "STABLE_AEST_DESI_DR1_R9B2E_RAW_SOLVER_HISTORY_UNRESOLVED"
DENSITY_FAIL = "STABLE_AEST_DESI_DR1_R9B2E_DENSITY_MAPPING_UNRESOLVED"
VELOCITY_FAIL = "STABLE_AEST_DESI_DR1_R9B2E_VELOCITY_MAPPING_DEFECT_NOT_LOCALIZED"
ROBUST_FAIL = "STABLE_AEST_DESI_DR1_R9B2E_RAW_INTERPOLATION_ROBUSTNESS_FAIL"
RUN_FAIL = "STABLE_AEST_DESI_DR1_R9B2E_RUN_FAIL"

FIELDS = ("d_b", "t_b", "d_cdm", "t_cdm")


def ancestor(sha: str) -> bool:
    return subprocess.run(["git", "merge-base", "--is-ancestor", sha, "HEAD"], cwd=ROOT,
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel_scalar(a: float, b: float) -> float:
    aa=float(a); bb=float(b)
    return abs(aa-bb)/max(abs(aa),abs(bb),1e-300)


def rel_l2(a, b) -> float:
    aa=np.asarray(a,float); bb=np.asarray(b,float)
    return float(np.linalg.norm(aa-bb)/max(np.linalg.norm(aa),np.linalg.norm(bb),1e-300))


def symrel(a, b) -> float:
    aa=float(a); bb=float(b)
    return abs(aa-bb)/max(abs(aa),abs(bb),1e-300)


def _base_default_params():
    p, _, _ = r5b.build_params(0.0, TOL)
    p["aest_tau_H0"] = TAU
    p["output"] = "mPk,mTk,vTk"
    p["z_max_pk"] = max(2.3, float(np.max(ZEFF))+0.25)
    p["P_k_max_h/Mpc"] = 5.0
    for key in ("non_linear", "lensing", "l_max_scalars", "k_output_values",
                "k_per_decade_for_pk", "k_per_decade_for_bao"):
        p.pop(key, None)
    return p


def _diag_params(aest: bool):
    p=dict(_base_default_params())
    h=float(p["H0"])/100.0
    k_req=K_H*h
    p["k_output_values"] = ", ".join(format(float(k), ".17g") for k in k_req)
    if not aest:
        p["aest_enabled"] = "no"
        p["aest_memory_enabled"] = "no"
        p["aest_eta"] = 0.0
    return p


def _pick(raw, names):
    for name in names:
        if name in raw:
            return name
    raise RuntimeError(f"missing field among {names}; available={sorted(raw.keys())}")


def _reported_kh(raw, h: float) -> float:
    candidates = (
        ("k (h/Mpc)", 1.0), ("k [h/Mpc]", 1.0), ("k[h/Mpc]", 1.0),
        ("k (1/Mpc)", 1.0/h), ("k [1/Mpc]", 1.0/h), ("k[1/Mpc]", 1.0/h),
    )
    for key,factor in candidates:
        if key in raw:
            a=np.asarray(raw[key],float).ravel(); a=a[np.isfinite(a)]
            if a.size == 0:
                continue
            if np.max(np.abs(a-a[0])) > 1e-10*max(abs(float(a[0])),1.0):
                raise RuntimeError(f"reported k field {key} is not constant")
            return float(a[0])*factor
    raise RuntimeError(f"raw history lacks recognized k field; available={sorted(raw.keys())}")


def _clean_x(x, *ys):
    x=np.asarray(x,float); arrs=[np.asarray(y,float) for y in ys]
    if any(y.shape != x.shape for y in arrs):
        raise RuntimeError("raw history shape mismatch")
    order=np.argsort(x); x=x[order]; arrs=[y[order] for y in arrs]
    good=np.isfinite(x)
    for y in arrs: good &= np.isfinite(y)
    x=x[good]; arrs=[y[good] for y in arrs]
    keep=np.ones(x.size,dtype=bool)
    if x.size>1: keep[1:]=np.diff(x)>0
    x=x[keep]; arrs=[y[keep] for y in arrs]
    if x.size < 4 or np.any(np.diff(x)<=0):
        raise RuntimeError("insufficient/nonmonotone raw history coordinate")
    return (x,*arrs)


def _prepare_history(raw, h: float):
    akey=_pick(raw,("a","scale factor"))
    tkey=_pick(raw,("tau [Mpc]","tau","tau[Mpc]"))
    dbkey=_pick(raw,("delta_b","d_b"))
    tbkey=_pick(raw,("theta_b","t_b"))
    dckey=_pick(raw,("delta_cdm","d_cdm"))
    tckey=_pick(raw,("theta_cdm","t_cdm"))
    phikey=_pick(raw,("phi",))
    pprime="phi_prime" if "phi_prime" in raw else None
    arrays=[np.asarray(raw[k],float) for k in (akey,tkey,dbkey,tbkey,dckey,tckey,phikey)]
    aa,tau,db,tb,dc,tc,phi=arrays
    if pprime is not None:
        phip=np.asarray(raw[pprime],float)
        tau,aa,db,tb,dc,tc,phi,phip=_clean_x(tau,aa,db,tb,dc,tc,phi,phip)
        phip_source="direct_CLASS_phi_prime"
    else:
        tau,aa,db,tb,dc,tc,phi=_clean_x(tau,aa,db,tb,dc,tc,phi)
        phip=CubicSpline(tau,phi,bc_type="not-a-knot")(tau,1)
        phip_source="cubic_spline_derivative_of_phi"
    if np.any(aa<=0):
        raise RuntimeError("nonpositive scale factor in raw history")
    return {
        "k_h":_reported_kh(raw,h), "tau":tau, "a":aa, "z":1.0/aa-1.0,
        "d_b":db, "t_b":tb, "d_cdm":dc, "t_cdm":tc,
        "phi":phi, "phi_prime":phip, "phi_prime_source":phip_source,
        "n":int(tau.size), "keys":sorted(raw.keys()),
    }


def _ordered_histories(c, h: float):
    pert=c.get_perturbations(); raws,key=d2a.scalar_histories(pert)
    if len(raws) != len(K_H):
        raise RuntimeError(f"expected {len(K_H)} scalar histories, got {len(raws)}")
    hs=[_prepare_history(raw,h) for raw in raws]
    out=[]; used=set(); misses=[]
    for target in K_H:
        d=np.asarray([abs(x["k_h"]-target) if i not in used else np.inf for i,x in enumerate(hs)],float)
        j=int(np.argmin(d)); miss=float(d[j]/target)
        if not np.isfinite(miss):
            raise RuntimeError("raw history mode assignment failed")
        used.add(j); out.append(hs[j]); misses.append(miss)
    return out,key,float(max(misses))


def _raw_target_matrix(histories, method: str):
    at=1.0/(1.0+ZEFF); mats={f:np.empty((len(K_H),len(ZEFF)),float) for f in FIELDS}
    for i,hist in enumerate(histories):
        a=hist["a"]
        if float(np.min(a)) > float(np.min(at)) or float(np.max(a)) < float(np.max(at)):
            raise RuntimeError(f"raw history k={hist['k_h']} does not bracket target a range")
        for f in FIELDS:
            if method == "cubic":
                sp=CubicSpline(a,hist[f],bc_type="not-a-knot")
            elif method == "pchip":
                sp=PchipInterpolator(a,hist[f],extrapolate=False)
            else:
                raise ValueError(method)
            vals=np.asarray(sp(at),float)
            if not np.all(np.isfinite(vals)):
                raise RuntimeError(f"nonfinite {method} raw interpolation field={f}")
            mats[f][i,:]=vals
    return mats


def _transfer_target_matrix(c):
    mats={f:np.empty((len(K_H),len(ZEFF)),float) for f in FIELDS}
    max_miss=0.0
    for iz,z in enumerate(ZEFF):
        tr=c.get_transfer(float(z),output_format="class")
        kh=np.asarray(tr[_pick(tr,("k (h/Mpc)","k [h/Mpc]","k[h/Mpc]"))],float)
        for f in FIELDS:
            if f not in tr:
                raise RuntimeError(f"transfer missing {f} at z={z}; keys={sorted(tr)}")
        for ik,target in enumerate(K_H):
            j=int(np.argmin(np.abs(kh-target)))
            miss=abs(float(kh[j])-float(target))/float(target); max_miss=max(max_miss,miss)
            for f in FIELDS:
                mats[f][ik,iz]=float(np.asarray(tr[f],float)[j])
    return mats,float(max_miss)


def _continuity(histories):
    out={"b":{"max":0.0,"rows":[]},"cdm":{"max":0.0,"rows":[]}}
    finite=True
    for i,hist in enumerate(histories):
        tau=hist["tau"]; z=hist["z"]; phip=hist["phi_prime"]
        for species,df,tf in (("b","d_b","t_b"),("cdm","d_cdm","t_cdm")):
            delta=hist[df]; theta=hist[tf]
            finite &= bool(np.all(np.isfinite(delta)) and np.all(np.isfinite(theta)) and np.all(np.isfinite(phip)))
            dp=CubicSpline(tau,delta,bc_type="not-a-knot")(tau,1)
            idx=np.where((z>=Z_CONT_MIN)&(z<=Z_CONT_MAX))[0]
            if idx.size > 2*EDGE_DROP: idx=idx[EDGE_DROP:-EDGE_DROP]
            if idx.size < MIN_INTERIOR:
                raise RuntimeError(f"mode {i} species={species} has only {idx.size} continuity samples")
            res=dp[idx]+theta[idx]-3.0*phip[idx]
            scale=max(float(np.linalg.norm(dp[idx])),float(np.linalg.norm(theta[idx])),
                      float(np.linalg.norm(3.0*phip[idx])),1e-300)
            nr=float(np.linalg.norm(res)/scale)
            out[species]["max"]=max(out[species]["max"],nr)
            out[species]["rows"].append({"mode_index":i,"k_h":float(hist["k_h"]),
                                          "n":int(idx.size),"normalized_L2":nr})
    out["finite"]=bool(finite)
    return out


def _closure(raw, transfer):
    out={}
    for f in FIELDS:
        out[f]=rel_l2(raw[f],transfer[f])
    return out


def _point_max(raw, transfer, fields):
    worst={"value":0.0,"field":None,"mode_index":None,"k_h":None,"z":None,
           "raw":None,"transfer":None}
    for f in fields:
        for i,k in enumerate(K_H):
            for j,z in enumerate(ZEFF):
                q=symrel(raw[f][i,j],transfer[f][i,j])
                if q>worst["value"]:
                    worst={"value":float(q),"field":f,"mode_index":int(i),"k_h":float(k),
                           "z":float(z),"raw":float(raw[f][i,j]),"transfer":float(transfer[f][i,j])}
    return worst


def _internal(c):
    rows=[]
    for z in ZEFF:
        s=float(c.sigma(8.0,float(z),h_units=True)); p=float(c.effective_f_sigma8(float(z),z_step=0.1))/s
        rows.append({"z":float(z),"sigma8":s,"growth_proxy":p})
    return rows


def _run(aest: bool):
    from classy import Class
    p=_diag_params(aest); c=Class(); c.set(p); c.compute()
    try:
        h=float(c.h())
        histories,container,raw_k_miss=_ordered_histories(c,h)
        cubic=_raw_target_matrix(histories,"cubic")
        pchip=_raw_target_matrix(histories,"pchip")
        transfer,transfer_k_miss=_transfer_target_matrix(c)
        continuity=_continuity(histories)
        return {
            "container":container,"raw_k_miss_max":raw_k_miss,"transfer_k_miss_max":transfer_k_miss,
            "histories_summary":[{"k_h":float(x["k_h"]),"n":x["n"],
                                  "z_min":float(np.min(x["z"])),"z_max":float(np.max(x["z"])),
                                  "phi_prime_source":x["phi_prime_source"]} for x in histories],
            "raw_cubic":{f:cubic[f].tolist() for f in FIELDS},
            "raw_pchip":{f:pchip[f].tolist() for f in FIELDS},
            "transfer":{f:transfer[f].tolist() for f in FIELDS},
            "closure_cubic":_closure(cubic,transfer),
            "closure_pchip":_closure(pchip,transfer),
            "raw_interp_cubic_vs_pchip":{f:rel_l2(cubic[f],pchip[f]) for f in FIELDS},
            "velocity_point_worst_cubic":_point_max(cubic,transfer,("t_b","t_cdm")),
            "velocity_point_worst_pchip":_point_max(pchip,transfer,("t_b","t_cdm")),
            "continuity":continuity,"internal":_internal(c),
        }
    finally:
        c.struct_cleanup(); c.empty()


def _map_rows(rows):
    return {float(x["z"]):x for x in rows}


def main() -> int:
    outpath=ROOT/"results/stable_aest_desi_dr1_r9b2e_raw_solver_velocity_closure.json"
    print("STABLE_AEST_DESI_DR1_R9B2E_START",flush=True)
    parent={}; e1=False
    try:
        p=json.loads(R9B2D_JSON.read_text()); parent={"classification":p.get("classification"),"sha256":sha256(R9B2D_JSON)}
        expected_gates={
            "R9B2D_D1_provenance_and_configuration_isolation":True,
            "R9B2D_D2_node_count_separation":True,
            "R9B2D_D3_GR_sampling_invariance":True,
            "R9B2D_D4_DEFAULT_AeST_eta0_closure":False,
            "R9B2D_D5_DENSE_pathology_reproduction":False,
            "R9B2D_D6_internal_solution_invariance":True,
        }
        e1=bool(all(ancestor(x) for x in (PREFIT_LOCK,R9B2D_POSTDATA_LOCK,R9B2D_PREFIT_LOCK,R9B2D_IMPL_LOCK,R9B2C_POSTDATA_LOCK))
                and sha256(R9B2D_JSON)==R9B2D_SHA256 and p.get("classification")==R9B2D_CLASS
                and p.get("diagnostic_complete") is True and p.get("science_evaluated") is False
                and p.get("gates")==expected_gates)
    except Exception as exc:
        parent["error"]=repr(exc); p={}
    if not e1:
        out={"classification":PROV_FAIL,"diagnostic_complete":False,"science_evaluated":False,
             "gates":{"R9B2E_E1_provenance_and_requested_mode_identity":False},"parent":parent}
        outpath.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
        print("STABLE_AEST_DESI_DR1_R9B2E_CLASSIFICATION="+PROV_FAIL,flush=True); return 3
    try:
        print("STABLE_AEST_DESI_DR1_R9B2E_RUN=AEST_RAW",flush=True); ae=_run(True)
        print("STABLE_AEST_DESI_DR1_R9B2E_RUN=GR_RAW",flush=True); gr=_run(False)
    except Exception as exc:
        out={"classification":RUN_FAIL,"diagnostic_complete":False,"science_evaluated":False,"error":repr(exc),"parent":parent}
        outpath.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
        print(f"STABLE_AEST_DESI_DR1_R9B2E_RUN_FAIL error={exc!r}",flush=True)
        print("STABLE_AEST_DESI_DR1_R9B2E_CLASSIFICATION="+RUN_FAIL,flush=True); return 2

    e1=bool(e1 and ae["raw_k_miss_max"]<=K_MATCH_GATE and ae["transfer_k_miss_max"]<=K_MATCH_GATE
            and gr["raw_k_miss_max"]<=K_MATCH_GATE and gr["transfer_k_miss_max"]<=K_MATCH_GATE)

    base=_map_rows(p["AeST_default"]["rows"]); current=_map_rows(ae["internal"])
    intdiff={"sigma8":0.0,"growth_proxy":0.0}
    for z in current:
        intdiff["sigma8"]=max(intdiff["sigma8"],rel_scalar(current[z]["sigma8"],base[z]["sigma8_internal"]))
        intdiff["growth_proxy"]=max(intdiff["growth_proxy"],rel_scalar(current[z]["growth_proxy"],base[z]["legacy_growth_proxy"]))
    e2=bool(max(intdiff.values())<=INTERNAL_GATE)

    e3=bool(max(gr["closure_cubic"].values())<=PRIMARY_CLOSURE_GATE and
            max(gr["closure_pchip"].values())<=PCHIP_CLOSURE_GATE)

    e4=bool(ae["continuity"]["finite"] and ae["continuity"]["b"]["max"]<=CONTINUITY_GATE and
            ae["continuity"]["cdm"]["max"]<=CONTINUITY_GATE)

    e5=bool(max(ae["closure_cubic"][f] for f in ("d_b","d_cdm"))<=PRIMARY_CLOSURE_GATE and
            max(ae["closure_pchip"][f] for f in ("d_b","d_cdm"))<=PCHIP_CLOSURE_GATE)

    vel_global=max(ae["closure_cubic"]["t_b"],ae["closure_cubic"]["t_cdm"],
                   ae["closure_pchip"]["t_b"],ae["closure_pchip"]["t_cdm"])
    vel_point=max(ae["velocity_point_worst_cubic"]["value"],ae["velocity_point_worst_pchip"]["value"])
    material=bool(vel_global>=MATERIAL_GLOBAL_GATE or vel_point>=MATERIAL_POINT_GATE)
    e6=bool(e4 and e5 and material)

    e7=bool(max(ae["raw_interp_cubic_vs_pchip"].values())<=RAW_INTERP_GATE)

    gates={
        "R9B2E_E1_provenance_and_requested_mode_identity":e1,
        "R9B2E_E2_koutput_internal_invariance":e2,
        "R9B2E_E3_GR_raw_transfer_closure":e3,
        "R9B2E_E4_AeST_raw_continuity_and_finiteness":e4,
        "R9B2E_E5_AeST_raw_transfer_density_closure":e5,
        "R9B2E_E6_AeST_velocity_discrepancy_localization":e6,
        "R9B2E_E7_raw_interpolation_robustness":e7,
    }
    if not e1: classification=PROV_FAIL
    elif not e2: classification=KOUT_FAIL
    elif not e3: classification=GR_FAIL
    elif not e4: classification=RAW_FAIL
    elif not e5: classification=DENSITY_FAIL
    elif not e6: classification=VELOCITY_FAIL
    elif not e7: classification=ROBUST_FAIL
    else: classification=PASS

    metrics={
        "k_match_gate":K_MATCH_GATE,"internal_gate":INTERNAL_GATE,
        "primary_closure_gate":PRIMARY_CLOSURE_GATE,"pchip_closure_gate":PCHIP_CLOSURE_GATE,
        "continuity_gate":CONTINUITY_GATE,"material_global_gate":MATERIAL_GLOBAL_GATE,
        "material_point_gate":MATERIAL_POINT_GATE,"raw_interp_gate":RAW_INTERP_GATE,
        "AeST_raw_k_miss_max":ae["raw_k_miss_max"],"AeST_transfer_k_miss_max":ae["transfer_k_miss_max"],
        "GR_raw_k_miss_max":gr["raw_k_miss_max"],"GR_transfer_k_miss_max":gr["transfer_k_miss_max"],
        "koutput_internal_vs_R9b2d_default":intdiff,
        "GR_closure_cubic":gr["closure_cubic"],"GR_closure_pchip":gr["closure_pchip"],
        "AeST_continuity_max":{"b":ae["continuity"]["b"]["max"],"cdm":ae["continuity"]["cdm"]["max"]},
        "AeST_closure_cubic":ae["closure_cubic"],"AeST_closure_pchip":ae["closure_pchip"],
        "AeST_raw_interp_cubic_vs_pchip":ae["raw_interp_cubic_vs_pchip"],
        "AeST_velocity_material_global_max":vel_global,"AeST_velocity_material_point_max":vel_point,
        "AeST_velocity_worst_cubic":ae["velocity_point_worst_cubic"],
        "AeST_velocity_worst_pchip":ae["velocity_point_worst_pchip"],
    }
    out={
        "classification":classification,"diagnostic_complete":True,"science_evaluated":False,"desi_data_loaded":False,
        "settings":{"K_H":K_H.tolist(),"ZEFF":ZEFF.tolist(),"eta":0.0,"tau_H0":TAU,
                    "default_k_sampling":True,"n_requested_modes":len(K_H)},
        "gates":gates,"metrics":metrics,"parent":parent,"AeST":ae,"GR":gr,
        "interpretation":{"historical_failures_reclassified":False,"desi_detection_claim_licensed":False,
                          "transfer_velocity_mapping_defect_certified":classification==PASS,
                          "raw_solver_history_unresolved":classification==RAW_FAIL},
    }
    outpath.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print("STABLE_AEST_DESI_DR1_R9B2E_GATES="+json.dumps(gates,sort_keys=True),flush=True)
    print("STABLE_AEST_DESI_DR1_R9B2E_METRICS="+json.dumps(metrics,sort_keys=True),flush=True)
    print("STABLE_AEST_DESI_DR1_R9B2E_CLASSIFICATION="+classification,flush=True)
    return 0 if classification==PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
