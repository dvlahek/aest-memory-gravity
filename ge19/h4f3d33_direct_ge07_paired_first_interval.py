#!/usr/bin/env python3
"""GE19 D33: original-action direct GE07 signed-pair source and paired first-interval audit.

No physical source, frozen parent, Ward gate, mode cohort, boundary rule, or
production H3 state is modified. Candidate C retains original Stage E Y and
Lambda, plus original-action D30 direct smooth GE06 and direct smooth GE07.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from contextlib import ExitStack
from pathlib import Path
import numpy as np
from ge19 import h4f3d32_independent_sector_first_interval as d32

ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/'ge19/h4f3d33_direct_ge07_paired_first_interval_prereg.json'
LOCK=ROOT/'ge19/h4f3d33_direct_ge07_paired_first_interval_lock.json'
TINY=1e-300


def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda:f.read(1<<20),b''):
            h.update(chunk)
    return h.hexdigest()


def rel(a,b):
    a=np.asarray(a,complex);b=np.asarray(b,complex)
    return float(np.linalg.norm(a-b)/max(np.linalg.norm(a),np.linalg.norm(b),TINY))


def pair(v):
    v=complex(v)
    return [float(v.real),float(v.imag)]


def signed_ge07_jets(r7,bg,h1,dh1):
    """Actual frozen reduced H1: N, L=R=S, b=0, density, Tdot, Tx."""
    nt=len(bg['x']);modes=tuple(int(v) for v in r7.FOURIER_N)
    if h1.shape!=(len(modes),6,nt) or dh1.shape!=(len(modes),4,nt):
        raise RuntimeError('D33 GE07 frozen H1/dot dimensions changed')
    kfund=float(r7.g9.K_REQ[0]/r7.FOURIER_N[0])
    zero=np.zeros(nt,complex)
    signed={}
    for i,m in enumerate(modes):
        jet=(h1[i,0],h1[i,1],h1[i,1],zero,h1[i,5],
             dh1[i,3],1j*(m*kfund)*h1[i,4])
        signed[m]=tuple(np.asarray(v,complex).copy() for v in jet)
        signed[-m]=tuple(np.conjugate(v) for v in signed[m])
    return signed, (np.asarray(bg['a'],float),
                    3.0*float(r7.C_VALUES['C_star'])/np.asarray(bg['a'],float)**3)


def evaluate_c2(mod7,head,jet,nt):
    """Evaluate the unchanged original GE07 common-direction epsilon^2 partials."""
    if len(head)!=2 or len(jet)!=7 or tuple(mod7.f_c2)!=('N_f','L_f','R_f','b_f','rho_f','T_t','T_x'):
        raise RuntimeError('D33 GE07 original directional partial interface mismatch')
    args=(*head,*jet)
    result={}
    for key,fun in mod7.f_c2.items():
        v=np.asarray(fun(*args),complex)
        if v.shape not in ((),(nt,)):
            raise RuntimeError('D33 GE07 original c2 output shape mismatch '+key)
        result[key]=np.broadcast_to(v,(nt,)).copy()
        if not np.isfinite(result[key]).all():
            raise RuntimeError('D33 GE07 nonfinite action partial '+key)
    return result


def direct_ge07_partials(m,signed,mod7,head,nt):
    """Unordered signed-mode pairs, with the original FULL cross coefficient."""
    out={key:np.zeros(nt,complex) for key in mod7.f_c2}
    terms=[];labels=sorted(signed)
    for i,p in enumerate(labels):
        for q in labels[i:]:
            if p+q!=m:
                continue
            v=signed[p];w=signed[q]
            if p==q:
                part=evaluate_c2(mod7,head,v,nt)
            else:
                plus=evaluate_c2(mod7,head,tuple(a+b for a,b in zip(v,w)),nt)
                minus=evaluate_c2(mod7,head,tuple(a-b for a,b in zip(v,w)),nt)
                part={key:(plus[key]-minus[key])/2.0 for key in out}
            for key in out:
                out[key]+=part[key]
            terms.append([int(p),int(q)])
    return out,terms


def assemble_signed_ge07(r7,bg,partial,m):
    nt=len(bg['x']);x=np.asarray(bg['x'],float)
    Dt=np.asarray(bg['H'],float)[:,None]*r7.fd4_matrix(nt,float(x[0]),float(x[-1]))
    k=float(m)*float(r7.g9.K_REQ[0]/r7.FOURIER_N[0])
    q=r7.assemble_m_local(partial,Dt,k=k,spatial_real=False)
    zero=np.zeros(nt,complex)
    main=-np.stack([q['N'],q['L']+q['R'],zero,zero,q['T'],q['rho']],axis=0)
    con=-np.stack([q['b'],q['L']-0.5*q['R']],axis=0)
    return main,con


def check_self(rd,pre,lock):
    if pre['classification']!='GE19_D33_PREEXEC_DIRECT_GE07_SIGNED_PAIR_AND_PAIRED_FIRST_INTERVAL':
        raise RuntimeError('D33 preregistration mismatch')
    branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()
    if branch!=pre['branch'] or branch=='main':
        raise RuntimeError('D33 wrong branch; main forbidden')
    for name,want in lock['sha256_local_files'].items():
        p=ROOT/name
        if not p.is_file() or sha(p)!=want:
            raise RuntimeError('D33 self SHA lock FAIL '+name)
    for name,want in pre['frozen_local_code_sha256'].items():
        p=ROOT/name
        if not p.is_file() or sha(p)!=want:
            raise RuntimeError('D33 frozen code SHA lock FAIL '+name)
    for name,want in pre['frozen_results_sha256'].items():
        p=rd/name
        if not p.is_file() or sha(p)!=want:
            raise RuntimeError('D33 frozen results SHA lock FAIL '+name)
    frozen,j30,j25,r31,j27=d32.verify_self(rd,
        json.loads(d32.PRE.read_text()),json.loads(d32.LOCK.read_text()))
    j32=json.loads((rd/pre['D32_json']).read_text())
    if j32['classification']!=pre['required_D32_classification'] or any(
        j32[k] for k in ('Z11_certified','Z20_certified','Z21_certified','lensing_licensed')):
        raise RuntimeError('D33 frozen D32 diagnostic-only scope mismatch')
    if not j32['nonanalytic_StageE_Y_retained'] or not j32['original_shift_gate_unchanged']:
        raise RuntimeError('D33 D32 action/source scope mismatch')
    print('GE19_D33_ORIGINAL_ACTION_D30_D32_AND_ALL_FROZEN_PARENT_LOCK_PASS',flush=True)
    return frozen,j30,j25,r31,j27,j32


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--results-dir',required=True)
    ap.add_argument('--json-out',required=True)
    ap.add_argument('--npz-out',required=True)
    args=ap.parse_args()
    rd=Path(args.results_dir).resolve();jp=Path(args.json_out).resolve();zp=Path(args.npz_out).resolve()
    if jp.exists() or zp.exists():
        raise RuntimeError('D33 REFUSE_OVERWRITE')
    pre=json.loads(PRE.read_text());lock=json.loads(LOCK.read_text())
    frozen,j30,j25,r31,j27,j32=check_self(rd,pre,lock)
    d31=d32.d31;d25=d31.d25;d30=d31.d30
    r7=d25.d20.source.old.r7;d27=d30.d29.d28.d27
    if d27.d20.source.old.r7 is not r7:
        raise RuntimeError('D33 original action source/operator module mismatch')
    support=set(j30['exact_support_nonnegative'])
    cases=tuple((int(c[0]),float(c[1])) for c in pre['cases'])
    if cases!=((14,0.1),(1,1.0),(40,0.1)) or \
       any(m in support for m in pre['off_support_modes']):
        raise RuntimeError('D33 preregistered support/case cohort mismatch')
    report={
      'classification':'GE19_D33_ORIGINAL_GE07_DIRECT_SIGNED_PAIRS_PAIRED_FIRST_INTERVAL_DIAGNOSTIC_COMPLETE_PARENTS_UNCERTIFIED',
      'preregistration':pre['classification'],'source_sha256':sha(Path(__file__)),
      'scope':'Frozen Cstar Nt128 first-interval only. Original GE07 c2 direct signed-mode pairs, original D30 GE06 pairs, original Lambda and beta-specific Stage E Y independently summed as candidate C. D32 candidate B replay; unchanged boundary projection and n1/n8 Radau. No production code/source changed.',
      'claim_boundary':'GE07 numerical representation diagnostic, not a rigorous floating-point envelope, H1/Noether continuum proof, full H3/H4 Ward certificate, q20, Z20, Z21 or lensing.',
      'D22A_original_science_FAIL_immutable':True,'D27_original_triplet_FAIL_immutable':True,
      'D31_original_remainder_FAIL_immutable':True,'D32_diagnostic_only':True,
      'all_modes_retained':True,'nonanalytic_StageE_Y_retained':True,
      'original_action_modified':False,'production_H3F_source_modified':False,
      'boundary_rule_unchanged_momenta_reprojected':True,'original_shift_gate_unchanged':True,
      'no_observational_tuning':True,'H3_full_window_solve_performed':False,
      'Z11_certified':False,'Z20_certified':False,'Z21_certified':False,
      'full_H4_Ward_certified':False,'lensing_licensed':False,
      'GE07_original_vs_direct_modes':[],'per_beta_source':{},'per_case':[],
      'candidate_C_original_shift_gate_report_only':{}
    }
    arrays={}
    with ExitStack() as es:
        z22=es.enter_context(np.load(frozen['D22A_NPZ'],allow_pickle=False))
        z13=es.enter_context(np.load(rd/'ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz',allow_pickle=False))
        z30=es.enter_context(np.load(rd/pre['D30_npz'],allow_pickle=False))
        z32=es.enter_context(np.load(rd/pre['D32_npz'],allow_pickle=False))
        bgs,_,mod6,mod7,_,_,_,_,_=d25.d20.source.old.build_context(rd,z13)
        bg=bgs[(128,'C_star')];tag='C_star';x=np.asarray(bg['x'],float)
        h1=np.asarray(z22['D17_H1_action_primary'],complex)
        dh1=np.asarray(z22['D17_H1dot_action_primary'],complex)
        if x.shape!=(128,) or not np.array_equal(x,z22['x_primary']) or \
           h1.shape!=(6,6,128) or dh1.shape!=(6,4,128):
            raise RuntimeError('D33 frozen Cstar H1 grid and source parent mismatch')
        direct_ga=np.asarray(z30['direct_GE06_main_six_by_128_by_41'],complex)
        direct_gc=np.asarray(z30['direct_GE06_constraint_two_by_128_by_41'],complex)
        if direct_ga.shape!=(6,128,41) or direct_gc.shape!=(2,128,41):
            raise RuntimeError('D33 original D30 GE06 shapes mismatch')
        signed,head=signed_ge07_jets(r7,bg,h1,dh1)
        if tuple(sorted(signed))!=tuple(sorted([int(m) for m in r7.FOURIER_N]+[-int(m) for m in r7.FOURIER_N])):
            raise RuntimeError('D33 signed GE07 H1 support differs from GE06')
        direct_ma=np.zeros((6,128,41),complex);direct_mc=np.zeros((2,128,41),complex)
        pairs={}
        for m in range(41):
            partial,pair_list=direct_ge07_partials(m,signed,mod7,head,128)
            pairs[str(m)]=pair_list
            if bool(pair_list)!=(m in support):
                raise RuntimeError('D33 original GE07 mode-pair support changed m='+str(m))
            main,con=assemble_signed_ge07(r7,bg,partial,m)
            direct_ma[:,:,m]=main;direct_mc[:,:,m]=con
            if m not in support and (np.any(main) or np.any(con)):
                raise RuntimeError('D33 GE07 exact offsupport source must vanish m='+str(m))
        if not (np.isfinite(direct_ma).all() and np.isfinite(direct_mc).all()):
            raise RuntimeError('D33 direct GE07 source nonfinite')
        print('GE19_D33_ORIGINAL_GE07_DIRECT_SIGNED_PAIR_ALL_41_MODES_PASS',flush=True)
        arrays['direct_GE07_main_six_by_128_by_41']=direct_ma
        arrays['direct_GE07_constraint_two_by_128_by_41']=direct_mc
        old_bg=r7._bg_point;old_cache=r7._CANONICAL_LOCAL_CACHE
        r7._CANONICAL_LOCAL_CACHE={};active={'ctx':None}
        def action_point(b,t):
            if active['ctx'] is None:
                raise RuntimeError('D33 original-action clock unavailable')
            return active['ctx'](b,t)
        r7._bg_point=action_point
        try:
            evalH,_=d25.d17driver.d16r1.d15.clk.make_original_action_background(r7,bg,tag)
            ctx=d25.d17core.ActionBackground(r7,bg,evalH)
            active['ctx']=ctx;ctx.knot_check()
            print('GE19_D33_ORIGINAL_H3F_SECTOR_REBUILD_BEGIN',flush=True)
            rebuilt,sectors=d27.audited_rebuild(r7,d27.r14,mod6,mod7,bg,tag,h1,dh1,nx=1024)
            frozen_source=d25.freeze_source(r7,bg,z22)
            B={};C={};supported_errors=[]
            for ib,beta in enumerate(r7.BETAS):
                orig=rebuilt[beta];sec=sectors[beta]
                replay=max(rel(orig['rhs'],frozen_source[beta]['rhs']),
                           rel(orig['rhs_constraint'],frozen_source[beta]['rhs_constraint']))
                if replay>pre['original_source_replay_limit']:
                    raise RuntimeError('D33 original D22A source replay FAIL beta='+str(beta))
                B[beta],_=d32.independent_candidate(direct_ga,direct_gc,
                       sec['GE07_main'],sec['GE07_constraint'],orig['Q_lambda'],orig['Y_H3'])
                C[beta],_=d32.independent_candidate(direct_ga,direct_gc,
                       direct_ma,direct_mc,orig['Q_lambda'],orig['Y_H3'])
                for key,stem,shape in (('rhs','main_six_by_128_by_41',(6,128,41)),
                                       ('rhs_constraint','constraint_two_by_128_by_41',(2,128,41))):
                    archived=np.asarray(z32[f'beta{ib}_independent_{stem}'],complex)
                    if archived.shape!=shape or rel(archived,B[beta][key])>pre['D32_candidate_B_source_replay_limit']:
                        raise RuntimeError('D33 archived D32 candidate B source replay FAIL beta='+str(beta)+' '+key)
                for m in pre['off_support_modes']:
                    if not np.array_equal(C[beta]['rhs_constraint'][0,:,m],np.zeros(128,complex)):
                        raise RuntimeError('D33 offsupport direct smooth action shift source nonzero')
                    y=np.asarray(orig['Y_H3'][3,:,m],complex)
                    if not np.any(y) or rel(C[beta]['rhs'][3,:,m],y)>pre['off_support_StageE_Y_replay_limit']:
                        raise RuntimeError('D33 original beta-specific nonanalytic Y lost')
                beta_info={
                    'beta':beta,'D22A_original_source_replay_relative':replay,
                    'D32_candidate_B_source_replayed':True,
                    'candidate_C_shift_offsupport_identically_zero':True,
                    'Y_preserved_main_scalar_m1_m14':True,
                    'B_minus_C_constraint_max_abs_report_only':float(np.max(np.abs(B[beta]['rhs_constraint']-C[beta]['rhs_constraint']))),
                    'B_minus_C_main_max_abs_report_only':float(np.max(np.abs(B[beta]['rhs']-C[beta]['rhs'])))
                }
                report['per_beta_source'][str(beta)]=beta_info
                arrays[f'beta{ib}_candidate_C_main_six_by_128_by_41']=C[beta]['rhs']
                arrays[f'beta{ib}_candidate_C_constraint_two_by_128_by_41']=C[beta]['rhs_constraint']
            for m in range(41):
                original_ma=np.asarray(sectors[0.1]['GE07_main'][:,:,m],complex)
                original_mc=np.asarray(sectors[0.1]['GE07_constraint'][:,:,m],complex)
                em=rel(original_ma,direct_ma[:,:,m]);ec=rel(original_mc,direct_mc[:,:,m])
                row={'mode':m,'exact_smooth_GE07_quadratic_supported':m in support,
                     'signed_H1_mode_pairs':pairs[str(m)],
                     'original_GE07_main_max_abs_report_only':float(np.max(np.abs(original_ma))),
                     'direct_GE07_main_max_abs_report_only':float(np.max(np.abs(direct_ma[:,:,m]))),
                     'original_GE07_constraint_max_abs_report_only':float(np.max(np.abs(original_mc))),
                     'direct_GE07_constraint_max_abs_report_only':float(np.max(np.abs(direct_mc[:,:,m]))),
                     'original_vs_direct_main_relative_report_only':em,
                     'original_vs_direct_constraint_relative_report_only':ec}
                report['GE07_original_vs_direct_modes'].append(row)
                if m in support:
                    supported_errors.append(max(em,ec))
                if m in (1,14,40):
                    print(f'GE19_D33_GE07_MODE m={m} support={m in support} '
                          f'orig_con={row["original_GE07_constraint_max_abs_report_only"]:.6e} '
                          f'direct_con={row["direct_GE07_constraint_max_abs_report_only"]:.6e} '
                          f'main_rel={em:.3e} con_rel={ec:.3e}',flush=True)
            report['GE07_m40_original_vs_direct_main_relative_report_only']=report['GE07_original_vs_direct_modes'][40]['original_vs_direct_main_relative_report_only']
            report['GE07_m40_original_vs_direct_constraint_relative_report_only']=report['GE07_original_vs_direct_modes'][40]['original_vs_direct_constraint_relative_report_only']
            report['GE07_all_supported_max_per_mode_relative_report_only']=float(max(supported_errors))
            # The original-action m40 source is a mandatory independent reproduction.
            if max(report['GE07_m40_original_vs_direct_main_relative_report_only'],
                   report['GE07_m40_original_vs_direct_constraint_relative_report_only'])>pre['m40_GE07_original_direct_replay_limit']:
                raise RuntimeError('D33 m40 original GE07 direct source replay FAIL')
            print('GE19_D33_M40_ORIGINAL_GE07_DIRECT_ACTION_REPLAY_PASS',flush=True)
            x0,x1=float(x[0]),float(x[1])
            for m,beta in cases:
                ib=list(r7.BETAS).index(beta)
                key=f'm{m}_beta{str(beta).replace(".","p")}'
                k=float(m*r7.g9.K_REQ[0]/r7.FOURIER_N[0])
                rfb,cfb=r7._source_interp(x,B,m)
                rfc,cfc=r7._source_interp(x,C,m)
                op0C=d25.shift_at(r7,mod6,mod7,bg,tag,k,x0,None,rfc,cfc)
                op1C=d25.shift_at(r7,mod6,mod7,bg,tag,k,x1,None,rfc,cfc)
                op1B=d25.shift_at(r7,mod6,mod7,bg,tag,k,x1,None,rfb,cfb)
                y0C,projection=d31.projection(r7,mod6,mod7,bg,tag,k,x0,rfc,cfc,ib)
                initC=d25.metric_from_y(r7,op0C,y0C,ib)
                proj_pass=bool(max(projection['lapse_relative_backward'],
                                   projection['shift_relative_backward'],
                                   initC['relative_backward'])<=pre['original_boundary_backward_gate'])
                if not proj_pass:
                    raise RuntimeError('D33 unchanged candidate C initial two-row boundary projection FAIL '+key)
                archived_y0=np.asarray(z32[key+'_independent_candidate_B_y0'],complex)
                y0B,_=d31.projection(r7,mod6,mod7,bg,tag,k,x0,rfb,cfb,ib)
                if rel(y0B,archived_y0)>pre['D32_candidate_B_state_replay_limit']:
                    raise RuntimeError('D33 D32 candidate B boundary replay FAIL '+key)
                rows=[]
                for n in pre['substeps']:
                    archived_y1=np.asarray(z32[f'{key}_n{n}_independent_candidate_B_y1'],complex)
                    archived_json=next(c for c in j32['per_case'] if c['mode']==m and c['beta']==beta)
                    old_row=next(c for c in archived_json['comparisons'] if c['substeps']==n)
                    check_B=d25.metric_from_y(r7,op1B,archived_y1,ib)
                    if abs(check_B['relative_backward']-old_row['candidate_B_independent_shift']['relative_backward'])>pre['D32_candidate_B_metric_replay_limit']*max(
                            abs(check_B['relative_backward']),abs(old_row['candidate_B_independent_shift']['relative_backward']),TINY):
                        raise RuntimeError('D33 archived D32 candidate B shift replay FAIL '+key+' n='+str(n))
                    def rr(t,fun=rfc,index=ib):
                        return np.asarray(fun(t),complex)[:,index:index+1]
                    def cc(t,fun=cfc,index=ib):
                        return np.asarray(fun(t),complex)[:,index:index+1]
                    y1C,erC=d25.integrate(r7,mod6,mod7,bg,tag,k,y0C,x0,x1,rr,cc,n)
                    opC=d25.metric_from_y(r7,op1C,y1C,ib)
                    if m==40 and rel(y1C,archived_y1)>pre['m40_endpoint_state_relative_limit']:
                        raise RuntimeError('D33 m40 first-interval original-action state control FAIL n='+str(n))
                    entry={'substeps':n,'candidate_B_archived_shift':old_row['candidate_B_independent_shift'],
                           'candidate_C_independent_shift':opC,'candidate_C_Radau_block_backward':float(erC),
                           'candidate_C_vs_B_end_state_relative_report_only':rel(y1C,archived_y1),
                           'candidate_C_original_shift_gate_report_only':bool(opC['relative_backward']<=pre['original_shift_gate'])}
                    rows.append(entry)
                    arrays[f'{key}_n{n}_candidate_C_y1']=y1C
                    print(f'GE19_D33_MODE m={m} beta={beta} n={n} '
                          f'B_abs={check_B["absolute_residual"]:.6e} '
                          f'C_abs={opC["absolute_residual"]:.6e} '
                          f'C_relative={opC["relative_backward"]:.6e} '
                          f'C_Radau={erC:.3e}',flush=True)
                report['per_case'].append({'mode':m,'beta':beta,'candidate_C_initial':initC,
                    'candidate_C_initial_projection':projection,'candidate_C_initial_projection_pass':proj_pass,
                    'candidate_C_shift_source_first':pair(C[beta]['rhs_constraint'][0,0,m]),
                    'candidate_C_shift_source_last':pair(C[beta]['rhs_constraint'][0,1,m]),
                    'candidate_C_scalar_first':pair(C[beta]['rhs'][3,0,m]),
                    'original_beta_specific_StageE_Y_scalar_first':pair(rebuilt[beta]['Y_H3'][3,0,m]),
                    'comparisons':rows})
                report['candidate_C_original_shift_gate_report_only'][key]=[
                   q['candidate_C_original_shift_gate_report_only'] for q in rows]
                arrays[key+'_candidate_C_y0']=y0C
        finally:
            r7._bg_point=old_bg
            r7._CANONICAL_LOCAL_CACHE=old_cache
    if not all(np.isfinite(a).all() for a in arrays.values()):
        raise RuntimeError('D33 output nonfinite')
    jp.parent.mkdir(parents=True,exist_ok=True);zp.parent.mkdir(parents=True,exist_ok=True)
    jp.write_text(json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+'\n')
    np.savez_compressed(zp,**arrays)
    print('GE19_D33_CLASSIFICATION '+report['classification'],flush=True)


if __name__=='__main__':
    main()
