#!/usr/bin/env python3
"""GE19: corrected neutrino F3 k^3 gate + causal NL0B source-onset jet.

Action-exact finite-time jet ONLY under selected X=E=q=qdot=0 initial
boundary data and prescribed Delta_A; not a primordial mode/Ward/DES result.
No CLASS or observational runs. Keep the archived 37-gate report untouched.
"""
from __future__ import annotations
import argparse,json,subprocess
from pathlib import Path
import sympy as s

LOCKS={
 "ge19/physics_gate/radiation_neutrino_finite_k_NLO_memory_source_20261121.py":
  "eb0bf46391bbce136a69e3d41f90f4b0d58a7ce9",
 "docs/ge19_20261119_exact_driven_X_E_constrained_source_bridge.md":
  "ebd1e7ae6c7221c1bbdc17a94409533a60c02c65",
 "ge19/physics_gate/action_to_class_scalar_matrix_20261111.py":
  "c90a3de0b71d0ef4e6664512e6e247cd44e27dd",
 "ge19/physics_gate/physical_baryon_Exp_leading_seed_20261121.py":
  "b58e4119a73a2d4a4a279e9a858177e99fbd95fb",
}
def source_locks(root):
 for path,expected in LOCKS.items():
  f=root/path
  if not f.is_file():raise RuntimeError("MISSING_SOURCE "+path)
  actual=subprocess.check_output(["git","hash-object",str(f)],
                                 cwd=root,text=True).strip()
  if actual!=expected:raise RuntimeError("SOURCE_CHANGED "+path+" "+actual)
 print("GE19_CAUSAL_ONSET_SOURCE_LOCKS_PASS",len(LOCKS),flush=True)

