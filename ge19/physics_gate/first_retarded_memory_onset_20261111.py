#!/usr/bin/env python3
"""GE19: exact reduced scalar first retarded memory-onset gate; NO CLASS run.

Compares action-based chi/E/bath equations in the frozen scalar dictionary.
Local-in-time Taylor identities only, not a full primordial next-order solution.
"""
import argparse, json, subprocess
from pathlib import Path
import sympy as s

LOCKS={
 'v019/apply_patch_v019.py':'c78484eb916bfee2730759c0bdc813a706bf9a68',
 'v019j/apply_memory_patch.py':'14796a5ed9e6265ed6810c792a93d7328a109364',
 'ge05/memory_directional_source_generator.py':'40837d77f89028da30c28899e2d0530a4401844e',
 'docs/ge19_lw33_exact_scalar_action_to_CLASS_offshell_source_decision_2026-11-10.md':'dedcb6148b6ee4353c32972fcc456d9e3a185ffd',
}

def lock(root):
 for name,expected in LOCKS.items():
  path=root/name
  if not path.exists(): raise RuntimeError('SOURCE_MISSING '+name)
  actual=subprocess.check_output(['git','hash-object',str(path)],cwd=root,text=True).strip()
  if actual!=expected: raise RuntimeError('SOURCE_CHANGED '+name+' '+actual)
 fluid=(root/'v019/apply_patch_v019.py').read_text()
 bath=(root/'v019j/apply_memory_patch.py').read_text()
 for term in ('dy[pv->index_pt_theta_cdm]', 'Pi_aest = cad2_aest*y',
              'E_rhs_aest = KQ_aest*chi_aest'):
  if term not in fluid: raise RuntimeError('FLUID_ANCHOR_MISSING '+term)
 for term in ('dy[pv->index_pt_mem_q_aest+jm] = pj;',
              'Bchi_aest += wj*chi_aest-sw*(a*omega_j/k)*qj;',
              'Bchi_aest *= pba->aest_eta;',
              'E_rhs_aest -= 0.5*Q_aest*Bchi_aest;'):
  if term not in bath: raise RuntimeError('BATH_ANCHOR_MISSING '+term)
 print('GE19_FIRST_ONSET_SOURCE_LOCKS_PASS',len(LOCKS),flush=True)

