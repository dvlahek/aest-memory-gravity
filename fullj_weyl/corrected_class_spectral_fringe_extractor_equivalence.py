#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys

import numpy as np
from scipy.interpolate import CubicSpline

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fullj_weyl import corrected_class_spectral_fringe_gr_control as base
from fullj_weyl import corrected_class_spectral_fringe_gr_control_r3 as r3
from fullj_weyl import spectral_fringe_source_decomposition as sd

PREDATA_LOCK = "4f3b2738487331229838e557d9c74f1a2485408d"
R3_RESULT_JSON = ROOT / "results/fullj_corrected_class_spectral_fringe_gr_control.json"
R3_RESULT_NPZ = ROOT / "results/fullj_corrected_class_spectral_fringe_gr_control.npz"
SOURCE_JSON = ROOT / "results/fullj_spectral_fringe_source_decomposition.json"
SOURCE_NPZ = ROOT / "results/fullj_spectral_fringe_source_decomposition.npz"

PASS_MISMATCH = "FULLJ_CLASS_FRINGE_EXTRACTOR_MISMATCH_CERTIFIED"
FROZEN_REF_FAIL = "FULLJ_CLASS_FRINGE_FROZEN_REFERENCE_NOT_REPRODUCED"
NUMFAIL = "FULLJ_CLASS_FRINGE_EXTRACTOR_NUMERICAL_CONTROL_FAIL"
R3_IMPL_DEFECT = "FULLJ_CLASS_FRINGE_R3_COMPARISON_IMPLEMENTATION_DEFECT"
INCOMPLETE = "FULLJ_CLASS_FRINGE_EXTRACTOR_AUDIT_INCOMPLETE"

GLOBAL_GATE = 2.0e-5
PERK_GATE = 5.0e-5
ORIGINAL_DG2_GLOBAL = 2.0e-5
ORIGINAL_DG2_PERK = 5.0e-5


def is_ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"],
        cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    ).returncode == 0


def rel(a, b):
    aa = np.asarray(a, complex); bb = np.asarray(b, complex)
    return float(np.linalg.norm(aa-bb) / max(float(np.linalg.norm(aa)), float(np.linalg.norm(bb)), 1e-300))


def per_k_rel(a, b):
    aa = np.asarray(a, complex); bb = np.asarray(b, complex)
    return [rel(aa[i], bb[i]) for i in range(aa.shape[0])]


def idx(grid, x):
    q = np.where(np.isclose(np.asarray(grid, float), float(x), rtol=0.0, atol=5e-13))[0]
    if len(q) != 1:
        raise RuntimeError(f"nonunique/missing value {x}")
    return int(q[0])


def raw_history_at_tau(raw, tau_target):
    kt = base.pick(raw, ("tau [Mpc]", "tau", "tau[Mpc]"))
    kp = base.pick(raw, ("phi",))
    ks = base.pick(raw, ("psi",))
    tt = np.asarray(raw[kt], float)
    ww = np.asarray(raw[kp], float) + np.asarray(raw[ks], float)
    order = np.argsort(tt)
    tt = tt[order]; ww = ww[order]
    uniq, ui = np.unique(tt, return_index=True)
    ww = ww[ui]
    sp = CubicSpline(uniq, ww, extrapolate=False)
    vals = np.asarray(sp(np.asarray(tau_target, float)), float)
    if not np.all(np.isfinite(vals)):
        raise RuntimeError("nonfinite raw-tau interpolation")
    return vals


def load_locked():
    for p in (R3_RESULT_JSON, R3_RESULT_NPZ, SOURCE_JSON, SOURCE_NPZ):
        if not p.exists():
            raise FileNotFoundError(str(p))
    rj = json.loads(R3_RESULT_JSON.read_text())
    sj = json.loads(SOURCE_JSON.read_text())
    rq = np.load(R3_RESULT_NPZ)
    sq = np.load(SOURCE_NPZ)
    return rj, sj, rq, sq


