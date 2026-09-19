#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.optimize._numdiff import approx_derivative

import nl1c7a.a6_a10_spherical_reconstruction as rec
import nl1c7a.evaluate_identity_preserving_repair08 as r8
import nl1c7b.initial_constraint_certification as b4
import nl1c7b.initial_constraint_certification_repair01 as r1
import nl1c7b.initial_constraint_certification_repair09 as r9
import nl1c7b.initial_constraint_certification_repair16 as r16
import nl1c7b.initial_constraint_certification_repair18a as r18a
import nl1c7b.initial_constraint_certification_repair19 as r19
import nl1c7b.initial_constraint_certification_repair19a as r19a
import nl1c7b.initial_constraint_certification_repair19c as r19c

R15A_JSON_SHA256='596c7b13c4683840bcf40f6850356e179e77f873c3a3b42ba0b54730ae80811d'
R15A_NPZ_SHA256='997d0033eeed1f3e60c1907c7938a0ea87a1cf38de6ab860340bd003d18d6e6e'
R16_JSON_SHA256='a225f435ef61eaf33a1b4466eea678b23d1a221a537589bd8e2b0717ed66335b'
R17_JSON_SHA256='09750aeb9fdce7bbbbe148c8478b9af5067a72ab20a1e48171f5a9e3a1d4b82e'
R18_JSON_SHA256='8f8b6ce1316bd5cad3442ebd0cba692e4d4c82060685da083517b990cac36922'
R18A_JSON_SHA256='29a81013b42ebe22989ca1a00b48bb2bb33447677bb77db6aefee298c7159782'
R18B_JSON_SHA256='cbb68157c2408d8d52c180586db0b7d6f007c584d48c5ffc8c8d272b74a6c855'
R18B1_JSON_SHA256='8e0d796e0368372d0b4cf75a075fba12ebde154b651d74929e745118c1ca6dab'
R18C_JSON_SHA256='d49600f8b27536aeb0dca28d1d777d09439a376241c7f8f93b74e754c502e24b'
R18D_JSON_SHA256='adc1410d50118c8080c1f84e5733cb09e5ff7d8f51a4937f1e306a96fe416def'
R18D1_JSON_SHA256='21d5be34660f0054bd8550908f300de64ec1ec9e8f81e0f150c7c1540e3bf04c'
R19_JSON_SHA256='ccf4a362f6a8a791f681d565881ff5728520752b1cbd93d72024b0919e1fe879'
R19A_JSON_SHA256='b9b79d1fe12dff7b59d80260572129b746322412bf96ff214204f9651bd77761'
R19B_JSON_SHA256='d177394b45e19ac2bca739d4ff256694c5df65e9331276e3c1b1466f4fbe5929'
R19B1_JSON_SHA256='33774c721bfd15c1c2f6b776408b3fc4623e3720f9199aa04fc43e8415be1a26'
R19C_JSON_SHA256='5ad02254c512f90d0f82a42d0f5aa00f15c1dae6248bdbe7ad69addb183b600a'
R19C1_JSON_SHA256='b4898fed6c6bbe7d4c91f8144ed35d03e6f318b298a2fc13c0daaef038c0e3cd'

R19C_CLASS='NL1C7B4_REPAIR19C_ORTHONORMAL_DIRECT_GN_NONLINEAR_CLOSURE_FAIL'
R19C1_CLASS='NL1C7B4_REPAIR19C1_FIRST_STEP_DIRECTIONAL_JACOBIAN_FIDELITY_CHARACTERIZED'
CANON_KIND='Simple'
CANON_BETA=1.0
METHODS=('2-point','3-point')
ABS_STEPS=(1e-5,3e-6,1e-6,3e-7,1e-7,3e-8)
TINY=1e-300
REPRO_LIMIT=1e-10
Q_LIMIT=1e-12
GAUGE_LIMIT=1e-12


def sha256_file(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):
            h.update(block)
    return h.hexdigest()


def smatch(a,b,limit=REPRO_LIMIT):
    a=float(a); b=float(b)
    ae=abs(a-b)
    re=ae/max(abs(a),abs(b),TINY)
    return bool(ae<=limit or re<=limit),float(ae),float(re)