def calculate():
 h,k,w,omega,KB,C,eta=s.symbols("h k w omega K_B C eta",positive=True)
 a=s.Function("a")(h);Q=s.Function("Q")(h);H=s.Function("H")(h)
 X=s.Function("X")(h);E=s.Function("E")(h)
 c=s.Function("c")(h);D=s.Function("Delta")(h);q=s.Function("q")(h)
 ai,Qi,ci,Di,Hi=s.symbols("a_i Q_i c_i Delta_i H_i",positive=True)
 init={
  a.subs(h,0):ai,Q.subs(h,0):Qi,c.subs(h,0):ci,
  D.subs(h,0):Di,H.subs(h,0):Hi,
  q.subs(h,0):0,s.diff(q,h).subs(h,0):0,
  s.diff(q,h,2).subs(h,0):0,
  X.subs(h,0):0,s.diff(X,h).subs(h,0):ci*Di,E.subs(h,0):0,
 }
 acc=-3*H*s.diff(q,h)-omega**2*q+omega*s.sqrt(w)*k*Q*X/a
 jerk0=s.factor(s.diff(acc,h).subs(h,0).subs(init))
 def value(expr):return s.factor(expr.subs(h,0).subs(init))
 bdel=-a*omega*s.sqrt(w)*q/k
 def bjet(order):
  expr=s.diff(bdel,h,order)
  return s.factor(value(expr).subs(s.diff(q,h,3).subs(h,0),jerk0))
 wb,m2=s.symbols("W_b M_2",positive=True)
 # Independent, correctly graded free-streaming neutrino octupole equation.
 R,P,t=s.symbols("R_nu Psi0 tau",positive=True)
 xx=k*t
 sigma2=P/s.Integer(15)
 sigma4=-P*(56*R+295)/(1890*(2*R+25))
 sigma=sigma2*xx**2+sigma4*xx**4
 F3=2*P*xx**3/105
 oct_res=s.expand(s.diff(F3,t)-s.Rational(6,7)*k*sigma)
 missing_res=s.expand(-s.Rational(6,7)*k*sigma)
 wrong_res=s.expand(s.diff(-F3,t)-s.Rational(6,7)*k*sigma)
 get=lambda expr,power:s.factor(s.expand(expr).coeff(k,power))
 dAi=-P*(15+4*R)*xx**2/40
 Binst1=wb*Qi*ci*Di
 Bdel3=-Qi*ci*Di*m2
 checks={
  "neutrino_octupole_CORRECT_k3_coefficient_zero":get(oct_res,3)==0,
  "neutrino_octupole_missing_F3_negative_control_nonzero":get(missing_res,3)!=0,
  "neutrino_octupole_wrong_sign_negative_control_nonzero":get(wrong_res,3)!=0,
  "neutrino_octupole_k5_remainder_declared_not_tested_as_k3":get(oct_res,5)!=0,
  "original_auxiliary_q_acceleration_initial_zero":value(acc)==0,
  "original_auxiliary_q_jerk_from_chidot":s.simplify(
    jerk0-omega*s.sqrt(w)*k*Qi*ci*Di/ai)==0,
  "retarded_Bdel_initial_zero":bjet(0)==0,
  "retarded_Bdel_first_derivative_zero":bjet(1)==0,
  "retarded_Bdel_second_derivative_zero":bjet(2)==0,
  "retarded_Bdel_third_derivative_nonzero":s.simplify(
    bjet(3)+w*omega**2*Qi*ci*Di)==0,
  "instantaneous_B_first_derivative":s.simplify(
    value(s.diff(wb*Q*X,h))-Binst1)==0,
  "positive_bath_m2_first_nonzero_ratio":s.simplify(
    Bdel3/(6*Binst1)+m2/(6*wb))==0,
  "late_E_eta_tangent_first_delayed_h4":s.simplify(
    -Qi*Bdel3/(4*KB*24)-Qi**2*ci*Di*m2/(96*KB))==0,
  "zero_c_strict_dust_retarded_onset_zero":
    s.simplify(Bdel3.subs(ci,0))==0,
  "full_radiation_NLO_Delta_is_k2_tau2":s.simplify(
    dAi/xx**2+(15+4*R)*P/40)==0,
  "one_mode_positive_spectral_moment":s.simplify(w*omega**2).is_positive,
  "retarded_Bdel_opposes_Binst_early_time":
    s.simplify((Bdel3/(6*Binst1))).is_negative,
 }
 bad=[name for name,passed in checks.items() if not bool(passed)]
 if bad:raise RuntimeError("GE19_CAUSAL_ONSET_SYMBOLIC_FAIL "+repr(bad))
 return {
  "classification":"GE19_CORRECTED_F3_K3_AND_ACTION_CAUSAL_ONSET_JET_PASS_CONDITIONAL_NOT_FULL_PRIMORDIAL",
  "gate_count":len(checks),"gates":{key:bool(value) for key,value in checks.items()},
  "old_37_gate_octupole_audit":"Legacy neutrino_octupole_F3_evolution_k4 checked an identically absent k^4 coefficient; this audit corrects it to k^3 and includes missing-F3/wrong-sign negative controls. Archived r1 retained unchanged.",
  "leading_input_DeltaA":"Delta_A=-(15+4R_nu)*Psi0*(k*tau)^2/40 in zero-matter-fraction radiation test-fluid limit",
  "selected_initial_state":"At finite regular ti assume X=E=qj=qdotj=0, smooth background and Delta_A(ti)=D_i; this finite-ti zero bath assumption is NOT implied by no-free-bath history from earlier times.",
  "Xdot_ti":"c_i*Delta_i",
  "Edot_ti":"-C*Q_i*c_i*Delta_i/K_B",
  "qddot_ti":"0",
  "qjerk_ti":"omega_j*sqrt(w_j)*k*Q_i*c_i*Delta_i/a_i",
  "spectral_moments":"W_b=sum_j w_j >0, M_2=sum_j w_j*omega_j**2 >0",
  "Binstant_early":"W_b*Q_i*c_i*Delta_i*(t-ti)+O((t-ti)**2)",
  "Bdelayed_early":"-Q_i*c_i*Delta_i*M_2*(t-ti)**3/6+O((t-ti)**4)",
  "Bdelayed_over_Binstant_early":"-M_2*(t-ti)**2/(6*W_b)+O((t-ti)**3) provided c_i*Delta_i!=0",
  "E_eta_tangent_delayed_early":"Q_i**2*c_i*Delta_i*M_2*(t-ti)**4/(96*K_B)+O((t-ti)**5) in the source-only linear tangent, zero IC",
  "scope":"Reduced original action source-jet at finite ti; NOT full Einstein + AeST + photon/baryon/neutrino mixed O(y_m*(k*tau)^2) growing mode, not Ward-certified, not DES.",
  "full_physics_GO":False,"DES_detection":False
 }
def main():
 ap=argparse.ArgumentParser()
 ap.add_argument("--repo-root",type=Path,default=Path(__file__).resolve().parents[2])
 ap.add_argument("--self-test",action="store_true")
 ap.add_argument("--out",type=Path)
 a=ap.parse_args()
 if not a.self_test:source_locks(a.repo_root.resolve())
 result=calculate()
 print("GE19_CORRECTED_OCTUPOLE_AND_CAUSAL_ONSET_PASS",result["gate_count"],flush=True)
 print("GE19_FULL_PHYSICS_GO False",flush=True)
 if a.out:
  target=a.out.resolve()
  if target.exists():raise RuntimeError("REFUSE_OVERWRITE "+str(target))
  target.parent.mkdir(parents=True,exist_ok=True)
  target.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
  print("GE19_CAUSAL_ONSET_REPORT",target,flush=True)
 elif a.self_test:print(json.dumps(result,indent=2,sort_keys=True))
if __name__=="__main__":main()
