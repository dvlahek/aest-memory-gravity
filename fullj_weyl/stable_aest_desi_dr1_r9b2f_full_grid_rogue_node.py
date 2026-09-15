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
from fullj_weyl import stable_aest_desi_dr1_r9b_shapefit_projection as r9b
from nl1c6d2a import baryon_matter_sector_audit as d2a

PREFIT_LOCK = "8413ed74450e387b3dee543ff67b39bf2cbb31bc"
R9B2E_POSTDATA_LOCK = "f1f2bfd032065360ec7a18c080403d6e39f54dc7"
R9B2E_REPAIR_PREFIT_LOCK = "28e98f6490ab02a979461b150af972898156d1fa"
R9B2E_REPAIR_IMPL_LOCK = "02c95668f655afe96c9351b573c020cb1f241acb"
R9B2E_REPAIR_RUNNER_LOCK = "793248884e4c5fbba52943716d54135ec05f55f7"
R9B2D_POSTDATA_LOCK = "6b26243f78b477f7d4040c6499085faf05e8ffac"

R9B2E_JSON = ROOT / "results/stable_aest_desi_dr1_r9b2e_raw_solver_velocity_closure.json"
R9B2E_SHA256 = "3deb9cf8b946f56727b4f10af70dababefda2b31098e1039b15ac21d03c5d255"
R9B2E_CLASS = "STABLE_AEST_DESI_DR1_R9B2E_VELOCITY_MAPPING_DEFECT_NOT_LOCALIZED"

ZEFF = np.asarray([
    0.29536404346937617,
    0.5096288678782911,
    0.7057956472488681,
    0.9185851971138159,
    1.3170658832980264,
    1.4905017757527006,
], float)
TOL = 3.0e-8
TAU = 10.0
KH_MIN = 1.0e-4
KH_MAX = 5.0
KPIVOT = 0.05
NLOG = 8192
REL_GATE = 5.0e-3
RAW_TRANSFER_GATE = 2.0e-4
MATERIAL_GATE = 5.0e-2
K_MATCH_GATE = 1.0e-12
N_TOP = 8

CLS_EXTRAP = "STABLE_AEST_DESI_DR1_R9B2F_HIGH_K_EXTRAPOLATION_DEFECT_CERTIFIED"
CLS_INTERP = "STABLE_AEST_DESI_DR1_R9B2F_POWER_INTERPOLATION_DEFECT_CERTIFIED"
CLS_ROGUE = "STABLE_AEST_DESI_DR1_R9B2F_AUTOMATIC_KGRID_ROGUE_NODE_DEFECT_CERTIFIED"
CLS_UNRES = "STABLE_AEST_DESI_DR1_R9B2F_FULL_GRID_PATHOLOGY_UNRESOLVED"
CLS_PROV = "STABLE_AEST_DESI_DR1_R9B2F_PROVENANCE_FAIL"
CLS_RUN = "STABLE_AEST_DESI_DR1_R9B2F_RUN_FAIL"


def ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"], cwd=ROOT,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    ).returncode == 0


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(a: float, b: float) -> float:
    aa=float(a); bb=float(b)
    return abs(aa-bb)/max(abs(aa),abs(bb),1e-300)


def point_rel(a: float, b: float, floor: float) -> float:
    return abs(float(a)-float(b))/max(abs(float(a)),abs(float(b)),float(floor),1e-300)


def _pick(raw, names):
    for name in names:
        if name in raw:
            return name
    raise RuntimeError(f"missing field among {names}; available={sorted(raw.keys())}")


def _base_params(kout_kh=None):
    p, _, _ = r5b.build_params(0.0, TOL)
    p["aest_tau_H0"] = TAU
    p["output"] = "mPk,mTk,vTk"
    p["z_max_pk"] = max(2.3, float(np.max(ZEFF))+0.25)
    p["P_k_max_h/Mpc"] = KH_MAX
    for key in ("non_linear","lensing","l_max_scalars","k_output_values",
                "k_per_decade_for_pk","k_per_decade_for_bao"):
        p.pop(key, None)
    if kout_kh is not None:
        h=float(p["H0"])/100.0
        vals=np.asarray(kout_kh,float)*h
        p["k_output_values"] = ", ".join(format(float(x), ".17g") for x in vals)
    return p


