#!/usr/bin/env python3
"""GE19 D20: D17/D19R1-dependent five-family numerical source and GE05 Ward subset.

The original M1[Z20,q20] remains a frozen comparator; reusing it in a
six-piece mixed-parent row is explicitly NOT a H4 source reclosure.
No Z21 solve, full Ward, on-shell certificate or observational fitting.
"""
from __future__ import annotations
import argparse,hashlib,json,subprocess
from pathlib import Path
import numpy as np
from ge19 import h4f3d16r1_actual_original_H1dot_Hermite_physical_bath as d16r1
from ge19 import h4f3d19r1_physical_bath_numerical_core as d19core
from ge19 import h4f3d6_actual_normalized_bath_parent_ward as d6
from ge19 import h4f3b_actual_corrected_six_piece_source as source
from ge19 import h4f2g_action_completed_six_piece_source_ledger as ledger
from ge19 import h4f2h_physical_time_source_ward_bridge as clock
ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/'ge19/h4f3d20_predata_dependency_reclosure.json'
TINY=1.e-300

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for c in iter(lambda:f.read(1<<20),b''):h.update(c)
    return h.hexdigest()

def rel(a,b):
    a=np.asarray(a);b=np.asarray(b)
    return float(np.linalg.norm(a-b)/max(np.linalg.norm(a),np.linalg.norm(b),TINY))

def canonical_knots_to_h1(Y,bg,tag,r7,mod6,mod7):
    """Reconstruct original 10-field canonical GE06/GE07 solution, zero H1 RHS."""
    y=np.asarray(Y,complex)
    if y.shape!=(6,8,4*(len(bg['x'])-1)+1):
        raise ValueError('D17 canonical H1 shape/fine-grid changed')
    nt=len(bg['x']);st=np.empty((6,6,nt),complex);dt=np.empty((6,4,nt),complex)
    # Original PCHIP callback is evaluated ONLY at unchanged original knots.
    # Both D17 source-action callback and frozen PCHIP match there.
    op_res=0.
    for it,x in enumerate(bg['x']):
        for im,m in enumerate(r7.FOURIER_N):
            k=float(m*r7.g9.K_REQ[0]/r7.FOURIER_N[0])
            M,F,ZY,ZR,WY,WR,Cmat,bp,diag=r7._canonical_operator_matrices(
                mod6,mod7,bg,tag,k,float(x))
            w=WY@y[im,:,4*it]
            st[im,:,it]=w[[0,2,3,4,5,1]]
            dt[im,:,it]=w[[6,7,8,9]]
            alg=np.vstack((Cmat[0:4],Cmat[5:6],Cmat[12:13]+Cmat[13:14]))
            goal=np.r_[y[im,4:8,4*it],0.,0.]
            op_res=max(op_res,float(np.linalg.norm(alg@w-goal)/max(
                np.linalg.norm(alg@w),np.linalg.norm(goal),TINY)))
    if not all(np.isfinite(q).all() for q in (st,dt)):
        raise RuntimeError('D20 nonfinite source-action reconstructed H1')
    return st,dt,op_res

