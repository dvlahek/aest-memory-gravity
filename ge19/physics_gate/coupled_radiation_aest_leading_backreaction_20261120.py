#!/usr/bin/env python3
"""GE19 leading photon+neutrino+dustlike-AeST joint gravity feedback.

First order y=rho_A/rho_r, k*tau->0, c_a²,w_A->0. Exactly 16 symbolic
gates. This is NOT the complete Einstein-AeST-NL0B primordial mode.
"""
from __future__ import annotations
import argparse,json,subprocess
from pathlib import Path
import sympy as sp

LOCKS={
 'ge19/physics_gate/radiation_neutrino_delta_source_20261111.py':
   '19e9efd5713dc8df3057c4b33f8c4a2921a96687',
 'ge19/physics_gate/primordial_pressureful_velocity_20261120.py':
   '849b74297a2293327956c548d53b5a802bb865d3',
 'ge19/physics_gate/constraint_projected_joint_operator_20261112.py':
   'b98bec1e1af46021d810676a062957d4efe80c58',
}

def source_locks(root):
 for path,blob in LOCKS.items():
  f=root/path
  if not f.is_file():raise RuntimeError('MISSING_SOURCE: '+path)
  got=subprocess.check_output(['git','hash-object',str(f)],cwd=root,text=True).strip()
  if got!=blob:raise RuntimeError('SOURCE_CHANGED: '+path+' '+got)
 print('GE19_RADIATION_BACKREACTION_SOURCE_LOCKS_PASS',len(LOCKS))

def symbolic():
 R,P,k,tau,y=sp.symbols('R_nu Psi0 k tau y',real=True,nonzero=True)
 Phi1,Psi1=sp.symbols('Phi1 Psi1',real=True)
 H=(1+y/sp.Integer(4))/tau
 a2rho_r=(1-y/sp.Integer(2))/tau**2
 a2rho_A=y/tau**2
 Phi0=(1+2*R/sp.Integer(5))*P
 Phi=Phi0+Phi1*y
 Psi=P+Psi1*y
 delta_r=-2*P+4*Phi1*y
 delta_A=-sp.Rational(3,2)*P+3*Phi1*y
 theta_r=k**2*tau*(P/2+(Phi1+Psi1)*y/2)
 theta_A=k**2*tau*(P/2+(Psi1-P/sp.Integer(8))*y/3)
 sigma_nu=k**2*tau**2*(P/sp.Integer(15)+2*(Phi1+Psi1)*y/45)
 def D(f):return sp.diff(f,tau)+y*sp.diff(f,y)/tau
 ham=3*H*(D(Phi)+H*Psi)+sp.Rational(3,2)*(a2rho_r*delta_r+a2rho_A*delta_A)
 mom=D(Phi)+H*Psi-sp.Rational(3,2)*(sp.Rational(4,3)*a2rho_r*theta_r+a2rho_A*theta_A)/k**2
 shear=Phi-Psi-6*R*a2rho_r*sigma_nu/k**2
 eq=[sp.expand(ham*tau**2).coeff(y,1),sp.expand(shear).coeff(y,1)]
 sols=sp.solve(eq,[Phi1,Psi1],dict=True)
 if len(sols)!=1:raise RuntimeError('BACKREACTION_NOT_UNIQUE')
 sol=sols[0]
 def through_y_zero(expr):
  ex=sp.expand(sp.cancel(expr.subs(sol)))
  return sp.simplify(ex.coeff(y,0))==0 and sp.simplify(ex.coeff(y,1))==0
 gates={
  'background_friedmann_through_y':through_y_zero(tau**2*(H**2-a2rho_r-a2rho_A)),
  'background_matter_fraction_first_order':through_y_zero(a2rho_A*tau**2-y),
  'adiabatic_density_entropy_through_y':through_y_zero(delta_A-sp.Rational(3,4)*delta_r),
  'neutrino_slip_radiation_leading':sp.simplify(Phi0-Psi-2*R*P/5).subs(y,0)==0,
  'photon_continuity_superhorizon_through_y':through_y_zero(tau*(D(delta_r)-4*D(Phi))),
  'dust_aest_continuity_superhorizon_through_y':through_y_zero(tau*(D(delta_A)-3*D(Phi))),
  'photon_euler_through_y':through_y_zero((D(theta_r)-k**2*(delta_r/4+Psi))/k**2),
  'dust_aest_euler_through_y':through_y_zero((D(theta_A)+H*theta_A-k**2*Psi)/k**2),
  'neutrino_shear_Boltzmann_through_y':through_y_zero((D(sigma_nu)-sp.Rational(4,15)*theta_r)/(k**2*tau)),
  'Einstein_Hamiltonian_k0_through_y':through_y_zero(tau**2*ham),
  'Einstein_momentum_through_y':through_y_zero(tau*mom),
  'Einstein_neutrino_traceless_shear_through_y':through_y_zero(shear),
  'unique_Phi_coefficient':sp.simplify(sol[Phi1]+P*(15+16*R)/(16*(15+2*R)))==0,
  'unique_Psi_coefficient':sp.simplify(sol[Psi1]-P*(40*R-15)/(16*(15+2*R)))==0,
  'no_neutrino_potential_limit_Phi':sp.simplify(sol[Phi1].subs(R,0)+P/16)==0,
  'no_neutrino_potential_limit_Psi':sp.simplify(sol[Psi1].subs(R,0)+P/16)==0,
 }
 gates={name:bool(val) for name,val in gates.items()}
 if not all(gates.values()):raise RuntimeError('SYMBOLIC_FAIL '+str([n for n,v in gates.items() if not v]))
 return {
  'classification':'GE19_COUPLED_RADIATION_NEUTRINO_DUSTLIKE_AEST_LEADING_Y_PASS_NOT_FULL_PHYSICS',
  'gates':gates,'gate_count':len(gates),
  'Phi0_over_Psi0':str(sp.factor(Phi0/P)),
  'Phi_y_over_Psi0':str(sp.factor(sol[Phi1]/P)),
  'Psi_y_over_Psi0':str(sp.factor(sol[Psi1]/P)),
  'model':'photons + free-streaming massless neutrinos + separately conserved pressureless AeST-like species',
  'expansion':'first order y=rho_A/rho_r, leading k*tau->0 and c_a2,w_A->0',
  'limitations':[
   'baryon-photon tight-coupling loading omitted',
   'true AeST pressureful Exp K(Q) dynamics omitted',
   'NL0B bath eta and retarded history omitted',
   'finite k²*tau² corrections not solved',
   'full scalar Ward and physical primordial eigenvector not proved',
   'physical delayed Weyl and DES transfer not proved'],
  'full_physics_GO':False,'DES_detection':False
 }

def main():
 pa=argparse.ArgumentParser()
 pa.add_argument('--repo-root',type=Path,default=Path(__file__).resolve().parents[2])
 pa.add_argument('--self-test',action='store_true')
 pa.add_argument('--out',type=Path)
 opt=pa.parse_args()
 if not opt.self_test:source_locks(opt.repo_root.resolve())
 report=symbolic()
 print('GE19_COUPLED_RADIATION_BACKREACTION_SYMBOLIC_PASS',report['gate_count'])
 print('GE19_FULL_PHYSICS_GO False')
 if opt.out:
  out=opt.out.resolve()
  if out.exists():raise RuntimeError('REFUSE_OVERWRITE '+str(out))
  out.parent.mkdir(parents=True,exist_ok=True)
  out.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
  print('GE19_COUPLED_RADIATION_REPORT',out)
 elif opt.self_test:print(json.dumps(report,indent=2,sort_keys=True))
if __name__=='__main__':main()
