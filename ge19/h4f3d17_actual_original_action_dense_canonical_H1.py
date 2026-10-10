#!/usr/bin/env python3
"""D17: independent original-action dense canonical H1 NUMERICAL DIAGNOSTIC.

This is not an interval-certified continuous H1 or GE05 bath on-shell solve.
No bath state is propagated or modified. The original Repair07 source is
source-locked, not edited. Its off-knot PCHIP background callback is replaced
only inside this separate process with the scalar-charge/Lambda action
continuation verified by original D15a, then restored in finally.
"""
from __future__ import annotations
import argparse,hashlib,json,subprocess
from pathlib import Path
import numpy as np
from ge19 import h4f3d16r1_actual_original_H1dot_Hermite_physical_bath as d16r1
from ge19 import h4f3d16_original_H1dot_Hermite_physical_bath_core as d16core
from ge19 import h4f3d17_original_action_dense_H1_core as core

ROOT=Path(__file__).resolve().parents[1]
PRE='ge19/h4f3d17_predata_original_action_dense_canonical_H1.json'
NSUB=(1,2,4)
TINY=1e-300

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda:f.read(1<<20),b''):h.update(block)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--results-dir',required=True)
    ap.add_argument('--repair26-trace',required=True)
    ap.add_argument('--json-out',required=True);ap.add_argument('--npz-out',required=True)
    args=ap.parse_args()
    rd=Path(args.results_dir).resolve();trace=Path(args.repair26_trace).resolve()
    oj=Path(args.json_out).resolve();on=Path(args.npz_out).resolve()
    if oj.exists() or on.exists():raise RuntimeError('D17 refuses overwrite')
    pre=json.loads((ROOT/PRE).read_text())
    if pre['classification']!='GE19_H4F3D17_PREDATA_ORIGINAL_ACTION_DENSE_CANONICAL_H1_NUMERICAL_DIAGNOSTIC':
        raise RuntimeError('D17 preregistration changed')
    for rel,want in pre['source_blobs'].items():
        head=subprocess.check_output(['git','rev-parse','HEAD:'+rel],cwd=ROOT,text=True).strip()
        work=subprocess.check_output(['git','hash-object',str(ROOT/rel)],cwd=ROOT,text=True).strip()
        if not (head==work==want):raise RuntimeError('D17 original frozen source blob changed: '+rel)
    for rel,want in pre['local_source_SHA256'].items():
        if sha(ROOT/rel)!=want:raise RuntimeError('D17 local prereg source changed: '+rel)
    d16pre=json.loads((ROOT/d16r1.PRE).read_text())
    pins,raw,actual=d16r1.physical_input_locks(rd,trace,d16pre)
    d15=d16r1.d15
    paths,parentlocks=d15.parents.frozen_inputs(rd,trace)
    if not all(parentlocks[q]['exact'] for q in d15.parents.REQUIRED):
        raise RuntimeError('D17 original H3F H3G Z11 Repair13 locked parent changed')
    d16j=rd/pre['D16R1_parents']['JSON'][0]
    d16n=rd/pre['D16R1_parents']['NPZ'][0]
    if sha(d16j)!=pre['D16R1_parents']['JSON'][1] or sha(d16n)!=pre['D16R1_parents']['NPZ'][1]:
        raise RuntimeError('D17 D16R1 actual physical parent changed')
    d16report=json.loads(d16j.read_text())
    if (d16report.get('classification')!='GE19_H4F3D16R1_ACTUAL_ORIGINAL_H1DOT_HERMITE_PHYSICAL_CLOCK_BATH_SURROGATE_DIAGNOSTIC_PASS_TRUE_X10_ONSHELL_OPEN'
        or d16report.get('true_continuous_original_X10_error_enclosed') is not False):
        raise RuntimeError('D17 D16R1 immutable claim boundary changed')
    old=d15.d13.old
    r7=old.r7
    summary=[];saved={}
    bg_rows=[]
    print('GE19_D17_SOURCE_AND_D16R1_ACTUAL_PARENT_SHA_PASS',flush=True)
    with (np.load(paths['r13'],allow_pickle=False) as r13,
          np.load(paths['h3fn'],allow_pickle=False) as h3f,
          np.load(d16n,allow_pickle=False) as d16archive):
        bgs,_,mod6,mod7,_,_,_,_,_=old.build_context(rd,r13)
        # Frozen callback / local Cmat cache must never be changed on disk.
        original_bgpoint=r7._bg_point
        original_Cmat_cache=r7._CANONICAL_LOCAL_CACHE
        r7._CANONICAL_LOCAL_CACHE={}
        active={'context':None}
        def exact_bgpoint(bg,xq):
            ctx=active['context']
            if ctx is None:raise RuntimeError('D17 action callback missing active case')
            return ctx(bg,xq)
        r7._bg_point=exact_bgpoint
        try:
            for label,nt in (('primary',128),('control',64)):
                xx=np.asarray(h3f['x_'+label],float)
                saved['x_'+label]=xx
                for tag in r7.C_TAGS:
                    bg=bgs[(nt,tag)]
                    if not np.array_equal(xx,np.asarray(bg['x'],float)):
                        raise RuntimeError('D17 original H3F/Repair13 x-grid changed')
                    h1=np.asarray(h3f[f'{tag}_H1_{label}'],complex)
                    h1dot=np.asarray(h3f[f'{tag}_H1dot_{label}'],complex)
                    Xorig,Xxorig=d16core.frozen_endpoint_X_Xx(r7,bg,h1,h1dot)
                    prefix=f'{label}_{tag}_'
                    if (core.rel(Xorig,np.asarray(d16archive[prefix+'original_X10_H1_endpoint'],complex))>1e-13
                        or core.rel(Xxorig,np.asarray(d16archive[prefix+'original_X10_x_derivative_from_H1dot'],complex))>1e-13):
                        raise RuntimeError('D17 original D16R1 certified H1 endpoint jets changed')
                    evalH,actiondiag=d15.clk.make_original_action_background(r7,bg,tag)
                    ctx=core.ActionBackground(r7,bg,evalH)
                    active['context']=ctx
                    ctx.knot_check()
                    # Source-exact continuous action vs original source PCHIP,
                    # sampled strictly inside each original H3F interval.
                    for xmid in .5*(xx[1:]+xx[:-1]):
                        source=original_bgpoint(bg,float(xmid))
                        action=ctx(bg,float(xmid))
                        for key in ctx.max_frozen_pchip_relative:
                            av=float(action[key]);fv=float(source[key])
                            diff=abs(av-fv)/max(abs(av),abs(fv),TINY)
                            ctx.max_frozen_pchip_relative[key]=max(ctx.max_frozen_pchip_relative[key],diff)
                    # At frozen H1 knots both continuations reproduce
                    # original Repair13 H,Q,Z, but off-knot values need not.
                    row={'C':tag,'Nt':nt,'original_action_background':actiondiag,
                         'sampled_original_PCHIP_vs_original_action_relative_max_not_bound':ctx.max_frozen_pchip_relative.copy()}
                    Ys={};Xs={};Xxs={};numeric={};defects=[]
                    for im,m in enumerate(np.asarray(r7.FOURIER_N,int)):
                        k=float(m*r7.g9.K_REQ[0]/r7.FOURIER_N[0])
                        matrices={};operator_diag=[]
                        def M_at(xq):
                            key=round(float(xq),15)
                            if key not in matrices:
                                M,F,ZY,ZR,WY,WR,Cmat,bp,d=r7._canonical_operator_matrices(
                                    mod6,mod7,bg,tag,k,float(xq))
                                if not np.isfinite(M).all():
                                    raise RuntimeError('D17 nonfinite frozen canonical first-order action operator')
                                matrices[key]=M
                                operator_diag.append(d)
                            return matrices[key]
                        q0=h1[im,[1,2,3,4],0]
                        v0=h1dot[im,:,0]
                        y0,w0,idg=r7._initial_canonical_state(mod6,mod7,bg,tag,k,float(xx[0]),q0,v0,np.zeros(6,complex))
                        init=core.aor(w0[[0,1,2,3,4,5,6,7,8,9]],
                            np.r_[h1[im,0,0],h1[im,5,0],h1[im,[1,2,3,4],0],h1dot[im,:,0]])
                        if init>1e-9 or idg['initial_algebraic_scaled_residual']>1e-8:
                            raise RuntimeError('D17 frozen original canonical initial boundary mismatch')
                        ymode={};stepdiag={}
                        for nsub in NSUB:
                            xf,yf,diag=core.integrate_original_grid(xx,y0,nsub,M_at,r7._dense_equilibrated_solve)
                            ymode[nsub]=(xf,yf);stepdiag[nsub]=diag
                        if not np.array_equal(ymode[4][0][::4],xx):
                            raise RuntimeError('D17 true original H3F knots not retained in dense action solve')
                        xfine,yfine=ymode[4]
                        Xfine=np.empty(len(xfine),complex);Xxfine=np.empty_like(Xfine)
                        for it,xq in enumerate(xfine):
                            point=ctx(bg,float(xq))
                            dy=M_at(float(xq))@yfine[:,it]
                            ik_a=1j*k/point['a']
                            Xfine[it]=point['Q_action']*yfine[1,it]+ik_a*yfine[2,it]
                            Xxfine[it]=(core.action_Qx_from_Z(point['Z_action'],r7.Z0)*yfine[1,it]
                                         +point['Q_action']*dy[1]+ik_a*(dy[2]-yfine[2,it]))
                        if not(np.isfinite(Xfine).all() and np.isfinite(Xxfine).all()):
                            raise RuntimeError('D17 nonfinite source-action X10 dense output')
                        original_at_knots=Xorig[im]
                        original_xjets=Xxorig[im]
                        true_x0=core.aor(Xfine[0],original_at_knots[0])
                        if true_x0>1e-11:
                            raise RuntimeError('D17 original X10 first knot changed')
                        # Original parent Xx is based on original H1dot cosmic-time jets.
                        Xx0diff=core.aor(Xxfine[0],original_xjets[0])
                        sampled=core.sampled_hermite_ode_defect(xfine,yfine,M_at)
                        defects.append(sampled)
                        Ys[im]=yfine;Xs[im]=Xfine;Xxs[im]=Xxfine
                        numeric[im]={'mode_m':int(m),'initial_H1_action_vs_frozen_aor':init,
                                     'initial_Xx_source_vs_H3F_H1dot_aor':Xx0diff,
                                     'Radau_step_scaled_solve_residual_max':{str(n):stepdiag[n] for n in NSUB},
                                     'canonical_algebraic_scaled_residual_max':float(max(q['algebraic_scaled_residual_max'] for q in operator_diag)),
                                     'source_operator_condition_2_max_report_only':float(max(q['algebraic_scaled_condition_2'] for q in operator_diag)),
                                     'source_noether_null_scaled_L2_max_report_only':float(max(q['old_partition_noether_null_scaled_L2'] for q in operator_diag)),
                                     'H1_canonical_endpoint_sub1_vs_sub2_relative_diagnostic_not_bound':core.rel(ymode[1][1],ymode[2][1][:,::2]),
                                     'H1_canonical_endpoint_sub2_vs_sub4_relative_diagnostic_not_bound':core.rel(ymode[2][1],ymode[4][1][:,::2]),
                                     'X10_original_H3F_knots_vs_action_sub4_relative_diagnostic_not_bound':core.rel(Xfine[::4],original_at_knots),
                                     **sampled}
                        del matrices,operator_diag,ymode
                    Xdense=np.stack([Xs[i] for i in range(6)])
                    Xxdense=np.stack([Xxs[i] for i in range(6)])
                    Ydense=np.stack([Ys[i] for i in range(6)])
                    if Ydense.shape!=(6,8,(nt-1)*4+1):
                        raise RuntimeError('D17 dense canonical H1 shape changed')
                    saved[prefix+'x_dense_sub4']=xfine
                    saved[prefix+'H1_canonical_y_dense_sub4']=Ydense
                    saved[prefix+'X10_original_action_dense_sub4']=Xdense
                    saved[prefix+'X10_x_original_action_dense_sub4']=Xxdense
                    saved[prefix+'X10_original_H3F_knots']=Xorig
                    saved[prefix+'X10_x_original_H3F_H1dot_knots']=Xxorig
                    row['mode_diagnostics']=[numeric[i] for i in range(6)]
                    row['H1_canonical_Radau_sub2_vs_sub4_relative_max_not_bound']=float(max(numeric[i]['H1_canonical_endpoint_sub2_vs_sub4_relative_diagnostic_not_bound'] for i in range(6)))
                    row['X10_original_H3F_vs_action_sub4_knots_relative_max_not_bound']=float(max(numeric[i]['X10_original_H3F_knots_vs_action_sub4_relative_diagnostic_not_bound'] for i in range(6)))
                    row['X10_source_action_dense_all_finite']=bool(np.isfinite(Xdense).all() and np.isfinite(Xxdense).all())
                    summary.append(row)
                    print(f"GE19_D17_CASE_DONE C={tag} Nt={nt} H1dense4_Xknot_vs_H3F={row['X10_original_H3F_vs_action_sub4_knots_relative_max_not_bound']:.8e}",flush=True)
                    r7._CANONICAL_LOCAL_CACHE.clear()
                    active['context']=None
        finally:
            r7._bg_point=original_bgpoint
            r7._CANONICAL_LOCAL_CACHE=original_Cmat_cache
            active['context']=None
    if len(summary)!=6 or len(saved)!=6*6+2:
        raise RuntimeError('D17 original 3C x2Nt complete source-parent scope failed')
    report={'classification':'GE19_H4F3D17_ORIGINAL_ACTION_DENSE_CANONICAL_H1_NUMERICAL_DIAGNOSTIC_PASS_TRUE_CONTINUOUS_H1_ENCLOSURE_OPEN',
            'preregistration':pre['classification'],
            'D16R1_actual_JSON_SHA256':sha(d16j),'D16R1_actual_NPZ_SHA256':sha(d16n),
            'original_source_and_parent_blobs':pins,'original_parent_SHA256':{q:sha(p) for q,p in actual.items()},
            'original_H3F_H3G_Z11_Repair13_locks':parentlocks,
            'original_action_dense_3C_x2Nt_all_6_positive_modes':True,
            'original_source_canonical_operator_PCHIP_vs_action_offknot_separate':True,
            'original_D16R1_surrogate_results_immutable':True,
            'source_action_dense_H1_substeps_preregistered':list(NSUB),
            'sampling_scope':'canonical 8D H1 Radau IIA on source-action H,Q,Z with substeps 1,2,4; midpoint residual only on sub4 fine intervals; no all-interval residual supremum',
            'true_continuous_original_H1_X10_error_enclosed':False,
            'rigorous_original_action_H1_integrator_error_enclosed':False,
            'original_GE05_bath_first_order_on_shell_certified':False,
            'full_original_H4_Ward_certified':False,'Z21_certified':False,'lensing_licensed':False,
            'original_Repair37_SCIENCE_FAIL_immutable':True,'no_observational_tuning':True,
            'claim_boundary':'Original frozen H3F initial canonical H1 state and original GE06/GE07 first-order operator are reused with an explicit independent Repair13 scalar-charge/Lambda action continuation off-grid. This D17 only diagnoses differences from original operator PCHIP, numerical H1 integration sub1/2/4, X10 and sampled ODE defects. No source-certified continuum H1 enclosure, no bath rerun, no GE05 on-shell, no H4 Ward, Z21 or lensing.',
            'rows':summary}
    oj.parent.mkdir(parents=True,exist_ok=True);on.parent.mkdir(parents=True,exist_ok=True)
    oj.write_text(json.dumps(report,sort_keys=True,indent=2,allow_nan=False)+'\n')
    np.savez_compressed(on,**saved)
    print(json.dumps(report,sort_keys=True,indent=2,allow_nan=False))

if __name__=='__main__':main()
