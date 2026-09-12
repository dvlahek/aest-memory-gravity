#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import numpy as np
from scipy.interpolate import PchipInterpolator

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fullj_weyl import stochastic_tagged_mode_poc as poc
from fullj_weyl import stochastic_tagged_radial_convergence as radial
from fullj_weyl import stochastic_tagged_radial_k2_refinement as k2mod
from fullj_weyl import stochastic_response_kernel_poc as kernel

r2 = radial.r2
m = radial.m
static = radial.static
d2b = radial.d2b

R2_RESULT_LOCK = "1f42f88e9724c58d2d242a65ca7266a207e4a0f8"
GAUSS_RESULT_LOCK = "05e38b273f91eb04b7b4c8753731017d0ed839c1"
SAT_RESULT_LOCK = "f6eb7099cffc9ae6f4fe11ddef1794f0e6dd6e4f"
TAGGED_POC_RESULT_LOCK = "aff670fa8551163f5cde2b5146e0e5840d53b424"
K1_FAIL_RESULT_LOCK = "2531a10772f97958ab221bd1f39ceffc23e964a5"
K2_FAIL_RESULT_LOCK = "a293ff5d02824ba170fcf46251df1e480682386c"
KERNEL_RESULT_LOCK = "2a5f884a50b7b30b90ddff01721914626dbde20f"
HISTORY_LOCK = "6eea250e82c2ed2b161a776594948062a6d77743"
PREDATA_LOCK = "30630042acc41b1978f7ac8a0be2b736ababbc0b"

PASS = "FULLJ_STOCHASTIC_TAGGED_POWER_LATTICE_PASS"
FAIL = "FULLJ_STOCHASTIC_TAGGED_POWER_LATTICE_FAIL"
INCOMPLETE = "FULLJ_STOCHASTIC_TAGGED_POWER_LATTICE_INCOMPLETE"

SEED = 20260912
COEFF_HASH = "9c511b09899cb874d09c0513b89b82c796769886ecba5dd6347c71678b19d200"
B4 = (0, 1, 2, 3)
B2 = (0, 1)
EPS = 0.05
NSTEP = 4096
CHECK_Z = np.asarray(m.CHECK_Z, float)
REFERENCE_MEMBER = {"sigma": 0, "kind": "simple", "beta0": 1.0}

KF_A = 0.005
NX_A = 256
BOX_A = 2.0*np.pi/(KF_A*float(static.h))
KF_B = 0.0025
NX_B = 512
BOX_B = 2.0*np.pi/(KF_B*float(static.h))

KFULL = np.round(np.arange(0.030, 0.2000001, 0.005), 6)
HMISS = np.asarray([0.060,0.075,0.105,0.115,0.120,0.130,0.140,0.145,0.155,0.165,0.170,0.180,0.190,0.195], float)
FIXED_HALF = np.asarray([0.0325,0.0625,0.0925,0.1225,0.1625,0.1975], float)
N_HALF = 16
CURV_Z = (1.0, 0.5, 0.2)

CANONICAL_GATE = 1.0e-10
METRIC_GATE = 1.0e-8
SAT_GATE = 2.0e-2
ALG_GATE = 1.0e-12
BG_T_GLOBAL_GATE = 1.0e-2
BG_T_PERK_GATE = 3.0e-2
BG_P_GLOBAL_GATE = 2.0e-2
BG_P_PERK_GATE = 5.0e-2
POWER_L2_MAX_GATE = 5.0e-2
POWER_L2_MED_GATE = 2.5e-2
POWER_PEAK_GATE = 1.0e-1
SPIKE_FACTOR = 2.0

K2_JSON = ROOT / "results/fullj_stochastic_tagged_radial_k2_refinement.json"
K2_NPZ = ROOT / "results/fullj_stochastic_tagged_radial_k2_refinement.npz"
KERNEL_JSON = ROOT / "results/fullj_stochastic_response_kernel_poc.json"


def is_ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"], cwd=ROOT,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    ).returncode == 0


def idx(grid, value):
    q = np.where(np.isclose(np.asarray(grid,float), float(value), rtol=0.0, atol=5e-13))[0]
    if len(q) != 1:
        raise RuntimeError(f"nonunique index for {value}")
    return int(q[0])


