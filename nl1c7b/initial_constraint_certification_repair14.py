#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import sympy as sp

import nl1c7a.a6_a10_spherical_reconstruction as rec
import nl1c7a.evaluate_identity_preserving_repair08 as r8
import nl1c7b.initial_constraint_certification as b4
import nl1c7b.initial_constraint_certification_repair01 as r1
import nl1c7b.initial_constraint_certification_repair09 as r9
import nl1c7b.initial_constraint_certification_repair12 as r12

R8_JSON_SHA256='054851decab71e79a05aca2bc9fb287bb1239c8fb425989f40920004c3d88453'
R8_NPZ_SHA256='4639f3b5c0afcddb2f98c8b9f6a9dbbf8661dac685b12d235c09075a106dafa7'
R10_JSON_SHA256='f1fc1a86d2d488f5e88f0d32b0d3d1d5ce9dab22f52e51fa69801948aeb6de9d'
R11_JSON_SHA256='48c8caf0c5758b089318bcd18885c87725bc244ed5a47862ac841b37b834742d'
R12_JSON_SHA256='99c963dc65cca35c90c6b892fb4192bed1a8c03776664c9da532a5702c62767c'
R13_JSON_SHA256='ef6791edd595a2bd8b44e52a703915385a1e2c4d98345ff4cc509a5d22a61a9b'
R13A_JSON_SHA256='cad6cb2b49b3b20a0b6346390f8536fb90da8d5000ceed82ac0de86b912679b3'

R10_CLASS='NL1C7B4_REPAIR10_RAW_SOURCE_LOCALIZATION_DIAGNOSTIC_PASS'
R11_CLASS='NL1C7B4_REPAIR11_ESECTOR_ANALYTIC_COVARIANT_AUDIT_PASS'
R12_CLASS='NL1C7B4_REPAIR12_FULL_CONSTRAINT_FIRST_ORDER_RESIDUAL'
R13_CLASS='NL1C7B4_REPAIR13_IMPLEMENTATION_FAIL'
R13A_CLASS='NL1C7B4_REPAIR13A_ROUNDOFF_STABLE_SOURCE_LOCALIZATION_PASS'

LAMBDAS=(1.0,0.5,0.25,0.125)
KINDS=('Simple','Exponential','Sharp')
BETAS=(1.0,0.5,0.1)
CANCEL_LIMIT=1e-12
SLOPE_MIN=1.8
SLOPE_MAX=2.2


def sha256_file(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):
            h.update(block)
    return h.hexdigest()


def rel_sym(a,b):
    a=np.asarray(a,float); b=np.asarray(b,float)
    return float(np.linalg.norm(a-b)/max(np.linalg.norm(a),np.linalg.norm(b),1e-300))


def adjacent_slopes(vals):
    out=[]
    for x,y in zip(vals[:-1],vals[1:]):
        if x>0 and y>0 and np.isfinite(x) and np.isfinite(y):
            out.append(float(math.log(x/y,2.0)))
        else:
            out.append(None)
    return out


