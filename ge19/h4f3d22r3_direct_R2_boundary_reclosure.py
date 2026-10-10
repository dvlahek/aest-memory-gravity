#!/usr/bin/env python3
"""D22R3: one bounded repair of D22A's reused source-dependent Z11 time jet.

Rebuild the original R2 eta-tangent reference AND its physical-time jet from
Repair28, replay frozen D17/D19/D22A provenance, inspect the action shift at
initial time under fresh and historical data, and re-solve only the six Z11
modes if the fresh reference genuinely differs. Do NOT reclassify D22A FAIL,
weaken its gates, reuse stale q20, or claim full H4/Z21/lensing.
"""
from __future__ import annotations
import argparse, hashlib, json, os, subprocess
from pathlib import Path
from contextlib import ExitStack
import numpy as np
from ge19 import h4f3d22a_action_parent_reclosure as d22
from ge19 import h4f3d20r1_recompute_five_sources_and_bath_ward as d20
from ge19 import h4f3d17_actual_original_action_dense_canonical_H1 as d17driver
from ge19 import h4f3d17_original_action_dense_H1_core as d17core
from ge19 import repair32b_factor2_corrected_reduced_h2_z11_reconstruction as h2

ROOT=Path(__file__).resolve().parents[1]
D22J='158207d747e9fa617c335f4a30d860c011264b2da1dcde34870bad762ec5bbf4'
D22N='6952a2cde9a39367d29b75b63aca53a97a8feb622e7cbe7b33a468ae2b9a1632'
FORENSICJ='8ea15a3d3ca433551efeb8c2e445a4f14f2a0c6c246d54c6195899b180c03210'
CONSTRAINT_MAX=1e-6
TINY=1e-300

def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()

def rel(a,b):
    a=np.asarray(a);b=np.asarray(b)
    return float(np.linalg.norm(a-b)/max(np.linalg.norm(a),np.linalg.norm(b),TINY))

def aor(a,b):
    a=np.asarray(a);b=np.asarray(b)
    d=np.abs(a-b)
    return float(np.max(np.minimum(d,d/np.maximum(np.maximum(np.abs(a),np.abs(b)),TINY))))

def locate_r28(rd,provided):
    if provided:
        paths=[Path(provided).expanduser().resolve()]
    else:
        paths=sorted({p for p in rd.glob('*repair28*.npz') if p.is_file()} |
                     {p for p in (ROOT/'frozen_repair26_repair27').rglob('*repair28*.npz') if p.is_file()})
    for path in paths:
        if sha(path)==h2.R28_NPZ_SHA:return path
    raise RuntimeError('R2 Repair28 NPZ SHA not found; set GE19_REPAIR28_R2_NPZ to the original, SHA '+h2.R28_NPZ_SHA)

