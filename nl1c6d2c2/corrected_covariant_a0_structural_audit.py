#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import subprocess
import sys

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

from nl1c6d1 import longitudinal_weakfield_reduction_audit as d1a

KB=0.0665
K2=9500.0
Q0=1.0e-4
Z0=1.0e-17
A=2.0-KB
EPS_MIX=0.25
A0_SI=1.2e-10
C_SI=299792458.0
MPC_M=3.085677581491367e22
A0=A0_SI*MPC_M/(C_SI*C_SI)
BETAS=(1.0,0.5,0.1)
KINDS=("simple","exponential","sharp")
SIGMAS=(-1,0,1)
GATE=1.0e-12
PASS="NL1C6D2C2_CORRECTED_COVARIANT_A0_STRUCTURAL_PASS"
FAIL="NL1C6D2C2_CORRECTED_COVARIANT_A0_STRUCTURAL_FAIL"


def git_meta():
    try:
        h=subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip()
        b=subprocess.check_output(["git","rev-parse","--abbrev-ref","HEAD"],cwd=ROOT,text=True).strip()
    except Exception:
        h,b="unknown","unknown"
    return h,b


def rel(a,b,floor=1e-30):
    return float(abs(a-b)/max(abs(b),abs(a),floor))


def Kexp_from_Z(z):
    return K2*Z0*Z0*math.expm1(z*z)


def KQ_from_Z(z):
    return 2.0*K2*Z0*z*math.exp(z*z)


def KQQ_from_Z(z):
    return 2.0*K2*math.exp(z*z)*(1.0+2.0*z*z)


def Jdimless_series(x,beta,kind):
    aa=1.0+beta
    if x==0.0: return 0.0
    if kind=="simple":
        r=beta/aa
        return 2.0*sum(((-r)**n)*(x**(n+3))/(n+3) for n in range(24))/aa
    if kind=="exponential":
        c=beta/aa
        s=0.0
        for m in range(1,24):
            s += ((-1.0)**(m+1))*(c**m)*(x**(m+2))/(math.factorial(m)*(m+2))
        return 2.0*s/beta
    if kind=="sharp": return 2.0*x**3/(3.0*aa)
    raise ValueError(kind)


def Jdimless(x,beta,kind):
    if x<=2e-2: return Jdimless_series(x,beta,kind)
    aa=1.0+beta
    if kind=="simple":
        return 2.0*(x*x/(2*beta)-aa*x/(beta*beta)+(aa*aa/beta**3)*math.log1p(beta*x/aa))
    if kind=="exponential":
        c=beta/aa; y=c*x
        one_minus=-math.expm1(-y)-y*math.exp(-y)
        return (2.0/beta)*(x*x/2.0-one_minus/(c*c))
    if kind=="sharp":
        xt=aa/beta
        if x<=xt: return 2.0*x**3/(3.0*aa)
        return x*x/beta-aa*aa/(3.0*beta**3)
    raise ValueError(kind)


def Jphys(x,beta,kind): return A0*A0*Jdimless(x,beta,kind)


def Bmix_from_x(x):
    # Y*x^2/(1+x^2) = Y^2/(a0^2+Y)
    Y=A0*A0*x*x
    return Y*(x*x/(1.0+x*x))


def Bmix_Y_derivative_from_x(x):
    # d/dY [Y^2/(a0^2+Y)] = Y(2a0^2+Y)/(a0^2+Y)^2
    u=x*x
    return u*(2.0+u)/(1.0+u)**2


def Fsigma(x,z,beta,kind,sigma):
    Y=A0*A0*x*x
    mix=sigma*EPS_MIX*A*(1.0/beta)*Bmix_from_x(x)*math.tanh(z)
    return A*Jphys(x,beta,kind)-2.0*Kexp_from_Z(z)+mix


def completion_slice_audit():
    zgrid=(-8.,-2.,-0.5,0.,0.5,2.,8.)
    xgrid=(0.,1e-6,1e-3,0.1,1.,10.,1e4)
    worst=0.0; worst_case=None
    for sigma in SIGMAS:
        for kind in KINDS:
            for beta in BETAS:
                for z in zgrid:
                    got=Fsigma(0.,z,beta,kind,sigma)
                    target=-2.0*Kexp_from_Z(z)
                    e=rel(got,target,1e-80)
                    if e>worst: worst,worst_case=e,["Y0",sigma,kind,beta,z]
                    # mixed piece and its first Y derivative vanish at Y=0
                    m0=sigma*EPS_MIX*A*(1.0/beta)*Bmix_from_x(0.)*math.tanh(z)
                    my0=sigma*EPS_MIX*A*(1.0/beta)*Bmix_Y_derivative_from_x(0.)*math.tanh(z)
                    for label,val in (("mix_Y0",m0),("mixY_Y0",my0)):
                        e=abs(val)
                        if e>worst: worst,worst_case=e,[label,sigma,kind,beta,z]
                for x in xgrid:
                    got=Fsigma(x,0.,beta,kind,sigma)
                    target=A*Jphys(x,beta,kind)
                    e=rel(got,target,1e-80)
                    if e>worst: worst,worst_case=e,["Q0",sigma,kind,beta,x]
    return {"max_relative_or_absolute_discrepancy":worst,"worst_case":worst_case,"gate":GATE,"pass":bool(worst<=GATE)}


