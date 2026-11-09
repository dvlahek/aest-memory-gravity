#!/usr/bin/env python3
"""GE19 LW06: source-level signed matter-Weyl cross-power from frozen LW01.

Exactly archived native (k,z), no new CLASS, no k/z interpolation, no
observations. A PASS licenses only a Newtonian-gauge mathematical cross
transfer; NOT galaxy bias, shear, source redshift kernels or a survey fit.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/"ge19/lw06_native_matter_weyl_cross_predata_20261109.json"
PRE_BLOB="5b9811d04ad934d3c1a1c3fcad18505fd79ea6ff"
TINY=1.e-300


def require(ok,name):
    if not bool(ok):
        raise RuntimeError("GE19_LW06_"+name)


def sha256(p):
    h=hashlib.sha256()
    with Path(p).open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):
            h.update(b)
    return h.hexdigest()


def rel_l2(delta,reference):
    return float(np.linalg.norm(delta)/max(np.linalg.norm(reference),TINY))


def selftest():
    # Algebra at a node where the Weyl field vanishes, and signed
    # invariance under simultaneous sign changes of both transfers.
    d=np.array([2.,-3.,4.]);w=np.array([5.,0.,-1.])
    dd=np.array([.1,.2,.3]);dw=np.array([.4,.5,.6])
    derivative=dd*w+d*dw
    eps=1.e-5
    direct=((d+eps*dd)*(w+eps*dw) -
            (d-eps*dd)*(w-eps*dw))/(2*eps)
    require(np.max(abs(derivative-direct))<1.e-10,
            "SELFTEST_SYMMETRIC_DERIVATIVE")
    require(np.array_equal(derivative,(-dd)*(-w)+(-d)*(-dw)),
            "SELFTEST_SIMULTANEOUS_SIGN")
    require(np.all(np.isfinite(derivative)),"SELFTEST_ZERO_CROSS")
    print("GE19_LW06_NATIVE_CROSS_SYNTHETIC_SELFTEST_PASS",flush=True)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--self-test",action="store_true")
    ap.add_argument("--lw01-prefix",type=Path,default=ROOT/
                    "results/ge19_linear_weyl_native_tangent_20261109_kgridfix")
    ap.add_argument("--lw05-json",type=Path,default=ROOT/
                    "results/ge19_lw05_line_of_sight_domain_audit_20261109.json")
    ap.add_argument("--output-prefix",type=Path,default=ROOT/
                    "results/ge19_lw06_native_matter_weyl_cross_20261109")
    args=ap.parse_args()
    if args.self_test:
        selftest()
        return
    digest=subprocess.check_output(["git","hash-object",str(PRE)],
                                   text=True).strip()
    require(digest==PRE_BLOB,"PREDATA_GIT_BLOB_CHANGED")
    pre=json.loads(PRE.read_text())
    require(pre["protocol"]==
            "GE19_LW06_SIGNED_NATIVE_MATTER_WEYL_CROSS_PREDATA_LOCKED",
            "PREDATA_CHANGED")
    pp=args.lw01_prefix.resolve()
    pj=Path(str(pp)+".json")
    pn=Path(str(pp)+".npz")
    prior=args.lw05_json.resolve()
    parent=pre["frozen_parent"]
    for p,d in [(pj,parent["lw01_json_sha256"]),
                (pn,parent["lw01_npz_sha256"]),
                (prior,parent["lw05_json_sha256"])]:
        require(p.is_file() and sha256(p)==d,"PARENT_SHA_"+p.name)

    j=json.loads(pj.read_text())
    five=json.loads(prior.read_text())
    require(j["classification"]==parent["archived_classification"]
            and j["class_official_HEAD"]==parent["CLASS_HEAD"]
            and all(j["gates"].values()),"LW01_NOT_FROZEN_PASS")
    require(five["classification"]==
            "GE19_LW05_FULL_LOS_DOMAIN_BLOCKED_BY_CERTIFIED_KZ_SUPPORT",
            "LW05_STOP_NOT_PRESERVED")
    with np.load(pn,allow_pickle=False) as f:
        a={k:np.array(f[k],copy=True) for k in f.files}
    k=a["k_native_h"]
    z=a["z_native"]
    mask=a["primary_mask"]
    lam=a["lambdas"]
    require(mask.shape==(912,24) and k.shape==(912,) and
            z.shape==(24,) and int(np.sum(mask))==2576 and
            np.all(np.diff(k)>0) and np.all(np.diff(z)<0),
            "NATIVE_GRID_CHANGED")
    require(np.array_equal(lam,np.array(pre["sources"]["lambdas"])),
            "NUMERICAL_LAMBDA_CHANGED")
    ki=np.where(mask.any(axis=1))[0]
    zi=np.where(mask.any(axis=0))[0][::-1]
    require(ki.size==322 and zi.size==8,"PRIMARY_WINDOW_CHANGED")
    exact=(k[:,None]>=.03)&(k[:,None]<=.2)&(z[None,:]>=.2)&(z[None,:]<=1.5)
    require(np.array_equal(mask,exact),"NATIVE_MASK_CHANGED")

    cosmo=parent["cosmology"]
    h=cosmo["H0"]/100.
    kphys=k[ki]*h
    P=(2*np.pi**2/kphys**3)*cosmo["As"]*(
       kphys/cosmo["pivot_k_Mpc_inverse"])**(cosmo["ns"]-1)
    P=P[:,None]
    sl=np.ix_(ki,zi)
    d=a["matter_base"][sl]
    w=a["weyl_base"][sl]
    dm=a["matter_tangents"][:,ki,:][:,:,zi]
    dw=a["weyl_tangents"][:,ki,:][:,:,zi]
    require(dm.shape==dw.shape==(4,322,8),"SIGNED_ARRAY_SHAPE")
    require(np.all(np.isfinite(d)) and np.all(np.isfinite(w)) and
            np.all(np.isfinite(dm)) and np.all(np.isfinite(dw)),
            "INPUT_NONFINITE")

    Pdd=P*d*d
    Pww=P*w*w
    Pdw=P*d*w
    additive_terms=(P[None,:,:]*dm*w[None,:,:],
                    P[None,:,:]*d[None,:,:]*dw)
    per_lambda=additive_terms[0]+additive_terms[1]
    mean=np.mean(per_lambda,axis=0)
    dmbar=a["matter_signed_mean"][sl]
    dwbar=a["weyl_signed_mean"][sl]
    mean_from_parents=P*(dmbar*w+d*dwbar)
    bmean_rel=rel_l2(mean-mean_from_parents,mean)
    wcheck=rel_l2(
        w-.5*(a["phi_base"][sl]+a["psi_base"][sl]),w)
    affinities=[rel_l2(per_lambda[i]-mean,mean)
                for i in range(len(lam))]
    power_bound=float(np.max(np.abs(Pdw**2-Pdd*Pww))/
                      max(np.max(np.abs(Pdd*Pww)),TINY))
    ratio=float(np.linalg.norm(mean)/max(np.linalg.norm(Pdw),TINY))
    lim=pre["preregistered_numerical_gates"]
    gates={
        "original_signed_Weyl_dictionary":
            wcheck<=lim["transfer_weyl_half_phi_plus_psi_max_relative_L2"],
        "exact_signed_bilinear_product_rule":
            bmean_rel<=lim["cross_mean_vs_mean_field_product_rule_max_relative_L2"],
        "cross_lambda_affinity":
            max(affinities)<=lim["linear_cross_lambda_affinity_max"],
        "nonzero_cross_tangent":
            ratio>=lim["linear_cross_tangent_L2_over_baseline_min"],
        "common_adiabatic_mode_power_bound":
            power_bound<=lim["algebraic_per_node_cross_power_bound_max_normalized_absolute_error"],
        "all_finite":
            all(np.isfinite(y).all() for y in
                (Pdd,Pww,Pdw,per_lambda,mean))
    }
    rows=[]
    for iz in range(8):
        rows.append({
            "z":float(z[zi[iz]]),
            "cross_power_negative_nodes":int(np.sum(Pdw[:,iz]<0)),
            "cross_power_positive_nodes":int(np.sum(Pdw[:,iz]>0)),
            "signed_cross_tangent_negative_nodes":int(np.sum(mean[:,iz]<0)),
            "signed_cross_tangent_positive_nodes":int(np.sum(mean[:,iz]>0)),
            "signed_cross_tangent_L2_over_baseline_L2":
                float(np.linalg.norm(mean[:,iz])/
                      max(np.linalg.norm(Pdw[:,iz]),TINY)),
        })
    outcome=(pre["scientific_interpretation"]["pass"]
             if all(gates.values()) else
             pre["scientific_interpretation"]["fail"])
    report={
        "classification":outcome,
        "predata_git_blob_sha1":PRE_BLOB,
        "frozen_parent_sha256":{
            "lw01_json":sha256(pj),"lw01_npz":sha256(pn),
            "lw05_json":sha256(prior)},
        "k_native_primary_h_per_Mpc":[float(k[ki[0]]),float(k[ki[-1]])],
        "z_native_primary_ascending":z[zi].tolist(),
        "shape":[322,8],
        "native_nodes":2576,
        "physical_gauge":"conformal Newtonian CLASS d_m versus W=(phi+psi)/2",
        "primordial_k_pivot_Mpc_inverse":cosmo["pivot_k_Mpc_inverse"],
        "numerical_amplifications":lam.tolist(),
        "weyl_dictionary_relative_L2":wcheck,
        "bilinear_product_rule_relative_L2":bmean_rel,
        "common_mode_power_bound_relative":power_bound,
        "signed_cross_lambda_affinity_relative_L2":affinities,
        "signed_cross_tangent_norm_to_baseline_cross_norm":ratio,
        "cross_power_negative_nodes":int(np.sum(Pdw<0)),
        "cross_power_positive_nodes":int(np.sum(Pdw>0)),
        "signed_cross_tangent_negative_nodes":int(np.sum(mean<0)),
        "signed_cross_tangent_positive_nodes":int(np.sum(mean>0)),
        "by_z":rows,
        "gates":gates,
        "LW03_radial_quadrature_FAIL_preserved":True,
        "LW04_source_time_sampling_PASS_preserved":True,
        "LW05_full_LOS_domain_BLOCK_preserved":True,
        "galaxy_galaxy_lensing_certified":False,
        "full_lensing_spectrum_certified":False,
        "observational_detection":False,
        "finite_physical_eta_calibrated":False,
        "H4_Z21_certified":False,
        "interpretation":"Signed Newtonian gauge matter-Weyl transfer product only. Not a galaxy shear spectrum, observed galaxy density transfer, calibrated finite memory coupling, full LOS, or model selection.",
    }
    output=args.output_prefix.resolve()
    jp=Path(str(output)+".json")
    npzout=Path(str(output)+".npz")
    require(output.parent.is_dir() and
            not jp.exists() and not npzout.exists(),
            "OUTPUT_PREEXISTS_OR_PARENT_MISSING")
    jp.write_text(json.dumps(report,indent=2,sort_keys=True,
                             allow_nan=False)+"\n")
    np_save={
        "k_primary_h":k[ki],"z_primary":z[zi],
        "primordial_power_3D_by_k":P[:,0],
        "P_matter_matter":Pdd,"P_Weyl_Weyl":Pww,
        "P_matter_Weyl":Pdw,
        "signed_cross_tangent_by_lambda":per_lambda,
        "signed_cross_tangent_mean":mean,
        "signed_cross_tangent_matter_contribution_mean":
            np.mean(additive_terms[0],axis=0),
        "signed_cross_tangent_weyl_contribution_mean":
            np.mean(additive_terms[1],axis=0),
    }
    np.savez_compressed(npzout,**np_save)
    print("GE19_LW06_CLASSIFICATION",outcome,flush=True)
    print("GE19_LW06_MAX_AFFINITY",max(affinities),flush=True)
    print("GE19_LW06_OUTPUT",str(jp),str(npzout),flush=True)


if __name__=="__main__":
    main()
