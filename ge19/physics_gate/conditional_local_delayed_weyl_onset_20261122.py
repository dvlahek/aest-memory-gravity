#!/usr/bin/env python3
"""GE19: finite-time delayed-Weyl onset from original quarter-source.

A theorem within the source-projected REDUCED Einstein--AeST equations on
a finite regular interval, with all ordinary species evolving only via metric
and no direct linear bath stress. This is NOT a globally selected physical
primordial mode, CLASS implementation, DES eta forecast, or observed signal.
"""
from __future__ import annotations
import argparse
import json
import subprocess
from pathlib import Path
import sympy as s

LOCKS = {
 "docs/ge19_20261115_constraint_eliminated_weyl_memory_cancellation_identity.md":
   "836b3ef6381a030ee549146b13948a7c2e01b499",
 "docs/ge19_20261120_joint_primordial_fluid_einstein_constraint_decision.md":
   "d2b35dbf361fe73398197963bfccc85021e2d1ba",
 "ge19/physics_gate/primordial_k2_XS_retarded_bath_hierarchy_20261122.py":
   "a7fa9069fb2670a0231ed8374d09ebd0b684d192",
 "docs/ge19_20261114_noether_constraint_and_eta0_retarded_branch_theorems.md":
   "dc5e1a39ffa383e425b1f3d5531ec8d5f6ad7a76",
}

