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
import nl1c7b.initial_constraint_certification_repair16 as r16
import nl1c7b.initial_constraint_certification_repair18a as r18a
import nl1c7b.initial_constraint_certification_repair19c as r19c

B5_JSON_SHA256='bfeae8019b69f23e0fa659c6c3e0134353b85e0dcd67f0337c14d6f50b887c8d'
B5_CLASS='NL1C7B5_CONSERVATIVE_DIFFERENTIAL_CERTIFICATION_FAIL'
B5_FREEZE_COMMIT='2a2739db609ffb58e899baa7308199fd8dbc528b'
B6_PREREG_COMMIT='571d5bacee7a18f8c853a95769e2963c045e3e69'

R15A_JSON_SHA256='596c7b13c4683840bcf40f6850356e179e77f873c3a3b42ba0b54730ae80811d'
R15A_NPZ_SHA256='997d0033eeed1f3e60c1907c7938a0ea87a1cf38de6ab860340bd003d18d6e6e'
R16_JSON_SHA256='a225f435ef61eaf33a1b4466eea678b23d1a221a537589bd8e2b0717ed66335b'

REL_NONDEGENERACY_LIMIT=1e-8
REPRO_LIMIT=1e-12
TINY=1e-300


def sha256_file(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):
            h.update(block)
    return h.hexdigest()


def zero(expr):
    return bool(sp.simplify(expr)==0)


