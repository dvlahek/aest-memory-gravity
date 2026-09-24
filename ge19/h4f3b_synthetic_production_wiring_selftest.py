#!/usr/bin/env python3
"""H4F3b exact production-path wiring selftest with manufactured externals.

Use the unchanged *actual* H4F3b actual_case_source, frozen r7 reduced
Fourier reconstruction, M1(B20), Stage E complete Y u+phi, six-piece
H4F2g assembly and H*FD8/H*FD4 H4F2h physical Ward. Stub only
externally expensive Q_GE06/GE07, Q_Lambda and Repair26-R1 M2 numerics.

No synthetic Z11 is ever presented as the missing certified Repair32B
NPZ. This cannot license an actual H4F3b source result or a Z21 solve.
"""
from __future__ import annotations
import argparse
import json
import subprocess
from pathlib import Path
from unittest.mock import patch
import numpy as np
from ge19 import h4f3b_actual_corrected_six_piece_source as actual
from ge19 import h4f2g_action_completed_six_piece_source_ledger as ledger
from ge19 import h4f2h_physical_time_source_ward_bridge as clock
from ge19 import h4_stagee_versioned_y_source_rows as y

ROOT=Path(__file__).resolve().parents[1]
PINNED={
    "ge19/h4f3b_predata_synthetic_production_wiring.json":
        "7121c2fa7ca2502dbf66923a2522fb2340003ee3",
    **actual.PINNED,
    "ge19/h4f3b_actual_corrected_six_piece_source.py":
        "0423cbc64f6cda3b2a9aeb67c734935ef3ae7f9c",
    "ge19/repair07_window_retarded_reduced_h3_z20_particular.py":
        "e34d28a2062c748f48bc82fa928844b02631de25",
}


def exact_blobs():
    return {
        p:{"expected":want,
           "observed":(got:=subprocess.check_output(
               ["git","rev-parse","HEAD:"+p],cwd=ROOT,text=True
           ).strip()),
           "exact":got==want}
        for p,want in PINNED.items()
    }


def rel(a,b):
    u=np.asarray(a)
    v=np.asarray(b)
    return float(np.linalg.norm(u-v)/max(
        np.linalg.norm(u),np.linalg.norm(v),1e-300
    ))


