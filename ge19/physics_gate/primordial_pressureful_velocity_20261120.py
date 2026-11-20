#!/usr/bin/env python3
"""Exact O(c_a^2) pressureful AeST primordial velocity audit in radiation test-fluid limit.

9 symbolic gates only; not a complete physical finite-k adiabatic mode or DES prediction.
"""
import argparse
import json
import subprocess
from pathlib import Path
import sympy as s

SOURCE_LOCKS = {
 'ge19/physics_gate/radiation_neutrino_delta_source_20261111.py': '19e9efd5713dc8df3057c4b33f8c4a2921a96687',
 'ge19/physics_gate/frozen_exp_superhorizon_growing_mode_20261111.py': 'e0a2562b2c728c1deef2eadb784f6c750aeef3b7',
 'docs/ge19_20261120_radiation_regular_aether_bath_leading_coefficients.md': 'd646c8482cbb443ffd886c867eabe9ffd8f068a3',
}

def verify_locks(root):
 for path, expected in SOURCE_LOCKS.items():
  file=root/path
  if not file.is_file(): raise RuntimeError('SOURCE_MISSING '+path)
  got=subprocess.check_output(['git','hash-object',str(file)],cwd=root,text=True).strip()
  if got!=expected: raise RuntimeError('SOURCE_CHANGED '+path+': '+got+' != '+expected)
 print('GE19_PRIMORDIAL_VELOCITY_SOURCE_LOCKS_PASS',len(SOURCE_LOCKS))

def calculate():
 R,P,k,tau,c=s.symbols('R_nu Psi0 k tau c',real=True)
 ph2,ps2,tg3,tn3,sn4=s.symbols('ph2 ps2 tg3 tn3 sn4')
 p0=(1+s.Rational(2,5)*R)*P
 sn2=P/15
 fn3=s.Rational(2,7)*sn2
 d2=-P/3+4*ph2
 equations=[
  3*tg3-d2/4-ps2,
  3*tn3-d2/4+sn2-ps2,
  sn4-tn3/15+s.Rational(3,40)*fn3,
  2*ph2+ps2-2*((1-R)*tg3+R*tn3),
  ph2-ps2-6*R*sn4,
  12*ph2+3*ps2+p0-P/2,
 ]
 sols=s.solve(equations,[ph2,ps2,tg3,tn3,sn4],dict=True)
 if len(sols)!=1: raise RuntimeError('RADIATION_SOLUTION_NOT_UNIQUE')
 sol=sols[0]
 ps2v=s.factor(sol[ps2]);ph2v=s.factor(sol[ph2])
 delta2=s.factor(3*ph2v-P/4)
 f=s.factor(-(15+4*R)*P/40)
 Psi=P+ps2v*k**2*tau**2
 theta_d=k**2*P*tau/2+ps2v*k**4*tau**3/4
 dnorm=-3*P/2+delta2*k**2*tau**2
 theta_c=s.factor(f*k**4*tau**3/4)
 theta=theta_d+c*theta_c
 # a~tau and Q'/Q=-3*c/tau. varphi=a*Q*theta/k²,
 # delta Q/Q=varphi'/(a*Q)-Psi.
 def phase(th):
  return (s.diff(th,tau)+th/tau)/k**2-Psi-3*c*th/(tau*k**2)
 # Original AeST pressureful effective-fluid Euler, pressure gradient S
 # neglected at retained joint O(c) and radiation-gradient order.
 def euler(th):
  return s.diff(th,tau)-(3*c-1)*th/tau-k**2*(c*dnorm+Psi)
 dust_density_error=s.factor((phase(theta_d)-c*dnorm)/c)
 corrected_phase_first=s.factor(s.diff(phase(theta)-c*dnorm,c).subs(c,0))
 delta_comov=s.factor(dnorm+3*theta/(tau*k**2))
 checks={
  'independent_six_equation_radiation_solution':all(s.simplify(eq.subs(sol))==0 for eq in equations),
  'archived_radiation_Delta_A':s.simplify(delta2+3*ps2v/4-f)==0,
  'dust_velocity_solves_zero_pressure_euler':s.simplify(euler(theta_d).subs(c,0))==0,
  'dust_velocity_action_density_error_equals_minus_f':s.simplify(dust_density_error+f*k**2*tau**2)==0,
  'nonzero_dust_action_error_for_generic_adiabatic_mode':s.simplify(dust_density_error)!=0,
  'pressureful_velocity_O_c_euler_consistent':s.simplify(s.diff(euler(theta),c).subs(c,0))==0,
  'pressureful_velocity_O_c_phase_action_consistent':corrected_phase_first==0,
  'corrected_comoving_source':s.simplify(delta_comov-f*(1+s.Rational(3,4)*c)*k**2*tau**2)==0,
  'X_source_cF_unchanged_to_first_order_c':s.simplify(s.diff(c*delta_comov-c*f*k**2*tau**2,c).subs(c,0))==0,
 }
 checks={name:bool(ok) for name,ok in checks.items()}
 if not all(checks.values()):
  raise RuntimeError('PHASE_VELOCITY_SYMBOLIC_FAIL '+str([n for n,ok in checks.items() if not ok]))
 return {
  'classification':'GE19_PRESSUREFUL_PRIMORDIAL_VELOCITY_CORRECTION_REDUCED_PASS_NOT_FULL_PHYSICS',
  'checks':checks,'gate_count':len(checks),
  'f_over_Psi0':str(s.factor(f/P)),
  'theta_c_per_c':str(theta_c),
  'strict_dust_action_density_error':str(dust_density_error),
  'corrected_comoving_Delta_A':str(delta_comov),
  'scope':'leading radiation+neutrino test-AeST geometry, linear in c=c_a², through (k*tau)^2 in Delta, Qprime/Q=-3c/tau',
  'pressure_gradient_S':'higher order under archived X/E proxy scaling, not certified in full mode',
  'complete_scalar_Ward_and_all_species_mode_proved':False,
  'physical_delayed_Weyl_transfer_proved':False,
  'DES_observability_ready':False
 }

def main():
 ap=argparse.ArgumentParser()
 ap.add_argument('--repo-root',type=Path,default=Path(__file__).resolve().parents[2])
 ap.add_argument('--skip-source-lock',action='store_true')
 ap.add_argument('--self-test',action='store_true')
 ap.add_argument('--out',type=Path)
 a=ap.parse_args()
 if not (a.skip_source_lock or a.self_test):
  verify_locks(a.repo_root.resolve())
 result=calculate()
 print('GE19_PRIMORDIAL_PRESSUREFUL_VELOCITY_SYMBOLIC_PASS',result['gate_count'])
 print('GE19_FULL_PHYSICS_GO False')
 if a.out:
  dest=a.out.resolve()
  if dest.exists(): raise RuntimeError('REFUSE_OVERWRITE '+str(dest))
  dest.parent.mkdir(parents=True,exist_ok=True)
  dest.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
  print('GE19_PRIMORDIAL_PRESSUREFUL_REPORT',dest)
 elif a.self_test:
  print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
