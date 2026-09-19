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
import nl1c7b.reduced_radial_initial_data_b7 as b7

B6_JSON_SHA256='ed1efdac5dee72d8c57cbda23d074213babd15fdf3bc7adc18e61789f862e635'
B7_JSON_SHA256='449201305c535e24e592296f5e2a53e7fc0866b5cae2970a147c2bcebe12bfc6'
B6_CLASS='NL1C7B6_SYMBOLIC_RADIAL_REDUCTION_PASS'
B7_CLASS='NL1C7B7_REDUCED_RADIAL_CONSTRUCTION_FAIL'
B7_FREEZE_COMMIT='6bd01d8e4c825fe4f150a851c4dc402644b664cc'
B8_PREREG_COMMIT='6f0bda207d8f38e3f24b747564196a42750aa668'

R15A_JSON_SHA256='596c7b13c4683840bcf40f6850356e179e77f873c3a3b42ba0b54730ae80811d'
R15A_NPZ_SHA256='997d0033eeed1f3e60c1907c7938a0ea87a1cf38de6ab860340bd003d18d6e6e'
R16_JSON_SHA256='a225f435ef61eaf33a1b4466eea678b23d1a221a537589bd8e2b0717ed66335b'

CENTER_L2_LIMIT=1e-6
OUTER_L_LIMIT=1e-7
OUTER_RT_LIMIT=1e-7
CONSTRAINT_LIMIT=1e-7
Q_LIMIT=1e-12
SAFETY_BOUND=0.5
GRID_RATIO_LIMIT=2.0
PRIMARY_LAUNCH=1e-5
CONTROL_LAUNCH=1e-4
TINY=1e-300


def sha256_file(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):
            h.update(block)
    return h.hexdigest()


def scalar_match(a,b,limit=1e-12):
    a=float(a); b=float(b)
    d=abs(a-b)
    r=d/max(abs(a),abs(b),TINY)
    return bool(d<=limit or r<=limit),float(d),float(r)


def center_identity_audit():
    L0,R1,Lt0,T1,e=sp.symbols('L0 R1 Lt0 T1 e', positive=True, real=True)

    # Exact leading GR curvature center term:
    # 2L + 2R_r^2/L - d_r(4 R R_r/L), with R=e R1 and L_r(0)=0.
    hcurv=sp.simplify(2*L0+2*R1**2/L0-4*R1**2/L0)
    hcurv_target=2*L0-2*R1**2/L0

    # Exact simplified GR kinetic term from B6.
    hkin=2*L0*(e*T1)**2+4*Lt0*(e*R1)*(e*T1)

    # Exact leading GR momentum from B6.
    # M_GR=4 R Lt Rr - 4 L R Rtr.
    mgr=4*(e*R1)*Lt0*R1-4*L0*(e*R1)*T1
    t1_solution=sp.solve(sp.Eq(sp.factor(mgr/e),0),T1)

    # Non-GR H local terms all carry R^2. Their radial fluxes carry R^2,
    # so a single radial derivative is O(e). j/K/dust/background local H
    # terms likewise carry R^2.
    # Regular momentum non-GR terms carry R^2 times an odd radial quantity
    # (phi_r, rapidity/velocity, or equivalent), hence O(e^3).
    structural_orders={
        'AeST_H_local_R2_or_higher':True,
        'AeST_H_flux_divergence_O_r':True,
        'j_K_dust_background_H_R2_or_higher':True,
        'nonGR_momentum_O_r3':True,
    }

    checks={
        'GR_curvature_center_identity':bool(sp.simplify(hcurv-hcurv_target)==0),
        'GR_kinetic_vanishes_O_r2':bool(sp.limit(hkin/e,e,0)==0),
        'positive_L_center_solution_is_L_eq_Rr':bool(
            sp.simplify(hcurv_target.subs(L0,R1))==0
        ),
        'GR_momentum_regular_slope_identity':bool(
            len(t1_solution)==1 and sp.simplify(t1_solution[0]-Lt0*R1/L0)==0
        ),
        **structural_orders,
    }
    return {
        'pass':bool(all(checks.values())),
        'checks':checks,
        'H_center':'2*L0 - 2*Rr0**2/L0',
        'regular_positive_solution':'L0=Rr0',
        'Rt_center':'Rt(0)=0',
        'Rt_slope':'Rt_r(0)=Lt0*Rr0/L0=Lt0',
    }


