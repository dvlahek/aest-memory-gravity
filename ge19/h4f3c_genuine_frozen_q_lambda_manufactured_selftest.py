#!/usr/bin/env python3
"""H4F3c frozen real GE06+GE07+Lambda mixed-source manufactured runtime.

Do not mistake this source-generator integration test for a physical
H4F3b calculation: the smooth H1/Z11 and background are MANUFACTURED.
All three previously mocked source functions now execute unchanged.
Original frozen generator imports write only into r7's disposable CWD.
No Z21 propagation, complete Ward certificate or old-file edit.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import subprocess
from pathlib import Path

import numpy as np
from ge19 import repair37_cancellation_safe_fd8_h4_z21_reclosure as old

ROOT=Path(__file__).resolve().parents[1]
PINS={
 "ge19/h4f3c_predata_real_generator_manufactured_runtime.json":
    "2fab9aafd16aa6ea6b11fa6dafff3f3394d97061",
 "ge19/repair37_cancellation_safe_fd8_h4_z21_reclosure.py":
    "45d203a092f9ac71cc612b15df5f0c0c630f5898",
 "ge19/repair07_window_retarded_reduced_h3_z20_particular.py":
    "e34d28a2062c748f48bc82fa928844b02631de25",
 "ge19/repair14_self_consistent_reduced_h3_z20_particular.py":
    "06c5ced952c2370cfa4aaadb6ef8f72d2d7221de",
 "ge06/analytic_aest_directional_source_generator.py":
    "a7afe0035054a9dca55d74a6497c081422114b4c",
 "ge07/pressureless_matter_directional_source_generator.py":
    "cde8da77a80799cef00fc7c09c3633310fc9e3d4",
 "ge19/h4f3b_actual_corrected_six_piece_source.py":
    "0423cbc64f6cda3b2a9aeb67c734935ef3ae7f9c",
 "docs/ge19_h4f3b_synthetic_production_wiring_valid_freeze.md":
    "564211a52941976015dfec81e30618d3aacb5d3f",
}

def pinned_blobs():
    out={}
    for p,want in PINS.items():
        got=subprocess.check_output(
            ["git","rev-parse","HEAD:"+p],cwd=ROOT,text=True).strip()
        out[p]={"expected":want,"observed":got,"exact":got==want}
    return out

def rel(a,b):
    x=np.asarray(a)
    y=np.asarray(b)
    return float(np.linalg.norm(x-y)/max(
        np.linalg.norm(x),np.linalg.norm(y),1e-300
    ))

def fixtures(nt):
    # No real H3F/H3G/R32B binary is loaded, and no manufactured
    # state is ever labelled on-shell or used as an observed result.
    x=np.linspace(math.log(.42),math.log(.83),nt)
    a=np.exp(x)
    H=.71+.11*np.exp(-x)
    bg={
       "x":x,"a":a,"H":H,
       "Z_action":old.r7.Z0*(1+.1*np.cos(x)),
       "Q_action":old.r7.Q0*(1+.09*np.sin(x)),
       "rho_lambda_action":np.full(nt,2.4e-9,float),
    }
    tim=np.arange(nt,dtype=float)[None,None,:]
    mode=np.arange(6,dtype=float)[:,None,None]
    fld=np.arange(6,dtype=float)[None,:,None]
    astate=1.2e-5*np.exp(1j*(.07*tim+.13*mode+.19*fld))
    bstate=6.7e-6*np.exp(1j*(-.1*tim+.29*mode-.12*fld))
    astate=np.broadcast_to(astate,(6,6,nt)).copy()
    bstate=np.broadcast_to(bstate,(6,6,nt)).copy()
    Dx=old.fd8_matrix(nt,float(x[0]),float(x[-1]))
    Dt=H[:,None]*Dx
    adot=np.stack([Dt@astate[:,i,:].T for i in (1,2,3,4)],axis=1)
    bdot=np.stack([Dt@bstate[:,i,:].T for i in (1,2,3,4)],axis=1)
    # [6,4,nt] from each field's [nt,6] cosmic-time derivative.
    adot=np.transpose(adot,(2,1,0))
    bdot=np.transpose(bdot,(2,1,0))
    return bg,astate,adot,bstate,bdot

def build_genuine_generators():
    frozen_ge06=old.r7.load_frozen_generator(
        ROOT/"ge06/analytic_aest_directional_source_generator.py",
        "ge19_h4f3c_frozen_ge06"
    )
    stable_ge06=old.r7.build_stable_ge06_generator_v2(frozen_ge06)
    frozen_ge07=old.r7.load_frozen_generator(
        ROOT/"ge07/pressureless_matter_directional_source_generator.py",
        "ge19_h4f3c_frozen_ge07"
    )
    genuine=old.build_direct_bilinear_generators(
        frozen_ge06,stable_ge06,frozen_ge07
    )
    return genuine

def run(nt,qdirect):
    bg,h1,dh1,z11,dz11=fixtures(nt)
    nx=128
    direct=old.q_cross_direct(
        qdirect,bg,"C_star",h1,dh1,z11,dz11,nx
    )
    swapped=old.q_cross_direct(
        qdirect,bg,"C_star",z11,dz11,h1,dh1,nx
    )
    names=("GE06_main","GE06_constraints",
           "GE07_main","GE07_constraints")
    per={}
    for i,name in enumerate(names):
        s=direct[i]
        correct=(6 if i%2==0 else 2,nt,nx)
        per[name]={
            "shape":list(s.shape),
            "expected_shape":list(correct),
            "shape_ok":s.shape==correct,
            "all_finite":bool(np.isfinite(s).all()),
            "swapped_relative_L2":rel(s,swapped[i]),
            "Fourier_0_to_40_shape_ok":
                old.fft_low(s).shape==(correct[0],nt,41)
        }
    lam,con,ex,pol,sy=old.lambda_cross_direct(
        bg,h1,dh1,z11,dz11,nx
    )
    lambda_gates={
        "main_shape":lam.shape==(6,nt,nx),
        "constraint_shape":con.shape==(2,nt,nx),
        "all_finite":bool(np.isfinite(lam).all()
                          and np.isfinite(con).all()),
        "constraint_exactly_zero":bool(np.count_nonzero(con)==0),
        "expanded_exact_relative_L2":float(ex),
        "swapped_relative_L2":float(sy),
        "nonzero_main":bool(np.linalg.norm(lam)>0),
    }
    all_q=bool(all(x["shape_ok"] and x["all_finite"]
                      and x["Fourier_0_to_40_shape_ok"]
                      and x["swapped_relative_L2"]<=1e-12
                      for x in per.values()))
    all_l=bool(
        all(lambda_gates[k] for k in (
            "main_shape","constraint_shape","all_finite",
            "constraint_exactly_zero","nonzero_main"
        )) and ex<=1e-12 and sy<=1e-12
    )
    return {
        "Nt":nt,"Nx":nx,"source_type":"genuine frozen GE06/GE07/Lambda",
        "GE06_GE07":per,
        "Lambda":{
            **lambda_gates,
            "subtractive_polarization_relative_L2_report_only":float(pol),
        },
        "GE06_main_nonzero":bool(np.linalg.norm(direct[0])>0),
        "GE07_main_nonzero":bool(np.linalg.norm(direct[2])>0),
        "all_frozen_generator_gates_pass":bool(
           all_q and all_l
           and np.linalg.norm(direct[0])>0
           and np.linalg.norm(direct[2])>0
        ),
    }

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--json-out",type=Path,required=True)
    args=parser.parse_args()
    locks=pinned_blobs()
    qdirect=build_genuine_generators()
    cases=[run(nt,qdirect) for nt in (16,32)]
    symbolic=bool(qdirect["all_symbolic_polarization_identities_exact"]
                  and all(qdirect["GE06_identity_by_partial"].values())
                  and all(qdirect["GE07_identity_by_partial"].values()))
    passed=bool(
        all(c["exact"] for c in locks.values())
        and symbolic and len(cases)==2
        and all(c["all_frozen_generator_gates_pass"] for c in cases)
    )
    report={
        "classification":(
            "GE19_H4F3C_GENUINE_FROZEN_Q_LAMBDA_MANUFACTURED_RUNTIME_PASS"
            if passed else
            "GE19_H4F3C_GENUINE_GENERATOR_MANUFACTURED_RUNTIME_FAIL"
        ),
        "predata_classification":
            "GE19_H4F3C_PREDATA_REAL_FROZEN_Q_LAMBDA_MANUFACTURED_RUNTIME",
        "source_blobs":locks,
        "actual_frozen_symbolic_polarization_pass":symbolic,
        "manufactured_cases":cases,
        "all_gates_pass":passed,
        "genuine_unmocked_evaluators":[
            "GE06 mixed Q","GE07 mixed Q","Lambda mixed Q"
        ],
        "manufactured_background_and_state_only":True,
        "original_certified_Repair32B_Z11_binary_consumed":False,
        "H4F3b_actual_corrected_parent_six_source_run":False,
        "complete_H4_operator_parent_Ward_derived":False,
        "H4_Z21_solved":False,
        "Z21_certified":False,
        "lensing_licensed":False,
        "next_route":(
            "REAL_H4F3B_REQUIRES_EXACT_REPAIR32B_Z11_BINARY"
            if passed else "FREEZE_GENUINE_MIXED_GENERATOR_RUNTIME_FAILURE"
        )
    }
    args.json_out.parent.mkdir(parents=True,exist_ok=True)
    args.json_out.write_text(json.dumps(
        report,indent=2,sort_keys=True,allow_nan=False
    )+"\n")
    print(json.dumps(report,indent=2,sort_keys=True,allow_nan=False))
    if not passed:
        raise SystemExit(3)

if __name__=="__main__":
    main()
