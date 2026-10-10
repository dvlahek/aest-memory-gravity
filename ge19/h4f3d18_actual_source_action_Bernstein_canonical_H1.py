#!/usr/bin/env python3
"""D18 actual frozen D17 H1: interval-wide AFFINE-OPERATOR surrogate residual.

D18 never treats midpoint checks of M_action-M_affine as verified suprema.
The original continuous canonical H1 remains OPEN until independently
source-certified M_action'' and outward floating/ODE error bounds are supplied.
"""
from __future__ import annotations
import argparse,hashlib,json,math,subprocess
from pathlib import Path
import numpy as np
from ge19 import h4f3d16r1_actual_original_H1dot_Hermite_physical_bath as d16r1
from ge19 import h4f3d17_original_action_dense_H1_core as d17core
from ge19 import h4f3d18_bernstein_affine_canonical_H1_core as core

ROOT=Path(__file__).resolve().parents[1]
PRE='ge19/h4f3d18_predata_source_action_bernstein_canonical_H1.json'
D17PRE='ge19/h4f3d17_predata_original_action_dense_canonical_H1.json'
CLASS='GE19_H4F3D18_ACTUAL_AFFINE_OPERATOR_BERNSTEIN_SURROGATE_PASS_ORIGINAL_ACTION_CURVATURE_AND_CONTINUUM_H1_OPEN'
TINY=1.e-300