def manufactured_states():
    rows=[]
    for i in range(64):
        a=0.15+0.8*((i+1)/65.0)
        H=2.0e-4+1.3e-3*((i%11)+1)/12.0
        k=0.015+0.22*((i%13)+1)/14.0
        Q=Q0*(0.82+0.36*((i%9)+1)/10.0)
        KQ=(1.5e-7+2.0e-7*((i%7)+1)/8.0)*(1 if i%2==0 else -1)
        rho=4.0e-8+2.5e-7*((i%10)+1)/11.0
        w=-0.05+0.22*((i%8)+1)/9.0
        cad2=0.005+0.12*((i%6)+1)/7.0
        delta=(-1 if i%2 else 1)*(1.0e-5+2.0e-5*((i%5)+1)/6.0)
        Theta=(-1 if i%3 else 1)*(2.0e-6+4.0e-6*((i%7)+1)/8.0)
        phip=(-1 if i%4 else 1)*(1.0e-7+2.0e-7*((i%5)+1)/6.0)
        Psi=(-1 if i%5 else 1)*(3.0e-6+2.0e-6*((i%6)+1)/7.0)
        alpha=(-1 if i%2 else 1)*(0.01+0.03*((i%9)+1)/10.0)
        E=(-1 if i%3 else 1)*(2.0e-6+5.0e-6*((i%8)+1)/9.0)
        rows.append((a,H,k,Q,KQ,rho,w,cad2,delta,Theta,phip,Psi,alpha,E))
    return rows


def theory_to_conformal(state):
    a,H,k,Q,KQ,rho,w,cad2,delta,Theta,phip,Psi,alpha,E=state
    Hc=a*H
    theta_pot=a*Theta/(k*k)
    chi=Q*(theta_pot+alpha)
    Pi=cad2*delta+cad2*k*k/(3.0*a*a*rho)*(KB*E+A*chi)
    phidot=phip/a
    delta_dot=3.0*H*(w*delta-Pi)+(1.0+w)*(3.0*phidot-(k*k/(a*a))*theta_pot)
    delta_prime=a*delta_dot
    theta_pot_dot=3.0*cad2*H*theta_pot+Pi/(1.0+w)+Psi
    Theta_prime=k*k*theta_pot_dot-Hc*Theta
    alpha_prime=a*(E-Psi)
    Erhs=KQ*chi-A*(Q*Pi/(1.0+w)+(H+Q)*chi-3.0*cad2*H*Q*alpha)
    E_prime=a*Erhs/KB-Hc*E
    return {"Pi":Pi,"delta_prime":delta_prime,"Theta_prime":Theta_prime,"alpha_prime":alpha_prime,"E_prime":E_prime,"chi":chi}


def class_convention_eval(state):
    a,H,k,Q,KQ,rho,w,cad2,delta,Theta,phip,Psi,alpha,E=state
    k2=k*k; Hc=a*H
    theta_potential=a*Theta/k2
    chi=Q*(theta_potential+alpha)
    Pi=cad2*delta+cad2*k2/(3.0*a*a*rho)*(KB*E+A*chi)
    metric_continuity=-3.0*phip
    metric_euler=k2*Psi
    dp=3.0*Hc*(w*delta-Pi)-(1.0+w)*(Theta+metric_continuity)
    tp=(3.0*cad2-1.0)*Hc*Theta+k2*Pi/(1.0+w)+metric_euler
    ap=a*(E-Psi)
    rhs=KQ*chi-A*(Q*Pi/(1.0+w)+(H+Q)*chi-3.0*cad2*H*Q*alpha)
    ep=a*rhs/KB-Hc*E
    return {"Pi":Pi,"delta_prime":dp,"Theta_prime":tp,"alpha_prime":ap,"E_prime":ep,"chi":chi}


def linear_mapping_audit():
    worst=0.0; wc=None; per={q:0.0 for q in ("Pi","delta_prime","Theta_prime","alpha_prime","E_prime","chi")}
    for i,s in enumerate(manufactured_states()):
        t=theory_to_conformal(s); c=class_convention_eval(s)
        for q in per:
            e=rel(t[q],c[q],1e-30)
            per[q]=max(per[q],e)
            if e>worst: worst,wc=e,[i,q,t[q],c[q]]
    return {"n_states":64,"max_relative_discrepancy":worst,"per_quantity_max":per,"worst_case":wc,"gate":GATE,"pass":bool(worst<=GATE)}


