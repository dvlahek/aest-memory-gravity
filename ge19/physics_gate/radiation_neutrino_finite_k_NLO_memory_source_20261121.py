#!/usr/bin/env python3
"""GE19 radiation-era finite-k NLO seed + conditional strict-dust no-source theorem.

30 exact Einstein/Boltzmann/dust identities at O((k*tau)^2) for a zero-
background-fraction AeST-like test component, including neutrino F3 and
sigma to O((k*tau)^4); 7 exact reduced-action source tests.
NOT an O(y_m (k*tau)^2) coupled finite-k mode, Ward or memory detection.
"""
from __future__ import annotations
import argparse,json,subprocess
from pathlib import Path
import sympy as s

LOCKS={
 'ge19/physics_gate/physical_baryon_Exp_leading_seed_20261121.py':
  'b58e4119a73a2d4a4a279e9a858177e99fbd95fb',
 'ge19/physics_gate/radiation_neutrino_delta_source_20261111.py':
  '19e9efd5713dc8df3057c4b33f8c4a2921a96687',
 'docs/ge19_20261119_exact_driven_X_E_constrained_source_bridge.md':
  'ebd1e7ae6c7221c1bbdc17a94409533a60c02c65',
}
def locks(root):
 for path,expected in LOCKS.items():
  f=root/path
  if not f.is_file():raise RuntimeError('SOURCE_MISSING '+path)
  got=subprocess.check_output(['git','hash-object',str(f)],cwd=root,text=True).strip()
  if got!=expected:raise RuntimeError('SOURCE_CHANGED '+path+' '+got)
 print('GE19_FINITE_K_NLO_SOURCE_LOCKS_PASS',len(LOCKS),flush=True)