def calculate():
 a,H,k,Q,cs2,rhop,KB,C,KQ,eta,gamma,weight,omega,sw=s.symbols(
  'a H k Q cs2 rhop KB C KQ eta gamma weight omega sw',nonzero=True,real=True)
 chi,E,Delta,q,p=s.symbols('chi E Delta q p',real=True)
 theta,alpha,delta,Psi,oneplus=s.symbols('theta alpha delta Psi oneplus',real=True,nonzero=True)
 press=cs2*(delta/oneplus+k**2*(KB*E+C*chi)/(3*a**2*rhop))
 Qdot=-3*H*cs2*Q
 thetadot=(3*cs2-1)*H*theta+(k**2/a)*(press+Psi)
 alphadot=E-Psi
 raw=s.expand(Qdot*(a*theta/k**2+alpha)+Q*(H*a*theta/k**2+a*thetadot/k**2+alphadot))
 kin=Q*(E+press-3*H*cs2*alpha)
 grad=k**2*(KB*E+C*chi)/(3*a**2*rhop)
 closed=Q*E+Q*cs2*(Delta-3*H*chi/Q+grad)
 B=weight*chi-a*omega*sw*q/k  # single node; sum is linear
 Edot=-H*E+(KQ*chi-C*(closed-Q*E+(H+Q)*chi)-eta*gamma*Q*B)/KB
 init={chi:0,E:0,q:0,p:0}
 chi_i=s.simplify(closed.subs(init))
 E_i=s.simplify(Edot.subs(init))
 Bprime_i=weight*a*chi_i # Bprime=dB/dtau; chi_i is cosmic-time derivative
 q_third_i=a*a*k*omega*sw*chi_i  # q'=p; p'= -2aH p-a^2 omega^2 q+a k omega sw chi
 eta_E_quadratic=s.simplify(-eta*gamma*a*Q*Bprime_i/(2*KB))
 half_minus_quarter=s.simplify(eta_E_quadratic.subs(gamma,s.Rational(1,2))
                                  -eta_E_quadratic.subs(gamma,s.Rational(1,4)))
 tests={
  'kinematic_phase_theta_alpha':s.simplify(raw-kin)==0,
  'kinematic_comoving_delta':s.simplify((kin-closed).subs({chi:Q*(a*theta/k**2+alpha),Delta:delta/oneplus+3*H*a*theta/k**2}))==0,
  'initial_chi_derivative':s.simplify(chi_i-Q*cs2*Delta)==0,
  'initial_E_derivative':s.simplify(E_i+C*Q*cs2*Delta/KB)==0,
  'initial_B_force_zero':s.simplify(B.subs(init))==0,
  'initial_q_p_derivatives_zero':s.simplify(p.subs(init))==0,
  'bath_first_force_gradient':s.simplify(Bprime_i-weight*a*Q*cs2*Delta)==0,
  'bath_q_third_derivative':s.simplify(q_third_i-a*a*k*omega*sw*Q*cs2*Delta)==0,
  'quarter_eta_E_quadratic':s.simplify(eta_E_quadratic.subs(gamma,s.Rational(1,4))
                           +eta*a*a*Q**2*cs2*Delta*weight/(8*KB))==0,
  'half_minus_quarter_E_quadratic':s.simplify(half_minus_quarter
                           +eta*a*a*Q**2*cs2*Delta*weight/(8*KB))==0,
  'strict_dust_zero_chi_drive':s.simplify(closed.subs({cs2:0,chi:0,E:0}))==0,
  'strict_dust_zero_E_drive':s.simplify(Edot.subs({cs2:0,chi:0,E:0,q:0}))==0,
  'source_is_zero_at_exact_leading_adiabatic':s.simplify(chi_i.subs(Delta,0))==0,
  'quarter_source_only_not_initial_force':s.simplify(Edot.subs(init).diff(eta))==0,
 }
 failed=[n for n,v in tests.items() if not v]
 if failed:raise RuntimeError('GE19_FIRST_ONSET_ALGEBRA_FAIL '+repr(failed))
 return tests,{
  'chi_dot_at_zero_chi_E_q_p':'Q*c_a2*Delta_A',
  'E_dot_at_zero_chi_E_q_p':'-(2-K_B)*Q*c_a2*Delta_A/K_B',
  'B_chi_prime_at_zero_state':'sum(w_j)*a*Q*c_a2*Delta_A (conformal derivative)',
  'q_j_cubic_Taylor_coefficient':'a^2*k*omega_j*sqrt(w_j)*Q*c_a2*Delta_A/6',
  'E_eta_quadratic_Taylor_coefficient_quarter':'-eta*a^2*Q^2*c_a2*Delta_A*sum(w_j)/(8*K_B)',
  'E_half_minus_quarter_quadratic_coefficient':'-eta*a^2*Q^2*c_a2*Delta_A*sum(w_j)/(8*K_B)',
  'causal_taylor_time_variable':'Delta_tau=tau-tau_i',
 }

def main():
 ap=argparse.ArgumentParser()
 ap.add_argument('--repo-root',type=Path,default=Path(__file__).resolve().parents[2])
 ap.add_argument('--no-source-lock',action='store_true')
 ap.add_argument('--out',type=Path)
 a=ap.parse_args()
 if not a.no_source_lock:lock(a.repo_root.resolve())
 gates,identities=calculate()
 report={'classification':'GE19_REDUCED_FIRST_MEMORY_ONSET_SOURCE_IDENTITY_PASS_NOT_FULL_MODE',
  'source_locks_executed':not a.no_source_lock,'source_blobs':LOCKS if not a.no_source_lock else {},
  'exact_symbolic_gates':gates,'identity_count':len(gates),'identities':identities,
  'assumptions':['separate regular no-free-bath q_i=p_i=0','chi_i=E_i=0',
                 'fixed identical initial cosmological state for half and quarter',
                 'smooth fixed t_i>0, nonzero K_B and rho_A+p_A',
                 'linear reduced source/CLASS dictionary'],
  'first_nonzero_mode_amplitude_solved':False,
  'initial_comoving_Delta_A_fixed_by_all_species_next_order':False,
  'finite_eta_TRANSFER_convergence_certified':False,
  'full_physics_go':False,'DES_detection':False}
 print('GE19_FIRST_MEMORY_ONSET_EXACT_PASS',len(gates),flush=True)
 print('GE19_FULL_PHYSICS_GO False',flush=True)
 if a.out:
  target=a.out.resolve()
  if target.exists():raise RuntimeError('REFUSE_OUTPUT_OVERWRITE')
  target.parent.mkdir(parents=True,exist_ok=True)
  target.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
  print('GE19_FIRST_MEMORY_ONSET_REPORT',target,flush=True)
if __name__=='__main__':main()
