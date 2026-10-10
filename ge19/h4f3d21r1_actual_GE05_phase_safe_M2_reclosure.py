#!/usr/bin/env python3
"""D21: original GE05 M2 scalar-current analytic-time repair on actual D20R1.

This recalculates ONLY the derivative of the original f_c2['pt'] scalar
current, using the exact original action c2 identity and physical H1/bath
first-order jets. It does not alter non-scalar M2, the GE06/07/Lambda/Y
sources, GE05 action, original certified parents, or frozen D20R1 outputs.
The old H3G q20/M1 and Z11 are still not reclosed under D17/D19R1;
therefore no full six-source, full Ward, Z21 or lensing certification.
"""
from __future__ import annotations
import argparse,hashlib,json,subprocess
from pathlib import Path
import numpy as np
from ge19 import h4f3d21_GE05_phase_safe_M2_core as core
from ge19 import h4f3d20r1_recompute_five_sources_and_bath_ward as d20
from ge19 import h4f2g_action_completed_six_piece_source_ledger as ledger
from ge19 import h4f2h_physical_time_source_ward_bridge as clock

ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/'ge19/h4f3d21r1_predata_undefined_proper_repair.json'
TINY=1.e-300

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as s:
        for c in iter(lambda:s.read(1<<20),b''):h.update(c)
    return h.hexdigest()

def exact_locks(rd,trace,pre):
    for rel,want in pre['original_git_blobs'].items():
        head=subprocess.check_output(['git','rev-parse','HEAD:'+rel],cwd=ROOT,text=True).strip()
        work=subprocess.check_output(['git','hash-object',str(ROOT/rel)],cwd=ROOT,text=True).strip()
        if head!=want or work!=want:
            raise RuntimeError('D21 original action/frozen source was changed: '+rel)
    for rel,want in pre['source_sha256'].items():
        if sha(ROOT/rel)!=want:raise RuntimeError('D21 new source differs from preregistration: '+rel)
    for rel,want in pre['required_existing_local_sources'].items():
        if sha(ROOT/rel)!=want:raise RuntimeError('D21 existing D20R1 source changed: '+rel)
    for tag,(filename,want) in pre['parent_results_sha256'].items():
        f=rd/filename
        if not f.is_file() or sha(f)!=want:
            raise RuntimeError('D21 actual frozen parent missing or changed: '+tag)
    if not trace.is_file() or sha(trace)!=pre['Repair26_R1_trace_SHA256'] or trace.stat().st_size!=26643162:
        raise RuntimeError('D21 Repair26 original full-history trace changed')
    return {tag:filename for tag,(filename,_) in pre['parent_results_sha256'].items()}