def solve():
 r,p,k,t=s.symbols('R_nu Psi0 k tau',positive=True)
 x=k*t
 Phi0=(1+2*r/s.Integer(5))*p
 Phi2=-p*(56*r**2+580*r+525)/(630*(2*r+25))
 Psi2=p*(56*r**2+10*r-525)/(630*(2*r+25))
 Phi=Phi0+Phi2*x**2
 Psi=p+Psi2*x**2
 delta2=4*Phi2-p/s.Integer(3)
 dg=-2*p+delta2*x**2
 dn=dg
 tg3=(Phi2+Psi2-p/s.Integer(12))/3
 tn3=(Phi2+Psi2-3*p/s.Integer(20))/3
 tg=k**2*t*(p/2+tg3*x**2)
 tn=k**2*t*(p/2+tn3*x**2)
 sigma2=p/s.Integer(15)
 f3c=2*p/s.Integer(105)
 sigma4=tn3/15-s.Rational(3,40)*f3c
 sigma=sigma2*x**2+sigma4*x**4
 F3=f3c*x**3
 da=-s.Rational(3,2)*p+(3*Phi2-p/4)*x**2
 ta=k**2*t*(p/2+Psi2*x**2/4)
 H=1/t
 dr=(1-r)*dg+r*dn
 th=(1-r)*tg+r*tn
 ham=k**2*Phi+3*H*(s.diff(Phi,t)+H*Psi)+s.Rational(3,2)*dr/t**2
 mom=s.diff(Phi,t)+H*Psi-2*th/(k**2*t**2)
 shear=Phi-Psi-6*r*sigma/(k**2*t**2)
 trace=(s.diff(Phi,t,2)+H*(s.diff(Psi,t)+2*s.diff(Phi,t))
        +(2*s.diff(H,t)+H**2)*Psi+k**2*(Phi-Psi)/3-dr/(2*t**2))
 def coeffzero(expr,power):return s.simplify(s.expand(expr).coeff(k,power))==0
 gates={
  'Einstein_Hamiltonian_leading':coeffzero(ham,0),
  'Einstein_Hamiltonian_k2':coeffzero(ham,2),
  'Einstein_momentum_leading':coeffzero(mom,0),
  'Einstein_momentum_k2':coeffzero(mom,2),
  'Einstein_shear_leading':coeffzero(shear,0),
  'Einstein_shear_k2_requires_neutrino_sigma4':coeffzero(shear,2),
  'Einstein_pressure_trace_leading':coeffzero(trace,0),
  'Einstein_pressure_trace_k2_with_slip':coeffzero(trace,2),
  'photon_continuity_k2':coeffzero(s.diff(dg,t)+s.Rational(4,3)*tg-4*s.diff(Phi,t),2),
  'neutrino_continuity_k2':coeffzero(s.diff(dn,t)+s.Rational(4,3)*tn-4*s.diff(Phi,t),2),
  'dustlike_A_continuity_k2':coeffzero(s.diff(da,t)+ta-3*s.diff(Phi,t),2),
  'photon_Euler_k2':coeffzero(s.diff(tg,t)-k**2*(dg/4+Psi),2),
  'photon_Euler_k4':coeffzero(s.diff(tg,t)-k**2*(dg/4+Psi),4),
  'neutrino_Euler_k2':coeffzero(s.diff(tn,t)-k**2*(dn/4+Psi-sigma),2),
  'neutrino_Euler_k4':coeffzero(s.diff(tn,t)-k**2*(dn/4+Psi-sigma),4),
  'dustlike_A_Euler_k2':coeffzero(s.diff(ta,t)+H*ta-k**2*Psi,2),
  'dustlike_A_Euler_k4':coeffzero(s.diff(ta,t)+H*ta-k**2*Psi,4),
  'neutrino_shear_evolution_k2':coeffzero(s.diff(sigma,t)-s.Rational(4,15)*tn+s.Rational(3,10)*k*F3,2),
  'neutrino_shear_evolution_k4':coeffzero(s.diff(sigma,t)-s.Rational(4,15)*tn+s.Rational(3,10)*k*F3,4),
  'neutrino_octupole_F3_evolution_k4':coeffzero(s.diff(F3,t)-s.Rational(6,7)*k*sigma,4),
  'neutrino_leading_gravity_slip':s.simplify(Phi0-p-6*r*sigma2)==0,
  'no_neutrino_Phi2_check':s.simplify(Phi2.subs(r,0)+p/30)==0,
  'no_neutrino_Psi2_check':s.simplify(Psi2.subs(r,0)+p/30)==0,
  'AeST_test_dust_delta_comoving_NLO':s.simplify(
    (da+3*H*ta/k**2)/x**2+(15+4*r)*p/40)==0,
  'photon_comoving_NLO':s.simplify(
    (dg+4*H*tg/k**2)/x**2+2*(4*r+15)*p/45)==0,
  'neutrino_comoving_NLO':s.simplify(
    (dn+4*H*tn/k**2)/x**2+2*(4*r+17)*p/45)==0,
  'Einstein_total_radiation_comoving_k2_constraint':s.simplify(
    (1-r)*(dg+4*H*tg/k**2)+r*(dn+4*H*tn/k**2)
    +s.Rational(2,3)*x**2*Phi0)==0,
  'neutrino_F3_coefficient':s.simplify(f3c-2*p/105)==0,
  'neutrino_sigma4_matches_gravity_slip':s.simplify(Phi2-Psi2-6*r*sigma4)==0,
  'Einstein_momentum_relation_unique':s.simplify(
    4*Phi2+Psi2+(s.Rational(1,6)+2*r/15)*p)==0,
 }
 C,KB,Q,KQ,Hc,c,eta,om,wb,ab,RA,X,E,q,D=s.symbols(
   'C KB Q KQ H c eta omega w_b a R_A X E q Delta_A',nonzero=True)
 F=D+k**2/(3*ab**2*RA)*(KB*E+C*Q*X)
 Bchi=wb*Q*X-ab*om*s.sqrt(wb)*q/k
 Xdot=E+c*F
 Edot=-Hc*E+Q/KB*((KQ-C*(Hc+Q-3*Hc*c))*X-C*c*F-eta*Bchi/4)
 zero={X:0,E:0,q:0}
 gates.update({
  'original_action_zero_state_X_forcing_is_c_DeltaA':
    s.simplify(Xdot.subs(zero)-c*D)==0,
  'original_action_zero_state_E_forcing_is_minus_CQc_DeltaA_over_KB':
    s.simplify(Edot.subs(zero)+C*Q*c*D/KB)==0,
  'strict_dust_zero_state_X_remains_zero':s.simplify(Xdot.subs(zero).subs(c,0))==0,
  'strict_dust_zero_state_E_remains_zero':s.simplify(Edot.subs(zero).subs(c,0))==0,
  'zero_scalar_state_has_zero_bath_force':s.simplify(Bchi.subs(zero))==0,
  'zero_scalar_state_has_zero_oscillator_drive':
    s.simplify(om*s.sqrt(wb)*k*Q*X/ab).subs(zero)==0,
  'leading_scalar_drive_linear_in_c':
    s.simplify(s.diff(Xdot.subs(zero),c)-D)==0,
 })
 gates={n:bool(v) for n,v in gates.items()}
 failed=[n for n,v in gates.items() if not v]
 if failed:raise RuntimeError('NLO_GATE_FAIL '+repr(failed))
 return {
  'classification':'GE19_FULL_RADIATION_NLO_FREE_STREAMING_NEUTRINO_TEST_AEST_SEED_AND_STRICT_DUST_MEMORY_SOURCE_GATE_PASS_NOT_FULL_PHYSICS',
  'scope':'radiation-only self-gravitating photons/massless free-streaming neutrinos with dustlike non-gravitating AeST test fluid, O((k*tau)^2); separate exact reduced action conditional c_a^2=0 source-null theorem',
  'gate_count':len(gates),'gates':gates,
  'Phi2_over_Psi0':str(s.factor(Phi2/p)),
  'Psi2_over_Psi0':str(s.factor(Psi2/p)),
  'sigma_nu4_over_Psi0':str(s.factor(sigma4/p)),
  'neutrino_F3_over_Psi0_x3':'2/105',
  'Delta_A_over_Psi0_x2':str(s.factor(((da+3*H*ta/k**2)/x**2)/p)),
  'Delta_gamma_over_Psi0_x2':str(s.factor(((dg+4*H*tg/k**2)/x**2)/p)),
  'Delta_nu_over_Psi0_x2':str(s.factor(((dn+4*H*tn/k**2)/x**2)/p)),
  'strict_dust_conditional':'For c_a^2=0 and selected initial X=E=q=qdot=0, the original reduced action has X=E=q=qdot=0 for any externally supplied Delta_A on a regular interval; finite c_a^2 introduces zero-state drive Xdot=c_a^2 Delta_A and Edot=-C Q c_a^2 Delta_A/K_B.',
  'new_genuine_physics_still_needed':'Coupled O(y_A,y_b*(k*tau)^2) and original full finite-k scalar/aether Ward, physical initial X,E, selected bath and full Einstein constraints.',
  'full_physics_GO':False,'DES_detection':False,
 }
def main():
 p=argparse.ArgumentParser()
 p.add_argument('--repo-root',type=Path,default=Path(__file__).resolve().parents[2])
 p.add_argument('--self-test',action='store_true')
 p.add_argument('--out',type=Path)
 args=p.parse_args()
 if not args.self_test:locks(args.repo_root.resolve())
 rep=solve()
 print('GE19_RADIATION_NLO_AND_STRICT_DUST_SYMBOLIC_PASS',rep['gate_count'],flush=True)
 print('GE19_FULL_PHYSICS_GO False',flush=True)
 if args.out:
  out=args.out.resolve()
  if out.exists():raise RuntimeError('REFUSE_OVERWRITE '+str(out))
  out.parent.mkdir(parents=True,exist_ok=True)
  out.write_text(json.dumps(rep,indent=2,sort_keys=True)+'\n')
  print('GE19_RADIATION_NLO_REPORT',out,flush=True)
 elif args.self_test:print(json.dumps(rep,indent=2,sort_keys=True))
if __name__=='__main__':main()
