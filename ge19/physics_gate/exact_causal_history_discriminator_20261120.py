#!/usr/bin/env python3
"""GE19 exact original-reduced NL0B pulse-history discrimination.

Controlled external chi(t), a=1,H=0, one positive bath oscillator,
no homogeneous auxiliary mode. NOT a full gravitational/Weyl detection.
"""
import argparse,json,subprocess
from pathlib import Path
import sympy as s

LOCKS={
 "docs/ge19_20261114_noether_constraint_and_eta0_retarded_branch_theorems.md":
  "dc5e1a39ffa383e425b1f3d5531ec8d5f6ad7a76",
 "docs/ge19_lw33_exact_scalar_action_to_CLASS_offshell_source_decision_2026-11-10.md":
  "dedcb6148b6ee4353c32972fcc456d9e3a185ffd",
 "docs/ge19_20261119_retarded_history_transport_no_finite_reset.md":
  "22b149ecd4af867135dfb14e12aa3cfed30cc941",
}
def source_locks(root):
 for path,expected in LOCKS.items():
  f=root/path
  if not f.is_file():raise RuntimeError("SOURCE_MISSING "+path)
  got=subprocess.check_output(["git","hash-object",str(f)],cwd=root,text=True).strip()
  if got!=expected:raise RuntimeError("SOURCE_CHANGED "+path+" "+got)
 print("GE19_EXACT_HISTORY_SOURCE_LOCKS_PASS",len(LOCKS))

def derive():
 t,T,A,k,w,eta,Q,KB=s.symbols("t T chi0 k w eta Q K_B",positive=True,real=True)
 omega=s.pi/T
 chi=A*s.sin(omega*t)**2
 q=s.sqrt(w)*k*A/(6*omega)*(3+s.cos(2*omega*t)-4*s.cos(omega*t))
 pd=s.diff(q,t)
 B=w*chi-omega*s.sqrt(w)*q/k
 B_expected=s.Rational(2,3)*w*A*(s.cos(omega*t)-s.cos(2*omega*t))
 q_post=s.simplify(q.subs(t,T))*s.cos(omega*(t-T))
 B_post=-omega*s.sqrt(w)*q_post/k
 energy_at_T=s.factor(eta/4*(pd.subs(t,T)**2+(omega*q.subs(t,T))**2))
 Om=s.symbols("Omega",real=True)
 susceptibility=s.factor(w*(1-omega**2/(omega**2-Om**2)))
 checks={
  "pulse_chi_zero_at_end":s.simplify(chi.subs(t,T))==0,
  "pulse_chidot_zero_at_end":s.simplify(s.diff(chi,t).subs(t,T))==0,
  "zero_initial_auxiliary_coordinate":s.simplify(q.subs(t,0))==0,
  "zero_initial_auxiliary_velocity":s.simplify(pd.subs(t,0))==0,
  "original_forced_auxiliary_ode":s.simplify(s.diff(q,t,2)+omega**2*q-omega*s.sqrt(w)*k*chi)==0,
  "exact_history_force_during_pulse":s.simplify(B-B_expected)==0,
  "nonzero_endpoint_auxiliary_coordinate":s.simplify(q.subs(t,T)-4*s.sqrt(w)*k*A*T/(3*s.pi))==0,
  "zero_endpoint_auxiliary_velocity":s.simplify(pd.subs(t,T))==0,
  "endpoint_force_retarded_nonzero":s.simplify(B.subs(t,T)+4*w*A/3)==0,
  "endpoint_instantaneous_force_zero":s.simplify((w*chi).subs(t,T))==0,
  "positive_auxiliary_energy_stored":s.simplify(energy_at_T-4*eta*w*k**2*A**2/9)==0,
  "post_pulse_homogeneous_oscillator":s.simplify(s.diff(q_post,t,2)+omega**2*q_post)==0,
  "post_pulse_force_oscillatory":s.simplify(B_post+4*w*A*s.cos(omega*(t-T))/3)==0,
  "retarded_susceptibility_frequency_dependence":s.simplify(susceptibility+w*Om**2/(omega**2-Om**2))==0,
  "adiabatic_static_susceptibility_zero":s.limit(susceptibility,Om,0)==0,
  "high_frequency_limit_instantaneous":s.limit(susceptibility,Om,s.oo)==w,
  "low_frequency_quadratic_suppression":s.simplify(s.limit(susceptibility/Om**2,Om,0)+w/omega**2)==0,
  "quarter_normalized_direct_aether_source":s.simplify(-eta*Q*B.subs(t,T)/(4*KB)-eta*Q*w*A/(3*KB))==0,
 }
 failures=[key for key,value in checks.items() if not bool(value)]
 if failures:raise RuntimeError("GE19_EXACT_HISTORY_SYMBOLIC_FAIL "+str(failures))
 return {
  "classification":"GE19_EXACT_NL0B_REDUCED_CAUSAL_HISTORY_DISCRIMINATOR_PASS_NOT_PHYSICAL_WEYL",
  "symbolic_checks":{key:bool(value) for key,value in checks.items()},
  "gate_count":len(checks),
  "exact_controlled_pulse":"chi(t)=chi0*sin(pi*t/T)**2 for 0<=t<=T, omega=pi/T",
  "state_at_endpoint":"chi(T)=chidot(T)=qdot(T)=0; q(T)=4*k*sqrt(w)*chi0*T/(3*pi)",
  "history_force_at_endpoint":"Bchi(T)=-4*w*chi0/3 vs Bchi(T)=0 for never-driven history",
  "post_pulse":"Bchi(t)=-4*w*chi0*cos(pi*(t-T)/T)/3 for t>T with H=0",
  "bath_energy_at_endpoint":"E_bath(T)=4*eta*w*k**2*chi0**2/9 >0 for eta,w>0",
  "quarter_action_aether_force_at_endpoint":"+eta*Q*w*chi0/(3*K_B)",
  "steady_frequency_response":"Bchi/chi=-w*Omega**2/(omega**2-Omega**2) with causal i0 prescription",
  "interpretation":"Same chi and chidot at T but different Bchi for distinct input histories. Reduced-action causal memory, not cosmological or Ward-certified physical Weyl memory.",
  "full_physics_GO":False,"physical_Weyl_memory_detection":False,
 }
def main():
 ap=argparse.ArgumentParser()
 ap.add_argument("--repo-root",type=Path,default=Path(__file__).resolve().parents[2])
 ap.add_argument("--self-test",action="store_true")
 ap.add_argument("--out",type=Path)
 opt=ap.parse_args()
 if not opt.self_test:source_locks(opt.repo_root.resolve())
 report=derive()
 print("GE19_EXACT_CAUSAL_HISTORY_DISCRIMINATOR_SYMBOLIC_PASS",report["gate_count"])
 print("GE19_FULL_PHYSICS_GO False")
 if opt.out:
  target=opt.out.resolve()
  if target.exists():raise RuntimeError("REFUSE_OVERWRITE "+str(target))
  target.parent.mkdir(parents=True,exist_ok=True)
  target.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
  print("GE19_HISTORY_DISCRIMINATOR_REPORT",target)
 elif opt.self_test:print(json.dumps(report,indent=2,sort_keys=True))
if __name__=="__main__":main()
