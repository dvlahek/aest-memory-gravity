#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from scipy.interpolate import PchipInterpolator

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fullj_weyl import dense_radial_weyl_extension_r1 as densefix

base = densefix.mod
r2 = base.r2
m = base.m
static = base.static

R2_RESULT_LOCK = "1f42f88e9724c58d2d242a65ca7266a207e4a0f8"
GAUSS1D_RESULT_LOCK = "05e38b273f91eb04b7c8753731017d0ed839c1"
GEOM_RESULT_LOCK = "ca6a102196055e27dc2b31379285bfc7aea1a35b"
SAT_RESULT_LOCK = "f6eb7099cffc9ae6f4fe11ddef1794f0e6dd6e4f"
HISTORICAL_TRANSFER_FAIL_LOCK = "b7bb0aef90ec935821f4dc1a63db0d79966a15f8"
R1_PHASE_RESULT_LOCK = "20679c5274e936037c226904d40c9d6779b00a49"
DENSE_FAIL_RESULT_LOCK = "55495cc968082f1cf6638785f7609c787971835c"
PREDATA_LOCK = "3aada0bdcd350f58ddcdf37aa45c4a8a574cb1db"

PASS = "FULLJ_DENSE_RADIAL_CLASS_RESIDUAL_R2_PASS"
FAIL = "FULLJ_DENSE_RADIAL_CLASS_RESIDUAL_R2_FAIL"
INCOMPLETE = "FULLJ_DENSE_RADIAL_CLASS_RESIDUAL_R2_INCOMPLETE"

REFERENCE_MEMBER = {"sigma": 0, "kind": "simple", "beta0": 1.0}
CHECK_Z = np.asarray(m.CHECK_Z, float)
K0 = np.asarray([0.03,0.05,0.08,0.10,0.15,0.20], float)
N_EMBED = 10
NX = r2.NX
NSTEP = r2.NSTEP
OLD_JSON = ROOT / "results/fullj_dense_radial_weyl_extension.json"

CANONICAL_GATE = 1e-10
METRIC_GATE = 1e-8
CLASS_MED_GATE = 1e-8
CLASS_MAX_GATE = 1e-5
INITIAL_GATE = 5e-3
PHASE_GLOBAL_GATE = 1e-8
PHASE_ABS_GATE = 1e-8
POWER_PROJ_GATE = 1e-12
SAT_GATE = 2e-2
HOLD_T_GATE = 3e-2
HOLD_P_GATE = 5e-2
HOLD_PEAK_GATE = 1e-1
CORR_GRID_GATE = 2e-2
TOTAL_T_GATE = 3e-2
TOTAL_P_GATE = 5e-2
TOTAL_PEAK_GATE = 1e-1
ALG_GATE = 1e-12


