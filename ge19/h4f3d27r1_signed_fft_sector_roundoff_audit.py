#!/usr/bin/env python3
"""D27R1: finite-precision provenance of original GE06/GE07 shift sources.

No new H3 solve, no source adjustment, no certification. Recompute the frozen
original H3F source *only* to separate its original GE06/GE07 constraint terms.
Reproduce D22A/D26 exactly; preserve original D27 per-mode FAIL explicitly.
"""
from __future__ import annotations
import argparse, hashlib, json
from contextlib import ExitStack
from pathlib import Path
import numpy as np
from scipy.interpolate import PchipInterpolator
from ge19 import h4f3d26_action_shift_source_transport_ledger as d26
from ge19 import h4f3d25r1_first_interval_shift_substep_decision as d25
from ge19 import h4f3d20r1_recompute_five_sources_and_bath_ward as d20
from ge19 import h4f3d17_actual_original_action_dense_canonical_H1 as d17driver
from ge19 import h4f3d17_original_action_dense_H1_core as d17core
from ge19 import h3f_corrected_y_source_adapter as h3f
from ge19 import repair14_self_consistent_reduced_h3_z20_particular as r14

ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/'ge19/h4f3d27r1_signed_fft_sector_roundoff_prereg.json'
LOCK=ROOT/'ge19/h4f3d27r1_signed_fft_sector_roundoff_lock.json'
CASES=((14,0.1),(1,1.0),(40,0.1))
EPS=1e-300


def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for block in iter(lambda:f.read(1<<20),b''):h.update(block)
    return h.hexdigest()


def complex_pair(x):
    c=complex(x)
    return [float(c.real),float(c.imag)]


def relative(a,b):
    a=np.asarray(a,complex);b=np.asarray(b,complex)
    return float(np.linalg.norm(a-b)/max(np.linalg.norm(a),np.linalg.norm(b),EPS))


def pchip_at_first(x,y):
    """Exactly Repair07's separate real/imag PCHIP at first coarse knot."""
    a=np.asarray(y,complex)
    re=PchipInterpolator(x,a.real,extrapolate=False)
    im=PchipInterpolator(x,a.imag,extrapolate=False)
    return complex(re.derivative()(x[0])+1j*im.derivative()(x[0]))


def check_triplet(total,ga,matter,threshold=1e-11):
    """Signed original-action GE06 + GE07 decomposition, no fitted correction."""
    err=relative(total,np.asarray(ga)+np.asarray(matter))
    if not np.isfinite(err) or err>threshold:raise RuntimeError(f'D27 original source sector triplet FAIL {err}')
    return err


def check_original_real_shift(total,ga,matter):
    """Original Eb=GE06[b]+GE07[b] must hold in real space exactly.

    This checks the original assembler at full real-space resolution, before
    independently transformed sector FFTs can lose distributivity in tiny modes.
    It is not a replacement for the archived relative Fourier-sector FAIL.
    """
    t=np.asarray(total);g=np.asarray(ga);m=np.asarray(matter)
    if t.shape!=g.shape or t.shape!=m.shape or not all(np.isfinite(z).all() for z in (t,g,m)):
        raise RuntimeError('D27R1 real shift sector shape/nonfinite FAIL')
    if not np.array_equal(t,g+m):
        raise RuntimeError('D27R1 original real-space Eb=GE06+GE07 FAIL')
    return True


