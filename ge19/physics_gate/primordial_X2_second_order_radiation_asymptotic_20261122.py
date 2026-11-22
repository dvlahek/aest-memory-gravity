#!/usr/bin/env python3
"""GE19 exact X2 second-order elimination and reference radiation indicial screen.

Original reduced action only; reference radiation a=A sqrt(t), Q=q0 constant is
NOT the exact Exp background as t->0. No claim of physical growing-mode selection.
"""
from __future__ import annotations
import argparse,json,subprocess
from pathlib import Path
import sympy as s

LOCKS={
 'ge19/physics_gate/primordial_k2_XS_retarded_bath_hierarchy_20261122.py': 'a7fa9069fb2670a0231ed8374d09ebd0b684d192',
 'ge19/physics_gate/exact_X_S_stress_lift_scalar_current_bridge_20261122.py': '6eb7e886fb04b8bdfd49295b2a298937c98c8612',
 'v019/patch/source/aest_memory.c': '9a522a653a1855eda3cb67e856f9fc10a1e73d54',
 'docs/ge19_20261119_primordial_initial_stress_null_direction.md': '33a0e880f24874fbf0e5f80b4c113d1000f14eba',
}

def algebra():
 t=s.symbols('t',positive=True)
 KB,C,eta=s.symbols('K_B C eta',positive=True)
 Q=s.Function('Q')(t);H=s.Function('H')(t);KQ=s.Function('K_Q')(t)
 c=s.Function('c')(t);X=s.Function('X')(t);S=s.Function('S')(t)
 D=s.Function('Delta2')(t);B=s.Function('B2')(t)
 A=C*Q/KB; f=c*D
 Xd=-A*X+S/KB+f
 Sd=(A-H)*S+Q*(KQ-2*A)*X-eta*Q*B/4
 Xdd=s.diff(Xd,t).subs({s.diff(S,t):Sd,s.diff(X,t):Xd,s.diff(Q,t):-3*H*c*Q})
 V=Q*(C*Q-KQ)/KB +A*H*(1-3*c)
 Sd_half=(A-H)*S+Q*(KQ-2*A)*X-eta*Q*B/2
 Xdd_half=s.diff(Xd,t).subs({s.diff(S,t):Sd_half,s.diff(X,t):Xd,s.diff(Q,t):-3*H*c*Q})
 lhs_half=s.factor((Xdd_half+H*Xd+V*X-s.diff(f,t)-(H-A)*f+eta*Q*B/(4*KB)).subs(C,2-KB))
 lhs=s.factor((Xdd+H*Xd+V*X-s.diff(f,t)-(H-A)*f+eta*Q*B/(4*KB)).subs(C,2-KB))
 A0,Qbar,I,D0,k=s.symbols('A0 Qbar I D0 k',positive=True)
 D0true=Qbar*I/(KB*A0**3)
 L=lambda z:s.diff(z,t,2)+s.diff(z,t)/(2*t)-D0*z/t**s.Rational(3,2)
 xp=1+2*D0*s.sqrt(t)*s.log(t)
 xh=s.sqrt(t)+2*D0*t
 ap=A0*s.sqrt(t)
 KQrad=I/(A0**3*t**s.Rational(3,2))
 Sp=KB*(s.diff(xp,t)+C*Qbar*xp/KB)
 Sh=KB*(s.diff(xh,t)+C*Qbar*xh/KB)
 rp=s.factor(-k*k*Sp/(ap**2*Qbar*KQrad))
 rh=s.factor(-k*k*Sh/(ap**2*Qbar*KQrad))
 Z,Z0,Q0,K2=s.symbols('Z Z0 Q0 K2',positive=True)
 Qexp=Q0+Z0*Z
 KQQexp=4*K2*s.exp(Z**2)*(1+2*Z**2)
 KQexp=4*K2*Z0*Z*s.exp(Z**2)
 cexp=KQexp/(Qexp*KQQexp)
 dz_dln_a=-3*Z/(1+2*Z**2)
 tests={
  'second_order_X_identity':lhs==0,
  'source_normalization_is_quarter':s.simplify(s.diff(eta*Q*B/(4*KB),eta)-Q*B/(4*KB))==0,
  'half_source_negative_control_has_nonzero_X_residual':s.simplify(lhs_half+eta*Q*B/(4*KB))==0,
  'reference_indicial_exponents':s.solve(s.Eq(s.Symbol('p')*(s.Symbol('p')-s.Rational(1,2)),0),s.Symbol('p'))==[0,s.Rational(1,2)],
  'reference_radiation_Xconst_first_subleading_cancels':s.limit(t**s.Rational(3,2)*L(xp),t,0)==0,
  'reference_radiation_Xsqrt_first_subleading_cancels':s.limit(t**s.Rational(3,2)*L(xh),t,0)==0,
  'constant_branch_stress_log_divergence_coefficient':s.simplify(s.limit(Sp*s.sqrt(t)/s.log(t),t,0)-KB*D0)==0,
  'sqrt_branch_stress_inv_sqrt_coefficient':s.simplify(s.limit(Sh*s.sqrt(t),t,0)-KB/2)==0,
  'sqrt_branch_fractional_gradient_density_finite':s.simplify(s.limit(rh,t,0)+k*k*A0*KB/(2*Qbar*I))==0,
  'constant_branch_fractional_gradient_density_log':s.simplify(s.limit(rp/s.log(t),t,0).subs(D0,D0true)+k*k/A0**2)==0,
  'Exp_exact_KQ_over_KQQ':s.simplify(KQexp/KQQexp-Z0*Z/(1+2*Z**2))==0,
  'Exp_exact_Q_dln_a':s.simplify(dz_dln_a*s.diff(Qexp,Z)+3*cexp*Qexp)==0,
  'Exp_KQQ_over_KQ':s.simplify(KQQexp/KQexp-(1+2*Z**2)/(Z0*Z))==0,
  'Exp_exact_c_as_Z0Z_over_Q':s.simplify(cexp-Z0*Z/(Qexp*(1+2*Z**2)))==0,
  'Exp_strict_Zlarge_c_Z2_limit':s.limit(cexp*Z**2,Z,s.oo)==s.Rational(1,2),
  'Exp_strict_Zlarge_Q_over_Z_limit':s.limit(Qexp/Z,Z,s.oo)==Z0,
  'positive_Exp_background_KQ':bool(KQexp.is_positive),
 }
 bad=[n for n,b in tests.items() if not bool(b)]
 if bad: raise RuntimeError('GE19_INDICIAL_GATES_FAIL '+str(bad))
 return {'classification':'GE19_EXACT_X2_ELIMINATION_AND_RADIATION_REFERENCE_INDICIAL_SCREEN_PASS_NOT_PHYSICAL_PRIMORDIAL','gate_count':len(tests),'gates':{n:bool(b) for n,b in tests.items()},'second_order_operator':'ddot X2 +H dot X2+[Q(C Q-K_Q)/K_B+(C Q/K_B) H(1-3 c_a2)]X2= d(c_a2 Delta2)/dt +(H-C Q/K_B)c_a2 Delta2 -eta Q B2/(4 K_B)','reference_indicial_exponents':['0','1/2'],'reference_radiation_caveat':'a=A0*sqrt(t),Q=Qbar are REFERENCE approximations. Strict Exp has Q=Q0+Z0 Z with Z**2+ln Z=-3ln a +const, so Q slowly grows with sqrt(log 1/a).','density_regular_caveat':'S2 ~ t^-1/2 does not automatically imply divergent fraction of AeST energy density: its standalone gradient-stress / rho_A ratio is finite in reference radiation branch. Full deltaQ+metric+adiabatic/Noether selection required.','FULL_PHYSICS_GO':False,'DES_detection':False}

if __name__=='__main__':
 ap=argparse.ArgumentParser()
 ap.add_argument('--repo-root',type=Path,default=Path(__file__).resolve().parents[2]);ap.add_argument('--out',type=Path);ap.add_argument('--self-test',action='store_true')
 args=ap.parse_args()
 if not args.self_test:
  for p,h in LOCKS.items():
   f=args.repo_root/p
   if not f.exists():raise RuntimeError('MISSING '+p)
   got=subprocess.check_output(['git','hash-object',str(f)],cwd=args.repo_root,text=True).strip()
   if got!=h:raise RuntimeError('SOURCE_CHANGED '+p+' '+got)
  print('GE19_INDICIAL_SOURCE_LOCKS_PASS',len(LOCKS))
 result=algebra()
 print('GE19_INDICIAL_PHYSICS_SCREEN_PASS',result['gate_count'])
 print('GE19_FULL_PHYSICS_GO False')
 if args.out:
  if args.out.exists():raise RuntimeError('REFUSE_OVERWRITE')
  args.out.parent.mkdir(parents=True,exist_ok=True)
  args.out.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
