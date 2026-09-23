#!/usr/bin/env python3
"""GE19 Repair38 — frozen-source Radau substep localization.

Diagnostic only.

Repair38 does not recompute the H4 source and does not rerun Repair37 as a
science certification.  It loads the frozen Repair37 Nt128 total H4 source
arrays and frozen projected p0, keeps the Repair07 PCHIP stage-source
representation and two-stage Radau IIA tableau, and varies only the number
of internal Radau substeps per frozen Nt128 interval: 1, 2, 4.

The output remains sampled on the original Nt128 nodes.  The Repair37 active
mask is frozen from the Repair37 primary shift-scale arrays.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

import ge19.repair07_window_retarded_reduced_h3_z20_particular as r7
import ge19.repair11_lambda_inclusive_reduced_h1_reclosure as r11
import ge19.repair13_self_consistent_reduced_background_h1_reclosure as r13
import ge19.repair24_q20_construction as r24

TINY=1e-300
EPS=float(np.finfo(float).eps)
SQRT_EPS=float(np.sqrt(EPS))

R37_JSON_SHA="da8f2f00c22c866ec3f82381d23f69bf036e630fe2a29c5c44657984b760f61a"
R37_NPZ_SHA="572d8937c1d742b10da66e34cc076377c1b2feb20b8f72eb25c3eaf31a59829f"
R13_NPZ_SHA="011c0ae54fd21d70c0e2c695ce62e7b74a3c5529a07c9023c882a447d5b40ca3"
GE15_DENSE_SHA="7f57ab676f2a31cf0abf93ff0f8b0f1f2f80bb9a58d7cf1e47e10a158c57c69f"

SUBSTEP_FACTORS=(1,2,4)
SCIENCE_SHIFT_TARGET=1e-6
ORDER_CONFIRM_MIN=2.5
MATERIAL_RATIO_MAX=0.8
REPRO_STATE_MAX=1e-11
REPRO_SHIFT_MAX=1e-10
FROZEN_ACTIVE_COUNT=23850


def sha256(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1<<20),b""):
            h.update(block)
    return h.hexdigest()


def rel_l2(a,b)->float:
    aa=np.asarray(a)
    bb=np.asarray(b)
    return float(np.linalg.norm(aa-bb)/max(np.linalg.norm(aa),np.linalg.norm(bb),TINY))


def observed_order(ec,ef)->float:
    if not (np.isfinite(ec) and np.isfinite(ef) and ec>0.0 and ef>0.0):
        return float("nan")
    return float(math.log(ec/ef)/math.log(2.0))


def load_frozen_inputs(rd:Path):
    paths={
        "r37j":rd/"ge19_repair37_cancellation_safe_fd8_h4_z21_reclosure.json",
        "r37n":rd/"ge19_repair37_cancellation_safe_fd8_h4_z21_reclosure.npz",
        "r13n":rd/"ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz",
        "dense":rd/"ge15_R1_dense_accepted_step_trace.dat",
        "lambda":rd/"ge15_R1_cli_background.dat",
    }
    missing=[str(p) for p in paths.values() if not p.exists()]
    if missing:
        raise RuntimeError("missing Repair38 frozen inputs: "+", ".join(missing))

    expected={
        "r37j":R37_JSON_SHA,
        "r37n":R37_NPZ_SHA,
        "r13n":R13_NPZ_SHA,
        "dense":GE15_DENSE_SHA,
    }
    hashes={}
    for key,h in expected.items():
        got=sha256(paths[key])
        hashes[key]=got
        if got!=h:
            raise RuntimeError(f"{key} hash mismatch: {got} != {h}")

    report=json.loads(paths["r37j"].read_text())
    if report.get("classification")!="GE19_REPAIR37_CANCELLATION_SAFE_FD8_H4_Z21_RECLOSURE_FAIL":
        raise RuntimeError("Repair37 frozen JSON classification mismatch")
    gates=report.get("gates",{})
    false_gates=[k for k,v in gates.items() if v is not True]
    if false_gates!=["H4_active_shift_Nt128_Linf_le_1e6"]:
        raise RuntimeError(f"Repair37 frozen false-gate set mismatch: {false_gates}")
    if report.get("Z21_window_local_particular_certified") is not False:
        raise RuntimeError("Repair37 unexpectedly certified Z21")

    return paths,hashes,report,np.load(paths["r37n"]),np.load(paths["r13n"])


def build_frozen_operator_context(rd:Path,r13npz):
    bgs,_=r24.reconstruct_backgrounds(r7,r11,r13,rd,r13npz)

    lambda_by_bg={}
    for key,bg in bgs.items():
        rho=np.asarray(bg["rho_lambda_action"],float)
        if rho.shape!=np.asarray(bg["x"],float).shape or not np.all(np.isfinite(rho)):
            raise RuntimeError(f"invalid rho_lambda_action for {key}")
        lambda_by_bg[id(bg)]=rho
    lambda_diag=r11.install_lambda_operator(r7,lambda_by_bg)

    mod6f=r7.load_frozen_generator(
        ROOT/"ge06/analytic_aest_directional_source_generator.py","ge06r38"
    )
    mod6=r7.build_stable_ge06_generator_v2(mod6f)
    mod7=r7.load_frozen_generator(
        ROOT/"ge07/pressureless_matter_directional_source_generator.py","ge07r38"
    )
    return bgs,mod6,mod7,lambda_diag


def frozen_source_by_beta(r37npz,tag):
    out={}
    for ib,beta in enumerate(r7.BETAS):
        out[float(beta)]={
            "rhs":np.asarray(r37npz[f"primary_{tag}_beta{ib}_total_main"],complex),
            "rhs_constraint":np.asarray(
                r37npz[f"primary_{tag}_beta{ib}_total_constraint"],complex
            ),
        }
    return out


def radau2_integrate_substepped(
    mod6,mod7,bg,tag,k,y0,rhsfun,conrhsfun,substeps:int
):
    """Repair07 two-stage Radau IIA with only internal step subdivision changed."""
    if substeps<1:
        raise ValueError("substeps must be >=1")
    x=np.asarray(bg["x"],float)
    Y0=np.asarray(y0,complex)
    if Y0.ndim==1:
        Y0=Y0[:,None]
    ncol=Y0.shape[1]
    Y=np.empty((ncol,8,len(x)),complex)
    Y[:,:,0]=Y0.T

    a11=5.0/12.0; a12=-1.0/12.0
    a21=3.0/4.0; a22=1.0/4.0
    b1=3.0/4.0; b2=1.0/4.0
    c1=1.0/3.0; c2=1.0

    cur=Y0.copy()
    I=np.eye(8,dtype=complex)
    step_res=[]
    step_cond=[]
    local_cond=[]
    local_zero=[]

    for i in range(len(x)-1):
        H=float(x[i+1]-x[i])
        h=H/float(substeps)
        for isub in range(substeps):
            # Preserve Repair07's c2=1 domain-safety exactly.  Computing the
            # right stage as xl+h can overshoot x[i+1] by a few ULPs after
            # subdivision, which makes the frozen extrapolate=False PCHIP
            # Lambda/source interpolators return NaN.  Bind every substep to
            # its parent interval and use the exact parent right endpoint for
            # the final internal substep.
            xl=float(x[i]+isub*h)
            xr=(
                float(x[i+1])
                if isub==substeps-1
                else float(x[i]+(isub+1)*h)
            )
            hs=float(xr-xl)
            x1=float(xl+c1*hs)
            x2=xr

            M1,Fmap1,*rest1=r7._canonical_operator_matrices(
                mod6,mod7,bg,tag,k,x1
            )
            M2,Fmap2,*rest2=r7._canonical_operator_matrices(
                mod6,mod7,bg,tag,k,x2
            )
            d1=rest1[-1]; d2=rest2[-1]
            local_cond.extend([
                d1["algebraic_scaled_condition_2"],
                d2["algebraic_scaled_condition_2"],
            ])
            local_zero.extend([
                d1["raw_zero_output_abs_max"],
                d2["raw_zero_output_abs_max"],
            ])

            R1=np.asarray(rhsfun(x1),complex)
            R2=np.asarray(rhsfun(x2),complex)
            C1=np.asarray(conrhsfun(x1),complex)
            C2=np.asarray(conrhsfun(x2),complex)
            if R1.ndim==1: R1=R1[:,None]
            if R2.ndim==1: R2=R2[:,None]
            if C1.ndim==1: C1=C1[:,None]
            if C2.ndim==1: C2=C2[:,None]

            S1=np.vstack([R1,C1])
            S2=np.vstack([R2,C2])
            F1=Fmap1@S1
            F2=Fmap2@S2

            K=np.block([
                [I-h*a11*M1, -h*a12*M2],
                [-h*a21*M1, I-h*a22*M2],
            ])
            RHS=np.vstack([
                cur+h*(a11*F1+a12*F2),
                cur+h*(a21*F1+a22*F2),
            ])
            stages,diag=r7._dense_equilibrated_solve(K,RHS)
            Y1=stages[:8]
            Y2=stages[8:]
            G1=M1@Y1+F1
            G2=M2@Y2+F2
            cur=cur+h*(b1*G1+b2*G2)

            step_res.append(diag["scaled_relative_L2_residual_max"])
            step_cond.append(diag["scaled_condition_2"])

        Y[:,:,i+1]=cur.T

    return Y,{
        "radau_block_scaled_relative_L2_residual_max":float(max(step_res,default=0.0)),
        "radau_scaled_condition_2_max":float(max(step_cond,default=0.0)),
        "local_algebraic_scaled_condition_2_max":float(max(local_cond,default=0.0)),
        "raw_zero_output_abs_max":float(max(local_zero,default=0.0)),
    }


def shift_trace_from_canonical(mod6,mod7,bg,tag,k,Y,rhsfun,confun):
    ncol,_,nt=Y.shape
    metric=np.empty((ncol,nt),float)
    absres=np.empty((ncol,nt),float)
    scale=np.empty((ncol,nt),float)
    for it,xq in enumerate(bg["x"]):
        rr=np.asarray(rhsfun(float(xq)),complex)
        rc=np.asarray(confun(float(xq)),complex)
        if rr.ndim==1: rr=rr[:,None]
        if rc.ndim==1: rc=rc[:,None]
        M,F,ZY,ZR,WY,WR,Cmat,bp,opdiag=r7._canonical_operator_matrices(
            mod6,mod7,bg,tag,k,float(xq)
        )
        for j in range(ncol):
            src=np.concatenate([rr[:,j],rc[:,j]])
            w=WY@Y[j,:,it]+WR@src
            sm=r7._constraint_backward_error(
                Cmat[10]+Cmat[11],w,rc[0,j],Cmat[10]@w,Cmat[11]@w
            )
            metric[j,it]=sm["metric"]
            absres[j,it]=sm["absolute_residual"]
            scale[j,it]=sm["scale"]
    return metric,absres,scale


def frozen_active_masks(r37npz):
    sref=max(
        float(np.max(r37npz[f"{tag}_shift_scale_primary"]))
        for tag in r7.C_TAGS
    )
    threshold=SQRT_EPS*sref
    masks={}
    count=0
    for tag in r7.C_TAGS:
        scale=np.asarray(r37npz[f"{tag}_shift_scale_primary"],float)
        mask=scale>threshold
        masks[tag]=mask
        count+=int(np.count_nonzero(mask))
    return sref,threshold,masks,count


def run_factor(factor,bgs,mod6,mod7,r37npz):
    nt=128
    states={}
    metrics={}
    absres={}
    scales={}
    p0_loaded={}
    radau_res=0.0
    finite=True

    xref=np.asarray(r37npz["x_primary"],float)

    for tag in r7.C_TAGS:
        bg=bgs[(nt,tag)]
        if not np.array_equal(np.asarray(bg["x"],float),xref):
            raise RuntimeError(f"Repair38 x-grid mismatch for {tag}")

        source=frozen_source_by_beta(r37npz,tag)
        p0=np.asarray(r37npz[f"{tag}_projected_p0_primary"],complex)
        frozen_state=np.asarray(r37npz[f"{tag}_Z21_primary"],complex)

        nb=len(r7.BETAS)
        nm=len(r7.M_SOLVE)
        st=np.empty_like(frozen_state)
        mt=np.empty((nb,nm,nt),float)
        at=np.empty_like(mt)
        sc=np.empty_like(mt)

        for jm,m in enumerate(r7.M_SOLVE):
            k=float(m*r7.g9.K_REQ[0]/r7.FOURIER_N[0])
            rhsfun,confun=r7._source_interp(xref,source,m)

            y0=np.zeros((8,nb),complex)
            y0[4:8,:]=p0[:,jm,:].T

            Y,rdiag=radau2_integrate_substepped(
                mod6,mod7,bg,tag,k,y0,rhsfun,confun,factor
            )
            state,dd,odiag=r7._reconstruct_canonical_solution(
                mod6,mod7,bg,tag,k,Y,rhsfun,confun
            )
            mtr,atr,scr=shift_trace_from_canonical(
                mod6,mod7,bg,tag,k,Y,rhsfun,confun
            )

            st[:,jm]=state
            mt[:,jm]=mtr
            at[:,jm]=atr
            sc[:,jm]=scr
            radau_res=max(
                radau_res,
                float(rdiag["radau_block_scaled_relative_L2_residual_max"]),
                float(odiag["algebraic_scaled_relative_L2_residual_max"]),
                float(odiag["lapse_noether_row_relative_residual_max"]),
            )
            finite=bool(
                finite
                and np.all(np.isfinite(Y))
                and np.all(np.isfinite(state))
                and np.all(np.isfinite(mtr))
                and np.all(np.isfinite(atr))
                and np.all(np.isfinite(scr))
            )

        # The full per-tag arrays are initialized with np.empty and become
        # meaningful only after every Fourier mode has been filled.  Do not
        # inspect future uninitialized mode slots inside the loop above.
        finite=bool(
            finite
            and np.all(np.isfinite(st))
            and np.all(np.isfinite(mt))
            and np.all(np.isfinite(at))
            and np.all(np.isfinite(sc))
        )

        states[tag]=st
        metrics[tag]=mt
        absres[tag]=at
        scales[tag]=sc
        p0_loaded[tag]=p0

    return {
        "states":states,
        "metrics":metrics,
        "absres":absres,
        "scales":scales,
        "p0":p0_loaded,
        "linear_residual_max":float(radau_res),
        "all_outputs_finite":bool(finite),
    }


def active_summary(run,masks):
    vals=[]
    absvals=[]
    for tag in r7.C_TAGS:
        mask=masks[tag]
        vals.extend(np.asarray(run["metrics"][tag][mask],float).tolist())
        absvals.extend(np.asarray(run["absres"][tag][mask],float).tolist())
    v=np.asarray(vals,float)
    a=np.asarray(absvals,float)
    if v.size==0:
        raise RuntimeError("no frozen active samples")
    return {
        "active_sample_count":int(v.size),
        "Linf":float(np.max(v)),
        "RMS":float(np.sqrt(np.mean(v**2))),
        "median":float(np.median(v)),
        "max_absolute_residual":float(np.max(a)),
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--results-dir",default=str(ROOT/"results"))
    ap.add_argument("--json-out",required=True)
    ap.add_argument("--npz-out",required=True)
    args=ap.parse_args()

    rd=Path(args.results_dir)
    paths,hashes,r37json,r37npz,r13npz=load_frozen_inputs(rd)
    bgs,mod6,mod7,lambda_diag=build_frozen_operator_context(rd,r13npz)

    sref,null_thr,masks,active_count=frozen_active_masks(r37npz)
    if active_count!=FROZEN_ACTIVE_COUNT:
        raise RuntimeError(
            f"frozen Repair37 active count mismatch: {active_count} != {FROZEN_ACTIVE_COUNT}"
        )

    runs={}
    summaries={}
    for factor in SUBSTEP_FACTORS:
        runs[factor]=run_factor(factor,bgs,mod6,mod7,r37npz)
        summaries[factor]=active_summary(runs[factor],masks)

    # Factor 1 must reproduce the frozen Repair37 propagation.
    frozen_states=np.concatenate([
        np.asarray(r37npz[f"{tag}_Z21_primary"],complex).ravel()
        for tag in r7.C_TAGS
    ])
    factor1_states=np.concatenate([
        np.asarray(runs[1]["states"][tag],complex).ravel()
        for tag in r7.C_TAGS
    ])
    state_repro=rel_l2(factor1_states,frozen_states)

    frozen_metrics=np.concatenate([
        np.asarray(r37npz[f"{tag}_shift_metric_primary"],float).ravel()
        for tag in r7.C_TAGS
    ])
    factor1_metrics=np.concatenate([
        np.asarray(runs[1]["metrics"][tag],float).ravel()
        for tag in r7.C_TAGS
    ])
    shift_repro=rel_l2(factor1_metrics,frozen_metrics)

    p0_exact=all(
        np.array_equal(
            np.asarray(runs[1]["p0"][tag],complex),
            np.asarray(r37npz[f"{tag}_projected_p0_primary"],complex)
        )
        for tag in r7.C_TAGS
    )

    e1=summaries[1]["Linf"]
    e2=summaries[2]["Linf"]
    e4=summaries[4]["Linf"]
    r12=float(e2/max(e1,TINY))
    r24=float(e4/max(e2,TINY))
    p12=observed_order(e1,e2)
    p24=observed_order(e2,e4)

    q1=summaries[1]["RMS"]
    q2=summaries[2]["RMS"]
    q4=summaries[4]["RMS"]
    rp12=observed_order(q1,q2)
    rp24=observed_order(q2,q4)

    implementation_gates={
        "Repair37_hashes_and_classification_exact":True,
        "frozen_active_sample_count_exact":bool(active_count==FROZEN_ACTIVE_COUNT),
        "factor1_Z21_global_relative_L2_le_1e11":bool(state_repro<=REPRO_STATE_MAX),
        "factor1_shift_metric_global_relative_L2_le_1e10":bool(shift_repro<=REPRO_SHIFT_MAX),
        "factor1_projected_p0_exact":bool(p0_exact),
        "all_outputs_finite":bool(all(runs[f]["all_outputs_finite"] for f in SUBSTEP_FACTORS)),
    }
    impl_ok=bool(all(implementation_gates.values()))

    radau_confirmed=bool(
        impl_ok
        and r12<=MATERIAL_RATIO_MAX
        and np.isfinite(p12) and p12>=ORDER_CONFIRM_MIN
        and e2<=SCIENCE_SHIFT_TARGET
        and e4<=SCIENCE_SHIFT_TARGET
    )
    accuracy_dependence=bool(
        impl_ok
        and (r12<=MATERIAL_RATIO_MAX or r24<=MATERIAL_RATIO_MAX)
    )

    if not impl_ok:
        route="IMPLEMENTATION_FAIL"
        classification="GE19_REPAIR38_FROZEN_SOURCE_RADAU_SUBSTEP_LOCALIZATION_IMPLEMENTATION_FAIL"
    elif radau_confirmed:
        route="RADAU_PROPAGATION_FLOOR_CONFIRMED"
        classification="GE19_REPAIR38_FROZEN_SOURCE_RADAU_SUBSTEP_LOCALIZATION_COMPLETE"
    elif accuracy_dependence:
        route="PROPAGATION_ACCURACY_DEPENDENCE_CONFIRMED"
        classification="GE19_REPAIR38_FROZEN_SOURCE_RADAU_SUBSTEP_LOCALIZATION_COMPLETE"
    else:
        route="PCHIP_OR_OTHER_FLOOR_REMAINS"
        classification="GE19_REPAIR38_FROZEN_SOURCE_RADAU_SUBSTEP_LOCALIZATION_COMPLETE"

    lrows=list(lambda_diag.values())
    report={
        "classification":classification,
        "predata_classification":"GE19_REPAIR38_PREDATA_FROZEN_SOURCE_RADAU_SUBSTEP_LOCALIZATION",
        "diagnostic_only":True,
        "uses_observational_data":False,
        "finite_physical_eta":False,
        "provenance":{
            "input_sha256":hashes,
            "Repair37_classification":r37json["classification"],
            "Repair37_false_gates":[k for k,v in r37json["gates"].items() if v is not True],
            "Repair37_relabelled":False,
        },
        "frozen_contract":{
            "H4_source_recomputed":False,
            "source_arrays":"Repair37 frozen primary total_main/total_constraint",
            "projected_p0_recomputed":False,
            "projected_p0":"Repair37 frozen primary projected_p0",
            "source_stage_interpolator":"Repair07 PchipInterpolator on frozen Nt128 source grid",
            "Radau_tableau":"Repair07 two-stage Radau IIA",
            "substep_factors":list(SUBSTEP_FACTORS),
            "output_grid":"frozen Repair37 Nt128 nodes",
            "science_shift_target_report_only":SCIENCE_SHIFT_TARGET,
            "threshold_relaxed":False,
        },
        "Lambda_operator":{
            "stage_evaluation_count":int(len(lrows)),
            "all_stage_rho_finite":bool(
                lrows and all(np.isfinite(q["rho_lambda"]) for q in lrows)
            ),
            "lambda_shift_abs_max":float(
                max((q["lambda_shift_abs_max"] for q in lrows),default=math.inf)
            ),
            "lambda_anisotropy_abs_max":float(
                max((q["lambda_anisotropy_abs_max"] for q in lrows),default=math.inf)
            ),
        },
        "frozen_active_mask":{
            "S_ref":float(sref),
            "near_null_threshold":float(null_thr),
            "active_sample_count":int(active_count),
        },
        "factor1_reproduction":{
            "Z21_global_relative_L2":float(state_repro),
            "shift_metric_global_relative_L2":float(shift_repro),
            "projected_p0_exact":bool(p0_exact),
        },
        "substep_results":{
            str(f):{
                **summaries[f],
                "canonical_Radau_and_algebraic_linear_residual_max":runs[f]["linear_residual_max"],
                "all_outputs_finite":runs[f]["all_outputs_finite"],
            }
            for f in SUBSTEP_FACTORS
        },
        "convergence":{
            "Linf_factor2_over_factor1":r12,
            "Linf_factor4_over_factor2":r24,
            "Linf_order_factor1_to_factor2":p12,
            "Linf_order_factor2_to_factor4":p24,
            "RMS_order_factor1_to_factor2":rp12,
            "RMS_order_factor2_to_factor4":rp24,
            "material_improvement_ratio_max":MATERIAL_RATIO_MAX,
            "third_order_confirmation_min":ORDER_CONFIRM_MIN,
        },
        "implementation_gates":implementation_gates,
        "diagnostic_flags":{
            "Radau_propagation_floor_confirmed":radau_confirmed,
            "propagation_accuracy_dependence_confirmed":accuracy_dependence,
        },
        "routing":{"next_route":route},
        "Z21_window_local_particular_certified":False,
        "lensing_licensed":False,
        "claim_boundary":"Repair38 is a propagation-only localization diagnostic on the frozen Repair37 Nt128 H4 source and projected boundary. It cannot relabel Repair37 or certify Z21. It changes no H4 physics, source term, threshold, parent, finite-eta assumption or observational input."
    }

    outj=Path(args.json_out)
    outn=Path(args.npz_out)
    outj.parent.mkdir(parents=True,exist_ok=True)
    outj.write_text(json.dumps(report,indent=2,allow_nan=False)+"\n")

    save={
        "x_primary":np.asarray(r37npz["x_primary"],float),
        "beta0":np.asarray(r7.BETAS,float),
        "modes_output":np.asarray(r7.M_SOLVE,int),
        "frozen_S_ref":np.asarray(sref,float),
        "frozen_near_null_threshold":np.asarray(null_thr,float),
    }
    for tag in r7.C_TAGS:
        save[f"{tag}_frozen_active_mask"]=np.asarray(masks[tag],bool)
        for factor in SUBSTEP_FACTORS:
            save[f"{tag}_substep{factor}_Z21"]=runs[factor]["states"][tag]
            save[f"{tag}_substep{factor}_shift_metric"]=runs[factor]["metrics"][tag]
            save[f"{tag}_substep{factor}_shift_abs"]=runs[factor]["absres"][tag]
            save[f"{tag}_substep{factor}_shift_scale"]=runs[factor]["scales"][tag]
    np.savez_compressed(outn,**save)

    print(json.dumps(report,indent=2,allow_nan=False))
    if not impl_ok:
        raise SystemExit(3)


if __name__=="__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:
        print(json.dumps({
            "classification":"GE19_REPAIR38_FROZEN_SOURCE_RADAU_SUBSTEP_LOCALIZATION_IMPLEMENTATION_FAIL",
            "error":repr(exc),
            "Z21_window_local_particular_certified":False,
            "lensing_licensed":False,
        },indent=2))
        raise
