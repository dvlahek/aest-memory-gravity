#!/usr/bin/env python3
"""GE19 exact Einstein-constrained AeST scalar source and Exp regularity screen.

Does NOT solve original finite-k Einstein-AeST-NL0B primordial mode or Ward.
No CLASS, fitting or numerical parameter search.
"""
from __future__ import annotations
import argparse, json, subprocess
from pathlib import Path
import sympy as s

LOCKS = {
 "docs/ge19_20261119_exact_driven_X_E_constrained_source_bridge.md":
  "ebd1e7ae6c7221c1bbdc17a94409533a60c02c65",
 "docs/ge19_20261119_scalar_current_stress_null_primordial_selection.md":
  "33a0e880f24874fbf0e5f80b4c113d1000f14eba",
 "v019/patch/source/aest_memory.c":
  "9a522a653a1855eda3cb67e856f9fc10a1e73d54",
 "ge19/physics_gate/coupled_mixed_y_k2_photon_baryon_neutrino_20261121.py":
  "1a5736e05eb6c02dc3a05dc8334014088adef16d",
}
def locks(root):
 for path,want in LOCKS.items():
  f=root/path
  if not f.exists(): raise RuntimeError("GE19_SOURCE_MISSING "+path)
  got=subprocess.check_output(["git","hash-object",str(f)],cwd=root,text=True).strip()
  if got!=want: raise RuntimeError("GE19_SOURCE_CHANGED "+path+" "+got)
 print("GE19_EXP_CONSTRAINT_SOURCE_LOCKS_PASS",len(LOCKS),flush=True)