def _clean_common(kh,*ys):
    kh=np.asarray(kh,float); arr=[np.asarray(y,float) for y in ys]
    if any(y.shape!=kh.shape for y in arr):
        raise RuntimeError("transfer shape mismatch")
    good=np.isfinite(kh)&(kh>=KH_MIN)&(kh<=KH_MAX)
    for y in arr: good &= np.isfinite(y)
    kh=kh[good]; arr=[y[good] for y in arr]
    order=np.argsort(kh); kh=kh[order]; arr=[y[order] for y in arr]
    keep=np.ones(kh.size,dtype=bool)
    if kh.size>1: keep[1:]=np.diff(kh)>0
    kh=kh[keep]; arr=[y[keep] for y in arr]
    if kh.size<32 or kh[0]>2e-4 or kh[-1]<2.0:
        raise RuntimeError(f"insufficient transfer support n={kh.size} range={kh[0] if kh.size else np.nan}..{kh[-1] if kh.size else np.nan}")
    return (kh,*arr)


def _w2(x):
    x=np.asarray(x,float); out=np.empty_like(x)
    low=x<0.1
    x2=x[low]**2
    out[low]=(1.0+x2*(-1.0/10.0+x2*(1.0/280.0+x2*(-1.0/15120.0+x2*(1.0/1330560.0+x2*(-1.0/172972800.0))))))**2
    xx=x[~low]
    out[~low]=(3.0*(np.sin(xx)-xx*np.cos(xx))/xx**3)**2
    return out


def _loglinear_sigma8(kh, pk):
    kh=np.asarray(kh,float); pk=np.asarray(pk,float)
    if not np.all(np.isfinite(pk)) or np.any(pk<=0):
        raise RuntimeError("LOGLINEAR_BOUNDED requires finite positive P(k)")
    logk=np.log(kh); logp=np.log(pk)
    grid=np.linspace(logk[0],logk[-1],NLOG)
    kg=np.exp(grid); pg=np.exp(np.interp(grid,logk,logp))
    integ=kg**3*pg*_w2(8.0*kg)
    var=float(simpson(integ,x=grid)/(2.0*np.pi**2))
    if not np.isfinite(var) or var<=0:
        raise RuntimeError(f"invalid direct variance {var}")
    return math.sqrt(var)


def _cosmo_sigma8(kh,pk,bounded: bool):
    from cosmoprimo import PowerSpectrumInterpolator1D
    kw={}
    if bounded:
        kw.update(extrap_kmin=float(kh[0]),extrap_kmax=float(kh[-1]))
    ip=PowerSpectrumInterpolator1D(np.asarray(kh,float),np.asarray(pk,float),**kw)
    return float(np.asarray(ip.sigma8()))


def _state_at_z(c,z: float,As: float,ns: float):
    tr=c.get_transfer(float(z),output_format="class")
    kh,db,dc,tb,tc=_clean_common(
        tr[_pick(tr,("k (h/Mpc)","k [h/Mpc]","k[h/Mpc]"))],
        tr["d_b"],tr["d_cdm"],tr["t_b"],tr["t_cdm"])
    Ob=r9b._omega(c,"Omega_b"); Oc=r9b._omega(c,"Omega_cdm")
    fb=Ob/(Ob+Oc); fc=1.0-fb
    dcb=fb*db+fc*dc; tcb=fb*tb+fc*tc
    Hconf=float(c.Hubble(float(z)))/(1.0+float(z))
    vcb=-tcb/Hconf
    h=float(c.h()); kmpc=kh*h
    primordial=As*(kmpc/KPIVOT)**(ns-1.0)
    pref=(2.0*np.pi**2/kmpc**3)*primordial
    pdd=pref*dcb**2*h**3; ptt=pref*vcb**2*h**3
    if np.any(~np.isfinite(pdd)) or np.any(~np.isfinite(ptt)) or np.any(pdd<=0) or np.any(ptt<=0):
        raise RuntimeError(f"nonpositive/nonfinite source power at z={z}")
    return {"z":float(z),"kh":kh,"db":db,"dc":dc,"tb":tb,"tc":tc,"dcb":dcb,"tcb":tcb,
            "pdd":pdd,"ptt":ptt,"fb":float(fb),"fc":float(fc),"Hconf":Hconf}


