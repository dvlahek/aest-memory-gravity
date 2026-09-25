#!/usr/bin/env python3
"""H4F3d2: exact frozen GE07 dust and GE05 per-node bath parent Euler currents.

Build the REAL frozen lagrangians by compiling only their pinned symbolic
assignment AST, not importing their module-level generator campaigns.
Derive both conserved currents, scalar multipliers and the first-order
FLRW Euler inputs to the SIGNED mixed H4 Ward. No physical Z21, source
reweighting, fitted threshold or full all-parent Noether certificate.
"""
from __future__ import annotations
import argparse
import ast
import json
import subprocess
from pathlib import Path
import numpy as np
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
PINS={
 "ge19/h4f3d2_predata_dust_bath_parent_euler_currents.json":"6e9f83fc7f245bfedb82db53afd96ab2ba8616db",
 "ge19/h4f3d_predata_actual_operator_all_parent_ward_closure.json":"f1bd4eb52b7da96ac2d50ed9136e3e1a74635f51",
 "ge19/h4f3d1_frozen_canonical_operator_ward.py":"60786ac14c9478801c5df9ccf458ead9a34ac827",
 "ge19/h4f2b_signed_mixed_ward_template.py":"ab783ffe8242d8ff455647df8664a074f725ee81",
 "ge07/pressureless_matter_directional_source_generator.py":"cde8da77a80799cef00fc7c09c3633310fc9e3d4",
 "ge05/memory_directional_source_generator.py":"40837d77f89028da30c28899e2d0530a4401844e",
 "docs/ge19_h4f2a_dust_offshell_ward_valid_freeze.md":"ca21c65ce2da8d760aa12018aefd849b3b67adf9",
 "docs/ge19_h4f1_longitudinal_bath_ward_valid_freeze.md":"5aa99f10383a253e934c0c2833230fa714c3ef1d",
 "docs/ge19_h4f3d1_canonical_operator_ward_valid_freeze.md":"605a163fb9fa7e59e9babdbfdc279022b95d038a",
}

def blob_audit():
    result={}
    for path,want in PINS.items():
        got=subprocess.check_output(
            ["git","rev-parse","HEAD:"+path],cwd=ROOT,text=True
        ).strip()
        result[path]={"expected":want,"observed":got,"exact":got==want}
    return result

def frozen_symbolic_assignments(path,start,end):
    tree=ast.parse((ROOT/path).read_text(),filename=path)
    selected=[node for node in tree.body
              if getattr(node,"lineno",0)>=start
              and getattr(node,"end_lineno",10**9)<=end]
    if not selected or selected[0].lineno!=start:
        raise RuntimeError("Frozen symbolic assignment region shifted: "+path)
    env={"sp":sp}
    exec(compile(ast.fix_missing_locations(
        ast.Module(body=selected,type_ignores=[])),path,"exec"),env,env)
    return env

def exact(expr):
    return bool(sp.trigsimp(sp.factor(sp.cancel(sp.together(expr))))==0)

def first(expr,sub,eps):
    return sp.simplify(sp.diff(expr.subs(sub),eps).subs(eps,0))

