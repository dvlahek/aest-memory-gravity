#!/usr/bin/env python3
"""GE04 spectral-convergence characterization for the frozen GE03 DY2 source."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

import ge03.weakly_nonlinear_y_memory_cross_source as g3
import nl1c4.expanding_memory_source_trajectory as c4

RESOLUTIONS=(128,256,512,1024,2048,4096)
BETAS=np.asarray([1.0,0.5,0.1],float)
LAMBDAS=np.asarray([10.0,5.0,2.5,1.25],float)
TINY=1.0e-300
PAIR_STARTS=(128,256,512,1024,2048)
FIT_STARTS=(256,512,1024,2048)
AFFINITY_MAX=5.0e-3
COS_MIN=0.9999
FD_MAX=1.0e-4
N1024_2048_MAX=5.0e-4
P_MIN=0.5
BETA_MAX=1.0e-12


def pair_key(n):
    return f"{n}_{2*n}"


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--artifact-dir",required=True)
    ap.add_argument("--artifact-meta-json",required=True)
    ap.add_argument("--json-out",required=True)
    ap.add_argument("--npz-out",required=True)
    args=ap.parse_args()

    artifact=c4.validate_artifact_metadata(Path(args.artifact_meta_json))
    if not artifact.get("pass",False):
        raise RuntimeError(f"artifact provenance mismatch: {artifact}")

    ad=Path(args.artifact_dir)
    base_hist,k_miss,native_mismatch=g3.load_selected(ad/c4.TRACE_NAME)
    base_chi,tau,a,H=g3.history_arrays(base_hist)
    z=1.0/a-1.0
    eval_idx=np.where((z>=g3.ZMIN-1e-12)&(z<=g3.ZMAX+1e-12))[0]
    if eval_idx.size<8:
        raise RuntimeError(f"only {eval_idx.size} native evaluation times")

    tangents=[]
    k_miss_max=float(k_miss)
    grid_mismatch=float(native_mismatch)
    for lam in LAMBDAS:
        hp,kp,gp=g3.load_selected(ad/g3.trace_name("plus",lam))
        hm,km,gm=g3.load_selected(ad/g3.trace_name("minus",lam))
        k_miss_max=max(k_miss_max,kp,km)
        grid_mismatch=max(
            grid_mismatch,gp,gm,
            g3.compare_grid(base_hist,hp),
            g3.compare_grid(base_hist,hm),
        )
        cp,*_=g3.history_arrays(hp)
        cm,*_=g3.history_arrays(hm)
        tangents.append((cp-cm)/(2.0*float(lam)))
    tangents=np.asarray(tangents,float)

    widths=c4.log_trap_weights(c4.K_H)
    PR=c4.AS*(c4.K_MPC/c4.KPIV_MPC)**(c4.NS-1.0)
    amplitudes=np.sqrt(2.0*widths*PR)

    weighted=tangents[:,:,eval_idx]*amplitudes[None,:,None]
    vals=weighted.reshape(len(LAMBDAS),-1)
    mean_vec=np.mean(vals,axis=0)
    affinity=np.asarray(
        [g3.norm(vals[i]-mean_vec)/max(g3.norm(mean_vec),TINY) for i in range(len(LAMBDAS))],
        float,
    )
    cosines=np.asarray([g3.cosine(vals[i],mean_vec) for i in range(len(LAMBDAS))],float)
    affinity_pass=bool(np.max(affinity)<=AFFINITY_MAX and np.min(cosines)>=COS_MIN)
    chi11_modes=np.mean(tangents,axis=0)

    kfund=float(c4.K_MPC[0]/c4.FOURIER_N[0])

    rows=[]
    all_finite=True
    fd_max=0.0
    beta_max=0.0
    n1024_2048_max=0.0
    monotone_all=True
    p_min_observed=math.inf

    store_pair_errors=[]
    store_orders=[]

    for it in eval_idx:
        c0=amplitudes*base_chi[:,it]
        c1=amplitudes*chi11_modes[:,it]

        dy={}
        y2={}
        fd4096={}
        for nx in RESOLUTIONS:
            chi0=g3.reconstruct(c0,nx)
            chi1=g3.reconstruct(c1,nx)
            for beta in BETAS:
                key=(nx,float(beta))
                yy,_=g3.op_and_grad(chi0,a[it],kfund,beta)
                dd,gg,hh=g3.directional_analytic(chi0,chi1,a[it],kfund,beta)
                y2[key]=yy
                dy[key]=dd
                all_finite=bool(
                    all_finite
                    and np.all(np.isfinite(yy))
                    and np.all(np.isfinite(dd))
                    and np.all(np.isfinite(gg))
                    and np.all(np.isfinite(hh))
                )
                if nx==4096:
                    fd,step=g3.directional_fd(
                        chi0,chi1,a[it],kfund,beta,g3.FD_PRIMARY
                    )
                    fd4096[float(beta)]=(fd,step)
                    err=g3.rel_l2(dd,fd)
                    fd_max=max(fd_max,err)
                    all_finite=bool(all_finite and np.all(np.isfinite(fd)))

        per_beta={}
        for beta in BETAS:
            b=float(beta)
            pair_errors={}
            reference_errors={}
            for n in PAIR_STARTS:
                e=g3.rel_l2(
                    g3.low_coeff(dy[(n,b)]),
                    g3.low_coeff(dy[(2*n,b)]),
                )
                pair_errors[pair_key(n)]=float(e)
            ref=g3.low_coeff(dy[(4096,b)])
            for n in RESOLUTIONS[:-1]:
                reference_errors[str(n)]=float(
                    g3.rel_l2(g3.low_coeff(dy[(n,b)]),ref)
                )

            seq=np.asarray([pair_errors[pair_key(n)] for n in FIT_STARTS],float)
            monotone=bool(np.all(seq[1:]<=seq[:-1]*(1.0+1e-12)))
            monotone_all=bool(monotone_all and monotone)

            if np.any(seq<=0) or not np.all(np.isfinite(seq)):
                p=float("-inf")
            else:
                slope,_=np.polyfit(np.log(np.asarray(FIT_STARTS,float)),np.log(seq),1)
                p=float(-slope)
            p_min_observed=min(p_min_observed,p)

            e1024=float(pair_errors["1024_2048"])
            n1024_2048_max=max(n1024_2048_max,e1024)

            per_beta[str(b)]={
                "pairwise_low_mode_relative_errors":pair_errors,
                "relative_errors_to_N4096":reference_errors,
                "monotone_from_N256":monotone,
                "fitted_convergence_order":p,
                "analytic_vs_fd_at_N4096_relative_L2":float(
                    g3.rel_l2(dy[(4096,b)],fd4096[b][0])
                ),
            }

        refnorm=g3.norm(dy[(4096,1.0)])
        beta_rows={}
        for beta in BETAS:
            b=float(beta)
            measured=g3.norm(dy[(4096,b)])/max(refnorm,TINY)
            expected=2.0/(1.0+b)
            err=abs(measured-expected)/expected
            beta_max=max(beta_max,err)
            beta_rows[str(b)]={
                "measured_ratio_to_beta1":float(measured),
                "expected_ratio":float(expected),
                "relative_error":float(err),
            }

        yy=y2[(4096,1.0)]
        dd=dy[(4096,1.0)]
        rows.append({
            "native_index":int(it),
            "a":float(a[it]),
            "z":float(z[it]),
            "by_beta":per_beta,
            "beta_scaling":beta_rows,
            "Y2_beta1_L2_norm":g3.norm(yy),
            "DY2_beta1_L2_norm":g3.norm(dd),
            "two_DY2_over_two_Y2_norm_ratio_per_eta_tangent":float(
                g3.norm(2.0*dd)/max(g3.norm(2.0*yy),TINY)
            ),
            "Y2_DY2_cosine":g3.cosine(yy,dd),
        })
        store_pair_errors.append([
            per_beta["1.0"]["pairwise_low_mode_relative_errors"][pair_key(n)]
            for n in PAIR_STARTS
        ])
        store_orders.append(per_beta["1.0"]["fitted_convergence_order"])

    gates={
        "artifact_digest_exact":bool(artifact.get("pass",False)),
        "all_requested_k_relative_miss_le_1e12":bool(k_miss_max<=1e-12),
        "common_native_grid_relative_mismatch_le_1e12":bool(grid_mismatch<=1e-12),
        "chi11_four_lambda_affinity_pass":affinity_pass,
        "analytic_vs_fd_DY2_at_N4096_relative_L2_le_1e4":bool(fd_max<=FD_MAX),
        "beta0_scaling_relative_error_le_1e12":bool(beta_max<=BETA_MAX),
        "pairwise_error_monotone_decrease_from_N256":bool(monotone_all),
        "N1024_vs_N2048_low_mode_relative_L2_le_5e4":bool(n1024_2048_max<=N1024_2048_MAX),
        "fitted_convergence_order_ge_0p5":bool(p_min_observed>=P_MIN),
        "all_outputs_finite":bool(all_finite),
        "no_GE03_relabel_finite_eta_or_observational_input":True,
    }
    passed=bool(all(gates.values()))
    classification=(
        "GE04_DY2_SPECTRAL_CONVERGENCE_PASS"
        if passed else
        "GE04_DY2_SPECTRAL_CONVERGENCE_FAIL"
    )

    result={
        "classification":classification,
        "predata_classification":"GE04_PREDATA_DY2_SPECTRAL_CONVERGENCE_CHARACTERIZATION",
        "scope":"Resolution characterization of the frozen GE03/NL1B2 DY2 cross-source only. GE03 remains frozen FAIL.",
        "artifact_provenance":artifact,
        "frozen_resolutions":list(RESOLUTIONS),
        "trace_controls":{
            "requested_k_relative_miss_max":float(k_miss_max),
            "common_native_grid_relative_mismatch_max":float(grid_mismatch),
            "native_history_length":int(base_chi.shape[1]),
            "evaluation_times":int(eval_idx.size),
        },
        "chi11_affinity":{
            "relative_L2_by_lambda":{
                str(float(LAMBDAS[i])):float(affinity[i])
                for i in range(len(LAMBDAS))
            },
            "relative_L2_max":float(np.max(affinity)),
            "cosine_by_lambda":{
                str(float(LAMBDAS[i])):float(cosines[i])
                for i in range(len(LAMBDAS))
            },
            "cosine_min":float(np.min(cosines)),
            "pass":affinity_pass,
        },
        "summary":{
            "analytic_vs_fd_N4096_relative_L2_max":float(fd_max),
            "beta0_scaling_relative_error_max":float(beta_max),
            "N1024_vs_N2048_low_mode_relative_L2_max":float(n1024_2048_max),
            "minimum_fitted_convergence_order":float(p_min_observed),
            "pairwise_monotone_all_times_beta":bool(monotone_all),
        },
        "rows":rows,
        "gates":gates,
        "claim_boundary":"GE04 characterizes convergence only. It cannot relabel GE03 and does not solve Z21, introduce finite eta, or establish an observational result.",
    }

    out=Path(args.json_out)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2)+"\n")
    np.savez_compressed(
        args.npz_out,
        resolutions=np.asarray(RESOLUTIONS,int),
        pair_starts=np.asarray(PAIR_STARTS,int),
        z=np.asarray([r["z"] for r in rows],float),
        pair_errors_beta1=np.asarray(store_pair_errors,float),
        fitted_orders_beta1=np.asarray(store_orders,float),
        affinity=affinity,
        cosines=cosines,
    )
    print(json.dumps(result,indent=2))


if __name__=="__main__":
    main()
