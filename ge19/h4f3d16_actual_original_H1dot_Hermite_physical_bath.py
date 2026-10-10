#!/usr/bin/env python3
"""D16 actual original parent-locked conditional physical-clock GE05 bath bridge.

This is a SURROGATE driven by cubic Hermite of original H3F H1/H1dot
endpoints. It is not a certified original continuous-H1 bath on-shell solve.
"""
from __future__ import annotations
import argparse,hashlib,json,subprocess
from pathlib import Path
import numpy as np
from ge19 import h4f3d15a_actual_original_R1_clock_conditional as d15
from ge19 import h4f3d16_original_H1dot_Hermite_physical_bath_core as core

ROOT=Path(__file__).resolve().parents[1]
PRE='ge19/h4f3d16_predata_original_H1dot_Hermite_physical_bath_bridge.json'
SOURCE='ge19/h4f3d16_original_H1dot_Hermite_physical_bath_core.py'
PARENT={
 'D15A_JSON':('ge19_h4f3d15a_actual_original_R1_clock_conditional.json','cad2a1c548582177d49019153fab34aa5b0ab520c7dd62f361c9e780af22794d'),
 'D15A_NPZ':('ge19_h4f3d15a_actual_original_R1_clock_conditional.npz','f7f9c94a341ec514d7d97ade297097b29102754231746531cde4485b61b2273c')}
N_SUB=(4,8,16)
TINY=1e-300

def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for q in iter(lambda:f.read(1<<20),b''): h.update(q)
 return h.hexdigest()

def rel(a,b):return core.rel(a,b)
def l2(a):return core.l2(a)
def weighted(w,z):return np.einsum('n,nmt->mt',w,z,optimize=True)

def physical_input_locks(rd,trace,pre):
 if pre.get('classification')!='GE19_H4F3D16_PREDATA_ORIGINAL_H1DOT_HERMITE_TRUE_ACTION_CLOCK_BATH_SURROGATE_DIAGNOSTIC':
  raise RuntimeError('D16 preregistration classification changed')
 d15pins=d15.physical_source_locks()
 for rel,want in pre['original_source_blobs'].items():
  head=subprocess.check_output(['git','rev-parse','HEAD:'+rel],cwd=ROOT,text=True).strip()
  work=subprocess.check_output(['git','hash-object',str(ROOT/rel)],cwd=ROOT,text=True).strip()
  if head!=want or work!=want:raise RuntimeError('D16 original source changed: '+rel)
 raw,actual=d15.original_physical_files(rd,trace)
 for name,(filename,want) in PARENT.items():
  p=rd/filename
  if not p.is_file() or sha(p)!=want:raise RuntimeError('D16 original D15a actual parent changed: '+name)
 if sha(trace)!=pre['frozen_parents_SHA256']['Repair26_R1_trace']:
  raise RuntimeError('D16 original Repair26 trace SHA changed')
 for name,path in actual.items():
  if sha(path)!=pre['frozen_parents_SHA256'][name]:
   raise RuntimeError('D16 D13/D14 actual SHA changed: '+name)
 return d15pins,raw,actual

