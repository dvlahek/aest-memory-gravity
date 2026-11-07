#!/usr/bin/env python3
"""Exact frozen-source linear GE06+Lambda/GE07 lapse-Ward balance.

Read only pinned original action assignments via AST. No generator import,
no Z21 solve, no observed H4 Ward defect or physical Cmat certification.
"""
from __future__ import annotations
import argparse
import ast
import json
import subprocess
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
PINS={
    "ge06/analytic_aest_directional_source_generator.py":
        "a7afe0035054a9dca55d74a6497c081422114b4c",
    "ge07/pressureless_matter_directional_source_generator.py":
        "cde8da77a80799cef00fc7c09c3633310fc9e3d4",
    "ge19/repair11_lambda_inclusive_reduced_h1_reclosure.py":
        "dbfa43ae11dbd3cfeeb1994a30237e9374dbb3e7",
    "ge19/repair13_self_consistent_reduced_background_h1_reclosure.py":
        "362d63d03d7b850fceae393f535353ded79aeea7",
    "ge19/repair07_window_retarded_reduced_h3_z20_particular.py":
        "e34d28a2062c748f48bc82fa928844b02631de25",
    "ge19/h4f3d1_frozen_canonical_operator_ward.py":
        "60786ac14c9478801c5df9ccf458ead9a34ac827",
}

def need(ok, message):
    if not bool(ok):
        raise RuntimeError(message)

def zero(expr):
    return bool(sp.cancel(sp.together(sp.expand(expr.doit()))) == 0)

def frozen_assignments(path, first_tuple, last_name):
    source=(ROOT/path).read_text()
    nodes=ast.parse(source).body
    start=next(i for i,n in enumerate(nodes)
               if isinstance(n,ast.Assign) and len(n.targets)==1
               and isinstance(n.targets[0],ast.Tuple)
               and [z.id for z in n.targets[0].elts]==list(first_tuple))
    end=next(i for i in range(start,len(nodes))
             if isinstance(nodes[i],ast.Assign)
             and len(nodes[i].targets)==1
             and isinstance(nodes[i].targets[0],ast.Name)
             and nodes[i].targets[0].id==last_name)
    selected=nodes[start:end+1]
    need(all(isinstance(n,ast.Assign) for n in selected),
         "original action assignment structure changed: "+path)
    env={"sp":sp}
    exec(compile(ast.fix_missing_locations(
         ast.Module(body=selected,type_ignores=[])),path,"exec"),env,env)
    return env

