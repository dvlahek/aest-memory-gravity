#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import subprocess
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fullj_weyl import stochastic_tagged_radial_convergence as prev
from fullj_weyl import stochastic_tagged_mode_poc as poc

r2 = prev.r2
m = prev.m
static = prev.static

R2_RESULT_LOCK = "1f42f88e9724c58d2d242a65ca7266a207e4a0f8"
SAT_RESULT_LOCK = "f6eb7099cffc9ae6f4fe11ddef1794f0e6dd6e4f"
CARDINALITY_RESULT_LOCK = "df182a828b3c140fba22f1f5d58414ec41017e7b"
POC_RESULT_LOCK = "aff670fa8551163f5cde2b5146e0e5840d53b424"
K1_FAIL_RESULT_LOCK = "2531a10772f97958ab221bd1f39ceffc23e964a5"
HISTORY_LOCK = "c80b8034787be17b20d6757f3043a0a55c49f68a"
PREDATA_LOCK = "acb6d26c0778d9bffa27248b26ffc55a99558ddd"

PASS = "FULLJ_STOCHASTIC_TAGGED_RADIAL_K2_REFINEMENT_PASS"
FAIL = "FULLJ_STOCHASTIC_TAGGED_RADIAL_K2_REFINEMENT_FAIL"
INCOMPLETE = "FULLJ_STOCHASTIC_TAGGED_RADIAL_K2_REFINEMENT_INCOMPLETE"

SEED = prev.SEED
COEFF_HASH = prev.COEFF_HASH
B4 = prev.B4
B2 = prev.B2
K1 = np.asarray(prev.K1, float)
H2 = np.asarray([0.035,0.045,0.055,0.070,0.085,0.095,0.110,0.135,0.160,0.185], float)
K2 = np.asarray(sorted(set(np.round(np.concatenate([K1,H2]), 14))), float)
CHECK_Z = np.asarray(prev.CHECK_Z, float)
EPS = prev.EPS
KF_H = prev.KF_H
NX = prev.NX
NSTEP = prev.NSTEP
BOX = prev.BOX
REFERENCE_MEMBER = dict(prev.REFERENCE_MEMBER)

CANONICAL_GATE = prev.CANONICAL_GATE
METRIC_GATE = prev.METRIC_GATE
SAT_GATE = prev.SAT_GATE
ALG_GATE = prev.ALG_GATE
BG_T_GLOBAL_GATE = prev.BG_T_GLOBAL_GATE
BG_T_PERK_GATE = prev.BG_T_PERK_GATE
BG_P_GLOBAL_GATE = prev.BG_P_GLOBAL_GATE
BG_P_PERK_GATE = prev.BG_P_PERK_GATE
HOLD_T_GATE = prev.HOLD_T_GATE
HOLD_P_GATE = prev.HOLD_P_GATE
HOLD_PEAK_GATE = prev.HOLD_PEAK_GATE
FINE_T_GATE = prev.FINE_T_GATE
FINE_P_GATE = prev.FINE_P_GATE
FINE_PEAK_GATE = prev.FINE_PEAK_GATE
FINE_T_MED_GATE = prev.FINE_T_MED_GATE
FINE_P_MED_GATE = prev.FINE_P_MED_GATE
SMOOTH_FACTOR = prev.SMOOTH_FACTOR

OLD_JSON = ROOT / "results/fullj_stochastic_tagged_radial_convergence.json"
OLD_NPZ = ROOT / "results/fullj_stochastic_tagged_radial_convergence.npz"


def is_ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"], cwd=ROOT,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    ).returncode == 0


def idx(grid, value):
    q = np.where(np.isclose(np.asarray(grid,float), float(value), rtol=0.0, atol=5e-13))[0]
    if len(q) != 1:
        raise RuntimeError(f"nonunique radial node {value}")
    return int(q[0])


def rel(a, b):
    return prev.rel(a,b)


