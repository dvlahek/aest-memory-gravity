#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys

import numpy as np

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
    aa = np.asarray(a, complex)
    bb = np.asarray(b, complex)
    return float(np.linalg.norm(aa-bb) / max(float(np.linalg.norm(aa)), float(np.linalg.norm(bb)), 1e-300))


def per_k_rel(a, b):
    aa = np.asarray(a, complex)
    bb = np.asarray(b, complex)
    return [rel(aa[i], bb[i]) for i in range(aa.shape[0])]


def idx(grid, x):
    q = np.where(np.isclose(np.asarray(grid, float), float(x), rtol=0.0, atol=5e-13))[0]
    if len(q) != 1:
        raise RuntimeError(f"nonunique/missing value {x}")
    return int(q[0])


def direct_tau_values(raw, redshifts):
    akey = base.d2a.pick(raw, "a", ("scale factor",))
    tkey = base.d2a.pick(raw, "tau [Mpc]", ("tau", "tau[Mpc]"))
    pkey = base.d2a.pick(raw, "phi")
    skey = base.d2a.pick(raw, "psi")
    aa = np.asarray(raw[akey], float)
    tt = np.asarray(raw[tkey], float)
    ww = np.asarray(raw[pkey], float) + np.asarray(raw[skey], float)
    tau_of_a, ax = base.unique_spline_x(aa, tt)
    w_of_tau, tx = base.unique_spline_x(tt, ww)
    at = 1.0/(1.0+np.asarray(redshifts, float))
    if float(np.min(ax)) > float(np.min(at))+1e-12 or float(np.max(ax)) < float(np.max(at))-1e-12:
        raise RuntimeError("raw history lacks scale-factor coverage")
    tau_target = np.asarray(tau_of_a(at), float)
    if float(np.min(tx)) > float(np.min(tau_target))+1e-9 or float(np.max(tx)) < float(np.max(tau_target))-1e-9:
        raise RuntimeError("raw history lacks conformal-time coverage")
    out = np.asarray(w_of_tau(tau_target), float)
    if not np.all(np.isfinite(out)):
        raise RuntimeError("nonfinite direct tau-coordinate values")
    return out


def load_locked():
    for p in (R3_RESULT_JSON, R3_RESULT_NPZ, SOURCE_JSON, SOURCE_NPZ):
        if not p.exists():
            raise FileNotFoundError(str(p))
    return (
        json.loads(R3_RESULT_JSON.read_text()),
        json.loads(SOURCE_JSON.read_text()),
        np.load(R3_RESULT_NPZ),
        np.load(SOURCE_NPZ),
    )


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
        out.extend([y[j+1]-2.0*y[j]+y[j-1] for j in (1,2,3)])
    return np.asarray(out, complex)


def safe_corr(a,b):
    aa=np.asarray(a,float); bb=np.asarray(b,float)
    if aa.size<2 or float(np.std(aa))<=1e-300 or float(np.std(bb))<=1e-300:
        return float("nan")
    return float(np.corrcoef(aa,bb)[0,1])


