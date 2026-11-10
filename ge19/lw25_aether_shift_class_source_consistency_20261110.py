#!/usr/bin/env python3
"""GE19 LW25: exact reduced aether+shift Euler vs frozen CLASS eta source.

Physics-only conditional consistency diagnostic. A conditional coefficient
difference DOES NOT by itself establish an error in full 3+1 gravity or CLASS:
the action-to-effective-fluid velocity/Euler field redefinition is open.
No CLASS, galaxy observations, model tuning or numerical sweeps.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/"ge19/lw25_aether_shift_class_memory_source_consistency_predata_20261110.json"
PRE_BLOB="80afe36c4ea5859f3f0e4f76e9f5814f99b7290f"
ANCHORS={
 "ge06/analytic_aest_directional_source_generator.py":[
   "Qinv=ch*sigma+sh*px/L","Xinv=sh*sigma+ch*px/L",
   "aest=N*L*R**2*(KB*E**2 + 2*C*E*Xinv - C*Xinv**2 + 2*Kfun)"],
 "ge05/memory_directional_source_generator.py":[
   "lag=N*L*R**2*sp.Rational(1,4)*(Aq**2-(om*q-sw*Xphi)**2)"],
 "ge19/lw19_reduced_full_action_temporal_invariance_20261110.py":[
   "matter=volume*(KB*E**2+2*C*E*X-C*X**2+2*K(Q)"],
 "v019/apply_patch_v019.py":[
   "dy[pv->index_pt_theta_cdm] =",
   "dy[pv->index_pt_alpha_aest] = a*(E_aest-psi_aest);",
   "dy[pv->index_pt_E_aest] = a*E_rhs_aest/pba->aest_KB-a_prime_over_a*E_aest;"],
 "v019j/apply_memory_patch.py":[
   "Bchi_aest *= pba->aest_eta;",
   "E_rhs_aest -= 0.5*Q_aest*Bchi_aest;"],
 "ge19/lw24_reduced_action_class_density_pressure_dictionary_20261110.py":[
   "linear_shift_momentum_exploratory",
   "CLASS_Pi_dictionary"]
}
def require(ok,label):
 if not bool(ok):
  raise RuntimeError("GE19_LW25_"+label)
def blob(p):
 return subprocess.check_output(["git","hash-object",str(p)],cwd=ROOT,text=True).strip()
def sha(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for b in iter(lambda:f.read(1<<20),b""):h.update(b)
 return h.hexdigest()

def symbolic():
 import sympy as s
 N,L,R,b,u,pt,px,ut,ux,Nx,Lt,Lx,bx,qt,qx,q=s.symbols(
  "N L R b u pt px ut ux Nx Lt Lx bx qt qx q",real=True)
 KB,C,eta,om,sw=s.symbols("KB C eta om sw",real=True,nonzero=True)
 a,ad,Q,eps,n,ell,rr,z,v,pdt,pdx,vdt,nx,q1,qd=s.symbols(
  "a ad Q eps n ell rr z v pdt pdx vdt nx q1 qd",real=True,nonzero=True)
 KQ=s.symbols("KQ",real=True)
 ch,sh=s.cosh(u),s.sinh(u)
 sigma=(pt-b*px)/N
 Qinv=ch*sigma+sh*px/L
 X=sh*sigma+ch*px/L
 E=ch*((ut-b*ux)/N+Nx/(N*L))+sh*((Lt-b*Lx-L*bx)/(N*L)+ux/L)
 Aq=ch*(qt-b*qx)/N+sh*qx/L
 K=s.Function("K")
 lag=N*L*R**2*(KB*E**2+2*C*E*X-C*X**2+2*K(Qinv)
    +eta*s.Rational(1,4)*(Aq**2-(om*q-sw*X)**2))
 perturb={N:1+eps*n,L:a+eps*ell,R:a+eps*rr,b:eps*z,
  u:eps*v,pt:Q+eps*pdt,px:eps*pdx,ut:eps*vdt,ux:0,
  Nx:eps*nx,Lt:ad,Lx:0,bx:0,qt:eps*qd,q:eps*q1,qx:0}
 def linpartial(field):
  t=s.diff(lag,field).subs(perturb)
  t=s.diff(t,eps).subs(eps,0).doit()
  return s.simplify(t).subs(s.Derivative(K(Q),Q),KQ)
 E1=vdt+nx/a+ad*v/a
 X1=Q*v+pdx/a
 B1=sw**2*X1-om*sw*q1
 H=ad/a
 A1=KB*E1+C*X1
 pu=linpartial(u)
 put=linpartial(ut)
 pux=linpartial(ux)
 pb=linpartial(b)
 pbx=linpartial(bx)
 goal_pu=2*a**3*(H*A1+C*Q*(E1-X1)+KQ*X1)-eta*a**3*Q*B1/2
 goal_put=2*a**3*A1
 # The true density-space CLASS theta/alpha dictionary is still
 # conditionally assumed, not derived here for finite eta.
 k,EA,chi,Bchi,Pi,alpha,ca2,w,Ed,Chid,theta,thetad,Psi,alphad,Qdot=s.symbols(
  "k EA chi Bchi Pi alpha ca2 w Ed Chid theta thetad Psi alphad Qdot",
  real=True,nonzero=True)
 class_theta=(3*ca2-1)*H*theta+k*k/a*(Pi/(1+w)+Psi)
 class_alpha=EA-Psi
 class_Qdot=-3*H*ca2*Q
 chi_dot=Qdot*(a*theta/k**2+alpha)+Q*(a*H*theta+a*thetad)/k**2+Q*alphad
 chi_ideal=Q*(EA+Pi/(1+w)-3*ca2*H*alpha)
 # After substituting E1=(ik/a)EA, X1=(ik/a)chi and
 # taking the full proper-time derivative of 2 a^3 A1:
 # E_u/(2 i k a^2) = -[KB*(Ed+H EA)-KQ chi +
 # C*(Chid-Q EA+(H+Q)chi)+eta Q Bchi/4].
 action_res=KB*(Ed+H*EA)-KQ*chi+C*(Chid-Q*EA+(H+Q)*chi)+eta*Q*Bchi/4
 # Literal original v019j/CLASS E_rhs memory source is -eta QB/2.
 class_res=KB*(Ed+H*EA)-KQ*chi+C*(Q*Pi/(1+w)+(H+Q)*chi-3*ca2*H*Q*alpha)+eta*Q*Bchi/2
 gap=s.simplify((class_res-action_res).subs(Chid,chi_ideal))
 needed=eta*Q*Bchi/(4*C)
 checks={
  "original_reduced_aether_u_force":s.simplify(pu-goal_pu)==0,
  "original_reduced_aether_u_kinetic_momentum":s.simplify(put-goal_put)==0,
  "reduced_aether_u_spatial_derivative_zero_at_linear":s.simplify(pux)==0,
  "original_reduced_shift_source":s.simplify(pb+2*a**3*KQ*pdx)==0,
  "original_reduced_shift_gradient_zero":s.simplify(pbx)==0,
  "aether_bath_Euler_coefficient_minus_eta_half_before_normalization":
   s.simplify(s.diff(pu,eta)+a**3*Q*B1/2)==0,
  "Newtonian_E1_projection":
   s.simplify(E1.subs({v:s.I*k*alpha/a,
     vdt:s.I*k*(alphad-H*alpha)/a,nx:s.I*k*Psi})
     -s.I*k*(alphad+Psi)/a)==0,
  "Newtonian_X1_projection":
   s.simplify(X1.subs({v:s.I*k*alpha/a,pdx:s.I*k*s.Symbol('varphi')})
    -s.I*k*(s.Symbol('varphi')+Q*alpha)/a)==0,
  "original_CLASS_chidot_chain_with_unmodified_theta":
   s.simplify(chi_dot.subs({Qdot:class_Qdot,thetad:class_theta,alphad:class_alpha})-chi_ideal)==0,
  "eta0_action_CLASS_E_source_agree_conditional":
   s.simplify((class_res-action_res).subs({Chid:chi_ideal,eta:0}))==0,
  "finite_eta_conditioned_coefficient_gap":
   s.simplify(gap-eta*Q*Bchi/4)==0,
  "factor_two_ratio_is_exact":
   s.simplify((eta*Q*Bchi/2)/(eta*Q*Bchi/4)-2)==0,
  "gap_canceled_by_required_chidot_correction":
   s.simplify((class_res-action_res).subs(Chid,chi_ideal+needed))==0,
  "required_conformal_theta_source":
   s.simplify((k*k/(a*Q)*needed)*a-eta*k*k*Bchi/(4*C))==0,
  "negative_control_unmodified_theta_not_equal_eta_nonzero":
   s.simplify(gap)!=0,
 }
 failed=[name for name,ok in checks.items() if not bool(ok)]
 if failed:print("GE19_LW25_FAILED_GATES",failed,flush=True)
 require(not failed,"SYMBOLIC_FAIL")
 return {k:bool(v) for k,v in checks.items()},{
  "action_first_order_reduced_aether":
   "E_u/(2 i k a^2)=-[K_B*(E_A_dot+H E_A)-K_Q*chi+C*(chi_dot-Q E_A+(H+Q)*chi)+eta Q Bchi/4]",
  "class_source":
   "K_B*(E_A_dot+H E_A)=K_Q*chi-C*(Q Pi/(1+w)+(H+Q)*chi-3*c_a^2*H*Q*alpha)-eta Q Bchi/2",
  "conditional_coefficient_gap":
   "CLASS_vs_reduced_action source: eta Q Bchi/4, assuming unchanged CLASS theta_dot and standard chi dictionary",
  "needed_if_same_dictionary":"delta chi_dot=eta Q Bchi/(4 C); or delta theta_prime=eta k^2 Bchi/(4 C)",
  "shift":"E_b^(1)=-2a^3 K_Q partial_x(varphi) with no direct bath O(eta*perturbation)",
 }

def main():
 ap=argparse.ArgumentParser()
 ap.add_argument("--self-test",action="store_true")
 ap.add_argument("--lw24",type=Path,default=ROOT/
   "results/ge19_lw24_reduced_action_class_density_pressure_dictionary_20261110_r1.json")
 ap.add_argument("--out",type=Path,default=ROOT/
   "results/ge19_lw25_aether_shift_class_source_consistency_20261110_r1.json")
 o=ap.parse_args()
 checks,formulas=symbolic()
 print("GE19_LW25_EXACT_SYMBOLIC_SELFTEST_PASS",len(checks),flush=True)
 if o.self_test:return
 require(PRE.is_file() and blob(PRE)==PRE_BLOB,"PRELOCK_CHANGED")
 pre=json.loads(PRE.read_text())
 require(pre["classification"]=="GE19_LW25_REDUCED_AETHER_SHIFT_CLASS_MEMORY_SOURCE_CONDITIONAL_CONSISTENCY_PRELOCK","PRECLASS_CHANGED")
 require(set(pre["source_blobs"])==set(ANCHORS),"SOURCES_CHANGED")
 for p,want in pre["source_blobs"].items():
  f=ROOT/p
  require(f.is_file() and blob(f)==want,"SOURCE_SHA_CHANGED_"+f.name)
  for j,needle in enumerate(ANCHORS[p],1):
   require(needle in f.read_text(),"SOURCE_ANCHOR_MISSING_"+f.name+"_"+str(j))
 print("GE19_LW25_SOURCE_LOCKS_PASS",len(ANCHORS),flush=True)
 require(o.lw24.is_file() and sha(o.lw24)==pre["parent_LW24_original_JSON_SHA256"],"ORIGINAL_LW24_SHA_CHANGED")
 lw24=json.loads(o.lw24.read_text())
 require(lw24["classification"]=="GE19_LW24_REDUCED_ACTION_BACKGROUND_LINEAR_CLASS_DENSITY_PRESSURE_PASS_FULL_METRIC_FLUID_BRIDGE_OPEN","PARENT_CLASS")
 require(len(lw24["exact_gates"])==17 and all(lw24["exact_gates"].values()),"PARENT_GATES")
 out=o.out.resolve()
 require(out.parent.is_dir() and not out.exists(),"OUTPUT_PREEXISTS_OR_PARENT_MISSING")
 report={
  "classification":"GE19_LW25_REDUCED_AETHER_CLASS_ETA_SOURCE_FACTOR_TWO_CONDITIONAL_REVIEW_REQUIRED",
  "exact_symbolic_checks":checks,"formulas":formulas,
  "predata_blob":PRE_BLOB,"original_source_blobs":pre["source_blobs"],
  "LW24_original_SHA256":pre["parent_LW24_original_JSON_SHA256"],
  "physical_interpretation":"A conditional discrepancy under unchanged CLASS theta equation and naive action-to-fluid identification; the complete constraint-reduced scalar+aether+metric Euler map is still open. NOT a proved bug of CLASS or of the full theory.",
  "physical_eta_Weyl_derivative_certified":False,
  "full_3plus1_action_to_CLASS_certified":False,
  "LW22_geometry_PASS_preserved":True,
  "LW23_source_PASS_preserved":True,
  "LW24_reduced_density_pressure_PASS_preserved":True,
  "DES_observation_found":False}
 out.write_text(json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+"\n")
 print("GE19_LW25_CLASSIFICATION",report["classification"],flush=True)
 print("GE19_LW25_PHYSICAL_OBSERVER_READY",False,flush=True)
 print("GE19_LW25_OUTPUT",out,flush=True)

if __name__=="__main__":main()
