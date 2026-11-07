#!/usr/bin/env python3
"""Source-bound actual GE19 Cmat Ward: 16 integrated-jet exact conditions.

Construct ONLY the three actual independent Euler rows B, J and P from
the FROZEN ORIGINAL GE06 and GE07 c1 action generators, with Repair11
Lambda L row. Do not use manufactured Cmat, rescale source terms, solve
Z21, or read any actual H4 Ward defect.

This is a NEW analytic gate. Failure or resource exhaustion is UNRESOLVED,
never retroactively changes frozen physical science outcomes.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import sympy as sp
from ge19 import repair07_window_retarded_reduced_h3_z20_particular as r7

ROOT=Path(__file__).resolve().parents[1]
PINS={
 "ge06/analytic_aest_directional_source_generator.py":
    "a7afe0035054a9dca55d74a6497c081422114b4c",
 "ge07/pressureless_matter_directional_source_generator.py":
    "cde8da77a80799cef00fc7c09c3633310fc9e3d4",
 "ge19/repair07_window_retarded_reduced_h3_z20_particular.py":
    "e34d28a2062c748f48bc82fa928844b02631de25",
 "ge19/repair11_lambda_inclusive_reduced_h1_reclosure.py":
    "dbfa43ae11dbd3cfeeb1994a30237e9374dbb3e7",
 "ge19/repair13_self_consistent_reduced_background_h1_reclosure.py":
    "362d63d03d7b850fceae393f535353ded79aeea7",
 "ge19/h4f3d1_frozen_canonical_operator_ward.py":
    "60786ac14c9478801c5df9ccf458ead9a34ac827",
}
TINY=sp.S.Zero

def require(v,msg):
    if not bool(v): raise RuntimeError(msg)

def original_lock():
    out={}
    for name,want in PINS.items():
        got=subprocess.check_output(["git","rev-parse","HEAD:"+name],
                                   cwd=ROOT,text=True).strip()
        require(got==want,"ORIGINAL_SOURCE_BLOB_MISMATCH "+name)
        out[name]={"expected":want,"observed":got,"exact":True}
    s=(ROOT/"ge19/repair07_window_retarded_reduced_h3_z20_particular.py").read_text()
    d1=(ROOT/"ge19/h4f3d1_frozen_canonical_operator_ward.py").read_text()
    d11=(ROOT/"ge19/repair11_lambda_inclusive_reduced_h1_reclosure.py").read_text()
    d13=(ROOT/"ge19/repair13_self_consistent_reduced_background_h1_reclosure.py").read_text()
    facts={
      "original_raw_w_order":
        "w=(N,dr,S,u,phi,T,Sdot,udot,phidot,Tdot)" in s,
      "original_raw_GE06_L_Euler":
        'p6["L_f"]' in s and 'p6["L_x"]' in s,
      "original_raw_GE07_L_Euler":
        'p7["L_f"]' in s,
      "original_raw_GE06_L_momentum":
        'p6["L_t"]' in s,
      "original_raw_GE06_shift":
        'shift_ga=p6["b_f"]-ik*p6["b_x"]' in s,
      "original_raw_GE07_shift":
        'shift_m=p7["b_f"]' in s,
      "original_independent_L_projection":
        "EL_non=(iso+2*aniso)/3" in d1,
      "original_independent_L_momentum_term":
        "EL=EL_non-H*(D@pL)" in d1,
      "original_shift_time_derivative":
        "Eshift_time=H*(D@Eb)" in d1,
      "original_Lambda_action":
        "L_lambda = -6 rho_lambda N L R^2" in d11,
      "original_Lambda_L_projection":
        'C[6,0]=-18.0*rho*a*a' in d11 and
        'C[6,2]=-36.0*rho*a' in d11,
      "Repair13_Friedmann":
        "H2=rho_aest+rho_d+rho_l" in d13 and
        "rho_aest=(q*kq-kval)/3.0" in d13,
      "Repair13_background_pressure_derivative":
        "dH2_dx=-q*kq-3.0*rho_d" in d13,
      "Repair13_dust_action_density":
        "rho_d=r7.C_VALUES[tag]/a**3" in d13,
      "Repair07_GE07_raw_density_three_C":
        'rhob=3.0*C_VALUES[tag]/aa**3' in s,
    }
    require(all(facts.values()),"ORIGINAL_ROW_OR_BACKGROUND_BINDINGS_FAIL: "+str(facts))
    return out,facts

def source_rows():
    print("LOADING ORIGINAL FROZEN GE06/GE07 GENERATORS",flush=True)
    g6=r7.load_frozen_generator(
        ROOT/"ge06/analytic_aest_directional_source_generator.py",
        "ge06_h4f3d_actual_16jet")
    g7=r7.load_frozen_generator(
        ROOT/"ge07/pressureless_matter_directional_source_generator.py",
        "ge07_h4f3d_actual_16jet")
    require(len(g6.direction_args)==23,"GE06 direction arg layout changed")
    require(len(g7.direction_args)==9,"GE07 direction arg layout changed")
    a,H,Q,k,Cd,rhoL=sp.symbols(
        "a H Q k C_d rho_L",real=True,finite=True)
    n,dr,S,u,phi,T,Sdot,udot,phidot,Tdot=sp.symbols(
        "n dr S u phi T Sdot udot phidot Tdot",real=True)
    w=(n,dr,S,u,phi,T,Sdot,udot,phidot,Tdot)
    ik=sp.I*k
    old6=g6.direction_args
    # Exactly Repair07 _raw_local_outputs: drho enters GE07 only;
    # b, bx, and independent L-R anisotropy set to zero only in FIELD
    # direction after independently differentiating the full action.
    new6=(a,a*H,Q,n,S,S,sp.S.Zero,u,Sdot,ik*S,
          Sdot,ik*S,sp.S.Zero,udot,ik*u,
          phidot,ik*phi,ik*n,*old6[18:])
    require(len(new6)==23,"GE06 canonical argument count")
    sub6=dict(zip(old6,new6))
    rho_dust_action=3*Cd/a**3
    old7=g7.direction_args
    new7=(a,rho_dust_action,n,S,S,sp.S.Zero,dr,Tdot,ik*T)
    require(len(new7)==9,"GE07 canonical argument count")
    sub7=dict(zip(old7,new7))

    def ge6(key):
        return g6.coeff1[key].subs(sub6,simultaneous=True)
    def ge7(key):
        return g7.coeff1[key].subs(sub7,simultaneous=True)

    # These three source-bound rows reproduce the ORIGINAL 16x10 Cmat
    # row combination. Lambda's E_L is 1/3 of original isotropic row,
    # not a new coefficient fitted to Ward.
    print("ASSEMBLING THREE ORIGINAL ACTION-DERIVED EULER ROWS",flush=True)
    Eb=ge6("b_f")-ik*ge6("b_x")+ge7("b_f")
    J=(ge6("L_f")-ik*ge6("L_x")+ge7("L_f")
       -6*rhoL*a*a*n-12*rhoL*a*S)
    P=ge6("L_t")
    require(all(not e.has(*[z for z in
            (sp.Symbol("eps"),) if z in e.free_symbols])
            for e in (Eb,J,P)),"unexpected eps dependency")
    rows=[]
    for label,expr in (("B_shift",Eb),("J_L_nonderivative",J),
                       ("P_L_momentum",P)):
        cc=[sp.diff(expr,var) for var in w]
        rem=sp.expand(expr-sum(z*v for z,v in zip(cc,w)))
        require(rem==0,"NONLINEAR_OR_ZERO_OFFSET_"+label)
        rows.append(cc)
    return rows,dict(a=a,H=H,Q=Q,k=k,Cd=Cd,rhoL=rhoL,w=w,
                     action_parameters={
                       "KB":old6[18],"C_AeST":old6[19],
                       "K2":old6[20],"Q0":old6[21],"Z0":old6[22]})

def on_shell_coefficients(rows,p):
    B,J,P=rows
    a,H,Q,k,Cd,rhoL=(p[x] for x in ("a","H","Q","k","Cd","rhoL"))
    kb,cv,k2,q0,z0=(p["action_parameters"][x] for x in
                      ("KB","C_AeST","K2","Q0","Z0"))
    z=(Q-q0)/z0
    ee=sp.exp(z*z)
    K=2*k2*z0*z0*(ee-1)
    KQ=4*k2*(Q-q0)*ee
    KQQ=4*k2*ee*(1+2*z*z)
    H2=(Q*KQ-K)/3+Cd/a**3+rhoL
    Hdot=-(Q*KQ+3*Cd/a**3)/2
    Qdot=-3*H*KQ/KQQ
    def Dt(f):
        return (sp.diff(f,a)*a*H+sp.diff(f,H)*Hdot+
                sp.diff(f,Q)*Qdot)
    U=[-Dt(B[j])-sp.I*k*a*J[j]+sp.I*k*a*Dt(P[j])
       for j in range(10)]
    V=[-B[j]+sp.I*k*a*P[j] for j in range(10)]
    conditions=(
       [("field_"+str(j),U[j]) for j in range(6)]
      +[("time_N",V[0]),("time_drho",V[1])]
      +[("second_"+str(j),V[j]) for j in range(6,10)]
      +[("dynamic_first_"+str(j),U[j+6]+V[j+2])
        for j in range(4)]
    )
    require(len(conditions)==16,"not 16 jet conditions")
    return conditions,H2,{"K":K,"KQ":KQ,"KQQ":KQQ,
                          "Hdot":Hdot,"Qdot":Qdot}

def polynomial_reduce(expr,H,H2):
    """Exact rational polynomial reduction modulo Friedmann H^2-H2=0.

    This is an equality in the original analytic action's rational/exponential
    coefficient ring. A nonzero rem is a failure, not something to tune.
    """
    expr=sp.cancel(sp.together(expr))
    if expr==0: return True,sp.S.Zero
    num,den=sp.fraction(expr)
    try:
        reduced=sp.rem(num,H*H-H2,H)
    except Exception as ex:
        raise RuntimeError("FRIEDMANN_POLYNOMIAL_REDUCTION_ERROR "+repr(ex))
    reduced=sp.cancel(sp.together(reduced))
    ok=bool(reduced==0 or sp.simplify(reduced)==0)
    return ok,reduced

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--json-out",type=Path,required=True)
    args=ap.parse_args()
    require(not args.json_out.exists(),"REFUSE_OVERWRITE "+str(args.json_out))
    pins,bindings=original_lock()
    rows,p=source_rows()
    conditions,H2,derivs=on_shell_coefficients(rows,p)
    checked={}
    for i,(name,expr) in enumerate(conditions):
        print("CHECK_ACTUAL_SOURCE_BOUND_CMAT_JET "+
              str(i+1)+"/16 "+name,flush=True)
        ok,rem=polynomial_reduce(expr,p["H"],H2)
        checked[name]={
          "exact_zero_modulo_Repair13_Friedmann":bool(ok),
          "nonzero_remainder_preview":
              "" if ok else str(rem)[:1400],
        }
        print("RESULT "+name+"="+("EXACT_ZERO" if ok else "NOT_PROVEN"),
              flush=True)
    passed=all(x["exact_zero_modulo_Repair13_Friedmann"]
               for x in checked.values())
    out={
      "classification":(
       "GE19_ACTUAL_FROZEN_CMAT_16JET_EXACT_WARD_SYZYGY_PASS_H4_OPEN"
       if passed else
       "GE19_ACTUAL_CMAT_16JET_ANALYTIC_UNRESOLVED"),
      "original_source_blob_locks":pins,
      "original_source_row_and_background_bindings":bindings,
      "exact_source_bound_16_conditions":checked,
      "Repair13_background_derivatives":{
        "a_dot":"a H","H_dot":str(derivs["Hdot"]),
        "Q_dot":str(derivs["Qdot"]),
        "H2_Friedmann":str(H2),
      },
      "all_16_actual_Cmat_analytic_coefficients_exact":passed,
      "full_H4_Ward_certified":False,
      "Z21_certified":False,
      "lensing_licensed":False,
      "physical_FD4_FD8_error_budget_frozen":False,
      "claim_boundary":
       "Source-bound symbolic check of exact 16 integrated-jet GE06+"
       "GE07+Lambda linear operator syzygy, conditional on frozen Repair13"
       " background ODEs and original 16x10 Cmat row definitions. "
       "It does NOT evaluate actual mixed H4 parent/source/boundary Noether,"
       " real-grid FD4/FD8 truncation/roundoff, or certify Z21 or lensing.",
      "next_if_pass":
       "INSTANTIATE_G1_PARENTS_AND_G3_PHYSICAL_ERROR_BUDGET_BEFORE_ONE_FULL_H4_WARD"
       if passed else "FREEZE_EXACT_NONZERO_JET_COEFFICIENTS_AND_REVIEW_SOURCE_CONVENTIONS"
    }
    args.json_out.parent.mkdir(parents=True,exist_ok=True)
    args.json_out.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(out["classification"],flush=True)
    if not passed:
        raise SystemExit(3)

if __name__=="__main__":
    main()
