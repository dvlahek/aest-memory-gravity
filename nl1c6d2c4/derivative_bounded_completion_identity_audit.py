#!/usr/bin/env python3
from __future__ import annotations

import argparse, functools, json, math, subprocess
from pathlib import Path

import numpy as np
from scipy.integrate import quad

KB=0.0665
A=2.0-KB
K2=9500.0
Q0=1.0e-4
Z0=1.0e-17
EPS=0.25
A0_SI=1.2e-10
C_SI=299792458.0
MPC_M=3.085677581491367e22
A0=A0_SI*MPC_M/(C_SI*C_SI)
Y0=A0*A0
BETAS=(1.0,0.5,0.1)
KINDS=("simple","exponential","sharp")
SIGMAS=(-1,0,1)
ZGRID=(-8.,-2.,-0.5,0.,0.5,2.,8.)
XTRACK=(1e-6,1e-4,1e-2,1.,1e2,1e6)
XDEEP=(1e-2,5e-3,2.5e-3,1.25e-3)
XBOUND=(1e-4,1e-2,1.,1e2,1e3,1e4,1e6)
XHIGH=(1e2,1e3,1e4,1e6)
EXACT_GATE=1e-12
DEEP_GATE=5e-4
FD_GATE=2e-6
ASYM_GATE=2e-5
MIX_ASYM_GATE=1e-10
PASS="NL1C6D2C4_DERIVATIVE_BOUNDED_COMPLETION_IDENTITY_PASS"
FAIL="NL1C6D2C4_DERIVATIVE_BOUNDED_COMPLETION_IDENTITY_FAIL"


def git_meta():
    try:
        h=subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip()
        b=subprocess.check_output(["git","rev-parse","--abbrev-ref","HEAD"],text=True).strip()
    except Exception:
        h,b="unknown","unknown"
    return h,b


def jfun(x,b,kind):
    aa=1+b
    if kind=="simple": return x/(aa+b*x)
    if kind=="exponential": return -math.expm1(-b*x/aa)/b
    if kind=="sharp": return min(x/aa,1/b)
    raise ValueError(kind)


def Jdim(x,b,kind):
    aa=1+b
    if x==0: return 0.0
    if x<2e-2:
        if kind=="simple":
            r=b/aa
            return 2*sum(((-r)**n)*x**(n+3)/(n+3) for n in range(30))/aa
        if kind=="exponential":
            c=b/aa
            return 2*sum(((-1)**(m+1))*c**m*x**(m+2)/(math.factorial(m)*(m+2)) for m in range(1,30))/b
        return 2*x**3/(3*aa)
    if kind=="simple":
        return 2*(x*x/(2*b)-aa*x/(b*b)+(aa*aa/b**3)*math.log1p(b*x/aa))
    if kind=="exponential":
        c=b/aa; y=c*x
        one_minus=-math.expm1(-y)-y*math.exp(-y)
        return (2/b)*(x*x/2-one_minus/(c*c))
    xt=aa/b
    return 2*x**3/(3*aa) if x<=xt else x*x/b-aa*aa/(3*b**3)


def Sx(x): return x*x/(1+x*x)


@functools.lru_cache(maxsize=None)
def Hdim_cached(x,b,kind):
    if x==0: return 0.0
    f=lambda u: 2*u*jfun(u,b,kind)*Sx(u)
    xt=(1+b)/b
    pts=[xt] if kind=="sharp" and 0<xt<x else None
    val,_=quad(f,0,x,epsabs=1e-24,epsrel=2e-12,limit=300,points=pts)
    return float(val)


def Hdim(x,b,kind): return Hdim_cached(float(x),float(b),str(kind))
def K(z): return K2*Z0*Z0*math.expm1(z*z)
def KQ(z): return 2*K2*Z0*z*math.exp(z*z)
def G(z):
    t=math.tanh(z); return t*t
def Gz(z):
    t=math.tanh(z); c=math.cosh(z); return 2*t/(c*c)


def F(Y,z,b,kind,sigma):
    x=math.sqrt(max(Y,0.0))/A0
    return A*Y0*Jdim(x,b,kind)-2*K(z)+sigma*EPS*A*Y0*Hdim(x,b,kind)*G(z)

def FY(Y,z,b,kind,sigma):
    x=math.sqrt(max(Y,0.0))/A0
    j=jfun(x,b,kind)
    return A*j*(1+sigma*EPS*Sx(x)*G(z))
def FQ(Y,z,b,kind,sigma):
    x=math.sqrt(max(Y,0.0))/A0
    return -2*KQ(z)+sigma*EPS*A*Y0*Hdim(x,b,kind)*Gz(z)/Z0

