#!/usr/bin/env python3
"""GE19: frozen-coefficient longitudinal AeST+positive-bath gain gate.

Only an algebraic diagnostic of the original fixed-source *reduced scalar*
ODEs. A local frozen-coefficient eigenvalue is not a physical global
Einstein-constraint-compatible cosmological mode. No CLASS, DES or sweeps.
"""
from __future__ import annotations
import argparse
import json
import subprocess
from pathlib import Path
import sympy as s

SOURCE_BLOBS={
 'v019/apply_patch_v019.py':'c78484eb916bfee2730759c0bdc813a706bf9a68',
 'v019j/apply_memory_patch.py':'14796a5ed9e6265ed6810c792a93d7328a109364',
 'docs/ge19_20261112_retarded_bath_energy_amplification_gate.md':'f53374384ee02d737ab6c4f9dc4c2c71925fda0a',
 'v019/ini/aest_exp.ini':'f9a2bde8921a148e063f9657a8ede0a51c6a629d',
}

def lock(root):
 for path,expected in SOURCE_BLOBS.items():
  p=root/path
  if not p.is_file():raise RuntimeError('MISSING_SOURCE: '+path)
  actual=subprocess.check_output(['git','hash-object',str(p)],cwd=root,text=True).strip()
  if actual!=expected:raise RuntimeError('SOURCE_CHANGED: '+path+' '+actual)
 src=(root/'v019/apply_patch_v019.py').read_text()
 mem=(root/'v019j/apply_memory_patch.py').read_text()
 ini=(root/'v019/ini/aest_exp.ini').read_text()
 for st in ('E_rhs_aest = KQ_aest*chi_aest','-(2.-pba->aest_KB)',
            'dy[pv->index_pt_E_aest]'):
  if st not in src: raise RuntimeError('AEST_CODE_ANCHOR_MISSING: '+st)
 for st in ('Bchi_aest += wj*chi_aest-sw*(a*omega_j/k)*qj;',
            'dy[pv->index_pt_mem_p_aest+jm] ='):
  if st not in mem:raise RuntimeError('BATH_CODE_ANCHOR_MISSING: '+st)
 if 'aest_KB = 0.1' not in ini:raise RuntimeError('BENCHMARK_KB_CHANGED')
 print('GE19_GAIN_SOURCE_LOCKS_PASS',len(SOURCE_BLOBS),flush=True)