def run_fixture():
    old=actual.old
    nt,nx=16,128
    x=np.linspace(np.log(0.42),np.log(0.83),nt)
    a=np.exp(x)
    H=0.71+0.11*np.exp(-x)
    Q=1.1e-4+1.8e-5*np.sin(np.arange(nt)*0.21)
    bg={"x":x,"a":a,"H":H,"Q_action":Q}
    t=np.arange(nt)[None,None,:]
    fm=np.arange(6)[:,None,None]
    # state: six positive Fourier modes x six GE19 fields x Nt
    field=np.arange(6)[None,:,None]
    h1=1.6e-4*np.exp(1j*(0.13*t+fm*0.17+field*0.23))
    h1=h1*np.ones((6,6,nt),complex)
    hdot=8e-5*np.exp(1j*(0.19*t+fm*0.31+
                              np.arange(4)[None,:,None]*0.16))
    hdot=hdot*np.ones((6,4,nt),complex)
    z11=0.55*h1*np.exp(1j*0.09)
    zdot=0.55*hdot*np.exp(-1j*0.05)
    B20=np.zeros((3,40,nt),complex)
    mm=np.arange(1,41,dtype=float)[None,:,None]
    B20[:]=2e-6/(1+mm)*np.exp(1j*(0.11*t+0.07*mm))
    weights=np.array([0.4,0.6])
    z10=np.zeros((2,6,nt),complex)
    for i in range(2):
        z10[i]=1e-5*(i+1)*np.exp(
            1j*(0.13*t[0,0,:][None,:]+0.07*fm[:,0,0][:,None])
        )
    v10=0.1*z10
    weighted=np.einsum("b,bmt->mt",weights,z10,optimize=True)
    boundary={"w":weights}

    xx=2*np.pi*np.arange(nx)/nx
    timephase=np.arange(nt)[:,None]*0.073
    cos=np.cos(xx[None,:]+timephase)
    sin=np.sin(2*xx[None,:]-timephase)
    def real_rows(nrows,used,scale):
        out=np.zeros((nrows,nt,nx),float)
        for j in used:
            out[j]=scale*(j+1)*(cos+0.24*sin)
        return out

    gm=real_rows(6,(0,1,2,3),1e-7)
    gc=real_rows(2,(0,1),2e-7)
    dm=real_rows(6,(0,1,4,5),3e-7)
    dc=real_rows(2,(0,1),1e-7)
    lm=real_rows(6,(0,1),2e-8)
    lc=real_rows(2,(),0)
    m2m=np.fft.fft(
        real_rows(6,(0,1,2,3),1e-8),axis=-1
    )[:,:,:41]/nx
    m2c=np.fft.fft(
        real_rows(2,(0,1),1e-8),axis=-1
    )[:,:,:41]/nx
    invokes={"cross":0,"lambda":0,"M2":0}
    def mock_cross(*args,**kw):
        invokes["cross"]+=1
        return gm,gc,dm,dc
    def mock_lambda(*args,**kw):
        invokes["lambda"]+=1
        return lm,lc,0.0,0.0,0.0
    def mock_m2(*args,**kw):
        invokes["M2"]+=1
        return m2m,m2c,z10,v10

    # Only externally expensive physical evaluators are replaced. The
    # r7 Fourier spatial reconstructor, M1, Stage E, ledger and physical
    # clock are executed unchanged in actual_case_source().
    with patch.object(old,"q_cross_direct",mock_cross),\
         patch.object(old,"lambda_cross_direct",mock_lambda),\
         patch.object(old,"reconstruct_m2_source",mock_m2):
        outputs,diagnostics=actual.actual_case_source(
            bg,"C_star",h1,hdot,z11,zdot,B20,weighted,
            None,None,None,None,boundary
        )
        wrong=weighted+1e-3
        _,negative=actual.actual_case_source(
            bg,"C_star",h1,hdot,z11,zdot,B20,wrong,
            None,None,None,None,boundary
        )

    real0,_,spatial0=old.r7.reduced_state_real(
        bg,h1,actual.SOURCE_NX_Y,hdot
    )
    real1,_,spatial1=old.r7.reduced_state_real(
        bg,z11,actual.SOURCE_NX_Y,zdot
    )
    kfund=float(old.r7.g9.K_REQ[0]/old.r7.FOURIER_N[0])
    all_beta=[]
    for ib,beta in enumerate(old.r7.BETAS):
        data=outputs[ib]
        pieces=data["assembled"]["piece_rows"]
        total=data["assembled"]["total_rows"]
        out=data["physical"]
        computed_y=y.source_h4(
            a,Q,real0["u20"],spatial0["phi20"],
            real1["u20"],spatial1["phi20"],
            old.r7.KB,old.r7.A0_MPC_INV,float(beta),kfund
        )
        fy=np.fft.fft(computed_y["main"],axis=-1)[:,:,:41]/actual.SOURCE_NX_Y
        cy=np.fft.fft(computed_y["constraint"],axis=-1)[:,:,:41]/actual.SOURCE_NX_Y
        y_expected=np.concatenate((fy,cy),axis=0)
        same=np.array_equal(pieces[ledger.Y_PIECE],y_expected)
        direct_m1,con_m1=old.m1_mapped_fourier(bg,B20)
        m1=np.concatenate((direct_m1[ib],con_m1[ib]),axis=0)
        exact_m1=np.array_equal(pieces[ledger.PIECES[4]],m1)
        source_error=float(np.max(np.abs(
            sum((pieces[n] for n in ledger.PIECES),
                np.zeros_like(total))-total
        )))
        ward_error=float(np.max(np.abs(
            sum((out["per_piece"][n] for n in ledger.PIECES),
                np.zeros_like(out["total_source_ward"]))-
            out["total_source_ward"]
        )))
        checks={
          "six_real_assembly_families_present":set(pieces)==set(ledger.PIECES),
          "GE19_eight_rows_41_modes":total.shape==(8,nt,41),
          "complete_StageE_Y_actual_both_rows":
              bool(same and np.linalg.norm(y_expected[2])>0
                   and np.linalg.norm(y_expected[3])>0),
          "Y_metric_constraint_rows_exactly_zero":
              bool(np.array_equal(y_expected[[0,1,4,5,6,7]],
                                  np.zeros((6,nt,41),complex))),
          "frozen_real_M1_from_B20_exact":bool(exact_m1),
          "actual_physical_FD8_FD4_scheme":
              bool(out["schemes"]==clock.SCHEMES),
          "source_total_linear_max_abs":source_error,
          "physical_Ward_total_linear_max_abs":ward_error,
          "all_results_finite":bool(
              np.isfinite(total).all()
              and np.isfinite(out["total_source_ward"]).all()
          ),
          "nonzero_source_Ward_not_mistaken_as_fail":
              bool(np.linalg.norm(out["total_source_ward"])>0),
        }
        checks["pass"]=bool(
            all(val for name,val in checks.items()
                if not name.endswith("_max_abs") and name!="pass")
            and source_error<=1e-12 and ward_error<=1e-12
        )
        all_beta.append({"beta0":float(beta),"checks":checks})
    time_rejected=False
    try:
        clock.physical_source_ward(
            outputs[0]["assembled"]["total_rows"],
            x,a*np.array([1.001]+[1.0]*(nt-1)),H,kfund,"fd8"
        )
    except ValueError:
        time_rejected=True
    return {
       "cases":all_beta,
       "mock_calls":invokes,
       "q10_exact_match_relative_L2":diagnostics[
           "Repair26_R1_q10_vs_H3G_weighted_z10_relative_L2"
       ],
       "wrong_q10_detected_relative_L2":negative[
           "Repair26_R1_q10_vs_H3G_weighted_z10_relative_L2"
       ],
       "wrong_physical_time_grid_rejected":time_rejected,
       "synthetic_external_evaluators_only":(
           "q_cross_direct","lambda_cross_direct","reconstruct_m2_source"
       ),
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--json-out",required=True)
    args=ap.parse_args()
    blobs=exact_blobs()
    fixture=run_fixture()
    ok=bool(
      all(v["exact"] for v in blobs.values())
      and all(case["checks"]["pass"] for case in fixture["cases"])
      and len(fixture["cases"])==3
      and fixture["mock_calls"]=={"cross":4,"lambda":2,"M2":2}
      and fixture["q10_exact_match_relative_L2"]==0.0
      and fixture["wrong_q10_detected_relative_L2"]>1e-10
      and fixture["wrong_physical_time_grid_rejected"]
    )
    report={
      "classification":(
        "GE19_H4F3B_SYNTHETIC_PRODUCTION_WIRING_PASS"
        if ok else "GE19_H4F3B_SYNTHETIC_PRODUCTION_WIRING_IMPLEMENTATION_FAIL"
      ),
      "predata_classification":
        "GE19_H4F3B_PREDATA_SYNTHETIC_PRODUCTION_WIRING_AUDIT",
      "all_wiring_gates_pass":ok,
      "frozen_source_blobs":blobs,
      "manufactured_runtime":fixture,
      "actual_corrected_parent_binary_consumed":False,
      "certified_Repair32B_Z11_binary_consumed":False,
      "actual_six_source_H4F3b_executed":False,
      "full_operator_parent_Ward_derived":False,
      "H4_Z21_solve_performed":False,
      "Z21_certified":False,
      "lensing_licensed":False,
      "next_route":(
        "REAL_H4F3B_REQUIRES_HASH_MATCHED_REPAIR32B_Z11_AND_ORIGINAL_PARENTS"
        if ok else "FREEZE_SYNTHETIC_WIRING_IMPLEMENTATION_FAILURE"
      ),
    }
    path=Path(args.json_out);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(report,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print(json.dumps(report,sort_keys=True,indent=2,allow_nan=False))
    if not ok:raise SystemExit(3)

if __name__=="__main__":
    main()