def dust_analytic(d):
    N,L,R,b,rho,Tt,Tx=(d[z] for z in (
        "N","L","R","b","varrho","Tt","Tx"
    ))
    vol=N*L*R**2
    W=(Tt-b*Tx)/N
    V=Tx/L
    lag=d["lag"]
    pTt=sp.diff(lag,Tt)
    pTx=sp.diff(lag,Tx)
    pRho=sp.diff(lag,rho)
    pL=sp.diff(lag,L)
    pb=sp.diff(lag,b)
    gates={
      "dust_exact_frozen_action":exact(lag-vol*rho*(W**2-V**2-1)),
      "dust_T_time_current":exact(pTt-2*L*R**2*rho*W),
      "dust_T_spatial_current":
         exact(pTx+2*L*R**2*rho*b*W+2*N*R**2*rho*Tx/L),
      "dust_rho_multiplier_Euler_no_rho_factor":
         exact(pRho-vol*(W**2-V**2-1)),
      "dust_shift_action_source_bound":
         exact(pb-d["partial_map"]["b_f"]),
      "dust_L_action_source_bound":
         exact(pL-d["partial_map"]["L_f"]),
    }
    eps=sp.symbols("eps",real=True)
    a,r0=sp.symbols("a r0",positive=True,real=True)
    dN,dL,dR,db,drho,dTt,dTx=sp.symbols(
        "dN dL dR db drho dTt dTx",real=True
    )
    sub={N:1+eps*dN,L:a+eps*dL,R:a+eps*dR,b:eps*db,
         rho:r0+eps*drho,Tt:1+eps*dTt,Tx:eps*dTx}
    tcur=first(pTt,sub,eps)
    xcur=first(pTx,sub,eps)
    constraint=first(pRho,sub,eps)
    eL=first(pL,sub,eps)
    eb=first(pb,sub,eps)
    gates.update({
      "dust_FLRW_first_T_time_current":
        exact(tcur-2*a**3*r0*(dL/a+2*dR/a+drho/r0+dTt-dN)),
      "dust_FLRW_first_T_spatial_current":
        exact(xcur+2*a**3*r0*db+2*a*r0*dTx),
      "dust_FLRW_first_rho_Euler":
        exact(constraint-2*a**3*(dTt-dN)),
      "dust_FLRW_rho_Euler_independent_of_rho":
        exact(sp.diff(constraint,r0)),
      "dust_FLRW_first_L_Euler":
        exact(eL-2*a**2*r0*(dTt-dN)),
      "dust_FLRW_first_shift_Euler":
        exact(eb+2*a**3*r0*dTx),
      "dust_background_rho_and_shift_and_L_zero":
        all(exact(expr.subs(sub).subs(eps,0))
            for expr in (pRho,pb,pL)),
    })
    t=sp.symbols("t",real=True)
    af=sp.Function("a")(t)
    r0f=sp.symbols("rho0const",real=True)/af**3
    gates["dust_background_T_continuity_if_a3rho_constant"]=exact(
        sp.diff(2*af**3*r0f,t)
    )
    return gates,{
        "E_rho":"N*L*R**2*(W**2-(T_x/L)**2-1)",
        "E_T":"-d_t J_T^t-d_x J_T^x",
        "J_T^t":"2*L*R**2*rho*W",
        "J_T^x":"-2*L*R**2*rho*b*W-2*N*R**2*rho*T_x/L",
        "E_rho10":"2*a**3*(dTt-dN), no rho0 multiplier",
        "E_L10":"2*a**2*rho0*(dTt-dN)",
        "E_b10":"-2*a**3*rho0*dTx",
        "J_Tt10":"2*a**3*rho0*(dL/a+2*dR/a+drho/rho0+dTt-dN)",
        "J_Tx10":"-2*a**3*rho0*db-2*a*rho0*dTx",
    },(d,sub,eps,(pTt,pTx,pRho,pL,pb),(tcur,xcur,constraint,eL,eb))

def bath_analytic(d):
    N,L,R,b,u,pt,px,qt,qx,q,om,sw=(
      d[z] for z in ("N","L","R","b","r","pt","px","qt","qx","q","om","sw")
    )
    ch,sh=sp.cosh(u),sp.sinh(u)
    At=ch/N
    Ax=-b*ch/N+sh/L
    Aq=At*qt+Ax*qx
    Xphi=sh*(pt-b*px)/N+ch*px/L
    P=om*q-sw*Xphi
    vol=N*L*R**2
    lag=d["lag"]
    jt=sp.diff(lag,qt)
    jx=sp.diff(lag,qx)
    local=sp.diff(lag,q)
    el=sp.diff(lag,L)
    eb=sp.diff(lag,b)
    gates={
      "bath_exact_frozen_action":
        exact(lag-vol*(Aq**2-P**2)/4),
      "bath_q_time_current":
        exact(jt-vol*Aq*At/2),
      "bath_q_spatial_current":
        exact(jx-vol*Aq*Ax/2),
      "bath_q_local_Euler":
        exact(local+vol*om*P/2),
      "bath_shift_action_source_bound":
        exact(eb-d["partials"]["b"]),
      "bath_L_action_source_bound":
        exact(el-d["partials"]["L"]),
      "bath_A_dot_U_orthogonality_consistent":
        exact(At*(-N*sh+L*b*ch)+Ax*(L*ch)),
    }
    eps=sp.symbols("eps",real=True)
    a,Q=sp.symbols("a Q",positive=True,real=True)
    dN,dL,dR,db,du,dpt,dpx,dqt,dqx,dq=sp.symbols(
        "dN dL dR db du dpt dpx dqt dqx dq",real=True
    )
    sub={N:1+eps*dN,L:a+eps*dL,R:a+eps*dR,b:eps*db,
         u:eps*du,pt:Q+eps*dpt,px:eps*dpx,
         qt:eps*dqt,qx:eps*dqx,q:eps*dq}
    time=first(jt,sub,eps)
    space=first(jx,sub,eps)
    potential=first(local,sub,eps)
    el1=first(el,sub,eps)
    eb1=first(eb,sub,eps)
    gates.update({
      "bath_FLRW_first_q_time_current":
         exact(time-a**3*dqt/2),
      "bath_FLRW_first_q_spatial_current_zero":
         exact(space),
      "bath_FLRW_first_local_q_Euler":
         exact(potential+a**3*om*(om*dq-sw*(Q*du+dpx/a))/2),
      "bath_FLRW_first_metric_L_Euler_zero":
         exact(el1),
      "bath_FLRW_first_shift_Euler_zero":
         exact(eb1),
      "bath_FLRW_zero_background_E_q_and_currents":
         all(exact(expr.subs(sub).subs(eps,0))
             for expr in (jt,jx,local,el,eb)),
    })
    return gates,{
      "E_q_per_node":"-NLR**2*omega*(omega*q-sqrt(w)*Xphi)/2 -d_t(J_q^t)-d_x(J_q^x)",
      "J_q^t":"NLR**2*A(q)*A^t/2",
      "J_q^x":"NLR**2*A(q)*A^x/2",
      "E_q10":"-a**3*omega*(omega*dq-sqrt(w)*(Q*du+dphi_x/a))/2-d_t(a**3*dqt/2)",
      "J_qt10":"a**3*dqt/2",
      "J_qx10":"0",
      "E_L10_and_E_b10":"0 for the frozen quadratic per-node bath action",
      "eta_regularization_not_assumed":"raw per-node q; normalized eta-rescaled bath parent handled only in later all-sector gate",
    },(d,sub,eps,(jt,jx,local,el,eb),(time,space,potential,el1,eb1))