def load_locked_k1():
    if not OLD_JSON.exists() or not OLD_NPZ.exists():
        raise FileNotFoundError("missing locked K0->K1 local JSON/NPZ")
    meta = json.loads(OLD_JSON.read_text())
    if meta.get("classification") != "FULLJ_STOCHASTIC_TAGGED_RADIAL_CONVERGENCE_FAIL":
        raise RuntimeError("locked K1 JSON does not preserve historical FAIL")
    g = meta.get("gates", {})
    required_true = [
        "STR_G1_provenance_and_frozen_identity",
        "STR_G2_all_88_tagged_runs_finite_constraint_clean",
        "STR_G3_broadband_saturated_closure",
        "STR_G4_tagged_response_power_algebra",
        "STR_G5_common_geometry_regression_to_POC",
        "STR_G6_background_convergence_B2_to_B4",
        "STR_G9_direct_radial_smoothness_spike_veto",
        "STR_G10_preserved_lowk_broadband_regime",
    ]
    if not all(g.get(x) is True for x in required_true):
        raise RuntimeError("locked K1 non-radial gates are not all true")
    if g.get("STR_G7_direct_K0_to_K1_holdout_accuracy") is not False or g.get("STR_G8_K0_to_K1_continuous_radial_convergence") is not False:
        raise RuntimeError("locked K1 radial FAIL gates not preserved")
    q = np.load(OLD_NPZ)
    old_k1 = np.asarray(q["K1"], float)
    A1 = np.asarray(q["response"], complex)
    if old_k1.shape != K1.shape or not np.allclose(old_k1,K1,rtol=0,atol=5e-14):
        raise RuntimeError("locked K1 NPZ radial grid mismatch")
    if A1.shape != (len(B4),len(K1),len(CHECK_Z)):
        raise RuntimeError(f"locked K1 response shape mismatch {A1.shape}")
    if not np.all(np.isfinite(A1)):
        raise RuntimeError("locked K1 response contains nonfinite values")
    return meta, A1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json-out", default="results/fullj_stochastic_tagged_radial_k2_refinement.json")
    ap.add_argument("--npz-out", default="results/fullj_stochastic_tagged_radial_k2_refinement.npz")
    ap.add_argument("--csv-out", default="results/fullj_stochastic_tagged_radial_k2_refinement.csv")
    args = ap.parse_args()

    ancestry = {
        "r2_result_lock": is_ancestor(R2_RESULT_LOCK),
        "gaussian_1d_result_lock": bool(poc.gaussian_lock_ok()),
        "saturated_closure_result_lock": is_ancestor(SAT_RESULT_LOCK),
        "cardinality_result_lock": is_ancestor(CARDINALITY_RESULT_LOCK),
        "tagged_poc_result_lock": is_ancestor(POC_RESULT_LOCK),
        "k1_fail_result_lock": is_ancestor(K1_FAIL_RESULT_LOCK),
        "history_lock": is_ancestor(HISTORY_LOCK),
        "predata_lock": is_ancestor(PREDATA_LOCK),
    }
    _, gcoef, digest = poc.coeff_draw()
    expected_h2 = np.asarray([0.035,0.045,0.055,0.070,0.085,0.095,0.110,0.135,0.160,0.185],float)
    expected_k2 = np.asarray([0.03,0.035,0.04,0.045,0.05,0.055,0.065,0.070,0.08,0.085,0.09,0.095,0.10,0.110,0.125,0.135,0.15,0.160,0.175,0.185,0.20],float)
    grid_ok = bool(
        np.allclose(H2,expected_h2,rtol=0,atol=5e-14)
        and np.allclose(K2,expected_k2,rtol=0,atol=5e-14)
        and all(abs(round(k/KF_H)*KF_H-k)<5e-13 for k in K2)
        and len(K2)==21 and len(H2)==10
    )
    frozen = bool(
        digest==COEFF_HASH and B4==(0,1,2,3) and B2==(0,1)
        and EPS==0.05 and KF_H==0.005 and NX==256 and NSTEP==4096
        and grid_ok and REFERENCE_MEMBER=={"sigma":0,"kind":"simple","beta0":1.0}
    )

    print("FULLJ_TAGGED_K2_START", flush=True)
    print("FULLJ_TAGGED_K2_ANCESTRY="+json.dumps(ancestry,sort_keys=True), flush=True)
    print("FULLJ_TAGGED_K2_COEFFICIENT_SHA256="+digest, flush=True)
    print("FULLJ_TAGGED_K2_H2="+json.dumps(H2.tolist()), flush=True)
    print("FULLJ_TAGGED_K2_K2="+json.dumps(K2.tolist()), flush=True)
    print(f"FULLJ_TAGGED_K2_GEOMETRY kF_h={KF_H:.6f} NX={NX} box_Mpc={BOX:.12e}", flush=True)

    try:
        old_meta, A1 = load_locked_k1()
    except Exception as exc:
        out={"classification":INCOMPLETE,"diagnostic_complete":False,"ancestry":ancestry,"frozen_setup":frozen,"reason":str(exc)}
        Path(args.json_out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
        print("FULLJ_TAGGED_K2_CLASSIFICATION="+INCOMPLETE, flush=True)
        return 3

    if not all(ancestry.values()) or not frozen:
        out={"classification":INCOMPLETE,"diagnostic_complete":False,"ancestry":ancestry,"frozen_setup":frozen,"coefficient_sha256":digest}
        Path(args.json_out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
        print("FULLJ_TAGGED_K2_CLASSIFICATION="+INCOMPLETE, flush=True)
        return 3

    old_kmpc=np.asarray(m.K_MPC,float).copy()
    old_kh=np.asarray(getattr(m,"K_H",prev.K0),float).copy()
    Anew=np.full((len(B4),len(H2),len(CHECK_Z)),np.nan+1j*np.nan,complex)
    all_runs=[]; rows=[]; run_index=0
    try:
        for ih,kh in enumerate(H2):
            mode_h=poc.target_modes(float(kh))
            m.K_H=mode_h.copy(); m.K_MPC=mode_h*float(static.h)
            data=r2.r0.prepare_bridge_data()
            for ib,bgid in enumerate(B4):
                pair={}; meta=None
                for sign in (+1,-1):
                    run_index+=1
                    rec, wh, mm = prev.run_signed_common(data,mode_h,gcoef[bgid],bgid,float(kh),sign)
                    rec["run_index"]=int(run_index)
                    all_runs.append(rec)
                    print(
                        f"FULLJ_TAGGED_K2_RUN {run_index:03d}/80 bg={bgid} k_h={kh:.6f} sign={sign:+d} "
                        + (f"canonical={rec['canonical_max']:.3e} satMax={rec['sat_max']:.3e}" if rec.get("finite") else f"finite=False reason={rec.get('reason','unknown')}"),
                        flush=True,
                    )
                    if wh is not None:
                        pair[sign]=wh; meta=mm
                if len(pair)==2:
                    T=(pair[+1]-pair[-1])*np.exp(-1j*float(meta["phase_tag"]))/(EPS*float(meta["amp_tag"]))
                    Anew[ib,ih,:]=T
                    for iz,z in enumerate(CHECK_Z):
                        rows.append({"background":int(bgid),"k_h_Mpc_inv":float(kh),"z":float(z),
                                     "T_real":float(np.real(T[iz])),"T_imag":float(np.imag(T[iz])),"P_tag":float(abs(T[iz])**2)})
    finally:
        m.K_MPC=old_kmpc; m.K_H=old_kh

    all_finite=len(all_runs)==80 and all(bool(r.get("finite",False)) for r in all_runs)
    health_ok=bool(all_finite and all(
        float(r["canonical_max"])<=CANONICAL_GATE and all(float(v)<=METRIC_GATE for v in r["metric_max"].values())
        for r in all_runs
    ))
    satmax=float(max([r.get("sat_max",float("inf")) for r in all_runs],default=float("inf")))

    Pnew=np.abs(Anew)**2
    back=np.real(Anew)**2+np.imag(Anew)**2
    alg=float(np.linalg.norm(Pnew-back)/max(float(np.linalg.norm(Pnew)),1e-300)) if np.all(np.isfinite(Anew)) else float("inf")
    algebra_ok=bool(np.all(np.isfinite(Anew)) and np.all(np.isfinite(Pnew)) and np.all(Pnew>=0) and alg<=ALG_GATE)

    # Background convergence on the ten new direct nodes.
    Tn4=np.mean(Anew,axis=0); Tn2=np.mean(Anew[:2],axis=0)
    Pn4=np.mean(Pnew,axis=0); Pn2=np.mean(Pnew[:2],axis=0)
    bg_t_global=rel(Tn2,Tn4)
    bg_p_global=float(np.linalg.norm(Pn2-Pn4)/max(float(np.linalg.norm(Pn2)),float(np.linalg.norm(Pn4)),1e-300))
    bg_rows=[]; bg_t_pk=[]; bg_p_pk=[]
    for ih,kh in enumerate(H2):
        qt=rel(Tn2[ih],Tn4[ih])
        qp=float(np.linalg.norm(Pn2[ih]-Pn4[ih])/max(float(np.linalg.norm(Pn2[ih])),float(np.linalg.norm(Pn4[ih])),1e-300))
        bg_t_pk.append(qt); bg_p_pk.append(qp)
        bg_rows.append({"k_h_Mpc_inv":float(kh),"response_relative_L2":float(qt),"power_relative_L2":float(qp)})
    bg_t_max=float(np.max(bg_t_pk)); bg_p_max=float(np.max(bg_p_pk))

    # Merge immutable K1 and new H2 into K2.
    A2=np.full((len(B4),len(K2),len(CHECK_Z)),np.nan+1j*np.nan,complex)
    for ik,k in enumerate(K1):
        A2[:,idx(K2,k),:]=A1[:,ik,:]
    for ih,k in enumerate(H2):
        A2[:,idx(K2,k),:]=Anew[:,ih,:]
    if not np.all(np.isfinite(A2)):
        raise RuntimeError("merged K2 response is incomplete")
    P1=np.abs(A1)**2; P2=np.abs(A2)**2
    Tbar1=np.mean(A1,axis=0); Pbar1=np.mean(P1,axis=0)
    Tbar2=np.mean(A2,axis=0); Pbar2=np.mean(P2,axis=0)

    # Direct K1->K2 holdouts on H2.
    hold_rows=[]; hold_t=[]; hold_p=[]; hold_peak=[]
    smooth_ok=True; smooth_max_ratio=0.0
    for iz,z in enumerate(CHECK_Z):
        pred=prev.interp_complex(K1,Tbar1[:,iz],H2)
        true=Tn4[:,iz]
        qt=rel(pred,true)
        pp=np.abs(pred)**2; pt=Pn4[:,iz]
        qp=float(np.linalg.norm(pp-pt)/max(float(np.linalg.norm(pp)),float(np.linalg.norm(pt)),1e-300))
        qpeak=float(np.max(np.abs(pp-pt))/max(float(np.max(pt)),1e-300))
        hold_t.append(qt); hold_p.append(qp); hold_peak.append(qpeak)
        hold_rows.append({"z":float(z),"transfer_L2":float(qt),"power_L2":float(qp),"power_peak":float(qpeak)})
        for ih,kh in enumerate(H2):
            right=int(np.searchsorted(K1,kh)); left=right-1
            den=max(abs(Tbar1[left,iz]),abs(Tbar1[right,iz]),1e-12)
            ratio=float(abs(true[ih])/den)
            smooth_max_ratio=max(smooth_max_ratio,ratio)
            if ratio>SMOOTH_FACTOR:
                smooth_ok=False

    # Continuous K1->K2 convergence.
    kfine=np.exp(np.linspace(np.log(float(K2[0])),np.log(float(K2[-1])),401))
    fine_rows=[]; fine_t=[]; fine_p=[]; fine_peak=[]; fine_T2=[]; fine_P2=[]
    fine_power_ok=True
    for iz,z in enumerate(CHECK_Z):
        t1=prev.interp_complex(K1,Tbar1[:,iz],kfine)
        t2=prev.interp_complex(K2,Tbar2[:,iz],kfine)
        p1=prev.interp_power(K1,Pbar1[:,iz],kfine)
        p2=prev.interp_power(K2,Pbar2[:,iz],kfine)
        fine_power_ok = fine_power_ok and bool(np.all(np.isfinite(p2)) and np.all(p2>=0))
        qt=rel(t1,t2)
        qp=float(np.linalg.norm(p1-p2)/max(float(np.linalg.norm(p1)),float(np.linalg.norm(p2)),1e-300))
        qpeak=float(np.max(np.abs(p1-p2))/max(float(np.max(p2)),1e-300))
        fine_t.append(qt); fine_p.append(qp); fine_peak.append(qpeak)
        fine_rows.append({"z":float(z),"transfer_L2":float(qt),"power_L2":float(qp),"power_peak":float(qpeak)})
        fine_T2.append(t2); fine_P2.append(p2)
    fine_T2=np.asarray(fine_T2,complex); fine_P2=np.asarray(fine_P2,float)

    # Refinement improvement against locked K0->K1 direct-holdout rows.
    old_by_z={float(r["z"]):r for r in old_meta["holdout_rows"]}
    improve_rows=[]; improve_t=[]; improve_p=[]
    for r in hold_rows:
        z=float(r["z"]); old=old_by_z[z]
        it=bool(float(r["transfer_L2"])<=float(old["transfer_L2"]))
        ip=bool(float(r["power_L2"])<=float(old["power_L2"]))
        improve_t.append(it); improve_p.append(ip)
        improve_rows.append({"z":z,"old_transfer_L2":float(old["transfer_L2"]),"new_transfer_L2":float(r["transfer_L2"]),
                             "old_power_L2":float(old["power_L2"]),"new_power_L2":float(r["power_L2"]),
                             "transfer_improved":it,"power_improved":ip})

    gates={
        "K2_G1_provenance_and_locked_K1_identity":bool(all(ancestry.values()) and frozen),
        "K2_G2_all_80_new_runs_finite_constraint_clean":bool(health_ok),
        "K2_G3_broadband_saturated_closure":bool(satmax<=SAT_GATE),
        "K2_G4_tagged_response_power_algebra":bool(algebra_ok),
        "K2_G5_new_node_background_convergence_B2_to_B4":bool(bg_t_global<=BG_T_GLOBAL_GATE and bg_t_max<=BG_T_PERK_GATE and bg_p_global<=BG_P_GLOBAL_GATE and bg_p_max<=BG_P_PERK_GATE),
        "K2_G6_direct_K1_to_K2_holdout_accuracy":bool(max(hold_t)<=HOLD_T_GATE and max(hold_p)<=HOLD_P_GATE and max(hold_peak)<=HOLD_PEAK_GATE),
        "K2_G7_continuous_K1_to_K2_radial_convergence":bool(max(fine_t)<=FINE_T_GATE and max(fine_p)<=FINE_P_GATE and max(fine_peak)<=FINE_PEAK_GATE and np.median(fine_t)<=FINE_T_MED_GATE and np.median(fine_p)<=FINE_P_MED_GATE and fine_power_ok),
        "K2_G8_direct_radial_smoothness_spike_veto":bool(smooth_ok),
        "K2_G9_refinement_improves_every_redshift":bool(all(improve_t) and all(improve_p)),
    }
    classification=PASS if all(gates.values()) else FAIL

    summary={
        "coefficient_sha256":digest,"runs_finite":int(sum(bool(r.get("finite",False)) for r in all_runs)),"runs_expected":80,
        "broadband_saturation_max":satmax,"tagged_power_identity_relative_residual":alg,
        "background_response_global":bg_t_global,"background_response_per_k_max":bg_t_max,
        "background_power_global":bg_p_global,"background_power_per_k_max":bg_p_max,
        "holdout_transfer_L2_max":float(max(hold_t)),"holdout_power_L2_max":float(max(hold_p)),"holdout_power_peak_max":float(max(hold_peak)),
        "fine_transfer_L2_median":float(np.median(fine_t)),"fine_transfer_L2_max":float(max(fine_t)),
        "fine_power_L2_median":float(np.median(fine_p)),"fine_power_L2_max":float(max(fine_p)),"fine_power_peak_max":float(max(fine_peak)),
        "fine_power_finite_nonnegative":bool(fine_power_ok),
        "smoothness_max_interior_to_endpoint_ratio":float(smooth_max_ratio),
        "refinement_transfer_improved_redshifts":int(sum(improve_t)),
        "refinement_power_improved_redshifts":int(sum(improve_p)),
    }

    out={
        "classification":classification,"diagnostic_complete":True,
        "git_head":subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip(),
        "ancestry":ancestry,"gates":gates,"summary":summary,
        "seed":SEED,"coefficient_sha256":digest,"background_ids_B4":list(B4),"background_ids_B2":list(B2),
        "K1_h_Mpc_inv":K1.tolist(),"H2_h_Mpc_inv":H2.tolist(),"K2_h_Mpc_inv":K2.tolist(),
        "epsilon":EPS,"kF_h":KF_H,"NX":NX,"NSTEP":NSTEP,"box_Mpc":BOX,
        "redshifts":CHECK_Z.tolist(),"reference_member":REFERENCE_MEMBER,
        "runs":all_runs,"background_convergence":bg_rows,"holdout_rows":hold_rows,
        "fine_convergence_rows":fine_rows,"refinement_improvement":improve_rows,
        "STOCHASTIC_TAGGED_RADIAL_CONTINUUM_LICENSED":bool(classification==PASS),
        "STOCHASTIC_TAGGED_BOUNDED_RESPONSE_TESTED":bool(classification==PASS),
        "THREE_D_BOUNDED_CONTINUOUS_WEYL_POWER_LICENSED":False,
        "THREE_D_CONTINUOUS_WEYL_POWER_LICENSED":False,
        "EVOLVING_WEYL_POWER_LICENSED":False,"ACT_LIKELIHOOD_LICENSED":False,"OBSERVATIONAL_CLAIM_LICENSED":False,
    }
    Path(args.json_out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    np.savez_compressed(args.npz_out,redshifts=CHECK_Z,K1=K1,H2=H2,K2=K2,background_ids=np.asarray(B4),
                        response_new=Anew,response_K2=A2,power_K2=P2,Tbar2=Tbar2,Pbar2=Pbar2,
                        fine_k=kfine,fine_T2=fine_T2,fine_P2=fine_P2)
    with open(args.csv_out,"w",newline="") as f:
        fields=["background","k_h_Mpc_inv","z","T_real","T_imag","P_tag"]
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)

    print("FULLJ_TAGGED_K2_SUMMARY="+json.dumps(summary,sort_keys=True),flush=True)
    print("FULLJ_TAGGED_K2_GATES="+json.dumps(gates,sort_keys=True),flush=True)
    print("FULLJ_TAGGED_K2_CLASSIFICATION="+classification,flush=True)
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
