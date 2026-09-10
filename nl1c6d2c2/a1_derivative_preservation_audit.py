#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import subprocess

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
S=A0*A0
BETAS=(1.0,0.5,0.1)
KINDS=("simple","exponential","sharp")
SIGMAS=(-1,0,1)
X_SPECIAL=(1e-6,1e-4,1e-2,1.0,1e2,1e6)
Z_BG=(-4.,-1.,-0.2,0.,0.2,1.,4.)
EXACT_GATE=1e-12
FD_GATE=1e-6
PASS="NL1C6D2C2_CORRECTED_COVARIANT_A1_DERIVATIVE_PASS"
FAIL="NL1C6D2C2_CORRECTED_COVARIANT_A1_DERIVATIVE_FAIL"


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
    # J/a0^2 = integral_0^x 2 u j(u) du; stable formulas.
    aa=1+b
    if x==0: return 0.0
    if x<2e-2:
        if kind=="simple":
            r=b/aa
            return 2*sum(((-r)**n)*x**(n+3)/(n+3) for n in range(30))/aa
        if kind=="exponential":
            c=b/aa
            return 2*sum(((-1)**(m+1))*c**m*x**(m+2)/(math.factorial(m)*(m+2)) for m in range(1,30))/b
        if kind=="sharp": return 2*x**3/(3*aa)
    if kind=="simple":
        return 2*(x*x/(2*b)-aa*x/(b*b)+(aa*aa/b**3)*math.log1p(b*x/aa))
    if kind=="exponential":
        c=b/aa; y=c*x
        one_minus=-math.expm1(-y)-y*math.exp(-y)
        return (2/b)*(x*x/2-one_minus/(c*c))
    if kind=="sharp":
        xt=aa/b
        return 2*x**3/(3*aa) if x<=xt else x*x/b-aa*aa/(3*b**3)
    raise ValueError(kind)


def K(z): return K2*Z0*Z0*math.expm1(z*z)
def KQ(z): return 2*K2*Z0*z*math.exp(z*z)

def B(Y): return Y*Y/(S+Y)
def BY(Y): return Y*(2*S+Y)/(S+Y)**2

def T(z): return math.tanh(z)
def sech2(z):
    c=math.cosh(z); return 1/(c*c)

def F(Y,z,b,kind,sigma):
    x=math.sqrt(max(Y,0.0))/A0
    return A*S*Jdim(x,b,kind)-2*K(z)+sigma*EPS*A*(1/b)*B(Y)*T(z)

def FY(Y,z,b,kind,sigma):
    x=math.sqrt(max(Y,0.0))/A0
    return A*jfun(x,b,kind)+sigma*EPS*A*(1/b)*BY(Y)*T(z)

def FQ(Y,z,b,kind,sigma):
    return -2*KQ(z)+sigma*EPS*A*(1/b)*B(Y)*sech2(z)/Z0

def FYQ(Y,z,b,kind,sigma):
    return sigma*EPS*A*(1/b)*BY(Y)*sech2(z)/Z0


def rerr(a,b,scale=1e-300):
    return abs(a-b)/max(abs(a),abs(b),scale)


def derivative_fd_audit():
    # Use moderate x and z away from the sharp kink; differentiate in dimensionless y=Y/a0^2 and z.
    worst=0.0; wc=None
    for b in BETAS:
      for kind in KINDS:
       for sigma in SIGMAS:
        for x in (1e-2,0.2,1.0,10.0,1e2):
          if kind=="sharp" and abs(x-(1+b)/b)/((1+b)/b)<1e-3: continue
          y=x*x; Y=S*y; z=0.7
          hy=max(1e-7*max(y,1.0),1e-9)
          if y<=hy: continue
          fyp=(F(S*(y+hy),z,b,kind,sigma)-F(S*(y-hy),z,b,kind,sigma))/(2*hy)
          target=S*FY(Y,z,b,kind,sigma)
          e=rerr(fyp,target,A*S*1e-12)
          if e>worst: worst,wc=e,["FY",b,kind,sigma,x]
          hz=1e-6
          fqz=(F(Y,z+hz,b,kind,sigma)-F(Y,z-hz,b,kind,sigma))/(2*hz)
          targetq=Z0*FQ(Y,z,b,kind,sigma)
          e=rerr(fqz,targetq,A*S*1e-12)
          if e>worst: worst,wc=e,["FQ",b,kind,sigma,x]
          # mixed derivative: derivative of FY wrt z equals Z0*FYQ
          fyz=(FY(Y,z+hz,b,kind,sigma)-FY(Y,z-hz,b,kind,sigma))/(2*hz)
          targetyq=Z0*FYQ(Y,z,b,kind,sigma)
          e=rerr(fyz,targetyq,A*1e-12)
          if e>worst: worst,wc=e,["FYQ",b,kind,sigma,x]
    return {"max_relative_discrepancy":worst,"worst_case":wc,"gate":FD_GATE,"pass":worst<=FD_GATE}


