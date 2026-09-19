#!/usr/bin/env python3
"""GE03 weakly nonlinear Y-memory cross-source.

Uses the retained v0.77 accepted-source traces to reconstruct the baseline
chi10 direction and the eta=0 memory tangent chi11, then evaluates the exact
NL1B2 directional derivative of the NL0C/NL1A Y-sector operator.

Theory-only. No finite eta, no Z21 solve, no collapse, no observations.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

import nl1c4.expanding_memory_source_trajectory as c4

LAMBDAS=np.asarray([10.0,5.0,2.5,1.25],float)
BETAS=np.asarray([1.0,0.5,0.1],float)
NX_VALUES=(256,512)
FD_PRIMARY=1.0e-4
FD_CONTROL=3.0e-5
AFFINITY_MAX=5.0e-3
COS_MIN=0.9999
FD_REL_MAX=1.0e-4
NX_REL_MAX=5.0e-4
BETA_REL_MAX=1.0e-12
TINY=1.0e-300
ZMIN,ZMAX=0.2,1.5
LOW_MMAX=32


def norm(x):
    return float(np.linalg.norm(np.asarray(x)))


def rel_l2(a,b):
    aa=np.asarray(a); bb=np.asarray(b)
    return float(np.linalg.norm(aa-bb)/max(np.linalg.norm(aa),np.linalg.norm(bb),TINY))


def cosine(a,b):
    aa=np.asarray(a,float).ravel(); bb=np.asarray(b,float).ravel()
    return float(np.dot(aa,bb)/max(np.linalg.norm(aa)*np.linalg.norm(bb),TINY))


def trace_name(sign,lam):
    tag=str(float(lam)).replace('.','p')
    return f"v076_v077_{sign}_{tag}_trace.dat"


def load_selected(path):
    rows=c4.read_trace(Path(path))
    histories,k_miss,native_mismatch=c4.select_and_align(rows)
    return histories,float(k_miss),float(native_mismatch)


def history_arrays(histories):
    # shape: mode,time
    chi=np.asarray([[r['chi'] for r in h] for h in histories],float)
    tau=np.asarray([r['tau'] for r in histories[0]],float)
    a=np.asarray([r['a'] for r in histories[0]],float)
    H=np.asarray([r['H_over_H0'] for r in histories[0]],float)
    return chi,tau,a,H


def compare_grid(ref_hist,cur_hist):
    _,tr,ar,Hr=history_arrays(ref_hist)
    _,tc,ac,Hc=history_arrays(cur_hist)
    if tr.shape!=tc.shape:
        return math.inf
    vals=[]
    for x,y in ((tr,tc),(ar,ac),(Hr,Hc)):
        vals.append(float(np.max(np.abs(x-y)/np.maximum(np.maximum(np.abs(x),np.abs(y)),1.0))))
    return max(vals)


def mask23(n):
    m=np.fft.fftfreq(n)*n
    return (np.abs(m)<=n/3.0+1.0e-12).astype(float)


def mvec(n):
    return np.fft.fftfreq(n)*n


def op_and_grad(chi,a,kfund,beta):
    n=len(chi); mm=mvec(n)
    ch=np.fft.fft(chi)
    fac=float(kfund/a)
    g=np.fft.ifft(1j*mm*ch).real*fac
    flux=np.abs(g)*g
    fh=np.fft.fft(flux)*mask23(n)
    src=np.fft.ifft(1j*mm*fh).real*fac/(1.0+float(beta))
    return src,g


def directional_analytic(chi0,chi1,a,kfund,beta):
    n=len(chi0); mm=mvec(n); fac=float(kfund/a)
    _,g=op_and_grad(chi0,a,kfund,0.0)
    h=np.fft.ifft(1j*mm*np.fft.fft(chi1)).real*fac
    ag=np.abs(g)
    directional=np.zeros_like(g)
    nz=ag>0.0
    directional[nz]=ag[nz]*h[nz]+(g[nz]*h[nz]/ag[nz])*g[nz]
    fh=np.fft.fft(directional)*mask23(n)
    out=np.fft.ifft(1j*mm*fh).real*fac/(1.0+float(beta))
    return out,g,h


def directional_fd(chi0,chi1,a,kfund,beta,hrel):
    scale=float(hrel)*norm(chi0)/max(norm(chi1),TINY)
    if not np.isfinite(scale) or scale<=0:
        raise RuntimeError("invalid finite-difference direction scale")
    op_p,_=op_and_grad(chi0+scale*chi1,a,kfund,beta)
    op_m,_=op_and_grad(chi0-scale*chi1,a,kfund,beta)
    return (op_p-op_m)/(2.0*scale),scale


def low_coeff(a,mmax=LOW_MMAX):
    h=np.fft.fft(np.asarray(a,float))/len(a)
    return h[:mmax+1]


def reconstruct(coeff,n):
    theta=2.0*np.pi*np.arange(n,dtype=float)/n
    return np.sum(
        coeff[:,None]*np.cos(c4.FOURIER_N[:,None]*theta[None,:]+c4.PHASES[:,None]),
        axis=0,
    )


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--artifact-dir",required=True)
    ap.add_argument("--artifact-meta-json",required=True)
    ap.add_argument("--json-out",required=True)
    ap.add_argument("--npz-out",required=True)
    args=ap.parse_args()

    ad=Path(args.artifact_dir)
    artifact=c4.validate_artifact_metadata(Path(args.artifact_meta_json))
    if not artifact.get('pass',False):
        raise RuntimeError(f"artifact provenance mismatch: {artifact}")

    base_hist,k_miss,native_mismatch=load_selected(ad/c4.TRACE_NAME)
    base_chi,tau,a,H=history_arrays(base_hist)
    z=1.0/a-1.0
    eval_idx=np.where((z>=ZMIN-1e-12)&(z<=ZMAX+1e-12))[0]
    if eval_idx.size<8:
        raise RuntimeError(f"only {eval_idx.size} native evaluation times")

    tangent_modes=[]
    grid_mismatch=float(native_mismatch)
    k_miss_max=float(k_miss)
    for lam in LAMBDAS:
        hp,kp,gp=load_selected(ad/trace_name('plus',lam))
        hm,km,gm=load_selected(ad/trace_name('minus',lam))
        k_miss_max=max(k_miss_max,kp,km)
        grid_mismatch=max(grid_mismatch,gp,gm,compare_grid(base_hist,hp),compare_grid(base_hist,hm))
        cp,tp,ap_,Hp=history_arrays(hp)
        cm,tm,am_,Hm=history_arrays(hm)
        tangent_modes.append((cp-cm)/(2.0*float(lam)))
    tangent_modes=np.asarray(tangent_modes,float)  # lambda,mode,time

    widths=c4.log_trap_weights(c4.K_H)
    PR=c4.AS*(c4.K_MPC/c4.KPIV_MPC)**(c4.NS-1.0)
    amplitudes=np.sqrt(2.0*widths*PR)

    # Four-lambda affinity on physically weighted retained mode coefficients
    # over the frozen native time window.
    weighted=tangent_modes[:,:,eval_idx]*amplitudes[None,:,None]
    vals=weighted.reshape(len(LAMBDAS),-1)
    mean_vec=np.mean(vals,axis=0)
    den=max(norm(mean_vec),TINY)
    affinity=np.asarray([norm(vals[i]-mean_vec)/den for i in range(len(LAMBDAS))],float)
    cosines=np.asarray([cosine(vals[i],mean_vec) for i in range(len(LAMBDAS))],float)
    affinity_pass=bool(np.max(affinity)<=AFFINITY_MAX and np.min(cosines)>=COS_MIN)

    chi11_modes=np.mean(tangent_modes,axis=0)
    kfund=float(c4.K_MPC[0]/c4.FOURIER_N[0])

    rows=[]
    fd_max=0.0; fd_control_max=0.0; nx_max=0.0; beta_max=0.0
    all_finite=True
    store_y=[]; store_dy=[]; store_z=[]

    for it in eval_idx:
        c0=amplitudes*base_chi[:,it]
        c1=amplitudes*chi11_modes[:,it]
        by_nx={}
        for nx in NX_VALUES:
            chi0=reconstruct(c0,nx)
            chi1=reconstruct(c1,nx)
            beta_outputs={}
            for beta in BETAS:
                y0,_=op_and_grad(chi0,a[it],kfund,beta)
                dy,g,h=directional_analytic(chi0,chi1,a[it],kfund,beta)
                fd_p,step_p=directional_fd(chi0,chi1,a[it],kfund,beta,FD_PRIMARY)
                fd_c,step_c=directional_fd(chi0,chi1,a[it],kfund,beta,FD_CONTROL)
                efd=rel_l2(dy,fd_p)
                ect=rel_l2(fd_p,fd_c)
                fd_max=max(fd_max,efd); fd_control_max=max(fd_control_max,ect)
                all_finite=bool(all_finite and all(np.all(np.isfinite(v)) for v in (y0,dy,fd_p,fd_c,g,h)))
                beta_outputs[float(beta)]={
                    'Y2':y0,'DY2':dy,'fd_primary':fd_p,'fd_control':fd_c,
                    'fd_relative_error':efd,'fd_control_relative_error':ect,
                    'step_primary':step_p,'step_control':step_c,
                }
            by_nx[nx]=beta_outputs

        # Low-mode resolution at each beta.
        nx_rows={}
        for beta in BETAS:
            c256=low_coeff(by_nx[256][float(beta)]['DY2'])
            c512=low_coeff(by_nx[512][float(beta)]['DY2'])
            en=rel_l2(c256,c512)
            nx_max=max(nx_max,en)
            nx_rows[str(float(beta))]=en

        # beta scaling at primary spatial resolution, relative to beta=1.
        ref=norm(by_nx[512][1.0]['DY2'])
        beta_rows={}
        for beta in BETAS:
            measured=norm(by_nx[512][float(beta)]['DY2'])/max(ref,TINY)
            expected=2.0/(1.0+float(beta))
            eb=abs(measured-expected)/expected
            beta_max=max(beta_max,eb)
            beta_rows[str(float(beta))]={
                'measured_ratio_to_beta1':measured,
                'expected_ratio':expected,
                'relative_error':eb,
            }

        # Descriptive physical source geometry for beta=1 at primary Nx.
        y=by_nx[512][1.0]['Y2']
        dy=by_nx[512][1.0]['DY2']
        ratio=norm(2.0*dy)/max(norm(2.0*y),TINY)
        inner=float(np.mean(y*dy))
        row={
            'native_index':int(it),
            'a':float(a[it]),'z':float(z[it]),
            'Y2_beta1_L2_norm':norm(y),
            'DY2_beta1_L2_norm':norm(dy),
            'two_DY2_over_two_Y2_norm_ratio_per_eta_tangent':ratio,
            'Y2_DY2_cosine':cosine(y,dy),
            'Y2_DY2_mean_inner_product':inner,
            'analytic_vs_fd_relative_error_max_over_beta':max(by_nx[512][float(b)]['fd_relative_error'] for b in BETAS),
            'fd_primary_vs_control_relative_error_max_over_beta':max(by_nx[512][float(b)]['fd_control_relative_error'] for b in BETAS),
            'Nx256_vs_Nx512_low_mode_relative_error_by_beta':nx_rows,
            'beta_scaling':beta_rows,
        }
        rows.append(row)
        store_y.append(y)
        store_dy.append(dy)
        store_z.append(z[it])

    gates={
        'artifact_digest_exact':bool(artifact.get('pass',False)),
        'all_requested_k_relative_miss_le_1e12':bool(k_miss_max<=1e-12),
        'common_native_grid_relative_mismatch_le_1e12':bool(grid_mismatch<=1e-12),
        'at_least_8_native_times':bool(eval_idx.size>=8),
        'chi11_four_lambda_affinity_pass':affinity_pass,
        'analytic_vs_fd_DY2_relative_L2_le_1e4':bool(fd_max<=FD_REL_MAX),
        'primary_vs_control_fd_DY2_relative_L2_le_1e4':bool(fd_control_max<=FD_REL_MAX),
        'Nx256_vs_Nx512_low_mode_DY2_relative_L2_le_5e4':bool(nx_max<=NX_REL_MAX),
        'beta0_scaling_relative_error_le_1e12':bool(beta_max<=BETA_REL_MAX),
        'all_outputs_finite':bool(all_finite),
        'no_finite_eta_or_observational_input':True,
    }
    passed=bool(all(gates.values()))
    classification=(
        'GE03_WEAKLY_NONLINEAR_Y_MEMORY_CROSS_SOURCE_PASS'
        if passed else 'GE03_WEAKLY_NONLINEAR_Y_MEMORY_CROSS_SOURCE_FAIL'
    )

    result={
        'classification':classification,
        'predata_classification':'GE03_PREDATA_WEAKLY_NONLINEAR_Y_MEMORY_CROSS_SOURCE',
        'uses_observational_data':False,
        'finite_physical_eta':False,
        'scope':'Exact NL1B2 weakly nonlinear Y-memory directional cross-source on retained v0.77 native traces; no Z21 solve and no nonlinear collapse.',
        'artifact_provenance':artifact,
        'frozen_model':{
            'KB':0.0665,'a0_m_s2':1.2e-10,'beta0':[1.0,0.5,0.1],
            'tauH0':10.0,'lambdas':LAMBDAS.tolist(),
        },
        'trace_controls':{
            'requested_k_relative_miss_max':k_miss_max,
            'common_native_grid_relative_mismatch_max':grid_mismatch,
            'native_history_length':int(base_chi.shape[1]),
            'evaluation_times':int(eval_idx.size),
        },
        'chi11_affinity':{
            'relative_L2_by_lambda':{str(float(LAMBDAS[i])):float(affinity[i]) for i in range(len(LAMBDAS))},
            'relative_L2_max':float(np.max(affinity)),
            'cosine_by_lambda':{str(float(LAMBDAS[i])):float(cosines[i]) for i in range(len(LAMBDAS))},
            'cosine_min':float(np.min(cosines)),
            'pass':affinity_pass,
        },
        'operator_controls':{
            'analytic_vs_fd_relative_L2_max':fd_max,
            'fd_primary_vs_control_relative_L2_max':fd_control_max,
            'Nx256_vs_Nx512_low_mode_relative_L2_max':nx_max,
            'beta0_scaling_relative_error_max':beta_max,
        },
        'rows':rows,
        'gates':gates,
        'claim_boundary':'PASS certifies the weakly nonlinear Y-memory cross-source entering the exact eta=0 second-order hierarchy. It does not solve Z21, introduce finite eta, simulate collapse, or establish observational evidence.',
    }

    out=Path(args.json_out); out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2)+'\n')
    np.savez_compressed(
        args.npz_out,
        lambdas=LAMBDAS,
        beta0=BETAS,
        z=np.asarray(store_z,float),
        Y2_beta1=np.asarray(store_y,float),
        DY2_beta1=np.asarray(store_dy,float),
        chi11_mode_tangents=tangent_modes,
        chi11_mode_consensus=chi11_modes,
        affinity=affinity,
        cosines=cosines,
    )
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
