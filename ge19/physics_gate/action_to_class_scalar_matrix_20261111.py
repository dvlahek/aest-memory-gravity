#!/usr/bin/env python3
"""One action-to-CLASS scalar equivalence matrix: NO CLASS runs, no tuning.

Exact SymPy checks on the frozen GE06+GE05 linear scalar Lagrangian,
original CLASS fluid mapping and original v019j source. Includes source
blob locks if executed in the research Git checkout. Does NOT claim
unreduced full 3+1 action equivalence, constraint propagation or DES fit.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
import sympy as s

SOURCE_BLOBS={
    'ge06/analytic_aest_directional_source_generator.py':'a7afe0035054a9dca55d74a6497c081422114b4c',
    'ge05/memory_directional_source_generator.py':'40837d77f89028da30c28899e2d0530a4401844e',
    'v019/apply_patch_v019.py':'c78484eb916bfee2730759c0bdc813a706bf9a68',
    'v019j/apply_memory_patch.py':'14796a5ed9e6265ed6810c792a93d7328a109364',
    'docs/ge19_lw33_exact_scalar_action_to_CLASS_offshell_source_decision_2026-11-10.md':'dedcb6148b6ee4353c32972fcc456d9e3a185ffd',
}

def locks(root):
    for p,want in SOURCE_BLOBS.items():
        f=root/p
        if not f.is_file(): raise RuntimeError('ORIGINAL_SOURCE_MISSING: '+p)
        got=subprocess.check_output(['git','hash-object',str(f)],text=True,cwd=root).strip()
        if got != want:raise RuntimeError(f'ORIGINAL_SOURCE_CHANGED: {p} {got}')
    fluid=(root/'v019/apply_patch_v019.py').read_text()
    memory=(root/'v019j/apply_memory_patch.py').read_text()
    assert 'dy[pv->index_pt_theta_cdm]' in fluid
    assert 'dy[pv->index_pt_delta_cdm]' in fluid
    assert 'dy[pv->index_pt_alpha_aest]' in fluid
    assert 'dy[pv->index_pt_E_aest]' in fluid
    assert 'E_rhs_aest -= 0.5*Q_aest*Bchi_aest;' in memory
    assert 'Bchi_aest *= pba->aest_eta;' in memory
    assert 'dy[pv->index_pt_mem_p_aest+jm]' in memory
    print('GE19_ORIGINAL_SOURCE_LOCKS_PASS',len(SOURCE_BLOBS),flush=True)
    return True

def algebra():
    a,k,H,Q,KB,C,KQ,KQQ,rho,eta,omega,sw =s.symbols(
        'a k H Q K_B C K_Q K_QQ rho eta omega sw',real=True,nonzero=True)
    E,chi,dQ,D,Pi,th,alpha,phi,q,qd,qdd,Psi=s.symbols(
        'E chi dQ D Pi theta alpha phi q qdot qddot Psi',real=True)
    ca=KQ/(Q*KQQ)
    R=Q*KQ/3
    oneplusw=R/rho
    Daction=(Q*KQQ*dQ-k**2/a**2*(KB*E+C*chi))/3
    Paction=KQ*dQ/3
    Pclass=ca*Daction+ca*k**2/(3*a**2)*(KB*E+C*chi)
    tests={}
    tests['action_pressure_equals_class_pressure']=s.simplify(Pclass-Paction)==0
    tests['action_momentum_equals_class_momentum']=s.simplify(R*th-KQ*k**2*(a*Q*th/k**2)/(3*a))==0
    # proper-time theta is conformal theta' divided by a.
    Qdot=-3*H*ca*Q
    thdot=(3*ca-1)*H*th + k**2/a*(Pi/oneplusw+Psi)
    phidot=s.expand(a*(H*Q+Qdot)*th/k**2+a*Q*thdot/k**2)
    tests['class_theta_euler_recovers_action_dQ']=s.simplify(phidot-Q*Psi-Q*Pi/oneplusw)==0
    tests['action_dQ_to_class_pressure']=s.simplify(Q*Pi/oneplusw-3*rho*Pi/KQ)==0
    chidot=s.expand(phidot+Qdot*alpha+Q*(E-Psi))
    expected_chidot=Q*(E+Pi/oneplusw-3*H*ca*alpha)
    tests['class_alpha_theta_recover_chi_dot']=s.simplify(chidot-expected_chidot)==0
    # original normalized longitudinal action per positive bath node
    bath=eta*a**3/s.Integer(4)*(qd**2-(omega*q-sw*k*chi/a)**2)
    B=sw**2*chi-a*omega*sw*q/k
    tests['bath_scalar_source_exact']=s.simplify(s.diff(bath,chi)+eta*a*k**2*B/2)==0
    tests['bath_aether_source_rank_one']=s.simplify(Q*s.diff(bath,chi)+eta*a*k**2*Q*B/2)==0
    action_kinetic=a*k**2*(KB*E**2+2*C*E*chi-C*chi**2)
    tests['aether_kinetic_hessian_2KB']=s.simplify(s.diff(action_kinetic,E,2)-2*a*k**2*KB)==0
    normalized=s.simplify(Q*s.diff(bath,chi)/s.diff(action_kinetic,E,2))
    tests['action_normalized_quarter_source']=s.simplify(normalized+eta*Q*B/(4*KB))==0
    # q proper-time E-L variation after d/dt(a^3)=3Ha^3
    eq_q=s.simplify(eta*a**3/s.Integer(2)*(qdd+3*H*qd)-s.diff(bath,q))
    expected_q=eta*a**3/s.Integer(2)*(qdd+3*H*qd+omega**2*q-omega*sw*k*chi/a)
    tests['auxiliary_retarded_oscillator_eq']=s.simplify(eq_q-expected_q)==0
    # q''=a^2(qdd+H qdot), Hconf=aH, q'=a qdot.
    conf=s.expand(a**2*(qdd+H*qd)+2*(a*H)*(a*qd)+a**2*omega**2*q-a*omega*sw*k*chi)
    tests['auxiliary_conformal_source_units']=s.simplify(conf-a**2*(qdd+3*H*qd+omega**2*q-omega*sw*k*chi/a))==0
    gamma=s.symbols('gamma')
    S=a*eta*k**2*B/s.Integer(2)*(1-4*gamma)
    tests['quarter_scalar_charge_residual_zero']=s.simplify(S.subs(gamma,s.Rational(1,4)))==0
    tests['half_scalar_charge_residual_nonzero']=s.simplify(S.subs(gamma,s.Rational(1,2))+a*eta*k**2*B/2)==0
    # On the true scalar Euler, Rrho_dot+3H Rrho =
    # eta Q k^2 B (1-4gamma)/(12 a^2), when other residuals vanish.
    drift=eta*Q*k**2*B*(1-4*gamma)/(12*a**2)
    tests['quarter_density_dictionary_no_source_drift']=s.simplify(drift.subs(gamma,s.Rational(1,4)))==0
    tests['half_density_dictionary_forced_drift']=s.simplify(drift.subs(gamma,s.Rational(1,2))+eta*Q*k**2*B/(12*a**2))==0
    failed=[x for x,ok in tests.items() if not ok]
    if failed:raise RuntimeError('SYMBOLIC_GATE_FAIL: '+','.join(failed))
    return tests,{
        'bath_euler_source_in_proper_time':str(normalized),
        'pressure_action':'K_Q deltaQ/3',
        'pressure_class':'rho_A Pi_A',
        'phase_chi_dot':'Q*(E_A+Pi_A/(1+w_A)-3*H*c_a^2*alpha_A)',
        'scalar_charge_residual_on_other_rows':'a*eta*k^2*B_chi*(1-4*gamma)/2',
        'density_dictionary_drift_if_scalar_euler_on_shell':
            'Rrho_dot+3H Rrho=eta*Q*k^2*B_chi*(1-4*gamma)/(12*a^2)',
        'bath_oscillator_proper_time':
            'qddot+3H qdot+omega^2 q = omega sqrt(w) k chi/a',
        'bath_oscillator_conformal_time':
            "q''+2Hconf q'+a^2 omega^2 q = a omega sqrt(w) k chi",
    }

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--repo-root',type=Path,default=Path(__file__).resolve().parents[2])
    parser.add_argument('--no-source-lock',action='store_true',help='standalone algebra test only')
    parser.add_argument('--out',type=Path)
    args=parser.parse_args()
    locked=False
    if not args.no_source_lock:locked=locks(args.repo_root.resolve())
    gates,results=algebra()
    report={
        'classification':'GE19_LINEAR_SCALAR_MATRIX_ALGEBRA_PASS_PRODUCTION_ACTION_TO_CLASS_STILL_OPEN',
        'source_locks_executed':locked,
        'source_blobs':SOURCE_BLOBS if locked else {},
        'symbolic_gates':gates,
        'identities':results,
        'minimal_matter_coupling_assumed':True,
        'all_species_CLASS_ODE_rows_independently_matched':False,
        'full_covariant_constraint_propagation_certified':False,
        'production_physics_go':False,
        'DES_detection':False,
    }
    print('GE19_SCALAR_MATRIX_SYMBOLIC_PASS',len(gates),flush=True)
    print('GE19_PRODUCTION_PHYSICS_GO',False,flush=True)
    if args.out:
        dest=args.out.resolve()
        if dest.exists():raise RuntimeError('OUTPUT_EXISTS')
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
        print('GE19_MATRIX_OUTPUT',dest,flush=True)
if __name__=='__main__':main()
