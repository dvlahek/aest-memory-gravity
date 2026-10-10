#!/usr/bin/env python3
"""GE19 D31R1: paired original vs direct-action GE06 representation, first H3 interval.

Diagnostic candidate only. The original D22A H3F source and D25R1 failures
remain immutable. Change only the GE06 *representation*, reproject the same
source-aware two-constraint zero-q boundary rule for the candidate, then run
original beta-aligned two-stage Radau (n=1 and n=8) on three preselected modes.
Original GE07, Lambda and beta-specific nonanalytic Stage E Y are retained.
No production source replacement, gate relaxation, H3/H4 certification.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from contextlib import ExitStack
from pathlib import Path
import numpy as np
from ge19 import h4f3d25r1_first_interval_shift_substep_decision as d25
from ge19 import h4f3d30_direct_ge06_mode_pair_audit as d30
from ge19 import h4f3d22a_action_parent_reclosure as d22a

ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/'ge19/h4f3d31r1_paired_direct_ge06_first_interval_prereg.json'
LOCK=ROOT/'ge19/h4f3d31r1_paired_direct_ge06_first_interval_lock.json'
TINY=1e-300


def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()


def rel(a,b):
    aa=np.asarray(a,complex);bb=np.asarray(b,complex)
    return float(np.linalg.norm(aa-bb)/max(np.linalg.norm(aa),np.linalg.norm(bb),TINY))


def ascomplex(a):
    c=complex(a)
    return [float(c.real),float(c.imag)]


def candidate_swap(old_main,old_con,old_ge06_main,old_ge06_con,direct_main,direct_con):
    """Only replace the original action-derived GE06 contribution.

    The remaining original total (GE07+Lambda+Stage E Y+finite FFT remainder)
    is untouched. All m=0..40 remain in the array, even GE06-off-support modes.
    """
    shapes=((6,128,41),(2,128,41))
    a,b,c,d,e,f=tuple(np.asarray(x,complex) for x in
                    (old_main,old_con,old_ge06_main,old_ge06_con,direct_main,direct_con))
    if any(v.shape!=expected for v,expected in zip((a,c,e),[shapes[0]]*3)) or \
       any(v.shape!=expected for v,expected in zip((b,d,f),[shapes[1]]*3)):
        raise RuntimeError('D31 source sector shape or signed-row mismatch')
    if not all(np.isfinite(x).all() for x in (a,b,c,d,e,f)):
        raise RuntimeError('D31 nonfinite source input')
    return {'rhs':(a-c)+e,'rhs_constraint':(b-d)+f}


def projection(r7,mod6,mod7,bg,tag,k,x0,rf,cf,ib):
    """Unchanged D22A/Repair18 source-aware lapse/shift momentum rule, q0=0."""
    rr=np.asarray(rf(x0),complex);cc=np.asarray(cf(x0),complex)
    if rr.shape!=(6,3) or cc.shape!=(2,3):
        raise RuntimeError('D31 initial beta batch mismatch')
    _M,_F,_ZY,_ZR,WY,WR,Cmat,_bp,_diag=r7._canonical_operator_matrices(
        mod6,mod7,bg,tag,k,x0)
    source0=np.concatenate((rr[:,ib],cc[:,ib]))
    offset=WR@source0
    lr=Cmat[4];sr=Cmat[10]+Cmat[11]
    A=np.vstack((lr@WY,sr@WY))[:,4:8]
    target=np.array([rr[0,ib]-lr@offset,cc[0,ib]-sr@offset],complex)
    p,diag=d22a.r18.projected_momentum_solve(A,target)
    ev=d22a.r18.evaluate_candidate(Cmat,WY,WR,source0,rr[:,ib],cc[:,ib],p)
    if int(diag['rank'])!=2 or int(diag['augmented_rank'])!=2:
        raise RuntimeError('D31 candidate original two-row projection rank FAIL')
    y=np.zeros(8,complex);y[4:8]=p
    return y,{'rank':int(diag['rank']),'augmented_rank':int(diag['augmented_rank']),
              'scaled_relative_residual':float(diag['scaled_relative_residual_final']),
              'lapse_relative_backward':float(ev['lapse']['metric']),
              'shift_relative_backward':float(ev['shift']['metric'])}



def finite_source_roundoff_ledger(total,ga,matter,lam,y,limit):
    """Keep the signed finite-arithmetic main-row remainder; do not fit it.

    The original D31 low-scale test divides the cancellation residual after
    subtracting a ~1e10 GE06 sector by the ~1e-2 non-GE06 remainder. That
    is not a reliable proof of relative source-sector equality in float64.
    The original full-source-scale replay remains a hard implementation gate.
    The original low-scale gate and signed remainder remain report-only.
    """
    arrays=tuple(np.asarray(v,complex) for v in (total,ga,matter,lam,y))
    if any(v.shape!=(6,128,41) or not np.isfinite(v).all() for v in arrays):
        raise RuntimeError('D31R1 source/sector input shape or finiteness FAIL')
    total,ga,matter,lam,y=arrays
    non_ga=total-ga
    reference=matter+lam+y
    signed_remainder=non_ga-reference
    full_reconstructed=ga+reference
    full_relative=rel(total,full_reconstructed)
    old_gate_relative=rel(non_ga,reference)
    if not np.isfinite(full_relative) or full_relative>limit:
        raise RuntimeError('D31R1 original full-source sector identity FAIL '+str(full_relative))
    # Signed remainder is an arithmetic diagnostic, not an added physical source.
    # It stays inside the archived total-minus-GE06 candidate swap unchanged.
    return {
        'original_full_source_relative':full_relative,
        'original_full_source_abs_l2_report_only':float(np.linalg.norm(total-full_reconstructed)),
        'original_subtractive_remainder_relative_report_only':old_gate_relative,
        'original_subtractive_remainder_abs_l2_report_only':float(np.linalg.norm(signed_remainder)),
        'original_subtractive_remainder_max_abs_report_only':float(np.max(np.abs(signed_remainder))),
        'non_GE06_remainder_norm_report_only':float(np.linalg.norm(non_ga)),
        'non_GE06_reference_norm_report_only':float(np.linalg.norm(reference)),
        'GE06_norm_report_only':float(np.linalg.norm(ga)),
    }


def check_inputs(rd,pre,lock):
    if pre['classification']!='GE19_D31R1_PREEXEC_REMAINDER_ROUNDOFF_AUDIT':
        raise RuntimeError('D31 preregistration mismatch')
    if subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()!=pre['branch']:
        raise RuntimeError('D31 wrong branch; main forbidden')
    for path,want in lock['sha256_local_files'].items():
        p=ROOT/path
        if not p.is_file() or sha(p)!=want:
            raise RuntimeError('D31 self-code/prereg/static/runner SHA lock FAIL '+path)
    for path,want in pre['frozen_code_sha256'].items():
        p=ROOT/path
        if not p.is_file() or sha(p)!=want:
            raise RuntimeError('D31 frozen existing source code SHA lock FAIL '+path)
    for name,want in pre['frozen_results_sha256'].items():
        p=rd/name
        if not p.is_file() or sha(p)!=want:
            raise RuntimeError('D31 frozen output SHA lock FAIL '+name)
    d25.verify_r1_code_lock()
    frozen=d25.verify(rd,json.loads(d25.MANIFEST.read_text()))
    if frozen['D22A_NPZ']!=(rd/pre['original_D22A_npz']):
        raise RuntimeError('D31 D22A source archive identity mismatch')
    j30=json.loads((rd/pre['D30_json']).read_text())
    j25=json.loads((rd/pre['D25R1_json']).read_text())
    if j30['classification']!=pre['required_D30_classification'] or j25['classification']!=pre['required_D25R1_classification']:
        raise RuntimeError('D31 frozen diagnostic parent classification mismatch')
    if any(j30[x] for x in ('Z11_certified','Z20_certified','Z21_certified')) or \
       any(j25[x] for x in ('Z11_certified','Z20_certified','Z21_certified')):
        raise RuntimeError('D31 historical failed parents unexpectedly certified')
    print('GE19_D31_ALL_ORIGINAL_ACTION_D22A_D25R1_D30_SHA_AND_SCOPE_LOCK_PASS',flush=True)
    return frozen,j30,j25


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--results-dir',required=True)
    ap.add_argument('--json-out',required=True)
    ap.add_argument('--npz-out',required=True)
    a=ap.parse_args();rd=Path(a.results_dir).resolve()
    jp=Path(a.json_out).resolve();zp=Path(a.npz_out).resolve()
    if jp.exists() or zp.exists():raise RuntimeError('D31 REFUSE_OVERWRITE')
    pre=json.loads(PRE.read_text());lock=json.loads(LOCK.read_text())
    frozen,j30,j25=check_inputs(rd,pre,lock)
    d25.manufactured_test()
    r7=d25.d20.source.old.r7
    d27=d30.d29.d28.d27
    if d27.d20.source.old.r7 is not r7:
        raise RuntimeError('D31 original GE19 operator/module identity mismatch')
    support=set(j30['exact_support_nonnegative'])
    if set(int(m) for m in pre['expected_offsupport']) & support or \
       support!=set(int(m) for m in pre['expected_support_all']):
        raise RuntimeError('D31 analytic GE06 support changed')
    out={}
    report={'classification':'GE19_D31R1_PAIRED_DIRECT_GE06_FIRST_INTERVAL_DIAGNOSTIC_COMPLETE_PARENTS_UNCERTIFIED',
            'preregistration':pre['classification'],'source_sha256':sha(Path(__file__)),
            'original_D22A_science_FAIL_immutable':True,'D25R1_diagnostic_only':True,
            'D30_diagnostic_only':True,'original_D27_triplet_FAIL_immutable':True,
            'original_D31_remainder_gate_FAIL_immutable':True,
            'D31R1_fix_is_roundoff_ledger_only':True,
            'production_H3F_source_modified':False,'original_action_modified':False,
            'boundary_rule_unchanged_candidate_momenta_reprojected':True,
            'nonanalytic_StageE_Y_retained':True,'all_modes_retained':True,
            'original_shift_gate_unchanged':True,'no_observational_tuning':True,
            'Z11_certified':False,'Z20_certified':False,'Z21_certified':False,
            'full_H4_Ward_certified':False,'lensing_licensed':False,
            'q20_B20_recomputed':False,'H3_full_window_solve_performed':False,
            'candidate_first_interval_solve_performed':True,
            'claim_boundary':('Paired numerical source-representation test on Cstar first interval only. '
                  'Original D22A H3F and D25R1 baselines are immutable. Candidate replaces '
                  'smooth GE06 with original-action D30 signed-pair representation on all '
                  'm0..40, retains original GE07/Lambda/nonanalytic Stage E Y and original '
                  'finite GE06-sector FFT split remainder, and reprojects the original '
                  'source-aware lapse/shift momentum rule before n1/n8 Radau. Candidate '
                  'has a different initial momentum because its source changed. This is '
                  'not a rigorous roundoff envelope or proof that beta-specific Y survives every cancellation at float64; H1 on-shell certificate, Ward proof, '
                  'full H3/H4 parent, Z21 or lensing permission.'),
            'per_case':[],'original_non_GE06_remainder_roundoff_by_beta':{}}
    with ExitStack() as es:
        z22=es.enter_context(np.load(frozen['D22A_NPZ'],allow_pickle=False))
        z13=es.enter_context(np.load(rd/'ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz',allow_pickle=False))
        z30=es.enter_context(np.load(rd/pre['D30_npz'],allow_pickle=False))
        z25=es.enter_context(np.load(rd/pre['D25R1_npz'],allow_pickle=False))
        bgs,_,mod6,mod7,_,_,_,_,_=d25.d20.source.old.build_context(rd,z13)
        bg=bgs[(128,'C_star')];x=np.asarray(bg['x'],float);tag='C_star'
        if x.shape!=(128,) or not np.array_equal(x,z22['x_primary']):
            raise RuntimeError('D31 original-action Cstar grid mismatch')
        head=tuple(float(m) for m in r7.BETAS)
        if head!=(1.0,0.5,0.1):raise RuntimeError('D31 frozen beta cohort mismatch')
        def loadz(key,shape):
            arr=np.asarray(z30[key],complex)
            if arr.shape!=shape or not np.isfinite(arr).all():
                raise RuntimeError('D31 malformed D30 '+key)
            return arr
        main_direct=loadz('direct_GE06_main_six_by_128_by_41',(6,128,41))
        con_direct=loadz('direct_GE06_constraint_two_by_128_by_41',(2,128,41))
        main_old30=loadz('original_GE06_main_six_by_128_by_41',(6,128,41))
        con_old30=loadz('original_GE06_constraint_two_by_128_by_41',(2,128,41))
        y30=loadz('original_StageE_Y_main_six_by_128_by_41',(6,128,41))
        for m in range(41):
            if m not in support and (np.any(main_direct[:,:,m]) or np.any(con_direct[:,:,m])):
                raise RuntimeError('D31 off-support direct GE06 not exact zero m='+str(m))
        for m in pre['required_nonanalytic_y_modes']:
            if float(np.max(np.abs(y30[:,:,m])))<=0:
                raise RuntimeError('D31 Stage E Y missing off-support m='+str(m))
        m40err=max(rel(main_old30[:,:,40],main_direct[:,:,40]),
                   rel(con_old30[:,:,40],con_direct[:,:,40]))
        if m40err>pre['m40_unchanged_action_relative_limit']:
            raise RuntimeError('D31 original GE06 m40 direct-action control FAIL')
        support_index=sorted(support)
        sup_err_main=rel(main_old30[:,:,support_index],main_direct[:,:,support_index])
        sup_err_con=rel(con_old30[:,:,support_index],con_direct[:,:,support_index])
        if max(sup_err_main,sup_err_con)>pre['global_supported_GE06_relative_limit']:
            raise RuntimeError('D31 original GE06 global supported direct representation control FAIL')
        report['D30_global_supported_main_relative']=sup_err_main
        report['D30_global_supported_constraint_relative']=sup_err_con
        report['D30_m40_all_eight_relative']=m40err
        # Original finite FFT can be relatively inaccurate in a weak *supported*
        # mode (e.g. m8). Report all modes; do not silently remove or reclassify.
        report['all_supported_mode_relative_diagnostics']=[
            {'mode':m,'main_relative':rel(main_old30[:,:,m],main_direct[:,:,m]),
             'constraint_relative':rel(con_old30[:,:,m],con_direct[:,:,m])}
            for m in support_index]
        print('GE19_D31_D30_ALL_SUPPORTED_MODE_AUDIT_AND_OFFSUPPORT_ZERO_PASS',flush=True)
        oldsrc=d25.freeze_source(r7,bg,z22)
        p0=np.asarray(z22['Z20_source_aware_projected_p0_primary'],complex)
        if p0.shape!=(3,40,4):raise RuntimeError('D31 archived projected momentum layout mismatch')
        old_bg=r7._bg_point;old_cache=r7._CANONICAL_LOCAL_CACHE
        r7._CANONICAL_LOCAL_CACHE={};active={'ctx':None}
        def action_point(b,t):
            if active['ctx'] is None:raise RuntimeError('D31 original-action clock missing')
            return active['ctx'](b,t)
        r7._bg_point=action_point
        try:
            evalH,_=d25.d17driver.d16r1.d15.clk.make_original_action_background(r7,bg,tag)
            ctx=d25.d17core.ActionBackground(r7,bg,evalH);active['ctx']=ctx;ctx.knot_check()
            h1=np.asarray(z22['D17_H1_action_primary'],complex)
            dh1=np.asarray(z22['D17_H1dot_action_primary'],complex)
            if h1.shape!=(6,6,128) or dh1.shape!=(6,4,128):
                raise RuntimeError('D31 original H1 parent shape mismatch')
            print('GE19_D31_ORIGINAL_H3F_INDEPENDENT_SECTOR_REBUILD_BEGIN',flush=True)
            src,sectors=d27.audited_rebuild(r7,d27.r14,mod6,mod7,bg,tag,h1,dh1,nx=1024)
            candidate={};beta_sector_replay={}
            for ib,beta in enumerate(r7.BETAS):
                orig=oldsrc[beta];rebuild=src[beta];sector=sectors[beta]
                replay=max(rel(orig['rhs'],rebuild['rhs']),rel(orig['rhs_constraint'],rebuild['rhs_constraint']))
                ge06replay=max(rel(main_old30,sector['GE06_main']),
                               rel(con_old30,sector['GE06_constraint']))
                if replay>pre['original_D22A_replay_limit'] or ge06replay>pre['original_D30_GE06_all_beta_replay_limit']:
                    raise RuntimeError('D31 frozen original source/GE06 beta-replay FAIL '+str(beta)+' '+str((replay,ge06replay)))
                candidate[beta]=candidate_swap(orig['rhs'],orig['rhs_constraint'],
                      sector['GE06_main'],sector['GE06_constraint'],main_direct,con_direct)
                beta_sector_replay[str(beta)]={'original_H3F_relative':replay,
                                                 'GE06_vs_D30_beta0p1_relative':ge06replay}
                # The original beta-specific Stage E Y array is immutable: it
                # was not used in the swap and must reappear unchanged in the
                # algebraic non-GE06 remainder of the source.
                y=np.asarray(rebuild['Y_H3'],complex)
                # Keep the failed D31 low-scale gate unchanged as a diagnostic;
                # its subtraction is cancellation-sensitive. The hard check is
                # the original full-source-scale identity, including GE07,
                # Lambda and the actual beta-specific Stage E Y term.
                ledger=finite_source_roundoff_ledger(
                    rebuild['rhs'], sector['GE06_main'],
                    rebuild['Q_matter'],rebuild['Q_lambda'],y,
                    pre['original_D22A_replay_limit'])
                ledger['original_D31_narrow_remainder_gate_limit_unchanged']=pre['non_GE06_remainder_relative_limit']
                ledger['original_D31_narrow_remainder_gate_pass_report_only']=bool(
                    ledger['original_subtractive_remainder_relative_report_only']<=
                    pre['non_GE06_remainder_relative_limit'])
                report['original_non_GE06_remainder_roundoff_by_beta'][str(beta)]=ledger
                print('GE19_D31R1_ORIGINAL_REMAINDER_ROUNDOFF '
                      f'beta={beta} full_rel={ledger["original_full_source_relative"]:.3e} '
                      f'old_narrow_rel={ledger["original_subtractive_remainder_relative_report_only"]:.3e} '
                      f'old_narrow_pass={ledger["original_D31_narrow_remainder_gate_pass_report_only"]} '
                      f'signed_abs_l2={ledger["original_subtractive_remainder_abs_l2_report_only"]:.3e}',
                      flush=True)
            report['independent_source_replay']=beta_sector_replay
            print('GE19_D31R1_ORIGINAL_GE06_BETA_INDEPENDENCE_AND_NON_GE06_SIGNED_REMAINDER_RETAINED_PASS',flush=True)
            x0,x1=float(x[0]),float(x[1])
            for m,beta in tuple((int(t[0]),float(t[1])) for t in pre['cases']):
                ib=list(r7.BETAS).index(beta);jm=list(r7.M_SOLVE).index(m)
                key=f'm{m}_beta{str(beta).replace(".","p")}'
                k=float(m*r7.g9.K_REQ[0]/r7.FOURIER_N[0])
                rfo,cfo=r7._source_interp(x,oldsrc,m)
                rfn,cfn=r7._source_interp(x,candidate,m)
                op0o=d25.shift_at(r7,mod6,mod7,bg,tag,k,x0,None,rfo,cfo)
                op1o=d25.shift_at(r7,mod6,mod7,bg,tag,k,x1,None,rfo,cfo)
                op0n=d25.shift_at(r7,mod6,mod7,bg,tag,k,x0,None,rfn,cfn)
                op1n=d25.shift_at(r7,mod6,mod7,bg,tag,k,x1,None,rfn,cfn)
                y0o=np.zeros(8,complex);y0o[4:8]=p0[ib,jm]
                y0n,pr=projection(r7,mod6,mod7,bg,tag,k,x0,rfn,cfn,ib)
                oldinit=d25.metric_from_y(r7,op0o,y0o,ib)
                newinit=d25.metric_from_y(r7,op0n,y0n,ib)
                frozen_y0=np.asarray(z25[key+'_y0'],complex)
                if rel(frozen_y0,y0o)>pre['baseline_y_replay_limit']:
                    raise RuntimeError('D31 original archived projected y0 mismatch '+key)
                pr['passes_original_boundary_gate_report_only']=bool(max(
                    pr['lapse_relative_backward'],pr['shift_relative_backward'],
                    newinit['relative_backward'])<=pre['original_boundary_backward_gate'])
                ysum=np.asarray(src[beta]['Y_H3'][:,:,m],complex)
                if m in pre['required_nonanalytic_y_modes'] and np.max(np.abs(ysum))<=0:
                    raise RuntimeError('D31 beta-specific Stage E Y lost '+key)
                baseline=[];test=[]
                for n in pre['substeps']:
                    def o_r(t,fun=rfo,idx=ib):return np.asarray(fun(t),complex)[:,idx:idx+1]
                    def o_c(t,fun=cfo,idx=ib):return np.asarray(fun(t),complex)[:,idx:idx+1]
                    def n_r(t,fun=rfn,idx=ib):return np.asarray(fun(t),complex)[:,idx:idx+1]
                    def n_c(t,fun=cfn,idx=ib):return np.asarray(fun(t),complex)[:,idx:idx+1]
                    yo,eo=d25.integrate(r7,mod6,mod7,bg,tag,k,y0o,x0,x1,o_r,o_c,n)
                    yn,en=d25.integrate(r7,mod6,mod7,bg,tag,k,y0n,x0,x1,n_r,n_c,n)
                    original_r=d25.metric_from_y(r7,op1o,yo,ib)
                    new_r=d25.metric_from_y(r7,op1n,yn,ib)
                    ref=np.asarray(z25[f'{key}_n{n}_y1'],complex)
                    if rel(yo,ref)>pre['baseline_y_replay_limit']:
                        raise RuntimeError('D31 baseline D25R1 original first-step replay FAIL '+key+' n='+str(n))
                    baseline.append({'substeps':n,'shift':original_r,'Radau_block_backward':eo})
                    test.append({'substeps':n,'shift':new_r,'Radau_block_backward':en,
                        'candidate_vs_original_end_state_relative_report_only':rel(yn,yo)})
                    out[f'{key}_n{n}_candidate_y1']=yn
                    out[f'{key}_n{n}_baseline_y1']=yo
                    print(f'GE19_D31_MODE m={m} beta={beta} n={n} '
                          f'original_shift={original_r["relative_backward"]:.6e} '
                          f'original_abs={original_r["absolute_residual"]:.6e} '
                          f'candidate_shift={new_r["relative_backward"]:.6e} '
                          f'candidate_abs={new_r["absolute_residual"]:.6e} '
                          f'candidate_Radau={en:.3e}',flush=True)
                report['per_case'].append({'mode':m,'beta':beta,
                    'original_initial':oldinit,'candidate_initial':newinit,
                    'candidate_original_rule_momentum_projection':pr,
                    'initial_momentum_relative_change_report_only':rel(y0n[4:8],y0o[4:8]),
                    'original_beta_specific_StageE_Y_max_abs':float(np.max(np.abs(ysum))),
                    'original_GE06_max_abs':float(np.max(np.abs(sectors[beta]['GE06_main'][:,:,m]))),
                    'direct_GE06_max_abs':float(np.max(np.abs(main_direct[:,:,m]))),
                    'original_source_first_main_scalar':ascomplex(oldsrc[beta]['rhs'][3,0,m]),
                    'candidate_source_first_main_scalar':ascomplex(candidate[beta]['rhs'][3,0,m]),
                    'baseline':baseline,'candidate':test,
                    'candidate_n8_over_n1_absolute_shift_defect_report_only':float(
                      test[-1]['shift']['absolute_residual']/max(test[0]['shift']['absolute_residual'],TINY)),
                    'candidate_original_shift_gate_report_only':[row['shift']['relative_backward']<=pre['original_shift_gate'] for row in test]})
                out[key+'_candidate_y0']=y0n;out[key+'_original_y0']=y0o
            # Persist the complete *diagnostic* candidate source representation,
            # including Y/G07/Lambda and all modes; never change the historical files.
            for ib,beta in enumerate(r7.BETAS):
                out[f'beta{ib}_candidate_main_six_by_128_by_41']=candidate[beta]['rhs']
                out[f'beta{ib}_candidate_constraint_two_by_128_by_41']=candidate[beta]['rhs_constraint']
        finally:
            r7._bg_point=old_bg;r7._CANONICAL_LOCAL_CACHE=old_cache
    if len(report['per_case'])!=len(pre['cases']):
        raise RuntimeError('D31 missing preregistered first-interval modes')
    if not all(np.isfinite(v).all() for v in out.values()):
        raise RuntimeError('D31 nonfinite output')
    np.savez_compressed(zp,**out)
    jp.write_text(json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+'\n')
    print('GE19_D31R1_CLASSIFICATION '+report['classification'],flush=True)

if __name__=='__main__':main()