def FYQ(Y,z,b,kind,sigma):
    x=math.sqrt(max(Y,0.0))/A0
    return sigma*EPS*A*jfun(x,b,kind)*Sx(x)*Gz(z)/Z0


def norm_err(got,target,scale):
    return abs(got-target)/max(abs(got),abs(target),scale,1e-300)


def homogeneous():
    worst=0.; wc=None
    for b in BETAS:
      for kind in KINDS:
       for sigma in SIGMAS:
        for z in ZGRID:
          vals=((F(0,z,b,kind,sigma),-2*K(z),A*Y0),
                (Z0*FQ(0,z,b,kind,sigma),Z0*(-2*KQ(z)),A*Y0),
                (FY(0,z,b,kind,sigma),0.0,A))
          for i,(got,target,sc) in enumerate(vals):
            e=norm_err(got,target,sc)
            if e>worst: worst,wc=e,[b,kind,sigma,z,i,got,target]
    return {"max_normalized_discrepancy":worst,"worst_case":wc,"gate":EXACT_GATE,"pass":worst<=EXACT_GATE}


def tracking():
    worst=0.; wc=None
    for b in BETAS:
      for kind in KINDS:
       for sigma in SIGMAS:
        for x in XTRACK:
          Y=Y0*x*x; tf=A*Y0*Jdim(x,b,kind); ty=A*jfun(x,b,kind)
          vals=((F(Y,0,b,kind,sigma),tf,max(A*Y0,abs(tf))),
                (Y*FY(Y,0,b,kind,sigma),Y*ty,max(A*Y0,abs(Y*ty))),
                (Z0*FQ(Y,0,b,kind,sigma),0.0,max(A*Y0,abs(tf),abs(Y*ty))),
                (Z0*FYQ(Y,0,b,kind,sigma),0.0,A))
          for i,(got,target,sc) in enumerate(vals):
            e=norm_err(got,target,sc)
            if e>worst: worst,wc=e,[b,kind,sigma,x,i,got,target]
    return {"max_normalized_discrepancy":worst,"worst_case":wc,"gate":EXACT_GATE,"pass":worst<=EXACT_GATE}


def deep_mond():
    rows=[]; ok=True; maxfinal=0.
    gz=G(1.0)
    for b in BETAS:
      for kind in KINDS:
       for sigma in (-1,1):
        ratios=[]
        for x in XDEEP:
            base=Jdim(x,b,kind)
            mix=abs(sigma*EPS*Hdim(x,b,kind)*gz)
            ratios.append(mix/max(abs(base),1e-300))
        mono=all(ratios[i+1]<ratios[i] for i in range(len(ratios)-1))
        final=ratios[-1]; maxfinal=max(maxfinal,final)
        rowok=mono and final<=DEEP_GATE; ok=ok and rowok
        rows.append({"beta0":b,"kind":kind,"sigma":sigma,"ratios":ratios,"monotone":mono,"final":final,"pass":rowok})
    return {"rows":rows,"max_final_ratio":maxfinal,"final_gate":DEEP_GATE,"pass":ok}


def constitutive_bound():
    mn=float("inf"); mx=-float("inf"); ok=True; wc=None
    for b in BETAS:
      for kind in KINDS:
       for sigma in SIGMAS:
        for x in XBOUND:
         Y=Y0*x*x; j=jfun(x,b,kind)
         for z in ZGRID:
            ratio=FY(Y,z,b,kind,sigma)/(A*j)
            if ratio<mn: mn=ratio; wc=["min",b,kind,sigma,x,z,ratio]
            if ratio>mx: mx=ratio; wc=["max",b,kind,sigma,x,z,ratio]
            ok=ok and ratio>=0.75-1e-12 and ratio<=1.25+1e-12
    return {"min_ratio":mn,"max_ratio":mx,"range":[0.75,1.25],"last_extreme_case":wc,"pass":ok}


def high_gradient():
    rows=[]; ok=True; worst_final=0.; worst_mix=0.
    for b in BETAS:
      lam=1/b
      for kind in KINDS:
        vals=[jfun(x,b,kind)/lam for x in XHIGH]
        positive=all(v>0 for v in vals)
        mono=all(vals[i+1]>=vals[i]-1e-15 for i in range(len(vals)-1))
        final=abs(vals[-1]-1.0); worst_final=max(worst_final,final)
        rowok=positive and mono and final<=ASYM_GATE; ok=ok and rowok
        rows.append({"beta0":b,"kind":kind,"j_over_lambda":vals,"positive":positive,"monotone":mono,"final_abs_error":final,"pass":rowok})
        x=1e6; Y=Y0*x*x
        for sigma in SIGMAS:
          for z in ZGRID:
            got=FY(Y,z,b,kind,sigma)/(A*jfun(x,b,kind))
            target=1+sigma*EPS*G(z)
            e=abs(got-target); worst_mix=max(worst_mix,e); ok=ok and e<=MIX_ASYM_GATE
    return {"rows":rows,"worst_base_final_abs_error":worst_final,"base_final_gate":ASYM_GATE,"worst_mixed_modulation_error":worst_mix,"mixed_gate":MIX_ASYM_GATE,"pass":ok}


