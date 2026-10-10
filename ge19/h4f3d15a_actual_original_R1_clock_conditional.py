#!/usr/bin/env python3
"""GE19 D15a physical conditional GE05 clock audit on original frozen R1.

Recomputes the original Repair26 R1 bath states, validates original actual
D13/D14 physical archives and source blobs, evaluates the action-derived
continuous Repair13 background H(x), H_x(x), and exact original R1 field
embedded as z_step(x) at frozen collocation theta=0,1/2,1. The interior
continuous original H1 drive Xtrue(x) is UNKNOWN: U_X is only a conditional
coefficient for its error and there is no certified GE05 on-shell claim.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess
from pathlib import Path
import numpy as np
from ge19 import h4f3d13_actual_original_r1_signed_interval_bath_parent as d13
from ge19 import h4f3d14_actual_original_r1_source_weighted_phase_bath as d14
from ge19 import h4f3d15a_original_GE05_clock_embedded_source as clk
from ge19 import h4f3d15a1_original_GE05_interface_current_jump as iface
from ge19 import h4f3b_actual_corrected_six_piece_source as parents

ROOT=Path(__file__).resolve().parents[1]
PRE='c5cb22394dc8eabf12c9fe8d5f6acd57a24d90f356976122864723ec73513745'
SOURCE='14da31797282fb7959c44793f04751f1dd0ff25765424e566ca6015e759a82ae'
PREPATH='ge19/h4f3d15a_predata_original_GE05_clock_consistent_conditional_collocation.json'
SOURCEPATH='ge19/h4f3d15a_original_GE05_clock_embedded_source.py'
IFACEPRE='da56f2c42e11ce480ee72a888f725d422c71a2e7a3c2c19d8b19cabda752874c'
IFACESOURCE='d5e55055348cfeb9462d566d436e91da563d77c7b3f6d36b914a73c7711cce2c'
IFACEPREPATH='ge19/h4f3d15a1_predata_original_GE05_interface_current_jump.json'
IFACESOURCEPATH='ge19/h4f3d15a1_original_GE05_interface_current_jump.py'
SHA_D13_J='2b4dfbd30ec6466292e0dcf62eeed8b723555d1890a127a5e0a6ff761d2ebe76'
SHA_D13_N='1608fe98dd924b2b235ecf0f8fce768f2f3a2fa4a2854de04a56fe622ad3df89'
SHA_D14_J='8d8244cf810447c96df82f6ece6c161a4dd0553f707e3a698ed0b29f37ff3c6e'
SHA_D14_N='f79d87f10dc1561ef2c61997b7952d62d85eda6674abaa015e5d38e161b55c48'
ORIGINAL_PINS={
 'ge05/memory_directional_source_generator.py':'40837d77f89028da30c28899e2d0530a4401844e',
 'ge19/repair13_self_consistent_reduced_background_h1_reclosure.py':'362d63d03d7b850fceae393f535353ded79aeea7',
 'ge19/repair07_window_retarded_reduced_h3_z20_particular.py':'e34d28a2062c748f48bc82fa928844b02631de25',
 'ge19/repair24_q20_construction.py':'fc271987d1bddcd023cc9c057ddcad036b1d72fb',
 'ge19/h4f3d13_actual_original_r1_signed_interval_bath_parent.py':'5cce06a82869d5b7ff70c12a92e70b9257073c42',
 'ge19/h4f3d14_actual_original_r1_source_weighted_phase_bath.py':'cb823960e9b2cf1b82b1accd458ec75f4acf4547',
 'ge19/h4f3d14_actual_original_r1_source_weighted_phase_bath_independent_archive_audit.json':'3f7acc17aee24c6b776578ef2b654a40b2db6af0',
}
THETAS=(0.,.5,1.)
TINY=1e-300

def sha256(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for chunk in iter(lambda:f.read(1<<20),b''):
   h.update(chunk)
 return h.hexdigest()

def physical_source_locks():
 out={}
 for rel, expected in ORIGINAL_PINS.items():
  head=subprocess.check_output(['git','rev-parse','HEAD:'+rel],cwd=ROOT,text=True).strip()
  work=subprocess.check_output(['git','hash-object',str(ROOT/rel)],cwd=ROOT,text=True).strip()
  if head!=expected or work!=expected:
   raise RuntimeError('D15a original action/parent blob changed: '+rel)
  out[rel]=expected
 for rel,want in ((PREPATH,PRE),(SOURCEPATH,SOURCE),
                 (IFACEPREPATH,IFACEPRE),(IFACESOURCEPATH,IFACESOURCE)):
  got=sha256(ROOT/rel)
  if got!=want:
   raise RuntimeError('D15a new predata/source hash mismatch: '+rel)
  out[rel+'_SHA256']=got
 out['D13_original_source_blobs']=d13.locks()
 return out

def clock_slip(evaluate,x,hmid,tau):
 """Compare original R1 hmid clock to original analytic Repair13 H(x).

 8/16 Gaussian estimates are diagnostics, not rigorous quadrature enclosure.
 """
 dx=np.diff(np.asarray(x,float))
 midpoint=(np.asarray(x[:-1])+np.asarray(x[1:]))/2
 row={}
 for n in (8,16):
  nodes,weights=np.polynomial.legendre.leggauss(n)
  xnodes=midpoint[:,None]+dx[:,None]*nodes[None,:]/2
  H,_=evaluate(xnodes)
  step_true=(dx/2)*np.einsum('ij,j->i',1/(tau*H),weights,optimize=True)
  row[n]=step_true
 step_R1=dx/hmid
 return {
  'original_R1_delta_s':step_R1,
  'original_action_delta_s_Gauss8':row[8],
  'original_action_delta_s_Gauss16':row[16],
  'original_action_Gauss16_minus_R1_delta_s':row[16]-step_R1,
  'original_action_Gauss16_minus_Gauss8_report_only':row[16]-row[8],
  'original_action_cumulative_Gauss16_minus_R1_delta_s':np.cumsum(row[16]-step_R1),
 }

def step_at_fraction(r24,z,v,X,x,hmid,r,theta):
 """RECONSTRUCT frozen original R1 state, no alternate bath solver."""
 if theta==0.:
  return z[:,:,:-1],v[:,:,:-1]
 if theta==1.:
  return z[:,:,1:],v[:,:,1:]
 if theta!=.5:
  raise ValueError('D15a unregistered original R1 collocation fraction')
 ni=len(x)-1; nm=X.shape[0];nq=len(r)
 zz=np.empty((nq,nm,ni),complex);vv=np.empty_like(zz)
 for i in range(ni):
  xi=X[:,i];Xmid=xi+theta*(X[:,i+1]-xi)
  delta_s=theta*(x[i+1]-x[i])/hmid[i]
  zz[:,:,i],vv[:,:,i]=r24.step_linear_nd(
   z[:,:,i],v[:,:,i],r,float(hmid[i]),
   np.broadcast_to(xi,(nq,nm)),np.broadcast_to(Xmid,(nq,nm)),
   float(delta_s))
 return zz,vv

def original_physical_files(rd,trace):
 raw=d13.original_physical_inputs(rd,trace)
 actual={
  'D13_JSON':(rd/'ge19_h4f3d13_actual_original_r1_signed_interval_bath_parent.json',SHA_D13_J),
  'D13_NPZ':(rd/'ge19_h4f3d13_actual_original_r1_signed_interval_bath_parent.npz',SHA_D13_N),
  'D14_JSON':(rd/'ge19_h4f3d14_actual_original_r1_source_weighted_phase_bath.json',SHA_D14_J),
  'D14_NPZ':(rd/'ge19_h4f3d14_actual_original_r1_source_weighted_phase_bath.npz',SHA_D14_N),
 }
 for label,(path,want) in actual.items():
  if not path.is_file() or sha256(path)!=want:
   raise RuntimeError('D15a actual original R1/D13/D14 parent SHA mismatch: '+label)
 return raw,{key:path for key,(path,_) in actual.items()}

def main():
 ap=argparse.ArgumentParser()
 ap.add_argument('--results-dir',required=True)
 ap.add_argument('--repair26-trace',required=True)
 ap.add_argument('--json-out',required=True)
 ap.add_argument('--npz-out',required=True)
 args=ap.parse_args()
 rd=Path(args.results_dir).resolve(); trace=Path(args.repair26_trace).resolve()
 outj=Path(args.json_out).resolve();outn=Path(args.npz_out).resolve()
 if outj.exists() or outn.exists():
  raise RuntimeError('D15a refuses overwrite of any previous original physical output')
 pre=json.loads((ROOT/PREPATH).read_text())
 if pre['classification']!='GE19_H4F3D15A_PREDATA_ORIGINAL_GE05_CLOCK_CONSISTENT_X_EMBEDDED_R1_CONDITIONAL_COLLOCATION':
  raise RuntimeError('D15a original preregistration mismatch')
 ifacepre=json.loads((ROOT/IFACEPREPATH).read_text())
 if ifacepre['classification']!='GE19_H4F3D15A1_PREDATA_ORIGINAL_GE05_X_EMBEDDED_R1_INTERNAL_INTERFACE_CURRENT_JUMP':
  raise RuntimeError('D15a1 original interface preregistration mismatch')
 pins=physical_source_locks()
 raw,actual=original_physical_files(rd,trace)
 parent_paths,parent_locks=parents.frozen_inputs(rd,trace)
 if not all(parent_locks[key]['exact'] for key in parents.REQUIRED):
  raise RuntimeError('D15a original frozen H3F/H3G/Z11/Repair13 input mismatch')
 previous_j=json.loads(actual['D14_JSON'].read_text())
 if (previous_j.get('classification')!='GE19_H4F3D14_ACTUAL_ORIGINAL_R1_SOURCE_WEIGHTED_PHASE_BATH_DIAGNOSTIC_PASS_ONSHELL_OPEN'
     or len(previous_j.get('rows',[]))!=12):
  raise RuntimeError('D15a original D14 physical classification/rows changed')
 saved={};rows=[]
 with (np.load(parent_paths['r13'],allow_pickle=False) as r13,
       np.load(parent_paths['h3fn'],allow_pickle=False) as h3f,
       np.load(raw['source_n'],allow_pickle=False) as source_npz,
       np.load(actual['D13_NPZ'],allow_pickle=False) as prev13,
       np.load(actual['D14_NPZ'],allow_pickle=False) as prev14):
  bgs,_,_,_,_,_,_,_,_=d13.old.build_context(rd,r13)
  r24=d13.old.r24
  boundaries={n:r24.full_history_boundary(d13.old.c4,d13.old.r7,trace,n)
              for n in (2048,1024)}
  tau=r24.TAUH0/float(d13.old.r7.g9.H0_CLASS)
  kfund=float(d13.old.r7.g9.K_REQ[0]/d13.old.r7.FOURIER_N[0])
  for nt,label in ((128,'primary'),(64,'control')):
   x=np.asarray(source_npz['x_'+label],float)
   if not np.array_equal(x,np.asarray(h3f['x_'+label],float)) or x.shape!=(nt,):
    raise RuntimeError('D15a original H3F and six-source x clocks changed')
   saved['x_'+label]=x
   for tag in d13.old.r7.C_TAGS:
    bg=bgs[(nt,tag)]
    if not np.array_equal(x,np.asarray(bg['x'],float)):
     raise RuntimeError('D15a frozen Repair13 original action x clock changed')
    a=np.asarray(bg['a'],float);H=np.asarray(bg['H'],float)
    bg_eval,bgdiag=clk.make_original_action_background(d13.old.r7,bg,tag)
    hmid=tau*np.sqrt(H[:-1]*H[1:])
    slip=clock_slip(bg_eval,x,hmid,tau)
    for name,value in slip.items():
     saved[f'{label}_{tag}_{name}']=value
    H1=np.asarray(h3f[f'{tag}_H1_{label}'],complex)
    X=r24.first_order_X_modes(d13.old.r7,bg,H1)
    scope={}
    for nq in (2048,1024):
     boundary=boundaries[nq]
     r=np.asarray(boundary['r'],float);w=np.asarray(boundary['w'],float)
     if r.shape!=(nq,) or w.shape!=(nq,):
      raise RuntimeError('D15a original R1 quadrature scope changed')
     z,v=r24.evolve_z10(d13.old.c4,bg,X,boundary['z0'],boundary['v0'],r,tau)
     orig,diag=d13.signed.interval_signed(z,v,X,a,H,x,r,w,tau,kfund,
                                           d13.d6.fd4,d13.d6.ward_signed_convolution)
     prefix=f'{label}_{tag}_Nq{nq}_'
     prev_fd=np.asarray(prev13[prefix+'FD4_original_signed_W'],complex)
     parent_rel=clk.relative(orig['FD4_original_signed_W'],prev_fd)
     prior_phase=np.asarray(prev13[prefix+'left_original_interval_phase'],float)
     prior14_phase=np.asarray(prev14[prefix+'original_interval_phase'],float)
     if (parent_rel>1e-10 or not np.array_equal(orig['left_original_interval_phase'],prior_phase)
         or not np.array_equal(prior_phase,prior14_phase)):
      raise RuntimeError('D15a original D13/D14 source or exact original phase changed')
     # Check actual original step at theta=1 independently from the right endpoint.
     endpoint_step=np.empty_like(z[:,:,1:]);endpoint_v=np.empty_like(v[:,:,1:])
     for i in range(nt-1):
      endpoint_step[:,:,i],endpoint_v[:,:,i]=r24.step_linear_nd(
       z[:,:,i],v[:,:,i],r,float(hmid[i]),
       np.broadcast_to(X[:,i],(nq,len(clk.MODES))),
       np.broadcast_to(X[:,i+1],(nq,len(clk.MODES))),
       float((x[i+1]-x[i])/hmid[i]))
     endpoint_rel=max(clk.relative(endpoint_step,z[:,:,1:]),
                      clk.relative(endpoint_v,v[:,:,1:]))
     if endpoint_rel>1e-11:
      raise RuntimeError('D15a frozen original Repair24 propagator failed endpoint identity')
     # The x-embedded R1 physical z_t has two gamma values at every
     # internal knot. Preserve its ORIGINAL ACTION delta(t-t_i) term;
     # its coefficient has different units from the smooth sampled W.
     H_knots,_=bg_eval(x)
     jump=iface.original_GE05_interior_current_jump(
      z,v,a,H_knots,hmid,r,w,tau,kfund,d13.d6.ward_signed_convolution)
     for name,value in jump.items():
      if isinstance(value,np.ndarray):
       saved[prefix+name]=value
     theta_rows=[];theta_results={}
     for theta,short in ((0.,'theta0'),(.5,'theta05'),(1.,'theta1')):
      ztheta,vtheta=step_at_fraction(r24,z,v,X,x,hmid,r,theta)
      xq=x[:-1]+theta*np.diff(x)
      Hq,Hxq=bg_eval(xq)
      Xlin=X[:,:-1]+theta*(X[:,1:]-X[:,:-1])
      source=clk.x_embedded_clock_source(
       ztheta,vtheta,Xlin,np.exp(xq),Hq,Hxq,hmid,r,w,tau,kfund,
       d13.d6.ward_signed_convolution)
      source_arrays={k:val for k,val in source.items() if isinstance(val,np.ndarray)}
      for name,value in source_arrays.items():
       saved[prefix+short+'_'+name]=value
      theta_results[short]=source_arrays
      theta_rows.append({
       'theta':theta,
       'original_clock_gamma_minus_one_max_abs_report_only':float(np.max(np.abs(source['gamma']-1))),
       'original_clock_W_signed_L2_report_only':clk.l2(source['signed_W_clock']),
       'original_clock_W_unsigned_envelope_L2_report_only':clk.l2(source['unsigned_W_clock_envelope']),
       'original_continuous_drive_unknown_conditional_W_eps_X_multiplier_L2_report_only':clk.l2(source['conditional_unsigned_W_drive_per_max_eps_X']),
       'original_clock_R_node_mode_L2_report_only':clk.l2(source['clock_R_node_mode_L2']),
       'original_original_R1_theta_state_preserved':True,
       'original_true_X10_continuous_drive_enclosure_available':False,
       'original_GE05_bath_onshell_certified':False})
     scope[nq]=theta_results
     rows.append({
      'C':tag,'Nt':nt,'original_Nq':nq,
      'original_action_background_source_checks':bgdiag,
      'original_R1_step_endpoint_relative_machine':endpoint_rel,
      'original_D13_actual_FD4_signed_parent_relative_machine':parent_rel,
      'original_D13_D14_phase_arrays_bitwise_exact':True,
      'original_GE05_internal_action_gamma_jump_max_abs_report_only':float(np.max(np.abs(jump['interior_gamma_plus_minus_jump']))),
      'original_GE05_internal_action_impulse_signed_W_coeff_L2_report_only_not_smooth_W':clk.l2(jump['interior_original_GE05_Eq_impulse_signed_W_coeff']),
      'original_GE05_internal_action_impulse_unsigned_W_coeff_L2_report_only_not_smooth_W':clk.l2(jump['interior_original_GE05_Eq_impulse_unsigned_W_coeff_envelope']),
      'original_GE05_interface_impulse_distributions_retained':True,
      'original_action_clock_total_delta_s_Gauss16_minus_R1_report_only':float(np.sum(slip['original_action_Gauss16_minus_R1_delta_s'])),
      'original_action_clock_delta_s_Gauss16_vs_Gauss8_max_absolute_report_only':float(np.max(np.abs(slip['original_action_Gauss16_minus_Gauss8_report_only']))),
      'source_bound_collocation_theta_rows':theta_rows,
      'original_true_X10_continuous_drive_enclosure_available':False,
      'original_GE05_bath_first_order_on_shell_certified':False,
      'all_sector_H4_Ward_certified':False,
      'pass_machine_only':True})
    for theta,short in ((0.,'theta0'),(.5,'theta05'),(1.,'theta1')):
     xhi=scope[2048][short];xlo=scope[1024][short]
     for row in rows[-2:]:
      row.setdefault('original_Nq2048_vs_Nq1024_conditional_signed_clock_and_drive_multiplier_report_only',{})[short]={
       'signed_clock_absolute_L2':clk.l2(xhi['signed_W_clock']-xlo['signed_W_clock']),
       'signed_clock_relative':clk.relative(xhi['signed_W_clock'],xlo['signed_W_clock']),
       'unsigned_clock_envelope_absolute_L2':clk.l2(xhi['unsigned_W_clock_envelope']-xlo['unsigned_W_clock_envelope']),
       'conditional_drive_unsigned_multiplier_absolute_L2':clk.l2(xhi['conditional_unsigned_W_drive_per_max_eps_X']-xlo['conditional_unsigned_W_drive_per_max_eps_X'])}
 if len(rows)!=12 or any(not np.isfinite(arr).all() for arr in saved.values()):
  raise RuntimeError('D15a original physical data nonfinite or original cohort missing')
 report={
  'classification':'GE19_H4F3D15A_ACTUAL_ORIGINAL_GE05_X_EMBEDDED_CLOCK_CONDITIONAL_COLLOCATION_PASS_CONTINUOUS_X10_OPEN',
  'preregistration':pre['classification'],
  'interface_preregistration':ifacepre['classification'],
  'actual_original_D13_D14_physical_SHA256':{k:sha256(path) for k,path in actual.items()},
  'original_Repair26_R1_full_trace_SHA256':sha256(trace),
  'original_existing_source_SHA256':{k:sha256(path) for k,path in raw.items()},
  'source_and_prereg_SHA_locks':pins,
  'original_H3F_H3G_Z11_Repair13_certified_parent_locks':parent_locks,
  'all_twelve_original_C_Nt_Nq_cohorts_saved':len(rows)==12,
  'actual_original_GE05_bath_first_order_on_shell_certified':False,
  'actual_true_continuous_X10_drive_enclosed':False,
  'original_internal_GE05_action_interface_distribution_saved':True,
  'original_external_GE05_action_boundary_evaluated':False,
  'actual_all_interval_continuous_bath_error_budget_certified':False,
  'actual_original_E00_F21_and_complete_action_boundary_evaluated':False,
  'full_original_H4_Ward_certified':False,
  'Z21_certified':False,'lensing_licensed':False,
  'original_Repair37_SCIENCE_FAIL_immutable':True,
  'no_observation_tuning':True,
  'claim_boundary':'Original GE05 action H/Hx evaluates on original Repair13 scalar-charge/positive Exp branch; exact original frozen R1 state embedded on physical x clock at theta=0,.5,1 only. Signed +4 E_clock*qx and original noncancelling signed mode-pair envelope and U_X coefficient are conditional at sampled points. The exact original internal knot gamma jump generates an action Euler delta(t-t_i) source with separately saved signed impulse coefficients, NEVER combined in smooth time-grid L2. H clock Gauss8/16 time slips diagnostic only; true continuous X10, true bath state error, interval supremum, original external boundary, full GE05 and H4 on-shell all OPEN.',
  'rows':rows}
 outj.parent.mkdir(parents=True,exist_ok=True)
 outn.parent.mkdir(parents=True,exist_ok=True)
 outj.write_text(json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+'\n')
 np.savez_compressed(outn,**saved)
 print(json.dumps(report,indent=2,sort_keys=True,allow_nan=False))
if __name__=='__main__': main()