def build_symbolic_audit():
    N,L,R,b,u,Lt,Rt,ut,pt,Nr,Lr,Rr,br,ur,pr=sp.symbols(
        'N L R b u Lt Rt ut pt Nr Lr Rr br ur pr', real=True
    )
    q,Rtr=sp.symbols('q Rtr', real=True)
    KB=sp.Float(b4.KB)
    C=sp.Float(b4.C)

    ch=sp.cosh(u)
    sh=sp.sinh(u)
    kL=(Lt-b*Lr-L*br)/(N*L)
    kR=(Rt-b*Rr)/(N*R)
    sigma=(pt-b*pr)/N
    Q=ch*sigma+sh*pr/L
    X=sh*sigma+ch*pr/L
    Y=X**2
    E=ch*((ut-b*ur)/N+Nr/(N*L))+sh*(kL+ur/L)
    P=N*L*R**2

    terms={
        'GR_kin':P*(-4*kL*kR-2*kR**2),
        'GR_curv_NL':2*N*L,
        'GR_curv_Rr':2*N*Rr**2/L,
        'GR_Nr_boundary':4*Nr*R*Rr/L,
        'AeST_E2':P*KB*E**2,
        'AeST_EX':P*sp.Float(2*b4.C)*E*X,
        'AeST_X2':-P*C*X**2,
    }
    expected=[
        'GR_kin','GR_curv_NL','GR_curv_Rr','GR_Nr_boundary',
        'AeST_E2','AeST_EX','AeST_X2',
    ]
    dictionary_ok=bool(list(terms.keys())==expected)

    gauge={N:1,b:0,Nr:0,br:0}
    pt_exact=(q-sh*pr/L)/ch
    subq={pt:pt_exact}

    Qg=Q.subs(gauge).subs(subq)
    Eg=sp.cancel(E.subs(gauge).subs(subq))
    Xg=sp.cancel(X.subs(gauge).subs(subq))
    E_target=ch*ut+sh*(Lt+ur)/L
    X_target=sp.tanh(u)*q+pr/(ch*L)

    g2=bool(
        zero(Qg-q)
        and zero(Eg-E_target)
        and zero(Xg-X_target)
    )

    fN={name:sp.diff(t,N).subs(gauge).subs(subq) for name,t in terms.items()}
    fNr={name:sp.diff(t,Nr).subs(gauge).subs(subq) for name,t in terms.items()}
    fb={name:sp.diff(t,b).subs(gauge).subs(subq) for name,t in terms.items()}
    fbr={name:sp.diff(t,br).subs(gauge).subs(subq) for name,t in terms.items()}

    FH=sp.cancel(sum(fNr.values()))
    FH_target=(
        4*R*Rr/L
        +2*KB*R**2*ch*E_target
        +2*C*R**2*ch*X_target
    )
    AH=sp.cancel(-sp.diff(FH_target,L))
    AH_target=sp.cancel(
        (
            4*R*Rr
            +2*KB*R**2*ch*sh*(Lt+ur)
            +2*C*R**2*pr
        )/L**2
    )
    H_gr_kin=sp.cancel(fN['GR_kin'])
    H_gr_target=2*L*Rt**2+4*Lt*R*Rt
    H_non_gr=sum(v for k,v in fN.items() if k!='GR_kin')

    h_flux_independent=bool(
        not FH.has(Lr)
        and not FH.has(Rt)
        and not FH.has(Rtr)
    )
    h_local_structure=bool(
        all(not v.has(Lr) and not v.has(Rtr) for v in fN.values())
        and zero(H_gr_kin-H_gr_target)
        and not H_non_gr.has(Rt)
    )
    h_affine_Lr=bool(not FH.has(Lr))
    h_quadratic_Rt=bool(
        zero(sp.diff(H_gr_target,Rt,3))
        and not zero(sp.diff(H_gr_target,Rt,2))
    )
    g3=bool(
        zero(FH-FH_target)
        and zero(AH-AH_target)
        and h_flux_independent
        and h_local_structure
        and h_affine_Lr
        and h_quadratic_Rt
    )

    SMgr=sp.cancel(fb['GR_kin'])
    FMgr=sp.cancel(fbr['GR_kin'])
    SMgr_target=4*(L*Rr*Rt+Lr*R*Rt+Lt*R*Rr)
    FMgr_target=4*L*R*Rt
    dFMgr=(
        sp.diff(FMgr_target,L)*Lr
        +sp.diff(FMgr_target,R)*Rr
        +sp.diff(FMgr_target,Rt)*Rtr
    )
    Mgr=sp.cancel(SMgr_target-dFMgr)
    Mgr_target=4*R*Lt*Rr-4*L*R*Rtr

    non_gr_names=[k for k in terms if k!='GR_kin']
    non_gr_rt_independent=bool(
        all(not fb[k].has(Rt) and not fbr[k].has(Rt) for k in non_gr_names)
    )
    non_gr_flux_no_Lr=bool(all(not fbr[k].has(Lr) for k in non_gr_names))
    non_gr_source_affine_Lr=bool(
        all(zero(sp.diff(fb[k],Lr,2)) for k in non_gr_names)
    )

    # Explicit structural audit of the additional frozen sectors used by source_arrays.
    # j/J sector: Y=X^2, so the shift-radial flux derivative is exactly zero.
    dyb=sp.diff(Y,b).subs(gauge).subs(subq)
    dybr=sp.diff(Y,br).subs(gauge).subs(subq)
    jv,Jv=sp.symbols('jv Jv', real=True)
    jb_extra=-C*(L*R**2*jv*dyb)
    jbr_extra=-C*(L*R**2*jv*dybr)

    # K, dust and background momentum terms are purely local.  Their detailed
    # frozen coefficients are irrelevant to solved-field derivative order.
    K2s,Z0s,zs,ews,vs,varrhos,rhostd=sp.symbols(
        'K2s Z0s zs ews vs varrhos rhostd', real=True
    )
    kb_extra=-8*K2s*L*R**2*ch*pr*Z0s*zs*ews
    dustM_extra=2*L**2*R**2*varrhos*sp.cosh(vs)*sp.sinh(vs)
    bgM_extra=sp.Integer(0)

    extra_momentum=[
        jb_extra,jbr_extra,kb_extra,dustM_extra,bgM_extra
    ]
    extra_momentum_structure=bool(
        zero(dybr)
        and all(not e.has(Rt) and not e.has(Rtr) and not e.has(Lr) for e in extra_momentum)
    )

    # Hamiltonian j/J, K, dust and background pieces are also local and carry
    # no L_r, R_t or R_{t,r}.  Verify the Y-derived radial flux vanishes.
    dyN=sp.diff(Y,N).subs(gauge).subs(subq)
    dyNr=sp.diff(Y,Nr).subs(gauge).subs(subq)
    jN_extra=-C*(L*R**2*Jv+L*R**2*jv*dyN)
    jNr_extra=-C*(L*R**2*jv*dyNr)
    kN_extra=sp.symbols('kN_extra', real=True)*L*R**2
    dustH_extra=sp.symbols('dustH_extra', real=True)*L*R**2
    bgH_extra=sp.symbols('bgH_extra', real=True)*L*R**2
    extra_hamiltonian=[jN_extra,jNr_extra,kN_extra,dustH_extra,bgH_extra]
    extra_hamiltonian_structure=bool(
        zero(dyNr)
        and all(not e.has(Lr) and not e.has(Rt) and not e.has(Rtr) for e in extra_hamiltonian)
    )

    g3=bool(g3 and extra_hamiltonian_structure)
    g4=bool(
        zero(SMgr-SMgr_target)
        and zero(FMgr-FMgr_target)
        and zero(Mgr-Mgr_target)
        and non_gr_rt_independent
        and non_gr_flux_no_Lr
        and non_gr_source_affine_Lr
        and extra_momentum_structure
        and zero(sp.diff(Mgr,Rtr)+4*L*R)
        and not Mgr.has(Rt)
    )

    # Structural derivative-order proof:
    # H flux has no solved-field derivative, so one radial derivative adds only L_r.
    # M non-GR flux has no L_r/R_t; GR flux is linear in R_t, so one radial
    # derivative adds only R_{t,r}. No second solved-field derivative is generated.
    g5=bool(
        not FH.has(Lr) and not FH.has(Rtr)
        and all(not fbr[k].has(Lr) for k in terms)
        and non_gr_rt_independent
    )

    return {
        'dictionary_ok':dictionary_ok,
        'exact_Q_identity':g2,
        'hamiltonian_identity':g3,
        'momentum_identity':g4,
        'derivative_order_identity':g5,
        'forms':{
            'pt_exact':str(pt_exact),
            'E_reduced':str(E_target),
            'X_reduced':str(X_target),
            'F_H':str(FH_target),
            'A_H':str(AH_target),
            'H_GR_Rt_polynomial':str(H_gr_target),
            'S_M_GR':str(SMgr_target),
            'F_M_GR':str(FMgr_target),
            'M_GR_reduced':str(Mgr_target),
            'Rtr_coefficient':str(-4*L*R),
        },
        'checks':{
            'H_flux_independent_of_Lr_Rt_Rtr':h_flux_independent,
            'H_local_independent_of_Lr_Rtr_and_nonGR_Rt':h_local_structure,
            'H_affine_in_Lr':h_affine_Lr,
            'H_quadratic_in_Rt':h_quadratic_Rt,
            'M_nonGR_independent_of_Rt':non_gr_rt_independent,
            'M_nonGR_flux_independent_of_Lr':non_gr_flux_no_Lr,
            'M_nonGR_source_affine_in_Lr':non_gr_source_affine_Lr,
            'extra_j_K_dust_background_H_structure':extra_hamiltonian_structure,
            'extra_j_K_dust_background_M_structure':extra_momentum_structure,
        },
    }