def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--results-dir',required=True)
    ap.add_argument('--repair26-trace',required=True)
    ap.add_argument('--json-out',required=True);ap.add_argument('--npz-out',required=True)
    args=ap.parse_args()
    rd=Path(args.results_dir).resolve();trace=Path(args.repair26_trace).resolve()
    oj=Path(args.json_out).resolve();on=Path(args.npz_out).resolve()
    if oj.exists() or on.exists():raise RuntimeError('D18 refuses overwrite of existing physical result')
    pre=json.loads((ROOT/PRE).read_text())
    if pre['classification']!='GE19_H4F3D18_PREDATA_SOURCE_ACTION_AFFINE_OPERATOR_BERNSTEIN_CONDITIONAL_H1':
        raise RuntimeError('D18 preregistration changed')
    for rel,want in pre['local_sha256'].items():
        if sha(ROOT/rel)!=want:raise RuntimeError('D18 local locked source changed: '+rel)
    d17pre=json.loads((ROOT/D17PRE).read_text())
    if sha(ROOT/D17PRE)!=pre['D17_prereg_sha256']:
        raise RuntimeError('D18 D17 preregistration changed')
    for rel,want in d17pre['source_blobs'].items():
        head=subprocess.check_output(['git','rev-parse','HEAD:'+rel],cwd=ROOT,text=True).strip()
        work=subprocess.check_output(['git','hash-object',str(ROOT/rel)],cwd=ROOT,text=True).strip()
        if not(head==work==want):raise RuntimeError('D18 original source blob changed: '+rel)
    for rel,want in d17pre['local_source_SHA256'].items():
        if sha(ROOT/rel)!=want:raise RuntimeError('D18 D17 local locked source changed: '+rel)
    d16pre=json.loads((ROOT/d16r1.PRE).read_text())
    _,_,actual=d16r1.physical_input_locks(rd,trace,d16pre)
    d15=d16r1.d15;old=d15.d13.old;r7=old.r7
    paths,parentlocks=d15.parents.frozen_inputs(rd,trace)
    if not all(parentlocks[k]['exact'] for k in d15.parents.REQUIRED):
        raise RuntimeError('D18 original H3F/H3G/Z11/Repair13 parent changed')
    dj=rd/pre['D17_parents']['JSON'][0];dn=rd/pre['D17_parents']['NPZ'][0]
    if sha(dj)!=pre['D17_parents']['JSON'][1] or sha(dn)!=pre['D17_parents']['NPZ'][1]:
        raise RuntimeError('D18 original D17 numeric parent changed')
    prior=json.loads(dj.read_text())
    if (prior.get('classification')!='GE19_H4F3D17_ORIGINAL_ACTION_DENSE_CANONICAL_H1_NUMERICAL_DIAGNOSTIC_PASS_TRUE_CONTINUOUS_H1_ENCLOSURE_OPEN'
            or prior.get('true_continuous_original_H1_X10_error_enclosed') is not False
            or prior.get('original_GE05_bath_first_order_on_shell_certified') is not False):
        raise RuntimeError('D18 immutable D17 claim boundary changed')
    print('GE19_D18_FROZEN_ACTION_AND_D17_ACTUAL_SHA_PASS',flush=True)
    rows=[];saved={}
    with (np.load(paths['r13'],allow_pickle=False) as r13,
          np.load(dn,allow_pickle=False) as archive):
        bgs,_,mod6,mod7,_,_,_,_,_=old.build_context(rd,r13)
        original_bgpoint=r7._bg_point
        original_cache=r7._CANONICAL_LOCAL_CACHE
        r7._CANONICAL_LOCAL_CACHE={}
        active={'context':None}
        def true_action_point(bg,xq):
            if active['context'] is None:raise RuntimeError('D18 action case not installed')
            return active['context'](bg,xq)
        r7._bg_point=true_action_point
        try:
            for label,nt in (('primary',128),('control',64)):
                xo=np.asarray(archive['x_'+label],float)
                saved['x_'+label]=xo
                for tag in r7.C_TAGS:
                    bg=bgs[(nt,tag)]
                    if not np.array_equal(xo,np.asarray(bg['x'],float)):
                        raise RuntimeError('D18 frozen Repair13/H3F original clock changed')
                    prefix=f'{label}_{tag}_'
                    xf=np.asarray(archive[prefix+'x_dense_sub4'],float)
                    Y=np.asarray(archive[prefix+'H1_canonical_y_dense_sub4'],complex)
                    if (len(xf)!=(nt-1)*4+1 or Y.shape!=(6,8,len(xf))
                            or not np.array_equal(xf[::4],xo) or not(np.diff(xf)>0).all()):
                        raise RuntimeError('D18 actual D17 full dense H1 scope changed')
                    evalH,actiondiag=d15.clk.make_original_action_background(r7,bg,tag)
                    ctx=d17core.ActionBackground(r7,bg,evalH)
                    active['context']=ctx;ctx.knot_check()
                    nint=len(xf)-1
                    rs=np.empty((6,nint),float);ys=np.empty_like(rs)
                    ls=np.empty_like(rs);sample=np.empty_like(rs)
                    mid_actual=np.empty_like(rs);E=np.empty((6,nint+1),float)
                    Xscenario=np.empty((6,nint+1),float)
                    diagnostic=[]
                    for im,m in enumerate(np.asarray(r7.FOURIER_N,int)):
                        k=float(m*r7.g9.K_REQ[0]/r7.FOURIER_N[0])
                        Mnodes=np.empty((len(xf),8,8),complex)
                        qnodes=np.empty(len(xf),float)
                        for j,xq in enumerate(xf):
                            mq,*_=r7._canonical_operator_matrices(mod6,mod7,bg,tag,k,float(xq))
                            if not np.isfinite(mq).all():raise RuntimeError('D18 source canonical M nonfinite')
                            Mnodes[j]=mq
                            qnodes[j]=ctx(bg,float(xq))['Q_action']
                        log_e=-math.inf;E[im,0]=0.;Xscenario[im,0]=0.
                        for j in range(nint):
                            y0=Y[im,:,j];y1=Y[im,:,j+1]
                            M0=Mnodes[j];M1=Mnodes[j+1]
                            out=core.bernstein_ideal_float(xf[j],xf[j+1],y0,y1,M0,M1)
                            rs[im,j]=out['residual_poly_sup_ideal_float']
                            ys[im,j]=out['y_poly_sup_ideal_float']
                            ls[im,j]=out['operator_affine_fro_sup_ideal_float']
                            # This is the exact-input affine-operator surrogate SCENARIO.
                            # Never import E as an action-continuum error bar.
                            log_e=core.gronwall_log_step(log_e,out['h'],ls[im,j],rs[im,j])
                            E[im,j+1]=core.log10_1plus_error(log_e)
                            cx=math.hypot(max(abs(qnodes[j]),abs(qnodes[j+1])),
                                          abs(k)*math.exp(-float(xf[j])))
                            Xscenario[im,j+1]=core.log10_1plus_error(log_e+math.log(cx)) if cx else 0.
                            xm=.5*(float(xf[j])+float(xf[j+1]))
                            Mmid,*_=r7._canonical_operator_matrices(mod6,mod7,bg,tag,k,xm)
                            Maff=.5*(M0+M1)
                            dm=Mmid-Maff
                            sample[im,j]=float(np.linalg.norm(dm,ord='fro'))
                            pmid=core.exact_polynomial_residual_at(out,y0,M0,M1,.5)
                            ym=.125*out['y_bernstein'][0]+.375*out['y_bernstein'][1]+.375*out['y_bernstein'][2]+.125*out['y_bernstein'][3]
                            mid_actual[im,j]=core.norm(pmid-dm@ym)
                        diagnostic.append({'m':int(m),
                            'poly_residual_max_ideal_float':float(np.max(rs[im])),
                            'affine_operator_fro_max_ideal_float':float(np.max(ls[im])),
                            'source_action_M_mid_vs_affine_fro_sampled_max_NOT_BOUND':float(np.max(sample[im])),
                            'actual_action_midpoint_residual_L2_max_sampled_NOT_BOUND':float(np.max(mid_actual[im])),
                            'conditional_affine_only_H1_state_error_log10_1plus_scenario_NOT_ACTION_BOUND':float(E[im,-1]),
                            'conditional_affine_only_X10_projection_log10_1plus_scenario_NOT_ACTION_BOUND':float(np.max(Xscenario[im]))})
                        r7._CANONICAL_LOCAL_CACHE.clear()
                    if not all(np.isfinite(v).all() for v in (rs,ys,ls,sample,mid_actual,E,Xscenario)):
                        raise RuntimeError('D18 nonfinite computed surrogate diagnostics')
                    saved[prefix+'x_dense_sub4']=xf
                    for key,arr in (('r_bernstein_affine_ideal_float',rs),
                        ('y_bernstein_affine_ideal_float',ys),('M_affine_fro_ideal_float',ls),
                        ('action_Mmid_minus_affine_sampled_NOT_BOUND',sample),
                        ('action_midpoint_canonical_defect_sampled_NOT_BOUND',mid_actual),
                        ('conditional_affine_only_state_error_LOG10_1PLUS_NOT_ACTION_BOUND',E),
                        ('conditional_affine_only_X10_projection_LOG10_1PLUS_NOT_ACTION_BOUND',Xscenario)):
                        saved[prefix+key]=arr
                    rows.append({'C':tag,'Nt':nt,'six_original_positive_modes':list(map(int,r7.FOURIER_N)),
                        'n_D17_fine_intervals':nint,
                        'action_background_original_source_knots':actiondiag,
                        'all_fine_intervals_polynomial_Bernstein_controls_computed':True,
                        'source_action_second_derivative_operator_sup_enclosed':False,
                        'numerical_float_rounding_outward_enclosed':False,
                        'true_original_continuum_H1_error_enclosed':False,
                        'mode_diagnostics':diagnostic})
                    print('GE19_D18_CASE_DONE C='+tag+' Nt='+str(nt)+
                        ' polyR_max='+f'{np.max(rs):.6e}'+
                        ' source_Mmid_sampled_max='+f'{np.max(sample):.6e}',flush=True)
                    active['context']=None
        finally:
            r7._bg_point=original_bgpoint
            r7._CANONICAL_LOCAL_CACHE=original_cache
            active['context']=None
    if len(rows)!=6 or len(saved)!=2+6*8:
        raise RuntimeError('D18 original 3C x2Nt scope incomplete')
    report={
      'classification':CLASS,
      'preregistration':pre['classification'],
      'D17_original_actual_JSON_SHA256':sha(dj),'D17_original_actual_NPZ_SHA256':sha(dn),
      'original_D13_D14_D16R1_parent_SHA256':{k:sha(p) for k,p in actual.items()},
      'original_parent_locks':parentlocks,
      'original_action_operator_frozen_GE06_GE07':True,
      'all_six_original_H1_modes_and_3C_x2Nt':True,
      'polynomial_residual_Bernstein_convex_hull_formula_exact_algebra':True,
      'float64_bernstein_arithmetic_outward_enclosed':False,
      'source_action_M_second_derivative_sup_enclosed':False,
      'source_action_M_minus_affine_sup_enclosed':False,
      'source_action_M_midpoint_differences_only_sampled_NOT_BOUND':True,
      'reported_affine_only_H1_error_is_counterfactual_log10_1plus_scenario_NOT_action_bound':True,
      'rigorous_original_action_continuous_H1_X10_enclosed':False,
      'original_GE05_bath_first_order_on_shell_certified':False,
      'full_original_H4_Ward_certified':False,
      'Z21_certified':False,'lensing_licensed':False,
      'original_Repair37_SCIENCE_FAIL_immutable':True,
      'no_observational_tuning':True,
      'claim_boundary':'Bernstein control norms bound the ideal exact-arithmetic quartic residual for the LINEAR-ENDPOINT-MATRIX surrogate on each D17 fine interval. Recorded float64 numbers are not outward rounded. The actual original-action operator deviates from that affine surrogate by an UNKNOWN all-interval amount; midpoint differences are not upper bounds. Affine-only Gronwall profile is only a counterfactual scenario. No true continuous H1/X10 enclosure, numerical rounding certificate, original GE05 bath on-shell, H4 Ward, Z21 or lensing.',
      'missing_source_certificates':[
          'source-verified all-interval sup ||M_action_xx|| per fine interval (or direct validated interval M-Maff enclosure)',
          'outward-rounded canonical matrix and Bernstein coefficient arithmetic',
          'rigorous initial-state error if initial parent has only numerical rather than interval-certified state',
          'propagated continuous H1 and X10_x error into original GE05 bath with time-quadrature bounds'],
      'rows':rows}
    oj.parent.mkdir(parents=True,exist_ok=True);on.parent.mkdir(parents=True,exist_ok=True)
    oj.write_text(json.dumps(report,sort_keys=True,indent=2,allow_nan=False)+'\n')
    np.savez_compressed(on,**saved)
    print('GE19_D18_SURROGATE_BERNSTEIN_ALL_INTERVALS_PASS_TRUE_ACTION_H1_AND_GE05_OPEN',flush=True)

if __name__=='__main__':main()
