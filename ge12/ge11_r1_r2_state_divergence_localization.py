#!/usr/bin/env python3
"""GE12 diagnostic localization of the frozen GE11 Repair01 R1/R2 divergence.

No CLASS execution and no new physics. Reconstructs exactly the frozen GE09/
GE11 common-ln(a) first-order state and GE06 local jet from the retained R1/R2
dense accepted-step traces.
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

import ge09.repair01_dense_accepted_step_local_jet_bridge as g9

PARENT_CLASS="GE11_REPAIR01_DENSE_LOCAL_JET_FIXED_REFINEMENT_FAIL"
ARTIFACT_ID=10600652596
ARTIFACT_DIGEST="sha256:b35a3a0c8bbd22483bd04c006b20ceb97d3c7f263e178382026cba2983628ecc"
R1_SHA="c50aae91fee94f00e1cbb5bd3c4d9352f15d892e91b230fad690f06c43e25fbd"
R2_SHA="5a9480f69744db59ab8ca7fbdef56398c5fe38493730976d92b25873f46379b1"
PARENT_GL=0.45886068704381233
PARENT_PT=0.7829092344800966
TINY=1e-300

RAW_CHANNELS=(
    "phi","psi","delta_dark","theta_dark","alpha_aest","E_aest",
    "Q","H_over_H0","rho_dark","p_dark","cad2_dark",
    "phi_prime_interp","delta_dark_prime_interp","theta_dark_prime_interp",
    "alpha_aest_prime_interp","E_aest_prime_interp",
)
DERIVED_CHANNELS=("uA","varphi","chi","Pi","pt","ut_kernel","u_kernel")
SCALE_CHANNELS=("alpha_aest","theta_dark","E_aest","uA","varphi","chi","Pi","pt","ut_kernel")
PER_K_CHANNELS=("alpha_aest","theta_dark","E_aest","chi","varphi","pt")


def unique_find(root:Path,name:str)->Path:
    hits=sorted(p for p in root.rglob(name) if p.is_file())
    if len(hits)!=1:
        raise RuntimeError(f"expected exactly one {name} under {root}, found {len(hits)}")
    return hits[0]


def sha256(path:Path)->str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def cosine(a,b):
    aa=np.asarray(a,float).ravel(); bb=np.asarray(b,float).ravel()
    return float(np.dot(aa,bb)/max(np.linalg.norm(aa)*np.linalg.norm(bb),TINY))


def metrics(a,b):
    aa=np.asarray(a,float); bb=np.asarray(b,float)
    return {
        "global_relative_L2":g9.rel_l2(aa,bb),
        "pointwise_abs_or_rel_max":g9.aor(aa,bb),
        "cosine":cosine(aa,bb),
    }


def ls_scale(r1,r2):
    x=np.asarray(r1,float).ravel()
    y=np.asarray(r2,float).ravel()
    den=float(np.dot(x,x))
    if den<=TINY:
        return math.nan,math.nan
    c=float(np.dot(x,y)/den)
    residual=float(np.linalg.norm(y-c*x)/max(np.linalg.norm(y),TINY))
    return c,residual


def state_from_trace(path:Path):
    rows=g9.read_table(path)
    modes,kmiss=g9.group_modes(rows)
    interps=[]
    for m in modes:
        if m[0]["a"]>g9.AMIN or m[-1]["a"]<g9.AMAX:
            raise RuntimeError(f"{path.name}: accepted trace does not bracket frozen window")
        interps.append(g9.build_interps(m))
    x=np.linspace(math.log(g9.AMIN),math.log(g9.AMAX),g9.NCOMMON)
    a=np.exp(x)
    states=[]
    for interp in interps:
        states.append(g9.eval_state(interp,x))
    return rows,modes,states,x,a,float(kmiss)


def stack_raw(states,name):
    return np.asarray([s[name] for s in states],float)


def derive(states,a):
    out={k:[] for k in DERIVED_CHANNELS}
    jets_cos={name:[] for name in g9.JET_NAMES}
    jets_sin={name:[] for name in g9.JET_NAMES}
    identity_errors=[]
    for ik,k in enumerate(g9.K_REQ):
        s=states[ik]
        H=s["H_over_H0"]*g9.H0_CLASS
        Q=s["Q"]
        phi=s["phi"]
        psi=s["psi"]
        delta=s["delta_dark"]
        theta=s["theta_dark"]
        alpha=s["alpha_aest"]
        E=s["E_aest"]
        rho=s["rho_dark"]
        p=s["p_dark"]
        c2=s["cad2_dark"]

        uA=a*theta/(k*k)
        varphi=Q*uA
        chi=Q*(uA+alpha)
        Pi=c2*delta+c2*k*k/(3.0*a*a*rho)*(g9.KB*E+(2.0-g9.KB)*chi)
        pt=Q*(psi+Pi/(1.0+p/rho))
        ut_kernel=H*alpha-E+psi
        u_kernel=alpha

        vals={
            "uA":uA,"varphi":varphi,"chi":chi,"Pi":Pi,"pt":pt,
            "ut_kernel":ut_kernel,"u_kernel":u_kernel,
        }
        for name in DERIVED_CHANNELS:
            out[name].append(np.asarray(vals[name],float))

        jc,js,diag=g9.jet_from_state(s,a,k)
        for name in g9.JET_NAMES:
            jets_cos[name].append(jc[name])
            jets_sin[name].append(js[name])

        # Exact dictionary identities tying diagnostics to the frozen jet map.
        identity_errors.extend([
            g9.aor(js["u"],-(k/a)*u_kernel),
            g9.aor(js["ut"],(k/a)*ut_kernel),
            g9.aor(js["px"],-k*varphi),
            g9.aor(jc["pt"],pt),
            g9.aor(diag["chi"],chi),
            g9.aor(diag["Pi"],Pi),
            g9.aor(diag["varphi"],varphi),
            g9.aor(diag["pt"],pt),
        ])

    for d in (out,jets_cos,jets_sin):
        for name in d:
            d[name]=np.asarray(d[name],float)
    return out,jets_cos,jets_sin,float(max(identity_errors,default=math.inf))


def compare_jets(c1,s1,c2,s2):
    by={}
    glmax=0.0; ptmax=0.0
    for name in g9.JET_NAMES:
        a=np.concatenate([c1[name].ravel(),s1[name].ravel()])
        b=np.concatenate([c2[name].ravel(),s2[name].ravel()])
        gl=g9.rel_l2(a,b); pp=g9.aor(a,b)
        by[name]={"global_relative_L2":gl,"pointwise_abs_or_rel_max":pp}
        glmax=max(glmax,gl); ptmax=max(ptmax,pp)
    return by,float(glmax),float(ptmax)


def channel_dict(states,derived):
    d={name:stack_raw(states,name) for name in RAW_CHANNELS}
    d.update({name:np.asarray(derived[name],float) for name in DERIVED_CHANNELS})
    return d


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--artifact-root",required=True)
    ap.add_argument("--artifact-meta-json",required=True)
    ap.add_argument("--json-out",required=True)
    ap.add_argument("--npz-out",required=True)
    args=ap.parse_args()

    root=Path(args.artifact_root).resolve()
    meta=json.loads(Path(args.artifact_meta_json).read_text())
    artifact_ok=bool(
        int(meta.get("id",-1))==ARTIFACT_ID
        and meta.get("digest")==ARTIFACT_DIGEST
        and meta.get("expired") is False
    )

    parent_json=unique_find(root,"ge11_repair01_dense_local_jet_fixed_refinement.json")
    r1_path=unique_find(root,"ge11r1_R1_dense_accepted_step_trace.dat")
    r2_path=unique_find(root,"ge11r1_R2_dense_accepted_step_trace.dat")
    parent=json.loads(parent_json.read_text())
    parent_ok=bool(parent.get("classification")==PARENT_CLASS)

    r1_hash=sha256(r1_path); r2_hash=sha256(r2_path)
    hashes_ok=bool(r1_hash==R1_SHA and r2_hash==R2_SHA)

    rows1,modes1,states1,x1,a1,km1=state_from_trace(r1_path)
    rows2,modes2,states2,x2,a2,km2=state_from_trace(r2_path)
    common_ok=bool(
        len(x1)==g9.NCOMMON==64 and len(x2)==g9.NCOMMON
        and np.array_equal(x1,x2) and np.array_equal(a1,a2)
    )

    d1,jc1,js1,id1=derive(states1,a1)
    d2,jc2,js2,id2=derive(states2,a2)
    exact_identity=max(id1,id2)

    ch1=channel_dict(states1,d1)
    ch2=channel_dict(states2,d2)

    channel_metrics={}
    all_finite=True
    for name in RAW_CHANNELS+DERIVED_CHANNELS:
        mm=metrics(ch1[name],ch2[name])
        channel_metrics[name]=mm
        all_finite=bool(
            all_finite
            and np.all(np.isfinite(ch1[name]))
            and np.all(np.isfinite(ch2[name]))
            and all(np.isfinite(list(mm.values())))
        )

    scale_fits={}
    for name in SCALE_CHANNELS:
        sc,res=ls_scale(ch1[name],ch2[name])
        scale_fits[name]={"R2_over_R1_least_squares_scale":sc,
                          "post_rescaling_relative_L2":res}
        all_finite=bool(all_finite and np.isfinite(sc) and np.isfinite(res))

    per_k={}
    for name in PER_K_CHANNELS:
        per_k[name]=[
            g9.rel_l2(ch1[name][ik],ch2[name][ik])
            for ik in range(len(g9.K_REQ))
        ]

    # Eight equal ln(a) bins; fit one scale over all six k modes in each bin.
    edges=np.linspace(x1[0],x1[-1],9)
    time_bin_scales={name:[] for name in SCALE_CHANNELS}
    for ib in range(8):
        if ib<7:
            mask=(x1>=edges[ib])&(x1<edges[ib+1])
        else:
            mask=(x1>=edges[ib])&(x1<=edges[ib+1])
        if not np.any(mask):
            raise RuntimeError(f"empty ln(a) bin {ib}")
        for name in SCALE_CHANNELS:
            sc,res=ls_scale(ch1[name][:,mask],ch2[name][:,mask])
            time_bin_scales[name].append({
                "bin":ib,
                "ln_a_min":float(edges[ib]),
                "ln_a_max":float(edges[ib+1]),
                "scale":sc,
                "post_rescaling_relative_L2":res,
            })
            all_finite=bool(all_finite and np.isfinite(sc) and np.isfinite(res))

    jet_by,jet_gl,jet_pt=compare_jets(jc1,js1,jc2,js2)
    parent_gl=float(parent["refinement_control"]["global_relative_L2_max"])
    parent_pt=float(parent["refinement_control"]["pointwise_abs_or_rel_max"])
    gl_repro_err=abs(jet_gl-parent_gl)
    pt_repro_err=abs(jet_pt-parent_pt)

    gates={
        "artifact_digest_exact":artifact_ok,
        "parent_classification_exact":parent_ok,
        "dense_trace_hashes_exact":hashes_ok,
        "common_grid_nodes_exact_64":common_ok,
        "reconstructed_parent_cross_jet_global_relative_L2_abs_error_le_1e12":bool(gl_repro_err<=1e-12),
        "reconstructed_parent_cross_jet_pointwise_abs_or_rel_abs_error_le_1e12":bool(pt_repro_err<=1e-12),
        "exact_derived_identity_abs_or_rel_le_1e12":bool(exact_identity<=1e-12),
        "all_quantities_finite":all_finite,
    }
    passed=bool(all(gates.values()))
    classification=(
        "GE12_GE11_R1_R2_STATE_DIVERGENCE_LOCALIZED"
        if passed else
        "GE12_GE11_R1_R2_STATE_DIVERGENCE_DIAGNOSTIC_FAIL"
    )

    # Rank channels descriptively by cross-level global disagreement.
    ranked=sorted(
        ({"channel":name,**channel_metrics[name]} for name in channel_metrics),
        key=lambda q:q["global_relative_L2"],
        reverse=True,
    )

    result={
        "classification":classification,
        "predata_classification":"GE12_PREDATA_GE11_R1_R2_STATE_DIVERGENCE_LOCALIZATION",
        "scope":"Diagnostic-only localization of the frozen GE11 Repair01 R1/R2 divergence; no new CLASS run, precision choice, interpolation choice, or physics.",
        "artifact":{
            "id":ARTIFACT_ID,
            "digest":ARTIFACT_DIGEST,
            "metadata_exact":artifact_ok,
            "R1_dense_sha256":r1_hash,
            "R2_dense_sha256":r2_hash,
        },
        "parent":{
            "classification":parent.get("classification"),
            "cross_jet_global_relative_L2":parent_gl,
            "cross_jet_pointwise_abs_or_rel_max":parent_pt,
            "reconstructed_global_relative_L2":jet_gl,
            "reconstructed_pointwise_abs_or_rel_max":jet_pt,
            "global_reconstruction_abs_error":gl_repro_err,
            "pointwise_reconstruction_abs_error":pt_repro_err,
        },
        "trace":{
            "R1_rows":len(rows1),"R2_rows":len(rows2),
            "R1_requested_k_relative_miss_max":km1,
            "R2_requested_k_relative_miss_max":km2,
            "common_ln_a_nodes":len(x1),
        },
        "channel_metrics":channel_metrics,
        "channels_ranked_by_global_relative_L2":ranked,
        "least_squares_scale_fits":scale_fits,
        "per_k_global_relative_L2":per_k,
        "time_bin_scale_fits":time_bin_scales,
        "reconstructed_jet_by_entry":jet_by,
        "exact_derived_identity_abs_or_rel_max":exact_identity,
        "gates":gates,
        "project_boundary":{
            "GE11_relabelled":False,
            "R1_selected":False,
            "R2_selected":False,
            "R3_licensed":False,
            "Z20_licensed":False,
            "physical_instability_claimed":False,
        },
        "claim_boundary":"GE12 localizes only the frozen R1/R2 state divergence. It cannot relabel GE11 Repair01, choose a precision level, add R3, alter the local-jet dictionary, license Z20, or make a physical-instability claim.",
    }

    outj=Path(args.json_out); outj.parent.mkdir(parents=True,exist_ok=True)
    outj.write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
    save={"k_Mpc":g9.K_REQ,"k_h_Mpc":g9.K_H,"ln_a":x1,"a":a1}
    for name in RAW_CHANNELS+DERIVED_CHANNELS:
        save[f"R1_{name}"]=ch1[name]
        save[f"R2_{name}"]=ch2[name]
    np.savez_compressed(args.npz_out,**save)
    print(json.dumps(result,indent=2,allow_nan=False))
    if not passed:
        raise SystemExit(2)


if __name__=="__main__":
    main()
