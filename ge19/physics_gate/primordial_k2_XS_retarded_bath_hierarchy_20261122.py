#!/usr/bin/env python3
"""GE19 exact finite-k^2 hierarchy of the original reduced X-S-NL0B bath.

At any fixed regular time, for a selected analytic adiabatic branch with
X0=S0=Delta0=0 and no independent k-linear bath homogeneous solution:
X=k^2 X2+O(k^4), S=k^2 S2+O(k^4), q=k^3 q3+O(k^5).
This proves a conditional coefficient reduction, NOT the existence,
physical admissibility or uniqueness of the full primordial mode.
"""
from __future__ import annotations
import argparse,json,subprocess
from pathlib import Path
import sympy as sp

LOCKS={
 "ge19/physics_gate/frozen_exp_superhorizon_growing_mode_20261111.py":
  "e0a2562b2c728c1deef2eadb784f6c750aeef3b7",
 "ge19/physics_gate/exact_X_S_stress_lift_scalar_current_bridge_20261122.py":
  "6eb7e886fb04b8bdfd49295b2a298937c98c8612",
 "ge19/physics_gate/coupled_mixed_y_k2_photon_baryon_neutrino_20261121.py":
  "1a5736e05eb6c02dc3a05dc8334014088adef16d",
 "v019j/apply_memory_patch.py":
  "14796a5ed9e6265ed6810c792a93d7328a109364",
}
def lock_sources(root):
 for path,blob in LOCKS.items():
  f=root/path
  if not f.is_file():raise RuntimeError("GE19_K2_MISSING_SOURCE "+path)
  got=subprocess.check_output(["git","hash-object",str(f)],cwd=root,text=True).strip()
  if got!=blob:raise RuntimeError("GE19_K2_SOURCE_CHANGED "+path+" "+got)
 print("GE19_PHYSICAL_K2_HIERARCHY_SOURCE_LOCKS_PASS",len(LOCKS),flush=True)