def signed_parent_coefficient():
    eps,eta=sp.symbols("eps eta",real=True)
    qnames=("T","rho","q_node")
    tests={}
    for name in qnames:
        e00,e10,e11,e20,e21=sp.symbols(
            name+"_E00 "+name+"_E10 "+name+"_E11 "+name+"_E20 "+name+"_E21"
        )
        f10x,f11x,f20x,f21x=sp.symbols(
            name+"_F10x "+name+"_F11x "+name+"_F20x "+name+"_F21x"
        )
        e=e00+eps*(e10+eta*e11)+eps**2*(e20+eta*e21)/2
        fx=eps*(f10x+eta*f11x)+eps**2*(f20x+eta*f21x)/2
        actual=sp.diff(sp.diff(e*fx,eps,2),eta).subs(
            {eps:0,eta:0})
        expected=e00*f21x+2*e10*f11x+2*e11*f10x
        tests[name+"_signed_mixed_parent_all_coefficients_exact"]=exact(
            actual-expected)
        tests[name+"_no_direct_E20_term_on_eta_independent_FLRW"]=exact(
            sp.diff(actual,e20))
        tests[name+"_omit_E10_or_E11_negative_controls"] = (
            not exact(expected-(e00*f21x+2*e11*f10x))
            and not exact(expected-(e00*f21x+2*e10*f11x)))
    return tests,{
        "dust_T_and_rho":
          "Sum_i [E_i00 F_i21,x+2 E_i10 F_i11,x+2 E_i11 F_i10,x], i=T,rho",
        "bath_per_node":
          "Sum_j [E_qj00 q_j21,x+2 E_qj10 q_j11,x+2 E_qj11 q_j10,x]",
        "dust_conditional_E00":
          "E_rho00=0 on W0**2-V0**2=1; E_T00=0 only when d_t(a**3*rho0)=0",
        "bath_conditional_E00":
          "E_qj00=0 for q0=0, Xphi0=0 after stated regularized eta convention",
        "other_parent_and_boundary_terms_needed":True,
    }

def _relative(a,b):
    return float(abs(a-b)/max(abs(a),abs(b),1e-15))