def derive():
 Q,KQ,KQQ,a,k,KB,C,X,E,Phi,Om,D=s.symbols(
  "Q K_Q K_QQ a k K_B C X E Phi Omega_s Delta_A",real=True,nonzero=True)
 RA=Q*KQ/3
 c=KQ/(Q*KQQ)
 stress=KB*E+C*Q*X
 numerator=-Om+k**2*(stress-2*Phi)/(3*a**2)
 F=numerator/RA
 derived=(-3*Om+k**2*(stress-2*Phi)/a**2)/(Q**2*KQQ)
 constrained_Omega=k**2*(stress-2*Phi)/(3*a**2)-RA*D
 Z,eps,Q0,K2=s.symbols("Z epsilon Q0 K2",positive=True)
 Qe=Q0+eps*Z
 KQe=4*K2*eps*Z*s.exp(Z**2)
 KQQe=4*K2*s.exp(Z**2)*(1+2*Z**2)
 ce=KQe/(Qe*KQQe)
 RAe=Qe*KQe/3
 ratio=s.factor(ce/RAe)
 lim=s.limit(ratio,eps,0,dir="+")
 e,eta,Wb=s.symbols("e eta W_b",positive=True)
 dchi=e; dE=-C*e/KB; dalpha=e/Q
 dS=KB*dE+C*dchi
 dJ=2*C*(dE-dchi)+2*KQ*dalpha-eta*Wb*e/2
 test={
  "exact_constrained_cF_source":s.simplify(c*F-derived)==0,
  "ratio_c_over_RA_cancels_KQ":s.simplify(c/RA-3/(Q**2*KQQ))==0,
  "regular_Delta_gives_numerator_RA_Delta":
   s.simplify(numerator.subs(Om,constrained_Omega)-RA*D)==0,
  "regular_Delta_gives_cF_c_Delta":
   s.simplify((c*F).subs(Om,constrained_Omega)-c*D)==0,
  "Exp_c_exact":
   s.simplify(ce-eps*Z/(Qe*(1+2*Z**2)))==0,
  "Exp_RA_exact":
   s.simplify(RAe-4*K2*Qe*eps*Z*s.exp(Z**2)/3)==0,
  "Exp_ratio_nonzero_fixed_Z_epsilon_to_zero":
   s.simplify(lim-3/(4*K2*Q0**2*s.exp(Z**2)*(1+2*Z**2)))==0,
  "Exp_c_to_zero_at_fixed_Z":s.limit(ce,eps,0,dir="+")==0,
  "Exp_RA_to_zero_at_fixed_Z":s.limit(RAe,eps,0,dir="+")==0,
  "Exp_KQQ_positive":bool(KQQe.is_positive),
  "stress_null_S_invariant":s.simplify(dS)==0,
  "stress_null_spatial_scalar_current":
   s.simplify((dJ/e-2*KQ/Q+4*C/KB+eta*Wb/2).subs(C,2-KB))==0,
  "eta0_stress_null_spatial_current":
   s.simplify((dJ.subs(eta,0)/e-2*KQ/Q+4*C/KB).subs(C,2-KB))==0,
 }
 failed=[name for name,v in test.items() if not bool(v)]
 if failed: raise RuntimeError("GE19_EXP_CONSTRAINT_SYMBOLIC_FAIL "+str(failed))
 return {
  "classification":"GE19_EXP_CONSTRAINT_NORMALIZED_SOURCE_AND_REGULARITY_NECESSARY_CONDITION_PASS_NOT_PHYSICAL_PRIMORDIAL",
  "gate_count":len(test),"gates":{n:bool(v) for n,v in test.items()},
  "exact_identity":"c_a2/R_A=3/(Q**2*K_QQ)",
  "exact_source":"c_a2*F=[k**2*(K_B E+(2-K_B)QX-2Phi)/a**2-3Omega_s]/(Q**2*K_QQ)",
  "Einstein_numerator":"N=-Omega_s+k**2*(K_B E+(2-K_B)QX-2Phi)/(3a**2)=R_A Delta_A",
  "frozen_Exp_bound":"0<c_a2/R_A<3/(4*K2*Q0**2)=7894.736842105263 at Q0=1e-4 K2=9500 Z>0",
  "fixed_Z_limit":"For Z0=epsilon->0 at fixed finite positive Z, c_a2 and R_A vanish, but c_a2/R_A remains finite nonzero; NOT a physical fixed-calibrated-I0 limit.",
  "necessary_regular_condition":"If Delta_A remains bounded as R_A tends to zero, N must be O(R_A), and c_a2*F=c_a2*Delta_A tends to zero. N held nonzero makes Delta_A divergent, not a regular physical source.",
  "stress_null_selection":"Einstein stress depends on S=K_B E+(2-K_B)QX; delta chi=e, delta E=-(2-K_B)e/K_B leaves S unchanged. Full scalar/aether propagation and Ward needed to fix the physical amplitude.",
  "scalar_current":"delta J_phi^x/(i k a e)=2K_Q/Q-4(2-K_B)/K_B-eta W_b/2; Ward constrains current divergence, not its spatial component to vanish.",
  "full_physics_GO":False,"DES_detection":False,
 }
def main():
 p=argparse.ArgumentParser()
 p.add_argument("--repo-root",type=Path,default=Path(__file__).resolve().parents[2])
 p.add_argument("--self-test",action="store_true")
 p.add_argument("--out",type=Path)
 opts=p.parse_args()
 if not opts.self_test:locks(opts.repo_root.resolve())
 report=derive()
 print("GE19_EXP_CONSTRAINT_REGULAR_SOURCE_PASS",report["gate_count"],flush=True)
 print("GE19_FULL_PHYSICS_GO False",flush=True)
 if opts.out:
  out=opts.out.resolve()
  if out.exists():raise RuntimeError("REFUSE_OVERWRITE "+str(out))
  out.parent.mkdir(parents=True,exist_ok=True)
  out.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
  print("GE19_EXP_CONSTRAINT_REPORT",out,flush=True)
 elif opts.self_test:print(json.dumps(report,indent=2,sort_keys=True))
if __name__=="__main__":main()
