#!/usr/bin/env python3
"""GE19: independent *leading* radiation-era adiabatic mode with AeST Exp background.

NO CLASS evolution, DES observations, parameter optimization, solver sweeps, or code patching.
This proves leading k*tau -> 0, rho_A/rho_r -> 0 relations, not the
next-to-leading coupled growing eigenvector/production action-to-CLASS match.
"""
from __future__ import annotations
import argparse
import json
import subprocess
from pathlib import Path
import sympy as sp
import mpmath as mp

LOCKS = {
    'v019/patch/source/aest_memory.c': '9a522a653a1855eda3cb67e856f9fc10a1e73d54',
    'v019/ini/aest_exp.ini': 'f9a2bde8921a148e063f9657a8ede0a51c6a629d',
    'v019/apply_patch_v019.py': 'c78484eb916bfee2730759c0bdc813a706bf9a68',
    'v019j/apply_memory_patch.py': '14796a5ed9e6265ed6810c792a93d7328a109364',
}


def source_locks(repo_root: Path):
    for name, sha in LOCKS.items():
        path = repo_root / name
        if not path.is_file():
            raise RuntimeError('MISSING_SOURCE: ' + name)
        got = subprocess.check_output(['git', 'hash-object', str(path)], cwd=repo_root, text=True).strip()
        if got != sha:
            raise RuntimeError(f'FROZEN_SOURCE_CHANGED: {name}: {got} != {sha}')
    code = (repo_root / 'v019/patch/source/aest_memory.c').read_text()
    ini = (repo_root / 'v019/ini/aest_exp.ini').read_text()
    for key, snippet in {
        'EXP_BACKGROUND_K': 'k=2.*K2*Z0*Z0*(ex-1.);',
        'EXP_BACKGROUND_KQ': 'kq=4.*K2*Z0*Z*ex;',
        'EXP_BACKGROUND_KQQ': 'kqq=4.*K2*ex*(1.+2.*zz);',
        'EXP_BACKGROUND_QUANTIZED': 'kq=I0/(a*a*a);',
    }.items():
        if snippet not in code: raise RuntimeError('SOURCE_ANCHOR_MISSING: ' + key)
    for line in ('aest_model = Exp','aest_Q0 = 1e-4','aest_K2 = 9500',
                 'aest_Z0 = 1e-17','omega_cdm = 0.1201075'):
        if line not in ini: raise RuntimeError('BENCHMARK_PARAMETER_CHANGED: ' + line)
    print('GE19_FROZEN_EXP_SOURCE_LOCKS_PASS', len(LOCKS), flush=True)