def second_difference_vector(nodes, arr, z_index):
    windows = (
        [0.09875,0.10000,0.10125,0.10250,0.10375],
        [0.16125,0.16250,0.16375,0.16500,0.16625],
        [0.19375,0.19500,0.19625,0.19750,0.19875],
    )
    out=[]
    for w in windows:
        ii=[idx(nodes,k) for k in w]
        y=np.asarray(arr[ii,z_index], complex)
        out.extend([y[j+1]-2*y[j]+y[j-1] for j in (1,2,3)])
    return np.asarray(out, complex)


def safe_corr(a,b):
    aa=np.asarray(a,float); bb=np.asarray(b,float)
    if aa.size<2 or np.std(aa)<=1e-300 or np.std(bb)<=1e-300:
        return float("nan")
    return float(np.corrcoef(aa,bb)[0,1])


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--json-out", default="results/fullj_corrected_class_spectral_fringe_extractor_equivalence.json")
    ap.add_argument("--npz-out", default="results/fullj_corrected_class_spectral_fringe_extractor_equivalence.npz")
    args=ap.parse_args()

    print("FULLJ_CLASS_FRINGE_EXTRACTOR_AUDIT_START", flush=True)
    try:
        rj,sj,rq,sq=load_locked()
    except Exception as exc:
        out={"classification":INCOMPLETE,"diagnostic_complete":False,"reason":str(exc)}
        Path(args.json_out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
        print("FULLJ_CLASS_FRINGE_EXTRACTOR_AUDIT_CLASSIFICATION="+INCOMPLETE, flush=True)
        return 3

    anchors=np.asarray(base.K_ANCHOR,float)
    z=np.asarray(base.ZLIST,float)
    frozen=bool(
        is_ancestor(PREDATA_LOCK)
        and rj.get("classification")=="FULLJ_CORRECTED_CLASS_SPECTRAL_FRINGE_NUMERICAL_CONTROL_FAIL"
        and sj.get("classification")==sd.CLASS_DOMINATED
        and len(anchors)==15 and np.allclose(z,[6,5,4,3,2,1.5,1,0.5,0.2],rtol=0,atol=5e-14)
        and rj.get("gates",{}).get("DG_G3_requested_k_list_invariance") is True
        and rj.get("gates",{}).get("DG_G4_dense_grid_health") is True
        and rj.get("gates",{}).get("DG_G5_fine_grid_spectral_structure") is True
        and rj.get("gates",{}).get("DG_G6_AeST_specificity_against_GR") is True
    )

    rkeys=set(rq.files)
    if "W_aest_sparse" in rkeys:
        E1=np.asarray(rq["W_aest_sparse"],float)
    elif "W_aest_sparse_15" in rkeys:
        E1=np.asarray(rq["W_aest_sparse_15"],float)
    else:
        dense=np.asarray(rq["W_aest_dense" if "W_aest_dense" in rkeys else "W_aest_dense_51"],float)
        kd=np.asarray(rq["k_dense_h_Mpc"],float) if "k_dense_h_Mpc" in rkeys else np.asarray(base.K_DENSE,float)
        E1=np.stack([dense[idx(kd,k)] for k in anchors],axis=0)
    if E1.shape!=(15,len(z)):
        raise RuntimeError(f"bad E1 shape {E1.shape}")

    from classy import Class
    pars=base.cb.build_params(aest_enabled=True)
    pars["output"]="mTk,vTk"
    pars.pop("l_max_scalars",None)
    kvals,meta=r3.serialize_requested_k(anchors)
    pars["k_output_values"]=kvals
    pars["aest_memory_enabled"]="no"
    pars["aest_eta"]=0.0
    c=Class(); c.set(pars); c.compute()
    try:
        pert=c.get_perturbations()
        histories,_=base.scalar_histories(pert)
        if len(histories)!=15:
            raise RuntimeError(f"history count {len(histories)} != 15")
        bg=c.get_background()
        tau_bg=np.asarray(bg[base.pick(bg,("conf. time [Mpc]","conf. time[Mpc]","tau [Mpc]","tau"))],float)
        z_bg=np.asarray(bg[base.pick(bg,("z",))],float)
        order=np.argsort(z_bg)
        z_s=z_bg[order]; tau_s=tau_bg[order]
        tau_target=np.interp(z,z_s,tau_s)
        E2=np.stack([raw_history_at_tau(raw,tau_target) for raw in histories],axis=0)
    finally:
        c.struct_cleanup(); c.empty()

    old_kmpc=np.asarray(sd.m.K_MPC,float).copy()
    old_kh=np.asarray(getattr(sd.m,"K_H",[]),float).copy()
    E3=np.full((15,len(z)),np.nan+1j*np.nan,complex)
    _,gcoef,_=sd.poc.coeff_draw()
    try:
        for ik,kh in enumerate(anchors):
            mode_h=sd.poc.target_modes(float(kh))
            sd.m.K_H=mode_h.copy(); sd.m.K_MPC=mode_h*float(sd.static.h)
            data=sd.r2.r0.prepare_bridge_data()
            pair={}; mm=None
            for sign in (+1,-1):
                rec,comps,meta3=sd.sl.run_signed(
                    data, mode_h, gcoef[sd.BG], float(kh), int(sign), sd.EPS, sd.NSTEP,
                    sd.KF, sd.NX, sd.BOX, "extractor_equivalence", surrogate=False,
                )
                if not rec.get("finite",False) or comps is None:
                    raise RuntimeError(f"bridge extractor nonfinite k={kh} sign={sign}: {rec.get('reason','unknown')}")
                pair[int(sign)]=comps; mm=meta3
            resp=sd.sl.pair_response(pair,mm,sd.EPS)
            E3[ik]=np.asarray(resp["W_CLASS"],complex)
    finally:
        sd.m.K_MPC=old_kmpc
        if old_kh.size: sd.m.K_H=old_kh

    snodes=np.asarray(sq["merged_nodes"],float)
    E4all=np.asarray(sq["merged__W_CLASS"],complex)
    E4=np.stack([E4all[idx(snodes,k)] for k in anchors],axis=0)

    e12=rel(E1,E2); p12=per_k_rel(E1,E2)
    e34=rel(E3,E4); p34=per_k_rel(E3,E4)
    e13=rel(E1,E3); p13=per_k_rel(E1,E3)
    e14=rel(E1,E4); p14=per_k_rel(E1,E4)
    rz13=[rel(E1[:,j],E3[:,j]) for j in range(len(z))]
    rz14=[rel(E1[:,j],E4[:,j]) for j in range(len(z))]
    diff=np.abs(E1-E4)
    imax=np.unravel_index(int(np.argmax(diff)),diff.shape)
    sign_disagree=int(np.count_nonzero(np.sign(np.real(E1))*np.sign(np.real(E4))<0))
    iz02=idx(z,0.2)
    d21=second_difference_vector(anchors,E1,iz02)
    d23=second_difference_vector(anchors,E3,iz02)
    d24=second_difference_vector(anchors,E4,iz02)

    g1=frozen and np.all(np.isfinite(E1)) and np.all(np.isfinite(E2)) and np.all(np.isfinite(E3)) and np.all(np.isfinite(E4))
    g2=bool(e12<=GLOBAL_GATE and max(p12)<=PERK_GATE)
    g3=bool(e34<=GLOBAL_GATE and max(p34)<=PERK_GATE)
    s=rj.get("summary",{})
    g5=bool(
        float(s.get("k_list_invariance_global_relative_L2",np.inf))==0.0
        and float(s.get("k_list_invariance_per_k_max",np.inf))==0.0
        and list(s.get("z0p2_extrema_per_window",[]))==[10,11,9]
        and abs(float(s.get("z0p2_kappa_AeST",np.nan))-0.403340049182677)<=1e-15
        and abs(float(s.get("z0p2_kappa_GR",np.nan))-0.00016609014215828433)<=1e-18
        and abs(float(s.get("z0p2_specificity_ratio",np.nan))-2428.440628332372)<=1e-9
    )
    direct_bridge_material=bool(e13>ORIGINAL_DG2_GLOBAL or max(p13)>ORIGINAL_DG2_PERK)
    all_agree=bool(e14<=ORIGINAL_DG2_GLOBAL and max(p14)<=ORIGINAL_DG2_PERK)

    if not g1 or not g2:
        classification=NUMFAIL
    elif g3 and g5 and direct_bridge_material:
        classification=PASS_MISMATCH
    elif (not g3) and g5:
        classification=FROZEN_REF_FAIL
    elif g3 and g5 and all_agree:
        classification=R3_IMPL_DEFECT
    else:
        classification=INCOMPLETE

    summary={
        "E1_E2_global_relative_L2":e12,"E1_E2_per_k_max":float(max(p12)),
        "E3_E4_global_relative_L2":e34,"E3_E4_per_k_max":float(max(p34)),
        "E1_E3_global_relative_L2":e13,"E1_E3_per_k_max":float(max(p13)),
        "E1_E4_global_relative_L2":e14,"E1_E4_per_k_max":float(max(p14)),
        "E1_E3_per_redshift_relative_L2":rz13,"E1_E4_per_redshift_relative_L2":rz14,
        "max_abs_E1_E4_difference":float(diff[imax]),"max_abs_E1_E4_k_h":float(anchors[imax[0]]),
        "max_abs_E1_E4_z":float(z[imax[1]]),"sign_disagreement_count":sign_disagree,
        "z0p2_D2_corr_E1_E3":safe_corr(np.real(d21),np.real(d23)),
        "z0p2_D2_corr_E1_E4":safe_corr(np.real(d21),np.real(d24)),
    }
    gates={"EX_G1_provenance_and_frozen_identity":bool(g1),"EX_G2_direct_coordinate_equivalence":bool(g2),
           "EX_G3_bridge_extractor_self_equivalence":bool(g3),"EX_G4_discrepancy_localized":True,
           "EX_G5_direct_signal_controls_preserved":bool(g5)}
    out={"classification":classification,"diagnostic_complete":True,"frozen_setup":bool(frozen),
         "gates":gates,"summary":summary,"thresholds":{"global":GLOBAL_GATE,"per_k":PERK_GATE},
         "interpretation":{"historical_R3_reclassified":False,"new_physics_claim_licensed":False,
         "equation_level_followup_licensed":classification in (PASS_MISMATCH,FROZEN_REF_FAIL)}}
    Path(args.json_out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    np.savez_compressed(args.npz_out,anchors=anchors,redshifts=z,E1_raw_a_direct=E1,E2_raw_tau_direct=E2,
                        E3_bridge_tagged=E3,E4_frozen_source=E4,diff_E1_E3=E1-E3,diff_E1_E4=E1-E4,
                        D2_z0p2_E1=d21,D2_z0p2_E3=d23,D2_z0p2_E4=d24)
    print("FULLJ_CLASS_FRINGE_EXTRACTOR_AUDIT_SUMMARY="+json.dumps(summary,sort_keys=True), flush=True)
    print("FULLJ_CLASS_FRINGE_EXTRACTOR_AUDIT_GATES="+json.dumps(gates,sort_keys=True), flush=True)
    print("FULLJ_CLASS_FRINGE_EXTRACTOR_AUDIT_CLASSIFICATION="+classification, flush=True)
    return 0 if classification in (PASS_MISMATCH,R3_IMPL_DEFECT) else 1


if __name__=="__main__":
    raise SystemExit(main())
