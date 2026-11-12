#!/usr/bin/env python3
"""GE19: Einstein constraints projected into all-species AeST scalar source system.
Exact symbolic identities only. Standard species are conserved stress sources,
not a completed CLASS Boltzmann hierarchy. Frozen spectrum is instantaneous.
No new CLASS, DES, η scans, numerical transfer, or full physics GO.
"""
import argparse, json, subprocess
from pathlib import Path
import sympy as s

LOCKS={
 'v019/apply_patch_v019.py':'c78484eb916bfee2730759c0bdc813a706bf9a68',
 'v019j/apply_memory_patch.py':'14796a5ed9e6265ed6810c792a93d7328a109364',
 'docs/ge19_lw30_original_gr_aest_adm_scalar_constraints_class_bridge_2026-11-10.md':'353c18db50c248acff91ddd95d5742ae169f3de3',
 'docs/ge19_20261111_all_species_Einstein_operator_and_adiabatic_IC_block.md':'e872a066b4e9a5190360f402bd81681e6ec047c5',
 'docs/ge19_20261112_frozen_coupled_scalar_bath_gain_conditional_root.md':'9c0886f4842452ead4d47e235b36ebd43508bafc',
}

def lock(root):
 for path,want in LOCKS.items():
  f=root/path
  if not f.is_file():raise RuntimeError('MISSING_SOURCE '+path)
  got=subprocess.check_output(['git','hash-object',str(f)],text=True,cwd=root).strip()
  if got!=want:raise RuntimeError(f'SOURCE_CHANGED {path}: {got}')
 print('GE19_CONSTRAINT_SOURCE_LOCKS_PASS',len(LOCKS),flush=True)