def kahan_add(acc,comp,chunk):
    z=np.asarray(chunk,float)-comp
    nxt=acc+z
    comp[:]=(nxt-acc)-z
    acc[:]=nxt

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--results-dir',required=True)
    ap.add_argument('--repair26-trace',required=True)
    ap.add_argument('--json-out',required=True)
    ap.add_argument('--npz-out',required=True)
    args=ap.parse_args()
    rd=Path(args.results_dir).resolve();trace=Path(args.repair26_trace).resolve()
    oj=Path(args.json_out).resolve();on=Path(args.npz_out).resolve()
    if oj.exists() or on.exists():raise RuntimeError('D21 refuses to overwrite any result')
    pre=json.loads(PRE.read_text())
    if pre['classification']!='GE19_H4F3D21R1_PREDATA_UNDEFINED_PROPER_IMPLEMENTATION_REPAIR':
        raise RuntimeError('D21 preregistered science boundary changed')
    files=exact_locks(rd,trace,pre)
    d20report=json.loads((rd/files['D20_JSON']).read_text())
    d19report=json.loads((rd/files['D19_JSON']).read_text())
    if not(d20report.get('classification')==
           'GE19_D20R1_D17_D19R1_FIVE_SOURCE_DEPENDENCY_DIAGNOSTIC_PASS_FULL_H4_OPEN' and
           all(d20report.get('gates',{}).values()) and
           d20report.get('GE05_M2_FD4_high_phase_temporal_aliasing_closed') is False and
           d20report.get('M1_uses_FROZEN_H3G_B20_not_new_q20') is True and
           d19report.get('numerical_tol_pass') is True):
        raise RuntimeError('D21 cannot accept a changed D20R1/D19R1 classification')
    old=d20.source.old;r7=old.r7
    d20.source.code_lock()
    paths,cert=d20.source.frozen_inputs(rd,trace)
    if not (len(r7.FOURIER_N)==6 and old.M_MAX==40 and old.GE05_TO_GE06==2.):
        raise RuntimeError('D21 Fourier dictionary/original GE05 mapping changed')
    print('GE19_D21R1_D17_D19R1_D20R1_AND_ORIGINAL_GE05_SOURCE_SHA_PASS',flush=True)
    out={};modes=np.asarray(r7.FOURIER_N,int);nx=128;chunk=int(pre['node_chunk'])
    with (np.load(paths['r13'],allow_pickle=False) as r13,
          np.load(rd/files['D17_NPZ'],allow_pickle=False) as d17,
          np.load(rd/files['D19_NPZ'],allow_pickle=False) as d19,
          np.load(rd/files['D20_NPZ'],allow_pickle=False) as d20npz):
        bgs,_,mod6,mod7,ge05,_,_,_,_=old.build_context(rd,r13)
        bg=bgs[(128,'C_star')];x=np.asarray(bg['x'],float)
        Y=np.asarray(d17['primary_C_star_H1_canonical_y_dense_sub4'],complex)
        h1,dh1,backward,raw,slots=d20.canonical_knots_to_h1(
            Y,bg,'C_star',r7,mod6,mod7)
        X=np.asarray(d17['primary_C_star_X10_original_action_dense_sub4'],complex)[:,::4]
        DX=np.asarray(d17['primary_C_star_X10_x_original_action_dense_sub4'],complex)[:,::4]
        Xrecomputed=old.r24.first_order_X_modes(r7,bg,h1)
        if not(np.array_equal(x,np.asarray(d17['x_primary'],float)) and
               np.array_equal(x,np.asarray(d19['original_x_primary'],float)) and
               core.rel(X,Xrecomputed)<1e-10 and backward<1e-9 and slots<1e-9):
            raise RuntimeError('D21 D17 canonical original-action H1/X/physical grid mismatch')
        z=np.asarray(d19['physical_Cstar_Nt128_Nq2048_z_sub256'],complex)
        v=np.asarray(d19['physical_Cstar_Nt128_Nq2048_v_sub256'],complex)
        if z.shape!=(2048,6,128) or v.shape!=z.shape or not np.isfinite(z).all():
            raise RuntimeError('D21 all original D19 bath nodes not available')
        r,w=old.c4.tan_gl_nodes(2048);r=np.asarray(r,float);w=np.asarray(w,float)
        tau=old.r24.TAUH0/float(r7.g9.H0_CLASS)
        if max(core.rel(np.einsum('n,nmt->mt',w,z),np.asarray(d19['sub256_weighted_z'],complex)),
               core.rel(np.einsum('n,nmt->mt',w,v),np.asarray(d19['sub256_weighted_v'],complex)))>1e-11:
            raise RuntimeError('D21 D19R1 complete-bath replay failed')
        grav=old.grav_real_for_memory(bg,h1,modes,nx)
        u=np.asarray(grav['u'],float)
        ut=np.asarray(r7.reconstruct_positive_modes(dh1[:,1,:],nx),float)
        Xr=np.asarray(r7.reconstruct_positive_modes(X,nx),float)
        Xtr=np.asarray(r7.reconstruct_positive_modes(bg['H'][None,:]*DX,nx),float)
        action_X_from_fields=bg['Q_action'][:,None]*u+grav['px']/bg['a'][:,None]
        xreal_rel=core.rel(Xr,action_X_from_fields)
        if xreal_rel>1e-10:
            raise RuntimeError('D21 X10 real reconstructed from old action fields mismatches D17 X')
        H=np.asarray(bg['H'],float);a=np.asarray(bg['a'],float)
        Dx=r7.fd4_matrix(len(x),x[0],x[-1]);Dt=H[:,None]*Dx
        # Independent check that the diagnostic stencil is exactly the
        # original frozen FD4 matrix; the actual delta uses frozen Dt.
        probe=np.cos(.13*np.arange(len(x),dtype=float))[None,:,None]
        check=core.rel(core.fd4_uniform(probe,x,H)[0,:,0],H*(Dx@probe[0,:,0]))
        if check>1e-11:raise RuntimeError('D21 original FD4 definition differs')
        total=np.zeros((len(x),nx),float)
        compensation=np.zeros_like(total)
        oldt_norm=0.;newt_norm=0.;delta_norm=0.;max_symbolic_rel=0.
        max_symbolic_aor=0.;max_chunk_delta_abs=0.
        nn=len(r)
        for i in range(0,nn,chunk):
            stop=min(i+chunk,nn);rr=r[i:stop];ww=w[i:stop]
            zr=np.asarray(old.r24.reconstruct_batched_positive_modes(z[i:stop],modes,nx),float)
            ztr=np.asarray(old.r24.reconstruct_batched_positive_modes(v[i:stop]/tau,modes,nx),float)
            om=rr[:,None,None]/tau;sw=np.sqrt(ww)[:,None,None]
            aa=a[None,:,None];Q=bg['Q_action'][None,:,None]
            # Frozen f_c2['pt'] is evaluated, then compared against its
            # independently derived exact normalized action identity.
            q=sw*zr/om
            pt=np.asarray(ge05.f_c2['pt'](
                aa,Q,grav['N'][None],grav['S'][None],grav['S'][None],
                0.,grav['u'][None],grav['pt'][None],grav['px'][None],
                0.,0.,q,om,sw),float)
            analytic_pt=core.current(a,u,zr,Xr,ww)
            symrel=core.rel(pt,analytic_pt)
            symaor=float(np.max(np.abs(pt-analytic_pt)))
            max_symbolic_rel=max(max_symbolic_rel,symrel)
            max_symbolic_aor=max(max_symbolic_aor,symaor)
            if symrel>pre['max_original_GE05_pt_current_identity_relative']:
                raise RuntimeError(f'D21 true original GE05 pt current identity FAIL chunk {i}: {symrel}')
            olddot=np.einsum('ij,bjk->bik',Dt,pt,optimize=True)
            newdot=core.current_dot(a,H,u,ut,zr,ztr,Xr,Xtr,ww)
            diff=core.mapped_M2_scalar_delta(olddot,newdot,old.GE05_TO_GE06)
            if not(np.isfinite(diff).all() and np.isfinite(pt).all()):
                raise RuntimeError('D21 nonfinite GE05 phase-safe M2 derivative')
            kahan_add(total,compensation,np.sum(diff,axis=0))
            oldt_norm+=float(np.vdot(olddot,olddot).real)
            newt_norm+=float(np.vdot(newdot,newdot).real)
            delta_norm+=float(np.vdot(diff,diff).real)
            max_chunk_delta_abs=max(max_chunk_delta_abs,float(np.max(np.abs(diff))))
            if (i//chunk+1)%32==0 or stop==nn:
                print(f'GE19_D21R1_PT_TIME_DERIVATIVE_CHUNK {stop}/{nn} '
                      f'original_pt_identity={symrel:.3e}',flush=True)
        fft_delta=np.asarray(old.fft_low(total),complex)
        if fft_delta.shape!=(128,41) or not np.isfinite(fft_delta).all():
            raise RuntimeError('D21 GE05 scalar M2 source delta Fourier shape changed')
        old_m2=np.asarray(d20npz['Cstar_beta0_'+ledger.PIECES[5]+'_rows_M1_FROZEN_UNRECLOSED'],complex)
        for ib in (1,2):
            other=np.asarray(d20npz[f'Cstar_beta{ib}_'+ledger.PIECES[5]+'_rows_M1_FROZEN_UNRECLOSED'],complex)
            if not np.array_equal(old_m2,other):
                raise RuntimeError('D21 D20 original M2 source unexpectedly beta-dependent')
        corrected=old_m2.copy();corrected[3]+=fft_delta
        delta=corrected-old_m2
        if (corrected.shape!=(8,128,41) or not np.isfinite(corrected).all() or
            not np.array_equal(corrected[np.array([0,1,2,4,5,6,7])],old_m2[np.array([0,1,2,4,5,6,7])])):
            raise RuntimeError('D21 non-scalar GE05 M2 rows were changed')
        out['original_x_primary']=x
        out['M2_old_original_knot_FD4_D20R1_NOT_PHASE_SAFE']=old_m2
        out['M2_new_exact_GE05_pt_time_derivative_D19R1_CONDITIONAL']=corrected
        out['M2_delta_scalar_row_3_only']=delta[3]
        out['M2_analytic_minus_FD4_mapped_scalar_spatial_sum']=total
        controls=[];max_linearity=0.;max_reassemble=0.
        for ib,beta in enumerate(r7.BETAS):
            prefix=f'Cstar_beta{ib}_'
            parts={name:np.asarray(d20npz[prefix+name+'_rows_M1_FROZEN_UNRECLOSED'],complex).copy()
                   for name in ledger.PIECES}
            parts[ledger.PIECES[5]]=corrected
            oldtotal=np.asarray(d20npz[prefix+'mixed_parent_total_rows_NOT_H4_SOURCE'],complex)
            oldward=np.asarray(d20npz[prefix+'mixed_parent_source_ward_NOT_FULL_WARD'],complex)
            full=oldtotal+delta
            summed=sum(parts.values())
            # The exact H4 source-Ward projection reads only rows 6,1,7.
            # GE05 c2[pt] contributes to the scalar row 3. Therefore this
            # corrected M2 scalar does not change the SOURCE-ONLY Ward;
            # this is a structural zero, NOT the full on-shell Ward test.
            delta_ward=clock.physical_source_ward(delta,x,bg['a'],H,
                float(r7.g9.K_REQ[0]/r7.FOURIER_N[0]),'fd4')
            if np.any(delta_ward):
                raise RuntimeError('D21 pure M2 scalar row affected source-only Ward')
            proper=clock.physical_six_piece_ward(
                parts,x,bg['a'],H,
                float(r7.g9.K_REQ[0]/r7.FOURIER_N[0]))
            lin=core.rel(oldward,proper['total_source_ward'])
            sumrel=core.rel(full,summed)
            max_linearity=max(max_linearity,lin);max_reassemble=max(max_reassemble,sumrel)
            out[prefix+'M2_phase_safe_scalar_current_CONDITIONAL']=corrected
            out[prefix+'mixed_M1_FROZEN_UNRECLOSED_total_rows_CONDITIONAL']=full
            out[prefix+'mixed_M1_FROZEN_UNRECLOSED_source_ward_NOT_FULL_H4']=proper['total_source_ward']
            controls.append({'beta':float(beta),'source_ward_linear_relative':lin,
                'six_piece_row_reassemble_relative':sumrel,
                'M1_q20_reclosed':False,'Z11_under_D17_reclosed':False})
        gates={
          'frozen_D17_D19_D20_original_source_sha':True,
          'original_GE05_c2_pt_symbolic_action_identity':max_symbolic_rel<=pre['max_original_GE05_pt_current_identity_relative'],
          'D17_X_and_physical_u_jets_consistent':xreal_rel<=1e-10 and backward<1e-9 and slots<1e-9,
          'all_original_quadrature_nodes_included':nn==2048,
          'only_original_M2_scalar_pt_derivative_changed':True,
          'new_conditional_source_all_finite':np.isfinite(corrected).all() and np.isfinite(full).all(),
          'mixed_stale_M1_linear_ledger_only':max(max_linearity,max_reassemble)<=1e-10,
        }
        passed=all(gates.values())
        classification=('GE19_D21R1_EXACT_GE05_PT_CHAIN_RULE_M2_NUMERICAL_REPAIR_PASS_Q20_Z11_FULL_H4_OPEN'
                        if passed else 'GE19_D21R1_EXACT_GE05_PT_CHAIN_RULE_M2_NUMERICAL_REPAIR_FAIL')
        result={
          'classification':classification,'preregistration':pre['classification'],
          'gates':{k:bool(v) for k,v in gates.items()},
          'cohort':'C_star Nt128 Nq2048; original 6 positive Fourier, output m0..40',
          'parent_results_sha256':{name:sha(rd/file) for name,file in files.items()},
          'source_sha256':{rel:sha(ROOT/rel) for rel in pre['source_sha256']},
          'original_GE05_c2_pt_current_identity':'c2[pt]=a^3*w*u10*(z10-X10)',
          'original_GE05_c2_pt_time_derivative':'a^3*w*[(3*H*u10+u10_t)*(z10-X10)+u10*(v10/tau-X10_t)]',
          'original_GE05_c2_pt_current_identity_relative_max':max_symbolic_rel,
          'original_GE05_c2_pt_current_identity_absolute_max_report_only':max_symbolic_aor,
          'D17_X_real_from_action_fields_relative':xreal_rel,
          'D17_canonical_row_backward_relative_max':backward,
          'original_FD4_stencil_reproduction_relative':check,
          'GE05_M2_phase_safe_scalar_time_derivative':True,
          'GE05_pt_time_derivative_old_FD4_node_L2_report_only':float(np.sqrt(oldt_norm)),
          'GE05_pt_time_derivative_new_chain_rule_node_L2_report_only':float(np.sqrt(newt_norm)),
          'GE05_mapped_scalar_derivative_delta_node_L2_report_only':float(np.sqrt(delta_norm)),
          'GE05_mapped_scalar_derivative_delta_node_max_abs_report_only':max_chunk_delta_abs,
          'GE05_M2_phase_safe_vs_original_FD4_relative_L2_report_only':core.rel(corrected,old_m2),
          'GE05_M2_phase_safe_vs_original_FD4_scalar_relative_L2_report_only':core.rel(corrected[3],old_m2[3]),
          'GE05_M2_phase_safe_vs_original_FD4_scalar_absolute_L2_report_only':float(np.linalg.norm(delta[3])),
          'GE05_M2_non_scalar_rows_exact_unchanged':True,
          'GE05_M2_scalar_row_source_only_Ward_exact_zero_delta':True,
          'GE05_bath_original_knot_FD4_Euler_unreliable_parent_report_only':d20report['GE05_bath_original_knot_FD4_Euler_report_only'],
          'D19R1_sampled_GE05_bath_relative_parent_report_only':d19report['runs'][-1]['sampled_GE05_D17_surrogate_relative_residual_max_not_continuum_bound'],
          'GE05_on_shell_certified':False,'GE05_M2_source_depends_on_numerical_D17_and_D19R1':True,
          'new_physical_q20_and_Z11_recomputed':False,'M1_uses_FROZEN_H3G_B20_not_new_q20':True,
          'beta_controls':controls,'full_original_H4_Ward_certified':False,
          'H4_Z21_solve_performed':False,'Z21_certified':False,'lensing_licensed':False,
          'original_Repair37_SCIENCE_FAIL_immutable':True,'no_observational_tuning':True,
          'claim_boundary':'Exact GE05 action c2[pt] identity and ODE-jet chain rule remove the temporal FD4 derivative from M2 scalar row at all original knots for D19R1 full bath. This scalar-only change leaves the SOURCE-ONLY Ward projection unchanged, not a proof of full H4 identity. Original action other GE05 M2 pieces, D17 H1, old H3G q20/M1, Z11, other five source rows are untouched. Does NOT independently certify continuum GE05 Euler, H1 or q20/Z11 under changed drive, and mixed old-M1 ledger is not a consistent full H4 source. No full Noether/operator/boundary, Z21 or lensing.',
        }
        oj.parent.mkdir(parents=True,exist_ok=True)
        oj.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+'\n')
        np.savez_compressed(on,**out)
        print('GE19_D21R1_GE05_M2_CORRECTED_DELTA_REL={:.8e} '
              'GE05_PT_IDENTITY_REL={:.8e} LEDGER_REL={:.8e}'.format(
                result['GE05_M2_phase_safe_vs_original_FD4_relative_L2_report_only'],
                max_symbolic_rel,max(max_linearity,max_reassemble)),flush=True)
        print('GE19_D21R1_CLASSIFICATION '+classification,flush=True)
        if not passed:raise SystemExit(2)

if __name__=='__main__':main()
