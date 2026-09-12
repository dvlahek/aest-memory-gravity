#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
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

r2 = poc.r2
m = poc.m
static = poc.static
d2b = poc.d2b

R2_RESULT_LOCK = "1f42f88e9724c58d2d242a65ca7266a207e4a0f8"
SAT_RESULT_LOCK = "f6eb7099cffc9ae6f4fe11ddef1794f0e6dd6e4f"
RESIDUAL_FAIL_RESULT_LOCK = "4d87865a8e45985388dfab2b9d8922faa9290f7f"
CARDINALITY_RESULT_LOCK = "df182a828b3c140fba22f1f5d58414ec41017e7b"
POC_RESULT_LOCK = "aff670fa8551163f5cde2b5146e0e5840d53b424"
HISTORY_LOCK = "60fe83c37b74fea60d62df8fbe7a429218108af5"
PREDATA_LOCK = "26571f4e2fadab7bccfd1c42c2c1f4fd7881e624"

PASS = "FULLJ_STOCHASTIC_TAGGED_RADIAL_CONVERGENCE_PASS"
FAIL = "FULLJ_STOCHASTIC_TAGGED_RADIAL_CONVERGENCE_FAIL"
INCOMPLETE = "FULLJ_STOCHASTIC_TAGGED_RADIAL_CONVERGENCE_INCOMPLETE"

SEED = 20260912
COEFF_HASH = poc.COEFF_HASH
B4 = (0, 1, 2, 3)
B2 = (0, 1)
K0 = np.asarray([0.03, 0.05, 0.08, 0.10, 0.15, 0.20], float)
K1 = np.asarray([0.03, 0.04, 0.05, 0.065, 0.08, 0.09, 0.10, 0.125, 0.15, 0.175, 0.20], float)
H1 = np.asarray([0.04, 0.065, 0.09, 0.125, 0.175], float)
CHECK_Z = np.asarray(poc.CHECK_Z, float)
EPS = 0.05
KF_H = 0.005
NX = 256
NSTEP = 4096
BOX = 2.0 * np.pi / (KF_H * float(static.h))
REFERENCE_MEMBER = {"sigma": 0, "kind": "simple", "beta0": 1.0}

CANONICAL_GATE = 1.0e-10
METRIC_GATE = 1.0e-8
SAT_GATE = 2.0e-2
ALG_GATE = 1.0e-12
REG_MED_GATE = 1.0e-6
REG_MAX_GATE = 1.0e-5
BG_T_GLOBAL_GATE = 1.0e-2
BG_T_PERK_GATE = 3.0e-2
BG_P_GLOBAL_GATE = 2.0e-2
BG_P_PERK_GATE = 5.0e-2
HOLD_T_GATE = 3.0e-2
HOLD_P_GATE = 5.0e-2
HOLD_PEAK_GATE = 1.0e-1
FINE_T_GATE = 3.0e-2
FINE_P_GATE = 5.0e-2
FINE_PEAK_GATE = 1.0e-1
FINE_T_MED_GATE = 1.5e-2
FINE_P_MED_GATE = 2.5e-2
SMOOTH_FACTOR = 2.0

POC_NPZ = ROOT / "results/fullj_stochastic_tagged_mode_poc.npz"
POC_JSON = ROOT / "results/fullj_stochastic_tagged_mode_poc.json"


def is_ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"], cwd=ROOT,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    ).returncode == 0


def idx(grid, value):
    q = np.where(np.isclose(np.asarray(grid, float), float(value), rtol=0.0, atol=5e-13))[0]
    if len(q) != 1:
        raise RuntimeError(f"nonunique radial node {value}")
    return int(q[0])


def rel(a, b):
    aa = np.asarray(a, complex)
    bb = np.asarray(b, complex)
    return float(np.linalg.norm(aa-bb) / max(float(np.linalg.norm(aa)), float(np.linalg.norm(bb)), 1e-300))


def interp_complex(k, y, keval):
    lk = np.log(np.asarray(k, float))
    le = np.log(np.asarray(keval, float))
    yy = np.asarray(y, complex)
    rr = PchipInterpolator(lk, np.real(yy), extrapolate=False)(le)
    ii = PchipInterpolator(lk, np.imag(yy), extrapolate=False)(le)
    return np.asarray(rr + 1j*ii, complex)


