#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
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

R19C_CLASS='NL1C7B4_REPAIR19C_ORTHONORMAL_DIRECT_GN_NONLINEAR_CLOSURE_FAIL'
CANON_KIND='Simple'
CANON_BETA=1.0
ALPHAS=tuple(2.0**(-k) for k in range(13))
TINY=1e-300
REPRO_LIMIT=1e-12
FIRST_REPRO_LIMIT=1e-10
GAUGE_LIMIT=1e-12
Q_LIMIT=1e-12


def sha256_file(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):
            h.update(block)
    return h.hexdigest()


def smatch(a,b,limit):
    a=float(a); b=float(b)
    ae=abs(a-b)
    re=ae/max(abs(a),abs(b),TINY)
    return bool(ae<=limit or re<=limit),float(ae),float(re)


def block_norms(v,m):
    v=np.asarray(v,float)
    return float(np.linalg.norm(v[:m])),float(np.linalg.norm(v[m:]))


def safe_slope(a,b):
    if a>0 and b>0 and np.isfinite(a) and np.isfinite(b):
        return float(math.log(a/b,2.0))
    return None


def median_finite(vals):
    xs=[float(x) for x in vals if x is not None and np.isfinite(x)]
    return None if not xs else float(np.median(xs))


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
    }

    p19c=json.loads(Path(a.repair19c_json).read_text())
    cov=json.loads(Path(a.coverage_json).read_text())
    off=np.load(a.repair15a_npz)

    g1=bool(
        hashes==expected
        and p19c.get('classification')==R19C_CLASS
        and p19c.get('gates',{}).get('R19C_G1_exact_frozen_provenance') is True
        and p19c.get('gates',{}).get('R19C_G2_orthonormal_constrained_basis') is True
        and p19c.get('gates',{}).get('R19C_G3_exact_parent_reproduction') is True
        and p19c.get('gates',{}).get('R19C_G4_certified_first_step_reproduction') is True
        and p19c.get('gates',{}).get('R19C_G5_exact_canonical_nonlinear_closure') is False
        and p19c.get('gates',{}).get('R19C_G9_field_freeze_invariant') is True
        and p19c.get('gates',{}).get('R19C_G10_output_integrity') is True
        and p19c.get('gates',{}).get('R19C_G11_claim_boundary') is True
        and p19c.get('output',{}).get('written') is False
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

    basis_rows=[]
    bases={}
    g2=True
    for nr in (256,512):
        obs,Bc,Bo=r19a.basis_audit(nr)
        fr=next(x for x in p19c['basis_rows'] if int(x['Nr'])==nr)['audit']
        checks=[]
        for key in ('GB_Frobenius','condition_number','sigma_max','sigma_min','orthonormality_Frobenius'):
            ok,ae,re=smatch(obs['orth'][key],fr['orth'][key],REPRO_LIMIT)
            checks.append({'key':key,'pass':ok,'abs_error':ae,'relative_error':re})
        checks.append({'key':'shape','pass':obs['orth']['shape']==fr['orth']['shape']})
        ok=bool(all(x['pass'] for x in checks))
        g2 &= ok
        basis_rows.append({'Nr':nr,'checks':checks,'pass':ok})
        bases[nr]=Bo

    states={}
    for scale in b4.SCALES:
        states[(scale,256)]=r16.load_primary_state(off,scale)
        states[(scale,512)]=r16.reconstructed_corrected_state(
            scale,512,ks,h,tv_b4,tv_rec,scalar_ai,qbg,kqq_bg
        )

    frozen_rows={(float(r['scale_hinv_Mpc']),int(r['Nr'])):r
                 for r in p19c['solve_rows'] if float(r['lambda'])==1.0}

    rows=[]
    g3=True; g4=True; g5=True; g6=True; g7=True

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
            Jx=approx_derivative(
                fun_x,x0,method='2-point',sparsity=r18a.jac_pattern(n)
            )
            Jx=Jx.tocsr()
            J=(Jx@B).toarray()
            step,dz,dx=r19c.direct_gelsy_step(J,F0,B)
            Jdz=np.asarray(J@dz,float)
            frozen=frozen_rows[(float(scale),nr)]
            fstep=frozen['history'][0]['direct_step']
            frozen_F0=float(
                fstep['predicted_residual_L2']
                / max(fstep['predicted_relative_residual'],TINY)
            )
            p0,ae0,re0=smatch(np.linalg.norm(F0),frozen_F0,REPRO_LIMIT)
            g3 &= p0

            checks=[]
            for key,obs,fr in (
                ('rank',step['rank'],fstep['rank']),
                ('predicted_relative_residual',step['predicted_relative_residual'],fstep['predicted_relative_residual']),
                ('max_abs_step_yL',step['max_abs_step_yL'],fstep['max_abs_step_yL']),
                ('max_abs_step_qRt',step['max_abs_step_qRt'],fstep['max_abs_step_qRt']),
            ):
                if key=='rank':
                    ok=int(obs)==int(fr); ae=abs(int(obs)-int(fr)); re=float(ae/max(abs(int(obs)),abs(int(fr)),1))
                else:
                    ok,ae,re=smatch(obs,fr,FIRST_REPRO_LIMIT)
                checks.append({'key':key,'pass':bool(ok),'abs_error':float(ae),'relative_error':float(re)})
            g4_step=bool(all(x['pass'] for x in checks))

            samples=[]
            for alpha in ALPHAS:
                x=np.asarray(alpha*dx,float)
                F=np.asarray(fun_x(x),float)
                Flin=np.asarray(F0+alpha*Jdz,float)
                rem=np.asarray(F-Flin,float)
                Hn,Mn=block_norms(F,m)
                Hlin,Mlin=block_norms(Flin,m)
                Hr,Mr=block_norms(rem,m)
                st,ev,freeze_ok,freeze_rows=evaluate_x(x)
                gy,gq=r19.gauge_values(x)
                exact_norm=float(np.linalg.norm(F))
                lin_norm=float(np.linalg.norm(Flin))
                rem_norm=float(np.linalg.norm(rem))
                directional=float(
                    np.linalg.norm((F-F0)/alpha-Jdz)
                    / max(np.linalg.norm(Jdz),TINY)
                )
                finite=bool(
                    np.all(np.isfinite(F)) and np.all(np.isfinite(Flin))
                    and np.all(np.isfinite(rem))
                    and np.isfinite([exact_norm,lin_norm,rem_norm,directional,gy,gq]).all()
                    and ev.get('finite',False)
                )
                gauge_q=bool(
                    finite and float(ev['qerr'])<=Q_LIMIT
                    and abs(gy)<=GAUGE_LIMIT and abs(gq)<=GAUGE_LIMIT
                )
                samples.append({
                    'alpha':float(alpha),
                    'max_abs_x':float(np.max(np.abs(x))),
                    'exact_residual_L2':exact_norm,
                    'exact_residual_ratio':float(exact_norm/max(np.linalg.norm(F0),TINY)),
                    'linear_predicted_residual_L2':lin_norm,
                    'linear_predicted_residual_ratio':float(lin_norm/max(np.linalg.norm(F0),TINY)),
                    'nonlinear_remainder_L2':rem_norm,
                    'relative_nonlinear_remainder':float(rem_norm/max(np.linalg.norm(F0),TINY)),
                    'directional_derivative_mismatch':directional,
                    'H_block_exact_L2':Hn,'M_block_exact_L2':Mn,
                    'H_block_linear_L2':Hlin,'M_block_linear_L2':Mlin,
                    'H_block_remainder_L2':Hr,'M_block_remainder_L2':Mr,
                    'max_epsilon_H':float(ev['maxH']),
                    'max_epsilon_M':float(ev['maxM']),
                    'Q_target_max_normalized_error':float(ev['qerr']),
                    'Y4_residual':float(gy),'Qmean_residual':float(gq),
                    'finite':finite,'gauge_Q_pass':gauge_q,
                    'field_freeze_pass':bool(freeze_ok),
                    'field_freeze':freeze_rows,
                })
                g5 &= finite
                g6 &= gauge_q
                g7 &= bool(freeze_ok)

            alpha1=samples[0]
            ok_alpha1,aea1,rea1=smatch(
                alpha1['exact_residual_L2'],
                frozen['history'][0]['residual_L2_after'],
                FIRST_REPRO_LIMIT
            )
            checks.append({
                'key':'exact_nonlinear_residual_L2_alpha1',
                'pass':ok_alpha1,'abs_error':aea1,'relative_error':rea1
            })
            g4_case=bool(g4_step and ok_alpha1)
            g4 &= g4_case

            remainder_slopes=[
                safe_slope(samples[i]['nonlinear_remainder_L2'],samples[i+1]['nonlinear_remainder_L2'])
                for i in range(len(samples)-1)
            ]
            directional_slopes=[
                safe_slope(samples[i]['directional_derivative_mismatch'],samples[i+1]['directional_derivative_mismatch'])
                for i in range(len(samples)-1)
            ]
            imin=int(np.argmin([s['directional_derivative_mismatch'] for s in samples]))
            ires=int(np.argmin([s['exact_residual_ratio'] for s in samples]))
            rows.append({
                'scale_hinv_Mpc':float(scale),'Nr':int(nr),
                'parent_F0_L2':float(np.linalg.norm(F0)),
                'parent_reproduction':{'pass':p0,'abs_error':ae0,'relative_error':re0},
                'first_step':step,
                'first_step_reproduction':{'checks':checks,'pass':g4_case},
                'exact_over_predicted_alpha1':float(
                    alpha1['exact_residual_L2']/max(alpha1['linear_predicted_residual_L2'],TINY)
                ),
                'samples':samples,
                'remainder_adjacent_log2_slopes':remainder_slopes,
                'directional_mismatch_adjacent_log2_slopes':directional_slopes,
                'summary':{
                    'minimum_directional_derivative_mismatch':float(samples[imin]['directional_derivative_mismatch']),
                    'alpha_at_minimum_directional_mismatch':float(samples[imin]['alpha']),
                    'minimum_exact_residual_ratio':float(samples[ires]['exact_residual_ratio']),
                    'alpha_at_minimum_exact_residual_ratio':float(samples[ires]['alpha']),
                    'median_remainder_slope_largest_three':median_finite(remainder_slopes[:3]),
                    'median_remainder_slope_smallest_three':median_finite(remainder_slopes[-3:]),
                    'median_directional_mismatch_slope_largest_three':median_finite(directional_slopes[:3]),
                    'median_directional_mismatch_slope_smallest_three':median_finite(directional_slopes[-3:]),
                },
            })

    g3=bool(g3 and len(rows)==6)
    g4=bool(g4 and len(rows)==6)
    g5=bool(g5 and sum(len(r['samples']) for r in rows)==78)
    g6=bool(g6 and sum(len(r['samples']) for r in rows)==78)
    g7=bool(g7 and sum(len(r['samples']) for r in rows)==78)

    claim_boundary={
        'more_than_single_x0_direct_direction_per_case':False,
        'nonlinear_optimizer_run':False,
        'corrected_state_accepted_or_certified':False,
        'state_NPZ_written':False,
        'physical_projection_pair_changed':False,
        'physical_field_added':False,
        'Y4_or_Qmean_changed':False,
        'source_changed':False,'coefficient_changed':False,'sign_changed':False,
        'finite_eta_executed':False,'branch_changed':False,'threshold_changed':False,
        'radial_points_removed':False,'historical_artifact_changed':False,
        'time_evolution_run':False,'observational_claimed':False,
        'Repair19c_relabelled':False,
    }
    g8=bool(not any(claim_boundary.values()))

    gates={
        'R19C1_G1_exact_frozen_provenance':g1,
        'R19C1_G2_exact_orthonormal_basis_reproduction':bool(g2),
        'R19C1_G3_exact_parent_reproduction':bool(g3),
        'R19C1_G4_exact_first_step_reproduction':bool(g4),
        'R19C1_G5_complete_finite_directional_sweep':bool(g5),
        'R19C1_G6_exact_gauge_and_Q_preservation':bool(g6),
        'R19C1_G7_field_freeze_invariant':bool(g7),
        'R19C1_G8_claim_boundary':g8,
    }
    if all(gates.values()):
        classification='NL1C7B4_REPAIR19C1_FIRST_STEP_DIRECTIONAL_JACOBIAN_FIDELITY_CHARACTERIZED'
        rc=0
    else:
        classification='NL1C7B4_REPAIR19C1_IMPLEMENTATION_FAIL'
        rc=2

    result={
        'classification':classification,
        'scope':'Repair19c1 directional secant/Jacobian fidelity characterization along the frozen Repair19c first GELSY direction.',
        'provenance':{
            **hashes,
            'repair19c_result_freeze_commit':'e0d7415be5da36757327c0d36cc2eaaae2ecc2d5',
            'repair19c1_prereg_commit':'6318ce0f3a61a6503c4090bde6f4f247563cb704',
        },
        'amplitudes':list(ALPHAS),
        'basis_rows':basis_rows,
        'rows':rows,
        'gates':gates,
        'claim_boundary':claim_boundary,
        'summary':{
            'max_exact_over_predicted_alpha1':float(max(r['exact_over_predicted_alpha1'] for r in rows)),
            'min_exact_over_predicted_alpha1':float(min(r['exact_over_predicted_alpha1'] for r in rows)),
            'minimum_directional_mismatch_over_all':float(min(
                r['summary']['minimum_directional_derivative_mismatch'] for r in rows
            )),
            'maximum_minimum_directional_mismatch_across_cases':float(max(
                r['summary']['minimum_directional_derivative_mismatch'] for r in rows
            )),
        },
        'interpretation_boundary':{
            'nonlinear_closure_certified':False,
            'Jacobian_repair_selected':False,
            'physical_ansatz_changed':False,
            'short_time_eta0_evolution_certified':False,
        },
    }

    out=Path(a.out)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True,allow_nan=False))
    raise SystemExit(rc)


if __name__=='__main__':
    main()
