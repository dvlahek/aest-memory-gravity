#!/usr/bin/env python3
"""GE19 D30: original-action GE06 c2 direct signed-mode pair audit.

This is an *independent diagnostic representation* of the original smooth
quadratic source. It does not patch the production FFT source, remove modes,
change a solver/gate, or certify H3/H4. The nonanalytic Stage E Y is retained
in the independently replayed original H3F bundle.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from contextlib import ExitStack
from pathlib import Path
import numpy as np
from ge19 import h4f3d29r1_analytic_quadratic_support as d29

ROOT = Path(__file__).resolve().parents[1]
PRE = ROOT/'ge19/h4f3d30_direct_ge06_mode_pair_audit_prereg.json'
LOCK = ROOT/'ge19/h4f3d30_direct_ge06_mode_pair_audit_lock.json'
TINY = 1e-300


def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()


def rel(a,b):
    aa=np.asarray(a,complex);bb=np.asarray(b,complex)
    return float(np.linalg.norm(aa-bb)/max(np.linalg.norm(aa),np.linalg.norm(bb),TINY))


def action_eval(mod6,head,jet,tail,nt):
    """Evaluate frozen original GE06 f_c2; 15 complex directional jets."""
    args=tuple(head)+tuple(jet)+tuple(tail)
    if len(args)!=23 or len(jet)!=15:
        raise RuntimeError('D30 original-action GE06 jet interface mismatch')
    out={}
    for key,fun in mod6.f_c2.items():
        value=np.asarray(fun(*args),complex)
        if value.shape not in ((),(nt,)):
            raise RuntimeError('D30 original-action partial shape mismatch '+key)
        out[key]=np.broadcast_to(value,(nt,)).copy()
        if not np.isfinite(out[key]).all():
            raise RuntimeError('D30 nonfinite original-action partial '+key)
    return out


def signed_mode_jets(d29_module,r7,bg,h1,dh1):
    """Only frozen ±6 H1 modes; no numerical Fourier transform of real space."""
    modes=tuple(int(x) for x in r7.FOURIER_N)
    signed={};head=None;tail=None
    for i,m in enumerate(modes):
        args=d29_module.positive_mode_jet(r7,bg,h1,dh1,i)
        if head is None:
            head=args[:3];tail=args[18:]
        jets=tuple(np.asarray(v,complex) for v in args[3:18])
        signed[m]=jets
        signed[-m]=tuple(np.conjugate(v) for v in jets)
    if sorted(signed)!=sorted((*modes,*(-m for m in modes))):
        raise RuntimeError('D30 signed original H1 support mismatch')
    return signed,head,tail


def mode_pair_partials(m,signed,mod6,head,tail,nt):
    """Homogeneous quadratic Fourier coefficient from unordered signed pairs.

    Diagonal p=p contributes f_c2(v_p). For p!=q, the TWO ordered cross
    contributions sum to [f_c2(v_p+v_q)-f_c2(v_p-v_q)]/2.
    """
    keys=tuple(mod6.f_c2)
    parts={key:np.zeros(nt,complex) for key in keys}
    terms=[]
    signed_modes=sorted(signed)
    for i,p in enumerate(signed_modes):
        for q in signed_modes[i:]:
            if p+q!=m:
                continue
            v=signed[p];w=signed[q]
            if p==q:
                z=action_eval(mod6,head,v,tail,nt)
            else:
                plus=action_eval(mod6,head,tuple(a+b for a,b in zip(v,w)),tail,nt)
                minus=action_eval(mod6,head,tuple(a-b for a,b in zip(v,w)),tail,nt)
                z={key:(plus[key]-minus[key])/2.0 for key in keys}
            for key in keys:
                parts[key]+=z[key]
            terms.append([int(p),int(q)])
    if not all(np.isfinite(v).all() for v in parts.values()):
        raise RuntimeError('D30 nonfinite mode-pair partials')
    return parts,terms


def assembled_ge06(r7,bg,partial,m):
    nt=len(bg['x']);x=np.asarray(bg['x'],float)
    Dt=np.asarray(bg['H'],float)[:,None]*r7.fd4_matrix(nt,float(x[0]),float(x[-1]))
    k=float(m)*float(r7.g9.K_REQ[0]/r7.FOURIER_N[0])
    g=r7.assemble_ga_local(partial,Dt,k=k,spatial_real=False)
    zeros=np.zeros(nt,complex)
    main=-np.stack((g['N'],g['L']+g['R'],g['u'],g['phi'],zeros,zeros),axis=0)
    con=-np.stack((g['b'],g['L']-0.5*g['R']),axis=0)
    return main,con


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--results-dir',required=True)
    ap.add_argument('--json-out',required=True)
    ap.add_argument('--npz-out',required=True)
    a=ap.parse_args();rd=Path(a.results_dir).resolve();jp=Path(a.json_out).resolve();zp=Path(a.npz_out).resolve()
    if jp.exists() or zp.exists():
        raise RuntimeError('D30 REFUSE_OVERWRITE')
    pre=json.loads(PRE.read_text());lock=json.loads(LOCK.read_text())
    if pre['classification']!='GE19_D30_PREEXEC_ORIGINAL_GE06_DIRECT_SIGNED_PAIR_DIAGNOSTIC':
        raise RuntimeError('D30 preregistration changed')
    for name,want in lock['sha256_local_files'].items():
        p=ROOT/name
        if not p.is_file() or sha(p)!=want:
            raise RuntimeError('D30 source/prereg/runner SHA lock FAIL '+name)
    for name,want in pre['frozen_source_sha256'].items():
        p=ROOT/name
        if not p.is_file() or sha(p)!=want:
            raise RuntimeError('D30 frozen original-source code lock FAIL '+name)
    for name,want in pre['frozen_outputs_sha256'].items():
        p=rd/name
        if not p.is_file() or sha(p)!=want:
            raise RuntimeError('D30 frozen input SHA lock FAIL '+name)
    old=d29.d28.d27.d20.source.old;r7=old.r7
    parents,_=d29.d28.d27.d26.checked_source_files(rd)
    # D29R1 already passed direct m40 using this frozen source/action cohort.
    prev=json.loads((rd/'ge19_h4f3d29r1_analytic_quadratic_support.json').read_text())
    if prev['classification']!=pre['required_D29R1_classification'] or prev['Z20_certified']:
        raise RuntimeError('D30 original D29R1 result scope FAIL')
    print('GE19_D30_ORIGINAL_ACTION_D29R1_AND_ALL_FROZEN_INPUT_LOCK_PASS',flush=True)
    arrays={}
    with ExitStack() as es:
        z22=es.enter_context(np.load(parents['D22A_NPZ'],allow_pickle=False))
        z13=es.enter_context(np.load(rd/'ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz',allow_pickle=False))
        z29=es.enter_context(np.load(rd/'ge19_h4f3d29r1_analytic_quadratic_support.npz',allow_pickle=False))
        bgs,_,mod6,mod7,_,_,_,_,_=old.build_context(rd,z13)
        bg=bgs[(128,'C_star')];x=np.asarray(bg['x'],float)
        h1=np.asarray(z22['D17_H1_action_primary'],complex)
        dh1=np.asarray(z22['D17_H1dot_action_primary'],complex)
        nt=len(x)
        modes=tuple(int(m) for m in r7.FOURIER_N)
        if (nt!=128 or not np.array_equal(x,z22['x_primary'])
                or h1.shape!=(6,6,128) or dh1.shape!=(6,4,128)
                or modes!=tuple(pre['first_order_modes'])):
            raise RuntimeError('D30 original D17 parent cohort/grid mismatch')
        support=d29.quadratic_support(modes)
        selected=tuple(int(m) for m in pre['diagnostic_modes'])
        if not all((m in support)==pre['expected_support'][str(m)] for m in selected):
            raise RuntimeError('D30 preregistered Fourier support mismatch')
        signed,head,tail=signed_mode_jets(d29,r7,bg,h1,dh1)
        all_main=np.zeros((6,nt,41),complex);all_con=np.zeros((2,nt,41),complex)
        all_bf=np.zeros((nt,41),complex);all_grad=np.zeros((nt,41),complex)
        pair_dictionary={}
        for m in range(41):
            partial,pairs=mode_pair_partials(m,signed,mod6,head,tail,nt)
            if bool(pairs)!=(m in support):
                raise RuntimeError('D30 exact signed pair support disagreement m='+str(m))
            ga,gc=assembled_ge06(r7,bg,partial,m)
            all_main[:,:,m]=ga;all_con[:,:,m]=gc
            k=float(m)*float(r7.g9.K_REQ[0]/r7.FOURIER_N[0])
            all_bf[:,m]=-partial['b_f']
            all_grad[:,m]=1j*k*partial['b_x']
            if m in selected:
                pair_dictionary[str(m)]=pairs
            if m not in support and (np.any(ga) or np.any(gc)):
                raise RuntimeError('D30 off-support direct GE06 must be exact zero m='+str(m))
        for key,val in (('m40_original_action_direct_minus_b_f_128',all_bf[:,40]),
                        ('m40_original_action_direct_plus_dx_b_x_128',all_grad[:,40]),
                        ('m40_original_action_direct_GE06_main_six_by_128',all_main[:,:,40]),
                        ('m40_original_action_direct_GE06_constraint_two_by_128',all_con[:,:,40])):
            replay=rel(val,z29[key])
            if replay>pre['original_m40_direct_replay_relative_limit']:
                raise RuntimeError('D30 m40 original-action D29R1 replay FAIL '+key+' '+str(replay))
        print('GE19_D30_M40_DIRECT_ORIGINAL_ACTION_FULL_ROW_REPLAY_PASS',flush=True)
        # Rebuild the ORIGINAL H3F source separately. Nothing is patched and
        # the old per-mode D27 relative failure is not reclassified.
        d27=d29.d28.d27
        oldbg=r7._bg_point;oldcache=r7._CANONICAL_LOCAL_CACHE;r7._CANONICAL_LOCAL_CACHE={}
        active={'ctx':None}
        def bgpoint(b,t):
            if active['ctx'] is None:raise RuntimeError('D30 action context not initialized')
            return active['ctx'](b,t)
        r7._bg_point=bgpoint
        try:
            evalH,_=d27.d17driver.d16r1.d15.clk.make_original_action_background(r7,bg,'C_star')
            ctx=d27.d17core.ActionBackground(r7,bg,evalH)
            active['ctx']=ctx;ctx.knot_check()
            print('GE19_D30_ORIGINAL_H3F_SOURCE_REBUILD_BEGIN',flush=True)
            sources,sectors=d27.audited_rebuild(r7,d27.r14,mod6,mod7,bg,'C_star',h1,dh1,nx=1024)
        finally:
            r7._bg_point=oldbg;r7._CANONICAL_LOCAL_CACHE=oldcache
        for ib,beta in enumerate(r7.BETAS):
            replay=max(rel(sources[beta]['rhs'],z22[f'beta{ib}_H3F_D17_source_rows']),
                       rel(sources[beta]['rhs_constraint'],z22[f'beta{ib}_H3F_D17_source_constraints']))
            if replay>pre['original_H3F_source_replay_relative_limit']:
                raise RuntimeError('D30 original H3F source replay FAIL beta='+str(beta))
        print('GE19_D30_ORIGINAL_D22A_H3F_FULL_SOURCE_REPLAY_PASS',flush=True)
        orig=np.concatenate([sectors[0.1]['GE06_main'],sectors[0.1]['GE06_constraint']],axis=0)
        direct=np.concatenate([all_main,all_con],axis=0)
        report_modes=[]
        max_supported=0.0
        max_mode=None
        for m in selected:
            orig_row=orig[:,:,m];direct_row=direct[:,:,m]
            original_abs=float(np.max(np.abs(orig_row)))
            candidate_abs=float(np.max(np.abs(direct_row)))
            global_rel=rel(orig_row,direct_row)
            if m in support and global_rel>max_supported:
                max_supported=global_rel;max_mode=m
            # Reconstruct nonanalytic Y separately. The original H3F source
            # still contains it at every mode. We do NOT zero entire modes.
            y=np.asarray(sources[0.1]['Y_H3'][:,:,m],complex)
            y_abs=float(np.max(np.abs(y)))
            if m in (1,14) and (not np.array_equal(direct_row,np.zeros_like(direct_row)) or not y_abs>0):
                raise RuntimeError('D30 offsupport GE06 zero / original nonanalytic Y retention FAIL')
            row={'mode':m,'exact_smooth_GE06_quadratic_supported':m in support,
                 'signed_H1_mode_pairs':pair_dictionary[str(m)],
                 'original_GE06_max_abs_report_only':original_abs,
                 'original_GE06_scalar_first_abs_report_only':float(abs(orig_row[3,0])),
                 'direct_mode_pair_GE06_max_abs_report_only':candidate_abs,
                 'original_vs_direct_all_eight_rows_relative_report_only':global_rel,
                 'original_StageE_Y_max_abs_report_only':y_abs,
                 'original_StageE_Y_scalar_first_abs_report_only':float(abs(y[3,0]))}
            report_modes.append(row)
            print(f'GE19_D30_MODE m={m} support={m in support} pairs={len(pair_dictionary[str(m)])} '
                  f'original_GE06_abs={original_abs:.6e} direct_GE06_abs={candidate_abs:.6e} '
                  f'orig_direct_relative_report_only={global_rel:.6e} Y_abs={y_abs:.6e}',flush=True)
        if len(report_modes)!=len(selected):
            raise RuntimeError('D30 incomplete selected mode dictionary')
        # Store all m=0..40, including exact off-support zeros, without using
        # this candidate in any original production source or H3 integration.
        arrays.update({'direct_GE06_main_six_by_128_by_41':all_main,
                       'direct_GE06_constraint_two_by_128_by_41':all_con,
                       'direct_GE06_minus_b_f_128_by_41':all_bf,
                       'direct_GE06_plus_dx_b_x_128_by_41':all_grad,
                       'original_GE06_main_six_by_128_by_41':sectors[0.1]['GE06_main'],
                       'original_GE06_constraint_two_by_128_by_41':sectors[0.1]['GE06_constraint'],
                       'original_StageE_Y_main_six_by_128_by_41':sources[0.1]['Y_H3']})
        if not all(np.isfinite(v).all() for v in arrays.values()):
            raise RuntimeError('D30 nonfinite source archive')
        result={'classification':'GE19_D30_FROZEN_ORIGINAL_ACTION_DIRECT_SIGNED_GE06_MODE_PAIR_DIAGNOSTIC_COMPLETE_PARENTS_UNCERTIFIED',
                'preregistration':pre['classification'],'source_sha256':sha(Path(__file__)),
                'original_D29R1_JSON_sha256':pre['frozen_outputs_sha256']['ge19_h4f3d29r1_analytic_quadratic_support.json'],
                'input_modes':list(modes),'exact_support_nonnegative':[m for m in range(41) if m in support],
                'selected_modes':report_modes,'max_selected_supported_original_vs_direct_global_relative_report_only':max_supported,
                'max_selected_supported_relative_mode_report_only':max_mode,
                'D29R1_m40_replayed':True,'original_H3F_source_replayed':True,
                'original_D22A_shift_science_FAIL_immutable':True,'original_D27_selected_mode_triplet_FAIL_immutable':True,
                'original_D29_SHA43_execution_FAIL_immutable':True,'D29R1_diagnostic_only':True,
                'original_action_modified':False,'production_GE06_source_modified':False,
                'original_GE07_Lambda_StageE_Y_modified':False,'no_mode_exclusion':True,
                'solver_rerun':False,'original_shift_gate_unchanged':True,
                'Z11_certified':False,'Z20_certified':False,'q20_B20_recomputed':False,
                'full_H4_Ward_certified':False,'Z21_certified':False,'lensing_licensed':False,
                'claim_boundary':'All original GE06 c2 signed-mode pairs evaluated directly on frozen D17 H1 (complex float64). In-support m40 direct original-action replay and unchanged D22A original full H3F source rebuild checked. Results are an independent diagnostic candidate only, not a mathematically rigorous roundoff bound, approved production source, physical H3 Ward result or permission to omit nonanalytic Y or any mode.'}
    jp.parent.mkdir(parents=True,exist_ok=True)
    np.savez_compressed(zp,**arrays)
    jp.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+'\n')
    print('GE19_D30_CLASSIFICATION '+result['classification'],flush=True)


if __name__=='__main__':
    main()