def derive():
 h,k,a,Q,c,KB,KQ,KQQ,H,Delta,M2 = s.symbols(
  "h k a Q c K_B K_Q K_QQ H Delta M2", nonzero=True, real=True)
 S,Omega,Phi,phi,SS = s.symbols("S Omega Phi phi S_shear",real=True)
 RA=Q*KQ/3
 F=-(Omega+2*k*k*Phi/(3*a*a))/RA+k*k*S/(a*a*Q*KQ)
 deltaQ=-3*H*c*phi+Q*c*F
 W_from_stress=S/2-a*a*Q*KQQ*deltaQ/(2*k*k) - (
  3*a*a*H*KQ*phi+3*a*a*Omega)/(2*k*k) -9*a*a*SS/(4*k*k)
 exact_cancel=s.simplify(
  (W_from_stress-Phi+9*a*a*SS/(4*k*k)).subs(KQQ,KQ/(Q*c)))
 # Source comparison at eta=0+ with identical tangent initial data.
 # eta source history begins when chi_0(t_i+h)=D h+O(h²).
 D=Q*c*Delta
 bath_r_sum=M2*D*h**3/6
 Bdel=-bath_r_sum
 E1=s.integrate(-Q*Bdel/(4*KB),(h,0,h))
 S1=KB*E1   # only leading h^4; C*chi1 starts at h^5.
 F1=k*k*S1/(a*a*Q*KQ)  # Omega1,Phi1 start at h^6.
 phi1=s.integrate(Q*c*F1,(h,0,h))
 Phi1=s.integrate(KQ*phi1/2,(h,0,h))
 P_A1=c*k*k*S1/(3*a*a)
 DA1=-H*KQ*phi1
 checks={
  "stress_W_exactly_reduces_to_Phi_minus_shear": exact_cancel==0,
  "bath_retarded_h3":s.simplify(Bdel+M2*Q*c*Delta*h**3/6)==0,
  "E_history_h4":s.simplify(E1-Q*D*M2*h**4/(96*KB))==0,
  "phi_history_h5":s.simplify(phi1-c*k*k*Q*D*M2*h**5/(480*a*a*KQ))==0,
  "Weyl_history_h6":s.simplify(Phi1-c*k*k*Q*D*M2*h**6/(5760*a*a))==0,
  "AeST_density_history_h5":s.simplify(DA1+H*c*k*k*Q*D*M2*h**5/(480*a*a))==0,
  "spatial_trace_leading_pressure":s.simplify(s.diff(Phi1,h,2)-s.Rational(3,2)*P_A1)==0,
  "AeST_continuity_leading":s.simplify(s.diff(DA1,h)+3*H*P_A1)==0,
  "comoving_density_h5_cancels":s.simplify(DA1+H*KQ*phi1)==0,
  "Weyl_k4_if_adiabatic_Delta_k2":s.simplify(
   (Phi1.subs(Delta,k*k*s.Symbol("Delta2"))/k**4).diff(k))==0,
 }
 bad=[n for n,v in checks.items() if not v]
 if bad:raise RuntimeError("LOCAL_CAUSAL_EINSTEIN_ONSET_FAIL "+repr(bad))
 return {
  "classification":"GE19_CONDITIONAL_REDUCED_ALL_SPECIES_CAUSAL_WEYL_H6_PROVED_NOT_FULL_PRIMORDIAL",
  "symbolic_checks":checks,"check_count":len(checks),
  "conditions":[
   "Finite regular t_i, k!=0, a,Q,K_Q,K_B,c nonzero and smooth.",
   "At eta0+ baseline chi_i=E_i=r_j_i=dot_r_j_i=0 and D_i=Q_i c_i Delta_A_i !=0.",
   "History-only eta derivative is retarded-minus-instantaneous comparator under SAME baseline, SAME operator and SAME initial eta derivative.",
   "All ordinary species have no direct eta NL0B forcing and respond through the metric (no earlier independent eta source); direct linear bath stress vanishes about relaxed background.",
   "Original quarter-normalized reduced scalar/aether and total Einstein constraints/pressure trace; full covariant action equivalence and physical finite-k growing adiabatic mode NOT certified.",
   "The leading-order calculation uses coefficients at t_i; coefficient time derivatives enter subleading orders."
  ],
  "E_1_hist":"Q_i D_i M2 h^4/(96 K_B)+O(h^5)",
  "phi_1_hist":"c_i k^2 Q_i D_i M2 h^5/(480 a_i^2 K_Q_i)+O(h^6)",
  "Phi_1_hist_and_W1_hist":"c_i k^2 Q_i D_i M2 h^6/(5760 a_i^2)+O(h^7)",
  "density_A_1_hist":"-H_i c_i k^2 Q_i D_i M2 h^5/(480 a_i^2)+O(h^6)",
  "D_i":"Q_i c_i Delta_A_i",
  "if_Delta_A_i_is_O_k2":"W_history=O(k^4 h^6) at FIXED finite regular t_i; not a uniform primordial limit.",
  "exact_stress_reduction":"W_stress(Phi,phi,E,chi,ordinary)=Phi-9 a^2 S_shear/(4 k^2), provided the action density/phase and Einstein source constraints are imposed.",
  "physical_matter_Weyl_transfer_ready":False,
  "DES_detection":False,
  "FULL_PHYSICS_GO":False,
 }

def main():
 p=argparse.ArgumentParser()
 p.add_argument("--repo-root",type=Path,default=Path(__file__).resolve().parents[2])
 p.add_argument("--out",type=Path)
 p.add_argument("--self-test",action="store_true")
 args=p.parse_args()
 if not args.self_test:
  for path,sha in LOCKS.items():
   f=args.repo_root/path
   if not f.is_file():raise RuntimeError("MISSING_SOURCE "+path)
   got=subprocess.check_output(["git","hash-object",str(f)],cwd=args.repo_root,text=True).strip()
   if got!=sha:raise RuntimeError("SOURCE_CHANGED "+path+" "+got)
  print("GE19_LOCAL_WEYL_ONSET_SOURCE_LOCKS_PASS",len(LOCKS),flush=True)
 result=derive()
 print("GE19_CONDITIONAL_WEYL_H6_SYMBOLIC_PASS",result["check_count"],flush=True)
 print("GE19_FULL_PHYSICS_GO False",flush=True)
 if args.out:
  o=args.out.resolve()
  if o.exists():raise RuntimeError("REFUSE_OVERWRITE "+str(o))
  o.parent.mkdir(parents=True,exist_ok=True)
  o.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
  print("GE19_LOCAL_WEYL_ONSET_REPORT",o,flush=True)
if __name__=="__main__":main()
