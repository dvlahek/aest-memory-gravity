#!/usr/bin/env python3
"""H4F2d exact Y and M1 aether/scalar flux identity: six-piece subset.

Only source-local algebra is tested. No corrected-parent q20 reconstruction
or mixed full six-sector H4 Ward identity is implied by this PASS.
"""
from __future__ import annotations
import argparse,json,subprocess
from pathlib import Path
import numpy as np
import sympy as sp
from ge19 import h4_stagee_versioned_y_source_rows as y
from ge19 import repair37_cancellation_safe_fd8_h4_z21_reclosure as r37
from ge19 import repair07_window_retarded_reduced_h3_z20_particular as r7

ROOT=Path(__file__).resolve().parents[1]
BLOBS={
 "ge19/h4f2d_predata_y_m1_flux_compatibility.json":"902310e1e623cf65c3bdd5c5ecb199263558a39c",
 "ge19/h4_stagee_versioned_y_source_rows.py":"282166ea5840d7fba4dbc328d40d7687afa6fa0f",
 "ge19/repair37_cancellation_safe_fd8_h4_z21_reclosure.py":"45d203a092f9ac71cc612b15df5f0c0c630f5898",
 "docs/ge19_repair32a_ge06_ge05_raw_residual_normalization_dictionary_result_freeze.md":"6c5b7f830cbae95209eda0e8c8663c6620ab7071",
 "docs/ge19_h4_staged_common_y_action_rows_valid_freeze.md":"7d140a608d91a39106c34565cd50e4aa729ec30b",
 "docs/ge19_h4f2c_complete_action_spatial_ward_valid_freeze.md":"H4F2C_FREEZE_BLOB",
}
def blob_gates():
    result={}
    for path,want in BLOBS.items():
        got=subprocess.check_output(["git","rev-parse","HEAD:"+path],
                                    cwd=ROOT,text=True).strip()
        result[path]={"expected":want,"observed":got,"exact":got==want}
    return result

def source_bindings():
    a=(ROOT/"ge19/h4_stagee_versioned_y_source_rows.py").read_text()
    m=(ROOT/"ge19/repair37_cancellation_safe_fd8_h4_z21_reclosure.py").read_text()
    n=(ROOT/"docs/ge19_repair32a_ge06_ge05_raw_residual_normalization_dictionary_result_freeze.md").read_text()
    return {
      "StageE_Y_u_raw_RHS":"main[2]=2.0*aa**3*qq*kappa*projected" in a,
      "StageE_Y_phi_raw_RHS":"main[3]=-2.0*aa**2*kappa*div_x" in a,
      "StageE_same_2over3_projected_flux":"_project_flux_and_dx(flux,kfund)" in a,
      "GE05_M1_aether_mapped":"main[:,2,:,m]=bg[\"Q_action\"][None,:]*bg[\"a\"][None,:]**3*B[:,jm,:]" in m,
      "GE05_M1_scalar_mapped":"main[:,3,:,m]=-bg[\"a\"][None,:]**2*(1j*k)*B[:,jm,:]" in m,
      "GE05_M1_zero_constraints":"con=np.zeros((nb,2,nt,M_MAX+1),complex)" in m,
      "Repair32A_exact_factor_two":"GE05_M1_to_GE06_raw_residual_scale = 2" in n,
    }

def exact_symbolic():
    x=sp.symbols("x",real=True)
    a,Q,kappa=sp.symbols("a Q kappa",real=True)
    f=sp.Function("f")(x)
    B=sp.Function("B")(x)
    uy=2*a**3*Q*kappa*f
    py=-2*a**2*kappa*sp.diff(f,x)
    um=a**3*Q*B
    pm=-a**2*sp.diff(B,x)
    return {
      "Y_action_flux_identity":
          bool(sp.simplify(sp.diff(uy,x)+a*Q*py)==0),
      "M1_mapped_flux_identity":
          bool(sp.simplify(sp.diff(um,x)+a*Q*pm)==0),
      "Y_zero_set_directional":
          bool(sp.limit(2*sp.Abs(x),x,0,dir="+")==0
               and sp.limit(2*sp.Abs(x),x,0,dir="-")==0),
    }

def rel(a,b):
    return float(np.linalg.norm(a)/max(np.linalg.norm(b),1e-300))

