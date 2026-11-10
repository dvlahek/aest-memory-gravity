#!/usr/bin/env python3
"""LW24: analytic reduced GE06 action -> CLASS density/pressure dictionary.

A lightweight exact SymPy check. Not the full 3+1 action/constraint map,
a physical eta observer, or an observed DES shear fit.
"""
from __future__ import annotations
import argparse,json,subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/"ge19/lw24_reduced_action_class_density_pressure_dictionary_predata_20261110.json"
PRE_BLOB="7c6ba7a0a0b85af6104d1b7e398c57edf0943f40"
ANCHORS={
 "ge06/analytic_aest_directional_source_generator.py":[
  "aest=N*L*R**2*(KB*E**2 + 2*C*E*Xinv - C*Xinv**2 + 2*Kfun)",
  "Qinv=ch*sigma+sh*px/L"],
 "v019/patch/source/aest_memory.c":[
  "rho8=q*kq-k;","*rho_class=rho8/3.;","*p_class=k/3.;",
  "*cad2=kq/(q*kqq);","kq=I0/(a*a*a);"],
 "v019/apply_patch_v019.py":[
  "Pi_aest = cad2_aest*y[ppw->pv->index_pt_delta_cdm]",
  "ppw->delta_p += rho_dark*Pi_aest;"],
 "ge05/memory_directional_source_generator.py":[
  "lag=N*L*R**2*sp.Rational(1,4)*(Aq**2-(om*q-sw*Xphi)**2)"]
}
def need(ok,tag):
 if not bool(ok):raise RuntimeError("GE19_LW24_"+tag)
def blob(p):
 return subprocess.check_output(["git","hash-object",str(p)],cwd=ROOT,text=True).strip()

def symbolic():
 import sympy as s
 N,L,R,b,u,pt,px,ut,ux,Nx,Lt,Lx,bx=s.symbols(
  "N L R b u pt px ut ux Nx Lt Lx bx",real=True)
 KB,C=s.symbols("KB C",real=True)
 a,ad,Q,eps,n,ell,rr,z,v,pdt,pdx,vdt,nx=s.symbols(
  "a ad Q eps n ell rr z v pdt pdx vdt nx",real=True)
 K=s.Function("K");ch=s.cosh(u);sh=s.sinh(u)
 sigma=(pt-b*px)/N
 Qinv=ch*sigma+sh*px/L
 X=sh*sigma+ch*px/L
 kL=(Lt-b*Lx-L*bx)/(N*L)
 E=ch*((ut-b*ux)/N+Nx/(N*L))+sh*(kL+ux/L)
 lag=N*L*R**2*(KB*E**2+2*C*E*X-C*X**2+2*K(Qinv))
 perturb={N:1+eps*n,L:a+eps*ell,R:a+eps*rr,b:eps*z,
  u:eps*v,pt:Q+eps*pdt,px:eps*pdx,ut:eps*vdt,ux:0,
  Nx:eps*nx,Lt:ad,Lx:0,bx:0}
 K0,KQ,KQQ=s.symbols("K0 KQ KQQ",real=True)
 repl={K(Q):K0,s.diff(K(Q),Q):KQ,s.diff(K(Q),Q,2):KQQ}
 def coeff(f,order=1):
  t=s.diff(lag,f).subs(perturb)
  return s.simplify(s.diff(t,eps,order).subs(eps,0).doit().xreplace(repl))
 N0,N1,Nx0,Nx1=coeff(N,0),coeff(N),coeff(Nx,0),coeff(Nx)
 L1,R1,b1,bx1=coeff(L),coeff(R),coeff(b),coeff(bx)
 Lt1,Lx1=coeff(Lt),coeff(Lx)
 dQ=pdt-Q*n
 X1=Q*v+pdx/a
 E1=vdt+nx/a+ad*v/a
 vol=ell+2*rr
 rho8=Q*KQ-K0;pc=K0/3;rhoc=rho8/3;ca=KQ/(Q*KQQ)
 k,EA,chi,phi,phidot,alpha,alphadot,Psi=s.symbols(
  "k EA chi phi phidot alpha alphadot Psi",real=True)
 I=s.I;H=ad/a
 newt={v:I*k*alpha/a,vdt:I*k*(alphadot-H*alpha)/a,
       nx:I*k*Psi,pdx:I*k*phi,n:Psi,pdt:phidot}
 densN=s.simplify((N1-2*a*a*(K0-Q*KQ)*vol).subs(newt))
 gradN=s.simplify(Nx1.subs(newt))
 dens=s.simplify(-(densN-I*k*gradN)/(6*a**3))
 ds=(phidot-Q*Psi)
 expected=(Q*KQQ*ds-k*k/a**2*(KB*(alphadot+Psi)+C*(phi+Q*alpha)))/3
 Pi=ca*(dens+k*k/(3*a*a)*
      (KB*(alphadot+Psi)+C*(phi+Q*alpha)))
 pressL=s.simplify((L1-2*a*K0*(a*n+2*rr))/(2*a*a))
 pressR=s.simplify((R1-4*a*K0*(a*n+ell+rr))/(4*a*a))
 def zero(e):return s.simplify(s.factor(e))==0
 gates={
  "background_lapse":zero(N0-2*a**3*(K0-Q*KQ)),
  "linear_lapse":zero(N1-(-2*a**3*Q*KQQ*dQ+2*a*a*(K0-Q*KQ)*vol)),
  "linear_lapse_gradient":zero(Nx0) and zero(Nx1-2*a*a*(KB*E1+C*X1)),
  "linear_longitudinal_pressure":zero(L1-(2*a*a*KQ*dQ+2*a*K0*(a*n+2*rr))) and zero(Lt1) and zero(Lx1),
  "linear_transverse_pressure":zero(R1-(4*a*a*KQ*dQ+4*a*K0*(a*n+ell+rr))),
  "linear_shift_momentum_exploratory":zero(b1+2*a**3*KQ*pdx) and zero(bx1),
  "newtonian_E_projection":zero(E1.subs(newt)-I*k*(alphadot+Psi)/a),
  "newtonian_X_projection":zero(X1.subs(newt)-I*k*(phi+Q*alpha)/a),
  "CLASS_linear_density_from_action":zero(dens-expected),
  "CLASS_spatial_pressure":zero(pressL-KQ*dQ) and zero(pressR-KQ*dQ),
  "CLASS_Pi_dictionary":zero(Pi-KQ*ds/3),
  "CLASS_background_rho_p":zero(rhoc-(Q*KQ-K0)/3) and zero(pc-K0/3),
  "CLASS_adiabatic_sound_speed":zero((KQ/3)/(Q*KQQ/3)-ca),
  "CLASS_background_conservation":zero((Q*KQQ/3)*(-3*KQ/KQQ)+3*(rhoc+pc)),
  "negative_wrong_rho_scaling":not zero(rhoc-rho8/2),
  "negative_drop_gradient":not zero(expected-Q*KQQ*ds/3),
  "negative_wrong_pressure_sign":not zero(Pi+KQ*ds/3)
 }
 failed=[k for k,v in gates.items() if not bool(v)]
 if failed:print("GE19_LW24_FAILED_GATES",failed,flush=True)
 need(not failed,"SYMBOLIC_ACTION_DICTIONARY_FAIL")
 return {k:bool(v) for k,v in gates.items()},{
  "background_rho8":"Q*K_Q-K","background_p8":"K",
  "CLASS_background":"rho=(Q*K_Q-K)/3, p=K/3, c_a^2=K_Q/(Q*K_QQ)",
  "CLASS_linear_density":"(Q*K_QQ*(phi_dot-Q*Psi) - k^2/a^2*(K_B*E_A+(2-K_B)*chi))/3",
  "CLASS_linear_pressure":"K_Q*(phi_dot-Q*Psi)/3",
  "CLASS_pressure_identity":"delta_p=c_a^2*(delta_rho + k^2/(3*a^2)*(K_B*E_A+(2-K_B)*chi))",
  "linear_shift_exploratory":"E_b=-2*a^3*K_Q*partial_x(phi)"
 }