def manufactured(dust,bath):
    # Independently compare action exact first-order directional
    # derivatives to symmetric finite differences at deterministic,
    # moderate-amplitude synthetic values (no real GE19 parent).
    rows=[]
    for name,pack in (("dust",dust),("bath",bath)):
        env,sub,eps,exacts,linear=pack
        var_order=(
          ("N","L","R","b","varrho","Tt","Tx")
          if name=="dust" else
          ("N","L","R","b","r","pt","px","qt","qx","q")
        )
        synthetic={"N":0.015,"L":-0.021,"R":0.027,"b":0.031,
          "varrho":-0.009,"Tt":0.023,"Tx":0.033,"r":0.024,
          "pt":0.035,"px":-0.016,"qt":0.047,"qx":-0.013,"q":0.019}
        a=.79;r0=.18;Q=.12;om=1.23;sw=.36
        vals={"dN":synthetic["N"],"dL":synthetic["L"],
              "dR":synthetic["R"],"db":synthetic["b"],
              "drho":synthetic["varrho"],"dTt":synthetic["Tt"],
              "dTx":synthetic["Tx"],"du":synthetic["r"],
              "dpt":synthetic["pt"],"dpx":synthetic["px"],
              "dqt":synthetic["qt"],"dqx":synthetic["qx"],
              "dq":synthetic["q"]}
        substitutions={}
        for expr in sub.values():
            for z in expr.free_symbols:
                if str(z) in vals:
                    substitutions[z]=vals[str(z)]
                elif str(z)=="a":substitutions[z]=a
                elif str(z)=="r0":substitutions[z]=r0
                elif str(z)=="Q":substitutions[z]=Q
        substitutions[env.get("om",sp.Symbol("om"))]=om
        substitutions[env.get("sw",sp.Symbol("sw"))]=sw
        h=1e-5
        def number(expr):
            return float(sp.N(expr.subs(substitutions)))
        for item,derivative in zip(exacts,linear):
            expression=item.subs(sub)
            plus=number(expression.subs(eps,h))
            minus=number(expression.subs(eps,-h))
            fd=(plus-minus)/(2*h)
            expected=number(derivative)
            rows.append({"sector":name,"Euler_or_current":str(item)[:70],
                "nonzero_first_order":bool(abs(expected)>1e-10),
                "finite_directional_relative":_relative(fd,expected),
                "finite_directional_abs":float(abs(fd-expected))})
    return rows

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--json-out",required=True)
    args=parser.parse_args()
    pins=blob_audit()
    frozen_dust=frozen_symbolic_assignments(
        "ge07/pressureless_matter_directional_source_generator.py",25,40)
    frozen_bath=frozen_symbolic_assignments(
        "ge05/memory_directional_source_generator.py",17,26)
    dgate,df,dp=dust_analytic(frozen_dust)
    bgate,bf,bp=bath_analytic(frozen_bath)
    mgate,formal=signed_parent_coefficient()
    sample=manufactured(dp,bp)
    finite=bool(all(v["finite_directional_abs"]<=1e-8
                    and (not v["nonzero_first_order"]
                         or v["finite_directional_relative"]<=1e-6)
                    for v in sample))
    ok=bool(all(v["exact"] for v in pins.values())
            and all(dgate.values()) and all(bgate.values())
            and all(mgate.values()) and finite)
    report={
      "classification":(
          "GE19_H4F3D2_DUST_BATH_PARENT_EULER_CURRENT_COMPILER_PASS"
          if ok else "GE19_H4F3D2_PARENT_EULER_CURRENT_COMPILER_FAIL"),
      "preregistration":"GE19_H4F3D2_PREDATA_DUST_BATH_PARENT_EULER_CURRENT_COMPILER",
      "frozen_git_blobs":pins,
      "dust_exact_symbolic_gates":dgate,
      "dust_derived_parent_dictionary":df,
      "bath_exact_symbolic_gates":bgate,
      "bath_derived_parent_dictionary":bf,
      "signed_mixed_parent_coefficient_gates":mgate,
      "signed_parent_dictionary":formal,
      "manufactured_exact_vs_symmetric_directional":sample,
      "manufactured_all_gates_pass":finite,
      "all_restricted_gates_pass":ok,
      "actual_H3F_H3G_Z11_source_arrays_loaded":False,
      "remaining_GE06_Einstein_aether_scalar_and_boundary_parent_terms_derived":False,
      "complete_all_sector_parent_Euler_residuals_evaluated":False,
      "full_H4_Noether_structural_PASS":False,
      "H4_Z21_solve_performed":False,
      "Z21_certified":False,
      "lensing_licensed":False,
      "next_route":(
         "DERIVE_REMAINING_EINSTEIN_AEST_DUST_BATH_SIGNED_PARENT_AND_BOUNDARY_TERMS"
         if ok else "FREEZE_LOCALIZED_PARENT_CURRENT_COMPILER_FAILURE"),
      "claim_boundary":"Action-bound GE07/GE05 per-node local parent Euler currents and their formal mixed coefficient are a restricted necessary analytic input only. They do not certify actual corrected-parent residuals, complete boundary cancellation, an actual H4 Ward or Z21."
    }
    out=Path(args.json_out)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print(json.dumps(report,indent=2,sort_keys=True,allow_nan=False))
    if not ok:raise SystemExit(3)

if __name__=="__main__":main()