def bridge_tagged_class_only(anchors, redshifts):
    old_kmpc=np.asarray(sd.m.K_MPC,float).copy()
    old_kh=np.asarray(getattr(sd.m,"K_H",[]),float).copy()
    E3=np.full((len(anchors),len(redshifts)),np.nan+1j*np.nan,complex)
    _,gcoef,_=sd.poc.coeff_draw()
    try:
        for ik,kh in enumerate(anchors):
            mode_h=sd.poc.target_modes(float(kh))
            sd.m.K_H=mode_h.copy()
            sd.m.K_MPC=mode_h*float(sd.static.h)
            data=sd.r2.r0.prepare_bridge_data()
            tau_check=np.asarray(data["tau_check"],float)
            if len(tau_check)!=len(redshifts):
                raise RuntimeError(f"bridge checkpoint count {len(tau_check)} != {len(redshifts)}")
            ntag=int(round(float(kh)/float(sd.KF)))
            if abs(ntag*float(sd.KF)-float(kh))>5e-13:
                raise RuntimeError(f"anchor {kh} is not exact on historical bridge geometry")
            vals={}
            meta=None
            for sign in (+1,-1):
                make,amp_tag,phase_tag=sd.poc.basis_factory(
                    mode_h,gcoef[sd.BG],float(kh),sd.EPS,int(sign),sd.NX,sd.BOX
                )
                C=make(sd.NX)
                wh=[]
                for tau in tau_check:
                    _,_,w0=sd.r2.r0.class_metric_fields(data,float(tau),sd.NX,C)
                    fh=np.fft.fft(np.asarray(w0,float))/float(sd.NX)
                    wh.append(fh[ntag])
                vals[int(sign)]=np.asarray(wh,complex)
                meta=(float(amp_tag),float(phase_tag))
            amp,phase=meta
            E3[ik]=(vals[+1]-vals[-1])*np.exp(-1j*phase)/(float(sd.EPS)*amp)
    finally:
        sd.m.K_MPC=old_kmpc
        if old_kh.size:
            sd.m.K_H=old_kh
    return E3


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--json-out",default="results/fullj_corrected_class_spectral_fringe_extractor_equivalence.json")
    ap.add_argument("--npz-out",default="results/fullj_corrected_class_spectral_fringe_extractor_equivalence.npz")
    args=ap.parse_args()

    print("FULLJ_CLASS_FRINGE_EXTRACTOR_AUDIT_START",flush=True)
    try:
        rj,sj,rq,sq=load_locked()
    except Exception as exc:
        out={"classification":INCOMPLETE,"diagnostic_complete":False,"reason":str(exc)}
        Path(args.json_out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
        print("FULLJ_CLASS_FRINGE_EXTRACTOR_AUDIT_CLASSIFICATION="+INCOMPLETE,flush=True)
        return 3

    anchors=np.asarray(base.K_ANCHOR,float)
    z=np.asarray(base.CHECK_Z,float)
    frozen=bool(
        is_ancestor(PREDATA_LOCK)
        and rj.get("classification")=="FULLJ_CORRECTED_CLASS_SPECTRAL_FRINGE_NUMERICAL_CONTROL_FAIL"
        and sj.get("classification")==sd.CLASS_DOMINATED
        and np.allclose(np.asarray(rq["k_anchor_h_Mpc"],float),anchors,rtol=0,atol=5e-13)
        and np.allclose(np.asarray(rq["redshifts"],float),z,rtol=0,atol=5e-13)
        and rj.get("gates",{}).get("DG_G3_requested_k_list_invariance") is True
        and rj.get("gates",{}).get("DG_G4_dense_grid_health") is True
        and rj.get("gates",{}).get("DG_G5_fine_grid_spectral_structure") is True
        and rj.get("gates",{}).get("DG_G6_AeST_specificity_against_GR") is True
    )

    # E1: exact completed-R3 sparse direct anchors; no recomputation.
    E1=np.asarray(rq["aest_sparse_W"],float)
    if E1.shape!=(15,len(z)):
        raise RuntimeError(f"bad E1 shape {E1.shape}")

    # E2: same 15-anchor corrected CLASS run, evaluated through tau rather than a.
    from classy import Class
    pars=dict(base.cb.build_params())
    pars.update({
        "output":"mTk,vTk",
        "lensing":"no",
        "P_k_max_h/Mpc":0.30,
        "z_max_pk":6.5,
        "aest_memory_enabled":"no",
        "aest_eta":0.0,
        "aest_enabled":"yes",
    })
    pars.pop("l_max_scalars",None)
    kvals,serial_meta=r3.serialize_requested_k(anchors)
    pars["k_output_values"]=kvals
    c=Class(); c.set(pars); c.compute()
    try:
        pert=c.get_perturbations()
        histories,_=base.d2a.scalar_histories(pert)
        if len(histories)!=15:
            raise RuntimeError(f"history count {len(histories)} != 15")
        E2=np.stack([direct_tau_values(raw,z) for raw in histories],axis=0)
    finally:
        c.struct_cleanup(); c.empty()

    # E3: exact historical bridge/tagged CLASS-only extraction algebra, with no nonlinear integration required.
    E3=bridge_tagged_class_only(anchors,z)

    # E4: frozen historical source-decomposition reference.
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

    g1=bool(frozen and np.all(np.isfinite(E1)) and np.all(np.isfinite(E2)) and np.all(np.isfinite(E3)) and np.all(np.isfinite(E4)))
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
        "E1_E2_global_relative_L2":e12,
        "E1_E2_per_k_max":float(max(p12)),
        "E3_E4_global_relative_L2":e34,
        "E3_E4_per_k_max":float(max(p34)),
        "E1_E3_global_relative_L2":e13,
        "E1_E3_per_k_max":float(max(p13)),
        "E1_E4_global_relative_L2":e14,
        "E1_E4_per_k_max":float(max(p14)),
        "E1_E3_per_redshift_relative_L2":rz13,
        "E1_E4_per_redshift_relative_L2":rz14,
        "max_abs_E1_E4_difference":float(diff[imax]),
        "max_abs_E1_E4_k_h":float(anchors[imax[0]]),
        "max_abs_E1_E4_z":float(z[imax[1]]),
        "sign_disagreement_count":sign_disagree,
        "z0p2_D2_corr_E1_E3":safe_corr(np.real(d21),np.real(d23)),
        "z0p2_D2_corr_E1_E4":safe_corr(np.real(d21),np.real(d24)),
        "serialization_dense15_chars":int(serial_meta["string_length"]),
    }
    gates={
        "EX_G1_provenance_and_frozen_identity":g1,
        "EX_G2_direct_coordinate_equivalence":g2,
        "EX_G3_bridge_extractor_self_equivalence":g3,
        "EX_G4_discrepancy_localized":True,
        "EX_G5_direct_signal_controls_preserved":g5,
    }
    out={
        "classification":classification,
        "diagnostic_complete":True,
        "frozen_setup":bool(frozen),
        "gates":gates,
        "summary":summary,
        "thresholds":{"global":GLOBAL_GATE,"per_k":PERK_GATE},
        "interpretation":{
            "historical_R3_reclassified":False,
            "new_physics_claim_licensed":False,
            "equation_level_followup_licensed":classification in (PASS_MISMATCH,FROZEN_REF_FAIL),
        },
    }
    Path(args.json_out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    np.savez_compressed(
        args.npz_out,
        anchors=anchors,redshifts=z,
        E1_raw_a_direct=E1,E2_raw_tau_direct=E2,E3_bridge_tagged=E3,E4_frozen_source=E4,
        diff_E1_E3=E1-E3,diff_E1_E4=E1-E4,
        D2_z0p2_E1=d21,D2_z0p2_E3=d23,D2_z0p2_E4=d24,
    )
    print("FULLJ_CLASS_FRINGE_EXTRACTOR_AUDIT_SUMMARY="+json.dumps(summary,sort_keys=True),flush=True)
    print("FULLJ_CLASS_FRINGE_EXTRACTOR_AUDIT_GATES="+json.dumps(gates,sort_keys=True),flush=True)
    print("FULLJ_CLASS_FRINGE_EXTRACTOR_AUDIT_CLASSIFICATION="+classification,flush=True)
    return 0 if classification in (PASS_MISMATCH,R3_IMPL_DEFECT) else 1


if __name__=="__main__":
    raise SystemExit(main())
