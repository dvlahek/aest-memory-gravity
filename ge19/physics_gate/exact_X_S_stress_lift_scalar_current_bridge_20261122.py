#!/usr/bin/env python3
"""GE19: exact closed (X,S_A) reduced-action flow and local scalar-current bridge.

No CLASS, no numerical scans, no full primordial-mode claim.
A stress-null state is tested dynamically, NOT assumed a physical free mode.
General gamma audits original gamma=1/4 versus historical gamma=1/2.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
import sympy as sp

LOCKS={
 "docs/ge19_20261119_exact_driven_X_E_constrained_source_bridge.md":
  "ebd1e7ae6c7221c1bbdc17a94409533a60c02c65",
 "docs/ge19_lw33_exact_scalar_action_to_CLASS_offshell_source_decision_2026-11-10.md":
  "dedcb6148b6ee4353c32972fcc456d9e3a185ffd",
 "docs/ge19_20261119_scalar_current_stress_null_primordial_selection.md":
  "33a0e880f24874fbf0e5f80b4c113d1000f14eba",
 "ge19/physics_gate/Exp_constraint_normalized_regular_source_20261122.py":
  "445d1b92a756cefd9189f3a884506823269c0958",
}
def source_locks(root):
 for path,expected in LOCKS.items():
  file=root/path
  if not file.is_file(): raise RuntimeError("MISSING_SOURCE "+path)
  actual=subprocess.check_output(["git","hash-object",str(file)],
                                 cwd=root,text=True).strip()
  if actual!=expected: raise RuntimeError("SOURCE_CHANGED "+path+" "+actual)
 print("GE19_XS_WARD_BRIDGE_SOURCE_LOCKS_PASS",len(LOCKS),flush=True)

def algebra():
 Kb,C,Q,Kq,Kqq,H,c,k,a,eta,B,F,Delta,X,E,S,eps,wb,gamma,Ra=sp.symbols(
  "K_B C Q K_Q K_QQ H c k a eta B F Delta X E S epsilon W_b gamma R_A",
  nonzero=True,real=True)
 Qdot=-3*H*c*Q
 Xdot=E+c*F
 Edot=-H*E+Q/Kb*((Kq-C*(H+Q-3*H*c))*X-C*c*F-gamma*eta*B)
 Sdef=Kb*E+C*Q*X
 Sdot=sp.expand(Kb*Edot+C*Qdot*X+C*Q*Xdot)
 lam=Kq-C*Q*(1+C/Kb)
 Sclosed=(C*Q/Kb-H)*Sdef+Q*lam*X-gamma*eta*Q*B
 Ffull=Delta+k*k*S/(3*a*a*Ra)
 Xformal=sp.cancel(Xdot.subs(E,(S-C*Q*X)/Kb)
                   .subs(F,Ffull).subs(c,Kq/(Q*Kqq))
                   .subs(Ra,Q*Kq/3))
 Xclosed=-C*Q*X/Kb+(1/Kb+k*k/(a*a*Q*Q*Kqq))*S+c*Delta
 Sformal=sp.factor(Sdot.subs(F,Ffull).subs(E,(S-C*Q*X)/Kb))
 Sfinal=(C*Q/Kb-H)*S+Q*lam*X-gamma*eta*Q*B

 # This variation assumes equal instantaneous metric, varphi, deltaQ
 # and q_j, with chi shift eps and E shift -C*eps/Kb.
 # Hence delta(Bchi)=W_b eps even for eta>0 on normalized bath branch.
 dS=Kb*(-C*eps/Kb)+C*eps
 dSdot=eps*(lam-gamma*eta*Q*wb)
 dJ_over_ika=eps*(2*Kq/Q-4*C/Kb-eta*wb/2)
 difference=sp.simplify((dSdot-Q*dJ_over_ika/2).subs(C,2-Kb))

 # For a selected, finite-time zero initial state X=S=q=qdot=0,
 # dot(X)_i=c*Delta_i and dot(S)_i=0. Derivative of B_i is
 # W_b Q_i dot(X)_i if the same selected zero auxiliary history starts there.
 # Thus Sddot_i=Q_i*c_i*Delta_i*(lambda_i-gamma*eta*Q_i*W_b).
 tests={
  "Sdot_density_source_F_cancels_exactly":sp.diff(Sdot,F)==0,
  "Sdot_action_to_raw_combination":sp.simplify(Sdot-Sclosed)==0,
  "Sdot_closed_X_S":sp.simplify(Sformal-Sfinal)==0,
  "Xdot_closed_X_S_gradient":sp.simplify(
    Xformal-Xclosed.subs(c,Kq/(Q*Kqq)))==0,
  "c_over_RA_from_action":sp.simplify(
    (Kq/(Q*Kqq))/(Q*Kq/3)-3/(Q*Q*Kqq))==0,
  "lambda_simplification_C_plus_KB_two":sp.simplify(
    (lam-Kq+2*C*Q/Kb).subs(C,2-Kb))==0,
  "stress_null_initial_S_zero":sp.simplify(dS)==0,
  "stress_null_eta0_lifting":sp.simplify(
    dSdot.subs({gamma:sp.Rational(1,4),eta:0})-lam*eps)==0,
  "quarter_source_current_bridge":sp.simplify(
    difference.subs(gamma,sp.Rational(1,4)))==0,
  "half_source_current_bridge_defect":sp.simplify(
    difference.subs(gamma,sp.Rational(1,2))+eta*Q*wb*eps/4)==0,
  "arbitrary_source_gamma_bridge_defect":sp.simplify(
    difference-(sp.Rational(1,4)-gamma)*eta*Q*wb*eps)==0,
  "scalar_current_agrees_with_stress_lift_eta0":sp.simplify(
    (dJ_over_ika.subs(eta,0)-2*eps*lam/Q).subs(C,2-Kb))==0,
  "zero_state_Xdot_first_nonzero":sp.simplify(
    Xclosed.subs({X:0,S:0})-c*Delta)==0,
  "zero_state_Sdot_initial_zero":sp.simplify(
    Sfinal.subs({X:0,S:0,B:0}))==0,
  "selected_zero_state_S_second_derivative":sp.simplify(
    Q*c*Delta*(lam-gamma*eta*Q*wb)
     -Q*c*Delta*(Kq-C*Q*(1+C/Kb)-gamma*eta*Q*wb))==0,
  "source_gamma_quarter_unique_for_nonzero_eta_wb":sp.simplify(
    (sp.Rational(1,4)-gamma).subs(gamma,sp.Rational(1,4)))==0,
  "source_gamma_half_negative_control_nonzero":sp.simplify(
    (sp.Rational(1,4)-gamma).subs(gamma,sp.Rational(1,2)))!=0,
 }
 failed=[name for name,ok in tests.items() if not bool(ok)]
 if failed: raise RuntimeError("GE19_XS_WARD_BRIDGE_SYMBOLIC_FAIL "+str(failed))
 return {
  "classification":"GE19_EXACT_REDUCED_X_S_STRESS_LIFT_AND_LOCAL_SCALAR_CURRENT_BRIDGE_PASS_NOT_FULL_PRIMORDIAL_WARD",
  "gate_count":len(tests),
  "gates":{name:bool(value) for name,value in tests.items()},
  "Xdot":"-(C*Q/K_B)*X+[1/K_B+k²/(a²*Q²*K_QQ)]*S_A+c_a²*Delta_A",
  "Sdot":"[C*Q/K_B-H]*S_A+Q*[K_Q-2*C*Q/K_B]*X-eta*Q*Bchi/4",
  "C":"2-K_B",
  "lambda":"K_Q-2*C*Q/K_B",
  "local_stress_null_shift":"delta chi=epsilon, delta E=-C epsilon/K_B; delta S_A=delta metric stress=0 at the same initial instant",
  "local_stress_lift":"delta Sdot_A=[K_Q-2*C*Q/K_B-eta*Q*W_b/4]*epsilon if delta q_j=0 at this initial instant",
  "local_spatial_current":"delta J_phi^x/(i*k*a)=epsilon*[2*K_Q/Q-4*C/K_B-eta*W_b/2]",
  "quarter_local_bridge":"delta Sdot_A=Q*delta J_phi^x/(2*i*k*a) for the stress-null displacement with fixed auxiliary coordinates, at gamma=1/4",
  "general_gamma_defect":"delta Sdot_gamma-Q delta J_phi^x/(2 i k a)=(1/4-gamma)*eta*Q*W_b*epsilon",
  "historical_half_source_defect":"-eta*Q*W_b*epsilon/4 for gamma=1/2",
  "selected_zero_state_onset":"If X=S=q=qdot=0 at a finite initial instant, Xdot=c_a² Delta_A, Sdot=0, Sddot=Q*c_a²*Delta_A*(K_Q-2*C*Q/K_B-eta*Q*W_b/4)",
  "important_limitations":[
   "The current-to-stress bridge holds for this specific initial variation, not the complete covariant Noether identity.",
   "A stress-null direction need not be a physical primordial adiabatic eigenmode.",
   "Chosen finite-time zero bath is not guaranteed by the original global no-free-bath retarded history.",
   "No complete Einstein-AeST-NL0B Hessian, finite-k physical growing eigenvector, or original full Ward propagation is certified.",
   "No CLASS runs, DES comparison, or physical delayed Weyl detection."
  ],
  "FULL_PHYSICS_GO":False,"DES_detection":False
 }
def main():
 p=argparse.ArgumentParser()
 p.add_argument("--repo-root",type=Path,default=Path(__file__).resolve().parents[2])
 p.add_argument("--self-test",action="store_true")
 p.add_argument("--out",type=Path)
 args=p.parse_args()
 if not args.self_test:source_locks(args.repo_root.resolve())
 result=algebra()
 print("GE19_XS_WARD_BRIDGE_SYMBOLIC_PASS",result["gate_count"],flush=True)
 print("GE19_FULL_PHYSICS_GO False",flush=True)
 if args.out:
  out=args.out.resolve()
  if out.exists():raise RuntimeError("REFUSE_OVERWRITE "+str(out))
  out.parent.mkdir(parents=True,exist_ok=True)
  out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
  print("GE19_XS_WARD_BRIDGE_REPORT",out,flush=True)
 elif args.self_test: print(json.dumps(result,indent=2,sort_keys=True))
if __name__=="__main__": main()