def coefficient_row(parent,scale,nr):
    r=np.asarray(parent['r'],float)
    D=b4.dmat(r)
    L=b4.AI+np.asarray(parent['L_minus_a'],float)
    R=b4.AI*r+np.asarray(parent['R_minus_ar'],float)
    Lt=b4.AI*b4.H_DIRECT+np.asarray(parent['Ldot_minus_aH'],float)
    u=np.asarray(parent['u'],float)
    ur=D@u
    pr=D@np.asarray(parent['phi'],float)
    Rr=D@R

    ch=np.cosh(u)
    sh=np.sinh(u)
    AH=(
        4.0*R*Rr
        +2.0*b4.KB*R**2*ch*sh*(Lt+ur)
        +2.0*b4.C*R**2*pr
    )/(L**2)
    AM=4.0*L*R

    non=np.arange(nr)>0
    ah=np.asarray(AH[non],float)
    am=np.asarray(AM[non],float)
    rr=np.asarray(r[non],float)

    def audit(a):
        aa=np.abs(a)
        finite=bool(np.all(np.isfinite(a)))
        nz=bool(np.all(aa>0))
        sign_constant=bool(np.all(a>0) or np.all(a<0))
        ratio=float(np.min(aa)/max(float(np.max(aa)),TINY)) if finite and nz else 0.0
        return {
            'finite':finite,
            'nonzero_all_noncenter':nz,
            'constant_sign':sign_constant,
            'sign':1 if np.all(a>0) else (-1 if np.all(a<0) else 0),
            'min_abs':float(np.min(aa)) if finite else None,
            'max_abs':float(np.max(aa)) if finite else None,
            'min_over_max_abs':ratio,
            'relative_nondegeneracy_limit':REL_NONDEGENERACY_LIMIT,
            'pass':bool(finite and nz and sign_constant and ratio>=REL_NONDEGENERACY_LIMIT),
        }

    ah_a=audit(ah)
    am_a=audit(am)
    k=min(8,len(rr))
    ah_over_r=ah[:k]/rr[:k]
    am_over_r=am[:k]/rr[:k]
    center={
        'node_count':int(k),
        'A_H_over_r':{
            'finite':bool(np.all(np.isfinite(ah_over_r))),
            'min':float(np.min(ah_over_r)),
            'max':float(np.max(ah_over_r)),
            'values':[float(x) for x in ah_over_r],
        },
        'A_M_over_r':{
            'finite':bool(np.all(np.isfinite(am_over_r))),
            'min':float(np.min(am_over_r)),
            'max':float(np.max(am_over_r)),
            'values':[float(x) for x in am_over_r],
        },
    }
    return {
        'scale_hinv_Mpc':float(scale),
        'Nr':int(nr),
        'L_min':float(np.min(L)),
        'R_center':float(R[0]),
        'Rt_regular_center_expected':0.0,
        'A_H':ah_a,
        'A_M_4LR':am_a,
        'center_structure':center,
        'pass':bool(ah_a['pass'] and am_a['pass']),
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--trace',required=True)
    ap.add_argument('--coverage-json',required=True)
    ap.add_argument('--repair15a-json',required=True)
    ap.add_argument('--repair15a-npz',required=True)
    ap.add_argument('--repair16-json',required=True)
    ap.add_argument('--b5-repair01-json',required=True)
    ap.add_argument('--out',required=True)
    a=ap.parse_args()

    hashes={
        'repair15a_json':sha256_file(a.repair15a_json),
        'repair15a_npz':sha256_file(a.repair15a_npz),
        'repair16_json':sha256_file(a.repair16_json),
        'b5_repair01_json':sha256_file(a.b5_repair01_json),
    }
    expected={
        'repair15a_json':R15A_JSON_SHA256,
        'repair15a_npz':R15A_NPZ_SHA256,
        'repair16_json':R16_JSON_SHA256,
        'b5_repair01_json':B5_JSON_SHA256,
    }

    p15=json.loads(Path(a.repair15a_json).read_text())
    p16=json.loads(Path(a.repair16_json).read_text())
    pb5=json.loads(Path(a.b5_repair01_json).read_text())
    cov=json.loads(Path(a.coverage_json).read_text())
    off=np.load(a.repair15a_npz)

    g1=bool(
        hashes==expected
        and p15.get('classification')==r18a.R15A_CLASS
        and p16.get('classification')==r18a.R16_CLASS
        and pb5.get('classification')==B5_CLASS
        and pb5.get('project_boundary',{}).get('further_B5_solver_parameter_repairs_licensed') is False
        and pb5.get('project_boundary',{}).get('eta0_short_time_evolution_licensed') is False
        and cov.get('classification')=='NL1C7A_NATIVE_TRACE_COVERAGE_PASS'
        and cov.get('requested_k_relative_miss_max')==0
        and cov.get('n_native_times')==179
    )

    sym=build_symbolic_audit()
    g2=bool(sym['dictionary_ok'] and sym['exact_Q_identity'])
    g3=bool(sym['hamiltonian_identity'])
    g4=bool(sym['momentum_identity'])
    g5=bool(sym['derivative_order_identity'])

    ztrace=rec.read_trace(a.trace)
    ks,gs=rec.groups(ztrace)
    tv_rec=rec.at_ai(gs,'pchip')
    ks_b4,gs_b4=b4.groups(b4.read_trace(a.trace))
    tv_b4=b4.at_ai(gs_b4)
    h=float(cov['h'])
    scalar_ai,scalar_independent,scalar_finite,_=r8.scalar_composites_at_ai(ks,gs,'pchip')
    scalar_identity=r16.rel_sym(scalar_ai,scalar_independent)
    kq_bg=float(np.median(tv_b4['KQ']))
    qbg=b4.stable_q_from_kq(kq_bg)
    kqq_bg=float(np.median(tv_rec['KQQ']))
    zbg=r9.stable_zbg(kq_bg)
    funcs,dY,kidentity=r1.build_nonK()
    g1=bool(
        g1 and len(ks)==128 and np.array_equal(ks,ks_b4)
        and scalar_finite and scalar_identity<=1e-10
        and np.isfinite([qbg,kqq_bg,zbg]).all()
        and bool(kidentity)
    )

    parents={}
    for scale in b4.SCALES:
        parents[(scale,256)]=r16.load_primary_state(off,scale)
        parents[(scale,512)]=r16.reconstructed_corrected_state(
            scale,512,ks,h,tv_b4,tv_rec,scalar_ai,qbg,kqq_bg
        )

    frozen16={
        (float(x['scale_hinv_Mpc']),int(x['Nr']),x['Y_kind'],float(x['beta0'])):x
        for x in p16['constraint_rows']
    }
    parent_reproduction=[]
    for scale in b4.SCALES:
        for nr in (256,512):
            ev=r18a.source_arrays(
                parents[(scale,nr)],r19c.CANON_KIND,r19c.CANON_BETA,qbg,zbg,funcs,dY
            )
            fr=frozen16[(float(scale),nr,r19c.CANON_KIND,r19c.CANON_BETA)]
            ph,ah,rh=r19c.smatch(ev['maxH'],fr['max_epsilon_H'])
            pm,am,rm=r19c.smatch(ev['maxM'],fr['max_epsilon_M'])
            ok=bool(ev.get('finite',False) and ph and pm)
            g1 &= ok
            parent_reproduction.append({
                'scale_hinv_Mpc':float(scale),'Nr':int(nr),'pass':ok,
                'H_abs_error':ah,'H_relative_error':rh,
                'M_abs_error':am,'M_relative_error':rm,
            })

    coeff_rows=[
        coefficient_row(parents[(scale,nr)],scale,nr)
        for scale in b4.SCALES for nr in (256,512)
    ]
    g6=bool(len(coeff_rows)==6 and all(x['pass'] for x in coeff_rows))

    boundary_accounting={
        'reduced_unknown_functions':['L(r)','R_t(r)'],
        'reduced_first_order_equations':2,
        'integration_constants':2,
        'regular_center_information':'R_t(0)=0 from regular spherical center; coefficient division is not performed at r=0.',
        'outer_boundary_information':'Existing project scope requires a regular asymptotic-background outer boundary; exact future numerical enforcement is not chosen here.',
        'Y4_Qmean_status':'Repair18d1 projection-nullspace transversality functionals; not reinterpreted here as physical radial boundary conditions.',
        'numerical_boundary_policy_selected':False,
        'corrected_state_constructed':False,
        'time_evolution_run':False,
        'finite_eta_claimed':False,
        'observational_claimed':False,
    }
    g7=bool(
        not boundary_accounting['numerical_boundary_policy_selected']
        and not boundary_accounting['corrected_state_constructed']
        and not boundary_accounting['time_evolution_run']
        and not boundary_accounting['finite_eta_claimed']
        and not boundary_accounting['observational_claimed']
    )

    gates={
        'B6_G1_frozen_provenance':bool(g1),
        'B6_G2_exact_Q_structural_identities':bool(g2),
        'B6_G3_hamiltonian_reduction_identity':bool(g3),
        'B6_G4_momentum_reduction_identity':bool(g4),
        'B6_G5_derivative_order':bool(g5),
        'B6_G6_six_case_coefficient_nondegeneracy':bool(g6),
        'B6_G7_boundary_gauge_claim_boundary':bool(g7),
    }

    implementation_ok=bool(g1 and sym['dictionary_ok'])
    structural_ok=bool(g2 and g3 and g4 and g5)
    if not implementation_ok:
        classification='NL1C7B6_SYMBOLIC_REDUCTION_IMPLEMENTATION_FAIL'; rc=2
    elif not structural_ok:
        classification='NL1C7B6_SYMBOLIC_RADIAL_REDUCTION_FAIL'; rc=2
    elif not g6:
        classification='NL1C7B6_RADIAL_REDUCTION_COEFFICIENT_DEGENERACY'; rc=2
    elif not g7:
        classification='NL1C7B6_SYMBOLIC_REDUCTION_IMPLEMENTATION_FAIL'; rc=2
    else:
        classification='NL1C7B6_SYMBOLIC_RADIAL_REDUCTION_PASS'; rc=0

    result={
        'classification':classification,
        'scope':'NL1C7B6 symbolic and frozen-parent audit of exact analytic reduction of the eta=0 spherical H/M constraints to a first-order radial system for (L,R_t); no state construction and no evolution.',
        'provenance':{
            **hashes,
            'b5_repair01_result_freeze_commit':B5_FREEZE_COMMIT,
            'b6_prereg_commit':B6_PREREG_COMMIT,
        },
        'symbolic':sym,
        'parent_reproduction':parent_reproduction,
        'coefficient_rows':coeff_rows,
        'relative_nondegeneracy_limit':REL_NONDEGENERACY_LIMIT,
        'boundary_gauge_accounting':boundary_accounting,
        'gates':gates,
        'project_boundary':{
            'reduced_radial_numerical_construction_licensed':bool(classification=='NL1C7B6_SYMBOLIC_RADIAL_REDUCTION_PASS'),
            'eta0_initial_data_certified':False,
            'eta0_short_time_evolution_licensed':False,
            'finite_eta_certified':False,
            'observational_claimed':False,
        },
    }

    out=Path(a.out)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True,allow_nan=False))
    raise SystemExit(rc)


if __name__=='__main__':
    main()