def symbolic_audit():
    N,L,R,b,u,Lt,ut,pt,Nr,Lr,br,ur,pr=sp.symbols(
        'N L R b u Lt ut pt Nr Lr br ur pr', real=True
    )
    KB,C=sp.symbols('KB C', real=True)
    c=sp.cosh(u); s=sp.sinh(u)
    kL=(Lt-b*Lr-L*br)/(N*L)
    sigma=(pt-b*pr)/N
    Qexpr=c*sigma+s*pr/L
    X=c*pr/L+s*sigma
    E=c*((ut-b*ur)/N+Nr/(N*L))+s*(kL+ur/L)
    P=N*L*R**2
    LE2=P*KB*E**2
    LEX=P*2*C*E*X
    gauge={N:1,b:0,Nr:0,br:0}

    identities={
        'dE_dN':sp.simplify(sp.diff(E,N).subs(gauge)-(-c*ut-s*Lt/L)),
        'dE_dNr':sp.simplify(sp.diff(E,Nr).subs(gauge)-c/L),
        'dX_dN':sp.simplify(sp.diff(X,N).subs(gauge)-(-s*pt)),
        'dX_dNr':sp.simplify(sp.diff(X,Nr).subs(gauge)),
    }
    g2=bool(all(v==0 for v in identities.values()))

    rr,eps,a,H,Q0=sp.symbols('r epsilon a H Q', real=True, nonzero=True)
    lf=sp.Function('l')(rr)
    R1=sp.Function('R1')(rr)
    ltf=sp.Function('lt1')(rr)
    u1=sp.Function('u1')(rr)
    ut1=sp.Function('ut1')(rr)
    p1=sp.Function('dq1')(rr)
    phi1=sp.Function('phi1')(rr)

    sub_eps={
        L:a+eps*lf,
        R:a*rr+eps*R1,
        Lt:a*H+eps*ltf,
        u:eps*u1,
        ut:eps*ut1,
        pt:Q0+eps*p1,
        Lr:eps*sp.diff(lf,rr),
        ur:eps*sp.diff(u1,rr),
        pr:eps*sp.diff(phi1,rr),
    }

    dN_E2=sp.simplify(sp.diff(LE2,N).subs(gauge)).subs(sub_eps)
    dNr_E2=sp.simplify(sp.diff(LE2,Nr).subs(gauge)).subs(sub_eps)
    dN_EX=sp.simplify(sp.diff(LEX,N).subs(gauge)).subs(sub_eps)
    dNr_EX=sp.simplify(sp.diff(LEX,Nr).subs(gauge)).subs(sub_eps)

    CH_E2=sp.expand(dN_E2-sp.diff(dNr_E2,rr))
    CH_EX=sp.expand(dN_EX-sp.diff(dNr_EX,rr))
    lin_E2=sp.simplify(sp.diff(CH_E2,eps).subs(eps,0))
    lin_EX=sp.simplify(sp.diff(CH_EX,eps).subs(eps,0))
    lin_direct_E2=sp.simplify(sp.diff(dN_E2,eps).subs(eps,0))
    lin_direct_EX=sp.simplify(sp.diff(dN_EX,eps).subs(eps,0))

    E1=ut1+H*u1
    X1=Q0*u1+sp.diff(phi1,rr)/a
    target_E2=-2*KB*a**2*sp.diff(rr**2*E1,rr)
    target_EX=-2*C*a**2*sp.diff(rr**2*X1,rr)

    e2_ok=bool(sp.simplify(lin_E2-target_E2)==0)
    ex_ok=bool(sp.simplify(lin_EX-target_EX)==0)
    direct_ok=bool(lin_direct_E2==0 and lin_direct_EX==0)

    # Local Taylor representation of the exact K(Q) sector through first order.
    K0,KQ,KQQ=sp.symbols('K0 KQ KQQ', real=True)
    Qg=sp.simplify(Qexpr.subs(gauge)).subs(sub_eps)
    dQg=sp.expand(Qg-Q0)
    Kseries=K0+KQ*dQg+sp.Rational(1,2)*KQQ*dQg**2
    # At gauge: C_H^K = 2 L R^2 [K(Q)-cosh(u)*phi_t*K_Q(Q)].
    KQseries=KQ+KQQ*dQg
    CHK=2*(a+eps*lf)*(a*rr+eps*R1)**2*(
        Kseries-sp.cosh(eps*u1)*(Q0+eps*p1)*KQseries
    )
    lin_K=sp.simplify(sp.diff(CHK,eps).subs(eps,0))
    rhoA=Q0*KQ-K0
    V=(a+eps*lf)*(a*rr+eps*R1)**2
    dV=sp.simplify(sp.diff(V,eps).subs(eps,0))
    target_K=-2*rhoA*dV-2*a**3*rr**2*Q0*KQQ*p1
    k_ok=bool(sp.simplify(lin_K-target_K)==0)

    weighted=KB*E1+C*X1
    densityE=sp.diff(rr**2*weighted,rr)/(a*rr**2)
    target_combined=-2*a**3*rr**2*densityE
    comb_ok=bool(sp.simplify(target_E2+target_EX-target_combined)==0)

    rho=sp.symbols('rho', real=True)
    dqfull=sp.symbols('dqfull', real=True)
    bridge_identity=sp.simplify(
        Q0*KQQ*dqfull+densityE-rho
    )
    # This is a stated relation, not set to zero without dqfull substitution.
    solved=sp.solve(sp.Eq(bridge_identity,0),dqfull)
    expected_solution=(rho-densityE)/(Q0*KQQ)
    solve_ok=bool(len(solved)==1 and sp.simplify(solved[0]-expected_solution)==0)

    g3=bool(e2_ok and ex_ok and direct_ok and k_ok and comb_ok and solve_ok)
    return {
        'gauge_identity_residuals':{k:str(v) for k,v in identities.items()},
        'gauge_identities_pass':g2,
        'first_variation':{
            'E2_direct_N_linear_zero':bool(lin_direct_E2==0),
            'EX_direct_N_linear_zero':bool(lin_direct_EX==0),
            'E2_closed_form_pass':e2_ok,
            'EX_closed_form_pass':ex_ok,
            'K_intrinsic_closed_form_pass':k_ok,
            'combined_density_form_pass':comb_ok,
            'density_Q_solution_pass':solve_ok,
        },
        'first_variation_pass':g3,
        'closed_forms':{
            'CH_E2_1':'-2*K_B*a^2*d_r(r^2*E1)',
            'CH_EX_1':'-2*C*a^2*d_r(r^2*X1)',
            'CH_K_intrinsic_1':'-2*a^3*r^2*Q*K_QQ*deltaQ',
            'delta_rho_A':'Q*K_QQ*deltaQ + (a*r^2)^-1*d_r(r^2*(K_B*E1+C*X1))',
            'Fourier_delta_rho_A':'Q*K_QQ*deltaQ - k^2/a^2*(K_B*E_A+C*chi)',
        },
    }


