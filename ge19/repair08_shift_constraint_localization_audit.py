#!/usr/bin/env python3
"""GE19 Repair08 shift-constraint localization audit.

Diagnostic only.  Reuses the frozen Repair07 operator and trajectories and
does not construct Z20 or change any equation, sign, threshold, background,
solver, or reduced-matter choice.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

import ge09.repair01_dense_accepted_step_local_jet_bridge as g9
import ge18.repair01_on_shell_matched_dust_first_order_bridge as g18

TINY=1.0e-300
SHIFT_GATE=1.0e-6
FULL_CLASS_GOOD=1.0e-4
SIGN_IMPROVE=100.0
REPAIR07_JSON_SHA="f27d31b637332bd043ebabdcc47a18e1126f05065aea2cca794ac8e0f2b2e894"


def sha256(path:Path)->str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module(path:Path,name:str):
    spec=importlib.util.spec_from_file_location(name,path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def pair_metric(a,b):
    return float(abs(a+b)/max(abs(a),abs(b),TINY))


def pair_metric_sub(a,b):
    return float(abs(a-b)/max(abs(a),abs(b),TINY))


def positive_mode_series(r7,arr,amp,phase):
    arr=np.asarray(arr,float)
    return r7.positive_mode_coeff(arr,np.zeros_like(arr),amp,phase)


def state_w(state,dot,it):
    # Repair07 local canonical order:
    # (N,dr,S,u,phi,T,Sdot,udot,phidot,Tdot)
    return np.asarray([
        state[0,it],state[5,it],
        state[1,it],state[2,it],state[3,it],state[4,it],
        dot[0,it],dot[1,it],dot[2,it],dot[3,it],
    ],complex)


def metric_summary(vals,z):
    vals=np.asarray(vals,float)
    im=int(np.argmax(vals))
    return {
        "initial":float(vals[0]),
        "max":float(vals[im]),
        "max_index":im,
        "max_z":float(z[im]),
        "final":float(vals[-1]),
    }


def first_crossing(vals,z,limit):
    vals=np.asarray(vals,float)
    ii=np.where(vals>limit)[0]
    if ii.size==0:
        return None
    i=int(ii[0])
    return {"index":i,"z":float(z[i]),"value":float(vals[i])}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--results-dir",default=str(ROOT/"results"))
    ap.add_argument("--json-out",required=True)
    args=ap.parse_args()
    rd=Path(args.results_dir)

    required=[
        rd/"ge15_R1_dense_accepted_step_trace.dat",
        rd/"ge15_cancellation_free_s_state_precision_closure.json",
        rd/"ge15_cancellation_free_s_state_precision_closure.npz",
        rd/"ge15_R1_cli_background.dat",
        rd/"ge18_repair01_on_shell_matched_dust_first_order_bridge.json",
        rd/"ge18_repair01_on_shell_matched_dust_first_order_bridge.npz",
        rd/"ge19_repair07_window_retarded_reduced_h3_z20_particular.json",
    ]+[rd/f"ge15_R1_cli_perturbations_k{i}_s.dat" for i in range(6)]
    missing=[str(p) for p in required if not p.exists()]
    if missing:
        raise RuntimeError("missing required frozen local inputs: "+", ".join(missing))

    r7path=ROOT/"ge19"/"repair07_window_retarded_reduced_h3_z20_particular.py"
    r7=load_module(r7path,"ge19_repair07_frozen")

    r7_result_path=rd/"ge19_repair07_window_retarded_reduced_h3_z20_particular.json"
    r7_hash=sha256(r7_result_path)
    if r7_hash!=REPAIR07_JSON_SHA:
        raise RuntimeError(f"Repair07 result hash mismatch: {r7_hash}")

    r7_result=json.loads(r7_result_path.read_text())
    if r7_result.get("classification")!="GE19_REPAIR07_WINDOW_RETARDED_REDUCED_H3_Z20_PARTICULAR_FAIL":
        raise RuntimeError("unexpected Repair07 classification")
    if r7_result.get("failure_stage")!="Stage_A_reduced_H1_reclosure":
        raise RuntimeError("unexpected Repair07 failure stage")

    ge15=json.loads((rd/"ge15_cancellation_free_s_state_precision_closure.json").read_text())
    ge18=json.loads((rd/"ge18_repair01_on_shell_matched_dust_first_order_bridge.json").read_text())
    dense=rd/"ge15_R1_dense_accepted_step_trace.dat"
    if sha256(dense)!=ge15["precision_binding"]["dense_trace_sha256"]["R1"]:
        raise RuntimeError("GE15 dense hash mismatch")
    ge18_npz_path=rd/"ge18_repair01_on_shell_matched_dust_first_order_bridge.npz"
    if sha256(ge18_npz_path)!=r7.GE18_NPZ_SHA:
        raise RuntimeError("GE18 NPZ hash mismatch")
    npz=np.load(ge18_npz_path)

    mod6_frozen=r7.load_frozen_generator(
        ROOT/"ge06"/"analytic_aest_directional_source_generator.py",
        "ge19r8_ge06",
    )
    mod6=r7.build_stable_ge06_generator_v2(mod6_frozen)
    mod7=r7.load_frozen_generator(
        ROOT/"ge07"/"pressureless_matter_directional_source_generator.py",
        "ge19r8_ge07",
    )

    bg,jstate,jets=r7.build_ge15_reference(dense,r7.NT_PRIMARY)
    x=np.asarray(bg["x"],float)
    a=np.asarray(bg["a"],float)
    z=1.0/a-1.0
    amps,_,_=r7.amplitudes()

    # Exact full-standard CLASS density/momentum arrays on the same 64 nodes,
    # using the same frozen GE18 parser/interpolation convention.
    raw_bg=g18.parse_background(rd/"ge15_R1_cli_background.dat")
    bgi=g18.interp_bg(raw_bg)
    raw_modes=[g18.parse_raw_mode(rd/f"ge15_R1_cli_perturbations_k{i}_s.dat") for i in range(6)]
    full_std=[
        g18.mode_standard_state(raw_modes[i],bgi,x)
        for i in range(6)
    ]

    rows=[]
    global_initial=0.0
    global_canonical=0.0
    global_reference=0.0
    global_full_class=0.0
    global_full_class_wrong_sign=0.0
    global_tflip_initial=0.0
    global_phiflip_initial=0.0
    worst_initial_improve_T=0.0
    worst_initial_improve_phi=0.0

    for tag in r7.C_TAGS:
        ref,refdot=r7.reference_reduced_mode_state(bg,jets,npz,tag)

        for ik,m in enumerate(r7.FOURIER_N):
            k=float(g9.K_REQ[ik])
            amp=float(amps[ik])
            phase=float(r7.PHASES[ik])

            # Frozen mixed GE15+GE18 reference shift over the whole window.
            ref_metric=[]
            full_metric=[]
            full_wrong_sign=[]
            dust_piece_metric=[]
            tflip_metric=[]
            phiflip_metric=[]
            ga_abs=[]
            dust_abs=[]
            full_abs=[]

            mom_pos=positive_mode_series(r7,full_std[ik]["momentum_std"],amp,phase)

            for it,xq in enumerate(x):
                w=state_w(ref[ik],refdot[ik],it)
                Cmat,bp,_=r7._local_linear_matrix(mod6,mod7,bg,tag,k,float(xq))
                sga=Cmat[10]@w
                sm=Cmat[11]@w
                met=r7._constraint_backward_error(Cmat[10]+Cmat[11],w,0.0,sga,sm)
                ref_metric.append(met["metric"])
                dust_piece_metric.append(pair_metric(sga,sm))

                # Full-standard CLASS momentum contribution in the same action
                # normalization.  GE07 gives E_b,m=-6 i a^4 [(rho+p)theta]/k.
                sm_full=-6j*(a[it]**4)*mom_pos[it]/k
                full_metric.append(pair_metric(sga,sm_full))
                full_wrong_sign.append(pair_metric_sub(sga,sm_full))

                wt=w.copy(); wt[5]*=-1.0
                tflip_metric.append(pair_metric(Cmat[10]@wt,Cmat[11]@wt))
                wp=w.copy(); wp[4]*=-1.0
                phiflip_metric.append(pair_metric(Cmat[10]@wp,Cmat[11]@wp))

                ga_abs.append(float(abs(sga)))
                dust_abs.append(float(abs(sm)))
                full_abs.append(float(abs(sm_full)))

            # Repair07 canonical trajectory from the same frozen initial data.
            q0=np.asarray(ref[ik,[1,2,3,4],0],complex)
            v0=np.asarray(refdot[ik,:,0],complex)
            y0,w0,idiag=r7._initial_canonical_state(
                mod6,mod7,bg,tag,k,float(x[0]),q0,v0,np.zeros(6,complex)
            )
            rhsfun,confun=r7._zero_source_interp(1)
            Y,rdiag=r7._radau2_integrate_canonical(
                mod6,mod7,bg,tag,k,y0[:,None],rhsfun,confun
            )

            canonical_metric=[]
            canonical_abs=[]
            for it,xq in enumerate(x):
                M,F,ZY,ZR,WY,WR,Cmat,bp,opdiag=r7._canonical_operator_matrices(
                    mod6,mod7,bg,tag,k,float(xq)
                )
                w=WY@Y[0,:,it]
                sga=Cmat[10]@w
                sm=Cmat[11]@w
                met=r7._constraint_backward_error(Cmat[10]+Cmat[11],w,0.0,sga,sm)
                canonical_metric.append(met["metric"])
                canonical_abs.append(met["absolute_residual"])

            # Initial prescribed w0, before any propagation.
            C0,bp0,_=r7._local_linear_matrix(mod6,mod7,bg,tag,k,float(x[0]))
            sga0=C0[10]@w0
            sm0=C0[11]@w0
            initial_current=r7._constraint_backward_error(
                C0[10]+C0[11],w0,0.0,sga0,sm0
            )
            initial_piece=pair_metric(sga0,sm0)

            wT=w0.copy(); wT[5]*=-1.0
            initial_Tflip=pair_metric(C0[10]@wT,C0[11]@wT)
            wP=w0.copy(); wP[4]*=-1.0
            initial_phiflip=pair_metric(C0[10]@wP,C0[11]@wP)

            initial_improve_T=initial_piece/max(initial_Tflip,TINY)
            initial_improve_phi=initial_piece/max(initial_phiflip,TINY)

            rs={
                "C":tag,
                "m":int(m),
                "k_Mpc":k,
                "initial_prescribed": {
                    "shift_backward_error":initial_current["metric"],
                    "shift_pair_metric":initial_piece,
                    "shift_absolute_residual":initial_current["absolute_residual"],
                    "matter_sign_flip_pair_metric":initial_Tflip,
                    "aest_scalar_phi_sign_flip_pair_metric":initial_phiflip,
                    "matter_sign_flip_improvement_factor":float(initial_improve_T),
                    "aest_scalar_phi_sign_flip_improvement_factor":float(initial_improve_phi),
                },
                "mixed_reference_reduced_dust":metric_summary(ref_metric,z),
                "mixed_reference_piece_metric":metric_summary(dust_piece_metric,z),
                "full_standard_CLASS_pair_metric":metric_summary(full_metric,z),
                "full_standard_CLASS_wrong_sign_pair_metric":metric_summary(full_wrong_sign,z),
                "canonical_repair07":metric_summary(canonical_metric,z),
                "canonical_first_crossing_1e6":first_crossing(canonical_metric,z,SHIFT_GATE),
                "canonical_absolute_residual_max":float(np.max(canonical_abs)),
                "reference_T_sign_flip_pair_metric":metric_summary(tflip_metric,z),
                "reference_phi_sign_flip_pair_metric":metric_summary(phiflip_metric,z),
                "piece_abs_max": {
                    "GE06_gravity_AeST":float(np.max(ga_abs)),
                    "GE07_reduced_dust":float(np.max(dust_abs)),
                    "full_standard_CLASS_equivalent":float(np.max(full_abs)),
                },
                "radau_scaled_residual_max":rdiag["radau_block_scaled_relative_L2_residual_max"],
            }
            rows.append(rs)

            global_initial=max(global_initial,float(initial_current["metric"]))
            global_canonical=max(global_canonical,float(np.max(canonical_metric)))
            global_reference=max(global_reference,float(np.max(ref_metric)))
            global_full_class=max(global_full_class,float(np.max(full_metric)))
            global_full_class_wrong_sign=max(global_full_class_wrong_sign,float(np.max(full_wrong_sign)))
            global_tflip_initial=max(global_tflip_initial,float(initial_Tflip))
            global_phiflip_initial=max(global_phiflip_initial,float(initial_phiflip))
            worst_initial_improve_T=max(worst_initial_improve_T,float(initial_improve_T))
            worst_initial_improve_phi=max(worst_initial_improve_phi,float(initial_improve_phi))

    initial_bad=bool(global_initial>SHIFT_GATE)
    propagation_bad=bool((not initial_bad) and global_canonical>SHIFT_GATE)
    full_class_good=bool(global_full_class<=FULL_CLASS_GOOD)
    matter_sign_suspect=bool(initial_bad and worst_initial_improve_T>=SIGN_IMPROVE)
    phi_sign_suspect=bool(initial_bad and worst_initial_improve_phi>=SIGN_IMPROVE)
    reduced_reference_bad=bool(global_reference>SHIFT_GATE)

    if matter_sign_suspect:
        route="INITIAL_MATTER_TX_SIGN_CONVENTION_SUSPECT"
    elif phi_sign_suspect:
        route="INITIAL_AEST_SCALAR_SIGN_CONVENTION_SUSPECT"
    elif initial_bad:
        route="INITIAL_SURFACE_MAPPING_OR_CONSTRAINT_INCOMPATIBILITY"
    elif full_class_good and reduced_reference_bad:
        route="REDUCED_DUST_BRIDGE_OR_BACKGROUND_OFFSHELL_SUSPECT"
    elif full_class_good and propagation_bad:
        route="CANONICAL_CONSTRAINT_PROPAGATION_SUSPECT"
    elif not full_class_good:
        route="GE15_GE06_FULL_CLASS_SHIFT_CONVENTION_MISMATCH_SUSPECT"
    else:
        route="SHIFT_DEFECT_NOT_LOCALIZED"

    report={
        "classification":"GE19_REPAIR08_SHIFT_CONSTRAINT_LOCALIZATION_AUDIT_COMPLETE",
        "predata_classification":"GE19_REPAIR08_PREDATA_SHIFT_CONSTRAINT_LOCALIZATION_AUDIT",
        "diagnostic_only":True,
        "repair07_result_sha256":r7_hash,
        "repair07_historical_classification":r7_result["classification"],
        "thresholds":{
            "science_shift_gate_reference":SHIFT_GATE,
            "full_CLASS_pair_cancellation_good":FULL_CLASS_GOOD,
            "sign_flip_strong_improvement_factor":SIGN_IMPROVE,
        },
        "global":{
            "initial_prescribed_shift_backward_error_max":global_initial,
            "mixed_reference_reduced_dust_shift_backward_error_max":global_reference,
            "canonical_repair07_shift_backward_error_max":global_canonical,
            "full_standard_CLASS_pair_metric_max":global_full_class,
            "full_standard_CLASS_wrong_sign_pair_metric_max":global_full_class_wrong_sign,
            "initial_matter_sign_flip_pair_metric_max":global_tflip_initial,
            "initial_aest_scalar_phi_sign_flip_pair_metric_max":global_phiflip_initial,
            "max_initial_matter_sign_flip_improvement_factor":worst_initial_improve_T,
            "max_initial_phi_sign_flip_improvement_factor":worst_initial_improve_phi,
        },
        "routing":{
            "initial_surface_defect":initial_bad,
            "propagation_defect":propagation_bad,
            "full_standard_CLASS_shift_convention_closes":full_class_good,
            "reduced_reference_exceeds_shift_gate":reduced_reference_bad,
            "matter_sign_suspect":matter_sign_suspect,
            "aest_scalar_sign_suspect":phi_sign_suspect,
            "next_route":route,
        },
        "per_case":rows,
        "claim_boundary":"Diagnostic localization only. No equation, sign, threshold, solver, background, reduced-matter choice or H3/Z20 result is changed or licensed."
    }

    out=Path(args.json_out)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2,allow_nan=False)+"\n")
    print(json.dumps(report,indent=2,allow_nan=False))


if __name__=="__main__":
    main()
