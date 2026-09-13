#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys

import numpy as np
from scipy.interpolate import CubicSpline, PchipInterpolator

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fullj_weyl import corrected_class_spectral_fringe_gr_control as base
from fullj_weyl import corrected_class_spectral_fringe_gr_control_r3 as r3
from fullj_weyl import spectral_fringe_source_decomposition as sd

PREDATA_LOCK = "82d6f80495f9b3265c4cd949e573a39abea69df3"
EXTRACTOR_JSON = ROOT / "results/fullj_corrected_class_spectral_fringe_extractor_equivalence.json"
EXTRACTOR_NPZ = ROOT / "results/fullj_corrected_class_spectral_fringe_extractor_equivalence.npz"
R3_JSON = ROOT / "results/fullj_corrected_class_spectral_fringe_gr_control.json"
R3_NPZ = ROOT / "results/fullj_corrected_class_spectral_fringe_gr_control.npz"

INCOMPLETE = "FULLJ_CLASS_FRINGE_BRIDGE_IDENTITY_INCOMPLETE"
KLIST = "FULLJ_CLASS_FRINGE_BRIDGE_KLIST_DEPENDENCE"
PARAM = "FULLJ_CLASS_FRINGE_BRIDGE_PARAMETER_DEPENDENCE"
HISTORY = "FULLJ_CLASS_FRINGE_BRIDGE_HISTORY_MAPPING_DEFECT"
TIME = "FULLJ_CLASS_FRINGE_BRIDGE_TIME_MAPPING_DEFECT"
BASIS = "FULLJ_CLASS_FRINGE_BRIDGE_BASIS_EXTRACTION_DEFECT"
NO_TECH = "FULLJ_CLASS_FRINGE_BRIDGE_TECHNICAL_CAUSE_NOT_FOUND"

GLOBAL_GATE = 2.0e-5
PERK_GATE = 5.0e-5
K_REPORT_GATE = 5.0e-12
MATERIAL_GATE = 2.0e-5


def is_ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"],
        cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    ).returncode == 0


def rel(a, b) -> float:
    aa = np.asarray(a, complex); bb = np.asarray(b, complex)
    return float(np.linalg.norm(aa-bb) / max(float(np.linalg.norm(aa)), float(np.linalg.norm(bb)), 1e-300))


def per_k_rel(a, b):
    return [rel(np.asarray(a)[i], np.asarray(b)[i]) for i in range(np.asarray(a).shape[0])]


def clean_xy(x, y):
    x=np.asarray(x,float); y=np.asarray(y,float)
    order=np.argsort(x); x=x[order]; y=y[order]
    finite=np.isfinite(x)&np.isfinite(y); x=x[finite]; y=y[finite]
    keep=np.ones(x.size,dtype=bool)
    if x.size>1: keep[1:]=np.diff(x)>0
    x=x[keep]; y=y[keep]
    if x.size<8 or np.any(np.diff(x)<=0):
        raise RuntimeError("insufficient/nonmonotone history coordinate")
    return x,y


def history_keys(raw):
    akey=base.d2a.pick(raw,"a",("scale factor",))
    tkey=base.d2a.pick(raw,"tau [Mpc]",("tau","tau[Mpc]"))
    pkey=base.d2a.pick(raw,"phi")
    skey=base.d2a.pick(raw,"psi")
    return akey,tkey,pkey,skey


def reported_kh(raw):
    candidates=(
        ("k (h/Mpc)",1.0),("k [h/Mpc]",1.0),("k[h/Mpc]",1.0),
        ("k (1/Mpc)",1.0/base.cb.h),("k [1/Mpc]",1.0/base.cb.h),("k[1/Mpc]",1.0/base.cb.h),
    )
    for key,factor in candidates:
        if key in raw:
            a=np.asarray(raw[key],float).ravel()
            a=a[np.isfinite(a)]
            if a.size==0:
                continue
            spread=float(np.max(np.abs(a-a[0])))
            if spread>1e-10*max(abs(float(a[0])),1.0):
                raise RuntimeError(f"reported k key {key} is not constant")
            return float(a[0])*factor,key
    # CLASS documentation says perturbation histories carry k(h/Mpc). Be strict if absent.
    raise RuntimeError(f"history has no recognized reported-k key; available={sorted(raw.keys())}")