def exact_dust():
    e=frozen_assignments(
       "ge07/pressureless_matter_directional_source_generator.py",
       ("N","L","R","b","varrho","Tt","Tx"),"partial_map")
    n,l,r,b,rho,tt,tx=[e[k] for k in
                       ("N","L","R","b","varrho","Tt","Tx")]
    lag=n*l*r**2*rho*(((tt-b*tx)/n)**2-(tx/l)**2-1)
    need(zero(e["lag"]-lag),"GE07 source lagrangian mismatch")
    for k,v in {"N_f":n,"L_f":l,"R_f":r,"b_f":b,
                "rho_f":rho,"T_t":tt,"T_x":tx}.items():
        need(zero(e["partial_map"][k]-sp.diff(e["lag"],v)),
             "GE07 source partial mismatch "+k)
    t,x,eps=sp.symbols("t x eps",real=True)
    D=sp.symbols("D",real=True)
    a=sp.Function("a")(t)
    F={k:sp.Function(k)(t,x) for k in ("N","L","R","b","varrho","T")}
    rep={n:F["N"],l:F["L"],r:F["R"],b:F["b"],
         rho:F["varrho"],tt:sp.diff(F["T"],t),
         tx:sp.diff(F["T"],x)}
    physical=e["lag"].xreplace(rep)
    Euler={k:sp.diff(physical,F[k])
           for k in ("N","L","R","b","varrho")}
    Euler["T"]=(-sp.diff(sp.diff(physical,sp.diff(F["T"],t)),t)
                -sp.diff(sp.diff(physical,sp.diff(F["T"],x)),x))
    W=(sum(Euler[k]*sp.diff(F[k],x) for k in F)
       -sp.diff(F["L"]*Euler["L"]-F["b"]*Euler["b"],x)
       -sp.diff(Euler["b"],t))
    need(zero(W),"GE07 exact off-shell Euler Ward failed")
    dn,dl,dr,db,dp,dT=[sp.Function("d"+k)(t,x)
                        for k in ("N","L","R","b","rho","T")]
    sub={n:1+eps*dn,l:a+eps*dl,r:a+eps*dr,b:eps*db,
         rho:D/a**3+eps*dp,tt:1+eps*sp.diff(dT,t),
         tx:eps*sp.diff(dT,x)}
    def c(k,order):
        v=e["partial_map"][k].subs(sub,simultaneous=True)
        return sp.simplify(sp.diff(v,eps,order).subs(eps,0))
    EN0=c("N_f",0); EL0=c("L_f",0)
    ER0=c("R_f",0); Eb0=c("b_f",0); Erho0=c("rho_f",0)
    EL1=c("L_f",1); Eb1=c("b_f",1)
    need(zero(EN0+2*D),"GE07 EN00 != -2D")
    need(all(zero(z) for z in (EL0,ER0,Eb0,Erho0)),
         "GE07 other homogeneous Euler terms not zero")
    need(zero(EL1-2*D*(sp.diff(dT,t)-dn)/a),
         "GE07 longitudinal Euler first-order mismatch")
    need(zero(Eb1+2*D*sp.diff(dT,x)),
         "GE07 shift Euler first-order mismatch")
    W1=EN0*sp.diff(dn,x)-sp.diff(a*EL1,x)-sp.diff(Eb1,t)
    need(zero(W1),"GE07 first-order background-aware Ward failed")
    wrong=-sp.diff(a*EL1,x)-sp.diff(Eb1,t)
    need(zero(wrong-2*D*sp.diff(dn,x)) and not zero(wrong),
         "negative control: dropped dust background EN00 not detected")
    need(zero(e["partial_map"]["T_t"].subs(sub,simultaneous=True)
              .subs(eps,0)-2*D),"GE07 conserved dust time current mismatch")
    return {"offshell_GE07_Euler_Ward_exact":True,
            "GE07_EN00_is_minus_2D":True,
            "GE07_linear_EL1_Eb1_exact":True,
            "GE07_first_order_Ward_including_EN00_exact":True,
            "dropping_EN00_negative_control_nonzero":True}

