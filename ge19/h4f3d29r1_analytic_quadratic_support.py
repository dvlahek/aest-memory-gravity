#!/usr/bin/env python3
"""D29R1: identical D29 physics with corrected preregistered D28 SHA-256.

No H3 rerun, source filtering, or modified science gate. The original GE06
f_c2 second directional coefficient is quadratic in its 15 first-order jets.
A direct complex +m20 evaluation checks the allowed m40 coefficient against
the original real-space FFT result, while m1/m14 must be zero at the smooth
analytic GE06 level. The NL0C Stage E Y main source is reported separately.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from contextlib import ExitStack
import numpy as np
from ge19 import h4f3d28_ge06_shift_two_term_provenance as d28

ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/'ge19/h4f3d29r1_analytic_quadratic_support_prereg.json'
LOCK=ROOT/'ge19/h4f3d29r1_analytic_quadratic_support_lock.json'
TINY=1e-300

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda:f.read(1<<20),b''):h.update(block)
    return h.hexdigest()

def pair(z):
    z=complex(z)
    return [float(z.real),float(z.imag)]

def relative(a,b):
    a=np.asarray(a,complex);b=np.asarray(b,complex)
    return float(np.linalg.norm(a-b)/max(float(np.linalg.norm(a)),float(np.linalg.norm(b)),TINY))

def quadratic_support(first_modes):
    """Exact integer-support rule for homogeneous quadratic smooth-action sources."""
    ms=tuple(int(x) for x in first_modes)
    if not ms or any(x<=0 for x in ms) or len(ms)!=len(set(ms)):
        raise ValueError('D29 first-order mode cohort invalid')
    signed=tuple(ms)+tuple(-x for x in ms)
    return frozenset(a+b for a in signed for b in signed)

def positive_mode_jet(r7,bg,h1,dh1,index):
    """Original D17 H1 first-order GE06 jet, in +k complex Fourier basis."""
    im=int(r7.FOURIER_N[index]);kfund=float(r7.g9.K_REQ[0]/r7.FOURIER_N[0]);k=im*kfund
    aa=np.asarray(bg['a'],float); H=np.asarray(bg['H'],float)
    N,S,u,phi=(np.asarray(h1[index,j],complex) for j in (0,1,2,3))
    Sdot,udot,phidot=(np.asarray(dh1[index,j],complex) for j in (0,1,2))
    z=np.zeros_like(N)
    args=(aa,aa*H,np.asarray(bg['Z_action'],float),
          N,S,S,z,u,Sdot,1j*k*S,Sdot,1j*k*S,z,
          udot,1j*k*u,phidot,1j*k*phi,1j*k*N,
          r7.KB,r7.CV,r7.K2,r7.Q0,r7.Z0)
    if len(args)!=23 or any(np.asarray(x).shape not in ((),aa.shape) for x in args):
        raise RuntimeError('D29 original GE06 direction-jet interface mismatch')
    return args

def original_ge06_mode40(r7,mod6,bg,h1,dh1):
    modes=tuple(int(x) for x in r7.FOURIER_N)
    if modes[-1]!=20:
        raise RuntimeError('D29 original +m20 parent absent')
    vals=positive_mode_jet(r7,bg,h1,dh1,modes.index(20))
    nt=len(bg['x']);pd={}
    for name,fn in mod6.f_c2.items():
        arr=np.asarray(fn(*vals),complex)
        if arr.shape not in ((),(nt,)):
            raise RuntimeError('D29 original GE06 partial shape mismatch '+name)
        pd[name]=np.broadcast_to(arr,(nt,)).copy()
        if not np.isfinite(pd[name]).all():
            raise RuntimeError('D29 nonfinite original GE06 complex partial '+name)
    # The +40 coefficient arises from +20+20, with NO FFT of a real-space
    # field and NO zeroing/projection of any original production source.
    k40=40.0*float(r7.g9.K_REQ[0]/r7.FOURIER_N[0])
    xx=np.asarray(bg['x'],float)
    Dt=np.asarray(bg['H'],float)[:,None]*r7.fd4_matrix(nt,float(xx[0]),float(xx[-1]))
    ga=r7.assemble_ga_local(pd,Dt,k=k40,spatial_real=False)
    z=np.zeros(nt,complex)
    rhs=-np.stack((ga['N'],ga['L']+ga['R'],ga['u'],ga['phi'],z,z),axis=0)
    con=-np.stack((ga['b'],ga['L']-0.5*ga['R']),axis=0)
    return pd, rhs, con, k40


def validate_repair_prereg(pre):
    """Only permit the canonical frozen D28 hash repair; preserve all D29 physics inputs."""
    old_pre=json.loads((ROOT/'ge19/h4f3d29_analytic_quadratic_support_prereg.json').read_text())
    old_lock=json.loads((ROOT/'ge19/h4f3d29_analytic_quadratic_support_lock.json').read_text())
    d28_lock=json.loads((ROOT/'ge19/h4f3d28_ge06_shift_two_term_lock.json').read_text())
    oldp='ge19/h4f3d29_analytic_quadratic_support_prereg.json'
    oldsrc='ge19/h4f3d29_analytic_quadratic_support.py'
    oldman='ge19/h4f3d29_analytic_quadratic_support_lock.json'
    d28man='ge19/h4f3d28_ge06_shift_two_term_lock.json'
    d28src='ge19/h4f3d28_ge06_shift_two_term_provenance.py'
    want=d28_lock['sha256_local_files'][d28src]
    broken=old_pre['frozen_source_code_sha256'][d28src]
    if (len(broken)!=43 or len(want)!=64 or
        any(c not in '0123456789abcdef' for c in want) or
        pre['frozen_source_code_sha256']!={d28src:want} or
        pre['D29_original_malformed_D28_SHA43']!=broken or
        pre['D29_original_prereg_sha256']!=sha(ROOT/oldp) or
        pre['D29_original_driver_sha256']!=sha(ROOT/oldsrc) or
        pre['D29_original_lock_sha256']!=sha(ROOT/oldman) or
        pre['D28_original_lock_sha256']!=sha(ROOT/d28man) or
        old_lock['sha256_local_files'][oldp]!=sha(ROOT/oldp) or
        old_lock['sha256_local_files'][oldsrc]!=sha(ROOT/oldsrc)):
        raise RuntimeError('D29R1 canonical SHA repair/immutable D29 source lock FAIL')
    original=dict(pre)
    for key in ('D29R1_repair_scope','D29_original_prereg_sha256',
                'D29_original_driver_sha256','D29_original_lock_sha256',
                'D29_original_malformed_D28_SHA43','D28_original_lock_sha256'):
        original.pop(key)
    original['classification']=old_pre['classification']
    original['frozen_source_code_sha256']=old_pre['frozen_source_code_sha256']
    if original!=old_pre:
        raise RuntimeError('D29R1 attempted non-SHA science input change')
    print('GE19_D29R1_CANONICAL_D28_SHA_AND_IMMUTABLE_D29_HISTORY_PASS',flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--results-dir',required=True)
    p.add_argument('--json-out',required=True)
    p.add_argument('--npz-out',required=True)
    a=p.parse_args();rd=Path(a.results_dir).resolve()
    jp=Path(a.json_out).resolve();zp=Path(a.npz_out).resolve()
    if jp.exists() or zp.exists():raise RuntimeError('D29R1 REFUSE_OVERWRITE')
    pre=json.loads(PRE.read_text());lock=json.loads(LOCK.read_text())
    if pre['classification']!='GE19_D29R1_PREEXEC_CANONICAL_D28_SHA_64_HEX_REPAIR':
        raise RuntimeError('D29 prereg changed')
    validate_repair_prereg(pre)
    for name,want in lock['sha256_local_files'].items():
        if not (ROOT/name).is_file() or sha(ROOT/name)!=want:
            raise RuntimeError('D29 source code/prereg/runner lock FAIL '+name)
    prev=json.loads((ROOT/'ge19/h4f3d28_ge06_shift_two_term_lock.json').read_text())
    for name,want in prev['sha256_local_files'].items():
        if sha(ROOT/name)!=want:
            raise RuntimeError('D29 D28 frozen source code lock FAIL '+name)
    for name,want in pre['frozen_source_code_sha256'].items():
        if sha(ROOT/name)!=want:
            raise RuntimeError('D29 frozen source lock FAIL '+name)
    for name,want in pre['frozen_outputs_sha256'].items():
        if sha(rd/name)!=want:
            raise RuntimeError('D29 frozen local output lock FAIL '+name)
    # Source of truth for original parent and action locks: the passed D28 gate.
    parents,_=d28.d27.d26.checked_source_files(rd)
    modes=tuple(pre['first_order_modes'])
    with ExitStack() as es:
        z22=es.enter_context(np.load(parents['D22A_NPZ'],allow_pickle=False))
        z13=es.enter_context(np.load(rd/'ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz',allow_pickle=False))
        z27=es.enter_context(np.load(rd/'ge19_h4f3d27r2_signed_fft_sector_roundoff.npz',allow_pickle=False))
        z28=es.enter_context(np.load(rd/'ge19_h4f3d28_ge06_shift_two_term_provenance.npz',allow_pickle=False))
        old=d28.d27.d20.source.old;r7=old.r7
        bgs,_,mod6,mod7,_,_,_,_,_=old.build_context(rd,z13)
        bg=bgs[(128,'C_star')];x=np.asarray(bg['x'],float)
        h1=np.asarray(z22['D17_H1_action_primary'],complex)
        dh1=np.asarray(z22['D17_H1dot_action_primary'],complex)
        if not (np.array_equal(x,z22['x_primary'])
                and h1.shape==(6,6,128) and dh1.shape==(6,4,128)
                and modes==tuple(int(k) for k in r7.FOURIER_N)):
            raise RuntimeError('D29 frozen H1 grid/modes mismatch')
        support=quadratic_support(modes)
        expectation=pre['expected_GE06_quadratic_support']
        for m in pre['selected_modes']:
            if (m in support)!=expectation[f'm{m}']:
                raise RuntimeError('D29 exact quadratic selection mismatch m='+str(m))
        print('GE19_D29_FROZEN_ACTION_QUADRATIC_HARMONIC_SELECTION_PASS',flush=True)
        pd,gmain,gcon,k40=original_ge06_mode40(r7,mod6,bg,h1,dh1)
        # Negative sign and Fourier gradient are fixed by original assembler.
        mode40='m40_beta0p1'
        orig_mbf=np.asarray(z28[f'{mode40}_minus_b_f_128'],complex)
        orig_grad=np.asarray(z28[f'{mode40}_plus_dx_b_x_128'],complex)
        new_mbf=-pd['b_f'];new_grad=1j*k40*pd['b_x']
        bf_rel=relative(new_mbf,orig_mbf)
        grad_rel=relative(new_grad,orig_grad)
        if bf_rel>pre['in_support_b_term_replay_relative_limit'] or grad_rel>pre['in_support_b_term_replay_relative_limit']:
            raise RuntimeError(f'D29 m40 direct original-action b_f/b_x replay FAIL {bf_rel} {grad_rel}')
        ref=np.asarray(z27[f'{mode40}_original_main_source_at_first_node_five_by_8'][0],complex)
        direct=np.r_[gmain[:,0],gcon[:,0]]
        rows_rel=relative(ref,direct)
        if rows_rel>pre['in_support_global_row_replay_relative_limit']:
            raise RuntimeError('D29 m40 direct original-action full GE06 row replay FAIL '+str(rows_rel))
        print('GE19_D29_IN_SUPPORT_M40_DIRECT_ACTION_REPLAY_PASS '
              f'bf={bf_rel:.3e} grad={grad_rel:.3e} all_rows={rows_rel:.3e}',flush=True)
        per=[]
        for m,beta in ((14,0.1),(1,1.0),(40,0.1)):
            name=f'm{m}_beta{str(beta).replace(".","p")}'
            archived=np.asarray(z27[f'{name}_original_main_source_at_first_node_five_by_8'],complex)
            original=np.asarray(z28[f'{name}_original_ge06_shift_source_128'],complex)
            y=np.asarray(archived[3,0:6],complex)
            ge06_main=np.asarray(archived[0,0:6],complex)
            row={'mode':m,'beta':beta,'exact_GE06_quadratic_supported':bool(m in support),
                 'original_GE06_shift_first_abs_report_only':float(abs(original[0])),
                 'original_GE06_shift_max_over_128_report_only':float(np.max(np.abs(original))),
                 'original_GE06_main_first_abs_report_only':[float(v) for v in np.abs(ge06_main)],
                 'original_StageE_Y_main_first_abs_report_only':[float(v) for v in np.abs(y)],
                 'GE06_smooth_action_exact_coefficient_if_out_of_support':0.0 if m not in support else None}
            if m not in support and not np.any(np.abs(y)>0):
                raise RuntimeError('D29 Stage E nonanalytic Y main inadvertently discarded')
            per.append(row)
            print(f'GE19_D29_MODE m={m} beta={beta} GE06_pair_allowed={m in support} '
                  f'archived_GE06_shift_abs={abs(original[0]):.6e} '
                  f'archived_GE06_scalar_main_abs={abs(ge06_main[3]):.6e} '
                  f'original_StageE_scalar_abs={abs(y[3]):.6e}',flush=True)
        report={'classification':'GE19_D29R1_ORIGINAL_ACTION_QUADRATIC_HARMONIC_SELECTION_AND_M40_DIRECT_REPLAY_DIAGNOSTIC_COMPLETE_PARENTS_UNCERTIFIED',
            'preregistration':pre['classification'],'source_sha256':sha(Path(__file__)),
            'D28_input_json_sha256':pre['frozen_outputs_sha256']['ge19_h4f3d28_ge06_shift_two_term_provenance.json'],
            'first_order_modes':list(modes),'nonnegative_exact_quadratic_support':sorted(k for k in support if k>=0),
            'in_support_m40_direct_action_replay':{'minus_b_f_relative':bf_rel,'plus_dx_b_x_relative':grad_rel,'all_eight_GE06_rows_global_relative':rows_rel,
                'note':'Direct unchanged original-action c2 on +m20 H1 local jets. The original FFT source was not modified.'},
            'per_case':per,'D29_original_43_character_SHA_lock_FAIL_immutable':True,'D22A_original_shift_FAIL_immutable':True,'D27_original_selected_triplet_FAIL_immutable':True,
            'D28_diagnostic_ONLY':True,'GE06_source_replaced':False,'Y_nonanalytic_source_not_removed':True,
            'original_shift_threshold_unchanged':True,'no_mode_exclusion':True,'H3_reintegrated':False,
            'Z11_certified':False,'Z20_certified':False,'full_H4_Ward_certified':False,'Z21_certified':False,'lensing_licensed':False,
            'claim_boundary':'Exact finite algebraic smooth-GE06 c2 quadratic Fourier support for the frozen six-mode H1 plus original-action allowed m40 direct coefficient replay, and measured original-offsupport outputs. This is not a rigorous floating-point error envelope or proof of H3 Ward constraint propagation. Stage E nonanalytic Y still contributes main rows at modes m1/m14. No original local relative shift FAIL is relabelled.'}
        arrays={'m40_original_action_direct_minus_b_f_128':new_mbf,
                'm40_original_action_direct_plus_dx_b_x_128':new_grad,
                'm40_original_action_direct_GE06_main_six_by_128':gmain,
                'm40_original_action_direct_GE06_constraint_two_by_128':gcon,
                'm40_original_archived_minus_b_f_128':orig_mbf,
                'm40_original_archived_plus_dx_b_x_128':orig_grad}
        if not all(np.isfinite(v).all() for v in arrays.values()):
            raise RuntimeError('D29 nonfinite output')
    jp.parent.mkdir(parents=True,exist_ok=True)
    np.savez_compressed(zp,**arrays)
    jp.write_text(json.dumps(report,sort_keys=True,indent=2,allow_nan=False)+'\n')
    print('GE19_D29R1_CLASSIFICATION '+report['classification'],flush=True)

if __name__=='__main__':main()