def derive():
 k,a,Q,Kb,C,Kq,Kqq,H,c,eta,wb,omega,w,RA=sp.symbols(
   "k a Q K_B C K_Q K_QQ H c eta W_b omega w R_A",nonzero=True,real=True)
 x2,s2,d2,q3,p3,epsilon=sp.symbols(
   "X2 S2 Delta2 q3 p3 epsilon",real=True)
 # A single oscillator is enough to certify each coefficient, because the
 # multi-mode bath is additive. q is odd in k on the selected driven branch.
 X=k**2*x2;S=k**2*s2;Delta=k**2*d2;q=k**3*q3;p=k**3*p3
 Binst=wb*Q*X
 Bdel=-a*omega*sp.sqrt(w)*q/k
 B=Binst+Bdel
 x_rhs=-C*Q*X/Kb+(1/Kb+k**2/(a**2*Q**2*Kqq))*S+c*Delta
 s_rhs=(C*Q/Kb-H)*S+Q*(Kq-2*C*Q/Kb)*X-eta*Q*B/4
 q_acc=-3*H*p-omega**2*q+omega*sp.sqrt(w)*k*Q*X/a
 x2_rhs=-C*Q*x2/Kb+s2/Kb+c*d2
 s2_rhs=(C*Q/Kb-H)*s2+Q*(Kq-2*C*Q/Kb)*x2-eta*Q*(wb*Q*x2-a*omega*sp.sqrt(w)*q3)/4
 q3_rhs=p3
 p3_rhs=-3*H*p3-omega**2*q3+omega*sp.sqrt(w)*Q*x2/a
 def coef(expr,n):return sp.expand(expr).coeff(k,n)
 checks={
  "X_first_nonzero_k2":sp.simplify(coef(x_rhs,2)-x2_rhs)==0,
  "X_gradient_feedback_only_k4":sp.simplify(coef(x_rhs,4)-s2/(a*a*Q*Q*Kqq))==0,
  "S_first_nonzero_k2":sp.simplify(coef(s_rhs,2)-s2_rhs)==0,
  "S_no_k4_in_truncated_eta_source":sp.simplify(coef(s_rhs,4))==0,
  "qdot_driven_k3":sp.simplify(p/k**3-q3_rhs)==0,
  "qacc_driven_k3":sp.simplify(coef(q_acc,3)-p3_rhs)==0,
  "qacc_no_k1_source_if_X0_zero":sp.simplify(coef(q_acc,1))==0,
  "Binstant_k2":sp.simplify(coef(Binst,2)-wb*Q*x2)==0,
  "Bdelayed_k2_despite_q3":sp.simplify(coef(Bdel,2)+a*omega*sp.sqrt(w)*q3)==0,
  "Btotal_k2":sp.simplify(coef(B,2)-(wb*Q*x2-a*omega*sp.sqrt(w)*q3))==0,
  "stress_null_S2_initial_zero":sp.simplify(Kb*(-C*epsilon/Kb)+C*epsilon)==0,
  "stress_null_lift_can_enter_at_k2":sp.simplify(
   s2_rhs.subs(x2,x2+epsilon/Q)-s2_rhs-
   (Kq-2*C*Q/Kb-eta*Q*wb/4)*epsilon)==0,
  "eta0_bath_driven_but_no_E_feedback":sp.simplify(
   sp.diff(s2_rhs,eta)+Q*(wb*Q*x2-a*omega*sp.sqrt(w)*q3)/4)==0,
  "Kqq_gradient_absent_from_leading_k2_operator":sp.simplify(
   sp.diff(coef(x_rhs,2),Kqq))==0,
 }
 failed=[name for name,v in checks.items() if not bool(v)]
 if failed:raise RuntimeError("GE19_K2_HIERARCHY_SYMBOLIC_FAIL "+str(failed))
 return {
  "classification":"GE19_CONDITIONAL_ANALYTIC_K2_ORIGINAL_X_S_CAUSAL_BATH_HIERARCHY_PASS_NOT_PHYSICAL_PRIMORDIAL",
  "gate_count":len(checks),"gates":{n:bool(v) for n,v in checks.items()},
  "assumptions":[
   "Fixed regular positive a,Q,K_B,K_QQ and differentiable background, at finite t. No uniform claim as a->0.",
   "Analytic even-k physical scalar branch with X(k=0)=S_A(k=0)=Delta_A(k=0)=0; leading pure-gauge adiabatic state is a necessary input, not proof of its unique full finite-k continuation.",
   "Retarded bath with no independent homogeneous q_j=O(k) or q_j=O(1) mode; q_j=O(k³) follows from the driven source if X=O(k²).",
   "For the test-fluid estimate, Delta_A2 may use frozen dustlike 42-gate mixed coefficient but must be replaced by action-derived coupled pressureful AeST source for full physical mode."
  ],
  "x2_evolution":"dot X2=-(C Q/K_B) X2+S2/K_B+c_a² Delta_A2",
  "s2_evolution":"dot S2=(C Q/K_B-H) S2+Q(K_Q-2 C Q/K_B) X2-eta Q B2/4",
  "q3_evolution":"dot q3_j=p3_j; dot p3_j=-3H p3_j-omega_j² q3_j+omega_j sqrt(w_j) Q X2/a",
  "B2":"W_b Q X2-a sum_j omega_j sqrt(w_j) q3_j",
  "Bdelayed2":"-a sum_j omega_j sqrt(w_j) q3_j",
  "relative_orders":"X,S_A,Delta_A,Binstant,Bdelayed=O(k²); q_j=O(k³). Direct gradient feedback k² S_A first contributes at O(k^4) for fixed regular a(t).",
  "matter_proxy_Delta2":"-(15+4R_nu)*Psi0*tau²/40*(1-y_m/5) from dustlike Einstein-Boltzmann proxy, not a self-consistent pressureful-AeST mode",
  "undetermined_physical_data":"Two O(k²) coefficients X2(t_i), S2(t_i) (and transported retarded bath q3_j,p3_j); leading X0=S0=0 does not fix them. Full covariant scalar/aether/multiplier/Einstein Ward/adiabatic Frobenius selection is required.",
  "retarded_historical_zero_warning":"No independent bath homogeneous mode does NOT imply q3=p3=0 at arbitrary finite stored CLASS time.",
  "tangent_warning":"At eta0+ the initial-state eta derivative may add an independent metric tangent, not fixed by source-only decomposition.",
  "FULL_PHYSICS_GO":False,"DES_detection":False
 }
def main():
 ap=argparse.ArgumentParser()
 ap.add_argument("--repo-root",type=Path,default=Path(__file__).resolve().parents[2])
 ap.add_argument("--self-test",action="store_true")
 ap.add_argument("--out",type=Path)
 args=ap.parse_args()
 if not args.self_test:lock_sources(args.repo_root.resolve())
 r=derive()
 print("GE19_PHYSICAL_K2_HIERARCHY_SYMBOLIC_PASS",r["gate_count"],flush=True)
 print("GE19_FULL_PHYSICS_GO False",flush=True)
 if args.out:
  out=args.out.resolve()
  if out.exists():raise RuntimeError("REFUSE_OVERWRITE "+str(out))
  out.parent.mkdir(parents=True,exist_ok=True)
  out.write_text(json.dumps(r,indent=2,sort_keys=True,ensure_ascii=True)+"\n")
  print("GE19_K2_HIERARCHY_REPORT",out,flush=True)
 elif args.self_test:print(json.dumps(r,indent=2,sort_keys=True,ensure_ascii=True))
if __name__=="__main__":main()
