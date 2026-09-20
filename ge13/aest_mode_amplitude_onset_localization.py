#!/usr/bin/env python3
"""GE13 diagnostic localization of AeST per-k amplitude onset.

Uses only frozen GE11 Repair01 dense traces and the frozen GE12 late-window
localization artifact. No CLASS execution and no new physics.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.interpolate import CubicHermiteSpline, PchipInterpolator

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

import ge09.repair01_dense_accepted_step_local_jet_bridge as g9

GE11_ID=10600652596
GE11_DIGEST="sha256:b35a3a0c8bbd22483bd04c006b20ceb97d3c7f263e178382026cba2983628ecc"
GE12_ID=10602610942
GE12_DIGEST="sha256:2b44a0c38d1a3aadcb05f1ed743560a68817e720dcb4d2cc41fe040d0b409fd9"
R1_SHA="c50aae91fee94f00e1cbb5bd3c4d9352f15d892e91b230fad690f06c43e25fbd"
R2_SHA="5a9480f69744db59ab8ca7fbdef56398c5fe38493730976d92b25873f46379b1"
GE11_CLASS="GE11_REPAIR01_DENSE_LOCAL_JET_FIXED_REFINEMENT_FAIL"
GE12_CLASS="GE12_GE11_R1_R2_STATE_DIVERGENCE_LOCALIZED"
THRESHOLDS=(1e-3,1e-2,5e-2,1e-1)
CHANNELS=("alpha_aest","E_aest","chi","ut_kernel")
NSAMP=4096
TINY=1e-300


def unique_find(root:Path,name:str)->Path:
    hits=sorted(p for p in root.rglob(name) if p.is_file())
    if len(hits)!=1:
        raise RuntimeError(f"expected exactly one {name} under {root}, found {len(hits)}")
    return hits[0]


def sha256(path:Path)->str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def meta_ok(path:Path,aid:int,digest:str)->bool:
    d=json.loads(path.read_text())
    return bool(int(d.get("id",-1))==aid and d.get("digest")==digest and d.get("expired") is False)


def ls_scale(x,y):
    xx=np.asarray(x,float).ravel(); yy=np.asarray(y,float).ravel()
    den=float(np.dot(xx,xx))
    if den<=TINY:
        return math.nan,math.nan,math.nan
    c=float(np.dot(xx,yy)/den)
    res=float(np.linalg.norm(yy-c*xx)/max(np.linalg.norm(yy),TINY))
    co=float(np.dot(xx,yy)/max(np.linalg.norm(xx)*np.linalg.norm(yy),TINY))
    return c,res,co


def aor_scalar(a,b):
    ae=abs(a-b)
    re=ae/max(abs(a),abs(b),TINY)
    return min(ae,re)


def read_dense(path:Path):
    df=pd.read_csv(path,sep=r"\s+",engine="c")
    required=("k","a","H_over_H0","alpha_aest","alpha_prime")
    missing=[c for c in required if c not in df.columns]
    if missing:
        raise RuntimeError(f"{path.name}: missing columns {missing}")
    if not np.all(np.isfinite(df[list(required)].to_numpy(float))):
        raise RuntimeError(f"{path.name}: nonfinite required values")
    return df


def dedup_arrays(df):
    # Same near-identical ln(a) grouping rule as GE09, implemented on a single k.
    df=df.sort_values("a")
    rows=df.to_dict("records")
    groups=[];cur=[];center=None
    for r in rows:
        x=math.log(r["a"])
        if center is None or abs(x-center)<=1e-13*max(1.0,abs(x),abs(center)):
            cur.append(r)
            center=float(np.median([math.log(z["a"]) for z in cur]))
        else:
            groups.append(cur);cur=[r];center=x
    if cur: groups.append(cur)
    keys=rows[0].keys()
    out={k:np.asarray([float(np.median([r[k] for r in grp])) for grp in groups],float) for k in keys}
    return out


def alpha_interps(df,k_target):
    unique=np.asarray(sorted(df["k"].unique()),float)
    kval=float(unique[np.argmin(np.abs(unique-k_target))])
    relmiss=abs(kval-k_target)/max(abs(k_target),TINY)
    if relmiss>1e-12:
        raise RuntimeError(f"k miss {relmiss} for target {k_target}")
    a=dedup_arrays(df[df["k"]==kval])
    x=np.log(a["a"])
    H=a["H_over_H0"]*g9.H0_CLASS
    calH=a["a"]*H
    if np.any(np.diff(x)<=0) or np.any(calH<=0):
        raise RuntimeError("invalid dense interpolation grid")
    alpha=CubicHermiteSpline(x,a["alpha_aest"],a["alpha_prime"]/calH,extrapolate=False)
    hub=PchipInterpolator(x,a["H_over_H0"],extrapolate=False)
    return alpha,hub,x,float(kval),float(relmiss)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--ge11-root",required=True)
    ap.add_argument("--ge12-root",required=True)
    ap.add_argument("--ge11-meta-json",required=True)
    ap.add_argument("--ge12-meta-json",required=True)
    ap.add_argument("--json-out",required=True)
    ap.add_argument("--npz-out",required=True)
    args=ap.parse_args()

    r11=Path(args.ge11_root).resolve()
    r12=Path(args.ge12_root).resolve()

    ge11_meta=meta_ok(Path(args.ge11_meta_json),GE11_ID,GE11_DIGEST)
    ge12_meta=meta_ok(Path(args.ge12_meta_json),GE12_ID,GE12_DIGEST)

    ge11_json=unique_find(r11,"ge11_repair01_dense_local_jet_fixed_refinement.json")
    ge12_json=unique_find(r12,"ge12_ge11_r1_r2_state_divergence_localization.json")
    ge12_npz=unique_find(r12,"ge12_ge11_r1_r2_state_divergence_localization.npz")
    r1_path=unique_find(r11,"ge11r1_R1_dense_accepted_step_trace.dat")
    r2_path=unique_find(r11,"ge11r1_R2_dense_accepted_step_trace.dat")

    j11=json.loads(ge11_json.read_text())
    j12=json.loads(ge12_json.read_text())
    parent_classes_ok=bool(j11.get("classification")==GE11_CLASS and j12.get("classification")==GE12_CLASS)
    dense_hashes_ok=bool(sha256(r1_path)==R1_SHA and sha256(r2_path)==R2_SHA)

    # Reproduce GE12 global late-window scale fits directly from the frozen NPZ.
    z12=np.load(ge12_npz)
    global_scale_reproduction={}
    max_scale_err=0.0
    for ch in CHANNELS:
        c,res,co=ls_scale(z12[f"R1_{ch}"],z12[f"R2_{ch}"])
        target=float(j12["least_squares_scale_fits"][ch]["R2_over_R1_least_squares_scale"])
        err=abs(c-target)
        max_scale_err=max(max_scale_err,err)
        global_scale_reproduction[ch]={
            "scale":c,"target_GE12_scale":target,"abs_error":err,
            "post_rescaling_relative_L2":res,"cosine":co,
        }

    # Per-k late-window exact amplitude/shape localization from GE12 arrays.
    per_k={}
    all_finite=True
    for ch in CHANNELS:
        A=np.asarray(z12[f"R1_{ch}"],float)
        B=np.asarray(z12[f"R2_{ch}"],float)
        rows=[]
        for ik,kh in enumerate(g9.K_H):
            c,res,co=ls_scale(A[ik],B[ik])
            rows.append({
                "k_h_Mpc":float(kh),
                "scale_R2_over_R1":c,
                "post_rescaling_relative_L2":res,
                "cosine":co,
            })
            all_finite=bool(all_finite and np.isfinite(c) and np.isfinite(res) and np.isfinite(co))
        per_k[ch]=rows

    # Channel-to-channel spread of the per-k scales.
    per_k_scale_spread=[]
    for ik,kh in enumerate(g9.K_H):
        vals=[per_k[ch][ik]["scale_R2_over_R1"] for ch in CHANNELS]
        per_k_scale_spread.append({
            "k_h_Mpc":float(kh),
            "scale_min":float(min(vals)),
            "scale_max":float(max(vals)),
            "scale_spread":float(max(vals)-min(vals)),
            "scale_mean":float(np.mean(vals)),
        })

    # Full accepted-step history onset using the same physical alpha derivative.
    df1=read_dense(r1_path); df2=read_dense(r2_path)
    histories=[]
    hist_save={}
    for ik,(k,kh) in enumerate(zip(g9.K_REQ,g9.K_H)):
        a1,h1,x1,k1,miss1=alpha_interps(df1,float(k))
        a2,h2,x2,k2,miss2=alpha_interps(df2,float(k))
        lo=max(float(x1[0]),float(x2[0]))
        hi=math.log(g9.AMAX)
        xx=np.linspace(lo,hi,NSAMP)
        aa=np.exp(xx)
        y1=np.asarray(a1(xx),float)
        y2=np.asarray(a2(xx),float)
        H2=np.asarray(h2(xx),float)*g9.H0_CLASS

        valid=np.isfinite(y1) & np.isfinite(y2) & (np.abs(y1)>1e-300)
        ratio=np.full_like(y1,np.nan)
        ratio[valid]=y2[valid]/y1[valid]
        if not np.any(valid):
            raise RuntimeError(f"k={k}: no valid alpha ratio samples")

        lower_alpha_r1=float(a1(lo)); lower_alpha_r2=float(a2(lo))
        lower_mismatch=aor_scalar(lower_alpha_r1,lower_alpha_r2)

        crosses={}
        for th in THRESHOLDS:
            ids=np.where(valid & (np.abs(ratio-1.0)>th))[0]
            if len(ids)==0:
                crosses[str(th)]=None
            else:
                j=int(ids[0])
                crosses[str(th)]={
                    "a":float(aa[j]),
                    "z":float(1.0/aa[j]-1.0),
                    "ratio_R2_over_R1":float(ratio[j]),
                    "k_over_aH":float(k/(aa[j]*H2[j])),
                }

        # Sixteen equal-ln(a) bins over full common history.
        edges=np.linspace(lo,hi,17)
        bins=[]
        for ib in range(16):
            if ib<15:
                mask=(xx>=edges[ib])&(xx<edges[ib+1])&valid
            else:
                mask=(xx>=edges[ib])&(xx<=edges[ib+1])&valid
            if not np.any(mask):
                raise RuntimeError(f"k={k}: empty valid history bin {ib}")
            c,res,co=ls_scale(y1[mask],y2[mask])
            bins.append({
                "bin":ib,
                "a_geometric_mid":float(math.exp(0.5*(edges[ib]+edges[ib+1]))),
                "scale":c,"post_rescaling_relative_L2":res,"cosine":co,
            })

        late=per_k["alpha_aest"][ik]
        histories.append({
            "k_Mpc":float(k),"k_h_Mpc":float(kh),
            "R1_k_relative_miss":miss1,"R2_k_relative_miss":miss2,
            "common_a_start":float(math.exp(lo)),
            "first_common_alpha_R1":lower_alpha_r1,
            "first_common_alpha_R2":lower_alpha_r2,
            "first_common_alpha_abs_or_rel_mismatch":lower_mismatch,
            "departure_crossings":crosses,
            "late_plateau_scale":late["scale_R2_over_R1"],
            "late_plateau_post_rescaling_relative_L2":late["post_rescaling_relative_L2"],
            "history_bins":bins,
        })
        hist_save[f"k{ik}_ln_a"]=xx
        hist_save[f"k{ik}_alpha_ratio"]=ratio
        all_finite=bool(
            all_finite and np.isfinite(lower_mismatch)
            and np.all(np.isfinite(y1)) and np.all(np.isfinite(y2))
            and np.all(np.isfinite(H2))
        )

    # Frozen IC source provenance.
    ic_txt=(ROOT/"v019i"/"apply_ic_patch.py").read_text()
    ic_checks={
        "alpha_i_identity_present":"-ppw->pvecback[pba->index_bg_a]*ppw->pv->y[ppw->pv->index_pt_theta_cdm]/(k*k)" in ic_txt,
        "E_i_zero_present":"ppw->pv->y[ppw->pv->index_pt_E_aest] = 0.;" in ic_txt,
        "adiabatic_density_identity_present":"index_pt_delta_cdm] *= (1.+w_aest_ini)" in ic_txt,
    }

    gates={
        "GE11_parent_artifact_digest_exact":ge11_meta,
        "GE12_parent_artifact_digest_exact":ge12_meta,
        "both_parent_classifications_exact":parent_classes_ok,
        "dense_trace_hashes_exact":dense_hashes_ok,
        "GE12_late_scales_reproduced_abs_error_le_1e12":bool(max_scale_err<=1e-12),
        "common_history_interpolation_finite":all_finite,
        "frozen_IC_source_identities_present":bool(all(ic_checks.values())),
        "all_reported_quantities_finite":all_finite,
    }
    passed=bool(all(gates.values()))
    classification=(
        "GE13_AEST_MODE_AMPLITUDE_ONSET_LOCALIZED"
        if passed else
        "GE13_AEST_MODE_AMPLITUDE_ONSET_DIAGNOSTIC_FAIL"
    )

    result={
        "classification":classification,
        "predata_classification":"GE13_PREDATA_AEST_MODE_AMPLITUDE_ONSET_LOCALIZATION",
        "scope":"Diagnostic-only localization of the frozen R1/R2 AeST per-k amplitude factor and its onset; no new CLASS run or precision level.",
        "parent_provenance":{
            "GE11_artifact_exact":ge11_meta,
            "GE12_artifact_exact":ge12_meta,
            "GE11_classification":j11.get("classification"),
            "GE12_classification":j12.get("classification"),
            "R1_dense_sha256":sha256(r1_path),
            "R2_dense_sha256":sha256(r2_path),
        },
        "GE12_global_scale_reproduction":global_scale_reproduction,
        "GE12_global_scale_reproduction_abs_error_max":max_scale_err,
        "late_per_k_scale_shape":per_k,
        "late_per_k_channel_scale_spread":per_k_scale_spread,
        "full_history_alpha_onset":histories,
        "IC_source_provenance":ic_checks,
        "gates":gates,
        "project_boundary":{
            "GE11_relabelled":False,
            "R1_selected":False,
            "R2_selected":False,
            "R3_licensed":False,
            "IC_modified":False,
            "physical_instability_claimed":False,
            "Z20_licensed":False,
        },
        "claim_boundary":"GE13 localizes only the onset and per-k amplitude structure of the frozen R1/R2 difference. It cannot relabel GE11, select a precision level, add R3, modify ICs, claim a physical instability, or license Z20.",
    }

    outj=Path(args.json_out); outj.parent.mkdir(parents=True,exist_ok=True)
    outj.write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
    save={"k_Mpc":g9.K_REQ,"k_h_Mpc":g9.K_H}
    save.update(hist_save)
    np.savez_compressed(args.npz_out,**save)
    print(json.dumps(result,indent=2,allow_nan=False))
    if not passed:
        raise SystemExit(2)


if __name__=="__main__":
    main()