def main():
 ap=argparse.ArgumentParser()
 ap.add_argument('--results-dir',required=True);ap.add_argument('--repair26-trace',required=True)
 ap.add_argument('--json-out',required=True);ap.add_argument('--npz-out',required=True)
 args=ap.parse_args()
 rd=Path(args.results_dir).resolve();trace=Path(args.repair26_trace).resolve()
 oj=Path(args.json_out).resolve();on=Path(args.npz_out).resolve()
 if oj.exists() or on.exists():raise RuntimeError('D16 refuses overwrite')
 pre=json.loads((ROOT/PRE).read_text())
 d15pins,raw,actual=physical_input_locks(rd,trace,pre)
 paths,parentlocks=d15.parents.frozen_inputs(rd,trace)
 if not all(parentlocks[k]['exact'] for k in d15.parents.REQUIRED):
  raise RuntimeError('D16 original H3F/Repair13/H3G/Z11 source parent changed')
 d15_json=json.loads((rd/PARENT['D15A_JSON'][0]).read_text())
 if (d15_json.get('classification')!='GE19_H4F3D15A_ACTUAL_ORIGINAL_GE05_X_EMBEDDED_CLOCK_CONDITIONAL_COLLOCATION_PASS_CONTINUOUS_X10_OPEN'
     or d15_json.get('actual_true_continuous_X10_drive_enclosed') is not False):
  raise RuntimeError('D16 D15a source parent claims changed')
 r24=d15.d13.old.r24;r7=d15.d13.old.r7;c4=d15.d13.old.c4
 tau=r24.TAUH0/float(r7.g9.H0_CLASS)
 kfund=float(r7.g9.K_REQ[0]/r7.FOURIER_N[0])
 boundaries={n:r24.full_history_boundary(c4,r7,trace,n) for n in (2048,1024)}
 report_rows=[];saved={};bg_rows=[];cross=[]
 with (np.load(paths['r13'],allow_pickle=False) as r13,
       np.load(paths['h3fn'],allow_pickle=False) as h3f,
       np.load(actual['D13_NPZ'],allow_pickle=False) as d13npz,
       np.load(rd/PARENT['D15A_NPZ'][0],allow_pickle=False) as d15npz):
  bgs,_,_,_,_,_,_,_,_=d15.d13.old.build_context(rd,r13)
  xs={lab:np.asarray(h3f['x_'+lab],float) for lab in ('primary','control')}
  for label,nt in (('primary',128),('control',64)):
   x=xs[label]
   if x.shape!=(nt,) or not np.array_equal(x,np.asarray(d13npz['x_'+label])):
    raise RuntimeError('D16 frozen original H1/D13 time grid changed')
   saved['x_'+label]=x
   for tag in r7.C_TAGS:
    bg=bgs[(nt,tag)];a=np.asarray(bg['a'],float);H=np.asarray(bg['H'],float)
    H1=np.asarray(h3f[f'{tag}_H1_{label}'],complex)
    H1dot=np.asarray(h3f[f'{tag}_H1dot_{label}'],complex)
    X,Xx=core.frozen_endpoint_X_Xx(r7,bg,H1,H1dot)
    Xorig=r24.first_order_X_modes(r7,bg,H1)
    xendpoint=rel(X,Xorig)
    if xendpoint>1e-13:raise RuntimeError('D16 original H1 endpoint X changed')
    evalH,bgdiag=d15.clk.make_original_action_background(r7,bg,tag)
    tagprefix=f'{label}_{tag}_'
    saved[tagprefix+'original_X10_H1_endpoint']=X
    saved[tagprefix+'original_X10_x_derivative_from_H1dot']=Xx
    saved[tagprefix+'original_X10_Hermite_midpoint']=core.evaluate_hermite(
     X,Xx,x,np.arange(nt-1),np.full(nt-1,.5))[0]
    linear_mid=.5*(X[:,:-1]+X[:,1:])
    hermite_mid_deviation=core.rel(saved[tagprefix+'original_X10_Hermite_midpoint'],linear_mid)
    bg_rows.append({'C':tag,'Nt':nt,'original_H1_X_endpoint_relative_machine':xendpoint,
     'original_action_background':bgdiag,
     'original_X10_Hermite_mid_vs_original_linear_relative_diagnostic':hermite_mid_deviation})
    # First-order H1 solve is independently executed on original Nt128/Nt64.
    # Non-nested grid cross-comparison is an empirical diagnostic, not a
    # bound on either continuum H1 solution.
    if label=='control':
     xf=xs['primary'];fX=saved[f'primary_{tag}_original_X10_H1_endpoint']
     fDx=saved[f'primary_{tag}_original_X10_x_derivative_from_H1dot']
     i=np.clip(np.searchsorted(xf,x,side='right')-1,0,len(xf)-2)
     theta=(x-xf[i])/(xf[i+1]-xf[i])
     xf_at_control,_=core.evaluate_hermite(fX,fDx,xf,i,theta)
     cross.append({'C':tag,'Nt128_Hermite_evaluated_at_Nt64_vs_original_Nt64_X10_relative_report_only':rel(xf_at_control,X),
      'absolute_L2_report_only':l2(xf_at_control-X)})
    for nq in (2048,1024):
     bd=boundaries[nq];r=np.asarray(bd['r'],float);w=np.asarray(bd['w'],float)
     if r.shape!=(nq,) or w.shape!=(nq,):raise RuntimeError('D16 original Nq boundary changed')
     prefix=f'{label}_{tag}_Nq{nq}_'
     # Verify D15a physical gamma exactly at the original theta=0 nodes.
     hmid=tau*np.sqrt(H[:-1]*H[1:])
     gamma=tau*H[:-1]/hmid
     if not np.allclose(gamma,np.asarray(d15npz[prefix+'theta0_gamma'],float),rtol=1e-13,atol=1e-14):
      raise RuntimeError('D16 physical D15a original action clock source mismatch')
     z0=np.asarray(bd['z0'],complex);v0=np.asarray(bd['v0'],complex)
     cases={}
     for sub in N_SUB:
      zsub,vsub,hl,hr=core.propagate_physical(x,X,Xx,evalH,z0,v0,r,tau,
       r24.step_linear_nd,sub,'hermite')
      cases[sub]=(zsub,vsub,hl,hr)
      saved[prefix+f'weighted_z_Hermite_physical_sub{sub}']=weighted(w,zsub)
      saved[prefix+f'weighted_v_Hermite_physical_sub{sub}']=weighted(w,vsub)
     (z4,v4,_,_)=cases.pop(4)
     (z8,v8,_,_)=cases.pop(8)
     (z16,v16,hl16,hr16)=cases.pop(16)
     d48z=rel(z4,z8);d48v=rel(v4,v8)
     del z4,v4
     d816z=rel(z8,z16);d816v=rel(v8,v16)
     d816zabs=l2(z8-z16);d816vabs=l2(v8-v16)
     phases=np.asarray(d13npz[prefix+'left_original_interval_phase'],float)
     if phases.shape!=(nq,nt-1):raise RuntimeError('D16 original R1 high-phase map changed')
     high=phases>=np.pi
     high_nodes=int(high.sum())
     z8high=np.where(high[:,None,:],z8[:,:,1:],0)
     z16high=np.where(high[:,None,:],z16[:,:,1:],0)
     v8high=np.where(high[:,None,:],v8[:,:,1:],0)
     v16high=np.where(high[:,None,:],v16[:,:,1:],0)
     high_dz=l2(z16high-z8high)/max(l2(z16high),l2(z8high),TINY)
     high_dv=l2(v16high-v8high)/max(l2(v16high),l2(v8high),TINY)
     del z8,v8,z8high,z16high,v8high,v16high
     zlinear,vlinear,_,_=core.propagate_physical(x,X,Xx,evalH,z0,v0,r,tau,
      r24.step_linear_nd,16,'linear')
     change_drive_z=rel(z16,zlinear);change_drive_v=rel(v16,vlinear)
     saved[prefix+'weighted_z_physical_original_Xlinear_sub16']=weighted(w,zlinear)
     saved[prefix+'weighted_v_physical_original_Xlinear_sub16']=weighted(w,vlinear)
     zR1,vR1=r24.evolve_z10(c4,bg,X,z0,v0,r,tau)
     clock_z=rel(zlinear,zR1);clock_v=rel(vlinear,vR1)
     source_W={}
     for side,hs in (('left',hl16),('right',hr16)):
      W,U=core.signed_one_sided_endpoint_W(z16,v16,a,H,hs,r,w,tau,kfund,
       d15.d13.d6.ward_signed_convolution,d15.clk.unsigned_signed_pair_envelope,side)
      saved[prefix+f'physical_Hermite_sub16_{side}_signed_W_clock_ODE']=W
      saved[prefix+f'physical_Hermite_sub16_{side}_unsigned_W_clock_ODE_envelope']=U
      source_W[side]={'signed_W_clock_L2_report_only':l2(W),
       'unsigned_W_clock_envelope_L2_report_only':l2(U),
       'envelope_pass':bool(np.all(np.abs(W)<=U*(1+1e-10)+1e-25))}
     saved[prefix+'original_R1_H1drive_weighted_z']=weighted(w,zR1)
     saved[prefix+'original_R1_H1drive_weighted_v']=weighted(w,vR1)
     # All 12 cohorts have per-mode/time source-weighted states. Full
     # node states of ONLY original primary Cstar Nq2048 retained to enable
     # a bounded-size independent raw node-state spot audit.
     if label=='primary' and tag=='C_star' and nq==2048:
      saved[prefix+'node_z_Hermite_physical_sub16']=z16
      saved[prefix+'node_v_Hermite_physical_sub16']=v16
     report_rows.append({'C':tag,'Nt':nt,'Nq':nq,
      'original_R1_H1_endpoints_and_action_clock_reproduced':True,
      'original_H1_X_endpoint_relative_machine':xendpoint,
      'Hermite_drive_midpoint_vs_linear_relative_report_only':hermite_mid_deviation,
      'Hermite_physical_z_sub4_vs_sub8_relative_report_only':d48z,
      'Hermite_physical_v_sub4_vs_sub8_relative_report_only':d48v,
      'Hermite_physical_z_sub8_vs_sub16_relative_report_only':d816z,
      'Hermite_physical_v_sub8_vs_sub16_relative_report_only':d816v,
      'Hermite_physical_z_sub8_vs_sub16_absolute_L2_report_only':d816zabs,
      'Hermite_physical_v_sub8_vs_sub16_absolute_L2_report_only':d816vabs,
      'original_high_phase_ge_pi_node_steps':high_nodes,
      'original_high_phase_ge_pi_node_step_fraction':float(high.mean()),
      'high_phase_ge_pi_z_sub8_vs_sub16_relative_report_only_not_error_bar':high_dz,
      'high_phase_ge_pi_v_sub8_vs_sub16_relative_report_only_not_error_bar':high_dv,
      'physical_clock_Hermite_vs_original_linear_z_relative_report_only':change_drive_z,
      'physical_clock_Hermite_vs_original_linear_v_relative_report_only':change_drive_v,
      'original_linear_physical_clock_vs_frozen_R1_z_relative_report_only':clock_z,
      'original_linear_physical_clock_vs_frozen_R1_v_relative_report_only':clock_v,
      'one_sided_original_GE05_bath_signed_source':source_W,
      'physical_time_v_continuously_propagated_without_original_R1_x_embedding_impulse':True,
      'true_continuous_original_X10_enclosed':False,
      'original_GE05_first_order_bath_on_shell_certified':False})
     del z16,v16,zlinear,vlinear,zR1,vR1
  if len(report_rows)!=12 or len(cross)!=3 or not all(np.isfinite(q).all() for q in saved.values()):
   raise RuntimeError('D16 original physical C/Nt/Nq output scope invalid')
  # Source and original quadrature comparisons are diagnostics, not rigorous
  # error estimates: independent node sets cannot be paired pointwise.
  qdiag=[]
  for label,nt in (('primary',128),('control',64)):
   for tag in r7.C_TAGS:
    ka=f'{label}_{tag}_Nq2048_weighted_z_Hermite_physical_sub16'
    kb=f'{label}_{tag}_Nq1024_weighted_z_Hermite_physical_sub16'
    qa=saved[ka];qb=saved[kb]
    qdiag.append({'C':tag,'Nt':nt,'Nq2048_vs_Nq1024_Hermite16_weighted_z_relative_report_only':rel(qa,qb),
     'absolute_L2_report_only':l2(qa-qb)})
  rep={'classification':'GE19_H4F3D16_ACTUAL_ORIGINAL_H1DOT_HERMITE_PHYSICAL_CLOCK_BATH_SURROGATE_DIAGNOSTIC_PASS_TRUE_X10_ONSHELL_OPEN',
   'preregistration':pre['classification'],'source_SHA256':sha(ROOT/SOURCE),
   'predata_SHA256':sha(ROOT/PRE),'original_frozen_source_locks':d15pins,
   'original_parent_SHA256':{k:sha(p) for k,p in actual.items()},
   'D15A_actual_JSON_SHA256':sha(rd/PARENT['D15A_JSON'][0]),
   'D15A_actual_NPZ_SHA256':sha(rd/PARENT['D15A_NPZ'][0]),
   'Repair26_trace_SHA256':sha(trace),'original_H3F_H3G_Z11_Repair13_locks':parentlocks,
   'original_cohorts_all_12_saved':len(report_rows)==12,
   'original_H1dot_endpoint_source_derivatives_used':True,
   'original_action_physical_time_substeps_integrated':True,
   'numerical_substeps_preregistered':list(N_SUB),
   'original_high_phase_nodes_all_propagated':True,
   'original_x_embedded_R1_artificial_internal_impulses_not_imported_into_physical_time_substep_state':True,
   'true_continuous_original_X10_error_enclosed':False,
   'true_original_GE05_bath_first_order_on_shell_certified':False,
   'rigorous_numerical_time_quadrature_enclosure_certified':False,
   'external_original_action_boundary_and_full_GE05_Noether_certified':False,
   'original_full_H4_Ward_certified':False,'Z21_certified':False,
   'lensing_licensed':False,'original_Repair37_SCIENCE_FAIL_immutable':True,'no_observational_tuning':True,
   'claim_boundary':'D16 propagates original Repair26 bath initial data using original action H(x), original Repair24 exact frozen step kernel and true physical action-clock increments with endpoint-H1dot-matched cubic Hermite surrogate drive. The numerical physical-time z/v is continuous at each knot, but H1 Hermite interpolation error and finite-substep true continuous-bath residual are not certified. Signed one-sided endpoint W and unsigned envelope report finite-substep residual only; 4/8/16, nonnested quadrature and high-phase differences are empirical diagnostics. No original GE05 bath on-shell, H4 Ward, Z21, lensing or observable fitting.',
   'original_action_and_H1_source_rows':bg_rows,
   'Nt128_vs_Nt64_X10_cross_grid_diagnostics':cross,
   'Nq2048_vs_Nq1024_weighted_z_diagnostics':qdiag,
   'rows':report_rows}
  oj.parent.mkdir(parents=True,exist_ok=True);on.parent.mkdir(parents=True,exist_ok=True)
  oj.write_text(json.dumps(rep,indent=2,sort_keys=True,allow_nan=False)+'\n')
  np.savez_compressed(on,**saved)
  print(json.dumps(rep,indent=2,sort_keys=True,allow_nan=False))

if __name__=='__main__':main()