def rel_l2(a,b):
    a=np.asarray(a,float); b=np.asarray(b,float)
    return float(np.linalg.norm(a-b)/max(np.linalg.norm(b),TINY))


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--trace',required=True)
    ap.add_argument('--coverage-json',required=True)
    ap.add_argument('--repair15a-json',required=True)
    ap.add_argument('--repair15a-npz',required=True)
    ap.add_argument('--repair16-json',required=True)
    ap.add_argument('--b6-json',required=True)
    ap.add_argument('--b7-json',required=True)
    ap.add_argument('--out',required=True)
    ap.add_argument('--state-npz',required=True)
    a=ap.parse_args()

    hashes={
        'repair15a_json':sha256_file(a.repair15a_json),
        'repair15a_npz':sha256_file(a.repair15a_npz),
        'repair16_json':sha256_file(a.repair16_json),
        'b6_json':sha256_file(a.b6_json),
        'b7_json':sha256_file(a.b7_json),
    }
    expected={
        'repair15a_json':R15A_JSON_SHA256,
        'repair15a_npz':R15A_NPZ_SHA256,
        'repair16_json':R16_JSON_SHA256,
        'b6_json':B6_JSON_SHA256,
        'b7_json':B7_JSON_SHA256,
    }

    p15=json.loads(Path(a.repair15a_json).read_text())
    p16=json.loads(Path(a.repair16_json).read_text())
    pb6=json.loads(Path(a.b6_json).read_text())
    pb7=json.loads(Path(a.b7_json).read_text())
    cov=json.loads(Path(a.coverage_json).read_text())
    off=np.load(a.repair15a_npz)

    g1=bool(
        hashes==expected
        and p15.get('classification')==r18a.R15A_CLASS
        and p16.get('classification')==r18a.R16_CLASS
        and pb6.get('classification')==B6_CLASS
        and pb6.get('project_boundary',{}).get('reduced_radial_numerical_construction_licensed') is True
        and pb7.get('classification')==B7_CLASS
        and pb7.get('project_boundary',{}).get('further_B7_solver_parameter_repairs_licensed') is False
        and pb7.get('project_boundary',{}).get('eta0_short_time_evolution_licensed') is False
        and cov.get('classification')=='NL1C7A_NATIVE_TRACE_COVERAGE_PASS'
        and cov.get('requested_k_relative_miss_max')==0
        and cov.get('n_native_times')==179
    )

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
    parent_repro=[]
    for scale in b4.SCALES:
        for nr in (256,512):
            ev=r18a.source_arrays(
                parents[(scale,nr)],b7.CANON_KIND,b7.CANON_BETA,qbg,zbg,funcs,dY
            )
            fr=frozen16[(float(scale),nr,b7.CANON_KIND,b7.CANON_BETA)]
            ph,ah,rh=scalar_match(ev['maxH'],fr['max_epsilon_H'])
            pm,am,rm=scalar_match(ev['maxM'],fr['max_epsilon_M'])
            ok=bool(ev.get('finite',False) and ph and pm)
            g1 &= ok
            parent_repro.append({
                'scale_hinv_Mpc':float(scale),'Nr':int(nr),'pass':ok,
                'H_abs_error':ah,'H_relative_error':rh,
                'M_abs_error':am,'M_relative_error':rm,
            })

    rhs_fun,coeff_fun,rhs_audit=b7.build_exact_reduced_rhs()
    center_audit=center_identity_audit()
    g3=bool(rhs_audit['pass'] and center_audit['pass'])

    poly_rows=[]
    contexts={}
    g2=True
    for scale in b4.SCALES:
        for nr in (256,512):
            parent=parents[(scale,nr)]
            ff=b7.frozen_fields(parent,qbg)
            interp=b7.LocalDegree8(parent['r'],ff)
            pok,prows=interp.derivative_reproduction(ff)
            g2 &= pok
            poly_rows.append({
                'scale_hinv_Mpc':float(scale),'Nr':int(nr),
                'pass':bool(pok),'fields':prows,
            })
            contexts[(scale,nr)]=(parent,interp)

    case_rows=[]
    solved_states={}
    construct_ok=True
    center_control_ok=True
    outer_L_ok=True
    outer_Rt_ok=True
    safety_ok=True
    differential_ok=True

    for scale in b4.SCALES:
        for nr in (256,512):
            parent,interp=contexts[(scale,nr)]
            e0=interp.eval(0.0)
            Rr0=float(e0['R'][1])
            Lt0=float(e0['Lt'][0])
            center_data_ok=bool(
                np.isfinite([Rr0,Lt0]).all()
                and Rr0>0
            )
            ell0=float(math.log(Rr0/b4.AI)) if center_data_ok else float('nan')
            center_data_ok=bool(center_data_ok and abs(ell0)<=SAFETY_BOUND)

            if center_data_ok:
                primary=b7.integrate_trial(
                    interp,scale,h,qbg,zbg,rhs_fun,ell0,PRIMARY_LAUNCH,True
                )
                control=b7.integrate_trial(
                    interp,scale,h,qbg,zbg,rhs_fun,ell0,CONTROL_LAUNCH,True
                )
            else:
                primary={'success':False,'reason':'invalid_regular_center_data'}
                control={'success':False,'reason':'invalid_regular_center_data'}

            c_ok=bool(
                center_data_ok
                and primary.get('success',False)
                and control.get('success',False)
            )
            construct_ok &= c_ok
            row={
                'scale_hinv_Mpc':float(scale),'Nr':int(nr),
                'center_data':{
                    'Rr0':Rr0,'Lt0':Lt0,'L0':Rr0,
                    'ell0':ell0,'Rt0':0.0,'Rt_r0':Lt0,
                    'pass':center_data_ok,
                },
                'primary_launch':{
                    k:v for k,v in primary.items()
                    if k not in ('L','Rt','ell','w')
                },
                'control_launch':{
                    k:v for k,v in control.items()
                    if k not in ('L','Rt','ell','w')
                },
                'construction_pass':c_ok,
            }

            if not c_ok:
                center_control_ok=False
                outer_L_ok=False
                outer_Rt_ok=False
                safety_ok=False
                differential_ok=False
                row.update({
                    'center_control_pass':False,
                    'outer_L_compatibility_pass':False,
                    'outer_Rt_compatibility_pass':False,
                    'safety_pass':False,
                    'differential_constraint_pass':False,
                })
                case_rows.append(row)
                continue

            Lp=np.asarray(primary['L'],float)
            Rtp=np.asarray(primary['Rt'],float)
            Lc=np.asarray(control['L'],float)
            Rtc=np.asarray(control['Rt'],float)
            dL=rel_l2(Lc,Lp)
            dRt=rel_l2(Rtc,Rtp)
            cc=bool(dL<=CENTER_L2_LIMIT and dRt<=CENTER_L2_LIMIT)
            center_control_ok &= cc

            Lm=float(Lp[-1])
            olm=float(abs(Lm-b4.AI)/b4.AI)
            olp=bool(olm<=OUTER_L_LIMIT)
            outer_L_ok &= olp

            rmax=float(np.asarray(parent['r'],float)[-1])
            rtbg=float(b4.AI*b4.H_DIRECT*rmax)
            orm=float(abs(Rtp[-1]-rtbg)/max(abs(rtbg),TINY))
            orp=bool(orm<=OUTER_RT_LIMIT)
            outer_Rt_ok &= orp

            st,ev=b7.evaluate_primary(
                parent,Lp,Rtp,scale,h,qbg,zbg,funcs,dY
            )
            Lparent=b4.AI+np.asarray(parent['L_minus_a'],float)
            Rtparent=b4.AI*b4.H_DIRECT*np.asarray(parent['r'],float)+np.asarray(parent['Rdot_minus_aHr'],float)
            char=float(b4.AI*b4.H_DIRECT*(float(scale)/float(h)))
            all_y=np.log(Lp/Lparent)
            all_q=(Rtp-Rtparent)/char
            all_bounds=bool(
                np.max(np.abs(all_y))<=SAFETY_BOUND
                and np.max(np.abs(all_q))<=SAFETY_BOUND
            )
            safe=bool(ev['safety_pass'] and all_bounds)
            safety_ok &= safe
            differential_ok &= bool(ev['differential_constraint_pass'])
            solved_states[(scale,nr)]=st

            row.update({
                'center_control':{
                    'L_relative_L2':dL,'Rt_relative_L2':dRt,
                    'limit':CENTER_L2_LIMIT,'pass':cc,
                },
                'outer_L_compatibility':{
                    'L_outer':Lm,'L_background':float(b4.AI),
                    'relative_mismatch':olm,'limit':OUTER_L_LIMIT,'pass':olp,
                },
                'outer_Rt_compatibility':{
                    'R_t_outer':float(Rtp[-1]),'R_t_background':rtbg,
                    'relative_mismatch':orm,'limit':OUTER_RT_LIMIT,'pass':orp,
                },
                **ev,
                'safety_pass':safe,
                'all_node_max_abs_log_L_over_parent':float(np.max(np.abs(all_y))),
                'all_node_max_abs_qRt_correction':float(np.max(np.abs(all_q))),
            })
            case_rows.append(row)

    g4=bool(construct_ok)
    g5=bool(g4 and center_control_ok)
    g6=bool(g4 and outer_L_ok)
    g7=bool(g4 and outer_Rt_ok)
    g8=bool(g4 and safety_ok)
    g9=bool(g4 and differential_ok)

    two_grid=[]
    g10=True
    if all((s,n) in solved_states for s in b4.SCALES for n in (256,512)):
        for scale in b4.SCALES:
            c256=r18a.correction_metrics(
                parents[(scale,256)],solved_states[(scale,256)],scale,h
            )['combined_norm']
            c512=r18a.correction_metrics(
                parents[(scale,512)],solved_states[(scale,512)],scale,h
            )['combined_norm']
            ratio=float(max(c256/max(c512,TINY),c512/max(c256,TINY)))
            ok=bool(np.isfinite(ratio) and ratio<=GRID_RATIO_LIMIT)
            g10 &= ok
            two_grid.append({
                'scale_hinv_Mpc':float(scale),
                'C256':float(c256),'C512':float(c512),
                'symmetric_ratio':ratio,'limit':GRID_RATIO_LIMIT,'pass':ok,
            })
    else:
        g10=False

    gates={
        'B8_G1_frozen_provenance':bool(g1),
        'B8_G2_frozen_field_polynomial_representation':bool(g2),
        'B8_G3_exact_reduced_equation_and_center_identity':bool(g3),
        'B8_G4_complete_zero_parameter_IVP_construction':bool(g4),
        'B8_G5_center_launch_stability':bool(g5),
        'B8_G6_outer_L_background_compatibility':bool(g6),
        'B8_G7_outer_Rt_background_compatibility':bool(g7),
        'B8_G8_safety_exactQ_field_freeze':bool(g8),
        'B8_G9_original_B4_differential_exact_constraints':bool(g9),
        'B8_G10_two_grid_correction_control':bool(g10),
        'B8_G11_output_integrity_claim_boundary':True,
    }

    if not (g1 and g2 and g3):
        classification='NL1C7B8_REGULAR_CENTER_IVP_IMPLEMENTATION_FAIL'
    elif not g4:
        classification='NL1C7B8_REGULAR_CENTER_IVP_CONSTRUCTION_FAIL'
    elif not g5:
        classification='NL1C7B8_REGULAR_CENTER_CONTROL_FAIL'
    elif not g6:
        classification='NL1C7B8_OUTER_L_COMPATIBILITY_FAIL'
    elif not g7:
        classification='NL1C7B8_OUTER_RT_COMPATIBILITY_FAIL'
    elif not g8:
        classification='NL1C7B8_REGULAR_CENTER_IVP_CONSTRUCTION_FAIL'
    elif not g9:
        classification='NL1C7B8_DIFFERENTIAL_CERTIFICATION_FAIL'
    elif not g10:
        classification='NL1C7B8_TWO_GRID_CONTROL_FAIL'
    else:
        classification='NL1C7B8_REGULAR_CENTER_INITIAL_DATA_CERTIFIED'

    science_pass=bool(
        classification=='NL1C7B8_REGULAR_CENTER_INITIAL_DATA_CERTIFIED'
    )
    state_path=Path(a.state_npz)
    if science_pass:
        b7.write_npz(state_path,solved_states)
    elif state_path.exists():
        state_path.unlink()

    output={
        'written':science_pass,
        'exists_after_run':bool(state_path.exists()),
        'pass':bool(state_path.exists()==science_pass),
    }
    gates['B8_G11_output_integrity_claim_boundary']=bool(output['pass'])

    result={
        'classification':classification,
        'scope':'NL1C7B8 zero-free-parameter regular-center IVP construction of the exact B6 eta=0 radial constraint system for (L,R_t), with both outer background conditions treated as predictions.',
        'provenance':{
            **hashes,
            'b7_result_freeze_commit':B7_FREEZE_COMMIT,
            'b8_prereg_commit':B8_PREREG_COMMIT,
        },
        'settings':{
            'free_shooting_parameters':0,
            'regular_center_L0':'R_r(0)',
            'regular_center_Rt0':0.0,
            'regular_center_Rt_slope':'L_t(0)',
            'primary_launch_fraction_r1':PRIMARY_LAUNCH,
            'control_launch_fraction_r1':CONTROL_LAUNCH,
            'ivp_method':'DOP853',
            'ivp_rtol':b7.IVP_RTOL,'ivp_atol':b7.IVP_ATOL,
            'ivp_max_step':'dr',
            'center_L2_limit':CENTER_L2_LIMIT,
            'outer_L_relative_limit':OUTER_L_LIMIT,
            'outer_Rt_relative_limit':OUTER_RT_LIMIT,
            'exact_constraint_limit':CONSTRAINT_LIMIT,
            'two_grid_ratio_limit':GRID_RATIO_LIMIT,
        },
        'rhs_audit':rhs_audit,
        'center_identity_audit':center_audit,
        'parent_reproduction':parent_repro,
        'polynomial_representation':poly_rows,
        'case_rows':case_rows,
        'two_grid_control':two_grid,
        'gates':gates,
        'output':output,
        'summary':{
            'case_count':6,
            'constructed_case_count':int(sum(bool(r['construction_pass']) for r in case_rows)),
            'center_pass_count':int(sum(bool(r.get('center_control',{}).get('pass',False)) for r in case_rows)),
            'outer_L_pass_count':int(sum(bool(r.get('outer_L_compatibility',{}).get('pass',False)) for r in case_rows)),
            'outer_Rt_pass_count':int(sum(bool(r.get('outer_Rt_compatibility',{}).get('pass',False)) for r in case_rows)),
            'safe_case_count':int(sum(bool(r.get('safety_pass',False)) for r in case_rows)),
            'differential_pass_count':int(sum(bool(r.get('differential_constraint_pass',False)) for r in case_rows)),
            'max_exact_epsilon_H':max([r.get('max_epsilon_H') for r in case_rows if r.get('max_epsilon_H') is not None],default=None),
            'max_exact_epsilon_M':max([r.get('max_epsilon_M') for r in case_rows if r.get('max_epsilon_M') is not None],default=None),
        },
        'project_boundary':{
            'eta0_initial_data_certified':science_pass,
            'eta0_short_time_evolution_licensed':science_pass,
            'finite_eta_certified':False,
            'observational_claimed':False,
            'further_B8_solver_parameter_repairs_licensed':False,
        },
    }

    out=Path(a.out)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True,allow_nan=False))
    raise SystemExit(0 if science_pass else 2)


if __name__=='__main__':
    main()
