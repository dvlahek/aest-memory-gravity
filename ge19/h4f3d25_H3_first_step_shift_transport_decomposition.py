#!/usr/bin/env python3
"""GE19 D25: original-action H3 shift transport decomposition, three frozen first steps.

A diagnostic on immutable D22A source/trajectories: not a reclosure, projection,
new physical term, source correction, certification, q20, H4 or lensing.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from contextlib import ExitStack
import numpy as np
from scipy.interpolate import PchipInterpolator

from ge19 import h4f3d22a_action_parent_reclosure as d22a

ROOT=Path(__file__).resolve().parents[1]
TINY=1e-300
PARENTS={
 'D17_NPZ':('ge19_h4f3d17_actual_original_action_dense_canonical_H1.npz','cd3bcf8cf5ac9ab14385baa4d90bd53400daae9f2bb89d4d22bfa2a581846359'),
 'D22A_JSON':('ge19_h4f3d22a_actual_Cstar_action_B10_Z11_Z20_parent_candidates.json','158207d747e9fa617c335f4a30d860c011264b2da1dcde34870bad762ec5bbf4'),
 'D22A_NPZ':('ge19_h4f3d22a_actual_Cstar_action_B10_Z11_Z20_parent_candidates.npz','6952a2cde9a39367d29b75b63aca53a97a8feb622e7cbe7b33a468ae2b9a1632'),
 'D23_JSON':('ge19_h4f3d23_action_constraint_boundary_transport.json','207be9d3658ca53848a7584d72abe0e316efee574ea7f14c92b55309d5f13640'),
 'D23_NPZ':('ge19_h4f3d23_action_constraint_boundary_transport.npz','ebe1e17a1d3cfc23ad5e66ba8d225ea4dd5e1480233eac77b4ef978bfd36917b'),
 'D24_JSON':('ge19_h4f3d24_dense_first_interval_H3_source_resolution.json','cb12dd9c07871d47c804ed077309a155a37286dcf52672d08d072d4c67694041'),
 'D24_NPZ':('ge19_h4f3d24_dense_first_interval_H3_source_resolution.npz','3c2d5e75503024a8fc7e7e675a8154d5c8710c0f75624c5988066bde9df2d99d'),
 'R13_NPZ':('ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz','011c0ae54fd21d70c0e2c695ce62e7b74a3c5529a07c9023c882a447d5b40ca3'),
}
CASES=((14,2,0.1),(1,0,1.0),(40,2,0.1))

def sha(path):
 h=hashlib.sha256()
 with Path(path).open('rb') as f:
  for chunk in iter(lambda:f.read(1<<20),b''):h.update(chunk)
 return h.hexdigest()

def ab_rel(x,y):
 return float(abs(x-y)/max(abs(x),abs(y),TINY))

def cpair(z):
 z=complex(z)
 return [float(z.real),float(z.imag)]

def scalar_interp(x,arr):
 arr=np.asarray(arr,complex)
 re=PchipInterpolator(x,arr.real,axis=1,extrapolate=False)
 im=PchipInterpolator(x,arr.imag,axis=1,extrapolate=False)
 return lambda q:np.asarray(re(q)+1j*im(q),complex),lambda q:np.asarray(re.derivative()(q)+1j*im.derivative()(q),complex)

def operator_coefficients(r7,mod6,mod7,bg,k,xq):
 M,F,ZY,ZR,WY,WR,Cmat,bp,_=r7._canonical_operator_matrices(mod6,mod7,bg,'C_star',k,float(xq))
 row=Cmat[10]+Cmat[11]
 ky=np.asarray(row@WY,complex)
 ks=np.asarray(row@WR,complex).copy()
 ks[6]-=1.0  # Signed shift-source subtraction: g = L_shift - source_shift.
 return M,F,ky,ks,Cmat,WY,WR,row

def start_end_y(state,dot,Cmat,at):
 w=np.r_[state[[0,5,1,2,3,4],at],dot[:,at]]
 p=np.asarray(Cmat[0:4]@w,complex)
 return np.r_[state[[1,2,3,4],at],p],w

def derivative_onesided(fun,x,eps):
 return (-3*fun(x)+4*fun(x+eps)-fun(x+2*eps))/(2*eps)

def evaluate(r7,mod6,mod7,bg,x,archive,mode,ib,beta):
 h=float(x[1]-x[0]); x0=float(x[0]);x1=float(x[1]);k=float(mode*r7.g9.K_REQ[0]/r7.FOURIER_N[0]);jm=mode-1
 main=np.asarray(archive[f'beta{ib}_H3F_D17_source_rows'][:,:,mode],complex)
 constraint=np.asarray(archive[f'beta{ib}_H3F_D17_source_constraints'][:,:,mode],complex)
 if main.shape!=(6,len(x)) or constraint.shape!=(2,len(x)):
  raise RuntimeError('D25 archived H3 source layout mismatch')
 src,srcdot=scalar_interp(x,np.concatenate((main,constraint),axis=0))
 state=np.asarray(archive['Z20_D17_H3F_candidate_primary'],complex)[ib,jm]
 dot=np.asarray(archive['Z20dot_D17_H3F_candidate_primary'],complex)[ib,jm]
 p0=np.asarray(archive['Z20_source_aware_projected_p0_primary'],complex)[ib,jm]
 op0=operator_coefficients(r7,mod6,mod7,bg,k,x0)
 op1=operator_coefficients(r7,mod6,mod7,bg,k,x1)
 y0,w0=start_end_y(state,dot,op0[4],0)
 y1,w1=start_end_y(state,dot,op1[4],1)
 p0_error=float(np.linalg.norm(y0[4:]-p0)/max(np.linalg.norm(y0[4:]),np.linalg.norm(p0),TINY))
 if p0_error>1e-6:raise RuntimeError(f'D25 initial canonical momentum reconstruction failed m={mode} {p0_error}')
 s0=src(x0);s1=src(x1);sp0=srcdot(x0)
 ky0,ks0=op0[2],op0[3];ky1,ks1=op1[2],op1[3]
 g0=complex(ky0@y0+ks0@s0);g1=complex(ky1@y1+ks1@s1)
 # Independent reconstruction from frozen native Cmat + original-action sourced w.
 wg0=op0[5]@y0+op0[6]@s0;wg1=op1[5]@y1+op1[6]@s1
 direct0=complex(op0[7]@wg0-s0[6]);direct1=complex(op1[7]@wg1-s1[6])
 gate=float(r7._constraint_backward_error(op1[7],wg1,s1[6])['metric'])
 yp0=np.asarray(op0[0]@y0+op0[1]@s0,complex)
 def coeff(q):
  z=operator_coefficients(r7,mod6,mod7,bg,k,q)
  return np.r_[z[2],z[3]]
 scales=(h/16.,h/32.)
 diags=[]
 for eps in scales:
  dc=derivative_onesided(coeff,x0,eps);kyp=dc[:8];ksp=dc[8:]
  terms={
   'operator_explicit_x':complex(kyp@y0),
   'canonical_evolution':complex(ky0@yp0),
   'source_operator_explicit_x':complex(ksp@s0),
   'explicit_source_time_derivative':complex(ks0@sp0),
  }
  total=sum(terms.values())
  # Independently differentiate g along the linearized flow at x0.
  def glin(q):
   off=q-x0;z=coeff(q)
   return complex(z[:8]@(y0+off*yp0)+z[8:]@(s0+off*sp0))
  direct=complex(derivative_onesided(glin,x0,eps))
  diags.append({'eps':eps,'gprime_decomposed':total,'gprime_independent_linearized':direct,'terms':terms})
 first=diags[0];second=diags[1]
 gprime=first['gprime_decomposed'];gprime_half=second['gprime_decomposed']
 consistency=float(abs(gprime-first['gprime_independent_linearized'])/max(sum(abs(v) for v in first['terms'].values()),abs(first['gprime_independent_linearized']),TINY))
 g0def=float(abs(g0-direct0)/max(np.sum(np.abs(ky0*y0))+np.sum(np.abs(ks0*s0)),np.sum(np.abs(op0[7]*wg0))+abs(s0[6]),TINY))
 g1def=float(abs(g1-direct1)/max(np.sum(np.abs(ky1*y1))+np.sum(np.abs(ks1*s1)),np.sum(np.abs(op1[7]*wg1))+abs(s1[6]),TINY))
 if max(g0def,g1def,consistency)>1e-4:
  raise RuntimeError(f'D25 independent shift identity/decomposition failed m={mode}: {g0def},{g1def},{consistency}')
 term_abs={key:float(abs(v)) for key,v in first['terms'].items()}
 denom=sum(term_abs.values())
 report={
  'mode':mode,'beta':beta,'initial_momentum_reconstruction_relative':p0_error,
  'g0':cpair(g0),'g1_archived':cpair(g1),
  'original_action_shift_backward_first_step':gate,
  'gprime_terms_at_eps_h_over_16':{k:cpair(v) for k,v in first['terms'].items()},
  'gprime_relative_term_magnitudes':{k:float(abs(v)/max(denom,TINY)) for k,v in first['terms'].items()},
  'gprime_decomposed':cpair(gprime),'gprime_decomposed_halved':cpair(gprime_half),
  'gprime_step_halving_relative_report_only':ab_rel(gprime,gprime_half),
  'gprime_linearized_crosscheck_relative':consistency,
  'first_step_h_times_gprime':cpair(h*gprime),
  'first_step_g1_over_h_gprime_absolute_ratio_report_only':float(abs(g1)/max(abs(h*gprime),TINY)),
  'first_step_g0_over_g1_absolute_ratio_report_only':float(abs(g0)/max(abs(g1),TINY)),
  'H3_first_step_source_shift_start':cpair(s0[6]),
  'H3_first_step_source_shift_next':cpair(s1[6]),
  'H3_first_step_source_shift_derivative_pchip':cpair(sp0[6]),
  'operator_source_coefficient_contribution':cpair(first['terms']['source_operator_explicit_x']),
  'source_time_derivative_contribution':cpair(first['terms']['explicit_source_time_derivative']),
 }
 return report,dict(g0=g0,g1=g1,gprime=gprime,gprime_half=gprime_half,term_vec=np.asarray(list(first['terms'].values()),complex))

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--results-dir',required=True);ap.add_argument('--json-out',required=True);ap.add_argument('--npz-out',required=True)
 ar=ap.parse_args();rd=Path(ar.results_dir).resolve();oj=Path(ar.json_out);on=Path(ar.npz_out)
 if oj.exists() or on.exists():raise RuntimeError('D25 no-overwrite outputs already present')
 paths={}
 for key,(filename,want) in PARENTS.items():
  p=rd/filename
  if not p.is_file() or sha(p)!=want:raise RuntimeError(f'D25 immutable parent missing or SHA differs {key}: {p}')
  paths[key]=p
 if json.loads(paths['D22A_JSON'].read_text())['classification']!='GE19_D22A_CSTAR_PARENT_NUMERICAL_CANDIDATE_FAIL_Q20_AND_FULL_H4_OPEN':
  raise RuntimeError('D25 immutable D22A failure changed')
 d24=json.loads(paths['D24_JSON'].read_text())
 if d24['classification']!='GE19_D24_DENSE_FIRST_INTERVAL_H3_SOURCE_RESOLUTION_DIAGNOSTIC_COMPLETE_PARENTS_UNCERTIFIED':
  raise RuntimeError('D25 immutable D24 diagnostic changed')
 pre=json.loads(d22a.PRE.read_text())
 for relpath,want in pre['frozen_git_blobs'].items():d22a.exact_git(relpath,want)
 for relpath,want in pre['local_sha256'].items():
  if sha(ROOT/relpath)!=want:raise RuntimeError('D25 D22A original source SHA changed '+relpath)
 d23=json.loads(paths['D23_JSON'].read_text())
 print('GE19_D25_D17_D22A_D23_D24_R13_AND_FROZEN_ORIGINAL_SOURCE_SHA_PASS',flush=True)
 old=d22a.d20.source.old;r7=old.r7
 with ExitStack() as stack:
  r13=stack.enter_context(np.load(paths['R13_NPZ'],allow_pickle=False))
  archive=stack.enter_context(np.load(paths['D22A_NPZ'],allow_pickle=False))
  d24z=stack.enter_context(np.load(paths['D24_NPZ'],allow_pickle=False))
  bgs,_,mod6,mod7,_,_,_,_,_=old.build_context(rd,r13)
  bg=bgs[(128,'C_star')];x=np.asarray(bg['x'],float)
  if not (np.array_equal(x,archive['x_primary']) and
          np.array_equal(d24z['x_original_first_interval_dense_sub4'][::4],x[:3])):
   raise RuntimeError('D25 D24 and D22A first-interval grid mismatch')
  old_bg=r7._bg_point;old_cache=r7._CANONICAL_LOCAL_CACHE
  r7._CANONICAL_LOCAL_CACHE={};active={'ctx':None}
  def action_bgpoint(bgarg,xq):
   if active['ctx'] is None:raise RuntimeError('D25 original-action background missing')
   return active['ctx'](bgarg,xq)
  r7._bg_point=action_bgpoint
  try:
   evalH,_=d22a.d17driver.d16r1.d15.clk.make_original_action_background(r7,bg,'C_star')
   ctx=d22a.d17core.ActionBackground(r7,bg,evalH);active['ctx']=ctx;ctx.knot_check()
   results=[];arrays={}
   for mode,ib,beta in CASES:
    rec,arr=evaluate(r7,mod6,mod7,bg,x,archive,mode,ib,beta)
    ref=next((q for q in d23['H3_first_interval_constraint_transport']
              if int(q['mode'])==mode and float(q['beta'])==beta),None)
    if ref is None:raise RuntimeError(f'D25 D23 archived first-step control missing m={mode} beta={beta}')
    stored_g1=complex(*ref['g1_archived_complex'])
    replay=ab_rel(arr['g1'],stored_g1)
    if replay>1e-4:raise RuntimeError(f'D25 D23 first-step shift replay mismatch m={mode}: {replay}')
    rec['D23_archived_first_step_g1_relative_replay']=replay
    rec['D24_dense_first_step_shift_backward_report_only']=next(
      float(q['dense']['first_step_shift_backward']) for q in d24['selected_first_step']
      if int(q['mode'])==mode and float(q['beta'])==beta)
    results.append(rec)
    arrays[f'm{mode}_beta{ib}_g0_g1_gprime']=np.asarray([arr['g0'],arr['g1'],arr['gprime'],arr['gprime_half']],complex)
    arrays[f'm{mode}_beta{ib}_gprime_four_terms']=arr['term_vec']
    print(f'GE19_D25_H3_SHIFT_COMPONENT m={mode} beta={beta} '
          f'g1={abs(arr["g1"]):.4e} gprime={abs(arr["gprime"]):.4e} '
          f'halving={rec["gprime_step_halving_relative_report_only"]:.3e} '
          f'backward={rec["original_action_shift_backward_first_step"]:.3e}',flush=True)
  finally:
   r7._bg_point=old_bg;r7._CANONICAL_LOCAL_CACHE=old_cache
 report={
  'classification':'GE19_D25_H3_FIRST_STEP_SHIFT_TRANSPORT_DECOMPOSITION_DIAGNOSTIC_COMPLETE_PARENTS_UNCERTIFIED',
  'preregistration':'D25 frozen three-case H3 shift coefficient/trajectory/source derivative breakdown on D22A coarse original-action sources',
  'input_sha256':{k:sha(p) for k,p in paths.items()},
  'D22A_SCIENCE_FAIL_immutable':True,'D23_H2_diagnostic_only':True,'D24_H3_dense_diagnostic_only':True,
  'source_changes':False,'new_H3_integration':False,'new_H2_integration':False,'q20_B20_recomputed':False,
  'Z11_certified':False,'Z20_certified':False,'Z21_certified':False,
  'full_H4_Ward_certified':False,'lensing_licensed':False,'observational_tuning':False,
  'claim_boundary':'Three first-step H3 shift transport decompositions on frozen coarse D22A source. Finite-difference derivative is a diagnostic, not a continuum enclosure or full Noether identity. D24 dense source is independent and not silently relabelled. No gate or tolerance change and no parent promotion.',
  'cases':results,
 }
 oj.parent.mkdir(parents=True,exist_ok=True)
 np.savez_compressed(on,**arrays)
 oj.write_text(json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+'\n')
 print('GE19_D25_CLASSIFICATION '+report['classification'],flush=True)

if __name__=='__main__':main()
