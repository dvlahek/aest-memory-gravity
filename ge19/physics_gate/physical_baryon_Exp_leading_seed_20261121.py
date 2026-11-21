#!/usr/bin/env python3
"""GE19: coupled photon-baryon-neutrino-dustlike AeST O(y) seed and
uniform frozen Exp EOS bounds. Leading k*tau, not full physical finite-k mode.
"""
from __future__ import annotations
import argparse,json,subprocess
from pathlib import Path
import sympy as s

SOURCE_BLOBS={
 'v019/patch/source/aest_memory.c':'9a522a653a1855eda3cb67e856f9fc10a1e73d54',
 'v019/ini/aest_exp.ini':'f9a2bde8921a148e063f9657a8ede0a51c6a629d',
 'ge19/physics_gate/coupled_radiation_aest_leading_backreaction_20261120.py':
   '437328edc2894d2d8f7216403a38c79294213981',
}
def source_locks(root):
 for path,expected in SOURCE_BLOBS.items():
  got=subprocess.check_output(['git','hash-object',str(root/path)],cwd=root,text=True).strip()
  if got!=expected:raise RuntimeError('GE19_SOURCE_CHANGED '+path+' '+got)
 print('GE19_BARYON_EXP_SOURCE_LOCKS_PASS',len(SOURCE_BLOBS),flush=True)