def interp_power(k, y, keval):
    out = PchipInterpolator(np.log(np.asarray(k,float)), np.asarray(y,float), extrapolate=False)(np.log(np.asarray(keval,float)))
    return np.asarray(out, float)


def common_geometry(kh: float):
    ntag = int(round(float(kh) / KF_H))
    if abs(ntag*KF_H - float(kh)) > 5e-13:
        raise RuntimeError(f"target {kh} is not an exact common-lattice mode")
    return KF_H, ntag, NX, BOX


def run_signed_common(data, mode_h, gvec, bgid, kh, sign):
    ntag = int(round(float(kh)/KF_H))
    make, amp_tag, phase_tag = poc.basis_factory(mode_h, gvec, kh, EPS, sign, NX, BOX)
    old_cos = m.cos_matrix
    old_box = float(static.BOX)
    d2b.set_member(REFERENCE_MEMBER)
    m.cos_matrix = make
    static.BOX = BOX
    poc._ACTIVE_DATA = data
    try:
        run = r2.integrate_combined_r2(data, NX, NSTEP, True)
        hh = poc.health(run)
        if not hh["finite"]:
            return {
                "finite": False, "background": int(bgid), "k_h": float(kh),
                "epsilon": EPS, "sign": int(sign), "nx": NX, "box_Mpc": BOX,
                "reason": run.get("fail_reason", "incomplete")
            }, None, None
        sat = poc.saturation(run, NX, BOX)
        wh = poc.tagged_fourier(run, ntag)
        rec = {
            "finite": True, "background": int(bgid), "k_h": float(kh),
            "epsilon": EPS, "sign": int(sign), "nx": NX, "box_Mpc": BOX,
            "kF_h": KF_H, "ntag": int(ntag),
            "canonical_max": float(hh["canonical_max"]),
            "metric_max": hh["metric_max"],
            "sat_max": float(np.max(sat)), "sat_by_z": sat.tolist(),
        }
        return rec, wh, {"amp_tag": amp_tag, "phase_tag": phase_tag}
    finally:
        poc._ACTIVE_DATA = None
        m.cos_matrix = old_cos
        static.BOX = old_box