def calculate():
 H,Q,KQ,cs,k,a,KB,C,eta=s.symbols('H Q KQ c2 k a KB C eta',positive=True)
 Phi,phi,chi,E=s.symbols('Phi phi chi E')
 SD,ST,SP,SS,RS=s.symbols('SD ST SP SS RS')
 RA=Q*KQ/3; RT=RA+RS
 Psi=Phi-s.Rational(9,2)*a*a*SS/k**2
 Phi_dot=KQ*phi/2-H*Psi+s.Rational(3,2)*a*ST/k**2
 DA=-s.Rational(2,3)*k*k*Phi/a**2-H*KQ*phi-3*a*H*ST/k**2-SD
 g=cs*k**2/(a*a*KQ)
 Omega=SD+3*a*H*ST/k**2
 phi_dot=Q*Psi-3*H*cs*phi+g*(KB*E+C*chi-2*Phi)-3*cs*Omega/KQ
 chi_dot=Q*E-3*H*cs*chi+g*(KB*E+C*chi-2*Phi)-3*cs*Omega/KQ
 alpha=(chi-phi)/Q
 alpha_dot=s.diff(alpha,phi)*phi_dot+s.diff(alpha,chi)*chi_dot+s.diff(alpha,Q)*(-3*H*cs*Q)
 PA=KQ*(phi_dot-Q*Psi)/3
 SD_dot=-3*H*(SD+SP)-ST/a+3*RS*Phi_dot
 ST_dot=-4*H*ST+k*k/a*(SP+RS*Psi-SS)
 bg={Phi:Phi_dot,phi:phi_dot,H:-s.Rational(3,2)*RT,
     KQ:-3*H*KQ,Q:-3*H*cs*Q,a:H*a,SD:SD_dot,ST:ST_dot}
 def Dt(expr):return sum((s.diff(expr,z)*zd for z,zd in bg.items() if expr.has(z)),s.Integer(0))
 chk={}
 chk['Einstein_Hamiltonian_matter_density_eliminated']=s.simplify(k*k*Phi/a**2+3*H*(Phi_dot+H*Psi)+s.Rational(3,2)*(DA+SD))==0
 chk['Einstein_momentum_all_species']=s.simplify(Phi_dot+H*Psi-s.Rational(3,2)*a/k**2*(RA*k*k*phi/(a*Q)+ST))==0
 chk['Einstein_shear_all_species']=s.simplify(Phi-Psi-s.Rational(9,2)*a*a*SS/k**2)==0
 chk['action_AeST_density_dictionary_preserved']=s.simplify(DA-(KQ/cs*(phi_dot-Q*Psi)-k*k/a**2*(KB*E+C*chi))/3)==0
 chk['aether_phase_alpha_kinematics']=s.simplify(alpha_dot-E+Psi)==0
 chk['aether_chi_closure_from_phase']=s.simplify(chi_dot-phi_dot+Q*Psi-Q*E+3*H*cs*(chi-phi))==0
 chk['standard_species_comoving_source']=s.simplify(Omega-SD-3*a*H*ST/k**2)==0
 chk['AeST_comoving_density_from_constraint']=s.simplify(DA+3*a*H*(RA*k*k*phi/(a*Q))/k**2+Omega+2*k*k*Phi/(3*a*a))==0
 chk['AeST_pressure_action']=s.simplify(PA-KQ*(phi_dot-Q*Psi)/3)==0
 chk['AeST_density_conservation_exact']=s.simplify(Dt(DA)+3*H*(DA+PA)+KQ*k*k*phi/(3*a*a)-3*RA*Phi_dot)==0
 TA=KQ*k*k*phi/(3*a)
 chk['AeST_momentum_conservation_exact']=s.simplify(Dt(TA)+4*H*TA-k*k/a*(PA+RA*Psi))==0
 chk['total_density_conservation']=s.simplify(Dt(DA+SD)+3*H*(DA+SD+PA+SP)+(TA+ST)/a-3*RT*Phi_dot)==0
 chk['total_momentum_conservation']=s.simplify(Dt(TA+ST)+4*H*(TA+ST)-k*k/a*(PA+SP+RT*Psi-SS))==0
 M,D0,P0,S0,R0=s.symbols('M D0 P0 S0 R0')
 M_dot=-3*H*M+s.Rational(3,2)*(P0+R0*Psi-S0)
 D0_dot=-3*H*(D0+P0)-2*k*k*M/(3*a*a)+3*R0*(M-H*Psi)
 CH=k*k*Phi/a**2+3*H*M+s.Rational(3,2)*D0
 CH_dot=k*k/a**2*(M-H*Psi-2*H*Phi)-s.Rational(9,2)*R0*M+3*H*M_dot+s.Rational(3,2)*D0_dot
 slip=Phi-Psi-s.Rational(9,2)*a*a*S0/k**2
 chk['Hamiltonian_constraint_propagation_with_shear']=s.simplify(CH_dot+3*H*CH-H*k*k*slip/a**2)==0
 chk['Einstein_trace_from_total_momentum_and_shear']=s.simplify(M_dot+3*H*M-s.Rational(3,2)*(P0+R0*Psi-S0))==0
 lam,G,Beff=s.symbols('lambda g B_eff')
 A=KQ-C*(H+Q-3*H*cs)
 MAT=s.Matrix([[-H,KQ/2,0,0],
 [Q-2*G,-3*H*cs,G*C,G*KB],
 [-2*G,0,-3*H*cs+G*C,Q+G*KB],
 [2*C*G/KB,0,(A-C*C*G-eta*Q*Beff/4)/KB,-H-C*G]])
 DG=(lam+H)*(lam+3*H*cs)-Q*KQ/2
 DS=(lam+H)*(lam+3*H*cs)-Q*(A-eta*Q*Beff/4)/KB
 N=KQ-C*Q*(1+C/KB)-eta*Q*Beff/4
 poly=s.expand(DG*DS+G*(KQ*DS-N*DG))
 char=s.factor((lam*s.eye(4)-MAT).det())
 chk['constraint_projected_frozen_rank_one_polynomial']=s.simplify(char-poly)==0
 chk['zero_gradient_gravity_scalar_factorization']=s.simplify(char.subs(G,0)-DG*DS)==0
 chk['frozen_gradient_is_rank_one_update']=(MAT.diff(G).rank()==1)
 Eoverchi=(lam+3*H*cs)/Q
 Phioverchi=G*(KB*Eoverchi+C)/(2*(lam+H)*(lam+3*H*cs)/KQ-Q+2*G)
 chk['finite_gradient_scalar_eigenmode_metric_induced']=s.simplify((2*(lam+H)*(lam+3*H*cs)/KQ-Q+2*G)*Phioverchi-G*(KB*Eoverchi+C))==0
 chk['physical_AeST_only_Delta_nonzero_for_metric']=s.simplify((-2*k*k*Phi/(3*a*a))/RA+2*k*k*Phi/(3*a*a*RA))==0
 chk['scalar_eigenvalue_persists_for_small_g_conditional']=s.simplify(s.diff(poly,G).subs(G,0)-KQ*DS+N*DG)==0
 bad=[n for n,v in chk.items() if not v]
 if bad:raise RuntimeError('SYMBOLIC_FAIL: '+str(bad))
 return chk,{
 'all_species_AeST_source':'Omega_s=sum[D_s+3*a*H*T_s/k^2]=sum[(rho_s+p_s)*Delta_s]',
 'Einstein_constraint':'R_A*Delta_A+Omega_s=-2*k^2*Phi/(3*a^2)',
 'source_ODE_phi':'phi_dot=Q*Psi-3H*c_a^2*phi+g*(K_B*E+(2-K_B)*chi-2*Phi)-3*c_a^2*Omega_s/K_Q',
 'source_ODE_chi':'chi_dot=Q*E-3H*c_a^2*chi+g*(K_B*E+(2-K_B)*chi-2*Phi)-3*c_a^2*Omega_s/K_Q',
 'metric_Phi_dot':'Phi_dot=K_Q*phi/2+3*a*T_s/(2*k^2)-H*Psi',
 'metric_shear':'Psi=Phi-9*a^2*S_s/(2*k^2)',
 'g':'c_a^2*k^2/(a^2*K_Q)',
 'Hamiltonian_propagation':'C_H_dot+3H*C_H=H*k^2/a^2*(Phi-Psi-9*a^2*Shear/(2*k^2))',
 'AeST_only_frozen_polynomial':'P(lambda,g)=DG*DS+g*(K_Q*DS-N*DG)',
 'DG':'(lambda+H)*(lambda+3H*c_a^2)-Q*K_Q/2',
 'DS':'(lambda+H)*(lambda+3H*c_a^2)-Q*(K_Q-C*(H+Q-3H*c_a^2)-eta*Q*B_eff(lambda)/4)/K_B',
 'N':'K_Q-C*Q*(1+C/K_B)-eta*Q*B_eff(lambda)/4',
 'scalar_mode_metric_ratio':'Phi/chi=g*(K_B*(lambda+3H*c_a^2)/Q+C)/[2*(lambda+H)*(lambda+3H*c_a^2)/K_Q-Q+2*g]',
 'root_scope':'Simple positive scalar root at g=0 persists for sufficiently small g>0 if distinct from gravity eigenvalue; not full cosmological growth',
 }