def rel(a, b):
    aa=np.asarray(a,complex); bb=np.asarray(b,complex)
    return float(np.linalg.norm(aa-bb)/max(float(np.linalg.norm(aa)),float(np.linalg.norm(bb)),1e-300))


def rel_real(a, b):
    aa=np.asarray(a,float); bb=np.asarray(b,float)
    return float(np.linalg.norm(aa-bb)/max(float(np.linalg.norm(aa)),float(np.linalg.norm(bb)),1e-300))


def load_locked_k2():
    if not K2_JSON.exists() or not K2_NPZ.exists():
        raise FileNotFoundError("missing locked K2 local JSON/NPZ")
    meta=json.loads(K2_JSON.read_text())
    if meta.get("classification") != "FULLJ_STOCHASTIC_TAGGED_RADIAL_K2_REFINEMENT_FAIL":
        raise RuntimeError("local K2 JSON does not preserve historical FAIL")
    q=np.load(K2_NPZ)
    K2=np.asarray(q["K2"],float)
    A2=np.asarray(q["response_K2"],complex)
    if A2.shape != (4,len(K2),len(CHECK_Z)) or not np.all(np.isfinite(A2)):
        raise RuntimeError(f"locked K2 response mismatch {A2.shape}")
    return meta,K2,A2


def load_kernel_pass():
    if not KERNEL_JSON.exists():
        raise FileNotFoundError("missing local response-kernel POC JSON")
    q=json.loads(KERNEL_JSON.read_text())
    if q.get("classification") != "FULLJ_STOCHASTIC_RESPONSE_KERNEL_POC_PASS":
        raise RuntimeError("local response-kernel JSON is not the locked PASS")
    if q.get("STOCHASTIC_SCALAR_DIAGONAL_REDUCTION_SUPPORTED") is not True:
        raise RuntimeError("kernel PASS does not support scalar diagonal reduction")
    if q.get("STOCHASTIC_MODE_COUPLING_KERNEL_REQUIRED") is not False:
        raise RuntimeError("kernel PASS unexpectedly requires off-diagonal kernel")
    return q


def run_signed_geom(data, mode_h, gvec, bgid, kh, sign, kf_h, nx, box, stage):
    ntag=int(round(float(kh)/float(kf_h)))
    if abs(ntag*float(kf_h)-float(kh)) > 5e-13:
        raise RuntimeError(f"target {kh} not exact on kF={kf_h}")
    make,amp_tag,phase_tag=poc.basis_factory(mode_h,gvec,float(kh),EPS,int(sign),int(nx),float(box))
    old_cos=m.cos_matrix
    old_box=float(static.BOX)
    poc._ACTIVE_DATA=data
    d2b.set_member(REFERENCE_MEMBER)
    m.cos_matrix=make
    static.BOX=float(box)
    try:
        run=r2.integrate_combined_r2(data,int(nx),int(NSTEP),True)
        hh=poc.health(run)
        if not hh["finite"]:
            return {"finite":False,"stage":stage,"background":int(bgid),"k_h":float(kh),"sign":int(sign),"nx":int(nx),"kF_h":float(kf_h),"reason":run.get("fail_reason","incomplete")},None,None
        sat=poc.saturation(run,int(nx),float(box))
        vals=[]
        for cp in run["checkpoints"]:
            w=np.asarray(cp["metric"]["weyl"],float)
            fh=np.fft.fft(w)/float(w.size)
            vals.append(fh[ntag])
        rec={
            "finite":True,"stage":stage,"background":int(bgid),"k_h":float(kh),"epsilon":EPS,"sign":int(sign),
            "nx":int(nx),"kF_h":float(kf_h),"box_Mpc":float(box),"ntag":int(ntag),
            "canonical_max":float(hh["canonical_max"]),"metric_max":hh["metric_max"],
            "sat_max":float(np.max(sat)),"sat_by_z":np.asarray(sat,float).tolist(),
        }
        return rec,np.asarray(vals,complex),{"amp_tag":float(amp_tag),"phase_tag":float(phase_tag)}
    finally:
        m.cos_matrix=old_cos
        static.BOX=old_box
        poc._ACTIVE_DATA=None