def preflight():
 need(PRE.is_file() and blob(PRE)==PRE_BLOB,"PRELOCK_CHANGED")
 d=json.loads(PRE.read_text())
 need(d["classification"]=="GE19_LW24_REDUCED_ACTION_TO_CLASS_BACKGROUND_AND_LINEAR_PRESSURE_DICTIONARY_PRELOCK","PRECLASS_CHANGED")
 need(set(d["original_sources"])==set(ANCHORS),"SOURCE_SET_CHANGED")
 for p,want in d["original_sources"].items():
  f=ROOT/p
  need(f.is_file() and blob(f)==want,"ORIGINAL_SOURCE_CHANGED_"+f.name)
  src=f.read_text()
  for j,anchor in enumerate(ANCHORS[p],1):
   need(anchor in src,"ANCHOR_MISSING_"+f.name+"_"+str(j))
 return d["original_sources"]

def main():
 ap=argparse.ArgumentParser()
 ap.add_argument("--self-test",action="store_true")
 ap.add_argument("--out",type=Path,default=ROOT/
   "results/ge19_lw24_reduced_action_class_density_pressure_dictionary_20261110_r1.json")
 a=ap.parse_args()
 checks,formulas=symbolic()
 print("GE19_LW24_ACTION_SYMBOLIC_SELFTEST_PASS",len(checks),flush=True)
 if a.self_test:return
 parents=preflight()
 print("GE19_LW24_SOURCE_LOCKS_PASS",len(parents),flush=True)
 dest=a.out.resolve()
 need(dest.parent.is_dir() and not dest.exists(),"OUTPUT_EXISTS_OR_PARENT_MISSING")
 data={
  "classification":"GE19_LW24_REDUCED_ACTION_BACKGROUND_LINEAR_CLASS_DENSITY_PRESSURE_PASS_FULL_METRIC_FLUID_BRIDGE_OPEN",
  "predata_git_blob":PRE_BLOB,"original_source_blobs":parents,
  "exact_gates":checks,"formulas":formulas,
  "scope":"Reduced analytic GE06 longitudinal FLRW action, background and linear density-pressure relation only",
  "physical_eta_tangent_certified":False,
  "full_3plus1_action_to_CLASS_certified":False,
  "complete_aether_momentum_metric_constraints_certified":False,
  "nonanalytic_Y_included":False,"DES_gamma_t_observation":False,
  "LW22_geometry_pass_preserved":True,"LW23_eta_source_pass_preserved":True,
  "LW08_differential_source_unresolved_preserved":True,"H4_Z21_certified":False}
 dest.write_text(json.dumps(data,indent=2,sort_keys=True,allow_nan=False)+"\n")
 print("GE19_LW24_CLASSIFICATION",data["classification"],flush=True)
 print("GE19_LW24_PHYSICAL_OBSERVER_READY",False,flush=True)
 print("GE19_LW24_OUTPUT",dest,flush=True)

if __name__=="__main__":main()
