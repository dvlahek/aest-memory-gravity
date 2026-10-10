#!/usr/bin/env python3
"""D28 original GE06 Eb two-term provenance on frozen D17/D27R2 H1.

Only report signed -b_f and +d_x(b_x), exactly as the ORIGINAL assembler
Eb=b_f-d_x(b_x). This audit does NOT modify the source or rerun H3.
"""
from __future__ import annotations
import argparse
from contextlib import ExitStack
import hashlib
import json
from pathlib import Path
import numpy as np
from ge19 import h4f3d27r2_signed_fft_sector_roundoff_audit as d27

ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/'ge19/h4f3d28_ge06_shift_two_term_prereg.json'
LOCK=ROOT/'ge19/h4f3d28_ge06_shift_two_term_lock.json'
TINY=1e-300


def sha256(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()


def relative(a,b):
    a=np.asarray(a,complex); b=np.asarray(b,complex)
    return float(np.linalg.norm(a-b)/max(np.linalg.norm(a),np.linalg.norm(b),TINY))


def pair(c):
    z=complex(c)
    return [float(z.real),float(z.imag)]


def capture_ge06_b_terms(r7, expected_shape, collected):
    """Transparent original-assembler wrapper: inspect, then return unaltered output."""
    original=r7.assemble_ga_local
    def capture(pd, Dt, k=None, spatial_real=False, kfund=None):
        if not spatial_real or kfund is None:
            raise RuntimeError('D28 unexpected GE06 source representation')
        bf=np.asarray(pd['b_f'],float)
        bx=np.asarray(pd['b_x'],float)
        if bf.shape!=expected_shape or bx.shape!=expected_shape:
            raise RuntimeError('D28 original GE06 b partials shape mismatch')
        if not (np.isfinite(bf).all() and np.isfinite(bx).all()):
            raise RuntimeError('D28 nonfinite original GE06 partials')
        dx=np.asarray(r7.spectral_dx(bx,kfund),float)
        result=original(pd,Dt,k=k,spatial_real=spatial_real,kfund=kfund)
        eb=np.asarray(result['b'],float)
        if eb.shape!=expected_shape or not np.isfinite(dx).all() or not np.isfinite(eb).all():
            raise RuntimeError('D28 original GE06 Eb shape/nonfinite')
        # Exact original assembler equality: do not replace it by a fitted sum.
        if not np.array_equal(eb,bf-dx):
            raise RuntimeError('D28 original GE06 Eb=b_f-d_x(b_x) exact real-space FAIL')
        collected.append({'minus_b_f':(-bf).copy(), 'plus_dx_b_x':dx.copy(),
                          'original_ge06_Eb':eb.copy()})
        return result
    return capture


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--results-dir',required=True)
    ap.add_argument('--json-out',required=True)
    ap.add_argument('--npz-out',required=True)
    args=ap.parse_args()
    rd=Path(args.results_dir).resolve()
    jp=Path(args.json_out).resolve()
    zp=Path(args.npz_out).resolve()
    if jp.exists() or zp.exists():raise RuntimeError('D28 refuse overwrite')
    pre=json.loads(PRE.read_text()); lock=json.loads(LOCK.read_text())
    if pre['classification']!='GE19_D28_PREEXEC_ORIGINAL_GE06_EB_TWO_TERM_PROVENANCE':
        raise RuntimeError('D28 prereg mismatch')
    for relative_path,want in lock['sha256_local_files'].items():
        path=ROOT/relative_path
        if not path.is_file() or sha256(path)!=want:
            raise RuntimeError('D28 source/prereg/runner SHA lock mismatch '+relative_path)
    oldlock=json.loads((ROOT/'ge19/h4f3d27r2_signed_fft_sector_roundoff_lock.json').read_text())
    for relative_path,want in oldlock['sha256_local_files'].items():
        path=ROOT/relative_path
        if not path.is_file() or sha256(path)!=want:
            raise RuntimeError('D28 frozen D27R2 source lock mismatch '+relative_path)
    for filename,want in pre['frozen_D27R2_outputs'].items():
        p=rd/filename
        if not p.is_file() or sha256(p)!=want:
            raise RuntimeError('D28 frozen D27R2 output SHA mismatch '+filename)
    parents,_=d27.d26.checked_source_files(rd)
    for key,spec in json.loads(d27.PRE.read_text())['frozen_D26_outputs'].items():
        p=rd/spec['filename']
        if not p.is_file() or sha256(p)!=spec['sha256']:
            raise RuntimeError('D28 D26 parent lock mismatch '+key)
        parents[key]=p
    if sha256(ROOT/'ge19/h4f3d27r2_signed_fft_sector_roundoff_audit.py')!=pre['D27R2_source_sha256']:
        raise RuntimeError('D28 D27R2 code SHA mismatch')
    print('GE19_D28_ALL_FROZEN_SOURCE_AND_D27R2_OUTPUT_LOCK_PASS',flush=True)
    d26j=json.loads(parents['D26_JSON'].read_text())
    d27j=json.loads((rd/'ge19_h4f3d27r2_signed_fft_sector_roundoff.json').read_text())
    rows27={(x['mode'],float(x['beta'])):x for x in d27j['per_case']}
    out={'classification':'GE19_D28_FROZEN_GE06_SHIFT_BF_GRADBX_DIAGNOSTIC_COMPLETE_PARENTS_UNCERTIFIED',
         'preregistration':pre['classification'],'source_sha256':sha256(Path(__file__)),
         'D27R2_input_json_sha256':pre['frozen_D27R2_outputs']['ge19_h4f3d27r2_signed_fft_sector_roundoff.json'],
         'D27R2_original_selected_triplet_FAIL_immutable':True,
         'D22A_science_FAIL_immutable':True,'D25_original_replay_FAIL_immutable':True,
         'D27R1_undefined_nx_FAIL_immutable':True,
         'original_action_modified':False,'H3F_source_modified':False,
         'solver_rerun':False,'boundary_modified':False,
         'Z11_certified':False,'Z20_certified':False,'q20_B20_recomputed':False,
         'full_H4_Ward_certified':False,'Z21_certified':False,'lensing_licensed':False,
         'claim_boundary':'Only exact original GE06 Eb=b_f-dx(b_x) real-space terms, signed source -b_f+dx(b_x), independently transformed selected modes, first-interval delta and knotwise PCHIP derivatives. D17 H1 and GE06 source remain numerical; no H1 on-shell/Noether/continuum derivative certificate. No source, operator, tolerances or constraints adjusted.',
         'per_case':[]}
    arrays={}
    with ExitStack() as stack:
        z22=stack.enter_context(np.load(parents['D22A_NPZ'],allow_pickle=False))
        z13=stack.enter_context(np.load(rd/'ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz',allow_pickle=False))
        z27=stack.enter_context(np.load(rd/'ge19_h4f3d27r2_signed_fft_sector_roundoff.npz',allow_pickle=False))
        old=d27.d20.source.old
        r7=old.r7
        bgs,_,mod6,mod7,_,_,_,_,_=old.build_context(rd,z13)
        bg=bgs[(128,'C_star')]; x=np.asarray(bg['x'],float); tag='C_star'
        if not np.array_equal(x,np.asarray(z22['x_primary'],float)):
            raise RuntimeError('D28 original action first-interval grid mismatch')
        H1=np.asarray(z22['D17_H1_action_primary'],complex)
        dH1=np.asarray(z22['D17_H1dot_action_primary'],complex)
        if H1.shape!=(6,6,128) or dH1.shape!=(6,4,128):
            raise RuntimeError('D28 original H1 state shape mismatch')
        old_bg=r7._bg_point; old_cache=r7._CANONICAL_LOCAL_CACHE
        old_ga=r7.assemble_ga_local
        r7._CANONICAL_LOCAL_CACHE={}
        active={'ctx':None}
        def action_bgpoint(b,t):
            if active['ctx'] is None:raise RuntimeError('D28 original action background context absent')
            return active['ctx'](b,t)
        r7._bg_point=action_bgpoint
        collected=[]
        r7.assemble_ga_local=capture_ge06_b_terms(r7,(128,1024),collected)
        try:
            evalH,_=d27.d17driver.d16r1.d15.clk.make_original_action_background(r7,bg,tag)
            ctx=d27.d17core.ActionBackground(r7,bg,evalH)
            active['ctx']=ctx;ctx.knot_check()
            print('GE19_D28_ORIGINAL_GE06_EB_PARTIAL_CAPTURE_BEGIN',flush=True)
            src,sectors=d27.audited_rebuild(r7,d27.r14,mod6,mod7,bg,tag,H1,dH1,nx=1024)
            if len(collected)!=len(r7.BETAS):
                raise RuntimeError('D28 GE06 capture count mismatch')
            # Unmodified exact original D22A source reproduction for each beta.
            for ib,beta in enumerate(r7.BETAS):
                main=np.asarray(z22[f'beta{ib}_H3F_D17_source_rows'],complex)
                con=np.asarray(z22[f'beta{ib}_H3F_D17_source_constraints'],complex)
                if max(relative(src[beta]['rhs'],main),
                       relative(src[beta]['rhs_constraint'],con))>pre['source_replay_limit']:
                    raise RuntimeError('D28 original D22A H3F source replay FAIL')
                eb=collected[ib]['original_ge06_Eb']
                expected=sectors[beta]['real_shift_triplet'][0]
                if not np.array_equal(eb,expected):
                    raise RuntimeError('D28 captured GE06 Eb vs D27 original call FAIL')
                if not np.array_equal(-eb,collected[ib]['minus_b_f']+collected[ib]['plus_dx_b_x']):
                    raise RuntimeError('D28 original signed -b_f+dx(b_x) real-space FAIL')
            print('GE19_D28_ORIGINAL_GE06_EB_AND_D22A_SOURCE_REPLAY_PASS',flush=True)
            for mode,beta in tuple((int(z[0]),float(z[1])) for z in pre['cases']):
                ib=list(r7.BETAS).index(beta)
                name=f'm{mode}_beta{str(beta).replace(".","p")}'
                c=collected[ib]
                ge06=np.asarray(sectors[beta]['GE06_constraint'][0,:,mode],complex)
                orig27=np.asarray(z27[f'{name}_shift_sector_three_by_128'][0],complex)
                if not np.array_equal(ge06,orig27):
                    raise RuntimeError('D28 original D27R2 GE06 selected Fourier source replay FAIL '+name)
                # These FFTs are separate solely for attribution. The original
                # archived GE06 remains authoritative; never replace it by a sum.
                s1=np.fft.fft(c['minus_b_f'],axis=-1)[:,mode]/1024
                s2=np.fft.fft(c['plus_dx_b_x'],axis=-1)[:,mode]/1024
                signed_rem=ge06-s1-s2
                first=np.array([s1[0],s2[0]],complex)
                last=np.array([s1[1],s2[1]],complex)
                delta=last-first
                dg=ge06[1]-ge06[0]
                pd1=d27.pchip_at_first(x,s1)
                pd2=d27.pchip_at_first(x,s2)
                pdg=d27.pchip_at_first(x,ge06)
                row27=rows27.get((mode,beta))
                if row27 is None or abs(pdg-complex(*row27['PCHIP_first_node_shift_source_derivative']['GE06'])) > pre['source_replay_limit']*max(abs(pdg),abs(complex(*row27['PCHIP_first_node_shift_source_derivative']['GE06'])),TINY):
                    raise RuntimeError('D28 D27R2 GE06 derivative replay FAIL '+name)
                row={'mode':mode,'beta':beta,
                     'ge06_first':pair(ge06[0]),'ge06_last':pair(ge06[1]),
                     'ge06_delta':pair(dg),'ge06_first_PCHIP_derivative':pair(pdg),
                     'minus_b_f':{'first':pair(first[0]),'last':pair(last[0]),'delta':pair(delta[0]),'PCHIP_derivative_first':pair(pd1)},
                     'plus_dx_b_x':{'first':pair(first[1]),'last':pair(last[1]),'delta':pair(delta[1]),'PCHIP_derivative_first':pair(pd2)},
                     'signed_independent_FFT_remainder':{'first':pair(signed_rem[0]),'last':pair(signed_rem[1]),'delta':pair(signed_rem[1]-signed_rem[0])},
                     'endpoint_delta_component_norm_ratio_report_only':float((abs(delta[0])+abs(delta[1]))/max(abs(dg),TINY)),
                     'endpoint_delta_minus_b_f_over_GE06_report_only':float(abs(delta[0])/max(abs(dg),TINY)),
                     'endpoint_delta_plus_dx_b_x_over_GE06_report_only':float(abs(delta[1])/max(abs(dg),TINY)),
                     'first_derivative_component_norm_ratio_report_only':float((abs(pd1)+abs(pd2))/max(abs(pdg),TINY)),
                     'signed_delta_reconstruction_relative_report_only':float(abs(dg-delta.sum())/max(abs(dg),abs(delta[0])+abs(delta[1]),TINY)),
                     'notes':'Exact real-space original GE06 assembly verified; separate FFT/PCHIP component derivatives are diagnostic, not action-exact continuum derivatives.'}
                out['per_case'].append(row)
                arrays[f'{name}_original_ge06_shift_source_128']=ge06.copy()
                arrays[f'{name}_minus_b_f_128']=s1.copy()
                arrays[f'{name}_plus_dx_b_x_128']=s2.copy()
                arrays[f'{name}_separate_fft_signed_remainder_128']=signed_rem.copy()
                print(f'GE19_D28_GE06_EB m={mode} beta={beta} '
                      f'ge06_delta={abs(dg):.6e} minus_bf_delta={abs(delta[0]):.6e} '
                      f'plus_dx_bx_delta={abs(delta[1]):.6e} '
                      f'cancellation_ratio={row["endpoint_delta_component_norm_ratio_report_only"]:.6e} '
                      f'fft_remainder_first={abs(signed_rem[0]):.6e}',flush=True)
        finally:
            r7.assemble_ga_local=old_ga
            r7._bg_point=old_bg
            r7._CANONICAL_LOCAL_CACHE=old_cache
    if len(out['per_case'])!=3 or any(not np.isfinite(v).all() for v in arrays.values()):
        raise RuntimeError('D28 expected three finite cases')
    jp.parent.mkdir(parents=True,exist_ok=True)
    np.savez_compressed(zp,**arrays)
    jp.write_text(json.dumps(out,indent=2,sort_keys=True,allow_nan=False)+'\n')
    print('GE19_D28_CLASSIFICATION '+out['classification'],flush=True)

if __name__=='__main__':main()