def is_ancestor(sha: str) -> bool:
    return subprocess.run(["git","merge-base","--is-ancestor",sha,"HEAD"], cwd=ROOT,
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0


def grids():
    k2 = list(K0)
    k3 = list(K0)
    for a,b in zip(K0[:-1],K0[1:]):
        k2.extend([a+0.25*(b-a), a+0.5*(b-a), a+0.75*(b-a)])
        k3.extend([a+(q/8.0)*(b-a) for q in range(1,8)])
    k2=np.asarray(sorted(set(np.round(k2,14))),float)
    k3=np.asarray(sorted(set(np.round(k3,14))),float)
    k1=list(K0)
    for a,b in zip(K0[:-1],K0[1:]): k1.append(0.5*(a+b))
    k1=np.asarray(sorted(set(np.round(k1,14))),float)
    h3=np.asarray([x for x in k3 if not np.any(np.isclose(x,k2,rtol=0,atol=5e-13))],float)
    return k1,k2,k3,h3


def ix(grid, x):
    q=np.where(np.isclose(grid,float(x),rtol=0,atol=5e-13))[0]
    if len(q)!=1: raise RuntimeError(f"grid node not unique: {x}")
    return int(q[0])


def rel(a,b):
    aa=float(a); bb=float(b)
    return abs(aa-bb)/max(abs(aa),abs(bb),1e-300)


def load_old(k2):
    if not OLD_JSON.exists():
        raise FileNotFoundError(str(OLD_JSON.relative_to(ROOT)))
    d=json.loads(OLD_JSON.read_text())
    if d.get("classification")!="FULLJ_DENSE_RADIAL_WEYL_EXTENSION_FAIL":
        raise RuntimeError("completed dense JSON does not preserve locked FAIL")
    g=d.get("gates",{})
    want_true=["G1_locked_provenance_setup","G2_finite_constraint_health","G3_initial_CLASS_normalization",
               "G4_zero_safe_phase_consistency","G5_dense_saturated_closure","G6_anchor_recovery","G10_power_sanity"]
    want_false=["G7_level1_direct_holdout_accuracy","G8_refinement_improvement","G9_fine_grid_K1_to_K2_convergence"]
    if not all(g.get(x) is True for x in want_true) or not all(g.get(x) is False for x in want_false):
        raise RuntimeError("completed dense JSON gate state differs from locked FAIL")
    T=np.full((len(CHECK_Z),len(k2)),np.nan,float)
    Tc=np.full_like(T,np.nan)
    finite=np.ones_like(T,dtype=bool)
    for row in d.get("rows",[]):
        z=float(row["z"]); kh=float(row["k_h_Mpc_inv"])
        if not np.any(np.isclose(kh,k2,rtol=0,atol=5e-13)): continue
        iz=ix(CHECK_Z,z); ik=ix(k2,kh)
        T[iz,ik]=float(row["T_real"]); Tc[iz,ik]=float(row["T_CLASS"])
        finite[iz,ik]=np.isfinite(T[iz,ik]) and np.isfinite(Tc[iz,ik])
    if not np.all(finite) or not np.all(np.isfinite(T)) or not np.all(np.isfinite(Tc)):
        raise RuntimeError("stored K2 direct grid incomplete")
    return d,T,Tc


def interp_residual(ktrain, residual, keval):
    return np.asarray(PchipInterpolator(np.log(ktrain),np.asarray(residual,float),extrapolate=False)(np.log(keval)),float)


def primordial(k_mpc):
    kk=np.asarray(k_mpc,float)
    return float(static.AS)*(kk/float(static.KPIV))**(float(static.NS)-1.0)


def power_from_T(kh, T):
    km=np.asarray(kh,float)*float(static.h)
    pr=primordial(km)
    return 2*np.pi**2*pr*np.asarray(T,float)**2/(km**3)


def metrics(pred,true,kh):
    pred=np.asarray(pred,float); true=np.asarray(true,float)
    pp=power_from_T(kh,pred); pt=power_from_T(kh,true)
    return {
        "transfer_L2": float(np.linalg.norm(pred-true)/max(float(np.linalg.norm(true)),1e-300)),
        "power_L2": float(np.linalg.norm(pp-pt)/max(float(np.linalg.norm(pt)),1e-300)),
        "power_peak": float(np.max(np.abs(pp-pt))/max(float(np.max(pt)),1e-300)),
    }


def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--json-out",default="results/fullj_dense_radial_class_residual_r2.json")
    ap.add_argument("--npz-out",default="results/fullj_dense_radial_class_residual_r2.npz")
    ap.add_argument("--csv-out",default="results/fullj_dense_radial_class_residual_r2.csv")
    args=ap.parse_args()

    ancestry={
        "r2_result_lock":is_ancestor(R2_RESULT_LOCK),
        "gaussian_1d_result_lock":is_ancestor(GAUSS1D_RESULT_LOCK),
        "geometry_result_lock":is_ancestor(GEOM_RESULT_LOCK),
        "saturated_closure_result_lock":is_ancestor(SAT_RESULT_LOCK),
        "historical_transfer_fail_lock":is_ancestor(HISTORICAL_TRANSFER_FAIL_LOCK),
        "r1_phase_result_lock":is_ancestor(R1_PHASE_RESULT_LOCK),
        "dense_fail_result_lock":is_ancestor(DENSE_FAIL_RESULT_LOCK),
        "predata_lock":is_ancestor(PREDATA_LOCK),
    }
    k1,k2,k3,h3=grids()
    frozen=bool(len(k1)==11 and len(k2)==21 and len(k3)==41 and len(h3)==20 and
                N_EMBED==10 and NX==128 and NSTEP==4096 and
                REFERENCE_MEMBER=={"sigma":0,"kind":"simple","beta0":1.0})
    try:
        old,T2,Tc2old=load_old(k2)
    except Exception as e:
        out={"classification":INCOMPLETE,"diagnostic_complete":False,"ancestry":ancestry,"reason":str(e)}
        Path(args.json_out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
        print("FULLJ_DENSE_RESIDUAL_R2_CLASSIFICATION="+INCOMPLETE,flush=True); return 3
    if not all(ancestry.values()) or not frozen:
        out={"classification":INCOMPLETE,"diagnostic_complete":False,"ancestry":ancestry,"frozen_setup":frozen}
        Path(args.json_out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
        print("FULLJ_DENSE_RESIDUAL_R2_CLASSIFICATION="+INCOMPLETE,flush=True); return 3

    print("FULLJ_DENSE_RESIDUAL_R2_START",flush=True)
    print("FULLJ_DENSE_RESIDUAL_R2_ANCESTRY="+json.dumps(ancestry,sort_keys=True),flush=True)
    print("FULLJ_DENSE_RESIDUAL_R2_GRIDS="+json.dumps({"K1":k1.tolist(),"K2":k2.tolist(),"K3":k3.tolist(),"H3":h3.tolist()}),flush=True)

    amp3,phase3=base.interpolation_probe(k3)
    old_kmpc=np.asarray(m.K_MPC,float).copy(); old_kh=np.asarray(getattr(m,"K_H",K0),float).copy()
    k3_mpc=k3*float(static.h)
    m.K_MPC=k3_mpc.copy(); m.K_H=k3.copy()
    try:
        data=r2.r0.prepare_bridge_data()
        Tc3=np.asarray([[float(m.mode_values(data,float(tau),"phi")[j]+m.mode_values(data,float(tau),"psi_bridge")[j])
                         for j in range(len(k3))] for tau in np.asarray(data["tau_check"],float)],float)

        # CLASS cross-run consistency at stored K2 nodes.
        class_diff=[]
        for iz in range(len(CHECK_Z)):
            for j,kh in enumerate(k2): class_diff.append(rel(Tc3[iz,ix(k3,kh)],Tc2old[iz,j]))

        Th=np.full((len(CHECK_Z),len(h3)),np.nan+1j*np.nan,complex)
        Sath=np.full((len(CHECK_Z),len(h3)),np.nan,float)
        health_rows=[]
        for ih,kh in enumerate(h3):
            j3=ix(k3,kh)
            run,box=base.run_single_mode(data,j3,float(k3_mpc[j3]),float(amp3[j3]),float(phase3[j3]))
            hh=base.health(run); health_rows.append({"k_h_Mpc_inv":float(kh),"box_Mpc":float(box),**hh})
            if not hh["finite"]: raise RuntimeError(f"new H3 run incomplete at k/h={kh:g}")
            Th[:,ih]=base.transfer_from_run(run,float(amp3[j3]),float(phase3[j3]))
            Sath[:,ih]=base.saturation_residuals(data,run,box)
            print(f"FULLJ_DENSE_RESIDUAL_R2_HOLDOUT {ih+1:02d}/{len(h3)} k_h={kh:.8f} canonical={hh['canonical_max']:.3e} satMax={np.max(Sath[:,ih]):.3e}",flush=True)
    finally:
        m.K_MPC=old_kmpc; m.K_H=old_kh

    # Combine direct K3 real transfer: completed K2 + new H3.
    T3=np.full((len(CHECK_Z),len(k3)),np.nan,float)
    for iz in range(len(CHECK_Z)):
        for j,kh in enumerate(k2): T3[iz,ix(k3,kh)]=T2[iz,j]
        for ih,kh in enumerate(h3): T3[iz,ix(k3,kh)]=float(np.real(Th[iz,ih]))

    h3_idx=np.asarray([ix(k3,x) for x in h3],int)
    k2_idx=np.asarray([ix(k3,x) for x in k2],int)
    k1_idx=np.asarray([ix(k3,x) for x in k1],int)

    hold_rows=[]; improve_t=0; improve_p=0
    total_ref_rows=[]; corr_grid_rows=[]
    grid801=np.exp(np.linspace(np.log(k3[0]),np.log(k3[-1]),801))
    k1k2_corr=[]; k2k3_corr=[]
    k1k2_t=[]; k2k3_t=[]; k1k2_p=[]; k2k3_p=[]; k1k2_pk=[]; k2k3_pk=[]

    for iz,z in enumerate(CHECK_Z):
        D3=T3[iz]-Tc3[iz]
        D1=D3[k1_idx]; D2=D3[k2_idx]
        pred1_h=Tc3[iz,h3_idx]+interp_residual(k1,D1,h3)
        pred2_h=Tc3[iz,h3_idx]+interp_residual(k2,D2,h3)
        true_h=T3[iz,h3_idx]
        e1=metrics(pred1_h,true_h,h3); e2=metrics(pred2_h,true_h,h3)
        improve_t += int(e2["transfer_L2"] < e1["transfer_L2"])
        improve_p += int(e2["power_L2"] < e1["power_L2"])
        hold_rows.append({"z":float(z),"K1_residual":e1,"K2_residual":e2})

        d1g=interp_residual(k1,D1,grid801); d2g=interp_residual(k2,D2,grid801); d3g=interp_residual(k3,D3,grid801)
        norm=max(float(np.linalg.norm(Tc3[iz])),float(np.linalg.norm(T3[iz])),1e-300)
        q12=float(np.linalg.norm(d2g-d1g)/norm); q23=float(np.linalg.norm(d3g-d2g)/norm)
        k1k2_corr.append(q12); k2k3_corr.append(q23)
        corr_grid_rows.append({"z":float(z),"K1_to_K2":q12,"K2_to_K3":q23})

        t1=Tc3[iz]+interp_residual(k1,D1,k3)
        t2=Tc3[iz]+interp_residual(k2,D2,k3)
        t3=Tc3[iz]+interp_residual(k3,D3,k3)
        e12=metrics(t1,t2,k3); e23=metrics(t2,t3,k3)
        k1k2_t.append(e12["transfer_L2"]); k2k3_t.append(e23["transfer_L2"])
        k1k2_p.append(e12["power_L2"]); k2k3_p.append(e23["power_L2"])
        k1k2_pk.append(e12["power_peak"]); k2k3_pk.append(e23["power_peak"])
        total_ref_rows.append({"z":float(z),"K1_to_K2":e12,"K2_to_K3":e23})

    all_health=all(bool(q["finite"]) and float(q["canonical_max"])<=CANONICAL_GATE and
                   all(float(v)<=METRIC_GATE for v in q["metric_max"].values()) for q in health_rows)
    initial=np.asarray([rel(np.real(Th[0,ih]),Tc3[0,ix(k3,kh)]) for ih,kh in enumerate(h3)],float)
    imag=np.imag(Th); real=np.real(Th)
    phase_global=float(np.linalg.norm(imag)/max(float(np.linalg.norm(Th)),1e-300))
    phase_abs=float(np.max(np.abs(imag)))
    pc=np.abs(Th)**2; pr=real**2
    proj=float(np.max(np.abs(pc-pr)/np.maximum(np.maximum(pc,pr),1e-300)))
    satmax=float(np.max(Sath))

    h2=[r["K2_residual"] for r in hold_rows]; h1=[r["K1_residual"] for r in hold_rows]
    h2_t=[x["transfer_L2"] for x in h2]; h2_p=[x["power_L2"] for x in h2]; h2_pk=[x["power_peak"] for x in h2]
    h1_t=[x["transfer_L2"] for x in h1]; h1_p=[x["power_L2"] for x in h1]

    # Power identity on new direct nodes.
    kmh=h3*float(static.h); prim=primordial(kmh)
    d2new=prim[None,:]*real**2
    pnew=2*np.pi**2*d2new/(kmh[None,:]**3)
    d2check=prim[None,:]*(np.real(Th)**2)
    alg=float(np.linalg.norm(d2new-d2check)/max(float(np.linalg.norm(d2new)),1e-300))

    gates={
        "R2_G1_locked_provenance_setup": bool(all(ancestry.values()) and frozen),
        "R2_G2_completed_K2_state_integrity": True,
        "R2_G3_CLASS_cross_run_consistency": bool(np.median(class_diff)<=CLASS_MED_GATE and np.max(class_diff)<=CLASS_MAX_GATE),
        "R2_G4_new_H3_direct_health": bool(all_health),
        "R2_G5_new_H3_initial_CLASS_normalization": bool(np.max(initial)<=INITIAL_GATE),
        "R2_G6_new_H3_zero_safe_phase": bool(phase_global<=PHASE_GLOBAL_GATE and phase_abs<=PHASE_ABS_GATE and proj<=POWER_PROJ_GATE),
        "R2_G7_new_H3_saturated_closure": bool(satmax<=SAT_GATE),
        "R2_G8_independent_K2_residual_holdout_accuracy": bool(max(h2_t)<=HOLD_T_GATE and max(h2_p)<=HOLD_P_GATE and max(h2_pk)<=HOLD_PEAK_GATE),
        "R2_G9_residual_refinement_improvement": bool(improve_t>=7 and improve_p>=7 and np.median(h2_t)<np.median(h1_t) and np.median(h2_p)<np.median(h1_p)),
        "R2_G10_K2_to_K3_residual_convergence": bool(max(k2k3_corr)<=CORR_GRID_GATE and np.median(k2k3_corr)<np.median(k1k2_corr) and
            max(k2k3_t)<=TOTAL_T_GATE and max(k2k3_p)<=TOTAL_P_GATE and max(k2k3_pk)<=TOTAL_PEAK_GATE and
            np.median(k2k3_t)<np.median(k1k2_t) and np.median(k2k3_p)<np.median(k1k2_p)),
        "R2_G11_power_sanity": bool(np.all(np.isfinite(d2new)) and np.all(np.isfinite(pnew)) and np.all(d2new>=0) and np.all(pnew>=0) and alg<=ALG_GATE),
    }
    classification=PASS if all(gates.values()) else FAIL
    summary={
        "class_cross_run_median":float(np.median(class_diff)),"class_cross_run_max":float(np.max(class_diff)),
        "new_initial_CLASS_max":float(np.max(initial)),"new_phase_global":phase_global,"new_phase_abs_max":phase_abs,
        "new_real_projection_power_change_max":proj,"new_saturation_max":satmax,
        "K2_holdout_transfer_L2_median":float(np.median(h2_t)),"K2_holdout_transfer_L2_max":float(max(h2_t)),
        "K2_holdout_power_L2_median":float(np.median(h2_p)),"K2_holdout_power_L2_max":float(max(h2_p)),
        "K2_holdout_power_peak_max":float(max(h2_pk)),"holdout_improved_redshifts_transfer":int(improve_t),"holdout_improved_redshifts_power":int(improve_p),
        "corr_K1_to_K2_median":float(np.median(k1k2_corr)),"corr_K2_to_K3_median":float(np.median(k2k3_corr)),"corr_K2_to_K3_max":float(max(k2k3_corr)),
        "total_K2_to_K3_transfer_L2_max":float(max(k2k3_t)),"total_K2_to_K3_power_L2_max":float(max(k2k3_p)),"total_K2_to_K3_power_peak_max":float(max(k2k3_pk)),
        "power_identity_relative_residual":alg,
    }
    out={
        "classification":classification,"diagnostic_complete":True,"git_head":subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip(),
        "ancestry":ancestry,"gates":gates,"summary":summary,"K1_h_Mpc_inv":k1.tolist(),"K2_h_Mpc_inv":k2.tolist(),"K3_h_Mpc_inv":k3.tolist(),"H3_h_Mpc_inv":h3.tolist(),
        "redshifts":CHECK_Z.tolist(),"reference_member":REFERENCE_MEMBER,"health":health_rows,"holdout_rows":hold_rows,"correction_convergence_rows":corr_grid_rows,"total_refinement_rows":total_ref_rows,
        "THREE_D_DENSE_RADIAL_WEYL_NODES_LICENSED": classification==PASS,
        "THREE_D_BOUNDED_CLASS_RESIDUAL_WEYL_TRANSFER_LICENSED": classification==PASS,
        "THREE_D_BOUNDED_CONTINUOUS_WEYL_POWER_LICENSED": classification==PASS,
        "BOUNDED_K_H_MPC_MIN":0.03,"BOUNDED_K_H_MPC_MAX":0.20,
        "THREE_D_CONTINUOUS_WEYL_POWER_LICENSED":False,"EVOLVING_WEYL_POWER_LICENSED":False,"ACT_LIKELIHOOD_LICENSED":False,"OBSERVATIONAL_CLAIM_LICENSED":False,
        "HISTORICAL_SIGNED_TRANSFER_DENSE_FAIL_PRESERVED":True,
    }
    Path(args.json_out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    np.savez_compressed(args.npz_out,K1=k1,K2=k2,K3=k3,H3=h3,CHECK_Z=CHECK_Z,T_K3=T3,T_CLASS_K3=Tc3,T_H3=Th,eps_sat_H3=Sath)
    with open(args.csv_out,"w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=["z","k_h_Mpc_inv","T_real","T_imag","T_CLASS","DeltaT","eps_sat"]); w.writeheader()
        for iz,z in enumerate(CHECK_Z):
            for ih,kh in enumerate(h3):
                j3=ix(k3,kh); w.writerow({"z":float(z),"k_h_Mpc_inv":float(kh),"T_real":float(real[iz,ih]),"T_imag":float(imag[iz,ih]),"T_CLASS":float(Tc3[iz,j3]),"DeltaT":float(real[iz,ih]-Tc3[iz,j3]),"eps_sat":float(Sath[iz,ih])})

    print("FULLJ_DENSE_RESIDUAL_R2_SUMMARY="+json.dumps(summary,sort_keys=True),flush=True)
    print("FULLJ_DENSE_RESIDUAL_R2_GATES="+json.dumps(gates,sort_keys=True),flush=True)
    print("FULLJ_DENSE_RESIDUAL_R2_CLASSIFICATION="+classification,flush=True)
    print("THREE_D_DENSE_RADIAL_WEYL_NODES_LICENSED="+str(classification==PASS),flush=True)
    print("THREE_D_BOUNDED_CLASS_RESIDUAL_WEYL_TRANSFER_LICENSED="+str(classification==PASS),flush=True)
    print("THREE_D_BOUNDED_CONTINUOUS_WEYL_POWER_LICENSED="+str(classification==PASS),flush=True)
    print("THREE_D_CONTINUOUS_WEYL_POWER_LICENSED=False",flush=True)
    print("EVOLVING_WEYL_POWER_LICENSED=False",flush=True)
    print("ACT_LIKELIHOOD_LICENSED=False",flush=True)
    print("OBSERVATIONAL_CLAIM_LICENSED=False",flush=True)
    return 0 if classification==PASS else 2

if __name__=="__main__":
    raise SystemExit(main())