def exact_algebra():
 Q,H,KB,KQ,R,k,a,cs,eta,Wb=s.symbols(
   'Q H K_B K_Q R_A k a cs2 eta Wb',positive=True)
 C=s.symbols('C',real=True)
 chi,E,Delta=s.symbols('chi E Delta',real=True)
 lam,omega,weight=s.symbols('lambda omega w',positive=True)
 grad=k*k*(KB*E+C*chi)/(3*a*a*R)
 dchi=Q*E+Q*cs*(Delta-3*H*chi/Q+grad)
 B=s.symbols('B_chi',real=True)
 dE=-H*E+(KQ*chi-C*(dchi-Q*E+(H+Q)*chi)-eta*Q*B/s.Integer(4))/KB
 m=s.simplify(s.Matrix([dchi,dE.subs(B,Wb*chi)]).jacobian([chi,E]))
 force=s.simplify(s.Matrix([dchi,dE]).diff(Delta))
 w_eff=weight*lam*(lam+3*H)/(lam*lam+3*H*lam+omega*omega)
 Eoverchi=(lam+3*H*cs)/Q
 qoverchi=omega*s.sqrt(weight)*k/(a*(lam*lam+3*H*lam+omega*omega))
 Boverchi=s.simplify(weight-a*omega*s.sqrt(weight)*qoverchi/k)
 F=s.factor(KB*(lam+H)*(lam+3*H*cs)/Q -
   (KQ-C*(H+Q-3*H*cs))+eta*Q*w_eff/s.Integer(4))
 eq=KB*(lam+H)*Eoverchi-(KQ-C*(lam-Q*Eoverchi+H+Q)-eta*Q*Boverchi/s.Integer(4))
 thresh=KQ-C*(H+Q-3*H*cs)-3*KB*H*H*cs/Q
 Fzero=s.simplify(F.subs(lam,0))
 dr=s.diff(w_eff,lam)
 expected_dr=weight*omega**2*(2*lam+3*H)/(lam*lam+3*H*lam+omega*omega)**2
 dF=s.diff(F,lam)
 expected_dF=KB*(2*lam+H*(1+3*cs))/Q+eta*Q*dr/4
 f_A,mu=s.symbols('f_A mu',positive=True)
 pol=s.expand((2*mu/s.Integer(3))*(2*mu/s.Integer(3)-1)+
      (s.Rational(2,3))*(2*mu/s.Integer(3)) -
      s.Rational(4,3)*f_A/KB)
 muplus=(1+s.sqrt(1+48*f_A/KB))/4
 muminus=(1-s.sqrt(1+48*f_A/KB))/4
 checks={
   'kinematic_pressure_source':s.simplify(dchi-Q*E-Q*cs*(Delta-3*H*chi/Q+grad))==0,
   'forced_vector_exact':s.simplify(force-s.Matrix([Q*cs,-C*Q*cs/KB]))==s.zeros(2,1),
   'trace_exact':s.simplify(s.trace(m)+H*(1+3*cs))==0,
   'k_zero_matrix_a11':s.simplify(m[0,0].subs(k,0)+3*H*cs)==0,
   'k_zero_matrix_a12':s.simplify(m[0,1].subs(k,0)-Q)==0,
   'k_zero_matrix_a21':s.simplify(m[1,0].subs(k,0)-(KQ-C*(H+Q-3*H*cs)-eta*Q*Wb/4)/KB)==0,
   'k_zero_matrix_a22':s.simplify(m[1,1].subs(k,0)+H)==0,
   'bath_retarded_eigen_response':s.simplify(Boverchi-w_eff)==0,
   'complete_bath_dispersion':s.simplify(eq-F)==0,
   'static_bath_force_cancelled':s.simplify(w_eff.subs(lam,0))==0,
   'static_root_threshold_eta_independent':s.simplify(Fzero+thresh)==0,
   'positive_bath_kernel_derivative':s.simplify(dr-expected_dr)==0,
   'positive_F_derivative':s.simplify(dF-expected_dF)==0,
   'eta_increases_F_for_positive_lambda':s.simplify(s.diff(F,eta)-Q*w_eff/4)==0,
   'no_bath_dust_threshold':s.simplify(thresh.subs(cs,0)-KQ+C*(H+Q))==0,
   'matter_era_positive_power_root':s.simplify(pol.subs(mu,muplus))==0,
   'matter_era_negative_power_root':s.simplify(pol.subs(mu,muminus))==0,
 }
 bad=[key for key,val in checks.items() if not val]
 if bad:raise RuntimeError('GE19_GAIN_IDENTITY_FAIL '+repr(bad))
 return checks,{
 'matrix_chi_E':'dchi=Achi*chi+AE*E+Q*c_a^2*Delta_A; dE=... -eta*Q*B_chi/(4*K_B)',
 'trace_chi_E':'-H*(1+3*c_a^2)',
 'frozen_dispersion_one_node':'K_B*(lambda+H)*(lambda+3*H*c_a^2)/Q -[K_Q-(2-K_B)*(H+Q-3*H*c_a^2)]+eta*Q/4*w*lambda*(lambda+3*H)/(lambda^2+3H*lambda+omega^2)',
 'all_nodes_rule':'sum positive node dispersion contributions w_j*lambda*(lambda+3H)/(lambda^2+3H*lambda+omega_j^2)',
 'positive_real_root_condition':'K_Q > (2-K_B)*(H+Q-3*H*c_a^2)+3*K_B*H^2*c_a^2/Q',
 'positive_real_root_count_given_condition':1,
 'bath_cannot_remove_positive_frozen_root_given_condition':True,
 'bath_positive_weights_reduce_positive_growth_rate':True,
 'matter_era_illustrative_power_chi_a':'a^[(1+sqrt(1+48*f_A/K_B))/4]',
 'fixed_background_numerical_epoch_threshold_evaluated':False,
 'physical_gravitational_constraint_mode_certified':False,
 'full_time_dependent_fundamental_matrix_bounded':False,
 }

def main():
 ap=argparse.ArgumentParser()
 ap.add_argument('--repo-root',type=Path,default=Path(__file__).resolve().parents[2])
 ap.add_argument('--no-source-lock',action='store_true')
 ap.add_argument('--out',type=Path)
 args=ap.parse_args()
 if not args.no_source_lock:lock(args.repo_root.resolve())
 checks,conclusions=exact_algebra()
 payload={
 'classification':'GE19_REDUCED_FROZEN_COEFFICIENT_POSITIVE_ROOT_CONDITIONAL_NOT_FULL_GR_INSTABILITY',
 'identity_count':len(checks),'identities':checks,'derivations':conclusions,
 'assumptions':['one fixed local FLRW snapshot; coefficients treated as constants',
                'k->0+ longitudinal limit; q_j scales with k',
                'Delta_A treated as independent prescribed input and set to zero for eigenmode',
                'H>0,Q>0,K_B>0,c_a^2>=0,eta>=0,w_j>=0,omega_j>0',
                'retarded no-free-bath initial sector for forced evolution'],
 'source_locks_executed':not args.no_source_lock,
 'source_blobs':SOURCE_BLOBS if not args.no_source_lock else {},
 'isolation_physical_consistency':'UNPROVED: full Einstein constraints and dynamically coupled Delta_A not imposed',
 'full_GR_AeST_NL0B_instability_proved':False,
 'cosmological_eta_transfer_converged':False,
 'DES_detection':False,'production_physics_go':False,
 }
 print('GE19_REDUCED_FROZEN_GAIN_IDENTITIES_PASS',len(checks),flush=True)
 print('GE19_FULL_PHYSICS_GO False',flush=True)
 if args.out:
  out=args.out.resolve()
  if out.exists():raise RuntimeError('REFUSE_OUTPUT_OVERWRITE')
  out.parent.mkdir(parents=True,exist_ok=True)
  out.write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n')
  print('GE19_FROZEN_GAIN_RESULT',out,flush=True)
if __name__=='__main__':main()