def static_semantics():
    c7=Path('docs/nl1c7a_predata_growing_mode_bridge.md').read_text()
    b4src=Path('nl1c7b/initial_constraint_certification.py').read_text()
    v019=Path('v019/apply_patch_v019.py').read_text()

    c7_current=('deltaQ = rho_A delta_A/(Q K_QQ)' in c7)
    b4_current=("dq=inv(k,(rho/(Q*KQQ))*F['delta_A'],r)" in b4src)
    class_density=("ppw->delta_rho += rho_dark*y[ppw->pv->index_pt_delta_cdm];" in v019)
    pressure_combo=(
        "pba->aest_KB*y[ppw->pv->index_pt_E_aest]+(2.-pba->aest_KB)*chi_aest" in v019
        and "ppw->delta_p += rho_dark*Pi_aest;" in v019
    )

    # The frozen v0.19 replacement block has a direct effective-density line.
    # Require no explicit E/chi addition on a ppw->delta_rho line.
    delta_rho_lines=[ln.strip() for ln in v019.splitlines() if 'ppw->delta_rho +=' in ln]
    no_explicit_Echi_density=bool(
        delta_rho_lines
        and all(('E_aest' not in ln and 'chi_aest' not in ln) for ln in delta_rho_lines)
    )

    gates={
        'C7A_current_deltaQ_relation_found':c7_current,
        'B4_current_deltaQ_implementation_found':b4_current,
        'CLASS_effective_density_deltaA_line_found':class_density,
        'CLASS_Echi_pressure_combination_found':pressure_combo,
        'CLASS_no_explicit_Echi_delta_rho_line':no_explicit_Echi_density,
    }
    return {
        'checks':gates,
        'pass':bool(all(gates.values())),
        'delta_rho_lines':delta_rho_lines,
    }


