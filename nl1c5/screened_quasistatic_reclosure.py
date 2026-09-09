#!/usr/bin/env python3
import argparse
import json
import math
from pathlib import Path

import numpy as np

H0=67.3324639084866
h=H0/100.0
OMEGA_B=0.022377376877682164
OMEGA_CDM=0.12006705327635288
OMEGA_NU=0.06/93.14
OMEGA_M=OMEGA_B+OMEGA_CDM+OMEGA_NU
AS=2.1308864352626987e-9
NS=0.9666229454895277
KPIV=0.05
KB=0.0665
K2=9500.0
Q0=1.0e-4
MU2=2.0*K2*Q0**2/(2.0-KB)
BETA=[1.0,0.5,0.1]
K_H=np.asarray([0.03,0.05,0.08,0.10,0.15,0.20],float)
K_MPC=K_H*h
PHASE=np.asarray([0.13,0.71,1.29,2.03,2.77,3.41],float)
C_KM=299792.458
C=299792458.0
MPC_M=3.0856775814913673e22
A0=1.2e-10
ZMIN,ZMAX=0.2,1.5


def weights_log(k):
    x=np.log(np.asarray(k,float)); w=np.empty_like(x)
    w[0]=0.5*(x[1]-x[0]); w[-1]=0.5*(x[-1]-x[-2])
    w[1:-1]=0.5*(x[2:]-x[:-2])
    return w

WIDTH=weights_log(K_H)
PR=AS*(K_MPC/KPIV)**(NS-1.0)
MODE_AMP=np.sqrt(2.0*WIDTH*PR)


def read_trace(path):
    arr=np.genfromtxt(path,names=True)
    target=K_MPC[0]
    rel=np.abs(arr['k']-target)/target
    rows=arr[rel<=1e-12]
    order=np.argsort(rows['tau']); rows=rows[order]
    # exact target mode has one accepted row per native source time
    return rows


def load_inputs(npz_path,trace_path):
    d=np.load(npz_path)
    kn=np.asarray(d['k_native_h'],float); zn=np.asarray(d['z_native'],float)
    dm=np.asarray(d['d_m_base'],float)
    idx=[]; misses=[]
    for target in K_H:
        j=int(np.argmin(np.abs(kn-target)))
        miss=abs(kn[j]-target)/target
        idx.append(j); misses.append(miss)
    dm6=dm[np.asarray(idx),:].T
    tr=read_trace(trace_path)
    if len(tr)!=len(zn):
        raise RuntimeError(f'trace/native z count mismatch {len(tr)} != {len(zn)}')
    ztrace=1.0/np.asarray(tr['a'],float)-1.0
    z_mismatch=float(np.max(np.abs(ztrace-zn)))
    return {'z':zn,'a':1.0/(1.0+zn),'H':np.asarray(tr['H_over_H0'],float),
            'chi_linear_transfer':None,'dm':dm6,
            'k_miss_max':float(max(misses)),'z_mismatch_max':z_mismatch,
            'trace':tr}


def reconstruct_modes(coeff,nx):
    kfund=h*0.01; box=2*np.pi/kfund
    x=np.arange(nx)*box/nx
    field=np.zeros(nx,float)
    for a,k,p in zip(coeff,K_MPC,PHASE):
        field += a*np.cos(k*x+p)
    return field,box


def spectral_lap(field,box):
    kk=2*np.pi*np.fft.fftfreq(len(field),d=box/len(field))
    return np.fft.ifft(-(kk**2)*np.fft.fft(field)).real


def spectral_grad(field,box):
    kk=2*np.pi*np.fft.fftfreq(len(field),d=box/len(field))
    return np.fft.ifft(1j*kk*np.fft.fft(field)).real