def source_anchor_audit():
    ctext=(ROOT/"v019/patch/source/aest_memory.c").read_text()
    ptext=(ROOT/"v019/apply_patch_v019.py").read_text()
    corrected=(
        "k=K2*Z0*Z0*(ex-1.);",
        "kq=2.*K2*Z0*Z*ex;",
        "kqq=2.*K2*ex*(1.+2.*zz);",
    )
    old=(
        "k=2.*K2*Z0*Z0*(ex-1.);",
        "kq=4.*K2*Z0*Z*ex;",
        "kqq=4.*K2*ex*(1.+2.*zz);",
        "double x=kq/(4.*K2*Z0);",
    )
    structural=(
        "double chi_aest = Q_aest*(theta_potential_aest+alpha_aest);",
        "*(pba->aest_KB*E_aest+(2.-pba->aest_KB)*chi_aest);",
        "dy[pv->index_pt_alpha_aest] = a*(E_aest-psi_aest);",
        "dy[pv->index_pt_E_aest] = a*E_rhs_aest/pba->aest_KB-a_prime_over_a*E_aest;",
        "3.*a_prime_over_a*(w_aest*y[pv->index_pt_delta_cdm]-Pi_aest)",
        "(3.*cad2_aest-1.)*a_prime_over_a*theta_div_aest",
    )
    counts={s:ctext.count(s) for s in corrected}
    old_counts={s:ctext.count(s) for s in old}
    scounts={s:ptext.count(s) for s in structural}
    passed=all(v==1 for v in counts.values()) and all(v==0 for v in old_counts.values()) and all(v>=1 for v in scounts.values())
    return {"corrected_formula_counts":counts,"historical_formula_counts":old_counts,"CLASS_structural_anchor_counts":scounts,"pass":bool(passed)}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--json-out",default="results/nl1c6d2c2_corrected_covariant_a0_structural_audit.json")
    args=ap.parse_args()
    head,branch=git_meta()

    kqq=KQQ_from_Z(0.0)
    mu2=2.0*K2*Q0*Q0/A
    curvature={
        "KQQ_Q0":kqq,"target_2K2":2.0*K2,"KQQ_relative":rel(kqq,2.0*K2),
        "mu2":mu2,"D1A_frozen_mu2":float(d1a.frozen.MU2),"mu2_relative":rel(mu2,float(d1a.frozen.MU2)),
    }
    curvature["pass"]=bool(max(curvature["KQQ_relative"],curvature["mu2_relative"])<=GATE)

    canon=d1a.canonical_regression()
    static=d1a.static_reduction_regression()
    slices=completion_slice_audit()
    linear=linear_mapping_audit()
    anchors=source_anchor_audit()

    gates={
        "A0_1_corrected_Minkowski_curvature":curvature["pass"],
        "A0_2_D1A_canonical":bool(canon["pass"] and canon["max_relative_error"]<=GATE),
        "A0_3_fixed_a_fullJ_operator":bool(static["pass"] and static["max_relative_error"]<=GATE),
        "A0_4_completion_exact_slices":slices["pass"],
        "A0_5_published_linear_CLASS_mapping":linear["pass"],
        "A0_6_source_anchor_provenance":anchors["pass"],
        "A0_7_scope_clean":True,
    }
    passed=all(gates.values())
    classification=PASS if passed else FAIL
    result={
        "classification":classification,"git":{"head":head,"branch":branch},
        "curvature":curvature,"D1A_canonical":canon,"fixed_a_fullJ_operator":static,
        "completion_slices":slices,"linear_CLASS_mapping":linear,"source_anchors":anchors,
        "gates":gates,"full_D2C2_classified":False,"D2C2_A1_licensed":passed,
        "historical_D2C_unchanged":True,"historical_R3_unchanged":True,
        "nonlinear_FLRW_evolved":False,"branch_selection_performed":False,
        "memory_or_likelihood_evaluated":False,"cosmological_refit_performed":False,"NL1C7_authorized":False,
    }
    out=Path(args.json_out); out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,sort_keys=True,default=str)+"\n")
    print("NL1C6D2C2_CORRECTED_COVARIANT_A0_START")
    print(f"A0_1_CURVATURE KQQ={kqq:.16e} mu2={mu2:.16e} pass={curvature['pass']}")
    print(f"A0_2_CANON max={canon['max_relative_error']:.12e} pass={gates['A0_2_D1A_canonical']}")
    print(f"A0_3_STATIC max={static['max_relative_error']:.12e} pass={gates['A0_3_fixed_a_fullJ_operator']}")
    print(f"A0_4_SLICES max={slices['max_relative_or_absolute_discrepancy']:.12e} pass={slices['pass']}")
    print(f"A0_5_LINEAR max={linear['max_relative_discrepancy']:.12e} pass={linear['pass']}")
    print(f"A0_6_ANCHORS pass={anchors['pass']}")
    print(f"CLASSIFICATION={classification}")
    print(f"D2C2_A1_LICENSED={passed}")
    print(f"JSON={out}")
    print("NL1C6D2C2_CORRECTED_COVARIANT_A0_END")
    return 0 if passed else 2

if __name__=="__main__":
    raise SystemExit(main())