def _method_row(c,state):
    z=state["z"]; kh=state["kh"]; pdd=state["pdd"]; ptt=state["ptt"]
    si=float(c.sigma(8.0,z,h_units=True)); proxy=float(c.effective_f_sigma8(z,z_step=0.1))/si
    out={"z":z,"n_k":int(kh.size),"kh_min":float(kh[0]),"kh_max":float(kh[-1]),
         "sigma8_internal":si,"legacy_growth_proxy":proxy}
    for name,bounded in (("COSMO_DEFAULT",False),("COSMO_BOUNDED",True)):
        sdd=_cosmo_sigma8(kh,pdd,bounded); stt=_cosmo_sigma8(kh,ptt,bounded)
        out[name]={"sigma8_dd":sdd,"sigma8_tt":stt,"f":stt/sdd,
                   "rel_sigma8_vs_internal":rel(sdd,si),"rel_f_vs_proxy":rel(stt/sdd,proxy)}
    sdd=_loglinear_sigma8(kh,pdd); stt=_loglinear_sigma8(kh,ptt)
    out["LOGLINEAR_BOUNDED"]={"sigma8_dd":sdd,"sigma8_tt":stt,"f":stt/sdd,
                              "rel_sigma8_vs_internal":rel(sdd,si),"rel_f_vs_proxy":rel(stt/sdd,proxy)}
    return out


def _healthy(row,method):
    x=row[method]
    return bool(np.isfinite(x["sigma8_dd"]) and np.isfinite(x["sigma8_tt"]) and np.isfinite(x["f"])
                and 0.1<x["sigma8_dd"]<2.0 and 0.05<x["f"]<2.0
                and x["rel_sigma8_vs_internal"]<=REL_GATE and x["rel_f_vs_proxy"]<=REL_GATE)


def _widths(logk):
    n=len(logk); w=np.empty(n,float)
    w[0]=logk[1]-logk[0]; w[-1]=logk[-1]-logk[-2]
    if n>2: w[1:-1]=0.5*(logk[2:]-logk[:-2])
    return w


def _candidate_indices(states):
    kh0=states[0]["kh"]
    score=np.zeros(kh0.size,float)
    perz=[]
    for st in states:
        if st["kh"].shape!=kh0.shape or not np.allclose(st["kh"],kh0,rtol=0,atol=1e-14):
            raise RuntimeError("automatic transfer k grid differs across target redshifts")
        q=_widths(np.log(kh0))*kh0**3*st["ptt"]*_w2(8.0*kh0)
        total=float(np.sum(q))
        if not np.isfinite(total) or total<=0: raise RuntimeError("invalid contribution proxy")
        share=q/total; score=np.maximum(score,share)
        top=np.argsort(share)[::-1][:5]
        perz.append({"z":st["z"],"top":[{"index":int(i),"k_h":float(kh0[i]),"share":float(share[i]),
                                             "t_cb":float(st["tcb"][i])} for i in top]})
    core=np.argsort(score)[::-1][:N_TOP]
    idx=set()
    for i in core:
        for j in (int(i)-1,int(i),int(i)+1):
            if 0<=j<kh0.size: idx.add(j)
    idx=np.asarray(sorted(idx),int)
    if idx.size>24: raise RuntimeError(f"candidate expansion exceeded 24 modes: {idx.size}")
    return idx,score,perz