def actual_m2(ge05,old,bg,h1,z,v,r,w,tau,nx=128,chunk=8):
    """Same frozen GE05 M2 action recipe, with D19R1 physical bath.

    WARNING: the original FD4 temporal derivative in memory_m2_chunk is
    not phase resolved for every quadrature node. Its error is reported,
    not promoted to a source/on-shell certificate.
    """
    grav=old.grav_real_for_memory(bg,h1,old.r7.FOURIER_N,nx)
    nt=len(bg['x']);rm=np.zeros((6,nt,nx),float);rc=np.zeros((2,nt,nx),float)
    for i in range(0,len(r),chunk):
        stop=min(i+chunk,len(r))
        mm,cc=old.memory_m2_chunk(ge05,bg,grav,z[i:stop],v[i:stop],
                                  r[i:stop],w[i:stop],tau,nx)
        rm+=mm;rc+=cc
        if (i//chunk+1)%32==0 or stop==len(r):
            print(f'GE19_D20_M2_CHUNK {stop}/{len(r)}',flush=True)
    out=np.concatenate((-old.GE05_TO_GE06*old.fft_low(rm),
                        -old.GE05_TO_GE06*old.fft_low(rc)),axis=0)
    if out.shape!=(8,nt,old.M_MAX+1) or not np.isfinite(out).all():
        raise RuntimeError('D20 original-action mapped M2 shape/finite failure')
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--results-dir',required=True);ap.add_argument('--repair26-trace',required=True)
    ap.add_argument('--json-out',required=True);ap.add_argument('--npz-out',required=True)
    args=ap.parse_args();rd=Path(args.results_dir).resolve();trace=Path(args.repair26_trace).resolve()
    oj=Path(args.json_out).resolve();on=Path(args.npz_out).resolve()
    if oj.exists() or on.exists():raise RuntimeError('D20 refuses to overwrite')
    pre=json.loads(PRE.read_text())
    if pre['classification']!='GE19_D20_PREDATA_D17_D19R1_FIVE_SOURCE_AND_GE05_WARD_SUBSET':
        raise RuntimeError('D20 preregistration has changed')
    for path,want in pre['local_sha256'].items():
        if sha(ROOT/path)!=want:raise RuntimeError('D20 local source mismatch: '+path)
    for path,want in pre['original_git_blobs'].items():
        head=subprocess.check_output(['git','rev-parse','HEAD:'+path],cwd=ROOT,text=True).strip()
        work=subprocess.check_output(['git','hash-object',str(ROOT/path)],cwd=ROOT,text=True).strip()
        if not(head==work==want):raise RuntimeError('D20 frozen original source changed: '+path)
    for key,(name,want) in pre['actual_parent_sha256'].items():
        if not (rd/name).is_file() or sha(rd/name)!=want:
            raise RuntimeError('D20 actual parent missing/changed: '+key)
    if sha(trace)!=pre['repair26_trace_sha256'] or trace.stat().st_size!=26643162:
        raise RuntimeError('D20 Repair26 full-history trace changed')
    d19report=json.loads((rd/pre['actual_parent_sha256']['D19_JSON'][0]).read_text())
    if not(d19report.get('numerical_tol_pass') is True and
           d19report.get('classification')==
           'GE19_H4F3D19R1_CSTAR_NUMERICAL_BATH_TOLERANCE_PASS_D17_H1_AND_FULL_H4_OPEN' and
           d19report.get('full_original_H4_Ward_certified') is False and
           d19report.get('Z21_certified') is False):
        raise RuntimeError('D20 cannot promote or accept altered D19R1 science claims')
    d17report=json.loads((rd/pre['actual_parent_sha256']['D17_JSON'][0]).read_text())
    if d17report.get('true_continuous_original_H1_X10_error_enclosed') is not False:
        raise RuntimeError('D20 D17 continuous H1 status changed')
    old=source.old;r7=old.r7
    source_code_locks=source.code_lock()
    inputs,cert=source.frozen_inputs(rd,trace)
    if not(np.array_equal(r7.FOURIER_N,d19core.MODES) and old.M_MAX==40):
        raise RuntimeError('D20 original Fourier dictionary mismatch')
    print('GE19_D20_ORIGINAL_SOURCE_D17_D19R1_AND_REPAIR26_SHA_PASS',flush=True)
    out={};controls=[]
    with (np.load(inputs['r13'],allow_pickle=False) as r13,
          np.load(inputs['h3fn'],allow_pickle=False) as h3f,
          np.load(inputs['h3gn'],allow_pickle=False) as h3g,
          np.load(inputs['z11'],allow_pickle=False) as z11,
          np.load(rd/pre['actual_parent_sha256']['D17_NPZ'][0],allow_pickle=False) as d17,
          np.load(rd/pre['actual_parent_sha256']['D19_NPZ'][0],allow_pickle=False) as d19):
        bgs,_,mod6,mod7,ge05,_,_,qdirect,_=old.build_context(rd,r13)
        bg=bgs[(128,'C_star')];x=np.asarray(bg['x'],float)
        if not (np.array_equal(x,np.asarray(h3f['x_primary'],float)) and
                np.array_equal(x,np.asarray(z11['x_primary'],float)) and
                np.array_equal(x,np.asarray(d19['original_x_primary'],float)) and
                np.array_equal(np.asarray(d17['primary_C_star_x_dense_sub4'],float)[::4],x)):
            raise RuntimeError('D20 genuine parent time grids differ')
        h1,dh1,calgres=canonical_knots_to_h1(np.asarray(
            d17['primary_C_star_H1_canonical_y_dense_sub4'],complex),bg,'C_star',r7,mod6,mod7)
        X=old.r24.first_order_X_modes(r7,bg,h1)
        Xref=np.asarray(d17['primary_C_star_X10_original_action_dense_sub4'],complex)[:,::4]
        Xdiff=rel(X,Xref)
        if Xdiff>1e-9 or calgres>1e-9:
            raise RuntimeError('D20 D17 reconstructed H1 not its actual action drive')
        # We DO NOT replace certified H3F Z20, H3G q20, or Z11 with this
        # independent numerically converged D17 reconstruction.
        frozen_h1=np.asarray(h3f['C_star_H1_primary'],complex)
        parent_h1_delta=rel(h1,frozen_h1)
        tangent=np.asarray(z11['C_star_Z11_primary'],complex)
        tangentdot=np.asarray(z11['C_star_Z11dot_primary'],complex)
        z=np.asarray(d19['physical_Cstar_Nt128_Nq2048_z_sub256'],complex)
        v=np.asarray(d19['physical_Cstar_Nt128_Nq2048_v_sub256'],complex)
        if z.shape!=(2048,6,128) or v.shape!=z.shape:
            raise RuntimeError('D20 D19R1 entire node bath missing')
        mask=np.asarray(d19['original_action_phase_mask_at_orig_intervals'],bool)
        highphase=int(np.sum(mask))
        if mask.shape!=(2048,127) or highphase!=int(d19report['original_high_phase_node_step_count']):
            raise RuntimeError('D20 D19R1 original-action high-phase scope changed')
        # Original quadrature exactly matches D19's independent Gauss nodes.
        r,w=old.c4.tan_gl_nodes(2048);r=np.asarray(r,float);w=np.asarray(w,float)
        tau=old.r24.TAUH0/float(r7.g9.H0_CLASS)
        wz=np.einsum('j,jmt->mt',w,z,optimize=True)
        wv=np.einsum('j,jmt->mt',w,v,optimize=True)
        bath_wz_rel=rel(wz,np.asarray(d19['sub256_weighted_z'],complex))
        bath_wv_rel=rel(wv,np.asarray(d19['sub256_weighted_v'],complex))
        if max(bath_wz_rel,bath_wv_rel)>1e-11:
            raise RuntimeError('D20 D19R1 full bath vs weighted archive mismatch')
        print('GE19_D20_D17_CANONICAL_AND_D19_BATH_RECONSTRUCTION_PASS',flush=True)
        # Original normalized GE05 Euler current is evaluated with FD4 at
        # the 128 original knots, explicitly as an UNRESOLVED high-phase test.
        kfund=float(r7.g9.K_REQ[0]/r7.FOURIER_N[0])
        wbath,ediag=d6.physical_bath_ward(z,v,X,bg['a'],bg['H'],x,r,w,tau,kfund)
        out['GE05_bath_original_knot_FD4_ward_subset_REPORT_ONLY']=wbath
        out['D19_GE05_bath_sampled_W_sub256_REPORT_ONLY']=np.asarray(
            d19['sub256_sampled_signed_GE05_W_D17_surrogate'],complex)
        out['D19_GE05_bath_sampled_W_unsigned_envelope_sub256']=np.asarray(
            d19['sub256_sampled_unsigned_GE05_W_envelope_D17_surrogate'],float)
        out['x_primary']=x
        # Recompute four D17-H1-dependent source families. Z11 stays frozen:
        # therefore these are a provenance-explicit conditional reclosure.
        gm,gc,dm,dc=old.q_cross_direct(qdirect,bg,'C_star',h1,dh1,tangent,tangentdot,128)
        sg,sc,sd,st=old.q_cross_direct(qdirect,bg,'C_star',tangent,tangentdot,h1,dh1,128)
        cross_swap=max(rel(gm,sg),rel(gc,sc),rel(dm,sd),rel(dc,st))
        lm,lc,lam_exact,lam_pol,lam_swap=old.lambda_cross_direct(bg,h1,dh1,tangent,tangentdot,128)
        piece={
            ledger.PIECES[0]:np.concatenate((-2*old.fft_low(gm),-2*old.fft_low(gc)),axis=0),
            ledger.PIECES[1]:np.concatenate((-2*old.fft_low(dm),-2*old.fft_low(dc)),axis=0),
            ledger.PIECES[2]:np.concatenate((-2*old.fft_low(lm),-2*old.fft_low(lc)),axis=0),
        }
        print('GE19_D20_GE06_GE07_LAMBDA_D17_CONDITIONAL_CROSS_DONE',flush=True)
        # Recompute original GE05 M2 with complete D19R1 on original knots.
        # Original FD4 differentiated M2 current is an explicit unresolved
        # temporal-aliasing limitation in high-phase bath nodes.
        piece[ledger.PIECES[5]]=actual_m2(ge05,old,bg,h1,z,v,r,w,tau,nx=128,chunk=8)
        print('GE19_D20_ORIGINAL_GE05_M2_D19_BATH_RECOMPUTED_REPORT_ONLY',flush=True)
        first,_,firstx=r7.reduced_state_real(bg,h1,old.NX_DY_PRIMARY,dh1)
        z11real,_,z11x=r7.reduced_state_real(bg,tangent,old.NX_DY_PRIMARY,tangentdot)
        # Only old H3G B20 is available. Never call a six-piece combination
        # with the old M1 a new on-shell source. Its provenance is explicit.
        old_B20=np.asarray(h3g['C_star_B20_linear_primary'],complex)
        stale_M1,stale_M1c=old.m1_mapped_fourier(bg,old_B20)
        if stale_M1.shape!=(3,6,128,41) or stale_M1c.shape!=(3,2,128,41):
            raise RuntimeError('D20 frozen H3G M1 shape changed')
        legacy_path=rd/'ge19_h4f3b_actual_corrected_six_piece_source.npz'
        legacy_m2_delta={}
        if legacy_path.exists():
            if sha(legacy_path)!=d6.SOURCE_NPZ_SHA:
                raise RuntimeError('D20 optional original H4F3b comparison archive SHA changed')
            with np.load(legacy_path,allow_pickle=False) as legacy:
                for ib,_ in enumerate(r7.BETAS):
                    old_m2=np.asarray(legacy[
                        f'primary_C_star_beta{ib}_{ledger.PIECES[5]}_rows'],complex)
                    legacy_m2_delta[str(ib)]=rel(piece[ledger.PIECES[5]],old_m2)
            print('GE19_D20_FROZEN_H4F3B_ORIGINAL_M2_COMPARISON_DONE',flush=True)
        else:
            print('GE19_D20_OPTIONAL_ORIGINAL_H4F3B_SOURCE_NOT_FOUND_COMPARISON_OPEN',flush=True)
        for ib,beta in enumerate(r7.BETAS):
            ext={k:(piece[k][:6],piece[k][6:]) for k in piece}
            old_m1=np.concatenate((stale_M1[ib],stale_M1c[ib]),axis=0)
            ext[ledger.PIECES[4]]=(old_m1[:6],old_m1[6:])
            assembled=ledger.assemble_six(ext,bg['a'],bg['Q_action'],
                first['u20'],firstx['phi20'],z11real['u20'],z11x['phi20'],
                r7.KB,r7.A0_MPC_INV,float(beta),kfund,x,mmax=40)
            proper=clock.physical_six_piece_ward(assembled['piece_rows'],x,bg['a'],bg['H'],kfund)
            prefix=f'Cstar_beta{ib}_'
            for name in ledger.PIECES:
                arr=np.asarray(assembled['piece_rows'][name],complex)
                out[prefix+name+'_rows_M1_FROZEN_UNRECLOSED']=arr
                out[prefix+name+'_source_ward_M1_FROZEN_UNRECLOSED']=proper['per_piece'][name]
            out[prefix+'mixed_parent_total_rows_NOT_H4_SOURCE']=assembled['total_rows']
            out[prefix+'mixed_parent_source_ward_NOT_FULL_WARD']=proper['total_source_ward']
            controls.append({'beta':float(beta),
                'sum_six_mixed_provenance_rows_max_abs':float(np.max(np.abs(
                    assembled['total_rows']-sum(assembled['piece_rows'].values())))),
                'six_mixed_ward_linearity_max_abs':float(np.max(np.abs(
                    proper['total_source_ward']-sum(proper['per_piece'].values())))),
                'all_finite':bool(np.isfinite(assembled['total_rows']).all()
                                 and np.isfinite(proper['total_source_ward']).all())})
            print(f'GE19_D20_BETA_{ib}_MIXED_PROVENANCE_SOURCE_LEDGER_DONE_NOT_FULL_WARD',flush=True)
        # Guard scientific scope in machine-readable fields.
        gates={'immutable_D17_D19R1_and_source_SHA':True,
            'reconstructed_D17_canonical_source_H1':Xdiff<=1e-9 and calgres<=1e-9,
            'complete_D19R1_bath_weighted_replay':max(bath_wz_rel,bath_wv_rel)<=1e-11,
            'GE06_GE07_bilinear_swap_check':cross_swap<=1e-10,
            'original_Lambda_cross_identity':lam_exact<=1e-10 and lam_swap<=1e-10,
            'new_M2_and_all_source_families_finite':all(np.isfinite(q).all() for q in piece.values()),
            'mixed_provenance_Ward_assembly_linear':all(q['all_finite'] and
                q['six_mixed_ward_linearity_max_abs']<=1e-9 for q in controls)}
        passed=all(gates.values())
        rep={'classification':('GE19_D20_D17_D19R1_FIVE_SOURCE_DEPENDENCY_DIAGNOSTIC_PASS_FULL_H4_OPEN'
             if passed else 'GE19_D20_FIVE_SOURCE_DEPENDENCY_DIAGNOSTIC_FAIL_FULL_H4_OPEN'),
             'preregistration':pre['classification'],
             'parent_sha256':{key:sha(rd/name) for key,(name,_) in pre['actual_parent_sha256'].items()},
             'source_sha256':{key:sha(ROOT/key) for key in pre['local_sha256']},
             'original_parent_source_locks':cert,
             'original_H4F3b_code_locks':source_code_locks,'gates':gates,
             'reconstructed_action_H1_X10_vs_D17_rel':Xdiff,
             'reconstructed_action_H1_canonical_scaled_algebraic_residual_max':calgres,
             'D17_H1_vs_frozen_H3F_relative':parent_h1_delta,
             'D19_full_bath_weighted_z_vs_archive_relative':bath_wz_rel,
             'D19_full_bath_weighted_v_vs_archive_relative':bath_wv_rel,
             'D19_original_high_phase_node_interval_count':highphase,
             'GE05_bath_original_knot_FD4_Euler_report_only':ediag,
             'GE05_bath_original_knot_FD4_Ward_L2_report_only':float(np.linalg.norm(wbath)),
             'GE05_D19_sampled_signed_W_L2_report_only':float(np.linalg.norm(
                 out['D19_GE05_bath_sampled_W_sub256_REPORT_ONLY'])),
             'GE06_GE07_cross_swap_relative_max':cross_swap,
             'Lambda_exact_relative':lam_exact,'Lambda_swap_relative':lam_swap,
             'beta_controls':controls,
             'frozen_H4F3b_old_M2_vs_D17_D19R1_M2_relative_report_only':legacy_m2_delta,
             'optional_frozen_H4F3b_archive_comparison_present':legacy_path.exists(),
             'D19_bath_coupled_M2_recomputed':True,
             'D17_H1_coupled_GE06_GE07_Lambda_DY2_recomputed':True,
             'M1_uses_FROZEN_H3G_B20_not_new_q20':True,
             'GE05_M2_FD4_high_phase_temporal_aliasing_closed':False,
             'new_physical_q20_and_Z11_recomputed':False,
             'original_all_parent_nonbath_Euler_boundary_ward_evaluated':False,
             'full_original_H4_Ward_certified':False,'Z21_certified':False,
             'lensing_licensed':False,'no_observation_tuning':True,
             'frozen_Repair37_SCIENCE_FAIL_immutable':True,
             'claim_boundary':'Five D17/D19R1-dependent source families (GE06, GE07, Lambda, DY2, GE05 M2) are numerically regenerated using the frozen Z11. Frozen H3G B20/M1 is included solely in labeled mixed-provenance ledger. FD4 M2 high-phase temporal error, q20/Z11 physical reclosure, all nonbath Euler and boundary parent terms, linear H4 operator Ward and Z21 are NOT closed. Original-knot GE05 FD4 and D19 sample Ward are not interchangeable.'}
        oj.parent.mkdir(parents=True,exist_ok=True);on.parent.mkdir(parents=True,exist_ok=True)
        oj.write_text(json.dumps(rep,indent=2,sort_keys=True,allow_nan=False)+'\n')
        np.savez_compressed(on,**out)
        print('GE19_D20_FIVE_DEPENDENT_SOURCE_DIAGNOSTIC_PASS='+str(passed),flush=True)
        print(json.dumps({'classification':rep['classification'],'gates':gates,
                          'D17_H1_vs_H3F_relative':parent_h1_delta,
                          'M1_new_q20_closed':False,'full_original_H4_Ward_certified':False},
                         indent=2,sort_keys=True),flush=True)
        if not passed:raise SystemExit(2)

if __name__=='__main__':main()