def pair_response(pair, meta):
    return (pair[+1]-pair[-1])*np.exp(-1j*float(meta["phase_tag"]))/(EPS*float(meta["amp_tag"]))


def power_interp(k, p, keval):
    q=PchipInterpolator(np.log(np.asarray(k,float)),np.asarray(p,float),extrapolate=False)(np.log(np.asarray(keval,float)))
    return np.asarray(q,float)


def complex_interp(k, t, keval):
    return radial.interp_complex(np.asarray(k,float),np.asarray(t,complex),np.asarray(keval,float))


def adaptive_half_selection(Pb2):
    Pb2=np.asarray(Pb2,float)
    if Pb2.shape != (len(KFULL),len(CHECK_Z)):
        raise RuntimeError(f"bad B2 power shape {Pb2.shape}")
    izs=[idx(CHECK_Z,z) for z in CURV_Z]
    node_score=np.zeros(len(KFULL),float)
    for iz in izs:
        pm=float(np.max(Pb2[:,iz]))
        floor=max(1e-14*pm,1e-300)
        for j in range(1,len(KFULL)-1):
            den=max(float(Pb2[j-1,iz]),float(Pb2[j,iz]),float(Pb2[j+1,iz]),floor)
            c=abs(float(Pb2[j+1,iz]-2.0*Pb2[j,iz]+Pb2[j-1,iz]))/den
            node_score[j]=max(node_score[j],c)
    node_score[0]=node_score[1]
    node_score[-1]=node_score[-2]
    mids=0.5*(KFULL[:-1]+KFULL[1:])
    interval_score=np.maximum(node_score[:-1],node_score[1:])
    chosen=set()
    for q in FIXED_HALF:
        i=int(np.argmin(np.abs(mids-q)))
        chosen.add(i)
    order=sorted(range(len(mids)),key=lambda i:(-float(interval_score[i]),float(mids[i])))
    for i in order:
        if len(chosen)>=N_HALF:
            break
        chosen.add(i)
    if len(chosen)!=N_HALF:
        raise RuntimeError(f"adaptive selection produced {len(chosen)} intervals")
    sel=sorted(chosen,key=lambda i:float(mids[i]))
    rows=[{"interval_index":int(i),"left_k":float(KFULL[i]),"right_k":float(KFULL[i+1]),"mid_k":float(mids[i]),"curvature_score":float(interval_score[i]),"fixed_control":bool(np.any(np.isclose(FIXED_HALF,mids[i],rtol=0,atol=5e-13)))} for i in sel]
    return np.asarray([mids[i] for i in sel],float),rows,node_score,interval_score


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--json-out",default="results/fullj_stochastic_tagged_power_lattice.json")
    ap.add_argument("--npz-out",default="results/fullj_stochastic_tagged_power_lattice.npz")
    ap.add_argument("--csv-out",default="results/fullj_stochastic_tagged_power_lattice.csv")
    args=ap.parse_args()

    ancestry={
        "r2_result_lock":is_ancestor(R2_RESULT_LOCK),
        "gaussian_1d_result_lock":bool(poc.gaussian_lock_ok()),
        "saturated_closure_result_lock":is_ancestor(SAT_RESULT_LOCK),
        "tagged_poc_result_lock":is_ancestor(TAGGED_POC_RESULT_LOCK),
        "k1_fail_result_lock":is_ancestor(K1_FAIL_RESULT_LOCK),
        "k2_fail_result_lock":is_ancestor(K2_FAIL_RESULT_LOCK),
        "kernel_result_lock":is_ancestor(KERNEL_RESULT_LOCK),
        "history_lock":is_ancestor(HISTORY_LOCK),
        "predata_lock":is_ancestor(PREDATA_LOCK),
    }
    _,gcoef,digest=poc.coeff_draw()
    expected_full=np.round(np.arange(0.03,0.2000001,0.005),6)
    expected_miss=np.asarray([0.060,0.075,0.105,0.115,0.120,0.130,0.140,0.145,0.155,0.165,0.170,0.180,0.190,0.195],float)
    frozen=bool(
        digest==COEFF_HASH and B4==(0,1,2,3) and B2==(0,1) and EPS==0.05 and NSTEP==4096
        and KF_A==0.005 and NX_A==256 and KF_B==0.0025 and NX_B==512 and N_HALF==16
        and np.allclose(KFULL,expected_full,rtol=0,atol=5e-14) and np.allclose(HMISS,expected_miss,rtol=0,atol=5e-14)
        and np.allclose(FIXED_HALF,[0.0325,0.0625,0.0925,0.1225,0.1625,0.1975],rtol=0,atol=5e-14)
        and CURV_Z==(1.0,0.5,0.2) and REFERENCE_MEMBER=={"sigma":0,"kind":"simple","beta0":1.0}
    )

    print("FULLJ_POWER_LATTICE_START",flush=True)
    print("FULLJ_POWER_LATTICE_ANCESTRY="+json.dumps(ancestry,sort_keys=True),flush=True)
    print("FULLJ_POWER_LATTICE_COEFFICIENT_SHA256="+digest,flush=True)
    print("FULLJ_POWER_LATTICE_KFULL="+json.dumps(KFULL.tolist()),flush=True)
    print("FULLJ_POWER_LATTICE_HMISS="+json.dumps(HMISS.tolist()),flush=True)
    print(f"FULLJ_POWER_LATTICE_GEOMETRY_A kF_h={KF_A:.6f} NX={NX_A} box_Mpc={BOX_A:.12e}",flush=True)
    print(f"FULLJ_POWER_LATTICE_GEOMETRY_B kF_h={KF_B:.6f} NX={NX_B} box_Mpc={BOX_B:.12e}",flush=True)

    try:
        k2meta,K2,A2=load_locked_k2()
        kernelmeta=load_kernel_pass()
    except Exception as exc:
        out={"classification":INCOMPLETE,"diagnostic_complete":False,"ancestry":ancestry,"frozen_setup":frozen,"reason":str(exc)}
        Path(args.json_out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
        print("FULLJ_POWER_LATTICE_CLASSIFICATION="+INCOMPLETE,flush=True)
        return 3
    if not all(ancestry.values()) or not frozen:
        out={"classification":INCOMPLETE,"diagnostic_complete":False,"ancestry":ancestry,"frozen_setup":frozen,"coefficient_sha256":digest}
        Path(args.json_out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
        print("FULLJ_POWER_LATTICE_CLASSIFICATION="+INCOMPLETE,flush=True)
        return 3

    Anew=np.full((len(B4),len(HMISS),len(CHECK_Z)),np.nan+1j*np.nan,complex)
    all_runs=[]; response_rows=[]; run_index=0
    old_kmpc=np.asarray(m.K_MPC,float).copy(); old_kh=np.asarray(getattr(m,"K_H",radial.K0),float).copy()
    try:
        for ih,kh in enumerate(HMISS):
            mode_h=poc.target_modes(float(kh))
            m.K_H=mode_h.copy(); m.K_MPC=mode_h*float(static.h)
            data=r2.r0.prepare_bridge_data()
            for ib,bgid in enumerate(B4):
                pair={}; meta=None
                for sign in (+1,-1):
                    run_index+=1
                    rec,wh,mm=run_signed_geom(data,mode_h,gcoef[bgid],bgid,float(kh),sign,KF_A,NX_A,BOX_A,"full005")
                    rec["run_index"]=int(run_index); all_runs.append(rec)
                    print(f"FULLJ_POWER_LATTICE_RUN {run_index:03d}/176 stage=A bg={bgid} k_h={kh:.4f} sign={sign:+d} "+(f"canonical={rec['canonical_max']:.3e} satMax={rec['sat_max']:.3e}" if rec.get('finite') else f"finite=False reason={rec.get('reason','unknown')}"),flush=True)
                    if wh is not None:
                        pair[sign]=wh; meta=mm
                if len(pair)==2:
                    T=pair_response(pair,meta); Anew[ib,ih,:]=T
                    for iz,z in enumerate(CHECK_Z):
                        response_rows.append({"stage":"A","background":int(bgid),"k_h_Mpc_inv":float(kh),"z":float(z),"T_real":float(np.real(T[iz])),"T_imag":float(np.imag(T[iz])),"P_tag":float(abs(T[iz])**2)})
    finally:
        m.K_MPC=old_kmpc; m.K_H=old_kh

    stageA_runs=list(all_runs)
    A_finite=bool(np.all(np.isfinite(Anew)))
    Afull=np.full((len(B4),len(KFULL),len(CHECK_Z)),np.nan+1j*np.nan,complex)
    for ik,k in enumerate(K2):
        Afull[:,idx(KFULL,k),:]=A2[:,ik,:]
    for ih,k in enumerate(HMISS):
        Afull[:,idx(KFULL,k),:]=Anew[:,ih,:]
    if not np.all(np.isfinite(Afull)):
        raise RuntimeError("merged complete 0.005 lattice is incomplete")
    Pfull=np.abs(Afull)**2
    Pb2=np.mean(Pfull[:2],axis=0); Pb4=np.mean(Pfull,axis=0)
    Tb2=np.mean(Afull[:2],axis=0); Tb4=np.mean(Afull,axis=0)

    # New-node B2->B4 convergence.
    Tn2=np.mean(Anew[:2],axis=0); Tn4=np.mean(Anew,axis=0)
    Pn2=np.mean(np.abs(Anew[:2])**2,axis=0); Pn4=np.mean(np.abs(Anew)**2,axis=0)
    bg_t_global=rel(Tn2,Tn4); bg_p_global=rel_real(Pn2,Pn4)
    bg_rows=[]; bg_t_pk=[]; bg_p_pk=[]
    for ih,kh in enumerate(HMISS):
        qt=rel(Tn2[ih],Tn4[ih]); qp=rel_real(Pn2[ih],Pn4[ih])
        bg_t_pk.append(qt); bg_p_pk.append(qp)
        bg_rows.append({"k_h_Mpc_inv":float(kh),"response_relative_L2":float(qt),"power_relative_L2":float(qp)})
    bg_t_max=float(np.max(bg_t_pk)); bg_p_max=float(np.max(bg_p_pk))

    back=np.real(Afull)**2+np.imag(Afull)**2
    alg=float(np.linalg.norm(Pfull-back)/max(float(np.linalg.norm(Pfull)),1e-300))

    selected,selection_rows,node_curv,interval_curv=adaptive_half_selection(Pb2)
    print("FULLJ_POWER_LATTICE_SELECTED_HALF="+json.dumps(selected.tolist()),flush=True)
    print("FULLJ_POWER_LATTICE_SELECTION="+json.dumps(selection_rows,sort_keys=True),flush=True)

    Amid=np.full((len(B2),len(selected),len(CHECK_Z)),np.nan+1j*np.nan,complex)
    old_kmpc=np.asarray(m.K_MPC,float).copy(); old_kh=np.asarray(getattr(m,"K_H",radial.K0),float).copy()
    try:
        for ih,kh in enumerate(selected):
            mode_h=poc.target_modes(float(kh))
            m.K_H=mode_h.copy(); m.K_MPC=mode_h*float(static.h)
            data=r2.r0.prepare_bridge_data()
            for ib,bgid in enumerate(B2):
                pair={}; meta=None
                for sign in (+1,-1):
                    run_index+=1
                    rec,wh,mm=run_signed_geom(data,mode_h,gcoef[bgid],bgid,float(kh),sign,KF_B,NX_B,BOX_B,"half0025")
                    rec["run_index"]=int(run_index); all_runs.append(rec)
                    print(f"FULLJ_POWER_LATTICE_RUN {run_index:03d}/176 stage=B bg={bgid} k_h={kh:.4f} sign={sign:+d} "+(f"canonical={rec['canonical_max']:.3e} satMax={rec['sat_max']:.3e}" if rec.get('finite') else f"finite=False reason={rec.get('reason','unknown')}"),flush=True)
                    if wh is not None:
                        pair[sign]=wh; meta=mm
                if len(pair)==2:
                    T=pair_response(pair,meta); Amid[ib,ih,:]=T
                    for iz,z in enumerate(CHECK_Z):
                        response_rows.append({"stage":"B","background":int(bgid),"k_h_Mpc_inv":float(kh),"z":float(z),"T_real":float(np.real(T[iz])),"T_imag":float(np.imag(T[iz])),"P_tag":float(abs(T[iz])**2)})
    finally:
        m.K_MPC=old_kmpc; m.K_H=old_kh

    stageB_runs=all_runs[len(stageA_runs):]
    Pmid=np.mean(np.abs(Amid)**2,axis=0)
    Tmid=np.mean(Amid,axis=0)

    power_rows=[]; transfer_desc=[]; power_l2=[]; power_peak=[]; pinterp_all=[]
    spike_ok=True; spike_max_ratio=0.0
    for iz,z in enumerate(CHECK_Z):
        pred=power_interp(KFULL,Pb2[:,iz],selected)
        direct=Pmid[:,iz]
        ep=rel_real(pred,direct)
        epeak=float(np.max(np.abs(pred-direct))/max(float(np.max(direct)),1e-300))
        power_l2.append(ep); power_peak.append(epeak); pinterp_all.append(pred)
        power_rows.append({"z":float(z),"power_L2":float(ep),"power_peak":float(epeak)})
        tpred=complex_interp(KFULL,Tb2[:,iz],selected)
        transfer_desc.append({"z":float(z),"transfer_L2_descriptive":float(rel(tpred,Tmid[:,iz]))})
        pmax=float(np.max(Pb2[:,iz]))
        floor=1e-14*pmax
        for ih,kh in enumerate(selected):
            right=int(np.searchsorted(KFULL,kh)); left=right-1
            den=max(float(Pb2[left,iz]),float(Pb2[right,iz]),floor,1e-300)
            ratio=float(direct[ih]/den)
            spike_max_ratio=max(spike_max_ratio,ratio)
            if float(direct[ih]) > SPIKE_FACTOR*max(float(Pb2[left,iz]),float(Pb2[right,iz])) + floor:
                spike_ok=False
    pinterp_all=np.asarray(pinterp_all,float).T  # selected,z
    interp_nonneg=bool(np.all(np.isfinite(pinterp_all)) and np.all(pinterp_all>=0.0))

    healthA=bool(len(stageA_runs)==112 and all(r.get("finite",False) for r in stageA_runs) and all(float(r["canonical_max"])<=CANONICAL_GATE and all(float(v)<=METRIC_GATE for v in r["metric_max"].values()) for r in stageA_runs))
    satA=float(max([r.get("sat_max",float("inf")) for r in stageA_runs],default=float("inf")))
    healthB=bool(len(stageB_runs)==64 and all(r.get("finite",False) for r in stageB_runs) and all(float(r["canonical_max"])<=CANONICAL_GATE and all(float(v)<=METRIC_GATE for v in r["metric_max"].values()) for r in stageB_runs))
    satB=float(max([r.get("sat_max",float("inf")) for r in stageB_runs],default=float("inf")))

    gates={
        "PL_G1_provenance_and_frozen_identity":bool(all(ancestry.values()) and frozen),
        "PL_G2_stageA_solver_constraint_health":bool(healthA),
        "PL_G3_stageA_broadband_saturated_closure":bool(satA<=SAT_GATE),
        "PL_G4_complete_lattice_algebra_background_sanity":bool(A_finite and np.all(np.isfinite(Afull)) and np.all(np.isfinite(Pfull)) and np.all(Pfull>=0) and alg<=ALG_GATE and bg_t_global<=BG_T_GLOBAL_GATE and bg_t_max<=BG_T_PERK_GATE and bg_p_global<=BG_P_GLOBAL_GATE and bg_p_max<=BG_P_PERK_GATE),
        "PL_G5_stageB_solver_constraint_saturation_health":bool(healthB and satB<=SAT_GATE and np.all(np.isfinite(Amid))),
        "PL_G6_power_half_lattice_interpolation_accuracy":bool(interp_nonneg and max(power_l2)<=POWER_L2_MAX_GATE and float(np.median(power_l2))<=POWER_L2_MED_GATE and max(power_peak)<=POWER_PEAK_GATE),
        "PL_G7_no_unresolved_selected_interval_power_spike":bool(spike_ok),
    }
    classification=PASS if all(gates.values()) else FAIL
    summary={
        "coefficient_sha256":digest,
        "runs_expected":176,
        "runs_finite":int(sum(bool(r.get("finite",False)) for r in all_runs)),
        "stageA_saturation_max":satA,"stageB_saturation_max":satB,
        "tagged_power_identity_relative_residual":alg,
        "newnode_background_response_global":bg_t_global,"newnode_background_response_per_k_max":bg_t_max,
        "newnode_background_power_global":bg_p_global,"newnode_background_power_per_k_max":bg_p_max,
        "selected_half_nodes":selected.tolist(),
        "power_half_L2_max":float(max(power_l2)),"power_half_L2_median":float(np.median(power_l2)),
        "power_half_peak_max":float(max(power_peak)),"power_interpolant_finite_nonnegative":interp_nonneg,
        "power_midpoint_spike_max_ratio":float(spike_max_ratio),
    }
    out={
        "classification":classification,"diagnostic_complete":True,
        "git_head":subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip(),
        "ancestry":ancestry,"gates":gates,"summary":summary,
        "seed":SEED,"coefficient_sha256":digest,"background_ids_B4":list(B4),"background_ids_B2":list(B2),
        "K_full_h_Mpc_inv":KFULL.tolist(),"H_missing_h_Mpc_inv":HMISS.tolist(),"selected_half_h_Mpc_inv":selected.tolist(),
        "redshifts":CHECK_Z.tolist(),"epsilon":EPS,"NSTEP":NSTEP,"reference_member":REFERENCE_MEMBER,
        "selection":selection_rows,"background_convergence_new_nodes":bg_rows,
        "power_half_validation":power_rows,"transfer_half_descriptive":transfer_desc,"runs":all_runs,
        "STOCHASTIC_TAGGED_FULL_005_LATTICE_TESTED":classification==PASS,
        "STOCHASTIC_TAGGED_BOUNDED_POWER_INTERPOLANT_TESTED":classification==PASS,
        "THREE_D_BOUNDED_CONTINUOUS_WEYL_POWER_LICENSED":False,
        "THREE_D_CONTINUOUS_WEYL_POWER_LICENSED":False,
        "EVOLVING_WEYL_POWER_LICENSED":False,
        "ACT_LIKELIHOOD_LICENSED":False,
        "OBSERVATIONAL_CLAIM_LICENSED":False,
    }
    Path(args.json_out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    np.savez_compressed(args.npz_out,redshifts=CHECK_Z,K_full=KFULL,H_missing=HMISS,selected_half=selected,response_full=Afull,power_full=Pfull,response_half=Amid,power_half=np.abs(Amid)**2,Pb2=Pb2,Pb4=Pb4,Tb2=Tb2,Tb4=Tb4,power_interp_half=pinterp_all,node_curvature=node_curv,interval_curvature=interval_curv)
    with open(args.csv_out,"w",newline="") as f:
        fields=["stage","background","k_h_Mpc_inv","z","T_real","T_imag","P_tag"]
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(response_rows)

    print("FULLJ_POWER_LATTICE_SUMMARY="+json.dumps(summary,sort_keys=True),flush=True)
    print("FULLJ_POWER_LATTICE_GATES="+json.dumps(gates,sort_keys=True),flush=True)
    print("FULLJ_POWER_LATTICE_CLASSIFICATION="+classification,flush=True)
    print("STOCHASTIC_TAGGED_FULL_005_LATTICE_TESTED="+str(classification==PASS),flush=True)
    print("STOCHASTIC_TAGGED_BOUNDED_POWER_INTERPOLANT_TESTED="+str(classification==PASS),flush=True)
    print("THREE_D_BOUNDED_CONTINUOUS_WEYL_POWER_LICENSED=False",flush=True)
    print("THREE_D_CONTINUOUS_WEYL_POWER_LICENSED=False",flush=True)
    print("EVOLVING_WEYL_POWER_LICENSED=False",flush=True)
    print("ACT_LIKELIHOOD_LICENSED=False",flush=True)
    print("OBSERVATIONAL_CLAIM_LICENSED=False",flush=True)
    return 0 if classification==PASS else 2


if __name__ == "__main__":
    raise SystemExit(main())