def _prepare_raw(raw):
    a=np.asarray(raw[_pick(raw,("a","scale factor"))],float)
    tb=np.asarray(raw[_pick(raw,("theta_b","t_b"))],float)
    tc=np.asarray(raw[_pick(raw,("theta_cdm","t_cdm"))],float)
    good=np.isfinite(a)&np.isfinite(tb)&np.isfinite(tc)&(a>0)
    a=a[good]; tb=tb[good]; tc=tc[good]
    order=np.argsort(a); a=a[order]; tb=tb[order]; tc=tc[order]
    keep=np.ones(a.size,dtype=bool)
    if a.size>1: keep[1:]=np.diff(a)>0
    a=a[keep]; tb=tb[keep]; tc=tc[keep]
    if a.size<4: raise RuntimeError("insufficient raw history")
    return a,tb,tc


def _run_stage_a():
    from classy import Class
    p=_base_params(); c=Class(); c.set(p); c.compute()
    try:
        As=float(p["A_s"]); ns=float(p["n_s"])
        states=[_state_at_z(c,float(z),As,ns) for z in ZEFF]
        rows=[_method_row(c,st) for st in states]
        idx,score,perz=_candidate_indices(states)
        internal=[{"z":float(z),"sigma8":float(c.sigma(8.0,float(z),h_units=True)),
                   "growth_proxy":float(c.effective_f_sigma8(float(z),z_step=0.1))/float(c.sigma(8.0,float(z),h_units=True))} for z in ZEFF]
        return p,states,rows,idx,score,perz,internal
    finally:
        c.struct_cleanup(); c.empty()


def _run_stage_b(candidate_kh,base_states):
    from classy import Class
    p=_base_params(candidate_kh); c=Class(); c.set(p); c.compute()
    try:
        pert=c.get_perturbations(); raws,container=d2a.scalar_histories(pert)
        if len(raws)!=len(candidate_kh):
            raise RuntimeError(f"expected {len(candidate_kh)} scalar histories, got {len(raws)}")
        prepared=[_prepare_raw(x) for x in raws]
        Ob=r9b._omega(c,"Omega_b"); Oc=r9b._omega(c,"Omega_cdm"); fb=Ob/(Ob+Oc); fc=1-fb
        raw_rerun_max=0.0; base_rerun_max=0.0; k_miss=0.0; rows=[]
        at=1.0/(1.0+ZEFF)
        for iz,z in enumerate(ZEFF):
            tr=c.get_transfer(float(z),output_format="class")
            kh=np.asarray(tr[_pick(tr,("k (h/Mpc)","k [h/Mpc]","k[h/Mpc]"))],float)
            tb_all=np.asarray(tr["t_b"],float); tc_all=np.asarray(tr["t_cdm"],float)
            base=base_states[iz]; scale=max(float(np.max(np.abs(base["tcb"]))),1e-300); floor=1e-12*scale
            rr=[]
            for i,target in enumerate(candidate_kh):
                j=int(np.argmin(np.abs(kh-target))); miss=abs(float(kh[j])-float(target))/float(target); k_miss=max(k_miss,miss)
                rtb=float(tb_all[j]); rtc=float(tc_all[j]); rtcb=float(fb*rtb+fc*rtc)
                a,htb,htc=prepared[i]
                rawtb=float(PchipInterpolator(a,htb,extrapolate=False)(at[iz])); rawtc=float(PchipInterpolator(a,htc,extrapolate=False)(at[iz])); rawtcb=float(fb*rawtb+fc*rawtc)
                jb=int(np.argmin(np.abs(base["kh"]-target))); bmiss=abs(float(base["kh"][jb])-float(target))/float(target)
                if bmiss>K_MATCH_GATE: raise RuntimeError(f"base candidate k mismatch {bmiss}")
                btb=float(base["tb"][jb]); btc=float(base["tc"][jb]); btcb=float(base["tcb"][jb])
                rawdiff=max(point_rel(rawtb,rtb,floor),point_rel(rawtc,rtc,floor),point_rel(rawtcb,rtcb,floor))
                basediff=max(point_rel(btb,rtb,floor),point_rel(btc,rtc,floor),point_rel(btcb,rtcb,floor))
                raw_rerun_max=max(raw_rerun_max,rawdiff); base_rerun_max=max(base_rerun_max,basediff)
                rr.append({"k_h":float(target),"base_tcb":btcb,"rerun_tcb":rtcb,"raw_tcb":rawtcb,
                           "base_vs_rerun":basediff,"raw_vs_rerun":rawdiff})
            rows.append({"z":float(z),"points":rr})
        internal=[{"z":float(z),"sigma8":float(c.sigma(8.0,float(z),h_units=True)),
                   "growth_proxy":float(c.effective_f_sigma8(float(z),z_step=0.1))/float(c.sigma(8.0,float(z),h_units=True))} for z in ZEFF]
        return {"container":container,"k_miss_max":float(k_miss),"raw_vs_rerun_max":float(raw_rerun_max),
                "base_vs_rerun_max":float(base_rerun_max),"rows":rows,"internal":internal}
    finally:
        c.struct_cleanup(); c.empty()