def rel_mismatch(a,b):
    a=np.asarray(a,float); b=np.asarray(b,float)
    return float(np.linalg.norm(a-b)/max(np.linalg.norm(b),TINY))


def exact_probe(evaluate_x,fun_x,x):
    x=np.asarray(x,float)
    F=np.asarray(fun_x(x),float)
    st,ev,freeze_ok,freeze_rows=evaluate_x(x)
    gy,gq=r19.gauge_values(x)
    return {
        'frozen_residual_L2':float(np.linalg.norm(F)),
        'frozen_residual_ratio':None,
        'max_epsilon_H':float(ev['maxH']) if ev.get('finite',False) else None,
        'max_epsilon_M':float(ev['maxM']) if ev.get('finite',False) else None,
        'Q_target_max_normalized_error':float(ev['qerr']) if ev.get('finite',False) else None,
        'Y4_residual':float(gy),
        'Qmean_residual':float(gq),
        'field_freeze_pass':bool(freeze_ok),
        'field_freeze':freeze_rows,
        'finite':bool(
            np.all(np.isfinite(F))
            and ev.get('finite',False)
            and np.isfinite([gy,gq]).all()
        ),
    },F


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--trace',required=True)
    ap.add_argument('--coverage-json',required=True)
    ap.add_argument('--repair15a-json',required=True)
    ap.add_argument('--repair15a-npz',required=True)
    ap.add_argument('--repair16-json',required=True)
    ap.add_argument('--repair17-json',required=True)
    ap.add_argument('--repair18-json',required=True)
    ap.add_argument('--repair18a-json',required=True)
    ap.add_argument('--repair18b-json',required=True)
    ap.add_argument('--repair18b1-json',required=True)
    ap.add_argument('--repair18c-json',required=True)
    ap.add_argument('--repair18d-json',required=True)
    ap.add_argument('--repair18d1-json',required=True)
    ap.add_argument('--repair19-json',required=True)
    ap.add_argument('--repair19a-json',required=True)
    ap.add_argument('--repair19b-json',required=True)
    ap.add_argument('--repair19b1-json',required=True)
    ap.add_argument('--repair19c-json',required=True)
    ap.add_argument('--repair19c1-json',required=True)
    ap.add_argument('--out',required=True)
    a=ap.parse_args()

    hashes={
        'repair15a_json':sha256_file(a.repair15a_json),
        'repair15a_npz':sha256_file(a.repair15a_npz),
        'repair16_json':sha256_file(a.repair16_json),
        'repair17_json':sha256_file(a.repair17_json),
        'repair18_json':sha256_file(a.repair18_json),
        'repair18a_json':sha256_file(a.repair18a_json),
        'repair18b_json':sha256_file(a.repair18b_json),
        'repair18b1_json':sha256_file(a.repair18b1_json),
        'repair18c_json':sha256_file(a.repair18c_json),
        'repair18d_json':sha256_file(a.repair18d_json),
        'repair18d1_json':sha256_file(a.repair18d1_json),
        'repair19_json':sha256_file(a.repair19_json),
        'repair19a_json':sha256_file(a.repair19a_json),
        'repair19b_json':sha256_file(a.repair19b_json),
        'repair19b1_json':sha256_file(a.repair19b1_json),
        'repair19c_json':sha256_file(a.repair19c_json),
        'repair19c1_json':sha256_file(a.repair19c1_json),
    }
    expected={
        'repair15a_json':R15A_JSON_SHA256,'repair15a_npz':R15A_NPZ_SHA256,
        'repair16_json':R16_JSON_SHA256,'repair17_json':R17_JSON_SHA256,
        'repair18_json':R18_JSON_SHA256,'repair18a_json':R18A_JSON_SHA256,
        'repair18b_json':R18B_JSON_SHA256,'repair18b1_json':R18B1_JSON_SHA256,
        'repair18c_json':R18C_JSON_SHA256,'repair18d_json':R18D_JSON_SHA256,
        'repair18d1_json':R18D1_JSON_SHA256,'repair19_json':R19_JSON_SHA256,
        'repair19a_json':R19A_JSON_SHA256,'repair19b_json':R19B_JSON_SHA256,
        'repair19b1_json':R19B1_JSON_SHA256,'repair19c_json':R19C_JSON_SHA256,
        'repair19c1_json':R19C1_JSON_SHA256,
    }

    p19c=json.loads(Path(a.repair19c_json).read_text())
    p19c1=json.loads(Path(a.repair19c1_json).read_text())
    cov=json.loads(Path(a.coverage_json).read_text())
    off=np.load(a.repair15a_npz)

    g1=bool(
        hashes==expected
        and p19c.get('classification')==R19C_CLASS
        and p19c1.get('classification')==R19C1_CLASS
        and all(p19c1.get('gates',{}).values())
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
        and np.isfinite([qbg,kqq_bg,zbg]).all() and bool(kidentity)
    )

    bases={}
    for nr in (256,512):
        audit,Bc,Bo=r19a.basis_audit(nr)
        bases[nr]=Bo

    states={}
    for scale in b4.SCALES:
        states[(scale,256)]=r16.load_primary_state(off,scale)
        states[(scale,512)]=r16.reconstructed_corrected_state(
            scale,512,ks,h,tv_b4,tv_rec,scalar_ai,qbg,kqq_bg
        )

    frozen19c={(float(r['scale_hinv_Mpc']),int(r['Nr'])):r
               for r in p19c['solve_rows'] if float(r['lambda'])==1.0}

    case_rows=[]
    g2=True; g3=True; g4=True; g5=True; g6=True

    for scale in b4.SCALES:
        for nr in (256,512):
            parent=states[(scale,nr)]
            vp,base,fun_x,evaluate_x,char_rt=r19c.build_virtual_problem(
                parent,scale,1.0,h,qbg,zbg,funcs,dY
            )
            n=len(vp['r']); m=n-1
            B=bases[nr]
            x0=np.zeros(2*m,float)
            F0=np.asarray(fun_x(x0),float)
            F0norm=float(np.linalg.norm(F0))
            pattern=r18a.jac_pattern(n)

            Jx0=approx_derivative(fun_x,x0,method='2-point',sparsity=pattern).tocsr()
            J0=(Jx0@B).toarray()
            step0,dz0,dx0=r19c.direct_gelsy_step(J0,F0,B)

            fr=frozen19c[(float(scale),nr)]['history'][0]['direct_step']
            checks=[]
            for key,obs,exp in (
                ('rank',step0['rank'],fr['rank']),
                ('predicted_relative_residual',step0['predicted_relative_residual'],fr['predicted_relative_residual']),
                ('max_abs_step_yL',step0['max_abs_step_yL'],fr['max_abs_step_yL']),
                ('max_abs_step_qRt',step0['max_abs_step_qRt'],fr['max_abs_step_qRt']),
            ):
                if key=='rank':
                    ok=int(obs)==int(exp); ae=float(abs(int(obs)-int(exp))); re=ae/max(abs(float(obs)),abs(float(exp)),1.0)
                else:
                    ok,ae,re=smatch(obs,exp,REPRO_LIMIT)
                checks.append({'key':key,'pass':bool(ok),'abs_error':ae,'relative_error':re})
            dir_repro=bool(all(x['pass'] for x in checks))
            g2 &= dir_repro

            refs=[]
            Fref={}
            for alpha in (1.0,-1.0,0.5,-0.5):
                x=alpha*dx0
                probe,F=exact_probe(evaluate_x,fun_x,x)
                probe['alpha']=alpha
                probe['frozen_residual_ratio']=float(probe['frozen_residual_L2']/max(F0norm,TINY))
                refs.append(probe)
                Fref[alpha]=F
                g3 &= probe['finite']
                g4 &= bool(
                    probe['finite']
                    and probe['Q_target_max_normalized_error']<=Q_LIMIT
                    and abs(probe['Y4_residual'])<=GAUGE_LIMIT
                    and abs(probe['Qmean_residual'])<=GAUGE_LIMIT
                    and probe['field_freeze_pass']
                )

            D1=(Fref[1.0]-Fref[-1.0])/2.0
            Dhalf=(Fref[0.5]-Fref[-0.5])/1.0
            Dref=(4.0*Dhalf-D1)/3.0
            ref_stability=rel_mismatch(Dhalf,D1)

            default_action=np.asarray(J0@dz0,float)
            default_total=rel_mismatch(default_action,Dref)
            default_H=rel_mismatch(default_action[:m],Dref[:m])
            default_M=rel_mismatch(default_action[m:],Dref[m:])

            candidates=[]
            for method in METHODS:
                for abs_step in ABS_STEPS:
                    Jx=approx_derivative(
                        fun_x,x0,method=method,sparsity=pattern,abs_step=abs_step
                    ).tocsr()
                    J=(Jx@B).toarray()
                    action=np.asarray(J@dz0,float)
                    total=rel_mismatch(action,Dref)
                    hm=rel_mismatch(action[:m],Dref[:m])
                    mm=rel_mismatch(action[m:],Dref[m:])

                    step,dz,dx=r19c.direct_gelsy_step(J,F0,B)
                    probe,Ftrial=exact_probe(evaluate_x,fun_x,dx)
                    probe['frozen_residual_ratio']=float(probe['frozen_residual_L2']/max(F0norm,TINY))
                    probe['max_abs_yL']=float(np.max(np.abs(dx[:m])))
                    probe['max_abs_qRt']=float(np.max(np.abs(dx[m:])))
                    probe['predicted_relative_residual']=float(step['predicted_relative_residual'])
                    probe['rank']=int(step['rank'])

                    finite=bool(
                        np.all(np.isfinite(J))
                        and np.isfinite([total,hm,mm]).all()
                        and step['finite']
                    )
                    g5 &= finite
                    g6 &= bool(finite and probe['finite'])
                    candidates.append({
                        'method':method,'abs_step':float(abs_step),
                        'directional_action_mismatch':total,
                        'H_action_mismatch':hm,
                        'M_action_mismatch':mm,
                        'finite':finite,
                        'one_step_probe':probe,
                    })

            case_rows.append({
                'scale_hinv_Mpc':float(scale),'Nr':int(nr),
                'F0_L2':F0norm,
                'frozen_direction_reproduction':{'checks':checks,'pass':dir_repro},
                'frozen_direction':step0,
                'reference_probes':refs,
                'reference_stability_Dhalf_vs_D1':ref_stability,
                'Dref_L2':float(np.linalg.norm(Dref)),
                'default_control':{
                    'directional_action_mismatch':default_total,
                    'H_action_mismatch':default_H,
                    'M_action_mismatch':default_M,
                },
                'candidates':candidates,
            })

    g2=bool(g2 and len(case_rows)==6)
    g3=bool(g3 and sum(len(r['reference_probes']) for r in case_rows)==24)
    g4=bool(g4 and sum(len(r['reference_probes']) for r in case_rows)==24)
    g5=bool(g5 and sum(len(r['candidates']) for r in case_rows)==72)
    g6=bool(g6 and sum(len(r['candidates']) for r in case_rows)==72)

    aggregates=[]
    for method in METHODS:
        for step_i,abs_step in enumerate(ABS_STEPS):
            vals=[]
            Hvals=[]
            Mvals=[]
            exact_vals=[]
            for row in case_rows:
                c=next(x for x in row['candidates']
                       if x['method']==method and x['abs_step']==float(abs_step))
                vals.append(c['directional_action_mismatch'])
                Hvals.append(c['H_action_mismatch'])
                Mvals.append(c['M_action_mismatch'])
                exact_vals.append(c['one_step_probe']['frozen_residual_ratio'])
            aggregates.append({
                'method':method,'abs_step':float(abs_step),
                'max_directional_action_mismatch':float(np.max(vals)),
                'median_directional_action_mismatch':float(np.median(vals)),
                'max_H_action_mismatch':float(np.max(Hvals)),
                'max_M_action_mismatch':float(np.max(Mvals)),
                'median_exact_one_step_residual_ratio_descriptive':float(np.median(exact_vals)),
                'max_exact_one_step_residual_ratio_descriptive':float(np.max(exact_vals)),
                'method_preference':0 if method=='3-point' else 1,
                'step_preference':int(step_i),
            })

    ordered=sorted(
        aggregates,
        key=lambda x:(
            x['max_directional_action_mismatch'],
            x['median_directional_action_mismatch'],
            x['max_M_action_mismatch'],
            x['method_preference'],
            x['step_preference'],
        )
    )
    selected=ordered[0] if ordered else None
    g7=bool(
        selected is not None
        and len(aggregates)==12
        and sum(
            1 for x in aggregates
            if x['method']==selected['method'] and x['abs_step']==selected['abs_step']
        )==1
    )

    claim_boundary={
        'nonlinear_iteration_run':False,'line_search_run':False,
        'corrected_state_certified':False,'state_NPZ_written':False,
        'physical_projection_pair_changed':False,'physical_field_added':False,
        'Y4_or_Qmean_changed':False,'source_changed':False,
        'coefficient_changed':False,'sign_changed':False,
        'finite_eta_executed':False,'branch_changed':False,
        'historical_threshold_changed':False,'radial_points_removed':False,
        'parent_artifact_changed':False,'time_evolution_run':False,
        'observational_claimed':False,'Repair19c_relabelled':False,
        'Repair19c1_relabelled':False,
    }
    g8=bool(not any(claim_boundary.values()))

    gates={
        'R19C2_G1_exact_frozen_provenance':g1,
        'R19C2_G2_exact_frozen_direction_reproduction':g2,
        'R19C2_G3_finite_symmetric_directional_reference':g3,
        'R19C2_G4_exact_gauge_Q_field_freeze_reference':g4,
        'R19C2_G5_complete_finite_candidate_Jacobian_audit':g5,
        'R19C2_G6_complete_one_step_descriptive_probes':g6,
        'R19C2_G7_deterministic_selection_completeness':g7,
        'R19C2_G8_claim_boundary':g8,
    }
    if all(gates.values()):
        classification='NL1C7B4_REPAIR19C2_FINITE_DIFFERENCE_STEP_SCALE_CHARACTERIZED'
        rc=0
    else:
        classification='NL1C7B4_REPAIR19C2_IMPLEMENTATION_FAIL'
        rc=2

    default_scores=[r['default_control']['directional_action_mismatch'] for r in case_rows]
    result={
        'classification':classification,
        'scope':'Repair19c2 finite-difference method/absolute-step audit against a Richardson symmetric directional reference along the frozen Repair19c first direction.',
        'provenance':{
            **hashes,
            'repair19c1_result_freeze_commit':'cbf05b2a2845cda70fb962b20c5062d516b24a5b',
            'repair19c2_prereg_commit':'a094d9b660b346c3fcf03f6b26f2ce39ce263894',
        },
        'candidate_methods':list(METHODS),
        'candidate_abs_steps':list(ABS_STEPS),
        'case_rows':case_rows,
        'aggregates':aggregates,
        'selected_candidate':selected,
        'gates':gates,
        'claim_boundary':claim_boundary,
        'summary':{
            'default_control_max_directional_mismatch':float(np.max(default_scores)),
            'default_control_median_directional_mismatch':float(np.median(default_scores)),
            'selected_max_directional_mismatch':None if selected is None else selected['max_directional_action_mismatch'],
            'selected_median_directional_mismatch':None if selected is None else selected['median_directional_action_mismatch'],
            'selected_method':None if selected is None else selected['method'],
            'selected_abs_step':None if selected is None else selected['abs_step'],
            'max_reference_instability':float(max(r['reference_stability_Dhalf_vs_D1'] for r in case_rows)),
        },
        'interpretation_boundary':{
            'nonlinear_closure_certified':False,
            'selected_Jacobian_licensed_for_future_repair_only_after_freeze':bool(all(gates.values())),
            'physical_ansatz_changed':False,
        },
    }

    out=Path(a.out)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True,allow_nan=False))
    raise SystemExit(rc)


if __name__=='__main__':
    main()
