#!/usr/bin/env python3
"""H4F3d1: independent frozen GE19 canonical-operator Ward compiler.

Extract signed linear Euler shift/independent L rows from the original
non-gauge-fixed 16x10 Cmat, including physical time derivative of the
L momentum. Manufactured polynomial data exercise the ORIGINAL FD4
stencil and derivative of Cmat(x)*w(x), with negative controls.

This is a necessary operator dictionary gate, not a complete actual
all-parent H4 Ward/Noether test or a Z21 solve.
"""
from __future__ import annotations
import argparse
import json
import subprocess
from pathlib import Path
import numpy as np
import sympy as sp
from ge19 import repair07_window_retarded_reduced_h3_z20_particular as r7

ROOT=Path(__file__).resolve().parents[1]
PINS={
 "ge19/h4f3d1_predata_frozen_canonical_operator_ward.json":
   "4577de495692ecbe4c07d1156ffab2abfc99e96d",
 "ge19/h4f3d_predata_actual_operator_all_parent_ward_closure.json":
   "f1bd4eb52b7da96ac2d50ed9136e3e1a74635f51",
 "ge19/repair07_window_retarded_reduced_h3_z20_particular.py":
   "e34d28a2062c748f48bc82fa928844b02631de25",
 "ge19/h4f2b_signed_mixed_ward_template.py":
   "ab783ffe8242d8ff455647df8664a074f725ee81",
 "ge19/h4f2h_physical_time_source_ward_bridge.py":
   "65ce1e68a2f77e063c4bb8848d770abb4baeeebf",
 "docs/ge19_h4f3b_actual_corrected_six_source_valid_local_freeze.md":
   "578768817615807260afc2d7baaa24d2c4928858",
}

def pinned_blobs():
    out={}
    for path,want in PINS.items():
        got=subprocess.check_output(
            ["git","rev-parse","HEAD:"+path],cwd=ROOT,text=True
        ).strip()
        out[path]={"expected":want,"observed":got,"exact":got==want}
    return out

def frozen_dictionary():
    txt=(ROOT/"ge19/repair07_window_retarded_reduced_h3_z20_particular.py").read_text()
    ward=(ROOT/"ge19/h4f2b_signed_mixed_ward_template.py").read_text()
    return {
      "noniso_is_full_L_plus_R_without_momentum_time":
        'non_iso=p6["L_f"]+p6["R_f"]-ik*(p6["L_x"]+p6["R_x"])+p7["L_f"]+p7["R_f"]' in txt,
      "independent_anisotropy_is_full_L_minus_R_over_two":
        'aniso_ga=(p6["L_f"]-ik*p6["L_x"])-0.5*(p6["R_f"]-ik*p6["R_x"])' in txt
        and 'aniso_m=p7["L_f"]-0.5*p7["R_f"]' in txt,
      "shift_is_GE06_plus_GE07_original":
        'shift_ga=p6["b_f"]-ik*p6["b_x"]' in txt
        and 'shift_m=p7["b_f"]' in txt,
      "frozen_16_row_order_matches_original":
        'non_iso,non_u,non_phi,non_T,\n        shift_ga,shift_m,aniso_ga,aniso_m,\n        p6["L_t"],p6["R_t"]' in txt,
      "old_noether_elimination_uses_anisotropy_not_lapse":
        'Cmat[12:13]+Cmat[13:14]' in txt
        and 'Rr[5,7]=1.0' in txt,
      "exact_GE19_projection_in_signed_ward_template":
        '"Euler_L_projection":"E_L=(E_iso+2 E_aniso)/3"' in ward,
      "original_FD4_including_boundary_rows":
        'def fd4_matrix(n:int,x0:float,x1:float)' in txt
        and 'D[0,0:5]=np.asarray([-25,48,-36,16,-3],float)/(12*h)' in txt,
    }

def symbolic_rows_and_sign():
    A,B,dpL,dpR=sp.symbols("A B dpL dpR")
    Eiso=A+B-dpL-dpR
    Eaniso=A-B/sp.Integer(2)-dpL+dpR/sp.Integer(2)
    EL=(Eiso+2*Eaniso)/3
    ER=(2*Eiso-2*Eaniso)/3
    Lb,Ll,Sb,Sl,a,k,H,DB,DP=sp.symbols(
        "Lb Ll Sb Sl a k H DB DP"
    )
    actual=-DB*(Lb-Sb)-sp.I*k*a*(Ll-Sl)
    operator=-DB*Lb-sp.I*k*a*Ll
    source=DB*Sb+sp.I*k*a*Sl
    return {
      "E_L_exact_from_iso_aniso_with_time_momentum":
        bool(sp.simplify(EL-(A-dpL))==0),
      "E_R_exact_from_iso_aniso_with_time_momentum":
        bool(sp.simplify(ER-(B-dpR))==0),
      "signed_E_equals_L_minus_S_ward_factorization":
        bool(sp.simplify(actual-operator-source)==0),
      "physical_clock_is_H_times_D_log_a_not_D_log_a_alone":
        bool(sp.simplify(H*DP-DP)==(H-1)*DP),
    }