def row_metric(r7,mod6,mod7,bg,tag,mode,x0,reference,dot,rhs):
    k=float(mode*r7.g9.K_REQ[0]/r7.FOURIER_N[0])
    q0=np.asarray(reference[[1,2,3,4],0],complex)
    v0=np.asarray(dot[:,0],complex)
    y0,w0,init=r7._initial_canonical_state(mod6,mod7,bg,tag,k,float(x0),q0,v0,rhs)
    *_,Cmat,_,_=r7._canonical_operator_matrices(mod6,mod7,bg,tag,k,float(x0))
    row=Cmat[10]+Cmat[11]
    value=r7._constraint_backward_error(row,w0,0j,Cmat[10]@w0,Cmat[11]@w0)
    return {k:float(value[k]) for k in ('metric','absolute_residual','scale','contribution_scale')},w0

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--results-dir',type=Path,required=True)
    p.add_argument('--repair26-trace',type=Path,required=True)
    p.add_argument('--repair28-npz',type=Path)
    p.add_argument('--json-out',type=Path,required=True)
    p.add_argument('--npz-out',type=Path,required=True)
    args=p.parse_args()
    rd=args.results_dir.resolve();trace=args.repair26_trace.resolve()
    jout=args.json_out.resolve();nout=args.npz_out.resolve()
    if jout.exists() or nout.exists():raise RuntimeError('D22R3 refuses to overwrite original or previous results')
    pre=json.loads(d22.PRE.read_text())
    files,inputs,_=d22.verify(rd,trace,pre)
    d22j=rd/'ge19_h4f3d22a_actual_Cstar_action_B10_Z11_Z20_parent_candidates.json'
    d22n=d22j.with_suffix('.npz')
    forensic=rd/'ge19_h4f3d22a_r2_shift_forensic.json'
    for pp,want in ((d22j,D22J),(d22n,D22N),(forensic,FORENSICJ)):
        if not pp.is_file() or sha(pp)!=want:raise RuntimeError('D22R3 frozen failed archive changed '+str(pp))
    if json.loads(d22j.read_text())['classification']!='GE19_D22A_CSTAR_PARENT_NUMERICAL_CANDIDATE_FAIL_Q20_AND_FULL_H4_OPEN':
        raise RuntimeError('D22A failed archive classification modified')
    r28path=locate_r28(rd,args.repair28_npz)
    print('GE19_D22R3_FROZEN_D17_D19_D22A_FORENSIC_AND_R28_SHA_PASS',flush=True)
    old=d20.source.old;r7=old.r7
    with ExitStack() as st:
        r13=st.enter_context(np.load(inputs['r13'],allow_pickle=False))
        oldz=st.enter_context(np.load(inputs['z11'],allow_pickle=False))
        failed=st.enter_context(np.load(d22n,allow_pickle=False))
        r28=st.enter_context(np.load(r28path,allow_pickle=False))
        xR2,R2,chi=h2.load_r2_parent(r28)
        bgs,_,mod6,mod7,_,_,_,_,_=old.build_context(rd,r13)
        bg=bgs[(128,'C_star')];x=np.asarray(bg['x'],float)
        _,bases,base_states,_,_=h2.build_backgrounds(rd/'ge15_R1_dense_accepted_step_trace.dat',r13)
        fields=h2.tangent_on_grid(xR2,R2,x)
        dust,std_dr,std_mom=h2.integrate_dust_tangent(bg,base_states[128],fields)
        fresh_ref,fresh_dot=h2.make_reference(bg,bases[128],fields,dust)
        old_ref=np.asarray(failed['Z11_R2_frozen_reference_primary'],complex)
        stale_dot=np.asarray(oldz['C_star_Z11dot_primary'],complex)
        rhs=np.asarray(failed['GE05_M1_rhs_for_Z11_primary'],complex)
        if fresh_ref.shape!=(6,6,128) or fresh_dot.shape!=(6,4,128) or rhs.shape!=(6,6,128):
            raise RuntimeError('R2 boundary, source or reference shape mismatch')
        # This is a genuine R2 reference identity check, not self-comparison of old solution derivatives.
        ref_state_rel=rel(fresh_ref,old_ref)
        ref_boundary=aor(fresh_ref[:,1:5,0],old_ref[:,1:5,0])
        oldjet_delta=aor(fresh_dot[:,:,0],stale_dot[:,:,0])
        if ref_boundary>1e-8:raise RuntimeError('Fresh Repair28 R2 initial state differs from archived physical eta reference')
        print('GE19_D22R3_FRESH_R2_BOUNDARY_CHECK '
              f'state_rel={ref_state_rel:.4e} initial_state_aor={ref_boundary:.4e} '
              f'fresh_dot_vs_stale_dot_aor={oldjet_delta:.4e}',flush=True)
        oldbg=r7._bg_point;oldcache=r7._CANONICAL_LOCAL_CACHE
        # Both comparisons use identical true-R2 data, and no frozen matrix cache.
        try:
            r7._CANONICAL_LOCAL_CACHE={}
            legacy=[]
            for im,m in enumerate(r7.FOURIER_N):
                rr,_=row_metric(r7,mod6,mod7,bg,'C_star',int(m),x[0],
                                fresh_ref[im],fresh_dot[im],rhs[im,:,0])
                legacy.append(rr)
            evalH,_=d17driver.d16r1.d15.clk.make_original_action_background(r7,bg,'C_star')
            ctx=d17core.ActionBackground(r7,bg,evalH);ctx.knot_check()
            r7._bg_point=lambda b,xx:ctx(b,xx)
            r7._CANONICAL_LOCAL_CACHE={}
            act=[];stale=[]
            for im,m in enumerate(r7.FOURIER_N):
                rr,_=row_metric(r7,mod6,mod7,bg,'C_star',int(m),x[0],
                                fresh_ref[im],fresh_dot[im],rhs[im,:,0])
                rs,_=row_metric(r7,mod6,mod7,bg,'C_star',int(m),x[0],
                                old_ref[im],stale_dot[im],rhs[im,:,0])
                act.append(rr);stale.append(rs)
                print(f'GE19_D22R3_ACTION_R2_MODE {int(m)} '
                      f'fresh_shift={rr["metric"]:.3e} stale_shift={rs["metric"]:.3e}',flush=True)
            fresh_init=max(q['metric'] for q in act)
            # Only one six-mode solve. Do it if fresh R2 data are not literally equivalent,
            # or if the initial shift has changed; never repeat the old D22A Z20 40-mode solve.
            can_solve=bool(oldjet_delta>1e-12 or abs(fresh_init-max(q['metric'] for q in stale))>1e-6)
            zz=dd=ctrl=None
            if can_solve:
                zz,dd,ctrl=h2.solve_h2_case(mod6,mod7,bg,'C_star',rhs,fresh_ref,fresh_dot)
                print('GE19_D22R3_ONE_FRESH_R2_Z11_SOLVE '
                      f'linear={ctrl["linear_system_relative_L2_max"]:.3e} '
                      f'shift={ctrl["shift_constraint_relative_L2_max"]:.3e}',flush=True)
            else:
                print('GE19_D22R3_ORIGINAL_R2_DOT_EQUIVALENT_SKIP_POINTLESS_REINTEGRATION',flush=True)
        finally:
            r7._bg_point=oldbg;r7._CANONICAL_LOCAL_CACHE=oldcache
        # Zero is not a desired target for source-only Ward or a test of H4.
        report={
            'classification':('GE19_D22R3_FRESH_R2_Z11_SOLVE_NUMERICAL_CANDIDATE_ONLY' if ctrl is not None
                              else 'GE19_D22R3_FRESH_R2_BOUNDARY_EQUIVALENT_D22A_FAIL_RETAINS'),
            'D22A_failure_immutable':True,'D22AR2_forensic_immutable':True,
            'new_R2_derived_from_Repair28_not_old_Z11_solution_dot':True,
            'reference_full_state_relative_report_only':ref_state_rel,
            'reference_initial_dynamic_state_abs_or_rel':ref_boundary,
            'fresh_R2_dot_vs_stale_Z11_solution_dot_initial_abs_or_rel':oldjet_delta,
            'fresh_R2_initial_shift_max':fresh_init,
            'frozen_operator_fresh_R2_initial_shift_max':max(q['metric'] for q in legacy),
            'original_action_stale_R2_initial_shift_max':max(q['metric'] for q in stale),
            'fresh_R2_initial_shift_by_mode':{str(int(m)):q for m,q in zip(r7.FOURIER_N,act)},
            'old_solution_dot_initial_shift_by_mode':{str(int(m)):q for m,q in zip(r7.FOURIER_N,stale)},
            'one_six_mode_Z11_solve_performed':ctrl is not None,
            'one_six_mode_Z11_solve_controls':None if ctrl is None else {k:v for k,v in ctrl.items() if k!='canonical_march_diagnostics'},
            'Z11_shift_original_frozen_gate_1e6_met':bool(ctrl is not None and ctrl['shift_constraint_relative_L2_max']<=CONSTRAINT_MAX),
            'Z11_certified':False,'Z20_certified':False,'q20_B20_recomputed':False,
            'full_H4_Ward_certified':False,'Z21_certified':False,'lensing_licensed':False,
            'source_hashes':{'R28':sha(r28path),'D22J':D22J,'D22N':D22N,'D22AR2J':FORENSICJ},
            'claim_boundary':'Genuine R2-derived initial physical jets and source-aware original-action six-mode H2 test only. D22A FAIL remains immutable. Nt64/C-control and H3 shift propagation remain open; no q20, full H4/Z21 or lensing.'
        }
        out={'x_primary':x,'fresh_R2_reference_primary':fresh_ref,
             'fresh_R2_dot_primary':fresh_dot,'stale_Z11_solution_dot_primary':stale_dot,
             'new_GE05_M1_rhs_primary':rhs}
        if zz is not None:
            out['fresh_R2_Z11_numerical_candidate_primary']=zz
            out['fresh_R2_Z11dot_numerical_candidate_primary']=dd
    jout.parent.mkdir(parents=True,exist_ok=True)
    jout.write_text(json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+'\n')
    np.savez_compressed(nout,**out)
    print('GE19_D22R3_CLASSIFICATION '+report['classification'],flush=True)
    if ctrl is not None and not report['Z11_shift_original_frozen_gate_1e6_met']:
        print('GE19_D22R3_Z11_ACTION_SHIFT_STILL_OPEN_DO_NOT_PROMOTE',flush=True)

if __name__=='__main__':main()