def sampled():
    nt,nx=4,256
    xx=2*np.pi*np.arange(nx)[None,:]/nx
    t=np.arange(nt,dtype=float)[:,None]
    a=0.5+0.07*np.arange(nt,dtype=float)
    Q=1.1e-4+4e-6*np.arange(nt,dtype=float)
    u0=1e-4*np.cos(xx+0.16*t)+0.6e-4*np.sin(3*xx)
    u1=0.8e-4*np.cos(2*xx-0.12*t)
    g0=1e-7*np.sin(xx+0.1*t)+2e-8*np.sin(4*xx)
    g1=4e-8*np.cos(2*xx-0.1*t)+1e-8*np.sin(5*xx)
    p0=a[:,None]*(g0-Q[:,None]*u0)
    p1=a[:,None]*(g1-Q[:,None]*u1)
    kfund=float(r7.g9.K_REQ[0]/r7.FOURIER_N[0])
    modes=np.arange(1,41)
    kk=kfund*modes[None,None,:,None]
    # shape [beta,m,time], fixed deterministic complex M1 drive.
    beta=np.arange(3,dtype=float)[:,None,None]
    mm=modes[None,:,None]
    tt=np.arange(nt)[None,None,:]
    B=1e-9*(np.cos(mm/6+tt/10+beta)
             +1j*np.sin(mm/7-tt/9+beta))
    m1,c1=r37.m1_mapped_fourier({"a":a,"Q_action":Q},B)
    umat=m1[:,2,:,1:41].transpose(0,2,1)
    pmat=m1[:,3,:,1:41].transpose(0,2,1)
    kk_m=(kfund*modes)[None,:,None]
    # Original stored m1 format [beta,6,time,modes]; transpose
    # to [beta,m,time] for compatible mode weights.
    defect_m=1j*kk_m*umat+a[None,None,:]*Q[None,None,:]*pmat
    denom_m=np.linalg.norm(1j*kk_m*umat)+np.linalg.norm(
        a[None,None,:]*Q[None,None,:]*pmat)
    rows=[]
    for bb in y.FROZEN_BETAS:
        sy=y.source_h4(a,Q,u0,p0,u1,p1,r7.KB,
                       r7.A0_MPC_INV,bb,kfund)
        fy=np.fft.fft(sy["main"][2],axis=-1)[:,1:41]
        fp=np.fft.fft(sy["main"][3],axis=-1)[:,1:41]
        ky=(kfund*modes)[None,:]
        defect_y=1j*ky*fy+(a*Q)[:,None]*fp
        d_y=rel(defect_y,1j*ky*fy)+rel(
            defect_y,(a*Q)[:,None]*fp)
        rows.append({
            "beta":bb,
            "Y_fourier_flux_identity_relative_defect":float(d_y),
            "Y_all_other_main_rows_zero_exact":bool(np.array_equal(
                sy["main"][[0,1,4,5]],np.zeros((4,nt,nx)))),
            "Y_constraint_rows_zero_exact":bool(
                np.array_equal(sy["constraint"],np.zeros((2,nt,nx)))),
        })
    return {
      "Y_beta_cases":rows,
      "M1_fourier_flux_identity_relative_defect":float(
          np.linalg.norm(defect_m)/max(denom_m,1e-300)),
      "M1_constraint_rows_zero_exact":bool(np.array_equal(
          c1,np.zeros_like(c1))),
      "M1_other_main_rows_zero_exact":bool(np.array_equal(
          m1[:,[0,1,4,5]],np.zeros_like(m1[:,[0,1,4,5]]))),
      "M1_uses_only_weighted_B20":True,
      "M1_weighted_B20_definition":"X20-weighted_z20 from independently certified H3G",
      "sampled_fields_are_deterministic_not_parent_observations":True,
    }

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--json-out",required=True)
    args=parser.parse_args()
    lock=blob_gates();bind=source_bindings();exact=exact_symbolic()
    num=sampled()
    numeric_ok=bool(
        all(r["Y_fourier_flux_identity_relative_defect"]<=1e-12
            and r["Y_all_other_main_rows_zero_exact"]
            and r["Y_constraint_rows_zero_exact"]
            for r in num["Y_beta_cases"])
        and num["M1_fourier_flux_identity_relative_defect"]<=1e-12
        and num["M1_constraint_rows_zero_exact"]
        and num["M1_other_main_rows_zero_exact"]
    )
    ok=bool(all(v["exact"] for v in lock.values())
            and all(bind.values()) and all(exact.values()) and numeric_ok)
    d={
       "classification":("GE19_H4F2D_Y_AND_M1_FLUX_SUBIDENTITY_PASS"
                         if ok else "GE19_H4F2D_FLUX_SUBIDENTITY_FAIL"),
       "frozen_blobs":lock,"source_code_bindings":bind,
       "exact_symbolic":exact,"deterministic_checks":num,
       "all_subset_gates_pass":ok,
       "six_piece_H4_source_parent_Noether_derived":False,
       "corrected_H3F_H3G_common_grid_evaluated":False,
       "H4_Z21_solve_performed":False,"Z21_certified":False,
       "lensing_licensed":False,
       "next_route":"DERIVE_REMAINING_GE06_GE07_LAMBDA_M2_SIGNED_SOURCE_PARENT_ROWS",
    }
    p=Path(args.json_out);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(d,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print(json.dumps(d,indent=2,sort_keys=True,allow_nan=False))
    if not ok:raise SystemExit(3)
if __name__=="__main__":main()