def load_poc_primary():
    if not POC_NPZ.exists() or not POC_JSON.exists():
        raise FileNotFoundError("missing locked stochastic tagged POC local outputs")
    meta = json.loads(POC_JSON.read_text())
    if meta.get("classification") != "FULLJ_STOCHASTIC_TAGGED_MODE_POC_PASS":
        raise RuntimeError("local tagged POC JSON does not preserve locked PASS")
    q = np.load(POC_NPZ)
    arr = np.asarray(q["primary_response"], complex)
    if arr.shape != (9, len(CHECK_Z)):
        raise RuntimeError(f"unexpected tagged POC primary_response shape {arr.shape}")
    return arr.reshape(3, 3, len(CHECK_Z))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json-out", default="results/fullj_stochastic_tagged_radial_convergence.json")
    ap.add_argument("--npz-out", default="results/fullj_stochastic_tagged_radial_convergence.npz")
    ap.add_argument("--csv-out", default="results/fullj_stochastic_tagged_radial_convergence.csv")
    args = ap.parse_args()

    ancestry = {
        "r2_result_lock": is_ancestor(R2_RESULT_LOCK),
        "gaussian_1d_result_lock": bool(poc.gaussian_lock_ok()),
        "saturated_closure_result_lock": is_ancestor(SAT_RESULT_LOCK),
        "residual_r2_fail_result_lock": is_ancestor(RESIDUAL_FAIL_RESULT_LOCK),
        "cardinality_result_lock": is_ancestor(CARDINALITY_RESULT_LOCK),
        "tagged_poc_result_lock": is_ancestor(POC_RESULT_LOCK),
        "history_lock": is_ancestor(HISTORY_LOCK),
        "predata_lock": is_ancestor(PREDATA_LOCK),
    }
    _, g, digest = poc.coeff_draw()
    grid_ok = bool(
        np.array_equal(K0, np.asarray(poc.K0,float))
        and len(K1)==11 and len(H1)==5
        and all(abs(round(k/KF_H)*KF_H-k)<5e-13 for k in K1)
        and common_geometry(0.03)[:3] == (KF_H,6,NX)
        and common_geometry(0.20)[:3] == (KF_H,40,NX)
    )
    frozen = bool(
        digest == COEFF_HASH and B4==(0,1,2,3) and B2==(0,1)
        and EPS==0.05 and KF_H==0.005 and NX==256 and NSTEP==4096 and grid_ok
        and REFERENCE_MEMBER=={"sigma":0,"kind":"simple","beta0":1.0}
    )

    print("FULLJ_TAGGED_RADIAL_START", flush=True)
    print("FULLJ_TAGGED_RADIAL_ANCESTRY="+json.dumps(ancestry,sort_keys=True), flush=True)
    print("FULLJ_TAGGED_RADIAL_COEFFICIENT_SHA256="+digest, flush=True)
    print("FULLJ_TAGGED_RADIAL_K1="+json.dumps(K1.tolist()), flush=True)
    print(f"FULLJ_TAGGED_RADIAL_GEOMETRY kF_h={KF_H:.6f} NX={NX} box_Mpc={BOX:.12e}", flush=True)

    try:
        poc_locked = load_poc_primary()
    except Exception as exc:
        out={"classification":INCOMPLETE,"diagnostic_complete":False,"ancestry":ancestry,"frozen_setup":frozen,"reason":str(exc)}
        Path(args.json_out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
        print("FULLJ_TAGGED_RADIAL_CLASSIFICATION="+INCOMPLETE, flush=True)
        return 3

    if not all(ancestry.values()) or not frozen:
        out={"classification":INCOMPLETE,"diagnostic_complete":False,"ancestry":ancestry,"frozen_setup":frozen,"coefficient_sha256":digest}
        Path(args.json_out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
        print("FULLJ_TAGGED_RADIAL_CLASSIFICATION="+INCOMPLETE, flush=True)
        return 3

    old_kmpc = np.asarray(m.K_MPC,float).copy()
    old_kh = np.asarray(getattr(m,"K_H",K0),float).copy()
    all_runs=[]
    A=np.full((len(B4),len(K1),len(CHECK_Z)),np.nan+1j*np.nan,complex)
    rows=[]
    run_index=0

    try:
        for ik,kh in enumerate(K1):
            mode_h = poc.target_modes(float(kh))
            m.K_H = mode_h.copy(); m.K_MPC = mode_h*float(static.h)
            data = r2.r0.prepare_bridge_data()
            for ib,bgid in enumerate(B4):
                pair={}; meta=None
                for sign in (+1,-1):
                    run_index += 1
                    rec, wh, mm = run_signed_common(data, mode_h, g[bgid], bgid, float(kh), sign)
                    rec["run_index"] = int(run_index)
                    all_runs.append(rec)
                    print(
                        f"FULLJ_TAGGED_RADIAL_RUN {run_index:03d}/88 bg={bgid} k_h={kh:.6f} sign={sign:+d} "
                        + (f"canonical={rec['canonical_max']:.3e} satMax={rec['sat_max']:.3e}" if rec.get("finite") else f"finite=False reason={rec.get('reason','unknown')}"),
                        flush=True,
                    )
                    if wh is not None:
                        pair[sign]=wh; meta=mm
                if len(pair)==2:
                    T=(pair[+1]-pair[-1])*np.exp(-1j*float(meta["phase_tag"]))/(EPS*float(meta["amp_tag"]))
                    A[ib,ik,:]=T
                    for iz,z in enumerate(CHECK_Z):
                        rows.append({
                            "background":int(bgid),"k_h_Mpc_inv":float(kh),"z":float(z),
                            "T_real":float(np.real(T[iz])),"T_imag":float(np.imag(T[iz])),
                            "P_tag":float(abs(T[iz])**2),
                        })
    finally:
        m.K_MPC=old_kmpc; m.K_H=old_kh

    all_finite = len(all_runs)==88 and all(bool(r.get("finite",False)) for r in all_runs)
    health_ok = bool(all_finite and all(
        float(r["canonical_max"])<=CANONICAL_GATE
        and all(float(v)<=METRIC_GATE for v in r["metric_max"].values())
        for r in all_runs
    ))
    satmax=float(max([r.get("sat_max",float("inf")) for r in all_runs],default=float("inf")))

    P=np.abs(A)**2
    back=np.real(A)**2+np.imag(A)**2
    alg=float(np.linalg.norm(P-back)/max(float(np.linalg.norm(P)),1e-300)) if np.all(np.isfinite(A)) else float("inf")
    algebra_ok=bool(np.all(np.isfinite(A)) and np.all(np.isfinite(P)) and np.all(P>=0) and alg<=ALG_GATE)

    T4=np.mean(A,axis=0); T2=np.mean(A[:2],axis=0)
    P4=np.mean(P,axis=0); P2=np.mean(P[:2],axis=0)

    reg_rows=[]; reg_err=[]
    for bg in (0,1,2):
        for kh,poc_ik in ((0.10,1),(0.175,2)):
            new=A[idx(np.asarray(B4,float),float(bg)),idx(K1,kh),:]
            old=poc_locked[bg,poc_ik,:]
            q=rel(new,old); reg_err.append(q)
            reg_rows.append({"background":int(bg),"k_h_Mpc_inv":float(kh),"relative_L2":float(q)})
    reg_med=float(np.median(reg_err)); reg_max=float(np.max(reg_err))

    bg_t_global=rel(T2,T4)
    bg_p_global=float(np.linalg.norm(P2-P4)/max(float(np.linalg.norm(P2)),float(np.linalg.norm(P4)),1e-300))
    bg_rows=[]; bg_t_pk=[]; bg_p_pk=[]
    for ik,kh in enumerate(K1):
        qt=rel(T2[ik],T4[ik])
        qp=float(np.linalg.norm(P2[ik]-P4[ik])/max(float(np.linalg.norm(P2[ik])),float(np.linalg.norm(P4[ik])),1e-300))
        bg_t_pk.append(qt); bg_p_pk.append(qp)
        bg_rows.append({"k_h_Mpc_inv":float(kh),"response_relative_L2":float(qt),"power_relative_L2":float(qp)})
    bg_t_max=float(np.max(bg_t_pk)); bg_p_max=float(np.max(bg_p_pk))

    i0=np.asarray([idx(K1,k) for k in K0],int)
    ih=np.asarray([idx(K1,k) for k in H1],int)
    hold_rows=[]; hold_t=[]; hold_p=[]; hold_peak=[]
    smooth_ok=True; smooth_max_ratio=0.0
    for iz,z in enumerate(CHECK_Z):
        pred=interp_complex(K0,T4[i0,iz],H1)
        true=T4[ih,iz]
        qt=rel(pred,true)
        pp=np.abs(pred)**2; pt=P4[ih,iz]
        qp=float(np.linalg.norm(pp-pt)/max(float(np.linalg.norm(pp)),float(np.linalg.norm(pt)),1e-300))
        qpeak=float(np.max(np.abs(pp-pt))/max(float(np.max(pt)),1e-300))
        hold_t.append(qt); hold_p.append(qp); hold_peak.append(qpeak)
        hold_rows.append({"z":float(z),"transfer_L2":float(qt),"power_L2":float(qp),"power_peak":float(qpeak)})
        for kmid in H1:
            j=idx(K1,kmid)
            right=int(np.searchsorted(K0,kmid)); left=right-1
            den=max(abs(T4[idx(K1,K0[left]),iz]),abs(T4[idx(K1,K0[right]),iz]),1e-12)
            ratio=float(abs(T4[j,iz])/den)
            smooth_max_ratio=max(smooth_max_ratio,ratio)
            if ratio>SMOOTH_FACTOR:
                smooth_ok=False

    kfine=np.exp(np.linspace(np.log(float(K1[0])),np.log(float(K1[-1])),401))
    fine_rows=[]; fine_t=[]; fine_p=[]; fine_peak=[]
    fine_T1=[]; fine_P1=[]
    fine_power_ok=True
    for iz,z in enumerate(CHECK_Z):
        t0=interp_complex(K0,T4[i0,iz],kfine)
        t1=interp_complex(K1,T4[:,iz],kfine)
        p0=interp_power(K0,P4[i0,iz],kfine)
        p1=interp_power(K1,P4[:,iz],kfine)
        fine_power_ok = fine_power_ok and bool(
            np.all(np.isfinite(t0)) and np.all(np.isfinite(t1))
            and np.all(np.isfinite(p0)) and np.all(np.isfinite(p1))
            and np.all(p0>=0.0) and np.all(p1>=0.0)
        )
        qt=rel(t0,t1)
        qp=float(np.linalg.norm(p0-p1)/max(float(np.linalg.norm(p0)),float(np.linalg.norm(p1)),1e-300))
        qpeak=float(np.max(np.abs(p0-p1))/max(float(np.max(p1)),1e-300))
        fine_t.append(qt); fine_p.append(qp); fine_peak.append(qpeak)
        fine_rows.append({"z":float(z),"transfer_L2":float(qt),"power_L2":float(qp),"power_peak":float(qpeak)})
        fine_T1.append(t1); fine_P1.append(p1)
    fine_T1=np.asarray(fine_T1,complex); fine_P1=np.asarray(fine_P1,float)

    lowk_sat={}
    for kh in (0.03,0.04,0.05):
        vals=[float(r["sat_max"]) for r in all_runs if r.get("finite") and abs(float(r["k_h"])-kh)<1e-12]
        lowk_sat[str(kh)]=float(max(vals)) if vals else float("inf")

    ensemble_rows=[]
    for ik,kh in enumerate(K1):
        for iz,z in enumerate(CHECK_Z):
            vals=A[:,ik,iz]; mean=T4[ik,iz]
            scat=float(np.sqrt(np.mean(np.abs(vals-mean)**2)))
            rms=float(np.sqrt(np.mean(np.abs(vals)**2)))
            pw=P[:,ik,iz]; mp=float(np.mean(pw)); sp=float(np.std(pw,ddof=1))
            ensemble_rows.append({
                "k_h_Mpc_inv":float(kh),"z":float(z),
                "mean_T_real":float(np.real(mean)),"mean_T_imag":float(np.imag(mean)),
                "scatter_over_rms":float(scat/max(rms,1e-300)),
                "mean_P_tag":mp,"cv_P_tag":float(sp/max(mp,1e-300)),
            })

    gates={
        "STR_G1_provenance_and_frozen_identity":bool(all(ancestry.values()) and frozen),
        "STR_G2_all_88_tagged_runs_finite_constraint_clean":bool(health_ok),
        "STR_G3_broadband_saturated_closure":bool(satmax<=SAT_GATE),
        "STR_G4_tagged_response_power_algebra":bool(algebra_ok),
        "STR_G5_common_geometry_regression_to_POC":bool(reg_med<=REG_MED_GATE and reg_max<=REG_MAX_GATE),
        "STR_G6_background_convergence_B2_to_B4":bool(bg_t_global<=BG_T_GLOBAL_GATE and bg_t_max<=BG_T_PERK_GATE and bg_p_global<=BG_P_GLOBAL_GATE and bg_p_max<=BG_P_PERK_GATE),
        "STR_G7_direct_K0_to_K1_holdout_accuracy":bool(max(hold_t)<=HOLD_T_GATE and max(hold_p)<=HOLD_P_GATE and max(hold_peak)<=HOLD_PEAK_GATE),
        "STR_G8_K0_to_K1_continuous_radial_convergence":bool(fine_power_ok and max(fine_t)<=FINE_T_GATE and max(fine_p)<=FINE_P_GATE and max(fine_peak)<=FINE_PEAK_GATE and np.median(fine_t)<=FINE_T_MED_GATE and np.median(fine_p)<=FINE_P_MED_GATE),
        "STR_G9_direct_radial_smoothness_spike_veto":bool(smooth_ok),
        "STR_G10_preserved_lowk_broadband_regime":bool(all(v<=SAT_GATE for v in lowk_sat.values())),
    }
    classification=PASS if all(gates.values()) else FAIL
    summary={
        "coefficient_sha256":digest,
        "runs_finite":int(sum(bool(r.get("finite",False)) for r in all_runs)),"runs_expected":88,
        "broadband_saturation_max":satmax,
        "tagged_power_identity_relative_residual":alg,
        "poc_regression_median":reg_med,"poc_regression_max":reg_max,
        "background_response_global":bg_t_global,"background_response_per_k_max":bg_t_max,
        "background_power_global":bg_p_global,"background_power_per_k_max":bg_p_max,
        "holdout_transfer_L2_max":float(max(hold_t)),"holdout_power_L2_max":float(max(hold_p)),"holdout_power_peak_max":float(max(hold_peak)),
        "fine_transfer_L2_median":float(np.median(fine_t)),"fine_transfer_L2_max":float(max(fine_t)),
        "fine_power_L2_median":float(np.median(fine_p)),"fine_power_L2_max":float(max(fine_p)),"fine_power_peak_max":float(max(fine_peak)),
        "fine_power_finite_nonnegative":bool(fine_power_ok),
        "smoothness_max_midpoint_to_endpoint_ratio":float(smooth_max_ratio),
        "lowk_saturation_max":lowk_sat,
        "ensemble_scatter_over_rms_max":float(max(r["scatter_over_rms"] for r in ensemble_rows)),
        "ensemble_power_cv_median":float(np.median([r["cv_P_tag"] for r in ensemble_rows])),
    }

    out={
        "classification":classification,"diagnostic_complete":True,
        "git_head":subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip(),
        "ancestry":ancestry,"gates":gates,"summary":summary,
        "seed":SEED,"coefficient_sha256":digest,"background_ids_B4":list(B4),"background_ids_B2":list(B2),
        "K0_h_Mpc_inv":K0.tolist(),"K1_h_Mpc_inv":K1.tolist(),"H1_h_Mpc_inv":H1.tolist(),
        "epsilon":EPS,"kF_h":KF_H,"NX":NX,"NSTEP":NSTEP,"box_Mpc":BOX,
        "redshifts":CHECK_Z.tolist(),"reference_member":REFERENCE_MEMBER,
        "runs":all_runs,"poc_regression":reg_rows,"background_convergence":bg_rows,
        "holdout_rows":hold_rows,"fine_convergence_rows":fine_rows,"ensemble_rows":ensemble_rows,
        "STOCHASTIC_TAGGED_RADIAL_CONTINUUM_LICENSED":bool(classification==PASS),
        "STOCHASTIC_TAGGED_BOUNDED_RESPONSE_TESTED":bool(classification==PASS),
        "THREE_D_BOUNDED_CONTINUOUS_WEYL_POWER_LICENSED":False,
        "THREE_D_CONTINUOUS_WEYL_POWER_LICENSED":False,
        "EVOLVING_WEYL_POWER_LICENSED":False,"ACT_LIKELIHOOD_LICENSED":False,"OBSERVATIONAL_CLAIM_LICENSED":False,
    }
    Path(args.json_out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    np.savez_compressed(
        args.npz_out,redshifts=CHECK_Z,K0=K0,K1=K1,H1=H1,background_ids=np.asarray(B4),
        response=A,power=P,Tbar4=T4,Pbar4=P4,Tbar2=T2,Pbar2=P2,
        fine_k=kfine,fine_T1=fine_T1,fine_P1=fine_P1,
    )
    with open(args.csv_out,"w",newline="") as f:
        fields=["background","k_h_Mpc_inv","z","T_real","T_imag","P_tag"]
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)

    print("FULLJ_TAGGED_RADIAL_SUMMARY="+json.dumps(summary,sort_keys=True),flush=True)
    print("FULLJ_TAGGED_RADIAL_GATES="+json.dumps(gates,sort_keys=True),flush=True)
    print("FULLJ_TAGGED_RADIAL_CLASSIFICATION="+classification,flush=True)
    print("STOCHASTIC_TAGGED_RADIAL_CONTINUUM_LICENSED="+str(classification==PASS),flush=True)
    print("STOCHASTIC_TAGGED_BOUNDED_RESPONSE_TESTED="+str(classification==PASS),flush=True)
    print("THREE_D_BOUNDED_CONTINUOUS_WEYL_POWER_LICENSED=False",flush=True)
    print("THREE_D_CONTINUOUS_WEYL_POWER_LICENSED=False",flush=True)
    print("EVOLVING_WEYL_POWER_LICENSED=False",flush=True)
    print("ACT_LIKELIHOOD_LICENSED=False",flush=True)
    print("OBSERVATIONAL_CLAIM_LICENSED=False",flush=True)
    return 0 if classification==PASS else 2


if __name__ == "__main__":
    raise SystemExit(main())