def symbolic():
    tau, k, psi, a0, ca, w, rho, Q, KQ, KQQ, Rnu = sp.symbols(
        'tau k psi a0 ca w rho Q KQ KQQ Rnu', real=True, nonzero=True)
    a = a0*tau
    confH = 1/tau
    theta = k**2*tau*psi/2
    alpha = -a*tau*psi/2
    varphi = a*Q*tau*psi/2
    Qprime = -3*confH*Q*ca
    varphiprime = sp.diff(varphi,tau) + sp.diff(varphi,Q)*Qprime
    deltaQ = sp.expand(varphiprime/a-Q*psi)
    alpha_prime = sp.diff(alpha,tau)
    E = sp.expand(alpha_prime/a+psi)
    chi = sp.expand(varphi+Q*alpha)
    dA = -sp.Rational(3,2)*(1+w)*psi
    dgamma = -2*psi
    dnu = dgamma
    db = sp.Rational(3,4)*dgamma
    dp_over_rho = ca*dA
    dQ_action_expected = -sp.Rational(3,2)*Q*ca*psi
    Daction = Q*KQQ*deltaQ/3  # E=chi=0
    Paction = KQ*deltaQ/3
    tests = {}
    tests['ae_phase_deltaQ'] = sp.simplify(deltaQ-dQ_action_expected)==0
    tests['ae_aether_electric_vanishes'] = sp.simplify(E)==0
    tests['ae_chi_vanishes'] = sp.simplify(chi)==0
    tests['ae_density_action_dictionary'] = sp.simplify((Daction+sp.Rational(3,2)*(rho*(1+w))*psi).subs(KQQ, KQ/(Q*ca)).subs(KQ,3*rho*(1+w)/Q))==0
    tests['ae_pressure_action_dictionary'] = sp.simplify((Paction-ca*rho*dA).subs(KQ,3*rho*(1+w)/Q))==0
    tests['ae_ad_entropy_vs_photons'] = sp.simplify(dA/(1+w)-sp.Rational(3,4)*dgamma)==0
    # Photon and dark-fluid Euler, using a radiation-dominated Hconf=1/tau.
    thetaprime = sp.diff(theta,tau)
    tests['photon_euler_leading'] = sp.simplify(thetaprime-k**2*(dgamma/4+psi))==0
    tests['ae_theta_euler_leading'] = sp.simplify(thetaprime-((3*ca-1)*confH*theta+k**2*(ca*dA/(1+w)+psi)))==0
    # ae density conservation to zeroth order in k*tau, including w' and c_a^2.
    wprime=-3*confH*(1+w)*(ca-w)
    deltaAprime=sp.diff(dA,w)*wprime
    tests['ae_density_continuity_k0'] = sp.simplify(deltaAprime-3*confH*(w-ca)*dA)==0
    # Metric constraints at radiation leading order, using a^2 rho_r=Hconf^2
    Phi = (1+sp.Rational(2,5)*Rnu)*psi
    delta_rho_r = -2*confH**2/a**2*psi
    T_r = sp.Rational(4,3)*confH**2/a**2*theta
    tests['einstein_hamiltonian_radiation_k0'] = sp.simplify(3*confH**2*psi+sp.Rational(3,2)*a**2*delta_rho_r)==0
    tests['einstein_momentum_radiation_k0'] = sp.simplify(confH*psi-sp.Rational(3,2)*a**2*T_r/k**2)==0
    sigma_nu = k**2*tau**2*psi/15
    tests['nu_quadrupole_leading'] = sp.simplify(sp.diff(sigma_nu,tau)-sp.Rational(4,15)*theta)==0
    tests['einstein_neutrino_slip_leading'] = sp.simplify(Phi-psi-sp.Rational(9,2)*a**2/k**2*sp.Rational(4,3)*(confH**2/a**2)*Rnu*sigma_nu)==0
    # Scalar charge temporal part has vanishing derivative if a^3 KQ = I0.
    Jt=2*a**3*KQQ*deltaQ-6*a**3*KQ*Phi
    Jt=sp.factor(Jt.subs(KQQ,KQ/(Q*ca)))
    tests['ae_scalar_charge_constant_temporal_leading'] = sp.simplify(Jt+3*a**3*KQ*(psi+2*Phi))==0
    # inherited CDM adiabatic density and gauge mapping violate pressureful entropy by O(w)
    x,d=sp.symbols('x d',real=True)
    relative_entropy=(sp.Rational(3,4)*d-3*x)/(1+w)-sp.Rational(3,4)*(d-4*x)
    tests['class_dust_ic_entropy_exact'] = sp.simplify(relative_entropy-3*w*(4*x-d)/(4*(1+w)))==0
    # Nonzero w does not affect the leading bath with chi=0 and no homogeneous q excitation.
    tests['zero_bath_forcing_on_adiabatic_state'] = sp.simplify(chi)==0 and sp.simplify(E)==0
    failed=[key for key,val in tests.items() if not val]
    if failed: raise RuntimeError('GE19_SYMBOLIC_GROWING_MODE_FAIL: '+repr(failed))
    return {key:bool(val) for key,val in tests.items()}


def bisect(f, lo, hi, iterations=260):
    if not (f(lo)<0 and f(hi)>0): raise RuntimeError('BACKGROUND_BRACKET_FAIL')
    for _ in range(iterations):
        mid=(lo+hi)/2
        if f(mid)>0:hi=mid
        else:lo=mid
    return (lo+hi)/2


