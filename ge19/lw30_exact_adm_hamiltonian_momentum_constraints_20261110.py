#!/usr/bin/env python3
"""GE19 LW30: exact reduced 3+1 ADM lapse/shift and CLASS scalar constraints.

Exact first variations of frozen plane-symmetric GE06 GR + AeST + GE05
about relaxed FLRW, restricted to Newtonian-gauge scalar Fourier modes.
This is NOT full 3+1 tensor/vector/Y/species/action-to-CLASS closure.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess
from pathlib import Path
import sympy as s

ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/'ge19/lw30_exact_adm_hamiltonian_momentum_constraints_predata_20261110.json'
PRE_BLOB='5cce6d6c0736f42feff691ce4370d783dad1d8f2'


def require(ok, why):
    if not bool(ok):
        raise RuntimeError('GE19_LW30_'+why)


def gitblob(path):
    return subprocess.check_output(['git','hash-object',str(path)],cwd=ROOT,text=True).strip()


def file_sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1<<20), b''):
            h.update(block)
    return h.hexdigest()


def symbolic():
    N,L,R,b,u,pt,px,ut,ux,Nx,Lt,Lx,bx,Rt,Rx,qt,qx,q=s.symbols(
        'N L R b u pt px ut ux Nx Lt Lx bx Rt Rx qt qx q',real=True)
    KB,C,K0,KQ,KQQ,eta,omega,sw=s.symbols('KB C K0 KQ KQQ eta omega sw',real=True)
    a,H,Q,eps,k=s.symbols('a H Q eps k',real=True,nonzero=True)
    psi,Phi,Phidot,shift,alpha,alphadot,varphi,varphidot,q1,qd=s.symbols(
        'psi Phi Phidot shift alpha alphadot varphi varphidot q1 qd',real=True)
    kL=(Lt-b*Lx-L*bx)/(N*L)
    kR=(Rt-b*Rx)/(N*R)
    sigma=(pt-b*px)/N
    ch,sh=s.cosh(u),s.sinh(u)
    Qi=ch*sigma+sh*px/L
    Xi=sh*sigma+ch*px/L
    E=ch*((ut-b*ux)/N+Nx/(N*L))+sh*(kL+ux/L)
    Aq=ch*(qt-b*qx)/N+sh*qx/L
    vol=N*L*R**2
    K=s.Function('K')
    GR=vol*(-4*kL*kR-2*kR**2)+2*N*Rx**2/L+4*Nx*R*Rx/L
    AE=vol*(KB*E**2+2*C*E*Xi-C*Xi**2+2*K(Qi))
    bath=eta*vol*s.Rational(1,4)*(Aq**2-(omega*q-sw*Xi)**2)
    # Use a complex Fourier mode as a linear perturbation label;
    # only the coefficient linear in eps enters each Euler variation.
    fields={N:1+eps*psi,L:a*(1-eps*Phi),R:a*(1-eps*Phi),
       b:eps*shift,u:eps*s.I*k*alpha/a,
       pt:Q+eps*varphidot,px:eps*s.I*k*varphi,
       ut:eps*s.I*k*(alphadot-H*alpha)/a,ux:0,Nx:eps*s.I*k*psi,
       Lt:a*H*(1-eps*Phi)-eps*a*Phidot,
       Lx:-a*eps*s.I*k*Phi,bx:eps*s.I*k*shift,
       Rt:a*H*(1-eps*Phi)-eps*a*Phidot,
       Rx:-a*eps*s.I*k*Phi,qt:eps*qd,qx:0,q:eps*q1}
    def replaceK(t):
        return t.subs(s.Derivative(K(Q),Q,2),KQQ).subs(
            s.Derivative(K(Q),Q),KQ).subs(K(Q),K0)
    def lin(src,field):
        z=s.diff(s.diff(src,field).subs(fields),eps).subs(eps,0).doit()
        return s.simplify(replaceK(z))
    def zero(e):
        return s.simplify(s.factor(e))==0
    Ngr=lin(GR,N)-s.I*k*lin(GR,Nx)
    Nae=lin(AE,N)-s.I*k*lin(AE,Nx)
    Nba=lin(bath,N)-s.I*k*lin(bath,Nx)
    bgr=lin(GR,b)-s.I*k*lin(GR,bx)
    bae=lin(AE,b)-s.I*k*lin(AE,bx)
    bba=lin(bath,b)-s.I*k*lin(bath,bx)
    EN=s.simplify(Ngr+Nae+Nba)
    Eb=s.simplify(bgr+bae+bba)
    EN0=s.simplify(replaceK(s.diff(GR+AE+bath,N).subs(fields).subs(eps,0).doit()))
    background=3*H**2-(Q*KQ-K0)
    rho=(Q*KQ-K0)/3
    pressure=K0/3
    DA=(Q*KQQ*(varphidot-Q*psi)
        -k*k/a**2*(KB*(alphadot+psi)+C*(varphi+Q*alpha)))/3
    TA=(rho+pressure)*k*k*varphi/(a*Q)
    mom=Phidot+H*psi-s.Rational(3,2)*a*TA/k**2
    CH=k*k*Phi/a**2+3*H*(Phidot+H*psi)+s.Rational(3,2)*DA
    CHclass=k*k*Phi/a**2+s.Rational(3,2)*(DA+3*a*H*TA/k**2)
    checks={
      'background_friedmann_lapse':zero(EN0-2*a**3*background),
      'GR_shift_4a3ik_Phidot_Hpsi':zero(bgr-4*a**3*s.I*k*(Phidot+H*psi)),
      'AeST_shift_minus_2a3ik_KQ_varphi':zero(bae+2*a**3*s.I*k*KQ*varphi),
      'bath_shift_direct_linear_zero':zero(bba),
      'full_momentum_equal_CLASS':zero(Eb-4*a**3*s.I*k*mom),
      'GR_lapse_grad_4aik_Phi':zero(lin(GR,Nx)+4*a*s.I*k*Phi),
      'AeST_lapse_grad_from_E_chi':zero(lin(AE,Nx)-2*a*s.I*k*(KB*(alphadot+psi)+C*(varphi+Q*alpha))),
      'bath_lapse_direct_linear_zero':zero(Nba),
      'full_Hamiltonian_offshell_background_residual':zero(
           EN.subs(shift,0)+4*a**3*CH+6*a**3*Phi*background),
      'Hamiltonian_on_background':zero(
           s.expand(EN.subs(shift,0)+4*a**3*CH).subs(H**2,(Q*KQ-K0)/3)),
      'Hamiltonian_to_CLASS_using_momentum':zero(
           (CH-CHclass).subs(Phidot,s.Rational(3,2)*a*TA/k**2-H*psi)),
      'enthalpy_QKQ_over_three':zero(rho+pressure-Q*KQ/3),
      'velocity_phase_momentum_dictionary':zero(TA-(rho+pressure)*k*k*varphi/(a*Q)),
      'negative_wrong_GR_shift_factor':not zero(bgr-2*a**3*s.I*k*(Phidot+H*psi)),
      'negative_missing_AeST_shift':not zero(Eb-bgr),
      'negative_drop_AeST_lapse_gradient':not zero(lin(AE,Nx)),
      'negative_wrong_friedmann_background':not zero(EN0-2*a**3*(3*H**2-2*(Q*KQ-K0))),
    }
    failed=[key for key,v in checks.items() if not bool(v)]
    if failed:print('GE19_LW30_FAILED_GATES',failed,flush=True)
    require(not failed,'SYMBOLIC_ACTION_CONSTRAINT_FAIL')
    results={
     'background_lapse':'E_N0/(2a^3)=3H^2-(Q*K_Q-K)',
     'Einstein_AeST_momentum':'E_b^(1)=4*i*k*a^3*(Phi_dot+H*Psi-K_Q*varphi/2)',
     'Einstein_AeST_Hamiltonian':'E_N^(1)|b=0+4a^3*C_H+6a^3*Phi*[3H^2-(Q*K_Q-K)]=0',
     'C_H':'k^2*Phi/a^2+3H*(Phi_dot+H*Psi)+3*delta_rho_A/2',
     'delta_rho_A':'(Q*K_QQ*(varphi_dot-Q*Psi)-k^2/a^2*(K_B*(alpha_dot+Psi)+(2-K_B)*(varphi+Q*alpha)))/3',
     'C_H_CLASS':'k^2*Phi/a^2+(3/2)*(delta_rho_A+3*a*H*T_A/k^2), using momentum',
     'matter_enthalpy':'rho_A+p_A=Q*K_Q/3',
     'T_A':'(rho_A+p_A)*k^2*varphi/(a*Q)',
     'scope':'Original analytic 3+1 plane-symmetric scalar coframe GR+AeST+GE05; AeST-only FLRW, not all ordinary species, not Y or full gauge/unit-aether map',
    }
    return {k:bool(v) for k,v in checks.items()},results


def parents(parent):
    require(PRE.is_file() and gitblob(PRE)==PRE_BLOB,'PREDATA_CHANGED')
    pre=json.loads(PRE.read_text())
    require(pre['classification']==
       'GE19_LW30_REDUCED_3PLUS1_GR_AEST_ADM_SCALAR_CONSTRAINTS_PRELOCK','CLASSIFICATION_CHANGED')
    for name,want in pre['source_git_blobs'].items():
        f=ROOT/name
        require(f.is_file() and gitblob(f)==want,'SOURCE_CHANGED_'+f.name)
    ge06=(ROOT/'ge06/analytic_aest_directional_source_generator.py').read_text()
    ge05=(ROOT/'ge05/memory_directional_source_generator.py').read_text()
    require('grav=N*L*R**2*(-4*kL*kR-2*kR**2) + 2*N*Rx**2/L + 4*Nx*R*Rx/L' in ge06,
            'GR_ACTION_ANCHOR_CHANGED')
    require('aest=N*L*R**2*(KB*E**2 + 2*C*E*Xinv - C*Xinv**2 + 2*Kfun)' in ge06,
            'AEST_ACTION_ANCHOR_CHANGED')
    require('lag=N*L*R**2*sp.Rational(1,4)*(Aq**2-(om*q-sw*Xphi)**2)' in ge05,
            'BATH_ACTION_ANCHOR_CHANGED')
    require(parent.is_file() and file_sha(parent)==pre['parent_LW29_original_sha256'],
            'ORIGINAL_LW29_SHA_CHANGED')
    d=json.loads(parent.read_text())
    require(d['classification']==
       'GE19_LW29_ORIGINAL_COVARIANT_3D_QUADRATIC_NORMALIZATION_QUARTER_PASS_FULL_ADM_BRIDGE_OPEN'
       and len(d['symbolic_checks'])==15 and all(d['symbolic_checks'].values()),
       'LW29_PARENT_INVALID')
    return pre


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--self-test',action='store_true')
    ap.add_argument('--lw29',type=Path,default=ROOT/
       'results/ge19_lw29_covariant_3d_scalar_quadratic_normalization_20261110_r1.json')
    ap.add_argument('--out',type=Path,default=ROOT/
       'results/ge19_lw30_exact_adm_hamiltonian_momentum_constraints_20261110_r1.json')
    args=ap.parse_args()
    checks,derived=symbolic()
    print('GE19_LW30_GR_AEST_ADM_SCALAR_SELFTEST_PASS',len(checks),flush=True)
    if args.self_test:return
    pre=parents(args.lw29)
    print('GE19_LW30_FROZEN_SOURCE_LOCKS_PASS',len(pre['source_git_blobs']),flush=True)
    out=args.out.resolve()
    require(out.parent.is_dir() and not out.exists(),'OUTPUT_EXISTS_OR_PARENT_MISSING')
    result={
       'classification':'GE19_LW30_REDUCED_3PLUS1_GR_AEST_ADM_SCALAR_CONSTRAINTS_PASS_FULL_ACTION_TO_CLASS_OPEN',
       'symbolic_gates':checks,'derived':derived,
       'predata_git_blob':PRE_BLOB,'source_git_blobs':pre['source_git_blobs'],
       'original_LW29_SHA256':pre['parent_LW29_original_sha256'],
       'unit_aether_and_auxiliary_multiplier_equivalence_certified':False,
       'all_ordinary_species_included':False,
       'full_3plus1_covariant_AeST_Y_and_CLASS_equivalence':False,
       'full_3plus1_shear_equation_certified':False,
       'physical_eta_matter_Weyl_derivative_certified':False,
       'original_CLASS_patch_modified':False,'DES_detection_found':False,
       'LW29_scalar_quadratic_source_normalization_preserved':True,
       'LW22_lensing_geometry_preserved':True
    }
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('GE19_LW30_CLASSIFICATION',result['classification'],flush=True)
    print('GE19_LW30_PHYSICAL_OBSERVER_READY',False,flush=True)
    print('GE19_LW30_OUTPUT',out,flush=True)

if __name__=='__main__': main()
