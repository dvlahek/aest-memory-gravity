#!/usr/bin/env python3
"""D19R1: one source-locked C_star Nt128 Nq2048 GE05 numerical reclosure.

Original frozen Repair24 exact-step kernel, D17 source-action dense H1 drive,
D15a true action H(x) and Repair26 initial bath as archived in immutable D16R1.
This is a finite-tolerance NUMERICAL test, not certified continuum H1, all-interval
GE05 on shell, dependent q20 or full H4 Ward. Existing archives are immutable.
"""
from __future__ import annotations
import argparse,hashlib,json,subprocess
from pathlib import Path
import numpy as np
from ge19 import h4f3d16r1_actual_original_H1dot_Hermite_physical_bath as d16r1
from ge19 import h4f3d16_original_H1dot_Hermite_physical_bath_core as d16core
from ge19 import h4f3d19r1_physical_bath_numerical_core as core

ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/'ge19/h4f3d19r1_predata_numerical_reclosure.json'
TINY=1e-300

def digest(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--results-dir',required=True)
    ap.add_argument('--repair26-trace',required=True)
    ap.add_argument('--json-out',required=True)
    ap.add_argument('--npz-out',required=True)
    args=ap.parse_args()
    rd=Path(args.results_dir).resolve();trace=Path(args.repair26_trace).resolve()
    oj=Path(args.json_out).resolve();on=Path(args.npz_out).resolve()
    if oj.exists() or on.exists():raise RuntimeError('D19R1 refuses to overwrite existing result')
    pre=json.loads(PRE.read_text())
    if pre['classification']!='GE19_H4F3D19R1_PREDATA_EXTENDED_ORIGINAL_ACTION_NUMERICAL_BATH_RECLOSURE':
        raise RuntimeError('D19R1 preregistration classification changed')
    for rel,sha in pre['frozen_source_blobs'].items():
        head=subprocess.check_output(['git','rev-parse','HEAD:'+rel],cwd=ROOT,text=True).strip()
        work=subprocess.check_output(['git','hash-object',str(ROOT/rel)],cwd=ROOT,text=True).strip()
        if not(head==work==sha):raise RuntimeError('D19R1 immutable original source changed: '+rel)
    for rel,sha in pre['source_sha256'].items():
        if digest(ROOT/rel)!=sha:raise RuntimeError('D19R1 local preregistered source changed: '+rel)
    for name,(filename,sha) in pre['actual_parent_results'].items():
        if not (rd/filename).is_file() or digest(rd/filename)!=sha:
            raise RuntimeError('D19R1 actual parent changed: '+name)
    if digest(trace)!=pre['Repair26_trace_sha256'] or trace.stat().st_size!=26643162:
        raise RuntimeError('D19R1 original Repair26 R1 trace changed')
    d16pre=json.loads((ROOT/d16r1.PRE).read_text())
    pins,raw,parents=d16r1.physical_input_locks(rd,trace,d16pre)
    d15=d16r1.d15;old=d15.d13.old;r24=old.r24;r7=old.r7;c4=old.c4
    paths,parentlocks=d15.parents.frozen_inputs(rd,trace)
    if not all(parentlocks[k]['exact'] for k in d15.parents.REQUIRED):
        raise RuntimeError('D19R1 H3F/H3G/Z11/Repair13 frozen parent changed')
    print('GE19_D19R1_FROZEN_ACTION_AND_D17_D16R1_PARENT_SHA_PASS',flush=True)
    tau=r24.TAUH0/float(r7.g9.H0_CLASS)
    kfund=float(r7.g9.K_REQ[0]/r7.FOURIER_N[0])
    prefix='primary_C_star_';nq=2048
    out={};rows=[];runs={}
    with (np.load(paths['r13'],allow_pickle=False) as r13,
          np.load(rd/pre['actual_parent_results']['D17_NPZ'][0],allow_pickle=False) as d17,
          np.load(rd/pre['actual_parent_results']['D16R1_NPZ'][0],allow_pickle=False) as d16,
          np.load(rd/pre['actual_parent_results']['D15A_NPZ'][0],allow_pickle=False) as d15npz):
        bgs,_,_,_,_,_,_,_,_=old.build_context(rd,r13)
        bg=bgs[(128,'C_star')]
        evalH,bgdiag=d15.clk.make_original_action_background(r7,bg,'C_star')
        xorig=np.asarray(d17['x_primary'],float)
        xf=np.asarray(d17[prefix+'x_dense_sub4'],float)
        X=np.asarray(d17[prefix+'X10_original_action_dense_sub4'],complex)
        DX=np.asarray(d17[prefix+'X10_x_original_action_dense_sub4'],complex)
        xold=np.asarray(d16['x_primary'],float)
        if not(np.array_equal(xorig,xold) and np.array_equal(xf[::4],xorig)):
            raise RuntimeError('D19R1 physical D17 original H1 knot grid mismatch')
        zold=np.asarray(d16[prefix+'Nq2048_node_z_Hermite_physical_sub16'],complex)
        vold=np.asarray(d16[prefix+'Nq2048_node_v_Hermite_physical_sub16'],complex)
        if zold.shape!=(nq,6,128) or vold.shape!=zold.shape:
            raise RuntimeError('D19R1 original D16R1 complete bath node state missing')
        z0=zold[:,:,0].copy();v0=vold[:,:,0].copy()
        r,w=c4.tan_gl_nodes(nq);r=np.asarray(r,float);w=np.asarray(w,float)
        iz=np.einsum('n,nm->m',w,z0,optimize=True)
        iv=np.einsum('n,nm->m',w,v0,optimize=True)
        bz=np.asarray(d16[prefix+'Nq2048_weighted_z_Hermite_physical_sub16'],complex)[:,0]
        bv=np.asarray(d16[prefix+'Nq2048_weighted_v_Hermite_physical_sub16'],complex)[:,0]
        initial_error=max(core.rel(iz,bz),core.rel(iv,bv))
        if initial_error>1e-12:raise RuntimeError('D19R1 original Repair26 bath initial state changed')
        original_X0=np.asarray(d16[prefix+'original_X10_H1_endpoint'],complex)[:,0]
        if core.rel(X[:,0],original_X0)>1e-12:
            raise RuntimeError('D19R1 source-action H1 and original bath initial drive changed')
        # Mandatory parent replay: validate full frozen D16R1 numerical state,
        # not merely its hash or initial boundary. Do NOT compare old Hermite
        # output to the new D17-driven bath as though they were same physics.
        Xold=np.asarray(d16[prefix+'original_X10_H1_endpoint'],complex)
        DXold=np.asarray(d16[prefix+'original_X10_x_derivative_from_H1dot'],complex)
        zreplay,vreplay,_,_=d16core.propagate_physical(
            xorig,Xold,DXold,evalH,z0,v0,r,tau,r24.step_linear_nd,16,'hermite')
        replay_z=core.rel(zreplay,zold);replay_v=core.rel(vreplay,vold)
        print('GE19_D19R1_MANDATORY_D16R1_FULL_PARENT_REPLAY z={:.8e} v={:.8e}'.format(
            replay_z,replay_v),flush=True)
        if replay_z>1e-10 or replay_v>1e-10:
            raise RuntimeError('D19R1 original D16R1 full-node parent did not numerically replay; '
                               'source-action bath reclosure NOT licensed')
        del zreplay,vreplay,zold,vold
        dsa=np.asarray(d15npz[prefix+'original_action_delta_s_Gauss16'],float)
        if dsa.shape!=(127,) or np.any(dsa<=0):
            raise RuntimeError('D19R1 true original action Gauss16 clock parent invalid')
        phase_mask=core.high_phase_mask(r,dsa,tau)
        if not(np.array_equal(np.asarray(r7.FOURIER_N,int),core.MODES)):
            raise RuntimeError('D19R1 original Fourier mode dictionary changed')
        for sub in pre['substeps_per_D17_fine_interval']:
            print('GE19_D19R1_SUBSTEP_BEGIN original_sub={}'.format(4*int(sub)),flush=True)
            sol=core.propagate(xf,X,DX,evalH,z0,v0,r,tau,
                r24.step_linear_nd,int(sub),xorig,sample=True,progress=True)
            sds=sol['clock_substep_ds'].reshape(127,4*int(sub)).sum(axis=1)
            clock_rel=core.rel(sds,dsa)
            if clock_rel>1e-9:raise RuntimeError('D19R1 original physical action clock vs D15a Gauss16 mismatch')
            Rs=sol['sample_Rs'];zs=sol['sample_z'];vs=sol['sample_v']
            W,U=core.source_signed(zs,vs,Rs,sol['sample_x'],w,r,tau,kfund,
                d15.d13.d6.ward_signed_convolution,d15.clk.unsigned_signed_pair_envelope)
            rs_mode=np.linalg.norm(Rs,axis=0)
            natural=np.maximum(np.linalg.norm(3.*tau*sol['sample_H'][None,None,:]*vs,axis=0),
                np.linalg.norm((r[:,None,None]**2)*(
                  zs-np.stack([core.hermite_value(X,DX,xf,4*i+branch,.6 if branch==1 else .4)
                    for i in range(127) for branch in (1,2)],axis=-1)[None,:,:]),axis=0))
            relative_residual=float(np.max(rs_mode/np.maximum(natural,TINY)))
            tag=f'sub{4*sub}'
            wz=np.einsum('n,nmt->mt',w,sol['z'],optimize=True)
            wv=np.einsum('n,nmt->mt',w,sol['v'],optimize=True)
            out[tag+'_weighted_z']=wz;out[tag+'_weighted_v']=wv
            out[tag+'_sampled_signed_GE05_W_D17_surrogate']=W
            out[tag+'_sampled_unsigned_GE05_W_envelope_D17_surrogate']=U
            out[tag+'_sampled_Rs_node_L2_per_mode']=rs_mode
            out[tag+'_sample_x_fixed']=sol['sample_x']
            if int(sub)==64:
                out['physical_Cstar_Nt128_Nq2048_z_sub256']=sol['z']
                out['physical_Cstar_Nt128_Nq2048_v_sub256']=sol['v']
            rows.append({'substeps_per_original_H3F_interval':4*int(sub),
                'original_source_action_clock_relative_vs_D15a_Gauss16':clock_rel,
                'sampled_GE05_D17_surrogate_relative_residual_max_not_continuum_bound':relative_residual,
                'sampled_signed_W_L2_not_full_H4':core.norm(W),
                'sampled_unsigned_W_envelope_L2':core.norm(U),
                'source_envelope_pass':bool(np.all(np.abs(W)<=U*(1+1e-10)+1e-24)),
                'high_phase_physical_interval_node_steps':int(phase_mask.sum())})
            runs[int(sub)]={'z':sol['z'],'v':sol['v'],'wz':wz,'wv':wv,'W':W,
                  'relative_residual':relative_residual}
            print('GE19_D19R1_SUBSTEP_DONE original_sub={} GE05_sampled_rel={:.6e} signedW_L2={:.6e}'.format(
                4*sub,relative_residual,core.norm(W)),flush=True)
        a,b,c=(runs[q] for q in (16,32,64))
        comparisons={}
        for name,oldrun,newrun in [('sub64_vs_sub128',a,b),('sub128_vs_sub256',b,c)]:
            comparisons[name]={'full_node_z_relative':core.rel(oldrun['z'],newrun['z']),
                'full_node_v_relative':core.rel(oldrun['v'],newrun['v']),
                'weighted_z_relative':core.rel(oldrun['wz'],newrun['wz']),
                'weighted_v_relative':core.rel(oldrun['wv'],newrun['wv']),
                'high_phase_z_relative':core.masked_rel(oldrun['z'],newrun['z'],phase_mask),
                'high_phase_v_relative':core.masked_rel(oldrun['v'],newrun['v'],phase_mask),
                'sampled_signed_W_relative_report_only':core.rel(oldrun['W'],newrun['W'])}
        fixed=pre['frozen_numerical_gates'];last=comparisons['sub128_vs_sub256']
        gate={
            'weighted_z':last['weighted_z_relative']<=fixed['weighted_z_relative'],
            'weighted_v':last['weighted_v_relative']<=fixed['weighted_v_relative'],
            'full_node_z':last['full_node_z_relative']<=fixed['full_node_z_relative'],
            'full_node_v':last['full_node_v_relative']<=fixed['full_node_v_relative'],
            'high_phase_v':last['high_phase_v_relative']<=fixed['high_phase_v_relative'],
            'sampled_GE05_relative':c['relative_residual']<=fixed['sampled_GE05_relative_residual'],
            'signed_source_envelope':all(q['source_envelope_pass'] for q in rows),
            'action_clock_exact_parent':all(q['original_source_action_clock_relative_vs_D15a_Gauss16']<=1e-9 for q in rows)}
        passed=all(gate.values())
        rep={'classification':('GE19_H4F3D19R1_CSTAR_NUMERICAL_BATH_TOLERANCE_PASS_D17_H1_AND_FULL_H4_OPEN' if passed
            else 'GE19_H4F3D19R1_CSTAR_NUMERICAL_BATH_TOLERANCE_NOT_CLOSED_D17_H1_AND_FULL_H4_OPEN'),
            'preregistration':pre['classification'],'source_sha256':{rel:digest(ROOT/rel) for rel in pre['source_sha256']},
            'parent_sha256':{name:digest(rd/f) for name,(f,_) in pre['actual_parent_results'].items()},
            'source_action_background':bgdiag,'original_bath_initial_weighted_reproduction_relative':initial_error,
            'original_D16R1_full_node_replay_relative':{'z':replay_z,'v':replay_v},
            'original_fourier_modes':list(map(int,core.MODES)),
            'cohort':'C_star Nt128 Nq2048 only; both source +/- and output Fourier m0..40',
            'retained_all_original_quadrature_nodes':True,
            'original_high_phase_node_step_count':int(phase_mask.sum()),
            'original_action_physical_clock_not_R1_hmid':True,
            'frozen_numerical_gates':fixed,'gates':gate,'numerical_tol_pass':passed,
            'comparisons':comparisons,'runs':rows,
            'source_claim_boundary':'GE05 residual and signed W are sampled at fixed x=.4,.6 of each original interval against D17 source-action dense H1 Hermite surrogate. This tests finite-step bath numerics, NOT source-exact continuous H1, all-interval GE05 Euler, original full GE05/H4 Ward or action boundary. No dependent q20 or Z11 rebuild or Z21 solve.',
            'true_continuous_original_H1_X10_enclosed':False,
            'all_interval_GE05_on_shell_certified':False,
            'full_original_H4_Ward_certified':False,'Z21_certified':False,'lensing_licensed':False,
            'frozen_Repair37_SCIENCE_FAIL_immutable':True,'no_observation_tuning':True}
        out['original_x_primary']=xorig;out['D17_x_dense_sub4']=xf
        out['original_action_phase_mask_at_orig_intervals']=phase_mask
        oj.parent.mkdir(parents=True,exist_ok=True);on.parent.mkdir(parents=True,exist_ok=True)
        oj.write_text(json.dumps(rep,sort_keys=True,indent=2,allow_nan=False)+'\n')
        np.savez_compressed(on,**out)
        print('GE19_D19R1_NUMERICAL_TOLERANCE_PASS='+str(passed),flush=True)
        print(json.dumps({'classification':rep['classification'],'gates':gate,'comparisons':comparisons,
                          'runs':rows},sort_keys=True,indent=2),flush=True)

if __name__=='__main__':main()