def _imap(rows): return {float(x["z"]):x for x in rows}


def main() -> int:
    outpath=ROOT/"results/stable_aest_desi_dr1_r9b2f_full_grid_rogue_node.json"
    print("STABLE_AEST_DESI_DR1_R9B2F_START",flush=True)
    prov=False; parent={}
    try:
        p=json.loads(R9B2E_JSON.read_text()); parent={"classification":p.get("classification"),"sha256":sha256(R9B2E_JSON)}
        prov=bool(all(ancestor(x) for x in (PREFIT_LOCK,R9B2E_POSTDATA_LOCK,R9B2E_REPAIR_PREFIT_LOCK,
                                            R9B2E_REPAIR_IMPL_LOCK,R9B2E_REPAIR_RUNNER_LOCK,R9B2D_POSTDATA_LOCK))
                  and sha256(R9B2E_JSON)==R9B2E_SHA256 and p.get("classification")==R9B2E_CLASS
                  and p.get("diagnostic_complete") is True and p.get("science_evaluated") is False)
    except Exception as exc:
        parent["error"]=repr(exc)
    if not prov:
        out={"classification":CLS_PROV,"diagnostic_complete":False,"science_evaluated":False,"parent":parent}
        outpath.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
        print("STABLE_AEST_DESI_DR1_R9B2F_CLASSIFICATION="+CLS_PROV,flush=True); return 3
    try:
        print("STABLE_AEST_DESI_DR1_R9B2F_STAGE=A_FULL_DEFAULT_GRID",flush=True)
        params,states,rows,idx,score,perz,internal_a=_run_stage_a()
        candidate_kh=states[0]["kh"][idx]
        print("STABLE_AEST_DESI_DR1_R9B2F_CANDIDATES="+json.dumps([float(x) for x in candidate_kh]),flush=True)
        print("STABLE_AEST_DESI_DR1_R9B2F_STAGE=B_EXACT_K_RAW_RERUN",flush=True)
        stageb=_run_stage_b(candidate_kh,states)
    except Exception as exc:
        out={"classification":CLS_RUN,"diagnostic_complete":False,"science_evaluated":False,"error":repr(exc),"parent":parent}
        outpath.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
        print(f"STABLE_AEST_DESI_DR1_R9B2F_RUN_FAIL error={exc!r}",flush=True)
        print("STABLE_AEST_DESI_DR1_R9B2F_CLASSIFICATION="+CLS_RUN,flush=True); return 2

    pathology=any((r["COSMO_DEFAULT"]["f"]>2.0 or r["COSMO_DEFAULT"]["rel_f_vs_proxy"]>=MATERIAL_GATE) for r in rows)
    bounded_healthy=all(_healthy(r,"COSMO_BOUNDED") for r in rows)
    linear_healthy=all(_healthy(r,"LOGLINEAR_BOUNDED") for r in rows)
    default_bounded=max(rel(r["COSMO_DEFAULT"]["f"],r["COSMO_BOUNDED"]["f"]) for r in rows)
    bounded_linear=max(rel(r["COSMO_BOUNDED"]["f"],r["LOGLINEAR_BOUNDED"]["f"]) for r in rows)
    ia=_imap(internal_a); ib=_imap(stageb["internal"]); intdiff={"sigma8":0.0,"growth_proxy":0.0}
    for z in ia:
        intdiff["sigma8"]=max(intdiff["sigma8"],rel(ia[z]["sigma8"],ib[z]["sigma8"]))
        intdiff["growth_proxy"]=max(intdiff["growth_proxy"],rel(ia[z]["growth_proxy"],ib[z]["growth_proxy"]))
    raw_ok=bool(stageb["raw_vs_rerun_max"]<=RAW_TRANSFER_GATE and stageb["k_miss_max"]<=K_MATCH_GATE)
    int_ok=bool(max(intdiff.values())<=REL_GATE)
    base_rerun_material=bool(stageb["base_vs_rerun_max"]>=MATERIAL_GATE)

    if pathology and bounded_healthy and default_bounded>=MATERIAL_GATE:
        classification=CLS_EXTRAP
    elif pathology and (not bounded_healthy) and linear_healthy and bounded_linear>=MATERIAL_GATE:
        classification=CLS_INTERP
    elif pathology and (not linear_healthy) and raw_ok and int_ok and base_rerun_material:
        classification=CLS_ROGUE
    else:
        classification=CLS_UNRES

    gates={
        "R9B2F_F1_provenance":True,
        "R9B2F_F2_historical_pathology_reproduced":bool(pathology),
        "R9B2F_F3_cosmo_bounded_healthy":bool(bounded_healthy),
        "R9B2F_F4_loglinear_bounded_healthy":bool(linear_healthy),
        "R9B2F_F5_exact_k_raw_transfer_closure":bool(raw_ok),
        "R9B2F_F6_internal_solution_invariance":bool(int_ok),
        "R9B2F_F7_automatic_vs_exact_k_material_discrepancy":bool(base_rerun_material),
    }
    metrics={
        "rel_gate":REL_GATE,"raw_transfer_gate":RAW_TRANSFER_GATE,"material_gate":MATERIAL_GATE,
        "n_automatic_k":int(states[0]["kh"].size),"automatic_k_min":float(states[0]["kh"][0]),"automatic_k_max":float(states[0]["kh"][-1]),
        "n_candidate_k":int(candidate_kh.size),"candidate_k_h":[float(x) for x in candidate_kh],
        "max_rel_f_default_vs_bounded":float(default_bounded),"max_rel_f_bounded_vs_loglinear":float(bounded_linear),
        "exact_k_raw_vs_rerun_transfer_max":stageb["raw_vs_rerun_max"],
        "automatic_vs_exact_k_transfer_max":stageb["base_vs_rerun_max"],
        "exact_k_transfer_k_miss_max":stageb["k_miss_max"],"internal_stageA_vs_stageB":intdiff,
    }
    out={"classification":classification,"diagnostic_complete":True,"science_evaluated":False,"desi_data_loaded":False,
         "gates":gates,"metrics":metrics,"parent":parent,"stageA_rows":rows,
         "candidate_selection":{"core_top8_indices":[int(x) for x in np.argsort(score)[::-1][:N_TOP]],
                                "expanded_indices":[int(x) for x in idx],"score":[float(x) for x in score],"top_by_z":perz},
         "stageB":stageb,
         "interpretation":{"historical_failures_reclassified":False,"desi_detection_claim_licensed":False,
                           "localized_mechanism":({CLS_EXTRAP:"high_k_extrapolation",CLS_INTERP:"power_interpolation",CLS_ROGUE:"automatic_kgrid_rogue_node"}.get(classification,"unresolved"))}}
    outpath.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print("STABLE_AEST_DESI_DR1_R9B2F_GATES="+json.dumps(gates,sort_keys=True),flush=True)
    print("STABLE_AEST_DESI_DR1_R9B2F_METRICS="+json.dumps(metrics,sort_keys=True),flush=True)
    print("STABLE_AEST_DESI_DR1_R9B2F_CLASSIFICATION="+classification,flush=True)
    return 0 if classification in (CLS_EXTRAP,CLS_INTERP,CLS_ROGUE) else 1


if __name__ == "__main__":
    raise SystemExit(main())