def solve_one(beta,a,dm_coeff,nx):
    # Deterministic matter-contrast Fourier coefficients.
    delta_coeff=MODE_AMP*dm_coeff
    # Frozen late-time density normalization, in c=1 Mpc units.
    source_pref=1.5*(100.0/C_KM)**2*OMEGA_M*a**-3
    source_coeff=source_pref*delta_coeff
    kphys=K_MPC/a
    mass2=(1.0+beta)*MU2
    denom=mass2-kphys*kphys
    if np.any(np.abs(denom)<1e-12*np.maximum(kphys*kphys,mass2)):
        raise RuntimeError('screened Helmholtz pole approached')
    phi_coeff=source_coeff/denom
    chi_coeff=(beta/(1.0+beta))*phi_coeff

    delta,box=reconstruct_modes(delta_coeff,nx)
    source,_=reconstruct_modes(source_coeff,nx)
    phi,_=reconstruct_modes(phi_coeff,nx)
    chi,_=reconstruct_modes(chi_coeff,nx)
    lap_phys=spectral_lap(phi,box)/(a*a)
    residual=lap_phys+mass2*phi-source
    scale=max(np.linalg.norm(source),1e-300)
    helm_rel=float(np.linalg.norm(residual)/scale)
    chi_relation=float(np.linalg.norm(chi-(beta/(1+beta))*phi)/max(np.linalg.norm(chi),1e-300))
    grad_phys=spectral_grad(chi,box)/a
    Xrms=float(np.sqrt(np.mean(grad_phys*grad_phys)))
    xrms=(C*C/A0)*(Xrms/MPC_M)
    low=np.asarray([np.fft.fft(chi)[m]/nx for m in [3,5,8,10,15,20]])
    return {'phi_coeff':phi_coeff,'chi_coeff':chi_coeff,'helmholtz_residual_relative_l2':helm_rel,
            'chi_relation_relative_l2':chi_relation,'X_rms_1_per_Mpc':Xrms,
            'x_rms':float(xrms),'low_modes':low}


def linear_x_from_trace(inputs,nx=512):
    # Historical CLASS chi context at exact requested modes.
    trall=np.genfromtxt(args.trace,names=True)
    out=[]
    for it,(a,z) in enumerate(zip(inputs['a'],inputs['z'])):
        coeff=[]
        for km in K_MPC:
            rel=np.abs(trall['k']-km)/km
            rows=trall[rel<=1e-12]
            rows=rows[np.argsort(rows['tau'])]
            coeff.append(MODE_AMP[len(coeff)]*float(rows['chi'][it]))
        chi,box=reconstruct_modes(np.asarray(coeff),nx)
        grad=spectral_grad(chi,box)/a
        xr=(C*C/A0)*(float(np.sqrt(np.mean(grad*grad)))/MPC_M)
        out.append(xr)
    return np.asarray(out)