def eval_at_a(raw, z):
    akey,tkey,pkey,skey=history_keys(raw)
    aa=np.asarray(raw[akey],float)
    ww=np.asarray(raw[pkey],float)+np.asarray(raw[skey],float)
    ax,wy=clean_xy(aa,ww)
    sp=CubicSpline(ax,wy,bc_type="not-a-knot")
    at=1.0/(1.0+np.asarray(z,float))
    vals=np.asarray(sp(at),float)
    if not np.all(np.isfinite(vals)):
        raise RuntimeError("nonfinite a-coordinate evaluation")
    return vals


def target_tau_from_history(raw,z):
    akey,tkey,_,_=history_keys(raw)
    aa=np.asarray(raw[akey],float); tt=np.asarray(raw[tkey],float)
    ax,ty=clean_xy(aa,tt)
    sp=PchipInterpolator(ax,ty,extrapolate=False)
    at=1.0/(1.0+np.asarray(z,float))
    vals=np.asarray(sp(at),float)
    if not np.all(np.isfinite(vals)):
        raise RuntimeError("nonfinite target tau")
    return vals


def bridge_tau_from_first_history(histories,z):
    return target_tau_from_history(histories[0],z)


def eval_at_tau(raw,tau):
    akey,tkey,pkey,skey=history_keys(raw)
    tt=np.asarray(raw[tkey],float)
    ww=np.asarray(raw[pkey],float)+np.asarray(raw[skey],float)
    tx,wy=clean_xy(tt,ww)
    sp=CubicSpline(tx,wy,bc_type="not-a-knot")
    vals=np.asarray(sp(np.asarray(tau,float)),float)
    if not np.all(np.isfinite(vals)):
        raise RuntimeError("nonfinite tau-coordinate evaluation")
    return vals


def a_at_tau(raw,tau):
    akey,tkey,_,_=history_keys(raw)
    tt=np.asarray(raw[tkey],float); aa=np.asarray(raw[akey],float)
    tx,ay=clean_xy(tt,aa)
    sp=CubicSpline(tx,ay,bc_type="not-a-knot")
    vals=np.asarray(sp(np.asarray(tau,float)),float)
    if not np.all(np.isfinite(vals)):
        raise RuntimeError("nonfinite a(tau)")
    return vals


def r3_params(kh):
    p=dict(base.cb.build_params())
    p.update({
        "output":"mTk,vTk","lensing":"no","P_k_max_h/Mpc":0.30,"z_max_pk":6.5,
        "aest_memory_enabled":"no","aest_eta":0.0,"aest_enabled":"yes",
    })
    p.pop("l_max_scalars",None)
    text,meta=r3.serialize_requested_k(np.asarray(kh,float))
    p["k_output_values"]=text
    return p,meta


def bridge_params(mode_h):
    old_mpc=np.asarray(sd.m.K_MPC,float).copy(); old_h=np.asarray(getattr(sd.m,"K_H",[]),float).copy()
    try:
        sd.m.K_H=np.asarray(mode_h,float).copy()
        sd.m.K_MPC=np.asarray(mode_h,float)*float(sd.static.h)
        p=dict(sd.m.build_params())
    finally:
        sd.m.K_MPC=old_mpc
        if old_h.size: sd.m.K_H=old_h
    return p


def run_histories(pars):
    from classy import Class
    c=Class(); c.set(pars); c.compute()
    try:
        pert=c.get_perturbations()
        histories,_=base.d2a.scalar_histories(pert)
        copied=[]
        for raw in histories:
            copied.append({k:np.asarray(v).copy() if hasattr(v,"__len__") and not isinstance(v,(str,bytes)) else v for k,v in raw.items()})
        return copied
    finally:
        c.struct_cleanup(); c.empty()


def target_by_reported_k(histories,target):
    vals=[]
    for i,raw in enumerate(histories):
        kh,key=reported_kh(raw); vals.append((i,kh,key))
    dist=np.asarray([abs(v[1]-float(target)) for v in vals],float)
    j=int(np.argmin(dist))
    if dist[j]>K_REPORT_GATE:
        raise RuntimeError(f"no returned history matches target {target}; reported={[(x[0],x[1]) for x in vals]}")
    return j, vals