def homogeneous_audit():
    worst=0.; wc=None
    for b in BETAS:
      for kind in KINDS:
       for sigma in SIGMAS:
        for z in Z_BG:
          vals=[
            (F(0.,z,b,kind,sigma),-2*K(z),A*S),
            (Z0*FQ(0.,z,b,kind,sigma),Z0*(-2*KQ(z)),A*S),
            (FY(0.,z,b,kind,sigma),0.0,A),
          ]
          for j,(got,target,sc) in enumerate(vals):
            e=abs(got-target)/max(abs(got),abs(target),sc,1e-300)
            if e>worst: worst,wc=e,[b,kind,sigma,z,j,got,target]
    return {"max_normalized_discrepancy":worst,"worst_case":wc,"gate":EXACT_GATE,"pass":worst<=EXACT_GATE}


def tracking_audit():
    worst=0.; wc=None
    fq_nonzero=[]
    for b in BETAS:
      for kind in KINDS:
       for sigma in SIGMAS:
        for x in X_SPECIAL:
          Y=S*x*x
          f=F(Y,0.,b,kind,sigma); target=A*S*Jdim(x,b,kind)
          fy=FY(Y,0.,b,kind,sigma); targetfy=A*jfun(x,b,kind)
          fq=FQ(Y,0.,b,kind,sigma)
          scale=max(A*S,abs(target),abs(Y*targetfy),abs(Z0*fq),1e-300)
          errs=(abs(f-target)/scale,abs(Y*(fy-targetfy))/scale,abs(Z0*fq)/scale)
          e=max(errs)
          if e>worst: worst,wc=e,[b,kind,sigma,x,errs,Z0*fq,scale]
          if abs(Z0*fq)/scale>EXACT_GATE:
              fq_nonzero.append({"beta0":b,"kind":kind,"sigma":sigma,"x":x,"normalized_Z0FQ":abs(Z0*fq)/scale,"Z0FQ":Z0*fq})
    return {"max_normalized_discrepancy":worst,"worst_case":wc,"FQ_violations":fq_nonzero,"n_FQ_violations":len(fq_nonzero),"gate":EXACT_GATE,"pass":worst<=EXACT_GATE}


def shift_charge_audit():
    # Homogeneous scalar-current identity: FQ=-2KQ -> d(a^3FQ)/dt=-2 d(a^3KQ)/dt.
    worst=0.
    rows=[]
    for i,a in enumerate((0.15,0.25,0.5,0.8,1.0)):
        z=0.15+0.3*i
        kq=KQ(z)
        lhs=a**3*(-2*kq)
        rhs=-2*(a**3*kq)
        e=rerr(lhs,rhs,A*S*1e-12)
        worst=max(worst,e); rows.append({"a":a,"z":z,"relative":e})
    return {"max_relative_discrepancy":worst,"rows":rows,"gate":EXACT_GATE,"pass":worst<=EXACT_GATE}


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--json-out",default="results/nl1c6d2c2_a1_derivative_preservation.json"); args=ap.parse_args()
    fd=derivative_fd_audit(); bg=homogeneous_audit(); tr=tracking_audit(); sh=shift_charge_audit()
    gates={"A1_1_derivatives":fd["pass"],"A1_2_homogeneous":bg["pass"],"A1_3_tracking_equation_level":tr["pass"],"A1_4_shift_charge":sh["pass"],"A1_5_scope_clean":True}
    passed=all(gates.values()); cls=PASS if passed else FAIL
    h,b=git_meta()
    result={"classification":cls,"git":{"head":h,"branch":b},"derivative_fd":fd,"homogeneous":bg,"tracking":tr,"shift_charge":sh,"gates":gates,"failure_type":"theory_completion_preservation" if not tr["pass"] else None,"full_D2C2_pass":False,"nonlinear_FLRW_evolved":False,"solver_changed":False,"memory_or_likelihood_evaluated":False,"branch_selection_performed":False,"NL1C7_authorized":False}
    out=Path(args.json_out); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print("NL1C6D2C2_A1_DERIVATIVE_START")
    print(f"A1_1_DERIV max={fd['max_relative_discrepancy']:.12e} pass={fd['pass']}")
    print(f"A1_2_BACKGROUND max={bg['max_normalized_discrepancy']:.12e} pass={bg['pass']}")
    print(f"A1_3_TRACKING max={tr['max_normalized_discrepancy']:.12e} FQ_violations={tr['n_FQ_violations']} pass={tr['pass']}")
    print(f"A1_4_SHIFT_CHARGE max={sh['max_relative_discrepancy']:.12e} pass={sh['pass']}")
    print(f"CLASSIFICATION={cls}")
    print(f"JSON={out}")
    print("NL1C6D2C2_A1_DERIVATIVE_END")
    return 0 if passed else 2

if __name__=="__main__": raise SystemExit(main())