def background():
    mp.mp.dps = 75
    Q0=mp.mpf('1e-4'); Z0=mp.mpf('1e-17'); K2=mp.mpf('9500')
    omegaCDM=mp.mpf('0.1201075')
    # CLASS H0/c = (h/2997.92458) Mpc^-1 and Omega_cdm = omega_cdm/h^2.
    target=3*omegaCDM/(mp.mpf('2997.92458')**2)
    def kval(z):return 2*K2*Z0**2*(mp.exp(z*z)-1)
    def kqval(z):return 4*K2*Z0*z*mp.exp(z*z)
    def qval(z):return Q0+Z0*z
    z1=bisect(lambda z:qval(z)*kqval(z)-kval(z)-target,mp.mpf(0),mp.mpf(20))
    I0=kqval(z1)
    rows=[]
    for astr in ('1','0.6666666666666667','0.1','0.01','1e-4','1e-6','1e-8'):
        a=mp.mpf(astr)
        KQ=I0/a**3
        Z=bisect(lambda z:kqval(z)-KQ,mp.mpf(0),mp.mpf(20))
        Q=qval(Z);K=kval(Z)
        rho=Q*KQ-K
        w=K/rho
        ca=KQ/(Q*4*K2*mp.exp(Z*Z)*(1+2*Z*Z))
        r=Z0*(1-mp.exp(-Z*Z))/(2*Z)
        w_reduced=r/(Q-r)
        if abs(w-w_reduced)>mp.mpf('1e-65'):
            raise RuntimeError('EXACT_W_BACKGROUND_FORMULA_FAIL')
        if not (0<w<mp.mpf('1.2e-14') and 0<ca<mp.mpf('1.2e-14')):
            raise RuntimeError('UNEXPECTED_BENCHMARK_W_BOUND_FAIL')
        rows.append({'a':astr,'Z':mp.nstr(Z,24),'w_A':mp.nstr(w,24),
                     'c_a2':mp.nstr(ca,24),'Q':mp.nstr(Q,24)})
    return {'K_Q_today_I0':mp.nstr(I0,24),'calibration_target_3Omega_cdm_H0sq':mp.nstr(target,24),
            'Z_today':mp.nstr(z1,24),'rows':rows,
            'w_A_upper_bound_over_a_in_(0,1]': '1.2e-14',
            'relative_dust_ic_density_error_scaling':'O(w_A) for fixed leading adiabatic amplitude'}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--repo-root',type=Path,default=Path(__file__).resolve().parents[2])
    ap.add_argument('--no-source-lock',action='store_true')
    ap.add_argument('--out',type=Path)
    args=ap.parse_args()
    if not args.no_source_lock: source_locks(args.repo_root.resolve())
    gates=symbolic()
    bg=background()
    report={
      'classification':'GE19_FROZEN_EXP_LEADING_RADIATION_ADIABATIC_MODE_SUPPORTED_NOT_FULL_PHYSICS_GO',
      'original_sources_locked':not args.no_source_lock,
      'source_blobs': LOCKS if not args.no_source_lock else {},
      'mode_limit':'k*tau -> 0, rho_A/rho_r -> 0; tight-coupled photons; radiation-dominated background',
      'one_physical_mode_amplitude':'Psi0',
      'free_streaming_neutrino_fraction':'Rnu = rho_free_streaming_radiation / rho_total_radiation',
      'leading_mode':{
        'Psi':'Psi0','Phi':'(1+2*Rnu/5)*Psi0',
        'delta_gamma':'-2*Psi0','delta_nu':'-2*Psi0',
        'delta_b':'-3*Psi0/2','delta_A':'-3*(1+w_A)*Psi0/2',
        'theta_gamma':'k^2*tau*Psi0/2',
        'theta_nu':'k^2*tau*Psi0/2',
        'theta_b':'k^2*tau*Psi0/2',
        'theta_A':'k^2*tau*Psi0/2',
        'sigma_nu':'k^2*tau^2*Psi0/15',
        'varphi_A':'a*Q*tau*Psi0/2','alpha_A':'-a*tau*Psi0/2',
        'delta_Q':'-3*Q*c_a^2*Psi0/2','chi':'0 leading',
        'E_A':'0 leading','q_j':'0 selected no-free-bath-mode leading',
        'p_j':'0 selected no-free-bath-mode leading'},
      'symbolic_gates':gates,
      'frozen_exp_background':bg,
      'original_dust_IC_exactly_adiabatic_for_nonzero_w':False,
      'legacy_IC_formal_discrepancy_actual_frozen_exp_tiny':True,
      'full_coupled_next_order_in_k_tau_and_rhoA_over_rhor_solved':False,
      'all_CLASS_approximation_switches_certified':False,
      'finite_eta_numerical_transfer_converged':False,
      'production_physics_go':False,'DES_detection':False,
      'caveat':'A leading-order radiation growing mode, not a finite-k full Einstein-AeST-NL0B primordial eigenmode.'
    }
    print('GE19_FROZEN_EXP_LEADING_GROWING_MODE_PASS',len(gates),flush=True)
    print('GE19_FROZEN_EXP_EARLY_W_A_UPPER_BOUND',bg['w_A_upper_bound_over_a_in_(0,1]'],flush=True)
    print('GE19_FULL_PHYSICS_GO False',flush=True)
    if args.out:
        dest=args.out.expanduser().resolve()
        if dest.exists():raise RuntimeError('REFUSE_OUTPUT_OVERWRITE')
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
        print('GE19_GROWING_MODE_REPORT',str(dest),flush=True)

if __name__=='__main__':main()