def normalized_param_diff(a,b):
    ignore={"k_output_values","P_k_max_h/Mpc"}
    keys=sorted((set(a)|set(b))-ignore)
    out={}
    for k in keys:
        av=a.get(k,"<MISSING>"); bv=b.get(k,"<MISSING>")
        if str(av)!=str(bv): out[k]={"r3":str(av),"bridge":str(bv)}
    return out


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--json-out",default="results/fullj_corrected_class_spectral_fringe_bridge_identity.json")
    ap.add_argument("--npz-out",default="results/fullj_corrected_class_spectral_fringe_bridge_identity.npz")
    args=ap.parse_args()

    print("FULLJ_CLASS_FRINGE_BRIDGE_IDENTITY_START",flush=True)
    for p in (EXTRACTOR_JSON,EXTRACTOR_NPZ,R3_JSON,R3_NPZ):
        if not p.exists():
            out={"classification":INCOMPLETE,"diagnostic_complete":False,"reason":f"missing {p}"}
            Path(args.json_out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
            print("FULLJ_CLASS_FRINGE_BRIDGE_IDENTITY_CLASSIFICATION="+INCOMPLETE,flush=True)
            return 3

    ej=json.loads(EXTRACTOR_JSON.read_text()); eq=np.load(EXTRACTOR_NPZ)
    rj=json.loads(R3_JSON.read_text()); rq=np.load(R3_NPZ)
    anchors=np.asarray(base.K_ANCHOR,float); z=np.asarray(base.CHECK_Z,float)
    B0=np.asarray(rq["aest_sparse_W"],float)
    B5=np.asarray(eq["E3_bridge_tagged"],complex)

    frozen=bool(
        is_ancestor(PREDATA_LOCK)
        and ej.get("classification")=="FULLJ_CLASS_FRINGE_EXTRACTOR_MISMATCH_CERTIFIED"
        and ej.get("interpretation",{}).get("historical_R3_reclassified") is False
        and rj.get("classification")=="FULLJ_CORRECTED_CLASS_SPECTRAL_FRINGE_NUMERICAL_CONTROL_FAIL"
        and np.allclose(np.asarray(rq["k_anchor_h_Mpc"],float),anchors,rtol=0,atol=5e-13)
        and np.allclose(np.asarray(rq["redshifts"],float),z,rtol=0,atol=5e-13)
        and B0.shape==(15,9) and B5.shape==(15,9)
    )

    B1=np.full_like(B0,np.nan); B2=np.full_like(B0,np.nan); B3=np.full_like(B0,np.nan); B4=np.full_like(B0,np.nan)
    reported_rows=[]; tau_offsets=[]; a_offsets=[]; param_diffs={}
    positional_k_ok=True

    for ik,kh in enumerate(anchors):
        mode_h=np.asarray(sd.poc.target_modes(float(kh)),float)
        target_pos=int(np.where(np.isclose(mode_h,float(kh),rtol=0,atol=5e-13))[0][0])

        p1,serial=r3_params(mode_h)
        h1=run_histories(p1)
        j1,rep1=target_by_reported_k(h1,float(kh))
        B1[ik]=eval_at_a(h1[j1],z)

        p2=bridge_params(mode_h)
        h2=run_histories(p2)
        j2,rep2=target_by_reported_k(h2,float(kh))
        B2[ik]=eval_at_a(h2[j2],z)
        if target_pos>=len(h2):
            raise RuntimeError(f"historical positional index {target_pos} outside returned histories {len(h2)}")
        B3[ik]=eval_at_a(h2[target_pos],z)

        bridge_tau=bridge_tau_from_first_history(h2,z)
        target_tau=target_tau_from_history(h2[j2],z)
        B4[ik]=eval_at_tau(h2[j2],bridge_tau)
        atarget=1.0/(1.0+z)
        abridge=a_at_tau(h2[j2],bridge_tau)
        tau_offsets.append(float(np.max(np.abs(bridge_tau-target_tau))))
        a_offsets.append(float(np.max(np.abs(abridge-atarget))))

        pos_k,pos_key=reported_kh(h2[target_pos])
        pos_ok=bool(abs(pos_k-float(kh))<=K_REPORT_GATE)
        positional_k_ok=positional_k_ok and pos_ok
        param_diffs[f"{kh:.5f}"]=normalized_param_diff(p1,p2)
        reported_rows.append({
            "k_h":float(kh),"bridge_list_h":mode_h.tolist(),"target_pos":target_pos,
            "r3_reported":[{"index":int(i),"k_h":float(k),"key":key} for i,k,key in rep1],
            "bridge_reported":[{"index":int(i),"k_h":float(k),"key":key} for i,k,key in rep2],
            "matched_index_r3":int(j1),"matched_index_bridge":int(j2),
            "positional_reported_k_h":float(pos_k),"positional_k_ok":pos_ok,
            "serialization_chars":int(serial["string_length"]),
        })
        print(f"FULLJ_CLASS_FRINGE_BRIDGE_IDENTITY_RUN {ik+1:02d}/15 k_h={kh:.5f} n={len(mode_h)} match_r3={j1} match_bridge={j2} pos={target_pos} pos_k={pos_k:.8f}",flush=True)

    def cmp(a,b):
        pp=per_k_rel(a,b); return rel(a,b),float(max(pp)),pp
    e10,m10,p10=cmp(B1,B0)
    e21,m21,p21=cmp(B2,B1)
    e32,m32,p32=cmp(B3,B2)
    e42,m42,p42=cmp(B4,B2)
    e54,m54,p54=cmp(B5,B4)
    e50,m50,p50=cmp(B5,B0)
    unexpected={k:v for k,v in param_diffs.items() if v}

    g1=bool(frozen and all(np.all(np.isfinite(x)) for x in (B0,B1,B2,B3,B4,B5)))
    g2=bool(e10<=GLOBAL_GATE and m10<=PERK_GATE)
    g3=bool(e21<=GLOBAL_GATE and m21<=PERK_GATE and len(unexpected)==0)
    g4=bool(positional_k_ok and e32<=GLOBAL_GATE and m32<=PERK_GATE)
    g5=bool(e42<=GLOBAL_GATE and m42<=PERK_GATE)
    g6=bool(e54<=GLOBAL_GATE and m54<=PERK_GATE)
    material=bool(e50>MATERIAL_GATE or m50>PERK_GATE)

    if not g1:
        classification=INCOMPLETE
    elif not g2:
        classification=KLIST
    elif not g3:
        classification=PARAM
    elif not g4:
        classification=HISTORY
    elif not g5:
        classification=TIME
    elif not g6:
        classification=BASIS
    elif material:
        classification=NO_TECH
    else:
        classification=INCOMPLETE

    gates={
        "BI_G1_provenance_and_frozen_identity":g1,
        "BI_G2_bridge_list_invariance_direct_params":g2,
        "BI_G3_parameter_construction_identity":g3,
        "BI_G4_history_order_identity":g4,
        "BI_G5_bridge_time_coordinate_identity":g5,
        "BI_G6_basis_fourier_extraction_identity":g6,
    }
    summary={
        "B1_vs_B0_global_relative_L2":e10,"B1_vs_B0_per_k_max":m10,
        "B2_vs_B1_global_relative_L2":e21,"B2_vs_B1_per_k_max":m21,
        "B3_vs_B2_global_relative_L2":e32,"B3_vs_B2_per_k_max":m32,
        "B4_vs_B2_global_relative_L2":e42,"B4_vs_B2_per_k_max":m42,
        "B5_vs_B4_global_relative_L2":e54,"B5_vs_B4_per_k_max":m54,
        "B5_vs_B0_global_relative_L2":e50,"B5_vs_B0_per_k_max":m50,
        "positional_k_all_ok":bool(positional_k_ok),
        "max_bridge_tau_offset_Mpc":float(max(tau_offsets)),
        "max_bridge_a_offset":float(max(a_offsets)),
        "unexpected_parameter_diff_anchor_count":int(len(unexpected)),
        "unexpected_parameter_differences":unexpected,
    }
    out={
        "classification":classification,"diagnostic_complete":True,"frozen_setup":frozen,
        "gates":gates,"summary":summary,"reported_histories":reported_rows,
        "thresholds":{"global":GLOBAL_GATE,"per_k":PERK_GATE,"reported_k_abs_h_Mpc":K_REPORT_GATE},
        "interpretation":{
            "historical_R3_reclassified":False,"extractor_mismatch_reclassified":False,
            "equation_level_discrepancy_followup_licensed":bool(classification==NO_TECH),
            "new_physics_claim_licensed":False,
        },
    }
    Path(args.json_out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    np.savez_compressed(args.npz_out,anchors=anchors,redshifts=z,B0_locked_R3_direct=B0,
                        B1_direct_params_bridge_list=B1,B2_bridge_params_actual_k=B2,
                        B3_bridge_params_positional=B3,B4_bridge_tau_actual_k=B4,
                        B5_locked_bridge_tagged=B5)
    print("FULLJ_CLASS_FRINGE_BRIDGE_IDENTITY_SUMMARY="+json.dumps(summary,sort_keys=True),flush=True)
    print("FULLJ_CLASS_FRINGE_BRIDGE_IDENTITY_GATES="+json.dumps(gates,sort_keys=True),flush=True)
    print("FULLJ_CLASS_FRINGE_BRIDGE_IDENTITY_CLASSIFICATION="+classification,flush=True)
    return 0 if classification!=INCOMPLETE else 1

if __name__=="__main__":
    raise SystemExit(main())
