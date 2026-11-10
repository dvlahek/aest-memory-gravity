#!/usr/bin/env python3
"""Bounded GE19 LW28 restricted reduced-action momentum and source-coefficient proof.

No CLASS, no survey data. This cannot certify full 3+1 AeST+Y or an observation.
"""
import json
import sympy as s

N,L,R,b,u,pt,px,ut,ux,Nx,Lt,Lx,bx,qt,qx,q = s.symbols(
    'N L R b u pt px ut ux Nx Lt Lx bx qt qx q', real=True)
a,Q,H,eps,pdx = s.symbols('a Q H eps pdx', positive=True, real=True)
KB,C,KQ,eta,omega,sw = s.symbols('KB C KQ eta omega sw', real=True)
k,B,gamma,Ddot,Edot,Chidot = s.symbols('k B gamma Ddot Edot Chidot',real=True, nonzero=True)
ch,sh=s.cosh(u),s.sinh(u)
sigma=(pt-b*px)/N
Qi=ch*sigma+sh*px/L
Xi=sh*sigma+ch*px/L
kL=(Lt-b*Lx-L*bx)/(N*L)
E=ch*((ut-b*ux)/N+Nx/(N*L))+sh*(kL+ux/L)
Aq=ch*(qt-b*qx)/N+sh*qx/L
K=s.Function('K')
analytic=N*L*R**2*(KB*E**2+2*C*E*Xi-C*Xi**2+2*K(Qi))
bath=N*L*R**2*eta*s.Rational(1,4)*(Aq**2-(omega*q-sw*Xi)**2)
# Relaxed FLRW with scalar spatial perturbation and arbitrary metric amplitude.
subs={N:1,L:a,R:a,b:0,u:0,pt:Q,px:eps*pdx,ut:0,ux:0,
      Nx:0,Lt:a*H,Lx:0,bx:0,qt:0,qx:0,q:0}
def coeff(expr):
    return s.simplify(s.diff(expr.subs(subs),eps).subs(eps,0).doit())
shift_analytic=coeff(s.diff(analytic,b)).subs(s.Derivative(K(Q),Q),KQ)
shift_bath=coeff(s.diff(bath,b))
shift_grad=coeff(s.diff(analytic+bath,bx))
rho=(Q*KQ-K(Q))/3
pressure=K(Q)/3
enthalpy=s.simplify(rho+pressure)
# Full reduced scalar-source compatibility at fixed state. The scalar flux
# has coefficient -eta B/2. All k factors are CLASS physical k.
scalar_source=s.Rational(6)*a**3*Ddot/Q+2*a*k*k*(KB*Edot+C*Chidot)/Q+a*k*k*B/2
E_dot_eta=-gamma*Q*B/KB
required_Ddot=s.solve(scalar_source.subs({Edot:E_dot_eta,Chidot:0}),Ddot)[0]
unique_gamma=s.solve(required_Ddot,gamma)[0]
checks={
  'exact_momentum_constraint_shift':s.simplify(shift_analytic+2*a**3*KQ*pdx)==0,
  'bath_direct_shift_first_order_zero':s.simplify(shift_bath)==0,
  'metric_shift_gradient_first_order_zero':s.simplify(shift_grad)==0,
  'enthalpy_QKQ_over_3':s.simplify(enthalpy-Q*KQ/3)==0,
  'momentum_per_enthalpy_phase_velocity':s.simplify(shift_analytic+6*a**3*enthalpy*pdx/Q)==0,
  'unique_scalar_charge_coefficient_one_quarter':unique_gamma==s.Rational(1,4),
  'action_one_quarter_does_not_require_density_source':s.simplify(required_Ddot.subs(gamma,s.Rational(1,4)))==0,
  'original_patch_one_half_requires_nonzero_density_source':s.simplify(required_Ddot.subs(gamma,s.Rational(1,2))-Q*k*k*B/(12*a*a))==0,
  'density_source_nonzero_for_old_patch':s.simplify(required_Ddot.subs(gamma,s.Rational(1,2)))!=0,
  'no_compensation_with_frozen_phase_dictionary':s.simplify((Q*B/(4*C)))!=0,
  'negative_wrong_shift_normalization':s.simplify(shift_analytic+3*a**3*KQ*pdx)!=0,
  'negative_no_scalar_bath_flux':s.simplify(s.solve(scalar_source-a*k*k*B/2,Ddot)[0].subs({Edot:-Q*B/(4*KB),Chidot:0}))!=0,
}
assert all(checks.values()),[k for k,v in checks.items() if not v]
out={
 'classification':'GE19_LW28_REDUCED_MOMENTUM_AND_SCALAR_CHARGE_SELECT_QUARTER_CONDITIONAL_FULL_3PLUS1_OPEN',
 'symbolic_gates':checks,
 'unique_reduced_action_eta_E_coefficient':str(unique_gamma),
 'old_patch_eta_E_coefficient':'1/2',
 'required_density_explicit_eta_source_general':str(s.factor(required_Ddot)),
 'required_density_explicit_eta_source_old_patch':str(s.factor(required_Ddot.subs(gamma,s.Rational(1,2)))),
 'momentum_shift':'-2*a**3*K_Q*partial_x(varphi)',
 'enthalpy':'Q*K_Q/3',
 'physical_eta_matter_Weyl_certified':False,
 'original_patch_changed':False,
 'CLASS_run':False,
 'observational_memory_detection':False,
 'scope':'exact reduced analytic GE06+GE05 scalar-longitudinal model, not full covariant Einstein-AeST-Y closure'
}
print('GE19_LW28_SYMBOLIC_PASS',len(checks))
print(json.dumps(out,indent=2,sort_keys=True))