def _validate(C,w,x,a,H,k):
    C=np.asarray(C,complex)
    w=np.asarray(w,complex)
    x=np.asarray(x,float)
    a=np.asarray(a,float)
    H=np.asarray(H,float)
    nt=len(x)
    if (x.ndim!=1 or nt<9 or C.shape!=(nt,16,10)
        or w.shape!=(nt,10) or a.shape!=(nt,) or H.shape!=(nt,)
        or not np.isfinite(C).all() or not np.isfinite(w).all()
        or not np.isfinite(x).all() or not np.isfinite(a).all()
        or not np.isfinite(H).all() or not np.all(a>0)
        or not np.all(H>0) or not np.isfinite(k) or k<0
        or not np.all(np.diff(x)>0)
        or not np.allclose(a,np.exp(x),rtol=1e-12,atol=1e-14)):
        raise ValueError("invalid common GE19 canonical operator/time grid")
    h=(x[-1]-x[0])/(nt-1)
    if not np.allclose(np.diff(x),h,rtol=1e-9,atol=1e-13):
        raise ValueError("H4F3d1 FD4 only on frozen uniform ln(a) grid")
    return C,w,x,a,H

def operator_ward_from_frozen_Cmat(C,w,x,a,H,k):
    """Return independent linear operator Ward; accepts actual frozen Cmat.

    E_b = (C10+C11) w.
    E_L = [C6+2(C12+C13)]w/3 - H*D4_x(C14 w).
    W_op = -H*D4_x E_b - i*k*a*E_L.

    Never assert W_op=0: requires actual six-source and signed parents.
    """
    C,w,x,a,H=_validate(C,w,x,a,H,k)
    products=np.einsum("nij,nj->ni",C,w,optimize=True)
    D=r7.fd4_matrix(len(x),float(x[0]),float(x[-1]))
    Eb=products[:,10]+products[:,11]
    iso=products[:,6]
    aniso=products[:,12]+products[:,13]
    pL=products[:,14]
    pR=products[:,15]
    EL_non=(iso+2*aniso)/3
    EL=EL_non-H*(D@pL)
    Eshift_time=H*(D@Eb)
    ward=-Eshift_time-1j*float(k)*a*EL
    return {
       "operator_ward":ward,
       "Euler_shift":Eb,
       "Euler_L":EL,
       "Euler_L_nonderivative":EL_non,
       "pL":pL,"pR":pR,
       "original_pS_minus_pL_pR":products[:,0]-pL-pR,
       "shift_physical_time_derivative":Eshift_time,
       "L_momentum_physical_time_derivative":H*(D@pL),
       "source_ward_not_evaluated":True,
       "all_parent_Euler_residuals_not_evaluated":True,
    }

def _rel(a,b):
    A=np.asarray(a,complex);B=np.asarray(b,complex)
    return float(np.linalg.norm(A-B)/max(
        np.linalg.norm(A),np.linalg.norm(B),1e-300
    ))