def audited_rebuild(r7,r14,mod6,mod7,bg,tag,H1,dh1,nx=1024):
    """Capture original main_and_constraints calls: total, GE06-only, GE07-only.

    The original Repair07 implementation makes exactly these three calls per
    beta. This wrapper changes no return value or source operation.
    """
    captured=[];original=r7.main_and_constraints
    def capture(ga,matter):
        main,con=original(ga,matter)
        main=np.asarray(main);con=np.asarray(con)
        if main.shape!=(6,len(bg['x']),nx) or con.shape!=(2,len(bg['x']),nx):
            raise RuntimeError('D27 original GE06/GE07 assembly unexpected shape')
        if not (np.isfinite(main).all() and np.isfinite(con).all()):
            raise RuntimeError('D27 original GE06/GE07 assembly nonfinite')
        raw_shift=np.asarray(con[0])
        if np.iscomplexobj(raw_shift) and np.any(raw_shift.imag!=0):
            raise RuntimeError('D27R1 unexpected imaginary original real-space shift source')
        captured.append((np.asarray(np.fft.fft(main,axis=-1)[:,:,:41]/nx,complex),
                         np.asarray(np.fft.fft(con,axis=-1)[:,:,:41]/nx,complex),
                         np.asarray(raw_shift.real,float).copy()))
        return main,con
    r7.main_and_constraints=capture
    try:
        sources=h3f.source_bundle_reduced_lambda(r7,r14,mod6,mod7,bg,
            np.asarray(bg['rho_lambda_action'],float),tag,nx,H1,dh1)
    finally:
        r7.main_and_constraints=original
    if len(captured)!=3*len(r7.BETAS):
        raise RuntimeError(f'D27 original source assembly call count {len(captured)} != 9')
    sectors={}
    for ib,beta in enumerate(r7.BETAS):
        full,ga,ma=captured[3*ib:3*ib+3]
        for part in (0,1):check_triplet(full[part],ga[part],ma[part])
        check_original_real_shift(full[2],ga[2],ma[2])
        src=sources[beta]
        if relative(-full[1],src['rhs_constraint'])>1e-11:
            raise RuntimeError('D27 signed H3F original full constraint does not replay')
        if relative(-ga[0],src['Q_ga'])>1e-11 or relative(-ma[0],src['Q_matter'])>1e-11:
            raise RuntimeError('D27 original H3F GE06/GE07 main sector dictionary mismatch')
        if relative(src['rhs'],src['Q_ga']+src['Q_matter']+src['Q_lambda']+src['Y_H3'])>1e-11:
            raise RuntimeError('D27 original H3F main source dictionary mismatch')
        sectors[beta]={
            'GE06_main':-ga[0], 'GE06_constraint':-ga[1],
            'GE07_main':-ma[0], 'GE07_constraint':-ma[1],
            'real_shift_triplet':np.stack((ga[2],ma[2],full[2])),
        }
    return sources,sectors


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--results-dir',required=True)
    ap.add_argument('--json-out',required=True)
    ap.add_argument('--npz-out',required=True)
    a=ap.parse_args();rd=Path(a.results_dir).resolve();jp=Path(a.json_out).resolve();npz=Path(a.npz_out).resolve()
    if jp.exists() or npz.exists():raise RuntimeError('D27 no-overwrite results')
    pre=json.loads(PRE.read_text());lock=json.loads(LOCK.read_text())
    if pre['classification']!='GE19_D27R1_PREEXEC_ORIGINAL_SHIFT_REAL_SPACE_AND_FFT_SPLIT_AUDIT':
        raise RuntimeError('D27 prereg changed')
    for path,want in lock['sha256_local_files'].items():
        if sha(ROOT/path)!=want:raise RuntimeError('D27 code/prereg lock mismatch '+path)
    parents,_=d26.checked_source_files(rd)
    for key,spec in pre['frozen_D26_outputs'].items():
        p=rd/spec['filename']
        if not p.is_file() or sha(p)!=spec['sha256']:
            raise RuntimeError('D27 D26 source archive SHA mismatch '+key)
        parents[key]=p
    print('GE19_D27_ACTION_AND_ALL_FROZEN_D26_PARENT_LOCK_PASS',flush=True)
    report={'classification':'GE19_D27R1_FROZEN_H3F_SIGNED_FFT_SPLIT_DIAGNOSTIC_COMPLETE_PARENTS_UNCERTIFIED',
        'preregistration':pre['classification'],'source_sha256':sha(Path(__file__)),
        'all_input_sha256':{k:sha(v) for k,v in parents.items()},
        'scope':'Frozen Cstar Nt128 original H3F GE06/GE07 sources; exact real-space shift source split, separately transformed signed FFT remainder and PCHIP decomposition on three existing D26 modes. No H3 solve.',
        'D22A_science_FAIL_immutable':True,'D25_original_replay_FAIL_immutable':True,
        'D27_original_selected_triplet_FAIL_immutable':True,
        'D25R1_D26_diagnostic_only':True,'original_action_modified':False,
        'source_modified':False,'boundary_modified':False,'solver_rerun':False,
        'Z11_certified':False,'Z20_certified':False,'q20_B20_recomputed':False,
        'full_H4_Ward_certified':False,'Z21_certified':False,'lensing_licensed':False,
        'no_observational_tuning':True,
        'claim_boundary':'Original D27 per-mode relative Fourier triplet failure is preserved. Full real-space original-action shift identity is independently checked before signed finite FFT arithmetic remainder is recorded without using it to alter any original source, solver, threshold or physical gate. The derivative of that remainder is separated from PCHIP non-additivity. No continuum H1 source derivative, Noether or GE05 on-shell certification, no H3/q20/H4/Z21/lensing.',
        'per_case':[],'original_D27_triplet_gate_failed_for_any_case':False}
    arrays={}
    with ExitStack() as es:
        z22=es.enter_context(np.load(parents['D22A_NPZ'],allow_pickle=False))
        z13=es.enter_context(np.load(rd/'ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz',allow_pickle=False))
        zd25=es.enter_context(np.load(parents['D25R1_NPZ'],allow_pickle=False))
        d26j=json.loads(parents['D26_JSON'].read_text())
        old=d20.source.old;r7=old.r7
        bgs,_,mod6,mod7,_,_,_,_,_=old.build_context(rd,z13)
        bg=bgs[(128,'C_star')];tag='C_star';x=np.asarray(bg['x'],float)
        if not np.array_equal(x,np.asarray(z22['x_primary'],float)):
            raise RuntimeError('D27 original coarse clock mismatch')
        H1=np.asarray(z22['D17_H1_action_primary'],complex)
        dh1=np.asarray(z22['D17_H1dot_action_primary'],complex)
        if H1.shape!=(6,6,128) or dh1.shape!=(6,4,128):
            raise RuntimeError('D27 original H1 parent shape mismatch')
        old_bg=r7._bg_point;old_cache=r7._CANONICAL_LOCAL_CACHE;r7._CANONICAL_LOCAL_CACHE={}
        active={'ctx':None}
        def action_bgpoint(b,t):
            if active['ctx'] is None:raise RuntimeError('D27 original action context unavailable')
            return active['ctx'](b,t)
        r7._bg_point=action_bgpoint
        try:
            evalH,_=d17driver.d16r1.d15.clk.make_original_action_background(r7,bg,tag)
            ctx=d17core.ActionBackground(r7,bg,evalH);active['ctx']=ctx;ctx.knot_check()
            print('GE19_D27_ORIGINAL_ACTION_GE06_GE07_SOURCE_REBUILD_BEGIN',flush=True)
            src,sectors=audited_rebuild(r7,r14,mod6,mod7,bg,tag,H1,dh1,nx=1024)
            replay=[]
            for ib,beta in enumerate(r7.BETAS):
                main=np.asarray(z22[f'beta{ib}_H3F_D17_source_rows'],complex)
                con=np.asarray(z22[f'beta{ib}_H3F_D17_source_constraints'],complex)
                em=relative(src[beta]['rhs'],main);ec=relative(src[beta]['rhs_constraint'],con)
                replay.append((em,ec))
                if max(em,ec)>1e-11:raise RuntimeError(f'D27 original D22A source replay FAIL beta={beta} main={em} con={ec}')
            print('GE19_D27_ORIGINAL_D22A_H3F_SOURCE_REPLAY_PASS',flush=True)
            report['original_D22A_full_source_replay_relative_max']=float(max(v for pair in replay for v in pair))
            for m,beta in CASES:
                s=src[beta];q=sectors[beta]
                name=f'm{m}_beta{str(beta).replace(".","p")}'
                refrows=[v for v in d26j['per_case'] if v['mode']==m and v['beta']==beta]
                if len(refrows)!=1:raise RuntimeError('D27 D26 case ambiguous')
                d26row=refrows[0]
                sg=np.asarray(q['GE06_constraint'][0,:,m],complex)
                sm=np.asarray(q['GE07_constraint'][0,:,m],complex)
                st=np.asarray(s['rhs_constraint'][0,:,m],complex)
                # Preserve the exact original D27 local relative gate as report-only.
                # Its failure is NOT turned into a PASS by increasing tolerance.
                err=relative(st,sg+sm)
                original_gate_pass=bool(err<=pre['original_D27_local_relative_limit'])
                report['original_D27_triplet_gate_failed_for_any_case'] |= not original_gate_pass
                signed_fft_remainder=st-sg-sm
                real3=np.asarray(q['real_shift_triplet'],float)
                if not check_original_real_shift(real3[2],real3[0],real3[1]):
                    raise RuntimeError('D27R1 independent original real shift replay FAIL')
                gp=pchip_at_first(x,sg);mp=pchip_at_first(x,sm);tp=pchip_at_first(x,st)
                rp=pchip_at_first(x,signed_fft_remainder)
                d26p=complex(*d26row['first_node_source_shift_time_derivative_pchip'])
                if relative(np.array([tp]),np.array([d26p]))>1e-11:
                    raise RuntimeError('D27 D26 aggregate PCHIP derivative replay FAIL')
                delta=st[1]-st[0];dga=sg[1]-sg[0];dma=sm[1]-sm[0]
                # Original D27 demanded relative FFT distributivity in each tiny
                # selected mode; retain its mismatch as a measured signed defect.
                # No selected-mode physical shift gate is relaxed or evaluated here.
                delta_fft_remainder=signed_fft_remainder[1]-signed_fft_remainder[0]
                ib=list(r7.BETAS).index(beta);k=float(m*r7.g9.K_REQ[0]/r7.FOURIER_N[0])
                ky,ks,M,F=d26.operator(r7,mod6,mod7,bg,tag,k,float(x[0]))
                y0=np.asarray(zd25[f'{name}_y0'],complex)
                pieces={
                    'GE06':np.r_[q['GE06_main'][:,0,m],q['GE06_constraint'][:,0,m]],
                    'GE07':np.r_[q['GE07_main'][:,0,m],q['GE07_constraint'][:,0,m]],
                    'Lambda':np.r_[s['Q_lambda'][:,0,m],np.zeros(2,complex)],
                    'StageE_Y':np.r_[s['Y_H3'][:,0,m],np.zeros(2,complex)],
                }
                s0=np.r_[s['rhs'][:,0,m],s['rhs_constraint'][:,0,m]]
                ssum=sum(pieces.values(),np.zeros(8,complex))
                original_main_constraint_split_relative=relative(s0,ssum)
                # Arithmetic remainder of SEPARATELY transformed sector arrays.
                # Diagnostic ledger only: the original archived s0 remains the
                # sole input for D26 and no H3 equation or source is modified.
                pieces['Fourier_split_remainder_report_only']=s0-ssum
                forcing={key:complex(ky@(F@val)) for key,val in pieces.items()}
                hom=complex(ky@(M@y0));all_can=hom+sum(forcing.values())
                d26can=complex(*d26row['first_node_derivative'][1]['terms']['canonical_evolution'])
                if abs(all_can-d26can)>1e-11*max(abs(all_can),abs(d26can),abs(hom),sum(map(abs,forcing.values())),EPS):
                    raise RuntimeError('D27 D26 original canonical source forcing replay FAIL')
                residual=tp-gp-mp
                pchip_only_nonadditivity=residual-rp
                ratio=float(abs(residual)/max(abs(tp),abs(gp),abs(mp),EPS))
                n0=float(np.sum(np.abs(real3[0,0])+np.abs(real3[1,0]))/nx)
                n1=float(np.sum(np.abs(real3[0,1])+np.abs(real3[1,1]))/nx)
                row={'mode':m,'beta':beta,
                    'original_D27_selected_triplet_relative':err,
                    'original_D27_selected_triplet_gate_pass':original_gate_pass,
                    'original_D27_selected_triplet_limit_unchanged':pre['original_D27_local_relative_limit'],
                    'original_real_space_shift_split_exact_all_128x1024':True,
                    'shift_source_fft_signed_remainder':{
                        'first':complex_pair(signed_fft_remainder[0]),
                        'last':complex_pair(signed_fft_remainder[1]),
                        'delta':complex_pair(delta_fft_remainder),
                        'first_absolute':float(abs(signed_fft_remainder[0])),
                        'last_absolute':float(abs(signed_fft_remainder[1])),
                        'first_over_real_space_sector_l1_bound_report_only':float(abs(signed_fft_remainder[0])/max(n0,EPS)),
                        'last_over_real_space_sector_l1_bound_report_only':float(abs(signed_fft_remainder[1])/max(n1,EPS))},
                    'first_interval_source_shift':{'GE06_first':complex_pair(sg[0]),'GE07_first':complex_pair(sm[0]),'total_first':complex_pair(st[0]),
                        'GE06_last':complex_pair(sg[1]),'GE07_last':complex_pair(sm[1]),'total_last':complex_pair(st[1]),
                        'GE06_delta':complex_pair(dga),'GE07_delta':complex_pair(dma),'total_delta':complex_pair(delta),
                        'delta_sector_cancellation_ratio':float((abs(dga)+abs(dma))/max(abs(delta),EPS)),
                        'FFT_split_remainder_delta':complex_pair(delta_fft_remainder)},
                    'PCHIP_first_node_shift_source_derivative':{'GE06':complex_pair(gp),'GE07':complex_pair(mp),'aggregate_original_D26':complex_pair(tp),
                        'sum_sector_derivatives':complex_pair(gp+mp),
                        'signed_FFT_remainder_derivative':complex_pair(rp),
                        'aggregate_minus_sum_sector_derivatives':complex_pair(residual),
                        'PCHIP_only_after_FFT_remainder_derivative':complex_pair(pchip_only_nonadditivity),
                        'combined_non_additivity_relative_report_only':ratio},
                    'canonical_first_node_evolution_signed':{'homogeneous':complex_pair(hom),
                        'GE06_forcing':complex_pair(forcing['GE06']),'GE07_forcing':complex_pair(forcing['GE07']),
                        'Lambda_forcing':complex_pair(forcing['Lambda']),'StageE_Y_forcing':complex_pair(forcing['StageE_Y']),
                        'FFT_split_remainder_forcing_report_only':complex_pair(forcing['Fourier_split_remainder_report_only']),
                        'original_main_constraint_split_relative':original_main_constraint_split_relative,
                        'total_replays_D26':complex_pair(all_can)},
                    'note':'Original selected-mode D27 failure is not a physical PASS. Real-space GE06+GE07 shift assembly is exact. Separately evaluated Fourier transforms and PCHIP can be nonadditive at a tiny selected mode. Signed FFT remainder is reported, not fitted or inserted into a physical solve.'}
                report['per_case'].append(row)
                arrays[f'{name}_shift_sector_three_by_128']=np.stack((sg,sm,st))
                arrays[f'{name}_original_main_source_at_first_node_five_by_8']=np.stack(tuple(pieces.values()))
                arrays[f'{name}_real_shift_triplet_first_last_3_by_2_by_1024']=real3[:,0:2,:].copy()
                arrays[f'{name}_signed_fft_shift_remainder_128']=signed_fft_remainder.copy()
                print(f'GE19_D27_SECTOR m={m} beta={beta} '
                      f'delta_GE06={abs(dga):.6e} delta_GE07={abs(dma):.6e} '
                      f'delta_total={abs(delta):.6e} '
                      f'original_D27_relative={err:.6e} original_gate_pass={original_gate_pass} '
                      f'FFT_remainder_first_abs={abs(signed_fft_remainder[0]):.6e} '
                      f'PCHIP_only_abs={abs(pchip_only_nonadditivity):.6e}',flush=True)
        finally:
            r7._bg_point=old_bg;r7._CANONICAL_LOCAL_CACHE=old_cache
    if len(report['per_case'])!=3 or not all(np.isfinite(a).all() for a in arrays.values()):
        raise RuntimeError('D27 finite/three-mode output failure')
    jp.parent.mkdir(parents=True,exist_ok=True)
    np.savez_compressed(npz,**arrays)
    jp.write_text(json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+'\n')
    print('GE19_D27_CLASSIFICATION '+report['classification'],flush=True)

if __name__=='__main__':main()
