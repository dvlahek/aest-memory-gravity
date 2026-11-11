#!/usr/bin/env python3
"""GE19: radiation+neutrino O((k tau)^2) comoving AeST source.

Exact symbolic truncated expansion in flat Newtonian gauge.
Treat AeST as a TEST perfect dustlike component to leading c_a^2 and rho_A/rho_r;
use the separately derived first-onset equation to source memory.
NOT a finite-k Einstein-AeST-NL0B solution and NOT a CLASS run.
"""
import argparse,json,subprocess
from pathlib import Path
import sympy as s

LOCKS={
 'ge19/physics_gate/first_retarded_memory_onset_20261111.py':'9c41778234a734643d2527ff539d5fdb255bd66a',
 'ge19/physics_gate/frozen_exp_superhorizon_growing_mode_20261111.py':'e0a2562b2c728c1deef2eadb784f6c750aeef3b7',
 'v019/patch/source/aest_memory.c':'9a522a653a1855eda3cb67e856f9fc10a1e73d54'
}
def lock(root):
 for name,expected in LOCKS.items():
  path=root/name
  if not path.is_file():raise RuntimeError('SOURCE_MISSING '+name)
  actual=subprocess.check_output(['git','hash-object',str(path)],cwd=root,text=True).strip()
  if actual!=expected:raise RuntimeError('SOURCE_CHANGED '+name+' '+actual)
 print('GE19_RADIATION_SOURCE_LOCKS_PASS',len(LOCKS),flush=True)

def exact_source():
 R,P=s.symbols('R_nu Psi_0',real=True)
 f2,g2,tg3,tn3,s4=s.symbols('Phi_2 Psi_2 theta_g3 theta_nu3 sigma_nu4',real=True)
 f0=(1+s.Rational(2,5)*R)*P
 sigma2=P/s.Integer(15)
 Fnu3_3=s.Rational(2,7)*sigma2
 density2=-P/s.Integer(3)+4*f2
 # Newtonian gauge: photon/neutrino continuity+Euler, Boltzmann F2/F3,
 # Einstein momentum+traceless shear+Hamiltonian at the first nontrivial order.
 equations={
  'photon_Euler':3*tg3-density2/4-g2,
  'neutrino_Euler':3*tn3-density2/4+sigma2-g2,
  'neutrino_quadrupole':s4-tn3/15+s.Rational(3,40)*Fnu3_3,
  'Einstein_momentum':2*f2+g2-2*((1-R)*tg3+R*tn3),
  'Einstein_shear':f2-g2-6*R*s4,
  'Einstein_Hamiltonian':12*f2+3*g2+f0-P/2,
 }
 sol=s.solve(list(equations.values()),[f2,g2,tg3,tn3,s4],dict=True)
 if len(sol)!=1:raise RuntimeError('NONUNIQUE_RADIATION_SYSTEM')
 sol=sol[0]
 # Test dustlike separately conserved AeST driven by the metric, not backreacting
 # to the radiation at zeroth order in rho_A/rho_r:
 # delta_A=-3Psi0/2+(3Phi2-Psi0/4)x^2,
 # theta_A=k[Psi0*x/2+(Psi2/4)x^3], x=k tau.
 delta2=s.factor(3*sol[f2]-P/4)
 theta3=s.factor(sol[g2]/4)
 comoving2=s.factor(delta2+3*theta3)
 target=-(15+4*R)*P/40
 checks={
  'unique_radiation_neutrino_solution':len(sol)==5,
  'six_radiation_equations_exact':all(s.simplify(e.subs(sol))==0 for e in equations.values()),
  'neutrino_leading_slip':s.simplify(f0-P-6*R*sigma2)==0,
  'neutrino_octupole_coefficient':s.simplify(Fnu3_3-s.Rational(2,7)*sigma2)==0,
  'comoving_AeST_dust_order_x2':s.simplify(comoving2-target)==0,
  'no_neutrino_limit':s.simplify(comoving2.subs(R,0)+s.Rational(3,8)*P)==0,
  'all_radiation_limit':s.simplify(comoving2.subs(R,1)+s.Rational(19,40)*P)==0,
  'density_velocity_full_comoving_combination':s.simplify(comoving2-(delta2+3*theta3))==0,
  'source_vanishes_superhorizon_leading':s.simplify(target.subs(P,0))==0,
 }
 if not all(checks.values()):raise RuntimeError('SYMBOLIC_GATES_FAILED')
 return checks,{
  'Phi_2_over_Psi0':str(s.factor(sol[f2]/P)),
  'Psi_2_over_Psi0':str(s.factor(sol[g2]/P)),
  'Delta_A_order_(k_tau)^2_over_Psi0':str(s.factor(comoving2/P)),
  'chi_dot_at_initial_from_source': '-Q*c_a2*(15+4*R_nu)*Psi0*(k*tau_i)^2/40',
  'assumed_primordial_state':'single adiabatic growing mode, zero free bath q/p',
  'neglected_orders':['rho_A/rho_rad','rho_b/rho_rad','c_a2 corrections to Delta_A','higher (k tau) powers']}

def main():
 ap=argparse.ArgumentParser()
 ap.add_argument('--repo-root',type=Path,default=Path(__file__).resolve().parents[2])
 ap.add_argument('--no-source-lock',action='store_true')
 ap.add_argument('--out',type=Path)
 a=ap.parse_args()
 if not a.no_source_lock:lock(a.repo_root.resolve())
 gates,values=exact_source()
 report={'classification':'GE19_RADIATION_NEUTRINO_DELTA_A_FIRST_SOURCE_CLOSED_REDUCED_NOT_PHYSICS_GO',
  'scope':'radiation-dominated flat Newtonian, leading in dustlike AeST and rho_A/rho_rad, through x^2 only',
  'source_locks_executed':not a.no_source_lock,
  'source_blobs':LOCKS if not a.no_source_lock else {},
  'symbolic_gates':gates,'identity_count':len(gates),'result':values,
  'full_AeST_bath_finite_k_solution':False,
  'finite_eta_transfers_computed':False,'physical_weyl_observer_ready':False,
  'DES_detection':False,'production_physics_go':False}
 print('GE19_RADIATION_DELTA_SOURCE_PASS',len(gates),flush=True)
 print('GE19_FULL_PHYSICS_GO False',flush=True)
 if a.out:
  p=a.out.expanduser().resolve()
  if p.exists():raise RuntimeError('REFUSE_OVERWRITE')
  p.parent.mkdir(parents=True,exist_ok=True)
  p.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
  print('GE19_RADIATION_DELTA_REPORT',p,flush=True)
if __name__=='__main__':main()
