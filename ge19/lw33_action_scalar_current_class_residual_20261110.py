#!/usr/bin/env python3
"""GE19 LW33: exact off-shell scalar-current / CLASS residual identity.

Original GE06+GE05 linear scalar action, fixed FLRW background laws and
original CLASS effective fluid dictionary. No changes to frozen patches.
Algebraic state definitions are *not* assumed when proving the identity:
their residuals and their time derivatives appear explicitly.
No full 3+1 action-to-CLASS or observed Weyl detection is claimed.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess
from pathlib import Path
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/'ge19/lw33_action_scalar_euler_class_residual_predata_20261110.json'
PRE_BLOB='19b1e2cfca8937c7af4beb6bf9784bd9a1372c7e'

def need(flag,tag):
    if not bool(flag): raise RuntimeError('GE19_LW33_'+tag)
def blob(path):
    return subprocess.check_output(['git','hash-object',str(path)],cwd=ROOT,text=True).strip()
def sha256(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()

def exact():
    a,H,Q,KB,C,KQ,KQQ,k,eta,B,gamma=s.symbols(
        'a H Q KB C KQ KQQ k eta B gamma',real=True,nonzero=True)
    D,E,chi,alpha,varphi,dQ,Phi,Psi=s.symbols(
        'D E chi alpha varphi deltaQ Phi Psi',real=True)
    Ddot,Edot,chidot,dQdot,Phidot,KQQdot=s.symbols(
        'Ddot Edot chidot deltaQdot Phidot KQQdot',real=True)
    Qdot=-3*H*KQ/KQQ
    KQdot=-3*H*KQ
    rates={a:a*H,Q:Qdot,KQ:KQdot,KQQ:KQQdot,
           D:Ddot,E:Edot,chi:chidot,dQ:dQdot,Phi:Phidot}
    def Dt(expr):
        return s.expand(sum(s.diff(expr,v)*rate for v,rate in rates.items()))
    P=KQ*dQ/3
    R=Q*KQ/3
    theta=k*k*varphi/(a*Q)
    T=R*theta
    A=KB*E+C*chi
    D_action=(Q*KQQ*dQ-k*k*A/a**2)/3
    Jt_action=2*a**3*KQQ*dQ-6*a**3*KQ*Phi
    Jt_fluid=6*a**3*D/Q+2*a*k*k*A/Q-6*a**3*KQ*Phi
    Jx_action=s.I*k*a*(2*C*(E-chi)+2*KQ*alpha-eta*B/2)
    S_action=Dt(Jt_action)-a*k*k*(2*C*(E-chi)+2*KQ*alpha-eta*B/2)
    # Original effective-fluid CLASS rows expressed in proper time.
    Ddot_class=-3*H*(D+P)-T/a+3*R*Phidot
    chidot_kin=dQ+Q*E+Qdot*alpha
    Edot_gamma=-H*E+(KQ*chi-C*(chidot_kin-Q*E+(H+Q)*chi)-eta*gamma*Q*B)/KB
    R_D=Ddot-Ddot_class
    R_E=Edot-Edot_gamma
    R_chi=chidot-chidot_kin
    R_geo=chi-varphi-Q*alpha
    R_rho=D-D_action
    residual=s.expand(
        6*a**3*R_D/Q+2*a*k*k*KB*R_E/Q+2*a*k*k*C*R_chi/Q
        +2*a*k*k*KQ*R_geo/Q-6*a**3*Dt(R_rho)/Q
        -18*a**3*H*R_rho/Q+a*eta*k*k*B*(1-4*gamma)/2)
    def zero(expr): return s.cancel(s.factor(expr))==0
    on_shell=residual.subs({Ddot:Ddot_class,Edot:Edot_gamma,chidot:chidot_kin})
    # Above substituting different residuals sequentially would recompute
    # D_action time derivatives, so use independent formal residual variables
    # instead when checking on-shell scalar source.
    gamma_source=a*eta*k*k*B*(1-4*gamma)/2
    needed_Ddot=s.solve(6*a**3*s.Symbol('dD')/Q+gamma_source,s.Symbol('dD'))[0]
    needed_chidot=s.solve(2*a*k*k*C*s.Symbol('dc')/Q+gamma_source,s.Symbol('dc'))[0]
    checks={
      'off_shell_action_scalar_to_CLASS_exact_identity':zero(S_action-residual),
      'action_current_exact_density_state_reexpression':zero(Jt_action-Jt_fluid+6*a**3*R_rho/Q),
      'time_derivative_of_density_dictionary_retained':zero(Dt(Jt_action-Jt_fluid+6*a**3*R_rho/Q)),
      'original_spatial_scalar_charge_flux_sign':zero(-s.I*k*Jx_action-a*k*k*(2*C*(E-chi)+2*KQ*alpha-eta*B/2)),
      'action_KQ_background_conservation':zero(KQdot+3*H*KQ),
      'action_Q_background_evolution':zero(Qdot+3*H*KQ/KQQ),
      'full_remainder_has_only_gamma_factor':zero(gamma_source-a*eta*k*k*B*(1-4*gamma)/2),
      'unique_evolution_coefficient_quarter':s.solve(gamma_source,gamma)==[s.Rational(1,4)],
      'original_action_gamma_quarter_scalar_source_zero':zero(gamma_source.subs(gamma,s.Rational(1,4))),
      'old_patch_gamma_half_scalar_source_nonzero':not zero(gamma_source.subs(gamma,s.Rational(1,2))),
      'old_patch_gamma_half_scalar_source_exact_negative_half':zero(gamma_source.subs(gamma,s.Rational(1,2))+a*eta*k*k*B/2),
      'old_patch_extra_Ddot_required':zero(needed_Ddot.subs(gamma,s.Rational(1,2))-eta*Q*k*k*B/(12*a*a)),
      'old_patch_formal_chidot_compensation':zero(needed_chidot.subs(gamma,s.Rational(1,2))-eta*Q*B/(4*C)),
      'eta_zero_recovers_unchanged_source':zero(gamma_source.subs(eta,0)),
      'negative_omit_spatial_scalar_flux_detected':not zero(gamma_source.subs(gamma,s.Rational(1,4))-a*eta*k*k*B/2),
      'negative_drop_density_dictionary_derivative_detected':not zero(Dt(R_rho)),
      'negative_drop_phase_field_dictionary_detected':not zero(R_geo),
      'negative_drop_aether_residual_detected':not zero(R_E),
      'negative_arbitrary_E_coefficient_not_universal':not zero(gamma_source.subs(gamma,s.Rational(1,3))),
    }
    bad=[n for n,p in checks.items() if not bool(p)]
    if bad:print('GE19_LW33_FAILED_CHECKS',bad,flush=True)
    need(not bad,'EXACT_IDENTITY_FAIL')
    return {n:bool(p) for n,p in checks.items()},{
      'scalar_action_equation':'S=dot(Jt)-a*k²*(2C(E-chi)+2KQ alpha-eta B/2)=0',
      'off_shell_exact_identity':'S=(6a³/Q)R_D+(2ak² KB/Q)R_E+(2ak² C/Q)R_chi+(2ak² KQ/Q)R_geo-(6a³/Q)dot(R_rho)-(18a³ H/Q)R_rho+(a eta k² B/2)(1-4gamma)',
      'R_D':'dot(D)-(-3H(D+P)-T/a+3R dot(Phi))',
      'R_E':'dot(E)-[-H E+(KQ chi-C*(dot(chi)_kin-Q E+(H+Q)chi)-eta gamma Q B)/KB]',
      'R_chi':'dot(chi)-(deltaQ+Q E+dot(Q)alpha)',
      'R_geo':'chi-varphi-Q alpha',
      'R_rho':'D-[QKQQ deltaQ-k²/a²*(KB E+C chi)]/3',
      'background_laws':'dot(KQ)=-3H KQ; dot(Q)=-3H KQ/KQQ',
      'on_shell_scalar_source_gamma_quarter':'0',
      'on_shell_scalar_source_gamma_half':'-a eta k² B/2',
      'minimal_required_Ddot_correction_half':'+eta Q k² B/(12a²)',
      'formal_chi_dot_compensation_half':'+eta Q B/(4C), violates fixed scalar phase dictionary if inserted ad hoc',
      'no_complete_full_covariant_3plus1_claim':True,
    }

def sources(parent):
    need(PRE.is_file() and blob(PRE)==PRE_BLOB,'PRELOCK_CHANGED')
    pre=json.loads(PRE.read_text())
    need(pre['classification']=='GE19_LW33_OFFSHELL_SCALAR_CURRENT_TO_CLASS_RESIDUAL_IDENTITY_PRELOCK','CLASSIFICATION_CHANGED')
    for path,want in pre['sources'].items():
        f=ROOT/path
        need(f.is_file() and blob(f)==want,'SOURCE_BLOB_CHANGED_'+f.name)
    need(parent.is_file() and sha256(parent)==pre['original_LW32_JSON_SHA256'],'LW32_PARENT_SHA_MISMATCH')
    d=json.loads(parent.read_text())
    need(d['classification']=='GE19_LW32_COVARIANT_MULTIPLIER_ELIMINATION_EXACT_PASS_CLASS_ETA_EVOLUTION_OPEN'
         and len(d['gates'])==20 and all(d['gates'].values()),'LW32_PARENT_GATES')
    patch=(ROOT/'v019j/apply_memory_patch.py').read_text()
    need('E_rhs_aest -= 0.5*Q_aest*Bchi_aest;' in patch,'ORIGINAL_HALF_NOT_FOUND')
    return pre

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--self-test',action='store_true')
    ap.add_argument('--lw32',type=Path,default=ROOT/'results/ge19_lw32_covariant_aether_auxiliary_multiplier_elimination_20261110_r1.json')
    ap.add_argument('--out',type=Path,default=ROOT/'results/ge19_lw33_action_scalar_current_class_residual_20261110_r1.json')
    args=ap.parse_args()
    checks,derived=exact()
    print('GE19_LW33_OFFSHELL_SCALAR_CLASS_IDENTITY_PASS',len(checks),flush=True)
    if args.self_test:return
    p=sources(args.lw32)
    print('GE19_LW33_SOURCE_LOCKS_PASS',len(p['sources']),flush=True)
    out=args.out.resolve()
    need(out.parent.is_dir() and not out.exists(),'OUTPUT_EXISTS_OR_PARENT_MISSING')
    report={
       'classification':'GE19_LW33_FULL_REDUCED_OFFSHELL_SCALAR_TO_CLASS_RESIDUAL_IDENTITY_PASS_OLD_HALF_SOURCE_INCOMPATIBLE_CONDITIONALLY_FULL_3PLUS1_OPEN',
       'checks':checks,'derived':derived,'original_LW32_SHA256':p['original_LW32_JSON_SHA256'],
       'predata_git_blob':PRE_BLOB,'source_blobs':p['sources'],
       'action_source_normalization_quarter_in_reduced_sector':True,
       'old_frozen_CLASS_gamma_half_reduced_equivalence':False,
       'original_CLASS_modified':False,
       'full_3plus1_Einstein_AeST_Y_action_to_CLASS_closed':False,
       'actual_physical_eta_matter_Weyl_derivative_certified':False,
       'DES_memory_observation':False,
    }
    out.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print('GE19_LW33_CLASSIFICATION',report['classification'],flush=True)
    print('GE19_LW33_PHYSICAL_OBSERVER_READY',False,flush=True)
    print('GE19_LW33_OUTPUT',out,flush=True)

if __name__=='__main__':main()