def manufactured(nt):
    # C(x) and w(x) independently polynomial degree<=2. Their products
    # are degree<=4, so the frozen FD4 incl edges differentiates exactly.
    x=np.linspace(np.log(.4),0.,nt)
    a=np.exp(x)
    H=0.84+0.1*(x-x[0])
    k=.31*8
    ix=np.arange(16)[:,None]
    jx=np.arange(10)[None,:]
    C0=(.02*(1+ix+jx)/27+.03j*np.cos(ix+2*jx))/ (1+ix+jx)
    C1=.1*C0+(.007+.003j)*(ix+1)/(jx+3)
    C2=.08*C0+(.009-.002j)*(jx+1)/(ix+5)
    C=np.stack([C0+xq*C1+xq*xq*C2 for xq in x])
    j=np.arange(10)
    w0=(.05+.001j)*(j+1)/(j+3)
    w1=(.03-.002j)*(j+2)/(j+5)
    w2=(.014+.003j)*(j+3)/(j+7)
    w=np.stack([w0+xq*w1+xq*xq*w2 for xq in x])
    cp=np.stack([C1+2*xq*C2 for xq in x])
    wp=np.stack([w1+2*xq*w2 for xq in x])
    vals=operator_ward_from_frozen_Cmat(C,w,x,a,H,k)
    exact_derivative=np.einsum("nij,nj->ni",cp,w,optimize=True)+np.einsum("nij,nj->ni",C,wp,optimize=True)
    full=np.einsum("nij,nj->ni",C,w,optimize=True)
    derivative_shift=exact_derivative[:,10]+exact_derivative[:,11]
    derivative_pL=exact_derivative[:,14]
    EL_exact=(full[:,6]+2*(full[:,12]+full[:,13]))/3-H*derivative_pL
    op_exact=-H*derivative_shift-1j*k*a*EL_exact
    D=r7.fd4_matrix(nt,x[0],x[-1])
    poly4=x**4-0.3*x**3+0.2*x**2+0.3*x+1.0
    poly4prime=4*x**3-0.9*x**2+0.4*x+0.3
    # Negative controls must have significant exact discrepancy.
    no_momentum=-H*derivative_shift-1j*k*a*(full[:,6]+2*(full[:,12]+full[:,13]))/3
    omit_Cdot=-H*(np.einsum("nij,nj->ni",C,wp,optimize=True)[:,10:12].sum(axis=1))-1j*k*a*(
        (full[:,6]+2*(full[:,12]+full[:,13]))/3-H*np.einsum("nij,nj->ni",C,wp,optimize=True)[:,14])
    wrong_iso=-H*derivative_shift-1j*k*a*(
        full[:,6]-H*derivative_pL)
    exact_error=float(np.max(np.abs(vals["operator_ward"]-op_exact)))
    res={
      "Nt":nt,
      "FD4_degree4_polynomial_relative_L2":_rel(D@poly4,poly4prime),
      "FD4_degree4_polynomial_max_abs":float(np.max(np.abs(D@poly4-poly4prime))),
      "full_Cmat_product_operator_relative_L2":_rel(vals["operator_ward"],op_exact),
      "full_Cmat_product_operator_max_abs":exact_error,
      "negative_omit_momentum_relative_L2":_rel(no_momentum,op_exact),
      "negative_omit_Cmat_time_derivative_relative_L2":_rel(omit_Cdot,op_exact),
      "negative_wrong_isotropic_only_relative_L2":_rel(wrong_iso,op_exact),
      "all_outputs_finite":bool(np.isfinite(vals["operator_ward"]).all()),
      "source_parent_not_claimed":bool(vals["source_ward_not_evaluated"] and vals["all_parent_Euler_residuals_not_evaluated"]),
    }
    res["pass"]=bool(
        res["FD4_degree4_polynomial_relative_L2"]<=1e-10
        and res["FD4_degree4_polynomial_max_abs"]<=1e-10
        and res["full_Cmat_product_operator_relative_L2"]<=1e-10
        and res["full_Cmat_product_operator_max_abs"]<=1e-10
        and min(res[k] for k in (
           "negative_omit_momentum_relative_L2",
           "negative_omit_Cmat_time_derivative_relative_L2",
           "negative_wrong_isotropic_only_relative_L2"
        ))>1e-4
        and res["all_outputs_finite"] and res["source_parent_not_claimed"]
    )
    return res

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--json-out",required=True)
    args=parser.parse_args()
    pins=pinned_blobs()
    source=frozen_dictionary()
    symbolic=symbolic_rows_and_sign()
    cases=[manufactured(nt) for nt in (64,128)]
    pass_all=bool(all(v["exact"] for v in pins.values()) and
                  all(source.values()) and all(symbolic.values()) and
                  all(c["pass"] for c in cases))
    report={
       "classification":("GE19_H4F3D1_CANONICAL_OPERATOR_WARD_COMPILER_PASS"
                         if pass_all else "GE19_H4F3D1_OPERATOR_ROW_OR_DISCRETIZATION_FAIL"),
       "predata_classification":"GE19_H4F3D1_PREDATA_FROZEN_CANONICAL_OPERATOR_WARD_COMPILER",
       "frozen_git_blobs":pins,
       "bound_original_Cmat_and_Ge19_row_semantics":source,
       "exact_symbolic_projection_and_source_signs":symbolic,
       "manufactured_FD4_product_cases":cases,
       "all_compiler_gates_pass":pass_all,
       "actual_H4F3b_source_npz_loaded":False,
       "actual_H3F_H3G_Z11_parents_loaded":False,
       "full_linear_operator_plus_all_parent_Noether_derived":False,
       "H4_Z21_solve_performed":False,
       "Z21_certified":False,
       "lensing_licensed":False,
       "next_route":"PREREGISTER_INTEGRATED_ACTUAL_PARENT_OPERATOR_AND_ALL_EULER_BOUNDARY_GATE" if pass_all else "FREEZE_CANONICAL_OPERATOR_COMPILER_FAILURE",
       "claim_boundary":"This result freezes the source-bound canonical linear operator Euler row dictionary and manufactured physical FD4 implementation only. It does not assert that the operator Ward is zero or cancel actual H4F3b source without the complete signed parent and boundary terms.",
    }
    p=Path(args.json_out)
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print(json.dumps(report,indent=2,sort_keys=True,allow_nan=False))
    if not pass_all:
        raise SystemExit(3)

if __name__=="__main__":
    main()