def algebra():
 yA,yb,R,P,k,t=s.symbols('y_A y_b R_nu Psi0 k tau',positive=True)
 y=yA+yb
 zz={yA:0,yb:0}
 def Dt(ex):return s.diff(ex,t)+(yA*s.diff(ex,yA)+yb*s.diff(ex,yb))/t
 def linear_zero(ex):
  return all(s.simplify(v)==0 for v in [
   ex.subs(zz),s.diff(ex,yA).subs(zz),s.diff(ex,yb).subs(zz)])
 F=-P*(15+16*R)/(16*(15+2*R))
 G=P*(40*R-15)/(16*(15+2*R))
 Phi=P*(1+2*R/s.Integer(5))+F*y
 Psi=P+G*y
 H=(1+y/s.Integer(4))/t
 Ar=(1-y/s.Integer(2))/t**2
 AA=yA/t**2
 Ab=yb/t**2
 dg=-2*P+4*F*y
 dn=dg
 dA=-s.Rational(3,2)*P+3*F*y
 db=dA
 thpb=k*k*t*(P/s.Integer(2)+(F+G)*y/s.Integer(2))
 thnu=thpb
 thA=k*k*t*(P/s.Integer(2)+(G-P/s.Integer(8))*y/s.Integer(3))
 sigmanu=k*k*t*t*(P/s.Integer(15)+2*(F+G)*y/45)
 Rb=s.Rational(3,4)*yb/(1-R)
 Ham=3*H*(Dt(Phi)+H*Psi)+s.Rational(3,2)*(Ar*dg+AA*dA+Ab*db)
 Mom=Dt(Phi)+H*Psi-s.Rational(3,2)/k**2*(
    s.Rational(4,3)*Ar*((1-R)*thpb+R*thnu)+AA*thA+Ab*thpb)
 Shear=Phi-Psi-6*R*Ar*sigmanu/k**2
 Trace=Dt(Dt(Phi))+H*(Dt(Psi)+2*Dt(Phi))+(2*Dt(H)+H**2)*Psi-s.Rational(1,2)*Ar*dg
 EulerPB=Dt(thpb)+H*Rb/(1+Rb)*thpb-k*k*(dg/(4*(1+Rb))+Psi)
 EulerNu=Dt(thnu)-k*k*(dn/4+Psi)
 EulerA=Dt(thA)+H*thA-k*k*Psi
 Quad=Dt(sigmanu)-s.Rational(4,15)*thnu
 checks={
  'combined_first_order_Friedmann':linear_zero(t*t*(H**2-Ar-AA-Ab)),
  'combined_first_order_Raychaudhuri':linear_zero(t*t*(Dt(H)+Ar+(AA+Ab)/2)),
  'Einstein_Hamiltonian_yA_yb':linear_zero(t*t*Ham),
  'Einstein_momentum_yA_yb':linear_zero(t*Mom),
  'Einstein_anisotropic_shear_yA_yb':linear_zero(Shear),
  'Einstein_spatial_pressure_trace_yA_yb':linear_zero(t*t*Trace),
  'photon_baryon_tight_coupling_euler':linear_zero(EulerPB/k**2),
  'free_streaming_neutrino_leading_euler':linear_zero(EulerNu/k**2),
  'aest_like_dust_euler':linear_zero(EulerA/k**2),
  'free_streaming_neutrino_leading_quadrupole':linear_zero(Quad/(k**2*t)),
  'photon_continuity_k0':linear_zero(t*(Dt(dg)-4*Dt(Phi))),
  'neutrino_continuity_k0':linear_zero(t*(Dt(dn)-4*Dt(Phi))),
  'baryon_continuity_k0':linear_zero(t*(Dt(db)-3*Dt(Phi))),
  'aest_continuity_k0':linear_zero(t*(Dt(dA)-3*Dt(Phi))),
  'baryon_photon_adiabatic_entropy_zero':linear_zero(db-s.Rational(3,4)*dg),
  'aest_photon_adiabatic_entropy_zero':linear_zero(dA-s.Rational(3,4)*dg),
  'photon_neutrino_density_equality':linear_zero(dg-dn),
  'photon_neutrino_leading_velocity_equality':linear_zero((thpb-thnu)/(k*k*t)),
  'aest_comoving_density_cancels_at_k0':linear_zero(dA+3*H*thA/(k*k)),
  'photon_comoving_density_cancels_at_k0':linear_zero(dg+4*H*thpb/(k*k)),
  'neutrino_comoving_density_cancels_at_k0':linear_zero(dn+4*H*thnu/(k*k)),
  'baryon_comoving_density_cancels_at_k0':linear_zero(db+3*H*thpb/(k*k)),
  'baryon_loading_leading_drag_pressure_cancellation':
   linear_zero((-H*Rb*thpb-Rb*k*k*dg/4)/k**2),
  'equal_matter_potential_coefficient_AeST_baryons':
   s.simplify(s.diff(Phi,yA)-s.diff(Phi,yb))==0 and
   s.simplify(s.diff(Psi,yA)-s.diff(Psi,yb))==0,
  'no_neutrino_Phi_limit':s.simplify((F/P).subs(R,0)+s.Rational(1,16))==0,
  'no_neutrino_Psi_limit':s.simplify((G/P).subs(R,0)+s.Rational(1,16))==0,
 }
 Z,Q0,Z0,K2=s.symbols('Z Q0 Z0 K2',positive=True)
 Q=Q0+Z0*Z
 K=2*K2*Z0**2*(s.exp(Z**2)-1)
 KQ=4*K2*Z0*Z*s.exp(Z**2)
 KQQ=4*K2*s.exp(Z**2)*(1+2*Z**2)
 w=K/(Q*KQ-K)
 c=KQ/(Q*KQQ)
 wstable=Z0*(1-s.exp(-Z**2))/(2*Q0*Z+Z0*(2*Z**2-1+s.exp(-Z**2)))
 cstable=Z0*Z/((Q0+Z0*Z)*(1+2*Z**2))
 checks.update({
  'Exp_w_from_original_K':s.simplify(w-wstable)==0,
  'Exp_c_a2_from_original_K':s.simplify(c-cstable)==0,
  'Exp_positive_energy_background_identity':
    s.simplify(Q*KQ-K-2*K2*Z0*s.exp(Z**2)*(
      2*Q0*Z+Z0*(2*Z**2-1+s.exp(-Z**2))))==0,
  'Exp_c_a2_derivative_maximum':
    s.simplify(s.diff(Z/(1+2*Z**2),Z)-(1-2*Z**2)/(1+2*Z**2)**2)==0,
  'Exp_dwdlna_background_identity':
    s.simplify(-3*KQ/(Z0*KQQ)*s.diff(w,Z)+3*(1+w)*(c-w))==0,
 })
 checks={n:bool(v) for n,v in checks.items()}
 failed=[n for n,v in checks.items() if not v]
 if failed:raise RuntimeError('GE19_BARYON_EXP_SYMBOLIC_FAIL '+str(failed))
 return {
  'classification':'GE19_PHOTON_BARYON_NEUTRINO_AESTLIKE_LEADING_MATTER_FEEDBACK_AND_EXP_BACKGROUND_UNIFORM_BOUNDS_PASS_NOT_FULL_PHYSICS',
  'symbolic_gates':checks,'gate_count':len(checks),
  'expansion':'y_m=y_A+y_b=(rho_A+rho_b)/rho_r <<1, k*tau <<1, tight coupling, free-streaming neutrinos; AeST dustlike stress leading only',
  'Phi0_over_Psi0':str(s.factor((Phi-F*y)/P)),
  'Phi_y_m_over_Psi0':str(s.factor(F/P)),
  'Psi_y_m_over_Psi0':str(s.factor(G/P)),
  'baryon_loading':'R_b=3*rho_b/(4*rho_gamma)=3*y_b/[4*(1-R_nu)]; pressure/inertia O(y_b) cancel in photon-baryon Euler at leading k*tau',
  'comoving_density_seed':'Delta_A=delta_A+3*Hcal*theta_A/k²=0 and Delta_gamma,nu,b=0 through O(y_A,y_b) at leading k*tau; first nonzero finite-k source F requires O(k²*tau²) NLO',
  'frozen_Exp_parameters':{'Q0':1e-4,'Z0':1e-17,'K2':9500,'K_B':0.1},
  'valid_Exp_branch':'Z>0 where K_Q=I0/a^3>0 and Q0,Z0,K2>0',
  'Exp_w':'Z0*(1-exp(-Z**2))/[2*Q0*Z+Z0*(2*Z**2-1+exp(-Z**2))]',
  'Exp_c_a2':'Z0*Z/[(Q0+Z0*Z)*(1+2*Z**2)]',
  'proven_uniform_w_bound':'0<=w_A<Z0/(2*Q0)=5e-14; 1-exp(-Z**2)<=min(Z**2,1)',
  'proven_uniform_c_a2_bound':'0<=c_a2<=Z0/(2*sqrt(2)*Q0)=3.5355339059327378e-14',
  'historical_dust_IC_entropy_bound':'|S_Agamma|<=3.75e-14*|4*Hcal*alpha-d_gamma_sync| if old dust IC used',
  'background_dust_density_bound':'|ln[(rho_A*a**3)(af)/(rho_A*a**3)(ai)]|<=3*(5e-14)*ln(af/ai), af>=ai>0',
  'warning':'Background w,c bounds DO NOT bound perturbation c*k*k*S_A/(a*a*R_A), finite-k Ward, true action-normalized growing eigenvector, retarded memory or observed Weyl.',
  'full_physics_GO':False,'DES_detection':False,
 }

def main():
 p=argparse.ArgumentParser()
 p.add_argument('--repo-root',type=Path,default=Path(__file__).resolve().parents[2])
 p.add_argument('--self-test',action='store_true')
 p.add_argument('--out',type=Path)
 opt=p.parse_args()
 if not opt.self_test:source_locks(opt.repo_root.resolve())
 report=algebra()
 print('GE19_BARYON_EXP_LEADING_COUPLED_SYMBOLIC_PASS',report['gate_count'],flush=True)
 print('GE19_FULL_PHYSICS_GO False',flush=True)
 if opt.out:
  target=opt.out.resolve()
  if target.exists():raise RuntimeError('REFUSE_OVERWRITE '+str(target))
  target.parent.mkdir(parents=True,exist_ok=True)
  target.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
  print('GE19_BARYON_EXP_REPORT',target,flush=True)
 elif opt.self_test:print(json.dumps(report,indent=2,sort_keys=True))
if __name__=='__main__':main()