def grav_lambda_lapse():
    g=frozen_assignments(
       "ge06/analytic_aest_directional_source_generator.py",
       ("N","L","R","b","u","phi"),"lag")
    a,H,Q,rl,C,n=sp.symbols("a H Q rhoLambda C n",positive=True)
    sub={g["N"]:n,g["L"]:a,g["R"]:a,g["b"]:0,g["u"]:0,
         g["Lt"]:a*H,g["Lx"]:0,g["Rt"]:a*H,
         g["Rx"]:0,g["bx"]:0,g["ut"]:0,g["ux"]:0,
         g["pt"]:Q,g["px"]:0,g["Nx"]:0}
    hom=sp.simplify(g["lag"].subs(sub,simultaneous=True))
    q=sp.symbols("q")
    K=lambda v:2*g["K2"]*g["Z0"]**2*(
         sp.exp(((v-g["Q0"])/g["Z0"])**2)-1)
    k=K(Q); kq=sp.diff(K(q),q).subs(q,Q)
    need(zero(hom-(-6*a**3*H**2/n+2*n*a**3*K(Q/n))),
         "GE06 homogeneous action mismatch")
    r11=(ROOT/"ge19/repair11_lambda_inclusive_reduced_h1_reclosure.py").read_text()
    need("L_lambda = -6 rho_lambda N L R^2" in r11,
         "Repair11 Lambda source action changed")
    EN=sp.simplify(sp.diff(hom-6*rl*n*a**3,n).subs(n,1))
    expected=6*a**3*H**2+2*a**3*(k-Q*kq)-6*rl*a**3
    need(zero(EN-expected),"GE06+Lambda EN background mismatch")
    r13=(ROOT/"ge19/repair13_self_consistent_reduced_background_h1_reclosure.py").read_text()
    need(all(t in r13 for t in (
         "rho_aest=(q*kq-kval)/3.0",
         "rho_d=r7.C_VALUES[tag]/a**3",
         "H2=rho_aest+rho_d+rho_l")),
         "original Repair13 Friedmann source changed")
    H2=(Q*kq-k)/3+C/a**3+rl
    need(zero(EN.subs(H**2,H2)-6*C),"gravity+Lambda EN00 != +6C")
    r7=(ROOT/"ge19/repair07_window_retarded_reduced_h3_z20_particular.py").read_text()
    need('rhob=3.0*C_VALUES[tag]/aa**3' in r7,
         "GE19 dust action density factor changed")
    need('shift_m=p7["b_f"]' in r7,
         "original GE07 shift row binding changed")
    d1=(ROOT/"ge19/h4f3d1_frozen_canonical_operator_ward.py").read_text()
    need('Eb=products[:,10]+products[:,11]' in d1 and
         'EL_non=(iso+2*aniso)/3' in d1,
         "original GE19 Cmat total row projection changed")
    # D=a^3*rho_action=3C in Repair07 raw GE07 units.
    D=sp.symbols("D")
    need(zero((EN.subs(H**2,H2)-2*D).subs(D,3*C)),
         "GE06+Lambda/GE07 background lapse does not cancel")
    return {"GE06_original_homogeneous_action_exact":True,
            "Repair11_and_Repair13_original_actions_bound":True,
            "GE06_plus_Lambda_EN00_is_plus_6C":True,
            "GE07_EN00_is_minus_6C":True,
            "total_background_EN00_cancels_exactly":True,
            "GE19_Cmat_shift_and_L_projection_source_bound":True}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--json-out",type=Path)
    args=ap.parse_args()
    locks={}
    for path,want in PINS.items():
        got=subprocess.check_output(["git","rev-parse","HEAD:"+path],
                                    cwd=ROOT,text=True).strip()
        need(got==want,"source hash mismatch "+path)
        locks[path]={"expected":want,"observed":got,"exact":True}
    dust=exact_dust()
    gravity=grav_lambda_lapse()
    result={
       "classification":
         "GE19_LINEAR_GE06_LAMBDA_GE07_LAPSE_BACKGROUND_EXACT_PASS_TOTAL_CMAT_OPEN",
       "source_blobs":locks,"GE07_checks":dust,"GE06_Lambda_checks":gravity,
       "physical_dictionary":"D=a^3*rho_dust_action=3*C_VALUES[tag]",
       "claim_boundary":"Exact source-bound background lapse cancellation and GE07 sector first-order Euler Ward. Does not establish the full arbitrary-jet GE06+GE07+Lambda canonical Cmat syzygy, FD4/FD8 budget, actual H4 Ward, Z21 or lensing.",
       "complete_canonical_Cmat_Ward_certified":False,
       "full_H4_Ward_certified":False,
       "Z21_certified":False,"lensing_licensed":False,
       "original_1e_minus6_gate_changed":False,
    }
    if args.json_out:
        need(not args.json_out.exists(),"output exists: no overwrite")
        args.json_out.parent.mkdir(parents=True,exist_ok=True)
        args.json_out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print("GE19_EXACT_GE07_OFFSHELL_AND_LINEAR_WARD_PASS")
    print("GE19_GE06_PLUS_LAMBDA_EN00_PLUS_6C_PASS")
    print("GE19_GE07_EN00_MINUS_6C_PASS")
    print("GE19_TOTAL_BACKGROUND_LAPSE_CANCELLATION_PASS")
    print("FULL_CMAT_WARD_OPEN Z21_CERTIFIED=false LENSING_LICENSED=false")

if __name__=="__main__":
    main()