def main():
    global args
    ap=argparse.ArgumentParser()
    ap.add_argument('--npz',required=True)
    ap.add_argument('--trace',required=True)
    ap.add_argument('--json-out',required=True)
    args=ap.parse_args()
    inp=load_inputs(args.npz,args.trace)
    lin_x=linear_x_from_trace(inp)

    branches={}
    all_numeric=True; all_saturated=True
    eval_mask=(inp['z']>=ZMIN-1e-12)&(inp['z']<=ZMAX+1e-12)
    for beta in BETA:
        rows=[]; max_helm=0.0; max_chi=0.0; max_res=0.0
        for it,(z,a) in enumerate(zip(inp['z'],inp['a'])):
            s256=solve_one(beta,a,inp['dm'][it],256)
            s512=solve_one(beta,a,inp['dm'][it],512)
            max_helm=max(max_helm,s256['helmholtz_residual_relative_l2'],s512['helmholtz_residual_relative_l2'])
            max_chi=max(max_chi,s256['chi_relation_relative_l2'],s512['chi_relation_relative_l2'])
            mode_rel=float(np.linalg.norm(s256['low_modes']-s512['low_modes'])/max(np.linalg.norm(s512['low_modes']),1e-300))
            xr_rel=abs(s256['x_rms']-s512['x_rms'])/max(abs(s512['x_rms']),1e-300)
            max_res=max(max_res,mode_rel,xr_rel)
            saturated=s512['x_rms']>=10.0
            all_saturated=all_saturated and saturated
            rows.append({'index':it,'z':float(z),'a':float(a),'x_rms':s512['x_rms'],
                         'historical_linear_x_rms':float(lin_x[it]),
                         'screened_to_historical_x_ratio':float(s512['x_rms']/max(lin_x[it],1e-300)),
                         'helmholtz_residual_relative_l2':s512['helmholtz_residual_relative_l2'],
                         'chi_relation_relative_l2':s512['chi_relation_relative_l2'],
                         'resolution_relative':max(mode_rel,xr_rel),
                         'high_gradient_x_ge_10':bool(saturated)})
        numeric=(max_helm<=1e-10 and max_chi<=1e-12 and max_res<=5e-3 and
                 all(math.isfinite(float(v)) for r in rows for v in r.values() if not isinstance(v,bool)))
        all_numeric=all_numeric and numeric
        ev=[r for r,m in zip(rows,eval_mask) if m]
        branches[str(beta)]={
            'max_helmholtz_residual_relative_l2':max_helm,
            'max_chi_relation_relative_l2':max_chi,
            'max_resolution_relative':max_res,
            'all_native_times_high_gradient_x_ge_10':all(r['high_gradient_x_ge_10'] for r in rows),
            'x_rms_all_native_min':min(r['x_rms'] for r in rows),
            'x_rms_all_native_max':max(r['x_rms'] for r in rows),
            'x_rms_evaluation_min':min(r['x_rms'] for r in ev),
            'x_rms_evaluation_max':max(r['x_rms'] for r in ev),
            'screened_to_historical_x_ratio_eval_min':min(r['screened_to_historical_x_ratio'] for r in ev),
            'screened_to_historical_x_ratio_eval_max':max(r['screened_to_historical_x_ratio'] for r in ev),
            'numerical_pass':bool(numeric),'rows':rows,
        }

    input_gates={
        'artifact_grid_k_match_le_1e-12':inp['k_miss_max']<=1e-12,
        'z_trace_native_match_le_1e-12':inp['z_mismatch_max']<=1e-12,
        'minimum_8_evaluation_times':int(np.sum(eval_mask))>=8,
    }
    numeric_pass=bool(all(input_gates.values()) and all_numeric)
    if not numeric_pass:
        classification='NL1C5_SCREENED_QUASISTATIC_RECLOSURE_FAIL'
        diagnosis='NL1C5_NUMERICAL_OR_ACTION_RECLOSURE_FAILURE'
    elif not all_saturated:
        classification='NL1C5_SCREENED_RECLOSURE_TRANSITION_REQUIRES_FULL_J'
        diagnosis='SATURATED_HIGH_GRADIENT_ASSUMPTION_NOT_SELF_CONSISTENT'
    else:
        # The preregistered memory-source survival test is intentionally not
        # executed unless the saturated branch validates itself.
        classification='NL1C5_SCREENED_QUASISTATIC_RECLOSURE_PASS'
        diagnosis='SATURATED_RECLOSURE_VALID_MEMORY_SOURCE_TEST_REQUIRED'

    result={
        'classification':classification,'diagnosis':diagnosis,
        'scope':'published high-gradient AeST quasistatic field reclosure at fixed certified v0.77 total-matter state; no matter re-evolution, finite eta, collapse statistic, observation or likelihood',
        'physical_eta':0.0,'uses_observational_data':False,
        'frozen_inputs':{'H0_km_s_Mpc':H0,'omega_b':OMEGA_B,'omega_cdm':OMEGA_CDM,
                         'omega_nu_standard_0p06_over_93p14':OMEGA_NU,'omega_m':OMEGA_M,
                         'KB':KB,'K2':K2,'Q0_1_per_Mpc':Q0,'mu2_1_per_Mpc2':MU2,
                         'beta0_co_primary':BETA,'k_h_per_Mpc':K_H.tolist(),
                         'phases_rad':PHASE.tolist()},
        'input_audit':{'k_native_relative_miss_max':inp['k_miss_max'],
                       'z_trace_native_absolute_mismatch_max':inp['z_mismatch_max'],
                       'native_evaluation_times':int(np.sum(eval_mask))},
        'input_gates':input_gates,'branches':branches,
        'saturation_validity_all_beta_all_native_times':bool(all_saturated),
        'memory_source_survival_test_executed':False,
        'continuation_rule':('If the saturated reclosed field is not itself in x>=10 at every native bath time, do not evaluate/promote the saturated memory-survival result. Proceed to the already validated full-J quasistatic operator.'),
        'historical_results_unchanged':True,
    }
    Path(args.json_out).parent.mkdir(parents=True,exist_ok=True)
    Path(args.json_out).write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