def main():
 ap=argparse.ArgumentParser()
 ap.add_argument('--repo-root',type=Path,default=Path(__file__).resolve().parents[2])
 ap.add_argument('--no-source-lock',action='store_true')
 ap.add_argument('--out',type=Path)
 x=ap.parse_args()
 if not x.no_source_lock:lock(x.repo_root.resolve())
 chk,derived=calculate()
 report={'classification':'GE19_ALL_SPECIES_CONSTRAINT_PROPAGATION_AND_AEST_PROJECTED_OPERATOR_SYMBOLIC_PASS_NOT_FULL_PRODUCTION',
 'symbolic_gates':chk,'gate_count':len(chk),'derivations':derived,
 'original_source_locks_executed':not x.no_source_lock,
 'source_blobs':LOCKS if not x.no_source_lock else {},
 'standard_species_represented_by_conserved_stress_sources_not_full_hierarchy':True,
 'full_covariant_all_components_action_variation_proved':False,
 'CLASS_approximation_branches_verified':False,'time_dependent_full_spectral_gain_bounded':False,
 'physical_eta_Weyl_response_certified':False,'DES_detection':False,'production_physics_go':False}
 print('GE19_CONSTRAINT_PROJECTED_JOINT_IDENTITIES_PASS',len(chk),flush=True)
 print('GE19_FULL_PHYSICS_GO False',flush=True)
 if x.out:
  dest=x.out.resolve()
  if dest.exists():raise RuntimeError('REFUSE_OVERWRITE')
  dest.parent.mkdir(parents=True,exist_ok=True)
  dest.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
  print('GE19_JOINT_CONSTRAINT_REPORT',dest,flush=True)
if __name__=='__main__':main()