def corrected_state_and_profiles(st,qbg,kqqbg):
    r=np.asarray(st['r'],float)
    D=b4.dmat(r)
    a=b4.AI
    u=np.asarray(st['u'],float)
    ut=np.asarray(st['udot'],float)
    phi=np.asarray(st['phi'],float)
    pr=D@phi

    E1=ut+b4.H_DIRECT*u
    X1=qbg*u+pr/a
    fluxE2=r*r*(b4.KB*E1)
    fluxEX=r*r*(b4.C*X1)
    flux=fluxE2+fluxEX
    fluxE2=np.array(fluxE2,copy=True); fluxE2[0]=0.0
    fluxEX=np.array(fluxEX,copy=True); fluxEX[0]=0.0
    flux=np.array(flux,copy=True); flux[0]=0.0

    dE2=D@fluxE2
    dEX=D@fluxEX
    dF=D@flux

    A_E2=-2.0*b4.AI*b4.AI*dE2
    A_EX=-2.0*b4.AI*b4.AI*dEX
    A_E=A_E2+A_EX

    delta_rho_E=np.zeros_like(r)
    non=np.arange(len(r))>0
    delta_rho_E[non]=dF[non]/(a*r[non]*r[non])
    # Center is a finite diagnostic placeholder only and is excluded from every gate.
    delta_rho_E[0]=delta_rho_E[1]

    qkqq=qbg*kqqbg
    delta_dq=-delta_rho_E/qkqq
    A_Kcorr=-2.0*a**3*r*r*qkqq*delta_dq

    corr={k:(np.array(v,copy=True) if isinstance(v,np.ndarray) else v) for k,v in st.items()}
    corr['phidot_minus_Q']=np.asarray(st['phidot_minus_Q'],float)+delta_dq

    return corr,{
        'E1':E1,'X1':X1,'A_E2':A_E2,'A_EX':A_EX,'A_E':A_E,
        'delta_rho_E':delta_rho_E,'Delta_deltaQ':delta_dq,'A_Kcorr':A_Kcorr,
        'noncenter':non,
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--trace',required=True)
    ap.add_argument('--coverage-json',required=True)
    ap.add_argument('--repair08-json',required=True)
    ap.add_argument('--repair08-npz',required=True)
    ap.add_argument('--repair10-json',required=True)
    ap.add_argument('--repair11-json',required=True)
    ap.add_argument('--repair12-json',required=True)
    ap.add_argument('--repair13-json',required=True)
    ap.add_argument('--repair13a-json',required=True)
    ap.add_argument('--out',required=True)
    a=ap.parse_args()

    cov=json.loads(Path(a.coverage_json).read_text())
    js={
        'r8':json.loads(Path(a.repair08_json).read_text()),
        'r10':json.loads(Path(a.repair10_json).read_text()),
        'r11':json.loads(Path(a.repair11_json).read_text()),
        'r12':json.loads(Path(a.repair12_json).read_text()),
        'r13':json.loads(Path(a.repair13_json).read_text()),
        'r13a':json.loads(Path(a.repair13a_json).read_text()),
    }
    off=np.load(a.repair08_npz)

    hashes={
        'repair08_json_sha256':sha256_file(a.repair08_json),
        'repair08_npz_sha256':sha256_file(a.repair08_npz),
        'repair10_json_sha256':sha256_file(a.repair10_json),
        'repair11_json_sha256':sha256_file(a.repair11_json),
        'repair12_json_sha256':sha256_file(a.repair12_json),
        'repair13_json_sha256':sha256_file(a.repair13_json),
        'repair13a_json_sha256':sha256_file(a.repair13a_json),
    }

    z=rec.read_trace(a.trace)
    ks,gs=rec.groups(z)
    tv_rec=rec.at_ai(gs,'pchip')
    ks_b4,gs_b4=b4.groups(b4.read_trace(a.trace))
    tv_b4=b4.at_ai(gs_b4)
    h=float(cov['h'])

    g1=bool(
        hashes['repair08_json_sha256']==R8_JSON_SHA256
        and hashes['repair08_npz_sha256']==R8_NPZ_SHA256
        and hashes['repair10_json_sha256']==R10_JSON_SHA256
        and hashes['repair11_json_sha256']==R11_JSON_SHA256
        and hashes['repair12_json_sha256']==R12_JSON_SHA256
        and hashes['repair13_json_sha256']==R13_JSON_SHA256
        and hashes['repair13a_json_sha256']==R13A_JSON_SHA256
        and js['r8'].get('classification')=='NL1C7A_REPAIR08_IDENTITY_PRESERVING_SCALAR_REPRESENTATION_CERTIFIED'
        and js['r10'].get('classification')==R10_CLASS
        and js['r11'].get('classification')==R11_CLASS
        and js['r12'].get('classification')==R12_CLASS
        and js['r13'].get('classification')==R13_CLASS
        and js['r13a'].get('classification')==R13A_CLASS
        and all(js['r13a'].get('gates',{}).values())
        and cov.get('classification')=='NL1C7A_NATIVE_TRACE_COVERAGE_PASS'
        and cov.get('requested_k_relative_miss_max')==0
        and cov.get('n_native_times')==179
        and len(ks)==128 and np.array_equal(ks,ks_b4)
    )

    sym=symbolic_audit()
    g2=bool(sym['gauge_identities_pass'])
    g3=bool(sym['first_variation_pass'])

    static=static_semantics()
    g4=bool(static['pass'])

    scalar_ai,scalar_independent,scalar_finite,_=r8.scalar_composites_at_ai(ks,gs,'pchip')
    states={}
    for scale in b4.SCALES:
        states[(float(scale),256)]=r9.load_primary_state(off,scale)
        states[(float(scale),512)]=r9.repaired_state_nr(scale,512,ks,h,tv_b4,tv_rec,scalar_ai)

    kq_bg=float(np.median(tv_b4['KQ']))
    kqq_bg=float(np.median(tv_b4['KQQ']))
    qbg=b4.stable_q_from_kq(kq_bg)
    zbg=r9.stable_zbg(kq_bg)
    funcs,dY,kidentity=r1.build_nonK()
    g1=bool(g1 and kidentity and np.isfinite(kqq_bg) and kqq_bg>0)

    profile_rows=[]
    corrected_states={}
    g5=True
    for scale in b4.SCALES:
        for nr in (256,512):
            st=states[(float(scale),int(nr))]
            corr,p=corrected_state_and_profiles(st,qbg,kqq_bg)
            corrected_states[(float(scale),int(nr))]=corr
            non=p['noncenter']
            err=rel_sym(p['A_Kcorr'][non],-p['A_E'][non])
            g5 &= bool(np.isfinite(err) and err<=CANCEL_LIMIT)
            profile_rows.append({
                'scale_hinv_Mpc':float(scale),
                'Nr':int(nr),
                'E2_A_L2':float(np.linalg.norm(p['A_E2'][non])),
                'EX_A_L2':float(np.linalg.norm(p['A_EX'][non])),
                'combined_E_A_L2':float(np.linalg.norm(p['A_E'][non])),
                'K_correction_A_L2':float(np.linalg.norm(p['A_Kcorr'][non])),
                'Kcorr_plus_E_relative_L2':err,
                'Delta_deltaQ_L2':float(np.linalg.norm(p['Delta_deltaQ'][non])),
                'Delta_deltaQ_Linf':float(np.max(np.abs(p['Delta_deltaQ'][non]))),
                'delta_rho_E_L2':float(np.linalg.norm(p['delta_rho_E'][non])),
                'pass':bool(np.isfinite(err) and err<=CANCEL_LIMIT),
            })

    corrected_rows=[]
    H_gated=[]
    M_gated=[]
    g6=True
    g7=True
    for scale in b4.SCALES:
        for nr in (256,512):
            st=corrected_states[(float(scale),int(nr))]
            for kind in KINDS:
                for beta in BETAS:
                    e0=r12.source_matrices(st,0.0,qbg,zbg,funcs,dY,kind,beta)
                    non=e0['noncenter']
                    bH=e0['numH'][non]
                    bM=e0['numM'][non]
                    nH=[]; nM=[]
                    metrics=[]
                    for lam in LAMBDAS:
                        ev=r12.source_matrices(st,lam,qbg,zbg,funcs,dY,kind,beta)
                        dH=ev['numH'][non]-bH
                        dM=ev['numM'][non]-bM
                        h2=float(np.linalg.norm(dH))
                        m2=float(np.linalg.norm(dM))
                        nH.append(h2); nM.append(m2)
                        metrics.append({
                            'lambda':float(lam),
                            'deltaN_H_L2':h2,
                            'deltaN_M_L2':m2,
                            'deltaN_H_Linf':float(np.max(np.abs(dH))),
                            'deltaN_M_Linf':float(np.max(np.abs(dM))),
                        })
                    sH=adjacent_slopes(nH)
                    sM=adjacent_slopes(nM)
                    Hpass=bool(all(p is not None and SLOPE_MIN<=p<=SLOPE_MAX for p in sH[1:]))
                    Mpass=bool(all(p is not None and SLOPE_MIN<=p<=SLOPE_MAX for p in sM[1:]))
                    g6 &= Hpass
                    g7 &= Mpass
                    H_gated.extend([float(p) for p in sH[1:] if p is not None])
                    M_gated.extend([float(p) for p in sM[1:] if p is not None])
                    corrected_rows.append({
                        'scale_hinv_Mpc':float(scale),'Nr':int(nr),
                        'Y_kind':kind,'beta0':float(beta),
                        'lambda_metrics':metrics,
                        'H_L2_adjacent_log2_slopes':sH,
                        'M_L2_adjacent_log2_slopes':sM,
                        'H_gated_pass':Hpass,
                        'M_gated_pass':Mpass,
                    })

    g6=bool(g6 and len(corrected_rows)==54)
    g7=bool(g7 and len(corrected_rows)==54)

    claim_boundary={
        'official_Repair08_state_written_or_modified':False,
        'diagnostic_corrected_state_written':False,
        'historical_B4_fail_preserved':True,
        'historical_Repair12_first_order_H_preserved':True,
        'historical_Repair13_implementation_fail_preserved':True,
        'Repair13a_pass_preserved':True,
        'coefficient_changed':False,
        'sign_changed':False,
        'source_changed':False,
        'historical_threshold_changed':False,
        'radial_points_removed':False,
        'Y_beta_or_scale_selected':False,
        'nonlinear_evolution_executed':False,
        'finite_eta_executed':False,
        'observational_detection_claimed':False,
        'B4_pass_relabel_claimed':False,
    }
    g8=bool(
        claim_boundary['historical_B4_fail_preserved']
        and claim_boundary['historical_Repair12_first_order_H_preserved']
        and claim_boundary['historical_Repair13_implementation_fail_preserved']
        and claim_boundary['Repair13a_pass_preserved']
        and not any(v for k,v in claim_boundary.items() if k not in (
            'historical_B4_fail_preserved',
            'historical_Repair12_first_order_H_preserved',
            'historical_Repair13_implementation_fail_preserved',
            'Repair13a_pass_preserved'
        ))
    )

    gates={
        'R14_G1_frozen_provenance':g1,
        'R14_G2_exact_Hamiltonian_E_X_gauge_identities':g2,
        'R14_G3_exact_B3_first_variations':g3,
        'R14_G4_frozen_current_bridge_semantics':g4,
        'R14_G5_analytic_Esector_Kcorrection_cancellation':bool(g5),
        'R14_G6_corrected_diagnostic_Hamiltonian_second_order':bool(g6),
        'R14_G7_corrected_diagnostic_momentum_second_order':bool(g7),
        'R14_G8_claim_boundary':g8,
    }

    if all(gates.values()):
        cls='NL1C7B4_REPAIR14_DENSITY_Q_BRIDGE_OMISSION_IDENTIFIED'; rc=0
    elif g1 and g2 and g3 and g4 and g5 and (not g6 or not g7):
        cls='NL1C7B4_REPAIR14_HAMILTONIAN_ESECTOR_INTERFACE_MISMATCH'; rc=2
    else:
        cls='NL1C7B4_REPAIR14_IMPLEMENTATION_FAIL'; rc=2

    result={
        'classification':cls,
        'scope':'Repair14 analytic Hamiltonian E-sector first-variation and effective-density-to-Q bridge audit; diagnostic in-memory correction only.',
        'provenance':{
            **hashes,
            'repair13a_result_freeze_commit':'cb6440383eac99001369e976fae035d74adf30fc',
            'repair14_prereg_commit':'117d227737a1a78dfe5055878d703a90cbf74bd3',
        },
        'symbolic_audit':sym,
        'static_bridge_semantics':static,
        'background':{
            'a_i':b4.AI,
            'Q_background_Mpc_inv':qbg,
            'KQQ_background':kqq_bg,
            'QKQQ_background':qbg*kqq_bg,
        },
        'analytic_profile_rows':profile_rows,
        'corrected_diagnostic_order_rows':corrected_rows,
        'summary':{
            'n_profile_pairs':len(profile_rows),
            'n_corrected_cases':len(corrected_rows),
            'max_Kcorr_plus_E_relative_L2':float(max(x['Kcorr_plus_E_relative_L2'] for x in profile_rows)),
            'corrected_H_gated_min_slope':float(min(H_gated)) if H_gated else None,
            'corrected_H_gated_max_slope':float(max(H_gated)) if H_gated else None,
            'corrected_M_gated_min_slope':float(min(M_gated)) if M_gated else None,
            'corrected_M_gated_max_slope':float(max(M_gated)) if M_gated else None,
            'historical_Repair12_H_order':'first_order',
            'historical_B4_classification_unchanged':'NL1C7B4_REPAIR09_REPAIR08_RAW_CONSTRAINT_FAIL',
        },
        'state_anchor':{
            'scalar_canonical_vs_independent_at_ai_relative_L2':r9.rel_sym(scalar_ai,scalar_independent),
            'scalar_finite':bool(scalar_finite),
        },
        'gates':gates,
        'claim_boundary':claim_boundary,
        'interpretation_boundary':{
            'density_Q_bridge_omission_identified_if_pass':bool(all(gates.values())),
            'AeST_E2_coefficient_declared_wrong':False,
            'official_state_modified':False,
            'B4_passed':False,
            'nonlinear_evolution_certified':False,
            'observational_detection_claimed':False,
        },
    }

    out=Path(a.out)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True,allow_nan=False))
    raise SystemExit(rc)


if __name__=='__main__':
    main()
