#!/usr/bin/env python3
"""GE19 Stage E preregistered deterministic audit of standalone Y-only rows.

No parent states, frozen historical sources or H4 solver are modified.
Original Repair07/Repair37 Y scalar expressions are comparators ONLY;
the Repair37 reduced-state adapter is restored after its local test.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import numpy as np

import ge19.h4_stagee_versioned_y_source_rows as ys
import ge19.repair07_window_retarded_reduced_h3_z20_particular as r7
import ge19.repair37_cancellation_safe_fd8_h4_z21_reclosure as r37

ROOT=Path(__file__).resolve().parents[1]
BLOBS={
    "ge19/h4_stagee_predata_versioned_y_source_rows.json":
        "e5ff7d12e963fa7487a1dff42ce06053f4b8d82e",
    "docs/ge19_h4_staged_local_analytic_reproduction_freeze.md":
        "cb41f5633caaebf87924f464d509747ca7a7c4dc",
    "docs/ge19_h4_staged_common_y_action_rows_valid_freeze.md":
        "7d140a608d91a39106c34565cd50e4aa729ec30b",
    "ge19/h4_structural_stage_d_common_action_y_rows.py":
        "162357ce845a93982b46aef7d839a7171964b47e",
    "ge19/repair07_window_retarded_reduced_h3_z20_particular.py":
        "e34d28a2062c748f48bc82fa928844b02631de25",
    "ge19/repair37_cancellation_safe_fd8_h4_z21_reclosure.py":
        "45d203a092f9ac71cc612b15df5f0c0c630f5898",
}


def rel_l2(a,b):
    x=np.asarray(a)
    y=np.asarray(b)
    return float(np.linalg.norm(x-y)/max(np.linalg.norm(x),np.linalg.norm(y),1e-300))


def old_dy_with_test_adapter(bg,u0,px0,u1,px1,beta,nx):
    original=r37.r7.reduced_state_real
    def adapter(bg,state,nx,dot):
        u,px=state
        return {"u20":u},None,{"phi20":px}
    try:
        r37.r7.reduced_state_real=adapter
        return r37.dy2_real(bg,(u0,px0),None,(u1,px1),None,beta,nx)
    finally:
        r37.r7.reduced_state_real=original


def compare_frozen_blobs():
    d={}
    for path,expected in BLOBS.items():
        got=subprocess.check_output(
            ["git","rev-parse","HEAD:"+path],cwd=ROOT,text=True
        ).strip()
        d[path]={"expected":expected,"observed":got,"exact":bool(got==expected)}
    return d


def deterministic_test(beta):
    nt,nx=6,256
    tt=np.arange(nt,dtype=float)[:,None]
    xx=(2.0*np.pi*np.arange(nx,dtype=float)/nx)[None,:]
    a=0.55+0.035*np.arange(nt,dtype=float)
    Q=1.0e-4+8.0e-6*np.cos(np.arange(nt,dtype=float))
    # Small-gradient test directions; both are periodic derivatives.
    u0=2.0e-4*np.cos(xx+0.1*tt)+0.6e-4*np.sin(3.0*xx-0.2*tt)
    u1=0.8e-4*np.sin(2.0*xx+0.3*tt)-0.3e-4*np.cos(4.0*xx)
    g0=1.0e-7*np.sin(xx+0.11*tt)+0.35e-7*np.sin(5*xx-0.17*tt)
    g1=4.5e-8*np.cos(2*xx+0.17*tt)+2.0e-8*np.sin(4*xx-0.21*tt)
    # phi_x cancels the Q u term and leaves the fixed g direction.
    p0=a[:,None]*(g0-Q[:,None]*u0)
    p1=a[:,None]*(g1-Q[:,None]*u1)
    kfund=float(r7.g9.K_REQ[0]/r7.FOURIER_N[0])
    kwargs=dict(KB=r7.KB,a0=r7.A0_MPC_INV,beta=beta,kfund=kfund)
    h3=ys.source_h3(a,Q,u0,p0,**kwargs)
    h4=ys.source_h4(a,Q,u0,p0,u1,p1,**kwargs)
    delta=1.0e-5
    hp=ys.source_h3(a,Q,u0+delta*u1,p0+delta*p1,**kwargs)
    hm=ys.source_h3(a,Q,u0-delta*u1,p0-delta*p1,**kwargs)
    tangent=(hp["main"]-hm["main"])/(2*delta)
    tangent_rel=rel_l2(tangent,h4["main"])

    frozen_bg={"a":a,"Q_action":Q}
    old_h3=r7.y2_source_from_reduced(
        frozen_bg,{"u20":u0},{"phi20":p0},beta
    )
    old_dy=old_dy_with_test_adapter(
        frozen_bg,u0,p0,u1,p1,beta,nx
    )
    # Frozen H3 legacy reduced Y2 has no flux mask. Only the
    # original low m<=40 projected modes are compared. Frozen
    # H4 has the same 2/3 flux projection as the new source.
    legacy_h3_modes=np.fft.fft(-2*a[:,None]**3*old_h3,axis=1)[:,:41]
    new_h3_modes=np.fft.fft(h3["main"][3],axis=1)[:,:41]
    h3_rel=rel_l2(legacy_h3_modes,new_h3_modes)
    h4_rel=rel_l2(
        h4["main"][3],
        -2*a[:,None]**3*old_dy
    )
    zero3=ys.source_h3(
        a,Q,np.zeros_like(u0),np.zeros_like(p0),**kwargs
    )
    zero4=ys.source_h4(
        a,Q,np.zeros_like(u0),np.zeros_like(p0),u1,p1,**kwargs
    )
    modes=np.fft.fftfreq(nx)*nx
    hi=np.abs(modes)>nx/3+1e-12
    high_modes=np.fft.fft(h3["projected_flux"],axis=-1)[:,hi]
    high_norm=float(np.linalg.norm(high_modes)/max(
        np.linalg.norm(np.fft.fft(h3["projected_flux"],axis=-1)),
        1e-300
    ))
    aa=a[:,None]
    direct_u=2*aa**3*Q[:,None]*h3["kappa"]*h3["projected_flux"]
    direct_phi=-2*aa**2*h3["kappa"]*h3["spatial_flux_derivative"]
    rowgate=bool(
        h3["main"].shape==(6,nt,nx)
        and h3["constraint"].shape==(2,nt,nx)
        and h4["main"].shape==(6,nt,nx)
        and h4["constraint"].shape==(2,nt,nx)
        and np.array_equal(h3["main"][2],direct_u)
        and np.array_equal(h3["main"][3],direct_phi)
        and np.array_equal(h3["main"][[0,1,4,5]],np.zeros((4,nt,nx)))
        and np.array_equal(h4["main"][[0,1,4,5]],np.zeros((4,nt,nx)))
        and np.array_equal(h3["constraint"],np.zeros((2,nt,nx)))
        and np.array_equal(h4["constraint"],np.zeros((2,nt,nx)))
        and np.array_equal(zero3["main"],np.zeros((6,nt,nx)))
        and np.array_equal(zero4["main"],np.zeros((6,nt,nx)))
    )
    return {
        "beta":beta,
        "row_and_zero_set_exact":rowgate,
        "kappa":h3["kappa"],
        "eta_tangent_relative_L2":tangent_rel,
        "H3_vs_frozen_reduced_Y_scalar_low_modes_relative_L2":h3_rel,
        "H4_vs_frozen_DY_scalar_relative_L2":h4_rel,
        "projected_flux_high_modes_relative_L2":high_norm,
        "all_outputs_finite":bool(
            np.isfinite(h3["main"]).all()
            and np.isfinite(h4["main"]).all()
        ),
        "pass":bool(
            rowgate and tangent_rel<=1.0e-4
            and h3_rel<=1.0e-12 and h4_rel<=1.0e-12
            and high_norm<=1.0e-11
        ),
    }


def test_invalid_inputs():
    a=np.asarray([0.8,0.9])
    Q=np.asarray([0.0001,0.0001])
    f=np.zeros((2,16))
    kwargs=dict(KB=r7.KB,a0=r7.A0_MPC_INV,beta=1.0,kfund=0.5)
    variants=[
        (a, Q[:1],f,f,kwargs),
        (a, Q,f,f[:1],kwargs),
        (np.asarray([0.0,0.9]),Q,f,f,kwargs),
        (a,Q,np.full_like(f,np.nan),f,kwargs),
        (a,Q,f,f,dict(kwargs,a0=0.0)),
        (a,Q,f,f,dict(kwargs,kfund=0.0)),
        (a,Q,f,f,dict(kwargs,beta=0.2)),
        (a,Q,f,f,dict(kwargs,KB=2.0)),
    ]
    return all(_raises_value(*data) for data in variants)


def _raises_value(a,Q,u,p,kwargs):
    try:
        ys.source_h3(a,Q,u,p,**kwargs)
    except ValueError:
        return True
    return False


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--json-out",required=True)
    args=ap.parse_args()
    blobs=compare_frozen_blobs()
    tests=[deterministic_test(beta) for beta in ys.FROZEN_BETAS]
    invalid=test_invalid_inputs()
    allpass=bool(
        all(v["exact"] for v in blobs.values())
        and all(t["pass"] and t["all_outputs_finite"] for t in tests)
        and invalid
    )
    report={
        "classification":(
            "GE19_H4_STAGEE_Y_SOURCE_ROW_DICTIONARY_IMPLEMENTATION_PASS"
            if allpass else
            "GE19_H4_STAGEE_Y_SOURCE_ROW_IMPLEMENTATION_FAIL"
        ),
        "predata_classification":
            "GE19_H4_STAGEE_PREDATA_VERSIONED_COMPLETE_Y_SOURCE_ROWS",
        "source_contract":"Y-only action-derived GE19 raw RHS, full 6+2 rows with 2/3-projected common real-space flux.",
        "frozen_blobs":blobs,
        "beta_cases":tests,
        "invalid_inputs_rejected":invalid,
        "all_implementation_gates_pass":allpass,
        "historical_H3_H4_sources_modified":False,
        "H3_Z20_reclosure_performed":False,
        "q20_reclosure_performed":False,
        "full_H4_Noether_derived":False,
        "H4_Z21_solve_performed":False,
        "Z21_window_local_particular_certified":False,
        "lensing_licensed":False,
        "next_route":(
            "FREEZE_VERSIONED_Y_ROWS_AND_PREREGISTER_NEW_H3_PARENT_RECLOSURE"
            if allpass else
            "FREEZE_STAGEE_IMPLEMENTATION_FAIL"
        ),
    }
    p=Path(args.json_out)
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print(json.dumps(report,indent=2,sort_keys=True,allow_nan=False))
    if not allpass:
        raise SystemExit(3)


if __name__=="__main__":
    main()