def finite_difference():
    worst=0.; wc=None
    for b in BETAS:
      for kind in KINDS:
       for sigma in SIGMAS:
        for x in (1e-2,0.2,1.0,10.0,1e2):
          xt=(1+b)/b
          if kind=="sharp" and abs(x-xt)/xt<1e-3: continue
          y=x*x; Y=Y0*y; z=0.7
          hy=max(1e-7*max(y,1.0),1e-9)
          if y<=hy: continue
          fy_num=(F(Y0*(y+hy),z,b,kind,sigma)-F(Y0*(y-hy),z,b,kind,sigma))/(2*hy)
          e=norm_err(fy_num,Y0*FY(Y,z,b,kind,sigma),A*Y0*1e-12)
          if e>worst: worst,wc=e,["FY",b,kind,sigma,x]
          hz=1e-6
          fq_num=(F(Y,z+hz,b,kind,sigma)-F(Y,z-hz,b,kind,sigma))/(2*hz)
          e=norm_err(fq_num,Z0*FQ(Y,z,b,kind,sigma),A*Y0*1e-12)
          if e>worst: worst,wc=e,["FQ",b,kind,sigma,x]
          fyq_num=(FY(Y,z+hz,b,kind,sigma)-FY(Y,z-hz,b,kind,sigma))/(2*hz)
          e=norm_err(fyq_num,Z0*FYQ(Y,z,b,kind,sigma),A*1e-12)
          if e>worst: worst,wc=e,["FYQ",b,kind,sigma,x]
    return {"max_relative_discrepancy":worst,"worst_case":wc,"gate":FD_GATE,"pass":worst<=FD_GATE}


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--json-out",default="results/nl1c6d2c4_derivative_bounded_completion_identity.json"); args=ap.parse_args()
    h=homogeneous(); t=tracking(); d=deep_mond(); cb=constitutive_bound(); hg=high_gradient(); fd=finite_difference()
    gates={"C4_1_homogeneous":h["pass"],"C4_2_tracking_EL_slice":t["pass"],"C4_3_deep_MOND":d["pass"],"C4_4_local_constitutive_bound":cb["pass"],"C4_5_high_gradient_recovery":hg["pass"],"C4_6_derivative_control":fd["pass"],"C4_7_scope_clean":True}
    passed=all(gates.values()); cls=PASS if passed else FAIL; head,branch=git_meta()
    result={"classification":cls,"git":{"head":head,"branch":branch},"homogeneous":h,"tracking":t,"deep_MOND":d,"constitutive_bound":cb,"high_gradient":hg,"finite_difference":fd,"gates":gates,"nonlinear_FLRW_evolved":False,"solver_changed":False,"memory_or_likelihood_evaluated":False,"branch_selection_performed":False,"D2C4_action_derivation_licensed":passed,"NL1C7_authorized":False}
    out=Path(args.json_out); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print("NL1C6D2C4_DERIVATIVE_BOUNDED_IDENTITY_START")
    print(f"C4_1_BACKGROUND max={h['max_normalized_discrepancy']:.12e} pass={h['pass']}")
    print(f"C4_2_TRACKING max={t['max_normalized_discrepancy']:.12e} pass={t['pass']}")
    print(f"C4_3_DEEP final_max={d['max_final_ratio']:.12e} pass={d['pass']}")
    print(f"C4_4_BOUND min={cb['min_ratio']:.12e} max={cb['max_ratio']:.12e} pass={cb['pass']}")
    print(f"C4_5_HIGH base_final={hg['worst_base_final_abs_error']:.12e} mixed={hg['worst_mixed_modulation_error']:.12e} pass={hg['pass']}")
    print(f"C4_6_DERIV max={fd['max_relative_discrepancy']:.12e} pass={fd['pass']}")
    print(f"CLASSIFICATION={cls}")
    print(f"D2C4_ACTION_DERIVATION_LICENSED={passed}")
    print(f"JSON={out}")
    print("NL1C6D2C4_DERIVATIVE_BOUNDED_IDENTITY_END")
    return 0 if passed else 2

if __name__=="__main__": raise SystemExit(main())
